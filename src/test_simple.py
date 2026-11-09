from nodebpy import geometry as g, TreeBuilder

with TreeBuilder('Test', arrange=None) as tree:
    _val = tree.inputs.float('Value 1', 3.0)
    
    with g.Frame('Frame'):
        join = g.JoinGeometry()

# Check what layout_snapshot actually produces now
from nodebpy.export import codegen
lines = codegen._layout_snapshot_lines(tree.tree, '    ', keep_reroutes=False)
print('Generated lines:')
for line in lines:
    print(repr(line))
