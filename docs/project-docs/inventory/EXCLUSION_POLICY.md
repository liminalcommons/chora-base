# SAP Coverage Exclusion Policy

**Version**: 1.0
**Date**: 2025-10-28
**Status**: Active

---

## Purpose

This document defines which files and directories are intentionally excluded from SAP (Skilled Awareness Package) coverage in the chora-base repository.

---

## Excluded Directories

### 1. `examples/`

**Status**: Intentionally excluded from SAP coverage
**Rationale**: The `examples/` directory contains reference implementations and template projects that demonstrate how to use chora-base. These are meant to be:
- **Self-contained**: Complete working examples that users can copy and modify
- **Template nature**: Not part of the core framework, but demonstrations of it
- **Evolving**: May be added, removed, or updated without impacting SAP coverage
- **User-facing**: Intended for users to explore and learn from, not as part of the SAP system

**Decision date**: 2025-10-28
**Decision maker**: User (Priority 3, Option C selected)

**Excluded paths**:
- `examples/full-featured-with-vision/` (34 files)
- Any future examples added to `examples/` directory

**Coverage implications**: Files in the `examples/` directory will not be counted in SAP coverage metrics and will not be inventoried.

---

### 2. Standard Development Exclusions

The following directories are excluded as standard development artifacts that should not be tracked:

- `.git/` - Git repository metadata
- `__pycache__/` - Python bytecode cache
- `.pytest_cache/` - Pytest cache
- `.mypy_cache/` - MyPy type checker cache
- `.ruff_cache/` - Ruff linter cache
- `node_modules/` - Node.js dependencies
- `venv/`, `.venv/` - Python virtual environments
- `dist/` - Distribution artifacts
- `build/` - Build artifacts
- `*.egg-info/` - Python package metadata
- `.DS_Store` - macOS filesystem metadata
- `test-output/` - Temporary test output

---

## Archived Content Policy

### Deleted in Phase 2

**`docs/reference/chora-compose/`** (121 files)
**Status**: Deleted
**Date**: 2025-10-28
**Rationale**: Chora-compose documentation was obsolete and no longer relevant to current architecture.

---

## Coverage Validation

### Current State (Phase 2 Complete)

- **Total files inventoried**: 266 files
- **SAP coverage**: 266 files (100.0%)
- **Excluded from inventory**: `examples/` directory (~34 files)
- **Intentional exclusions**: Standard development artifacts (see section 2 above)

### Coverage Formula

```
SAP Coverage % = (Files Covered by SAPs) / (Total Inventoried Files) × 100
```

**Note**: Excluded directories are not counted in either numerator or denominator.

---

## Review and Updates

This policy should be reviewed when:
1. New top-level directories are created
2. Major architectural changes occur
3. New example projects are added
4. SAP framework undergoes significant changes

**Next review date**: 2026-01-28 (3 months from Phase 2 completion)

---

## Related Documents

- [SAP Framework Protocol](../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [Inventory Summary](./inventory-summary.md)
- [Phase 2 Findings and Recommendations](./phase2-findings-and-recommendations.md)
- [SAP Coverage Matrix](./sap-coverage-matrix.md)
