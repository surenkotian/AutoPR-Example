# Demo Repository

Try AutoPR with our ready-to-deploy demo repository.

## 🚀 Quick Demo

1. **Visit the demo repository:**
   [https://github.com/surenkotian/AutoPR-Example](https://github.com/surenkotian/AutoPR-Example)

2. **Create a test PR:**
   - Fork the repository
   - Make a small code change
   - Create a pull request

3. **Watch AutoPR in action:**
   - The GitHub Action will automatically run
   - AutoPR posts a comment with analysis
   - See PR generation, review, and suggestions

## 📋 Demo Features

### Sample Code
- Python calculator application
- Unit tests with pytest
- GitHub Actions CI pipeline

### AutoPR Integration
- Automatic PR processing
- Static analysis results
- AI-generated review comments
- Reviewer suggestions

### Live Results
The demo shows:
- PR title and description generation
- Code review with findings
- Test validation
- Coverage analysis

## 🛠️ Local Demo Setup

Run the demo locally:

```bash
# Clone demo repository
git clone https://github.com/surenkotian/AutoPR-Example.git
cd AutoPR-Example

# Install AutoPR
pip install autopr

# Initialize
autopr init

# Use stub provider for offline demo
autopr mock

# Generate PR for sample changes
autopr gen --diff "+ def multiply(a, b): return a * b"

# Review sample code
autopr review --diff "print('debug')"
```

## 🎬 Demo Scenarios

### Scenario 1: Feature Addition
- Add a new function
- See PR generation with proper categorization
- Review for code quality

### Scenario 2: Bug Fix
- Fix a test failure
- Validate issue alignment
- Check test coverage impact

### Scenario 3: Refactoring
- Improve code structure
- Analyze complexity changes
- Review maintainability improvements

## 📊 Demo Output Examples

### PR Generation
```
🔍 Analyzing diff...
✔ Identified 2 changed files
🔬 Running static analysis...
🤖 Generating PR description...
✅ PR description generated

📝 Title: feat: add multiplication function
📋 Summary: Adds multiply function to calculator module
🚀 PR submitted: #42
```

### Code Review
```
🔍 Analyzing diff...
🔬 Running static analysis...
🤖 Generating AI review...

✅ Review completed
📊 Confidence: 92.0%
🔍 Findings: 1

Summary: Clean implementation with good test coverage
Findings:
- Consider adding type hints for better code documentation
```

## 🔗 Integration Examples

### GitHub Actions
```yaml
name: AutoPR
on: pull_request

jobs:
  autopr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run AutoPR
        uses: surenkotian/autopr@v1
        with:
          provider: 'openai'
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
```

### Local Development
```bash
# Set up environment
autopr init
autopr configure

# Process existing PR
autopr gen --diff "$(git diff origin/main)"
autopr review --diff "$(git diff origin/main)"
```

## 🎯 Learning Objectives

After the demo, you'll understand:
- How AutoPR analyzes code changes
- PR generation quality and formatting
- Code review depth and accuracy
- Integration with development workflows
- Configuration and customization options