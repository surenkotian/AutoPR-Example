# CLI Reference

Complete reference for all AutoPR command-line commands.

## Global Options

All commands support:

- `--help`: Show help message
- `--version`: Show version information

## 🔧 Setup Commands

### `autopr init`

Initialize AutoPR configuration in the current directory.

```bash
autopr init
```

**Creates:**
- `.autopr.json` - Configuration file
- `.env.example` - Environment template

### `autopr configure`

Interactive configuration setup.

```bash
autopr configure
```

**Prompts for:**
- LLM provider selection (openai/anthropic/stub)
- API key input (if not stub)
- Sync/async mode preference

### `autopr doctor`

Check system health and requirements.

```bash
autopr doctor
```

**Checks:**
- Python version ≥ 3.8
- Git installation
- Git repository presence
- API key availability
- Directory write permissions

### `autopr hooks install`

Install pre-commit hooks.

```bash
autopr hooks install
```

**Creates:**
- `.git/hooks/pre-commit` - Runs static analysis and tests

### `autopr mock`

Switch to offline stub provider.

```bash
autopr mock
```

**Use case:** Offline demos and testing without API keys.

## 🚀 Core Commands

### `autopr gen`

Generate PR title and description.

```bash
autopr gen [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff or snippet [required]
- `--commits TEXT`: Commit messages (can specify multiple)
- `--issue TEXT`: Linked issue ID or URL
- `--open-browser`: Open PR in browser after generation

**Example:**
```bash
autopr gen \
  --diff "+ def add(a, b): return a + b" \
  --commits "feat: add math helper" \
  --issue "#123" \
  --open-browser
```

### `autopr review`

Perform AI-assisted code review.

```bash
autopr review [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff or snippet [required]
- `--commits TEXT`: Commit messages to consider
- `--issue TEXT`: Issue description for context
- `--test-log PATH`: Path to pytest log file
- `--coverage-before PATH`: Before coverage report
- `--coverage-after PATH`: After coverage report

**Example:**
```bash
autopr review \
  --diff "print('debug')" \
  --test-log results/pytest.log \
  --coverage-before coverage_before.txt \
  --coverage-after coverage_after.txt
```

### `autopr analyze`

Run static analysis on code.

```bash
autopr analyze [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff or snippet [required]
- `--lang TEXT`: Language (default: python)

**Example:**
```bash
autopr analyze --diff "+ def foo(): pass" --lang python
```

## 📊 Validation Commands

### `autopr ci-parse`

Parse CI/test logs.

```bash
autopr ci-parse [OPTIONS]
```

**Options:**
- `--log PATH`: Path to log file [required]

**Example:**
```bash
autopr ci-parse --log test-output.log
```

### `autopr coverage-compare`

Compare coverage reports.

```bash
autopr coverage-compare [OPTIONS]
```

**Options:**
- `--before PATH`: Before coverage file [required]
- `--after PATH`: After coverage file [required]

**Example:**
```bash
autopr coverage-compare \
  --before coverage_main.txt \
  --after coverage_pr.txt
```

### `autopr validate-issue`

Check if changes align with issue.

```bash
autopr validate-issue [OPTIONS]
```

**Options:**
- `--issue TEXT`: Issue description [required]
- `--diff TEXT`: Code diff [required]
- `--commits TEXT`: Commit messages

**Example:**
```bash
autopr validate-issue \
  --issue "Fix login bug" \
  --diff "+ if user: login(user)" \
  --commits "fix: handle user login"
```

## 👥 Collaboration Commands

### `autopr suggest-reviewers`

Suggest reviewers based on code changes.

```bash
autopr suggest-reviewers [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff (optional, uses git diff if not provided)

**Example:**
```bash
autopr suggest-reviewers
```

**Output:**
```
👥 Suggested reviewers:
  • alice (15 commits in related files)
  • bob (8 commits in related files)
  • charlie (5 commits in related files)
```

## 📋 Command Summary

| Command | Description | Key Options |
|---------|-------------|-------------|
| `init` | Initialize configuration | - |
| `configure` | Interactive setup | - |
| `doctor` | System health check | - |
| `hooks install` | Install git hooks | - |
| `mock` | Use stub provider | - |
| `gen` | Generate PR description | `--diff`, `--commits`, `--issue` |
| `review` | AI code review | `--diff`, `--test-log`, `--coverage-*` |
| `analyze` | Static analysis | `--diff`, `--lang` |
| `ci-parse` | Parse test logs | `--log` |
| `coverage-compare` | Compare coverage | `--before`, `--after` |
| `validate-issue` | Issue alignment check | `--issue`, `--diff`, `--commits` |
| `suggest-reviewers` | Reviewer suggestions | `--diff` |

## 🔧 Configuration

### `.autopr.json`

```json
{
  "provider": "openai",
  "repo": "local",
  "mode": "sync"
}
```

### Environment Variables

- `AUTOPR_PROVIDER`: LLM provider (openai/anthropic/stub)
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `AUTOPR_DEBUG`: Enable debug logging (true/false)

## 🚨 Exit Codes

- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: API error
- `4`: File not found