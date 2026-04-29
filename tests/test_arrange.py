"""Tests for the simple node arrangement algorithm."""

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.arrange import (
    arrange_tree,
    build_dependency_graph,
    calculate_node_dimensions,
    organize_into_columns,
    topological_sort,
)


class TestArrangeTree:
    """End-to-end tests for arrange_tree."""

    def test_empty_tree(self):
        """arrange_tree should not crash on an empty node tree."""
        tree = bpy.data.node_groups.new("Empty", "GeometryNodeTree")
        for node in list(tree.nodes):
            tree.nodes.remove(node)
        arrange_tree(tree)

    def test_single_node(self):
        """A single node should be placed at the origin."""
        with TreeBuilder(arrange=None) as tree:
            g.Value()

        arrange_tree(tree.tree)
        value_node = tree.tree.nodes["Value"]
        assert value_node.location.x == 0
        assert value_node.location.y == 0

    def test_linear_chain_left_to_right(self):
        """Nodes in a linear chain should be arranged left-to-right."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out

        arrange_tree(tree.tree)
        nodes = tree.tree.nodes
        set_pos = nodes["Set Position"]
        realize = nodes["Realize Instances"]
        assert set_pos.location.x < realize.location.x

    def test_does_not_delete_nodes(self):
        """arrange_tree must never remove nodes from the tree."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out
            g.Value()

        count_before = len(tree.tree.nodes)
        arrange_tree(tree.tree)
        assert len(tree.tree.nodes) == count_before

    def test_nodes_do_not_overlap_vertically(self):
        """Multiple nodes in the same column should not overlap."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            v1 = g.Value()
            v2 = g.Value()
            add = g.Math.add(v1, v2)
            _ = geo >> g.SetPosition(offset=g.CombineXYZ(x=add)) >> out

        arrange_tree(tree.tree)

        # The two Value nodes should be in the same column,
        # and their y-positions should differ by at least some spacing
        nodes = [n for n in tree.tree.nodes if n.bl_idname == "ShaderNodeValue"]
        assert len(nodes) == 2
        y_positions = sorted([n.location.y for n in nodes], reverse=True)
        assert y_positions[0] > y_positions[1]


class TestBuildDependencyGraph:
    """Tests for build_dependency_graph."""

    def test_excludes_frame_nodes(self):
        """Frame nodes should not appear in the dependency graph."""
        with TreeBuilder(arrange=None) as tree:
            g.Value()

        # Manually add a frame node
        tree.tree.nodes.new("NodeFrame")

        graph, _ = build_dependency_graph(tree.tree)
        bl_idnames = {n.bl_idname for n in graph}
        assert "NodeFrame" not in bl_idnames

    def test_excludes_reroute_nodes(self):
        """Reroute nodes should not appear in the dependency graph."""
        with TreeBuilder(arrange=None) as tree:
            g.Value()

        tree.tree.nodes.new("NodeReroute")

        graph, _ = build_dependency_graph(tree.tree)
        bl_idnames = {n.bl_idname for n in graph}
        assert "NodeReroute" not in bl_idnames

    def test_connection_counts(self):
        """Socket connection counts should reflect the number of incoming links."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out

        _, counts = build_dependency_graph(tree.tree)
        # At least one socket should have a connection
        assert sum(counts.values()) > 0


class TestTopologicalSort:
    """Tests for topological_sort."""

    def test_linear_chain_order(self):
        """Nodes should be sorted so dependencies come before dependents."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out

        graph, _ = build_dependency_graph(tree.tree)
        sorted_nodes = topological_sort(graph)
        names = [n.name for n in sorted_nodes]
        assert names.index("Group Input") < names.index("Set Position")
        assert names.index("Set Position") < names.index("Realize Instances")

    def test_all_nodes_present(self):
        """All layoutable nodes should appear in the sorted output."""
        with g.tree(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out

        graph, _ = build_dependency_graph(tree.tree)
        sorted_nodes = topological_sort(graph)
        assert len(sorted_nodes) == len(graph)


class TestOrganizeIntoColumns:
    """Tests for organize_into_columns."""

    def test_linear_chain_columns(self):
        """A linear chain of N nodes should produce N columns of 1 node each."""
        with g.tree(arrange=None) as tree:
            _ = (
                tree.inputs.geometry()
                >> g.SetPosition()
                >> g.RealizeInstances()
                >> tree.outputs.geometry()
            )

        graph, _ = build_dependency_graph(tree.tree)
        sorted_nodes = topological_sort(graph)
        columns = organize_into_columns(sorted_nodes, graph)

        # Each node in its own column for a linear chain
        for col in columns:
            assert len(col) == 1

    def test_fan_in_shares_column(self):
        """Nodes at the same dependency depth should share a column."""
        with TreeBuilder(arrange=None) as tree:
            out = tree.outputs.geometry()
            v1 = g.Value()
            v2 = g.Value()
            _ = g.CombineXYZ(x=v1, y=v2) >> g.SetPosition() >> out

        graph, _ = build_dependency_graph(tree.tree)
        sorted_nodes = topological_sort(graph)
        columns = organize_into_columns(sorted_nodes, graph)

        # The two Value nodes should be in the same column
        value_nodes = [n for n in tree.tree.nodes if n.bl_idname == "ShaderNodeValue"]
        if len(value_nodes) == 2:
            col_of = {}
            for i, col in enumerate(columns):
                for n in col:
                    col_of[n] = i
            assert col_of[value_nodes[0]] == col_of[value_nodes[1]]


class TestCalculateNodeDimensions:
    """Tests for calculate_node_dimensions."""

    def test_positive_dimensions(self):
        """Every node should have positive width and height."""
        from collections import Counter

        with TreeBuilder(arrange=None) as tree:
            g.SetPosition()

        node = tree.tree.nodes["Set Position"]
        width, height = calculate_node_dimensions(node, Counter(), 1.0)
        assert width > 0
        assert height > 0

    def test_more_sockets_taller(self):
        """A node with more sockets should be estimated taller."""
        from collections import Counter

        with TreeBuilder(arrange=None) as tree:
            g.Value()
            g.SetPosition()

        value = tree.tree.nodes["Value"]
        set_pos = tree.tree.nodes["Set Position"]
        _, h_value = calculate_node_dimensions(value, Counter(), 1.0)
        _, h_set_pos = calculate_node_dimensions(set_pos, Counter(), 1.0)
        assert h_set_pos > h_value

    def test_interface_scale(self):
        """Height should scale with interface_scale."""
        from collections import Counter

        with TreeBuilder(arrange=None) as tree:
            g.SetPosition()

        node = tree.tree.nodes["Set Position"]
        _, h1 = calculate_node_dimensions(node, Counter(), 1.0)
        _, h2 = calculate_node_dimensions(node, Counter(), 2.0)
        assert h2 == pytest.approx(h1 * 2.0)


class TestReroutePositioning:
    """Tests for reroute node handling."""

    def test_reroute_positioned_between_neighbours(self):
        """A reroute node should be placed between its connected nodes."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out

        # Insert a reroute between SetPosition and GroupOutput
        reroute = tree.tree.nodes.new("NodeReroute")
        set_pos = tree.tree.nodes["Set Position"]
        group_out = tree.tree.nodes["Group Output"]

        # Place source and target at known positions
        set_pos.location = (0, 0)
        group_out.location = (400, 0)

        # Remove the existing link and re-route through the reroute node
        for link in list(tree.tree.links):
            if link.from_node == set_pos and link.to_node == group_out:
                tree.tree.links.remove(link)
                break

        tree.tree.links.new(set_pos.outputs[0], reroute.inputs[0])
        tree.tree.links.new(reroute.outputs[0], group_out.inputs[0])

        arrange_tree(tree.tree)

        # Reroute should be between set_pos and group_out on the x-axis
        assert reroute.location.x >= set_pos.location.x
        assert reroute.location.x <= group_out.location.x

    def test_disconnected_reroute_not_moved(self):
        """A reroute with no connections should stay at its original position."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out

        reroute = tree.tree.nodes.new("NodeReroute")
        reroute.location = (999, 999)

        arrange_tree(tree.tree)
        assert reroute.location.x == 999
        assert reroute.location.y == 999


class TestFrameHandling:
    """Tests for frame node handling."""

    def test_frame_not_repositioned(self):
        """Frame nodes should not be moved by arrange_tree."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> out

        frame = tree.tree.nodes.new("NodeFrame")
        frame.location = (123, 456)

        arrange_tree(tree.tree)
        assert frame.location.x == 123
        assert frame.location.y == 456


class TestArrangeIntegration:
    """Integration tests via TreeBuilder."""

    def test_simple_arrange_strategy(self):
        """TreeBuilder with arrange='simple' should arrange without error."""
        with TreeBuilder(arrange="simple") as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out

        set_pos = tree.tree.nodes["Set Position"]
        realize = tree.tree.nodes["Realize Instances"]
        assert set_pos.location.x < realize.location.x

    def test_none_arrange_skips(self):
        """TreeBuilder with arrange=None should not move any nodes."""
        with TreeBuilder(arrange=None) as tree:
            geo = tree.inputs.geometry()
            out = tree.outputs.geometry()
            set_pos_node = g.SetPosition()
            _ = geo >> set_pos_node >> out

        # All nodes should still be at their default creation position (0, 0)
        for node in tree.tree.nodes:
            assert node.location.x == 0
            assert node.location.y == 0
