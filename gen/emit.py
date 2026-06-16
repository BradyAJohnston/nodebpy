"""Render NodeInfo objects (and module headers) into Python source."""

from __future__ import annotations

import typing

from .config import (
    SOCKET_TYPES,
    _OUTPUT_SOCKET_CLASSES,
    TreeTypeConfig,
    nodebpy_types,
)
from .customizations import _CUSTOMIZATIONS
from .model import NodeInfo, PropertyInfo, SocketInfo
from .util import format_python_value, get_socket_param_name, normalize_name


def generate_node_class(node_info: NodeInfo, config: TreeTypeConfig) -> str:
    """Generate Python class code for a node."""
    class_name = node_info.class_name_for_config(config)
    custom = _CUSTOMIZATIONS.get(node_info.bl_idname)
    suppress = custom.suppress if custom else frozenset()

    # A node is generic when its output and/or input sockets change type across
    # enum values, with all varying sockets on a side sharing one type per value
    # (so a single _S/_T suffices). The output side drives nodes like Switch/Mix
    # and the multi-output field nodes (leading/trailing/total); the input side
    # alone drives nodes like Compare whose output is a fixed Boolean. Varying
    # inputs are typed _S and their __init__ params accept InputAny.
    varying_outputs = node_info.varying_output_identifiers
    varying_inputs = node_info.varying_input_identifiers
    outputs_generic = node_info.outputs_generic
    inputs_generic = node_info.inputs_generic
    is_generic = outputs_generic or inputs_generic
    if not inputs_generic:
        varying_inputs = set()

    init_params = ["self"]
    establish_links_params = []

    # Add input sockets as parameters
    all_labels = [socket.label for socket in node_info.inputs]
    sockets_use_same_name = all(label == all_labels[0] for label in all_labels)

    # For sockets that change type across enum states (e.g. a "Value" socket that is
    # Float in the default state but Vector when data_type="VECTOR"), widen the __init__
    # parameter to accept all possible types so factory classmethods type-check cleanly.
    _socket_type_variants: dict[str, set[str]] = {}
    for s in node_info.inputs:
        _socket_type_variants.setdefault(s.identifier, set()).add(s.type_hint)
    for prop in node_info.properties:
        for enum in prop.enum_items:
            for s in enum.sockets:
                if s.identifier in _socket_type_variants:
                    _socket_type_variants[s.identifier].add(s.type_hint)
    for enum in node_info.type_socket_enums:
        for s in enum.sockets:
            if s.identifier in _socket_type_variants:
                _socket_type_variants[s.identifier].add(s.type_hint)

    for socket in node_info.inputs:
        param_name = get_socket_param_name(socket, sockets_use_same_name)
        variants = _socket_type_variants[socket.identifier]
        if inputs_generic and socket.identifier in varying_inputs:
            # Generic input — accepts any socket type (matches the _S annotation).
            type_hint = "InputAny"
        elif len(variants) > 1:
            type_hint = " | ".join(sorted(variants))
        else:
            type_hint = socket.type_hint

        if "GRID" in socket.structure_type or "LIST" in socket.structure_type:
            default = "None"
        elif hasattr(socket, "default_value"):
            default = format_python_value(socket.default_value)
        else:
            default = "None"
        init_params.append(f"{param_name}: {type_hint} = {default}")
        establish_links_params.append((param_name, socket))

    # Add sockets that only appear in certain enum states (e.g. mode="FREE" reveals
    # a "Custom Normal" socket that isn't in the default state).  Without these the
    # generated classmethods call cls(..., custom_normal=...) but __init__ never
    # declares the parameter.
    def _generates_classmethods(prop: PropertyInfo) -> bool:
        """Mirror the filter used in generate_enum_class_methods."""
        return not (
            (
                prop.identifier not in ["operation", "domain", "mode"]
                and "type" not in prop.identifier
            )
            or prop.identifier in ["blend_type", "direction_type"]
        )

    _seen_identifiers = {s.identifier for s in node_info.inputs}
    _extra_sockets: list[SocketInfo] = []

    for prop in node_info.properties:
        if not _generates_classmethods(prop):
            continue
        for enum in prop.enum_items:
            for socket in enum.sockets:
                if socket.identifier not in _seen_identifiers:
                    _seen_identifiers.add(socket.identifier)
                    _extra_sockets.append(socket)

    for enum in node_info.type_socket_enums:
        for socket in enum.sockets:
            if socket.identifier not in _seen_identifiers:
                _seen_identifiers.add(socket.identifier)
                _extra_sockets.append(socket)

    for socket in _extra_sockets:
        param_name = get_socket_param_name(socket, sockets_use_same_name)
        init_params.append(f"{param_name}: {socket.type_hint} = None")
        establish_links_params.append((param_name, socket))

    # Add properties as parameters
    _has_socket_params = len(node_info.inputs) > 0 or bool(_extra_sockets)
    for i, prop in enumerate(node_info.properties):
        if i == 0:
            if _has_socket_params:
                init_params.append("*")

        init_params.append(prop.format_property_argument())

    # Format init signature
    if len(init_params) > 2:  # If more than just self
        init_signature = "(\n        " + ",\n        ".join(init_params) + ",\n    )"
    else:
        init_signature = "(" + ", ".join(init_params) + ")"

    # Build establish_links call - map parameter names to socket identifiers
    link_mappings = []
    for param_name, socket in establish_links_params:
        link_mappings.append(f'"{socket.identifier}": {param_name}')

    # Build property setting calls. Use ``format_name()`` (not the raw bpy
    # identifier) so the assignment goes through the property setter under the
    # same name as the constructor param — these differ when a property is
    # renamed to avoid colliding with a same-named socket (AxesToRotation's
    # ``primary_axis`` enum becomes ``primary`` because the Vector socket owns
    # ``primary_axis``).
    property_calls = []
    for prop in node_info.properties:
        param_name = prop.format_name()
        property_calls.append(f"""        self.{param_name} = {param_name}""")

    property_setting = "\n".join(property_calls)

    if _extra_sockets:
        # When there are enum-state-dependent sockets, set properties first so the
        # node reflects the correct enum state, then filter key_args at runtime to
        # only include sockets that actually exist in the current state.
        establish_call = (
            f"        _all_args = {{{', '.join(link_mappings)}}}\n"
            f"        _socket_ids = {{s.identifier for s in self.node.inputs}}\n"
            f"        key_args = {{k: v for k, v in _all_args.items() if k in _socket_ids}}"
        )
    else:
        if link_mappings:
            establish_call = f"""        key_args = {{{", ".join(link_mappings)}}}"""
        else:
            establish_call = "        key_args = {}"

    property_accessors = [
        prop.format_property_accessors()
        for prop in node_info.properties
        if prop.format_name() not in suppress
    ]
    enum_methods = node_info.generate_enum_class_methods(config, suppress)

    # Add node type annotation — always use specific type so property access is typed
    # TODO: remove the ty: ignore as its only for unreleased bpy version and the new nodes
    node_type_annotation = (
        f"bpy.types.{node_info.bl_idname}  # ty: ignore[unresolved-attribute]"
    )

    # Build numpy-style class docstring
    doc_lines = [node_info.description, ""]
    all_init_sockets = [s for s in node_info.inputs] + _extra_sockets
    if all_init_sockets:
        doc_lines += ["Parameters", "----------"]
        for socket in all_init_sockets:
            param_name = get_socket_param_name(socket, sockets_use_same_name)
            doc_lines.append(f"{param_name} : {socket.type_hint}")
            desc = socket.description if socket.description else socket.name
            doc_lines.append(f"    {desc}")
        doc_lines.append("")

    def _socket_doc_lines(sockets, prefix):
        lines = []
        for socket in sockets:
            return_type = "Socket"
            for key, cls in _OUTPUT_SOCKET_CLASSES.items():
                if key in socket.bl_socket_type:
                    return_type = cls
                    break
            attr_name = normalize_name(socket.identifier)
            desc = socket.description if socket.description else socket.name
            lines.append(f"{prefix}.{attr_name} : {return_type}")
            lines.append(f"    {desc}")
        return lines

    if all_init_sockets:
        doc_lines += ["Inputs", "------"]
        doc_lines += _socket_doc_lines(all_init_sockets, "i")
        doc_lines.append("")
    if node_info.outputs:
        doc_lines += ["Outputs", "-------"]
        doc_lines += _socket_doc_lines(node_info.outputs, "o")

    docstring_body = "\n    ".join(doc_lines).rstrip()

    # Inputs/Outputs inner classes are generic (parameterised by _S) when the
    # node is generic; see the flags computed at the top of this function.
    def _input_annotation(socket: SocketInfo) -> str:
        if inputs_generic and socket.identifier in varying_inputs:
            attr_name = normalize_name(socket.identifier)
            doc = socket.description or socket.name
            ann = f"        {attr_name}: _S"
            if doc:
                ann += f'\n        """{doc}"""'
            return ann
        return socket.format_accessor_annotation()

    # Build Inputs inner class
    input_annotations = [_input_annotation(socket) for socket in node_info.inputs] + [
        _input_annotation(socket) for socket in _extra_sockets
    ]
    inputs_base = (
        "(SocketAccessor, Generic[_S])" if inputs_generic else "(SocketAccessor)"
    )
    if input_annotations:
        inputs_class = f"    class _Inputs{inputs_base}:\n" + "\n".join(
            input_annotations
        )
    else:
        inputs_class = f"    class _Inputs{inputs_base}:\n        pass"

    output_annotations = []
    for socket in node_info.outputs:
        if outputs_generic and socket.identifier in varying_outputs:
            attr_name = normalize_name(socket.identifier)
            doc = socket.description or socket.name
            ann = f"        {attr_name}: _S"
            if doc:
                ann += f'\n        """{doc}"""'
            output_annotations.append(ann)
        else:
            output_annotations.append(socket.format_accessor_annotation())

    outputs_base = (
        "(SocketAccessor, Generic[_S])" if outputs_generic else "(SocketAccessor)"
    )
    if output_annotations:
        outputs_class = f"    class _Outputs{outputs_base}:\n" + "\n".join(
            output_annotations
        )
    else:
        outputs_class = "    class _Outputs(SocketAccessor):\n        pass"

    # Prepend any registered mixin bases (listed first so they win via MRO).
    base_classes = list(custom.bases) if custom else []
    generated_base = "BaseNode, Generic[_T]" if is_generic else "BaseNode"
    class_base = "(" + ", ".join(base_classes + [generated_base]) + ")"
    o_return_type = "_Outputs[_T]" if outputs_generic else "_Outputs"
    i_return_type = "_Inputs[_T]" if inputs_generic else "_Inputs"

    # When extra sockets exist, properties must be set before collecting socket IDs
    # so the node reflects the correct enum state when we filter key_args.
    if _extra_sockets and property_setting:
        init_body = f"\n{property_setting}\n{establish_call}"
    else:
        init_body = f"\n{establish_call}\n{property_setting}"

    # A customization may drop the generated constructor (its mixin or
    # extra_body provides one instead).
    if "__init__" in suppress:
        init_block = ""
    else:
        init_block = f"""    def __init__{init_signature}:
        super().__init__(){init_body}
        self._establish_links(**key_args)
"""

    extra_body = f"\n{custom.extra_body}\n" if custom and custom.extra_body else ""

    class_code = f'''class {class_name}{class_base}:
    """
    {docstring_body}
    """

    _bl_idname = "{node_info.bl_idname}"
    node: {node_type_annotation}

{inputs_class}

{outputs_class}

    if TYPE_CHECKING:
        @property
        def i(self) -> {i_return_type}: ...
        @property
        def o(self) -> {o_return_type}: ...

{init_block}
{enum_methods}
{chr(10).join(property_accessors) if property_accessors else ""}
{extra_body}'''

    return class_code.strip()


def generate_file_header(nodes: list[NodeInfo], config: TreeTypeConfig) -> str:
    """Generate the header for generated files, importing only what's needed."""
    # Collect all type hints used across all nodes in this module
    used_type_hints: set[str] = set()
    used_output_socket_classes: set[str] = set()
    has_sockets = False
    has_linkable = False

    def _check_socket(socket):
        nonlocal has_sockets, has_linkable
        has_sockets = True
        hint = socket.type_mapped
        if hint == "InputLinkable":
            has_linkable = True
        else:
            used_type_hints.add(hint)
        for key, cls in _OUTPUT_SOCKET_CLASSES.items():
            if key in socket.bl_socket_type:
                used_output_socket_classes.add(cls)
                break

    for node in nodes:
        for socket in node.inputs + node.outputs:
            _check_socket(socket)
        for prop in node.properties:
            if prop.prop_type == "ENUM" and prop.enum_items:
                for enum in prop.enum_items:
                    for socket in enum.sockets:
                        _check_socket(socket)

    # Collect mathutils types needed by float-array property accessors
    mathutils_needed: set[str] = set()
    for node in nodes:
        for prop in node.properties:
            mt = prop._mathutils_type
            if mt:
                mathutils_needed.add(mt)

    has_generic_nodes = any(len(n.varying_output_identifiers) == 1 for n in nodes)

    lines = ["# Auto-generated by generate.py — do not edit manually."]
    typing_imports = (
        ["TYPE_CHECKING", "Generic", "Literal"]
        if has_generic_nodes
        else ["TYPE_CHECKING", "Literal"]
    )
    lines.append(f"from typing import {', '.join(typing_imports)}")
    lines.append("import bpy")
    if mathutils_needed:
        lines.append(f"from mathutils import {', '.join(sorted(mathutils_needed))}")

    # Builder imports
    builder_imports = ["BaseNode", "SocketAccessor", "Socket"]
    # Add only the specific output socket classes actually used in this file
    # for cls in sorted(used_output_socket_classes):
    #     if cls != "Socket":
    #         builder_imports.append(cls)
    lines.append(f"from ...builder import {', '.join(builder_imports)}")

    data_types = [f"{t.title()}" for t in typing.get_args(SOCKET_TYPES)]
    data_types += ["Integer", "Color", "IntegerVector", "Linkable", "Sound"]
    data_types.sort()

    sockets = [f"{d}Socket" for d in data_types]
    grids = [
        "FloatSocketGrid",
        "IntegerSocketGrid",
        "VectorSocketGrid",
        "BooleanSocketGrid",
    ]
    lists = [s + "List" for s in sockets]
    all = sockets + grids + lists
    # InputAny is the widened type used for generic input parameters; ruff prunes
    # it from modules that don't use it.
    inputs = [f"Input{x}".replace("Socket", "") for x in all] + ["InputAny"]
    typevars = ["_T", "_S"]

    # The socket-name → Input*/…Socket mapping over-generates a few names that
    # don't actually exist (e.g. "INT" → InputInt/IntSocket, "RGBA" →
    # InputRgba/RgbaSocket; the real names are InputInteger/IntegerSocket and
    # InputColor/ColorSocket). Drop the non-existent ones — they were only ever
    # pruned later by ruff, but an unpruned stray import breaks the package on
    # the next generation run's bootstrap import. A socket class XSocket is valid
    # iff its parallel InputX exists in the (standalone-loaded) types leaf, so a
    # single existence check covers both lists without importing the package.
    def _input_name(socket_name: str) -> str:
        return "Input" + socket_name.replace("Socket", "")

    inputs = [name for name in inputs if hasattr(nodebpy_types, name)]
    socket_names = [name for name in all if hasattr(nodebpy_types, _input_name(name))]

    lines.append(f"from ...types import (\n    {',\n'.join(inputs)},\n)")

    lines.append(
        f"from ...builder.socket import ({', '.join(socket_names + typevars)})"
    )

    # Imports required by any registered customizations in this module
    # (mixin bases referenced in the class definition / extra_body).
    custom_imports: list[str] = []
    for node in nodes:
        custom = _CUSTOMIZATIONS.get(node.bl_idname)
        if custom:
            for imp in custom.imports:
                if imp not in custom_imports:
                    custom_imports.append(imp)
    lines.extend(custom_imports)

    return "\n\n".join(lines) + "\n"
