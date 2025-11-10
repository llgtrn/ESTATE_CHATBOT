"""Tests for metrics module."""
import pytest
from prometheus_client import REGISTRY

from app.core.metrics import (
    active_sessions,
    briefs_created_total,
    briefs_submitted_total,
    cache_hits_total,
    cache_misses_total,
    conversation_duration_seconds,
    conversation_turns_total,
    conversations_completed_total,
    conversations_started_total,
    db_queries_total,
    db_query_duration_seconds,
    entities_extracted_total,
    errors_total,
    http_request_duration_seconds,
    http_requests_total,
    llm_cost_usd_total,
    llm_request_duration_seconds,
    llm_requests_total,
    llm_tokens_used_total,
    setup_metrics,
)


class TestMetricsDefinitions:
    """Tests for metrics definitions."""

    def test_http_requests_total_exists(self) -> None:
        """Test http_requests_total metric exists."""
        assert http_requests_total is not None
        assert http_requests_total._name == "http_requests_total"
        assert http_requests_total._type == "counter"

    def test_http_request_duration_seconds_exists(self) -> None:
        """Test http_request_duration_seconds metric exists."""
        assert http_request_duration_seconds is not None
        assert http_request_duration_seconds._name == "http_request_duration_seconds"
        assert http_request_duration_seconds._type == "histogram"

    def test_conversations_started_total_exists(self) -> None:
        """Test conversations_started_total metric exists."""
        assert conversations_started_total is not None
        assert conversations_started_total._name == "conversations_started_total"
        assert conversations_started_total._type == "counter"

    def test_conversations_completed_total_exists(self) -> None:
        """Test conversations_completed_total metric exists."""
        assert conversations_completed_total is not None
        assert conversations_completed_total._name == "conversations_completed_total"

    def test_conversation_turns_total_exists(self) -> None:
        """Test conversation_turns_total metric exists."""
        assert conversation_turns_total is not None
        assert conversation_turns_total._name == "conversation_turns_total"

    def test_conversation_duration_seconds_exists(self) -> None:
        """Test conversation_duration_seconds metric exists."""
        assert conversation_duration_seconds is not None
        assert conversation_duration_seconds._name == "conversation_duration_seconds"

    def test_llm_requests_total_exists(self) -> None:
        """Test llm_requests_total metric exists."""
        assert llm_requests_total is not None
        assert llm_requests_total._name == "llm_requests_total"

    def test_llm_request_duration_seconds_exists(self) -> None:
        """Test llm_request_duration_seconds metric exists."""
        assert llm_request_duration_seconds is not None
        assert llm_request_duration_seconds._name == "llm_request_duration_seconds"

    def test_llm_tokens_used_total_exists(self) -> None:
        """Test llm_tokens_used_total metric exists."""
        assert llm_tokens_used_total is not None
        assert llm_tokens_used_total._name == "llm_tokens_used_total"

    def test_llm_cost_usd_total_exists(self) -> None:
        """Test llm_cost_usd_total metric exists."""
        assert llm_cost_usd_total is not None
        assert llm_cost_usd_total._name == "llm_cost_usd_total"

    def test_briefs_created_total_exists(self) -> None:
        """Test briefs_created_total metric exists."""
        assert briefs_created_total is not None
        assert briefs_created_total._name == "briefs_created_total"

    def test_briefs_submitted_total_exists(self) -> None:
        """Test briefs_submitted_total metric exists."""
        assert briefs_submitted_total is not None
        assert briefs_submitted_total._name == "briefs_submitted_total"

    def test_entities_extracted_total_exists(self) -> None:
        """Test entities_extracted_total metric exists."""
        assert entities_extracted_total is not None
        assert entities_extracted_total._name == "entities_extracted_total"

    def test_cache_hits_total_exists(self) -> None:
        """Test cache_hits_total metric exists."""
        assert cache_hits_total is not None
        assert cache_hits_total._name == "cache_hits_total"

    def test_cache_misses_total_exists(self) -> None:
        """Test cache_misses_total metric exists."""
        assert cache_misses_total is not None
        assert cache_misses_total._name == "cache_misses_total"

    def test_db_queries_total_exists(self) -> None:
        """Test db_queries_total metric exists."""
        assert db_queries_total is not None
        assert db_queries_total._name == "db_queries_total"

    def test_db_query_duration_seconds_exists(self) -> None:
        """Test db_query_duration_seconds metric exists."""
        assert db_query_duration_seconds is not None
        assert db_query_duration_seconds._name == "db_query_duration_seconds"

    def test_active_sessions_exists(self) -> None:
        """Test active_sessions metric exists."""
        assert active_sessions is not None
        assert active_sessions._name == "active_sessions"
        assert active_sessions._type == "gauge"

    def test_errors_total_exists(self) -> None:
        """Test errors_total metric exists."""
        assert errors_total is not None
        assert errors_total._name == "errors_total"


class TestMetricsLabels:
    """Tests for metrics labels."""

    def test_http_requests_total_has_correct_labels(self) -> None:
        """Test http_requests_total has correct labels."""
        assert "method" in http_requests_total._labelnames
        assert "endpoint" in http_requests_total._labelnames
        assert "status_code" in http_requests_total._labelnames

    def test_http_request_duration_has_correct_labels(self) -> None:
        """Test http_request_duration_seconds has correct labels."""
        assert "method" in http_request_duration_seconds._labelnames
        assert "endpoint" in http_request_duration_seconds._labelnames

    def test_llm_requests_total_has_correct_labels(self) -> None:
        """Test llm_requests_total has correct labels."""
        assert "model" in llm_requests_total._labelnames
        assert "status" in llm_requests_total._labelnames

    def test_llm_request_duration_has_correct_labels(self) -> None:
        """Test llm_request_duration_seconds has correct labels."""
        assert "model" in llm_request_duration_seconds._labelnames

    def test_llm_tokens_used_has_correct_labels(self) -> None:
        """Test llm_tokens_used_total has correct labels."""
        assert "model" in llm_tokens_used_total._labelnames
        assert "token_type" in llm_tokens_used_total._labelnames

    def test_llm_cost_has_correct_labels(self) -> None:
        """Test llm_cost_usd_total has correct labels."""
        assert "model" in llm_cost_usd_total._labelnames

    def test_briefs_created_has_correct_labels(self) -> None:
        """Test briefs_created_total has correct labels."""
        assert "property_type" in briefs_created_total._labelnames

    def test_briefs_submitted_has_correct_labels(self) -> None:
        """Test briefs_submitted_total has correct labels."""
        assert "property_type" in briefs_submitted_total._labelnames

    def test_entities_extracted_has_correct_labels(self) -> None:
        """Test entities_extracted_total has correct labels."""
        assert "entity_type" in entities_extracted_total._labelnames
        assert "method" in entities_extracted_total._labelnames

    def test_cache_hits_has_correct_labels(self) -> None:
        """Test cache_hits_total has correct labels."""
        assert "cache_type" in cache_hits_total._labelnames

    def test_cache_misses_has_correct_labels(self) -> None:
        """Test cache_misses_total has correct labels."""
        assert "cache_type" in cache_misses_total._labelnames

    def test_db_queries_has_correct_labels(self) -> None:
        """Test db_queries_total has correct labels."""
        assert "operation" in db_queries_total._labelnames
        assert "table" in db_queries_total._labelnames

    def test_db_query_duration_has_correct_labels(self) -> None:
        """Test db_query_duration_seconds has correct labels."""
        assert "operation" in db_query_duration_seconds._labelnames
        assert "table" in db_query_duration_seconds._labelnames

    def test_errors_total_has_correct_labels(self) -> None:
        """Test errors_total has correct labels."""
        assert "error_type" in errors_total._labelnames


class TestMetricsUsage:
    """Tests for metrics usage patterns."""

    def test_http_requests_can_be_incremented(self) -> None:
        """Test http_requests_total can be incremented."""
        before = http_requests_total.labels(
            method="GET", endpoint="/api/test", status_code="200"
        )._value._value

        http_requests_total.labels(
            method="GET", endpoint="/api/test", status_code="200"
        ).inc()

        after = http_requests_total.labels(
            method="GET", endpoint="/api/test", status_code="200"
        )._value._value

        assert after > before

    def test_conversation_turns_can_be_incremented(self) -> None:
        """Test conversation_turns_total can be incremented."""
        before = conversation_turns_total._value._value
        conversation_turns_total.inc()
        after = conversation_turns_total._value._value

        assert after > before

    def test_conversations_started_can_be_incremented(self) -> None:
        """Test conversations_started_total can be incremented."""
        before = conversations_started_total._value._value
        conversations_started_total.inc()
        after = conversations_started_total._value._value

        assert after > before

    def test_conversations_completed_can_be_incremented(self) -> None:
        """Test conversations_completed_total can be incremented."""
        before = conversations_completed_total._value._value
        conversations_completed_total.inc()
        after = conversations_completed_total._value._value

        assert after > before

    def test_active_sessions_can_be_set(self) -> None:
        """Test active_sessions gauge can be set."""
        active_sessions.set(10)
        assert active_sessions._value._value == 10

        active_sessions.set(20)
        assert active_sessions._value._value == 20

    def test_active_sessions_can_be_incremented(self) -> None:
        """Test active_sessions gauge can be incremented."""
        current = active_sessions._value._value
        active_sessions.inc()
        assert active_sessions._value._value == current + 1

    def test_active_sessions_can_be_decremented(self) -> None:
        """Test active_sessions gauge can be decremented."""
        active_sessions.set(10)
        active_sessions.dec()
        assert active_sessions._value._value == 9

    def test_llm_requests_can_track_success(self) -> None:
        """Test llm_requests_total can track success."""
        before = llm_requests_total.labels(model="gpt-4", status="success")._value._value
        llm_requests_total.labels(model="gpt-4", status="success").inc()
        after = llm_requests_total.labels(model="gpt-4", status="success")._value._value

        assert after > before

    def test_llm_requests_can_track_failure(self) -> None:
        """Test llm_requests_total can track failure."""
        before = llm_requests_total.labels(model="gpt-4", status="error")._value._value
        llm_requests_total.labels(model="gpt-4", status="error").inc()
        after = llm_requests_total.labels(model="gpt-4", status="error")._value._value

        assert after > before

    def test_llm_tokens_can_track_prompt_tokens(self) -> None:
        """Test llm_tokens_used_total can track prompt tokens."""
        llm_tokens_used_total.labels(model="gpt-4", token_type="prompt").inc(100)
        # Just verify it doesn't raise an error

    def test_llm_tokens_can_track_completion_tokens(self) -> None:
        """Test llm_tokens_used_total can track completion tokens."""
        llm_tokens_used_total.labels(model="gpt-4", token_type="completion").inc(200)
        # Just verify it doesn't raise an error

    def test_briefs_created_can_track_by_type(self) -> None:
        """Test briefs_created_total can track by property type."""
        before = briefs_created_total.labels(property_type="buy")._value._value
        briefs_created_total.labels(property_type="buy").inc()
        after = briefs_created_total.labels(property_type="buy")._value._value

        assert after > before

    def test_briefs_submitted_can_track_by_type(self) -> None:
        """Test briefs_submitted_total can track by property type."""
        before = briefs_submitted_total.labels(property_type="rent")._value._value
        briefs_submitted_total.labels(property_type="rent").inc()
        after = briefs_submitted_total.labels(property_type="rent")._value._value

        assert after > before

    def test_entities_extracted_can_track(self) -> None:
        """Test entities_extracted_total can track extractions."""
        before = entities_extracted_total.labels(
            entity_type="budget", method="regex"
        )._value._value

        entities_extracted_total.labels(entity_type="budget", method="regex").inc()

        after = entities_extracted_total.labels(
            entity_type="budget", method="regex"
        )._value._value

        assert after > before

    def test_cache_hits_can_be_tracked(self) -> None:
        """Test cache_hits_total can be tracked."""
        before = cache_hits_total.labels(cache_type="redis")._value._value
        cache_hits_total.labels(cache_type="redis").inc()
        after = cache_hits_total.labels(cache_type="redis")._value._value

        assert after > before

    def test_cache_misses_can_be_tracked(self) -> None:
        """Test cache_misses_total can be tracked."""
        before = cache_misses_total.labels(cache_type="redis")._value._value
        cache_misses_total.labels(cache_type="redis").inc()
        after = cache_misses_total.labels(cache_type="redis")._value._value

        assert after > before

    def test_db_queries_can_be_tracked(self) -> None:
        """Test db_queries_total can be tracked."""
        before = db_queries_total.labels(
            operation="select", table="sessions"
        )._value._value

        db_queries_total.labels(operation="select", table="sessions").inc()

        after = db_queries_total.labels(
            operation="select", table="sessions"
        )._value._value

        assert after > before

    def test_errors_can_be_tracked(self) -> None:
        """Test errors_total can be tracked."""
        before = errors_total.labels(error_type="validation_error")._value._value
        errors_total.labels(error_type="validation_error").inc()
        after = errors_total.labels(error_type="validation_error")._value._value

        assert after > before

    def test_conversation_duration_can_observe(self) -> None:
        """Test conversation_duration_seconds can observe values."""
        # Observe a duration
        conversation_duration_seconds.observe(12.5)
        # Just verify it doesn't raise an error

    def test_http_request_duration_can_observe(self) -> None:
        """Test http_request_duration_seconds can observe values."""
        http_request_duration_seconds.labels(method="POST", endpoint="/api/test").observe(0.25)
        # Just verify it doesn't raise an error

    def test_llm_request_duration_can_observe(self) -> None:
        """Test llm_request_duration_seconds can observe values."""
        llm_request_duration_seconds.labels(model="gpt-4").observe(2.5)
        # Just verify it doesn't raise an error

    def test_db_query_duration_can_observe(self) -> None:
        """Test db_query_duration_seconds can observe values."""
        db_query_duration_seconds.labels(operation="select", table="messages").observe(0.05)
        # Just verify it doesn't raise an error


class TestSetupMetrics:
    """Tests for setup_metrics function."""

    def test_setup_metrics_executes(self) -> None:
        """Test setup_metrics function executes without error."""
        setup_metrics()
        # Function should execute successfully

    def test_setup_metrics_is_idempotent(self) -> None:
        """Test setup_metrics can be called multiple times."""
        setup_metrics()
        setup_metrics()
        setup_metrics()
        # Should not raise any errors


class TestMetricsRegistry:
    """Tests for metrics registration."""

    def test_all_metrics_registered(self) -> None:
        """Test all metrics are registered in Prometheus registry."""
        collector_names = [collector._name for collector in REGISTRY.collect()]

        assert "http_requests_total" in collector_names
        assert "conversations_started_total" in collector_names
        assert "llm_requests_total" in collector_names
        assert "briefs_created_total" in collector_names
        assert "active_sessions" in collector_names
