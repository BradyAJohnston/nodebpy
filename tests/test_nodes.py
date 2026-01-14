from nodebpy import TreeBuilder, nodes as n, sockets as s


def test_capture_attribute():
    with TreeBuilder("TestCaptureAttribute") as tree:
        cube = n.Cube()
        cap = n.CaptureAttribute(domain="POINT")

        _ = (
            cube
            >> cap
            >> n.SetPosition(offset=(0, 0, 10))
            >> n.SetPosition(position=cap.capture(n.Position()))
        )

    assert "Capture Attribute" in tree.nodes
    assert len(cap._items) == 1
    assert cap.node.outputs[1].name == "Position"
    assert cap.node.outputs[1].type == "VECTOR"
