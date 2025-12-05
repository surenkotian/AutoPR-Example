# GitHub Actions Setup

Integrate AutoPR into your CI/CD pipeline with GitHub Actions.

## 🚀 Quick Setup

Add this workflow to `.github/workflows/autopr.yml`:

```yaml
name: AutoPR
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  autopr:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run AutoPR
        uses: surenkotian/autopr@v1
        with:
          provider: 'openai'
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          mode: 'sync'
```

## ⚙️ Configuration Options

### Required Secrets

Add to your repository secrets:
- `OPENAI_API_KEY` - For OpenAI GPT models
- `ANTHROPIC_API_KEY` - For Anthropic Claude models

### Action Inputs

| Input | Description | Default | Required |
|-------|-------------|---------|----------|
| `provider` | LLM provider (openai/anthropic/stub) | `openai` | Yes |
| `openai-api-key` | OpenAI API key | - | If using OpenAI |
| `anthropic-api-key` | Anthropic API key | - | If using Anthropic |
| `mode` | Processing mode (sync/async) | `sync` | No |
| `debug` | Enable debug logging | `false` | No |

### Advanced Configuration

```yaml
- name: Run AutoPR
  uses: surenkotian/autopr@v1
  with:
    provider: 'anthropic'
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    mode: 'async'
    debug: 'true'
```

## 📋 Workflow Examples

### Full CI Pipeline

```yaml
name: CI with AutoPR
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  autopr:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Download coverage
        uses: actions/download-artifact@v3
        with:
          name: coverage-report

      - name: Run AutoPR
        uses: surenkotian/autopr@v1
        with:
          provider: 'openai'
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          coverage-before: 'coverage-baseline.xml'
          coverage-after: 'coverage.xml'
```

### Multiple Providers

```yaml
- name: Run AutoPR (OpenAI)
  if: github.event.pull_request.user.login != 'dependabot[bot]'
  uses: surenkotian/autopr@v1
  with:
    provider: 'openai'
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}

- name: Run AutoPR (Stub)
  if: github.event.pull_request.user.login == 'dependabot[bot]'
  uses: surenkotian/autopr@v1
  with:
    provider: 'stub'
```

## 🔧 Custom Workflows

### Conditional Processing

```yaml
name: AutoPR (Selective)
on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - 'src/**'
      - 'tests/**'
      - '!docs/**'

jobs:
  autopr:
    runs-on: ubuntu-latest
    if: contains(github.event.pull_request.labels.*.name, 'autopr')
    steps:
      - uses: actions/checkout@v4
      - name: Run AutoPR
        uses: surenkotian/autopr@v1
        with:
          provider: 'openai'
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
```

### Scheduled Reviews

```yaml
name: Weekly AutoPR Review
on:
  schedule:
    - cron: '0 9 * * 1'  # Mondays at 9 AM
  workflow_dispatch:

jobs:
  review-open-prs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get open PRs
        id: prs
        run: |
          PR_NUMBERS=$(gh pr list --json number --jq '.[].number' | tr '\n' ' ')
          echo "prs=$PR_NUMBERS" >> $GITHUB_OUTPUT

      - name: Review PRs
        run: |
          for pr in ${{ steps.prs.outputs.prs }}; do
            echo "Reviewing PR #$pr"
            # Run AutoPR on each PR
          done
```

## 📊 Output Examples

### PR Comment Format

AutoPR posts comments like:

```
## 🤖 AutoPR Analysis

### 📝 PR Summary
**Title:** feat: add user authentication
**Type:** Feature Addition
**Risk Level:** Low

### 🔍 Code Review
✅ **Confidence:** 94%
**Findings:** 2 minor suggestions

- Consider adding input validation
- Add unit tests for edge cases

### 📊 Test Results
✅ All tests passing
📈 Coverage: +2.3%

### 👥 Suggested Reviewers
- @alice (5 commits in auth module)
- @bob (3 commits in user management)
```

## 🛠️ Troubleshooting

### Common Issues

**"Resource not accessible by integration"**
- Add `pull-requests: write` permission to the job

**"API rate limit exceeded"**
- Use async mode or add delays between requests
- Consider using Anthropic for higher limits

**"Action fails with timeout"**
- Increase job timeout in workflow
- Use stub provider for testing

### Debug Mode

Enable debug logging:

```yaml
- name: Run AutoPR
  uses: surenkotian/autopr@v1
  with:
    provider: 'openai'
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    debug: 'true'
```

## 🔒 Security Considerations

- Store API keys as repository secrets
- Use least-privilege tokens
- Consider IP allowlisting for API providers
- Regularly rotate API keys

## 📈 Monitoring

### Success Metrics

Track:
- PR processing success rate
- Average response time
- User satisfaction scores
- False positive/negative rates

### Logging

Action logs are available in:
- GitHub Actions run logs
- PR comments
- AutoPR debug logs (when enabled)