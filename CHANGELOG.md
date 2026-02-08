# Changelog - SI-Lab Visualizer

All notable changes to the SI-Lab visualizer will be documented in this file.

## [v0.6.0] - 2026-02-08 (Current)
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
