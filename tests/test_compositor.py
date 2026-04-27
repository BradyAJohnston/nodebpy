from nodebpy import compositor as c


def test_initial_compositor():
    with c.tree("comp", fake_user=True) as t:
        image = t.inputs.color("Image")
        depth = t.inputs.float("Depth")
        normal = t.inputs.vector("Normal")
        ao = t.inputs.float("AO")
        background_menu = t.inputs.menu("Background", "Output")
        background_color = t.inputs.color("Background Color")
        outline_menu = t.inputs.menu(
            "Outline", "Outline", expanded=True, optional_label=True
        )
        outline_depth = t.inputs.float("Socket Depth", 5.0)
        outline_size = t.inputs.integer("Outline Size", 2)
        outline_color = t.inputs.color("Outline Color")

        output_color = t.outputs.color("Image")

        with c.Frame("Ambient Occlusion"):
            ao_factor = (1 - ao) ** 0.94 >> c.Kuwahara(..., size=4.0)
            active_image = c.Mix.color(ao_factor, image)
        with c.Frame("Outline"):
            depth_line = c.Filter.sobel(depth) > (outline_depth / 100)
            normal_line = c.Filter.sobel(normal) > 1.5
            outline_comp = (
                (depth_line + normal_line)
                >> c.AntiAliasing()
                >> c.Dilateerode.distance(size=outline_size - 1.0)
                >> c.AntiAliasing()
            )

        with c.Frame("Final Composit"):
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
    with c.tree() as tree:
        menu = c.MenuSwitch.string(*[str(x) for x in range(10)])
        menu >> tree.outputs.string()

    assert len(menu.node.enum_items) == 10
    assert menu.node.outputs[0].links

    with c.tree() as tree:
        menu = c.MenuSwitch.float(
            **{f"Input_{i}": float(value) for i, value in enumerate(range(10))}
        )
        menu >> tree.outputs.float()

    assert len(menu.node.enum_items) == 10
    for i, input in enumerate([x for x in menu.inputs._values() if x.type == "VALUE"]):
        assert f"Input_{i}" == input.name
        assert float(i) == input.socket.default_value

    with c.tree() as tree:
        menu = c.MenuSwitch.float(
            **{f"Input_{i}": c.Value(value) for i, value in enumerate(range(10))}
        )
        menu >> tree.outputs.float()

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
        assert idx.data_type == "VECTOR"
        idx.data_type = "FLOAT"
        assert idx.data_type == "FLOAT"
