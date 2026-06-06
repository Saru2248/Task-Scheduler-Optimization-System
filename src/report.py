"""
=============================================================
  Task Scheduler Optimization System
  Module: report.py
  Purpose: Generate text reports, CSV exports, timeline views
=============================================================
"""

import csv
import os
from datetime import datetime
from src.scheduler import ScheduleResult


# -------------------------------------------------------------
#  TIMELINE DISPLAY
# -------------------------------------------------------------

def print_timeline(result: ScheduleResult) -> None:
    """
    Print a visual Gantt-style timeline of the scheduled tasks.
    """
    print(f"\n  {'-'*64}")
    print(f"  TIMELINE - {result.algorithm_name}")
    print(f"  {'-'*64}")

    if not result.timeline:
        print("  No tasks were scheduled.")
    else:
        sorted_timeline = sorted(result.timeline, key=lambda x: x[0])
        for start, finish, task in sorted_timeline:
            bar_len  = max(1, task.exec_time * 3)
            bar      = "#" * bar_len
            print(f"  t={start:>3} ---> {bar} ---> t={finish:<3}  "
                  f"| {task.name:<18} | profit={task.profit:>3} | deadline={task.deadline}")

    print(f"  {'-'*64}\n")


# -------------------------------------------------------------
#  SCHEDULE SUMMARY
# -------------------------------------------------------------

def print_schedule_summary(result: ScheduleResult) -> None:
    """Print a full summary table of scheduled and missed tasks."""

    print(f"\n  +{'-'*66}+")
    print(f"  |  SCHEDULE RESULT - {result.algorithm_name:<45}|")
    print(f"  +{'-'*66}+")

    # Scheduled tasks
    print(f"  |  [OK] SCHEDULED TASKS ({len(result.scheduled_tasks)} tasks){' '*37}|")
    print(f"  +{'-'*7}+{'-'*18}+{'-'*6}+{'-'*8}+{'-'*6}+{'-'*7}+{'-'*9}+")
    print(f"  | {'ID':<5} | {'Name':<16} | {'Start':^4} | {'Finish':^6} | {'Time':^4} | {'Profit':^5} | {'Deadline':^7} |")
    print(f"  +{'-'*7}+{'-'*18}+{'-'*6}+{'-'*8}+{'-'*6}+{'-'*7}+{'-'*9}+")

    for t in sorted(result.scheduled_tasks, key=lambda x: x.start_time):
        print(f"  | {t.task_id:<5} | {t.name:<16} | {t.start_time:^4} | {t.finish_time:^6} | "
              f"{t.exec_time:^4} | {t.profit:^5} | {t.deadline:^7} |")

    # Missed tasks
    if result.missed_tasks:
        print(f"  +{'-'*66}+")
        print(f"  |  [MISS] MISSED TASKS ({len(result.missed_tasks)} tasks){' '*39}|")
        print(f"  +{'-'*7}+{'-'*18}+{'-'*8}+{'-'*6}+{'-'*27}+")
        print(f"  | {'ID':<5} | {'Name':<16} | {'Deadline':^6} | {'ExecT':^4} | {'Reason':<27} |")
        print(f"  +{'-'*7}+{'-'*18}+{'-'*8}+{'-'*6}+{'-'*27}+")
        for t in result.missed_tasks:
            reason = "No available slot"
            print(f"  | {t.task_id:<5} | {t.name:<16} | {t.deadline:^6} | "
                  f"{t.exec_time:^4} | {reason:<27} |")

    # Totals
    print(f"  +{'-'*66}+")
    print(f"  |  PERFORMANCE METRICS{' '*45}|")
    print(f"  +{'-'*66}+")
    print(f"  |  Total Tasks Submitted  : {result.total_tasks:<39}|")
    print(f"  |  Tasks Scheduled        : {len(result.scheduled_tasks):<39}|")
    print(f"  |  Tasks Missed           : {len(result.missed_tasks):<39}|")
    print(f"  |  Completion Rate        : {result.completion_rate:.1f}%{' '*36}|")
    print(f"  |  Total Profit Earned    : {result.total_profit:<39}|")
    print(f"  |  Total Execution Time   : {result.total_exec_time} units{' '*32}|")
    print(f"  +{'-'*66}+\n")


# -------------------------------------------------------------
#  COMPARISON TABLE
# -------------------------------------------------------------

def print_comparison_table(results: dict) -> None:
    """
    Compare all scheduling algorithms side by side.
    """
    print(f"\n  {'-'*75}")
    print(f"  ALGORITHM COMPARISON TABLE")
    print(f"  {'-'*75}")
    print(f"  {'Algorithm':<30} | {'Scheduled':^9} | {'Missed':^6} | "
          f"{'Profit':^8} | {'Rate%':^7} | {'ExecTime':^8}")
    print(f"  {'-'*30}-+-{'-'*9}-+-{'-'*6}-+-{'-'*8}-+-{'-'*7}-+-{'-'*8}")

    best_profit = max(r.total_profit    for r in results.values())
    best_rate   = max(r.completion_rate for r in results.values())

    for name, res in results.items():
        profit_mark = " *" if res.total_profit    == best_profit else "  "
        rate_mark   = " *" if res.completion_rate == best_rate   else "  "
        print(f"  {name:<30} | {len(res.scheduled_tasks):^9} | {len(res.missed_tasks):^6} | "
              f"{res.total_profit:^8}{profit_mark}| {res.completion_rate:^6.1f}%"
              f"{rate_mark}| {res.total_exec_time:^8}")

    print(f"  {'-'*75}")
    print(f"  * = Best in category\n")


# -------------------------------------------------------------
#  CSV EXPORT
# -------------------------------------------------------------

def export_to_csv(result: ScheduleResult, output_dir: str = "outputs") -> str:
    """
    Export the schedule result to a CSV file.
    Returns the file path of the created CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    algo_name = result.algorithm_name.replace(" ", "_").replace("(", "").replace(")", "")
    filename  = f"{algo_name}_{timestamp}.csv"
    filepath  = os.path.join(output_dir, filename)

    all_tasks = result.scheduled_tasks + result.missed_tasks

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "task_id", "name", "priority", "deadline",
            "exec_time", "profit", "scheduled", "start_time", "finish_time"
        ])
        writer.writeheader()
        for task in all_tasks:
            writer.writerow(task.to_dict())

    print(f"  CSV exported -> {filepath}")
    return filepath


# -------------------------------------------------------------
#  TEXT REPORT EXPORT
# -------------------------------------------------------------

def export_text_report(result: ScheduleResult,
                       comparison: dict = None,
                       output_dir: str = "outputs") -> str:
    """
    Export a full human-readable report as a .txt file.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"Schedule_Report_{timestamp}.txt"
    filepath  = os.path.join(output_dir, filename)

    lines = []
    sep   = "=" * 68

    lines.append(sep)
    lines.append("  TASK SCHEDULER OPTIMIZATION SYSTEM - PERFORMANCE REPORT")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(sep)

    lines.append(f"\n  Algorithm Used: {result.algorithm_name}")
    lines.append(f"  Total Tasks   : {result.total_tasks}")
    lines.append(f"  Scheduled     : {len(result.scheduled_tasks)}")
    lines.append(f"  Missed        : {len(result.missed_tasks)}")
    lines.append(f"  Total Profit  : {result.total_profit}")
    lines.append(f"  Completion    : {result.completion_rate:.1f}%")

    lines.append(f"\n{'-'*68}")
    lines.append("  SCHEDULED TASKS (Execution Order):")
    lines.append(f"{'-'*68}")

    for t in sorted(result.scheduled_tasks, key=lambda x: x.start_time):
        lines.append(
            f"  [{t.start_time:>3} -> {t.finish_time:<3}]  "
            f"{t.name:<20} | Priority={t.priority} | "
            f"Deadline={t.deadline} | Profit={t.profit}"
        )

    if result.missed_tasks:
        lines.append(f"\n{'-'*68}")
        lines.append("  MISSED TASKS:")
        lines.append(f"{'-'*68}")
        for t in result.missed_tasks:
            lines.append(
                f"  [MISS] {t.name:<20} | Priority={t.priority} | "
                f"Deadline={t.deadline} | Profit={t.profit}"
            )

    if comparison:
        lines.append(f"\n{'-'*68}")
        lines.append("  ALGORITHM COMPARISON:")
        lines.append(f"{'-'*68}")
        lines.append(f"  {'Algorithm':<30} {'Scheduled':>9} {'Missed':>7} {'Profit':>8} {'Rate':>7}")
        for name, res in comparison.items():
            lines.append(
                f"  {name:<30} {len(res.scheduled_tasks):>9} "
                f"{len(res.missed_tasks):>7} {res.total_profit:>8} "
                f"{res.completion_rate:>6.1f}%"
            )

    lines.append(f"\n{sep}")
    lines.append("  END OF REPORT")
    lines.append(sep)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Text report saved -> {filepath}")
    return filepath
