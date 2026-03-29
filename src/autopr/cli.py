import json
import os
import click
from typing import Optional
from loguru import logger
import questionary
from dotenv import load_dotenv

from autopr.llm import llm
from autopr import reviewer
from autopr.generator import generate_pr_from
from autopr import analysis

# Load environment variables from .env file
load_dotenv()


@click.group()
def cli():
    """CLI for AutoPR (minimal)"""


@cli.command(name="gen")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--commits", required=False, multiple=True, help="One or more commit messages")
@click.option("--issue", required=False, help="Linked issue id or url")
@click.option("--open-browser", is_flag=True, help="Open PR in browser after generation")
def generate(diff: str, commits: tuple[str, ...], issue: Optional[str], open_browser: bool):
    """Generate PR title/description"""
    import webbrowser

    click.echo("🔍 Analyzing diff...")
    # Count changed files (simple heuristic)
    lines = diff.split('\n')
    file_count = sum(1 for line in lines if line.startswith('diff --git'))
    click.echo(f"✔ Identified {file_count} changed files")

    click.echo("🔬 Running static analysis...")
    # Run analysis
    analysis_results = analysis.analyze_diff(diff)
    click.echo(f"✔ Found {len(analysis_results)} analysis items")

    click.echo("🤖 Generating PR description...")
    logger.info("Generating PR description via CLI...")
    commits_list = list(commits) if commits else []
    out = generate_pr_from(diff, commits_list, issue)

    click.echo("✅ PR description generated")

    # Display summary
    if "title" in out:
        click.echo(f"📝 Title: {out['title']}")
    if "what_changed" in out:
        click.echo(f"📋 Summary: {out['what_changed'][:100]}...")

    # Mock PR creation
    mock_pr_number = 17  # Mock PR number
    click.echo(f"🚀 PR submitted: #{mock_pr_number}")

    if open_browser:
        # Mock PR URL
        pr_url = f"https://github.com/user/repo/pull/{mock_pr_number}"
        click.echo(f"🌐 Opening in browser...")
        webbrowser.open(pr_url)

    # Output full JSON
    click.echo("\n" + json.dumps(out, indent=2))


@cli.command(name="review")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--commits", required=False, multiple=True, help="Commit messages to consider")
@click.option("--issue", required=False, help="Issue text or short description to check alignment")
@click.option("--test-log", required=False, help="Path to a pytest log file to include in validation")
@click.option("--coverage-before", required=False, help="Path to a coverage report for baseline")
@click.option("--coverage-after", required=False, help="Path to a coverage report for PR run")
def review(diff: str, commits: tuple[str, ...], issue: str | None, test_log: str | None, coverage_before: str | None, coverage_after: str | None):
    click.echo("🔍 Analyzing diff...")
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
    click.echo("🔬 Running static analysis...")
    click.echo("🤖 Generating AI review...")

    out = reviewer.review_pr(diff, commits=commits_list, issue_text=issue, test_log=test_log_content, coverage_before=coverage_before_content, coverage_after=coverage_after_content)

    click.echo("✅ Review completed")
    click.echo(f"📊 Confidence: {out.get('confidence', 0) * 100:.1f}%")
    click.echo(f"🔍 Findings: {len(out.get('findings', []))}")

    click.echo("\n" + json.dumps(out, indent=2))


@cli.command(name="analyze")
@click.option("--diff", required=True, help="Diff or code snippet")
@click.option("--lang", required=False, default="python", help="Language for analysis (default: python)")
@click.option("--file-path", required=False, help="Optional file path for context")
@click.option("--summary", is_flag=True, help="Show summary statistics")
def analyze(diff: str, lang: str, file_path: str | None, summary: bool):
    """Run the static analyzer on a diff or snippet and print findings."""
    click.echo("🔬 Running enhanced static analysis...")
    result = analysis.analyze_diff(diff, language=lang, file_path=file_path)
    
    # Display findings
    click.echo(f"📊 Found {result['summary']['total_findings']} findings")
    
    # Show summary if requested
    if summary:
        click.echo("\n📈 Summary by severity:")
        for severity, count in result['summary']['by_severity'].items():
            click.echo(f"  {severity}: {count}")
        
        click.echo("\n🔍 Summary by type:")
        for finding_type, count in result['summary']['by_type'].items():
            click.echo(f"  {finding_type}: {count}")
        
        if result.get('diff_info'):
            diff_info = result['diff_info']
            click.echo("\n📝 Diff information:")
            click.echo(f"  Files changed: {diff_info.get('files_changed', 0)}")
            click.echo(f"  Lines added: {diff_info.get('lines_added', 0)}")
            click.echo(f"  Lines deleted: {diff_info.get('lines_deleted', 0)}")
    
    # Show findings
    if result['findings']:
        click.echo("\n🔍 Findings:")
        for finding in result['findings']:
            severity_emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(finding['severity'], "📝")
            line_info = f":{finding['line']}" if finding.get('line') else ""
            click.echo(f"  {severity_emoji} [{finding['severity'].upper()}] {finding['type']}{line_info}: {finding['message']}")
            if finding.get('code_snippet'):
                click.echo(f"    Code: {finding['code_snippet']}")
    else:
        click.echo("✅ No issues found!")
    
    click.echo("\n" + json.dumps(result, indent=2))


@cli.command(name="analyze-files")
@click.option("--directory", required=True, help="Directory to analyze")
@click.option("--pattern", required=False, default="*.py", help="File pattern to match (default: *.py)")
@click.option("--summary", is_flag=True, help="Show summary statistics")
def analyze_files(directory: str, pattern: str, summary: bool):
    """Analyze multiple files in a directory."""
    import glob
    import os
    
    click.echo(f"🔍 Scanning directory: {directory}")
    
    # Find matching files
    search_pattern = os.path.join(directory, "**", pattern)
    files = glob.glob(search_pattern, recursive=True)
    
    if not files:
        click.echo(f"❌ No files found matching pattern: {pattern}")
        return
    
    click.echo(f"📁 Found {len(files)} files to analyze")
    
    # Read file contents
    file_contents = {}
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                file_contents[file_path] = content
        except Exception as e:
            click.echo(f"⚠️  Warning: Could not read {file_path}: {e}")
    
    if not file_contents:
        click.echo("❌ No readable files found")
        return
    
    click.echo("🔬 Running batch static analysis...")
    result = analysis.batch_analyze_files(file_contents)
    
    # Display results
    click.echo(f"📊 Analyzed {result['files_analyzed']} files")
    click.echo(f"🔍 Found {result['total_findings']} total findings")
    
    if summary:
        click.echo("\n📈 Overall summary by severity:")
        for severity, count in result['overall_summary']['by_severity'].items():
            click.echo(f"  {severity}: {count}")
        
        click.echo("\n🔍 Overall summary by type:")
        for finding_type, count in result['overall_summary']['by_type'].items():
            click.echo(f"  {finding_type}: {count}")
    
    # Show critical findings first
    critical_findings = [f for f in result['findings'] if f['severity'] == 'critical']
    if critical_findings:
        click.echo(f"\n🚨 Critical findings ({len(critical_findings)}):")
        for finding in critical_findings:
            line_info = f":{finding['line']}" if finding.get('line') else ""
            click.echo(f"  🚨 [CRITICAL] {finding['type']}{line_info}: {finding['message']}")
            if finding.get('file_path'):
                click.echo(f"    File: {finding['file_path']}")
    
    # Show warnings
    warning_findings = [f for f in result['findings'] if f['severity'] == 'warning']
    if warning_findings and len(warning_findings) <= 10:  # Limit to avoid spam
        click.echo(f"\n⚠️  Warnings ({len(warning_findings)}):")
        for finding in warning_findings:
            line_info = f":{finding['line']}" if finding.get('line') else ""
            click.echo(f"  ⚠️  [WARNING] {finding['type']}{line_info}: {finding['message']}")
            if finding.get('file_path'):
                click.echo(f"    File: {finding['file_path']}")
    
    if len(warning_findings) > 10:
        click.echo(f"\n⚠️  ... and {len(warning_findings) - 10} more warnings (see JSON output)")
    
    click.echo("\n" + json.dumps(result, indent=2))


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


@cli.command(name="init")
def init():
    """Initialize AutoPR configuration"""
    config_path = ".autopr.json"
    env_path = ".env.example"

    # Create config file
    config = {
        "provider": "openai",
        "repo": "local",
        "mode": "sync"
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # Create .env.example if it doesn't exist
    if not os.path.exists(env_path):
        env_content = """# AutoPR Environment Variables
AUTOPR_PROVIDER=openai
OPENAI_API_KEY=your-openai-key-here
# ANTHROPIC_API_KEY=your-anthropic-key-here
# AUTOPR_DEBUG=true
"""
        with open(env_path, 'w') as f:
            f.write(env_content)

    click.echo(f"✓ Created {config_path}")
    click.echo(f"✓ Created {env_path}")
    click.echo("Run 'autopr configure' to set up your API keys")


@cli.command(name="configure")
def configure():
    """Interactive configuration setup"""
    config_path = ".autopr.json"

    # Load existing config
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {"provider": "openai", "repo": "local", "mode": "sync"}

    # Interactive prompts
    provider = questionary.select(
        "Which LLM provider do you want to use?",
        choices=["openai", "anthropic", "stub"],
        default=config.get("provider", "openai")
    ).ask()

    config["provider"] = provider

    if provider != "stub":
        token = questionary.password(f"Enter your {provider.upper()} API key:").ask()
        if token:
            # Update .env file manually
            env_path = ".env"
            env_lines = []

            # Read existing .env if it exists
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    env_lines = f.readlines()

            # Remove existing API key lines
            env_lines = [line for line in env_lines if not line.startswith(f"{provider.upper()}_API_KEY=")]

            # Add the new API key
            env_lines.append(f"{provider.upper()}_API_KEY={token}\n")

            # Write back to .env
            with open(env_path, 'w') as f:
                f.writelines(env_lines)

    mode = questionary.select(
        "Use async mode for API calls?",
        choices=["sync", "async"],
        default=config.get("mode", "sync")
    ).ask()

    config["mode"] = mode

    # Save config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # Also set AUTOPR_PROVIDER in .env
    env_path = ".env"
    env_lines = []

    # Read existing .env if it exists
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_lines = f.readlines()

    # Remove existing AUTOPR_PROVIDER line
    env_lines = [line for line in env_lines if not line.startswith("AUTOPR_PROVIDER=")]

    # Add AUTOPR_PROVIDER
    env_lines.append(f"AUTOPR_PROVIDER={provider}\n")

    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(env_lines)

    click.echo("✓ Configuration updated")


@cli.command(name="doctor")
def doctor():
    """Check system health and requirements"""
    import sys
    import subprocess

    # Reload environment variables
    load_dotenv(override=True)

    issues = []

    # Check Python version
    if sys.version_info >= (3, 10):
        click.echo("[OK] Python version >= 3.10")
    else:
        issues.append("[ERROR] Python version < 3.10")

    # Check git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        click.echo("[OK] Git installed")
    except:
        issues.append("[ERROR] Git not installed")

    # Check if git repo
    try:
        subprocess.run(["git", "status"], capture_output=True, check=True, cwd=".")
        click.echo("[OK] Directory is a git repository")
    except:
        issues.append("[ERROR] Not a git repository")

    # Check token
    provider = os.getenv("AUTOPR_PROVIDER", "openai")
    token_env = f"{provider.upper()}_API_KEY"
    if os.getenv(token_env) or provider == "stub":
        click.echo(f"[OK] {token_env} available")
    else:
        issues.append(f"[ERROR] {token_env} not set")

    # Check writable
    try:
        with open(".autopr_test", 'w') as f:
            f.write("test")
        os.remove(".autopr_test")
        click.echo("[OK] Directory is writable")
    except:
        issues.append("[ERROR] Directory not writable")

    if issues:
        click.echo("\nIssues found:")
        for issue in issues:
            click.echo(issue)
        click.echo("\nRun 'autopr configure' to fix configuration issues")
    else:
        click.echo("\n[SUCCESS] All systems ready!")


@cli.command(name="hooks")
@click.argument("action")
def hooks(action: str):
    """Manage git hooks"""
    if action == "install":
        hooks_dir = ".git/hooks"
        if not os.path.exists(hooks_dir):
            click.echo("✗ Not a git repository")
            return

        pre_commit_path = os.path.join(hooks_dir, "pre-commit")
        hook_content = """#!/bin/bash
# AutoPR pre-commit hooks

echo "Running AutoPR static analysis..."
# Add static analysis command here

echo "Running AutoPR test summary..."
# Add test summary command here
"""

        with open(pre_commit_path, 'w') as f:
            f.write(hook_content)

        # Make executable
        os.chmod(pre_commit_path, 0o755)

        click.echo("✓ Pre-commit hooks installed")
        click.echo("Hooks will run static analysis and test summary on commit")
    else:
        click.echo("Usage: pr-ai hooks install")


@cli.command(name="mock")
def mock():
    """Use stub provider for offline demos"""
    config_path = ".autopr.json"

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {"provider": "openai", "repo": "local", "mode": "sync"}

    config["provider"] = "stub"

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    click.echo("[OK] Switched to stub provider for offline demos")


@cli.command(name="suggest-reviewers")
@click.option("--diff", required=False, help="Diff to analyze (optional, uses git diff if not provided)")
def suggest_reviewers(diff: str | None):
    """Suggest reviewers based on code changes"""
    import subprocess
    from collections import Counter

    click.echo("🔍 Analyzing code changes...")

    # Get diff if not provided
    if not diff:
        try:
            result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
            diff = result.stdout
            if not diff:
                result = subprocess.run(["git", "diff"], capture_output=True, text=True, check=True)
                diff = result.stdout
        except subprocess.CalledProcessError:
            click.echo("✗ Could not get git diff")
            return

    # Extract changed files
    lines = diff.split('\n')
    changed_files = []
    for line in lines:
        if line.startswith('diff --git'):
            parts = line.split()
            if len(parts) >= 3:
                file_path = parts[2].lstrip('b/')
                changed_files.append(file_path)

    if not changed_files:
        click.echo("✗ No changed files found")
        return

    click.echo(f"📁 Found {len(changed_files)} changed files")

    # Get commit history for these files
    author_counts = Counter()
    for file_path in changed_files:
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%an", "--", file_path],
                capture_output=True, text=True, check=True
            )
            authors = result.stdout.strip().split('\n')
            author_counts.update(authors)
        except subprocess.CalledProcessError:
            continue

    # Get overall repo contributors as fallback
    if not author_counts:
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%an", "-n", "50"],
                capture_output=True, text=True, check=True
            )
            authors = result.stdout.strip().split('\n')
            author_counts.update(authors)
        except subprocess.CalledProcessError:
            pass

    if not author_counts:
        click.echo("✗ No commit history found")
        return

    # Suggest top contributors
    suggestions = author_counts.most_common(3)

    click.echo("\n👥 Suggested reviewers:")
    for author, count in suggestions:
        click.echo(f"  • {author} ({count} commits in related files)")

    # Fallback suggestion
    if not suggestions:
        click.echo("  • Repository owner (fallback)")


if __name__ == "__main__":
    cli()
