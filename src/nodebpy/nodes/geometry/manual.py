from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

import bpy
from bpy.types import NodeEvaluateClosure, NodeSocket

from ...builder import (
    BaseNode,
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    DynamicInputsMixin,
    FloatSocket,
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
from .converter import Switch
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
)


def tree(
    name: str = "Geometry Node Group",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
) -> TreeBuilder:
    return TreeBuilder.geometry(name, collapse=collapse, arrange=arrange)


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
        *args,
        format: InputString = "",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Format": format}
        key_args.update(self._add_inputs(*args, **kwargs))
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

    def __init__(self, *args: InputLinkable, delimiter: InputString = ""):
        super().__init__()

        self._establish_links(Delimiter=delimiter)
        for arg in args:
            self._link_from(arg, "Strings")


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
            operation="UNION",
        )

    @classmethod
    def difference(
        cls,
        *args: InputGeometry,
        mesh_1: InputGeometry = None,
        self_intersection: InputBoolean = False,
        hole_tolerant: InputBoolean = False,
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

    def __init__(self, *args: InputLinkable):
        super().__init__()
        for source in reversed(args):
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
        cls, *args: InputFloat, index: InputInteger = 0
    ) -> "IndexSwitch[FloatSocket]":
        return IndexSwitch(*args, index=index, data_type="FLOAT")

    @classmethod
    def integer(
        cls, *args: InputInteger, index: InputInteger = 0
    ) -> "IndexSwitch[IntegerSocket]":
        return IndexSwitch(*args, index=index, data_type="INT")

    @classmethod
    def boolean(
        cls, *args: InputBoolean, index: InputInteger = 0
    ) -> "IndexSwitch[BooleanSocket]":
        return IndexSwitch(*args, index=index, data_type="BOOLEAN")

    @classmethod
    def vector(
        cls, *args: InputVector, index: InputInteger = 0
    ) -> "IndexSwitch[VectorSocket]":
        return IndexSwitch(*args, index=index, data_type="VECTOR")

    @classmethod
    def color(
        cls, *args: InputColor, index: InputInteger = 0
    ) -> "IndexSwitch[ColorSocket]":
        return IndexSwitch(*args, index=index, data_type="RGBA")

    @classmethod
    def rotation(
        cls, *args: InputRotation, index: InputInteger = 0
    ) -> "IndexSwitch[RotationSocket]":
        return IndexSwitch(*args, index=index, data_type="ROTATION")

    @classmethod
    def matrix(
        cls, *args: InputMatrix, index: InputInteger = 0
    ) -> "IndexSwitch[MatrixSocket]":
        return IndexSwitch(*args, index=index, data_type="MATRIX")

    @classmethod
    def string(
        cls, *args: InputString, index: InputInteger = 0
    ) -> "IndexSwitch[StringSocket]":
        return IndexSwitch(*args, index=index, data_type="STRING")

    @classmethod
    def menu(
        cls, *args: InputMenu, index: InputInteger = 0
    ) -> "IndexSwitch[MenuSocket]":
        return IndexSwitch(*args, index=index, data_type="MENU")

    @classmethod
    def object(
        cls, *args: InputObject, index: InputInteger = 0
    ) -> "IndexSwitch[ObjectSocket]":
        return IndexSwitch(*args, index=index, data_type="OBJECT")

    @classmethod
    def geometry(
        cls, *args: InputGeometry, index: InputInteger = 0
    ) -> "IndexSwitch[GeometrySocket]":
        return IndexSwitch(*args, index=index, data_type="GEOMETRY")

    @classmethod
    def collection(
        cls, *args: InputCollection, index: InputInteger = 0
    ) -> "IndexSwitch[CollectionSocket]":
        return IndexSwitch(*args, index=index, data_type="COLLECTION")

    @classmethod
    def image(
        cls, *args: InputImage, index: InputInteger = 0
    ) -> "IndexSwitch[ImageSocket]":
        return IndexSwitch(*args, index=index, data_type="IMAGE")

    @classmethod
    def material(
        cls, *args: InputMaterial, index: InputInteger = 0
    ) -> "IndexSwitch[MaterialSocket]":
        return IndexSwitch(*args, index=index, data_type="MATERIAL")

    @classmethod
    def bundle(
        cls, *args: InputBundle, index: InputInteger = 0
    ) -> "IndexSwitch[BundleSocket]":
        return IndexSwitch(*args, index=index, data_type="BUNDLE")

    @classmethod
    def closure(
        cls, *args: InputClosure, index: InputInteger = 0
    ) -> "IndexSwitch[ClosureSocket]":
        return IndexSwitch(*args, index=index, data_type="CLOSURE")

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


class MenuSwitch(_MenuSwitchBase[_T], Generic[_T]):
    """Node builder for the Menu Switch node"""

    @classmethod
    def float(
        cls, *args: InputFloat, menu: InputMenu = None, **kwargs: InputFloat
    ) -> "MenuSwitch[FloatSocket]":
        return MenuSwitch(*args, menu=menu, data_type="FLOAT", **kwargs)

    @classmethod
    def integer(
        cls, *args: InputInteger, menu: InputMenu = None, **kwargs: InputInteger
    ) -> "MenuSwitch[IntegerSocket]":
        return MenuSwitch(*args, menu=menu, data_type="INT", **kwargs)

    @classmethod
    def boolean(
        cls, *args: InputBoolean, menu: InputMenu = None, **kwargs: InputBoolean
    ) -> "MenuSwitch[BooleanSocket]":
        return MenuSwitch(*args, menu=menu, data_type="BOOLEAN", **kwargs)

    @classmethod
    def vector(
        cls, *args: InputVector, menu: InputMenu = None, **kwargs: InputVector
    ) -> "MenuSwitch[VectorSocket]":
        return MenuSwitch(*args, menu=menu, data_type="VECTOR", **kwargs)

    @classmethod
    def color(
        cls, *args: InputColor, menu: InputMenu = None, **kwargs: InputColor
    ) -> "MenuSwitch[ColorSocket]":
        return MenuSwitch(*args, menu=menu, data_type="RGBA", **kwargs)

    @classmethod
    def rotation(
        cls, *args: InputRotation, menu: InputMenu = None, **kwargs: InputRotation
    ) -> "MenuSwitch[RotationSocket]":
        return MenuSwitch(*args, menu=menu, data_type="ROTATION", **kwargs)

    @classmethod
    def matrix(
        cls, *args: InputMatrix, menu: InputMenu = None, **kwargs: InputMatrix
    ) -> "MenuSwitch[MatrixSocket]":
        return MenuSwitch(*args, menu=menu, data_type="MATRIX", **kwargs)

    @classmethod
    def string(
        cls, *args: InputString, menu: InputMenu = None, **kwargs: InputString
    ) -> "MenuSwitch[StringSocket]":
        return MenuSwitch(*args, menu=menu, data_type="STRING", **kwargs)

    @classmethod
    def menu(
        cls, *args: InputMenu, menu: InputMenu = None, **kwargs: InputMenu
    ) -> "MenuSwitch[MenuSocket]":
        return MenuSwitch(*args, menu=menu, data_type="MENU", **kwargs)

    @classmethod
    def object(
        cls, *args: InputObject, menu: InputMenu = None, **kwargs: InputObject
    ) -> "MenuSwitch[ObjectSocket]":
        return MenuSwitch(*args, menu=menu, data_type="OBJECT", **kwargs)

    @classmethod
    def geometry(
        cls, *args: InputGeometry, menu: InputMenu = None, **kwargs: InputGeometry
    ) -> "MenuSwitch[GeometrySocket]":
        return MenuSwitch(*args, menu=menu, data_type="GEOMETRY", **kwargs)

    @classmethod
    def collection(
        cls, *args: InputCollection, menu: InputMenu = None, **kwargs: InputCollection
    ) -> "MenuSwitch[CollectionSocket]":
        return MenuSwitch(*args, menu=menu, data_type="COLLECTION", **kwargs)

    @classmethod
    def image(
        cls, *args: InputImage, menu: InputMenu = None, **kwargs: InputImage
    ) -> "MenuSwitch[ImageSocket]":
        return MenuSwitch(*args, menu=menu, data_type="IMAGE", **kwargs)

    @classmethod
    def material(
        cls, *args: InputMaterial, menu: InputMenu = None, **kwargs: InputMaterial
    ) -> "MenuSwitch[MaterialSocket]":
        return MenuSwitch(*args, menu=menu, data_type="MATERIAL", **kwargs)

    @classmethod
    def bundle(
        cls, *args: InputBundle, menu: InputMenu = None, **kwargs: InputBundle
    ) -> "MenuSwitch[BundleSocket]":
        return MenuSwitch(*args, menu=menu, data_type="BUNDLE", **kwargs)

    @classmethod
    def closure(
        cls, *args: InputClosure, menu: InputMenu = None, **kwargs: InputClosure
    ) -> "MenuSwitch[ClosureSocket]":
        return MenuSwitch(*args, menu=menu, data_type="CLOSURE", **kwargs)


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
            *args: InputLinkable,
            geometry: InputGeometry = None,
            **kwargs,
        ) -> "CaptureAttribute":
            """Create a CaptureAttribute node with a pre-set domain"""
            return CaptureAttribute(
                *args, geometry=geometry, domain=self._domain, **kwargs
            )

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


class FieldToGrid(DynamicInputsMixin, BaseNode):
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


class SDFGridBoolean(BaseNode):
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
            node._link_from(*node._find_best_socket_pair(arg, node.i["Grid 2"]))
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
            node._link_from(*node._find_best_socket_pair(arg, node.i["Grid 2"]))
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
            node._link_from(*node._find_best_socket_pair(grid_1, node.i["Grid 1"]))
        for arg in args:
            if arg is None:
                continue
            node._link_from(*node._find_best_socket_pair(arg, node.i["Grid 2"]))
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
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        key_args.update(kwargs)
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

        def rotation(
            self, value: InputRotation = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[RotationSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="QUATERNION"
            )

        def transform(
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

        def transform(
            self, value: InputMatrix = None
        ) -> "EvaluateOnDomain[MatrixSocket]":
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

        def rotation(
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

        def rotation(
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

        def rotation(
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
