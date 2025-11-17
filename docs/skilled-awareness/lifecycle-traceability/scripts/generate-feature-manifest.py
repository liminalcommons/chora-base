#!/usr/bin/env python3
"""
Feature Manifest Generator for SAP-056 (Lifecycle Traceability)

Auto-generates feature entries by scanning:
- Git log for commits with feature markers
- Beads tasks for [Feature: FEAT-XXX] tags
- Test files for pytest markers (@pytest.mark.feature)
- Documentation for frontmatter feature_id

Usage:
    python generate-feature-manifest.py [--feature FEAT-XXX] [--output feature-manifest.yaml]

Options:
    --feature FEAT-XXX  Generate entry for specific feature only
    --output FILE       Output file (default: feature-manifest.yaml)
    --append            Append to existing manifest (don't overwrite)
    --git-log DAYS      Parse git log for last N days (default: 90)
    --beads-db PATH     Path to beads database (default: .beads/beads.db)
    --dry-run           Show what would be generated without writing

Exit Codes:
    0 - Success
    1 - Warnings (manifest generated but incomplete)
    2 - Fatal error
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


@dataclass
class FeatureData:
    """Collected data for a single feature."""
    feature_id: str
    name: str = ""
    vision_ref: str = ""
    status: str = "in_progress"
    requirements: List[Dict] = field(default_factory=list)
    code_files: Set[str] = field(default_factory=set)
    test_files: Set[str] = field(default_factory=set)
    doc_files: Set[str] = field(default_factory=set)
    git_commits: List[str] = field(default_factory=list)
    beads_tasks: List[str] = field(default_factory=list)

    def to_manifest_entry(self) -> dict:
        """Convert to feature-manifest.yaml entry."""
        return {
            "id": self.feature_id,
            "name": self.name or f"Feature {self.feature_id}",
            "vision_ref": self.vision_ref or "TBD",
            "status": self.status,
            "requirements": self.requirements,
            "code": [{"path": path} for path in sorted(self.code_files)],
            "tests": [
                {"path": path, "type": "unit" if "/test_" in path else "integration"}
                for path in sorted(self.test_files)
            ],
            "documentation": [
                {"path": path, "type": "how-to"}
                for path in sorted(self.doc_files)
            ]
        }


class ManifestGenerator:
    """Generator for feature-manifest.yaml from git/beads/tests/docs."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.features: Dict[str, FeatureData] = {}

    def scan_git_log(self, days: int = 90):
        """Scan git log for feature references in commits."""
        print(f"Scanning git log (last {days} days)...")

        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        try:
            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--pretty=format:%H|%s"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            for line in result.stdout.splitlines():
                if "|" not in line:
                    continue

                commit_hash, commit_msg = line.split("|", 1)

                # Extract feature ID from commit message
                # Patterns: [FEAT-XXX], (FEAT-XXX), FEAT-XXX:
                pattern = r'\[?(FEAT-[A-Z0-9-]+)\]?'
                matches = re.findall(pattern, commit_msg, re.IGNORECASE)

                for feature_id in matches:
                    feature_id = feature_id.upper()
                    if feature_id not in self.features:
                        self.features[feature_id] = FeatureData(feature_id=feature_id)
                    self.features[feature_id].git_commits.append(commit_hash[:7])

                    # Try to extract feature name from commit message
                    # Pattern: feat(scope): Add feature name [FEAT-XXX]
                    name_pattern = r'feat\([^)]+\):\s*(.+?)\s*\[?FEAT-'
                    name_match = re.search(name_pattern, commit_msg, re.IGNORECASE)
                    if name_match and not self.features[feature_id].name:
                        self.features[feature_id].name = name_match.group(1).strip()

            print(f"  Found {len(self.features)} features from git log")

        except subprocess.CalledProcessError as e:
            print(f"  Warning: Git log parsing failed: {e}", file=sys.stderr)
        except FileNotFoundError:
            print(f"  Warning: Git not found or not in a git repository", file=sys.stderr)

    def scan_beads_tasks(self, beads_db: Optional[str] = None):
        """Scan beads tasks for [Feature: FEAT-XXX] tags."""
        print("Scanning beads tasks...")

        beads_jsonl = self.project_root / ".beads" / "issues.jsonl"
        if not beads_jsonl.exists():
            print("  Warning: Beads database not found (.beads/issues.jsonl)")
            return

        try:
            with open(beads_jsonl, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        task = json.loads(line.strip())
                        title = task.get("title", "")
                        notes = " ".join(task.get("notes", []))

                        # Extract feature ID from title or notes
                        # Pattern: [Feature: FEAT-XXX] or [FEAT-XXX]
                        pattern = r'\[(?:Feature:\s*)?(FEAT-[A-Z0-9-]+)\]'
                        matches = re.findall(pattern, title + " " + notes, re.IGNORECASE)

                        for feature_id in matches:
                            feature_id = feature_id.upper()
                            if feature_id not in self.features:
                                self.features[feature_id] = FeatureData(feature_id=feature_id)
                            self.features[feature_id].beads_tasks.append(task.get("id", ""))

                            # Extract feature name from title
                            # Pattern: [FEAT-XXX] Feature Name
                            name_pattern = r'\[FEAT-[A-Z0-9-]+\]\s*(.+)'
                            name_match = re.search(name_pattern, title, re.IGNORECASE)
                            if name_match and not self.features[feature_id].name:
                                self.features[feature_id].name = name_match.group(1).strip()

                    except json.JSONDecodeError:
                        continue

            print(f"  Found features in {len([f for f in self.features.values() if f.beads_tasks])} beads tasks")

        except Exception as e:
            print(f"  Warning: Beads scanning failed: {e}", file=sys.stderr)

    def scan_test_files(self):
        """Scan test files for @pytest.mark.feature markers."""
        print("Scanning test files...")

        test_files = list(self.project_root.glob("tests/**/test_*.py"))
        features_found = set()

        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract feature markers
                # Pattern: @pytest.mark.feature("FEAT-XXX")
                pattern = r'@pytest\.mark\.feature\(["\']?(FEAT-[A-Z0-9-]+)["\']?\)'
                matches = re.findall(pattern, content, re.IGNORECASE)

                for feature_id in matches:
                    feature_id = feature_id.upper()
                    if feature_id not in self.features:
                        self.features[feature_id] = FeatureData(feature_id=feature_id)

                    # Add test file to feature
                    rel_path = test_file.relative_to(self.project_root)
                    self.features[feature_id].test_files.add(str(rel_path))
                    features_found.add(feature_id)

            except Exception as e:
                print(f"  Warning: Failed to parse {test_file}: {e}", file=sys.stderr)

        print(f"  Found {len(features_found)} features in test markers")

    def scan_documentation(self):
        """Scan documentation for frontmatter feature_id."""
        print("Scanning documentation...")

        doc_files = (
            list(self.project_root.glob("docs/**/*.md")) +
            list(self.project_root.glob("*.md"))
        )
        features_found = set()

        for doc_file in doc_files:
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract frontmatter
                if not content.startswith("---"):
                    continue

                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                frontmatter = yaml.safe_load(parts[1])
                if not frontmatter:
                    continue

                # Extract feature_id or feature_ids
                feature_ids = []
                if "feature_id" in frontmatter:
                    feature_ids.append(frontmatter["feature_id"])
                if "feature_ids" in frontmatter:
                    feature_ids.extend(frontmatter["feature_ids"])

                for feature_id in feature_ids:
                    feature_id = feature_id.upper()
                    if feature_id not in self.features:
                        self.features[feature_id] = FeatureData(feature_id=feature_id)

                    # Add doc file to feature
                    rel_path = doc_file.relative_to(self.project_root)
                    self.features[feature_id].doc_files.add(str(rel_path))
                    features_found.add(feature_id)

                    # Extract code_references from frontmatter
                    code_refs = frontmatter.get("code_references", [])
                    for code_ref in code_refs:
                        self.features[feature_id].code_files.add(code_ref)

            except Exception as e:
                print(f"  Warning: Failed to parse frontmatter in {doc_file}: {e}", file=sys.stderr)

        print(f"  Found {len(features_found)} features in documentation frontmatter")

    def scan_all(self, git_days: int = 90):
        """Run all scanners."""
        self.scan_git_log(days=git_days)
        self.scan_beads_tasks()
        self.scan_test_files()
        self.scan_documentation()

        print(f"\nTotal features discovered: {len(self.features)}")

    def generate_manifest(self, feature_filter: Optional[str] = None) -> dict:
        """Generate feature-manifest.yaml structure."""
        features_list = []

        for feature_id, feature_data in sorted(self.features.items()):
            if feature_filter and feature_id != feature_filter:
                continue

            features_list.append(feature_data.to_manifest_entry())

        return {
            "version": "1.0.0",
            "project": self.project_root.name,
            "features": features_list
        }

    def merge_with_existing(self, existing_path: Path, new_manifest: dict) -> dict:
        """Merge generated manifest with existing manifest."""
        try:
            with open(existing_path, 'r', encoding='utf-8') as f:
                existing = yaml.safe_load(f)
        except FileNotFoundError:
            return new_manifest

        # Merge features (existing takes precedence for fields, but add new code/tests/docs)
        existing_features = {f["id"]: f for f in existing.get("features", [])}
        new_features = {f["id"]: f for f in new_manifest.get("features", [])}

        merged_features = {}

        # Keep existing features (with updates from new)
        for feature_id, existing_feature in existing_features.items():
            merged_feature = existing_feature.copy()

            if feature_id in new_features:
                new_feature = new_features[feature_id]

                # Merge code files
                existing_code = {c["path"] for c in existing_feature.get("code", [])}
                new_code = {c["path"] for c in new_feature.get("code", [])}
                merged_code = existing_code | new_code
                merged_feature["code"] = [{"path": path} for path in sorted(merged_code)]

                # Merge test files
                existing_tests = {t["path"] for t in existing_feature.get("tests", [])}
                new_tests = {t["path"] for t in new_feature.get("tests", [])}
                merged_tests = existing_tests | new_tests
                merged_feature["tests"] = [
                    {"path": path, "type": "unit" if "/test_" in path else "integration"}
                    for path in sorted(merged_tests)
                ]

                # Merge docs
                existing_docs = {d["path"] for d in existing_feature.get("documentation", [])}
                new_docs = {d["path"] for d in new_feature.get("documentation", [])}
                merged_docs = existing_docs | new_docs
                merged_feature["documentation"] = [
                    {"path": path, "type": "how-to"}
                    for path in sorted(merged_docs)
                ]

            merged_features[feature_id] = merged_feature

        # Add new features not in existing
        for feature_id, new_feature in new_features.items():
            if feature_id not in existing_features:
                merged_features[feature_id] = new_feature

        return {
            "version": existing.get("version", "1.0.0"),
            "project": existing.get("project", self.project_root.name),
            "features": [merged_features[fid] for fid in sorted(merged_features.keys())]
        }


def main():
    parser = argparse.ArgumentParser(
        description="Auto-generate feature-manifest.yaml from git/beads/tests/docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--feature",
        metavar="FEAT-XXX",
        help="Generate entry for specific feature only"
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default="feature-manifest.yaml",
        help="Output file (default: feature-manifest.yaml)"
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Merge with existing manifest (don't overwrite)"
    )
    parser.add_argument(
        "--git-log",
        metavar="DAYS",
        type=int,
        default=90,
        help="Parse git log for last N days (default: 90)"
    )
    parser.add_argument(
        "--beads-db",
        metavar="PATH",
        help="Path to beads database (default: .beads/beads.db)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing"
    )

    args = parser.parse_args()

    # Generate manifest
    generator = ManifestGenerator()
    generator.scan_all(git_days=args.git_log)

    manifest = generator.generate_manifest(feature_filter=args.feature)

    # Merge with existing if --append
    output_path = Path(args.output)
    if args.append and output_path.exists():
        print(f"\nMerging with existing manifest: {output_path}")
        manifest = generator.merge_with_existing(output_path, manifest)

    # Output
    if args.dry_run:
        print("\n" + "="*80)
        print("DRY RUN - Generated Manifest:")
        print("="*80)
        print(yaml.dump(manifest, sort_keys=False, default_flow_style=False))
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(manifest, f, sort_keys=False, default_flow_style=False)
        print(f"\nManifest written to {output_path}")
        print(f"  Features: {len(manifest['features'])}")
        print(f"  Total code files: {sum(len(f.get('code', [])) for f in manifest['features'])}")
        print(f"  Total tests: {sum(len(f.get('tests', [])) for f in manifest['features'])}")
        print(f"  Total docs: {sum(len(f.get('documentation', [])) for f in manifest['features'])}")

    sys.exit(0)


if __name__ == "__main__":
    main()
