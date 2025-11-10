"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

from app.api.v1 import sessions, messages, briefs, glossary
from app.config import get_settings
from app.core.exceptions import ChatbotException
from app.core.logging import setup_logging
from app.core.metrics import setup_metrics

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Real Estate Chatbot API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # Initialize metrics
    if settings.enable_metrics:
        setup_metrics()
        logger.info("Metrics enabled")

    # Configure logging
    setup_logging(settings.log_level)

    yield

    # Shutdown
    logger.info("Shutting down Real Estate Chatbot API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multilingual real estate qualification chatbot with AI agent",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount Prometheus metrics endpoint
if settings.enable_metrics:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


@app.exception_handler(ChatbotException)
async def chatbot_exception_handler(request, exc: ChatbotException) -> JSONResponse:
    """Handle custom chatbot exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.message, "details": exc.details},
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


# Include routers
app.include_router(sessions.router, prefix=settings.api_v1_prefix, tags=["sessions"])
app.include_router(messages.router, prefix=settings.api_v1_prefix, tags=["messages"])
app.include_router(briefs.router, prefix=settings.api_v1_prefix, tags=["briefs"])
app.include_router(glossary.router, prefix=settings.api_v1_prefix, tags=["glossary"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
