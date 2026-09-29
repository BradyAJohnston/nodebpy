"""Prototype: a custom group generic over its data type, like GetBundleItem[T].

Each data type builds its own inner tree (``_group_name``), and the typed
factories narrow ``i.value`` for type checkers.
"""

from typing import TYPE_CHECKING, Any, Literal, assert_type

import pytest

from nodebpy.builder import (
    CustomGeometryGroup,
    FloatSocket,
    GeometrySocket,
    IntegerSocket,
    SocketAccessor,
    StringSocket,
    TreeBuilder,
    VectorSocket,
)
from nodebpy.nodes import geometry as g
from nodebpy.types import (
    InputAny,
    InputFloat,
    InputGeometry,
    InputInteger,
    InputString,
    InputVector,
)

_DataType = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "FLOAT_VECTOR",
    "FLOAT_COLOR",
    "QUATERNION",
    "FLOAT4X4",
]

# data_type → tree.inputs / tree.outputs factory name
_INTERFACE_METHOD = {
    "FLOAT": "float",
    "INT": "integer",
    "BOOLEAN": "boolean",
    "FLOAT_VECTOR": "vector",
    "FLOAT_COLOR": "color",
    "QUATERNION": "rotation",
    "FLOAT4X4": "matrix",
}


class StoreNamedAttributeIfExists[T](CustomGeometryGroup):
    _name = "Store Named Attribute If Exists"
    # create_group() builds without __init__, so it gets this variant.
    _data_type: _DataType = "FLOAT"

    class _Inputs[S](SocketAccessor):
        geometry: GeometrySocket
        """Geometry"""
        name: StringSocket
        """Name"""
        value: S
        """Value"""

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
        """Geometry"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs[T]: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        geometry: InputGeometry = None,
        name: InputString = "",
        value: InputAny = None,
        *,
        data_type: _DataType = "FLOAT",
    ):
        # Set before super().__init__(): it picks and builds the inner tree.
        self._data_type = data_type
        super().__init__(Geometry=geometry, Name=name, Value=value)

    @property
    def data_type(self) -> _DataType:
        """Read-only: the group's socket types are fixed once built, so a
        different data type needs a new node."""
        return self._data_type

    def _group_name(self) -> str:
        return f"{self._name} ({self.data_type})"

    def _build_group(self, tree: TreeBuilder[Any]) -> None:
        geometry = tree.inputs.geometry("Geometry")
        name = tree.inputs.string("Name")
        value = getattr(tree.inputs, _INTERFACE_METHOD[self.data_type])("Value")

        exists = (
            g.NamedAttribute(name, data_type=self.data_type).o.exists
            >> g.SampleIndex.point.boolean(geometry=geometry)
        ).o.value

        (
            exists.switch.geometry(
                geometry,
                g.StoreNamedAttribute(
                    geometry=geometry,
                    data_type=self.data_type,
                    name=name,
                    value=value,
                ),
            )
            >> tree.outputs.geometry("Geometry")
        )

    @classmethod
    def float(
        cls,
        geometry: InputGeometry = None,
        name: InputString = "",
        value: InputFloat = 0.0,
    ) -> "StoreNamedAttributeIfExists[FloatSocket]":
        return StoreNamedAttributeIfExists(geometry, name, value, data_type="FLOAT")

    @classmethod
    def integer(
        cls,
        geometry: InputGeometry = None,
        name: InputString = "",
        value: InputInteger = 0,
    ) -> "StoreNamedAttributeIfExists[IntegerSocket]":
        return StoreNamedAttributeIfExists(geometry, name, value, data_type="INT")

    @classmethod
    def vector(
        cls,
        geometry: InputGeometry = None,
        name: InputString = "",
        value: InputVector = (0.0, 0.0, 0.0),
    ) -> "StoreNamedAttributeIfExists[VectorSocket]":
        return StoreNamedAttributeIfExists(
            geometry, name, value, data_type="FLOAT_VECTOR"
        )


def test_each_data_type_builds_its_own_group():
    with g.tree("Host") as tree:
        geo = tree.inputs.geometry("Geometry")
        f = StoreNamedAttributeIfExists.float(geo, "a", 1.5)
        v = StoreNamedAttributeIfExists.vector(f, "b", (1, 2, 3))
        f2 = StoreNamedAttributeIfExists.float(v, "c")
        f2 >> tree.outputs.geometry("Geometry")

    assert f.node.node_tree is f2.node.node_tree  # same variant reused
    assert f.node.node_tree is not v.node.node_tree
    assert f.node.node_tree.name == "Store Named Attribute If Exists (FLOAT)"
    assert v.node.node_tree.name == "Store Named Attribute If Exists (FLOAT_VECTOR)"
    assert f.i.value.socket.type == "VALUE"
    assert v.i.value.socket.type == "VECTOR"
    assert f.i.value.socket.default_value == 1.5
    assert tuple(v.i.value.socket.default_value) == (1, 2, 3)
    assert f.o.geometry.socket.links[0].to_node == v.node


def test_data_type_is_read_only():
    with g.tree("Host"):
        node = StoreNamedAttributeIfExists.vector()
    assert node.data_type == "FLOAT_VECTOR"
    with pytest.raises(AttributeError):
        node.data_type = "FLOAT"


def test_create_group_builds_default_variant():
    tree = StoreNamedAttributeIfExists.create_group()
    assert tree.name == "Store Named Attribute If Exists (FLOAT)"
    assert tree.interface.items_tree["Value"].socket_type == "NodeSocketFloat"


def _typing() -> None:
    with g.tree("Typing"):
        f = StoreNamedAttributeIfExists.float()
        assert_type(f, StoreNamedAttributeIfExists[FloatSocket])
        assert_type(f.i.value, FloatSocket)
        assert_type(StoreNamedAttributeIfExists.vector().i.value, VectorSocket)
        assert_type(f.o.geometry, GeometrySocket)
