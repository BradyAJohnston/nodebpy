from typing import Any, Literal

import bpy

from ..builder import NodeBuilder, NodeSocket, SocketLinker
from ..types import (
    LINKABLE,
    SOCKET_TYPES,
    TYPE_INPUT_ALL,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_DATA,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_GRID,
    TYPE_INPUT_INT,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_MENU,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
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
    "GeometryToInstance",
    "SDFGridBoolean",
    #
    "SetHandleType",
    "HandleTypeSelection",
    "IndexSwitch",
    "MenuSwitch",
    "CaptureAttribute",
    "FieldToGrid",
    "JoinGeometry",
    "SDFGridBoolean",
    "Bake",
    "JoinStrings",
    "GeometryToInstance",
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "SimulationInput",
    "SimulationOutput",
    "SimulationZone",
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


class Bake(NodeBuilder):
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

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.bake_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.bake_items
        }

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__")


class GeometryToInstance(NodeBuilder):
    """Convert each input geometry into an instance, which can be much faster than the Join Geometry node when the inputs are large"""

    _bl_idname = "GeometryNodeGeometryToInstance"
    node: bpy.types.GeometryNodeGeometryToInstance

    def __init__(self, *args: TYPE_INPUT_GEOMETRY):
        super().__init__()
        for arg in reversed(args):
            self._link_from(arg, "Geometry")

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class Value(NodeBuilder):
    """Input numerical values to other nodes in the tree"""

    _bl_idname = "ShaderNodeValue"
    node: bpy.types.ShaderNodeValue

    def __init__(self, value: float = 0.0):
        super().__init__()
        self.value = value

    @property
    def value(self) -> float:
        """Input socket: Value"""
        # this node is a strange one because it doesn't have a value property,
        # instead we directly access and change the sockets default output
        return self.node.outputs[0].default_value  # type: ignore

    @value.setter
    def value(self, value: float):
        self.node.outputs[0].default_value = value  # type: ignore

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")


class FormatString(NodeBuilder):
    """Insert values into a string using a Python and path template compatible formatting syntax"""

    _bl_idname = "FunctionNodeFormatString"
    node: bpy.types.FunctionNodeFormatString
    _socket_data_types = ("VALUE", "INT", "STRING")

    def __init__(
        self,
        *args,
        format: TYPE_INPUT_STRING = "",
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
    def i_format(self) -> SocketLinker:
        """Input socket: Format"""
        return self._input("Format")

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def items(self) -> dict[str, SocketLinker]:
        """Input sockets:"""
        return {socket.name: self._input(socket.name) for socket in self.node.inputs}

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class JoinStrings(NodeBuilder):
    """Combine any number of input strings"""

    _bl_idname = "GeometryNodeStringJoin"
    node: bpy.types.GeometryNodeStringJoin

    def __init__(self, *args: LINKABLE, delimiter: TYPE_INPUT_STRING = ""):
        super().__init__()

        self._establish_links(Delimiter=delimiter)
        for arg in args:
            self._link_from(arg, "Strings")

    @property
    def i_delimiter(self) -> SocketLinker:
        """Input socket: Delimiter"""
        return self._input("Delimiter")

    @property
    def i_strings(self) -> SocketLinker:
        """Input socket: Strings"""
        return self._input("Strings")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class MeshBoolean(NodeBuilder):
    """Cut, subtract, or join multiple mesh inputs"""

    _bl_idname = "GeometryNodeMeshBoolean"
    node: bpy.types.GeometryNodeMeshBoolean

    def __init__(
        self,
        *args: TYPE_INPUT_GEOMETRY,
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
        *args: TYPE_INPUT_GEOMETRY,
        self_intersection: TYPE_INPUT_BOOLEAN = False,
        hole_tolerant: TYPE_INPUT_BOOLEAN = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ):
        key_args = {}
        if solver == "EXACT":
            key_args["Self Intersection"] = self_intersection
            key_args["Hole Tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="INTERSECT",
        )

    @classmethod
    def m_union(
        cls,
        *args: TYPE_INPUT_GEOMETRY,
        hole_tolerant: TYPE_INPUT_BOOLEAN = False,
        self_intersection: TYPE_INPUT_BOOLEAN = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ):
        key_args = {}
        if solver == "EXACT":
            key_args["Self Intersection"] = self_intersection
            key_args["Hole Tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="UNION",
        )

    @classmethod
    def m_difference(
        cls,
        *args: TYPE_INPUT_GEOMETRY,
        mesh_1: TYPE_INPUT_GEOMETRY = None,
        hole_tolerant: TYPE_INPUT_BOOLEAN = False,
        self_intersection: TYPE_INPUT_BOOLEAN = False,
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ):
        key_args = {}
        key_args["Mesh 1"] = mesh_1
        if solver == "EXACT":
            key_args["Self Intersection"] = self_intersection
            key_args["Hole Tolerant"] = hole_tolerant
        return cls(
            *args,
            **key_args,
            solver=solver,
            operation="DIFFERENCE",
        )

    @classmethod
    def union(cls, mesh_1: LINKABLE = None, mesh_2: LINKABLE = None) -> "MeshBoolean":
        """Create Mesh Boolean with operation 'Union'."""
        return cls(operation="UNION", mesh_1=mesh_1, mesh_2=mesh_2)

    @classmethod
    def difference(
        cls, mesh_1: LINKABLE = None, mesh_2: LINKABLE = None
    ) -> "MeshBoolean":
        """Create Mesh Boolean with operation 'Difference'."""
        return cls(operation="DIFFERENCE", mesh_1=mesh_1, mesh_2=mesh_2)

    @property
    def i_mesh_1(self) -> SocketLinker:
        """Input socket: Mesh 1"""
        return self._input("Mesh 1")

    @property
    def i_mesh_2(self) -> SocketLinker:
        """Input socket: Mesh 2"""
        return self._input("Mesh 2")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_intersecting_edges(self) -> SocketLinker:
        """Output socket: Mesh"""
        if self.solver == "FLOAT":
            raise ValueError("Intersecting Edges is not supported for FLOAT solver")
        return self._output("Intersecting Edges")

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

    def __init__(self, *args: LINKABLE):
        super().__init__()
        for source in reversed(args):
            self._link_from(source, self)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetHandleType(NodeBuilder):
    """Set the handle type for the control points of a Bézier curve"""

    _bl_idname = "GeometryNodeCurveSetHandles"
    node: bpy.types.GeometryNodeCurveSetHandles

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
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
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

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
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")

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


def _typed_index_switch(data_type: SOCKET_TYPES):
    @classmethod
    def method(cls, *args: TYPE_INPUT_ALL, index: TYPE_INPUT_INT = 0) -> "IndexSwitch":
        """Create an IndexSwitch node with a pre-set data_type"""
        return cls(*args, index=index, data_type=data_type)

    return method


class IndexSwitch(NodeBuilder):
    """Node builder for the Index Switch node"""

    _bl_idname = "GeometryNodeIndexSwitch"
    node: bpy.types.GeometryNodeIndexSwitch
    float = _typed_index_switch("FLOAT")
    integer = _typed_index_switch("INT")
    boolean = _typed_index_switch("BOOLEAN")
    vector = _typed_index_switch("VECTOR")
    color = _typed_index_switch("RGBA")
    rotation = _typed_index_switch("ROTATION")
    matrix = _typed_index_switch("MATRIX")
    string = _typed_index_switch("STRING")
    menu = _typed_index_switch("MENU")
    object = _typed_index_switch("OBJECT")
    geometry = _typed_index_switch("GEOMETRY")
    collection = _typed_index_switch("COLLECTION")
    image = _typed_index_switch("IMAGE")
    material = _typed_index_switch("MATERIAL")
    bundle = _typed_index_switch("BUNDLE")
    closure = _typed_index_switch("CLOSURE")

    def __init__(
        self,
        *args: TYPE_INPUT_ALL,
        index: TYPE_INPUT_INT = 0,
        data_type: SOCKET_TYPES = "FLOAT",
    ):
        super().__init__()
        self.data_type = data_type
        key_args: dict[str, TYPE_INPUT_ALL] = {"Index": index}
        self.node.index_switch_items.clear()
        self._link_args(*args)
        self._establish_links(**key_args)

    def _create_socket(self) -> NodeSocket:
        item = self.node.index_switch_items.new()
        return self.node.inputs[item.identifier]

    def _link_args(self, *args: TYPE_INPUT_ALL):
        for arg in args:
            if _is_default_value(arg):
                socket = self._create_socket()
                socket.default_value = arg
            else:
                source = self._source_socket(arg)
                self.tree.link(source, self.node.inputs["__extend__"])

    @property
    def inputs(self) -> list[SocketLinker]:
        """Input sockets"""
        return [
            SocketLinker(self.node.inputs[i + 1])
            for i in range(len(self.node.index_switch_items))
        ]

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def data_type(self) -> SOCKET_TYPES:
        """Input socket: Data Type"""
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value


def _typed_menu_switch(data_type: SOCKET_TYPES):
    @classmethod
    def method(
        cls,
        *args: TYPE_INPUT_ALL,
        menu: TYPE_INPUT_MENU = None,
        data_type: SOCKET_TYPES = "FLOAT",
        **kwargs: TYPE_INPUT_ALL,
    ) -> "IndexSwitch":
        """Create an IndexSwitch node with a pre-set data_type"""
        return cls(*args, menu=menu, data_type=data_type, **kwargs)

    return method


class MenuSwitch(NodeBuilder):
    """Node builder for the Index Switch node"""

    _bl_idname = "GeometryNodeMenuSwitch"
    node: bpy.types.GeometryNodeMenuSwitch

    float = _typed_menu_switch("FLOAT")
    integer = _typed_menu_switch("INT")
    boolean = _typed_menu_switch("BOOLEAN")
    vector = _typed_menu_switch("VECTOR")
    color = _typed_menu_switch("RGBA")
    rotation = _typed_menu_switch("ROTATION")
    matrix = _typed_menu_switch("MATRIX")
    string = _typed_menu_switch("STRING")
    menu = _typed_menu_switch("MENU")
    object = _typed_menu_switch("OBJECT")
    geometry = _typed_menu_switch("GEOMETRY")
    collection = _typed_menu_switch("COLLECTION")
    image = _typed_menu_switch("IMAGE")
    material = _typed_menu_switch("MATERIAL")
    bundle = _typed_menu_switch("BUNDLE")
    closure = _typed_menu_switch("CLOSURE")

    def __init__(
        self,
        *args: TYPE_INPUT_ALL,
        menu: TYPE_INPUT_MENU = None,
        data_type: SOCKET_TYPES = "FLOAT",
        **kwargs: TYPE_INPUT_ALL,
    ):
        super().__init__()
        self.data_type = data_type
        self.node.enum_items.clear()
        key_args = {"Menu": menu}
        self._link_args(*args, **kwargs)
        self._establish_links(**key_args)

    def _link_args(self, *args: TYPE_INPUT_ALL, **kwargs: TYPE_INPUT_ALL):
        for arg in args:
            if _is_default_value(arg):
                socket = self._create_socket(f"Item_{len(self.node.enum_items)}")
                socket.default_value = arg
            else:
                source = self._source_socket(arg)
                self.tree.link(source, self.node.inputs["__extend__"])

        for key, value in kwargs.items():
            if _is_default_value(value):
                socket = self._create_socket(key)
                socket.default_value = value
            else:
                source = self._source_socket(value)  # type: ignore
                self._link(source, self.node.inputs["__extend__"])
                self.node.enum_items[-1].name = key

    def _create_socket(self, name: str) -> bpy.types.NodeSocket:
        item = self.node.enum_items.new(name)
        return self.node.inputs[item.name]

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        """Input sockets"""
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.enum_items
        }

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        """Input sockets"""
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.enum_items
        }

    @property
    def i_menu(self) -> SocketLinker:
        """Input socket: Menu"""
        return self._input("Menu")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def data_type(self) -> SOCKET_TYPES:
        """Input socket: Data Type"""
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value


def _domain_capture_attribute(domain: _AttributeDomains):
    @classmethod
    def method(
        cls,
        *args: LINKABLE,
        geometry: TYPE_INPUT_GEOMETRY = None,
        **kwargs,
    ) -> "CaptureAttribute":
        """Create an IndexSwitch node with a pre-set domain"""
        return cls(*args, geometry=geometry, domain=domain, **kwargs)

    return method


class CaptureAttribute(NodeBuilder):
    """Store the result of a field on a geometry and output the data as a node socket. Allows remembering or interpolating data as the geometry changes, such as positions before deformation"""

    _bl_idname = "GeometryNodeCaptureAttribute"
    node: bpy.types.GeometryNodeCaptureAttribute
    point = _domain_capture_attribute("POINT")
    edge = _domain_capture_attribute("EDGE")
    face = _domain_capture_attribute("FACE")
    corner = _domain_capture_attribute("CORNER")
    curve = _domain_capture_attribute("CURVE")
    instance = _domain_capture_attribute("INSTANCE")
    layer = _domain_capture_attribute("LAYER")

    def __init__(
        self,
        *args: LINKABLE,
        geometry: TYPE_INPUT_GEOMETRY = None,
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry}
        self.domain = domain
        key_args.update(self._add_inputs(*args, **kwargs))  # type: ignore
        self._establish_links(**key_args)

    def _add_socket(self, name: str, type: _AttributeDataTypes):
        item = self.node.capture_items.new(socket_type=type, name=name)
        return self.node.inputs[item.name]

    def capture(self, value: LINKABLE) -> SocketLinker:
        """Capture the value to store in the attribute

        Return the SocketLinker for the output socket
        """
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
        input_dict = self._add_inputs(value)
        return SocketLinker(self.node.outputs[next(iter(input_dict))])

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.capture_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.capture_items
        }

    @property
    def _items(self) -> bpy.types.NodeGeometryCaptureAttributeItems:
        return self.node.capture_items

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

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


class FieldToGrid(NodeBuilder):
    """Create new grids by evaluating new values on an existing volume grid topology

    New socket items for field evaluation are first created from *args then **kwargs to give specific names to the items.

    Data types are inferred automatically from the closest compatible data type.

    Inputs:
    -------
    topology: LINKABLE
        The grid which contains the topology to evaluate the different fields on.
    data_type: _GridDataTypes = "FLOAT"
        The data type of the grid to evaluate on. Possible values are "FLOAT", "INT", "VECTOR", "BOOLEAN".
    *args: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT | TYPE_INPUT_BOOLEAN
        The fields to evaluate on the grid.
    **kwargs: dict[str, TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT | TYPE_INPUT_GEOMETRY]
        The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket.

    """

    _bl_idname = "GeometryNodeFieldToGrid"
    node: bpy.types.GeometryNodeFieldToGrid
    _socket_data_types = ("FLOAT", "VALUE", "INT", "VECTOR", "BOOLEAN")
    _default_input_id = "Topology"

    def __init__(
        self,
        *args: TYPE_INPUT_GRID,
        topology: TYPE_INPUT_GRID = None,
        data_type: _GridDataTypes = "FLOAT",
        **kwargs: TYPE_INPUT_GRID,
    ):
        super().__init__()
        self.data_type = data_type
        key_args = {
            "Topology": topology,
        }
        key_args.update(self._add_inputs(*args, **kwargs))  # type: ignore
        self._establish_links(**key_args)

    def _add_socket(  # type: ignore
        self,
        name: str,
        type: _GridDataTypes = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.grid_items.new(socket_type=type, name=name)
        if default_value is not None:
            try:
                self.node.inputs[item.name].default_value = default_value  # type: ignore
            except TypeError as e:
                raise ValueError(
                    f"Invalid default value for {type}: {default_value}"
                ) from e
        return self.node.inputs[item.name]

    def capture(self, *args, **kwargs) -> list[SocketLinker]:
        outputs = {
            name: self.node.outputs[name] for name in self._add_inputs(*args, **kwargs)
        }

        return [SocketLinker(x) for x in outputs.values()]

    @classmethod
    def float(cls, *args: TYPE_INPUT_GRID, topology: TYPE_INPUT_GRID = None, **kwargs):
        return cls(*args, data_type="FLOAT", topology=topology, **kwargs)

    @classmethod
    def integer(
        cls, *args: TYPE_INPUT_GRID, topology: TYPE_INPUT_GRID = None, **kwargs
    ):
        return cls(*args, data_type="INT", topology=topology, **kwargs)

    @classmethod
    def vector(cls, *args: TYPE_INPUT_GRID, topology: TYPE_INPUT_GRID = None, **kwargs):
        return cls(*args, data_type="VECTOR", topology=topology, **kwargs)

    @classmethod
    def boolean(
        cls, *args: TYPE_INPUT_GRID, topology: TYPE_INPUT_GRID = None, **kwargs
    ):
        return cls(*args, data_type="BOOLEAN", topology=topology, **kwargs)

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.grid_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.grid_items
        }

    @property
    def i_topology(self) -> SocketLinker:
        """Input socket: Topology"""
        return self._input("Topology")

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
        *args: LINKABLE,
    ) -> "SDFGridBoolean":
        node = cls(operation="INTERSECT")
        for arg in args:
            if arg is None:
                continue
            node._link_from(arg, "Grid 2")
        return node

    @classmethod
    def union(
        cls,
        *args: LINKABLE,
    ) -> "SDFGridBoolean":
        node = cls(operation="UNION")
        for arg in args:
            if arg is None:
                continue
            node._link_from(arg, "Grid 2")
        return node

    @classmethod
    def difference(
        cls,
        *args: LINKABLE,
        grid_1: LINKABLE,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Difference'."""
        node = cls(operation="DIFFERENCE")
        node._link_from(grid_1, "Grid 1")
        for arg in args:
            if arg is None:
                continue
            node._link_from(arg, "Grid 2")
        return node

    @property
    def i_grid_1(self) -> SocketLinker:
        """Input socket: Grid 1"""
        return self._input("Grid 1")

    @property
    def i_grid_2(self) -> SocketLinker:
        """Input socket: Grid 2"""
        return self._input("Grid 2")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value


def _accumlate_field_factory(domain: _AttributeDomains):
    """Create a factory for AccumulateField with a specific data type"""

    class EvaluateAtIndexDomainFactory:
        @staticmethod
        def float(
            value: TYPE_INPUT_VALUE = None, index: TYPE_INPUT_INT = 0
        ) -> "AccumulateField":
            return AccumulateField(value, index, domain=domain, data_type="FLOAT")

        @staticmethod
        def integer(
            value: TYPE_INPUT_INT = None, index: TYPE_INPUT_INT = 0
        ) -> "AccumulateField":
            return AccumulateField(value, index, domain=domain, data_type="INT")

        @staticmethod
        def vector(
            value: TYPE_INPUT_VECTOR = None, index: TYPE_INPUT_INT = 0
        ) -> "AccumulateField":
            return AccumulateField(
                value, index, domain=domain, data_type="FLOAT_VECTOR"
            )

        @staticmethod
        def transform(
            value: TYPE_INPUT_MATRIX = None, index: TYPE_INPUT_INT = 0
        ) -> "AccumulateField":
            return AccumulateField(value, index, domain=domain, data_type="TRANSFORM")

    return EvaluateAtIndexDomainFactory()


class AccumulateField(NodeBuilder):
    """Add the values of an evaluated field together and output the running total for each element"""

    _bl_idname = "GeometryNodeAccumulateField"
    node: bpy.types.GeometryNodeAccumulateField

    point = _accumlate_field_factory("POINT")
    edge = _accumlate_field_factory("EDGE")
    face = _accumlate_field_factory("FACE")
    corner = _accumlate_field_factory("CORNER")
    spline = _accumlate_field_factory("CURVE")
    instance = _accumlate_field_factory("INSTANCE")
    layer = _accumlate_field_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_VALUE
        | TYPE_INPUT_INT
        | TYPE_INPUT_VECTOR
        | TYPE_INPUT_MATRIX = 1.0,
        group_index: TYPE_INPUT_INT = 0,
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

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_leading(self) -> SocketLinker:
        """Output socket: Leading"""
        return self._output("Leading")

    @property
    def o_trailing(self) -> SocketLinker:
        """Output socket: Trailing"""
        return self._output("Trailing")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")

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


def _evaluate_at_index_factory(domain: _AttributeDomains):
    """Create a factory for AccumulateField with a specific data type"""

    class EvaluateAtIndexDomainFactory:
        @staticmethod
        def float(value: TYPE_INPUT_VALUE = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(value, index, domain=domain, data_type="FLOAT")

        @staticmethod
        def integer(value: TYPE_INPUT_INT = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(value, index, domain=domain, data_type="INT")

        @staticmethod
        def boolean(value: TYPE_INPUT_BOOLEAN = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(value, index, domain=domain, data_type="BOOLEAN")

        @staticmethod
        def vector(value: TYPE_INPUT_VECTOR = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(
                value, index, domain=domain, data_type="FLOAT_VECTOR"
            )

        @staticmethod
        def rotation(value: TYPE_INPUT_ROTATION = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(value, index, domain=domain, data_type="QUATERNION")

        @staticmethod
        def transform(value: TYPE_INPUT_MATRIX = None, index: TYPE_INPUT_INT = 0):
            return EvaluateAtIndex(value, index, domain=domain, data_type="FLOAT4X4")

    return EvaluateAtIndexDomainFactory()


class EvaluateAtIndex(NodeBuilder):
    """Retrieve data of other elements in the context's geometry"""

    _bl_idname = "GeometryNodeFieldAtIndex"
    node: bpy.types.GeometryNodeFieldAtIndex

    point = _evaluate_at_index_factory("POINT")
    edge = _evaluate_at_index_factory("EDGE")
    face = _evaluate_at_index_factory("FACE")
    corner = _evaluate_at_index_factory("CORNER")
    spline = _evaluate_at_index_factory("CURVE")
    instance = _evaluate_at_index_factory("INSTANCE")
    layer = _evaluate_at_index_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_DATA = None,
        index: TYPE_INPUT_INT = 0,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Index": index}
        key_args.update(kwargs)
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

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


def _field_average_factory(domain: _AttributeDomains):
    """Create a factory for FieldVariance with a specific data type"""

    class FieldAverageDomainFactory:
        @staticmethod
        def float(
            value: TYPE_INPUT_VALUE = 1.0,
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldAverage":
            """Create FieldAverage for the "FLOAT" data type"""
            return FieldAverage(value, group_index, data_type="FLOAT", domain=domain)

        @staticmethod
        def vector(
            value: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldAverage":
            """Create FieldAverage on for the "FLOAT_VECTOR" data type"""
            return FieldAverage(
                value, group_index, data_type="FLOAT_VECTOR", domain=domain
            )

    return FieldAverageDomainFactory()


class FieldAverage(NodeBuilder):
    """Calculate the mean and median of a given field"""

    _bl_idname = "GeometryNodeFieldAverage"
    node: bpy.types.GeometryNodeFieldAverage

    point = _field_average_factory("POINT")
    edge = _field_average_factory("EDGE")
    face = _field_average_factory("FACE")
    corner = _field_average_factory("CORNER")
    spline = _field_average_factory("CURVE")
    instance = _field_average_factory("INSTANCE")
    layer = _field_average_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR = None,
        group_index: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR = 0,
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
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_mean(self) -> SocketLinker:
        """Output socket: Mean"""
        return self._output("Mean")

    @property
    def o_median(self) -> SocketLinker:
        """Output socket: Median"""
        return self._output("Median")

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


def _field_min_and_max_factory(domain: _AttributeDomains):
    """Create a factory for AccumulateField with a specific data type"""

    class FieldMinMaxDataTypeFactory:
        @staticmethod
        def float(
            value: TYPE_INPUT_VALUE = 1.0,
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldMinAndMax":
            """Create FieldMinMax for the "FLOAT" data type"""
            return FieldMinAndMax(value, group_index, data_type="FLOAT", domain=domain)

        @staticmethod
        def integer(
            value: TYPE_INPUT_INT = 1,
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldMinAndMax":
            """Create FieldMinMax for the "INT" data type"""
            return FieldMinAndMax(value, group_index, data_type="INT", domain=domain)

        @staticmethod
        def vector(
            value: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldMinAndMax":
            """Create FieldMinMax on for the "FLOAT_VECTOR" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="FLOAT_VECTOR", domain=domain
            )

    return FieldMinMaxDataTypeFactory()


class FieldMinAndMax(NodeBuilder):
    """Calculate the minimum and maximum of a given field"""

    _bl_idname = "GeometryNodeFieldMinAndMax"
    node: bpy.types.GeometryNodeFieldMinAndMax

    point = _field_min_and_max_factory("POINT")
    edge = _field_min_and_max_factory("EDGE")
    face = _field_min_and_max_factory("FACE")
    corner = _field_min_and_max_factory("CORNER")
    spline = _field_min_and_max_factory("CURVE")
    instance = _field_min_and_max_factory("INSTANCE")
    layer = _field_min_and_max_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT = 1.0,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_min(self) -> SocketLinker:
        """Output socket: Min"""
        return self._output("Min")

    @property
    def o_max(self) -> SocketLinker:
        """Output socket: Max"""
        return self._output("Max")

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


def _evaluate_on_domain_factory(domain: _AttributeDomains):
    """Create a factory for AccumulateField with a specific data type"""

    class EvaluateOnDomainDomainFactory:
        @staticmethod
        def float(value: TYPE_INPUT_VALUE = None):
            return EvaluateOnDomain(value, domain=domain, data_type="FLOAT")

        @staticmethod
        def integer(value: TYPE_INPUT_INT = None):
            return EvaluateOnDomain(value, domain=domain, data_type="INT")

        @staticmethod
        def boolean(value: TYPE_INPUT_BOOLEAN = None, index: TYPE_INPUT_INT = 0):
            return EvaluateOnDomain(value, domain=domain, data_type="BOOLEAN")

        @staticmethod
        def vector(value: TYPE_INPUT_VECTOR = None):
            return EvaluateOnDomain(value, domain=domain, data_type="FLOAT_VECTOR")

        @staticmethod
        def rotation(value: TYPE_INPUT_ROTATION = None):
            return EvaluateOnDomain(value, domain=domain, data_type="QUATERNION")

        @staticmethod
        def transform(value: TYPE_INPUT_MATRIX = None):
            return EvaluateOnDomain(value, domain=domain, data_type="FLOAT4X4")

    return EvaluateOnDomainDomainFactory()


class EvaluateOnDomain(NodeBuilder):
    """Retrieve values from a field on a different domain besides the domain from the context"""

    _bl_idname = "GeometryNodeFieldOnDomain"
    node: bpy.types.GeometryNodeFieldOnDomain

    point = _field_min_and_max_factory("POINT")
    edge = _field_min_and_max_factory("EDGE")
    face = _field_min_and_max_factory("FACE")
    corner = _field_min_and_max_factory("CORNER")
    spline = _field_min_and_max_factory("CURVE")
    instance = _field_min_and_max_factory("INSTANCE")
    layer = _field_min_and_max_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_DATA = None,
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
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

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


def _field_variance_factory(domain: _AttributeDomains):
    """Create a factory for FieldVariance with a specific data type"""

    class FieldVarianceDomainFactory:
        @staticmethod
        def float(
            value: TYPE_INPUT_VALUE = 1.0,
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldVariance":
            """Create FieldVariance for the "FLOAT" data type"""
            return FieldVariance(value, group_index, data_type="FLOAT", domain=domain)

        @staticmethod
        def vector(
            value: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
            group_index: TYPE_INPUT_INT = 0,
        ) -> "FieldVariance":
            """Create FieldVariance on for the "FLOAT_VECTOR" data type"""
            return FieldVariance(
                value, group_index, data_type="FLOAT_VECTOR", domain=domain
            )

    return FieldVarianceDomainFactory()


class FieldVariance(NodeBuilder):
    """Calculate the standard deviation and variance of a given field"""

    _bl_idname = "GeometryNodeFieldVariance"
    node: bpy.types.GeometryNodeFieldVariance

    point = _field_variance_factory("POINT")
    edge = _field_variance_factory("EDGE")
    face = _field_variance_factory("FACE")
    corner = _field_variance_factory("CORNER")
    spline = _field_variance_factory("CURVE")
    instance = _field_variance_factory("INSTANCE")
    layer = _field_variance_factory("LAYER")

    def __init__(
        self,
        value: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR = None,
        group_index: TYPE_INPUT_INT = None,
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
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_standard_deviation(self) -> SocketLinker:
        """Output socket: Standard Deviation"""
        return self._output("Standard Deviation")

    @property
    def o_variance(self) -> SocketLinker:
        """Output socket: Variance"""
        return self._output("Variance")

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


def _compare_operation_method(operation: _CompareOperations):
    """Create a factory for Compare with a specific operation"""

    class CompareOperationFactory:
        @staticmethod
        def float(
            a: TYPE_INPUT_VALUE = 0.0,
            b: TYPE_INPUT_VALUE = 0.0,
            *,
            epsilon: TYPE_INPUT_VALUE = 0.0001,
        ) -> "Compare":
            return Compare.float(operation=operation, a=a, b=b, epsilon=epsilon)

        @staticmethod
        def integer(a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "Compare":
            return Compare.integer(operation=operation, a=a, b=b)

        @staticmethod
        def vector(
            a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
            b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
            *,
            mode: _CompareVectorModes = "ELEMENT",
            c: TYPE_INPUT_VALUE = None,
            angle: TYPE_INPUT_VALUE = None,
            epsilon: TYPE_INPUT_VALUE = None,
        ) -> "Compare":
            return Compare.vector(
                operation=operation,
                a=a,
                b=b,
                mode=mode,
                c=c,
                angle=angle,
                epsilon=epsilon,
            )

        @staticmethod
        def color(
            a: TYPE_INPUT_COLOR = None,
            b: TYPE_INPUT_COLOR = None,
            epsilon: TYPE_INPUT_VALUE = None,
        ) -> "Compare":
            return Compare.color(operation=operation, a=a, b=b, epsilon=epsilon)

        @staticmethod
        def string(a: TYPE_INPUT_STRING = "", b: TYPE_INPUT_STRING = "") -> "Compare":
            return Compare.string(operation=operation, a=a, b=b)

    return CompareOperationFactory()


class Compare(NodeBuilder):
    """Perform a comparison operation on the two given inputs"""

    _bl_idname = "FunctionNodeCompare"
    node: bpy.types.FunctionNodeCompare

    less_than = _compare_operation_method("LESS_THAN")
    less_equal = _compare_operation_method("LESS_EQUAL")
    greater_than = _compare_operation_method("GREATER_THAN")
    greater_equal = _compare_operation_method("GREATER_EQUAL")
    equal = _compare_operation_method("EQUAL")
    not_equal = _compare_operation_method("NOT_EQUAL")
    brighter = _compare_operation_method("BRIGHTER")
    darker = _compare_operation_method("DARKER")

    def __init__(
        self,
        operation: _CompareOperations = "GREATER_THAN",
        data_type: _CompareDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        self.operation = operation
        self.data_type = data_type
        if self.data_type == "VECTOR":
            self.mode = kwargs["mode"]
        self._establish_links(**kwargs)

    @classmethod
    def float(
        cls,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        operation: _CompareOperations = "LESS_THAN",
        *,
        epsilon: TYPE_INPUT_VALUE = 0.0001,
    ):
        kwargs = {"operation": operation, "data_type": "FLOAT", "A": a, "B": b}
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon
        return cls(**kwargs)

    @classmethod
    def integer(
        cls,
        a: TYPE_INPUT_INT = 0,
        b: TYPE_INPUT_INT = 0,
        operation: _CompareOperations = "LESS_THAN",
    ) -> "Compare":
        return cls(operation=operation, data_type="INT", A_INT=a, B_INT=b)

    @classmethod
    def vector(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        operation: _CompareOperations = "LESS_THAN",
        *,
        mode: _CompareVectorModes = "ELEMENT",
        c: TYPE_INPUT_VALUE = None,
        angle: TYPE_INPUT_VALUE = None,
        epsilon: TYPE_INPUT_VALUE = None,
    ) -> "Compare":
        kwargs = {
            "operation": operation,
            "data_type": "VECTOR",
            "mode": mode,
            "A_VEC3": a,
            "B_VEC3": b,
        }
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon

        match mode:
            case "DIRECTION":
                kwargs["Angle"] = angle
            case "DOT_PRODUCT":
                kwargs["C"] = c
            case _:
                pass

        return cls(**kwargs)

    @classmethod
    def color(
        cls,
        a: TYPE_INPUT_COLOR = None,
        b: TYPE_INPUT_COLOR = None,
        operation: _CompareOperations = "EQUAL",
        *,
        epsilon: TYPE_INPUT_VALUE = None,
    ) -> "Compare":
        """Create Compare with operation 'Color'."""
        kwargs = {
            "operation": operation,
            "data_type": "RGBA",
            "A_COL": a,
            "B_COL": b,
        }
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon
        return cls(**kwargs)

    @classmethod
    def string(
        cls,
        a,
        b,
    ) -> "Compare":
        """Create Compare with operation 'String'."""
        return cls(mode="STRING", A_STR=a, B_STR=b)

    def _suffix(self) -> str:
        suffix_lookup = {
            "FLOAT": "",
            "INT": "_INT",
            "VECTOR": "_VEC",
            "RGBA": "_COL",
            "STRING": "_STR",
        }
        return suffix_lookup[self.data_type]

    @property
    def i_a(self) -> SocketLinker:
        """Input socket: A"""
        return self._input(f"A{self._suffix()}")

    @property
    def i_b(self) -> SocketLinker:
        """Input socket: B"""
        return self._input(f"B{self._suffix()}")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")

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
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        attribute: LINKABLE = None,
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
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_attribute(self) -> SocketLinker:
        """Input socket: Attribute"""
        return self._input("Attribute")

    @property
    def o_mean(self) -> SocketLinker:
        """Output socket: Mean"""
        return self._output("Mean")

    @property
    def o_median(self) -> SocketLinker:
        """Output socket: Median"""
        return self._output("Median")

    @property
    def o_sum(self) -> SocketLinker:
        """Output socket: Sum"""
        return self._output("Sum")

    @property
    def o_min(self) -> SocketLinker:
        """Output socket: Min"""
        return self._output("Min")

    @property
    def o_max(self) -> SocketLinker:
        """Output socket: Max"""
        return self._output("Max")

    @property
    def o_range(self) -> SocketLinker:
        """Output socket: Range"""
        return self._output("Range")

    @property
    def o_standard_deviation(self) -> SocketLinker:
        """Output socket: Standard Deviation"""
        return self._output("Standard Deviation")

    @property
    def o_variance(self) -> SocketLinker:
        """Output socket: Variance"""
        return self._output("Variance")

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
