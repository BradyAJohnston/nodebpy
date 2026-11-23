"""Stage 1 of "Robust Planar Maps for 3D Vectorization" (Fuchs & Crane, TOG 2026).

Builds the paper's binary space partition (Section 2) in Geometry Nodes: the screen
is split recursively until every cell crosses at most one curve, or the cell is at
the maximum depth. Cells still crossed by more than one curve at that depth are the
paper's *intersection nodes*, which become vertices of the planar map in stage 2.

Three groups lead up to the partition:

- `ProjectedContours`: silhouette, boundary and crease edges of a mesh, seen from a
  camera and flattened onto the XY plane with a perspective divide.
- `CurveFragments`: those curves cut into pieces that turn by less than a half turn,
  so no piece can cross itself (the paper's preprocessing), with each straight
  segment as one point carrying its end points `a`, `b` and its piece id `curve`.
- `BSPCells`: the partition itself, as a repeat zone with one tree level per pass,
  including separating lines (Section 2.3).

Cells and fragments live in one point cloud. Every point has a `cell` attribute: the
cell's path through the tree (`2 * parent + child`), which a fragment shares with
the cell it lies in. Grouping fields by `cell` then gives each cell what it needs
from its fragments (and each fragment what it needs from its cell) without index
lookups.

Each pass has three steps. *Decide* picks every cell's split line and stores it on
all of the cell's points (`split`, `axis`, `m1`, `m2`). *Duplicate* copies cells that
split and fragments that the stored line cuts. *Rewrite* turns the copies into
children. Storing the decision matters: sums and means change when points are
duplicated, so nothing after the duplicate recomputes them.
"""

from __future__ import annotations

import math

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import (
    InputBoolean,
    InputFloat,
    InputGeometry,
    InputInteger,
    InputObject,
    InputVector,
)

BIG = 1.0e9
CREASE = math.radians(60)
MAX_TURN = math.radians(160)

# Every attribute of the cloud: name -> type, as the `g.NamedAttribute` /
# `g.StoreNamedAttribute.point` variant and the interface socket method.
CLOUD = {
    "is_cell": "boolean",
    "cell": "integer",
    "depth": "integer",
    "curve": "integer",
    "a": "vector",
    "b": "vector",
    "p0": "vector",
    "p1": "vector",
    "p2": "vector",
    "p3": "vector",
    "split": "boolean",
    "axis": "integer",
    "m1": "vector",
    "m2": "vector",
}


# --------------------------------------------------------------------------
# Reading and writing the cloud
# --------------------------------------------------------------------------


class ReadCloud(CustomGeometryGroup):
    """Every attribute of the cloud as a field, from one node.

    Fields read whatever geometry they are evaluated on, so one of these serves a
    whole pass: before a write and after it, before a duplicate and after it.
    """

    _name = "Read BSP Cloud"
    _color_tag = "INPUT"

    def __init__(self):
        super().__init__()

    def _build_group(self, tree):
        for name, kind in CLOUD.items():
            value = getattr(g.NamedAttribute, kind)(name).o.attribute
            value >> getattr(tree.outputs, kind)(name)


def writer(group_name: str, names: list[str]) -> type[CustomGeometryGroup]:
    """A group that writes `names` to the cloud.

    All values are captured on the incoming geometry first, then stored, so no
    value sees another's new contents whatever order the stores run in.
    """

    class Write(CustomGeometryGroup):
        _name = group_name
        _color_tag = "ATTRIBUTE"

        def __init__(self, geometry: InputGeometry = ..., **values):
            super().__init__(geometry=geometry, **values)

        def _build_group(self, tree):
            geometry = tree.inputs.geometry("Geometry")
            sockets = {
                name: getattr(tree.inputs, CLOUD[name])(name, hide_value=True)
                for name in names
            }
            capture = g.CaptureAttribute(geometry)
            items = {
                name: getattr(capture.items, CLOUD[name])(socket, name)
                for name, socket in sockets.items()
            }
            out = capture.o.geometry
            for name, item in items.items():
                store = getattr(g.StoreNamedAttribute.point, CLOUD[name])
                out = out >> store(name=name, value=item.output)
            out >> tree.outputs.geometry("Geometry")

    Write.__name__ = group_name.replace(" ", "")
    return Write


WriteSplit = writer("Write BSP Split", ["split", "axis", "m1", "m2"])
WriteChildren = writer(
    "Write BSP Children", ["a", "b", "cell", "depth", "p0", "p1", "p2", "p3"]
)


# --------------------------------------------------------------------------
# Field helpers
# --------------------------------------------------------------------------


def cross2(u, v):
    """The z component of `u x v`: the 2D cross product of two XY vectors."""
    return u.cross(v).z


def perp(v):
    """`v` turned a quarter turn counter-clockwise in the XY plane."""
    return g.CombineXYZ(-v.y, v.x).o.vector


def lerp(a, b, t):
    return a + (b - a) * t


class Groups:
    """Per-cell statistics, with neutral values for the points that don't count."""

    def __init__(self, r):
        self.r = r
        self.is_fragment = ~r.is_cell

    def min(self, mask, value):
        return mask.switch.float(BIG, value).point.min(self.r.cell)

    def max(self, mask, value):
        return mask.switch.float(-BIG, value).point.max(self.r.cell)

    def total(self, mask, value):
        return mask.switch.vector((0, 0, 0), value).point.total(self.r.cell)

    def count(self, mask):
        return mask.switch.float(0.0, 1.0).point.total(self.r.cell)

    def cell_vector(self, value):
        """A cell's own vector, on every point of the cell."""
        return self.is_fragment.switch.vector(value, (-BIG, -BIG, -BIG)).point.max(
            self.r.cell
        )


def multiple_curves(r):
    """The lowest and highest curve id crossing each cell, and whether they differ.
    Cells take no part in the statistics, so they contribute the neutral value."""
    lowest = r.is_cell.switch.integer(r.curve, 2**30).point.min(r.cell)
    highest = r.is_cell.switch.integer(r.curve, -1).point.max(r.cell)
    return lowest, highest, lowest < highest


def edge_crossing(start, end, origin, direction, margin=1e-4):
    """Where the line through `origin` along `direction` crosses the edge
    `start -> end`, as a factor along the edge, and whether it does so clear of
    the corners."""
    denom = cross2(direction, end - start)
    t = cross2(direction, origin - start) / denom
    hit = (denom.abs() > 1e-12) & (t > margin) & (t < 1 - margin)
    return t, hit


def gap_split_point(groups, a, b, start, end):
    """Paper, Section 2.1: the middle of the gap between curve crossings that
    contains the edge's midpoint, so the split line stays clear of curves."""
    d = b - a
    e = end - start
    w = start - a
    denom = cross2(d, e)
    s = cross2(w, e) / denom  # along the fragment
    t = cross2(w, d) / denom  # along the edge
    tol = 1e-5
    hit = (
        groups.is_fragment
        & (denom.abs() > 1e-12)
        & (s >= -tol)
        & (s <= 1 + tol)
        & (t >= 0.0)
        & (t <= 1.0)
    )
    below = groups.max(hit & (t <= 0.5), t).max(0.0)
    above = groups.min(hit & (t > 0.5), t).min(1.0)
    return lerp(start, end, (below + above) * 0.5)


def cell_corners(r, groups):
    """The four corners of each point's cell."""
    return [groups.cell_vector(p) for p in (r.p0, r.p1, r.p2, r.p3)]


# --------------------------------------------------------------------------
# One pass, as group nodes. Each reads the cloud itself and outputs fields,
# which are evaluated on whatever geometry the caller uses them with.
# --------------------------------------------------------------------------


class CurvesInCell(CustomGeometryGroup):
    """Which curves cross each point's cell."""

    _name = "Curves In Cell"
    _color_tag = "CONVERTER"

    def __init__(self):
        super().__init__()

    def _build_group(self, tree):
        r = ReadCloud().o
        lowest, highest, multi = multiple_curves(r)
        middle = ~r.is_cell & (r.curve != lowest) & (r.curve != highest)
        third = middle.switch.integer(0, 1).point.max(r.cell)
        lowest >> tree.outputs.integer("Lowest")
        highest >> tree.outputs.integer("Highest")
        multi >> tree.outputs.boolean("Multiple")
        (multi & (third == 0)) >> tree.outputs.boolean("Exactly Two")


class RegularSplit(CustomGeometryGroup):
    """Paper, Section 2.1: split across the cell, alternating direction by depth,
    through the middle of the gaps between curve crossings."""

    _name = "Regular Split"
    _color_tag = "CONVERTER"

    def __init__(self):
        super().__init__()

    def _build_group(self, tree):
        r = ReadCloud().o
        groups = Groups(r)
        p0, p1, p2, p3 = cell_corners(r, groups)
        depth = groups.is_fragment.switch.integer(r.depth, -1).point.max(r.cell)
        # axis 0 cuts bottom (p0 p1) and top (p3 p2), axis 1 left (p0 p3) and
        # right (p1 p2)
        axis = depth % 2
        vertical = axis == 0
        m1 = gap_split_point(groups, r.a, r.b, p0, vertical.switch.vector(p3, p1))
        m2 = gap_split_point(groups, r.a, r.b, vertical.switch.vector(p1, p3), p2)
        depth >> tree.outputs.integer("Depth")
        axis >> tree.outputs.integer("Axis")
        m1 >> tree.outputs.vector("M1")
        m2 >> tree.outputs.vector("M2")


class SeparatingCandidate(CustomGeometryGroup):
    """A line across the cell along `Normal` with the two curves on either side.

    Fragments are straight, so a curve's extent along the normal is the extent of
    its end points and the test is exact. The line runs through the middle of the
    gap, and must cross two opposite edges so both children stay quads. `Score` is
    the gap, or -1 when there is no such line.
    """

    _name = "Separating Candidate"
    _color_tag = "CONVERTER"

    def __init__(
        self,
        normal: InputVector = None,
        lowest: InputInteger = None,
        highest: InputInteger = None,
    ):
        super().__init__(normal=normal, lowest=lowest, highest=highest)

    def _build_group(self, tree):
        n = tree.inputs.vector("Normal", hide_value=True)
        lowest = tree.inputs.integer("Lowest", hide_value=True)
        highest = tree.inputs.integer("Highest", hide_value=True)
        r = ReadCloud().o
        groups = Groups(r)
        first = groups.is_fragment & (r.curve == lowest)
        second = groups.is_fragment & (r.curve == highest)

        with g.Frame("Extents along the normal"):
            a_n, b_n = n.dot(r.a), n.dot(r.b)
            low, high = a_n.min(b_n), a_n.max(b_n)
            lo1, hi1 = groups.min(first, low), groups.max(first, high)
            lo2, hi2 = groups.min(second, low), groups.max(second, high)
            ahead, behind = lo2 - hi1, lo1 - hi2
            gap = ahead.max(behind)
            offset = (ahead > behind).switch.float((hi2 + lo1) * 0.5, (hi1 + lo2) * 0.5)
            origin = n * offset
            direction = perp(n)

        with g.Frame("Opposite edges"):
            p0, p1, p2, p3 = cell_corners(r, groups)
            t_bottom, bottom = edge_crossing(p0, p1, origin, direction)
            t_top, top = edge_crossing(p3, p2, origin, direction)
            t_left, left = edge_crossing(p0, p3, origin, direction)
            t_right, right = edge_crossing(p1, p2, origin, direction)
            vertical = bottom & top
            ok = (gap > 1e-9) & (vertical | (left & right)) & (n.length() > 0.5)

        ok.switch.float(-1.0, gap) >> tree.outputs.float("Score")
        vertical.switch.integer(1, 0) >> tree.outputs.integer("Axis")
        vertical.switch.vector(
            lerp(p0, p3, t_left), lerp(p0, p1, t_bottom)
        ) >> tree.outputs.vector("M1")
        vertical.switch.vector(
            lerp(p1, p2, t_right), lerp(p3, p2, t_top)
        ) >> tree.outputs.vector("M2")


class SeparatingLine(CustomGeometryGroup):
    """Paper, Section 2.3, for cells crossed by exactly two curves: the best of three
    candidate lines, normal to each curve's chord and to the line between them."""

    _name = "Separating Line"
    _color_tag = "CONVERTER"

    def __init__(self, lowest: InputInteger = None, highest: InputInteger = None):
        super().__init__(lowest=lowest, highest=highest)

    def _build_group(self, tree):
        lowest = tree.inputs.integer("Lowest", hide_value=True)
        highest = tree.inputs.integer("Highest", hide_value=True)
        r = ReadCloud().o
        groups = Groups(r)
        first = groups.is_fragment & (r.curve == lowest)
        second = groups.is_fragment & (r.curve == highest)

        with g.Frame("Candidate normals"):
            middle = (r.a + r.b) * 0.5
            centre1 = groups.total(first, middle) / groups.count(first)
            centre2 = groups.total(second, middle) / groups.count(second)
            normals = [
                perp(groups.total(first, r.b - r.a)).normalize(),
                perp(groups.total(second, r.b - r.a)).normalize(),
                (centre2 - centre1).normalize(),
            ]

        candidates = [
            SeparatingCandidate(n, lowest=lowest, highest=highest).o for n in normals
        ]
        first_candidate = candidates[0]
        best = _Best(
            first_candidate.score,
            first_candidate.axis,
            first_candidate.m1,
            first_candidate.m2,
        )
        for candidate in candidates[1:]:
            take = candidate.score > best.score
            best = _Best(
                score=take.switch.float(best.score, candidate.score),
                axis=take.switch.integer(best.axis, candidate.axis),
                m1=take.switch.vector(best.m1, candidate.m1),
                m2=take.switch.vector(best.m2, candidate.m2),
            )

        (best.score > 0.0) >> tree.outputs.boolean("Found")
        best.axis >> tree.outputs.integer("Axis")
        best.m1 >> tree.outputs.vector("M1")
        best.m2 >> tree.outputs.vector("M2")


class _Best:
    def __init__(self, score, axis, m1, m2):
        self.score, self.axis, self.m1, self.m2 = score, axis, m1, m2


class DecideSplit(CustomGeometryGroup):
    """Choose each cell's split line and store it on all of the cell's points."""

    _name = "Decide Split"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        geometry: InputGeometry = ...,
        max_depth: InputInteger = 18,
        separating_lines: InputBoolean = True,
    ):
        super().__init__(
            geometry=geometry, max_depth=max_depth, separating_lines=separating_lines
        )

    def _build_group(self, tree):
        geometry = tree.inputs.geometry("Geometry")
        max_depth = tree.inputs.integer("Max Depth", 18, min_value=0)
        use_separating = tree.inputs.boolean("Separating Lines", True)

        curves = CurvesInCell().o
        regular = RegularSplit().o
        separating = SeparatingLine(curves.lowest, highest=curves.highest).o

        separate = use_separating & curves.exactly_two & separating.found
        split_regular = curves.multiple & (regular.depth < max_depth)

        WriteSplit(
            geometry=geometry,
            split=separate | split_regular,
            axis=separate.switch.integer(regular.axis, separating.axis),
            m1=separate.switch.vector(regular.m1, separating.m1),
            m2=separate.switch.vector(regular.m2, separating.m2),
        ) >> tree.outputs.geometry("Geometry")


class SplitCells(CustomGeometryGroup):
    """Apply the stored split: copy split cells and cut fragments, then turn the
    copies into children."""

    _name = "Split Cells"
    _color_tag = "GEOMETRY"

    def __init__(self, geometry: InputGeometry = ...):
        super().__init__(geometry=geometry)

    def _build_group(self, tree):
        geometry = tree.inputs.geometry("Geometry")
        r = ReadCloud().o

        with g.Frame("Duplicate"):
            direction = r.m2 - r.m1
            side_a = cross2(direction, r.a - r.m1)
            side_b = cross2(direction, r.b - r.m1)
            crossing = ~r.is_cell & (side_a * side_b < 0.0)
            amount = (r.split & (r.is_cell | crossing)).switch.integer(1, 2)
            dup = g.DuplicateElements.point(geometry, amount=amount)
            copy = dup.o.duplicate_index
            first_copy = copy == 0

        with g.Frame("Child corners"):
            # axis 0 gives left [p0 m1 m2 p3] / right [m1 p1 p2 m2],
            # axis 1 gives top [m1 m2 p2 p3] / bottom [p0 p1 m2 m1]
            own = [r.p0, r.p1, r.p2, r.p3]
            m1, m2 = r.m1, r.m2
            children = {
                0: ([own[0], m1, m2, own[3]], [m1, own[1], own[2], m2]),
                1: ([m1, m2, own[2], own[3]], [own[0], own[1], m2, m1]),
            }
            split_cell = r.split & r.is_cell
            vertical = r.axis == 0
            new_p = []
            for i in range(4):
                by_axis = [
                    first_copy.switch.vector(children[ax][1][i], children[ax][0][i])
                    for ax in (0, 1)
                ]
                child = vertical.switch.vector(by_axis[1], by_axis[0])
                new_p.append(split_cell.switch.vector(own[i], child))

        with g.Frame("Fragment pieces"):
            # a cut fragment's copy 0 is [a, x], copy 1 is [x, b]
            cut = r.split & crossing
            x = lerp(r.a, r.b, side_a / (side_a - side_b))
            new_a = (cut & ~first_copy).switch.vector(r.a, x)
            new_b = (cut & first_copy).switch.vector(r.b, x)
            side = cut.switch.float(
                side_a + side_b, first_copy.switch.float(side_b, side_a)
            )
            # the positive side of the line is child 0
            fragment_child = (side > 0.0).switch.integer(1, 0)
            child = r.is_cell.switch.integer(fragment_child, copy)
            child = r.split.switch.integer(0, child)

        WriteChildren(
            geometry=dup.o.geometry,
            a=new_a,
            b=new_b,
            cell=r.cell * 2 + child,
            depth=r.depth + split_cell.switch.integer(0, 1),
            p0=new_p[0],
            p1=new_p[1],
            p2=new_p[2],
            p3=new_p[3],
        ) >> tree.outputs.geometry("Geometry")


class ProjectedContours(CustomGeometryGroup):
    """Silhouette, boundary and crease edges of a mesh as curves in screen space."""

    _name = "Projected Contours"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        mesh: InputGeometry = ...,
        camera: InputObject = None,
        crease_angle: InputFloat = CREASE,
    ):
        super().__init__(mesh=mesh, camera=camera, crease_angle=crease_angle)

    def _build_group(self, tree):
        mesh = tree.inputs.geometry("Mesh")
        camera = tree.inputs.object("Camera")
        crease = tree.inputs.float(
            "Crease Angle", CREASE, subtype="ANGLE", min_value=0.0
        )

        self_matrix = g.ObjectInfo(g.SelfObject()).o.transform
        camera_matrix = g.ObjectInfo(camera).o.transform

        with g.Frame("Silhouettes"):
            eye = g.ObjectInfo(camera).o.location.transform(self_matrix.invert())
            face_center = g.Position().o.position
            facing = g.Normal().o.normal.dot(face_center - eye) < 0.0
            # face -> edge interpolation averages the two faces: 0.5 on a silhouette
            front = g.EvaluateOnDomain.face.float(facing.switch.float(0.0, 1.0))
            share = front.o.value
            silhouette = (share > 0.01) & (share < 0.99)

        with g.Frame("Boundaries and creases"):
            boundary = g.EdgeNeighbors().o.face_count == 1
            sharp = g.EdgeAngle().o.unsigned_angle > crease

        with g.Frame("Perspective divide"):
            to_camera = camera_matrix.invert() @ self_matrix
            q = g.Position().o.position.transform(to_camera)
            screen = g.CombineXYZ(q.x / -q.z, q.y / -q.z)

        (
            g.MeshToCurve.edges(mesh, selection=silhouette | boundary | sharp)
            >> g.SetPosition(position=screen)
            >> tree.outputs.geometry("Curves")
        )


class CurveFragments(CustomGeometryGroup):
    """Cut curves into pieces that cannot cross themselves, one point per segment."""

    _name = "Curve Fragments"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        curves: InputGeometry = ...,
        max_turn: InputFloat = MAX_TURN,
    ):
        super().__init__(curves=curves, max_turn=max_turn)

    def _build_group(self, tree):
        curves = tree.inputs.geometry("Curves")
        max_turn = tree.inputs.float(
            "Max Turn",
            MAX_TURN,
            subtype="ANGLE",
            min_value=0.01,
            max_value=math.pi,
            description="Total turning of a piece; below a half turn it cannot cross itself",
        )

        position = g.Position().o.position
        prev = g.OffsetPointInCurve(offset=-1)
        nxt = g.OffsetPointInCurve(offset=1)
        prev_pos = position.point.at(prev.o.point_index)
        next_pos = position.point.at(nxt.o.point_index)
        spline = g.CurveOfPoint()

        with g.Frame("Turning"):
            incoming = position - prev_pos
            outgoing = next_pos - position
            angle = cross2(incoming, outgoing).atan2(incoming.dot(outgoing)).abs()
            turn = (prev.o.is_valid_offset & nxt.o.is_valid_offset).switch.float(
                0.0, angle
            )
            total = g.AccumulateField.point.float(turn, spline.o.curve_index).o.leading
            piece = (total / max_turn).floor()

        with g.Frame("Piece ids"):
            # a new piece starts at each curve's first point and wherever the
            # running turn passes another multiple of Max Turn
            first = spline.o.index_in_curve == 0
            starts = first | (piece != piece.point.at(prev.o.point_index))
            piece_id = g.AccumulateField.point.integer(
                starts.switch.integer(0, 1)
            ).o.leading

        keep = nxt.o.is_valid_offset & ((next_pos - position).length() > 1e-9)

        (
            curves
            >> g.StoreNamedAttribute.point.vector(name="a", value=position)
            >> g.StoreNamedAttribute.point.vector(name="b", value=next_pos)
            >> g.StoreNamedAttribute.point.integer(name="curve", value=piece_id)
            # stored: Offset Point in Curve means nothing once these are points
            >> g.StoreNamedAttribute.point.boolean(name="keep", value=keep)
            >> g.CurveToPoints.evaluated()
            >> g.DeleteGeometry.point(
                selection=~g.NamedAttribute.boolean("keep").o.attribute
            )
            >> g.RemoveNamedAttribute(name="keep")
            >> tree.outputs.geometry("Fragments")
        )


class BSPCells(CustomGeometryGroup):
    """Split the plane until each cell crosses at most one curve fragment."""

    _name = "BSP Cells"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        fragments: InputGeometry = ...,
        max_depth: InputInteger = 18,
        separating_lines: InputBoolean = True,
        separating_passes: InputInteger = 6,
        padding: InputFloat = 0.05,
    ):
        super().__init__(
            fragments=fragments,
            max_depth=max_depth,
            separating_lines=separating_lines,
            separating_passes=separating_passes,
            padding=padding,
        )

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        max_depth = tree.inputs.integer(
            "Max Depth",
            18,
            min_value=0,
            max_value=24,
            description="Tree levels; cell area is the root's divided by 2^depth",
        )
        use_separating = tree.inputs.boolean(
            "Separating Lines",
            True,
            description="Split two-curve cells along a line between the curves (Section 2.3)",
        )
        extra = tree.inputs.integer(
            "Separating Passes",
            6,
            min_value=0,
            max_value=6,
            description="Passes after Max Depth in which only separating lines split",
        )
        padding = tree.inputs.float("Padding", 0.05, min_value=0.0)

        with g.Frame("Root cell"):
            bounds = g.BoundingBox(fragments, use_radius=False)
            size = bounds.o.max - bounds.o.min
            lo = bounds.o.min - size * padding
            hi = bounds.o.max + size * padding
            root = g.Points(1, position=(bounds.o.min + bounds.o.max) * 0.5)
            root = root >> g.StoreNamedAttribute.point.boolean(
                name="is_cell", value=True
            )
            corners = [(lo.x, lo.y), (hi.x, lo.y), (hi.x, hi.y), (lo.x, hi.y)]
            for k, (x, y) in enumerate(corners):
                root = root >> g.StoreNamedAttribute.point.vector(
                    name=f"p{k}", value=g.CombineXYZ(x, y)
                )

        cloud = (
            g.JoinGeometry([fragments, root])
            >> g.StoreNamedAttribute.point.integer(name="cell", value=0)
            >> g.StoreNamedAttribute.point.integer(name="depth", value=0)
        )

        zone = g.RepeatZone(max_depth + use_separating.switch.integer(0, extra))
        state = zone.items.geometry(cloud, "Cloud")
        (
            state.current
            >> DecideSplit(max_depth=max_depth, separating_lines=use_separating)
            >> SplitCells()
            >> state.next
        )

        with g.Frame("Intersection nodes"):
            multiple = CurvesInCell().o.multiple
            is_cell = g.NamedAttribute.boolean("is_cell").o.attribute
            (
                state.result
                >> g.StoreNamedAttribute.point.boolean(
                    name="is_intersection", value=multiple & is_cell
                )
                # the last pass's decision is stale once its children exist
                >> g.RemoveNamedAttribute(name="split")
                >> g.RemoveNamedAttribute(name="axis")
                >> g.RemoveNamedAttribute(name="m1")
                >> g.RemoveNamedAttribute(name="m2")
                >> tree.outputs.geometry("Cloud")
            )


class BSPDebugView(CustomGeometryGroup):
    """Cells, fragments and intersection nodes as meshes, for looking at the tree.

    Lines become thin tubes so they can carry a material; intersection nodes are
    filled. Everything stays in screen space, on the XY plane.
    """

    _name = "BSP Debug View"
    _color_tag = "GEOMETRY"

    def __init__(self, cloud: InputGeometry = ..., line_width: InputFloat = 0.0015):
        super().__init__(cloud=cloud, line_width=line_width)

    def _build_group(self, tree):
        cloud = tree.inputs.geometry("Cloud")
        width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
        r = ReadCloud().o
        is_intersection = g.NamedAttribute.boolean("is_intersection").o.attribute
        profile = g.CurveCircle(resolution=4, radius=0.5).o.curve

        def tube(curves):
            return g.CurveToMesh(curves, profile_curve=profile, scale=width)

        with g.Frame("Cell outlines"):
            cells = g.DuplicateElements.point(
                g.SeparateGeometry.point(cloud, selection=r.is_cell).o.selection,
                amount=4,
            )
            corner = cells.o.duplicate_index
            outline = (
                cells
                >> g.SetPosition(
                    position=g.IndexSwitch.vector(corner, [r.p0, r.p1, r.p2, r.p3])
                )
                >> g.PointsToCurves(curve_group_id=r.cell, weight=corner)
                >> g.SetSplineCyclic(cyclic=True)
            )
            # Points to Curves keeps point attributes; any corner will do
            hit = g.SeparateGeometry.spline(
                outline,
                selection=is_intersection.point.at(g.PointsOfCurve().o.point_index),
            ).o.selection
            tube(outline) >> tree.outputs.geometry("Cells")
            g.FillCurve(hit, mode="N-gons") >> tree.outputs.geometry("Intersections")

        with g.Frame("Fragments"):
            capture = g.CaptureAttribute(
                g.SeparateGeometry.point(cloud, selection=~r.is_cell).o.selection
            )
            index = capture.items.integer(g.Index(), "Index")
            segments = g.DuplicateElements.point(capture, amount=2)
            end = segments.o.duplicate_index
            pieces = (
                segments
                >> g.SetPosition(position=(end == 0).switch.vector(r.b, r.a))
                >> g.PointsToCurves(curve_group_id=index.output, weight=end)
            )
            tube(pieces) >> tree.outputs.geometry("Fragments")


def build(name: str = "Planar Map BSP"):
    """The modifier tree: contours of the object it sits on, split into cells.

    The debug view is placed on a plane `Overlay Distance` in front of the camera,
    where it lines up with the object in the camera's view. `Show Cloud` adds the
    raw point cloud (in screen space), which `run_suzanne.py` reads.
    """
    with g.tree(name, clear=True, is_modifier=True) as tree:
        mesh = tree.inputs.geometry("Geometry")
        camera = tree.inputs.object("Camera")
        max_depth = tree.inputs.integer("Max Depth", 18, min_value=0, max_value=24)
        separating = tree.inputs.boolean("Separating Lines", True)
        crease = tree.inputs.float(
            "Crease Angle", CREASE, subtype="ANGLE", min_value=0.0
        )
        with tree.inputs.panel("Display"):
            distance = tree.inputs.float(
                "Overlay Distance", 1.0, min_value=0.001, subtype="DISTANCE"
            )
            width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
            show_mesh = tree.inputs.boolean("Show Mesh", True)
            show_cloud = tree.inputs.boolean("Show Cloud", False)
            materials = [
                tree.inputs.material(name)
                for name in ("Cell Material", "Fragment Material", "Node Material")
            ]

        cloud = (
            ProjectedContours(mesh, camera=camera, crease_angle=crease)
            >> CurveFragments()
            >> BSPCells(max_depth=max_depth, separating_lines=separating)
        )
        view = BSPDebugView(cloud, line_width=width)

        with g.Frame("Place in front of the camera"):
            # screen (x, y) is camera-space (x, y, -1) after the divide, so
            # (x d, y d, -d) projects to the same spot for any distance d
            to_local = (
                g.ObjectInfo(g.SelfObject()).o.transform.invert()
                @ g.ObjectInfo(camera).o.transform
                @ g.CombineTransform(
                    translation=g.CombineXYZ(z=-distance),
                    scale=g.CombineXYZ(distance, distance, distance),
                ).o.transform
            )
            overlay = g.TransformGeometry(
                g.JoinGeometry(
                    [
                        g.SetMaterial(view.o.cells, material=materials[0]),
                        g.SetMaterial(view.o.fragments, material=materials[1]),
                        g.SetMaterial(view.o.intersections, material=materials[2]),
                    ]
                ),
                mode="Matrix",
                transform=to_local,
            )

        g.JoinGeometry(
            [
                g.Switch(show_mesh, None, mesh),
                overlay,
                g.Switch(show_cloud, None, cloud),
            ]
        ) >> tree.outputs.geometry("Geometry")
    return tree
