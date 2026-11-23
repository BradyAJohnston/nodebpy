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
- `BSPCells`: the partition itself, as a repeat zone with one tree level per pass.

Cells and fragments live in one point cloud. Every point has a `cell` attribute: the
cell's path through the tree (`2 * parent + child`), which a fragment shares with
the cell it lies in. Grouping fields by `cell` then gives each cell what it needs
from its fragments (and each fragment what it needs from its cell) without index
lookups. Min and max are the only statistics used, so the duplicates a split makes
never change a group's result.
"""

from __future__ import annotations

import math

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry, InputInteger, InputObject

BIG = 1.0e9
CREASE = math.radians(60)
MAX_TURN = math.radians(160)


# --------------------------------------------------------------------------
# Field helpers. Each returns sockets; they read the attributes of whatever
# geometry the field is evaluated on.
# --------------------------------------------------------------------------


def attr_vector(name: str):
    return g.NamedAttribute.vector(name).o.attribute


def attr_int(name: str):
    return g.NamedAttribute.integer(name).o.attribute


def attr_bool(name: str):
    return g.NamedAttribute.boolean(name).o.attribute


def cross2(u, v):
    """The z component of `u x v`: the 2D cross product of two XY vectors."""
    return u.cross(v).z


def lerp(a, b, t):
    return a + (b - a) * t


def multiple_curves(is_cell, curve, cell):
    """Whether more than one curve piece crosses the cell. Cells take no part in
    the statistics, so they contribute the neutral value."""
    lowest = is_cell.switch.integer(curve, 2**30).point.min(cell)
    highest = is_cell.switch.integer(curve, -1).point.max(cell)
    return lowest < highest


class CellFields:
    """The fields one splitting pass reads, for the current state of the cloud.

    Built once per pass and evaluated both before the points are duplicated (for
    the duplicate amount) and after (for the new attributes). Grouped min/max
    ignore duplicates, so the two evaluations agree.
    """

    def __init__(self, axis):
        self.is_cell = attr_bool("is_cell")
        self.is_fragment = ~self.is_cell
        self.cell = attr_int("cell")
        self.curve = attr_int("curve")
        self.a = attr_vector("a")
        self.b = attr_vector("b")

        with g.Frame("Curves in cell"):
            self.split = multiple_curves(self.is_cell, self.curve, self.cell)

        with g.Frame("Cell corners"):
            # broadcast the cell's corners to every fragment in it
            self.p = [
                self.is_fragment.switch.vector(
                    attr_vector(f"p{k}"), (-BIG, -BIG, -BIG)
                ).point.max(self.cell)
                for k in range(4)
            ]
            p0, p1, p2, p3 = self.p
            # axis 0 cuts across the bottom (p0 -> p1) and top (p3 -> p2) edges,
            # axis 1 across the left (p0 -> p3) and right (p1 -> p2) edges
            vertical = axis == 0
            self.e1 = (p0, vertical.switch.vector(p3, p1))
            self.e2 = (vertical.switch.vector(p1, p3), p2)

        with g.Frame("Split points"):
            self.m1 = self._split_point(*self.e1)
            self.m2 = self._split_point(*self.e2)

        with g.Frame("Fragment sides"):
            direction = self.m2 - self.m1
            self.side_a = cross2(direction, self.a - self.m1)
            self.side_b = cross2(direction, self.b - self.m1)
            self.crossing = self.is_fragment & (self.side_a * self.side_b < 0.0)
            t = self.side_a / (self.side_a - self.side_b)
            self.x = lerp(self.a, self.b, t)

    def _split_point(self, start, end):
        """Paper, Section 2.1: the middle of the gap between curve crossings that
        contains the edge's midpoint, so the split line stays clear of curves."""
        d = self.b - self.a
        e = end - start
        w = start - self.a
        denom = cross2(d, e)
        s = cross2(w, e) / denom  # along the fragment
        t = cross2(w, d) / denom  # along the edge
        tol = 1e-5
        hit = (
            self.is_fragment
            & (denom.abs() > 1e-12)
            & (s >= -tol)
            & (s <= 1 + tol)
            & (t >= 0.0)
            & (t <= 1.0)
        )
        below = (hit & (t <= 0.5)).switch.float(0.0, t).point.max(self.cell)
        above = (hit & (t > 0.5)).switch.float(1.0, t).point.min(self.cell)
        return lerp(start, end, (below + above) * 0.5)


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
            >> g.DeleteGeometry.point(selection=~attr_bool("keep"))
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
        padding: InputFloat = 0.05,
    ):
        super().__init__(fragments=fragments, max_depth=max_depth, padding=padding)

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        max_depth = tree.inputs.integer(
            "Max Depth",
            18,
            min_value=0,
            max_value=28,
            description="Tree levels; cell area is the root's divided by 2^depth",
        )
        padding = tree.inputs.float("Padding", 0.05, min_value=0.0)

        with g.Frame("Root cell"):
            bounds = g.BoundingBox(fragments, use_radius=False)
            size = bounds.o.max - bounds.o.min
            lo = bounds.o.min - size * padding
            hi = bounds.o.max + size * padding
            corners = [
                (lo.x, lo.y, 0.0),
                (hi.x, lo.y, 0.0),
                (hi.x, hi.y, 0.0),
                (lo.x, hi.y, 0.0),
            ]
            root = g.Points(1, position=(bounds.o.min + bounds.o.max) * 0.5)
            root = root >> g.StoreNamedAttribute.point.boolean(
                name="is_cell", value=True
            )
            for k, corner in enumerate(corners):
                root = root >> g.StoreNamedAttribute.point.vector(
                    name=f"p{k}", value=corner
                )

        cloud = (
            g.JoinGeometry([fragments, root])
            >> g.StoreNamedAttribute.point.integer(name="cell", value=0)
            >> g.StoreNamedAttribute.point.integer(name="depth", value=0)
        )

        zone = g.RepeatZone(max_depth)
        state = zone.items.geometry(cloud, "Cloud")

        with g.Frame("Split pass"):
            axis = zone.iteration % 2
            f = CellFields(axis)
            amount = (f.split & (f.is_cell | f.crossing)).switch.integer(1, 2)
            dup = g.DuplicateElements.point(state.current, amount=amount)
            k = dup.o.duplicate_index

            with g.Frame("Children"):
                p0, p1, p2, p3 = f.p
                m1, m2 = f.m1, f.m2
                first = k == 0
                vertical = axis == 0
                # axis 0: left [p0 m1 m2 p3] / right [m1 p1 p2 m2]
                # axis 1: top [m1 m2 p2 p3] / bottom [p0 p1 m2 m1]
                children = {
                    True: ([p0, m1, m2, p3], [m1, p1, p2, m2]),
                    False: ([m1, m2, p2, p3], [p0, p1, m2, m1]),
                }
                child_corners = [
                    vertical.switch.vector(
                        first.switch.vector(
                            children[False][1][i], children[False][0][i]
                        ),
                        first.switch.vector(children[True][1][i], children[True][0][i]),
                    )
                    for i in range(4)
                ]
                cell_split = f.split & f.is_cell
                new_p = [
                    cell_split.switch.vector(attr_vector(f"p{i}"), c)
                    for i, c in enumerate(child_corners)
                ]

            with g.Frame("Fragment pieces"):
                # a crossing fragment's copy 0 is [a, x] and copy 1 is [x, b]
                piece_split = f.split & f.crossing
                new_a = (piece_split & ~first).switch.vector(f.a, f.x)
                new_b = (piece_split & first).switch.vector(f.b, f.x)
                side = piece_split.switch.float(
                    f.side_a + f.side_b, first.switch.float(f.side_b, f.side_a)
                )
                # the positive side of the line is child 0
                fragment_child = (side > 0.0).switch.integer(1, 0)
                child = f.is_cell.switch.integer(fragment_child, k)
                child = f.split.switch.integer(0, child)
                new_cell = f.cell * 2 + child
                new_depth = attr_int("depth") + f.split.switch.integer(0, 1)

            # evaluate every new value on the same state, then write them all
            capture = g.CaptureAttribute(dup.o.geometry)
            items = {
                "a": capture.items.vector(new_a, "a"),
                "b": capture.items.vector(new_b, "b"),
                "cell": capture.items.integer(new_cell, "cell"),
                "depth": capture.items.integer(new_depth, "depth"),
            }
            for i, value in enumerate(new_p):
                items[f"p{i}"] = capture.items.vector(value, f"p{i}")

            geo = capture.o.geometry
            for name, item in items.items():
                store = (
                    g.StoreNamedAttribute.point.integer
                    if name in ("cell", "depth")
                    else g.StoreNamedAttribute.point.vector
                )
                geo = geo >> store(name=name, value=item.output)
            geo >> state.next

        with g.Frame("Intersection nodes"):
            is_cell = attr_bool("is_cell")
            (
                state.result
                >> g.StoreNamedAttribute.point.boolean(
                    name="is_intersection",
                    value=multiple_curves(is_cell, attr_int("curve"), attr_int("cell"))
                    & is_cell,
                )
                >> tree.outputs.geometry("Cloud")
            )


class BSPDebugView(CustomGeometryGroup):
    """Cells, fragments and intersection nodes as meshes, for looking at the tree.

    Lines become thin ribbons so they can carry a material; intersection nodes are
    filled. Everything stays in screen space, on the XY plane.
    """

    _name = "BSP Debug View"
    _color_tag = "GEOMETRY"

    def __init__(self, cloud: InputGeometry = ..., line_width: InputFloat = 0.0015):
        super().__init__(cloud=cloud, line_width=line_width)

    def _build_group(self, tree):
        cloud = tree.inputs.geometry("Cloud")
        width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
        is_cell = attr_bool("is_cell")
        profile = g.CurveCircle(resolution=4, radius=0.5).o.curve

        def ribbon(curves):
            return g.CurveToMesh(curves, profile_curve=profile, scale=width)

        with g.Frame("Cell outlines"):
            cells = g.DuplicateElements.point(
                g.SeparateGeometry.point(cloud, selection=is_cell).o.selection,
                amount=4,
            )
            corner = cells.o.duplicate_index
            outline = (
                cells
                >> g.SetPosition(
                    position=g.IndexSwitch.vector(
                        corner, [attr_vector(f"p{k}") for k in range(4)]
                    )
                )
                >> g.PointsToCurves(curve_group_id=attr_int("cell"), weight=corner)
                >> g.SetSplineCyclic(cyclic=True)
            )
            # Points to Curves keeps point attributes; any corner will do
            hit = g.SeparateGeometry.spline(
                outline,
                selection=attr_bool("is_intersection").point.at(
                    g.PointsOfCurve().o.point_index
                ),
            ).o.selection
            ribbon(outline) >> tree.outputs.geometry("Cells")
            g.FillCurve(hit, mode="N-gons") >> tree.outputs.geometry("Intersections")

        with g.Frame("Fragments"):
            capture = g.CaptureAttribute(
                g.SeparateGeometry.point(cloud, selection=~is_cell).o.selection
            )
            index = capture.items.integer(g.Index(), "Index")
            segments = g.DuplicateElements.point(capture, amount=2)
            end = segments.o.duplicate_index
            pieces = (
                segments
                >> g.SetPosition(
                    position=(end == 0).switch.vector(
                        attr_vector("b"), attr_vector("a")
                    )
                )
                >> g.PointsToCurves(curve_group_id=index.output, weight=end)
            )
            ribbon(pieces) >> tree.outputs.geometry("Fragments")


def build(name: str = "Planar Map BSP"):
    """The modifier tree: contours of the object it sits on, split into cells.

    The debug view is placed on a plane `Overlay Distance` in front of the camera,
    where it lines up with the object in the camera's view. `Show Cloud` adds the
    raw point cloud (in screen space), which `run_suzanne.py` reads.
    """
    with g.tree(name, clear=True, is_modifier=True) as tree:
        mesh = tree.inputs.geometry("Geometry")
        camera = tree.inputs.object("Camera")
        max_depth = tree.inputs.integer("Max Depth", 18, min_value=0, max_value=28)
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
            >> BSPCells(max_depth=max_depth)
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
