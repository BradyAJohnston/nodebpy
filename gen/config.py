"""Tree-type configuration and node-name derivation for the generator."""

from __future__ import annotations

import enum
import importlib.util
from dataclasses import dataclass
from pathlib import Path

from .customizations import _CUSTOMIZATIONS

# Repo root (gen/ lives at the top level, outside the packaged src/ tree).
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_standalone(name: str, relative_path: str):
    """Load a leaf module straight from its file, without importing the
    ``nodebpy`` package. The generator must run even when the generated tree is
    mid-refactor and temporarily un-importable, so it never imports the package
    it generates — it only reads the dependency-free ``types`` leaf."""
    spec = importlib.util.spec_from_file_location(name, _REPO_ROOT / relative_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# nodebpy.types is a leaf (only stdlib + bpy), so it loads standalone.
nodebpy_types = _load_standalone("_nodebpy_types", "src/nodebpy/types.py")
SOCKET_TYPES = nodebpy_types.SOCKET_TYPES

TREE_TYPES = ("GeometryNodeTree", "ShaderNodeTree", "CompositorNodeTree")

# Maps NodeSocket bl_idname substrings to the Python socket class used as a
# return type on output property accessors in generated node files.
# Order matters — more specific keys (e.g. "NodeSocketFloatFactor") would need
# to come before "NodeSocketFloat", but in practice all subtypes share the same
# class so substring matching on the canonical key is sufficient.
_OUTPUT_SOCKET_CLASSES: dict[str, str] = {
    "NodeSocketFloat": "FloatSocket",
    "NodeSocketVector": "VectorSocket",
    "NodeSocketColor": "ColorSocket",
    "NodeSocketInt": "IntegerSocket",
    "NodeSocketIntVector3D": "IntegerVectorSocket",
    "NodeSocketBool": "BooleanSocket",
    "NodeSocketRotation": "RotationSocket",
    "NodeSocketMatrix": "MatrixSocket",
    "NodeSocketString": "StringSocket",
    "NodeSocketMenu": "MenuSocket",
    "NodeSocketGeometry": "GeometrySocket",
    "NodeSocketObject": "ObjectSocket",
    "NodeSocketMaterial": "MaterialSocket",
    "NodeSocketImage": "ImageSocket",
    "NodeSocketCollection": "CollectionSocket",
    "NodeSocketBundle": "BundleSocket",
    "NodeSocketClosure": "ClosureSocket",
    "NodeSocketShader": "ShaderSocket",
    "NodeSocketFont": "FontSocket",
    "NodeSocketSound": "SoundSocket",
}


class Disposition(enum.Enum):
    """How the generator should treat a given Blender node type."""

    SKIP = "skip"  # not exported at all
    MANUAL = "manual"  # hand-written in manual.py / zone.py
    GENERATE = "generate"  # auto-generated (possibly with a customization)


def class_name_for(display_name: str, bl_idname: str, config: TreeTypeConfig) -> str:
    """Derive the Python class name for a node from its Blender display name.

    A registered customization may pin the public API name when it differs from
    the display name (e.g. ``FieldMinAndMax`` vs Blender's "Field Min Max").
    """
    custom = _CUSTOMIZATIONS.get(bl_idname)
    if custom and custom.class_name:
        return custom.class_name

    class_name = display_name.replace("_", " ").replace("-", " ")
    class_name = "".join(c if c.isalnum() or c.isspace() else "" for c in class_name)
    class_name = class_name.title().replace(" ", "")

    replacements = {
        "&": "And",
        "Uv": "UV",
        "Sdf": "SDF",
        "Rgb": "RGB",
        "3DCursor": "Cursor3D",
        "Xyz": "XYZ",
        "Id": "ID",
        "Bézier": "Bezier",
        "ImportStl": "ImportSTL",
        "ImportObj": "ImportOBJ",
        "ImportCsv": "ImportCSV",
        "ImportPly": "ImportPLY",
        "Vdb": "VDB",
        "3DLocation": "Location3D",
        "Bsdf": "BSDF",
        "Svd": "SVD",
        "Bw": "BW",
    }
    for prefix in config.class_name_prefix_strips:
        replacements[prefix] = ""
    for key, value in replacements.items():
        class_name = class_name.replace(key, value)
    return class_name


@dataclass
class TreeTypeConfig:
    """Configuration for generating node classes for a specific tree type."""

    tree_type: str  # e.g. "GeometryNodeTree"
    output_dir_name: str  # e.g. "geometry"
    nodes_to_skip: list[str]
    manually_defined: tuple[str, ...]
    # Prefixes stripped from bl_idname when generating Python class names.
    # Order matters – longer/more-specific prefixes first.
    class_name_prefix_strips: list[str]

    @property
    def output_dir(self) -> Path:
        return _REPO_ROOT / f"src/nodebpy/nodes/{self.output_dir_name}/"

    def disposition(self, node_type: type) -> Disposition:
        """Decide how a Blender node type should be handled for this tree.

        The single source of truth for the skip / hand-written / generate
        decision, shared by the generation loop and the re-export registry so
        they can never disagree.
        """
        name = node_type.__name__
        rna_name = node_type.bl_rna.name
        # MANUAL wins over SKIP: some nodes match a skip substring *and* are
        # hand-written + re-exported (e.g. "Simulation" is skipped, but the
        # SimulationInput/Output/Zone classes live in zone.py). Matched via the
        # *same* class-name derivation used for generation so the two can't drift
        # (an ad-hoc title()-based match used to miss names needing replacements
        # like UV/RGB/&→And).
        if class_name_for(rna_name, name, self) in self.manually_defined:
            return Disposition.MANUAL
        if any(s in name for s in self.nodes_to_skip) or any(
            s in rna_name for s in self.nodes_to_skip
        ):
            return Disposition.SKIP
        return Disposition.GENERATE


GEOMETRY_CONFIG = TreeTypeConfig(
    tree_type="GeometryNodeTree",
    output_dir_name="geometry",
    nodes_to_skip=[
        "AlignEulerToVector",
        "Legacy",
        "Simulation",
        "For Each",
        "GridBoolean",
    ],
    manually_defined=(
        "IndexSwitch",
        "MenuSwitch",
        "CaptureAttribute",
        "FieldToGrid",
        "JoinGeometry",
        "SDFGridBoolean",
        "JoinStrings",
        "GeometryToInstance",
        "RepeatInput",
        "RepeatOutput",
        "RepeatZone",
        "SimulationInput",
        "SimulationOutput",
        "SimulationZone",
        "ForEachGeometryElementInput",
        "ForEachGeometryElementOutput",
        "ForEachGeometryElementZone",
        "EvaluateClosure",
        "ClosureInput",
        "ClosureOutput",
        "ClosureZone",
        "JoinStrings",
        "Menu",
        "Collection",
        "Material",
        "Object",
        "Value",
        "MeshBoolean",
        "Compare",
        "Mix",
        "AttributeStatistic",
        "SampleIndex",
        "IntegerVector",
        "SampleCurve",
        "Frame",
        "Float",
        "FloatCurve",
        "ColorRamp",
        "StoreNamedAttribute",
        "tree",
    ),
    class_name_prefix_strips=[
        "GeometryNode",
        "ShaderMath",
        "FunctionNode",
        "Node",
    ],
)

SHADER_CONFIG = TreeTypeConfig(
    tree_type="ShaderNodeTree",
    output_dir_name="shader",
    nodes_to_skip=[
        "Legacy",
    ],
    manually_defined=(
        "MenuSwitch",
        "RepeatInput",
        "RepeatOutput",
        "RepeatZone",
        "Attribute",
        "Frame",
        "tree",
        "Float",
        "material",
    ),
    class_name_prefix_strips=[
        "ShaderNode",
        "Node",
    ],
)

COMPOSITOR_CONFIG = TreeTypeConfig(
    tree_type="CompositorNodeTree",
    output_dir_name="compositor",
    nodes_to_skip=[
        "Legacy",
    ],
    manually_defined=(
        "MenuSwitch",
        "Frame",
        "tree",
        "Float",
        "Image",
        "Cryptomatte",
        "ConvertColorspace",
    ),
    class_name_prefix_strips=[
        "CompositorNode",
        "Node",
    ],
)

ALL_CONFIGS = [GEOMETRY_CONFIG, SHADER_CONFIG, COMPOSITOR_CONFIG]
