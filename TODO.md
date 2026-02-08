# SI-Lab TODO List

Track upcoming features and technical improvements for the Structural Information Laboratory.

## Phase A: UX & Layout Refinement
- [ ] **Split-Screen Layout**: Redesign UI to show the 2D Topology and 3D Encoding Tree simultaneously without tab switching.
- [ ] **Interactive Drill-Down**: Allow clicking on community nodes in L1+ to "unwrap" and see internal nodes from lower levels.
- [ ] **Internal Energy Viz**: Improve Cytoscape styles to visualize "Self-Loops" as a representation of community internal density.
- [ ] **MathJax Optimization**: Implement lazy-loading for MathJax to improve dashboard responsiveness.

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
