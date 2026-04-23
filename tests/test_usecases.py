from functools import reduce
from itertools import product
from operator import and_

import bpy

from nodebpy import geometry as g
from nodebpy.nodes.geometry.groups import PrincipalComponents


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


def test_decoder_8bit():
    # this should actually be 8 bits but it takes a bit longer to run through
    # (~20 seconds) so for testing we can keep it much smaller. It's a nice
    # clean implementation and good example of the code in action.
    N_BITS = 4
    with g.tree("8-Bit Decoder", arrange="simple") as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(N_BITS)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]

        for i, combo in enumerate(product((False, True), repeat=N_BITS)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")

    assert len(tree) == 54
    assert len(tree.inputs) == 4
    assert len(tree.outputs) == 16
    assert all(
        i.links[0].from_node.operation == "AND"
        for i in tree.nodes["Group Output"].inputs
        if i.identifier != "__extend__"
    )


def test_import_channel():
    tree = import_channel()
    assert len(tree.nodes) == 10


def test_PCA_asset():
    with g.tree():
        pca = PrincipalComponents()

    assert len(pca.node.node_tree.nodes) == 31
