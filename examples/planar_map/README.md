# Planar maps from 3D curves, in Geometry Nodes

A port of [Robust Planar Maps for 3D Vectorization](https://www.cs.cmu.edu/~kmcrane/Projects/RobustPlanarMaps/index.html)
(Fuchs & Crane, ACM TOG 45(4), 2026) to Geometry Nodes, built with nodebpy.

```bash
BLENDER_USER_EXTENSIONS=/nonexistent uv run python examples/planar_map/run_suzanne.py
```

## Status

| Stage | Paper | State |
|---|---|---|
| 1. Intersection detection (BSP) | §2.1, §2.2 | done: `bsp.py` |
| Separating lines | §2.3 | done, for cells crossed by exactly two curves |
| 2. Region identification (halfedge planar map) | §3 | not started |
| Gap circles | §3.5 | not started |
| 3. Ray-traced region identity, merging | §4.1–4.3 | not started |
| Partial transparency (layer merging) | §4.4 | out of scope: sequential, with cycle checks |

## How stage 1 maps onto nodes

- **Input curves.** `ProjectedContours` selects silhouette edges (one face of the
  pair faces the camera and the other doesn't), boundary edges and creases, then
  flattens them with a perspective divide in camera space.
- **No self-intersections.** The paper needs curves that don't cross themselves.
  `CurveFragments` cuts each curve wherever its running turn passes `Max Turn`
  (160°). A planar curve that turns less than 180° in total can't cross itself.
- **Cells stay quads.** Every split runs between points on two opposite edges of a
  cell, so both children are quads. A cell is one point with four corner attributes
  (`p0`–`p3`, counter-clockwise), and a split is Duplicate Elements with amount 2.
- **One point cloud.** Fragments (one point per straight segment: `a`, `b`, `curve`)
  and cells share a cloud, both tagged with `cell`, the cell's path through the tree
  (`2 * parent + child`). Grouped Field Min & Max by `cell` answers "does more than
  one curve cross this cell?", picks the paper's split points (the middle of the gap
  between crossings that holds each edge's midpoint), and passes the cell's corners
  to its fragments.
- **Breadth-first.** A repeat zone runs one tree level per pass, splitting every
  cell at that level at once. The paper builds its tree one cell at a time and
  mentions parallelising it as future work.
- **Separating lines.** A cell crossed by exactly two curves is split along a line
  between them when one exists: fragments are straight, so projecting their end
  points onto a normal gives each curve's exact extent, and non-overlapping extents
  leave a gap no fragment crosses. Three normals are tried (perpendicular to each
  curve's chord, and the direction between the curves' centres); the line must cross
  two opposite edges so both children stay quads. As in the paper, these splits run
  past `Max Depth`, for up to `Separating Passes` more levels.
- **Decide, then split.** Each pass first stores every cell's split line on all of
  its points (`split`, `axis`, `m1`, `m2`), then duplicates and rewrites from the
  stored line. The separating test uses sums and means, which change when points are
  duplicated, so nothing after the duplicate recomputes them. Each group reads the
  cloud through `Read BSP Cloud` and writes through capture-then-store groups.

`run_suzanne.py` checks the invariants after each run: cells are counter-clockwise
and tile the root exactly, cell ids are unique, every fragment lies inside its cell,
cells other than intersection nodes hold at most one curve, and the total length of
the fragments equals that of the input.
