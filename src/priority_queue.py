"""
=============================================================
  Task Scheduler Optimization System
  Module: priority_queue.py
  Purpose: Custom Max-Heap Priority Queue (from scratch)
  DSA Concept: Binary Heap / Priority Queue
=============================================================

HOW A MAX-HEAP WORKS:
─────────────────────
A heap is a complete binary tree stored as an array.
In a MAX-HEAP: parent.value >= children.value

Array index relationships (0-based):
  Parent of i  → (i - 1) // 2
  Left child   → 2 * i + 1
  Right child  → 2 * i + 2

Operations:
  insert()    → O(log n)   Add task and bubble up
  extract_max()→ O(log n)  Remove top task and bubble down
  peek()      → O(1)       View top task without removal
"""


class MaxHeapPriorityQueue:
    """
    A Max-Heap Priority Queue where the task with the
    HIGHEST PROFIT is always at the top.

    Used by the scheduler to always pick the most
    valuable task available at each scheduling step.
    """

    def __init__(self):
        self._heap = []   # Internal array storage

    # ─────────────────────────────────────────────
    # PUBLIC INTERFACE
    # ─────────────────────────────────────────────

    def insert(self, task) -> None:
        """
        Insert a task into the heap.
        Steps:
          1. Append task to end of array
          2. Bubble UP to restore heap property
        Time: O(log n)
        """
        self._heap.append(task)
        self._bubble_up(len(self._heap) - 1)

    def extract_max(self):
        """
        Remove and return the task with the highest profit.
        Steps:
          1. Swap root with last element
          2. Remove last element (was root)
          3. Bubble DOWN to restore heap property
        Time: O(log n)
        """
        if self.is_empty():
            return None

        # Swap root with last element
        self._swap(0, len(self._heap) - 1)
        max_task = self._heap.pop()      # Remove old root
        self._bubble_down(0)             # Restore heap property
        return max_task

    def peek(self):
        """Return the max-profit task WITHOUT removing it. O(1)"""
        return self._heap[0] if self._heap else None

    def is_empty(self) -> bool:
        """Return True if the heap has no tasks."""
        return len(self._heap) == 0

    def size(self) -> int:
        """Return current number of tasks in heap."""
        return len(self._heap)

    def build_from_list(self, tasks: list) -> None:
        """
        Build heap from a list of tasks efficiently.
        Uses Floyd's algorithm: O(n) instead of n × O(log n).
        Start from last non-leaf and bubble down each node.
        """
        self._heap = list(tasks)
        # Last non-leaf index
        start = (len(self._heap) - 2) // 2
        for i in range(start, -1, -1):
            self._bubble_down(i)

    def to_sorted_list(self) -> list:
        """
        Extract all tasks in descending profit order.
        Destructive — empties the heap.
        """
        result = []
        while not self.is_empty():
            result.append(self.extract_max())
        return result

    # ─────────────────────────────────────────────
    # PRIVATE HELPERS
    # ─────────────────────────────────────────────

    def _bubble_up(self, index: int) -> None:
        """
        Move element at `index` UP until heap property holds.
        Compare child with parent; swap if child.profit > parent.profit
        """
        while index > 0:
            parent = (index - 1) // 2
            # If current task has MORE profit than parent → swap
            if self._heap[index].profit > self._heap[parent].profit:
                self._swap(index, parent)
                index = parent
            else:
                break   # Heap property satisfied

    def _bubble_down(self, index: int) -> None:
        """
        Move element at `index` DOWN until heap property holds.
        Find the largest among node and its children; swap if needed.
        """
        n = len(self._heap)
        while True:
            largest = index
            left  = 2 * index + 1
            right = 2 * index + 2

            # Check left child
            if left < n and self._heap[left].profit > self._heap[largest].profit:
                largest = left
            # Check right child
            if right < n and self._heap[right].profit > self._heap[largest].profit:
                largest = right

            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break   # Heap property satisfied

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap array."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    # ─────────────────────────────────────────────
    # DISPLAY
    # ─────────────────────────────────────────────

    def display(self) -> None:
        """Print current heap state with tree visualization."""
        if self.is_empty():
            print("  [Heap is empty]")
            return

        print(f"\n  {'='*50}")
        print(f"  MAX-HEAP STATE  (size = {self.size()})")
        print(f"  {'='*50}")

        level = 0
        i     = 0
        while i < len(self._heap):
            nodes_at_level = 2 ** level
            row = []
            for _ in range(nodes_at_level):
                if i >= len(self._heap):
                    break
                t = self._heap[i]
                row.append(f"[{t.name}|P{t.profit}]")
                i += 1
            indent = " " * (3 * (4 - level))
            print(f"  {indent}{' | '.join(row)}")
            level += 1

        print(f"  {'='*50}")
        print(f"  Top task: {self.peek().name} (profit={self.peek().profit})\n")
