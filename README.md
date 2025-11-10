# Real Estate Chatbot - AI-Powered Lead Qualification

[![CI](https://github.com/your-org/estate-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/estate-chatbot/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/your-org/estate-chatbot/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/estate-chatbot)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready multilingual real estate qualification chatbot powered by LangChain and Google Vertex AI.

## Features

- 🤖 **AI-Powered Conversations**: Leverages Google Gemini 1.5 Flash/Pro for intelligent responses
- 🌍 **Multilingual Support**: Japanese, English, and Vietnamese
- 📊 **99%+ Test Coverage**: Comprehensive testing with pytest
- 🚀 **Production-Ready**: Docker, Cloud Run, and Terraform for infrastructure
- 📈 **Observability**: LangSmith integration, Prometheus metrics, structured logging
- 🔒 **Security**: Content filtering, PII masking, rate limiting
- ⚡ **High Performance**: <2.5s P95 latency, Redis caching, optimized queries

## Architecture

- **Framework**: FastAPI + LangChain + LangGraph
- **LLM**: Google Vertex AI (Gemini 1.5)
- **Database**: PostgreSQL 15 + pgvector
- **Cache**: Redis 7.0
- **Deployment**: Google Cloud Run
- **CI/CD**: GitHub Actions
- **Infrastructure**: Terraform

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry 1.7+
- Docker (optional)
- GCP account (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/estate-chatbot.git
cd estate-chatbot/backend

# Install dependencies
make install

# Or with Poetry directly
poetry install
```

### Configuration

Create a `.env` file in the `backend` directory:

```env
ENVIRONMENT=dev
DEBUG=true
LOG_LEVEL=DEBUG

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chatbot
REDIS_URL=redis://localhost:6379/0

GCP_PROJECT_ID=your-project-id
GCP_REGION=asia-northeast1

LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_TRACING=true
```

### Running Locally

```bash
# Run with auto-reload
make dev

# Or with Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Access the API
open http://localhost:8080/docs
```

## Development

### Testing

```bash
# Run all tests with coverage (99% target)
make test-coverage

# Run only unit tests
make test-unit

# Run integration tests
make test-integration

# Run E2E tests
make test-e2e

# Run load tests
make test-load
```

### Code Quality

```bash
# Lint code
make lint

# Format code
make format

# Type check
make type-check

# Security scan
make security

# Run all checks (CI simulation)
make ci
```

### Docker

```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run

# Development mode with volume mount
make docker-build-dev
make docker-run-dev
```

## Testing Strategy

This project aims for **99% test coverage** following this pyramid:

- **60% Unit Tests**: Fast, isolated component tests
- **25% Integration Tests**: API endpoints, database, cache
- **10% E2E Tests**: Complete user flows (buy, rent, sell)
- **4% Load Tests**: Performance and scalability (1000+ concurrent users)
- **1% Manual Tests**: Edge cases and exploratory testing

### Running Tests

```bash
# All tests with coverage report
poetry run pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=99

# View coverage report
open htmlcov/index.html
```

## CI/CD

### Continuous Integration

On every push/PR:
- ✅ Linting (Ruff, Black, mypy)
- ✅ Security scans (Bandit, Safety)
- ✅ Unit tests
- ✅ Integration tests
- ✅ E2E tests
- ✅ Coverage report (99% required)

### Continuous Deployment

- **Staging**: Auto-deploy from `develop` branch
- **Production**: Manual deployment with approval

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Key Endpoints

```
POST   /api/v1/sessions              Create new session
GET    /api/v1/sessions/{id}         Get session details
DELETE /api/v1/sessions/{id}         Delete session

POST   /api/v1/sessions/{id}/messages   Send message
GET    /api/v1/sessions/{id}/messages   Get message history

GET    /api/v1/briefs/{id}           Get brief
PATCH  /api/v1/briefs/{id}           Update brief
POST   /api/v1/briefs/{id}/submit    Submit brief

GET    /api/v1/glossary/search       Search glossary
GET    /api/v1/glossary/terms/{id}   Get term details
```

## Deployment

### Google Cloud Run

```bash
# Deploy to staging
gcloud run deploy chatbot-api-staging \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated

# Deploy to production
gcloud run deploy chatbot-api-production \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --min-instances 2 \
  --max-instances 100
```

### Terraform

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Plan infrastructure
terraform plan -var-file=environments/production.tfvars

# Apply infrastructure
terraform apply -var-file=environments/production.tfvars
```

## Monitoring

- **LangSmith**: LLM tracing and debugging
- **Prometheus**: Metrics export at `/metrics`
- **Cloud Monitoring**: GCP-native monitoring
- **Structured Logging**: JSON logs to Cloud Logging

## Performance

Target metrics:
- **P95 Latency**: <2.5s
- **Uptime**: 99.9%
- **Cost**: $0.05 per conversation
- **Concurrent Users**: 1000+
- **Cache Hit Rate**: 95%+

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests and ensure 99% coverage
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.example.com
- Issues: https://github.com/your-org/estate-chatbot/issues
- Slack: #estate-chatbot

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [Google Vertex AI](https://cloud.google.com/vertex-ai)
- Deployed on [Google Cloud Run](https://cloud.google.com/run)
