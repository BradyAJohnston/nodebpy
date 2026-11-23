"""Compare the node Line Art with Blender's Line Art modifier on Suzanne.

    BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/line_art/compare.py --subdiv 0 1 2 3

For each subdivision level: evaluation time of each (median of repeated updates
after nudging the camera, the other modifier disabled), stroke counts, and how
well the strokes agree on screen (precision: share of our stroke pixels within
2 px of Line Art's; recall: the reverse). Writes a side-by-side plot per level
and `out/compare.json`.
"""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# isort: off
import nodebpy  # noqa: F401  (before bpy, so the source tree wins)
import bpy
import numpy as np
from line_art import build
from mathutils import Vector
# isort: on

RES = 800


def set_input(mod, name: str, value) -> None:
    for item in mod.node_group.interface.items_tree:
        if item.item_type == "SOCKET" and item.in_out == "INPUT" and item.name == name:
            getattr(mod.properties.inputs, item.identifier).value = value
            # without a tag the evaluated copy keeps the old value
            mod.id_data.update_tag()
            return
    raise KeyError(name)


def scene(subdiv: int, intersections: bool):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_monkey_add()
    monkey = bpy.context.object
    sc = bpy.context.scene
    assert monkey is not None and sc is not None
    if subdiv:
        smooth = monkey.modifiers.new("Subdivision", "SUBSURF")
        smooth.levels = smooth.render_levels = subdiv

    cam_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", cam_data)
    sc.collection.objects.link(camera)
    camera.location = (3.2, -5.5, 1.8)
    camera.rotation_euler = (
        (Vector((0, 0, 0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    )
    sc.camera = camera

    mat = bpy.data.materials.new("Line")
    bpy.data.materials.create_gpencil_data(mat)

    def pencil(name):
        data = bpy.data.grease_pencils.new(name)
        data.layers.new("Lines")
        data.materials.append(mat)
        obj = bpy.data.objects.new(name, data)
        sc.collection.objects.link(obj)
        return obj

    native = pencil("Line Art")
    lineart = native.modifiers.new("Line Art", "LINEART")
    lineart.source_type = "OBJECT"
    lineart.source_object = monkey
    lineart.target_layer = "Lines"
    lineart.target_material = mat
    lineart.use_intersection = intersections
    lineart.use_cache = False

    nodes = pencil("Line Art (Nodes)")
    mod = nodes.modifiers.new("Line Art (Nodes)", "NODES")
    mod.node_group = build().tree
    set_input(mod, "Source", monkey)
    set_input(mod, "Camera", camera)
    set_input(mod, "Stroke Material", mat)
    set_input(mod, "Intersection", intersections)
    return monkey, camera, native, nodes


def timed(camera, n: int = 7) -> float:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    times = []
    for i in range(n):
        camera.location.x += 1.0e-4 if i % 2 else -1.0e-4
        start = time.perf_counter()
        depsgraph.update()
        times.append(time.perf_counter() - start)
    return statistics.median(times)


def strokes(obj) -> list[np.ndarray]:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    gp = obj.evaluated_get(depsgraph).data
    out = []
    for layer in gp.layers:
        frame = layer.current_frame()
        if frame is None:
            continue
        for stroke in frame.drawing.strokes:
            pts = np.array([p.position for p in stroke.points], dtype=np.float64)
            if len(pts):
                out.append(pts)  # both objects sit at the origin
    return out


def project(camera, pts: np.ndarray) -> np.ndarray:
    m = np.array(camera.matrix_world.inverted())
    q = pts @ m[:3, :3].T + m[:3, 3]
    return q[:, :2] / -q[:, 2:3]


def raster(lines: list[np.ndarray], lo, hi) -> np.ndarray:
    image = np.zeros((RES, RES), dtype=bool)
    scale = (RES - 1) / (hi - lo).max()
    for line in lines:
        pix = (line - lo) * scale
        for p, q in itertools.pairwise(pix):
            n = int(np.ceil(np.linalg.norm(q - p) * 2)) + 1
            t = np.linspace(0, 1, n)[:, None]
            s = np.round(p + (q - p) * t).astype(int)
            ok = (s >= 0).all(1) & (s < RES).all(1)
            image[s[ok, 1], s[ok, 0]] = True
    return image


def dilate(image: np.ndarray, r: int = 2) -> np.ndarray:
    out = image.copy()
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            out |= np.roll(np.roll(image, dx, 0), dy, 1)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdiv", type=int, nargs="+", default=[0, 1, 2, 3])
    parser.add_argument("--intersections", action="store_true")
    parser.add_argument("--out", type=Path, default=HERE / "out")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    results = []
    for level in args.subdiv:
        monkey, camera, native, nodes = scene(level, args.intersections)
        faces = len(
            monkey.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.polygons
        )
        timings = {}
        for obj, other in ((native, nodes), (nodes, native)):
            for m in other.modifiers:
                m.show_viewport = False
            for m in obj.modifiers:
                m.show_viewport = True
            timings[obj.name] = timed(camera)
        for m in native.modifiers:
            m.show_viewport = True
        lines = {obj.name: strokes(obj) for obj in (native, nodes)}
        screen = {
            k: [project(camera, line) for line in v if len(line) > 1]
            for k, v in lines.items()
        }
        every = np.concatenate([p for v in screen.values() for p in v])
        lo, hi = every.min(0), every.max(0)
        theirs = raster(screen["Line Art"], lo, hi)
        ours = raster(screen["Line Art (Nodes)"], lo, hi)
        precision = (ours & dilate(theirs)).sum() / max(ours.sum(), 1)
        recall = (theirs & dilate(ours)).sum() / max(theirs.sum(), 1)
        row = {
            "subdiv": level,
            "faces": faces,
            "line_art_s": round(timings["Line Art"], 4),
            "nodes_s": round(timings["Line Art (Nodes)"], 4),
            "speedup": round(timings["Line Art"] / timings["Line Art (Nodes)"], 2),
            "line_art_strokes": len(lines["Line Art"]),
            "nodes_strokes": len(lines["Line Art (Nodes)"]),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
        }
        results.append(row)
        print(row)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5.4))
        for ax, (title, image) in zip(
            axes,
            [
                ("Line Art modifier", theirs),
                ("Line Art (Nodes)", ours),
                ("difference: Line Art only red, nodes only blue", None),
            ],
        ):
            if image is not None:
                ax.imshow(~image, cmap="gray", origin="lower")
            else:
                rgb = np.ones((RES, RES, 3))
                rgb[theirs & ~dilate(ours)] = (0.85, 0.15, 0.1)
                rgb[ours & ~dilate(theirs)] = (0.1, 0.3, 0.85)
                rgb[ours & dilate(theirs)] = (0.2, 0.2, 0.2)
                ax.imshow(rgb, origin="lower")
            ax.set_title(title)
            ax.set_xticks([])
            ax.set_yticks([])
        fig.suptitle(
            f"subdivision {level}: {faces} faces; Line Art {row['line_art_s'] * 1000:.0f} ms, "
            f"nodes {row['nodes_s'] * 1000:.0f} ms; precision {precision:.1%}, recall {recall:.1%}"
        )
        fig.tight_layout()
        tag = "_intersections" if args.intersections else ""
        fig.savefig(args.out / f"compare_subdiv{level}{tag}.png", dpi=110)
        plt.close(fig)

    tag = "_intersections" if args.intersections else ""
    (args.out / f"compare{tag}.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
