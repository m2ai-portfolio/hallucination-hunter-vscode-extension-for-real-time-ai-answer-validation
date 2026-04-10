"""Tests for the interceptor module."""

import pytest

from hallucination_hunter.models import Suggestion
from hallucination_hunter import interceptor


def test_intercept_valid_suggestion():
    """A well-formed suggestion is returned unchanged."""
    suggestion = Suggestion(
        id="s1",
        language="python",
        code="print('hello')",
        provider="copilot",
        timestamp="2026-01-01T00:00:00Z",
    )
    result = interceptor.intercept(suggestion)
    assert result.id == "s1"
    assert result.language == "python"
    assert result.code == "print('hello')"
    assert result.provider == "copilot"
    assert result.timestamp == "2026-01-01T00:00:00Z"
    assert result is suggestion  # same object returned


def test_intercept_rejects_empty_code():
    """A suggestion with empty code raises ValueError."""
    suggestion = Suggestion(
        id="s2",
        language="python",
        code="",
        provider="copilot",
        timestamp="2026-01-01T00:00:00Z",
    )
    with pytest.raises(ValueError, match="empty"):
        interceptor.intercept(suggestion)
