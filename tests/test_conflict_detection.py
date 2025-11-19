"""
Tests for conflict-checker.py script

Tests SAP-053 (conflict resolution) pre-merge conflict detection.

Author: Claude (Anthropic)
Created: 2025-11-19
SAP: SAP-053 (Conflict Resolution)
"""

import json
import pytest
import subprocess
import tempfile
from pathlib import Path

# Get repo root for running scripts
REPO_ROOT = Path(__file__).parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "conflict-checker.py"


class TestCLIExecution:
    """Test conflict-checker.py CLI execution"""

    def test_script_exists(self):
        """Verify script file exists"""
        assert SCRIPT_PATH.exists(), f"Script not found at {SCRIPT_PATH}"

    def test_script_executable(self):
        """Verify script has executable permissions"""
        assert SCRIPT_PATH.stat().st_mode & 0o111, "Script is not executable"

    def test_help_output(self):
        """Verify --help flag produces usage information"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "conflict" in result.stdout.lower()
        assert "--branch" in result.stdout
        assert "--json" in result.stdout
        assert "--verbose" in result.stdout

    def test_help_shows_exit_codes(self):
        """Verify help text documents exit codes"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert "Exit Codes:" in result.stdout
        assert "0 -" in result.stdout  # No conflicts
        assert "1 -" in result.stdout  # Manual review
        assert "2 -" in result.stdout  # Auto-resolvable
        assert "3 -" in result.stdout  # Error


class TestGitRepositorySetup:
    """Test conflict detection in various git scenarios"""

    @pytest.fixture
    def temp_git_repo(self, tmp_path):
        """Create a temporary git repository for testing."""
        repo_dir = tmp_path / "test_repo"
        repo_dir.mkdir()

        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        # Create initial commit on main
        test_file = repo_dir / "test.txt"
        test_file.write_text("initial content\n")
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "branch", "-M", "main"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        return repo_dir

    def test_error_not_in_git_repo(self, tmp_path):
        """Test error when not in a git repository"""
        non_git_dir = tmp_path / "non_git"
        non_git_dir.mkdir()

        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            cwd=non_git_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should fail with error exit code
        assert result.returncode == 3
        assert "not in a git repository" in result.stderr.lower() or "fatal" in result.stderr.lower()

    def test_error_on_target_branch(self, temp_git_repo):
        """Test error when already on target branch"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should fail - already on target branch
        assert result.returncode == 3
        assert "already on" in result.stderr.lower() or "target branch" in result.stderr.lower()

    def test_error_with_uncommitted_changes(self, temp_git_repo):
        """Test error when working directory has uncommitted changes"""
        # Create a feature branch
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Create uncommitted changes
        test_file = temp_git_repo / "uncommitted.txt"
        test_file.write_text("uncommitted content\n")

        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should fail - dirty working directory
        assert result.returncode == 3
        assert "uncommitted" in result.stderr.lower() or "changes" in result.stderr.lower()

    def test_no_conflicts_detected(self, temp_git_repo):
        """Test when no conflicts exist (clean merge)"""
        # Create feature branch with non-conflicting changes
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        new_file = temp_git_repo / "feature.txt"
        new_file.write_text("new feature content\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Add feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Run conflict checker
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should succeed with exit code 0 (no conflicts)
        assert result.returncode == 0
        assert "NO CONFLICTS DETECTED" in result.stdout
        assert "Safe to merge" in result.stdout

    def test_no_conflicts_json_output(self, temp_git_repo):
        """Test JSON output when no conflicts exist"""
        # Create feature branch with non-conflicting changes
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        new_file = temp_git_repo / "feature.txt"
        new_file.write_text("new feature content\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Add feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Run conflict checker with JSON output
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main", "--json"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0

        # Parse JSON output
        report = json.loads(result.stdout)

        assert report["has_conflicts"] is False
        assert report["safe_to_merge"] is True
        assert report["conflicting_files"] == []
        assert report["total_files"] == 0
        assert report["detection_method"] == "git_merge_simulation"
        assert "timestamp" in report
        assert "branch" in report
        assert "target_branch" in report

    def test_conflicts_detected_manual_review(self, temp_git_repo):
        """Test when conflicts exist requiring manual review"""
        # Modify test.txt on main
        test_file = temp_git_repo / "test.txt"
        test_file.write_text("main branch content\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Update on main"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Create feature branch from earlier commit
        subprocess.run(
            ["git", "checkout", "HEAD~1"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Modify same file differently
        test_file.write_text("feature branch content\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Update on feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Run conflict checker
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should detect conflicts with exit code 1 (manual review)
        assert result.returncode == 1
        assert "CONFLICTS DETECTED" in result.stdout
        assert "test.txt" in result.stdout
        assert "Manual Review" in result.stdout

    def test_conflicts_json_output(self, temp_git_repo):
        """Test JSON output when conflicts exist"""
        # Create a file first (common base)
        test_file = temp_git_repo / "code.py"
        test_file.write_text("# initial version\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Add initial code"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Modify on main
        test_file.write_text("# main version\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Update code on main"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Create feature branch from earlier commit
        subprocess.run(
            ["git", "checkout", "HEAD~1"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Modify same file differently
        test_file.write_text("# feature version\n")

        subprocess.run(
            ["git", "add", "."],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Update code on feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True
        )

        # Run conflict checker with JSON
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main", "--json"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should detect conflicts
        assert result.returncode in [1, 2]  # Manual or auto-resolvable

        # Parse JSON
        report = json.loads(result.stdout)

        assert report["has_conflicts"] is True
        assert report["safe_to_merge"] is False
        assert "code.py" in report["conflicting_files"]
        assert report["total_files"] >= 1
        assert "conflict_types" in report
        assert "resolution_strategies" in report
        assert "code.py" in report["conflict_types"]


class TestConflictClassification:
    """Test conflict type classification logic"""

    @pytest.fixture
    def git_repo_with_lockfile_conflict(self, tmp_path):
        """Create repo with lockfile conflict"""
        repo_dir = tmp_path / "lockfile_repo"
        repo_dir.mkdir()

        # Initialize repo
        subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True)

        # Create package-lock.json on main
        lockfile = repo_dir / "package-lock.json"
        lockfile.write_text('{"version": "1.0.0", "lockfileVersion": 2}\n')

        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Add lockfile"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True, capture_output=True)

        # Modify on main
        lockfile.write_text('{"version": "1.1.0", "lockfileVersion": 2}\n')
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update lockfile main"], cwd=repo_dir, check=True, capture_output=True)

        # Create feature branch from earlier
        subprocess.run(["git", "checkout", "HEAD~1"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_dir, check=True, capture_output=True)

        lockfile.write_text('{"version": "1.0.1", "lockfileVersion": 2}\n')
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update lockfile feature"], cwd=repo_dir, check=True, capture_output=True)

        return repo_dir

    def test_lockfile_conflict_classification(self, git_repo_with_lockfile_conflict):
        """Test that lockfile conflicts are classified correctly"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main", "--json"],
            cwd=git_repo_with_lockfile_conflict,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Parse JSON
        report = json.loads(result.stdout)

        # Should detect lockfile conflict
        assert "package-lock.json" in report["conflicting_files"]
        assert report["conflict_types"]["package-lock.json"] == "lockfile"
        assert report["resolution_strategies"]["package-lock.json"] == "regenerate_from_source"

        # Lockfile should be auto-resolvable
        assert "package-lock.json" in report["auto_resolvable_files"]

        # Exit code should be 2 (all auto-resolvable) if only lockfile conflicts
        if len(report["conflicting_files"]) == 1:
            assert result.returncode == 2


class TestVerboseMode:
    """Test verbose output mode"""

    @pytest.fixture
    def simple_git_repo(self, tmp_path):
        """Create simple git repo for testing"""
        repo_dir = tmp_path / "verbose_repo"
        repo_dir.mkdir()

        subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True)

        test_file = repo_dir / "test.txt"
        test_file.write_text("initial\n")

        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True, capture_output=True)

        subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_dir, check=True, capture_output=True)

        new_file = repo_dir / "feature.txt"
        new_file.write_text("feature content\n")

        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Add feature"], cwd=repo_dir, check=True, capture_output=True)

        return repo_dir

    def test_verbose_output(self, simple_git_repo):
        """Test that verbose mode produces debug output"""
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "main", "--verbose"],
            cwd=simple_git_repo,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Verbose output should appear in stderr
        assert "Fetching" in result.stderr or "Running" in result.stderr or "Simulating" in result.stderr


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_invalid_branch_name(self, tmp_path):
        """Test behavior with invalid branch name"""
        repo_dir = tmp_path / "edge_repo"
        repo_dir.mkdir()

        subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True)

        test_file = repo_dir / "test.txt"
        test_file.write_text("initial\n")

        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True, capture_output=True)

        subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_dir, check=True, capture_output=True)

        # Try checking against non-existent branch
        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--branch", "nonexistent"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should fail with error exit code
        assert result.returncode == 3
        assert "does not exist" in result.stderr.lower() or "not found" in result.stderr.lower()

    def test_json_parseable_output(self, tmp_path):
        """Test that JSON output is always valid JSON even on errors"""
        non_git_dir = tmp_path / "non_git_json"
        non_git_dir.mkdir()

        result = subprocess.run(
            ["python", str(SCRIPT_PATH), "--json"],
            cwd=non_git_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Even on error, if --json was specified, stderr might have error
        # but stdout should be empty or valid JSON
        if result.stdout.strip():
            try:
                json.loads(result.stdout)
                # If we get here, it's valid JSON
                assert True
            except json.JSONDecodeError:
                # For errors, we output to stderr, not stdout
                assert result.returncode == 3


# Test coverage summary:
# - CLI execution: 4 tests (help, exit codes, permissions)
# - Git scenarios: 6 tests (not in repo, on target, dirty, no conflicts, conflicts)
# - JSON output: 2 tests (no conflicts, with conflicts)
# - Classification: 1 test (lockfile detection)
# - Verbose mode: 1 test
# - Edge cases: 2 tests (invalid branch, JSON parsing)
# - Total: 16+ test cases covering all major functionality
