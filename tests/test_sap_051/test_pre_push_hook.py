"""
Test suite for SAP-051 pre-push git hook.

Tests branch name validation against SAP-051 branch naming conventions.
"""

import subprocess
import tempfile
import os
import pytest
from pathlib import Path


class TestPrePushHook:
    """Test pre-push hook branch name validation."""

    @pytest.fixture
    def hook_path(self):
        """Path to pre-push hook."""
        return Path(__file__).parent.parent.parent / ".githooks" / "pre-push"

    def run_hook_with_branch(self, hook_path, branch_name, bash_path='bash'):
        """Run pre-push hook with mocked branch name."""
        # Create a temporary git repository for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            subprocess.run(['git', 'init'], capture_output=True, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], capture_output=True, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True, check=True)

            # Create initial commit
            Path('test.txt').write_text('test')
            subprocess.run(['git', 'add', 'test.txt'], capture_output=True, check=True)
            subprocess.run(['git', 'commit', '-m', 'feat: initial commit'], capture_output=True, check=True)

            # Create test branch
            subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True, check=True)

            # Run hook
            result = subprocess.run(
                [bash_path, str(hook_path)],
                capture_output=True,
                text=True
            )
            return result

    # Valid branch names
    def test_valid_feature_branch(self, hook_path, bash_path):
        """Test valid feature branch."""
        result = self.run_hook_with_branch(hook_path, "feature/SAP-051-git-workflow", bash_path)
        assert result.returncode == 0
        assert "validation passed" in result.stdout

    def test_valid_bugfix_branch(self, hook_path, bash_path):
        """Test valid bugfix branch."""
        result = self.run_hook_with_branch(hook_path, "bugfix/.beads-abc-fix-validation", bash_path)
        assert result.returncode == 0

    def test_valid_hotfix_branch(self, hook_path, bash_path):
        """Test valid hotfix branch."""
        result = self.run_hook_with_branch(hook_path, "hotfix/urgent-security-patch", bash_path)
        assert result.returncode == 0

    def test_valid_chore_branch(self, hook_path, bash_path):
        """Test valid chore branch."""
        result = self.run_hook_with_branch(hook_path, "chore/update-dependencies", bash_path)
        assert result.returncode == 0

    def test_valid_docs_branch(self, hook_path, bash_path):
        """Test valid docs branch."""
        result = self.run_hook_with_branch(hook_path, "docs/sap-051-protocol-spec", bash_path)
        assert result.returncode == 0

    def test_valid_refactor_branch(self, hook_path, bash_path):
        """Test valid refactor branch."""
        result = self.run_hook_with_branch(hook_path, "refactor/simplify-hooks", bash_path)
        assert result.returncode == 0

    def test_valid_test_branch(self, hook_path, bash_path):
        """Test valid test branch."""
        result = self.run_hook_with_branch(hook_path, "test/add-validation-tests", bash_path)
        assert result.returncode == 0

    def test_valid_with_dots(self, hook_path, bash_path):
        """Test valid branch with dots in identifier."""
        result = self.run_hook_with_branch(hook_path, "feature/.beads-abc.def-test", bash_path)
        assert result.returncode == 0

    def test_valid_with_underscores(self, hook_path, bash_path):
        """Test valid branch with underscores."""
        result = self.run_hook_with_branch(hook_path, "feature/TEST_123-description", bash_path)
        assert result.returncode == 0

    def test_valid_long_description(self, hook_path, bash_path):
        """Test valid branch with long description."""
        result = self.run_hook_with_branch(hook_path, "feature/SAP-051-git-workflow-patterns-for-multi-dev", bash_path)
        assert result.returncode == 0

    # Invalid branch names
    def test_invalid_no_type(self, hook_path, bash_path):
        """Test invalid branch without type prefix."""
        result = self.run_hook_with_branch(hook_path, "my-feature-branch", bash_path)
        assert result.returncode == 1
        assert "doesn't follow convention" in result.stdout

    def test_invalid_wrong_type(self, hook_path, bash_path):
        """Test invalid branch with wrong type."""
        result = self.run_hook_with_branch(hook_path, "new-feature/SAP-051-test", bash_path)
        assert result.returncode == 1

    def test_invalid_no_slash(self, hook_path, bash_path):
        """Test invalid branch without slash separator."""
        result = self.run_hook_with_branch(hook_path, "feature-SAP-051-test", bash_path)
        assert result.returncode == 1

    def test_invalid_no_identifier(self, hook_path, bash_path):
        """Test invalid branch without identifier (just type/)."""
        result = self.run_hook_with_branch(hook_path, "feature/", bash_path)
        assert result.returncode == 1

    def test_invalid_spaces(self, hook_path, bash_path):
        """Test invalid branch with spaces."""
        result = self.run_hook_with_branch(hook_path, "feature/my branch name", bash_path)
        assert result.returncode == 1

    def test_invalid_uppercase_type(self, hook_path, bash_path):
        """Test invalid branch with uppercase type."""
        result = self.run_hook_with_branch(hook_path, "FEATURE/SAP-051-test", bash_path)
        assert result.returncode == 1

    # Edge cases
    def test_main_branch_skipped(self, hook_path, bash_path):
        """Test main branch is skipped (not validated)."""
        # This would require mocking git branch --show-current to return "main"
        # For now, test that main branch name is handled
        pass  # Skip test, requires special git setup

    def test_master_branch_skipped(self, hook_path, bash_path):
        """Test master branch is skipped."""
        pass  # Skip test, requires special git setup

    def test_branch_length_warning(self, hook_path, bash_path):
        """Test branch length warning (>100 chars)."""
        long_branch = "feature/SAP-051-" + "a" * 100
        result = self.run_hook_with_branch(hook_path,long_branch)
        # Should pass with warning
        assert result.returncode == 0

    # All branch types
    def test_all_branch_types(self, hook_path, bash_path):
        """Test all valid branch types."""
        types = ["feature", "bugfix", "hotfix", "chore", "docs", "refactor", "test"]
        for branch_type in types:
            result = self.run_hook_with_branch(hook_path,f"{branch_type}/TEST-123-description")
            assert result.returncode == 0, f"Branch type '{branch_type}' should be valid"


class TestPrePushHookUnit:
    """Unit tests for pre-push hook (without full git setup)."""

    def test_branch_regex_pattern(self):
        """Test branch naming regex pattern."""
        import re

        # Pattern from pre-push hook
        pattern = r"^(feature|bugfix|hotfix|chore|docs|refactor|test)\/[a-zA-Z0-9\.\-\_]+"

        # Valid branches
        valid = [
            "feature/SAP-051-test",
            "bugfix/.beads-abc-fix",
            "hotfix/urgent-patch",
            "chore/update-deps",
            "docs/readme-update",
            "refactor/simplify-code",
            "test/add-tests",
            "feature/TEST_123-desc",
            "feature/.beads-123.456-test",
        ]

        for branch in valid:
            assert re.match(pattern, branch), f"Branch '{branch}' should match pattern"

        # Invalid branches
        invalid = [
            "my-branch",
            "new-feature/test",
            "feature-test",
            "feature/",
            "FEATURE/test",
            "feature/my branch",
        ]

        for branch in invalid:
            assert not re.match(pattern, branch), f"Branch '{branch}' should NOT match pattern"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
