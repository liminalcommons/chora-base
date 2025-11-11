#!/usr/bin/env python3
"""
Validate README.md structure in SAP documentation.

This script checks that all SAP README.md files follow the standardized 9-section
pattern established in Batches 11-15.

Usage:
    python scripts/validate-readme-structure.py                    # Check all SAPs
    python scripts/validate-readme-structure.py --sap SAP-034      # Check specific SAP
    python scripts/validate-readme-structure.py --verbose          # Show all sections found
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Required README sections (in order)
REQUIRED_SECTIONS = [
    ("header", r"^# SAP-\d+:"),
    ("what_is", r"^## (What is|What Is|Overview)"),
    ("when_to_use", r"^## (When to Use|Use Cases)"),
    ("quick_start", r"^## (Quick Start|Getting Started)"),
    ("key_features", r"^## Key Features"),
    ("workflows_or_reference", r"^## (Common Workflows|Quick Reference|Reference)"),
    ("integration", r"^## Integration"),
    ("success_metrics", r"^## Success Metrics"),
    ("troubleshooting", r"^## Troubleshooting"),
    ("learn_more", r"^## (Learn More|Documentation|Resources)"),
]

# Recommended Quick Start time range (minutes)
QUICK_START_TIME_MIN = 5
QUICK_START_TIME_MAX = 60


def find_sap_directories(base_path: Path = None) -> List[Path]:
    """Find all SAP directories in skilled-awareness."""
    if base_path is None:
        base_path = Path(__file__).parent.parent / "docs" / "skilled-awareness"

    sap_dirs = []
    for path in base_path.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            # Check if directory has README.md
            if (path / "README.md").exists():
                sap_dirs.append(path)

    return sorted(sap_dirs)


def extract_sections(content: str) -> Dict[str, Tuple[int, str]]:
    """
    Extract all sections from README content.

    Returns:
        Dict mapping section name to (line_number, header_text)
    """
    sections = {}
    lines = content.split("\n")

    for i, line in enumerate(lines, start=1):
        if line.startswith("#"):
            # Extract header level and text
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level, text = match.groups()
                section_key = text.lower().replace(" ", "_").replace("-", "_")
                sections[section_key] = (i, f"{level} {text}")

    return sections


def validate_readme_structure(readme_path: Path, verbose: bool = False) -> Tuple[bool, List[str], Dict]:
    """
    Validate README.md structure.

    Returns:
        (is_valid, issues, metadata) tuple
    """
    if not readme_path.exists():
        return False, ["README.md not found"], {}

    content = readme_path.read_text(encoding="utf-8")
    issues = []
    metadata = {
        "line_count": len(content.split("\n")),
        "sections_found": [],
        "missing_sections": [],
    }

    # Extract all sections
    sections = extract_sections(content)
    metadata["sections_found"] = list(sections.keys())

    # Check required sections
    for section_name, pattern in REQUIRED_SECTIONS:
        found = False
        for section_key, (line_num, header_text) in sections.items():
            if re.search(pattern, header_text, re.IGNORECASE):
                found = True
                if verbose:
                    print(f"  ✓ {section_name}: {header_text} (line {line_num})")
                break

        if not found:
            issues.append(f"Missing required section: {section_name} (pattern: {pattern})")
            metadata["missing_sections"].append(section_name)

    # Check Quick Start time estimate
    quick_start_match = re.search(
        r"Quick Start.*?\((\d+)\s*(?:min|minute)", content, re.IGNORECASE
    )
    if quick_start_match:
        time_minutes = int(quick_start_match.group(1))
        metadata["quick_start_time"] = time_minutes

        if time_minutes < QUICK_START_TIME_MIN:
            issues.append(
                f"Quick Start time ({time_minutes} min) is suspiciously short "
                f"(expected {QUICK_START_TIME_MIN}-{QUICK_START_TIME_MAX} min)"
            )
        elif time_minutes > QUICK_START_TIME_MAX:
            issues.append(
                f"Quick Start time ({time_minutes} min) is longer than recommended "
                f"(expected {QUICK_START_TIME_MIN}-{QUICK_START_TIME_MAX} min)"
            )
    else:
        issues.append("Quick Start section missing time estimate (e.g., '## Quick Start (15 minutes)')")

    # Check for emoji markers in Key Features
    if "Key Features" in content:
        key_features_section = re.search(
            r"## Key Features.*?(?=\n## |\Z)", content, re.DOTALL
        )
        if key_features_section:
            emoji_bullets = re.findall(r"- ✅", key_features_section.group(0))
            metadata["emoji_bullets"] = len(emoji_bullets)

            if len(emoji_bullets) < 5:
                issues.append(
                    f"Key Features has {len(emoji_bullets)} emoji bullets, expected at least 5"
                )
        else:
            issues.append("Could not extract Key Features section")

    # Check for integration table
    if "Integration" in content or "integration" in content.lower():
        has_table = bool(re.search(r"\|.*\|.*\|", content))
        metadata["has_integration_table"] = has_table

        if not has_table:
            issues.append("Integration section should contain a table of related SAPs")

    # Check for troubleshooting scenarios
    if "Troubleshooting" in content:
        troubleshooting_section = re.search(
            r"## Troubleshooting.*?(?=\n## |\Z)", content, re.DOTALL
        )
        if troubleshooting_section:
            problem_headings = re.findall(
                r"### Problem \d+:", troubleshooting_section.group(0)
            )
            metadata["troubleshooting_scenarios"] = len(problem_headings)

            if len(problem_headings) < 3:
                issues.append(
                    f"Troubleshooting has {len(problem_headings)} scenarios, expected at least 3"
                )

    return len(issues) == 0, issues, metadata


def validate_sap(sap_dir: Path, verbose: bool = False) -> Dict:
    """Validate README structure for a SAP."""
    sap_id = sap_dir.name
    readme_path = sap_dir / "README.md"

    result = {
        "sap_id": sap_id,
        "path": str(sap_dir),
        "valid": False,
        "issues": [],
        "metadata": {},
    }

    result["valid"], result["issues"], result["metadata"] = validate_readme_structure(
        readme_path, verbose
    )

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate README.md structure in SAP documentation"
    )
    parser.add_argument(
        "--sap",
        type=str,
        help="Validate specific SAP (e.g., SAP-034)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all sections found in each README",
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
            print(f"\nValidating {sap_dir.name} README.md...")
        result = validate_sap(sap_dir, verbose=args.verbose)
        results.append(result)

    # Generate summary
    total_saps = len(results)
    valid_count = sum(1 for r in results if r["valid"])

    # Calculate average metrics
    line_counts = [r["metadata"].get("line_count", 0) for r in results if r["metadata"].get("line_count")]
    avg_line_count = sum(line_counts) / len(line_counts) if line_counts else 0

    quick_start_times = [r["metadata"].get("quick_start_time") for r in results if r["metadata"].get("quick_start_time")]
    avg_quick_start = sum(quick_start_times) / len(quick_start_times) if quick_start_times else 0

    print("\n" + "=" * 70)
    print("README Structure Validation Summary")
    print("=" * 70)
    print(f"Total SAPs checked: {total_saps}")
    print(f"Valid README structure: {valid_count}/{total_saps} ({valid_count/total_saps*100:.1f}%)")
    print(f"Average README length: {avg_line_count:.0f} lines")
    if avg_quick_start > 0:
        print(f"Average Quick Start time: {avg_quick_start:.0f} minutes")
    print("=" * 70)

    # Show SAPs with issues (if not summary-only)
    if not args.summary_only:
        saps_with_issues = [r for r in results if not r["valid"]]

        if saps_with_issues:
            print("\nSAPs with README structure issues:")
            for result in saps_with_issues:
                print(f"\n{result['sap_id']}:")
                for issue in result["issues"]:
                    print(f"  - {issue}")

                # Show metadata
                if result["metadata"]:
                    print(f"  Metadata:")
                    print(f"    - Lines: {result['metadata'].get('line_count', 'N/A')}")
                    if result["metadata"].get("quick_start_time"):
                        print(f"    - Quick Start: {result['metadata']['quick_start_time']} min")
                    if result["metadata"].get("emoji_bullets"):
                        print(f"    - Key Features bullets: {result['metadata']['emoji_bullets']}")
                    if result["metadata"].get("troubleshooting_scenarios"):
                        print(f"    - Troubleshooting scenarios: {result['metadata']['troubleshooting_scenarios']}")
        else:
            print("\n✅ All SAPs have valid README structure!")

    # Exit with error if any validation failed
    return 0 if valid_count == total_saps else 1


if __name__ == "__main__":
    sys.exit(main())
