"""Enhanced coverage analysis with meaningful change detection and plain English explanations.

This module provides robust coverage parsing and comparison capabilities:
- Multiple coverage report format support
- Meaningful change detection (ignores trivial changes)
- Plain English impact explanations
- Detailed change analysis
- Edge case handling
"""
from __future__ import annotations

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ChangeSeverity(Enum):
    """Classification of coverage change severity."""
    TRIVIAL = "trivial"  # < 0.5% change
    MINOR = "minor"      # 0.5% - 2% change
    MODERATE = "moderate"  # 2% - 5% change
    SIGNIFICANT = "significant"  # 5% - 10% change
    CRITICAL = "critical"  # > 10% change


@dataclass
class CoverageFile:
    """Coverage information for a single file."""
    filename: str
    statements: int
    missing: int
    excluded: int
    coverage_percent: float
    covered_lines: List[int] = None
    missing_lines: List[int] = None
    
    def __post_init__(self):
        if self.covered_lines is None:
            self.covered_lines = []
        if self.missing_lines is None:
            self.missing_lines = []


@dataclass
class CoverageChange:
    """Detailed coverage change for a file."""
    filename: str
    before_percent: float
    after_percent: float
    absolute_change: float
    relative_change: float
    statements_change: int
    missing_change: int
    severity: ChangeSeverity
    impact_explanation: str


@dataclass
class CoverageSummary:
    """Comprehensive coverage analysis summary."""
    total_statements: int
    missing_statements: int
    excluded_statements: int
    coverage_percent: float
    files: List[CoverageFile] = None
    branch_coverage: Optional[float] = None
    line_coverage: Optional[float] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = []


@dataclass
class CoverageComparison:
    """Comprehensive coverage comparison result."""
    before: CoverageSummary
    after: CoverageSummary
    overall_change: float
    severity: ChangeSeverity
    files_changed: List[CoverageChange]
    meaningful_changes: List[CoverageChange]
    trivial_changes: List[CoverageChange]
    new_files: List[CoverageFile]
    removed_files: List[CoverageFile]
    summary_explanation: str
    recommendations: List[str]


class EnhancedCoverageAnalyzer:
    """Enhanced coverage analyzer with intelligent change detection."""
    
    # Threshold for considering changes meaningful (0.5%)
    MEANINGFUL_CHANGE_THRESHOLD = 0.5
    
    # Severity thresholds
    SEVERITY_THRESHOLDS = {
        ChangeSeverity.TRIVIAL: 0.5,
        ChangeSeverity.MINOR: 2.0,
        ChangeSeverity.MODERATE: 5.0,
        ChangeSeverity.SIGNIFICANT: 10.0,
        ChangeSeverity.CRITICAL: float('inf'),
    }
    
    def __init__(self):
        self.coverage_patterns = self._compile_coverage_patterns()
        
    def _compile_coverage_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for different coverage report formats."""
        return {
            'total': [
                re.compile(r"TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)%\s*$", re.MULTILINE),
                re.compile(r"Total.*?(\d+)%"),
                re.compile(r"Coverage.*?(\d+)%"),
            ],
            'file_line': [
                re.compile(r"^([^\s]+\.py)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)%\s*$", re.MULTILINE),
                re.compile(r"^([^\s]+\.py)\s+(\d+)\s+(\d+)\s+(\d+)%\s*$", re.MULTILINE),
            ],
            'branch_coverage': [
                re.compile(r"BRANCH\s+(\d+)\s+(\d+)\s+(\d+)%\s*$", re.MULTILINE),
                re.compile(r"Branch.*?(\d+)%"),
            ],
            'line_coverage': [
                re.compile(r"LINE\s+(\d+)\s+(\d+)\s+(\d+)%\s*$", re.MULTILINE),
                re.compile(r"Line.*?(\d+)%"),
            ]
        }
    
    def parse_coverage_report(self, report_text: str) -> CoverageSummary:
        """Parse coverage report from multiple formats."""
        lines = report_text.splitlines()
        files = []
        
        # Try different parsing strategies
        coverage_data = self._try_html_coverage_format(report_text)
        if not coverage_data:
            coverage_data = self._try_text_coverage_format(report_text)
        if not coverage_data:
            coverage_data = self._try_xml_coverage_format(report_text)
        
        if coverage_data:
            files = coverage_data.get('files', [])
            total_statements = coverage_data.get('total_statements', 0)
            missing_statements = coverage_data.get('missing_statements', 0)
            excluded_statements = coverage_data.get('excluded_statements', 0)
            coverage_percent = coverage_data.get('coverage_percent', 0.0)
            branch_coverage = coverage_data.get('branch_coverage')
            line_coverage = coverage_data.get('line_coverage')
        else:
            # Fallback to basic parsing
            total_statements, missing_statements, excluded_statements, coverage_percent = self._parse_basic_coverage(report_text)
            branch_coverage = self._extract_branch_coverage(report_text)
            line_coverage = self._extract_line_coverage(report_text)
        
        return CoverageSummary(
            total_statements=total_statements,
            missing_statements=missing_statements,
            excluded_statements=excluded_statements,
            coverage_percent=coverage_percent,
            files=files,
            branch_coverage=branch_coverage,
            line_coverage=line_coverage
        )
    
    def _try_html_coverage_format(self, text: str) -> Optional[Dict[str, Any]]:
        """Try to parse HTML format coverage reports."""
        if '<html' not in text.lower() and '<!doctype' not in text.lower():
            return None
        
        files = []
        coverage_percent = 0.0
        total_statements = 0
        missing_statements = 0
        excluded_statements = 0
        
        # Extract file coverage from HTML table rows
        file_pattern = re.compile(r'<tr[^>]*>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>(\d+)</td>.*?<td[^>]*>(\d+)</td>.*?<td[^>]*>(\d+)</td>.*?<td[^>]*>(\d+)%</td>.*?</tr>', re.DOTALL)
        
        for match in file_pattern.finditer(text):
            filename = match.group(1).strip()
            statements = int(match.group(2))
            missing = int(match.group(3))
            excluded = int(match.group(4))
            percent = float(match.group(5))
            
            files.append(CoverageFile(
                filename=filename,
                statements=statements,
                missing=missing,
                excluded=excluded,
                coverage_percent=percent
            ))
            
            total_statements += statements
            missing_statements += missing
            excluded_statements += excluded
        
        # Extract overall coverage
        total_match = re.search(r'<tfoot.*?<td[^>]*>(\d+)%</td>', text, re.DOTALL)
        if total_match:
            coverage_percent = float(total_match.group(1))
        
        if files:
            return {
                'files': files,
                'total_statements': total_statements,
                'missing_statements': missing_statements,
                'excluded_statements': excluded_statements,
                'coverage_percent': coverage_percent
            }
        
        return None
    
    def _try_text_coverage_format(self, text: str) -> Optional[Dict[str, Any]]:
        """Try to parse text format coverage reports."""
        lines = text.splitlines()
        files = []
        total_statements = 0
        missing_statements = 0
        excluded_statements = 0
        coverage_percent = 0.0
        
        for line in lines:
            line = line.strip()
            
            # Parse file lines
            match = re.match(r'^([^\s]+\.py)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)%\s*$', line)
            if match:
                filename = match.group(1)
                statements = int(match.group(2))
                missing = int(match.group(3))
                excluded = int(match.group(4))
                percent = float(match.group(5))
                
                files.append(CoverageFile(
                    filename=filename,
                    statements=statements,
                    missing=missing,
                    excluded=excluded,
                    coverage_percent=percent
                ))
                
                total_statements += statements
                missing_statements += missing
                excluded_statements += excluded
            
            # Parse total line
            match = re.match(r'^TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)%\s*$', line)
            if match:
                coverage_percent = float(match.group(4))
        
        if files:
            return {
                'files': files,
                'total_statements': total_statements,
                'missing_statements': missing_statements,
                'excluded_statements': excluded_statements,
                'coverage_percent': coverage_percent
            }
        
        return None
    
    def _try_xml_coverage_format(self, text: str) -> Optional[Dict[str, Any]]:
        """Try to parse XML format coverage reports."""
        if '<?xml' not in text and '<coverage' not in text:
            return None
        
        files = []
        
        # Extract overall coverage
        coverage_match = re.search(r'line-rate="([\d.]+)"', text)
        if coverage_match:
            coverage_percent = float(coverage_match.group(1)) * 100
        else:
            coverage_percent = 0.0
        
        # Extract file coverage
        file_pattern = re.compile(r'<package[^>]*name="([^"]*)"[^>]*line-rate="([\d.]+)"', text)
        
        for match in file_pattern.finditer(text):
            filename = match.group(1)
            line_rate = float(match.group(2))
            percent = line_rate * 100
            
            files.append(CoverageFile(
                filename=filename,
                statements=0,  # XML format might not have this detail
                missing=0,
                excluded=0,
                coverage_percent=percent
            ))
        
        if files:
            return {
                'files': files,
                'total_statements': 0,
                'missing_statements': 0,
                'excluded_statements': 0,
                'coverage_percent': coverage_percent
            }
        
        return None
    
    def _parse_basic_coverage(self, text: str) -> Tuple[int, int, int, float]:
        """Basic coverage parsing as fallback."""
        total_statements = 0
        missing_statements = 0
        excluded_statements = 0
        coverage_percent = 0.0
        
        # Try to extract total coverage
        for pattern in self.coverage_patterns['total']:
            match = pattern.search(text)
            if match:
                if len(match.groups()) >= 4:
                    total_statements = int(match.group(1))
                    missing_statements = int(match.group(2))
                    excluded_statements = int(match.group(3))
                    coverage_percent = float(match.group(4))
                else:
                    coverage_percent = float(match.group(1))
                break
        
        # If no total found, try to extract any percentage
        if coverage_percent == 0.0:
            percent_match = re.search(r'(\d+(?:\.\d+)?)%', text)
            if percent_match:
                coverage_percent = float(percent_match.group(1))
        
        return total_statements, missing_statements, excluded_statements, coverage_percent
    
    def _extract_branch_coverage(self, text: str) -> Optional[float]:
        """Extract branch coverage percentage."""
        for pattern in self.coverage_patterns['branch_coverage']:
            match = pattern.search(text)
            if match:
                return float(match.group(1))
        return None
    
    def _extract_line_coverage(self, text: str) -> Optional[float]:
        """Extract line coverage percentage."""
        for pattern in self.coverage_patterns['line_coverage']:
            match = pattern.search(text)
            if match:
                return float(match.group(1))
        return None
    
    def compare_coverage(self, before_text: str, after_text: str) -> CoverageComparison:
        """Compare two coverage reports and provide detailed analysis."""
        before_summary = self.parse_coverage_report(before_text)
        after_summary = self.parse_coverage_report(after_text)
        
        overall_change = after_summary.coverage_percent - before_summary.coverage_percent
        severity = self._classify_change_severity(abs(overall_change))
        
        # Analyze file-level changes
        files_changed, meaningful_changes, trivial_changes = self._analyze_file_changes(before_summary, after_summary)
        
        # Find new and removed files
        new_files, removed_files = self._find_new_removed_files(before_summary, after_summary)
        
        # Generate explanations
        summary_explanation = self._generate_summary_explanation(
            overall_change, severity, len(meaningful_changes), len(trivial_changes)
        )
        
        recommendations = self._generate_recommendations(
            severity, meaningful_changes, overall_change
        )
        
        return CoverageComparison(
            before=before_summary,
            after=after_summary,
            overall_change=overall_change,
            severity=severity,
            files_changed=files_changed,
            meaningful_changes=meaningful_changes,
            trivial_changes=trivial_changes,
            new_files=new_files,
            removed_files=removed_files,
            summary_explanation=summary_explanation,
            recommendations=recommendations
        )
    
    def _analyze_file_changes(self, before: CoverageSummary, after: CoverageSummary) -> Tuple[List[CoverageChange], List[CoverageChange], List[CoverageChange]]:
        """Analyze changes at file level."""
        files_changed = []
        meaningful_changes = []
        trivial_changes = []
        
        # Create dictionaries for easy lookup
        before_files = {f.filename: f for f in before.files}
        after_files = {f.filename: f for f in after.files}
        
        # Analyze changed files
        all_filenames = set(before_files.keys()) | set(after_files.keys())
        
        for filename in all_filenames:
            before_file = before_files.get(filename)
            after_file = after_files.get(filename)
            
            if before_file and after_file:
                # File exists in both reports
                change = self._calculate_file_change(before_file, after_file)
                files_changed.append(change)
                
                if abs(change.absolute_change) >= self.MEANINGFUL_CHANGE_THRESHOLD:
                    meaningful_changes.append(change)
                else:
                    trivial_changes.append(change)
        
        return files_changed, meaningful_changes, trivial_changes
    
    def _calculate_file_change(self, before_file: CoverageFile, after_file: CoverageFile) -> CoverageChange:
        """Calculate detailed change for a single file."""
        before_percent = before_file.coverage_percent
        after_percent = after_file.coverage_percent
        absolute_change = after_percent - before_percent
        
        # Calculate relative change
        if before_percent > 0:
            relative_change = (absolute_change / before_percent) * 100
        else:
            relative_change = 0.0
        
        statements_change = after_file.statements - before_file.statements
        missing_change = after_file.missing - before_file.missing
        severity = self._classify_change_severity(abs(absolute_change))
        
        impact_explanation = self._generate_file_impact_explanation(
            before_percent, after_percent, absolute_change, statements_change, missing_change
        )
        
        return CoverageChange(
            filename=before_file.filename,
            before_percent=before_percent,
            after_percent=after_percent,
            absolute_change=absolute_change,
            relative_change=relative_change,
            statements_change=statements_change,
            missing_change=missing_change,
            severity=severity,
            impact_explanation=impact_explanation
        )
    
    def _find_new_removed_files(self, before: CoverageSummary, after: CoverageSummary) -> Tuple[List[CoverageFile], List[CoverageFile]]:
        """Find files that were added or removed."""
        before_filenames = {f.filename for f in before.files}
        after_filenames = {f.filename for f in after.files}
        
        new_files = [f for f in after.files if f.filename not in before_filenames]
        removed_files = [f for f in before.files if f.filename not in after_filenames]
        
        return new_files, removed_files
    
    def _classify_change_severity(self, absolute_change: float) -> ChangeSeverity:
        """Classify the severity of a coverage change."""
        for severity, threshold in self.SEVERITY_THRESHOLDS.items():
            if absolute_change < threshold:
                return severity
        return ChangeSeverity.CRITICAL
    
    def _generate_summary_explanation(self, overall_change: float, severity: ChangeSeverity, meaningful_count: int, trivial_count: int) -> str:
        """Generate a plain English summary explanation."""
        direction = "increased" if overall_change > 0 else "decreased"
        abs_change = abs(overall_change)
        
        explanation = f"Overall code coverage {direction} by {abs_change:.1f}% "
        
        if severity == ChangeSeverity.TRIVIAL:
            explanation += "(this is a trivial change and can be ignored). "
        elif severity == ChangeSeverity.MINOR:
            explanation += "(minor change, likely due to small code modifications). "
        elif severity == ChangeSeverity.MODERATE:
            explanation += "(moderate change that warrants attention). "
        elif severity == ChangeSeverity.SIGNIFICANT:
            explanation += "(significant change that requires investigation). "
        else:
            explanation += "(critical change that needs immediate attention). "
        
        explanation += f"Analyzed {meaningful_count} meaningful file changes and {trivial_count} trivial changes. "
        
        if overall_change > 0:
            explanation += "This improvement suggests better test coverage or code refactoring."
        elif overall_change < 0:
            explanation += "This decline may indicate new code without adequate tests or removed tests."
        
        return explanation
    
    def _generate_file_impact_explanation(self, before_percent: float, after_percent: float, absolute_change: float, statements_change: int, missing_change: int) -> str:
        """Generate impact explanation for a single file."""
        direction = "improved" if absolute_change > 0 else "declined"
        
        explanation = f"Coverage {direction} from {before_percent:.1f}% to {after_percent:.1f}% "
        
        if statements_change != 0:
            if statements_change > 0:
                explanation += f"(added {statements_change} statements, "
            else:
                explanation += f"(removed {abs(statements_change)} statements, "
        
        if missing_change != 0:
            if missing_change > 0:
                explanation += f"{missing_change} new uncovered lines)"
            else:
                explanation += f"{abs(missing_change)} fewer uncovered lines)"
        else:
            explanation += "no change in uncovered lines)"
        
        return explanation
    
    def _generate_recommendations(self, severity: ChangeSeverity, meaningful_changes: List[CoverageChange], overall_change: float) -> List[str]:
        """Generate actionable recommendations based on coverage analysis."""
        recommendations = []
        
        if severity in [ChangeSeverity.SIGNIFICANT, ChangeSeverity.CRITICAL]:
            if overall_change < 0:
                recommendations.append("CRITICAL: Significant coverage decline detected. Review new code for adequate test coverage.")
                recommendations.append("Consider adding tests for recently modified or new files.")
            else:
                recommendations.append("EXCELLENT: Significant coverage improvement detected. This is great progress!")
        
        if meaningful_changes:
            recommendations.append(f"{len(meaningful_changes)} files have meaningful coverage changes. Focus on:")
            
            # Suggest specific actions based on change types
            for change in meaningful_changes[:3]:  # Top 3 changes
                if change.absolute_change < -2:  # Significant drop
                    recommendations.append(f"   - {change.filename}: Coverage dropped by {abs(change.absolute_change):.1f}%. Add tests.")
                elif change.absolute_change > 2:  # Significant improvement
                    recommendations.append(f"   - {change.filename}: Coverage improved by {change.absolute_change:.1f}%. Good work!")
        
        if severity == ChangeSeverity.TRIVIAL:
            recommendations.append("The coverage change is trivial and can be safely ignored.")
        
        if severity == ChangeSeverity.MINOR:
            recommendations.append("Minor coverage change detected. Consider reviewing if intentional.")
        
        return recommendations
    
    def generate_coverage_report(self, before_text: str, after_text: str) -> str:
        """Generate a human-readable coverage comparison report."""
        comparison = self.compare_coverage(before_text, after_text)
        
        report = []
        report.append("# Coverage Analysis Report")
        report.append("")
        
        # Summary section
        report.append("## Summary")
        report.append(f"- **Overall Change**: {comparison.overall_change:+.1f}%")
        report.append(f"- **Severity**: {comparison.severity.value.title()}")
        report.append(f"- **Files Changed**: {len(comparison.files_changed)}")
        report.append(f"- **Meaningful Changes**: {len(comparison.meaningful_changes)}")
        report.append(f"- **Trivial Changes**: {len(comparison.trivial_changes)}")
        report.append("")
        
        # Explanation
        report.append("## Analysis")
        report.append(comparison.summary_explanation)
        report.append("")
        
        # Detailed file changes
        if comparison.meaningful_changes:
            report.append("## Meaningful File Changes")
            for change in comparison.meaningful_changes:
                report.append(f"### {change.filename}")
                report.append(f"- **Before**: {change.before_percent:.1f}%")
                report.append(f"- **After**: {change.after_percent:.1f}%")
                report.append(f"- **Change**: {change.absolute_change:+.1f}%")
                report.append(f"- **Impact**: {change.impact_explanation}")
                report.append("")
        
        if comparison.trivial_changes and len(comparison.trivial_changes) <= 5:
            report.append("## Trivial Changes (ignored)")
            for change in comparison.trivial_changes:
                report.append(f"- **{change.filename}**: {change.before_percent:.1f}% → {change.after_percent:.1f}% ({change.absolute_change:+.1f}%)")
            report.append("")
        
        # New and removed files
        if comparison.new_files:
            report.append("## New Files")
            for file in comparison.new_files:
                report.append(f"- **{file.filename}**: {file.coverage_percent:.1f}% coverage")
            report.append("")
        
        if comparison.removed_files:
            report.append("## Removed Files")
            for file in comparison.removed_files:
                report.append(f"- **{file.filename}**: Had {file.coverage_percent:.1f}% coverage")
            report.append("")
        
        # Recommendations
        if comparison.recommendations:
            report.append("## Recommendations")
            for recommendation in comparison.recommendations:
                report.append(f"- {recommendation}")
            report.append("")
        
        return "\n".join(report)


# Convenience functions for backward compatibility
def compare_coverage(before_text: str, after_text: str) -> dict:
    """Analyze coverage comparison with enhanced detection."""
    import json, enum, dataclasses
    class EnumEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, enum.Enum): return obj.value
            if dataclasses.is_dataclass(obj): return dataclasses.asdict(obj)
            return super().default(obj)
    analyzer = EnhancedCoverageAnalyzer()
    res = analyzer.compare_coverage(before_text, after_text)
    return json.loads(json.dumps(res, cls=EnumEncoder))


def generate_coverage_report(before_text: str, after_text: str) -> str:
    """Generate human-readable coverage report."""
    analyzer = EnhancedCoverageAnalyzer()
    return analyzer.generate_coverage_report(before_text, after_text)


def parse_coverage_enhanced(text: str) -> CoverageSummary:
    """Enhanced coverage parsing with multiple format support."""
    analyzer = EnhancedCoverageAnalyzer()
    return analyzer.parse_coverage_report(text)