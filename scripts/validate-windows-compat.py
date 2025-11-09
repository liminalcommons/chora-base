#!/usr/bin/env python3
"""Validate Windows Compatibility

This script validates Python scripts for Windows compatibility issues:
1. Scripts using emojis without UTF-8 console reconfiguration
2. File I/O operations missing explicit encoding='utf-8'
3. Hardcoded Unix paths in documentation

Usage:
    python scripts/validate-windows-compat.py
    python scripts/validate-windows-compat.py --fix-dry-run
    python scripts/validate-windows-compat.py --scripts-only
    python scripts/validate-windows-compat.py --format json

Exit codes:
    0 - All checks pass
    1 - Validation failures found
    2 - Invalid usage
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VERSION = "1.0.0"

# Emoji patterns to detect
EMOJI_PATTERN = re.compile(r'[✓✗⚠❌✅💡🔍⚡🎯📋🚀🔄ℹ]')

# File open patterns without encoding
FILE_OPEN_PATTERN = re.compile(r'''
    with\s+open\s*\(
    [^)]*?                # anything except closing paren
    (?!encoding\s*=)      # not followed by encoding=
    \)
''', re.VERBOSE)

# UTF-8 reconfiguration pattern
UTF8_RECONFIG_PATTERN = re.compile(r'''
    sys\.(?:stdout|stderr)\.reconfigure\(encoding=['"]utf-8['"]\)
''', re.VERBOSE)


class ValidationResult:
    """Result of a validation check"""
    def __init__(self, file_path: str, issue_type: str, line_num: Optional[int] = None,
                 line_content: Optional[str] = None, severity: str = "medium"):
        self.file_path = file_path
        self.issue_type = issue_type
        self.line_num = line_num
        self.line_content = line_content
        self.severity = severity

    def to_dict(self) -> Dict:
        return {
            "file": self.file_path,
            "issue": self.issue_type,
            "line": self.line_num,
            "content": self.line_content,
            "severity": self.severity
        }


def check_emoji_without_utf8(file_path: Path) -> List[ValidationResult]:
    """Check if Python file uses emojis without UTF-8 reconfiguration"""
    results = []

    try:
        content = file_path.read_text(encoding='utf-8')

        # Check for emojis
        has_emoji = bool(EMOJI_PATTERN.search(content))

        if has_emoji:
            # Check for UTF-8 reconfiguration
            has_utf8_reconfig = bool(UTF8_RECONFIG_PATTERN.search(content))

            if not has_utf8_reconfig:
                # Find line with emoji
                for i, line in enumerate(content.splitlines(), 1):
                    if EMOJI_PATTERN.search(line):
                        results.append(ValidationResult(
                            file_path=str(file_path),
                            issue_type="emoji_without_utf8_reconfiguration",
                            line_num=i,
                            line_content=line.strip()[:80],
                            severity="critical"
                        ))
                        break  # Report first occurrence only

    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}", file=sys.stderr)

    return results


def check_file_open_encoding(file_path: Path) -> List[ValidationResult]:
    """Check if file has open() calls without encoding parameter"""
    results = []

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Simple heuristic: check for 'with open(' without 'encoding='
            if 'with open(' in line or 'open(' in line:
                # Check if this line or next few lines have encoding=
                context = '\n'.join(lines[max(0, i-1):min(len(lines), i+2)])

                if 'with open(' in line and 'encoding=' not in context:
                    # Skip binary mode opens
                    if "'rb'" in context or '"rb"' in context or "'wb'" in context or '"wb"' in context:
                        continue

                    results.append(ValidationResult(
                        file_path=str(file_path),
                        issue_type="file_open_missing_encoding",
                        line_num=i,
                        line_content=line.strip()[:80],
                        severity="high"
                    ))

    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}", file=sys.stderr)

    return results


def check_hardcoded_unix_paths(file_path: Path) -> List[ValidationResult]:
    """Check for hardcoded Unix paths in documentation"""
    results = []

    # Only check documentation files
    if not (file_path.suffix == '.md' or file_path.suffix == '.rst'):
        return results

    try:
        content = file_path.read_text(encoding='utf-8')

        # Patterns for Unix-only path examples
        unix_path_patterns = [
            (r'~/[a-zA-Z0-9_/-]+', 'tilde_home_path'),
            (r'/usr/local/[a-zA-Z0-9_/-]+', 'absolute_unix_path'),
            (r'/home/[a-zA-Z0-9_/-]+', 'home_directory_path'),
        ]

        for i, line in enumerate(content.splitlines(), 1):
            # Skip code blocks and inline code
            if line.strip().startswith('```') or line.strip().startswith('#'):
                continue

            for pattern, issue_name in unix_path_patterns:
                if re.search(pattern, line):
                    results.append(ValidationResult(
                        file_path=str(file_path),
                        issue_type=f"hardcoded_unix_path_{issue_name}",
                        line_num=i,
                        line_content=line.strip()[:80],
                        severity="medium"
                    ))
                    break  # One issue per line

    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}", file=sys.stderr)

    return results


def find_python_files(root_dir: Path, exclude_dirs: List[str] = None) -> List[Path]:
    """Find all Python files in directory"""
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv', 'build', 'dist']

    python_files = []
    for py_file in root_dir.rglob('*.py'):
        # Exclude directories
        if any(excluded in str(py_file) for excluded in exclude_dirs):
            continue
        python_files.append(py_file)

    return python_files


def find_markdown_files(root_dir: Path, exclude_dirs: List[str] = None) -> List[Path]:
    """Find all Markdown files in directory"""
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv']

    md_files = []
    for md_file in root_dir.rglob('*.md'):
        # Exclude directories
        if any(excluded in str(md_file) for excluded in exclude_dirs):
            continue
        md_files.append(md_file)

    return md_files


def print_results(results: List[ValidationResult], format_type: str = "text"):
    """Print validation results"""
    if format_type == "json":
        print(json.dumps([r.to_dict() for r in results], indent=2))
        return

    # Group by severity
    critical = [r for r in results if r.severity == "critical"]
    high = [r for r in results if r.severity == "high"]
    medium = [r for r in results if r.severity == "medium"]

    if critical:
        print("\n🔴 CRITICAL ISSUES")
        print("=" * 80)
        for result in critical:
            print(f"  File: {result.file_path}:{result.line_num}")
            print(f"  Issue: {result.issue_type}")
            print(f"  Line: {result.line_content}")
            print()

    if high:
        print("\n🟡 HIGH PRIORITY ISSUES")
        print("=" * 80)
        for result in high:
            print(f"  File: {result.file_path}:{result.line_num}")
            print(f"  Issue: {result.issue_type}")
            print(f"  Line: {result.line_content}")
            print()

    if medium:
        print("\n🟢 MEDIUM PRIORITY ISSUES")
        print("=" * 80)
        count_by_file = {}
        for result in medium:
            count_by_file[result.file_path] = count_by_file.get(result.file_path, 0) + 1

        for file_path, count in count_by_file.items():
            print(f"  {file_path}: {count} issue(s)")


def main():
    parser = argparse.ArgumentParser(description="Validate Windows compatibility")
    parser.add_argument('--scripts-only', action='store_true',
                       help='Only check scripts/ directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format')
    parser.add_argument('--fix-dry-run', action='store_true',
                       help='Show what would be fixed (not implemented yet)')

    args = parser.parse_args()

    # Find files to check
    root_dir = Path.cwd()

    print(f"🔍 Validating Windows compatibility...")
    print(f"   Root: {root_dir}")
    print()

    # Check Python files
    if args.scripts_only:
        python_files = find_python_files(root_dir / 'scripts')
    else:
        python_files = find_python_files(root_dir)

    print(f"   Found {len(python_files)} Python files")

    all_results = []

    # Check 1: Emojis without UTF-8 reconfiguration
    print("   Checking for emojis without UTF-8 reconfiguration...")
    for py_file in python_files:
        all_results.extend(check_emoji_without_utf8(py_file))

    # Check 2: File open without encoding
    print("   Checking for file open() without encoding parameter...")
    for py_file in python_files:
        all_results.extend(check_file_open_encoding(py_file))

    # Check 3: Hardcoded Unix paths (if checking all files)
    if not args.scripts_only:
        md_files = find_markdown_files(root_dir)
        print(f"   Found {len(md_files)} Markdown files")
        print("   Checking for hardcoded Unix paths in documentation...")
        for md_file in md_files:
            all_results.extend(check_hardcoded_unix_paths(md_file))

    # Print results
    print()
    print("=" * 80)
    print(f"VALIDATION COMPLETE")
    print("=" * 80)

    if not all_results:
        print("✅ No Windows compatibility issues found!")
        return 0

    print(f"❌ Found {len(all_results)} issue(s)")
    print_results(all_results, format_type=args.format)

    # Summary
    critical = len([r for r in all_results if r.severity == "critical"])
    high = len([r for r in all_results if r.severity == "high"])
    medium = len([r for r in all_results if r.severity == "medium"])

    print("\n" + "=" * 80)
    print(f"SUMMARY: {critical} critical, {high} high, {medium} medium priority issues")
    print("=" * 80)

    if critical > 0:
        print("\n⚠️  Critical issues must be fixed for Windows compatibility!")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
