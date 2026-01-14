

# nodebpy

[![Run
Tests](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml/badge.svg)](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml)
[![](https://codecov.io/gh/BradyAJohnston/nodebpy/graph/badge.svg?token=buThDQZUED)](https://codecov.io/gh/BradyAJohnston/nodebpy)

A package to help build node trees in blender more elegantly with python
code.

## The Design Idea

Other projects have attempted similar but none quite handled the API how
I felt it should be done. Notable existing projects are
[geometry-script](https://github.com/carson-katri/geometry-script),
[geonodes](https://github.com/al1brn/geonodes),
[NodeToPython](https://github.com/BrendanParmer/NodeToPython).

Other projects implement chaining of nodes mostly as dot methos of nodes
to chain them (`InstanceOnPoints().set_position()`). This has the
potential to crowd the API for individual nodes and easy chaining is
instead approached via overriding the `>>` operator.

### Chain Nodes with `>>`

By default the operator attempts to link the first output of the
previous node with the first input of the next. You can override this
behaviour by being explicit with the socket you are passing out
(`AccumulateField().o_total`) or using the `...` for the inputs into the
next node. The dots can appear at multiple locations and each input will
be linked to the previous node via the inferred or specified socket.

# Example Node Tree

``` python
import bpy
from nodebpy import TreeBuilder, NodeTreeDisplay, nodes as n, sockets as s

bpy.ops.wm.read_homefile()

with TreeBuilder("AnotherTree") as tree:
    tree.interface(
        inputs=[s.SocketInt("Count")],
        outputs=[s.SocketGeometry("Instances")],
    )

    rotation = (
        n.RandomValue.vector(min=(-1, -1, -1), seed=2)
        >> n.AlignRotationToVector()
        >> n.RotateRotation(
            rotate_by=n.AxisAngleToRotation(angle=0.3), rotation_space="LOCAL"
        )
    )

    _ = (
        tree.inputs.count
        >> n.Points(position=n.RandomValue.vector(min=(-1, -1, -1)))
        >> n.InstanceOnPoints(instance=n.Cube(), rotation=rotation)
        >> n.SetPosition(
            position=n.Position() * 2.0 + (0, 0.2, 0.3),
            offset=(0, 0, 0.1),
        )
        >> n.RealizeInstances()
        >> n.InstanceOnPoints(n.Cube(), instance=...)
        >> tree.outputs.instances
    )

NodeTreeDisplay(tree)
```

    Found Blender at: /usr/bin/blender
    Info: Saved as "tmpbn8wrkx0.blend"
    Launching Blender to capture screenshot...
    Command: /usr/bin/blender --window-geometry 0 0 1920 1080 --python /tmp/tmpa_iwflsa.py
    Blender exited with code: -11
    stdout: 00:02.934  blend            | Read blend: "/tmp/tmpbn8wrkx0.blend"
    Writing: /tmp/tmpbn8wrkx0.crash.txt

    Screenshot failed: Blender screenshot failed with exit code -11
    stdout: 00:02.934  blend            | Read blend: "/tmp/tmpbn8wrkx0.blend"
    Writing: /tmp/tmpbn8wrkx0.crash.txt

    stderr: 
    Check that Blender is installed and accessible.

    <NodeTreeDisplay: 'AnotherTree' with 17 nodes>

<!-- ![](images/paste-2.png) -->

# Design Considerations

Whenever possible, support IDE auto-complete and have useful types. We
should know as much ahead of time as possible if our network will
actually build.

- Stick as closely to Geometry Nodes naming as possible
  - `RandomValue` creates a random value node
    - `RandomValue.vector()` creates it set to `"VECTOR"` data type and
      provides arguments for IDE auto-complete
- Inputs and outputs from a node are prefixed with `i_*` and `o_`:
  - `AccumulateField().o_total` returns the output `Total` socket
  - `AccumulateField().i_value` returns the input `Value` socket
- If inputs are subject to change depending on enums, provide separate
  constructor methods that provide related inputs as arguments. There
  should be no guessing involved and IDEs should provide documentation
  for what is required:
  - `TransformGeometry.matrix(CombineTrasnsform(translation=(0, 0, 1))`
  - `TransformGeoemtry.components(translation=(0, 0, 1))`
  - `TransformGeometry(translation=(0, 0, 1))`

# Jupyter Notebook Integration

Install with Jupyter support:

``` bash
pip install nodebpy[jupyter]
```

You can automatically capture and display screenshots of your node trees
in Jupyter notebooks.

## How It Works

Screenshots work in two modes:

1.  **Direct Mode** (GUI available): Fast, captures from the current
    Blender window
2.  **Subprocess Mode** (Headless/Jupyter): Launches Blender in GUI
    mode, captures screenshot, exits

The mode is automatically detected - no configuration needed!

## Method 1: Explicit Screenshot

``` python
from nodebpy import screenshot_node_tree, TreeBuilder
from IPython.display import display

# Build your node tree
with TreeBuilder("MyTree") as tree:
    # ... create nodes ...
    pass

# Capture and display screenshot (auto-detects mode)
img = screenshot_node_tree(tree=tree, return_format='pil')
display(img)
```

## Method 2: Auto-Display Wrapper

``` python
from nodebpy import NodeTreeDisplay, TreeBuilder, nodes as n

# Use NodeTreeDisplay wrapper for automatic display
with NodeTreeDisplay(TreeBuilder("MyTree")) as tree:
    # Build your tree
    tree.inputs.geometry >> n.SetPosition() >> tree.outputs.geometry

# Simply evaluate the tree object to see the screenshot
tree  # Automatically displays the node tree screenshot in Jupyter
```

## Method 3: Save to File

``` python
from nodebpy import save_node_tree_screenshot
save_node_tree_screenshot('/tmp/my_tree.png', tree=tree)
```

## Advanced: Force Subprocess Mode

If you want to explicitly use subprocess mode (e.g., for consistent
behavior):

``` python
img = screenshot_node_tree(
    tree=tree,
    use_subprocess=True,
    blender_executable="/path/to/blender",  # Optional, auto-detected
    timeout=30.0  # Timeout in seconds
)
```

## Technical Details

**Direct Mode:** - Captures tiles of the node editor view - Stitches
them together into a single image - Very fast, requires existing Blender
GUI

**Subprocess Mode:** - Saves current .blend file - Launches Blender with
GUI as subprocess - Blender opens file, captures screenshot, exits -
Slower (~5-10 seconds) but works everywhere - Automatically cleans up
temporary files
