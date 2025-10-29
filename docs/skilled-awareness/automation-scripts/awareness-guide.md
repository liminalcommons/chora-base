---
sap_id: SAP-008
version: 1.0.0
status: Draft
last_updated: 2025-10-28
audience: ai-agents
---

# Awareness Guide: Automation Scripts

**SAP ID**: SAP-008
**Version**: 1.0.1
**For**: AI Coding Agents
**Purpose**: Workflows for using automation scripts via justfile

---

## 1. Quick Reference

### When to Use This SAP

**Use the Automation Scripts SAP when**:
- Running pre-merge checks before creating PR (`just pre-merge`)
- Releasing versions to PyPI (`just bump-patch`, `just publish-prod`)
- Running tests and quality gates locally (`just test`, `just lint`)
- Setting up or diagnosing development environment (`just diagnose`, `just install`)
- Validating documentation (`just docs-validate`, `just docs-metrics`)

**Don't use for**:
- One-off bash commands - use Bash tool directly for simple operations
- Non-justfile projects - this SAP is justfile-specific
- Learning justfile syntax - use justfile official docs instead
- CI/CD automation - GitHub Actions workflows call scripts directly, not via `just`

### Primary Interface

**Always use justfile** (not direct script invocation):
```bash
just <task>    # ✅ Correct (unified interface)
./scripts/<script>.sh   # ❌ Avoid (direct invocation)
```

### Common Tasks

| User Request | Justfile Command |
|--------------|------------------|
| "Run tests" | `just test` |
| "Run all checks" | `just pre-merge` |
| "Bump version" | `just bump-patch` (or minor, major) |
| "Build package" | `just build` |
| "Release to PyPI" | `just publish-prod` |
| "Quick validation" | `just smoke` |
| "Fix environment" | `just diagnose` |

---

## 2. Core Agent Workflows

### 2.1 Development Workflow

**Typical sequence during feature development**:

```bash
# Step 1: Run tests frequently
just test

# Step 2: Quick validation (10 seconds)
just smoke

# Step 3: Before committing
just pre-merge

# Step 4: Create commit (if all pass)
git add .
git commit -m "feat: Add feature X"
```

---

### 2.2 Release Workflow

**Typical sequence for releasing new version**:

```bash
# Step 1: Bump version
just bump-patch   # 1.0.0 → 1.0.1

# Step 2: Update CHANGELOG.md
Edit CHANGELOG.md  # Add release notes

# Step 3: Prepare release (run all checks)
just prepare patch

# Step 4: Build distribution
just build

# Step 5: Publish to production PyPI
just publish-prod

# Step 6: Create git tag (done by publish-prod)
# Automatic
```

---

## 3. Script Categories

### Category 1: Setup & Environment

**Use when**: Setting up project for first time or fixing environment

```bash
# Initial setup (first time)
just install          # Install dependencies
just setup-hooks      # Install pre-commit hooks

# Environment validation
just check-env        # Verify Python version, deps

# Environment reset
just venv-clean       # Clean and recreate venv
just venv-create      # Create venv (if missing)
```

**Agent Workflow: Fix Environment Issues**
```
1. User reports "Environment broken"
2. Read just check-env output
3. If venv issues: just venv-clean
4. If dependency issues: just install
5. Verify: just check-env
```

---

### Category 2: Testing

**Use when**: Validating code quality

```bash
# During development (fast feedback)
just test             # Run all tests (~1 min)
just smoke            # Quick smoke tests (~10 sec)

# Before PR (comprehensive)
just pre-merge        # All quality gates (~2 min)

# Coverage reporting
just test-coverage    # Generate HTML coverage report
```

**Agent Workflow: Run Pre-Merge Checks**
```
1. User requests "Check if ready for PR"
2. Bash: just pre-merge
3. If passes: Create PR
4. If fails: Show errors, fix issues, re-run
```

---

### Category 3: Quality

**Use when**: Checking code style and types

```bash
# Linting
just lint             # Check code style (ruff)
just lint-fix         # Auto-fix linting issues

# Formatting
just format           # Format code (ruff format)

# Type checking
just type-check       # Run mypy
```

**Agent Workflow: Fix Linting Errors**
```
1. Bash: just lint
2. If errors: Bash: just lint-fix (auto-fix)
3. If still errors: Manual fixes
4. Verify: just lint
```

---

### Category 4: Building & Releasing

**Use when**: Preparing release or publishing package

```bash
# Version management
just bump-patch       # 1.0.0 → 1.0.1
just bump-minor       # 1.0.0 → 1.1.0
just bump-major       # 1.0.0 → 2.0.0

# Release preparation
just prepare patch    # Prepare patch release
just prepare minor    # Prepare minor release
just prepare major    # Prepare major release

# Building
just build            # Build .tar.gz and .whl files

# Publishing
just publish-test     # Publish to test.pypi.org
just publish-prod     # Publish to pypi.org (production)
```

**Agent Workflow: Release Patch Version**
```
1. User requests "Release version 1.2.1"
2. Bash: just bump-patch
3. Edit CHANGELOG.md (add release notes)
4. Bash: just prepare patch
5. If checks pass:
   a. Bash: just build
   b. Bash: just publish-prod
6. Verify: Check pypi.org for new version
```

---

### Category 5: Documentation

**Use when**: Working with documentation

```bash
# Validation
just docs-validate    # Validate frontmatter, links

# Metrics
just docs-metrics     # Calculate doc coverage

# Sitemap
just docs-map         # Generate documentation map
```

**Agent Workflow: Validate Documentation**
```
1. User adds/edits docs
2. Bash: just docs-validate
3. If errors: Fix frontmatter or links
4. Verify: just docs-validate (pass)
```

---

### Category 6: Safety & Recovery

**Use when**: Rolling back changes or diagnosing issues

```bash
# Diagnostics
just diagnose         # Diagnose environment issues

# Rollback
just rollback         # Rollback uncommitted changes
```

**Agent Workflow: Rollback Failed Changes**
```
1. User requests "Rollback my changes"
2. Bash: just rollback
3. Confirm with user (prompts for confirmation)
4. Verify: git status (clean)
```

---

## 4. Detailed Workflows

### 4.1 Workflow: Run Pre-Merge Checks

**When**: Before creating pull request

**Steps**:
```bash
Bash: just pre-merge
```

**Expected Output**:
```
=== Pre-Merge Verification ===

[1/6] Running pre-commit hooks...
  ✓ All pre-commit hooks passed

[2/6] Running smoke tests...
  ✓ Smoke tests passed

[3/6] Running full test suite with coverage...
  ✓ Tests passed with 95% coverage

[4/6] Checking CHANGELOG.md...
  ✓ CHANGELOG.md has unreleased entries

[5/6] Checking for uncommitted changes...
  ⚠ Uncommitted changes detected
    Consider committing or stashing before merge

[6/6] Checking version...
  ✓ Current version: 1.2.0

=== Summary ===
✓ Ready for merge (0 errors, 1 warning)
```

**If Fails**:
```
Read error messages
Fix issues
Bash: just pre-merge (re-run)
```

---

### 4.2 Workflow: Bump Version and Release

**When**: User requests "Release version X.Y.Z"

**Steps**:

**1. Determine Bump Type**:
- **Patch** (1.0.0 → 1.0.1): Bug fixes, no breaking changes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Major** (1.0.0 → 2.0.0): Breaking changes

**2. Bump Version**:
```bash
# Example: Patch release
Bash: just bump-patch
```

**Output**:
```
=== Version Bump: patch ===

Current version: 1.0.0
New version:     1.0.1

Updated:
  - pyproject.toml
  - src/__init__.py

Next steps:
  1. Update CHANGELOG.md
  2. Run: just prepare patch
  3. Run: just publish-prod
```

**3. Update CHANGELOG.md**:
```markdown
Edit CHANGELOG.md

## [1.0.1] - 2025-10-28

### Fixed
- Bug X fixed
- Issue Y resolved
```

**4. Prepare Release**:
```bash
Bash: just prepare patch
```

**5. Build Distribution**:
```bash
Bash: just build
```

**6. Publish to Production**:
```bash
Bash: just publish-prod
```

**Output** (with confirmation prompt):
```
Publish 1.0.1 to production PyPI? (y/N) y

Running pre-merge checks...
✓ All checks passed

Uploading to PyPI...
✓ Package uploaded successfully

Creating git tag v1.0.1...
✓ Tag created and pushed

Release complete! View at: https://pypi.org/project/{package}/1.0.1/
```

---

### 4.3 Workflow: Fix Environment Issues

**When**: User reports "Environment broken" or tests won't run

**Steps**:

**1. Diagnose**:
```bash
Bash: just diagnose
```

**Output**:
```
=== Environment Diagnostics ===

Python version: 3.12.0 ✓
Virtual environment: venv/ ✓
Dependencies installed: pytest, ruff, mypy ✓
Pre-commit hooks: Installed ✓

Environment: OK
```

**If Issues Found**:

**Issue: Virtual environment missing**
```bash
Bash: just venv-create
```

**Issue: Dependencies missing**
```bash
Bash: just install
```

**Issue: Pre-commit hooks not installed**
```bash
Bash: just setup-hooks
```

**Issue: Virtual environment corrupted**
```bash
Bash: just venv-clean
# Prompts for confirmation, then recreates venv
```

**2. Verify Fix**:
```bash
Bash: just check-env
```

---

### 4.4 Workflow: Extract Tests from How-To Docs

**When**: User writes How-To doc with test_extraction: true

**Steps**:

**1. Check Frontmatter**:
```yaml
Read user-docs/how-to/01-example.md

---
title: Example How-To
type: how-to
test_extraction: true   # ← Must be true
---
```

**2. Extract Tests**:
```bash
Bash: python scripts/extract_tests.py \
  --input user-docs/how-to/01-example.md \
  --output tests/docs/test_example.py
```

**3. Run Extracted Tests**:
```bash
Bash: pytest tests/docs/test_example.py
```

**4. Verify Tests Pass**:
```
Expected: All tests pass (documentation examples are correct)
If fails: Fix examples in How-To doc, re-extract
```

---

## 5. Script Safety Classifications

### Read-Only Scripts (Safe to run anytime)
- `check-env.sh` - Validate environment
- `smoke-test.sh` - Quick tests
- `diagnose.sh` - Environment diagnostics
- `validate_docs.py` - Validate documentation
- `docs_metrics.py` - Calculate doc metrics

### Idempotent Scripts (Safe to re-run)
- `setup.sh` - Initial setup
- `venv-create.sh` - Create venv (skips if exists)
- `bump-version.sh` - Bump version (checks current first)
- `build-dist.sh` - Build packages (cleans dist/ first)
- `pre-merge.sh` - Pre-merge checks

### Destructive Scripts (Require confirmation)
- `venv-clean.sh` - Deletes venv/ (prompts for confirmation)
- `rollback.sh` - Stashes changes (prompts for confirmation)
- `publish-prod.sh` - Publishes to PyPI (prompts for confirmation)

### Non-Idempotent Scripts (Run once per version)
- `publish-test.sh` - Publish to test PyPI (fails if version exists)
- `publish-prod.sh` - Publish to production PyPI (fails if version exists)

---

## 6. Common Agent Mistakes

### Mistake 1: Direct Script Invocation
**Wrong**: `./scripts/pre-merge.sh`
**Correct**: `just pre-merge`
**Why**: Justfile is the unified interface, hides script paths

### Mistake 2: Skipping Pre-Merge Checks
**Wrong**: Create PR without running `just pre-merge`
**Correct**: Always run `just pre-merge` before PR
**Why**: CI will fail if pre-merge checks don't pass

### Mistake 3: Publishing Without Testing
**Wrong**: `just publish-prod` immediately after coding
**Correct**: `just pre-merge` → `just build` → `just publish-test` → verify → `just publish-prod`
**Why**: Production releases should be tested first

### Mistake 4: Bumping Version Manually
**Wrong**: Manually edit pyproject.toml version
**Correct**: `just bump-patch` (or minor, major)
**Why**: Script updates multiple files consistently

### Mistake 5: Ignoring Script Output
**Wrong**: Run script, ignore error messages
**Correct**: Read error messages, follow remediation steps
**Why**: Error messages include clear fix instructions

---

## 7. Integration with Other SAPs

### SAP-012 (development-lifecycle)
- **Phase 4 (Development)**: `just test`, `just lint`
- **Phase 5 (Testing)**: `just pre-merge`
- **Phase 7 (Release)**: `just bump-patch`, `just publish-prod`

### SAP-006 (quality-gates)
- **Pre-commit hooks**: Automatically call scripts
- **Manual validation**: `just pre-merge`

### SAP-007 (documentation-framework)
- **Test extraction**: `python scripts/extract_tests.py`
- **Validation**: `just docs-validate`

---

## 8. Decision Trees for Agents

### Decision Tree 1: Which Command to Run?

```
User request:
│
├─ "Run tests"
│  └─ just test
│
├─ "Quick validation"
│  └─ just smoke
│
├─ "Check if ready for PR"
│  └─ just pre-merge
│
├─ "Fix linting errors"
│  └─ just lint-fix
│
├─ "Bump version"
│  ├─ Bug fix? → just bump-patch
│  ├─ New feature? → just bump-minor
│  └─ Breaking change? → just bump-major
│
├─ "Release to PyPI"
│  └─ just publish-prod
│
└─ "Fix environment"
   └─ just diagnose → follow output
```

### Decision Tree 2: Release Workflow

```
Release request:
│
├─ Step 1: Bump version
│  └─ just bump-{patch|minor|major}
│
├─ Step 2: Update CHANGELOG.md
│  └─ Edit CHANGELOG.md
│
├─ Step 3: Prepare release
│  └─ just prepare {patch|minor|major}
│  │
│  ├─ Pass? → Continue to Step 4
│  └─ Fail? → Fix issues, re-run Step 3
│
├─ Step 4: Build distribution
│  └─ just build
│
├─ Step 5: Publish (optional: test first)
│  ├─ just publish-test (optional)
│  └─ just publish-prod
│
└─ Step 6: Verify
   └─ Check pypi.org for new version
```

---

## 9. Justfile Task Reference

### Complete Task List

Run `just --list` to see all available tasks:

```bash
Bash: just --list
```

**Output**:
```
Available recipes:
    build               # Build distribution packages
    bump-major          # Bump major version (1.0.0 → 2.0.0)
    bump-minor          # Bump minor version (1.0.0 → 1.1.0)
    bump-patch          # Bump patch version (1.0.0 → 1.0.1)
    check-env           # Validate environment
    diagnose            # Environment diagnostics
    docs-map            # Generate documentation sitemap
    docs-metrics        # Calculate documentation metrics
    docs-validate       # Validate documentation
    format              # Format code (ruff format)
    install             # Install dependencies
    lint                # Check code style (ruff)
    lint-fix            # Auto-fix linting issues
    pre-merge           # Run all pre-merge checks
    prepare-release     # Prepare release
    publish-prod        # Publish to production PyPI
    publish-test        # Publish to test PyPI
    rollback            # Rollback uncommitted changes
    setup-hooks         # Install pre-commit hooks
    smoke               # Quick smoke tests
    test                # Run all tests
    test-coverage       # Run tests with coverage
    type-check          # Run type checking (mypy)
    venv-clean          # Clean and recreate venv
    venv-create         # Create virtual environment
```

---

## 10. Common Pitfalls

### Pitfall 1: Direct Script Invocation Instead of Justfile

**Scenario**: Agent calls scripts directly instead of using `just` interface.

**Example**:
```bash
# Agent runs script directly:
./scripts/pre-merge.sh

# Error: Permission denied (scripts not executable)
# OR: Wrong working directory (scripts expect root)
```

**Fix**: Always use `just` commands:
```bash
# Correct approach:
just pre-merge

# Why just is better:
# - Handles working directory automatically
# - Provides tab completion
# - Shows available tasks (just --list)
# - Validates prerequisites before running
```

**Why it matters**: Direct script invocation breaks when paths change. Justfile is the stable interface (Protocol Section 2.1). Scripts may move locations, but `just` commands remain constant. Using `just` takes 0 extra seconds, debugging path issues takes 5-10 minutes.

### Pitfall 2: Running Destructive Scripts Without Reading Prompts

**Scenario**: Agent runs `just venv-clean` or `just rollback`, ignores confirmation prompt, loses data.

**Example**:
```bash
# Agent runs destructive command:
just venv-clean

# Script prompts:
# "Delete venv/ and recreate? This will remove all installed packages. (y/N)"

# Agent sends "y" without informing user
# Result: User's venv deleted, custom packages lost!
```

**Fix**: Always warn user before confirming destructive operations:
```bash
# Before running destructive command:
# 1. Inform user what will happen:
print("This will DELETE venv/ and recreate it. Custom packages will be lost.")

# 2. Ask user for confirmation:
print("Running: just venv-clean")
print("Script will prompt for confirmation. Proceed? (y/N)")

# 3. Only proceed if user confirms
```

**Why it matters**: Protocol Section 5 classifies scripts by safety. Destructive scripts (`venv-clean`, `rollback`, `publish-prod`) require human confirmation. One ignored prompt can delete hours of work. Always respect confirmation prompts.

### Pitfall 3: Skipping Pre-Merge Checks Before Creating PR

**Scenario**: Agent creates PR without running `just pre-merge`, CI fails, blocks development.

**Example**:
```bash
# Agent workflow (WRONG):
git add .
git commit -m "feat: add feature"
git push origin feature-branch
# Create PR via gh pr create

# Result: CI fails!
# - Ruff violations: 12 errors
# - Coverage: 78% (required 85%)
# - Tests failing: 3 failures

# Now PR blocks main, must fix urgently
```

**Fix**: Always run pre-merge checks BEFORE pushing:
```bash
# Correct workflow:
git add .

# BEFORE committing, run pre-merge:
just pre-merge

# If fails:
# - Fix issues
# - Re-run just pre-merge
# - Repeat until passes

# THEN commit and push:
git commit -m "feat: add feature"
git push origin feature-branch
gh pr create
```

**Why it matters**: Pre-merge checks prevent CI failures. CI failure blocks all PRs, wasting team time. Running `just pre-merge` locally takes 2 minutes, fixing broken CI takes 10-30 minutes. Protocol Section 3.5 mandates pre-merge before PR.

### Pitfall 4: Bumping Version Manually Instead of Using just bump-*

**Scenario**: Agent edits `pyproject.toml` version manually, misses `src/__init__.py`, release fails.

**Example**:
```python
# Agent manually edits pyproject.toml:
# pyproject.toml
[project]
version = "1.2.1"  # Changed from 1.2.0

# But forgets src/mypackage/__init__.py:
__version__ = "1.2.0"  # STILL OLD VERSION!

# Build package:
just build

# Publish:
just publish-prod

# Result: Package metadata says 1.2.1, but __version__ returns "1.2.0"
# Users confused, health checks fail
```

**Fix**: Use `just bump-*` scripts that update ALL version locations:
```bash
# Correct approach:
just bump-patch  # or bump-minor, bump-major

# Output shows all files updated:
# Updated:
#   - pyproject.toml (1.2.0 → 1.2.1)
#   - src/mypackage/__init__.py (1.2.0 → 1.2.1)
#   - docs/conf.py (1.2.0 → 1.2.1)

# Now ALL versions consistent
```

**Why it matters**: Version inconsistency breaks deployments. Health checks read `__version__`, package metadata reads `pyproject.toml`. Mismatch causes failures. Protocol Section 4.1 documents version bump script guarantees all files updated.

### Pitfall 5: Not Understanding Script Safety Classifications

**Scenario**: Agent treats all scripts as safe, runs destructive script casually, loses data.

**Example**:
```bash
# Agent sees failing test, thinks venv is corrupted
# Runs without thinking:
just venv-clean

# Prompt appears:
# "Delete venv/? (y/N)"

# Agent auto-confirms "y"
# Result: venv deleted, including:
# - Custom packages user installed manually
# - Debug tools (ipdb, etc.)
# - Takes 5-10 minutes to recreate
```

**Fix**: Check script classification BEFORE running (Protocol Section 5):
```bash
# Script Safety Classifications:

# Read-Only (Safe anytime):
just check-env      # ✅ No changes
just smoke          # ✅ No changes
just diagnose       # ✅ No changes

# Idempotent (Safe to re-run):
just install        # ✅ Skips if deps installed
just test           # ✅ No destructive changes
just pre-merge      # ✅ Read-only checks

# Destructive (Require confirmation):
just venv-clean     # ⚠️ DELETES venv/
just rollback       # ⚠️ STASHES uncommitted changes
just publish-prod   # ⚠️ PUBLISHES to PyPI (irreversible)

# Before running ⚠️ script:
# 1. Understand what it destroys
# 2. Warn user
# 3. Get explicit confirmation
# 4. Respect script's confirmation prompt
```

**Why it matters**: Destructive scripts cause data loss. `venv-clean` deletes venv/, `rollback` stashes changes, `publish-prod` publishes to PyPI (can't unpublish). Understanding classification prevents accidents. Reading classification takes 10 seconds, recovering from data loss takes 10-60 minutes.

---

## 11. Related Content

### Within This SAP (skilled-awareness/automation-scripts/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-008
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (script specs, safety classifications)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for using justfile
- [ledger.md](ledger.md) - Automation script adoption tracking, version history
- **This document** (awareness-guide.md) - Agent workflows and script usage patterns

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/TDD_WORKFLOW.md](../../dev-docs/workflows/TDD_WORKFLOW.md) - Test-driven development (`just test` integration)
- [dev-docs/workflows/release-workflow.md](../../dev-docs/workflows/release-workflow.md) - Release process using `just bump-*`, `just publish-*`

**Tools**:
- [dev-docs/tools/pytest.md](../../dev-docs/tools/pytest.md) - Testing tool (`just test`, `just smoke`)
- [dev-docs/tools/ruff.md](../../dev-docs/tools/ruff.md) - Linting (`just lint`, `just lint-fix`)
- [dev-docs/tools/mypy.md](../../dev-docs/tools/mypy.md) - Type checking (`just type-check`)

**Development Guidelines**:
- [dev-docs/development/scripting-standards.md](../../dev-docs/development/scripting-standards.md) - Standards for writing automation scripts

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [static-template/justfile](/static-template/justfile) - Unified task interface (all `just` commands)
- [static-template/scripts/](/static-template/scripts/) - 25 automation scripts
- [static-template/pyproject.toml](/static-template/pyproject.toml) - Project configuration

**Guides**:
- [project-docs/guides/automation-setup.md](../../project-docs/guides/automation-setup.md) - Setting up justfile in projects
- [project-docs/guides/release-process.md](../../project-docs/guides/release-process.md) - Complete release process using scripts

**Audits & Releases**:
- [project-docs/audits/](../../project-docs/audits/) - SAP audits including SAP-008 validation
- [project-docs/releases/](../../project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/using-justfile.md](../../user-docs/guides/using-justfile.md) - Introduction to justfile

**Tutorials**:
- [user-docs/tutorials/first-release.md](../../user-docs/tutorials/first-release.md) - Release your first version (uses `just bump-*`, `just publish-*`)
- [user-docs/tutorials/debugging-scripts.md](../../user-docs/tutorials/debugging-scripts.md) - Debug automation script failures

**Reference**:
- [user-docs/reference/justfile-reference.md](../../user-docs/reference/justfile-reference.md) - Complete justfile command reference
- [user-docs/reference/script-reference.md](../../user-docs/reference/script-reference.md) - Individual script documentation

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.6 (documents SAP-008)

**Dependent Capabilities**:
- [testing-framework/](../testing-framework/) - SAP-004 (`just test` runs tests per SAP-004 standards)
- [quality-gates/](../quality-gates/) - SAP-006 (`just lint`, `just type-check` enforce SAP-006 gates)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (GitHub Actions call scripts directly)
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates justfile and scripts)

**Supporting Capabilities**:
- [documentation-framework/](../documentation-framework/) - SAP-007 (`just docs-validate` validates docs per SAP-007)
- [metrics-tracking/](../metrics-tracking/) - SAP-013 (scripts track metrics)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-008 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings (5 scenarios: direct script invocation, destructive prompts, skipping pre-merge, manual version bumps, safety classifications), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide for automation-scripts SAP
