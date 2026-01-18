"""OpenAI Agents SDK implementation for conversational todo management."""

import os
import sys

# Set OpenAI API key from environment BEFORE any other imports
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

# Removed hardcoded Windows site-packages path for Render deployment
# Install 'swarm' package via requirements.txt instead

from typing import Dict, Any, Optional
from pydantic import BaseModel

# Import openai-agents package
from swarm import Agent, Swarm
Runner = Swarm  # Alias for compatibility

# Define function_tool as a decorator for Swarm-compatible functions
def function_tool(func):
    """Decorator to mark a function as a tool for the Swarm agent."""
    # In Swarm, functions can be used as tools directly
    func.is_swarm_tool = True
    return func

# Import local modules
from skills.todo_operations import (
    add_task as add_task_skill,
    update_task as update_task_skill,
    delete_task as delete_task_skill,
    list_tasks as list_tasks_skill,
)
from utils.logging_config import logger


class AddTaskResult(BaseModel):
    """Result of adding a task."""
    success: bool
    message: str
    title: str = ""


class UpdateTaskResult(BaseModel):
    """Result of updating a task."""
    success: bool
    message: str
    title: str = ""


class DeleteTaskResult(BaseModel):
    """Result of deleting a task."""
    success: bool
    message: str


from typing import List as TypingList

class ListTasksResult(BaseModel):
    """Result of listing tasks."""
    success: bool
    message: str
    task_count: int = 0
    tasks: TypingList[Dict[str, Any]] = []


class TodoAgent:
    """Todo agent using OpenAI Agents SDK."""

    @staticmethod
    @function_tool
    def add_task(title: str, description: Optional[str] = None, due_date: Optional[str] = None, priority: str = "medium") -> AddTaskResult:
        """Add a new task to the todo list."""
        logger.info(f"Agent calling add_task: {title}, priority: {priority}")
        try:
            result = add_task_skill(title=title, description=description, dueDate=due_date, priority=priority)
            return AddTaskResult(
                success=True,
                message=f"Added task: {title}",
                title=title
            )
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return AddTaskResult(
                success=False,
                message=f"Failed to add task: {str(e)}"
            )

    @staticmethod
    @function_tool
    def update_task(task_id: str, new_title: Optional[str] = None, new_status: Optional[str] = None) -> UpdateTaskResult:
        """Update an existing task by ID. If you don't know the ID, use list_tasks first to get task IDs."""
        logger.info(f"Agent calling update_task: {task_id}")
        try:
            # If task_id looks like a name (contains letters), try to find by name
            original_task = None

            if any(c.isalpha() for c in task_id):
                # List all tasks to find the one matching this name
                all_tasks = list_tasks_skill()
                for task in all_tasks:
                    if task_id.lower() in task.get('title', '').lower():
                        original_task = task
                        break

                if original_task:
                    task_id = original_task['id']
                    logger.info(f"Found task '{original_task['title']}' with ID: {task_id}")
                else:
                    return UpdateTaskResult(
                        success=False,
                        message=f"Could not find a task matching '{task_id}'. Please list tasks first to see available tasks and their IDs."
                    )

            updates = {}
            if new_title:
                updates["title"] = new_title
            if new_status:
                updates["status"] = new_status

            result = update_task_skill(id=task_id, updates=updates)
            task_title = original_task.get('title', task_id) if original_task else task_id
            return UpdateTaskResult(
                success=True,
                message=f"Updated task: {task_title}",
                title=result.get('title', task_title)
            )
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return UpdateTaskResult(
                success=False,
                message=f"Failed to update task: {str(e)}"
            )

    @staticmethod
    @function_tool
    def delete_task(task_id: str) -> DeleteTaskResult:
        """Delete a task from the todo list by ID. Can also accept task names."""
        logger.info(f"Agent calling delete_task: {task_id}")
        try:
            # Check if the task_id is likely a task name (contains non-numeric characters)
            is_name_lookup = not task_id.isdigit() and any(c.isalpha() for c in task_id)

            actual_task_id = task_id
            task_title = task_id  # Default to the input

            if is_name_lookup:
                # Need to find the actual ID by searching through all tasks
                try:
                    all_tasks = list_tasks_skill()

                    # Find the best matching task
                    matched_task = None
                    for task in all_tasks:
                        if task_id.lower() in task.get('title', '').lower():
                            matched_task = task
                            actual_task_id = task.get('id', '')
                            task_title = task.get('title', task_id)
                            break

                    if not matched_task:
                        return DeleteTaskResult(
                            success=False,
                            message=f"I couldn't find a task matching '{task_id}'. Please use 'show my tasks' to see available tasks."
                        )

                except Exception as list_error:
                    logger.error(f"Error listing tasks for name lookup: {list_error}")
                    return DeleteTaskResult(
                        success=False,
                        message=f"I need a numeric task ID to delete the task. Please use the 'show my tasks' command first to see task IDs."
                    )

            # Now delete using the actual ID
            success = delete_task_skill(id=actual_task_id)
            if success:
                return DeleteTaskResult(
                    success=True,
                    message=f"Deleted task: {task_title}"
                )
            else:
                return DeleteTaskResult(
                    success=False,
                    message=f"Failed to delete task '{task_title}' (ID: {actual_task_id}). The task might not exist."
                )
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return DeleteTaskResult(
                success=False,
                message=f"Failed to delete task: {str(e)}"
            )

    @staticmethod
    @function_tool
    def list_tasks(status_filter: Optional[str] = None) -> ListTasksResult:
        """List tasks from the todo list."""
        logger.info(f"Agent calling list_tasks: status={status_filter}")
        try:
            filters = {}
            if status_filter:
                filters["status"] = status_filter

            tasks = list_tasks_skill(filters=filters if filters else None)

            if not tasks:
                return ListTasksResult(
                    success=True,
                    message="No tasks found",
                    task_count=0,
                    tasks=[]
                )

            # Create a numbered list with actual titles for user reference
            task_list_parts = []
            for i, task in enumerate(tasks, 1):
                title = task.get("title", "Untitled")
                task_list_parts.append(f"{i}. {title}")

            task_list_str = "\n".join(task_list_parts)
            message = f"Here are your tasks:\n{task_list_str}\n\nLet me know if you want to add, update, or delete any task!"

            return ListTasksResult(
                success=True,
                message=message,
                task_count=len(tasks),
                tasks=tasks
            )
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return ListTasksResult(
                success=False,
                message=f"Failed to list tasks: {str(e)}",
                task_count=0,
                tasks=[]
            )


# Create the agent with instructions
AGENT_INSTRUCTIONS = """You are a helpful conversational todo management assistant.

You can help users manage their tasks through natural conversation. You understand both English and Urdu.

## Your Capabilities:
1. **Add tasks** - When user wants to create a new task, use the add_task tool
2. **Update tasks** - When user wants to modify a task (mark complete, change title, etc.), use the update_task tool
3. **Delete tasks** - When user wants to remove a task, use the delete_task tool (REQUIRES NUMERIC TASK ID)
4. **List tasks** - When user wants to see their tasks, use the list_tasks tool

## Critical Workflow for Deletions and Updates:
- If a user wants to delete or update a task by NAME, YOU MUST FIRST call list_tasks to get the numeric IDs
- THEN use the numeric ID to call delete_task or update_task
- DO NOT try to pass task names directly as IDs to delete_task or update_task
- For example: User says "delete buy milk" -> You call list_tasks -> See that "buy milk" has ID 5 -> Call delete_task with ID "5"

## Priority Handling:
- When adding a task, analyze the user's input to determine priority
- HIGH PRIORITY: Keywords like "urgent", "asap", "important", "critical", "immediately", "emergency", "right now", "today", "deadline", "crucial", "must do"
- MEDIUM PRIORITY: Normal tasks without priority indicators
- LOW PRIORITY: Keywords like "eventually", "whenever", "later", "someday", "maybe", "possibly"
- Set priority parameter as "high", "medium", or "low"
- Examples: "Buy milk ASAP" -> priority="high", "Buy milk" -> priority="medium", "Buy milk eventually" -> priority="low"

## Guidelines:
- Respond in the same language the user uses (English or Urdu)
- Be concise and friendly
- Confirm actions clearly (e.g., "Added task: buy milk")
- If a command is unclear, ask for clarification
- When listing tasks, show them with their numeric IDs
- If a tool fails, explain the error to the user clearly

## Example Responses:
- English: "Added task: buy milk"
- Urdu (when user speaks Urdu): "کام شامل کریں: دودھ خریدیں"

Remember: Use the tools to interact with the todo system. Always call the appropriate tool based on what the user wants to do, and follow the critical workflow for deletions and updates."""


def create_todo_agent() -> Agent:
    """Create and return the todo agent."""
    agent = Agent(
        name="Todo Management Agent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[
            TodoAgent.add_task,
            TodoAgent.update_task,
            TodoAgent.delete_task,
            TodoAgent.list_tasks,
        ],
    )
    return agent


async def run_agent(user_input: str) -> Dict[str, Any]:
    """Run the todo agent with user input."""
    agent = create_todo_agent()

    try:
        logger.info(f"Running agent with input: {user_input}")
        result = await Runner.run(agent, user_input)

        return {
            "success": True,
            "message": result.final_output,
            "raw_response": str(result)
        }
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        return {
            "success": False,
            "message": f"An error occurred: {str(e) if str(e) else type(e).__name__}"
        }


def run_agent_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper for run_agent that handles both sync and async contexts."""
    import asyncio

    try:
        # Try to get the current running loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create a new one
            loop = None

        if loop is not None:
            # We're in an async context (FastAPI), use create_task or run in thread
            import concurrent.futures
            import threading

            # Run the coroutine in a separate thread to avoid event loop conflicts
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(run_agent(user_input))
                finally:
                    new_loop.close()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = executor.submit(run_in_thread).result(timeout=30)
            return result
        else:
            # No running loop, safe to create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(run_agent(user_input))
                return result
            finally:
                loop.close()
    except Exception as e:
        logger.error(f"Sync agent error: {e}", exc_info=True)
        return {
            "success": False,
            "message": f"An error occurred: {str(e) if str(e) else type(e).__name__}"
        }


if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing Todo Agent...")

        # Test list tasks
        print("\n1. Listing tasks:")
        result = await run_agent("show my tasks")
        print(f"Response: {result}")

        # Test add task
        print("\n2. Adding task:")
        result = await run_agent("add buy milk to my list")
        print(f"Response: {result}")

    asyncio.run(test())
