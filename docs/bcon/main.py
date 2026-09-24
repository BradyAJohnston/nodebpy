import molecularnodes as mn
import molecularnodes.nodes.geometry as mg

from nodebpy import geometry as g

cv = mn.Canvas(mn.scene.EEVEE(samples=16))
cv.camera.lens = 35

mol = mn.Molecule.fetch("4ozs")
cv.look_at(mol, margin=0.2)
mat = mn.material.Default().material

with mol.tree.reset() as (atoms, join):
    anim = mg.AnimateValue(value_max=1.1)
    factor = mg.ChainParameter().o.factor.map_range(anim - 0.1, anim)

    (
        atoms
        >> mg.SetPhiPsiAngle(
            phi=factor.mix.float(mg.DihedralPhi(), 0.0),
            psi=factor.mix.float(mg.DihedralPsi(), 0.0),
        )
        >> mg.StyleBallAndStick(
            quality=2, selection=mg.IsPeptide() & (factor < 1.0), material=mat
        )
        >> join
    )

    (atoms >> mg.StyleCartoon(selection=factor < 0.1, material=mat) >> join)

cv.animation(path="animation.mp4")
