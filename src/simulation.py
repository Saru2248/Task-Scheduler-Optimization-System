"""
=============================================================
  Task Scheduler Optimization System
  Module: simulation.py
  Purpose: Virtual simulation & comparison of all algorithms
=============================================================
"""

import copy
import time as time_module
from src.data_loader   import get_sample_tasks, get_invalid_sample_tasks
from src.validator     import validate_all_tasks, print_validation_report
from src.sorter        import (sort_by_deadline, sort_by_profit,
                                sort_by_priority, sort_by_efficiency,
                                display_sorted_tasks)
from src.priority_queue import MaxHeapPriorityQueue
from src.scheduler     import run_all_algorithms
from src.report        import (print_timeline, print_schedule_summary,
                                print_comparison_table,
                                export_to_csv, export_text_report)


def run_simulation():
    """
    Full end-to-end simulation of the Task Scheduler.
    Demonstrates the complete DSA pipeline:
      Input → Validate → Sort → Heap → Schedule → Report
    """

    # ─── HEADER ───────────────────────────────────────────────
    print("\n")
    print("  " + "▓" * 64)
    print("  ▓▓   TASK SCHEDULER OPTIMIZATION SYSTEM — SIMULATION   ▓▓")
    print("  " + "▓" * 64)
    print(f"\n  DSA Concepts: Priority Queue | Greedy | Heap | Sorting")
    print(f"  Algorithms  : Greedy Deadline | EDF | SJF | PQ Heap\n")

    input("  ► Press ENTER to start simulation...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 1: LOAD TASK DATA
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 1: LOADING TASK DATA")
    print("  " + "─" * 60)

    # Combine valid + invalid tasks to demo validation
    raw_valid   = get_sample_tasks()
    raw_invalid = get_invalid_sample_tasks()
    all_raw     = raw_valid + raw_invalid

    print(f"\n  Total raw tasks loaded: {len(all_raw)}")
    print(f"  (Includes {len(raw_invalid)} intentionally invalid tasks for demo)\n")
    input("  ► Press ENTER for Phase 2: Validation...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 2: VALIDATION
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 2: TASK VALIDATION")
    print("  " + "─" * 60)

    valid_tasks, invalid_tasks = validate_all_tasks(all_raw)
    print_validation_report(valid_tasks, invalid_tasks)

    input("  ► Press ENTER for Phase 3: Sorting...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 3: SORTING COMPARISON
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 3: SORTING STRATEGIES")
    print("  " + "─" * 60)

    print("\n  [A] UNSORTED (Original Input):")
    display_sorted_tasks(valid_tasks, "None (Original Order)")

    print("\n  [B] SORTED BY DEADLINE (Earliest Deadline First):")
    display_sorted_tasks(sort_by_deadline(valid_tasks), "Earliest Deadline First")

    print("\n  [C] SORTED BY PROFIT (Greedy / Maximum Profit First):")
    display_sorted_tasks(sort_by_profit(valid_tasks), "Maximum Profit First")

    print("\n  [D] SORTED BY PRIORITY (Highest Priority First):")
    display_sorted_tasks(sort_by_priority(valid_tasks), "Highest Priority First")

    print("\n  [E] SORTED BY EFFICIENCY (Profit ÷ Exec Time):")
    display_sorted_tasks(sort_by_efficiency(valid_tasks), "Efficiency Ratio")

    input("  ► Press ENTER for Phase 4: Priority Queue (Max-Heap)...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 4: PRIORITY QUEUE DEMONSTRATION
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 4: MAX-HEAP PRIORITY QUEUE DEMO")
    print("  " + "─" * 60)

    pq = MaxHeapPriorityQueue()
    pq.build_from_list(copy.deepcopy(valid_tasks))

    print("\n  ► All tasks inserted into Max-Heap:")
    pq.display()

    print("\n  ► Extracting top 3 tasks from heap (highest profit):")
    for i in range(min(3, pq.size())):
        task = pq.extract_max()
        print(f"    Extract #{i+1}: {task.name} (profit={task.profit}, deadline={task.deadline})")

    print(f"\n  ► Remaining tasks in heap: {pq.size()}")

    input("\n  ► Press ENTER for Phase 5: Scheduling Algorithms...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 5: RUN ALL SCHEDULING ALGORITHMS
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 5: SCHEDULING ALGORITHMS")
    print("  " + "─" * 60)

    print("\n  Running all 4 algorithms on the same task set...")
    results = run_all_algorithms(valid_tasks)

    # Show timeline for best algorithm (Greedy)
    best_result = results["Greedy"]
    print_timeline(best_result)

    input("  ► Press ENTER for Phase 6: Detailed Schedule View...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 6: SCHEDULE SUMMARIES
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 6: SCHEDULE DETAILS FOR EACH ALGORITHM")
    print("  " + "─" * 60)

    for name, res in results.items():
        print_schedule_summary(res)
        input(f"  ► Press ENTER for next algorithm...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 7: COMPARISON TABLE
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 7: ALGORITHM COMPARISON")
    print("  " + "─" * 60)

    print_comparison_table(results)
    input("  ► Press ENTER for Phase 8: Export Reports...\n")

    # ══════════════════════════════════════════════════════════
    # PHASE 8: EXPORT REPORTS
    # ══════════════════════════════════════════════════════════
    print("  " + "─" * 60)
    print("  PHASE 8: EXPORTING REPORTS")
    print("  " + "─" * 60)
    print()

    # Export CSV for all algorithms
    for name, res in results.items():
        export_to_csv(res)

    # Export detailed text report for Greedy (best algorithm)
    export_text_report(best_result, comparison=results)

    # ── FINAL SUMMARY ─────────────────────────────────────────
    print(f"\n  {'▓'*64}")
    print(f"  ▓▓  SIMULATION COMPLETE!{' '*39}▓▓")
    print(f"  {'▓'*64}")
    print(f"\n  📁 Output files saved to: outputs/")
    print(f"  ✅ All reports generated successfully.\n")
