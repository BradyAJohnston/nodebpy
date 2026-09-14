"""Generate ``nodebpy/builder/_socket_order.py`` from Blender's node sources.

Blender draws most nodes *conventionally*: outputs, then the node's buttons,
then inputs, in the order of ``node.outputs`` / ``node.inputs`` — which is
all the headless ``bpy`` module exposes. Since Blender 4.0 a growing set of
nodes instead declare ``use_custom_socket_order()``: their sockets are drawn
in declaration order, inputs and outputs interleaved, an output can share a
row with the input declared before it (``align_with_previous()``), buttons
sit wherever ``add_default_layout()`` / ``add_layout()`` was called, and
sockets can be grouped into collapsible panels. None of that is visible
through RNA, so this script parses the ``node_declare`` functions of the
node sources for the Blender version the installed ``bpy`` reports and
records, per node ``bl_idname``, the sequence of drawn items.

Run with either a Blender source checkout or let it sparse-clone the
matching tag::

    uv run python -m gen.socket_order                # clones v<bpy version>
    uv run python -m gen.socket_order --source ~/blender-src
    uv run python -m gen.socket_order --tag v5.2.0

The parser is deliberately small: it walks each declaration linearly, so a
socket declared under a condition or inside an item loop is recorded as
present (missing sockets are skipped at runtime) or as a dynamic ``items``
block, respectively.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "src" / "nodebpy" / "builder" / "_socket_order.py"
REPO = "https://github.com/blender/blender"
NODE_DIRS = ("geometry", "shader", "function", "composite", "texture")

Entry = tuple[Any, ...]

_DECLARE_RE = re.compile(
    r"^static void (\w+)\(\s*(?:blender::)?(?:nodes::)?NodeDeclarationBuilder\s*&\s*b\s*\)\s*\{",
    re.MULTILINE,
)
_REGISTER_RE = re.compile(r"ntype\.declare\s*=\s*(?:\w+::)*(\w+)\s*;")
_IDNAME_RE = re.compile(r'node_type_base\(\s*&ntype,\s*"([A-Za-z0-9_]+)"')
_CALL_RE = re.compile(
    r"\b(?P<obj>[A-Za-z_]\w*)\s*\.\s*(?P<call>add_input|add_output|add_layout|"
    r"add_default_layout|add_panel|add_separator|use_custom_socket_order)\s*"
    r"(?:<[^;(]*?>)?\s*\("
)
_ASSIGN_RE = re.compile(r"&\s*(\w+)\s*=\s*$")
_STRING_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def _balanced(text: str, start: int, open_ch: str = "(", close_ch: str = ")") -> int:
    """Index just past the bracket that closes the one at ``text[start]``."""
    depth = 0
    i = start
    in_string = False
    while i < len(text):
        c = text[i]
        if in_string:
            if c == "\\":
                i += 1
            elif c == '"':
                in_string = False
        elif c == '"':
            in_string = True
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced brackets")


def _chain_after(text: str, pos: int) -> str:
    """The method chain following a call: text up to the statement's ``;``
    (skipping over nested brackets, e.g. lambdas passed to ``.description``)."""
    i = pos
    while i < len(text):
        c = text[i]
        if c == ";":
            return text[pos:i]
        if c in "([{":
            i = _balanced(text, i, c, {"(": ")", "[": "]", "{": "}"}[c])
            continue
        if c == '"':
            i = _STRING_RE.match(text, i).end()  # type: ignore[union-attr]
            continue
        i += 1
    return text[pos:]


@dataclass
class _Panel:
    name: str
    default_closed: bool
    items: list[Any] = field(default_factory=list)


def _literals(args: str) -> list[str]:
    return [m.group(1) for m in _STRING_RE.finditer(args)]


def parse_declaration(body: str) -> tuple[bool, list[Entry]]:
    """Parse one ``node_declare`` body into ``(custom_order, entries)``."""
    root: list[Any] = []
    panels: dict[str, _Panel] = {}
    custom = False
    pos = 0
    while True:
        m = _CALL_RE.search(body, pos)
        if m is None:
            break
        obj, call = m.group("obj"), m.group("call")
        args_start = m.end() - 1
        args_end = _balanced(body, args_start)
        args = body[args_start + 1 : args_end - 1]
        chain = _chain_after(body, args_end)
        pos = args_end

        target = panels[obj].items if obj in panels else root
        if obj != "b" and obj not in panels:
            # A builder we don't track (e.g. a helper); treat as root.
            target = root

        if call == "use_custom_socket_order":
            custom = "false" not in args
        elif call in ("add_layout", "add_default_layout"):
            target.append(("layout",))
        elif call == "add_separator":
            target.append(("separator",))
        elif call == "add_panel":
            names = _literals(args)
            panel = _Panel(names[0] if names else "", "default_closed(true" in chain)
            target.append(panel)
            assign = _ASSIGN_RE.search(body[: m.start()].rstrip())
            if assign:
                panels[assign.group(1)] = panel
        else:  # add_input / add_output
            side = "in" if call == "add_input" else "out"
            names = _literals(args)
            aligned = (
                ".align_with_previous(" in chain
                and "false" not in chain.split(".align_with_previous(")[1].split(")")[0]
            )
            if not names:
                target.append(("dyn", side, aligned))
                continue
            name = names[0]
            identifier = names[1] if len(names) > 1 else name
            if ".panel_toggle(" in chain and side == "in":
                target.append(("toggle", identifier))
            else:
                target.append((side, identifier, aligned))

    return custom, _flatten(root)


def _flatten(items: list[Any]) -> list[Entry]:
    out: list[Entry] = []
    pending_dyn: list[tuple[str, bool]] | None = None

    def flush() -> None:
        nonlocal pending_dyn
        if pending_dyn:
            has_in = any(s == "in" for s, _ in pending_dyn)
            has_out = any(s == "out" for s, _ in pending_dyn)
            aligned = any(a for _, a in pending_dyn)
            out.append(("items", has_in, has_out, aligned))
        pending_dyn = None

    for item in items:
        if isinstance(item, _Panel):
            flush()
            out.append(("panel", item.name, item.default_closed))
            out.extend(_flatten(item.items))
            out.append(("end",))
        elif item[0] == "dyn":
            pending_dyn = (pending_dyn or []) + [(item[1], item[2])]
        elif item[0] == "separator":
            continue
        else:
            flush()
            out.append(item)
    flush()
    return out


def parse_file(path: Path) -> dict[str, tuple[bool, list[Entry]]]:
    """Map every registered node idname in *path* to its parsed declaration."""
    text = path.read_text(encoding="utf-8", errors="replace")
    declares: list[tuple[int, str, str]] = []  # (pos, fn name, body)
    for m in _DECLARE_RE.finditer(text):
        brace = m.end() - 1
        try:
            end = _balanced(text, brace, "{", "}")
        except ValueError:
            continue
        declares.append((m.start(), m.group(1), text[brace + 1 : end - 1]))

    result: dict[str, tuple[bool, list[Entry]]] = {}
    for reg in _REGISTER_RE.finditer(text):
        fn = reg.group(1)
        idname_match = None
        for cand in _IDNAME_RE.finditer(text, 0, reg.start()):
            idname_match = cand
        if idname_match is None:
            continue
        # The declare function registered here is the nearest one with that
        # name defined before the registration (files with several nodes
        # reuse `node_declare` in separate namespaces).
        body = None
        for pos, name, candidate in declares:
            if name == fn and pos < reg.start():
                body = candidate
        if body is None:
            continue
        result[idname_match.group(1)] = parse_declaration(body)
    return result


def _bpy_tag() -> str:
    import bpy

    major, minor, patch = bpy.app.version
    return f"v{major}.{minor}.{patch}"


def _sparse_clone(tag: str, into: Path) -> Path:
    print(f"Cloning {REPO} at {tag} (sparse, blobless) ...")
    subprocess.run(
        [
            "git",
            "clone",
            "--quiet",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            "--branch",
            tag,
            REPO,
            str(into),
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(into), "sparse-checkout", "set", "source/blender/nodes"],
        check=True,
    )
    return into


def collect(source: Path) -> dict[str, list[Entry]]:
    """Parse every node source under *source* and keep the nodes drawn with
    a custom socket order (the only ones Blender draws from their
    declaration; conventional nodes are drawn outputs-buttons-inputs)."""
    nodes_root = source / "source" / "blender" / "nodes"
    files: list[Path] = []
    if nodes_root.is_dir():
        for sub in NODE_DIRS:
            files.extend(sorted((nodes_root / sub / "nodes").glob("node_*.cc")))
    else:
        files = sorted(source.rglob("node_*.cc"))
    table: dict[str, list[Entry]] = {}
    for path in files:
        for idname, (custom, entries) in parse_file(path).items():
            if custom:
                table[idname] = entries
    return table


def render(table: dict[str, list[Entry]], tag: str) -> str:
    lines = [
        '"""Socket draw order of Blender nodes declared with a custom socket',
        "order. GENERATED by ``python -m gen.socket_order`` from the Blender",
        f"sources at ``{tag}`` — do not edit by hand.",
        "",
        "Each entry is one drawn item, top to bottom:",
        "",
        '- ``("in" | "out", identifier, aligned)`` — a socket; ``aligned`` puts it',
        "  on the same row as the socket entry before it.",
        '- ``("toggle", identifier)`` — a boolean input drawn in its panel header.',
        '- ``("items", has_inputs, has_outputs, aligned)`` — a dynamic block of',
        "  item sockets (zone / switch / bundle items), paired by identifier.",
        '- ``("layout",)`` — where the node\'s buttons are drawn.',
        '- ``("panel", name, default_closed)`` … ``("end",)`` — a collapsible panel.',
        '"""',
        "",
        "from __future__ import annotations",
        "",
        f"BLENDER_VERSION = {tuple(int(p) for p in tag.lstrip('v').split('.'))!r}",
        "",
        "SOCKET_ORDER: dict[str, tuple[tuple, ...]] = {",
    ]
    for idname in sorted(table):
        lines.append(f"    {idname!r}: (")
        for entry in table[idname]:
            lines.append(f"        {entry!r},")
        lines.append("    ),")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", type=Path, help="Blender source checkout to parse.")
    parser.add_argument(
        "--tag", help="Blender git tag to clone (default: the installed bpy version)."
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)

    tag = args.tag or _bpy_tag()
    if args.source is not None:
        table = collect(args.source)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            table = collect(_sparse_clone(tag, Path(tmp) / "blender"))
    if not table:
        sys.exit("No custom-ordered node declarations found")
    args.output.write_text(render(table, tag), encoding="utf-8")
    print(f"Wrote {len(table)} node socket orders to {args.output}")


if __name__ == "__main__":
    main()
