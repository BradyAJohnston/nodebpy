"""Generate ``src/nodebpy/math.pyi``: typed overloads for :mod:`nodebpy.math`.

``python -m gen.math_stub`` rewrites the stub from ``nodebpy.math._SPECS``;
``tests/test_node_math.py`` fails while the checked-in stub is stale.

The overloads mirror ``nodebpy.math._resolve``:

- Promotable kinds (boolean → integer → float → vector) are tried in
  ascending order, each taking arguments of that kind or below, so the most
  general argument picks the result.
- Pinned kinds (matrix, rotation, color) take one argument of exactly that
  kind, as the runtime never promotes to them.
- A list or grid argument makes a list or grid result. Those overloads come
  before the field ones (``ColorSocketList`` is a ``ColorSocket``).
- A node argument has no static output type, so the last overloads take one
  and return ``Socket`` (or the one type every node returns). They also take
  ``Socket`` so those results chain, which lets a wrong-kind socket through
  to the runtime ``TypeError`` (``m.sqrt(vector_socket)``).

Integer results assume a geometry tree; elsewhere the runtime builds a float
Math node instead.
"""

from __future__ import annotations

import inspect
from pathlib import Path

STUB_PATH = Path(__file__).resolve().parents[1] / "src" / "nodebpy" / "math.pyi"

_LADDER = ("BOOLEAN", "INT", "FLOAT", "VECTOR")
_PINNED = ("MATRIX", "ROTATION", "COLOR")
_BASE = {
    "BOOLEAN": "Boolean",
    "INT": "Integer",
    "FLOAT": "Float",
    "VECTOR": "Vector",
    "COLOR": "Color",
    "ROTATION": "Rotation",
    "MATRIX": "Matrix",
}
_SOCKET_TYPE_KIND = {
    "VALUE": "FLOAT",
    "INT": "INT",
    "BOOLEAN": "BOOLEAN",
    "VECTOR": "VECTOR",
    "RGBA": "COLOR",
    "ROTATION": "ROTATION",
    "MATRIX": "MATRIX",
}
# plain values the runtime reads as each kind
_PLAIN = {
    "BOOLEAN": ["bool"],
    "INT": ["int"],
    "FLOAT": ["float"],
    "VECTOR": ["tuple[float, float, float]", "Vector"],
    "COLOR": ["tuple[float, float, float, float]"],
    "ROTATION": ["Euler", "Quaternion"],
    "MATRIX": ["Matrix"],
}
_GRID_KINDS = ("BOOLEAN", "INT", "FLOAT", "VECTOR")
# a node, raw socket or untyped ``Socket`` (what a node argument returns) has
# no static kind
_NODE = "BaseNode | NodeSocket | Socket"


def _exact(kind: str, structure: str) -> list[str]:
    cls = f"{_BASE[kind]}Socket{structure}"
    if structure == "":
        return [*_PLAIN[kind], cls]
    if structure == "Grid" and kind not in _GRID_KINDS:
        return []
    return [cls]


def _below(kind: str, available: set[str]) -> list[str]:
    """Kinds an argument may have when ``kind`` is picked."""
    if kind in _LADDER:
        kinds = list(_LADDER[: _LADDER.index(kind) + 1])
        if kind == "VECTOR" and "COLOR" not in available:
            kinds.append("COLOR")  # colors read as vectors
        return kinds
    lower = [*_LADDER, "COLOR", "ROTATION", "MATRIX"]
    return lower[: lower.index(kind) + 1]


_STRUCTURE_SUFFIX = {
    ("",): "",
    ("List",): "List",
    ("Grid",): "Grid",
    ("", "List"): "OrList",
    ("", "List", "Grid"): "Any",
}
# alias name → the union it stands for, filled while rendering
_ALIASES: dict[str, str] = {}


def _union(kinds: list[str], structures: tuple[str, ...]) -> str:
    """The argument type: one class, or an alias naming the union.

    ``_FloatLike`` is anything a float function promotes (booleans, integers,
    floats); ``_VectorColorLike`` adds colors read as vectors; ``…List``,
    ``…Grid``, ``…OrList`` (fields or lists) and ``…Any`` give the structure.
    """
    types = list(
        dict.fromkeys(t for k in kinds for s in structures for t in _exact(k, s))
    )
    if len(types) <= 1:
        return "".join(types)
    top = _BASE[kinds[-1]]
    if kinds[-1] == "COLOR" and "VECTOR" in kinds and len(kinds) == 5:
        top = "VectorColor"
    name = f"_{top}{'Like' if len(kinds) > 1 else ''}{_STRUCTURE_SUFFIX[structures]}"
    union = " | ".join(types)
    if _ALIASES.setdefault(name, union) != union:
        raise ValueError(f"alias {name} names two unions")
    return name


def _output_bases() -> dict[tuple[str, str], str]:
    """(function, kind) → base class name of the socket it returns."""
    import bpy

    import nodebpy.math as m
    from nodebpy import geometry as g

    bases: dict[tuple[str, str], str] = {}
    with g.tree("_math_stub") as tree:
        for name, spec in m._SPECS.items():
            for kind, impl in spec.impls.items():
                socket = getattr(m._impl_callable(impl)().o, impl.output)
                bases[name, kind] = _BASE[_SOCKET_TYPE_KIND[socket.socket.type]]
    bpy.data.node_groups.remove(tree.tree)
    return bases


def _params(name: str) -> list[tuple[str, str, bool, bool]]:
    """(name, annotation for a fixed argument, has default, dispatches)."""
    import nodebpy.math as m

    spec = m._SPECS[name]
    impl = next(iter(spec.impls.values()))
    factory_params = m._impl_params(impl)
    factory_sig = inspect.signature(m._impl_callable(impl)).parameters
    result = []
    for index, param in enumerate(
        inspect.signature(getattr(m, name)).parameters.values()
    ):
        annotation = factory_sig[factory_params[index]].annotation
        dispatches = spec.dispatch is None or index in spec.dispatch
        result.append(
            (param.name, str(annotation), param.default is not param.empty, dispatches)
        )
    return result


def _signature(params, types: dict[int, str], returns: str) -> str:
    parts = []
    for index, (pname, fixed, has_default, _) in enumerate(params):
        annotation = types.get(index, fixed)
        parts.append(f"{pname}: {annotation}" + (" = ..." if has_default else ""))
    return f"({', '.join(parts)}) -> {returns}: ..."


def _overloads(name: str, bases: dict[tuple[str, str], str]) -> list[str]:
    import nodebpy.math as m

    available = set(m._SPECS[name].impls)
    params = _params(name)
    slots = [i for i, p in enumerate(params) if p[3]]
    sigs: list[str] = []

    def add(types: dict[int, str], returns: str) -> None:
        sig = _signature(params, types, returns)
        if sig not in sigs:
            sigs.append(sig)

    kinds = [k for k in _LADDER if k in available] + [
        k for k in _PINNED if k in available
    ]
    for kind in kinds:
        below = _below(kind, available)
        base = bases[name, kind]
        pinned = kind in _PINNED
        lead = [kind] if pinned else below
        for structure, others in (
            ("Grid", ("", "List", "Grid")),
            ("List", ("", "List")),
        ):
            if (
                base not in ("Boolean", "Integer", "Float", "Vector")
                and structure == "Grid"
            ):
                continue
            leads = _union(lead, (structure,))
            if not leads:
                continue
            for slot in slots:
                types = {i: _union(below, others) for i in slots}
                types[slot] = leads
                add(types, f"{base}Socket{structure}")
        if pinned:
            for slot in slots:
                types = {i: _union(below, ("",)) for i in slots}
                types[slot] = _union([kind], ("",))
                add(types, f"{base}Socket")
        else:
            add({i: _union(below, ("",)) for i in slots}, f"{base}Socket")

    # nodes: the output type is only known at runtime
    returns = {bases[name, k] for k in available}
    node_return = f"{returns.pop()}Socket" if len(returns) == 1 else "Socket"
    anything = _union(
        [
            k
            for k in (*_LADDER, "COLOR", "ROTATION", "MATRIX")
            if any(k in _below(a, available) for a in available)
        ],
        ("", "List", "Grid"),
    )
    for slot in slots:
        types = {i: f"{anything} | {_NODE}" for i in slots}
        types[slot] = _NODE
        add(types, node_return)
    return [f"@overload\ndef {name}{sig}" for sig in sigs]


_HEADER = '''"""Typed overloads for nodebpy.math. Generated by ``python -m gen.math_stub``
from ``nodebpy.math._SPECS``; do not edit."""

from collections.abc import Sequence
from typing import Any, NamedTuple, overload

from bpy.types import NodeSocket
from mathutils import Euler, Matrix, Quaternion, Vector

from .builder.node import BaseNode
from .builder.socket import (
    BooleanSocket,
    BooleanSocketGrid,
    BooleanSocketList,
    ColorSocket,
    ColorSocketList,
    FloatSocket,
    FloatSocketGrid,
    FloatSocketList,
    IntegerSocket,
    IntegerSocketGrid,
    IntegerSocketList,
    MatrixSocket,
    MatrixSocketList,
    ResultMatrixSVD,
    RotationSocket,
    RotationSocketList,
    Socket,
    VectorSocket,
    VectorSocketGrid,
    VectorSocketList,
)
from .types import InputBoolean, InputFloat

__all__ = {all_names}

pi: float
tau: float
e: float

# used by nodebpy.export.codegen
class _Impl(NamedTuple):
    cls: str
    factory: str | None
    output: str
    params: tuple[str, ...] | None = None

class _Spec(NamedTuple):
    impls: dict[str, _Impl]
    dispatch: tuple[int, ...] | None = None

_SPECS: dict[str, _Spec]
_SOCKET_KINDS: dict[str, str]

def _value_kind(value: Any) -> str | None: ...
def _resolve(name: str, kinds: Sequence[str | None], geometry: bool) -> str: ...
def _dispatch_kinds(name: str, args: Sequence[Any]) -> list[Any]: ...
def _impl_params(impl: _Impl) -> tuple[str, ...]: ...
def _impl_class(impl: _Impl) -> type[BaseNode]: ...
def _impl_callable(impl: _Impl) -> Any: ...

def svd(
    x: MatrixSocket | BaseNode | NodeSocket | Socket,
) -> ResultMatrixSVD[MatrixSocket, VectorSocket]: ...
@overload
def matmul(a: MatrixSocket | Matrix, b: MatrixSocket | Matrix) -> MatrixSocket: ...
@overload
def matmul(
    a: MatrixSocket | Matrix, b: VectorSocket | Vector | tuple[float, float, float]
) -> VectorSocket: ...
@overload
def matmul(a: RotationSocket, b: RotationSocket | Euler | Quaternion) -> RotationSocket: ...
@overload
def matmul(
    a: RotationSocket, b: VectorSocket | Vector | tuple[float, float, float]
) -> VectorSocket: ...
@overload
def matmul(
    a: VectorSocket | Vector | tuple[float, float, float],
    b: VectorSocket | Vector | tuple[float, float, float],
) -> FloatSocket: ...
@overload
def matmul(a: BaseNode | NodeSocket | Socket, b: Any) -> Socket: ...
@overload
def matmul(a: Any, b: BaseNode | NodeSocket | Socket) -> Socket: ...
'''


def render() -> str:
    """The stub's source, formatted."""
    import subprocess

    from ruff import find_ruff_bin

    import nodebpy.math as m

    bases = _output_bases()
    _ALIASES.clear()
    functions = ["\n".join(_overloads(name, bases)) for name in m._SPECS]
    aliases = "\n".join(f"type {name} = {union}" for name, union in _ALIASES.items())
    header = _HEADER.replace("{all_names}", repr(list(m.__all__)))
    blocks = [header, aliases, *functions]
    # format as `make format` does, with the repo's config
    return subprocess.run(
        [find_ruff_bin(), "format", "--stdin-filename", str(STUB_PATH), "-"],
        input="\n\n".join(blocks) + "\n",
        capture_output=True,
        encoding="utf-8",
        check=True,
        cwd=STUB_PATH.parents[2],
    ).stdout


def main() -> None:
    STUB_PATH.write_text(render())
    print(f"wrote {STUB_PATH}")


if __name__ == "__main__":
    main()
