# Tasks: Core CLI Todo Application

**Input**: Design documents from `/specs/001-core-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included in this phase as they were not explicitly requested in the specification. Manual acceptance testing will be performed instead.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, at repository root
- Paths assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project root structure (src/, specs/, tests/, history/)
- [ ] T002 [P] Create src/models/ directory with __init__.py
- [ ] T003 [P] Create src/services/ directory with __init__.py
- [ ] T004 [P] Create src/cli/ directory with __init__.py
- [ ] T005 [P] Create src/utils/ directory with __init__.py
- [ ] T006 [P] Create src/__init__.py for package initialization
- [ ] T007 [P] Create requirements.txt (empty, standard library only)
- [ ] T008 [P] Create .gitignore for Python (*.pyc, __pycache__/, .venv/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 [P] Create Task dataclass in src/models/task.py with fields (id: int, title: str, description: str = "", completed: bool = False)
- [ ] T010 [P] Add Task.to_dict() method in src/models/task.py for JSON serialization using dataclasses.asdict()
- [ ] T011 [P] Add Task.__str__() method in src/models/task.py for human-readable display
- [ ] T012 Create TaskService class skeleton in src/services/task_service.py with __init__ (tasks: List[Task] = [], next_id: int = 1)
- [ ] T013 [P] Create message constants in src/utils/messages.py (TASK_ADDED, TASK_NOT_FOUND, TITLE_REQUIRED, etc.)
- [ ] T014 Create CLI argument parser setup in src/cli/main.py with argparse subparsers structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks and view their todo list (basic note-taking system)

**Independent Test**: Add multiple tasks and verify they appear in list view with correct IDs, titles, and pending status

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement TaskService.add_task(title, description) method in src/services/task_service.py with validation and ID generation
- [ ] T016 [P] [US1] Implement TaskService.get_all_tasks() method in src/services/task_service.py returning List[Task]
- [ ] T017 [US1] Implement add command handler in src/cli/commands.py (handle_add function) with error handling
- [ ] T018 [US1] Implement list command handler in src/cli/commands.py (handle_list function) with formatted table output
- [ ] T019 [US1] Wire add subcommand in src/cli/main.py (parser.add_parser('add') with title positional, --description optional)
- [ ] T020 [US1] Wire list subcommand in src/cli/main.py (parser.add_parser('list'))
- [ ] T021 [US1] Add main() entry point in src/cli/main.py to parse args and dispatch to handlers

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

**Manual Test US1**:
- [ ] Add task with title only → verify ID 1, status pending, confirmation displayed
- [ ] Add 3 tasks → verify all 3 display with correct IDs in list
- [ ] Add task with title and description → verify both stored
- [ ] Add task without title → verify error "Title is required"

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to track progress by marking tasks complete/incomplete

**Independent Test**: Add tasks, mark some complete, verify status changes appear in list view

### Implementation for User Story 2

- [ ] T022 [P] [US2] Implement TaskService.get_task(task_id) method in src/services/task_service.py with error handling
- [ ] T023 [P] [US2] Implement TaskService.toggle_complete(task_id, completed) method in src/services/task_service.py
- [ ] T024 [US2] Implement complete command handler in src/cli/commands.py (handle_complete function)
- [ ] T025 [US2] Implement incomplete command handler in src/cli/commands.py (handle_incomplete function)
- [ ] T026 [US2] Wire complete subcommand in src/cli/main.py (parser.add_parser('complete') with id positional type=int)
- [ ] T027 [US2] Wire incomplete subcommand in src/cli/main.py (parser.add_parser('incomplete') with id positional type=int)
- [ ] T028 [US2] Update handle_list in src/cli/commands.py to display completed status distinctly (✓ completed vs pending)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

**Manual Test US2**:
- [ ] Mark pending task complete → verify status changes, confirmation displayed
- [ ] Mark completed task incomplete → verify toggle works
- [ ] Try completing non-existent ID → verify error "Task not found with ID X"
- [ ] View tasks → verify completed/pending distinguishable

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to modify task information when requirements change

**Independent Test**: Create task, update its title/description, verify changes reflected

### Implementation for User Story 3

- [ ] T029 [US3] Implement TaskService.update_task(task_id, title, description) method in src/services/task_service.py with optional params
- [ ] T030 [US3] Implement update command handler in src/cli/commands.py (handle_update function) with validation
- [ ] T031 [US3] Wire update subcommand in src/cli/main.py (parser.add_parser('update') with id positional, --title optional, --description optional)

**Checkpoint**: All three user stories (US1, US2, US3) should now be independently functional

**Manual Test US3**:
- [ ] Update task title → verify change reflected, confirmation displayed
- [ ] Update task description only → verify title unchanged
- [ ] Try updating non-existent ID → verify error
- [ ] View updated task → verify changes shown in list

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P4)

**Goal**: Enable users to remove tasks that are no longer relevant

**Independent Test**: Create tasks, delete specific ones, verify they no longer appear

### Implementation for User Story 4

- [ ] T032 [US4] Implement TaskService.delete_task(task_id) method in src/services/task_service.py returning bool
- [ ] T033 [US4] Implement delete command handler in src/cli/commands.py (handle_delete function)
- [ ] T034 [US4] Wire delete subcommand in src/cli/main.py (parser.add_parser('delete') with id positional type=int)
- [ ] T035 [US4] Update handle_list in src/cli/commands.py to handle empty list case (display "No tasks found")

**Checkpoint**: All user stories should now be independently functional

**Manual Test US4**:
- [ ] Delete task by ID → verify removal, confirmation displayed
- [ ] View after delete → verify task not shown
- [ ] Delete non-existent ID → verify error
- [ ] Delete all tasks → verify empty list message

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 [P] Add comprehensive docstrings to all TaskService methods in src/services/task_service.py
- [ ] T037 [P] Add comprehensive docstrings to all CLI command handlers in src/cli/commands.py
- [ ] T038 [P] Add type hints to all function signatures in src/ (use typing.List, typing.Optional)
- [ ] T039 Create README.md with project overview, installation, basic usage examples from quickstart.md
- [ ] T040 Create CLAUDE.md with development workflow, constitution reference, spec-driven process
- [ ] T041 Add --help text to all subcommands in src/cli/main.py (use help= parameter in add_parser)
- [ ] T042 Add global --help to main parser in src/cli/main.py with application description
- [ ] T043 Validate all error messages match spec requirements (clear, actionable, consistent format)
- [ ] T044 Validate all success messages match spec requirements (confirmation, clear feedback)
- [ ] T045 Run manual acceptance testing checklist for all user stories (16 scenarios + 7 edge cases)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires TaskService.get_task() (also built in US2, or can reuse from US1 if added early)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Requires handle_list empty case (task T035)

### Within Each User Story

- Models before services (T009-T011 complete before T012)
- Services before CLI handlers (T015-T016 before T017-T018 for US1)
- Handlers before argparse wiring (T017-T018 before T019-T020 for US1)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup (Phase 1)**: All tasks T002-T008 marked [P] can run in parallel
- **Foundational (Phase 2)**: Tasks T009-T011 (Task model) and T013 (messages) marked [P] can run in parallel
- **User Story 1**: Tasks T015-T016 (service methods) marked [P] can run in parallel
- **User Story 2**: Tasks T022-T023 (service methods) marked [P] can run in parallel
- **Polish (Phase 7)**: Tasks T036-T038 (docstrings, type hints) and T039-T040 (docs) marked [P] can run in parallel
- **Once Foundational phase completes, all user stories CAN start in parallel** (if team capacity allows)

---

## Parallel Example: User Story 1

```bash
# Launch service methods for User Story 1 together:
Task: "Implement TaskService.add_task(title, description) method in src/services/task_service.py"
Task: "Implement TaskService.get_all_tasks() method in src/services/task_service.py"

# These can run simultaneously as they create different methods in the same file
# or are truly independent operations
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add and View)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: A working CLI todo app where users can add tasks and view their list. This alone provides value as a basic note-taking system.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T015-T021)
   - Developer B: User Story 2 (T022-T028) - may need T022 coordination if get_task added in US2
   - Developer C: User Story 3 (T029-T031)
   - Developer D: User Story 4 (T032-T035)
3. Stories complete and integrate independently

---

## Manual Acceptance Testing Checklist

### User Story 1: Add and View Tasks

- [ ] **AS1.1**: Add task with title "Buy groceries" → Task #1 created, status pending, confirmation displayed
- [ ] **AS1.2**: Add 3 tasks → All 3 display with IDs 1, 2, 3 in list command
- [ ] **AS1.3**: Add task with title and description → Both stored and retrievable
- [ ] **AS1.4**: Add task without title (empty string) → Error "Title is required"

### User Story 2: Mark Tasks Complete

- [ ] **AS2.1**: Mark pending task ID 1 complete → Status changes to completed, confirmation displayed
- [ ] **AS2.2**: Mark completed task ID 2 incomplete → Status changes to pending (toggle works)
- [ ] **AS2.3**: Complete non-existent ID 99 → Error "Task not found with ID 99"
- [ ] **AS2.4**: View tasks → Completed and pending clearly distinguishable (✓ completed vs pending)

### User Story 3: Update Task Details

- [ ] **AS3.1**: Update task ID 1 title to "Buy groceries and medicine" → Title updated, confirmation displayed
- [ ] **AS3.2**: Update task ID 2 description only → Description updated, title unchanged
- [ ] **AS3.3**: Update non-existent ID 99 → Error "Task not found with ID 99"
- [ ] **AS3.4**: View updated task → Changes reflected in list command

### User Story 4: Delete Unwanted Tasks

- [ ] **AS4.1**: Delete task ID 2 → Task removed, confirmation displayed
- [ ] **AS4.2**: View after delete → Only tasks 1 and 3 shown (2 is gone)
- [ ] **AS4.3**: Delete non-existent ID 99 → Error "Task not found with ID 99"
- [ ] **AS4.4**: Delete all tasks → Empty list displays "No tasks found"

### Edge Cases

- [ ] **EC1**: Empty title (whitespace only) → Error "Title is required"
- [ ] **EC2**: Invalid task ID (negative or zero) → Error "Task not found with ID X"
- [ ] **EC3**: View tasks with empty list → Display "No tasks found"
- [ ] **EC4**: Very long title (>200 chars) → Accepted, may truncate in display
- [ ] **EC5**: Complete already completed task → Idempotent (no error, confirmation displayed)
- [ ] **EC6**: Incomplete already pending task → Idempotent (no error, confirmation displayed)
- [ ] **EC7**: High task count (100+ tasks) → System remains responsive, no performance degradation

---

## Task Execution Commands

### How to Execute Tasks

Each task is designed to be executed via Claude Code with spec-driven generation. For example:

```
Task T015: Implement TaskService.add_task(title, description) method
→ Claude generates code based on data-model.md and plan.md specifications
→ Code includes validation, ID generation, error handling per spec
→ Output: Working method in src/services/task_service.py
```

### Validation After Each Task

1. Run the CLI to test: `python -m src.cli.main --help`
2. Test the specific command: `python -m src.cli.main add "Test Task"`
3. Verify output matches specification contracts
4. Check error cases with invalid input
5. Confirm exit codes (0 for success, 1 for errors)

---

## Notes

- [P] tasks = different files or methods, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- No automated tests in Phase I (manual testing only) per spec and constitution
- Commit after each task or logical group (e.g., after completing a user story phase)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution compliance: All code generated via Claude Code, no manual coding

---

## Success Criteria Mapping

| Task Phase | Success Criteria Met |
|------------|---------------------|
| Phase 2 (Foundational) | SC-001, SC-009 (infrastructure for performance) |
| Phase 3 (US1) | SC-001 (add task in <5s), SC-002 (view formatted), SC-007 (feedback), SC-008 (intuitive) |
| Phase 4 (US2) | SC-003 (mark complete instantly), SC-007 (clear feedback) |
| Phase 5 (US3) | SC-004 (update reflected instantly), SC-007 (clear feedback) |
| Phase 6 (US4) | SC-005 (delete confirmed), SC-007 (clear feedback) |
| Phase 7 (Polish) | SC-006 (100+ tasks), SC-008 (intuitive), SC-009 (<1s response), SC-010 (clear errors) |

**All 10 Success Criteria** from spec.md are addressed across the task phases.

---

## Total Task Count: 45 Tasks

- **Phase 1 (Setup)**: 8 tasks
- **Phase 2 (Foundational)**: 6 tasks (CRITICAL BLOCKING)
- **Phase 3 (US1 - Add/View)**: 7 tasks (MVP)
- **Phase 4 (US2 - Complete)**: 7 tasks
- **Phase 5 (US3 - Update)**: 3 tasks
- **Phase 6 (US4 - Delete)**: 4 tasks
- **Phase 7 (Polish)**: 10 tasks

**Parallel Opportunities**: 16 tasks marked with [P] can run in parallel within their phases

**MVP Scope**: Phases 1-3 (21 tasks) deliver a working add/view todo app

**Estimated LOC**: ~500 total (task.py: 50, task_service.py: 150, commands.py: 200, main.py: 80, messages.py: 20)
