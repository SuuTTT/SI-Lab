import time
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from cdlib import algorithms, evaluation, NodeClustering
import sys
import os

# Import our SI implementations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.louvain_optimizer import SILouvainOptimizer
from core.greedy_si import GreedySIOptimizer
from sip import PartitionTree

def get_node_clustering(partition_dict, G):
    """Convert partition dict to cdlib NodeClustering object."""
    communities = {}
    for node, comm in partition_dict.items():
        if comm not in communities:
            communities[comm] = []
        communities[comm].append(node)
    return NodeClustering(list(communities.values()), G)

def calculate_structural_entropy(G, partition_dict):
    """
    Calculate 2D structural entropy H(G, P) as per sip.py / SI theory.
    H(G, P) = sum_{C in P} - (g_C / VOL) * log2(V_C / VOL)
    """
    vol_total = G.size(weight='weight') * 2
    if vol_total == 0:
        return 0
    
    # Group nodes by community
    communities = {}
    for node, comm in partition_dict.items():
        if comm not in communities:
            communities[comm] = []
        communities[comm].append(node)
        
    se = 0.0
    for comm_nodes in communities.values():
        # Volume of community (sum of degrees)
        v_c = sum(dict(G.degree(comm_nodes, weight='weight')).values())
        # Cut of community (edges leaving)
        g_c = nx.cut_size(G, comm_nodes, weight='weight')
        
        if v_c > 0:
            se += - (g_c / vol_total) * np.log2(v_c / vol_total)
            
    return se

def benchmark_clustering():
    # Reduced scales because Greedy is O(N^2)
    scales = [100, 300, 500] 
    all_results = []
    viz_data = {} # To store partition for N=100 for visualization
    
    for N in scales:
        print(f"\n--- Benchmarking Scale N={N} ---")
        sizes = [N//3, N//3, N - 2*(N//3)]
        probs = [[0.2, 0.01, 0.01], [0.01, 0.2, 0.01], [0.01, 0.01, 0.2]]
        G_raw = nx.stochastic_block_model(sizes, probs, seed=42)
        G = nx.Graph()
        G.add_nodes_from(G_raw.nodes())
        G.add_edges_from(G_raw.edges())
        
        gt_labels = []
        for i, size in enumerate(sizes):
            gt_labels.extend([i] * size)
        
        if N == 100:
            viz_data['G'] = G
            viz_data['gt'] = gt_labels
            viz_data['partitions'] = {}

        methods = [
            ("SI Louvain (Refactored)", "si_louvain"),
            ("SI Greedy (Refactored)", "si_greedy"),
            ("SIHD (Original sip.py)", "sihd_orig"),
            ("Leiden", "leiden"),
        ]

        for name, key in methods:
            print(f"Running {name}...")
            start = time.time()
            try:
                if key == "si_louvain":
                    partition_dict = SILouvainOptimizer(G).run()
                elif key == "si_greedy":
                    # target_communities=3 for fair ground truth comparison
                    partition_dict = GreedySIOptimizer(G).run(target_communities=3)
                elif key == "sihd_orig":
                    adj = nx.to_numpy_array(G)
                    tree = PartitionTree(adj)
                    # For comparison with 3-community SBM, k=2 should find the top-level
                    tree.build_encoding_tree(k=2)
                    root_node = tree.tree_node[tree.root_id]
                    partition_dict = {}
                    for i, c_id in enumerate(root_node.children):
                        for node in tree.tree_node[c_id].partition:
                            partition_dict[node] = i
                elif key == "leiden":
                    clustering_obj = algorithms.leiden(G)
                    partition_dict = {node: i for i, comm in enumerate(clustering_obj.communities) for node in comm}
                
                exec_time = time.time() - start
                
                # Store visualization sample
                if N == 100:
                    viz_data['partitions'][name] = partition_dict

                clustering_obj = get_node_clustering(partition_dict, G)
                
                # Accuracy Labels
                pred_labels = [partition_dict[i] for i in range(N)]
                
                # Metrics
                nmi = normalized_mutual_info_score(gt_labels, pred_labels)
                ari = adjusted_rand_score(gt_labels, pred_labels)
                mod = evaluation.newman_girvan_modularity(G, clustering_obj).score
                se = calculate_structural_entropy(G, partition_dict)
                
                all_results.append({
                    "Scale": N,
                    "Method": name,
                    "Time (s)": exec_time,
                    "NMI": nmi,
                    "ARI": ari,
                    "Modularity": mod,
                    "Structural Entropy": se,
                    "Communities": len(clustering_obj.communities)
                })
            except Exception as e:
                print(f"Error in {name}: {e}")

    df = pd.DataFrame(all_results)
    print("\n=== Comprehensive SI-Variant Comparison ===")
    print(df.to_string(index=False))
    
    df.to_csv("/workspace/SI-Lab/benchmarks/benchmark_results.csv", index=False)
    
    # Visualizations
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    
    sns.lineplot(ax=axes[0, 0], data=df, x="Scale", y="Time (s)", hue="Method", marker='o')
    axes[0, 0].set_yscale('log')
    axes[0, 0].set_title("Execution Time [Lower is Better ↓]")

    sns.barplot(ax=axes[0, 1], data=df, x="Scale", y="NMI", hue="Method")
    axes[0, 1].set_title("NMI Accuracy [Higher is Better ↑]")

    sns.barplot(ax=axes[0, 2], data=df, x="Scale", y="Structural Entropy", hue="Method")
    axes[0, 2].set_title("Structural Entropy [Minimize is Better ↓]")

    sns.barplot(ax=axes[1, 0], data=df, x="Scale", y="ARI", hue="Method")
    axes[1, 0].set_title("ARI Accuracy [Higher is Better ↑]")

    sns.barplot(ax=axes[1, 1], data=df, x="Scale", y="Modularity", hue="Method")
    axes[1, 1].set_title("Structural Quality (Modularity)")
    
    sns.barplot(ax=axes[1, 2], data=df, x="Scale", y="Communities", hue="Method")
    axes[1, 2].set_title("Number of Communities")

    plt.tight_layout()
    plt.savefig("/workspace/SI-Lab/benchmarks/si_comparison_plot.png")
    print(f"\nReport saved to /workspace/SI-Lab/benchmarks/si_comparison_plot.png")

    # --- Community Visualization Plot ---
    if 'G' in viz_data:
        print("Generating community visualization plots...")
        G = viz_data['G']
        pos = nx.spring_layout(G, seed=42)
        methods_to_plot = list(viz_data['partitions'].keys())
        n_methods = len(methods_to_plot) + 1 # +1 for Ground Truth
        
        fig, axes = plt.subplots(1, n_methods, figsize=(5 * n_methods, 5))
        
        # Plot Ground Truth
        nx.draw_networkx_nodes(G, pos, node_size=50, node_color=viz_data['gt'], cmap=plt.cm.jet, ax=axes[0])
        nx.draw_networkx_edges(G, pos, alpha=0.2, ax=axes[0])
        axes[0].set_title("Ground Truth (N=100)")
        axes[0].axis('off')

        # Plot each method
        for i, name in enumerate(methods_to_plot):
            ax = axes[i+1]
            partition = viz_data['partitions'][name]
            node_colors = [partition[node] for node in G.nodes()]
            nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors, cmap=plt.cm.jet, ax=ax)
            nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)
            ax.set_title(f"{name}")
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("/workspace/SI-Lab/benchmarks/community_visualization.png")
        print(f"Community visualization saved to /workspace/SI-Lab/benchmarks/community_visualization.png")

if __name__ == "__main__":
    benchmark_clustering()


if __name__ == "__main__":
    benchmark_clustering()


