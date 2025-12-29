"""Basic message response schema."""

from pydantic import BaseModel


class Message(BaseModel):
    """Simple message response for operations like delete."""
    message: str
