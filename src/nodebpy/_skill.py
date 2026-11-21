"""``nodebpy skill``: the agent skill bundled with the package.

The skill (``nodebpy/skills/nodebpy/SKILL.md`` and its references) teaches
AI coding agents to write node trees with the installed nodebpy, so it
always matches the installed version. ``path`` prints its directory;
``install`` copies it into agents' skills directories: by default both
Claude Code's ``~/.claude/skills`` and ``~/.agents/skills``, the shared
directory that Codex, Cursor, Gemini CLI, Copilot, OpenCode and others read.
``--agent`` picks one of them and ``--to`` any other skills directory.
``npx skills add BradyAJohnston/nodebpy`` installs the same folder from the
repository.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent / "skills" / "nodebpy"

AGENT_DIRS = {
    "claude": Path("~/.claude/skills"),
    "agents": Path("~/.agents/skills"),
}


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
    where = parser.add_mutually_exclusive_group()
    where.add_argument(
        "--agent",
        choices=[*AGENT_DIRS, "all"],
        default="all",
        help="claude: ~/.claude/skills; agents: ~/.agents/skills; all (default): both",
    )
    where.add_argument(
        "--to",
        type=Path,
        help="install into this skills directory instead",
    )


def run(args: argparse.Namespace) -> None:
    if args.what == "path":
        print(SKILL_DIR)
        return
    if args.to is not None:
        targets = [args.to]
    elif args.agent == "all":
        targets = list(AGENT_DIRS.values())
    else:
        targets = [AGENT_DIRS[args.agent]]
    for target in targets:
        print(f"installed {install(target)}")
