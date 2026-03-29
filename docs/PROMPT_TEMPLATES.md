# AutoPR Prompt Templates - Examples and Usage

## Overview

This document provides examples of the versioned prompt templates used in AutoPR's enhanced provider architecture. All prompts are designed for deterministic behavior with temperature=0.

## Version Information

**Current Version**: `1.0.0`
**Purpose**: Ensure consistent behavior across different runs and provider updates

## Template Examples

### 1. PR Title Generation

**Template**: `TITLE_PROMPT`
**Purpose**: Generate concise, descriptive PR titles

```python
TITLE_PROMPT = (
    "[PROMPT_VERSION:1.0.0] "
    "You are an assistant that writes concise PR titles. Given a code diff and commit messages, produce a one-line title (max 60 characters).\n"
    "Diff:\n{diff}\n\nCommit messages:\n{commits}\n\nIssue: {issue}\n\n"
    "Return only the title text with no explanation."
)
```

**Example Usage**:
```
Input:
Diff: --- a/src/auth.py
      +++ b/src/auth.py
      @@ -1,3 +1,8 @@
      +import hashlib
      +import secrets
       def authenticate(username, password):
      +    salt = secrets.token_hex(16)
      +    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
           return True

Commits: ["Implement secure password hashing", "Add authentication security"]
Issue: "Add password hashing for security"

Expected Output:
"Add secure password hashing to authentication"
```

### 2. PR Description Generation

**Template**: `PR_DESCRIPTION_PROMPT`
**Purpose**: Generate comprehensive PR descriptions in structured JSON format

```python
PR_DESCRIPTION_PROMPT = (
    "[PROMPT_VERSION:1.0.0] "
    "You are an assistant that writes a detailed PR description as JSON. Given a code diff, commits, and an optional issue, return a JSON object with the following keys: title, what_changed, why, files_impacted (array), tests (string), risk_level (low/medium/high), rollback_plan.\n\n"
    "Diff:\n{diff}\n\nCommits:\n{commits}\n\nIssue: {issue}\n\n"
    "Provide only valid JSON (no surrounding markdown)."
)
```

**Expected JSON Structure**:
```json
{
  "title": "Add secure password hashing to authentication",
  "what_changed": "Implemented PBKDF2 password hashing with salt",
  "why": "Improves security by properly hashing passwords before storage",
  "files_impacted": ["src/auth.py"],
  "tests": "Added unit tests for password hashing functions",
  "risk_level": "low",
  "rollback_plan": "Revert commit to restore previous authentication method"
}
```

### 3. Code Review Analysis

**Template**: `REVIEW_PROMPT`
**Purpose**: Analyze code changes and provide structured feedback

```python
REVIEW_PROMPT = (
    "[PROMPT_VERSION:1.0.0] "
    "You are an automated code reviewer. Given a code diff, return a JSON object describing: summary, findings (array of objects with keys: type, message, severity), and confidence (0.0-1.0).\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)
```

**Expected JSON Structure**:
```json
{
  "summary": "Code review complete - 2 issues found (1 high priority)",
  "findings": [
    {
      "type": "security",
      "message": "Potential code injection risk: eval(user_input)",
      "severity": "high"
    },
    {
      "type": "performance",
      "message": "Inefficient loop - use enumerate() instead",
      "severity": "medium"
    }
  ],
  "confidence": 0.85
}
```

### 4. Issue Alignment Validation

**Template**: `ISSUE_VALIDATION_PROMPT`
**Purpose**: Assess how well code changes address a specific issue

```python
ISSUE_VALIDATION_PROMPT = (
    "[PROMPT_VERSION:1.0.0] "
    "You are an issue alignment validator. Given an issue description and code changes, assess how well the changes address the issue. Return a JSON object with: alignment_score (0.0-1.0), key_matches (array of strings), gaps (array of strings), recommendations (array of strings).\n\n"
    "Issue:\n{issue}\n\nDiff:\n{diff}\n\nCommits:\n{commits}\n\nReturn only valid JSON."
)
```

**Expected JSON Structure**:
```json
{
  "alignment_score": 0.9,
  "key_matches": [
    "JWT token generation",
    "password hashing",
    "user authentication"
  ],
  "gaps": [
    "No implementation details for storing hashed passwords",
    "Lack of error handling for JWT encoding"
  ],
  "recommendations": [
    "Implement a function to securely store hashed passwords in the database.",
    "Add error handling for potential exceptions during JWT token generation.",
    "Consider adding logging for authentication attempts for security auditing."
  ]
}
```

### 5. Enhanced Code Review

**Template**: `ENHANCED_REVIEW_PROMPT`
**Purpose**: Comprehensive code review with detailed analysis

```python
ENHANCED_REVIEW_PROMPT = (
    "[PROMPT_VERSION:1.0.0] "
    "You are an expert code reviewer. Given a code diff, provide a comprehensive review as JSON with: summary, findings (array with type, message, severity, file, line), suggestions (array of improvements), security_notes (array), performance_notes (array), confidence (0.0-1.0).\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)
```

**Expected JSON Structure**:
```json
{
  "summary": "Comprehensive review completed - 3 findings with actionable recommendations",
  "findings": [
    {
      "type": "security",
      "message": "Potential SQL injection in query string construction",
      "severity": "high",
      "file": "src/database.py",
      "line": 45
    }
  ],
  "suggestions": [
    "Consider using parameterized queries to prevent SQL injection",
    "Add input validation for user parameters",
    "Implement connection pooling for better performance"
  ],
  "security_notes": [
    "Validate all user inputs before database operations",
    "Use prepared statements for dynamic queries"
  ],
  "performance_notes": [
    "Consider adding database connection pooling",
    "Implement query result caching for frequently accessed data"
  ],
  "confidence": 0.92
}
```

## Deterministic Behavior

### Temperature Setting
All prompts are designed to work with `temperature=0.0` for:
- **Consistent Outputs**: Same input produces same output
- **Reproducible Results**: Essential for testing and debugging
- **Reliable Behavior**: Predictable responses across runs

### Version Tracking
Each prompt includes version information:
```
[PROMPT_VERSION:1.0.0]
```

This enables:
- **Backward Compatibility**: Track prompt changes over time
- **Testing**: Verify expected behavior with specific versions
- **Migration**: Smooth transitions between prompt versions

## Enhanced Stub Provider

The enhanced stub provider uses these templates to generate realistic outputs even without API access:

### Stub Provider Analysis
```python
def _analyze_changes(self, diff: str) -> Dict[str, Any]:
    """Analyze diff to extract meaningful information."""
    files = self._extract_files_from_diff(diff)
    
    analysis = {
        "files_changed": len(files),
        "has_tests": any("test" in f.lower() for f in files),
        "has_docs": any("doc" in f.lower() or "readme" in f.lower() for f in files),
        "complexity": "high" if len(files) > 5 else "medium" if len(files) > 2 else "low"
    }
    
    return analysis, files
```

### Stub Security Analysis
The stub provider performs static analysis for common issues:
- **Security**: `eval()`, `exec()`, hardcoded secrets
- **Performance**: Inefficient loops, redundant operations
- **Code Quality**: TODO/FIXME comments, debug code
- **Error Handling**: Bare except clauses

## Usage Examples

### Basic Usage
```python
from autopr.llm import llm

# Generate PR title
title = llm.generate_pr_title(diff, commits, issue)

# Generate PR description
description = llm.generate_pr_description(diff, commits, issue)

# Review code
review = llm.review_code(diff)
```

### Issue Validation
```python
from autopr.issue_validator import comprehensive_issue_alignment

# Comprehensive validation with both heuristic and LLM analysis
result = comprehensive_issue_alignment(issue_text, diff, commits)

print(f"Alignment Score: {result['llm']['alignment_score']}")
print(f"Recommendation: {result['recommendation']}")
```

### Provider Switching
```python
from autopr.providers import create_provider

# Create specific provider
openai_provider = create_provider("openai")
anthropic_provider = create_provider("anthropic")
stub_provider = create_provider("stub")

# Environment-based selection (default)
llm = create_provider()  # Uses AUTOPR_PROVIDER env var
```

## Best Practices

### 1. **Consistent Input Format**
- Always provide structured diff format
- Include relevant commit messages
- Specify issues when available

### 2. **Error Handling**
```python
try:
    result = llm.generate_pr_description(diff, commits, issue)
except ProviderError as e:
    print(f"Provider error: {e}")
    # Fallback to stub or alternative provider
```

### 3. **Testing with Stub**
```python
# Use stub provider for deterministic testing
stub = create_provider("stub")
result = stub.generate_pr_title(diff, commits, issue)
# Result will be consistent across runs
```

### 4. **Version Awareness**
```python
from autopr.prompts import PROMPT_VERSION

print(f"Using prompt version: {PROMPT_VERSION}")
# Enables version-specific testing and migration
```

## Migration Notes

### From Basic to Enhanced
1. **No Code Changes Required**: Enhanced providers maintain same interface
2. **Automatic Fallbacks**: Existing error handling improves automatically
3. **Enhanced Features**: New validation and analysis features available

### Environment Variable Changes
```bash
# Existing configuration continues to work
AUTOPR_PROVIDER=openai
OPENAI_API_KEY=your_key

# New optional configuration
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-3-sonnet-20240229
AUTOPR_DEBUG=true
```

This template system provides a robust foundation for AI-powered code analysis while maintaining consistency, reliability, and extensibility.