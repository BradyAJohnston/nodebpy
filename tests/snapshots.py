"""Custom syrupy snapshots for NodeBPY TreeBuilder class."""

import base64
import gzip
import json

from jsondiff import diff
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.types import SerializableData, SerializedData
from tree_clipper.common import MAGIC_STRING
from tree_clipper.export_nodes import ExportIntermediate, ExportParameters
from tree_clipper.specific_handlers import BUILT_IN_EXPORTER

from nodebpy import TreeBuilder


def _serialize_tree_builder(data: TreeBuilder) -> str:
    """Serialize TreeBuilder to compressed JSON string."""
    # Export the tree using tree_clipper
    export_intermediate = ExportIntermediate(
        parameters=ExportParameters(
            is_material=False,
            name=data.tree.name,
            specific_handlers=BUILT_IN_EXPORTER,
            export_sub_trees=True,
            debug_prints=False,
            write_from_roots=False,
        )
    )

    # Process all steps
    while export_intermediate.step():
        pass

    # Handle external references
    export_intermediate.set_external(
        (
            external_id,
            external_item.pointed_to_by.get_pointee().name,
        )
        for external_id, external_item in export_intermediate.get_external().items()
    )

    # Export to compressed string
    compressed_data = export_intermediate.export_to_str(compress=True, json_indent=4)

    return compressed_data


def _format_key_differences(
    differences: dict, expected_data: dict, current_data: dict
) -> str:
    """Format only the most important differences for readability."""
    summary = []

    # Get tree info for context
    expected_tree = expected_data.get("node_trees", [{}])[0].get("data", {})
    current_tree = current_data.get("node_trees", [{}])[0].get("data", {})

    tree_name = expected_tree.get("name", "Unknown")
    summary.append(f"Tree: {tree_name}")

    # Get node and link lists
    expected_nodes = expected_tree.get("nodes", {}).get("data", {}).get("items", [])
    current_nodes = current_tree.get("nodes", {}).get("data", {}).get("items", [])
    expected_links = expected_tree.get("links", {}).get("data", {}).get("items", [])
    current_links = current_tree.get("links", {}).get("data", {}).get("items", [])

    # Build lists of node names/types for comparison
    def get_node_signature(node_data):
        return f"{node_data.get('name', 'Unnamed')} ({node_data.get('bl_idname', 'Unknown')})"

    expected_node_sigs = [
        get_node_signature(node.get("data", {})) for node in expected_nodes
    ]
    current_node_sigs = [
        get_node_signature(node.get("data", {})) for node in current_nodes
    ]

    # Find new and missing nodes
    new_nodes = [sig for sig in current_node_sigs if sig not in expected_node_sigs]
    missing_nodes = [sig for sig in expected_node_sigs if sig not in current_node_sigs]

    if new_nodes:
        summary.append(f"• New nodes: {', '.join(new_nodes)}")
    if missing_nodes:
        summary.append(f"• Missing nodes: {', '.join(missing_nodes)}")

    # Node count summary if different
    if len(expected_nodes) != len(current_nodes):
        summary.append(
            f"• Node count: expected {len(expected_nodes)}, got {len(current_nodes)}"
        )

    # Build link signatures for comparison
    def get_link_signature(link_data, nodes_list):
        from_id = link_data.get("from_socket")
        to_id = link_data.get("to_socket")

        # Find the nodes these sockets belong to
        from_node = "Unknown"
        to_node = "Unknown"

        for node in nodes_list:
            node_data = node.get("data", {})
            # Check outputs for from_socket
            outputs = node_data.get("outputs", {}).get("data", {}).get("items", [])
            for output in outputs:
                if output.get("id") == from_id:
                    from_node = node_data.get("name", "Unknown")
                    break

            # Check inputs for to_socket
            inputs = node_data.get("inputs", {}).get("data", {}).get("items", [])
            for input_socket in inputs:
                if input_socket.get("id") == to_id:
                    to_node = node_data.get("name", "Unknown")
                    break

        return f"{from_node} → {to_node}"

    expected_link_sigs = [
        get_link_signature(link.get("data", {}), expected_nodes)
        for link in expected_links
    ]
    current_link_sigs = [
        get_link_signature(link.get("data", {}), current_nodes)
        for link in current_links
    ]

    # Find new and missing links
    new_links = [sig for sig in current_link_sigs if sig not in expected_link_sigs]
    missing_links = [sig for sig in expected_link_sigs if sig not in current_link_sigs]

    if new_links:
        summary.append(f"• New links: {', '.join(new_links)}")
    if missing_links:
        summary.append(f"• Missing links: {', '.join(missing_links)}")

    # Link count summary if different
    if len(expected_links) != len(current_links):
        summary.append(
            f"• Link count: expected {len(expected_links)}, got {len(current_links)}"
        )

    # Check for property changes in nodes when counts are the same
    if (
        len(expected_nodes) == len(current_nodes)
        and len(new_nodes) == 0
        and len(missing_nodes) == 0
    ):
        property_changes = []

        for i, (exp_node, curr_node) in enumerate(zip(expected_nodes, current_nodes)):
            exp_data = exp_node.get("data", {})
            curr_data = curr_node.get("data", {})
            node_name = curr_data.get("name", f"Node {i}")

            # Check interface socket default values
            exp_interface = (
                exp_data.get("interface", {})
                .get("data", {})
                .get("items_tree", {})
                .get("data", {})
                .get("items", [])
            )
            curr_interface = (
                curr_data.get("interface", {})
                .get("data", {})
                .get("items_tree", {})
                .get("data", {})
                .get("items", [])
            )

            for j, (exp_sock, curr_sock) in enumerate(
                zip(exp_interface, curr_interface)
            ):
                exp_sock_data = exp_sock.get("data", {})
                curr_sock_data = curr_sock.get("data", {})

                if exp_sock_data.get("default_value") != curr_sock_data.get(
                    "default_value"
                ):
                    sock_name = curr_sock_data.get("name", f"Socket {j}")
                    exp_val = exp_sock_data.get("default_value")
                    curr_val = curr_sock_data.get("default_value")
                    property_changes.append(
                        f"interface socket '{sock_name}': {exp_val} → {curr_val}"
                    )

            # Check node input socket default values
            exp_inputs = exp_data.get("inputs", {}).get("data", {}).get("items", [])
            curr_inputs = curr_data.get("inputs", {}).get("data", {}).get("items", [])

            for j, (exp_input, curr_input) in enumerate(zip(exp_inputs, curr_inputs)):
                exp_input_data = exp_input.get("data", {})
                curr_input_data = curr_input.get("data", {})

                if exp_input_data.get("default_value") != curr_input_data.get(
                    "default_value"
                ):
                    input_name = curr_input_data.get("name", f"Input {j}")
                    exp_val = exp_input_data.get("default_value")
                    curr_val = curr_input_data.get("default_value")
                    property_changes.append(
                        f"{node_name}.{input_name}: {exp_val} → {curr_val}"
                    )

            # Check other node properties
            for prop in ["operation", "use_clamp", "data_type"]:
                if (
                    prop in exp_data
                    and prop in curr_data
                    and exp_data[prop] != curr_data[prop]
                ):
                    property_changes.append(
                        f"{node_name}.{prop}: {exp_data[prop]} → {curr_data[prop]}"
                    )

        if property_changes:
            summary.append(f"• Property changes: {', '.join(property_changes)}")

    # Check for interface differences
    expected_interface = (
        expected_tree.get("interface", {})
        .get("data", {})
        .get("items_tree", {})
        .get("data", {})
        .get("items", [])
    )
    current_interface = (
        current_tree.get("interface", {})
        .get("data", {})
        .get("items_tree", {})
        .get("data", {})
        .get("items", [])
    )

    if len(expected_interface) != len(current_interface):
        summary.append(
            f"• Interface socket count: expected {len(expected_interface)}, got {len(current_interface)}"
        )

    # Check for interface property changes
    if len(expected_interface) == len(current_interface):
        interface_changes = []
        for i, (exp_sock, curr_sock) in enumerate(
            zip(expected_interface, current_interface)
        ):
            exp_data = exp_sock.get("data", {})
            curr_data = curr_sock.get("data", {})

            if exp_data.get("default_value") != curr_data.get("default_value"):
                sock_name = curr_data.get("name", f"Interface Socket {i}")
                exp_val = exp_data.get("default_value")
                curr_val = curr_data.get("default_value")
                interface_changes.append(f"{sock_name}: {exp_val} → {curr_val}")

        if interface_changes:
            summary.append(f"• Interface changes: {', '.join(interface_changes)}")

    # If no specific differences found, show generic message
    if len(summary) == 1:  # Only has tree name
        summary.append("• Tree structure differs (run with -vv for full details)")

    return "\n".join(summary)


def _decompress_tree_data(compressed_data: str) -> dict:
    """Decompress tree clipper data and return as dict."""
    if not compressed_data.startswith(MAGIC_STRING):
        raise ValueError("Data does not appear to be compressed tree clipper format")

    # Remove magic string prefix
    base64_data = compressed_data[len(MAGIC_STRING) :]

    # Decode base64 and decompress
    gzipped = base64.b64decode(base64_data.encode("utf-8"))
    json_str = gzip.decompress(gzipped).decode("utf-8")

    return json.loads(json_str)


class TreeBuilderSnapshotExtension(AmberSnapshotExtension):
    """Syrupy extension for TreeBuilder snapshots with custom comparison."""

    _file_extension = "tree"

    def serialize(self, data: SerializableData, **kwargs) -> SerializedData:
        """Serialize TreeBuilder to compressed JSON string."""
        if not isinstance(data, TreeBuilder):
            raise TypeError(
                f"TreeBuilderSnapshotExtension can only serialize TreeBuilder instances, got {type(data)}"
            )

        return _serialize_tree_builder(data)

    def matches(
        self, *, serialized_data: SerializedData, snapshot_data: SerializedData
    ) -> bool:
        """Custom comparison logic that decompresses and uses jsondiff."""
        try:
            # Both should be compressed tree clipper data
            current_data = _decompress_tree_data(str(serialized_data))
            expected_data = _decompress_tree_data(str(snapshot_data))

            # Simple equality check first
            if current_data == expected_data:
                return True

            # If different, try to provide helpful comparison
            try:
                # Use jsondiff for detailed comparison
                differences = diff(expected_data, current_data, syntax="symmetric")
                print("\nTree snapshot differences detected:")
                print(
                    f"Key differences:\n{_format_key_differences(differences, expected_data, current_data)}"
                )
            except Exception as diff_error:
                # Fallback to high-level summary if jsondiff fails
                print(
                    f"\nTree snapshot differences detected (jsondiff failed: {diff_error}):"
                )
                print(
                    f"Expected tree name: {expected_data.get('node_trees', [{}])[0].get('data', {}).get('name', 'Unknown')}"
                )
                print(
                    f"Actual tree name: {current_data.get('node_trees', [{}])[0].get('data', {}).get('name', 'Unknown')}"
                )
                print("Run test with --tb=long for full details")

            return False

        except Exception as e:
            print(f"\nError comparing tree snapshots: {e}")
            import traceback

            traceback.print_exc()
            return False
