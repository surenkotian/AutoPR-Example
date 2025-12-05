import json
import click
from typing import Optional
from loguru import logger

from autopr.llm import llm
from autopr import reviewer
from autopr.generator import generate_pr_from
from autopr import analysis


@click.group()
def cli():
    """CLI for AutoPR (minimal)"""


@cli.command(name="gen")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--commits", required=False, multiple=True, help="One or more commit messages")
@click.option("--issue", required=False, help="Linked issue id or url")
def generate(diff: str, commits: tuple[str, ...], issue: Optional[str]):
    """Generate PR title/description (mock)"""
    logger.info("Generating PR description via CLI...")
    commits_list = list(commits) if commits else []
    out = generate_pr_from(diff, commits_list, issue)
    click.echo(json.dumps(out, indent=2))


@cli.command(name="review")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--commits", required=False, multiple=True, help="Commit messages to consider")
@click.option("--issue", required=False, help="Issue text or short description to check alignment")
@click.option("--test-log", required=False, help="Path to a pytest log file to include in validation")
@click.option("--coverage-before", required=False, help="Path to a coverage report for baseline")
@click.option("--coverage-after", required=False, help="Path to a coverage report for PR run")
def review(diff: str, commits: tuple[str, ...], issue: str | None, test_log: str | None, coverage_before: str | None, coverage_after: str | None):
    logger.info("Reviewing PR via CLI...")
    # Gather options passed by Click
    commits_list = list(commits) if commits else []

    test_log_content = None
    if test_log:
        try:
            with open(test_log, 'r', encoding='utf-8') as f:
                test_log_content = f.read()
        except Exception as e:
            click.echo(f"Warning: failed to read test log: {e}")

    coverage_before_content = None
    coverage_after_content = None
    if coverage_before:
        try:
            with open(coverage_before, 'r', encoding='utf-8') as f:
                coverage_before_content = f.read()
        except Exception as e:
            click.echo(f"Warning: failed to read coverage_before: {e}")
    if coverage_after:
        try:
            with open(coverage_after, 'r', encoding='utf-8') as f:
                coverage_after_content = f.read()
        except Exception as e:
            click.echo(f"Warning: failed to read coverage_after: {e}")
    out = reviewer.review_pr(diff, commits=commits_list, issue_text=issue, test_log=test_log_content, coverage_before=coverage_before_content, coverage_after=coverage_after_content)
    click.echo(json.dumps(out, indent=2))


@cli.command(name="analyze")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--lang", required=False, default="python", help="Language for analysis (default: python)")
def analyze(diff: str, lang: str):
    """Run the static analyzer on a diff or snippet and print findings."""
    out = analysis.analyze_diff(diff, language=lang)
    click.echo(json.dumps(out, indent=2))


@cli.command(name="ci-parse")
@click.option("--log", required=True, help="Path to pytest log or CI log file")
def ci_parse(log: str):
    """Parse a pytest/CI log and print a summary."""
    from autopr import ci_parser
    try:
        with open(log, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        click.echo(f"Failed to read log: {e}")
        return
    out = ci_parser.parse_pytest_output(data)
    click.echo(json.dumps(out, indent=2))


@cli.command(name="coverage-compare")
@click.option("--before", required=True, help="Path to before coverage summary")
@click.option("--after", required=True, help="Path to after coverage summary")
def coverage_compare(before: str, after: str):
    from autopr import coverage_utils
    try:
        with open(before, 'r', encoding='utf-8') as f:
            b = f.read()
        with open(after, 'r', encoding='utf-8') as f:
            a = f.read()
    except Exception as e:
        click.echo(f"Failed to read files: {e}")
        return
    out = coverage_utils.compare_coverage(b, a)
    click.echo(json.dumps(out, indent=2))


@cli.command(name="validate-issue")
@click.option("--issue", required=True, help="Issue text to validate")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--commits", required=False, multiple=True, help="Commit messages to use")
def validate_issue(issue: str, diff: str, commits: tuple[str, ...]):
    from autopr import issue_validator
    res = issue_validator.simple_issue_alignment(issue, diff, list(commits))
    click.echo(json.dumps(res, indent=2))


if __name__ == "__main__":
    cli()
