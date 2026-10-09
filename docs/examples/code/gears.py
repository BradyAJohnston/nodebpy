from math import cos, pi, sin, tau

from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputInteger


class Gear(CustomGeometryGroup):
    """A spur gear with trapezoidal teeth, sized by its tooth count and module."""

    _name = "Gear"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        teeth: InputInteger = 16,
        module: InputFloat = 0.1,
        thickness: InputFloat = 0.2,
        rotation: InputFloat = 0.0,
    ):
        super().__init__(
            teeth=teeth, module=module, thickness=thickness, rotation=rotation
        )

    def _build_group(self, tree):
        teeth = tree.inputs.integer("Teeth", 16, min_value=4)
        module = tree.inputs.float("Module", 0.1, min_value=0.0)
        thickness = tree.inputs.float("Thickness", 0.2, min_value=0.0)
        rotation = tree.inputs.float("Rotation", 0.0, subtype="ANGLE")

        with g.Frame("Tooth Profile"):
            # every tooth is four points: up the leading flank, across the tip,
            # down the trailing flank; the root carries on to the next tooth
            pitch = module * teeth / 2
            tip, root = pitch + module, pitch - 1.25 * module

            index = g.Index()
            corner = index % 4
            fraction = g.IndexSwitch.float(corner, [0.0, 0.15, 0.35, 0.5])
            radius = g.IndexSwitch.float(corner, [root, tip, tip, root])
            angle = (index // 4 + fraction) * tau / teeth + rotation

            position = g.CombineXYZ(radius * angle.cos(), radius * angle.sin())
            outline = g.CurveCircle(resolution=teeth * 4) >> g.SetPosition(
                position=position
            )

        with g.Frame("Solid"):
            bore = g.CurveCircle(radius=root * 0.4)
            (
                g.JoinGeometry([outline, bore])
                >> g.FillCurve()
                >> g.ExtrudeMesh(offset=g.CombineXYZ(z=thickness), individual=False)
                >> tree.outputs.geometry("Gear")
            )


# each gear in the train: its tooth count and the direction it sits in,
# seen from the gear before it
TRAIN = [(24, 0.0), (12, 0.0), (18, 1.9), (10, 0.4)]

with g.tree("Gear Train", is_modifier=True) as tree:
    module = tree.inputs.float("Module", 0.1, min_value=0.0)
    thickness = tree.inputs.float("Thickness", 0.2, min_value=0.0)
    spin = tree.inputs.float("Spin", 0.0, subtype="ANGLE")
    material = tree.inputs.material("Material")

    gears = []
    x = y = phase = 0.0  # centre (in modules) and rotation at zero spin
    ratio = 1.0  # how fast this gear turns relative to the first
    previous = None
    for teeth, direction in TRAIN:
        if previous:
            x += (previous + teeth) / 2 * cos(direction)
            y += (previous + teeth) / 2 * sin(direction)
            # put a gap of this gear where a tooth of the previous one points
            phase = direction + pi + previous / teeth * (direction - phase)
            ratio *= -previous / teeth
        previous = teeth

        gear = Gear(teeth, module, thickness, rotation=phase + spin * ratio)
        gears.append(gear >> g.TransformGeometry(translation=module * (x, y, 0.0)))

    (
        g.JoinGeometry(gears)
        >> g.SetMaterial(material=material)
        >> tree.outputs.geometry("Geometry")
    )
