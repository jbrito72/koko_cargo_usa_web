# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Rules for Claude

1. **Always consult PROJECT_INDEX.md first** - This file contains the complete project structure, API endpoints, database schema, and architecture overview. Reference it before making any assumptions about the codebase.

2. **Use PROJECT_INDEX.md for navigation** - When asked about project structure, features, or where to find specific functionality, refer to PROJECT_INDEX.md for the authoritative project map.

3. **Cross-reference documentation** - When working on features, check both this CLAUDE.md for technical details and PROJECT_INDEX.md for architectural context.

4. **Domain knowledge source** - For understanding shrimp production domain models and their relationships, PROJECT_INDEX.md contains the complete database schema documentation.

## Project Overview

This is a shrimp farming production management system built on the FastAPI Full-Stack Template. The system manages production tracking, feeding schedules, harvest settlements, and multi-company inventory integration for shrimp farming operations.

**Domain Context**: The application connects to a PostgreSQL cluster with a main `camaronera` database for production data and multiple company databases for inventory management. It includes extensive domain models for tracking shrimp growth, feeding, harvesting, and processing.

**Key Documentation Files**:
- `PROJECT_INDEX.md` - Complete project structure, API documentation, and database schema
- `docs/descripcion-del-proyecto.md` - Detailed domain model descriptions in Spanish
- `README.md` - Original FastAPI template documentation
- `deployment.md` - Production deployment instructions
- `development.md` - Development environment setup

## Development Commands

### Backend Development
```bash
# Run all backend tests
cd backend && uv run pytest

# Run specific test file
cd backend && uv run pytest tests/api/routes/test_users.py

# Run specific test function
cd backend && uv run pytest tests/api/routes/test_users.py::test_create_user

# Run tests with coverage
cd backend && uv run coverage run -m pytest
cd backend && uv run coverage report

# Format code (uses ruff)
cd backend && uv run bash scripts/format.sh

# Lint code (mypy + ruff)
cd backend && uv run bash scripts/lint.sh

# Type checking only
cd backend && uv run mypy app

# Database migrations
cd backend && bash scripts/prestart.sh  # Run existing migrations
cd backend && uv run alembic revision --autogenerate -m "description"  # Generate new migration
cd backend && uv run alembic upgrade head  # Apply migrations
cd backend && uv run alembic downgrade -1  # Rollback one migration

# Start backend dev server (without Docker)
cd backend && uv run fastapi dev app/main.py
```

### Frontend Development
```bash
# Install dependencies
cd frontend && npm install

# Start dev server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Lint and auto-fix code (uses Biome)
cd frontend && npm run lint

# Generate TypeScript client from backend OpenAPI
cd frontend && npm run generate-client

# Run Playwright E2E tests
cd frontend && npx playwright test
cd frontend && npx playwright test --ui  # Interactive mode
cd frontend && npx playwright test tests/login.spec.ts  # Specific test

# Preview production build
cd frontend && npm run preview
```

### Docker Development
```bash
# Start all services
docker compose up -d

# Start with rebuild
docker compose up -d --build

# View logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db

# Stop all services
docker compose down

# Reset database (careful!)
docker compose down -v  # Removes volumes
docker compose up -d

# Access running container
docker compose exec backend bash
docker compose exec db psql -U postgres -d app

# Service URLs:
# - Frontend: http://localhost
# - Backend API: http://localhost/api
# - API Documentation: http://localhost/docs
# - Adminer (DB UI): http://localhost:8080
```

## Architecture Overview

### Backend Architecture

The backend follows a modular, layered architecture:

```
backend/app/
├── api/
│   ├── deps.py          # Dependency injection (auth, db sessions)
│   ├── main.py          # API router aggregation
│   └── routes/          # Endpoint definitions
│       ├── users.py     # User management endpoints
│       ├── items.py     # Generic CRUD example
│       ├── login.py     # Authentication endpoints
│       └── utils.py     # Utility endpoints
├── core/
│   ├── config.py        # Settings with Pydantic
│   ├── security.py      # JWT, password hashing
│   └── db.py           # Database engine setup
├── models.py           # SQLModel definitions
├── crud.py            # Database operations
└── main.py           # FastAPI app initialization
```

**Key Backend Patterns**:
- **Dependency Injection**: All routes use `SessionDep` for database access and `CurrentUser` for authentication
- **Model Inheritance**: Base models → Create/Update schemas → Database models → Public response models
- **UUID Primary Keys**: All tables use UUID v4 for primary keys
- **Async Support**: FastAPI runs async but uses sync SQLModel operations (can be optimized)

### Frontend Architecture

React SPA with modern tooling:

```
frontend/src/
├── client/             # Auto-generated from OpenAPI
│   ├── schemas.gen.ts  # TypeScript types
│   ├── sdk.gen.ts      # API client methods
│   └── core/          # HTTP client setup
├── components/
│   ├── Admin/         # User management UI
│   ├── Common/        # Navbar, Sidebar, etc.
│   ├── Items/         # CRUD example UI
│   └── ui/           # Chakra UI primitives
├── routes/           # TanStack Router pages
├── hooks/           # React Query wrappers
└── main.tsx        # App entry point
```

**Key Frontend Patterns**:
- **Type-Safe API Client**: Generated from OpenAPI spec, ensures frontend/backend contract
- **Optimistic Updates**: React Query mutations with optimistic UI updates
- **Protected Routes**: TanStack Router guards check authentication before rendering
- **Component Architecture**: Presentational components in `ui/`, container components with business logic

### Database Schema

The project has two parallel data models:

1. **Core Application Models** (from template):
   - `User`: Authentication and user management
   - `Item`: Example CRUD entity with owner relationship

2. **Shrimp Production Models** (domain-specific):
   - Production tracking: `camaroneras`, `corridas`, `aguaje`
   - Sampling: `gramaje_cabecera`, `gramaje_detalle`
   - Processing: `liquidacion_cabecera`, `liquidacion_detalle`
   - Orders: `orden_produccion_c`, `orden_produccion_d`
   - Transport: `guia`, `guia_transporte`
   - Classification: `camaron_talla`, `camaron_tipo`, `camaron_clase`

### Authentication & Security

- **JWT Authentication**: Access tokens expire in 8 days (configurable)
- **Password Security**: Bcrypt hashing with Passlib
- **Role-Based Access**: `is_superuser` flag for admin operations
- **CORS Configuration**: Configured via `BACKEND_CORS_ORIGINS` environment variable
- **Protected Endpoints**: Use `CurrentUser` or `get_current_active_superuser` dependencies

### API Client Generation Flow

1. Backend defines models and endpoints using FastAPI
2. FastAPI generates OpenAPI schema at `/api/openapi.json`
3. Frontend's `openapi-ts.config.ts` points to this schema
4. Running `npm run generate-client` creates TypeScript client
5. Client provides type-safe methods like `UsersService.readUsers()`

### Testing Strategy

**Backend Testing**:
- Test database separate from development database
- Fixtures in `conftest.py` for common test data
- Test client with authentication helpers
- Categories: API routes, CRUD operations, utilities

**Frontend Testing**:
- Playwright for E2E testing
- Tests run against dev server on port 5173
- Test user credentials from environment variables

### Environment Configuration

Key environment variables:
- `PROJECT_NAME`: Application name
- `SECRET_KEY`: JWT signing key (generate with `openssl rand -hex 32`)
- `FIRST_SUPERUSER`: Initial admin email
- `FIRST_SUPERUSER_PASSWORD`: Initial admin password
- `POSTGRES_SERVER`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Database connection
- `SMTP_*`: Email configuration for password recovery
- `SENTRY_DSN`: Error tracking in production

### Adding Domain Features

When implementing shrimp production features:

1. **Check PROJECT_INDEX.md**: Review existing database schema and API structure
2. **Create Domain Models**: Add SQLModel classes for production entities
3. **Add CRUD Operations**: Implement database operations for domain models
4. **Create API Routes**: New route files in `backend/app/api/routes/`
5. **Update Router**: Include new routes in `backend/app/api/main.py`
6. **Generate Client**: Run `npm run generate-client` to update TypeScript types
7. **Build UI Components**: Create React components for domain features
8. **Add Routes**: Define new pages in `frontend/src/routes/`
9. **Write Tests**: Add test coverage for new endpoints
10. **Update Documentation**: Keep PROJECT_INDEX.md updated with new features

### Working with Documentation

**Reference Hierarchy**:
1. `PROJECT_INDEX.md` - Primary reference for project structure and features
2. `CLAUDE.md` - Technical implementation details and commands
3. `docs/descripcion-del-proyecto.md` - Domain-specific business logic
4. Other documentation as needed

**When answering questions**:
- Always check PROJECT_INDEX.md first for structural information
- Use the database schema section for understanding data relationships
- Reference the API endpoints section for available operations
- Consult the architecture overview for system design decisions