"""Run the planar map on Suzanne, check it, and plot the BSP.

    BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/planar_map/run_suzanne.py

Checks the partition (cells tile the root, fragments sit in their cells, no curve
length is lost) and the planar map (`next` is a permutation that continues where
each halfedge ends, every connected piece has V - E + F = 2, signed areas cancel).
Writes `suzanne_bsp.png` and `suzanne_bsp.blend` to `out/` next to this script
(`suzanne_subdiv<N>_*` with `--subdiv N`, which puts a Subdivision Surface modifier
before the planar map).
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
from bsp import CREASE
from planar_map import build
from mathutils import Vector
# isort: on


def scene(max_depth: int, subdiv: int = 0):
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
    if subdiv:
        smooth = monkey.modifiers.new("Subdivision", "SUBSURF")
        smooth.levels = smooth.render_levels = subdiv
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
    set_input(mod, "Region Material", fill_material())
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


def fill_material():
    """A Grease Pencil material; the regions' own colours come from their fill and
    stroke colour attributes. Fills show because the fill colour is opaque."""
    mat = bpy.data.materials.new("Region")
    bpy.data.materials.create_gpencil_data(mat)
    gp = mat.grease_pencil
    gp.fill_color = (1.0, 1.0, 1.0, 1.0)
    gp.color = (0.05, 0.05, 0.08, 1.0)
    return mat


def _get(attrs, name, n, width=1, dtype=np.int32):
    key = {3: "vector", 1: "value"}[width]
    out = np.zeros(n * width, dtype=np.float32 if width == 3 else dtype)
    attrs[name].data.foreach_get(key, out)
    return out.reshape(n, width) if width == 3 else out


def read_map(obj):
    """The halfedges (points) and region loops (curves) from the Halfedges output."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    geo = obj.evaluated_get(depsgraph).evaluated_geometry()
    pc = geo.pointcloud
    n = len(pc.points)
    half = {
        name: _get(pc.attributes, name, n)
        for name in ("hid", "vertex", "next", "face", "rank")
    }
    curves = geo.curves
    m = len(curves.points)
    positions = np.zeros(m * 3, dtype=np.float32)
    curves.attributes["position"].data.foreach_get("vector", positions)
    offsets = np.zeros(len(curves.curves) + 1, dtype=np.int32)
    curves.curve_offset_data.foreach_get("value", offsets)
    area = _get(curves.attributes, "area", len(curves.curves), dtype=np.float32)
    loops = [
        positions.reshape(m, 3)[offsets[i] : offsets[i + 1], :2]
        for i in range(len(curves.curves))
    ]
    # what each loop's face sees, from its first point (all points agree)
    firsts = offsets[:-1]
    if "patch" in curves.attributes:
        patch = _get(curves.attributes, "patch", m)[firsts]
        seen = np.zeros(m, dtype=bool)
        curves.attributes["seen"].data.foreach_get("value", seen)
        seen = seen[firsts]
    else:
        patch = np.full(len(firsts), -1)
        seen = np.zeros(len(firsts), dtype=bool)
    loops_seen = {"patch": patch, "seen": seen}
    return half, loops, area, loops_seen


def surface_mesh(obj):
    """The mesh the planar map sees: the object evaluated with every modifier
    before the planar map (a subdivision, say) and without the planar map."""
    planar = obj.modifiers["Planar Map"]
    planar.show_viewport = False
    obj.update_tag()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = bpy.data.meshes.new_from_object(evaluated)
    planar.show_viewport = True
    obj.update_tag()
    return mesh


def surface_patches(mesh, crease: float):
    """Face -> patch id: faces joined across edges that are neither creases nor
    boundaries, as `SurfacePatches` does in the tree."""
    parent = list(range(len(mesh.polygons)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    by_edge: dict[tuple[int, int], list[int]] = {}
    for poly in mesh.polygons:
        for key in poly.edge_keys:
            by_edge.setdefault(key, []).append(poly.index)
    for faces in by_edge.values():
        if len(faces) != 2:
            continue
        a, b = faces
        angle = mesh.polygons[a].normal.angle(mesh.polygons[b].normal)
        if angle <= crease:
            parent[find(a)] = find(b)
    roots = {}
    return [roots.setdefault(find(i), len(roots)) for i in range(len(parent))]


def raster_agreement(obj, camera, loops, area, loops_seen, crease, size=240):
    """The paper's measure (Section 5.3): the share of pixels where the region
    drawn there shows the same patch as a ray cast straight at the mesh.

    Islands are numbered differently here and in the tree, so each drawn patch
    id is matched to the true id it overlaps most.
    """
    from mathutils.bvhtree import BVHTree
    from matplotlib.path import Path as MplPath

    mesh = surface_mesh(obj)
    world = obj.matrix_world
    verts = [world @ v.co for v in mesh.vertices]
    tree = BVHTree.FromPolygons(verts, [tuple(p.vertices) for p in mesh.polygons])
    patch_of_face = surface_patches(mesh, crease)

    points = np.concatenate(loops)
    lo, hi = points.min(0), points.max(0)
    xs = np.linspace(lo[0], hi[0], size)
    ys = np.linspace(lo[1], hi[1], size)
    grid = np.stack(np.meshgrid(xs, ys), -1).reshape(-1, 2)

    origin = camera.matrix_world.translation
    rot = camera.matrix_world.to_3x3()
    truth = np.full(len(grid), -1)
    for i, (x, y) in enumerate(grid):
        hit = tree.ray_cast(origin, (rot @ Vector((x, y, -1.0))).normalized())
        if hit[0] is not None:
            truth[i] = patch_of_face[hit[2]]

    drawn = np.full(len(grid), -1)
    order = np.argsort(-area)  # largest first, as drawn
    for k in order:
        if area[k] <= 0 or not loops_seen["seen"][k]:
            continue
        inside = MplPath(loops[k]).contains_points(grid)
        drawn[inside] = loops_seen["patch"][k]

    # match tree patch ids to these by most common overlap
    mapping = {-1: -1}
    for p in np.unique(drawn[drawn >= 0]):
        values, counts = np.unique(truth[drawn == p], return_counts=True)
        mapping[p] = values[np.argmax(counts)]
    mapped = np.array([mapping[d] for d in drawn])
    return float((mapped == truth).mean())


def check_map(half, loops, area, node_area: float) -> tuple[list[str], dict]:
    """The planar map's invariants; returns what failed and some counts."""
    failures = []
    hid, nxt, vertex, face = half["hid"], half["next"], half["vertex"], half["face"]
    h = len(hid)
    if not (hid == np.arange(h)).all():
        failures.append("halfedges are not in hid order")
    if sorted(nxt) != list(range(h)):
        failures.append("next is not a permutation")
    twin = hid ^ 1
    if (vertex[nxt] != vertex[twin]).any():
        bad = (vertex[nxt] != vertex[twin]).sum()
        failures.append(f"{bad} halfedges continue from the wrong vertex")
    if (face[nxt] != face).any():
        failures.append("next leaves its face")

    # connected pieces of the graph, by union-find over edges
    ids = {v: i for i, v in enumerate(np.unique(vertex))}
    parent = list(range(len(ids)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in range(0, h, 2):
        a, b = find(ids[vertex[e]]), find(ids[vertex[e + 1]])
        parent[a] = b
    piece = np.array([find(ids[v]) for v in vertex])
    euler_bad = 0
    for p in np.unique(piece):
        mask = piece == p
        v = len(np.unique(vertex[mask]))
        e = mask.sum() // 2
        f = len(np.unique(face[mask]))
        euler_bad += v - e + f != 2
    if euler_bad:
        failures.append(f"{euler_bad} pieces have V - E + F != 2")

    total = float(area.sum())
    if abs(total) > node_area:
        failures.append(f"signed areas sum to {total:.3e}, over {node_area:.3e}")
    counts = {
        "vertices": len(ids),
        "edges": h // 2,
        "faces": len(np.unique(face)),
        "regions": int((area > 0).sum()),
        "pieces": len(np.unique(piece)),
        "area_sum": total,
    }
    return failures, counts


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
    parser.add_argument(
        "--subdiv", type=int, default=0, help="Subdivision Surface levels first"
    )
    parser.add_argument("--out", type=Path, default=HERE / "out")
    parser.add_argument(
        "--no-separating", action="store_true", help="turn off separating lines"
    )
    parser.add_argument(
        "--no-occlusion", action="store_true", help="don't merge hidden regions"
    )
    parser.add_argument(
        "--no-intersections",
        action="store_true",
        help="don't add curves where surfaces pass through each other",
    )
    args = parser.parse_args()

    monkey, mod, tree = scene(args.max_depth, args.subdiv)
    name = f"suzanne_subdiv{args.subdiv}" if args.subdiv else "suzanne"
    set_input(mod, "Separating Lines", not args.no_separating)
    set_input(mod, "Occlusion", not args.no_occlusion)
    set_input(mod, "Resolve Intersections", not args.no_intersections)
    set_input(mod, "Data", "BSP Cloud")

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
    print(f"evaluated in {elapsed:.2f}s")
    print(
        f"fragments: {frag.sum()} segments in {len(np.unique(cloud['curve'][frag]))} pieces"
    )
    print(
        f"cells: {cells.sum()} leaves, max depth {cloud['depth'][cells].max()}, "
        f"{cloud['is_intersection'].sum()} intersection nodes"
    )
    failures = check(cloud, input_length)
    print("partition checks:", "all passed" if not failures else "; ".join(failures))

    set_input(mod, "Data", "Halfedges")
    half, loops, area, loops_seen = read_map(monkey)
    quads = np.stack([cloud[f"p{k}"][cells, :2] for k in range(4)], axis=1)
    node_area = float(_area(quads[cloud["is_intersection"][cells]]).sum())
    failures, counts = check_map(half, loops, area, node_area)
    print(
        "planar map: {vertices} vertices, {edges} edges, {faces} faces "
        "({regions} bounded regions) in {pieces} pieces".format(**counts)
    )
    print("map checks:", "all passed" if not failures else "; ".join(failures))
    camera = bpy.data.objects["Camera"]
    agreement = raster_agreement(monkey, camera, loops, area, loops_seen, CREASE)
    print(f"raster agreement: {agreement:.1%} of pixels show the right patch")

    args.out.mkdir(parents=True, exist_ok=True)
    plot(cloud, args.out / f"{name}_bsp.png")
    set_input(mod, "Data", "None")
    bpy.ops.wm.save_as_mainfile(filepath=str(args.out / f"{name}_bsp.blend"))


if __name__ == "__main__":
    main()
