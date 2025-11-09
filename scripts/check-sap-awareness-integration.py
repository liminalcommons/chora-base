#!/usr/bin/env python3
"""SAP Awareness Integration Checker.

Purpose: Quick pattern detection for AGENTS.md/CLAUDE.md integration in SAP adoption blueprints
Scope: SIMPLE checks only - complex validation requires LLM-based audit

Usage:
    python scripts/check-sap-awareness-integration.py <sap-directory>
    python scripts/check-sap-awareness-integration.py docs/skilled-awareness/testing-framework
    python scripts/check-sap-awareness-integration.py --json <sap-directory>

Exit codes:
    0 - All basic patterns found (still requires full LLM audit for quality)
    1 - Missing critical patterns
    2 - Invalid usage
"""

import json
import re
import sys
from pathlib import Path


def check_pattern(content, pattern_name, pattern, case_insensitive=False):
    """Check if a pattern exists in content.

    Args:
        content: File content to search
        pattern_name: Human-readable pattern name
        pattern: Regex pattern or simple string to search for
        case_insensitive: Whether to ignore case

    Returns:
        dict with keys: pattern_name, found, status
    """
    flags = re.IGNORECASE if case_insensitive else 0

    if isinstance(pattern, str) and not any(c in pattern for c in r'.*+?[]{}()^$|\\'):
        # Simple string search
        found = (pattern.lower() in content.lower()) if case_insensitive else (pattern in content)
    else:
        # Regex search
        found = bool(re.search(pattern, content, flags))

    status = "PASS" if found else "FAIL"

    return {
        "pattern_name": pattern_name,
        "found": found,
        "status": status
    }


def run_sap_awareness_checks(sap_dir):
    """Run all SAP awareness integration checks.

    Args:
        sap_dir: Path to SAP directory

    Returns:
        dict with validation results
    """
    sap_path = Path(sap_dir)
    blueprint_path = sap_path / "adoption-blueprint.md"

    # Check if blueprint exists
    if not blueprint_path.exists():
        return {
            "sap_directory": str(sap_dir),
            "blueprint_path": str(blueprint_path),
            "blueprint_exists": False,
            "error": "adoption-blueprint.md not found",
            "checks": [],
            "summary": {
                "passed": 0,
                "warnings": 0,
                "failed": 1
            },
            "overall_status": "FAIL"
        }

    # Read blueprint content
    try:
        content = blueprint_path.read_text(encoding='utf-8')
    except (IOError, UnicodeDecodeError) as e:
        return {
            "sap_directory": str(sap_dir),
            "blueprint_path": str(blueprint_path),
            "blueprint_exists": True,
            "error": f"Could not read blueprint: {e}",
            "checks": [],
            "summary": {
                "passed": 0,
                "warnings": 0,
                "failed": 1
            },
            "overall_status": "FAIL"
        }

    # Run pattern checks
    checks = []

    # Check 1: Post-install section
    checks.append(check_pattern(
        content,
        "Post-install section exists",
        r"post-install|awareness enablement",
        case_insensitive=True
    ))

    # Check 2: AGENTS.md mentioned
    checks.append(check_pattern(
        content,
        "AGENTS.md mentioned",
        r"AGENTS\.md",
        case_insensitive=False
    ))

    # Check 3: Validation command (grep check)
    check3 = check_pattern(
        content,
        "Validation command present",
        r"grep.*AGENTS\.md",
        case_insensitive=False
    )
    # Downgrade to WARNING if not found (not critical)
    if not check3["found"]:
        check3["status"] = "WARNING"
    checks.append(check3)

    # Check 4: Agent-executable guidance
    check4 = check_pattern(
        content,
        "Agent-executable instructions",
        r"use edit tool|use Edit|For agents",
        case_insensitive=True
    )
    # Downgrade to WARNING if not found (not critical)
    if not check4["found"]:
        check4["status"] = "WARNING"
    checks.append(check4)

    # Calculate summary
    passed = sum(1 for c in checks if c["status"] == "PASS")
    warnings = sum(1 for c in checks if c["status"] == "WARNING")
    failed = sum(1 for c in checks if c["status"] == "FAIL")

    # Determine overall status
    if failed > 0:
        overall_status = "FAIL"
    elif warnings > 0:
        overall_status = "WARNING"
    else:
        overall_status = "PASS"

    return {
        "sap_directory": str(sap_dir),
        "blueprint_path": str(blueprint_path),
        "blueprint_exists": True,
        "checks": checks,
        "summary": {
            "passed": passed,
            "warnings": warnings,
            "failed": failed
        },
        "overall_status": overall_status
    }


def format_human_readable(results):
    """Format results as human-readable text.

    Args:
        results: Results from run_sap_awareness_checks()

    Returns:
        str: Formatted output
    """
    output = []

    output.append("=" * 60)
    output.append("SAP Awareness Integration Checker")
    output.append("=" * 60)
    output.append("")
    output.append(f"SAP Directory: {results['sap_directory']}")
    output.append(f"Blueprint: {results['blueprint_path']}")
    output.append("")

    if not results.get("blueprint_exists"):
        output.append("[FAIL] adoption-blueprint.md not found")
        output.append("")
        output.append(f"Expected: {results['blueprint_path']}")
        return "\n".join(output)

    if "error" in results:
        output.append(f"[FAIL] Error: {results['error']}")
        return "\n".join(output)

    output.append("[OK] adoption-blueprint.md exists")
    output.append("")

    output.append("Running pattern checks...")
    output.append("-" * 60)

    for check in results["checks"]:
        status_symbol = {
            "PASS": "[PASS]",
            "WARNING": "[WARN]",
            "FAIL": "[FAIL]"
        }.get(check["status"], "[????]")

        output.append(f"{status_symbol} {check['pattern_name']}")

        if not check["found"] and check["status"] != "PASS":
            # Add hint for failed/warning checks
            if "AGENTS.md" in check["pattern_name"]:
                output.append("    -> 'AGENTS.md' not mentioned in blueprint")
            elif "post-install" in check["pattern_name"].lower():
                output.append("    -> No 'post-install' or 'awareness enablement' section found")
            elif "validation" in check["pattern_name"].lower():
                output.append("    -> No validation command found (grep check)")
            elif "agent-executable" in check["pattern_name"].lower():
                output.append("    -> No explicit agent-executable instructions found")

    output.append("")
    output.append("=" * 60)
    output.append("Summary")
    output.append("=" * 60)
    output.append("")
    output.append(f"[OK]   Passed:   {results['summary']['passed']}")
    output.append(f"[WARN] Warnings: {results['summary']['warnings']}")
    output.append(f"[FAIL] Failed:   {results['summary']['failed']}")
    output.append("")

    # Final assessment
    if results["overall_status"] == "PASS":
        output.append("[PASS] RESULT: All basic patterns found")
        output.append("")
        output.append("[INFO] IMPORTANT: This script only checks for basic patterns.")
        output.append("       Full quality audit requires LLM-based review using:")
        output.append("       docs/dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md")
    elif results["overall_status"] == "WARNING":
        output.append("[WARN] RESULT: Basic patterns found with warnings")
        output.append("")
        output.append("Recommended action:")
        output.append("  - Review warnings above")
        output.append("  - Run full LLM audit: SAP_AWARENESS_INTEGRATION_CHECKLIST.md")
    else:
        output.append("[FAIL] RESULT: Missing critical awareness integration patterns")
        output.append("")
        output.append("Required actions:")
        output.append("  1. Review failed checks above")
        output.append("  2. Add missing post-install awareness enablement section")
        output.append("  3. Include AGENTS.md update instructions")
        output.append("  4. Run full LLM audit: SAP_AWARENESS_INTEGRATION_CHECKLIST.md")
        output.append("")
        output.append("Reference examples:")
        output.append("  - SAP-000: docs/skilled-awareness/sap-framework/adoption-blueprint.md")
        output.append("  - SAP-001: docs/skilled-awareness/inbox/adoption-blueprint.md")

    output.append("")
    return "\n".join(output)


def main():
    """Main entry point."""
    # Parse arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    output_json = '--json' in sys.argv

    if len(args) != 1:
        print("Usage: python scripts/check-sap-awareness-integration.py <sap-directory>")
        print("")
        print("Example:")
        print("  python scripts/check-sap-awareness-integration.py docs/skilled-awareness/testing-framework")
        print("")
        sys.exit(2)

    sap_dir = args[0]

    # Run checks
    results = run_sap_awareness_checks(sap_dir)

    # Output
    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(format_human_readable(results))

    # Exit with appropriate code
    if results["overall_status"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
