# AutoPR: AI-Powered Pull Request Automation

[![PyPI version](https://badge.fury.io/py/autopr.svg)](https://pypi.org/project/autopr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AutoPR automates the repetitive parts of pull requests for development teams. It writes concise PR titles & descriptions, validates CI/tests, runs deterministic static and lint checks, and provides AI-assisted review summaries.

## ✨ Features

- **🤖 AI-Powered PR Generation**: Automatically generate titles, descriptions, and risk assessments
- **🔍 Intelligent Code Review**: AI-assisted review with findings and confidence scores
- **🛠️ Static Analysis**: AST-based Python code analysis with linting
- **📊 CI/Test Validation**: Parse test logs and compare coverage reports
- **⚡ CLI Tool**: Developer-friendly command-line interface
- **🔧 GitHub Actions Integration**: Automated PR processing workflows
- **📱 Multiple LLM Providers**: Support for OpenAI, Anthropic, and offline stub mode

## 🚀 Quick Example

```bash
# Install
pip install autopr

# Initialize
pr-ai init

# Generate PR description
pr-ai gen --diff "+ def add(a, b): return a + b" --commits "feat: add math helper"

# Review code changes
pr-ai review --diff "print('debug')" --test-log pytest.log
```

## 📖 Documentation Sections

- [Quickstart Guide](quickstart.md) - Get up and running in minutes
- [CLI Reference](cli-reference.md) - Complete command documentation
- [PR Automation](pr-automation.md) - How AutoPR works
- [Demo Repository](demo-repo.md) - Try it live
- [GitHub Actions Setup](github-actions.md) - CI/CD integration
- [Offline Mode](offline-mode.md) - Development without API keys

## 🎯 Use Cases

- **Individual Developers**: Speed up PR creation and get AI review feedback
- **Teams**: Standardize PR quality and reduce review time
- **Open Source**: Automate contributor PR processing
- **CI/CD Pipelines**: Integrate automated PR validation

## 🤝 Contributing

We welcome contributions! See our [GitHub repository](https://github.com/surenkotian/AutoPR) for issues, feature requests, and development setup.

## 📄 License

AutoPR is open source software licensed under the [MIT License](https://github.com/surenkotian/AutoPR/blob/main/LICENSE).