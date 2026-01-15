# Phase II FastAPI Todo API Documentation

## API Endpoints

### Base URL: `/api/todos`

#### 1. Create Todo
- **Method**: `POST /api/todos`
- **Request Body**:
  ```json
  {
    "title": "string (1-200 chars)",
    "description": "string (optional, max 2000 chars)",
    "priority": "enum ['low', 'medium', 'high'] (default: 'medium')"
  }
  ```
- **Response**: `201 Created` with TodoResponse object
- **Description**: Creates a new todo item

#### 2. List Todos
- **Method**: `GET /api/todos`
- **Query Parameters**:
  - `is_complete`: boolean (optional) - filter by completion status
- **Response**: `200 OK` with array of TodoResponse objects
- **Description**: List all todos, optionally filtered by completion status

#### 3. Get Todo by ID
- **Method**: `GET /api/todos/{todo_id}`
- **Path Parameter**: `todo_id` (integer)
- **Response**: `200 OK` with TodoResponse object
- **Description**: Get a single todo by ID

#### 4. Update Todo (Full Update)
- **Method**: `PUT /api/todos/{todo_id}`
- **Path Parameter**: `todo_id` (integer)
- **Request Body**:
  ```json
  {
    "title": "string (1-200 chars)",
    "description": "string (optional, max 2000 chars)",
    "priority": "enum ['low', 'medium', 'high']",
    "is_complete": "boolean"
  }
  ```
- **Response**: `200 OK` with TodoResponse object
- **Description**: Update a todo item (full update)

#### 5. Update Todo (Partial Update)
- **Method**: `PATCH /api/todos/{todo_id}`
- **Path Parameter**: `todo_id` (integer)
- **Request Body**:
  ```json
  {
    "title"?: "string (1-200 chars)",
    "description"?: "string (optional, max 2000 chars)",
    "priority"?: "enum ['low', 'medium', 'high']",
    "is_complete"?: "boolean"
  }
  ```
- **Response**: `200 OK` with TodoResponse object
- **Description**: Update a todo item (partial update)

#### 6. Delete Todo
- **Method**: `DELETE /api/todos/{todo_id}`
- **Path Parameter**: `todo_id` (integer)
- **Response**: `204 No Content`
- **Description**: Delete a todo item

#### 7. Mark Todo as Complete
- **Method**: `PATCH /api/todos/{todo_id}/complete`
- **Path Parameter**: `todo_id` (integer)
- **Response**: `200 OK` with TodoResponse object
- **Description**: Mark a todo as complete

#### 8. Mark Todo as Incomplete
- **Method**: `PATCH /api/todos/{todo_id}/incomplete`
- **Path Parameter**: `todo_id` (integer)
- **Response**: `200 OK` with TodoResponse object
- **Description**: Mark a todo as incomplete

## Data Models

### TodoResponse
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (nullable)",
  "priority": "enum ['low', 'medium', 'high']",
  "is_complete": "boolean",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### TodoCreate
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, max 2000 chars)",
  "priority": "enum ['low', 'medium', 'high'] (default: 'medium')"
}
```

### TodoUpdate
```json
{
  "title"?: "string (1-200 chars)",
  "description"?: "string (optional, max 2000 chars)",
  "priority"?: "enum ['low', 'medium', 'high']",
  "is_complete"?: "boolean"
}
```

## Authentication
- Bearer token authentication via Authorization header (to be confirmed)

## Error Handling
- Standard HTTP status codes
- 404 Not Found for non-existent todo IDs
- 422 Unprocessable Entity for validation errors