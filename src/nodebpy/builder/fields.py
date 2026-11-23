"""Custom node groups declared as class fields.

A group's interface is written once, as typed fields on the class::

    class Jitter(GeometryGroup):
        geometry: GeometryInput = GeometryInput(default=None)
        amount: FloatInput = FloatInput(default=0.2, min_value=0.0)
        result: ClassVar[GeometryOutput] = GeometryOutput(name="Geometry")

        def build(self) -> None:
            offset = g.RandomValue.vector(min=-1) * self.amount
            _ = self.geometry >> g.SetPosition(offset=offset) >> self.result

Input fields are dataclass-style fields (``typing.dataclass_transform``), so
type checkers give the class an ``__init__`` taking ``geometry: InputGeometry``
and ``amount: InputFloat``. Inside :meth:`build` each field reads as the
group's interface socket (``FloatSocket``, ...); on a group node it reads as
that node's socket, so it can be linked into (``x >> node.amount``) or set
(``node.amount = 0.5``). Output fields are not ``__init__`` parameters: link
into them inside :meth:`build`, read them on the node. ``with Panel(...)`` in
the class body puts the fields declared inside it in an interface panel.

Write ``default=`` by keyword: pyright only treats a field as optional when
its ``default`` is passed by keyword. Annotate outputs ``ClassVar[...]``: they
are not ``__init__`` parameters, and pyrefly / basedpyright reject an
unannotated attribute on a dataclass-like class. mypy does not see fields
declared inside a ``with`` block, so it misses inputs declared in a panel.
"""

from __future__ import annotations

import inspect
import re
from contextlib import ExitStack
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Self,
    cast,
    dataclass_transform,
    overload,
)

import bpy

from ..types import (
    InputBoolean,
    InputBundle,
    InputClosure,
    InputCollection,
    InputColor,
    InputFloat,
    InputFont,
    InputGeometry,
    InputImage,
    InputInteger,
    InputMaterial,
    InputMatrix,
    InputMenu,
    InputObject,
    InputRotation,
    InputShader,
    InputSound,
    InputString,
    InputVector,
)
from ._utils import denormalize_name
from .node import (
    CustomCompositorGroup,
    CustomGeometryGroup,
    CustomShaderGroup,
    NodeGroupBuilder,
)
from .socket import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    FloatSocket,
    FontSocket,
    GeometrySocket,
    ImageSocket,
    IntegerSocket,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    ShaderSocket,
    SoundSocket,
    StringSocket,
    VectorSocket,
)

if TYPE_CHECKING:
    from .tree import TreeBuilder

__all__ = [
    "BooleanInput",
    "BooleanOutput",
    "BundleInput",
    "BundleOutput",
    "ClosureInput",
    "ClosureOutput",
    "CollectionInput",
    "CollectionOutput",
    "ColorInput",
    "ColorOutput",
    "CompositorGroup",
    "FloatInput",
    "FloatOutput",
    "FontInput",
    "FontOutput",
    "GeometryGroup",
    "GeometryInput",
    "GeometryOutput",
    "ImageInput",
    "ImageOutput",
    "IntegerInput",
    "IntegerOutput",
    "MaterialInput",
    "MaterialOutput",
    "MatrixInput",
    "MatrixOutput",
    "MenuInput",
    "MenuOutput",
    "ObjectInput",
    "ObjectOutput",
    "Panel",
    "RotationInput",
    "RotationOutput",
    "ShaderGroup",
    "ShaderInput",
    "ShaderOutput",
    "SoundInput",
    "SoundOutput",
    "StringInput",
    "StringOutput",
    "VectorInput",
    "VectorOutput",
]

# Panels open while a class body runs: a field takes the innermost one.
_OPEN_PANELS: list[Panel] = []


class Panel:
    """Interface panel for the fields declared inside ``with Panel(...)`` in a
    group's class body. Panels nest, and may hold inputs and outputs."""

    def __init__(
        self, name: str, *, description: str = "", default_closed: bool = False
    ) -> None:
        self.name = name
        self.description = description
        self.default_closed = default_closed
        self.parent: Panel | None = None

    def __enter__(self) -> Self:
        self.parent = _OPEN_PANELS[-1] if _OPEN_PANELS else None
        _OPEN_PANELS.append(self)
        return self

    def __exit__(self, *exc: object) -> None:
        _OPEN_PANELS.pop()

    def _chain(self) -> list[Panel]:
        return [*(self.parent._chain() if self.parent else []), self]

    def __repr__(self) -> str:
        return f"Panel({self.name!r})"


class _Field[S]:
    """A group interface socket declared on the class. Reads as the interface
    socket ``S`` while the group builds, and as the group node's socket after."""

    _method: ClassVar[str]  # the tree.inputs / tree.outputs factory
    _is_input: ClassVar[bool]

    def __init__(
        self, default: Any = None, *, name: str | None, description: str, **options: Any
    ) -> None:
        self._default = default
        self._name = name
        self._description = description
        self._options = options
        self._panel = _OPEN_PANELS[-1] if _OPEN_PANELS else None
        self._attr = ""
        self._label = ""

    def __set_name__(self, owner: type, attr: str) -> None:
        self._attr = attr
        self._label = self._name or denormalize_name(attr)
        if self._options.get("is_panel_toggle"):
            if self._panel is None:
                raise TypeError(
                    f"{owner.__name__}.{attr}: a panel toggle must be declared "
                    "inside `with Panel(...)`."
                )
            # Blender names a panel's toggle socket after the panel.
            self._label = self._panel.name

    @overload
    def __get__(self, obj: None, owner: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: object, owner: type | None = None) -> S: ...
    def __get__(self, obj: object, owner: type | None = None) -> Any:
        if obj is None:
            return self
        building = obj.__dict__.get("_field_sockets")
        if building is not None:
            return building[self._attr]
        group = cast(NodeGroupBuilder, obj)
        return (group.i if self._is_input else group.o)[self._label]

    def _declare(
        self,
        tree: TreeBuilder[Any],
        panels: dict[Panel, bpy.types.NodeTreeInterfacePanel],
    ) -> Any:
        with ExitStack() as stack:
            for panel in self._panel._chain() if self._panel else []:
                context = stack.enter_context(
                    tree.panel(
                        panels.get(panel, panel.name),
                        description=panel.description,
                        default_closed=panel.default_closed,
                        reuse=False,
                    )
                )
                assert context.panel is not None
                panels[panel] = context.panel
            sockets = tree.inputs if self._is_input else tree.outputs
            kwargs = dict(self._options)
            if self._is_input and self._default is not None:
                kwargs["default_value"] = self._default
            return getattr(sockets, self._method)(
                self._label, description=self._description, **kwargs
            )


class _InputField[S, V](_Field[S]):
    """An input field: an ``__init__`` parameter taking ``V``."""

    _is_input = True

    def __set__(self, obj: object, value: V) -> None:
        if obj.__dict__.get("_field_sockets") is not None:
            raise AttributeError(
                f"Inputs can't be assigned inside build(); "
                f"'{self._attr}' is the group's interface socket."
            )
        cast(NodeGroupBuilder, obj)._establish_links(**{self._label: cast(Any, value)})


class _OutputField[S](_Field[S]):
    """An output field: link into it inside ``build()``."""

    _is_input = False

    def __init__(self, *, name: str | None = None, description: str = "") -> None:
        super().__init__(name=name, description=description)


# -- inputs -------------------------------------------------------------------


class FloatInput(_InputField[FloatSocket, InputFloat]):
    _method = "float"

    def __init__(
        self,
        *,
        default: float = 0.0,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class IntegerInput(_InputField[IntegerSocket, InputInteger]):
    _method = "integer"

    def __init__(
        self,
        *,
        default: int = 0,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class BooleanInput(_InputField[BooleanSocket, InputBoolean]):
    """``panel_toggle=True`` makes it the toggle in its panel's header; the
    socket then takes the panel's name."""

    _method = "boolean"

    def __init__(
        self,
        *,
        default: bool = False,
        name: str | None = None,
        description: str = "",
        panel_toggle: bool = False,
        **options: Any,
    ) -> None:
        super().__init__(
            default,
            name=name,
            description=description,
            is_panel_toggle=panel_toggle,
            **options,
        )


class VectorInput(_InputField[VectorSocket, InputVector]):
    _method = "vector"

    def __init__(
        self,
        *,
        default: tuple[float, ...] | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class ColorInput(_InputField[ColorSocket, InputColor]):
    _method = "color"

    def __init__(
        self,
        *,
        default: tuple[float, float, float, float] | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class RotationInput(_InputField[RotationSocket, InputRotation]):
    _method = "rotation"

    def __init__(
        self,
        *,
        default: tuple[float, float, float] | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class StringInput(_InputField[StringSocket, InputString]):
    _method = "string"

    def __init__(
        self,
        *,
        default: str = "",
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class MenuInput(_InputField[MenuSocket, InputMenu]):
    _method = "menu"

    def __init__(
        self,
        *,
        default: str | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class ObjectInput(_InputField[ObjectSocket, InputObject]):
    _method = "object"

    def __init__(
        self,
        *,
        default: bpy.types.Object | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class CollectionInput(_InputField[CollectionSocket, InputCollection]):
    _method = "collection"

    def __init__(
        self,
        *,
        default: bpy.types.Collection | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class ImageInput(_InputField[ImageSocket, InputImage]):
    _method = "image"

    def __init__(
        self,
        *,
        default: bpy.types.Image | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class MaterialInput(_InputField[MaterialSocket, InputMaterial]):
    _method = "material"

    def __init__(
        self,
        *,
        default: bpy.types.Material | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class FontInput(_InputField[FontSocket, InputFont]):
    _method = "font"

    def __init__(
        self,
        *,
        default: bpy.types.VectorFont | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class SoundInput(_InputField[SoundSocket, InputSound]):
    _method = "sound"

    def __init__(
        self,
        *,
        default: bpy.types.Sound | None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class MatrixInput(_InputField[MatrixSocket, InputMatrix]):
    _method = "matrix"

    def __init__(
        self,
        *,
        default: None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class GeometryInput(_InputField[GeometrySocket, InputGeometry]):
    _method = "geometry"

    def __init__(
        self,
        *,
        default: None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class BundleInput(_InputField[BundleSocket, InputBundle]):
    _method = "bundle"

    def __init__(
        self,
        *,
        default: None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class ClosureInput(_InputField[ClosureSocket, InputClosure]):
    _method = "closure"

    def __init__(
        self,
        *,
        default: None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


class ShaderInput(_InputField[ShaderSocket, InputShader]):
    _method = "shader"

    def __init__(
        self,
        *,
        default: None = None,
        name: str | None = None,
        description: str = "",
        **options: Any,
    ) -> None:
        super().__init__(default, name=name, description=description, **options)


# -- outputs ------------------------------------------------------------------


class FloatOutput(_OutputField[FloatSocket]):
    _method = "float"


class IntegerOutput(_OutputField[IntegerSocket]):
    _method = "integer"


class BooleanOutput(_OutputField[BooleanSocket]):
    _method = "boolean"


class VectorOutput(_OutputField[VectorSocket]):
    _method = "vector"


class ColorOutput(_OutputField[ColorSocket]):
    _method = "color"


class RotationOutput(_OutputField[RotationSocket]):
    _method = "rotation"


class MatrixOutput(_OutputField[MatrixSocket]):
    _method = "matrix"


class StringOutput(_OutputField[StringSocket]):
    _method = "string"


class MenuOutput(_OutputField[MenuSocket]):
    _method = "menu"


class ObjectOutput(_OutputField[ObjectSocket]):
    _method = "object"


class CollectionOutput(_OutputField[CollectionSocket]):
    _method = "collection"


class ImageOutput(_OutputField[ImageSocket]):
    _method = "image"


class MaterialOutput(_OutputField[MaterialSocket]):
    _method = "material"


class FontOutput(_OutputField[FontSocket]):
    _method = "font"


class SoundOutput(_OutputField[SoundSocket]):
    _method = "sound"


class GeometryOutput(_OutputField[GeometrySocket]):
    _method = "geometry"


class BundleOutput(_OutputField[BundleSocket]):
    _method = "bundle"


class ClosureOutput(_OutputField[ClosureSocket]):
    _method = "closure"


class ShaderOutput(_OutputField[ShaderSocket]):
    _method = "shader"


# -- group base classes ---------------------------------------------------------


def _title(class_name: str) -> str:
    """'RadialArray' → 'Radial Array'."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", class_name)


# Attributes a field can't shadow: the group node's own API.
_RESERVED = frozenset(
    name
    for name in dir(CustomGeometryGroup)
    + dir(CustomShaderGroup)
    + dir(CustomCompositorGroup)
    if not name.startswith("_")
) | {"build"}


@dataclass_transform(
    field_specifiers=(
        FloatInput,
        IntegerInput,
        BooleanInput,
        VectorInput,
        ColorInput,
        RotationInput,
        StringInput,
        MenuInput,
        ObjectInput,
        CollectionInput,
        ImageInput,
        MaterialInput,
        FontInput,
        SoundInput,
        MatrixInput,
        GeometryInput,
        BundleInput,
        ClosureInput,
        ShaderInput,
    )
)
class _FieldGroup:
    """Builds a group from its class fields; see the module docstring."""

    _inputs: ClassVar[tuple[_InputField[Any, Any], ...]] = ()
    _outputs: ClassVar[tuple[_OutputField[Any], ...]] = ()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if cls.__module__ == __name__:
            return  # GeometryGroup & co. build nothing themselves
        fields: dict[str, _Field[Any]] = {}
        for base in reversed(cls.__mro__):
            for attr, value in vars(base).items():
                if isinstance(value, _Field):
                    fields.pop(attr, None)  # a redefinition moves to the end
                    fields[attr] = value
        for attr in fields:
            if attr in _RESERVED:
                raise TypeError(
                    f"{cls.__name__}.{attr}: '{attr}' is part of the group node's "
                    "API; give the field another name (and the socket its label "
                    "with name=...)."
                )
        cls._inputs = tuple(f for f in fields.values() if isinstance(f, _InputField))
        cls._outputs = tuple(f for f in fields.values() if isinstance(f, _OutputField))
        for side in (cls._inputs, cls._outputs):
            labels = [f._label for f in side]
            twice = sorted({label for label in labels if labels.count(label) > 1})
            if twice:
                raise TypeError(
                    f"{cls.__name__}: several {'inputs' if side is cls._inputs else 'outputs'} "
                    f"named {twice}; give them distinct names."
                )
        if "_name" not in cls.__dict__:
            cls._name = _title(cls.__name__)
        if "__init__" not in cls.__dict__:
            cls.__init__ = _typed_init(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        inputs = type(self)._inputs
        name = type(self).__name__
        if len(args) > len(inputs):
            raise TypeError(
                f"{name}() takes {len(inputs)} positional inputs, got {len(args)}"
            )
        values = {field._attr: value for field, value in zip(inputs, args)}
        attrs = {field._attr for field in inputs}
        for attr, value in kwargs.items():
            if attr not in attrs:
                raise TypeError(f"{name}() got an unexpected input '{attr}'")
            if attr in values:
                raise TypeError(f"{name}() got multiple values for input '{attr}'")
            values[attr] = value
        super().__init__(
            **{f._label: values[f._attr] for f in inputs if f._attr in values}
        )

    def _build_group(self, tree: TreeBuilder[Any]) -> None:
        panels: dict[Panel, bpy.types.NodeTreeInterfacePanel] = {}
        fields = [*type(self)._inputs, *type(self)._outputs]
        self.__dict__["_field_sockets"] = {
            f._attr: f._declare(tree, panels) for f in fields
        }
        try:
            self.build()
        finally:
            del self.__dict__["_field_sockets"]

    def build(self) -> None:
        """Build the group's nodes: read input fields, link into output fields."""
        raise NotImplementedError(f"{type(self).__name__} must define build()")


def _typed_init(cls: type[_FieldGroup]) -> Any:
    """A per-class ``__init__`` whose signature names the input fields, for
    ``inspect.signature`` (help(), to_python's references to group classes)."""

    def __init__(self: _FieldGroup, *args: Any, **kwargs: Any) -> None:
        _FieldGroup.__init__(self, *args, **kwargs)

    parameters = [inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    parameters += [
        inspect.Parameter(
            f._attr, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=f._default
        )
        for f in cls._inputs
    ]
    __init__.__signature__ = inspect.Signature(parameters)  # ty: ignore[missing-attribute]
    __init__.__qualname__ = f"{cls.__qualname__}.__init__"
    __init__.__module__ = cls.__module__
    return __init__


class GeometryGroup(_FieldGroup, CustomGeometryGroup):
    """Geometry Nodes group declared with class fields."""


class ShaderGroup(_FieldGroup, CustomShaderGroup):
    """Shader group declared with class fields."""


class CompositorGroup(_FieldGroup, CustomCompositorGroup):
    """Compositor group declared with class fields."""
