<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial creation)
- Added principles: 6 new principles from user input
- Added sections: Required Capabilities, Technology Constraints, Repository Requirements, Explicit Constraints, Success Criteria, Forward Compatibility
- Templates requiring review: ✅ plan-template.md (no changes needed - Constitution Check section is generic), ✅ spec-template.md (no changes needed), ✅ tasks-template.md (no changes needed), ✅ phr-template.prompt.md (no changes needed)
- No placeholders intentionally deferred
-->
# Evolution of Todo Constitution

## Core Principles

### I. Spec First, Code Never
All behavior MUST be defined in Markdown specs. No manual coding. Every feature MUST begin with a written specification that describes the expected behavior before any implementation begins. The spec serves as the source of truth for all development work.

### II. Agent as Decision Maker
An AI Agent interprets user intent and selects the correct tool. The agent is responsible for understanding natural language input and mapping it to the appropriate tool invocation. This separation allows the core logic to remain pure while the agent handles interpretation.

### III. Tools = Reusable Intelligence
Todo operations MUST be exposed as callable tools for future phases. Each operation (add, update, delete, list, mark complete/incomplete) MUST be implemented as an independent, reusable tool. Tools MUST have clear inputs, outputs, and error conditions documented in specs.

### IV. Separation of Concerns
Three distinct layers MUST be maintained:
1. Core task logic - pure business logic for todo operations
2. Agent reasoning - interpretation and tool selection
3. CLI interface - user interaction layer

Changes to one layer MUST NOT require modifications to another. This enables independent testing and future extension.

### V. Deterministic + Auditable
Agent actions MUST be traceable and predictable. Every agent decision MUST be logged with sufficient context to understand why a particular tool was selected. The system MUST provide mechanisms to audit the full chain from user input to action taken.

### VI. Spec-Driven Iteration
All changes MUST flow through the specification lifecycle: spec → plan → tasks → implementation. Manual code edits that bypass this flow are prohibited. The specification document MUST be updated when requirements change.

## Required Capabilities

Manage todos using natural language with the following operations:

- **Add task**: Create new tasks with optional metadata (due date, priority, description)
- **Update task**: Modify existing task attributes
- **Delete task**: Remove tasks from the system
- **List tasks**: Display tasks with filtering and sorting options
- **Mark complete/incomplete**: Toggle task status

**Dual Modes**:
1. **Manual CLI**: Direct commands for power users
2. **AI Assistant Mode**: Natural language interpretation for casual users

## Technology Constraints

- Python 3.13+
- Claude Code (agent framework)
- Spec-Kit Plus (specification tooling)
- In-memory storage only (no database)
- No UI - CLI only

## Repository Requirements

- CONSTITUTION.md - This governance document
- /specs/ - Versioned feature specifications
- /src/ - Generated code only (no manual edits)
- CLAUDE.md - Agent instructions
- README.md - Project documentation

## Explicit Constraints

- No manual code edits to source files under /src/
- No hard-coded AI logic (all routing via specs)
- No external storage systems
- No user interface beyond CLI

## Success Criteria

- AI agent correctly maps natural language to appropriate tool
- Tools are reusable across Phase III+
- Clean, spec-driven iteration history exists in history/prompts/
- All changes traceable from spec through implementation

## Forward Compatibility

This phase MUST seamlessly extend into:
- **Phase III (Chat UI)**: Existing tools exposed via chat interface
- **Phase IV (Kubernetes)**: Containerized deployment without tool changes
- **Phase V (Event-Driven AI)**: Event-based tool invocation

## Governance

The Constitution supersedes all other development practices. Amendments MUST be documented with:
1. Clear description of changes
2. Rationale for each change
3. Migration plan for existing specifications
4. Version increment following semantic versioning rules

**Compliance**: All pull requests and reviews MUST verify alignment with constitution principles. Complex deviations MUST be justified in writing and approved before implementation.

**Reference**: Runtime development guidance available in CLAUDE.md and command files under .claude/commands/

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
