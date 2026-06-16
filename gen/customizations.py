"""Per-node customizations layered onto generated classes.

Mirrors :func:`nodebpy.export.codegen.register_emitter`: a node keeps its
generated boilerplate and a registered :class:`NodeCustomization` (keyed by
``bl_idname``) adds mixin bases, suppresses members, overrides ``__init__`` via
``extra_body``, or pins the public class name.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NodeCustomization:
    """Declarative customization applied to a generated node class.

    Attributes
    ----------
    bl_idname:
        The Blender RNA name of the node this customization applies to.
    bases:
        Extra base classes, prepended before ``BaseNode`` in the class
        definition (e.g. ``("_HandleModeMixin",)``). Listed first so their
        methods win via MRO over the generated body.
    imports:
        Raw import lines added to the generated module header so ``bases`` and
        ``extra_body`` resolve (e.g. ``"from .._mixins import _HandleModeMixin"``).
    suppress:
        Names of generated members to omit because a mixin or ``extra_body``
        replaces them. May include property accessor names, enum factory method
        names, and the special token ``"__init__"`` to drop the generated
        constructor.
    extra_body:
        Source appended verbatim to the class body (already indented four
        spaces). Used for a bespoke ``__init__`` or methods that reference the
        node's own generated types.
    class_name:
        Override the Python class name derived from the Blender display name,
        when the public API name differs (e.g. ``FieldMinAndMax`` where Blender
        calls the node "Field Min Max").
    """

    bl_idname: str
    bases: tuple[str, ...] = ()
    imports: tuple[str, ...] = ()
    suppress: frozenset[str] = field(default_factory=frozenset)
    extra_body: str = ""
    class_name: str | None = None


_CUSTOMIZATIONS: dict[str, NodeCustomization] = {}


def register_customization(custom: NodeCustomization) -> None:
    """Register a :class:`NodeCustomization`, keyed by ``bl_idname``."""
    _CUSTOMIZATIONS[custom.bl_idname] = custom


# The Bézier handle nodes share an ENUM_FLAG ``mode`` set ({"LEFT", "RIGHT"})
# that the generator renders as a broken ``mode: str`` parameter. _HandleModeMixin
# replaces it with ergonomic ``left``/``right`` toggles; the bespoke __init__
# exposes those instead of ``mode``.
register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeCurveSetHandles",
        bases=("_HandleModeMixin",),
        imports=("from .._mixins import _HandleModeMixin",),
        suppress=frozenset({"__init__", "mode"}),
        extra_body="""    def __init__(
        self,
        curve: InputGeometry = None,
        selection: InputBoolean = True,
        *,
        left: bool = True,
        right: bool = True,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
    ):
        super().__init__()
        self.handle_type = handle_type
        self.left = left
        self.right = right
        self._establish_links(Curve=curve, Selection=selection)""",
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeCurveHandleTypeSelection",
        bases=("_HandleModeMixin",),
        imports=("from .._mixins import _HandleModeMixin",),
        suppress=frozenset({"__init__", "mode"}),
        extra_body="""    def __init__(
        self,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
        left: bool = True,
        right: bool = True,
    ):
        super().__init__()
        self.handle_type = handle_type
        self.left = left
        self.right = right""",
    )
)


# Bundle pack/unpack nodes carry dynamic items the introspector can't see; the
# bespoke __init__ adds them via the bundle_items collection (Combine infers the
# type from a linked source through the __extend__ socket; Separate declares each
# item by name + socket-type string). The generated define_signature accessor and
# Outputs are kept.
register_customization(
    NodeCustomization(
        bl_idname="NodeCombineBundle",
        imports=("from ...builder.items import _infer_value_type",),
        suppress=frozenset({"__init__"}),
        extra_body='''    def __init__(
        self,
        items: "dict[str, InputAny] | None" = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        for name, value in (items or {}).items():
            self._add_bundle_item(name, value)
        self.define_signature = define_signature

    def _add_bundle_item(self, name: str, value: InputAny) -> None:
        """Add a named bundle item from a value of any supported kind.

        - a socket-type string (``"GEOMETRY"``) declares an empty item;
        - a socket / node source is linked in via the ``__extend__`` virtual
          socket (Blender makes an item of the source\'s own type, then renamed);
        - any other value declares an item of the inferred type and sets its
          default.
        """
        if isinstance(value, str):
            self.node.bundle_items.new(value, name)
        elif isinstance(value, (BaseNode, Socket, bpy.types.NodeSocket)):
            extend = self.node.inputs[len(self.node.inputs) - 1]
            self.tree.link(self._source_socket(value), extend)
            # Re-fetch by index: the collection just grew, so any earlier item
            # reference is stale (see bpy collection invalidation).
            self.node.bundle_items[len(self.node.bundle_items) - 1].name = name
        else:
            socket_type = _infer_value_type(value)
            if socket_type is None:
                raise TypeError(f"Unsupported bundle item {name!r}: {value!r}")
            self.node.bundle_items.new(socket_type, name)
            self.node.inputs[name].default_value = value''',
    )
)

register_customization(
    NodeCustomization(
        bl_idname="NodeSeparateBundle",
        suppress=frozenset({"__init__"}),
        extra_body="""    def __init__(
        self,
        bundle: InputBundle = None,
        items: "dict[str, str] | None" = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        self.define_signature = define_signature
        # Items are output sockets pulled from the bundle; each is declared by
        # name and socket-type string (the inverse of CombineBundle, where the
        # type is inferred from a linked source).
        for name, socket_type in (items or {}).items():
            self.node.bundle_items.new(socket_type, name)
        self._establish_links(Bundle=bundle)""",
    )
)


# Items-based nodes: the generated boilerplate (sockets, docstring, property
# accessors) is kept; a mixin in _mixins.py supplies the variadic items
# constructor and item helpers.
register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeBake",
        bases=("_BakeMixin",),
        imports=("from .._mixins import _BakeMixin",),
        suppress=frozenset({"__init__"}),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldToList",
        bases=("_FieldToListMixin",),
        imports=("from .._mixins import _FieldToListMixin",),
        suppress=frozenset({"__init__"}),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="FunctionNodeFormatString",
        bases=("_FormatStringMixin",),
        imports=("from .._mixins import _FormatStringMixin",),
        suppress=frozenset({"__init__"}),
    )
)


# Generic field nodes: the generator now emits the full generic structure
# (Generic[_T], _S-typed sockets, __init__, data_type/domain properties, and the
# flat per-type/per-domain factories). Only the nested `<node>.<domain>.<dtype>()`
# domain-factory helpers are bespoke (they self-reference the class for precise
# return typing), so they live in extra_body; the colliding flat domain factories
# the generator emits are suppressed.

# Blender data_type enum value -> (factory method name, socket class used for
# the parameterised return type / the matching Input* parameter type).
_DATA_TYPE: dict[str, tuple[str, str]] = {
    "FLOAT": ("float", "FloatSocket"),
    "INT": ("integer", "IntegerSocket"),
    "BOOLEAN": ("boolean", "BooleanSocket"),
    "FLOAT_VECTOR": ("vector", "VectorSocket"),
    "FLOAT_COLOR": ("color", "ColorSocket"),
    "QUATERNION": ("quaternion", "RotationSocket"),
    "FLOAT4X4": ("matrix", "MatrixSocket"),
    "TRANSFORM": ("transform", "MatrixSocket"),
}

# Factory attribute name -> Blender domain enum value.
_DOMAINS: dict[str, str] = {
    "point": "POINT",
    "edge": "EDGE",
    "face": "FACE",
    "corner": "CORNER",
    "spline": "CURVE",
    "instance": "INSTANCE",
    "layer": "LAYER",
}

# The generator emits flat per-domain (point/edge/…) and per-data-type
# (float/integer/…) classmethods for these nodes' enums; the nested
# `<node>.<domain>.<dtype>()` factory below is the real (and only) public API,
# so suppress both sets of flat factories.
_SUPPRESS_METHODS = frozenset(_DOMAINS) | {method for method, _ in _DATA_TYPE.values()}


def _domain_factory_typed(
    node_name: str,
    data_types: list[str],
    index: str | None = "group_index",
) -> str:
    """Build a nested ``<node>.<domain>.<dtype>()`` factory as class-body source.

    ``data_types`` are Blender ``data_type`` enum values; ``index`` names the
    optional per-element index parameter (``None`` if the node has none). Each
    method returns the parameterised node type (e.g. ``AccumulateField[FloatSocket]``)
    for precise typing — which is why they self-reference the class and are built
    here rather than in a shared mixin.
    """
    factory = f"_{node_name}DomainFactory"
    idx_param = f", {index}: InputInteger = 0" if index else ""
    idx_arg = f", {index}" if index else ""

    lines = [
        f"    class {factory}:",
        "        def __init__(self, domain: _AttributeDomains):",
        "            self._domain = domain",
    ]
    for dtype in data_types:
        method, socket = _DATA_TYPE[dtype]
        input_type = "Input" + socket.replace("Socket", "")
        lines += [
            "",
            f'        def {method}(self, value: {input_type} = None{idx_param}) -> "{node_name}[{socket}]":',
            f'            """Create \'{node_name}\' on this domain with \'{dtype}\' data type."""',
            f'            return {node_name}(value{idx_arg}, domain=self._domain, data_type="{dtype}")',
        ]
    lines.append("")
    lines += [f'    {attr} = {factory}("{dom}")' for attr, dom in _DOMAINS.items()]
    return "\n".join(lines)


register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeAccumulateField",
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed(
            "AccumulateField", ["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"]
        ),
    )
)


register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldAtIndex",  # EvaluateAtIndex
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed(
            "EvaluateAtIndex",
            [
                "FLOAT",
                "INT",
                "BOOLEAN",
                "FLOAT_VECTOR",
                "FLOAT_COLOR",
                "QUATERNION",
                "FLOAT4X4",
            ],
            "index",
        ),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldAverage",
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed("FieldAverage", ["FLOAT", "FLOAT_VECTOR"]),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldMinAndMax",
        class_name="FieldMinAndMax",  # Blender display name is "Field Min & Max"
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed(
            "FieldMinAndMax", ["FLOAT", "INT", "FLOAT_VECTOR"]
        ),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldOnDomain",  # EvaluateOnDomain
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed(
            "EvaluateOnDomain",
            [
                "FLOAT",
                "INT",
                "BOOLEAN",
                "FLOAT_VECTOR",
                "FLOAT_COLOR",
                "QUATERNION",
                "FLOAT4X4",
            ],
            index=None,
        ),
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldVariance",
        imports=("from ...types import _AttributeDomains",),
        suppress=_SUPPRESS_METHODS,
        extra_body=_domain_factory_typed("FieldVariance", ["FLOAT", "FLOAT_VECTOR"]),
    )
)
