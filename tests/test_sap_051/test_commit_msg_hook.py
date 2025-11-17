"""
Test suite for SAP-051 commit-msg git hook.

Tests commit message validation against Conventional Commits v1.0.0 spec.
"""

import subprocess
import tempfile
import os
import pytest
from pathlib import Path


class TestCommitMsgHook:
    """Test commit-msg hook validation."""

    @pytest.fixture
    def hook_path(self):
        """Path to commit-msg hook."""
        return Path(__file__).parent.parent.parent / ".githooks" / "commit-msg"

    @pytest.fixture
    def temp_commit_msg(self):
        """Create temporary commit message file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            yield f.name
        os.unlink(f.name)

    def run_hook(self, hook_path, commit_msg, temp_file):
        """Run commit-msg hook with given message."""
        with open(temp_file, 'w') as f:
            f.write(commit_msg)

        result = subprocess.run(
            ['bash', str(hook_path), temp_file],
            capture_output=True,
            text=True
        )
        return result

    # Valid commit messages
    def test_valid_feat_commit(self, hook_path, temp_commit_msg):
        """Test valid feat commit with scope."""
        result = self.run_hook(hook_path, "feat(sap-051): add git workflow patterns", temp_commit_msg)
        assert result.returncode == 0
        assert "validation passed" in result.stdout

    def test_valid_fix_commit(self, hook_path, temp_commit_msg):
        """Test valid fix commit."""
        result = self.run_hook(hook_path, "fix(git-hooks): correct validation regex", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_docs_commit(self, hook_path, temp_commit_msg):
        """Test valid docs commit."""
        result = self.run_hook(hook_path, "docs(readme): update installation guide", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_refactor_commit(self, hook_path, temp_commit_msg):
        """Test valid refactor commit."""
        result = self.run_hook(hook_path, "refactor(hooks): simplify validation logic", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_test_commit(self, hook_path, temp_commit_msg):
        """Test valid test commit."""
        result = self.run_hook(hook_path, "test(sap-051): add commit-msg validation tests", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_chore_commit(self, hook_path, temp_commit_msg):
        """Test valid chore commit."""
        result = self.run_hook(hook_path, "chore: update dependencies", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_breaking_change(self, hook_path, temp_commit_msg):
        """Test valid breaking change commit."""
        result = self.run_hook(hook_path, "feat(api)!: change response format", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_no_scope(self, hook_path, temp_commit_msg):
        """Test valid commit without scope."""
        result = self.run_hook(hook_path, "feat: add new feature", temp_commit_msg)
        assert result.returncode == 0

    def test_valid_multiword_scope(self, hook_path, temp_commit_msg):
        """Test valid commit with multi-word scope."""
        result = self.run_hook(hook_path, "feat(git-workflow-patterns): add hooks", temp_commit_msg)
        assert result.returncode == 0

    # Invalid commit messages
    def test_invalid_no_type(self, hook_path, temp_commit_msg):
        """Test invalid commit without type."""
        result = self.run_hook(hook_path, "added new feature", temp_commit_msg)
        assert result.returncode == 1
        assert "doesn't follow Conventional Commits format" in result.stdout

    def test_invalid_wrong_type(self, hook_path, temp_commit_msg):
        """Test invalid commit with wrong type."""
        result = self.run_hook(hook_path, "feature: add new feature", temp_commit_msg)
        assert result.returncode == 1

    def test_invalid_missing_colon(self, hook_path, temp_commit_msg):
        """Test invalid commit missing colon."""
        result = self.run_hook(hook_path, "feat add new feature", temp_commit_msg)
        assert result.returncode == 1

    def test_invalid_no_description(self, hook_path, temp_commit_msg):
        """Test invalid commit without description."""
        result = self.run_hook(hook_path, "feat:", temp_commit_msg)
        assert result.returncode == 1

    def test_invalid_no_space_after_colon(self, hook_path, temp_commit_msg):
        """Test invalid commit without space after colon."""
        result = self.run_hook(hook_path, "feat:add feature", temp_commit_msg)
        assert result.returncode == 1

    def test_invalid_empty_scope(self, hook_path, temp_commit_msg):
        """Test invalid commit with empty scope."""
        result = self.run_hook(hook_path, "feat(): add feature", temp_commit_msg)
        assert result.returncode == 1

    # Edge cases
    def test_merge_commit_skipped(self, hook_path, temp_commit_msg):
        """Test merge commits are skipped (not validated)."""
        result = self.run_hook(hook_path, "Merge branch 'feature/test' into main", temp_commit_msg)
        assert result.returncode == 0  # Should be skipped

    def test_revert_commit_skipped(self, hook_path, temp_commit_msg):
        """Test revert commits are skipped."""
        result = self.run_hook(hook_path, 'Revert "feat: add feature"', temp_commit_msg)
        assert result.returncode == 0  # Should be skipped

    def test_multiline_commit_message(self, hook_path, temp_commit_msg):
        """Test multiline commit message (only first line validated)."""
        message = """feat(sap-051): add git hooks

This is the body of the commit message explaining
the changes in more detail.

Refs: SAP-051"""
        result = self.run_hook(hook_path, message, temp_commit_msg)
        assert result.returncode == 0

    def test_commit_with_footer(self, hook_path, temp_commit_msg):
        """Test commit with footer."""
        message = """fix(hooks): correct validation

BREAKING CHANGE: Changes hook interface"""
        result = self.run_hook(hook_path, message, temp_commit_msg)
        assert result.returncode == 0

    # Configuration tests (require git config mocking)
    def test_custom_types(self, hook_path, temp_commit_msg):
        """Test with custom commit types (requires git config)."""
        # This would require setting git config conventional-commits.types
        # For now, test with default types
        result = self.run_hook(hook_path, "feat(sap-051): add feature", temp_commit_msg)
        assert result.returncode == 0

    def test_subject_length_validation(self, hook_path, temp_commit_msg):
        """Test subject length validation (72 char default)."""
        long_subject = "feat(sap-051): " + "a" * 100  # Exceeds 72 chars
        result = self.run_hook(hook_path, long_subject, temp_commit_msg)
        # Should pass with warning (not strict mode)
        assert result.returncode == 0
        # Warning output would be in stdout but hook still passes

    # All conventional commit types
    def test_all_conventional_types(self, hook_path, temp_commit_msg):
        """Test all conventional commit types."""
        types = [
            "feat", "fix", "docs", "style", "refactor",
            "test", "chore", "perf", "ci", "build", "revert"
        ]
        for commit_type in types:
            result = self.run_hook(hook_path, f"{commit_type}: test message", temp_commit_msg)
            assert result.returncode == 0, f"Type '{commit_type}' should be valid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
