#!/usr/bin/env python3

import re
import os


def extract_class_names(file_path):
    """Extract all class names from a Python file."""
    with open(file_path, "r") as f:
        content = f.read()

    # Find all class definitions
    class_pattern = r"^class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
    matches = re.findall(class_pattern, content, re.MULTILINE)
    return sorted(matches)


def generate_explicit_imports():
    """Generate explicit import statements for all node modules."""
    modules = [
        "manually_specified",
        "attribute",
        "curve",
        "geometry",
        "input",
        "mesh",
        "utilities",
    ]

    nodes_dir = "src/nodebpy/nodes"
    all_imports = []

    all_imports.append('"""Auto-generated geometry node classes."""')
    all_imports.append("")

    for module in modules:
        file_path = os.path.join(nodes_dir, f"{module}.py")
        if os.path.exists(file_path):
            class_names = extract_class_names(file_path)
            if class_names:
                all_imports.append(f"# Import from {module}")

                # Split into chunks of 5 for readability
                for i in range(0, len(class_names), 5):
                    chunk = class_names[i : i + 5]
                    if i == 0:
                        all_imports.append(f"from .{module} import (")
                    else:
                        all_imports.append("    ")

                    formatted_chunk = ", ".join(chunk)
                    if i + 5 >= len(class_names):  # Last chunk
                        all_imports.append(f"    {formatted_chunk}")
                        all_imports.append(")")
                    else:
                        all_imports.append(f"    {formatted_chunk},")

                all_imports.append("")

    return "\n".join(all_imports)


if __name__ == "__main__":
    result = generate_explicit_imports()
    print(result)
