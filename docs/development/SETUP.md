# Development Setup Guide

Complete guide to setting up the Real Estate Chatbot development environment.

## Prerequisites

- Python 3.11+
- Poetry 1.7+
- Docker & Docker Compose
- PostgreSQL 15 (or use Docker)
- Redis 7.0+ (or use Docker)
- GCP Account (for production deployment)

## Quick Start with Docker Compose

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/your-org/ESTATE_CHATBOT.git
cd ESTATE_CHATBOT

# Start all services
docker-compose up

# API will be available at http://localhost:8080
# PostgreSQL at localhost:5432
# Redis at localhost:6379
```

## Local Development Setup

### 1. Install Dependencies

```bash
cd backend

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 2. Start Database Services

**Option A: Using Docker**
```bash
# Start PostgreSQL with pgvector
docker run -d \
  --name chatbot-postgres \
  -e POSTGRES_USER=chatbot \
  -e POSTGRES_PASSWORD=chatbot_dev_password \
  -e POSTGRES_DB=chatbot \
  -p 5432:5432 \
  pgvector/pgvector:pg15

# Start Redis
docker run -d \
  --name chatbot-redis \
  -p 6379:6379 \
  redis:7-alpine
```

**Option B: Local Installation**
```bash
# Install PostgreSQL 15 with pgvector
# Install Redis 7
```

### 3. Configure Environment

Create `.env` file in `backend/` directory:

```env
# Application
ENVIRONMENT=dev
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql+asyncpg://chatbot:chatbot_dev_password@localhost:5432/chatbot

# Redis
REDIS_URL=redis://localhost:6379/0

# GCP (Optional for local dev)
GCP_PROJECT_ID=your-project-id
GCP_REGION=asia-northeast1

# LangSmith (Optional)
LANGSMITH_API_KEY=your-api-key
LANGSMITH_TRACING=false
```

### 4. Run Database Migrations

```bash
# Run migrations
alembic upgrade head

# Or using make
make migrate
```

### 5. Seed Database (Optional)

```bash
# Seed glossary terms
python scripts/seed_glossary.py
```

### 6. Start Development Server

```bash
# Using Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Or using Make
make dev
```

Server will start at http://localhost:8080

- **API Documentation**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

## Development Workflow

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests
make test-integration

# E2E tests
make test-e2e

# With coverage (99% target)
make test-coverage
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Security scan
make security

# Run all checks (CI simulation)
make ci
```

### Database Operations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current
```

### Docker Operations

```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run

# Development mode with hot-reload
make docker-build-dev
make docker-run-dev
```

## Project Structure

```
backend/
├── app/                      # Application code
│   ├── api/                  # API routes
│   ├── core/                 # Core utilities
│   ├── db/                   # Database models & repos
│   ├── langchain/            # LangChain components
│   ├── services/             # Business logic
│   ├── schemas/              # Pydantic models
│   ├── utils/                # Utility functions
│   ├── config.py             # Settings
│   └── main.py               # Application entry
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   ├── e2e/                  # End-to-end tests
│   └── load/                 # Load tests
├── scripts/                  # Utility scripts
├── pyproject.toml            # Dependencies
└── Dockerfile                # Production image
```

## Testing Strategy

Target: **99% test coverage**

### Coverage Breakdown

- **60% Unit Tests**: Fast, isolated component tests
- **25% Integration Tests**: API, database, cache tests
- **10% E2E Tests**: Complete user flows
- **4% Load Tests**: Performance testing
- **1% Manual**: Edge cases

### Writing Tests

```python
# Unit test example
def test_feature():
    # Arrange
    service = MyService()

    # Act
    result = service.do_something()

    # Assert
    assert result == expected

# Async test example
@pytest.mark.asyncio
async def test_async_feature():
    service = MyAsyncService()
    result = await service.do_something()
    assert result is not None
```

### Test Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.e2e           # End-to-end test
@pytest.mark.slow          # Slow running test
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check connection
psql -h localhost -U chatbot -d chatbot
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
```

### Import Errors

```bash
# Reinstall dependencies
poetry install --no-cache

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

## Useful Commands

```bash
# Shell into Poetry environment
poetry shell

# Update dependencies
make upgrade

# Export requirements.txt
make export-requirements

# Clean build artifacts
make clean

# View logs (Docker Compose)
docker-compose logs -f api
```

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Python Test Explorer
- Docker
- PostgreSQL

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

### PyCharm

1. Set Python interpreter to Poetry environment
2. Enable pytest as test runner
3. Configure code style: Black
4. Enable type checking: mypy

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Environment name | `dev` | No |
| `DEBUG` | Debug mode | `false` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `DATABASE_URL` | PostgreSQL connection URL | - | Yes |
| `REDIS_URL` | Redis connection URL | - | Yes |
| `GCP_PROJECT_ID` | GCP Project ID | - | Production only |
| `LANGSMITH_API_KEY` | LangSmith API key | - | No |

## Next Steps

1. **Read the API documentation**: http://localhost:8080/docs
2. **Check the test suite**: `make test-coverage`
3. **Review the codebase**: Start with `app/main.py`
4. **Try the example flows**: See `tests/e2e/`
5. **Deploy to staging**: See `docs/operations/deployment.md`

## Getting Help

- **Documentation**: `/docs`
- **Issues**: GitHub Issues
- **Slack**: #estate-chatbot channel

## Additional Resources

- [Testing Guide](./testing.md)
- [Deployment Guide](../operations/deployment.md)
- [Architecture Overview](../architecture/system-design.md)
- [API Reference](../api/openapi.yaml)
