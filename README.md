

<p align="center">
  <img src="assets/infographic.png" alt="Hallucination Hunter – VSCode extension for real-time AI answer validation" width="800">
</p>

<h3 align="center">A VSCode extension that, when Copilot or any LLM suggests code, runs a lightweight self-check: executes the code in a sandbox, runs relevant linters/tests, and scores confidence. Flags low-confidence suggestions with explanations, helping solo developers catch hallucinations before they break builds.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
Hallucination Hunter is a VSCode extension that monitors AI‑generated code suggestions, runs them in an isolated sandbox with linters, type checks and unit tests, and returns a confidence score. It is aimed at solo developers who rely on Copilot, Claude, Cursor or similar assistants and want immediate feedback on the safety of each suggestion.

Example usage via the bundled CLI:
```
$ hhunter check --code "def add(a, b): return a + b"
Confidence: 0.96 | Lint: none | Tests: passed
```

## Problem
AI-generated code often contains subtle bugs or nonexistent APIs; solo developers lack time to manually verify each suggestion, leading to wasted debugging cycles and eroded trust in AI assistants.

## Features
| Feature | Description |
|---|---|
| Real‑time interception | Hooks into the suggestion stream of Copilot, Claude, Cursor and forwards snippets instantly to the checker. |
| Sandboxed self‑check | Spins up an ephemeral container to run linting, type checking and unit tests without affecting the workspace. |
| Confidence‑based scoring | Computes a 0‑1 score from lint, test and security results; shows warnings only when below the threshold. |
| Inline diagnostics | Decorates the original suggestion with explanations and a quick‑fix link when confidence is low. |
| Configurable thresholds | Environment variables let you adjust confidence cutoff, sandbox timeout and lint tools. |
| Zero external calls | All verification runs locally; no calls to OpenAI, Anthropic, Google or GitHub APIs. |

## Quick Start
1. Clone the repository:  
   ```bash
   git clone https://github.com/m2ai-portfolio/hallucination-hunter.git
   cd hallucination-hunter
   ```
2. Install the Python package in editable mode:  
   ```bash
   pip install -e .
   ```
3. Launch the extension in VSCode for testing:  
   ```bash
   code .
   ```  
   Press `F5` to start the extension host, then trigger a Copilot suggestion to see the inline confidence badge.

## Examples
**Basic safe suggestion**  
```
$ hhunter check --code "def square(x): return x * x"
Confidence: 0.99 | Lint: none | Tests: passed
```
**Suggestion with lint issue**  
```
$ hhunter check --code "def foo( ):return 1"
Confidence: 0.62 | Lint: missing whitespace after ',' and before ')' | Tests: passed
```
**Suggestion failing a security check**  
```
$ hhunter check --code "import os; os.system('rm -rf /')"
Confidence: 0.08 | Lint: none | Tests: passed | Security: Potential command injection
```

## File Structure
```
Hallucination Hunter – VSCode extension for real-time AI answer validation/
  hallucination-hunter/
    src/                    # Core source code
    tests/                  # Test suite
    pyproject.toml          # Project config & dependencies
    README.md               # This file
  assets/                   # Banner image
  .gitignore
  LICENSE
  spec.md                   # Specification
```

## Tech Stack
| Technology | Purpose |
|---|---|
| Python 3.11+ | Extension host and sandbox logic |
| TypeScript / JavaScript | VSCode API integration |
| Click | Command‑line interface for the checker |
| Pytest | Test framework executed inside the sandbox |
| Ruff / Flake8 | Linting of suggested code |
| MyPy | Type checking |
| Bandit | Security linting |
| Docker (optional) | Underlying sandbox container execution |

## Contributing
Fork the repository, make your changes, run `pytest` to verify, and submit a pull request.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)