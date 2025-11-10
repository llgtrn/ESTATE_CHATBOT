.PHONY: help install test test-unit test-integration test-e2e test-coverage lint format type-check security clean run dev docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies with Poetry
	poetry install

test: ## Run all tests
	poetry run pytest -v

test-unit: ## Run unit tests only
	poetry run pytest tests/unit/ -v --cov=app --cov-report=term-missing

test-integration: ## Run integration tests only
	poetry run pytest tests/integration/ -v -m integration

test-e2e: ## Run E2E tests only
	poetry run pytest tests/e2e/ -v -m e2e

test-coverage: ## Run tests with coverage report (99% target)
	poetry run pytest \
		tests/unit/ \
		tests/integration/ \
		-v \
		--cov=app \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-fail-under=99

test-load: ## Run load tests with Locust
	poetry run locust -f tests/load/locustfile.py --host=http://localhost:8080

lint: ## Run linter (Ruff)
	poetry run ruff check .

format: ## Format code with Black
	poetry run black .

format-check: ## Check code formatting
	poetry run black --check .

type-check: ## Run type checker (mypy)
	poetry run mypy app/

security: ## Run security checks
	poetry run bandit -r app/ -f screen
	poetry run safety check

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*.coverage' -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

run: ## Run the application
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

dev: ## Run in development mode with auto-reload
	poetry run uvicorn app.main:app --reload --log-level debug --host 0.0.0.0 --port 8080

docker-build: ## Build Docker image
	docker build -t real-estate-chatbot:latest .

docker-build-dev: ## Build development Docker image
	docker build -f Dockerfile.dev -t real-estate-chatbot:dev .

docker-run: ## Run Docker container
	docker run -p 8080:8080 real-estate-chatbot:latest

docker-run-dev: ## Run development Docker container
	docker run -p 8080:8080 -v $(PWD):/app real-estate-chatbot:dev

ci: lint format-check type-check test-coverage security ## Run all CI checks locally

pre-commit: format lint type-check ## Run pre-commit checks

shell: ## Open Poetry shell
	poetry shell

upgrade: ## Upgrade dependencies
	poetry update

lock: ## Update lock file
	poetry lock

export-requirements: ## Export requirements.txt
	poetry export -f requirements.txt --output requirements.txt --without-hashes
