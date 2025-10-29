---
sap_id: SAP-008
version: 1.0.0
status: Draft
last_updated: 2025-10-28
audience: ai-agents
---

# Awareness Guide: Automation Scripts

**SAP ID**: SAP-008
**For**: AI Coding Agents
**Purpose**: Workflows for using automation scripts via justfile

---

## 1. Quick Reference

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

## 10. Related Documents

**Scripts**:
- [All scripts](../../../../static-template/scripts/) - 25 automation scripts

**Justfile**:
- [justfile](../../../../static-template/justfile) - Unified task interface

**Protocol**:
- [protocol-spec.md](protocol-spec.md) - Script contracts and validation standards

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - Scripts run pytest
- [SAP-006: quality-gates](../quality-gates/) - Scripts enforce quality
- [SAP-007: documentation-framework](../documentation-framework/) - Documentation scripts
- [SAP-012: development-lifecycle](../development-lifecycle/) - Scripts support lifecycle

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for automation-scripts SAP
