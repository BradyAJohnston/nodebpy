---
name: cli-mainfile-test-teardown
description: Tests that open/save/read .blend mainfiles must restore the home file in a finally block
metadata:
  type: feedback
---

Tests that call `bpy.ops.wm.open_mainfile` / `read_factory_settings` / `save_as_mainfile` (e.g. the `nodebpy` CLI tests in `tests/test_cli.py`) must reload the test home file in a `finally`:

```python
bpy.ops.wm.read_homefile(filepath=str(Path(__file__).parent / "data/test_startup.blend"))
```

**Why:** the autouse `clean_and_save` fixture in `tests/conftest.py` teardown references `bpy.data.objects["Cube"]` and `bpy.data.materials["Material"]` to stash node groups before saving. If a test replaced the active file, those datablocks are gone and teardown raises `KeyError`.

**How to apply:** wrap any mainfile-mutating test body in `try/finally` and restore the startup home file at the end. Relates to the `nodebpy` CLI ([[MEMORY]] Codegen section): `export` opens a .blend → `to_python(top_level="class")` merged into one module; `build` imports the module, calls `NodeGroupBuilder.create_asset()`, saves.
