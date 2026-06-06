"""
=============================================================
  Task Scheduler Optimization System
  Module: data_loader.py
  Purpose: Load tasks from CSV file or inline sample data
=============================================================
"""

import csv
import os


def load_tasks_from_csv(filepath: str) -> list:
    """
    Load raw task data from a CSV file.
    Returns a list of dictionaries.

    Expected CSV columns:
      task_id, name, priority, deadline, exec_time, profit
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    raw_tasks = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_tasks.append(dict(row))

    print(f"  📂 Loaded {len(raw_tasks)} tasks from '{filepath}'")
    return raw_tasks


def get_sample_tasks() -> list:
    """
    Return a hardcoded list of sample tasks for simulation/demo.
    Covers edge cases: high profit + tight deadline, low profit + easy deadline, etc.
    """
    return [
        # task_id, name,                  priority, deadline, exec_time, profit
        {"task_id": 1,  "name": "Database Backup",    "priority": 9,  "deadline": 4,  "exec_time": 1, "profit": 90},
        {"task_id": 2,  "name": "User Auth Service",  "priority": 8,  "deadline": 3,  "exec_time": 2, "profit": 80},
        {"task_id": 3,  "name": "API Rate Limiter",   "priority": 7,  "deadline": 5,  "exec_time": 1, "profit": 70},
        {"task_id": 4,  "name": "Email Notification", "priority": 5,  "deadline": 6,  "exec_time": 2, "profit": 50},
        {"task_id": 5,  "name": "Log Aggregation",    "priority": 4,  "deadline": 2,  "exec_time": 1, "profit": 40},
        {"task_id": 6,  "name": "Cache Warmup",       "priority": 6,  "deadline": 5,  "exec_time": 2, "profit": 60},
        {"task_id": 7,  "name": "Report Generation",  "priority": 3,  "deadline": 8,  "exec_time": 3, "profit": 30},
        {"task_id": 8,  "name": "Payment Processing", "priority": 10, "deadline": 2,  "exec_time": 1, "profit": 100},
        {"task_id": 9,  "name": "ML Model Inference", "priority": 7,  "deadline": 7,  "exec_time": 3, "profit": 75},
        {"task_id": 10, "name": "Disk Cleanup",       "priority": 2,  "deadline": 9,  "exec_time": 2, "profit": 20},
        {"task_id": 11, "name": "SSL Certificate",    "priority": 8,  "deadline": 3,  "exec_time": 2, "profit": 85},
        {"task_id": 12, "name": "Analytics Sync",     "priority": 5,  "deadline": 10, "exec_time": 4, "profit": 55},
    ]


def get_invalid_sample_tasks() -> list:
    """
    Return tasks with intentional errors to demonstrate validation.
    """
    return [
        # Missing deadline
        {"task_id": 13, "name": "Bad Task A",   "priority": 5,  "exec_time": 2, "profit": 40},
        # Invalid priority > 10
        {"task_id": 14, "name": "Bad Task B",   "priority": 15, "deadline": 5,  "exec_time": 1, "profit": 30},
        # exec_time > deadline
        {"task_id": 15, "name": "Bad Task C",   "priority": 7,  "deadline": 2,  "exec_time": 5, "profit": 60},
        # Negative profit
        {"task_id": 16, "name": "Bad Task D",   "priority": 3,  "deadline": 4,  "exec_time": 1, "profit": -10},
        # Empty name
        {"task_id": 17, "name": "",             "priority": 5,  "deadline": 6,  "exec_time": 2, "profit": 45},
    ]
