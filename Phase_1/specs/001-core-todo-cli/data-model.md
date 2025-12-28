# Data Model: Core CLI Todo Application

**Feature**: 001-core-todo-cli
**Date**: 2025-12-26
**Purpose**: Define data entities, relationships, validation rules, and state management

## Entity Overview

The Core CLI Todo Application has a single primary entity: **Task**. This entity represents a todo item with support for future extensibility.

## Task Entity

### Description

A Task represents a single todo item that a user wants to track. Tasks have a unique identifier, required title, optional description, and completion status. The model is designed to be extensible for Phase II/III enhancements (priority, due dates, recurrence, tags) without breaking existing functionality.

### Fields

| Field | Type | Required | Default | Description | Validation Rules |
|-------|------|----------|---------|-------------|------------------|
| `id` | `int` | Yes | Auto-generated | Unique sequential identifier starting from 1 | Positive integer, auto-increment, never reused |
| `title` | `str` | Yes | (none) | Main task description | Non-empty string, max 200 chars recommended for display |
| `description` | `str` | No | `""` (empty string) | Additional task details | Any string, may be empty |
| `completed` | `bool` | Yes | `False` | Completion status indicator | True (completed) or False (pending) |

### Python Implementation

```python
from dataclasses import dataclass, asdict
from typing import Dict

@dataclass
class Task:
    """
    Represents a todo item with unique ID, title, optional description, and completion status.

    Attributes:
        id: Unique sequential integer identifier (auto-generated)
        title: Required main task description
        description: Optional additional task details (default: empty string)
        completed: Boolean completion status (default: False/pending)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def to_dict(self) -> Dict[str, any]:
        """
        Convert Task instance to dictionary for serialization (future JSON API).

        Returns:
            Dictionary with id, title, description, completed fields
        """
        return asdict(self)

    def __str__(self) -> str:
        """
        Human-readable string representation for CLI display.

        Returns:
            Formatted string: "Task #<id>: <title> [<status>]"
        """
        status = "completed" if self.completed else "pending"
        return f"Task #{self.id}: {self.title} [{status}]"
```

### Field Validation Rules

**id (Unique Identifier)**:
- MUST be a positive integer (>= 1)
- MUST be unique across all tasks in the session
- MUST be auto-generated (users never provide IDs)
- MUST be sequential (incremented by TaskService)
- MUST NOT be reused after task deletion (IDs are stable)

**title (Required Task Description)**:
- MUST be a non-empty string
- MUST be provided by user (no default)
- SHOULD be limited to 200 characters for display readability (not enforced, but truncated in list view)
- MAY contain any valid UTF-8 characters (including Urdu in future phases)

**description (Optional Task Details)**:
- MAY be an empty string (default)
- MAY be omitted by user (defaults to "")
- MAY contain any valid UTF-8 characters
- NO length limit (full content stored and displayed on demand)

**completed (Completion Status)**:
- MUST be a boolean value (True or False)
- MUST default to False when task is created
- MUST be toggled via TaskService methods (not directly set by CLI)

### State Transitions

Tasks have two states: **pending** (not completed) and **completed**. State transitions are managed by the TaskService.

```
         ┌─────────────┐
         │   Created   │
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
    ┌───►│   Pending   │◄───┐
    │    └──────┬──────┘    │
    │           │            │
    │           │ complete() │ incomplete()
    │           │            │
    │    ┌──────▼──────┐    │
    └────┤  Completed  ├────┘
         └─────────────┘
```

**State Transitions**:
1. **Created → Pending**: Automatic when task is added (completed=False)
2. **Pending → Completed**: User calls `complete <id>` command (completed=True)
3. **Completed → Pending**: User calls `incomplete <id>` command (completed=False)
4. **Pending/Completed → Deleted**: User calls `delete <id>` command (removed from storage)

**State Validation**:
- Task MUST exist (have valid ID) to transition states
- Completed status is idempotent (calling `complete` on already completed task is allowed)
- Deleted tasks cannot be recovered in Phase I (in-memory, no undo)

### Extensibility Design (Phase II/III)

The Task model is designed to accommodate future enhancements without breaking existing functionality:

**Reserved Future Fields** (not implemented in Phase I):
```python
# Phase II/III additions
from typing import Optional, List
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False

    # Phase II additions (optional fields)
    priority: Optional[int] = None           # 1=high, 2=medium, 3=low
    due_date: Optional[datetime] = None       # Deadline for task
    tags: List[str] = field(default_factory=list)  # Category tags

    # Phase III additions (optional fields)
    recurrence: Optional[str] = None          # "daily", "weekly", "monthly"
    assigned_to: Optional[str] = None         # User ID for multi-user
    created_at: Optional[datetime] = None     # Timestamp
    updated_at: Optional[datetime] = None     # Timestamp
```

**Backward Compatibility Strategy**:
- All new fields MUST be optional (have default values)
- Phase I code ignores new fields (no impact)
- Phase II/III API can return additional fields without breaking Phase I CLI
- Serialization (to_dict()) automatically includes all fields

---

## TaskService State Management

### Description

TaskService is a stateful class that manages the in-memory task collection and ID generation. It provides CRUD operations and completion status management.

### State Fields

| Field | Type | Description | Initial Value |
|-------|------|-------------|---------------|
| `tasks` | `List[Task]` | In-memory task storage | `[]` (empty list) |
| `next_id` | `int` | Auto-increment counter for IDs | `1` |

### Python Implementation

```python
from typing import List, Optional

class TaskService:
    """
    Manages task storage and operations (add, retrieve, update, delete, toggle complete).

    Uses in-memory list for storage with sequential numeric IDs.
    Thread-safe for single-threaded CLI usage (Phase I).
    """

    def __init__(self):
        """Initialize TaskService with empty task list and ID counter at 1."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new task.

        Args:
            title: Required task title (non-empty)
            description: Optional task description (default: "")

        Returns:
            The newly created Task instance

        Raises:
            ValueError: If title is empty
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
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in insertion order.

        Returns:
            List of all Task instances (may be empty)
        """
        return self.tasks.copy()  # Return copy to prevent external mutation

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a single task by ID.

        Args:
            task_id: The task's unique identifier

        Returns:
            The Task instance with the given ID

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None:
            raise ValueError(f"Task not found with ID {task_id}")
        return task

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The task's unique identifier
            title: New title (optional, None = no change)
            description: New description (optional, None = no change)

        Returns:
            The updated Task instance

        Raises:
            ValueError: If task not found or title is empty when provided
        """
        task = self.get_task(task_id)  # Raises ValueError if not found

        if title is not None:
            if not title or title.strip() == "":
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The task's unique identifier

        Returns:
            True if task was deleted

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = self.get_task(task_id)  # Raises ValueError if not found
        self.tasks.remove(task)
        return True

    def toggle_complete(self, task_id: int, completed: bool) -> Task:
        """
        Toggle task completion status.

        Args:
            task_id: The task's unique identifier
            completed: True to mark complete, False to mark pending

        Returns:
            The updated Task instance

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = self.get_task(task_id)  # Raises ValueError if not found
        task.completed = completed
        return task
```

### State Persistence

**Phase I (Current)**:
- Storage: In-memory Python list
- Lifecycle: Data exists only during application runtime
- On exit: All tasks are lost (by design)
- On restart: Fresh TaskService with empty task list and next_id=1

**Phase II (Future)**:
- Storage: Database or file (e.g., SQLite, JSON file)
- Lifecycle: Data persists across sessions
- On exit: Tasks saved to storage
- On restart: Tasks loaded from storage, next_id computed from max(task.id) + 1

**Migration Strategy**:
- TaskService interface remains unchanged
- Constructor accepts optional storage backend: `TaskService(storage: Optional[Storage] = None)`
- CLI layer unaware of storage mechanism

---

## Data Flow Diagram

### Add Task Flow

```
┌──────────┐      ┌──────────┐      ┌──────────────┐      ┌──────────┐
│   User   │─────►│   CLI    │─────►│ TaskService  │─────►│  Task    │
│          │      │ (main.py)│      │ (add_task)   │      │  List    │
└──────────┘      └──────────┘      └──────────────┘      └──────────┘
    │                   │                    │                    │
    │ "add 'Title'"     │ parse args         │ create Task        │
    │                   │ extract title      │ assign next_id     │
    │                   │ call add_task()    │ append to list     │
    │                   │                    │ increment next_id  │
    │                   │◄───────────────────┤ return Task        │
    │◄──────────────────┤ print confirmation │                    │
    │ "Task #1 added"   │                    │                    │
```

### View Tasks Flow

```
┌──────────┐      ┌──────────┐      ┌──────────────┐      ┌──────────┐
│   User   │─────►│   CLI    │─────►│ TaskService  │─────►│  Task    │
│          │      │ (main.py)│      │ (get_all)    │      │  List    │
└──────────┘      └──────────┘      └──────────────┘      └──────────┘
    │                   │                    │                    │
    │ "list"            │ call get_all_tasks()                    │
    │                   │◄───────────────────┤ return tasks copy  │
    │                   │ format as table    │                    │
    │◄──────────────────┤ print table        │                    │
    │ ID Title Status   │                    │                    │
```

### Update Task Flow

```
┌──────────┐      ┌──────────┐      ┌──────────────┐      ┌──────────┐
│   User   │─────►│   CLI    │─────►│ TaskService  │─────►│  Task    │
│          │      │ (main.py)│      │ (update)     │      │ Instance │
└──────────┘      └──────────┘      └──────────────┘      └──────────┘
    │                   │                    │                    │
    │ "update 1         │ parse args         │ find task by ID    │
    │  --title 'New'"   │ call update_task() │ update task.title  │
    │                   │                    │                    │
    │                   │◄───────────────────┤ return Task        │
    │◄──────────────────┤ print confirmation │                    │
    │ "Task #1 updated" │                    │                    │
```

---

## Validation Rules Summary

### Input Validation (CLI Layer)

- Task ID must be provided as integer (argparse type=int)
- Title must be provided for add command (argparse required=True)
- Description is optional (argparse default=None)

### Business Logic Validation (Service Layer)

- Title must not be empty or whitespace-only → `ValueError("Title is required")`
- Task ID must exist in storage → `ValueError("Task not found with ID {id}")`
- Update with empty title → `ValueError("Title cannot be empty")`

### Display Validation (CLI Layer)

- Truncate long titles (>30 chars) in list view for readability
- Show full title in detailed view or confirmation messages
- Format completed status as "✓ completed" or "pending" for clarity

---

## Error Handling

### Service Layer Exceptions

All TaskService methods raise `ValueError` with descriptive messages:

| Error Condition | Exception Message | CLI Action |
|----------------|-------------------|-----------|
| Empty title on add | "Title is required" | Print error, exit 1 |
| Task not found | "Task not found with ID {id}" | Print error, exit 1 |
| Empty title on update | "Title cannot be empty" | Print error, exit 1 |

### CLI Layer Handling

```python
try:
    result = task_service.method(...)
    print(success_message)
    sys.exit(0)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

---

## Future Considerations

### Phase II Enhancements

**Database Schema** (SQLite example):
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    completed BOOLEAN DEFAULT 0,
    priority INTEGER,
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Repository Pattern**:
```python
class TaskRepository:
    def save(self, task: Task) -> Task: ...
    def find_by_id(self, task_id: int) -> Optional[Task]: ...
    def find_all(self) -> List[Task]: ...
    def delete(self, task_id: int) -> bool: ...

# TaskService uses repository
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
```

### Phase III AI Agent Integration

**Agent Interface** (already AI-ready):
```python
# AI agent code
service = TaskService()
task = service.add_task("AI-generated task")
all_tasks_dict = [t.to_dict() for t in service.get_all_tasks()]
# Send to LLM, receive command, execute via service methods
```

---

## Data Model Sign-Off

All entities, fields, validation rules, state transitions, and extensibility considerations documented. Ready to proceed to CLI Contracts definition.

**Reviewer**: Claude Sonnet 4.5
**Date**: 2025-12-26
**Status**: ✅ Complete
