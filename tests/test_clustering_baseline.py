import sys
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Add current dir to path to import core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.louvain_optimizer import SILouvainOptimizer

def generate_gaussian_states(n_clusters=3, nodes_per_cluster=20):
    states = []
    labels = []
    centers = np.random.uniform(-10, 10, (n_clusters, 2))
    for i in range(n_clusters):
        cluster_states = np.random.normal(centers[i], 1.0, (nodes_per_cluster, 2))
        states.append(cluster_states)
        labels.extend([i] * nodes_per_cluster)
    return np.vstack(states), np.array(labels)

def build_similarity_graph(states, threshold=2.0):
    G = nx.Graph()
    n = len(states)
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(states[i] - states[j])
            if dist < threshold:
                weight = np.exp(-dist) # RBF kernel weight
                G.add_edge(i, j, weight=weight)
    return G

def main():
    print("Generating synthetic state space...")
    states, true_labels = generate_gaussian_states()
    
    print("Building similarity graph...")
    G = build_similarity_graph(states)
    
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    
    print("Optimizing Structural Entropy (Louvain-style)...")
    optimizer = SILouvainOptimizer(G)
    partition = optimizer.run()
    
    # Plotting
    plt.figure(figsize=(12, 5))
    
    # Ground Truth
    plt.subplot(1, 2, 1)
    plt.scatter(states[:, 0], states[:, 1], c=true_labels, cmap='viridis')
    plt.title("True State Clusters")
    
    # SI Clusters
    plt.subplot(1, 2, 2)
    si_labels = [partition[i] for i in range(len(states))]
    plt.scatter(states[:, 0], states[:, 1], c=si_labels, cmap='tab20')
    plt.title("Structural Information Clusters")
    
    save_path = "/workspace/SI-Lab/tests/clustering_results.png"
    plt.savefig(save_path)
    print(f"Results saved to {save_path}")

if __name__ == "__main__":
    main()
