#!/usr/bin/env python3
"""
Documentation Link Updater

Updates SAP-XXX references in documentation to modern chora.domain.capability namespaces.

Features:
- Scans markdown files for SAP-XXX references
- Updates to modern namespace format
- Preserves context (inline mentions, code blocks, etc.)
- Dry-run mode for preview
- Detailed change reporting

Usage:
    # Dry-run (preview changes)
    python scripts/update-doc-links.py --docs docs/ --dry-run

    # Update documentation
    python scripts/update-doc-links.py --docs docs/

    # Update specific file
    python scripts/update-doc-links.py --file docs/README.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# SAP-XXX pattern (matches SAP-000 through SAP-999)
SAP_PATTERN = re.compile(r'\bSAP-(\d{3})\b')


class DocLinkUpdater:
    """Updates SAP-XXX references to modern namespaces in documentation"""

    def __init__(
        self,
        alias_mapping_path: Path,
        dry_run: bool = False,
    ):
        self.alias_mapping_path = alias_mapping_path
        self.dry_run = dry_run
        self.aliases: Dict[str, str] = {}  # SAP-XXX -> modern namespace
        self.stats = {
            "total_files": 0,
            "updated_files": 0,
            "skipped_files": 0,
            "total_replacements": 0,
            "errors": 0,
        }
        self.changes: List[Dict] = []

    def load_aliases(self) -> bool:
        """Load SAP-XXX -> modern namespace alias mapping"""
        if not self.alias_mapping_path.exists():
            print(
                f"ERROR: Alias mapping file not found: {self.alias_mapping_path}",
                file=sys.stderr,
            )
            return False

        try:
            with open(self.alias_mapping_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Build alias dict: SAP-XXX -> modern namespace
            for legacy_id, info in data.get("aliases", {}).items():
                modern_namespace = info.get("namespace")
                if modern_namespace:
                    self.aliases[legacy_id] = modern_namespace

            print(f"Loaded {len(self.aliases)} alias mappings")
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

    def should_skip_line(self, line: str) -> bool:
        """
        Determine if a line should be skipped (don't update SAP-XXX)

        Skip:
        - Code blocks (```)
        - Example commands
        - File paths
        - Assessment report titles (preserve for historical records)
        """
        # Skip if in code fence
        if line.strip().startswith("```"):
            return True

        # Skip if it's a file path reference
        if "/SAP-" in line or "\\SAP-" in line:
            return True

        # Skip assessment report titles (historical records)
        if line.strip().startswith("# SAP-") and "assessment" in line.lower():
            return True

        return False

    def update_file_content(self, file_path: Path) -> Tuple[bool, int, str]:
        """
        Update SAP-XXX references in a file

        Returns:
            Tuple of (updated, num_replacements, new_content)
        """
        try:
            # Read file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            updated_lines = []
            in_code_block = False
            num_replacements = 0

            for line in lines:
                # Track code blocks
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block

                # Skip certain lines
                if in_code_block or self.should_skip_line(line):
                    updated_lines.append(line)
                    continue

                # Find and replace SAP-XXX references
                original_line = line
                for match in SAP_PATTERN.finditer(line):
                    sap_id = match.group(0)  # e.g., "SAP-015"

                    if sap_id in self.aliases:
                        modern_namespace = self.aliases[sap_id]

                        # Replace with modern namespace
                        # Format: SAP-015 -> chora.awareness.task_tracking (SAP-015)
                        replacement = f"{modern_namespace} ({sap_id})"
                        line = line.replace(sap_id, replacement, 1)

                        # Record change
                        self.changes.append({
                            "file": str(file_path),
                            "line": original_line.strip(),
                            "sap_id": sap_id,
                            "namespace": modern_namespace,
                        })

                        num_replacements += 1

                updated_lines.append(line)

            # Check if anything changed
            new_content = "\n".join(updated_lines)
            updated = new_content != content

            return updated, num_replacements, new_content

        except Exception as e:
            print(
                f"ERROR: Failed to update {file_path.name}: {e}", file=sys.stderr
            )
            self.stats["errors"] += 1
            return False, 0, ""

    def update_file(self, file_path: Path) -> bool:
        """Update a single markdown file"""
        self.stats["total_files"] += 1

        # Update content
        updated, num_replacements, new_content = self.update_file_content(file_path)

        if not updated:
            self.stats["skipped_files"] += 1
            return False

        # Write updated content (if not dry-run)
        if not self.dry_run:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
            except Exception as e:
                print(
                    f"ERROR: Failed to write {file_path.name}: {e}", file=sys.stderr
                )
                self.stats["errors"] += 1
                return False

        mode = "[DRY-RUN]" if self.dry_run else "[UPDATED]"
        print(f"{mode} {file_path.relative_to(file_path.parent.parent)}: {num_replacements} replacement(s)")

        self.stats["updated_files"] += 1
        self.stats["total_replacements"] += num_replacements
        return True

    def update_directory(self, docs_dir: Path) -> bool:
        """Update all markdown files in directory"""
        if not docs_dir.exists():
            print(
                f"ERROR: Documentation directory not found: {docs_dir}",
                file=sys.stderr,
            )
            return False

        # Find all markdown files
        md_files = list(docs_dir.rglob("*.md"))

        if not md_files:
            print(
                f"WARNING: No markdown files found in {docs_dir}",
                file=sys.stderr,
            )
            return False

        print("\n" + "=" * 80)
        print(
            f"Documentation Link Updater - {'DRY RUN' if self.dry_run else 'EXECUTING'}"
        )
        print("=" * 80)
        print(f"Documentation directory: {docs_dir}")
        print(f"Total markdown files: {len(md_files)}")
        print(f"Alias mappings: {len(self.aliases)}")
        print("=" * 80 + "\n")

        # Update each file
        for md_file in sorted(md_files):
            self.update_file(md_file)

        return self.stats["errors"] == 0

    def print_summary(self):
        """Print update summary"""
        print("\n" + "=" * 80)
        print("Update Summary")
        print("=" * 80)
        print(f"Total files scanned: {self.stats['total_files']}")
        print(f"Updated files: {self.stats['updated_files']}")
        print(f"Skipped files: {self.stats['skipped_files']}")
        print(f"Errors: {self.stats['errors']}")

        print(f"\nReplacements:")
        print(f"  Total: {self.stats['total_replacements']}")

        if self.stats['total_replacements'] > 0:
            print(
                f"\n{self.stats['total_replacements']} SAP-XXX reference(s) {'would be' if self.dry_run else 'were'} updated"
            )

        if self.stats["errors"] == 0:
            print(f"\nSUCCESS: All documentation links updated successfully")
        else:
            print(
                f"\nERROR: Update completed with errors", file=sys.stderr
            )

        if self.dry_run:
            print(f"\n(DRY RUN - No files were modified)")

        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Update SAP-XXX references to modern namespaces in documentation"
    )

    # Input
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--docs",
        type=Path,
        help="Documentation directory to update (recursively scans for *.md)",
    )
    group.add_argument(
        "--file",
        type=Path,
        help="Single file to update",
    )

    parser.add_argument(
        "--aliases",
        type=Path,
        default=Path("capabilities/alias-mapping.json"),
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
    updater = DocLinkUpdater(
        alias_mapping_path=args.aliases,
        dry_run=args.dry_run,
    )

    # Load alias mapping
    if not updater.load_aliases():
        sys.exit(2)

    # Update documentation
    if args.docs:
        success = updater.update_directory(args.docs)
    else:
        success = updater.update_file(args.file)

    # Print summary
    updater.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
