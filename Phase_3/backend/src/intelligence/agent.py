"""OpenAI Agents SDK implementation for conversational todo management."""

import os
import sys

# Set OpenAI API key from environment BEFORE any other imports
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

# Removed hardcoded Windows site-packages path for Render deployment
# Install 'swarm' package via requirements.txt instead

from typing import Dict, Any, Optional
from pydantic import BaseModel

# Fallback implementation using OpenAI Assistants API
try:
    from openai import OpenAI
    import os

    # Mock the swarm classes to avoid import errors
    class MockAgent:
        def __init__(self, name=None, instructions=None, tools=None):
            self.name = name
            self.instructions = instructions
            self.tools = tools or []

    class MockSwarm:
        def run(self, agent, messages):
            # Placeholder implementation
            pass

    Agent = MockAgent
    Swarm = MockSwarm
    Runner = MockSwarm

    def function_tool(func):
        """Decorator to mark a function as a tool."""
        func.is_tool = True
        return func

except ImportError:
    # If openai is not available either, create basic mocks
    class MockAgent:
        def __init__(self, name=None, instructions=None, tools=None):
            self.name = name
            self.instructions = instructions
            self.tools = tools or []

    class MockSwarm:
        def run(self, agent, messages):
            # Placeholder implementation
            pass

    Agent = MockAgent
    Swarm = MockSwarm
    Runner = MockSwarm

    def function_tool(func):
        """Decorator to mark a function as a tool."""
        func.is_tool = True
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

You can help users manage their tasks through natural conversation. You understand English, Roman Urdu and Urdu.

## Your Capabilities:
1. **Add tasks** - use add_task tool
2. **Update tasks** - use update_task tool (accepts task name OR ID directly)
3. **Delete tasks** - use delete_task tool (accepts task name OR ID directly)
4. **List tasks** - use list_tasks tool

## IMPORTANT - Direct Task Operations:
- Pass task NAMES directly to delete_task and update_task - the system looks up the ID automatically
- Example: "delete buy milk" -> Call delete_task(task_id="buy milk")
- Example: "mark groceries done" -> Call update_task(task_id="groceries", new_status="completed")
- DO NOT call list_tasks first to get IDs - pass the task name directly!

## Priority Handling:
- HIGH: urgent, asap, important, critical, immediately
- MEDIUM: normal tasks (default)
- LOW: eventually, whenever, later, someday

## Guidelines:
- Respond in same language as user (English, Roman Urdu, or Urdu)
- Be concise and confirm actions clearly

Remember: For delete and update, pass the task name directly."""


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
    """Run the todo agent with user input using OpenAI function calling."""
    try:
        logger.info(f"Running agent with input: {user_input}")

        from openai import OpenAI
        import json
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

        # Define the tools/functions for OpenAI
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"},
                            "due_date": {"type": "string", "description": "Optional due date in ISO format"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks from the todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status_filter": {"type": "string", "enum": ["pending", "completed", "in-progress"], "description": "Filter tasks by status"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task. You can pass either the task ID (number) or task name/title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The task ID (number) OR task name/title. Example: '1' or 'buy milk'"},
                            "new_title": {"type": "string", "description": "New title for the task"},
                            "new_status": {"type": "string", "enum": ["pending", "completed", "in-progress"], "description": "New status for the task"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the todo list. You can pass either the task ID (number) or the task name/title directly.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The task ID (number) OR task name/title to delete. Example: '1' or 'buy milk'"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        # First API call with function calling
        messages = [
            {"role": "system", "content": AGENT_INSTRUCTIONS},
            {"role": "user", "content": user_input}
        ]

        # Force tool usage for task-related commands
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Better at function calling
            messages=messages,
            tools=tools,
            tool_choice="required",  # Force tool usage
            temperature=0.3  # Lower temperature for more consistent tool calls
        )

        response_message = response.choices[0].message
        print(f"DEBUG: OpenAI response - has tool_calls: {response_message.tool_calls is not None}, content: {response_message.content[:100] if response_message.content else 'None'}")
        logger.info(f"OpenAI response - has tool_calls: {response_message.tool_calls is not None}, content: {response_message.content[:100] if response_message.content else 'None'}")

        # Check if the model wants to call a function
        if response_message.tool_calls:
            print(f"DEBUG: Tool calls found: {len(response_message.tool_calls)}")
            # Process each tool call
            tool_results = []
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"DEBUG: Executing tool: {function_name} with args: {function_args}")
                logger.info(f"Executing tool: {function_name} with args: {function_args}")

                # Execute the appropriate function
                if function_name == "add_task":
                    result = TodoAgent.add_task(
                        title=function_args.get("title"),
                        description=function_args.get("description"),
                        due_date=function_args.get("due_date"),
                        priority=function_args.get("priority", "medium")
                    )
                elif function_name == "list_tasks":
                    result = TodoAgent.list_tasks(
                        status_filter=function_args.get("status_filter")
                    )
                elif function_name == "update_task":
                    result = TodoAgent.update_task(
                        task_id=function_args.get("task_id"),
                        new_title=function_args.get("new_title"),
                        new_status=function_args.get("new_status")
                    )
                elif function_name == "delete_task":
                    result = TodoAgent.delete_task(
                        task_id=function_args.get("task_id")
                    )
                else:
                    result = {"success": False, "message": f"Unknown function: {function_name}"}

                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "result": result
                })

                logger.info(f"Tool {function_name} result: {result}")

            # Return the result from the tool execution
            if tool_results:
                final_result = tool_results[0]["result"]
                return {
                    "success": final_result.success if hasattr(final_result, 'success') else True,
                    "message": final_result.message if hasattr(final_result, 'message') else str(final_result),
                    "data": final_result.model_dump() if hasattr(final_result, 'model_dump') else final_result
                }

        # If no function was called, return the text response
        return {
            "success": True,
            "message": response_message.content or "I'm here to help you manage your tasks. What would you like to do?",
            "raw_response": str(response)
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
    print(f"DEBUG run_agent_sync called with: {user_input}")

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
