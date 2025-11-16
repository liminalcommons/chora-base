#!/usr/bin/env python3
"""
Fix Relationship Type Violations

Fixes cross-type dependency relationship type violations identified during
Phase 2 validation.

Relationship Type Rules:
- Service -> Service: runtime, prerequisite, optional, extends
- Service -> Pattern: prerequisite, optional, extends (NOT runtime)
- Pattern -> Service: runtime, optional (NOT prerequisite)
- Pattern -> Pattern: prerequisite, optional, extends

Usage:
    python scripts/fix-relationship-types.py [--dry-run]
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


class RelationshipTypeFixer:
    """Fixes relationship type violations in capability manifests"""

    # Relationship type fixes to apply
    # Format: (source_capability, target_capability, old_relationship, new_relationship)
    FIXES = [
        # Type 1: Service -> Pattern with "runtime" (should be "prerequisite")
        ("chora.awareness.sap_self_evaluation", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.awareness.task_tracking", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.awareness.task_tracking", "chora.awareness.memory_system", "runtime", "prerequisite"),
        ("chora.devex.bootstrap", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.documentation_framework", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.interface_design", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.multi_interface", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.registry", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.capability_server_template", "chora.infrastructure.sap_framework", "runtime", "prerequisite"),
        ("chora.devex.capability_server_template", "chora.devex.composition", "runtime", "prerequisite"),

        # Type 2: Pattern -> Service with "prerequisite" (should be "runtime")
        ("chora.awareness.agent_awareness", "chora.devex.documentation_framework", "prerequisite", "runtime"),
        ("chora.awareness.development_lifecycle", "chora.devex.documentation_framework", "prerequisite", "runtime"),
        ("chora.devex.composition", "chora.devex.interface_design", "prerequisite", "runtime"),
        ("chora.devex.composition", "chora.devex.registry", "prerequisite", "runtime"),
    ]

    def __init__(self, capabilities_dir: Path, dry_run: bool = False):
        self.capabilities_dir = capabilities_dir
        self.dry_run = dry_run
        self.stats = {
            "total_fixes": len(self.FIXES),
            "applied_fixes": 0,
            "failed_fixes": 0,
            "manifests_updated": 0,
        }

    def fix_manifest(self, source_capability: str, target_capability: str,
                     old_relationship: str, new_relationship: str) -> bool:
        """
        Fix a single relationship type in a manifest

        Returns:
            True if fix was applied successfully
        """
        manifest_path = self.capabilities_dir / f"{source_capability}.yaml"

        if not manifest_path.exists():
            print(f"ERROR: Manifest not found: {manifest_path}", file=sys.stderr)
            self.stats["failed_fixes"] += 1
            return False

        try:
            # Read manifest
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f)

            # Find and update the dependency
            dc_relation = manifest.get("dc_relation", {})
            requires = dc_relation.get("requires", [])

            updated = False
            for dep in requires:
                if (dep.get("capability") == target_capability and
                    dep.get("relationship") == old_relationship):

                    # Apply fix
                    dep["relationship"] = new_relationship
                    updated = True

                    mode = "[DRY-RUN]" if self.dry_run else "[FIXED]"
                    print(f"{mode} {source_capability}")
                    print(f"  -> {target_capability}: {old_relationship} -> {new_relationship}")
                    break

            if not updated:
                print(f"WARNING: Dependency not found in {source_capability}", file=sys.stderr)
                print(f"  Looking for: {target_capability} with relationship '{old_relationship}'", file=sys.stderr)
                self.stats["failed_fixes"] += 1
                return False

            # Write updated manifest (if not dry-run)
            if not self.dry_run:
                with open(manifest_path, "w", encoding="utf-8") as f:
                    yaml.dump(
                        manifest,
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False,
                    )

            self.stats["applied_fixes"] += 1
            return True

        except yaml.YAMLError as e:
            print(f"ERROR: Failed to parse {manifest_path.name}: {e}", file=sys.stderr)
            self.stats["failed_fixes"] += 1
            return False
        except Exception as e:
            print(f"ERROR: Failed to fix {manifest_path.name}: {e}", file=sys.stderr)
            self.stats["failed_fixes"] += 1
            return False

    def fix_all(self) -> bool:
        """Apply all relationship type fixes"""
        print("\n" + "=" * 80)
        print(f"Relationship Type Fixer - {'DRY RUN' if self.dry_run else 'EXECUTING'}")
        print("=" * 80)
        print(f"Capabilities directory: {self.capabilities_dir}")
        print(f"Total fixes to apply: {len(self.FIXES)}")
        print("=" * 80 + "\n")

        # Group fixes by source capability
        by_capability: Dict[str, List[Tuple]] = {}
        for fix in self.FIXES:
            source = fix[0]
            if source not in by_capability:
                by_capability[source] = []
            by_capability[source].append(fix)

        # Apply fixes
        for source_capability, fixes in sorted(by_capability.items()):
            print(f"\n{source_capability}:")
            for fix in fixes:
                self.fix_manifest(*fix)

        self.stats["manifests_updated"] = len(by_capability)

        return self.stats["failed_fixes"] == 0

    def print_summary(self):
        """Print fix summary"""
        print("\n" + "=" * 80)
        print("Fix Summary")
        print("=" * 80)
        print(f"Total fixes planned: {self.stats['total_fixes']}")
        print(f"Applied successfully: {self.stats['applied_fixes']}")
        print(f"Failed: {self.stats['failed_fixes']}")
        print(f"Manifests updated: {self.stats['manifests_updated']}")

        if self.stats["failed_fixes"] == 0:
            print(f"\nSUCCESS: All relationship types {'would be' if self.dry_run else 'were'} fixed")
        else:
            print(f"\nERROR: {self.stats['failed_fixes']} fix(es) failed", file=sys.stderr)

        if self.dry_run:
            print(f"\n(DRY RUN - No files were modified)")

        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Fix relationship type violations in capability manifests"
    )

    parser.add_argument(
        "--capabilities",
        type=Path,
        default=Path("capabilities"),
        help="Directory containing capability manifests (default: capabilities/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode (preview changes without modifying files)",
    )

    args = parser.parse_args()

    # Initialize fixer
    fixer = RelationshipTypeFixer(
        capabilities_dir=args.capabilities,
        dry_run=args.dry_run,
    )

    # Apply fixes
    success = fixer.fix_all()

    # Print summary
    fixer.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
