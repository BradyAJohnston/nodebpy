"""``nodebpy run`` / :func:`nodebpy.report.run`: build a script's trees and
report them in a few lines."""

import textwrap

import bpy
import pytest

from nodebpy.__main__ import main
from nodebpy.report import run


def _script(tmp_path, name, source):
    path = tmp_path / name
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


SCATTER = """
    from nodebpy import geometry as g
    from nodebpy import shader as s

    with s.material("Report Gold", clear=True) as gold:
        s.PrincipledBSDF(metallic=1.0) >> s.MaterialOutput()

    with g.tree("Report Scatter", clear=True, is_modifier=True) as tree:
        count = tree.inputs.integer("Count", 5, min_value=0)
        (
            g.Points(count, position=g.RandomValue.vector(min=-1))
            >> g.InstanceOnPoints(instance=g.Cube(size=0.1))
            >> g.SetMaterial(material=gold.material)
            >> tree.outputs.geometry("Geometry")
        )
"""


def test_report_lists_trees_and_the_evaluated_geometry(tmp_path):
    report = run(
        _script(tmp_path, "scatter.py", SCATTER), object="Report Target", echo=False
    )
    assert report.ok
    lines = report.text.splitlines()
    assert lines[0] == "built material 'Report Gold': 2 nodes, 1 link"
    assert lines[1].startswith("built 'Report Scatter' (geometry, modifier): 7 nodes")
    assert "in (Count: Int = 5) -> out (Geometry: Geometry)" in lines[1]
    assert lines[2] == "object 'Report Target' (Report Scatter): 5 instances"
    assert lines[3].startswith("  bounds (")
    low, high = (
        [float(v) for v in part.strip("()").split(", ")]
        for part in lines[3].removeprefix("  bounds ").split("..")
    )
    assert all(-1 <= lo <= hi <= 1 for lo, hi in zip(low, high))
    # the object was created and carries the tree
    assert bpy.data.objects["Report Target"].modifiers[0].node_group.name == (
        "Report Scatter"
    )


def test_errors_report_the_failing_line_and_no_half_built_tree(tmp_path):
    path = _script(
        tmp_path,
        "broken.py",
        """
        from nodebpy import geometry as g

        with g.tree("Report Broken", clear=True) as tree:
            g.Math(operation="SUBSTRACT") >> tree.outputs.float("Value")
        """,
    )
    report = run(path, object="Report Target", echo=False)
    assert not report.ok
    first, at = report.text.splitlines()[:2]
    assert first.startswith(
        "ERROR TypeError: Math's operation has no option 'SUBSTRACT'"
    )
    assert (
        at
        == '  at broken.py:5: g.Math(operation="SUBSTRACT") >> tree.outputs.float("Value")'
    )
    assert "built" not in report.text
    assert "Traceback" not in report.text
    assert "Traceback" in run(path, traceback=True, echo=False).text


def test_node_warnings_and_mesh_counts(tmp_path):
    path = _script(
        tmp_path,
        "warn.py",
        """
        from nodebpy import geometry as g

        with g.tree("Report Warn", clear=True, is_modifier=True) as tree:
            g.Points(4) >> g.ExtrudeMesh() >> tree.outputs.geometry("Geometry")
        with g.tree("Report Mesh", clear=True, is_modifier=True) as tree:
            g.Cube() >> tree.outputs.geometry("Geometry")
        """,
    )
    warned = run(path, object="Report Target", tree="Report Warn", echo=False)
    assert "object 'Report Target' (Report Warn): 4 points" in warned.text
    assert "  info: Input geometry has unsupported type: Point Cloud" in warned.text
    meshed = run(path, object="Report Target", echo=False)  # the last tree
    assert "(Report Mesh): mesh 8 vertices, 6 faces" in meshed.text
    assert "bounds (-0.5, -0.5, -0.5)..(0.5, 0.5, 0.5)" in meshed.text


def test_frame_steps_simulations(tmp_path):
    path = _script(
        tmp_path,
        "fall.py",
        """
        from nodebpy import geometry as g

        with g.tree("Report Fall", clear=True, is_modifier=True) as tree:
            sim = g.SimulationZone()
            geo = sim.items.geometry(g.Points(1), "Geometry")
            geo.current >> g.SetPosition(offset=(0, 0, -1)) >> geo.next
            geo.result >> tree.outputs.geometry("Geometry")
        """,
    )
    report = run(path, object="Report Faller", frame=5, echo=False)
    bounds = report.text.splitlines()[-1]
    # the zone runs once per frame, the first included
    assert bounds == "  bounds (0, 0, -5)..(0, 0, -5)"


def test_group_classes_and_reruns(tmp_path):
    path = _script(
        tmp_path,
        "groups.py",
        """
        from nodebpy import geometry as g
        from nodebpy.builder import CustomGeometryGroup


        class ReportLift(CustomGeometryGroup):
            _name = "Report Lift"

            def _build_group(self, tree):
                geometry = tree.inputs.geometry("Geometry")
                geometry >> g.SetPosition(offset=(0, 0, 1)) >> tree.outputs.geometry("Geometry")


        with g.tree("Report Uses Lift", clear=True, is_modifier=True) as tree:
            g.Cube() >> ReportLift() >> tree.outputs.geometry("Geometry")
        """,
    )
    first = run(path, object="Report Target", echo=False)
    assert "built 'Report Lift' (geometry)" in first.text
    assert "(Report Uses Lift): mesh 8 vertices" in first.text
    groups = len(bpy.data.node_groups)
    again = run(path, object="Report Target", echo=False)  # rebuilt, not duplicated
    assert again.ok and len(bpy.data.node_groups) == groups


def test_cli_exit_code(tmp_path, capsys):
    good = _script(tmp_path, "good.py", SCATTER)
    with pytest.raises(SystemExit) as exit_info:
        main(["run", str(good)])
    assert exit_info.value.code == 0
    assert "built 'Report Scatter'" in capsys.readouterr().out
    bad = _script(tmp_path, "bad.py", "import nodebpy\nraise ValueError('nope')\n")
    with pytest.raises(SystemExit) as exit_info:
        main(["run", str(bad)])
    assert exit_info.value.code == 1
    assert "ERROR ValueError: nope" in capsys.readouterr().out


def test_interface_defaults_worlds_and_curves(tmp_path):
    path = _script(
        tmp_path,
        "mixed.py",
        """
        import bpy
        from nodebpy import geometry as g
        from nodebpy import shader as s

        steel = bpy.data.materials.get("Report Steel") or bpy.data.materials.new("Report Steel")
        with s.world("Report Sky", clear=True):
            s.Background() >> s.WorldOutput()
        with g.tree("Report Curve", clear=True, is_modifier=True) as tree:
            length = tree.inputs.float("Length", 2.0)
            tree.inputs.vector("Offset", (0.0, 0.0, 1.0))
            tree.inputs.material("Material", steel)
            g.CurveLine(end=g.CombineXYZ(z=length)) >> tree.outputs.geometry("Curve")
        """,
    )
    report = run(path, object="Report Curves", echo=False)
    assert str(report) == report.text
    assert "built world 'Report Sky': 2 nodes, 1 link" in report.text
    assert (
        "in (Length: Float = 2.0, Offset: Vector = (0.0, 0.0, 1.0), "
        "Material: Material = 'Report Steel')"
    ) in report.text
    assert "(Report Curve): 1 curve (2 points)" in report.text
    assert "bounds (0, 0, 0)..(0, 0, 2)" in report.text


def test_object_problems_are_reported(tmp_path):
    shader_only = _script(
        tmp_path,
        "shader_only.py",
        """
        from nodebpy import shader as s

        with s.material("Report Only", clear=True):
            s.PrincipledBSDF() >> s.MaterialOutput()
        """,
    )
    report = run(shader_only, object="Report Target", echo=False)
    assert not report.ok
    assert "ERROR ValueError: the script built no geometry tree" in report.text
    missing = run(shader_only, object="Report Target", tree="No Such Tree", echo=False)
    assert "ERROR KeyError" in missing.text
    empty = run(_script(tmp_path, "empty.py", "import nodebpy\n"), echo=False)
    assert empty.ok and empty.text == "built no trees"


def test_empty_geometry_has_no_bounds(tmp_path):
    path = _script(
        tmp_path,
        "nothing.py",
        """
        from nodebpy import geometry as g

        with g.tree("Report Nothing", clear=True, is_modifier=True) as tree:
            tree.outputs.geometry("Geometry")
        """,
    )
    report = run(path, object="Report Target", echo=False)
    assert (
        report.text.splitlines()[-1] == "object 'Report Target' (Report Nothing): empty"
    )


def test_cli_opens_a_blend_first(tmp_path, capsys):
    blend = tmp_path / "start.blend"
    bpy.data.objects.new("Report Saved", bpy.data.meshes.new("Report Saved"))
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), copy=True)
    script = _script(
        tmp_path,
        "check.py",
        """
        import bpy
        print("opened:", bpy.data.filepath.endswith("start.blend"))
        """,
    )
    with pytest.raises(SystemExit):
        main(["run", str(script), "--blend", str(blend)])
    assert "opened: True" in capsys.readouterr().out
