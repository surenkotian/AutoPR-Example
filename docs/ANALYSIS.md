# Static analysis (Python)

This repository includes a lightweight AST-based static analyzer designed to find a small, targeted set of actionable findings inside Python diffs and snippets.

What it looks for
- TODO comments in added lines
- print() debug statements
- unused imports
- comparisons to None using `==` or `!=` (prefer `is`/`is not`)
- functions calling risky APIs (`open`, `requests`, `subprocess`, `socket`) without try/except blocks

How it's used
- Automatically run in the API `/review` endpoint for Python diffs and merged into the reported findings.
- Available as a CLI command: `autopr analyze --diff "..." --lang python`.

Extending it
- This is intentionally conservative and easy to extend — add rules in `src/autopr/analysis.py` and add corresponding tests under `tests/`.
