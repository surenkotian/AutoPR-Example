# Changelog

All notable changes to AutoPR will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0-beta] - 2025-12-05

### Added
- Complete MkDocs documentation site with 7 pages
- Enhanced CLI with interactive prompts using questionary
- Git-based reviewer suggestions
- Pre-commit hook installation
- Offline stub provider for demos
- Comprehensive logging with loguru
- Environment variable persistence fixes
- PyPI package configuration improvements

### Changed
- Improved pyproject.toml with proper metadata and classifiers
- Enhanced console script configuration (autopr + pr-ai)
- Better error handling and user feedback
- Updated README with simplified onboarding

### Fixed
- Environment variable loading and persistence
- Doctor command API key detection
- Configure command .env file handling

### Technical
- Added questionary for interactive CLI
- Implemented structured logging
- Enhanced configuration management
- Improved package distribution setup

## [0.3.0-beta] - 2025-12-05

### Added
- FastAPI backend with /generate and /review endpoints
- CLI tool with 15+ commands
- Static analysis for Python code
- CI/test validation tools
- Multiple LLM provider support (OpenAI, Anthropic, Stub)
- GitHub Actions integration ready
- Comprehensive test suite

### Changed
- Complete architecture overhaul from MVP to production-ready
- Enhanced user experience with progress indicators
- Improved error handling and validation

## [0.2.0-beta] - 2025-12-05

### Added
- Basic PR generation functionality
- Initial CLI commands
- Core LLM integration
- Project scaffolding

### Changed
- Improved documentation and setup instructions

## [0.1.0] - 2025-12-05

### Added
- Initial MVP release
- Basic FastAPI endpoints
- Core functionality proof-of-concept