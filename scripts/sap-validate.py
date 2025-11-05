#!/usr/bin/env python3
"""
SAP Structure Validator

Validates that a SAP directory contains all required artifacts with proper frontmatter.

Usage:
    python scripts/sap-validate.py <sap-directory>
    python scripts/sap-validate.py docs/skilled-awareness/testing-framework
    python scripts/sap-validate.py --all  # Validate all SAPs

Requirements (Level 3):
- 5 core artifacts (charter, protocol, awareness, blueprint, ledger)
- Valid frontmatter in each artifact
- Proper SAP ID format (SAP-###)
- Version follows semver

Exit Codes:
    0 - All validations passed
    1 - Validation failures found
    2 - Usage error or missing directory
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Required SAP artifacts
REQUIRED_ARTIFACTS = [
    "capability-charter.md",
    "protocol-spec.md",
    "awareness-guide.md",
    "adoption-blueprint.md",
    "ledger.md"
]

# Frontmatter patterns
FRONTMATTER_PATTERN = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)
SAPID_PATTERN = re.compile(r'^SAP-\d{3}$')
VERSION_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')


def validate_frontmatter(content: str, file_path: Path) -> List[str]:
    """Validate frontmatter exists and has required fields."""
    errors = []

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        errors.append(f"{file_path.name}: Missing frontmatter (---...---)")
        return errors

    frontmatter = match.group(1)

    # Check for required fields
    required_fields = ['sap_id', 'version', 'status']
    for field in required_fields:
        if f"{field}:" not in frontmatter:
            errors.append(f"{file_path.name}: Missing frontmatter field '{field}'")

    # Validate SAP ID format
    sap_id_match = re.search(r'sap_id:\s*(\S+)', frontmatter)
    if sap_id_match:
        sap_id = sap_id_match.group(1)
        if not SAPID_PATTERN.match(sap_id):
            errors.append(f"{file_path.name}: Invalid SAP ID format '{sap_id}' (expected: SAP-###)")

    # Validate version format
    version_match = re.search(r'version:\s*(\S+)', frontmatter)
    if version_match:
        version = version_match.group(1)
        if not VERSION_PATTERN.match(version):
            errors.append(f"{file_path.name}: Invalid version format '{version}' (expected: semver X.Y.Z)")

    return errors


def validate_sap_directory(sap_dir: Path) -> Tuple[bool, List[str]]:
    """
    Validate a SAP directory structure.

    Returns:
        (success, errors) tuple
    """
    if not sap_dir.exists():
        return False, [f"Directory does not exist: {sap_dir}"]

    if not sap_dir.is_dir():
        return False, [f"Not a directory: {sap_dir}"]

    errors = []

    # Check for required artifacts
    for artifact in REQUIRED_ARTIFACTS:
        artifact_path = sap_dir / artifact
        if not artifact_path.exists():
            errors.append(f"Missing required artifact: {artifact}")
            continue

        # Read and validate frontmatter
        try:
            content = artifact_path.read_text(encoding='utf-8')
            frontmatter_errors = validate_frontmatter(content, artifact_path)
            errors.extend(frontmatter_errors)
        except Exception as e:
            errors.append(f"{artifact}: Failed to read file - {e}")

    return len(errors) == 0, errors


def find_all_saps(base_dir: Path = None) -> List[Path]:
    """Find all SAP directories in docs/skilled-awareness/."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent / "docs" / "skilled-awareness"

    if not base_dir.exists():
        return []

    saps = []
    for item in base_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it looks like a SAP directory (has at least one required artifact)
            if any((item / artifact).exists() for artifact in REQUIRED_ARTIFACTS):
                saps.append(item)

    return sorted(saps)


def print_result(sap_dir: Path, success: bool, errors: List[str]):
    """Print validation results."""
    sap_name = sap_dir.name

    if success:
        print(f"[OK] {sap_name}")
    else:
        print(f"[FAIL] {sap_name}")
        for error in errors:
            print(f"  - {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate SAP directory structure and frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "sap_directory",
        nargs='?',
        type=Path,
        help="Path to SAP directory to validate"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all SAPs in docs/skilled-awareness/"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if any validation fails"
    )

    args = parser.parse_args()

    # Determine which SAPs to validate
    if args.all:
        saps = find_all_saps()
        if not saps:
            print("[WARN] No SAP directories found in docs/skilled-awareness/", file=sys.stderr)
            return 0
    elif args.sap_directory:
        saps = [args.sap_directory]
    else:
        parser.print_help()
        return 2

    # Validate each SAP
    all_success = True
    for sap_dir in saps:
        success, errors = validate_sap_directory(sap_dir)
        print_result(sap_dir, success, errors)

        if not success:
            all_success = False

    # Summary
    total = len(saps)
    passed = sum(1 for sap in saps if validate_sap_directory(sap)[0])
    failed = total - passed

    print(f"\nSummary: {passed}/{total} SAPs passed")

    if failed > 0:
        print(f"[WARN] {failed} SAP(s) failed validation")
        return 1 if args.strict else 0
    else:
        print("[OK] All SAPs valid")
        return 0


if __name__ == "__main__":
    sys.exit(main())
