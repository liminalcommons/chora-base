#!/usr/bin/env python3
"""
Comprehensive file inventory script for chora-base.

This script catalogs every file in chora-base, categorizes it by type,
identifies which SAP (if any) it relates to, and generates detailed reports.

Usage:
    python scripts/inventory-chora-base.py

Outputs:
    - docs/inventory/file-inventory.csv
    - docs/inventory/directory-structure.md
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# File extensions to inventory
EXTENSIONS = {
    ".md", ".py", ".yml", ".yaml", ".sh", ".toml", ".txt",
    ".json", ".cfg", ".ini", ".env.example", ".blueprint"
}

# Special files without extensions
SPECIAL_FILES = {
    "Dockerfile", "Dockerfile.test", "justfile",
    ".dockerignore", ".gitignore", ".gitattributes",
    "LICENSE", "MANIFEST.in"
}

# Directories to exclude
EXCLUDE_DIRS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "node_modules", "venv", ".venv",
    "dist", "build", "*.egg-info", ".DS_Store",
    "test-output",  # Temp directory
    # Phase 2 exclusions: Examples are intentionally outside SAP coverage (templates)
    "examples"
}

# SAP mappings (based on SAP protocol-specs)
SAP_MAPPINGS = {
    "SAP-000": {
        "patterns": [
            "docs/reference/skilled-awareness/sap-framework/",
            "SKILLED_AWARENESS_PACKAGE_PROTOCOL.md",
            # Phase 2 additions: SAP planning and audit artifacts
            "docs/reference/skilled-awareness/INDEX.md",
            "docs/reference/skilled-awareness/quality-gates.md",
            "docs/reference/skilled-awareness/inputs-audit.md",
            "docs/reference/skilled-awareness/chora-base-sap-roadmap.md",
            "docs/reference/skilled-awareness/document-templates.md",
            "docs/reference/skilled-awareness/workflow-mapping.md",
            "docs/reference/skilled-awareness/copier-audit.md",
            # Phase 2 additions: Inventory reports (meta-SAP documentation)
            "docs/inventory/"
        ]
    },
    "SAP-001": {
        "patterns": [
            "inbox/",
            "docs/reference/skilled-awareness/inbox/"
        ]
    },
    "SAP-002": {
        "patterns": [
            "docs/reference/skilled-awareness/chora-base/",
            "README.md",
            "CHANGELOG.md",
            # Phase 2 additions: Root-level documentation
            "AGENTS.md",
            "CLAUDE_SETUP_GUIDE.md",
            # Phase 2 additions: Ecosystem/architecture docs
            "docs/reference/ecosystem/",
            # Phase 2 additions: Integration plans
            "docs/integration/",
            # Phase 2 additions: Release notes
            "docs/releases/",
            # Phase 2 additions: static-template roadmap
            "static-template/ROADMAP.md"
        ]
    },
    "SAP-003": {
        "patterns": [
            "blueprints/",
            "docs/reference/skilled-awareness/project-bootstrap/",
            "scripts/generate_project.py",
            # Phase 2 additions: .gitignore files
            ".gitignore",
            "static-template/.gitignore"
        ]
    },
    "SAP-004": {
        "patterns": [
            "static-template/tests/",
            "static-template/conftest.py",
            "static-template/pytest.ini",
            "docs/reference/skilled-awareness/testing-framework/"
        ]
    },
    "SAP-005": {
        "patterns": [
            "static-template/.github/workflows/",
            "static-template/.github/dependabot.yml",
            "docs/reference/skilled-awareness/ci-cd-workflows/"
        ]
    },
    "SAP-006": {
        "patterns": [
            "static-template/.pre-commit-config.yaml",
            "static-template/.ruff.toml",
            "docs/reference/skilled-awareness/quality-gates/"
        ]
    },
    "SAP-007": {
        "patterns": [
            "static-template/DOCUMENTATION_STANDARD.md",
            "static-template/user-docs/",
            "static-template/dev-docs/",
            "static-template/project-docs/",
            "docs/reference/skilled-awareness/documentation-framework/",
            # Phase 2 additions: Root docs/ files
            "docs/BENEFITS.md",
            "docs/DOCUMENTATION_PLAN.md",
            # Phase 2 additions: Research documents
            "docs/research/",
            # Phase 2 additions: static-template documentation
            "static-template/PYPI_SETUP.md",
            "static-template/NAMESPACES.md",
            "static-template/UPGRADING.md",
            # Phase 2 additions: Docs/reference guides
            "docs/reference/writing-executable-howtos.md"
        ]
    },
    "SAP-008": {
        "patterns": [
            "static-template/scripts/",
            "static-template/justfile",
            "docs/reference/skilled-awareness/automation-scripts/",
            # Phase 2 additions: Utility scripts
            "scripts/rollback-migration.sh",
            "scripts/inventory-chora-base.py",
            "scripts/fix-shell-syntax.sh",
            "scripts/analyze-coverage-gaps.py",
            # Phase 2 additions: Root-level utility scripts
            "repo-dump.py",
            "setup.py"
        ]
    },
    "SAP-009": {
        "patterns": [
            "static-template/AGENTS.md",
            "static-template/CLAUDE.md",
            "blueprints/AGENTS.md.blueprint",
            "blueprints/CLAUDE.md.blueprint",
            "claude/",
            "docs/reference/skilled-awareness/agent-awareness/",
            "AGENT_SETUP_GUIDE.md"
        ]
    },
    "SAP-010": {
        "patterns": [
            "static-template/.chora/memory/",
            "docs/reference/skilled-awareness/memory-system/",
            # Phase 2 additions: Template memory system code
            "static-template/src/{{package_name}}/memory/",
            "static-template/src/__package_name__/memory/"
        ]
    },
    "SAP-011": {
        "patterns": [
            "static-template/Dockerfile",
            "static-template/Dockerfile.test",
            "static-template/docker-compose.yml",
            "static-template/.dockerignore",
            "static-template/DOCKER_BEST_PRACTICES.md",
            "docs/reference/skilled-awareness/docker-operations/",
            # Phase 2 additions: Docker documentation
            "static-template/docker/"
        ]
    },
    "SAP-012": {
        "patterns": [
            "static-template/dev-docs/workflows/",
            "docs/reference/skilled-awareness/development-lifecycle/"
        ]
    },
    "SAP-013": {
        "patterns": [
            "static-template/src/__package_name__/utils/claude_metrics.py",
            "static-template/project-docs/metrics/",
            "docs/reference/skilled-awareness/metrics-tracking/"
        ]
    },
    # Catch-all for template source code utilities
    "SAP-TEMPLATE-UTILS": {
        "patterns": [
            "static-template/src/{{package_name}}/utils/",
            "static-template/src/__package_name__/utils/"
        ]
    }
}


def categorize_file(filepath: Path) -> str:
    """Categorize file by type."""
    if filepath.suffix == ".md":
        return "documentation"
    elif filepath.suffix in {".py", ".sh"}:
        return "code"
    elif filepath.suffix in {".yml", ".yaml", ".toml", ".json", ".cfg", ".ini"}:
        return "config"
    elif filepath.name in {"Dockerfile", "Dockerfile.test", ".dockerignore"}:
        return "docker"
    elif filepath.name in {"justfile", ".gitignore", ".gitattributes"}:
        return "tooling"
    elif ".blueprint" in filepath.name:
        return "template"
    else:
        return "other"


def identify_sap(filepath: Path, root: Path) -> List[str]:
    """Identify which SAP(s) this file relates to."""
    relative_path = filepath.relative_to(root)
    related_saps = []

    for sap_id, config in SAP_MAPPINGS.items():
        for pattern in config["patterns"]:
            if pattern in str(relative_path):
                related_saps.append(sap_id)
                break

    return related_saps


def get_file_status(saps: List[str]) -> str:
    """Determine file status based on SAP coverage."""
    if len(saps) > 0:
        return "covered"
    else:
        return "uncovered"


def scan_directory(root: Path) -> List[Dict]:
    """Scan directory and return list of file metadata."""
    files_data = []

    for filepath in root.rglob("*"):
        # Skip if not a file
        if not filepath.is_file():
            continue

        # Skip excluded directories
        if any(excluded in filepath.parts for excluded in EXCLUDE_DIRS):
            continue

        # Check if file should be inventoried
        should_inventory = False
        if filepath.suffix in EXTENSIONS:
            should_inventory = True
        elif filepath.name in SPECIAL_FILES:
            should_inventory = True
        elif any(special in filepath.name for special in SPECIAL_FILES):
            should_inventory = True

        if not should_inventory:
            continue

        # Get file metadata
        stat = filepath.stat()
        relative_path = filepath.relative_to(root)
        category = categorize_file(filepath)
        related_saps = identify_sap(filepath, root)
        status = get_file_status(related_saps)

        files_data.append({
            "filepath": str(relative_path),
            "type": category,
            "size_bytes": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "related_saps": ",".join(related_saps) if related_saps else "None",
            "status": status
        })

    return files_data


def generate_csv_report(files_data: List[Dict], output_path: Path):
    """Generate CSV inventory report."""
    fieldnames = ["filepath", "type", "size_bytes", "last_modified", "related_saps", "status"]

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(files_data)

    print(f"✅ CSV report generated: {output_path}")


def generate_directory_structure(root: Path, output_path: Path):
    """Generate directory structure markdown."""
    lines = ["# Chora-Base Directory Structure\n"]
    lines.append(f"**Generated**: {datetime.now().isoformat()}\n")
    lines.append("---\n\n")

    def walk_directory(path: Path, prefix: str = "", is_last: bool = True):
        """Recursively walk directory and generate tree."""
        if path.name in EXCLUDE_DIRS:
            return

        # Count files in this directory
        try:
            items = sorted([p for p in path.iterdir() if p.name not in EXCLUDE_DIRS])
        except PermissionError:
            return

        dirs = [p for p in items if p.is_dir()]
        files = [p for p in items if p.is_file()]

        # Directory summary
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}**{path.name}/** ({len(files)} files, {len(dirs)} subdirs)\n")

        # Recursively walk subdirectories (limit depth to 3)
        if prefix.count("│") < 3:
            extension = "    " if is_last else "│   "
            for i, subdir in enumerate(dirs):
                walk_directory(subdir, prefix + extension, i == len(dirs) - 1)

    lines.append("```\n")
    lines.append("chora-base/\n")

    # Walk from root
    try:
        items = sorted([p for p in root.iterdir() if p.name not in EXCLUDE_DIRS and p.name != ".git"])
        dirs = [p for p in items if p.is_dir()]

        for i, subdir in enumerate(dirs):
            walk_directory(subdir, "", i == len(dirs) - 1)
    except Exception as e:
        lines.append(f"Error: {e}\n")

    lines.append("```\n")

    with output_path.open("w") as f:
        f.writelines(lines)

    print(f"✅ Directory structure generated: {output_path}")


def generate_summary_stats(files_data: List[Dict], output_path: Path):
    """Generate summary statistics."""
    total_files = len(files_data)
    covered = len([f for f in files_data if f["status"] == "covered"])
    uncovered = len([f for f in files_data if f["status"] == "uncovered"])

    by_type = {}
    for file_data in files_data:
        ftype = file_data["type"]
        by_type[ftype] = by_type.get(ftype, 0) + 1

    by_sap = {}
    for file_data in files_data:
        saps = file_data["related_saps"]
        if saps != "None":
            for sap in saps.split(","):
                by_sap[sap] = by_sap.get(sap, 0) + 1

    lines = ["# Inventory Summary Statistics\n\n"]
    lines.append(f"**Generated**: {datetime.now().isoformat()}\n\n")
    lines.append("---\n\n")

    lines.append("## Overall Statistics\n\n")
    lines.append(f"- **Total files inventoried**: {total_files}\n")
    lines.append(f"- **Covered by SAPs**: {covered} ({covered/total_files*100:.1f}%)\n")
    lines.append(f"- **Uncovered**: {uncovered} ({uncovered/total_files*100:.1f}%)\n\n")

    lines.append("## By File Type\n\n")
    lines.append("| Type | Count | % of Total |\n")
    lines.append("|------|-------|------------|\n")
    for ftype, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {ftype} | {count} | {count/total_files*100:.1f}% |\n")

    lines.append("\n## By SAP\n\n")
    lines.append("| SAP | Files Covered | % of Total |\n")
    lines.append("|-----|---------------|------------|\n")
    for sap, count in sorted(by_sap.items()):
        lines.append(f"| {sap} | {count} | {count/total_files*100:.1f}% |\n")

    lines.append(f"\n**Note**: {uncovered} files ({uncovered/total_files*100:.1f}%) are not currently associated with any SAP.\n")

    with output_path.open("w") as f:
        f.writelines(lines)

    print(f"✅ Summary statistics generated: {output_path}")


def main():
    """Main execution."""
    print("Starting chora-base inventory...")
    print(f"Root directory: {ROOT_DIR}")

    # Scan all files
    print("\n📂 Scanning directories...")
    files_data = scan_directory(ROOT_DIR)
    print(f"Found {len(files_data)} files to inventory")

    # Generate outputs
    output_dir = ROOT_DIR / "docs" / "inventory"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n📊 Generating reports...")
    generate_csv_report(files_data, output_dir / "file-inventory.csv")
    generate_directory_structure(ROOT_DIR, output_dir / "directory-structure.md")
    generate_summary_stats(files_data, output_dir / "inventory-summary.md")

    print("\n✅ Inventory complete!")
    print(f"\nOutputs:")
    print(f"  - {output_dir / 'file-inventory.csv'}")
    print(f"  - {output_dir / 'directory-structure.md'}")
    print(f"  - {output_dir / 'inventory-summary.md'}")


if __name__ == "__main__":
    main()
