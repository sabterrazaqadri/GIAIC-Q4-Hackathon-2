# Quickstart: Full-Stack Web Todo Application

## Prerequisites

- **Python 3.13+** (for FastAPI backend)
- **Node.js 18+** (for Next.js frontend)
- **Git** (for version control)
- **Neon Account** (for PostgreSQL database)

## Environment Setup

### 1. Clone and Branch

```bash
git checkout 001-web-todo-app
```

### 2. Backend Setup (FastAPI + SQLModel)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install fastapi uvicorn sqlmodel pydantic psycopg2-binary
pip install -e .

# Set environment variables
export DATABASE_URL="postgresql://user:password@host/dbname"
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### 3. Frontend Setup (Next.js)

```bash
# Create Next.js app
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir

cd frontend
npm install axios

# Set environment variables
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### 4. Database Setup (Neon)

```bash
# Create Neon project
# 1. Go to https://console.neon.tech
# 2. Create new project
# 3. Copy connection string
# 4. Update DATABASE_URL
```

## Running the Application

### Start Backend

```bash
cd backend
python -m uvicorn src.main:app --reload
```

API will be available at: http://localhost:8000
API documentation at: http://localhost:8000/docs

### Start Frontend

```bash
cd frontend
npm run dev
```

Application will be available at: http://localhost:3000

## Development Workflow

### 1. Create New Todo (API Test)

```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs", "priority": "medium"}'
```

### 2. List Todos

```bash
curl http://localhost:8000/todos
```

### 3. Update Todo

```bash
curl -X PUT http://localhost:8000/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and coffee", "priority": "high"}'
```

### 4. Complete Todo

```bash
curl -X PATCH http://localhost:8000/todos/{id}/complete
```

### 5. Delete Todo

```bash
curl -X DELETE http://localhost:8000/todos/{id}
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── db/
│   │   └── connection.py # Database connection
│   ├── models/
│   │   └── todo.py       # SQLModel Todo entity
│   ├── schemas/
│   │   └── todo.py       # Pydantic schemas
│   └── api/
│       └── routes.py     # REST endpoints
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx      # Main todo list
│   │   ├── layout.tsx    # Root layout
│   │   └── globals.css   # Global styles
│   ├── components/
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   └── TodoForm.tsx
│   ├── services/
│   │   └── api.ts        # API client
│   └── types/
│       └── todo.ts       # TypeScript types
├── public/
├── tests/
├── next.config.js
├── tailwind.config.js
└── package.json
```

## Next Steps

1. **Set up database connection** in `backend/src/db/connection.py`
2. **Implement Todo model** in `backend/src/models/todo.py`
3. **Create API schemas** in `backend/src/schemas/todo.py`
4. **Build REST endpoints** in `backend/src/api/routes.py`
5. **Create FastAPI app** in `backend/src/main.py`
6. **Build frontend components** in `frontend/src/components/`
7. **Implement API service** in `frontend/src/services/api.ts`
8. **Create Next.js pages** in `frontend/src/app/`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection failed | Verify Neon connection string; check IP allowlist |
| CORS errors | Add frontend origin to backend CORS middleware |
| Module not found | Ensure virtual environment is activated |
| Next.js build errors | Check TypeScript types match API responses |
