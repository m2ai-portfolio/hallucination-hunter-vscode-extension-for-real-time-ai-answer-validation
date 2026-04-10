"""Reporter: generates inline diagnostic warnings."""

from dataclasses import dataclass
from typing import Optional

from .models import CheckResult


@dataclass
class Diagnostic:
    """An inline diagnostic warning."""

    line: int
    severity: str  # "warning" | "info" | "error"
    message: str
    explanation: str
    fix_suggestion: Optional[str] = None


def generate_diagnostics(result: CheckResult) -> list[Diagnostic]:
    """Convert a CheckResult into a list of Diagnostic objects.

    One diagnostic per lint issue, test failure, or security warning.
    """
    diagnostics: list[Diagnostic] = []

    for issue in result.lint_issues:
        diagnostics.append(
            Diagnostic(
                line=1,
                severity="warning",
                message=issue,
                explanation=f"Lint issue detected: {issue}. This may indicate code quality problems.",
                fix_suggestion="Review and fix the lint issue.",
            )
        )

    for failure in result.test_failures:
        diagnostics.append(
            Diagnostic(
                line=1,
                severity="error",
                message=failure,
                explanation=f"Test failure detected: {failure}. The code may not compile or run correctly.",
                fix_suggestion="Fix the compilation or runtime error.",
            )
        )

    for warning in result.security_warnings:
        diagnostics.append(
            Diagnostic(
                line=1,
                severity="error",
                message=warning,
                explanation=f"Security concern: {warning}. This pattern could be dangerous.",
                fix_suggestion="Avoid using dangerous patterns like eval() or exec().",
            )
        )

    return diagnostics


def format_inline_warning(diagnostic: Diagnostic) -> str:
    """Return a human-readable inline warning string."""
    parts = [
        f"[{diagnostic.severity.upper()}] Line {diagnostic.line}: {diagnostic.message}",
        f"  Explanation: {diagnostic.explanation}",
    ]
    if diagnostic.fix_suggestion:
        parts.append(f"  Suggested fix: {diagnostic.fix_suggestion}")
    return "\n".join(parts)


def should_warn(result: CheckResult, threshold: float) -> bool:
    """Return True if confidence is below threshold."""
    return result.confidence < threshold
