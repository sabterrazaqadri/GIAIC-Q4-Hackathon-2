"""Skill functions for todo operations in the conversational todo management system."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from utils.logging_config import logger, log_error
from models.todo import TodoTask, TaskStatus
from validators.task_validator import validate_new_task_data, validate_task_update_data
import asyncio


def run_async(coro):
    """Helper to run async functions from sync context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        # We're in an async context, run in a new thread
        import concurrent.futures
        def run_in_thread():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(coro)
            finally:
                new_loop.close()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return executor.submit(run_in_thread).result(timeout=30)
    else:
        # No running loop, safe to create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


class AddTaskSkill:
    """Skill for adding new tasks."""

    @staticmethod
    def execute(title: str, description: str = None, dueDate: str = None, priority: str = "medium") -> Dict[str, Any]:
        """
        Execute the add task skill.

        Args:
            title: The title of the task
            description: Optional description of the task
            dueDate: Optional due date in ISO format
            priority: Task priority (low, medium, high) - defaults to medium

        Returns:
            Dictionary containing the created task
        """
        try:
            logger.info(f"Executing add_task skill with title: {title}")

            # Validate the task data before processing
            validate_new_task_data(title, description, "pending", dueDate)

            # Use local Neon database
            from db.todo_operations import add_task_db

            result = run_async(add_task_db(
                title=title,
                description=description,
                status="pending",
                priority=priority,
                due_date=dueDate
            ))

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": result.get("status", "pending"),
                "priority": result.get("priority", priority),
                "dueDate": dueDate,
                "createdAt": str(result.get("created_at", "")),
                "updatedAt": str(result.get("updated_at", "")),
            }

            logger.info(f"Successfully added task with ID: {transformed_result['id']}")
            return transformed_result

        except Exception as e:
            log_error(e, "AddTaskSkill.execute")
            raise e


class UpdateTaskSkill:
    """Skill for updating existing tasks."""

    @staticmethod
    def execute(id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the update task skill.

        Args:
            id: The ID of the task to update
            updates: Dictionary containing the fields to update

        Returns:
            Dictionary containing the updated task
        """
        try:
            logger.info(f"Executing update_task skill for task ID: {id}")

            # Validate the update data before processing
            validate_task_update_data(updates)

            # Use local Neon database
            from db.todo_operations import update_task_db

            # Map our data model to database schema
            db_updates = {}
            if "title" in updates:
                db_updates["title"] = updates["title"]
            if "description" in updates:
                db_updates["description"] = updates["description"]
            if "status" in updates:
                db_updates["status"] = updates["status"]
            if "priority" in updates:
                db_updates["priority"] = updates["priority"]
            if "dueDate" in updates:
                db_updates["due_date"] = updates["dueDate"]

            result = run_async(update_task_db(int(id), db_updates))

            if not result:
                raise Exception(f"Task with ID {id} not found")

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": result.get("status", "pending"),
                "priority": result.get("priority", "medium"),
                "dueDate": str(result.get("due_date", "")) if result.get("due_date") else None,
                "createdAt": str(result.get("created_at", "")),
                "updatedAt": str(result.get("updated_at", "")),
            }

            logger.info(f"Successfully updated task with ID: {transformed_result['id']}")
            return transformed_result

        except Exception as e:
            log_error(e, "UpdateTaskSkill.execute")
            raise e


class DeleteTaskSkill:
    """Skill for deleting tasks."""

    @staticmethod
    def execute(id: str) -> bool:
        """
        Execute the delete task skill.

        Args:
            id: The ID of the task to delete

        Returns:
            Boolean indicating success
        """
        try:
            logger.info(f"Executing delete_task skill for task ID: {id}")

            # Use local Neon database
            from db.todo_operations import delete_task_db

            result = run_async(delete_task_db(int(id)))

            if result:
                logger.info(f"Successfully deleted task with ID: {id}")
            else:
                logger.warning(f"Task with ID {id} not found or already deleted")

            return result

        except Exception as e:
            log_error(e, "DeleteTaskSkill.execute")
            raise e


class ListTasksSkill:
    """Skill for listing tasks."""

    @staticmethod
    def execute(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute the list tasks skill.

        Args:
            filters: Optional dictionary containing filter criteria

        Returns:
            List of tasks
        """
        try:
            logger.info(f"Executing list_tasks skill with filters: {filters}")

            # Use local Neon database
            from db.todo_operations import list_tasks_db

            todos = run_async(list_tasks_db(filters))

            # Transform the response to match our data model
            transformed_todos = []
            for todo in todos:
                transformed_todo = {
                    "id": str(todo.get("id", "")),
                    "title": todo.get("title", ""),
                    "description": todo.get("description"),
                    "status": todo.get("status", "pending"),
                    "priority": todo.get("priority", "medium"),
                    "dueDate": str(todo.get("due_date", "")) if todo.get("due_date") else None,
                    "createdAt": str(todo.get("created_at", "")),
                    "updatedAt": str(todo.get("updated_at", "")),
                }
                transformed_todos.append(transformed_todo)

            logger.info(f"Successfully listed {len(transformed_todos)} tasks")
            return transformed_todos

        except Exception as e:
            log_error(e, "ListTasksSkill.execute")
            raise e


# Convenience functions that map to the skill classes
def add_task(title: str, description: str = None, dueDate: str = None, priority: str = "medium") -> Dict[str, Any]:
    """Add a new task."""
    return AddTaskSkill.execute(title, description, dueDate, priority)


def update_task(id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing task."""
    return UpdateTaskSkill.execute(id, updates)


def delete_task(id: str) -> bool:
    """Delete a task."""
    return DeleteTaskSkill.execute(id)


def list_tasks(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """List tasks."""
    return ListTasksSkill.execute(filters)