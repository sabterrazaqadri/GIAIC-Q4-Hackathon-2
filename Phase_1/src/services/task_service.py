"""
TaskService for managing todo tasks.

This module provides the business logic layer for CRUD operations on tasks.
Uses file-based JSON storage with sequential numeric IDs for CLI usability.
"""

import json
import os
from pathlib import Path
from typing import List, Optional
from src.models.task import Task


class TaskService:
    """
    Manages task storage and operations (add, retrieve, update, delete, toggle complete).

    Uses JSON file for persistence with sequential numeric IDs.
    Thread-safe for single-threaded CLI usage (Phase I).
    """

    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialize TaskService with file-based storage.

        Args:
            storage_file: Path to JSON file for task storage (default: tasks.json)
        """
        self.storage_file = Path(storage_file)
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self._load_tasks()

    def _load_tasks(self):
        """Load tasks from JSON file if it exists."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task(**task_dict) for task_dict in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, OSError):
                # If file is corrupted or unreadable, start fresh
                self.tasks = []
                self.next_id = 1

    def _save_tasks(self):
        """Save tasks to JSON file."""
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise RuntimeError(f"Failed to save tasks: {e}")

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new task.

        Args:
            title: Required task title (non-empty)
            description: Optional task description (default: "")

        Returns:
            The newly created Task instance

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        if not title or title.strip() == "":
            raise ValueError("Title is required")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save_tasks()  # Persist to file
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in insertion order.

        Returns:
            List of all Task instances (may be empty)
        """
        return self.tasks.copy()  # Return copy to prevent external mutation

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The task ID to search for

        Returns:
            Task instance if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: The task ID to mark as completed

        Returns:
            The updated Task instance

        Raises:
            ValueError: If task with given ID is not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        task.completed = True
        self._save_tasks()
        return task

    def incomplete_task(self, task_id: int) -> Task:
        """
        Mark a task as incomplete (pending).

        Args:
            task_id: The task ID to mark as incomplete

        Returns:
            The updated Task instance

        Raises:
            ValueError: If task with given ID is not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        task.completed = False
        self._save_tasks()
        return task
