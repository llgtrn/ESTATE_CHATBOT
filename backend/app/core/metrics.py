"""Prometheus metrics for monitoring."""
from prometheus_client import Counter, Gauge, Histogram

# Request metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

# Conversation metrics
conversations_started_total = Counter(
    "conversations_started_total",
    "Total conversations started",
)

conversations_completed_total = Counter(
    "conversations_completed_total",
    "Total conversations completed",
)

conversation_turns_total = Counter(
    "conversation_turns_total",
    "Total conversation turns",
)

conversation_duration_seconds = Histogram(
    "conversation_duration_seconds",
    "Conversation duration in seconds",
)

# LLM metrics
llm_requests_total = Counter(
    "llm_requests_total",
    "Total LLM requests",
    ["model", "status"],
)

llm_request_duration_seconds = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration in seconds",
    ["model"],
)

llm_tokens_used_total = Counter(
    "llm_tokens_used_total",
    "Total tokens used",
    ["model", "token_type"],
)

llm_cost_usd_total = Counter(
    "llm_cost_usd_total",
    "Total LLM cost in USD",
    ["model"],
)

# Brief metrics
briefs_created_total = Counter(
    "briefs_created_total",
    "Total briefs created",
    ["property_type"],
)

briefs_submitted_total = Counter(
    "briefs_submitted_total",
    "Total briefs submitted",
    ["property_type"],
)

# Entity extraction metrics
entities_extracted_total = Counter(
    "entities_extracted_total",
    "Total entities extracted",
    ["entity_type", "method"],
)

# Cache metrics
cache_hits_total = Counter(
    "cache_hits_total",
    "Total cache hits",
    ["cache_type"],
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total cache misses",
    ["cache_type"],
)

# Database metrics
db_queries_total = Counter(
    "db_queries_total",
    "Total database queries",
    ["operation", "table"],
)

db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation", "table"],
)

# Active sessions gauge
active_sessions = Gauge(
    "active_sessions",
    "Number of active sessions",
)

# Error metrics
errors_total = Counter(
    "errors_total",
    "Total errors",
    ["error_type"],
)


def setup_metrics() -> None:
    """Initialize metrics."""
    # Metrics are initialized on import
    pass
