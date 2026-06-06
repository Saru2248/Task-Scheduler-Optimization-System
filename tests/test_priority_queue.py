"""
=============================================================
  Task Scheduler Optimization System
  File   : tests/test_priority_queue.py
  Purpose: Unit tests for MaxHeapPriorityQueue
=============================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.task           import Task
from src.priority_queue import MaxHeapPriorityQueue


def make_task(tid, name, profit, deadline=10, exec_time=1, priority=5):
    return Task(tid, name, priority, deadline, exec_time, profit)


class TestMaxHeapPriorityQueue:

    def setup_method(self):
        """Fresh heap before each test."""
        self.pq = MaxHeapPriorityQueue()

    # ── Empty state ──────────────────────────────────────────

    def test_empty_on_creation(self):
        assert self.pq.is_empty() is True
        assert self.pq.size() == 0

    def test_peek_empty_returns_none(self):
        assert self.pq.peek() is None

    def test_extract_empty_returns_none(self):
        assert self.pq.extract_max() is None

    # ── Single element ───────────────────────────────────────

    def test_insert_one(self):
        t = make_task(1, "Solo", 50)
        self.pq.insert(t)
        assert self.pq.size() == 1
        assert self.pq.peek() == t

    def test_extract_single_element(self):
        t = make_task(1, "Solo", 50)
        self.pq.insert(t)
        result = self.pq.extract_max()
        assert result == t
        assert self.pq.is_empty()

    # ── Max-heap property ────────────────────────────────────

    def test_max_profit_always_at_top(self):
        tasks = [
            make_task(1, "Low",    profit=10),
            make_task(2, "High",   profit=90),
            make_task(3, "Medium", profit=50),
        ]
        for t in tasks:
            self.pq.insert(t)
        assert self.pq.peek().profit == 90

    def test_extract_order_descending(self):
        profits = [30, 70, 10, 90, 50]
        for i, p in enumerate(profits, 1):
            self.pq.insert(make_task(i, f"T{i}", p))

        extracted = []
        while not self.pq.is_empty():
            extracted.append(self.pq.extract_max().profit)

        assert extracted == sorted(profits, reverse=True)

    # ── Build from list ──────────────────────────────────────

    def test_build_from_list(self):
        tasks = [make_task(i, f"T{i}", i * 10) for i in range(1, 6)]
        self.pq.build_from_list(tasks)
        assert self.pq.size() == 5
        assert self.pq.peek().profit == 50   # highest = T5 (profit=50)

    def test_build_and_extract_all(self):
        profits = [15, 25, 5, 40, 30]
        tasks   = [make_task(i, f"T{i}", p) for i, p in enumerate(profits, 1)]
        self.pq.build_from_list(tasks)

        result = []
        while not self.pq.is_empty():
            result.append(self.pq.extract_max().profit)

        assert result == sorted(profits, reverse=True)

    # ── to_sorted_list ───────────────────────────────────────

    def test_to_sorted_list(self):
        profits = [60, 20, 80, 40]
        tasks   = [make_task(i, f"T{i}", p) for i, p in enumerate(profits, 1)]
        self.pq.build_from_list(tasks)

        sorted_list = self.pq.to_sorted_list()
        assert [t.profit for t in sorted_list] == sorted(profits, reverse=True)
        assert self.pq.is_empty()   # heap should be empty after

    # ── Size tracking ────────────────────────────────────────

    def test_size_tracks_inserts_and_extracts(self):
        for i in range(5):
            self.pq.insert(make_task(i + 1, f"T{i}", i * 10))
        assert self.pq.size() == 5

        self.pq.extract_max()
        assert self.pq.size() == 4

        self.pq.extract_max()
        assert self.pq.size() == 3

    # ── Duplicate profits ────────────────────────────────────

    def test_duplicate_profits(self):
        for i in range(1, 4):
            self.pq.insert(make_task(i, f"T{i}", 50))
        # All profits equal, all should extract without error
        extracted = [self.pq.extract_max().profit for _ in range(3)]
        assert all(p == 50 for p in extracted)
        assert self.pq.is_empty()
