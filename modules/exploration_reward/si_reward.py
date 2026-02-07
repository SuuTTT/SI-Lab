import numpy as np
import math
from collections import Counter

class SI2E_Exploration:
    """
    Lab implementation of Value-Conditional Structural Entropy for Exploration.
    Based on the SI2E paper concept.
    """
    def __init__(self, partition_tree):
        self.tree = partition_tree

    @staticmethod
    def compute_intrinsic_reward(states, partition_tree):
        """
        Rewards states that fall into communities with higher 'structural novelty'.
        In SI2E, this is typically the entropy reduction of the partition tree.
        """
        # Simplified version: reward is negative of normalized community size
        # Rare communities = higher reward
        communities = [partition_tree[s] for s in states]
        counts = Counter(communities)
        total = len(states)
        
        rewards = []
        for s in states:
            p_community = counts[partition_tree[s]] / total
            # Structural novelty signal
            reward = -np.log(p_community + 1e-6)
            rewards.append(reward)
        return np.array(rewards)

# This module would typically interface with a replay buffer
print("Exploration Reward module initialized.")
