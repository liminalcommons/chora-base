#!/usr/bin/env python3
"""
SAP-028 OIDC Publishing Validation

Validates that a project correctly adopts SAP-028 OIDC trusted publishing.

Usage:
    # Validate current directory
    python scripts/sap028-validate.py

    # Validate specific project
    python scripts/sap028-validate.py --project /path/to/project

    # CI/CD mode (exit 1 on failure)
    python scripts/sap028-validate.py --strict
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple



# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def check_workflow_exists(project_dir: Path) -> Tuple[bool, str]:
    """Check if release workflow exists"""
    workflow_paths = [
        project_dir / ".github" / "workflows" / "release.yml",
        project_dir / ".github" / "workflows" / "release.yaml",
        project_dir / ".github" / "workflows" / "publish.yml",
        project_dir / ".github" / "workflows" / "publish.yaml",
    ]

    for workflow_path in workflow_paths:
        if workflow_path.exists():
            return True, str(workflow_path.relative_to(project_dir))

    return False, "No release workflow found (.github/workflows/release.yml)"


def check_oidc_permissions(workflow_path: Path) -> Tuple[bool, str]:
    """Check if workflow has id-token: write permission"""
    content = workflow_path.read_text()

    if "id-token: write" in content:
        return True, "OIDC permissions configured (id-token: write)"

    return False, "Missing 'id-token: write' permission (required for OIDC)"


def check_pypi_action(workflow_path: Path) -> Tuple[bool, str]:
    """Check if workflow uses pypa/gh-action-pypi-publish"""
    content = workflow_path.read_text()

    if "pypa/gh-action-pypi-publish" in content:
        return True, "Using pypa/gh-action-pypi-publish action"

    if "twine upload" in content:
        return False, "Using twine (legacy token-based publishing)"

    return False, "PyPI publish action not found"


def check_attestations(workflow_path: Path) -> Tuple[bool, str]:
    """Check if PEP 740 attestations are enabled"""
    content = workflow_path.read_text()

    if "attestations: true" in content:
        return True, "PEP 740 attestations enabled"

    return False, "PEP 740 attestations not enabled (add 'attestations: true')"


def check_no_token_secrets(workflow_path: Path) -> Tuple[bool, str]:
    """Check that workflow doesn't use PYPI_API_TOKEN"""
    content = workflow_path.read_text()

    if "PYPI_API_TOKEN" in content:
        return False, "Found PYPI_API_TOKEN reference (should use OIDC instead)"

    return True, "No token secrets found (OIDC-only)"


def check_pyproject_toml(project_dir: Path) -> Tuple[bool, str]:
    """Check if pyproject.toml exists"""
    pyproject_path = project_dir / "pyproject.toml"

    if pyproject_path.exists():
        return True, "pyproject.toml exists"

    return False, "pyproject.toml not found"


def validate_project(project_dir: Path, strict: bool = False) -> Dict:
    """Validate SAP-028 OIDC publishing adoption"""
    results = {
        "project": str(project_dir),
        "checks": [],
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "compliant": False
    }

    # Check 1: Workflow exists
    check_result, message = check_workflow_exists(project_dir)
    results["checks"].append({
        "check": "Release workflow exists",
        "passed": check_result,
        "message": message,
        "severity": "error" if not check_result else "info"
    })

    if not check_result:
        results["failed"] += 1
        results["compliant"] = False
        return results

    # Find workflow path
    workflow_path = None
    for path in [".github/workflows/release.yml", ".github/workflows/release.yaml",
                 ".github/workflows/publish.yml", ".github/workflows/publish.yaml"]:
        full_path = project_dir / path
        if full_path.exists():
            workflow_path = full_path
            break

    results["passed"] += 1

    # Check 2: OIDC permissions
    check_result, message = check_oidc_permissions(workflow_path)
    results["checks"].append({
        "check": "OIDC permissions configured",
        "passed": check_result,
        "message": message,
        "severity": "error" if not check_result else "info"
    })
    if check_result:
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Check 3: PyPI action
    check_result, message = check_pypi_action(workflow_path)
    results["checks"].append({
        "check": "Using pypa/gh-action-pypi-publish",
        "passed": check_result,
        "message": message,
        "severity": "error" if not check_result else "info"
    })
    if check_result:
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Check 4: PEP 740 attestations
    check_result, message = check_attestations(workflow_path)
    results["checks"].append({
        "check": "PEP 740 attestations enabled",
        "passed": check_result,
        "message": message,
        "severity": "warning" if not check_result else "info"
    })
    if check_result:
        results["passed"] += 1
    else:
        results["warnings"] += 1

    # Check 5: No token secrets
    check_result, message = check_no_token_secrets(workflow_path)
    results["checks"].append({
        "check": "No PYPI_API_TOKEN secrets",
        "passed": check_result,
        "message": message,
        "severity": "warning" if not check_result else "info"
    })
    if check_result:
        results["passed"] += 1
    else:
        results["warnings"] += 1

    # Check 6: pyproject.toml exists
    check_result, message = check_pyproject_toml(project_dir)
    results["checks"].append({
        "check": "pyproject.toml exists",
        "passed": check_result,
        "message": message,
        "severity": "info"
    })
    if check_result:
        results["passed"] += 1

    # Determine compliance
    critical_checks = [c for c in results["checks"] if c["severity"] == "error"]
    critical_failures = [c for c in critical_checks if not c["passed"]]
    results["compliant"] = len(critical_failures) == 0

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate SAP-028 OIDC trusted publishing adoption"
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Project directory to validate (default: current directory)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 on validation failure (CI/CD mode)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    project_dir = Path(args.project).resolve()

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}", file=sys.stderr)
        return 1

    results = validate_project(project_dir, args.strict)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0 if results["compliant"] else 1

    # Human-readable output
    print("=" * 80)
    print("SAP-028 OIDC Publishing Validation")
    print("=" * 80)
    print(f"Project: {results['project']}")
    print()

    for check in results["checks"]:
        if check["passed"]:
            icon = "✅"
        elif check["severity"] == "warning":
            icon = "⚠️ "
        else:
            icon = "❌"

        print(f"{icon} {check['check']}")
        print(f"   {check['message']}")
        print()

    print("=" * 80)
    print(f"Summary: {results['passed']} passed, {results['failed']} failed, {results['warnings']} warnings")

    if results["compliant"]:
        print("✅ Project is SAP-028 compliant!")
        return 0
    else:
        print("❌ Project is NOT SAP-028 compliant")
        return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
