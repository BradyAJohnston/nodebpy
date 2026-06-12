from typing import NamedTuple

import pytest
from mathutils import Euler

from nodebpy.nodes import geometry as g


def test_dynamic_inputs():
    with g.tree() as tree:
        ftg = g.FieldToGrid()
        inferred_flaot_item = ftg.add_item("float", 1.0)
        assert inferred_flaot_item.name == "float"
        assert inferred_flaot_item.socket_type == "FLOAT"
        inferred_boolean = ftg.add_item("boolean", True)
        assert inferred_boolean.name == "boolean"
        assert inferred_boolean.socket_type == "BOOLEAN"
        inferred_integer = ftg.add_item("integer", 42)
        assert inferred_integer.name == "integer"
        assert inferred_integer.socket_type == "INT"


        with pytest.raises(TypeError):
            ftg.add_item("name", None)

        with pytest.raises(TypeError):
            ftg.add_items({'example': 1.0, 'none': None})


        ftl = g.FieldToList(10)
        inferred_float_list = ftl.add_item("float", 1.0)
        assert inferred_float_list.name == "float"
        assert inferred_float_list.socket_type == "FLOAT"
        inferred_boolean_list = ftl.add_item("boolean", True)
        assert inferred_boolean_list.name == "boolean"
        assert inferred_boolean_list.socket_type == "BOOLEAN"
        inferred_integer_list = ftl.add_item("integer", 42)
        assert inferred_integer_list.name == "integer"
        assert inferred_integer_list.socket_type == "INT"
        inferred_rotation_list = ftl.add_item("rotation", Euler())
        assert inferred_rotation_list.name == "rotation"
        assert inferred_rotation_list.socket_type == "ROTATION"

        switch = g.IndexSwitch.integer(items=range(10))
        assert switch.data_type == "INT"
        assert len(switch.node.inputs) == 12 # 10 items + 1 index + 1 dynamic input socket
        assert len(switch._items) == 10
        switch2 = g.IndexSwitch.integer(items=range(20))

        with pytest.raises(KeyError):
            switch._item_socket(switch2._items[11])
        with pytest.raises(ValueError):
            switch2._item_socket(switch._items[1], output=True)
