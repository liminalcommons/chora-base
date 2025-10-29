# GitHub Actions Guide for Chora-Base Projects

**Audience**: Developers using chora-base projects
**Prerequisites**: Basic Git knowledge, GitHub account
**Related**: [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/) for technical specifications

---

## Overview

Chora-base projects come with pre-configured GitHub Actions workflows that automatically test, lint, and validate your code on every push and pull request. This guide helps you understand and work effectively with these workflows.

### What You Get Out of the Box

When you create a project from chora-base, you automatically get:

1. **Test Workflow** - Runs your test suite across Python 3.11, 3.12, 3.13
2. **Lint Workflow** - Checks code quality with ruff and mypy
3. **Security Workflows** - CodeQL scanning and dependency review
4. **Documentation Workflow** - Validates markdown and checks links
5. **Release Workflow** - Automates PyPI publishing on version tags

All workflows are located in `.github/workflows/` and run automatically on push and pull requests.

---

## Understanding Your Workflows

### Test Workflow (`test.yml`)

**What it does**: Runs your pytest suite with coverage requirements

**When it runs**:
- Every push to `main` or `develop` branches
- Every pull request targeting `main` or `develop`

**What it checks**:
```bash
# Equivalent local command
pytest --cov=src --cov-report=term --cov-fail-under=85
```

**Success criteria**:
- ✅ All tests pass
- ✅ Code coverage ≥ 85%
- ✅ Tests pass on Python 3.11, 3.12, and 3.13

**Typical duration**: 2-3 minutes

**Example output** (passing):
```
============================= test session starts ==============================
collected 42 items

tests/test_validation.py ........                                        [ 19%]
tests/test_memory.py ................                                    [ 57%]
tests/utils/test_helpers.py ..................                           [100%]

---------- coverage: platform linux, python 3.11.5-final-0 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/myproject/__init__.py         12      0   100%
src/myproject/validation.py       45      3    93%   78-80
src/myproject/memory.py            67      5    93%   123, 145-148
------------------------------------------------------------
TOTAL                             124      8    94%

Required test coverage of 85% reached. Total coverage: 94.00%
============================= 42 passed in 2.15s ================================
```

---

### Lint Workflow (`lint.yml`)

**What it does**: Checks code style and type annotations

**When it runs**: Same as test workflow (push/PR to main or develop)

**What it checks**:
```bash
# Equivalent local commands
ruff check .          # Code style (PEP 8, import sorting, etc.)
mypy src             # Type checking
```

**Success criteria**:
- ✅ No ruff linting errors
- ✅ No mypy type errors

**Typical duration**: 1-2 minutes

**Example output** (with errors):
```
ruff check .
src/myproject/validation.py:45:1: E501 Line too long (102 > 100 characters)
src/myproject/memory.py:67:5: F401 'typing.Optional' imported but unused

mypy src
src/myproject/validation.py:78: error: Argument 1 to "validate" has incompatible type "str"; expected "int"
Found 1 error in 1 file (checked 12 source files)
```

---

### Security Workflows

#### CodeQL (`codeql.yml`)

**What it does**: Static security analysis to detect vulnerabilities

**When it runs**:
- Every push/PR to main or develop
- Weekly on schedule (Sundays at midnight UTC)

**What it scans for**:
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Command injection
- Path traversal
- Use of insecure cryptography
- And 200+ other security patterns

**Typical duration**: 3-5 minutes

**Where to view results**: GitHub Security tab → Code scanning alerts

#### Dependency Review (`dependency-review.yml`)

**What it does**: Checks new dependencies for known vulnerabilities

**When it runs**: On pull requests that modify `pyproject.toml` or lockfiles

**Success criteria**: No high or critical severity vulnerabilities in new dependencies

---

### Documentation Workflow (`docs-quality.yml`)

**What it does**: Validates markdown files and checks internal links

**When it runs**: When markdown files or docs/ are modified

**What it checks**:
- Markdown syntax validity
- Internal link integrity (no broken links within the repo)
- Documentation structure consistency

**Status**: ⚠️ Warning only (doesn't block merges)

---

## Working with Workflows

### Viewing Workflow Status

**In GitHub UI**:
1. Navigate to your repository
2. Click **Actions** tab
3. See all workflow runs, filter by workflow type, branch, or status

**Workflow status badges** (add to README.md):
```markdown
![Tests](https://github.com/your-org/your-repo/workflows/Test/badge.svg)
![Lint](https://github.com/your-org/your-repo/workflows/Lint/badge.svg)
```

**Via Git CLI** (with GitHub CLI):
```bash
gh run list --limit 5                    # List recent workflow runs
gh run view <run-id>                    # View specific run details
gh run watch                            # Watch current run in real-time
```

---

### Running Workflows Locally

**Before pushing**, run the equivalent commands locally to catch issues early:

**Test workflow equivalent**:
```bash
pytest --cov=src --cov-report=term --cov-fail-under=85
```

**Lint workflow equivalent**:
```bash
ruff check .
mypy src
```

**Quick pre-push check** (run both):
```bash
# Create alias in ~/.bashrc or ~/.zshrc
alias precommit="ruff check . && mypy src && pytest --cov=src --cov-fail-under=85"

# Then just run
precommit
```

---

### Debugging Failed Workflows

#### Step 1: Identify the Failure

Click on the failed workflow run → Click on the failed job → Expand the failing step

**Common failure patterns**:

**Test failures**:
```
FAILED tests/test_validation.py::test_email_validation - AssertionError: ...
```
**Fix**: Run `pytest tests/test_validation.py::test_email_validation -v` locally to debug

**Coverage failure**:
```
FAILED coverage: total coverage (82.00%) is below 85%
```
**Fix**: Add tests for uncovered code (see coverage report for missing lines)

**Lint failures**:
```
src/myproject/api.py:45:1: E501 Line too long
```
**Fix**: Run `ruff check --fix .` to auto-fix, or manually adjust

**Type errors**:
```
src/myproject/validation.py:78: error: Argument 1 has incompatible type
```
**Fix**: Add proper type hints or use `# type: ignore` with justification

#### Step 2: Reproduce Locally

Always try to reproduce the failure on your machine:

```bash
# Use same Python version as workflow (check .github/workflows/test.yml)
python --version  # Should match workflow matrix

# Run failing command
pytest tests/test_validation.py -v

# Or run full test suite
pytest --cov=src --cov-report=term --cov-fail-under=85
```

#### Step 3: Fix and Verify

```bash
# Fix the issue in your code
vim src/myproject/validation.py

# Verify fix locally
pytest tests/test_validation.py -v

# Push fix
git add src/myproject/validation.py
git commit -m "fix: resolve validation test failure"
git push
```

#### Step 4: Monitor Re-Run

GitHub Actions will automatically re-run workflows on the new push. Watch for the green checkmark ✅

---

## Common Scenarios

### Scenario 1: Adding a New Dependency

**Task**: Add `httpx` library to your project

**Steps**:
```bash
# 1. Add dependency
poetry add httpx
# or
pip install httpx
pip freeze > requirements.txt

# 2. Run tests locally (ensure httpx doesn't break anything)
pytest

# 3. Commit and push
git add pyproject.toml poetry.lock  # or requirements.txt
git commit -m "feat: add httpx for HTTP requests"
git push
```

**What happens in CI**:
1. `test.yml` runs - installs httpx, runs tests ✅
2. `dependency-review.yml` runs - scans httpx for vulnerabilities ✅
3. `lint.yml` runs - checks if httpx is actually used (warns if unused) ⚠️

**If dependency-review fails**: httpx has a known vulnerability
- Check workflow log for CVE details
- Consider using a patched version or alternative library
- If acceptable risk, document in PR why vulnerability is acceptable

---

### Scenario 2: Coverage Drops Below 85%

**Problem**: Added new feature, forgot to write tests, coverage drops to 78%

**Workflow failure**:
```
FAILED coverage: total coverage (78.00%) is below the failure threshold (85.00%)
```

**Solution**:
```bash
# 1. Run coverage locally to see what's missing
pytest --cov=src --cov-report=term-missing

# Output shows missing lines:
# src/myproject/new_feature.py    45    12    73%   78-80, 145-151, 200-205

# 2. Write tests for uncovered lines
# Focus on lines 78-80, 145-151, 200-205

# 3. Verify coverage improved
pytest --cov=src --cov-report=term-missing
# Now shows: src/myproject/new_feature.py    45     2    96%   145-146

# 4. Commit tests
git add tests/test_new_feature.py
git commit -m "test: add coverage for new_feature edge cases"
git push
```

**Pro tip**: Use `pytest --cov=src --cov-report=html` to generate interactive HTML coverage report (`htmlcov/index.html`)

---

### Scenario 3: Workflow Taking Too Long

**Problem**: Test workflow takes 10+ minutes (should be 2-3 minutes)

**Common causes**:

**1. Cache miss** (first run or dependencies changed):
```yaml
# Workflow rebuilds cache from scratch
- name: Cache pip dependencies
  uses: actions/cache@v4
  # Cache miss: rebuilding...
```
**Solution**: Wait for cache to build (subsequent runs will be faster)

**2. Slow tests**:
```python
# Example: test with time.sleep()
def test_delayed_operation():
    time.sleep(5)  # ← Slows down CI
    assert delayed_op() == expected
```
**Solution**: Mock time-dependent operations:
```python
from unittest.mock import patch

def test_delayed_operation():
    with patch('time.sleep'):  # Mock sleep (instant)
        assert delayed_op() == expected
```

**3. Too many test variations**:
```python
# Parameterized test with 1000 cases
@pytest.mark.parametrize("input", range(1000))
def test_validation(input):
    assert validate(input)
```
**Solution**: Reduce parameterization or use hypothesis for property-based testing

---

### Scenario 4: Need to Skip a Workflow

**Use case**: Need to push documentation-only changes without running tests

**Option 1: Skip via commit message** (GitHub Actions built-in):
```bash
git commit -m "docs: update README [skip ci]"
```
**Effect**: ALL workflows skip (test, lint, security, etc.)

**Option 2: Skip specific workflows** (modify workflow file):
```yaml
# .github/workflows/test.yml
on:
  push:
    branches: [main, develop]
    paths-ignore:
      - 'docs/**'        # Skip if only docs/ changed
      - '**.md'          # Skip if only markdown changed
      - 'README.md'
```

**Option 3: Manual workflow dispatch** (run workflow on-demand):
```yaml
# .github/workflows/test.yml
on:
  workflow_dispatch:  # Add this to enable manual runs
  push:
    branches: [main, develop]
```
**Then trigger manually**: Actions tab → Select workflow → Run workflow button

---

## Advanced: Customizing Workflows

### Adding a New Python Version

**File**: `.github/workflows/test.yml`

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13", "3.14"]  # Add 3.14
```

### Running Tests in Docker

```yaml
jobs:
  test-docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and test in Docker
        run: |
          docker build -t myproject:test .
          docker run myproject:test pytest
```

### Adding Environment-Specific Tests

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]
```

---

## Troubleshooting

### Workflow Won't Trigger

**Check**:
1. Workflow file syntax: Use [GitHub Actions YAML validator](https://rhysd.github.io/actionlint/)
2. Branch name matches trigger: `branches: [main, develop]`
3. File path matches `paths:` filter (if specified)

### Workflow Stuck on "Queued"

**Causes**:
- GitHub Actions runners unavailable (rare)
- Concurrent workflow limit reached (paid plans only)
- Waiting for required workflows to complete

**Solution**: Wait or cancel and re-run

### Secrets Not Available

**Problem**: `${{ secrets.CODECOV_TOKEN }}` is empty

**Solution**:
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `CODECOV_TOKEN`, Value: `<your-token>`
4. Re-run workflow

---

## Best Practices

### 1. Always Run Locally Before Pushing

```bash
# Pre-push checklist
ruff check .                    # Linting
mypy src                        # Type checking
pytest --cov=src --cov-fail-under=85  # Tests + coverage
```

### 2. Monitor Workflow Duration

**Target**: <5 minutes for test + lint workflows

**If slower**:
- Use caching (chora-base enables this by default)
- Parallelize tests: `pytest -n auto` (requires pytest-xdist)
- Mock slow external calls
- Use pytest markers to separate fast/slow tests

### 3. Don't Commit Workflow Fixes Without Testing

**Bad**:
```bash
# Modify workflow file
vim .github/workflows/test.yml
git add .github/workflows/test.yml
git commit -m "fix: update workflow"
git push
# Wait 3 minutes... workflow fails with YAML syntax error!
```

**Good**:
```bash
# Validate YAML locally first
yamllint .github/workflows/test.yml

# Or use actionlint
brew install actionlint
actionlint .github/workflows/test.yml
```

### 4. Review Security Workflow Results Weekly

Even if CodeQL doesn't block merges, review findings:
- GitHub repo → Security → Code scanning alerts
- Triage: Fix, dismiss with justification, or create issue

---

## Related Documentation

**Chora-Base SAPs**:
- [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/) - Technical specifications
- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/) - Test patterns
- [SAP-006: Quality Gates](../../skilled-awareness/quality-gates/) - Quality standards

**Tutorials**:
- [Debugging CI Failures](../tutorials/debugging-ci-failures.md) - Step-by-step debugging guide
- [Customizing Workflows](../tutorials/customizing-workflows.md) - Advanced customization

**Reference**:
- [Workflow Reference](../reference/workflow-reference.md) - Complete YAML reference
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official docs

---

## Quick Commands Reference

```bash
# View workflow runs
gh run list

# Watch workflow run in real-time
gh run watch

# Re-run failed workflow
gh run rerun <run-id>

# Download workflow logs
gh run download <run-id>

# Run tests locally (equivalent to CI)
pytest --cov=src --cov-report=term --cov-fail-under=85

# Run lint locally (equivalent to CI)
ruff check . && mypy src

# Pre-commit check (all CI checks locally)
ruff check . && mypy src && pytest --cov=src --cov-fail-under=85
```

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
**Maintainer**: Chora-Base Team
