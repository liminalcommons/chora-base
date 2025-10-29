---
sap_id: SAP-008
version: 1.0.0
status: Draft
last_updated: 2025-10-28
type: how-to
audience: developers, ai-agents
---

# Adoption Blueprint: Automation Scripts

**SAP ID**: SAP-008
**For**: Projects adopting automation scripts and justfile interface
**Purpose**: Step-by-step guide to implement script automation

---

## 1. Overview

This blueprint helps projects adopt **25 automation scripts** with **justfile as the unified interface**.

**Adoption Benefits**:
- 80% reduction in script-related onboarding time
- 100% idempotent scripts (safe to re-run)
- Consistent error handling across all scripts
- Unified developer interface (`just <task>`)

**Prerequisites**: chora-base generated project (includes all scripts and justfile)

---

## 2. Adoption Levels

### Level 1: Basic Usage (Day 1)
- Learn justfile interface (`just --list`, `just help`)
- Use core commands (`just test`, `just pre-merge`)
- Understand script safety classifications

**Time**: 30 minutes
**Goal**: Productive immediately without deep script knowledge

---

### Level 2: Standard Usage (Week 1)
- Use all script categories (setup, testing, building, release)
- Understand idempotency patterns
- Customize justfile for project-specific tasks

**Time**: 2 hours over first week
**Goal**: Proficient with all automation workflows

---

### Level 3: Advanced Usage (Month 1)
- Write custom scripts following chora-base patterns
- Integrate scripts with CI/CD (SAP-005)
- Validate script robustness

**Time**: 4 hours over first month
**Goal**: Extend automation for project-specific needs

---

## 3. Level 1: Basic Usage (Day 1)

### 3.1 Install Just

**macOS**:
```bash
brew install just
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt install just

# Arch
sudo pacman -S just

# Or via cargo
cargo install just
```

**Verify installation**:
```bash
just --version
# Expected: just 1.14.0 (or newer)
```

---

### 3.2 Learn Justfile Interface

**List all available commands**:
```bash
cd /path/to/your/project
just --list
```

**Output** (example):
```
Available recipes:
    build               # Build distribution packages
    bump-patch          # Bump patch version
    lint                # Check code style
    pre-merge           # Run all pre-merge checks
    test                # Run all tests
    (... 25+ more commands)
```

**Show common workflows**:
```bash
just help
```

**Output**:
```
=== your-project - Development Commands ===

Quick validation:
  just test           # Run test suite (~1 min)
  just smoke          # Quick smoke tests (~10 sec)
  just lint           # Check code style

Before creating PR:
  just pre-merge      # Run all checks (required)

Building & releasing:
  just build          # Build distribution packages
  just prepare patch  # Prepare patch release

Full command list:
  just --list
```

---

### 3.3 Core Commands (Memorize These 5)

#### 1. `just test` - Run Tests
**When**: During development, after making changes
**Time**: ~1 minute

```bash
just test
```

**What it does**:
- Runs all pytest tests
- Shows pass/fail for each test
- Exit code 0 (pass) or 1 (fail)

---

#### 2. `just smoke` - Quick Validation
**When**: Rapid feedback loop (every 5-10 minutes)
**Time**: ~10 seconds

```bash
just smoke
```

**What it does**:
- Runs subset of fast tests (marked with `@pytest.mark.smoke`)
- Verifies imports work
- Verifies CLI works (if applicable)

---

#### 3. `just lint` - Check Code Style
**When**: Before committing
**Time**: ~5 seconds

```bash
just lint
```

**What it does**:
- Runs ruff linter
- Shows style violations
- Exit code 0 (clean) or 1 (violations)

**Auto-fix** (if violations found):
```bash
just lint-fix
```

---

#### 4. `just pre-merge` - All Quality Gates
**When**: **ALWAYS** before creating pull request
**Time**: ~2 minutes

```bash
just pre-merge
```

**What it does**:
- Runs pre-commit hooks (all files)
- Runs smoke tests
- Runs full test suite with coverage check (≥85%)
- Checks CHANGELOG.md updated
- Checks no uncommitted changes (warning)
- Checks version (informational)

**Exit code 0**: Ready for PR
**Exit code 1**: Fix issues, re-run

---

#### 5. `just help` - Show Common Workflows
**When**: Forgot a command or learning
**Time**: Instant

```bash
just help
```

---

### 3.4 Script Safety Classifications

**Understand safety before running**:

#### ✅ Read-Only (Safe to run anytime)
- `just check-env` - Validate environment
- `just smoke` - Quick tests
- `just test` - Run tests
- `just lint` - Check code style
- `just docs-validate` - Validate documentation

**Characteristic**: No side effects, can run freely

---

#### ✅ Idempotent (Safe to re-run)
- `just install` - Install dependencies (skips if installed)
- `just setup-hooks` - Install pre-commit hooks (skips if installed)
- `just venv-create` - Create venv (skips if exists)
- `just build` - Build packages (cleans dist/ first)
- `just bump-patch` - Bump version (checks current first)

**Characteristic**: Can run multiple times, produces same result

---

#### ⚠️ Destructive (Require confirmation)
- `just venv-clean` - Deletes venv/ (prompts: "Delete venv/? (y/N)")
- `just rollback` - Stashes changes (prompts: "Rollback? (y/N)")
- `just publish-prod` - Publishes to PyPI (prompts: "Publish to production? (y/N)")

**Characteristic**: Prompts for user confirmation before destructive action

---

#### 🔒 Non-Idempotent (Run once per version)
- `just publish-test` - Publish to test PyPI (fails if version exists)
- `just publish-prod` - Publish to production PyPI (fails if version exists)

**Characteristic**: Cannot re-run for same version (PyPI immutable)

---

### 3.5 Your First Day Workflow

**Morning: Start work on feature**:
```bash
# 1. Verify environment OK
just check-env

# 2. Work on code...
# (edit files in src/)

# 3. Run tests frequently
just test

# 4. Quick validation
just smoke
```

**Afternoon: Commit work**:
```bash
# 5. Check code style
just lint

# 6. Auto-fix style issues
just lint-fix

# 7. Run all quality gates
just pre-merge

# 8. If pass, commit
git add .
git commit -m "feat: Add feature X"
```

**End of day: Create PR**:
```bash
# 9. Push to remote
git push origin feature/feature-x

# 10. Create PR (quality gates already passed)
gh pr create --title "feat: Add feature X" --body "..."
```

---

## 4. Level 2: Standard Usage (Week 1)

### 4.1 All Script Categories

#### Category 1: Setup & Environment

**Initial setup** (first time in project):
```bash
# Install dependencies (pip install -e ".[dev]")
just install

# Install pre-commit hooks
just setup-hooks

# Verify environment
just check-env
```

**Environment issues** (troubleshooting):
```bash
# Diagnose issues
just diagnose

# Clean and recreate venv (if corrupted)
just venv-clean

# Create venv (if missing)
just venv-create
```

---

#### Category 2: Testing

**During development**:
```bash
# Run all tests
just test

# Run with coverage report (HTML + terminal)
just test-coverage

# Quick smoke tests
just smoke
```

**Before PR**:
```bash
# Run all quality gates
just pre-merge
```

---

#### Category 3: Quality

**Code quality checks**:
```bash
# Linting
just lint              # Check code style
just lint-fix          # Auto-fix issues

# Formatting
just format            # Format code with ruff

# Type checking
just type-check        # Run mypy
```

---

#### Category 4: Building & Releasing

**Version management**:
```bash
# Bump version (updates pyproject.toml, __init__.py, CHANGELOG.md)
just bump-patch        # 1.0.0 → 1.0.1 (bug fixes)
just bump-minor        # 1.0.0 → 1.1.0 (new features)
just bump-major        # 1.0.0 → 2.0.0 (breaking changes)
```

**Release workflow**:
```bash
# 1. Prepare release (run all checks)
just prepare patch

# 2. Build distribution packages
just build

# 3. Publish to test PyPI (optional, for testing)
just publish-test

# 4. Publish to production PyPI
just publish-prod
```

---

#### Category 5: Documentation

**Documentation workflows**:
```bash
# Validate documentation (frontmatter, links)
just docs-validate

# Calculate documentation metrics (coverage, staleness)
just docs-metrics

# Generate documentation sitemap
just docs-map
```

---

#### Category 6: Safety & Recovery

**Safety nets**:
```bash
# Diagnose environment issues
just diagnose

# Rollback uncommitted changes (git stash)
just rollback
```

---

### 4.2 Understanding Idempotency

**Key Principle**: Idempotent scripts can be run multiple times safely

#### Example 1: `just venv-create` (Idempotent)

**First run** (venv doesn't exist):
```bash
just venv-create
# Creates venv/
# Installs dependencies
# Exit code: 0
```

**Second run** (venv exists):
```bash
just venv-create
# Checks: venv/ exists
# Skips creation
# Message: "Virtual environment already exists. Skipping."
# Exit code: 0
```

**Why idempotent**: Check-before-act pattern

---

#### Example 2: `just build` (Idempotent)

**First run**:
```bash
just build
# Cleans old dist/
# Builds new packages
# Exit code: 0
```

**Second run**:
```bash
just build
# Cleans old dist/
# Builds new packages (same result)
# Exit code: 0
```

**Why idempotent**: Cleanup-before-create pattern

---

#### Example 3: `just bump-patch` (Idempotent)

**First run** (version 1.0.0):
```bash
just bump-patch
# Bumps to 1.0.1
# Updates files
# Exit code: 0
```

**Second run** (version 1.0.1):
```bash
just bump-patch
# Bumps to 1.0.2
# Updates files
# Exit code: 0
```

**Why idempotent**: Reads current version, calculates next

---

### 4.3 Customize Justfile

**Add project-specific tasks**:

```makefile
# Open your justfile
vim justfile

# Add custom tasks at the end
# Example: Run your app locally
run:
    python -m {{ package_name }}

# Example: Watch tests (rerun on file change)
watch:
    pytest-watch

# Example: Deploy to staging
deploy-staging:
    ./scripts/deploy.sh staging

# Example: Generate API docs
docs-api:
    sphinx-build -b html docs/ docs/_build/
```

**Use custom tasks**:
```bash
just run
just watch
just deploy-staging
just docs-api
```

---

### 4.4 Your First Week Workflows

#### Workflow 1: Feature Development (Day 1-3)

```bash
# Day 1: Start feature
just test               # Baseline (all pass)
# (code feature)
just smoke              # Quick validation
just test               # Full validation

# Day 2: Continue feature
# (code more)
just test
just lint-fix
just pre-merge          # Before committing

# Day 3: Finish feature
# (final touches)
just test-coverage      # Verify coverage ≥85%
just pre-merge
git commit -m "feat: Feature X complete"
```

---

#### Workflow 2: Bug Fix (Day 4)

```bash
# Bug reported
just test               # Reproduce bug (test fails)
# (write failing test)
# (fix bug)
just test               # Test passes
just pre-merge
git commit -m "fix: Bug Y fixed"
```

---

#### Workflow 3: Release (Day 5)

```bash
# Release day
just bump-minor         # 1.0.0 → 1.1.0
# (update CHANGELOG.md)
just prepare minor      # Run all checks
just build              # Build packages
just publish-test       # Test on test.pypi.org
# (verify test install works)
just publish-prod       # Publish to production
# (verify on pypi.org)
```

---

## 5. Level 3: Advanced Usage (Month 1)

### 5.1 Write Custom Scripts

**Follow chora-base patterns**:

#### Pattern 1: Shell Script Template

```bash
#!/usr/bin/env bash
# my-custom-script.sh - Brief description
#
# Usage: ./scripts/my-custom-script.sh [args]
#
# Description: What this script does.
#
# Examples:
#   ./scripts/my-custom-script.sh           # Default
#   ./scripts/my-custom-script.sh --option  # With option
#
# Safety: [Idempotent | Destructive | Read-only | Stateful]
# Rollback: [Yes | No | N/A]

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Validate inputs
ARG="${1:-}"
if [ -z "$ARG" ]; then
    echo -e "${RED}Error: Argument required${NC}"
    echo "Usage: $0 <arg>"
    exit 1
fi

# Check preconditions
if [ ! -f "required-file.txt" ]; then
    echo -e "${RED}Error: required-file.txt not found${NC}"
    echo "Run: ./scripts/setup.sh first"
    exit 1
fi

# Main logic (with error handling)
echo -e "${YELLOW}Running operation...${NC}"
if ! some_command "$ARG"; then
    echo -e "${RED}Error: Operation failed${NC}"
    echo "To fix: Check logs and retry"
    exit 1
fi

echo -e "${GREEN}✓${NC} Operation completed successfully"
exit 0
```

---

#### Pattern 2: Python Script Template

```python
#!/usr/bin/env python3
"""
my-custom-script.py - Brief description

Usage: python scripts/my-custom-script.py [--option]

Description: What this script does.

Examples:
    python scripts/my-custom-script.py
    python scripts/my-custom-script.py --verbose

Safety: [Idempotent | Destructive | Read-only | Stateful]
Rollback: [Yes | No | N/A]
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="My custom script")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Validate preconditions
    required_file = Path("required-file.txt")
    if not required_file.exists():
        print(f"Error: {required_file} not found", file=sys.stderr)
        print("Run: ./scripts/setup.sh first", file=sys.stderr)
        return 1

    # Main logic (with error handling)
    try:
        # Your code here
        if args.verbose:
            print("Processing...")

        # Operation
        result = some_operation()

        print(f"✓ Operation completed: {result}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

### 5.2 Integrate Scripts with Justfile

**Add your custom script to justfile**:

```makefile
# my-custom-task: Brief description
my-custom-task ARG:
    ./scripts/my-custom-script.sh {{ARG}}

# Another custom task (Python script)
analyze:
    python scripts/analyze.py --verbose

# Task with dependencies (run other tasks first)
full-analysis: lint test
    python scripts/analyze.py
```

**Use your custom tasks**:
```bash
just my-custom-task value
just analyze
just full-analysis
```

---

### 5.3 Validate Script Robustness

**Checklist for custom scripts**:

#### 1. Idempotency Test
```bash
# Run script twice, verify second run succeeds or skips
./scripts/my-custom-script.sh arg
./scripts/my-custom-script.sh arg  # Should succeed or skip, not fail
```

---

#### 2. Error Handling Test
```bash
# Test missing arguments
./scripts/my-custom-script.sh
# Expected: Clear error message + usage, exit code 1

# Test missing preconditions
rm required-file.txt
./scripts/my-custom-script.sh arg
# Expected: Clear error about missing file + remedy, exit code 1
```

---

#### 3. Exit Code Test
```bash
# Success case
./scripts/my-custom-script.sh valid-arg
echo $?
# Expected: 0

# Failure case
./scripts/my-custom-script.sh invalid-arg
echo $?
# Expected: 1 (or other non-zero)
```

---

#### 4. Documentation Test
```bash
# Verify header comments present
head -20 scripts/my-custom-script.sh
# Expected: Usage, description, examples, safety, rollback
```

---

#### 5. Safety Flags Test (Bash only)
```bash
# Verify 'set -euo pipefail' present
grep "set -euo pipefail" scripts/my-custom-script.sh
# Expected: Match found
```

---

### 5.4 Integrate with CI/CD

**Add scripts to GitHub Actions workflows**:

```yaml
# .github/workflows/custom-checks.yml
name: Custom Checks

on: [push, pull_request]

jobs:
  custom-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Just
        run: |
          curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
          echo "$HOME/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: just install

      - name: Run custom checks
        run: just my-custom-task arg
```

---

### 5.5 Your First Month Advanced Workflows

#### Workflow 1: Custom Deployment Script

**Goal**: Add deployment script with rollback support

**Step 1: Create script**:
```bash
cat > scripts/deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh - Deploy to staging or production
#
# Usage: ./scripts/deploy.sh <staging|production>
#
# Safety: Stateful (makes changes to remote servers)
# Rollback: Yes (saves previous version, can rollback)

set -euo pipefail

ENV="${1:-}"
if [[ ! "$ENV" =~ ^(staging|production)$ ]]; then
    echo "Error: Invalid environment '$ENV'"
    echo "Usage: $0 <staging|production>"
    exit 1
fi

# Save current version for rollback
CURRENT_VERSION=$(git describe --tags --abbrev=0)
echo "Current version: $CURRENT_VERSION" > .last-deploy

# Deploy
echo "Deploying to $ENV..."
# (your deployment logic here)

echo "✓ Deployed to $ENV"
echo "To rollback: ./scripts/rollback-deploy.sh"
EOF

chmod +x scripts/deploy.sh
```

**Step 2: Add to justfile**:
```makefile
# Deploy to staging
deploy-staging:
    ./scripts/deploy.sh staging

# Deploy to production (requires confirmation)
deploy-production:
    ./scripts/deploy.sh production

# Rollback deployment
rollback-deploy:
    ./scripts/rollback-deploy.sh
```

**Step 3: Use**:
```bash
just deploy-staging
just deploy-production
```

---

#### Workflow 2: Custom Code Generation Script

**Goal**: Generate boilerplate code from templates

**Step 1: Create script**:
```python
#!/usr/bin/env python3
"""
generate-module.py - Generate module boilerplate

Usage: python scripts/generate-module.py <module-name>

Safety: Idempotent (checks if module exists)
"""

import sys
from pathlib import Path

def generate_module(name: str) -> int:
    """Generate module boilerplate."""
    module_dir = Path(f"src/{name}")

    # Idempotency check
    if module_dir.exists():
        print(f"Module '{name}' already exists. Skipping.")
        return 0

    # Create module structure
    module_dir.mkdir(parents=True)
    (module_dir / "__init__.py").write_text(f'"""Module: {name}"""\n')
    (module_dir / "main.py").write_text(f'"""Main module for {name}."""\n\ndef main() -> None:\n    """Entry point."""\n    pass\n')

    # Create tests
    test_dir = Path(f"tests/{name}")
    test_dir.mkdir(parents=True)
    (test_dir / "__init__.py").write_text("")
    (test_dir / "test_main.py").write_text(f'"""Tests for {name}.main."""\n\ndef test_main():\n    """Test main function."""\n    pass\n')

    print(f"✓ Module '{name}' created")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate-module.py <module-name>")
        sys.exit(1)

    sys.exit(generate_module(sys.argv[1]))
```

**Step 2: Add to justfile**:
```makefile
# Generate module boilerplate
generate-module NAME:
    python scripts/generate-module.py {{NAME}}
```

**Step 3: Use**:
```bash
just generate-module my_feature
# Creates:
# src/my_feature/__init__.py
# src/my_feature/main.py
# tests/my_feature/__init__.py
# tests/my_feature/test_main.py
```

---

## 6. Troubleshooting

### Problem 1: "Just command not found"

**Symptom**: `bash: just: command not found`

**Fix**:
```bash
# macOS
brew install just

# Linux (Ubuntu/Debian)
sudo apt install just

# Or via cargo
cargo install just
```

---

### Problem 2: "Script not executable"

**Symptom**: `Permission denied: ./scripts/my-script.sh`

**Fix**:
```bash
chmod +x scripts/my-script.sh
```

---

### Problem 3: "Script fails with 'set -u: unbound variable'"

**Symptom**: Script exits with unbound variable error

**Root Cause**: Using variable that might not be set

**Fix**:
```bash
# Wrong
ARG=$1  # Fails if no argument provided

# Correct (provide default)
ARG="${1:-default_value}"

# Or check explicitly
if [ -z "${1:-}" ]; then
    echo "Error: Argument required"
    exit 1
fi
ARG="$1"
```

---

### Problem 4: "Justfile task not found"

**Symptom**: `error: Justfile does not contain recipe 'task-name'`

**Fix**:
```bash
# List all available tasks
just --list

# Verify task name spelling

# If task missing, add to justfile
echo "task-name:\n    ./scripts/task-name.sh" >> justfile
```

---

### Problem 5: "Script hangs waiting for input"

**Symptom**: Script runs but doesn't complete

**Root Cause**: Script waiting for user input (prompt)

**Fix**:
```bash
# Make prompts explicit
read -p "Continue? (y/N) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# Or add timeout
read -t 30 -p "Continue? (y/N) " -n 1 -r
```

---

## 7. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Automation Scripts capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover justfile commands and automation scripts
- Quick reference for development workflows
- Links to script documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Automation Scripts

25+ automation scripts with justfile interface for development workflows.

**Documentation**: [docs/skilled-awareness/automation-scripts/](docs/skilled-awareness/automation-scripts/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/automation-scripts/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/automation-scripts/awareness-guide.md)

**Core Commands**:
- `just test`: Run test suite
- `just smoke`: Quick validation
- `just lint`: Check code style
- `just pre-merge`: All quality gates
- `just --list`: Show all commands
```

**Validation**:
```bash
grep "Automation Scripts" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 8. Success Metrics

### Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Justfile usage** | ≥90% | % of script invocations via `just` (not direct `./scripts/`) |
| **Command memorization** | 5 core commands | Developer survey: Can name `test`, `smoke`, `lint`, `pre-merge`, `help` |
| **Onboarding time** | <30 min | Time from "never used" to "productive with justfile" |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Script idempotency** | 100% | % of scripts pass idempotency test (run twice, both succeed) |
| **Error handling** | 100% | % of scripts with `set -euo pipefail` and clear error messages |
| **Documentation** | 100% | % of scripts with header comments (usage, safety, rollback) |

### Efficiency Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **Script-related questions** | Varies | 80% reduction | Count of "How do I..." questions in Slack/email |
| **Script failures** | Varies | 80% reduction | Count of script failures (wrong usage, missing deps) |
| **Pre-merge check time** | Varies | <2 minutes | Time for `just pre-merge` to complete |

---

## 9. Related Documents

**Scripts**:
- [All scripts](/static-template/scripts/) - 25 automation scripts
- [justfile](/static-template/justfile) - Unified task interface

**Protocol**:
- [protocol-spec.md](protocol-spec.md) - Script contracts and validation standards

**Awareness Guide**:
- [awareness-guide.md](awareness-guide.md) - Agent workflows for using scripts

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - Scripts run pytest
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - CI/CD calls scripts
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit hooks use scripts
- [SAP-007: documentation-framework](../documentation-framework/) - Documentation scripts
- [SAP-012: development-lifecycle](../development-lifecycle/) - Scripts support lifecycle phases

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for automation-scripts SAP
