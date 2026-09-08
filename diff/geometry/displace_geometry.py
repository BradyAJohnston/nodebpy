# Node-group asset 'Displace Geometry' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class DisplaceGeometry(CustomGeometryGroup):
    _name = "Displace Geometry"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        geometry = tree.inputs.geometry(
            "Geometry", description="Geometry with points to displace"
        )
        selection = tree.inputs.boolean(
            "Selection",
            True,
            description="Selection of points that should be displaced",
            hide_value=True,
        )
        strength = tree.inputs.float(
            "Strength",
            1.0,
            description="Factor that the displacement is multiplied with",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
        )
        offset_method = tree.inputs.menu(
            "Offset Method",
            description="Input method for how to generate the displacement vector",
            expanded=True,
            optional_label=True,
            structure_type="SINGLE",
        )
        offset_vector = tree.inputs.vector(
            "Offset Vector",
            (0.0, 0.0, 0.0),
            description="Displacement offset vector",
            hide_value=True,
            structure_type="FIELD",
            subtype="TRANSLATION",
        )
        offset_distance = tree.inputs.float(
            "Offset Distance",
            1.0,
            description="Distance of the displacement offset in normal direction",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
            subtype="DISTANCE",
        )
        substeps = tree.inputs.integer(
            "Substeps",
            1,
            description="Number of steps to divide the full displacement into. Fields, including normal and position, are re-evaluated before each step.",
            min_value=1,
            max_value=64,
        )
        post_substep_process = tree.inputs.closure(
            "Post Substep Process",
            description="Geometry process to apply after each displacement step",
        )
        geometry_1 = tree.outputs.geometry("Geometry", description="Displaced geometry")

        with g.Frame("Normal Displacement"):
            vector_math = g.Normal().o.normal * (offset_distance * strength)
        repeat_zone = g.RepeatZone(substeps)
        geometry_2 = repeat_zone.items.geometry("Geometry", geometry)
        math = strength / substeps
        index_switch = g.IndexSwitch.vector(
            g.MenuSwitch.integer(offset_method, {"Normal": 0, "Vector": 1}),
            (vector_math, offset_vector),
        )
        set_position = g.SetPosition(
            geometry=geometry_2.current,
            selection=selection,
            offset=index_switch.o.output * math,
        )
        evaluate_closure = g.EvaluateClosure(
            post_substep_process, define_signature=True
        )
        evaluate_closure.inputs.geometry("Geometry", set_position)
        evaluate_closure.inputs.boolean("Selection", selection)
        evaluate_closure.inputs.float("Strength", g.Reroute(input=math))
        evaluate_closure.inputs.integer("Substep Index", repeat_zone.iteration)
        geometry_3 = evaluate_closure.outputs.geometry("Geometry")
        geometry_3 >> geometry_2.next
        (
            g.Warning.warning(
                substeps <= 0, "Substeps <1 means the process is not executed"
            ).o.show.switch.geometry(geometry_2.result, geometry)
            >> geometry_1
        )

        offset_method.default_value = "Normal"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (1879.7, 193.2),
            "Group Input": (220.0, 280.0),
            "Set Position": (640.0, 180.0),
            "Repeat Input": (440.0, 340.0),
            "Repeat Output": (1040.0, 180.0),
            "Vector Math": (440.0, 60.0),
            "Math": (220.0, -80.0),
            "Vector Math.001": (389.6, -55.7),
            "Normal": (209.6, -35.7),
            "Frame": (-429.6, 235.7),
            "Group Input.003": (29.6, -95.7),
            "Math.002": (209.6, -95.7),
            "Group Input.004": (220.0, 340.0),
            "Group Input.005": (440.0, 140.0),
            "Group Input.006": (40.0, -100.0),
            "Group Input.010": (-20.0, -20.0),
            "Evaluate Closure": (840.0, 240.0),
            "Group Input.011": (640.0, 260.0),
            "Reroute": (700.0, -120.0),
            "Group Input.001": (29.6, -155.7),
            "Menu Switch": (-40.0, 300.0),
            "Index Switch": (220.0, 180.0),
            "Group Input.002": (-240.0, 340.0),
            "Warning": (1500.0, 280.0),
            "Compare": (1328.2, 285.2),
            "Switch": (1687.9, 227.3),
            "Group Input.007": (1164.0, 282.5),
            "Group Input.008": (1477.9, 129.8),
        }


ASSET = DisplaceGeometry

ASSET_METADATA = {
    "description": "Displace geometry by an offset iteratively",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "463e71f0-6db1-41af-bc96-6f875196aac7",
    "catalog_simple_name": "Geometry-Operations",
}
