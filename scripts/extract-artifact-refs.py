#!/usr/bin/env python3
r"""
SAP Artifact Reference Extractor

Scans SAP directories for artifacts and generates artifact reference arrays for
Pattern-type capability manifests. Validates that all 5 required SAP artifacts
are present.

Features:
- Scans docs/skilled-awareness/{domain}/ directories
- Detects all 5 SAP artifact types
- Validates artifact presence and completeness
- Outputs warnings for missing artifacts
- Generates YAML-formatted artifact arrays
- Supports dry-run mode for validation only

Usage:
  # Extract artifacts for single SAP
  python scripts/extract-artifact-refs.py --sap agent-awareness

  # Extract artifacts for all SAPs
  python scripts/extract-artifact-refs.py --all

  # Validation mode (check for missing artifacts)
  python scripts/extract-artifact-refs.py --all --validate-only

  # Output as JSON
  python scripts/extract-artifact-refs.py --sap inbox --format json

Exit Codes:
  0 - All artifacts found
  1 - Missing artifacts detected
  2 - Invalid arguments or file access errors
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# Required SAP artifact files (canonical names)
REQUIRED_ARTIFACTS = {
    "capability-charter.md": "capability_charter",
    "protocol-spec.md": "protocol_specification",
    "adoption-blueprint.md": "adoption_blueprint",
    "ledger.md": "adoption_ledger",
}

# Awareness guide can have multiple names
AWARENESS_GUIDE_FILES = ["AGENTS.md", "awareness-guide.md", "CLAUDE.md"]


class ArtifactExtractor:
    """Extracts and validates SAP artifact references"""

    def __init__(
        self,
        base_dir: Path = Path("docs/skilled-awareness"),
        output_format: str = "yaml",
        validate_only: bool = False,
    ):
        self.base_dir = base_dir
        self.output_format = output_format
        self.validate_only = validate_only
        self.stats = {
            "total_saps": 0,
            "complete_saps": 0,
            "incomplete_saps": 0,
            "total_artifacts": 0,
            "missing_artifacts": 0,
        }

    def scan_sap_directory(self, sap_dir: Path) -> Dict:
        """Scan a single SAP directory for artifacts"""
        result = {
            "sap_name": sap_dir.name,
            "artifacts": [],
            "missing": [],
            "warnings": [],
            "complete": False,
        }

        if not sap_dir.exists() or not sap_dir.is_dir():
            result["warnings"].append(f"Directory not found or not accessible")
            return result

        # Check for required artifacts
        for file_name, artifact_type in REQUIRED_ARTIFACTS.items():
            artifact_path = sap_dir / file_name
            if artifact_path.exists():
                rel_path = str(artifact_path.relative_to(Path("docs/skilled-awareness")))
                result["artifacts"].append(
                    {
                        "type": artifact_type,
                        "path": f"docs/skilled-awareness/{rel_path}",
                        "format": "text/markdown",
                    }
                )
                self.stats["total_artifacts"] += 1
            else:
                result["missing"].append(file_name)
                result["warnings"].append(f"Missing required artifact: {file_name}")
                self.stats["missing_artifacts"] += 1

        # Check for awareness guide (can have multiple names)
        awareness_guide_found = False
        for guide_file in AWARENESS_GUIDE_FILES:
            guide_path = sap_dir / guide_file
            if guide_path.exists():
                rel_path = str(guide_path.relative_to(Path("docs/skilled-awareness")))
                result["artifacts"].append(
                    {
                        "type": "awareness_guide",
                        "path": f"docs/skilled-awareness/{rel_path}",
                        "format": "text/markdown",
                    }
                )
                awareness_guide_found = True
                self.stats["total_artifacts"] += 1
                break

        if not awareness_guide_found:
            result["missing"].append("AGENTS.md or awareness-guide.md")
            result["warnings"].append(
                f"Missing awareness guide (expected: {', '.join(AWARENESS_GUIDE_FILES)})"
            )
            self.stats["missing_artifacts"] += 1

        # Check completeness (all 5 artifacts present)
        expected_count = 5  # 4 required + 1 awareness guide
        actual_count = len(result["artifacts"])
        result["complete"] = actual_count == expected_count

        if result["complete"]:
            self.stats["complete_saps"] += 1
        else:
            self.stats["incomplete_saps"] += 1

        self.stats["total_saps"] += 1

        return result

    def scan_all_saps(self) -> List[Dict]:
        """Scan all SAP directories"""
        results = []

        if not self.base_dir.exists():
            print(f"ERROR: Base directory not found: {self.base_dir}", file=sys.stderr)
            return results

        # Get all subdirectories
        for sap_dir in sorted(self.base_dir.iterdir()):
            if not sap_dir.is_dir():
                continue

            # Skip special directories
            if sap_dir.name.startswith(".") or sap_dir.name in [
                "templates",
                "archive",
            ]:
                continue

            result = self.scan_sap_directory(sap_dir)
            results.append(result)

        return results

    def format_artifacts_yaml(self, artifacts: List[Dict]) -> str:
        """Format artifacts as YAML"""
        if not artifacts:
            return "artifacts: []"

        yaml_str = yaml.dump(
            {"artifacts": artifacts},
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        return yaml_str.strip()

    def format_artifacts_json(self, artifacts: List[Dict]) -> str:
        """Format artifacts as JSON"""
        return json.dumps({"artifacts": artifacts}, indent=2)

    def print_result(self, result: Dict):
        """Print extraction result for a single SAP"""
        sap_name = result["sap_name"]
        artifacts = result["artifacts"]
        missing = result["missing"]
        complete = result["complete"]

        print(f"\n{'='*80}")
        print(f"SAP: {sap_name}")
        print(f"{'='*80}")
        print(f"Status: {'COMPLETE' if complete else 'INCOMPLETE'}")
        print(f"Artifacts found: {len(artifacts)}/5")

        if artifacts:
            print(f"\nArtifacts:")
            for artifact in artifacts:
                print(f"  - {artifact['type']}: {artifact['path']}")

        if missing:
            print(f"\nMissing artifacts:")
            for artifact in missing:
                print(f"  - {artifact}")

        if result["warnings"]:
            print(f"\nWarnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")

        if not self.validate_only and artifacts:
            print(f"\nGenerated artifact array ({self.output_format}):")
            print("-" * 80)
            if self.output_format == "yaml":
                print(self.format_artifacts_yaml(artifacts))
            else:
                print(self.format_artifacts_json(artifacts))

    def print_summary(self, results: List[Dict]):
        """Print summary statistics"""
        print(f"\n{'='*80}")
        print("Extraction Summary")
        print(f"{'='*80}")
        print(f"Total SAPs scanned: {self.stats['total_saps']}")
        print(f"Complete SAPs (5/5 artifacts): {self.stats['complete_saps']}")
        print(f"Incomplete SAPs: {self.stats['incomplete_saps']}")
        print(f"Total artifacts found: {self.stats['total_artifacts']}")
        print(f"Missing artifacts: {self.stats['missing_artifacts']}")

        if self.stats["incomplete_saps"] > 0:
            print(f"\nIncomplete SAPs:")
            for result in results:
                if not result["complete"]:
                    print(
                        f"  - {result['sap_name']}: {len(result['artifacts'])}/5 artifacts"
                    )

        if self.stats["missing_artifacts"] == 0:
            print(f"\nSUCCESS: All SAPs have complete artifact sets")
        else:
            print(f"\nWARNING: {self.stats['incomplete_saps']} SAP(s) missing artifacts")

        print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract and validate SAP artifact references"
    )

    # Input
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("docs/skilled-awareness"),
        help="Base directory for SAP artifacts (default: docs/skilled-awareness)",
    )

    # Scan modes
    scan_mode = parser.add_mutually_exclusive_group(required=True)
    scan_mode.add_argument("--all", action="store_true", help="Scan all SAP directories")
    scan_mode.add_argument(
        "--sap", type=str, help="Scan single SAP directory (e.g., agent-awareness)"
    )

    # Output
    parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format (default: yaml)",
    )

    # Options
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validation mode (check for missing artifacts, don't generate output)",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode (only show summary)",
    )

    args = parser.parse_args()

    # Initialize extractor
    extractor = ArtifactExtractor(
        base_dir=args.base_dir,
        output_format=args.format,
        validate_only=args.validate_only,
    )

    # Run extraction
    if args.all:
        results = extractor.scan_all_saps()
    elif args.sap:
        sap_dir = args.base_dir / args.sap
        result = extractor.scan_sap_directory(sap_dir)
        results = [result]
    else:
        print("ERROR: Must specify --all or --sap", file=sys.stderr)
        sys.exit(2)

    # Print results
    if not args.quiet:
        for result in results:
            extractor.print_result(result)

    # Print summary
    extractor.print_summary(results)

    # Exit with appropriate code
    if extractor.stats["missing_artifacts"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
