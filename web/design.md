# SI-Lab Platform: Design Specification (v0.1.0)

## 1. Overview & Vision
SI-Lab is evolving from a visualizer into a comprehensive, interactive platform for the development, benchmarking, and testing of community detection algorithms. The platform's core mission is to provide an "Algorithm Workbench" where researchers can:
- Compare diverse community detection strategies (Modularity-based, Infomap, SI-Entropy, etc.).
- Visualize hierarchical decompositions in a standardized multi-dimensional environment.
- Validate local moves and global convergence against established benchmarks.

## 2. Technical Architecture
The system follows a modular architecture to support plug-and-play algorithms and metrics.

### 2.1. Backend Framework
- **Core**: Python/Flask.
- **Library Integration**: **cdlib (Community Discovery Library)**.
    - **Algorithms**: Standardizing access to over 100+ algorithms (Louvain, Leiden, Walktrap, etc.) via a unified interface.
    - **Metrics**: Using `cdlib.evaluation` for standardized community quality assessment (Internal/External).
    - **Datasets**: Leveraging `cdlib` and `networkx` for standard benchmark graphs.
- **LabManager**: Acts as the bridge between `cdlib` output (Partition objects) and the hierarchical visualizer.

### 2.2. Frontend Workbench
- **Cytoscape.js**: 2D Interactive topology and manual partition overrides.
- **Three.js (r128)**: 3D hierarchical encoding tree mapping.
- **TWEEN.js**: Animation engine for state transitions.

## 3. Visualization Design
### 3.1. Dual-View Interface
- **Top Panel (2D)**: Real-time topology interaction. Standardized node coloring based on `cdlib` partition IDs.
- **Bottom Panel (3D)**: Tree-based hierarchical mapping. Supports multiple-level aggregation layers provided by hierarchical algorithms in `cdlib`.

### 3.2. Hierarchical Representation
- **Nodes**: Spheres positioned via centroid calculation.
- **Edges**: Dual-mode (Adjacency vs. Hierarchy/Tree) styling for structural clarity.

## 4. Platform Logic & Standards
### 4.1. CDLib Integration Strategy
To maintain interoperability, all internal partitions are mapped to `cdlib.NodeClustering` or `cdlib.HierarchicalClustering` objects. This allows the platform to:
1. **Fetch Algorithm**: Query any CDLib-supported algorithm via a configuration-driven API.
2. **Standardize Metrics**: Display standardized evaluation scores (conductance, coverage, expansion) alongside SI-Entropy.
3. **Compare**: Side-by-side comparison of different algorithm outputs on the same topology.

## 6. Visualization of Arbitrary Algorithms
To support any algorithm from `cdlib`, the platform implements a standardized mapping layer between algorithm outputs and the 2D/3D views.

### 6.1. Mapping Clusterings to Tree Levels
The visualizer treats algorithm outputs based on their mathematical structure:
- **Flat Algorithms (e.g., Louvain, Leiden, Walktrap)**:
    - Mapped as a 2-level tree in 3D.
    - Level 0 (Nodes) $\to$ Level 1 (Communities) $\to$ Root.
    - 2D View: Nodes are colored by their cluster ID.
- **Hierarchical Algorithms (e.g., Paris, Louvain-hierarchical, Bisecting K-Means)**:
    - `cdlib.HierarchicalClustering` objects are parsed into a multi-level `labData.tree`.
    - Each level in the hierarchy translates to a specific $Y$-height in the 3D view.
    - 2D aggregation allows the user to "scroll" through different levels of the hierarchy, updating the topology view accordingly.

### 6.2. Universal Algorithm Runner
The platform uses a dynamic dispatcher to execute algorithms:
```python
# Conceptual Backend Dispatcher
def execute_algo(algo_name, G, params):
    # Dynamically find function in cdlib.algorithms
    method = getattr(cdlib.algorithms, algo_name)
    clustering = method(G, **params)
    
    # Transform to standardized tree structure
    if isinstance(clustering, cdlib.HierarchicalClustering):
        return transform_hierarchical(clustering)
    else:
        return transform_flat(clustering)
```

### 6.3. Standardized Evaluation Dashboard
For any executed algorithm, the platform automatically triggers a suite of `cdlib.evaluation` metrics:
- **Internal Quality**: Conductance, Modularity, Density, Internal Edge Density.
- **External Comparison** (if ground truth exists): Adjusted Rand Index (ARI), Normalized Mutual Information (NMI).
- **Complexity**: Time taken and number of clusters detected.

## 7. Step-by-Step Execution & Steering
The platform provides two primary modes for stepped execution, depending on the algorithm's nature.

### 7.1. Level-wise Navigational Stepping
For **Hierarchical Algorithms** (e.g., Paris, Leiden), the entire decomposition is calculated upfront. The "Step" function in the UI then:
1. **Traverses the Tree**: Iterates through the hierarchy levels stored in the `cdlib.HierarchicalClustering` object.
2. **Topology Aggregation**: Triggers a backend `merge` and frontend 3D "lift" animation for each discrete level.
3. **Temporal Playback**: Allows the user to move the "Current Level" slider to see the graph aggregate and simplify in real-time.

### 7.2. Move-wise Optimization Stepping
For **Iterative Algorithms** (e.g., Louvain, Greedy Modularity, SI-Optimization), the platform supports atomic move execution:
1. **Move Suggestion**: The backend identifies the single node move $\Delta \alpha \to \beta$ that maximizes the target objective (e.g., minimizes SI-Entropy).
2. **Human-in-the-Loop**: The UI pauses after each suggestion, allowing the researcher to:
    - **Accept**: Commit the move and recalculate metrics.
    - **Override**: Manually drag the node to a different community to test "what-if" scenarios.
    - **Auto-Play**: Trigger the `autoLoop` to continue until local convergence is reached.

### 7.3. Unified Stepper Design
The Workbench UI implements a standard control bar:
- **[ > ] Play**: Runs the algorithm to completion/convergence.
- **[ |> ] Step**: Performs the next logical step (one Move for flat algos, one Level for hierarchical ones).
- **[ << ] Reset**: Reverts to the base graph $G_0$.
- **[ < ] Undo**: Traverses the `LabManager` level history.

## 8. Performance & Scalability
- **Caching**: `l0Positions` ensure stability across algorithmic re-runs.
- **Stateless API**: The backend is designed to be stateless, with `LabManager` session-based state allowing for easy tracking of "Algorithm History".
