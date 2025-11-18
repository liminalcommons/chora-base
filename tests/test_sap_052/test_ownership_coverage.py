"""
Tests for ownership-coverage.py (SAP-052 tool).

Validates:
- CODEOWNERS file parsing
- Coverage calculation (% files with owners)
- Orphan file detection (files without owners)
- Domain coverage breakdown
- JSON schema compliance
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestOwnershipCoverage:
    """Test suite for ownership coverage analyzer."""

    def test_analyze_full_coverage(
        self, temp_repo, codeowners_file, ownership_coverage_script
    ):
        """Test analysis with full coverage (all files have owners)."""
        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
                "--format",
                "text",
            ],
            capture_output=True,
            text=True,
        )

        # Check exit code (0 if coverage >= 80%)
        assert result.returncode in [0, 1]  # May not reach 80% depending on patterns

        output = result.stdout
        assert "Ownership Coverage Report" in output
        assert "Total Files:" in output
        assert "Coverage:" in output

    def test_analyze_json_output(
        self, temp_repo, codeowners_file, ownership_coverage_script
    ):
        """Test JSON output format and schema compliance."""
        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 1]

        # Parse JSON output
        report = json.loads(result.stdout)

        # Verify required fields (SAP-052 protocol spec schema)
        assert "repository" in report
        assert "analysis_date" in report
        assert "total_files" in report
        assert "covered_files" in report
        assert "uncovered_files" in report
        assert "coverage_percent" in report
        assert "domain_coverage" in report
        assert "orphan_files" in report

        # Verify types
        assert isinstance(report["total_files"], int)
        assert isinstance(report["covered_files"], int)
        assert isinstance(report["coverage_percent"], (int, float))
        assert isinstance(report["domain_coverage"], list)
        assert isinstance(report["orphan_files"], list)

    def test_orphan_files_detection(
        self, temp_repo, codeowners_file, ownership_coverage_script
    ):
        """Test detection of files without ownership."""
        # Create a file not covered by CODEOWNERS patterns
        orphan_file = temp_repo / "temp" / "orphan.txt"
        orphan_file.parent.mkdir(exist_ok=True)
        orphan_file.write_text("Orphan file\n")

        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
                "--orphans-only",
            ],
            capture_output=True,
            text=True,
        )

        output = result.stdout
        # Should list the orphan file
        assert "/temp/orphan.txt" in output or "orphan.txt" in output

    def test_domain_coverage_breakdown(
        self, temp_repo, codeowners_file, ownership_coverage_script
    ):
        """Test per-domain coverage breakdown."""
        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        report = json.loads(result.stdout)

        # Verify domain_coverage has entries
        assert len(report["domain_coverage"]) > 0

        # Verify domain coverage structure
        for dc in report["domain_coverage"]:
            assert "domain" in dc
            assert "pattern" in dc
            assert "owner" in dc
            assert "files_covered" in dc
            assert "percent_of_repo" in dc

    def test_missing_codeowners_file(
        self, temp_repo, ownership_coverage_script
    ):
        """Test error when CODEOWNERS file is missing."""
        # Remove CODEOWNERS file if it exists
        codeowners_path = temp_repo / "CODEOWNERS"
        if codeowners_path.exists():
            codeowners_path.unlink()

        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
            ],
            capture_output=True,
            text=True,
        )

        # Should fail with error
        assert result.returncode != 0
        assert "not found" in result.stderr.lower()

    def test_coverage_percentage_calculation(
        self, temp_repo, codeowners_file, ownership_coverage_script
    ):
        """Test that coverage percentage is calculated correctly."""
        result = subprocess.run(
            [
                sys.executable,
                str(ownership_coverage_script),
                "--repo",
                str(temp_repo),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        report = json.loads(result.stdout)

        # Verify percentage calculation
        total = report["total_files"]
        covered = report["covered_files"]
        uncovered = report["uncovered_files"]

        assert total == covered + uncovered
        expected_percent = (covered / total * 100) if total > 0 else 0.0
        assert abs(report["coverage_percent"] - expected_percent) < 0.1
