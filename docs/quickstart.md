# Quickstart Guide

Get AutoPR up and running in your development environment.

## 📦 Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install autopr
```

### Option 2: Install from Source

```bash
git clone https://github.com/surenkotian/AutoPR.git
cd AutoPR
pip install -e .
```

## ⚙️ Initial Setup

1. **Initialize AutoPR configuration:**

```bash
pr-ai init
```

This creates:
- `.autopr.json` - Configuration file
- `.env.example` - Environment variables template

2. **Configure your LLM provider:**

```bash
pr-ai configure
```

Choose your provider and enter API keys:
- **OpenAI**: Requires `OPENAI_API_KEY`
- **Anthropic**: Requires `ANTHROPIC_API_KEY`
- **Stub**: No API key needed (offline mode)

## 🚀 Basic Usage

### Generate PR Description

```bash
pr-ai gen --diff "+ def add(a, b): return a + b" --commits "feat: add math helper"
```

**Output:**
```
🔍 Analyzing diff...
✔ Identified 1 changed files
🔬 Running static analysis...
✔ Found 0 analysis items
🤖 Generating PR description...
✅ PR description generated
📝 Title: feat: add math helper function
📋 Summary: Adds a simple addition helper function...
🚀 PR submitted: #17
🌐 Opening in browser...
```

### Review Code Changes

```bash
pr-ai review --diff "print('debug')" --test-log pytest.log
```

**Output:**
```
🔍 Analyzing diff...
🔬 Running static analysis...
🤖 Generating AI review...
✅ Review completed
📊 Confidence: 85.0%
🔍 Findings: 2
```

### Check System Health

```bash
pr-ai doctor
```

**Output:**
```
✓ Python version >= 3.10
✓ Git installed
✓ Directory is a git repository
✓ OPENAI_API_KEY available
✓ Directory is writable

✓ All systems ready!
```

## 🔧 Advanced Usage

### With Git Integration

```bash
# Generate PR from current changes
git add .
pr-ai gen

# Review staged changes
pr-ai review

# Get reviewer suggestions
pr-ai suggest-reviewers
```

### CI/CD Integration

```bash
# Parse test results
pr-ai ci-parse --log test-results.log

# Compare coverage
pr-ai coverage-compare --before coverage_before.txt --after coverage_after.txt
```

## 🌐 API Usage

Start the web API server:

```bash
uvicorn autopr.main:app --reload --port 8000
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## 🐛 Troubleshooting

### Common Issues

**"Command not found: pr-ai"**
- Ensure AutoPR is installed: `pip install autopr`
- Check your PATH includes Python scripts directory

**"API key not found"**
- Run `pr-ai configure` to set up your API keys
- Or use `pr-ai mock` for offline testing

**"Git repository not found"**
- Ensure you're in a git repository directory
- Run `git init` if needed

### Debug Mode

Enable debug logging:

```bash
export AUTOPR_DEBUG=true
pr-ai gen --diff "test"
```

## 📚 Next Steps

- [CLI Reference](cli-reference.md) - Complete command documentation
- [Demo Repository](demo-repo.md) - Try AutoPR live
- [GitHub Actions Setup](github-actions.md) - CI/CD integration