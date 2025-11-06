#!/usr/bin/env python3
"""Validate Model Citizen MCP Server Compliance

This script validates that an MCP server project meets all "model citizen"
requirements from chora-base. It checks 12 key requirements across:

- FastMCP server infrastructure
- Agent awareness (SAP-009)
- Task tracking (SAP-015)
- Memory system (SAP-010)
- Inbox coordination (SAP-001)
- Testing framework (SAP-004)
- CI/CD workflows (SAP-005)
- Quality gates (SAP-006)
- Documentation (SAP-007)

Usage:
    # Validate current directory
    python scripts/validate-model-citizen.py

    # Validate specific directory
    python scripts/validate-model-citizen.py --project-dir ~/projects/my-mcp-server

    # Output as JSON
    python scripts/validate-model-citizen.py --format json

    # Fail on any warning
    python scripts/validate-model-citizen.py --strict
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


VERSION = "1.0.0"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ValidationResult:
    """Result of a single validation check."""
    name: str
    passed: bool
    level: str  # "required" or "recommended"
    message: str
    details: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report for a project."""
    project_dir: Path
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    results: List[ValidationResult] = field(default_factory=list)

    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result and update counters."""
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            if result.level == "required":
                self.failed += 1
            else:
                self.warnings += 1

    def is_compliant(self, strict: bool = False) -> bool:
        """Check if project is model citizen compliant."""
        if strict:
            return self.failed == 0 and self.warnings == 0
        return self.failed == 0

    def to_dict(self) -> Dict:
        """Convert report to dictionary for JSON output."""
        return {
            "project_dir": str(self.project_dir.absolute()),
            "summary": {
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warnings,
                "total": len(self.results),
                "compliant": self.is_compliant(),
            },
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "level": r.level,
                    "message": r.message,
                    "details": r.details,
                }
                for r in self.results
            ],
        }


# ============================================================================
# VALIDATION CHECKS
# ============================================================================

def check_fastmcp_server(project_dir: Path) -> ValidationResult:
    """Check 1: FastMCP server exists and is properly configured."""
    # Try to find server.py in common locations
    server_locations = [
        project_dir / "src" / "**" / "server.py",
    ]

    server_found = False
    has_fastmcp = False
    server_path = None

    for location_pattern in server_locations:
        for server_file in project_dir.glob(str(location_pattern.relative_to(project_dir))):
            server_found = True
            server_path = server_file
            content = server_file.read_text()
            has_fastmcp = "from fastmcp import FastMCP" in content or "import fastmcp" in content
            if has_fastmcp:
                break
        if has_fastmcp:
            break

    if not server_found:
        return ValidationResult(
            name="FastMCP server exists",
            passed=False,
            level="required",
            message="No server.py file found in src/ directory",
            details="Expected: src/{package}/server.py with FastMCP server",
        )

    if not has_fastmcp:
        return ValidationResult(
            name="FastMCP server exists",
            passed=False,
            level="required",
            message=f"server.py found but doesn't import FastMCP: {server_path}",
            details="Expected: 'from fastmcp import FastMCP' in server.py",
        )

    return ValidationResult(
        name="FastMCP server exists",
        passed=True,
        level="required",
        message=f"FastMCP server found: {server_path.relative_to(project_dir)}",
    )


def check_mcp_namespace_module(project_dir: Path) -> ValidationResult:
    """Check 2: MCP namespace module exists with Chora conventions."""
    # Find mcp/__init__.py
    mcp_init_files = list(project_dir.glob("src/**/mcp/__init__.py"))

    if not mcp_init_files:
        return ValidationResult(
            name="MCP namespace module exists",
            passed=False,
            level="required",
            message="No mcp/__init__.py found",
            details="Expected: src/{package}/mcp/__init__.py with namespace helpers",
        )

    mcp_init = mcp_init_files[0]
    content = mcp_init.read_text()

    # Check for Chora MCP Conventions helpers
    has_namespace = "NAMESPACE" in content
    has_helpers = ("make_tool_name" in content and "make_resource_uri" in content)

    if not (has_namespace and has_helpers):
        return ValidationResult(
            name="MCP namespace module exists",
            passed=False,
            level="required",
            message="mcp/__init__.py found but missing Chora MCP Conventions helpers",
            details="Expected: NAMESPACE constant, make_tool_name(), make_resource_uri() functions",
        )

    return ValidationResult(
        name="MCP namespace module exists",
        passed=True,
        level="required",
        message=f"MCP namespace module found: {mcp_init.relative_to(project_dir)}",
    )


def check_agents_md(project_dir: Path) -> ValidationResult:
    """Check 3: AGENTS.md exists with proper YAML frontmatter."""
    agents_md = project_dir / "AGENTS.md"

    if not agents_md.exists():
        return ValidationResult(
            name="AGENTS.md with YAML frontmatter",
            passed=False,
            level="required",
            message="AGENTS.md not found",
            details="Expected: AGENTS.md at project root with YAML frontmatter",
        )

    content = agents_md.read_text()

    # Check for YAML frontmatter (starts with --- and has closing ---)
    has_frontmatter = content.strip().startswith("---")
    if has_frontmatter:
        # Check if frontmatter is properly closed
        lines = content.split("\n")
        closing_found = False
        for i, line in enumerate(lines[1:], 1):  # Skip first ---
            if line.strip() == "---":
                closing_found = True
                break
        has_frontmatter = closing_found

    if not has_frontmatter:
        return ValidationResult(
            name="AGENTS.md with YAML frontmatter",
            passed=False,
            level="required",
            message="AGENTS.md found but missing YAML frontmatter",
            details="Expected: YAML frontmatter with ---...--- delimiters",
        )

    return ValidationResult(
        name="AGENTS.md with YAML frontmatter",
        passed=True,
        level="required",
        message="AGENTS.md found with proper YAML frontmatter",
    )


def check_claude_md(project_dir: Path) -> ValidationResult:
    """Check 4: CLAUDE.md exists for Claude Code integration."""
    claude_md = project_dir / "CLAUDE.md"

    if not claude_md.exists():
        return ValidationResult(
            name="CLAUDE.md exists",
            passed=False,
            level="recommended",
            message="CLAUDE.md not found",
            details="Recommended: CLAUDE.md with Claude Code workflows",
        )

    return ValidationResult(
        name="CLAUDE.md exists",
        passed=True,
        level="recommended",
        message="CLAUDE.md found",
    )


def check_beads_initialization(project_dir: Path) -> ValidationResult:
    """Check 5: Beads task tracking initialized (SAP-015)."""
    beads_dir = project_dir / ".beads"

    if not beads_dir.exists():
        return ValidationResult(
            name="Beads initialized",
            passed=False,
            level="recommended",
            message=".beads/ directory not found",
            details="Recommended: Initialize beads with 'bd init'",
        )

    # Check for required files
    required_files = [
        beads_dir / "issues.jsonl",
        beads_dir / "config.yaml",
        beads_dir / "metadata.json",
    ]

    missing = [f for f in required_files if not f.exists()]

    if missing:
        missing_names = [f.name for f in missing]
        return ValidationResult(
            name="Beads initialized",
            passed=False,
            level="recommended",
            message=f"Beads directory incomplete, missing: {', '.join(missing_names)}",
            details="Expected: issues.jsonl, config.yaml, metadata.json in .beads/",
        )

    return ValidationResult(
        name="Beads initialized",
        passed=True,
        level="recommended",
        message="Beads task tracking initialized",
    )


def check_inbox_initialization(project_dir: Path) -> ValidationResult:
    """Check 6: Inbox coordination initialized (SAP-001)."""
    inbox_dir = project_dir / "inbox" / "coordination"

    if not inbox_dir.exists():
        return ValidationResult(
            name="Inbox initialized",
            passed=False,
            level="recommended",
            message="inbox/coordination/ directory not found",
            details="Recommended: Initialize inbox for cross-repo coordination",
        )

    # Check for required files
    required_files = [
        inbox_dir / "active.jsonl",
        inbox_dir / "events.jsonl",
    ]

    missing = [f for f in required_files if not f.exists()]

    if missing:
        missing_names = [f.name for f in missing]
        return ValidationResult(
            name="Inbox initialized",
            passed=False,
            level="recommended",
            message=f"Inbox incomplete, missing: {', '.join(missing_names)}",
            details="Expected: active.jsonl, events.jsonl in inbox/coordination/",
        )

    return ValidationResult(
        name="Inbox initialized",
        passed=True,
        level="recommended",
        message="Inbox coordination initialized",
    )


def check_memory_initialization(project_dir: Path) -> ValidationResult:
    """Check 7: A-MEM memory system initialized (SAP-010)."""
    memory_dir = project_dir / ".chora" / "memory" / "events"

    if not memory_dir.exists():
        return ValidationResult(
            name="Memory system initialized",
            passed=False,
            level="recommended",
            message=".chora/memory/events/ directory not found",
            details="Recommended: Initialize A-MEM for event-sourced memory",
        )

    # Check for at least one event file
    event_files = list(memory_dir.glob("*.jsonl"))

    if not event_files:
        return ValidationResult(
            name="Memory system initialized",
            passed=False,
            level="recommended",
            message="Memory directory exists but no event files found",
            details="Expected: At least development.jsonl in .chora/memory/events/",
        )

    return ValidationResult(
        name="Memory system initialized",
        passed=True,
        level="recommended",
        message=f"Memory system initialized ({len(event_files)} event file(s))",
    )


def check_testing_framework(project_dir: Path) -> ValidationResult:
    """Check 8: pytest testing framework configured (SAP-004)."""
    # Check for pytest configuration
    pyproject = project_dir / "pyproject.toml"
    pytest_ini = project_dir / "pytest.ini"

    has_config = False
    if pyproject.exists():
        content = pyproject.read_text()
        has_config = "[tool.pytest" in content

    if not has_config and pytest_ini.exists():
        has_config = True

    if not has_config:
        return ValidationResult(
            name="Testing framework configured",
            passed=False,
            level="required",
            message="pytest configuration not found",
            details="Expected: [tool.pytest.ini_options] in pyproject.toml or pytest.ini",
        )

    # Check for tests directory
    tests_dir = project_dir / "tests"
    if not tests_dir.exists():
        return ValidationResult(
            name="Testing framework configured",
            passed=False,
            level="required",
            message="tests/ directory not found",
            details="Expected: tests/ directory with test files",
        )

    return ValidationResult(
        name="Testing framework configured",
        passed=True,
        level="required",
        message="Testing framework configured with tests/ directory",
    )


def check_ci_cd_workflows(project_dir: Path) -> ValidationResult:
    """Check 9: GitHub Actions CI/CD workflows (SAP-005)."""
    workflows_dir = project_dir / ".github" / "workflows"

    if not workflows_dir.exists():
        return ValidationResult(
            name="CI/CD workflows configured",
            passed=False,
            level="recommended",
            message=".github/workflows/ directory not found",
            details="Recommended: GitHub Actions workflows for CI/CD",
        )

    workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))

    if not workflow_files:
        return ValidationResult(
            name="CI/CD workflows configured",
            passed=False,
            level="recommended",
            message=".github/workflows/ exists but no workflow files found",
            details="Expected: At least test.yml and lint.yml workflows",
        )

    # Check for recommended workflows
    workflow_names = [f.stem for f in workflow_files]
    recommended = ["test", "lint"]
    found = [w for w in recommended if w in workflow_names]

    if len(found) < len(recommended):
        missing = [w for w in recommended if w not in workflow_names]
        return ValidationResult(
            name="CI/CD workflows configured",
            passed=True,  # Still pass, but note missing
            level="recommended",
            message=f"CI/CD configured ({len(workflow_files)} workflows), missing recommended: {', '.join(missing)}",
        )

    return ValidationResult(
        name="CI/CD workflows configured",
        passed=True,
        level="recommended",
        message=f"CI/CD workflows configured ({len(workflow_files)} workflows)",
    )


def check_quality_gates(project_dir: Path) -> ValidationResult:
    """Check 10: Quality gates configured (SAP-006)."""
    pyproject = project_dir / "pyproject.toml"

    if not pyproject.exists():
        return ValidationResult(
            name="Quality gates configured",
            passed=False,
            level="required",
            message="pyproject.toml not found",
            details="Expected: pyproject.toml with ruff, mypy configuration",
        )

    content = pyproject.read_text()

    # Check for quality tools
    has_ruff = "[tool.ruff" in content
    has_mypy = "[tool.mypy" in content
    has_coverage = "[tool.coverage" in content

    if not (has_ruff and has_mypy):
        missing = []
        if not has_ruff:
            missing.append("ruff")
        if not has_mypy:
            missing.append("mypy")

        return ValidationResult(
            name="Quality gates configured",
            passed=False,
            level="required",
            message=f"Quality gates incomplete, missing: {', '.join(missing)}",
            details="Expected: [tool.ruff] and [tool.mypy] in pyproject.toml",
        )

    return ValidationResult(
        name="Quality gates configured",
        passed=True,
        level="required",
        message="Quality gates configured (ruff, mypy" + (", coverage)" if has_coverage else ")"),
    )


def check_documentation_structure(project_dir: Path) -> ValidationResult:
    """Check 11: Documentation structure follows Diátaxis (SAP-007)."""
    docs_dir = project_dir / "docs"

    if not docs_dir.exists():
        return ValidationResult(
            name="Documentation structure",
            passed=False,
            level="recommended",
            message="docs/ directory not found",
            details="Recommended: docs/ with user-docs/, dev-docs/, project-docs/",
        )

    # Check for Diátaxis 4-domain structure
    recommended_dirs = ["user-docs", "dev-docs", "project-docs", "skilled-awareness"]
    found_dirs = [d for d in recommended_dirs if (docs_dir / d).exists()]

    if len(found_dirs) < 2:
        return ValidationResult(
            name="Documentation structure",
            passed=False,
            level="recommended",
            message=f"Documentation structure incomplete (found {len(found_dirs)}/4 domains)",
            details=f"Recommended: {', '.join(recommended_dirs)} in docs/",
        )

    return ValidationResult(
        name="Documentation structure",
        passed=True,
        level="recommended",
        message=f"Documentation structure follows Diátaxis ({len(found_dirs)}/4 domains)",
    )


def check_unsubstituted_variables(project_dir: Path) -> ValidationResult:
    """Check 12: No unsubstituted template variables."""
    unsubstituted_files = []

    # Check all .py, .md, .toml, .yml files
    patterns = ["**/*.py", "**/*.md", "**/*.toml", "**/*.yml", "**/*.yaml"]

    for pattern in patterns:
        for file_path in project_dir.glob(pattern):
            # Skip certain directories
            if any(part in file_path.parts for part in [".git", ".venv", "venv", "__pycache__", ".beads", "node_modules"]):
                continue

            try:
                content = file_path.read_text()
                # Check for Jinja2 variables
                if '{{' in content or '}}' in content:
                    unsubstituted_files.append(str(file_path.relative_to(project_dir)))
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                continue

    if unsubstituted_files:
        details = "Files with {{ }} patterns:\n" + "\n".join(f"  - {f}" for f in unsubstituted_files[:10])
        if len(unsubstituted_files) > 10:
            details += f"\n  ... and {len(unsubstituted_files) - 10} more"

        return ValidationResult(
            name="No unsubstituted variables",
            passed=False,
            level="required",
            message=f"{len(unsubstituted_files)} file(s) with unsubstituted template variables",
            details=details,
        )

    return ValidationResult(
        name="No unsubstituted variables",
        passed=True,
        level="required",
        message="No unsubstituted template variables found",
    )


# ============================================================================
# MAIN VALIDATION
# ============================================================================

def validate_project(project_dir: Path) -> ValidationReport:
    """Run all validation checks on a project."""
    report = ValidationReport(project_dir=project_dir)

    # Run all checks
    checks = [
        check_fastmcp_server,
        check_mcp_namespace_module,
        check_agents_md,
        check_claude_md,
        check_beads_initialization,
        check_inbox_initialization,
        check_memory_initialization,
        check_testing_framework,
        check_ci_cd_workflows,
        check_quality_gates,
        check_documentation_structure,
        check_unsubstituted_variables,
    ]

    for check_func in checks:
        result = check_func(project_dir)
        report.add_result(result)

    return report


def print_report(report: ValidationReport, strict: bool = False) -> None:
    """Print validation report in human-readable format."""
    print("=" * 80)
    print(f"Model Citizen MCP Server Validation v{VERSION}")
    print("=" * 80)
    print()
    print(f"Project: {report.project_dir.absolute()}")
    print()

    # Print results
    for result in report.results:
        if result.passed:
            icon = "✅"
        elif result.level == "required":
            icon = "❌"
        else:
            icon = "⚠️ "

        print(f"{icon} {result.name}")
        if not result.passed:
            print(f"   {result.message}")
            if result.details:
                # Indent details
                for line in result.details.split("\n"):
                    print(f"   {line}")

    # Print summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"  Passed:    {report.passed}/{len(report.results)}")
    print(f"  Failed:    {report.failed} required checks")
    print(f"  Warnings:  {report.warnings} recommended checks")
    print()

    if report.is_compliant(strict=strict):
        print("✅ Project is MODEL CITIZEN COMPLIANT!")
        if report.warnings > 0:
            print(f"   ({report.warnings} optional improvement(s) recommended)")
    else:
        if strict and report.warnings > 0:
            print("⚠️  Project has warnings (strict mode)")
        if report.failed > 0:
            print("❌ Project is NOT compliant")
            print(f"   Fix {report.failed} required check(s) above")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate Model Citizen MCP Server compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project directory to validate (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings (recommended checks), not just required checks",
    )

    args = parser.parse_args()

    # Validate project directory exists
    if not args.project_dir.exists():
        print(f"❌ Error: Project directory not found: {args.project_dir}")
        sys.exit(1)

    if not args.project_dir.is_dir():
        print(f"❌ Error: Not a directory: {args.project_dir}")
        sys.exit(1)

    # Run validation
    report = validate_project(args.project_dir)

    # Output results
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print_report(report, strict=args.strict)

    # Exit with appropriate code
    if not report.is_compliant(strict=args.strict):
        sys.exit(1)


if __name__ == "__main__":
    main()
