"""Report what the public API lost between a release and the working tree.

Regenerating the node classes can change public names without anyone editing
them: Blender renames a socket or an enum item, turns a property into a menu
socket, or gives two inputs the same name. This compares the source of
``src/nodebpy`` at a git ref (normally the last release tag) with the working
tree, statically, and lists every public name that is gone::

    uv run python -m gen.api_diff v530.0.0
    uv run python -m gen.api_diff v520.41.0 5.3     # between two refs

Reported: public classes and module-level functions, their public methods and
properties, parameters (a renamed parameter shows as removed), positional
parameters that moved to another slot or became keyword-only, ``Literal``
values a parameter no longer takes, and the ``i.<name>`` / ``o.<name>`` socket
attributes. Private classes are included, as the generated classes get public
methods from ``_...Mixin`` bases. Classes are keyed by package (``nodes.geometry.Math``), so moving
one between modules of a package is not a removal. Additions are not listed.

Exits 1 when something was removed: each entry needs a deprecation shim or a
breaking-change entry in the changelog (see CONTRIBUTING.md, "Changing the
public API").
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path

ROOT = "src/nodebpy"


def _sources(ref: str | None) -> dict[str, str]:
    """Path -> source of every module under ``ROOT`` at ``ref`` (``None``: the
    working tree)."""
    if ref is None:
        return {str(p): p.read_text() for p in Path(ROOT).rglob("*.py")}
    names = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, ROOT],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return {
        name: subprocess.run(
            ["git", "show", f"{ref}:{name}"], capture_output=True, text=True, check=True
        ).stdout
        for name in names
        if name.endswith(".py")
    }


def _literals(annotation: ast.expr | None) -> set[str]:
    """The string values of every ``Literal[...]`` in an annotation."""
    values: set[str] = set()
    for node in ast.walk(annotation) if annotation is not None else ():
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == "Literal"
        ):
            values |= {
                c.value
                for c in ast.walk(node.slice)
                if isinstance(c, ast.Constant) and isinstance(c.value, str)
            }
    return values


def _params(
    func: ast.FunctionDef,
) -> tuple[list[str], list[str], dict[str, set[str]]]:
    """(positional parameters in order, keyword-only parameters, the
    ``Literal`` values each parameter accepts)."""
    a = func.args
    args = [x for x in a.posonlyargs + a.args if x.arg not in ("self", "cls")]
    literals = {x.arg: _literals(x.annotation) for x in args + a.kwonlyargs}
    return [x.arg for x in args], [x.arg for x in a.kwonlyargs], literals


def _is_public(name: str) -> bool:
    return not name.startswith("_") or name == "__init__"


def _api(ref: str | None) -> dict[str, dict]:
    """Public API keyed ``package.Name``; classes map member names to
    parameters (or ``None`` for socket attributes)."""
    api: dict[str, dict] = {}
    for path, source in _sources(ref).items():
        if "/skills/" in path:
            continue
        package = ".".join(Path(path).relative_to(ROOT).parent.parts)
        for node in ast.parse(source).body:
            if isinstance(node, ast.FunctionDef) and _is_public(node.name):
                api[f"{package}.{node.name}()"] = {"": _params(node)}
            # private classes too: generated classes get public methods from
            # ``_...Mixin`` bases
            if not isinstance(node, ast.ClassDef):
                continue
            members: dict[str, tuple | None] = {}
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and _is_public(item.name):
                    members.setdefault(item.name, _params(item))
                elif isinstance(item, ast.ClassDef) and item.name in (
                    "_Inputs",
                    "_Outputs",
                ):
                    prefix = "i" if item.name == "_Inputs" else "o"
                    for ann in item.body:
                        if isinstance(ann, ast.AnnAssign) and isinstance(
                            ann.target, ast.Name
                        ):
                            members[f"{prefix}.{ann.target.id}"] = None
            api[f"{package}.{node.name}"] = members
    return api


def removals(old_ref: str, new_ref: str | None = None) -> list[str]:
    old, new = _api(old_ref), _api(new_ref)
    found = []
    for name in sorted(old):
        if name not in new:
            found.append(f"{name}: removed")
            continue
        for member, params in old[name].items():
            label = f"{name}.{member}" if member else name
            if member not in new[name]:
                found.append(f"{label}: removed")
                continue
            if params is None:
                continue
            (old_pos, old_kw, old_lit), (new_pos, new_kw, new_lit) = (
                params,
                new[name][member],
            )
            gone = [p for p in old_pos + old_kw if p not in new_pos + new_kw]
            if gone:
                found.append(f"{label}: parameters removed {gone}")
            # a positional call must still land every argument where it did
            kept = [p for p in old_pos if p in new_pos]
            for slot, (was, now) in enumerate(zip(kept, new_pos)):
                if was != now:
                    found.append(
                        f"{label}: positional slot {slot} was {was}, now {now}"
                    )
                    break
            moved = [p for p in old_pos if p in new_kw]
            if moved:
                found.append(f"{label}: now keyword-only {moved}")
            for param, values in old_lit.items():
                lost = values - new_lit.get(param, values)
                if lost and new_lit.get(param):
                    found.append(f"{label}: {param}= no longer takes {sorted(lost)}")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gen.api_diff")
    parser.add_argument("old", help="git ref of the release to compare against")
    parser.add_argument("new", nargs="?", help="git ref (default: working tree)")
    args = parser.parse_args(argv)
    found = removals(args.old, args.new)
    print("\n".join(found) if found else "No public API removed.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
