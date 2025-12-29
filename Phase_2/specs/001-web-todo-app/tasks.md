# Tasks: Full-Stack Web Todo Application

**Input**: Design documents from `/specs/001-web-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/openapi.yaml, research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Backend Setup (Shared Infrastructure)

**Purpose**: Initialize FastAPI backend with project structure and dependencies

- [X] T001 Create backend directory structure per plan.md: `backend/src/{models,schemas,api,db}`
- [X] T002 Initialize Python project with `pyproject.toml` including: fastapi, uvicorn, sqlmodel, pydantic, psycopg2-binary, pytest
- [X] T003 [P] Create `backend/.env.example` with DATABASE_URL, API_HOST, API_PORT variables
- [X] T004 [P] Configure `backend/pyproject.toml` with tool settings for ruff (linting) and pytest

---

## Phase 2: Database & Models (Foundational)

**Purpose**: Set up SQLModel with Neon PostgreSQL and create Todo entity

**CRITICAL**: Must complete before any user story implementation

- [X] T005 Create `backend/src/db/__init__.py` with database connection module
- [X] T006 Create `backend/src/db/connection.py` with SQLModel engine setup for Neon PostgreSQL
- [X] T007 Create `backend/src/models/__init__.py` exporting all models
- [X] T008 Create `backend/src/models/todo.py` with Todo SQLModel entity (id, title, description, priority, is_complete, created_at, updated_at)
- [X] T009 Create `backend/src/schemas/__init__.py` exporting all Pydantic schemas
- [X] T010 Create `backend/src/schemas/todo.py` with TodoCreate, TodoUpdate, TodoResponse schemas
- [X] T011 Create `backend/src/schemas/message.py` with basic message response schema

**Checkpoint**: Database connection and Todo model ready for API implementation

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Users can create new todos and view the todo list

**Independent Test**: Add a todo through the UI, verify it appears in the list without page refresh

### Backend Implementation

- [X] T012 [P] [US1] Create `backend/src/api/__init__.py` with router module
- [X] T013 [P] [US1] Create `backend/src/api/dependencies.py` with get_db dependency
- [X] T014 [US1] Implement POST `/todos` endpoint in `backend/src/api/todos.py` (create todo with title, description, priority)
- [X] T015 [US1] Implement GET `/todos` endpoint in `backend/src/api/todos.py` (list all todos)
- [X] T016 [US1] Implement GET `/todos/{id}` endpoint in `backend/src/api/todos.py` (get single todo)
- [X] T017 [US1] Add validation error handling (400) and not found error handling (404)

### Frontend Setup

- [X] T018 Initialize Next.js 14 app in `frontend/` with TypeScript, Tailwind CSS, ESLint, App Router, src directory
- [X] T019 [P] [US1] Create `frontend/src/types/todo.ts` with TypeScript interfaces matching API schemas
- [X] T020 [P] [US1] Create `frontend/src/services/api.ts` with API client functions (fetchTodos, createTodo)
- [X] T021 [US1] Create `frontend/src/app/globals.css` with Tailwind directives
- [X] T022 [US1] Create `frontend/src/app/layout.tsx` with root layout including metadata
- [X] T023 [US1] Create `frontend/src/components/TodoForm.tsx` with form for creating todos (title, description, priority)
- [X] T024 [US1] Create `frontend/src/components/TodoList.tsx` to display todo items
- [X] T025 [US1] Create `frontend/src/app/page.tsx` main page integrating TodoForm and TodoList

**Checkpoint**: User Story 1 complete - todos can be created and viewed in browser

---

## Phase 4: User Story 2 - Update and Delete Todos (Priority: P1)

**Goal**: Users can modify existing todos and delete them with confirmation

**Independent Test**: Edit a todo's title/priority, delete a todo, verify changes persist after reload

### Backend Implementation

- [X] T026 [P] [US2] Implement PUT `/todos/{id}` endpoint in `backend/src/api/todos.py` (full update)
- [X] T027 [P] [US2] Implement PATCH `/todos/{id}` endpoint in `backend/src/api/todos.py` (partial update)
- [X] T028 [US2] Implement DELETE `/todos/{id}` endpoint in `backend/src/api/todos.py` (delete todo)

### Frontend Implementation

- [X] T029 [P] [US2] Add `updateTodo` and `deleteTodo` functions to `frontend/src/services/api.ts`
- [X] T030 [US2] Create `frontend/src/components/TodoItem.tsx` with edit and delete buttons
- [X] T031 [US2] Create `frontend/src/components/EditTodoForm.tsx` with inline edit capability
- [X] T032 [US2] Add delete confirmation dialog in `frontend/src/components/TodoItem.tsx`
- [X] T033 [US2] Update `frontend/src/components/TodoList.tsx` to render TodoItem components

**Checkpoint**: User Story 2 complete - todos can be edited and deleted

---

## Phase 5: User Story 3 - Mark Todos Complete (Priority: P1)

**Goal**: Users can toggle todo completion status

**Independent Test**: Mark todos complete/incomplete, verify visual distinction and status persistence

### Backend Implementation

- [X] T034 [P] [US3] Implement PATCH `/todos/{id}/complete` endpoint in `backend/src/api/todos.py`
- [X] T035 [P] [US3] Implement PATCH `/todos/{id}/incomplete` endpoint in `backend/src/api/todos.py`

### Frontend Implementation

- [X] T036 [P] [US3] Add `completeTodo` and `reopenTodo` functions to `frontend/src/services/api.ts`
- [X] T037 [US3] Add checkbox component to `frontend/src/components/TodoItem.tsx` for completion toggle
- [X] T038 [US3] Apply visual distinction in `frontend/src/components/TodoItem.tsx` (strikethrough, color change) for completed todos
- [X] T039 [US3] Update `frontend/src/app/page.tsx` to refresh todo list after status changes

**Checkpoint**: User Story 3 complete - todos can be marked complete/incomplete

---

## Phase 6: User Story 4 - Prioritize Todos (Priority: P2)

**Goal**: Users can assign and view priority levels for todos

**Independent Test**: Create todos with different priorities, verify visual indicators display correctly

### Frontend Implementation

- [X] T040 [P] [US4] Add priority display in `frontend/src/components/TodoItem.tsx` (color-coded badge for Low/Medium/High)
- [X] T041 [P] [US4] Add priority selector to `frontend/src/components/TodoForm.tsx`
- [X] T042 [US4] Add priority selector to `frontend/src/components/EditTodoForm.tsx`
- [X] T043 [US4] Apply priority-based styling in `frontend/src/components/TodoItem.tsx` (e.g., red=High, yellow=Medium, green=Low)

**Checkpoint**: User Story 4 complete - priority levels are visible and settable

---

## Phase 7: API Integration & Validation

**Purpose**: Verify frontend-backend integration and data persistence

- [X] T044 Add loading states to `frontend/src/components/TodoForm.tsx` during API calls
- [X] T045 Add loading states to `frontend/src/components/TodoList.tsx` during API calls
- [X] T046 Add error handling with toast notifications in `frontend/src/services/api.ts`
- [X] T047 [P] Create `frontend/.env.local` with NEXT_PUBLIC_API_URL configuration
- [X] T048 Test data persistence: Create todo, reload page, verify todo still exists (backend database persistence)
- [X] T049 Test CRUD end-to-end: Create, Read, Update, Delete all operations work via UI
- [X] T050 Verify Phase I logic: If migrating from console app, ensure todo operations are preserved

**Checkpoint**: Full stack integration validated, data persists across reloads

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [X] T051 [P] Add CORS middleware configuration in `backend/src/main.py` for frontend origin
- [X] T052 [P] Create `backend/src/main.py` with FastAPI app initialization and included routers
- [X] T053 Add favicon and basic metadata in `frontend/public/`
- [X] T054 Add responsive design to `frontend/src/components/TodoItem.tsx` for mobile view
- [X] T055 Run validation against quickstart.md: verify all setup steps work
- [X] T056 Verify project structure matches plan.md: backend/ and frontend/ directories exist

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Backend Setup | None | Phase 2 |
| Phase 2: Database & Models | Phase 1 | All User Stories |
| Phase 3: US1 (Create/View) | Phase 2 | US2, US3, US4 |
| Phase 4: US2 (Update/Delete) | Phase 2 | US4, Polish |
| Phase 5: US3 (Complete) | Phase 2 | Polish |
| Phase 6: US4 (Priority) | Phase 2 | Polish |
| Phase 7: Integration | Phases 3-6 | Phase 8 |
| Phase 8: Polish | Phases 3-7 | Complete |

### User Story Dependencies

- **US1 (Create/View)**: Starts after Phase 2 - No dependencies on other stories
- **US2 (Update/Delete)**: Starts after Phase 2 - Can run in parallel with US1, US3
- **US3 (Mark Complete)**: Starts after Phase 2 - Can run in parallel with US1, US2
- **US4 (Priority)**: Starts after Phase 2 - Can run in parallel with US1, US2, US3

### Parallel Opportunities

All tasks marked [P] within a phase can run in parallel. User stories can proceed in parallel after Phase 2.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Backend Setup
2. Complete Phase 2: Database & Models (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test creating and viewing todos
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Phase 1 + Phase 2 → Foundation ready
2. Add US1 → Test independently → Deploy (MVP!)
3. Add US2 → Test independently → Deploy
4. Add US3 → Test independently → Deploy
5. Add US4 → Test independently → Deploy
6. Add Integration + Polish → Final deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 1 + Phase 2 together
2. Once Foundation is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3 + US4
3. Stories complete and integrate independently

---

## Task Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 56 |
| Backend Tasks | 19 |
| Frontend Tasks | 25 |
| Validation Tasks | 12 |
| Parallelizable Tasks | 18 |
| User Story 1 Tasks | 14 |
| User Story 2 Tasks | 9 |
| User Story 3 Tasks | 6 |
| User Story 4 Tasks | 4 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies
