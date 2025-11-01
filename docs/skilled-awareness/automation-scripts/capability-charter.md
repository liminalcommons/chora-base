---
sap_id: SAP-008
version: 1.0.0
status: Draft
last_updated: 2025-10-28
scope: Implementation
---

# Capability Charter: Automation Scripts

**SAP ID**: SAP-008
**Capability Name**: automation-scripts
**Version**: 1.0.0
**Status**: Draft (Phase 3)

---

## 1. Problem Statement

### Current State

chora-base includes 25 automation scripts (shell + Python) and a justfile with 30+ commands, but **lacks a single authoritative SAP** that:

1. **Defines safety contracts** for scripts (idempotency, error handling, rollback)
2. **Documents script categories** (setup, development, release, safety)
3. **Specifies justfile interface** as the unified developer entry point
4. **Establishes validation standards** for script robustness
5. **Tracks script adoption** across projects

### User Pain Points

**From INDEX.md**:
> "Current Adopter Pain: Standards for safety/idempotency assumed rather than contractually defined"

**Specific Issues**:
- Scripts lack consistent error handling
- Idempotency not guaranteed (unsafe to re-run some scripts)
- No rollback mechanism for failed operations
- Documentation scattered (header comments vary in quality)
- No clear interface (users invoke scripts directly vs through justfile)

### Impact

**Without this SAP**:
- ❌ Scripts may corrupt state when run multiple times
- ❌ Failed operations leave system in undefined state
- ❌ Developers unsure which script to use for which task
- ❌ Onboarding developers spend hours learning script ecosystem
- ❌ No systematic validation of script robustness

**With this SAP**:
- ✅ All scripts guaranteed idempotent (safe to re-run)
- ✅ Error handling standardized (clear messages, exit codes)
- ✅ Rollback mechanisms for critical operations
- ✅ Unified justfile interface reduces learning curve by 80%
- ✅ Validation standards ensure script quality

---

## 2. Proposed Solution

A **comprehensive SAP defining contracts for 25 automation scripts** organized by category, with **justfile as the unified interface**.

**Key Principles**:
1. **Idempotency** - All scripts safe to re-run (check-before-act pattern)
2. **Error Handling** - Consistent error messages, non-zero exit codes on failure
3. **Rollback Support** - Critical scripts support rollback on failure
4. **Unified Interface** - `just <task>` as primary entry point (not `./scripts/<script>.sh`)
5. **Documentation** - Header comments with usage, examples, safety notes

**Scope**: Implementation level only
- Scripts support development lifecycle (SAP-012 phases)
- Scripts enforce quality gates (SAP-006)
- Scripts automate release process (SAP-012 Phase 7)

---

## 3. Capability Definition

### What This SAP Includes

**Scripts** (25 total in `static-template/scripts/`):

**Category 1: Setup & Environment** (4 scripts)
- `setup.sh` - Initial project setup (venv, deps, hooks)
- `venv-create.sh` - Create virtual environment
- `venv-clean.sh` - Clean/recreate virtual environment
- `check-env.sh` - Validate environment (Python version, deps)

**Category 2: Development** (4 scripts)
- `dev-server.sh` - Start development server (if applicable)
- `smoke-test.sh` - Quick validation (~10 seconds)
- `integration-test.sh` - Integration tests
- `diagnose.sh` - Diagnose environment issues

**Category 3: Version Management** (2 scripts)
- `bump-version.sh` - Semantic version bumping (major/minor/patch)
- `prepare-release.sh` - Prepare release (run checks, update changelog)

**Category 4: Release & Publishing** (4 scripts)
- `build-dist.sh` - Build distribution packages (.tar.gz, .whl)
- `publish-test.sh` - Publish to test.pypi.org
- `publish-prod.sh` - Publish to pypi.org (production)
- `verify-stable.sh` - Verify stable release candidate

**Category 5: Safety & Recovery** (2 scripts)
- `rollback-dev.sh` - Rollback failed development changes
- `pre-merge.sh` - Pre-merge validation (all quality gates)

**Category 6: Documentation** (5 Python scripts)
- `validate_docs.py` - Validate frontmatter, links, structure
- `extract_tests.py` - Extract tests from How-To docs (SAP-007)
- `docs_metrics.py` - Calculate documentation metrics
- `generate_docs_map.py` - Generate documentation sitemap
- `query_docs.py` - Query documentation (search, filter)

**Category 7: MCP & Specialized** (2 scripts)
- `mcp-tool.sh` - MCP server development tools
- `validate_mcp_names.py` - Validate MCP naming conventions

**Category 8: Migration & Handoff** (2 scripts)
- `migrate_namespace.sh` - Migrate package namespaces
- `handoff.sh` - Handoff checklist for project transfers

**Justfile** (~150 lines, 30+ commands):
- Unified interface for all scripts
- Task categories: setup, testing, linting, building, releasing
- Examples: `just test`, `just pre-merge`, `just prepare patch`

### What This SAP Excludes

- Script implementation details (covered by script files themselves)
- Workflow processes (covered by SAP-012: development-lifecycle)
- CI/CD automation (covered by SAP-005: ci-cd-workflows)
- Pre-commit hooks (covered by SAP-006: quality-gates)

---

## 4. Success Criteria

### Adoption Metrics

**Target**: 90% of chora-base adopters use justfile interface (not direct script invocation)

**Measurement**:
- Presence of `justfile` in project root
- `scripts/` directory follows chora-base conventions
- Scripts pass validation (idempotency, error handling)

### Quality Metrics

**Target**: 100% of scripts follow safety contracts

**Measurement**:
- Idempotency: All scripts can be run multiple times safely
- Error handling: All scripts use `set -euo pipefail` (bash best practice)
- Documentation: All scripts have header comments (usage, examples)
- Exit codes: All scripts return 0 (success) or non-zero (failure)

### Efficiency Metrics

**Target**: 80% reduction in script-related onboarding time

**Measurement**:
- Time to learn script ecosystem: <30 minutes (vs 2+ hours without justfile)
- `just --list` provides complete command reference
- `just help` shows common workflows

---

## 5. Dependencies

### Upstream Dependencies

- **SAP-000** (sap-framework): Provides SAP structure and governance
- **SAP-012** (development-lifecycle): Scripts support lifecycle phases

### Downstream Dependencies

- All chora-base capabilities use scripts (setup, testing, release)
- SAP-006 (quality-gates): pre-commit hooks call scripts
- SAP-007 (documentation-framework): extract_tests.py, validate_docs.py

### Cross-References

- **SAP-012 Phase 5** (Testing): Uses `pre-merge.sh`, `smoke-test.sh`
- **SAP-012 Phase 7** (Release): Uses `bump-version.sh`, `prepare-release.sh`, `publish-prod.sh`
- **SAP-006**: Pre-commit hooks validate scripts run successfully

---

## 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Script failures corrupt state** | Critical | Require idempotency, add rollback mechanisms |
| **Inconsistent script interfaces** | Medium | Enforce justfile as unified interface, deprecate direct invocation |
| **Scripts not portable** (Linux vs macOS) | Medium | Test on both platforms, use portable bash constructs |
| **Error messages unclear** | Low | Standardize error message format (script name, issue, remedy) |
| **Scripts become stale** | Medium | Ledger tracks script versions, automated validation |

---

## 7. Open Questions

1. **Platform support**: Linux + macOS only, or add Windows (WSL) support?
2. **Script language**: Bash for simplicity vs Python for portability?
3. **Rollback granularity**: Per-script rollback or transaction-based rollback?

---

## 8. Related Capabilities

- **SAP-000** (sap-framework): Meta-framework for all SAPs
- **SAP-004** (testing-framework): Scripts run pytest
- **SAP-005** (ci-cd-workflows): CI workflows call scripts
- **SAP-006** (quality-gates): Pre-commit hooks use scripts
- **SAP-007** (documentation-framework): Documentation scripts (validate_docs.py, extract_tests.py)
- **SAP-012** (development-lifecycle): Scripts support all 8 phases

---

## 9. Approval & Sign-Off

**Charter Author**: Claude Code
**Date**: 2025-10-28
**Status**: Draft - Ready for Protocol Spec

**Approved By**: _(Pending Victor review)_

---

**Next Steps**:
1. Create [protocol-spec.md](protocol-spec.md) - Define script contracts, justfile interface, validation standards
2. Create [awareness-guide.md](awareness-guide.md) - Agent workflows for using scripts
3. Create [adoption-blueprint.md](adoption-blueprint.md) - How to adopt scripts in projects
4. Create [ledger.md](ledger.md) - Track script adoption and metrics
