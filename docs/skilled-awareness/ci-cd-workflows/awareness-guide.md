# Awareness Guide: CI/CD Workflows

**SAP ID**: SAP-005
**Version**: 1.0.0
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

**View workflow status**:
```bash
# In GitHub UI: Actions tab → Select workflow → View runs
```

**Run workflow locally** (test.yml equivalent):
```bash
pytest --cov=src --cov-report=term --cov-fail-under=85
```

**Run workflow locally** (lint.yml equivalent):
```bash
ruff check .
mypy src
```

---

## 2. Agent Context Loading

**Essential Context (2-3k tokens)**:
- [protocol-spec.md](protocol-spec.md) Sections 2, 3 - Workflow inventory, specifications

**For debugging failures**:
- [protocol-spec.md](protocol-spec.md) Section 8 - Error handling

---

## 3. Common Workflows

### 3.1 Interpret Test Workflow Failure

**Context**: 2k tokens (Protocol Section 3.1)

**Steps**:
1. Check GitHub Actions logs
2. Identify failure type:
   - Tests failed → Check pytest output
   - Coverage <85% → Check coverage report
   - Cache miss → Normal (will rebuild cache)
3. Fix locally, push again

### 3.2 Modify Workflow Safely

**Context**: 3k tokens (Protocol Sections 3, 6)

**Steps**:
1. Read existing workflow (.github/workflows/<name>.yml)
2. Understand contract (triggers, guarantees from Protocol)
3. Make minimal changes
4. Test locally if possible
5. Commit and watch workflow run

---

## 4. Best Practices

**DO**:
- ✅ Use caching for pip dependencies
- ✅ Keep security workflows enabled
- ✅ Test locally before relying on CI

**DON'T**:
- ❌ Disable CodeQL or security workflows
- ❌ Skip required workflows
- ❌ Increase timeout without investigating root cause

---

## 5. Related Resources

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [adoption-blueprint.md](adoption-blueprint.md) - Usage guide
- [.github/workflows/](../../../../static-template/.github/workflows/) - Workflow files

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide
