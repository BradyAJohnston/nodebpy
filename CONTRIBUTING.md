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

## Regenerating node classes

Most node classes under `src/nodebpy/nodes/` are auto-generated from Blender's live node registry. After a Blender / `bpy` version change, regenerate with:

```sh
uv run generate.py && uvx ruff format && uvx ruff check --fix && uvx ty check --fix src
```

The pre-commit hook runs all three format and typing checks automatically. If `ty check` reports errors, the commit is blocked until they are resolved.

## CI

Two GitHub Actions workflows run on every push and pull request:

- **lint.yml** — ruff format check, ruff check, ty check (Ubuntu only, platform-independent)
- **tests.yml** — pytest on macOS, Windows, and Ubuntu
