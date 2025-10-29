# Awareness Guide: Quality Gates

**SAP ID**: SAP-006
**Version**: 1.0.0
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

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

## 4. Best Practices

**DO**:
- ✅ Run `pre-commit run --all-files` before committing
- ✅ Use `ruff check --fix` to auto-fix violations
- ✅ Add type annotations to all functions

**DON'T**:
- ❌ Skip hooks with `--no-verify`
- ❌ Disable ruff rules without understanding them
- ❌ Ignore mypy errors

---

## 5. Related Resources

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [.pre-commit-config.yaml](../../../../static-template/.pre-commit-config.yaml)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide
