<!--
Sync Impact Report:
- Version change: Initial version → 1.0.0
- New Constitution created for Evolution of Todo - Phase I
- Principles established:
  1. Spec-Driven Development (No Manual Coding)
  2. Reusability & AI-Ready Design
  3. Clean Code & Modular Structure
  4. Test-First Development
  5. Traceability & Documentation
- Templates requiring updates:
  ✅ spec-template.md - Aligned with prioritization and traceability requirements
  ✅ plan-template.md - Aligned with constitution check and modular structure
  ✅ tasks-template.md - Aligned with test-first and independent task execution
  ✅ phr-template.prompt.md - Ready for traceability recording
- Follow-up TODOs: None - all placeholders filled
-->

# Evolution of Todo - Phase I Constitution

## Core Principles

### I. Spec-Driven Development (No Manual Coding)

**Non-Negotiable Rules:**

- ALL code MUST be generated through specification refinement and Claude Code execution
- NO manual coding permitted; developers act as architects defining clear specifications
- Every feature MUST begin with a specification document before any code generation
- Specifications MUST be refined through clarifying questions until unambiguous
- Code changes MUST be traced back to specification updates

**Rationale:** Ensures consistency, reproducibility, and establishes patterns for AI-driven development workflows in future phases. Manual coding introduces variance that undermines the evolution path to full AI automation.

### II. Reusability & AI-Ready Design

**Non-Negotiable Rules:**

- All business logic MUST be encapsulated in reusable service modules
- Public interfaces (functions, classes) MUST be designed for future AI agent consumption
- Agent Skills / Subagents hooks MUST be planned (even if not implemented in Phase I)
- Serialization functions MUST be extracted as reusable utilities
- Core domain logic MUST be separated from CLI presentation layer

**Rationale:** Phase I lays foundation for Phase II (full-stack) and Phase III (AI agents). Retrofitting reusability is expensive; designing for it from inception enables smooth evolution.

### III. Clean Code & Modular Structure

**Non-Negotiable Rules:**

- Python 3.13+ MUST be used as the implementation language
- Project structure MUST follow this layout:
  ```
  /src            # All production code
  /specs          # All specification files
  /tests          # All test files (when testing added)
  README.md       # User-facing documentation
  CLAUDE.md       # Development instructions for Claude Code
  ```
- Source code MUST be organized by concern:
  ```
  src/
  ├── models/      # Data structures and entities
  ├── services/    # Business logic
  ├── cli/         # Command-line interface
  └── utils/       # Shared utilities
  ```
- Each module MUST have a single, clear responsibility
- Function names MUST be descriptive and follow PEP 8 conventions
- No God objects or mega-files (max 300 lines per file guideline)

**Rationale:** Maintainability and extensibility require clear boundaries. Modular structure enables parallel development and easier testing in future phases.

### IV. Test-First Development

**Non-Negotiable Rules:**

- Tests MAY be added when explicitly required (Phase I focuses on core functionality)
- When tests are added, TDD cycle MUST be followed: Write test → See it fail → Implement → See it pass
- Test files MUST mirror source structure: `tests/unit/services/test_task_service.py` for `src/services/task_service.py`
- Tests MUST be executable and pass before code is considered complete
- Contract tests MUST be added when integrating with external systems (future phases)

**Rationale:** While Phase I is CLI-focused, establishing test-first discipline now prevents technical debt and enables confident refactoring as the system evolves.

### V. Traceability & Documentation

**Non-Negotiable Rules:**

- Every feature MUST have a corresponding spec file in `/specs/<feature-name>/spec.md`
- Every implementation MUST have a plan file in `/specs/<feature-name>/plan.md`
- Every implementation MUST have a tasks file in `/specs/<feature-name>/tasks.md`
- All user inputs and significant decisions MUST be recorded as Prompt History Records (PHRs)
- README.md MUST be kept current with feature additions
- CLAUDE.md MUST document all development workflows and conventions

**Rationale:** Traceability enables understanding why decisions were made, supports knowledge transfer, and creates a learning corpus for future AI agent training.

## Development Workflow

### Specification Process

1. **Feature Request**: User describes desired functionality
2. **Specification Creation**: Generate spec.md with user stories, requirements, success criteria
3. **Specification Review**: Clarify ambiguities with targeted questions
4. **Planning**: Create plan.md with technical approach and architecture decisions
5. **Task Breakdown**: Generate tasks.md with atomic, testable implementation steps
6. **Implementation**: Execute tasks via Claude Code (code generation only)
7. **Validation**: Verify implementation meets specification requirements
8. **Documentation**: Update README and create Prompt History Record

### Constitution Compliance Gates

All features MUST pass these checks before implementation:

- ✅ Specification exists and is unambiguous
- ✅ Plan defines clear module boundaries (models/services/cli/utils)
- ✅ Tasks are atomic and independently executable
- ✅ No manual coding steps in task list
- ✅ Reusable components identified and extracted
- ✅ Agent interface hooks documented (for future AI integration)

### Complexity Management

If a feature requires violating any principle:

1. Document the violation in plan.md Complexity Tracking section
2. Explain why the violation is necessary
3. Describe what simpler alternatives were rejected and why
4. Get explicit approval before proceeding

## Technology Standards

### Required Technologies

- **Language**: Python 3.13+
- **Package Management**: pip with requirements.txt
- **Code Style**: PEP 8 (enforced via formatter)
- **CLI Framework**: argparse (standard library) or click if needed

### Forbidden in Phase I

- Persistent storage (databases, files) - memory-only implementation
- Web frameworks (deferred to Phase II)
- External AI service integrations (deferred to Phase III)
- Manual code edits outside of specification-driven generation

### Future-Ready Considerations

While not implemented in Phase I, design MUST accommodate:

- Multi-language support (Urdu + English) - use message constants
- API serialization - use dataclasses with to_dict() methods
- Agent Skills interface - design public service methods clearly
- State persistence - separate domain logic from memory storage

## Constraints & Boundaries

### In Scope for Phase I

- Add task functionality
- Delete task functionality
- Update task functionality
- View tasks functionality (list all, filter by status)
- Mark task complete/incomplete functionality
- In-memory storage only
- Command-line interface only

### Out of Scope for Phase I

- Persistent storage (files, databases)
- Web interface or API
- Authentication or multi-user support
- Task priorities, due dates, categories (unless spec'd later)
- AI agent integration (prepared for, not implemented)

### External Dependencies

- Python 3.13+ runtime (owned by: user's environment)
- Standard library only (no external packages unless justified in plan)
- Claude Code for code generation (owned by: Anthropic)
- Spec-Kit Plus templates (owned by: project .specify/ directory)

## Governance

### Amendment Process

1. Propose amendment with clear rationale in GitHub issue or spec
2. Document impact on existing features and templates
3. Update constitution.md with version bump (semantic versioning)
4. Update all dependent templates (spec, plan, tasks, phr)
5. Create Prompt History Record documenting the change
6. Commit with message: `docs: amend constitution to vX.Y.Z (brief description)`

### Version Semantics

- **MAJOR** (X.0.0): Backward incompatible principle changes (e.g., removing no-manual-coding rule)
- **MINOR** (0.X.0): New principles added or existing principles significantly expanded
- **PATCH** (0.0.X): Clarifications, wording improvements, typo fixes

### Compliance Verification

- All PRs/reviews MUST verify constitution compliance via gates listed above
- Constitution supersedes all other practices and documentation
- Violations MUST be documented and justified in Complexity Tracking section
- Review checklist MUST include: "Does this change require constitution amendment?"

### Current Status

**Version**: 1.0.0
**Ratified**: 2025-12-26
**Last Amended**: 2025-12-26

---

**Success Criteria for Phase I Completion:**

- ✅ CLI app runs and performs all 5 core operations (Add/Delete/Update/View/Mark Complete)
- ✅ All spec files exist and are traceable to implementation
- ✅ Project structure is clean and modular (src/models, src/services, src/cli, src/utils)
- ✅ No manual code edits - all code generated from specifications
- ✅ Agent interface hooks documented for Phase III AI integration
- ✅ README and CLAUDE.md are complete and current
- ✅ Codebase is ready for extension to persistent storage and full-stack (Phase II)
