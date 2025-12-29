"""Pydantic schemas for Todo API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.todo import TodoPriority


class TodoCreate(BaseModel):
    """Schema for creating a new todo item."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short summary of the task (required)"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Optional detailed description"
    )
    priority: TodoPriority = Field(
        default=TodoPriority.MEDIUM,
        description="Priority level for the todo"
    )

    class Config:
        from_attributes = True


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item (partial update)."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated task summary"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Updated description"
    )
    priority: Optional[TodoPriority] = Field(
        None,
        description="Updated priority level"
    )
    is_complete: Optional[bool] = Field(
        None,
        description="Updated completion status"
    )

    class Config:
        from_attributes = True


class TodoResponse(BaseModel):
    """Schema for todo item in API responses."""
    id: int
    title: str
    description: Optional[str]
    priority: TodoPriority
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for list of todos in API responses."""
    todos: list[TodoResponse]
    count: int
