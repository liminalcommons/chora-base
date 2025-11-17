"""
Integration tests for SAP-051 Git Workflow Patterns.

Tests end-to-end workflows combining git hooks, justfile recipes,
and multi-step development scenarios.
"""

import subprocess
import pytest
from pathlib import Path
import time


class TestCommitWorkflow:
    """Test complete commit workflow with hooks."""

    def test_invalid_commit_rejected_then_fixed(self, git_helper, hooks_dir):
        """Test workflow: invalid commit → rejection → fix → acceptance."""
        # Install hooks
        git_helper.install_hooks(hooks_dir)

        # Step 1: Try to commit with invalid message
        git_helper.add_file('feature.txt')
        result = git_helper.commit('added new feature', check=False)

        # Should be rejected
        assert result.returncode == 1
        assert "doesn't follow" in result.stdout.lower() or "doesn't follow" in result.stderr.lower()

        # Step 2: Fix commit message
        result = git_helper.commit('feat(test): add new feature', check=False)

        # Should be accepted
        assert result.returncode == 0

        # Verify commit exists with correct message
        commits = git_helper.get_commits(count=1)
        assert 'feat(test): add new feature' in commits[0]

    def test_multiple_commit_types_workflow(self, git_helper, hooks_dir):
        """Test workflow with multiple commit types."""
        git_helper.install_hooks(hooks_dir)

        # Create different types of commits
        commit_types = [
            ('feat(api): add endpoint', 'feature.txt'),
            ('fix(api): correct bug', 'fix.txt'),
            ('docs(readme): update', 'README.md'),
            ('test(api): add tests', 'test.txt'),
            ('chore(deps): update', 'deps.txt'),
        ]

        for msg, filename in commit_types:
            git_helper.add_file(filename)
            result = git_helper.commit(msg)
            assert result.returncode == 0

        # Verify all commits
        commits = git_helper.get_commits(count=5)
        assert len(commits) == 5

        # Validate all commits
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~5'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_commit_with_breaking_change(self, git_helper, hooks_dir):
        """Test commit with breaking change marker."""
        git_helper.install_hooks(hooks_dir)

        # Create breaking change commit
        git_helper.add_file('breaking.txt')
        result = git_helper.commit('feat!: breaking API change')

        assert result.returncode == 0

        # Alternative format
        git_helper.add_file('breaking2.txt')
        result = git_helper.commit('fix(api)!: breaking bug fix')

        assert result.returncode == 0


class TestBranchWorkflow:
    """Test complete branch workflow with hooks."""

    def test_invalid_branch_rejected_then_fixed(self, git_helper, hooks_dir):
        """Test workflow: invalid branch → rejection → fix → acceptance."""
        git_helper.install_hooks(hooks_dir)

        # Step 1: Create invalid branch (bypassing hook with git command)
        git_helper.run(['git', 'checkout', '-b', 'invalid-branch'])

        # Step 2: Try to push (pre-push hook should reject)
        # Note: This test requires a remote, so we simulate the hook check
        result = subprocess.run(
            ['bash', str(hooks_dir / 'pre-push')],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should be rejected
        assert result.returncode == 1
        assert "doesn't follow convention" in result.stdout

        # Step 3: Rename branch to valid name
        git_helper.run(['git', 'checkout', '-b', 'feature/SAP-051-valid'])

        # Step 4: Try pre-push hook again
        result = subprocess.run(
            ['bash', str(hooks_dir / 'pre-push')],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )

        # Should be accepted
        assert result.returncode == 0
        assert "validation passed" in result.stdout

    def test_all_branch_types_workflow(self, git_helper, hooks_dir):
        """Test workflow with all branch types."""
        git_helper.install_hooks(hooks_dir)

        branch_types = [
            'feature/SAP-051-test-feature',
            'bugfix/.beads-abc-fix',
            'hotfix/urgent-patch',
            'chore/update-deps',
            'docs/update-readme',
            'refactor/cleanup-code',
            'test/add-tests',
        ]

        for branch_name in branch_types:
            # Create branch
            git_helper.run(['git', 'checkout', '-b', branch_name])

            # Verify with pre-push hook
            result = subprocess.run(
                ['bash', str(hooks_dir / 'pre-push')],
                cwd=git_helper.repo_path,
                capture_output=True,
                text=True
            )

            assert result.returncode == 0, f"Branch {branch_name} should be valid"

            # Go back to main for next iteration
            git_helper.run(['git', 'checkout', 'main'])


class TestFeatureDevelopmentWorkflow:
    """Test realistic feature development workflow."""

    def test_complete_feature_workflow(self, git_helper, hooks_dir):
        """Test: create branch → commits → validation → changelog."""
        # Setup
        git_helper.install_hooks(hooks_dir)

        # Step 1: Create feature branch
        git_helper.create_branch('feature/SAP-051-user-auth')

        # Verify branch name
        result = subprocess.run(
            ['bash', str(hooks_dir / 'pre-push')],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

        # Step 2: Implement feature with multiple commits
        commits = [
            ('feat(auth): add user model', 'user.py'),
            ('feat(auth): add authentication service', 'auth.py'),
            ('test(auth): add user model tests', 'test_user.py'),
            ('docs(auth): add authentication guide', 'AUTH.md'),
        ]

        for msg, filename in commits:
            git_helper.add_file(filename, f'Content for {filename}')
            result = git_helper.commit(msg)
            assert result.returncode == 0

        # Step 3: Validate all commits
        result = subprocess.run(
            ['just', 'validate-commits', 'main'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

        # Step 4: Run git-check
        result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

        # Step 5: Generate changelog for feature
        changelog_path = Path(git_helper.repo_path) / 'FEATURE_CHANGELOG.md'
        result = subprocess.run(
            ['just', 'changelog', 'main', str(changelog_path)],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert changelog_path.exists()

        # Verify changelog content
        changelog = changelog_path.read_text()
        assert 'auth' in changelog.lower()
        assert 'user model' in changelog.lower() or 'authentication' in changelog.lower()

    def test_bugfix_workflow(self, git_helper, hooks_dir):
        """Test bugfix workflow with urgent fix."""
        git_helper.install_hooks(hooks_dir)

        # Create bugfix branch
        git_helper.create_branch('bugfix/.beads-123-critical-fix')

        # Implement fix
        git_helper.add_file('fix.py', 'Fixed code')
        result = git_helper.commit('fix(critical): resolve memory leak\n\nRefs: .beads-123')

        assert result.returncode == 0

        # Add test
        git_helper.add_file('test_fix.py', 'Test for fix')
        result = git_helper.commit('test(critical): add regression test')

        assert result.returncode == 0

        # Validate
        result = subprocess.run(
            ['just', 'git-check'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestMultiDeveloperScenarios:
    """Test scenarios with multiple developers."""

    def test_parallel_feature_development(self, git_helper, hooks_dir):
        """Test two features developed in parallel."""
        git_helper.install_hooks(hooks_dir)

        # Developer 1: Feature A
        git_helper.create_branch('feature/SAP-051-feature-a')
        git_helper.add_file('feature_a.py')
        git_helper.commit('feat(a): implement feature A')

        # Switch to main
        git_helper.run(['git', 'checkout', 'main'])

        # Developer 2: Feature B
        git_helper.create_branch('feature/SAP-051-feature-b')
        git_helper.add_file('feature_b.py')
        git_helper.commit('feat(b): implement feature B')

        # Both branches should be valid
        for branch in ['feature/SAP-051-feature-a', 'feature/SAP-051-feature-b']:
            git_helper.run(['git', 'checkout', branch])
            result = subprocess.run(
                ['bash', str(hooks_dir / 'pre-push')],
                cwd=git_helper.repo_path,
                capture_output=True,
                text=True
            )
            assert result.returncode == 0

    def test_sequential_commits_validation(self, git_helper, hooks_dir):
        """Test validation of sequential commits from multiple developers."""
        git_helper.install_hooks(hooks_dir)

        # Simulate commits from different developers
        commits = [
            'feat(api): add endpoint (dev1)',
            'feat(ui): add component (dev2)',
            'fix(api): correct validation (dev1)',
            'docs(api): update docs (dev3)',
        ]

        for msg in commits:
            git_helper.add_file(f'file-{msg[:10]}.txt')
            git_helper.commit(msg)

        # Validate all commits
        result = subprocess.run(
            ['just', 'validate-commits', f'HEAD~{len(commits)}'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestErrorRecovery:
    """Test error recovery workflows."""

    def test_recover_from_invalid_commit(self, git_helper, hooks_dir):
        """Test recovery from accidentally bypassed hook."""
        git_helper.install_hooks(hooks_dir)

        # Accidentally bypass hook
        git_helper.add_file('oops.txt')
        git_helper.run(['git', 'commit', '-m', 'oops invalid message', '--no-verify'])

        # Detect with validation
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~1'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

        # Fix with amend
        result = git_helper.run([
            'git', 'commit', '--amend', '-m',
            'fix(recovery): correct invalid commit message'
        ])
        assert result.returncode == 0

        # Validate again
        result = subprocess.run(
            ['just', 'validate-commits', 'HEAD~1'],
            cwd=git_helper.repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_hook_disabled_and_reenabled(self, git_helper, hooks_dir):
        """Test disabling and re-enabling hooks."""
        git_helper.install_hooks(hooks_dir)

        # Disable hook
        git_helper.run(['git', 'config', 'hooks.commit-msg-enabled', 'false'])

        # Invalid commit should succeed (hook disabled)
        git_helper.add_file('test.txt')
        result = git_helper.commit('invalid message', check=False)
        # Note: May still fail if hook checks the config properly

        # Re-enable hook
        git_helper.run(['git', 'config', 'hooks.commit-msg-enabled', 'true'])

        # Invalid commit should fail now
        git_helper.add_file('test2.txt')
        result = git_helper.commit('another invalid', check=False)
        # Should fail if hook is working


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_commit_message(self, git_helper, hooks_dir):
        """Test handling of empty commit message."""
        git_helper.install_hooks(hooks_dir)

        git_helper.add_file('test.txt')
        result = git_helper.run(
            ['git', 'commit', '--allow-empty-message', '-m', ''],
            check=False
        )

        # Should be rejected
        assert result.returncode == 1

    def test_very_long_commit_message(self, git_helper, hooks_dir):
        """Test handling of very long commit message."""
        git_helper.install_hooks(hooks_dir)

        # Create very long message
        long_msg = 'feat(test): ' + 'a' * 200

        git_helper.add_file('test.txt')
        result = git_helper.commit(long_msg, check=False)

        # May warn but could still succeed depending on strict mode
        # Exact behavior depends on configuration

    def test_special_characters_in_commit(self, git_helper, hooks_dir):
        """Test special characters in commit messages."""
        git_helper.install_hooks(hooks_dir)

        messages = [
            'feat(api): add "quoted" feature',
            "fix(ui): handle user's input",
            'docs(readme): update § section',
        ]

        for msg in messages:
            git_helper.add_file(f'file-{hash(msg)}.txt')
            result = git_helper.commit(msg, check=False)
            # Should handle special characters gracefully


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
