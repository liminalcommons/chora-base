#!/usr/bin/env python3
"""Nested Awareness Structure Validator (SAP-009 v2.1.0).

Purpose: Validate awareness files against SAP-009 nested structure requirements
Scope: File size, frontmatter, nested files, Critical Workflows section

Usage:
    python scripts/validate-nested-awareness.py <file-or-directory>
    python scripts/validate-nested-awareness.py docs/skilled-awareness/react-form-validation/awareness-guide.md
    python scripts/validate-nested-awareness.py docs/skilled-awareness/
    python scripts/validate-nested-awareness.py --json <file-or-directory>
    python scripts/validate-nested-awareness.py --summary docs/skilled-awareness/

Exit codes:
    0 - All validations pass
    1 - Validation failures found
    2 - Invalid usage

Thresholds (SAP-009 v2.1.0):
    - Warning: 1,000 lines (~5.6k tokens)
    - Critical: 2,000 lines (~11.2k tokens)
    - Token calculation: lines × 5.6 avg tokens/line

Validation Checks:
    1. File size against thresholds
    2. Frontmatter: nested_structure, nested_files fields
    3. Nested files existence and validity
    4. Critical Workflows section (if nested_structure: true)
    5. Token budget within Phase 1 target (<10k)
"""

import json
import re
import sys
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# Configure UTF-8 output for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


# SAP-009 v2.1.0 thresholds
THRESHOLD_WARNING = 1000  # lines
THRESHOLD_CRITICAL = 2000  # lines
AVG_TOKENS_PER_LINE = 5.6
PHASE_1_TOKEN_TARGET = 10000  # tokens


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    status: str  # PASS, WARN, FAIL
    message: str
    details: Optional[Dict] = None


@dataclass
class FileValidation:
    """Complete validation results for a file."""
    file_path: str
    line_count: int
    token_estimate: int
    status: str  # PASS, WARN, FAIL
    checks: List[ValidationResult]
    recommendations: List[str]


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception as e:
        return 0


def extract_frontmatter(file_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from a markdown file.

    Returns:
        Dict with frontmatter fields, or None if no frontmatter
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter (--- at start and end)
        # Allow for optional content before frontmatter (e.g., title line)
        match = re.search(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None

        frontmatter_text = match.group(1)
        frontmatter = {}

        # Parse simple YAML fields (nested_structure, nested_files, version)
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Handle nested_structure: true/false
            if line.startswith('nested_structure:'):
                value = line.split(':', 1)[1].strip()
                frontmatter['nested_structure'] = value.lower() == 'true'

            # Handle version
            elif line.startswith('version:'):
                value = line.split(':', 1)[1].strip()
                frontmatter['version'] = value

            # Handle nested_files array
            elif line.startswith('nested_files:'):
                frontmatter['nested_files'] = []
            elif line.startswith('- "') or line.startswith("- '"):
                # Extract quoted file path
                file_match = re.match(r'- ["\'](.+?)["\']', line)
                if file_match and 'nested_files' in frontmatter:
                    frontmatter['nested_files'].append(file_match.group(1))

        return frontmatter

    except Exception as e:
        return None


def check_critical_workflows_section(file_path: Path) -> Tuple[bool, int]:
    """Check if file has Critical Workflows section within first 300 lines.

    Returns:
        (found, line_number) tuple
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [f.readline() for _ in range(300)]  # Check first 300 lines

        for i, line in enumerate(lines, start=1):
            if re.search(r'Critical Workflows', line, re.IGNORECASE):
                return (True, i)

        return (False, 0)

    except Exception as e:
        return (False, 0)


def validate_file(file_path: Path) -> FileValidation:
    """Validate a single awareness file against SAP-009 v2.1.0 requirements.

    Args:
        file_path: Path to awareness file (AGENTS.md, CLAUDE.md, or awareness-guide.md)

    Returns:
        FileValidation with complete results
    """
    checks = []
    recommendations = []
    overall_status = "PASS"

    # Check 1: File exists and is readable
    if not file_path.exists():
        checks.append(ValidationResult(
            check_name="file_exists",
            status="FAIL",
            message=f"File does not exist: {file_path}"
        ))
        return FileValidation(
            file_path=str(file_path),
            line_count=0,
            token_estimate=0,
            status="FAIL",
            checks=checks,
            recommendations=["File not found"]
        )

    # Count lines and calculate tokens
    line_count = count_lines(file_path)
    token_estimate = int(line_count * AVG_TOKENS_PER_LINE)

    # Check 2: File size against thresholds
    if line_count >= THRESHOLD_CRITICAL:
        checks.append(ValidationResult(
            check_name="file_size",
            status="FAIL",
            message=f"File exceeds CRITICAL threshold: {line_count} lines (>{THRESHOLD_CRITICAL} lines)",
            details={
                "line_count": line_count,
                "threshold": THRESHOLD_CRITICAL,
                "percent_over": int(((line_count - THRESHOLD_CRITICAL) / THRESHOLD_CRITICAL) * 100)
            }
        ))
        overall_status = "FAIL"
        recommendations.append(f"CRITICAL: Split file immediately (see SAP-009 splitting strategy)")

    elif line_count >= THRESHOLD_WARNING:
        checks.append(ValidationResult(
            check_name="file_size",
            status="WARN",
            message=f"File exceeds WARNING threshold: {line_count} lines (>{THRESHOLD_WARNING} lines)",
            details={
                "line_count": line_count,
                "threshold": THRESHOLD_WARNING,
                "percent_over": int(((line_count - THRESHOLD_WARNING) / THRESHOLD_WARNING) * 100)
            }
        ))
        if overall_status == "PASS":
            overall_status = "WARN"
        recommendations.append(f"Consider splitting file (see SAP-009 splitting strategy)")

    else:
        checks.append(ValidationResult(
            check_name="file_size",
            status="PASS",
            message=f"File size within target: {line_count} lines (<{THRESHOLD_WARNING} lines)",
            details={"line_count": line_count, "threshold": THRESHOLD_WARNING}
        ))

    # Check 3: Token budget
    if token_estimate >= PHASE_1_TOKEN_TARGET:
        checks.append(ValidationResult(
            check_name="token_budget",
            status="FAIL",
            message=f"Token budget exceeds Phase 1 target: {token_estimate} tokens (>{PHASE_1_TOKEN_TARGET} tokens)",
            details={
                "token_estimate": token_estimate,
                "target": PHASE_1_TOKEN_TARGET,
                "percent_over": int(((token_estimate - PHASE_1_TOKEN_TARGET) / PHASE_1_TOKEN_TARGET) * 100)
            }
        ))
        overall_status = "FAIL"
        recommendations.append(f"Reduce token budget to <{PHASE_1_TOKEN_TARGET} via splitting")

    else:
        checks.append(ValidationResult(
            check_name="token_budget",
            status="PASS",
            message=f"Token budget within Phase 1 target: {token_estimate} tokens (<{PHASE_1_TOKEN_TARGET} tokens)",
            details={"token_estimate": token_estimate, "target": PHASE_1_TOKEN_TARGET}
        ))

    # Check 4: Frontmatter
    frontmatter = extract_frontmatter(file_path)

    if frontmatter is None:
        checks.append(ValidationResult(
            check_name="frontmatter",
            status="WARN",
            message="No YAML frontmatter found",
            details={}
        ))
        if overall_status == "PASS":
            overall_status = "WARN"

    else:
        # Check nested_structure field
        has_nested_structure = frontmatter.get('nested_structure', False)

        if has_nested_structure:
            checks.append(ValidationResult(
                check_name="nested_structure_field",
                status="PASS",
                message="Frontmatter declares nested_structure: true",
                details={"nested_structure": True}
            ))

            # Check nested_files field
            nested_files = frontmatter.get('nested_files', [])

            if not nested_files:
                checks.append(ValidationResult(
                    check_name="nested_files_field",
                    status="FAIL",
                    message="nested_structure: true but nested_files array is empty",
                    details={}
                ))
                overall_status = "FAIL"
                recommendations.append("Add nested_files array to frontmatter")

            else:
                checks.append(ValidationResult(
                    check_name="nested_files_field",
                    status="PASS",
                    message=f"Frontmatter lists {len(nested_files)} nested files",
                    details={"nested_files": nested_files}
                ))

                # Check 5: Verify nested files exist
                parent_dir = file_path.parent
                missing_files = []

                for nested_file in nested_files:
                    nested_path = parent_dir / nested_file
                    if not nested_path.exists():
                        missing_files.append(nested_file)

                if missing_files:
                    checks.append(ValidationResult(
                        check_name="nested_files_exist",
                        status="FAIL",
                        message=f"Missing {len(missing_files)} nested files",
                        details={"missing_files": missing_files}
                    ))
                    overall_status = "FAIL"
                    recommendations.append(f"Create missing nested files: {', '.join(missing_files)}")

                else:
                    checks.append(ValidationResult(
                        check_name="nested_files_exist",
                        status="PASS",
                        message=f"All {len(nested_files)} nested files exist",
                        details={"nested_files": nested_files}
                    ))

            # Check 6: Critical Workflows section
            has_critical_workflows, cw_line = check_critical_workflows_section(file_path)

            if not has_critical_workflows:
                checks.append(ValidationResult(
                    check_name="critical_workflows_section",
                    status="FAIL",
                    message="Missing Critical Workflows section (required when nested_structure: true)",
                    details={}
                ))
                overall_status = "FAIL"
                recommendations.append("Add Critical Workflows section (lines 20-100, see SAP-009)")

            elif cw_line > 100:
                checks.append(ValidationResult(
                    check_name="critical_workflows_section",
                    status="WARN",
                    message=f"Critical Workflows section found at line {cw_line} (should be <100)",
                    details={"line_number": cw_line}
                ))
                if overall_status == "PASS":
                    overall_status = "WARN"
                recommendations.append(f"Move Critical Workflows section to top (currently line {cw_line}, target lines 20-100)")

            else:
                checks.append(ValidationResult(
                    check_name="critical_workflows_section",
                    status="PASS",
                    message=f"Critical Workflows section found at line {cw_line} (within target lines 20-100)",
                    details={"line_number": cw_line}
                ))

        else:
            # No nested structure declared - check if file size suggests it should be split
            if line_count >= THRESHOLD_WARNING:
                checks.append(ValidationResult(
                    check_name="nested_structure_field",
                    status="WARN",
                    message=f"File has {line_count} lines but nested_structure not declared (consider splitting)",
                    details={"nested_structure": False, "line_count": line_count}
                ))
                if overall_status == "PASS":
                    overall_status = "WARN"

            else:
                checks.append(ValidationResult(
                    check_name="nested_structure_field",
                    status="PASS",
                    message="nested_structure: false (appropriate for small files)",
                    details={"nested_structure": False}
                ))

    return FileValidation(
        file_path=str(file_path),
        line_count=line_count,
        token_estimate=token_estimate,
        status=overall_status,
        checks=checks,
        recommendations=recommendations
    )


def validate_directory(directory: Path, recursive: bool = True) -> List[FileValidation]:
    """Validate all awareness files in a directory.

    Args:
        directory: Path to directory
        recursive: Whether to search subdirectories

    Returns:
        List of FileValidation results
    """
    results = []

    # Find all awareness files
    patterns = ['**/AGENTS.md', '**/CLAUDE.md', '**/awareness-guide.md'] if recursive else ['AGENTS.md', 'CLAUDE.md', 'awareness-guide.md']

    for pattern in patterns:
        for file_path in directory.glob(pattern):
            results.append(validate_file(file_path))

    return results


def print_validation_result(validation: FileValidation, verbose: bool = True):
    """Print validation result in human-readable format."""
    # Status symbol
    status_symbol = {
        "PASS": "✅",
        "WARN": "⚠️",
        "FAIL": "❌"
    }

    symbol = status_symbol.get(validation.status, "❓")

    print(f"\n{symbol} {validation.status}: {validation.file_path}")
    print(f"   Lines: {validation.line_count} | Tokens: ~{validation.token_estimate}")

    if verbose:
        print(f"\n   Checks:")
        for check in validation.checks:
            check_symbol = status_symbol.get(check.status, "❓")
            print(f"   {check_symbol} {check.check_name}: {check.message}")

            if check.details and check.status != "PASS":
                for key, value in check.details.items():
                    print(f"      - {key}: {value}")

    if validation.recommendations:
        print(f"\n   Recommendations:")
        for rec in validation.recommendations:
            print(f"   → {rec}")


def print_summary(results: List[FileValidation]):
    """Print summary of all validation results."""
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    warned = sum(1 for r in results if r.status == "WARN")
    failed = sum(1 for r in results if r.status == "FAIL")

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files validated: {total}")
    print(f"✅ PASS: {passed} ({int(passed/total*100)}%)")
    print(f"⚠️  WARN: {warned} ({int(warned/total*100)}%)")
    print(f"❌ FAIL: {failed} ({int(failed/total*100)}%)")
    print("=" * 60)

    # Overall status
    if failed > 0:
        print("\n❌ OVERALL STATUS: FAIL (action required)")
        return 1
    elif warned > 0:
        print("\n⚠️  OVERALL STATUS: WARN (review recommended)")
        return 0
    else:
        print("\n✅ OVERALL STATUS: PASS (all validations passed)")
        return 0


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    # Parse arguments
    json_output = '--json' in sys.argv
    summary_only = '--summary' in sys.argv

    # Get file/directory path
    path_arg = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if not path_arg:
        print("Error: No file or directory specified")
        print(__doc__)
        sys.exit(2)

    target_path = Path(path_arg[0])

    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(2)

    # Validate
    if target_path.is_file():
        results = [validate_file(target_path)]
    else:
        results = validate_directory(target_path)

    if not results:
        print(f"No awareness files found in {target_path}")
        sys.exit(0)

    # Output results
    if json_output:
        output = {
            "total": len(results),
            "passed": sum(1 for r in results if r.status == "PASS"),
            "warned": sum(1 for r in results if r.status == "WARN"),
            "failed": sum(1 for r in results if r.status == "FAIL"),
            "files": [asdict(r) for r in results]
        }
        print(json.dumps(output, indent=2))
        exit_code = 1 if output["failed"] > 0 else 0

    else:
        # Human-readable output
        if not summary_only:
            for result in results:
                print_validation_result(result)

        exit_code = print_summary(results)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
