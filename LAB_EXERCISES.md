# 🧪 SI-Lab Exercises

This lab is designed for you to experiment with and optimize Structural Information (SI) implementations.

## Exercise 1: Efficiency Optimization
**Target**: `core/louvain_optimizer.py`
**Goal**: The current `_calculate_delta` is a placeholder that triggers a full recalculation. 
**Task**: Refactor it to use local updates only. Calculate the entropy change by only considering the affected communities ($C_{source}$ and $C_{target}$). 
*Hint: Look at the `si_louvain.py` in the original repository for the optimized algebraic formula.*

## Exercise 2: Directed Graphs (Transitions)
**Target**: `core/si_base.py`
**Goal**: Reinforcement Learning is inherently about transitions. 
**Task**: Extend the base class to support `DiGraph` (Directed Graphs). Modify the volume $V_C$ and out-degree $g_C$ calculations to handle directed edges (In-degree vs Out-degree structural entropy).

## Exercise 3: Intrinsic Reward Normalization
**Target**: `modules/exploration_reward/si_reward.py`
**Goal**: Intrinsic rewards can destabilize PPO if not scaled correctly.
**Task**: Implement a moving average normalization for the SI-reward. Compare the exploration behavior with a standard RND (Random Network Distillation) baseline.

## Exercise 4: Hierarchical State Visualization
**Target**: `tests/test_clustering_baseline.py`
**Goal**: Visualize deep hierarchies.
**Task**: Instead of a flat partition, build a 3-layer partition tree ($K=3$) and visualize the nested communities using different color shades.
