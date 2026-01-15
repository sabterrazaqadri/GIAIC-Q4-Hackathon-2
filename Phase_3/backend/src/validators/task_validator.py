"""Validation functions for task creation and updates based on data-model.md requirements."""

from typing import Dict, Any, Optional
from datetime import datetime
from utils.logging_config import logger, InvalidTaskDataException


def validate_task_title(title: str) -> None:
    """
    Validate task title based on data-model.md requirements.

    Requirements:
    - title must be 1-200 characters
    """
    if not title:
        raise InvalidTaskDataException("title", "Title is required")

    if len(title) < 1:
        raise InvalidTaskDataException("title", "Title must be at least 1 character")

    if len(title) > 200:
        raise InvalidTaskDataException("title", f"Title must be no more than 200 characters, got {len(title)}")


def validate_urdu_text(text: str) -> None:
    """
    Validate Urdu text for proper format and encoding.
    This function checks if the provided text is valid Urdu text.
    """
    if not text:
        return  # Urdu text is optional for most fields

    # Check if the text contains Urdu characters
    urdu_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
    if urdu_pattern.search(text):
        # Additional validation could be added here if needed
        # For now, we just ensure it's not empty when it contains Urdu
        if len(text.strip()) == 0:
            raise InvalidTaskDataException("text", "Urdu text cannot be empty")


def validate_task_description(description: Optional[str]) -> None:
    """
    Validate task description based on data-model.md requirements.

    Requirements:
    - description must be 0-1000 characters if provided
    """
    if description is None:
        return  # Description is optional

    if len(description) > 1000:
        raise InvalidTaskDataException("description", f"Description must be no more than 1000 characters, got {len(description)}")


def validate_task_status(status: str) -> None:
    """
    Validate task status based on data-model.md requirements.

    Requirements:
    - status must be one of the allowed values ['pending', 'completed', 'in-progress']
    """
    valid_statuses = ['pending', 'completed', 'in-progress']

    if status not in valid_statuses:
        raise InvalidTaskDataException("status", f"Status must be one of {valid_statuses}, got '{status}'")


def validate_task_due_date(due_date: Optional[str]) -> None:
    """
    Validate task due date based on data-model.md requirements.

    Requirements:
    - dueDate must be a valid future date if provided
    """
    if due_date is None:
        return  # Due date is optional

    try:
        # Parse the date string - expect ISO 8601 format
        parsed_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        # Check if it's a future date
        if parsed_date < datetime.utcnow():
            raise InvalidTaskDataException("dueDate", "Due date must be a future date")
    except ValueError:
        raise InvalidTaskDataException("dueDate", f"Invalid date format: {due_date}. Expected ISO 8601 format.")


def validate_new_task_data(title: str, description: Optional[str] = None,
                          status: Optional[str] = None, due_date: Optional[str] = None) -> None:
    """
    Validate all task data for new task creation based on data-model.md requirements.

    Requirements from data-model.md:
    - title must be 1-200 characters
    - description must be 0-1000 characters if provided
    - status must be one of the allowed values
    - dueDate must be a valid future date if provided
    - createdAt and updatedAt are automatically managed by the system
    """
    logger.info("Validating new task data")

    # Validate title (required)
    validate_task_title(title)

    # Validate description (optional)
    validate_task_description(description)

    # Validate status (optional for creation, defaults to 'pending')
    if status:
        validate_task_status(status)

    # Validate due date (optional)
    validate_task_due_date(due_date)

    logger.info("Task data validation completed successfully")


def validate_task_update_data(updates: Dict[str, Any]) -> None:
    """
    Validate task update data based on data-model.md requirements.

    Requirements from data-model.md:
    - title must be 1-200 characters if provided
    - description must be 0-1000 characters if provided
    - status must be one of the allowed values if provided
    - dueDate must be a valid future date if provided
    """
    logger.info("Validating task update data")

    if "title" in updates:
        validate_task_title(updates["title"])

    if "description" in updates:
        validate_task_description(updates["description"])

    if "status" in updates:
        validate_task_status(updates["status"])

    if "dueDate" in updates:
        validate_task_due_date(updates["dueDate"])

    logger.info("Task update data validation completed successfully")


def validate_task_filters(filters: Optional[Dict[str, Any]]) -> None:
    """
    Validate task filtering parameters.
    """
    if not filters:
        return

    logger.info("Validating task filters")

    # Validate status filter if present
    if "status" in filters:
        validate_task_status(filters["status"])

    # Validate due date filter if present
    if "dueDate" in filters:
        validate_task_due_date(filters["dueDate"])

    logger.info("Task filters validation completed successfully")