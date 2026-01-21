from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class BlurAttribute(NodeBuilder):
    """Mix attribute values of neighboring elements"""

    name = "GeometryNodeBlurAttribute"
    node: bpy.types.GeometryNodeBlurAttribute

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value, "Iterations": iterations, "Weight": weight}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        value: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
    ) -> "BlurAttribute":
        """Create Blur Attribute with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, iterations=iterations, weight=weight)

    @classmethod
    def integer(
        cls,
        value: TYPE_INPUT_INT = 0,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
    ) -> "BlurAttribute":
        """Create Blur Attribute with operation 'Integer'."""
        return cls(data_type="INT", value=value, iterations=iterations, weight=weight)

    @classmethod
    def vector(
        cls,
        value: TYPE_INPUT_VECTOR = None,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
    ) -> "BlurAttribute":
        """Create Blur Attribute with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR", value=value, iterations=iterations, weight=weight
        )

    @classmethod
    def color(
        cls,
        value: TYPE_INPUT_COLOR = None,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
    ) -> "BlurAttribute":
        """Create Blur Attribute with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR", value=value, iterations=iterations, weight=weight
        )

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def i_weight(self) -> SocketLinker:
        """Input socket: Weight"""
        return self._input("Weight")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR"]):
        self.node.data_type = value


class DomainSize(NodeBuilder):
    """Retrieve the number of elements in a geometry for each attribute domain"""

    name = "GeometryNodeAttributeDomainSize"
    node: bpy.types.GeometryNodeAttributeDomainSize

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        *,
        component: Literal[
            "MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"
        ] = "MESH",
    ):
        super().__init__()
        key_args = {"Geometry": geometry}
        self.component = component
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_point_count(self) -> SocketLinker:
        """Output socket: Point Count"""
        return self._output("Point Count")

    @property
    def o_edge_count(self) -> SocketLinker:
        """Output socket: Edge Count"""
        return self._output("Edge Count")

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")

    @property
    def o_face_corner_count(self) -> SocketLinker:
        """Output socket: Face Corner Count"""
        return self._output("Face Corner Count")

    @property
    def o_spline_count(self) -> SocketLinker:
        """Output socket: Spline Count"""
        return self._output("Spline Count")

    @property
    def o_instance_count(self) -> SocketLinker:
        """Output socket: Instance Count"""
        return self._output("Instance Count")

    @property
    def o_layer_count(self) -> SocketLinker:
        """Output socket: Layer Count"""
        return self._output("Layer Count")

    @property
    def component(
        self,
    ) -> Literal["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"]:
        return self.node.component

    @component.setter
    def component(
        self, value: Literal["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"]
    ):
        self.node.component = value


class RemoveNamedAttribute(NodeBuilder):
    """Delete an attribute with a specified name from a geometry. Typically used to optimize performance"""

    name = "GeometryNodeRemoveAttribute"
    node: bpy.types.GeometryNodeRemoveAttribute

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        pattern_mode: TYPE_INPUT_MENU = "Exact",
        name: TYPE_INPUT_STRING = "",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Pattern Mode": pattern_mode, "Name": name}

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_pattern_mode(self) -> SocketLinker:
        """Input socket: Pattern Mode"""
        return self._input("Pattern Mode")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class StoreNamedAttribute(NodeBuilder):
    """Store the result of a field on a geometry as an attribute with the specified name"""

    name = "GeometryNodeStoreNamedAttribute"
    node: bpy.types.GeometryNodeStoreNamedAttribute

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal[
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
        ] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
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

    @classmethod
    def float(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_VALUE = 0.0,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def integer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_INT = 0,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Integer'."""
        return cls(
            data_type="INT",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def boolean(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_BOOLEAN = False,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def vector(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_VECTOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def color(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def quaternion(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_ROTATION = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Quaternion'."""
        return cls(
            data_type="QUATERNION",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Point'."""
        return cls(
            domain="POINT",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Edge'."""
        return cls(
            domain="EDGE",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Face'."""
        return cls(
            domain="FACE",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def spline(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Spline'."""
        return cls(
            domain="CURVE",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def instance(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Instance'."""
        return cls(
            domain="INSTANCE",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @classmethod
    def layer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        name: TYPE_INPUT_STRING = "",
        value: TYPE_INPUT_COLOR = None,
    ) -> "StoreNamedAttribute":
        """Create Store Named Attribute with operation 'Layer'."""
        return cls(
            domain="LAYER",
            geometry=geometry,
            selection=selection,
            name=name,
            value=value,
        )

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def data_type(
        self,
    ) -> Literal[
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
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
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
        ],
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"],
    ):
        self.node.domain = value
