#!/usr/bin/env python3
"""merge-upstream-structure.py - Merge structural updates from chora-base upstream

Purpose: Safely merge structure-only files from chora-base upstream while preserving project content
Usage: python scripts/merge-upstream-structure.py [--dry-run] [--no-backup]

This script:
1. Reads .chorabase metadata to identify structure-only files
2. Fetches latest from upstream chora-base
3. Merges structure-only files using git checkout
4. Identifies hybrid files requiring manual merge
5. Creates backup and provides rollback mechanism

Exit codes:
  0 - Success
  1 - Error (configuration, git operation, etc.)
  2 - Invalid usage
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Set, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install PyYAML")
    sys.exit(1)

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class MergeStats:
    """Track merge statistics"""
    def __init__(self):
        self.structure_files_merged = 0
        self.hybrid_files_found = 0
        self.errors = 0

stats = MergeStats()

#############################################################################
# Helper Functions
#############################################################################

def print_header(text: str) -> None:
    """Print section header"""
    print(f"{Colors.BLUE}======================================={Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}======================================={Colors.NC}")
    print()

def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.NC} {text}")

def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {text}")

def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.NC} {text}")

def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.NC} {text}")

def run_command(cmd: List[str], check: bool = True, capture: bool = True) -> Tuple[int, str, str]:
    """Run shell command and return (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e.returncode, e.stdout or "", e.stderr or ""

#############################################################################
# Validation Functions
#############################################################################

def check_prerequisites(chorabase_file: str) -> dict:
    """Check prerequisites and load .chorabase metadata"""
    print_header("Checking Prerequisites")

    # Check if in git repository
    returncode, _, _ = run_command(["git", "rev-parse", "--is-inside-work-tree"], check=False)
    if returncode != 0:
        print_error("Not in a git repository")
        sys.exit(1)
    print_success("Git repository detected")

    # Check if .chorabase exists
    if not os.path.exists(chorabase_file):
        print_error(f".chorabase file not found: {chorabase_file}")
        print_info("Expected: .chorabase in repository root")
        sys.exit(1)
    print_success(".chorabase metadata found")

    # Load .chorabase metadata
    try:
        with open(chorabase_file, 'r') as f:
            config = yaml.safe_load(f)
        print_success("Successfully parsed .chorabase metadata")
    except Exception as e:
        print_error(f"Failed to parse .chorabase: {e}")
        sys.exit(1)

    print()
    return config

def check_upstream_remote(config: dict, dry_run: bool) -> None:
    """Check if upstream remote exists, add if needed"""
    print_header("Checking Upstream Remote")

    upstream_remote = config.get('merge', {}).get('upstream_remote', 'chora-base')
    upstream_url = config.get('merge', {}).get('upstream_url')

    if not upstream_url:
        print_error("No upstream_url found in .chorabase")
        sys.exit(1)

    # Check if remote exists
    returncode, _, _ = run_command(
        ["git", "remote", "get-url", upstream_remote],
        check=False
    )

    if returncode != 0:
        print_warning(f"Upstream remote '{upstream_remote}' not found")
        print_info("Adding upstream remote...")

        if not dry_run:
            run_command(["git", "remote", "add", upstream_remote, upstream_url])
            print_success(f"Added upstream remote: {upstream_url}")
        else:
            print_info(f"[DRY RUN] Would add remote: {upstream_url}")
    else:
        _, current_url, _ = run_command(["git", "remote", "get-url", upstream_remote])
        print_success(f"Upstream remote found: {current_url.strip()}")

    print()

def fetch_upstream(config: dict, dry_run: bool) -> None:
    """Fetch latest changes from upstream"""
    print_header("Fetching Upstream Changes")

    upstream_remote = config.get('merge', {}).get('upstream_remote', 'chora-base')
    upstream_branch = config.get('merge', {}).get('upstream_branch', 'main')

    if not dry_run:
        print_info(f"Fetching from {upstream_remote}...")
        try:
            run_command(["git", "fetch", upstream_remote, upstream_branch])
            print_success(f"Fetched latest from {upstream_remote}/{upstream_branch}")
        except subprocess.CalledProcessError:
            print_error("Failed to fetch from upstream")
            sys.exit(1)
    else:
        print_info(f"[DRY RUN] Would fetch from {upstream_remote}/{upstream_branch}")

    print()

#############################################################################
# Backup Functions
#############################################################################

def create_backup(config: dict, no_backup: bool, dry_run: bool) -> str:
    """Create backup of current state"""
    if no_backup:
        print_info("Skipping backup (--no-backup specified)")
        print()
        return ""

    print_header("Creating Backup")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = f".chora-backup-{timestamp}"

    if not dry_run:
        os.makedirs(backup_dir, exist_ok=True)

        # Save current commit
        _, current_commit, _ = run_command(["git", "rev-parse", "HEAD"])
        current_commit = current_commit.strip()
        with open(f"{backup_dir}/commit.txt", 'w') as f:
            f.write(current_commit)

        # Save current branch
        _, current_branch, _ = run_command(["git", "branch", "--show-current"])
        current_branch = current_branch.strip()
        with open(f"{backup_dir}/branch.txt", 'w') as f:
            f.write(current_branch)

        print_success(f"Backup created: {backup_dir}")
        print_info(f"Current commit: {current_commit}")
        print_info(f"Current branch: {current_branch}")
    else:
        print_info(f"[DRY RUN] Would create backup: {backup_dir}")

    print()
    return backup_dir

#############################################################################
# Merge Functions
#############################################################################

def expand_glob_pattern(pattern: str, upstream_ref: str) -> List[str]:
    """Expand glob pattern from upstream git tree"""
    # Check if pattern contains glob characters
    if '*' in pattern or '?' in pattern:
        # Use git ls-tree to expand pattern from upstream
        returncode, stdout, _ = run_command(
            ["git", "ls-tree", "-r", "--name-only", upstream_ref, pattern],
            check=False
        )
        if returncode == 0:
            return [line.strip() for line in stdout.split('\n') if line.strip()]
        return []
    else:
        # Plain file path
        return [pattern]

def file_exists_in_upstream(file: str, upstream_ref: str) -> bool:
    """Check if file exists in upstream"""
    returncode, _, _ = run_command(
        ["git", "cat-file", "-e", f"{upstream_ref}:{file}"],
        check=False
    )
    return returncode == 0

def merge_structure_files(config: dict, dry_run: bool) -> None:
    """Merge structure-only files from upstream"""
    print_header("Merging Structure-Only Files")

    structure_files = config.get('structure_only', [])
    if not structure_files:
        print_warning("No structure_only files found in .chorabase")
        print()
        return

    upstream_remote = config.get('merge', {}).get('upstream_remote', 'chora-base')
    upstream_branch = config.get('merge', {}).get('upstream_branch', 'main')
    upstream_ref = f"{upstream_remote}/{upstream_branch}"

    print_success(f"Found {len(structure_files)} structure-only file patterns")
    print()

    # Process each structure file pattern
    for pattern in structure_files:
        if not pattern or pattern.startswith('#'):
            continue

        # Expand glob patterns
        files_to_merge = expand_glob_pattern(pattern, upstream_ref)

        if not files_to_merge:
            print_warning(f"No files match pattern: {pattern}")
            continue

        # Merge each file
        for file in files_to_merge:
            if not file:
                continue

            # Check if file exists in upstream
            if not file_exists_in_upstream(file, upstream_ref):
                print_warning(f"File not in upstream: {file}")
                continue

            if not dry_run:
                # Merge file from upstream
                try:
                    run_command(["git", "checkout", upstream_ref, "--", file])
                    print_success(f"Merged: {file}")
                    stats.structure_files_merged += 1
                except subprocess.CalledProcessError:
                    print_error(f"Failed to merge: {file}")
                    stats.errors += 1
            else:
                print_info(f"[DRY RUN] Would merge: {file}")
                stats.structure_files_merged += 1

    print()

#############################################################################
# Hybrid File Detection
#############################################################################

def detect_hybrid_files(config: dict) -> None:
    """Detect and report hybrid files requiring manual merge"""
    print_header("Detecting Hybrid Files")

    hybrid_files = config.get('hybrid', {})
    if not hybrid_files:
        print_info("No hybrid files defined in .chorabase")
        print()
        return

    print_warning("The following files require manual merge:")
    print()

    for file, file_config in hybrid_files.items():
        merge_strategy = file_config.get('merge_strategy', 'manual')
        print_info(f"  {file} (strategy: {merge_strategy})")
        stats.hybrid_files_found += 1

    print()
    print_info("Hybrid files were NOT automatically merged")
    print_info("Use specialized merge tools in scripts/ directory:")
    print()
    print_info("  ./scripts/merge-agents-md.py      # For AGENTS.md")
    print_info("  ./scripts/merge-readme-md.py      # For README.md")
    print_info("  ./scripts/merge-index-md.py       # For INDEX.md")
    print()

#############################################################################
# Validation
#############################################################################

def run_validation(config: dict, dry_run: bool) -> None:
    """Run validation commands if configured"""
    print_header("Running Validation")

    validate = config.get('merge', {}).get('validate_after_merge', False)
    if not validate:
        print_info("Validation disabled in .chorabase")
        print()
        return

    if dry_run:
        print_info("[DRY RUN] Would run validation commands")
        print()
        return

    validation_commands = config.get('merge', {}).get('validation_commands', [])
    if not validation_commands:
        print_info("No validation commands defined")
        print()
        return

    print_info("Running validation commands...")
    print()

    validation_failed = False

    for cmd in validation_commands:
        if not cmd:
            continue

        print_info(f"Running: {cmd}")

        returncode = subprocess.call(cmd, shell=True)
        if returncode == 0:
            print_success("Passed")
        else:
            print_error(f"Failed: {cmd}")
            validation_failed = True
        print()

    if validation_failed:
        print_warning("Some validation checks failed")
        print_info("Review errors above and fix before committing")
        print()
    else:
        print_success("All validation checks passed")
        print()

#############################################################################
# Summary
#############################################################################

def print_summary(backup_dir: str, dry_run: bool) -> None:
    """Print merge summary"""
    print_header("Merge Summary")

    print(f"{Colors.GREEN}Structure files merged:{Colors.NC} {stats.structure_files_merged}")
    print(f"{Colors.YELLOW}Hybrid files requiring manual merge:{Colors.NC} {stats.hybrid_files_found}")
    print(f"{Colors.RED}Errors:{Colors.NC} {stats.errors}")
    print()

    if dry_run:
        print_info("DRY RUN - No changes were made")
        print()
        print_info("To apply changes, run without --dry-run:")
        print_info("  python scripts/merge-upstream-structure.py")
        print()
    else:
        if backup_dir:
            print_info(f"Backup created: {backup_dir}")
            print()
            print_info("To rollback, run:")
            print_info(f"  git reset --hard $(cat {backup_dir}/commit.txt)")
            print()

        if stats.structure_files_merged > 0:
            print_info("Next steps:")
            print_info("  1. Review merged changes: git status")
            print_info("  2. Handle hybrid files (see above)")
            print_info("  3. Run tests: just test")
            print_info("  4. Commit changes: git add . && git commit -m 'chore: Merge structural updates from upstream'")
            print()

    if stats.errors > 0:
        print_warning("Merge completed with errors - review above")
        sys.exit(1)

#############################################################################
# Main
#############################################################################

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Merge structural updates from chora-base upstream while preserving project content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what would be merged
  python scripts/merge-upstream-structure.py --dry-run

  # Merge structural updates
  python scripts/merge-upstream-structure.py

  # Merge without backup (not recommended)
  python scripts/merge-upstream-structure.py --no-backup

More Info:
  See: docs/user-docs/how-to/upgrade-structure-from-upstream.md
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be merged without making changes'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup before merge'
    )
    parser.add_argument(
        '--chorabase',
        default='.chorabase',
        help='Path to .chorabase metadata file (default: .chorabase)'
    )

    args = parser.parse_args()

    print_header("Merge Upstream Structure")

    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
        print()

    # Run merge workflow
    config = check_prerequisites(args.chorabase)
    check_upstream_remote(config, args.dry_run)
    fetch_upstream(config, args.dry_run)
    backup_dir = create_backup(config, args.no_backup, args.dry_run)
    merge_structure_files(config, args.dry_run)
    detect_hybrid_files(config)
    run_validation(config, args.dry_run)
    print_summary(backup_dir, args.dry_run)

    print_success("Merge workflow completed successfully")

if __name__ == '__main__':
    main()
