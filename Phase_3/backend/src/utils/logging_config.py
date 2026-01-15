"""Error handling and logging infrastructure for the conversational todo management system."""

import logging
import sys
from datetime import datetime
from typing import Any, Dict
from enum import Enum


class LogLevel(str, Enum):
    """Log levels for the application."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def setup_logging(service_name: str = "conversational-todo", level: LogLevel = LogLevel.INFO):
    """Set up logging infrastructure for the application."""

    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.value))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.value))

    # Create file handler
    file_handler = logging.FileHandler(f"{service_name}.log")
    file_handler.setLevel(getattr(logging, level.value))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_error(error: Exception, context: str = "", logger: logging.Logger = None):
    """Log an error with context."""
    if logger is None:
        logger = setup_logging()

    logger.error(
        f"Error in {context}: {str(error)} | Type: {type(error).__name__} | "
        f"Timestamp: {datetime.utcnow().isoformat()}"
    )


def log_info(message: str, context: str = "", logger: logging.Logger = None):
    """Log an informational message."""
    if logger is None:
        logger = setup_logging()

    logger.info(
        f"{context}: {message} | Timestamp: {datetime.utcnow().isoformat()}"
    )


def handle_api_error(error: Exception, status_code: int = 500) -> Dict[str, Any]:
    """Handle API errors and return standardized error response."""
    error_response = {
        "error": {
            "type": type(error).__name__,
            "message": str(error),
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat(),
        }
    }
    return error_response


class TodoException(Exception):
    """Base exception class for todo-related errors."""

    def __init__(self, message: str, status_code: int = 400, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class TaskNotFoundException(TodoException):
    """Exception raised when a task is not found."""

    def __init__(self, task_id: str):
        super().__init__(
            message=f"Task with ID {task_id} not found",
            status_code=404
        )


class InvalidTaskDataException(TodoException):
    """Exception raised when task data is invalid."""

    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Invalid task data for field '{field}': {reason}",
            status_code=422
        )


class AuthenticationException(TodoException):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401
        )


# Initialize the main logger
logger = setup_logging()