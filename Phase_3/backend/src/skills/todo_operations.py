"""Skill functions for todo operations in the conversational todo management system."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from utils.logging_config import logger, log_error
from auth.auth_handler import todo_api_client
from models.todo import TodoTask, TaskStatus
from validators.task_validator import validate_new_task_data, validate_task_update_data


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

            # Prepare the todo data according to the Phase II API schema
            todo_data = {
                "title": title,
                "description": description,
                "priority": priority  # Use provided priority
            }

            # Add dueDate if provided (we'll store it in description if needed)
            if dueDate:
                if description:
                    todo_data["description"] = f"{description} (Due: {dueDate})"
                else:
                    todo_data["description"] = f"Due: {dueDate}"

            # Call the Phase II API to create the task
            result = todo_api_client.create_todo(todo_data)

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": "pending",  # Default to pending when creating
                "dueDate": dueDate,
                "createdAt": result.get("created_at", ""),
                "updatedAt": result.get("updated_at", ""),
                "userId": result.get("userId", "")  # This might not be in Phase II model
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

            # Map our data model to Phase II API schema
            api_updates = {}
            if "title" in updates:
                api_updates["title"] = updates["title"]
            if "description" in updates:
                # Handle dueDate if present in updates
                if "dueDate" in updates:
                    due_date = updates["dueDate"]
                    description = updates["description"] if "description" in updates else ""
                    api_updates["description"] = f"{description} (Due: {due_date})" if description else f"Due: {due_date}"
                else:
                    api_updates["description"] = updates["description"]
            if "status" in updates:
                # Map our status to Phase II's is_complete field
                status = updates["status"]
                if status == "completed":
                    api_updates["is_complete"] = True
                elif status in ["pending", "in-progress"]:
                    api_updates["is_complete"] = False
            if "priority" in updates:
                api_updates["priority"] = updates["priority"]

            # Call the Phase II API to update the task
            result = todo_api_client.update_todo(id, api_updates)

            # Transform the response to match our data model
            transformed_result = {
                "id": str(result.get("id", "")),
                "title": result.get("title", ""),
                "description": result.get("description"),
                "status": "completed" if result.get("is_complete", False) else "pending",
                "dueDate": None,  # Phase II doesn't have dueDate field
                "createdAt": result.get("created_at", ""),
                "updatedAt": result.get("updated_at", ""),
                "userId": result.get("userId", "")  # This might not be in Phase II model
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

            # Call the Phase II API to delete the task
            todo_api_client.delete_todo(id)

            logger.info(f"Successfully deleted task with ID: {id}")
            return True

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

            # Prepare filters for the Phase II API
            api_filters = {}
            if filters:
                # Map our filters to Phase II API filters
                if "status" in filters:
                    # Map our status to Phase II's is_complete field
                    if filters["status"] == "completed":
                        api_filters["is_complete"] = True
                    elif filters["status"] in ["pending", "in-progress"]:
                        api_filters["is_complete"] = False
                elif "is_complete" in filters:
                    # If the filter is already in Phase II format
                    api_filters["is_complete"] = filters["is_complete"]

            # Call the Phase II API to list tasks
            result = todo_api_client.list_todos(api_filters)

            # The API returns a list of todos, but we need to handle the response format
            if isinstance(result, list):
                todos = result
            elif isinstance(result, dict) and 'todos' in result:
                todos = result['todos']
            else:
                todos = [result] if result else []

            # Transform the response to match our data model
            transformed_todos = []
            for todo in todos:
                # Determine the status based on is_complete field
                status = "completed" if todo.get("is_complete", False) else "pending"

                # For "in-progress" status, we need special handling since Phase II doesn't have this
                # For now, we'll map tasks with certain keywords or characteristics to "in-progress"
                # In a real implementation, you might have additional logic to determine this
                if status == "pending":
                    # Check if the task description or title suggests it's in progress
                    title = todo.get("title", "").lower()
                    description = (todo.get("description") or "").lower()
                    if any(keyword in title or keyword in description for keyword in ["working on", "in progress", "started"]):
                        status = "in-progress"

                transformed_todo = {
                    "id": str(todo.get("id", "")),
                    "title": todo.get("title", ""),
                    "description": todo.get("description"),
                    "status": status,
                    "dueDate": None,  # Phase II doesn't have dueDate field
                    "createdAt": todo.get("created_at", ""),
                    "updatedAt": todo.get("updated_at", ""),
                    "userId": todo.get("userId", "")  # This might not be in Phase II model
                }

                # Apply additional filtering on our end if needed
                include_task = True
                if filters:
                    if "status" in filters and filters["status"] != transformed_todo["status"]:
                        include_task = False

                if include_task:
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