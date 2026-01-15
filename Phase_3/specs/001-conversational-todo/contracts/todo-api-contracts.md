# API Contracts: AI-Powered Conversational Todo Management

## FastAPI Todo API Contracts

### Base URL
`http://localhost:8000/api` (or configured endpoint from environment)

### Authentication
All endpoints require Bearer token authentication via the `Authorization` header:
```
Authorization: Bearer {access_token}
```

## Todo Endpoints

### Create Todo
**Endpoint**: `POST /api/todos`
**Description**: Creates a new todo item

**Request**:
```json
{
  "title": "string (1-200 characters)",
  "description": "string (0-1000 characters, optional)",
  "dueDate": "string (ISO 8601 format, optional)"
}
```

**Response**:
- `201 Created`: Todo created successfully
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "string (pending|completed|in-progress)",
  "dueDate": "string (ISO 8601 format, optional)",
  "createdAt": "string (ISO 8601 format)",
  "updatedAt": "string (ISO 8601 format)",
  "userId": "string"
}
```
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication
- `422 Unprocessable Entity`: Validation error

### List Todos
**Endpoint**: `GET /api/todos`
**Description**: Retrieves a list of todo items with optional filtering

**Query Parameters**:
- `status` (optional): Filter by status (pending|completed|in-progress)
- `limit` (optional): Maximum number of results (default: 50, max: 100)
- `offset` (optional): Number of results to skip (for pagination)

**Response**:
- `200 OK`: Todos retrieved successfully
```json
{
  "items": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "status": "string (pending|completed|in-progress)",
      "dueDate": "string (ISO 8601 format, optional)",
      "createdAt": "string (ISO 8601 format)",
      "updatedAt": "string (ISO 8601 format)",
      "userId": "string"
    }
  ],
  "total": "number",
  "offset": "number",
  "limit": "number"
}
```
- `401 Unauthorized`: Invalid or missing authentication

### Get Todo
**Endpoint**: `GET /api/todos/{id}`
**Description**: Retrieves a specific todo item by ID

**Path Parameters**:
- `id`: The unique identifier of the todo item

**Response**:
- `200 OK`: Todo retrieved successfully
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "string (pending|completed|in-progress)",
  "dueDate": "string (ISO 8601 format, optional)",
  "createdAt": "string (ISO 8601 format)",
  "updatedAt": "string (ISO 8601 format)",
  "userId": "string"
}
```
- `401 Unauthorized`: Invalid or missing authentication
- `404 Not Found`: Todo with specified ID not found

### Update Todo
**Endpoint**: `PUT /api/todos/{id}`
**Description**: Updates an existing todo item

**Path Parameters**:
- `id`: The unique identifier of the todo item

**Request**:
```json
{
  "title": "string (1-200 characters, optional)",
  "description": "string (0-1000 characters, optional)",
  "status": "string (pending|completed|in-progress, optional)",
  "dueDate": "string (ISO 8601 format, optional)"
}
```

**Response**:
- `200 OK`: Todo updated successfully
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "string (pending|completed|in-progress)",
  "dueDate": "string (ISO 8601 format, optional)",
  "createdAt": "string (ISO 8601 format)",
  "updatedAt": "string (ISO 8601 format)",
  "userId": "string"
}
```
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication
- `404 Not Found`: Todo with specified ID not found
- `422 Unprocessable Entity`: Validation error

### Delete Todo
**Endpoint**: `DELETE /api/todos/{id}`
**Description**: Deletes a specific todo item by ID

**Path Parameters**:
- `id`: The unique identifier of the todo item

**Response**:
- `204 No Content`: Todo deleted successfully
- `401 Unauthorized`: Invalid or missing authentication
- `404 Not Found`: Todo with specified ID not found

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "string (human-readable error message)"
}
```

## Agent Skills as MCP Tools

### add_task
**Description**: Creates a new task via the agent

**Parameters**:
```json
{
  "title": {
    "type": "string",
    "description": "The title of the task to create",
    "required": true
  },
  "description": {
    "type": "string",
    "description": "Optional description of the task",
    "required": false
  },
  "dueDate": {
    "type": "string",
    "description": "Optional due date in ISO 8601 format",
    "required": false
  }
}
```

**Returns**: Todo object as defined above

### update_task
**Description**: Updates an existing task via the agent

**Parameters**:
```json
{
  "id": {
    "type": "string",
    "description": "The ID of the task to update",
    "required": true
  },
  "updates": {
    "type": "object",
    "description": "Object containing fields to update",
    "required": true,
    "properties": {
      "title": {"type": "string"},
      "description": {"type": "string"},
      "status": {"type": "string"},
      "dueDate": {"type": "string"}
    }
  }
}
```

**Returns**: Updated Todo object as defined above

### delete_task
**Description**: Deletes a task via the agent

**Parameters**:
```json
{
  "id": {
    "type": "string",
    "description": "The ID of the task to delete",
    "required": true
  }
}
```

**Returns**: Boolean indicating success

### list_tasks
**Description**: Lists tasks with optional filters via the agent

**Parameters**:
```json
{
  "filters": {
    "type": "object",
    "description": "Optional filters for task listing",
    "required": false,
    "properties": {
      "status": {"type": "string"},
      "limit": {"type": "number"},
      "offset": {"type": "number"}
    }
  }
}
```

**Returns**: Array of Todo objects as defined above