# How to Integrate with GitHub Actions

**Goal:** Automate testing, validation, and content generation using GitHub Actions

**When to use this:** Setting up CI/CD pipelines for chora-compose projects

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [GitHub Actions Setup](#github-actions-setup)
4. [Automated Testing Pipeline](#automated-testing-pipeline)
5. [Content Generation in CI](#content-generation-in-ci)
6. [Deployment Workflows](#deployment-workflows)
7. [Example Workflows](#example-workflows)
8. [Secrets and Environment Variables](#secrets-and-environment-variables)

---

## Overview

GitHub Actions can automate:

- **Config validation** on pull requests
- **Test execution** on code changes
- **Content generation** on schedule or trigger
- **Artifact deployment** to production
- **Release publishing** to PyPI

### Benefits

- **Early error detection** - Catch issues before merge
- **Consistent testing** - Same environment every time
- **Automated deployment** - No manual intervention
- **Scheduled generation** - Nightly docs updates

---

## Quick Start

### Minimal Config Validation Workflow

Create `.github/workflows/validate-configs.yml`:

```yaml
name: Validate Configs

on:
  pull_request:
    paths:
      - 'configs/**/*.json'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Validate all configs
        run: poetry run chora-compose validate configs/
```

**What this does:**
- Triggers on PRs that change config files
- Validates all configs against schemas
- Fails PR if validation fails

---

## GitHub Actions Setup

### Directory Structure

```
your-repo/
├── .github/
│   └── workflows/
│       ├── validate-configs.yml
│       ├── test.yml
│       ├── generate-docs.yml
│       └── release.yml
├── configs/
│   ├── content/
│   └── artifact/
├── templates/
└── pyproject.toml
```

### Common Workflow Triggers

```yaml
# Run on push to main
on:
  push:
    branches: [main]

# Run on pull requests
on:
  pull_request:
    branches: [main, develop]

# Run on specific path changes
on:
  push:
    paths:
      - 'configs/**'
      - 'templates/**'
      - 'src/**'

# Run on schedule (nightly)
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily

# Run manually
on:
  workflow_dispatch:
    inputs:
      config_id:
        description: 'Config ID to generate'
        required: true
```

---

## Automated Testing Pipeline

### Complete Test Workflow

Create `.github/workflows/test.yml`:

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

      - name: Cache Poetry dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry
          key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
          restore-keys: |
            ${{ runner.os }}-poetry-

      - name: Install Poetry
        run: |
          python -m pip install --upgrade pip
          python -m pip install poetry

      - name: Install dependencies
        run: poetry install

      - name: Run tests with coverage
        run: |
          poetry run pytest \
            --cov=src/chora_compose \
            --cov-report=xml \
            --cov-report=term \
            --cov-fail-under=85

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.11'
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

      - name: Run type checking
        run: poetry run mypy src/chora_compose

      - name: Run linting
        run: poetry run ruff check src/chora_compose
```

**What this tests:**
- Unit tests across Python versions
- Code coverage (must be ≥85%)
- Type checking with mypy
- Linting with ruff

### Config Testing Workflow

Create `.github/workflows/test-configs.yml`:

```yaml
name: Test Configs

on:
  pull_request:
    paths:
      - 'configs/**/*.json'
      - 'templates/**/*'
  workflow_dispatch:

jobs:
  test-configs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Validate all configs (schema)
        run: poetry run chora-compose validate configs/

      - name: Test config generation (dry-run)
        run: |
          # Create script to test all configs
          cat > test_all_configs.py << 'EOF'
          #!/usr/bin/env python3
          import subprocess
          import json
          import sys
          from pathlib import Path

          configs = Path("configs/content").glob("*.json")
          failed = 0

          for config in configs:
              print(f"Testing {config}...")

              # Create draft
              result = subprocess.run(
                  ["poetry", "run", "chora-compose", "draft-config", "content", str(config)],
                  capture_output=True,
                  text=True
              )

              if result.returncode != 0:
                  print(f"  ✗ Failed: {result.stderr}")
                  failed += 1
                  continue

              # Extract draft ID
              for line in result.stdout.split("\n"):
                  if "Draft created:" in line:
                      draft_id = line.split()[-1]
                      break
              else:
                  print(f"  ✗ Could not find draft ID")
                  failed += 1
                  continue

              # Test config
              result = subprocess.run(
                  ["poetry", "run", "chora-compose", "test-config", draft_id],
                  capture_output=True,
                  text=True
              )

              if result.returncode != 0:
                  print(f"  ✗ Test failed: {result.stderr}")
                  failed += 1
              else:
                  print(f"  ✓ Passed")

          sys.exit(1 if failed > 0 else 0)
          EOF

          chmod +x test_all_configs.py
          python test_all_configs.py
```

---

## Content Generation in CI

### Scheduled Documentation Generation

Create `.github/workflows/generate-docs.yml`:

```yaml
name: Generate Documentation

on:
  # Run nightly at 2 AM UTC
  schedule:
    - cron: '0 2 * * *'

  # Allow manual trigger
  workflow_dispatch:
    inputs:
      artifact_id:
        description: 'Artifact ID to generate (optional, default: all)'
        required: false

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Generate all artifacts
        run: |
          # Generate each artifact config
          for config in configs/artifact/*.json; do
            echo "Generating: $config"
            poetry run chora-compose compose "$config"
          done

      - name: Check for changes
        id: changes
        run: |
          git diff --quiet dist/ || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Commit generated docs
        if: steps.changes.outputs.changed == 'true'
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add dist/
          git commit -m "chore: regenerate documentation [skip ci]"
          git push
```

**What this does:**
- Runs nightly (or on demand)
- Generates all artifacts
- Commits changes back to repo (if any)

### PR Preview Generation

Create `.github/workflows/pr-preview.yml`:

```yaml
name: PR Preview

on:
  pull_request:
    paths:
      - 'configs/**'
      - 'templates/**'

jobs:
  preview:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Generate preview
        run: |
          # Generate to preview directory
          mkdir -p preview/
          for config in configs/artifact/*.json; do
            poetry run chora-compose compose "$config"
          done

          # Copy generated artifacts to preview
          cp -r dist/* preview/

      - name: Upload preview artifacts
        uses: actions/upload-artifact@v4
        with:
          name: preview-docs
          path: preview/
          retention-days: 7

      - name: Comment PR with preview link
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const previewFiles = fs.readdirSync('preview/');

            const comment = `
            ## 📄 Documentation Preview

            Generated documentation preview for this PR:

            ${previewFiles.map(f => `- \`${f}\``).join('\n')}

            Download artifacts to review changes.
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.name,
              body: comment
            });
```

---

## Deployment Workflows

### Release to PyPI

Based on chora-compose's `.github/workflows/release.yml`:

```yaml
name: Release to PyPI

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags (v0.1.0, v1.0.0, etc.)

permissions:
  contents: write

jobs:
  build:
    name: Build distribution packages
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build distribution packages
        run: python -m build

      - name: Check distribution packages
        run: twine check dist/*

      - name: Upload distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: python-package-distributions
          path: dist/
          retention-days: 7

  test:
    name: Run tests before release
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run smoke tests
        run: ./scripts/smoke-test.sh
        timeout-minutes: 2

      - name: Run full test suite
        run: pytest --cov=src/chora_compose --cov-report=term

  publish-pypi:
    name: Publish to PyPI
    needs: [build, test]
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/chora-compose

    steps:
      - name: Download distribution artifacts
        uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}
          print-hash: true

  github-release:
    name: Create GitHub Release
    needs: [publish-pypi]
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
          files: |
            CHANGELOG.md
```

**Trigger:**
```bash
# Create and push version tag
git tag v1.2.3
git push origin v1.2.3

# GitHub Actions will:
# 1. Build package
# 2. Run tests
# 3. Publish to PyPI
# 4. Create GitHub release
```

### Deploy Artifacts to GitHub Pages

Create `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Docs to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'configs/artifact/documentation-site.json'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Generate documentation site
        run: |
          poetry run chora-compose compose configs/artifact/documentation-site.json

      - name: Upload artifact for deployment
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist/docs/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Example Workflows

### Example 1: Validate on PR, Generate on Merge

```yaml
name: CI/CD Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  # Run on PR: Validate only
  validate:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Validate configs
        run: poetry run chora-compose validate configs/

      - name: Test configs (dry-run)
        run: python scripts/test_all_configs.py

  # Run on merge: Generate and deploy
  generate:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Generate all artifacts
        run: |
          for config in configs/artifact/*.json; do
            poetry run chora-compose compose "$config"
          done

      - name: Deploy artifacts
        run: |
          # Your deployment logic here
          # e.g., rsync to server, upload to S3, etc.
```

### Example 2: Multi-Environment Deployment

```yaml
name: Multi-Environment Deploy

on:
  push:
    tags:
      - 'v*-dev'
      - 'v*-staging'
      - 'v*-prod'

jobs:
  determine-environment:
    runs-on: ubuntu-latest
    outputs:
      environment: ${{ steps.parse.outputs.environment }}

    steps:
      - name: Parse environment from tag
        id: parse
        run: |
          TAG=${GITHUB_REF#refs/tags/}
          if [[ $TAG == *-dev ]]; then
            echo "environment=dev" >> $GITHUB_OUTPUT
          elif [[ $TAG == *-staging ]]; then
            echo "environment=staging" >> $GITHUB_OUTPUT
          elif [[ $TAG == *-prod ]]; then
            echo "environment=prod" >> $GITHUB_OUTPUT
          fi

  deploy:
    needs: determine-environment
    runs-on: ubuntu-latest
    environment:
      name: ${{ needs.determine-environment.outputs.environment }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Generate with environment context
        run: |
          export ENVIRONMENT=${{ needs.determine-environment.outputs.environment }}
          poetry run chora-compose compose configs/artifact/api-docs.json

      - name: Deploy to ${{ needs.determine-environment.outputs.environment }}
        run: |
          echo "Deploying to ${{ needs.determine-environment.outputs.environment }}..."
          # Environment-specific deployment logic
```

**Usage:**
```bash
# Deploy to dev
git tag v1.2.3-dev
git push origin v1.2.3-dev

# Deploy to staging
git tag v1.2.3-staging
git push origin v1.2.3-staging

# Deploy to production
git tag v1.2.3-prod
git push origin v1.2.3-prod
```

---

## Secrets and Environment Variables

### Required Secrets

Set these in GitHub repository settings → Secrets and variables → Actions:

**For PyPI Publishing:**
- `PYPI_TOKEN` - PyPI API token for package publishing

**For API-based Generators:**
- `ANTHROPIC_API_KEY` - For AI-powered generation
- `OPENAI_API_KEY` - If using OpenAI

**For Deployment:**
- `DEPLOY_SSH_KEY` - SSH key for server deployment
- `AWS_ACCESS_KEY_ID` - For S3 deployment
- `AWS_SECRET_ACCESS_KEY` - For S3 deployment

### Using Secrets in Workflows

```yaml
jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: poetry install

      - name: Generate content with AI
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # API key available as environment variable
          poetry run chora-compose compose configs/artifact/ai-generated-content.json
```

### Environment Variables

```yaml
jobs:
  generate:
    runs-on: ubuntu-latest
    env:
      # Global environment variables
      CHORA_TRACE_ID: ${{ github.run_id }}
      ENVIRONMENT: production

    steps:
      - name: Generate with context
        run: |
          # Environment variables available to all steps
          poetry run chora-compose compose configs/artifact/api-docs.json
```

### Context Variables

Access GitHub context in workflows:

```yaml
- name: Generate with GitHub context
  run: |
    poetry run chora-compose compose configs/artifact/release-notes.json
  env:
    GIT_SHA: ${{ github.sha }}
    GIT_REF: ${{ github.ref }}
    PR_NUMBER: ${{ github.event.pull_request.number }}
    ACTOR: ${{ github.actor }}
```

**Use in templates:**
```jinja2
# Release Notes

Version: {{ version }}
Git SHA: {{ env.GIT_SHA }}
Released by: {{ env.ACTOR }}
```

---

## Best Practices

### 1. Cache Dependencies

```yaml
# ✓ Good: Cache Poetry dependencies
- name: Cache Poetry dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pypoetry
    key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}

# ✗ Bad: No caching (slower builds)
```

### 2. Use Matrix Builds for Testing

```yaml
# ✓ Good: Test across Python versions
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]

# ✗ Bad: Only test one version
```

### 3. Fail Fast on Errors

```yaml
# ✓ Good: Explicit error handling
- name: Validate configs
  run: poetry run chora-compose validate configs/ || exit 1

# ✗ Bad: Continue on error
- name: Validate configs
  run: poetry run chora-compose validate configs/ || true
```

### 4. Use Specific Action Versions

```yaml
# ✓ Good: Pinned version
uses: actions/checkout@v4

# ✗ Bad: Latest (may break)
uses: actions/checkout@latest
```

### 5. Add Timeouts

```yaml
# ✓ Good: Timeout prevents hanging jobs
- name: Generate content
  run: poetry run chora-compose compose configs/artifact/large-doc.json
  timeout-minutes: 10

# ✗ Bad: No timeout (may hang forever)
```

---

## Related Documentation

- [Test Configs Before Deployment](../testing/test-configs-before-deployment.md) - Pre-deployment testing
- [Validate Generated Content](../testing/validate-generated-content.md) - Post-generation validation
- [Testing Philosophy](../../explanation/testing/testing-philosophy.md) - Testing approach
- [Deploy Without Docker](../deployment/deploy-without-docker.md) - Native deployment
