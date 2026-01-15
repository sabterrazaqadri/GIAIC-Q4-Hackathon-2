"""Chat Message and Intent Classification models for the conversational todo management system."""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"


class IntentType(str, Enum):
    """Type of intent from user input."""
    ADD_TASK = "ADD_TASK"
    UPDATE_TASK = "UPDATE_TASK"
    DELETE_TASK = "DELETE_TASK"
    LIST_TASKS = "LIST_TASKS"
    UNKNOWN = "UNKNOWN"


class ChatMessage(BaseModel):
    """
    Chat Message Entity: Represents messages exchanged in the chat conversation

    Fields:
    - id: string (unique identifier)
    - userId: string (user identifier)
    - content: string (message content)
    - role: enum ['user', 'assistant'] (message sender)
    - timestamp: string (when the message was sent in ISO 8601 format)
    - intent: string (classified intent from the agent)
    - taskId: string (associated task ID if the message relates to a specific task)

    Validation Rules:
    - content must be 1-2000 characters
    - role must be either 'user' or 'assistant'
    - timestamp is automatically set when message is created
    """

    id: str = Field(..., description="Unique identifier for the message")
    userId: str = Field(..., description="Identifier of the user who sent the message")
    content: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The text content of the message"
    )
    role: MessageRole = Field(..., description="The sender of the message")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="When the message was sent in ISO 8601 format"
    )
    intent: Optional[str] = Field(
        None,
        description="The classified intent from the agent"
    )
    taskId: Optional[str] = Field(
        None,
        description="Associated task ID if the message relates to a specific task"
    )


class IntentClassification(BaseModel):
    """
    Intent Classification Entity: Represents the classified intent from user input

    Fields:
    - id: string (unique identifier)
    - type: enum ['ADD_TASK', 'UPDATE_TASK', 'DELETE_TASK', 'LIST_TASKS', 'UNKNOWN'] (intent type)
    - parameters: object (intent-specific parameters)
    - confidence: number (confidence score between 0 and 1)
    - originalText: string (original user input text)
    - timestamp: string (when the intent was classified in ISO 8601 format)

    Validation Rules:
    - confidence must be between 0 and 1
    - type must be one of the allowed values
    - parameters structure varies by intent type
    """

    id: str = Field(..., description="Unique identifier for the intent")
    type: IntentType = Field(..., description="The type of intent")
    parameters: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional parameters extracted from the intent"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    originalText: str = Field(..., description="The original user input text")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="When the intent was classified in ISO 8601 format"
    )