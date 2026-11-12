# Contributing

## Setup

```sh
uv sync --all-extras --dev
git config core.hooksPath .githooks
```

The second command activates the shared pre-commit hook, which runs format, lint, and type-check before every commit.

## Running tests

Tests run using `bpy` installed from pip (no need for Blender on `PATH`)

```sh
uv run pytest -n 4
```

### On the previous Blender

The node classes are generated from one Blender (`nodes/_blender.py` records which), and also run on the one before it. There, constructing a node that Blender lacks, setting one of its options or an input it lacks to anything but the constructor's default, or linking a bundled asset it lacks raises `NodeUnavailableError`, naming the Blender needed; an input the node lacks, left at its default, is skipped. CI runs the suite against that Blender too (`tests-5.2.yml`): a test that hits `NodeUnavailableError` is skipped there, and a test of the newer Blender's behaviour on a node both have is marked `@pytest.mark.generated_blender`. To run it locally:

```sh
uv pip install --python .venv "bpy==5.2.*" && uv run --no-sync pytest -n 4
uv sync --all-extras    # back to the locked bpy
```

## The agent skill

`src/nodebpy/skills/nodebpy/` is the source of the agent skill and ships in the wheel;
`skills/nodebpy/` at the repository root is the copy that `npx skills add` and the
Claude Code marketplace (`.claude-plugin/`) read. After editing the source, run
`make skills` to refresh the copy; a test fails when the two differ. Keep the skill
in step with API changes in the same pull request, since it is what agents rely on for
the current argument orders and method names: `SKILL.md` holds the loop, the core
idioms and the errors table, and `references/` one file per task. `test_skill.py` runs
every Python block in it against the package, so an outdated example fails the tests.

## Regenerating node classes

Most node classes under `src/nodebpy/nodes/` are auto-generated from Blender's live node registry by the `gen/` package (kept outside `src/` so it never ships in the wheel). After a Blender / `bpy` version change, regenerate with:

```sh
make generate
```

which runs, in order:

1. `uv run python -m gen` — regenerates the typed classes for Blender's bundled essentials asset libraries, then the node classes for every tree type
2. `make format` — `ruff format`, `ruff check --fix`, and `ty check --fix src`
3. `uv run python -m gen.math_stub` — regenerates the typed overloads for `nodebpy.math` (it imports `nodebpy`, so it runs after the fixes)

CI regenerates on every pull request and fails when the checked-in classes differ from the generator's output, so a change to `gen/` ships with its regenerated classes. The generator imports the project's own `nodebpy` before `bpy`: Blender puts its extensions' site-packages first on the path when `bpy` loads, and a `nodebpy` installed there would otherwise shadow the sources being generated.

For faster iteration you can regenerate a single tree type:

```sh
uv run python -m gen --only geometry
```

(Geometry is always processed first because the shader and compositor trees re-export shared nodes from it.)

Inside `gen/`: `config.py` holds the per-tree-type configuration and the skip / hand-written / generate disposition for each node, `customizations.py` is the `register_customization` registry that layers generation-time mixins onto specific nodes, `introspect.py` inspects the live node registry, and `model.py` / `emit.py` / `writers.py` turn the results into module files.

The socket *draw order* table `src/nodebpy/builder/_socket_order.py` is generated separately, from Blender's C++ node declarations rather than the live registry: Blender draws nodes declared with `use_custom_socket_order()` in declaration order (inputs and outputs interleaved, aligned pairs sharing a row, buttons and panels where declared), which RNA does not expose. After a Blender version change regenerate it with

```sh
uv run python -m gen.socket_order            # sparse-clones the tag matching the installed bpy
uv run python -m gen.socket_order --source ~/src/blender   # or parse a local checkout
```

The typed overloads for `nodebpy.math` (`src/nodebpy/math.pyi`) are generated from its `_SPECS` table. `make generate` rebuilds them; after editing the table run

```sh
uv run python -m gen.math_stub
```

`tests/test_node_math.py` fails while the stub is stale.

Nodes that need special handling are hand-written in `src/nodebpy/nodes/*/manual.py` (and the zone nodes in `nodes/geometry/zone.py` / `nodes/shader/zone.py`); the generator skips these and re-exports them alongside the generated classes.

## Changing the public API

Other packages and many scripts build on nodebpy, so a script written against one release should keep running on the next, warning before anything it uses goes away.

**What is public:** every name without a leading underscore that can be reached from `nodebpy`. That includes the generated node classes, their constructor and factory parameters (by name *and* position), their `i.<name>` / `o.<name>` socket attributes, socket methods, and the `nodebpy` command. The code `to_python` writes is public too: it ends up in users' files.

**Versions:** `XYZ.minor.patch`, where `XYZ` is the Blender line (`530` is Blender 5.3).

- Within a line, nothing public is removed or renamed without a deprecation that keeps the old spelling working. Additions are fine.
- Deprecated names are removed in the first release of the next line (`540.0.0`), never in between.
- The previous line's branch (`5.2` while `main` is 5.3) takes bug fixes only: no deprecations and no removals.
- When Blender changes something and no shim is possible, the release notes list it under **breaking**, with the replacement.

### Deprecating hand-written API

Keep the old name working by forwarding to the new one, and warn with `_deprecated` from `nodebpy.builder._utils`:

```python
# -- deprecated entry points, removed in 540 --


def add_item(self, name: str, value: Any = None) -> Item:
    """Deprecated: use ``items.new(value, name)``."""
    _deprecated("add_item(name, value)", "items.new(value, name)", removed_in=540)
    return self.items.new(value, name)
```

- **Warning:** `removed_in` is the next Blender line. The warning points at the first frame outside nodebpy, so users see their own line.
- **Renamed keyword:** keep the old one as a keyword-only parameter defaulting to `None`. Warn when it's given and pass it on under the new name.
- **CLI entry points:** warn with `FutureWarning` instead. Python hides `DeprecationWarning` unless it's attributed to `__main__`, and a command has no user frame to attribute it to.
- **Grouping:** put shims under a `# -- deprecated ..., removed in 540 --` comment and start their docstring with "Deprecated: use ...". Then `grep -rn "removed in 540\|removed_in=540" src gen` finds all of them at removal time.
- **Test:** test that the old spelling warns *and* still does what it did.
- **Changelog:** add a `### Deprecations` entry naming the replacement and the removal version.
- **Replacement spelling everywhere:** `to_python` must never emit a deprecated spelling. Move the docs, examples and agent skill (`src/nodebpy/skills/`) to the new spelling in the same pull request. `test_skill.py` doesn't catch a deprecated example, because it still runs.

### Generated API

Regenerating can change public names without anyone editing them. For example, Blender renames a socket or an enum item, moves a property to a menu socket, adds an input ahead of existing ones, or gives two inputs the same name. After every `make generate` for a new Blender version, and before every release, compare against the last release tag:

```sh
uv run python -m gen.api_diff v530.0.0
```

It lists every public class, method, parameter, socket attribute and `Literal` value that is gone, and every positional slot that now takes a different argument. It exits 1 when it finds anything. Every line needs one of the following:

Generated signatures follow Blender: parameters take Blender's socket order and the values Blender takes now, even when that breaks positional calls. Shims keep the old *spellings* working, with a warning:

- **An enum property became a menu socket:** register `legacy_menu_customization(...)` in `gen/customizations.py` (Merge Layers is the example). It reads the old values from the deprecated property Blender keeps alongside the socket. With it, the old values still work as the socket's argument, and the old property and the factories you list come back as deprecated shims. It raises when Blender drops that property.
- **Any other factory, method or property is gone:** add it back as a shim through `register_customization` in `gen/customizations.py`:

  ```python
  register_customization(
      NodeCustomization(
          bl_idname="GeometryNodeExample",
          imports=("from ...builder._utils import _deprecated",),
          extra_body='''
      @classmethod
      def by_name(cls, *args, **kwargs):
          """Deprecated: use ``Example(..., mode="Name")``."""
          _deprecated("Example.by_name()", 'Example(mode="Name")', removed_in=540)
          return cls(*args, mode="Name", **kwargs)''',
      )
  )
  ```

- **A parameter is renamed:** a mixin can't intercept the old keyword, because the generated method is defined on the class itself. Release 530 removed the general mechanism for this. It was a `_renamed_params` table the generator wrote per class, plus `BaseNode.__init_subclass__` wrapping each listed method so the old keyword still works with a warning (#273, `67a99552`). Restore it from there rather than writing per-node overrides.
- **An `i.` / `o.` socket attribute is renamed, or positional parameters change order:** there's no shim. List it as breaking in the changelog. If Blender only relabelled the socket and kept its identifier, the old attribute still resolves (Import PLY's `o.mesh`), and the generator says so in the socket's docstring (`gen.util.former_name`).
- **An input is GPU-only:** Blender declares some inputs `.available(is_gpu_internal)` (the shaders' `Weight`). `gen.socket_order` records them in `INTERNAL_SOCKETS`, and the generator leaves them out.
- **A name falls back to a socket identifier** (`input_14`, `socket_1`): two sockets share a display name. Fix the naming instead of shipping it.
- **A node Blender deprecates:** it stays and warns on construction through `_DeprecatedNodeMixin` (see Rotate Euler in `gen/customizations.py`). Remove it when Blender removes the node.

### Removing at the next Blender line

On the new line's branch, delete everything marked `removed in <line>` / `removed_in=<line>`, along with its tests. List the removals under `### Removals` in the changelog with their replacements. Then run `gen.api_diff` against the previous line's last release and check that it lists only what you meant to remove.

## Building the docs

The documentation is a [Quarto](https://quarto.org) site under `docs/`, with the API reference generated by `quartodoc`:

```sh
make docs
```

### A note on `bpy` shadowing the repo package

Importing the pip `bpy` module prepends Blender's user extension site-packages
(`~/.config/blender/<ver>/extensions/.local/...`) to `sys.path`. If a Blender
extension bundles its own `nodebpy` wheel (MolecularNodes does), any process
that imports `bpy` *before* `nodebpy` will silently import that bundled copy
instead of the code in this repo — typically surfacing as `AttributeError`s
for APIs that exist in your working tree but not in the released wheel.

Two places already guard against this: `tests/conftest.py` re-inserts the
repo's `src/` at the front of `sys.path`, and `docs/_environment` points
`BLENDER_USER_EXTENSIONS` / `BLENDER_USER_SCRIPTS` at nonexistent stubs so
Quarto's render kernels never see the extension packages. For ad-hoc scripts,
either import `nodebpy` before `bpy` or run with the same environment
variables:

```sh
BLENDER_USER_EXTENSIONS=/nonexistent uv run python my_script.py
```

## CI

These GitHub Actions workflows run on every push and pull request:

- **lint.yml** — ruff format check, ruff check, ty check (Ubuntu only, platform-independent)
- **tests-5.2.yml** / **tests-5.3.yml** — pytest on macOS, Windows, and Ubuntu against each supported Blender, through the reusable `_tests.yml`; each has a badge in the README's table, per branch (`main` is 530, `5.2` is 520)
