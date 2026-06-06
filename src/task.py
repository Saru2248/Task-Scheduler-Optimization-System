"""
=============================================================
  Task Scheduler Optimization System
  Module: task.py
  Purpose: Defines the Task data model
  Author: Student DSA Project
=============================================================
"""

class Task:
    """
    Represents a single schedulable task with all its attributes.

    Attributes:
        task_id  (int)  : Unique identifier for the task
        name     (str)  : Human-readable task name
        priority (int)  : Priority level (1 = lowest, 10 = highest)
        deadline (int)  : Deadline in time units (e.g., slot 1, 2, 3 …)
        exec_time(int)  : Execution time required (in time units)
        profit   (int)  : Profit/importance score gained if completed on time
    """

    def __init__(self, task_id: int, name: str, priority: int,
                 deadline: int, exec_time: int, profit: int):
        # --- Validate inputs ------------------------------------------------
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"task_id must be a positive integer. Got: {task_id}")
        if not name or not isinstance(name, str):
            raise ValueError("Task name must be a non-empty string.")
        if not (1 <= priority <= 10):
            raise ValueError(f"Priority must be between 1 and 10. Got: {priority}")
        if deadline <= 0:
            raise ValueError(f"Deadline must be a positive integer. Got: {deadline}")
        if exec_time <= 0:
            raise ValueError(f"Execution time must be positive. Got: {exec_time}")
        if profit < 0:
            raise ValueError(f"Profit cannot be negative. Got: {profit}")

        # --- Assign attributes ----------------------------------------------
        self.task_id   = task_id
        self.name      = name
        self.priority  = priority
        self.deadline  = deadline
        self.exec_time = exec_time
        self.profit    = profit

        # Status set after scheduling
        self.scheduled   = False   # Was the task scheduled?
        self.start_time  = None    # When does execution begin?
        self.finish_time = None    # When does execution finish?

    # -------------------------------------------------------------------------
    # Comparison operators (used by heapq / sorting)
    # We compare by NEGATIVE profit so that heapq (min-heap) acts as max-heap
    # -------------------------------------------------------------------------
    def __lt__(self, other):
        return self.profit > other.profit   # higher profit = higher priority

    def __repr__(self):
        return (f"Task(id={self.task_id}, name='{self.name}', "
                f"priority={self.priority}, deadline={self.deadline}, "
                f"exec_time={self.exec_time}, profit={self.profit})")

    def to_dict(self) -> dict:
        """Convert task to a dictionary (for CSV / JSON export)."""
        return {
            "task_id"    : self.task_id,
            "name"       : self.name,
            "priority"   : self.priority,
            "deadline"   : self.deadline,
            "exec_time"  : self.exec_time,
            "profit"     : self.profit,
            "scheduled"  : self.scheduled,
            "start_time" : self.start_time,
            "finish_time": self.finish_time,
        }
