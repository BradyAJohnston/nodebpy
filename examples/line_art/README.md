# Line Art in Geometry Nodes

Blender's Line Art modifier rebuilt as a Geometry Nodes tree, from the pieces of
[`examples/planar_map`](../planar_map). It goes on a Grease Pencil object, as Line Art
does, and draws a source object's feature lines whose occlusion level is in a range.

```bash
BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/line_art/compare.py --subdiv 0 1 2 3 4 5 6
```

`compare.py` sets up Suzanne, a camera, and two Grease Pencil objects, one with Line
Art and one with this tree, and for each subdivision level reports each one's
evaluation time and how well their strokes agree on screen (precision: share of our
stroke pixels within 2 px of Line Art's; recall: the reverse). It writes a
side-by-side image per level to `out/`.

## Results

Suzanne from the test camera, default settings (contours, creases, material
boundaries, edge marks; occlusion level 0), median of repeated updates:

| Subdivision | Faces | Line Art | Nodes | Speed-up | Precision | Recall |
|---|---|---|---|---|---|---|
| 0 | 500 | 2.1 ms | 5.5 ms | 0.38x | 92.4% | 89.9% |
| 1 | 1,968 | 2.8 ms | 4.7 ms | 0.60x | 90.5% | 94.9% |
| 2 | 7,872 | 5.8 ms | 5.0 ms | 1.15x | 98.1% | 95.9% |
| 3 | 31,488 | 9.7 ms | 7.3 ms | 1.34x | 98.0% | 98.4% |
| 4 | 125,952 | 27.1 ms | 13.1 ms | 2.08x | 98.1% | 99.8% |
| 5 | 503,808 | 93.3 ms | 30.6 ms | 3.04x | 98.1% | 100% |
| 6 | 2,015,232 | 331.7 ms | 76.2 ms | 4.35x | 98.1% | 100% |

The node tree has a fixed cost of a few milliseconds and then scales better: Line
Art is faster on small meshes, the nodes from about 8,000 faces up. (Line Art is
not single-threaded throughout: its occlusion stage runs on a task pool.)

With intersection lines on, the node tree is far slower (0.30 s at subdivision 2,
1.19 s at 3, against Line Art's 9 and 14 ms): they come from an exact Mesh Boolean
self-union, and the faster Float and Manifold solvers can't do it (Float doesn't
resolve self-intersections within one mesh; Manifold needs a closed mesh). Line
Art tests triangle pairs directly; doing that in nodes is open work. The
Intersection type is off by default.

## How it works

- **Feature edges.** Each edge is classified once on the full mesh (contour: a
  silhouette or open boundary; crease: normals more than Crease Angle apart, or a
  sharp edge; material boundary; edge mark `freestyle_edge`; intersection; loose),
  then everything but the feature edges is deleted and the curves are built from
  what's left. Mesh to Curve averages edge attributes onto points, so each vertex
  stores the share of its edges of each type and a segment takes the larger.
- **Sampled (default).** Curves are resampled to `Spacing` (about a pixel at the
  test framing). Each sample casts from the camera; every hit nearer than the
  sample adds an occlusion level and the next cast starts just past it, up to
  Level End + 1 casts. The kept flag is blurred along the curve so a grazing ray
  can't flicker one sample, and kept samples chain into strokes, split where the
  curve, the selection or the edge type changes. Strokes are placed back in 3D at
  each point's distance from the camera.
- **Precise.** The planar map's BSP cuts the curves where they cross on screen;
  each piece between crossings takes the majority of its fragments' levels. Exact
  crossings, but each BSP pass has a fixed cost, so it runs at 66-200 ms here.

## Where the time went, and what fixed it

Profiling turned up three things worth knowing for any large node tree:

1. **Classify once, then shrink.** Storing six per-type attributes on the full mesh
   re-evaluated the face and edge fields for each store: 58 ms at 126k faces. One
   edge code, a delete, and the per-type shares on the few edges left: 6 ms.
2. **A repeat zone inside a group defeats laziness.** The unused Precise branch
   was evaluated on every update: a node group containing a repeat zone makes
   Blender evaluate the group's geometry input even when a switch doesn't use its
   output. The Precise path now gets an empty input and zero passes unless chosen.
3. **Each repeat-zone pass has a fixed cost.** Sixteen BSP passes over a single
   point still cost about 50 ms, from evaluating several hundred nodes per pass.

`../planar_map/ISSUES.md` has these, with repros, among the other bugs and rough
edges found while building both examples.
