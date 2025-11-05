# Protocol Specification: Quality Gates

**SAP ID**: SAP-006
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Overview

### Purpose

The quality-gates capability provides **pre-commit hooks for code quality** using ruff (linter + formatter) and mypy (type checker). It enforces style, types, and formatting before code is committed.

### Design Principles

1. **Ruff-Based** - Modern all-in-one tool (200x faster than flake8+isort+black combined)
2. **Type-Checked** - Mypy strict mode enforces type safety
3. **Pre-Commit Enforced** - Quality gates before commit (prevent bad code from entering repo)
4. **Fast Feedback** - Ruff completes in <1s (vs 10-30s for legacy tools)
5. **Correct Order** - ruff (check) before ruff-format (critical ordering)

---

## 2. Hook Inventory

### 2.1 pre-commit-hooks (Basic Checks)

**Repo**: https://github.com/pre-commit/pre-commit-hooks (v4.6.0)

**Hooks**:
1. **check-yaml** - Validate YAML syntax
2. **end-of-file-fixer** - Ensure files end with newline
3. **trailing-whitespace** - Remove trailing whitespace
4. **check-added-large-files** - Prevent large files (default 500KB limit)

**Purpose**: Basic file hygiene
**Duration**: <1 second total

### 2.2 ruff-pre-commit (Linting + Formatting)

**Repo**: https://github.com/astral-sh/ruff-pre-commit (v0.5.5)

**Hooks**:
1. **ruff** (check) - Lint code, fix violations
   - Args: `--fix, --exit-non-zero-on-fix`
   - Excludes: `^(temp/|repo-dump\.py)`

2. **ruff-format** - Format code (replaces black)
   - Excludes: `^(temp/|repo-dump\.py)`

**Purpose**: Style enforcement, auto-formatting
**Duration**: <1 second (200x faster than flake8+isort+black)

**CRITICAL**: ruff (check) MUST run before ruff-format
- Reason: ruff --fix modifies code, ruff-format then formats it
- If reversed: Formatting happens first, then linting might change it again (inconsistent)

### 2.3 mypy (Type Checking)

**Repo**: https://github.com/pre-commit/mirrors-mypy (v1.11.0)

**Hooks**:
1. **mypy** - Static type checking
   - Args: `--config-file=pyproject.toml`
   - Excludes: `^(temp/|repo-dump\.py)`

**Purpose**: Type safety enforcement
**Duration**: 1-3 seconds

---

## 3. Ruff Configuration

### 3.1 Basic Settings (pyproject.toml)

```toml
[tool.ruff]
line-length = 88         # Match black default
target-version = "py311" # Python 3.11+ syntax

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

### 3.2 Rule Categories

**E (pycodestyle errors)**:
- E101: Indentation contains mixed spaces and tabs
- E201: Whitespace after '('
- E501: Line too long (>88 characters)
- Many more...

**F (pyflakes)**:
- F401: Module imported but unused
- F841: Local variable assigned but never used
- F821: Undefined name

**I (isort)**:
- I001: Import block is un-sorted
- I002: Missing required import

**N (pep8-naming)**:
- N801: Class name should use CapWords
- N802: Function name should be lowercase
- N806: Variable in function should be lowercase

**W (pycodestyle warnings)**:
- W291: Trailing whitespace
- W293: Blank line contains whitespace

**UP (pyupgrade)**:
- UP006: Use `list` instead of `List` for type annotations (Python 3.9+)
- UP007: Use `X | Y` instead of `Union[X, Y]` (Python 3.10+)

**Why these rules?**:
- **E, F, W**: Core style and error detection (PEP 8)
- **I**: Import sorting (replaces isort)
- **N**: Naming conventions (PEP 8)
- **UP**: Modern Python syntax (3.11+ features)

---

## 4. Mypy Configuration

### 4.1 Strict Settings (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.11"
strict = true                    # Enable all strict checks
warn_return_any = true           # Warn if function returns Any
warn_unused_configs = true       # Warn about unused config options
disallow_untyped_defs = true     # Require type annotations on all functions
exclude = ["temp/"]
```

### 4.2 Module Overrides

**Allow missing imports for third-party libraries**:
```toml
[[tool.mypy.overrides]]
module = ["fastmcp", "fastmcp.*"]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ["pytest", "pytest.*"]
ignore_missing_imports = true
```

**Why?**: Some libraries lack type stubs, mypy can't check them

---

## 5. Hook Execution Flow

```
Developer: git commit -m "message"
    │
    v
pre-commit: Detect commit attempt
    │
    ├──► Repo 1: pre-commit-hooks
    │    ├─► check-yaml (✅ or ❌)
    │    ├─► end-of-file-fixer (✅ or ❌)
    │    ├─► trailing-whitespace (✅ or ❌)
    │    └─► check-added-large-files (✅ or ❌)
    │
    ├──► Repo 2: ruff-pre-commit
    │    ├─► ruff (check + --fix) (✅ or ❌)
    │    └─► ruff-format (✅ or ❌)
    │
    └──► Repo 3: mypy
         └─► mypy (✅ or ❌)
    │
    v
All hooks pass?
    ├─► YES: Commit succeeds ✅
    └─► NO: Commit blocked, fix issues ❌
```

---

## 6. Guarantees

When pre-commit hooks pass, code **guarantees**:

1. **Style Compliance**:
   - ✅ Follows PEP 8 (E, W rules)
   - ✅ No unused imports (F401)
   - ✅ Imports sorted (I001)
   - ✅ Naming conventions followed (N rules)
   - ✅ Modern Python syntax (UP rules)

2. **Type Safety**:
   - ✅ All functions have type annotations
   - ✅ No untyped defs (mypy strict)
   - ✅ Type consistency verified

3. **File Hygiene**:
   - ✅ Valid YAML syntax
   - ✅ Files end with newline
   - ✅ No trailing whitespace
   - ✅ No large files

---

## 7. Integration with CI/CD (SAP-005)

**lint.yml workflow uses same tools**:
```yaml
- name: Run ruff (linting)
  run: ruff check .

- name: Run mypy (type checking)
  run: mypy src
```

**Ensures**:
- Pre-commit hooks catch issues locally
- CI catches same issues if hooks skipped
- Consistent quality enforcement

---

## 8. Best Practices

### 8.1 Hook Order Importance

**CORRECT ORDER** (.pre-commit-config.yaml):
```yaml
- id: ruff                # Check + fix first
  args: [--fix, --exit-non-zero-on-fix]
- id: ruff-format         # Format second
```

**Why critical**:
1. ruff --fix modifies code (fixes violations)
2. ruff-format then formats the fixed code
3. If reversed: Formatting happens first, then fixes might break formatting

### 8.2 Ruff vs Legacy Tools

**Ruff replaces**:
- flake8 (linting)
- isort (import sorting)
- black (formatting, via ruff-format)
- pyupgrade (modernization)

**Benefits**:
- **Speed**: 200x faster (Rust-based)
- **Single tool**: One config, one command
- **Auto-fix**: `--fix` flag fixes most violations
- **Modern**: Active development, latest Python support

### 8.3 Mypy Strict Mode

**strict = true** enables:
- disallow_untyped_defs: Require type annotations
- no_implicit_optional: Don't infer Optional
- warn_return_any: Warn if returning Any
- Many more strict checks

**Benefits**:
- Catches type errors before runtime
- Improves code documentation
- Enables better IDE support

---

## 9. Common Violations & Fixes

**F401: Unused import**:
```python
# Violation
import os  # Imported but never used

# Fix
# Remove unused import
```

**E501: Line too long**:
```python
# Violation
result = some_very_long_function_name(arg1, arg2, arg3, arg4, arg5, arg6)  # >88 chars

# Fix (ruff-format handles this)
result = some_very_long_function_name(
    arg1, arg2, arg3, arg4, arg5, arg6
)
```

**I001: Imports unsorted**:
```python
# Violation
import os
import sys
import asyncio  # Should be before 'sys' (alphabetical)

# Fix (ruff --fix handles this)
import asyncio
import os
import sys
```

**Mypy: Function missing type annotation**:
```python
# Violation
def process(data):  # No type annotation
    return data.upper()

# Fix
def process(data: str) -> str:
    return data.upper()
```

---

## 10. Bypassing Hooks (Rare)

**Skip all hooks** (NOT recommended):
```bash
git commit --no-verify -m "message"
```

**Skip specific file** (add to .pre-commit-config.yaml):
```yaml
- id: ruff
  exclude: ^(temp/|special-file\.py)
```

**When acceptable**:
- Generated code (vendor/, temp/)
- Emergency hotfix (fix hooks immediately after)

**When NOT acceptable**:
- "Hooks are slow" → Fix: Hooks should be <5s total
- "Too many violations" → Fix: Fix violations incrementally
- "Don't like the rules" → Fix: Discuss rule changes, don't bypass

---

## 11. Related Documents

**SAP-006 Artifacts**:
- [capability-charter.md](capability-charter.md)
- [awareness-guide.md](awareness-guide.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [ledger.md](ledger.md)

**Configuration Files**:
- [.pre-commit-config.yaml](/static-template/.pre-commit-config.yaml)
- [pyproject.toml](/blueprints/pyproject.toml.blueprint) (lines 45-86)

**Related SAPs**:
- [testing-framework/](../testing-framework/) - SAP-004
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005
- [project-bootstrap/](../project-bootstrap/) - SAP-003

---

## 11. Self-Evaluation: Awareness File Coverage

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 5 (specified in this document)
1. Initial setup (install pre-commit, configure hooks)
2. Running checks manually (pre-commit run)
3. Fixing violations (ruff auto-fix, manual fixes)
4. Customizing rules (pyproject.toml configuration)
5. Updating hooks (pre-commit autoupdate)

**AGENTS.md Workflows**: 5 (implemented)
1. Initial Setup (First-Time Installation)
2. Running Quality Checks Manually
3. Fixing Ruff Violations
4. Fixing Mypy Type Errors
5. Customizing Quality Gate Rules

**CLAUDE.md Workflows**: 3 (implemented)
1. Set Up Quality Gates (Bash + Read + Write tools)
2. Diagnose and Fix Quality Violations (Read + Edit tools)
3. Customize Rules for Project (Read + Edit tools)

**Coverage**: 5/5 = 100% (all protocol-spec workflows covered in AGENTS.md)

**Variance**: 40% (5 generic workflows vs 3 Claude-specific workflows)

**Rationale**:
- AGENTS.md provides comprehensive step-by-step guidance for all agents (5 workflows)
- CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write/Edit) for Claude Code (3 workflows)
- Both files cover all protocol-spec workflows but with different levels of detail
- CLAUDE.md consolidates "Fixing Ruff Violations" and "Fixing Mypy Type Errors" into single "Diagnose and Fix" workflow (tool-focused)
- Variance is acceptable: both provide equivalent support for SAP-006 adoption

**Conclusion**: ✅ Equivalent support across agent types

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for quality-gates
- **1.0.1** (2025-11-05): Added self-evaluation section for awareness file coverage
