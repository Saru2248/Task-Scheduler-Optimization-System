"""
=============================================================
  Task Scheduler Optimization System
  Module: scheduler.py
  Purpose: Core scheduling algorithms
  DSA Concepts:
    - Greedy Algorithm
    - Priority Queue (Max-Heap)
    - Job Scheduling Problem
    - Interval Scheduling
=============================================================

ALGORITHMS IMPLEMENTED:
────────────────────────
1. GREEDY DEADLINE SCHEDULER  (classic Job Scheduling Problem)
   ─ Sort tasks by profit (descending)
   ─ Assign each task to the latest available slot before its deadline
   ─ Guarantees maximum profit
   ─ Time: O(n² ) with array, O(n log n) with Union-Find

2. PRIORITY QUEUE SCHEDULER
   ─ Insert all tasks into Max-Heap by profit
   ─ Always process highest-profit task next
   ─ Check if it fits within deadline; schedule or miss
   ─ Time: O(n log n)

3. EARLIEST DEADLINE FIRST (EDF)
   ─ Always schedule the task whose deadline is soonest
   ─ Minimizes number of missed deadlines
   ─ Optimal for preemptive real-time systems
   ─ Time: O(n log n)

4. SHORTEST JOB FIRST (SJF)
   ─ Schedule the task with shortest execution time first
   ─ Minimizes average waiting time
   ─ Time: O(n log n)
"""

from src.priority_queue import MaxHeapPriorityQueue
from src.sorter import (sort_by_deadline, sort_by_profit,
                        sort_by_priority, sort_by_efficiency)


# ─────────────────────────────────────────────────────────────
#  RESULT CONTAINER
# ─────────────────────────────────────────────────────────────

class ScheduleResult:
    """Holds the complete output of a scheduling algorithm."""

    def __init__(self, algorithm_name: str):
        self.algorithm_name  = algorithm_name
        self.scheduled_tasks = []   # Tasks successfully scheduled
        self.missed_tasks    = []   # Tasks that could NOT be scheduled
        self.timeline        = []   # List of (start, end, task) tuples
        self.total_profit    = 0
        self.total_exec_time = 0

    def add_scheduled(self, task, start: int, finish: int):
        task.scheduled   = True
        task.start_time  = start
        task.finish_time = finish
        self.scheduled_tasks.append(task)
        self.timeline.append((start, finish, task))
        self.total_profit    += task.profit
        self.total_exec_time += task.exec_time

    def add_missed(self, task):
        task.scheduled = False
        self.missed_tasks.append(task)

    @property
    def total_tasks(self):
        return len(self.scheduled_tasks) + len(self.missed_tasks)

    @property
    def completion_rate(self):
        if self.total_tasks == 0:
            return 0.0
        return len(self.scheduled_tasks) / self.total_tasks * 100


# ─────────────────────────────────────────────────────────────
#  ALGORITHM 1: GREEDY DEADLINE SCHEDULER
#  (Classic Job Scheduling Problem — Profit Maximization)
# ─────────────────────────────────────────────────────────────

def greedy_deadline_scheduler(tasks: list) -> ScheduleResult:
    """
    Classic Greedy Job Scheduling Algorithm.

    Goal: Maximize total profit while meeting deadlines.

    Steps:
      1. Sort all tasks by profit (descending)
      2. Find the maximum deadline → defines time slots [1 … max_deadline]
      3. For each task (in profit order):
           → Find the latest FREE slot ≤ task.deadline
           → If found: assign task to that slot (scheduled)
           → If not found: task is missed
      4. Report schedule

    Why Greedy works here:
      → Taking the highest-profit task first and fitting it as LATE
        as possible (to leave early slots free for other tasks)
        guarantees the globally optimal solution.

    Time Complexity: O(n²) — n tasks × n slots worst case
    Space Complexity: O(n) — slot array
    """
    result = ScheduleResult("Greedy Deadline Scheduler")

    if not tasks:
        return result

    # Step 1: Sort by profit descending
    sorted_tasks = sort_by_profit(tasks)

    # Step 2: Create slot array
    max_deadline = max(t.deadline for t in sorted_tasks)
    # slots[i] = None means slot i is FREE (1-indexed, slot 0 unused)
    slots = [None] * (max_deadline + 1)

    # Step 3: Assign tasks to slots
    for task in sorted_tasks:
        # Try to fit task in the latest free slot ≤ deadline
        placed = False
        # Search from deadline down to slot 1
        for slot in range(min(task.deadline, max_deadline), 0, -1):
            if slots[slot] is None:
                slots[slot] = task
                placed = True
                break

        if not placed:
            result.add_missed(task)

    # Step 4: Build ordered timeline from slots
    current_time = 0
    for slot in range(1, max_deadline + 1):
        if slots[slot] is not None:
            task = slots[slot]
            start  = current_time
            finish = current_time + task.exec_time
            result.add_scheduled(task, start, finish)
            current_time = finish

    return result


# ─────────────────────────────────────────────────────────────
#  ALGORITHM 2: PRIORITY QUEUE SCHEDULER
#  (Max-Heap based — always pick highest profit available)
# ─────────────────────────────────────────────────────────────

def priority_queue_scheduler(tasks: list) -> ScheduleResult:
    """
    Priority Queue (Max-Heap) Scheduler.

    Goal: Always execute the highest-profit task that can finish
          before its deadline given the current time.

    Steps:
      1. Insert all tasks into a Max-Heap (by profit)
      2. current_time = 0
      3. Extract max from heap
         → If current_time + exec_time <= deadline: SCHEDULE it
         → Else: MISS it
         → Repeat until heap empty

    This is a simplified non-preemptive simulation.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    result = ScheduleResult("Priority Queue Scheduler")

    if not tasks:
        return result

    # Build max-heap from task list
    pq = MaxHeapPriorityQueue()
    pq.build_from_list(tasks)

    current_time = 0

    while not pq.is_empty():
        task = pq.extract_max()   # Highest-profit task

        finish = current_time + task.exec_time

        if finish <= task.deadline:
            # Task can finish before deadline → schedule it
            result.add_scheduled(task, current_time, finish)
            current_time = finish
        else:
            # Task cannot finish in time → miss it
            result.add_missed(task)

    return result


# ─────────────────────────────────────────────────────────────
#  ALGORITHM 3: EARLIEST DEADLINE FIRST (EDF)
# ─────────────────────────────────────────────────────────────

def earliest_deadline_first(tasks: list) -> ScheduleResult:
    """
    Earliest Deadline First (EDF) Scheduler.

    Goal: Minimize the number of missed deadlines.

    Steps:
      1. Sort all tasks by deadline (ascending)
      2. Schedule each task sequentially
         → If current_time + exec_time <= deadline: SCHEDULE
         → Else: MISS

    EDF is provably optimal for minimizing missed tasks
    in non-preemptive scheduling with unit time slots.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    result = ScheduleResult("Earliest Deadline First (EDF)")

    if not tasks:
        return result

    sorted_tasks = sort_by_deadline(tasks)
    current_time = 0

    for task in sorted_tasks:
        finish = current_time + task.exec_time

        if finish <= task.deadline:
            result.add_scheduled(task, current_time, finish)
            current_time = finish
        else:
            result.add_missed(task)

    return result


# ─────────────────────────────────────────────────────────────
#  ALGORITHM 4: SHORTEST JOB FIRST (SJF)
# ─────────────────────────────────────────────────────────────

def shortest_job_first(tasks: list) -> ScheduleResult:
    """
    Shortest Job First (SJF) Scheduler.

    Goal: Minimize average waiting time.

    Steps:
      1. Sort tasks by execution time (ascending)
      2. Schedule each task sequentially
         → If task fits before deadline: SCHEDULE
         → Else: MISS

    SJF is optimal for minimizing average turnaround time
    in non-preemptive batch scheduling environments.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    result = ScheduleResult("Shortest Job First (SJF)")

    if not tasks:
        return result

    # Sort by execution time ascending; tie-break by profit descending
    sorted_tasks = sorted(tasks, key=lambda t: (t.exec_time, -t.profit))
    current_time = 0

    for task in sorted_tasks:
        finish = current_time + task.exec_time

        if finish <= task.deadline:
            result.add_scheduled(task, current_time, finish)
            current_time = finish
        else:
            result.add_missed(task)

    return result


# ─────────────────────────────────────────────────────────────
#  COMPARISON RUNNER
# ─────────────────────────────────────────────────────────────

def run_all_algorithms(tasks: list) -> dict:
    """
    Run all 4 scheduling algorithms on the same task list.
    Returns a dictionary of {algorithm_name: ScheduleResult}.
    Useful for performance comparison.
    """
    # Deep copy tasks for each algorithm so they don't interfere
    import copy

    results = {}
    algorithms = {
        "Greedy"  : greedy_deadline_scheduler,
        "PQ Heap" : priority_queue_scheduler,
        "EDF"     : earliest_deadline_first,
        "SJF"     : shortest_job_first,
    }

    for name, algo in algorithms.items():
        tasks_copy = copy.deepcopy(tasks)
        results[name] = algo(tasks_copy)

    return results
