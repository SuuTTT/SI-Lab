import itertools
import networkx as nx
import math
import numpy as np

def all_partitions(collection):
    """
    Generate all possible partitions of a set.
    The number of partitions is the Bell number B_n.
    """
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for older in all_partitions(collection[1:]):
        # Insert `first` into each existing sub-collection
        for i in range(len(older)):
            yield older[:i] + [[first] + older[i]] + older[i+1:]
        # Or insert `first` as a new singleton sub-collection
        yield [[first]] + older

class BruteForceSI:
    def __init__(self, G):
        self.G = G
        self.total_vol = sum(dict(G.degree(weight='weight')).values())
        if self.total_vol == 0:
            self.total_vol = 1 # Avoid division by zero
            
    def get_cut(self, nodes):
        if not nodes: return 0
        return nx.cut_size(self.G, nodes, weight='weight')

    def get_vol(self, nodes):
        if not nodes: return 0
        return sum(dict(self.G.degree(nodes, weight='weight')).values())

    def solve(self):
        """Find the optimal clustering tree for the whole graph."""
        nodes = list(self.G.nodes())
        best_h, best_tree = self._recurse(nodes, self.total_vol)
        return best_h, best_tree

    def _recurse(self, nodes, parent_vol):
        """
        Recursively find the best sub-tree for a set of nodes.
        nodes: current cluster
        parent_vol: volume of the parent cluster in the tree
        """
        if len(nodes) == 1:
            return 0, {"id": nodes[0]}

        best_h = float('inf')
        best_tree = None

        # Try all possible partitions of the current set of nodes
        for partition in all_partitions(list(nodes)):
            # Trivial partition (all in one) is not a split, unless it's a leaf.
            # But SI trees must eventually split down to leaves.
            if len(partition) == 1:
                continue
            
            current_h = 0
            current_subtrees = []
            
            # For each community in the partition, calculate its contribution
            # H = sum_{C} [ -(g_C/VOL) * log2(V_C / V_parent) + H_sub_tree ]
            for community in partition:
                v_c = self.get_vol(community)
                g_c = self.get_cut(community)
                
                # Contribution of this node in the tree
                if v_c > 0 and parent_vol > 0:
                    level_h = - (g_c / self.total_vol) * math.log2(v_c / parent_vol)
                else:
                    level_h = 0
                
                sub_h, sub_tree = self._recurse(community, v_c)
                current_h += level_h + sub_h
                current_subtrees.append(sub_tree)
            
            if current_h < best_h:
                best_h = current_h
                best_tree = {
                    "partition": partition,
                    "children": current_subtrees,
                    "h_total": current_h
                }
        
        return best_h, best_tree

def print_tree(tree, indent=0):
    if "id" in tree:
        print("  " * indent + f"Leaf: {tree['id']}")
    else:
        print("  " * indent + f"Internal Node (H_total: {tree['h_total']:.4f})")
        for child in tree["children"]:
            print_tree(child, indent + 1)

if __name__ == "__main__":
    # Create a small community graph (N=4)
    # 0 -- 1 (Strong)
    # 2 -- 3 (Strong)
    # 1 -- 2 (Weak)
    G = nx.Graph()
    G.add_edge(0, 1, weight=10)
    G.add_edge(2, 3, weight=10)
    G.add_edge(1, 2, weight=1)
    
    print("Graph: 4 nodes, clear community structure (0,1) and (2,3)")
    solver = BruteForceSI(G)
    best_h, best_tree = solver.solve()
    
    print(f"\nMinimum Structural Entropy: {best_h:.4f}")
    print("Optimal Encoding Tree Structure:")
    print_tree(best_tree)
