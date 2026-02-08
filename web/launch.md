# SI-Lab Launch Guide

This document contains the instructions and direct links to launch the Structural Information (SI) Lab ecosystem.

## 1. Quick Launch: Lab Visualizer
The visualizer is an interactive tool designed for real-time validation of structural entropy calculations.

**Run Command:**
```bash
python3 /workspace/SI-Lab/web/app.py
```

**Access URL:**
- [http://127.0.0.1:8002](http://127.0.0.1:8002)

**Port Note:** We use port `8002` because macOS (Monterey+) reserves port `8000` and `5000` for system services (AirPlay Receiver), which often blocks local access even if the remote server is running.

**Key Features:**
- **Hierarchical View:** Switch between aggregated levels (L0, L1...).
- **Tree Inspector:** Click tree nodes to see the exact SI contribution formula.
- **Auto Louvain:** Runs the greedy SI minimize algorithm step-by-step.

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
- [/workspace/SI-Lab/web/app.py](/workspace/SI-Lab/web/app.py): Integrated Flask server.
- [/workspace/SI-Lab/web/templates/](/workspace/SI-Lab/web/templates/): Frontend UI.

---

## 4. Troubleshooting
If the web page fails to load:
1. Ensure Port `8002` is forwarded in your VS Code terminal.
2. If you see "Address already in use", run:
   ```bash
   pkill -9 -f app.py
   ```
3. **macOS Conflict:** If you cannot see the page on `8000`, it is likely due to the macOS "AirPlay Receiver" occupy. Switching to `8002` as we have done is the standard fix.
   ```
3. Refresh [http://127.0.0.1:8000](http://127.0.0.1:8000).
