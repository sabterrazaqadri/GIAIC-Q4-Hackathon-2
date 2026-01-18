"""Skill functions for todo operations in the conversational todo management system."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from utils.logging_config import logger, log_error
# Removed API client - using database directly now
from models.todo import TodoTask, TaskStatus
from validators.task_validator import validate_new_task_data, validate_task_update_data


class AddTaskSkill:
    """Skill for adding new tasks."""

    @staticmethod
    async def execute(title: str, description: str = None, dueDate: str = None, priority: str = "medium") -> Dict[str, Any]:
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

            # Import database operations
            from db.todo_operations import add_task_db

            # Prepare the todo data according to the database schema
            priority_level = priority.lower() if priority.lower() in ["low", "medium", "high"] else "medium"

            # Add task to database
            result = await add_task_db(
                title=title,
                description=description,
                status="pending",  # Default to pending when creating
                priority=priority_level,
                due_date=dueDate
            )

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": result.get("status", "pending"),
                "dueDate": result.get("due_date"),
                "createdAt": result.get("created_at", ""),
                "updatedAt": result.get("updated_at", ""),
                "priority": result.get("priority", "medium")
            }

            logger.info(f"Successfully added task with ID: {transformed_result['id']}")
            return transformed_result

        except Exception as e:
            log_error(e, "AddTaskSkill.execute")
            raise


class UpdateTaskSkill:
    """Skill for updating existing tasks."""

    @staticmethod
    async def execute(id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
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

            # Import database operations
            from db.todo_operations import update_task_db

            # Map our data model to database schema
            db_updates = {}
            if "title" in updates:
                db_updates["title"] = updates["title"]
            if "description" in updates:
                db_updates["description"] = updates["description"]
            if "status" in updates:
                status = updates["status"]
                # Normalize status values
                if status.lower() in ["completed", "done", "finished"]:
                    db_updates["status"] = "completed"
                elif status.lower() in ["pending", "not started"]:
                    db_updates["status"] = "pending"
                elif status.lower() in ["in-progress", "in progress", "working on it"]:
                    db_updates["status"] = "in-progress"
                else:
                    db_updates["status"] = status.lower()
            if "priority" in updates:
                priority = updates["priority"].lower()
                if priority in ["low", "medium", "high"]:
                    db_updates["priority"] = priority
            if "dueDate" in updates:
                db_updates["due_date"] = updates["dueDate"]

            # Update task in database
            result = await update_task_db(id, db_updates)

            if not result:
                raise ValueError(f"Task with ID {id} not found")

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": result.get("status", "pending"),
                "dueDate": result.get("due_date"),
                "createdAt": result.get("created_at", ""),
                "updatedAt": result.get("updated_at", ""),
                "priority": result.get("priority", "medium")
            }

            logger.info(f"Successfully updated task with ID: {transformed_result['id']}")
            return transformed_result

        except Exception as e:
            log_error(e, "UpdateTaskSkill.execute")
            raise e


class DeleteTaskSkill:
    """Skill for deleting tasks."""

    @staticmethod
    async def execute(id: str) -> bool:
        """
        Execute the delete task skill.

        Args:
            id: The ID of the task to delete

        Returns:
            Boolean indicating success
        """
        try:
            logger.info(f"Executing delete_task skill for task ID: {id}")

            # Import database operations
            from db.todo_operations import delete_task_db

            # Delete task from database
            success = await delete_task_db(int(id))

            if success:
                logger.info(f"Successfully deleted task with ID: {id}")
            else:
                logger.warning(f"Task with ID {id} not found for deletion")

            return success

        except Exception as e:
            log_error(e, "DeleteTaskSkill.execute")
            raise e


class ListTasksSkill:
    """Skill for listing tasks."""

    @staticmethod
    async def execute(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute the list tasks skill.

        Args:
            filters: Optional dictionary containing filter criteria

        Returns:
            List of tasks
        """
        try:
            logger.info(f"Executing list_tasks skill with filters: {filters}")

            # Import database operations
            from db.todo_operations import list_tasks_db

            # Prepare filters for the database
            db_filters = {}
            if filters:
                # Map our filters to database schema
                if "status" in filters:
                    db_filters["status"] = filters["status"]
                if "priority" in filters:
                    db_filters["priority"] = filters["priority"]
                if "search" in filters:
                    db_filters["search"] = filters["search"]

            # Get tasks from database
            result = await list_tasks_db(db_filters)

            # Transform the response to match our data model
            transformed_todos = []
            for task in result:
                transformed_todo = {
                    "id": str(task.get("id", "")),
                    "title": task.get("title", ""),
                    "description": task.get("description"),
                    "status": task.get("status", "pending"),
                    "dueDate": task.get("due_date"),  # Use due_date from database
                    "createdAt": task.get("created_at", ""),
                    "updatedAt": task.get("updated_at", ""),
                    "priority": task.get("priority", "medium")
                }

                transformed_todos.append(transformed_todo)

            logger.info(f"Successfully listed {len(transformed_todos)} tasks")
            return transformed_todos

        except Exception as e:
            log_error(e, "ListTasksSkill.execute")
            raise e


# Convenience functions that map to the skill classes
async def add_task(title: str, description: str = None, dueDate: str = None, priority: str = "medium") -> Dict[str, Any]:
    """Add a new task."""
    return await AddTaskSkill.execute(title, description, dueDate, priority)


async def update_task(id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing task."""
    return await UpdateTaskSkill.execute(id, updates)


async def delete_task(id: str) -> bool:
    """Delete a task."""
    return await DeleteTaskSkill.execute(id)


async def list_tasks(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """List tasks."""
    return await ListTasksSkill.execute(filters)