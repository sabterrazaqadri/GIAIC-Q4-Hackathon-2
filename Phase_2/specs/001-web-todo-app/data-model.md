# Data Model: Full-Stack Web Todo Application

## Entity: Todo

### Overview

The `Todo` entity represents a task that users can create, view, update, and delete. It stores all information needed for basic todo management with priority support.

### Schema Definition

```python
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid

class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique identifier for the todo item"
    )
    title: str = Field(
        max_length=200,
        min_length=1,
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
```

### Field Details

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | UUID | Primary Key | Auto-generated | Unique identifier; no two todos share an ID |
| `title` | String | 1-200 chars required | N/A | Brief task summary; shown in todo list |
| `description` | String | 0-2000 chars optional | `null` | Detailed task information |
| `priority` | Enum | Low/Medium/High | Medium | Determines display ordering |
| `is_complete` | Boolean | N/A | `false` | `true` = completed, `false` = pending |
| `created_at` | Timestamp | N/A | Auto-generated | Immutable creation time |
| `updated_at` | Timestamp | N/A | Auto-generated | Updates on every modification |

### Validation Rules

1. **Title Validation**
   - Minimum length: 1 character
   - Maximum length: 200 characters
   - Cannot be whitespace only
   - Required field

2. **Description Validation**
   - Maximum length: 2000 characters
   - Optional field (can be `null`)

3. **Priority Validation**
   - Must be one of: `low`, `medium`, `high`
   - Case-insensitive storage
   - Default: `medium`

4. **Completion Status**
   - Boolean flag (true/false)
   - Toggleable via API

### State Transitions

```
        ┌─────────────────────────────────────┐
        │                                     │
        ▼                                     │
   [CREATED] ──► [UPDATED] ──► [COMPLETED] ◄─┘
        │              │
        │              ▼
        └─────────► [DELETED]
```

- **CREATED**: Initial state after POST to `/todos`
- **UPDATED**: Any field modification via PUT/PATCH
- **COMPLETED**: `is_complete` set to `true`
- **DELETED**: Removed via DELETE (soft or hard delete per implementation)

### Database Constraints

```sql
-- Primary key constraint
ALTER TABLE todo ADD PRIMARY KEY (id);

-- Title not null constraint
ALTER TABLE todo ALTER COLUMN title SET NOT NULL;

-- Priority check constraint
ALTER TABLE todo ADD CONSTRAINT todo_priority_check
    CHECK (priority IN ('low', 'medium', 'high'));

-- Indexes for common queries
CREATE INDEX idx_todo_is_complete ON todo(is_complete);
CREATE INDEX idx_todo_priority ON todo(priority);
CREATE INDEX idx_todo_created_at ON todo(created_at DESC);
```

### API Schemas (Pydantic)

#### Create Todo Request

```python
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    priority: TodoPriority = TodoPriority.MEDIUM
```

#### Update Todo Request

```python
from pydantic import BaseModel
from typing import Optional

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    priority: TodoPriority | None = None
    is_complete: bool | None = None
```

#### Todo Response

```python
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import uuid

class TodoResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    priority: TodoPriority
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Relationships

The `Todo` entity is self-contained with no foreign key relationships in Phase II. Future phases may add:

- **User**: Many-to-one relationship for multi-user support
- **Category**: Many-to-one for todo organization
- **Tag**: Many-to-many for flexible labeling
