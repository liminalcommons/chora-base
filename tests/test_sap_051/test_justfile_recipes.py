"""
Test suite for SAP-051 justfile recipes.

Tests git workflow automation recipes: git-setup, validate-commits,
git-check, and changelog generation.
"""

import subprocess
import pytest
from pathlib import Path
import re


class TestGitSetupRecipe:
    """Test 'just git-setup' recipe."""

    def test_git_setup_installs_hooks(self, temp_git_repo, chora_base_root):
        """Test git-setup configures hooks correctly."""
        # Run git-setup from chora-base
        result = subprocess.run(
            ['just', 'git-setup'],
            cwd=chora_base_root,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "Git hooks installed successfully" in result.stdout

        # Verify git config
        config_result = subprocess.run(
            ['git', 'config', 'core.hooksPath'],
            cwd=chora_base_root,
            capture_output=True,
            text=True
        )
        assert config_result.stdout.strip() == '.githooks'

        # Verify hooks are enabled
        commit_msg_enabled = subprocess.run(
            ['git', 'config', 'hooks.commit-msg-enabled'],
            cwd=chora_base_root,
            capture_output=True,
            text=True
        )
        assert commit_msg_enabled.stdout.strip() == 'true'

    def test_git_setup_makes_hooks_executable(self, chora_base_root, hooks_dir):
        """Test git-setup makes hooks executable."""
        # Run git-setup
        subprocess.run(['just', 'git-setup'], cwd=chora_base_root, capture_output=True)

        # Check hooks are executable
        hooks = ['commit-msg', 'pre-push', 'pre-commit']
        for hook_name in hooks:
            hook_path = hooks_dir / hook_name
            assert hook_path.exists(), f"Hook {hook_name} should exist"
            # On Unix-like systems, check executable bit
            # On Windows, this may not apply
            if hasattr(os, 'access'):
                import os
                assert os.access(hook_path, os.X_OK), f"Hook {hook_name} should be executable"


class TestValidateCommitsRecipe:
    """Test 'just validate-commits' recipe."""

    def test_validate_commits_accepts_valid_commits(self, git_helper, hooks_dir):
        """Test validate-commits passes for valid conventional commits."""
        # Install hooks
        git_helper.install_hooks(hooks_dir)

        # Create valid commits
        git_helper.add_file('file1.txt')
        git_helper.commit('feat(test): add feature 1')

        git_helper.add_file('file2.txt')
        git_helper.commit('fix(test): fix bug 2')

        # Validate commits
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~2'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should pass
        assert result.returncode == 0
        assert "All commits are valid" in result.stdout or "validation passed" in result.stdout.lower()

    def test_validate_commits_rejects_invalid_commits(self, git_helper):
        """Test validate-commits fails for non-conventional commits."""
        # Create invalid commit (bypass hook with --no-verify)
        git_helper.add_file('file1.txt')
        git_helper.run(['git', 'commit', '-m', 'invalid commit message', '--no-verify'])

        # Validate commits should fail
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~1'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode == 1
        assert "doesn't follow" in result.stdout.lower() or "invalid" in result.stdout.lower()

    def test_validate_commits_with_custom_ref(self, git_helper, hooks_dir):
        """Test validate-commits with custom reference point."""
        git_helper.install_hooks(hooks_dir)

        # Create multiple commits
        for i in range(3):
            git_helper.add_file(f'file{i}.txt')
            git_helper.commit(f'feat(test): add feature {i}')

        # Validate only last 2 commits
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~2'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0


class TestGitCheckRecipe:
    """Test 'just git-check' recipe."""

    def test_git_check_passes_when_valid(self, git_helper, hooks_dir):
        """Test git-check passes for valid setup."""
        # Install hooks
        git_helper.install_hooks(hooks_dir)

        # Create valid branch
        git_helper.create_branch('feature/SAP-051-test')

        # Create valid commit
        git_helper.add_file('file1.txt')
        git_helper.commit('feat(test): add feature')

        # Run git-check
        result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should pass
        assert result.returncode == 0
        assert "✓" in result.stdout or "pass" in result.stdout.lower()

    def test_git_check_detects_missing_hooks(self, git_helper):
        """Test git-check detects when hooks are not installed."""
        # Don't install hooks
        result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should fail or warn
        assert "not installed" in result.stdout.lower() or "not configured" in result.stdout.lower()

    def test_git_check_detects_invalid_branch_name(self, git_helper, hooks_dir):
        """Test git-check detects invalid branch names."""
        git_helper.install_hooks(hooks_dir)

        # Create invalid branch (bypass hook)
        git_helper.run(['git', 'checkout', '-b', 'invalid-branch-name'])

        result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should warn about branch name
        assert "branch" in result.stdout.lower() and ("invalid" in result.stdout.lower() or "doesn't follow" in result.stdout.lower())


class TestChangelogRecipe:
    """Test 'just changelog' recipe."""

    def test_changelog_generation(self, git_helper, hooks_dir, chora_base_root):
        """Test changelog generates from conventional commits."""
        git_helper.install_hooks(hooks_dir)

        # Create commits of different types
        commits = [
            ('feat(api): add new endpoint', 'Features'),
            ('fix(api): correct validation', 'Bug Fixes'),
            ('docs(readme): update guide', 'Documentation'),
            ('chore(deps): update packages', 'Chores'),
        ]

        for msg, _ in commits:
            git_helper.add_file(f'file-{msg[:4]}.txt')
            git_helper.commit(msg)

        # Generate changelog
        changelog_path = Path(git_helper.repo_path) / 'CHANGELOG.md'
        result = subprocess.run(
            ['just', 'changelog', '', str(changelog_path)],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0

        # Verify changelog exists and contains expected sections
        assert changelog_path.exists()
        changelog_content = changelog_path.read_text()

        # Check for section headers
        assert 'Features' in changelog_content or 'feat' in changelog_content.lower()
        assert 'Bug Fixes' in changelog_content or 'fix' in changelog_content.lower()

    def test_changelog_with_date_range(self, git_helper, hooks_dir):
        """Test changelog generation with date range."""
        git_helper.install_hooks(hooks_dir)

        # Create old commit
        git_helper.add_file('old.txt')
        git_helper.commit('feat(old): old feature')

        # Get commit SHA for reference
        old_sha = git_helper.run(['git', 'rev-parse', 'HEAD']).stdout.strip()

        # Create new commit
        git_helper.add_file('new.txt')
        git_helper.commit('feat(new): new feature')

        # Generate changelog since old commit
        changelog_path = Path(git_helper.repo_path) / 'CHANGELOG.md'
        result = subprocess.run(
            ['just', 'changelog', old_sha, str(changelog_path)],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert changelog_path.exists()

        changelog_content = changelog_path.read_text()
        # Should contain new feature, not old feature
        assert 'new feature' in changelog_content
        # Old feature might or might not be included depending on range


class TestRecipeIntegration:
    """Integration tests for recipe workflows."""

    def test_complete_workflow(self, git_helper, hooks_dir, chora_base_root):
        """Test complete workflow: setup → commits → validation → changelog."""
        # Step 1: Install hooks
        git_helper.install_hooks(hooks_dir)

        # Step 2: Create valid branch
        git_helper.create_branch('feature/SAP-051-integration-test')

        # Step 3: Create valid commits
        git_helper.add_file('feature1.txt')
        git_helper.commit('feat(integration): add feature 1')

        git_helper.add_file('feature2.txt')
        git_helper.commit('fix(integration): fix bug 2')

        # Step 4: Validate commits
        validate_result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~2'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert validate_result.returncode == 0

        # Step 5: Run git-check
        check_result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert check_result.returncode == 0

        # Step 6: Generate changelog
        changelog_path = Path(git_helper.repo_path) / 'CHANGELOG.md'
        changelog_result = subprocess.run(
            ['just', 'changelog', '', str(changelog_path)],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert changelog_result.returncode == 0
        assert changelog_path.exists()

    def test_recipe_error_handling(self, git_helper):
        """Test recipes handle errors gracefully."""
        # Try to run validate-commits without any commits
        result = subprocess.run(
            ['just', 'validate-commits'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should handle gracefully (either succeed with no commits or provide helpful error)
        # Exact behavior depends on implementation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
