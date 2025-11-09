#!/usr/bin/env python3
"""
SAP-007 Documentation Framework - Structure Validation Script

Purpose:
    Validates that a project's documentation structure complies with SAP-007
    (Documentation Framework) requirements.

Validation Checks:
    1. Root directory file count (default: ≤8 markdown files)
    2. Required project-docs/ subdirectories exist
    3. No orphaned documentation in project-docs/ root

Usage:
    python validate-sap-007-structure.py [--repo-root /path/to/repo]

Exit Codes:
    0 = All validation checks passed (SAP-007 compliant)
    1 = One or more validation checks failed (non-compliant)

Configuration:
    Customize ALLOWED_ROOT_FILES and REQUIRED_PROJECT_DOCS_SUBDIRS below
    to match your project's specific needs.

Windows Compatibility Note:
---------------------------
Windows console (cmd.exe, PowerShell) has limited unicode support.
To ensure cross-platform compatibility, this script uses:
- "[PASS]" instead of "✅"
- "[FAIL]" instead of "❌"
- "[INFO]" instead of "ℹ️"
- "<=" instead of "≤"
- ">=" instead of "≥"

This ensures validation output displays correctly on all platforms.

SAP-031 Integration:
--------------------
This validation script implements SAP-031 (Discoverability-Based Enforcement)
Layer 2 (Pre-Commit Validation) for SAP-007 (Documentation Framework).

See: docs/skilled-awareness/discoverability-based-enforcement/
"""

import sys
from pathlib import Path
from typing import List, Tuple

# =============================================================================
# CONFIGURATION - Customize for your project
# =============================================================================

# Root directory allowed files (SAP-007 guideline: ≤8 for navigability)
ALLOWED_ROOT_FILES = [
    "README.md",              # Project overview (required)
    "AGENTS.md",              # Agent awareness (SAP-009)
    "CLAUDE.md",              # Claude-specific workflows (SAP-009)
    "CHANGELOG.md",           # Version history
    "CONTRIBUTING.md",        # Contribution guidelines
    "LICENSE.md",             # License file
    "DOCUMENTATION_STANDARD.md",  # Doc writing standards (SAP-007)
    "ROADMAP.md",             # Strategic vision (optional)
    # Add project-specific exceptions below (document rationale in AGENTS.md)
]

# Required subdirectories under project-docs/
# Customize based on your project's needs
REQUIRED_PROJECT_DOCS_SUBDIRS = [
    "sprints",
    "releases",
    "metrics",
    "decisions",
    "retrospectives",
]

# Standard files that should exist (informational warnings only, not errors)
STANDARD_ROOT_FILES = [
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
]

# =============================================================================
# VALIDATION LOGIC - Don't modify unless customizing validation behavior
# =============================================================================

def get_repo_root() -> Path:
    """
    Get repository root directory.

    Returns:
        Path to repository root (current directory or --repo-root argument)
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--repo-root":
        return Path(sys.argv[2]).resolve()
    return Path.cwd()


def validate_root_directory(repo_root: Path) -> Tuple[bool, List[str]]:
    """
    Validate root directory file count.

    Args:
        repo_root: Path to repository root

    Returns:
        Tuple of (passed: bool, messages: List[str])
    """
    messages = []

    # Count markdown files in root directory
    root_md_files = list(repo_root.glob("*.md"))
    root_md_count = len(root_md_files)
    allowed_count = len(ALLOWED_ROOT_FILES)

    # Check against allowed count
    if root_md_count <= allowed_count:
        messages.append(f"   [PASS] Root has {root_md_count} markdown file(s) (within policy)")
        passed = True
    else:
        messages.append(f"   [FAIL] Root has {root_md_count} markdown file(s), expected <={allowed_count}")
        messages.append(f"")
        messages.append(f"   Allowed root files (customize ALLOWED_ROOT_FILES in script):")
        for allowed_file in ALLOWED_ROOT_FILES:
            messages.append(f"      - {allowed_file}")
        messages.append(f"")
        messages.append(f"   Actual root files:")
        for md_file in sorted(root_md_files):
            allowed_marker = "  [OK]" if md_file.name in ALLOWED_ROOT_FILES else "[VIOLATION]"
            messages.append(f"      {allowed_marker} {md_file.name}")
        messages.append(f"")
        messages.append(f"   Remediation:")
        messages.append(f"      1. Move violating files to user-docs/, dev-docs/, or project-docs/")
        messages.append(f"      2. Use decision tree: docs/skilled-awareness/documentation-framework/decision-tree-template.md")
        messages.append(f"      3. Re-run validation: python {Path(__file__).name}")
        passed = False

    # Informational: Check for missing standard files
    missing_standard = [f for f in STANDARD_ROOT_FILES if not (repo_root / f).exists()]
    if missing_standard:
        messages.append(f"")
        messages.append(f"   [INFO] Missing standard root files (not an error, but recommended):")
        for missing_file in missing_standard:
            messages.append(f"      - {missing_file}")

    return passed, messages


def validate_project_docs_structure(repo_root: Path) -> Tuple[bool, List[str]]:
    """
    Validate project-docs/ subdirectory structure.

    Args:
        repo_root: Path to repository root

    Returns:
        Tuple of (passed: bool, messages: List[str])
    """
    messages = []
    project_docs_dir = repo_root / "project-docs"

    # Check if project-docs/ exists
    if not project_docs_dir.exists():
        messages.append(f"   [INFO] project-docs/ directory does not exist (skipping subdirectory check)")
        return True, messages  # Not an error if project-docs/ doesn't exist

    # Check required subdirectories
    missing_subdirs = []
    for subdir in REQUIRED_PROJECT_DOCS_SUBDIRS:
        if not (project_docs_dir / subdir).exists():
            missing_subdirs.append(subdir)

    if not missing_subdirs:
        messages.append(f"   [PASS] All {len(REQUIRED_PROJECT_DOCS_SUBDIRS)} required subdirectories exist")
        passed = True
    else:
        messages.append(f"   [FAIL] Missing {len(missing_subdirs)} required subdirectories:")
        for subdir in missing_subdirs:
            messages.append(f"      - project-docs/{subdir}/")
        messages.append(f"")
        messages.append(f"   Remediation:")
        messages.append(f"      1. Create missing subdirectories:")
        for subdir in missing_subdirs:
            messages.append(f"         mkdir -p project-docs/{subdir}")
        messages.append(f"      2. Move relevant docs into subdirectories")
        messages.append(f"      3. Re-run validation: python {Path(__file__).name}")
        passed = False

    return passed, messages


def validate_no_orphaned_docs(repo_root: Path) -> Tuple[bool, List[str]]:
    """
    Validate no orphaned documentation in project-docs/ root.

    Args:
        repo_root: Path to repository root

    Returns:
        Tuple of (passed: bool, messages: List[str])
    """
    messages = []
    project_docs_dir = repo_root / "project-docs"

    # Check if project-docs/ exists
    if not project_docs_dir.exists():
        messages.append(f"   [INFO] project-docs/ directory does not exist (skipping orphan check)")
        return True, messages

    # Find markdown files in project-docs/ root (not subdirectories)
    orphaned_docs = [
        f for f in project_docs_dir.glob("*.md")
        if f.name not in ["README.md", "AGENTS.md"]  # These are allowed in root
    ]

    if not orphaned_docs:
        messages.append(f"   [PASS] No orphaned docs in project-docs/ root")
        passed = True
    else:
        messages.append(f"   [FAIL] Found {len(orphaned_docs)} orphaned doc(s) in project-docs/ root:")
        for doc in sorted(orphaned_docs):
            messages.append(f"      - {doc.name}")
        messages.append(f"")
        messages.append(f"   Remediation:")
        messages.append(f"      1. Move orphaned docs into appropriate subdirectories:")
        messages.append(f"         - sprints/ (sprint planning, retrospectives)")
        messages.append(f"         - releases/ (release planning, upgrade guides)")
        messages.append(f"         - metrics/ (process metrics, velocity)")
        messages.append(f"         - decisions/ (ADRs, design decisions)")
        messages.append(f"         - retrospectives/ (project retrospectives)")
        messages.append(f"      2. Use decision tree: docs/skilled-awareness/documentation-framework/decision-tree-template.md")
        messages.append(f"      3. Re-run validation: python {Path(__file__).name}")
        passed = False

    return passed, messages


def main() -> int:
    """
    Main validation entry point.

    Returns:
        Exit code (0=pass, 1=fail)
    """
    # UTF-8 console (cross-platform compatibility)
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    repo_root = get_repo_root()

    print("Validating SAP-007 Documentation Framework compliance...")
    print(f"   Repository: {repo_root}")
    print("")

    all_passed = True

    # Check 1: Root directory files
    print(f"Check 1: Root directory files ({len(ALLOWED_ROOT_FILES)} allowed)...")
    passed, messages = validate_root_directory(repo_root)
    all_passed = all_passed and passed
    for msg in messages:
        print(msg)
    print("")

    # Check 2: project-docs/ subdirectory structure
    print(f"Check 2: project-docs/ subdirectory structure...")
    passed, messages = validate_project_docs_structure(repo_root)
    all_passed = all_passed and passed
    for msg in messages:
        print(msg)
    print("")

    # Check 3: No orphaned docs in project-docs/ root
    print(f"Check 3: Orphaned docs in project-docs/ root...")
    passed, messages = validate_no_orphaned_docs(repo_root)
    all_passed = all_passed and passed
    for msg in messages:
        print(msg)
    print("")

    # Summary
    print("=" * 60)
    if all_passed:
        print("[PASS] SAP-007 validation PASSED")
        print("")
        print("Documentation structure complies with SAP-007 framework:")
        print(f"- Root directory: Clean (<={len(ALLOWED_ROOT_FILES)} files)")
        print("- project-docs/: Properly structured")
        print("- No orphaned docs")
        return 0
    else:
        print("[FAIL] SAP-007 validation FAILED")
        print("")
        print("Please fix violations above and re-run validation.")
        print("")
        print("Resources:")
        print("- SAP-007 Documentation: docs/skilled-awareness/documentation-framework/")
        print("- Decision Tree: docs/skilled-awareness/documentation-framework/decision-tree-template.md")
        print("- Enforcement Guide: docs/skilled-awareness/documentation-framework/adoption-blueprint.md (Level 3)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
