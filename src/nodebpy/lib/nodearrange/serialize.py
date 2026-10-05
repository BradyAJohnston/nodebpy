# SPDX-License-Identifier: GPL-2.0-or-later
"""The layout's input and output as JSON.

A :class:`~.dna.bNodeTree`, the :class:`~.config.Settings` and the
:class:`~.arrange.edits.LayoutResult` written as plain lists and numbers,
nodes and sockets referred to by index. That makes a layout problem and its
answer a file: a corpus to test this implementation against, and the same
corpus to test a port in another language against this one.

A node is its index in ``tree.nodes``; a reroute the layout creates gets the
next free index, in the order the ``add_reroute`` edits appear. A socket is
``[node, is_output, index]``.
"""

from __future__ import annotations

from dataclasses import fields
from typing import Any

from .arrange.edits import (
    AddLink,
    AddReroute,
    Edit,
    LayoutResult,
    MoveNode,
    RemoveLink,
    RemoveNode,
    ResizeFrame,
    RestoreMultiInputOrder,
)
from .config import Settings
from .dna import bNode, bNodeSocket, bNodeTree, new_reroute

type Json = dict[str, Any]

FORMAT = 1

# -------------------------------------------------------------------
# Trees


def _pair(value: tuple[float, float] | None) -> list[float] | None:
    return None if value is None else [value[0], value[1]]


def tree_to_json(tree: bNodeTree) -> Json:
    index = {node: i for i, node in enumerate(tree.nodes)}
    nodes = []
    for node in tree.nodes:
        data: Json = {"name": node.name, "idname": node.idname}
        if node.label:
            data["label"] = node.label
        if node.parent is not None:
            data["parent"] = index[node.parent]
        if node.is_frame():
            data["label_size"] = node.label_size
            data["shrink"] = node.shrink
        else:
            data["location"] = _pair(node.location)
            data["width"] = node.width
            data["draw_bounds"] = list(node.draw_bounds)
            if node.is_collapsed:
                data["collapsed"] = True
            data["inputs"] = [
                [s.idname, int(s.is_multi_input), _pair(s.location)]
                for s in node.inputs
            ]
            data["outputs"] = [[s.idname, _pair(s.location)] for s in node.outputs]
        nodes.append(data)

    links = [
        [
            index[link.fromnode],
            link.fromsock.index,
            index[link.tonode],
            link.tosock.index,
            link.multi_input_sort_id,
            int(link.is_valid),
        ]
        for link in tree.links
    ]
    return {"format": FORMAT, "nodes": nodes, "links": links}


def tree_from_json(data: Json) -> bNodeTree:
    if data.get("format") != FORMAT:
        raise ValueError(f"unsupported tree format {data.get('format')!r}")

    tree = bNodeTree()
    for item in data["nodes"]:
        node = tree.add_node(
            bNode(
                name=item["name"],
                idname=item["idname"],
                label=item.get("label", ""),
                location=tuple(item.get("location", (0.0, 0.0))),
                width=item.get("width", 0.0),
                draw_bounds=tuple(item.get("draw_bounds", (0.0, 0.0, 0.0, 0.0))),
                is_collapsed=item.get("collapsed", False),
                label_size=item.get("label_size", 20),
                shrink=item.get("shrink", True),
            )
        )
        for idname, multi, location in item.get("inputs", ()):
            node.add_socket(
                False,
                is_multi_input=bool(multi),
                location=None if location is None else tuple(location),
                idname=idname,
            )
        for idname, location in item.get("outputs", ()):
            node.add_socket(
                True,
                location=None if location is None else tuple(location),
                idname=idname,
            )

    for node, item in zip(tree.nodes, data["nodes"]):
        if "parent" in item:
            node.parent = tree.nodes[item["parent"]]

    for from_node, from_index, to_node, to_index, sort_id, valid in data["links"]:
        link = tree.add_link(
            tree.nodes[from_node].outputs[from_index],
            tree.nodes[to_node].inputs[to_index],
            sort_id,
        )
        link.is_valid = bool(valid)

    return tree


# -------------------------------------------------------------------
# Settings


def settings_to_json(settings: Settings) -> Json:
    """Only the fields that differ from the defaults."""
    default = Settings()
    return {
        f.name: getattr(settings, f.name)
        for f in fields(Settings)
        if getattr(settings, f.name) != getattr(default, f.name)
    }


def settings_from_json(data: Json) -> Settings:
    return Settings(**data)


# -------------------------------------------------------------------
# Results


def result_to_json(tree: bNodeTree, result: LayoutResult) -> Json:
    """*result* (a layout of *tree*) as a list of edits."""
    index = {node: i for i, node in enumerate(tree.nodes)}

    def node_ref(node: bNode | None) -> int | None:
        return None if node is None else index[node]

    def socket_ref(socket: bNodeSocket | None) -> list[int]:
        assert socket is not None
        return [index[socket.node], int(socket.is_output), socket.index]

    edits: list[list[Any]] = []
    for edit in result.edits:
        match edit:
            case RemoveNode(node=node):
                edits.append(["remove_node", index[node]])
            case AddReroute(node=node):
                index[node] = len(index)
                edits.append(["add_reroute", index[node], node_ref(node.parent)])
            case AddLink(fromsock=fromsock, tosock=tosock):
                edits.append(["add_link", socket_ref(fromsock), socket_ref(tosock)])
            case RemoveLink(fromsock=fromsock, tosock=tosock):
                edits.append(["remove_link", socket_ref(fromsock), socket_ref(tosock)])
            case RestoreMultiInputOrder(socket=socket, outputs=outputs, order=order):
                edits.append(
                    [
                        "multi_input_order",
                        socket_ref(socket),
                        [socket_ref(s) for s in outputs],
                        [[socket_ref(s), sort_id] for s, sort_id in order],
                    ]
                )
            case MoveNode(node=node, top_left=(x, y), parent=parent):
                edits.append(["move", index[node], x, y, node_ref(parent)])
            case ResizeFrame(frame=frame, children=children):
                edits.append(
                    ["resize_frame", index[frame], [index[c] for c in children]]
                )
    return {"format": FORMAT, "edits": edits}


def result_from_json(tree: bNodeTree, data: Json) -> LayoutResult:
    """The edits of *data*, referring to the nodes of *tree*."""
    if data.get("format") != FORMAT:
        raise ValueError(f"unsupported result format {data.get('format')!r}")

    nodes: list[bNode] = list(tree.nodes)

    def node_at(ref: int | None) -> bNode | None:
        return None if ref is None else nodes[ref]

    def socket_at(ref: list[int]) -> bNodeSocket:
        node, is_output, i = ref
        return (nodes[node].outputs if is_output else nodes[node].inputs)[i]

    edits: list[Edit] = []
    for kind, *args in data["edits"]:
        match kind:
            case "remove_node":
                edits.append(RemoveNode(nodes[args[0]]))
            case "add_reroute":
                assert args[0] == len(nodes)
                nodes.append(new_reroute(node_at(args[1])))
                edits.append(AddReroute(nodes[-1]))
            case "add_link":
                edits.append(AddLink(socket_at(args[0]), socket_at(args[1])))
            case "remove_link":
                edits.append(RemoveLink(socket_at(args[0]), socket_at(args[1])))
            case "multi_input_order":
                edits.append(
                    RestoreMultiInputOrder(
                        socket_at(args[0]),
                        tuple(socket_at(s) for s in args[1]),
                        tuple((socket_at(s), sort_id) for s, sort_id in args[2]),
                    )
                )
            case "move":
                edits.append(
                    MoveNode(nodes[args[0]], (args[1], args[2]), node_at(args[3]))
                )
            case "resize_frame":
                edits.append(
                    ResizeFrame(nodes[args[0]], tuple(nodes[c] for c in args[1]))
                )
            case _:
                raise ValueError(f"unknown edit {kind!r}")
    return LayoutResult(edits)
