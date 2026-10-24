import subprocess
import sys
import tomllib
from pathlib import Path


def test_version_is_this_package():
    # In a fresh interpreter: conftest imports bpy before nodebpy, and bpy puts
    # Blender's extension site-packages, which can hold another nodebpy's
    # metadata, first on sys.path.
    code = "import nodebpy, bpy; print(nodebpy.__version__)"
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    pyproject = Path(__file__).parents[1] / "pyproject.toml"
    project = tomllib.loads(pyproject.read_text())["project"]
    assert out.stdout.splitlines()[-1] == project["version"]
