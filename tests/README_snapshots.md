# TreeBuilder Snapshots

This directory contains a custom syrupy snapshot extension for testing TreeBuilder instances.

## How it works

The `TreeBuilderSnapshotExtension` provides:

1. **Compressed storage**: Trees are serialized using tree_clipper with `compress=True`, creating compact snapshots
2. **Intelligent comparison**: When snapshots differ, the extension decompresses both versions and uses `jsondiff` to provide detailed, informative error messages about what changed
3. **Tree-specific format**: Uses `.tree` file extension and tree_clipper's magic string format

## Usage

```python
def test_my_tree(snapshot_tree):
    """Test that demonstrates tree snapshot usage."""
    with TreeBuilder("MyTree") as tree:
        # Set up interface
        geom_in = sockets.SocketGeometry("Geometry") 
        geom_out = sockets.SocketGeometry("Geometry")
        tree.interface(inputs=[geom_in], outputs=[geom_out])
        
        # Create and connect nodes
        set_pos = nodes.SetPosition()
        tree.inputs.geometry >> set_pos >> tree.outputs.geometry
        
        # Set properties
        set_pos.node.inputs["Offset"].default_value = (1.0, 2.0, 3.0)
        
    # This creates/compares a snapshot of the entire tree structure
    assert snapshot_tree == tree
```

## What gets captured

The snapshot captures the complete node tree structure including:

- All nodes and their types
- All node properties and their values  
- All links between nodes
- Interface sockets (inputs/outputs)
- Node positions and other metadata
- Sub-trees and node groups

## Benefits over regular snapshots

1. **Compact storage**: Compressed format saves disk space
2. **Tree-aware comparison**: jsondiff shows exactly which nodes, properties, or links changed
3. **Version control friendly**: Text-based format works well with git
4. **Semantic understanding**: Diffs show meaningful tree structure changes rather than raw JSON

## Error example

When a tree changes, you'll see detailed output like:

```
Tree snapshot differences detected:
Differences: {
  "trees": {
    "$insert": [
      {
        "id": 15,
        "data": {
          "nodes": {
            "items": {
              "$insert": [
                {
                  "id": 12,
                  "data": {
                    "bl_idname": "GeometryNodeSetPosition",
                    "inputs": {
                      "items": [
                        {
                          "data": {
                            "default_value": [1.0, 2.0, 3.0]
                          }
                        }
                      ]
                    }
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

This shows exactly what node was added and what its properties are.