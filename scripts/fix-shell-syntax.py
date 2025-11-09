#!/usr/bin/env python3
"""Fix shell syntax incorrectly converted by delimiter migration (Jinja2 → shell).

This script restores shell constructs that got converted to Jinja2 syntax during
template delimiter migration. It processes .jinja files and applies regex-based
substitutions.

Usage:
    python scripts/fix-shell-syntax.py
    python scripts/fix-shell-syntax.py --dry-run  # Preview without changes
    python scripts/fix-shell-syntax.py --verbose  # Show each file processed

Part of SAP-008: Cross-Platform Automation Scripts
"""

import re
import sys
from pathlib import Path


def fix_heredocs(content):
    """Fix heredoc syntax: {{EOF → <<EOF, {{'EOF' → <<'EOF'.

    Args:
        content: File content to process

    Returns:
        str: Content with heredoc syntax fixed
    """
    # Fix {{EOF → <<EOF
    content = content.replace("{{EOF", "<<EOF")

    # Fix {{'EOF' → <<'EOF'
    content = content.replace("{{'EOF'", "<<'EOF'")

    # Fix }}'EOF' → <<'EOF' (closing delimiter)
    content = content.replace("}}'EOF'", "<<'EOF'")

    return content


def fix_test_expressions(content):
    """Fix shell test expressions: if {{ condition }} → if [[ condition ]].

    Args:
        content: File content to process

    Returns:
        str: Content with test expressions fixed
    """
    # Fix: if {{ → if [[
    content = re.sub(r'if \{\{ ', 'if [[ ', content)

    # Fix: }}; then → ]]; then
    content = re.sub(r' \}\}; then', ' ]]; then', content)

    return content


def fix_while_loops(content):
    """Fix while loops: while {{ condition }} → while [[ condition ]].

    Args:
        content: File content to process

    Returns:
        str: Content with while loops fixed
    """
    # Fix: while {{ → while [[
    content = re.sub(r'while \{\{ ', 'while [[ ', content)

    # Fix: }}; do → ]]; do
    content = re.sub(r' \}\}; do', ' ]]; do', content)

    return content


def fix_array_access(content):
    """Fix array access: ${VAR{{0}}} → ${VAR[0]}.

    Only applies to .sh.jinja files where array syntax is common.
    Pattern: ${UPPERCASE_VAR{{digit}}} → ${UPPERCASE_VAR[digit]}

    Args:
        content: File content to process

    Returns:
        str: Content with array access fixed
    """
    # Fix: ${UPPERCASE{{0}}} → ${UPPERCASE[0]}
    # Pattern: Variable name is uppercase with underscores, index is digits
    content = re.sub(
        r'\$\{([A-Z_]+)\{\{(\d+)\}\}\}',
        r'${\1[\2]}',
        content
    )

    return content


def process_file(file_path, dry_run=False, verbose=False, is_shell_script=False):
    """Process a single file and apply all fixes.

    Args:
        file_path: Path to file to process
        dry_run: If True, don't write changes (just report)
        verbose: If True, print each file being processed
        is_shell_script: If True, apply array access fixes (for .sh.jinja files)

    Returns:
        dict with keys: file_path, changed, changes_count
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except (IOError, UnicodeDecodeError) as e:
        if verbose:
            print(f"  [FAIL] Error reading {file_path.name}: {e}")
        return {
            "file_path": str(file_path),
            "changed": False,
            "error": str(e)
        }

    original_content = content

    # Apply fixes
    content = fix_heredocs(content)
    content = fix_test_expressions(content)
    content = fix_while_loops(content)

    # Array access fix only for shell scripts
    if is_shell_script:
        content = fix_array_access(content)

    # Check if content changed
    changed = (content != original_content)

    if changed:
        if dry_run:
            if verbose:
                print(f"  [DRY RUN] Would fix: {file_path.name}")
        else:
            # Write changes
            try:
                file_path.write_text(content, encoding='utf-8')
                if verbose:
                    print(f"  [OK] Fixed: {file_path.name}")
            except (IOError, UnicodeDecodeError) as e:
                if verbose:
                    print(f"  [FAIL] Error writing {file_path.name}: {e}")
                return {
                    "file_path": str(file_path),
                    "changed": False,
                    "error": str(e)
                }
    else:
        if verbose:
            print(f"  [SKIP] No changes: {file_path.name}")

    return {
        "file_path": str(file_path),
        "changed": changed
    }


def find_jinja_files(base_dir="template"):
    """Find all .jinja files in the template directory.

    Args:
        base_dir: Base directory to search (default: template/)

    Returns:
        tuple: (all_jinja_files, shell_script_files)
            all_jinja_files: List of all .jinja files
            shell_script_files: List of .sh.jinja files only
    """
    base_path = Path(base_dir)

    if not base_path.exists():
        return [], []

    # Find all .jinja files
    all_jinja_files = sorted(base_path.glob("**/*.jinja"))

    # Find .sh.jinja files (shell scripts)
    shell_script_files = sorted(base_path.glob("scripts/**/*.sh.jinja"))

    return all_jinja_files, shell_script_files


def main():
    """Main entry point."""
    # Parse command-line arguments
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or dry_run  # dry-run implies verbose

    print("[INFO] Fixing shell syntax in template files...")
    print("")

    # Find all files to process
    all_jinja_files, shell_script_files = find_jinja_files()
    shell_script_paths = set(shell_script_files)  # For fast lookup

    if not all_jinja_files:
        print("[FAIL] No .jinja files found in template/ directory")
        print("")
        print("Expected: Files with .jinja extension in template/")
        sys.exit(1)

    print(f"[INFO] Found {len(all_jinja_files)} .jinja files")
    print(f"[INFO] Found {len(shell_script_files)} .sh.jinja files (will apply array fixes)")

    if dry_run:
        print("[INFO] DRY RUN mode - no changes will be made")

    print("")

    # Process all files
    changed_count = 0
    error_count = 0

    for jinja_file in all_jinja_files:
        is_shell_script = jinja_file in shell_script_paths

        result = process_file(
            jinja_file,
            dry_run=dry_run,
            verbose=verbose,
            is_shell_script=is_shell_script
        )

        if result.get("changed"):
            changed_count += 1

        if "error" in result:
            error_count += 1

    # Summary
    print("")
    if dry_run:
        print(f"[INFO] Would fix {changed_count} files")
    else:
        print(f"[OK] Fixed {changed_count} files")
        if error_count > 0:
            print(f"[WARN] Failed to process {error_count} files")

    print("")

    if not dry_run and changed_count > 0:
        print("[INFO] To verify changes, run:")
        print("       git diff template/")
        print("")

    # Exit with appropriate code
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
