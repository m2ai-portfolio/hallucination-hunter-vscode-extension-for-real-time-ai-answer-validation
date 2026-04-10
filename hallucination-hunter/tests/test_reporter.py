"""Tests for the reporter module."""

from hallucination_hunter.models import CheckResult
from hallucination_hunter import reporter


def test_inline_warning_added():
    """Low-confidence results should generate warning diagnostics."""
    result = CheckResult(
        suggestion_id="s1",
        confidence=0.3,
        safe=False,
        lint_issues=["E501 line too long", "F401 unused import"],
        test_failures=[],
        security_warnings=[],
    )
    diagnostics = reporter.generate_diagnostics(result)

    assert len(diagnostics) > 0
    assert any(d.severity == "warning" for d in diagnostics)
    for d in diagnostics:
        assert d.message != ""
        assert d.explanation != ""


def test_no_warning_for_safe_code():
    """Safe, high-confidence code should not trigger a warning."""
    result = CheckResult(
        suggestion_id="s2",
        confidence=0.95,
        safe=True,
        lint_issues=[],
        test_failures=[],
        security_warnings=[],
    )
    assert reporter.should_warn(result, threshold=0.7) is False
