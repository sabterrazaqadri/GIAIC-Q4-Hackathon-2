# Implementation Plan: Core CLI Todo Application

**Branch**: `001-core-todo-cli` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-core-todo-cli/spec.md`

## Summary

Build an in-memory Python CLI todo application with 5 core operations (add, view, update, delete, mark complete/incomplete). The application uses a modular architecture with clean separation between models, services, and CLI layers. All business logic is exposed through reusable service functions to enable future AI agent integration in Phase III. Task data is stored in-memory using Python lists, with sequential numeric IDs for CLI usability. The implementation prioritizes simplicity, extensibility, and adherence to spec-driven development principles.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (standard library for CLI parsing), dataclasses (standard library for Task model)
**Storage**: In-memory Python list (no persistence)
**Testing**: Manual CLI testing in Phase I (pytest deferred to when tests explicitly requested)
**Target Platform**: Ubuntu/WSL Linux-based systems (cross-platform Python)
**Project Type**: Single CLI application
**Performance Goals**: Sub-second response time for all operations, handle 100+ tasks without degradation
**Constraints**: In-memory only, no external dependencies, CLI-only interface, single-user
**Scale/Scope**: Expected 10-100 tasks per session, support up to 1000+ tasks, single CLI application ~500 LOC

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (No Manual Coding)

- ✅ **PASS**: Specification complete and validated (specs/001-core-todo-cli/spec.md)
- ✅ **PASS**: All code will be generated through Claude Code from specifications
- ✅ **PASS**: Implementation plan being created before any code generation
- ✅ **PASS**: Tasks will be defined and reviewed before implementation

### Principle II: Reusability & AI-Ready Design

- ✅ **PASS**: Business logic encapsulated in src/services/task_service.py
- ✅ **PASS**: Service functions designed with clear interfaces (add_task, get_tasks, update_task, delete_task, toggle_complete)
- ✅ **PASS**: Task model uses dataclass for easy serialization (to_dict() method)
- ✅ **PASS**: Agent Skills hooks planned: service layer functions are the future AI agent interface
- ✅ **PASS**: Domain logic separated from CLI presentation (services vs cli)

### Principle III: Clean Code & Modular Structure

- ✅ **PASS**: Python 3.13+ specified
- ✅ **PASS**: Project structure follows constitution:
  ```
  /src (production code)
  /specs (specifications)
  /tests (when testing added)
  README.md, CLAUDE.md
  ```
- ✅ **PASS**: Source organized by concern:
  ```
  src/models/task.py      # Task dataclass
  src/services/task_service.py  # Business logic
  src/cli/commands.py     # CLI commands
  src/cli/main.py         # CLI entry point
  src/utils/messages.py   # Message constants (i18n ready)
  ```
- ✅ **PASS**: Single responsibility per module
- ✅ **PASS**: PEP 8 naming conventions (generated code will follow)
- ✅ **PASS**: No files expected to exceed 300 lines (task_service.py ~150 LOC, commands.py ~200 LOC)

### Principle IV: Test-First Development

- ✅ **PASS**: Tests not required in Phase I per constitution ("MAY be added when explicitly required")
- ✅ **PASS**: Manual acceptance testing planned against user story scenarios
- ✅ **PASS**: Test structure prepared for future: tests/unit/services/, tests/integration/

### Principle V: Traceability & Documentation

- ✅ **PASS**: Spec file exists: specs/001-core-todo-cli/spec.md
- ✅ **PASS**: Plan file being created: specs/001-core-todo-cli/plan.md
- ✅ **PASS**: Tasks file will be created: specs/001-core-todo-cli/tasks.md
- ✅ **PASS**: PHRs being recorded in history/prompts/001-core-todo-cli/
- ✅ **PASS**: README.md and CLAUDE.md will be updated with feature documentation

**Constitution Check Result**: ✅ **ALL GATES PASS** - Ready to proceed with Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-core-todo-cli/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 research decisions (to be created)
├── data-model.md        # Phase 1 task entity model (to be created)
├── quickstart.md        # Phase 1 user quickstart guide (to be created)
├── contracts/           # Phase 1 CLI command contracts (to be created)
│   └── cli-commands.md  # CLI command interface definitions
├── checklists/
│   └── requirements.md  # Specification quality checklist (complete)
└── tasks.md             # Phase 2 implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py              # Task dataclass: id, title, description, completed
├── services/
│   ├── __init__.py
│   └── task_service.py      # TaskService class with CRUD operations + toggle
├── cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point, argument parser setup
│   └── commands.py          # Command implementations (add, view, update, delete, complete, incomplete)
└── utils/
    ├── __init__.py
    └── messages.py          # Message constants for i18n readiness

tests/                       # Created when tests requested
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── test_task_service.py
└── integration/
    ├── __init__.py
    └── test_cli_flow.py

# Root files
requirements.txt             # Empty or minimal (standard library only)
README.md                    # User documentation and quickstart
CLAUDE.md                    # Development instructions
.gitignore                   # Python standard gitignore
```

**Structure Decision**: Selected **Option 1: Single project** structure. This is a standalone CLI application with no frontend/backend split or mobile components. The single project structure aligns with constitution requirements and provides clear separation of concerns through the src/models, src/services, src/cli, src/utils organization. Tests directory prepared but empty in Phase I (will be populated when tests are explicitly requested).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied:
- Spec-driven: Complete spec with all clarifications resolved
- Reusability: Service layer designed for AI agent consumption
- Modular: Clean src/ structure with single responsibilities
- Test-ready: Structure prepared, manual testing sufficient for Phase I
- Traceable: Full spec/plan/PHR documentation

## Phase 0: Research & Decision Documentation

### Research Tasks

Based on Technical Context unknowns and architectural decisions, the following research will be conducted:

1. **CLI Argument Parsing**: Best practices for Python argparse subcommands
2. **In-Memory Storage Pattern**: Optimal data structure for task storage and ID generation
3. **ID Management Strategy**: Auto-increment counter vs. list index-based IDs
4. **Error Handling Pattern**: Exception-based vs. result-object pattern for service layer
5. **Message Formatting**: CLI output formatting best practices for tables and lists
6. **Dataclass Serialization**: to_dict() implementation patterns for future JSON API

### Decisions to Document

Each decision will be documented in research.md with:
- **Decision**: What was chosen
- **Rationale**: Why it was chosen
- **Alternatives Considered**: What else was evaluated
- **Trade-offs**: Pros/cons of the chosen approach
- **Future Impact**: How this affects Phase II/III evolution

Initial decision summary (to be expanded in research.md):

1. **In-memory vs Database**: In-memory for simplicity (Phase I constraint)
2. **Numeric IDs vs UUIDs**: Sequential integers for CLI usability and human readability
3. **Function-based vs Class-based service**: Class-based for state encapsulation and AI agent reuse
4. **argparse vs click**: argparse (standard library, zero dependencies)
5. **Dataclass vs dict**: Dataclass for type safety and extensibility
6. **List vs dict storage**: List with linear search (simple, adequate for <1000 tasks)

## Phase 1: Data Model & Contracts

### Data Model (data-model.md)

**Task Entity**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False

    # Extensibility: Reserved for Phase II/III
    # priority: Optional[int] = None
    # due_date: Optional[datetime] = None
    # recurrence: Optional[str] = None
    # tags: List[str] = field(default_factory=list)
```

**TaskService State**:
- `tasks: List[Task]` - In-memory task storage
- `next_id: int` - Auto-increment counter starting at 1

### CLI Contracts (contracts/cli-commands.md)

**Command Interface**:

```bash
# Add task
python -m src.cli.main add "Title" [--description "Description"]
→ Output: "Task #1 added: Title"

# View all tasks
python -m src.cli.main list
→ Output: Table with ID | Title | Status columns

# Update task
python -m src.cli.main update 1 [--title "New Title"] [--description "New Desc"]
→ Output: "Task #1 updated"

# Delete task
python -m src.cli.main delete 1
→ Output: "Task #1 deleted"

# Mark complete
python -m src.cli.main complete 1
→ Output: "Task #1 marked as complete"

# Mark incomplete
python -m src.cli.main incomplete 1
→ Output: "Task #1 marked as incomplete"

# Help
python -m src.cli.main --help
python -m src.cli.main <command> --help
```

**Error Responses**:
- Invalid ID: "Error: Task not found with ID {id}"
- Missing title: "Error: Title is required"
- Invalid command: argparse auto-generates usage message

### Quickstart (quickstart.md)

**Installation**:
```bash
git clone <repo>
cd Phase_1
# No pip install needed (standard library only)
```

**Usage Examples**:
```bash
# Add tasks
python -m src.cli.main add "Buy groceries"
python -m src.cli.main add "Write report" --description "Quarterly summary"

# View tasks
python -m src.cli.main list

# Mark complete
python -m src.cli.main complete 1

# Update task
python -m src.cli.main update 2 --title "Write annual report"

# Delete task
python -m src.cli.main delete 1
```

## Phase 2: Implementation Strategy

### Build Order (Priority-Based)

Following user story priorities from spec.md:

**Phase 2.1: Foundation** (Shared Infrastructure)
- Task model (dataclass)
- TaskService skeleton with storage
- CLI main.py with argparse setup
- Message constants

**Phase 2.2: P1 - Add and View** (MVP)
- TaskService.add_task()
- TaskService.get_all_tasks()
- CLI add command
- CLI list command
- ID generation logic

**Phase 2.3: P2 - Mark Complete** (Progress Tracking)
- TaskService.toggle_complete()
- CLI complete command
- CLI incomplete command
- Status display in list

**Phase 2.4: P3 - Update** (Maintenance)
- TaskService.update_task()
- CLI update command
- Validation for optional fields

**Phase 2.5: P4 - Delete** (Cleanup)
- TaskService.delete_task()
- CLI delete command
- Empty list handling

### Module Dependencies

```
models/task.py  →  (no dependencies)
    ↓
services/task_service.py  →  (depends on: models/task.py)
    ↓
cli/commands.py  →  (depends on: services/task_service.py, utils/messages.py)
    ↓
cli/main.py  →  (depends on: cli/commands.py)
```

**Parallel Opportunities**:
- models/task.py and utils/messages.py can be built in parallel
- After TaskService is complete, all CLI commands can be built in parallel
- Documentation (README, CLAUDE.md) can be written in parallel with final testing

### Validation Strategy

**Manual Testing Checklist** (per acceptance scenarios in spec.md):

**User Story 1 - Add and View**:
- [ ] Add task with title only → verify ID 1, status "pending"
- [ ] Add 3 tasks → verify all 3 display with correct IDs
- [ ] Add task with title and description → verify both stored
- [ ] Add task without title → verify error message

**User Story 2 - Mark Complete**:
- [ ] Mark pending task complete → verify status changes
- [ ] Mark completed task incomplete → verify toggle works
- [ ] Try completing non-existent ID → verify error
- [ ] View tasks → verify completed/pending distinguishable

**User Story 3 - Update**:
- [ ] Update task title → verify change reflected
- [ ] Update task description only → verify title unchanged
- [ ] Update non-existent ID → verify error
- [ ] View updated task → verify changes shown

**User Story 4 - Delete**:
- [ ] Delete task by ID → verify removal and confirmation
- [ ] View after delete → verify task not shown
- [ ] Delete non-existent ID → verify error
- [ ] Delete all tasks → verify empty list message

**Edge Cases**:
- [ ] Empty title → error
- [ ] Invalid ID → error
- [ ] Empty list view → appropriate message
- [ ] Long title (>200 chars) → accepts and displays
- [ ] Complete already completed → idempotent or info message
- [ ] Negative/zero ID → error
- [ ] High task count (100+) → no performance issues

### Architecture Decisions

**Key Decision 1: In-Memory Storage with List**

**Decision**: Use Python list for task storage with linear search by ID

**Rationale**:
- Simplicity: List operations (append, remove, iterate) are straightforward
- Performance: Linear search adequate for expected scale (10-100 tasks, max 1000)
- Phase I constraint: No persistence required
- Easy migration: Can swap to dict or database in Phase II without API changes

**Alternatives Considered**:
- Dict with ID keys: Faster lookups (O(1) vs O(n)) but unnecessary for small scale
- SQLite in-memory: Overkill for simple CRUD, adds complexity

**Trade-offs**:
- Pro: Simple, readable code
- Pro: No external dependencies
- Con: O(n) search performance (acceptable for scale)
- Con: IDs must be managed manually (counter variable)

**Future Impact**: Service layer interface remains stable; Phase II can replace list with database without CLI changes

---

**Key Decision 2: Sequential Numeric IDs**

**Decision**: Use auto-incrementing integer IDs starting from 1

**Rationale**:
- CLI usability: Short, memorable IDs (1, 2, 3 vs UUIDs)
- Human-readable: Users can easily reference tasks ("complete 1")
- Simple implementation: Single counter variable
- Phase I scope: Single-user, no distributed ID concerns

**Alternatives Considered**:
- UUIDs: Globally unique but verbose for CLI (e.g., "complete 3f8e9d2a-...")
- List indices: Simple but breaks when items deleted (IDs change)

**Trade-offs**:
- Pro: Excellent CLI UX
- Pro: Simple counter logic
- Con: IDs not reused after delete (acceptable, expected behavior)
- Con: Won't scale to distributed systems (not needed in Phase I)

**Future Impact**: Phase II/III may need UUIDs for API; can be added as additional field while keeping numeric IDs for CLI

---

**Key Decision 3: Class-Based Service Layer**

**Decision**: Implement TaskService as a class with instance state

**Rationale**:
- State encapsulation: tasks list and next_id counter are instance variables
- AI agent reuse: Agents can instantiate TaskService and call methods
- Testability: Easy to mock and test with different initial states
- OOP patterns: Aligns with Python best practices for stateful components

**Alternatives Considered**:
- Module-level functions with global state: Simpler but harder to test and reuse
- Functional approach with state passing: Pure but verbose for this use case

**Trade-offs**:
- Pro: Clean interface for future AI agents
- Pro: Instance state makes testing easier
- Pro: Can create multiple TaskService instances (e.g., for testing)
- Con: Slightly more code than global functions (acceptable)

**Future Impact**: Class-based design enables dependency injection in Phase II (e.g., inject database instead of list)

---

**Key Decision 4: argparse for CLI Parsing**

**Decision**: Use argparse (standard library) with subcommands

**Rationale**:
- Zero dependencies: Standard library only (constitution preference)
- Rich features: Subcommands, help generation, type validation
- Widely known: Standard Python CLI tool
- Ubuntu/WSL compatible: No installation needed

**Alternatives Considered**:
- click: More modern, easier subcommands, but external dependency
- sys.argv parsing: Too low-level, reinventing the wheel
- typer: Modern but requires external dependency

**Trade-offs**:
- Pro: Zero dependencies
- Pro: Auto-generated help messages
- Pro: Type coercion and validation
- Con: More verbose than click (acceptable trade-off)

**Future Impact**: Stable CLI interface; Phase II API can coexist without changes

---

**Key Decision 5: Dataclass for Task Model**

**Decision**: Use @dataclass decorator for Task entity

**Rationale**:
- Type safety: Field types enforced by Python type hints
- Extensibility: Easy to add fields in Phase II (priority, due_date, etc.)
- Serialization: Simple to_dict() method for future JSON API
- Readable: Clean syntax, auto-generated __init__, __repr__

**Alternatives Considered**:
- dict: Flexible but no type safety, harder to extend
- NamedTuple: Immutable but we need mutation for updates
- Pydantic: Rich validation but external dependency

**Trade-offs**:
- Pro: Type safety and IDE support
- Pro: Extensible (add fields without breaking old code)
- Pro: to_dict() enables future API serialization
- Con: Requires Python 3.7+ (satisfied by 3.13+ requirement)

**Future Impact**: Dataclass fields become API response schema in Phase II; easy to serialize to JSON

## Re-Evaluation: Constitution Check (Post-Design)

*Re-check compliance after Phase 1 design decisions*

### Principle I: Spec-Driven Development
- ✅ **PASS**: Plan created from spec, no manual coding yet
- ✅ **PASS**: All architectural decisions traced to spec requirements

### Principle II: Reusability & AI-Ready Design
- ✅ **PASS**: TaskService methods are the AI agent interface:
  - `add_task(title, description) → Task`
  - `get_all_tasks() → List[Task]`
  - `get_task(id) → Optional[Task]`
  - `update_task(id, title, description) → Task`
  - `delete_task(id) → bool`
  - `toggle_complete(id, completed) → Task`
- ✅ **PASS**: Task.to_dict() enables future JSON serialization
- ✅ **PASS**: Message constants in utils/messages.py enable i18n

### Principle III: Clean Code & Modular Structure
- ✅ **PASS**: Structure refined to exact file paths
- ✅ **PASS**: Each file has single responsibility
- ✅ **PASS**: No files expected >300 LOC

### Principle IV: Test-First Development
- ✅ **PASS**: Manual testing checklist covers all acceptance scenarios
- ✅ **PASS**: Test structure prepared for future automated tests

### Principle V: Traceability & Documentation
- ✅ **PASS**: Plan documents all decisions with rationale
- ✅ **PASS**: Research, data-model, contracts, quickstart will be created

**Final Constitution Check**: ✅ **ALL GATES PASS** - Ready to proceed to /sp.tasks

## Next Steps

1. **Create remaining Phase 1 artifacts**:
   - Generate research.md with detailed decision documentation
   - Generate data-model.md with Task entity specification
   - Generate contracts/cli-commands.md with command interface details
   - Generate quickstart.md with user guide

2. **Update agent context**:
   - Run .specify/scripts/powershell/update-agent-context.ps1
   - Add Python 3.13, argparse, dataclass to technology context

3. **Generate tasks.md**:
   - Run `/sp.tasks` to break down implementation into atomic tasks
   - Tasks will follow priority order: Foundation → P1 → P2 → P3 → P4

4. **Begin implementation**:
   - Execute tasks via Claude Code (spec-driven generation)
   - Validate against manual testing checklist
   - Update README and CLAUDE.md

5. **Create PHR**:
   - Document planning session in history/prompts/001-core-todo-cli/
   - Record all architectural decisions and rationale
