"""
CLI command handlers for the Core CLI Todo Application.

This module implements handlers for all CLI commands (add, list, update, delete, complete, incomplete).
"""

import sys
from typing import Any
from src.services.task_service import TaskService
from src.utils import messages


def handle_add(args: Any, task_service: TaskService) -> int:
    """
    Handle the 'add' command to create a new task.

    Args:
        args: Parsed command-line arguments (title, description)
        task_service: TaskService instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = task_service.add_task(args.title, args.description or "")
        print(messages.TASK_ADDED.format(id=task.id, title=task.title))
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_list(args: Any, task_service: TaskService) -> int:
    """
    Handle the 'list' command to display all tasks.

    Args:
        args: Parsed command-line arguments
        task_service: TaskService instance

    Returns:
        Exit code (0 for success)
    """
    tasks = task_service.get_all_tasks()

    if not tasks:
        print(messages.NO_TASKS_FOUND)
        return 0

    # Print header
    print(f"{'ID':<5} {'Title':<30} {'Status':<15}")
    print("-" * 50)

    # Print tasks
    for task in tasks:
        status = messages.STATUS_COMPLETED if task.completed else messages.STATUS_PENDING
        title = task.title[:30]  # Truncate long titles for display
        print(f"{task.id:<5} {title:<30} {status:<15}")

    return 0


def handle_complete(args: Any, task_service: TaskService) -> int:
    """
    Handle the 'complete' command to mark a task as completed.

    Args:
        args: Parsed command-line arguments (id)
        task_service: TaskService instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = task_service.complete_task(args.id)
        print(f"Task #{task.id} marked as completed: {task.title}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_incomplete(args: Any, task_service: TaskService) -> int:
    """
    Handle the 'incomplete' command to mark a task as incomplete.

    Args:
        args: Parsed command-line arguments (id)
        task_service: TaskService instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = task_service.incomplete_task(args.id)
        print(f"Task #{task.id} marked as pending: {task.title}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
