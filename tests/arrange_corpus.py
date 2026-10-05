"""A corpus of layout problems and their answers, as JSON files.

Each file of ``tests/arrange_corpus/`` holds one node tree as plain data
and the layout computed for it under a few settings (see
:mod:`nodebpy.lib.nodearrange.serialize` for the format). Reading them needs
no Blender, so they serve two purposes:

- a regression test: the layout must still give these answers
  (``tests/test_arrange_corpus.py``);
- a conformance suite: an implementation in another language can read the
  same trees and settings and be compared against the stored edits.

After a deliberate change to the layout, rewrite the answers (the trees are
kept as they are) and review the diff:

    uv run python -m tests.arrange_corpus --update

To rebuild the trees themselves from Blender (new cases, or a new Blender
version changing node sizes):

    uv run python -m tests.arrange_corpus --rebuild
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from nodebpy.lib.nodearrange.arrange.edits import LayoutResult
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNodeTree
from nodebpy.lib.nodearrange.serialize import (
    result_from_json,
    result_to_json,
    settings_from_json,
    settings_to_json,
    tree_from_json,
    tree_to_json,
)

DIRECTORY = Path(__file__).parent / "arrange_corpus"

MARGIN = (50.0, 20.0)

# The settings each tree is laid out under. `default` is what
# `SugiyamaOptions()` gives.
SETTINGS: dict[str, Settings] = {
    "default": Settings(direction="BALANCED", add_reroutes=False),
    "reroutes": Settings(direction="BALANCED", add_reroutes=True),
    "plain": Settings(
        add_reroutes=False,
        direction="RIGHT_DOWN",
        socket_alignment="NONE",
        stack_collapsed=False,
        sequential_frames=False,
        balance_heights=False,
        link_priority="none",
        pin_group_output=False,
    ),
}

# Blender's bundled node groups that go into the corpus: a spread of sizes,
# with frames, reroutes and collapsed nodes.
ESSENTIALS = (
    "Array",
    "Displace Geometry",
    "Scatter on Surface",
    "Randomize Transforms",
    "Geometry Input",
)
FUZZ_SEEDS = (3, 19, 37, 50, 184, 204)


def _round(value: Any, ndigits: int = 4) -> Any:
    """*value* with every float rounded, so the files do not depend on the
    last bits of a computation."""
    if isinstance(value, float):
        return round(value, ndigits)
    if isinstance(value, list):
        return [_round(item, ndigits) for item in value]
    if isinstance(value, dict):
        return {key: _round(item, ndigits) for key, item in value.items()}
    return value


def layout_json(tree: bNodeTree, settings: Settings) -> dict[str, Any]:
    """The layout of *tree* under *settings*, as it is stored."""
    return _round(result_to_json(tree, sugiyama_layout(tree, settings, MARGIN)))


def cases() -> Iterator[tuple[str, dict[str, Any]]]:
    """``(name, contents)`` of every corpus file."""
    for path in sorted(DIRECTORY.glob("*.json")):
        yield path.stem, json.loads(path.read_text())


def load(case: dict[str, Any], layout: str) -> tuple[bNodeTree, Settings, LayoutResult]:
    """The tree of *case*, and the settings and stored result of *layout*."""
    tree = tree_from_json(case["tree"])
    stored = case["layouts"][layout]
    return (
        tree,
        settings_from_json(stored["settings"]),
        result_from_json(tree, stored["result"]),
    )


def _write(name: str, tree_json: dict[str, Any]) -> None:
    layouts = {}
    for key, settings in SETTINGS.items():
        # A fresh tree per layout: nothing may carry over.
        tree = tree_from_json(tree_json)
        layouts[key] = {
            "settings": settings_to_json(settings),
            "result": layout_json(tree, settings),
        }
    contents = {"margin": list(MARGIN), "tree": tree_json, "layouts": layouts}
    DIRECTORY.mkdir(exist_ok=True)
    (DIRECTORY / f"{name}.json").write_text(
        json.dumps(contents, separators=(",", ":")) + "\n"
    )


def update() -> None:
    """Recompute the stored layouts of the trees already in the corpus."""
    for name, case in cases():
        _write(name, case["tree"])


def rebuild() -> None:
    """Rebuild every tree from Blender, and its layouts."""
    import bpy

    from nodebpy.lib.nodearrange.extract import extract

    from . import arrange_cases
    from .arrange_fuzz import random_tree

    for path in DIRECTORY.glob("*.json"):
        path.unlink()

    bpy.ops.wm.read_factory_settings(use_empty=True)
    builders = {**arrange_cases.CASES, **arrange_cases.asset_groups()}
    for name, build in builders.items():
        ntree = build()
        arrange_cases.reset_locations(ntree)
        _write(name, _round(tree_to_json(extract(ntree)[0])))

    for ntree in arrange_cases.essentials(list(ESSENTIALS)):
        name = "essentials_" + ntree.name.lower().replace(" ", "_")
        _write(name, _round(tree_to_json(extract(ntree)[0])))

    for seed in FUZZ_SEEDS:
        _write(f"random_{seed:03}", tree_to_json(random_tree(seed)))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="recompute the layouts")
    group.add_argument(
        "--rebuild", action="store_true", help="rebuild the trees too (needs bpy)"
    )
    args = parser.parse_args(argv)
    if args.rebuild:
        rebuild()
    else:
        update()
    files = list(DIRECTORY.glob("*.json"))
    size = sum(path.stat().st_size for path in files)
    print(f"{len(files)} files, {size / 1024:.0f} kB in {DIRECTORY}")


if __name__ == "__main__":
    main()
