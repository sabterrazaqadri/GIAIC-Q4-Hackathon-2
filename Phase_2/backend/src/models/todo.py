"""Todo model definition using SQLModel."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class TodoPriority(str, Enum):
    """Priority levels for todo items."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(SQLModel, table=True):
    """
    Todo item entity representing a task in the system.

    Attributes:
        id: Unique identifier (UUID)
        title: Brief summary of the task (required, 1-200 chars)
        description: Optional detailed description (max 2000 chars)
        priority: Priority level (Low/Medium/High, default: Medium)
        is_complete: Completion status (default: False)
        created_at: Timestamp when the todo was created
        updated_at: Timestamp when the todo was last modified
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Short text summary of the task (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional detailed description of the task"
    )
    priority: TodoPriority = Field(
        default=TodoPriority.MEDIUM,
        description="Priority level affecting display order"
    )
    is_complete: bool = Field(
        default=False,
        description="Completion status of the todo"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the todo was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the todo was last modified"
    )
