"""Find nodebpy node classes and show their API compactly.

    python lookup.py search <term> [--tree geometry|shader|compositor]
    python lookup.py show <ClassName> [--tree geometry|shader|compositor]
    python lookup.py socket [Vector|Float|Rotation|Matrix|String|...]

`search` matches the term (case-insensitive) against class names, Blender
bl_idnames and the first docstring line. `show` prints the constructor
parameters, enum options, class-method variants and output sockets without
the huge Union types that `inspect.signature` prints. `socket` lists the
methods and properties available on a socket type (what you get from
`node.o.<name>` or `tree.inputs.<type>(...)`), e.g. `vec.normalize()`.
"""

import argparse
import inspect
import re
import typing

import nodebpy  # noqa: F401  (import before bpy so the repo copy wins)
from nodebpy import compositor, geometry, shader

MODULES = {"geometry": geometry, "shader": shader, "compositor": compositor}


def _classes(module):
    for name in dir(module):
        obj = getattr(module, name)
        if name[0].isupper() and inspect.isclass(obj) and hasattr(obj, "_bl_idname"):
            yield name, obj


def _summary(cls) -> str:
    doc = inspect.getdoc(cls) or ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


def search(term: str, trees: list[str]) -> None:
    words = re.split(r"[\s_]+", term.strip())
    pattern = re.compile(".*".join(re.escape(w) for w in words), re.IGNORECASE)
    hits = 0
    for tree in trees:
        for name, cls in _classes(MODULES[tree]):
            idname = getattr(cls, "_bl_idname", "")
            summary = _summary(cls)
            if pattern.search(name) or pattern.search(idname) or pattern.search(summary):
                prefix = {"geometry": "g", "shader": "s", "compositor": "c"}[tree]
                print(f"{prefix}.{name:32} {idname:40} {summary[:70]}")
                hits += 1
    if not hits:
        print(f"no node class matches {term!r}")


def _short_type(annotation) -> str:
    if typing.get_origin(annotation) is typing.Literal:
        return " | ".join(repr(a) for a in typing.get_args(annotation))
    text = str(annotation)
    match = re.search(r"ForwardRef\('(\w+Socket)'\)", text)
    return match.group(1) if match else text.replace("typing.", "")[:40]


def show(name: str, trees: list[str]) -> None:
    for tree in trees:
        cls = getattr(MODULES[tree], name, None)
        if cls is None:
            continue
        print(f"{tree}.{name}  ({getattr(cls, '_bl_idname', '?')})")
        print(f"  {_summary(cls)}\n")
        print("  constructor:")
        try:
            sig = inspect.signature(cls)
            hints = typing.get_type_hints(cls.__init__)
        except Exception:
            sig, hints = inspect.signature(cls), {}
        keyword_only = False
        for param in sig.parameters.values():
            if param.kind is param.KEYWORD_ONLY and not keyword_only:
                print("    * (keyword-only properties)")
                keyword_only = True
            if param.kind in (param.VAR_KEYWORD, param.VAR_POSITIONAL):
                print(f"    {'**' if param.kind is param.VAR_KEYWORD else '*'}{param.name}")
                continue
            default = "" if param.default is param.empty else f" = {param.default!r}"
            kind = _short_type(hints.get(param.name, param.annotation))
            print(f"    {param.name}: {kind}{default}")
        methods, factories = [], {}
        for attr in sorted(dir(cls)):
            if attr.startswith("_") or not attr.islower():
                continue
            static = inspect.getattr_static(cls, attr, None)
            if isinstance(static, classmethod) and attr != "create_group":
                methods.append(attr)
            elif not isinstance(static, (property, staticmethod)) and not callable(static):
                # factory objects: g.Compare.float.less_than(), g.StoreNamedAttribute.point.float()
                subs = tuple(s for s in dir(static) if not s.startswith("_"))
                if subs:
                    factories.setdefault(subs, []).append(attr)
        if methods:
            print("\n  variants:")
            for m in methods:
                params = ", ".join(inspect.signature(getattr(cls, m)).parameters)
                print(f"    {name}.{m}({params})")
        for subs, attrs in factories.items():
            left = attrs[0] if len(attrs) == 1 else "{" + ",".join(attrs) + "}"
            print(f"\n  variants: {name}.{left}.{{{','.join(subs)}}}()")
        doc = inspect.getdoc(cls) or ""
        outputs = doc.split("Outputs\n-------", 1)
        if len(outputs) == 2:
            lines = [l.strip() for l in outputs[1].splitlines() if l.startswith("o.")]
            print("\n  outputs: " + ", ".join(lines))
        return
    print(f"no class {name!r}; try: python lookup.py search {name}")


def socket(kind: str | None) -> None:
    from nodebpy.builder import socket as sockets

    base = set(dir(sockets.Socket))
    classes = {
        n.removesuffix("Socket"): c
        for n, c in vars(sockets).items()
        if inspect.isclass(c) and n.endswith("Socket") and n not in ("Socket", "BaseSocket")
    }
    if not kind:
        print("socket types: " + ", ".join(sorted(classes)))
        return
    key = next((k for k in classes if k.lower() == kind.lower().removesuffix("socket")), None)
    if key is None:
        print(f"no socket type {kind!r}; types: {', '.join(sorted(classes))}")
        return
    cls = classes[key]
    print(f"{key}Socket")
    for attr in sorted(set(dir(cls)) - base):
        if attr.startswith("_"):
            continue
        static = inspect.getattr_static(cls, attr, None)
        doc = (inspect.getdoc(static) or "").strip().splitlines()
        first = doc[0] if doc else ""
        if isinstance(static, property):
            print(f"  .{attr:22} {first[:80]}")
        elif callable(static) or isinstance(static, (classmethod, staticmethod)):
            try:
                params = list(inspect.signature(getattr(cls, attr)).parameters)[1:]
            except (TypeError, ValueError):
                params = []
            print(f"  .{attr}({', '.join(params)})".ljust(40) + f" {first[:70]}")
        else:
            subs = [x for x in dir(static) if not x.startswith("_")]
            print(f"  .{attr}.{{{','.join(subs)}}}()"[:110])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["search", "show", "socket"])
    parser.add_argument("term", nargs="?")
    parser.add_argument("--tree", choices=list(MODULES), default=None)
    args = parser.parse_args()
    trees = [args.tree] if args.tree else list(MODULES)
    if args.command == "socket":
        socket(args.term)
    elif not args.term:
        parser.error(f"{args.command} needs a term")
    else:
        (search if args.command == "search" else show)(args.term, trees)
