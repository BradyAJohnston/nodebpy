from __future__ import annotations

import re
from typing import Optional

from quartodoc import MdRenderer, layout
from plum import dispatch


class Renderer(MdRenderer):
    style = "_renderer.py"

    @dispatch
    def summarize(self, el: layout.Doc, path: Optional[str] = None, shorten: bool = False):
        name = el.name

        # Wrap i_* and o_* attribute names in code backticks
        if re.match(r"^[io]_", name):
            display = f"`{name}`"
        else:
            display = name

        if path is None:
            link = f"[{display}](#{el.anchor})"
        else:
            link = f"[{display}]({path}.qmd#{el.anchor})"

        description = self.summarize(el.obj)
        return self._summary_row(link, description)
