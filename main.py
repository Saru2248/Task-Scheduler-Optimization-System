"""
=============================================================
  Task Scheduler Optimization System
  File   : main.py
  Purpose: Command-Line Interface (CLI) entry point
  Author : DSA Course Project
  Run    : python main.py
=============================================================

USAGE:
  python main.py                  → Interactive menu
  python main.py --simulate       → Run full simulation (auto)
  python main.py --algorithm greedy  → Run specific algorithm
  python main.py --csv data/tasks.csv → Load from CSV file

DSA CONCEPTS DEMONSTRATED:
  ✅ Priority Queue (Max-Heap) — from scratch
  ✅ Greedy Algorithm
  ✅ Multiple Sorting Strategies
  ✅ Deadlines & Job Scheduling
  ✅ Performance Analysis & Comparison
=============================================================
"""

import sys
import os
import copy
import argparse
import webbrowser
import http.server
import socketserver
import threading
import time

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader    import get_sample_tasks, load_tasks_from_csv
from src.validator      import validate_all_tasks, print_validation_report
from src.sorter         import (sort_by_deadline, sort_by_profit,
                                 sort_by_priority, display_sorted_tasks)
from src.priority_queue import MaxHeapPriorityQueue
from src.scheduler      import (greedy_deadline_scheduler,
                                 priority_queue_scheduler,
                                 earliest_deadline_first,
                                 shortest_job_first,
                                 run_all_algorithms)
from src.report         import (print_timeline, print_schedule_summary,
                                 print_comparison_table,
                                 export_to_csv, export_text_report)
from src.simulation     import run_simulation



# ─────────────────────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────────────────────

def print_banner():
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║    ████████╗ █████╗ ███████╗██╗  ██╗                   ║
  ║       ██╔══╝██╔══██╗██╔════╝██║ ██╔╝                   ║
  ║       ██║   ███████║███████╗█████╔╝                     ║
  ║       ██║   ██╔══██║╚════██║██╔═██╗                     ║
  ║       ██║   ██║  ██║███████║██║  ██╗                    ║
  ║       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                   ║
  ║                                                          ║
  ║    TASK SCHEDULER OPTIMIZATION SYSTEM                    ║
  ║    DSA Course Project  |  Python Implementation          ║
  ║                                                          ║
  ║    Algorithms: Greedy | EDF | SJF | Priority Queue       ║
  ║    Data Structures: Max-Heap | Queue | Array              ║
  ╚══════════════════════════════════════════════════════════╝
    """)


# ─────────────────────────────────────────────────────────────
#  INTERACTIVE MENU & WEB REDIRECT
# ─────────────────────────────────────────────────────────────

def launch_web_dashboard():
    """Launch local HTTP server on background thread and open dashboard in browser."""
    PORT = 8080
    class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    def start_server():
        try:
            handler = SilentHTTPHandler
            with socketserver.TCPServer(("", PORT), handler) as httpd:
                httpd.serve_forever()
        except OSError:
            pass

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    url = f"http://localhost:{PORT}/"
    print(f"\n  [WEB] Launching Web Dashboard in browser: {url} ...")
    webbrowser.open(url)


def interactive_menu():
    """Show the main interactive CLI menu."""
    print_banner()

    while True:
        print("""
  ┌─────────────────────────────────────────┐
  │            MAIN MENU                    │
  ├─────────────────────────────────────────┤
  │  1. Run Full Simulation (All Phases)    │
  │  2. Quick Run — Greedy Scheduler        │
  │  3. Quick Run — Priority Queue          │
  │  4. Quick Run — Earliest Deadline First │
  │  5. Quick Run — Shortest Job First      │
  │  6. Compare All Algorithms              │
  │  7. Load Tasks from CSV File            │
  │  8. Add Custom Task Manually            │
  │  9. Show Priority Queue Demo            │
  │  10. Launch Web Dashboard (Web)         │
  │  0. Exit                                │
  └─────────────────────────────────────────┘
        """)

        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            run_simulation()

        elif choice in ["2", "3", "4", "5"]:
            tasks = _load_default_tasks()
            algo_map = {
                "2": ("Greedy Deadline", greedy_deadline_scheduler),
                "3": ("Priority Queue",  priority_queue_scheduler),
                "4": ("EDF",             earliest_deadline_first),
                "5": ("SJF",             shortest_job_first),
            }
            name, algo = algo_map[choice]
            print(f"\n  Running {name} Scheduler...\n")
            result = algo(copy.deepcopy(tasks))
            print_timeline(result)
            print_schedule_summary(result)
            save = input("  Save report? (y/n): ").strip().lower()
            if save == "y":
                export_to_csv(result)
                export_text_report(result)

        elif choice == "6":
            tasks = _load_default_tasks()
            results = run_all_algorithms(tasks)
            print_comparison_table(results)
            save = input("  Save comparison reports? (y/n): ").strip().lower()
            if save == "y":
                for _, res in results.items():
                    export_to_csv(res)
                best = max(results.values(), key=lambda r: r.total_profit)
                export_text_report(best, comparison=results)

        elif choice == "7":
            filepath = input("  Enter CSV file path (e.g., data/tasks.csv): ").strip()
            try:
                raw = load_tasks_from_csv(filepath)
                valid, invalid = validate_all_tasks(raw)
                print_validation_report(valid, invalid)
                if valid:
                    results = run_all_algorithms(valid)
                    print_comparison_table(results)
            except FileNotFoundError as e:
                print(f"\n  ❌ Error: {e}")

        elif choice == "8":
            task = _get_manual_task()
            if task:
                result = greedy_deadline_scheduler([task])
                print_schedule_summary(result)

        elif choice == "9":
            _demo_priority_queue()

        elif choice == "10":
            launch_web_dashboard()

        elif choice == "0":
            print("\n  👋 Goodbye! Happy coding!\n")
            sys.exit(0)


        else:
            print("  ⚠️  Invalid choice. Please enter 0-9.\n")


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def _load_default_tasks():
    """Load and validate the default sample tasks."""
    raw   = get_sample_tasks()
    valid, invalid = validate_all_tasks(raw)
    if invalid:
        print(f"  ⚠️  {len(invalid)} invalid tasks skipped.")
    return valid


def _get_manual_task():
    """Prompt the user to enter a single task manually."""
    from src.validator import validate_task
    print("\n  Enter task details (press Ctrl+C to cancel):\n")
    try:
        data = {
            "task_id"  : input("  Task ID   (integer): ").strip(),
            "name"     : input("  Task Name          : ").strip(),
            "priority" : input("  Priority  (1-10)   : ").strip(),
            "deadline" : input("  Deadline  (slots)  : ").strip(),
            "exec_time": input("  Exec Time (units)  : ").strip(),
            "profit"   : input("  Profit/Score       : ").strip(),
        }
        task = validate_task(data)
        print(f"\n  ✅ Task '{task.name}' created successfully!")
        return task
    except ValueError as e:
        print(f"\n  ❌ Validation error: {e}")
        return None
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        return None


def _demo_priority_queue():
    """Interactive Max-Heap Priority Queue demonstration."""
    print("\n  MAX-HEAP PRIORITY QUEUE DEMO")
    print("  ─────────────────────────────\n")

    tasks = _load_default_tasks()
    pq    = MaxHeapPriorityQueue()

    print("  Building heap from all tasks...")
    pq.build_from_list(copy.deepcopy(tasks))
    pq.display()

    print("  Extracting tasks one by one (highest profit first):\n")
    order = 1
    while not pq.is_empty():
        task = pq.extract_max()
        print(f"  #{order:<2} Extracted: {task.name:<20} profit={task.profit:>4} "
              f" deadline={task.deadline}  exec={task.exec_time}")
        order += 1

    print("\n  Heap is now empty. All tasks extracted in profit order.\n")


# ─────────────────────────────────────────────────────────────
#  ARGUMENT PARSER (Non-interactive flags)
# ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Task Scheduler Optimization System — DSA Project",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--simulate", action="store_true",
        help="Run the full interactive simulation"
    )
    parser.add_argument(
        "--web", action="store_true",
        help="Launch the interactive Web Dashboard in browser"
    )
    parser.add_argument(
        "--algorithm", type=str,
        choices=["greedy", "pq", "edf", "sjf", "all"],
        help="Run a specific scheduling algorithm:\n"
             "  greedy = Greedy Deadline Scheduler\n"
             "  pq     = Priority Queue Scheduler\n"
             "  edf    = Earliest Deadline First\n"
             "  sjf    = Shortest Job First\n"
             "  all    = Compare all algorithms"
     )
    parser.add_argument(
        "--csv", type=str, metavar="FILE",
        help="Path to a CSV file containing tasks"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Automatically save reports to outputs/"
    )
    return parser.parse_args()


# ─────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Load tasks
    if args.csv:
        try:
            raw = load_tasks_from_csv(args.csv)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        raw = get_sample_tasks()

    valid_tasks, invalid_tasks = validate_all_tasks(raw)
    print_validation_report(valid_tasks, invalid_tasks)

    if not valid_tasks:
        print("No valid tasks to schedule. Exiting.")
        sys.exit(1)

    # Handle Web Dashboard flag
    if args.web:
        launch_web_dashboard()
        print("  Press Ctrl+C to terminate dashboard server.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Web Dashboard server stopped.")
        return

    # No flags → interactive menu
    if not any([args.simulate, args.algorithm, args.web]):
        interactive_menu()
        return

    # Full simulation
    if args.simulate:
        run_simulation()
        return

    # Specific algorithm
    algo_map = {
        "greedy": greedy_deadline_scheduler,
        "pq"    : priority_queue_scheduler,
        "edf"   : earliest_deadline_first,
        "sjf"   : shortest_job_first,
    }

    if args.algorithm == "all":
        results = run_all_algorithms(valid_tasks)
        for name, res in results.items():
            print_timeline(res)
            print_schedule_summary(res)
            if args.save:
                export_to_csv(res)
        print_comparison_table(results)
        if args.save:
            best = max(results.values(), key=lambda r: r.total_profit)
            export_text_report(best, comparison=results)

    elif args.algorithm in algo_map:
        result = algo_map[args.algorithm](copy.deepcopy(valid_tasks))
        print_banner()
        print_timeline(result)
        print_schedule_summary(result)
        if args.save:
            export_to_csv(result)
            export_text_report(result)


if __name__ == "__main__":
    main()

