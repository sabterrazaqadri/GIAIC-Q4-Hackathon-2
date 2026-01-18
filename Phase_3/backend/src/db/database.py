"""Database connection and initialization for Neon PostgreSQL."""
import os
import asyncpg
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Database connection pool
_pool: Optional[asyncpg.Pool] = None

async def init_db_pool():
    """Initialize the database connection pool."""
    global _pool

    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        logger.warning("NEON_DATABASE_URL environment variable is not set, skipping database initialization")
        return

    try:
        _pool = await asyncpg.create_pool(
            dsn=database_url,
            min_size=1,
            max_size=10,
            command_timeout=60,
        )
        logger.info("Database connection pool initialized successfully")

        # Test the connection
        async with _pool.acquire() as conn:
            await conn.execute("SELECT 1")

        # Ensure tables exist
        await _ensure_tables_exist()

    except Exception as e:
        logger.error(f"Failed to initialize database connection pool: {e}")
        raise

async def _ensure_tables_exist():
    """Ensure the todos table exists."""
    global _pool

    if not _pool:
        raise RuntimeError("Database pool not initialized")

    async with _pool.acquire() as conn:
        # Create the todos table if it doesn't exist
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                priority VARCHAR(20) DEFAULT 'medium',
                due_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create updated_at trigger function if it doesn't exist
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)

        # Create trigger if it doesn't exist
        await conn.execute("""
            CREATE OR REPLACE TRIGGER update_todos_updated_at
            BEFORE UPDATE ON todos
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)

def get_db_pool() -> asyncpg.Pool:
    """Get the database connection pool."""
    global _pool
    if not _pool:
        # Return None to indicate database is not available
        return None
    return _pool

async def close_db_pool():
    """Close the database connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")