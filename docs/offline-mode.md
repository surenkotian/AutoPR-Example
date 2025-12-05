# Offline Mode Usage

Use AutoPR without internet access or API keys for development and testing.

## 🧱 Stub Provider

AutoPR includes a deterministic "stub" provider that returns consistent mock responses.

### Benefits

- **No API keys required** - Perfect for development
- **Deterministic output** - Same input always produces same result
- **Fast response times** - No network latency
- **Offline capable** - Works without internet
- **Testing friendly** - Predictable behavior for automated tests

## 🚀 Getting Started

### Switch to Stub Mode

```bash
# Initialize if not done
pr-ai init

# Switch to stub provider
pr-ai mock
```

Or manually edit `.autopr.json`:

```json
{
  "provider": "stub",
  "repo": "local",
  "mode": "sync"
}
```

## 📝 Stub Responses

### PR Generation

**Input:**
```bash
pr-ai gen --diff "+ def hello(): return 'world'" --commits "feat: add greeting"
```

**Output:**
```json
{
  "title": "feat: add greeting function",
  "what_changed": "Added a simple greeting function",
  "why": "To provide basic greeting functionality",
  "files_impacted": ["main.py"],
  "tests": "Add unit tests for the greeting function",
  "risk_level": "low",
  "rollback_plan": "Remove the hello function"
}
```

### Code Review

**Input:**
```bash
pr-ai review --diff "print('debug')"
```

**Output:**
```json
{
  "summary": "Code review completed",
  "findings": [
    {
      "type": "debug",
      "message": "Debug print statement found",
      "severity": "low"
    }
  ],
  "confidence": 0.9
}
```

## 🧪 Testing Scenarios

### Unit Testing

```python
from autopr.cli import generate, review
from click.testing import CliRunner

def test_pr_generation():
    runner = CliRunner()
    result = runner.invoke(generate, [
        '--diff', "+ def test(): pass",
        '--commits', 'feat: add test function'
    ])
    assert result.exit_code == 0
    assert 'feat: add test function' in result.output
```

### Integration Testing

```python
import os
os.environ['AUTOPR_PROVIDER'] = 'stub'

# All AutoPR operations now use stub responses
from autopr.generator import generate_pr_from
result = generate_pr_from("test diff", ["test commit"])
# Returns deterministic mock data
```

## 🔄 Switching Providers

### Development → Production

```bash
# Development (stub)
pr-ai mock

# Production (real API)
pr-ai configure
# Select openai/anthropic and enter API key
```

### Environment-Specific

```bash
# CI/CD - use stub for testing
AUTOPR_PROVIDER=stub pr-ai gen --diff "test"

# Local development - use real API
pr-ai configure  # Sets up real provider
```

## 📊 Stub vs Real Providers

| Feature | Stub | OpenAI | Anthropic |
|---------|------|--------|-----------|
| API Key Required | ❌ | ✅ | ✅ |
| Internet Required | ❌ | ✅ | ✅ |
| Deterministic | ✅ | ❌ | ❌ |
| Response Speed | ⚡ | 🐌 | 🐌 |
| Cost | $0 | 💰 | 💰 |
| Testing | ✅ | ❌ | ❌ |

## 🛠️ Advanced Usage

### Custom Stub Responses

For testing specific scenarios, you can modify the stub provider responses in `src/autopr/providers.py`.

### CI/CD Integration

```yaml
# GitHub Actions
- name: Test AutoPR (Stub)
  run: |
    pr-ai mock
    pr-ai gen --diff "+ test" > pr_output.json
    # Validate JSON structure

- name: Deploy AutoPR (Real)
  run: |
    pr-ai configure --provider openai --key ${{ secrets.API_KEY }}
    # Production deployment
```

### Docker Development

```dockerfile
FROM python:3.11

# Install AutoPR
RUN pip install autopr

# Set stub mode by default
ENV AUTOPR_PROVIDER=stub

# Your application code
COPY . /app
WORKDIR /app

CMD ["pr-ai", "gen", "--diff", "sample diff"]
```

## 🎯 Use Cases

### Development
- Rapid prototyping without API costs
- Testing CLI integration
- Documentation examples

### CI/CD
- Testing AutoPR integration
- Validating workflow configurations
- Performance benchmarking

### Demos
- Live presentations
- Customer showcases
- Training sessions

### Offline Work
- Airplane coding sessions
- Limited connectivity environments
- Cost-conscious development

## 🔄 Limitations

### What Stub Doesn't Do

- **Real AI Analysis** - No intelligent code understanding
- **Dynamic Responses** - Fixed response patterns
- **Cost Tracking** - No API usage monitoring
- **Rate Limiting** - No throttling or quotas

### When to Use Real Providers

- Production deployments
- Actual code review needs
- Learning from AI suggestions
- Complex analysis requirements

## 📚 Next Steps

- [Quickstart](quickstart.md) - Get started with real providers
- [CLI Reference](cli-reference.md) - Complete command documentation
- [Demo Repository](demo-repo.md) - Try AutoPR live