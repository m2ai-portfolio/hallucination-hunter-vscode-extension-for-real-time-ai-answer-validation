"""Pydantic data models for Hallucination Hunter."""

from pydantic import BaseModel, Field


class Suggestion(BaseModel):
    """An AI-generated code suggestion to be validated."""

    id: str
    language: str
    code: str
    provider: str
    timestamp: str


class CheckResult(BaseModel):
    """Result of running checks on a suggestion."""

    suggestion_id: str
    confidence: float = Field(ge=0.0, le=1.0)
    lint_issues: list[str] = Field(default_factory=list)
    test_failures: list[str] = Field(default_factory=list)
    security_warnings: list[str] = Field(default_factory=list)
    safe: bool
