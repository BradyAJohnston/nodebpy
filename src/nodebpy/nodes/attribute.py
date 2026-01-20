from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    _AttributeDataTypes,
    _AttributeDomains,
    _StoreNamedAttributeTypes,
)


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
    def component(
        self,
    ) -> Literal["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"]:
        return self.node.component

    @component.setter
    def component(
        self, value: Literal["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"]
    ):
        match value:
            case "MESH" | "POINTCLOUD" | "CURVE":
                self._default_output_id = "Point Count"
            case "INSTANCES":
                self._default_output_id = "Instance Count"
            case "GREASEPENCIL":
                self._default_output_id = "Layer Count"
        self.node.component = value


class AttributeStatistic(NodeBuilder):
    """Calculate statistics about a data set from a field evaluated on a geometry"""

    name = "GeometryNodeAttributeStatistic"
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


class BlurAttribute(NodeBuilder):
    """Mix attribute values of neighboring elements"""

    name = "GeometryNodeBlurAttribute"
    node: bpy.types.GeometryNodeBlurAttribute

    def __init__(
        self,
        value: LINKABLE = None,
        iterations: TYPE_INPUT_INT = 1,
        weight: TYPE_INPUT_VALUE = 1.0,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value, "Iterations": iterations, "Weight": weight}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
    ]:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
        ],
    ):
        self.node.data_type = value


class RemoveNamedAttribute(NodeBuilder):
    """Delete an attribute with a specified name from a geometry. Typically used to optimize performance"""

    name = "GeometryNodeRemoveAttribute"
    node: bpy.types.GeometryNodeRemoveAttribute

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        pattern_mode: Literal["Exact", "Wildcard"] | TYPE_INPUT_MENU = "Exact",
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
        value: LINKABLE = None,
        *,
        data_type: _StoreNamedAttributeTypes = "FLOAT",
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
    ) -> _StoreNamedAttributeTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _StoreNamedAttributeTypes,
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
