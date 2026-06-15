"""Entry point: ``python -m gen`` regenerates the node classes.

``python -m gen`` regenerates every tree type; ``python -m gen --only geometry``
regenerates a single tree for faster iteration (geometry is always processed
first because the shader/compositor trees re-export shared nodes from it).
"""

from __future__ import annotations

import argparse

from .config import ALL_CONFIGS, GEOMETRY_CONFIG, Disposition, TreeTypeConfig
from .introspect import get_node_names, introspect_node, probe_node_tree_compatibility
from .model import NodeInfo
from .writers import ModulesHandler

_Registry = dict[str, tuple[str, str, NodeInfo]]


def _probe_compatibility(all_nodes: list[type]) -> dict[str, list[str]]:
    """Map each node's bl_idname to the tree types it can be added to."""
    print("\n--- Probing node tree compatibility ---")
    node_compatibility: dict[str, list[str]] = {}
    for node_type in all_nodes:
        compatible = probe_node_tree_compatibility(node_type)
        if compatible:
            node_compatibility[node_type.__name__] = compatible

    multi_tree = {n: t for n, t in node_compatibility.items() if len(t) > 1}
    if multi_tree:
        print(f"\nNodes compatible with multiple tree types ({len(multi_tree)}):")
        for name, trees in sorted(multi_tree.items()):
            print(f"  {name}: {', '.join(t.replace('NodeTree', '') for t in trees)}")
    return node_compatibility


def _generate_tree(
    config: TreeTypeConfig,
    all_nodes: list[type],
    node_compatibility: dict[str, list[str]],
    gn_registry: _Registry | None,
    *,
    write: bool,
) -> ModulesHandler:
    """Introspect every generatable node for one tree type into a handler,
    optionally writing the module files."""
    print(f"\n{'=' * 60}")
    print(f"Generating {config.output_dir_name} nodes ({config.tree_type})")
    print(f"{'=' * 60}")

    handler = ModulesHandler(config, gn_registry=gn_registry or None)
    skipped = 0
    for node_type in all_nodes:
        if config.tree_type not in node_compatibility.get(node_type.__name__, []):
            continue
        if config.disposition(node_type) is not Disposition.GENERATE:
            print(f"  Skipping: {node_type.__name__}")
            skipped += 1
            continue
        node_info = introspect_node(node_type, config.tree_type)
        if node_info:
            node_info.tree_types = node_compatibility.get(node_type.__name__, [])
        handler.add_node(node_info)

    print(f"Successfully introspected {handler.count_nodes()} nodes")
    print(f"Skipped {skipped} nodes")
    if write:
        handler.write()
        print(f"Generated {len(handler.modules)} module files:")
        for filename in sorted(handler.modules.keys()):
            print(f"  - {filename}")
    return handler


def generate_all(only: set[str] | None = None):
    """Generate node classes and write them to ``src/nodebpy/nodes``.

    ``only`` restricts which tree types are *written* (by output dir name, e.g.
    ``{"geometry"}``); geometry is still processed when another tree is
    requested, since the others re-export shared geometry nodes.
    """
    all_nodes = get_node_names()
    print(f"Found {len(all_nodes)} total node types in bpy.types")
    node_compatibility = _probe_compatibility(all_nodes)

    needs_geometry_registry = only is not None and only != {"geometry"}
    gn_registry: _Registry = {}
    for config in ALL_CONFIGS:
        is_geometry = config is GEOMETRY_CONFIG
        write = only is None or config.output_dir_name in only
        if not write and not (is_geometry and needs_geometry_registry):
            continue
        handler = _generate_tree(
            config, all_nodes, node_compatibility, gn_registry, write=write
        )
        if is_geometry:
            gn_registry = handler.build_registry(all_nodes)
            print(f"Built geometry registry with {len(gn_registry)} class names")

    print("\n--- Generation complete! ---")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate nodebpy node classes.")
    parser.add_argument(
        "--only",
        action="append",
        choices=[c.output_dir_name for c in ALL_CONFIGS],
        help="Only write this tree type (repeatable). Defaults to all.",
    )
    args = parser.parse_args()
    generate_all(only=set(args.only) if args.only else None)


if __name__ == "__main__":
    main()
