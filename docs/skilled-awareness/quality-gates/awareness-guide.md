# Awareness Guide: Quality Gates

**SAP ID**: SAP-006
**Version**: 1.0.1
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

### When to Use This SAP

**Use the Quality Gates SAP when**:
- Understanding pre-commit hooks in generated projects
- Configuring linting (ruff) and type checking (mypy)
- Fixing quality gate violations before commits
- Understanding quality standards (coverage 85%, type checking required)
- Troubleshooting pre-commit hook failures

**Don't use for**:
- Manual code review - quality gates automate checks, not review
- Non-Python projects - ruff and mypy are Python-specific
- Projects without pre-commit - chora-base uses pre-commit by default
- Bypassing quality checks - gates exist for quality, not frustration

**Install pre-commit hooks**:
```bash
pre-commit install
```

**Run hooks manually**:
```bash
pre-commit run --all-files
```

**Fix ruff violations**:
```bash
ruff check . --fix
ruff format .
```

**Check mypy**:
```bash
mypy src
```

---

## 2. Agent Context Loading

**Essential Context (2-3k tokens)**:
- [protocol-spec.md](protocol-spec.md) Sections 2, 3, 4 - Hooks, ruff config, mypy config

**For fixing violations**:
- [protocol-spec.md](protocol-spec.md) Section 9 - Common violations & fixes

---

## 3. Common Workflows

### 3.1 Fix Ruff Violations

**Context**: 2k tokens (Protocol Section 9)

**Steps**:
1. Run `ruff check . --fix` (auto-fixes most violations)
2. Run `ruff format .` (format code)
3. Review changes (`git diff`)
4. Commit

### 3.2 Fix Mypy Errors

**Context**: 2k tokens (Protocol Section 4, 9)

**Steps**:
1. Run `mypy src`
2. Read error messages
3. Add type annotations
4. Re-run mypy

---

## 4. Common Pitfalls

### Pitfall 1: Skipping Pre-Commit Hooks with --no-verify

**Scenario**: Agent commits with `--no-verify` to bypass quality gates, introducing quality issues.

**Example**:
```bash
# Agent encounters ruff violation
ruff check . --fix
# Shows: 5 violations fixed, 2 remain

# Agent decides to "save time" by skipping hooks
git commit -m "feat: add new feature" --no-verify
# Bypasses all quality gates!

# Result: Code with quality issues pushed to main
# CI fails, blocks all PRs, requires fix commit
```

**Fix**: Never use `--no-verify` - fix violations instead:
```bash
# Proper workflow:
ruff check . --fix  # Auto-fix what you can
ruff format .       # Format code
mypy src            # Check types

# If violations remain, FIX them:
# - Read error message
# - Understand what's wrong
# - Fix the code (don't bypass the check)

git commit -m "feat: add new feature"  # Hooks run, pass
```

**Why it matters**: `--no-verify` bypasses ALL hooks (ruff, mypy, coverage). Quality issues multiply. One skipped hook leads to 5-10 quality issues. Protocol Section 6.1 mandates hooks must pass.

### Pitfall 2: Disabling Ruff Rules Without Understanding Them

**Scenario**: Agent disables ruff rule because code violates it.

**Example**:
```python
# Code violates F401 (unused import)
import os  # Not used anywhere

# Ruff complains:
# F401 [*] `os` imported but unused

# Agent "fixes" by disabling rule:
# pyproject.toml
[tool.ruff]
ignore = ["F401"]  # Disable unused import check

# Result: ALL unused imports now ignored project-wide!
# Imports accumulate, code becomes messy
```

**Fix**: Fix the violation, don't disable the rule:
```python
# Option 1: Remove unused import
# (If truly unused)

# Option 2: Use the import
import os
print(os.getcwd())  # Now used

# Option 3: Mark as intentionally unused (rare)
import os  # noqa: F401 - Used by dynamic import

# Don't disable rules globally!
```

**Why it matters**: Ruff rules exist for code quality. Disabling rules globally affects entire project. Fix violations locally (# noqa) if absolutely necessary. Protocol Section 3.2 documents standard ruff configuration.

### Pitfall 3: Ignoring Mypy Errors Instead of Adding Type Annotations

**Scenario**: Agent sees mypy errors, adds `# type: ignore` everywhere.

**Example**:
```python
# Code missing type annotations
def process_data(data):
    return data.upper()

# Mypy complains:
# error: Function is missing a type annotation

# Agent "fixes" with type: ignore:
def process_data(data):  # type: ignore
    return data.upper()

# Result: No type safety, defeats purpose of mypy
```

**Fix**: Add proper type annotations:
```python
# Proper fix:
def process_data(data: str) -> str:
    return data.upper()

# Now mypy can:
# - Verify data is actually a string
# - Catch errors: process_data(123) → error!
# - Provide IDE autocomplete
```

**Why it matters**: Type annotations catch bugs. `# type: ignore` defeats this. One ignored error leads to 10+ uncaught bugs. Protocol Section 4 mandates type annotations for all functions.

### Pitfall 4: Not Running Pre-Commit Hooks Before Large Commits

**Scenario**: Agent makes large changes, commits without running hooks locally, hooks fail.

**Example**:
```bash
# Agent refactors 10 files
git add .
git commit -m "refactor: major cleanup"

# Pre-commit runs:
# ruff...........................................Failed
# - 47 violations across 8 files
# mypy...........................................Failed
# - 23 type errors across 5 files

# Commit blocked! Must fix all violations before committing
# Takes 30-60 minutes to fix everything
```

**Fix**: Run hooks manually BEFORE committing:
```bash
# After making changes, BEFORE committing:
pre-commit run --all-files

# Shows violations early:
# ruff: 47 violations
# mypy: 23 errors

# Fix violations incrementally:
ruff check . --fix  # Auto-fix 40/47
# Manually fix remaining 7
mypy src  # Fix 23 type errors one by one

# THEN commit:
git commit -m "refactor: major cleanup"
# Pre-commit runs, passes instantly (already fixed)
```

**Why it matters**: Fixing violations during commit is frustrating. Running hooks early (during development) is easier. Large commits with violations take 30-60 minutes to fix, running hooks early takes 5-10 minutes total.

### Pitfall 5: Not Understanding That Coverage Gate Runs in CI, Not Pre-Commit

**Scenario**: Agent expects pre-commit to block low coverage, but it doesn't.

**Example**:
```bash
# Agent writes code without tests
# Runs pre-commit:
pre-commit run --all-files
# ✅ Passes! (ruff, mypy happy)

git commit -m "feat: add feature"
# ✅ Commits! Pre-commit passed

git push origin main
# CI runs pytest --cov...
# ❌ FAILED: Coverage 73%, required 85%

# Result: Commit in history but CI blocked
```

**Fix**: Understand two-tier quality gates:
```bash
# Pre-commit checks (local):
# - ruff (linting)
# - mypy (type checking)
# - trailing whitespace, yaml syntax

# CI checks (GitHub Actions):
# - Tests pass
# - Coverage ≥85%
# - Security (CodeQL)

# Before pushing, run tests locally:
pytest --cov=src --cov-fail-under=85
# Shows: Coverage 73% - need more tests!

# Write tests to reach 85%, THEN push
```

**Why it matters**: Coverage gate is in CI (SAP-005), not pre-commit. Pre-commit passing doesn't mean CI will pass. Protocol Section 2.1 lists pre-commit hooks (coverage not included). Protocol Section 6.2 documents CI coverage gate.

---

## 5. Best Practices

**DO**:
- ✅ Run `pre-commit run --all-files` before committing
- ✅ Use `ruff check --fix` to auto-fix violations
- ✅ Add type annotations to all functions

**DON'T**:
- ❌ Skip hooks with `--no-verify`
- ❌ Disable ruff rules without understanding them
- ❌ Ignore mypy errors

---

## 6. Related Content

### Within This SAP (skilled-awareness/quality-gates/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-006
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (pre-commit config, ruff, mypy)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for using quality gates
- [ledger.md](ledger.md) - Quality gate adoption tracking, version history
- **This document** (awareness-guide.md) - Agent workflows and troubleshooting

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/TDD_WORKFLOW.md](/dev-docs/workflows/TDD_WORKFLOW.md) - Test-driven development (quality gates enforce tests)
- [dev-docs/workflows/code-review.md](/dev-docs/workflows/code-review.md) - Code review process (quality gates pre-check)

**Tools**:
- [dev-docs/tools/ruff.md](/dev-docs/tools/ruff.md) - Linting tool (pre-commit hook)
- [dev-docs/tools/mypy.md](/dev-docs/tools/mypy.md) - Type checking (pre-commit hook)
- [dev-docs/tools/pre-commit.md](/dev-docs/tools/pre-commit.md) - Pre-commit framework

**Development Guidelines**:
- [dev-docs/development/code-style.md](/dev-docs/development/code-style.md) - Code style (enforced by ruff)
- [dev-docs/development/type-annotations.md](/dev-docs/development/type-annotations.md) - Type annotation standards (enforced by mypy)

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [static-template/.pre-commit-config.yaml](/static-template/.pre-commit-config.yaml) - Pre-commit configuration
- [static-template/pyproject.toml](/static-template/pyproject.toml) - Ruff and mypy configuration ([tool.ruff], [tool.mypy])

**Guides**:
- [project-docs/guides/quality-standards.md](/project-docs/guides/quality-standards.md) - Quality standards overview
- [project-docs/guides/fixing-quality-violations.md](/project-docs/guides/fixing-quality-violations.md) - Common violations and fixes

**Audits & Releases**:
- [project-docs/audits/](/project-docs/audits/) - SAP audits including SAP-006 validation
- [project-docs/releases/](/project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/code-quality.md](/user-docs/guides/code-quality.md) - Understanding code quality

**Tutorials**:
- [user-docs/tutorials/fixing-ruff-violations.md](/user-docs/tutorials/fixing-ruff-violations.md) - Fix common ruff violations
- [user-docs/tutorials/adding-type-annotations.md](/user-docs/tutorials/adding-type-annotations.md) - Add mypy type annotations

**Reference**:
- [user-docs/reference/ruff-rules.md](/user-docs/reference/ruff-rules.md) - Ruff rules reference
- [user-docs/reference/mypy-config.md](/user-docs/reference/mypy-config.md) - Mypy configuration reference

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.4 (documents SAP-006)

**Dependent Capabilities**:
- [testing-framework/](../testing-framework/) - SAP-004 (quality gates enforce test coverage)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (lint.yml runs ruff and mypy in CI)
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates quality gate files)

**Supporting Capabilities**:
- [automation-scripts/](../automation-scripts/) - SAP-008 (scripts for quality checks)
- [documentation-framework/](../documentation-framework/) - SAP-007 (quality gates for docs)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-006 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings (5 scenarios: --no-verify, disabling rules, type: ignore, large commits, coverage gate understanding), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide
