"""Stage 3 of "Robust Planar Maps for 3D Vectorization": occlusion (Section 4.1-4.3).

- `SurfacePatches`: the mesh's patches, faces connected across edges that are not
  creases, boundaries or intersections, as a face attribute `patch`.
- `RegionIdentity`: Section 4.1. Each face casts a 2D ray inward from the middle of
  its longest halfedge to the nearest curve, then a camera ray through the point
  halfway along. What that ray hits (patch, normal, or nothing) is the region's
  identity.
- `EdgeVisibility`: which edges to merge across. The paper merges neighbours with
  the same identity, but on a mesh one patch can fold over itself (Suzanne's ear
  over her head), and that rule would erase the fold's silhouette. So an edge with
  geometry must also be hidden itself: the camera ray through its middle hits
  the surface nearer than the curve.
- `MergeRegions`: Section 4.2. Drops hidden edges, relinks `next` past them by
  pointer jumping, and compacts the halfedges so `Faces` can relabel them.
"""

from __future__ import annotations

from bsp import BIG, perp
from regions import at, attr, jump_zone, store

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry, InputObject


def camera_ray(camera, screen):
    """Origin and direction, in this object's space, of the camera ray through the
    screen point `screen` (camera-space x / -z, y / -z)."""
    to_local = (
        g.ObjectInfo(g.SelfObject()).o.transform.invert()
        @ g.ObjectInfo(camera).o.transform
    )
    origin = g.CombineXYZ().o.vector.transform(to_local)
    direction = g.CombineXYZ(screen.x, screen.y, -1.0).o.vector.transform_direction(
        to_local
    )
    return origin, direction


def cast(surface, camera, screen):
    """The camera ray through `screen`, cast at the surface's patches."""
    origin, direction = camera_ray(camera, screen)
    ray = g.Raycast.integer(
        target_geometry=surface,
        attribute=attr("integer", "patch"),
        interpolation="Nearest",
        source_position=origin,
        ray_direction=direction,
        ray_length=1.0e5,
    ).o
    return ray, direction


def middle_fragment(fragments):
    """End points and cell size of the middle fragment of each halfedge's edge,
    and the unit normal to the left of the halfedge."""
    count, after = attr("integer", "count"), attr("integer", "after")
    index = after + count // 2

    def sample(kind, name):
        return getattr(g.SampleIndex.point, kind)(
            fragments, value=attr(kind, name), index=index
        ).o.value

    a, b = sample("vector", "a"), sample("vector", "b")
    size = sample("float", "size")
    along = (b - a).normalize()
    left = attr("boolean", "back").switch.vector(perp(along), perp(along) * -1.0)
    return (a + b) * 0.5, left, size


class SurfacePatches(CustomGeometryGroup):
    """Mark each face with its patch: faces connected across edges that are
    neither creases nor boundaries."""

    _name = "Surface Patches"
    _color_tag = "GEOMETRY"

    def __init__(self, mesh: InputGeometry = ..., crease_angle: InputFloat = 1.0472):
        super().__init__(mesh=mesh, crease_angle=crease_angle)

    def _build_group(self, tree):
        mesh = tree.inputs.geometry("Mesh")
        crease = tree.inputs.float("Crease Angle", 1.0472, subtype="ANGLE")
        (
            mesh
            >> g.SplitEdges(
                selection=(g.EdgeAngle().o.unsigned_angle > crease)
                | attr("boolean", "intersection")
            )
            >> g.StoreNamedAttribute.face.integer(
                name="patch", value=g.MeshIsland().o.island_index
            )
            >> tree.outputs.geometry("Surface")
        )


class FragmentWalls(CustomGeometryGroup):
    """Every fragment as a vertical wall, so Raycast can find the nearest curve
    along a 2D ray in the screen plane."""

    _name = "Fragment Walls"
    _color_tag = "GEOMETRY"

    def __init__(self, fragments: InputGeometry = ...):
        super().__init__(fragments=fragments)

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        capture = g.CaptureAttribute(fragments)
        index = capture.items.integer(g.Index(), "Index")
        ends = g.DuplicateElements.point(capture, amount=2)
        end = ends.o.duplicate_index
        (
            ends
            >> g.SetPosition(
                position=(end == 0).switch.vector(
                    attr("vector", "b"), attr("vector", "a")
                )
                - g.CombineXYZ(z=1.0).o.vector
            )
            >> g.PointsToCurves(curve_group_id=index.output, weight=end)
            >> g.CurveToMesh()
            >> g.ExtrudeMesh(mode="EDGES", offset=(0.0, 0.0, 2.0))
            >> tree.outputs.geometry("Walls")
        )


class RegionIdentity(CustomGeometryGroup):
    """Section 4.1: what each face sees, stored on all of its halfedges as
    `seen` (hit anything), `patch` and `normal`."""

    _name = "Region Identity"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        halfedges: InputGeometry = ...,
        fragments: InputGeometry = None,
        walls: InputGeometry = None,
        surface: InputGeometry = None,
        camera: InputObject = None,
    ):
        super().__init__(
            halfedges=halfedges,
            fragments=fragments,
            walls=walls,
            surface=surface,
            camera=camera,
        )

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        fragments = tree.inputs.geometry("Fragments")
        walls = tree.inputs.geometry("Walls")
        surface = tree.inputs.geometry("Surface")
        camera = tree.inputs.object("Camera")
        face, hid = attr("integer", "face"), attr("integer", "hid")
        count = attr("integer", "count")

        with g.Frame("Longest halfedge of each face"):
            longest = count.point.max(face)
            candidate = (count > 0) & (count == longest)
            chosen = hid == candidate.switch.integer(2**30, hid).point.min(face)

        with g.Frame("Inward to the nearest curve (2D)"):
            middle, left, size = middle_fragment(fragments)
            start = middle + left * (size * 1.0e-3)
            wall = g.Raycast.float(
                target_geometry=walls,
                source_position=start,
                ray_direction=left,
                ray_length=10.0,
            ).o
            reach = wall.is_hit.switch.float(size * 0.02, wall.hit_distance)
            inside = start + left * (reach * 0.5)

        with g.Frame("Camera ray through it (3D)"):
            hit, direction = cast(surface, camera, inside)
            # headlight: brightest where the surface faces the camera
            shade = hit.hit_normal.normalize().dot(direction.normalize()).abs()

        with g.Frame("Share with the face"):
            sample = chosen & (count > 0)
            seen = (sample & hit.is_hit).switch.integer(0, 1).point.max(face)
            known = sample.switch.integer(0, 1).point.max(face)
            patch = sample.switch.integer(-(2**30), hit.attribute).point.max(face)
            normal = sample.switch.vector((-BIG, -BIG, -BIG), hit.hit_normal).point.max(
                face
            )
            shade_face = sample.switch.float(-BIG, shade).point.max(face)
            store(
                halfedges,
                {
                    "known": ("boolean", known > 0),
                    "seen": ("boolean", seen > 0),
                    "patch": ("integer", (seen > 0).switch.integer(-1, patch)),
                    "normal": ("vector", normal),
                    "shade": ("float", shade_face.max(0.0)),
                },
            ) >> tree.outputs.geometry("Halfedges")


class EdgeVisibility(CustomGeometryGroup):
    """Mark edges whose curve is hidden behind the surface as `hidden`.

    An edge goes when both faces see the same thing (the paper's rule) and, if it
    has geometry, its curve is hidden: a camera ray through the middle of its
    middle fragment hits the surface clearly nearer than the curve. Keeping
    visible edges with the same patch on both sides keeps the silhouette where a
    surface folds over itself; keeping hidden edges between faces that see
    different things keeps a region whose visible outline is missing from the
    input curves.
    """

    _name = "Edge Visibility"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        halfedges: InputGeometry = ...,
        fragments: InputGeometry = None,
        surface: InputGeometry = None,
        camera: InputObject = None,
        tolerance: InputFloat = 0.002,
    ):
        super().__init__(
            halfedges=halfedges,
            fragments=fragments,
            surface=surface,
            camera=camera,
            tolerance=tolerance,
        )

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        fragments = tree.inputs.geometry("Fragments")
        surface = tree.inputs.geometry("Surface")
        camera = tree.inputs.object("Camera")
        tolerance = tree.inputs.float(
            "Tolerance",
            0.002,
            min_value=0.0,
            description="How much nearer than the curve, as a fraction of its "
            "distance, a hit must be to hide it",
        )
        hid = attr("integer", "hid")
        count = attr("integer", "count")
        twin = hid + 1 - (hid % 2) * 2

        with g.Frame("Is anything in front of the curve?"):
            index = attr("integer", "after") + count // 2

            def sample(kind, name):
                return getattr(g.SampleIndex.point, kind)(
                    fragments, value=attr(kind, name), index=index
                ).o.value

            middle = (sample("vector", "a") + sample("vector", "b")) * 0.5
            distance = (sample("float", "da") + sample("float", "db")) * 0.5
            hit, _ = cast(surface, camera, middle)
            in_front = hit.is_hit & (hit.hit_distance < distance * (1.0 - tolerance))

        with g.Frame("Do both faces see the same thing? (paper)"):
            seen, patch = attr("boolean", "seen"), attr("integer", "patch")
            known = attr("boolean", "known")
            # both faces must have been sampled: letting an unsampled face match
            # anything chains unrelated regions together through clusters of
            # tiny faces
            same = (
                known
                & at(known, twin)
                & (seen == at(seen, twin))
                & (patch == at(patch, twin))
            )

        # edges with geometry must also be hidden themselves; edges without
        # it (steps between adjacent nodes) go on the paper's rule alone
        hidden = same & ((count == 0) | in_front)
        store(halfedges, {"hidden": ("boolean", hidden)}) >> tree.outputs.geometry(
            "Halfedges"
        )


class MergeRegions(CustomGeometryGroup):
    """Section 4.2: remove hidden edges, merging the faces on either side."""

    _name = "Merge Regions"
    _color_tag = "GEOMETRY"

    def __init__(self, halfedges: InputGeometry = ...):
        super().__init__(halfedges=halfedges)

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        hid, nxt = attr("integer", "hid"), attr("integer", "next")
        hidden = attr("boolean", "hidden")
        twin = hid + 1 - (hid % 2) * 2
        count = g.DomainSize(halfedges, component="POINTCLOUD").o.point_count
        passes = (count.to_float() + 1.0).log(2.0).ceil() + 1
        skip = attr("integer", "skip")

        with g.Frame("Skip hidden halfedges"):
            # from a hidden halfedge, the next one around the vertex is
            # next(twin); jump until a kept one is reached
            skipped = jump_zone(
                halfedges,
                {"skip": ("integer", hidden.switch.integer(hid, at(nxt, twin)))},
                lambda: {"skip": ("integer", at(skip, skip))},
                passes,
            )

        with g.Frame("Compact"):
            kept = ~hidden
            edge = (
                g.AccumulateField.point.integer(
                    (kept & (hid % 2 == 0)).switch.integer(0, 1)
                ).o.leading
                - 1
            )
            new_hid = edge * 2 + hid % 2
            relinked = store(
                skipped,
                {
                    "new_hid": ("integer", new_hid),
                    "new_next": ("integer", at(skip, nxt)),
                },
            )
            new_next = at(attr("integer", "new_hid"), attr("integer", "new_next"))
            (
                store(relinked, {"next_kept": ("integer", new_next)})
                >> g.DeleteGeometry.point(selection=hidden)
                >> g.StoreNamedAttribute.point.integer(
                    name="hid", value=attr("integer", "new_hid")
                )
                >> g.StoreNamedAttribute.point.integer(
                    name="next", value=attr("integer", "next_kept")
                )
                >> tree.outputs.geometry("Halfedges")
            )
