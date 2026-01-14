# SPDX-License-Identifier: GPL-3.0-or-later
"""Subprocess-based screenshot capture for headless environments.

This module launches Blender in GUI mode as a subprocess to capture screenshots
of node trees. This allows screenshots to be taken from Jupyter notebooks or
other headless Python environments.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from PIL import Image as PILImage
    import numpy as np


def find_blender_executable() -> str | None:
    """
    Find the Blender executable.

    Returns:
        Path to Blender executable, or None if not found
    """
    # Check if we're running inside Blender
    try:
        import bpy
        # If bpy is available, we can get the binary path
        binary_path = bpy.app.binary_path
        if binary_path and os.path.exists(binary_path):
            return binary_path
    except (ImportError, AttributeError):
        pass

    # Try 'which blender' on Unix-like systems
    if sys.platform != "win32":
        try:
            result = subprocess.run(
                ["which", "blender"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip()
                if os.path.exists(path):
                    return path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Check common locations
    if sys.platform == "darwin":  # macOS
        common_paths = [
            "/Applications/Blender.app/Contents/MacOS/Blender",
            "~/Applications/Blender.app/Contents/MacOS/Blender",
        ]
    elif sys.platform == "win32":  # Windows
        common_paths = [
            "C:/Program Files/Blender Foundation/Blender/blender.exe",
            "C:/Program Files/Blender Foundation/Blender 5.0/blender.exe",
            "C:/Program Files/Blender Foundation/Blender 4.2/blender.exe",
            "C:/Program Files/Blender Foundation/Blender 4.1/blender.exe",
        ]
    else:  # Linux
        common_paths = [
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "~/blender/blender",
            "/snap/bin/blender",
        ]

    for path in common_paths:
        expanded = Path(path).expanduser()
        if expanded.exists():
            return str(expanded)

    return None


def generate_screenshot_script(
    node_tree_name: str,
    output_path: str,
    blend_file: str | None = None
) -> str:
    """
    Generate a Python script that Blender will execute to take a screenshot.

    Args:
        node_tree_name: Name of the node tree to screenshot
        output_path: Path where screenshot should be saved
        blend_file: Optional .blend file to open first

    Returns:
        Python script as a string
    """
    script = f'''
import bpy
import sys

def take_screenshot():
    """Take a screenshot of the specified node tree."""

    # Open blend file if specified
    blend_file = {repr(blend_file)}
    if blend_file:
        try:
            bpy.ops.wm.open_mainfile(filepath=blend_file)
            print(f"Opened blend file: {{blend_file}}")
        except Exception as e:
            print(f"Error opening blend file: {{e}}", file=sys.stderr)
            return False

    # Find the node tree
    node_tree_name = {repr(node_tree_name)}
    if node_tree_name not in bpy.data.node_groups:
        print(f"Error: Node tree '{{node_tree_name}}' not found", file=sys.stderr)
        print(f"Available node groups: {{list(bpy.data.node_groups.keys())}}", file=sys.stderr)
        return False

    node_tree = bpy.data.node_groups[node_tree_name]
    print(f"Found node tree: {{node_tree.name}} with {{len(node_tree.nodes)}} nodes")

    # Ensure we have a window
    if not bpy.context.window_manager.windows:
        print("Error: No GUI windows available", file=sys.stderr)
        return False

    try:
        window = bpy.context.window_manager.windows[0]
        screen = window.screen

        # Find or create a node editor area
        node_editor_area = None
        for area in screen.areas:
            if area.type == 'NODE_EDITOR':
                node_editor_area = area
                break

        # If no node editor exists, convert the first area
        if not node_editor_area:
            if screen.areas:
                node_editor_area = screen.areas[0]
                node_editor_area.type = 'NODE_EDITOR'
            else:
                print("Error: No areas available", file=sys.stderr)
                return False

        # Set the node tree in the editor
        space = node_editor_area.spaces.active
        space.tree_type = 'GeometryNodeTree'
        space.node_tree = node_tree

        # Find the window region
        region = None
        for r in node_editor_area.regions:
            if r.type == 'WINDOW':
                region = r
                break

        if not region:
            print("Error: No window region found", file=sys.stderr)
            return False

        # Set up context override
        ctx = bpy.context.copy()
        ctx['window'] = window
        ctx['screen'] = screen
        ctx['area'] = node_editor_area
        ctx['region'] = region

        # Try to hide UI elements for cleaner screenshot
        # Wrap in try/except since these may fail in some contexts
        try:
            space.show_region_header = False
        except:
            pass

        try:
            space.overlay.show_context_path = False
        except:
            pass

        # Frame all nodes
        try:
            with bpy.context.temp_override(**ctx):
                bpy.ops.node.view_all()
        except Exception as e:
            print(f"Warning: Could not frame nodes: {{e}}", file=sys.stderr)

        # Give the UI a moment to update
        try:
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=2)
        except:
            pass

        # Take the screenshot
        output_path = {repr(output_path)}
        with bpy.context.temp_override(**ctx):
            bpy.ops.screen.screenshot_area(filepath=output_path)

        print(f"Screenshot saved to: {{output_path}}")
        return True

    except Exception as e:
        print(f"Error during screenshot: {{e}}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

# Execute and exit
success = take_screenshot()
sys.exit(0 if success else 1)
'''
    return script


def screenshot_node_tree_subprocess(
    tree,
    output_path: str | None = None,
    return_format: Literal['pil', 'numpy', 'path'] = 'pil',
    blender_executable: str | None = None,
    timeout: float = 30.0,
    keep_blend_file: bool = False
) -> PILImage.Image | np.ndarray | str:
    """
    Take a screenshot of a node tree by launching Blender as a subprocess.

    This function works from any Python environment, including Jupyter notebooks
    and headless servers. It launches Blender with a GUI, takes the screenshot,
    and exits.

    Args:
        tree: TreeBuilder or GeometryNodeTree to screenshot
        output_path: Where to save screenshot (temp file if None)
        return_format: 'pil' for PIL Image, 'numpy' for array, 'path' for file path
        blender_executable: Path to Blender executable (auto-detected if None)
        timeout: Maximum seconds to wait for Blender to complete
        keep_blend_file: If True, don't delete the temporary .blend file

    Returns:
        PIL Image, numpy array, or file path depending on return_format

    Raises:
        RuntimeError: If Blender executable not found or screenshot fails
        TimeoutError: If Blender takes too long

    Example:
        >>> from nodebpy import TreeBuilder, screenshot_node_tree_subprocess
        >>> with TreeBuilder("MyTree") as tree:
        ...     # build your tree
        ...     pass
        >>> img = screenshot_node_tree_subprocess(tree)
        >>> # img is a PIL Image
    """
    import bpy

    # Find Blender executable
    if blender_executable is None:
        blender_executable = find_blender_executable()
        if blender_executable is None or not blender_executable:
            raise RuntimeError(
                "Could not find Blender executable. Please specify blender_executable parameter.\n"
                "Tried:\n"
                "  - bpy.app.binary_path\n"
                "  - which blender (Unix)\n"
                "  - Common installation paths\n"
                "You can specify the path explicitly:\n"
                "  screenshot_node_tree_subprocess(tree, blender_executable='/path/to/blender')"
            )

        # Validate the executable exists
        if not os.path.exists(blender_executable):
            raise RuntimeError(
                f"Blender executable not found at: {blender_executable}\n"
                "Please specify the correct path using blender_executable parameter."
            )

        print(f"Found Blender at: {blender_executable}")

    # Check for display server on Linux
    if sys.platform == "linux":
        if not os.environ.get('DISPLAY'):
            print("\nWARNING: No DISPLAY environment variable detected.")
            print("Blender GUI requires a display server. Options:")
            print("1. Install xvfb: sudo apt-get install xvfb")
            print("2. Then set: export DISPLAY=:99")
            print("3. Or the subprocess will try to use xvfb-run automatically\n")

    # Get the node tree
    if hasattr(tree, 'tree'):
        node_tree = tree.tree
    else:
        node_tree = tree

    # IMPORTANT: Ensure the node tree has a fake user so it gets saved
    # Without this, orphaned node groups won't be saved in the blend file
    original_use_fake_user = node_tree.use_fake_user
    node_tree.use_fake_user = True

    # Ensure the current blend file is saved or create a temp one
    current_blend = bpy.data.filepath
    temp_blend = None

    try:
        if not current_blend:
            # Create a temporary blend file
            temp_blend = tempfile.NamedTemporaryFile(
                suffix='.blend',
                delete=False
            )
            temp_blend.close()
            bpy.ops.wm.save_as_mainfile(filepath=temp_blend.name)
            blend_file_path = temp_blend.name
        else:
            # Save current file
            bpy.ops.wm.save_mainfile()
            blend_file_path = current_blend
    finally:
        # Restore original fake user setting
        node_tree.use_fake_user = original_use_fake_user

    # Create output path if not specified
    temp_output_file = None
    if output_path is None:
        temp_output_file = tempfile.NamedTemporaryFile(
            suffix='.png',
            delete=False
        )
        temp_output_file.close()
        output_path = temp_output_file.name

    # Generate the screenshot script
    script_content = generate_screenshot_script(
        node_tree_name=node_tree.name,
        output_path=output_path,
        blend_file=blend_file_path
    )

    # Write script to temporary file
    temp_script = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    )
    temp_script.write(script_content)
    temp_script.close()

    try:
        # Launch Blender with the script
        # Note: NOT using --background so GUI is available for screenshots

        # Check if we should use xvfb-run (Linux without DISPLAY)
        use_xvfb = False
        if sys.platform == "linux" and not os.environ.get('DISPLAY'):
            # Try to use xvfb-run for virtual framebuffer
            try:
                result = subprocess.run(
                    ["which", "xvfb-run"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    use_xvfb = True
                    print("Using xvfb-run for virtual framebuffer")
            except:
                print("WARNING: xvfb-run not found. Blender may crash without a display server.")

        if use_xvfb:
            cmd = [
                "xvfb-run",
                "-a",  # Automatically find a free server number
                "-s", "-screen 0 1920x1080x24",  # Screen configuration
                blender_executable,
                "--window-geometry", "0", "0", "1920", "1080",
                "--python", temp_script.name
            ]
        else:
            cmd = [
                blender_executable,
                "--window-geometry", "0", "0", "1920", "1080",  # Set window size
                "--python", temp_script.name
            ]

        print(f"Launching Blender to capture screenshot...")
        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        print(f"Blender exited with code: {result.returncode}")
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")

        # Check if screenshot was created
        if result.returncode != 0:
            raise RuntimeError(
                f"Blender screenshot failed with exit code {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

        if not os.path.exists(output_path):
            raise RuntimeError(
                f"Screenshot file was not created at {output_path}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

        print(f"Screenshot captured successfully: {output_path}")

        # Return in the requested format
        if return_format == 'path':
            return output_path
        elif return_format == 'pil':
            from PIL import Image
            img = Image.open(output_path)
            img_copy = img.copy()
            img.close()
            # Clean up temp file unless path was specified
            if temp_output_file:
                os.unlink(output_path)
            return img_copy
        elif return_format == 'numpy':
            from PIL import Image
            import numpy as np
            img = Image.open(output_path)
            arr = np.array(img)
            img.close()
            # Clean up temp file unless path was specified
            if temp_output_file:
                os.unlink(output_path)
            return arr
        else:
            raise ValueError(f"Invalid return_format: {return_format}")

    finally:
        # Clean up temporary script
        if os.path.exists(temp_script.name):
            os.unlink(temp_script.name)

        # Clean up temporary blend file if created
        if temp_blend and not keep_blend_file:
            if os.path.exists(temp_blend.name):
                os.unlink(temp_blend.name)
