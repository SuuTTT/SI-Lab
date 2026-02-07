import math
import heapq
import numpy as np
import numba as nb
from collections import defaultdict

@nb.jit(nopython=True)
def calculate_cut_weight(adj_matrix, p1, p2):
    """Numba-accelerated cut calculation for greedy merging."""
    cut_w = 0.0
    for i in range(len(p1)):
        for j in range(len(p2)):
            w = adj_matrix[p1[i], p2[j]]
            if w != 0:
                cut_w += w
    return cut_w

def compute_entropy_delta(g1, g2, v1, v2, dl1, dl2, cut_12, vol_total):
    """
    Correct delta H for merging two communities in 2D structural entropy.
    Includes both the cut change and the inner volume expansion.
    """
    v_new = v1 + v2
    g_new = g1 + g2 - 2 * cut_12
    dl_new = dl1 + dl2
    
    def h_comm(g, v, dl):
        if v <= 0: return 0
        return - (g / vol_total) * math.log2(v / vol_total) + (v / vol_total) * math.log2(v) - dl / vol_total

    h1 = h_comm(g1, v1, dl1)
    h2 = h_comm(g2, v2, dl2)
    h_new = h_comm(g_new, v_new, dl_new)
    
    return h_new - (h1 + h2)

class GreedySIOptimizer:
    """
    Optimized Greedy Structural Entropy minimization.
    """
    def __init__(self, G):
        self.G = G
        self.adj = nx.to_numpy_array(G)
        self.N = len(G.nodes())
        self.vol_total = np.sum(self.adj)
        
        # Initial communities (singletons)
        self.partition = {i: i for i in range(self.N)}
        self.com_info = {}
        for i in range(self.N):
            degree = np.sum(self.adj[i])
            self_loop = self.adj[i, i]
            g = degree - self_loop # initial g
            dl = degree * math.log2(degree) if degree > 0 else 0
            self.com_info[i] = {'partition': [i], 'vol': degree, 'g': g, 'dl': dl}

    def run(self, target_communities=None):
        active_ids = set(self.com_info.keys())
        
        # Build initial merge heap
        pq = []
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.adj[i, j] > 0:
                    delta = compute_entropy_delta(
                        self.com_info[i]['g'], self.com_info[j]['g'],
                        self.com_info[i]['vol'], self.com_info[j]['vol'],
                        self.com_info[i]['dl'], self.com_info[j]['dl'],
                        self.adj[i, j], self.vol_total
                    )
                    heapq.heappush(pq, (delta, i, j, self.adj[i, j]))

        # Track community edges to speed up merges
        com_adj = defaultdict(lambda: defaultdict(float))
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.adj[i, j] > 0:
                    com_adj[i][j] = self.adj[i, j]
                    com_adj[j][i] = self.adj[i, j]

        next_id = self.N
        while len(active_ids) > (target_communities if target_communities else 1):
            if not pq: break
            
            delta, id1, id2, cut_w = heapq.heappop(pq)
            if id1 not in active_ids or id2 not in active_ids: continue
            
            # Merge id1 and id2 into new_id
            new_id = next_id
            next_id += 1
            
            info1, info2 = self.com_info[id1], self.com_info[id2]
            new_vol = info1['vol'] + info2['vol']
            new_g = info1['g'] + info2['g'] - 2 * cut_w
            new_dl = info1['dl'] + info2['dl']
            new_part = info1['partition'] + info2['partition']
            
            self.com_info[new_id] = {'partition': new_part, 'vol': new_vol, 'g': new_g, 'dl': new_dl}
            
            active_ids.remove(id1)
            active_ids.remove(id2)
            
            # Update community adjacency
            new_neighbors = {}
            for nid, w in com_adj[id1].items():
                if nid != id2 and nid in active_ids:
                    new_neighbors[nid] = new_neighbors.get(nid, 0) + w
            for nid, w in com_adj[id2].items():
                if nid != id1 and nid in active_ids:
                    new_neighbors[nid] = new_neighbors.get(nid, 0) + w
            
            # Clean up old
            del com_adj[id1]
            del com_adj[id2]
            for nid in list(new_neighbors.keys()):
                com_adj[nid].pop(id1, None)
                com_adj[nid].pop(id2, None)
                com_adj[nid][new_id] = new_neighbors[nid]
                com_adj[new_id][nid] = new_neighbors[nid]
                
                # Push new deltas
                d = compute_entropy_delta(
                    new_g, self.com_info[nid]['g'],
                    new_vol, self.com_info[nid]['vol'],
                    new_dl, self.com_info[nid]['dl'],
                    new_neighbors[nid], self.vol_total
                )
                heapq.heappush(pq, (d, new_id, nid, new_neighbors[nid]))
            
            active_ids.add(new_id)

        # Build final partition map
        final_partition = {}
        for i, cid in enumerate(active_ids):
            for node in self.com_info[cid]['partition']:
                final_partition[node] = i
        return final_partition

import networkx as nx
