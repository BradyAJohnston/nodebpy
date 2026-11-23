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
| 2. Region identification (halfedge planar map) | §3.1–3.4 | done: `regions.py` |
| Gap circles | §3.5 | not started |
| 3. Ray-traced region identity, merging | §4.1–4.2 | done: `occlusion.py` |
| Edge classification, line layers | §4.3 | done: `lines.py` |
| Holes assigned to their region | §4.4.1 | done: `RegionFills` |
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

## How stage 2 maps onto nodes

- **Curve order.** Fragments carry their source segment `seg` and the part of it
  they cover (`fa` to `fb`) through every split, so sorting by segment, then `fa`,
  puts each curve back in order. Sort Elements orders groups by id.
- **Stops and edges.** `Stops` walks each curve: a run of fragments in one
  intersection node is a visit to that node's vertex; a curve end in a plain cell
  is a dangling vertex. Consecutive stops make an edge. Edges with no plain
  fragment step straight between adjacent nodes, and only the first per pair of
  nodes is kept (Section 3.3's degenerate faces).
- **Rotation.** `NextHalfedge` sorts the halfedges leaving each vertex by where they
  cross the node's boundary, counter-clockwise (Section 3.3), and sets
  `next(h)` to the one just before `twin(h)`.
- **Faces.** `Faces` labels each orbit of `next` with its lowest `hid` and ranks the
  halfedges in it, by pointer jumping in repeat zones (`log2(H)` passes).
- **Region loops.** `RegionLoops` concatenates each face's edges, stepping straight
  across nodes between them (Section 3.4). `RegionsToGreasePencil` fills the
  counter-clockwise loops, largest first; Grease Pencil only fills strokes with a
  non-zero `fill_id`.

## How stage 3 maps onto nodes

- **Patches.** `SurfacePatches` splits the mesh at crease edges and numbers the
  islands: a face attribute `patch`.
- **Region identity (4.1).** `RegionIdentity` takes each face's longest halfedge,
  casts a 2D ray inward from its middle against `FragmentWalls` (every fragment
  extruded into a vertical quad, so Raycast works in the screen plane), and fires
  a camera ray through the point halfway to the wall. The hit's patch, normal and
  a headlight shade are stored on every halfedge of the face.
- **Which edges go.** `EdgeVisibility` hides an edge when both faces see the same
  thing (the paper's rule) *and*, if the edge has geometry, its own curve is
  hidden: the camera ray through its middle meets the surface nearer than the
  curve. Fragments carry their distance from the camera (`da`, `db`) through the
  BSP for this. The second condition is not in the paper: on a mesh one patch can
  fold over itself, and the paper's rule alone erases those silhouettes (the ear
  over the head).
- **Merging (4.2).** `MergeRegions` points each hidden halfedge at `next(twin)`,
  pointer-jumps until every chain reaches a kept halfedge, relinks `next` through
  it, compacts the halfedges, and `Faces` relabels them.
- **Colour.** Regions are coloured by the patch they show and shaded by its
  normal; regions that see nothing are left unfilled.

## Drawing

The output is one Grease Pencil geometry with three named layers, from
`ToGreasePencil` (each layer is an instance whose geometry name becomes the layer
name):

- **Fills:** one fill per region (`fill_id`), coloured by patch and shaded by
  normal. A clockwise outline (a connected piece inside a region, like an eye in
  the head) joins its surrounding region's fill as a hole, so each area is filled
  once. The surrounding region is found by filling every bounded loop, stacking
  the fills by area (smallest on top) and casting down from just outside the
  outline.
- **Lines:** every visible edge, wider for outlines (background on one side) than
  silhouettes, and for silhouettes than creases (Section 4.3). The paper
  classifies by patch adjacency; here each segment remembers whether it came
  from a silhouette or boundary edge or a crease, which Mesh to Curve passes on
  as a per-vertex share of the two.
- **Hidden:** the edges occlusion removed, dashed (off by default).

## Open items in the method

- Faces made only of zero-length steps between nodes have no fragment to sample,
  so they get no identity and stay as unfilled specks. Letting them match any
  neighbour chained the far eye into the head, so they are left alone.
- At depth 8 and below, the straight step across a large node can cross another
  curve; the loop then crosses itself and Grease Pencil leaves part of it
  unfilled. The map is still valid.
- Line classes come from the input curves, so a silhouette that coincides with
  a crease takes whichever its segment's ends say.

`run_suzanne.py` checks the invariants after each run: cells are counter-clockwise
and tile the root exactly, cell ids are unique, every fragment lies inside its cell,
cells other than intersection nodes hold at most one curve, and the total length of
the fragments equals that of the input. For the map: `next` is a permutation, each
halfedge's `next` starts at the vertex it ends at, every connected piece has
V - E + F = 2 (which fails if the order around any vertex is inconsistent), and
the signed areas of all loops cancel to within the intersection nodes' area. It
also reports the paper's raster measure (Section 5.3): the share of a 240 x 240
grid where the region drawn shows the same patch as a ray cast at the mesh.
