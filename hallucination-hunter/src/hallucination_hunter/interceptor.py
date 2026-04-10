"""Interceptor: validates and forwards AI code suggestions."""

from .models import Suggestion, CheckResult
from . import checker


KNOWN_LANGUAGES = {
    "python", "javascript", "typescript", "java", "go", "rust",
    "c", "cpp", "csharp", "ruby", "php", "swift", "kotlin",
}

KNOWN_PROVIDERS = {
    "copilot", "claude", "chatgpt", "gemini", "codewhisperer",
    "tabnine", "cursor", "unknown",
}


def intercept(suggestion: Suggestion) -> Suggestion:
    """Validate a suggestion object.

    Returns the suggestion unchanged if valid.
    Raises ValueError if malformed.
    """
    if not suggestion.code or suggestion.code.strip() == "":
        raise ValueError("Suggestion has empty code")

    if suggestion.language.lower() not in KNOWN_LANGUAGES:
        raise ValueError(
            f"Unknown language: {suggestion.language}. "
            f"Known: {sorted(KNOWN_LANGUAGES)}"
        )

    if suggestion.provider.lower() not in KNOWN_PROVIDERS:
        raise ValueError(
            f"Unknown provider: {suggestion.provider}. "
            f"Known: {sorted(KNOWN_PROVIDERS)}"
        )

    return suggestion


def forward_to_checker(suggestion: Suggestion) -> CheckResult:
    """Validate and forward a suggestion to the checker."""
    validated = intercept(suggestion)
    return checker.check(validated)
