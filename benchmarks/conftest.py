import sys
from pathlib import Path

import bpy
import pytest

# Importing bpy can put Blender's extensions site-packages ahead of the repo on
# sys.path; force the repo's src back to the front so the code under test wins.
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

STARTUP = Path(__file__).parent.parent / "tests" / "data" / "test_startup.blend"


@pytest.fixture(autouse=True)
def clean_file():
    """Start every benchmark from the same clean Blender file."""
    bpy.ops.wm.read_homefile(filepath=str(STARTUP))
    yield
