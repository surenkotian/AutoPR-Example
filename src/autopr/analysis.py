"""Enhanced AST-based static analysis for Python diffs.

This module provides comprehensive deterministic checks that are fast to run
and helpful when reviewing code changes:

Static Analysis Features:
- Unused imports (enhanced AST-based detection)
- Function complexity analysis (cyclomatic complexity, nesting depth)
- Missing docstrings for functions and classes
- Risky patterns (eval, exec, bare except blocks)
- Code quality issues (debug prints, TODO comments, None comparisons)
- Security vulnerabilities (dangerous functions without error handling)

Diff-Aware Analysis:
- Only analyzes changed lines in git diffs
- Provides line-accurate findings
- Handles partial code snippets

Severity Levels:
- info: Informational suggestions
- warning: Potential issues that should be reviewed
- critical: Serious issues that likely need immediate attention

The analyzer is fully deterministic and requires no AI calls.
"""

from __future__ import annotations

import ast
import re
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict


class AnalysisFinding:
    """Represents a static analysis finding."""
    
    def __init__(self, type: str, message: str, line: int | None = None, 
                 severity: str = "info", column: int | None = None,
                 code_snippet: str | None = None, file_path: str | None = None):
        self.type = type
        self.message = message
        self.line = line
        self.column = column
        self.severity = severity
        self.code_snippet = code_snippet
        self.file_path = file_path
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary format."""
        result = {
            "type": self.type,
            "message": self.message,
            "severity": self.severity
        }
        if self.line is not None:
            result["line"] = self.line
        if self.column is not None:
            result["column"] = self.column
        if self.code_snippet:
            result["code_snippet"] = self.code_snippet
        if self.file_path:
            result["file_path"] = self.file_path
        return result


class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyzes function and method complexity."""
    
    def __init__(self):
        self.complexity_findings: List[AnalysisFinding] = []
        self.current_function = None
        self.nesting_depth = 0
        self.max_nesting_depth = 0
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_function = self.current_function
        old_nesting = self.nesting_depth
        
        self.current_function = node.name
        self.nesting_depth = 0
        self.max_nesting_depth = 0
        
        # Count complexity points
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Increment complexity for control structures
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(child, ast.Try):
                complexity += len(child.handlers)
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
            
            # Track nesting depth
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                self.nesting_depth += 1
                self.max_nesting_depth = max(self.max_nesting_depth, self.nesting_depth)
        
        # Check complexity thresholds
        if complexity > 10:
            self.complexity_findings.append(AnalysisFinding(
                type="high_complexity",
                message=f"Function '{node.name}' has high cyclomatic complexity ({complexity}). Consider refactoring.",
                line=node.lineno,
                severity="warning"
            ))
        
        if self.max_nesting_depth > 4:
            self.complexity_findings.append(AnalysisFinding(
                type="deep_nesting",
                message=f"Function '{node.name}' has deep nesting ({self.max_nesting_depth} levels). Consider refactoring.",
                line=node.lineno,
                severity="warning"
            ))
        
        self.current_function = old_function
        self.nesting_depth = old_nesting
        self.generic_visit(node)


class DocstringAnalyzer(ast.NodeVisitor):
    """Analyzes missing docstrings."""
    
    def __init__(self):
        self.docstring_findings: List[AnalysisFinding] = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check if function has docstring (only for non-private functions)
        if not node.name.startswith('_') and not ast.get_docstring(node):
            self.docstring_findings.append(AnalysisFinding(
                type="missing_function_docstring",
                message=f"Function '{node.name}' is missing a docstring.",
                line=node.lineno,
                severity="info"
            ))
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # Check if async function has docstring (only for non-private functions)
        if not node.name.startswith('_') and not ast.get_docstring(node):
            self.docstring_findings.append(AnalysisFinding(
                type="missing_function_docstring",
                message=f"Async function '{node.name}' is missing a docstring.",
                line=node.lineno,
                severity="info"
            ))
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        # Check if class has docstring (only for non-private classes)
        if not node.name.startswith('_') and not ast.get_docstring(node):
            self.docstring_findings.append(AnalysisFinding(
                type="missing_class_docstring",
                message=f"Class '{node.name}' is missing a docstring.",
                line=node.lineno,
                severity="info"
            ))
        self.generic_visit(node)


class RiskyPatternAnalyzer(ast.NodeVisitor):
    """Analyzes risky code patterns."""
    
    def __init__(self):
        self.risky_findings: List[AnalysisFinding] = []
        self.in_try_block = False
        self.try_blocks = 0
    
    def visit_Try(self, node: ast.Try):
        old_in_try = self.in_try_block
        self.in_try_block = True
        self.try_blocks += 1
        self.generic_visit(node)
        self.in_try_block = old_in_try
    
    def visit_Call(self, node: ast.Call):
        # Check for eval() and exec() calls
        if isinstance(node.func, ast.Name):
            if node.func.id == 'eval':
                self.risky_findings.append(AnalysisFinding(
                    type="dangerous_function",
                    message="Use of eval() is dangerous and can lead to security vulnerabilities.",
                    line=node.lineno,
                    severity="critical"
                ))
            elif node.func.id == 'exec':
                self.risky_findings.append(AnalysisFinding(
                    type="dangerous_function",
                    message="Use of exec() is dangerous and can lead to security vulnerabilities.",
                    line=node.lineno,
                    severity="critical"
                ))
        
        # Check for subprocess calls without error handling
        if isinstance(node.func, ast.Attribute):
            func_name = ast.unparse(node.func)
            if func_name.startswith('subprocess.') and not self.in_try_block:
                self.risky_findings.append(AnalysisFinding(
                    type="missing_error_handling",
                    message=f"Function call '{func_name}' without try/except error handling.",
                    line=node.lineno,
                    severity="warning"
                ))
        
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        # Check for bare except clauses
        if node.type is None:
            self.risky_findings.append(AnalysisFinding(
                type="bare_except",
                message="Bare except clause catches all exceptions. Consider being more specific.",
                line=node.lineno if hasattr(node, 'lineno') else None,
                severity="warning"
            ))
        self.generic_visit(node)


def _extract_diff_info(diff: str) -> Tuple[str, Dict[str, Any]]:
    """Extract added lines from diff and return diff metadata."""
    if not diff.strip():
        return "", {}
    
    # Check if this looks like a unified diff
    if 'diff --git' in diff or '\n+' in diff:
        added_lines = []
        diff_info = {
            "files_changed": 0,
            "lines_added": 0,
            "lines_deleted": 0
        }
        
        current_file = None
        for line in diff.splitlines():
            if line.startswith('diff --git'):
                diff_info["files_changed"] += 1
                # Extract file path
                parts = line.split()
                if len(parts) >= 3:
                    current_file = parts[2].lstrip('b/')
            elif line.startswith('+++') or line.startswith('---'):
                continue
            elif line.startswith('+') and not line.startswith('+++'):
                # Added line
                content = line[1:]  # Remove leading +
                added_lines.append(content)
                diff_info["lines_added"] += 1
            elif line.startswith('-') and not line.startswith('---'):
                # Deleted line
                diff_info["lines_deleted"] += 1
        
        return '\n'.join(added_lines), diff_info
    
    # Not a diff, treat as regular code
    return diff, {}


def _analyze_imports(tree: ast.AST) -> List[AnalysisFinding]:
    """Enhanced import analysis with better scope tracking."""
    findings = []
    
    # Collect all imports with their line numbers
    imports = {}
    import_froms = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split('.')[0]
                imports[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                name = alias.asname or alias.name
                full_name = f"{module}.{name}" if module else name
                import_froms[name] = (node.lineno, full_name)
    
    # Collect all name usages
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            # Handle attribute access (e.g., os.path.join)
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)
    
    # Check for unused imports
    for name, line in imports.items():
        if name not in used_names:
            findings.append(AnalysisFinding(
                type="unused_import",
                message=f"Imported '{name}' is not used",
                line=line,
                severity="info"
            ))
    
    # Check for unused from imports
    for name, (line, full_name) in import_froms.items():
        if name not in used_names and full_name not in used_names:
            findings.append(AnalysisFinding(
                type="unused_import",
                message=f"Imported '{full_name}' is not used",
                line=line,
                severity="info"
            ))
    
    return findings


def _analyze_debug_and_todo(text: str) -> List[AnalysisFinding]:
    """Analyze debug prints and TODO comments."""
    findings = []
    
    for i, line in enumerate(text.splitlines(), start=1):
        # Check for TODO comments
        if 'TODO' in line or 'FIXME' in line:
            findings.append(AnalysisFinding(
                type="todo_comment",
                message="TODO/FIXME comment found",
                line=i,
                severity="info",
                code_snippet=line.strip()
            ))
        
        # Check for debug prints
        if re.search(r'\bprint\s*\(', line):
            findings.append(AnalysisFinding(
                type="debug_print",
                message="Debug print statement found",
                line=i,
                severity="info",
                code_snippet=line.strip()
            ))
        
        # Check for pdb debugger calls
        if re.search(r'\bpdb\.set_trace\s*\(', line):
            findings.append(AnalysisFinding(
                type="debugger_call",
                message="pdb.set_trace() call found - remove before committing",
                line=i,
                severity="warning",
                code_snippet=line.strip()
            ))
    
    return findings


def _analyze_none_comparisons(tree: ast.AST) -> List[AnalysisFinding]:
    """Analyze None comparisons using ==/!= instead of is/is not."""
    findings = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and comparator.value is None:
                    for op in node.ops:
                        if isinstance(op, (ast.Eq, ast.NotEq)):
                            findings.append(AnalysisFinding(
                                type="none_equality_comparison",
                                message="Use 'is'/'is not' when comparing to None",
                                line=getattr(node, 'lineno', None),
                                severity="warning"
                            ))
    
    return findings


def analyze_python_code(code: str, file_path: str | None = None) -> List[AnalysisFinding]:
    """Analyze Python code and return findings.
    
    Args:
        code: Python code to analyze (can be a diff or full file)
        file_path: Optional file path for context
    
    Returns:
        List of AnalysisFinding objects
    """
    if not code.strip():
        return []
    
    text, diff_info = _extract_diff_info(code)
    findings = []
    
    # Parse AST for deeper analysis
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        # If parsing fails, do basic text analysis only
        findings.append(AnalysisFinding(
            type="syntax_error",
            message=f"Syntax error in code: {str(e)}",
            line=getattr(e, 'lineno', None),
            severity="critical"
        ))
        # Still do text-based analysis on the original code
        text = code
        tree = None
    
    # Text-based analysis (always available)
    findings.extend(_analyze_debug_and_todo(text))
    
    if tree is None:
        return findings
    
    # AST-based analysis
    findings.extend(_analyze_imports(tree))
    findings.extend(_analyze_none_comparisons(tree))
    
    # Complexity analysis
    complexity_analyzer = ComplexityAnalyzer()
    complexity_analyzer.visit(tree)
    findings.extend(complexity_analyzer.complexity_findings)
    
    # Docstring analysis
    docstring_analyzer = DocstringAnalyzer()
    docstring_analyzer.visit(tree)
    findings.extend(docstring_analyzer.docstring_findings)
    
    # Risky pattern analysis
    risky_analyzer = RiskyPatternAnalyzer()
    risky_analyzer.visit(tree)
    findings.extend(risky_analyzer.risky_findings)
    
    # Add file path to findings if provided
    if file_path:
        for finding in findings:
            finding.file_path = file_path
    
    return findings


def analyze_diff(diff_text: str, language: str = "python", file_path: str | None = None) -> Dict[str, Any]:
    """Analyze a diff and return comprehensive findings.
    
    Args:
        diff_text: Diff content or code snippet
        language: Programming language (default: python)
        file_path: Optional file path for context
    
    Returns:
        Dictionary with analysis results and metadata
    """
    if language.lower() != "python":
        return {
            "language": language,
            "findings": [],
            "summary": {"total_findings": 0, "by_severity": {}, "by_type": {}}
        }
    
    findings = analyze_python_code(diff_text, file_path)
    
    # Convert findings to dictionaries
    finding_dicts = [finding.to_dict() for finding in findings]
    
    # Generate summary statistics
    severity_counts = defaultdict(int)
    type_counts = defaultdict(int)
    
    for finding in findings:
        severity_counts[finding.severity] += 1
        type_counts[finding.type] += 1
    
    summary = {
        "total_findings": len(findings),
        "by_severity": dict(severity_counts),
        "by_type": dict(type_counts)
    }
    
    # Extract diff metadata
    _, diff_info = _extract_diff_info(diff_text)
    
    return {
        "language": language,
        "findings": finding_dicts,
        "summary": summary,
        "diff_info": diff_info
    }


def batch_analyze_files(files: Dict[str, str]) -> Dict[str, Any]:
    """Analyze multiple files in batch.
    
    Args:
        files: Dictionary mapping file paths to code content
    
    Returns:
        Combined analysis results for all files
    """
    all_findings = []
    file_summaries = {}
    
    for file_path, content in files.items():
        result = analyze_diff(content, file_path=file_path)
        file_summaries[file_path] = result
        
        # Add file path to findings
        for finding in result["findings"]:
            finding["file_path"] = file_path
            all_findings.append(finding)
    
    # Overall summary
    total_findings = len(all_findings)
    severity_counts = defaultdict(int)
    type_counts = defaultdict(int)
    
    for finding in all_findings:
        severity_counts[finding["severity"]] += 1
        type_counts[finding["type"]] += 1
    
    return {
        "files_analyzed": len(files),
        "total_findings": total_findings,
        "findings": all_findings,
        "file_summaries": file_summaries,
        "overall_summary": {
            "by_severity": dict(severity_counts),
            "by_type": dict(type_counts)
        }
    }
