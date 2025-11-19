#!/usr/bin/env python3
"""
SAP-053 Conflict Resolution - Conflict Detection Script

Pre-merge conflict detection via git merge simulation.

Usage:
    python conflict-checker.py [--branch BRANCH] [--json] [--verbose]

Returns:
    Exit code 0: No conflicts detected (safe to merge)
    Exit code 1: Conflicts detected (manual review required)
    Exit code 2: Conflicts detected (auto-resolvable)
    Exit code 3: Error during detection

Author: Claude (Anthropic)
Created: 2025-11-19
SAP: SAP-053 (Conflict Resolution)
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ConflictType(Enum):
    """Classification of merge conflict types."""
    CONTENT = "content"                # Substantive changes (code, docs)
    WHITESPACE = "whitespace"          # Whitespace/formatting only
    FORMATTING = "formatting"          # Auto-fixable formatting (black, prettier)
    LOCKFILE = "lockfile"              # Dependency lockfiles
    METADATA = "metadata"              # Git metadata, cache files
    UNKNOWN = "unknown"                # Cannot determine type


class ResolutionStrategy(Enum):
    """Recommended resolution strategies."""
    MANUAL_REVIEW = "manual_review"
    MANUAL_REVIEW_WITH_OWNERSHIP = "manual_review_with_ownership"
    SCHEMA_DRIVEN_MERGE = "schema_driven_merge"
    REGENERATE_FROM_SOURCE = "regenerate_from_source"
    DELETE_AND_REGENERATE = "delete_and_regenerate"
    AUTO_RESOLVE_FORMATTING = "auto_resolve_formatting"


@dataclass
class ConflictBlock:
    """Represents a conflict block within a file."""
    file: str
    start_line: int
    end_line: int
    ours_content: str
    theirs_content: str
    base_content: Optional[str] = None


@dataclass
class ConflictReport:
    """Complete conflict detection report."""
    has_conflicts: bool
    safe_to_merge: bool
    branch: str
    target_branch: str
    timestamp: str
    conflicting_files: List[str]
    conflict_types: Dict[str, str]
    resolution_strategies: Dict[str, str]
    auto_resolvable: bool
    auto_resolvable_files: List[str]
    manual_review_files: List[str]
    total_files: int
    total_conflicts: int
    detection_method: str = "git_merge_simulation"

    def to_dict(self) -> dict:
        """Convert report to dictionary."""
        return asdict(self)


class ConflictChecker:
    """Pre-merge conflict detection via git merge simulation."""

    def __init__(self, branch: str = "main", verbose: bool = False):
        self.branch = branch
        self.verbose = verbose
        self.repo_root = self._find_repo_root()

    def _find_repo_root(self) -> Path:
        """Find git repository root."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error: Not in a git repository: {e}", file=sys.stderr)
            sys.exit(3)

    def _run_git_command(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run git command and return result."""
        if self.verbose:
            print(f"Running: git {' '.join(args)}", file=sys.stderr)

        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=False,
            cwd=self.repo_root
        )

        if check and result.returncode != 0:
            print(f"Git command failed: {result.stderr}", file=sys.stderr)

        return result

    def _get_target_branch_ref(self) -> Optional[str]:
        """
        Get the full ref for the target branch (try origin/branch first, then local branch).

        Returns:
            Branch ref string or None if not found
        """
        # Try remote branch first
        remote_check = self._run_git_command(
            ["rev-parse", "--verify", f"origin/{self.branch}"],
            check=False
        )
        if remote_check.returncode == 0:
            return f"origin/{self.branch}"

        # Fall back to local branch
        local_check = self._run_git_command(
            ["rev-parse", "--verify", self.branch],
            check=False
        )
        if local_check.returncode == 0:
            return self.branch

        return None

    def validate_preconditions(self) -> Tuple[bool, Optional[str]]:
        """
        Validate preconditions for conflict checking.

        Returns:
            (is_valid, error_message)
        """
        # Check if repository is clean
        status = self._run_git_command(["status", "--porcelain"])
        if status.stdout.strip():
            return False, "Working directory has uncommitted changes. Commit or stash changes first."

        # Check if target branch exists (remote or local)
        target_ref = self._get_target_branch_ref()
        if not target_ref:
            return False, f"Target branch '{self.branch}' does not exist (checked origin/{self.branch} and {self.branch})."

        # Get current branch
        current_branch = self._run_git_command(
            ["rev-parse", "--abbrev-ref", "HEAD"]
        )
        if current_branch.stdout.strip() == self.branch:
            return False, f"Already on target branch '{self.branch}'. Cannot check for conflicts."

        return True, None

    def check_for_conflicts(self) -> ConflictReport:
        """
        Main conflict detection algorithm via git merge simulation.

        Returns:
            ConflictReport with detection results
        """
        # Step 1: Validate preconditions
        is_valid, error_msg = self.validate_preconditions()
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(3)

        # Get current branch
        current_result = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        current_branch = current_result.stdout.strip()

        # Get target branch reference (remote or local)
        target_ref = self._get_target_branch_ref()

        # Step 2: Fetch latest from remote (if remote branch exists)
        if target_ref.startswith("origin/"):
            if self.verbose:
                print(f"Fetching latest from {target_ref}...", file=sys.stderr)

            self._run_git_command(["fetch", "origin", self.branch], check=False)

        # Step 3: Attempt test merge (no-commit, no-ff)
        if self.verbose:
            print(f"Simulating merge of {current_branch} into {target_ref}...", file=sys.stderr)

        merge_result = self._run_git_command(
            ["merge", "--no-commit", "--no-ff", target_ref],
            check=False
        )

        # Step 4: Parse results
        if merge_result.returncode == 0:
            # No conflicts - clean merge
            self._run_git_command(["merge", "--abort"], check=False)

            return ConflictReport(
                has_conflicts=False,
                safe_to_merge=True,
                branch=current_branch,
                target_branch=self.branch,
                timestamp=datetime.utcnow().isoformat() + "Z",
                conflicting_files=[],
                conflict_types={},
                resolution_strategies={},
                auto_resolvable=True,
                auto_resolvable_files=[],
                manual_review_files=[],
                total_files=0,
                total_conflicts=0
            )
        else:
            # Conflicts detected
            conflicting_files = self._parse_conflicting_files()
            conflict_types = self._classify_conflicts(conflicting_files)
            resolution_strategies = self._determine_resolution_strategies(conflict_types)

            # Determine auto-resolvable files
            auto_resolvable_strategies = {
                ResolutionStrategy.REGENERATE_FROM_SOURCE.value,
                ResolutionStrategy.DELETE_AND_REGENERATE.value,
                ResolutionStrategy.AUTO_RESOLVE_FORMATTING.value,
                ResolutionStrategy.SCHEMA_DRIVEN_MERGE.value
            }

            auto_resolvable_files = [
                f for f, strategy in resolution_strategies.items()
                if strategy in auto_resolvable_strategies
            ]

            manual_review_files = [
                f for f in conflicting_files
                if f not in auto_resolvable_files
            ]

            # Abort test merge
            self._run_git_command(["merge", "--abort"])

            return ConflictReport(
                has_conflicts=True,
                safe_to_merge=False,
                branch=current_branch,
                target_branch=self.branch,
                timestamp=datetime.utcnow().isoformat() + "Z",
                conflicting_files=conflicting_files,
                conflict_types=conflict_types,
                resolution_strategies=resolution_strategies,
                auto_resolvable=len(auto_resolvable_files) == len(conflicting_files),
                auto_resolvable_files=auto_resolvable_files,
                manual_review_files=manual_review_files,
                total_files=len(conflicting_files),
                total_conflicts=len(conflicting_files)
            )

    def _parse_conflicting_files(self) -> List[str]:
        """Parse list of files with merge conflicts from git status."""
        status = self._run_git_command(["status", "--porcelain"])

        conflicting_files = []
        for line in status.stdout.split('\n'):
            if line.startswith('UU '):  # Both modified (unmerged)
                file_path = line[3:].strip()
                conflicting_files.append(file_path)

        return conflicting_files

    def _classify_conflicts(self, files: List[str]) -> Dict[str, str]:
        """
        Classify conflict type for each file.

        Returns:
            Dict mapping file path to ConflictType
        """
        classifications = {}

        for file_path in files:
            conflict_type = self._classify_single_file(file_path)
            classifications[file_path] = conflict_type.value

        return classifications

    def _classify_single_file(self, file_path: str) -> ConflictType:
        """Classify conflict type for a single file."""
        # Lockfiles
        lockfile_patterns = [
            'package-lock.json',
            'yarn.lock',
            'poetry.lock',
            'Pipfile.lock',
            'Gemfile.lock',
            'Cargo.lock'
        ]
        if any(pattern in file_path for pattern in lockfile_patterns):
            return ConflictType.LOCKFILE

        # Metadata files
        metadata_patterns = [
            '.DS_Store',
            '__pycache__',
            '.pyc',
            '.egg-info',
            'node_modules',
            '.cache',
            'dist/',
            'build/'
        ]
        if any(pattern in file_path for pattern in metadata_patterns):
            return ConflictType.METADATA

        # Try to read conflict markers to determine type
        try:
            full_path = self.repo_root / file_path
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check if only whitespace/formatting differences
            if self._is_whitespace_conflict(content):
                return ConflictType.WHITESPACE

            # Check if formatting conflict (can be auto-fixed)
            if self._is_formatting_conflict(file_path, content):
                return ConflictType.FORMATTING

            # Default to content conflict
            return ConflictType.CONTENT

        except Exception:
            return ConflictType.UNKNOWN

    def _is_whitespace_conflict(self, content: str) -> bool:
        """Check if conflict is only whitespace differences."""
        # Extract ours and theirs sections
        ours_pattern = r'<<<<<<< HEAD\n(.*?)\n======='
        theirs_pattern = r'=======\n(.*?)\n>>>>>>>'

        ours_matches = re.findall(ours_pattern, content, re.DOTALL)
        theirs_matches = re.findall(theirs_pattern, content, re.DOTALL)

        if not ours_matches or not theirs_matches:
            return False

        # Compare normalized content (remove all whitespace)
        for ours, theirs in zip(ours_matches, theirs_matches):
            ours_normalized = re.sub(r'\s+', '', ours)
            theirs_normalized = re.sub(r'\s+', '', theirs)

            if ours_normalized != theirs_normalized:
                return False

        return True

    def _is_formatting_conflict(self, file_path: str, content: str) -> bool:
        """Check if conflict can be auto-resolved with formatters."""
        # File extensions that can be auto-formatted
        auto_format_extensions = {
            '.py': 'black/ruff',
            '.js': 'prettier',
            '.ts': 'prettier',
            '.jsx': 'prettier',
            '.tsx': 'prettier',
            '.json': 'prettier',
            '.css': 'prettier',
            '.scss': 'prettier'
        }

        ext = Path(file_path).suffix
        return ext in auto_format_extensions

    def _determine_resolution_strategies(
        self,
        conflict_types: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Determine resolution strategy for each file based on conflict type.

        Returns:
            Dict mapping file path to ResolutionStrategy
        """
        strategies = {}

        for file_path, conflict_type in conflict_types.items():
            strategy = self._select_strategy(file_path, ConflictType(conflict_type))
            strategies[file_path] = strategy.value

        return strategies

    def _select_strategy(self, file_path: str, conflict_type: ConflictType) -> ResolutionStrategy:
        """Select resolution strategy for a single file."""
        # Strategy selection based on conflict type
        if conflict_type == ConflictType.LOCKFILE:
            return ResolutionStrategy.REGENERATE_FROM_SOURCE

        elif conflict_type == ConflictType.METADATA:
            return ResolutionStrategy.DELETE_AND_REGENERATE

        elif conflict_type == ConflictType.WHITESPACE:
            return ResolutionStrategy.AUTO_RESOLVE_FORMATTING

        elif conflict_type == ConflictType.FORMATTING:
            return ResolutionStrategy.AUTO_RESOLVE_FORMATTING

        elif conflict_type == ConflictType.CONTENT:
            # Check file type for content conflicts
            ext = Path(file_path).suffix

            if ext == '.md':
                return ResolutionStrategy.MANUAL_REVIEW

            elif ext in ['.py', '.ts', '.js', '.jsx', '.tsx']:
                return ResolutionStrategy.MANUAL_REVIEW_WITH_OWNERSHIP

            elif ext in ['.yaml', '.yml', '.json']:
                return ResolutionStrategy.SCHEMA_DRIVEN_MERGE

            else:
                return ResolutionStrategy.MANUAL_REVIEW

        else:  # UNKNOWN
            return ResolutionStrategy.MANUAL_REVIEW


def format_text_report(report: ConflictReport) -> str:
    """Format conflict report as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("SAP-053 Conflict Detection Report")
    lines.append("=" * 60)
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append(f"Branch: {report.branch}")
    lines.append(f"Target: {report.target_branch}")
    lines.append(f"Detection Method: {report.detection_method}")
    lines.append("")

    if not report.has_conflicts:
        lines.append("✅ NO CONFLICTS DETECTED")
        lines.append("")
        lines.append("Status: Safe to merge")
        lines.append("Action: You can create a pull request or merge directly")
    else:
        lines.append("⚠️  CONFLICTS DETECTED")
        lines.append("")
        lines.append(f"Total Files with Conflicts: {report.total_files}")
        lines.append(f"Auto-Resolvable: {len(report.auto_resolvable_files)}")
        lines.append(f"Manual Review Required: {len(report.manual_review_files)}")
        lines.append("")

        if report.auto_resolvable_files:
            lines.append("Auto-Resolvable Files:")
            for file in report.auto_resolvable_files:
                strategy = report.resolution_strategies[file]
                lines.append(f"  - {file} ({strategy})")
            lines.append("")

        if report.manual_review_files:
            lines.append("Manual Review Required:")
            for file in report.manual_review_files:
                conflict_type = report.conflict_types[file]
                strategy = report.resolution_strategies[file]
                lines.append(f"  - {file}")
                lines.append(f"    Type: {conflict_type}")
                lines.append(f"    Strategy: {strategy}")
            lines.append("")

        lines.append("Next Steps:")
        if report.auto_resolvable_files:
            lines.append("  1. Run: just conflict-auto-resolve")
        if report.manual_review_files:
            lines.append(f"  {'2' if report.auto_resolvable_files else '1'}. Manually resolve conflicts in files above")
            lines.append(f"  {'3' if report.auto_resolvable_files else '2'}. Run: git add <resolved-files>")
            lines.append(f"  {'4' if report.auto_resolvable_files else '3'}. Run: git commit")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """Main entry point for conflict-checker."""
    parser = argparse.ArgumentParser(
        description="SAP-053 Pre-merge conflict detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check for conflicts against main branch
  python conflict-checker.py

  # Check against specific branch
  python conflict-checker.py --branch develop

  # Get JSON output for automation
  python conflict-checker.py --json

  # Verbose mode for debugging
  python conflict-checker.py --verbose

Exit Codes:
  0 - No conflicts (safe to merge)
  1 - Conflicts detected (manual review required)
  2 - Conflicts detected (all auto-resolvable)
  3 - Error during detection
        """
    )

    parser.add_argument(
        '--branch',
        default='main',
        help='Target branch to check conflicts against (default: main)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )

    args = parser.parse_args()

    # Run conflict detection
    checker = ConflictChecker(branch=args.branch, verbose=args.verbose)
    report = checker.check_for_conflicts()

    # Output results
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(format_text_report(report))

    # Exit with appropriate code
    if not report.has_conflicts:
        sys.exit(0)
    elif report.auto_resolvable:
        sys.exit(2)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
