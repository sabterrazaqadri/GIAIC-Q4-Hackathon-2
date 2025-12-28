# Quickstart Guide: Core CLI Todo Application

**Feature**: 001-core-todo-cli
**Date**: 2025-12-26
**Purpose**: Get users up and running with the CLI todo app in under 5 minutes

## Overview

The Core CLI Todo Application is a simple, in-memory task manager that runs entirely from your command line. Perfect for quick task tracking during development sessions or learning spec-driven development workflows.

**Key Features**:
- ✅ Add tasks with titles and descriptions
- ✅ View all tasks at a glance
- ✅ Mark tasks complete or incomplete
- ✅ Update task details
- ✅ Delete unwanted tasks
- ✅ Zero configuration required
- ✅ No external dependencies

**Note**: Data is stored in-memory only. Tasks are lost when the application exits.

---

## Prerequisites

- **Python 3.13+** installed on your system
- **Ubuntu/WSL** or any Linux-based environment (Windows/macOS also work)
- **Git** (for cloning the repository)

### Check Python Version

```bash
python --version
# Should show Python 3.13.0 or higher
```

If you need to install Python 3.13:
- Ubuntu/WSL: `sudo apt update && sudo apt install python3.13`
- macOS: `brew install python@3.13`
- Windows: Download from https://www.python.org/downloads/

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/evolution-of-todo.git
cd evolution-of-todo/Phase_1
```

### Step 2: Verify Structure

```bash
ls -la
# Should see: src/, specs/, README.md, CLAUDE.md
```

### Step 3: Test the Application

```bash
python -m src.cli.main --help
# Should display help text with available commands
```

**That's it!** No `pip install`, no virtual environment setup. The app uses only Python standard library.

---

## Basic Usage

### Add Your First Task

```bash
python -m src.cli.main add "Buy groceries"
```

**Output**:
```
Task #1 added: Buy groceries
```

### Add a Task with Description

```bash
python -m src.cli.main add "Write report" --description "Quarterly summary due Friday"
```

**Output**:
```
Task #2 added: Write report
```

### View All Tasks

```bash
python -m src.cli.main list
```

**Output**:
```
ID    Title                          Status
---------------------------------------------
1     Buy groceries                  pending
2     Write report                   pending
```

### Mark a Task Complete

```bash
python -m src.cli.main complete 1
```

**Output**:
```
Task #1 marked as completed.
```

### View Updated Status

```bash
python -m src.cli.main list
```

**Output**:
```
ID    Title                          Status
---------------------------------------------
1     Buy groceries                  ✓ completed
2     Write report                   pending
```

---

## Common Tasks

### Update a Task Title

```bash
python -m src.cli.main update 2 --title "Write annual report"
```

**Output**:
```
Task #2 updated.
```

### Update a Task Description

```bash
python -m src.cli.main update 2 --description "Annual summary due Monday"
```

**Output**:
```
Task #2 updated.
```

### Mark a Task Incomplete (Reopen)

```bash
python -m src.cli.main incomplete 1
```

**Output**:
```
Task #1 marked as pending.
```

### Delete a Task

```bash
python -m src.cli.main delete 1
```

**Output**:
```
Task #1 deleted.
```

---

## Example Workflow

Here's a typical 5-minute workflow:

```bash
# Start with empty list
$ python -m src.cli.main list
No tasks found.

# Add three tasks
$ python -m src.cli.main add "Review pull requests"
Task #1 added: Review pull requests

$ python -m src.cli.main add "Update documentation" --description "Add API examples"
Task #2 added: Update documentation

$ python -m src.cli.main add "Fix bug #42"
Task #3 added: Fix bug #42

# Check your task list
$ python -m src.cli.main list
ID    Title                          Status
---------------------------------------------
1     Review pull requests           pending
2     Update documentation           pending
3     Fix bug #42                    pending

# Complete first task
$ python -m src.cli.main complete 1
Task #1 marked as completed.

# Update task #3 with more details
$ python -m src.cli.main update 3 --title "Fix login bug #42" --description "Null pointer in auth"
Task #3 updated.

# Check progress
$ python -m src.cli.main list
ID    Title                          Status
---------------------------------------------
1     Review pull requests           ✓ completed
2     Update documentation           pending
3     Fix login bug #42              pending

# Complete another task
$ python -m src.cli.main complete 3
Task #3 marked as completed.

# Final status
$ python -m src.cli.main list
ID    Title                          Status
---------------------------------------------
1     Review pull requests           ✓ completed
2     Update documentation           pending
3     Fix login bug #42              ✓ completed
```

---

## Tips & Tricks

### Use Shell Aliases for Faster Access

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias todo="python -m src.cli.main"
```

Then reload your shell:
```bash
source ~/.bashrc
```

Now you can use shorter commands:
```bash
todo add "New task"
todo list
todo complete 1
```

### Quote Multi-Word Arguments

Always use quotes for titles/descriptions with spaces:

```bash
# ✅ Correct
todo add "Buy groceries and medicine"

# ❌ Wrong (will fail)
todo add Buy groceries and medicine
```

### Chain Commands with && for Workflows

```bash
# Add task and immediately view list
todo add "New task" && todo list

# Complete task and view updated list
todo complete 1 && todo list
```

### Create a Quick Session Snapshot

```bash
# Save current task list to a text file (manual)
todo list > tasks-$(date +%Y-%m-%d).txt

# Later review what you accomplished
cat tasks-2025-12-26.txt
```

---

## Troubleshooting

### "No module named src"

**Problem**: You're not in the correct directory.

**Solution**: Navigate to the `Phase_1` directory:
```bash
cd /path/to/evolution-of-todo/Phase_1
```

### "Task not found with ID X"

**Problem**: The task was deleted or never existed.

**Solution**: Run `todo list` to see current valid IDs.

### "Title is required"

**Problem**: You provided an empty title or forgot quotes.

**Solution**: Ensure title is non-empty and quoted:
```bash
# ✅ Correct
todo add "My Task"

# ❌ Wrong
todo add ""
```

### "Command not found: todo"

**Problem**: Shell alias not set up.

**Solution**: Use full command:
```bash
python -m src.cli.main add "Task"
```

Or set up alias as described in Tips & Tricks.

---

## Command Reference Summary

| Command | Purpose | Example |
|---------|---------|---------|
| `add <title> [--description <text>]` | Create new task | `todo add "Buy milk"` |
| `list` | View all tasks | `todo list` |
| `update <id> [--title] [--description]` | Modify task | `todo update 1 --title "New title"` |
| `delete <id>` | Remove task | `todo delete 1` |
| `complete <id>` | Mark as done | `todo complete 1` |
| `incomplete <id>` | Mark as pending | `todo incomplete 1` |
| `--help` | Show help | `todo --help` or `todo add --help` |

---

## Important Limitations (Phase I)

### No Persistence

**What it means**: Tasks exist only while the application is running.

**Impact**:
- Closing terminal = all tasks lost
- Restarting app = fresh empty list
- No save/load functionality

**Workaround**: Use `todo list > backup.txt` to manually save snapshots.

**Phase II**: Persistent storage (database or file-based) coming soon.

### Single User

**What it means**: No authentication or multi-user support.

**Impact**: Anyone with access to your terminal can see/modify tasks.

**Phase II**: User authentication and profiles coming soon.

### No Advanced Features

**Not Available in Phase I**:
- Task priorities
- Due dates
- Categories/tags
- Search/filter
- Sorting options
- Recurring tasks
- Undo/redo

**Phase II/III**: These features are planned for future releases.

---

## Next Steps

### Learn More

- Read the full specification: `specs/001-core-todo-cli/spec.md`
- Explore the architecture: `specs/001-core-todo-cli/plan.md`
- Understand the data model: `specs/001-core-todo-cli/data-model.md`
- Review CLI contracts: `specs/001-core-todo-cli/contracts/cli-commands.md`

### Contribute

This project follows **Spec-Driven Development** principles. To contribute:

1. Read `CLAUDE.md` for development guidelines
2. Check the constitution: `.specify/memory/constitution.md`
3. All code is generated from specifications (no manual coding)
4. Submit issues/PRs via GitHub

### Provide Feedback

Found a bug? Have a feature request?

- Open an issue: https://github.com/your-username/evolution-of-todo/issues
- Tag with `phase-i` label
- Include command output and expected vs. actual behavior

---

## Advanced Usage (Power Users)

### Integration with Other Tools

**Use with `watch` for Auto-Refresh**:
```bash
# Auto-refresh task list every 2 seconds
watch -n 2 python -m src.cli.main list
```

**Pipe to Other Commands**:
```bash
# Count pending tasks
todo list | grep pending | wc -l

# Search for specific task
todo list | grep "bug"
```

**Use in Scripts**:
```bash
#!/bin/bash
# Add multiple tasks from a file
while IFS= read -r line; do
    python -m src.cli.main add "$line"
done < tasks.txt
```

### Exit Code Checking in Scripts

```bash
#!/bin/bash
# Conditional execution based on success/failure
if python -m src.cli.main add "Test Task"; then
    echo "Task added successfully!"
else
    echo "Failed to add task" >&2
    exit 1
fi
```

---

## FAQ

**Q: Can I run multiple instances simultaneously?**
A: No. Each instance has its own in-memory storage. Tasks created in one terminal won't appear in another.

**Q: What happens if I accidentally delete a task?**
A: In Phase I, deletion is permanent (no undo). Be careful! Phase II may include undo functionality.

**Q: Can I export my tasks?**
A: Not in Phase I. You can manually copy the output of `todo list` to a text file. Phase II will add export/import.

**Q: Does it work on Windows?**
A: Yes, but designed for Ubuntu/WSL. Use PowerShell or WSL for best experience.

**Q: Can I change the task ID format?**
A: No. IDs are sequential integers starting from 1. This is by design for CLI usability.

**Q: Why are completed tasks not hidden?**
A: Phase I shows all tasks. Phase II will add filtering (`--status pending`, `--status completed`).

---

## Quickstart Checklist

Before you start using the app, verify:

- ✅ Python 3.13+ installed (`python --version`)
- ✅ Repository cloned and in `Phase_1` directory
- ✅ Help command works (`python -m src.cli.main --help`)
- ✅ Can add a task (`python -m src.cli.main add "Test"`)
- ✅ Can view tasks (`python -m src.cli.main list`)
- ✅ Understand data is in-memory only (lost on exit)

**You're ready to go! Start managing your tasks.**

---

## Support & Community

- **Documentation**: All docs in `specs/` directory
- **Issues**: GitHub issue tracker
- **Development**: Follow CLAUDE.md guidelines
- **Philosophy**: Read constitution in `.specify/memory/constitution.md`

**Happy task tracking!** 🎯
