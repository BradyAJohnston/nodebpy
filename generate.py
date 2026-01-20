"""
Code generator for Blender geometry node classes.

This script introspects Blender's node registry and generates Python classes
for all geometry nodes with proper type hints and autocomplete support.

Run this script from within Blender to generate node classes:
    blender --background --python generator.py

"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import bpy
from bpy.types import bpy_prop_array
from mathutils import Euler, Vector

NODES_TO_SKIP = [
    "Closure",
    "Simulation",
    "Repeat",
    "ForEach",
    "IndexSwitch",
    "MenuSwitch",
    "VectorMath",
    "CaptureAttribute",
    "JoinGeometry",
    "AlignEulerToVector",
    "Legacy",
]


@dataclass
class SocketInfo:
    """Information about a node socket."""

    name: str
    identifier: str  # Internal identifier
    label: str  # Socket label (empty string if no label)
    bl_socket_type: str  # e.g., "NodeSocketGeometry", "NodeSocketFloat"
    socket_type: str  # e.g., "GEOMETRY", "FLOAT", "VECTOR"
    is_output: bool
    is_multi_input: bool = False
    default_value: Any = None
    min_value: Any = None
    max_value: Any = None


@dataclass
class PropertyInfo:
    """Information about a node property."""

    identifier: str
    name: str
    prop_type: str  # 'ENUM', 'BOOLEAN', 'INT', 'FLOAT', etc.
    subtype: str | None = None
    enum_items: list[tuple[str, str]] | None = None  # [(identifier, name), ...]
    default: Any = None


@dataclass
class NodeInfo:
    """Complete information about a node type."""

    bl_idname: str  # e.g., "GeometryNodeSetPosition"
    name: str  # Human-readable name
    color_tag: str  # e.g., "GEOMETRY", "CONVERTER", "INPUT"
    description: str
    inputs: list[SocketInfo]
    outputs: list[SocketInfo]
    properties: list[PropertyInfo]

    @property
    def class_name(self):
        return python_class_name(self.name)


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
    if use_identifier:
        return normalize_name(socket.identifier)
    else:
        display_name = socket.label if socket.label else socket.name
        return normalize_name(display_name)


def python_class_name(name: str) -> str:
    """Convert 'set position' to 'SetPosition'.

    Handles edge cases like '3D Cursor' -> 'Cursor3D' to ensure valid Python identifiers.
    """
    # Replace common separators with spaces
    class_name = name.replace("_", " ").replace("-", " ")

    # Remove any characters that aren't alphanumeric or spaces
    # This handles cases like "Field Min&Max" -> "Field Min Max"
    class_name = "".join(c if c.isalnum() or c.isspace() else "" for c in class_name)
    class_name = class_name.title().replace(" ", "")

    # special mapping to upper case for things like "UV"
    replacements = {
        "Uv": "UV",
        "Sdf": "SDF",
        "3DCursor": "Cursor3D",
        "GeometryNode": "",
        "ShaderMath": "",
        "FunctionNode": "",
        "Node": "",
        "Xyz": "XYZ",
        "Id": "ID",
        "Bézier": "Bezier",
        "ImportStl": "ImportSTL",
        "ImportObj": "ImportOBJ",
        "ImportCsv": "ImportCSV",
        "ImportPly": "ImportPLY",
        "Vdb": "VDB",
        "3DLocation": "Location3D",
    }

    # Apply replacements
    for key, value in replacements.items():
        class_name = class_name.replace(key, value)

    return class_name


def get_socket_type_hint(socket_info: SocketInfo) -> str:
    """Get the Python type hint for a socket."""
    # Map Blender socket types to our type hints
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
    }
    for key in type_map.keys():
        if key in socket_info.bl_socket_type:
            return type_map[key]


def get_socket_type_annotation(socket_info: SocketInfo) -> str:
    """Get the Python type annotation for socket properties."""
    # Map Blender socket types to SocketLinker for consistency
    type_map = {
        "NodeSocketGeometry": "SocketLinker",
        "NodeSocketBool": "SocketLinker",
        "NodeSocketVector": "SocketLinker",
        "NodeSocketRotation": "SocketLinker",
        "NodeSocketFloat": "SocketLinker",
        "NodeSocketInt": "SocketLinker",
        "NodeSocketString": "SocketLinker",
        "NodeSocketColor": "SocketLinker",
        "NodeSocketMaterial": "SocketLinker",
        "NodeSocketImage": "SocketLinker",
        "NodeSocketObject": "SocketLinker",
        "NodeSocketCollection": "SocketLinker",
    }

    return type_map.get(socket_info.bl_socket_type, "SocketLinker")


def format_python_value(value: Any) -> str:
    """Format a Python value as a string for code generation."""
    if value is None:
        return "None"
    elif isinstance(value, str):
        return repr(value)
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
            return repr(value)
        except Exception:
            return "None"


def introspect_node(node_type: type) -> NodeInfo | None:
    """Introspect a Blender node type and extract all information."""
    try:
        # Create temporary node group to instantiate the node
        temp_tree = bpy.data.node_groups.new("temp", "GeometryNodeTree")
        node: bpy.types.Node = temp_tree.nodes.new(node_type.__name__)

        # Extract basic info
        bl_idname = node_type.__name__
        name = node_type.bl_rna.name
        description = node_type.bl_rna.description or f"{name} node"
        color_tag = getattr(node, "color_tag", "UTILITY")

        # Extract input sockets
        inputs = []
        for socket in node.inputs:
            if not socket.enabled:
                continue

            socket_info = SocketInfo(
                name=socket.name,
                identifier=socket.identifier,
                label=getattr(socket, "label", ""),  # Capture socket label
                bl_socket_type=type(socket).__name__,
                socket_type=socket.type,
                is_output=False,
                is_multi_input=getattr(socket, "is_multi_input", False),
            )

            if hasattr(socket, "default_value"):
                value = socket.default_value
                if isinstance(value, (Euler, Vector, bpy_prop_array)):
                    value = list(value)
                socket_info.default_value = value

            if hasattr(socket, "min_value"):
                socket_info.min_value = socket.min_value
            if hasattr(socket, "max_value"):
                socket_info.max_value = socket.max_value

            inputs.append(socket_info)

        # Extract output sockets
        outputs = []
        for socket in node.outputs:
            if not socket.enabled:
                continue

            socket_info = SocketInfo(
                name=socket.name,
                identifier=socket.identifier,
                label=getattr(socket, "label", ""),  # Capture socket label
                bl_socket_type=type(socket).__name__,
                socket_type=socket.type,
                is_output=True,
            )
            outputs.append(socket_info)

        # Extract properties (enum menus, boolean flags, etc.)
        properties = []
        parent_props = set()
        for base in node_type.__bases__:
            if hasattr(base, "bl_rna"):
                for prop in base.bl_rna.properties:
                    parent_props.add(prop.identifier)

        for prop in node_type.bl_rna.properties:
            if prop.identifier in parent_props:
                continue

            if prop.type == "ENUM":
                enum_items = [(item.identifier, item.name) for item in prop.enum_items]
                usable_values = []
                default = getattr(node, prop.identifier)
                for id, other in enum_items:
                    try:
                        setattr(node, prop.identifier, id)
                        usable_values.append((id, other))
                    except Exception:
                        pass

                properties.append(
                    PropertyInfo(
                        identifier=prop.identifier,
                        name=prop.name,
                        prop_type="ENUM",
                        enum_items=usable_values,
                        default=default,
                    )
                )
            elif prop.type in ["BOOLEAN", "INT", "FLOAT", "STRING"]:
                properties.append(
                    PropertyInfo(
                        identifier=prop.identifier,
                        name=prop.name,
                        prop_type=prop.type,
                        subtype=prop.subtype,
                        default=prop.default,
                    )
                )

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
        )

    except Exception as e:
        print(f"Error introspecting {node_type.__name__}: {e}")
        return None


def generate_enum_class_methods(node_info: NodeInfo) -> str:
    """Generate @classmethod convenience methods for enum operations."""
    methods = []

    # Find the main operation enum (usually contains "operation" in name)
    operation_enum = None
    for prop in node_info.properties:
        if prop.prop_type == "ENUM" and (
            "operation" in prop.identifier.lower() or prop.identifier == "type"
        ):
            operation_enum = prop
            break

    if not operation_enum:
        return ""

    # Generate method for each enum value
    for enum_id, enum_name in operation_enum.enum_items:
        method_name = enum_id.lower()

        # Handle special cases for better naming
        method_name = method_name.replace("_", "")
        if method_name == "and":
            method_name = "l_and"
        elif method_name == "or":
            method_name = "l_or"
        elif method_name == "not":
            method_name = "l_not"
        else:
            # Add underscore suffix to avoid Python keyword conflicts for others
            method_name = f"{method_name}"

        # Skip invalid method names
        if not method_name.replace("_", "").replace("l", "").isalnum():
            continue

        # Generate method signature based on node inputs (excluding operation socket)
        input_params = ["cls"]
        call_params = []

        all_labels = [socket.label for socket in node_info.inputs]
        sockets_use_same_name = all(label == all_labels[0] for label in all_labels)
        for socket in node_info.inputs:
            # Use label-based parameter naming
            param_name = get_socket_param_name(socket, sockets_use_same_name)
            if (
                param_name
                and param_name != ""
                and param_name != normalize_name(operation_enum.identifier)
            ):
                type_hint = get_socket_type_hint(socket)
                input_params.append(
                    f"{param_name}: {type_hint} = {socket.default_value}"
                )
                # Use the same parameter name as in the constructor
                call_params.append(f"{param_name}={param_name}")

        params_str = ",\n        ".join(input_params)
        call_params_str = ", ".join(call_params)

        # Add operation parameter to call
        operation_param = f'{operation_enum.identifier}="{enum_id}"'
        if call_params_str:
            call_params_str = f"{operation_param}, {call_params_str}"
        else:
            call_params_str = operation_param

        method = f'''
    @classmethod
    def {method_name}(
        {params_str}
    ) -> "{node_info.class_name}":
        """Create {node_info.name} with operation '{enum_name}'."""
        return cls({call_params_str})'''

        methods.append(method)

    return "".join(methods)


def generate_node_class(node_info: NodeInfo) -> tuple[str, bool]:
    """Generate Python class code for a node.

    Returns:
        tuple[str, bool]: (generated code, has_dynamic_sockets)
    """
    class_name = node_info.class_name
    has_dynamic_sockets = False

    # Build __init__ parameters
    init_params = ["self"]
    establish_links_params = []

    # Add input sockets as parameters
    all_labels = [socket.label for socket in node_info.inputs]
    sockets_use_same_name = all(label == all_labels[0] for label in all_labels)
    for socket in node_info.inputs:
        param_name = get_socket_param_name(socket, sockets_use_same_name)

        # Skip unnamed sockets (dynamic sockets that users can drag into)
        # TODO: Support dynamic multi-input sockets properly
        if not param_name or param_name.strip() == "":
            has_dynamic_sockets = True
            continue

        type_hint = get_socket_type_hint(socket)

        if hasattr(socket, "default_value"):
            default = format_python_value(socket.default_value)
        else:
            default = "None"
        init_params.append(f"{param_name}: {type_hint} = {default}")
        establish_links_params.append((param_name, socket))

    # Add properties as parameters
    for prop in node_info.properties:
        param_name = normalize_name(prop.identifier)
        if class_name == "AxesToRotation":
            param_name += "_axis"
        match prop.prop_type:
            case "ENUM":
                if prop.enum_items:
                    # Create type literal for enum
                    enum_values = [item[0] for item in prop.enum_items]
                    enums_joined = ", ".join(f'"{val}"' for val in enum_values)
                    enum_type = f"Literal[{enums_joined}]"
                    init_params.append(f'{param_name}: {enum_type} = "{prop.default}"')
            case "BOOLEAN":
                init_params.append(f"{param_name}: bool  = {prop.default}")
            case "INT":
                init_params.append(f"{param_name}: int  = {prop.default}")
            case "FLOAT":
                init_params.append(f"{param_name}: float = {prop.default}")
            case "STRING":
                init_params.append(f'{param_name}: str = "{prop.default}"')
            case _:
                init_params.append(f"{param_name}: Any | None = None")

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
        establish_call = "        key_args = kwargs"

    # Build property setting calls
    property_calls = []
    for prop in node_info.properties:
        param_name = normalize_name(prop.identifier)
        property_calls.append(f"""        self.{prop.identifier} = {param_name}""")

    # if property_calls:
    property_setting = "\n".join(property_calls)

    # Generate input properties
    input_properties = []
    used_input_names = set()
    for socket in node_info.inputs:
        if not socket.identifier or socket.identifier.strip() == "":
            continue

        prop_name = f"i_{normalize_name(socket.name)}"
        if prop_name in used_input_names:
            prop_name = f"i_{normalize_name(socket.identifier)}"

        if prop_name in used_input_names:
            continue

        used_input_names.add(prop_name)
        socket_type_annotation = get_socket_type_annotation(socket)

        input_properties.append(
            f'    @property\n    def {prop_name}(self) -> {socket_type_annotation}:\n        """Input socket: {socket.name}"""\n        return self._input("{socket.identifier}")'
        )

    # Generate output properties
    output_properties = []
    used_output_names = set()
    for socket in node_info.outputs:
        if not socket.identifier or socket.identifier.strip() == "":
            continue

        prop_name = f"o_{normalize_name(socket.name)}"
        if prop_name in used_output_names:
            prop_name = f"o_{normalize_name(socket.identifier)}"

        if prop_name in used_output_names:
            continue

        used_output_names.add(prop_name)
        socket_type_annotation = get_socket_type_annotation(socket)

        output_properties.append(
            f'    @property\n    def {prop_name}(self) -> {socket_type_annotation}:\n        """Output socket: {socket.name}"""\n        return self._output("{socket.identifier}")'
        )

    # Generate property accessors for node properties
    property_accessors = []
    for prop in node_info.properties:
        prop_name = normalize_name(prop.identifier)
        if prop.prop_type == "ENUM" and prop.enum_items:
            # Create type literal for enum
            enum_values = [item[0] for item in prop.enum_items]
            enum_type = f"Literal[{', '.join(repr(val) for val in enum_values)}]"
            property_accessors.append(
                f"    @property\n    def {prop_name}(self) -> {enum_type}:\n        return self.node.{prop.identifier}\n\n    @{prop_name}.setter\n    def {prop_name}(self, value: {enum_type}):\n        self.node.{prop.identifier} = value"
            )

        else:
            match prop.prop_type:
                case "BOOLEAN":
                    type = "bool"
                case "INT":
                    type = "int"
                case "FLOAT":
                    match prop.subtype:
                        case "XYZ":
                            type = "tuple[float, float, float]"
                        case "COLOR_GAMMA":
                            type = "tuple[float, float, float, float]"
                        case _:
                            type = "float"
                case "STRING":
                    type = "str"
                case _:
                    raise ValueError(f"Unsupported property type: {prop.prop_type}")
            property_accessors.append(
                f"    @property\n    def {prop_name}(self) -> {type}:\n        return self.node.{prop.identifier}\n\n    @{prop_name}.setter\n    def {prop_name}(self, value: {type}):\n        self.node.{prop.identifier} = value"
            )

    # Generate enum convenience methods
    enum_methods = generate_enum_class_methods(node_info)

    # Add node type annotation
    node_type_annotation = (
        f"bpy.types.{node_info.bl_idname}"
        if node_info.bl_idname.startswith(("Geometry", "Function", "Shader"))
        else "bpy.types.Node"
    )

    # Build class
    class_code = f'''class {class_name}(NodeBuilder):
    """{node_info.description}"""

    name = "{node_info.bl_idname}"
    node: {node_type_annotation}

    def __init__{init_signature}:
        super().__init__()
{establish_call}
{property_setting}
        self._establish_links(**key_args)
{enum_methods}

{chr(10).join(input_properties)}

{chr(10).join(output_properties)}

{chr(10).join(property_accessors)}
'''

    return class_code.strip(), has_dynamic_sockets


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


def generate_file_header() -> str:
    """Generate the header for generated files."""
    return """from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)

"""


def get_filename_for_node(node_info: NodeInfo) -> str:
    """Determine the target filename for a node based on color_tag and special cases."""
    # Special cases for zones
    if any(
        keyword in node_info.bl_idname
        for keyword in ["Repeat", "ForEach", "Simulation"]
    ):
        return "zone"

    # Special cases for grid/volume nodes
    if any(keyword in node_info.bl_idname for keyword in ["Volume", "Grid"]):
        return "grid" if node_info.class_name != "Grid" else "geometry"

    if "List" in node_info.bl_idname:
        return "experimental"

    # Map color_tag to filename
    color_tag_to_filename = {
        "GEOMETRY": "geometry",
        "CONVERTER": "converter",
        "INPUT": "input",
        "OUTPUT": "output",
        "ATTRIBUTE": "attribute",
        "COLOR": "converter",  # Color manipulation nodes typically conversion-related
        "TEXTURE": "texture",
        "GROUP": "group",
        "INTERFACE": "interface",  # Interface nodes are utility-like
        "LAYOUT": "layout",
        "VECTOR": "vector",
    }

    # Get filename from color_tag, default to utilities.py
    filename = color_tag_to_filename.get(node_info.color_tag, "utilities.py")

    return filename


class BaseModuleWriter:
    output_dir = Path(__file__).parent / "src/nodebpy/nodes/"


class ModuleWriter(BaseModuleWriter):
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.node_list: list[NodeInfo] = list()

    @property
    def filename(self):
        return f"{self.module_name}.py"

    def write(self):
        module_path = self.output_dir / self.filename
        with open(module_path, "w") as file:
            file.write(self.generate_content())

    def generate_content(self) -> str:
        print(f"Generating {self.filename} with {len(self.nodes)} nodes...")
        string = ""
        string += generate_file_header()
        string += "\n\n"

        for node_info in self.nodes:
            try:
                class_code, has_dynamic = generate_node_class(node_info)
                string += class_code
                string += "\n\n"
            except Exception as e:
                print(f"  Error generating {node_info.name}: {e}")

        return string

    @property
    def nodes(self):
        return sorted(self.node_list, key=lambda node: node.name)

    def add_node(self, node_info: NodeInfo):
        self.node_list.append(node_info)


class ModulesHandler(BaseModuleWriter):
    def __init__(self):
        super().__init__()
        self.modules: dict[str, ModuleWriter] = {}

    def write(self):
        self.write_modules()
        self.write_init()

    def write_modules(self):
        for module_name, module_writer in self.modules.items():
            module_writer.write()

    def generate_init(self):
        string = '"""Auto-generated init file from generate.py"""\n\n'
        all = []
        for writer in self.modules.values():
            nodes = writer.nodes
            all += [node.class_name for node in nodes]
            string += "from .{} import ({})\n".format(
                writer.module_name, ",\n".join([node.class_name for node in nodes])
            )
        all.sort()
        all_string = "\n__all__ = ({})".format(
            ",\n".join([f'"{name}"' for name in all])
        )
        return string + all_string

    def write_init(self):
        filepath = self.output_dir / "__init__.py"
        with open(filepath, "w") as file:
            file.write(self.generate_init())

    def add_node(self, node_info: NodeInfo | None) -> None:
        if not node_info:
            return
        module_name = get_filename_for_node(node_info)
        if module_name not in self.modules:
            self.modules[module_name] = ModuleWriter(module_name)
        self.modules[module_name].add_node(node_info)

    def count_nodes(self) -> int:
        return sum(len(module.nodes) for module in self.modules.values())


def generate_all():
    """Generate all node classes and write to files."""
    handler = ModulesHandler()

    print(f"Generating node classes to {handler.output_dir}")

    all_nodes = get_node_names()
    print(f"Found {len(all_nodes)} geometry nodes")

    node_infos = []
    skipped_count = 0

    for node_type in all_nodes:
        if any([n in node_type.__name__ for n in NODES_TO_SKIP]):
            print(f"  Skipping manually specified node: {node_type.__name__}")
            skipped_count += 1
            continue

        handler.add_node(introspect_node(node_type))

    print(f"Successfully introspected {handler.count_nodes()} nodes")
    print(f"Skipped {skipped_count} manually specified nodes")

    handler.write()

    print("\nGeneration complete!")
    print(f"Generated {len(handler.modules)} files:")
    for filename in sorted(handler.modules.keys()):
        print(f"  - {filename}")
    print(f"\nTotal: {len(node_infos)} node classes")


if __name__ == "__main__":
    generate_all()
