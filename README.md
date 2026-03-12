# TSP Simulator - Algorithmic Analysis Project

Interactive visualization tool for comparing Travelling Salesman Problem algorithms.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python src/main.py
```

## Features

- **Playground Tab**: Create cities by clicking or generate random/preset configurations
- **Visualization Tab**: Watch algorithms solve TSP step-by-step
- **Comparison Tab**: Compare all algorithms on the same city set

## Algorithms Implemented

1. **Brute Force** - Optimal solution, O(n!)
2. **Nearest Neighbor** - Fast greedy heuristic, O(n²)
3. **2-Opt** - Local search improvement, O(n²) per iteration
