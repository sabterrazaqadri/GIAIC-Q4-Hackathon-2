"""Database operations for todo items using Neon PostgreSQL."""
import asyncpg
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


async def get_connection():
    """Get a database connection - always creates a new connection for thread safety."""
    from dotenv import load_dotenv

    # Always create a new direct connection to avoid event loop conflicts
    # when running from different threads (ThreadPoolExecutor)
    load_dotenv()
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        logger.error("NEON_DATABASE_URL not set - cannot connect to database")
        raise RuntimeError("NEON_DATABASE_URL not set")

    conn = await asyncpg.connect(dsn=database_url)
    return conn


async def release_connection(conn):
    """Release/close the connection."""
    await conn.close()


async def add_task_db(title: str, description: Optional[str] = None,
                     status: str = "pending", priority: str = "medium",
                     due_date: Optional[str] = None) -> Dict[str, Any]:
    """Add a new task to the database."""
    conn = await get_connection()

    try:
        query = """
            INSERT INTO todos (title, description, status, priority, due_date)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, title, description, status, priority, due_date, created_at, updated_at
        """

        record = await conn.fetchrow(
            query, title, description, status, priority, due_date
        )

        task = dict(record)
        logger.info(f"Task added to database: {task['id']} - {task['title']}")

        return task

    except Exception as e:
        logger.error(f"Error adding task to database: {e}")
        raise
    finally:
        await release_connection(conn)


async def get_task_db(task_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific task by ID."""
    conn = await get_connection()

    try:
        query = "SELECT * FROM todos WHERE id = $1"
        record = await conn.fetchrow(query, task_id)

        if record:
            return dict(record)
        return None

    except Exception as e:
        logger.error(f"Error getting task {task_id} from database: {e}")
        raise
    finally:
        await release_connection(conn)


async def list_tasks_db(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """List tasks from the database with optional filters."""
    conn = await get_connection()

    try:
        # Build query with optional filters
        query = "SELECT * FROM todos ORDER BY created_at DESC"
        params = []

        if filters:
            conditions = []
            param_index = 1

            for key, value in filters.items():
                if key == 'status':
                    conditions.append(f"status = ${param_index}")
                    params.append(value)
                    param_index += 1
                elif key == 'priority':
                    conditions.append(f"priority = ${param_index}")
                    params.append(value)
                    param_index += 1
                elif key == 'search':
                    conditions.append(f"title ILIKE ${param_index}")
                    params.append(f"%{value}%")
                    param_index += 1

            if conditions:
                query = f"SELECT * FROM todos WHERE {' AND '.join(conditions)} ORDER BY created_at DESC"

        records = await conn.fetch(query, *params)
        tasks = [dict(record) for record in records]

        logger.info(f"Retrieved {len(tasks)} tasks from database")
        return tasks

    except Exception as e:
        logger.error(f"Error listing tasks from database: {e}")
        raise
    finally:
        await release_connection(conn)


async def update_task_db(task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a task in the database."""
    conn = await get_connection()

    try:
        # Build dynamic update query
        set_clauses = []
        params = []
        param_index = 1

        for key, value in updates.items():
            if key in ['title', 'description', 'status', 'priority', 'due_date']:
                set_clauses.append(f"{key} = ${param_index}")
                params.append(value)
                param_index += 1

        if not set_clauses:
            return None  # No valid fields to update

        # Add the task_id as the last parameter
        params.append(task_id)

        query = f"""
            UPDATE todos
            SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ${param_index}
            RETURNING *
        """

        record = await conn.fetchrow(query, *params)

        if record:
            task = dict(record)
            logger.info(f"Task updated in database: {task_id}")
            return task
        return None

    except Exception as e:
        logger.error(f"Error updating task {task_id} in database: {e}")
        raise
    finally:
        await release_connection(conn)


async def delete_task_db(task_id: int) -> bool:
    """Delete a task from the database."""
    conn = await get_connection()

    try:
        query = "DELETE FROM todos WHERE id = $1"
        result = await conn.execute(query, task_id)

        # Check if any rows were affected
        deleted_rows = int(result.split()[-1]) if result.split() else 0
        success = deleted_rows > 0

        if success:
            logger.info(f"Task deleted from database: {task_id}")
        else:
            logger.warning(f"No task found to delete with id: {task_id}")

        return success

    except Exception as e:
        logger.error(f"Error deleting task {task_id} from database: {e}")
        raise
    finally:
        await release_connection(conn)