"""Render the image for each example in ``docs/examples/code``.

Each example is run in its own Blender (``bpy``) process, attached as a Geometry
Nodes modifier to the object described in ``SHOTS`` below and rendered with Cycles
to ``docs/examples/images/<name>.png``. An image is only re-rendered when the
example, its shot or this script changes, so running it before every docs build is
cheap. Quarto runs it as a ``pre-render`` step; it can also be run by hand:

    uv run python docs/examples/render.py              # stale images only
    uv run python docs/examples/render.py gears --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import runpy
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE / "code"
IMAGES = HERE / "images"
CACHE = IMAGES / ".hashes.json"
SOURCE = HERE.parents[1] / "src" / "nodebpy"


@dataclass
class Shot:
    """How to stage one example for its picture."""

    base: str = "empty"
    """Object the modifier goes on: 'empty', 'monkey', 'sphere' or 'roads'."""
    inputs: dict = field(default_factory=dict)
    """Modifier input values by socket name."""
    frame: int = 1
    """Frame to render; simulations are stepped up to it."""
    azimuth: float = 35.0
    elevation: float = 30.0
    zoom: float = 0.8
    """Below 1 moves the camera in, above 1 out."""
    samples: int = 48
    occlusion: float = 0.0
    """Ambient occlusion distance for the clay material; 0 turns it off."""


SHOTS = {
    "voxelize": Shot(
        base="monkey",
        inputs={"Voxel Size": 0.05},
        azimuth=-40,
        elevation=10,
        occlusion=0.1,
    ),
    "lego": Shot(
        base="monkey",
        inputs={"Brick Size": 0.1},
        azimuth=-40,
        elevation=25,
        occlusion=0.15,
    ),
    "repeat_grid": Shot(base="monkey", elevation=40, azimuth=-20, zoom=0.65),
    "city_builder": Shot(base="roads", elevation=40, zoom=0.7, occlusion=0.3),
    "golf_ball": Shot(elevation=15, zoom=0.85, samples=64),
    "gears": Shot(elevation=55, azimuth=-15, zoom=0.75, inputs={"Spin": 0.2}),
    "explosion": Shot(base="sphere", frame=8, elevation=20, zoom=0.75),
    "arrow_field": Shot(elevation=55, zoom=0.6),
    "forest": Shot(elevation=25, zoom=0.7),
}

WIDTH, HEIGHT = 960, 600


def _source_digest() -> bytes:
    """nodebpy's own source, since a change there can change what an example builds."""
    h = hashlib.sha256()
    for path in sorted(SOURCE.rglob("*.py")):
        h.update(path.read_bytes())
    return h.digest()


def _digest(name: str, source: bytes) -> str:
    h = hashlib.sha256(source)
    h.update((CODE / f"{name}.py").read_bytes())
    h.update(json.dumps(asdict(SHOTS[name]), sort_keys=True).encode())
    h.update(Path(__file__).read_bytes())
    return h.hexdigest()


# --------------------------------------------------------------------------
# Inside the Blender process
# --------------------------------------------------------------------------


def _base_object(kind: str):
    import bpy

    if kind == "monkey":
        bpy.ops.mesh.primitive_monkey_add()
        return bpy.context.object
    if kind == "sphere":
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2)
        return bpy.context.object
    if kind == "roads":
        curve = bpy.data.curves.new("Roads", "CURVE")
        curve.dimensions = "3D"
        for points in [
            [(-2.6, -1.8, 0), (-0.5, -0.2, 0), (0.8, 0.9, 0), (2.6, 1.4, 0)],
            [(-1.6, 2.6, 0), (-0.9, 0.5, 0), (0.4, -1.2, 0), (0.9, -2.6, 0)],
            [(0.8, 0.9, 0), (1.2, 2.6, 0)],
        ]:
            spline = curve.splines.new("BEZIER")
            spline.bezier_points.add(len(points) - 1)
            for point, co in zip(spline.bezier_points, points):
                point.co = co
                point.handle_left_type = point.handle_right_type = "AUTO"
        obj = bpy.data.objects.new("Roads", curve)
        bpy.context.scene.collection.objects.link(obj)
        return obj
    obj = bpy.data.objects.new("Example", bpy.data.meshes.new("Example"))
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _set_inputs(obj, mod, tree, values: dict) -> None:
    identifiers = {
        item.name: item.identifier
        for item in tree.interface.items_tree
        if item.item_type == "SOCKET" and item.in_out == "INPUT"
    }
    for name, value in values.items():
        getattr(mod.properties.inputs, identifiers[name]).value = value
    obj.update_tag()


def _clay(occlusion: float):
    """Light grey clay, darkened in creases within ``occlusion`` of the surface."""
    from nodebpy import shader as s

    with s.material("Clay") as clay:
        color = (0.62, 0.6, 0.57, 1.0)
        if occlusion:
            ao = s.AmbientOcclusion(distance=occlusion).o.ao
            color = (ao**3).mix.color((0.03, 0.03, 0.035, 1.0), color)
        s.PrincipledBSDF(base_color=color, roughness=0.55) >> s.MaterialOutput()
    return clay.material


def _bounds(obj):
    """World-space centre and radius of the evaluated object."""
    import bpy
    from mathutils import Vector

    depsgraph = bpy.context.evaluated_depsgraph_get()
    corners = [
        inst.matrix_world @ Vector(corner)
        for inst in depsgraph.object_instances
        if inst.object.original == obj or inst.parent and inst.parent.original == obj
        for corner in inst.object.bound_box
    ]
    lo = Vector([min(c[i] for c in corners) for i in range(3)])
    hi = Vector([max(c[i] for c in corners) for i in range(3)])
    return (lo + hi) / 2, (hi - lo).length / 2, lo.z


def _stage(obj, shot: Shot) -> None:
    import bpy
    from mathutils import Vector

    scene = bpy.context.scene
    center, radius, floor = _bounds(obj)

    # camera on a sphere around the geometry, far enough to fit it in frame
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 50
    camera = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(camera)
    az, el = math.radians(shot.azimuth), math.radians(shot.elevation)
    direction = Vector(
        (math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))
    )
    fov = 2 * math.atan(cam_data.sensor_width / 2 / cam_data.lens) * HEIGHT / WIDTH
    camera.location = center + direction * (radius / math.sin(fov / 2)) * shot.zoom
    camera.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
    cam_data.clip_end = 10_000
    scene.camera = camera

    # key and rim lights scaled to the scene, plus a dim blue world
    for name, angle, energy, offset in [
        ("Key", 12, 2.5, (-1, -1.4, 2.2)),
        ("Rim", 10, 1.5, (1.5, 2, 1)),
    ]:
        light = bpy.data.lights.new(name, "SUN")
        light.energy, light.angle = energy, math.radians(angle)
        sun = bpy.data.objects.new(name, light)
        sun.rotation_euler = Vector(offset).to_track_quat("Z", "Y").to_euler()
        scene.collection.objects.link(sun)
    world = bpy.data.worlds.new("World")
    world.color = (0.03, 0.035, 0.06)
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        0.09,
        0.1,
        0.16,
        1,
    )
    scene.world = world

    # a shadow catcher keeps the shadows but leaves the background transparent
    bpy.ops.mesh.primitive_plane_add(
        size=radius * 40, location=(center.x, center.y, floor)
    )
    bpy.context.object.is_shadow_catcher = True

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = shot.samples
    scene.cycles.use_denoising = True
    scene.render.film_transparent = True
    scene.render.resolution_x, scene.render.resolution_y = WIDTH, HEIGHT
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "AgX"


def render_one(name: str, out: Path) -> None:
    # nodebpy before bpy, so a nodebpy bundled with an add-on cannot shadow it
    import nodebpy  # noqa: F401, I001
    import bpy

    bpy.ops.wm.read_factory_settings(use_empty=True)
    shot = SHOTS[name]
    namespace = runpy.run_path(str(CODE / f"{name}.py"))
    tree = namespace["tree"].tree

    obj = _base_object(shot.base)
    # the input geometry carries the clay in its slot; generated geometry gets it
    # through the tree's "Material" input when it has one
    clay = _clay(shot.occlusion)
    obj.data.materials.append(clay)
    mod = obj.modifiers.new("Example", "NODES")
    mod.node_group = tree
    inputs = dict(shot.inputs)
    if "Material" in tree.interface.items_tree:
        inputs.setdefault("Material", clay)
    _set_inputs(obj, mod, tree, inputs)

    scene = bpy.context.scene
    scene.frame_end = max(scene.frame_end, shot.frame)
    for frame in range(1, shot.frame + 1):
        scene.frame_set(frame)

    _stage(obj, shot)

    scene.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="examples to render (default: all)")
    parser.add_argument("--force", action="store_true", help="ignore the cache")
    parser.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 4))
    parser.add_argument("--one", help=argparse.SUPPRESS)
    parser.add_argument("--out", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.one:
        render_one(args.one, Path(args.out))
        return 0

    unknown = set(args.names) - set(SHOTS)
    if unknown:
        parser.error(f"no shot for {', '.join(sorted(unknown))}")
    missing = {p.stem for p in CODE.glob("*.py")} - set(SHOTS)
    if missing:
        print(
            f"warning: no shot defined for {', '.join(sorted(missing))}",
            file=sys.stderr,
        )

    IMAGES.mkdir(exist_ok=True)
    try:
        cache = json.loads(CACHE.read_text())
    except (OSError, ValueError):
        cache = {}

    source = _source_digest()
    todo = [
        name
        for name in (args.names or SHOTS)
        if args.force
        or cache.get(name) != _digest(name, source)
        or not (IMAGES / f"{name}.png").exists()
    ]
    if not todo:
        return 0

    env = {**os.environ, "BLENDER_USER_EXTENSIONS": "/nonexistent"}

    def run(name: str) -> tuple[str, int, float, str]:
        start = time.perf_counter()
        proc = subprocess.run(
            [
                sys.executable,
                __file__,
                "--one",
                name,
                "--out",
                str(IMAGES / f"{name}.png"),
            ],
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        return (
            name,
            proc.returncode,
            time.perf_counter() - start,
            proc.stdout + proc.stderr,
        )

    failed = []
    # bpy is not thread-safe, so each render is its own process
    with ThreadPoolExecutor(args.jobs) as pool:
        for name, code, seconds, output in pool.map(run, todo):
            if code == 0:
                cache[name] = _digest(name, source)
                print(f"rendered {name} in {seconds:.0f}s")
            else:
                failed.append(name)
                print(f"failed to render {name}:\n{output[-3000:]}", file=sys.stderr)
            CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
