# 🎯 SI-Lab Development Plan: From Research to Production

This document outlines the roadmap for transforming the Structural Information (SI) research series into a unified, high-performance library and an ablation playground.

---

## 📅 Roadmap Overview

### Phase 1: Archaeology & Benchmarking (Data-First)
**Goal**: Harvest all variants of SI and establish a rigorous performance baseline.

1.  **Code Extraction**:
    *   Pull logic from `SIRD` (Action Space), `SISA` (Markovian Abstraction), `SISL` (Transition Graphs), `SI2E` (Exploration), and `SIHD` (Diffusion Planning).
    *   Normalize into a repository-independent format.
2.  **Performance Profiling**:
    *   **Runtime**: Benchmark time-to-convergence for graph partitioning on graphs of $N \in [10^2, 10^5]$ nodes.
    *   **Entropy Efficiency**: Measure the actual structural entropy reduction achieved by each variant.
3.  **Baseline Duel**:
    *   Competitive testing against industry-standard graph clustering:
        *   **Louvain/Leiden**: Modularity-based benchmarks.
        *   **InfoMap**: Map-equation/Compression-based benchmarks.
    *   **Comparison Metrics**: Normalized Mutual Information (NMI), Adjusted Rand Index (ARI), and computation latency per update.

---

## Phase 2: The Unified "SIP-Core" Library
**Goal**: Build a single, optimized Python package (`sip-core`).

1.  **Architecture**:
    *   `sip.Graph`: Support for weighted, directed, and sparse transitions.
    *   `sip.PartitionTree`: Implementation of hierarchical encoding trees (2D, 3D, and K-dimensional).
2.  **Optimization**:
    *   Port critical loops to **Cython** or **Torch-Script** for real-time RL integration.
    *   Implement **incremental graph updates** to avoid $O(N^2)$ rebuilds during RL rollouts.
3.  **Flexible Backends**:
    *   Greedy Merging (SIRD/SIHD style).
    *   Hierarchical Louvain (SISL style).
    *   Optimization-based HCSE (SISA style).

---

## Phase 3: Integration & Ablation Framework
**Goal**: Create a plug-and-play pipeline to test the "True Effect" of SI on learning algorithms.

1.  **Modular Integration**:
    *   **Intrinsic Head**: A component that plugs into `DrQ-v2` or `PPO` to reward SI-novelty.
    *   **Abstract Head**: A wrapper to mask/cluster observations before they reach the Buffer.
2.  **Ablation Designer**:
    *   Compare **SI-based Exploration** vs. **RND** vs. **Emepheral Information**.
    *   Compare **SI-based Skill Discovery** vs. **DADS/VIC** style skill learning.
3.  **Standardized Benchmarking**:
    *   Test on `DMControl`, `MiniGrid`, and `Meta-Drive`.

---

## Phase 4: The Tutorial Lab
**Goal**: Showcase the utility of SI as a general-purpose learning tool.

1.  **Interactive Notebooks**:
    *   *Notebook 1*: "Why Modularity?" - Visualizing entropy on bottlenecks.
    *   *Notebook 2*: "Building the SIP-Reward" - Step-by-step PPO integration.
2.  **Comparative Analysis Report**:
    *   Final publication-grade report generated from the ablation results.

---

## 📈 Success Metrics
*   **Latency**: SI processing should occupy $<5\%$ of the total RL training loop time.
*   **Sample Efficiency**: $>20\%$ improvement in sparse-reward environments compared to non-SI baselines.
*   **Code Quality**: 100% test coverage for the `sip-core` library.
