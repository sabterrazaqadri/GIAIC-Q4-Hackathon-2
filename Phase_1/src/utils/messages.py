"""
Message constants for the Core CLI Todo Application.

Centralizes all user-facing messages for consistency and future i18n support (Urdu/English).
"""

# Success messages
TASK_ADDED = "Task #{id} added: {title}"
TASK_UPDATED = "Task #{id} updated."
TASK_DELETED = "Task #{id} deleted."
TASK_COMPLETED = "Task #{id} marked as completed."
TASK_INCOMPLETE = "Task #{id} marked as pending."

# Error messages
TASK_NOT_FOUND = "Task not found with ID {id}"
TITLE_REQUIRED = "Title is required"
TITLE_EMPTY = "Title cannot be empty"
NO_UPDATES_PROVIDED = "At least one of --title or --description must be provided"

# Info messages
NO_TASKS_FOUND = "No tasks found."

# Status labels
STATUS_COMPLETED = "completed"
STATUS_PENDING = "pending"
