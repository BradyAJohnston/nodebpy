"""Run stage 1 (the BSP) on Suzanne and plot the cells.

    BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/planar_map/run_suzanne.py

Writes `suzanne_bsp.png` (cells, fragments, intersection nodes) and
`suzanne_bsp.blend` to `out/` next to this script, checks the partition (cells tile
the root, fragments sit in their cells, no curve length is lost) and prints counts.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# isort: off
import nodebpy  # noqa: F401  (before bpy, so the source tree wins)
import bpy
import numpy as np
from bsp import build
from mathutils import Vector
# isort: on


def scene(max_depth: int):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_monkey_add()
    monkey = bpy.context.object
    scene = bpy.context.scene
    assert monkey is not None and scene is not None

    cam_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(camera)
    camera.location = (3.2, -5.5, 1.8)
    direction = Vector((0, 0, 0)) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.camera = camera

    tree = build()
    mod = monkey.modifiers.new("Planar Map", "NODES")
    mod.node_group = tree.tree
    set_input(mod, "Camera", camera)
    set_input(mod, "Max Depth", max_depth)
    for name, color in [
        ("Cell Material", (0.55, 0.6, 0.68, 1.0)),
        ("Fragment Material", (0.05, 0.25, 0.75, 1.0)),
        ("Node Material", (0.85, 0.12, 0.1, 1.0)),
    ]:
        set_input(mod, name, flat_material(name.replace(" Material", ""), color))
    monkey.update_tag()
    return monkey, mod, tree


def set_input(mod, name: str, value) -> None:
    """Set a modifier input by its socket name."""
    for item in mod.node_group.interface.items_tree:
        if item.item_type == "SOCKET" and item.in_out == "INPUT" and item.name == name:
            getattr(mod.properties.inputs, item.identifier).value = value
            mod.id_data.update_tag()
            return
    raise KeyError(name)


def flat_material(name: str, color):
    """An emissive material, also coloured in the viewport's solid mode."""
    from nodebpy import shader as s

    with s.material(f"BSP {name}") as mat:
        s.Emission(color=color, strength=1.0) >> s.MaterialOutput()
    mat.material.diffuse_color = color
    return mat.material


def read_cloud(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    geo = obj.evaluated_get(depsgraph).evaluated_geometry()
    attrs = geo.pointcloud.attributes
    n = len(geo.pointcloud.points)

    def get(name, width):
        data = attrs[name].data
        out = np.zeros(n * width, dtype=np.float32 if width == 3 else np.int32)
        key = "vector" if width == 3 else "value"
        data.foreach_get(key, out)
        return out.reshape(n, width) if width == 3 else out

    cloud = {name: get(name, 3) for name in ("a", "b", "p0", "p1", "p2", "p3")}
    for name in ("cell", "curve", "depth"):
        cloud[name] = get(name, 1)
    for name in ("is_cell", "is_intersection"):
        out = np.zeros(n, dtype=bool)
        attrs[name].data.foreach_get("value", out)
        cloud[name] = out
    return cloud


def _area(quads):
    x, y = quads[..., 0], quads[..., 1]
    return 0.5 * (x * np.roll(y, -1, 1) - np.roll(x, -1, 1) * y).sum(1)


def check(cloud, input_length: float) -> list[str]:
    """The invariants of the partition; returns what failed."""
    failures = []
    cells = cloud["is_cell"]
    frag = ~cells
    quads = np.stack([cloud[f"p{k}"][cells, :2] for k in range(4)], axis=1)

    # 1. cells are counter-clockwise and tile the root exactly
    areas = _area(quads)
    lo, hi = quads.reshape(-1, 2).min(0), quads.reshape(-1, 2).max(0)
    root = np.prod(hi - lo)
    if (areas <= 0).any():
        failures.append(f"{(areas <= 0).sum()} cells are not counter-clockwise")
    if not np.isclose(areas.sum(), root, rtol=1e-4):
        failures.append(f"cell area {areas.sum():.6f} != root {root:.6f}")

    # 2. cell ids are unique, and every fragment's midpoint is inside its cell
    ids = cloud["cell"][cells]
    if len(np.unique(ids)) != len(ids):
        failures.append("cell ids repeat")
    lookup = {cell: i for i, cell in enumerate(ids)}
    if missing := set(cloud["cell"][frag]) - set(lookup):
        failures.append(f"{len(missing)} fragments point at no cell")
    else:
        q = quads[[lookup[c] for c in cloud["cell"][frag]]]
        mid = (cloud["a"][frag, :2] + cloud["b"][frag, :2]) / 2
        edge = np.roll(q, -1, 1) - q
        rel = mid[:, None, :] - q
        inside = edge[..., 0] * rel[..., 1] - edge[..., 1] * rel[..., 0]
        scale = np.abs(edge).max()
        outside = (inside < -1e-5 * scale**2).any(1)
        if outside.any():
            failures.append(f"{outside.sum()} fragments lie outside their cell")

    # 3. leaves that are not intersection nodes hold at most one curve piece
    counts = {}
    for cell, curve in zip(cloud["cell"][frag], cloud["curve"][frag]):
        counts.setdefault(cell, set()).add(curve)
    plain = set(ids[~cloud["is_intersection"][cells]])
    if crowded := [c for c in plain if len(counts.get(c, ())) > 1]:
        failures.append(f"{len(crowded)} plain cells hold several curves")

    # 4. splitting kept every curve's length
    length = np.linalg.norm(cloud["b"][frag] - cloud["a"][frag], axis=1).sum()
    if not np.isclose(length, input_length, rtol=1e-4):
        failures.append(f"fragment length {length:.6f} != input {input_length:.6f}")
    return failures


def plot(cloud, path: Path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection, PolyCollection

    cells = cloud["is_cell"]
    quads = np.stack([cloud[f"p{k}"][cells, :2] for k in range(4)], axis=1)
    hits = cloud["is_intersection"][cells]
    frag = ~cells
    segs = np.stack([cloud["a"][frag, :2], cloud["b"][frag, :2]], axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8.5))
    for ax, zoom in zip(axes, (None, 0.12)):
        ax.add_collection(
            PolyCollection(
                quads, facecolors="none", edgecolors="#9aa4b1", linewidths=0.25
            )
        )
        ax.add_collection(
            LineCollection(
                segs,
                colors=plt.cm.tab20(cloud["curve"][frag] % 20),
                linewidths=0.8,
            )
        )
        ax.add_collection(
            PolyCollection(quads[hits], facecolors="#d62728", edgecolors="none")
        )
        ax.set_aspect("equal")
        lo, hi = quads.reshape(-1, 2).min(0), quads.reshape(-1, 2).max(0)
        if zoom is None:
            ax.set_xlim(lo[0], hi[0])
            ax.set_ylim(lo[1], hi[1])
            ax.set_title(f"{len(quads)} leaf cells, {hits.sum()} intersection nodes")
        else:
            # zoom on the busiest intersection node's neighbourhood
            centre = quads[hits].mean(1)
            busiest = centre[np.argmin(np.linalg.norm(centre - centre.mean(0), axis=1))]
            ax.set_xlim(busiest[0] - zoom, busiest[0] + zoom)
            ax.set_ylim(busiest[1] - zoom, busiest[1] + zoom)
            ax.set_title("detail")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=18)
    parser.add_argument("--out", type=Path, default=HERE / "out")
    args = parser.parse_args()

    monkey, mod, tree = scene(args.max_depth)
    set_input(mod, "Show Cloud", True)

    # depth 0 gives the fragments as they entered, to compare lengths against
    set_input(mod, "Max Depth", 0)
    before = read_cloud(monkey)
    input_length = np.linalg.norm(
        before["b"][~before["is_cell"]] - before["a"][~before["is_cell"]], axis=1
    ).sum()

    set_input(mod, "Max Depth", args.max_depth)
    start = time.perf_counter()
    cloud = read_cloud(monkey)
    elapsed = time.perf_counter() - start
    for warning in mod.node_warnings:
        print(f"{warning.type}: {warning.message}")

    cells = cloud["is_cell"]
    frag = ~cells
    print(f"tree: {len(tree)} nodes; evaluated in {elapsed:.2f}s")
    print(
        f"fragments: {frag.sum()} segments in {len(np.unique(cloud['curve'][frag]))} pieces"
    )
    print(
        f"cells: {cells.sum()} leaves, max depth {cloud['depth'][cells].max()}, "
        f"{cloud['is_intersection'].sum()} intersection nodes"
    )

    failures = check(cloud, input_length)
    print("checks:", "all passed" if not failures else "; ".join(failures))

    args.out.mkdir(parents=True, exist_ok=True)
    plot(cloud, args.out / "suzanne_bsp.png")
    set_input(mod, "Show Cloud", False)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.out / "suzanne_bsp.blend"))


if __name__ == "__main__":
    main()
