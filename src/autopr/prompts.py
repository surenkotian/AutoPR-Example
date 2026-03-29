"""Versioned prompt templates used by AutoPR LLM adapters.

Templates are intentionally designed to be deterministic and consistent across versions.
Each template version ensures the same input produces the same output when temperature=0.
"""

# Version tracking for prompt templates
PROMPT_VERSION = "1.0.0"

TITLE_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are an assistant that writes concise PR titles. Given a code diff and commit messages, produce a one-line title (max 60 characters).\n"
    "Diff:\n{diff}\n\nCommit messages:\n{commits}\n\nIssue: {issue}\n\n"
    "Return only the title text with no explanation."
)

PR_DESCRIPTION_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are an assistant that writes a detailed PR description as JSON. Given a code diff, commits, and an optional issue, return a JSON object with the following keys: title, what_changed, why, files_impacted (array), tests (string), risk_level (low/medium/high), rollback_plan.\n\n"
    "Diff:\n{diff}\n\nCommits:\n{commits}\n\nIssue: {issue}\n\n"
    "Provide only valid JSON (no surrounding markdown)."
)

REVIEW_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are an automated code reviewer. Given a code diff, return a JSON object describing: summary, findings (array of objects with keys: type, message, severity), and confidence (0.0-1.0).\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)

# Additional prompts for enhanced functionality
ISSUE_VALIDATION_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are an issue alignment validator. Given an issue description and code changes, assess how well the changes address the issue. Return a JSON object with: alignment_score (0.0-1.0), key_matches (array of strings), gaps (array of strings), recommendations (array of strings).\n\n"
    "Issue:\n{issue}\n\nDiff:\n{diff}\n\nCommits:\n{commits}\n\nReturn only valid JSON."
)

SENIOR_ENGINEER_REVIEW_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are a senior engineer conducting a thorough code review. Follow this 3-step process:\n\n"
    "STEP 1 - UNDERSTAND INTENT: Analyze what the code change is trying to accomplish\n"
    "STEP 2 - IDENTIFY RISK: Find critical issues in priority order:\n"
    "  • Logic errors and incorrect behavior (HIGHEST priority)\n"
    "  • Edge cases and boundary conditions\n"
    "  • Security vulnerabilities and data exposure\n"
    "  • Performance regressions and inefficiencies\n"
    "STEP 3 - SUGGEST FIX: Provide specific, actionable solutions with exact line references\n\n"
    "Review Rules:\n"
    "- NEVER comment on formatting (handled by linters)\n"
    "- Reference diff lines explicitly using 'Line X' format\n"
    "- Use short, actionable bullet points\n"
    "- Avoid vague comments like 'consider refactoring'\n"
    "- Focus on issues that could cause runtime failures or security breaches\n\n"
    "Return JSON with: summary, findings (array with: type, message, severity, line, file, action), confidence (0.0-1.0)\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)

ENHANCED_REVIEW_PROMPT = (
    f"[PROMPT_VERSION:{PROMPT_VERSION}] "
    "You are an expert code reviewer. Given a code diff, provide a comprehensive review as JSON with: summary, findings (array with type, message, severity, file, line), suggestions (array of improvements), security_notes (array), performance_notes (array), confidence (0.0-1.0).\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)
