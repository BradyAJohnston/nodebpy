from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Generic, Iterable, Literal, TypeVar

import bpy
import bpy.types
from bpy.types import (
    ColorRamp,
    ColorRampElements,
    CurveMapPoints,
    NodeEvaluateClosure,
    NodeSocket,
    NodeSocketString,
)

from nodebpy.builder._registry import _get_socket_linker

from ...builder import (
    BaseNode,
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    DynamicInputsMixin,
    FloatSocket,
    FontSocket,
    GeometrySocket,
    ImageSocket,
    IntegerSocket,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    SocketAccessor,
    StringSocket,
    TreeBuilder,
    VectorSocket,
)
from ...builder import (
    Socket as SocketLinker,
)
from ...types import (
    SOCKET_TYPES,
    InputAny,
    InputBoolean,
    InputBundle,
    InputClosure,
    InputCollection,
    InputColor,
    InputFloat,
    InputFont,
    InputGeometry,
    InputGrid,
    InputImage,
    InputInteger,
    InputLinkable,
    InputMaterial,
    InputMatrix,
    InputMenu,
    InputObject,
    InputRotation,
    InputString,
    InputVector,
    _AccumulateFieldDataTypes,
    _AttributeDataTypes,
    _AttributeDomains,
    _BakeDataTypes,
    _BakedDataTypeValues,
    _EvaluateAtIndexDataTypes,
    _GridDataTypes,
    _is_default_value,
)
from .zone import (
    ClosureInput,
    ClosureOutput,
    ClosureZone,
    ForEachGeometryElementInput,
    ForEachGeometryElementOutput,
    ForEachGeometryElementZone,
    RepeatInput,
    RepeatOutput,
    RepeatZone,
    SimulationInput,
    SimulationOutput,
    SimulationZone,
    _sync_closure_items,
)

_T = TypeVar("_T")
_S = TypeVar("_S")

__all__ = (
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "SimulationInput",
    "SimulationOutput",
    "SimulationZone",
    "ForEachGeometryElementInput",
    "ForEachGeometryElementOutput",
    "ForEachGeometryElementZone",
    "EvaluateClosure",
    "ClosureInput",
    "ClosureOutput",
    "ClosureZone",
    "GeometryToInstance",
    "SDFGridBoolean",
    #
    "SetHandleType",
    "HandleTypeSelection",
    "IndexSwitch",
    "MenuSwitch",
    "MeshBoolean",
    "CaptureAttribute",
    "FieldToGrid",
    "JoinGeometry",
    "SDFGridBoolean",
    "Bake",
    "JoinStrings",
    "GeometryToInstance",
    "FormatString",
    "JoinStrings",
    "Value",
    "AccumulateField",
    "EvaluateAtIndex",
    "FieldAverage",
    "FieldMinAndMax",
    "EvaluateOnDomain",
    "FieldVariance",
    "Compare",
    "AttributeStatistic",
    "Frame",
    "Float",
    "FloatCurve",
    "ColorRamp",
    "Switch",
    "StoreNamedAttribute",
)


def tree(
    name: str = "Geometry Node Group",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
) -> TreeBuilder:
    return TreeBuilder.geometry(name, collapse=collapse, arrange=arrange)


_SwitchDataTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "MENU",
    "OBJECT",
    "IMAGE",
    "GEOMETRY",
    "COLLECTION",
    "MATERIAL",
    "BUNDLE",
    "CLOSURE",
    "FONT",
]


class Switch(BaseNode, Generic[_T]):
    """
    Switch between two inputs

    Parameters
    ----------
    switch : InputBoolean
        Switch
    false : InputFloat
        False
    true : InputFloat
        True

    Inputs
    ------
    i.switch : BooleanSocket
        Switch
    i.false : FloatSocket
        False
    i.true : FloatSocket
        True

    Outputs
    -------
    o.output : FloatSocket
        Output
    """

    _bl_idname = "GeometryNodeSwitch"
    node: bpy.types.GeometryNodeSwitch

    class _Inputs(SocketAccessor, Generic[_S]):
        switch: BooleanSocket
        """Switch"""
        false: _S
        """False"""
        true: _S
        """True"""

    class _Outputs(SocketAccessor, Generic[_S]):
        output: _S
        """Output"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs[_T]: ...
        @property
        def o(self) -> _Outputs[_T]: ...

    def __init__(
        self,
        switch: InputBoolean = False,
        false: InputAny = None,
        true: InputAny = None,
        *,
        input_type: _SwitchDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Switch": switch, "False": false, "True": true}
        self.input_type = input_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        switch: InputBoolean = False,
        false: InputFloat = 0.0,
        true: InputFloat = 0.0,
    ) -> "Switch[FloatSocket]":
        """Create Switch with operation 'Float'."""
        return Switch(input_type="FLOAT", switch=switch, false=false, true=true)

    @classmethod
    def integer(
        cls,
        switch: InputBoolean = False,
        false: InputInteger = 0,
        true: InputInteger = 0,
    ) -> "Switch[IntegerSocket]":
        """Create Switch with operation 'Integer'."""
        return Switch(input_type="INT", switch=switch, false=false, true=true)

    @classmethod
    def boolean(
        cls,
        switch: InputBoolean = False,
        false: InputBoolean = False,
        true: InputBoolean = False,
    ) -> "Switch[BooleanSocket]":
        """Create Switch with operation 'Boolean'."""
        return Switch(input_type="BOOLEAN", switch=switch, false=false, true=true)

    @classmethod
    def vector(
        cls,
        switch: InputBoolean = False,
        false: InputVector = None,
        true: InputVector = None,
    ) -> "Switch[VectorSocket]":
        """Create Switch with operation 'Vector'."""
        return Switch(input_type="VECTOR", switch=switch, false=false, true=true)

    @classmethod
    def color(
        cls,
        switch: InputBoolean = False,
        false: InputColor = None,
        true: InputColor = None,
    ) -> "Switch[ColorSocket]":
        """Create Switch with operation 'Color'."""
        return Switch(input_type="RGBA", switch=switch, false=false, true=true)

    @classmethod
    def rotation(
        cls,
        switch: InputBoolean = False,
        false: InputRotation = None,
        true: InputRotation = None,
    ) -> "Switch[RotationSocket]":
        """Create Switch with operation 'Rotation'."""
        return Switch(input_type="ROTATION", switch=switch, false=false, true=true)

    @classmethod
    def matrix(
        cls,
        switch: InputBoolean = False,
        false: InputMatrix = None,
        true: InputMatrix = None,
    ) -> "Switch[MatrixSocket]":
        """Create Switch with operation 'Matrix'."""
        return Switch(input_type="MATRIX", switch=switch, false=false, true=true)

    @classmethod
    def string(
        cls,
        switch: InputBoolean = False,
        false: InputString = "",
        true: InputString = "",
    ) -> "Switch[StringSocket]":
        """Create Switch with operation 'String'."""
        return Switch(input_type="STRING", switch=switch, false=false, true=true)

    @classmethod
    def menu(
        cls,
        switch: InputBoolean = False,
        false: InputMenu = None,
        true: InputMenu = None,
    ) -> "Switch[MenuSocket]":
        """Create Switch with operation 'Menu'."""
        return Switch(input_type="MENU", switch=switch, false=false, true=true)

    @classmethod
    def object(
        cls,
        switch: InputBoolean = False,
        false: InputObject = None,
        true: InputObject = None,
    ) -> "Switch[ObjectSocket]":
        """Create Switch with operation 'Object'."""
        return Switch(input_type="OBJECT", switch=switch, false=false, true=true)

    @classmethod
    def image(
        cls,
        switch: InputBoolean = False,
        false: InputImage = None,
        true: InputImage = None,
    ) -> "Switch[ImageSocket]":
        """Create Switch with operation 'Image'."""
        return Switch(input_type="IMAGE", switch=switch, false=false, true=true)

    @classmethod
    def geometry(
        cls,
        switch: InputBoolean = False,
        false: InputGeometry = None,
        true: InputGeometry = None,
    ) -> "Switch[GeometrySocket]":
        """Create Switch with operation 'Geometry'."""
        return Switch(input_type="GEOMETRY", switch=switch, false=false, true=true)

    @classmethod
    def collection(
        cls,
        switch: InputBoolean = False,
        false: InputCollection = None,
        true: InputCollection = None,
    ) -> "Switch[CollectionSocket]":
        """Create Switch with operation 'Collection'."""
        return Switch(input_type="COLLECTION", switch=switch, false=false, true=true)

    @classmethod
    def material(
        cls,
        switch: InputBoolean = False,
        false: InputMaterial = None,
        true: InputMaterial = None,
    ) -> "Switch[MaterialSocket]":
        """Create Switch with operation 'Material'."""
        return Switch(input_type="MATERIAL", switch=switch, false=false, true=true)

    @classmethod
    def bundle(
        cls,
        switch: InputBoolean = False,
        false: InputBundle = None,
        true: InputBundle = None,
    ) -> "Switch[BundleSocket]":
        """Create Switch with operation 'Bundle'."""
        return Switch(input_type="BUNDLE", switch=switch, false=false, true=true)

    @classmethod
    def closure(
        cls,
        switch: InputBoolean = False,
        false: InputClosure = None,
        true: InputClosure = None,
    ) -> "Switch[ClosureSocket]":
        """Create Switch with operation 'Closure'."""
        return Switch(input_type="CLOSURE", switch=switch, false=false, true=true)

    @classmethod
    def font(
        cls,
        switch: InputBoolean = False,
        false: InputFont = None,
        true: InputFont = None,
    ) -> "Switch[FontSocket]":
        """Create Switch with operation 'Font'."""
        return Switch(input_type="FONT", switch=switch, false=false, true=true)

    @property
    def input_type(
        self,
    ) -> _SwitchDataTypes:
        return self.node.input_type  # ty: ignore[invalid-return-type]

    @input_type.setter
    def input_type(
        self,
        value: _SwitchDataTypes,
    ):
        self.node.input_type = value


_ColorRampColorInterpolations = Literal[
    "EASE", "CARDINAL", "LINEAR", "B_SPLINE", "CONSTANT"
]
_ColorRampHueInterpolations = Literal["NEAR", "FAR", "CW", "CCW"]
_ColorModes = Literal["RGB", "HSV", "HSL"]


class ColorRamp(BaseNode):
    """
    Map values to colors with the use of a gradient

    Parameters
    ----------
    fac : InputFloat
        Factor: Which is used to sample the ColorRamp for the output color.
    items : Iterable[tuple[float, tuple[float, float, float float]]]
        Iterable of items which contain (position, color) which position being a
        4-component float for values RGBA. Position is a value betwen `0..1`.


    Inputs
    ------
    i.fac : FloatSocket
        Factor: The input value between `0..1` which maps to the final color value.

    Outputs
    -------
    o.color : ColorSocket
        Color: The mapped color value based in the input `fac`.
    o.alpha : FloatSocket
        Alpha: The mapped alpha of the color based on the input `fac`.
    """

    _bl_idname = "ShaderNodeValToRGB"
    node: bpy.types.ShaderNodeValToRGB

    class _Inputs(SocketAccessor):
        fac: FloatSocket
        """Factor"""

    class _Outputs(SocketAccessor):
        color: ColorSocket
        """Color"""
        alpha: FloatSocket
        """Alpha"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        fac: InputFloat = 0.5,
        *,
        items: Iterable[tuple[float, tuple[float, float, float, float]]] = (),
        color_interpolation: _ColorRampColorInterpolations = "EASE",
        hue_interpolation: _ColorRampHueInterpolations = "NEAR",
        mode: _ColorModes = "RGB",
    ):
        super().__init__()
        key_args = {"Fac": fac}
        for i, item in enumerate(items):
            if i < 2:
                point = self.elements[i]
            else:
                point = self.elements.new(0.0)
            point.position = item[0]
            point.color = item[1]

        self._establish_links(**key_args)
        self.color_interpolation = color_interpolation
        self.hue_interpolation = hue_interpolation
        self.mode = mode

    @property
    def _color_ramp(self) -> ColorRamp:
        assert self.node.color_ramp
        return self.node.color_ramp

    @property
    def elements(self) -> ColorRampElements:
        return self._color_ramp.elements

    @property
    def color_interpolation(self) -> _ColorRampColorInterpolations:
        return self._color_ramp.interpolation

    @color_interpolation.setter
    def color_interpolation(self, value: _ColorRampColorInterpolations) -> None:
        self._color_ramp.interpolation = value

    @property
    def hue_interpolation(self) -> _ColorRampHueInterpolations:
        return self._color_ramp.hue_interpolation

    @hue_interpolation.setter
    def hue_interpolation(self, value: _ColorRampHueInterpolations) -> None:
        self._color_ramp.hue_interpolation = value

    @property
    def mode(self) -> _ColorModes:
        return self._color_ramp.color_mode

    @mode.setter
    def mode(self, value: _ColorModes) -> None:
        self._color_ramp.color_mode = value


class FloatCurve(BaseNode):
    """
    Map an input float to a curve and outputs a float value

    Parameters
    ----------
    factor : InputFloat
        Factor
    value : InputFloat
        Value
    items : Iterable[tuple[float, float] | tuple[float, float, Literal["AUTO", "AUTO_CLAMPED", "VECTOR"]]]
        An iterable which contains items `(x, y, Optional[handle_type])`. The position values are between
        `0..1` and map the input `value` to the output `value` from the resulting curve interpolation.

    Inputs
    ------
    i.factor : FloatSocket
        Factor
    i.value : FloatSocket
        Value

    Outputs
    -------
    o.value : FloatSocket
        Value
    """

    _bl_idname = "ShaderNodeFloatCurve"
    node: bpy.types.ShaderNodeFloatCurve

    class _Inputs(SocketAccessor):
        factor: FloatSocket
        """Factor"""
        value: FloatSocket
        """Value"""

    class _Outputs(SocketAccessor):
        value: FloatSocket
        """Value"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        factor: InputFloat = 1.0,
        value: InputFloat = 1.0,
        *,
        items: Iterable[
            tuple[float, float]
            | tuple[float, float, Literal["AUTO", "AUTO_CLAMPED", "VECTOR"]]
        ] = (),
    ):
        super().__init__()
        key_args = {"Factor": factor, "Value": value}

        for i, item in enumerate(items):
            if i < 2:
                point = self.points[i]
                point.location = item[:2]
            else:
                point = self.points.new(*item[:2])
            if len(item) > 2:
                point.handle_type = item[2]  # ty: ignore[index-out-of-bounds]

        self._establish_links(**key_args)

    @property
    def points(self) -> CurveMapPoints:
        mapping = self.node.mapping
        assert mapping
        return mapping.curves[0].points


_NamedAttributeDataTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "FLOAT_VECTOR",
    "FLOAT_COLOR",
    "QUATERNION",
    "FLOAT4X4",
    "INT8",
    "FLOAT2",
    "BYTE_COLOR",
]


class StoreNamedAttribute(BaseNode, Generic[_T]):
    """
    Store the result of a field on a geometry as an attribute with the specified name

    Parameters
    ----------
    geometry : InputGeometry
        Geometry
    selection : InputBoolean
        Selection
    name : InputString
        Name
    value : InputFloat
        Value

    Inputs
    ------
    i.geometry : GeometrySocket
        Geometry
    i.selection : BooleanSocket
        Selection
    i.name : StringSocket
        Name
    i.value : FloatSocket
        Value

    Outputs
    -------
    o.geometry : GeometrySocket
        Geometry
    """

    _bl_idname = "GeometryNodeStoreNamedAttribute"
    node: bpy.types.GeometryNodeStoreNamedAttribute

    class _StoreNamedAttributeDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputFloat = 0.0,
        ) -> "StoreNamedAttribute[FloatSocket]":
            """Create Store Named Attribute with operation 'Float'. Floating-point value"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="FLOAT",
                domain=self._domain,
            )

        def integer(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputInteger = 0,
        ) -> "StoreNamedAttribute[IntegerSocket]":
            """Create Store Named Attribute with operation 'Integer'. 32-bit integer"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="INT",
                domain=self._domain,
            )

        def boolean(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputBoolean = False,
        ) -> "StoreNamedAttribute[BooleanSocket]":
            """Create Store Named Attribute with operation 'Boolean'. True or false"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="BOOLEAN",
                domain=self._domain,
            )

        def vector(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputVector = None,
        ) -> "StoreNamedAttribute[VectorSocket]":
            """Create Store Named Attribute with operation 'Vector'. 3D vector with floating-point values"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="FLOAT_VECTOR",
                domain=self._domain,
            )

        def color(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputColor = None,
        ) -> "StoreNamedAttribute[ColorSocket]":
            """Create Store Named Attribute with operation 'Color'. RGBA color with 32-bit floating-point values"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="FLOAT_COLOR",
                domain=self._domain,
            )

        def quaternion(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputRotation = None,
        ) -> "StoreNamedAttribute[RotationSocket]":
            """Create Store Named Attribute with operation 'Quaternion'. Floating point quaternion rotation"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="QUATERNION",
                domain=self._domain,
            )

        def matrix(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputMatrix = None,
        ) -> "StoreNamedAttribute[MatrixSocket]":
            """Create Store Named Attribute with operation '4x4 Matrix'. Floating point matrix"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="FLOAT4X4",
                domain=self._domain,
            )

        def integer_8bit(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputInteger = 0,
        ) -> "StoreNamedAttribute[IntegerSocket]":
            """Create Store Named Attribute with operation '8-Bit Integer'. Smaller integer with a range from -128 to 127"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="INT8",
                domain=self._domain,
            )

        def vector_2d(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputVector = None,
        ) -> "StoreNamedAttribute[VectorSocket]":
            """Create Store Named Attribute with operation '2D Vector'. 2D vector with floating-point values"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="FLOAT2",
                domain=self._domain,
            )

        def byte_color(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = True,
            name: InputString = "",
            value: InputColor = None,
        ) -> "StoreNamedAttribute[ColorSocket]":
            """Create Store Named Attribute with operation 'Byte Color'. RGBA color with 8-bit positive integer values"""
            return StoreNamedAttribute(
                geometry=geometry,
                selection=selection,
                name=name,
                value=value,
                data_type="BYTE_COLOR",
                domain=self._domain,
            )

    point = _StoreNamedAttributeDomainFactory("POINT")
    edge = _StoreNamedAttributeDomainFactory("EDGE")
    face = _StoreNamedAttributeDomainFactory("FACE")
    corner = _StoreNamedAttributeDomainFactory("CORNER")
    spline = _StoreNamedAttributeDomainFactory("CURVE")
    instance = _StoreNamedAttributeDomainFactory("INSTANCE")
    layer = _StoreNamedAttributeDomainFactory("LAYER")

    class _Inputs(SocketAccessor, Generic[_S]):
        geometry: GeometrySocket
        """Geometry"""
        selection: BooleanSocket
        """Selection"""
        name: StringSocket
        """Name"""
        value: _S
        """Value"""

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
        """Geometry"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        geometry: InputGeometry = None,
        selection: InputBoolean = True,
        name: InputString = "",
        value: InputAny = 0.0,
        *,
        data_type: _NamedAttributeDataTypes = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Name": name,
            "Value": value,
        }
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def data_type(
        self,
    ) -> _NamedAttributeDataTypes:
        return self.node.data_type  # ty: ignore[invalid-return-type]

    @data_type.setter
    def data_type(
        self,
        value: _NamedAttributeDataTypes,
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class EvaluateClosure(BaseNode):
    """
    Execute a given closure

    Parameters
    ----------
    closure : InputClosure
        Closure

    Inputs
    ------
    i.closure : ClosureSocket
        Closure
    """

    _bl_idname = "NodeEvaluateClosure"
    node: NodeEvaluateClosure

    class _Inputs(SocketAccessor):
        closure: ClosureSocket
        """Closure"""

    class _Outputs(SocketAccessor):
        pass

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        closure: InputClosure = None,
        *,
        active_input_index: int = 0,
        active_output_index: int = 0,
        define_signature: bool = False,
    ):
        super().__init__()
        key_args = {"Closure": closure}
        self.active_input_index = active_input_index
        self.active_output_index = active_output_index
        self.define_signature = define_signature
        self._establish_links(**key_args)

    def sync_signature(self, node: ClosureOutput | ClosureZone) -> None:
        if isinstance(node, ClosureZone):
            node = node.output

        for name in ["input_items", "output_items"]:
            _sync_closure_items(getattr(node.node, name), getattr(self.node, name))


class Frame(BaseNode):
    """ """

    _bl_idname = "NodeFrame"
    node: bpy.types.NodeFrame

    def __init__(
        self,
        label: str | None = None,
        shrink: bool = True,
        text: bpy.types.Text | None = None,
    ):
        super().__init__()
        self.label = label
        self.shrink = shrink
        self.text = text

    @property
    def label(self) -> str | None:
        return self.node.label

    @label.setter
    def label(self, value: str | None):
        if value is not None:
            self.node.label = value

    @property
    def shrink(self) -> bool:
        return self.node.shrink

    @shrink.setter
    def shrink(self, value: bool):
        self.node.shrink = value

    @property
    def text(self) -> bpy.types.Text | None:
        return self.node.text

    @text.setter
    def text(self, value: bpy.types.Text | None):
        if value is not None:
            self.node.text = value

    def __enter__(self):
        TreeBuilder._frame_contexts.append(self.node)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        TreeBuilder._frame_contexts.pop()


class Bake(BaseNode, DynamicInputsMixin):
    """Cache the incoming data so that it can be used without recomputation

    TODO: properly handle Animation / Still bake opations and ability to bake to a file
    """

    _bl_idname = "GeometryNodeBake"
    node: bpy.types.GeometryNodeBake
    _socket_data_types = _BakedDataTypeValues

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._establish_links(**self._add_inputs(*args, **kwargs))

    def _add_socket(
        self, name: str, type: _BakeDataTypes, default_value: Any | None = None
    ):
        item = self.node.bake_items.new(socket_type=type, name=name)
        return self.node.inputs[item.name]


class GeometryToInstance(BaseNode):
    """
    Convert each input geometry into an instance, which can be much faster
    than the Join Geometry node when the inputs are large

    Inputs
    ------
    geometry : GeometrySocket
        Multi-input socket; geometry that will be converted into an instance

    Outputs
    -------
    instances : GeometrySocket
        Single geometry output with each input linked geometry as a separate instance

    """

    _bl_idname = "GeometryNodeGeometryToInstance"
    node: bpy.types.GeometryNodeGeometryToInstance

    class _Inputs(SocketAccessor):
        geometry: GeometrySocket

    class _Outputs(SocketAccessor):
        instances: GeometrySocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(self, *args: InputGeometry):
        super().__init__()
        for arg in reversed(args):
            self._link_from(arg, "Geometry")


### === ###
# The input properties for these nodes aren't being properly picked
# up by the generate script. TODO: debug why not


class Collection(BaseNode):
    """
    Output a single collection
    """

    _bl_idname = "GeometryNodeInputCollection"
    node: bpy.types.GeometryNodeInputCollection

    class _Outputs(SocketAccessor):
        collection: CollectionSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, collection: bpy.types.Collection | None = None):
        super().__init__()
        self.collection = collection

    @property
    def collection(self) -> bpy.types.Collection | None:
        """Input socket: Collection"""
        return self.node.collection

    @collection.setter
    def collection(self, value: bpy.types.Collection | None):
        self.node.collection = value


class Material(BaseNode):
    """
    Output a single material
    """

    _bl_idname = "GeometryNodeInputMaterial"
    node: bpy.types.GeometryNodeInputMaterial

    class _Outputs(SocketAccessor):
        material: MaterialSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, material: bpy.types.Material | None = None):
        super().__init__()
        self.material = material

    @property
    def material(self) -> bpy.types.Material | None:
        """Input socket: Material"""
        return self.node.material

    @material.setter
    def material(self, value: bpy.types.Material | None):
        self.node.material = value


class Object(BaseNode):
    """
    Output a single object
    """

    _bl_idname = "GeometryNodeInputObject"
    node: bpy.types.GeometryNodeInputObject

    class _Outputs(SocketAccessor):
        object: ObjectSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, object: bpy.types.Object | None = None):
        super().__init__()
        self.object = object

    @property
    def object(self) -> bpy.types.Object | None:
        """Input socket: Object"""
        return self.node.object

    @object.setter
    def object(self, value: bpy.types.Object | None):
        self.node.object = value


### === ###
# The value node doesn't have a proper value property and instead it directly display
# and access the default values from the output sockets themselves


class Value(BaseNode):
    """Input numerical values to other nodes in the tree"""

    _bl_idname = "ShaderNodeValue"
    node: bpy.types.ShaderNodeValue

    class _Outputs(SocketAccessor):
        value: FloatSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, value: float = 0.0):
        super().__init__()
        self.value = value

    @property
    def value(self) -> float:
        """Input socket: Value"""

        return self.node.outputs[0].default_value  # type: ignore

    @value.setter
    def value(self, value: float):
        self.node.outputs[0].default_value = value  # type: ignore


class Float(Value):
    """Input numerical values to other nodes in the tree. A 'type-hinted' wrapper of the Value node."""


### === ###


class FormatString(BaseNode, DynamicInputsMixin):
    """Insert values into a string using a Python and path template compatible formatting syntax"""

    _bl_idname = "FunctionNodeFormatString"
    node: bpy.types.FunctionNodeFormatString
    _socket_data_types = ("VALUE", "INT", "STRING")
    _type_map = {
        "VALUE": "FLOAT",
    }

    class _Inputs(SocketAccessor):
        format: StringSocket
        input_socket: SocketLinker

    class _Outputs(SocketAccessor):
        string: StringSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(
        self,
        format: InputString = "",
        items: Mapping[str, InputString | InputInteger | InputFloat] = {},
    ):
        super().__init__()
        key_args = {"Format": format}
        key_args.update(self._add_inputs(**items))
        self._establish_links(**key_args)

    def _add_socket(
        self,
        name: str,
        type: Literal["FLOAT", "INT", "STRING"] = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.format_items.new(socket_type=type, name=name)
        if default_value is not None and hasattr(self.i[item.name], "default_value"):
            self.i[item.name].default_value = default_value  # ty: ignore[unresolved-attribute]
        return self.node.inputs[item.name]

    @property
    def items(self) -> dict[str, SocketLinker]:
        """Input sockets:"""
        return {socket.name: self.i._get(socket.name) for socket in self.node.inputs}


class JoinStrings(BaseNode):
    """Combine any number of input strings"""

    _bl_idname = "GeometryNodeStringJoin"
    node: bpy.types.GeometryNodeStringJoin

    class _Outputs(SocketAccessor):
        string: StringSocket

    class _Inputs(SocketAccessor):
        delimiter: StringSocket
        strings: StringSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(
        self,
        strings: Iterable[StringSocket | NodeSocketString | BaseNode] = (),
        delimiter: InputString = "",
    ):
        super().__init__()

        self._establish_links(Delimiter=delimiter)
        for string in reversed(strings):
            self._link_from(string, "Strings")


class MeshBoolean(BaseNode):
    """Cut, subtract, or join multiple mesh inputs"""

    _bl_idname = "GeometryNodeMeshBoolean"
    node: bpy.types.GeometryNodeMeshBoolean

    class _Inputs(SocketAccessor):
        mesh_1: GeometrySocket
        mesh_2: GeometrySocket
        self_intersection: BooleanSocket
        hole_tolerant: BooleanSocket

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
        intersecting_edges: BooleanSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(
        self,
        mesh_1: InputGeometry = None,
        mesh_2: Iterable[InputGeometry] = (),
        *,
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
        operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE",
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Mesh 1": mesh_1,
            "Self Intersection": self_intersection,
            "Hole Tolerant": hole_tolerant,
        }
        for arg in mesh_2:
            self._link_from(arg, "Mesh 2")

        self.operation = operation
        self.solver = solver
        self._establish_links(**key_args)

    @classmethod
    def intersect(
        cls,
        items: Iterable[InputGeometry] = (),
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
        *,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            mesh_2=items,
            **key_args,
            solver=solver,
            operation="INTERSECT",
        )

    @classmethod
    def union(
        cls,
        items: Iterable[InputGeometry] = (),
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
        *,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            mesh_2=items,
            **key_args,
            solver=solver,
            operation="UNION",
        )

    @classmethod
    def difference(
        cls,
        mesh_1: InputGeometry = None,
        items: Iterable[InputGeometry] = (),
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
        *,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            mesh_1=mesh_1,
            mesh_2=items,
            solver=solver,
            operation="DIFFERENCE",
            **key_args,
        )

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value

    @property
    def solver(self) -> Literal["EXACT", "FLOAT", "MANIFOLD"]:
        return self.node.solver

    @solver.setter
    def solver(self, value: Literal["EXACT", "FLOAT", "MANIFOLD"]):
        self.node.solver = value


class JoinGeometry(BaseNode):
    """Merge separately generated geometries into a single one"""

    _bl_idname = "GeometryNodeJoinGeometry"
    node: bpy.types.GeometryNodeJoinGeometry

    class _Inputs(SocketAccessor):
        geometry: GeometrySocket

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(self, geometry: Iterable[InputGeometry] = ()):
        super().__init__()
        for source in reversed(geometry):
            assert source
            self._link(*self._find_best_socket_pair(source, self))


class SetHandleType(BaseNode):
    """Set the handle type for the control points of a Bézier curve"""

    _bl_idname = "GeometryNodeCurveSetHandles"
    node: bpy.types.GeometryNodeCurveSetHandles

    class _Inputs(SocketAccessor):
        curve: GeometrySocket
        selection: BooleanSocket

    class _Outputs(SocketAccessor):
        curve: GeometrySocket

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        curve: InputGeometry = None,
        selection: InputBoolean = True,
        *,
        left: bool = False,
        right: bool = False,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection}
        self.handle_type = handle_type
        self.left = left
        self.right = right
        self._establish_links(**key_args)

    @property
    def handle_type(self) -> Literal["FREE", "AUTO", "VECTOR", "ALIGN"]:
        return self.node.handle_type

    @handle_type.setter
    def handle_type(self, value: Literal["FREE", "AUTO", "VECTOR", "ALIGN"]):
        self.node.handle_type = value

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        match value, self.right:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        match self.left, value:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()


class HandleTypeSelection(BaseNode):
    """Provide a selection based on the handle types of Bézier control points"""

    _bl_idname = "GeometryNodeCurveHandleTypeSelection"
    node: bpy.types.GeometryNodeCurveHandleTypeSelection

    class _Outputs(SocketAccessor):
        selection: BooleanSocket

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
        left: bool = True,
        right: bool = True,
    ):
        super().__init__()
        self.handle_type = handle_type
        self.left = left
        self.right = right

    @property
    def handle_type(self) -> Literal["FREE", "AUTO", "VECTOR", "ALIGN"]:
        return self.node.handle_type

    @handle_type.setter
    def handle_type(self, value: Literal["FREE", "AUTO", "VECTOR", "ALIGN"]):
        self.node.handle_type = value

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        match value, self.right:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        match self.left, value:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]):
        self.node.mode = value


class IndexSwitch(BaseNode, Generic[_T]):
    """Node builder for the Index Switch node"""

    _bl_idname = "GeometryNodeIndexSwitch"
    node: bpy.types.GeometryNodeIndexSwitch

    @classmethod
    def float(
        cls, index: InputInteger = 0, items: Iterable[InputFloat] = ()
    ) -> "IndexSwitch[FloatSocket]":
        return IndexSwitch(index=index, items=items, data_type="FLOAT")

    @classmethod
    def integer(
        cls, index: InputInteger = 0, items: Iterable[InputInteger] = ()
    ) -> "IndexSwitch[IntegerSocket]":
        return IndexSwitch(index=index, items=items, data_type="INT")

    @classmethod
    def boolean(
        cls, index: InputInteger = 0, items: Iterable[InputBoolean] = ()
    ) -> "IndexSwitch[BooleanSocket]":
        return IndexSwitch(index=index, items=items, data_type="BOOLEAN")

    @classmethod
    def vector(
        cls, index: InputInteger = 0, items: Iterable[InputVector] = ()
    ) -> "IndexSwitch[VectorSocket]":
        return IndexSwitch(index=index, items=items, data_type="VECTOR")

    @classmethod
    def color(
        cls, index: InputInteger = 0, items: Iterable[InputColor] = ()
    ) -> "IndexSwitch[ColorSocket]":
        return IndexSwitch(index=index, items=items, data_type="RGBA")

    @classmethod
    def rotation(
        cls, index: InputInteger = 0, items: Iterable[InputRotation] = ()
    ) -> "IndexSwitch[RotationSocket]":
        return IndexSwitch(index=index, items=items, data_type="ROTATION")

    @classmethod
    def matrix(
        cls, index: InputInteger = 0, items: Iterable[InputMatrix] = ()
    ) -> "IndexSwitch[MatrixSocket]":
        return IndexSwitch(index=index, items=items, data_type="MATRIX")

    @classmethod
    def string(
        cls, index: InputInteger = 0, items: Iterable[InputString] = ()
    ) -> "IndexSwitch[StringSocket]":
        return IndexSwitch(index=index, items=items, data_type="STRING")

    @classmethod
    def menu(
        cls, index: InputInteger = 0, items: Iterable[InputMenu] = ()
    ) -> "IndexSwitch[MenuSocket]":
        return IndexSwitch(index=index, items=items, data_type="MENU")

    @classmethod
    def object(
        cls, index: InputInteger = 0, items: Iterable[InputObject] = ()
    ) -> "IndexSwitch[ObjectSocket]":
        return IndexSwitch(index=index, items=items, data_type="OBJECT")

    @classmethod
    def geometry(
        cls, index: InputInteger = 0, items: Iterable[InputGeometry] = ()
    ) -> "IndexSwitch[GeometrySocket]":
        return IndexSwitch(index=index, items=items, data_type="GEOMETRY")

    @classmethod
    def collection(
        cls, index: InputInteger = 0, items: Iterable[InputCollection] = ()
    ) -> "IndexSwitch[CollectionSocket]":
        return IndexSwitch(index=index, items=items, data_type="COLLECTION")

    @classmethod
    def image(
        cls, index: InputInteger = 0, items: Iterable[InputImage] = ()
    ) -> "IndexSwitch[ImageSocket]":
        return IndexSwitch(index=index, items=items, data_type="IMAGE")

    @classmethod
    def material(
        cls, index: InputInteger = 0, items: Iterable[InputMaterial] = ()
    ) -> "IndexSwitch[MaterialSocket]":
        return IndexSwitch(index=index, items=items, data_type="MATERIAL")

    @classmethod
    def bundle(
        cls, index: InputInteger = 0, items: Iterable[InputBundle] = ()
    ) -> "IndexSwitch[BundleSocket]":
        return IndexSwitch(index=index, items=items, data_type="BUNDLE")

    @classmethod
    def closure(
        cls, index: InputInteger = 0, items: Iterable[InputClosure] = ()
    ) -> "IndexSwitch[ClosureSocket]":
        return IndexSwitch(index=index, items=items, data_type="CLOSURE")

    class _Inputs(SocketAccessor):
        index: IntegerSocket

    class _Outputs(SocketAccessor, Generic[_S]):
        output: _S

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> "_Outputs[_T]": ...

    def __init__(
        self,
        index: InputInteger = 0,
        items: Iterable[InputAny] = (),
        data_type: SOCKET_TYPES = "FLOAT",
    ):
        super().__init__()
        self.data_type = data_type
        key_args: dict[str, InputAny] = {"Index": index}
        self.node.index_switch_items.clear()
        self._link_args(*items)
        self._establish_links(**key_args)

    def _create_socket(self) -> NodeSocket:
        self.node.index_switch_items.new()
        # -1 is the last item (__extent__ socket) and -2 is the socket for the item we just added
        return self.node.inputs[-2]

    def _link_args(self, *args: InputAny):
        for arg in args:
            if _is_default_value(arg):
                socket = self._create_socket()
                socket.default_value = arg  # ty: ignore[unresolved-attribute]
            else:
                source = self._source_socket(arg)
                self.tree.link(source, self.node.inputs["__extend__"])

    @property
    def data_type(self) -> SOCKET_TYPES:
        """Input socket: Data Type"""
        return self.node.data_type  # ty: ignore[invalid-return-type]

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value


class _MenuSwitchBase(BaseNode, Generic[_T]):
    """Base class for MenuSwitch nodes across all tree types."""

    _bl_idname = "GeometryNodeMenuSwitch"
    node: bpy.types.GeometryNodeMenuSwitch

    class _Inputs(SocketAccessor):
        menu: MenuSocket

    class _Outputs(SocketAccessor, Generic[_S]):
        output: _S

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    def __init__(
        self,
        menu: InputMenu = None,
        items: Mapping[str, InputAny] = {},
        *,
        data_type: SOCKET_TYPES = "FLOAT",
    ):
        super().__init__()
        self.data_type = data_type
        self.node.enum_items.clear()
        key_args = {"Menu": menu}
        self._link_args(**items)
        self._establish_links(**key_args)
        if self.node.enum_items:
            self.node.inputs[0].default_value = self.node.enum_items[0].name  # type: ignore

    def _link_args(self, **kwargs: InputAny):
        for key, value in kwargs.items():
            if _is_default_value(value):
                socket = self._create_socket(key)
                socket.default_value = value  # type: ignore
            else:
                source = self._source_socket(value)  # type: ignore
                self._link(source, self.node.inputs["__extend__"])
                self.node.enum_items[-1].name = key

    def _create_socket(self, name: str) -> bpy.types.NodeSocket:
        self.node.enum_items.new(name)
        # -1 is the last item (__extent__ socket) and -2 is the socket for the item we just added
        return self.node.inputs[-2]

    @property
    def data_type(self) -> SOCKET_TYPES:
        """Input socket: Data Type"""
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value


class MenuSwitch(_MenuSwitchBase[_T], Generic[_T]):
    """Node builder for the Menu Switch node"""

    @classmethod
    def float(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputFloat] = {},
    ) -> "MenuSwitch[FloatSocket]":
        return MenuSwitch(menu, items, data_type="FLOAT")

    @classmethod
    def integer(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputInteger] = {},
    ) -> "MenuSwitch[IntegerSocket]":
        return MenuSwitch(menu, items, data_type="INT")

    @classmethod
    def boolean(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputBoolean] = {},
    ) -> "MenuSwitch[BooleanSocket]":
        return MenuSwitch(menu, items, data_type="BOOLEAN")

    @classmethod
    def vector(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputVector] = {},
    ) -> "MenuSwitch[VectorSocket]":
        return MenuSwitch(menu, items, data_type="VECTOR")

    @classmethod
    def color(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputColor] = {},
    ) -> "MenuSwitch[ColorSocket]":
        return MenuSwitch(menu, items, data_type="RGBA")

    @classmethod
    def rotation(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputRotation] = {},
    ) -> "MenuSwitch[RotationSocket]":
        return MenuSwitch(menu, items, data_type="ROTATION")

    @classmethod
    def matrix(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputMatrix] = {},
    ) -> "MenuSwitch[MatrixSocket]":
        return MenuSwitch(menu, items, data_type="MATRIX")

    @classmethod
    def string(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputString] = {},
    ) -> "MenuSwitch[StringSocket]":
        return MenuSwitch(menu, items, data_type="STRING")

    @classmethod
    def menu(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputMenu] = {},
    ) -> "MenuSwitch[MenuSocket]":
        return MenuSwitch(menu, items, data_type="MENU")

    @classmethod
    def object(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputObject] = {},
    ) -> "MenuSwitch[ObjectSocket]":
        return MenuSwitch(menu, items, data_type="OBJECT")

    @classmethod
    def geometry(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputGeometry] = {},
    ) -> "MenuSwitch[GeometrySocket]":
        return MenuSwitch(menu, items, data_type="GEOMETRY")

    @classmethod
    def collection(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputCollection] = {},
    ) -> "MenuSwitch[CollectionSocket]":
        return MenuSwitch(menu, items, data_type="COLLECTION")

    @classmethod
    def image(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputImage] = {},
    ) -> "MenuSwitch[ImageSocket]":
        return MenuSwitch(menu, items, data_type="IMAGE")

    @classmethod
    def material(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputMaterial] = {},
    ) -> "MenuSwitch[MaterialSocket]":
        return MenuSwitch(menu, items, data_type="MATERIAL")

    @classmethod
    def bundle(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputBundle] = {},
    ) -> "MenuSwitch[BundleSocket]":
        return MenuSwitch(menu, items, data_type="BUNDLE")

    @classmethod
    def closure(
        cls,
        menu: InputMenu = None,
        items: dict[str, InputClosure] = {},
    ) -> "MenuSwitch[ClosureSocket]":
        return MenuSwitch(menu, items, data_type="CLOSURE")


class CaptureAttribute(BaseNode, DynamicInputsMixin):
    """
    Store the result of a field on a geometry and output the data as a node socket.
    Allows remembering or interpolating data as the geometry changes,
    such as positions before deformation
    """

    _bl_idname = "GeometryNodeCaptureAttribute"
    node: bpy.types.GeometryNodeCaptureAttribute
    _socket_data_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
    )
    _type_map = {
        "VALUE": "FLOAT",
        # "VECTOR": "FLOAT_VECTOR",
        "RGBA": "FLOAT_COLOR",
        "ROTATION": "QUATERNION",
        "MATRIX": "FLOAT4X4",
    }

    class _DomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def __call__(
            self,
            geometry: InputGeometry = None,
            items: dict[str, InputLinkable] = {},
        ) -> "CaptureAttribute":
            """Create a CaptureAttribute node with a pre-set domain"""
            return CaptureAttribute(geometry=geometry, domain=self._domain, items=items)

    point = _DomainFactory("POINT")
    edge = _DomainFactory("EDGE")
    face = _DomainFactory("FACE")
    corner = _DomainFactory("CORNER")
    curve = _DomainFactory("CURVE")
    instance = _DomainFactory("INSTANCE")
    layer = _DomainFactory("LAYER")

    class _Inputs(SocketAccessor):
        geometry: GeometrySocket
        """Input geometry."""

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
        """Output geometry."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        geometry: InputGeometry = None,
        items: dict[str, InputLinkable] = {},
        *,
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry}
        self.domain = domain
        key_args.update(self._add_inputs(**items))
        self._establish_links(**key_args)

    def _add_socket(self, name: str, type: _AttributeDataTypes):
        item = self.node.capture_items.new(socket_type=type, name=name)
        return self.node.inputs[item.name]

    def capture(self, value: InputLinkable) -> SocketLinker:
        """Capture the value to store in the attribute

        Return the SocketLinker for the output socket
        """
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
        input_dict = self._add_inputs(value)
        self._establish_links(**input_dict)
        return SocketLinker(self.node.outputs[next(iter(input_dict))])

    @property
    def _items(self) -> bpy.types.NodeGeometryCaptureAttributeItems:
        return self.node.capture_items

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class FieldToGrid(DynamicInputsMixin, BaseNode, Generic[_T]):
    """Create new grids by evaluating new values on an existing volume grid topology



    Data types are inferred automatically from the closest compatible data type.

    Inputs:
    -------
    topology: InputLinkable
        The grid which contains the topology to evaluate the different fields on.
    items: dict[str, InputAny]
        The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket.
    data_type: _GridDataTypes = "FLOAT"
        The data type of the grid to evaluate on. Possible values are "FLOAT", "INT", "VECTOR", "BOOLEAN".

    """

    _bl_idname = "GeometryNodeFieldToGrid"
    node: bpy.types.GeometryNodeFieldToGrid
    _socket_data_types = ("VALUE", "INT", "VECTOR", "BOOLEAN")
    _type_map = {"VALUE": "FLOAT"}
    _default_input_id = "Topology"

    if TYPE_CHECKING:

        class _Inputs(SocketAccessor, Generic[_S]):
            topology: _S
            """The grid which contains the topology to evaluate the different fields on."""

        @property
        def i(self) -> _Inputs[_T]: ...

    def __init__(
        self,
        topology: InputGrid = None,
        items: dict[str, InputAny] = {},
        *,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        self.data_type = data_type
        key_args = {"Topology": topology}

        linkable = {k: v for k, v in items.items() if not _is_default_value(v)}
        defaults = {k: v for k, v in items.items() if _is_default_value(v)}

        key_args.update(self._add_inputs(**linkable))
        for name, value in defaults.items():
            self._add_socket(name=name, default_value=value)

        self._establish_links(**key_args)

    def _add_socket(
        self,
        name: str,
        type: _GridDataTypes = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.grid_items.new(socket_type=type, name=name)
        if default_value is not None:
            self.node.inputs[item.name].default_value = default_value  # ty: ignore[unresolved-attribute]
        return self.node.inputs[item.name]

    def capture(self, items: dict[str, InputAny]) -> list[SocketLinker]:
        outputs = {name: self.node.outputs[name] for name in self._add_inputs(**items)}

        return [_get_socket_linker(x) for x in outputs.values()]

    @classmethod
    def float(
        cls, topology: InputGrid = None, items: dict[str, InputAny] = {}
    ) -> "FieldToGrid[FloatSocket]":
        return FieldToGrid(topology, items, data_type="FLOAT")

    @classmethod
    def integer(
        cls, topology: InputGrid = None, items: dict[str, InputAny] = {}
    ) -> "FieldToGrid[IntegerSocket]":
        return FieldToGrid(topology, items, data_type="INT")

    @classmethod
    def vector(
        cls, topology: InputGrid = None, items: dict[str, InputAny] = {}
    ) -> "FieldToGrid[VectorSocket]":
        return FieldToGrid(topology, items, data_type="VECTOR")

    @classmethod
    def boolean(
        cls, topology: InputGrid = None, items: dict[str, InputAny] = {}
    ) -> "FieldToGrid[BooleanSocket]":
        return FieldToGrid(topology, items, data_type="BOOLEAN")

    @property
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class SDFGridBoolean(BaseNode):
    """Cut, subtract, or join multiple SDF volume grid inputs"""

    _bl_idname = "GeometryNodeSDFGridBoolean"
    node: bpy.types.GeometryNodeSDFGridBoolean

    class _Inputs(SocketAccessor):
        grid_1: SocketLinker
        """First SDF grid input."""
        grid_2: SocketLinker
        """Second SDF grid input."""

    class _Outputs(SocketAccessor):
        grid: SocketLinker
        """Resulting SDF grid."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self, *, operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE"
    ):
        super().__init__()
        self.operation = operation

    @classmethod
    def intersect(
        cls,
        grids: Iterable[InputGrid] = (),
    ) -> "SDFGridBoolean":
        node = cls(operation="INTERSECT")
        for grid in grids:
            assert grid
            node._link_from(*node._find_best_socket_pair(grid, node.i["Grid 2"]))
        return node

    @classmethod
    def union(
        cls,
        grids: Iterable[InputGrid] = (),
    ) -> "SDFGridBoolean":
        node = cls(operation="UNION")
        for grid in grids:
            assert grid
            node._link_from(*node._find_best_socket_pair(grid, node.i["Grid 2"]))
        return node

    @classmethod
    def difference(
        cls,
        grid_1: InputLinkable = None,
        grids: Iterable[InputGrid] = (),
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Difference'."""
        node = cls(operation="DIFFERENCE")
        if grid_1 is not None:
            node._link_from(*node._find_best_socket_pair(grid_1, node.i["Grid 1"]))
        for grid in grids:
            assert grid
            node._link_from(*node._find_best_socket_pair(grid, node.i["Grid 2"]))
        return node

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value


class AccumulateField(BaseNode, Generic[_T]):
    """Add the values of an evaluated field together and output the running total for each element"""

    _bl_idname = "GeometryNodeAccumulateField"
    node: bpy.types.GeometryNodeAccumulateField

    class AccumulateFieldDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self, value: InputFloat = None, index: InputInteger = 0
        ) -> "AccumulateField[FloatSocket]":
            return AccumulateField(value, index, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None, index: InputInteger = 0
        ) -> "AccumulateField[IntegerSocket]":
            return AccumulateField(value, index, domain=self._domain, data_type="INT")

        def vector(
            self, value: InputVector = None, index: InputInteger = 0
        ) -> "AccumulateField[VectorSocket]":
            return AccumulateField(
                value, index, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def transform(
            self, value: InputMatrix = None, index: InputInteger = 0
        ) -> "AccumulateField[MatrixSocket]":
            return AccumulateField(
                value, index, domain=self._domain, data_type="TRANSFORM"
            )

    point = AccumulateFieldDomainFactory("POINT")
    edge = AccumulateFieldDomainFactory("EDGE")
    face = AccumulateFieldDomainFactory("FACE")
    corner = AccumulateFieldDomainFactory("CORNER")
    spline = AccumulateFieldDomainFactory("CURVE")
    instance = AccumulateFieldDomainFactory("INSTANCE")
    layer = AccumulateFieldDomainFactory("LAYER")

    def __init__(
        self,
        value: InputFloat | InputInteger | InputVector | InputMatrix = 1.0,
        group_index: InputInteger = 0,
        *,
        data_type: _AccumulateFieldDataTypes = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value to accumulate."""
        group_index: IntegerSocket
        """Index used to group elements for accumulation."""

    class _Outputs(SocketAccessor, Generic[_S]):
        leading: _S
        """Running total before including the current element."""
        trailing: _S
        """Running total after including the current element."""
        total: _S
        """Total sum across the entire group."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    @property
    def data_type(self) -> _AccumulateFieldDataTypes:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: _AccumulateFieldDataTypes):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class EvaluateAtIndex(BaseNode, Generic[_T]):
    """Retrieve data of other elements in the context's geometry"""

    _bl_idname = "GeometryNodeFieldAtIndex"
    node: bpy.types.GeometryNodeFieldAtIndex

    class _EvaluateAtIndexDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self, value: InputFloat = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[FloatSocket]":
            return EvaluateAtIndex(value, index, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[IntegerSocket]":
            return EvaluateAtIndex(value, index, domain=self._domain, data_type="INT")

        def boolean(
            self, value: InputBoolean = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[BooleanSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="BOOLEAN"
            )

        def vector(
            self, value: InputVector = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[VectorSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def quaternion(
            self, value: InputRotation = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[RotationSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="QUATERNION"
            )

        def matrix(
            self, value: InputMatrix = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[MatrixSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="FLOAT4X4"
            )

    point = _EvaluateAtIndexDomainFactory("POINT")
    edge = _EvaluateAtIndexDomainFactory("EDGE")
    face = _EvaluateAtIndexDomainFactory("FACE")
    corner = _EvaluateAtIndexDomainFactory("CORNER")
    spline = _EvaluateAtIndexDomainFactory("CURVE")
    instance = _EvaluateAtIndexDomainFactory("INSTANCE")
    layer = _EvaluateAtIndexDomainFactory("LAYER")

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field to evaluate at the given index."""
        index: IntegerSocket
        """The index of the element to retrieve."""

    class _Outputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value at the given index."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    def __init__(
        self,
        value: InputFloat
        | InputInteger
        | InputBoolean
        | InputVector
        | InputRotation
        | InputMatrix = None,
        index: InputInteger = 0,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value, "Index": index}
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def data_type(
        self,
    ) -> _EvaluateAtIndexDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _EvaluateAtIndexDataTypes,
    ):
        self.node.data_type = value


class FieldAverage(BaseNode, Generic[_T]):
    """Calculate the mean and median of a given field"""

    _bl_idname = "GeometryNodeFieldAverage"
    node: bpy.types.GeometryNodeFieldAverage

    class _FieldAverageDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = 1.0,
            group_index: InputInteger = 0,
        ) -> "FieldAverage[FloatSocket]":
            """Create FieldAverage for the "FLOAT" data type"""
            return FieldAverage(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = (1.0, 1.0, 1.0),
            group_index: InputInteger = 0,
        ) -> "FieldAverage[VectorSocket]":
            """Create FieldAverage for the "FLOAT_VECTOR" data type"""
            return FieldAverage(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldAverageDomainFactory("POINT")
    edge = _FieldAverageDomainFactory("EDGE")
    face = _FieldAverageDomainFactory("FACE")
    corner = _FieldAverageDomainFactory("CORNER")
    spline = _FieldAverageDomainFactory("CURVE")
    instance = _FieldAverageDomainFactory("INSTANCE")
    layer = _FieldAverageDomainFactory("LAYER")

    def __init__(
        self,
        value: InputFloat | InputVector = None,
        group_index: InputFloat | InputVector = 0,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value to average."""
        group_index: IntegerSocket
        """Index used to group elements."""

    class _Outputs(SocketAccessor, Generic[_S]):
        mean: _S
        """The arithmetic mean of the field."""
        median: _S
        """The median value of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    @property
    def data_type(self) -> Literal["FLOAT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "FLOAT_VECTOR"]):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class FieldMinAndMax(BaseNode, Generic[_T]):
    """Calculate the minimum and maximum of a given field"""

    _bl_idname = "GeometryNodeFieldMinAndMax"
    node: bpy.types.GeometryNodeFieldMinAndMax

    class _FieldMinAndMaxDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = 1.0,
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[FloatSocket]":
            """Create FieldMinMax for the "FLOAT" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def integer(
            self,
            value: InputInteger = 1,
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[IntegerSocket]":
            """Create FieldMinMax for the "INT" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="INT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = (1.0, 1.0, 1.0),
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[VectorSocket]":
            """Create FieldMinMax for the "FLOAT_VECTOR" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldMinAndMaxDomainFactory("POINT")
    edge = _FieldMinAndMaxDomainFactory("EDGE")
    face = _FieldMinAndMaxDomainFactory("FACE")
    corner = _FieldMinAndMaxDomainFactory("CORNER")
    spline = _FieldMinAndMaxDomainFactory("CURVE")
    instance = _FieldMinAndMaxDomainFactory("INSTANCE")
    layer = _FieldMinAndMaxDomainFactory("LAYER")

    def __init__(
        self,
        value: InputFloat | InputVector | InputInteger = 1.0,
        group_index: InputInteger = 0,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value to find the min/max of."""
        group_index: IntegerSocket
        """Index used to group elements."""

    class _Outputs(SocketAccessor, Generic[_S]):
        min: _S
        """The minimum value of the field."""
        max: _S
        """The maximum value of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "FLOAT_VECTOR"]):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class EvaluateOnDomain(BaseNode, Generic[_T]):
    """Retrieve values from a field on a different domain besides the domain from the context"""

    _bl_idname = "GeometryNodeFieldOnDomain"
    node: bpy.types.GeometryNodeFieldOnDomain

    class _EvaluateOnDomainDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(self, value: InputFloat = None) -> "EvaluateOnDomain[FloatSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None
        ) -> "EvaluateOnDomain[IntegerSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="INT")

        def boolean(
            self, value: InputBoolean = None
        ) -> "EvaluateOnDomain[BooleanSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="BOOLEAN")

        def vector(self, value: InputVector = None) -> "EvaluateOnDomain[VectorSocket]":
            return EvaluateOnDomain(
                value, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def rotation(
            self, value: InputRotation = None
        ) -> "EvaluateOnDomain[RotationSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="QUATERNION")

        def matrix(self, value: InputMatrix = None) -> "EvaluateOnDomain[MatrixSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="FLOAT4X4")

    point = _EvaluateOnDomainDomainFactory("POINT")
    edge = _EvaluateOnDomainDomainFactory("EDGE")
    face = _EvaluateOnDomainDomainFactory("FACE")
    corner = _EvaluateOnDomainDomainFactory("CORNER")
    spline = _EvaluateOnDomainDomainFactory("CURVE")
    instance = _EvaluateOnDomainDomainFactory("INSTANCE")
    layer = _EvaluateOnDomainDomainFactory("LAYER")

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value to evaluate on a different domain."""

    class _Outputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value evaluated on the target domain."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    def __init__(
        self,
        value: InputFloat
        | InputVector
        | InputBoolean
        | InputInteger
        | InputRotation
        | InputMatrix = None,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value}
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def data_type(
        self,
    ) -> _EvaluateAtIndexDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _EvaluateAtIndexDataTypes,
    ):
        self.node.data_type = value


class FieldVariance(BaseNode, Generic[_T]):
    """Calculate the standard deviation and variance of a given field"""

    _bl_idname = "GeometryNodeFieldVariance"
    node: bpy.types.GeometryNodeFieldVariance

    class _FieldVarianceDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = None,
            group_index: InputInteger = None,
        ) -> "FieldVariance[FloatSocket]":
            """Create FieldVariance for the "FLOAT" data type"""
            return FieldVariance(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = None,
            group_index: InputInteger = None,
        ) -> "FieldVariance[VectorSocket]":
            """Create FieldVariance for the "FLOAT_VECTOR" data type"""
            return FieldVariance(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldVarianceDomainFactory("POINT")
    edge = _FieldVarianceDomainFactory("EDGE")
    face = _FieldVarianceDomainFactory("FACE")
    corner = _FieldVarianceDomainFactory("CORNER")
    spline = _FieldVarianceDomainFactory("CURVE")
    instance = _FieldVarianceDomainFactory("INSTANCE")
    layer = _FieldVarianceDomainFactory("LAYER")

    class _Inputs(SocketAccessor, Generic[_S]):
        value: _S
        """The field value to calculate variance of."""
        group_index: IntegerSocket
        """Index used to group elements."""

    class _Outputs(SocketAccessor, Generic[_S]):
        standard_deviation: _S
        """The standard deviation of the field."""
        variance: _S
        """The variance of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> "_Outputs[_T]": ...

    def __init__(
        self,
        value: InputFloat | InputVector = None,
        group_index: InputInteger = None,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def data_type(self) -> Literal["FLOAT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "FLOAT_VECTOR"]):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


_CompareOperations = Literal[
    "LESS_THAN",
    "LESS_EQUAL",
    "GREATER_THAN",
    "GREATER_EQUAL",
    "EQUAL",
    "NOT_EQUAL",
    "BRIGHTER",
    "DARKER",
]

_CompareDataTypes = Literal[
    "FLOAT",
    "INT",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "STRING",
]

_CompareVectorModes = Literal[
    "ELEMENT", "LENGTH", "AVERAGE", "DOT_PRODUCT", "DIRECTION"
]


class Compare(BaseNode, Generic[_T]):
    """Perform a comparison operation on the two given inputs"""

    _bl_idname = "FunctionNodeCompare"
    node: bpy.types.FunctionNodeCompare

    class _FloatFactory:
        @staticmethod
        def less_than(
            a: InputFloat = 0.0, b: InputFloat = 0.0
        ) -> "Compare[FloatSocket]":
            return Compare(operation="LESS_THAN", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def less_equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0
        ) -> "Compare[FloatSocket]":
            return Compare(operation="LESS_EQUAL", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def greater_than(
            a: InputFloat = 0.0, b: InputFloat = 0.0
        ) -> "Compare[FloatSocket]":
            return Compare(operation="GREATER_THAN", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def greater_equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0
        ) -> "Compare[FloatSocket]":
            return Compare(operation="GREATER_EQUAL", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0, epsilon: InputFloat = 0.0001
        ) -> "Compare[FloatSocket]":
            return Compare(
                operation="EQUAL", data_type="FLOAT", A=a, B=b, Epsilon=epsilon
            )

        @staticmethod
        def not_equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0, epsilon: InputFloat = 0.0001
        ) -> "Compare[FloatSocket]":
            return Compare(
                operation="NOT_EQUAL", data_type="FLOAT", A=a, B=b, Epsilon=epsilon
            )

    class _IntegerFactory:
        @staticmethod
        def less_than(
            a: InputInteger = 0, b: InputInteger = 0
        ) -> "Compare[IntegerSocket]":
            return Compare(operation="LESS_THAN", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def less_equal(
            a: InputInteger = 0, b: InputInteger = 0
        ) -> "Compare[IntegerSocket]":
            return Compare(operation="LESS_EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def greater_than(
            a: InputInteger = 0, b: InputInteger = 0
        ) -> "Compare[IntegerSocket]":
            return Compare(operation="GREATER_THAN", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def greater_equal(
            a: InputInteger = 0, b: InputInteger = 0
        ) -> "Compare[IntegerSocket]":
            return Compare(operation="GREATER_EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def equal(a: InputInteger = 0, b: InputInteger = 0) -> "Compare[IntegerSocket]":
            return Compare(operation="EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def not_equal(
            a: InputInteger = 0, b: InputInteger = 0
        ) -> "Compare[IntegerSocket]":
            return Compare(operation="NOT_EQUAL", data_type="INT", A_INT=a, B_INT=b)

    class _VectorFactory:
        @staticmethod
        def _make(
            operation: _CompareOperations,
            a: InputVector,
            b: InputVector,
            mode: _CompareVectorModes,
            c: InputFloat,
            angle: InputFloat,
            epsilon: InputFloat,
        ) -> "Compare[VectorSocket]":
            kwargs: dict = {
                "operation": operation,
                "data_type": "VECTOR",
                "mode": mode,
                "A_VEC3": a,
                "B_VEC3": b,
            }
            if operation in ("EQUAL", "NOT_EQUAL") and epsilon is not None:
                kwargs["Epsilon"] = epsilon
            if mode == "DIRECTION" and angle is not None:
                kwargs["Angle"] = angle
            elif mode == "DOT_PRODUCT" and c is not None:
                kwargs["C"] = c
            return Compare(**kwargs)

        @staticmethod
        def less_than(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make("LESS_THAN", a, b, mode, c, angle, None)

        @staticmethod
        def less_equal(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make(
                "LESS_EQUAL", a, b, mode, c, angle, None
            )

        @staticmethod
        def greater_than(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make(
                "GREATER_THAN", a, b, mode, c, angle, None
            )

        @staticmethod
        def greater_equal(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make(
                "GREATER_EQUAL", a, b, mode, c, angle, None
            )

        @staticmethod
        def equal(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
            epsilon: InputFloat = 0.0001,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make("EQUAL", a, b, mode, c, angle, epsilon)

        @staticmethod
        def not_equal(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
            epsilon: InputFloat = 0.0001,
        ) -> "Compare[VectorSocket]":
            return Compare._VectorFactory._make(
                "NOT_EQUAL", a, b, mode, c, angle, epsilon
            )

    class _ColorFactory:
        @staticmethod
        def brighter(
            a: InputColor = None, b: InputColor = None
        ) -> "Compare[ColorSocket]":
            return Compare(operation="BRIGHTER", data_type="RGBA", A_COL=a, B_COL=b)

        @staticmethod
        def darker(
            a: InputColor = None, b: InputColor = None
        ) -> "Compare[ColorSocket]":
            return Compare(operation="DARKER", data_type="RGBA", A_COL=a, B_COL=b)

        @staticmethod
        def equal(
            a: InputColor = None, b: InputColor = None, epsilon: InputFloat = 0.0001
        ) -> "Compare[ColorSocket]":
            return Compare(
                operation="EQUAL", data_type="RGBA", A_COL=a, B_COL=b, Epsilon=epsilon
            )

        @staticmethod
        def not_equal(
            a: InputColor = None, b: InputColor = None, epsilon: InputFloat = 0.0001
        ) -> "Compare[ColorSocket]":
            return Compare(
                operation="NOT_EQUAL",
                data_type="RGBA",
                A_COL=a,
                B_COL=b,
                Epsilon=epsilon,
            )

    class _StringFactory:
        @staticmethod
        def equal(a: InputString = "", b: InputString = "") -> "Compare[StringSocket]":
            return Compare(operation="EQUAL", data_type="STRING", A_STR=a, B_STR=b)

        @staticmethod
        def not_equal(
            a: InputString = "", b: InputString = ""
        ) -> "Compare[StringSocket]":
            return Compare(operation="NOT_EQUAL", data_type="STRING", A_STR=a, B_STR=b)

    float = _FloatFactory()
    integer = _IntegerFactory()
    vector = _VectorFactory()
    color = _ColorFactory()
    string = _StringFactory()

    class _Inputs(SocketAccessor, Generic[_S]):
        _bpy_node: "bpy.types.FunctionNodeCompare"

        @property
        def a(self) -> _S:
            """Input socket: A"""
            return self._get("A{}".format(Compare._suffix(self._bpy_node.data_type)))  # type: ignore[return-value]

        @property
        def b(self) -> _S:
            """Input socket: B"""
            return self._get("B{}".format(Compare._suffix(self._bpy_node.data_type)))  # type: ignore[return-value]

        c: FloatSocket
        epsilon: FloatSocket
        angle: FloatSocket

    class _Outputs(SocketAccessor):
        result: BooleanSocket
        """Boolean result of the comparison."""

    @property
    def i(self) -> "_Inputs":  # type: ignore[override]
        accessor = Compare._Inputs(self.node.inputs, "input")
        accessor._bpy_node = self.node
        return accessor

    if TYPE_CHECKING:

        @property  # type: ignore[override]
        def i(self) -> "_Inputs[_T]": ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        operation: _CompareOperations = "GREATER_THAN",
        data_type: _CompareDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        self.data_type = data_type
        self.operation = operation
        if self.data_type == "VECTOR":
            self.mode = kwargs.pop("mode")
        self._establish_links(**kwargs)

    def switch(self, false: InputAny, true: InputAny) -> Switch:
        def _infer_data_type(
            a: InputAny, b: InputAny
        ) -> Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ]:
            # Check plain Python types first (most specific to least)
            # bool must come before int since bool is a subclass of int
            has_str = isinstance(a, str) or isinstance(b, str)
            has_numeric = isinstance(a, (int, float)) or isinstance(b, (int, float))

            # Reject mixing string with numeric types
            if has_str and has_numeric:
                raise ValueError(
                    f"Cannot infer compatible type from {type(a).__name__} and {type(b).__name__}"
                )

            has_float = isinstance(a, float) or isinstance(b, float)
            has_bool = isinstance(a, bool) or isinstance(b, bool)
            has_int = isinstance(a, int) or isinstance(b, int)

            set_types = [
                x._default_output_socket.type
                for x in (a, b)
                if hasattr(x, "_default_output_socket")
            ]
            if set_types:
                value = set_types[0]
                match value:
                    case "VALUE":
                        return "FLOAT"
                    case "INT":
                        # A float literal should promote INT to FLOAT
                        return "FLOAT" if has_float else "INT"
                    case _:
                        return value

            if has_float:
                return "FLOAT"
            if has_bool:
                return "BOOLEAN"
            if has_int:
                return "INT"
            if has_str:
                return "STRING"

            raise ValueError(f"Cannot infer compatible type from {a} and {b}")

        method = _infer_data_type(false, true).lower()
        if method == "int":
            method = "integer"
        return getattr(Switch, method)(switch=self, false=false, true=true)

    @staticmethod
    def _suffix(data_type: str) -> str:
        suffix_lookup = {
            "FLOAT": "",
            "INT": "_INT",
            "VECTOR": "_VEC3",
            "RGBA": "_COL",
            "STRING": "_STR",
        }
        return suffix_lookup[data_type]

    @property
    def operation(
        self,
    ) -> _CompareOperations:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: _CompareOperations,
    ):
        self.node.operation = value

    @property
    def data_type(
        self,
    ) -> _CompareDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _CompareDataTypes,
    ):
        self.node.data_type = value

    @property
    def mode(
        self,
    ) -> _CompareVectorModes:
        return self.node.mode

    @mode.setter
    def mode(
        self,
        value: _CompareVectorModes,
    ):
        self.node.mode = value


class AttributeStatistic(BaseNode, Generic[_T]):
    """Calculate statistics about a data set from a field evaluated on a geometry"""

    _bl_idname = "GeometryNodeAttributeStatistic"
    node: bpy.types.GeometryNodeAttributeStatistic

    class _AttributeStatisticDomainFactor:
        def __init__(
            self,
            domain: Literal[
                "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
            ],
        ):
            self._domain = domain

        def float(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = None,
            attribute: InputFloat = None,
        ) -> "AttributeStatistic[FloatSocket]":
            """Create FieldMinMax for the "FLOAT" data type"""
            return AttributeStatistic(
                geometry, selection, attribute, data_type="FLOAT", domain=self._domain
            )

        def vector(
            self,
            geometry: InputGeometry = None,
            selection: InputBoolean = None,
            attribute: InputVector = None,
        ) -> "AttributeStatistic[VectorSocket]":
            """Create FieldMinMax for the "FLOAT_VECTOR" data type"""
            return AttributeStatistic(
                geometry,
                selection,
                attribute,
                data_type="FLOAT_VECTOR",
                domain=self._domain,
            )

    point = _AttributeStatisticDomainFactor("POINT")
    edge = _AttributeStatisticDomainFactor("EDGE")
    face = _AttributeStatisticDomainFactor("FACE")
    corner = _AttributeStatisticDomainFactor("CORNER")
    spline = _AttributeStatisticDomainFactor("CURVE")
    instance = _AttributeStatisticDomainFactor("INSTANCE")
    layer = _AttributeStatisticDomainFactor("LAYER")

    class _Inputs(SocketAccessor, Generic[_S]):
        geometry: GeometrySocket
        """The geometry whose attribute to analyze."""
        selection: BooleanSocket
        """Limits which elements are included in the statistics."""
        attribute: _S
        """The field to calculate statistics for."""

    class _Outputs(SocketAccessor, Generic[_S]):
        mean: _S
        """The arithmetic mean."""
        median: _S
        """The median value."""
        sum: _S
        """The sum of all values."""
        min: _S
        """The minimum value."""
        max: _S
        """The maximum value."""
        range: _S
        """The range (max - min)."""
        standard_deviation: _S
        """The standard deviation."""
        variance: _S
        """The variance."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        geometry: InputGeometry = None,
        selection: InputBoolean = True,
        attribute: InputFloat | InputVector = None,
        *,
        data_type: Literal[
            "FLOAT",
            "FLOAT_VECTOR",
        ] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Attribute": attribute,
        }
        key_args.update(kwargs)
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "FLOAT_VECTOR",
    ]:
        return self.node.data_type  # ty: ignore[invalid-return-type]

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "FLOAT_VECTOR",
        ],
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


_SampleCurveDataTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "FLOAT_VECTOR",
    "FLOAT_COLOR",
    "QUATERNION",
    "FLOAT4X4",
]


class SampleCurve(BaseNode, Generic[_T]):
    """
    Retrieve data from a point on a curve at a certain distance from its start

    Parameters
    ----------
    curves : InputGeometry
        Curves
    value : InputFloat
        Value
    factor : InputFloat
        Factor
    length : InputFloat
        Length
    curve_index : InputInteger
        Curve Index

    Inputs
    ------
    i.curves : GeometrySocket
        Curves
    i.value : FloatSocket
        Value
    i.factor : FloatSocket
        Factor
    i.length : FloatSocket
        Length
    i.curve_index : IntegerSocket
        Curve Index

    Outputs
    -------
    o.value : FloatSocket
        Value
    o.position : VectorSocket
        Position
    o.tangent : VectorSocket
        Tangent
    o.normal : VectorSocket
        Normal
    """

    class _SampleCurveFactorFactory:
        def float(
            self,
            curves: InputGeometry = None,
            value: InputFloat = 0.0,
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[FloatSocket]":
            """Create Sample Curve with operation 'Float'. Floating-point value"""
            return SampleCurve(
                data_type="FLOAT",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def integer(
            self,
            curves: InputGeometry = None,
            value: InputInteger = 0,
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[IntegerSocket]":
            """Create Sample Curve with operation 'Integer'. Integer value"""
            return SampleCurve(
                data_type="INT",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def boolean(
            self,
            curves: InputGeometry = None,
            value: InputBoolean = False,
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[BooleanSocket]":
            """Create Sample Curve with operation 'Boolean'. Boolean value"""
            return SampleCurve(
                data_type="BOOLEAN",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def vector(
            self,
            curves: InputGeometry = None,
            value: InputVector = (0.0, 0.0, 0.0),
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[VectorSocket]":
            """Create Sample Curve with operation 'Vector'. Vector value"""
            return SampleCurve(
                data_type="FLOAT_VECTOR",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def color(
            self,
            curves: InputGeometry = None,
            value: InputColor = (0.0, 0.0, 0.0, 0.0),
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[VectorSocket]":
            """Create Sample Curve with operation 'Color'. Color value"""
            return SampleCurve(
                data_type="FLOAT_COLOR",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def quaternion(
            self,
            curves: InputGeometry = None,
            value: InputRotation = (0.0, 0.0, 0.0),
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[RotationSocket]":
            """Create Sample Curve with operation 'Quaternion'. Quaternion value"""
            return SampleCurve(
                data_type="QUATERNION",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

        def matrix(
            self,
            curves: InputGeometry = None,
            value: InputMatrix = None,
            factor: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[MatrixSocket]":
            """Create Sample Curve with operation 'Matrix'. Matrix value"""
            return SampleCurve(
                data_type="FLOAT4X4",
                curves=curves,
                value=value,
                factor=factor,
                curve_index=curve_index,
                mode="FACTOR",
                use_all_curves=use_all_curves,
            )

    class _SampleCurveLengthFactory:
        def float(
            self,
            curves: InputGeometry = None,
            value: InputFloat = 0.0,
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[FloatSocket]":
            """Create Sample Curve with operation 'Float'. Floating-point value"""
            return SampleCurve(
                data_type="FLOAT",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def integer(
            self,
            curves: InputGeometry = None,
            value: InputInteger = 0,
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[IntegerSocket]":
            """Create Sample Curve with operation 'Integer'. Integer value"""
            return SampleCurve(
                data_type="INT",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def boolean(
            self,
            curves: InputGeometry = None,
            value: InputBoolean = False,
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[BooleanSocket]":
            """Create Sample Curve with operation 'Boolean'. Boolean value"""
            return SampleCurve(
                data_type="BOOLEAN",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def vector(
            self,
            curves: InputGeometry = None,
            value: InputVector = (0.0, 0.0, 0.0),
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[VectorSocket]":
            """Create Sample Curve with operation 'Vector'. Vector value"""
            return SampleCurve(
                data_type="FLOAT_VECTOR",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def color(
            self,
            curves: InputGeometry = None,
            value: InputColor = (0.0, 0.0, 0.0, 0.0),
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[VectorSocket]":
            """Create Sample Curve with operation 'Color'. Color value"""
            return SampleCurve(
                data_type="FLOAT_COLOR",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def quaternion(
            self,
            curves: InputGeometry = None,
            value: InputRotation = (0.0, 0.0, 0.0),
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[RotationSocket]":
            """Create Sample Curve with operation 'Quaternion'. Quaternion value"""
            return SampleCurve(
                data_type="QUATERNION",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

        def matrix(
            self,
            curves: InputGeometry = None,
            value: InputMatrix = None,
            length: InputFloat = 0.0,
            curve_index: InputInteger = 0,
            *,
            use_all_curves: bool = False,
        ) -> "SampleCurve[MatrixSocket]":
            """Create Sample Curve with operation 'Matrix'. Matrix value"""
            return SampleCurve(
                data_type="FLOAT4X4",
                curves=curves,
                value=value,
                length=length,
                curve_index=curve_index,
                mode="LENGTH",
                use_all_curves=use_all_curves,
            )

    length = _SampleCurveLengthFactory()
    factor = _SampleCurveFactorFactory()

    _bl_idname = "GeometryNodeSampleCurve"
    node: bpy.types.GeometryNodeSampleCurve

    class _Inputs(SocketAccessor, Generic[_S]):
        curves: GeometrySocket
        """Curves"""
        value: _S
        """Value"""
        factor: FloatSocket
        """Factor"""
        length: FloatSocket
        """Length"""
        curve_index: IntegerSocket
        """Curve Index"""

    class _Outputs(SocketAccessor, Generic[_S]):
        value: _S
        """Value"""
        position: VectorSocket
        """Position"""
        tangent: VectorSocket
        """Tangent"""
        normal: VectorSocket
        """Normal"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        curves: InputGeometry = None,
        value: InputAny = 0.0,
        factor: InputFloat = 0.0,
        length: InputFloat = 0.0,
        curve_index: InputInteger = 0,
        *,
        mode: Literal["FACTOR", "LENGTH"] = "FACTOR",
        use_all_curves: bool = False,
        data_type: _SampleCurveDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Curves": curves,
            "Value": value,
            "Factor": factor,
            "Length": length,
            "Curve Index": curve_index,
        }
        self.mode = mode
        self.use_all_curves = use_all_curves
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def mode(self) -> Literal["FACTOR", "LENGTH"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["FACTOR", "LENGTH"]):
        self.node.mode = value

    @property
    def use_all_curves(self) -> bool:
        return self.node.use_all_curves

    @use_all_curves.setter
    def use_all_curves(self, value: bool):
        self.node.use_all_curves = value

    @property
    def data_type(
        self,
    ) -> _SampleCurveDataTypes:
        return self.node.data_type  # ty: ignore[invalid-return-type]

    @data_type.setter
    def data_type(
        self,
        value: _SampleCurveDataTypes,
    ):
        self.node.data_type = value


class SampleIndex(BaseNode, Generic[_T]):
    """
    Retrieve values from specific geometry elements

    Parameters
    ----------
    geometry : InputGeometry
        Geometry
    value : InputFloat
        Value
    index : InputInteger
        Index

    Inputs
    ------
    i.geometry : GeometrySocket
        Geometry
    i.value : FloatSocket
        Value
    i.index : IntegerSocket
        Index

    Outputs
    -------
    o.value : FloatSocket
        Value
    """

    class _SampleIndexDomainFactory:
        def __init__(
            self,
            domain: _AttributeDomains,
        ):
            self._domain = domain

        def float(
            self,
            geometry: InputGeometry = None,
            value: InputFloat = 0.0,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[FloatSocket]":
            """Create Sample Index with operation 'Float'. Floating-point value"""
            return SampleIndex(
                data_type="FLOAT",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def integer(
            self,
            geometry: InputGeometry = None,
            value: InputInteger = 0,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[IntegerSocket]":
            """Create Sample Index with operation 'Integer'. 32-bit integer"""
            return SampleIndex(
                data_type="INT",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def boolean(
            self,
            geometry: InputGeometry = None,
            value: InputBoolean = False,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[BooleanSocket]":
            """Create Sample Index with operation 'Boolean'. True or false"""
            return SampleIndex(
                data_type="BOOLEAN",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def vector(
            self,
            geometry: InputGeometry = None,
            value: InputVector = None,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[VectorSocket]":
            """Create Sample Index with operation 'Vector'. 3D vector with floating-point values"""
            return SampleIndex(
                data_type="FLOAT_VECTOR",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def color(
            self,
            geometry: InputGeometry = None,
            value: InputColor = None,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[ColorSocket]":
            """Create Sample Index with operation 'Color'. RGBA color with 32-bit floating-point values"""
            return SampleIndex(
                data_type="FLOAT_COLOR",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def quaternion(
            self,
            geometry: InputGeometry = None,
            value: InputRotation = None,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[RotationSocket]":
            """Create Sample Index with operation 'Quaternion'. Floating point quaternion rotation"""
            return SampleIndex(
                data_type="QUATERNION",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

        def matrix(
            self,
            geometry: InputGeometry = None,
            value: InputMatrix = None,
            index: InputInteger = 0,
            *,
            clamp: bool = False,
        ) -> "SampleIndex[MatrixSocket]":
            """Create Sample Index with operation '4x4 Matrix'. Floating point matrix"""
            return SampleIndex(
                data_type="FLOAT4X4",
                geometry=geometry,
                value=value,
                index=index,
                domain=self._domain,
                clamp=clamp,
            )

    point = _SampleIndexDomainFactory("POINT")
    edge = _SampleIndexDomainFactory("EDGE")
    face = _SampleIndexDomainFactory("FACE")
    face_corner = _SampleIndexDomainFactory("CORNER")
    spline = _SampleIndexDomainFactory("CURVE")
    instance = _SampleIndexDomainFactory("INSTANCE")
    layer = _SampleIndexDomainFactory("LAYER")

    _bl_idname = "GeometryNodeSampleIndex"
    node: bpy.types.GeometryNodeSampleIndex

    class _Inputs(SocketAccessor, Generic[_S]):
        geometry: GeometrySocket
        """Geometry"""
        value: _S
        """Value"""
        index: IntegerSocket
        """Index"""

    class _Outputs(SocketAccessor, Generic[_S]):
        value: _S
        """Value"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        geometry: InputGeometry = None,
        value: InputAny = 0.0,
        index: InputInteger = 0,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        clamp: bool = False,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Value": value, "Index": index}
        self.data_type = data_type
        self.domain = domain
        self.clamp = clamp
        self._establish_links(**key_args)

    @property
    def data_type(
        self,
    ) -> _SampleCurveDataTypes:
        return self.node.data_type  # ty: ignore[invalid-return-type]

    @data_type.setter
    def data_type(
        self,
        value: _SampleCurveDataTypes,
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def clamp(self) -> bool:
        return self.node.clamp

    @clamp.setter
    def clamp(self, value: bool):
        self.node.clamp = value
