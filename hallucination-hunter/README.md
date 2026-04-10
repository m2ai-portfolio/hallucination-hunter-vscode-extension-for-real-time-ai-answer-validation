# Hallucination Hunter

Python MVP for real-time AI answer validation. Implements three core components:

- **Interceptor**: Receives and validates AI code suggestions
- **Checker**: Runs lint/test checks and computes confidence scores
- **Reporter**: Generates inline diagnostic warnings

## Install

```bash
pip install -e ".[dev]"
```

## Test

```bash
pytest tests/ -v
```
