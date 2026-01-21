from typing import Literal

import bpy

from ..builder import NodeBuilder, NodeSocket, SocketLinker
from ..types import (
    LINKABLE,
    SOCKET_TYPES,
    TYPE_INPUT_ALL,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_GRID,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    _AttributeDataTypes,
    _AttributeDomains,
    _GridDataTypes,
    _is_default_value,
)


class JoinStrings(NodeBuilder):
    """Combine any number of input strings"""

    name = "GeometryNodeStringJoin"
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

    name = "GeometryNodeMeshBoolean"
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

    name = "GeometryNodeJoinGeometry"
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

    name = "GeometryNodeCurveSetHandles"
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

    name = "GeometryNodeCurveHandleTypeSelection"
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

    name = "GeometryNodeIndexSwitch"
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

    name = "GeometryNodeMenuSwitch"
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

    name = "GeometryNodeCaptureAttribute"
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

    name = "GeometryNodeFieldToGrid"
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

    name = "GeometryNodeSDFGridBoolean"
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
