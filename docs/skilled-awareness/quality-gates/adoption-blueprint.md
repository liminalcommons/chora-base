# Adoption Blueprint: Quality Gates

**SAP ID**: SAP-006
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides using chora-base's pre-commit hooks for code quality.

**Time Estimate**: 5-10 minutes to setup, <5 seconds per commit

---

## 2. Prerequisites

- Generated project from chora-base (SAP-003)
- Dependencies installed (`pip install -e ".[dev]"`)

---

## 3. Quick Start

### Step 1: Install Hooks

```bash
pre-commit install
```

**Output**:
```
pre-commit installed at .git/hooks/pre-commit
```

### Step 2: Test Hooks

```bash
pre-commit run --all-files
```

**Expected**: All hooks pass ✅

### Step 3: Make a Commit

```bash
git add .
git commit -m "feat: Add new feature"
```

**Hooks run automatically**:
- check-yaml ✅
- trailing-whitespace ✅
- ruff ✅
- ruff-format ✅
- mypy ✅

**Commit succeeds** if all hooks pass

---

## 4. When Hooks Fail

**Example failure**:
```
ruff....................................Failed
- hook id: ruff
- exit code: 1

src/my_package/module.py:10:1: F401 [*] `os` imported but unused
```

**Fix**:
```bash
# Option 1: Auto-fix
ruff check . --fix
git add .
git commit -m "feat: Add new feature"

# Option 2: Manual fix
# Edit src/my_package/module.py, remove unused import
git add .
git commit -m "feat: Add new feature"
```

---

## 5. Customizing Quality Gates

**Change ruff line length**:
```toml
# pyproject.toml
[tool.ruff]
line-length = 100  # Change from 88 to 100
```

**Disable specific ruff rule**:
```toml
# pyproject.toml
[tool.ruff.lint]
ignore = ["E501"]  # Ignore line-length violations
```

**Best Practice**: Understand rule before disabling

---

## 6. Troubleshooting

**Problem**: Hooks take too long
**Solution**: Hooks should complete in <5s. If slower, check for network issues or large files.

**Problem**: Mypy errors overwhelming
**Solution**: Start with specific modules, gradually expand:
```toml
# pyproject.toml
[tool.mypy]
files = ["src/my_package/core"]  # Start small
```

---

## 7. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Quality Gates capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover pre-commit hooks and quality checks
- Quick reference for quality gate operations
- Links to configuration documentation

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
### Quality Gates

Pre-commit hooks enforcing code quality with ruff, mypy, and automated formatting.

**Documentation**: [docs/skilled-awareness/quality-gates/](docs/skilled-awareness/quality-gates/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/quality-gates/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/quality-gates/awareness-guide.md)

**Key Commands**:
- Install hooks: `pre-commit install`
- Run all hooks: `pre-commit run --all-files`
- Auto-fix issues: `ruff check . --fix`
```

**Validation**:
```bash
grep "Quality Gates" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 8. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint
