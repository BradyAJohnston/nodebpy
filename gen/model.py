"""The introspection IR: SocketInfo / EnumInfo / PropertyInfo / NodeInfo.

These dataclasses describe a node as discovered from Blender and carry the
methods that render their own fragments of the generated source.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import bpy

from .config import (
    _OUTPUT_SOCKET_CLASSES,
    GEOMETRY_CONFIG,
    TreeTypeConfig,
    class_name_for,
)
from .util import format_python_value, get_socket_param_name, normalize_name


@dataclass
class SocketInfo:
    """Information about a node socket."""

    name: str
    identifier: str  # Internal identifier
    label: str  # Socket label (empty string if no label)
    description: str  # Socket description (empty string if no description)
    bl_socket_type: str  # e.g., "NodeSocketGeometry", "NodeSocketFloat"
    socket_type: str  # e.g., "GEOMETRY", "FLOAT", "VECTOR"
    is_output: bool
    is_multi_input: bool = False
    default_value: Any = None
    min_value: Any = None
    max_value: Any = None
    always_enabled: bool = True
    menu_items: list[str] = field(default_factory=list)
    structure_type: str = ""

    def format_argument_string(self) -> str:
        param_name = get_socket_param_name(self)
        default = (
            "None"
            if ("GRID" in self.structure_type or "LIST" in self.structure_type)
            else format_python_value(self.default_value)
        )
        return f"{param_name}: {self.type_hint} = {default}"

    @property
    def type_hint(self) -> str:
        """Get the mapped type for a socket."""
        addendum = (
            f" | Literal[{', '.join(self.menu_items)}]" if self.menu_items else ""
        )
        return f"{self.type_mapped}{addendum}"

    @property
    def type_mapped(self) -> str:
        """Get the Python type hint for a socket."""
        type_map = {
            "NodeSocketFloat": "InputFloat",
            "NodeSocketIntVector3D": "InputIntegerVector",
            "NodeSocketInt": "InputInteger",
            "NodeSocketBool": "InputBoolean",
            "NodeSocketVector": "InputVector",
            "NodeSocketColor": "InputColor",
            "NodeSocketRotation": "InputRotation",
            "NodeSocketMatrix": "InputMatrix",
            "NodeSocketString": "InputString",
            "NodeSocketMenu": "InputMenu",
            "NodeSocketObject": "InputObject",
            "NodeSocketGeometry": "InputGeometry",
            "NodeSocketCollection": "InputCollection",
            "NodeSocketImage": "InputImage",
            "NodeSocketMaterial": "InputMaterial",
            "NodeSocketBundle": "InputBundle",
            "NodeSocketClosure": "InputClosure",
            # Shader trees use NodeSocketShader for BSDF/closure outputs
            "NodeSocketShader": "InputShader",
            "NodeSocketFont": "InputFont",
            "NodeSocketSound": "InputSound",
            # Virtual sockets adapt to whatever is connected
            "NodeSocketVirtual": "InputLinkable",
        }
        # to handle all of the subtypes we have to iterate through and
        # instead just check to see if the name is in the socket type
        _GRID_TYPE_MAP = {
            "InputFloat": "InputFloatGrid",
            "InputInteger": "InputIntegerGrid",
            "InputBoolean": "InputBooleanGrid",
            "InputVector": "InputVectorGrid",
        }
        for key, item in type_map.items():
            if key in self.bl_socket_type:
                if "GRID" in self.structure_type:
                    return _GRID_TYPE_MAP.get(item, item)
                if "LIST" in self.structure_type:
                    return item.replace("Input", "InputList")
                return item
        raise KeyError(f"Couldnt match socket type {self.bl_socket_type}")

    def format_accessor_annotation(self) -> str:
        """Generate an annotation + attribute docstring for use in Inputs/Outputs inner classes."""
        attr_name = normalize_name(self.identifier)

        return_type = "Socket"
        for key, cls in _OUTPUT_SOCKET_CLASSES.items():
            if key in self.bl_socket_type:
                return_type = cls
                if "LIST" in self.structure_type:
                    return_type = return_type + "List"
                elif "GRID" in self.structure_type:
                    return_type = return_type.replace("Socket", "SocketGrid")
                break

        doc = self.description or self.name
        lines = [f"        {attr_name}: {return_type}"]
        if doc:
            lines.append(f'        """{doc}"""')
        return "\n".join(lines)


@dataclass
class EnumInfo:
    """Information about a node enum property."""

    identifier: str
    name: str
    description: str = ""
    sockets: list[SocketInfo] = field(default_factory=lambda: list())
    output_sockets: list[SocketInfo] = field(default_factory=lambda: list())


@dataclass
class PropertyInfo:
    """Information about a node property."""

    identifier: str
    name: str
    prop_type: Literal["ENUM", "BOOLEAN", "INT", "FLOAT", "STRING", "COLOR", "VECTOR"]
    subtype: str | None = None
    enum_items: list[EnumInfo] = field(default_factory=lambda: list())
    default: Any = None

    def enum_values_to_literal(self) -> str:
        if not self.enum_items:
            return "str"
        items = ", ".join('"' + item.identifier + '"' for item in self.enum_items)
        return f"Literal[{items}]"

    def format_name(self) -> str:
        prop_name = normalize_name(self.identifier)
        if prop_name in ["primary_axis", "secondary_axis"]:
            prop_name = prop_name.replace("_axis", "")
        return prop_name

    def type_hint(self) -> str:
        match self.prop_type:
            case "ENUM":
                type = self.enum_values_to_literal()
            case "BOOLEAN":
                type = "bool"
            case "INT":
                type = "int"
            case "FLOAT":
                if isinstance(self.default, float):
                    type = "float"
                else:
                    type = "tuple[{}]".format(", ".join(["float"] * len(self.default)))
            case "STRING":
                type = "str"
            case _:
                raise ValueError(f"Unsupported property type: {self.prop_type}")

        return type

    def format_property_argument(self) -> str:
        match self.prop_type:
            case "ENUM":
                default = f'"{self.default}"'
            case "BOOLEAN":
                default = self.default
            case "INT":
                default = self.default
            case "FLOAT":
                match self.subtype:
                    case "COLOR":
                        default = self.default
                    case "EULER" | "XYZ" | "DIRECTION":
                        default = self.default
                    case _:
                        default = round(self.default, 3)
            case "STRING":
                default = f'"{self.default}"'
            case _:
                raise ValueError(f"Unsupported property type: {self.prop_type}")

        return "{}: {} = {}".format(self.format_name(), self.type_hint(), default)

    @property
    def _mathutils_type(self) -> str | None:
        """The mathutils return type for float-array properties, or None if not applicable."""
        if self.prop_type != "FLOAT" or isinstance(self.default, (int, float)):
            return None
        if self.subtype == "EULER":
            return "Euler"
        if self.subtype in ("XYZ", "DIRECTION"):
            return "Vector"
        if self.subtype == "COLOR" and len(self.default) == 3:
            return "Color"
        return None

    def format_property_accessors(self) -> str:
        name = self.format_name()
        scalar_type = self.type_hint()

        mathutils_type = self._mathutils_type
        if mathutils_type:
            # Getter returns the actual bpy type; setter also accepts plain tuples
            getter_type = mathutils_type
            setter_type = f"{mathutils_type} | {scalar_type}"
        else:
            getter_type = scalar_type
            setter_type = scalar_type

        # bpy stubs occasionally have wrong types for specific properties
        needs_ignore = (
            self.prop_type == "ENUM"
            and name
            in [
                "data_type",
                "subsurface_method",
                "falloff",
                "socket_type",
                "layer",
                "input_type",
            ]
        ) or (
            self.prop_type == "STRING"
            and self.identifier in ["layer", "view", "layer_name"]
        )
        ignore = "  # ty: ignore[invalid-return-type]" if needs_ignore else ""
        return f"""    @property

    def {name}(self) -> {getter_type}:
        return self.node.{self.identifier}{ignore}

    @{name}.setter
    def {name}(self, value: {setter_type}):
        self.node.{self.identifier} = value{" # ty: ignore[invalid-assignment]" if name == "layer" else ""}
"""


@dataclass
class NodeInfo:
    """Complete information about a node type."""

    bl_idname: str  # blender RNA name "GeometryNodeSetPosition"
    name: str  # Node display node "Set Position"
    color_tag: str  # e.g., "GEOMETRY", "CONVERTER", "INPUT"
    description: str
    inputs: list[SocketInfo]
    outputs: list[SocketInfo]
    properties: list[PropertyInfo]
    domain_sockets: dict[str, list[SocketInfo]]
    tree_types: list[str] = field(default_factory=list)
    # Per-value socket snapshots for any input socket named "Type" that is a MENU.
    # Keyed by the socket identifier; each entry mirrors EnumInfo used for properties.
    type_socket_enums: list[EnumInfo] = field(default_factory=list)

    @property
    def node_docs_url(self) -> str | None:
        "Find adn returl the URL for the online Blender documentation for this node"
        return bpy.types.WM_OT_doc_view_manual._lookup_rna_url(
            f"bpy.types.{self.bl_idname}", verbose=False
        )

    @property
    def node_image_url(self) -> str:
        "Return the URL to a screenshot of the node from the online Blender documentation"
        return f"https://docs.blender.org/manual/en/latest/_images/node-types_{self.bl_idname}.webp"

    def class_name_for_config(self, config: TreeTypeConfig) -> str:
        """The Python class name for this node under the given config."""
        return class_name_for(self.name, self.bl_idname, config)

    @property
    def class_name(self) -> str:
        """Fallback that uses geometry config. Prefer class_name_for_config()."""
        return self.class_name_for_config(GEOMETRY_CONFIG)

    @property
    def module_name(self) -> str:
        """Determine the target filename for a node based on color_tag and special cases."""
        # Special cases for zones
        if any(
            keyword in self.bl_idname for keyword in ["Repeat", "ForEach", "Simulation"]
        ):
            return "zone"

        # Special cases for grid/volume nodes
        if any(keyword in self.bl_idname for keyword in ["Volume", "Grid"]):
            return "grid" if self.class_name != "Grid" else "geometry"

        # if "List" in self.bl_idname:
        #     return "experimental"

        # Map color_tag to filename – covers geometry, shader, and compositor tags
        color_tag_to_filename = {
            # Shared across tree types
            "CONVERTER": "converter",
            "INPUT": "input",
            "OUTPUT": "output",
            "COLOR": "color",
            "TEXTURE": "texture",
            "GROUP": "group",
            "INTERFACE": "interface",
            "LAYOUT": "layout",
            "VECTOR": "vector",
            "SCRIPT": "script",
            # Geometry-specific
            "GEOMETRY": "geometry",
            "ATTRIBUTE": "attribute",
            # Shader-specific
            "SHADER": "shader",
            "OP_COLOR": "color",
            # Compositor-specific
            "FILTER": "filter",
            "MATTE": "matte",
            "DISTORT": "distort",
        }

        filename = color_tag_to_filename.get(self.color_tag, "utilities")

        return filename

    @property
    def varying_output_identifiers(self) -> set[str]:
        """Output socket identifiers whose type changes across enum values."""
        default_types = {s.identifier: s.bl_socket_type for s in self.outputs}
        varying = set()
        for prop in self.properties:
            for enum in prop.enum_items:
                for s in enum.output_sockets:
                    if (
                        s.identifier in default_types
                        and s.bl_socket_type != default_types[s.identifier]
                    ):
                        varying.add(s.identifier)
        return varying

    @property
    def varying_input_identifiers(self) -> set[str]:
        """Input socket identifiers whose type changes across enum values.

        Mirrors :attr:`varying_output_identifiers` for the input side so that
        nodes like ``Switch`` (where ``false``/``true`` track the generic
        output type) can be typed with the shared ``_S`` type variable.
        """
        default_types = {s.identifier: s.bl_socket_type for s in self.inputs}
        varying = set()
        for prop in self.properties:
            for enum in prop.enum_items:
                for s in enum.sockets:
                    if (
                        s.identifier in default_types
                        and s.bl_socket_type != default_types[s.identifier]
                    ):
                        varying.add(s.identifier)
        return varying

    def _varying_share_single_type(self, varying: set[str], *, outputs: bool) -> bool:
        """True if, for every enum value, all the ``varying`` sockets on the
        given side resolve to the same socket type — i.e. they can share one
        ``_S`` type variable (as with AccumulateField's leading/trailing/total
        all tracking the data_type)."""
        if not varying:
            return False
        for prop in self.properties:
            for enum in prop.enum_items:
                sockets = enum.output_sockets if outputs else enum.sockets
                types = {s.bl_socket_type for s in sockets if s.identifier in varying}
                if len(types) > 1:
                    return False
        return True

    @property
    def outputs_generic(self) -> bool:
        """The output side is generic: ≥1 output varies and all varying outputs
        share a single type per enum value (so a single ``_S`` suffices)."""
        return self._varying_share_single_type(
            self.varying_output_identifiers, outputs=True
        )

    @property
    def inputs_generic(self) -> bool:
        """The input side is generic: ≥1 input varies and all varying inputs
        share a single type per enum value."""
        return self._varying_share_single_type(
            self.varying_input_identifiers, outputs=False
        )

    def output_class_for_enum(
        self, socket_identifier: str, enum_identifier: str
    ) -> str:
        """Return the socket class name for a varying output given an enum identifier."""
        for prop in self.properties:
            for enum in prop.enum_items:
                if enum.identifier == enum_identifier:
                    for s in enum.output_sockets:
                        if s.identifier == socket_identifier:
                            for key, cls in _OUTPUT_SOCKET_CLASSES.items():
                                if key in s.bl_socket_type:
                                    return cls
        for s in self.outputs:
            if s.identifier == socket_identifier:
                for key, cls in _OUTPUT_SOCKET_CLASSES.items():
                    if key in s.bl_socket_type:
                        return cls
        return "Socket"

    def input_class_for_enum(self, socket_identifier: str, enum_identifier: str) -> str:
        """Return the socket class name for a varying input given an enum
        identifier (mirrors :meth:`output_class_for_enum` for input-generic
        nodes like Compare)."""
        for prop in self.properties:
            for enum in prop.enum_items:
                if enum.identifier == enum_identifier:
                    for s in enum.sockets:
                        if s.identifier == socket_identifier:
                            for key, cls in _OUTPUT_SOCKET_CLASSES.items():
                                if key in s.bl_socket_type:
                                    return cls
        for s in self.inputs:
            if s.identifier == socket_identifier:
                for key, cls in _OUTPUT_SOCKET_CLASSES.items():
                    if key in s.bl_socket_type:
                        return cls
        return "Socket"

    def generate_enum_class_methods(
        self,
        config: TreeTypeConfig | None = None,
        suppress: frozenset[str] = frozenset(),
    ) -> str:
        """Generate @classmethod convenience methods for enum operations.

        ``suppress`` names factory methods to omit (a registered customization
        replaces them).
        """
        methods = []
        cls_name = self.class_name_for_config(config) if config else self.class_name

        for prop in self.properties:
            if (
                prop.identifier
                not in [
                    "operation",
                    "domain",
                    "mode",
                ]
                and "type" not in prop.identifier
                or prop.identifier in ["blend_type", "direction_type"]
            ):
                continue

            # assert operation_enum.enum_items
            for enum in prop.enum_items:
                # Handle special cases for better naming
                method_name = normalize_name(
                    enum.name.replace("4x4_matrix", "matrix")
                    .replace("8_bit_integer", "int8")
                    .replace("2d_vector", "vector2")
                )
                # method_name = method_name.replace("_", "")
                if method_name == "and":
                    method_name = "l_and"
                elif method_name == "or":
                    method_name = "l_or"
                elif method_name == "not":
                    method_name = "l_not"
                else:
                    # Add underscore suffix to avoid Python keyword conflicts for others
                    method_name = f"{method_name}"

                # # Skip invalid method names
                # if not method_name.replace("_", "").replace("l", "").isalnum():
                #     continue

                # Generate method signature based on node inputs (excluding operation socket)
                input_params = ["cls"]
                call_params = []

                all_labels = [socket.identifier for socket in enum.sockets]
                sockets_use_same_name = all(
                    label == all_labels[0] for label in all_labels
                )
                for socket in enum.sockets:
                    # Use label-based parameter naming
                    socket_name = get_socket_param_name(socket, sockets_use_same_name)
                    suffixes_to_remove = ["_float", "_vector"]
                    param_name = socket_name
                    if socket_name.startswith("min") or socket_name.startswith("max"):
                        suffixes_to_remove += ["_001", "_002"]
                    for suffix in suffixes_to_remove:
                        param_name = param_name.replace(suffix, "")

                    if (
                        param_name
                        and param_name != ""
                        and param_name != normalize_name(prop.identifier)
                    ):
                        input_params.append(
                            f"{param_name}: {socket.type_hint} = {format_python_value(socket.default_value)}"
                        )
                        # Use the same parameter name as in the constructor
                        call_params.append(f"{socket_name}={param_name}")

                params_str = ",\n        ".join(input_params)
                call_params_str = ", ".join(call_params)

                # Add operation parameter to call
                operation_param = f'{prop.identifier}="{enum.identifier}"'
                if call_params_str:
                    call_params_str = f"{operation_param}, {call_params_str}"
                else:
                    call_params_str = operation_param

                docstring = f"Create {self.name} with operation '{enum.name}'."
                if enum.description:
                    docstring += f" {enum.description}"

                # Parameterise the return type when the node is generic. The
                # output side wins when present (Switch/Mix/field nodes); else
                # the input side drives it (Compare, whose output is Boolean).
                if self.outputs_generic:
                    varying_id = next(iter(self.varying_output_identifiers))
                    socket_cls = self.output_class_for_enum(varying_id, enum.identifier)
                    return_type = f"{cls_name}[{socket_cls}]"
                    # Use the class name directly (not cls) so the type checker
                    # can resolve the parameterized return type.
                    call_expr = f"{cls_name}({call_params_str})"
                elif self.inputs_generic:
                    varying_id = next(iter(self.varying_input_identifiers))
                    socket_cls = self.input_class_for_enum(varying_id, enum.identifier)
                    return_type = f"{cls_name}[{socket_cls}]"
                    call_expr = f"{cls_name}({call_params_str})"
                else:
                    return_type = cls_name
                    call_expr = f"cls({call_params_str})"

                if method_name in suppress:
                    continue

                method = f'''
    @classmethod
    def {method_name}(
        {params_str}
    ) -> "{return_type}":
        """{docstring}"""
        return {call_expr}'''

                methods.append(method)

        # Generate classmethods for input sockets named "type" that are MENU sockets.
        # Uses per-value socket snapshots collected during introspection so that methods
        # only expose the sockets that are actually visible for that type value.
        type_param_name = "type"

        if not self.type_socket_enums:
            return "".join(methods)

        for enum in self.type_socket_enums:
            item_value = enum.identifier
            method_name = normalize_name(item_value)
            if method_name == "and":
                method_name = "l_and"
            elif method_name == "or":
                method_name = "l_or"
            elif method_name == "not":
                method_name = "l_not"

            input_params = ["cls"]
            call_params = []

            all_identifiers = [s.identifier for s in enum.sockets]
            sockets_use_same_name = (
                all(ident == all_identifiers[0] for ident in all_identifiers)
                if all_identifiers
                else False
            )

            for socket in enum.sockets:
                socket_name = get_socket_param_name(socket, sockets_use_same_name)
                suffixes_to_remove = ["_float", "_vector"]
                param_name = socket_name
                if socket_name.startswith("min") or socket_name.startswith("max"):
                    suffixes_to_remove += ["_001", "_002"]
                for suffix in suffixes_to_remove:
                    param_name = param_name.replace(suffix, "")

                if param_name and param_name != "" and param_name != type_param_name:
                    input_params.append(
                        f"{param_name}: {socket.type_hint} = {format_python_value(socket.default_value)}"
                    )
                    call_params.append(f"{socket_name}={param_name}")

            params_str = ",\n        ".join(input_params)
            call_params_str = ", ".join(call_params)
            type_call_param = f'{type_param_name}="{item_value}"'
            if call_params_str:
                call_params_str = f"{call_params_str}, {type_call_param}"
            else:
                call_params_str = type_call_param

            docstring = f"Create {self.name} node with type '{item_value}'."
            if enum.description:
                docstring += f" {enum.description}"

            if method_name in suppress:
                continue

            method = f'''
    @classmethod
    def {method_name}(
        {params_str}
    ) -> "{cls_name}":
        """{docstring}"""
        return cls({call_params_str})'''

            methods.append(method)

        return "".join(methods)
