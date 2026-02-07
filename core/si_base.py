import numpy as np
import math
import networkx as nx
from collections import defaultdict

class StructuralEntropyBase:
    """
    Base class for Structural Entropy calculations.
    Follows the principle of minimizing the entropy of a graph partition.
    """
    def __init__(self, graph):
        self.G = graph
        self.W = self.G.size(weight='weight')
        if self.W == 0:
            self.W = self.G.size()
        
        self.partition = {node: node for node in self.G.nodes()}
        self.V_C = defaultdict(float) # Volume of community
        self.g_C = defaultdict(float) # Degree of community (out-edges)
        self.dlog2d_per_community = defaultdict(float)
        self.dlog2d_per_node = {}

        self._initialize_metrics()

    def _initialize_metrics(self):
        for node in self.G.nodes():
            degree = self.G.degree(node, weight='weight') or 1
            self.V_C[node] = degree
            self.dlog2d_per_node[node] = degree * math.log2(degree)
            self.dlog2d_per_community[node] = self.dlog2d_per_node[node]
            
            # Initially, each node is in its own community
            # g_C for a singleton community is its degree minus 2*self-loop
            self_loop = self.G.get_edge_data(node, node, default={}).get('weight', 0)
            self.g_C[node] = degree - (2 * self_loop)

    def calculate_community_entropy(self, community_label):
        V_C = self.V_C[community_label]
        g_C = self.g_C[community_label]
        dlog2d_community = self.dlog2d_per_community[community_label]
        
        if V_C <= 0: return 0
        
        # 2D Structural Entropy Formula Component for a community C
        # H(C) = - (g_C / 2W) * log2(V_C / 2W) + (V_C / 2W) * log2(V_C) - (sum_{v in C} d_v log2 d_v) / 2W
        h_c = - (g_C / (2 * self.W)) * math.log2(V_C / (2 * self.W))
        h_c += (V_C / (2 * self.W)) * math.log2(V_C)
        h_c -= dlog2d_community / (2 * self.W)
        return h_c

    def get_total_entropy(self):
        communities = set(self.partition.values())
        return sum(self.calculate_community_entropy(c) for c in communities)

    def get_partition(self):
        return self.partition
