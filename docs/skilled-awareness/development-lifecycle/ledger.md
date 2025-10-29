---
sap_id: SAP-012
version: 1.0.0
status: Draft
last_updated: 2025-10-28
---

# Ledger: Development Lifecycle Adoption

**SAP ID**: SAP-012
**Capability**: development-lifecycle
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Adoption Overview

### Coverage Statistics

| Metric | Count | Target | Status |
|--------|-------|--------|--------|
| **Total Projects** | 0 | 10 | 🔴 0% |
| **Level 1 Adopters** (Development only) | 0 | 5 | 🔴 0% |
| **Level 2 Adopters** (+ Planning) | 0 | 3 | 🔴 0% |
| **Level 3 Adopters** (All 8 phases) | 0 | 2 | 🔴 0% |
| **DDD Adoption** | 0% | 80% | 🔴 Not Started |
| **BDD Adoption** | 0% | 60% | 🔴 Not Started |
| **TDD Adoption** | 0% | 70% | 🔴 Not Started |

**Status Legend**:
- 🟢 ≥80% (Excellent)
- 🟡 60-79% (Good)
- 🟠 40-59% (Fair)
- 🔴 <40% (Needs Improvement)

---

## 2. Adopter Registry

### Level 1: Development Focus (DDD→BDD→TDD)

#### chora-base (Self-Adoption)
- **Status**: 🔄 In Progress (Phase 3 Batch 2)
- **Version**: SAP-012 v1.0.0
- **Adoption Date**: 2025-10-28 (SAP created)
- **Level**: Level 1 (planning to Level 3)
- **Adopter Type**: Template repository (dogfooding)
- **Components**:
  - ✅ Workflow docs (6 files, 5,285 lines)
  - ✅ Templates (sprint, release, metrics)
  - ⏳ Full DDD→BDD→TDD adoption (in progress)
- **Metrics**:
  - Defects per release: Target <3 (baseline TBD)
  - Test coverage: 95%+ (already high)
  - Process adherence: TBD (start tracking in Sprint 1)
- **Notes**: chora-base is using this SAP to document its own development process
- **Contact**: Victor (victorpiper)

---

### Level 2: Planning + Development

_(No adopters yet)_

**Target Adopters**:
- chora-compose (MCP server)
- mcp-n8n (MCP gateway)
- Example projects in `examples/`

---

### Level 3: Full Lifecycle (All 8 Phases)

_(No adopters yet)_

**Target Adopters**:
- chora-base (upgrade from Level 1 after 2-3 sprints)
- Future chora-* ecosystem projects

---

## 3. Adoption Metrics by Project

### chora-base

**Adoption Timeline**:
- 2025-10-28: SAP-012 created (Protocol, Awareness, Adoption, Ledger)
- 2025-10-28: Level 1 adoption started (DDD→BDD→TDD workflow)
- TBD: Level 2 adoption (sprint planning)
- TBD: Level 3 adoption (full lifecycle)

**Quality Metrics** (baseline TBD):

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Defects per release | TBD | TBD | <3 | 🔴 Not tracking yet |
| Test coverage | 95% | 95% | ≥85% | 🟢 Excellent |
| Code review time | TBD | TBD | <24h | 🔴 Not tracking yet |
| Rework rate | TBD | TBD | <20% | 🔴 Not tracking yet |

**Velocity Metrics** (TBD after Sprint 1-2):

| Metric | Sprint 1 | Sprint 2 | Sprint 3 | Trend |
|--------|----------|----------|----------|-------|
| Story points committed | TBD | TBD | TBD | - |
| Story points delivered | TBD | TBD | TBD | - |
| Planned vs delivered | TBD | TBD | TBD | Target ≥70% |

**Process Adherence Metrics** (TBD):

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| DDD adoption (% features with docs-first) | 0% | 80% | 🔴 Not started |
| BDD adoption (% features with .feature files) | 0% | 60% | 🔴 Not started |
| TDD adoption (% code written test-first) | Unknown | 70% | 🔴 Not measured |
| Sprint adherence (% on-time completion) | N/A | 70% | 🔴 No sprints yet |

**Notes**:
- chora-base currently has workflow docs but not consistently following DDD→BDD→TDD
- SAP-012 formalizes the process, tracking adoption starting now
- Baseline metrics will be established in first sprint after SAP-012 adoption

---

## 4. Version History

### v1.0.0 (2025-10-28) - Initial Release

**Changes**:
- ✅ Created SAP-012 (5 artifacts)
- ✅ Documented 8-phase lifecycle
- ✅ Integrated DDD→BDD→TDD workflows
- ✅ Created templates (sprint, release, metrics)

**Artifacts**:
- [capability-charter.md](capability-charter.md) - Problem, solution, success criteria
- [protocol-spec.md](protocol-spec.md) - 8-phase contracts, DDD→BDD→TDD integration
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt lifecycle
- [ledger.md](ledger.md) - This document

**Adopters**: 0 (chora-base in progress)

---

## 5. Feedback & Learnings

### Sprint 1 Learnings (TBD)

**What Went Well**:
- TBD after first sprint

**What Could Improve**:
- TBD after first sprint

**Action Items**:
- TBD after first sprint

---

### Common Adoption Challenges (Future)

_(Document patterns as projects adopt)_

**Challenge 1**: [TBD based on pilot feedback]
**Solution**: [TBD]

**Challenge 2**: [TBD]
**Solution**: [TBD]

---

## 6. Research Evidence & ROI

### Expected ROI (Research-Backed)

**Sources**:
- "Test Driven Development: By Example" (Kent Beck, 2002)
- "The Cucumber Book" (Matt Wynne, Aslak Hellesøy, 2017)
- "Docs as Code" (Anne Gentle, 2017)

**Expected Outcomes**:

| Metric | Baseline | Target (3 months) | Evidence |
|--------|----------|-------------------|----------|
| **Defect Reduction** | Varies | 40-80% reduction | Kent Beck (TDD) |
| **Rework Reduction** | Varies | 40-60% reduction | Anne Gentle (DDD) |
| **Requirement Ambiguity** | Varies | 60% reduction | Wynne & Hellesøy (BDD) |
| **API Churn** | Varies | 50% reduction | Anne Gentle (DDD) |
| **Test Coverage** | Varies | ≥85% | Industry best practice |

---

### Actual ROI (Measured After Adoption)

_(Update after 3-6 months of adoption)_

**chora-base Results** (TBD):
- Defect reduction: TBD
- Rework reduction: TBD
- Time to implement feature: TBD (before vs after)
- Developer satisfaction: TBD (survey)

---

## 7. Upgrade Path

### From v1.0.0 to Future Versions

**Breaking Changes** (MAJOR version):
- Will require migration guide
- Announced 3 months in advance

**New Features** (MINOR version):
- Backward compatible
- Optional adoption

**Bug Fixes** (PATCH version):
- Transparent updates to workflow docs

---

## 8. Maintenance Notes

### Document Updates

**Last Review**: 2025-10-28 (initial creation)
**Next Review**: 2025-11-28 (1 month after Sprint 1 starts)
**Review Frequency**: Monthly (first 3 months), then quarterly

### Metrics Update Schedule

**Frequency**: After each sprint (biweekly)
**Owner**: Release manager or project maintainer
**Process**:
1. Update project metrics tables
2. Document learnings in Section 5
3. Update adoption statistics in Section 1

---

## 9. Related Documents

**SAP Artifacts**:
- [capability-charter.md](capability-charter.md) - Problem and solution overview
- [protocol-spec.md](protocol-spec.md) - Technical contracts for 8 phases
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt

**Workflow Docs**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - 8-phase lifecycle overview (1,108 lines)
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD→BDD→TDD integration (753 lines)
- [DDD_WORKFLOW.md](/static-template/dev-docs/workflows/DDD_WORKFLOW.md) - Documentation Driven Design (919 lines)
- [BDD_WORKFLOW.md](/static-template/dev-docs/workflows/BDD_WORKFLOW.md) - Behavior Driven Development (1,148 lines)
- [TDD_WORKFLOW.md](/static-template/dev-docs/workflows/TDD_WORKFLOW.md) - Test Driven Development (1,187 lines)
- [ANTI_PATTERNS.md](/static-template/dev-docs/ANTI_PATTERNS.md) - Common mistakes (1,309 lines)

**Templates**:
- [sprint-template.md](/static-template/project-docs/sprints/sprint-template.md) - Sprint planning template
- [release-template.md](/static-template/project-docs/releases/release-template.md) - Release planning template
- [PROCESS_METRICS.md](/static-template/project-docs/metrics/PROCESS_METRICS.md) - Metrics dashboard

**Related SAPs**:
- [SAP-000: sap-framework](../sap-framework/) - Meta SAP framework
- [SAP-004: testing-framework](../testing-framework/) - pytest, coverage, fixtures
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - CI/CD automation
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit hooks
- [SAP-007: documentation-framework](../documentation-framework/) - Diataxis structure
- [SAP-008: automation-scripts](../automation-scripts/) - Automation scripts
- [SAP-013: metrics-tracking](../metrics-tracking/) - ClaudeROICalculator

---

**Changelog**:
- **2025-10-28**: Initial ledger created for SAP-012 v1.0.0
- **TBD**: First metrics update after Sprint 1
- **TBD**: Quarterly review and process improvements

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger for development-lifecycle SAP
