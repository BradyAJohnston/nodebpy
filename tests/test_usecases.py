from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import sockets as s


def import_channel():
    string_to_format = "{base_path}/{scale}/x0y0z0/x0y0z0c0t{time:04}.vdb"

    with TreeBuilder("Channel Import", arrange="simple") as tree:
        with tree.inputs:
            base_path = s.SocketString("base_path", subtype="FILE_PATH")
            time = s.SocketInt("Time")
            channel_number = s.SocketInt("Channel Number")
            channel_name = s.SocketString("Channel Name")
            min_value = s.SocketFloat("Minimum Value")
            max_value = s.SocketFloat("Maximum Value")

        volume = g.ImportVDB(
            g.FormatString(
                time=time,
                channel_number=channel_number,
                base_path=base_path,
                scale=g.Integer(0),
                format=string_to_format,
            )
        )
        gng = g.GetNamedGrid.float(volume, "data")
        sng = g.StoreNamedGrid.float(
            gng,
            name=channel_name,
            grid=(gng.o_grid - min_value) / (max_value - min_value),
        )
        with tree.outputs:
            _ = sng >> s.SocketGeometry("Volume")

    return tree.tree


def test_import_channel():
    tree = import_channel()
    assert len(tree.nodes) == 10
