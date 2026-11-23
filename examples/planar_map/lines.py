"""Lines for the planar map: visible edges by kind (Section 4.3) and hidden edges.

- `EdgeCurves`: one curve per edge with geometry, along its forward halfedge.
- `VisibleLines`: the merged map's edges, classified as outline (background on one
  side), silhouette or crease. The paper classifies by whether the patches either
  side are adjacent in 3D; here the input says which mesh edge each curve came
  from, so the class comes from there and from what the faces see.
- `HiddenLines`: the edges occlusion removed, cut into dashes.

Both are curves carrying Grease Pencil's stroke attributes; `ToGreasePencil`
turns them into their own layers above the fills.
"""

from __future__ import annotations

from regions import at, attr

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry

OUTLINE, SILHOUETTE, CREASE = 2, 1, 0


def edge_curves(halfedges, fragments, selection):
    """A curve along each selected forward halfedge: its origin, then the far end
    of each of its fragments. Halfedge attributes carry over to the points."""
    count, after = attr("integer", "count"), attr("integer", "after")
    keep = ~attr("boolean", "back") & (count > 0)
    if selection is not None:
        keep = keep & selection
    chosen = g.SeparateGeometry.point(halfedges, selection=keep).o.selection
    dup = g.DuplicateElements.point(chosen, amount=count + 1)
    k = dup.o.duplicate_index
    end = g.SampleIndex.point.vector(
        fragments, value=attr("vector", "b"), index=after + k - 1
    ).o.value
    return (
        dup.o.geometry
        >> g.SetPosition(position=(k == 0).switch.vector(end, attr("vector", "origin")))
        >> g.PointsToCurves(curve_group_id=attr("integer", "hid"), weight=k.to_float())
    )


def strokes(curves, radius, color):
    """Curves ready for Grease Pencil: stroke radius and colour, no fill."""
    return (
        curves
        >> g.SetCurveRadius(radius=radius)
        >> g.StoreNamedAttribute.point.color(name="vertex_color", value=color)
        >> g.StoreNamedAttribute.point.float(name="opacity", value=1.0)
    )


class VisibleLines(CustomGeometryGroup):
    """The merged map's edges as strokes, wider for outlines than silhouettes, and
    for silhouettes than creases."""

    _name = "Visible Lines"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        halfedges: InputGeometry = ...,
        fragments: InputGeometry = None,
        line_width: InputFloat = 0.0015,
    ):
        super().__init__(
            halfedges=halfedges, fragments=fragments, line_width=line_width
        )

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        fragments = tree.inputs.geometry("Fragments")
        width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
        hid = attr("integer", "hid")
        twin = hid + 1 - (hid % 2) * 2

        with g.Frame("Kind (4.3)"):
            count, after = attr("integer", "count"), attr("integer", "after")
            middle = after + count // 2
            sil = g.SampleIndex.point.float(
                fragments, value=attr("float", "sil"), index=middle
            ).o.value
            seen = attr("boolean", "seen")
            outline = seen != at(seen, twin)
            kind = outline.switch.integer(
                (sil >= 0.5).switch.integer(CREASE, SILHOUETTE), OUTLINE
            )
            classified = g.StoreNamedAttribute.point.integer(
                halfedges, name="kind", value=kind
            )

        lines = edge_curves(classified, fragments, None)
        kind = attr("integer", "kind")
        scale = g.IndexSwitch.float(kind, [0.45, 0.8, 1.3])
        strokes(lines, width * 0.5 * scale, (0.04, 0.04, 0.06, 1.0)) >> (
            tree.outputs.geometry("Curves")
        )


class HiddenLines(CustomGeometryGroup):
    """The edges occlusion removed, as thin dashed strokes."""

    _name = "Hidden Lines"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        halfedges: InputGeometry = ...,
        fragments: InputGeometry = None,
        line_width: InputFloat = 0.0015,
        dash: InputFloat = 0.006,
    ):
        super().__init__(
            halfedges=halfedges, fragments=fragments, line_width=line_width, dash=dash
        )

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        fragments = tree.inputs.geometry("Fragments")
        width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
        dash = tree.inputs.float("Dash", 0.006, min_value=1e-5)
        hidden = edge_curves(halfedges, fragments, attr("boolean", "hidden"))
        with g.Frame("Dashes: every other piece"):
            pieces = (
                g.ResampleCurve(hidden, mode="Length", length=dash) >> g.CurveToMesh()
            )
            dashes = (
                g.DeleteGeometry.edge(pieces, selection=g.Index().o.index % 2 == 1)
                >> g.MeshToCurve.edges()
            )
        strokes(dashes, width * 0.25, (0.35, 0.37, 0.42, 1.0)) >> (
            tree.outputs.geometry("Curves")
        )
