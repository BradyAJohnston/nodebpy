"""Items on the Viewer, File Output and Raycast nodes, and their export."""

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.export import to_python


def _links(tree):
    return sorted(
        (link.from_node.bl_idname, link.from_socket.name, link.to_socket.name)
        for link in tree.links
    )


def _round_trip(tree):
    code = to_python(tree, format=False)
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    assert _links(namespace["tree"].tree) == _links(tree.tree), code
    return code


def test_viewer_items():
    with g.tree() as tree:
        viewer = g.Viewer(domain="POINT")
        height = viewer.items.float(g.Position().o.position.z, "Height")
        viewer.items.geometry(g.Cube())
        viewer.items.integer(name="Unlinked")
    assert [(i.name, i.input.socket.type) for i in viewer.items] == [
        ("Height", "VALUE"),
        ("Mesh", "GEOMETRY"),
        ("Unlinked", "INT"),
    ]
    assert height.input.socket.links
    code = _round_trip(tree)
    assert 'viewer.items.float(g.Position().o.position.z, "Height")' in code
    assert 'g.Viewer(domain="POINT")' in code


def test_file_output_items():
    with c.tree() as tree:
        image = tree.inputs.color("Image")
        output = c.FileOutput(directory="//renders/")
        output.items.color(image, "Beauty")
        output.items.float(c.Value(), "Depth")
    assert [(i.name, i.input.socket.type) for i in output.items] == [
        ("Beauty", "RGBA"),
        ("Depth", "VALUE"),
    ]
    code = _round_trip(tree)
    assert 'file_output.items.color(image, "Beauty")' in code


def test_raycast_samples_attributes_by_name():
    with s.tree() as tree:
        ray = s.Raycast(length=5.0)
        height = ray.items.float("height")
        color = ray.items.color("Col", "Colour")
        height.output >> tree.outputs.float("Height")
        ray.o["Colour Alpha"] >> tree.outputs.float("Alpha")
    # the input is the attribute to sample; the item is named after it
    assert (height.name, height.input.socket.default_value) == ("height", "height")
    assert (color.name, color.input.socket.default_value) == ("Colour", "Col")
    assert height.output.socket.identifier == "Attribute_0"
    assert color.output.socket.identifier == "Attribute_1"  # past Col's alpha
    code = _round_trip(tree)
    assert 'raycast.o["Colour Alpha"]' in code


def test_shader_closure_zone():
    with s.tree() as tree:
        zone = s.ClosureZone()
        x = zone.inputs.float("x")
        x.output * 2 >> zone.outputs.float("y").input
        s.EvaluateClosure(zone.closure)
    assert {n.bl_idname for n in tree.tree.nodes} >= {
        "NodeClosureInput",
        "NodeClosureOutput",
        "NodeEvaluateClosure",
    }
