# Wave 2 Sprint Plan: SAP Content Audit & Enhancement

**Sprint ID**: WAVE-2
**Version**: v3.5.0
**Sprint Goal**: Ensure all 14 SAPs properly reference 4-domain structure and have complete, actionable content
**Duration**: 2-3 weeks
**Estimated Effort**: 80-120 hours
**Start Date**: 2025-10-28
**Target Completion**: 2025-11-18

---

## Sprint Goal

Audit and enhance all 14 SAPs to ensure:
- Each SAP references actual implementation files across 4 domains
- All awareness-guides have explicit cross-domain references
- No broken links (validated automatically)
- Content is complete and actionable
- Foundation ready for Wave 3 (MCP-specific extraction)

---

## Success Criteria

### Quantitative
✅ All 14 SAPs audited (100%)
✅ SAP-016 (Link Validation) created and operational
✅ No broken links in any SAP (automated validation)
✅ 100% coherence maintained (inventory validation)
✅ Each SAP references 2-3+ domains on average
✅ 90%+ of critical gaps filled

### Qualitative
✅ Every SAP has clear, actionable content
✅ Cross-domain references are explicit and validated
✅ Awareness-guides reference actual files (not hypothetical)
✅ Examples are concrete and tested
✅ Meta-dogfooding demonstrated

### Meta-Goals
✅ Wave 2 tracked in project-docs/sprints/
✅ SAP audit workflow created in dev-docs/workflows/
✅ User guides enhanced in user-docs/
✅ SAPs improved in skilled-awareness/

---

## Committed Work Items

### High Priority (Must Complete)

#### Priority 1: Foundation & Tooling

**1.1 Create SAP-016: Link Validation & Reference Management**
- **Estimate**: 12-16 hours
- **Status**: Not Started
- **Deliverables**:
  - 5 SAP artifacts (charter, protocol, awareness-guide, blueprint, ledger)
  - `scripts/validate-links.sh` - Automated link checker
  - Test on Wave 1 documentation
  - Integration with validation workflow

**1.2 Create SAP Audit Workflow**
- **Estimate**: 4-6 hours
- **Status**: Not Started
- **Deliverable**: `docs/dev-docs/workflows/SAP_AUDIT_WORKFLOW.md`
- **Purpose**: Systematic process for auditing any SAP

**1.3 Create Wave 2 Sprint Plan**
- **Estimate**: 2-3 hours
- **Status**: In Progress
- **Deliverable**: This document

#### Priority 2: Tier 1 SAP Audit (High Impact)

**2.1 Audit SAP-000 (SAP Framework)**
- **Estimate**: 6 hours
- **Status**: Not Started
- **Rationale**: Meta-level, affects all other SAPs
- **Focus**: SAP creation patterns, opportunity identification

**2.2 Audit SAP-007 (Documentation Framework)**
- **Estimate**: 5 hours
- **Status**: Not Started
- **Rationale**: Just restructured in Wave 1, fresh context
- **Focus**: 4-domain integration, classification guides

**2.3 Audit SAP-002 (Chora-Base)**
- **Estimate**: 6 hours
- **Status**: Not Started
- **Rationale**: Core project SAP, high visibility
- **Focus**: Project overview, getting started guides

**2.4 Audit SAP-004 (Testing Framework)**
- **Estimate**: 4 hours
- **Status**: Not Started
- **Rationale**: Well-established, good example to follow
- **Focus**: TDD workflow references, test examples

#### Priority 3: Tier 2 SAP Audit (Medium Impact)

**3.1 Audit SAP-001 (Inbox Protocol)**
- **Estimate**: 6 hours
- **Status**: Not Started
- **Rationale**: Complex, needs concrete examples
- **Focus**: Coordination examples, triage workflows

**3.2 Audit SAP-012 (Development Lifecycle)**
- **Estimate**: 5 hours
- **Status**: Not Started
- **Rationale**: DDD/BDD/TDD integration
- **Focus**: Workflow connections, phase transitions

**3.3 Audit SAP-008 (Automation Scripts)**
- **Estimate**: 4 hours
- **Status**: Not Started
- **Rationale**: Many tools, needs catalog
- **Focus**: Script inventory, usage examples

#### Priority 4: Tier 3 SAP Audit (Complete Coverage)

**4.1 Audit Remaining 7 SAPs**
- **Estimate**: 24 hours (7 SAPs × 3-4h each)
- **Status**: Not Started
- **SAPs**: SAP-003, SAP-005, SAP-006, SAP-009, SAP-010, SAP-011, SAP-013
- **Approach**: Batch similar SAPs together

### Medium Priority (Should Complete)

#### Priority 5: Content Creation

**5.1 Create Missing dev-docs/ Content**
- **Estimate**: 10-15 hours
- **Status**: Not Started (gaps identified during audit)
- **Expected**:
  - 5-7 workflow documents
  - 3-5 example walkthroughs

**5.2 Create Missing user-docs/ Content**
- **Estimate**: 8-12 hours
- **Status**: Not Started (gaps identified during audit)
- **Expected**:
  - 4-6 how-to guides
  - 2-3 explanation documents
  - 3-5 reference specs

**5.3 Create Missing project-docs/ Content**
- **Estimate**: 4-6 hours
- **Status**: Not Started (gaps identified during audit)
- **Expected**:
  - 2-3 metric templates
  - Integration plan examples

#### Priority 6: Validation & Release

**6.1 Comprehensive Validation**
- **Estimate**: 6-8 hours
- **Status**: Not Started
- **Tasks**:
  - Run link checker on all SAPs
  - Run inventory validation
  - Manual quality spot-checks

**6.2 Wave 2 Documentation**
- **Estimate**: 6-8 hours
- **Status**: Not Started
- **Deliverables**:
  - wave-2-execution-metrics.md
  - wave-2-sap-opportunities.md
  - v3.5.0-wave-2-release-notes.md

### Low Priority (Nice to Have)

**7.1 Enhanced Examples**
- **Estimate**: 6-8 hours
- **Status**: Deferred if time-constrained
- **Purpose**: Polish, additional walkthroughs

**7.2 SAP Visualization**
- **Estimate**: 4-6 hours
- **Status**: Deferred if time-constrained
- **Purpose**: Dependency graphs, architecture diagrams

---

## Time Budget

**Available Capacity**: 120 hours (3 weeks × 40 hours/week)
**Commitment**: 96 hours (80% of capacity)
**Buffer**: 24 hours (20% for unknowns)

**Breakdown**:
- Priority 1 (Foundation): 18-25 hours
- Priority 2 (Tier 1 Audit): 21 hours
- Priority 3 (Tier 2 Audit): 15 hours
- Priority 4 (Tier 3 Audit): 24 hours
- Priority 5 (Content Creation): 22-33 hours
- Priority 6 (Validation & Release): 12-16 hours
- **Total Committed**: 112-134 hours

**Note**: If high end (134h) is needed, we'll defer Low Priority items or extend timeline.

**Target Velocity**: Deliver 100% of High + Medium Priority items

---

## Execution Strategy

### Phase-Based Approach

**Phase 1: Foundation (Days 1-3)**
- Create SAP-016 (link validation)
- Create SAP audit workflow
- Set up tracking

**Phase 2: Tier 1 Audit (Days 4-7)**
- 4 high-impact SAPs
- Establish audit pattern
- Identify gap types

**Phase 3: Tier 2 Audit (Days 8-11)**
- 3 medium-impact SAPs
- Refine audit process
- Continue gap tracking

**Phase 4: Tier 3 Audit (Days 12-15)**
- Remaining 7 SAPs
- Batch similar SAPs
- Complete gap analysis

**Phase 5: Content Creation (Days 16-18)**
- Fill critical gaps
- Fill high-value gaps
- Document nice-to-haves for future

**Phase 6: Validation & Release (Days 19-21)**
- Comprehensive validation
- Metrics and documentation
- Git commit

### Per-SAP Audit Pattern

**Standard Workflow** (3-6 hours per SAP):

1. **Read & Analyze** (1h)
   - Read all 5 artifacts
   - Map existing references
   - Note claims vs reality

2. **4-Domain Gap Analysis** (1h)
   - Check dev-docs/ → Exists?
   - Check project-docs/ → Exists?
   - Check user-docs/ → Exists?
   - Check system files → Valid paths?

3. **Run Link Checker** (0.5h)
   - `./scripts/validate-links.sh docs/skilled-awareness/[sap-name]/`
   - Document broken links
   - Note intentional external links

4. **Document Gaps** (0.5h)
   - Create gap report
   - Prioritize: Critical / High / Nice-to-have

5. **Create Critical Content** (1-2h)
   - Fill gaps that block SAP usage
   - Update awareness-guide
   - Re-run link checker

6. **Enhance Awareness Guide** (1h)
   - Add "Related Content" section
   - Ensure 4-domain coverage
   - Add concrete examples

### Batching Strategy for Efficiency

**Infrastructure SAPs** (batch together):
- SAP-003 (Project Bootstrap)
- SAP-005 (CI/CD Workflows)
- SAP-006 (Quality Gates)
- SAP-011 (Docker Operations)

**Advanced Capabilities** (batch together):
- SAP-009 (Agent Awareness)
- SAP-010 (Memory System)
- SAP-013 (Metrics Tracking)

**Rationale**: Similar context, shared patterns, efficiency gains

---

## Risks & Mitigations

### High Risks

**Risk 1: Scope Creep (Creating Too Much Content)**
- **Probability**: High
- **Impact**: High (timeline extension)
- **Mitigation**:
  - Focus on critical gaps only
  - Document nice-to-haves for future waves
  - Set 30% content creation limit (stop if exceeded)
- **Indicator**: Content creation exceeds 33 hours
- **Action**: Stop creating, move to backlog

**Risk 2: Link Checker Delays SAP-016 Creation**
- **Probability**: Medium
- **Impact**: High (blocks all audit work)
- **Mitigation**:
  - Prioritize SAP-016 above all else
  - Use simple grep-based approach if script is complex
  - Don't let perfect be enemy of good
- **Indicator**: SAP-016 not complete by Day 3
- **Action**: Simplify script, defer enhancements

**Risk 3: Inconsistent Audit Quality**
- **Probability**: Medium
- **Impact**: Medium (some SAPs excellent, others weak)
- **Mitigation**:
  - Create audit checklist (in workflow)
  - Review first 3 SAPs, adjust pattern
  - Use same template for all gap reports
- **Indicator**: Tier 1 SAPs have different enhancement levels
- **Action**: Normalize approach, re-audit if needed

### Medium Risks

**Risk 4: Time Estimation Errors**
- **Probability**: Medium
- **Impact**: Medium (timeline slip)
- **Mitigation**:
  - Track actual time per SAP
  - Adjust estimates after first 3 SAPs
  - Use buffer time wisely
- **Indicator**: First SAP takes 2× estimated time
- **Action**: Reduce scope or extend timeline

**Risk 5: Missing System Files**
- **Probability**: Low
- **Impact**: Medium (broken references)
- **Mitigation**:
  - Validate file paths during audit
  - Update inventory script if mappings wrong
  - Document "to be created" vs "should exist"
- **Indicator**: Many broken system file references
- **Action**: Create missing files or update SAP claims

**Risk 6: Discovered Gaps Too Large**
- **Probability**: Medium
- **Impact**: High (can't complete in wave)
- **Mitigation**:
  - Gap analysis early (Phase 2)
  - Prioritize ruthlessly
  - Defer large gaps to Wave 3+
- **Indicator**: Critical gap total > 40 hours
- **Action**: Escalate, discuss scope reduction

---

## Dependencies

**Blockers**: None

**Prerequisites**:
- ✅ Wave 1 complete (4-domain structure)
- ✅ 100% coherence achieved
- ✅ All SAPs exist (14/14)

**Dependent Work**:
- Wave 3 (MCP Extraction) depends on SAP-002, SAP-007 audit
- Wave 4 (Clone & Merge) depends on complete SAP documentation
- External adopters depend on complete SAPs for adoption

---

## Daily Standup Questions

### What did I complete yesterday?
- Which SAP(s) audited?
- What gaps identified?
- What content created?

### What am I working on today?
- Which SAP(s) to audit?
- What content to create?
- Any blockers?

### Any impediments?
- Link checker issues?
- Unclear SAP claims?
- Missing system files?
- Scope concerns?

---

## Tracking Matrix

### SAP Audit Status

| SAP ID | Name | Tier | Estimate | Status | Gaps Found | Content Created | Validated |
|--------|------|------|----------|--------|------------|-----------------|-----------|
| SAP-016 | Link Validation | 0 (Foundation) | 12-16h | Not Started | N/A | N/A | N/A |
| SAP-000 | SAP Framework | 1 | 6h | Not Started | ? | ? | ☐ |
| SAP-007 | Documentation Framework | 1 | 5h | Not Started | ? | ? | ☐ |
| SAP-002 | Chora-Base | 1 | 6h | Not Started | ? | ? | ☐ |
| SAP-004 | Testing Framework | 1 | 4h | Not Started | ? | ? | ☐ |
| SAP-001 | Inbox Protocol | 2 | 6h | Not Started | ? | ? | ☐ |
| SAP-012 | Development Lifecycle | 2 | 5h | Not Started | ? | ? | ☐ |
| SAP-008 | Automation Scripts | 2 | 4h | Not Started | ? | ? | ☐ |
| SAP-003 | Project Bootstrap | 3 | 3h | Not Started | ? | ? | ☐ |
| SAP-005 | CI/CD Workflows | 3 | 3h | Not Started | ? | ? | ☐ |
| SAP-006 | Quality Gates | 3 | 3h | Not Started | ? | ? | ☐ |
| SAP-009 | Agent Awareness | 3 | 4h | Not Started | ? | ? | ☐ |
| SAP-010 | Memory System | 3 | 4h | Not Started | ? | ? | ☐ |
| SAP-011 | Docker Operations | 3 | 4h | Not Started | ? | ? | ☐ |
| SAP-013 | Metrics Tracking | 3 | 3h | Not Started | ? | ? | ☐ |

**Progress**: 0/15 SAPs complete (0%) - SAP-016 + 14 existing

---

## Definition of Done

For this sprint to be complete:

- [ ] SAP-016 created (5 artifacts + script)
- [ ] All 14 existing SAPs audited
- [ ] Link checker passes on all SAPs
- [ ] Critical gaps filled (90%+)
- [ ] High-value gaps filled (70%+)
- [ ] Inventory validation: 100% coherence
- [ ] Wave 2 metrics documented
- [ ] Wave 2 release notes complete
- [ ] Git commit: v3.5.0
- [ ] No broken links in SAPs

---

## Process Adherence

**Target**: ≥90% workflow compliance

**Workflows being followed**:
- ✅ DDD (Documentation Driven Design) - Workflow created before audit
- ✅ Systematic Audit - Same pattern for all SAPs
- ✅ Continuous Validation - Link checker after each SAP
- ✅ Meta-dogfooding - Using all 4 domains during execution
- ✅ Cleanup Tracking - Update manifest as we go

**Process Metrics to Track**:
- Time: Estimated vs Actual (per SAP)
- Quality: Link validation pass rate
- Coverage: Avg domains referenced per SAP
- Efficiency: SAPs audited per day
- Adherence: % of audit steps followed

---

## Sprint Retrospective (To Complete at End)

### What Went Well?
- [To be filled during execution]

### What Could Be Improved?
- [To be filled during execution]

### Action Items for Wave 3?
- [To be filled during execution]

### SAP Opportunities Discovered?
- [To be filled - track in wave-2-sap-opportunities.md]

### Velocity Calculation
- Committed: 96 hours
- Completed: [TBD] hours
- Velocity: [TBD]% (Target: 80-90%)

---

## Meta-Dogfooding Plan

### Using dev-docs/ (Developer Process)

**Creating**:
- SAP_AUDIT_WORKFLOW.md (how we audit SAPs)
- Any missing workflows discovered (TDD, SAP creation, etc.)
- Examples of SAP usage

### Using project-docs/ (Project Lifecycle)

**Creating**:
- This sprint plan (planning artifact)
- Daily progress updates (in metrics or tracking doc)
- wave-2-execution-metrics.md (results)
- v3.5.0-wave-2-release-notes.md (what shipped)

### Using user-docs/ (Product Documentation)

**Creating**:
- How-to guides for SAP adoption
- Explanation of SAP framework benefits
- Reference docs for SAP catalog

### Using skilled-awareness/ (SAP Layer)

**Enhancing**:
- All 14 existing SAPs
- Creating SAP-016 (new)
- Demonstrating cross-domain integration

---

**Sprint Plan Version**: 1.0
**Created**: 2025-10-28
**Owner**: Claude (chora-base development)
**Status**: ACTIVE

This sprint plan demonstrates chora-base's project-docs/ domain in action (Wave 2).
