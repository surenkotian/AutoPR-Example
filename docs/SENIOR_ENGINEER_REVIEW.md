# Senior Engineer Code Review System

This document describes the enhanced AI-assisted code review system that provides senior engineer-level feedback quality.

## Overview

The enhanced code review system improves upon basic automated reviews by following a structured, multi-step approach that prioritizes critical issues and provides actionable feedback with explicit line references.

## Key Improvements

### 1. **Multi-Step Review Process**

The system follows a structured 3-step approach:

- **Step 1 - Understanding Intent**: Analyze what the code change is trying to accomplish
- **Step 2 - Identifying Risk**: Find critical issues in priority order:
  - Logic errors and incorrect behavior (HIGHEST priority)
  - Edge cases and boundary conditions  
  - Security vulnerabilities and data exposure
  - Performance regressions and inefficiencies
- **Step 3 - Suggesting Fix**: Provide specific, actionable solutions with exact line references

### 2. **Senior-Level Analysis**

Unlike basic automated reviews that focus on formatting and style, the senior engineer system prioritizes:

- **Logic Errors**: Incorrect algorithm implementation, wrong operators, flawed business logic
- **Security Vulnerabilities**: Code injection risks, insecure data handling, authentication flaws
- **Edge Cases**: Boundary conditions, null pointer risks, empty collection handling
- **Performance Issues**: Inefficient algorithms, unnecessary iterations, memory leaks

### 3. **Explicit Line References**

Every finding includes:
- Exact line number in the diff
- File path for context
- Specific code snippet when relevant

### 4. **Actionable Fixes**

Instead of vague suggestions like "consider refactoring", each finding includes:
- Clear problem description
- Specific fix recommendation
- Example code changes when applicable

### 5. **No Formatting Comments**

The system explicitly avoids commenting on:
- Code style (handled by linters)
- Formatting issues
- Naming conventions (unless they cause functional issues)

## Usage

### Basic Usage

```python
from autopr.reviewer import review_pr

# Enhanced review with senior-level prompt
result = review_pr(diff, use_senior_prompt=True)

print(result['summary'])
for finding in result['findings']:
    print(f"Line {finding['line']}: {finding['message']}")
    print(f"Fix: {finding['action']}")
```

### Comparison with Basic Review

```python
# Basic review (old system)
basic_result = review_pr(diff, use_senior_prompt=False)

# Senior engineer review (new system)  
senior_result = review_pr(diff, use_senior_prompt=True)
```

## Prompt Template

The senior engineer prompt (`SENIOR_ENGINEER_REVIEW_PROMPT`) includes:

```
You are a senior engineer conducting a thorough code review. Follow this 3-step process:

STEP 1 - UNDERSTAND INTENT: Analyze what the code change is trying to accomplish
STEP 2 - IDENTIFY RISK: Find critical issues in priority order:
  • Logic errors and incorrect behavior (HIGHEST priority)
  • Edge cases and boundary conditions
  • Security vulnerabilities and data exposure  
  • Performance regressions and inefficiencies
STEP 3 - SUGGEST FIX: Provide specific, actionable solutions with exact line references

Review Rules:
- NEVER comment on formatting (handled by linters)
- Reference diff lines explicitly using 'Line X' format
- Use short, actionable bullet points
- Avoid vague comments like 'consider refactoring'
- Focus on issues that could cause runtime failures or security breaches

Return JSON with: summary, findings (array with: type, message, severity, line, file, action), confidence (0.0-1.0)
```

## Example Output

### Before (Basic Review)
```json
{
  "summary": "Code review complete - 2 issues found",
  "findings": [
    {
      "type": "bug",
      "message": "Function returns wrong result",
      "severity": "high"
    }
  ]
}
```

### After (Senior Engineer Review)
```json
{
  "summary": "CRITICAL: Logic error must be fixed before merge",
  "findings": [
    {
      "type": "logic_error",
      "message": "Function returns subtraction instead of addition",
      "severity": "high",
      "line": 4,
      "file": "src/calculator.py",
      "action": "Change 'return a - b' to 'return a + b'"
    }
  ]
}
```

## Implementation Details

### Enhanced Stub Provider

The `EnhancedStubProvider` includes sophisticated static analysis that:

1. **Detects Logic Errors**: Identifies incorrect algorithms (e.g., addition vs subtraction)
2. **Security Analysis**: Finds eval/exec usage, SQL injection patterns
3. **Edge Case Detection**: Identifies potential IndexError, KeyError scenarios
4. **Performance Analysis**: Spots inefficient loops, O(n²) patterns
5. **Error Handling Gaps**: Finds bare except clauses, missing validation

### Provider Integration

All provider classes support the enhanced review:

- **EnhancedOpenAIProvider**: Uses custom prompts with GPT models
- **EnhancedAnthropicProvider**: Uses custom prompts with Claude models  
- **EnhancedStubProvider**: Provides deterministic offline analysis

### Backward Compatibility

The enhancement maintains full backward compatibility:
- Default behavior uses original prompts
- New `use_senior_prompt=True` parameter enables enhanced review
- Existing code continues to work unchanged

## Testing

Run the demonstration script to see the difference:

```bash
cd demo
python test_senior_review.py
```

This shows side-by-side comparison of basic vs senior engineer review output.

## Files Modified

- `src/autopr/prompts.py`: Added `SENIOR_ENGINEER_REVIEW_PROMPT`
- `src/autopr/reviewer.py`: Enhanced `review_pr()` function with senior prompt support
- `src/autopr/providers.py`: Updated all provider classes to support custom prompts
- `demo/senior_engineer_review_example.md`: Example review output
- `demo/test_senior_review.py`: Demonstration script

## Benefits

1. **Higher Quality Reviews**: Focuses on critical functional issues over style
2. **Actionable Feedback**: Developers can immediately understand and fix issues
3. **Explicit References**: Easy to locate and fix problems in code
4. **Risk Prioritization**: Critical issues are highlighted first
5. **Senior-Level Depth**: Matches quality of experienced engineer reviews

## Future Enhancements

Potential improvements include:
- Language-specific analysis rules
- Integration with security scanning tools
- Custom rule sets per organization
- Learning from historical review patterns