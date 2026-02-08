Here is the calculation documentation for **Structural Entropy**, designed for algorithm developers. This guide focuses on the mathematical definitions, data structures, and algorithms required to compute and minimize Structural Entropy as defined in the provided literature.

***

# **Algorithm Developer Guide: Structural Entropy Calculation**

## **1. Overview**
Structural Entropy is a metric used to quantify the dynamical complexity of a network. Unlike Shannon entropy, which measures uncertainty in a "flat" probability distribution, Structural Entropy measures the uncertainty of a random walker's trajectory embedded within a hierarchical structure (Encoding Tree) of the network.

**Core Objective:**
*   **Evaluation:** Calculate the Structural Entropy $H^T(G)$ for a graph $G$ given a specific hierarchical partition (Encoding Tree $T$).
*   **Optimization:** Find the optimal Encoding Tree $T^*$ that minimizes $H^T(G)$ to reveal the "natural structure" (e.g., communities) of the network.

## **2. Data Structures**

### **2.1 Input Graph ($G$)**
The system is modeled as a weighted, directed or undirected graph $G = (V, E, W)$.
*   **$V$**: Set of $n$ nodes.
*   **$E$**: Set of edges.
*   **$W$**: Weights of edges. For unweighted graphs, $w_{ij} = 1$.
*   **Total Volume ($2m$ or $Vol(G)$)**: The sum of all weighted degrees in the graph.
    *   $Vol(G) = \sum_{v \in V} d_v$.
    *   *Note:* In directed graphs, this is the sum of in-degrees (or out-degrees). In undirected graphs, it is $2 \times \text{total edge weight}$.

### **2.2 Encoding Tree ($T$)**
The Encoding Tree represents a hierarchical partitioning of the graph.
*   **Root ($\lambda$)**: Represents the entire graph node set $V$.
*   **Leaves**: Represent individual nodes of the graph.
*   **Internal Nodes ($\alpha$)**: Represent "modules" or clusters of nodes.
*   **Structure**:
    *   $T_\alpha$: The subset of graph nodes contained in the subtree rooted at $\alpha$.
    *   $\alpha^-$: The parent node of $\alpha$ in the tree.

## **3. Key Variables**

For any node $\alpha$ in the Encoding Tree, we calculate two primary metrics based on the underlying graph:

1.  **Volume ($V_\alpha$)**: The stationary distribution volume of the module.
    *   $V_\alpha = \sum_{v \in T_\alpha} d_v$
    *   *Where $d_v$ is the degree (or weighted degree) of graph node $v$.*

2.  **Cut ($g_\alpha$)**: The "flow" leaving the module.
    *   $g_\alpha = \sum_{u \in T_\alpha, v \notin T_\alpha} w_{uv}$
    *   *The sum of weights of edges connecting nodes inside $T_\alpha$ to nodes outside $T_\alpha$.*
    *   *Special Case (Leaves):* If $\alpha$ is a leaf representing graph node $u$, $g_\alpha = d_u$ (since all edges leave the singleton set).
    *   *Special Case (Root):* $g_\lambda = 0$ (no edges leave the entire graph).

## **4. Calculation Formulas**

### **4.1 Structural Entropy Formula ($H^T(G)$)**
The Structural Entropy is the sum of local entropies defined by the Encoding Tree. It is calculated by summing over all nodes in the tree **except the root**.

$$H^T(G) = - \sum_{\alpha \in T, \alpha \neq \lambda} \frac{g_\alpha}{Vol(G)} \log_2 \frac{V_\alpha}{V_{\alpha^-}}$$

**Step-by-Step Calculation:**
1.  **Normalize:** We use the stationary distribution probability $p_\alpha = \frac{g_\alpha}{Vol(G)}$ (Note: In some derivations, the coefficient is simply the cut normalized by the total volume).
2.  **Relative Volume:** Calculate the ratio of the module's volume to its parent's volume: $\frac{V_\alpha}{V_{\alpha^-}}$.
3.  **Summation:** For every node $\alpha$ (leaves and internal nodes), calculate $-\frac{g_\alpha}{Vol(G)} \log_2 (\text{ratio})$ and sum them up.

### **4.2 One-Dimensional Structural Entropy ($H_1$)**
This is the baseline entropy where the tree has height 1 (Root -> Leaves). It is equivalent to the Shannon entropy of the degree distribution.
$$H_1(G) = - \sum_{i=1}^n \frac{d_i}{Vol(G)} \log_2 \frac{d_i}{Vol(G)}$$

### **4.3 Two-Dimensional Structural Entropy ($H^P(G)$)**
If the tree has height 2 (Root -> Modules -> Leaves), defined by a partition $P = \{X_1, ..., X_L\}$:
$$H^P(G) = - \sum_{j=1}^L \frac{V_j}{Vol(G)} \sum_{i \in X_j} \frac{d_i}{V_j} \log_2 \frac{d_i}{V_j} - \sum_{j=1}^L \frac{g_j}{Vol(G)} \log_2 \frac{V_j}{Vol(G)}$$
*   **Term 1:** Weighted average of Shannon entropy within modules.
*   **Term 2:** Entropy of the module cuts relative to module volumes.

## **5. Minimization Algorithm (Optimization)**

To find the natural community structure, you must find the tree $T$ that minimizes $H^T(G)$.

**Greedy Strategy (Merging Operator):**
The standard approach is a bottom-up greedy algorithm (similar to agglomerative clustering).

1.  **Initialization:** Start with the 1-dimensional tree (Root connected directly to all leaves).
    *   Current Entropy = $H_1(G)$.
2.  **Iteration:** Attempt to merge two sibling nodes (modules) $\alpha$ and $\beta$ into a new module $\delta$.
3.  **Delta Calculation ($\Delta \mathcal{H}$):** Calculate the change in entropy if $\alpha$ and $\beta$ are merged.
    *   If nodes $i$ and $j$ are merged, the reduction in entropy is positive only if there are edges between them.
    *   **Merge Condition:** Only merge if $\Delta \mathcal{H} > 0$ (Entropy decreases).
4.  **Selection:** At each step, perform the merge that yields the maximum entropy reduction.
5.  **Termination:** Stop when no merge operation can further reduce the entropy.

**Optimization Metric ($\Delta$ for merging modules $i$ and $j$):**
When merging modules $i$ and $j$ into $new$, the change can be derived from the difference in the volume and cut terms.
*   $V_{new} = V_i + V_j$
*   $g_{new} = g_i + g_j - 2 \cdot w_{ij}$ (where $w_{ij}$ is the weight of edges between $i$ and $j$).

## **6. Pseudo-Code Implementation**

```python
def calculate_structural_entropy(graph, encoding_tree):
    """
    Calculates H^T(G) for a given graph and tree.
    """
    total_volume = sum(graph.degrees.values())
    entropy = 0.0
    
    # Traverse all nodes in tree except root
    for node in encoding_tree.nodes:
        if node.is_root():
            continue
            
        # 1. Get graph properties for the module represented by this tree node
        g_alpha = calculate_cut(graph, node.cluster_nodes)
        v_alpha = calculate_volume(graph, node.cluster_nodes)
        
        # 2. Get parent's volume
        v_parent = calculate_volume(graph, node.parent.cluster_nodes)
        
        # 3. Apply formula term
        if v_alpha > 0 and v_parent > 0:
            term = - (g_alpha / total_volume) * log2(v_alpha / v_parent)
            entropy += term
            
    return entropy

def minimize_structural_entropy(graph):
    """
    Greedy algorithm to find 2D Structural Entropy (Community Detection).
    """
    # Start with each node in its own cluster
    clusters = [{node} for node in graph.nodes]
    
    while True:
        best_merge = None
        max_delta = 0
        
        # Evaluate all pairs connected by edges
        for cluster_i, cluster_j in get_connected_pairs(clusters, graph):
            
            # Calculate entropy reduction
            # Heuristic: Focus on merging modules with high interconnectivity (w_ij)
            delta = calculate_merge_delta(cluster_i, cluster_j, graph)
            
            if delta > max_delta:
                max_delta = delta
                best_merge = (cluster_i, cluster_j)
        
        if best_merge:
            # Perform merge
            clusters.merge(best_merge, best_merge)
        else:
            break # Local minimum reached
            
    return clusters
```

## **7. References**
*   **Definitions & Formulas:** Li, A., & Pan, Y. (2016). *Structural Information and Dynamical Complexity of Networks*. IEEE Transactions on Information Theory.
*   **Minimization Principle:** Su, D., et al. (2025). *A Survey of Structural Entropy*. IJCAI.
*   **Optimization Algorithms:** Li, A. (2024). *Artificial Intelligence Science*.