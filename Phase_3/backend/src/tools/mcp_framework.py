"""MCP tool registration framework for agent skills in the conversational todo management system."""

import json
from typing import Any, Dict, List, Callable
from pydantic import BaseModel
from auth.auth_handler import todo_api_client
from utils.logging_config import logger, log_error


class ToolParameter(BaseModel):
    """Definition of a parameter for an MCP tool."""
    name: str
    type: str  # "string", "number", "boolean", "object", "array"
    description: str
    required: bool = True
    default: Any = None


class ToolDefinition(BaseModel):
    """Definition of an MCP tool that can be registered with the agent."""
    name: str
    description: str
    parameters: List[ToolParameter]
    function: Callable


class MCPToolRegistry:
    """Registry for MCP tools that can be used by the OpenAI Agent."""

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.tool_functions: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, parameters: List[ToolParameter], function: Callable):
        """Register a new tool with the MCP framework."""
        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            function=function
        )
        self.tools[name] = tool_def
        self.tool_functions[name] = function
        logger.info(f"Registered tool: {name}")

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """Get the schema for a registered tool in OpenAI-compatible format."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found in registry")

        tool_def = self.tools[tool_name]
        schema = {
            "type": "function",
            "function": {
                "name": tool_def.name,
                "description": tool_def.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

        for param in tool_def.parameters:
            schema["function"]["parameters"]["properties"][param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.default is not None:
                schema["function"]["parameters"]["properties"][param.name]["default"] = param.default

            if param.required:
                schema["function"]["parameters"]["required"].append(param.name)

        return schema

    def get_all_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all registered tools."""
        return [self.get_tool_schema(name) for name in self.tools.keys()]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool with the given arguments."""
        if tool_name not in self.tool_functions:
            raise ValueError(f"Tool {tool_name} not found in registry")

        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            result = self.tool_functions[tool_name](**arguments)
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except Exception as e:
            log_error(e, f"Executing tool {tool_name}")
            raise e


# Initialize the MCP tool registry
mcp_registry = MCPToolRegistry()


# Import the skill functions
from skills.todo_operations import add_task as skill_add_task, update_task as skill_update_task, \
    delete_task as skill_delete_task, list_tasks as skill_list_tasks


def add_task(title: str, description: str = None, dueDate: str = None) -> Dict[str, Any]:
    """
    Add a new task to the todo list.

    Args:
        title: The title of the task
        description: Optional description of the task
        dueDate: Optional due date in ISO format
    """
    try:
        return skill_add_task(title, description, dueDate)
    except Exception as e:
        log_error(e, "add_task")
        raise e


def update_task(id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing task.

    Args:
        id: The ID of the task to update
        updates: Dictionary containing the fields to update
    """
    try:
        return skill_update_task(id, updates)
    except Exception as e:
        log_error(e, "update_task")
        raise e


def delete_task(id: str) -> bool:
    """
    Delete a task by ID.

    Args:
        id: The ID of the task to delete
    """
    try:
        return skill_delete_task(id)
    except Exception as e:
        log_error(e, "delete_task")
        raise e


def list_tasks(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    List tasks with optional filters.

    Args:
        filters: Optional dictionary containing filter criteria
    """
    try:
        return skill_list_tasks(filters)
    except Exception as e:
        log_error(e, "list_tasks")
        raise e


# Register the tools with the MCP framework
mcp_registry.register_tool(
    name="add_task",
    description="Add a new task to the todo list",
    parameters=[
        ToolParameter(
            name="title",
            type="string",
            description="The title of the task",
            required=True
        ),
        ToolParameter(
            name="description",
            type="string",
            description="Optional description of the task",
            required=False
        ),
        ToolParameter(
            name="dueDate",
            type="string",
            description="Optional due date in ISO format",
            required=False
        )
    ],
    function=add_task
)

mcp_registry.register_tool(
    name="update_task",
    description="Update an existing task",
    parameters=[
        ToolParameter(
            name="id",
            type="string",
            description="The ID of the task to update",
            required=True
        ),
        ToolParameter(
            name="updates",
            type="object",
            description="Dictionary containing the fields to update",
            required=True
        )
    ],
    function=update_task
)

mcp_registry.register_tool(
    name="delete_task",
    description="Delete a task by ID",
    parameters=[
        ToolParameter(
            name="id",
            type="string",
            description="The ID of the task to delete",
            required=True
        )
    ],
    function=delete_task
)

mcp_registry.register_tool(
    name="list_tasks",
    description="List tasks with optional filters",
    parameters=[
        ToolParameter(
            name="filters",
            type="object",
            description="Optional dictionary containing filter criteria",
            required=False
        )
    ],
    function=list_tasks
)


def get_mcp_tools_for_openai():
    """Get the registered tools in OpenAI-compatible format."""
    return mcp_registry.get_all_tool_schemas()