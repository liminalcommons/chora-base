---
sap_id: SAP-012
version: 1.0.0
status: Draft
last_updated: 2025-10-28
scope: All (Vision & Strategy, Planning, Implementation)
---

# Capability Charter: Development Lifecycle

**SAP ID**: SAP-012
**Capability Name**: development-lifecycle
**Version**: 1.0.0
**Status**: Draft (Phase 3)

---

## 1. Problem Statement

### Current State

chora-base includes comprehensive development workflow documentation (5,285 lines across 6 files) covering the 8-phase lifecycle and DDD→BDD→TDD integration, but **lacks a single authoritative SAP** that:

1. **Defines the contracts** for each phase (inputs, outputs, duration, participants)
2. **Documents the integration** between DDD, BDD, and TDD methodologies
3. **Provides templates** for sprint planning, release planning, and process metrics
4. **Establishes quality gates** between phases
5. **Tracks adoption** of the lifecycle across projects

### User Pain Points

**From previous session context**:
- "No single source of truth for DDD→BDD→TDD workflow"
- Developers unsure when to use DDD vs BDD vs TDD
- Inconsistent phase execution across teams
- Unclear time scales and ROI expectations
- Process metrics undefined or not tracked

### Impact

**Without this SAP**:
- ❌ Teams deviate from proven workflow (40-80% defect reduction benefit lost)
- ❌ Onboarding developers spend days learning fragmented docs
- ❌ Process improvements not systematically captured
- ❌ No visibility into lifecycle adoption rates

**With this SAP**:
- ✅ Single source of truth for 8-phase lifecycle
- ✅ Clear contracts for each phase (inputs → activities → outputs)
- ✅ Templates reduce planning overhead by 50%
- ✅ Process metrics track adherence and quality

---

## 2. Proposed Solution

A **comprehensive SAP defining the 8-phase development lifecycle** (Vision → Planning → Requirements → Development → Testing → Review → Release → Monitoring) with DDD→BDD→TDD integration.

**Key Principles**:
1. **8-Phase Lifecycle** - Vision/Strategy (months) → Monitoring/Feedback (continuous)
2. **DDD→BDD→TDD Integration** - Documentation → Behavior → Tests → Implementation
3. **Time-Boxed Phases** - Clear duration expectations (minutes to months)
4. **Template-Based Planning** - Sprint templates, release templates, metrics dashboards
5. **Measurable Process Metrics** - Quality, velocity, adherence tracking

**Scope**: All three SAP levels
- **Vision & Strategy**: Long-term roadmap, ecosystem alignment (ROADMAP.md)
- **Planning**: Sprint planning templates, release planning guides
- **Implementation**: DDD, BDD, TDD workflows with code examples

---

## 3. Capability Definition

### What This SAP Includes

**Workflow Documentation** (6 files, 5,285 lines):
1. **DEVELOPMENT_PROCESS.md** (1,108 lines) - 8-phase lifecycle overview
2. **DEVELOPMENT_LIFECYCLE.md** (753 lines) - DDD→BDD→TDD integration
3. **DDD_WORKFLOW.md** (919 lines) - Documentation Driven Design
4. **BDD_WORKFLOW.md** (1,148 lines) - Behavior Driven Development
5. **TDD_WORKFLOW.md** (1,187 lines) - Test Driven Development
6. **workflows/README.md** (170 lines) - Workflow index

**Templates** (9 files):
- Sprint planning: `project-docs/sprints/sprint-template.md`, `README.md`
- Release planning: `project-docs/releases/release-template.md`, `upgrade-guide-template.md`, `RELEASE_PLANNING_GUIDE.md`, `upgrade-philosophy.md`, `README.md`
- Process metrics: `project-docs/metrics/PROCESS_METRICS.md`
- Project docs index: `project-docs/README.md`

**Anti-Patterns** (1 file):
- **dev-docs/ANTI_PATTERNS.md** (1,309 lines) - Common mistakes and how to avoid them

### What This SAP Excludes

- Testing infrastructure (covered by SAP-004: testing-framework)
- CI/CD pipelines (covered by SAP-005: ci-cd-workflows)
- Automation scripts (covered by SAP-008: automation-scripts)
- Documentation structure (covered by SAP-007: documentation-framework)

---

## 4. Success Criteria

### Adoption Metrics

**Target**: 80% of chora-base adopters follow 8-phase lifecycle

**Measurement**:
- Presence of `project-docs/sprints/` and `project-docs/releases/` (template adoption)
- PROCESS_METRICS.md populated with actuals
- DDD→BDD→TDD adherence tracked in sprint retrospectives

### Quality Metrics

**Target**: 40-80% defect reduction (research-backed)

**Measurement**:
- Defects per release: <3 (current target from PROCESS_METRICS.md)
- Test coverage: ≥85%
- Process adherence: ≥70% (sprint velocity ratio)

### Efficiency Metrics

**Target**: 50% reduction in planning overhead

**Measurement**:
- Sprint planning time: <2 hours (vs 4+ hours without templates)
- Release planning time: <4 hours (vs 8+ hours without templates)

---

## 5. Dependencies

### Upstream Dependencies

- **SAP-000** (sap-framework): Provides SAP structure and governance
- **SAP-007** (documentation-framework): Diataxis structure referenced in DDD workflow

### Downstream Dependencies

- **SAP-008** (automation-scripts): Scripts support lifecycle phases (pre-merge, release)
- **SAP-013** (metrics-tracking): ClaudeROICalculator tracks process efficiency

### Cross-References

- **DEVELOPMENT_PROCESS.md** references all 8 phases
- **DEVELOPMENT_LIFECYCLE.md** integrates DDD/BDD/TDD
- **Templates** reference workflow docs for guidance

---

## 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Complexity**: 8 phases overwhelming for small teams | Medium | Provide "Quick Start" for simple features (skip Phase 1-2) |
| **Adoption friction**: Teams resist process change | High | Demonstrate 40-80% defect reduction ROI in adoption-blueprint |
| **Template maintenance**: Templates diverge from practice | Medium | Ledger tracks template versions, changelog documents updates |
| **Over-engineering**: Process slows down simple tasks | Medium | Decision trees in DEVELOPMENT_LIFECYCLE.md guide "when to skip" |

---

## 7. Open Questions

1. **Sprint duration**: 1-week vs 2-week sprints? (Currently: 2 weeks assumed)
2. **BDD tooling**: pytest-bdd vs behave? (Currently: pytest-bdd assumed)
3. **Metrics automation**: Manual tracking vs automated dashboard? (Phase 4: SAP-013)

---

## 8. Related Capabilities

- **SAP-000** (sap-framework): Meta-framework for all SAPs
- **SAP-004** (testing-framework): pytest, coverage, fixtures used in TDD/BDD
- **SAP-005** (ci-cd-workflows): CI/CD executes test suites from phases 5-6
- **SAP-006** (quality-gates): Pre-commit hooks enforce quality in Phase 4
- **SAP-007** (documentation-framework): Diataxis used in DDD (Phase 3)
- **SAP-008** (automation-scripts): Scripts automate phase transitions
- **SAP-013** (metrics-tracking): ClaudeROICalculator tracks process ROI

---

## 9. Approval & Sign-Off

**Charter Author**: Claude Code
**Date**: 2025-10-28
**Status**: Draft - Ready for Protocol Spec

**Approved By**: _(Pending Victor review)_

---

**Next Steps**:
1. Create [protocol-spec.md](protocol-spec.md) - Define 8-phase contracts, DDD→BDD→TDD integration
2. Create [awareness-guide.md](awareness-guide.md) - Agent workflows for lifecycle execution
3. Create [adoption-blueprint.md](adoption-blueprint.md) - How to adopt lifecycle in projects
4. Create [ledger.md](ledger.md) - Track adopter metrics and versions
