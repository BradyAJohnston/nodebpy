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
        suppress=frozenset({"__init__"}),
        extra_body='''    def __init__(
        self,
        items: "dict[str, InputLinkable] | None" = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        self.define_signature = define_signature
        for name, value in (items or {}).items():
            self._add_bundle_item(name, value)

    def _add_bundle_item(self, name: str, value: "InputLinkable | str") -> None:
        """Add a named bundle item.

        A socket-type string (``"GEOMETRY"``) declares an unlinked item; any
        other value is linked in via the ``__extend__`` virtual socket, which
        makes Blender create an item of the source socket\'s own type (then
        renamed, since the item otherwise inherits the source socket\'s name)."""
        if isinstance(value, str):
            self.node.bundle_items.new(value, name)
            return
        extend = self.node.inputs[len(self.node.inputs) - 1]
        self.tree.link(self._source_socket(value), extend)
        # Re-fetch by index: the collection just grew, so any earlier item
        # reference is stale (see bpy collection invalidation).
        self.node.bundle_items[len(self.node.bundle_items) - 1].name = name''',
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
register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeAccumulateField",
        imports=("from ...types import _AttributeDomains",),
        suppress=frozenset(
            {"point", "edge", "face", "corner", "spline", "instance", "layer"}
        ),
        extra_body="""    class AccumulateFieldDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self, value: InputFloat = None, index: InputInteger = 0
        ) -> "AccumulateField[FloatSocket]":
            return AccumulateField(value, index, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None, index: InputInteger = 0
        ) -> "AccumulateField[IntegerSocket]":
            return AccumulateField(value, index, domain=self._domain, data_type="INT")

        def vector(
            self, value: InputVector = None, index: InputInteger = 0
        ) -> "AccumulateField[VectorSocket]":
            return AccumulateField(
                value, index, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def transform(
            self, value: InputMatrix = None, index: InputInteger = 0
        ) -> "AccumulateField[MatrixSocket]":
            return AccumulateField(
                value, index, domain=self._domain, data_type="TRANSFORM"
            )

    point = AccumulateFieldDomainFactory("POINT")
    edge = AccumulateFieldDomainFactory("EDGE")
    face = AccumulateFieldDomainFactory("FACE")
    corner = AccumulateFieldDomainFactory("CORNER")
    spline = AccumulateFieldDomainFactory("CURVE")
    instance = AccumulateFieldDomainFactory("INSTANCE")
    layer = AccumulateFieldDomainFactory("LAYER")""",
    )
)

_DOMAIN_SUPPRESS = frozenset(
    {"point", "edge", "face", "corner", "spline", "instance", "layer"}
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldAtIndex",  # EvaluateAtIndex
        imports=("from ...types import _AttributeDomains",),
        suppress=_DOMAIN_SUPPRESS,
        extra_body="""    class _EvaluateAtIndexDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self, value: InputFloat = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[FloatSocket]":
            return EvaluateAtIndex(value, index, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[IntegerSocket]":
            return EvaluateAtIndex(value, index, domain=self._domain, data_type="INT")

        def boolean(
            self, value: InputBoolean = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[BooleanSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="BOOLEAN"
            )

        def vector(
            self, value: InputVector = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[VectorSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def color(
            self, value: InputColor = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[ColorSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="FLOAT_COLOR"
            )

        def quaternion(
            self, value: InputRotation = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[RotationSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="QUATERNION"
            )

        def matrix(
            self, value: InputMatrix = None, index: InputInteger = 0
        ) -> "EvaluateAtIndex[MatrixSocket]":
            return EvaluateAtIndex(
                value, index, domain=self._domain, data_type="FLOAT4X4"
            )

    point = _EvaluateAtIndexDomainFactory("POINT")
    edge = _EvaluateAtIndexDomainFactory("EDGE")
    face = _EvaluateAtIndexDomainFactory("FACE")
    corner = _EvaluateAtIndexDomainFactory("CORNER")
    spline = _EvaluateAtIndexDomainFactory("CURVE")
    instance = _EvaluateAtIndexDomainFactory("INSTANCE")
    layer = _EvaluateAtIndexDomainFactory("LAYER")""",
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldAverage",
        imports=("from ...types import _AttributeDomains",),
        suppress=_DOMAIN_SUPPRESS,
        extra_body='''    class _FieldAverageDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = 1.0,
            group_index: InputInteger = 0,
        ) -> "FieldAverage[FloatSocket]":
            """Create FieldAverage for the "FLOAT" data type"""
            return FieldAverage(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = (1.0, 1.0, 1.0),
            group_index: InputInteger = 0,
        ) -> "FieldAverage[VectorSocket]":
            """Create FieldAverage for the "FLOAT_VECTOR" data type"""
            return FieldAverage(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldAverageDomainFactory("POINT")
    edge = _FieldAverageDomainFactory("EDGE")
    face = _FieldAverageDomainFactory("FACE")
    corner = _FieldAverageDomainFactory("CORNER")
    spline = _FieldAverageDomainFactory("CURVE")
    instance = _FieldAverageDomainFactory("INSTANCE")
    layer = _FieldAverageDomainFactory("LAYER")''',
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldMinAndMax",
        class_name="FieldMinAndMax",  # Blender display name is "Field Min Max"
        imports=("from ...types import _AttributeDomains",),
        suppress=_DOMAIN_SUPPRESS,
        extra_body='''    class _FieldMinAndMaxDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = 1.0,
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[FloatSocket]":
            """Create FieldMinMax for the "FLOAT" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def integer(
            self,
            value: InputInteger = 1,
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[IntegerSocket]":
            """Create FieldMinMax for the "INT" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="INT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = (1.0, 1.0, 1.0),
            group_index: InputInteger = 0,
        ) -> "FieldMinAndMax[VectorSocket]":
            """Create FieldMinMax for the "FLOAT_VECTOR" data type"""
            return FieldMinAndMax(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldMinAndMaxDomainFactory("POINT")
    edge = _FieldMinAndMaxDomainFactory("EDGE")
    face = _FieldMinAndMaxDomainFactory("FACE")
    corner = _FieldMinAndMaxDomainFactory("CORNER")
    spline = _FieldMinAndMaxDomainFactory("CURVE")
    instance = _FieldMinAndMaxDomainFactory("INSTANCE")
    layer = _FieldMinAndMaxDomainFactory("LAYER")''',
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldOnDomain",  # EvaluateOnDomain
        imports=("from ...types import _AttributeDomains",),
        suppress=_DOMAIN_SUPPRESS,
        extra_body="""    class _EvaluateOnDomainDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(self, value: InputFloat = None) -> "EvaluateOnDomain[FloatSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="FLOAT")

        def integer(
            self, value: InputInteger = None
        ) -> "EvaluateOnDomain[IntegerSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="INT")

        def boolean(
            self, value: InputBoolean = None
        ) -> "EvaluateOnDomain[BooleanSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="BOOLEAN")

        def vector(self, value: InputVector = None) -> "EvaluateOnDomain[VectorSocket]":
            return EvaluateOnDomain(
                value, domain=self._domain, data_type="FLOAT_VECTOR"
            )

        def quaternion(
            self, value: InputRotation = None
        ) -> "EvaluateOnDomain[RotationSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="QUATERNION")

        def matrix(self, value: InputMatrix = None) -> "EvaluateOnDomain[MatrixSocket]":
            return EvaluateOnDomain(value, domain=self._domain, data_type="FLOAT4X4")

    point = _EvaluateOnDomainDomainFactory("POINT")
    edge = _EvaluateOnDomainDomainFactory("EDGE")
    face = _EvaluateOnDomainDomainFactory("FACE")
    corner = _EvaluateOnDomainDomainFactory("CORNER")
    spline = _EvaluateOnDomainDomainFactory("CURVE")
    instance = _EvaluateOnDomainDomainFactory("INSTANCE")
    layer = _EvaluateOnDomainDomainFactory("LAYER")""",
    )
)

register_customization(
    NodeCustomization(
        bl_idname="GeometryNodeFieldVariance",
        imports=("from ...types import _AttributeDomains",),
        suppress=_DOMAIN_SUPPRESS,
        extra_body='''    class _FieldVarianceDomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def float(
            self,
            value: InputFloat = None,
            group_index: InputInteger = None,
        ) -> "FieldVariance[FloatSocket]":
            """Create FieldVariance for the "FLOAT" data type"""
            return FieldVariance(
                value, group_index, data_type="FLOAT", domain=self._domain
            )

        def vector(
            self,
            value: InputVector = None,
            group_index: InputInteger = None,
        ) -> "FieldVariance[VectorSocket]":
            """Create FieldVariance for the "FLOAT_VECTOR" data type"""
            return FieldVariance(
                value, group_index, data_type="FLOAT_VECTOR", domain=self._domain
            )

    point = _FieldVarianceDomainFactory("POINT")
    edge = _FieldVarianceDomainFactory("EDGE")
    face = _FieldVarianceDomainFactory("FACE")
    corner = _FieldVarianceDomainFactory("CORNER")
    spline = _FieldVarianceDomainFactory("CURVE")
    instance = _FieldVarianceDomainFactory("INSTANCE")
    layer = _FieldVarianceDomainFactory("LAYER")''',
    )
)
