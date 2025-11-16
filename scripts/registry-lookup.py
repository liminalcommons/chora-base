#!/usr/bin/env python3
r"""
Dual-Mode Registry Lookup Validator

Validates backward compatibility by supporting lookups in both legacy (SAP-XXX)
and unified (chora.domain.capability) namespace formats.

Features:
- Loads all capability manifests from capabilities/ directory
- Builds dual indexes (legacy ID -> manifest, namespace -> manifest)
- Provides lookup functions for both formats
- Validates all pilot capabilities resolve correctly
- Shows deprecation warnings for legacy format usage
- Tests alias mechanism for smooth migration

Usage:
  # Lookup by new namespace
  python scripts/registry-lookup.py --lookup chora.devex.registry

  # Lookup by legacy ID (with deprecation warning)
  python scripts/registry-lookup.py --lookup SAP-044

  # Validate all pilot capabilities (dual-mode test)
  python scripts/registry-lookup.py --validate-all

  # Show registry statistics
  python scripts/registry-lookup.py --stats

Exit Codes:
  0 - All lookups successful, backward compatibility validated
  1 - Lookup failures or validation errors
  2 - Invalid arguments or file access errors
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


class RegistryLookup:
    """Dual-mode registry lookup with backward compatibility"""

    def __init__(self, capabilities_dir: Path = Path("capabilities")):
        self.capabilities_dir = capabilities_dir
        self.namespace_index: Dict[str, Dict] = {}  # chora.domain.capability -> manifest
        self.legacy_index: Dict[str, Dict] = {}     # SAP-XXX -> manifest
        self.deprecation_warnings: List[str] = []
        self.stats = {
            "total_capabilities": 0,
            "service_type": 0,
            "pattern_type": 0,
            "legacy_lookups": 0,
            "modern_lookups": 0,
            "lookup_failures": 0,
        }

    def load_manifests(self) -> bool:
        """Load all capability manifests and build indexes"""
        if not self.capabilities_dir.exists():
            print(
                f"ERROR: Capabilities directory not found: {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        yaml_files = list(self.capabilities_dir.glob("*.yaml")) + list(
            self.capabilities_dir.glob("*.yml")
        )

        if not yaml_files:
            print(
                f"WARNING: No YAML files found in {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    manifest = yaml.safe_load(f)

                # Validate manifest structure
                if not manifest or "metadata" not in manifest:
                    print(
                        f"WARNING: Invalid manifest structure in {yaml_file.name}",
                        file=sys.stderr,
                    )
                    continue

                metadata = manifest["metadata"]
                namespace = metadata.get("dc_identifier")
                legacy_id = metadata.get("dc_identifier_legacy")
                cap_type = metadata.get("dc_type")

                if not namespace:
                    print(
                        f"WARNING: Missing dc_identifier in {yaml_file.name}",
                        file=sys.stderr,
                    )
                    continue

                # Add to namespace index
                self.namespace_index[namespace] = {
                    "manifest": manifest,
                    "file_path": str(yaml_file),
                }

                # Add to legacy index if legacy ID present
                if legacy_id:
                    self.legacy_index[legacy_id] = {
                        "manifest": manifest,
                        "file_path": str(yaml_file),
                        "modern_namespace": namespace,  # For migration
                    }

                # Update stats
                self.stats["total_capabilities"] += 1
                if cap_type == "Service":
                    self.stats["service_type"] += 1
                elif cap_type == "Pattern":
                    self.stats["pattern_type"] += 1

            except yaml.YAMLError as e:
                print(
                    f"ERROR: Failed to parse {yaml_file.name}: {e}", file=sys.stderr
                )
                continue
            except Exception as e:
                print(
                    f"ERROR: Failed to load {yaml_file.name}: {e}", file=sys.stderr
                )
                continue

        print(
            f"Loaded {self.stats['total_capabilities']} capabilities "
            f"({self.stats['service_type']} Service, {self.stats['pattern_type']} Pattern)"
        )
        return True

    def lookup(self, identifier: str, show_deprecation: bool = True) -> Optional[Dict]:
        """
        Lookup capability by either namespace or legacy ID

        Args:
            identifier: Either 'chora.domain.capability' or 'SAP-XXX'
            show_deprecation: Show deprecation warning for legacy lookups

        Returns:
            Capability manifest dict or None if not found
        """
        # Try modern namespace first
        if identifier in self.namespace_index:
            self.stats["modern_lookups"] += 1
            return self.namespace_index[identifier]

        # Try legacy ID with deprecation warning
        if identifier in self.legacy_index:
            self.stats["legacy_lookups"] += 1
            result = self.legacy_index[identifier]

            if show_deprecation:
                modern_namespace = result["modern_namespace"]
                warning = (
                    f"DEPRECATION WARNING: Legacy ID '{identifier}' is deprecated. "
                    f"Use '{modern_namespace}' instead."
                )
                self.deprecation_warnings.append(warning)
                print(f"\n{warning}", file=sys.stderr)

            return result

        # Not found
        self.stats["lookup_failures"] += 1
        return None

    def validate_dual_mode(self) -> Tuple[int, int]:
        """
        Validate dual-mode lookups for all capabilities

        Tests that each capability can be looked up by both:
        1. Modern namespace (chora.domain.capability)
        2. Legacy ID (SAP-XXX) if present

        Returns:
            Tuple of (successful_tests, failed_tests)
        """
        successful = 0
        failed = 0

        print("\n" + "=" * 80)
        print("Dual-Mode Lookup Validation")
        print("=" * 80)

        for namespace, entry in self.namespace_index.items():
            manifest = entry["manifest"]
            metadata = manifest["metadata"]
            legacy_id = metadata.get("dc_identifier_legacy")
            title = metadata.get("dc_title", "Unknown")

            print(f"\nTesting: {title}")
            print(f"  Namespace: {namespace}")
            if legacy_id:
                print(f"  Legacy ID: {legacy_id}")

            # Test 1: Modern namespace lookup
            result_modern = self.lookup(namespace, show_deprecation=False)
            if result_modern:
                print(f"  [PASS] Modern lookup: {namespace}")
                successful += 1
            else:
                print(f"  [FAIL] Modern lookup failed: {namespace}", file=sys.stderr)
                failed += 1

            # Test 2: Legacy ID lookup (if present)
            if legacy_id:
                result_legacy = self.lookup(legacy_id, show_deprecation=False)
                if result_legacy:
                    # Verify it resolves to same capability
                    resolved_namespace = result_legacy["modern_namespace"]
                    if resolved_namespace == namespace:
                        print(f"  [PASS] Legacy lookup: {legacy_id} -> {namespace}")
                        successful += 1
                    else:
                        print(
                            f"  [FAIL] Legacy lookup resolved to wrong namespace: "
                            f"{legacy_id} -> {resolved_namespace} (expected {namespace})",
                            file=sys.stderr,
                        )
                        failed += 1
                else:
                    print(
                        f"  [FAIL] Legacy lookup failed: {legacy_id}", file=sys.stderr
                    )
                    failed += 1
            else:
                print(f"  [SKIP] No legacy ID present")

        return successful, failed

    def print_lookup_result(self, identifier: str, result: Optional[Dict]):
        """Pretty print lookup result"""
        print(f"\n{'=' * 80}")
        print(f"Lookup: {identifier}")
        print(f"{'=' * 80}")

        if not result:
            print(f"NOT FOUND: No capability found for '{identifier}'")
            return

        manifest = result["manifest"]
        metadata = manifest["metadata"]

        print(f"Status: FOUND")
        print(f"File: {result['file_path']}")
        print(f"\nMetadata:")
        print(f"  Namespace: {metadata.get('dc_identifier')}")
        print(f"  Legacy ID: {metadata.get('dc_identifier_legacy', 'N/A')}")
        print(f"  Title: {metadata.get('dc_title')}")
        print(f"  Type: {metadata.get('dc_type')}")
        print(f"  Version: {metadata.get('dc_hasVersion')}")
        print(f"  Description: {metadata.get('dc_description')}")

        # Show migration info if legacy lookup
        if "modern_namespace" in result:
            print(f"\nMigration Info:")
            print(f"  Modern Namespace: {result['modern_namespace']}")
            print(
                f"  Recommendation: Update references to use '{result['modern_namespace']}'"
            )

    def print_statistics(self):
        """Print registry statistics"""
        print(f"\n{'=' * 80}")
        print("Registry Statistics")
        print(f"{'=' * 80}")
        print(f"Total Capabilities: {self.stats['total_capabilities']}")
        print(f"  Service-type: {self.stats['service_type']}")
        print(f"  Pattern-type: {self.stats['pattern_type']}")
        print(f"\nNamespace Index: {len(self.namespace_index)} entries")
        print(f"Legacy Index: {len(self.legacy_index)} entries")
        print(
            f"Backward Compatibility: {len(self.legacy_index)}/{self.stats['total_capabilities']} "
            f"({100 * len(self.legacy_index) // max(1, self.stats['total_capabilities'])}%)"
        )

        print(f"\nLookup Activity:")
        print(f"  Modern lookups: {self.stats['modern_lookups']}")
        print(f"  Legacy lookups: {self.stats['legacy_lookups']}")
        print(f"  Failed lookups: {self.stats['lookup_failures']}")

        if self.deprecation_warnings:
            print(f"\nDeprecation Warnings: {len(self.deprecation_warnings)}")

    def export_alias_mapping(self, output_file: Path):
        """Export legacy ID -> namespace alias mapping"""
        mapping = {}
        for legacy_id, entry in self.legacy_index.items():
            mapping[legacy_id] = {
                "namespace": entry["modern_namespace"],
                "status": "deprecated",
                "sunset_date": "2026-06-01",  # Example sunset timeline
            }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "aliases": mapping}, f, indent=2)

        print(f"\nAlias mapping exported to: {output_file}")
        print(f"Total aliases: {len(mapping)}")


def main():
    parser = argparse.ArgumentParser(
        description="Dual-mode registry lookup with backward compatibility"
    )

    # Actions
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--lookup", type=str, help="Lookup capability by namespace or legacy ID"
    )
    action.add_argument(
        "--validate-all",
        action="store_true",
        help="Validate dual-mode lookups for all capabilities",
    )
    action.add_argument(
        "--stats", action="store_true", help="Show registry statistics"
    )
    action.add_argument(
        "--export-aliases",
        type=Path,
        help="Export alias mapping to JSON file (e.g., aliases.json)",
    )

    # Options
    parser.add_argument(
        "--capabilities-dir",
        type=Path,
        default=Path("capabilities"),
        help="Directory containing capability manifests (default: capabilities/)",
    )
    parser.add_argument(
        "--no-deprecation-warnings",
        action="store_true",
        help="Suppress deprecation warnings for legacy lookups",
    )

    args = parser.parse_args()

    # Initialize registry
    registry = RegistryLookup(capabilities_dir=args.capabilities_dir)

    # Load manifests
    if not registry.load_manifests():
        sys.exit(2)

    # Execute action
    if args.lookup:
        # Single lookup
        result = registry.lookup(
            args.lookup, show_deprecation=not args.no_deprecation_warnings
        )
        registry.print_lookup_result(args.lookup, result)
        registry.print_statistics()

        if result:
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.validate_all:
        # Validate dual-mode for all capabilities
        successful, failed = registry.validate_dual_mode()

        print(f"\n{'=' * 80}")
        print("Validation Summary")
        print(f"{'=' * 80}")
        print(f"Total Tests: {successful + failed}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        if failed == 0:
            print(f"\nSUCCESS: All dual-mode lookups validated successfully")
            registry.print_statistics()
            sys.exit(0)
        else:
            print(
                f"\nERROR: {failed} validation test(s) failed", file=sys.stderr
            )
            registry.print_statistics()
            sys.exit(1)

    elif args.stats:
        # Show statistics only
        registry.print_statistics()
        sys.exit(0)

    elif args.export_aliases:
        # Export alias mapping
        registry.export_alias_mapping(args.export_aliases)
        registry.print_statistics()
        sys.exit(0)


if __name__ == "__main__":
    main()
