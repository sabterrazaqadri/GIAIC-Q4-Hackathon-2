"""Todo API endpoints for CRUD operations."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from api.dependencies import get_db
from models.todo import Todo
from schemas.message import Message
from schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Create a new todo item."""
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/", response_model=list[TodoResponse])
def list_todos(
    db: Annotated[Session, Depends(get_db)],
    is_complete: Optional[bool] = None,
) -> list[Todo]:
    """List all todos, optionally filtered by completion status."""
    query = select(Todo)
    if is_complete is not None:
        query = query.where(Todo.is_complete == is_complete)
    query = query.order_by(Todo.created_at.desc())
    todos = db.exec(query).all()
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Get a single todo by ID."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Update a todo item (full update)."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Update a todo item (partial update)."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete a todo item."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    db.delete(todo)
    db.commit()


@router.patch("/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Mark a todo as complete."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    todo.is_complete = True
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}/incomplete", response_model=TodoResponse)
def reopen_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Todo:
    """Mark a todo as incomplete."""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    todo.is_complete = False
    db.commit()
    db.refresh(todo)
    return todo
