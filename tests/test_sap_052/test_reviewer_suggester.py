"""
Tests for reviewer-suggester.py (SAP-052 tool).

Validates:
- Reviewer suggestion based on changed files
- Single-domain jurisdiction
- Multi-domain jurisdiction (cross-domain conflicts)
- Escalation for files without owners
- JSON output format
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestReviewerSuggester:
    """Test suite for reviewer suggester tool."""

    def test_suggest_single_domain(
        self, temp_repo, codeowners_file, reviewer_suggester_script
    ):
        """Test reviewer suggestion for single-domain change."""
        # Create a branch with docs-only changes
        subprocess.run(
            ["git", "checkout", "-b", "feature/update-docs"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )

        # Modify a file in docs domain
        (temp_repo / "docs" / "new-doc.md").write_text("# New Doc\n")
        subprocess.run(
            ["git", "add", "docs/new-doc.md"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Add new doc"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )

        # Run suggester
        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--base",
                "main",
                "--head",
                "feature/update-docs",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        suggestion = json.loads(result.stdout)

        # Verify single-domain jurisdiction
        assert suggestion["jurisdiction_type"] == "single_domain"
        assert len(suggestion["domains_touched"]) == 1
        assert "docs" in suggestion["domains_touched"]
        assert "@alice" in suggestion["reviewers"]

    def test_suggest_multi_domain(
        self, temp_repo, codeowners_file, reviewer_suggester_script
    ):
        """Test reviewer suggestion for multi-domain change."""
        # Create a branch with changes in multiple domains
        subprocess.run(
            ["git", "checkout", "-b", "feature/refactor"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )

        # Modify files in different domains
        (temp_repo / "docs" / "refactor.md").write_text("# Refactor\n")
        (temp_repo / "scripts" / "refactor.py").write_text("# Refactor script\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Refactor across domains"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )

        # Run suggester
        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--base",
                "main",
                "--head",
                "feature/refactor",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        suggestion = json.loads(result.stdout)

        # Verify multi-domain jurisdiction
        assert suggestion["jurisdiction_type"] == "multi_domain"
        assert len(suggestion["domains_touched"]) > 1
        assert suggestion["is_cross_domain"] is True

        # Should include both owners
        assert "@alice" in suggestion["reviewers"]
        assert "@bob" in suggestion["reviewers"]

    def test_suggest_specific_files(
        self, temp_repo, codeowners_file, reviewer_suggester_script
    ):
        """Test reviewer suggestion for specific files (no git diff)."""
        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--files",
                "docs/README.md",
                "scripts/validate.py",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        suggestion = json.loads(result.stdout)

        # Should suggest reviewers for both files
        assert "@alice" in suggestion["reviewers"]
        assert "@bob" in suggestion["reviewers"]
        assert suggestion["is_cross_domain"] is True

    def test_suggest_text_output(
        self, temp_repo, codeowners_file, reviewer_suggester_script
    ):
        """Test human-readable text output format."""
        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--files",
                "docs/README.md",
                "--format",
                "text",
            ],
            capture_output=True,
            text=True,
        )

        output = result.stdout

        # Verify text format
        assert "Reviewer Suggestion" in output
        assert "Suggested Reviewers:" in output
        assert "Domains Touched:" in output
        assert "Jurisdiction:" in output

    def test_no_files_changed(
        self, temp_repo, codeowners_file, reviewer_suggester_script
    ):
        """Test behavior when no files are changed."""
        # Create empty branch (no changes)
        subprocess.run(
            ["git", "checkout", "-b", "feature/empty"],
            cwd=temp_repo,
            check=True,
            capture_output=True,
        )

        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--base",
                "main",
                "--head",
                "feature/empty",
            ],
            capture_output=True,
            text=True,
        )

        # Should exit with 0 (no error, just no files)
        assert result.returncode == 0
        assert "No files changed" in result.stderr or "No files changed" in result.stdout

    def test_missing_codeowners_file(
        self, temp_repo, reviewer_suggester_script
    ):
        """Test error when CODEOWNERS file is missing."""
        # Remove CODEOWNERS file
        (temp_repo / "CODEOWNERS").unlink()

        result = subprocess.run(
            [
                sys.executable,
                str(reviewer_suggester_script),
                "--repo",
                str(temp_repo),
                "--files",
                "docs/README.md",
            ],
            capture_output=True,
            text=True,
        )

        # Should fail with error
        assert result.returncode != 0
        assert "not found" in result.stderr.lower()
