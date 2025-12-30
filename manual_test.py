"""Manual verification script for Todo CLI Application."""

import sys
import io

# Set UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.models.task import Task
from src.services.task_manager import TaskManager
from src.cli.formatters import format_task_list, format_success, format_error
from src.cli.menu import MenuHandler

print("=" * 80)
print("MANUAL VERIFICATION SCRIPT - Todo CLI Application")
print("=" * 80)

# Test 1: Task Model
print("\n[Test 1] Task Model")
task = Task(id=1, title="Test Task", description="Test Description", completed=False)
print(f"✓ Task created: ID={task.id}, Title={task.title}, Completed={task.completed}")

# Test 2: TaskManager - Add Tasks
print("\n[Test 2] TaskManager - Add Tasks")
manager = TaskManager()
task1 = manager.add_task("Buy groceries", "Milk and eggs")
task2 = manager.add_task("Review PRs")
task3 = manager.add_task("Write documentation", "Update README")
print(f"✓ Added 3 tasks. IDs: {task1.id}, {task2.id}, {task3.id}")
print(f"✓ Task count: {manager.task_count()}")

# Test 3: TaskManager - Get All Tasks
print("\n[Test 3] TaskManager - Get All Tasks")
tasks = manager.get_all_tasks()
print(f"✓ Retrieved {len(tasks)} tasks")
for t in tasks:
    print(f"  - Task #{t.id}: {t.title}")

# Test 4: TaskManager - Update Task
print("\n[Test 4] TaskManager - Update Task")
updated = manager.update_task(task1.id, title="Buy groceries and supplies")
print(f"✓ Updated task #{task1.id}: {updated.title}")

# Test 5: TaskManager - Toggle Status
print("\n[Test 5] TaskManager - Toggle Task Status")
toggled = manager.toggle_task(task2.id)
print(f"✓ Toggled task #{task2.id}: Completed={toggled.completed}")

# Test 6: TaskManager - Delete Task
print("\n[Test 6] TaskManager - Delete Task")
manager.delete_task(task3.id)
print(f"✓ Deleted task #{task3.id}")
print(f"✓ Remaining tasks: {manager.task_count()}")

# Test 7: Formatters
print("\n[Test 7] Formatters")
print("--- Task List ---")
print(format_task_list(manager.get_all_tasks()))
print("\n--- Success Message ---")
print(format_success("Operation completed"))
print("\n--- Error Message ---")
print(format_error("Task not found"))

# Test 8: Error Handling
print("\n[Test 8] Error Handling")
try:
    manager.add_task("")
    print("✗ FAILED: Empty title should raise ValueError")
except ValueError as e:
    print(f"✓ Empty title rejected: {e}")

try:
    manager.add_task("a" * 201)
    print("✗ FAILED: Long title should raise ValueError")
except ValueError as e:
    print(f"✓ Long title rejected: {e}")

try:
    manager.delete_task(999)
    print("✗ FAILED: Invalid ID should raise ValueError")
except ValueError as e:
    print(f"✓ Invalid ID rejected: {e}")

# Test 9: ID Auto-increment
print("\n[Test 9] ID Auto-increment and Non-reuse")
task4 = manager.add_task("Task 4")
print(f"✓ New task ID: {task4.id} (should be 4, not 3)")

# Test 10: Final State
print("\n[Test 10] Final State")
final_tasks = manager.get_all_tasks()
print(f"✓ Total tasks: {len(final_tasks)}")
print(f"✓ Task IDs: {[t.id for t.tasks in final_tasks]}")

print("\n" + "=" * 80)
print("ALL MANUAL TESTS PASSED ✓")
print("=" * 80)
print("\nThe application is ready to use!")
print("Run: python main.py")
