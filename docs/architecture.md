# Task Scheduler Optimization System — Architecture

This document describes the design, data structures, and algorithmic flows used in the **Task Scheduler Optimization System**.

---

## 1. System Components & Workflow

```
[Task Input (CSV/CLI)]
        │
        ▼
[Task Validation (validator.py)] ──(Invalid Tasks)──► [Validation Error Report]
        │
        ▼ (Valid Tasks)
[Sorting Engine (sorter.py)] ◄───► [Max-Heap Priority Queue (priority_queue.py)]
        │
        ▼
[Scheduling Algorithms (scheduler.py)]
  ├── Greedy Deadline Scheduler (Job Scheduling)
  ├── Priority Queue Scheduler (Heap-based HPF)
  ├── Earliest Deadline First (EDF)
  └── Shortest Job First (SJF)
        │
        ▼
[Timeline & Metrics Engine (report.py)] ────► [Terminal Output / Gantt Chart]
                                        ├──► [CSV Data Export]
                                        └──► [Detailed Text Report]
```

### Workflow Steps
1. **Task Input**: User inputs tasks via an interactive CLI prompt or by loading a pre-configured CSV dataset from the `data/` folder.
2. **Task Validation**: The validation engine ensures metadata compliance (e.g. positive IDs, priority bounded [1-10], deadline values, exec_time <= deadline).
3. **Task Sorting & Heap Operations**: 
   - Tasks are either sorted in-place (for algorithms like EDF, SJF) using Python's Timsort algorithm.
   - Or they are loaded into a custom-implemented **Binary Max-Heap Priority Queue** (from scratch) for profit-based prioritisation.
4. **Optimization & Selection**: The core scheduler runs the selected algorithm to calculate execution start and finish times.
5. **Report & Analysis**: Performance metrics (Completion Rate, Total Profit Earned, Average Execution Time) are generated, printed, and exported to CSV and text reports.

---

## 2. Core Data Structures & Complexities

| Data Structure / Operation | Description | Time Complexity | Space Complexity |
|:---|:---|:---|:---|
| **Task Model** | Encapsulates ID, priority, deadline, exec time, and profit. | $O(1)$ creation | $O(1)$ |
| **Max-Heap Insertion** | Bubbles up a newly added task based on profit. | $O(\log n)$ | $O(1)$ |
| **Max-Heap Extract Max** | Swaps root and last element, then bubbles down. | $O(\log n)$ | $O(1)$ |
| **Max-Heap Build** | Floyd's heap construction from unsorted list. | $O(n)$ | $O(1)$ |
| **Sorting Strategies** | Deadline, Profit, Priority, and combined scoring. | $O(n \log n)$ | $O(n)$ |

---

## 3. Algorithmic Comparison

* **Greedy Deadline Scheduler** (Job Scheduling):
  - **Logic**: Sort by profit descending. Try to schedule each task in its latest possible free slot $\le$ deadline.
  - **Optimal for**: Profit maximization.

* **Priority Queue Scheduler**:
  - **Logic**: Build a Max-Heap. Pop the highest profit task, execute immediately if it fits before deadline.
  - **Optimal for**: Dynamic systems where tasks arrive continuously.

* **Earliest Deadline First (EDF)**:
  - **Logic**: Sort by deadline ascending. Execute sequentially.
  - **Optimal for**: Minimizing missed deadlines.

* **Shortest Job First (SJF)**:
  - **Logic**: Sort by execution time ascending. Execute sequentially.
  - **Optimal for**: Minimizing waiting time / turnaround time.
