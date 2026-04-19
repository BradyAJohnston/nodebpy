from __future__ import annotations

from typing import Optional

from plum import dispatch
from quartodoc import MdRenderer, layout


def _section_title(section) -> str | None:
    """Extract the title from a griffe DocstringSection, handling multiple representations."""
    # Direct title attribute (some griffe versions)
    title = getattr(section, "title", None)
    if title:
        return title
    # Admonition sections store title in value.annotation
    value = getattr(section, "value", None)
    if value is not None:
        return getattr(value, "annotation", None)
    return None


def _section_content(section) -> str:
    """Extract raw text content from a section value."""
    value = getattr(section, "value", None)
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    # Admonition: value.description holds the body
    desc = getattr(value, "description", None)
    if desc is not None:
        return desc
    return str(value)


def _parse_socket_rows(text: str) -> list[tuple[str, str, str]]:
    """Parse numpy-style socket lines into (name, type, description) tuples.

    Expected format per socket:
        prefix.name : TypeClass
            Description text
    """
    rows = []
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if " : " in stripped and not stripped.startswith(" "):
            name, type_str = stripped.split(" : ", 1)
            desc = ""
            if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                desc = lines[i + 1].strip()
                i += 1
            rows.append((name.strip(), type_str.strip(), desc))
        i += 1
    return rows


def _rows_to_table(rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return ""
    header = "| Attribute | Type | Description |\n|-----------|------|-------------|"
    body = "\n".join(
        f"| `{name}` | `{type_str}` | {desc} |" for name, type_str, desc in rows
    )
    return f"{header}\n{body}"


class Renderer(MdRenderer):
    style = "_renderer.py"

    @dispatch
    def render(self, el: layout.DocClass):
        cls = el.obj

        if not cls.docstring:
            return super().render(el)

        # Separate Inputs/Outputs sections from the rest before standard rendering.
        # Griffe can't parse these non-standard numpy sections cleanly, so we
        # intercept them and render as proper tables ourselves.
        original_parsed = cls.docstring.parsed
        filtered = []
        socket_tables: list[tuple[str, str]] = []  # (title, markdown table)

        for section in original_parsed:
            title = _section_title(section)
            if title in ("Inputs", "Outputs"):
                content = _section_content(section)
                rows = _parse_socket_rows(content)
                table = _rows_to_table(rows)
                if table:
                    socket_tables.append((title, table))
            else:
                filtered.append(section)

        # Temporarily swap out parsed sections so super() never sees Inputs/Outputs
        cls.docstring.parsed = filtered
        result = super().render(el)
        cls.docstring.parsed = original_parsed

        if socket_tables:
            result += "\n\n" + "\n\n".join(
                f"**{title}**\n\n{table}" for title, table in socket_tables
            )

        return result

    @dispatch
    def summarize(
        self, el: layout.DocAttribute, path: Optional[str] = None, shorten: bool = False
    ):
        name = el.name
        if path is None:
            link = f"[`{name}`](#{el.anchor})"
        else:
            link = f"[`{name}`]({path}.qmd#{el.anchor})"
        description = self.summarize(el.obj)
        return self._summary_row(link, description)
