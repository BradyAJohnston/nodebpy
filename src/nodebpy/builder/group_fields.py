"""Declarative socket fields for custom node groups.

A single field declaration replaces the four places a socket used to be
repeated (the ``_Inputs``/``_Outputs`` accessor entry, the ``__init__``
signature, the ``py-name -> display-name`` mapping, and the
``tree.inputs.*`` interface call)::

    class OtherVertex(CustomGeometryGroup):
        vertex_index: IntegerIn = IntegerIn(default_input="INDEX")
        edge_number:  IntegerIn = IntegerIn(0)

        class _Outputs:
            other_vertex: IntegerOut = IntegerOut()

The input fields are read by ``@dataclass_transform`` to synthesise a fully
typed constructor; ``__get__``/``__set__`` give precise socket types for
``self.i.x`` / ``node.i.x`` access; and the field metadata drives the
node-group interface that is built on first use.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar


if TYPE_CHECKING:
    pass

_V = TypeVar("_V")
_S = TypeVar("_S")

_UNSET: Any = object()


class _SocketField(Generic[_V, _S]):
    """Metadata + descriptor base for a single custom-group socket.

    Subclasses bind the two type parameters and set ``_method`` to the name of
    the :class:`~nodebpy.builder.tree.SocketContext` factory (``"integer"``,
    ``"vector"`` …) used to build the interface socket.
    """

    _method: str

    def __init__(
        self,
        default: Any = _UNSET,
        *,
        name: str | None = None,
        doc: str = "",
        panel: str | None = None,
        panel_closed: bool = False,
        **props: Any,
    ) -> None:
        self._default = default
        self._name_override = name
        self._doc = doc
        self._panel = panel
        self._panel_closed = panel_closed
        self._props = props
        self._attr = ""

    def __set_name__(self, owner: type, attr: str) -> None:
        self._attr = attr

    @property
    def display_name(self) -> str:
        """The Blender socket name, derived from the attribute unless overridden."""
        from ._utils import denormalize_name

        return self._name_override or denormalize_name(self._attr)

    def _build_kwargs(self) -> tuple[list[Any], dict[str, Any]]:
        """Positional/keyword args for the matching ``tree.inputs/outputs`` call."""
        args: list[Any] = [self.display_name]
        if self._default is not _UNSET:
            args.append(self._default)
        kwargs: dict[str, Any] = dict(self._props)
        if self._doc:
            kwargs.setdefault("description", self._doc)
        return args, kwargs


class InputField(_SocketField[_V, _S]):
    """An input socket: a constructor parameter and a ``self.i`` entry."""

    def __get__(self, obj: Any, owner: Any = None) -> _S:
        if obj is None:
            return self  # ty: ignore[invalid-return-type]
        # obj.i is a (build-aware) SocketAccessor; it resolves the live socket
        # and wraps it in the concrete Socket subclass for this type.
        return obj.i._get(self.display_name)

    def __set__(self, obj: Any, value: _V) -> None:
        obj._establish_links(**{self.display_name: value})


class OutputField(_SocketField[Any, _S]):
    """An output socket: a ``self.o`` entry, linked into with ``>>``."""

    def __get__(self, obj: Any, owner: Any = None) -> _S:
        if obj is None:
            return self  # ty: ignore[invalid-return-type]
        return obj._get(self.display_name)


# ---------------------------------------------------------------------------
# Concrete per-type fields. ``_method`` names a SocketContext factory; the type
# parameters are ``[constructor-input-union, socket-class]`` for inputs and
# ``[socket-class]`` for outputs.
# ---------------------------------------------------------------------------


class IntegerIn(InputField["InputInteger", "IntegerSocket"]):
    _method = "integer"


class FloatIn(InputField["InputFloat", "FloatSocket"]):
    _method = "float"


class VectorIn(InputField["InputVector", "VectorSocket"]):
    _method = "vector"


class BooleanIn(InputField["InputBoolean", "BooleanSocket"]):
    _method = "boolean"


class ColorIn(InputField["InputColor", "ColorSocket"]):
    _method = "color"


class RotationIn(InputField["InputRotation", "RotationSocket"]):
    _method = "rotation"


class ObjectIn(InputField["InputObject", "ObjectSocket"]):
    _method = "object"


class MenuIn(InputField["InputMenu", "MenuSocket"]):
    _method = "menu"


class GeometryIn(InputField["InputGeometry", "GeometrySocket"]):
    _method = "geometry"


class StringIn(InputField["InputString", "StringSocket"]):
    _method = "string"


class IntegerOut(OutputField["IntegerSocket"]):
    _method = "integer"


class IntegerListOut(OutputField["IntegerSocketList"]):
    _method = "integer"


class FloatOut(OutputField["FloatSocket"]):
    _method = "float"


class VectorOut(OutputField["VectorSocket"]):
    _method = "vector"


class BooleanOut(OutputField["BooleanSocket"]):
    _method = "boolean"


class ColorOut(OutputField["ColorSocket"]):
    _method = "color"


class RotationOut(OutputField["RotationSocket"]):
    _method = "rotation"


class GeometryOut(OutputField["GeometrySocket"]):
    _method = "geometry"


class StringOut(OutputField["StringSocket"]):
    _method = "string"


_INPUT_FIELDS = (
    IntegerIn,
    FloatIn,
    VectorIn,
    BooleanIn,
    ColorIn,
    RotationIn,
    ObjectIn,
    MenuIn,
    GeometryIn,
    StringIn,
)
