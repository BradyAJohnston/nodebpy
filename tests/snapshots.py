"""Custom syrupy snapshots for NodeBPY TreeBuilder class."""

import base64
import gzip
import json
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.types import SerializableData, SerializedData
from nodebpy import TreeBuilder
from tree_clipper.export_nodes import ExportIntermediate, ExportParameters
from tree_clipper.specific_handlers import BUILT_IN_EXPORTER
from tree_clipper.common import MAGIC_STRING
from jsondiff import diff


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

            # Use jsondiff for detailed comparison
            differences = diff(expected_data, current_data)

            if differences:
                # Format the differences for better error messages
                print("\nTree snapshot differences detected:")
                print(f"Differences: {json.dumps(differences, indent=2)}")
                return False

            return True

        except Exception as e:
            print(f"\nError comparing tree snapshots: {e}")
            return False
