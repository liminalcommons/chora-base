#!/usr/bin/env python3
"""Rollback migration to angle brackets (restore from backups).

This script finds all .backup files in the template/ directory and restores
them to their original filenames (removing the .backup extension).

Usage:
    python scripts/rollback-migration.py
    python scripts/rollback-migration.py --dry-run  # Preview without changes
    python scripts/rollback-migration.py --verbose  # Show each file restored
"""

import shutil
import sys
from pathlib import Path


def find_backup_files(base_dir="template"):
    """Find all .backup files in the specified directory.

    Args:
        base_dir: Base directory to search (default: template/)

    Returns:
        List of Path objects for .backup files
    """
    base_path = Path(base_dir)

    if not base_path.exists():
        return []

    return list(base_path.glob("**/*.backup"))


def restore_backup(backup_path, dry_run=False, verbose=False):
    """Restore a single backup file to its original name.

    Args:
        backup_path: Path to .backup file
        dry_run: If True, don't actually restore (just report)
        verbose: If True, print each file being restored

    Returns:
        bool: True if successful, False if error
    """
    original_path = backup_path.with_suffix("")  # Remove .backup extension

    try:
        if dry_run:
            if verbose:
                print(f"  [DRY RUN] Would restore: {original_path.name}")
            return True
        else:
            shutil.copy2(backup_path, original_path)
            if verbose:
                print(f"  [OK] Restored: {original_path.name}")
            return True
    except (IOError, OSError) as e:
        print(f"  [FAIL] Error restoring {original_path.name}: {e}")
        return False


def main():
    """Main entry point."""
    # Parse command-line arguments
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or dry_run  # dry-run implies verbose

    print("[INFO] Rolling back migration...")
    print("")

    # Find all backup files
    backup_files = find_backup_files()
    backup_count = len(backup_files)

    if backup_count == 0:
        print("[FAIL] No backup files found. Cannot rollback.")
        print("")
        print("Expected: Files with .backup extension in template/ directory")
        sys.exit(1)

    print(f"[INFO] Found {backup_count} backup files")

    if dry_run:
        print("[INFO] DRY RUN mode - no changes will be made")

    print("")

    # Restore all backups
    restored_count = 0
    failed_count = 0

    for backup_file in backup_files:
        if restore_backup(backup_file, dry_run=dry_run, verbose=verbose):
            restored_count += 1
        else:
            failed_count += 1

    # Summary
    print("")
    if dry_run:
        print(f"[INFO] Would restore {restored_count} files")
    else:
        print(f"[OK] Rollback complete! Restored {restored_count} files")
        if failed_count > 0:
            print(f"[WARN] Failed to restore {failed_count} files")

    print("")

    if not dry_run and failed_count == 0:
        print("[INFO] To remove backup files, run:")
        print(f"       python -c \"from pathlib import Path; [p.unlink() for p in Path('template').glob('**/*.backup')]\"")
        print("")
        print("Or on Unix/Mac:")
        print("       find template/ -name '*.backup' -delete")
        print("")

    # Exit with appropriate code
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
