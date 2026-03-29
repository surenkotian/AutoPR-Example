from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

from autopr.llm import llm
from autopr import generator
from autopr import analysis
from autopr import reviewer

app = FastAPI(title="AutoPR - Minimal MVP")


class GenerateRequest(BaseModel):
    diff: str = Field(..., example="+ def add(a, b):\n+     return a + b")
    commits: List[str] = Field(..., example=["feat: add helper for math"])
    issue: Optional[str] = Field(None, example="#123")


class AnalysisRequest(BaseModel):
    diff: str = Field(..., example="+ def add(a, b):\n+     return a + b")
    language: str = Field(default="python", example="python")
    file_path: Optional[str] = Field(None, example="src/module.py")


class BatchAnalysisRequest(BaseModel):
    files: Dict[str, str] = Field(..., example={"src/main.py": "print('hello')", "src/utils.py": "import os"})


class AnalysisFinding(BaseModel):
    type: str
    message: str
    severity: str
    line: Optional[int] = None
    column: Optional[int] = None
    code_snippet: Optional[str] = None
    file_path: Optional[str] = None


class AnalysisResponse(BaseModel):
    language: str
    findings: List[AnalysisFinding]
    summary: Dict[str, Any]
    diff_info: Dict[str, Any] = {}


class BatchAnalysisResponse(BaseModel):
    files_analyzed: int
    total_findings: int
    findings: List[AnalysisFinding]
    file_summaries: Dict[str, Any]
    overall_summary: Dict[str, Any]


class ReviewRequest(BaseModel):
    diff: str = Field(..., example="print(\"debug\")\n# TODO: fix")



class GenerateResponse(BaseModel):
    title: str
    what_changed: str
    why: str
    files_impacted: List[str]
    tests: str
    risk_level: str
    rollback_plan: str


class ReviewFinding(BaseModel):
    type: str
    message: str
    severity: Optional[str]


class ReviewResponse(BaseModel):
    summary: str
    findings: List[ReviewFinding]
    confidence: float = Field(..., ge=0.0, le=1.0)


@app.get("/health")
def health():
    return {"status": "ok", "service": "AutoPR Enhanced Static Analysis"}


@app.post("/analyze", response_model=AnalysisResponse, summary="Static Analysis", response_description="Enhanced static analysis results")
def analyze_code(req: AnalysisRequest):
    """Perform enhanced static analysis on code diff or snippet.
    
    This endpoint provides comprehensive static analysis without requiring any AI calls.
    It analyzes Python code for:
    - Unused imports
    - Function complexity
    - Missing docstrings
    - Risky patterns (eval, exec, bare except)
    - Code quality issues
    - Security vulnerabilities
    """
    logger.info(f"Analyzing {req.language} code...")
    
    try:
        result = analysis.analyze_diff(
            diff_text=req.diff,
            language=req.language,
            file_path=req.file_path
        )
        
        # Convert to response model
        findings = [AnalysisFinding(**finding) for finding in result['findings']]
        
        return AnalysisResponse(
            language=result['language'],
            findings=findings,
            summary=result['summary'],
            diff_info=result.get('diff_info', {})
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/batch", response_model=BatchAnalysisResponse, summary="Batch Analysis", response_description="Batch static analysis results for multiple files")
def analyze_files_batch(req: BatchAnalysisRequest):
    """Perform static analysis on multiple files in batch.
    
    This endpoint analyzes multiple files at once and provides
    consolidated results with file-by-file breakdowns.
    """
    logger.info(f"Analyzing {len(req.files)} files...")
    
    try:
        result = analysis.batch_analyze_files(req.files)
        
        # Convert to response model
        findings = [AnalysisFinding(**finding) for finding in result['findings']]
        
        return BatchAnalysisResponse(
            files_analyzed=result['files_analyzed'],
            total_findings=result['total_findings'],
            findings=findings,
            file_summaries=result['file_summaries'],
            overall_summary=result['overall_summary']
        )
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@app.get("/analysis/rules", summary="Analysis Rules", response_description="List of supported analysis rules")
def get_analysis_rules():
    """Get information about supported static analysis rules."""
    rules = {
        "imports": {
            "unused_import": {
                "description": "Detect unused imports",
                "severity": "info",
                "category": "code_quality"
            }
        },
        "complexity": {
            "high_complexity": {
                "description": "Functions with high cyclomatic complexity (>10)",
                "severity": "warning",
                "category": "maintainability"
            },
            "deep_nesting": {
                "description": "Functions with deep nesting (>4 levels)",
                "severity": "warning",
                "category": "maintainability"
            }
        },
        "documentation": {
            "missing_function_docstring": {
                "description": "Functions without docstrings",
                "severity": "info",
                "category": "documentation"
            },
            "missing_class_docstring": {
                "description": "Classes without docstrings",
                "severity": "info",
                "category": "documentation"
            }
        },
        "security": {
            "dangerous_function": {
                "description": "Use of eval() or exec() functions",
                "severity": "critical",
                "category": "security"
            },
            "bare_except": {
                "description": "Bare except clauses that catch all exceptions",
                "severity": "warning",
                "category": "error_handling"
            }
        },
        "code_quality": {
            "debug_print": {
                "description": "Debug print statements",
                "severity": "info",
                "category": "debugging"
            },
            "todo_comment": {
                "description": "TODO/FIXME comments",
                "severity": "info",
                "category": "documentation"
            },
            "none_equality_comparison": {
                "description": "Using ==/!= instead of is/is not for None comparisons",
                "severity": "warning",
                "category": "code_style"
            }
        }
    }
    
    return {
        "rules": rules,
        "supported_languages": ["python"],
        "severity_levels": ["info", "warning", "critical"],
        "analysis_types": ["diff", "file", "batch"]
    }


@app.post("/generate", response_model=GenerateResponse, summary="Generate PR", response_description="Auto-generated PR description")
def generate_pr(req: GenerateRequest):
    """Generate a structured PR description from diff, commits and optional issue link.

    This endpoint uses the configured LLM provider (or the stub in dev) to return a JSON object
    describing the PR title, what changed, why it changed, impacted files, tests, risk level and rollback plan.
    """
    logger.info("Generating PR summary...")
    desc = generator.generate_pr_from(req.diff, req.commits, req.issue)
    # Ensure we return a shape matching the model - if provider returns a 'raw' fallback, adapt it
    if isinstance(desc, dict) and "title" in desc:
        return {k: desc.get(k, "") for k in GenerateResponse.__fields__.keys()}
    # minimal fallback
    return GenerateResponse(
        title=str(desc.get("title", "Auto PR")) if isinstance(desc, dict) else str(desc),
        what_changed=desc.get("what_changed", "") if isinstance(desc, dict) else "",
        why=desc.get("why", "") if isinstance(desc, dict) else "",
        files_impacted=desc.get("files_impacted", []) if isinstance(desc, dict) else [],
        tests=desc.get("tests", "") if isinstance(desc, dict) else "",
        risk_level=desc.get("risk_level", "unknown") if isinstance(desc, dict) else "unknown",
        rollback_plan=desc.get("rollback_plan", "") if isinstance(desc, dict) else "",
    )


@app.post("/review", response_model=ReviewResponse, summary="Review PR", response_description="AI-assisted code review findings")
def review_pr(req: ReviewRequest):
    """Analyze a diff and return review findings and a confidence score.

    The review output includes a brief summary, list of findings, each optionally annotated with a severity, and an overall confidence.
    """
    logger.info("Reviewing PR code...")
    out = reviewer.review_pr(req.diff)
    return out
