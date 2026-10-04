"""Arrange a corpus of node trees and report how good the layouts are.

The tool for iterating on the layout algorithm: run it before and after a
change and compare the numbers (and the pictures).

    uv run python -m tests.arrange_report                      # table of metrics
    uv run python -m tests.arrange_report --plots tests/plots  # also draw each tree
    uv run python -m tests.arrange_report --json before.json   # save the metrics
    uv run python -m tests.arrange_report --compare before.json  # what changed
    uv run python -m tests.arrange_report --set direction=BALANCED --set add_reroutes=true
    uv run python -m tests.arrange_report --only 'chain,diamond,Is*' --essentials
    uv run python -m tests.arrange_report --set ranking=longest_path  # another strategy
    uv run python -m tests.arrange_report --essentials --timings      # time per step

Each tree is arranged with ``SugiyamaOptions`` (``--set`` overrides a field)
and measured with :func:`nodebpy.lib.nodearrange.metrics.measure`. The
hand-built cases of :mod:`tests.arrange_cases` and nodebpy's asset groups
are always included; ``--essentials`` adds Blender's bundled node groups.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Iterator
from dataclasses import fields, replace
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import bpy
from bpy.types import NodeTree

from nodebpy import SugiyamaOptions, arrange
from nodebpy.builder.layout import _sugiyama_settings
from nodebpy.lib.nodearrange import arrange_node_tree
from nodebpy.lib.nodearrange.arrange.pipeline import Layout, Step
from nodebpy.lib.nodearrange.metrics import LayoutMetrics, measure

from . import arrange_cases

# Columns of the table: (heading, value).
_COLUMNS = (
    ("cross", lambda m: m.crossings),
    ("straight", lambda m: f"{m.straight_links}/{m.links}"),
    ("through", lambda m: m.links_through_nodes),
    ("overlap", lambda m: m.node_overlaps),
    ("back", lambda m: m.backward_links),
    ("frames", lambda m: m.frame_overlaps + m.foreign_nodes_in_frames),
    ("imbal", lambda m: f"{m.imbalance:.0f}"),
    ("size", lambda m: f"{m.width:.0f}x{m.height:.0f}"),
    ("cost", lambda m: f"{m.cost():.1f}"),
)


def _parse_value(text: str) -> Any:
    lowered = text.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    for convert in (int, float):
        try:
            return convert(text)
        except ValueError:
            pass
    if "," in text:
        return tuple(float(part) for part in text.split(","))
    return text


def options_from(overrides: list[str]) -> SugiyamaOptions:
    """``SugiyamaOptions`` with ``key=value`` *overrides* applied."""
    known = {f.name for f in fields(SugiyamaOptions)}
    values = {}
    for override in overrides:
        key, _, value = override.partition("=")
        if key not in known:
            raise SystemExit(f"unknown option {key!r}; choose from {sorted(known)}")
        values[key] = _parse_value(value)
    return replace(SugiyamaOptions(), **values)


def corpus(only: list[str], with_essentials: bool) -> Iterator[tuple[str, NodeTree]]:
    """``(name, tree)`` for every selected tree, built one at a time."""

    def selected(name: str) -> bool:
        return not only or any(fnmatch(name, pattern) for pattern in only)

    builders = {**arrange_cases.CASES, **arrange_cases.asset_groups()}
    for name, build in builders.items():
        if selected(name):
            tree = build()
            arrange_cases.reset_locations(tree)
            yield name, tree

    if with_essentials:
        for tree in arrange_cases.essentials():
            if selected(tree.name):
                yield tree.name, tree


def run(
    options: SugiyamaOptions,
    only: list[str],
    with_essentials: bool,
    plots: Path | None,
    timings: dict[str, float] | None = None,
) -> dict[str, dict[str, Any]]:
    """Arrange and measure the corpus: ``{name: metrics + cost/seconds}``.
    With *timings*, also add up the seconds spent in each layout step."""

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        assert timings is not None
        timings[step.name] = timings.get(step.name, 0.0) + seconds

    results: dict[str, dict[str, Any]] = {}
    for name, tree in corpus(only, with_essentials):
        start = time.perf_counter()
        try:
            if timings is None:
                arrange(tree, options)
            else:
                arrange_node_tree(
                    tree,
                    _sugiyama_settings(options),
                    tuple(options.margin),
                    observer=observer,
                )
                for node in tree.nodes:  # as `arrange` does
                    x, y = node.location
                    node.location = (round(x, 2), round(y, 2))
        except Exception as error:  # noqa: BLE001 - a crash is a result too
            results[name] = {"error": f"{type(error).__name__}: {error}"}
            continue
        seconds = time.perf_counter() - start
        metrics = measure(tree)
        results[name] = {
            **metrics.as_dict(ndigits=1),
            "cost": round(metrics.cost(), 1),
            "seconds": round(seconds, 2),
        }
        if plots is not None:
            from nodebpy.export import to_plot

            safe = name.strip(".").replace(" ", "_")
            to_plot(tree, plots / f"{safe}.png", title=f"{name} — {metrics.summary()}")
    return results


def _metrics_of(result: dict[str, Any]) -> LayoutMetrics:
    return LayoutMetrics(**{k: result[k] for k in LayoutMetrics.field_names()})


def print_table(results: dict[str, dict[str, Any]]) -> None:
    rows = []
    for name, result in results.items():
        if "error" in result:
            rows.append([name, result["error"][:70]])
            continue
        metrics = _metrics_of(result)
        rows.append(
            [
                name,
                *(str(value(metrics)) for _, value in _COLUMNS),
                f"{result['seconds']:.2f}s",
            ]
        )
    header = ["tree", *(heading for heading, _ in _COLUMNS), "time"]
    widths = [
        max(len(row[i]) for row in [header, *rows] if i < len(row))
        for i in range(len(header))
    ]
    for row in [header, *rows]:
        print("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())

    measured = [r for r in results.values() if "error" not in r]
    print(
        f"\n{len(measured)} trees: "
        f"{sum(r['crossings'] for r in measured)} crossings, "
        f"{sum(r['straight_links'] for r in measured)}/{sum(r['links'] for r in measured)} "
        f"links straight, "
        f"{sum(r['links_through_nodes'] for r in measured)} links through nodes, "
        f"total cost {sum(r['cost'] for r in measured):.1f}, "
        f"{sum(r['seconds'] for r in measured):.1f}s"
        + (
            f"; {len(results) - len(measured)} failed"
            if len(measured) < len(results)
            else ""
        )
    )


def print_comparison(
    before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]
) -> None:
    """What changed from *before* to *after*, tree by tree."""
    names = LayoutMetrics.field_names()
    changed = 0
    for name, result in after.items():
        old = before.get(name)
        if old is None:
            print(f"{name}: new")
            continue
        if "error" in result or "error" in old:
            if result.get("error") != old.get("error"):
                changed += 1
                print(
                    f"{name}: {old.get('error', 'ok')} -> {result.get('error', 'ok')}"
                )
            continue
        diffs = [
            f"{key} {old[key]:g} -> {result[key]:g}"
            for key in names
            if old[key] != result[key]
        ]
        if diffs:
            changed += 1
            delta = result["cost"] - old["cost"]
            print(f"{name}: cost {delta:+.1f} ({', '.join(diffs)})")

    shared = [
        n for n in after if n in before and "cost" in after[n] and "cost" in before[n]
    ]
    total = sum(after[n]["cost"] - before[n]["cost"] for n in shared)
    print(f"\n{changed} of {len(after)} trees changed; total cost {total:+.1f}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="override a SugiyamaOptions field (repeatable)",
    )
    parser.add_argument(
        "--only",
        default="",
        metavar="PATTERNS",
        help="comma-separated tree names or fnmatch patterns",
    )
    parser.add_argument(
        "--essentials",
        action="store_true",
        help="include Blender's bundled geometry-nodes essentials",
    )
    parser.add_argument(
        "--plots",
        type=Path,
        metavar="DIR",
        help="draw every arranged tree into DIR (needs matplotlib)",
    )
    parser.add_argument(
        "--json", type=Path, metavar="FILE", help="write the metrics to FILE"
    )
    parser.add_argument(
        "--compare",
        type=Path,
        metavar="FILE",
        help="report what changed since the metrics saved in FILE",
    )
    parser.add_argument(
        "--timings",
        action="store_true",
        help="also print the time spent in each step of the layout",
    )
    args = parser.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    only = [pattern for pattern in args.only.split(",") if pattern]
    timings: dict[str, float] | None = {} if args.timings else None
    results = run(options_from(args.set), only, args.essentials, args.plots, timings)

    print_table(results)
    if timings:
        total = sum(timings.values())
        print("\nstep                     seconds  share")
        for name, seconds in timings.items():
            print(f"{name:24s} {seconds:7.2f}  {seconds / total:5.0%}")
    if args.json:
        args.json.write_text(json.dumps(results, indent=1))
    if args.compare:
        print()
        print_comparison(json.loads(args.compare.read_text()), results)


if __name__ == "__main__":
    main()
