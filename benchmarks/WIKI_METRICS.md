# 📖 SI-Lab Wiki: Clustering Metrics

This wiki provides a detailed explanation of the metrics used in our SI benchmarking suite.

---

### 1. Normalized Mutual Information (NMI)
**Direct Comparison with Ground Truth**
*   **Definition**: Measures the statistical agreement between two partitions (e.g., predicted vs. ground truth).
*   **Range**: [0, 1]
*   **Interpretation**: 
    *   **1.0**: Perfect reconstruction of the true environment structure.
    *   **0.0**: The partitions are independent (random labeling).
*   **Polarity**: **Higher is better (↑)**.

---

### 2. Adjusted Rand Index (ARI)
**Accuracy Adjusted for Chance**
*   **Definition**: Counts how many pairs of nodes are correctly assigned to either the same or different clusters compared to the ground truth.
*   **Range**: [-1, 1] (Usually > 0)
*   **Interpretation**: 
    *   **1.0**: Perfect match.
    *   **0.0**: No better than random assignment.
*   **Polarity**: **Higher is better (↑)**.

---

### 3. Newman-Girvan Modularity
**Inner-Community Strength**
*   **Definition**: Measures the density of edges within communities compared to edges between communities. It evaluates the structural quality of the graph partition without needing ground truth.
*   **Range**: [-0.5, 1]
*   **Interpretation**: 
    *   **High (> 0.4)**: Very strong community structure and clear bottlenecks.
    *   **Low**: Random-like connectivity; poor structural discovery.
*   **Polarity**: **Higher is better (↑)**.

---

### 4. Computation Time (Latency)
**Algorithm Performance**
*   **Definition**: Total wall-clock time required for the algorithm to converge.
*   **Interpretation**: Crucial for RL integration. High latency hinders the real-time rollout frequency.
*   **Polarity**: **Lower is better (↓)**.

---

### 5. Number of Communities
**Structural Granularity**
*   **Definition**: The count of abstract nodes (clusters) identified in the state space.
*   **Interpretation**: In our benchmarks, we aim for the discovery of the true number of clusters (e.g., $K=3$ for our SBM).
*   **Polarity**: **Goal-specific (🎯 target closest to ground truth)**.
