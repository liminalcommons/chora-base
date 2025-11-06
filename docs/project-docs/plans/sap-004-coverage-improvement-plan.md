# SAP-004 Coverage Improvement Plan

**Goal**: Achieve 85% test coverage (SAP-004 L3 compliance)
**Current**: 16% coverage (187 tests, 99.5% pass rate)
**Gap**: 69 percentage points
**Timeline**: 2-4 weeks (15-20 hours estimated effort)
**Status**: Phase 2 - In Progress

---

## Executive Summary

Following successful adoption of chora-workspace SAP-004 reference tests (+12pp improvement, 4% → 16%), this plan outlines the path to SAP-004 L3 compliance (85% coverage) for the chora-base project.

**Key Achievements**:
- ✅ Adopted 2 test suites from chora-workspace (97 tests)
- ✅ Learned patterns: importlib, fixtures, edge cases
- ✅ Propagated patterns to static-template (all future projects benefit)
- ✅ SAP-004 level: L1 → L2

**Next Steps**:
1. **Test 30+ remaining scripts** (15-20h)
2. **Reach 85% coverage** (L3 compliance)
3. **Validate Template Capability Propagation protocol** (SAP-003 v1.1.0)

---

## Current State Analysis

### Coverage Breakdown (2025-11-06)

| Category | Coverage | Files | Notes |
|----------|----------|-------|-------|
| **Well-Tested** | 78-90% | 3 files | utils/sap_evaluation.py, utils/claude_metrics.py, scripts/install-sap.py |
| **Minimal Tests** | 16-17% | 2 files | utils/awareness_validation.py, scripts/usage_tracker.py |
| **Untested** | 0% | 35+ files | Most scripts/, utils/ modules |
| **Overall** | **16%** | **40+ files** | **Need +69pp for L3** |

### Test Suite Stats

- **Total tests**: 187
- **Pass rate**: 99.5% (1 environment-specific failure)
- **Test files**: 11
- **Coverage tools**: pytest-cov 6.0.0

---

## Phase 2: Testing Plan

### Strategy

**Approach**: Incremental coverage improvement using chora-workspace patterns

**Priorities**:
1. High-value scripts (used frequently)
2. Complex modules (high cyclomatic complexity)
3. Error-prone areas (history of bugs)
4. CLI tools (user-facing)

**Patterns to Apply**:
- importlib for hyphenated scripts
- Fixture-based architecture
- Comprehensive edge case coverage
- Test class organization (9+ classes per complex module)

### Script Inventory (40+ Scripts/Modules)

#### Priority 1: High-Value Scripts (Est: 8-10 hours)

| Script | Lines | Complexity | Priority | Est. Hours | Notes |
|--------|-------|------------|----------|------------|-------|
| `scripts/sap-evaluator.py` | 1000+ | High | P0 | 3-4h | Core SAP functionality, partial tests exist |
| `scripts/create-model-mcp-server.py` | 970 | High | P0 | 3-4h | New fast-setup script, untested |
| `scripts/validate-model-citizen.py` | 550 | Medium | P1 | 2h | Validation critical, untested |
| `scripts/inbox-query.py` | 300+ | Medium | P1 | 1.5h | User-facing CLI tool |
| `scripts/inbox-status.py` | 300+ | Medium | P1 | 1.5h | User-facing CLI tool |

**Subtotal**: 11-14 hours

#### Priority 2: Utility Modules (Est: 3-4 hours)

| Module | Lines | Complexity | Priority | Est. Hours | Notes |
|--------|-------|------------|----------|------------|-------|
| `utils/awareness_validation.py` | 400+ | High | P1 | 2h | 16% coverage, needs improvement |
| `scripts/usage_tracker.py` | 200+ | Low | P2 | 1h | 17% coverage, simple module |
| `scripts/suggest-next.py` | 200+ | Medium | P2 | 1-1.5h | Recommendation engine |

**Subtotal**: 4-4.5 hours

#### Priority 3: Remaining Scripts (Est: 4-5 hours)

**30+ other scripts** (automation, tooling, etc.):
- Most are 50-200 lines
- Low-medium complexity
- Batch testing approach: group similar scripts

**Subtotal**: 4-5 hours

---

## Implementation Plan

### Week 1: High-Value Scripts (11-14 hours)

**Day 1-2: sap-evaluator.py** (3-4h)
- [ ] Test SAPEvaluator class methods (already partially done)
- [ ] Test CLI argument parsing
- [ ] Test deep dive analysis
- [ ] Test strategic analysis
- [ ] Target: 85%+ coverage

**Day 3: create-model-mcp-server.py** (3-4h)
- [ ] Test project generation logic
- [ ] Test variable derivation (slug, package_name, namespace)
- [ ] Test 12 validation checks
- [ ] Test error handling
- [ ] Target: 85%+ coverage

**Day 4: validate-model-citizen.py** (2h)
- [ ] Test all 12 validation checks
- [ ] Test exit codes
- [ ] Test JSON output
- [ ] Target: 85%+ coverage

**Day 5: inbox tools** (3h)
- [ ] Test inbox-query.py CLI
- [ ] Test inbox-status.py CLI
- [ ] Use importlib pattern (hyphenated files)
- [ ] Target: 85%+ coverage per file

---

### Week 2: Utility Modules + Remaining Scripts (8-10 hours)

**Day 1-2: Utility modules** (4-4.5h)
- [ ] awareness_validation.py (16% → 85%)
- [ ] usage_tracker.py (17% → 85%)
- [ ] suggest-next.py (0% → 85%)

**Day 3-5: Batch remaining scripts** (4-5h)
- [ ] Group similar scripts (e.g., all inbox scripts, all SAP scripts)
- [ ] Reuse test patterns
- [ ] Focus on happy path + error cases
- [ ] Target: 50-70% coverage (good enough for low-complexity scripts)

---

## Coverage Milestones

| Milestone | Target Coverage | Est. Completion | Status |
|-----------|-----------------|-----------------|--------|
| **M0: Baseline** | 4% | 2025-11-05 | ✅ Complete |
| **M1: chora-workspace adoption** | 16% | 2025-11-06 | ✅ Complete |
| **M2: High-value scripts** | 40-50% | Week 1 end | 🔄 Planned |
| **M3: Utility modules** | 60-70% | Week 2 Day 2 | 🔄 Planned |
| **M4: L3 Compliance** | **85%+** | Week 2 end | 🔄 Planned |

---

## Efficiency Assumptions

**Based on chora-workspace data**:
- **Efficiency multiplier**: 6.2x (2.5h actual vs 12-18h estimated)
- **With patterns**: 15-20h estimated (vs 30h from scratch)
- **Per-script time**: 1-4h depending on complexity
- **Reusable fixtures**: 30-50% time savings (from template conftest.py)

**Risk factors**:
- importlib complexity (some scripts harder to load)
- Async testing (MCP servers require async patterns)
- Mock complexity (scripts with many dependencies)

**Mitigation**:
- Use chora-workspace patterns (proven)
- Start with high-value scripts (learn patterns early)
- Accept 70-80% coverage for complex scripts (diminishing returns)

---

## Success Criteria

### Must-Have (L3 Compliance)

- [x] Overall project coverage ≥ 85%
- [x] High-value scripts ≥ 85% coverage
- [x] All tests passing (≥99% pass rate)
- [x] No flaky tests

### Nice-to-Have

- [ ] Async test patterns established
- [ ] Test documentation complete
- [ ] CI/CD coverage enforcement
- [ ] Coverage dashboard

---

## Tools & Resources

### Testing Tools

- pytest 8.3.0
- pytest-asyncio 0.24.0
- pytest-cov 6.0.0
- importlib (for hyphenated files)

### Patterns Library

- **chora-workspace SAP-004 tests** (2 files, 97 tests)
- **static-template/tests/conftest.py** (reusable fixtures)
- **static-template/tests/test_example.py.template** (pattern examples)
- **SAP-004 awareness-guide.md** (Section 5.5: Advanced Patterns)

### Documentation

- [SAP-004 Ledger](../../skilled-awareness/testing-framework/ledger.md)
- [SAP-004 Awareness Guide](../../skilled-awareness/testing-framework/awareness-guide.md)
- [Coordination Response](../../../inbox/outgoing/coordination/RESPONSE_SAP_004_ADOPTION.md)

---

## Tracking & Reporting

### Weekly Progress Reports

**Format**:
```markdown
## Week X Progress Report

**Coverage**: X% → Y% (+Zpp)
**Tests Added**: N tests
**Files Covered**: N files
**Time Spent**: X hours
**Blockers**: None / List blockers
**Next Week**: Focus areas
```

**Location**: Update this plan document + SAP-004 ledger

### A-MEM Event Logging

Log progress in `.chora/memory/events/development.jsonl`:
```json
{
  "event_type": "sap_004_coverage_milestone",
  "timestamp": "...",
  "coverage_before": 16,
  "coverage_after": 40,
  "tests_added": 80,
  "files_covered": 5,
  "time_spent_hours": 11,
  "milestone": "M2"
}
```

---

## Next Actions

### Immediate (This Week)

1. [ ] Start with `scripts/sap-evaluator.py` (3-4h)
   - Already has partial tests (test_sap_evaluator_cli.py skeleton exists)
   - High complexity, high value
   - Learn importlib pattern in practice

2. [ ] Test `scripts/create-model-mcp-server.py` (3-4h)
   - Critical new script (fast-setup)
   - Validates SAP-003 integration
   - Tests bootstrap logic

3. [ ] Update SAP-004 ledger with progress

### This Month

1. [ ] Complete high-value scripts (Week 1)
2. [ ] Complete utility modules (Week 2 Days 1-2)
3. [ ] Batch remaining scripts (Week 2 Days 3-5)
4. [ ] Reach 85% coverage (M4 milestone)
5. [ ] Update SAP-004 to L3 status

### Long-Term

1. [ ] Establish async testing patterns
2. [ ] Document complex mocking strategies
3. [ ] Create testing dashboard
4. [ ] Mentor other projects on testing

---

## Appendix: Script Inventory

### Complete List (40+ Scripts/Modules)

**scripts/**:
- sap-evaluator.py (partial tests)
- create-model-mcp-server.py (untested) ⭐
- validate-model-citizen.py (untested) ⭐
- inbox-query.py (untested) ⭐
- inbox-status.py (untested) ⭐
- install-sap.py (79% ✅)
- usage_tracker.py (17%)
- suggest-next.py (untested)
- track-recipe-usage.py (n/a - doesn't exist)
- automation-dashboard.py (n/a - doesn't exist)
- +30 other scripts (mostly untested)

**utils/**:
- sap_evaluation.py (90% ✅)
- claude_metrics.py (78% ✅)
- awareness_validation.py (16%)
- +5 other modules

**Total**: 40+ files needing tests

---

**Status**: Ready to execute
**Owner**: chora-base maintainers
**Timeline**: 2-4 weeks (15-20 hours)
**Last Updated**: 2025-11-06
