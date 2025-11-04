#!/usr/bin/env python3
"""Create GitHub release from CHANGELOG.

Extracts version notes from CHANGELOG.md and creates GitHub release using gh CLI.
Part of GAP-003: Unified Release Workflow implementation.

Usage:
    python scripts/create-release.py
    python scripts/create-release.py --version 4.4.0
    python scripts/create-release.py --dry-run
    python scripts/create-release.py --help

Exit Codes:
    0 - Success
    1 - File operation or gh CLI error
    2 - Invalid arguments or missing git tag

Examples:
    # Create release for current git tag
    python scripts/create-release.py

    # Create release for specific version
    python scripts/create-release.py --version 4.4.0

    # Preview release creation
    python scripts/create-release.py --dry-run

    # Using Just task runner
    just release
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_current_git_tag() -> str:
    """Get current git tag (exact match for HEAD).

    Returns:
        Tag name without 'v' prefix, or empty string if no tag
    """
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--exact-match'],
            capture_output=True,
            text=True,
            check=True
        )
        # Strip 'v' prefix and whitespace
        return result.stdout.strip().lstrip('v')
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        print("[FAIL] git command not found. Ensure git is installed and in PATH.")
        return ""


def extract_changelog_section(version: str) -> str:
    """Extract section for specific version from CHANGELOG.md.

    Args:
        version: Version to extract (without 'v' prefix)

    Returns:
        Changelog content for version, or empty string if not found
    """
    changelog_path = Path("CHANGELOG.md")

    if not changelog_path.exists():
        print("[WARN] CHANGELOG.md not found")
        return ""

    try:
        content = changelog_path.read_text(encoding='utf-8')
    except (IOError, OSError) as e:
        print(f"[WARN] Error reading CHANGELOG.md: {e}")
        return ""

    # Pattern: ## [version] - date ... content ... ## [next-version]
    # Using re.DOTALL to match across newlines
    pattern = rf'## \[{re.escape(version)}\].*?\n(.*?)(?:\n## \[|\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        # Clean up the extracted content
        notes = match.group(1).strip()
        # Remove trailing --- separators
        notes = re.sub(r'\n---+\s*$', '', notes)
        return notes

    return ""


def check_gh_cli() -> bool:
    """Check if gh CLI is installed and authenticated.

    Returns:
        True if gh CLI is ready to use, False otherwise
    """
    try:
        # Check if gh is installed
        subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            check=True
        )

        # Check if authenticated
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("[FAIL] gh CLI not authenticated")
            print("  Run: gh auth login")
            return False

        return True

    except subprocess.CalledProcessError:
        print("[FAIL] gh CLI found but not working properly")
        return False
    except FileNotFoundError:
        print("[FAIL] gh CLI not found")
        print("  Install:")
        print("    Mac:     brew install gh")
        print("    Windows: winget install GitHub.cli")
        print("    Linux:   sudo apt install gh")
        return False


def create_github_release(version: str, notes: str, dry_run: bool = False) -> bool:
    """Create GitHub release using gh CLI.

    Args:
        version: Version for release (without 'v' prefix)
        notes: Release notes content
        dry_run: If True, preview without creating release

    Returns:
        True if successful, False otherwise
    """
    tag_name = f"v{version}"
    title = f"Release v{version}"

    if dry_run:
        print(f"[DRY RUN] Would create GitHub release:")
        print(f"  Tag: {tag_name}")
        print(f"  Title: {title}")
        print(f"  Notes:\n{'-' * 60}")
        # Use safe encoding for console output (handle Unicode gracefully)
        display_notes = notes if notes else "(No release notes from CHANGELOG)"
        try:
            print(display_notes)
        except UnicodeEncodeError:
            # Fallback: encode with 'replace' to show placeholder for unsupported chars
            print(display_notes.encode('ascii', 'replace').decode('ascii'))
        print('-' * 60)
        return True

    # Write notes to temporary file
    notes_file = Path('.release-notes.tmp')
    try:
        notes_file.write_text(notes or f"Release {version}", encoding='utf-8')

        # Create release
        subprocess.run([
            'gh', 'release', 'create', tag_name,
            '--title', title,
            '--notes-file', str(notes_file)
        ], check=True)

        print(f"[OK] Created GitHub release: {tag_name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to create GitHub release: {e}")
        return False
    finally:
        # Clean up temporary file
        if notes_file.exists():
            notes_file.unlink()


def create_release(version: str = None, dry_run: bool = False) -> int:
    """Main function to create GitHub release.

    Args:
        version: Version to release (auto-detected from git tag if None)
        dry_run: If True, preview without creating release

    Returns:
        Exit code (0 = success, 1 = error, 2 = invalid input)
    """
    # Auto-detect version from git tag if not provided
    if not version:
        print("Detecting version from current git tag...")
        version = get_current_git_tag()

        if not version:
            print("[FAIL] No git tag found for current commit")
            print("  Run: just bump <version>")
            print("  Or: python scripts/bump-version.py <version>")
            return 2

        print(f"[OK] Detected version: {version}")
    else:
        # Validate version format (basic check)
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            print(f"[FAIL] Invalid version format: {version}")
            print("Expected: X.Y.Z (e.g., 4.4.0)")
            return 2

    if dry_run:
        print("[DRY RUN MODE] No release will be created\n")
    else:
        # Check gh CLI availability
        if not check_gh_cli():
            return 1

    # Extract release notes from CHANGELOG
    print(f"Extracting release notes from CHANGELOG.md for version {version}...")
    notes = extract_changelog_section(version)

    if not notes:
        print(f"[WARN] No CHANGELOG entry found for version {version}")
        print("  Release will be created with default message")
    else:
        print(f"[OK] Found {len(notes)} characters of release notes")

    # Create GitHub release
    if not create_github_release(version, notes, dry_run):
        return 1

    if not dry_run:
        print("\n" + "=" * 70)
        print("GitHub release created successfully!")
        print("=" * 70)
        print(f"View at: https://github.com/liminalcommons/chora-base/releases/tag/v{version}")
        print("=" * 70)

    return 0


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Create GitHub release from CHANGELOG',
        epilog='Part of GAP-003: Unified Release Workflow. Requires gh CLI.'
    )
    parser.add_argument(
        '--version',
        help='Version to release (auto-detected from git tag if not provided)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview release creation without actually creating it'
    )

    args = parser.parse_args()

    exit_code = create_release(args.version, args.dry_run)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
