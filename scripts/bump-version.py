#!/usr/bin/env python3
"""Bump version for chora-base repository.

Updates CHANGELOG.md with new version header and creates git tag.
Part of GAP-003: Unified Release Workflow implementation.

Usage:
    python scripts/bump-version.py 4.4.0
    python scripts/bump-version.py 4.4.0 --dry-run
    python scripts/bump-version.py --help

Exit Codes:
    0 - Success
    1 - File operation error
    2 - Invalid arguments or version format

Examples:
    # Bump to version 4.4.0
    python scripts/bump-version.py 4.4.0

    # Preview changes without modifying files
    python scripts/bump-version.py 4.4.0 --dry-run

    # Using Just task runner
    just bump 4.4.0
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


def validate_version(version: str) -> bool:
    """Validate semantic version format (X.Y.Z).

    Args:
        version: Version string to validate

    Returns:
        True if valid semver, False otherwise
    """
    return bool(re.match(r'^\d+\.\d+\.\d+$', version))


def update_changelog(version: str, dry_run: bool = False) -> bool:
    """Update CHANGELOG.md with new version header.

    Args:
        version: Version to add to CHANGELOG
        dry_run: If True, preview changes without modifying file

    Returns:
        True if successful, False otherwise
    """
    changelog_path = Path("CHANGELOG.md")

    if not changelog_path.exists():
        print("[FAIL] CHANGELOG.md not found in repository root")
        return False

    try:
        content = changelog_path.read_text(encoding='utf-8')
    except (IOError, OSError) as e:
        print(f"[FAIL] Error reading CHANGELOG.md: {e}")
        return False

    # Prepare new version header with template
    today = date.today().strftime('%Y-%m-%d')
    new_section = f"""## [{version}] - {today}

### Added
- TODO: List new features

### Changed
- TODO: List changes

### Fixed
- TODO: List bug fixes

---

"""

    # Find insertion point (after first ## [ header)
    lines = content.split('\n')
    insert_index = None

    for i, line in enumerate(lines):
        if line.startswith('## ['):
            insert_index = i
            break

    if insert_index is None:
        print("[FAIL] Could not find version header pattern '## [' in CHANGELOG.md")
        return False

    # Insert new section
    lines.insert(insert_index, new_section.rstrip())
    updated_content = '\n'.join(lines)

    if dry_run:
        print(f"[DRY RUN] Would insert the following into CHANGELOG.md at line {insert_index + 1}:")
        print("---")
        print(new_section)
        print("---")
        return True

    # Write updated CHANGELOG
    try:
        changelog_path.write_text(updated_content, encoding='utf-8')
        print(f"[OK] Updated CHANGELOG.md with version {version}")
        return True
    except (IOError, OSError) as e:
        print(f"[FAIL] Error writing CHANGELOG.md: {e}")
        return False


def create_git_commit_and_tag(version: str, dry_run: bool = False) -> bool:
    """Create git commit and annotated tag for version bump.

    Args:
        version: Version for commit message and tag
        dry_run: If True, preview git operations without executing

    Returns:
        True if successful, False otherwise
    """
    commit_msg = f"chore(release): Bump version to v{version}"
    tag_name = f"v{version}"
    tag_msg = f"Release v{version}"

    if dry_run:
        print(f"[DRY RUN] Would execute:")
        print(f"  git add CHANGELOG.md")
        print(f"  git commit -m '{commit_msg}'")
        print(f"  git tag -a '{tag_name}' -m '{tag_msg}'")
        return True

    try:
        # Stage CHANGELOG
        subprocess.run(['git', 'add', 'CHANGELOG.md'], check=True, capture_output=True)

        # Commit
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] Created git commit: {commit_msg}")

        # Create annotated tag
        subprocess.run(
            ['git', 'tag', '-a', tag_name, '-m', tag_msg],
            check=True,
            capture_output=True
        )
        print(f"[OK] Created git tag: {tag_name}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Git operation failed: {e}")
        if e.stderr:
            print(f"  Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("[FAIL] git command not found. Ensure git is installed and in PATH.")
        return False


def show_next_steps(version: str):
    """Display next steps after version bump.

    Args:
        version: Version that was bumped to
    """
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print(f"1. Edit CHANGELOG.md and replace TODOs with actual changes for v{version}")
    print("2. Amend the commit with your changes:")
    print("     git commit --amend")
    print("3. Push the commit and tag to remote:")
    print("     git push && git push --tags")
    print("4. Create GitHub release:")
    print("     just release")
    print("     # or: python scripts/create-release.py")
    print("=" * 70)


def bump_version(version: str, dry_run: bool = False) -> int:
    """Main function to bump version.

    Args:
        version: Version to bump to (e.g., "4.4.0")
        dry_run: If True, preview changes without modifying anything

    Returns:
        Exit code (0 = success, 1 = error, 2 = invalid input)
    """
    # Validate version format
    if not validate_version(version):
        print(f"[FAIL] Invalid version format: {version}")
        print("Expected: X.Y.Z (e.g., 4.4.0)")
        return 2

    print(f"Bumping chora-base version to {version}...")
    if dry_run:
        print("[DRY RUN MODE] No files will be modified\n")

    # Update CHANGELOG
    if not update_changelog(version, dry_run):
        return 1

    # Create git commit and tag
    if not create_git_commit_and_tag(version, dry_run):
        return 1

    # Show next steps
    if not dry_run:
        show_next_steps(version)
    else:
        print("\n[DRY RUN] All operations completed successfully (preview only)")

    return 0


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Bump version for chora-base repository',
        epilog='Part of GAP-003: Unified Release Workflow'
    )
    parser.add_argument(
        'version',
        help='Version to bump to (semantic version: X.Y.Z, e.g., 4.4.0)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files or creating git commits/tags'
    )

    args = parser.parse_args()

    exit_code = bump_version(args.version, args.dry_run)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
