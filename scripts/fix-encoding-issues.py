#!/usr/bin/env python3
"""Fix File Encoding Issues

This script automatically fixes common file encoding issues in Python files:
1. Adds encoding='utf-8' to open() calls
2. Adds UTF-8 console reconfiguration for scripts using emojis

Usage:
    python scripts/fix-encoding-issues.py --dry-run
    python scripts/fix-encoding-issues.py --apply
    python scripts/fix-encoding-issues.py --file path/to/file.py

Exit codes:
    0 - Success
    1 - Error
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VERSION = "1.0.0"


def add_utf8_reconfiguration(content: str) -> Tuple[str, bool]:
    """Add UTF-8 reconfiguration after imports if emojis are present"""

    # Check if emojis exist
    emoji_pattern = re.compile(r'[✓✗⚠❌✅💡🔍⚡🎯📋🚀🔄ℹ]')
    if not emoji_pattern.search(content):
        return content, False

    # Check if already has UTF-8 reconfiguration
    if 'sys.stdout.reconfigure(encoding=' in content or 'sys.stderr.reconfigure(encoding=' in content:
        # Check if stderr is also configured
        if 'sys.stderr.reconfigure(encoding=' not in content and 'sys.stdout.reconfigure(encoding=' in content:
            # Add stderr reconfiguration
            content = content.replace(
                "sys.stdout.reconfigure(encoding='utf-8')",
                "sys.stdout.reconfigure(encoding='utf-8')\n    sys.stderr.reconfigure(encoding='utf-8')"
            )
            return content, True
        return content, False

    # Find where to insert (after imports, before first function/class)
    lines = content.splitlines(keepends=True)
    insert_index = None

    # Find last import statement
    last_import_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            last_import_index = i

    if last_import_index == -1:
        # No imports, insert at beginning
        insert_index = 0
    else:
        # Insert after imports with a blank line
        insert_index = last_import_index + 1
        # Skip blank lines after imports
        while insert_index < len(lines) and lines[insert_index].strip() == '':
            insert_index += 1

    # Create reconfiguration block
    reconfig_block = [
        "\n",
        "# Configure UTF-8 output for Windows console compatibility\n",
        "if sys.platform == 'win32':\n",
        "    sys.stdout.reconfigure(encoding='utf-8')\n",
        "    sys.stderr.reconfigure(encoding='utf-8')\n",
        "\n"
    ]

    # Insert reconfiguration block
    lines = lines[:insert_index] + reconfig_block + lines[insert_index:]

    return ''.join(lines), True


def fix_file_open_encoding(content: str) -> Tuple[str, int]:
    """Add encoding='utf-8' to open() calls"""

    changes = 0
    lines = content.splitlines(keepends=True)
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for 'with open(' without encoding
        if 'with open(' in line and 'encoding=' not in line:
            # Get context (current line + next line for multi-line opens)
            context = line
            if i + 1 < len(lines):
                context += lines[i + 1]

            # Skip binary mode
            if "'rb'" in context or '"rb"' in context or "'wb'" in context or '"wb"' in context:
                fixed_lines.append(line)
                i += 1
                continue

            # Check if encoding is on next line
            if i + 1 < len(lines) and 'encoding=' in lines[i + 1]:
                fixed_lines.append(line)
                i += 1
                continue

            # Fix the line
            # Pattern 1: with open('file')
            # Pattern 2: with open('file', 'r')
            # Pattern 3: with open(path)
            # Pattern 4: with open(path, 'r')

            if ') as ' in line:
                # Single line open()
                # Find the closing paren before 'as'
                match = re.search(r"(with\s+open\([^)]+)(\)\s+as)", line)
                if match:
                    # Add encoding parameter before closing paren
                    if match.group(1).strip().endswith(','):
                        # Already has comma
                        fixed_line = line.replace(match.group(0),
                                                 match.group(1) + " encoding='utf-8'" + match.group(2))
                    elif match.group(1).count(',') > 0:
                        # Has mode parameter
                        fixed_line = line.replace(match.group(0),
                                                 match.group(1) + ", encoding='utf-8'" + match.group(2))
                    else:
                        # Only file path
                        fixed_line = line.replace(match.group(0),
                                                 match.group(1) + ", encoding='utf-8'" + match.group(2))

                    fixed_lines.append(fixed_line)
                    changes += 1
                    i += 1
                    continue

        fixed_lines.append(line)
        i += 1

    return ''.join(fixed_lines), changes


def process_file(file_path: Path, apply: bool = False) -> dict:
    """Process a single file"""

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Fix 1: Add UTF-8 reconfiguration
        content, added_reconfig = add_utf8_reconfiguration(content)

        # Fix 2: Add encoding to open() calls
        content, encoding_fixes = fix_file_open_encoding(content)

        if content != original_content:
            if apply:
                file_path.write_text(content, encoding='utf-8')
                status = "FIXED"
            else:
                status = "WOULD FIX"

            return {
                "file": str(file_path),
                "status": status,
                "added_reconfig": added_reconfig,
                "encoding_fixes": encoding_fixes
            }
        else:
            return {
                "file": str(file_path),
                "status": "NO CHANGES",
                "added_reconfig": False,
                "encoding_fixes": 0
            }

    except Exception as e:
        return {
            "file": str(file_path),
            "status": "ERROR",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Fix file encoding issues")
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without making changes')
    parser.add_argument('--apply', action='store_true',
                       help='Apply fixes to files')
    parser.add_argument('--file', type=Path,
                       help='Fix a specific file')
    parser.add_argument('--scripts-only', action='store_true',
                       help='Only fix scripts/ directory')

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("❌ Error: Must specify either --dry-run or --apply")
        return 2

    # Find files to process
    if args.file:
        files = [args.file]
    elif args.scripts_only:
        files = list(Path('scripts').rglob('*.py'))
        # Exclude deprecated scripts
        files = [f for f in files if 'deprecated' not in str(f)]
    else:
        files = list(Path('.').rglob('*.py'))
        # Exclude common directories
        files = [f for f in files if not any(excluded in str(f)
                for excluded in ['.git', 'node_modules', '__pycache__', 'venv', '.venv'])]

    print(f"🔍 {'Analyzing' if args.dry_run else 'Fixing'} {len(files)} Python files...")
    print()

    results = []
    for file_path in files:
        result = process_file(file_path, apply=args.apply)
        if result['status'] != 'NO CHANGES':
            results.append(result)

    # Print results
    if not results:
        print("✅ No issues found!")
        return 0

    print(f"{'Would fix' if args.dry_run else 'Fixed'} {len(results)} files:")
    print()

    for result in results:
        if result['status'] == 'ERROR':
            print(f"  ❌ {result['file']}: {result.get('error')}")
        else:
            changes = []
            if result.get('added_reconfig'):
                changes.append("added UTF-8 reconfig")
            if result.get('encoding_fixes'):
                changes.append(f"{result['encoding_fixes']} encoding fixes")

            status_icon = "✅" if args.apply else "🔧"
            print(f"  {status_icon} {result['file']}: {', '.join(changes)}")

    print()
    print(f"Summary: {len(results)} files {'would be updated' if args.dry_run else 'updated'}")

    if args.dry_run:
        print()
        print("Run with --apply to make these changes")

    return 0


if __name__ == '__main__':
    sys.exit(main())
