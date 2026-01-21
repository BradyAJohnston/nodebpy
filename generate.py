"""
Code generator for Blender geometry node classes.

This script introspects Blender's node registry and generates Python classes
for all geometry nodes with proper type hints and autocomplete support.

Run this script from within Blender to generate node classes:
    blender --background --python generator.py

"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import bpy
from bpy.types import bpy_prop_array
from mathutils import Euler, Vector
from typing_extensions import Literal

NODES_TO_SKIP = [
    "AlignEulerToVector",
    "Legacy",
    "Closure",
    "Simulation",
    "For Each",
    "Frame",
    "GridBoolean",
    "Reroute",
    #
    "FieldMinAndMax",
]


MANUALLY_DEFINED = (
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
    "FormatString",
    "Value",
    "AccumulateField",
    "EvaluateAtIndex",
    "FieldAverage",
    "FieldMinAndMax",
    "EvaluateOnDomain",
    "FieldVariance",
    "Compare",
    "AttributeStatistic",
)


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

    def format_argument_string(self) -> str:
        type_hint = get_socket_type_hint(self)
        param_name = get_socket_param_name(self)
        return f"{param_name}: {type_hint} = {format_python_value(self.default_value)}"

    def format_property(self) -> str:
        """Generate the property string for this socket."""
        prop_name = "{}_{}".format(
            "o" if self.is_output else "i", normalize_name(self.identifier)
        )
        socket_type_annotation = get_socket_type_annotation(self)
        description = "{} socket: {}".format(
            "Output" if self.is_output else "Input", self.name
        )
        if self.description != "":
            description += f"\n        {self.description}\n        "

        return f'''
    @property
    def {prop_name}(self) -> {socket_type_annotation}:
        """{description}"""
        return self._{"output" if self.is_output else "input"}("{self.identifier}")
'''


@dataclass
class EnumInfo:
    """Information about a node enum property."""

    identifier: str
    name: str
    description: str = ""
    sockets: list[SocketInfo] | None = None


@dataclass
class PropertyInfo:
    """Information about a node property."""

    identifier: str
    name: str
    prop_type: Literal["ENUM", "BOOLEAN", "INT", "FLOAT", "STRING", "COLOR", "VECTOR"]
    subtype: str | None = None
    enum_items: list[EnumInfo] | None = None
    default: Any = None

    def enum_values_to_literal(self) -> str:
        if self.enum_items is None:
            return ""
        return (
            f"Literal[{', '.join(repr(item.identifier) for item in self.enum_items)}]"
        )

    def format_name(self) -> str:
        prop_name = normalize_name(self.identifier)
        if prop_name in ["primary_axis", "secondary_axis"]:
            prop_name = prop_name.replace("_axis", "")
        return prop_name

    def format_property_argument(self) -> str:
        match self.prop_type:
            case "ENUM":
                type = self.enum_values_to_literal()
                default = f'"{self.default}"'
            case "BOOLEAN":
                type = "bool"
                default = self.default
            case "INT":
                type = "int"
                default = self.default
            case "FLOAT":
                match self.subtype:
                    case "COLOR":
                        type = "tuple[float, float, float, float]"
                        default = self.default
                    case "EULER" | "XYZ":
                        type = "tuple[float, float, float]"
                        default = self.default
                    case _:
                        type = "float"
                        default = round(self.default, 3)
            case "STRING":
                type = "str"
                default = f'"{self.default}"'
            case _:
                raise ValueError(f"Unsupported property type: {self.prop_type}")

        return "{}: {} = {}".format(self.format_name(), type, default)

    def format_property_accessors(self) -> str:
        prop_name = self.format_name()
        match self.prop_type:
            case "ENUM":
                type = self.enum_values_to_literal()
            case "BOOLEAN":
                type = "bool"
            case "INT":
                type = "int"
            case "FLOAT":
                match self.subtype:
                    case "COLOR":
                        type = "tuple[float, float, float, float]"
                    case "EULER" | "XYZ":
                        type = "tuple[float, float, float]"
                    case _:
                        type = "float"
            case "STRING":
                type = "str"
            case _:
                raise ValueError(f"Unsupported property type: {self.prop_type}")

        return f"""\n
    @property
    def {prop_name}(self) -> {type}:
        return self.node.{self.identifier}

    @{prop_name}.setter
    def {prop_name}(self, value: {type}):
        self.node.{self.identifier} = value
    \n
    """


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
    domain_sockets: dict[str, list[SocketInfo]]

    @property
    def class_name(self):
        return python_class_name(self.name)

    def generate_enum_class_methods(self) -> str:
        """Generate @classmethod convenience methods for enum operations."""
        methods = []

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
                method_name = enum.name.lower()
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

                # Skip invalid method names
                if not method_name.replace("_", "").replace("l", "").isalnum():
                    continue

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
                        type_hint = get_socket_type_hint(socket)
                        input_params.append(
                            f"{param_name}: {type_hint} = {format_python_value(socket.default_value)}"
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
    ) -> "{self.class_name}":
        """Create {self.name} with operation '{enum.name}'."""
        return cls({call_params_str})'''

                methods.append(method)

        return "".join(methods)


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
        return repr(value) if value != "" else "''"
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


def collect_socket_info(
    sockets: bpy.types.bpy_prop_collection[bpy.types.NodeSocket],
    hidden=False,
    is_output=False,
) -> list[SocketInfo]:
    """Extract socket infos for a current node state"""
    inputs = []
    for socket in sockets:
        # GN switch sockets are innactive one or the other so we have to
        # be explicit to capture all of them
        if socket.node.bl_idname != "GeometryNodeSwitch":
            if (socket.is_inactive and not hidden) or "__extend__" in socket.identifier:
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
            if prop.subtype in ["EULER", "XYZ"]:
                default = (0.0, 0.0, 0.0)
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


def introspect_node(node_type: type) -> NodeInfo | None:
    """Introspect a Blender node type and extract all information."""
    try:
        # Create temporary node group to instantiate the node"
        temp_tree = bpy.data.node_groups.new("temp", "GeometryNodeTree")
        node: bpy.types.Node = temp_tree.nodes.new(node_type.__name__)

        # Extract basic info
        bl_idname = node_type.__name__
        name = node_type.bl_rna.name
        description = node_type.bl_rna.description or f"{name} node"
        color_tag = getattr(node, "color_tag", "UTILITY")

        inputs = collect_socket_info(node.inputs, hidden=True)
        outputs = collect_socket_info(node.outputs, hidden=True, is_output=True)
        properties = collect_property_info(node, node_type)

        # Extract properties (enum menus, boolean flags, etc.)

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
        print(f"Error introspecting {node_type.__name__}: {e}")
        return None


def generate_node_class(node_info: NodeInfo) -> str:
    """Generate Python class code for a node.

    Returns:
        tuple[str, bool]: (generated code, has_dynamic_sockets)
    """

    init_params = ["self"]
    establish_links_params = []

    # Add input sockets as parameters
    all_labels = [socket.label for socket in node_info.inputs]
    sockets_use_same_name = all(label == all_labels[0] for label in all_labels)

    for socket in node_info.inputs:
        param_name = get_socket_param_name(socket, sockets_use_same_name)
        type_hint = get_socket_type_hint(socket)

        if hasattr(socket, "default_value"):
            default = format_python_value(socket.default_value)
        else:
            default = "None"
        init_params.append(f"{param_name}: {type_hint} = {default}")
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
    enum_methods = node_info.generate_enum_class_methods()

    # Add node type annotation
    node_type_annotation = (
        f"bpy.types.{node_info.bl_idname}"
        if node_info.bl_idname.startswith(("Geometry", "Function", "Shader"))
        else "bpy.types.Node"
    )

    # Build class
    class_code = f'''class {node_info.class_name}(NodeBuilder):
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


def generate_file_header() -> str:
    """Generate the header for generated files."""
    return """from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_BUNDLE,
    TYPE_INPUT_CLOSURE,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_MATERIAL,
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
        "COLOR": "color",
        "TEXTURE": "texture",
        "GROUP": "group",
        "INTERFACE": "interface",
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
            # try:
            class_code = generate_node_class(node_info)
            string += class_code
            string += "\n\n"
            # except Exception as e:
            #     print(f"  Error generating {node_info.name}: {e}")

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
        string += f"from .manual import ({', '.join(MANUALLY_DEFINED)})\n"
        all += [name for name in MANUALLY_DEFINED]
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
        if (
            any([n in node_type.__name__ for n in NODES_TO_SKIP])
            or any([n in node_type.bl_rna.name for n in NODES_TO_SKIP])
            or any(
                [
                    n
                    == node_type.bl_rna.name.title()
                    .replace(" ", "")
                    .replace("Sdf", "SDF")
                    for n in MANUALLY_DEFINED
                ]
            )
        ):
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
