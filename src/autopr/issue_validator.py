"""Validate whether a PR/branch likely resolves a linked issue.

This module provides both heuristic and LLM-powered validation to check alignment
between issue text and the PR diff/commits. The LLM validation provides more
sophisticated analysis while the heuristic method ensures fast offline capability.
"""
from __future__ import annotations

import re
from typing import Dict, Any, List
from .llm import llm


def _tokenize(text: str) -> List[str]:
    """Tokenize text into words for analysis."""
    return re.findall(r"[A-Za-z0-9_]+", (text or "").lower())


def simple_issue_alignment(issue_text: str, diff: str, commits: List[str]) -> Dict[str, Any]:
    """Return a heuristic alignment score between issue and diff/commits.

    Steps:
      - tokenize issue, diff, commits
      - compute intersection size / union size (Jaccard-like)
      - return score (0.0-1.0) and matched tokens
    """
    issue_tokens = set(_tokenize(issue_text))
    diff_tokens = set(_tokenize(diff))
    commits_tokens = set()
    for c in commits:
        commits_tokens.update(_tokenize(c))

    combined = diff_tokens.union(commits_tokens)
    if not issue_tokens or not combined:
        return {"score": 0.0, "matched": []}

    matched = list(issue_tokens.intersection(combined))
    score = len(matched) / max(1, len(issue_tokens.union(combined)))
    return {"score": float(score), "matched": matched}


def llm_issue_alignment(issue_text: str, diff: str, commits: List[str]) -> Dict[str, Any]:
    """Use LLM to assess issue alignment with enhanced analysis.
    
    This method provides more sophisticated analysis including:
    - Semantic understanding of issue requirements
    - Identification of gaps in implementation
    - Specific recommendations for improvement
    """
    try:
        # Use the provider's enhanced issue validation if available
        if hasattr(llm, 'validate_issue_alignment'):
            return llm.validate_issue_alignment(issue_text, diff, commits)
        else:
            # Fallback to simple alignment if provider doesn't support enhanced validation
            return simple_issue_alignment(issue_text, diff, commits)
    except Exception as e:
        # Fallback to simple method if LLM fails
        import logging
        logging.warning(f"LLM issue validation failed: {e}. Using heuristic method.")
        return simple_issue_alignment(issue_text, diff, commits)


def comprehensive_issue_alignment(issue_text: str, diff: str, commits: List[str]) -> Dict[str, Any]:
    """Combine heuristic and LLM analysis for comprehensive issue validation.
    
    Returns both heuristic score and LLM analysis, allowing the caller to
    choose the appropriate level of detail for their use case.
    """
    heuristic_result = simple_issue_alignment(issue_text, diff, commits)
    llm_result = llm_issue_alignment(issue_text, diff, commits)
    
    # Combine results
    return {
        "heuristic": heuristic_result,
        "llm": llm_result,
        "recommendation": _generate_recommendation(heuristic_result, llm_result)
    }


def _generate_recommendation(heuristic_result: Dict[str, Any], llm_result: Dict[str, Any]) -> str:
    """Generate a recommendation based on both analysis methods."""
    heuristic_score = heuristic_result.get("score", 0.0)
    llm_score = llm_result.get("alignment_score", 0.0)
    
    # Use LLM score if available, otherwise heuristic
    score = llm_score if llm_score > 0 else heuristic_score
    
    if score >= 0.8:
        return "Excellent alignment - changes appear to fully address the issue"
    elif score >= 0.6:
        return "Good alignment - changes largely address the issue with minor gaps"
    elif score >= 0.4:
        return "Moderate alignment - changes partially address the issue"
    elif score >= 0.2:
        return "Weak alignment - changes may not fully address the issue"
    else:
        return "Poor alignment - changes may not address the issue at all"
