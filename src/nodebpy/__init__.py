from importlib.metadata import version as _version

# Before anything imports bpy, which puts Blender's extension site-packages (where
# an extension may carry its own nodebpy) ahead of this package's metadata.
__version__ = _version("nodebpy")

from . import builder, export, live, nodes, types
from .builder import (
    SIMPLE_OPTIONS,
    ArrangeMethod,
    SugiyamaOptions,
    TreeBuilder,
    arrange,
    default_keep_edits,
    default_split_inputs,
    default_sugiyama_options,
)
from .nodes import compositor, geometry, shader
from .types import Default

__all__ = [
    "SIMPLE_OPTIONS",
    "ArrangeMethod",
    "Default",
    "SugiyamaOptions",
    "TreeBuilder",
    "__version__",
    "arrange",
    "builder",
    "compositor",
    "default_keep_edits",
    "default_split_inputs",
    "default_sugiyama_options",
    "export",
    "geometry",
    "live",
    "nodes",
    "shader",
    "types",
]
