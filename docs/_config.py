"""
Generate _variables.yml for the documentation site.
Run this before building docs to update the version number.
"""

from importlib.metadata import version as get_version
from pathlib import Path

DOC_DIR = Path(__file__).parent

variables_filepath = DOC_DIR / "_variables.yml"
VARIABLES_TPL = """\
version: {version}
"""


def generate_variables_file():
    """
    Generate _variables.yml file in the quartodoc project directory
    """
    version = get_version("nodebpy")
    contents = VARIABLES_TPL.format(version=version)
    variables_filepath.write_text(contents)


if __name__ == "__main__":
    generate_variables_file()
