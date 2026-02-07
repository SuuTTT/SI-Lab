from core.si_base import StructuralEntropyBase
import networkx as nx
import math

class SILouvainOptimizer(StructuralEntropyBase):
    """
    Louvain-style optimizer to minimize Structural Entropy.
    Iteratively moves nodes between communities to find the optimal structural partition.
    """
    def run(self):
        """
        Multi-level Louvain optimization for Structural Entropy.
        """
        current_graph = self.G
        partition_map = {node: node for node in current_graph.nodes()}
        
        while True:
            optimizer = SILouvainOptimizerPass(current_graph)
            new_partition = optimizer.optimize()
            
            # Update the global partition map
            nodes_moved = False
            for node, target in partition_map.items():
                # node is original node, target is current super-node
                if new_partition[target] != target:
                    nodes_moved = True
                partition_map[node] = new_partition[target]
            
            if not nodes_moved:
                break
                
            # Aggregate graph for next level
            current_graph = self._aggregate_graph(current_graph, new_partition)
            if len(current_graph.nodes()) == 1:
                break
                
        self.partition = partition_map
        return self.partition

    def _aggregate_graph(self, G, partition):
        new_G = nx.Graph()
        communities = set(partition.values())
        new_G.add_nodes_from(communities)
        
        for u, v, data in G.edges(data=True):
            w = data.get('weight', 1)
            com_u = partition[u]
            com_v = partition[v]
            if new_G.has_edge(com_u, com_v):
                new_G[com_u][com_v]['weight'] += w
            else:
                new_G.add_edge(com_u, com_v, weight=w)
                
        # Handle nodes with no edges but potential self-loops from previous aggregation
        for node in G.nodes():
            com = partition[node]
            # Internal weights become self-loops in the aggregated graph
            # This is handled by u,v iteration if self-loops existed.
            # But we must ensure all nodes are present.
        
        return new_G

class SILouvainOptimizerPass(StructuralEntropyBase):
    """Internal helper for a single pass of Louvain moves."""
    def optimize(self):
        modified = True
        while modified:
            modified = self._one_pass()
        return self.partition

    def _one_pass(self):
        nodes = list(self.G.nodes())
        any_improvement = False
        
        for node in nodes:
            best_community = self.partition[node]
            min_delta = 1e-10 # Use a small epsilon for stability
            
            # Find neighboring communities
            neighbor_communities = set()
            for neighbor in self.G.neighbors(node):
                neighbor_communities.add(self.partition[neighbor])
            
            for community in neighbor_communities:
                if community == self.partition[node]: continue
                
                delta = self._calculate_delta(node, community)
                if delta < -min_delta:
                    min_delta = -delta
                    best_community = community
            
            if best_community != self.partition[node]:
                self._move_node(node, best_community)
                any_improvement = True
                
        return any_improvement

    def _calculate_delta(self, node, target_community):
        # (Same calculation logic as before)
        old_community = self.partition[node]
        
        entropy_before = self.calculate_community_entropy(old_community) + \
                         self.calculate_community_entropy(target_community)
        
        degree = self.G.degree(node, weight='weight') or 0
        v_old_after = self.V_C[old_community] - degree
        v_new_after = self.V_C[target_community] + degree
        
        dlog2d_node = self.dlog2d_per_node[node]
        dlog2d_old_after = self.dlog2d_per_community[old_community] - dlog2d_node
        dlog2d_new_after = self.dlog2d_per_community[target_community] + dlog2d_node

        g_old_after = self.g_C[old_community]
        g_new_after = self.g_C[target_community]
        
        # Self-loops on 'node' don't contribute to g_C changes when moving
        # but the cut to target and others does.
        for neighbor, data in self.G[node].items():
            if neighbor == node: continue
            w = data.get('weight', 1)
            if self.partition[neighbor] == old_community:
                g_old_after += w
            else:
                g_old_after -= w
            
            if self.partition[neighbor] == target_community:
                g_new_after -= w
            else:
                g_new_after += w

        def local_h(v, g, dl):
            if v <= 0: return 0
            h = - (g / (2 * self.W)) * math.log2(v / (2 * self.W))
            h += (v / (2 * self.W)) * math.log2(v)
            h -= dl / (2 * self.W)
            return h

        entropy_after = local_h(v_old_after, g_old_after, dlog2d_old_after) + \
                        local_h(v_new_after, g_new_after, dlog2d_new_after)
        
        return entropy_after - entropy_before

    def _move_node(self, node, target_community):
        source_community = self.partition[node]
        degree = self.G.degree(node, weight='weight') or 0
        
        self.V_C[source_community] -= degree
        self.dlog2d_per_community[source_community] -= self.dlog2d_per_node[node]
        
        self.V_C[target_community] += degree
        self.dlog2d_per_community[target_community] += self.dlog2d_per_node[node]

        for neighbor, data in self.G[node].items():
            if neighbor == node: continue
            w = data.get('weight', 1)
            if self.partition[neighbor] == source_community:
                self.g_C[source_community] += w
            else:
                self.g_C[source_community] -= w
            
            if self.partition[neighbor] == target_community:
                self.g_C[target_community] -= w
            else:
                self.g_C[target_community] += w
        
        self.partition[node] = target_community

