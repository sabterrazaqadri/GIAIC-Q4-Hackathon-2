# Research: Full-Stack Web Todo Application

## Key Technology Decisions

### Decision 1: SQLModel vs Raw SQL

**Decision**: SQLModel with PostgreSQL

**Rationale**:
- SQLModel provides type safety at both Python and database levels through Pydantic integration
- Auto-generates table schemas from Python classes, reducing boilerplate
- Native support for async operations via SQLAlchemy 2.0 async engine
- Pydantic validation ensures data integrity before database operations
- SQLModel is the recommended ORM for FastAPI applications (created by same author)

**Alternatives Considered**:
- **Raw SQL**: Maximum flexibility but error-prone; no type safety; harder to maintain
- **SQLAlchemy Core**: More mature but steeper learning curve; more verbose than SQLModel
- **Django ORM**: Full-stack framework overhead; unnecessary for simple CRUD app
- **Tortoise ORM**: Async-native but less documentation and community support

**Why Not Others**: SQLModel balances type safety, developer experience, and FastAPI compatibility. Raw SQL would violate Spec-Driven principles by requiring manual query management.

---

### Decision 2: REST vs RPC

**Decision**: REST (Representational State Transfer)

**Rationale**:
- REST is the industry standard for web APIs; well-understood by developers
- Naturally maps to CRUD operations: GET/POST/PUT/DELETE
- Stateless communication simplifies scaling and debugging
- Native browser support (no special client required)
- Future-proof for Phase III AI agent integration (HTTP-based tools)

**Alternatives Considered**:
- **RPC (gRPC)**: Better performance for internal services; requires code generation; harder to debug
- **GraphQL**: Flexible queries; over-engineering for simple CRUD; adds complexity
- **WebSockets**: Real-time updates; not needed for this use case
- **tRPC**: Type-safe API; requires full TypeScript stack; not compatible with Python backend

**Why REST**: Simplicity and universality. The application needs basic CRUD operations, and REST provides the right level of complexity without over-engineering. HTTP methods map directly to user actions (create, read, update, delete).

---

### Decision 3: Neon Serverless PostgreSQL

**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- Serverless architecture scales to zero; cost-effective for development
- Native support for TypeScript/Node.js and Python (via psycopg2/asyncpg)
- Automatic backups and high availability built-in
- Branching support enables easy development workflows
- Connection pooling optimized for serverless functions
- No infrastructure management required

**Alternatives Considered**:
- **Traditional VPS (DigitalOcean, Linode)**: Full control but requires sysadmin work
- **Supabase**: Similar serverless Postgres; additional auth/storage features (overkill)
- **AWS RDS**: Enterprise-grade; more complex; higher cost for small projects
- **Railway/Render**: Simpler deployment; less control over database configuration
- **Local SQLite**: Good for development; not production-ready

**Why Neon**: Best balance of serverless simplicity, developer experience, and cost for this project. Connection pooling and automatic scaling make it production-ready without ops overhead.

---

## Development Flow

### Phase 0: Research (COMPLETED)
- [x] Technology decisions documented
- [x] Architecture patterns selected
- [x] Trade-offs analyzed

### Phase 1: API Foundation (NEXT)
- Design data model (SQLModel entities)
- Define REST API contracts (OpenAPI)
- Set up database connection
- Implement CRUD endpoints

### Phase 2: UI Integration
- Create Next.js pages and components
- Connect frontend to backend API
- Implement form handling and validation
- Add visual feedback for user actions

### Phase 3: Validation
- Verify API endpoints return correct data
- Confirm database persistence across reloads
- Test frontend-backend synchronization
- Validate Phase I logic preserved (if migrating from console app)

---

## Best Practices Applied

### REST API Design
- Resource-based URLs (`/todos`, `/todos/{id}`)
- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- JSON request/response payloads
- Proper HTTP status codes (200, 201, 400, 404, 500)

### Database Schema
- UUID primary keys (globally unique, no number collision)
- Timestamps for auditing (`created_at`, `updated_at`)
- Priority enum with constraints
- Index on `is_complete` for filtering

### Frontend Architecture
- Next.js App Router for server components
- Client components for interactive forms
- API service layer for HTTP communication
- TypeScript for type safety
