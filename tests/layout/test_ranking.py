"""The rank phase and the steps after it that move nodes between columns
(``ranking``, ``balancing``, ``sugiyama.constrain_layers``)."""

import pytest

from nodebpy.layout import ranking
from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.pipeline import Layout, Step
from nodebpy.layout.sugiyama import default_pipeline, sugiyama_layout

from .data import options, plain_chain, plain_node, positions, random_tree


@pytest.mark.parametrize("seed", [3, 7, 11, 19])
def test_ranking_keeps_its_cut_values_right(seed, monkeypatch):
    """The network simplex only updates the cut values an exchange changes.
    After every exchange they are what computing all of them afresh gives."""
    exchange = ranking.exchange
    exchanges = []

    def checked(H, T, parents, leave, enter):
        parents = exchange(H, T, parents, leave, enter)
        kept = {link.ident: link.cut_value for link in T.all_links()}
        ranking.compute_cut_values(H, T)
        assert kept == {link.ident: link.cut_value for link in T.all_links()}
        exchanges.append(leave)
        return parents

    monkeypatch.setattr(ranking, "exchange", checked)
    sugiyama_layout(random_tree(seed), options(reroutes="all"), verify=True)
    assert exchanges


def _link_length(tree: bNodeTree, pipeline=None) -> int:
    """Columns spanned by the links of *tree*, summed, as ranked."""
    lengths = []

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name == "rank":
            lengths.append(
                sum(k.tonode.rank - k.fromnode.rank for k in layout.G.all_links())
            )

    sugiyama_layout(
        tree,
        options(balance_heights=False, pack_components=False),
        pipeline=pipeline,
        observer=observer,
    )
    (length,) = lengths
    return length


@pytest.mark.parametrize("seed", [2, 7, 10, 15, 18, 19, 22, 25, 26, 28])
def test_network_simplex_links_are_no_longer_than_longest_path(seed):
    """On trees without frames, where the links are all the ranking has to
    keep short."""
    assert not any(node.is_frame() for node in random_tree(seed).nodes)
    longest_path = default_pipeline()
    longest_path.replace(
        "rank", lambda L: ranking.compute_ranks(L.CG, ranking.longest_path_ranks)
    )

    simplex = _link_length(random_tree(seed))

    assert 0 < simplex <= _link_length(random_tree(seed), longest_path)


# ---------------------------------------------------------------------------
# Frames in sequence
# ---------------------------------------------------------------------------


def _frame(tree: bNodeTree, name: str) -> bNode:
    return tree.add_node(bNode(name, "NodeFrame", label=name))


def _frame_fed_early() -> bNodeTree:
    """a1 -> a2 -> a3 in frame A, b1 -> b2 in frame B, and a1 -> b1: B is
    fed by the first node of A."""
    tree = bNodeTree()
    a = plain_chain(tree, ("a1", "a2", "a3"), parent=_frame(tree, "A"))
    b = plain_chain(tree, ("b1", "b2"), parent=_frame(tree, "B"))
    tree.add_link(a["a1"].outputs[0], b["b1"].inputs[0])
    return tree


def test_sequential_frames_put_a_frame_after_the_frame_feeding_it():
    at = positions(_frame_fed_early(), sequential_frames=True)
    assert at["a3"][0] < at["b1"][0]

    at = positions(_frame_fed_early(), sequential_frames=False)
    assert at["b1"][0] == at["a2"][0]


def test_sequential_frames_leave_unlinked_frames_sharing_columns():
    """Two frames fed by one node and feeding another are branches, not
    stages: their nodes share a column."""
    tree = bNodeTree()
    source = plain_node(tree, "source")
    join = plain_node(tree, "join", multi_input=True)
    for i, name in enumerate("xy"):
        node = plain_node(tree, name, parent=_frame(tree, name.upper()))
        tree.add_link(source.outputs[0], node.inputs[0])
        tree.add_link(node.outputs[0], join.inputs[0], i)

    at = positions(tree, sequential_frames=True)

    assert at["source"][0] < at["x"][0] == at["y"][0] < at["join"][0]


# ---------------------------------------------------------------------------
# Balancing column heights
# ---------------------------------------------------------------------------


def _fan_in(feeders: int) -> bNodeTree:
    """A node with *feeders* inputs, each fed by its own chain of two."""
    tree = bNodeTree()
    target = plain_node(
        tree,
        "target",
        inputs=feeders,
        height=40.0 + 22.0 * feeders,
        socket="NodeSocketFloat",
    )
    for k in range(feeders):
        chain = plain_chain(
            tree, (f"value{k:02}", f"math{k:02}"), socket="NodeSocketFloat"
        )
        tree.add_link(chain[f"math{k:02}"].outputs[0], target.inputs[k])
    return tree


def _height(at: dict[str, tuple[float, float]]) -> float:
    tops = [y for _, y in at.values()]
    return max(tops) - min(tops)


def test_balance_heights_spreads_a_fan_in_over_columns():
    """The nodes feeding a wide fan-in share one column without balancing
    and spread over several with it, their own feeders still to their left;
    the drawing gets no taller."""
    plain = positions(_fan_in(12), balance_heights=False)
    assert len({plain[f"math{k:02}"][0] for k in range(12)}) == 1

    balanced = positions(_fan_in(12), balance_heights=True)
    assert len({balanced[f"math{k:02}"][0] for k in range(12)}) > 1
    assert _height(balanced) <= _height(plain)
    for k in range(12):
        value, math = balanced[f"value{k:02}"], balanced[f"math{k:02}"]
        assert value[0] < math[0] < balanced["target"][0]


def _output_among_short_chains() -> bNodeTree:
    """A three-node chain into a Group Output, a longer chain beside it,
    and eight unrelated pairs that make two columns tall."""
    tree = bNodeTree()
    chain = plain_chain(tree, "abc")
    out = plain_node(tree, "out", idname="NodeGroupOutput")
    tree.add_link(chain["c"].outputs[0], out.inputs[0])
    plain_chain(tree, [f"long{i}" for i in range(6)])
    for i in range(8):
        plain_chain(tree, (f"u{i}", f"v{i}"))
    return tree


def test_pinned_output_survives_height_balancing():
    """The balancing moves nodes left along with what feeds them; a pinned
    Group Output still ends up in the last column."""
    at = positions(_output_among_short_chains(), pack_components=False)
    assert at["out"][0] == max(x for x, _ in at.values())


# ---------------------------------------------------------------------------
# Pinned Group Input and Group Output nodes
# ---------------------------------------------------------------------------


def _with_interface(framed_output: bool = False) -> bNodeTree:
    """in -> a -> out, and a -> b -> c -> join with nothing after: the
    Group Output is not at the end of the longest chain. A second Group
    Input, ``late_in``, feeds the join."""
    tree = bNodeTree()
    group_in = plain_node(tree, "in", idname="NodeGroupInput", inputs=0)
    late_in = plain_node(tree, "late_in", idname="NodeGroupInput", inputs=0)
    frame = _frame(tree, "frame") if framed_output else None
    out = plain_node(tree, "out", idname="NodeGroupOutput", outputs=0, parent=frame)
    a, b, c = (plain_node(tree, name) for name in "abc")
    join = plain_node(tree, "join", multi_input=True)
    for u, v in ((group_in, a), (a, out), (a, b), (b, c), (c, join)):
        tree.add_link(u.outputs[0], v.inputs[0])
    tree.add_link(late_in.outputs[0], join.inputs[0], 1)
    return tree


def _columns(tree: bNodeTree, **fields) -> dict[str, float]:
    return {name: x for name, (x, _) in positions(tree, **fields).items()}


def test_group_output_is_pinned_to_the_last_column_by_default():
    x = _columns(_with_interface())
    assert x["out"] == max(x.values())

    x = _columns(_with_interface(), pin_group_output=False)
    assert x["out"] == x["b"] < max(x.values())


def test_group_input_is_pinned_to_the_first_column_only_when_asked():
    x = _columns(_with_interface())
    assert x["in"] == min(x.values()) < x["late_in"]

    x = _columns(_with_interface(), pin_group_input=True)
    assert x["in"] == x["late_in"] == min(x.values())


def test_group_output_in_a_frame_is_not_pinned():
    x = _columns(_with_interface(framed_output=True))
    assert x["out"] < max(x.values())
