# SI-Lab TODO List

Track upcoming features and technical improvements for the Structural Information Laboratory.

## Phase A: UX & Layout Refinement
- [x] **Split-Screen Layout**: Redesign UI to show the 2D Topology and 3D Encoding Tree simultaneously without tab switching. using 3.js, specifically:  the lowest layer is original 2D topology, one layer upper is the super node representing the community in the lower layer, and so on.


## Phase B: Algorithmic Depth
- [ ] **Leiden Integration**: Add support for the Leiden algorithm to fix "disconnected community" artifacts common in Louvain.
- [ ] **Resolution Slider**: Implement a slider for the resolution parameter ($\gamma$) to observe entropy changes across scales.
- [ ] **Incremental Updates**: Optimize the `suggestMove` loop to only recalculate affected communities during moves.

## Phase C: Scientific Data Handling
- [ ] **Edge List Import**: Allow users to drag-and-drop `.csv` or `.json` files to load proprietary graph datasets.
- [ ] **Snapshot Export**: Export current hierarchical state as a high-resolution SVG or JSON snapshot.
- [ ] **Monte-Carlo Benchmarking**: Run 100+ Louvain iterations in a background task and display the distribution of $H$ results to show stochastic variance.

## Maintenance
- [ ] Port `app.py` to a more structured multi-file Flask layout (Blueprints).
- [ ] Add unit tests for the Structural Entropy invariant logic in `LabManager`.
- [ ] Standardize the CSS/JS assets into a `/static/` folder.
