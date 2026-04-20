from typing import TYPE_CHECKING, Any, Literal

import bpy
from bpy.types import NodeSocket

from nodebpy.builder.accessor import SocketAccessor
from nodebpy.builder.interface import SocketGeometry

from ...builder import (
    BaseNode as NodeBuilder,
)
from ...builder import (
    DynamicInputsMixin,
    Socket,
    SocketBoolean,
    SocketCollection,
    SocketColor,
    SocketFloat,
    SocketInteger,
    SocketMaterial,
    SocketMenu,
    SocketObject,
    SocketString,
    SocketVector,
    TreeBuilder,
)
from ...builder import (
    Socket as SocketLinker,
)
from ...types import (
    SOCKET_TYPES,
    InputAny,
    InputBoolean,
    InputColor,
    InputFloat,
    InputGeometry,
    InputGrid,
    InputInteger,
    InputLinkable,
    InputMatrix,
    InputMenu,
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
from .converter import Switch
from .zone import (
    ForEachGeometryElementInput,
    ForEachGeometryElementOutput,
    ForEachGeometryElementZone,
    RepeatInput,
    RepeatOutput,
    RepeatZone,
    SimulationInput,
    SimulationOutput,
    SimulationZone,
)

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
    "Value",
    "AccumulateField",
    "EvaluateAtIndex",
    "FieldAverage",
    "FieldMinAndMax",
    "EvaluateOnDomain",
    "FieldVariance",
    "Compare",
    "AttributeStatistic",
)


def tree(
    name: str = "Geometry Node Group",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
) -> TreeBuilder:
    return TreeBuilder.geometry(name, collapse=collapse, arrange=arrange)


class Bake(NodeBuilder, DynamicInputsMixin):
    """Cache the incoming data so that it can be used without recomputation

    TODO: properly handle Animation / Still bake opations and ability to bake to a file
    """

    _bl_idname = "GeometryNodeBake"
    node: bpy.types.GeometryNodeBake
    _socket_data_types = _BakedDataTypeValues

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._establish_links(**self._add_inputs(*args, **kwargs))

    def _add_socket(  # type: ignore
        self, name: str, type: _BakeDataTypes, default_value: Any | None = None
    ):
        item = self.node.bake_items.new(socket_type=type, name=name)
        return self.node.inputs[item.name]


class GeometryToInstance(NodeBuilder):
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
        geometry: SocketGeometry

    class _Outputs(SocketAccessor):
        instances: SocketGeometry

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


class Collection(NodeBuilder):
    """
    Output a single collection
    """

    _bl_idname = "GeometryNodeInputCollection"
    node: bpy.types.GeometryNodeInputCollection

    class _Outputs(SocketAccessor):
        collection: SocketCollection

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


class Material(NodeBuilder):
    """
    Output a single material
    """

    _bl_idname = "GeometryNodeInputMaterial"
    node: bpy.types.GeometryNodeInputMaterial

    class _Outputs(SocketAccessor):
        material: SocketMaterial

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


class Object(NodeBuilder):
    """
    Output a single object
    """

    _bl_idname = "GeometryNodeInputObject"
    node: bpy.types.GeometryNodeInputObject

    class _Outputs(SocketAccessor):
        object: SocketObject

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


class Value(NodeBuilder):
    """Input numerical values to other nodes in the tree"""

    _bl_idname = "ShaderNodeValue"
    node: bpy.types.ShaderNodeValue

    class _Outputs(SocketAccessor):
        value: SocketFloat

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


### === ###


class FormatString(NodeBuilder, DynamicInputsMixin):
    """Insert values into a string using a Python and path template compatible formatting syntax"""

    _bl_idname = "FunctionNodeFormatString"
    node: bpy.types.FunctionNodeFormatString
    _socket_data_types = ("VALUE", "INT", "STRING")
    _type_map = {
        "VALUE": "FLOAT",
    }

    class _Inputs(SocketAccessor):
        format: SocketString
        input_socket: SocketLinker

    class _Outputs(SocketAccessor):
        string: SocketString

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(
        self,
        *args,
        format: InputString = "",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Format": format}
        key_args.update(self._add_inputs(*args, **kwargs))  # type: ignore
        self._establish_links(**key_args)

    def _add_socket(  # type: ignore
        self,
        name: str,
        type: Literal["FLOAT", "INT", "STRING"] = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.format_items.new(socket_type=type, name=name)
        if default_value is not None:
            try:
                self.node.inputs[item.name].default_value = default_value  # type: ignore
            except TypeError as e:
                raise ValueError(
                    f"Invalid default value for {type}: {default_value}"
                ) from e
        return self.node.inputs[item.name]

    @property
    def items(self) -> dict[str, SocketLinker]:
        """Input sockets:"""
        return {
            socket.name: self.inputs._get(socket.name) for socket in self.node.inputs
        }


class JoinStrings(NodeBuilder):
    """Combine any number of input strings"""

    _bl_idname = "GeometryNodeStringJoin"
    node: bpy.types.GeometryNodeStringJoin

    class _Outputs(SocketAccessor):
        string: SocketString

    class _Inputs(SocketAccessor):
        delimiter: SocketString
        strings: SocketString

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...
        @property
        def i(self) -> _Inputs: ...

    def __init__(self, *args: InputLinkable, delimiter: InputString = ""):
        super().__init__()

        self._establish_links(Delimiter=delimiter)
        for arg in args:
            self._link_from(arg, "Strings")


class MeshBoolean(NodeBuilder):
    """Cut, subtract, or join multiple mesh inputs"""

    _bl_idname = "GeometryNodeMeshBoolean"
    node: bpy.types.GeometryNodeMeshBoolean

    class _Inputs(SocketAccessor):
        mesh_1: SocketGeometry
        mesh_2: SocketGeometry

    class _Outputs(SocketAccessor):
        geometry: SocketGeometry
        intersecting_edges: SocketGeometry

    def __init__(
        self,
        *args: InputGeometry,
        operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE",
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {}
        key_args.update(kwargs)
        self.operation = operation
        self.solver = solver
        for arg in args:
            self._link_from(arg, "Mesh 2")
        self._establish_links(**key_args)

    @classmethod
    def intersect(
        cls,
        *args: InputGeometry,
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="INTERSECT",
        )

    @classmethod
    def union(
        cls,
        *args: InputGeometry,
        hole_tolerant: InputBoolean = False,
        self_intersection: InputBoolean = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="UNION",
        )

    @classmethod
    def difference(
        cls,
        *args: InputGeometry,
        mesh_1: InputGeometry = None,
        hole_tolerant: InputBoolean = False,
        self_intersection: InputBoolean = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ) -> "MeshBoolean":
        key_args = {}
        key_args["Mesh 1"] = mesh_1
        if solver == "EXACT":
            key_args["self_intersection"] = self_intersection
            key_args["hole_tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="DIFFERENCE",
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


class JoinGeometry(NodeBuilder):
    """Merge separately generated geometries into a single one"""

    _bl_idname = "GeometryNodeJoinGeometry"
    node: bpy.types.GeometryNodeJoinGeometry

    class _Inputs(SocketAccessor):
        geometry: SocketGeometry

    class _Outputs(SocketAccessor):
        geometry: SocketGeometry

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(self, *args: InputLinkable):
        super().__init__()
        for source in reversed(args):
            assert source
            self._link(*self._find_best_socket_pair(source, self))


class SetHandleType(NodeBuilder):
    """Set the handle type for the control points of a Bézier curve"""

    _bl_idname = "GeometryNodeCurveSetHandles"
    node: bpy.types.GeometryNodeCurveSetHandles

    class _Inputs(SocketAccessor):
        curve: SocketGeometry
        selection: SocketBoolean

    class _Outputs(SocketAccessor):
        curve: SocketGeometry

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


class HandleTypeSelection(NodeBuilder):
    """Provide a selection based on the handle types of Bézier control points"""

    _bl_idname = "GeometryNodeCurveHandleTypeSelection"
    node: bpy.types.GeometryNodeCurveHandleTypeSelection

    class _Outputs(SocketAccessor):
        selection: SocketBoolean

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


class IndexSwitch(NodeBuilder):
    """Node builder for the Index Switch node"""

    _bl_idname = "GeometryNodeIndexSwitch"
    node: bpy.types.GeometryNodeIndexSwitch

    @staticmethod
    def _typed(data_type: SOCKET_TYPES):
        @classmethod
        def method(cls, *args: InputAny, index: InputInteger = 0) -> "IndexSwitch":
            """Create an IndexSwitch node with a pre-set data_type"""
            return cls(*args, index=index, data_type=data_type)

        return method

    float = _typed("FLOAT")
    integer = _typed("INT")
    boolean = _typed("BOOLEAN")
    vector = _typed("VECTOR")
    color = _typed("RGBA")
    rotation = _typed("ROTATION")
    matrix = _typed("MATRIX")
    string = _typed("STRING")
    menu = _typed("MENU")
    object = _typed("OBJECT")
    geometry = _typed("GEOMETRY")
    collection = _typed("COLLECTION")
    image = _typed("IMAGE")
    material = _typed("MATERIAL")
    bundle = _typed("BUNDLE")
    closure = _typed("CLOSURE")

    class _Inputs(SocketAccessor):
        index: SocketInteger

    class _Outputs(SocketAccessor):
        output: Socket

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        *args: InputAny,
        index: InputInteger = 0,
        data_type: SOCKET_TYPES = "FLOAT",
    ):
        super().__init__()
        self.data_type = data_type
        key_args: dict[str, InputAny] = {"Index": index}
        self.node.index_switch_items.clear()
        self._link_args(*args)
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
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value


class _MenuSwitchBase(NodeBuilder):
    """Base class for MenuSwitch nodes across all tree types."""

    _bl_idname = "GeometryNodeMenuSwitch"
    node: bpy.types.GeometryNodeMenuSwitch

    @staticmethod
    def _typed(data_type: SOCKET_TYPES):
        @classmethod
        def method(
            cls,
            *args: InputAny,
            menu: InputMenu = None,
            **kwargs: InputAny,
        ) -> "MenuSwitch":
            """Create a MenuSwitch node with a pre-set data_type"""
            return cls(*args, menu=menu, data_type=data_type, **kwargs)

        return method

    class _Inputs(SocketAccessor):
        menu: SocketMenu

    @property
    def i(self) -> "MenuSwitch._Inputs":
        return MenuSwitch._Inputs(self.node.inputs, "input")

    class _Outputs(SocketAccessor):
        output: Socket

    @property
    def o(self) -> "MenuSwitch._Outputs":
        return MenuSwitch._Outputs(self.node.outputs, "output")

    def __init__(
        self,
        *args: InputAny,
        menu: InputMenu = None,
        data_type: SOCKET_TYPES = "FLOAT",
        **kwargs: InputAny,
    ):
        super().__init__()
        self.data_type = data_type
        self.node.enum_items.clear()
        key_args = {"Menu": menu}
        self._link_args(*args, **kwargs)
        self._establish_links(**key_args)
        if self.node.enum_items:
            self.node.inputs[0].default_value = self.node.enum_items[0].name  # type: ignore

    def _link_args(self, *args: InputAny, **kwargs: InputAny):
        for arg in args:
            if _is_default_value(arg):
                socket = self._create_socket(f"Input_{len(self.node.enum_items)}")
                socket.default_value = arg  # type: ignore
            else:
                source = self._source_socket(arg)
                self.tree.link(source, self.node.inputs["__extend__"])

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


class MenuSwitch(_MenuSwitchBase):
    """Node builder for the Menu Switch node"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    rotation = _MenuSwitchBase._typed("ROTATION")
    matrix = _MenuSwitchBase._typed("MATRIX")
    string = _MenuSwitchBase._typed("STRING")
    menu = _MenuSwitchBase._typed("MENU")
    object = _MenuSwitchBase._typed("OBJECT")
    geometry = _MenuSwitchBase._typed("GEOMETRY")
    collection = _MenuSwitchBase._typed("COLLECTION")
    image = _MenuSwitchBase._typed("IMAGE")
    material = _MenuSwitchBase._typed("MATERIAL")
    bundle = _MenuSwitchBase._typed("BUNDLE")
    closure = _MenuSwitchBase._typed("CLOSURE")


class CaptureAttribute(NodeBuilder, DynamicInputsMixin):
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

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        @classmethod
        def method(
            cls,
            *args: InputLinkable,
            geometry: InputGeometry = None,
            **kwargs,
        ) -> "CaptureAttribute":
            """Create a CaptureAttribute node with a pre-set domain"""
            return cls(*args, geometry=geometry, domain=domain, **kwargs)

        return method

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    curve = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

    class _Inputs(SocketAccessor):
        geometry: SocketGeometry
        """Input geometry."""

    class _Outputs(SocketAccessor):
        geometry: SocketGeometry
        """Output geometry."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        *args: InputLinkable,
        geometry: InputGeometry = None,
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry}
        self.domain = domain
        key_args.update(self._add_inputs(*args, **kwargs))
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


class FieldToGrid(DynamicInputsMixin, NodeBuilder):
    """Create new grids by evaluating new values on an existing volume grid topology

    New socket items for field evaluation are first created from *args then **kwargs to give specific names to the items.

    Data types are inferred automatically from the closest compatible data type.

    Inputs:
    -------
    topology: InputLinkable
        The grid which contains the topology to evaluate the different fields on.
    data_type: _GridDataTypes = "FLOAT"
        The data type of the grid to evaluate on. Possible values are "FLOAT", "INT", "VECTOR", "BOOLEAN".
    *args: InputFloat | InputVector | InputInteger | InputBoolean
        The fields to evaluate on the grid.
    **kwargs: dict[str, InputFloat | InputVector | InputInteger | InputGeometry]
        The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket.

    """

    _bl_idname = "GeometryNodeFieldToGrid"
    node: bpy.types.GeometryNodeFieldToGrid
    _socket_data_types = ("VALUE", "INT", "VECTOR", "BOOLEAN")
    _type_map = {"VALUE": "FLOAT"}
    _default_input_id = "Topology"

    def __init__(
        self,
        *args: InputGrid,
        topology: InputGrid = None,
        data_type: _GridDataTypes = "FLOAT",
        **kwargs: InputGrid,
    ):
        super().__init__()
        self.data_type = data_type
        key_args = {"Topology": topology}

        linkable = {k: v for k, v in kwargs.items() if not _is_default_value(v)}
        defaults = {k: v for k, v in kwargs.items() if _is_default_value(v)}

        key_args.update(self._add_inputs(*args, **linkable))
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

    def capture(self, *args, **kwargs) -> list[SocketLinker]:
        outputs = {
            name: self.node.outputs[name] for name in self._add_inputs(*args, **kwargs)
        }

        return [SocketLinker(x) for x in outputs.values()]

    @classmethod
    def float(cls, *args: InputGrid, topology: InputGrid = None, **kwargs):
        return cls(*args, data_type="FLOAT", topology=topology, **kwargs)

    @classmethod
    def integer(cls, *args: InputGrid, topology: InputGrid = None, **kwargs):
        return cls(*args, data_type="INT", topology=topology, **kwargs)

    @classmethod
    def vector(cls, *args: InputGrid, topology: InputGrid = None, **kwargs):
        return cls(*args, data_type="VECTOR", topology=topology, **kwargs)

    @classmethod
    def boolean(cls, *args: InputGrid, topology: InputGrid = None, **kwargs):
        return cls(*args, data_type="BOOLEAN", topology=topology, **kwargs)

    class _Inputs(SocketAccessor):
        topology: SocketLinker
        """The grid which contains the topology to evaluate the different fields on."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

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


class SDFGridBoolean(NodeBuilder):
    """Cut, subtract, or join multiple SDF volume grid inputs"""

    _bl_idname = "GeometryNodeSDFGridBoolean"
    node: bpy.types.GeometryNodeSDFGridBoolean

    def __init__(
        self, *, operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE"
    ):
        super().__init__()
        self.operation = operation

    @classmethod
    def intersect(
        cls,
        *args: InputLinkable,
    ) -> "SDFGridBoolean":
        node = cls(operation="INTERSECT")
        for arg in args:
            if arg is None:
                continue
            node._link_from(*node._find_best_socket_pair(arg, node.inputs["Grid 2"]))
        return node

    @classmethod
    def union(
        cls,
        *args: InputLinkable,
    ) -> "SDFGridBoolean":
        node = cls(operation="UNION")
        for arg in args:
            if arg is None:
                continue
            node._link_from(*node._find_best_socket_pair(arg, node.inputs["Grid 2"]))
        return node

    @classmethod
    def difference(
        cls,
        *args: InputLinkable,
        grid_1: InputLinkable = None,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Difference'."""
        node = cls(operation="DIFFERENCE")
        if grid_1 is not None:
            node._link_from(*node._find_best_socket_pair(grid_1, node.inputs["Grid 1"]))
        for arg in args:
            if arg is None:
                continue
            node._link_from(*node._find_best_socket_pair(arg, node.inputs["Grid 2"]))
        return node

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

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value


class AccumulateField(NodeBuilder):
    """Add the values of an evaluated field together and output the running total for each element"""

    _bl_idname = "GeometryNodeAccumulateField"
    node: bpy.types.GeometryNodeAccumulateField

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class AccumulateFieldDomainFactory:
            @staticmethod
            def float(
                value: InputFloat = None, index: InputInteger = 0
            ) -> "AccumulateField":
                return AccumulateField(value, index, domain=domain, data_type="FLOAT")

            @staticmethod
            def integer(
                value: InputInteger = None, index: InputInteger = 0
            ) -> "AccumulateField":
                return AccumulateField(value, index, domain=domain, data_type="INT")

            @staticmethod
            def vector(
                value: InputVector = None, index: InputInteger = 0
            ) -> "AccumulateField":
                return AccumulateField(
                    value, index, domain=domain, data_type="FLOAT_VECTOR"
                )

            @staticmethod
            def transform(
                value: InputMatrix = None, index: InputInteger = 0
            ) -> "AccumulateField":
                return AccumulateField(
                    value, index, domain=domain, data_type="TRANSFORM"
                )

        return AccumulateFieldDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

    def __init__(
        self,
        value: InputFloat | InputInteger | InputVector | InputMatrix = 1.0,
        group_index: InputInteger = 0,
        *,
        data_type: _AccumulateFieldDataTypes = "FLOAT",
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        key_args.update(kwargs)
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    class _Inputs(SocketAccessor):
        value: SocketLinker
        """The field value to accumulate."""
        group_index: SocketInteger
        """Index used to group elements for accumulation."""

    class _Outputs(SocketAccessor):
        leading: SocketLinker
        """Running total before including the current element."""
        trailing: SocketLinker
        """Running total after including the current element."""
        total: SocketLinker
        """Total sum across the entire group."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class EvaluateAtIndex(NodeBuilder):
    """Retrieve data of other elements in the context's geometry"""

    _bl_idname = "GeometryNodeFieldAtIndex"
    node: bpy.types.GeometryNodeFieldAtIndex

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class EvaluateAtIndexDomainFactory:
            @staticmethod
            def float(value: InputFloat = None, index: InputInteger = 0):
                return EvaluateAtIndex(value, index, domain=domain, data_type="FLOAT")

            @staticmethod
            def integer(value: InputInteger = None, index: InputInteger = 0):
                return EvaluateAtIndex(value, index, domain=domain, data_type="INT")

            @staticmethod
            def boolean(value: InputBoolean = None, index: InputInteger = 0):
                return EvaluateAtIndex(value, index, domain=domain, data_type="BOOLEAN")

            @staticmethod
            def vector(value: InputVector = None, index: InputInteger = 0):
                return EvaluateAtIndex(
                    value, index, domain=domain, data_type="FLOAT_VECTOR"
                )

            @staticmethod
            def rotation(value: InputRotation = None, index: InputInteger = 0):
                return EvaluateAtIndex(
                    value, index, domain=domain, data_type="QUATERNION"
                )

            @staticmethod
            def transform(value: InputMatrix = None, index: InputInteger = 0):
                return EvaluateAtIndex(
                    value, index, domain=domain, data_type="FLOAT4X4"
                )

        return EvaluateAtIndexDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

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

    class _Inputs(SocketAccessor):
        value: SocketLinker
        """The field to evaluate at the given index."""
        index: SocketInteger
        """The index of the element to retrieve."""

    class _Outputs(SocketAccessor):
        value: SocketLinker
        """The field value at the given index."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class FieldAverage(NodeBuilder):
    """Calculate the mean and median of a given field"""

    _bl_idname = "GeometryNodeFieldAverage"
    node: bpy.types.GeometryNodeFieldAverage

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class FieldAverageDomainFactory:
            @staticmethod
            def float(
                value: InputFloat = 1.0,
                group_index: InputInteger = 0,
            ) -> "FieldAverage":
                """Create FieldAverage for the "FLOAT" data type"""
                return FieldAverage(
                    value, group_index, data_type="FLOAT", domain=domain
                )

            @staticmethod
            def vector(
                value: InputVector = (1.0, 1.0, 1.0),
                group_index: InputInteger = 0,
            ) -> "FieldAverage":
                """Create FieldAverage for the "FLOAT_VECTOR" data type"""
                return FieldAverage(
                    value, group_index, data_type="FLOAT_VECTOR", domain=domain
                )

        return FieldAverageDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

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

    class _Inputs(SocketAccessor):
        value: SocketLinker
        """The field value to average."""
        group_index: SocketInteger
        """Index used to group elements."""

    class _Outputs(SocketAccessor):
        mean: SocketLinker
        """The arithmetic mean of the field."""
        median: SocketLinker
        """The median value of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class FieldMinAndMax(NodeBuilder):
    """Calculate the minimum and maximum of a given field"""

    _bl_idname = "GeometryNodeFieldMinAndMax"
    node: bpy.types.GeometryNodeFieldMinAndMax

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class FieldMinMaxDomainFactory:
            @staticmethod
            def float(
                value: InputFloat = 1.0,
                group_index: InputInteger = 0,
            ) -> "FieldMinAndMax":
                """Create FieldMinMax for the "FLOAT" data type"""
                return FieldMinAndMax(
                    value, group_index, data_type="FLOAT", domain=domain
                )

            @staticmethod
            def integer(
                value: InputInteger = 1,
                group_index: InputInteger = 0,
            ) -> "FieldMinAndMax":
                """Create FieldMinMax for the "INT" data type"""
                return FieldMinAndMax(
                    value, group_index, data_type="INT", domain=domain
                )

            @staticmethod
            def vector(
                value: InputVector = (1.0, 1.0, 1.0),
                group_index: InputInteger = 0,
            ) -> "FieldMinAndMax":
                """Create FieldMinMax for the "FLOAT_VECTOR" data type"""
                return FieldMinAndMax(
                    value, group_index, data_type="FLOAT_VECTOR", domain=domain
                )

        return FieldMinMaxDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

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

    class _Inputs(SocketAccessor):
        value: SocketLinker
        """The field value to find the min/max of."""
        group_index: SocketInteger
        """Index used to group elements."""

    class _Outputs(SocketAccessor):
        min: SocketLinker
        """The minimum value of the field."""
        max: SocketLinker
        """The maximum value of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class EvaluateOnDomain(NodeBuilder):
    """Retrieve values from a field on a different domain besides the domain from the context"""

    _bl_idname = "GeometryNodeFieldOnDomain"
    node: bpy.types.GeometryNodeFieldOnDomain

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class EvaluateOnDomainDomainFactory:
            @staticmethod
            def float(value: InputFloat = None):
                return EvaluateOnDomain(value, domain=domain, data_type="FLOAT")

            @staticmethod
            def integer(value: InputInteger = None):
                return EvaluateOnDomain(value, domain=domain, data_type="INT")

            @staticmethod
            def boolean(value: InputBoolean = None):
                return EvaluateOnDomain(value, domain=domain, data_type="BOOLEAN")

            @staticmethod
            def vector(value: InputVector = None):
                return EvaluateOnDomain(value, domain=domain, data_type="FLOAT_VECTOR")

            @staticmethod
            def rotation(value: InputRotation = None):
                return EvaluateOnDomain(value, domain=domain, data_type="QUATERNION")

            @staticmethod
            def transform(value: InputMatrix = None):
                return EvaluateOnDomain(value, domain=domain, data_type="FLOAT4X4")

        return EvaluateOnDomainDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

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

    class _Inputs(SocketAccessor):
        value: (
            InputFloat
            | InputVector
            | InputBoolean
            | InputInteger
            | InputRotation
            | InputMatrix
        )
        """The field value to evaluate on a different domain."""

    class _Outputs(SocketAccessor):
        value: (
            InputFloat
            | InputVector
            | InputBoolean
            | InputInteger
            | InputRotation
            | InputMatrix
        )
        """The field value evaluated on the target domain."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class FieldVariance(NodeBuilder):
    """Calculate the standard deviation and variance of a given field"""

    _bl_idname = "GeometryNodeFieldVariance"
    node: bpy.types.GeometryNodeFieldVariance

    @staticmethod
    def _domain_factory(domain: _AttributeDomains):
        class FieldVarianceDomainFactory:
            @staticmethod
            def float(
                value: InputFloat = None,
                group_index: InputInteger = None,
            ) -> "FieldVariance":
                """Create FieldVariance for the "FLOAT" data type"""
                return FieldVariance(
                    value, group_index, data_type="FLOAT", domain=domain
                )

            @staticmethod
            def vector(
                value: InputVector = None,
                group_index: InputInteger = None,
            ) -> "FieldVariance":
                """Create FieldVariance for the "FLOAT_VECTOR" data type"""
                return FieldVariance(
                    value, group_index, data_type="FLOAT_VECTOR", domain=domain
                )

        return FieldVarianceDomainFactory()

    point = _domain_factory("POINT")
    edge = _domain_factory("EDGE")
    face = _domain_factory("FACE")
    corner = _domain_factory("CORNER")
    spline = _domain_factory("CURVE")
    instance = _domain_factory("INSTANCE")
    layer = _domain_factory("LAYER")

    class _Inputs(SocketAccessor):
        value: SocketFloat | SocketVector
        """The field value to calculate variance of."""
        group_index: SocketInteger
        """Index used to group elements."""

    class _Outputs(SocketAccessor):
        standard_deviation: SocketFloat | SocketVector
        """The standard deviation of the field."""
        variance: SocketFloat | SocketVector
        """The variance of the field."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class Compare(NodeBuilder):
    """Perform a comparison operation on the two given inputs"""

    _bl_idname = "FunctionNodeCompare"
    node: bpy.types.FunctionNodeCompare

    class _FloatFactory:
        @staticmethod
        def less_than(a: InputFloat = 0.0, b: InputFloat = 0.0) -> "Compare":
            return Compare(operation="LESS_THAN", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def less_equal(a: InputFloat = 0.0, b: InputFloat = 0.0) -> "Compare":
            return Compare(operation="LESS_EQUAL", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def greater_than(a: InputFloat = 0.0, b: InputFloat = 0.0) -> "Compare":
            return Compare(operation="GREATER_THAN", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def greater_equal(a: InputFloat = 0.0, b: InputFloat = 0.0) -> "Compare":
            return Compare(operation="GREATER_EQUAL", data_type="FLOAT", A=a, B=b)

        @staticmethod
        def equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0, epsilon: InputFloat = 0.0001
        ) -> "Compare":
            return Compare(
                operation="EQUAL", data_type="FLOAT", A=a, B=b, Epsilon=epsilon
            )

        @staticmethod
        def not_equal(
            a: InputFloat = 0.0, b: InputFloat = 0.0, epsilon: InputFloat = 0.0001
        ) -> "Compare":
            return Compare(
                operation="NOT_EQUAL", data_type="FLOAT", A=a, B=b, Epsilon=epsilon
            )

    class _IntegerFactory:
        @staticmethod
        def less_than(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
            return Compare(operation="LESS_THAN", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def less_equal(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
            return Compare(operation="LESS_EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def greater_than(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
            return Compare(operation="GREATER_THAN", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def greater_equal(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
            return Compare(operation="GREATER_EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def equal(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
            return Compare(operation="EQUAL", data_type="INT", A_INT=a, B_INT=b)

        @staticmethod
        def not_equal(a: InputInteger = 0, b: InputInteger = 0) -> "Compare":
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
        ) -> "Compare":
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
        ) -> "Compare":
            return Compare._VectorFactory._make("LESS_THAN", a, b, mode, c, angle, None)

        @staticmethod
        def less_equal(
            a: InputVector = (0.0, 0.0, 0.0),
            b: InputVector = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: InputFloat = None,
            angle: InputFloat = None,
        ) -> "Compare":
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
        ) -> "Compare":
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
        ) -> "Compare":
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
        ) -> "Compare":
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
        ) -> "Compare":
            return Compare._VectorFactory._make(
                "NOT_EQUAL", a, b, mode, c, angle, epsilon
            )

    class _ColorFactory:
        @staticmethod
        def brighter(a: InputColor = None, b: InputColor = None) -> "Compare":
            return Compare(operation="BRIGHTER", data_type="RGBA", A_COL=a, B_COL=b)

        @staticmethod
        def darker(a: InputColor = None, b: InputColor = None) -> "Compare":
            return Compare(operation="DARKER", data_type="RGBA", A_COL=a, B_COL=b)

        @staticmethod
        def equal(
            a: InputColor = None, b: InputColor = None, epsilon: InputFloat = 0.0001
        ) -> "Compare":
            return Compare(
                operation="EQUAL", data_type="RGBA", A_COL=a, B_COL=b, Epsilon=epsilon
            )

        @staticmethod
        def not_equal(
            a: InputColor = None, b: InputColor = None, epsilon: InputFloat = 0.0001
        ) -> "Compare":
            return Compare(
                operation="NOT_EQUAL",
                data_type="RGBA",
                A_COL=a,
                B_COL=b,
                Epsilon=epsilon,
            )

    class _StringFactory:
        @staticmethod
        def equal(a: InputString = "", b: InputString = "") -> "Compare":
            return Compare(operation="EQUAL", data_type="STRING", A_STR=a, B_STR=b)

        @staticmethod
        def not_equal(a: InputString = "", b: InputString = "") -> "Compare":
            return Compare(operation="NOT_EQUAL", data_type="STRING", A_STR=a, B_STR=b)

    float = _FloatFactory()
    integer = _IntegerFactory()
    vector = _VectorFactory()
    color = _ColorFactory()
    string = _StringFactory()

    class _Inputs(SocketAccessor):
        _bpy_node: "bpy.types.FunctionNodeCompare"

        @property
        def a(self) -> SocketFloat | SocketVector | SocketColor:
            """Input socket: A"""
            return self._get("A{}".format(Compare._suffix(self._bpy_node.data_type)))  # ty: ignore[invalid-return-type]

        @property
        def b(self) -> SocketFloat | SocketVector | SocketColor:
            """Input socket: B"""
            return self._get("B{}".format(Compare._suffix(self._bpy_node.data_type)))  # ty: ignore[invalid-return-type]

        c: SocketFloat
        epsilon: SocketFloat
        angle: SocketFloat

    class _Outputs(SocketAccessor):
        result: SocketBoolean
        """Boolean result of the comparison."""

    @property
    def i(self) -> _Inputs:  # type: ignore[override]
        accessor = Compare._Inputs(self.node.inputs, "input")
        accessor._bpy_node = self.node
        return accessor

    if TYPE_CHECKING:

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


class AttributeStatistic(NodeBuilder):
    """Calculate statistics about a data set from a field evaluated on a geometry"""

    _bl_idname = "GeometryNodeAttributeStatistic"
    node: bpy.types.GeometryNodeAttributeStatistic

    def __init__(
        self,
        geometry: InputGeometry = None,
        selection: InputBoolean = True,
        attribute: InputLinkable = None,
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

    class _Inputs(SocketAccessor):
        geometry: SocketGeometry
        """The geometry whose attribute to analyze."""
        selection: SocketBoolean
        """Limits which elements are included in the statistics."""
        attribute: SocketFloat | SocketVector
        """The field to calculate statistics for."""

    class _Outputs(SocketAccessor):
        mean: SocketFloat | SocketVector
        """The arithmetic mean."""
        median: SocketFloat | SocketVector
        """The median value."""
        sum: SocketFloat | SocketVector
        """The sum of all values."""
        min: SocketFloat | SocketVector
        """The minimum value."""
        max: SocketFloat | SocketVector
        """The maximum value."""
        range: SocketFloat | SocketVector
        """The range (max - min)."""
        standard_deviation: SocketFloat | SocketVector
        """The standard deviation."""
        variance: SocketFloat | SocketVector
        """The variance."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "FLOAT_VECTOR",
    ]:
        return self.node.data_type  # type: ignore

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
