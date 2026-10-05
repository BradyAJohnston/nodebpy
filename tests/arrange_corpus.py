"""A corpus of node trees and the layout each must get, as JSON files.

Each file of ``tests/arrange_corpus/`` holds one node tree, serialised with
`tree_clipper <https://github.com/Algebraic-UG/tree_clipper>`_ (the same
format nodebpy uses for web rendering and parity checks), and where every
node ends up when the tree is arranged under a few settings, with the
headline counts of each layout (crossings, level links, size, ...). It is a
regression test for this implementation: the positions depend on the node
sizes nodebpy estimates without a UI, which the files do not hold, so
another implementation measuring drawn sizes would not reproduce them.

After a deliberate change to the layout, rewrite the stored layouts (the
trees are kept as they are). What changed in each layout's counts is
printed, to judge the change by:

    uv run python -m tests.arrange_corpus --update

To add the cases that have no file yet, leaving the others alone:

    uv run python -m tests.arrange_corpus --add

To rebuild every tree (a new Blender version; this rewrites every file, as
the compressed trees are not byte for byte reproducible):

    uv run python -m tests.arrange_corpus --rebuild
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import bpy
from bpy.types import NodeTree

from nodebpy.lib.nodearrange import arrange_node_tree
from nodebpy.lib.nodearrange.config import Settings

from . import arrange_cases
from .arrange_data import MARGIN
from .arrange_metrics import measure

DIRECTORY = Path(__file__).parent / "arrange_corpus"


# The settings each tree is laid out under, as the fields that differ from
# `Settings()`.
SETTINGS: dict[str, dict[str, Any]] = {
    "default": {},
    "reroutes": {"reroutes": "all"},
    "blocked": {"reroutes": "blocked"},
    "plain": {
        "direction": "RIGHT_DOWN",
        "stack_collapsed": False,
        "sequential_frames": False,
        "balance_heights": False,
        "straighten_trunk": False,
        "pin_group_output": False,
    },
}

# Blender's bundled node groups that go into the corpus: a spread of sizes,
# with frames, reroutes and collapsed nodes.
ESSENTIALS = (
    "Displace Geometry",
    "Scatter on Surface",
    "Randomize Transforms",
    "Geometry Input",
)

# The largest tree takes seconds to arrange, so it is stored under one of
# the settings only.
LAYOUTS_OF: dict[str, tuple[str, ...]] = {
    "essentials_scatter_on_surface": ("default",),
}


# -------------------------------------------------------------------
# Trees, through tree_clipper


def tree_to_payload(tree: NodeTree) -> str:
    """*tree* (and the node groups it uses) as a compressed Tree Clipper
    string."""
    from nodebpy.builder import TreeBuilder
    from nodebpy.export.web_render import to_tree_clipper_payload

    return to_tree_clipper_payload(TreeBuilder(tree), compress=True)


def tree_from_payload(payload: str) -> NodeTree:
    """Build the tree of a Tree Clipper string in the current file."""
    from tree_clipper.import_nodes import ImportIntermediate, ImportParameters
    from tree_clipper.specific_handlers import BUILT_IN_IMPORTER

    importing = ImportIntermediate(string=payload)
    # Nothing in the corpus depends on objects, images and the like.
    importing.set_external((int(key), None) for key in importing.get_external())
    report = importing.import_all(
        ImportParameters(specific_handlers=BUILT_IN_IMPORTER, debug_prints=False)  # ty: ignore[invalid-argument-type]
    )
    assert report.last_getter is not None
    tree = report.last_getter()
    assert isinstance(tree, NodeTree)
    return tree


# -------------------------------------------------------------------
# Layouts


def layout_of(tree: NodeTree) -> dict[str, Any]:
    """Where everything in *tree* is: each node's location and frame, and
    every link (the layout adds and removes reroutes, so those too)."""
    nodes = sorted(
        [
            node.name,
            round(node.location.x, 3),
            round(node.location.y, 3),
            node.parent.name if node.parent else None,
        ]
        for node in tree.nodes
    )
    links = sorted(
        [
            link.from_node.name,
            list(link.from_node.outputs).index(link.from_socket),
            link.to_node.name,
            list(link.to_node.inputs).index(link.to_socket),
            link.multi_input_sort_id,
        ]
        for link in tree.links
        if link.from_node and link.to_node
    )
    return {"nodes": nodes, "links": links}


def arranged(
    payload: str, layouts: Iterable[str] = tuple(SETTINGS)
) -> Iterator[tuple[str, NodeTree]]:
    """The tree of *payload* arranged under each of *layouts* (names in
    :data:`SETTINGS`), as ``(layout, tree)``. The tree is built once and
    copied for each layout: building a large one takes seconds."""
    original = tree_from_payload(payload)
    for layout in layouts:
        tree = original.copy()
        arrange_node_tree(tree, Settings(**SETTINGS[layout]), MARGIN)
        yield layout, tree


def cases() -> Iterator[tuple[str, dict[str, Any]]]:
    """``(name, contents)`` of every corpus file."""
    for path in sorted(DIRECTORY.glob("*.json")):
        yield path.stem, json.loads(path.read_text())


def _write(name: str, payload: str, before: dict[str, Any] | None = None) -> None:
    """Store *payload* with its layouts. *before* is the file's previous
    contents, if any: what changed in each layout's headline counts is
    printed, which is how a deliberate change to the layout is judged."""
    contents = {
        "margin": list(MARGIN),
        "tree": payload,
        "layouts": {
            layout: {
                "settings": SETTINGS[layout],
                "metrics": measure(tree).headline(),
                **layout_of(tree),
            }
            for layout, tree in arranged(payload, LAYOUTS_OF.get(name, SETTINGS))
        },
    }
    for layout, stored in contents["layouts"].items():
        old = ((before or {}).get("layouts", {}).get(layout) or {}).get("metrics")
        if old is None or old == stored["metrics"]:
            continue
        changes = ", ".join(
            f"{key} {old.get(key)} -> {value}"
            for key, value in stored["metrics"].items()
            if old.get(key) != value
        )
        print(f"{name} [{layout}]: {changes}")
    for group in list(bpy.data.node_groups):
        bpy.data.node_groups.remove(group)
    DIRECTORY.mkdir(exist_ok=True)
    (DIRECTORY / f"{name}.json").write_text(
        json.dumps(contents, separators=(",", ":")) + "\n"
    )


def update() -> None:
    """Recompute the stored layouts of the trees already in the corpus."""
    for name, case in cases():
        _write(name, case["tree"], case)


def rebuild(only_missing: bool = False) -> None:
    """Rebuild every tree, and its layouts; or, with *only_missing*, just
    those that have no file yet."""
    payloads = {}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    builders = {**arrange_cases.CASES, **arrange_cases.asset_groups()}
    for name, build in builders.items():
        tree = build()
        arrange_cases.reset_locations(tree)
        payloads[name] = tree_to_payload(tree)

    for tree in arrange_cases.essentials(list(ESSENTIALS)):
        name = "essentials_" + tree.name.lower().replace(" ", "_")
        payloads[name] = tree_to_payload(tree)

    if not only_missing:
        for path in DIRECTORY.glob("*.json"):
            path.unlink()
    for name, payload in payloads.items():
        if not (DIRECTORY / f"{name}.json").exists():
            _write(name, payload)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="recompute the layouts")
    group.add_argument("--add", action="store_true", help="add the missing cases")
    group.add_argument("--rebuild", action="store_true", help="rebuild the trees too")
    args = parser.parse_args(argv)
    if args.rebuild or args.add:
        rebuild(only_missing=args.add)
    else:
        update()
    files = list(DIRECTORY.glob("*.json"))
    size = sum(path.stat().st_size for path in files)
    print(f"{len(files)} files, {size / 1024:.0f} kB in {DIRECTORY}")


if __name__ == "__main__":
    main()
