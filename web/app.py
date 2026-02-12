from flask import Flask, jsonify, request, render_template
import networkx as nx
import math
import os
import sys
import numpy as np

# Add benchmarks to path to import sip.py
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'benchmarks'))
try:
    import sip
    SIP_AVAILABLE = True
except ImportError:
    SIP_AVAILABLE = False

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# --- Metrics Definitions ---
METRIC_DEFS = {
    "se_1d": {
        "name": "Structural Entropy (1D)",
        "formula": r"H^{(1)}(G) = - \sum_{i \in V} \frac{d_i}{V} \log_2 \frac{d_i}{V}",
    },
    "se_2d": {
        "name": "Structural Entropy (2D)",
        "formula": r"H^{(2)}(G, \mathcal{P}) = - \sum_{C \in \mathcal{P}} \left( \frac{g_C}{V} \log_2 \frac{V_C}{V} + \sum_{i \in C} \frac{d_i}{V} \log_2 \frac{d_i}{V_C} \right)",
    },
    "modularity": {
        "name": "Modularity (Q)",
        "formula": r"Q = \sum_{C \in \mathcal{P}} [ \frac{e_C}{m} - (\frac{V_C}{2m})^2 ]",
    }
}

class LabManager:
    def __init__(self):
        self.levels = []
        self.current_level = 0
        self.G0 = None
        self.load_preset("bridge")

    def load_preset(self, type):
        if type == "bridge":
            G = nx.Graph()
            G.add_edge("A1", "A2", weight=10.0); G.add_edge("A2", "A3", weight=10.0); G.add_edge("A3", "A1", weight=10.0)
            G.add_edge("B1", "B2", weight=10.0); G.add_edge("B2", "B3", weight=10.0); G.add_edge("B3", "B1", weight=10.0)
            G.add_edge("A3", "B1", weight=1.0)
        elif type == "karate":
            G = nx.karate_club_graph()
        elif type == "ring_cliques":
            G = nx.ring_of_cliques(4, 4)
        elif type == "grid":
            G = nx.grid_2d_graph(4, 4)
        elif type == "cube":
            G = nx.hypercube_graph(3) # 8 nodes, 3rd dimension
        elif type == "star_5":
            G = nx.star_graph(4) # center + 4 leaves = 5 nodes. H = 1 + 0.5*log2(4) = 2.0
        elif type == "star_3":
            G = nx.star_graph(2) # center + 2 leaves. H = 1.5 (Rational)
        elif type == "complete_4":
            G = nx.complete_graph(4) # 4 nodes, H = log2(4) = 2.0
        elif type == "path_4":
            G = nx.path_graph(4) # 4 nodes
        else:
            G = nx.ring_of_cliques(4, 4)
        
        # Standardize node names and weights
        mapping = {n: str(n).replace("(", "").replace(")", "").replace(", ", "_") for n in G.nodes()}
        G = nx.relabel_nodes(G, mapping)
        for u, v in G.edges(): 
            if 'weight' not in G[u][v]: G[u][v]['weight'] = 1.0
        
        self.G0 = G.copy()
        partition = {n: i for i, n in enumerate(G.nodes())}
        self.levels = [{"G": G.copy(), "partition": partition, "label": "L0: Nodes"}]
        self.current_level = 0

    def get_current(self):
        return self.levels[self.current_level]

    def move_node(self, node_id, target_comm):
        curr = self.get_current()
        curr["partition"][node_id] = int(target_comm)
        if self.current_level < len(self.levels) - 1:
            self.levels = self.levels[:self.current_level+1]

    def get_encoding_tree(self):
        tree_elements = []
        total_vol = sum(dict(self.G0.degree(weight='weight')).values())
        
        def get_l0_leafs(level_idx, node_id):
            if level_idx == 0:
                return [node_id]
            prev_level = self.levels[level_idx - 1]
            children = [nid for nid, cid in prev_level["partition"].items() if str(cid) == str(node_id)]
            leafs = []
            for c in children:
                leafs.extend(get_l0_leafs(level_idx - 1, c))
            return leafs

        # 1. Add layers G0...Gk
        for l_idx, lvl in enumerate(self.levels):
            G_lvl = lvl["G"]
            partition = lvl["partition"]
            
            for node in G_lvl.nodes():
                tree_id = f"L{l_idx}_{node}"
                leafs = get_l0_leafs(l_idx, node)
                v_alpha = sum(dict(self.G0.degree(leafs, weight='weight')).values())
                g_alpha = nx.cut_size(self.G0, leafs, weight='weight')
                
                # The parent is either the community in the next level, 
                # OR if this is the top level Gk, the parent is the community id or Root
                p_comm = partition.get(node)
                if l_idx < len(self.levels) - 1:
                    parent_id = f"L{l_idx+1}_{p_comm}"
                else:
                    # If partition is identity (num_comms == num_nodes), skip Comm layer and go to Root
                    if len(set(partition.values())) == len(G_lvl):
                        parent_id = "Root"
                    else:
                        parent_id = f"Comm_{p_comm}"
                
                tree_elements.append({
                    "id": tree_id, "label": f"[{l_idx}] {node}", "level": l_idx,
                    "parent": parent_id, "v": v_alpha, "g": g_alpha, "leafs": leafs
                })

        # 2. Add the "Current Partition" Layer (Virtual parent of Lk)
        curr_lvl = self.levels[-1]
        partition = curr_lvl["partition"]
        unique_comms = sorted(list(set(partition.values())))
        
        # Only add Comm layer if it compresses nodes
        is_comm_redundant = (len(unique_comms) == len(curr_lvl["G"]))
        
        root_level = len(self.levels)
        if not is_comm_redundant:
            for cid in unique_comms:
                # Nodes in Lk that belong to this cid
                lk_nodes = [nid for nid, c in partition.items() if c == cid]
                all_leafs = []
                for lk_n in lk_nodes:
                    all_leafs.extend(get_l0_leafs(len(self.levels)-1, lk_n))
                
                v_c = sum(dict(self.G0.degree(all_leafs, weight='weight')).values())
                g_c = nx.cut_size(self.G0, all_leafs, weight='weight')
                
                tree_elements.append({
                    "id": f"Comm_{cid}", "label": f"Comm {cid}", 
                    "level": len(self.levels), "parent": "Root",
                    "v": v_c, "g": g_c, "leafs": all_leafs
                })
            root_level = len(self.levels) + 1

        tree_elements.append({
            "id": "Root", "label": "Graph Root (\u03bb)", "level": root_level,
            "v": total_vol, "g": 0, "parent": None, "contrib": 0
        })

        node_map = {n["id"]: n for n in tree_elements}
        for n in tree_elements: n["children_ids"] = []
        for n in tree_elements:
            if n["parent"]:
                p_node = node_map.get(n["parent"])
                if p_node: p_node["children_ids"].append(n["id"])

        for n in tree_elements:
            if n["id"] == "Root": continue
            p = node_map.get(n["parent"])
            v_p = p["v"] if p else total_vol
            if n["v"] > 0 and v_p > 0 and total_vol > 0:
                n["contrib"] = -(n["g"]/total_vol) * math.log2(n["v"]/v_p)
            else:
                n["contrib"] = 0

        def calc_subtree_sum(node_id):
            node = node_map[node_id]
            c_sum = sum(calc_subtree_sum(cid) for cid in node["children_ids"])
            node["children_contrib_sum"] = sum(node_map[cid]["contrib"] for cid in node["children_ids"])
            node["subtree_total_h"] = node["contrib"] + c_sum
            return node["subtree_total_h"]

        calc_subtree_sum("Root")
        return tree_elements

    def merge_to_next_level(self):
        curr = self.get_current()
        G = curr["G"]
        partition = curr["partition"]
        
        num_nodes = G.number_of_nodes()
        unique_comms = set(partition.values())
        num_comms = len(unique_comms)
        
        if num_comms >= num_nodes:
            return False

        new_G = nx.Graph()
        comm_nodes = {}
        for n, c in partition.items():
            if c not in comm_nodes: comm_nodes[c] = []
            comm_nodes[c].append(n)
        
        new_nodes = sorted(comm_nodes.keys())
        new_G.add_nodes_from([str(c) for c in new_nodes])
        
        # Aggregate weights and INCLUDE SELF-LOOPS for modularity/volume consistency
        for i, c1 in enumerate(new_nodes):
            for j, c2 in enumerate(new_nodes):
                if i > j: continue
                w = 0
                for u in comm_nodes[c1]:
                    for v in comm_nodes[c2]:
                        if G.has_edge(u, v):
                            w += G[u][v]['weight']
                
                if w > 0:
                    # For self-loops (i==j), we've counted internal edges twice (u-v and v-u).
                    # NetworkX degree() counts self-loop weight twice, so we set weight = sum(internal)/2
                    actual_w = w / 2.0 if i == j else w
                    new_G.add_edge(str(c1), str(c2), weight=actual_w)

        new_partition = {str(n): idx for idx, n in enumerate(new_G.nodes())}
        self.levels.append({
            "G": new_G, 
            "partition": new_partition, 
            "label": f"L{len(self.levels)}: Aggregated"
        })
        self.current_level = len(self.levels) - 1
        return True

    def calculate_metrics(self, partition_override=None):
        curr = self.get_current()
        G = curr["G"]
        partition = partition_override if partition_override is not None else curr["partition"]
        vol_total = sum(dict(self.G0.degree(weight='weight')).values())
        m = vol_total / 2.0
        
        # Base 1D Entropy is ALWAYS relative to G0 (Fixed)
        se_1d_base = 0.0
        for n in self.G0.nodes():
            di = self.G0.degree(n, weight='weight')
            if di > 0 and vol_total > 0:
                se_1d_base += -(di/vol_total) * math.log2(di/vol_total)

        # Current level 1D Entropy (entropy of compressed nodes)
        se_1d_curr = 0.0
        for n in G.nodes():
            di = G.degree(n, weight='weight')
            if di > 0 and vol_total > 0:
                se_1d_curr += -(di/vol_total) * math.log2(di/vol_total)

        communities = {}
        for n, c in partition.items():
            if c not in communities: communities[c] = []
            communities[c].append(n)
            
        se_2d = 0.0
        mod_q = 0.0
        traces = []
        for cid in sorted(communities.keys()):
            nodes = communities[cid]
            # Volume and cut are relative to CURRENT graph
            # This allows 2D SI calculation at any level of aggregation
            v_curr = sum(dict(G.degree(nodes, weight='weight')).values())
            g_curr = nx.cut_size(G, nodes, weight='weight')
            
            h_comm = -(g_curr/vol_total)*math.log2(v_curr/vol_total) if v_curr>0 and vol_total>0 else 0
            h_nodes = 0
            for n in nodes:
                di = G.degree(n, weight='weight')
                if di > 0 and v_curr > 0:
                    # Contribution of current nodes to the community above them
                    h_nodes += -(di/vol_total)*math.log2(di/v_curr)
            se_2d += (h_comm + h_nodes)
            
            # Modularity calculation with self-loops
            e_c = (v_curr - g_curr) / 2.0
            q_c = (e_c/m) - (v_curr/(2*m))**2 if m > 0 else 0
            mod_q += q_c

            traces.append({
                "cid": int(cid), "nodes": sorted(nodes), "si": round(h_comm+h_nodes, 4), 
                "q": round(q_c, 4), "v_c": v_curr, "g_c": g_curr
            })
        
        # Tree Entropy (Total Hierarchical SI)
        tree_elements = self.get_encoding_tree()
        root_node = next(n for n in tree_elements if n["id"] == "Root")
        h_tree_total = root_node["subtree_total_h"]

        # SIP Validation
        sip_val = None
        if SIP_AVAILABLE and not partition_override:
            try:
                nodes = sorted(list(self.G0.nodes()))
                node_to_idx = {n: i for i, n in enumerate(nodes)}
                size = len(nodes)
                adj = np.zeros((size, size))
                for u, v, d in self.G0.edges(data=True):
                    i, j = node_to_idx[u], node_to_idx[v]
                    w = d.get('weight', 1.0)
                    adj[i,j] = adj[j,i] = w
                
                pt = sip.PartitionTree(adj)
                k = max(2, len(self.levels))
                pt.build_encoding_tree(k)
                sip_val = round(pt.entropy(), 6)
            except Exception as e:
                print(f"SIP Error: {e}")

        return {
            "se_1d_base": round(se_1d_base, 6),
            "se_1d_curr": round(se_1d_curr, 6),
            "se_2d": round(se_2d, 6), 
            "h_tree": round(h_tree_total, 6),
            "q": round(mod_q, 6), 
            "vol_total": vol_total,
            "traces": traces,
            "sip_optimal": sip_val
        }

lab = LabManager()

@app.route('/api/state')
def api_state():
    curr = lab.get_current()
    metrics = lab.calculate_metrics()
    
    # Current level graph elements
    elements = [{"data": {"id": str(n)}} for n in curr["G"].nodes()]
    for u, v, d in curr["G"].edges(data=True):
        elements.append({"data": {
            "id": f"e-{u}-{v}",
            "source": str(u), 
            "target": str(v), 
            "weight": d.get('weight', 1.0)
        }})

    # All level edges for 3D visualization
    all_level_edges = []
    for l_idx, lvl in enumerate(lab.levels):
        for u, v, d in lvl["G"].edges(data=True):
            all_level_edges.append({
                "level": l_idx,
                "source": f"L{l_idx}_{u}",
                "target": f"L{l_idx}_{v}",
                "weight": d.get('weight', 1.0)
            })

    return jsonify({
        "elements": elements, 
        "partition": curr["partition"], 
        "metrics": metrics, 
        "label": curr["label"],
        "history": [lvl["label"] for lvl in lab.levels],
        "current_idx": lab.current_level,
        "tree": lab.get_encoding_tree(),
        "level_edges": all_level_edges
    })

@app.route('/api/switch_level', methods=['POST'])
def switch_level():
    lab.current_level = int(request.json['idx'])
    return jsonify({"status": "ok"})

@app.route('/api/update_node', methods=['POST'])
def update_node():
    lab.move_node(request.json['id'], request.json['comm'])
    return jsonify({"status": "ok"})

@app.route('/api/update_edge', methods=['POST'])
def update_edge():
    u, v, w = request.json['u'], request.json['v'], float(request.json['weight'])
    curr = lab.get_current()
    if curr["G"].has_edge(u, v): curr["G"][u][v]['weight'] = w
    return jsonify({"status": "ok"})

@app.route('/api/merge', methods=['POST'])
def api_merge():
    success = lab.merge_to_next_level()
    return jsonify({"status": "ok" if success else "failed"})

@app.route('/api/preset', methods=['POST'])
def api_preset():
    lab.load_preset(request.json['type'])
    return jsonify({"status": "ok"})

@app.route('/api/suggest', methods=['POST'])
def api_suggest():
    curr = lab.get_current()
    G, partition = curr["G"], curr["partition"]
    base_metrics = lab.calculate_metrics()
    base_se = base_metrics["se_2d"]
    
    import random
    nodes = list(G.nodes())
    random.shuffle(nodes)
    
    test_partition = partition.copy()
    
    for n in nodes:
        old_comm = test_partition[n]
        neigh_comms = {test_partition[nb] for nb in G.neighbors(n)}
        if test_partition:
             neigh_comms.add(max(test_partition.values()) + 1)
        
        for t in neigh_comms:
            if t == old_comm: continue
            test_partition[n] = t
            new_m = lab.calculate_metrics(partition_override=test_partition)
            if new_m["se_2d"] < base_se - 1e-8:
                return jsonify({"best_move": {"node": n, "to": int(t)}})
            test_partition[n] = old_comm
    return jsonify({"best_move": None})

@app.route('/api/wiki/<name>')
def api_wiki(name):
    filename = "wiki_structural_entropy.md" if name == "structural_entropy" else f"wiki_{name}.md"
    wiki_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(wiki_path):
        with open(wiki_path, 'r') as f:
            return jsonify({"content": f.read()})
    return jsonify({"content": f"Wiki '{name}' not found."})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use port 8000 for standard access
    app.run(host='0.0.0.0', port=8006, debug=False)
