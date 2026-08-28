"""Decorators that turn a build function into a reusable group node.

The decorated function's parameters (after the leading ``tree``) become the
group's interface inputs, typed by their annotations and defaulted from the
signature. Calling the decorated function inside a tree context adds a group
node and links or sets its inputs from the arguments, exactly like calling a
:class:`CustomGeometryGroup` subclass.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, Concatenate, cast

from .. import types as t
from ._utils import denormalize_name
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


def _group_decorator[G: NodeGroupBuilder](base: type[G], name: str | None):
    def decorator[**P](
        fn: Callable[Concatenate[TreeBuilder[Any], P], Any],
    ) -> Callable[P, G]:
        meta: Any = fn
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())[1:]
        for p in params:
            if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                raise TypeError(
                    f"'{meta.__qualname__}' cannot use *args/**kwargs: each parameter "
                    "becomes a named group input."
                )
        methods = {p.name: _socket_method(fn, p) for p in params}
        call_sig = sig.replace(parameters=params)

        def _build_group(self, tree: TreeBuilder) -> None:
            sockets = {}
            for p in params:
                kwargs = {}
                if p.default not in (p.empty, ..., None):
                    kwargs["default_value"] = p.default
                add_socket = getattr(tree.inputs, methods[p.name])
                sockets[p.name] = add_socket(denormalize_name(p.name), **kwargs)
            bound = call_sig.bind(**sockets)
            fn(tree, *bound.args, **bound.kwargs)

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
            bound = call_sig.bind_partial(*args, **kwargs)
            return group(**bound.arguments)

        cast(Any, wrapper).__signature__ = call_sig
        return wrapper

    return decorator


def geometry_tree(name: str | None = None):
    """Turn a build function into a reusable geometry node group.

    The function receives the group's ``TreeBuilder`` first; every other
    parameter becomes an interface input whose socket type comes from the
    annotation and whose default comes from the signature. The group is built
    once (on first call) and cached by ``name`` in ``bpy.data.node_groups``;
    each call adds a group node to the active tree and links or sets its
    inputs from the arguments.
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
