from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import sockets as s


def test_initial_compositor():
    with c.tree("comp", fake_user=True) as t:
        with t.inputs:
            image = s.SocketColor("Image")
            depth = s.SocketFloat("Depth")
            normal = s.SocketVector("Normal")
            ao = s.SocketColor("AO")

            background_menu = s.SocketMenu("Background", "Output")
            background_color = s.SocketColor("Background Color")
            outline_menu = s.SocketMenu(
                "Outline", "Outline", expanded=True, optional_label=True
            )

            outline_depth = s.SocketFloat("Socket Depth", 5.0)
            outline_size = s.SocketInteger("Outline Size", 2)
            outline_color = s.SocketColor("Outline Color")

        with t.outputs:
            output_color = s.SocketColor("Image")

        ao_factor = c.InvertColor(ao) ** 0.94 >> c.Kuwahara(..., size=4.0)
        active_image = c.Mix.color(ao_factor, image)
        depth_line = c.Filter.sobel(depth) > (outline_depth / 100)
        normal_line = c.Filter.sobel(normal) > 1.5
        outline_comp = (
            (depth_line + normal_line)
            >> c.AntiAliasing()
            >> c.Dilateerode(type="Distance", size=outline_size - 1.0)
            >> c.AntiAliasing()
        )

        outline_switch = c.MenuSwitch.color(
            **{
                "None": active_image,
                "Outline": c.AlphaOver(outline_comp, outline_color),
            },
            menu=outline_menu,
        )

        _ = (
            c.MenuSwitch.color(
                outline_switch,
                c.AlphaOver(background_color, outline_switch),
                menu=background_menu,
            )
            >> output_color
        )


def test_compositor_menu_switch():
    with TreeBuilder.compositor() as tree:
        menu = c.MenuSwitch.string(*[str(x) for x in range(10)])
        with tree.outputs:
            _ = menu >> s.SocketString()

    assert len(menu.node.enum_items) == 10
    assert menu.node.outputs[0].links

    with TreeBuilder.compositor() as tree:
        menu = c.MenuSwitch.float(
            **{f"Input_{i}": float(value) for i, value in enumerate(range(10))}
        )
        with tree.outputs:
            _ = menu >> s.SocketFloat()

    assert len(menu.node.enum_items) == 10
    for i, input in enumerate([x for x in menu.inputs._values() if x.type == "VALUE"]):
        assert f"Input_{i}" == input.name
        assert float(i) == input.socket.default_value

    with TreeBuilder.shader() as tree:
        menu = c.MenuSwitch.float(
            **{f"Input_{i}": c.Value(value) for i, value in enumerate(range(10))}
        )
        with tree.outputs:
            _ = menu >> s.SocketFloat()

    assert len(menu.node.enum_items) == 10
    for i, input in enumerate([x for x in menu.inputs._values() if x.type == "VALUE"]):
        assert f"Input_{i}" == input.name
        assert input.socket.links[0].from_node.bl_idname == c.Value._bl_idname
        # we have to check the output defeault value here because that is how the Value
        # node is defined which is truly cursed but hey it is what it is
        assert input.socket.links[0].from_node.outputs[0].default_value == float(i)


def test_nodes():
    with c.tree():
        idx = c.IndexSwitch.vector()
        assert idx.node.data_type == "VECTOR"
        idx.node.data_type = "FLOAT"
        assert idx.node.data_type == "FLOAT"
