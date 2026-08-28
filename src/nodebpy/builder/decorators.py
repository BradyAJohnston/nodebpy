"""Decorators that turn a build function into a reusable group node.

The decorated function's parameters become the group's interface inputs,
typed by their annotations and defaulted from the signature; whatever it
returns becomes the interface outputs. Calling the decorated function inside a
tree context adds a group node and links or sets its inputs from the
arguments, exactly like calling a :class:`CustomGeometryGroup` subclass.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, cast

from bpy.types import NodeSocket

from .. import types as t
from ._utils import _NodeLike, _SocketLike, denormalize_name
from .node import (
    CustomCompositorGroup,
    CustomGeometryGroup,
    CustomShaderGroup,
    NodeGroupBuilder,
)
from .tree import TreeBuilder

# Parameter annotation -> the InputInterfaceContext method declaring that socket.
_SOCKET_METHODS: dict[str, str] = {
    "int": "integer",
    "float": "float",
    "bool": "boolean",
    "str": "string",
    "InputInteger": "integer",
    "InputFloat": "float",
    "InputBoolean": "boolean",
    "InputString": "string",
    "InputVector": "vector",
    "InputColor": "color",
    "InputRotation": "rotation",
    "InputMatrix": "matrix",
    "InputGeometry": "geometry",
    "InputObject": "object",
    "InputCollection": "collection",
    "InputMaterial": "material",
    "InputImage": "image",
    "InputShader": "shader",
    "InputBundle": "bundle",
    "InputClosure": "closure",
}
_ANNOTATION_NAMES: dict[Any, str] = {
    int: "int",
    float: "float",
    bool: "bool",
    str: "str",
}
_ANNOTATION_NAMES.update(
    {getattr(t, name): name for name in _SOCKET_METHODS if name.startswith("Input")}
)

# Blender socket ``type`` of a returned socket -> the OutputInterfaceContext
# method declaring the matching output.
_OUTPUT_METHODS: dict[str, str] = {
    "VALUE": "float",
    "FLOAT": "float",
    "INT": "integer",
    "BOOLEAN": "boolean",
    "VECTOR": "vector",
    "RGBA": "color",
    "ROTATION": "rotation",
    "MATRIX": "matrix",
    "STRING": "string",
    "MENU": "menu",
    "OBJECT": "object",
    "GEOMETRY": "geometry",
    "COLLECTION": "collection",
    "IMAGE": "image",
    "MATERIAL": "material",
    "BUNDLE": "bundle",
    "CLOSURE": "closure",
    "SHADER": "shader",
}


def _socket_method(fn: Any, param: inspect.Parameter) -> str:
    annotation = param.annotation
    if isinstance(annotation, str):
        key: str | None = annotation.rsplit(".", 1)[-1]
    else:
        key = _ANNOTATION_NAMES.get(annotation)
    method = _SOCKET_METHODS.get(key) if key is not None else None
    if method is None:
        raise TypeError(
            f"Parameter '{param.name}' of '{fn.__qualname__}' needs a socket type "
            f"annotation (e.g. int, float, InputGeometry) to become a group input; "
            f"got {annotation!r}."
        )
    return method


def _add_outputs(fn: Any, tree: TreeBuilder, result: Any) -> None:
    """Declare and link one interface output per returned socket.

    A single socket/node, a tuple of them, or a ``{name: socket}`` dict.
    Un-named outputs take the name of the socket they come from.
    """
    if result is None:
        return
    if isinstance(result, dict):
        items = list(result.items())
    elif isinstance(result, tuple):
        items = [(None, value) for value in result]
    else:
        items = [(None, result)]

    seen: set[str] = set()
    for name, value in items:
        if isinstance(value, NodeSocket):
            socket = value
        elif isinstance(value, (_SocketLike, _NodeLike)):
            socket = value._default_output_socket
        else:
            raise TypeError(
                f"'{fn.__qualname__}' returned {value!r}, which is not a socket or "
                "node and so cannot become a group output."
            )
        method = _OUTPUT_METHODS.get(socket.type)
        if method is None:
            raise TypeError(
                f"'{fn.__qualname__}' returned a {socket.type} socket, which cannot "
                "be a group output."
            )
        name = name or socket.name
        if name in seen:
            raise TypeError(
                f"'{fn.__qualname__}' returned two outputs named '{name}'; return a "
                "dict to name them explicitly."
            )
        seen.add(name)
        output = getattr(tree.outputs, method)(name)
        tree.link(socket, output.socket)


def _group_decorator[G: NodeGroupBuilder](base: type[G], name: str | None):
    def decorator[**P](fn: Callable[P, Any]) -> Callable[P, G]:
        meta: Any = fn
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        for p in params:
            if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                raise TypeError(
                    f"'{meta.__qualname__}' cannot use *args/**kwargs: each parameter "
                    "becomes a named group input."
                )
        methods = {p.name: _socket_method(fn, p) for p in params}

        def _build_group(self, tree: TreeBuilder) -> None:
            sockets = {}
            for p in params:
                kwargs = {}
                if p.default not in (p.empty, ..., None):
                    kwargs["default_value"] = p.default
                add_socket = getattr(tree.inputs, methods[p.name])
                sockets[p.name] = add_socket(denormalize_name(p.name), **kwargs)
            bound = sig.bind(**sockets)
            _add_outputs(fn, tree, fn(*bound.args, **bound.kwargs))

        group = cast(
            "type[G]",
            type(
                meta.__name__,
                (base,),
                {
                    "_name": name or denormalize_name(meta.__name__),
                    "_build_group": _build_group,
                    "__doc__": meta.__doc__,
                    "__module__": meta.__module__,
                    "__qualname__": meta.__qualname__,
                },
            ),
        )

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> G:
            bound = sig.bind_partial(*args, **kwargs)
            return group(**bound.arguments)

        return wrapper

    return decorator


def geometry_tree(name: str | None = None):
    """Turn a build function into a reusable geometry node group.

    Every parameter becomes an interface input whose socket type comes from
    the annotation and whose default comes from the signature; inside the
    function the parameters are those input sockets. Whatever the function
    returns (a socket or node, a tuple of them, or a ``{name: socket}`` dict)
    becomes the interface outputs. The group is built once (on first call)
    and cached by ``name`` in ``bpy.data.node_groups``; each call adds a group
    node to the active tree and links or sets its inputs from the arguments.
    """
    return _group_decorator(CustomGeometryGroup, name)


def shader_tree(name: str | None = None):
    """Turn a build function into a reusable shader node group.

    See :func:`geometry_tree`.
    """
    return _group_decorator(CustomShaderGroup, name)


def compositor_tree(name: str | None = None):
    """Turn a build function into a reusable compositor node group.

    See :func:`geometry_tree`.
    """
    return _group_decorator(CustomCompositorGroup, name)
