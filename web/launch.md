# SI-Lab Launch Guide

This document contains the instructions and direct links to launch the Structural Information (SI) Lab ecosystem.

## 1. Quick Launch: Lab Visualizer
The visualizer is a single-file interactive tool designed for real-time validation of structural entropy calculations.

**Run Command:**
```bash
python3 /workspace/test_simple.py
```

**Access URL:**
- [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Key Features:**
- **Manual Partitioning:** Tap nodes to cycle through 4 community colors.
- **Check Current Entropy:** Live calculation of $H(G, \mathcal{P})$ using the core 2D formula.
- **Find Best Move:** AI-driven greedy suggestion to find the mathematically optimal next move (Louvain-style).

---

## 2. Core Benchmark Suite
Run the comprehensive benchmark to compare the refactored SI optimizers against original `sip.py` and community baselines like Leiden.

**Run Command:**
```bash
python3 /workspace/SI-Lab/benchmarks/run_benchmark.py
```

**Outputs:**
- Accuracy Metrics: NMI, ARI, Modularity.
- Entropy Validation: Structural Entropy ($H$) values.
- Plots: [SI-Lab/benchmarks/si_comparison_plot.png](SI-Lab/benchmarks/si_comparison_plot.png)

---

## 3. Project Structure
- [/workspace/SI-Lab/core/](/workspace/SI-Lab/core/): Refactored high-performance optimizers (`louvain_optimizer.py`, `greedy_si.py`).
- [/workspace/sip.py](/workspace/sip.py): Original hierarchical SIHD implementation.
- [/workspace/test_simple.py](/workspace/test_simple.py): Self-contained web visualizer (Flask/Cytoscape.js).

---

## 4. Troubleshooting
If the web page fails to load:
1. Ensure Port `8000` is forwarded in your VS Code terminal.
2. If you see "Address already in use", run:
   ```bash
   pkill -f test_simple.py
   ```
3. Refresh [http://127.0.0.1:8000](http://127.0.0.1:8000).
