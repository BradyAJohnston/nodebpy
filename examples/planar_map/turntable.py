"""Vectorise Suzanne from a camera orbiting her, one frame at a time (Section 5.7).

    BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/planar_map/turntable.py --subdiv 2

Every frame is built from scratch: nothing is carried from one frame to the next.
Each frame is rendered and checked (partition, map, raster agreement), and the
frames are joined into `out/turntable_subdiv<N>.gif`, with per-frame numbers in
`out/turntable_subdiv<N>.json`.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# isort: off
import nodebpy  # noqa: F401  (before bpy, so the source tree wins)
import bpy
import numpy as np
from bsp import CREASE
from mathutils import Vector
from run_suzanne import (
    _area,
    check,
    check_map,
    raster_agreement,
    read_cloud,
    read_map,
    scene,
    set_input,
)
# isort: on


def place(camera, angle: float, radius: float, height: float) -> None:
    camera.location = (radius * math.sin(angle), -radius * math.cos(angle), height)
    direction = Vector((0.0, 0.0, 0.0)) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def frame_stats(monkey, mod, camera) -> dict:
    """Build this frame's map and check it, as run_suzanne.py does."""
    set_input(mod, "Data", "BSP Cloud")
    start = time.perf_counter()
    cloud = read_cloud(monkey)
    seconds = time.perf_counter() - start
    cells = cloud["is_cell"]
    frag = ~cells
    # the input length, for the length check, is the depth-0 fragments'
    set_input(mod, "Max Depth", 0)
    before = read_cloud(monkey)
    set_input(mod, "Max Depth", 18)
    input_length = float(
        np.linalg.norm(
            before["b"][~before["is_cell"]] - before["a"][~before["is_cell"]], axis=1
        ).sum()
    )
    failures = check(cloud, input_length)

    set_input(mod, "Data", "Halfedges")
    half, loops, area, loops_seen = read_map(monkey)
    quads = np.stack([cloud[f"p{k}"][cells, :2] for k in range(4)], axis=1)
    node_area = float(_area(quads[cloud["is_intersection"][cells]]).sum())
    map_failures, counts = check_map(half, loops, area, node_area)
    agreement = raster_agreement(
        monkey, camera, loops, area, loops_seen, CREASE, size=120
    )
    set_input(mod, "Data", "None")
    return {
        "fragments": int(frag.sum()),
        "nodes": int(cloud["is_intersection"].sum()),
        "regions": counts["regions"],
        "edges": counts["edges"],
        "agreement": round(agreement, 4),
        "seconds": round(seconds, 3),
        "failures": failures + map_failures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdiv", type=int, default=0)
    parser.add_argument("--frames", type=int, default=48)
    parser.add_argument("--size", type=int, default=640)
    parser.add_argument("--out", type=Path, default=HERE / "out")
    args = parser.parse_args()

    monkey, mod, _ = scene(18, args.subdiv)
    camera = bpy.data.objects["Camera"]
    sc = bpy.context.scene
    assert sc is not None
    radius = Vector((camera.location.x, camera.location.y)).length
    height = camera.location.z
    start_angle = math.atan2(camera.location.x, -camera.location.y)

    camera.data.lens = 60
    sc.render.engine = "BLENDER_WORKBENCH"
    display = sc.display
    assert display is not None
    display.shading.color_type = "MATERIAL"
    display.render_aa = "16"
    sc.view_settings.view_transform = "Standard"
    display.shading.background_type = "VIEWPORT"
    display.shading.background_color = (1.0, 1.0, 1.0)
    sc.render.resolution_x = sc.render.resolution_y = args.size
    set_input(mod, "Show Mesh", False)

    frames_dir = args.out / f"turntable_subdiv{args.subdiv}"
    frames_dir.mkdir(parents=True, exist_ok=True)
    stats = []
    for i in range(args.frames):
        angle = start_angle + 2 * math.pi * i / args.frames
        place(camera, angle, radius, height)
        monkey.update_tag()
        numbers = frame_stats(monkey, mod, camera)
        numbers.update(frame=i, degrees=round(math.degrees(angle) % 360, 1))
        stats.append(numbers)
        print(
            f"frame {i:3d}: {numbers['regions']:3d} regions, "
            f"{numbers['agreement']:.1%} right patch, "
            f"{'ok' if not numbers['failures'] else numbers['failures']}"
        )
        sc.render.filepath = str(frames_dir / f"{i:03d}.png")
        bpy.ops.render.render(write_still=True)

    from PIL import Image

    images = [
        Image.open(frames_dir / f"{i:03d}.png").convert("RGB")
        for i in range(args.frames)
    ]
    gif = args.out / f"turntable_subdiv{args.subdiv}.gif"
    images[0].save(
        gif,
        save_all=True,
        append_images=images[1:],
        duration=120,
        loop=0,
        optimize=True,
    )
    (args.out / f"turntable_subdiv{args.subdiv}.json").write_text(
        json.dumps(stats, indent=1)
    )
    bad = [s["frame"] for s in stats if s["failures"]]
    print(f"wrote {gif}; frames with failed checks: {bad or 'none'}")


if __name__ == "__main__":
    main()
