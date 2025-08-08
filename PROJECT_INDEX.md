# Sistema Nómina y Costos - Project Documentation Index

## 📋 Overview

**Project Name**: Sistema Nómina y Costos  
**Base Template**: FastAPI Full-Stack Template  
**Architecture**: Full-stack web application with FastAPI backend and React frontend  
**Database**: PostgreSQL 16.9  
**Primary Domain**: Shrimp farming production management system  

## 🏗️ Architecture

### Technology Stack

#### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: PostgreSQL 16.9
- **Authentication**: JWT tokens
- **Validation**: Pydantic
- **Testing**: Pytest
- **Migration**: Alembic

#### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **UI Library**: Chakra UI
- **Routing**: TanStack Router
- **API Client**: Auto-generated from OpenAPI
- **Testing**: Playwright (E2E)

#### DevOps
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Traefik
- **CI/CD**: GitHub Actions
- **Deployment**: Railway, DigitalOcean, AWS support

## 📁 Project Structure

```
sistema-nomina-costos/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/                # API routes and endpoints
│   │   │   ├── routes/         # Individual route modules
│   │   │   │   ├── users.py   # User management endpoints
│   │   │   │   ├── items.py   # Item CRUD endpoints
│   │   │   │   ├── login.py   # Authentication endpoints
│   │   │   │   ├── utils.py   # Utility endpoints
│   │   │   │   └── private.py # Private/internal endpoints
│   │   │   ├── deps.py         # Dependencies and security
│   │   │   └── main.py         # API router configuration
│   │   ├── core/               # Core configuration
│   │   │   ├── config.py      # Settings management
│   │   │   ├── security.py    # Password hashing, JWT
│   │   │   └── db.py          # Database connection
│   │   ├── alembic/            # Database migrations
│   │   ├── tests/              # Test suite
│   │   ├── models.py           # SQLModel database models
│   │   ├── crud.py             # Database operations
│   │   ├── utils.py            # Utility functions
│   │   └── main.py             # Application entry point
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── client/             # Auto-generated API client
│   │   ├── components/         # React components
│   │   │   ├── Admin/          # Admin panel components
│   │   │   ├── Common/         # Shared components
│   │   │   ├── Items/          # Item management
│   │   │   ├── UserSettings/  # User profile management
│   │   │   └── ui/             # UI primitives
│   │   ├── routes/             # Page routes
│   │   ├── hooks/              # Custom React hooks
│   │   └── routeTree.gen.ts    # Generated route tree
├── docs/                       # Documentation
│   └── descripcion-del-proyecto.md # Detailed project description
├── docker-compose.yml          # Docker services configuration
├── docker-compose.override.yml # Local development overrides
├── .env                        # Environment variables
└── CLAUDE.md                   # Claude Code assistant guide
```

## 🗄️ Database Schema

### Core Application Models (FastAPI Template)

#### User Model
- **Table**: `user`
- **Fields**:
  - `id` (UUID, PK)
  - `email` (unique, indexed)
  - `hashed_password`
  - `full_name`
  - `is_active`
  - `is_superuser`
- **Relationships**: One-to-Many with Items

#### Item Model
- **Table**: `item`
- **Fields**:
  - `id` (UUID, PK)
  - `title`
  - `description`
  - `owner_id` (FK → User)
- **Relationships**: Many-to-One with User

### Shrimp Production Models (Domain-Specific)

#### Production Tables
- **aguaje**: Marine tide records
- **alimentacion_cabecera**: Feeding planning header
- **alimentacion_detalle**: Feeding planning details
- **camaroneras**: Shrimp farms and ponds hierarchy
- **corridas**: Production runs per sector

#### Classification Tables
- **camaron_clase**: Shrimp class (ENTERO, etc.)
- **camaron_talla**: Shrimp sizes (20/30, 40/50, etc.)
- **camaron_tipo**: Shrimp types
- **camaron_talla_tipo**: Size-type relationships
- **colores**: Color classifications

#### Sampling & Harvest
- **gramaje_cabecera**: Growth sampling headers
- **gramaje_detalle**: Sampling details by size
- **guia**: Transport guides
- **guia_detalle**: Guide details
- **guia_transporte**: Transport information

#### Processing & Orders
- **liquidacion_cabecera**: Settlement headers
- **liquidacion_detalle**: Settlement details
- **orden_produccion_c**: Production order headers
- **orden_produccion_d**: Production order details

#### Support Tables
- **cliente**: Customers
- **cliente_destino**: Delivery destinations
- **empacadora**: Packing facilities
- **empresa**: Companies/databases
- **transporte**: Transport providers
- **usuarios**: System users (legacy)

## 🔌 API Endpoints

### Authentication
- `POST /api/login/access-token` - Login and get JWT token
- `POST /api/login/test-token` - Test token validity
- `POST /api/password-recovery/{email}` - Request password reset
- `POST /api/reset-password` - Reset password with token

### User Management
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create user (admin only)
- `GET /api/users/me` - Get current user
- `PATCH /api/users/me` - Update current user
- `PATCH /api/users/me/password` - Update password
- `DELETE /api/users/me` - Delete own account
- `POST /api/users/signup` - Register new user
- `GET /api/users/{user_id}` - Get user by ID
- `PATCH /api/users/{user_id}` - Update user (admin only)
- `DELETE /api/users/{user_id}` - Delete user (admin only)

### Items (Example CRUD)
- `GET /api/items/` - List items
- `POST /api/items/` - Create item
- `GET /api/items/{id}` - Get item
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item

### Utilities
- `POST /api/utils/test-email` - Test email configuration

## 🚀 Development Commands

### Backend
```bash
# Run tests
cd backend && uv run pytest

# Format code
cd backend && uv run bash scripts/format.sh

# Lint code
cd backend && uv run bash scripts/lint.sh

# Generate migration
cd backend && uv run alembic revision --autogenerate -m "description"

# Run migrations
cd backend && bash scripts/prestart.sh
```

### Frontend
```bash
# Start dev server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Generate API client
cd frontend && npm run generate-client

# Run E2E tests
cd frontend && npm run test

# Lint code
cd frontend && npm run lint
```

### Docker
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend

# Rebuild after changes
docker compose build && docker compose up -d
```

## 🔧 Configuration

### Environment Variables
Key environment variables to configure:
- `SECRET_KEY` - JWT secret key
- `FIRST_SUPERUSER` - Admin email
- `FIRST_SUPERUSER_PASSWORD` - Admin password
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_SERVER` - Database host
- `POSTGRES_DB` - Database name
- `SMTP_*` - Email configuration
- `SENTRY_DSN` - Error tracking (optional)

### Access Points
- **Frontend**: http://localhost
- **Backend API**: http://localhost/api
- **API Documentation**: http://localhost/docs
- **Database Admin**: http://localhost:8080 (Adminer)

## 📚 Documentation Files

- `README.md` - Main project overview
- `CLAUDE.md` - Claude Code assistant instructions
- `docs/descripcion-del-proyecto.md` - Detailed shrimp production system description
- `backend/README.md` - Backend-specific documentation
- `frontend/README.md` - Frontend-specific documentation
- `deployment.md` - Deployment instructions
- `development.md` - Development setup guide
- `SECURITY.md` - Security policies

## 🔒 Security Features

- Secure password hashing (bcrypt)
- JWT-based authentication
- Role-based access control (superuser/regular user)
- Email-based password recovery
- Automatic HTTPS with Traefik
- SQL injection protection via SQLModel
- CORS configuration
- Environment-based secrets management

## 🧪 Testing

### Backend Testing
- Unit tests with Pytest
- Test database isolation
- API endpoint testing
- Authentication testing
- CRUD operation testing

### Frontend Testing
- E2E tests with Playwright
- Component testing
- API integration testing
- Cross-browser testing

## 🚢 Deployment

### Supported Platforms
- **Railway**: One-click deployment with Railway button
- **DigitalOcean**: Docker Compose deployment
- **AWS**: EC2/ECS deployment options
- **Custom VPS**: Docker Compose with Traefik

### Production Checklist
1. Change all default passwords
2. Generate new SECRET_KEY
3. Configure SMTP for emails
4. Set up SSL certificates
5. Configure backup strategy
6. Set up monitoring (Sentry)
7. Review security settings
8. Configure CI/CD pipeline

## 📈 Project Status

### Current Implementation
✅ Authentication system  
✅ User management  
✅ Basic CRUD operations  
✅ Docker containerization  
✅ Database migrations  
✅ Frontend scaffolding  

### Domain-Specific Features (In Development)
🔄 Shrimp production tracking  
🔄 Feeding management system  
🔄 Harvest and settlement modules  
🔄 Production order management  
🔄 Multi-company inventory integration  

## 🤝 Contributing

1. Fork or clone the repository
2. Create a feature branch
3. Follow existing code patterns
4. Add tests for new features
5. Update documentation
6. Submit pull request

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check `docs/` folder
- **Claude Code**: Use CLAUDE.md for AI assistance
- **Email Support**: Configure in `.env` file

---

*Last Updated: 2025*  
*Based on FastAPI Full-Stack Template*  
*Enhanced for Shrimp Production Management*