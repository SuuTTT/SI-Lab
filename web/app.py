from flask import Flask, render_template, jsonify, request
import networkx as nx
import math
import numpy as np

app = Flask(__name__)

# Default Graph: 5 nodes, 2 communities
def get_default_graph():
    G = nx.Graph()
    # Community 1
    G.add_edge(0, 1, weight=10)
    G.add_edge(0, 2, weight=10)
    G.add_edge(1, 2, weight=10)
    # Community 2
    G.add_edge(3, 4, weight=10)
    # Bridge
    G.add_edge(2, 3, weight=1)
    return G

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph')
def get_graph():
    G = get_default_graph()
    nodes = [{"data": {"id": str(n), "label": f"Node {n}"}} for n in G.nodes()]
    edges = [{"data": {"source": str(u), "target": str(v), "weight": d['weight']}} for u, v, d in G.edges(data=True)]
    return jsonify({"nodes": nodes, "edges": edges})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    partition = data.get('partition', {}) # {node_id: community_id}
    G = get_default_graph()
    
    vol_total = sum(dict(G.degree(weight='weight')).values())
    communities = {}
    for node, comm in partition.items():
        if comm not in communities: communities[comm] = []
        communities[comm].append(int(node))
    
    steps = []
    total_entropy = 0
    
    steps.append({"msg": f"Total Volume (VOL) = {vol_total}"})
    
    for comm_id, nodes in communities.items():
        v_c = sum(dict(G.degree(nodes, weight='weight')).values())
        g_c = nx.cut_size(G, nodes, weight='weight')
        
        # Calculation for this community
        if v_c > 0:
            term = - (g_c / vol_total) * math.log2(v_c / vol_total)
            total_entropy += term
            steps.append({
                "msg": f"Community {comm_id}: Nodes {nodes}",
                "v_c": v_c,
                "g_c": g_c,
                "entropy_contribution": f"-({g_c}/{vol_total}) * log2({v_c}/{vol_total}) = {term:.4f}"
            })
            
    return jsonify({
        "total_entropy": total_entropy,
        "steps": steps,
        "formula": "H(G, P) = \\sum_{C \\in P} - \\frac{g_C}{VOL} \\log_2 \\frac{V_C}{VOL}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6789, debug=True)
