# Changelog - SI-Lab Visualizer

All notable changes to the SI-Lab visualizer will be documented in this file.

## [v0.7.0] - 2026-02-12 (Current)
### Added
- **Split-Screen Layout**: Implemented side-by-side visualization with 2D Cytoscape (Topology) and 3D Three.js (Encoding Tree).
- **3D Interactive Tree**: High-performance 3D rendering with OrbitControls and white minimalist aesthetic.
- **Animation Suite**: Integrated TWEEN.js for "lifting" supernodes during aggregation and a specialized "bounce" for final root convergence.
- **2D/3D Synchronization**: Real-time position tracking between Cytoscape coordinates and the 3D Level 0 plane.
- **Dynamic Edge Styling**: Color-coded visualization (Black for horizontal topology, Grey for vertical hierarchy tree).

### Fixed
- **Hierarchy Redundancy**: Optimized `get_encoding_tree` to automatically prune redundant partition layers.
- **Edge Connectivity**: Fixed a bug where vertical edges failed to track moving nodes across hierarchy levels.
- **Persistence**: Implemented `l0Positions` cache to prevent 3D model reset during state updates.

## [v0.6.0] - 2026-02-08
### Added
- **Knowledge Base**: Integrated a Modal-based Wiki in the header for real-time theory reference.
- **SIP.py Validation**: Real-time comparison of current Hierarchical SI against a ground-truth optimization engine.
- **Metric Stability**: Implemented self-loop handling in graph aggregation to ensure Modularity ($Q$) and Structural Entropy ($H$) remain invariant during "Collapse" phases.

### Fixed
- **Tree Visualization**: Corrected edge direction in the Encoding Tree (Parent -> Child) and implemented Breadth-First layout.
- **Javascript Robustness**: Added error handling in `refresh()` and fixed variable definition order.

## [v0.5.0] - 2026-02-07
### Added
- **Hierarchical Aggregation**: Supported multi-level graph collapsing (L0 -> L1 -> ... -> Lk).
- **Tree Inspector**: Detailed view for individual nodes in the encoding tree showing local $h_\alpha$ contributions.

## [v0.4.0] - 2026-02-05
### Added
- **Dynamic Presets**: Added classical graphs like Zachary's Karate Club, Ring of Cliques, and special rational-SI cases (Star graphs).
- **Louvain Logic**: Implemented "Next Move" suggestion engine for local community optimization.

## [v0.3.0] - 2026-02-03
### Added
- **Interactive Workbench**: Drag-and-drop support for graph nodes.
- **Live Calculation**: Mathematical formulas render via MathJax 3 while adjusting weights.

## [v0.2.0] - 2026-02-02
### Added
- **Web UI**: Transitioned from CLI `sip.py` to a Flask-based Cytoscape.js visualizer.
- **LabManager**: Backend state management for graph topology and partitions.

## [v0.1.0] - 2026-02-01
### Added
- **Base Algorithm**: Initial standalone Python implementation of Structural Information entropy calculations.

---

## [Upcoming / TODO]
- **Algorithm Integration**: Plug-in architecture for custom community detection algorithms (GN, Label Propagation, Infomap).
- **Batch Testing Suite**: Benchmarking tools to run optimization algorithms across multiple presets simultaneously.
- **Graph Import/Export**: Support for `.gml`, `.graphml`, and custom JSON exports of the 2D/3D state.
- **Real-time Collaboration**: WebSocket-based "Shared Room" for collaborative graph decomposition.
- **Advanced Layouts**: Integration of Force-Directed 3D layouts for the entire encoding tree.
