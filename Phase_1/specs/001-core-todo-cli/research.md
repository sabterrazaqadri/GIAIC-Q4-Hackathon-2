# Research: Core CLI Todo Application

**Feature**: 001-core-todo-cli
**Date**: 2025-12-26
**Purpose**: Document research findings and architectural decisions for Phase I CLI todo app

## Research Overview

This document consolidates research on Python CLI best practices, in-memory storage patterns, and architectural decisions for the Core CLI Todo Application. All decisions are made with Phase II/III evolution in mind while maintaining Phase I simplicity.

## Research Topics

### 1. Python CLI Argument Parsing with argparse

**Research Question**: What is the best practice for implementing CLI subcommands in Python 3.13?

**Findings**:

argparse provides built-in support for subcommands via `add_subparsers()`. Best practices include:

- Use `add_subparsers(dest='command')` to capture the command name
- Create a separate parser for each subcommand with `subparsers.add_parser('command_name')`
- Use `set_defaults(func=handler_function)` to map commands to handler functions
- Leverage `add_argument()` with `required=True/False` for command-specific options
- Use `type=` parameter for automatic type conversion (e.g., `type=int` for task IDs)
- Auto-generated help with `--help` for main command and each subcommand

**Example Pattern**:
```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

add_parser = subparsers.add_parser('add', help='Add a new task')
add_parser.add_argument('title', help='Task title')
add_parser.add_argument('--description', help='Task description')
add_parser.set_defaults(func=add_command)

list_parser = subparsers.add_parser('list', help='List all tasks')
list_parser.set_defaults(func=list_command)
```

**Decision**: Use argparse with subparsers pattern for clean command routing

**References**:
- Python argparse documentation: https://docs.python.org/3/library/argparse.html
- PEP 389 (argparse module): https://www.python.org/dev/peps/pep-0389/

---

### 2. In-Memory Storage Patterns for Python

**Research Question**: What is the optimal data structure for storing tasks in-memory with sequential ID generation?

**Findings**:

**Option A: List with Linear Search**
- Store tasks in a list: `tasks: List[Task] = []`
- Use separate counter for IDs: `next_id: int = 1`
- Search by ID: `next((t for t in tasks if t.id == id), None)`
- Performance: O(n) search, O(1) append, O(n) delete
- Best for: Small collections (< 1000 items)

**Option B: Dict with ID Keys**
- Store tasks in dict: `tasks: Dict[int, Task] = {}`
- Use separate counter for IDs: `next_id: int = 1`
- Search by ID: `tasks.get(id)`
- Performance: O(1) search, O(1) insert, O(1) delete
- Best for: Large collections or frequent lookups

**Option C: List with Index as ID**
- Use list index as task ID
- No separate ID counter needed
- Performance: O(1) search by index, but IDs change on delete
- Best for: Never used (breaks ID stability)

**Decision**: Use **Option A: List with Linear Search**

**Rationale**:
- Phase I expected scale: 10-100 tasks (linear search is fast enough)
- Simplicity: List operations are intuitive, code is readable
- Iteration: List maintains insertion order for display
- Migration path: Can swap to dict in Phase II if needed without API changes

**Trade-offs**:
- Pro: Simple, readable code
- Pro: Insertion order preserved for display
- Pro: Easy to implement and reason about
- Con: O(n) search (acceptable for <1000 tasks)
- Con: Must manage ID counter separately (simple counter)

---

### 3. ID Management Strategy

**Research Question**: Should we use numeric IDs, UUIDs, or list indices for task identification?

**Findings**:

**Option A: Sequential Numeric IDs (1, 2, 3, ...)**
- User types: `python -m src.cli.main complete 1`
- Implementation: `next_id` counter, increment on each add
- Reuse after delete: No (IDs never reused)
- CLI UX: Excellent (short, memorable)

**Option B: UUIDs (e.g., 3f8e9d2a-5b7c-4e1f-9a3b-2c5d8f7e1a4b)**
- User types: `python -m src.cli.main complete 3f8e9d2a-5b7c-4e1f-9a3b-2c5d8f7e1a4b`
- Implementation: `import uuid; uuid.uuid4()`
- Reuse after delete: N/A (globally unique)
- CLI UX: Poor (too long to type)

**Option C: List Index (0, 1, 2, ...)**
- User types: `python -m src.cli.main complete 0`
- Implementation: Use list.index(task)
- Reuse after delete: Yes (indices shift)
- CLI UX: Confusing (IDs change after delete)

**Decision**: Use **Option A: Sequential Numeric IDs**

**Rationale**:
- CLI usability: Users can easily remember and type "1", "2", "3"
- Stability: IDs never change, even after deletes
- Human-readable: Task #1, Task #2, etc.
- Phase I scope: Single-user, no distributed system concerns

**Trade-offs**:
- Pro: Best CLI user experience
- Pro: IDs are stable (predictable behavior)
- Pro: Simple counter implementation
- Con: IDs not reused after delete (expected, not a problem)
- Con: Not suitable for distributed systems (Phase III concern, can add UUIDs later)

**Future Phase Considerations**:
- Phase II: Numeric IDs remain for CLI, can add UUID as secondary field
- Phase III: AI agents may prefer numeric IDs for readability in logs

---

### 4. Error Handling Pattern

**Research Question**: Should service layer methods raise exceptions or return result objects?

**Findings**:

**Option A: Exception-Based**
- Raise `ValueError("Task not found")` for invalid operations
- CLI layer catches exceptions and formats error messages
- Pythonic: Follows "easier to ask forgiveness" (EAFP) principle

**Option B: Result Object Pattern**
- Return `Result[Task, Error]` tuple or custom Result class
- CLI layer checks result.is_success() before proceeding
- Explicit: No hidden control flow

**Option C: None for Errors**
- Return `None` on error, actual value on success
- CLI layer checks `if result is None`
- Simple but loses error context

**Decision**: Use **Option A: Exception-Based**

**Rationale**:
- Pythonic: Standard Python pattern for error handling
- Clean service API: Methods return Task directly, not wrapped
- Error context: Exception messages provide clear error descriptions
- CLI layer responsibility: Format exceptions into user-friendly messages

**Implementation Pattern**:
```python
# Service layer
def get_task(self, task_id: int) -> Task:
    task = next((t for t in self.tasks if t.id == task_id), None)
    if task is None:
        raise ValueError(f"Task not found with ID {task_id}")
    return task

# CLI layer
try:
    task = task_service.get_task(task_id)
    print(f"Task #{task.id}: {task.title}")
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

**Trade-offs**:
- Pro: Pythonic and standard
- Pro: Clean service method signatures
- Pro: Exception messages provide clear context
- Con: Requires try/except in CLI layer (acceptable)

---

### 5. CLI Output Formatting

**Research Question**: How should we format task lists and messages for optimal readability?

**Findings**:

**List Display Options**:

**Option A: Simple Line-by-Line**
```
1. Buy groceries [pending]
2. Write report [completed]
```

**Option B: Aligned Table with Borders**
```
+----+------------------+-----------+
| ID | Title            | Status    |
+----+------------------+-----------+
| 1  | Buy groceries    | pending   |
| 2  | Write report     | completed |
+----+------------------+-----------+
```

**Option C: Tab-Separated Columns**
```
ID   Title              Status
1    Buy groceries      pending
2    Write report       completed
```

**Decision**: Use **Option C: Tab-Separated Columns** (or formatted strings with .format())

**Rationale**:
- Readable: Clear columns without ASCII art overhead
- Simple: Easy to implement with f-strings or str.format()
- Extensible: Easy to add more columns in Phase II
- Standard: Follows common CLI tool patterns (ls, ps, etc.)

**Implementation Pattern**:
```python
print(f"{'ID':<5} {'Title':<30} {'Status':<10}")
print("-" * 47)
for task in tasks:
    status = "✓ completed" if task.completed else "pending"
    title = task.title[:30]  # Truncate long titles
    print(f"{task.id:<5} {title:<30} {status:<10}")
```

**Trade-offs**:
- Pro: Readable and professional
- Pro: Simple to implement
- Pro: Extensible (add columns easily)
- Con: Fixed column widths (acceptable for CLI)

---

### 6. Dataclass Serialization for Future API

**Research Question**: How should we implement Task.to_dict() for future JSON API support?

**Findings**:

**Option A: Manual to_dict() Method**
```python
def to_dict(self) -> dict:
    return {
        'id': self.id,
        'title': self.title,
        'description': self.description,
        'completed': self.completed
    }
```

**Option B: dataclasses.asdict()**
```python
from dataclasses import asdict
task_dict = asdict(task_instance)
```

**Option C: Pydantic Model**
- Use Pydantic BaseModel instead of dataclass
- Auto JSON serialization with .dict()
- Requires external dependency

**Decision**: Use **Option B: dataclasses.asdict()** (with optional manual override for future customization)

**Rationale**:
- Standard library: `dataclasses.asdict()` is built-in
- Automatic: Works for all fields without manual maintenance
- Extensible: Add fields to dataclass, serialization auto-updates
- Future-ready: Phase II API can use asdict() directly

**Implementation Pattern**:
```python
from dataclasses import dataclass, asdict

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

# Usage in future API
task_dict = task.to_dict()  # Ready for json.dumps()
```

**Trade-offs**:
- Pro: Zero maintenance (auto-updates with new fields)
- Pro: Standard library (no dependencies)
- Pro: Can be overridden if custom serialization needed
- Con: Serializes all fields (may need @field(metadata={'private': True}) in future)

---

## Technology Stack Summary

**Language & Version**: Python 3.13+

**Core Libraries** (Standard Library Only):
- `argparse` - CLI argument parsing and subcommands
- `dataclasses` - Task entity model with type safety
- `sys` - Exit codes and stderr for errors
- `typing` - Type hints (List, Optional, Dict)

**Project Structure**:
- `src/models/task.py` - Task dataclass
- `src/services/task_service.py` - TaskService class (business logic)
- `src/cli/main.py` - argparse setup and CLI entry point
- `src/cli/commands.py` - Command handler functions
- `src/utils/messages.py` - Message constants (i18n-ready)

**Development Tools**:
- Python 3.13 interpreter
- Git for version control
- Claude Code for code generation

**No External Dependencies**: Phase I uses only Python standard library

---

## Architectural Patterns Summary

### Service Layer Pattern

**TaskService Class**:
- Encapsulates business logic
- Manages in-memory task storage (list)
- Manages ID generation (counter)
- Raises exceptions for errors
- Returns Task instances or lists

**Public Interface** (AI Agent-Ready):
```python
class TaskService:
    def add_task(self, title: str, description: str = "") -> Task
    def get_all_tasks(self) -> List[Task]
    def get_task(self, task_id: int) -> Task
    def update_task(self, task_id: int, title: str = None, description: str = None) -> Task
    def delete_task(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int, completed: bool) -> Task
```

### CLI Command Pattern

**Command Handlers**:
- Each subcommand has a handler function
- Handlers instantiate TaskService
- Handlers format output for CLI
- Handlers catch exceptions and format errors

**Flow**:
1. argparse parses args and calls handler
2. Handler calls TaskService method
3. TaskService raises exception on error
4. Handler catches exception, prints error, exits with code 1
5. Handler formats success output, exits with code 0

### Message Externalization Pattern

**utils/messages.py**:
- Define message constants/templates
- Enable future i18n (Urdu/English)
- Centralize user-facing text

**Example**:
```python
# messages.py
TASK_ADDED = "Task #{id} added: {title}"
TASK_NOT_FOUND = "Task not found with ID {id}"
TITLE_REQUIRED = "Title is required"

# Usage in CLI
from utils.messages import TASK_ADDED
print(TASK_ADDED.format(id=task.id, title=task.title))
```

---

## Best Practices Applied

1. **PEP 8 Compliance**: All code follows Python style guide
2. **Type Hints**: Use typing module for all function signatures
3. **Docstrings**: Add docstrings to classes and public methods
4. **Single Responsibility**: Each module has one clear purpose
5. **Dependency Injection**: TaskService can be instantiated with initial state (for testing)
6. **Error Messages**: Clear, actionable error messages for users
7. **Exit Codes**: 0 for success, 1 for errors (CLI convention)
8. **Help Text**: Use argparse help= for all commands and arguments

---

## Phase II/III Evolution Considerations

### Phase II: Persistent Storage

**Current Design Enables**:
- Swap `List[Task]` for database repository
- Service interface remains unchanged
- CLI layer unaware of storage change

**Example Migration**:
```python
# Phase I: TaskService.__init__()
self.tasks: List[Task] = []

# Phase II: TaskService.__init__(db: Database)
self.db = db  # Repository pattern
```

### Phase III: AI Agent Integration

**Current Design Enables**:
- AI agents call TaskService methods directly
- Task.to_dict() provides JSON-serializable output
- Service methods return structured data (Task instances)

**Example Agent Usage**:
```python
# AI Agent code (Phase III)
from src.services.task_service import TaskService

service = TaskService()
task = service.add_task("AI-generated task", "Description")
all_tasks = service.get_all_tasks()
task_data = [t.to_dict() for t in all_tasks]  # Send to LLM
```

### Internationalization (Urdu/English)

**Current Design Enables**:
- Message constants in utils/messages.py
- Add language parameter to message functions

**Example Extension**:
```python
# Phase II/III
def get_message(key: str, lang: str = "en", **kwargs) -> str:
    messages = {
        "en": {"TASK_ADDED": "Task #{id} added: {title}"},
        "ur": {"TASK_ADDED": "ٹاسک #{id} شامل ہوا: {title}"}
    }
    return messages[lang][key].format(**kwargs)
```

---

## Research Sign-Off

All research questions resolved. No remaining NEEDS CLARIFICATION items. Architecture decisions documented with rationale, alternatives, and trade-offs. Ready to proceed to Phase 1: Data Model & Contracts.

**Reviewer**: Claude Sonnet 4.5
**Date**: 2025-12-26
**Status**: ✅ Complete
