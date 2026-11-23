"""Stage 2 of "Robust Planar Maps for 3D Vectorization": the planar map (Section 3).

Turns the BSP cloud from `bsp.py` into a halfedge mesh whose faces are the regions:

- `OrderedFragments`: the curve fragments in curve order, each knowing whether its
  cell is an intersection node and where its end points sit on the cell's boundary.
- `Stops`: the vertices each curve meets, in curve order. A run of fragments in one
  intersection node is a visit to that node's vertex; a curve end in a plain cell
  is a dangling vertex of its own. Consecutive stops on a curve are one logical edge.
- `Halfedges`: two per logical edge, each with its origin vertex and where it leaves
  the origin's node, as a position along the node's boundary (Section 3.3).
- `NextHalfedge`: orders the halfedges leaving each vertex by that position,
  counter-clockwise, and links each halfedge to the next one around its face.
- `Faces`: pointer jumping in a repeat zone. Every orbit of `next` takes its lowest
  halfedge index as its face id, and each halfedge learns its rank in the orbit.
- `RegionLoops`: one closed curve per face, made of the edges' fragments, with a
  straight step across each intersection node between consecutive edges
  (Section 3.4).

Faces are orbits: a bounded region is a counter-clockwise loop, and the outline of
each connected piece of the map is a clockwise loop (the hole it makes in whatever
region surrounds it, or the outside of everything).
"""

from __future__ import annotations

from bsp import Groups, ReadCloud, cell_corners, lerp, perp

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputGeometry, InputInteger, InputMaterial


def attr(kind: str, name: str):
    return getattr(g.NamedAttribute, kind)(name).o.attribute


def store(geometry, values: dict):
    """Capture every value on `geometry`, then store them all as named attributes."""
    capture = g.CaptureAttribute(geometry)
    items = {
        name: getattr(capture.items, kind)(value, name)
        for name, (kind, value) in values.items()
    }
    out = capture.o.geometry
    for name, item in items.items():
        kind = values[name][0]
        out = out >> getattr(g.StoreNamedAttribute.point, kind)(
            name=name, value=item.output
        )
    return out


def at(value, index):
    return value.point.at(index)


def perimeter(x, corners):
    """Where `x` sits on the boundary of the quad `corners` (counter-clockwise), as
    side index plus the fraction along that side: 0 <= value < 4."""
    best_distance = best_param = None
    for k in range(4):
        start, end = corners[k], corners[(k + 1) % 4]
        side = end - start
        t = ((x - start).dot(side) / side.dot(side)).clamp(0.0, 1.0)
        distance = (x - lerp(start, end, t)).length()
        param = t + k
        if best_distance is None:
            best_distance, best_param = distance, param
            continue
        closer = distance < best_distance
        best_distance = closer.switch.float(best_distance, distance)
        best_param = closer.switch.float(best_param, param)
    return best_param


class OrderedFragments(CustomGeometryGroup):
    """The fragments of the BSP cloud in curve order, with `in_node`, `pa`, `pb`."""

    _name = "Ordered Fragments"
    _color_tag = "GEOMETRY"

    def __init__(self, cloud: InputGeometry = ...):
        super().__init__(cloud=cloud)

    def _build_group(self, tree):
        cloud = tree.inputs.geometry("Cloud")
        r = ReadCloud().o
        groups = Groups(r)
        is_intersection = attr("boolean", "is_intersection")
        in_node = (r.is_cell & is_intersection).switch.integer(0, 1).point.max(
            r.cell
        ) > 0
        corners = cell_corners(r, groups)
        (
            store(
                cloud,
                {
                    "in_node": ("boolean", in_node),
                    "pa": ("float", perimeter(r.a, corners)),
                    "pb": ("float", perimeter(r.b, corners)),
                    # the cell's diagonal, a local length scale
                    "size": ("float", (corners[2] - corners[0]).length()),
                },
            )
            >> g.SeparateGeometry.point(selection=~r.is_cell)
            # segments are numbered along their curves, so (segment, fraction)
            # is curve order
            >> g.SortElements.point(group_id=r.seg, sort_weight=r.fa)
            >> tree.outputs.geometry("Fragments")
        )


class Stops(CustomGeometryGroup):
    """Each curve's vertices in curve order, and the edge that leaves each one."""

    _name = "Stops"
    _color_tag = "GEOMETRY"

    def __init__(self, fragments: InputGeometry = ...):
        super().__init__(fragments=fragments)

    def _build_group(self, tree):
        fragments = tree.inputs.geometry("Fragments")
        idx = g.Index().o.index
        count = g.DomainSize(fragments, component="POINTCLOUD").o.point_count
        curve, cell = attr("integer", "curve"), attr("integer", "cell")
        a, b = attr("vector", "a"), attr("vector", "b")
        pa, pb = attr("float", "pa"), attr("float", "pb")
        in_node = attr("boolean", "in_node")

        with g.Frame("Runs through nodes"):
            prev_same = (idx > 0) & (at(curve, idx - 1) == curve)
            next_same = (idx + 1 < count) & (at(curve, idx + 1) == curve)
            continues = prev_same & at(in_node, idx - 1) & (at(cell, idx - 1) == cell)
            run_start = in_node & ~continues
            run = g.AccumulateField.point.integer(
                run_start.switch.integer(0, 1)
            ).o.leading
            run_last = in_node.switch.integer(-1, idx).point.max(run)
            dangling_start = ~prev_same & ~in_node
            dangling_end = ~next_same & ~in_node

        with g.Frame("One point per stop"):
            capture = g.CaptureAttribute(fragments)
            c = {
                name: getattr(capture.items, kind)(value, name).output
                for name, (kind, value) in {
                    "f": ("integer", idx),
                    "run_last": ("integer", run_last),
                    "visit": ("boolean", run_start),
                    "start": ("boolean", dangling_start),
                    "end": ("boolean", dangling_end),
                    "exit_last": ("vector", at(b, run_last)),
                    "exit_param": ("float", at(pb, run_last)),
                }.items()
            }
            # a fragment can be a visit, or start and/or end a curve in a plain cell
            amount = (
                c["visit"].switch.integer(0, 1)
                + c["start"].switch.integer(0, 1)
                + c["end"].switch.integer(0, 1)
            )
            dup = g.DuplicateElements.point(capture.o.geometry, amount=amount)
            k = dup.o.duplicate_index
            visit = c["visit"]
            is_start = ~visit & c["start"] & (k == 0)
            is_end = ~visit & ~is_start
            f = c["f"]
            key = f * 2 + is_end.switch.integer(0, 1)
            entry = is_end.switch.vector(a, b)
            stops = store(
                dup.o.geometry,
                {
                    "key": ("integer", key),
                    "vertex": ("integer", visit.switch.integer(-(key + 1), cell)),
                    "entry": ("vector", entry),
                    "entry_param": ("float", visit.switch.float(0.0, pa)),
                    "exit": ("vector", visit.switch.vector(entry, c["exit_last"])),
                    "exit_param": ("float", visit.switch.float(0.0, c["exit_param"])),
                    # the plain fragments after this stop start at `after`; those
                    # before it end (exclusive) at `before`
                    "after": (
                        "integer",
                        visit.switch.integer(
                            is_start.switch.integer(f + 1, f), c["run_last"] + 1
                        ),
                    ),
                    "before": ("integer", is_end.switch.integer(f, f + 1)),
                },
            ) >> g.SortElements.point(sort_weight=attr("integer", "key"))

        with g.Frame("Edges"):
            j = g.Index().o.index
            stop_count = g.DomainSize(stops, component="POINTCLOUD").o.point_count
            follows = (j + 1 < stop_count) & (at(curve, j + 1) == curve)
            after = attr("integer", "after")
            count = at(attr("integer", "before"), j + 1) - after
            vertex = attr("integer", "vertex")
            dest = at(vertex, j + 1)

        with g.Frame("Drop parallel edges between adjacent nodes (3.3)"):
            # edges with no plain fragment step straight from one node into a
            # neighbour; several such between the same pair only make empty
            # two-sided faces, so the first one per pair stays
            direct = follows & (count == 0)
            low, high = vertex.min(dest), vertex.max(dest)
            pair = direct.switch.integer(-1, low.hash(high))
            first = direct.switch.integer(2**30, j).point.min(pair)
            same_pair = (at(low, first) == low) & (at(high, first) == high)
            duplicate = direct & (j != first) & same_pair
            has_edge = follows & ~duplicate
            edge = (
                g.AccumulateField.point.integer(has_edge.switch.integer(0, 1)).o.leading
                - 1
            )
            store(
                stops,
                {
                    "has_edge": ("boolean", has_edge),
                    "edge": ("integer", edge),
                    "dest_vertex": ("integer", dest),
                    "dest_entry": ("vector", at(attr("vector", "entry"), j + 1)),
                    "dest_param": ("float", at(attr("float", "entry_param"), j + 1)),
                    "count": ("integer", count),
                },
            ) >> tree.outputs.geometry("Stops")


class Halfedges(CustomGeometryGroup):
    """Two halfedges per edge: `hid = 2 * edge + direction`, in `hid` order."""

    _name = "Halfedges"
    _color_tag = "GEOMETRY"

    def __init__(self, stops: InputGeometry = ...):
        super().__init__(stops=stops)

    def _build_group(self, tree):
        stops = tree.inputs.geometry("Stops")
        edges = g.SeparateGeometry.point(
            stops, selection=attr("boolean", "has_edge")
        ).o.selection
        dup = g.DuplicateElements.point(edges, amount=2)
        back = dup.o.duplicate_index == 1
        (
            store(
                dup.o.geometry,
                {
                    "hid": (
                        "integer",
                        attr("integer", "edge") * 2 + dup.o.duplicate_index,
                    ),
                    "back": ("boolean", back),
                    "vertex": (
                        "integer",
                        back.switch.integer(
                            attr("integer", "vertex"), attr("integer", "dest_vertex")
                        ),
                    ),
                    "param": (
                        "float",
                        back.switch.float(
                            attr("float", "exit_param"), attr("float", "dest_param")
                        ),
                    ),
                    "origin": (
                        "vector",
                        back.switch.vector(
                            attr("vector", "exit"), attr("vector", "dest_entry")
                        ),
                    ),
                },
            )
            >> g.SortElements.point(sort_weight=attr("integer", "hid"))
            >> tree.outputs.geometry("Halfedges")
        )


class NextHalfedge(CustomGeometryGroup):
    """Link each halfedge to the next one around the face on its left.

    The halfedges leaving a vertex are sorted by where they cross the node's
    boundary, counter-clockwise. Arriving along `h`, the face on the left continues
    along the halfedge just before `twin(h)` in that order.
    """

    _name = "Next Halfedge"
    _color_tag = "GEOMETRY"

    def __init__(self, halfedges: InputGeometry = ...):
        super().__init__(halfedges=halfedges)

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        hid = attr("integer", "hid")
        vertex = attr("integer", "vertex")
        around = g.SortElements.point(
            halfedges, group_id=vertex, sort_weight=attr("float", "param")
        )
        idx = g.Index().o.index
        counter = g.AccumulateField.point.integer(1, vertex)
        position = counter.o.trailing
        size = counter.o.total
        before = (position - 1 + size) % size
        cw = at(hid, idx - position + before)
        ordered = store(around, {"cw": ("integer", cw)}) >> g.SortElements.point(
            sort_weight=hid
        )
        twin = hid + 1 - (hid % 2) * 2
        store(ordered, {"next": ("integer", at(attr("integer", "cw"), twin))}) >> (
            tree.outputs.geometry("Halfedges")
        )


def jump_zone(geometry, init: dict, step, iterations):
    """Run `step` `iterations` times in a repeat zone, storing what it returns."""
    zone = g.RepeatZone(iterations)
    state = zone.items.geometry(store(geometry, init), "Halfedges")
    store(state.current, step()) >> state.next
    return state.result


class Faces(CustomGeometryGroup):
    """Face id (lowest `hid` in the orbit of `next`) and rank within the face."""

    _name = "Faces"
    _color_tag = "GEOMETRY"

    def __init__(self, halfedges: InputGeometry = ...):
        super().__init__(halfedges=halfedges)

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        count = g.DomainSize(halfedges, component="POINTCLOUD").o.point_count
        # each pass doubles the stretch of the orbit a halfedge has seen
        passes = (count.to_float() + 1.0).log(2.0).ceil() + 1
        hid, nxt = attr("integer", "hid"), attr("integer", "next")
        jump = attr("integer", "jump")

        with g.Frame("Face: lowest hid in the orbit"):
            low = attr("integer", "face")
            faced = jump_zone(
                halfedges,
                {"jump": ("integer", nxt), "face": ("integer", hid)},
                lambda: {
                    "jump": ("integer", at(jump, jump)),
                    "face": ("integer", low.min(at(low, jump))),
                },
                passes,
            )

        with g.Frame("Rank: steps from the face's first halfedge"):
            first = hid == attr("integer", "face")
            dist = attr("integer", "dist")
            ranked = jump_zone(
                faced,
                {
                    "jump": ("integer", first.switch.integer(nxt, hid)),
                    "dist": ("integer", first.switch.integer(1, 0)),
                },
                lambda: {
                    "jump": ("integer", at(jump, jump)),
                    "dist": ("integer", dist + at(dist, jump)),
                },
                passes,
            )
            face = attr("integer", "face")
            length = dist.point.max(face) + 1
            (
                store(ranked, {"rank": ("integer", (length - dist) % length)})
                >> g.RemoveNamedAttribute(name="jump")
                >> tree.outputs.geometry("Halfedges")
            )


class RegionLoops(CustomGeometryGroup):
    """One closed curve per face: each halfedge's fragments in face order.

    A halfedge contributes its origin point, then the far end of each of its edge's
    fragments in its own direction. Consecutive halfedges meet inside a node, where
    the curve steps straight from one to the next.
    """

    _name = "Region Loops"
    _color_tag = "GEOMETRY"

    def __init__(self, halfedges: InputGeometry = ..., fragments: InputGeometry = None):
        super().__init__(halfedges=halfedges, fragments=fragments)

    def _build_group(self, tree):
        halfedges = tree.inputs.geometry("Halfedges")
        fragments = tree.inputs.geometry("Fragments")
        face, rank = attr("integer", "face"), attr("integer", "rank")
        n = attr("integer", "count")

        with g.Frame("Offsets within each face"):
            in_order = g.SortElements.point(halfedges, group_id=face, sort_weight=rank)
            offset = g.AccumulateField.point.integer(n + 1, face).o.trailing
            placed = store(in_order, {"offset": ("integer", offset)})

        with g.Frame("Points"):
            dup = g.DuplicateElements.point(placed, amount=n + 1)
            k = dup.o.duplicate_index
            back = attr("boolean", "back")
            first = attr("integer", "after")
            fragment = back.switch.integer(first + k - 1, first + n - k)
            # Sample Index evaluates its value on the fragments, so sample both
            # ends and choose here, where `back` means something
            ends = [
                g.SampleIndex.point.vector(
                    fragments, value=attr("vector", name), index=fragment
                ).o.value
                for name in ("a", "b")
            ]
            end = back.switch.vector(ends[1], ends[0])
            position = (k == 0).switch.vector(end, attr("vector", "origin"))
            weight = attr("integer", "offset") + k

        loops = (
            dup.o.geometry
            >> g.SetPosition(position=position)
            >> g.PointsToCurves(curve_group_id=face, weight=weight.to_float())
            >> g.SetSplineCyclic(cyclic=True)
        )

        with g.Frame("Signed area"):
            p = g.Position().o.position
            nxt = g.OffsetPointInCurve(offset=1).o.point_index
            twice = p.cross(at(p, nxt)).z.point.total(g.CurveOfPoint().o.curve_index)
            (
                loops
                >> g.StoreNamedAttribute.spline.float(name="area", value=twice * 0.5)
                >> tree.outputs.geometry("Loops")
            )


def region_stack(loops, values: dict):
    """Every bounded (counter-clockwise) loop filled and stacked by area, smallest
    on top, carrying `values` ({name: (kind, field)}) on its faces. A ray cast
    straight down onto it hits the smallest region containing the point first.

    Fill Curve drops curve attributes, so each loop is filled on its own.
    """
    area = attr("float", "area")
    zone = g.ForEachGeometryElementZone.curve(loops, selection=area > 0.0)
    area_item = zone.items.float(area, "Area")
    items = {
        name: getattr(zone.items, kind)(value, name)
        for name, (kind, value) in values.items()
    }
    stamped = g.FillCurve(zone.element, mode="Triangles")
    for name, item in items.items():
        store_face = getattr(g.StoreNamedAttribute.face, values[name][0])
        stamped = stamped >> store_face(name=name, value=item.output)
    stamped = stamped >> g.SetPosition(offset=g.CombineXYZ(z=-area_item.output))
    return zone.generated_items.geometry(stamped, "Fill").output


def look_down(stack, kind: str, name: str, point):
    """Cast down onto a region stack from above `point`."""
    return getattr(g.Raycast, kind)(
        target_geometry=stack,
        attribute=attr(kind, name),
        interpolation="Nearest",
        source_position=point + g.CombineXYZ(z=10.0).o.vector,
        ray_direction=(0.0, 0.0, -1.0),
        ray_length=100.0,
    ).o


class RegionFills(CustomGeometryGroup):
    """Regions as curves ready for Grease Pencil fills, one fill per region.

    A bounded region is a counter-clockwise loop. A connected piece of the map
    lying inside a region (an eye inside the head) has a clockwise outline; that
    outline joins the surrounding region's fill as a hole (Section 4.4.1), so each
    region is filled exactly once and nothing relies on draw order. The
    surrounding region is the smallest one containing a point just outside the
    outline: every bounded loop is filled and stacked by area, smallest on top,
    and a ray cast down from above that point hits it first.

    Edges are drawn by the line layers, so fills have no stroke of their own.
    """

    _name = "Region Fills"
    _color_tag = "GEOMETRY"

    def __init__(self, loops: InputGeometry = ..., seed: InputInteger = 0):
        super().__init__(loops=loops, seed=seed)

    def _build_group(self, tree):
        loops = tree.inputs.geometry("Loops")
        seed = tree.inputs.integer("Seed", 0)
        area = attr("float", "area")
        face = attr("integer", "face")
        seen = attr("boolean", "seen")
        bounded = area > 0.0

        with g.Frame("Bounded regions, filled and stacked by area"):
            stack = region_stack(
                loops,
                {
                    "face": ("integer", face),
                    "seen": ("integer", seen.switch.integer(0, 1)),
                },
            )

        with g.Frame("What surrounds each outline"):
            p = g.Position().o.position
            q = at(p, g.OffsetPointInCurve(offset=1).o.point_index)
            spline = g.CurveOfPoint().o.curve_index
            length = (q - p).length()
            pick = length == length.point.max(spline)
            # outlines run clockwise, so their left is outside the piece
            outside = (p + q) * 0.5 + perp((q - p).normalize()) * (length * 0.01)

            def down(name):
                return look_down(stack, "integer", name, outside)

            hit = down("face")
            found = pick & hit.is_hit
            container = found.switch.integer(-1, hit.attribute).point.max(spline)
            container_seen = found.switch.integer(0, down("seen").attribute)
            container_seen = container_seen.point.max(spline) > 0
            container_area = found.switch.float(-1.0, -hit.hit_position.z)
            container_area = container_area.point.max(spline)

        with g.Frame("Colour"):
            patch = attr("integer", "patch")
            shade = attr("float", "shade")
            # coloured by the patch they show, shaded by its normal
            base = g.RandomValue.vector(min=0.35, max=0.95, id=patch, seed=seed).o.value
            color = base * (shade * 0.6 + 0.4)

        hole = ~bounded & (container >= 0) & container_seen
        keep = (bounded & seen) | hole
        (
            g.SeparateGeometry.spline(
                loops
                # per stroke: Grease Pencil reads fill_id on the curve domain
                >> g.StoreNamedAttribute.spline.boolean(name="hole", value=hole)
                >> g.StoreNamedAttribute.spline.integer(
                    name="fill_id",
                    value=bounded.switch.integer(container + 1, face + 1),
                )
                >> g.StoreNamedAttribute.spline.float(
                    name="group_area",
                    value=bounded.switch.float(container_area, area),
                ),
                selection=keep,
            ).o.selection
            # regions first, largest first; holes after. A fill's colour comes
            # from its first stroke, which is then always the region itself
            >> g.SortElements.spline(
                group_id=attr("boolean", "hole").switch.integer(0, 1),
                sort_weight=-attr("float", "group_area"),
            )
            >> g.StoreNamedAttribute.spline.color(name="fill_color", value=color)
            >> g.StoreNamedAttribute.point.float(name="opacity", value=0.0)
            >> tree.outputs.geometry("Curves")
        )


class ToGreasePencil(CustomGeometryGroup):
    """Curves to Grease Pencil, one layer per input, named, bottom to top."""

    _name = "To Grease Pencil"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        fills: InputGeometry = None,
        lines: InputGeometry = None,
        hidden: InputGeometry = None,
        material: InputMaterial = None,
    ):
        super().__init__(fills=fills, lines=lines, hidden=hidden, material=material)

    def _build_group(self, tree):
        layers = [
            g.SetGeometryName(tree.inputs.geometry(name), name=name)
            for name in ("Fills", "Lines", "Hidden")
        ]
        material = tree.inputs.material("Material")
        (
            g.GeometryToInstance(*layers)
            # each instance's geometry name becomes its layer's name
            >> g.CurvesToGreasePencil(instances_as_layers=True)
            >> g.SetMaterial(material=material)
            >> tree.outputs.geometry("Grease Pencil")
        )
