"""
=============================================================
  Task Scheduler Optimization System
  Module: validator.py
  Purpose: Validate tasks before scheduling
=============================================================
"""

from src.task import Task


def validate_task(data: dict) -> Task:
    """
    Validate a raw dictionary of task data and return a Task object.
    Raises ValueError with a descriptive message on any failure.

    Expected keys: task_id, name, priority, deadline, exec_time, profit
    """
    required = ["task_id", "name", "priority", "deadline", "exec_time", "profit"]

    # 1. Check all required fields are present
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: '{field}'")

    # 2. Parse and type-check numeric fields
    try:
        task_id   = int(data["task_id"])
        priority  = int(data["priority"])
        deadline  = int(data["deadline"])
        exec_time = int(data["exec_time"])
        profit    = int(data["profit"])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Numeric field has invalid value: {e}")

    name = str(data["name"]).strip()

    # 3. Business rule validations
    errors = []

    if task_id <= 0:
        errors.append("task_id must be a positive integer (>0).")
    if not name:
        errors.append("Task name cannot be empty.")
    if len(name) > 50:
        errors.append("Task name cannot exceed 50 characters.")
    if not (1 <= priority <= 10):
        errors.append(f"Priority must be between 1 and 10 (got {priority}).")
    if deadline <= 0:
        errors.append(f"Deadline must be > 0 (got {deadline}).")
    if exec_time <= 0:
        errors.append(f"Execution time must be > 0 (got {exec_time}).")
    if exec_time > deadline:
        errors.append(
            f"Execution time ({exec_time}) cannot exceed deadline ({deadline}) — "
            f"task can never finish on time."
        )
    if profit < 0:
        errors.append(f"Profit cannot be negative (got {profit}).")

    if errors:
        raise ValueError(
            f"Validation failed for task '{name}':\n  " + "\n  ".join(errors)
        )

    return Task(task_id, name, priority, deadline, exec_time, profit)


def validate_all_tasks(raw_tasks: list) -> tuple:
    """
    Validate a list of task dictionaries.

    Returns:
        valid_tasks   (list[Task])  : Successfully validated tasks
        invalid_tasks (list[dict])  : Tasks that failed validation, with error info
    """
    valid_tasks   = []
    invalid_tasks = []
    seen_ids      = set()

    for raw in raw_tasks:
        try:
            task = validate_task(raw)

            # Check for duplicate IDs
            if task.task_id in seen_ids:
                raise ValueError(f"Duplicate task_id: {task.task_id}")
            seen_ids.add(task.task_id)

            valid_tasks.append(task)

        except ValueError as e:
            invalid_tasks.append({
                "raw_data": raw,
                "error"   : str(e)
            })

    return valid_tasks, invalid_tasks


def print_validation_report(valid: list, invalid: list) -> None:
    """Print a summary of validation results."""
    total = len(valid) + len(invalid)
    print(f"\n  +{'-'*50}+")
    print(f"  |  VALIDATION REPORT{' '*31}|")
    print(f"  +{'-'*50}+")
    print(f"  |  Total tasks submitted : {total:<24}|")
    print(f"  |  [OK] Valid tasks      : {len(valid):<24}|")
    print(f"  |  [ERR] Invalid tasks   : {len(invalid):<24}|")
    print(f"  +{'-'*50}+")

    if invalid:
        print("\n  -- Invalid Task Details --------------------------")
        for entry in invalid:
            raw = entry.get("raw_data", {})
            print(f"  Task: {raw.get('name', 'UNKNOWN')}")
            print(f"  Error: {entry['error']}")
            print(f"  {'-'*48}")

