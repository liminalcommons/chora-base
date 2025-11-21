#!/usr/bin/env python3
"""
SAP Ecosystem Integration Validator

Validates that a SAP is fully integrated into the chora-base ecosystem across
all 5 integration points: INDEX.md, sap-catalog.json, copier.yml, adoption paths, and dependencies.

Part of: SAP-061 (SAP Ecosystem Integration)
Origin: CORD-2025-023 (SAP Development Lifecycle Meta-SAP Suite)

Usage:
    # Validate single SAP
    python scripts/validate-ecosystem-integration.py SAP-053

    # Validate all SAPs
    python scripts/validate-ecosystem-integration.py --all

    # JSON output (for automation)
    python scripts/validate-ecosystem-integration.py SAP-053 --json

    # Verbose output
    python scripts/validate-ecosystem-integration.py SAP-053 --verbose

Exit Codes:
    0 - All integration points validated successfully
    1 - SAP missing from INDEX.md
    2 - SAP missing from sap-catalog.json
    3 - SAP missing from copier.yml (if distributable)
    4 - Broken dependencies (references non-existent SAPs)
    5 - Multiple integration failures (see JSON output for details)
    6 - Usage error or invalid SAP ID

Integration Points Checked:
    1. INDEX.md: SAP entry exists in appropriate domain section
    2. sap-catalog.json: SAP metadata exists in machine-readable catalog
    3. copier.yml: SAP available for Copier-based distribution (if status=active or pilot)
    4. Progressive Adoption Path: SAP mentioned in relevant adoption path (if status=active)
    5. Dependencies: All referenced SAPs exist and are valid

Created: 2025-11-20
Author: Claude Code (CORD-2025-023 Phase 1)
Trace: sap-development-lifecycle-meta-saps-2025-11-20
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).parent.parent
INDEX_PATH = REPO_ROOT / "docs" / "skilled-awareness" / "INDEX.md"
CATALOG_PATH = REPO_ROOT / "sap-catalog.json"
COPIER_PATH = REPO_ROOT / "copier.yml"
SAP_DIR = REPO_ROOT / "docs" / "skilled-awareness"

# Patterns
SAP_ID_PATTERN = re.compile(r'^SAP-\d{3}$')
SAP_ENTRY_PATTERN = re.compile(r'###\s+(SAP-\d{3}):\s+(.+?)$', re.MULTILINE)


class IntegrationCheck:
    """Result of a single integration point validation."""

    def __init__(self, name: str, passed: bool, message: str, details: Optional[str] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details

    def to_dict(self) -> Dict:
        return {
            "integration_point": self.name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details
        }


class ValidationResult:
    """Complete validation result for a SAP."""

    def __init__(self, sap_id: str):
        self.sap_id = sap_id
        self.checks: List[IntegrationCheck] = []

    def add_check(self, check: IntegrationCheck):
        self.checks.append(check)

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    @property
    def failed_checks(self) -> List[IntegrationCheck]:
        return [check for check in self.checks if not check.passed]

    @property
    def exit_code(self) -> int:
        """Determine exit code based on failed checks."""
        if self.passed:
            return 0

        failed_names = [check.name for check in self.failed_checks]

        # Priority exit codes (most critical first)
        if "INDEX.md" in failed_names:
            return 1
        if "sap-catalog.json" in failed_names:
            return 2
        if "copier.yml" in failed_names:
            return 3
        if "Dependencies" in failed_names:
            return 4

        # Multiple failures
        return 5

    def to_dict(self) -> Dict:
        return {
            "sap_id": self.sap_id,
            "passed": self.passed,
            "checks": [check.to_dict() for check in self.checks],
            "exit_code": self.exit_code
        }


def validate_sap_id(sap_id: str) -> bool:
    """Validate SAP ID format."""
    return SAP_ID_PATTERN.match(sap_id) is not None


def get_sap_directory(sap_id: str) -> Optional[Path]:
    """Find SAP directory by searching for capability-charter.md."""
    for sap_dir in SAP_DIR.iterdir():
        if not sap_dir.is_dir():
            continue
        charter = sap_dir / "capability-charter.md"
        if charter.exists():
            content = charter.read_text()
            # Support both "SAP ID" and "Capability ID" formats
            if (f"**SAP ID**: {sap_id}" in content or
                f"SAP ID: {sap_id}" in content or
                f"**Capability ID**: {sap_id}" in content or
                f"Capability ID: {sap_id}" in content):
                return sap_dir
    return None


def extract_sap_metadata(sap_dir: Path) -> Dict:
    """Extract SAP metadata from capability-charter.md."""
    charter = sap_dir / "capability-charter.md"
    if not charter.exists():
        return {}

    content = charter.read_text()
    metadata = {}

    # Extract frontmatter if present
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')

    # Extract from document if not in frontmatter
    if 'status' not in metadata:
        status_match = re.search(r'\*\*Status\*\*:\s*(\w+)', content)
        if status_match:
            metadata['status'] = status_match.group(1).lower()

    if 'version' not in metadata:
        version_match = re.search(r'\*\*Version\*\*:\s*(\d+\.\d+\.\d+)', content)
        if version_match:
            metadata['version'] = version_match.group(1)

    # Extract dependencies
    deps_match = re.search(r'\*\*Dependencies\*\*:\s*(.+?)(?:\n|$)', content)
    if deps_match:
        deps_text = deps_match.group(1)
        # Extract SAP-XXX patterns
        metadata['dependencies'] = re.findall(r'SAP-\d{3}', deps_text)
    else:
        metadata['dependencies'] = []

    return metadata


def check_index_md(sap_id: str) -> IntegrationCheck:
    """Check if SAP is listed in INDEX.md."""
    if not INDEX_PATH.exists():
        return IntegrationCheck(
            "INDEX.md",
            False,
            f"INDEX.md not found at {INDEX_PATH}",
            None
        )

    content = INDEX_PATH.read_text()

    # Check for SAP entry (#### or ### followed by SAP-XXX)
    pattern = re.compile(rf'####+\s+{re.escape(sap_id)}:\s+', re.MULTILINE)
    if pattern.search(content):
        return IntegrationCheck(
            "INDEX.md",
            True,
            f"{sap_id} found in INDEX.md",
            None
        )
    else:
        return IntegrationCheck(
            "INDEX.md",
            False,
            f"{sap_id} NOT found in INDEX.md",
            f"Expected entry like '#### {sap_id}: <Title>' in docs/skilled-awareness/INDEX.md"
        )


def check_catalog_json(sap_id: str) -> IntegrationCheck:
    """Check if SAP is in sap-catalog.json."""
    if not CATALOG_PATH.exists():
        return IntegrationCheck(
            "sap-catalog.json",
            False,
            f"sap-catalog.json not found at {CATALOG_PATH}",
            "Catalog file missing - ecosystem integration incomplete"
        )

    try:
        catalog = json.loads(CATALOG_PATH.read_text())
    except json.JSONDecodeError as e:
        return IntegrationCheck(
            "sap-catalog.json",
            False,
            f"Invalid JSON in sap-catalog.json: {e}",
            None
        )

    # Search for SAP in catalog (handle various catalog structures)
    sap_found = False
    if isinstance(catalog, dict):
        # Check if SAP exists as key or in "saps" array
        if sap_id in catalog:
            sap_found = True
        elif "saps" in catalog:
            saps = catalog["saps"]
            if isinstance(saps, list):
                sap_found = any(sap.get("id") == sap_id for sap in saps if isinstance(sap, dict))
            elif isinstance(saps, dict):
                sap_found = sap_id in saps

    if sap_found:
        return IntegrationCheck(
            "sap-catalog.json",
            True,
            f"{sap_id} found in sap-catalog.json",
            None
        )
    else:
        return IntegrationCheck(
            "sap-catalog.json",
            False,
            f"{sap_id} NOT found in sap-catalog.json",
            "Add SAP entry to sap-catalog.json for machine-readable discovery"
        )


def check_copier_yml(sap_id: str, metadata: Dict) -> IntegrationCheck:
    """Check if SAP is available in copier.yml for distribution."""
    status = metadata.get('status', '').lower()

    # Only active and pilot SAPs need Copier integration
    if status not in ['active', 'pilot']:
        return IntegrationCheck(
            "copier.yml",
            True,
            f"{sap_id} status={status}, Copier distribution not required (only for active/pilot)",
            None
        )

    if not COPIER_PATH.exists():
        return IntegrationCheck(
            "copier.yml",
            False,
            f"copier.yml not found at {COPIER_PATH}",
            "Copier configuration missing - distribution not possible"
        )

    content = COPIER_PATH.read_text()

    # Convert SAP-053 → sap_053, SAP-053 → include_sap_053
    sap_var = sap_id.lower().replace('-', '_')  # sap_053
    include_var = f"include_{sap_var}"  # include_sap_053

    # Check for either the include variable or SAP mentioned in comments/help
    if include_var in content or sap_id in content:
        return IntegrationCheck(
            "copier.yml",
            True,
            f"{sap_id} found in copier.yml ({include_var} or referenced)",
            None
        )
    else:
        return IntegrationCheck(
            "copier.yml",
            False,
            f"{sap_id} NOT found in copier.yml",
            f"Add {include_var} variable to copier.yml for distribution (status={status} requires distribution)"
        )


def check_progressive_adoption_path(sap_id: str, metadata: Dict) -> IntegrationCheck:
    """Check if SAP is mentioned in Progressive Adoption Path (soft requirement)."""
    status = metadata.get('status', '').lower()

    # Only active SAPs need adoption path mentions (pilot and draft are optional)
    if status != 'active':
        return IntegrationCheck(
            "Progressive Adoption Path",
            True,
            f"{sap_id} status={status}, adoption path mention not required (only for active)",
            None
        )

    if not INDEX_PATH.exists():
        return IntegrationCheck(
            "Progressive Adoption Path",
            False,
            "INDEX.md not found",
            None
        )

    content = INDEX_PATH.read_text()

    # Find "Progressive Adoption Path" section
    adoption_section_match = re.search(
        r'##\s+Progressive Adoption Path(.*?)(?=^##\s|\Z)',
        content,
        re.DOTALL | re.MULTILINE
    )

    if not adoption_section_match:
        return IntegrationCheck(
            "Progressive Adoption Path",
            False,
            "Progressive Adoption Path section not found in INDEX.md",
            None
        )

    adoption_section = adoption_section_match.group(1)

    # Check if SAP is mentioned in adoption paths
    if sap_id in adoption_section:
        return IntegrationCheck(
            "Progressive Adoption Path",
            True,
            f"{sap_id} mentioned in Progressive Adoption Path",
            None
        )
    else:
        # Soft failure - warn but don't fail validation
        return IntegrationCheck(
            "Progressive Adoption Path",
            True,  # Pass with warning
            f"{sap_id} NOT mentioned in Progressive Adoption Path (warning: consider adding for discoverability)",
            None
        )


def check_dependencies(sap_id: str, metadata: Dict) -> IntegrationCheck:
    """Check that all dependencies reference valid SAPs."""
    dependencies = metadata.get('dependencies', [])

    if not dependencies or dependencies == ['None']:
        return IntegrationCheck(
            "Dependencies",
            True,
            f"{sap_id} has no dependencies (or depends on SAP-000 only)",
            None
        )

    # Check each dependency exists
    broken_deps = []
    for dep in dependencies:
        if dep == 'SAP-000':
            continue  # SAP-000 is foundational, always exists

        dep_dir = get_sap_directory(dep)
        if not dep_dir:
            broken_deps.append(dep)

    if broken_deps:
        return IntegrationCheck(
            "Dependencies",
            False,
            f"{sap_id} has broken dependencies: {', '.join(broken_deps)}",
            f"Dependencies reference non-existent SAPs: {broken_deps}"
        )
    else:
        return IntegrationCheck(
            "Dependencies",
            True,
            f"{sap_id} dependencies validated ({len(dependencies)} deps: {', '.join(dependencies)})",
            None
        )


def validate_sap_ecosystem_integration(sap_id: str, verbose: bool = False) -> ValidationResult:
    """
    Validate a SAP's integration across all 5 ecosystem integration points.

    Args:
        sap_id: SAP identifier (e.g., "SAP-053")
        verbose: Enable verbose output

    Returns:
        ValidationResult with all checks
    """
    result = ValidationResult(sap_id)

    # Get SAP directory and metadata
    sap_dir = get_sap_directory(sap_id)
    if not sap_dir:
        result.add_check(IntegrationCheck(
            "SAP Directory",
            False,
            f"{sap_id} directory not found in {SAP_DIR}",
            "SAP does not exist in ecosystem"
        ))
        return result

    metadata = extract_sap_metadata(sap_dir)

    if verbose:
        print(f"Validating {sap_id} (status={metadata.get('status', 'unknown')}, version={metadata.get('version', 'unknown')})")
        print(f"SAP directory: {sap_dir}")
        print()

    # Run all 5 integration point checks
    result.add_check(check_index_md(sap_id))
    result.add_check(check_catalog_json(sap_id))
    result.add_check(check_copier_yml(sap_id, metadata))
    result.add_check(check_progressive_adoption_path(sap_id, metadata))
    result.add_check(check_dependencies(sap_id, metadata))

    return result


def validate_all_saps(verbose: bool = False) -> Dict[str, ValidationResult]:
    """Validate all SAPs in ecosystem."""
    results = {}

    # Find all SAPs by scanning INDEX.md
    if not INDEX_PATH.exists():
        print(f"ERROR: INDEX.md not found at {INDEX_PATH}", file=sys.stderr)
        return results

    content = INDEX_PATH.read_text()
    sap_entries = SAP_ENTRY_PATTERN.findall(content)

    for sap_id, title in sap_entries:
        if verbose:
            print(f"\nValidating {sap_id}: {title}")
        result = validate_sap_ecosystem_integration(sap_id, verbose=False)
        results[sap_id] = result

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate SAP ecosystem integration across all 5 integration points"
    )
    parser.add_argument(
        "sap_id",
        nargs="?",
        help="SAP ID to validate (e.g., SAP-053), or --all for all SAPs"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all SAPs in ecosystem"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Validate usage
    if not args.sap_id and not args.all:
        parser.print_help()
        print("\nERROR: Provide a SAP ID or use --all", file=sys.stderr)
        sys.exit(6)

    # Validate all SAPs
    if args.all:
        results = validate_all_saps(verbose=args.verbose)

        if args.json:
            output = {
                "validation_type": "all",
                "total_saps": len(results),
                "passed": sum(1 for r in results.values() if r.passed),
                "failed": sum(1 for r in results.values() if not r.passed),
                "results": {sap_id: result.to_dict() for sap_id, result in results.items()}
            }
            print(json.dumps(output, indent=2))
        else:
            print("\n" + "=" * 70)
            print(f"Ecosystem Integration Validation: {len(results)} SAPs")
            print("=" * 70)

            passed = [sap_id for sap_id, r in results.items() if r.passed]
            failed = [sap_id for sap_id, r in results.items() if not r.passed]

            print(f"\n✅ Passed: {len(passed)}/{len(results)}")
            print(f"❌ Failed: {len(failed)}/{len(results)}")

            if failed:
                print("\nFailed SAPs:")
                for sap_id in sorted(failed):
                    result = results[sap_id]
                    failed_checks = [check.name for check in result.failed_checks]
                    print(f"  - {sap_id}: {', '.join(failed_checks)}")

        # Exit with error if any SAP failed
        sys.exit(0 if all(r.passed for r in results.values()) else 5)

    # Validate single SAP
    sap_id = args.sap_id

    if not validate_sap_id(sap_id):
        print(f"ERROR: Invalid SAP ID format: {sap_id} (expected: SAP-###)", file=sys.stderr)
        sys.exit(6)

    result = validate_sap_ecosystem_integration(sap_id, verbose=args.verbose)

    # Output results
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\nEcosystem Integration Validation: {sap_id}")
        print("=" * 70)

        for check in result.checks:
            status = "✅" if check.passed else "❌"
            print(f"\n{status} {check.name}")
            print(f"   {check.message}")
            if check.details and (not check.passed or args.verbose):
                print(f"   Details: {check.details}")

        print("\n" + "=" * 70)
        if result.passed:
            print(f"✅ SUCCESS: {sap_id} is fully integrated into the ecosystem")
        else:
            print(f"❌ FAILURE: {sap_id} has {len(result.failed_checks)} integration gap(s)")
            print(f"\nFailed checks:")
            for check in result.failed_checks:
                print(f"  - {check.name}: {check.message}")

    sys.exit(result.exit_code)


if __name__ == "__main__":
    main()
