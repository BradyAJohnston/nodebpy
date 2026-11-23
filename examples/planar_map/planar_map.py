"""The modifier tree: contours of the object it sits on, the BSP, and the regions.

Everything is computed in screen space and shown on a plane `Overlay Distance` in
front of the camera, where it lines up with the object in the camera's view.
"""

from __future__ import annotations

from bsp import CREASE, BSPCells, BSPDebugView, CurveFragments, ProjectedContours
from regions import (
    Faces,
    Halfedges,
    NextHalfedge,
    OrderedFragments,
    RegionLoops,
    RegionsToGreasePencil,
    Stops,
)

from nodebpy import geometry as g


def build(name: str = "Planar Map"):
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
            show_mesh = tree.inputs.boolean("Show Mesh", True)
            show_regions = tree.inputs.boolean("Show Regions", True)
            show_bsp = tree.inputs.boolean("Show BSP", False)
            width = tree.inputs.float("Line Width", 0.0015, min_value=0.0)
            seed = tree.inputs.integer("Color Seed", 0)
            region_material = tree.inputs.material("Region Material")
            materials = [
                tree.inputs.material(name)
                for name in ("Cell Material", "Fragment Material", "Node Material")
            ]
            data = tree.inputs.menu(
                "Data",
                "None",
                description="Raw data to add to the output, for inspection",
            )

        cloud = (
            ProjectedContours(mesh, camera=camera, crease_angle=crease)
            >> CurveFragments()
            >> BSPCells(max_depth=max_depth, separating_lines=separating)
        )

        with g.Frame("Planar map"):
            fragments = OrderedFragments(cloud)
            halfedges = Stops(fragments) >> Halfedges() >> NextHalfedge() >> Faces()
            loops = RegionLoops(halfedges, fragments=fragments)
            pencil = RegionsToGreasePencil(loops, material=region_material, seed=seed)

        view = BSPDebugView(cloud, line_width=width)
        bsp_view = g.JoinGeometry(
            [
                g.SetMaterial(view.o.cells, material=materials[0]),
                g.SetMaterial(view.o.fragments, material=materials[1]),
                g.SetMaterial(view.o.intersections, material=materials[2]),
            ]
        )

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
                        g.Switch(show_regions, None, pencil),
                        g.Switch(show_bsp, None, bsp_view),
                    ]
                ),
                mode="Matrix",
                transform=to_local,
            )

        raw = g.MenuSwitch(
            data,
            {
                "None": g.JoinGeometry(),
                "BSP Cloud": cloud,
                "Halfedges": g.JoinGeometry([halfedges, loops]),
            },
        )

        g.JoinGeometry(
            [g.Switch(show_mesh, None, mesh), overlay, raw]
        ) >> tree.outputs.geometry("Geometry")
    return tree
