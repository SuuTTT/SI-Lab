# Structural Information (SI) Theory & Algorithms

Structural Information (SI) is a metric based on Shannon entropy that quantifies the information required to represent a graph's structure given a specific hierarchical partition. Minimizing structural entropy allows for the discovery of inherent community structures at multiple scales.

## 1. Mathematical Foundation

### 2D Structural Entropy
For a graph $G = (V, E)$ and a partition $\mathcal{P} = \{C_1, C_2, \dots, C_k\}$, the 2D structural entropy is defined as:

$$H(G, \mathcal{P}) = \sum_{C \in \mathcal{P}} - \frac{g_C}{VOL} \log_2 \left( \frac{V_C}{VOL} \right)$$

Where:
- $V_C$: Total degree of nodes in community $C$ (Volume).
- $g_C$: Number of edges with exactly one endpoint in $C$ (Cut).
- $VOL$: Sum of degrees of all nodes in the graph ($\sum_{v \in V} d_v$).

### High-Dimensional (Hierarchical) Structural Entropy
For an encoding tree $\mathcal{T}$ of $G$:

$$H(G, \mathcal{T}) = \sum_{\alpha \in \mathcal{T}, \alpha \neq \text{root}} - \frac{g_\alpha}{VOL} \log_2 \left( \frac{V_\alpha}{V_{\text{parent}(\alpha)}} \right)$$

---

## 2. Algorithms

### Algorithm 1: SI Greedy Merging (Legacy / SIRD)
Objective: Find a partition by iteratively merging communities that provide the maximum reduction in entropy.

```python
Algorithm GreedyMerge(G):
    Initialize: Each node v is its own community C_v
    While |Communities| > Target:
        For each pair of adjacent communities (Ci, Cj):
            Calculate delta_H = H(G, P_after_merge) - H(G, P_before)
        Select pair (Ci, Cj) with minimal delta_H
        Merge Ci and Cj into a single community
    Return Partition
```

### Algorithm 2: SI Louvain Optimization (Modern / SISL)
Objective: Optimize the partition using local node movements, similar to the Louvain method but targeting entropy instead of modularity.

```python
Algorithm SILouvain(G):
    Initialize: Each node v is its own community C_v
    Repeat:
        # Phase 1: Local Movement
        For each node v in V:
            For each neighbor u of v:
                Calculate delta_H of moving v from C(v) to C(u)
            Move v to community that minimizes delta_H
        # Phase 2: Aggregation
        If no node was moved: break
        Construct a new graph where nodes are communities
    Return Partition
```

### Algorithm 3: SIHD Hierarchical Refinement (High-Dimensional / SIHD)
Objective: Build a stable multi-level hierarchy using root-down and leaf-up operators.

```python
Algorithm SIHD_Refine(G, Tree T):
    Repeat:
        # Operator 1: Leaf-Up
        For each level from leaves to root:
            Build sub-graphs within parent communities
            Re-optimize sub-clusters to minimize local entropy
        
        # Operator 2: Root-Down
        For each level from root to leaves:
            Check if children of a node can be split or merged
            To better represent the global entropy gradient
            
    Until Tree structure stabilizes
    Return Encoding Tree T
```

---

## 3. Implementation History
1. **SIRD (2016):** Introduction of Greedy Merging for community detection.
2. **SIHD (2018):** High-dimensional hierarchical logic and stability proofs.
3. **SISL (2022):** Integration into Reinforcement Learning as an intrinsic reward head.
4. **SI2E (2024):** End-to-end differentiable structural information optimization.
