"""
Quick MVP test script to demonstrate add and list functionality.

This script tests the core functionality within a single Python process,
demonstrating that the in-memory storage works correctly.
"""

from src.services.task_service import TaskService
from src.models.task import Task

def test_mvp():
    """Test MVP functionality: add and view tasks."""
    print("=== Testing MVP: Add and View Tasks ===\n")

    # Create service
    service = TaskService()
    print("[OK] TaskService initialized\n")

    # Test 1: Add task with title only
    print("Test 1: Add task with title only")
    task1 = service.add_task("Buy groceries")
    print(f"  Result: {task1}")
    assert task1.id == 1
    assert task1.title == "Buy groceries"
    assert task1.completed == False
    print("  [PASS]\n")

    # Test 2: Add task with title and description
    print("Test 2: Add task with title and description")
    task2 = service.add_task("Write report", "Quarterly summary")
    print(f"  Result: {task2}")
    assert task2.id == 2
    assert task2.description == "Quarterly summary"
    print("  [PASS]\n")

    # Test 3: Add third task
    print("Test 3: Add third task")
    task3 = service.add_task("Call dentist")
    print(f"  Result: {task3}")
    assert task3.id == 3
    print("  [PASS]\n")

    # Test 4: View all tasks
    print("Test 4: View all tasks")
    all_tasks = service.get_all_tasks()
    print(f"  Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"    {task}")
    assert len(all_tasks) == 3
    print("  [PASS]\n")

    # Test 5: Try to add task with empty title
    print("Test 5: Try to add task with empty title")
    try:
        service.add_task("")
        print("  [FAIL]: Should have raised ValueError")
    except ValueError as e:
        print(f"  Result: ValueError caught - {e}")
        print("  [PASS]\n")

    print("=== All MVP Tests Passed! ===")
    print("\nNote: In Phase I, data is in-memory only.")
    print("Each CLI command runs in a separate Python process,")
    print("so tasks do not persist between commands.")
    print("This is expected behavior per the specification.")

if __name__ == "__main__":
    test_mvp()
