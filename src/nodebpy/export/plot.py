"""Render a node tree to an image, headlessly, styled like Blender's editor.

Blender can only draw node editors with a UI, so under the headless ``bpy``
module a tree is invisible. :func:`to_plot` reproduces what the node editor
would show — header colours per node class, socket markers coloured and
shaped by type, value widgets for unlinked inputs, property dropdowns,
frames, zones and socket-coloured links — from the same estimated geometry
the arranger works with (:mod:`nodebpy.builder.layout`), so a tree can be
reviewed without opening Blender. :func:`to_node_plot` draws a node group
the way it appears when *used*: as a single group node with its interface
sockets and default values.

Colours are read from Blender's active theme where possible, so a render
follows the user's preferences; the shipped defaults match Blender's dark
theme.

Requires ``matplotlib`` (``pip install nodebpy[plot]``).
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import bpy

from ..builder.layout import (
    HEADER,
    PROPERTY_ROW,
    VECTOR_EXPANDED,
    NodeRow,
    calculate_node_dimensions,
    calculate_socket_offset_y,
    node_rows,
)

if TYPE_CHECKING:
    from matplotlib.axes import Axes

# --------------------------------------------------------------------------
# Geometry (Blender UI units at 1.0 scale; 1 unit is drawn as 1 pt)
# --------------------------------------------------------------------------

#: Drawing scale: UI units per inch. One unit maps to one typographic point,
#: so an 11-unit Blender label is an 11 pt matplotlib label.
UNITS_PER_INCH = 72.0
_MARGIN = 40.0
_GRID = 20.0
_MAX_PIXELS = 16_000

_TEXT_SIZE = 11.0
_NODE_RADIUS = 5.0
_SOCKET_RADIUS = 5.0
_WIDGET_HEIGHT = 18.0
_WIDGET_INSET = 10.0  # from the node edge to a widget's edge
_LABEL_INSET = 12.0  # from the node edge to a socket label
_LINK_WIDTH = 2.6
_FRAME_PADDING = 30.0
_ZONE_PADDING = 22.0

# --------------------------------------------------------------------------
# Theme
# --------------------------------------------------------------------------

Color = tuple[float, float, float, float]


def _rgba(value: Any, alpha: float | None = None) -> Color:
    r, g, b = (float(c) for c in tuple(value)[:3])
    a = alpha if alpha is not None else (float(value[3]) if len(value) > 3 else 1.0)
    return (r, g, b, a)


def _hex(value: str, alpha: float = 1.0) -> Color:
    value = value.lstrip("#")
    r, g, b = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, alpha)


# Blender's default dark theme, used when the live theme lacks an entry.
_DEFAULT_HEADERS = {
    "ATTRIBUTE": "#1d2546",
    "COLOR": "#6e6e23",
    "CONVERTER": "#246283",
    "DISTORT": "#3e5a5b",
    "FILTER": "#412b51",
    "GEOMETRY": "#1d725e",
    "INPUT": "#83354c",
    "MATTE": "#5a3838",
    "OUTPUT": "#3e232a",
    "SCRIPT": "#203c3c",
    "SHADER": "#2b652b",
    "TEXTURE": "#794619",
    "VECTOR": "#3c3c83",
    "PATTERN": "#3c3c83",
    "INTERFACE": "#1d1d1d",
    "GROUP": "#374725",
    "NONE": "#303030",
}
_THEME_HEADER_ATTR = {
    "ATTRIBUTE": "attribute_node",
    "COLOR": "color_node",
    "CONVERTER": "converter_node",
    "DISTORT": "distor_node",
    "FILTER": "filter_node",
    "GEOMETRY": "geometry_node",
    "INPUT": "input_node",
    "MATTE": "matte_node",
    "OUTPUT": "output_node",
    "SCRIPT": "script_node",
    "SHADER": "shader_node",
    "TEXTURE": "texture_node",
    "VECTOR": "vector_node",
    "PATTERN": "pattern_node",
    "INTERFACE": "group_socket_node",
    "GROUP": "group_node",
}
_ZONE_THEME_ATTR = {
    "GeometryNodeSimulationInput": "simulation_zone",
    "GeometryNodeRepeatInput": "repeat_zone",
    "GeometryNodeForeachGeometryElementInput": "foreach_geometry_element_zone",
    "NodeClosureInput": "closure_zone",
}
_DEFAULT_ZONES = {
    "simulation_zone": "#664162",
    "repeat_zone": "#76512f",
    "foreach_geometry_element_zone": "#33527f",
    "closure_zone": "#7d7d3a",
}


@dataclass(frozen=True)
class _Theme:
    back: Color
    grid: Color
    text: Color
    text_dim: Color
    node_body: Color
    node_outline: Color
    frame: Color
    headers: dict[str, Color]
    zones: dict[str, Color]
    wire: Color
    # widgets: (inner, outline, text, item, inner_sel)
    num: tuple[Color, Color, Color, Color, Color]
    menu: tuple[Color, Color, Color, Color, Color]
    text_field: tuple[Color, Color, Color, Color, Color]
    option: tuple[Color, Color, Color, Color, Color]
    selected: Color
    muted: Color


def _widget(
    ui: Any, name: str, defaults: tuple[str, str, str, str, str]
) -> tuple[Color, Color, Color, Color, Color]:
    wc = getattr(ui, name, None)
    if wc is None:
        d = [_hex(d) for d in defaults]
        return (d[0], d[1], d[2], d[3], d[4])
    return (
        _rgba(wc.inner),
        _rgba(wc.outline),
        _rgba(wc.text),
        _rgba(wc.item),
        _rgba(wc.inner_sel),
    )


def _load_theme() -> _Theme:
    """Read the active Blender theme, falling back to the dark defaults."""
    try:
        theme: Any = cast(Any, bpy.context.preferences).themes[0]
        ne: Any = theme.node_editor
        ui: Any = theme.user_interface
    except Exception:  # noqa: BLE001 - no preferences in some embeddings
        ne = ui = None

    def ne_color(attr: str, default: str, alpha: float | None = None) -> Color:
        value = getattr(ne, attr, None) if ne is not None else None
        return _rgba(value, alpha) if value is not None else _hex(default, alpha or 1)

    headers = {
        tag: ne_color(attr, _DEFAULT_HEADERS[tag], 1.0)
        for tag, attr in _THEME_HEADER_ATTR.items()
    }
    headers["NONE"] = ne_color("node_backdrop", _DEFAULT_HEADERS["NONE"], 1.0)
    zones = {name: ne_color(name, default) for name, default in _DEFAULT_ZONES.items()}
    space = getattr(ne, "space", None)
    back = _rgba(space.back) if space is not None else _hex("#1a1a1a")
    text = _rgba(space.text) if space is not None else _hex("#e6e6e6")
    return _Theme(
        back=back,
        grid=ne_color("grid", "#303030", 1.0),
        text=text,
        text_dim=(text[0], text[1], text[2], 0.55),
        node_body=ne_color("node_backdrop", "#303030", 1.0),
        node_outline=_hex("#111111", 0.9),
        frame=ne_color("frame_node", "#0f0f0f", None),
        headers=headers,
        zones=zones,
        wire=ne_color("wire", "#1a1a1a", 1.0),
        num=_widget(
            ui,
            "wcol_numslider",
            ("#545454", "#3d3d3d", "#e6e6e6", "#4772b3", "#222222"),
        ),
        menu=_widget(
            ui, "wcol_menu", ("#282828", "#3d3d3d", "#e6e6e6", "#d9d9d9", "#4772b3")
        ),
        text_field=_widget(
            ui, "wcol_text", ("#1d1d1d", "#3d3d3d", "#e6e6e6", "#ffffff", "#181818")
        ),
        option=_widget(
            ui, "wcol_option", ("#545454", "#3d3d3d", "#e6e6e6", "#ffffff", "#4772b3")
        ),
        selected=ne_color("node_selected", "#ed5700", 1.0),
        muted=_hex("#c83c3c"),
    )


# --------------------------------------------------------------------------
# Text measurement
# --------------------------------------------------------------------------


def _font():
    from matplotlib.font_manager import FontProperties

    return FontProperties(family="DejaVu Sans")


def _text_width(text: str, size: float = _TEXT_SIZE) -> float:
    """Width of *text* in UI units (points) at *size*."""
    from matplotlib.textpath import TextPath

    if not text:
        return 0.0
    # TextPath extents drop trailing whitespace; pad with a glyph and subtract.
    probe = TextPath((0, 0), text + "|", size=size, prop=_font()).get_extents()
    bar = TextPath((0, 0), "|", size=size, prop=_font()).get_extents()
    return float(probe.width - bar.width)


def _fit(text: str, max_width: float, size: float = _TEXT_SIZE) -> str:
    """Truncate *text* with an ellipsis so it fits within *max_width*."""
    if _text_width(text, size) <= max_width:
        return text
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _text_width(text[:mid] + "…", size) <= max_width:
            lo = mid
        else:
            hi = mid - 1
    return (text[:lo] + "…") if lo > 0 else ""


# --------------------------------------------------------------------------
# Node introspection
# --------------------------------------------------------------------------


def _abs_location(node: bpy.types.Node) -> tuple[float, float]:
    x, y = node.location
    parent = node.parent
    while parent is not None:
        x += parent.location.x
        y += parent.location.y
        parent = parent.parent
    return x, y


def _enum_name(node: bpy.types.Node, identifier: str) -> str:
    """The UI name of the enum value *node* holds for property *identifier*."""
    value = getattr(node, identifier, None)
    prop: Any = node.bl_rna.properties.get(identifier)
    if prop is None or value is None:
        return str(value)
    items = getattr(prop, "enum_items", None)
    if items is not None and value in items:
        return items[value].name
    return str(value).replace("_", " ").title()


def _node_title(node: bpy.types.Node) -> str:
    """The text Blender draws in a node's header."""
    if node.label:
        return node.label
    if node.bl_idname.endswith("NodeGroup"):
        tree = getattr(node, "node_tree", None)
        return tree.name if tree is not None else node.bl_label
    if (
        node.bl_idname.endswith("Math") or node.bl_idname == "FunctionNodeCompare"
    ) and node.bl_rna.properties.get("operation") is not None:
        return _enum_name(node, "operation")
    if node.bl_idname in ("ShaderNodeTexImage", "ShaderNodeTexEnvironment"):
        image = getattr(node, "image", None)
        if image is not None:
            return image.name
    return node.bl_label


def _socket_color(socket: bpy.types.NodeSocket, theme: _Theme) -> Color:
    node = socket.node
    try:
        return _rgba(socket.draw_color(bpy.context, cast(Any, node)))
    except Exception:  # noqa: BLE001 - custom sockets may need a real context
        return _hex("#a1a1a1")


def _format_float(value: float, subtype: str) -> str:
    if subtype == "ANGLE":
        return f"{math.degrees(value):.1f}°"
    if subtype == "PERCENTAGE":
        return f"{value:.1f} %"
    if subtype == "DISTANCE":
        return f"{value:.3g} m"
    if subtype == "TIME":
        return f"{value:.0f} frames"
    return f"{value:.3f}"


def _default_value_subtype(socket: bpy.types.NodeSocket) -> str:
    prop = socket.bl_rna.properties.get("default_value")
    return getattr(prop, "subtype", "NONE") or "NONE"


# --------------------------------------------------------------------------
# Drawing primitives
# --------------------------------------------------------------------------


class _Canvas:
    """Thin layer over a matplotlib Axes that draws in UI units."""

    def __init__(self, ax: Axes, theme: _Theme):
        self.ax = ax
        self.theme = theme

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        face: Color | None,
        edge: Color | None = None,
        radius: float = 0.0,
        lw: float = 0.8,
        z: float = 3,
        ls: str = "-",
    ) -> None:
        from matplotlib.patches import FancyBboxPatch, Rectangle

        if radius > 0:
            patch = FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle=f"round,pad=0,rounding_size={min(radius, h / 2, w / 2)}",
                facecolor=face or "none",
                edgecolor=edge or "none",
                lw=lw,
                zorder=z,
                linestyle=ls,
            )
        else:
            patch = Rectangle(
                (x, y),
                w,
                h,
                facecolor=face or "none",
                edgecolor=edge or "none",
                lw=lw,
                zorder=z,
                linestyle=ls,
            )
        self.ax.add_patch(patch)

    def header_rect(self, x: float, y: float, w: float, h: float, face: Color) -> None:
        """A rectangle rounded only at its top corners."""
        from matplotlib.patches import Rectangle

        self.rect(x, y, w, h, face=face, radius=_NODE_RADIUS, z=3.1)
        self.ax.add_patch(
            Rectangle(
                (x, y),
                w,
                min(h / 2, _NODE_RADIUS + 1),
                facecolor=face,
                edgecolor="none",
                zorder=3.1,
            )
        )

    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        size: float = _TEXT_SIZE,
        ha: str = "left",
        va: str = "center",
        color: Color | None = None,
        z: float = 5,
        weight: str = "normal",
    ) -> None:
        if not s:
            return
        self.ax.text(
            x,
            y,
            s,
            fontsize=size,
            fontfamily="DejaVu Sans",
            ha=ha,
            va=va,
            color=color or self.theme.text,
            zorder=z,
            fontweight=weight,
        )

    def socket(
        self, x: float, y: float, shape: str, color: Color, *, z: float = 4
    ) -> None:
        from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, RegularPolygon

        outline = _hex("#0d0d0d", 0.8)
        r = _SOCKET_RADIUS
        kind = shape.split("_")[0]
        patch: Any
        if kind == "LINE":
            patch = FancyBboxPatch(
                (x - 3.0, y - 7.0),
                6.0,
                14.0,
                boxstyle="round,pad=0,rounding_size=3",
                facecolor=color,
                edgecolor=outline,
                lw=0.6,
                zorder=z,
            )
        elif kind == "DIAMOND":
            patch = RegularPolygon(
                (x, y),
                4,
                radius=r * 1.25,
                orientation=0.0,
                facecolor=color,
                edgecolor=outline,
                lw=0.6,
                zorder=z,
            )
        elif kind == "SQUARE":
            patch = Rectangle(
                (x - r * 0.9, y - r * 0.9),
                r * 1.8,
                r * 1.8,
                facecolor=color,
                edgecolor=outline,
                lw=0.6,
                zorder=z,
            )
        else:
            patch = Circle(
                (x, y), r, facecolor=color, edgecolor=outline, lw=0.6, zorder=z
            )
        self.ax.add_patch(patch)
        if shape.endswith("_DOT"):
            self.ax.add_patch(
                Circle((x, y), r * 0.35, facecolor=outline, edgecolor="none", zorder=z)
            )

    def bezier(
        self,
        p0: tuple[float, float],
        p3: tuple[float, float],
        c0: Color,
        c1: Color,
        *,
        dashed: bool = False,
        z: float = 2,
    ) -> None:
        """A link curve shaded from *c0* to *c1*, over a dark outline."""
        import numpy as np
        from matplotlib.collections import LineCollection

        (x0, y0), (x3, y3) = p0, p3
        # Blender: handle length = noodle_curving * 0.1 * |dx|, curving 4.
        d = 0.4 * abs(x3 - x0)
        d = max(d, 12.0)
        x1, y1, x2, y2 = x0 + d, y0, x3 - d, y3
        n = 40
        t = np.linspace(0.0, 1.0, n)
        mt = 1 - t
        xs = mt**3 * x0 + 3 * mt**2 * t * x1 + 3 * mt * t**2 * x2 + t**3 * x3
        ys = mt**3 * y0 + 3 * mt**2 * t * y1 + 3 * mt * t**2 * y2 + t**3 * y3
        pts = np.column_stack([xs, ys])
        segs = np.stack([pts[:-1], pts[1:]], axis=1)
        mids = (t[:-1] + t[1:]) / 2
        colors: list[Any] = [
            tuple(c0[k] * (1 - u) + c1[k] * u for k in range(4)) for u in mids
        ]
        # Scale linewidths from units to points (1 unit == 1 pt at this scale).
        outline = LineCollection(
            cast(Any, segs),
            colors=[self.theme.wire],
            linewidths=_LINK_WIDTH + 1.6,
            capstyle="round",
            zorder=z,
        )
        inner = LineCollection(
            cast(Any, segs),
            colors=colors,
            linewidths=_LINK_WIDTH,
            capstyle="round",
            zorder=z + 0.1,
        )
        if dashed:
            inner.set_linestyle((0, (2.2, 1.6)))
        self.ax.add_collection(outline)
        self.ax.add_collection(inner)


# --------------------------------------------------------------------------
# Node drawing
# --------------------------------------------------------------------------


def _draw_widget_number(
    cv: _Canvas,
    x: float,
    y: float,
    w: float,
    label: str,
    value: str,
    *,
    fraction: float | None = None,
) -> None:
    inner, outline, text, item, _ = cv.theme.num
    h = _WIDGET_HEIGHT
    r = 0.4 * h / 2
    cv.rect(x, y - h / 2, w, h, face=inner, edge=outline, radius=r, z=3.5)
    if fraction is not None:
        fill = max(0.0, min(1.0, fraction)) * w
        if fill > 0:
            cv.rect(x, y - h / 2, fill, h, face=item, radius=r, z=3.6)
    vw = _text_width(value)
    pad = 8.0
    cv.text(x + w - pad, y, value, ha="right", color=text, z=5)
    if label:
        cv.text(x + pad, y, _fit(label, w - vw - 3 * pad), color=text, z=5)


def _draw_widget_menu(cv: _Canvas, x: float, y: float, w: float, value: str) -> None:
    inner, outline, text, _, _ = cv.theme.menu
    h = _WIDGET_HEIGHT
    cv.rect(x, y - h / 2, w, h, face=inner, edge=outline, radius=0.4 * h / 2, z=3.5)
    cv.text(x + 8.0, y, _fit(value, w - 30.0), color=text, z=5)
    # dropdown chevron
    cx, cy = x + w - 11.0, y + 1.0
    cv.ax.plot(
        [cx - 3.2, cx, cx + 3.2],
        [cy + 1.6, cy - 1.8, cy + 1.6],
        color=text,
        lw=0.9,
        zorder=5,
        solid_capstyle="round",
    )


def _draw_widget_text(
    cv: _Canvas, x: float, y: float, w: float, label: str, value: str
) -> None:
    inner, outline, text, _, _ = cv.theme.text_field
    h = _WIDGET_HEIGHT
    field_x = x
    field_w = w
    if label:
        lw = min(_text_width(label) + 6.0, w * 0.45)
        cv.text(x, y, _fit(label, lw), color=cv.theme.text, z=5)
        field_x = x + lw + 4.0
        field_w = w - lw - 4.0
    cv.rect(
        field_x,
        y - h / 2,
        field_w,
        h,
        face=inner,
        edge=outline,
        radius=0.4 * h / 2,
        z=3.5,
    )
    cv.text(field_x + 6.0, y, _fit(value, field_w - 12.0), color=text, z=5)


def _draw_widget_bool(
    cv: _Canvas, x: float, y: float, w: float, label: str, value: bool
) -> None:
    inner, outline, text, _, checked = cv.theme.option
    s = 13.0
    cv.rect(
        x,
        y - s / 2,
        s,
        s,
        face=checked if value else inner,
        edge=outline,
        radius=3,
        z=3.5,
    )
    if value:
        cv.ax.plot(
            [x + 3.0, x + 5.6, x + 10.2],
            [y + 0.2, y - 2.6, y + 3.4],
            color="white",
            lw=1.3,
            zorder=5,
            solid_capstyle="round",
        )
    cv.text(x + s + 6.0, y, _fit(label, w - s - 6.0), color=text, z=5)


def _draw_widget_color(
    cv: _Canvas, x: float, y: float, w: float, label: str, value: Any
) -> None:
    h = _WIDGET_HEIGHT
    lw = w * 0.5
    cv.text(x, y, _fit(label, lw - 6.0), z=5)
    rgba = _rgba(value)
    # Blender shows the display-transformed colour; approximate sRGB gamma.
    face = tuple(min(1.0, c ** (1 / 2.2)) for c in rgba[:3]) + (1.0,)
    cv.rect(
        x + lw,
        y - h / 2,
        w - lw,
        h,
        face=face,  # ty: ignore[invalid-argument-type]
        edge=cv.theme.num[1],
        radius=0.4 * h / 2,
        z=3.5,
    )


def _draw_input_widget(
    cv: _Canvas, socket: bpy.types.NodeSocket, x: float, y: float, width: float
) -> None:
    """Draw the value widget Blender shows for an unlinked, visible input."""
    label = socket.label or socket.name
    wx = x + _WIDGET_INSET
    ww = width - 2 * _WIDGET_INSET
    stype = socket.type
    value = getattr(socket, "default_value", None)

    if socket.is_linked or socket.hide_value or value is None:
        cv.text(x + _LABEL_INSET, y, _fit(label, width - 2 * _LABEL_INSET), z=5)
        return

    if stype == "VALUE":
        subtype = _default_value_subtype(socket)
        fraction = None
        if subtype == "FACTOR":
            fraction = float(value)
        elif subtype == "PERCENTAGE":
            fraction = float(value) / 100.0
        _draw_widget_number(
            cv,
            wx,
            y,
            ww,
            label,
            _format_float(float(value), subtype),
            fraction=fraction,
        )
    elif stype == "INT":
        _draw_widget_number(cv, wx, y, ww, label, str(int(value)))
    elif stype == "VECTOR":
        subtype = _default_value_subtype(socket)
        cv.text(x + _LABEL_INSET, y, _fit(label, width - 2 * _LABEL_INSET), z=5)
        for k, component in enumerate(tuple(value)[:3]):
            row_y = y - (k + 1) * (VECTOR_EXPANDED / 3)
            _draw_widget_number(
                cv, wx, row_y, ww, "", _format_float(float(component), subtype)
            )
    elif stype == "BOOLEAN":
        _draw_widget_bool(cv, wx, y, ww, label, bool(value))
    elif stype == "STRING":
        _draw_widget_text(cv, wx, y, ww, label, str(value))
    elif stype == "RGBA":
        _draw_widget_color(cv, wx, y, ww, label, value)
    elif stype == "MENU":
        _draw_widget_menu(cv, wx, y, ww, _enum_name(cast(Any, socket), "default_value"))
    elif stype in ("OBJECT", "COLLECTION", "IMAGE", "MATERIAL", "TEXTURE"):
        name = getattr(value, "name", "") if value is not None else ""
        _draw_widget_text(cv, wx, y, ww, label, name)
    elif stype == "ROTATION":
        cv.text(x + _LABEL_INSET, y, _fit(label, width - 2 * _LABEL_INSET), z=5)
    else:
        cv.text(x + _LABEL_INSET, y, _fit(label, width - 2 * _LABEL_INSET), z=5)


def _draw_property(
    cv: _Canvas,
    node: bpy.types.Node,
    prop: Any,
    rows: int,
    x: float,
    top: float,
    width: float,
) -> None:
    """Draw one node property whose *rows* rows start at *top*."""
    wx = x + _WIDGET_INSET
    ww = width - 2 * _WIDGET_INSET
    y = top - PROPERTY_ROW / 2
    ident = prop.identifier
    value = getattr(node, ident, None)
    if prop.type == "ENUM":
        _draw_widget_menu(cv, wx, y, ww, _enum_name(node, ident))
    elif prop.type == "BOOLEAN":
        _draw_widget_bool(cv, wx, y, ww, prop.name, bool(value))
    elif prop.type == "POINTER":
        name = getattr(value, "name", "") if value is not None else ""
        _draw_widget_text(cv, wx, y, ww, "", name)
    elif prop.type == "STRING":
        _draw_widget_text(cv, wx, y, ww, "", str(value or ""))
    elif prop.type in ("INT", "FLOAT") and getattr(prop, "array_length", 0) > 1:
        subtype = getattr(prop, "subtype", "NONE")
        components = tuple(cast(Any, value))
        if subtype == "COLOR":
            # Blender draws a colour wheel here; show the swatch it picks.
            height = rows * PROPERTY_ROW - 6.0
            face = tuple(min(1.0, max(0.0, c)) ** (1 / 2.2) for c in components[:3])
            cv.rect(
                wx,
                top - height - 3.0,
                ww,
                height,
                face=(face[0], face[1], face[2], 1.0),
                edge=cv.theme.num[1],
                radius=4.0,
                z=3.5,
            )
            return
        for k in range(rows):
            component = components[k] if k < len(components) else 0.0
            text = (
                str(int(component))
                if prop.type == "INT"
                else _format_float(float(component), subtype)
            )
            _draw_widget_number(cv, wx, top - (k + 0.5) * PROPERTY_ROW, ww, "", text)
    elif prop.type == "INT":
        _draw_widget_number(cv, wx, y, ww, prop.name, str(value))
    elif prop.type == "FLOAT":
        text = _format_float(float(cast(Any, value)), getattr(prop, "subtype", "NONE"))
        _draw_widget_number(cv, wx, y, ww, prop.name, text)
    else:
        cv.text(wx, y, _fit(f"{prop.name}: {value}", ww), z=5)


def _header_color(node: bpy.types.Node, theme: _Theme) -> Color:
    tag = getattr(node, "color_tag", "NONE") or "NONE"
    if tag == "NONE" and node.bl_idname in ("NodeGroupInput", "NodeGroupOutput"):
        tag = "INTERFACE"
    return theme.headers.get(tag, theme.headers["NONE"])


def _draw_collapsed_node(cv: _Canvas, node: bpy.types.Node) -> None:
    x, top = _abs_location(node)
    width, height = calculate_node_dimensions(node)
    header = _header_color(node, cv.theme)
    if node.mute:
        header = (header[0], header[1], header[2], 0.55)
    cv.rect(
        x,
        top - height,
        width,
        height,
        face=header,
        edge=cv.theme.muted if node.mute else cv.theme.node_outline,
        radius=height / 2,
        lw=0.8,
        z=3,
    )
    # collapse arrow (points right when collapsed)
    ax_x, ax_y = x + 12.0, top - height / 2
    cv.ax.plot(
        [ax_x - 2.0, ax_x + 2.0, ax_x - 2.0, ax_x - 2.0],
        [ax_y + 3.5, ax_y, ax_y - 3.5, ax_y + 3.5],
        color=cv.theme.text,
        lw=0.8,
        zorder=5,
    )
    cv.text(x + 22.0, top - height / 2, _fit(_node_title(node), width - 34.0), z=5)
    for socket in list(node.inputs) + list(node.outputs):
        if not (socket.enabled and socket.is_linked):
            continue
        sx = x + width if socket.is_output else x
        sy = top + calculate_socket_offset_y(socket)
        cv.socket(sx, sy, socket.display_shape, _socket_color(socket, cv.theme))


def _draw_node(cv: _Canvas, node: bpy.types.Node) -> None:
    theme = cv.theme
    x, top = _abs_location(node)

    if node.bl_idname == "NodeReroute":
        socket = node.inputs[0] if node.inputs else None
        color = _socket_color(socket, theme) if socket else _hex("#a1a1a1")
        cv.socket(x, top, "CIRCLE", color, z=4)
        if node.label:
            cv.text(x, top + 9.0, node.label, ha="center", size=9.0, z=5)
        return

    if node.hide:
        _draw_collapsed_node(cv, node)
        return

    width, height = calculate_node_dimensions(node)
    bottom = top - height
    body = theme.node_body
    if node.use_custom_color:
        body = _rgba(node.color, 1.0)
    if node.mute:
        body = (body[0], body[1], body[2], 0.6)
    header = _header_color(node, theme)
    outline = theme.muted if node.mute else theme.node_outline

    cv.rect(x, bottom, width, height, face=body, radius=_NODE_RADIUS, z=3)
    cv.header_rect(x, top - HEADER, width, HEADER, header)
    cv.rect(
        x,
        bottom,
        width,
        height,
        face=None,
        edge=outline,
        radius=_NODE_RADIUS,
        lw=0.8,
        z=3.2,
    )

    # collapse arrow (points down when expanded) and title
    ax_x, ax_y = x + 12.0, top - HEADER / 2
    cv.ax.plot(
        [ax_x - 3.5, ax_x + 3.5, ax_x, ax_x - 3.5],
        [ax_y + 2.0, ax_y + 2.0, ax_y - 2.0, ax_y + 2.0],
        color=theme.text,
        lw=0.8,
        zorder=5,
    )
    cv.text(x + 22.0, ax_y, _fit(_node_title(node), width - 30.0), z=5)

    rows = node_rows(node)
    _draw_panel_bands(cv, rows, x, top, width)
    for row in rows:
        sy = top + row.anchor
        if row.kind == "output":
            assert row.socket is not None
            _draw_output_row(cv, node, row.socket, x, sy, width)
        elif row.kind == "property":
            _draw_property(
                cv,
                node,
                row.prop,
                round(row.height / PROPERTY_ROW),
                x,
                top + row.top,
                width,
            )
        elif row.kind == "input":
            assert row.socket is not None
            cv.socket(x, sy, row.socket.display_shape, _socket_color(row.socket, theme))
            _draw_input_widget(cv, row.socket, x, sy, width)
        else:
            _draw_panel_row(cv, row, x, sy, width)


def _draw_output_row(
    cv: _Canvas,
    node: bpy.types.Node,
    socket: bpy.types.NodeSocket,
    x: float,
    sy: float,
    width: float,
) -> None:
    cv.socket(x + width, sy, socket.display_shape, _socket_color(socket, cv.theme))
    if node.bl_idname == "ShaderNodeValue":
        # The Value node edits its output's value in place of the label.
        value = float(getattr(socket, "default_value", 0.0))
        _draw_widget_number(
            cv,
            x + _WIDGET_INSET,
            sy,
            width - 2 * _WIDGET_INSET,
            "",
            _format_float(value, "NONE"),
        )
        return
    label = socket.label or socket.name
    cv.text(
        x + width - _LABEL_INSET,
        sy,
        _fit(label, width - 2 * _LABEL_INSET),
        ha="right",
        z=5,
    )


def _draw_panel_bands(
    cv: _Canvas, rows: list[NodeRow], x: float, top: float, width: float
) -> None:
    """Shade the body of each open panel (header through its last row) a
    touch darker, as Blender does, nested panels darker still."""
    for k, row in enumerate(rows):
        if row.kind != "panel" or not row.open:
            continue
        end = k + 1
        while end < len(rows) and not (
            rows[end].kind == "panel" and rows[end].depth <= row.depth
        ):
            end += 1
        last = rows[end - 1]
        y0 = top + last.top - last.height
        y1 = top + row.top
        cv.rect(
            x,
            y0,
            width,
            y1 - y0,
            face=(0.0, 0.0, 0.0, 0.12),
            z=3.05 + row.depth * 0.001,
        )


def _draw_panel_row(
    cv: _Canvas, row: NodeRow, x: float, sy: float, width: float
) -> None:
    """A panel header: disclosure triangle, bold name, and — while closed —
    the linked sockets folded onto it."""
    indent = 6.0 * row.depth
    ax_x = x + _LABEL_INSET + indent + 3.0
    if row.open:
        xs = [ax_x - 3.2, ax_x + 3.2, ax_x, ax_x - 3.2]
        ys = [sy + 1.8, sy + 1.8, sy - 2.0, sy + 1.8]
    else:
        xs = [ax_x - 1.8, ax_x + 2.2, ax_x - 1.8, ax_x - 1.8]
        ys = [sy + 3.2, sy, sy - 3.2, sy + 3.2]
    cv.ax.plot(xs, ys, color=cv.theme.text, lw=0.8, zorder=5)
    label_x = ax_x + 9.0
    cv.text(
        label_x,
        sy,
        _fit(row.panel.name, x + width - _LABEL_INSET - label_x),
        weight="bold",
        z=5,
    )
    for socket in row.collapsed_sockets:
        sx = x + width if socket.is_output else x
        cv.socket(sx, sy, socket.display_shape, _socket_color(socket, cv.theme))


# --------------------------------------------------------------------------
# Frames, zones, links
# --------------------------------------------------------------------------


def _node_bounds(node: bpy.types.Node) -> tuple[float, float, float, float]:
    x, top = _abs_location(node)
    if node.bl_idname == "NodeReroute":
        return x - 6, top - 6, x + 6, top + 6
    w, h = calculate_node_dimensions(node)
    return x, top - h, x + w, top


def _frame_label_size(frame: bpy.types.Node) -> float:
    return float(getattr(frame, "label_size", 20))


def _frame_depth(node: bpy.types.Node) -> int:
    depth = 0
    parent = node.parent
    while parent is not None:
        depth += 1
        parent = parent.parent
    return depth


def _frame_bounds(
    tree: bpy.types.NodeTree, frame: bpy.types.Node
) -> tuple[float, float, float, float] | None:
    corners = []
    for child in tree.nodes:
        if child.parent != frame:
            continue
        if child.bl_idname == "NodeFrame":
            inner = _frame_bounds(tree, child)
            if inner is not None:
                corners.append(inner)
            continue
        corners.append(_node_bounds(child))
    if not corners:
        return None
    label_room = _frame_label_size(frame) + 10.0 if frame.label else 0.0
    return (
        min(c[0] for c in corners) - _FRAME_PADDING,
        min(c[1] for c in corners) - _FRAME_PADDING,
        max(c[2] for c in corners) + _FRAME_PADDING,
        max(c[3] for c in corners) + _FRAME_PADDING + label_room,
    )


def _draw_frames(cv: _Canvas, tree: bpy.types.NodeTree) -> None:
    frames = sorted(
        (n for n in tree.nodes if n.bl_idname == "NodeFrame"), key=_frame_depth
    )
    for k, frame in enumerate(frames):
        bounds = _frame_bounds(tree, frame)
        if bounds is None:
            continue
        x0, y0, x1, y1 = bounds
        face = cv.theme.frame
        if frame.use_custom_color:
            face = _rgba(frame.color, 0.8)
        cv.rect(x0, y0, x1 - x0, y1 - y0, face=face, radius=8.0, z=1 + k * 0.01)
        if frame.label:
            size = _frame_label_size(frame)
            cv.text(
                (x0 + x1) / 2,
                y1 - size * 0.9,
                _fit(frame.label, x1 - x0 - 16.0, size),
                ha="center",
                size=size,
                z=5,
            )


def _zone_members(
    tree: bpy.types.NodeTree, start: bpy.types.Node, end: bpy.types.Node
) -> set[bpy.types.Node]:
    """Nodes on a path from *start* to *end*: forward-reachable from the zone
    input and backward-reachable from the zone output."""
    forward: dict[bpy.types.Node, set[bpy.types.Node]] = {}
    backward: dict[bpy.types.Node, set[bpy.types.Node]] = {}
    for link in tree.links:
        if link.from_node is None or link.to_node is None:
            continue
        forward.setdefault(link.from_node, set()).add(link.to_node)
        backward.setdefault(link.to_node, set()).add(link.from_node)

    def reach(root: bpy.types.Node, graph: dict) -> set[bpy.types.Node]:
        seen = {root}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for nxt in graph.get(node, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen

    return (reach(start, forward) & reach(end, backward)) | {start, end}


def _draw_zones(cv: _Canvas, tree: bpy.types.NodeTree) -> None:
    for node in tree.nodes:
        attr = _ZONE_THEME_ATTR.get(node.bl_idname)
        if attr is None:
            continue
        paired = getattr(node, "paired_output", None)
        if paired is None:
            continue
        members = _zone_members(tree, node, paired)
        bounds = [_node_bounds(n) for n in members]
        x0 = min(b[0] for b in bounds) - _ZONE_PADDING
        y0 = min(b[1] for b in bounds) - _ZONE_PADDING
        x1 = max(b[2] for b in bounds) + _ZONE_PADDING
        y1 = max(b[3] for b in bounds) + _ZONE_PADDING
        color = cv.theme.zones[attr]
        border = (color[0], color[1], color[2], 0.9)
        cv.rect(
            x0,
            y0,
            x1 - x0,
            y1 - y0,
            face=color,
            edge=border,
            radius=10.0,
            lw=1.0,
            z=1.5,
        )


def _socket_anchor(socket: bpy.types.NodeSocket) -> tuple[float, float]:
    node = socket.node
    assert node is not None
    x, top = _abs_location(node)
    if node.bl_idname == "NodeReroute":
        return x, top
    width = calculate_node_dimensions(node)[0]
    anchor_x = x + width if socket.is_output else x
    return anchor_x, top + calculate_socket_offset_y(socket)


def _draw_link(cv: _Canvas, link: bpy.types.NodeLink) -> None:
    if link.from_socket is None or link.to_socket is None:
        return
    p0 = _socket_anchor(link.from_socket)
    p1 = _socket_anchor(link.to_socket)
    c0 = _socket_color(link.from_socket, cv.theme)
    c1 = _socket_color(link.to_socket, cv.theme)
    if link.is_muted or not link.is_valid:
        c0 = c1 = cv.theme.muted
    dashed = link.from_socket.display_shape.startswith("DIAMOND")
    cv.bezier(p0, p1, c0, c1, dashed=dashed)


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------


def _tree_bounds(tree: bpy.types.NodeTree) -> tuple[float, float, float, float]:
    boxes = []
    for node in tree.nodes:
        if node.bl_idname == "NodeFrame":
            fb = _frame_bounds(tree, node)
            if fb is not None:
                boxes.append(fb)
            continue
        boxes.append(_node_bounds(node))
    if not boxes:
        return -100.0, -100.0, 100.0, 100.0
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


def _render(
    tree: bpy.types.NodeTree,
    filepath: Path,
    *,
    title: str | None,
    dpi: int,
    grid: bool,
) -> Path:
    try:
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
    except ImportError as e:
        raise ImportError(
            "matplotlib is required for to_plot: pip install nodebpy[plot]"
        ) from e

    theme = _load_theme()
    x0, y0, x1, y1 = _tree_bounds(tree)
    x0 -= _MARGIN
    y0 -= _MARGIN
    x1 += _MARGIN
    y1 += _MARGIN + (22.0 if title else 0.0)
    width_in = (x1 - x0) / UNITS_PER_INCH
    height_in = (y1 - y0) / UNITS_PER_INCH
    largest = max(width_in, height_in)
    if largest * dpi > _MAX_PIXELS:
        dpi = max(int(_MAX_PIXELS / largest), 20)

    fig = Figure(figsize=(width_in, height_in), dpi=dpi)
    FigureCanvasAgg(fig)
    fig.patch.set_facecolor(theme.back)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(theme.back)

    cv = _Canvas(ax, theme)
    if grid:
        import numpy as np

        gx = np.arange(math.floor(x0 / _GRID) * _GRID, x1 + _GRID, _GRID)
        gy = np.arange(math.floor(y0 / _GRID) * _GRID, y1 + _GRID, _GRID)
        if gx.size * gy.size <= 250_000:
            mx, my = np.meshgrid(gx, gy)
            ax.scatter(
                mx.ravel(), my.ravel(), s=0.9, color=theme.grid, linewidths=0, zorder=0
            )

    _draw_frames(cv, tree)
    _draw_zones(cv, tree)
    for link in tree.links:
        _draw_link(cv, link)
    for node in tree.nodes:
        if node.bl_idname != "NodeFrame":
            _draw_node(cv, node)

    if title:
        cv.text(x0 + 12.0, y1 - 12.0, title, size=10.0, color=theme.text_dim, z=6)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, dpi=dpi, facecolor=theme.back)
    return filepath


def to_plot(
    tree: bpy.types.NodeTree,
    filepath: str | Path,
    *,
    title: str | None = None,
    dpi: int = 150,
    grid: bool = True,
) -> Path:
    """Draw the tree's current layout to an image file, Blender-style.

    Nodes are drawn at their real locations with the same estimated
    dimensions the arranger uses, so what you see is what the layout
    algorithm saw. Each node shows its header colour, title, socket markers,
    value widgets for unlinked inputs, and property dropdowns; links are
    coloured by socket type (dashed for fields), and frames and zones are
    drawn behind their members.

    Parameters
    ----------
    tree
        The node tree to draw.
    filepath
        Image path; the format follows the extension (``.png``, ``.svg``,
        ``.pdf``, ...).
    title
        Text drawn in the top-left corner, like the editor's breadcrumb.
        Defaults to no title; pass ``tree.name`` to label the render.
    dpi
        Output resolution. One Blender UI unit is drawn as one point, so a
        default 140-wide node is about 290 px across at 150 dpi. Very large
        trees lower the dpi automatically to stay within a sane image size.
    grid
        Draw the editor's dotted background grid.
    """
    return _render(tree, Path(filepath), title=title, dpi=dpi, grid=grid)


_GROUP_NODE_FOR_TREE = {
    "GeometryNodeTree": "GeometryNodeGroup",
    "ShaderNodeTree": "ShaderNodeGroup",
    "CompositorNodeTree": "CompositorNodeGroup",
    "TextureNodeTree": "TextureNodeGroup",
}


def to_node_plot(
    tree: bpy.types.NodeTree,
    filepath: str | Path,
    *,
    title: str | None = None,
    dpi: int = 150,
    width: float | None = None,
    open_panels: bool = False,
    grid: bool = True,
) -> Path:
    """Draw *tree* as the single group node a user sees when they add it.

    A scratch tree holding one group node that references *tree* is drawn
    and discarded, so the image shows the group's interface — input sockets
    with their default values and output sockets — exactly as it appears
    inside another tree.

    Parameters
    ----------
    width
        Node width in UI units; defaults to Blender's default group-node
        width (140), which is also what a user gets when adding the group.
    open_panels
        Expand every interface panel instead of honouring each panel's
        default closed state, so all sockets are visible for review.
    """
    group_idname = _GROUP_NODE_FOR_TREE.get(tree.bl_idname)
    if group_idname is None:
        raise ValueError(f"Cannot draw a group node for tree type {tree.bl_idname}")
    scratch = bpy.data.node_groups.new(".nodebpy_node_plot", cast(Any, tree.bl_idname))
    assert scratch is not None
    try:
        node: Any = scratch.nodes.new(group_idname)
        node.node_tree = tree
        node.location = (0.0, 0.0)
        if width is not None:
            node.width = width
        if open_panels:
            for state in node.panel_states:
                state.is_collapsed = False
        return _render(scratch, Path(filepath), title=title, dpi=dpi, grid=grid)
    finally:
        bpy.data.node_groups.remove(scratch)
