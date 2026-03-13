from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import sockets as s
from nodebpy.lib.nodearrange.arrange.stacking import T


def test_initial_compositor():
    with TreeBuilder.compositor("comp", fake_user=True) as t:
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
            outline_size = s.SocketInt("Outline Size", 2)
            outline_color = s.SocketColor("Outline Color")

        with t.outputs:
            output_color = s.SocketColor("Image")

        ao_factor = (ao >> c.InvertColor()) ** 0.94 >> c.Kuwahara(size=4.0).i_image
        active_image = c.Mix.color(ao_factor, image)
        depth_line = c.Filter(depth, type="Sobel") > (outline_depth / 100)
        normal_line = c.Filter(normal, type="Sobel") > 1.5
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
