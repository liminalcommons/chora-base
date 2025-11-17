# SAP-051 Test Suite

Comprehensive validation test suite for **SAP-051: Git Workflow Patterns**.

Tests git hooks, justfile recipes, and end-to-end development workflows to ensure SAP-051 implementation meets specification requirements.

---

## Test Coverage

### 1. Git Hook Tests

#### `test_commit_msg_hook.py` (~180 lines)

Tests the `commit-msg` hook for Conventional Commits v1.0.0 validation.

**Coverage**:
- ✅ Valid commit formats (all types: feat, fix, docs, etc.)
- ✅ Valid commits with/without scope
- ✅ Breaking change commits (`!` marker)
- ❌ Invalid commits (no type, wrong type, missing colon, etc.)
- 🔄 Edge cases (merge commits, revert commits, multiline messages)
- ⚙️ Configuration (custom types, subject length, strict mode)

**Test Classes**:
- `TestCommitMsgHook` - Integration tests with temp git repos
- `TestCommitMsgHookUnit` - Unit tests for regex patterns

**Example Test**:
```python
def test_valid_feat_commit(self, hook_path, temp_commit_msg):
    """Test valid feat commit with scope."""
    result = self.run_hook(hook_path, "feat(sap-051): add git workflow patterns", temp_commit_msg)
    assert result.returncode == 0
    assert "validation passed" in result.stdout
```

**Run Tests**:
```bash
pytest tests/test_sap_051/test_commit_msg_hook.py -v
```

---

#### `test_pre_push_hook.py` (~160 lines)

Tests the `pre-push` hook for branch name validation.

**Coverage**:
- ✅ Valid branch names (all types: feature, bugfix, hotfix, etc.)
- ✅ Valid formats with dots, underscores, hyphens
- ❌ Invalid branch names (no type, wrong type, no slash, spaces, uppercase)
- 🔄 Edge cases (main/master skipped, length warnings)
- ⚙️ Unit tests for regex patterns

**Test Classes**:
- `TestPrePushHook` - Integration tests with temp git repos
- `TestPrePushHookUnit` - Unit tests for regex validation

**Example Test**:
```python
def test_valid_feature_branch(self, hook_path):
    """Test valid feature branch."""
    result = self.run_hook_with_branch(hook_path, "feature/SAP-051-git-workflow")
    assert result.returncode == 0
    assert "validation passed" in result.stdout
```

**Run Tests**:
```bash
pytest tests/test_sap_051/test_pre_push_hook.py -v
```

---

### 2. Justfile Recipe Tests

#### `test_justfile_recipes.py` (~220 lines)

Tests automation recipes for git workflow management.

**Coverage**:
- `just git-setup` - Hook installation and configuration
- `just validate-commits` - Commit history validation
- `just git-check` - Comprehensive health check
- `just changelog` - Changelog generation from commits

**Test Classes**:
- `TestGitSetupRecipe` - Hook installation tests
- `TestValidateCommitsRecipe` - Commit validation tests
- `TestGitCheckRecipe` - Health check tests
- `TestChangelogRecipe` - Changelog generation tests
- `TestRecipeIntegration` - Multi-recipe workflows

**Example Test**:
```python
def test_git_setup_installs_hooks(self, temp_git_repo, chora_base_root):
    """Test git-setup configures hooks correctly."""
    result = subprocess.run(['just', 'git-setup'], cwd=chora_base_root, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Git hooks installed successfully" in result.stdout
```

**Run Tests**:
```bash
pytest tests/test_sap_051/test_justfile_recipes.py -v
```

---

### 3. Integration Tests

#### `test_integration.py` (~280 lines)

End-to-end workflow tests for realistic development scenarios.

**Coverage**:
- 🔄 Commit workflows (invalid → rejection → fix → acceptance)
- 🌿 Branch workflows (all branch types, validation, corrections)
- 🎯 Feature development (complete feature lifecycle)
- 🐛 Bugfix workflows (urgent fixes with validation)
- 👥 Multi-developer scenarios (parallel development, sequential commits)
- 🔧 Error recovery (invalid commits, hook disable/enable)
- 🎲 Edge cases (empty commits, long messages, special characters)

**Test Classes**:
- `TestCommitWorkflow` - Commit validation workflows
- `TestBranchWorkflow` - Branch validation workflows
- `TestFeatureDevelopmentWorkflow` - Realistic feature development
- `TestMultiDeveloperScenarios` - Multi-developer collaboration
- `TestErrorRecovery` - Error handling and recovery
- `TestEdgeCases` - Edge cases and special scenarios

**Example Test**:
```python
def test_complete_feature_workflow(self, git_helper, hooks_dir):
    """Test: create branch → commits → validation → changelog."""
    git_helper.install_hooks(hooks_dir)
    git_helper.create_branch('feature/SAP-051-user-auth')

    # Multiple commits with different types
    commits = [
        ('feat(auth): add user model', 'user.py'),
        ('test(auth): add tests', 'test_user.py'),
    ]
    for msg, filename in commits:
        git_helper.add_file(filename)
        git_helper.commit(msg)

    # Validate and generate changelog
    result = subprocess.run(['just', 'git-check'], cwd=git_helper.repo_path, capture_output=True)
    assert result.returncode == 0
```

**Run Tests**:
```bash
pytest tests/test_sap_051/test_integration.py -v
```

---

### 4. Test Fixtures and Utilities

#### `conftest.py` (~200 lines)

Shared test fixtures and helper utilities for all test modules.

**Key Fixtures**:
- `temp_git_repo` - Temporary git repository for testing
- `chora_base_root` - Path to chora-base root directory
- `hooks_dir` - Path to .githooks directory
- `commit_msg_hook`, `pre_push_hook`, `pre_commit_hook` - Hook paths
- `justfile_path` - Path to justfile
- `git_helper` - GitHelper instance with convenience methods

**Helper Classes**:
- `GitHelper` - Utility class for git operations in tests
  - `run(cmd)` - Run git command
  - `commit(message)` - Create commit
  - `create_branch(name)` - Create and checkout branch
  - `add_file(filename, content)` - Add file to repo
  - `install_hooks(hooks_dir)` - Install hooks
  - `get_current_branch()` - Get current branch name
  - `get_commits(ref, count)` - Get commit history

**Test Data Generators**:
- `generate_valid_commit_types()` - All valid commit types
- `generate_valid_branch_types()` - All valid branch types
- `generate_valid_commit_messages()` - Example valid commits
- `generate_invalid_commit_messages()` - Example invalid commits
- `generate_valid_branch_names()` - Example valid branch names
- `generate_invalid_branch_names()` - Example invalid branch names

**Usage**:
```python
def test_example(git_helper, hooks_dir):
    git_helper.install_hooks(hooks_dir)
    git_helper.create_branch('feature/test')
    git_helper.add_file('test.txt')
    git_helper.commit('feat(test): add feature')
```

---

## Running Tests

### Run All Tests

```bash
# Run all SAP-051 tests
pytest tests/test_sap_051/ -v

# Run with coverage
pytest tests/test_sap_051/ --cov=.githooks --cov-report=html

# Run specific test file
pytest tests/test_sap_051/test_commit_msg_hook.py -v

# Run specific test class
pytest tests/test_sap_051/test_integration.py::TestCommitWorkflow -v

# Run specific test
pytest tests/test_sap_051/test_integration.py::TestCommitWorkflow::test_invalid_commit_rejected_then_fixed -v
```

### Quick Validation

```bash
# Quick smoke test (fast, critical tests only)
pytest tests/test_sap_051/ -k "test_valid" --maxfail=3

# Integration tests only
pytest tests/test_sap_051/test_integration.py -v

# Hook tests only
pytest tests/test_sap_051/test_commit_msg_hook.py tests/test_sap_051/test_pre_push_hook.py -v
```

---

## Test Requirements

### Dependencies

Install test dependencies:

```bash
# Using pip
pip install pytest pytest-cov

# Using poetry (if in chora-base)
poetry install --with dev

# Using just recipe (if available)
just test-setup
```

**Required**:
- `pytest` >= 7.0
- `pytest-cov` >= 4.0 (for coverage)
- `bash` (for running git hooks)
- `git` >= 2.30

**Optional**:
- `just` (for running justfile recipes)
- `pytest-xdist` (for parallel test execution)

### Environment

Tests require:
- Git installed and in PATH
- Bash shell (Git Bash on Windows, native bash on Unix)
- Write access to create temporary directories
- Justfile recipes available (for recipe tests)

Tests are compatible with:
- Linux, macOS, Windows (with Git Bash)
- Python 3.8+
- Git 2.30+

---

## Test Statistics

**Total Test Coverage**:
- **Lines of Test Code**: ~840 lines
- **Test Files**: 5 files (4 test modules + 1 fixtures)
- **Test Classes**: 14 classes
- **Test Functions**: ~80 test cases
- **Code Coverage Target**: 90%+ for git hooks and justfile recipes

**Test Breakdown**:
- Hook Tests: ~340 lines (40%)
- Recipe Tests: ~220 lines (26%)
- Integration Tests: ~280 lines (33%)

**Estimated Runtime**:
- Full suite: ~2-5 minutes (depends on git operations)
- Smoke tests: ~30-60 seconds
- Single test file: ~20-60 seconds

---

## Test Design Principles

### 1. Isolation

Each test runs in a temporary git repository:
- No interference between tests
- Clean state for each test
- Safe to run in parallel (with pytest-xdist)

### 2. Realism

Tests simulate real development workflows:
- Actual git commands (not mocks)
- Real file operations
- Authentic error scenarios

### 3. Clarity

Test names describe what is being tested:
- `test_valid_feat_commit` - Clear what succeeds
- `test_invalid_no_type` - Clear what fails
- `test_complete_feature_workflow` - Clear scope

### 4. Maintainability

Shared fixtures reduce duplication:
- `GitHelper` class for common operations
- Fixtures for paths and configurations
- Data generators for test cases

---

## Troubleshooting

### Common Issues

**1. "bash: command not found"**
- **Cause**: Bash not in PATH (Windows)
- **Fix**: Install Git Bash or WSL, ensure in PATH

**2. "git: command not found"**
- **Cause**: Git not installed or not in PATH
- **Fix**: Install Git and add to PATH

**3. "Permission denied" on hooks**
- **Cause**: Hooks not executable (Unix)
- **Fix**: Run `chmod +x .githooks/*`

**4. Tests hang or timeout**
- **Cause**: Git prompting for input
- **Fix**: Configure git user.name and user.email globally

**5. "No such file or directory: justfile"**
- **Cause**: Running tests from wrong directory
- **Fix**: Run from chora-base root: `pytest tests/test_sap_051/`

### Debug Mode

Run tests with verbose output:

```bash
# Show all output (stdout/stderr)
pytest tests/test_sap_051/ -v -s

# Show test details
pytest tests/test_sap_051/ -vv

# Stop on first failure
pytest tests/test_sap_051/ -x

# Run specific failing test with full output
pytest tests/test_sap_051/test_integration.py::TestCommitWorkflow::test_invalid_commit_rejected_then_fixed -vv -s
```

---

## Future Enhancements

**Planned Improvements**:
- [ ] Add performance benchmarks (hook execution time <500ms)
- [ ] Add Windows-specific path handling tests
- [ ] Add CI/CD integration tests (GitHub Actions)
- [ ] Add security tests (secret detection)
- [ ] Add multi-repository tests (submodules, monorepos)
- [ ] Add locale/encoding tests (UTF-8, emoji in commits)

**Test Coverage Goals**:
- [ ] 95%+ line coverage for git hooks
- [ ] 90%+ branch coverage for justfile recipes
- [ ] 100% coverage for critical validation paths

---

## References

**SAP-051 Artifacts**:
- [Capability Charter](../../docs/skilled-awareness/git-workflow-patterns/capability-charter.md)
- [Protocol Specification](../../docs/skilled-awareness/git-workflow-patterns/protocol-spec.md)
- [Awareness Guide](../../docs/skilled-awareness/git-workflow-patterns/awareness-guide.md)
- [Adoption Blueprint](../../docs/skilled-awareness/git-workflow-patterns/adoption-blueprint.md)

**External References**:
- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Pytest Documentation](https://docs.pytest.org/)
- [Just Documentation](https://github.com/casey/just)

---

**Created**: 2025-11-16
**Last Updated**: 2025-11-16
**Maintainer**: chora-base team
**Test Suite Version**: 1.0.0
