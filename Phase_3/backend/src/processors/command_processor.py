"""
Command processor for handling natural language commands using OpenAI Agents SDK.
"""

from typing import Dict, Any
from intelligence.agent import run_agent_sync
from utils.logging_config import logger


def process_command(user_input: str, user_id: str = None) -> Dict[str, Any]:
    """
    Process a user command using OpenAI Agents SDK.

    Args:
        user_input: The raw user input string
        user_id: Optional user ID for context

    Returns:
        Dictionary containing the result of the command execution
    """
    try:
        logger.info(f"Processing command from user {user_id}: {user_input}")
        print(f"DEBUG process_command: calling run_agent_sync with: {user_input}")

        # Use the OpenAI Agents SDK to process the command
        result = run_agent_sync(user_input)
        print(f"DEBUG process_command: got result: {result}")

        if result.get("success"):
            return {
                "status": "success",
                "message": result.get("message", "Task completed successfully"),
                "action": "agent_command",
                "confidence": 0.95,
                "original_input": user_input
            }
        else:
            return {
                "status": "error",
                "message": result.get("message", "An error occurred"),
                "action": "agent_command",
                "confidence": 0.0,
                "original_input": user_input
            }

    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return {
            "status": "error",
            "message": f"An error occurred while processing your command: {str(e)}",
            "original_input": user_input
        }
