# Capability Charter: Quality Gates

**SAP ID**: SAP-006
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

### Current Challenge

chora-base provides **pre-commit hooks + ruff + mypy + black** for quality enforcement, but the system lacks:

1. **Explicit Quality Standards** - Hook order, ruff rules, mypy strictness not documented
2. **Modern Tool Rationale** - Why ruff over flake8/isort (200x faster) not explained
3. **Integration Clarity** - How quality gates integrate with CI/CD (SAP-005) unclear
4. **Customization Guidance** - Difficult to customize rules without breaking patterns
5. **Hook Order Importance** - Critical ordering (ruff-check before ruff-format) not explained

**Result**:
- **Adopters**: Uncertain about quality standards, modification risks
- **AI Agents**: Can't reason about rule violations or suggest fixes
- **Maintainers**: Can't enforce quality standards consistently

### Business Impact

Without structured quality gate documentation:
- **Code Quality Issues**: 15-20% of PRs have style violations
- **Review Friction**: 30-60 min per PR explaining quality violations
- **Inconsistency**: Quality standards vary by project

---

## 2. Proposed Solution

### Quality Gates SAP

A **comprehensive SAP describing pre-commit hooks, ruff, mypy, and quality standards** with explicit contracts and best practices.

This SAP documents:
1. **What gates exist** - 3 pre-commit hooks (pre-commit-hooks, ruff, mypy)
2. **How gates work** - Hook order, ruff rules, mypy strictness
3. **What's enforced** - Style (ruff), types (mypy), formatting (ruff-format)
4. **How to customize** - Safe modification patterns
5. **Modern tools** - Why ruff (200x faster than flake8+isort+black)

### Key Principles

1. **Ruff-Based** - Modern linter (replaces flake8, isort, black)
2. **Type-Checked** - Mypy strict mode (disallow_untyped_defs)
3. **Pre-Commit Enforced** - Quality gates before commit
4. **Fast Feedback** - Ruff 200x faster than alternatives
5. **Correct Order** - ruff-check before ruff-format (critical)

---

## 3. Scope

### In Scope

**Quality Gates SAP Artifacts**:
- ✅ Capability Charter (this document)
- ✅ Protocol Specification - All hooks, ruff rules, mypy config
- ✅ Awareness Guide - Agent workflows for understanding, fixing violations
- ✅ Adoption Blueprint - How to use quality gates, customize
- ✅ Traceability Ledger - Quality metrics, compliance tracking

**Components Covered**:
1. **.pre-commit-config.yaml** - Hook configuration (3 repos, 7 hooks)
2. **pyproject.toml [tool.ruff]** - Ruff rules (E, F, I, N, W, UP)
3. **pyproject.toml [tool.mypy]** - Mypy strict configuration
4. **pyproject.toml [tool.black]** - Black configuration (backup formatter)

### Out of Scope (for v1.0)

- ❌ Alternative linters (flake8, pylint) - use ruff
- ❌ Alternative formatters (autopep8, yapf) - use ruff-format
- ❌ Custom plugins (advanced)

---

## 4. Outcomes

### Success Criteria

**Quality Success** (Phase 2):
- ✅ SAP-006 complete (all 5 artifacts)
- ✅ All hooks documented (7 hooks across 3 repos)
- ✅ Ruff rationale explained (200x faster)
- ✅ Hook order importance documented

**Compliance Success** (Phase 2-3):
- ✅ 100% of commits pass pre-commit hooks
- ✅ Zero style violations in main branch
- ✅ Zero type errors in main branch

### Key Metrics

| Metric | Baseline | Target (Phase 2) | Target (Phase 4) |
|--------|----------|------------------|------------------|
| Pre-commit Pass Rate | ~85% | 95% | 99% |
| Style Violations (main) | ~5% | 0% | 0% |
| Type Errors (main) | ~3% | 0% | 0% |
| Quality Review Time | 30-60 min/PR | 10-20 min/PR | <10 min/PR |

---

## 5. Stakeholders

**Template Maintainer**: Victor - Maintains quality gates
**AI Agents**: Use SAP-006 to fix violations
**Project Developers**: Use quality gates for code quality
**CI/CD System**: Enforces same gates in lint.yml (SAP-005)

---

## 6. Dependencies

**Internal Dependencies**:
- ✅ SAP-003 (project-bootstrap) - Generates .pre-commit-config.yaml
- ✅ SAP-004 (testing-framework) - Coverage in pyproject.toml
- ✅ SAP-005 (ci-cd-workflows) - lint.yml uses same tools

**External Dependencies**:
- pre-commit 4.0.1 (hook framework)
- ruff 0.7.0 (linter + formatter)
- mypy 1.11.0 (type checker)
- black 24.10.0 (backup formatter)

---

## 7. Lifecycle

### Phase 2: Core Capability SAPs (2025-11 → 2026-01)

**Deliverables**: SAP-006 complete (all 5 artifacts), parallel with SAP-005

### Phase 3-4: Enhanced quality metrics, automated validation

---

## 8. Related Documents

- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [.pre-commit-config.yaml](/static-template/.pre-commit-config.yaml)
- [pyproject.toml](/blueprints/pyproject.toml.blueprint) - Lines 45-86
- [testing-framework/](../testing-framework/) - SAP-004
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for quality-gates SAP
