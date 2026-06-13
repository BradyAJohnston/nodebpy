# SPDX-License-Identifier: GPL-3.0-or-later
"""Render node trees as interactive graphs via geonodes-web-render.

The live Blender node tree built by a :class:`~nodebpy.builder.tree.TreeBuilder`
is exported to the Tree Clipper JSON format (using the ``tree_clipper`` package)
and embedded into a small HTML snippet that mounts the ``geonodes-web-render``
web component in the browser. This is what powers the rich ``_repr_html_`` shown
for a tree in Jupyter and Quarto.

Nothing here needs network access at build time: the Tree Clipper payload is
inlined into the HTML, and only the (cached) JS/CSS are fetched from the CDN
when the page is viewed.
"""

from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .builder.tree import TreeBuilder

#: Default geonodes-web-render version served from the CDN.
DEFAULT_VERSION = "0.3.1"

#: Default ESM CDN. esm.sh transparently resolves the external react/react-dom.
DEFAULT_CDN = "https://esm.sh"


def to_tree_clipper_payload(builder: "TreeBuilder", *, compress: bool = True) -> str:
    """Export *builder*'s node tree to a Tree Clipper payload.

    With ``compress=True`` (the default) the result is the ``TreeClipper::`` +
    base64(gzip(json)) string consumed directly by geonodes-web-render. With
    ``compress=False`` it is indented JSON, handy for inspection.

    Requires the optional ``tree_clipper`` package to be importable.
    """
    from tree_clipper.export_nodes import ExportIntermediate, ExportParameters
    from tree_clipper.specific_handlers import BUILT_IN_EXPORTER

    # A MaterialBuilder owns a bpy.types.Material; a plain TreeBuilder owns a
    # node group. Tree Clipper looks the root up by name in the matching
    # collection, so use the live name (Blender may have de-duplicated it).
    material = getattr(builder, "material", None)
    is_material = material is not None
    name = material.name if is_material else builder.tree.name

    export = ExportIntermediate(
        parameters=ExportParameters(
            is_material=is_material,
            name=name,
            specific_handlers=BUILT_IN_EXPORTER,
            export_sub_trees=True,
            debug_prints=False,
            write_from_roots=False,
        )
    )
    while export.step():
        pass
    export.set_external(
        (external_id, item.pointed_to_by.get_pointee().name)
        for external_id, item in export.get_external().items()
    )
    return export.export_to_str(compress=compress, json_indent=4)


def to_web_render_html(
    builder: "TreeBuilder",
    *,
    height: str = "480px",
    version: str = DEFAULT_VERSION,
    cdn: str = DEFAULT_CDN,
) -> str:
    """Return a self-contained HTML snippet rendering *builder* as a graph.

    The snippet mounts one geonodes-web-render instance into its own container,
    so multiple trees can be shown on the same page. The stylesheet is added to
    ``<head>`` only once across all snippets.
    """
    payload = to_tree_clipper_payload(builder, compress=True)
    container_id = f"gnwr-{uuid.uuid4().hex}"
    module_url = f"{cdn}/geonodes-web-render@{version}/embed"
    css_url = f"{cdn}/geonodes-web-render@{version}/dist/embed.css"
    # json.dumps keeps the payload a valid, safely-quoted JS string literal.
    payload_js = json.dumps(payload)
    css_id = "gnwr-stylesheet"

    return (
        f'<div id="{container_id}" '
        f'style="height: {height}; width: 100%; border-radius: 8px; overflow: hidden;">'
        f"</div>\n"
        f'<script type="module">\n'
        f'if (!document.getElementById("{css_id}")) {{\n'
        f'  const link = document.createElement("link");\n'
        f'  link.id = "{css_id}";\n'
        f'  link.rel = "stylesheet";\n'
        f'  link.href = "{css_url}";\n'
        f"  document.head.appendChild(link);\n"
        f"}}\n"
        f'import {{ mountGraphView }} from "{module_url}";\n'
        f'mountGraphView(document.getElementById("{container_id}"), '
        f"{{ payload: {payload_js} }});\n"
        f"</script>"
    )
