"""
=============================================================
  Task Scheduler Optimization System
  Module: sorter.py
  Purpose: Sorting strategies for task scheduling
  DSA Concepts: Sorting, Comparators, Greedy Ordering
=============================================================

SORTING STRATEGIES:
───────────────────
1. By Deadline (EDF – Earliest Deadline First)
   → Minimize missed deadlines
   → Optimal for real-time systems

2. By Priority (HPF – Highest Priority First)
   → Maximize priority-weighted completion

3. By Profit (Greedy Job Scheduling)
   → Maximize total profit earned

4. By Profit/Exec Ratio (Efficiency-Based)
   → Best profit per unit time

5. Combined Score (Weighted multi-criteria)
   → Balances all factors together
"""


def sort_by_deadline(tasks: list) -> list:
    """
    Earliest Deadline First (EDF).
    Tasks with closer deadlines are scheduled first.
    Tie-break: higher profit wins.
    Time: O(n log n)
    """
    return sorted(tasks, key=lambda t: (t.deadline, -t.profit))


def sort_by_priority(tasks: list) -> list:
    """
    Highest Priority First (HPF).
    Tasks with highest priority value scheduled first.
    Tie-break: earlier deadline wins.
    Time: O(n log n)
    """
    return sorted(tasks, key=lambda t: (-t.priority, t.deadline))


def sort_by_profit(tasks: list) -> list:
    """
    Greedy Job Scheduling by Profit.
    Most profitable tasks selected first.
    Tie-break: shorter execution time wins.
    Time: O(n log n)
    """
    return sorted(tasks, key=lambda t: (-t.profit, t.exec_time))


def sort_by_efficiency(tasks: list) -> list:
    """
    Efficiency = Profit / Execution Time.
    Best 'bang for buck' tasks scheduled first.
    Used in fractional knapsack-style analysis.
    Time: O(n log n)
    """
    return sorted(tasks, key=lambda t: (-(t.profit / t.exec_time), t.deadline))


def sort_combined(tasks: list,
                  w_priority: float = 0.3,
                  w_deadline:  float = 0.3,
                  w_profit:    float = 0.4) -> list:
    """
    Multi-criteria weighted scoring.
    Score = w_priority * norm(priority) + w_deadline * norm(1/deadline) + w_profit * norm(profit)
    Allows custom weighting between factors.
    Time: O(n log n)
    """
    if not tasks:
        return []

    max_priority = max(t.priority  for t in tasks)
    max_deadline = max(t.deadline  for t in tasks)
    max_profit   = max(t.profit    for t in tasks)

    # Avoid division by zero
    max_priority = max_priority if max_priority > 0 else 1
    max_deadline = max_deadline if max_deadline > 0 else 1
    max_profit   = max_profit   if max_profit   > 0 else 1

    def combined_score(t):
        norm_priority = t.priority / max_priority
        # Inverted deadline: tasks with LOWER deadline get higher urgency score
        norm_urgency  = (max_deadline - t.deadline + 1) / max_deadline
        norm_profit   = t.profit / max_profit
        score = (w_priority * norm_priority +
                 w_deadline * norm_urgency  +
                 w_profit   * norm_profit)
        return -score   # Negative for ascending sort → highest score first

    return sorted(tasks, key=combined_score)


def display_sorted_tasks(tasks: list, method_name: str) -> None:
    """Pretty-print the sorted task list in a table format."""
    print(f"\n  ┌{'─'*62}┐")
    print(f"  │  SORTED TASKS — Method: {method_name:<35}│")
    print(f"  ├{'─'*7}┬{'─'*18}┬{'─'*8}┬{'─'*8}┬{'─'*8}┬{'─'*8}┤")
    print(f"  │ {'ID':<5} │ {'Name':<16} │ {'Priority':^6} │ {'Deadline':^6} │ {'ExecTime':^6} │ {'Profit':^6} │")
    print(f"  ├{'─'*7}┼{'─'*18}┼{'─'*8}┼{'─'*8}┼{'─'*8}┼{'─'*8}┤")

    for rank, t in enumerate(tasks, 1):
        print(f"  │ {rank:<5} │ {t.name:<16} │ {t.priority:^6} │ "
              f"{t.deadline:^6} │ {t.exec_time:^6} │ {t.profit:^6} │")

    print(f"  └{'─'*7}┴{'─'*18}┴{'─'*8}┴{'─'*8}┴{'─'*8}┴{'─'*8}┘")
    print(f"  Total tasks: {len(tasks)}\n")
