"""Run a script that builds node trees and report what it built in a few lines.

The report lists each tree the script built (new or rebuilt in place) with its
node and link counts and interface, then, with an object, the geometry the
last geometry tree evaluates to and any node warnings. An error is reported
as its message and the line of the script that raised it, rather than a full
traceback. That keeps the build, check and fix loop cheap, for people and for
coding agents::

    nodebpy run build_tree.py --object Cube
    nodebpy run build_sim.py --object Emitter --frame 24 --blend scene.blend

Inside Blender (the text editor, an MCP server) call :func:`run`; it re-runs
through :func:`nodebpy.live.run_source`, so group classes rebuild and modifier
input values are kept.
"""

from __future__ import annotations

import argparse
import sys
import traceback as _traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import bpy

from .builder.tree import MaterialBuilder, TreeBuilder, WorldBuilder, record_built_trees
from .live import run_source

__all__ = ["RunReport", "run"]

_KIND = {
    "GeometryNodeTree": "geometry",
    "ShaderNodeTree": "shader",
    "CompositorNodeTree": "compositor",
}


@dataclass
class RunReport:
    """The outcome of :func:`run`: ``ok`` is False when the script raised."""

    ok: bool
    text: str

    def __str__(self) -> str:
        return self.text


def run(
    path: str | Path,
    *,
    object: str | None = None,
    tree: str | None = None,
    frame: int | None = None,
    traceback: bool = False,
    echo: bool = True,
) -> RunReport:
    """Run the script at ``path`` and report the trees it built.

    ``object`` names the object to show the last geometry tree on (``tree``
    picks another), as a Geometry Nodes modifier; the object is created if it
    doesn't exist. ``frame`` steps the scene to that frame first, so
    simulations advance. ``traceback=True`` adds the full traceback to an
    error. The report is printed unless ``echo=False``.
    """
    path = Path(path)
    lines: list[str] = []
    ok = True
    with record_built_trees() as built:
        try:
            run_source(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as error:  # noqa: BLE001 - the report is the point
            ok = False
            lines += _error_lines(error, path, full=traceback)
    lines += [_tree_line(builder) for builder in _unique(built)]
    if ok and object is not None:
        try:
            lines += _object_lines(object, _pick_tree(built, tree), frame)
        except Exception as error:  # noqa: BLE001
            ok = False
            lines += _error_lines(error, path, full=traceback)
    if ok and not built:
        lines.append("built no trees")
    report = RunReport(ok, "\n".join(lines))
    if echo:
        print(report.text)
    return report


def _unique(built: list[TreeBuilder[Any]]) -> list[TreeBuilder[Any]]:
    """One entry per tree, at its last build."""
    last = {builder.tree.name: builder for builder in built}
    return list(last.values())


def _error_lines(error: BaseException, path: Path, *, full: bool) -> list[str]:
    lines = [f"ERROR {type(error).__name__}: {error}"]
    frames = [
        frame
        for frame in _traceback.extract_tb(error.__traceback__)
        if Path(frame.filename).name == path.name
    ]
    if frames:
        frame = frames[-1]
        lines.append(f"  at {path.name}:{frame.lineno}: {(frame.line or '').strip()}")
    if full:
        lines += _traceback.format_exception(error)
    return lines


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}{'' if count == 1 else 's'}"


def _socket_summary(item: Any) -> str:
    kind = item.socket_type.removeprefix("NodeSocket")
    default = getattr(item, "default_value", None)
    if default is None or kind in ("Geometry", "Shader", "Bundle", "Closure"):
        return f"{item.name}: {kind}"
    try:
        values = [round(v, 3) for v in default]
        default = tuple(values)
    except TypeError:
        if isinstance(default, float):
            default = round(default, 3)
    if isinstance(default, bpy.types.ID):
        default = default.name
    return f"{item.name}: {kind} = {default!r}"


def _tree_line(builder: TreeBuilder[Any]) -> str:
    node_tree: Any = builder.tree
    links = len(node_tree.links)
    nodes = len(node_tree.nodes)
    counts = f"{_plural(nodes, 'node')}, {_plural(links, 'link')}"
    if isinstance(builder, MaterialBuilder):
        return f"built material '{builder.material.name}': {counts}"
    if isinstance(builder, WorldBuilder):
        return f"built world '{builder.world.name}': {counts}"
    flags = [
        flag for flag in ("is_modifier", "is_tool") if getattr(node_tree, flag, False)
    ]
    kind = _KIND.get(node_tree.bl_idname, node_tree.bl_idname)
    kind = ", ".join([kind, *(f.removeprefix("is_") for f in flags)])
    sockets = [
        item for item in node_tree.interface.items_tree if item.item_type == "SOCKET"
    ]
    inputs = ", ".join(_socket_summary(i) for i in sockets if i.in_out == "INPUT")
    outputs = ", ".join(_socket_summary(i) for i in sockets if i.in_out == "OUTPUT")
    return (
        f"built '{node_tree.name}' ({kind}): {counts}; in ({inputs}) -> out ({outputs})"
    )


def _pick_tree(built: list[TreeBuilder[Any]], name: str | None) -> Any:
    if name is not None:
        found = bpy.data.node_groups.get(name)
        if found is None:
            raise KeyError(f"no node group named {name!r}")
        return found
    geometry = [b.tree for b in built if b.tree.bl_idname == "GeometryNodeTree"]
    if not geometry:
        raise ValueError("the script built no geometry tree to show on the object")
    # prefer the last modifier tree over group trees built along the way
    modifiers = [t for t in geometry if getattr(t, "is_modifier", False)]
    return (modifiers or geometry)[-1]


def _object_lines(name: str, node_tree: Any, frame: int | None) -> list[str]:
    scene = cast(Any, bpy.context.scene)
    obj = cast(Any, bpy.data.objects.get(name))
    if obj is None:
        obj = cast(Any, bpy.data.objects.new(name, bpy.data.meshes.new(name)))
        scene.collection.objects.link(obj)
    mod: Any = next(
        (m for m in obj.modifiers if m.type == "NODES" and m.node_group == node_tree),
        None,
    ) or obj.modifiers.new("nodebpy", "NODES")
    mod.node_group = node_tree
    obj.update_tag()
    if frame is not None:
        for step in range(scene.frame_start, frame + 1):
            scene.frame_set(step)
    depsgraph = cast(Any, bpy.context.evaluated_depsgraph_get())
    evaluated = obj.evaluated_get(depsgraph)
    geometry = evaluated.evaluated_geometry()
    # evaluated data is freed on the next access of its kind, so the instance
    # point cloud is read once and kept for both the summary and the bounds
    instances = geometry.instances_pointcloud()
    summary = _geometry_summary(geometry, instances)
    lines = [f"object '{obj.name}' ({node_tree.name}): {summary}"]
    bounds = _bounds(geometry, instances)
    if bounds is not None:
        lines.append(f"  bounds {_point(bounds[0])}..{_point(bounds[1])}")
    lines += [f"  {w.type.lower()}: {w.message}" for w in mod.node_warnings]
    return lines


def _positions(attributes: Any, name: str, count: int) -> list[tuple[float, ...]]:
    attribute = attributes.get(name)
    if attribute is None or not count:
        return []
    flat = [0.0] * (count * 3)
    attribute.data.foreach_get("vector", flat)
    return [tuple(flat[i : i + 3]) for i in range(0, len(flat), 3)]


def _bounds(geometry: Any, instances: Any) -> tuple[list[float], list[float]] | None:
    """Object-space bounds of every component, instances by their positions
    (an object's own bounding box leaves unrealized instances out)."""
    points: list[tuple[float, ...]] = []
    if geometry.mesh:
        points += _positions(
            geometry.mesh.attributes, "position", len(geometry.mesh.vertices)
        )
    if geometry.pointcloud:
        points += _positions(
            geometry.pointcloud.attributes, "position", len(geometry.pointcloud.points)
        )
    if geometry.curves:
        points += _positions(
            geometry.curves.attributes, "position", len(geometry.curves.points)
        )
    if instances is not None and len(instances.points):
        # the point cloud's own position is not filled in; each instance's
        # transform holds it (foreach_get reads the matrices column by column)
        flat = [0.0] * (16 * len(instances.points))
        instances.attributes["instance_transform"].data.foreach_get("value", flat)
        points += [tuple(flat[i + 12 : i + 15]) for i in range(0, len(flat), 16)]
    if not points:
        return None
    lo = [min(p[i] for p in points) for i in range(3)]
    hi = [max(p[i] for p in points) for i in range(3)]
    return lo, hi


def _point(values: list[float]) -> str:
    return "(" + ", ".join(f"{v:.3g}" for v in values) + ")"


def _geometry_summary(geometry: Any, instances: Any) -> str:
    parts = []
    mesh = geometry.mesh
    if mesh and len(mesh.vertices):
        parts.append(
            f"mesh {_plural(len(mesh.vertices), 'vertex')}, "
            f"{_plural(len(mesh.polygons), 'face')}".replace("vertexs", "vertices")
        )
    if geometry.pointcloud and len(geometry.pointcloud.points):
        parts.append(_plural(len(geometry.pointcloud.points), "point"))
    curves = geometry.curves
    if curves and len(curves.curves):
        parts.append(
            f"{_plural(len(curves.curves), 'curve')} "
            f"({_plural(len(curves.points), 'point')})"
        )
    if instances is not None and len(instances.points):
        parts.append(_plural(len(instances.points), "instance"))
    return "; ".join(parts) or "empty"


def add_parser(sub: Any) -> None:
    parser = sub.add_parser(
        "run",
        help="Run a script that builds node trees and report what it built.",
        description=__doc__.split("\n\n")[1] if __doc__ else None,
    )
    parser.add_argument("script", type=Path)
    parser.add_argument("--object", help="show the last geometry tree on this object")
    parser.add_argument("--tree", help="the geometry tree to show, instead of the last")
    parser.add_argument("--frame", type=int, help="step the scene to this frame first")
    parser.add_argument("--blend", type=Path, help="open this .blend file first")
    parser.add_argument("--traceback", action="store_true", help="add full tracebacks")


def main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="nodebpy")
    add_parser(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(argv)
    if args.blend is not None:
        bpy.ops.wm.open_mainfile(filepath=str(args.blend))
    report = run(
        args.script,
        object=args.object,
        tree=args.tree,
        frame=args.frame,
        traceback=args.traceback,
    )
    sys.exit(0 if report.ok else 1)
