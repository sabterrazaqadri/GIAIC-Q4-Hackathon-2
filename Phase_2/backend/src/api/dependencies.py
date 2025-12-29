"""FastAPI dependencies for the Todo API."""

from db.connection import Session, engine
from sqlmodel import Session


def get_db() -> Session:
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session
