"""Random trees through the layout (plain data, no Blender).

One property test: whatever the tree, every step leaves the graph as it
promises (``verify=True``), every node is placed or replaced, no nodes
overlap, the result is the same every time, and laying the unconnected
parts out apart never puts more frames on each other than laying the tree
out as one graph.
"""

from dataclasses import replace

import pytest

from nodebpy.lib.nodearrange.arrange.edits import MoveNode, RemoveNode
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings

from .arrange_data import MARGIN, node_overlaps, random_tree
from .arrange_metrics import measure


def _placed(result) -> list[tuple[str, tuple[float, float]]]:
    return [(e.node.name, e.top_left) for e in result.edits if isinstance(e, MoveNode)]


def _frame_defects(tree, result) -> int:
    result.apply_to(tree)
    metrics = measure(tree)
    return metrics.frame_overlaps + metrics.foreign_nodes_in_frames


# Upstream's own defaults, which reach parts of the routing the defaults
# here do not.
_UPSTREAM = {"reroutes": "all", "direction": "LEFT_UP", "socket_alignment": "MODERATE"}


@pytest.mark.parametrize("seed", range(30))
@pytest.mark.parametrize(
    ("settings", "zones"),
    [
        ({}, 0),
        ({"reroutes": "all"}, 0),
        ({"reroutes": "blocked"}, 0),
        (_UPSTREAM, 0),
        ({}, 3),
        (_UPSTREAM, 3),
    ],
    ids=["plain", "reroutes", "blocked", "upstream", "zones", "upstream-zones"],
)
def test_random_tree(seed, settings, zones):
    """Zones are thrown at the trees at random, overlapping frames and each
    other in ways Blender's cannot."""
    add_reroutes = settings.get("reroutes") == "all"
    settings = Settings(**settings)
    tree = random_tree(seed, zones)

    result = sugiyama_layout(tree, settings, MARGIN, verify=True)

    moved = {edit.node for edit in result.edits if isinstance(edit, MoveNode)}
    removed = {edit.node for edit in result.edits if isinstance(edit, RemoveNode)}
    for node in tree.nodes:
        assert node.is_frame() or node in moved or node in removed
    assert node_overlaps(result) == 0

    again = sugiyama_layout(random_tree(seed, zones), settings, MARGIN)
    assert _placed(result) == _placed(again)

    if add_reroutes and not zones:
        as_one = random_tree(seed)
        unpacked = sugiyama_layout(
            as_one, replace(settings, pack_components=False), MARGIN
        )
        assert node_overlaps(unpacked) == 0
        assert _frame_defects(tree, result) <= _frame_defects(as_one, unpacked)
