"""Blender's Line Art modifier, rebuilt in Geometry Nodes.

Line Art draws a mesh's feature lines (contours, creases, material boundaries,
edge marks, intersections, loose edges) as Grease Pencil strokes, keeping the
segments whose occlusion level (how many surfaces hide them) is in a range. This
example does the same with the pieces of `examples/planar_map`:

- `LineArtEdges`: the feature edges by type, seen from the camera and flattened
  onto the screen, with each point's distance from the camera.
- `SampledStrokes` (the default, fast): the curves resampled to about a pixel,
  each sample's occlusion level counted by casting again past each hit, smoothed
  along the curve and chained into strokes, placed back in 3D at their distance
  from the camera.
- The precise path: `CurveFragments`, `BSPCells` and `OrderedFragments` from the
  planar map cut the curves wherever they cross on screen, so a piece between two
  crossings has one level throughout; `OcclusionLevels` takes each run's
  majority and `ChainStrokes` joins the kept pieces.

The modifier goes on a Grease Pencil object, as Line Art does.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "planar_map"))

# isort: off
from bsp import BSPCells, CurveFragments, ResolveIntersections  # ty: ignore[import-not-found]
from occlusion import camera_ray  # ty: ignore[import-not-found]
from regions import OrderedFragments, at, attr, store  # ty: ignore[import-not-found]
# isort: on

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry, InputInteger, InputObject

# Line Art's default crease threshold is 140 degrees between faces, so normals
# more than 40 degrees apart
CREASE = math.radians(40)
KINDS = ["Contour", "Crease", "Material", "Edge Mark", "Intersection", "Loose"]


class LineArtEdges(CustomGeometryGroup):
    """Feature edges of a mesh as screen-space curves.

    Each point carries `dist` (distance from the camera), `spline` (the curve it
    came from) and `kind`, the type of the segment starting there: Mesh to Curve
    averages edge attributes onto points, so each vertex stores the share of its
    selected edges of each type, and a segment takes the type with the largest
    share across its two ends.
    """

    _name = "Line Art Edges"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        mesh: InputGeometry = ...,
        camera: InputObject = None,
        crease_angle: InputFloat = CREASE,
        **kinds,
    ):
        super().__init__(mesh=mesh, camera=camera, crease_angle=crease_angle, **kinds)

    def _build_group(self, tree):
        mesh = tree.inputs.geometry("Mesh")
        camera = tree.inputs.object("Camera")
        crease = tree.inputs.float("Crease Angle", CREASE, subtype="ANGLE")
        enabled = {name: tree.inputs.boolean(name, True) for name in KINDS}

        self_matrix = g.ObjectInfo(g.SelfObject()).o.transform
        camera_matrix = g.ObjectInfo(camera).o.transform
        eye = g.ObjectInfo(camera).o.location.transform(self_matrix.invert())

        with g.Frame("Edge types"):
            facing = g.Normal().o.normal.dot(g.Position().o.position - eye) < 0.0
            share = g.EvaluateOnDomain.face.float(facing.switch.float(0.0, 1.0)).o.value
            faces = g.EdgeNeighbors().o.face_count
            silhouette = (share > 0.01) & (share < 0.99)
            material = g.MaterialIndex().o.material_index.to_float()
            mean = g.EvaluateOnDomain.face.float(material).o.value
            mean_sq = g.EvaluateOnDomain.face.float(material * material).o.value
            masks = {
                "Contour": silhouette | (faces == 1),
                "Crease": (g.EdgeAngle().o.unsigned_angle > crease)
                | attr("boolean", "sharp_edge"),
                "Material": (mean_sq - mean * mean) > 0.01,
                "Edge Mark": attr("boolean", "freestyle_edge"),
                "Intersection": attr("boolean", "intersection"),
                "Loose": faces == 0,
            }
            masks = {name: mask & enabled[name] for name, mask in masks.items()}
            # one code per edge, the first type that applies; -1 for none
            code = -1
            for k in reversed(range(len(KINDS))):
                code = masks[KINDS[k]].switch.integer(code, k)

        with g.Frame("Keep only the feature edges"):
            # classify once on the full mesh, then work on the few edges left:
            # each store on the full mesh would evaluate the face and edge
            # fields again
            features = (
                mesh
                >> g.StoreNamedAttribute.edge.integer(name="kind_edge", value=code)
                >> g.DeleteGeometry.face(selection=True, mode="ONLY_FACE")
                >> g.DeleteGeometry.edge(selection=attr("integer", "kind_edge") < 0)
            )

        with g.Frame("Share of each type at each vertex"):
            kind_edge = attr("integer", "kind_edge")
            marked = features
            for k in range(len(KINDS)):
                marked = marked >> g.StoreNamedAttribute.point.float(
                    name=f"share{k}",
                    value=g.EvaluateOnDomain.edge.float(
                        (kind_edge == k).switch.float(0.0, 1.0)
                    ).o.value,
                )

        with g.Frame("Kind of each segment"):
            nxt = g.OffsetPointInCurve(offset=1).o.point_index
            best = kind = None
            for k in range(len(KINDS)):
                s = attr("float", f"share{k}")
                both = s + at(s, nxt)
                if best is None:
                    best, kind = both, 0
                    continue
                more = both > best
                best = more.switch.float(best, both)
                kind = more.switch.integer(kind, k)

        with g.Frame("Perspective divide"):
            q = g.Position().o.position.transform(camera_matrix.invert() @ self_matrix)
            screen = g.CombineXYZ(q.x / -q.z, q.y / -q.z)

        (
            marked
            >> g.MeshToCurve.edges()
            >> g.StoreNamedAttribute.point.float(
                name="dist", value=(g.Position().o.position - eye).length()
            )
            >> g.StoreNamedAttribute.point.integer(
                name="spline", value=g.CurveOfPoint().o.curve_index
            )
            >> g.StoreNamedAttribute.point.integer(name="kind", value=kind)
            >> g.SetPosition(position=screen)
            >> tree.outputs.geometry("Curves")
        )


class OcclusionLevels(CustomGeometryGroup):
    """How many surfaces hide each fragment, and whether its run keeps it.

    From the camera towards the fragment's midpoint, cast; each hit nearer than
    the fragment adds a level and the next cast starts just past it. A run of
    fragments between two crossings has one level in truth, so it keeps its
    fragments when most of them are in [Level Start, Level End].
    """

    _name = "Occlusion Levels"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        fragments: InputGeometry = ...,
        surface: InputGeometry = None,
        camera: InputObject = None,
        level_start: InputInteger = 0,
        level_end: InputInteger = 0,
        tolerance: InputFloat = 0.002,
    ):
        super().__init__(
            fragments=fragments,
            surface=surface,
            camera=camera,
            level_start=level_start,
            level_end=level_end,
            tolerance=tolerance,
        )

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        surface = tree.inputs.geometry("Surface")
        camera = tree.inputs.object("Camera")
        start = tree.inputs.integer("Level Start", 0, min_value=0)
        end = tree.inputs.integer("Level End", 0, min_value=0)
        tolerance = tree.inputs.float("Tolerance", 0.002, min_value=0.0)

        a, b = attr("vector", "a"), attr("vector", "b")
        middle = (a + b) * 0.5
        distance = (attr("float", "da") + attr("float", "db")) * 0.5
        origin, direction = camera_ray(camera, middle)
        unit = direction.normalize()
        reach = distance * (1.0 - tolerance)
        step = distance * 1.0e-4

        with g.Frame("Count the surfaces in front"):
            travel, level = attr("float", "travel"), attr("integer", "level")
            searching = attr("boolean", "searching")
            zone = g.RepeatZone(end + 1)
            state = zone.items.geometry(
                store(
                    fragments,
                    {
                        "travel": ("float", 0.0),
                        "level": ("integer", 0),
                        "searching": ("boolean", True),
                    },
                ),
                "Fragments",
            )
            hit = g.Raycast.float(
                target_geometry=surface,
                source_position=origin + unit * (travel + step),
                ray_direction=unit,
                ray_length=(reach - travel - step).max(0.0),
            ).o
            found = searching & hit.is_hit & (travel + step < reach)
            (
                store(
                    state.current,
                    {
                        "travel": (
                            "float",
                            found.switch.float(
                                travel, travel + step + hit.hit_distance
                            ),
                        ),
                        "level": ("integer", level + found.switch.integer(0, 1)),
                        "searching": ("boolean", found),
                    },
                )
                >> state.next
            )

        with g.Frame("Majority over each run between crossings"):
            idx = g.Index().o.index
            curve, cell = attr("integer", "curve"), attr("integer", "cell")
            in_node = attr("boolean", "in_node")
            same = (idx > 0) & (at(curve, idx - 1) == curve)
            same = same & (at(in_node, idx - 1) == in_node)
            same = same & (~in_node | (at(cell, idx - 1) == cell))
            run = g.AccumulateField.point.integer(same.switch.integer(1, 0)).o.leading
            level = attr("integer", "level")
            within = (level >= start) & (level <= end)
            keep = within.switch.float(0.0, 1.0).point.mean(run) > 0.5
            store(state.result, {"keep": ("boolean", keep)}) >> tree.outputs.geometry(
                "Fragments"
            )


class ChainStrokes(CustomGeometryGroup):
    """Kept fragments joined into strokes along their original curves, one type
    per stroke, placed in 3D at their distance from the camera."""

    _name = "Chain Strokes"
    _color_tag = "GEOMETRY"

    def __init__(self, fragments: InputGeometry = ..., camera: InputObject = None):
        super().__init__(fragments=fragments, camera=camera)

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        camera = tree.inputs.object("Camera")
        kept = g.SeparateGeometry.point(
            fragments, selection=attr("boolean", "keep")
        ).o.selection
        # Ordered Fragments sorted by segment then fraction: curve order
        idx = g.Index().o.index
        a, b = attr("vector", "a"), attr("vector", "b")
        spline, kind = attr("integer", "spline"), attr("integer", "kind")

        with g.Frame("Chains"):
            joined = (
                (idx > 0)
                & (at(spline, idx - 1) == spline)
                & (at(kind, idx - 1) == kind)
                & ((at(b, idx - 1) - a).length() < 1.0e-9)
            )
            follows = at(joined, idx + 1) & (
                idx + 1 < g.DomainSize(kept, component="POINTCLOUD").o.point_count
            )
            chain = g.AccumulateField.point.integer(
                joined.switch.integer(1, 0)
            ).o.leading
            marked = store(
                kept,
                {
                    "chain": ("integer", chain),
                    "order": ("integer", idx * 2),
                    "last": ("boolean", ~follows),
                },
            )

        with g.Frame("Points, back in 3D"):
            dup = g.DuplicateElements.point(
                marked, amount=attr("boolean", "last").switch.integer(1, 2)
            )
            end = dup.o.duplicate_index == 1
            screen = end.switch.vector(a, b)
            distance = end.switch.float(attr("float", "da"), attr("float", "db"))
            origin, direction = camera_ray(camera, screen)
            position = origin + direction.normalize() * distance
            (
                dup.o.geometry
                >> g.SetPosition(position=position)
                >> g.PointsToCurves(
                    curve_group_id=attr("integer", "chain"),
                    weight=(
                        attr("integer", "order") + dup.o.duplicate_index
                    ).to_float(),
                )
                >> tree.outputs.geometry("Strokes")
            )


class SampledStrokes(CustomGeometryGroup):
    """The fast path: visibility per sample instead of per BSP piece.

    Curves are resampled to `Spacing` (about a pixel) and each sample counts the
    surfaces in front of it, as `OcclusionLevels` does for fragments. The result
    is smoothed along each curve, so a grazing ray can't flicker one sample on its
    own, and kept samples are chained into strokes, split where the curve, the
    selection or the edge type changes. Where visibility changes is then only
    known to within one sample, but nothing runs pass by pass over the whole
    cloud, which is what the BSP spends its time on.
    """

    _name = "Sampled Strokes"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        curves: InputGeometry = ...,
        surface: InputGeometry = None,
        camera: InputObject = None,
        level_start: InputInteger = 0,
        level_end: InputInteger = 0,
        spacing: InputFloat = 0.0007,
        tolerance: InputFloat = 0.002,
    ):
        super().__init__(
            curves=curves,
            surface=surface,
            camera=camera,
            level_start=level_start,
            level_end=level_end,
            spacing=spacing,
            tolerance=tolerance,
        )

    def _build_group(self, tree):
        curves = tree.inputs.geometry("Curves")
        surface = tree.inputs.geometry("Surface")
        camera = tree.inputs.object("Camera")
        start = tree.inputs.integer("Level Start", 0, min_value=0)
        end = tree.inputs.integer("Level End", 0, min_value=0)
        spacing = tree.inputs.float("Spacing", 0.0007, min_value=1.0e-6)
        tolerance = tree.inputs.float("Tolerance", 0.002, min_value=0.0)

        samples = g.ResampleCurve(curves, mode="Length", length=spacing)
        position = g.Position().o.position
        distance = attr("float", "dist")
        origin, direction = camera_ray(camera, position)
        unit = direction.normalize()
        reach = distance * (1.0 - tolerance)
        step = distance * 1.0e-4

        with g.Frame("Count the surfaces in front"):
            travel, level = attr("float", "travel"), attr("integer", "level")
            searching = attr("boolean", "searching")
            zone = g.RepeatZone(end + 1)
            state = zone.items.geometry(
                store(
                    samples,
                    {
                        "travel": ("float", 0.0),
                        "level": ("integer", 0),
                        "searching": ("boolean", True),
                    },
                ),
                "Samples",
            )
            hit = g.Raycast.float(
                target_geometry=surface,
                source_position=origin + unit * (travel + step),
                ray_direction=unit,
                ray_length=(reach - travel - step).max(0.0),
            ).o
            found = searching & hit.is_hit & (travel + step < reach)
            (
                store(
                    state.current,
                    {
                        "travel": (
                            "float",
                            found.switch.float(
                                travel, travel + step + hit.hit_distance
                            ),
                        ),
                        "level": ("integer", level + found.switch.integer(0, 1)),
                        "searching": ("boolean", found),
                    },
                )
                >> state.next
            )

        with g.Frame("Smooth along the curve, then chain"):
            level = attr("integer", "level")
            within = ((level >= start) & (level <= end)).switch.float(0.0, 1.0)
            keep = g.BlurAttribute(within, iterations=2).o.value > 0.5
            idx = g.Index().o.index
            spline = g.CurveOfPoint().o.curve_index
            kind = attr("integer", "kind")
            joined = (
                (idx > 0)
                & (at(spline, idx - 1) == spline)
                & at(keep, idx - 1)
                & (at(kind, idx - 1) == kind)
            )
            chain = g.AccumulateField.point.integer(
                joined.switch.integer(1, 0)
            ).o.leading
            marked = store(
                state.result,
                {"keep": ("boolean", keep), "chain": ("integer", chain)},
            )
            back = origin + unit * distance
            (
                g.CurveToPoints.evaluated(marked)
                >> g.DeleteGeometry.point(selection=~attr("boolean", "keep"))
                >> g.SetPosition(position=back)
                >> g.PointsToCurves(
                    curve_group_id=attr("integer", "chain"),
                    weight=g.Index().o.index.to_float(),
                )
                >> tree.outputs.geometry("Strokes")
            )


def build(name: str = "Line Art (Nodes)"):
    """The modifier tree, for a Grease Pencil object."""
    with g.tree(name, clear=True, is_modifier=True) as tree:
        tree.inputs.geometry("Geometry")
        source = tree.inputs.object("Source")
        camera = tree.inputs.object("Camera")
        with tree.inputs.panel("Edge Types"):
            # Intersection is off by default: its exact Mesh Boolean costs far
            # more than everything else (see the README)
            kinds = {
                name: tree.inputs.boolean(name, name not in ("Loose", "Intersection"))
                for name in KINDS
            }
            crease = tree.inputs.float(
                "Crease Angle", CREASE, subtype="ANGLE", min_value=0.0
            )
        with tree.inputs.panel("Occlusion"):
            start = tree.inputs.integer("Level Start", 0, min_value=0, max_value=16)
            end = tree.inputs.integer("Level End", 0, min_value=0, max_value=16)
        with tree.inputs.panel("Precision"):
            method = tree.inputs.menu(
                "Method",
                "Sampled",
                description="Sampled: visibility per sample, fast. Precise: "
                "curves cut where they cross on screen (the planar map's BSP)",
            )
            spacing = tree.inputs.float("Spacing", 0.0007, min_value=1.0e-6)
            max_depth = tree.inputs.integer("Max Depth", 16, min_value=4, max_value=24)
        with tree.inputs.panel("Stroke"):
            radius = tree.inputs.float(
                "Radius", 0.0025, min_value=0.0, subtype="DISTANCE"
            )
            material = tree.inputs.material("Stroke Material")

        mesh = g.RealizeInstances(
            g.ObjectInfo(source, transform_space="RELATIVE").o.geometry
        )
        solid = g.Switch(kinds["Intersection"], mesh, ResolveIntersections(mesh))
        edges = LineArtEdges(
            solid,
            camera=camera,
            crease_angle=crease,
            **{
                name.lower().replace(" ", "_"): socket for name, socket in kinds.items()
            },
        )
        # One Menu Switch only: a menu input linked to two gets no items. A
        # repeat zone inside a group makes Blender evaluate the group's
        # geometry input even when a switch doesn't use its output, so the
        # precise path gets no input at all unless it is chosen.
        precise_on = g.MenuSwitch.boolean(
            method, {"Sampled": False, "Precise": True}
        ).o.output
        fragments = OrderedFragments(
            g.Switch(precise_on, None, edges)
            >> CurveFragments()
            # and no passes: each pass has a fixed cost even with no data
            >> BSPCells(
                max_depth=precise_on.switch.integer(0, max_depth),
                separating_lines=False,
            )
        )
        precise = ChainStrokes(
            OcclusionLevels(
                fragments,
                surface=solid,
                camera=camera,
                level_start=start,
                level_end=end,
            ),
            camera=camera,
        )
        sampled = SampledStrokes(
            edges,
            surface=solid,
            camera=camera,
            level_start=start,
            level_end=end,
            spacing=spacing,
        )
        (
            g.Switch(precise_on, sampled, precise)
            >> g.SetCurveRadius(radius=radius)
            >> g.CurvesToGreasePencil(instances_as_layers=False)
            >> g.SetMaterial(material=material)
            >> tree.outputs.geometry("Grease Pencil")
        )
    return tree
