"""Deep round-trip parity checking, via ``tree_clipper``'s full JSON
serialization of node trees.

:func:`serialize_library` captures every given tree (and its nested groups)
as id-free JSON data; :func:`compare_libraries` diffs two such captures and
returns the differences as :class:`ParityFinding` records. Because a rebuild
legitimately renames nodes, node properties are compared as value-multisets
per ``(bl_idname, property path)`` within each tree rather than node-by-node.

What counts as a difference is configurable through *surfaces* passed to
``ignore``:

- ``"positions"`` — node locations (only meaningful to keep when the dump ran
  with ``snapshot_positions``);
- ``"presentation"`` — node width/height/labels/collapse state, custom
  colors, frames, socket visibility;
- ``"reroutes"`` — reroute nodes and the links that touch them (they only
  round-trip with ``keep_reroutes``).

Always ignored: UI state (selection, expansion), node names, id-based
references, and stale ``default_value``\\ s on *linked* sockets (the link
wins at evaluation; the value is an inert authoring leftover).

The CLI compares two ``.blend`` asset libraries::

    python -m nodebpy.export.parity original.blend rebuilt.blend \\
        --ignore positions reroutes presentation

Requires the optional ``tree_clipper`` package.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Collection, Iterable
from dataclasses import dataclass
from typing import Any

SURFACES = frozenset({"positions", "presentation", "reroutes"})

_ALWAYS_SKIP_NODE_KEYS = {
    "name",
    "select",
    "id",
    "location_absolute",
    "active_index",
    "active_input_index",
    "active_output_index",
}
# id-based references; the raw integers depend on serialization order.
_REF_KEYS = {
    "node_tree",
    "parent",
    "single_input",
    "single_output",
    "paired_output",
    "active_item",
}
_SKIP_IFACE_KEYS = {"id", "select"}
_SKIP_SOCKET_KEYS = {"id", "name", "show_expanded", "is_inactive"}
# Storage/session bookkeeping, not tree content.
_SKIP_TREE_KEYS = {"use_fake_user", "use_extra_user", "tag", "is_runtime_data"}
_POSITION_KEYS = {"location"}
_PRESENTATION_NODE_KEYS = {
    "width",
    "height",
    "label",
    "hide",
    "show_options",
    "show_preview",
    "show_texture",
    "use_custom_color",
    "color",
    "panel_states",
    "parent",  # frame membership
}
_PRESENTATION_SOCKET_KEYS = {"hide", "display_shape"}
# Group in/out nodes mirror interface defaults onto their sockets; the
# interface itself is compared directly, so the copies are pure noise.
_GROUP_IO = {"NodeGroupInput", "NodeGroupOutput"}


@dataclass
class ParityFinding:
    """One difference between the two captures."""

    tree: str
    context: str  # "tree" | "interface" | "node" | "links"
    path: str
    detail: str

    def __str__(self) -> str:  # pragma: no cover - convenience
        return f"{self.tree}: [{self.context}] {self.path} — {self.detail}"


def serialize_library(trees: Iterable[Any]) -> dict[str, dict]:
    """``tree_clipper`` JSON data for each tree in ``trees`` (nested groups
    included), keyed by tree name. The trees must be in the current session:
    the capture is enriched from the live data with what the JSON alone
    can't express — each socket's ``is_inactive`` flag (codegen's criterion
    for evaluation-inert links) and datablock references resolved to names
    instead of serialization-order ids."""
    import bpy

    from ..builder import TreeBuilder
    from .web_render import to_tree_clipper_payload

    out: dict[str, dict] = {}
    for tree in trees:
        payload = json.loads(to_tree_clipper_payload(TreeBuilder(tree), compress=False))
        external = {
            int(key): f"<{value.get('fixed_type_name')}:{value.get('description')}>"
            for key, value in payload.get("external", {}).items()
        }
        for entry in payload.get("node_trees", []):
            data = entry["data"]
            live = bpy.data.node_groups.get(data["name"])
            if live is None and tree.name == data["name"]:
                live = tree
            _enrich_tree(data, live, external)
            out.setdefault(data["name"], data)
    return out


_DATABLOCK_SOCKET_TYPES = {
    "OBJECT",
    "COLLECTION",
    "IMAGE",
    "MATERIAL",
    "TEXTURE",
    "FONT",
    "SOUND",
    "MASK",
    "SCENE",
}
_DATABLOCK_IFACE_TYPES = {
    "NodeSocketObject",
    "NodeSocketCollection",
    "NodeSocketImage",
    "NodeSocketMaterial",
    "NodeSocketTexture",
    "NodeSocketFont",
    "NodeSocketSound",
    "NodeSocketMask",
    "NodeSocketScene",
}


def _enrich_tree(data: dict, live: Any, external: dict[int, str]) -> None:
    for node_entry in _collection_items(data.get("nodes")):
        live_node = None
        if live is not None:
            live_node = live.nodes.get(node_entry.get("name", ""))
        for key in ("inputs", "outputs"):
            value = node_entry.get(key)
            if not isinstance(value, dict):
                continue
            live_sockets = list(getattr(live_node, key, ()) or ())
            for idx, item in enumerate(value["data"]["items"]):
                sdata = item["data"]
                if live_node is not None and idx < len(live_sockets):
                    sdata["is_inactive"] = getattr(
                        live_sockets[idx], "is_inactive", False
                    )
                default = sdata.get("default_value")
                if (
                    isinstance(default, int)
                    and sdata.get("type") in _DATABLOCK_SOCKET_TYPES
                ):
                    sdata["default_value"] = external.get(default, "<datablock>")
    interface = data.get("interface")
    if interface:
        for item in _collection_items(interface["data"]["items_tree"]):
            default = item.get("default_value")
            if (
                isinstance(default, int)
                and item.get("socket_type") in _DATABLOCK_IFACE_TYPES
            ):
                item["default_value"] = external.get(default, "<datablock>")


def _norm(value: Any) -> Any:
    """Hashable, id-free normal form of a JSON value."""
    if isinstance(value, dict):
        if set(value) == {"id", "data"}:
            return _norm(value["data"])
        if set(value) == {"id"}:
            return "<ref>"
        return tuple(sorted((k, _norm(v)) for k, v in value.items() if k != "id"))
    if isinstance(value, list):
        return tuple(_norm(v) for v in value)
    if isinstance(value, float):
        return round(value, 4)
    return value


def _collection_items(value: Any) -> list[dict]:
    if not value:
        return []
    if isinstance(value, dict):
        value = value["data"]["items"]
    return [item.get("data", item) for item in value]


def _linked_socket_ids(tree: dict) -> set[int]:
    linked: set[int] = set()
    for link in _collection_items(tree.get("links")):
        for key in ("from_socket", "to_socket"):
            ref = link.get(key)
            if isinstance(ref, dict):
                ref = ref.get("id")
            if isinstance(ref, int):
                linked.add(ref)
    return linked


def _node_socket_ids(node: dict) -> set[int]:
    ids: set[int] = set()
    for key in ("inputs", "outputs"):
        value = node.get(key)
        if isinstance(value, dict):
            ids.update(item["id"] for item in value["data"]["items"])
    return ids


def _node_paths(
    node: dict, linked: set[int], ignore: Collection[str]
) -> dict[str, Any]:
    """Flatten one node's data into ``{path: value}`` honouring the surfaces."""
    out: dict[str, Any] = {}
    skip_keys = set(_ALWAYS_SKIP_NODE_KEYS)
    skip_socket = set(_SKIP_SOCKET_KEYS)
    if "positions" in ignore:
        skip_keys |= _POSITION_KEYS
    if "presentation" in ignore:
        skip_keys |= _PRESENTATION_NODE_KEYS
        skip_socket |= _PRESENTATION_SOCKET_KEYS
    group_io = node.get("bl_idname") in _GROUP_IO
    for key, value in node.items():
        if key in skip_keys:
            continue
        if key in _REF_KEYS:
            out[key] = "<ref>" if value is not None else None
            continue
        if key in ("inputs", "outputs"):
            for idx, socket in enumerate(
                item
                for item in (
                    value["data"]["items"] if isinstance(value, dict) else value
                )
            ):
                sid = socket.get("id")
                sdata = socket.get("data", socket)
                sname = sdata.get("name", "")
                for skey, svalue in sdata.items():
                    if skey in skip_socket:
                        continue
                    if skey == "default_value" and (
                        key == "outputs"  # output values are residual storage
                        or sid in linked  # the link wins at evaluation
                        or group_io  # mirrors the interface, compared directly
                        or sdata.get("enabled") is False  # unavailable socket
                        or sdata.get("is_inactive")  # evaluation-inert socket
                        # A value equal to the node's fresh default carries no
                        # information — skipping it keeps the comparison
                        # symmetric when the other side's socket is linked or
                        # inactive (and therefore skipped).
                        or _is_fresh_default(node.get("bl_idname", ""), idx, svalue)
                    ):
                        continue
                    out[f"{key}[{idx}:{sname}].{skey}"] = _norm(svalue)
            continue
        out[key] = _norm(value)
    return out


def _fresh_input_defaults(bl_idname: str) -> tuple:
    """Normed ``default_value`` per input index of a freshly created node
    (cached), or ``()`` when the node can't be probed."""
    cached = _FRESH_DEFAULTS_CACHE.get(bl_idname)
    if cached is not None:
        return cached
    defaults: tuple = ()
    try:
        import bpy
    except ImportError:  # pragma: no cover - parity runs inside Blender
        bpy = None
    if bpy is not None:
        for tree_type in ("GeometryNodeTree", "CompositorNodeTree"):
            tree = bpy.data.node_groups.new("_parity_probe", tree_type)
            assert tree is not None
            try:
                try:
                    node = tree.nodes.new(bl_idname)
                except RuntimeError:
                    continue
                assert node is not None
                values = []
                for socket in node.inputs:
                    value = getattr(socket, "default_value", None)
                    if value is not None and not isinstance(
                        value, (bool, int, float, str)
                    ):
                        try:
                            value = tuple(value)
                        except TypeError:
                            value = None
                    values.append(_norm(value))
                defaults = tuple(values)
                break
            finally:
                bpy.data.node_groups.remove(tree)
    _FRESH_DEFAULTS_CACHE[bl_idname] = defaults
    return defaults


_FRESH_DEFAULTS_CACHE: dict[str, tuple] = {}


def _is_fresh_default(bl_idname: str, index: int, value: Any) -> bool:
    fresh = _fresh_input_defaults(bl_idname)
    return index < len(fresh) and _norm(value) == fresh[index]


def _compare_tree(
    name: str, a: dict, b: dict, ignore: Collection[str]
) -> list[ParityFinding]:
    findings: list[ParityFinding] = []

    # 1. Tree-level scalars.
    for key in sorted(set(a) | set(b)):
        if key in ("interface", "nodes", "links", "name") or key in _SKIP_TREE_KEYS:
            continue
        va, vb = _norm(a.get(key)), _norm(b.get(key))
        if va != vb:
            findings.append(ParityFinding(name, "tree", key, f"{va!r} -> {vb!r}"))

    # 2. Interface items, pairwise in order.
    def iface(tree: dict) -> list[dict]:
        node_iface = tree.get("interface")
        if not node_iface:
            return []
        return _collection_items(node_iface["data"]["items_tree"])

    ia, ib = iface(a), iface(b)
    if len(ia) != len(ib):
        findings.append(
            ParityFinding(name, "interface", "item count", f"{len(ia)} -> {len(ib)}")
        )
    else:
        for pa, pb in zip(ia, ib):
            for key in sorted(set(pa) | set(pb)):
                if key in _SKIP_IFACE_KEYS:
                    continue
                va, vb = _norm(pa.get(key)), _norm(pb.get(key))
                if va != vb:
                    findings.append(
                        ParityFinding(
                            name,
                            "interface",
                            f"{pa.get('name')}.{key}",
                            f"{va!r} -> {vb!r}",
                        )
                    )

    # 3. Node properties as value-multisets per (bl_idname, path).
    def node_multisets(tree: dict) -> dict[tuple[str, str], Counter]:
        linked = _linked_socket_ids(tree)
        per_type: dict[tuple[str, str], Counter] = defaultdict(Counter)
        for node in _collection_items(tree.get("nodes")):
            bl = node.get("bl_idname", "?")
            if "reroutes" in ignore and bl == "NodeReroute":
                continue
            if "presentation" in ignore and bl in ({"NodeFrame"} | _GROUP_IO):
                # Frames are pure layout; group-IO nodes are visual
                # instances of the interface, which is compared directly —
                # how many instances exist and what they mirror is
                # presentation.
                continue
            for path, value in _node_paths(node, linked, ignore).items():
                per_type[(bl, path)][value] += 1
        return per_type

    ma, mb = node_multisets(a), node_multisets(b)
    for key in sorted(set(ma) | set(mb)):
        ca, cb = ma.get(key, Counter()), mb.get(key, Counter())
        if ca == cb:
            continue
        bl, path = key
        lost = list((ca - cb).items())[:2]
        gained = list((cb - ca).items())[:2]
        findings.append(
            ParityFinding(
                name, "node", f"{bl}.{path}", f"lost {lost!r} gained {gained!r}"
            )
        )

    # 4. Link counts (endpoints are covered structurally by codegen tests;
    # the count catches whole links appearing or vanishing). With reroutes
    # ignored, links touching a reroute socket don't count.
    def link_count(tree: dict) -> int:
        # Muted links and links into disabled sockets are inert (Blender
        # keeps but ignores them; a rebuild drops them by design) and never
        # count. With reroutes ignored, links are counted by their
        # non-reroute destination only: A→reroute→B counts once (the
        # reroute→B hop), exactly like the collapsed direct A→B — so a
        # rebuild that dissolved the chain still matches, and dangling
        # reroute chains vanish from the count on both sides.
        # Links into or out of disabled/inactive sockets are inert: Blender
        # keeps but ignores them, and a rebuild drops them by design.
        # tree_clipper serializes reroute nodes without sockets, so a link
        # endpoint id that resolves to no known socket belongs to a reroute:
        # with reroutes ignored, count only links INTO known sockets —
        # A→reroute→B then counts once (the reroute→B hop), matching the
        # collapsed direct A→B.
        known: set[int] = set()
        inert: set[int] = set()
        for node in _collection_items(tree.get("nodes")):
            for key in ("inputs", "outputs"):
                value = node.get(key)
                if isinstance(value, dict):
                    for item in value["data"]["items"]:
                        known.add(item["id"])
                        sdata = item["data"]
                        if sdata.get("enabled") is False or sdata.get("is_inactive"):
                            inert.add(item["id"])
        count = 0
        for link in _collection_items(tree.get("links")):
            if link.get("is_muted"):
                continue
            ids = set()
            for lkey in ("from_socket", "to_socket"):
                ref = link.get(lkey)
                ids.add(ref.get("id") if isinstance(ref, dict) else ref)
            if ids & inert:
                continue
            to_ref = link.get("to_socket")
            to_id = to_ref.get("id") if isinstance(to_ref, dict) else to_ref
            if "reroutes" in ignore and to_id not in known:
                continue
            count += 1
        return count

    la, lb = link_count(a), link_count(b)
    if la != lb:
        findings.append(ParityFinding(name, "links", "count", f"{la} -> {lb}"))
    return findings


def compare_libraries(
    a: dict[str, dict],
    b: dict[str, dict],
    *,
    ignore: Collection[str] = frozenset(),
) -> list[ParityFinding]:
    """Differences between two :func:`serialize_library` captures.

    ``ignore`` selects the surfaces to exclude (see :data:`SURFACES`); an
    unknown surface name raises so a typo can't silently widen the check.
    """
    unknown = set(ignore) - SURFACES
    if unknown:
        raise ValueError(f"Unknown parity surfaces: {sorted(unknown)}")

    findings: list[ParityFinding] = []
    for name in sorted(set(a) - set(b)):
        findings.append(ParityFinding(name, "tree", "presence", "missing in second"))
    for name in sorted(set(b) - set(a)):
        findings.append(ParityFinding(name, "tree", "presence", "missing in first"))
    for name in sorted(set(a) & set(b)):
        findings.extend(_compare_tree(name, a[name], b[name], ignore))
    return findings


def format_report(findings: list[ParityFinding]) -> str:
    """Aggregate ``findings`` by (context, path) for a readable summary."""
    grouped: dict[tuple[str, str], list[ParityFinding]] = defaultdict(list)
    for finding in findings:
        grouped[(finding.context, finding.path)].append(finding)
    lines = [f"{len(findings)} findings in {len({f.tree for f in findings})} trees"]
    for (context, path), group in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
        first = group[0]
        lines.append(f"{len(group):>6}  [{context}] {path}")
        lines.append(f"        e.g. {first.detail}   (in: {first.tree})")
    return "\n".join(lines)


def _serialize_blend_assets(blend_path: str) -> dict[str, dict]:
    """Load a .blend's node-group assets, serialize them, and clean the
    session back up — including dependency datablocks, or the second blend's
    same-named materials/objects/collections would load renamed (".001") and
    show as spurious reference differences."""
    import bpy

    collections = ("node_groups", "materials", "images", "objects", "collections")
    before = {c: set(getattr(bpy.data, c).keys()) for c in collections}
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        blend_path, link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = list(src.node_groups)
    try:
        return serialize_library(list(dst.node_groups))
    finally:
        for collection in collections:
            data = getattr(bpy.data, collection)
            for datablock in [d for d in data if d.name not in before[collection]]:
                data.remove(datablock)


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI wrapper
    """Compare the node-group assets of two .blend files."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m nodebpy.export.parity",
        description=(
            "Deep-diff the node-group assets of two .blend files via "
            "tree_clipper serialization; exits non-zero when they differ "
            "on the selected surfaces."
        ),
    )
    parser.add_argument("first", help="The reference .blend (e.g. the original).")
    parser.add_argument("second", help="The .blend to compare (e.g. a rebuild).")
    parser.add_argument(
        "--ignore",
        nargs="+",
        default=(),
        choices=sorted(SURFACES),
        help="Surfaces to exclude from the comparison.",
    )
    args = parser.parse_args(argv)
    a = _serialize_blend_assets(args.first)
    b = _serialize_blend_assets(args.second)
    findings = compare_libraries(a, b, ignore=set(args.ignore))
    print(format_report(findings) if findings else "parity: no differences")
    return 1 if findings else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
