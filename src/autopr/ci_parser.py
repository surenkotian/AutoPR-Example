"""Enhanced CI and test log parsing with comprehensive error analysis.

This module provides robust parsing for multiple CI systems and test frameworks:
- pytest (enhanced from basic version)
- unittest
- GitHub Actions
- Error type classification
- Flaky test detection
- Detailed failure analysis
"""
from __future__ import annotations

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ErrorType(Enum):
    """Classification of error types for better analysis."""
    ASSERTION_ERROR = "assertion_error"
    IMPORT_ERROR = "import_error"
    TIMEOUT_ERROR = "timeout_error"
    CONNECTION_ERROR = "connection_error"
    PERMISSION_ERROR = "permission_error"
    VALUE_ERROR = "value_error"
    TYPE_ERROR = "type_error"
    KEY_ERROR = "key_error"
    INDEX_ERROR = "index_error"
    ATTRIBUTE_ERROR = "attribute_error"
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    ENVIRONMENT_ERROR = "environment_error"
    UNKNOWN = "unknown"


class TestStatus(Enum):
    """Test execution status."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    XFAILED = "xfailed"
    XPASSED = "xpassed"


@dataclass
class TestFailure:
    """Structured representation of a test failure."""
    name: str
    status: TestStatus
    message: str
    error_type: ErrorType
    stack_trace: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    flaky_indicators: List[str] = None
    
    def __post_init__(self):
        if self.flaky_indicators is None:
            self.flaky_indicators = []


@dataclass
class CISummary:
    """Comprehensive CI execution summary."""
    framework: str
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    xfailed: int
    xpassed: int
    duration: Optional[float] = None
    failures: List[TestFailure] = None
    environment_info: Dict[str, Any] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.failures is None:
            self.failures = []
        if self.environment_info is None:
            self.environment_info = {}
        if self.warnings is None:
            self.warnings = []


class EnhancedCIParser:
    """Enhanced CI parser supporting multiple frameworks and comprehensive analysis."""
    
    def __init__(self):
        self.error_patterns = self._compile_error_patterns()
        self.flaky_patterns = self._compile_flaky_patterns()
        
    def _compile_error_patterns(self) -> Dict[ErrorType, List[re.Pattern]]:
        """Compile regex patterns for error type classification."""
        patterns = {
            ErrorType.ASSERTION_ERROR: [
                re.compile(r"AssertionError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"assert.*failed", re.IGNORECASE),
            ],
            ErrorType.IMPORT_ERROR: [
                re.compile(r"ImportError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"ModuleNotFoundError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"No module named", re.IGNORECASE),
            ],
            ErrorType.TIMEOUT_ERROR: [
                re.compile(r"TimeoutError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"timed out", re.IGNORECASE),
                re.compile(r"Timeout.*exceeded", re.IGNORECASE),
            ],
            ErrorType.CONNECTION_ERROR: [
                re.compile(r"ConnectionError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"Connection.*refused", re.IGNORECASE),
                re.compile(r"Failed to establish.*connection", re.IGNORECASE),
            ],
            ErrorType.PERMISSION_ERROR: [
                re.compile(r"PermissionError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"Access denied", re.IGNORECASE),
                re.compile(r"Permission denied", re.IGNORECASE),
            ],
            ErrorType.VALUE_ERROR: [
                re.compile(r"ValueError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.TYPE_ERROR: [
                re.compile(r"TypeError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.KEY_ERROR: [
                re.compile(r"KeyError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.INDEX_ERROR: [
                re.compile(r"IndexError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.ATTRIBUTE_ERROR: [
                re.compile(r"AttributeError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.SYNTAX_ERROR: [
                re.compile(r"SyntaxError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.RUNTIME_ERROR: [
                re.compile(r"RuntimeError[:\s]*(.*)", re.IGNORECASE),
            ],
            ErrorType.ENVIRONMENT_ERROR: [
                re.compile(r"EnvironmentError[:\s]*(.*)", re.IGNORECASE),
                re.compile(r"OSError[:\s]*(.*)", re.IGNORECASE),
            ],
        }
        return patterns
    
    def _compile_flaky_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate flaky tests."""
        return [
            re.compile(r"sometimes|fail|pass|intermittent|inconsistent", re.IGNORECASE),
            re.compile(r"race condition", re.IGNORECASE),
            re.compile(r"timing.*issue", re.IGNORECASE),
            re.compile(r"network.*unstable", re.IGNORECASE),
            re.compile(r"flaky", re.IGNORECASE),
            re.compile(r"retry.*success", re.IGNORECASE),
            re.compile(r"occasionally", re.IGNORECASE),
        ]
    
    def classify_error(self, error_message: str) -> ErrorType:
        """Classify error type based on error message."""
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern.search(error_message):
                    return error_type
        return ErrorType.UNKNOWN
    
    def detect_flaky_indicators(self, failure: TestFailure) -> List[str]:
        """Detect indicators that suggest a flaky test."""
        indicators = []
        full_text = f"{failure.message} {failure.stack_trace}".lower()
        
        for pattern in self.flaky_patterns:
            if pattern.search(full_text):
                indicators.append(pattern.pattern)
        
        # Additional flaky indicators
        if "retry" in full_text or "rerun" in full_text:
            indicators.append("test_retried")
        if "network" in full_text or "connection" in full_text:
            indicators.append("network_dependency")
        if "sleep" in full_text or "wait" in full_text:
            indicators.append("timing_dependency")
            
        return indicators
    
    def parse_pytest_output(self, log: str) -> CISummary:
        """Enhanced pytest output parsing with comprehensive analysis."""
        lines = log.splitlines()
        failures = []
        warnings = []
        environment_info = {}
        
        # Extract basic statistics with improved regex
        stats = self._extract_pytest_stats(log)
        
        # Extract failures with enhanced parsing
        failures = self._extract_pytest_failures(log)
        
        # Extract warnings
        warnings = self._extract_warnings(log, "pytest")
        
        # Extract environment info
        environment_info = self._extract_environment_info(log)
        
        # Detect flaky tests
        for failure in failures:
            flaky_indicators = self.detect_flaky_indicators(failure)
            failure.flaky_indicators = flaky_indicators
        
        return CISummary(
            framework="pytest",
            total_tests=stats["total"],
            passed=stats["passed"],
            failed=stats["failed"],
            errors=stats["errors"],
            skipped=stats["skipped"],
            xfailed=stats.get("xfailed", 0),
            xpassed=stats.get("xpassed", 0),
            failures=failures,
            environment_info=environment_info,
            warnings=warnings,
            duration=self._extract_duration(log)
        )
    
    def parse_unittest_output(self, log: str) -> CISummary:
        """Parse unittest output with comprehensive analysis."""
        lines = log.splitlines()
        failures = []
        warnings = []
        environment_info = {}
        
        # Extract basic unittest statistics
        stats = self._extract_unittest_stats(log)
        
        # Extract failures
        failures = self._extract_unittest_failures(log)
        
        # Extract warnings
        warnings = self._extract_warnings(log, "unittest")
        
        # Extract environment info
        environment_info = self._extract_environment_info(log)
        
        # Detect flaky tests
        for failure in failures:
            flaky_indicators = self.detect_flaky_indicators(failure)
            failure.flaky_indicators = flaky_indicators
        
        return CISummary(
            framework="unittest",
            total_tests=stats["total"],
            passed=stats["passed"],
            failed=stats["failed"],
            errors=stats["errors"],
            skipped=stats["skipped"],
            xfailed=0,  # unittest doesn't have xfailed
            xpassed=0,  # unittest doesn't have xpassed
            failures=failures,
            environment_info=environment_info,
            warnings=warnings,
            duration=self._extract_duration(log)
        )
    
    def parse_github_actions_output(self, log: str) -> CISummary:
        """Parse GitHub Actions workflow output."""
        lines = log.splitlines()
        test_summaries = []
        
        # Look for test result sections in GitHub Actions logs
        test_patterns = [
            r"##\[error\].*?(?=##\[|\Z)",  # Error sections
            r"##\[group\].*?test.*?(?=##\[|\Z)",  # Test groups
            r"Test.*?failed.*?(?=\n\n|\Z)",  # Test failure messages
        ]
        
        for pattern in test_patterns:
            matches = re.finditer(pattern, log, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            for match in matches:
                section_content = match.group(0)
                test_summary = self._parse_github_actions_test_section(section_content)
                if test_summary:
                    test_summaries.append(test_summary)
        
        # If no specific test sections found, try to extract overall status
        if not test_summaries:
            overall_summary = self._extract_github_actions_overall_status(log)
            return overall_summary
        
        # Combine multiple test summaries
        return self._combine_github_actions_summaries(test_summaries)
    
    def _extract_pytest_stats(self, log: str) -> Dict[str, int]:
        """Extract pytest statistics with improved pattern matching."""
        stats = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0, "xfailed": 0, "xpassed": 0}
        
        # Main summary line patterns
        patterns = [
            r"=+\s*(\d+)\s+passed,?\s*(\d+)?\s+failed,?\s*(\d+)?\s+errors?,?\s*(\d+)?\s+skipped,?\s*(\d+)?\s+xfailed,?\s*(\d+)?\s+xpassed.*=+",
            r"(\d+)\s+passed.*?(\d+)\s+failed.*?(\d+)\s+errors?.*?(\d+)\s+skipped",
            r"(\d+)\s+passed.*?(\d+)\s+failed",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, log, re.IGNORECASE | re.DOTALL)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    stats["passed"] = int(groups[0]) if groups[0] else 0
                    stats["failed"] = int(groups[1]) if groups[1] else 0
                    if len(groups) >= 3:
                        stats["errors"] = int(groups[2]) if groups[2] else 0
                    if len(groups) >= 4:
                        stats["skipped"] = int(groups[3]) if groups[3] else 0
                    if len(groups) >= 5:
                        stats["xfailed"] = int(groups[4]) if groups[4] else 0
                    if len(groups) >= 6:
                        stats["xpassed"] = int(groups[5]) if groups[5] else 0
                break
        
        # Individual pattern searches as fallback
        individual_patterns = {
            "passed": r"(\d+)\s+passed",
            "failed": r"(\d+)\s+failed",
            "errors": r"(\d+)\s+errors?",
            "skipped": r"(\d+)\s+skipped",
            "xfailed": r"(\d+)\s+xfailed",
            "xpassed": r"(\d+)\s+xpassed",
        }
        
        for key, pattern in individual_patterns.items():
            match = re.search(pattern, log, re.IGNORECASE)
            if match and stats[key] == 0:  # Only use if not already set
                stats[key] = int(match.group(1))
        
        stats["total"] = stats["passed"] + stats["failed"] + stats["errors"] + stats["skipped"]
        return stats
    
    def _extract_unittest_stats(self, log: str) -> Dict[str, int]:
        """Extract unittest statistics."""
        stats = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0}
        
        # unittest summary patterns
        patterns = [
            r"Ran\s+(\d+)\s+test[s]?\s+in\s+[\d.]+s",
            r"OK|FAILED\s+\(failures=(\d+)\)|ERRORS?\s+(\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, log, re.IGNORECASE)
            if match:
                if "Ran" in pattern:
                    stats["total"] = int(match.group(1))
                elif "FAILED" in pattern:
                    stats["failed"] = int(match.group(1))
                elif "ERROR" in pattern:
                    stats["errors"] = int(match.group(1))
        
        # Individual pattern searches
        individual_patterns = {
            "passed": r"(\d+)\s+passed",
            "failed": r"(\d+)\s+failed",
            "errors": r"(\d+)\s+errors?",
            "skipped": r"(\d+)\s+skipped",
        }
        
        for key, pattern in individual_patterns.items():
            match = re.search(pattern, log, re.IGNORECASE)
            if match:
                stats[key] = int(match.group(1))
        
        # Calculate missing values
        if stats["total"] == 0:
            stats["total"] = stats["passed"] + stats["failed"] + stats["errors"] + stats["skipped"]
        
        return stats
    
    def _extract_pytest_failures(self, log: str) -> List[TestFailure]:
        """Extract detailed pytest failure information."""
        failures = []
        
        # Look for FAILURES section
        if "FAILURES" not in log:
            # Fallback to simple FAILED patterns
            return self._extract_simple_failures(log, "pytest")
        
        lines = log.splitlines()
        try:
            start = next(i for i, line in enumerate(lines) if "FAILURES" in line)
        except StopIteration:
            return failures
        
        i = start
        while i < len(lines):
            line = lines[i].strip()
            
            # Match test headers like: '____ test_name ____'
            match = re.match(r"_{3,}\s*([\w\-\[\]:.]+)\s*_{3,}", line)
            if match:
                test_name = match.group(1)
                failure_info = self._extract_failure_details(lines, i, test_name)
                if failure_info:
                    failures.append(failure_info)
            
            i += 1
        
        return failures
    
    def _extract_unittest_failures(self, log: str) -> List[TestFailure]:
        """Extract unittest failure information."""
        failures = []
        
        # Look for common unittest failure patterns
        lines = log.splitlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Match test method patterns
            if line.startswith("test") and ("FAIL:" in line or "ERROR:" in line):
                test_name = line.split(":", 1)[0].strip()
                status = TestStatus.FAILED if "FAIL:" in line else TestStatus.ERROR
                
                # Extract error message
                message_lines = []
                j = i + 1
                while j < len(lines) and lines[j].strip():
                    if lines[j].strip().startswith("Traceback"):
                        # Skip traceback header
                        j += 1
                        # Extract traceback and message
                        traceback_lines = []
                        while j < len(lines) and lines[j].strip():
                            traceback_lines.append(lines[j])
                            j += 1
                        
                        # Join message after traceback
                        if j < len(lines) and lines[j].strip():
                            message_lines.append(lines[j].strip())
                        
                        failure = TestFailure(
                            name=test_name,
                            status=status,
                            message=" ".join(message_lines),
                            error_type=self.classify_error(" ".join(message_lines)),
                            stack_trace="\n".join(traceback_lines)
                        )
                        failures.append(failure)
                        break
                    else:
                        message_lines.append(lines[j])
                    j += 1
            
            i += 1
        
        return failures
    
    def _extract_failure_details(self, lines: List[str], start_idx: int, test_name: str) -> Optional[TestFailure]:
        """Extract detailed failure information from pytest failure block."""
        i = start_idx + 1
        message_lines = []
        stack_trace_lines = []
        in_traceback = False
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Stop at next test header or end of failures section
            if re.match(r"_{3,}\s*[\w\-\[\]:.]+\s*_{3,}", line) or line.startswith("="):
                break
            
            if line.startswith("Traceback"):
                in_traceback = True
                stack_trace_lines.append(line)
            elif in_traceback:
                stack_trace_lines.append(line)
                # Check if we're at the end of traceback (error message follows)
                if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(" "):
                    # This is likely the error message
                    message_lines.append(line)
            else:
                message_lines.append(line)
            
            i += 1
        
        message = " ".join(message_lines)
        stack_trace = "\n".join(stack_trace_lines)
        error_type = self.classify_error(message)
        
        # Extract file and line number from stack trace
        file_path, line_number = self._extract_location_from_traceback(stack_trace)
        
        return TestFailure(
            name=test_name,
            status=TestStatus.FAILED,
            message=message,
            error_type=error_type,
            stack_trace=stack_trace,
            file_path=file_path,
            line_number=line_number
        )
    
    def _extract_simple_failures(self, log: str, framework: str) -> List[TestFailure]:
        """Extract failures using simple pattern matching."""
        failures = []
        pattern = r"FAILED\s+([^\s:]+).*?-\s*(.*)$"
        
        for line in log.splitlines():
            match = re.match(pattern, line.strip())
            if match:
                test_name = match.group(1)
                message = match.group(2)
                
                failure = TestFailure(
                    name=test_name,
                    status=TestStatus.FAILED,
                    message=message,
                    error_type=self.classify_error(message),
                    stack_trace=""
                )
                failures.append(failure)
        
        return failures
    
    def _extract_warnings(self, log: str, framework: str) -> List[str]:
        """Extract warnings from log output."""
        warnings = []
        
        warning_patterns = [
            r"WARNING[:\s]*(.*)",
            r"DeprecationWarning[:\s]*(.*)",
            r"UserWarning[:\s]*(.*)",
            r"FutureWarning[:\s]*(.*)",
        ]
        
        for pattern in warning_patterns:
            matches = re.finditer(pattern, log, re.IGNORECASE)
            for match in matches:
                warnings.append(match.group(1).strip())
        
        return warnings
    
    def _extract_environment_info(self, log: str) -> Dict[str, Any]:
        """Extract environment information from CI logs."""
        env_info = {}
        
        # Python version
        python_version_match = re.search(r"Python\s+(\d+\.\d+\.\d+)", log)
        if python_version_match:
            env_info["python_version"] = python_version_match.group(1)
        
        # Platform info
        platform_match = re.search(r"Platform:\s*(.*)", log)
        if platform_match:
            env_info["platform"] = platform_match.group(1)
        
        # Dependencies
        deps_patterns = [
            r"pytest-(\d+\.\d+\.\d+)",
            r"coverage-(\d+\.\d+\.\d+)",
            r"requests-(\d+\.\d+\.\d+)",
        ]
        
        for pattern in deps_patterns:
            match = re.search(pattern, log)
            if match:
                dep_name = pattern.split("-")[0].replace("r", "")
                env_info[dep_name] = match.group(1)
        
        return env_info
    
    def _extract_duration(self, log: str) -> Optional[float]:
        """Extract test execution duration."""
        duration_patterns = [
            r"in\s+([\d.]+)s",
            r"took\s+([\d.]+)\s+seconds",
            r"Duration:\s+([\d.]+)s",
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, log, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_location_from_traceback(self, stack_trace: str) -> Tuple[Optional[str], Optional[int]]:
        """Extract file path and line number from stack trace."""
        # Look for file:line patterns
        pattern = r'File\s+"([^"]+)",\s*line\s+(\d+)'
        match = re.search(pattern, stack_trace)
        
        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))
            return file_path, line_number
        
        return None, None
    
    def _parse_github_actions_test_section(self, section_content: str) -> Optional[CISummary]:
        """Parse a specific test section from GitHub Actions output."""
        # This would need more specific implementation based on actual GitHub Actions test output format
        # For now, return a basic summary
        return None
    
    def _extract_github_actions_overall_status(self, log: str) -> CISummary:
        """Extract overall GitHub Actions status."""
        # Look for success/failure indicators
        if "##[error]" in log or "FAILED" in log:
            status = "failed"
        elif "SUCCESS" in log or "##[success]" in log:
            status = "passed"
        else:
            status = "unknown"
        
        # Extract basic info
        warnings = self._extract_warnings(log, "github_actions")
        environment_info = self._extract_environment_info(log)
        
        return CISummary(
            framework="github_actions",
            total_tests=0,
            passed=1 if status == "passed" else 0,
            failed=1 if status == "failed" else 0,
            errors=0,
            skipped=0,
            xfailed=0,
            xpassed=0,
            warnings=warnings,
            environment_info=environment_info
        )
    
    def _combine_github_actions_summaries(self, summaries: List[CISummary]) -> CISummary:
        """Combine multiple GitHub Actions test summaries."""
        if not summaries:
            return self._extract_github_actions_overall_status("")
        
        # Combine statistics
        total_tests = sum(s.total_tests for s in summaries)
        passed = sum(s.passed for s in summaries)
        failed = sum(s.failed for s in summaries)
        errors = sum(s.errors for s in summaries)
        skipped = sum(s.skipped for s in summaries)
        
        # Combine failures
        all_failures = []
        for summary in summaries:
            all_failures.extend(summary.failures)
        
        # Combine warnings and environment info
        all_warnings = []
        for summary in summaries:
            all_warnings.extend(summary.warnings)
        
        # Merge environment info
        env_info = {}
        for summary in summaries:
            env_info.update(summary.environment_info)
        
        return CISummary(
            framework="github_actions",
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            failures=all_failures,
            warnings=all_warnings,
            environment_info=env_info
        )
    
    def parse(self, log: str, framework: Optional[str] = None) -> CISummary:
        """Parse CI log using appropriate parser based on framework or content detection."""
        if framework:
            framework = framework.lower()
        
        # Auto-detect framework if not specified
        if not framework:
            if "pytest" in log.lower() or "FAILED" in log and "=====" in log:
                framework = "pytest"
            elif "unittest" in log.lower() or "Ran" in log and "test" in log:
                framework = "unittest"
            elif "github" in log.lower() or "##[" in log:
                framework = "github_actions"
            else:
                # Default to pytest for backward compatibility
                framework = "pytest"
        
        if framework == "pytest":
            return self.parse_pytest_output(log)
        elif framework == "unittest":
            return self.parse_unittest_output(log)
        elif framework == "github_actions":
            return self.parse_github_actions_output(log)
        else:
            raise ValueError(f"Unsupported framework: {framework}")


# Export key classes and functions for easy import
__all__ = [
    'EnhancedCIParser', 'CISummary', 'TestFailure', 'ErrorType', 'TestStatus',
    'parse_ci_log', 'parse_pytest_enhanced', 'parse_unittest_enhanced', 
    'parse_github_actions_enhanced'
]

# Convenience functions for backward compatibility
def parse_ci_log(log: str, framework: Optional[str] = None) -> CISummary:
    """Parse CI log and return comprehensive summary."""
    parser = EnhancedCIParser()
    return parser.parse(log, framework)


def parse_pytest_output(log: str) -> dict:
    """Enhanced pytest parsing."""
    import json, enum, dataclasses
    class EnumEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, enum.Enum): return obj.value
            if dataclasses.is_dataclass(obj): return dataclasses.asdict(obj)
            return super().default(obj)
    parser = EnhancedCIParser()
    res = parser.parse_pytest_output(log)
    return json.loads(json.dumps(res, cls=EnumEncoder))


def parse_unittest_enhanced(log: str) -> CISummary:
    """Enhanced unittest parsing."""
    parser = EnhancedCIParser()
    return parser.parse_unittest_output(log)


def parse_github_actions_enhanced(log: str) -> CISummary:
    """Enhanced GitHub Actions parsing."""
    parser = EnhancedCIParser()
    return parser.parse_github_actions_output(log)