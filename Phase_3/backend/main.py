"""
Main FastAPI application for Phase 3: AI-Powered Conversational Todo Management
Uses OpenAI Agents SDK for natural language processing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# OpenAI API key (server-side only)
_openai_api_key = os.getenv("OPENAI_API_KEY")

# Import command processor - directly import function, not class
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from processors.command_processor import process_command
from utils.logging_config import logger
from db.database import init_db_pool, close_db_pool

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Conversational Todo API",
    description="Natural language interface for todo management powered by OpenAI Agents SDK",
    version="2.0.0"  # Updated to reflect OpenAI Agents SDK integration
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    logger.info("Starting up - initializing database connection...")
    try:
        await init_db_pool()
        logger.info("Database connection initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Don't raise - allow app to start even without DB


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    logger.info("Shutting down - closing database connection...")
    await close_db_pool()


# Request/Response Models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None


class ChatKitSessionResponse(BaseModel):
    client_secret: str


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "AI-Powered Conversational Todo API (OpenAI Agents SDK)",
        "version": "2.0.0",
        "description": "Natural language interface for todo management powered by OpenAI Agents SDK",
        "endpoints": {
            "POST /chat": "Send a natural language command to manage todos (uses OpenAI Agents SDK)",
            "GET /health": "Health check endpoint"
        },
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "conversational-todo-api",
        "version": "2.0.0",
        "engine": "OpenAI Agents SDK"
    }


@app.post("/api/chatkit/session", response_model=ChatKitSessionResponse)
async def create_chatkit_session():
    """
    Create a ChatKit session and return client secret (server-side only).

    Note: ChatKit Sessions API may require a workflow_id created in OpenAI Agent Builder.
    If you don't have a workflow_id, this endpoint will not work with ChatKit React.
    """
    if not _openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    workflow_id = os.getenv("CHATKIT_WORKFLOW_ID")
    if not workflow_id:
        logger.warning("CHATKIT_WORKFLOW_ID not configured - ChatKit integration may not work")
        # Continue anyway to allow endpoint to be callable

    # According to OpenAI documentation, use chatkit_beta header
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chatkit/sessions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_openai_api_key}",
                "OpenAI-Beta": "chatkit_beta=v1",
            },
            json={
                "workflow": {"id": workflow_id} if workflow_id else None,
                "user": "local-dev",
            },
            timeout=30,
        )

        if resp.status_code >= 400:
            logger.error(f"ChatKit API request failed: {resp.status_code} {resp.text}")
            # Check if it's a 404 (endpoint doesn't exist) vs other errors
            if resp.status_code == 404:
                raise HTTPException(
                    status_code=502,
                    detail="ChatKit Sessions API not found (404). Please create a workflow in OpenAI Agent Builder."
                )
            else:
                raise HTTPException(
                    status_code=502,
                    detail=f"ChatKit session request failed: {resp.status_code} {resp.text}"
                )

        payload = resp.json()
        client_secret = payload.get("client_secret")
        if not client_secret:
            raise HTTPException(status_code=502, detail="ChatKit session response missing client_secret")

        logger.info("ChatKit session created successfully")
        return ChatKitSessionResponse(client_secret=client_secret)

    except HTTPException:
        raise
    except requests.RequestException as e:
        logger.error(f"ChatKit session HTTP request failed: {str(e)}")
        raise HTTPException(status_code=502, detail=f"ChatKit session creation failed: {str(e)}")
    except Exception as e:
        logger.error(f"ChatKit session creation failed: {str(e)}")
        raise HTTPException(status_code=502, detail=f"ChatKit session creation failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a natural language command for todo management using OpenAI Agents SDK.

    Supports:
    - Adding tasks: "Add buy milk to my list"
    - Updating tasks: "Mark buy milk as completed"
    - Deleting tasks: "Delete meeting task"
    - Listing tasks: "Show my tasks"
    - Urdu commands: "کام شامل کریں buy milk"
    """
    try:
        logger.info(f"Received chat message: {message.message}")

        # Use OpenAI Agents SDK to process the command
        result = process_command(
            user_input=message.message,
            user_id=message.user_id
        )

        # Extract response data
        status = result.get("status", "error")
        response_message = result.get("message", "An error occurred")
        confidence = result.get("confidence", None)

        # Prepare data payload
        data = {
            "action": result.get("action"),
            "original_input": result.get("original_input"),
        }

        # Add task/tasks data if available
        if "task" in result:
            data["task"] = result["task"]
        if "tasks" in result:
            data["tasks"] = result["tasks"]

        return ChatResponse(
            status=status,
            message=response_message,
            data=data,
            confidence=confidence
        )

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )


@app.get("/test")
async def test_connection():
    """Test endpoint to verify backend is running"""
    return {
        "status": "ok",
        "message": "Phase 3 backend is running with OpenAI Agents SDK",
        "backend_url": os.getenv("TODO_API_BASE_URL", "not configured"),
        "features": {
            "openai_agents_sdk": "installed",
            "chatkit_endpoint": "available (optional)"
        }
    }


# ==================== Direct Database Endpoints ====================
# These endpoints serve tasks directly from the local Neon PostgreSQL database

from db.todo_operations import list_tasks_db, get_task_db, update_task_db, delete_task_db, add_task_db


@app.get("/todos")
async def get_todos():
    """Get all todos from the database"""
    try:
        logger.info("Fetching all todos from database")
        tasks = await list_tasks_db()
        # Transform to match frontend expected format
        return [
            {
                "id": task.get("id"),
                "title": task.get("title", ""),
                "description": task.get("description"),
                "status": task.get("status", "pending"),
                "is_complete": task.get("status") == "completed",
                "priority": task.get("priority", "medium"),
                "created_at": str(task.get("created_at", "")),
                "updated_at": str(task.get("updated_at", "")),
            }
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Error fetching todos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/todos/{task_id}")
async def get_todo(task_id: int):
    """Get a specific todo by ID"""
    try:
        logger.info(f"Fetching todo {task_id} from database")
        task = await get_task_db(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "id": task.get("id"),
            "title": task.get("title", ""),
            "description": task.get("description"),
            "status": task.get("status", "pending"),
            "is_complete": task.get("status") == "completed",
            "priority": task.get("priority", "medium"),
            "created_at": str(task.get("created_at", "")),
            "updated_at": str(task.get("updated_at", "")),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching todo {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.put("/todos/{task_id}")
async def update_todo(task_id: int, body: Dict[str, Any]):
    """Update a todo by ID"""
    try:
        logger.info(f"Updating todo {task_id} with: {body}")
        # Map frontend fields to database fields
        updates = {}
        if "title" in body:
            updates["title"] = body["title"]
        if "description" in body:
            updates["description"] = body["description"]
        if "status" in body:
            updates["status"] = body["status"]
        if "is_complete" in body:
            updates["status"] = "completed" if body["is_complete"] else "pending"
        if "priority" in body:
            updates["priority"] = body["priority"]

        task = await update_task_db(task_id, updates)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "id": task.get("id"),
            "title": task.get("title", ""),
            "description": task.get("description"),
            "status": task.get("status", "pending"),
            "is_complete": task.get("status") == "completed",
            "priority": task.get("priority", "medium"),
            "created_at": str(task.get("created_at", "")),
            "updated_at": str(task.get("updated_at", "")),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/todos/{task_id}")
async def delete_todo(task_id: int):
    """Delete a todo by ID"""
    try:
        logger.info(f"Deleting todo {task_id} from database")
        success = await delete_task_db(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "deleted", "id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run(app, host="0.0.0.0", port=port)
