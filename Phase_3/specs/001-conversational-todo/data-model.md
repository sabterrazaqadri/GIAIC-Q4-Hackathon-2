# Data Model: AI-Powered Conversational Todo Management

## Core Entities

### Todo Task
**Description**: The primary entity representing a user's task or todo item

**Fields**:
- `id` (string, required, unique): Unique identifier for the task
- `title` (string, required): The main title or description of the task
- `description` (string, optional): Additional details about the task
- `status` (enum, required): Current status of the task ['pending', 'completed', 'in-progress']
- `dueDate` (string, optional): Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)
- `createdAt` (string, required): Creation timestamp in ISO 8601 format
- `updatedAt` (string, required): Last update timestamp in ISO 8601 format
- `userId` (string, required): Identifier of the user who owns this task

**Validation Rules**:
- `title` must be 1-200 characters
- `description` must be 0-1000 characters if provided
- `status` must be one of the allowed values
- `dueDate` must be a valid future date if provided
- `createdAt` and `updatedAt` are automatically managed by the system

**State Transitions**:
- `pending` → `in-progress`: When user starts working on the task
- `pending` → `completed`: When user marks task as done
- `in-progress` → `completed`: When user finishes the task
- `completed` → `pending`: When user reopens the task

### Chat Message
**Description**: Represents messages exchanged in the chat conversation

**Fields**:
- `id` (string, required, unique): Unique identifier for the message
- `userId` (string, required): Identifier of the user who sent the message
- `content` (string, required): The text content of the message
- `role` (enum, required): The sender of the message ['user', 'assistant']
- `timestamp` (string, required): When the message was sent in ISO 8601 format
- `intent` (string, optional): The classified intent from the agent
- `taskId` (string, optional): Associated task ID if the message relates to a specific task

**Validation Rules**:
- `content` must be 1-2000 characters
- `role` must be either 'user' or 'assistant'
- `timestamp` is automatically set when message is created

### Intent Classification
**Description**: Represents the classified intent from user input

**Fields**:
- `id` (string, required, unique): Unique identifier for the intent
- `type` (enum, required): The type of intent ['ADD_TASK', 'UPDATE_TASK', 'DELETE_TASK', 'LIST_TASKS', 'UNKNOWN']
- `parameters` (object, optional): Additional parameters extracted from the intent
- `confidence` (number, required): Confidence score between 0 and 1
- `originalText` (string, required): The original user input text
- `timestamp` (string, required): When the intent was classified in ISO 8601 format

**Validation Rules**:
- `confidence` must be between 0 and 1
- `type` must be one of the allowed values
- `parameters` structure varies by intent type

## Relationships

### Todo Task ↔ Chat Message
- One Todo Task can be referenced by multiple Chat Messages
- One Chat Message can reference zero or one Todo Task
- Relationship: One-to-Many (from Task perspective)

### User ↔ Todo Task
- One User can own multiple Todo Tasks
- One Todo Task belongs to exactly one User
- Relationship: One-to-Many (from User perspective)

### User ↔ Chat Message
- One User can send multiple Chat Messages
- One Chat Message is sent by exactly one User
- Relationship: One-to-Many (from User perspective)

## Business Rules

1. **Task Ownership**: Users can only modify or delete their own tasks
2. **Unique Identification**: Each task has a unique ID within the system
3. **Status Management**: Tasks can only transition between statuses according to defined rules
4. **Data Integrity**: All timestamps are stored in UTC in ISO 8601 format
5. **Privacy**: Users cannot access tasks belonging to other users

## Constraints

1. **Title Length**: Task titles must be between 1 and 200 characters
2. **Description Length**: Task descriptions must be between 0 and 1000 characters
3. **Future Due Dates**: Due dates must be in the future (not past dates)
4. **Required Fields**: All required fields must be provided when creating entities
5. **Immutable IDs**: Once created, entity IDs cannot be changed