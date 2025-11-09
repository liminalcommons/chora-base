#!/usr/bin/env python3
"""Python environment validation utility for cross-platform development.

Validates Python setup across Mac, Windows, and Linux:
- Python version (3.11+)
- Virtual environment activation
- pip availability
- pyproject.toml setup

Usage:
    python scripts/check-python-env.py
    python scripts/check-python-env.py --json  # Output as JSON
"""

import json
import sys
import os
from pathlib import Path
import subprocess


# Minimum required Python version
MIN_PYTHON_VERSION = (3, 11)


def check_python_version():
    """Check if Python version meets minimum requirements."""
    current_version = sys.version_info[:2]
    meets_requirement = current_version >= MIN_PYTHON_VERSION
    return {
        "current": f"{current_version[0]}.{current_version[1]}",
        "minimum": f"{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}",
        "meets_requirement": meets_requirement,
        "status": "OK" if meets_requirement else "FAIL",
    }


def check_virtual_environment():
    """Check if running in a virtual environment."""
    in_venv = sys.prefix != sys.base_prefix
    return {
        "in_venv": in_venv,
        "venv_path": sys.prefix if in_venv else None,
        "status": "OK" if in_venv else "WARNING",
        "message": "Running in virtual environment" if in_venv else "Not in virtual environment (recommended to use venv)",
    }


def check_pip():
    """Check if pip is available and working."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        pip_available = result.returncode == 0
        pip_version = result.stdout.strip() if pip_available else None
        return {
            "available": pip_available,
            "version": pip_version,
            "status": "OK" if pip_available else "FAIL",
        }
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {
            "available": False,
            "version": None,
            "status": "FAIL",
            "error": str(e),
        }


def check_pyproject_toml():
    """Check if pyproject.toml exists in current directory."""
    pyproject_path = Path.cwd() / "pyproject.toml"
    exists = pyproject_path.exists()
    return {
        "exists": exists,
        "path": str(pyproject_path) if exists else None,
        "status": "OK" if exists else "WARNING",
        "message": "pyproject.toml found" if exists else "pyproject.toml not found in current directory",
    }


def check_platform_specific_issues():
    """Check for platform-specific Python environment issues."""
    issues = []
    warnings = []

    # Windows-specific checks
    if sys.platform == "win32":
        # Check if PYTHONIOENCODING is set (helps with UTF-8 issues)
        if "PYTHONIOENCODING" not in os.environ:
            warnings.append("PYTHONIOENCODING not set (may cause UTF-8 encoding issues on Windows)")

        # Check if symlinks are available (usually disabled on Windows)
        try:
            test_link = Path.cwd() / ".test_symlink"
            test_target = Path.cwd() / ".test_target"
            test_target.touch()
            test_link.symlink_to(test_target)
            test_link.unlink()
            test_target.unlink()
        except (OSError, NotImplementedError):
            warnings.append("Symlinks not available (common on Windows - may affect some packages)")

    # macOS-specific checks
    if sys.platform == "darwin":
        # Check if Python is Framework build (can cause issues with some packages)
        is_framework = "Python.framework" in sys.executable
        if is_framework:
            warnings.append("Using macOS Framework build (may have compatibility issues with some native extensions)")

    # Linux-specific checks
    if sys.platform.startswith("linux"):
        # Check if using system Python (not recommended)
        if sys.prefix == sys.base_prefix and "/usr" in sys.prefix:
            warnings.append("Using system Python (recommended to use pyenv or virtual environment)")

    return {
        "issues": issues,
        "warnings": warnings,
        "status": "FAIL" if issues else ("WARNING" if warnings else "OK"),
    }


def run_all_checks():
    """Run all Python environment checks."""
    checks = {
        "python_version": check_python_version(),
        "virtual_environment": check_virtual_environment(),
        "pip": check_pip(),
        "pyproject_toml": check_pyproject_toml(),
        "platform_specific": check_platform_specific_issues(),
    }

    # Determine overall status
    statuses = [check["status"] for check in checks.values()]
    if "FAIL" in statuses:
        overall_status = "FAIL"
    elif "WARNING" in statuses:
        overall_status = "WARNING"
    else:
        overall_status = "OK"

    return {
        "overall_status": overall_status,
        "checks": checks,
    }


def format_human_readable(results):
    """Format results as human-readable text."""
    output = []
    output.append("=" * 60)
    output.append("Python Environment Validation")
    output.append("=" * 60)
    output.append("")

    # Overall status
    status_symbol = {
        "OK": "[PASS]",
        "WARNING": "[WARN]",
        "FAIL": "[FAIL]"
    }
    output.append(f"Overall Status: {status_symbol[results['overall_status']]} {results['overall_status']}")
    output.append("")

    checks = results["checks"]

    # Python version
    pv = checks["python_version"]
    output.append(f"{status_symbol[pv['status']]} Python Version")
    output.append(f"    Current:  {pv['current']}")
    output.append(f"    Minimum:  {pv['minimum']}")
    output.append(f"    Status:   {pv['status']}")
    output.append("")

    # Virtual environment
    ve = checks["virtual_environment"]
    output.append(f"{status_symbol[ve['status']]} Virtual Environment")
    output.append(f"    Active:   {'Yes' if ve['in_venv'] else 'No'}")
    if ve['in_venv']:
        output.append(f"    Path:     {ve['venv_path']}")
    output.append(f"    Message:  {ve['message']}")
    output.append("")

    # pip
    pip = checks["pip"]
    output.append(f"{status_symbol[pip['status']]} pip")
    output.append(f"    Available: {'Yes' if pip['available'] else 'No'}")
    if pip['available']:
        output.append(f"    Version:   {pip['version']}")
    output.append("")

    # pyproject.toml
    pt = checks["pyproject_toml"]
    output.append(f"{status_symbol[pt['status']]} pyproject.toml")
    output.append(f"    Exists:   {'Yes' if pt['exists'] else 'No'}")
    if pt['exists']:
        output.append(f"    Path:     {pt['path']}")
    output.append(f"    Message:  {pt['message']}")
    output.append("")

    # Platform-specific
    ps = checks["platform_specific"]
    output.append(f"{status_symbol[ps['status']]} Platform-Specific Checks")
    if ps['issues']:
        output.append("    Issues:")
        for issue in ps['issues']:
            output.append(f"      - {issue}")
    if ps['warnings']:
        output.append("    Warnings:")
        for warning in ps['warnings']:
            output.append(f"      - {warning}")
    if not ps['issues'] and not ps['warnings']:
        output.append("    No issues detected")
    output.append("")

    output.append("=" * 60)

    # Add recommendations if there are failures
    if results['overall_status'] in ["FAIL", "WARNING"]:
        output.append("")
        output.append("Recommendations:")
        if not checks["python_version"]["meets_requirement"]:
            output.append("  - Upgrade Python to version 3.11 or higher")
        if not checks["virtual_environment"]["in_venv"]:
            output.append("  - Create and activate a virtual environment:")
            output.append("      python -m venv .venv")
            if sys.platform == "win32":
                output.append("      .venv\\Scripts\\activate  # Windows")
            else:
                output.append("      source .venv/bin/activate  # Mac/Linux")
        if not checks["pip"]["available"]:
            output.append("  - Install pip (usually included with Python 3.11+)")
        if not checks["pyproject_toml"]["exists"]:
            output.append("  - Create pyproject.toml or navigate to project root")
        output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    # Check if --json flag is provided
    output_json = "--json" in sys.argv

    # Run all checks
    results = run_all_checks()

    # Output in requested format
    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(format_human_readable(results))

    # Exit with appropriate code
    if results["overall_status"] == "FAIL":
        sys.exit(1)
    elif results["overall_status"] == "WARNING":
        sys.exit(0)  # Warnings don't fail the check
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
