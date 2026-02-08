# Wiki: Preservation of Invariants in SI-Lab

In hierarchical community detection (like Louvain), "aggregation" is a critical step where communities are collapsed into single nodes for the next level of optimization. 

## 1. Modularity Invariance
When you aggregate a graph:
- **Edges between communities** in Level $L$ become **edges between nodes** in Level $L+1$.
- **Edges within communities** in Level $L$ must become **self-loops** in Level $L+1$.

If self-loops are preserved correctly, the **Modularity (Q)** of current partition on the original graph is identical to the Modularity of a trivial singleton partition on the aggregated graph. 

## 2. Structural Entropy Invariance during Layer Aggregation

The "Hierarchical SI" shown in the Dashboard remains invariant during aggregation because our visualizer treats the **Partition** as a distinct layer in the encoding tree.

1. **Before Aggregation:** We have nodes $G_L$ and their partition $\mathcal{P}_L$. The tree is $G_0 \to \dots \to G_L \to \mathcal{P}_L \to \lambda$.
2. **During Aggregation:** Communities $\mathcal{P}_L$ are materialized into a new node layer $G_{L+1}$. The previous partition becomes the new nodes.
3. **After Aggregation:** The tree is $G_0 \to \dots \to G_L \to G_{L+1} \to \lambda$. 

Because $G_{L+1}$ is just the materialized version of $\mathcal{P}_L$ with preserved volumes and cuts, the information content remains identical.

### Why standard 2D SI fluctuates
In a "flat" implementation, 2D SI only considers the distance between **Nodes** and **Communities**. When you aggregate, your "nodes" become larger clusters.
- Level 0: $H(G, \mathcal{P})$ measures entropy of nodes relative to communities.
- Level 1: $H(G_{agg}, \mathcal{P}_{agg})$ measures entropy of *clusters* relative to *super-clusters*.

By using **Hierarchical SI $H(G; T)$**, we anchor everything back to the original graph $G_0$, ensuring that "Collapse Hierarchies" only changes the tree's height, not its mathematical result.

## 3. Summary of Metrics
| Metric | Behavior on Aggregate | Purpose |
| :--- | :--- | :--- |
| **Base $H(G_0)$** | Constant | Theoretical maximum entropy. |
| **Hierarchy $H(G;T)$** | Decreases (usually) | Shows the efficiency of the full multi-level tree. |
| **Modularity $Q$** | Constant | Validates consistency of edge preservation. |
| **L(n) 1D Entropy** | Decreases | Shows how much information is "abstracted away" into clusters. |
