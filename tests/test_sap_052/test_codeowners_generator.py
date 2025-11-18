"""
Tests for codeowners-generator.py (SAP-052 tool).

Validates:
- Template generation (chora-workspace, generic)
- Single owner assignment
- Multiple owner assignment
- Team ownership
- Pattern validation
- Output format (comments, patterns, owners)
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestCodeownersGenerator:
    """Test suite for CODEOWNERS template generator."""

    def test_generate_chora_workspace_template(
        self, temp_repo, codeowners_generator_script
    ):
        """Test generating chora-workspace template with single owner."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--owner",
                "@victorpiper",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify header
        assert "# CODEOWNERS" in output
        assert "SAP-052" in output

        # Verify domain patterns
        assert "/docs/ @victorpiper" in output
        assert "/scripts/ @victorpiper" in output
        assert "/inbox/ @victorpiper" in output
        assert "/.chora/ @victorpiper" in output
        assert "/project-docs/ @victorpiper" in output

        # Verify shared files
        assert "/AGENTS.md @victorpiper" in output
        assert "/CLAUDE.md @victorpiper" in output

    def test_generate_generic_template(self, temp_repo, codeowners_generator_script):
        """Test generating generic template."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "generic",
                "--owner",
                "@alice",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify generic patterns
        assert "/docs/ @alice" in output
        assert "/src/ @alice" in output
        assert "/tests/ @alice" in output

    def test_custom_domain_mappings(self, temp_repo, codeowners_generator_script):
        """Test custom domain-to-owner mappings."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--domains",
                "docs:@alice",
                "scripts:@bob",
                "inbox:@charlie",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify custom mappings
        assert "/docs/ @alice" in output
        assert "/scripts/ @bob" in output
        assert "/inbox/ @charlie" in output

        # Verify other domains still need owners (warnings)
        assert "TODO" in output or "OWNER_NEEDED" in output

    def test_multiple_owners_per_domain(
        self, temp_repo, codeowners_generator_script
    ):
        """Test assigning multiple owners to a domain."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--domains",
                "docs:@alice,@bob",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify multiple owners
        assert "/docs/ @alice @bob" in output

    def test_team_ownership(self, temp_repo, codeowners_generator_script):
        """Test team ownership (@org/team-name)."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--org",
                "myorg",
                "--teams",
                "docs-team",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify team ownership format
        assert "@myorg/docs-team" in output

    def test_output_to_file(self, temp_repo, codeowners_generator_script):
        """Test writing output to file."""
        output_file = temp_repo / "CODEOWNERS"

        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--owner",
                "@alice",
                "--output",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_file.exists()

        content = output_file.read_text()
        assert "# CODEOWNERS" in content
        assert "/docs/ @alice" in content

    def test_validation_only_mode(self, temp_repo, codeowners_generator_script):
        """Test validation-only mode (no output)."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--owner",
                "@alice",
                "--validate-only",
            ],
            capture_output=True,
            text=True,
        )

        # Should exit successfully (no validation errors)
        assert result.returncode == 0

        # Should not produce CODEOWNERS output
        assert "# CODEOWNERS" not in result.stdout

    def test_invalid_owner_format(self, temp_repo, codeowners_generator_script):
        """Test that invalid owner format is rejected."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                "--owner",
                "alice",  # Missing @ symbol
            ],
            capture_output=True,
            text=True,
        )

        # Should fail with error
        assert result.returncode != 0
        assert "Invalid owner format" in result.stderr or "Must start with '@'" in result.stderr

    def test_missing_owner_argument(self, temp_repo, codeowners_generator_script):
        """Test that missing owner argument is caught."""
        result = subprocess.run(
            [
                sys.executable,
                str(codeowners_generator_script),
                "--template",
                "chora-workspace",
                # No --owner, --domains, or --teams
            ],
            capture_output=True,
            text=True,
        )

        # Should fail with error
        assert result.returncode != 0
        assert "Must provide" in result.stderr or "required" in result.stderr.lower()
