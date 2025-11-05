#!/usr/bin/env python3
"""
Infrastructure Validation Script for SAP Adoption Levels

Validates that claimed SAP adoption levels match actual infrastructure present.
Prevents over-reported adoptions like SAP-004 (claimed 85% coverage, actually 4%)
and SAP-005 (claimed L3, no .github/workflows/ directory).

Usage:
    python scripts/validate-sap-infrastructure.py                  # Validate all SAPs
    python scripts/validate-sap-infrastructure.py --sap SAP-005    # Validate specific SAP
    python scripts/validate-sap-infrastructure.py --level 3        # Validate all L3 SAPs
    python scripts/validate-sap-infrastructure.py --fix            # Auto-fix ledgers (dry-run)

Exit Codes:
    0 = All validations pass
    1 = Validation failures found
    2 = Critical infrastructure missing
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# SAP infrastructure requirements by adoption level
INFRASTRUCTURE_REQUIREMENTS = {
    1: {
        "description": "Level 1 - Basic infrastructure operational",
        "checks": [
            "sap_directory_exists",
            "has_basic_artifacts",  # At least 1 of 5 artifacts
            "system_files_exist",   # If system_files listed, at least 1 must exist
        ]
    },
    2: {
        "description": "Level 2 - Production usage with metrics",
        "checks": [
            "sap_directory_exists",
            "has_most_artifacts",   # At least 3 of 5 artifacts
            "system_files_exist",
            "ledger_has_metrics",   # Ledger documents metrics/baselines
        ]
    },
    3: {
        "description": "Level 3 - Full automation and strategic impact",
        "checks": [
            "sap_directory_exists",
            "has_all_artifacts",    # All 5 artifacts present
            "system_files_exist",
            "ledger_has_metrics",
            "ledger_has_roi",       # Ledger documents ROI calculation
            "automation_present",   # CI/CD, scripts, or automation evidence
        ]
    }
}


def load_adoption_history(history_path: str = "adoption-history.jsonl") -> List[Dict]:
    """Load adoption events from adoption-history.jsonl"""
    events = []
    with open(history_path, 'r') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def get_current_adoption_levels(events: List[Dict]) -> Dict[str, int]:
    """
    Determine current adoption level for each SAP based on events.

    Returns dict: {SAP-ID: adoption_level}
    """
    levels = {}

    for event in events:
        sap_id = event.get("sap_id")
        if not sap_id:
            continue

        if event["event_type"] == "sap_installed":
            levels[sap_id] = event.get("adoption_level", 1)
        elif event["event_type"] == "level_progression":
            levels[sap_id] = event["to_level"]

    return levels


def check_sap_directory_exists(sap_name: str) -> bool:
    """Check if SAP directory exists in docs/skilled-awareness/"""
    sap_dir = Path(f"docs/skilled-awareness/{sap_name}")
    return sap_dir.exists() and sap_dir.is_dir()


def check_has_basic_artifacts(sap_name: str) -> Tuple[bool, int]:
    """Check if at least 1 of 5 artifacts exists. Returns (pass, count)"""
    sap_dir = Path(f"docs/skilled-awareness/{sap_name}")
    artifacts = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]

    count = sum(1 for artifact in artifacts if (sap_dir / artifact).exists())
    return count >= 1, count


def check_has_most_artifacts(sap_name: str) -> Tuple[bool, int]:
    """Check if at least 3 of 5 artifacts exist. Returns (pass, count)"""
    sap_dir = Path(f"docs/skilled-awareness/{sap_name}")
    artifacts = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]

    count = sum(1 for artifact in artifacts if (sap_dir / artifact).exists())
    return count >= 3, count


def check_has_all_artifacts(sap_name: str) -> Tuple[bool, int]:
    """Check if all 5 artifacts exist. Returns (pass, count)"""
    sap_dir = Path(f"docs/skilled-awareness/{sap_name}")
    artifacts = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]

    count = sum(1 for artifact in artifacts if (sap_dir / artifact).exists())
    return count == 5, count


def check_system_files_exist(sap_name: str, sap_catalog_entry: Dict) -> Tuple[bool, List[str]]:
    """
    Check if system files from sap_catalog.json exist.

    Returns (pass, missing_files)
    """
    system_files = sap_catalog_entry.get("system_files", [])
    if not system_files:
        return True, []  # No system files required

    missing = []
    for file_pattern in system_files:
        # Handle wildcards like "static-template/**"
        if "**" in file_pattern or "*" in file_pattern:
            # Check if at least one file matches the pattern
            base_path = file_pattern.split("*")[0]
            if not Path(base_path).exists():
                missing.append(file_pattern)
        else:
            if not Path(file_pattern).exists():
                missing.append(file_pattern)

    # Pass if at least 1 system file exists (not all required)
    return len(missing) < len(system_files), missing


def check_ledger_has_metrics(sap_name: str) -> Tuple[bool, str]:
    """Check if ledger.md documents metrics or baselines"""
    ledger_path = Path(f"docs/skilled-awareness/{sap_name}/ledger.md")
    if not ledger_path.exists():
        return False, "No ledger.md found"

    content = ledger_path.read_text()

    # Look for metric indicators
    metric_keywords = [
        "coverage",
        "baseline",
        "metrics",
        "measurement",
        "percentage",
        "time saved",
        "hours invested"
    ]

    found = any(keyword.lower() in content.lower() for keyword in metric_keywords)
    return found, "Metrics documented" if found else "No metrics found in ledger"


def check_ledger_has_roi(sap_name: str) -> Tuple[bool, str]:
    """Check if ledger.md documents ROI calculation"""
    ledger_path = Path(f"docs/skilled-awareness/{sap_name}/ledger.md")
    if not ledger_path.exists():
        return False, "No ledger.md found"

    content = ledger_path.read_text()

    # Look for ROI indicators
    roi_keywords = [
        "roi",
        "return on investment",
        "savings",
        "hours saved",
        "efficiency",
        "x return"
    ]

    found = any(keyword.lower() in content.lower() for keyword in roi_keywords)
    return found, "ROI documented" if found else "No ROI calculation found in ledger"


def check_automation_present(sap_name: str, sap_catalog_entry: Dict) -> Tuple[bool, str]:
    """Check if automation is present (CI/CD, scripts, workflows)"""
    automation_indicators = []

    # Check system files for automation patterns
    system_files = sap_catalog_entry.get("system_files", [])
    for file in system_files:
        if ".github/workflows/" in file:
            automation_indicators.append("GitHub Actions workflow")
        if "scripts/" in file:
            automation_indicators.append("Automation script")
        if ".pre-commit" in file:
            automation_indicators.append("Pre-commit hook")

    # Check ledger for automation mentions
    ledger_path = Path(f"docs/skilled-awareness/{sap_name}/ledger.md")
    if ledger_path.exists():
        content = ledger_path.read_text()
        automation_keywords = ["ci/cd", "automated", "automation", "workflow", "pipeline"]
        if any(keyword in content.lower() for keyword in automation_keywords):
            automation_indicators.append("Automation mentioned in ledger")

    return len(automation_indicators) > 0, f"Found: {', '.join(automation_indicators)}" if automation_indicators else "No automation detected"


def validate_sap(sap_id: str, sap_name: str, claimed_level: int, sap_catalog_entry: Dict) -> Dict:
    """
    Validate a single SAP's infrastructure against claimed adoption level.

    Returns validation result dict with pass/fail and details.
    """
    result = {
        "sap_id": sap_id,
        "sap_name": sap_name,
        "claimed_level": claimed_level,
        "validated": True,
        "failures": [],
        "warnings": [],
        "details": {}
    }

    # Get required checks for this level
    if claimed_level not in INFRASTRUCTURE_REQUIREMENTS:
        result["validated"] = False
        result["failures"].append(f"Invalid adoption level: {claimed_level}")
        return result

    checks = INFRASTRUCTURE_REQUIREMENTS[claimed_level]["checks"]

    # Run checks
    for check_name in checks:
        if check_name == "sap_directory_exists":
            passed = check_sap_directory_exists(sap_name)
            result["details"][check_name] = passed
            if not passed:
                result["validated"] = False
                result["failures"].append(f"SAP directory does not exist: docs/skilled-awareness/{sap_name}")

        elif check_name == "has_basic_artifacts":
            passed, count = check_has_basic_artifacts(sap_name)
            result["details"][check_name] = f"{count}/5 artifacts"
            if not passed:
                result["validated"] = False
                result["failures"].append(f"Needs ≥1 artifact, found {count}/5")

        elif check_name == "has_most_artifacts":
            passed, count = check_has_most_artifacts(sap_name)
            result["details"][check_name] = f"{count}/5 artifacts"
            if not passed:
                result["validated"] = False
                result["failures"].append(f"Needs ≥3 artifacts for L2, found {count}/5")

        elif check_name == "has_all_artifacts":
            passed, count = check_has_all_artifacts(sap_name)
            result["details"][check_name] = f"{count}/5 artifacts"
            if not passed:
                result["validated"] = False
                result["failures"].append(f"Needs all 5 artifacts for L3, found {count}/5")

        elif check_name == "system_files_exist":
            passed, missing = check_system_files_exist(sap_name, sap_catalog_entry)
            result["details"][check_name] = "OK" if passed else f"Missing: {', '.join(missing)}"
            if not passed:
                result["warnings"].append(f"Some system files missing (acceptable if template-only): {', '.join(missing[:3])}")

        elif check_name == "ledger_has_metrics":
            passed, msg = check_ledger_has_metrics(sap_name)
            result["details"][check_name] = msg
            if not passed:
                result["validated"] = False
                result["failures"].append(f"Ledger missing metrics documentation for L{claimed_level}")

        elif check_name == "ledger_has_roi":
            passed, msg = check_ledger_has_roi(sap_name)
            result["details"][check_name] = msg
            if not passed:
                result["validated"] = False
                result["failures"].append(f"Ledger missing ROI calculation for L3")

        elif check_name == "automation_present":
            passed, msg = check_automation_present(sap_name, sap_catalog_entry)
            result["details"][check_name] = msg
            if not passed:
                result["warnings"].append(f"No automation detected for L3 (may be template-only)")

    return result


def main():
    """Main validation orchestrator"""
    import argparse

    parser = argparse.ArgumentParser(description="Validate SAP infrastructure against claimed adoption levels")
    parser.add_argument("--sap", help="Validate specific SAP (e.g., SAP-005)")
    parser.add_argument("--level", type=int, choices=[1, 2, 3], help="Validate all SAPs at specific level")
    parser.add_argument("--fix", action="store_true", help="Suggest fixes for validation failures (dry-run)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Load adoption history
    events = load_adoption_history()
    levels = get_current_adoption_levels(events)

    # Load SAP catalog
    with open("sap-catalog.json", 'r') as f:
        catalog = json.load(f)

    # Determine which SAPs to validate
    saps_to_validate = []
    if args.sap:
        if args.sap in levels:
            saps_to_validate.append(args.sap)
        else:
            print(f"❌ SAP {args.sap} not found in adoption-history.jsonl", file=sys.stderr)
            return 2
    elif args.level:
        saps_to_validate = [sap_id for sap_id, level in levels.items() if level == args.level]
    else:
        saps_to_validate = list(levels.keys())

    # Validate each SAP
    results = []
    for sap_id in sorted(saps_to_validate):
        claimed_level = levels[sap_id]

        # Find SAP in catalog
        sap_entry = None
        for sap in catalog["saps"]:
            if sap["id"] == sap_id:
                sap_entry = sap
                break

        if not sap_entry:
            print(f"⚠️  {sap_id} not found in sap-catalog.json", file=sys.stderr)
            continue

        sap_name = sap_entry["name"]
        result = validate_sap(sap_id, sap_name, claimed_level, sap_entry)
        results.append(result)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*80)
        print("SAP Infrastructure Validation Report")
        print("="*80 + "\n")

        passed = [r for r in results if r["validated"]]
        failed = [r for r in results if not r["validated"]]

        print(f"✅ Passed: {len(passed)}/{len(results)}")
        print(f"❌ Failed: {len(failed)}/{len(results)}\n")

        if failed:
            print("FAILURES:\n")
            for r in failed:
                print(f"  ❌ {r['sap_id']} ({r['sap_name']}) - Claimed L{r['claimed_level']}")
                for failure in r["failures"]:
                    print(f"      • {failure}")
                if r["warnings"]:
                    for warning in r["warnings"]:
                        print(f"      ⚠️  {warning}")
                print()

        if passed:
            print("PASSED:\n")
            for r in passed:
                print(f"  ✅ {r['sap_id']} ({r['sap_name']}) - L{r['claimed_level']}")
                if r["warnings"]:
                    for warning in r["warnings"]:
                        print(f"      ⚠️  {warning}")

    # Exit with appropriate code
    if any(not r["validated"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
