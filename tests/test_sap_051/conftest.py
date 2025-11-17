"""
Shared test fixtures and utilities for SAP-051 test suite.

Provides common fixtures for git hook testing, temporary repositories,
and test data generation.
"""

import os
import platform
import subprocess
import tempfile
from pathlib import Path
import pytest
import shutil


def get_bash_path():
    """Get the correct bash path for the current platform.

    Returns:
        str: Path to bash executable
    """
    # Check if bash is in PATH first
    bash_in_path = shutil.which('bash')
    if bash_in_path:
        return 'bash'

    # Platform-specific bash locations
    if platform.system() == 'Windows':
        # Try common Git Bash locations on Windows
        possible_paths = [
            r'C:\Program Files\Git\bin\bash.exe',
            r'C:\Program Files (x86)\Git\bin\bash.exe',
            os.path.expanduser(r'~\AppData\Local\Programs\Git\bin\bash.exe'),
        ]

        for bash_path in possible_paths:
            if os.path.exists(bash_path):
                return bash_path

        # Fall back to git bash (which should work if git is installed)
        return 'bash'

    # Unix-like systems (Linux, macOS)
    return 'bash'


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing.

    Yields the path to the repository, then cleans up afterward.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=tmpdir, capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=tmpdir, capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmpdir, capture_output=True, check=True)

        # Create initial commit
        test_file = Path(tmpdir) / 'test.txt'
        test_file.write_text('initial content')
        subprocess.run(['git', 'add', 'test.txt'], cwd=tmpdir, capture_output=True, check=True)
        subprocess.run(['git', 'commit', '-m', 'feat: initial commit'], cwd=tmpdir, capture_output=True, check=True)

        yield tmpdir


@pytest.fixture
def chora_base_root():
    """Path to chora-base root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def hooks_dir(chora_base_root):
    """Path to .githooks directory."""
    return chora_base_root / '.githooks'


@pytest.fixture
def commit_msg_hook(hooks_dir):
    """Path to commit-msg hook."""
    return hooks_dir / 'commit-msg'


@pytest.fixture
def pre_push_hook(hooks_dir):
    """Path to pre-push hook."""
    return hooks_dir / 'pre-push'


@pytest.fixture
def pre_commit_hook(hooks_dir):
    """Path to pre-commit hook."""
    return hooks_dir / 'pre-commit'


@pytest.fixture
def justfile_path(chora_base_root):
    """Path to justfile."""
    return chora_base_root / 'justfile'


@pytest.fixture
def bash_path():
    """Get bash executable path for the current platform.

    Returns the correct bash path for running git hooks on Windows or Unix-like systems.
    """
    return get_bash_path()


class GitHelper:
    """Helper class for git operations in tests."""

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def run(self, cmd, check=True, capture=True):
        """Run git command in repository."""
        if capture:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
        else:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                check=False
            )

        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode,
                cmd,
                result.stdout if capture else None,
                result.stderr if capture else None
            )

        return result

    def commit(self, message, allow_empty=False):
        """Create a commit with given message."""
        cmd = ['git', 'commit', '-m', message]
        if allow_empty:
            cmd.append('--allow-empty')
        return self.run(cmd)

    def create_branch(self, branch_name):
        """Create and checkout a new branch."""
        return self.run(['git', 'checkout', '-b', branch_name])

    def add_file(self, filename, content='test content'):
        """Add a file to the repository."""
        file_path = Path(self.repo_path) / filename
        file_path.write_text(content)
        return self.run(['git', 'add', filename])

    def install_hooks(self, hooks_dir):
        """Install git hooks from hooks directory."""
        self.run(['git', 'config', 'core.hooksPath', str(hooks_dir)])
        self.run(['git', 'config', 'hooks.commit-msg-enabled', 'true'])
        self.run(['git', 'config', 'hooks.pre-push-enabled', 'true'])
        self.run(['git', 'config', 'hooks.pre-commit-enabled', 'false'])

    def get_current_branch(self):
        """Get current branch name."""
        result = self.run(['git', 'branch', '--show-current'])
        return result.stdout.strip()

    def get_commits(self, ref='HEAD', count=10):
        """Get recent commit messages."""
        result = self.run(['git', 'log', f'-{count}', ref, '--format=%s'])
        return result.stdout.strip().split('\n') if result.stdout else []


@pytest.fixture
def git_helper(temp_git_repo):
    """Git helper instance for test repository."""
    return GitHelper(temp_git_repo)


# Test data generators

def generate_valid_commit_types():
    """Generate all valid conventional commit types."""
    return [
        'feat', 'fix', 'docs', 'style', 'refactor',
        'test', 'chore', 'perf', 'ci', 'build', 'revert'
    ]


def generate_valid_branch_types():
    """Generate all valid branch types."""
    return ['feature', 'bugfix', 'hotfix', 'chore', 'docs', 'refactor', 'test']


def generate_valid_commit_messages():
    """Generate examples of valid commit messages."""
    return [
        'feat(sap-051): add git workflow patterns',
        'fix(hooks): correct validation regex',
        'docs(readme): update installation instructions',
        'chore: update dependencies',
        'refactor(validation): simplify hook logic',
        'test(sap-051): add hook validation tests',
        'perf(hooks): optimize regex matching',
        'ci(github): add workflow validation',
        'build(deps): bump pytest to 8.0',
        'revert: revert "feat: add feature"',
        'feat!: breaking change to API',
        'fix(scope)!: breaking bug fix'
    ]


def generate_invalid_commit_messages():
    """Generate examples of invalid commit messages."""
    return [
        'added new feature',  # No type
        'new-feature: add something',  # Wrong type
        'feat add something',  # Missing colon
        'feat:',  # No description
        'feat: Add feature',  # Uppercase description
        'FEAT: add feature',  # Uppercase type
        'feat(scope) add feature',  # Missing colon after scope
    ]


def generate_valid_branch_names():
    """Generate examples of valid branch names."""
    return [
        'feature/SAP-051-git-workflow',
        'bugfix/.beads-abc-fix-validation',
        'hotfix/urgent-security-patch',
        'chore/update-dependencies',
        'docs/sap-051-protocol-spec',
        'refactor/simplify-hooks',
        'test/add-validation-tests',
        'feature/TEST_123-description',
        'feature/.beads-123.456-test',
    ]


def generate_invalid_branch_names():
    """Generate examples of invalid branch names."""
    return [
        'my-feature-branch',  # No type
        'new-feature/SAP-051-test',  # Wrong type
        'feature-SAP-051-test',  # No slash
        'feature/',  # No identifier
        'feature/my branch name',  # Spaces
        'FEATURE/SAP-051-test',  # Uppercase type
    ]


# Export fixtures and helpers

__all__ = [
    'temp_git_repo',
    'chora_base_root',
    'hooks_dir',
    'commit_msg_hook',
    'pre_push_hook',
    'pre_commit_hook',
    'justfile_path',
    'git_helper',
    'GitHelper',
    'generate_valid_commit_types',
    'generate_valid_branch_types',
    'generate_valid_commit_messages',
    'generate_invalid_commit_messages',
    'generate_valid_branch_names',
    'generate_invalid_branch_names',
]
