"""Tests for NodeBuilder operator overloads.

Tests arithmetic, comparison, boolean, and unary operators on NodeBuilder.
"""

import itertools

import numpy as np
import pytest

import nodebpy
from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import sockets as s


class TestPowerOperator:
    """Tests for ** operator (__pow__ / __rpow__)."""

    def test_float_power(self):
        with g.tree("TestFloatPower"):
            result = g.Value(2.0) ** 3.0

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "POWER"
        assert result.i.value_001.default_value == 3.0

    def test_integer_power(self):
        with g.tree("TestIntPower"):
            result = g.Integer(2) ** 3

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.operation == "POWER"

    def test_vector_power(self):
        with g.tree("TestVectorPower"):
            result = g.Vector((2, 3, 4)) ** (2, 2, 2)

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "POWER"

    def test_vector_power_scalar_broadcast(self):
        with g.tree("TestVectorPowerScalar"):
            result = g.Vector((2, 3, 4)) ** 2

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "POWER"

    def test_rpow_float(self):
        with g.tree("TestRPowFloat"):
            result = 2.0 ** g.Value(3.0)

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "POWER"
        assert result.i.value.default_value == 2.0
        assert not result.i.value.links
        assert result.i.value_001.links


class TestModuloOperator:
    """Tests for % operator (__mod__ / __rmod__)."""

    def test_float_modulo(self):
        with g.tree("TestFloatModulo"):
            result = g.Value(10.0) % 3.0

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "FLOORED_MODULO"

    def test_integer_modulo(self):
        with g.tree("TestIntModulo"):
            result = g.Integer(10) % 3

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.operation == "MODULO"

    def test_vector_modulo(self):
        with g.tree("TestVectorModulo"):
            result = g.Vector((10, 20, 30)) % (3, 3, 3)

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "MODULO"

    def test_vector_modulo_scalar_broadcast(self):
        with g.tree("TestVectorModuloScalar"):
            result = g.Vector((10, 20, 30)) % 3

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "MODULO"

    def test_rmod_float(self):
        with g.tree("TestRModFloat"):
            result = 10.0 % g.Value(3.0)

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "FLOORED_MODULO"
        assert result.i.value.default_value == 10.0


class TestFloorDivOperator:
    """Tests for // operator (__floordiv__ / __rfloordiv__)."""

    def test_integer_floordiv(self):
        with TreeBuilder("TestIntFloorDiv"):
            result = g.Integer(10) // 3

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.operation == "DIVIDE_FLOOR"

    def test_float_floordiv(self):
        with TreeBuilder("TestFloatFloorDiv"):
            result = g.Value(10.0) // 3.0

        # float floordiv composes divide + floor
        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "FLOOR"
        # the divide node should feed into the floor node
        assert result.i.value.links[0].from_node.operation == "DIVIDE"

    def test_vector_floordiv(self):
        with TreeBuilder("TestVectorFloorDiv"):
            result = g.Vector((10, 20, 30)) // (3, 3, 3)

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "FLOOR"
        assert result.i.vector.links[0].from_node.operation == "DIVIDE"

    def test_rfloordiv_integer(self):
        with TreeBuilder("TestRFloorDivInt"):
            result = 10 // g.Integer(3)

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.operation == "DIVIDE_FLOOR"


class TestNegOperator:
    """Tests for unary - operator (__neg__)."""

    def test_neg_float(self):
        with TreeBuilder("TestNegFloat"):
            result = -g.Value(5.0)

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.operation == "MULTIPLY"
        assert result.i.value_001.default_value == -1

    def test_neg_integer(self):
        with TreeBuilder("TestNegInt"):
            result = -g.Integer(5)

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.operation == "NEGATE"

    def test_neg_vector(self):
        with TreeBuilder("TestNegVector"):
            result = -g.Vector((1, 2, 3))

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.operation == "SCALE"
        assert result.i.scale.default_value == -1


class TestAbsOperator:
    """Tests for abs() (__abs__)."""

    def test_abs_float(self):
        with TreeBuilder("TestAbsFloat"):
            result = abs(g.Value(-5.0))

        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.node.operation == "ABSOLUTE"

    def test_abs_integer(self):
        with TreeBuilder("TestAbsInt"):
            result = abs(g.Integer(-5))

        assert result.node.bl_idname == "FunctionNodeIntegerMath"
        assert result.node.operation == "ABSOLUTE"

    def test_abs_vector(self):
        with TreeBuilder("TestAbsVector"):
            result = abs(g.Vector((-1, -2, -3)))

        assert result.node.bl_idname == "ShaderNodeVectorMath"
        assert result.node.operation == "ABSOLUTE"


class TestComparisonOperators:
    """Tests for <, >, <=, >= operators using Compare node."""

    def test_lt_float(self):
        with TreeBuilder("TestLtFloat"):
            result = g.Value(1.0) < 2.0

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "LESS_THAN"
        assert result.data_type == "FLOAT"

    def test_gt_float(self):
        with TreeBuilder("TestGtFloat"):
            result = g.Value(5.0) > 2.0

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "GREATER_THAN"
        assert result.data_type == "FLOAT"

    def test_le_float(self):
        with TreeBuilder("TestLeFloat"):
            result = g.Value(1.0) <= 2.0

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "LESS_EQUAL"
        assert result.data_type == "FLOAT"

    def test_ge_float(self):
        with TreeBuilder("TestGeFloat"):
            result = g.Value(5.0) >= 2.0

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "GREATER_EQUAL"
        assert result.data_type == "FLOAT"

    def test_lt_integer(self):
        with TreeBuilder("TestLtInt"):
            result = g.Integer(1) < 2

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "LESS_THAN"
        assert result.data_type == "INT"

    def test_gt_integer(self):
        with TreeBuilder("TestGtInt"):
            result = g.Integer(5) > 2

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "GREATER_THAN"
        assert result.data_type == "INT"

    def test_le_integer(self):
        with TreeBuilder("TestLeInt"):
            result = g.Integer(1) <= 2

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "LESS_EQUAL"
        assert result.data_type == "INT"

    def test_ge_integer(self):
        with TreeBuilder("TestGeInt"):
            result = g.Integer(5) >= 2

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "GREATER_EQUAL"
        assert result.data_type == "INT"

    def test_lt_vector(self):
        with TreeBuilder("TestLtVector"):
            result = g.Vector((1, 2, 3)) < (4, 5, 6)

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.operation == "LESS_THAN"
        assert result.data_type == "VECTOR"

    def test_comparison_between_nodes(self):
        with TreeBuilder("TestCompareNodes"):
            a = g.Value(1.0)
            b = g.Value(2.0)
            result = a < b

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.node.operation == "LESS_THAN"
        assert len(result.i["A"].links) == 1
        assert len(result.i["B"].links) == 1


class TestBooleanOperators:
    """Tests for &, |, ~, ^ operators using BooleanMath node."""

    def test_and(self):
        with TreeBuilder("TestAnd"):
            a = g.Boolean(True)
            b = g.Boolean(False)
            result = a & b

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "AND"
        assert len(result.node.inputs[0].links) == 1
        assert len(result.node.inputs[1].links) == 1

    def test_or(self):
        with TreeBuilder("TestOr"):
            a = g.Boolean(True)
            b = g.Boolean(False)
            result = a | b

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "OR"

    def test_xor(self):
        with TreeBuilder("TestXor"):
            a = g.Boolean(True)
            b = g.Boolean(False)
            result = a ^ b

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "XOR"

    def test_invert(self):
        with TreeBuilder("TestInvert"):
            a = g.Boolean(True)
            result = ~a

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "NOT"
        assert len(result.node.inputs[0].links) == 1

    def test_and_with_literal(self):
        with TreeBuilder("TestAndLiteral"):
            result = g.Boolean(True) & True

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "AND"

    def test_or_with_literal(self):
        with TreeBuilder("TestOrLiteral"):
            result = g.Boolean(True) | False

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "OR"

    def test_implicit_conversion(self):
        """Boolean operators should work on non-boolean sockets."""
        with TreeBuilder("TestImplicitBool"):
            result = g.Value(1.0) & g.Value(0.0)

        assert result.node.bl_idname == "FunctionNodeBooleanMath"
        assert result.node.operation == "AND"


class TestParameterizedOperators:
    """Parametric tests across multiple input types."""

    @pytest.mark.parametrize(
        "operator,input_cls",
        itertools.product(
            ["**", "%"],
            [g.Vector, g.Value],
        ),
    )
    def test_binary_operators_with_types(self, operator, input_cls):
        with TreeBuilder("TestParameterized"):
            node = input_cls()  # noqa: F841
            result = eval(f"node {operator} 2.0")

        assert result.node is not None
        match input_cls:
            case g.Vector:
                expected_op = "POWER" if operator == "**" else "MODULO"
                assert result.node.operation == expected_op
                # vec in input 0 (linked), scalar broadcast in input 1 (default)
                assert len(result.node.inputs[0].links) == 1
                assert tuple(result.node.inputs[1].default_value) == (2.0, 2.0, 2.0)
                assert len(result.node.inputs[1].links) == 0
            case g.Value:
                expected_op = "POWER" if operator == "**" else "FLOORED_MODULO"
                assert result.node.operation == expected_op
                # value in input 0 (linked), scalar in input 1 (default)
                assert len(result.node.inputs[0].links) == 1
                assert result.node.inputs[1].default_value == 2.0
                assert len(result.node.inputs[1].links) == 0

    @pytest.mark.parametrize("input_cls", [g.Vector, g.Value, g.Integer])
    def test_neg_all_types(self, input_cls):
        with TreeBuilder("TestNegAll"):
            result = -input_cls()

        assert result.node is not None
        match input_cls:
            case g.Integer:
                assert result.operation == "NEGATE"
                assert (
                    result.node.inputs[0].links[0].from_node.bl_idname
                    == "FunctionNodeInputInt"
                )
            case g.Value:
                assert result.operation == "MULTIPLY"
                assert result.node.inputs[1].default_value == -1.0
            case g.Vector:
                assert result.operation == "SCALE"
                assert result.node.inputs["Scale"].default_value == -1.0

    @pytest.mark.parametrize("input_cls", [g.Vector, g.Value, g.Integer])
    def test_abs_all_types(self, input_cls):
        with TreeBuilder("TestAbsAll"):
            result = abs(input_cls())

        assert result.node is not None
        assert result.operation == "ABSOLUTE"


class TestVectorScalarOperandOrder:
    """Tests that non-commutative vector-scalar operations have the correct operand order.

    For `vec ** 2.0`, the vector should be in input 0 and scalar (2,2,2) in input 1.
    For `2.0 ** vec` (reverse), the scalar should be in input 0 and vector in input 1.
    """

    def test_vector_sub_scalar_order(self):
        """vec - 2.0 should put vec in input 0, (2,2,2) in input 1."""
        with TreeBuilder("TestVecSubOrder"):
            vec = g.Vector((1, 2, 3))
            result = vec - 2.0

        # vec links into input 0, scalar default in input 1
        assert len(result.node.inputs[0].links) == 1
        assert tuple(result.node.inputs[1].default_value) == (2.0, 2.0, 2.0)

    def test_scalar_sub_vector_order(self):
        """2.0 - vec should put (2,2,2) in input 0, vec in input 1."""
        with TreeBuilder("TestScalarSubVecOrder"):
            vec = g.Vector((1, 2, 3))
            result = 2.0 - vec

        # scalar default in input 0, vec links into input 1
        assert tuple(result.i[0].default_value) == (2.0, 2.0, 2.0)
        assert len(result.i[1].links) == 1

    def test_vector_div_scalar_order(self):
        """vec / 2.0 should put vec in input 0, (2,2,2) in input 1."""
        with TreeBuilder("TestVecDivOrder"):
            vec = g.Vector((1, 2, 3))
            result = vec / 2.0

        assert len(result.i.vector.links) == 1
        assert tuple(result.i.vector_001.default_value) == (2.0, 2.0, 2.0)

    def test_scalar_div_vector_order(self):
        """2.0 / vec should put (2,2,2) in input 0, vec in input 1."""
        with TreeBuilder("TestScalarDivVecOrder"):
            vec = g.Vector((1, 2, 3))
            result = 2.0 / vec

        assert tuple(result.i[0].default_value) == (2.0, 2.0, 2.0)
        assert len(result.i[1].links) == 1

    def test_vector_pow_scalar_order(self):
        """vec ** 2.0 should put vec in input 0, (2,2,2) in input 1."""
        with TreeBuilder("TestVecPowOrder"):
            vec = g.Vector((1, 2, 3))
            result = vec**2.0

        assert len(result.node.inputs[0].links) == 1
        assert tuple(result.node.inputs[1].default_value) == (2.0, 2.0, 2.0)

    def test_scalar_pow_vector_order(self):
        """2.0 ** vec should put (2,2,2) in input 0, vec in input 1."""
        with TreeBuilder("TestScalarPowVecOrder"):
            vec = g.Vector((1, 2, 3))
            result = 2.0**vec

        assert tuple(result.node.inputs[0].default_value) == (2.0, 2.0, 2.0)
        assert len(result.node.inputs[1].links) == 1

    def test_vector_mod_scalar_order(self):
        """vec % 3.0 should put vec in input 0, (3,3,3) in input 1."""
        with TreeBuilder("TestVecModOrder"):
            vec = g.Vector((10, 20, 30))
            result = vec % 3.0

        assert len(result.node.inputs[0].links) == 1
        assert tuple(result.node.inputs[1].default_value) == (3.0, 3.0, 3.0)

    def test_scalar_mod_vector_order(self):
        """3.0 % vec should put (3,3,3) in input 0, vec in input 1."""
        with TreeBuilder("TestScalarModVecOrder"):
            vec = g.Vector((10, 20, 30))
            result = 3.0 % vec

        assert tuple(result.node.inputs[0].default_value) == (3.0, 3.0, 3.0)
        assert len(result.node.inputs[1].links) == 1


class TestComparisonEqualNotEqual:
    def test_comparison_equal(self):
        """Test equality comparison."""
        with TreeBuilder("TestCompareEqual"):
            val = g.Value(5.0)
            result = val == 5.0

        assert result.node.bl_idname == g.Compare._bl_idname
        assert result.node.operation == "EQUAL"
        assert result.node.data_type == "FLOAT"

    def test_comparison_not_equal(self):
        """Test inequality comparison."""
        with TreeBuilder("TestCompareNotEqual"):
            val = g.Integer(5)
            result = val != 5

        assert result.node.operation == "NOT_EQUAL"
        assert result.node.data_type == "INT"

    def test_comparison_float(self):
        """Test float comparison."""
        with TreeBuilder("TestCompareFloat"):
            result = (g.Integer(5) == 4).switch(5.0, g.RandomValue.integer())

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "FLOAT"

    def test_comparison_float_socket(self):
        """Test float comparison with socket."""
        with TreeBuilder("TestCompareFloatSocket"):
            result = (g.Integer(5) == 4).switch(g.Value(5.0), g.RandomValue.integer())

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "FLOAT"

    def test_comparison_returns_float(self):
        """Test comparison returns float."""
        with TreeBuilder("TestCompareReturnsFloat"):
            result = (g.Integer(5) == 4).switch(5.0, int(5))

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "FLOAT"

    def test_comparison_returns_int(self):
        """Test comparison returns float."""
        with TreeBuilder("TestCompareReturnsInt"):
            result = (g.Integer(5) == 4).switch(int(5), 0)

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "INT"

    def test_comparison_returns_str(self):
        """Test comparison returns string."""
        with TreeBuilder("TestCompareReturnsString"):
            result = (g.Integer(5) == 4).switch("some_string", "another_string")

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "STRING"

    def test_comparison_int(self):
        """Test int comparison."""
        with TreeBuilder("TestCompareInt"):
            result = (g.Integer(5) == 4).switch(int(5), g.RandomValue.integer())

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "INT"

    def test_comparison_bool(self):
        """Test int comparison."""
        with TreeBuilder("TestCompareInt"):
            result = (g.Integer(5) == 4).switch(False, True)

        assert result.node.bl_idname == g.Switch._bl_idname
        assert result.node.input_type == "BOOLEAN"

        with pytest.raises(ValueError, match="Cannot infer compatible type from"):
            with TreeBuilder("TestCompareInt"):
                # we don't automatically infer changing data types of string & numeric
                result = (g.Integer(5) == 4).switch("str", 5.0)

    def test_raise_warning(self):
        with pytest.raises(ValueError, match="Cannot infer compatible type from"):
            with TreeBuilder("TestCompareInt"):
                _ = (g.Integer(5) == 4).switch(list, int)

    def test_comparison_into_switch_node(self):
        """Test using a comparison result as a switch condition."""
        with TreeBuilder("TestCompareSwitch"):
            val = g.Integer(5)
            result = (val == 5) >> g.Switch.geometry(..., g.Cube(), g.IcoSphere())

        assert result.node.input_type == "GEOMETRY"
        assert (
            result.node.inputs["False"].links[0].from_node.bl_idname
            == g.Cube._bl_idname
        )
        assert (
            result.node.inputs["True"].links[0].from_node.bl_idname
            == g.IcoSphere._bl_idname
        )
        assert result.node.inputs[0].links[0].from_node.operation == "EQUAL"
        assert result.node.inputs[0].links[0].from_node.data_type == "INT"

    def test_comparison_with_switch(self):
        """Test using a comparison result as a switch condition."""
        with TreeBuilder("TestCompareSwitch"):
            val = g.Integer(5)
            result = (val == 5).switch(g.Cube(), g.IcoSphere())

        assert result.node.input_type == "GEOMETRY"
        assert (
            result.node.inputs["False"].links[0].from_node.bl_idname
            == g.Cube._bl_idname
        )
        assert (
            result.node.inputs["True"].links[0].from_node.bl_idname
            == g.IcoSphere._bl_idname
        )
        assert result.node.inputs[0].links[0].from_node.operation == "EQUAL"
        assert result.node.inputs[0].links[0].from_node.data_type == "INT"


class TestComparisonChaining:
    """Tests for comparison operators used in realistic node tree scenarios."""

    def test_comparison_into_selection(self):
        """Use a comparison result as a selection input."""
        with TreeBuilder("TestCompareSelection"):
            pos = g.Position()
            selection = g.SeparateXYZ(pos) > 0.0
            set_pos = g.SetPosition(selection=selection)

        assert set_pos.node.inputs["Selection"].links[0].from_node == selection.node

    def test_comparison_chain_with_boolean(self):
        """Combine comparison results with boolean operators."""
        with TreeBuilder("TestCompareBool"):
            val = g.Value(5.0)
            result = (val > 1.0) & (val < 10.0)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "AND"
        assert (
            result.node.inputs[0].links[0].from_node.bl_idname == g.Compare._bl_idname
        )
        assert (
            result.node.inputs[1].links[0].from_node.bl_idname == g.Compare._bl_idname
        )

    def test_comparison_or_chain(self):
        """Combine comparisons with OR: val < 1 or val > 10."""
        with TreeBuilder("TestCompareOr"):
            val = g.Value(5.0)
            result = (val < 1.0) | (val > 10.0)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "OR"
        lt_node = result.node.inputs[0].links[0].from_node
        gt_node = result.node.inputs[1].links[0].from_node
        assert lt_node.operation == "LESS_THAN"
        assert gt_node.operation == "GREATER_THAN"

    def test_comparison_negated(self):
        """Negate a comparison: ~(val > 5)."""
        with TreeBuilder("TestCompareNegated"):
            result = ~(g.Value(3.0) > 5.0)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "NOT"
        assert (
            result.node.inputs[0].links[0].from_node.bl_idname == g.Compare._bl_idname
        )

    def test_comparison_xor(self):
        """XOR two comparisons."""
        with TreeBuilder("TestCompareXor"):
            a = g.Value(1.0)
            b = g.Value(2.0)
            result = (a > 0.0) ^ (b > 0.0)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "XOR"

    def test_multi_condition_and_or(self):
        """Build (a > 0 & b > 0) | c > 0."""
        with TreeBuilder("TestMultiCondition"):
            a = g.Value(1.0)
            b = g.Value(2.0)
            c = g.Value(3.0)
            result = ((a > 0.0) & (b > 0.0)) | (c > 0.0)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "OR"
        and_node = result.node.inputs[0].links[0].from_node
        assert and_node.bl_idname == g.BooleanMath._bl_idname
        assert and_node.operation == "AND"

    def test_integer_comparison_with_boolean_ops(self):
        """Integer comparisons combined with boolean operators."""
        with TreeBuilder("TestIntCompareBool"):
            idx = g.Index()
            result = (idx >= 5) & (idx <= 100)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.node.operation == "AND"
        ge_node = result.node.inputs[0].links[0].from_node
        le_node = result.node.inputs[1].links[0].from_node
        assert ge_node.operation == "GREATER_EQUAL"
        assert ge_node.data_type == "INT"
        assert le_node.operation == "LESS_EQUAL"
        assert le_node.data_type == "INT"

    def test_comparison_into_switch(self):
        """Use a comparison as a switch condition."""
        with TreeBuilder("TestCompareSwitch"):
            condition = g.SplineParameter().o.length > 0.5
            switch = g.Switch.float(condition, 1.0, 2.0)

        assert switch.node.inputs["Switch"].links[0].from_node == condition.node

    def test_comparison_boolean_into_set_position(self):
        """Full pipeline: compare + boolean logic as selection for SetPosition."""
        with TreeBuilder("TestCompareBoolSetPos") as tree:
            pos = g.Position()
            xyz = g.SeparateXYZ(pos)
            # select points where x > 0 and z <= 1
            selection = (xyz > 0.0) & (g.SeparateXYZ(pos).o.z <= 1.0)
            _ = g.Cube() >> g.SetPosition(selection=selection, offset=(0, 0, 1))

        assert len(tree) >= 5

    def test_comparison_xyz(self):
        """Full pipeline: compare + boolean logic as selection for SetPosition."""
        with TreeBuilder("TestCompareBoolSetPos") as tree:
            pos = g.Position().o.position
            # select points where x > 0 and z <= 1
            selection = (pos.x > 0.0) & (pos.z <= 1.0)
            _ = g.Cube() >> g.SetPosition(selection=selection, offset=(0, 0, 1))

        assert len(tree) >= 5


class TestComplexExpressions:
    """Tests for complex expressions combining multiple operator types."""

    def test_math_expression_chain(self):
        """Test a complex math expression: (value ** 2 + 1) % 10."""
        with TreeBuilder("TestComplexMath"):
            val = g.Value(3.0)
            result = (val**2 + 1) % 10

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.node.operation == "FLOORED_MODULO"

    def test_vector_expression(self):
        """Test: position * 2 + offset, then floor divide."""
        with TreeBuilder("TestComplexVector"):
            pos = g.Position()
            result = (pos * 2 + (0, 0, 1)) // (1, 1, 1)

        assert result.node.bl_idname == g.VectorMath._bl_idname
        assert result.node.operation == "FLOOR"

    def test_negation_and_abs_chain(self):
        """Test: abs(-value) ** 2."""
        with TreeBuilder("TestNegAbsChain"):
            val = g.Value(5.0)
            result = abs(-val) ** 2

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.node.operation == "POWER"

    def test_selection_logic(self):
        """Build a selection from multiple conditions combined with boolean ops."""
        with TreeBuilder("TestSelectionLogic") as tree:
            idx = g.Index()
            selection = (idx > 5) & (idx < 100) & ~(idx > 50)
            _ = g.Points(200) >> g.SetPosition(selection=selection)

        assert len(tree) >= 6

    def test_operators_into_set_position(self):
        """Combine operators with >> chaining into a full node tree."""
        with TreeBuilder("TestOpsSetPos") as tree:
            with tree.inputs:
                i_geo = s.SocketGeometry()
            with tree.outputs:
                o_geo = s.SocketGeometry()

            pos = g.Position()
            offset = (pos**2) % (1, 1, 1)
            _ = i_geo >> g.SetPosition(offset=offset) >> o_geo

        assert len(tree.tree.links) >= 4

    def test_integer_floor_div_chain(self):
        """Test integer floor division chained with other operations."""
        with TreeBuilder("TestIntFloorDivChain"):
            idx = g.Index()
            result = (idx + 5) // 3

        assert result.node.bl_idname == g.IntegerMath._bl_idname
        assert result.node.operation == "DIVIDE_FLOOR"

    def test_full_workflow(self):
        """A complete workflow using many of the new operators."""
        with TreeBuilder("TestFullWorkflow") as tree:
            with tree.outputs:
                out = s.SocketGeometry()

            count = g.Integer(100)
            pos = g.Position()

            # Use comparison for selection
            selection = (g.Index() % 2) > 0

            # Use power and modulo for position
            offset = (pos**2) % (2, 2, 2)

            _ = (
                g.Points(count, position=g.RandomValue.vector(min=-1))
                >> g.SetPosition(selection=selection, offset=offset)
                >> out
            )

        assert len(tree) >= 8


class TestReverseOperators:
    """Tests for reverse (r) operator variants triggered when the left operand is a literal."""

    def test_rmul(self):
        with TreeBuilder("TestRMul"):
            result = 3.0 * g.Value(2.0)

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.operation == "MULTIPLY"

    def test_rtruediv(self):
        with TreeBuilder("TestRTrueDiv"):
            result = 10.0 / g.Value(2.0)

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.operation == "DIVIDE"
        assert result.i.value.default_value == 10.0

    def test_radd(self):
        with TreeBuilder("TestRAdd"):
            result = 5.0 + g.Value(3.0)

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.operation == "ADD"

    def test_rsub(self):
        with TreeBuilder("TestRSub"):
            result = 10.0 - g.Value(3.0)

        assert result.node.bl_idname == g.Math._bl_idname
        assert result.operation == "SUBTRACT"
        assert result.i.value.default_value == 10.0

    def test_rand(self):
        with TreeBuilder("TestRAnd"):
            result = True & g.Boolean(False)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.operation == "AND"

    def test_ror(self):
        with TreeBuilder("TestROr"):
            result = False | g.Boolean(True)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.operation == "OR"

    def test_rxor(self):
        with TreeBuilder("TestRXor"):
            result = True ^ g.Boolean(False)

        assert result.node.bl_idname == g.BooleanMath._bl_idname
        assert result.operation == "XOR"

    def test_matmul(self):
        with TreeBuilder("TestMatmul"):
            mat = np.random.rand(4, 4)
            a = g.CombineTransform(translation=(1, 0, 0))
            result = a @ mat
            result2 = mat @ a
        assert result.node.bl_idname == g.MultiplyMatrices._bl_idname
        assert result2.node.bl_idname == g.MultiplyMatrices._bl_idname
        assert np.allclose(
            mat.ravel(),
            [i.default_value for i in result.node.inputs[1].links[0].from_node.inputs],
        )
        assert np.allclose(
            mat.ravel(),
            [i.default_value for i in result2.node.inputs[0].links[0].from_node.inputs],
        )

    def test_rmatmul(self):
        with TreeBuilder("TestRMatmul"):
            a = g.CombineTransform(translation=(1, 0, 0))
            b = g.CombineTransform(rotation=(0, 90, 0))
            mat = np.random.rand(4, 4)
            # use the output socket as the left operand so Python calls b.__rmatmul__
            result = a.o.transform.socket @ b
            result2 = mat @ a

        assert result.node.bl_idname == g.MultiplyMatrices._bl_idname
        assert result2.node.bl_idname == g.MultiplyMatrices._bl_idname
        assert np.allclose(
            mat.ravel(),
            [i.default_value for i in result2.node.inputs[0].links[0].from_node.inputs],
        )

    def test_matrix_matmul_vector(self):
        """matrix @ vector should produce a TransformPoint node."""
        with TreeBuilder("TestMatrixMatmulVector") as tree:
            mat = g.CombineTransform(translation=(1, 0, 0))
            vec = g.Vector((1, 2, 3))
            result = mat @ vec
            result2 = mat @ np.random.rand(4, 4)
            _ = mat @ result2

        assert result.node.bl_idname == g.TransformPoint._bl_idname
        assert result.node.inputs[0].links[0].from_node == vec.node
        assert result.node.inputs[1].links[0].from_node == mat.node
        assert result2.node.inputs[0].links[0].from_node == mat.node
        assert (
            result2.node.inputs[1].links[0].from_node.bl_idname
            == g.CombineMatrix._bl_idname
        )

        with tree:
            with pytest.raises(nodebpy.builder.SocketError):
                _ = vec @ mat


class TestMatrixMultiplcation:
    def test_matrix_multiplication(self):
        """Test matrix multiplication."""
        with TreeBuilder("MatrixMultiplication") as tree:
            with tree.outputs:
                out = s.SocketGeometry()
            cube = g.Cube()
            _ = (
                g.SetPosition(
                    cube,
                    position=g.CombineTransform(rotation=(0, 90, 0))
                    @ g.CombineTransform(translation=(1, 0, 0))
                    @ g.Position(),
                )
                >> out
            )

        assert cube.o.mesh.links[0].to_node.bl_idname == g.SetPosition._bl_idname
        assert (
            cube.o.mesh.links[0].to_node.inputs["Position"].links[0].from_node.bl_idname  # type: ignore
            == g.TransformPoint._bl_idname
        )
        assert (
            cube.o.mesh.links[0]  # type: ignore
            .to_node.inputs["Position"]
            .links[0]
            .from_node.inputs["Transform"]
            .links[0]
            .from_node.bl_idname
            == g.MultiplyMatrices._bl_idname
        )


class TestColorSocketOperatorMath:
    def test_color_socket_operator_math(self):
        "Multiplies a color by a scalar and verifies the result is a VectorMath node."
        with g.tree("ColorSocketOperatorMath") as tree:
            color = tree.inputs.color("Color")
            result = color * 0.01

            result2 = color * g.Integer(1).o.integer
            result3 = int(1) * color
            result4 = color * g.Value(2.0)
            result5 = color ** g.Value(3.0)
            result6 = color * (0.1, 0.2, 0.3)
            result7 = color**0.1

        assert result.node.bl_idname == g.VectorMath._bl_idname
        assert result2.node.bl_idname == g.VectorMath._bl_idname
        assert result2.operation == "SCALE"
        assert result3.node.bl_idname == g.VectorMath._bl_idname
        assert result3.operation == "SCALE"
        assert result4.node.bl_idname == g.VectorMath._bl_idname
        assert result4.operation == "SCALE"
        assert result5.node.bl_idname == g.VectorMath._bl_idname
        assert result5.operation == "POWER"
        assert result6.node.bl_idname == g.VectorMath._bl_idname
        assert result6.operation == "MULTIPLY"
        assert result7.node.bl_idname == g.VectorMath._bl_idname
        assert result7.operation == "POWER"
        assert result7.i.vector_001.default_value == pytest.approx((0.1, 0.1, 0.1))


class TestIntegerSocketOperators:
    def test_integer_socket_operations(self):
        "Only Geometry Nodes has Integer Math node so for now we fallback on Math"
        with c.tree() as tree:
            input = tree.inputs.integer()
            result = -input
            assert result.node.bl_idname == c.Math._bl_idname
            assert result.operation == "MULTIPLY"
            assert result.i.value.links
            assert result.i.value.links[0].from_node == input.node
            assert not result.i.value_001.links
            assert result.i.value_001.default_value == pytest.approx(-1.0)
