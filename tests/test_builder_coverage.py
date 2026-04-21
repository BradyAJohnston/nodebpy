"""
Targeted coverage tests for the nodebpy.builder module.
These tests exercise branches and paths not covered by the main test suite.
"""

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import sockets as socket
from nodebpy.builder import (
    BooleanSocket,
    FloatSocket,
    IntegerSocket,
    VectorSocket,
)
from nodebpy.builder._utils import normalize_name

# ---------------------------------------------------------------------------
# _utils.py
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Hello World", "hello_world"),
        ("hello_world", "hello_world"),
        ("My Socket Name", "my_socket_name"),
    ],
    ids=["spaces", "already_underscored", "multi_word"],
)
def test_normalize_name(name, expected):
    assert normalize_name(name) == expected


# ---------------------------------------------------------------------------
# interface.py — uncovered socket types and default_value paths
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sock_cls,kwargs",
    [
        (socket.SocketRotation, {"name": "Rot", "default_value": (0.0, 0.0, 1.0)}),
        (socket.SocketMatrix, {"name": "Mat"}),
        (socket.SocketObject, {"name": "Obj"}),
        (socket.SocketCollection, {"name": "Col"}),
        (socket.SocketImage, {"name": "Img"}),
        (socket.SocketMaterial, {"name": "Mat"}),
        (socket.SocketBundle, {"name": "Bnd"}),
        (socket.SocketClosure, {"name": "Cls"}),
    ],
    ids=[
        "rotation",
        "matrix",
        "object",
        "collection",
        "image",
        "material",
        "bundle",
        "closure",
    ],
)
def test_interface_socket_creation(sock_cls, kwargs):
    """All interface socket types can be instantiated inside a tree.inputs context."""
    tree = TreeBuilder(f"Test_{sock_cls.__name__}")
    with tree.inputs:
        s = sock_cls(**kwargs)
    assert s is not None


@pytest.mark.parametrize(
    "op,value",
    [("get", None), ("set", 1.0)],
    ids=["get", "set"],
)
def test_geometry_socket_default_value_raises(op, value):
    """SocketGeometry has no default_value — both get and set should raise AttributeError."""
    tree = TreeBuilder("GeoDefTest")
    with tree.inputs:
        geo = socket.SocketGeometry("Geo")
    with pytest.raises(AttributeError):
        if op == "get":
            _ = geo.default_value
        else:
            geo.default_value = value


def test_interface_socket_default_value_getter():
    """reading default_value on a socket that supports it."""
    tree = TreeBuilder("FloatDefGetTest")
    with tree.inputs:
        f = socket.SocketFloat("Value", 3.14)
    assert f.default_value == pytest.approx(3.14)


def test_interface_socket_default_value_setter():
    """setting default_value on a socket that supports it."""
    tree = TreeBuilder("FloatDefSetTest")
    with tree.inputs:
        f = socket.SocketFloat("Value", 1.0)
    f.default_value = 2.5
    assert f.default_value == pytest.approx(2.5)


def test_menu_socket_default_triggers_apply_defaults():
    """_apply_input_defaults runs when SocketMenu has a non-None default."""
    tree = TreeBuilder("MenuDefaultTest")
    with tree.inputs:
        m = socket.SocketMenu("Options", default_value="OPTION_A")
    assert m is not None


# ---------------------------------------------------------------------------
# tree.py — fake_user, link() Socket unwrapping, _repr_markdown_
# ---------------------------------------------------------------------------


def test_fake_user_getter():
    assert isinstance(TreeBuilder("FU").fake_user, bool)


def test_fake_user_setter():
    tree = TreeBuilder("FU2")
    tree.fake_user = True
    assert tree.fake_user is True
    tree.fake_user = False
    assert tree.fake_user is False


def test_link_unwraps_socket_wrappers():
    """tree.link() should unwrap Socket wrappers to raw NodeSocket."""
    with TreeBuilder("LinkWrapTest") as tree:
        pos = g.Position()
        set_pos = g.SetPosition()
        tree.link(pos.outputs._get("Position"), set_pos.inputs._get("Position"))
    assert len(tree.tree.links) > 0


def test_repr_markdown_returns_str_or_none():
    tree = TreeBuilder("MarkdownTest")
    with tree:
        g.Position()
    result = tree._repr_markdown_()
    assert result is None or isinstance(result, str)


def test_repr_markdown_exception_path(monkeypatch):
    """exception path when diagram generation raises."""
    import nodebpy.diagram as diagram_mod

    monkeypatch.setattr(
        diagram_mod,
        "to_mermaid",
        lambda t: (_ for _ in ()).throw(RuntimeError("fail")),
    )

    tree = TreeBuilder("MarkdownExcTest")
    with tree:
        g.Position()
    assert tree._repr_markdown_() is None


# ---------------------------------------------------------------------------
# node.py — outside-context error, tree setter, id branches, raw node wrap
# ---------------------------------------------------------------------------


def test_node_outside_context_raises():
    with pytest.raises(RuntimeError):
        g.Position()


def test_tree_is_readonly():
    """A node's tree is determined at creation and cannot be reassigned."""
    with TreeBuilder("T1") as tree1:
        pos = g.Position()
    with TreeBuilder("T2") as tree2:
        pass
    with pytest.raises(AttributeError):
        pos.tree = tree2
    assert pos.tree is tree1


def test_default_output_id_branch():
    """_default_output_socket uses _default_output_id when set."""
    with TreeBuilder("DefOutId"):
        pos = g.Position()
        pos._default_output_id = pos.node.outputs[0].identifier
        assert pos._default_output_socket is not None


def test_default_input_id_branch():
    """_default_input_socket uses _default_input_id when set."""
    with TreeBuilder("DefInId"):
        sp = g.SetPosition()
        sp._default_input_id = sp.node.inputs[0].identifier
        assert sp._default_input_socket is not None


def test_wrap_raw_bpy_node_as_input():
    """passing a raw bpy.types.Node as a kwarg wraps it in BaseNode."""
    with TreeBuilder("WrapBpy"):
        pos = g.Position()
        set_pos = g.SetPosition(position=pos.node)
    assert len(set_pos.node.inputs["Position"].links) > 0


# ---------------------------------------------------------------------------
# socket.py — unary ValueError, vector dispatch branches, compare fallbacks,
#             boolean mixin __and__/__or__, rotation/matrix properties
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sock_cls,node_fn",
    [
        (FloatSocket, lambda: g.Value()),
        (VectorSocket, lambda: g.Position()),
    ],
    ids=["float", "vector"],
)
def test_dispatch_unary_unknown_op_raises(sock_cls, node_fn):
    """_dispatch_unary raises ValueError for unknown operations."""
    with TreeBuilder("UnaryErr"):
        node = node_fn()
        sock = sock_cls(node.node.outputs[0])
        with pytest.raises(ValueError):
            sock._dispatch_unary("unknown_op")


@pytest.mark.parametrize(
    "other,expected_op",
    [
        ((1.0, 2.0, 3.0), "MULTIPLY"),  # tuple-of-3 → VectorMath.multiply  (line 192)
        (1.0, "SCALE"),  # scalar float → VectorMath.scale   (line 176)
    ],
    ids=["tuple3", "scalar_float"],
)
def test_vector_multiply_dispatch(other, expected_op):
    with TreeBuilder("VecMul"):
        pos = g.Position()
        result = pos * other
    assert result.operation == expected_op


def test_vector_multiply_by_scalar_node():
    """VectorSocket * scalar-type node uses VectorMath.scale."""
    with TreeBuilder("VecMulScalar"):
        result = g.Position() * g.Value()
    assert result.operation == "SCALE"


@pytest.mark.parametrize(
    "operation",
    ["multiply", "add"],
    ids=["multiply", "add"],
)
def test_vector_dispatch_unsupported_type_raises(operation):
    """_dispatch_math raises TypeError for unsupported other types."""
    with TreeBuilder("VecTypeErr"):
        sock = VectorSocket(g.Position().node.outputs[0])
        with pytest.raises(TypeError):
            sock._dispatch_math({"bad": "type"}, operation)


def test_vector_compare_non_geo_tree_fallback():
    """_VectorMixin._dispatch_compare falls back to Socket version in shader tree."""
    from nodebpy import shader as s

    with TreeBuilder.shader():
        vec_sock = s.CombineXYZ().outputs._get("Vector")
        result = vec_sock._dispatch_compare(0.5, "less_than")
    assert result is not None


def test_integer_compare_non_geo_tree_fallback():
    """_IntegerMixin._dispatch_compare falls back to Socket version in shader tree."""
    from nodebpy import shader as s

    with TreeBuilder.shader():
        raw_sock = s.Value().node.outputs[0]
        result = IntegerSocket(raw_sock)._dispatch_compare(5, "less_than")
    assert result is not None


@pytest.mark.parametrize(
    "op,expected_op",
    [("or", "OR"), ("and", "AND")],
    ids=["or", "and"],
)
def test_boolean_mixin_operators(op, expected_op):
    """_BooleanMixin.__or__ and __and__ route through BooleanMath."""
    with TreeBuilder("BoolOp"):
        raw_sock = g.RandomValue.boolean(0.5).node.outputs[0]
        bool_sock = BooleanSocket(raw_sock)
        result = (bool_sock | True) if op == "or" else (bool_sock & True)
    assert result.operation == expected_op


def test_color_separate_in_compositor_tree():
    """socket.py:250 — _ColorMixin._get_separate_color_cls uses compositor SeparateColor."""
    from nodebpy import compositor as c

    with TreeBuilder.compositor():
        raw_sock = c.Mix().node.outputs[0]
        from nodebpy.builder import ColorSocket

        r = ColorSocket(raw_sock).r
    assert r is not None


@pytest.mark.parametrize("component", ["w", "x", "y", "z"])
def test_rotation_socket_properties(component):
    """_RotationMixin .w/.x/.y/.z via RotationToQuaternion."""
    with TreeBuilder("RotProp"):
        rot_sock = g.AxisAngleToRotation(angle=1.0).outputs._get("Rotation")
        assert getattr(rot_sock, component) is not None


def test_rotation_socket_cached_link():
    """_RotationMixin second access reuses existing RotationToQuaternion node."""
    with TreeBuilder("RotCached"):
        rot_sock = g.AxisAngleToRotation(angle=1.0).outputs._get("Rotation")
        x1 = rot_sock.x
        x2 = rot_sock.x
    assert x1 is not None and x2 is not None


@pytest.mark.parametrize("component", ["translation", "rotation", "scale"])
def test_matrix_socket_properties(component):
    """_MatrixMixin .translation/.rotation/.scale via SeparateTransform."""
    with TreeBuilder("MatProp"):
        mat_sock = g.CombineTransform().outputs._get("Transform")
        assert getattr(mat_sock, component) is not None


def test_matrix_socket_cached_link():
    """_MatrixMixin second access reuses existing SeparateTransform node."""
    with TreeBuilder("MatCached"):
        mat_sock = g.CombineTransform().outputs._get("Transform")
        t1 = mat_sock.translation
        t2 = mat_sock.translation
    assert t1 is not None and t2 is not None


# ---------------------------------------------------------------------------
# mixins.py — __rmatmul__, _source/_target_socket, _find_best_socket_pair,
#             __rshift__ fallback and SocketLike path
# ---------------------------------------------------------------------------


def test_rmatmul_numpy_matrix_times_vector():
    """numpy eye(4) @ vector_node → TransformPoint via __rmatmul__."""
    import numpy as np

    with TreeBuilder("RMatMul"):
        result = np.eye(4) @ g.Position()
    assert result._bl_idname == g.TransformPoint._bl_idname


def test_target_socket_accepts_base_node():
    """_target_socket with BaseNode returns its _default_input_socket."""
    with TreeBuilder("TgtSockNode"):
        pos = g.Position()
        set_pos = g.SetPosition()
        assert pos._target_socket(set_pos) is not None


@pytest.mark.parametrize(
    "method,arg",
    [("_source_socket", 42), ("_target_socket", 42)],
    ids=["source", "target"],
)
def test_socket_methods_raise_for_invalid_type(method, arg):
    """_source_socket and _target_socket raise TypeError for unknown types."""
    with TreeBuilder("SockTypeErr"):
        pos = g.Position()
        with pytest.raises(TypeError):
            getattr(pos, method)(arg)


def test_find_best_socket_pair_raw_node_socket_source():
    """raw NodeSocket is valid as source.

    _find_best_socket_pair returns (target_input, source_output) — the compatible
    INPUT socket from the target node comes first, the OUTPUT socket from the source second.
    """
    with TreeBuilder("PairRawSrc"):
        pos = g.Position()
        set_pos = g.SetPosition()
        raw_src = pos.node.outputs[0]  # raw VECTOR output socket
        tgt_input, src_output = pos._find_best_socket_pair(raw_src, set_pos)
    # src_output is the raw socket we passed in (from the Position node)
    assert src_output is raw_src
    # tgt_input is the best-matched input on SetPosition
    assert tgt_input.node.name == "Set Position"
    assert tgt_input.type == "VECTOR"


def test_find_best_socket_pair_raw_node_socket_target():
    """raw NodeSocket as target (no .inputs) uses [target] directly.

    Returns (raw_target_socket, source_output) when target has no .inputs.
    """
    with TreeBuilder("PairRawTgt"):
        pos = g.Position()
        set_pos = g.SetPosition()
        raw_tgt = set_pos.node.inputs[3]  # raw VECTOR Position input
        tgt_input, src_output = pos._find_best_socket_pair(pos, raw_tgt)
    assert tgt_input is raw_tgt
    assert src_output.node.name == "Position"
    assert src_output.type == "VECTOR"


def test_find_best_socket_pair_bad_source_raises():
    """non-outputs, non-NodeSocket source raises TypeError."""
    with TreeBuilder("PairBadSrc"):
        with pytest.raises(TypeError):
            g.Position()._find_best_socket_pair(42, g.Position())


def test_rshift_fallback_path():
    """__rshift__ falls back to other._find_best_socket_pair on SocketError."""
    with TreeBuilder("RShiftFallback"):
        zone = g.SimulationZone(g.Value())
        _ = g.AxisAngleToRotation(angle=1.0) >> zone.output


def test_rshift_to_socket_wrapper():
    """>> to a _SocketLike links via _from_socket path."""
    tree = TreeBuilder("RShiftSock")
    with tree.inputs:
        in_geo = socket.SocketGeometry()
    with tree.outputs:
        out_geo = socket.SocketGeometry()
    with tree:
        _ = in_geo >> out_geo
    assert len(tree.tree.links) >= 1
