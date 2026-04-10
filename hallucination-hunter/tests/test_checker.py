"""Tests for the checker module."""

from hallucination_hunter.models import Suggestion, CheckResult
from hallucination_hunter import checker


def test_run_lint_and_tests():
    """Buggy code should produce low confidence and safe=False."""
    suggestion = Suggestion(
        id="buggy1",
        language="python",
        code="import os\nimport sys\nimport json\nimport collections\nimport pathlib\nimport re\nimport io\nimport abc\nimport math\nimport functools\nx = 1",
        provider="copilot",
        timestamp="2026-01-01T00:00:00Z",
    )
    result = checker.check(suggestion)

    assert isinstance(result, CheckResult)
    assert result.suggestion_id == suggestion.id
    assert result.confidence < 0.7
    assert result.safe is False
    assert len(result.lint_issues) > 0 or len(result.test_failures) > 0


def test_clean_code_passes():
    """Clean code should produce high confidence and safe=True."""
    suggestion = Suggestion(
        id="clean1",
        language="python",
        code="def add(a: int, b: int) -> int:\n    return a + b",
        provider="copilot",
        timestamp="2026-01-01T00:00:00Z",
    )
    result = checker.check(suggestion)

    assert isinstance(result, CheckResult)
    assert result.confidence >= 0.7
    assert result.safe is True
