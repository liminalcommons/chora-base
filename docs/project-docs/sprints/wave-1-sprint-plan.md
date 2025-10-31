# Wave 1 Sprint Plan: Documentation Architecture Unification

**Sprint ID**: WAVE-1
**Version**: v3.4.0
**Sprint Goal**: Restructure docs/ to universal 4-domain architecture
**Duration**: 1-2 weeks
**Estimated Effort**: 40-60 hours
**Start Date**: 2025-10-28
**Target Completion**: 2025-11-11

---

## Sprint Goal

Transform chora-base documentation from mixed structure to universal 4-domain architecture, enabling:
- Clear separation of concerns (dev/project/user/skilled-awareness)
- Consistent structure with static-template/
- Foundation for Wave 2-7 transformations
- Meta-demonstration of chora-base framework

---

## Success Criteria

✅ All files moved to correct domains (no content lost)
✅ No broken links (100% validation pass)
✅ All domain README.md files created
✅ SAP-000 added to static-template/
✅ ARCHITECTURE.md created explaining 4-domain model
✅ Cleanup manifest updated with Wave 1 items
✅ 100% coherence maintained (validated by inventory)

---

## Committed Work Items

### High Priority (Must Complete)

#### 1. Directory Structure Creation
**Estimate**: 1 hour
**Status**: Not Started

Create missing directories:
- docs/dev-docs/{workflows,examples,vision,research}
- docs/project-docs/{sprints,releases,metrics,integration,inventory}
- docs/user-docs/{how-to,explanation,reference,tutorials}
- docs/skilled-awareness/ (move from reference/)

#### 2. File Migrations
**Estimate**: 4 hours
**Status**: Not Started

**To dev-docs/research/**: (3 files)
- adopter-learnings-mcp-orchestration.md
- adopter-learnings-executable-docs.md
- CLAUDE_Complete.md

**To project-docs/**: (4 directories + 1 file)
- DOCUMENTATION_PLAN.md
- integration/ directory
- inventory/ directory
- releases/ directory

**To user-docs/**: (6 files)
- BENEFITS.md → explanation/benefits-of-chora-base.md
- reference/writing-executable-howtos.md → how-to/write-executable-documentation.md
- reference/ecosystem/multi-repo-capability-evolution-to-w3.md → explanation/
- reference/ecosystem/ARCHITECTURE_CLARIFICATION.md → explanation/
- reference/ecosystem/how-to-setup-mcp-ecosystem.md → how-to/

**Skilled-awareness relocation**: (1 directory)
- reference/skilled-awareness/ → skilled-awareness/

#### 3. Domain README Files
**Estimate**: 3 hours
**Status**: Not Started

Create 4 README.md files:
- docs/dev-docs/README.md
- docs/project-docs/README.md
- docs/user-docs/README.md
- docs/skilled-awareness/README.md

Each explains domain purpose, structure, audience, and cross-links.

#### 4. ARCHITECTURE.md
**Estimate**: 4 hours
**Status**: Not Started

Root-level docs/ARCHITECTURE.md explaining:
- The 4-domain model
- Diátaxis mapping
- Decision trees for content placement
- Visual structure diagram
- Examples and rationale

#### 5. Cross-Reference Updates
**Estimate**: 8-12 hours
**Status**: Not Started

Update all references in:
- All 14 SAP awareness-guides (reference moved files)
- docs/skilled-awareness/INDEX.md (new paths)
- Root README.md (new docs structure)
- Root AGENTS.md (new documentation locations)
- All files that link to moved documentation

#### 6. Add SAP-000 to static-template
**Estimate**: 2 hours
**Status**: Not Started

Copy to static-template/:
- skilled-awareness/sap-framework/
- skilled-awareness/document-templates.md
- skilled-awareness/INDEX.md (starter template)
- SKILLED_AWARENESS_PACKAGE_PROTOCOL.md (root)

#### 7. Validation
**Estimate**: 2 hours
**Status**: Not Started

Run:
- Inventory script: Verify 100% coherence
- Link checker: Ensure no broken references
- SAP validator: Verify all SAP references valid

#### 8. Cleanup Manifest Update
**Estimate**: 1 hour
**Status**: Not Started

Update v4-cleanup-manifest.md:
- Files to Delete: Old conversation logs, empty directories
- Files to Archive: TBD during execution
- Files to Move: Mark migrations as DONE
- References to Update: Mark as DONE
- Git History: Note any concerns

### Medium Priority (Should Complete)

#### 9. Meta-Documentation
**Estimate**: 6 hours
**Status**: Not Started

**Documentation Migration Workflow**:
- Create dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md
- Reusable pattern for future migrations
- Checklist, validation steps, anti-patterns

**Wave 1 Execution Metrics**:
- Create project-docs/metrics/wave-1-execution-metrics.md
- Track: Files moved, time spent, validation results
- Compare estimates vs. actuals

**Wave 1 Release Notes**:
- Create project-docs/releases/v3.4.0-wave-1-release-notes.md
- Document changes, benefits, migration impact

### Low Priority (Nice to Have)

#### 10. Enhanced Documentation
**Estimate**: 4 hours
**Status**: Not Started (Deferred if time constrained)

- Visual diagram of 4-domain architecture
- Migration guide for external adopters
- FAQ about new structure

---

## Time Budget

**Available Capacity**: 60 hours (1.5 weeks × 40 hours/week)
**Commitment**: 48 hours (80% of capacity)
**Buffer**: 12 hours (20% for unknowns)

**Breakdown**:
- High Priority (Must Complete): 25-35 hours
- Medium Priority (Should Complete): 12 hours
- Low Priority (Nice to Have): 4 hours (deferred if needed)
- Buffer: 12 hours

**Target Velocity**: Deliver 100% of High Priority + 100% of Medium Priority

---

## Risks & Mitigations

### Risk 1: Broken References
**Probability**: Medium
**Impact**: High
**Mitigation**:
- Update cross-references immediately after each move
- Run link checker continuously during development
- Keep reference table of old → new paths

### Risk 2: Missed Files
**Probability**: Low
**Impact**: Medium
**Mitigation**:
- Run inventory before and after
- Use systematic migration checklist
- Validate 100% coherence maintained

### Risk 3: Scope Creep
**Probability**: Medium
**Impact**: Medium
**Mitigation**:
- Defer Low Priority items if time constrained
- Focus on structural changes, not content improvements
- Save enhancements for Wave 2

### Risk 4: SAP Reference Complexity
**Probability**: Medium
**Impact**: Medium
**Mitigation**:
- Create reference table before starting
- Update SAPs systematically (one at a time)
- Validate each SAP after updating

---

## Dependencies

**Blockers**: None
**Prerequisites**:
- ✅ v4-cleanup-manifest.md created
- ✅ CHORA-BASE-4.0-VISION.md finalized
- ✅ 100% coherence achieved in v3.3.0

**Dependent Work**:
- Wave 2 (SAP Content Audit) depends on Wave 1 completion
- All future waves depend on 4-domain structure

---

## Daily Standup Questions

### What did I complete yesterday?
- Track completed work items
- Update todo list

### What am I working on today?
- Current work item from plan
- Any blockers encountered

### Any impediments?
- Broken links discovered
- Unexpected complexity
- Scope clarifications needed

---

## Definition of Done

For this sprint to be complete:

- [ ] All High Priority items: DONE
- [ ] All Medium Priority items: DONE (or explicitly deferred with reason)
- [ ] All validation scripts: PASS
- [ ] Cleanup manifest: UPDATED
- [ ] Git commit: COMPLETE
- [ ] Velocity tracked: MEASURED
- [ ] No broken links: VALIDATED
- [ ] 100% coherence: MAINTAINED

---

## Process Adherence

**Target**: ≥90% workflow compliance

**Workflows being followed**:
- ✅ DDD (Documentation Driven Design) - Sprint plan before execution
- ✅ BDD (Behavior Driven Development) - Success criteria define behavior
- ✅ Incremental commits - Atomic changes, validated at each step
- ✅ Continuous validation - Test as we go
- ✅ Retrospective - Metrics and learnings captured

**Process Metrics to Track**:
- Time: Estimated vs. Actual (per work item)
- Quality: Validation pass rate
- Efficiency: Files moved per hour
- Adherence: % of workflow steps followed

---

## Sprint Retrospective (To Complete at End)

### What Went Well?
- [To be filled during execution]

### What Could Be Improved?
- [To be filled during execution]

### Action Items for Wave 2?
- [To be filled during execution]

### Velocity Calculation
- Committed: 48 hours
- Completed: [TBD] hours
- Velocity: [TBD]% (Target: 80-90%)

---

**Sprint Plan Version**: 1.0
**Created**: 2025-10-28
**Owner**: Claude (chora-base development)
**Status**: ACTIVE

This sprint plan demonstrates chora-base's project-docs/ domain in action.
