"""Introspect Blender node types into the NodeInfo IR."""

from __future__ import annotations

import bpy
from bpy.types import bpy_prop_array
from mathutils import Euler, Vector

from .config import TREE_TYPES
from .model import EnumInfo, NodeInfo, PropertyInfo, SocketInfo
from .util import normalize_name


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
            structure_type=getattr(socket, "inferred_structure_type", ""),
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
    props_to_ignore = {
        "active_index",
        "active_output",
        "active_item_index",
        "socket_idname",
    }
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
                            output_sockets=collect_socket_info(
                                node.outputs, is_output=True
                            ),
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


# Introspecting a node spins up and tears down a temporary node group, which is
# the slow part of generation; cache by (bl_idname, tree_type) so the per-tree
# loop and the re-export registry never pay for it twice.
_INTROSPECT_CACHE: dict[tuple[str, str], "NodeInfo | None"] = {}


def introspect_node(node_type: type, tree_type: str) -> NodeInfo | None:
    """Introspect a Blender node type and extract all information.

    Args:
        node_type: The bpy.types node class to introspect.
        tree_type: The node tree type string (e.g. "GeometryNodeTree").
    """
    cache_key = (node_type.__name__, tree_type)
    if cache_key in _INTROSPECT_CACHE:
        return _INTROSPECT_CACHE[cache_key]
    result = _introspect_node_uncached(node_type, tree_type)
    _INTROSPECT_CACHE[cache_key] = result
    return result


def _introspect_node_uncached(node_type: type, tree_type: str) -> NodeInfo | None:
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

        # Collect per-value socket snapshots for any input socket named "Type"
        # that is a MENU.  Mirrors what collect_property_info does for enum properties.
        type_socket_enums: list[EnumInfo] = []
        for live_socket in node.inputs:
            if normalize_name(live_socket.identifier) != "type":
                continue
            if live_socket.type != "MENU":
                continue
            menu_items = _collect_socket_menu_items(live_socket)
            if not menu_items:
                continue
            # Build identifier → description map from the socket's RNA enum items.
            rna_descriptions: dict[str, str] = {}
            try:
                enum_prop = live_socket.bl_rna.properties.get("default_value")
                if enum_prop and hasattr(enum_prop, "enum_items"):
                    for rna_item in enum_prop.enum_items:
                        rna_descriptions[rna_item.identifier] = rna_item.description
            except Exception:
                pass

            saved = live_socket.default_value
            for raw_item in menu_items:
                item_value = raw_item.strip("'\"")
                try:
                    live_socket.default_value = item_value
                    type_socket_enums.append(
                        EnumInfo(
                            identifier=item_value,
                            name=item_value,
                            description=rna_descriptions.get(item_value, ""),
                            sockets=collect_socket_info(node.inputs),
                        )
                    )
                except Exception:
                    pass
                finally:
                    live_socket.default_value = saved
            break  # only handle the first "Type" socket

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
            type_socket_enums=type_socket_enums,
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
