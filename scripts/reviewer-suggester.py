#!/usr/bin/env python3
"""
Reviewer Suggester Tool

Suggests PR reviewers based on CODEOWNERS file and changed files in a PR.
Part of SAP-052 (Ownership Zones) infrastructure.

Usage:
    # Suggest reviewers for current branch vs main
    python reviewer-suggester.py

    # Suggest for specific branch
    python reviewer-suggester.py --branch feature/add-docs

    # Suggest for specific files
    python reviewer-suggester.py --files docs/vision/mcp.md scripts/validate.py

    # Compare two branches
    python reviewer-suggester.py --base main --head feature/refactor

    # JSON output for automation
    python reviewer-suggester.py --format json

Features:
- Analyzes changed files in PR/branch
- Matches files to CODEOWNERS patterns
- Suggests reviewers based on file ownership
- Detects cross-domain conflicts (multiple owners collaborate)
- Handles conflict jurisdiction rules (SAP-052 Contract 4)
- Provides human-readable and JSON output

Conflict Jurisdiction Rules (SAP-052):
- Single domain: Domain owner has jurisdiction
- Multiple domains: All owners collaborate (consensus required)
- Deadlock: Escalate to project lead

References:
- SAP-052: docs/skilled-awareness/ownership-zones/
- Protocol Spec: docs/skilled-awareness/ownership-zones/protocol-spec.md
- Awareness Guide: docs/skilled-awareness/ownership-zones/awareness-guide.md
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

# Reuse CodeownersParser from ownership-coverage.py
sys.path.insert(0, str(Path(__file__).parent))
try:
    from ownership_coverage import CodeownersParser
except ImportError:
    # Fallback: minimal parser for standalone use
    class CodeownersParser:
        """Minimal CODEOWNERS parser (fallback if ownership_coverage.py not available)."""

        def __init__(self, codeowners_path: Path):
            self.patterns = []
            with open(codeowners_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        self.patterns.append({"pattern": parts[0], "owners": parts[1:]})

        def find_owners(self, file_path: str) -> Optional[List[str]]:
            """Find owners for file path (last matching pattern wins)."""
            if not file_path.startswith("/"):
                file_path = "/" + file_path
            matched_owners = None
            for p in self.patterns:
                pattern = p["pattern"]
                if pattern.endswith("/") and file_path.startswith(pattern):
                    matched_owners = p["owners"]
                elif file_path == pattern or ("*" in pattern and self._match_wildcard(pattern, file_path)):
                    matched_owners = p["owners"]
            return matched_owners

        def _match_wildcard(self, pattern: str, path: str) -> bool:
            """Simple wildcard matching."""
            import fnmatch
            return fnmatch.fnmatch(path, pattern)


@dataclass
class ReviewerSuggestion:
    """Suggested reviewers with justification."""

    reviewers: List[str]
    domains_touched: List[str]
    files_per_domain: Dict[str, List[str]]
    is_cross_domain: bool
    jurisdiction_type: str  # "single_domain", "multi_domain", "escalation"
    justification: str


class ReviewerSuggester:
    """Suggests reviewers based on changed files and CODEOWNERS."""

    def __init__(self, repo_path: Path, codeowners_path: Optional[Path] = None):
        """Initialize suggester.

        Args:
            repo_path: Path to repository root
            codeowners_path: Path to CODEOWNERS file (default: repo_path/CODEOWNERS)
        """
        self.repo_path = repo_path
        self.codeowners_path = codeowners_path or (repo_path / "CODEOWNERS")

        if not self.codeowners_path.exists():
            raise FileNotFoundError(
                f"CODEOWNERS file not found: {self.codeowners_path}"
            )

        self.parser = CodeownersParser(self.codeowners_path)

    def get_changed_files_git(
        self, base_branch: str = "main", head_branch: Optional[str] = None
    ) -> List[str]:
        """Get changed files between two branches using git diff.

        Args:
            base_branch: Base branch (default: main)
            head_branch: Head branch (default: current branch)

        Returns:
            List of changed file paths
        """
        try:
            if head_branch:
                # Compare base...head
                cmd = ["git", "diff", "--name-only", f"{base_branch}...{head_branch}"]
            else:
                # Compare base...current
                cmd = ["git", "diff", "--name-only", base_branch]

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                raise RuntimeError(f"git diff failed: {result.stderr}")

            files = [
                line.strip()
                for line in result.stdout.strip().split("\n")
                if line.strip()
            ]
            return files

        except Exception as e:
            raise RuntimeError(f"Failed to get changed files: {e}")

    def suggest_reviewers(
        self, changed_files: List[str]
    ) -> ReviewerSuggestion:
        """Suggest reviewers based on changed files.

        Args:
            changed_files: List of file paths that changed

        Returns:
            ReviewerSuggestion with suggested reviewers and justification
        """
        if not changed_files:
            return ReviewerSuggestion(
                reviewers=[],
                domains_touched=[],
                files_per_domain={},
                is_cross_domain=False,
                jurisdiction_type="none",
                justification="No files changed",
            )

        # Map files to owners and domains
        owner_to_files: Dict[str, List[str]] = defaultdict(list)
        domain_to_files: Dict[str, List[str]] = defaultdict(list)
        unowned_files: List[str] = []

        for file_path in changed_files:
            owners = self.parser.find_owners(file_path)

            if owners:
                for owner in owners:
                    owner_to_files[owner].append(file_path)

                # Extract domain (heuristic: first path component)
                domain = self._extract_domain(file_path)
                domain_to_files[domain].append(file_path)
            else:
                unowned_files.append(file_path)

        # Determine jurisdiction type and suggested reviewers
        unique_owners = list(owner_to_files.keys())
        domains_touched = list(domain_to_files.keys())
        is_cross_domain = len(domains_touched) > 1

        if not unique_owners:
            # No owners found for any files
            return ReviewerSuggestion(
                reviewers=[],
                domains_touched=domains_touched,
                files_per_domain=dict(domain_to_files),
                is_cross_domain=is_cross_domain,
                jurisdiction_type="escalation",
                justification=f"No owners assigned for {len(unowned_files)} changed files. Escalate to project lead.",
            )

        if len(domains_touched) == 1:
            # Single domain - domain owner has jurisdiction
            jurisdiction_type = "single_domain"
            justification = (
                f"All changes are in the '{domains_touched[0]}' domain. "
                f"Domain owner(s) have jurisdiction."
            )
        else:
            # Multiple domains - all owners collaborate
            jurisdiction_type = "multi_domain"
            justification = (
                f"Changes span {len(domains_touched)} domains ({', '.join(domains_touched)}). "
                f"All domain owners must collaborate (consensus required)."
            )

        # Add warning for unowned files
        if unowned_files:
            justification += f" Warning: {len(unowned_files)} files have no assigned owner."

        return ReviewerSuggestion(
            reviewers=unique_owners,
            domains_touched=domains_touched,
            files_per_domain=dict(domain_to_files),
            is_cross_domain=is_cross_domain,
            jurisdiction_type=jurisdiction_type,
            justification=justification,
        )

    def _extract_domain(self, file_path: str) -> str:
        """Extract domain from file path (heuristic).

        Args:
            file_path: File path (e.g., /docs/vision/mcp.md)

        Returns:
            Domain name (e.g., docs)
        """
        # Remove leading /
        if file_path.startswith("/"):
            file_path = file_path[1:]

        # Get first path component
        parts = file_path.split("/")
        return parts[0] if parts else "root"


def format_suggestion_text(suggestion: ReviewerSuggestion) -> str:
    """Format reviewer suggestion as human-readable text."""
    lines = [
        "=" * 70,
        "Reviewer Suggestion (SAP-052)",
        "=" * 70,
        "",
    ]

    if not suggestion.reviewers:
        lines.append("⚠️  No reviewers found!")
        lines.append(f"Reason: {suggestion.justification}")
        lines.append("")
        lines.append("Action: Assign reviewers manually or update CODEOWNERS file.")
    else:
        lines.append("Suggested Reviewers:")
        for reviewer in suggestion.reviewers:
            lines.append(f"  • {reviewer}")
        lines.append("")

        lines.append("Domains Touched:")
        for domain in suggestion.domains_touched:
            file_count = len(suggestion.files_per_domain[domain])
            lines.append(f"  • {domain} ({file_count} files)")
        lines.append("")

        lines.append("Jurisdiction:")
        if suggestion.jurisdiction_type == "single_domain":
            lines.append("  ✓ Single domain - domain owner has jurisdiction")
        elif suggestion.jurisdiction_type == "multi_domain":
            lines.append("  ⚠️  Multiple domains - all owners must collaborate")
        elif suggestion.jurisdiction_type == "escalation":
            lines.append("  ⚠️  No owners assigned - escalate to project lead")
        lines.append("")

        lines.append("Justification:")
        lines.append(f"  {suggestion.justification}")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_suggestion_json(suggestion: ReviewerSuggestion) -> str:
    """Format reviewer suggestion as JSON."""
    data = {
        "reviewers": suggestion.reviewers,
        "domains_touched": suggestion.domains_touched,
        "files_per_domain": suggestion.files_per_domain,
        "is_cross_domain": suggestion.is_cross_domain,
        "jurisdiction_type": suggestion.jurisdiction_type,
        "justification": suggestion.justification,
    }
    return json.dumps(data, indent=2)


def main():
    # Fix Windows encoding issues - force UTF-8 output
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7 fallback
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    parser = argparse.ArgumentParser(
        description="Suggest PR reviewers based on CODEOWNERS file (SAP-052)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Suggest reviewers for current branch vs main
  %(prog)s

  # Suggest for specific branch
  %(prog)s --branch feature/add-docs

  # Suggest for specific files
  %(prog)s --files docs/vision/mcp.md scripts/validate.py

  # Compare two branches
  %(prog)s --base main --head feature/refactor

  # JSON output for automation
  %(prog)s --format json
        """,
    )

    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository path (default: current directory)",
    )

    parser.add_argument(
        "--base",
        default="main",
        help="Base branch for comparison (default: main)",
    )

    parser.add_argument(
        "--head",
        help="Head branch for comparison (default: current branch)",
    )

    parser.add_argument(
        "--branch",
        help="Branch to analyze (shorthand for --head)",
    )

    parser.add_argument(
        "--files",
        nargs="+",
        help="Specific files to analyze (instead of git diff)",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    try:
        # Resolve head branch
        head_branch = args.head or args.branch

        # Initialize suggester
        suggester = ReviewerSuggester(repo_path=args.repo)

        # Get changed files
        if args.files:
            changed_files = args.files
        else:
            changed_files = suggester.get_changed_files_git(
                base_branch=args.base, head_branch=head_branch
            )

        if not changed_files:
            print("No files changed.", file=sys.stderr)
            return 0

        # Suggest reviewers
        suggestion = suggester.suggest_reviewers(changed_files)

        # Format output
        if args.format == "json":
            print(format_suggestion_json(suggestion))
        else:
            print(format_suggestion_text(suggestion))

        # Exit code: 0 if reviewers found, 1 otherwise
        return 0 if suggestion.reviewers else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
