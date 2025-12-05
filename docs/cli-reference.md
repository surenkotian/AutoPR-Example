# CLI Reference

Complete reference for all AutoPR command-line commands.

## Global Options

All commands support:

- `--help`: Show help message
- `--version`: Show version information

## 🔧 Setup Commands

### `pr-ai init`

Initialize AutoPR configuration in the current directory.

```bash
pr-ai init
```

**Creates:**
- `.autopr.json` - Configuration file
- `.env.example` - Environment template

### `pr-ai configure`

Interactive configuration setup.

```bash
pr-ai configure
```

**Prompts for:**
- LLM provider selection (openai/anthropic/stub)
- API key input (if not stub)
- Sync/async mode preference

### `pr-ai doctor`

Check system health and requirements.

```bash
pr-ai doctor
```

**Checks:**
- Python version ≥ 3.8
- Git installation
- Git repository presence
- API key availability
- Directory write permissions

### `pr-ai hooks install`

Install pre-commit hooks.

```bash
pr-ai hooks install
```

**Creates:**
- `.git/hooks/pre-commit` - Runs static analysis and tests

### `pr-ai mock`

Switch to offline stub provider.

```bash
pr-ai mock
```

**Use case:** Offline demos and testing without API keys.

## 🚀 Core Commands

### `pr-ai gen`

Generate PR title and description.

```bash
pr-ai gen [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff or snippet [required]
- `--commits TEXT`: Commit messages (can specify multiple)
- `--issue TEXT`: Linked issue ID or URL
- `--open-browser`: Open PR in browser after generation

**Example:**
```bash
pr-ai gen \
  --diff "+ def add(a, b): return a + b" \
  --commits "feat: add math helper" \
  --issue "#123" \
  --open-browser
```

### `pr-ai review`

Perform AI-assisted code review.

```bash
pr-ai review [OPTIONS]
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
pr-ai review \
  --diff "print('debug')" \
  --test-log results/pytest.log \
  --coverage-before coverage_before.txt \
  --coverage-after coverage_after.txt
```

### `pr-ai analyze`

Run static analysis on code.

```bash
pr-ai analyze [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff or snippet [required]
- `--lang TEXT`: Language (default: python)

**Example:**
```bash
pr-ai analyze --diff "+ def foo(): pass" --lang python
```

## 📊 Validation Commands

### `pr-ai ci-parse`

Parse CI/test logs.

```bash
pr-ai ci-parse [OPTIONS]
```

**Options:**
- `--log PATH`: Path to log file [required]

**Example:**
```bash
pr-ai ci-parse --log test-output.log
```

### `pr-ai coverage-compare`

Compare coverage reports.

```bash
pr-ai coverage-compare [OPTIONS]
```

**Options:**
- `--before PATH`: Before coverage file [required]
- `--after PATH`: After coverage file [required]

**Example:**
```bash
pr-ai coverage-compare \
  --before coverage_main.txt \
  --after coverage_pr.txt
```

### `pr-ai validate-issue`

Check if changes align with issue.

```bash
pr-ai validate-issue [OPTIONS]
```

**Options:**
- `--issue TEXT`: Issue description [required]
- `--diff TEXT`: Code diff [required]
- `--commits TEXT`: Commit messages

**Example:**
```bash
pr-ai validate-issue \
  --issue "Fix login bug" \
  --diff "+ if user: login(user)" \
  --commits "fix: handle user login"
```

## 👥 Collaboration Commands

### `pr-ai suggest-reviewers`

Suggest reviewers based on code changes.

```bash
pr-ai suggest-reviewers [OPTIONS]
```

**Options:**
- `--diff TEXT`: Code diff (optional, uses git diff if not provided)

**Example:**
```bash
pr-ai suggest-reviewers
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