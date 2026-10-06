"""The layout's graph structs (``nodebpy.layout.digraph``).

``LayoutGraph`` / ``Link`` stand in for Blender's ``bNodeTree`` / ``bNodeLink``;
``DiGraph`` holds plain relations. The layout relies on all of them walking
nodes and neighbours in insertion order.
"""

import pytest

from nodebpy.layout.digraph import (
    CycleError,
    DiGraph,
    LayoutGraph,
    ancestors,
    bfs_edges,
    dag_longest_path_length,
    descendants,
    edge_dfs,
    find_cycle,
    is_acyclic,
    simple_digraph,
    strongly_connected_components,
    topological_generations,
    topological_sort,
    weakly_connected_components,
)


def _tree(*links: tuple[str, str]) -> LayoutGraph[str]:
    tree: LayoutGraph[str] = LayoutGraph()
    for u, v in links:
        tree.add_link(u, v)
    return tree


# ---------------------------------------------------------------------------
# LayoutGraph and Link
# ---------------------------------------------------------------------------


def test_tree_nodes_keep_insertion_order():
    tree: LayoutGraph[str] = LayoutGraph()
    tree.add_nodes("cab")
    tree.add_node("a")  # already there: stays where it is
    assert list(tree) == ["c", "a", "b"]
    assert len(tree) == 3
    assert "a" in tree
    assert "z" not in tree
    assert [] not in tree  # unhashable: simply not a node


def test_links_carry_sockets_and_keys():
    tree: LayoutGraph[str] = LayoutGraph()
    first = tree.add_link("a", "b", "out", "in0")
    second = tree.add_link("a", "b", "out", "in1")
    assert (first.fromnode, first.tonode) == ("a", "b")
    assert (first.fromsock, first.tosock) == ("out", "in0")
    assert (first.key, second.key) == (0, 1)
    assert first.ident == ("a", "b", 0)
    assert "a" in repr(first)

    assert tree.links_between("a", "b") == [first, second]
    assert tree.link("a", "b", 1) is second
    assert tree.has_link("a", "b")
    assert tree.has_link("a", "b", 1)
    assert not tree.has_link("a", "b", 2)
    assert not tree.has_link("b", "a")
    assert not tree.has_link("z", "a")
    assert (tree.out_degree("a"), tree.in_degree("b"), tree.degree("a")) == (2, 2, 2)


def test_add_link_with_an_existing_key_updates_that_link():
    tree: LayoutGraph[str] = LayoutGraph()
    link = tree.add_link("a", "b", "out", "in", weight=3)
    same = tree.add_link("a", "b", "other", key=0)
    assert same is link
    assert (link.fromsock, link.tosock, link.weight) == ("other", "in", 3)
    tree.add_link("a", "b", tosock="in2", key=0, weight=5)
    assert (link.tosock, link.weight) == ("in2", 5)


def test_removing_links():
    tree: LayoutGraph[str] = LayoutGraph()
    first = tree.add_link("a", "b")
    tree.add_link("a", "b")
    third = tree.add_link("a", "b")

    tree.remove_link_between("a", "b")  # the most recent
    assert third not in tree.links_between("a", "b")
    tree.remove_link(first)
    assert [link.key for link in tree.links_between("a", "b")] == [1]
    # The next key is one past the highest still in use.
    assert tree.add_link("a", "b").key == 2

    tree.discard_link_between("a", "b", 7)  # missing: ignored
    tree.discard_link_between("a", "z")
    with pytest.raises(KeyError):
        tree.remove_link_between("a", "b", 7)

    for link in tree.links_between("a", "b"):
        tree.remove_link(link)
    assert "b" not in tree.successors("a")
    assert "a" not in tree.predecessors("b")


def test_removing_nodes_removes_their_links():
    tree = _tree(("a", "b"), ("b", "c"), ("c", "a"))
    tree.remove_node("b")
    assert list(tree) == ["a", "c"]
    assert [link.ident for link in tree.all_links()] == [("c", "a", 0)]
    tree.remove_nodes(["c", "missing"])
    assert list(tree) == ["a"]
    assert list(tree.all_links()) == []


def test_link_iteration_order():
    tree = _tree(("b", "x"), ("a", "x"), ("a", "y"), ("b", "x"))
    assert [link.ident for link in tree.all_links()] == [
        ("b", "x", 0),
        ("b", "x", 1),
        ("a", "x", 0),
        ("a", "y", 0),
    ]
    assert list(tree.successors("a")) == ["x", "y"]
    assert list(tree.predecessors("x")) == ["b", "a"]
    assert [link.ident for link in tree.in_links("x")] == [
        ("b", "x", 0),
        ("b", "x", 1),
        ("a", "x", 0),
    ]
    assert [link.tonode for link in tree.out_links("a")] == ["x", "y"]
    assert [u for u, _ in tree.entering("x")] == ["b", "b", "a"]


def test_copy_is_independent_and_keeps_keys():
    tree: LayoutGraph[str] = LayoutGraph()
    tree.columns = [["a"], ["b"]]
    link = tree.add_link("a", "b", "out", "in", weight=2)
    link.cut_value = -1
    tree.add_link("a", "b")
    tree.remove_link(link)

    copy = tree.copy()
    assert copy.columns is tree.columns
    assert [other.ident for other in copy.all_links()] == [("a", "b", 1)]
    copy.link("a", "b", 1).tosock = "changed"
    assert tree.link("a", "b", 1).tosock is None
    copy.add_node("c")
    assert "c" not in tree


def test_reversed_is_a_view():
    tree = _tree(("a", "b"), ("b", "c"))
    tree.columns = [["a"], ["b"], ["c"]]
    view = tree.reversed()
    assert view.columns is tree.columns
    assert list(view.successors("c")) == ["b"]
    assert list(view.predecessors("a")) == ["b"]
    # Links keep their real direction.
    assert [link.ident for link in view.out_links("c")] == [("b", "c", 0)]
    assert [u for u, _ in view.entering("a")] == ["b"]
    assert list(view.reversed().successors("a")) == ["b"]
    # Shared with the tree it views.
    tree.add_link("c", "d")
    assert "d" in view
    assert topological_sort(view) == ["d", "c", "b", "a"]


def test_subgraph():
    tree = _tree(("a", "b"), ("b", "c"), ("c", "d"), ("a", "d"), ("a", "d"))
    sub = tree.subgraph(["d", "a", "c", "nope"])
    assert list(sub) == ["a", "c", "d"]
    assert [link.ident for link in sub.all_links()] == [
        ("a", "d", 0),
        ("a", "d", 1),
        ("c", "d", 0),
    ]
    sub.remove_node("a")
    assert "a" in tree

    # A small selection of a large tree is found without walking the tree.
    small = tree.subgraph(["d"])
    assert list(small) == ["d"]
    assert list(small.all_links()) == []
    assert topological_sort(tree) == ["a", "b", "c", "d"]


def test_simple_digraph_merges_parallel_links():
    graph = simple_digraph(_tree(("a", "b"), ("a", "b"), ("b", "c")))
    assert list(graph.edges()) == [("a", "b"), ("b", "c")]
    assert list(graph) == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# DiGraph
# ---------------------------------------------------------------------------


def test_digraph_basics():
    graph: DiGraph[str] = DiGraph([("a", "b"), ("b", "c")])
    graph.add_edge("a", "c", weight=2)
    graph.add_edge("a", "b")  # again: nothing changes
    graph.add_nodes(["z"])
    assert list(graph) == ["a", "b", "c", "z"]
    assert len(graph) == 4
    assert "z" in graph
    assert {} not in graph
    assert list(graph.edges()) == [("a", "b"), ("a", "c"), ("b", "c")]
    assert list(graph.out_edges("a")) == [("a", "b"), ("a", "c")]
    assert list(graph.successors("a")) == ["b", "c"]
    assert list(graph.predecessors("c")) == ["b", "a"]
    assert (graph.out_degree("a"), graph.in_degree("c"), graph.degree("b")) == (2, 2, 2)
    assert graph.has_edge("a", "c")
    assert not graph.has_edge("c", "a")
    assert not graph.has_edge("nope", "a")
    assert graph.weight("a", "c") == 2
    assert graph.weight("a", "b") is None

    graph.set_weight("a", "b", 5)
    assert graph.reversed().weight("b", "a") == 5
    assert list(graph.reversed().successors("c")) == ["b", "a"]


def test_digraph_removal_and_copies():
    graph: DiGraph[str] = DiGraph([("a", "b"), ("b", "c"), ("c", "d")])
    copy = graph.copy()
    graph.remove_edge("a", "b")
    graph.remove_edges([("b", "c"), ("b", "nope"), ("nope", "b")])
    assert list(graph.edges()) == [("c", "d")]
    graph.remove_node("c")
    graph.remove_nodes(["d", "nope"])
    assert list(graph) == ["a", "b"]
    assert list(copy.edges()) == [("a", "b"), ("b", "c"), ("c", "d")]

    copy.set_weight("b", "c", 4)
    sub = copy.subgraph(["c", "b", "a", "nope"])
    assert list(sub.edges()) == [("a", "b"), ("b", "c")]
    assert sub.weight("b", "c") == 4
    assert list(copy.subgraph(["d"])) == ["d"]


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------


def test_reachability():
    graph: DiGraph[str] = DiGraph(
        [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e"), ("x", "y")]
    )
    assert list(bfs_edges(graph, "a")) == [
        ("a", "b"),
        ("a", "c"),
        ("b", "d"),
        ("d", "e"),
    ]
    assert list(bfs_edges(graph, "d", reverse=True)) == [
        ("d", "b"),
        ("d", "c"),
        ("b", "a"),
    ]
    assert descendants(graph, "b") == {"d", "e"}
    assert ancestors(graph, "d") == {"a", "b", "c"}
    assert descendants(graph, "e") == set()
    # Stops as soon as everything has been reached.
    chain: DiGraph[str] = DiGraph([("a", "b"), ("b", "c")])
    assert descendants(chain, "a") == {"b", "c"}
    assert list(descendants(chain, "a")) == ["b", "c"]


def test_topological_order():
    tree = _tree(("a", "c"), ("b", "c"), ("b", "c"), ("c", "d"), ("a", "d"))
    assert list(topological_generations(tree)) == [["a", "b"], ["c"], ["d"]]
    assert topological_sort(tree) == ["a", "b", "c", "d"]
    assert is_acyclic(tree)

    tree.add_link("d", "a")
    assert not is_acyclic(tree)
    with pytest.raises(CycleError):
        topological_sort(tree)


def test_components():
    graph: DiGraph[str] = DiGraph([("a", "b"), ("c", "b"), ("x", "y"), ("y", "x")])
    graph.add_node("lone")
    assert list(weakly_connected_components(graph)) == [
        ["a", "b", "c"],
        ["x", "y"],
        ["lone"],
    ]
    strong = {frozenset(c) for c in strongly_connected_components(graph)}
    assert strong == {
        frozenset("a"),
        frozenset("b"),
        frozenset("c"),
        frozenset({"x", "y"}),
        frozenset({"lone"}),
    }
    # A longer cycle with a tail hanging off it.
    loop = _tree(("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"))
    assert {frozenset(c) for c in strongly_connected_components(loop)} == {
        frozenset("abc"),
        frozenset("d"),
    }


def test_find_cycle():
    assert find_cycle(_tree(("a", "b"), ("b", "c"))) is None
    assert find_cycle(_tree(("a", "b"), ("b", "b"))) == ["b"]

    tree = _tree(("s", "a"), ("a", "b"), ("b", "c"), ("c", "a"), ("b", "d"))
    cycle = find_cycle(tree)
    assert cycle is not None
    assert sorted(cycle) == ["a", "b", "c"]
    # In order: each node links to the next, the last back to the first.
    for u, v in zip(cycle, cycle[1:] + cycle[:1]):
        assert tree.has_link(u, v)

    # The first cycle a depth-first walk closes: 1 -> 2 -> 1, not the longer
    # one through 0.
    numbers: LayoutGraph[int] = LayoutGraph()
    for u, v in ((0, 1), (1, 2), (2, 1), (1, 3), (3, 0)):
        numbers.add_link(u, v)
    assert find_cycle(numbers) == [1, 2]


def test_edge_dfs():
    graph: DiGraph[str] = DiGraph([("a", "b"), ("b", "c"), ("a", "c"), ("c", "a")])
    assert list(edge_dfs(graph, "a")) == [
        ("a", "b"),
        ("b", "c"),
        ("c", "a"),
        ("a", "c"),
    ]
    assert list(edge_dfs(graph, "nope")) == []


def test_dag_longest_path_length():
    graph: DiGraph[str] = DiGraph([("a", "b"), ("b", "c"), ("a", "c")])
    assert dag_longest_path_length(graph) == 2
    graph.set_weight("a", "c", 5)
    assert dag_longest_path_length(graph) == 5
    assert dag_longest_path_length(DiGraph()) == 0
    lone: DiGraph[str] = DiGraph()
    lone.add_node("a")
    assert dag_longest_path_length(lone) == 0
