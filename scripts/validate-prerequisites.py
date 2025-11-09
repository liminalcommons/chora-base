#!/usr/bin/env python3
"""Pre-flight validation for chora-base onboarding.

Purpose: Catch prerequisite issues before install-sap.py runs
Exit codes: 0 = PASS, 1 = FAIL, 2 = USAGE ERROR

Usage:
    python scripts/validate-prerequisites.py
    python scripts/validate-prerequisites.py --json  # JSON output

Based on: COORD-003 Sprint 1 requirements
Target: Catch 90%+ of prerequisite issues before installation failure
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path


# Minimum versions
MIN_PYTHON_VERSION = (3, 8)
MIN_GIT_VERSION = (2, 0)
MIN_DISK_SPACE_MB = 100

# Validation counters
checks_passed = 0
checks_failed = 0
checks_warning = 0
validation_failed = False


def check_tool_version(tool_name, min_version=None):
    """Check if a tool is available and optionally validate version.

    Returns:
        dict with keys: available, version, meets_requirement, status
    """
    tool_path = shutil.which(tool_name)

    if not tool_path:
        return {
            "available": False,
            "version": None,
            "meets_requirement": False,
            "status": "FAIL",
            "message": f"{tool_name} not found in PATH"
        }

    # Get version
    try:
        # Try common version flags
        for flag in ["--version", "-v", "version"]:
            try:
                result = subprocess.run(
                    [tool_path, flag],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version_output = result.stdout or result.stderr
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        else:
            version_output = "unknown"
    except Exception as e:
        version_output = f"error: {e}"

    # Extract version number (first X.Y.Z pattern)
    import re
    version_match = re.search(r'(\d+)\.(\d+)(?:\.(\d+))?', version_output)

    if version_match:
        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        patch = int(version_match.group(3)) if version_match.group(3) else 0
        version_tuple = (major, minor, patch)
        version_str = f"{major}.{minor}.{patch}" if patch else f"{major}.{minor}"
    else:
        version_tuple = None
        version_str = version_output.strip().split('\n')[0][:50]  # First line, truncated

    # Check version requirement
    meets_requirement = True
    if min_version and version_tuple:
        meets_requirement = version_tuple[:len(min_version)] >= min_version

    status = "OK" if meets_requirement else ("WARNING" if version_tuple else "OK")

    return {
        "available": True,
        "version": version_str,
        "version_tuple": version_tuple,
        "meets_requirement": meets_requirement,
        "status": status,
        "message": f"{tool_name} {version_str}"
    }


def validate_python():
    """Validate Python installation and version."""
    global checks_passed, checks_failed, validation_failed

    result = check_tool_version("python3", MIN_PYTHON_VERSION)

    if not result["available"]:
        checks_failed += 1
        validation_failed = True
        result["recommendation"] = "Install Python 3.8+ from: https://www.python.org/downloads/"
        return result

    if not result["meets_requirement"]:
        checks_failed += 1
        validation_failed = True
        result["status"] = "FAIL"
        result["recommendation"] = f"Python {result['version']} found (requires 3.8+). Upgrade from: https://www.python.org/downloads/"
        return result

    checks_passed += 1
    return result


def validate_git():
    """Validate Git installation and version."""
    global checks_passed, checks_warning

    result = check_tool_version("git", MIN_GIT_VERSION)

    if not result["available"]:
        global checks_failed, validation_failed
        checks_failed += 1
        validation_failed = True
        result["recommendation"] = "Install Git from: https://git-scm.com/downloads"
        return result

    if not result["meets_requirement"]:
        checks_warning += 1
        result["status"] = "WARNING"
        result["recommendation"] = f"Git {result['version']} found (recommend 2.0+). Consider upgrading from: https://git-scm.com/downloads"
    else:
        checks_passed += 1

    return result


def validate_directory_structure():
    """Validate expected chora-base directory structure."""
    global checks_passed, checks_failed, validation_failed

    expected_dirs = [
        "docs",
        "docs/skilled-awareness",
        "scripts",
    ]

    missing_dirs = [d for d in expected_dirs if not Path(d).is_dir()]

    if missing_dirs:
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "missing_dirs": missing_dirs,
            "message": "Missing required directories",
            "recommendation": "Are you running from chora-base root directory?"
        }

    checks_passed += 1
    return {
        "status": "OK",
        "message": "Directory structure valid"
    }


def validate_sap_catalog():
    """Validate sap-catalog.json exists and has valid JSON."""
    global checks_passed, checks_failed, validation_failed

    catalog_path = Path("sap-catalog.json")

    if not catalog_path.exists():
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "message": "sap-catalog.json not found",
            "recommendation": "Are you in the chora-base root directory?"
        }

    # Validate JSON syntax
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "message": f"sap-catalog.json has invalid JSON syntax: {e}",
            "recommendation": "Fix JSON syntax errors"
        }

    checks_passed += 1
    return {
        "status": "OK",
        "message": "SAP catalog valid"
    }


def validate_disk_space():
    """Validate available disk space."""
    global checks_passed, checks_warning

    try:
        cwd = Path.cwd()
        disk_usage = shutil.disk_usage(cwd)
        available_mb = disk_usage.free // (1024 * 1024)

        if available_mb < MIN_DISK_SPACE_MB:
            checks_warning += 1
            return {
                "status": "WARNING",
                "available_mb": available_mb,
                "required_mb": MIN_DISK_SPACE_MB,
                "message": f"Low disk space: {available_mb}MB available",
                "recommendation": f"Recommend {MIN_DISK_SPACE_MB}MB+. SAP installation typically uses 50-100MB"
            }

        checks_passed += 1
        return {
            "status": "OK",
            "available_mb": available_mb,
            "message": f"Disk space: {available_mb}MB available"
        }
    except Exception as e:
        checks_warning += 1
        return {
            "status": "WARNING",
            "message": f"Could not check disk space: {e}"
        }


def validate_write_permissions():
    """Validate write permissions for required directories."""
    global checks_passed, checks_failed, validation_failed

    test_dirs = [
        Path("docs/skilled-awareness"),
        Path("."),
    ]

    permission_errors = []
    for test_dir in test_dirs:
        if not test_dir.exists():
            permission_errors.append(str(test_dir))
            continue

        # Try to create a temporary file
        try:
            test_file = test_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
        except (PermissionError, OSError):
            permission_errors.append(str(test_dir))

    if permission_errors:
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "permission_errors": permission_errors,
            "message": "Insufficient write permissions",
            "recommendation": f"Check file permissions for: {', '.join(permission_errors)}"
        }

    checks_passed += 1
    return {
        "status": "OK",
        "message": "Write permissions valid"
    }


def validate_install_script():
    """Validate install-sap.py script exists and is valid Python."""
    global checks_passed, checks_failed, checks_warning, validation_failed

    script_path = Path("scripts/install-sap.py")

    if not script_path.exists():
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "message": "scripts/install-sap.py not found"
        }

    # Test if script can be parsed by Python
    try:
        import py_compile
        py_compile.compile(str(script_path), doraise=True)
    except py_compile.PyCompileError as e:
        checks_failed += 1
        validation_failed = True
        return {
            "status": "FAIL",
            "message": f"scripts/install-sap.py has syntax errors: {e}"
        }

    checks_passed += 1
    return {
        "status": "OK",
        "message": "install-sap.py script valid"
    }


def validate_optional_yaml():
    """Check if optional PyYAML is available."""
    global checks_passed, checks_warning

    try:
        import yaml  # noqa: F401
        checks_passed += 1
        return {
            "status": "OK",
            "message": "PyYAML available"
        }
    except ImportError:
        checks_warning += 1
        return {
            "status": "WARNING",
            "message": "PyYAML not installed (optional - needed for custom .chorabase files)",
            "recommendation": "Install with: pip install PyYAML (not required for standard SAP set installation)"
        }


def run_all_validations():
    """Run all validation checks."""
    return {
        "python": validate_python(),
        "git": validate_git(),
        "directory_structure": validate_directory_structure(),
        "sap_catalog": validate_sap_catalog(),
        "disk_space": validate_disk_space(),
        "write_permissions": validate_write_permissions(),
        "install_script": validate_install_script(),
        "optional_yaml": validate_optional_yaml(),
    }


def format_human_readable(results):
    """Format validation results as human-readable text."""
    output = []

    output.append("=" * 60)
    output.append("chora-base Pre-Flight Validation")
    output.append("=" * 60)
    output.append("")
    output.append("This script validates prerequisites before running install-sap.py")
    output.append("Target: Catch 90%+ of installation issues before they occur")
    output.append("")

    # Run each validation and format output
    for check_name, result in results.items():
        status_symbol = {
            "OK": "[PASS]",
            "WARNING": "[WARN]",
            "FAIL": "[FAIL]"
        }.get(result["status"], "[????]")

        check_title = check_name.replace("_", " ").title()
        output.append(f"{status_symbol} {check_title}")
        output.append(f"    {result['message']}")

        if "recommendation" in result:
            output.append(f"    → {result['recommendation']}")

        output.append("")

    # Summary
    output.append("=" * 60)
    output.append("Validation Summary")
    output.append("=" * 60)
    output.append("")
    output.append(f"Checks passed:  {checks_passed}")
    output.append(f"Checks failed:  {checks_failed}")
    output.append(f"Warnings:       {checks_warning}")
    output.append("")

    # Final status
    if validation_failed:
        output.append("[FAIL] Pre-flight validation FAILED")
        output.append("")
        output.append("Fix the issues above before running install-sap.py")
        output.append("For common issues, see: docs/user-docs/troubleshooting/onboarding-faq.md")
    elif checks_warning > 0:
        output.append("[WARN] Pre-flight validation PASSED with warnings")
        output.append("")
        output.append("You can proceed with installation, but review warnings above")
        output.append("To install a SAP set, run:")
        output.append("")
        output.append("    python3 scripts/install-sap.py --set minimal-entry")
    else:
        output.append("[PASS] Pre-flight validation PASSED")
        output.append("")
        output.append("All checks passed! You're ready to install SAPs.")
        output.append("To see available SAP sets, run:")
        output.append("")
        output.append("    python3 scripts/install-sap.py --list-sets")
        output.append("")
        output.append("To install a SAP set, run:")
        output.append("")
        output.append("    python3 scripts/install-sap.py --set minimal-entry")
        output.append("")
        output.append("For help choosing a SAP set, see:")
        output.append("    docs/user-docs/reference/sap-set-decision-tree.md")

    output.append("")
    return "\n".join(output)


def main():
    """Main entry point."""
    # Check for --json flag
    output_json = "--json" in sys.argv

    # Run all validations
    results = run_all_validations()

    # Output
    if output_json:
        output_data = {
            "summary": {
                "passed": checks_passed,
                "failed": checks_failed,
                "warnings": checks_warning,
                "validation_failed": validation_failed
            },
            "checks": results
        }
        print(json.dumps(output_data, indent=2))
    else:
        print(format_human_readable(results))

    # Exit with appropriate code
    if validation_failed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
