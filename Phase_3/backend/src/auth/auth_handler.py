"""Authentication and authorization framework for API calls in the conversational todo management system."""

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests

# Get secret key from environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    """Data contained in a JWT token."""
    user_id: str
    username: str
    expires_at: datetime


class AuthHandler:
    """Authentication and authorization handler for API calls."""

    security = HTTPBearer()

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a new access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """Verify a JWT token and return the token data."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")
            username: str = payload.get("username")
            expires_at: float = payload.get("exp")

            if user_id is None or username is None:
                return None

            # Check if token has expired
            if datetime.utcnow().timestamp() > expires_at:
                return None

            return TokenData(
                user_id=user_id,
                username=username,
                expires_at=datetime.fromtimestamp(expires_at)
            )
        except jwt.PyJWTError:
            return None

    @staticmethod
    def authenticate_user(token: str) -> Optional[TokenData]:
        """Authenticate a user based on their token."""
        return AuthHandler.verify_token(token)

    @staticmethod
    def get_current_user(request: Request) -> Optional[TokenData]:
        """Get the current user from the request."""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix
        return AuthHandler.authenticate_user(token)

    @staticmethod
    def validate_user_access(user_id: str, requested_resource_user_id: str) -> bool:
        """Validate that a user has access to a specific resource."""
        # In a real implementation, this would check if the user has permission
        # to access the requested resource. For now, we'll just check if it's their own resource.
        return user_id == requested_resource_user_id

    @staticmethod
    def get_user_from_token(credentials: HTTPAuthorizationCredentials = None) -> Optional[TokenData]:
        """Get user from HTTP authorization credentials."""
        if not credentials:
            return None
        return AuthHandler.verify_token(credentials.credentials)


# API Client for making authenticated calls to the Phase II backend
class TodoAPIClient:
    """Client for making authenticated API calls to the Phase II FastAPI Todo backend."""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("TODO_API_BASE_URL", "http://localhost:8000/api")
        self.auth_token = os.getenv("TODO_API_AUTH_TOKEN")  # Bearer token for Phase II API

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None):
        """Make an authenticated request to the Todo API."""
        # Allow TODO_API_BASE_URL to be configured as either:
        # - "https://host" (recommended)
        # - "https://host/" (trailing slash ok)
        # - "https://host/todos" (legacy from earlier setup)
        base = (self.base_url or "").rstrip("/")
        if base.endswith("/todos"):
            base = base[: -len("/todos")]

        endpoint = "/" + endpoint.lstrip("/")
        url = f"{base}{endpoint}"

        headers = {
            "Content-Type": "application/json"
        }

        # Add authentication header if available
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Check if the request was successful
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API request failed: {response.text}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error making API request: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

    def create_todo(self, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new todo via the API."""
        return self._make_request("POST", "/todos", data=todo_data)

    def get_todo(self, todo_id: str) -> Dict[str, Any]:
        """Get a specific todo via the API."""
        return self._make_request("GET", f"/todos/{todo_id}")

    def list_todos(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """List todos via the API with optional filters."""
        return self._make_request("GET", "/todos", params=filters)

    def update_todo(self, todo_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a todo via the API."""
        return self._make_request("PUT", f"/todos/{todo_id}", data=update_data)

    def delete_todo(self, todo_id: str) -> None:
        """Delete a todo via the API."""
        # DELETE typically returns 204 No Content, so we handle empty responses
        base = (self.base_url or "").rstrip("/")
        if base.endswith("/todos"):
            base = base[: -len("/todos")]

        endpoint = f"/todos/{todo_id}"
        url = f"{base}{endpoint}"

        headers = {
            "Content-Type": "application/json"
        }

        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        response = requests.delete(url, headers=headers)

        # DELETE returns 204 or 200 typically, both are success
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API request failed: {response.text}"
            )

        # Return None for successful deletes (empty response is expected)
        return None

    def mark_todo_complete(self, todo_id: str) -> Dict[str, Any]:
        """Mark a todo as complete via the API."""
        return self._make_request("PATCH", f"/todos/{todo_id}/complete")

    def mark_todo_incomplete(self, todo_id: str) -> Dict[str, Any]:
        """Mark a todo as incomplete via the API."""
        return self._make_request("PATCH", f"/todos/{todo_id}/incomplete")


# Initialize the auth handler
auth_handler = AuthHandler()
todo_api_client = TodoAPIClient()