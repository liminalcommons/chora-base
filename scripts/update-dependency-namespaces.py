#!/usr/bin/env python3
r"""
Dependency Namespace Updater

Updates dependency references in capability manifests from legacy SAP-XXX format
to modern chora.domain.capability namespace format.

Features:
- Loads alias mapping (SAP-XXX -> modern namespace)
- Updates all dependency references in manifests
- Preserves version and relationship metadata
- Dry-run mode for preview
- Validation of updated manifests
- Detailed reporting of changes

Usage:
  # Dry-run (preview changes)
  python scripts/update-dependency-namespaces.py \
      --capabilities capabilities/ \
      --dry-run

  # Update dependencies
  python scripts/update-dependency-namespaces.py \
      --capabilities capabilities/

  # Use custom alias mapping
  python scripts/update-dependency-namespaces.py \
      --capabilities capabilities/ \
      --aliases custom-aliases.json

Exit Codes:
  0 - All dependencies updated successfully
  1 - Update errors
  2 - Invalid arguments or file access errors
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# Legacy dependency pattern: chora.SAP-XXX or SAP-XXX
LEGACY_PATTERN = re.compile(r"^(chora\.)?SAP-\d+$")


class DependencyUpdater:
    """Updates dependency namespaces from legacy to modern format"""

    def __init__(
        self,
        capabilities_dir: Path,
        aliases_file: Optional[Path] = None,
        dry_run: bool = False,
    ):
        self.capabilities_dir = capabilities_dir
        self.aliases_file = aliases_file or capabilities_dir / "alias-mapping.json"
        self.dry_run = dry_run
        self.aliases: Dict[str, str] = {}  # SAP-XXX -> modern namespace
        self.stats = {
            "total_manifests": 0,
            "updated_manifests": 0,
            "skipped_manifests": 0,
            "total_dependencies": 0,
            "updated_dependencies": 0,
            "unresolved_dependencies": 0,
            "errors": 0,
        }
        self.changes: List[Dict] = []
        self.unresolved: Set[str] = set()

    def load_aliases(self) -> bool:
        """Load SAP-XXX -> modern namespace alias mapping"""
        if not self.aliases_file.exists():
            print(
                f"ERROR: Alias mapping file not found: {self.aliases_file}",
                file=sys.stderr,
            )
            return False

        try:
            with open(self.aliases_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Build alias dict: SAP-XXX -> modern namespace
            for legacy_id, info in data.get("aliases", {}).items():
                modern_namespace = info.get("namespace")
                if modern_namespace:
                    self.aliases[legacy_id] = modern_namespace
                    # Also support "chora.SAP-XXX" format
                    self.aliases[f"chora.{legacy_id}"] = modern_namespace

            print(f"Loaded {len(self.aliases) // 2} alias mappings")
            return True

        except json.JSONDecodeError as e:
            print(
                f"ERROR: Invalid JSON in alias file: {e}", file=sys.stderr
            )
            return False
        except Exception as e:
            print(
                f"ERROR: Failed to load alias file: {e}", file=sys.stderr
            )
            return False

    def resolve_dependency(self, dep_namespace: str) -> Optional[str]:
        """
        Resolve legacy dependency namespace to modern format

        Args:
            dep_namespace: Either "SAP-XXX" or "chora.SAP-XXX" or modern namespace

        Returns:
            Modern namespace or None if unresolved
        """
        # Check if already modern format (doesn't match legacy pattern)
        if not LEGACY_PATTERN.match(dep_namespace):
            return dep_namespace  # Already modern, no change needed

        # Try direct lookup
        if dep_namespace in self.aliases:
            return self.aliases[dep_namespace]

        # Try without "chora." prefix
        if dep_namespace.startswith("chora."):
            legacy_id = dep_namespace[6:]  # Remove "chora." prefix
            if legacy_id in self.aliases:
                return self.aliases[legacy_id]

        # Unresolved
        self.unresolved.add(dep_namespace)
        return None

    def update_manifest_dependencies(
        self, manifest_path: Path
    ) -> Tuple[bool, int]:
        """
        Update dependencies in a single manifest

        Returns:
            Tuple of (updated, num_changes)
        """
        try:
            # Read manifest
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f)

            if not manifest or "metadata" not in manifest:
                print(
                    f"WARNING: Invalid manifest structure: {manifest_path.name}",
                    file=sys.stderr,
                )
                self.stats["skipped_manifests"] += 1
                return False, 0

            namespace = manifest["metadata"].get("dc_identifier")
            if not namespace:
                print(
                    f"WARNING: Missing dc_identifier: {manifest_path.name}",
                    file=sys.stderr,
                )
                self.stats["skipped_manifests"] += 1
                return False, 0

            # Get dependencies
            dc_relation = manifest.get("dc_relation", {})
            requires = dc_relation.get("requires", [])

            if not requires:
                # No dependencies to update
                self.stats["skipped_manifests"] += 1
                return False, 0

            # Update dependencies
            updated_count = 0
            for i, dep in enumerate(requires):
                if isinstance(dep, str):
                    # Convert string to dict
                    dep = {"capability": dep, "relationship": "prerequisite"}
                    requires[i] = dep
                elif not isinstance(dep, dict):
                    print(
                        f"WARNING: Invalid dependency format in {manifest_path.name}: {dep}",
                        file=sys.stderr,
                    )
                    continue

                dep_namespace = dep.get("capability")
                if not dep_namespace:
                    continue

                self.stats["total_dependencies"] += 1

                # Resolve dependency
                modern_namespace = self.resolve_dependency(dep_namespace)

                if modern_namespace and modern_namespace != dep_namespace:
                    # Update dependency
                    old_namespace = dep_namespace
                    dep["capability"] = modern_namespace

                    # Record change
                    self.changes.append(
                        {
                            "manifest": namespace,
                            "file": manifest_path.name,
                            "old": old_namespace,
                            "new": modern_namespace,
                            "relationship": dep.get("relationship", "prerequisite"),
                        }
                    )

                    updated_count += 1
                    self.stats["updated_dependencies"] += 1

                elif not modern_namespace:
                    # Unresolved dependency
                    self.stats["unresolved_dependencies"] += 1

            # Write updated manifest (if not dry-run and changes made)
            if updated_count > 0:
                if not self.dry_run:
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        yaml.dump(
                            manifest,
                            f,
                            default_flow_style=False,
                            allow_unicode=True,
                            sort_keys=False,
                        )

                self.stats["updated_manifests"] += 1
                return True, updated_count

            self.stats["skipped_manifests"] += 1
            return False, 0

        except yaml.YAMLError as e:
            print(
                f"ERROR: Failed to parse {manifest_path.name}: {e}", file=sys.stderr
            )
            self.stats["errors"] += 1
            return False, 0
        except Exception as e:
            print(
                f"ERROR: Failed to update {manifest_path.name}: {e}", file=sys.stderr
            )
            self.stats["errors"] += 1
            return False, 0

    def update_all(self) -> bool:
        """Update all capability manifests"""
        if not self.capabilities_dir.exists():
            print(
                f"ERROR: Capabilities directory not found: {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        # Get all YAML files
        yaml_files = list(self.capabilities_dir.glob("*.yaml")) + list(
            self.capabilities_dir.glob("*.yml")
        )

        # Filter out template files
        yaml_files = [f for f in yaml_files if "template" not in f.name.lower()]

        if not yaml_files:
            print(
                f"WARNING: No YAML files found in {self.capabilities_dir}",
                file=sys.stderr,
            )
            return False

        print("\n" + "=" * 80)
        print(
            f"Dependency Namespace Update - {'DRY RUN' if self.dry_run else 'EXECUTING'}"
        )
        print("=" * 80)
        print(f"Capabilities directory: {self.capabilities_dir}")
        print(f"Total manifests: {len(yaml_files)}")
        print(f"Alias mappings: {len(self.aliases) // 2}")
        print("=" * 80 + "\n")

        # Update each manifest
        for yaml_file in sorted(yaml_files):
            self.stats["total_manifests"] += 1
            updated, num_changes = self.update_manifest_dependencies(yaml_file)

            if updated:
                mode = "[DRY-RUN]" if self.dry_run else "[UPDATED]"
                print(
                    f"{mode} {yaml_file.name}: {num_changes} dependency update(s)"
                )

        return self.stats["errors"] == 0

    def print_changes(self):
        """Print detailed list of changes"""
        if not self.changes:
            return

        print("\n" + "=" * 80)
        print("Dependency Changes")
        print("=" * 80)

        # Group by manifest
        by_manifest: Dict[str, List[Dict]] = {}
        for change in self.changes:
            manifest = change["manifest"]
            if manifest not in by_manifest:
                by_manifest[manifest] = []
            by_manifest[manifest].append(change)

        for manifest, changes in sorted(by_manifest.items()):
            print(f"\n{manifest} ({changes[0]['file']}):")
            for change in changes:
                print(f"  - {change['old']} -> {change['new']}")
                print(f"    Relationship: {change['relationship']}")

    def print_unresolved(self):
        """Print unresolved dependencies"""
        if not self.unresolved:
            return

        print("\n" + "=" * 80)
        print("Unresolved Dependencies")
        print("=" * 80)
        print(
            f"Found {len(self.unresolved)} unresolved dependency reference(s):\n"
        )

        for dep in sorted(self.unresolved):
            print(f"  - {dep}")

        print(
            f"\nThese dependencies could not be resolved to modern namespaces."
        )
        print(
            f"Possible reasons:"
        )
        print(f"  1. Capability not yet migrated")
        print(f"  2. Missing from alias mapping")
        print(f"  3. Typo in dependency reference")

    def print_summary(self):
        """Print update summary"""
        print("\n" + "=" * 80)
        print("Update Summary")
        print("=" * 80)
        print(f"Total manifests: {self.stats['total_manifests']}")
        print(f"Updated manifests: {self.stats['updated_manifests']}")
        print(f"Skipped manifests: {self.stats['skipped_manifests']}")
        print(f"Errors: {self.stats['errors']}")

        print(f"\nDependencies:")
        print(f"  Total: {self.stats['total_dependencies']}")
        print(f"  Updated: {self.stats['updated_dependencies']}")
        print(f"  Unresolved: {self.stats['unresolved_dependencies']}")

        if self.stats["updated_dependencies"] > 0:
            print(
                f"\n{len(self.changes)} dependency update(s) {'would be' if self.dry_run else 'were'} made"
            )

        if self.stats["errors"] == 0 and self.stats["unresolved_dependencies"] == 0:
            print(f"\nSUCCESS: All dependencies updated successfully")
        elif self.stats["unresolved_dependencies"] > 0:
            print(
                f"\nWARNING: {self.stats['unresolved_dependencies']} unresolved dependency reference(s)",
                file=sys.stderr,
            )
        else:
            print(
                f"\nERROR: Update completed with errors", file=sys.stderr
            )

        if self.dry_run:
            print(f"\n(DRY RUN - No files were modified)")

        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Update dependency namespaces from legacy to modern format"
    )

    # Input
    parser.add_argument(
        "--capabilities",
        type=Path,
        default=Path("capabilities"),
        help="Directory containing capability manifests (default: capabilities/)",
    )
    parser.add_argument(
        "--aliases",
        type=Path,
        help="Alias mapping JSON file (default: capabilities/alias-mapping.json)",
    )

    # Options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode (preview changes without modifying files)",
    )

    args = parser.parse_args()

    # Initialize updater
    updater = DependencyUpdater(
        capabilities_dir=args.capabilities,
        aliases_file=args.aliases,
        dry_run=args.dry_run,
    )

    # Load alias mapping
    if not updater.load_aliases():
        sys.exit(2)

    # Update dependencies
    success = updater.update_all()

    # Print results
    updater.print_changes()
    updater.print_unresolved()
    updater.print_summary()

    # Exit with appropriate code
    if updater.stats["errors"] > 0:
        sys.exit(1)
    elif updater.stats["unresolved_dependencies"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
