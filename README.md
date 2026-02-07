# 🧪 SI-Lab: Structural Information in Reinforcement Learning

Welcome to the **SI-Lab**. This project is a curated refactoring of the **Structural Information (SI)** research series, designed as a tutorial and laboratory for integrating structural entropy into modern RL pipelines.

## 📖 Overview

The SI Series introduces the **Structural Information Principle (SIP)** to Reinforcement Learning. By representing states, actions, or skills as nodes in a graph, we can use structural entropy to discover hierarchical motifs, simplify decision-making, and drive exploration.

### The SI Workflow
1.  **Representation**: Project raw data into a latent embedding space.
2.  **Graph Construction**: Build similarity or transition graphs (Directed/Undirected).
3.  **Modular Partitioning**: Minimize structural entropy to find the optimal encoding tree.
4.  **Integration**: Use the partition hierarchy for State Abstraction, Action Grouping, or Intrinsic Rewards.

*   **[Planning](./PLAN.md)**: Development roadmap for Phase 1-4.

---

## 🛠️ Lab Modules

This lab is organized by the functional role SI plays in the learning pipeline:

| Module | Origin | Description |
| :--- | :--- | :--- |
| **[State Abstraction](./modules/state_abstraction)** | SISA / SISL | Hierarchical clustering of states to create "Abstract States" for high-level policies. |
| **[Action Abstraction](./modules/action_abstraction)** | SIRD | Partitioning large action spaces into manageable skill-like clusters. |
| **[Exploration Reward](./modules/exploration_reward)** | SI2E | Using Value-Conditional Structural Entropy as an intrinsic motivation signal. |
| **[Hierarchical Planning](./modules/planning)** | SIHD | Guiding diffusion-based planners using multi-level state partitions. |

---

## 🔬 Core Algorithms

The logic has been refactored into a unified library in `/core`:

1.  **`si_base.py`**: Foundation for Structural Entropy calculation.
2.  **`louvain_optimizer.py`**: Scalable community detection for directed graphs (SISL-style).
3.  **`encoding_tree.py`**: Logic for building and optimizing the k-dimensional partition tree.

---

## 🎓 How to Use This Lab

### 1. Run the Baseline Test
Visualize how SI clusters simple 2D Gaussian "states":
```bash
python tests/test_clustering_baseline.py
```

### 2. Refactor Experiments
Each module contains a `README.md` explaining how to integrate the SI loss into a standard PPO or SAC implementation.

### 3. Optimization Targets
*   **Latency**: SI graph construction is currently slow. The lab includes `fast_sip` optimizations using cached nearest neighbors.
*   **Scalability**: Moving from $O(N^2)$ similarity matrices to sparse graph representations.
