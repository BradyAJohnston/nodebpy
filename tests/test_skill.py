"""The bundled agent skill: valid, in sync with the repository copy, and
reachable through the CLI."""

import json
import re
import tomllib
from pathlib import Path

import pytest

from nodebpy import _skill
from nodebpy.__main__ import main

REPO = Path(__file__).resolve().parents[1]


def _frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "SKILL.md must start with YAML frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_skill_frontmatter_names_the_skill():
    meta = _frontmatter((_skill.SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    assert meta["name"] == "nodebpy"
    assert 50 < len(meta["description"]) <= 1024


def test_skill_references_exist():
    text = (_skill.SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for link in re.findall(r"\]\((references/[^)]+)\)", text):
        assert (_skill.SKILL_DIR / link).is_file(), link


def test_repository_copy_matches_package_source():
    """``skills/nodebpy`` (what npx skills add and the marketplace read) is a
    copy of the package source; ``make skills`` refreshes it."""
    source = {
        p.relative_to(_skill.SKILL_DIR): p
        for p in _skill.SKILL_DIR.rglob("*")
        if p.is_file()
    }
    copy_dir = REPO / "skills" / "nodebpy"
    copy = {p.relative_to(copy_dir): p for p in copy_dir.rglob("*") if p.is_file()}
    assert set(source) == set(copy)
    for rel, path in source.items():
        assert path.read_bytes() == copy[rel].read_bytes(), (
            f"{rel} differs; run make skills"
        )


def test_plugin_manifest_matches_package():
    manifest = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "nodebpy"
    project = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert manifest["version"] == project["project"]["version"]
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
    assert [p["name"] for p in marketplace["plugins"]] == ["nodebpy"]


def test_skill_cli_path_and_install(tmp_path, capsys):
    main(["skill", "path"])
    assert capsys.readouterr().out.strip() == str(_skill.SKILL_DIR)
    main(["skill", "install", "--to", str(tmp_path)])
    installed = tmp_path / "nodebpy"
    assert (installed / "SKILL.md").read_bytes() == (
        _skill.SKILL_DIR / "SKILL.md"
    ).read_bytes()
    assert not list(installed.rglob("__pycache__"))
    # installing again replaces the copy rather than failing
    main(["skill", "install", "--to", str(tmp_path)])
    assert "installed" in capsys.readouterr().out


# Names the code fragments in the skill assume, as a user's script would have them.
_FRAGMENT_PRELUDE = """
geometry = tree.inputs.geometry("Geometry")
condition = tree.inputs.boolean("Condition")
value = tree.inputs.float("Value")
index = tree.inputs.integer("Index")
height = tree.inputs.float("Height")
pos = g.Position().o.position
if "mod.properties" in __block__:
    tree.inputs.integer("Count")
    mod = obj.modifiers.new("GN", "NODES")
    mod.node_group = tree.tree
"""
# Blocks that show what to run against a user's own tree or source.
_NEEDS_USER_DATA = ('bpy.data.node_groups["My Tree"]', "code_string", 'ns["tree"]')


def _skill_blocks():
    for path in sorted(_skill.SKILL_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, block in enumerate(re.findall(r"```python\n(.*?)```", text, re.DOTALL)):
            yield pytest.param(block, id=f"{path.name}-{i}")


@pytest.mark.parametrize("block", list(_skill_blocks()))
def test_skill_code_runs(block):
    """Every Python block in the skill runs against the installed nodebpy, so
    the skill can't drift from the API it teaches."""
    import textwrap

    import bpy

    from nodebpy import compositor as c
    from nodebpy import geometry as g
    from nodebpy import shader as s
    from nodebpy.builder import TreeBuilder

    if any(marker in block for marker in _NEEDS_USER_DATA):
        compile(block, "<skill>", "exec")
        return
    code = block
    if not re.search(
        r"^with (g|s|c)\.|^with TreeBuilder|^class |^def |^from nodebpy", code, re.MULTILINE
    ):
        prelude = _FRAGMENT_PRELUDE.replace("__block__", repr(block))
        code = "with g.tree('Skill snippet') as tree:\n" + textwrap.indent(
            prelude + code, "    "
        )
    cube = bpy.data.objects.get("Cube") or bpy.data.objects.new(
        "Cube", bpy.data.meshes.new("Cube")
    )
    if cube.name not in bpy.context.scene.collection.all_objects:
        bpy.context.scene.collection.objects.link(cube)
    namespace = {
        "g": g,
        "s": s,
        "c": c,
        "bpy": bpy,
        "TreeBuilder": TreeBuilder,
        "obj": cube,
        "pi": 3.141592653589793,
    }
    exec(compile(code, "<skill>", "exec"), namespace)  # noqa: S102
