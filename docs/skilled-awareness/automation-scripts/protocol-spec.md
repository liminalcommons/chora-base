# Protocol Specification: Automation Scripts

**SAP ID**: SAP-008
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Overview

This protocol defines **contracts for 25 automation scripts** in chora-base projects, organized by category with **justfile as the unified interface**.

**Core Guarantee**: All scripts are idempotent, have consistent error handling, and provide clear rollback mechanisms for critical operations.

**Interface**: `just <task>` (primary) or `./scripts/<script>.sh` (direct, discouraged)

---

## 2. Architecture

### 2.1 Script Categories

```
scripts/
├── Category 1: Setup & Environment
│   ├── setup.sh (idempotent: project initialization)
│   ├── venv-create.sh (idempotent: create venv)
│   ├── venv-clean.sh (destructive: clean venv)
│   └── check-env.sh (read-only: validate environment)
│
├── Category 2: Development
│   ├── dev-server.sh (stateful: run dev server)
│   ├── smoke-test.sh (read-only: quick tests)
│   ├── integration-test.sh (read-only: integration tests)
│   └── diagnose.sh (read-only: environment diagnostics)
│
├── Category 3: Version Management
│   ├── bump-version.sh (write: semver bumping)
│   └── prepare-release.sh (orchestration: release prep)
│
├── Category 4: Release & Publishing
│   ├── build-dist.sh (write: build packages)
│   ├── publish-test.sh (write: publish to test PyPI)
│   ├── publish-prod.sh (write: publish to production PyPI)
│   └── verify-stable.sh (read-only: verify release)
│
├── Category 5: Safety & Recovery
│   ├── rollback-dev.sh (write: rollback changes)
│   └── pre-merge.sh (orchestration: all quality gates)
│
├── Category 6: Documentation
│   ├── validate_docs.py (read-only: validate docs)
│   ├── extract_tests.py (write: extract tests from docs)
│   ├── docs_metrics.py (read-only: calculate metrics)
│   ├── generate_docs_map.py (write: generate sitemap)
│   └── query_docs.py (read-only: search docs)
│
├── Category 7: MCP & Specialized
│   ├── mcp-tool.sh (mixed: MCP development)
│   └── validate_mcp_names.py (read-only: validate names)
│
└── Category 8: Migration & Handoff
    ├── migrate_namespace.sh (write: migrate namespaces)
    └── handoff.sh (orchestration: handoff checklist)
```

### 2.2 Justfile Interface

**Primary Entry Point**: `just <task>`

```
just
├── Setup & Environment
│   ├── install (pip install -e ".[dev]")
│   ├── setup-hooks (pre-commit install)
│   ├── venv-create (create virtual environment)
│   ├── venv-clean (clean virtual environment)
│   └── check-env (validate environment)
│
├── Testing
│   ├── test (pytest)
│   ├── test-coverage (pytest --cov with HTML report)
│   ├── smoke (quick smoke tests)
│   └── integration (integration tests)
│
├── Quality
│   ├── lint (ruff check)
│   ├── lint-fix (ruff check --fix)
│   ├── format (ruff format)
│   ├── type-check (mypy)
│   └── pre-merge (all quality gates)
│
├── Building & Releasing
│   ├── build (build distribution packages)
│   ├── bump-major (bump major version)
│   ├── bump-minor (bump minor version)
│   ├── bump-patch (bump patch version)
│   ├── prepare-release TYPE (prepare release)
│   ├── publish-test (publish to test PyPI)
│   └── publish-prod (publish to production PyPI)
│
├── Documentation
│   ├── docs-validate (validate documentation)
│   ├── docs-metrics (calculate doc metrics)
│   └── docs-map (generate doc sitemap)
│
└── Utilities
    ├── diagnose (environment diagnostics)
    ├── rollback (rollback development changes)
    └── mcp-tool (MCP development tools)
```

---

## 3. Script Contracts

### 3.1 General Contracts (All Scripts)

#### Safety Contract
```bash
# Required for all bash scripts
set -euo pipefail
# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Pipeline fails if any command fails
```

#### Error Handling Contract
```bash
# Pattern: Validate inputs
if [ -z "$REQUIRED_ARG" ]; then
    echo "Error: Required argument missing"
    echo "Usage: $0 <required-arg>"
    exit 1
fi

# Pattern: Check preconditions
if [ ! -f "required-file.txt" ]; then
    echo "Error: required-file.txt not found"
    echo "Run: ./scripts/setup.sh first"
    exit 1
fi

# Pattern: Wrap dangerous operations
if ! some_command; then
    echo "Error: Command failed"
    echo "To fix: Run ./scripts/rollback.sh"
    exit 1
fi
```

#### Exit Code Contract
- **0**: Success
- **1**: General error (missing arg, precondition failed)
- **2**: Command not found / dependency missing
- **3**: Permission denied / access error
- **130**: User canceled (Ctrl+C)

#### Documentation Contract
```bash
#!/usr/bin/env bash
# script-name.sh - Brief description
#
# Usage: ./scripts/script-name.sh [args]
#
# Description: Detailed explanation of what this script does.
#
# Examples:
#   ./scripts/script-name.sh           # Default behavior
#   ./scripts/script-name.sh --option  # With option
#
# Safety: [Idempotent | Destructive | Read-only | Stateful]
# Rollback: [Yes | No | N/A]
```

---

### 3.2 Idempotency Contracts

#### Pattern 1: Check-Before-Act
```bash
# Example: venv-create.sh
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping."
    exit 0
fi

python -m venv venv
echo "Virtual environment created."
```

#### Pattern 2: Update-Only-If-Changed
```bash
# Example: bump-version.sh
CURRENT_VERSION=$(grep "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')
NEW_VERSION="1.2.3"

if [ "$CURRENT_VERSION" = "$NEW_VERSION" ]; then
    echo "Version already $NEW_VERSION. Skipping."
    exit 0
fi

sed -i.bak "s/^version = .*/version = \"$NEW_VERSION\"/" pyproject.toml
```

#### Pattern 3: Cleanup-Before-Create
```bash
# Example: build-dist.sh
if [ -d "dist" ]; then
    echo "Cleaning previous dist/ directory..."
    rm -rf dist/
fi

python -m build
echo "Distribution packages built in dist/"
```

---

### 3.3 Category-Specific Contracts

#### Category 1: Setup & Environment

**setup.sh**
- **Purpose**: Initial project setup (venv, deps, pre-commit hooks)
- **Idempotency**: Yes (checks if each step already complete)
- **Rollback**: No (use venv-clean.sh to reset)
- **Dependencies**: Python 3.11+, git
- **Exit Codes**: 0 (success), 1 (missing dependencies), 2 (Python version too old)

**Contract**:
```bash
# 1. Check Python version
if ! python --version | grep -qE "Python 3\.(11|12|13)"; then
    echo "Error: Python 3.11+ required"
    exit 2
fi

# 2. Create venv (idempotent)
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# 3. Install dependencies (idempotent)
source venv/bin/activate
pip install -e ".[dev]"

# 4. Install pre-commit hooks (idempotent)
pre-commit install
```

---

**venv-create.sh**
- **Purpose**: Create virtual environment
- **Idempotency**: Yes (skips if venv/ exists)
- **Rollback**: Use venv-clean.sh
- **Exit Codes**: 0 (success or skipped), 1 (Python not found)

---

**venv-clean.sh**
- **Purpose**: Remove and recreate virtual environment
- **Idempotency**: Yes (always results in clean venv)
- **Rollback**: No (destructive operation)
- **Exit Codes**: 0 (success), 1 (Python not found)

**Contract**:
```bash
# Confirm before destructive operation
read -p "Delete venv/ and reinstall? (y/N) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Canceled."
    exit 0
fi

# Remove old venv
rm -rf venv/

# Recreate
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

---

**check-env.sh**
- **Purpose**: Validate environment (Python version, dependencies)
- **Idempotency**: Yes (read-only)
- **Rollback**: N/A
- **Exit Codes**: 0 (all checks pass), 1 (checks fail)

**Contract**:
```bash
ERRORS=0

# Check Python version
if ! python --version | grep -qE "Python 3\.(11|12|13)"; then
    echo "✗ Python 3.11+ required"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Python version OK"
fi

# Check venv exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found (run: just venv-create)"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Virtual environment exists"
fi

# Check dependencies installed
if ! pip show pytest > /dev/null 2>&1; then
    echo "✗ Dependencies not installed (run: just install)"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ Dependencies installed"
fi

exit $ERRORS
```

---

#### Category 2: Development

**smoke-test.sh**
- **Purpose**: Quick validation (~10 seconds)
- **Idempotency**: Yes (read-only)
- **Rollback**: N/A
- **Exit Codes**: 0 (tests pass), 1 (tests fail)

**Contract**:
```bash
# Run subset of fast tests
pytest tests/ -m "smoke or not slow" --maxfail=1 -x

# Verify imports work
python -c "import src.{{ package_name }}; print('Imports OK')"

# Verify CLI (if applicable)
if [ -f "src/{{ package_name }}/__main__.py" ]; then
    python -m {{ package_name }} --version
fi
```

---

**pre-merge.sh**
- **Purpose**: Comprehensive pre-merge validation
- **Idempotency**: Yes (read-only checks)
- **Rollback**: N/A
- **Exit Codes**: 0 (all pass), 1 (any fail)

**Contract** (6 checks):
1. Pre-commit hooks (all files)
2. Smoke tests
3. Full test suite with coverage ≥85%
4. CHANGELOG.md has [Unreleased] entries
5. No uncommitted changes (warning only)
6. Version check (informational)

---

#### Category 3: Version Management

**bump-version.sh**
- **Purpose**: Semantic version bumping (major, minor, patch)
- **Idempotency**: Yes (checks current version, skips if unchanged)
- **Rollback**: Git revert or manual edit
- **Exit Codes**: 0 (success), 1 (invalid bump type), 2 (version parse error)

**Contract**:
```bash
# Usage: bump-version.sh <major|minor|patch> [--dry-run]

# 1. Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
    exit 1
fi

# 2. Parse current version (semver: X.Y.Z)
CURRENT_VERSION=$(grep "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')
if [[ ! "$CURRENT_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version format"
    exit 2
fi

# 3. Calculate new version
# major: X+1.0.0
# minor: X.Y+1.0
# patch: X.Y.Z+1

# 4. Update files:
#    - pyproject.toml (version field)
#    - src/__init__.py (__version__)
#    - CHANGELOG.md (add new version header)

# 5. Dry-run support
if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would update to $NEW_VERSION"
    exit 0
fi
```

---

**prepare-release.sh**
- **Purpose**: Prepare release (run all checks, update docs)
- **Idempotency**: Yes (checks can run multiple times)
- **Rollback**: Git revert
- **Exit Codes**: 0 (ready to release), 1 (checks fail)

**Contract**:
```bash
# Usage: prepare-release.sh

# 1. Run all tests
pytest tests/

# 2. Check coverage ≥85%
pytest --cov --cov-fail-under=85

# 3. Verify CHANGELOG.md complete
if ! grep -q "## \[$NEW_VERSION\]" CHANGELOG.md; then
    echo "Error: CHANGELOG.md not updated"
    exit 1
fi

# 4. Verify git clean (no uncommitted changes)
if [ -n "$(git status --porcelain)" ]; then
    echo "Error: Uncommitted changes"
    exit 1
fi

# 5. Run smoke tests on built package
./scripts/build-dist.sh
pip install dist/*.whl
pytest --smoke
```

---

#### Category 4: Release & Publishing

**build-dist.sh**
- **Purpose**: Build distribution packages (.tar.gz, .whl)
- **Idempotency**: Yes (cleans dist/ before build)
- **Rollback**: N/A (delete dist/)
- **Exit Codes**: 0 (success), 1 (build failed)

**Contract**:
```bash
# 1. Clean previous build
rm -rf dist/ build/ *.egg-info

# 2. Build with python -m build
python -m build

# 3. Verify artifacts exist
if [ ! -f dist/*.whl ] || [ ! -f dist/*.tar.gz ]; then
    echo "Error: Build artifacts missing"
    exit 1
fi

# 4. List artifacts
ls -lh dist/
```

---

**publish-test.sh**
- **Purpose**: Publish to test.pypi.org (testing)
- **Idempotency**: No (fails if version already published)
- **Rollback**: No (cannot delete from PyPI)
- **Exit Codes**: 0 (success), 1 (upload failed)

**Contract**:
```bash
# 1. Verify dist/ exists
if [ ! -d "dist" ]; then
    echo "Error: dist/ not found (run: just build)"
    exit 1
fi

# 2. Upload to test PyPI
python -m twine upload --repository testpypi dist/*

# 3. Verify package installable
pip install --index-url https://test.pypi.org/simple/ {{ package_name }}==$VERSION
```

---

**publish-prod.sh**
- **Purpose**: Publish to pypi.org (production)
- **Idempotency**: No (fails if version already published)
- **Rollback**: No (cannot delete from PyPI)
- **Exit Codes**: 0 (success), 1 (upload failed)

**Contract**:
```bash
# 1. Confirm production publish (require user confirmation)
read -p "Publish $VERSION to production PyPI? (y/N) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# 2. Verify all quality gates passed
./scripts/pre-merge.sh || exit 1

# 3. Upload to production PyPI
python -m twine upload dist/*

# 4. Create git tag
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"
```

---

#### Category 5: Safety & Recovery

**rollback-dev.sh**
- **Purpose**: Rollback failed development changes
- **Idempotency**: Yes (git operations idempotent)
- **Rollback**: N/A (this is the rollback)
- **Exit Codes**: 0 (success), 1 (rollback failed)

**Contract**:
```bash
# 1. Show current git status
git status

# 2. Confirm rollback
read -p "Rollback uncommitted changes? (y/N) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# 3. Stash changes
git stash push -m "Rollback stash $(date +%Y-%m-%d_%H-%M-%S)"

# 4. Clean untracked files (optional)
read -p "Also remove untracked files? (y/N) " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git clean -fd
fi

# 5. Verify clean state
git status
```

---

#### Category 6: Documentation

**validate_docs.py**
- **Purpose**: Validate frontmatter, links, structure
- **Idempotency**: Yes (read-only)
- **Rollback**: N/A
- **Exit Codes**: 0 (valid), 1 (validation errors)

**Contract**:
```python
# Usage: python scripts/validate_docs.py [--check-frontmatter] [--check-links]

def validate_frontmatter(doc_path):
    """Validate YAML frontmatter."""
    # Check required fields: title, type, status, audience, last_updated
    # Check enum values: type (tutorial|how-to|reference|explanation)
    # Check enum values: status (current|draft|deprecated|archived)
    pass

def validate_links(doc_path):
    """Validate internal links."""
    # Check relative links exist
    # Check absolute links return 200 (optional)
    pass

def validate_structure(doc_dir):
    """Validate Diataxis structure."""
    # Check directories: tutorials/, how-to/, reference/, explanation/
    pass
```

---

**extract_tests.py**
- **Purpose**: Extract pytest tests from How-To docs (SAP-007)
- **Idempotency**: Yes (overwrites existing test file)
- **Rollback**: Git revert
- **Exit Codes**: 0 (success), 1 (extraction failed)

**Contract**:
```python
# Usage: python scripts/extract_tests.py --input <how-to.md> --output <test.py>

def extract_code_blocks(markdown_path):
    """Extract ```python code blocks from markdown."""
    pass

def generate_pytest_test(code_blocks):
    """Convert code blocks to pytest test functions."""
    # Pattern: Each code block → one test function
    # Add assertions if not present (basic validation)
    pass
```

---

## 4. Justfile Integration

### 4.1 Justfile Structure

**Location**: `justfile` (project root)

**Principles**:
1. **One task per script** (task name = script purpose)
2. **Clear task names** (verb-noun, e.g., `bump-patch`, not `bp`)
3. **Documentation** (comment above each task)
4. **Aliases** (short aliases for common tasks, e.g., `t` → `test`)

### 4.2 Justfile Example

```makefile
# Run all tests
test:
    pytest

# Run tests with coverage
test-coverage:
    pytest --cov=src --cov-report=html --cov-report=term

# Run smoke tests (quick validation)
smoke:
    ./scripts/smoke-test.sh

# Run pre-merge checks (required before PR)
pre-merge:
    ./scripts/pre-merge.sh

# Bump patch version (0.1.0 → 0.1.1)
bump-patch:
    ./scripts/bump-version.sh patch

# Bump minor version (0.1.0 → 0.2.0)
bump-minor:
    ./scripts/bump-version.sh minor

# Bump major version (0.1.0 → 1.0.0)
bump-major:
    ./scripts/bump-version.sh major

# Prepare release (run all checks, update docs)
prepare-release TYPE:
    ./scripts/prepare-release.sh {{TYPE}}

# Build distribution packages
build:
    ./scripts/build-dist.sh

# Publish to test PyPI
publish-test:
    ./scripts/publish-test.sh

# Publish to production PyPI
publish-prod:
    ./scripts/publish-prod.sh
```

---

## 5. Validation Standards

### 5.1 Script Validation Checklist

**Required for all scripts**:
- ✅ Has shebang (`#!/usr/bin/env bash` or `#!/usr/bin/env python3`)
- ✅ Has safety flags (`set -euo pipefail` for bash)
- ✅ Has header documentation (usage, description, examples, safety)
- ✅ Validates inputs (checks for required arguments)
- ✅ Checks preconditions (files exist, commands available)
- ✅ Has consistent error messages (script name, issue, remedy)
- ✅ Returns proper exit codes (0 = success, non-zero = failure)
- ✅ Is executable (`chmod +x scripts/*.sh`)

### 5.2 Idempotency Validation

**Test**: Run script twice, verify second run succeeds or skips

```bash
# Test idempotency
./scripts/some-script.sh
./scripts/some-script.sh  # Should succeed or skip, not fail
```

### 5.3 Error Handling Validation

**Test**: Verify script fails gracefully with clear error message

```bash
# Test error handling
./scripts/some-script.sh  # Missing required arg
# Expected: Clear error message + usage, exit code 1
```

---

## 6. Integration with Other SAPs

### 6.1 SAP-012 (development-lifecycle)
- **Phase 4 (Development)**: Scripts support TDD workflow (`just test`)
- **Phase 5 (Testing)**: Scripts run quality checks (`just pre-merge`)
- **Phase 7 (Release)**: Scripts automate release (`just prepare patch`, `just publish-prod`)

### 6.2 SAP-006 (quality-gates)
- **Pre-commit hooks**: Call scripts for validation
- **Linting**: `ruff check` integrated in justfile

### 6.3 SAP-007 (documentation-framework)
- **Test extraction**: `extract_tests.py` generates pytest tests from How-To docs
- **Validation**: `validate_docs.py` checks frontmatter and links

---

## 7. Anti-Patterns

### Anti-Pattern 1: Direct Script Invocation
**Wrong**: `./scripts/some-script.sh`
**Correct**: `just some-task`
**Why**: Justfile provides unified interface, hides script paths

### Anti-Pattern 2: Scripts Without Idempotency
**Wrong**:
```bash
python -m venv venv  # Fails if venv/ exists
```
**Correct**:
```bash
if [ ! -d "venv" ]; then
    python -m venv venv
fi
```

### Anti-Pattern 3: Scripts Without Error Handling
**Wrong**:
```bash
some_command
another_command  # Runs even if some_command failed
```
**Correct**:
```bash
set -euo pipefail
some_command  # Exits if fails
another_command  # Only runs if some_command succeeded
```

### Anti-Pattern 4: Unclear Error Messages
**Wrong**: `Error: Failed`
**Correct**: `Error: setup.sh failed - Python 3.11+ required. Run: brew install python@3.11`

---

## 8. Related Documents

**Scripts** (in `static-template/scripts/`):
- 25 shell scripts (.sh files)
- 5 Python scripts (.py files)

**Justfile**:
- [justfile](../../../../static-template/justfile) - Unified task interface

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - Scripts run pytest
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - CI calls scripts
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit uses scripts
- [SAP-007: documentation-framework](../documentation-framework/) - Documentation scripts
- [SAP-012: development-lifecycle](../development-lifecycle/) - Scripts support lifecycle

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for automation-scripts SAP
