"""
Pytest configuration and fixtures for SAP-052 (Ownership Zones) tests.

Provides shared test fixtures for validating:
- CODEOWNERS file generation
- Ownership coverage analysis
- Reviewer suggestion
- Integration with SAP-051 (Git Workflow Patterns)
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository with sample structure.

    Returns:
        Path: Path to temporary repository root
    """
    repo_path = tmp_path / "test-repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )

    # Create sample directory structure (chora-workspace pattern)
    (repo_path / "docs").mkdir()
    (repo_path / "scripts").mkdir()
    (repo_path / "inbox").mkdir()
    (repo_path / ".chora").mkdir()
    (repo_path / "project-docs").mkdir()

    # Create sample files
    (repo_path / "docs" / "README.md").write_text("# Documentation\n")
    (repo_path / "scripts" / "validate.py").write_text("# Validation script\n")
    (repo_path / "inbox" / "template.json").write_text("{}\n")
    (repo_path / ".chora" / "memory.jsonl").write_text("{}\n")
    (repo_path / "project-docs" / "plan.md").write_text("# Plan\n")
    (repo_path / "README.md").write_text("# Test Repo\n")

    # Initial commit
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )

    return repo_path


@pytest.fixture
def sample_codeowners_content():
    """Sample CODEOWNERS file content.

    Returns:
        str: Valid CODEOWNERS file content for chora-workspace pattern
    """
    return """# CODEOWNERS
# Ownership zones for chora-workspace

# Documentation domain
/docs/ @alice
*.md @alice

# Scripts domain
/scripts/ @bob
justfile @bob

# Coordination domain
/inbox/ @charlie

# Memory domain
/.chora/ @alice

# Project management domain
/project-docs/ @charlie

# Shared files
/AGENTS.md @alice @bob @charlie
/CLAUDE.md @alice @bob @charlie
"""


@pytest.fixture
def codeowners_file(temp_repo, sample_codeowners_content):
    """Create CODEOWNERS file in temporary repository.

    Args:
        temp_repo: Temporary repository fixture
        sample_codeowners_content: Sample CODEOWNERS content fixture

    Returns:
        Path: Path to CODEOWNERS file
    """
    codeowners_path = temp_repo / "CODEOWNERS"
    codeowners_path.write_text(sample_codeowners_content)
    return codeowners_path


@pytest.fixture
def scripts_dir():
    """Get path to scripts directory containing SAP-052 tools.

    Returns:
        Path: Path to scripts/ directory
    """
    # Assuming tests are in tests/test_sap_052/ and scripts are in scripts/
    return Path(__file__).parent.parent.parent / "scripts"


@pytest.fixture
def codeowners_generator_script(scripts_dir):
    """Get path to codeowners-generator.py script.

    Returns:
        Path: Path to codeowners-generator.py
    """
    script_path = scripts_dir / "codeowners-generator.py"
    if not script_path.exists():
        pytest.skip(f"Script not found: {script_path}")
    return script_path


@pytest.fixture
def ownership_coverage_script(scripts_dir):
    """Get path to ownership-coverage.py script.

    Returns:
        Path: Path to ownership-coverage.py
    """
    script_path = scripts_dir / "ownership-coverage.py"
    if not script_path.exists():
        pytest.skip(f"Script not found: {script_path}")
    return script_path


@pytest.fixture
def reviewer_suggester_script(scripts_dir):
    """Get path to reviewer-suggester.py script.

    Returns:
        Path: Path to reviewer-suggester.py
    """
    script_path = scripts_dir / "reviewer-suggester.py"
    if not script_path.exists():
        pytest.skip(f"Script not found: {script_path}")
    return script_path
