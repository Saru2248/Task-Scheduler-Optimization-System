"""
=============================================================
  Task Scheduler Optimization System
  File   : tests/test_scheduler.py
  Purpose: Unit tests for Scheduling Algorithms
=============================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.task      import Task
from src.scheduler import (greedy_deadline_scheduler,
                           priority_queue_scheduler,
                           earliest_deadline_first,
                           shortest_job_first)


def make_tasks():
    return [
        Task(1, "T1", priority=9,  deadline=4, exec_time=1, profit=90),
        Task(2, "T2", priority=8,  deadline=3, exec_time=2, profit=80),
        Task(3, "T3", priority=7,  deadline=5, exec_time=1, profit=70),
    ]


class TestSchedulers:

    def test_greedy_deadline_scheduler(self):
        tasks = make_tasks()
        result = greedy_deadline_scheduler(tasks)
        
        # Max profit possible here is all tasks: T1 (90) + T2 (80) + T3 (70) = 240
        # Let's check if they fit:
        # T1 (d=4, e=1) -> slot 4
        # T2 (d=3, e=2) -> slots 2 and 3
        # T3 (d=5, e=1) -> slot 5
        # They should all be scheduled.
        assert len(result.scheduled_tasks) == 3
        assert len(result.missed_tasks) == 0
        assert result.total_profit == 240

    def test_priority_queue_scheduler(self):
        tasks = make_tasks()
        result = priority_queue_scheduler(tasks)
        
        # PQ Scheduler processes by max profit:
        # T1 (profit=90, d=4, e=1) -> current_time=0. finish=1 <= 4 (scheduled). current_time=1
        # T2 (profit=80, d=3, e=2) -> current_time=1. finish=3 <= 3 (scheduled). current_time=3
        # T3 (profit=70, d=5, e=1) -> current_time=3. finish=4 <= 5 (scheduled). current_time=4
        assert len(result.scheduled_tasks) == 3
        assert result.total_profit == 240

    def test_earliest_deadline_first(self):
        tasks = make_tasks()
        result = earliest_deadline_first(tasks)
        
        # EDF sorts by deadline:
        # T2 (d=3, e=2) -> current_time=0, finish=2 <= 3 (scheduled). current_time=2
        # T1 (d=4, e=1) -> current_time=2, finish=3 <= 4 (scheduled). current_time=3
        # T3 (d=5, e=1) -> current_time=3, finish=4 <= 5 (scheduled). current_time=4
        assert len(result.scheduled_tasks) == 3
        assert result.total_profit == 240

    def test_shortest_job_first(self):
        tasks = make_tasks()
        result = shortest_job_first(tasks)
        
        # SJF sorts by exec_time:
        # T1 (e=1, profit=90, d=4) -> finish=1 <= 4 (scheduled). current_time=1
        # T3 (e=1, profit=70, d=5) -> finish=2 <= 5 (scheduled). current_time=2
        # T2 (e=2, profit=80, d=3) -> finish=4 > 3 (missed).
        assert len(result.scheduled_tasks) == 2
        assert len(result.missed_tasks) == 1
