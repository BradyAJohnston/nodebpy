# Node-group asset 'Displace Geometry' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class DisplaceGeometry(CustomGeometryGroup):
    _name = "Displace Geometry"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
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
        evaluate_closure.inputs.float("Strength", math)
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


ASSET = DisplaceGeometry

ASSET_METADATA = {
    "description": "Displace geometry by an offset iteratively",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "463e71f0-6db1-41af-bc96-6f875196aac7",
    "catalog_simple_name": "Geometry-Operations",
}
