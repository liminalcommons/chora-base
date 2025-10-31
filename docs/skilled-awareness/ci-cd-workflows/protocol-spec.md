# Protocol Specification: CI/CD Workflows

**SAP ID**: SAP-005
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Overview

### Purpose

The ci-cd-workflows capability provides **GitHub Actions automation** for testing, quality checks, security scanning, and deployment. It defines workflow structure, triggers, quality gates, and integration patterns.

### Design Principles

1. **Matrix Testing** - Test across Python 3.11, 3.12, 3.13 for compatibility
2. **Caching First** - Cache pip dependencies to reduce execution time
3. **Parallel Execution** - Independent workflows run in parallel
4. **Security First** - CodeQL, dependency review always enabled
5. **Fast Feedback** - Target <5 min execution time for common workflows

---

## 2. Workflow Inventory

### 2.1 Core Workflows

**test.yml** - Test Matrix
- **Trigger**: push (main, develop), pull_request
- **Purpose**: Run pytest across Python versions, enforce coverage ≥85%
- **Matrix**: Python 3.11, 3.12, 3.13
- **Duration**: ~2-3 minutes
- **Required**: ✅ Must pass for merge

**lint.yml** - Code Quality
- **Trigger**: push (main, develop), pull_request
- **Purpose**: Run ruff (linting) and mypy (type checking)
- **Matrix**: Python 3.11 only
- **Duration**: ~1-2 minutes
- **Required**: ✅ Must pass for merge

**smoke.yml** - Smoke Tests
- **Trigger**: push (main, develop), pull_request
- **Purpose**: Quick validation (server starts, basic operations)
- **Matrix**: Python 3.11 only
- **Duration**: ~30-60 seconds
- **Required**: ✅ Must pass for merge

### 2.2 Documentation Workflows

**docs-quality.yml** - Documentation Validation
- **Trigger**: push (main, develop), pull_request, paths: ['**/*.md', 'docs/**']
- **Purpose**: Validate markdown, check links, verify structure
- **Matrix**: Single job
- **Duration**: ~1-2 minutes
- **Required**: ⚠️ Recommended (not blocking)

### 2.3 Security Workflows

**codeql.yml** - CodeQL Security Scanning
- **Trigger**: push (main, develop), pull_request, schedule (weekly)
- **Purpose**: Static security analysis, vulnerability detection
- **Matrix**: Single job
- **Duration**: ~3-5 minutes
- **Required**: ✅ Must pass for merge (security critical)

**dependency-review.yml** - Dependency Security
- **Trigger**: pull_request
- **Purpose**: Check new dependencies for vulnerabilities
- **Matrix**: Single job
- **Duration**: ~30-60 seconds
- **Required**: ✅ Must pass for merge (security critical)

### 2.4 Release Workflows

**release.yml** - Build and Publish
- **Trigger**: push (tags: 'v*'), workflow_dispatch
- **Purpose**: Build wheel, publish to PyPI (test + prod)
- **Matrix**: Python 3.11 only
- **Duration**: ~2-3 minutes
- **Required**: N/A (only for releases)

**dependabot-automerge.yml** - Dependabot Auto-Merge
- **Trigger**: pull_request (dependabot), workflow_run (test.yml success)
- **Purpose**: Auto-merge minor/patch Dependabot PRs after tests pass
- **Matrix**: Single job
- **Duration**: ~10-30 seconds
- **Required**: N/A (automation only)

---

## 3. Workflow Specifications

### 3.1 test.yml (Test Matrix)

**Full Specification**:

```yaml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests with coverage
        run: pytest --cov=src/{{ package_name }} --cov-report=xml --cov-report=term --cov-fail-under=85

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.11'
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

**Guarantees**:
- ✅ Tests run on Python 3.11, 3.12, 3.13
- ✅ Coverage measured and enforced (≥85%)
- ✅ Pip dependencies cached (faster subsequent runs)
- ✅ Coverage uploaded to Codecov (Python 3.11 only)
- ✅ Fails if tests fail OR coverage <85%

**Best Practices**:
1. **Matrix Testing**: Ensures compatibility across Python versions
2. **Caching**: `actions/cache@v4` caches ~/.cache/pip, keyed by pyproject.toml hash
3. **Selective Upload**: Coverage uploaded once (Python 3.11) to avoid duplicates
4. **fail_ci_if_error: false**: Don't fail if Codecov upload fails (graceful degradation)

### 3.2 lint.yml (Code Quality)

**Full Specification**:

```yaml
name: Lint

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run ruff (linting)
        run: ruff check .

      - name: Run mypy (type checking)
        run: mypy src
```

**Guarantees**:
- ✅ Ruff linting passes (no style violations)
- ✅ Mypy type checking passes (no type errors)
- ✅ Runs on Python 3.11 only (linting version-independent)

**Best Practices**:
1. **Single Python Version**: Linting doesn't need matrix (style is version-independent)
2. **Sequential Checks**: Ruff before mypy (ruff faster, fail fast)
3. **Caching**: Reuses pip cache from test workflow

### 3.3 codeql.yml (Security Scanning)

**Specification Summary**:
- **Languages**: Python
- **Queries**: security-extended (more comprehensive than default)
- **Schedule**: Weekly (cron: '0 0 * * 0')
- **Triggers**: push, pull_request, schedule

**Guarantees**:
- ✅ Static security analysis on every PR
- ✅ Weekly scheduled scans (catch new vulnerabilities)
- ✅ Security-extended query suite (comprehensive)
- ✅ Results visible in Security tab

---

## 4. Integration Contracts

### 4.1 With Testing Framework (SAP-004)

**test.yml uses SAP-004**:
```yaml
- name: Run tests with coverage
  run: pytest --cov=src/{{ package_name }} --cov-report=xml --cov-report=term --cov-fail-under=85
```

**Integration Points**:
- Uses pytest configuration from pyproject.toml (SAP-004)
- Enforces 85% coverage threshold (SAP-004 standard)
- Generates coverage report in format expected by SAP-004

### 4.2 With Quality Gates (SAP-006)

**lint.yml uses SAP-006**:
```yaml
- name: Run ruff (linting)
  run: ruff check .

- name: Run mypy (type checking)
  run: mypy src
```

**Integration Points**:
- Uses ruff configuration from pyproject.toml (SAP-006)
- Uses mypy configuration from pyproject.toml (SAP-006)
- Enforces same quality gates as pre-commit hooks (SAP-006)

### 4.3 With Project Bootstrap (SAP-003)

**Generated by SAP-003**:
- All workflow files in .github/workflows/ come from static-template
- Placeholders ({{ package_name }}) substituted during generation
- Workflow structure consistent across all generated projects

---

## 5. Workflow Execution Flow

### 5.1 On Pull Request

```
Developer: git push origin feature-branch
    │
    v
GitHub: Detects pull_request event
    │
    ├──► test.yml (parallel: Python 3.11, 3.12, 3.13)
    ├──► lint.yml (ruff + mypy)
    ├──► smoke.yml (quick validation)
    ├──► docs-quality.yml (if docs changed)
    ├──► codeql.yml (security scan)
    └──► dependency-review.yml (new dependencies)
    │
    v
All Required Workflows: ✅ Pass
    │
    v
Pull Request: Approved for merge
```

### 5.2 On Release

```
Maintainer: git tag v1.2.3 && git push --tags
    │
    v
GitHub: Detects tag push (v*)
    │
    v
release.yml:
    ├──► Build wheel (hatchling)
    ├──► Publish to TestPyPI (validate)
    ├──► Publish to PyPI (production)
    │
    v
Release: Published to PyPI
```

---

## 6. Best Practices

### 6.1 Caching Strategy

**pip Dependencies**:
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Benefits**:
- 30-60 second speedup per workflow run
- Cache key based on pyproject.toml hash (invalidates when dependencies change)
- Fallback to partial match if exact cache miss

### 6.2 Matrix Testing

**Python Versions**:
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

**Benefits**:
- Ensures compatibility across Python versions
- Runs in parallel (3 jobs simultaneously)
- Detects version-specific issues early

**Cost**:
- 3x execution time (but parallel, so same wall time)
- 3x GitHub Actions minutes

### 6.3 Security First

**Required Security Workflows**:
1. **codeql.yml**: Always enabled, never skip
2. **dependency-review.yml**: Always enabled for PRs
3. **Secrets scanning**: GitHub native (always on)

**Never**:
- ❌ Disable security workflows
- ❌ Skip CodeQL scans
- ❌ Ignore dependency vulnerabilities

---

## 7. Performance Optimization

### Current Performance

| Workflow | Duration | Optimization | Target |
|----------|----------|--------------|--------|
| test.yml (matrix) | ~2-3 min | Caching, parallel | <2 min |
| lint.yml | ~1-2 min | Caching | <1 min |
| smoke.yml | ~30-60s | Minimal deps | <30s |
| codeql.yml | ~3-5 min | Incremental analysis | <3 min |
| docs-quality.yml | ~1-2 min | Path filtering | <1 min |

**Total CI Time (PR)**: ~5 minutes (parallel execution)

### Optimization Techniques

1. **Path Filtering**: docs-quality.yml only runs when docs change
2. **Caching**: Pip cache reduces install time from 60s → 10s
3. **Parallel Jobs**: Matrix jobs run simultaneously
4. **Fail Fast**: Ruff runs before mypy (faster feedback)
5. **Selective Upload**: Coverage uploaded once, not 3 times

---

## 8. Error Handling

### Common Workflow Failures

**Test Failure**:
```
Error: Process completed with exit code 1.
##[error]pytest failed with exit code 1
```
**Cause**: Tests failed OR coverage <85%
**Recovery**: Check test output, fix failing tests or increase coverage

**Lint Failure**:
```
Error: Process completed with exit code 1.
##[error]ruff check . failed
```
**Cause**: Ruff found style violations
**Recovery**: Run `ruff check .` locally, fix issues, or run `ruff check --fix .`

**CodeQL Failure**:
```
Error: CodeQL analysis failed
```
**Cause**: Security vulnerability detected
**Recovery**: Review CodeQL results in Security tab, fix vulnerability

**Cache Miss**:
```
Cache not found for input keys: ubuntu-latest-pip-<hash>
```
**Cause**: pyproject.toml changed or first run
**Recovery**: Normal behavior, cache will be created

---

## 9. Related Documents

**SAP-005 Artifacts**:
- [capability-charter.md](capability-charter.md)
- [awareness-guide.md](awareness-guide.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [ledger.md](ledger.md)

**Workflow Files**:
- [.github/workflows/test.yml](/static-template/.github/workflows/test.yml)
- [.github/workflows/lint.yml](/static-template/.github/workflows/lint.yml)
- [.github/workflows/codeql.yml](/static-template/.github/workflows/codeql.yml)
- [All workflows](/static-template/.github/workflows/)

**Related SAPs**:
- [testing-framework/](../testing-framework/) - SAP-004
- [quality-gates/](../quality-gates/) - SAP-006
- [project-bootstrap/](../project-bootstrap/) - SAP-003

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for ci-cd-workflows
