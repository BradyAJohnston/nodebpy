"""``nodebpy.arrange()`` and its options, on Blender trees."""

import dataclasses

import bpy
import pytest

import nodebpy
from nodebpy import (
    SugiyamaOptions,
    TreeBuilder,
    arrange,
    default_sugiyama_options,
)
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.layout import SIMPLE_OPTIONS, config

from . import cases
from .metrics import measure


def _build_chain(name: str, method=None) -> TreeBuilder:
    """Group Input -> Set Position -> Realize Instances -> Group Output."""
    with TreeBuilder(name, arrange=method) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out
    return tree


def _build_simulation(name: str, method="sugiyama") -> TreeBuilder:
    """A simulation zone with links long enough to get reroutes."""
    with TreeBuilder(name, arrange=method) as tree:
        cube = g.Cube()
        sim = g.SimulationZone({"cube": cube})
        pos = sim.item("Position", g.Position())
        (pos.current + 0.1) >> pos.next
        offset = sim.delta_time * g.Vector((0, 0, 0.1)) * pos.current
        sim.input >> g.SetPosition(offset=offset) >> sim.output
        sim.output >> g.SetPosition(position=sim.output.o["Position"])
    return tree


def _locations(tree) -> dict[str, tuple[float, float]]:
    return {node.name: tuple(node.location) for node in tree.nodes}


def _reroutes(tree) -> list:
    return [node for node in tree.nodes if node.bl_idname == "NodeReroute"]


def _columns(tree) -> list[float]:
    """The x of each node, in chain order."""
    names = ("Group Input", "Set Position", "Realize Instances", "Group Output")
    return [tree.nodes[name].location.x for name in names]


# ---------------------------------------------------------------------------
# The method
# ---------------------------------------------------------------------------


def test_arrange_lays_out_a_tree_outside_a_tree_builder():
    tree = _build_chain("Standalone").tree
    assert not TreeBuilder._tree_contexts

    arrange(tree)

    xs = _columns(tree)
    assert xs == sorted(xs) and len(set(xs)) == 4
    assert measure(tree).node_overlaps == 0


def test_arrange_none_leaves_the_tree_untouched():
    tree = _build_chain("NoArrange").tree
    for node in tree.nodes:
        node.location = (12.0, 34.0)
    arrange(tree, None)
    assert all(tuple(n.location) == (12.0, 34.0) for n in tree.nodes)


def test_sugiyama_is_the_default_options():
    by_name = _build_chain("ByName", "sugiyama").tree
    by_options = _build_chain("ByOptions", SugiyamaOptions()).tree
    assert _locations(by_name) == _locations(by_options)


def test_arranging_twice_gives_the_same_locations():
    tree = _build_chain("Twice", "sugiyama").tree
    once = _locations(tree)
    arrange(tree)
    assert _locations(tree) == once


def test_simple_lays_a_chain_out_left_to_right_in_columns():
    tree = _build_chain("SimpleChain").tree

    arrange(tree, "simple")

    xs = _columns(tree)
    assert xs == sorted(xs) and len(set(xs)) == 4
    metrics = measure(tree)
    assert metrics.node_overlaps == 0
    assert metrics.backward_links == 0


def test_simple_is_the_simple_options():
    by_name = _build_simulation("SimpleByName", "simple").tree
    by_options = _build_simulation("SimpleByOptions", SIMPLE_OPTIONS).tree
    default = _build_simulation("SimpleDefault", "sugiyama").tree

    assert _locations(by_name) == _locations(by_options)
    assert _locations(by_name) != _locations(default)


def test_simple_leaves_a_tree_without_nodes_to_place_alone():
    empty = bpy.data.node_groups.new("SimpleEmpty", "GeometryNodeTree")
    arrange(empty, "simple")
    assert len(empty.nodes) == 0

    only_frame = bpy.data.node_groups.new("SimpleFrameOnly", "GeometryNodeTree")
    frame = only_frame.nodes.new("NodeFrame")
    frame.location = (12.0, 34.0)
    arrange(only_frame, "simple")
    assert tuple(frame.location) == (12.0, 34.0)


def test_tree_builder_arranges_on_exit_with_its_method():
    unarranged = _build_chain("BuilderNone", None).tree
    arranged = _build_chain("BuilderDefault", "sugiyama").tree

    assert len(set(_columns(unarranged))) == 1
    assert len(set(_columns(arranged))) == 4


# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------


def test_there_is_one_frozen_options_class():
    assert nodebpy.SugiyamaOptions is config.SugiyamaOptions
    assert nodebpy.layout.SugiyamaOptions is config.SugiyamaOptions
    options = SugiyamaOptions()
    assert (options.margin, options.seed, options.reroutes) == ((30.0, 30.0), 0, "none")
    with pytest.raises(dataclasses.FrozenInstanceError):
        options.seed = 1  # ty: ignore[invalid-assignment]


def test_margin_is_the_gap_between_columns():
    narrow = _build_chain("Narrow", SugiyamaOptions(margin=(50, 20))).tree
    wide = _build_chain("Wide", SugiyamaOptions(margin=(400, 20))).tree

    def gap(tree) -> float:
        first, second = tree.nodes["Group Input"], tree.nodes["Set Position"]
        return second.location.x - (first.location.x + first.width)

    assert gap(narrow) == pytest.approx(50)
    assert gap(wide) == pytest.approx(400)


def test_default_adds_no_reroutes():
    assert _reroutes(_build_simulation("NoReroutes").tree) == []


def test_reroutes_all_adds_reroutes_on_long_links():
    tree = _build_simulation("WithReroutes", SugiyamaOptions(reroutes="all")).tree
    assert _reroutes(tree) != []


def test_default_sugiyama_options_apply_within_their_scope_only():
    """Inside the scope "sugiyama" means the given options; explicit
    options, and trees built after it, are unaffected."""
    with default_sugiyama_options(SugiyamaOptions(reroutes="all")):
        scoped = _build_simulation("Scoped")
        explicit = _build_simulation("ScopedExplicit", SugiyamaOptions())
    after = _build_simulation("ScopedAfter")

    assert _reroutes(scoped.tree) != []
    assert _reroutes(explicit.tree) == []
    assert _reroutes(after.tree) == []


def test_options_of_one_run_do_not_reach_the_next():
    reference = _build_chain("LeakReference", "sugiyama")
    _build_chain("LeakCustom", SugiyamaOptions(reroutes="all", optimize_sizes=True))
    repeat = _build_chain("LeakRepeat", "sugiyama")

    assert _locations(repeat.tree) == _locations(reference.tree)


def test_selected_only_moves_only_the_selection():
    tree = cases.chain()
    for i, node in enumerate(tree.nodes):
        node.location = (37.0 * i, -200.0 * i)
        node.select = i >= 2
    before = _locations(tree)

    arrange(tree, "sugiyama", selected_only=True)

    after = _locations(tree)
    kept, moved = list(tree.nodes)[:2], list(tree.nodes)[2:]
    assert all(after[node.name] == before[node.name] for node in kept)
    assert all(after[node.name] != before[node.name] for node in moved)
    assert len({after[node.name][1] for node in moved}) == 1


def test_isolated_chain_of_collapsed_math_nodes_is_stacked():
    """Two collapsed Math nodes linked to nothing else are placed one above
    the other."""
    tree = bpy.data.node_groups.new("IsolatedStack", "GeometryNodeTree")
    first = tree.nodes.new("ShaderNodeMath")
    second = tree.nodes.new("ShaderNodeMath")
    first.hide = second.hide = True
    tree.links.new(first.outputs[0], second.inputs[0])

    arrange(tree, SugiyamaOptions(stack_collapsed=True))
    assert first.location.x == second.location.x
    assert first.location.y != second.location.y

    arrange(tree, SugiyamaOptions(stack_collapsed=False))
    assert first.location.x < second.location.x


# ---------------------------------------------------------------------------
# optimize_sizes
# ---------------------------------------------------------------------------


def test_optimize_sizes_fits_collapsed_nodes_to_their_names():
    """Add and Multiply have display names of different lengths, so the
    collapsed Math nodes get different widths, none the default 140."""
    with TreeBuilder(
        "OptimizeSizes", arrange=SugiyamaOptions(optimize_sizes=True)
    ) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        a = g.Value()
        b = (a + 1.0) * 2.0
        _ = geo >> g.SetPosition(offset=g.CombineXYZ(x=b, y=b)) >> out
        for node in tree.tree.nodes:
            if node.bl_idname == "ShaderNodeMath":
                node.hide = True

    widths = {n.width for n in tree.tree.nodes if n.bl_idname == "ShaderNodeMath"}
    assert len(widths) == 2 and 140.0 not in widths


def test_optimize_sizes_widens_a_node_with_a_long_label():
    """The display name is the label, or else the Math operation, the node
    group's name or the image's name."""
    image = bpy.data.images.new("SizeTex", 2, 2)
    with TreeBuilder("DisplayNames", arrange=None) as tree:
        geo = tree.inputs.geometry()
        labelled = g.SetPosition(geometry=geo)
        labelled.node.label = "A Rather Long Custom Label"
        math = g.Math.add(1.0, 2.0)
        tex = g.ImageTexture(image=image)
        group = g.Group()
        group.node.node_tree = bpy.data.node_groups.new(
            "Sized Group", "GeometryNodeTree"
        )
        labelled >> tree.outputs.geometry()
        nodes = {"label": labelled, "math": math, "image": tex, "group": group}
        for node in nodes.values():
            node.node.hide = True

    arrange(tree.tree, SugiyamaOptions(optimize_sizes=True))

    widths = {key: node.node.width for key, node in nodes.items()}
    assert widths["label"] > 140.0
    assert widths["label"] > widths["group"] > widths["math"]
    bpy.data.images.remove(image)


def test_optimize_sizes_fits_a_shader_image_node_to_its_image_name():
    """The two collapsed Math nodes after it are joined by two links, which
    both survive."""
    image = bpy.data.images.new("A Long Name For A Shader Image", 2, 2)
    with TreeBuilder.shader("ShaderSizes") as tree:
        tex = s.ImageTexture()
        tex.node.image = image
        first = s.Math.add(tex.o.alpha, 1.0)
        second = s.Math.add(first, first)
        second >> tree.outputs.float("Out")
        for node in (tex.node, first.node, second.node):
            node.hide = True
    width, links = tex.node.width, len(tree.tree.links)

    arrange(tree.tree, SugiyamaOptions(optimize_sizes=True, stack_collapsed=True))

    assert tex.node.width != width
    assert tex.node.location.x < first.node.location.x < second.node.location.x
    assert len(tree.tree.links) == links
    assert [
        link.from_node for link in tree.tree.links if link.to_node == second.node
    ] == [
        first.node,
        first.node,
    ]
    bpy.data.images.remove(image)


# ---------------------------------------------------------------------------
# Blender's bundled node groups
# ---------------------------------------------------------------------------


def _essential(name: str):
    """A fresh copy of one of Blender's bundled node groups."""
    trees = list(cases.essentials([name]))
    if not trees:
        pytest.skip(f"no node group {name!r} in Blender's bundled essentials")
    return trees[0]


@pytest.mark.parametrize(
    ("tree_name", "options"),
    [
        # Reroutes of its own, replaced; sockets fully aligned.
        (
            "Random Rotation",
            SugiyamaOptions(reroutes="all", socket_alignment="FULL"),
        ),
        # Frames, with reroutes added outside them.
        (
            "Project with Depth",
            SugiyamaOptions(
                reroutes="all", direction="RIGHT_DOWN", socket_alignment="MODERATE"
            ),
        ),
        # Frames and reroutes of its own, kept.
        (
            "Face Corner Angle",
            SugiyamaOptions(direction="LEFT_DOWN", socket_alignment="MODERATE"),
        ),
        # Many nodes of one type: links get bend points around nodes.
        ("Randomize Transforms", SugiyamaOptions(reroutes="all")),
        # Frames, reroutes and several Group Input nodes.
        ("Is UV Split", SugiyamaOptions(reroutes="all")),
    ],
    ids=["full_alignment", "right_down", "left_down", "bend_points", "frames"],
)
def test_bundled_group_is_arranged_without_overlaps(tree_name, options):
    """Locations are rounded to two decimals, as far as single precision
    holds them."""
    tree = _essential(tree_name)

    arrange(tree, options, verify=True)

    metrics = measure(tree)
    assert metrics.node_overlaps == 0
    assert metrics.backward_links == 0
    for node in tree.nodes:
        for value in node.location:
            assert abs(value - round(value, 2)) < 1e-4


@pytest.mark.parametrize("tree_name", ["Is UV Split", "Transform and Project"])
def test_layout_does_not_depend_on_where_objects_are_in_memory(tree_name):
    """Eight copies of a tree, each arranged with the heap shifted, get the
    same locations and links."""
    layouts = set()
    ballast = []
    for run in range(8):
        existing = set(bpy.data.node_groups)
        tree = _essential(tree_name)
        ballast.append([object() for _ in range(997 * (run + 1))])
        arrange(tree, SugiyamaOptions(reroutes="all"))
        locations = sorted((n.name, tuple(n.location)) for n in tree.nodes)
        links = sorted(
            (
                link.from_node.name,
                link.from_socket.identifier,
                link.to_node.name,
                link.to_socket.identifier,
                link.multi_input_sort_id,
            )
            for link in tree.links
        )
        layouts.add((tuple(locations), tuple(links)))
        for group in set(bpy.data.node_groups) - existing:
            bpy.data.node_groups.remove(group)
    assert len(layouts) == 1
