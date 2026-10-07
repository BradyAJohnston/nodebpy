"""``nodebpy skill``: the agent skill bundled with the package.

The skill (``nodebpy/skills/nodebpy/SKILL.md`` and its references) teaches
AI coding agents to write node trees with the installed nodebpy, so it
always matches the installed version. ``path`` prints its directory;
``install`` copies it into an agent's skills directory (Claude Code's
``~/.claude/skills`` by default). Other agents are covered by
``npx skills add BradyAJohnston/nodebpy``, which reads the same folder from
the repository.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent / "skills" / "nodebpy"


def install(target: Path) -> Path:
    """Copy the skill into ``target`` (a skills directory), replacing an
    existing ``nodebpy`` skill there, and return the installed directory."""
    destination = Path(target).expanduser() / SKILL_DIR.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        SKILL_DIR, destination, ignore=shutil.ignore_patterns("__pycache__")
    )
    return destination


def add_parser(sub) -> None:
    parser = sub.add_parser(
        "skill",
        help="Locate or install the bundled agent skill.",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("what", choices=["path", "install"])
    parser.add_argument(
        "--to",
        type=Path,
        default=Path("~/.claude/skills"),
        help="skills directory to install into (default: ~/.claude/skills)",
    )


def run(args: argparse.Namespace) -> None:
    if args.what == "path":
        print(SKILL_DIR)
    else:
        print(f"installed {install(args.to)}")
