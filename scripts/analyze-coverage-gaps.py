#!/usr/bin/env python3
"""
Analyze SAP coverage gaps and generate detailed reports.
Phase 2: SAP Coverage Mapping
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set
from datetime import datetime


# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Root directory
ROOT = Path(__file__).parent.parent

# SAP definitions with expected coverage patterns
SAP_DEFINITIONS = {
    "SAP-000": {
        "name": "SAP Framework",
        "expected_patterns": [
            "docs/reference/skilled-awareness/sap-framework/",
            "SKILLED_AWARENESS_PACKAGE_PROTOCOL.md"
        ]
    },
    "SAP-001": {
        "name": "Inbox Protocol",
        "expected_patterns": [
            "inbox/",
            "docs/reference/skilled-awareness/inbox/"
        ]
    },
    "SAP-002": {
        "name": "Chora-Base",
        "expected_patterns": [
            "README.md",
            "CHANGELOG.md",
            "docs/reference/chora-base/",
            "docs/reference/chora-compose/",
            "docs/reference/skilled-awareness/chora-base/"
        ]
    },
    "SAP-003": {
        "name": "Project Bootstrap",
        "expected_patterns": [
            "blueprints/",
            "docs/reference/skilled-awareness/project-bootstrap/"
        ]
    },
    "SAP-004": {
        "name": "Testing Framework",
        "expected_patterns": [
            "static-template/tests/",
            "docs/reference/skilled-awareness/testing-framework/"
        ]
    },
    "SAP-005": {
        "name": "CI/CD Workflows",
        "expected_patterns": [
            "static-template/.github/workflows/",
            "docs/reference/skilled-awareness/ci-cd-workflows/"
        ]
    },
    "SAP-006": {
        "name": "Quality Gates",
        "expected_patterns": [
            "static-template/.pre-commit-config.yaml",
            "docs/reference/skilled-awareness/quality-gates/"
        ]
    },
    "SAP-007": {
        "name": "Documentation Framework",
        "expected_patterns": [
            "static-template/user-docs/",
            "static-template/dev-docs/",
            "static-template/project-docs/",
            "static-template/DOCUMENTATION_STANDARD.md",
            "docs/reference/skilled-awareness/documentation-framework/"
        ]
    },
    "SAP-008": {
        "name": "Automation Scripts",
        "expected_patterns": [
            "static-template/scripts/",
            "static-template/justfile",
            "docs/reference/skilled-awareness/automation-scripts/"
        ]
    },
    "SAP-009": {
        "name": "Agent Awareness",
        "expected_patterns": [
            "claude/",
            "static-template/CLAUDE.md",
            ".claude/",
            "AGENT_SETUP_GUIDE.md",
            "docs/reference/skilled-awareness/agent-awareness/"
        ]
    },
    "SAP-010": {
        "name": "Memory System",
        "expected_patterns": [
            "static-template/.chora/memory/",
            "docs/reference/skilled-awareness/memory-system/"
        ]
    },
    "SAP-011": {
        "name": "Docker Operations",
        "expected_patterns": [
            "static-template/Dockerfile",
            "static-template/Dockerfile.test",
            "static-template/docker-compose.yml",
            "static-template/.dockerignore",
            "static-template/DOCKER_BEST_PRACTICES.md",
            "docs/reference/skilled-awareness/docker-operations/"
        ]
    },
    "SAP-012": {
        "name": "Development Lifecycle",
        "expected_patterns": [
            "static-template/dev-docs/workflows/",
            "docs/reference/skilled-awareness/development-lifecycle/"
        ]
    },
    "SAP-013": {
        "name": "Metrics Tracking",
        "expected_patterns": [
            "static-template/src/__package_name__/utils/claude_metrics.py",
            "static-template/project-docs/metrics/",
            "docs/reference/skilled-awareness/metrics-tracking/"
        ]
    }
}


def load_inventory(csv_path: Path) -> List[Dict]:
    """Load file inventory from CSV."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def analyze_coverage_gaps() -> Dict:
    """Analyze coverage gaps for each SAP."""
    inventory = load_inventory(ROOT / "docs/inventory/file-inventory.csv")

    analysis = {
        "sap_coverage": {},
        "uncovered_files": [],
        "covered_files": [],
        "multi_sap_files": [],
        "uncovered_by_directory": defaultdict(list),
        "uncovered_by_type": defaultdict(list)
    }

    # Analyze each file
    for entry in inventory:
        filepath = entry['filepath']
        status = entry['status']
        related_saps = entry['related_saps']
        file_type = entry['type']

        if status == "covered":
            analysis["covered_files"].append(entry)

            # Track multi-SAP files
            if related_saps != "None" and "," in related_saps:
                sap_list = [s.strip() for s in related_saps.split(",")]
                analysis["multi_sap_files"].append({
                    "filepath": filepath,
                    "saps": sap_list,
                    "count": len(sap_list)
                })
        else:
            analysis["uncovered_files"].append(entry)

            # Group by directory
            directory = str(Path(filepath).parent)
            analysis["uncovered_by_directory"][directory].append(filepath)

            # Group by type
            analysis["uncovered_by_type"][file_type].append(filepath)

    # Analyze each SAP's coverage
    for sap_id, sap_info in SAP_DEFINITIONS.items():
        covered_files = [
            e for e in analysis["covered_files"]
            if sap_id in (e['related_saps'] or "")
        ]

        analysis["sap_coverage"][sap_id] = {
            "name": sap_info["name"],
            "covered_count": len(covered_files),
            "covered_files": [e['filepath'] for e in covered_files],
            "expected_patterns": sap_info["expected_patterns"]
        }

    return analysis


def generate_coverage_matrix(analysis: Dict, output_path: Path):
    """Generate SAP coverage matrix markdown."""
    content = [
        "# SAP Coverage Matrix",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Overview",
        "",
        f"- **Total files**: {len(analysis['covered_files']) + len(analysis['uncovered_files'])}",
        f"- **Covered files**: {len(analysis['covered_files'])} ({len(analysis['covered_files']) / (len(analysis['covered_files']) + len(analysis['uncovered_files'])) * 100:.1f}%)",
        f"- **Uncovered files**: {len(analysis['uncovered_files'])} ({len(analysis['uncovered_files']) / (len(analysis['covered_files']) + len(analysis['uncovered_files'])) * 100:.1f}%)",
        f"- **Multi-SAP files**: {len(analysis['multi_sap_files'])}",
        "",
        "---",
        "",
        "## SAP Coverage Details",
        ""
    ]

    # Add each SAP
    for sap_id in sorted(analysis["sap_coverage"].keys()):
        sap_data = analysis["sap_coverage"][sap_id]

        content.extend([
            f"### {sap_id}: {sap_data['name']}",
            "",
            f"**Files covered**: {sap_data['covered_count']}",
            "",
            "**Expected patterns**:",
            ""
        ])

        for pattern in sap_data["expected_patterns"]:
            content.append(f"- `{pattern}`")

        content.extend([
            "",
            "**Actual coverage**:",
            ""
        ])

        if sap_data["covered_files"]:
            # Group by directory
            by_dir = defaultdict(list)
            for filepath in sorted(sap_data["covered_files"]):
                directory = str(Path(filepath).parent)
                by_dir[directory].append(Path(filepath).name)

            for directory in sorted(by_dir.keys()):
                content.append(f"- **{directory}/** ({len(by_dir[directory])} files)")
                for filename in sorted(by_dir[directory])[:5]:  # Show first 5
                    content.append(f"  - {filename}")
                if len(by_dir[directory]) > 5:
                    content.append(f"  - ... and {len(by_dir[directory]) - 5} more")
                content.append("")
        else:
            content.append("*(No files covered)*")
            content.append("")

        content.extend([
            "---",
            ""
        ])

    output_path.write_text("\n".join(content))
    print(f"✅ Coverage matrix generated: {output_path}")


def generate_uncovered_report(analysis: Dict, output_path: Path):
    """Generate detailed uncovered files report."""
    content = [
        "# Uncovered Files Report",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"**Total uncovered files**: {len(analysis['uncovered_files'])}",
        "",
        "### By File Type",
        "",
        "| Type | Count |",
        "|------|-------|"
    ]

    for file_type in sorted(analysis["uncovered_by_type"].keys()):
        count = len(analysis["uncovered_by_type"][file_type])
        content.append(f"| {file_type} | {count} |")

    content.extend([
        "",
        "---",
        "",
        "## Uncovered Files by Directory",
        ""
    ])

    # Sort directories by number of uncovered files (descending)
    sorted_dirs = sorted(
        analysis["uncovered_by_directory"].items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    for directory, files in sorted_dirs:
        content.extend([
            f"### {directory}/ ({len(files)} files)",
            ""
        ])

        for filepath in sorted(files):
            filename = Path(filepath).name

            # Find in original uncovered_files to get metadata
            file_entry = next(
                (e for e in analysis["uncovered_files"] if e['filepath'] == filepath),
                None
            )

            if file_entry:
                file_type = file_entry['type']
                size_kb = int(file_entry['size_bytes']) / 1024
                content.append(f"- **{filename}** ({file_type}, {size_kb:.1f} KB)")
            else:
                content.append(f"- **{filename}**")

        content.extend([
            "",
            "**Recommendation**: TODO - Analyze these files for SAP assignment or archival",
            "",
            "---",
            ""
        ])

    output_path.write_text("\n".join(content))
    print(f"✅ Uncovered files report generated: {output_path}")


def generate_high_priority_review(analysis: Dict, output_path: Path):
    """Generate high-priority files for review."""
    content = [
        "# High-Priority Files for Review",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Critical Uncovered Files",
        "",
        "These files are high-priority for SAP assignment or archival decision.",
        "",
        "### Root-Level Documentation",
        ""
    ]

    # Root-level uncovered files
    root_docs = [
        e for e in analysis["uncovered_files"]
        if "/" not in e['filepath'] and e['type'] == 'documentation'
    ]

    if root_docs:
        for entry in root_docs:
            size_kb = int(entry['size_bytes']) / 1024
            content.append(f"- **{entry['filepath']}** ({size_kb:.1f} KB)")
            content.append(f"  - **Action needed**: Determine if should be covered by SAP-002 (chora-base)")
            content.append("")
    else:
        content.append("*(No root-level uncovered documentation)*")
        content.append("")

    content.extend([
        "---",
        "",
        "### Root-Level Code & Config",
        ""
    ])

    # Root-level code/config
    root_code = [
        e for e in analysis["uncovered_files"]
        if "/" not in e['filepath'] and e['type'] in ['code', 'config', 'tooling']
    ]

    if root_code:
        for entry in root_code:
            size_kb = int(entry['size_bytes']) / 1024
            content.append(f"- **{entry['filepath']}** ({entry['type']}, {size_kb:.1f} KB)")
            content.append(f"  - **Action needed**: Should this be covered by a SAP or archived?")
            content.append("")
    else:
        content.append("*(No root-level uncovered code/config)*")
        content.append("")

    content.extend([
        "---",
        "",
        "### Documentation in /docs/ Not Covered",
        ""
    ])

    # Docs directory uncovered
    docs_uncovered = [
        e for e in analysis["uncovered_files"]
        if e['filepath'].startswith('docs/') and e['type'] == 'documentation'
    ]

    # Group by subdirectory
    docs_by_subdir = defaultdict(list)
    for entry in docs_uncovered:
        parts = entry['filepath'].split('/')
        if len(parts) >= 2:
            subdir = parts[1]
            docs_by_subdir[subdir].append(entry)

    for subdir in sorted(docs_by_subdir.keys()):
        entries = docs_by_subdir[subdir]
        content.append(f"#### docs/{subdir}/ ({len(entries)} files)")
        content.append("")

        for entry in entries[:10]:  # Show first 10
            size_kb = int(entry['size_bytes']) / 1024
            content.append(f"- **{Path(entry['filepath']).name}** ({size_kb:.1f} KB)")

        if len(entries) > 10:
            content.append(f"- ... and {len(entries) - 10} more")

        content.append("")

    content.extend([
        "---",
        "",
        "### Examples Directory",
        ""
    ])

    # Examples directory
    examples_uncovered = [
        e for e in analysis["uncovered_files"]
        if e['filepath'].startswith('examples/')
    ]

    if examples_uncovered:
        content.append(f"**Total uncovered**: {len(examples_uncovered)} files")
        content.append("")
        content.append("**Action needed**: Determine if examples should be:")
        content.append("- Covered by SAP-003 (project-bootstrap) as reference examples")
        content.append("- Archived as obsolete")
        content.append("- Kept as-is (intentionally outside SAP coverage)")
        content.append("")
    else:
        content.append("*(No uncovered examples)*")
        content.append("")

    output_path.write_text("\n".join(content))
    print(f"✅ High-priority review list generated: {output_path}")


def main():
    print("Phase 2: SAP Coverage Mapping")
    print("=" * 60)
    print()

    # Analyze coverage
    print("Analyzing coverage gaps...")
    analysis = analyze_coverage_gaps()
    print(f"✅ Found {len(analysis['uncovered_files'])} uncovered files")
    print()

    # Generate reports
    inventory_dir = ROOT / "docs/inventory"
    inventory_dir.mkdir(parents=True, exist_ok=True)

    generate_coverage_matrix(analysis, inventory_dir / "sap-coverage-matrix.md")
    generate_uncovered_report(analysis, inventory_dir / "uncovered-files-detailed.md")
    generate_high_priority_review(analysis, inventory_dir / "high-priority-review.md")

    print()
    print("=" * 60)
    print("Phase 2 Complete!")
    print()
    print("Next steps:")
    print("1. Review high-priority-review.md for immediate actions")
    print("2. Review sap-coverage-matrix.md to understand SAP coverage")
    print("3. Review uncovered-files-detailed.md for full uncovered list")
    print("4. Proceed to Phase 3: Line-by-line content audit")


if __name__ == "__main__":
    main()
