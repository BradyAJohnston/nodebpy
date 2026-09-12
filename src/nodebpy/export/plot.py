"""Render a node tree's layout to an image, headlessly.

Blender can only draw node editors with a UI, so arrangement results are
invisible under the headless ``bpy`` module. ``to_plot`` draws the real
geometry the arranger works with — node rectangles at their locations with
estimated dimensions, links anchored to estimated socket positions — so a
layout can be inspected (or archived by tests) without opening Blender.

Requires ``matplotlib`` (``pip install nodebpy[plot]``).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import bpy

from ..builder.layout import calculate_node_dimensions, calculate_socket_offset_y

if TYPE_CHECKING:
    from matplotlib.axes import Axes

_NODE_FACE = "#dbe5f1"
_NODE_EDGE = "#5b7699"
_HIDDEN_FACE = "#ececec"
_HIDDEN_EDGE = "#8a8a8a"
_IO_FACE = "#d9eed2"
_IO_EDGE = "#6d9460"
_LINK_COLOR = "#555555"
_FRAME_EDGE = "#b08a3e"
_REROUTE_COLOR = "#444444"

_FRAME_PADDING = 30.0


def _abs_location(node: bpy.types.Node) -> tuple[float, float]:
    x, y = node.location
    parent = node.parent
    while parent is not None:
        x += parent.location.x
        y += parent.location.y
        parent = parent.parent
    return x, y


def _socket_anchor(socket: bpy.types.NodeSocket) -> tuple[float, float]:
    node = socket.node
    assert node is not None
    x, top = _abs_location(node)
    if node.bl_idname == "NodeReroute":
        return x, top
    width = calculate_node_dimensions(node)[0]
    anchor_x = x + width if socket.is_output else x
    return anchor_x, top + calculate_socket_offset_y(socket)


def _draw_link(ax: Axes, link: bpy.types.NodeLink) -> None:
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MplPath

    assert link.from_socket is not None and link.to_socket is not None
    x1, y1 = _socket_anchor(link.from_socket)
    x2, y2 = _socket_anchor(link.to_socket)
    bulge = min(abs(x2 - x1) * 0.5, 80.0)
    path = MplPath(
        [(x1, y1), (x1 + bulge, y1), (x2 - bulge, y2), (x2, y2)],
        [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4],
    )
    ax.add_patch(
        PathPatch(path, facecolor="none", edgecolor=_LINK_COLOR, lw=0.8, alpha=0.65)
    )
    ax.plot([x1, x2], [y1, y2], ".", color=_REROUTE_COLOR, ms=2.2, alpha=0.8)


def _draw_node(ax: Axes, node: bpy.types.Node) -> None:
    from matplotlib.patches import FancyBboxPatch, Rectangle

    x, top = _abs_location(node)

    if node.bl_idname == "NodeReroute":
        ax.plot([x], [top], "o", color=_REROUTE_COLOR, ms=4)
        return

    width, height = calculate_node_dimensions(node)
    if node.bl_idname in ("NodeGroupInput", "NodeGroupOutput"):
        face, edge = _IO_FACE, _IO_EDGE
    elif node.hide:
        face, edge = _HIDDEN_FACE, _HIDDEN_EDGE
    else:
        face, edge = _NODE_FACE, _NODE_EDGE

    patch: Any
    if node.hide:
        patch = FancyBboxPatch(
            (x, top - height),
            width,
            height,
            # Rounded rectangle, not a pill: a fixed corner radius well
            # under half the collapsed height.
            boxstyle=f"round,pad=0,rounding_size={min(6.0, height / 3)}",
            facecolor=face,
            edgecolor=edge,
            lw=0.9,
        )
        label_y = top - height / 2
        va = "center"
    else:
        patch = Rectangle(
            (x, top - height),
            width,
            height,
            facecolor=face,
            edgecolor=edge,
            lw=0.9,
        )
        label_y = top - 10
        va = "center"

    ax.add_patch(patch)
    if not node.hide:
        # header strip, over the body
        ax.add_patch(
            Rectangle((x, top - 20), width, 20, facecolor=edge, edgecolor="none")
        )
    label_color = "white" if not node.hide else "#333333"
    ax.text(
        x + width / 2,
        label_y,
        node.name,
        ha="center",
        va=va,
        fontsize=5,
        color=label_color,
        clip_on=True,
    )


def _draw_frames(ax: Axes, tree: bpy.types.NodeTree) -> None:
    from matplotlib.patches import Rectangle

    for frame in tree.nodes:
        if frame.bl_idname != "NodeFrame":
            continue
        children = [n for n in tree.nodes if n.parent == frame]
        if not children:
            continue
        corners = []
        for child in children:
            cx, ctop = _abs_location(child)
            w, h = (
                (8.0, 8.0)
                if child.bl_idname == "NodeReroute"
                else calculate_node_dimensions(child)
            )
            corners.append((cx, ctop - h, cx + w, ctop))
        x0 = min(c[0] for c in corners) - _FRAME_PADDING
        y0 = min(c[1] for c in corners) - _FRAME_PADDING
        x1 = max(c[2] for c in corners) + _FRAME_PADDING
        y1 = max(c[3] for c in corners) + _FRAME_PADDING
        ax.add_patch(
            Rectangle(
                (x0, y0),
                x1 - x0,
                y1 - y0,
                facecolor="none",
                edgecolor=_FRAME_EDGE,
                lw=1.0,
                linestyle="--",
            )
        )
        ax.text(
            x0 + 4,
            y1 + 6,
            frame.label or frame.name,
            fontsize=6,
            color=_FRAME_EDGE,
        )


def to_plot(
    tree: bpy.types.NodeTree,
    filepath: str | Path,
    *,
    title: str | None = None,
    dpi: int = 150,
) -> Path:
    """Draw the tree's current layout to an image file.

    Nodes are rectangles at their real locations with the same estimated
    dimensions the arranger uses; links are curves between estimated socket
    positions, so what you see is what the layout algorithm saw.
    """
    try:
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
    except ImportError as e:
        raise ImportError(
            "matplotlib is required for to_plot: pip install nodebpy[plot]"
        ) from e

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fig = Figure(figsize=(12, 8))
    FigureCanvasAgg(fig)
    ax = fig.add_subplot()

    _draw_frames(ax, tree)
    for link in tree.links:
        _draw_link(ax, link)
    for node in tree.nodes:
        if node.bl_idname != "NodeFrame":
            _draw_node(ax, node)

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.margins(0.05)
    ax.set_title(
        title or f"{tree.name}  ({len(tree.nodes)} nodes, {len(tree.links)} links)",
        fontsize=9,
    )
    ax.tick_params(labelsize=6)
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
    return filepath
