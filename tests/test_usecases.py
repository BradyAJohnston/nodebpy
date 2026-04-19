import bpy

from nodebpy import geometry as g


def import_channel() -> bpy.types.GeometryNodeTree:
    string_to_format = "{base_path}/{scale}/x0y0z0/x0y0z0c0t{time:04}.vdb"

    with g.tree("Channel Import", arrange="simple") as tree:
        base_path = tree.inputs.string("base_path", subtype="FILE_PATH")
        time = tree.inputs.integer("Time")
        channel_number = tree.inputs.integer("Channel Number")
        channel_name = tree.inputs.string("Channel Name")
        min_value = tree.inputs.float("Minimum Value")
        max_value = tree.inputs.float("Maximum Value")

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
            grid=(gng.o.grid - min_value) / (max_value - min_value),
        )
        _ = sng >> tree.outputs.geometry("Volume")

    return tree.tree


def test_import_channel():
    tree = import_channel()
    assert len(tree.nodes) == 10
