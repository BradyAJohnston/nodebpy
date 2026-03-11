from typing import Literal

import bpy

from ...builder import NodeBuilder, SocketLinker
from ...types import (
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class BrickTexture(NodeBuilder):
    """
    Generate a procedural texture producing bricks
    """

    _bl_idname = "ShaderNodeTexBrick"
    node: bpy.types.ShaderNodeTexBrick

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        color1: TYPE_INPUT_COLOR = None,
        color2: TYPE_INPUT_COLOR = None,
        mortar: TYPE_INPUT_COLOR = None,
        scale: TYPE_INPUT_VALUE = 5.0,
        mortar_size: TYPE_INPUT_VALUE = 0.02,
        mortar_smooth: TYPE_INPUT_VALUE = 0.1,
        bias: TYPE_INPUT_VALUE = 0.0,
        brick_width: TYPE_INPUT_VALUE = 0.5,
        row_height: TYPE_INPUT_VALUE = 0.25,
        *,
        offset_frequency: int = 2,
        squash_frequency: int = 2,
        offset: float = 0.5,
        squash: float = 1.0,
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Color1": color1,
            "Color2": color2,
            "Mortar": mortar,
            "Scale": scale,
            "Mortar Size": mortar_size,
            "Mortar Smooth": mortar_smooth,
            "Bias": bias,
            "Brick Width": brick_width,
            "Row Height": row_height,
        }
        self.offset_frequency = offset_frequency
        self.squash_frequency = squash_frequency
        self.offset = offset
        self.squash = squash
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_color1(self) -> SocketLinker:
        """Input socket: Color1"""
        return self._input("Color1")

    @property
    def i_color2(self) -> SocketLinker:
        """Input socket: Color2"""
        return self._input("Color2")

    @property
    def i_mortar(self) -> SocketLinker:
        """Input socket: Mortar"""
        return self._input("Mortar")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_mortar_size(self) -> SocketLinker:
        """Input socket: Mortar Size"""
        return self._input("Mortar Size")

    @property
    def i_mortar_smooth(self) -> SocketLinker:
        """Input socket: Mortar Smooth"""
        return self._input("Mortar Smooth")

    @property
    def i_bias(self) -> SocketLinker:
        """Input socket: Bias"""
        return self._input("Bias")

    @property
    def i_brick_width(self) -> SocketLinker:
        """Input socket: Brick Width"""
        return self._input("Brick Width")

    @property
    def i_row_height(self) -> SocketLinker:
        """Input socket: Row Height"""
        return self._input("Row Height")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def offset_frequency(self) -> int:
        return self.node.offset_frequency

    @offset_frequency.setter
    def offset_frequency(self, value: int):
        self.node.offset_frequency = value

    @property
    def squash_frequency(self) -> int:
        return self.node.squash_frequency

    @squash_frequency.setter
    def squash_frequency(self, value: int):
        self.node.squash_frequency = value

    @property
    def offset(self) -> float:
        return self.node.offset

    @offset.setter
    def offset(self, value: float):
        self.node.offset = value

    @property
    def squash(self) -> float:
        return self.node.squash

    @squash.setter
    def squash(self, value: float):
        self.node.squash = value


class CheckerTexture(NodeBuilder):
    """
    Generate a checkerboard texture
    """

    _bl_idname = "ShaderNodeTexChecker"
    node: bpy.types.ShaderNodeTexChecker

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        color1: TYPE_INPUT_COLOR = None,
        color2: TYPE_INPUT_COLOR = None,
        scale: TYPE_INPUT_VALUE = 5.0,
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Color1": color1,
            "Color2": color2,
            "Scale": scale,
        }

        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_color1(self) -> SocketLinker:
        """Input socket: Color1"""
        return self._input("Color1")

    @property
    def i_color2(self) -> SocketLinker:
        """Input socket: Color2"""
        return self._input("Color2")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")


class EnvironmentTexture(NodeBuilder):
    """
    Sample an image file as an environment texture. Typically used to light the scene with the background node
    """

    _bl_idname = "ShaderNodeTexEnvironment"
    node: bpy.types.ShaderNodeTexEnvironment

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        projection: Literal["EQUIRECTANGULAR", "MIRROR_BALL"] = "EQUIRECTANGULAR",
        interpolation: Literal["Linear", "Closest", "Cubic", "Smart"] = "Linear",
    ):
        super().__init__()
        key_args = {"Vector": vector}
        self.projection = projection
        self.interpolation = interpolation
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def projection(self) -> Literal["EQUIRECTANGULAR", "MIRROR_BALL"]:
        return self.node.projection

    @projection.setter
    def projection(self, value: Literal["EQUIRECTANGULAR", "MIRROR_BALL"]):
        self.node.projection = value

    @property
    def interpolation(self) -> Literal["Linear", "Closest", "Cubic", "Smart"]:
        return self.node.interpolation

    @interpolation.setter
    def interpolation(self, value: Literal["Linear", "Closest", "Cubic", "Smart"]):
        self.node.interpolation = value


class GaborTexture(NodeBuilder):
    """
    Generate Gabor noise
    """

    _bl_idname = "ShaderNodeTexGabor"
    node: bpy.types.ShaderNodeTexGabor

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VALUE = 5.0,
        frequency: TYPE_INPUT_VALUE = 2.0,
        anisotropy: TYPE_INPUT_VALUE = 1.0,
        orientation_2d: TYPE_INPUT_VALUE = 0.7854,
        orientation_3d: TYPE_INPUT_VECTOR = None,
        *,
        gabor_type: Literal["2D", "3D"] = "2D",
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Scale": scale,
            "Frequency": frequency,
            "Anisotropy": anisotropy,
            "Orientation 2D": orientation_2d,
            "Orientation 3D": orientation_3d,
        }
        self.gabor_type = gabor_type
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_frequency(self) -> SocketLinker:
        """Input socket: Frequency"""
        return self._input("Frequency")

    @property
    def i_anisotropy(self) -> SocketLinker:
        """Input socket: Anisotropy"""
        return self._input("Anisotropy")

    @property
    def i_orientation_2d(self) -> SocketLinker:
        """Input socket: Orientation"""
        return self._input("Orientation 2D")

    @property
    def i_orientation_3d(self) -> SocketLinker:
        """Input socket: Orientation"""
        return self._input("Orientation 3D")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_phase(self) -> SocketLinker:
        """Output socket: Phase"""
        return self._output("Phase")

    @property
    def o_intensity(self) -> SocketLinker:
        """Output socket: Intensity"""
        return self._output("Intensity")

    @property
    def gabor_type(self) -> Literal["2D", "3D"]:
        return self.node.gabor_type

    @gabor_type.setter
    def gabor_type(self, value: Literal["2D", "3D"]):
        self.node.gabor_type = value


class GradientTexture(NodeBuilder):
    """
    Generate interpolated color and intensity values based on the input vector
    """

    _bl_idname = "ShaderNodeTexGradient"
    node: bpy.types.ShaderNodeTexGradient

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        gradient_type: Literal[
            "LINEAR",
            "QUADRATIC",
            "EASING",
            "DIAGONAL",
            "SPHERICAL",
            "QUADRATIC_SPHERE",
            "RADIAL",
        ] = "LINEAR",
    ):
        super().__init__()
        key_args = {"Vector": vector}
        self.gradient_type = gradient_type
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def gradient_type(
        self,
    ) -> Literal[
        "LINEAR",
        "QUADRATIC",
        "EASING",
        "DIAGONAL",
        "SPHERICAL",
        "QUADRATIC_SPHERE",
        "RADIAL",
    ]:
        return self.node.gradient_type

    @gradient_type.setter
    def gradient_type(
        self,
        value: Literal[
            "LINEAR",
            "QUADRATIC",
            "EASING",
            "DIAGONAL",
            "SPHERICAL",
            "QUADRATIC_SPHERE",
            "RADIAL",
        ],
    ):
        self.node.gradient_type = value


class IesTexture(NodeBuilder):
    """
    Match real world lights with IES files, which store the directional intensity distribution of light sources
    """

    _bl_idname = "ShaderNodeTexIES"
    node: bpy.types.ShaderNodeTexIES

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        strength: TYPE_INPUT_VALUE = 1.0,
        *,
        filepath: str = "",
        mode: Literal["INTERNAL", "EXTERNAL"] = "INTERNAL",
    ):
        super().__init__()
        key_args = {"Vector": vector, "Strength": strength}
        self.filepath = filepath
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_strength(self) -> SocketLinker:
        """Input socket: Strength"""
        return self._input("Strength")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def filepath(self) -> str:
        return self.node.filepath

    @filepath.setter
    def filepath(self, value: str):
        self.node.filepath = value

    @property
    def mode(self) -> Literal["INTERNAL", "EXTERNAL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["INTERNAL", "EXTERNAL"]):
        self.node.mode = value


class ImageTexture(NodeBuilder):
    """
    Sample an image file as a texture
    """

    _bl_idname = "ShaderNodeTexImage"
    node: bpy.types.ShaderNodeTexImage

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        projection: Literal["FLAT", "BOX", "SPHERE", "TUBE"] = "FLAT",
        interpolation: Literal["Linear", "Closest", "Cubic", "Smart"] = "Linear",
        projection_blend: float = 0.0,
        extension: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"] = "REPEAT",
    ):
        super().__init__()
        key_args = {"Vector": vector}
        self.projection = projection
        self.interpolation = interpolation
        self.projection_blend = projection_blend
        self.extension = extension
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")

    @property
    def projection(self) -> Literal["FLAT", "BOX", "SPHERE", "TUBE"]:
        return self.node.projection

    @projection.setter
    def projection(self, value: Literal["FLAT", "BOX", "SPHERE", "TUBE"]):
        self.node.projection = value

    @property
    def interpolation(self) -> Literal["Linear", "Closest", "Cubic", "Smart"]:
        return self.node.interpolation

    @interpolation.setter
    def interpolation(self, value: Literal["Linear", "Closest", "Cubic", "Smart"]):
        self.node.interpolation = value

    @property
    def projection_blend(self) -> float:
        return self.node.projection_blend

    @projection_blend.setter
    def projection_blend(self, value: float):
        self.node.projection_blend = value

    @property
    def extension(self) -> Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]:
        return self.node.extension

    @extension.setter
    def extension(self, value: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]):
        self.node.extension = value


class MagicTexture(NodeBuilder):
    """
    Generate a psychedelic color texture
    """

    _bl_idname = "ShaderNodeTexMagic"
    node: bpy.types.ShaderNodeTexMagic

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VALUE = 5.0,
        distortion: TYPE_INPUT_VALUE = 1.0,
        *,
        turbulence_depth: int = 0,
    ):
        super().__init__()
        key_args = {"Vector": vector, "Scale": scale, "Distortion": distortion}
        self.turbulence_depth = turbulence_depth
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_distortion(self) -> SocketLinker:
        """Input socket: Distortion"""
        return self._input("Distortion")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def turbulence_depth(self) -> int:
        return self.node.turbulence_depth

    @turbulence_depth.setter
    def turbulence_depth(self, value: int):
        self.node.turbulence_depth = value


class NoiseTexture(NodeBuilder):
    """
    Generate fractal Perlin noise
    """

    _bl_idname = "ShaderNodeTexNoise"
    node: bpy.types.ShaderNodeTexNoise

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        w: TYPE_INPUT_VALUE = 0.0,
        scale: TYPE_INPUT_VALUE = 5.0,
        detail: TYPE_INPUT_VALUE = 2.0,
        roughness: TYPE_INPUT_VALUE = 0.5,
        lacunarity: TYPE_INPUT_VALUE = 2.0,
        offset: TYPE_INPUT_VALUE = 0.0,
        gain: TYPE_INPUT_VALUE = 1.0,
        distortion: TYPE_INPUT_VALUE = 0.0,
        *,
        noise_dimensions: Literal["1D", "2D", "3D", "4D"] = "3D",
        noise_type: Literal[
            "MULTIFRACTAL",
            "RIDGED_MULTIFRACTAL",
            "HYBRID_MULTIFRACTAL",
            "FBM",
            "HETERO_TERRAIN",
        ] = "FBM",
        normalize: bool = False,
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "W": w,
            "Scale": scale,
            "Detail": detail,
            "Roughness": roughness,
            "Lacunarity": lacunarity,
            "Offset": offset,
            "Gain": gain,
            "Distortion": distortion,
        }
        self.noise_dimensions = noise_dimensions
        self.noise_type = noise_type
        self.normalize = normalize
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_w(self) -> SocketLinker:
        """Input socket: W"""
        return self._input("W")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_detail(self) -> SocketLinker:
        """Input socket: Detail"""
        return self._input("Detail")

    @property
    def i_roughness(self) -> SocketLinker:
        """Input socket: Roughness"""
        return self._input("Roughness")

    @property
    def i_lacunarity(self) -> SocketLinker:
        """Input socket: Lacunarity"""
        return self._input("Lacunarity")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def i_gain(self) -> SocketLinker:
        """Input socket: Gain"""
        return self._input("Gain")

    @property
    def i_distortion(self) -> SocketLinker:
        """Input socket: Distortion"""
        return self._input("Distortion")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def noise_dimensions(self) -> Literal["1D", "2D", "3D", "4D"]:
        return self.node.noise_dimensions

    @noise_dimensions.setter
    def noise_dimensions(self, value: Literal["1D", "2D", "3D", "4D"]):
        self.node.noise_dimensions = value

    @property
    def noise_type(
        self,
    ) -> Literal[
        "MULTIFRACTAL",
        "RIDGED_MULTIFRACTAL",
        "HYBRID_MULTIFRACTAL",
        "FBM",
        "HETERO_TERRAIN",
    ]:
        return self.node.noise_type

    @noise_type.setter
    def noise_type(
        self,
        value: Literal[
            "MULTIFRACTAL",
            "RIDGED_MULTIFRACTAL",
            "HYBRID_MULTIFRACTAL",
            "FBM",
            "HETERO_TERRAIN",
        ],
    ):
        self.node.noise_type = value

    @property
    def normalize(self) -> bool:
        return self.node.normalize

    @normalize.setter
    def normalize(self, value: bool):
        self.node.normalize = value


class SkyTexture(NodeBuilder):
    """
    Generate a procedural sky texture
    """

    _bl_idname = "ShaderNodeTexSky"
    node: bpy.types.ShaderNodeTexSky

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        sky_type: Literal[
            "SINGLE_SCATTERING", "MULTIPLE_SCATTERING", "PREETHAM", "HOSEK_WILKIE"
        ] = "MULTIPLE_SCATTERING",
        sun_disc: bool = True,
        sun_size: float = 0.01,
        sun_intensity: float = 1.0,
        sun_elevation: float = 0.262,
        sun_rotation: float = 0.0,
        altitude: float = 100.0,
        air_density: float = 1.0,
        aerosol_density: float = 1.0,
        ozone_density: float = 1.0,
        sun_direction: float = 0.0,
        turbidity: float = 0.0,
        ground_albedo: float = 0.0,
    ):
        super().__init__()
        key_args = {"Vector": vector}
        self.sky_type = sky_type
        self.sun_disc = sun_disc
        self.sun_size = sun_size
        self.sun_intensity = sun_intensity
        self.sun_elevation = sun_elevation
        self.sun_rotation = sun_rotation
        self.altitude = altitude
        self.air_density = air_density
        self.aerosol_density = aerosol_density
        self.ozone_density = ozone_density
        self.sun_direction = sun_direction
        self.turbidity = turbidity
        self.ground_albedo = ground_albedo
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def sky_type(
        self,
    ) -> Literal[
        "SINGLE_SCATTERING", "MULTIPLE_SCATTERING", "PREETHAM", "HOSEK_WILKIE"
    ]:
        return self.node.sky_type

    @sky_type.setter
    def sky_type(
        self,
        value: Literal[
            "SINGLE_SCATTERING", "MULTIPLE_SCATTERING", "PREETHAM", "HOSEK_WILKIE"
        ],
    ):
        self.node.sky_type = value

    @property
    def sun_disc(self) -> bool:
        return self.node.sun_disc

    @sun_disc.setter
    def sun_disc(self, value: bool):
        self.node.sun_disc = value

    @property
    def sun_size(self) -> float:
        return self.node.sun_size

    @sun_size.setter
    def sun_size(self, value: float):
        self.node.sun_size = value

    @property
    def sun_intensity(self) -> float:
        return self.node.sun_intensity

    @sun_intensity.setter
    def sun_intensity(self, value: float):
        self.node.sun_intensity = value

    @property
    def sun_elevation(self) -> float:
        return self.node.sun_elevation

    @sun_elevation.setter
    def sun_elevation(self, value: float):
        self.node.sun_elevation = value

    @property
    def sun_rotation(self) -> float:
        return self.node.sun_rotation

    @sun_rotation.setter
    def sun_rotation(self, value: float):
        self.node.sun_rotation = value

    @property
    def altitude(self) -> float:
        return self.node.altitude

    @altitude.setter
    def altitude(self, value: float):
        self.node.altitude = value

    @property
    def air_density(self) -> float:
        return self.node.air_density

    @air_density.setter
    def air_density(self, value: float):
        self.node.air_density = value

    @property
    def aerosol_density(self) -> float:
        return self.node.aerosol_density

    @aerosol_density.setter
    def aerosol_density(self, value: float):
        self.node.aerosol_density = value

    @property
    def ozone_density(self) -> float:
        return self.node.ozone_density

    @ozone_density.setter
    def ozone_density(self, value: float):
        self.node.ozone_density = value

    @property
    def sun_direction(self) -> float:
        return self.node.sun_direction

    @sun_direction.setter
    def sun_direction(self, value: float):
        self.node.sun_direction = value

    @property
    def turbidity(self) -> float:
        return self.node.turbidity

    @turbidity.setter
    def turbidity(self, value: float):
        self.node.turbidity = value

    @property
    def ground_albedo(self) -> float:
        return self.node.ground_albedo

    @ground_albedo.setter
    def ground_albedo(self, value: float):
        self.node.ground_albedo = value


class VoronoiTexture(NodeBuilder):
    """
    Generate Worley noise based on the distance to random points. Typically used to generate textures such as stones, water, or biological cells
    """

    _bl_idname = "ShaderNodeTexVoronoi"
    node: bpy.types.ShaderNodeTexVoronoi

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        w: TYPE_INPUT_VALUE = 0.0,
        scale: TYPE_INPUT_VALUE = 5.0,
        detail: TYPE_INPUT_VALUE = 0.0,
        roughness: TYPE_INPUT_VALUE = 0.5,
        lacunarity: TYPE_INPUT_VALUE = 2.0,
        smoothness: TYPE_INPUT_VALUE = 1.0,
        exponent: TYPE_INPUT_VALUE = 0.5,
        randomness: TYPE_INPUT_VALUE = 1.0,
        *,
        voronoi_dimensions: Literal["1D", "2D", "3D", "4D"] = "3D",
        distance: Literal[
            "EUCLIDEAN", "MANHATTAN", "CHEBYCHEV", "MINKOWSKI"
        ] = "EUCLIDEAN",
        feature: Literal[
            "F1", "F2", "SMOOTH_F1", "DISTANCE_TO_EDGE", "N_SPHERE_RADIUS"
        ] = "F1",
        normalize: bool = False,
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "W": w,
            "Scale": scale,
            "Detail": detail,
            "Roughness": roughness,
            "Lacunarity": lacunarity,
            "Smoothness": smoothness,
            "Exponent": exponent,
            "Randomness": randomness,
        }
        self.voronoi_dimensions = voronoi_dimensions
        self.distance = distance
        self.feature = feature
        self.normalize = normalize
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_w(self) -> SocketLinker:
        """Input socket: W"""
        return self._input("W")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_detail(self) -> SocketLinker:
        """Input socket: Detail"""
        return self._input("Detail")

    @property
    def i_roughness(self) -> SocketLinker:
        """Input socket: Roughness"""
        return self._input("Roughness")

    @property
    def i_lacunarity(self) -> SocketLinker:
        """Input socket: Lacunarity"""
        return self._input("Lacunarity")

    @property
    def i_smoothness(self) -> SocketLinker:
        """Input socket: Smoothness"""
        return self._input("Smoothness")

    @property
    def i_exponent(self) -> SocketLinker:
        """Input socket: Exponent"""
        return self._input("Exponent")

    @property
    def i_randomness(self) -> SocketLinker:
        """Input socket: Randomness"""
        return self._input("Randomness")

    @property
    def o_distance(self) -> SocketLinker:
        """Output socket: Distance"""
        return self._output("Distance")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")

    @property
    def o_w(self) -> SocketLinker:
        """Output socket: W"""
        return self._output("W")

    @property
    def o_radius(self) -> SocketLinker:
        """Output socket: Radius"""
        return self._output("Radius")

    @property
    def voronoi_dimensions(self) -> Literal["1D", "2D", "3D", "4D"]:
        return self.node.voronoi_dimensions

    @voronoi_dimensions.setter
    def voronoi_dimensions(self, value: Literal["1D", "2D", "3D", "4D"]):
        self.node.voronoi_dimensions = value

    @property
    def distance(self) -> Literal["EUCLIDEAN", "MANHATTAN", "CHEBYCHEV", "MINKOWSKI"]:
        return self.node.distance

    @distance.setter
    def distance(
        self, value: Literal["EUCLIDEAN", "MANHATTAN", "CHEBYCHEV", "MINKOWSKI"]
    ):
        self.node.distance = value

    @property
    def feature(
        self,
    ) -> Literal["F1", "F2", "SMOOTH_F1", "DISTANCE_TO_EDGE", "N_SPHERE_RADIUS"]:
        return self.node.feature

    @feature.setter
    def feature(
        self,
        value: Literal["F1", "F2", "SMOOTH_F1", "DISTANCE_TO_EDGE", "N_SPHERE_RADIUS"],
    ):
        self.node.feature = value

    @property
    def normalize(self) -> bool:
        return self.node.normalize

    @normalize.setter
    def normalize(self, value: bool):
        self.node.normalize = value


class WaveTexture(NodeBuilder):
    """
    Generate procedural bands or rings with noise
    """

    _bl_idname = "ShaderNodeTexWave"
    node: bpy.types.ShaderNodeTexWave

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VALUE = 5.0,
        distortion: TYPE_INPUT_VALUE = 0.0,
        detail: TYPE_INPUT_VALUE = 2.0,
        detail_scale: TYPE_INPUT_VALUE = 1.0,
        detail_roughness: TYPE_INPUT_VALUE = 0.5,
        phase_offset: TYPE_INPUT_VALUE = 0.0,
        *,
        wave_type: Literal["BANDS", "RINGS"] = "BANDS",
        bands_direction: Literal["X", "Y", "Z", "DIAGONAL"] = "X",
        rings_direction: Literal["X", "Y", "Z", "SPHERICAL"] = "X",
        wave_profile: Literal["SIN", "SAW", "TRI"] = "SIN",
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Scale": scale,
            "Distortion": distortion,
            "Detail": detail,
            "Detail Scale": detail_scale,
            "Detail Roughness": detail_roughness,
            "Phase Offset": phase_offset,
        }
        self.wave_type = wave_type
        self.bands_direction = bands_direction
        self.rings_direction = rings_direction
        self.wave_profile = wave_profile
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_distortion(self) -> SocketLinker:
        """Input socket: Distortion"""
        return self._input("Distortion")

    @property
    def i_detail(self) -> SocketLinker:
        """Input socket: Detail"""
        return self._input("Detail")

    @property
    def i_detail_scale(self) -> SocketLinker:
        """Input socket: Detail Scale"""
        return self._input("Detail Scale")

    @property
    def i_detail_roughness(self) -> SocketLinker:
        """Input socket: Detail Roughness"""
        return self._input("Detail Roughness")

    @property
    def i_phase_offset(self) -> SocketLinker:
        """Input socket: Phase Offset"""
        return self._input("Phase Offset")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_fac(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Fac")

    @property
    def wave_type(self) -> Literal["BANDS", "RINGS"]:
        return self.node.wave_type

    @wave_type.setter
    def wave_type(self, value: Literal["BANDS", "RINGS"]):
        self.node.wave_type = value

    @property
    def bands_direction(self) -> Literal["X", "Y", "Z", "DIAGONAL"]:
        return self.node.bands_direction

    @bands_direction.setter
    def bands_direction(self, value: Literal["X", "Y", "Z", "DIAGONAL"]):
        self.node.bands_direction = value

    @property
    def rings_direction(self) -> Literal["X", "Y", "Z", "SPHERICAL"]:
        return self.node.rings_direction

    @rings_direction.setter
    def rings_direction(self, value: Literal["X", "Y", "Z", "SPHERICAL"]):
        self.node.rings_direction = value

    @property
    def wave_profile(self) -> Literal["SIN", "SAW", "TRI"]:
        return self.node.wave_profile

    @wave_profile.setter
    def wave_profile(self, value: Literal["SIN", "SAW", "TRI"]):
        self.node.wave_profile = value


class WhiteNoiseTexture(NodeBuilder):
    """
    Calculate a random value or color based on an input seed
    """

    _bl_idname = "ShaderNodeTexWhiteNoise"
    node: bpy.types.ShaderNodeTexWhiteNoise

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        w: TYPE_INPUT_VALUE = 0.0,
        *,
        noise_dimensions: Literal["1D", "2D", "3D", "4D"] = "3D",
    ):
        super().__init__()
        key_args = {"Vector": vector, "W": w}
        self.noise_dimensions = noise_dimensions
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_w(self) -> SocketLinker:
        """Input socket: W"""
        return self._input("W")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def noise_dimensions(self) -> Literal["1D", "2D", "3D", "4D"]:
        return self.node.noise_dimensions

    @noise_dimensions.setter
    def noise_dimensions(self, value: Literal["1D", "2D", "3D", "4D"]):
        self.node.noise_dimensions = value
