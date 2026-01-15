"""Todo Task model definition for the conversational todo management system."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status values for todo tasks."""
    PENDING = "pending"
    COMPLETED = "completed"
    IN_PROGRESS = "in-progress"


class TodoTask(BaseModel):
    """
    Todo Task Entity: The primary entity representing a user's task or todo item

    Fields:
    - id: string (unique identifier)
    - title: string (task title)
    - description: string (optional task description)
    - status: enum ['pending', 'completed', 'in-progress'] (task status)
    - dueDate: string (optional due date in ISO format)
    - createdAt: string (timestamp of creation)
    - updatedAt: string (timestamp of last update)
    - userId: string (identifier of the user who owns this task)

    Validation Rules:
    - title must be 1-200 characters
    - description must be 0-1000 characters if provided
    - status must be one of the allowed values
    - dueDate must be a valid future date if provided
    - createdAt and updatedAt are automatically managed by the system
    """

    id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The main title or description of the task"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional details about the task"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status of the task"
    )
    dueDate: Optional[str] = Field(
        None,
        description="Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)"
    )
    createdAt: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Creation timestamp in ISO 8601 format"
    )
    updatedAt: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Last update timestamp in ISO 8601 format"
    )
    userId: str = Field(..., description="Identifier of the user who owns this task")

    class Config:
        use_enum_values = True