# Function reference

## Interface

|  |  |
|----|----|
| [builder.tree](../reference/builder.tree.llms.md#nodebpy.builder.tree) |  |
| [builder.socket](../reference/builder.socket.llms.md#nodebpy.builder.socket) | Typed Python wrappers around Blender node sockets. |
| [builder.node](../reference/builder.node.llms.md#nodebpy.builder.node) |  |
| [builder.accessor](../reference/builder.accessor.llms.md#nodebpy.builder.accessor) |  |
| [TreeBuilder](../reference/TreeBuilder.llms.md#nodebpy.TreeBuilder) | Builder for creating Blender node trees with a clean Python API. |
| [builder.BaseNode](../reference/builder.BaseNode.llms.md#nodebpy.builder.BaseNode) | Base class for all node wrappers. |

## Arrangement

Automatic node layout and its options.

|  |  |
|----|----|
| [arrange](../reference/arrange.llms.md#nodebpy.arrange) | Arrange the nodes of a tree. |
| [SugiyamaOptions](../reference/SugiyamaOptions.llms.md#nodebpy.SugiyamaOptions) | Options for the Sugiyama (layered) arrangement. |
| [SimpleOptions](../reference/SimpleOptions.llms.md#nodebpy.SimpleOptions) | Options for the simple column-based arrangement. |
| [default_sugiyama_options](../reference/default_sugiyama_options.llms.md#nodebpy.default_sugiyama_options) | Scope in which `arrange(tree, "sugiyama")` — and therefore every |

## Assets

Generating classes from pre-build assets

|  |  |
|----|----|
| [assets.generate_asset_api](../reference/assets.generate_asset_api.llms.md#nodebpy.assets.generate_asset_api) | Generate typed asset classes for `libraries` into `output_path`. |
| [assets.generate_asset_modules](../reference/assets.generate_asset_modules.llms.md#nodebpy.assets.generate_asset_modules) | Generate typed asset classes for `libraries`, split into one module per |
| [assets.dump_library](../reference/assets.dump_library.llms.md#nodebpy.assets.dump_library) | Dump every node-group and material asset in `blend_path` to Python |
| [assets.build_library](../reference/assets.build_library.llms.md#nodebpy.assets.build_library) | Rebuild a `.blend` asset library from sources written by |
| [assets.plot_library](../reference/assets.plot_library.llms.md#nodebpy.assets.plot_library) | Render node groups from `blend_path` to PNG images under |
| [assets.AssetLibrary](../reference/assets.AssetLibrary.llms.md#nodebpy.assets.AssetLibrary) | Locates a `.blend` asset library on disk at runtime. |
| [assets.BundledLibrary](../reference/assets.BundledLibrary.llms.md#nodebpy.assets.BundledLibrary) | A node-group asset library shipped with Blender itself, under the system |
| [assets.PackageLibrary](../reference/assets.PackageLibrary.llms.md#nodebpy.assets.PackageLibrary) | A `.blend` shipped inside a Python package, located relative to a module |

## Export

Exporting node trees to code.

|  |  |
|----|----|
| [export.to_python](../reference/export.to_python.llms.md#nodebpy.export.to_python) | Generate Python code that recreates the given node tree using nodebpy. |
| [export.to_mermaid](../reference/export.to_mermaid.llms.md#nodebpy.export.to_mermaid) | Generate a Mermaid diagram string from a node tree. |
| [export.to_plot](../reference/export.to_plot.llms.md#nodebpy.export.to_plot) | Draw the tree’s current layout to an image file. |
| [export.serialize_library](../reference/export.serialize_library.llms.md#nodebpy.export.serialize_library) | `tree_clipper` JSON data for each tree in `trees` (nested groups |
| [export.compare_libraries](../reference/export.compare_libraries.llms.md#nodebpy.export.compare_libraries) | Differences between two :func:`serialize_library` captures. |

## Geometry Nodes

Nodes use in Geometry Nodes trees.

|  |  |
|----|----|
| [nodes.geometry.input](../reference/nodes.geometry.input.llms.md#nodebpy.nodes.geometry.input) |  |
| [nodes.geometry.attribute](../reference/nodes.geometry.attribute.llms.md#nodebpy.nodes.geometry.attribute) |  |
| [nodes.geometry.color](../reference/nodes.geometry.color.llms.md#nodebpy.nodes.geometry.color) |  |
| [nodes.geometry.converter](../reference/nodes.geometry.converter.llms.md#nodebpy.nodes.geometry.converter) |  |
| [nodes.geometry.texture](../reference/nodes.geometry.texture.llms.md#nodebpy.nodes.geometry.texture) |  |
| [nodes.geometry.grid](../reference/nodes.geometry.grid.llms.md#nodebpy.nodes.geometry.grid) |  |
| [nodes.geometry.groups](../reference/nodes.geometry.groups.llms.md#nodebpy.nodes.geometry.groups) |  |
| [nodes.geometry.geometry](../reference/nodes.geometry.geometry.llms.md#nodebpy.nodes.geometry.geometry) |  |
| [nodes.geometry.attribute](../reference/nodes.geometry.attribute.llms.md#nodebpy.nodes.geometry.attribute) |  |
| [nodes.geometry.vector](../reference/nodes.geometry.vector.llms.md#nodebpy.nodes.geometry.vector) |  |
| [nodes.geometry.manual](../reference/nodes.geometry.manual.llms.md#nodebpy.nodes.geometry.manual) |  |
| [nodes.geometry.zone](../reference/nodes.geometry.zone.llms.md#nodebpy.nodes.geometry.zone) |  |

## Shader Nodes

Nodes use in Material / Shader node trees

|  |  |
|----|----|
| [nodes.shader.color](../reference/nodes.shader.color.llms.md#nodebpy.nodes.shader.color) |  |
| [nodes.shader.converter](../reference/nodes.shader.converter.llms.md#nodebpy.nodes.shader.converter) |  |
| [nodes.shader.grid](../reference/nodes.shader.grid.llms.md#nodebpy.nodes.shader.grid) |  |
| [nodes.shader.group](../reference/nodes.shader.group.llms.md#nodebpy.nodes.shader.group) |  |
| [nodes.shader.input](../reference/nodes.shader.input.llms.md#nodebpy.nodes.shader.input) |  |
| [nodes.shader.manual](../reference/nodes.shader.manual.llms.md#nodebpy.nodes.shader.manual) |  |
| [nodes.shader.output](../reference/nodes.shader.output.llms.md#nodebpy.nodes.shader.output) |  |
| [nodes.shader.script](../reference/nodes.shader.script.llms.md#nodebpy.nodes.shader.script) |  |
| [nodes.shader.shader](../reference/nodes.shader.shader.llms.md#nodebpy.nodes.shader.shader) |  |
| [nodes.shader.texture](../reference/nodes.shader.texture.llms.md#nodebpy.nodes.shader.texture) |  |
| [nodes.shader.vector](../reference/nodes.shader.vector.llms.md#nodebpy.nodes.shader.vector) |  |

## Compositor Nodes

Nodes for use in the compositor

|  |  |
|----|----|
| [nodes.compositor.color](../reference/nodes.compositor.color.llms.md#nodebpy.nodes.compositor.color) |  |
| [nodes.compositor.converter](../reference/nodes.compositor.converter.llms.md#nodebpy.nodes.compositor.converter) |  |
| [nodes.compositor.distort](../reference/nodes.compositor.distort.llms.md#nodebpy.nodes.compositor.distort) |  |
| [nodes.compositor.filter](../reference/nodes.compositor.filter.llms.md#nodebpy.nodes.compositor.filter) |  |
| [nodes.compositor.group](../reference/nodes.compositor.group.llms.md#nodebpy.nodes.compositor.group) |  |
| [nodes.compositor.input](../reference/nodes.compositor.input.llms.md#nodebpy.nodes.compositor.input) |  |
| [nodes.compositor.interface](../reference/nodes.compositor.interface.llms.md#nodebpy.nodes.compositor.interface) |  |
| [nodes.compositor.manual](../reference/nodes.compositor.manual.llms.md#nodebpy.nodes.compositor.manual) |  |
| [nodes.compositor.matte](../reference/nodes.compositor.matte.llms.md#nodebpy.nodes.compositor.matte) |  |
| [nodes.compositor.output](../reference/nodes.compositor.output.llms.md#nodebpy.nodes.compositor.output) |  |
| [nodes.compositor.vector](../reference/nodes.compositor.vector.llms.md#nodebpy.nodes.compositor.vector) |  |
