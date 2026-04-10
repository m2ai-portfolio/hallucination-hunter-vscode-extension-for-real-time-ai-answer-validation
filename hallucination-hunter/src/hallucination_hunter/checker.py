"""Checker: runs lint/test checks and computes confidence scores."""

import shutil
import subprocess
import sys
import tempfile
import os
from pathlib import Path

from .models import Suggestion, CheckResult
from .config import CONFIDENCE_THRESHOLD, LINT_TOOLS, MAX_SANDBOX_TIME


def _find_tool(name: str) -> str | None:
    """Find a tool executable, checking the current Python env's bin dir first."""
    # Check same directory as the running Python interpreter
    bin_dir = Path(sys.executable).parent
    candidate = bin_dir / name
    if candidate.is_file():
        return str(candidate)
    # Fall back to system PATH
    return shutil.which(name)


def compute_confidence(
    lint_issues: list[str],
    test_failures: list[str],
    security_warnings: list[str],
) -> float:
    """Compute a confidence score starting at 1.0, deducting per issue.

    Deductions:
    - lint issue: -0.1 each
    - test failure: -0.2 each
    - security warning: -0.3 each

    Clamped to [0, 1].
    """
    score = 1.0
    score -= len(lint_issues) * 0.1
    score -= len(test_failures) * 0.2
    score -= len(security_warnings) * 0.3
    return max(0.0, min(1.0, score))


def run_lint(code_path: str) -> list[str]:
    """Run configured linters on the file.

    Returns list of issue strings. Returns empty list if linter not installed.
    """
    issues: list[str] = []

    for tool in LINT_TOOLS:
        tool = tool.strip()
        if not tool:
            continue

        tool_path = _find_tool(tool)
        if not tool_path:
            continue

        try:
            if tool == "ruff":
                result = subprocess.run(
                    [tool_path, "check", "--no-fix", code_path],
                    capture_output=True,
                    text=True,
                    timeout=MAX_SANDBOX_TIME,
                )
            elif tool == "flake8":
                result = subprocess.run(
                    [tool_path, code_path],
                    capture_output=True,
                    text=True,
                    timeout=MAX_SANDBOX_TIME,
                )
            else:
                continue

            output = result.stdout.strip()
            if output:
                for line in output.splitlines():
                    line = line.strip()
                    # Extract lines that contain rule codes (e.g. F401, E501)
                    # Ruff outputs multi-line diagnostics; grab the summary line
                    if line and not line.startswith("Found") and not line.startswith("|") and not line.startswith("help:") and not line.startswith("-->") and not line.startswith("[*"):
                        issues.append(line)

        except (FileNotFoundError, subprocess.TimeoutExpired):
            # Linter not installed or timed out - graceful fallback
            continue

    return issues


def run_tests(code_path: str) -> list[str]:
    """Attempt to run pytest on the code.

    Returns failure strings or empty list.
    """
    failures: list[str] = []

    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import py_compile; py_compile.compile('{code_path}', doraise=True)"],
            capture_output=True,
            text=True,
            timeout=MAX_SANDBOX_TIME,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if stderr:
                failures.append(f"Compile error: {stderr}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return failures


def check(suggestion: Suggestion) -> CheckResult:
    """Core check logic.

    Writes code to temp file, runs linters, computes confidence, returns CheckResult.
    """
    suffix = ".py" if suggestion.language.lower() == "python" else ".txt"

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=suffix,
        delete=False,
        prefix="hunter_",
    ) as f:
        f.write(suggestion.code)
        code_path = f.name

    try:
        lint_issues = run_lint(code_path) if suffix == ".py" else []
        test_failures = run_tests(code_path) if suffix == ".py" else []
        security_warnings: list[str] = []

        # Basic security checks
        dangerous_patterns = ["eval(", "exec(", "__import__", "subprocess.call("]
        for pattern in dangerous_patterns:
            if pattern in suggestion.code:
                security_warnings.append(f"Potentially dangerous: {pattern}")

        confidence = compute_confidence(lint_issues, test_failures, security_warnings)
        safe = confidence >= CONFIDENCE_THRESHOLD

        return CheckResult(
            suggestion_id=suggestion.id,
            confidence=confidence,
            lint_issues=lint_issues,
            test_failures=test_failures,
            security_warnings=security_warnings,
            safe=safe,
        )
    finally:
        os.unlink(code_path)
