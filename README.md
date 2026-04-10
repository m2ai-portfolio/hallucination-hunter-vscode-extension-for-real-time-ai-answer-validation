

<p align="center">
  <img src="assets/infographic.png" alt="Hallucination Hunter – VSCode extension for real-time AI answer validation" width="800">
</p>

<h3 align="center">REPLACE THIS WITH A ONE-LINE DESCRIPTION (e.g. "Scan dependencies for vulnerabilities without leaving your terminal")</h3>

Hallucination Hunter is a VSCode extension that monitors AI-generated code suggestions (e.g., from GitHub Copilot, Claude Code, Cursor) and runs lightweight self-checks in a sandbox to catch bugs before they break builds. It helps solo developers trust AI assistants by validating suggestions in real time.
$ hallucination-hunter scan
[INFO] Started scanning AI suggestions...
[WARN] Potential hallucination detected: call to non-existent function 'foo_bar' in suggestion from Copilot
```
| Feature | Description |
|---------|-------------|
| Real-time interception | Captures AI-generated code suggestions as they appear and forwards them for immediate validation without noticeable latency. |
| Sandboxed self-check | Runs lightweight linters (e.g., Ruff, Flake8), type checkers (e.g., MyPy), and unit tests (e.g., Pytest) in an isolated, ephemeral container to validate suggestions without affecting the workspace. |
| Confidence-based reporting | Assigns a confidence score (0–1) to each suggestion; triggers inline warnings with explanations only when score < threshold; offers quick‑fix links for fixable issues. |
| Language agnostic | Works with any AI code assistant (GitHub Copilot, Claude Code, Cursor) by intercepting their suggestion streams. |
| Zero external dependencies | All validation (linting, type checking, testing) occurs locally inside the sandbox; no calls to external APIs for verification. |
| Sandbox timeout control | Configurable maximum sandbox lifetime (default 30 seconds) prevents resource hogging and ensures timely cleanup. |
1. Clone the repository: `git clone https://github.com/m2ai-portfolio/hallucination-hunter`
2. Install dependencies: `npm install`
3. Open the project in VSCode: `code hallucination-hunter`
4. Start debugging: Press `F5` or use the Run > Start Debugging menu
**Title**: Detecting an undefined variable in a Copilot suggestion
**Command**: (Triggered automatically when accepting an AI suggestion in VSCode)
**Sample Output**: 
```
[Hallucination Hunter] Warning: Undefined variable 'result' on line 3 of suggested code
```
**Title**: Blocking a call to a non-existent internal API
**Command**: (Upon AI suggestion acceptance)
**Sample Output**:
```
[Hallucination Hunter] Security Warning: Call to non-existent function 'internalApi_v2' blocked
```
**Title**: Auto-correcting a common typo in a suggestion
**Command**: (When confidence is low and issue is fixable)
**Sample Output**:
```
[Hallucination Hunter] Info: Fixed typo: 'recieve' -> 'receive' at line 10
[Hallucination Hunter] Info: Suggestion accepted after fix
```
hallucination-hunter/
├── .vscode/
│   └── launch.json
├── src/
│   ├── interceptor.ts
│   ├── checker.ts
│   └── reporter.ts
├─ tests/
│   ├── test_interceptor.py
│   ├── test_checker.py
│   └── test_reporter.py
├── sandbox/
│   └── Dockerfile   # used by Checker to spawn ephemeral containers
├── pyproject.toml
├── README.md
└─ LICENSE
```
# Key files:
# - src/: Contains the core source code (TypeScript)
# - tests/: Contains unit tests (Python)
# - sandbox/: Contains Dockerfile for ephemeral test containers
# - pyproject.toml: Project configuration and dependencies
# - README.md: This documentation file
# - LICENSE: License terms
| Technology | Purpose |
|----------|---------|
| TypeScript | Extension source code |
| Python | Unit test suite |
| Docker | Sandboxed test containers (for Checker to spawn ephemeral environments) |
## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for submitting pull requests to us.

## How to Contribute

- Fork the repository
- Create a feature branch
- Make your changes
- Test your changes
- Submit a pull request
MIT
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)