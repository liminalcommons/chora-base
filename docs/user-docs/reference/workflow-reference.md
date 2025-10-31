# GitHub Actions Workflow Reference

**Audience**: Developers customizing chora-base workflows
**Related**: [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/protocol-spec.md) for complete specifications

---

## Overview

Complete reference for all GitHub Actions workflows included in chora-base projects. This document provides quick lookup for workflow configurations, triggers, and outputs.

---

## Test Workflow (test.yml)

### Purpose
Run pytest test suite across multiple Python versions with coverage enforcement.

### Triggers
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### Matrix Configuration
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

### Steps Reference

| Step | Action/Command | Purpose |
|------|---------------|---------|
| Checkout | `actions/checkout@v4` | Clone repository |
| Setup Python | `actions/setup-python@v5` | Install Python from matrix |
| Cache Dependencies | `actions/cache@v4` | Cache ~/.cache/pip |
| Install | `pip install -e ".[dev]"` | Install project + dev dependencies |
| Run Tests | `pytest --cov=src --cov-fail-under=85` | Execute tests with coverage |
| Upload Coverage | `codecov/codecov-action@v4` | Upload to Codecov (Python 3.11 only) |

### Environment Variables
- `CODECOV_TOKEN`: Secret for Codecov upload

### Success Criteria
- All tests pass
- Coverage ≥ 85%
- Passes on all Python versions in matrix

### Typical Duration
2-3 minutes per Python version

---

## Lint Workflow (lint.yml)

### Purpose
Check code quality with ruff (linting) and mypy (type checking).

### Triggers
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### Python Version
Single version: 3.11 (linting is version-independent)

### Steps Reference

| Step | Command | Purpose |
|------|---------|---------|
| Checkout | `actions/checkout@v4` | Clone repository |
| Setup Python | Python 3.11 | Install Python 3.11 |
| Cache | Cache pip dependencies | Speed up subsequent runs |
| Install | `pip install -e ".[dev]"` | Install dependencies |
| Ruff | `ruff check .` | Lint code (PEP 8, imports, etc.) |
| Mypy | `mypy src` | Type checking |

### Success Criteria
- No ruff violations
- No mypy type errors

### Typical Duration
1-2 minutes

---

## Smoke Test Workflow (smoke.yml)

### Purpose
Quick validation that basic operations work (server starts, basic endpoints respond).

### Triggers
Same as test.yml

### Configuration
- Python: 3.11 only
- Fast execution: 30-60 seconds
- Required: Yes (blocks merges)

### Typical Smoke Tests
```python
def test_server_starts():
    """Verify server can start without errors."""
    assert server.is_running()

def test_health_endpoint():
    """Verify health check responds."""
    response = client.get("/health")
    assert response.status_code == 200
```

---

## Documentation Quality Workflow (docs-quality.yml)

### Purpose
Validate markdown syntax and check internal links.

### Triggers
```yaml
on:
  push:
    paths:
      - '**/*.md'
      - 'docs/**'
```

### Validation Checks
1. Markdown syntax (markdownlint)
2. Internal link integrity
3. Documentation structure consistency

### Status
⚠️ Warning only (doesn't block merges)

### Typical Duration
1-2 minutes

---

## CodeQL Security Workflow (codeql.yml)

### Purpose
Static security analysis to detect vulnerabilities.

### Triggers
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

### Configuration
```yaml
strategy:
  matrix:
    language: [python]

# Use security-extended query suite (comprehensive)
queries: security-extended
```

### Detections
- SQL injection
- Command injection
- Path traversal
- XSS vulnerabilities
- Insecure crypto
- 200+ security patterns

### Results
View in: GitHub Security tab → Code scanning alerts

### Typical Duration
3-5 minutes

---

## Dependency Review Workflow (dependency-review.yml)

### Purpose
Check new dependencies for known vulnerabilities.

### Triggers
```yaml
on:
  pull_request:
```

### What It Checks
- New dependencies added in PR
- Known CVEs in dependencies
- License compatibility

### Configuration
```yaml
fail-on-severity: high  # Block on high/critical vulnerabilities
```

### Typical Duration
30-60 seconds

---

## Release Workflow (release.yml)

### Purpose
Build and publish package to PyPI on version tags.

### Triggers
```yaml
on:
  push:
    tags:
      - 'v*'  # v1.0.0, v2.1.3, etc.
  workflow_dispatch:  # Manual trigger
```

### Steps
1. Build wheel: `python -m build`
2. Publish to Test PyPI (if tag contains `-rc`, `-alpha`, `-beta`)
3. Publish to PyPI (if release tag)

### Required Secrets
- `PYPI_API_TOKEN`: PyPI authentication token
- `TEST_PYPI_API_TOKEN`: Test PyPI token (optional)

### Creating Release
```bash
# 1. Tag release
git tag v1.0.0
git push origin v1.0.0

# 2. Workflow triggers automatically
# 3. Check Actions tab for build status
```

---

## Dependabot Auto-Merge Workflow (dependabot-automerge.yml)

### Purpose
Automatically merge minor/patch Dependabot PRs after tests pass.

### Triggers
```yaml
on:
  pull_request:
  workflow_run:
    workflows: ["Test"]
    types: [completed]
```

### Auto-Merge Conditions
```yaml
# Only auto-merge if:
- PR author is dependabot[bot]
- Update is minor or patch (not major)
- All checks passed
```

### Safety
- Major version updates require manual review
- Tests must pass before merge
- Can be disabled by adding `[no-automerge]` to PR title

---

## Cache Configuration Reference

### Pip Cache
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Cache invalidation**: When `pyproject.toml` changes

### Poetry Cache
```yaml
- name: Cache poetry
  uses: actions/cache@v4
  with:
    path: ~/.cache/pypoetry
    key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
```

### Conda Cache
```yaml
- name: Cache conda
  uses: actions/cache@v4
  with:
    path: ~/conda_pkgs_dir
    key: ${{ runner.os }}-conda-${{ hashFiles('environment.yml') }}
```

---

## Environment Variables Reference

### Built-in GitHub Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `github.ref` | `refs/heads/main` | Git reference |
| `github.sha` | `abc123...` | Commit SHA |
| `github.repository` | `org/repo` | Repository name |
| `github.actor` | `username` | User who triggered workflow |
| `github.event_name` | `push` or `pull_request` | Trigger event |
| `runner.os` | `Linux`, `macOS`, `Windows` | Runner OS |

### Custom Environment Variables
```yaml
env:
  PYTHON_VERSION: "3.11"
  COVERAGE_THRESHOLD: "85"

jobs:
  test:
    steps:
      - run: pytest --cov-fail-under=${{ env.COVERAGE_THRESHOLD }}
```

---

## Matrix Build Reference

### Basic Matrix
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, macos-latest, windows-latest]
# Creates 9 jobs (3 Python × 3 OS)
```

### Matrix with Exclusions
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, macos-latest, windows-latest]
    exclude:
      - os: macos-latest
        python-version: "3.13"  # Skip Python 3.13 on macOS
# Creates 8 jobs (9 - 1 exclusion)
```

### Matrix with Includes
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
    include:
      - python-version: "3.13"
        experimental: true  # Add extra field
```

### Accessing Matrix Values
```yaml
steps:
  - run: echo "Testing Python ${{ matrix.python-version }}"
  - run: echo "Running on ${{ matrix.os }}"
```

---

## Secrets Management Reference

### Setting Secrets
GitHub repo → Settings → Secrets and variables → Actions → New repository secret

### Using Secrets
```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    run: ./deploy.sh
```

### Security Notes
- Secrets are masked in logs
- Not available in fork PRs (security feature)
- Rotate secrets regularly

---

## Conditional Execution Reference

### Branch Conditions
```yaml
- name: Deploy to prod
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### Event Conditions
```yaml
- name: Only on push
  if: github.event_name == 'push'
  run: echo "Pushed to branch"
```

### Status Conditions
```yaml
- name: On failure
  if: failure()
  run: echo "Previous step failed"

- name: Always run
  if: always()
  run: echo "Cleanup tasks"
```

### Combining Conditions
```yaml
- name: Deploy to prod (push to main only)
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  run: ./deploy-prod.sh
```

---

## Workflow Outputs Reference

### Defining Outputs
```yaml
jobs:
  test:
    outputs:
      coverage: ${{ steps.cov.outputs.percentage }}
    steps:
      - id: cov
        run: |
          COV=$(pytest --cov=src | grep TOTAL | awk '{print $4}')
          echo "percentage=$COV" >> $GITHUB_OUTPUT
```

### Using Outputs
```yaml
jobs:
  report:
    needs: test
    steps:
      - run: echo "Coverage: ${{ needs.test.outputs.coverage }}"
```

---

## Timeout Reference

### Job Timeout
```yaml
jobs:
  test:
    timeout-minutes: 10  # Kill job after 10 minutes
```

### Step Timeout
```yaml
steps:
  - name: Long running test
    timeout-minutes: 5
    run: pytest tests/integration
```

### Default Timeout
- Job default: 360 minutes (6 hours)
- GitHub Actions free tier: 2000 minutes/month

---

## Workflow Status Badges

### Basic Badge
```markdown
![Test](https://github.com/org/repo/workflows/Test/badge.svg)
```

### Branch-Specific Badge
```markdown
![Test](https://github.com/org/repo/workflows/Test/badge.svg?branch=main)
```

### Event-Specific Badge
```markdown
![Test](https://github.com/org/repo/workflows/Test/badge.svg?event=push)
```

---

## Common Workflow Patterns

### Run on Schedule
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

### Path Filtering
```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
    paths-ignore:
      - 'docs/**'
      - '**.md'
```

### Manual Workflow Trigger
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

---

## Troubleshooting Reference

### Workflow Not Triggering

**Check**:
1. File location: Must be `.github/workflows/*.yml`
2. YAML syntax: Use `actionlint` to validate
3. Branch/path filters match
4. Workflow file committed to repo

### Secrets Not Available

**Symptoms**:
- `${{ secrets.TOKEN }}` is empty
- Authentication fails

**Solutions**:
1. Verify secret exists in repo settings
2. Check secret name matches exactly (case-sensitive)
3. For fork PRs, secrets aren't available (security feature)

### Cache Not Working

**Symptoms**:
- Every run takes full time
- Dependencies reinstall every time

**Solutions**:
1. Check cache key uniqueness
2. Verify cache path is correct
3. Check if cache size exceeded (10GB limit)

---

## Related Documentation

- [GitHub Actions Guide](../guides/github-actions.md) - General usage guide
- [Debugging CI Failures](../tutorials/debugging-ci-failures.md) - Troubleshooting
- [Customizing Workflows](../tutorials/customizing-workflows.md) - Advanced customization
- [SAP-005: CI/CD Workflows](../../skilled-awareness/ci-cd-workflows/) - Complete technical specs
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official docs

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
