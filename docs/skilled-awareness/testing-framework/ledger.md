# Traceability Ledger: Testing Framework

**SAP ID**: SAP-004
**Current Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Projects Using Testing Framework

| Project | Coverage | Status | Last Updated | Notes |
|---------|----------|--------|--------------|-------|
| chora-base | 49.7% | Improving | 2025-11-04 | Below 85% target - working toward compliance, example tests in static-template |
| chora-compose | ~80% | Active | 2025-10-20 | Working toward 85% |
| mcp-n8n | ~75% | Active | 2025-10-22 | Coverage improvement in progress |
| _Other projects_ | - | - | - | Add as adopted |

**Legend**:
- **Coverage**: Test coverage percentage (from pytest --cov)
- **Status**: Active (using framework), Improving (working toward 85%), Archived (deprecated)
- **Last Updated**: Last coverage measurement (YYYY-MM-DD)

---

## 2. Version History

| Version | Release Date | Type | Changes | Migration Required |
|---------|--------------|------|---------|-------------------|
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-004 release: pytest 8.3.0, pytest-asyncio 0.24.0, pytest-cov 6.0.0, 85% coverage standard, async patterns | N/A (initial) |

**Legend**:
- **Type**: MAJOR (breaking changes), MINOR (features), PATCH (fixes)
- **Migration Required**: Y/N, link to upgrade blueprint if yes

---

## 3. Coverage Tracking

### Phase 2 (Current)

**Target**: Document testing framework (SAP-004 complete)
**Actual**: SAP-004 complete (all 5 artifacts)
**Status**: ✅ On track

**Coverage Metrics**:
- **chora-base** (template): 49.7% (below 85% target)
  - utils/: 100% (test_validation.py, test_errors.py, test_responses.py, test_persistence.py)
  - scripts/: Minimal coverage (inbox tools, sap-evaluator not fully tested)
  - memory/: Not yet tested (future - SAP-010 not implemented)
  - mcp/: Not yet tested (project-specific)
  - **Gap**: Need to add tests for scripts/ and increase overall coverage to ≥85%
- **chora-compose**: ~80% (working toward 85%)
- **mcp-n8n**: ~75% (coverage improvement in progress)

**Compliance**:
- Projects at ≥85%: 0/3 (0%) - No projects meeting target yet
- Target: 3/3 (100%) by end of Phase 2

### Phase 3 (2026-01 → 2026-03)

**Planned Metrics**:
- All projects ≥85% coverage
- Test pattern reuse ≥80%
- CI test failures (config issues) <10%

### Phase 4 (2026-03 → 2026-05)

**Planned Metrics**:
- Automated coverage tracking
- Test quality metrics (flakiness, speed)
- Coverage dashboard

---

## 4. Test Pattern Usage

### Current Patterns (v1.0.0)

| Pattern | Usage | Example Location | Status |
|---------|-------|------------------|--------|
| Basic test | 100% | static-template/tests/utils/test_validation.py | ✅ Active |
| Parametrized test | ~60% | static-template/tests/utils/test_validation.py | ✅ Active |
| Async test | ~20% | (project-specific, not in template yet) | ✅ Active |
| Fixture | ~40% | (project-specific) | ✅ Active |
| Mock | ~30% | (project-specific) | ✅ Active |
| Error testing | ~80% | static-template/tests/utils/test_validation.py | ✅ Active |

**Pattern Reuse Target**: ≥80% by Phase 3

---

## 5. Known Issues

### Active Issues

**Issue: chora-base coverage at 49.7%, below 85% target**
- **Description**: chora-base itself has 49.7% coverage vs. 85% target documented in SAP-004
- **Severity**: High (template doesn't dogfood own standards)
- **Root Cause**: scripts/ directory has minimal test coverage (inbox tools, sap-evaluator)
- **Workaround**: Focus on utils/ which has 100% coverage as reference examples
- **Status**: Identified 2025-11-04
- **Fix**: Planned for Phase 3 - add comprehensive tests for scripts/ to achieve 85%+

**Issue: Async test patterns not in template examples**
- **Description**: static-template includes utils tests only, no async MCP server tests
- **Severity**: Medium (developers must create own async patterns)
- **Workaround**: Reference SAP-004 Protocol Section 7.4 for async patterns
- **Status**: Documented in Protocol
- **Fix**: Planned for v1.1.0 (add example async MCP server test)

**Issue: Coverage calculation includes __init__.py**
- **Description**: pytest-cov includes __init__.py files which often have low coverage
- **Severity**: Low (minor coverage impact)
- **Workaround**: Accept that __init__.py may drag down coverage slightly
- **Status**: Expected behavior
- **Fix**: Not planned (standard pytest-cov behavior)

### Resolved Issues

_None yet_ - SAP-004 is new

---

## 6. Testing Tool Versions

### Current (v1.0.0)

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| pytest | 8.3.0 | Test runner | ✅ Active |
| pytest-asyncio | 0.24.0 | Async test support | ✅ Active |
| pytest-cov | 6.0.0 | Coverage measurement | ✅ Active |
| Python | 3.11+ | Runtime | ✅ Active |

### Upgrade History

_None yet_ - Initial versions

### Future Upgrades

**pytest 9.x**:
- Monitor for breaking changes
- Test compatibility
- Update SAP-004 if patterns change

**pytest-asyncio 1.x**:
- Async mode may change
- Test with asyncio_mode = "auto"
- Update Protocol if needed

---

## 7. Coverage Standards Evolution

### Phase 2 (Current): 85% Minimum

**Rationale**:
- Based on industry research (80-85% optimal)
- Balance between quality and effort
- Above 85% shows diminishing returns

**Enforcement**:
- pyproject.toml: `--cov-fail-under=85`
- CI workflow: Fails if coverage <85%
- Pre-commit: Optional coverage check

**Exceptions**:
- Boilerplate code (__init__.py): May be <85%
- Generated code: Excluded from coverage
- Deprecated code: May be <85%

### Phase 3-4: Maintain 85%

**No Change Planned**: 85% remains optimal target

**Potential Additions**:
- Branch coverage (in addition to line coverage)
- Test quality metrics (assertions per test)
- Flakiness tracking

---

## 8. CI/CD Integration

### GitHub Actions Workflow

**Current** (.github/workflows/test.yml):
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=term-missing --cov-report=xml
```

**Workflow Behavior**:
- Runs on: push, pull_request
- Matrix: Python 3.11, 3.12
- Fails if: Tests fail OR coverage <85%
- Reports: Coverage to Codecov (optional)

**Success Rate**:
- Baseline: ~95% (5% failures due to coverage issues)
- Target: 100% (Phase 3-4)

---

## 9. Performance Tracking

### Test Suite Performance

| Project | Test Count | Time (local) | Time (CI) | Target |
|---------|------------|--------------|-----------|--------|
| chora-base template | ~5 | <1s | ~2s | <60s |
| chora-compose | ~15 | ~3s | ~5s | <60s |
| mcp-n8n | ~20 | ~4s | ~7s | <60s |

**Performance Guidelines**:
- Target: <60s for local development (fast feedback)
- CI may be slower (matrix testing)
- Use mocks to speed up tests (avoid network calls)

### Test Quality Metrics

**Current** (Phase 2):
- Assertions per test: Not tracked yet
- Test flakiness: Not tracked yet
- Test maintainability: Not tracked yet

**Planned** (Phase 4):
- Track assertions per test (target: ≥1)
- Track flakiness (intermittent failures)
- Measure test maintenance time

---

## 10. Adoption Feedback

### Phase 2 Feedback (2025-10 → 2026-01)

**Collected From**: chora-base maintainer (Victor), early adopters

**Key Themes**:
- ✅ **pytest clarity**: pytest patterns clear, easy to follow
- ✅ **Coverage target**: 85% feels achievable and meaningful
- ⚠️ **Async patterns**: Async test examples needed in template
- ✅ **CI integration**: Automatic testing works well
- ⚠️ **Coverage gaps**: Error path testing often missed

**Action Items**:
- ✅ Document testing framework (SAP-004 created)
- 🔄 Add async MCP server test example (planned for v1.1.0)
- 🔄 Emphasize error path testing in docs (updated in Protocol)
- 🔄 Track coverage compliance across projects (ledger tracking)

### Phase 3 Feedback (Future)

_Not yet collected_

---

## 11. Compliance & Audit

### Testing Quality Gates

**Current** (Phase 2):
- ✅ pytest configuration documented
- ✅ Coverage standard documented (85%)
- ✅ Test patterns documented (6 patterns)
- ✅ CI integration documented
- ⚠️ Automated compliance checking: Not yet implemented

**Planned** (Phase 4):
- Automated pattern validation (CI check)
- Coverage tracking dashboard
- Test quality metrics dashboard

### Audit Trail

| Date | Auditor | Finding | Resolution |
|------|---------|---------|------------|
| 2025-10-28 | Claude Code | SAP-004 created | Complete documentation of testing framework |
| _Future audits_ | - | - | - |

---

## 12. Related Documents

**SAP-004 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to use testing

**Testing Components**:
- [pyproject.toml](/blueprints/pyproject.toml.blueprint) - pytest configuration (lines 45-50)
- [static-template/tests/](/static-template/tests/) - Example tests
- [.github/workflows/test.yml](/static-template/.github/workflows/test.yml) - Test workflow

**Related SAPs**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (runs tests in CI)
- [quality-gates/](../quality-gates/) - SAP-006 (enforces coverage)

---

## 13. How to Update This Ledger

### Adding Project Coverage

**When**: New project reaches ≥85% coverage or adopts testing framework

**Steps**:
1. Add row to "Projects Using Testing Framework" table:
   ```markdown
   | <project-name> | <coverage>% | Active | <today> | <notes> |
   ```
2. Update coverage compliance metrics
3. Commit message: `docs(SAP-004): Add <project-name> coverage tracking`

### Recording Coverage Changes

**When**: Project coverage changes significantly (±5%)

**Steps**:
1. Update coverage in "Projects Using Testing Framework" table
2. Update "Last Updated" date
3. Add note if significant change
4. Commit message: `docs(SAP-004): Update <project-name> coverage (<old>% → <new>%)`

### Recording Pattern Usage

**When**: New test pattern created or existing pattern usage changes

**Steps**:
1. Update "Test Pattern Usage" table
2. Add example location if new pattern
3. Update usage percentage
4. Commit message: `docs(SAP-004): Update pattern usage (<pattern-name>)`

### Recording Tool Upgrades

**When**: pytest, pytest-asyncio, or pytest-cov upgraded

**Steps**:
1. Add row to "Upgrade History" (in "Testing Tool Versions")
2. Update "Current" versions
3. Test all patterns with new versions
4. Update Protocol if patterns change
5. Commit message: `chore(SAP-004): Upgrade <tool> to v<version>`

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger for testing-framework SAP
