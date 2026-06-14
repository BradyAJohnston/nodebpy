# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for the geonodes-web-render HTML/payload export."""

import json

import bpy

from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.web_render import (
    DEFAULT_CDN,
    DEFAULT_VERSION,
    to_tree_clipper_payload,
    to_web_render_html,
)


def test_default_version_is_semver_range():
    """The CDN pin is a "0.3" range so patch releases auto-ship (see commit)."""
    assert DEFAULT_VERSION == "0.3"


def test_payload_compressed_has_tree_clipper_prefix():
    """compress=True yields the TreeClipper:: base64(gzip(json)) string."""
    with g.tree("PayloadCompressed") as tree:
        tree.inputs.geometry() >> g.SetPosition() >> tree.outputs.geometry()

    payload = to_tree_clipper_payload(tree)  # compress=True is the default
    assert payload.startswith("TreeClipper::")


def test_payload_uncompressed_is_indented_json():
    """compress=False yields inspectable, indented JSON."""
    with g.tree("PayloadRaw") as tree:
        tree.inputs.geometry() >> g.SetPosition() >> tree.outputs.geometry()

    payload = to_tree_clipper_payload(tree, compress=False)
    # Parses as JSON and is indented (multi-line), unlike the compressed form.
    parsed = json.loads(payload)
    assert isinstance(parsed, dict)
    assert "\n" in payload


def test_payload_uses_material_name_for_material_builder():
    """A MaterialBuilder exports under its material's (live) name, not a group."""
    with s.material("WebRenderMat", fake_user=True) as mat:
        s.MaterialOutput(surface=s.PrincipledBSDF())

    payload = to_tree_clipper_payload(mat, compress=False)
    assert mat.material.name == "WebRenderMat"
    assert "WebRenderMat" in payload


def test_payload_includes_external_datablock_references():
    """External ID references (e.g. an Object Info target) are wired in.

    This exercises the ``set_external`` generator over a non-empty external
    map: the Object Info node points at the startup-file ``Cube``.
    """
    with g.tree("PayloadExternal") as tree:
        obj_info = g.ObjectInfo()
        obj_info.node.inputs["Object"].default_value = bpy.data.objects["Cube"]
        tree.inputs.geometry() >> tree.outputs.geometry()

    payload = to_tree_clipper_payload(tree, compress=False)
    assert "Cube" in payload


def test_html_snippet_default():
    """The default snippet wires module, stylesheet and embedded payload."""
    with g.tree("HtmlDefault") as tree:
        tree.inputs.geometry() >> g.SetPosition() >> tree.outputs.geometry()

    html = to_web_render_html(tree)

    assert f"{DEFAULT_CDN}/geonodes-web-render@{DEFAULT_VERSION}/embed" in html
    assert f"{DEFAULT_CDN}/geonodes-web-render@{DEFAULT_VERSION}/dist/embed.css" in html
    assert "mountGraphView" in html
    # The stylesheet is added once, keyed by a fixed element id.
    assert 'getElementById("gnwr-stylesheet")' in html
    assert "height: 480px" in html
    # The compressed payload is inlined as a JS string literal.
    assert "TreeClipper::" in html


def test_html_snippet_custom_version_cdn_and_height():
    """Custom version/cdn/height flow through to the emitted URLs and style."""
    with g.tree("HtmlCustom") as tree:
        tree.inputs.geometry() >> tree.outputs.geometry()

    html = to_web_render_html(
        tree, height="300px", version="0.3.2", cdn="https://cdn.example.com"
    )

    assert "https://cdn.example.com/geonodes-web-render@0.3.2/embed" in html
    assert "height: 300px" in html


def test_html_snippets_have_unique_container_ids():
    """Each call mounts into its own container so trees don't collide on a page."""
    with g.tree("HtmlUniqueA") as tree:
        tree.inputs.geometry() >> tree.outputs.geometry()

    html_a = to_web_render_html(tree)
    html_b = to_web_render_html(tree)

    def container_id(html: str) -> str:
        marker = 'id="gnwr-'
        start = html.index(marker) + len('id="')
        return html[start : html.index('"', start)]

    assert container_id(html_a) != container_id(html_b)
