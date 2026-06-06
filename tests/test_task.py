"""
=============================================================
  Task Scheduler Optimization System
  File   : tests/test_task.py
  Purpose: Unit tests for the Task class
=============================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.task import Task


class TestTaskCreation:

    def test_valid_task_creation(self):
        """Task is created correctly with valid inputs."""
        t = Task(1, "My Task", 5, 10, 3, 50)
        assert t.task_id == 1
        assert t.name == "My Task"
        assert t.priority == 5
        assert t.deadline == 10
        assert t.exec_time == 3
        assert t.profit == 50
        assert t.scheduled is False
        assert t.start_time is None
        assert t.finish_time is None

    def test_invalid_task_id_zero(self):
        with pytest.raises(ValueError, match="task_id must be a positive integer"):
            Task(0, "Task", 5, 10, 3, 50)

    def test_invalid_task_id_negative(self):
        with pytest.raises(ValueError):
            Task(-1, "Task", 5, 10, 3, 50)

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="non-empty string"):
            Task(1, "", 5, 10, 3, 50)

    def test_priority_too_low(self):
        with pytest.raises(ValueError, match="Priority must be between"):
            Task(1, "Task", 0, 10, 3, 50)

    def test_priority_too_high(self):
        with pytest.raises(ValueError, match="Priority must be between"):
            Task(1, "Task", 11, 10, 3, 50)

    def test_deadline_zero_raises(self):
        with pytest.raises(ValueError, match="Deadline must be"):
            Task(1, "Task", 5, 0, 3, 50)

    def test_exec_time_zero_raises(self):
        with pytest.raises(ValueError, match="Execution time must be positive"):
            Task(1, "Task", 5, 10, 0, 50)

    def test_negative_profit_raises(self):
        with pytest.raises(ValueError, match="Profit cannot be negative"):
            Task(1, "Task", 5, 10, 3, -1)

    def test_boundary_priority_1(self):
        t = Task(1, "Task", 1, 10, 3, 50)
        assert t.priority == 1

    def test_boundary_priority_10(self):
        t = Task(1, "Task", 10, 10, 3, 50)
        assert t.priority == 10

    def test_zero_profit_allowed(self):
        t = Task(1, "Free Task", 5, 10, 2, 0)
        assert t.profit == 0

    def test_to_dict(self):
        t = Task(1, "My Task", 5, 10, 3, 50)
        d = t.to_dict()
        assert d["task_id"] == 1
        assert d["name"] == "My Task"
        assert d["scheduled"] is False

    def test_comparison_higher_profit_less(self):
        """__lt__ should return True when self has HIGHER profit (max-heap order)."""
        t1 = Task(1, "A", 5, 10, 2, 100)
        t2 = Task(2, "B", 5, 10, 2, 50)
        assert t1 < t2   # t1 has higher profit → "less" in heap order

    def test_repr(self):
        t = Task(1, "My Task", 5, 10, 3, 50)
        r = repr(t)
        assert "My Task" in r
        assert "profit=50" in r
