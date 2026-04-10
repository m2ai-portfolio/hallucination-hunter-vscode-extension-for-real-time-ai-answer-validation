

# Hallucination Hunter – VSCode extension for real-time AI answer validation

## Overview
Hallucination Hunter is a VSCode extension that monitors AI-generated code suggestions (e.g., from GitHub Copilot, Claude Code, Cursor) and runs lightweight self‑checks in a sandbox. It executes relevant linters, unit tests, and static analysis tools, scores confidence, and flags low‑confidence suggestions with inline explanations so solo developers can catch hallucinations before they break builds.

## Problem Statement
AI‑generated code often contains subtle bugs or calls to nonexistent APIs; solo developers lack time to manually verify each suggestion, leading to wasted debugging cycles and eroded trust in AI assistants.

## Target Audience
Solo developers who use AI code assistants (GitHub Copilot, Claude Code, Cursor) and want to increase trust in AI suggestions while reducing rework.

## Tech Stack
- Python 3.11+ (extension host)
- TypeScript / JavaScript (VSCode API)
- Click (for UI interactions)
- Pytest (test runner invoked in sandbox)
- Ruff or Flake8 (linting)
- Bandit (security lint)
- MyPy (type checking)

## Environment Setup
### Prerequisites
- Python 3.11 installed and on PATH
- Node.js ≥18 (for VSCode webview)
- Git (to fetch sample repos for sandbox tests)

### Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| HUNTER_SANDBOX_DIR | `~/.hallucination-hunter/sandbox` | Directory where temporary test sandboxes are created |
| HUNTER_CONFIDENCE_THRESHOLD | `0.7` | Minimum confidence score to consider a suggestion safe |
| HUNTER_LINT_TOOLS | `ruff,flake8` | Comma‑separated list of linters to run |
| HUNTER_TEST_FRAMEWORK | `pytest` | Test framework used for self‑check |
| HUNTER_MAX_SANDBOX_TIME | `30` | Seconds before a sandbox is killed |

## Architecture
The extension consists of three loosely‑coupled components that each fit in a single iteration of the builder’s 5‑iteration budget:

1. **Interceptor** – Hooks into the Copilot/Claude/Cursor suggestion stream, receives the proposed code snippet, and forwards it to the Checker.
2. **Checker** – Spins up a temporary sandbox, runs the selected linters and test framework, collects results, computes a confidence score (0–1), and returns a verdict.
3. **Reporter** – Decorates the original suggestion in the editor with inline diagnostics (warnings, info, explanations) based on the verdict.

Each component can be implemented, unit‑tested, and integrated within one of the five iterations allocated to the builder.

## Core Features
* **Real‑time interception** – Captures AI suggestions as they appear and streams them to the checker without noticeable latency.
* **Sandboxed self‑check** – Executes linting, type checking, and unit tests in an isolated, ephemeral container to avoid polluting the workspace.
* **Confidence‑based reporting** – Scores the safety of a suggestion, shows inline warnings only when confidence falls below the threshold, and provides a quick‑fix link when applicable.

## Data Models
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Suggestion(BaseModel):
    """Represents a single AI‑generated code suggestion."""
    id: str = Field(..., description="Unique identifier from the provider")
    language: str = Field(..., description="Programming language of the snippet")
    code: str = Field(..., description="The suggested code block")
    provider: str = Field(..., description="Copilot, Claude, Cursor, etc.")
    timestamp: str = Field(..., description="When the suggestion was received")

class CheckResult(BaseModel):
    """Outcome of running the self‑check sandbox."""
    suggestion_id: str = Field(..., description="Links back to the original Suggestion")
    confidence: float = Field(..., ge=0, le=1, description="Score where 1.0 is fully safe")
    lint_issues: List[str] = Field(..., default_factory=list, description="Messages from linters")
    test_failures: List[str] = Field(..., default_factory=list, description="Pytest failures, if any")
    security_warnings: List[str] = Field(..., default_factory=list, description="Output from bandit")
    safe: bool = Field(..., description="Derived from confidence >= threshold")
```

## File Structure
```
hallucination-hunter/
├─ .vscode/
│   └─ launch.json
├─ src/
│   ├─ interceptor.ts
│   ├─ checker.ts
│   └─ reporter.ts
├─ tests/
│   ├─ test_interceptor.py
│   ├─ test_checker.py
│   └─ test_reporter.py
├─ sandbox/
│   └─ Dockerfile   # used by Checker to spawn ephemeral containers
├─ pyproject.toml
├─ README.md
└─ LICENSE
```
* The `tests/` directory contains at least two test files (`test_*.py`) for each module, satisfying the requirement for test artifacts.

## Test Plan
- `tests/test_interceptor.py::test_intercept_valid_suggestion` → receives a well‑formed suggestion object and passes it unchanged.
- `tests/test_checker.py::test_run_lint_and_tests` → starts a sandbox, invokes `ruff` and `pytest`, asserts that the returned CheckResult contains expected lint issue strings and a confidence < 0.7 for buggy code.
- `tests/test_reporter.py::test_inline_warning_added` → opens a document with low‑confidence suggestion, verifies that a diagnostic warning with explanation appears inline.
Each test is a proper pytest function with assertions; there are at least five test functions total across the three modules.

## Success Criteria
- **Works correctly**: The extension flags every AI‑generated suggestion whose post‑check confidence is below the configurable threshold with an inline warning that includes a short explanation and, when available, a one‑click fix link.
- **No false positives on clean code**: When the sandbox runs on a known‑good snippet (e.g., a std‑library helper), the confidence score is ≥ threshold and no warning is displayed.
- **Performance**: Intercept‑to‑report latency stays under 200 ms for typical suggestions; sandbox spin‑up and tear‑down stays under the configurable `HUNTER_MAX_SANDBOX_TIME` seconds.

## Constraints & Notes
- No external API calls – all processing (linting, type checking, test execution) is performed locally inside the sandbox; the extension never contacts OpenAI, Anthropic, Google, Slack, or GitHub APIs for verification.
- Target: working MVP that can be demonstrated after the builder’s 5 iterations.
- Prioritize “works correctly” over “feature complete” – the essential goal is to catch hallucinations reliably; extra polish (themes, settings UI, telemetry) is optional.