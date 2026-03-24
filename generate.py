"""
Code generator for Blender node classes.

This script introspects Blender's node registry and generates Python classes
for geometry, shader, and compositor nodes with proper type hints and
autocomplete support.

Run this script from within Blender to generate node classes:
    blender --background --python generate.py

"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import bpy
from bpy.types import bpy_prop_array
from mathutils import Euler, Vector

# ---------------------------------------------------------------------------
# Tree-type configuration
# ---------------------------------------------------------------------------

TREE_TYPES = ("GeometryNodeTree", "ShaderNodeTree", "CompositorNodeTree")


@dataclass
class TreeTypeConfig:
    """Configuration for generating node classes for a specific tree type."""

    tree_type: str  # e.g. "GeometryNodeTree"
    output_dir_name: str  # e.g. "geometry"
    nodes_to_skip: list[str]
    manually_defined: tuple[str, ...]
    # Prefixes stripped from bl_idname when generating Python class names.
    # Order matters – longer/more-specific prefixes first.
    class_name_prefix_strips: list[str]

    @property
    def output_dir(self) -> Path:
        return Path(__file__).parent / f"src/nodebpy/nodes/{self.output_dir_name}/"


GEOMETRY_CONFIG = TreeTypeConfig(
    tree_type="GeometryNodeTree",
    output_dir_name="geometry",
    nodes_to_skip=[
        "AlignEulerToVector",
        "Legacy",
        "Closure",
        "Simulation",
        "For Each",
        "Frame",
        "GridBoolean",
        "Reroute",
        "FieldMinAndMax",
    ],
    manually_defined=(
        "SetHandleType",
        "HandleTypeSelection",
        "IndexSwitch",
        "MenuSwitch",
        "CaptureAttribute",
        "FieldToGrid",
        "JoinGeometry",
        "SDFGridBoolean",
        "Bake",
        "JoinStrings",
        "GeometryToInstance",
        "RepeatInput",
        "RepeatOutput",
        "RepeatZone",
        "SimulationInput",
        "SimulationOutput",
        "SimulationZone",
        "ForEachGeometryElementInput",
        "ForEachGeometryElementOutput",
        "ForEachGeometryElementZone",
        "FormatString",
        "Collection",
        "Material",
        "Object",
        "Value",
        "AccumulateField",
        "EvaluateAtIndex",
        "FieldAverage",
        "FieldMinAndMax",
        "EvaluateOnDomain",
        "FieldVariance",
        "Compare",
        "AttributeStatistic",
    ),
    class_name_prefix_strips=[
        "GeometryNode",
        "ShaderMath",
        "FunctionNode",
        "Node",
    ],
)

SHADER_CONFIG = TreeTypeConfig(
    tree_type="ShaderNodeTree",
    output_dir_name="shader",
    nodes_to_skip=[
        "Legacy",
        "Frame",
        "Reroute",
    ],
    manually_defined=("MenuSwitch",),
    class_name_prefix_strips=[
        "ShaderNode",
        "Node",
    ],
)

COMPOSITOR_CONFIG = TreeTypeConfig(
    tree_type="CompositorNodeTree",
    output_dir_name="compositor",
    nodes_to_skip=[
        "Legacy",
        "Frame",
        "Reroute",
        "Cryptomatte",
        "Image",
    ],
    manually_defined=("MenuSwitch",),
    class_name_prefix_strips=[
        "CompositorNode",
        "Node",
    ],
)

ALL_CONFIGS = [GEOMETRY_CONFIG, SHADER_CONFIG, COMPOSITOR_CONFIG]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


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

    def format_argument_string(self) -> str:
        param_name = get_socket_param_name(self)
        return f"{param_name}: {self.type_hint} = {format_python_value(self.default_value)}"

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
            "NodeSocketFloat": "TYPE_INPUT_VALUE",
            "NodeSocketInt": "TYPE_INPUT_INT",
            "NodeSocketBool": "TYPE_INPUT_BOOLEAN",
            "NodeSocketVector": "TYPE_INPUT_VECTOR",
            "NodeSocketColor": "TYPE_INPUT_COLOR",
            "NodeSocketRotation": "TYPE_INPUT_ROTATION",
            "NodeSocketMatrix": "TYPE_INPUT_MATRIX",
            "NodeSocketString": "TYPE_INPUT_STRING",
            "NodeSocketMenu": "TYPE_INPUT_MENU",
            "NodeSocketObject": "TYPE_INPUT_OBJECT",
            "NodeSocketGeometry": "TYPE_INPUT_GEOMETRY",
            "NodeSocketCollection": "TYPE_INPUT_COLLECTION",
            "NodeSocketImage": "TYPE_INPUT_IMAGE",
            "NodeSocketMaterial": "TYPE_INPUT_MATERIAL",
            "NodeSocketBundle": "TYPE_INPUT_BUNDLE",
            "NodeSocketClosure": "TYPE_INPUT_CLOSURE",
            # Shader trees use NodeSocketShader for BSDF/closure outputs
            "NodeSocketShader": "TYPE_INPUT_SHADER",
            # Virtual sockets adapt to whatever is connected
            "NodeSocketVirtual": "LINKABLE",
        }
        # to handle all of the subtypes we have to iterate through and
        # instead just check to see if the name is in the socket type
        for key, item in type_map.items():
            if key in self.bl_socket_type:
                return item
        raise KeyError(f"Couldnt match socket type {self.bl_socket_type}")

    def format_property(self) -> str:
        """Generate the property string for this socket."""
        prop_name = "{}_{}".format(
            "o" if self.is_output else "i", normalize_name(self.identifier)
        )
        description = "{} socket: {}".format(
            "Output" if self.is_output else "Input", self.name
        )
        if self.description != "":
            description += f"\n        {self.description}\n        "

        return_type = (
            "VectorSocketLinker"
            if "NodeSocketVector" in self.bl_socket_type
            else "SocketLinker"
        )

        return_value = "self._{}('{}'{})".format(
            "output" if self.is_output else "input",
            self.identifier,
            ', subtype="Vector"' if "NodeSocketVector" in self.bl_socket_type else "",
        )

        return f'''    @property
    def {prop_name}(self) -> {return_type}:
        """{description}"""
        return {return_value}
'''


@dataclass
class EnumInfo:
    """Information about a node enum property."""

    identifier: str
    name: str
    description: str = ""
    sockets: list[SocketInfo] = field(default_factory=lambda: list())


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

    def format_property_accessors(self) -> str:
        name = self.format_name()
        type = self.type_hint()
        return f"""    @property

    def {name}(self) -> {type}:
        return self.node.{self.identifier}

    @{name}.setter
    def {name}(self, value: {type}):
        self.node.{self.identifier} = value
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

    @property
    def node_docs_url(self) -> str | None:
        "Find adn returl the URL for the online Blender documentation for this node"
        return bpy.types.WM_OT_doc_view_manual._lookup_rna_url(  # type: ignore
            f"bpy.types.{self.bl_idname}", verbose=False
        )

    @property
    def node_image_url(self) -> str:
        "Return the URL to a screenshot of the node from the online Blender documentation"
        return f"https://docs.blender.org/manual/en/latest/_images/node-types_{self.bl_idname}.webp"

    def class_name_for_config(self, config: TreeTypeConfig) -> str:
        """Generate a Python class name using the given config's prefix strips."""
        # Replace common separators with spaces
        class_name = self.name.replace("_", " ").replace("-", " ")

        # Remove any characters that aren't alphanumeric or spaces
        class_name = "".join(
            c if c.isalnum() or c.isspace() else "" for c in class_name
        )
        class_name = class_name.title().replace(" ", "")

        # Static replacements shared across all tree types
        replacements = {
            "&": "And",
            "Uv": "UV",
            "Sdf": "SDF",
            "Rgb": "RGB",
            "3DCursor": "Cursor3D",
            "Xyz": "XYZ",
            "Id": "ID",
            "Bézier": "Bezier",
            "ImportStl": "ImportSTL",
            "ImportObj": "ImportOBJ",
            "ImportCsv": "ImportCSV",
            "ImportPly": "ImportPLY",
            "Vdb": "VDB",
            "3DLocation": "Location3D",
            "Bsdf": "BSDF",
        }

        # Add prefix strips from config
        for prefix in config.class_name_prefix_strips:
            replacements[prefix] = ""

        for key, value in replacements.items():
            class_name = class_name.replace(key, value)

        return class_name

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

        if "List" in self.bl_idname:
            return "experimental"

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

    def generate_enum_class_methods(self, config: TreeTypeConfig | None = None) -> str:
        """Generate @classmethod convenience methods for enum operations."""
        methods = []
        cls_name = self.class_name_for_config(config) if config else self.class_name

        for prop in self.properties:
            if prop.identifier not in [
                "operation",
                "domain",
                "data_type",
                "input_type",
            ]:
                continue

            # assert operation_enum.enum_items
            for enum in prop.enum_items:
                # Handle special cases for better naming
                method_name = (
                    enum.name.lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("4x4_matrix", "matrix")
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
                    if socket_name.startswith("min"):
                        param_name = "min"
                    elif socket_name.startswith("max"):
                        param_name = "max"
                    else:
                        param_name = socket_name
                    param_name = param_name.replace("_float", "").replace("_vector", "")

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

                method = f'''
    @classmethod
    def {method_name}(
        {params_str}
    ) -> "{cls_name}":
        """Create {self.name} with operation '{enum.name}'."""
        return cls({call_params_str})'''

                methods.append(method)

        return "".join(methods)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'.

    Handles numeric names by prefixing with 'input_' to make valid Python identifiers.
    """
    # Replace spaces, hyphens, and other non-alphanumeric characters with underscores
    normalized = name.lower()
    normalized = "".join(c if c.isalnum() else "_" for c in normalized)

    # Remove consecutive underscores and leading/trailing underscores
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")

    # If the name starts with a digit or is purely numeric, prefix it
    if normalized and (normalized[0].isdigit() or normalized.isdigit()):
        normalized = f"input_{normalized}"

    # If the name is empty or only underscores, provide a fallback
    if not normalized or normalized == "_":
        normalized = "input_socket"

    return normalized


def get_socket_param_name(socket: SocketInfo, use_identifier: bool = False) -> str:
    """Get the best parameter name for a socket, preferring label over name."""
    # Use label if available and non-empty, otherwise fallback to name
    # if sockets all use the same label name, we need to drop back to using the iden
    return normalize_name(socket.identifier)
    if use_identifier:
        return normalize_name(socket.identifier)
    else:
        display_name = socket.label if socket.label else socket.name
        return normalize_name(display_name)


def format_python_value(value: Any) -> str:
    """Format a Python value as a string for code generation."""
    if value is None:
        return "None"
    elif isinstance(value, str):
        return f'"{value}"' if value != "" else '""'
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return str(round(value, 4))
    elif hasattr(value, "__iter__") and not isinstance(value, str):
        try:
            return "({})".format(", ".join([round(x, 3) for x in value]))
        except (TypeError, AttributeError):
            return "None"
    else:
        try:
            return f'"{value}"'
        except Exception:
            return "None"


# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------


def _collect_socket_menu_items(socket: bpy.types.NodeSocket) -> list[str]:
    """Collect menu items for a socket of type 'MENU'."""
    try:
        socket.default_value = "X" * 100
        raise ValueError(
            f"Should not be able to set default value of this menu socket, but it succeeded: {socket.default_value}, {socket}"
        )
    except TypeError as e:
        string = str(e)
        values = string.split("not found in ")[1].strip("()").split(", ")
        return values


def collect_socket_info(
    sockets: bpy.types.bpy_prop_collection[bpy.types.NodeSocket],
    hidden=False,
    is_output=False,
) -> list[SocketInfo]:
    """Extract socket infos for a current node state"""
    inputs = []
    for socket in sockets:
        # Switch-type nodes have sockets that are inactive one or the other
        # so we have to be explicit to capture all of them
        if "Switch" not in socket.node.bl_idname:
            if (
                (socket.is_inactive and socket.node.bl_idname != "NodeEnableOutput")
                and not hidden
            ) or "__extend__" in socket.identifier:
                continue

        socket_info = SocketInfo(
            name=socket.name,
            identifier=socket.identifier,
            description=socket.description,
            label=getattr(socket, "label", ""),
            bl_socket_type=type(socket).__name__,
            socket_type=socket.type,
            is_output=is_output,
            is_multi_input=getattr(socket, "is_multi_input", False),
            menu_items=_collect_socket_menu_items(socket)
            if socket.type == "MENU" and socket.default_value != ""
            else [],
        )

        if hasattr(socket, "default_value"):
            value = socket.default_value
            if isinstance(value, (Euler, Vector, bpy_prop_array)):
                value = list(value)
            if socket.type == "MENU" and value == "":
                value = None
            socket_info.default_value = value

        if hasattr(socket, "min_value"):
            socket_info.min_value = socket.min_value
        if hasattr(socket, "max_value"):
            socket_info.max_value = socket.max_value

        inputs.append(socket_info)
    return inputs


def collect_property_info(node, node_type):
    properties = []
    props_to_ignore = {"active_index", "active_output"}
    for base in node_type.__bases__:
        if hasattr(base, "bl_rna"):
            for prop in base.bl_rna.properties:
                props_to_ignore.add(prop.identifier)

    for prop in node_type.bl_rna.properties:
        if prop.identifier in props_to_ignore:
            continue

        if prop.type == "ENUM":
            # the classes quite often have enums registered with lots of potential items
            # but can only use a subset of them. We attempt to change the value for each item
            # and collect the sockets that are visible when each property is changed
            # for generating the class methods late on
            usable_values: list[EnumInfo] = []
            # default = prop.default
            prop_identifier = prop.identifier
            default = getattr(node, prop_identifier)
            for item in prop.enum_items:
                try:
                    setattr(node, prop_identifier, item.identifier)
                    usable_values.append(
                        EnumInfo(
                            identifier=item.identifier,
                            name=item.name,
                            description=item.description,
                            sockets=collect_socket_info(node.inputs),
                        )
                    )
                    setattr(node, prop_identifier, default)

                except TypeError as e:
                    print(f"TypeError: {prop.identifier}, {e}")
                    pass

            properties.append(
                PropertyInfo(
                    identifier=prop_identifier,
                    name=prop.name,
                    prop_type="ENUM",
                    enum_items=usable_values,
                    default=default,
                )
            )
        elif prop.type in ["BOOLEAN", "INT", "FLOAT", "STRING"]:
            default = prop.default if not prop.type == "STRING" else ""
            if prop.subtype == "COLOR":
                default = (0.735, 0.735, 0.735, 1.0)
                if len(prop.default_array) == 3:
                    default = (0.735, 0.735, 0.735)
            if prop.subtype in ["EULER", "XYZ"]:
                default = (0.0, 0.0, 0.0)
            if prop.subtype in ["DIRECTION"]:
                default = (0.0, 0.0, 1.0)
            properties.append(
                PropertyInfo(
                    identifier=prop.identifier,
                    name=prop.name,
                    prop_type=prop.type,
                    subtype=prop.subtype,
                    default=default,
                )
            )
    return properties


def introspect_node(node_type: type, tree_type: str) -> NodeInfo | None:
    """Introspect a Blender node type and extract all information.

    Args:
        node_type: The bpy.types node class to introspect.
        tree_type: The node tree type string (e.g. "GeometryNodeTree").
    """
    try:
        # Create temporary node group to instantiate the node
        temp_tree = bpy.data.node_groups.new("temp", tree_type)
        node: bpy.types.Node = temp_tree.nodes.new(node_type.__name__)

        # Extract basic info
        bl_idname = node_type.__name__
        name = node_type.bl_rna.name
        description = node_type.bl_rna.description or f"{name} node"
        color_tag = getattr(node, "color_tag", "UTILITY")

        inputs = collect_socket_info(node.inputs, hidden=True)
        outputs = collect_socket_info(node.outputs, hidden=True, is_output=True)
        properties = collect_property_info(node, node_type)

        # Clean up
        bpy.data.node_groups.remove(temp_tree)

        return NodeInfo(
            bl_idname=bl_idname,
            name=name,
            color_tag=color_tag,
            description=description,
            inputs=inputs,
            outputs=outputs,
            properties=properties,
            domain_sockets={},
        )

    except RuntimeError as e:
        print(f"Error introspecting {node_type.__name__} in {tree_type}: {e}")
        return None


def probe_node_tree_compatibility(node_type: type) -> list[str]:
    """Try adding a node to each tree type and return which ones succeed."""
    compatible = []
    for tree_type in TREE_TYPES:
        try:
            temp_tree = bpy.data.node_groups.new("probe", tree_type)
            temp_tree.nodes.new(node_type.__name__)
            bpy.data.node_groups.remove(temp_tree)
            compatible.append(tree_type)
        except RuntimeError:
            # Clean up on failure too
            try:
                bpy.data.node_groups.remove(temp_tree)
            except Exception:
                pass
    return compatible


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------


def generate_node_class(node_info: NodeInfo, config: TreeTypeConfig) -> str:
    """Generate Python class code for a node."""
    class_name = node_info.class_name_for_config(config)

    init_params = ["self"]
    establish_links_params = []

    # Add input sockets as parameters
    all_labels = [socket.label for socket in node_info.inputs]
    sockets_use_same_name = all(label == all_labels[0] for label in all_labels)

    for socket in node_info.inputs:
        param_name = get_socket_param_name(socket, sockets_use_same_name)

        if hasattr(socket, "default_value"):
            default = format_python_value(socket.default_value)
        else:
            default = "None"
        init_params.append(f"{param_name}: {socket.type_hint} = {default}")
        establish_links_params.append((param_name, socket))

    # Add properties as parameters
    for i, prop in enumerate(node_info.properties):
        if i == 0:
            if len(node_info.inputs) > 0:
                init_params.append("*")

        init_params.append(prop.format_property_argument())

    # Format init signature
    if len(init_params) > 2:  # If more than just self
        init_signature = "(\n        " + ",\n        ".join(init_params) + ",\n    )"
    else:
        init_signature = "(" + ", ".join(init_params) + ")"

    # Build establish_links call - map parameter names to socket identifiers
    establish_call = ""
    if establish_links_params:
        # Create mapping of parameter names to socket identifiers for _establish_links
        link_mappings = []
        for param_name, socket in establish_links_params:
            # Use socket identifier as key (which maps to the actual blender socket)
            # parameter name as value
            link_mappings.append(f'"{socket.identifier}": {param_name}')

        if link_mappings:
            establish_call = f"""        key_args = {{{", ".join(link_mappings)}}}"""
    else:
        establish_call = "        key_args = {}"

    # Build property setting calls
    property_calls = []
    for prop in node_info.properties:
        param_name = normalize_name(prop.identifier)
        property_calls.append(f"""        self.{prop.identifier} = {param_name}""")

    # if property_calls:
    property_setting = "\n".join(property_calls)

    # Generate input properties
    input_properties = [socket.format_property() for socket in node_info.inputs]
    output_properties = [socket.format_property() for socket in node_info.outputs]

    property_accessors = [
        prop.format_property_accessors() for prop in node_info.properties
    ]
    enum_methods = node_info.generate_enum_class_methods(config)

    # Add node type annotation
    node_type_annotation = (
        f"bpy.types.{node_info.bl_idname}"
        if node_info.bl_idname.startswith(
            ("Geometry", "Function", "Shader", "Compositor")
        )
        else "bpy.types.Node"
    )

    # Build class body after __init__
    body_parts = []
    if enum_methods:
        body_parts.append(enum_methods)
    if input_properties:
        body_parts.append(chr(10).join(input_properties))
    if output_properties:
        body_parts.append(chr(10).join(output_properties))
    if property_accessors:
        body_parts.append(chr(10).join(property_accessors))
    body = chr(10).join(body_parts)

    class_code = f'''class {class_name}(NodeBuilder):
    """
    {node_info.description}
    """

    _bl_idname = "{node_info.bl_idname}"
    node: {node_type_annotation}

    def __init__{init_signature}:
        super().__init__()
{establish_call}
{property_setting}
        self._establish_links(**key_args)

{body}'''

    return class_code.strip()


def get_node_names() -> list[type]:
    all_nodes = []
    for attr_name in dir(bpy.types):
        node_type = getattr(bpy.types, attr_name)
        try:
            if issubclass(node_type, bpy.types.Node):
                all_nodes.append(node_type)
        except TypeError:
            pass

    return sorted(all_nodes, key=lambda x: x.__name__)


def generate_file_header(nodes: list[NodeInfo], config: TreeTypeConfig) -> str:
    """Generate the header for generated files, importing only what's needed."""
    # Collect all type hints used across all nodes in this module
    used_type_hints: set[str] = set()
    has_sockets = False
    has_linkable = False

    for node in nodes:
        for socket in node.inputs + node.outputs:
            has_sockets = True
            hint = socket.type_mapped
            if hint == "LINKABLE":
                has_linkable = True
            else:
                used_type_hints.add(hint)
        for prop in node.properties:
            if prop.prop_type == "ENUM" and prop.enum_items:
                # Enum classmethods use sockets from each enum variant
                for enum in prop.enum_items:
                    for socket in enum.sockets:
                        has_sockets = True
                        hint = socket.type_mapped
                        if hint == "LINKABLE":
                            has_linkable = True
                        else:
                            used_type_hints.add(hint)

    lines = ["# Auto-generated by generate.py — do not edit manually."]
    lines.append("from typing import Literal")
    lines.append("import bpy")

    # Builder imports
    builder_imports = ["NodeBuilder"]
    if has_sockets:
        builder_imports.append("SocketLinker")
        builder_imports.append("VectorSocketLinker")
    lines.append(f"from ...builder import {', '.join(builder_imports)}")

    # Types imports — use canonical order matching the type_map
    type_order = [
        "LINKABLE",
        "TYPE_INPUT_BOOLEAN",
        "TYPE_INPUT_BUNDLE",
        "TYPE_INPUT_CLOSURE",
        "TYPE_INPUT_COLLECTION",
        "TYPE_INPUT_COLOR",
        "TYPE_INPUT_GEOMETRY",
        "TYPE_INPUT_IMAGE",
        "TYPE_INPUT_INT",
        "TYPE_INPUT_MATERIAL",
        "TYPE_INPUT_MATRIX",
        "TYPE_INPUT_MENU",
        "TYPE_INPUT_OBJECT",
        "TYPE_INPUT_ROTATION",
        "TYPE_INPUT_SHADER",
        "TYPE_INPUT_STRING",
        "TYPE_INPUT_VALUE",
        "TYPE_INPUT_VECTOR",
    ]
    type_imports = [
        t
        for t in type_order
        if t in used_type_hints or (t == "LINKABLE" and has_linkable)
    ]
    if type_imports:
        imports_str = ",\n    ".join(type_imports)
        lines.append(f"from ...types import (\n    {imports_str},\n)")

    return "\n\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Module writers
# ---------------------------------------------------------------------------


class ModuleWriter:
    def __init__(self, module_name: str, output_dir: Path):
        self.module_name = module_name
        self.output_dir = output_dir
        self.node_list: list[NodeInfo] = list()

    @property
    def filename(self):
        return f"{self.module_name}.py"

    def write(self, config: TreeTypeConfig):
        module_path = self.output_dir / self.filename
        with open(module_path, "w") as file:
            file.write(self.generate_content(config))

    def generate_content(self, config: TreeTypeConfig) -> str:
        print(f"Generating {self.filename} with {len(self.nodes)} nodes...")
        string = generate_file_header(self.nodes, config)
        string += "\n\n"

        for node_info in self.nodes:
            class_code = generate_node_class(node_info, config)
            string += class_code
            string += "\n\n"

        return string

    @property
    def nodes(self):
        return sorted(self.node_list, key=lambda node: node.name)

    def add_node(self, node_info: NodeInfo):
        self.node_list.append(node_info)


def _enum_properties_match(a: NodeInfo, b: NodeInfo) -> bool:
    """Check whether two NodeInfo objects have identical enum properties.

    Returns True if every ENUM property in both nodes has the same set of
    allowed values, meaning one can safely re-export the other's class.
    """

    def enum_signature(node_info: NodeInfo) -> dict[str, list[str]]:
        return {
            p.identifier: [e.identifier for e in p.enum_items]
            for p in node_info.properties
            if p.prop_type == "ENUM"
        }

    return enum_signature(a) == enum_signature(b)


class ModulesHandler:
    def __init__(
        self,
        config: TreeTypeConfig,
        gn_registry: dict[str, tuple[str, str, NodeInfo]] | None = None,
    ):
        self.config = config
        self.output_dir = config.output_dir
        self.modules: dict[str, ModuleWriter] = {}
        # Track class names to detect duplicates across modules
        self._class_names: dict[str, NodeInfo] = {}
        # Nodes re-exported from the geometry module: maps class_name → gn module name
        self._gn_reexports: dict[str, str] = {}
        # Registry from the geometry handler: maps bl_idname → (class_name, module_name)
        # Used to auto-detect nodes that were already generated for geometry.
        self._gn_registry = gn_registry or {}

    def write(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # gross and messy but currently only way I can stop it writing out experimental modules??
        for key, filename in [
            (key, item.filename) for key, item in self.modules.items()
        ]:
            if filename == "experimental.py":
                print(f"----Removing experimental module: {key}")
                self.modules.pop(key)
        self.write_modules()
        self.write_init()

    def write_modules(self):
        for module_name, module_writer in self.modules.items():
            module_writer.write(self.config)

    def generate_init(self):
        string = "# Auto-generated by generate.py — do not edit manually.\n\n"
        all_names = []
        if self.config.manually_defined:
            imports = ",\n    ".join(self.config.manually_defined)
            string += f"from .manual import (\n    {imports},\n)\n"
            all_names += list(self.config.manually_defined)

        # Emit re-exports from geometry, grouped by source module
        if self._gn_reexports:
            gn_by_module: dict[str, list[str]] = {}
            for cls_name, gn_module in self._gn_reexports.items():
                gn_by_module.setdefault(gn_module, []).append(cls_name)
            for gn_module, class_names in sorted(gn_by_module.items()):
                class_names.sort()
                all_names += class_names
                imports = ",\n    ".join(class_names)
                string += f"from ..geometry.{gn_module} import (\n    {imports},\n)\n"

        for writer in self.modules.values():
            nodes = writer.nodes
            class_names = [node.class_name_for_config(self.config) for node in nodes]
            all_names += class_names
            imports = ",\n    ".join(class_names)
            string += f"from .{writer.module_name} import (\n    {imports},\n)\n"
        all_names.sort()
        all_items = ",\n    ".join(f'"{name}"' for name in all_names)
        string += f"\n__all__ = (\n    {all_items},\n)\n"
        return string

    def write_init(self):
        filepath = self.output_dir / "__init__.py"
        with open(filepath, "w") as file:
            file.write(self.generate_init())

    def add_node(self, node_info: NodeInfo | None) -> None:
        if not node_info:
            return
        cls_name = node_info.class_name_for_config(self.config)
        if cls_name in self._class_names:
            existing = self._class_names[cls_name]
            print(
                f"  Duplicate class name '{cls_name}': "
                f"{node_info.bl_idname} vs {existing.bl_idname} — skipping {node_info.bl_idname}"
            )
            return
        self._class_names[cls_name] = node_info

        # If this exact node (by bl_idname) was already generated for geometry,
        # re-export it — unless its enum properties differ in this tree type.
        if self._gn_registry and node_info.bl_idname in self._gn_registry:
            gn_cls_name, gn_module, gn_node_info = self._gn_registry[
                node_info.bl_idname
            ]
            if _enum_properties_match(gn_node_info, node_info):
                self._gn_reexports[gn_cls_name] = gn_module
                print(f"  Re-exporting from geometry.{gn_module}: {gn_cls_name}")
                return
            else:
                print(
                    f"  Enum mismatch for {node_info.bl_idname} — "
                    f"generating separate class for {self.config.output_dir_name}"
                )

        module_name = node_info.module_name
        if module_name not in self.modules:
            self.modules[module_name] = ModuleWriter(module_name, self.output_dir)
        self.modules[module_name].add_node(node_info)

    def build_registry(self) -> dict[str, tuple[str, str, NodeInfo]]:
        """Build a bl_idname → (class_name, module_name, node_info) mapping.

        Used to pass the geometry handler's registry to subsequent handlers
        so they can auto-detect shared nodes by bl_idname and compare
        properties to ensure compatibility.
        """
        registry: dict[str, tuple[str, str, NodeInfo]] = {}
        for cls_name, node_info in self._class_names.items():
            if cls_name in self.config.manually_defined:
                module = "manual"
            else:
                module = node_info.module_name
            registry[node_info.bl_idname] = (cls_name, module, node_info)

        # Also include manually defined nodes — they were skipped during
        # add_node so they're not in _class_names, but subsequent tree-type
        # handlers still need to detect them for re-export.
        all_nodes = get_node_names()
        for node_type in all_nodes:
            node_name = (
                node_type.bl_rna.name.title().replace(" ", "").replace("Sdf", "SDF")
            )
            if node_name in self.config.manually_defined:
                if node_type.__name__ not in registry:
                    node_info = introspect_node(node_type, self.config.tree_type)
                    if node_info:
                        cls_name = node_info.class_name_for_config(self.config)
                        registry[node_info.bl_idname] = (cls_name, "manual", node_info)

        return registry

    def count_nodes(self) -> int:
        return sum(len(module.nodes) for module in self.modules.values())


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_all():
    """Generate all node classes and write to files."""

    all_nodes = get_node_names()
    print(f"Found {len(all_nodes)} total node types in bpy.types")

    # --- Phase 1: probe tree-type compatibility for every node ---
    print("\n--- Probing node tree compatibility ---")
    node_compatibility: dict[str, list[str]] = {}
    for node_type in all_nodes:
        compatible = probe_node_tree_compatibility(node_type)
        if compatible:
            node_compatibility[node_type.__name__] = compatible

    # Report multi-tree nodes
    multi_tree_nodes: dict[str, list[str]] = {
        name: trees for name, trees in node_compatibility.items() if len(trees) > 1
    }
    if multi_tree_nodes:
        print(f"\nNodes compatible with multiple tree types ({len(multi_tree_nodes)}):")
        for name, trees in sorted(multi_tree_nodes.items()):
            tree_labels = [t.replace("NodeTree", "") for t in trees]
            print(f"  {name}: {', '.join(tree_labels)}")

    # --- Phase 2: generate per-tree-type ---
    # After processing geometry, we pass its registry to subsequent handlers
    # so they can auto-detect nodes already defined in geometry.
    gn_registry: dict[str, tuple[str, str, NodeInfo]] = {}

    for config in ALL_CONFIGS:
        print(f"\n{'=' * 60}")
        print(f"Generating {config.output_dir_name} nodes ({config.tree_type})")
        print(f"{'=' * 60}")

        handler = ModulesHandler(
            config, gn_registry=gn_registry if gn_registry else None
        )
        skipped_count = 0

        for node_type in all_nodes:
            # Skip nodes that can't be added to this tree type
            if config.tree_type not in node_compatibility.get(node_type.__name__, []):
                continue

            if (
                any(n in node_type.__name__ for n in config.nodes_to_skip)
                or any(n in node_type.bl_rna.name for n in config.nodes_to_skip)
                or any(
                    n
                    == node_type.bl_rna.name.title()
                    .replace(" ", "")
                    .replace("Sdf", "SDF")
                    for n in config.manually_defined
                )
            ):
                print(f"  Skipping: {node_type.__name__}")
                skipped_count += 1
                continue

            node_info = introspect_node(node_type, config.tree_type)
            if node_info:
                node_info.tree_types = node_compatibility.get(node_type.__name__, [])
            handler.add_node(node_info)

        print(f"Successfully introspected {handler.count_nodes()} nodes")
        print(f"Skipped {skipped_count} nodes")

        handler.write()

        # After processing geometry, capture its registry for subsequent handlers
        if config is GEOMETRY_CONFIG:
            gn_registry = handler.build_registry()
            print(f"Built geometry registry with {len(gn_registry)} class names")

        print(f"Generated {len(handler.modules)} module files:")
        for filename in sorted(handler.modules.keys()):
            print(f"  - {filename}")

    print("\n--- Generation complete! ---")


if __name__ == "__main__":
    generate_all()
