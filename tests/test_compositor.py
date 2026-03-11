from nodebpy import TreeBuilder
from nodebpy import sockets as s
from nodebpy.nodes import compositor as c


def test_initial_compositor():
    with TreeBuilder.compositor("comp", fake_user=True) as t:
        with t.inputs:
            image = s.SocketColor("Image")
            depth = s.SocketFloat("Depth")
            normal = s.SocketVector("Normal")
            ao = s.SocketColor("AO")
            background_menu = s.SocketMenu("Background")
            background_color = s.SocketColor("Background Color")
            outline_menu = s.SocketMenu(name="Outline", expanded=True)
            outline_depth = s.SocketFloat("Socket Depth", default_value=5.0)
            outline_size = s.SocketInt("Outline Size", default_value=2)
            outline_color = s.SocketColor("Outline Color")
        with t.outputs:
            output_color = s.SocketColor("Image")

        ao_factor = (
            ao
            >> c.InvertColor()
            >> c.Math.power(value_001=0.94)
            >> c.Kuwahara(size=4.0)
        )

        active_image = c.Mix.color(ao_factor, image)
        depth_line = (
            depth
            >> c.Filter(type="Sobel")
            >> c.Math.greater_than(..., outline_depth / 100)
        )
        normal_line = normal >> c.Filter(type="Sobel") >> c.Math.greater_than(..., 1.5)
        outline_comp = (
            (depth_line + normal_line)
            >> c.AntiAliasing()
            >> c.Dilateerode(type="Distance", size=outline_size - 1.0)
            >> c.AntiAliasing()
        )

        outline_switch = c.MenuSwitch.color(
            outline_menu, active_image, c.AlphaOver(outline_comp, outline_color)
        )

        _ = (
            c.MenuSwitch.color(
                background_menu,
                outline_switch,
                c.AlphaOver(background_color, outline_switch),
            )
            >> output_color
        )
