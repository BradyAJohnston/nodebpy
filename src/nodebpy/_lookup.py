"""``nodebpy lookup``: find node classes and show their API compactly.

``search <term>`` matches the term (case-insensitive, words may be separated
by anything) against class names, Blender ``bl_idname``s and the first
docstring line. ``show <ClassName>`` prints the constructor parameters, enum
options, class-method variants and output sockets without the long Union
types ``inspect.signature`` prints. ``socket [Type]`` lists the methods and
properties on a socket type (what ``node.o.<name>`` or
``tree.inputs.<type>(...)`` returns), or the socket types themselves.
"""

from __future__ import annotations

import argparse
import inspect
import re
import typing
from collections.abc import Iterator

_PREFIX = {"geometry": "g", "shader": "s", "compositor": "c"}


def _modules() -> dict[str, object]:
    import nodebpy  # noqa: F401  # before bpy: the project's own copy wins
    from nodebpy import compositor, geometry, shader

    return {"geometry": geometry, "shader": shader, "compositor": compositor}


def _classes(module) -> Iterator[tuple[str, type]]:
    for name in dir(module):
        obj = getattr(module, name)
        if name[0].isupper() and inspect.isclass(obj) and hasattr(obj, "_bl_idname"):
            yield name, obj


def _summary(cls) -> str:
    doc = inspect.getdoc(cls) or ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


def search(term: str, trees: list[str]) -> list[str]:
    words = re.split(r"[\s_]+", term.strip())
    pattern = re.compile(".*".join(re.escape(w) for w in words), re.IGNORECASE)
    modules = _modules()
    lines = []
    for tree in trees:
        for name, cls in _classes(modules[tree]):
            idname = getattr(cls, "_bl_idname", "")
            summary = _summary(cls)
            if (
                pattern.search(name)
                or pattern.search(idname)
                or pattern.search(summary)
            ):
                lines.append(f"{_PREFIX[tree]}.{name:32} {idname:40} {summary[:70]}")
    return lines or [f"no node class matches {term!r}"]


def _short_type(annotation) -> str:
    if typing.get_origin(annotation) is typing.Literal:
        return " | ".join(repr(a) for a in typing.get_args(annotation))
    text = str(annotation)
    match = re.search(r"ForwardRef\('(\w+Socket)'\)", text)
    return match.group(1) if match else text.replace("typing.", "")[:40]


def _signature_lines(fn, names_only: bool = False) -> list[str]:
    """One entry per parameter, with a ``*`` marker before keyword-only ones."""
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):  # pragma: no cover - C-implemented callables
        return []
    hints: dict = {}
    if not names_only:
        try:
            hints = typing.get_type_hints(fn)
        except Exception:  # noqa: BLE001 - forward references that do not resolve
            hints = {}
    entries, keyword_only = [], False
    for param in sig.parameters.values():
        if param.name == "self":
            continue
        if param.kind is param.KEYWORD_ONLY and not keyword_only:
            entries.append("*")
            keyword_only = True
        if param.kind in (param.VAR_KEYWORD, param.VAR_POSITIONAL):
            entries.append(
                f"{'**' if param.kind is param.VAR_KEYWORD else '*'}{param.name}"
            )
            continue
        if names_only:
            entries.append(param.name)
            continue
        default = "" if param.default is param.empty else f" = {param.default!r}"
        kind = _short_type(hints.get(param.name, param.annotation))
        entries.append(f"{param.name}: {kind}{default}")
    return entries


def show(name: str, trees: list[str]) -> list[str]:
    modules = _modules()
    for tree in trees:
        cls = getattr(modules[tree], name, None)
        if cls is None:
            continue
        lines = [
            f"{tree}.{name}  ({getattr(cls, '_bl_idname', '?')})",
            f"  {_summary(cls)}",
            "",
            "  constructor:",
        ]
        for entry in _signature_lines(cls.__init__):
            lines.append(
                "    * (keyword-only properties)" if entry == "*" else f"    {entry}"
            )
        methods, factories = [], {}
        for attr in sorted(dir(cls)):
            if attr.startswith("_") or not attr.islower():
                continue
            static = inspect.getattr_static(cls, attr, None)
            if isinstance(static, classmethod) and attr != "create_group":
                methods.append(attr)
            elif not isinstance(static, (property, staticmethod)) and not callable(
                static
            ):
                # factory objects: g.Compare.float.less_than(), g.StoreNamedAttribute.point.float()
                subs = tuple(s for s in dir(static) if not s.startswith("_"))
                if subs:
                    factories.setdefault(subs, []).append(attr)
        if methods:
            lines.append("")
            lines.append("  variants:")
            for m in methods:
                params = ", ".join(_signature_lines(getattr(cls, m), names_only=True))
                lines.append(f"    {name}.{m}({params})")
        for subs, attrs in factories.items():
            left = attrs[0] if len(attrs) == 1 else "{" + ",".join(attrs) + "}"
            lines.append("")
            lines.append(f"  variants: {name}.{left}.{{{','.join(subs)}}}()")
        doc = inspect.getdoc(cls) or ""
        outputs = doc.split("Outputs\n-------", 1)
        if len(outputs) == 2:
            names = [
                ln.strip() for ln in outputs[1].splitlines() if ln.startswith("o.")
            ]
            lines.append("")
            lines.append("  outputs: " + ", ".join(names))
        return lines
    return [f"no class {name!r}; try: nodebpy lookup search {name}"]


def socket(kind: str | None) -> list[str]:
    from nodebpy.builder import socket as sockets

    base = set(dir(sockets.Socket))
    classes = {
        n.removesuffix("Socket"): c
        for n, c in vars(sockets).items()
        if inspect.isclass(c)
        and n.endswith("Socket")
        and n not in ("Socket", "BaseSocket")
    }
    if not kind:
        return ["socket types: " + ", ".join(sorted(classes))]
    wanted = kind.lower().removesuffix("socket")
    key = next((k for k in classes if k.lower() == wanted), None)
    if key is None:
        return [f"no socket type {kind!r}; types: {', '.join(sorted(classes))}"]
    cls = classes[key]
    lines = [f"{key}Socket"]
    for attr in sorted(set(dir(cls)) - base):
        if attr.startswith("_"):
            continue
        static = inspect.getattr_static(cls, attr, None)
        doc = (inspect.getdoc(static) or "").strip().splitlines()
        first = doc[0] if doc else ""
        if isinstance(static, property):
            lines.append(f"  .{attr:22} {first[:80]}")
        elif callable(static) or isinstance(static, (classmethod, staticmethod)):
            params = _signature_lines(getattr(cls, attr), names_only=True)
            lines.append(f"  .{attr}({', '.join(params)})".ljust(40) + f" {first[:70]}")
        else:  # pragma: no cover - a plain factory object on a socket class
            subs = [x for x in dir(static) if not x.startswith("_")]
            lines.append(f"  .{attr}.{{{','.join(subs)}}}()"[:110])
    return lines


def add_parser(sub) -> None:
    parser = sub.add_parser(
        "lookup",
        help="Find node classes and show their API: search, show, socket.",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("what", choices=["search", "show", "socket"])
    parser.add_argument(
        "term", nargs="?", help="search term, class name or socket type"
    )
    parser.add_argument(
        "--tree", choices=list(_PREFIX), default=None, help="limit to one tree type"
    )


def run(args: argparse.Namespace) -> None:
    trees = [args.tree] if args.tree else list(_PREFIX)
    if args.what == "socket":
        lines = socket(args.term)
    elif not args.term:
        raise SystemExit(f"nodebpy lookup {args.what} needs a term")
    elif args.what == "search":
        lines = search(args.term, trees)
    else:
        lines = show(args.term, trees)
    print("\n".join(lines))
