# Tutorial: Customizing GitHub Actions Workflows

**Difficulty**: Intermediate
**Time**: 45-60 minutes
**Prerequisites**: Understanding of YAML, basic GitHub Actions knowledge

---

## Introduction

Learn how to safely customize the GitHub Actions workflows provided by chora-base to match your project's specific needs.

### What You'll Learn

- How to modify workflow triggers
- Adding custom workflow steps
- Configuring matrix builds
- Adding secrets and environment variables
- Best practices for workflow customization

---

## Understanding Workflow Structure

### Anatomy of a Workflow File

**File**: `.github/workflows/test.yml`

```yaml
name: Test                    # Workflow name (shown in Actions tab)

on:                          # Triggers
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:                        # Jobs (run in parallel by default)
  test:                      # Job ID
    runs-on: ubuntu-latest   # Runner OS
    strategy:                # Build matrix
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:                   # Steps (run sequentially)
      - name: Checkout
        uses: actions/checkout@v4     # Pre-built action

      - name: Run tests
        run: pytest                   # Shell command
```

**Key concepts**:
- **name**: Display name
- **on**: What triggers the workflow (push, PR, schedule, manual)
- **jobs**: Parallel units of work
- **steps**: Sequential commands within a job
- **uses**: Pre-built actions from marketplace
- **run**: Raw shell commands

---

## Common Customizations

### 1. Adding a New Python Version

**Scenario**: Your project now supports Python 3.14

**File**: `.github/workflows/test.yml`

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13", "3.14"]  # Add 3.14
```

**Test locally first**:
```bash
pyenv install 3.14.0
pyenv local 3.14.0
pytest
```

---

### 2. Running Tests on Multiple Operating Systems

**Scenario**: Support macOS and Windows users

**Before**:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest  # Linux only
```

**After**:
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]
```

**Result**: 9 test runs (3 OS × 3 Python versions)

**Optimization** (if too slow):
```yaml
strategy:
  matrix:
    os: [ubuntu-latest]
    python-version: ["3.11", "3.12", "3.13"]
    include:
      # Only test Python 3.11 on macOS/Windows
      - os: macos-latest
        python-version: "3.11"
      - os: windows-latest
        python-version: "3.11"
```

**Result**: 5 test runs (3 Linux + 1 macOS + 1 Windows)

---

### 3. Adding Environment Variables

**Scenario**: Tests need API keys or configuration

**Using secrets**:
```yaml
steps:
  - name: Run tests
    run: pytest
    env:
      API_KEY: ${{ secrets.API_KEY }}           # From GitHub Secrets
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**Set secrets**: GitHub repo → Settings → Secrets and variables → Actions → New repository secret

**Using environment files**:
```yaml
steps:
  - name: Create .env file
    run: |
      echo "API_KEY=${{ secrets.API_KEY }}" > .env
      echo "DEBUG=False" >> .env

  - name: Run tests
    run: pytest  # Loads .env automatically
```

---

### 4. Adding Custom Test Commands

**Scenario**: Run integration tests separately

**Add new job**:
```yaml
jobs:
  test:
    # ... existing test job

  integration-test:
    runs-on: ubuntu-latest
    needs: test  # Only run if test job passes
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest tests/integration --maxfail=1
    services:
      postgres:  # Spin up database for integration tests
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
```

---

### 5. Conditional Steps

**Scenario**: Only upload coverage on main branch

```yaml
- name: Upload coverage
  if: github.ref == 'refs/heads/main' && matrix.python-version == '3.11'
  uses: codecov/codecov-action@v4
```

**Common conditions**:
```yaml
if: github.event_name == 'push'              # Only on push (not PR)
if: github.ref == 'refs/heads/main'          # Only on main branch
if: contains(github.event.head_commit.message, '[docs]')  # Commit message contains [docs]
if: success()                                # Previous step succeeded
if: failure()                                # Previous step failed
if: always()                                 # Run regardless of previous step
```

---

### 6. Adding Manual Workflow Dispatch

**Scenario**: Trigger workflows on-demand

**Add to triggers**:
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:  # Enable manual trigger
    inputs:
      python-version:
        description: 'Python version to test'
        required: false
        default: '3.11'
```

**Use input in job**:
```yaml
jobs:
  test:
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version || '3.11' }}
```

**Trigger manually**: Actions tab → Select workflow → "Run workflow" button

---

### 7. Caching Custom Dependencies

**Scenario**: Cache poetry or conda dependencies

**Poetry**:
```yaml
- name: Cache poetry dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pypoetry
    key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
```

**Conda**:
```yaml
- name: Cache conda
  uses: actions/cache@v4
  with:
    path: ~/conda_pkgs_dir
    key: ${{ runner.os }}-conda-${{ hashFiles('environment.yml') }}
```

---

### 8. Running Tests in Docker

**Scenario**: Test in production-like environment

```yaml
jobs:
  docker-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myproject:test .

      - name: Run tests in container
        run: docker run myproject:test pytest --cov=src

      - name: Copy coverage out of container
        run: |
          docker create --name temp myproject:test
          docker cp temp:/app/coverage.xml .
          docker rm temp

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

---

## Advanced Patterns

### Reusable Workflows

**Create shared workflow** (`.github/workflows/reusable-test.yml`):
```yaml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest
```

**Call from another workflow**:
```yaml
jobs:
  call-reusable:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: "3.11"
```

---

### Composite Actions

**Create custom action** (`.github/actions/setup-project/action.yml`):
```yaml
name: 'Setup Project'
description: 'Install Python and project dependencies'
inputs:
  python-version:
    description: 'Python version'
    required: true

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
    - run: pip install -e ".[dev]"
      shell: bash
    - run: pre-commit install
      shell: bash
```

**Use in workflow**:
```yaml
steps:
  - uses: ./.github/actions/setup-project
    with:
      python-version: "3.11"
```

---

## Best Practices

### 1. Validate Before Committing

```bash
# Install actionlint
brew install actionlint  # macOS
# or
go install github.com/rhysd/actionlint/cmd/actionlint@latest

# Validate workflow files
actionlint .github/workflows/*.yml
```

### 2. Use Specific Action Versions

**Bad** (breaks when action updates):
```yaml
- uses: actions/checkout@v4  # Major version (can break)
```

**Good** (pinned to exact version):
```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

**Get commit SHA**: Visit action repo → Releases → Copy commit SHA

### 3. Fail Fast

```yaml
strategy:
  fail-fast: true  # Stop all jobs if one fails (default)
  # or
  fail-fast: false  # Run all jobs even if some fail
```

### 4. Set Timeouts

```yaml
jobs:
  test:
    timeout-minutes: 10  # Kill job if runs >10 minutes
```

### 5. Use Job Outputs

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

  report:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Coverage was ${{ needs.test.outputs.coverage }}"
```

---

## Troubleshooting

### Workflow Not Triggering

**Check**:
1. YAML syntax: `actionlint .github/workflows/test.yml`
2. File location: Must be in `.github/workflows/`
3. Branch matches trigger: `branches: [main]` but you're on `develop`

### Secrets Not Available in PR from Forks

**Issue**: `${{ secrets.API_KEY }}` is empty in fork PRs (security feature)

**Solution**:
```yaml
- name: Run tests
  if: github.event.pull_request.head.repo.full_name == github.repository
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

### Workflow Runs Twice

**Cause**: Both `push` and `pull_request` triggers

**Fix**:
```yaml
on:
  push:
    branches: [main]  # Only on direct pushes to main
  pull_request:
    branches: [main]  # Only on PRs to main
```

---

## Related Documentation

- [GitHub Actions Guide](../guides/github-actions.md) - General workflow usage
- [Debugging CI Failures](debugging-ci-failures.md) - Troubleshooting failed workflows
- [Workflow Reference](../reference/workflow-reference.md) - Complete YAML reference
- [GitHub Actions Docs](https://docs.github.com/en/actions) - Official documentation

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
