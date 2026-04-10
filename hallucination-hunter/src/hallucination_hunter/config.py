"""Configuration constants for Hallucination Hunter."""

import os


CONFIDENCE_THRESHOLD: float = float(
    os.environ.get("HUNTER_CONFIDENCE_THRESHOLD", "0.7")
)

LINT_TOOLS: list[str] = os.environ.get(
    "HUNTER_LINT_TOOLS", "ruff,flake8"
).split(",")

MAX_SANDBOX_TIME: int = int(
    os.environ.get("HUNTER_MAX_SANDBOX_TIME", "30")
)
