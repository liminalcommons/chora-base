#!/usr/bin/env python3
"""
Ownership Coverage Analyzer

Analyzes CODEOWNERS file coverage and generates detailed metrics reports.
Part of SAP-052 (Ownership Zones) infrastructure.

Usage:
    # Analyze current repository
    python ownership-coverage.py

    # Analyze specific repository
    python ownership-coverage.py --repo /path/to/repo

    # Generate JSON report
    python ownership-coverage.py --format json --output coverage-report.json

    # Show orphan files only
    python ownership-coverage.py --orphans-only

    # Include git history for last-modified dates
    python ownership-coverage.py --include-git-history

Features:
- Parses CODEOWNERS file using gitignore-style pattern matching
- Calculates ownership coverage percentage (files with assigned owners)
- Identifies orphan files (no matching ownership pattern)
- Per-domain coverage breakdown
- Suggests owners for orphan files (based on git blame)
- JSON schema-compliant output (SAP-052 protocol spec)

References:
- SAP-052: docs/skilled-awareness/ownership-zones/
- Protocol Spec: docs/skilled-awareness/ownership-zones/protocol-spec.md
- Coverage Schema: protocol-spec.md § Ownership Coverage Report Schema
"""

import argparse
import fnmatch
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class OwnershipPattern:
    """Represents a single ownership pattern from CODEOWNERS."""

    pattern: str
    owners: List[str]
    line_number: int
    is_directory: bool = False
    is_wildcard: bool = False

    def __post_init__(self):
        self.is_directory = self.pattern.endswith("/")
        self.is_wildcard = "*" in self.pattern or "?" in self.pattern


@dataclass
class DomainCoverage:
    """Coverage metrics for a single domain."""

    domain: str
    pattern: str
    owner: str
    files_covered: int
    percent_of_repo: float = 0.0
    avg_review_time_hours: Optional[float] = None


@dataclass
class OrphanFile:
    """File without assigned ownership."""

    path: str
    size_bytes: int = 0
    last_modified: Optional[str] = None
    suggested_owner: Optional[str] = None


@dataclass
class CoverageReport:
    """Complete ownership coverage report."""

    repository: str
    analysis_date: str
    total_files: int
    covered_files: int
    uncovered_files: int
    coverage_percent: float
    domain_coverage: List[DomainCoverage] = field(default_factory=list)
    orphan_files: List[OrphanFile] = field(default_factory=list)


class CodeownersParser:
    """Parses CODEOWNERS file and matches file paths to ownership patterns."""

    def __init__(self, codeowners_path: Path):
        """Initialize parser with CODEOWNERS file path."""
        self.codeowners_path = codeowners_path
        self.patterns: List[OwnershipPattern] = []
        self._parse()

    def _parse(self) -> None:
        """Parse CODEOWNERS file into ownership patterns."""
        if not self.codeowners_path.exists():
            raise FileNotFoundError(
                f"CODEOWNERS file not found: {self.codeowners_path}"
            )

        with open(self.codeowners_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                # Skip comments and blank lines
                if not line or line.startswith("#"):
                    continue

                # Parse pattern and owners
                parts = line.split()
                if len(parts) < 2:
                    continue  # Invalid line, skip

                pattern = parts[0]
                owners = parts[1:]

                self.patterns.append(
                    OwnershipPattern(
                        pattern=pattern, owners=owners, line_number=line_num
                    )
                )

    def find_owners(self, file_path: str) -> Optional[List[str]]:
        """Find owners for a file path.

        Args:
            file_path: File path relative to repository root

        Returns:
            List of owners (last matching pattern wins), or None if no match
        """
        # Normalize path (ensure leading /)
        if not file_path.startswith("/"):
            file_path = "/" + file_path

        matched_owners = None

        # Iterate patterns (last match wins)
        for pattern_obj in self.patterns:
            pattern = pattern_obj.pattern

            # Handle directory patterns (/docs/ matches /docs/anything)
            if pattern_obj.is_directory:
                if file_path.startswith(pattern):
                    matched_owners = pattern_obj.owners
                    continue

            # Handle wildcard patterns (*.md, /scripts/*.py)
            if pattern_obj.is_wildcard:
                if fnmatch.fnmatch(file_path, pattern):
                    matched_owners = pattern_obj.owners
                    continue

            # Handle exact match
            if file_path == pattern:
                matched_owners = pattern_obj.owners
                continue

        return matched_owners

    def get_domain_patterns(self) -> Dict[str, List[OwnershipPattern]]:
        """Group patterns by domain (heuristic based on pattern prefix).

        Returns:
            Dict mapping domain names to their patterns
        """
        domains = {}
        for pattern_obj in self.patterns:
            # Extract domain from pattern (e.g., /docs/ -> docs)
            pattern = pattern_obj.pattern
            if pattern.startswith("/"):
                domain = pattern.split("/")[1] if len(pattern.split("/")) > 1 else "root"
            else:
                domain = "wildcard"

            if domain not in domains:
                domains[domain] = []
            domains[domain].append(pattern_obj)

        return domains


class OwnershipCoverageAnalyzer:
    """Analyzes ownership coverage for a repository."""

    def __init__(
        self,
        repo_path: Path,
        include_git_history: bool = False,
        ignore_patterns: Optional[List[str]] = None,
    ):
        """Initialize analyzer.

        Args:
            repo_path: Path to repository root
            include_git_history: If True, fetch git history for last-modified dates
            ignore_patterns: File patterns to exclude from analysis
        """
        self.repo_path = repo_path
        self.include_git_history = include_git_history
        # Default ignore patterns (can be overridden with ignore_patterns argument)
        default_ignores = [
            ".git/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "node_modules/",
            ".venv/",
            "venv/",
            "env/",
            ".env/",
            "test-integration*/",  # Test virtual environments
            "*/site-packages/*",   # Python packages
            "*/Lib/*",             # Python library files (Windows)
            "*/Scripts/*",         # Python scripts (Windows venv)
            "*/bin/*",             # Binary files (Unix venv)
            ".tox/",
            ".pytest_cache/",
            ".mypy_cache/",
            ".coverage",
            "htmlcov/",
            "dist/",
            "build/",
            "*.egg-info/",
        ]
        self.ignore_patterns = ignore_patterns if ignore_patterns is not None else default_ignores

        codeowners_path = repo_path / "CODEOWNERS"
        self.parser = CodeownersParser(codeowners_path)

    def _should_ignore(self, file_path: str) -> bool:
        """Check if file should be ignored based on ignore patterns.

        Supports glob patterns including:
        - Simple wildcards: *.pyc, test_*.py
        - Directory patterns: node_modules/, dist/
        - Recursive globs: **/node_modules/**, **/dist/**
        """
        from pathlib import PurePath

        path = PurePath(file_path)

        for pattern in self.ignore_patterns:
            # Try glob pattern matching with PurePath.match()
            # This supports ** for recursive matching
            try:
                if path.match(pattern):
                    return True
            except ValueError:
                # Invalid pattern, skip it
                pass

            # Also try with ** prefix/suffix for directory patterns
            # e.g., "node_modules/" → "**/node_modules/**"
            if pattern.endswith("/"):
                # Directory pattern - match anywhere in path
                dir_name = pattern.rstrip("/")
                recursive_pattern = f"**/{dir_name}/**"
                try:
                    if path.match(recursive_pattern):
                        return True
                except ValueError:
                    pass

                # Also check if any path component matches exactly
                # e.g., "node_modules/" matches "/foo/node_modules/bar.js"
                if dir_name in path.parts:
                    return True

        return False

    def _get_all_files(self) -> List[Path]:
        """Get all files in repository (excluding ignored patterns)."""
        all_files = []
        for path in self.repo_path.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(self.repo_path).as_posix()
                if not self._should_ignore(rel_path):
                    all_files.append(path)
        return all_files

    def _get_file_last_modified(self, file_path: Path) -> Optional[str]:
        """Get last modified date from git history."""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ci", str(file_path)],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                # Parse git date (e.g., "2025-11-17 14:30:00 -0800")
                git_date = result.stdout.strip().split()[0]
                return git_date
        except Exception:
            pass
        return None

    def _suggest_owner_from_git(self, file_path: Path) -> Optional[str]:
        """Suggest owner based on git blame (most frequent committer)."""
        try:
            result = subprocess.run(
                ["git", "blame", "--line-porcelain", str(file_path)],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                # Count authors
                authors = {}
                for line in result.stdout.split("\n"):
                    if line.startswith("author "):
                        author = line.replace("author ", "").strip()
                        authors[author] = authors.get(author, 0) + 1

                # Return most frequent author
                if authors:
                    most_frequent = max(authors.items(), key=lambda x: x[1])
                    return f"@{most_frequent[0].replace(' ', '').lower()}"
        except Exception:
            pass
        return None

    def analyze(self) -> CoverageReport:
        """Analyze ownership coverage and generate report."""
        all_files = self._get_all_files()
        total_files = len(all_files)

        covered_files_set: Set[str] = set()
        orphan_files = []
        domain_file_counts: Dict[str, int] = {}

        # Analyze each file
        for file_path in all_files:
            rel_path = "/" + file_path.relative_to(self.repo_path).as_posix()
            owners = self.parser.find_owners(rel_path)

            if owners:
                covered_files_set.add(rel_path)
                # Increment domain count (heuristic: first path component)
                domain = rel_path.split("/")[1] if len(rel_path.split("/")) > 1 else "root"
                domain_file_counts[domain] = domain_file_counts.get(domain, 0) + 1
            else:
                # Orphan file
                size_bytes = file_path.stat().st_size if file_path.exists() else 0
                last_modified = None
                suggested_owner = None

                if self.include_git_history:
                    last_modified = self._get_file_last_modified(file_path)
                    suggested_owner = self._suggest_owner_from_git(file_path)

                orphan_files.append(
                    OrphanFile(
                        path=rel_path,
                        size_bytes=size_bytes,
                        last_modified=last_modified,
                        suggested_owner=suggested_owner,
                    )
                )

        covered_files = len(covered_files_set)
        uncovered_files = total_files - covered_files
        coverage_percent = (covered_files / total_files * 100) if total_files > 0 else 0.0

        # Build domain coverage breakdown
        domain_coverage = []
        domain_patterns = self.parser.get_domain_patterns()
        for domain, patterns in domain_patterns.items():
            files_covered = domain_file_counts.get(domain, 0)
            percent_of_repo = (files_covered / total_files * 100) if total_files > 0 else 0.0

            # Get primary owner (first owner of first pattern)
            owner = patterns[0].owners[0] if patterns and patterns[0].owners else "@unknown"

            domain_coverage.append(
                DomainCoverage(
                    domain=domain,
                    pattern=patterns[0].pattern if patterns else "",
                    owner=owner,
                    files_covered=files_covered,
                    percent_of_repo=round(percent_of_repo, 1),
                )
            )

        # Create report
        report = CoverageReport(
            repository=self.repo_path.name,
            analysis_date=datetime.utcnow().isoformat() + "Z",
            total_files=total_files,
            covered_files=covered_files,
            uncovered_files=uncovered_files,
            coverage_percent=round(coverage_percent, 1),
            domain_coverage=domain_coverage,
            orphan_files=orphan_files,
        )

        return report


def format_report_text(report: CoverageReport) -> str:
    """Format coverage report as human-readable text."""
    lines = [
        "=" * 70,
        "Ownership Coverage Report",
        "=" * 70,
        f"Repository: {report.repository}",
        f"Analysis Date: {report.analysis_date}",
        "",
        "Summary:",
        f"  Total Files: {report.total_files}",
        f"  Covered Files: {report.covered_files}",
        f"  Uncovered Files: {report.uncovered_files}",
        f"  Coverage: {report.coverage_percent}%",
        "",
    ]

    # Domain coverage breakdown
    if report.domain_coverage:
        lines.append("Domain Coverage:")
        for dc in report.domain_coverage:
            lines.append(
                f"  {dc.domain:20s} {dc.owner:20s} {dc.files_covered:4d} files ({dc.percent_of_repo:5.1f}%)"
            )
        lines.append("")

    # Orphan files
    if report.orphan_files:
        lines.append(f"Orphan Files ({len(report.orphan_files)}):")
        for orphan in report.orphan_files[:20]:  # Limit to first 20
            suggested = f" [suggest: {orphan.suggested_owner}]" if orphan.suggested_owner else ""
            lines.append(f"  {orphan.path}{suggested}")
        if len(report.orphan_files) > 20:
            lines.append(f"  ... and {len(report.orphan_files) - 20} more")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


def format_report_json(report: CoverageReport) -> str:
    """Format coverage report as JSON (schema-compliant)."""
    # Convert dataclasses to dicts
    report_dict = {
        "repository": report.repository,
        "analysis_date": report.analysis_date,
        "total_files": report.total_files,
        "covered_files": report.covered_files,
        "uncovered_files": report.uncovered_files,
        "coverage_percent": report.coverage_percent,
        "domain_coverage": [
            {
                "domain": dc.domain,
                "pattern": dc.pattern,
                "owner": dc.owner,
                "files_covered": dc.files_covered,
                "percent_of_repo": dc.percent_of_repo,
            }
            for dc in report.domain_coverage
        ],
        "orphan_files": [
            {
                "path": of.path,
                "size_bytes": of.size_bytes,
                **({"last_modified": of.last_modified} if of.last_modified else {}),
                **({"suggested_owner": of.suggested_owner} if of.suggested_owner else {}),
            }
            for of in report.orphan_files
        ],
    }
    return json.dumps(report_dict, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze CODEOWNERS coverage and generate metrics reports (SAP-052)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current repository
  %(prog)s

  # Analyze specific repository
  %(prog)s --repo /path/to/repo

  # Generate JSON report
  %(prog)s --format json --output coverage-report.json

  # Show orphan files only
  %(prog)s --orphans-only

  # Include git history for suggestions
  %(prog)s --include-git-history
        """,
    )

    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository path (default: current directory)",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)",
    )

    parser.add_argument(
        "--orphans-only",
        action="store_true",
        help="Show only orphan files (no coverage summary)",
    )

    parser.add_argument(
        "--include-git-history",
        action="store_true",
        help="Include git history (last modified, suggested owner from git blame)",
    )

    parser.add_argument(
        "--ignore",
        nargs="+",
        help="Additional file patterns to ignore (e.g., *.log temp/)",
    )

    args = parser.parse_args()

    try:
        # Validate repository
        if not (args.repo / "CODEOWNERS").exists():
            print(
                f"Error: CODEOWNERS file not found in {args.repo}",
                file=sys.stderr,
            )
            return 1

        # Run analysis
        analyzer = OwnershipCoverageAnalyzer(
            repo_path=args.repo,
            include_git_history=args.include_git_history,
            ignore_patterns=args.ignore,
        )
        report = analyzer.analyze()

        # Format output
        if args.orphans_only:
            if args.format == "json":
                output = json.dumps([asdict(of) for of in report.orphan_files], indent=2)
            else:
                output = "\n".join([of.path for of in report.orphan_files])
        else:
            if args.format == "json":
                output = format_report_json(report)
            else:
                output = format_report_text(report)

        # Write output
        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"Report written to: {args.output}", file=sys.stderr)
        else:
            print(output)

        # Exit code: 0 if coverage >= 80%, 1 otherwise
        return 0 if report.coverage_percent >= 80.0 else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
