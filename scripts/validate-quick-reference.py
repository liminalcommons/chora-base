#!/usr/bin/env python3
"""
Validate Quick Reference sections in SAP documentation.

This script checks that all SAP AGENTS.md/awareness-guide.md and CLAUDE.md files
contain the standardized Quick Reference section established in Batches 11-15.

Usage:
    python scripts/validate-quick-reference.py                    # Check all SAPs
    python scripts/validate-quick-reference.py --sap SAP-034      # Check specific SAP
    python scripts/validate-quick-reference.py --fix              # Auto-fix issues (dry-run)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Fix Windows Unicode encoding for emoji output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# Required Quick Reference pattern elements
REQUIRED_ELEMENTS = {
    "emoji_header": r"^## 📖 Quick Reference",
    "new_to_prompt": r"\*\*New to SAP-\d+\?\*\* → Read \*\*\[README\.md\]\(README\.md\)\*\* first",
    "provides_section": r"The README provides:",
    "emoji_bullet_start": r"- 🚀 \*\*Quick Start\*\*",
    "emoji_bullet_time_savings": r"- 📚 \*\*.*Time Savings\*\*",
    "emoji_bullet_feature": r"- 🎯 \*\*.*\*\*",
    "emoji_bullet_integration": r"- 🔗 \*\*Integration\*\*",
    "purpose_statement": r"This (AGENTS\.md|CLAUDE\.md|awareness-guide\.md) provides:",
}


def find_sap_directories(base_path: Path = None) -> List[Path]:
    """Find all SAP directories in skilled-awareness."""
    if base_path is None:
        base_path = Path(__file__).parent.parent / "docs" / "skilled-awareness"

    sap_dirs = []
    for path in base_path.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            # Check if directory has SAP artifacts
            if (path / "README.md").exists() or (path / "protocol-spec.md").exists():
                sap_dirs.append(path)

    return sorted(sap_dirs)


def extract_sap_id(sap_dir: Path) -> str:
    """Extract SAP ID from directory name or README."""
    # Try to extract from README first
    readme_path = sap_dir / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        match = re.search(r"SAP-\d+", content, re.MULTILINE)
        if match:
            return match.group(0)

    # Fallback: infer from directory name
    return sap_dir.name.upper().replace("-", "_")


def find_agents_file(sap_dir: Path) -> Path:
    """Find AGENTS.md or awareness-guide.md file."""
    if (sap_dir / "AGENTS.md").exists():
        return sap_dir / "AGENTS.md"
    elif (sap_dir / "awareness-guide.md").exists():
        return sap_dir / "awareness-guide.md"
    return None


def validate_quick_reference(file_path: Path, sap_id: str) -> Tuple[bool, List[str]]:
    """
    Validate Quick Reference section in a file.

    Returns:
        (is_valid, issues) tuple
    """
    if not file_path or not file_path.exists():
        return False, ["File not found"]

    content = file_path.read_text(encoding="utf-8")
    issues = []

    # Check for Quick Reference section
    if "## 📖 Quick Reference" not in content:
        issues.append("Missing '## 📖 Quick Reference' header")
        return False, issues

    # Extract Quick Reference section
    match = re.search(
        r"## 📖 Quick Reference.*?(?=\n## |\Z)",
        content,
        re.DOTALL
    )

    if not match:
        issues.append("Could not extract Quick Reference section")
        return False, issues

    quick_ref_section = match.group(0)

    # Validate each required element
    for element_name, pattern in REQUIRED_ELEMENTS.items():
        if not re.search(pattern, quick_ref_section, re.MULTILINE):
            issues.append(f"Missing or incorrect: {element_name}")

    # Check for at least 5 emoji bullets (🚀📚🎯🔧📊🔗)
    emoji_bullets = re.findall(r"- [🚀📚🎯🔧📊🔗] \*\*", quick_ref_section)
    if len(emoji_bullets) < 5:
        issues.append(f"Expected at least 5 emoji bullets, found {len(emoji_bullets)}")

    # Check SAP ID consistency
    if sap_id and f"New to {sap_id}?" not in quick_ref_section:
        issues.append(f"SAP ID mismatch: expected '{sap_id}' in 'New to' prompt")

    return len(issues) == 0, issues


def validate_sap(sap_dir: Path, verbose: bool = False) -> Dict:
    """Validate Quick Reference sections for a SAP."""
    sap_id = extract_sap_id(sap_dir)
    result = {
        "sap_id": sap_id,
        "path": str(sap_dir),
        "agents_valid": False,
        "claude_valid": False,
        "agents_issues": [],
        "claude_issues": [],
    }

    # Validate AGENTS.md or awareness-guide.md
    agents_file = find_agents_file(sap_dir)
    if agents_file:
        result["agents_valid"], result["agents_issues"] = validate_quick_reference(
            agents_file, sap_id
        )
        if verbose and result["agents_issues"]:
            print(f"  {agents_file.name}: {', '.join(result['agents_issues'])}")
    else:
        result["agents_issues"] = ["AGENTS.md or awareness-guide.md not found"]

    # Validate CLAUDE.md
    claude_file = sap_dir / "CLAUDE.md"
    if claude_file.exists():
        result["claude_valid"], result["claude_issues"] = validate_quick_reference(
            claude_file, sap_id
        )
        if verbose and result["claude_issues"]:
            print(f"  CLAUDE.md: {', '.join(result['claude_issues'])}")
    else:
        result["claude_issues"] = ["CLAUDE.md not found"]

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate Quick Reference sections in SAP documentation"
    )
    parser.add_argument(
        "--sap",
        type=str,
        help="Validate specific SAP (e.g., SAP-034)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed issues for each SAP",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics",
    )

    args = parser.parse_args()

    # Find SAPs to validate
    base_path = Path(__file__).parent.parent / "docs" / "skilled-awareness"

    if args.sap:
        # Find specific SAP directory
        sap_dirs = [d for d in find_sap_directories(base_path) if args.sap.lower() in d.name.lower()]
        if not sap_dirs:
            print(f"Error: SAP '{args.sap}' not found")
            return 1
    else:
        sap_dirs = find_sap_directories(base_path)

    # Validate each SAP
    results = []
    for sap_dir in sap_dirs:
        if args.verbose and not args.summary_only:
            print(f"\nValidating {sap_dir.name}...")
        result = validate_sap(sap_dir, verbose=args.verbose)
        results.append(result)

    # Generate summary
    total_saps = len(results)
    agents_valid_count = sum(1 for r in results if r["agents_valid"])
    claude_valid_count = sum(1 for r in results if r["claude_valid"])
    both_valid_count = sum(
        1 for r in results if r["agents_valid"] and r["claude_valid"]
    )

    print("\n" + "=" * 70)
    print("Quick Reference Validation Summary")
    print("=" * 70)
    print(f"Total SAPs checked: {total_saps}")
    print(f"AGENTS.md/awareness-guide.md valid: {agents_valid_count}/{total_saps} ({agents_valid_count/total_saps*100:.1f}%)")
    print(f"CLAUDE.md valid: {claude_valid_count}/{total_saps} ({claude_valid_count/total_saps*100:.1f}%)")
    print(f"Both valid: {both_valid_count}/{total_saps} ({both_valid_count/total_saps*100:.1f}%)")
    print("=" * 70)

    # Show SAPs with issues (if not summary-only)
    if not args.summary_only:
        saps_with_issues = [
            r for r in results if not (r["agents_valid"] and r["claude_valid"])
        ]

        if saps_with_issues:
            print("\nSAPs with Quick Reference issues:")
            for result in saps_with_issues:
                print(f"\n{result['sap_id']} ({Path(result['path']).name}):")
                if result["agents_issues"]:
                    agents_file = "AGENTS.md" if (Path(result['path']) / "AGENTS.md").exists() else "awareness-guide.md"
                    print(f"  {agents_file}:")
                    for issue in result["agents_issues"]:
                        print(f"    - {issue}")
                if result["claude_issues"]:
                    print(f"  CLAUDE.md:")
                    for issue in result["claude_issues"]:
                        print(f"    - {issue}")
        else:
            print("\n✅ All SAPs have valid Quick Reference sections!")

    # Exit with error if any validation failed
    return 0 if both_valid_count == total_saps else 1


if __name__ == "__main__":
    sys.exit(main())
