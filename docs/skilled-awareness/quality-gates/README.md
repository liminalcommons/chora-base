# SAP-006: Quality Gates

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Pre-commit hooks with ruff (200x faster linting) + mypy (type checking)—catch style, type, and formatting issues before commit with <3s feedback loops.

---

## 🚀 Quick Start (2 minutes)

```bash
# Install pre-commit hooks
just setup-hooks

# Test hooks (dry run without committing)
pre-commit run --all-files

# Make commit (hooks run automatically)
git add .
git commit -m "Add feature"  # ← Hooks run here
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for pre-commit setup (5-min read)

---

## 📖 What Is SAP-006?

SAP-006 provides **pre-commit hooks for code quality** using ruff (linter + formatter, 200x faster than legacy tools) and mypy (type checker). It enforces style, types, and formatting before code is committed—preventing bad code from entering the repository with <3s feedback loops vs 10-30s with legacy tools (flake8+isort+black).

**Key Innovation**: Ruff all-in-one tool (linting + formatting) replaces 3 separate tools with 200x speed improvement, plus strict mypy type checking for type safety.

---

## 🎯 When to Use

Use SAP-006 when you need to:

1. **Enforce code quality** - Catch style, type, and formatting issues before commit
2. **Fast feedback loops** - Get results in <3s (vs 10-30s with legacy tools)
3. **Prevent bad commits** - Block commits that fail quality gates
4. **Team consistency** - Ensure all team members follow same code standards
5. **CI/CD integration** - Pre-commit hooks align with CI workflows (SAP-005)

**Not needed for**: Quick prototyping (disable hooks temporarily), or single-developer projects (but still recommended)

---

## ✨ Key Features

- ✅ **Ruff-Based** - 200x faster than flake8+isort+black combined (<1s vs 10-30s)
- ✅ **Type-Checked** - Mypy strict mode enforces type safety
- ✅ **Pre-Commit Enforced** - Quality gates before commit (prevent bad code from entering repo)
- ✅ **Fast Feedback** - Complete in <3s total (ruff <1s, mypy 1-3s)
- ✅ **Auto-Fix** - Ruff automatically fixes violations where possible
- ✅ **7 Hooks** - check-yaml, end-of-file-fixer, trailing-whitespace, check-added-large-files, ruff, ruff-format, mypy
- ✅ **Correct Ordering** - ruff (check) before ruff-format (critical for consistency)
- ✅ **CI Aligned** - Same checks run in pre-commit and CI/CD (SAP-005)

---

## 📚 Quick Reference

### 7 Pre-Commit Hooks

#### Basic File Hygiene (pre-commit-hooks v4.6.0)

**1. check-yaml** - Validate YAML syntax
- **Duration**: <1s
- **Fixes**: None (fails if invalid YAML)
- **Purpose**: Catch YAML syntax errors early

**2. end-of-file-fixer** - Ensure files end with newline
- **Duration**: <1s
- **Fixes**: Adds newline if missing
- **Purpose**: POSIX compliance

**3. trailing-whitespace** - Remove trailing whitespace
- **Duration**: <1s
- **Fixes**: Removes trailing spaces/tabs
- **Purpose**: Clean diffs

**4. check-added-large-files** - Prevent large files (>500KB)
- **Duration**: <1s
- **Fixes**: None (blocks commit if file >500KB)
- **Purpose**: Prevent accidental large file commits

#### Code Quality (ruff v0.5.5 + mypy v1.11.0)

**5. ruff** (linting) - Lint code, fix violations
- **Duration**: <1s
- **Fixes**: Auto-fixes violations (--fix)
- **Purpose**: Style enforcement (F, E, W, I, N, UP, etc.)
- **Rules**: ~700 rules across multiple categories

**6. ruff-format** (formatting) - Format code (replaces black)
- **Duration**: <1s
- **Fixes**: Auto-formats code
- **Purpose**: Consistent code formatting
- **CRITICAL**: Must run AFTER ruff (check)

**7. mypy** (type checking) - Static type checking
- **Duration**: 1-3s
- **Fixes**: None (manual type hints required)
- **Purpose**: Type safety enforcement
- **Config**: --config-file=pyproject.toml

---

### CLI Commands

#### **setup-hooks** - Install Pre-Commit Hooks
```bash
just setup-hooks
# Installs: pre-commit hooks from .pre-commit-config.yaml
# Creates: .git/hooks/pre-commit
# Use: One-time setup per project
```

#### **lint** - Run Ruff Linting
```bash
just lint
# Runs: ruff check src/ tests/ scripts/
# Output: Linting violations (if any)
# Use: Manual linting without committing
```

#### **lint-fix** - Auto-Fix Ruff Violations
```bash
just lint-fix
# Runs: ruff check --fix src/ tests/ scripts/
# Output: Fixed violations
# Use: Automatically fix style issues
```

#### **format** - Format Code with Ruff
```bash
just format
# Runs: ruff format src/ tests/ scripts/
# Output: Formatted files
# Use: Manually format code (also runs in pre-commit)
```

#### **type-check** - Run Mypy Type Checking
```bash
just type-check
# Runs: mypy src/ tests/ scripts/
# Output: Type errors (if any)
# Use: Manual type checking without committing
```

#### **pre-merge** - All Quality Gates Before Merge
```bash
just pre-merge
# Runs: tests + lint + format + type-check
# Use: Final check before creating PR
```

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-005** (CI/CD) | Aligned Checks | Same ruff + mypy configs in pre-commit and CI workflows |
| **SAP-004** (Testing) | Pre-Merge Gate | `just pre-merge` runs tests + quality gates |
| **SAP-003** (Bootstrap) | Included by Default | Generated projects include .pre-commit-config.yaml |
| **SAP-008** (Automation) | Justfile Integration | Quality gate commands via justfile recipes |
| **SAP-011** (Docker) | Container Validation | Docker builds run quality gates before image creation |

**Cross-SAP Workflow Example**:
```bash
# Local Development (SAP-006)
git add src/my_feature.py
git commit -m "Add feature"  # Pre-commit runs:
# 1. check-yaml (<1s)
# 2. end-of-file-fixer (<1s)
# 3. trailing-whitespace (<1s)
# 4. check-added-large-files (<1s)
# 5. ruff linting (<1s)
# 6. ruff-format (<1s)
# 7. mypy type checking (1-3s)
# Total: <3s

# If Hooks Fail → Fix → Retry
just lint-fix            # Auto-fix ruff issues
# Fix type errors manually
git add src/my_feature.py
git commit -m "Add feature"  # ✅ Passes

# Push to GitHub (SAP-005)
git push origin feature-branch
# CI runs same checks (aligned with pre-commit)
```

---

## 🏆 Success Metrics

- **Speed**: <3s for all 7 hooks (vs 10-30s with legacy tools)
- **Ruff Performance**: 200x faster than flake8+isort+black combined
- **Auto-Fix Rate**: 80-90% of violations fixed automatically
- **Type Coverage**: Strict mypy mode enforces type hints
- **Blocked Commits**: 95%+ style/type issues caught before commit

---

## 🎓 Hook Execution Order

**CRITICAL**: ruff (check) MUST run before ruff-format for consistency.

```
git commit
    ↓
┌─────────────────────────────────────────────┐
│  Pre-Commit Hooks Execute (Sequential)      │
├─────────────────────────────────────────────┤
│  1. check-yaml (<1s)                       │
│  2. end-of-file-fixer (<1s)                │
│  3. trailing-whitespace (<1s)              │
│  4. check-added-large-files (<1s)          │
│  5. ruff (linting + --fix) (<1s)   ← FIRST │
│  6. ruff-format (formatting) (<1s) ← SECOND│
│  7. mypy (type checking) (1-3s)            │
└─────────────────────────────────────────────┘
    ↓
All Hooks Pass? ───┬─── ✅ Commit Succeeds
                   └─── ❌ Commit Blocked (fix issues)
```

**Why Order Matters**:
- ruff --fix modifies code → ruff-format then formats it
- If reversed: Formatting happens first → linting might change it again → inconsistent

---

## 🔧 Troubleshooting

**Problem**: `pre-commit run` fails with "command not found"

**Solution**: Install pre-commit tool:
```bash
pip install pre-commit
# or
brew install pre-commit  # macOS
```

---

**Problem**: Hooks fail every commit (annoying during development)

**Solution**: Temporarily bypass hooks (use sparingly):
```bash
git commit --no-verify -m "WIP: Temporary commit"
# Fix issues later:
just lint-fix
just type-check
# Amend commit:
git add .
git commit --amend --no-edit
```

---

**Problem**: Mypy fails with "No library stub file for module X"

**Solution**: Install type stubs:
```bash
pip install types-requests  # For requests library
pip install types-PyYAML    # For PyYAML library
# or ignore (add to pyproject.toml):
# [[tool.mypy.overrides]]
# module = "untyped_module"
# ignore_missing_imports = true
```

---

**Problem**: Ruff linting fails with rule violation I disagree with

**Solution**: Configure ruff in pyproject.toml:
```toml
[tool.ruff]
# Ignore specific rules
ignore = ["E501"]  # Ignore line length (if needed)

# Or per-file ignores
[tool.ruff.per-file-ignores]
"tests/*" = ["F401"]  # Allow unused imports in tests
```

---

**Problem**: Pre-commit hooks are slow (>10s)

**Solution**: Update to latest pre-commit hooks:
```bash
pre-commit autoupdate  # Update all hooks to latest versions
pre-commit clean       # Clear cache
pre-commit run --all-files  # Test speed
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete hook specifications, ruff/mypy configs (15KB)
- **[AGENTS.md](AGENTS.md)** - AI agent quality gate workflows (17KB, 9-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific quality gate patterns (15KB, 8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Pre-commit setup guide (5KB, 5-min read)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design
- **[ledger.md](ledger.md)** - Production adoption metrics

---

## 📞 Support

- **Documentation**: Read [protocol-spec.md](protocol-spec.md) for complete reference
- **Issues**: Report bugs via GitHub issues with `[SAP-006]` prefix
- **Feedback**: Log adoption feedback in [ledger.md](ledger.md)
- **Ruff Docs**: See ruff.rs for rule reference
- **Mypy Docs**: See mypy.readthedocs.io for type checking guide

---

## 🔍 Ruff vs Legacy Tools

| Metric | Ruff | flake8+isort+black |
|--------|------|-------------------|
| **Speed** | <1s | 10-30s |
| **Tools Count** | 1 | 3 |
| **Rules** | 700+ | 500+ (combined) |
| **Auto-Fix** | ✅ Built-in | ❌ Limited |
| **Python** | ✅ Python | ✅ Python |
| **Written In** | Rust | Python |

**Verdict**: Ruff is 200x faster, consolidates 3 tools into 1, and provides better auto-fix capabilities.

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial quality gates with ruff + mypy, 7 pre-commit hooks, <3s feedback

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
