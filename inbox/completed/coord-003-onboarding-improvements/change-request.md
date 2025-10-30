# Change Request: COORD-003 - Onboarding Improvements

**Status**: Accepted - In Progress
**Phase**: Phase 3 (DDD - Domain-Driven Design)
**Created**: 2025-10-30
**Request ID**: coord-003
**Trace ID**: chora-workspace-onboarding-improvements-2025-10-30

---

## Executive Summary

Implement 7 high-impact onboarding improvements across 2 sprints to reduce friction for new chora-base adopters (AI agents and humans). Based on quantitative pilot adoption feedback, these improvements target a 50% reduction in onboarding time (from 3-4 hours to 1.5-2 hours) while increasing success rate from ~60% to 90%+.

**Decision**: ACCEPTED with phased Sprint 1 + Sprint 2 implementation
**Total Effort**: 14-18 development hours + 3-4 hours artifact review
**Timeline**: 4 weeks (2 sprints)

---

## Phase 3: Domain-Driven Design (DDD)

### Problem Domain Analysis

**Domain**: Developer Onboarding Experience
**Subdomain**: chora-base adoption workflow (from discovery → installation → validation → productive use)

#### Current State Pain Points

From pilot adoption (chora-workspace, 3-4 hour onboarding, 18/18 SAPs verified):

**Ergonomics Issues** (Decision-making & Understanding):
1. **Decision paralysis**: 15-30 minutes reading 500+ lines to choose SAP set
2. **Unclear success criteria**: "Am I done?" uncertainty at each tier
3. **Text-only dependency graph**: Difficult to visualize SAP relationships
4. **Common pitfalls undocumented**: Repeated issues (file locations, prerequisites)

**Efficiency Issues** (Installation & Validation):
5. **No pre-flight validation**: 40-60% of adopters hit prerequisite failures mid-installation
6. **No progress indicators**: Anxiety/uncertainty during 5-15 minute installation
7. **Scattered validation steps**: Post-install verification unclear
8. **No custom .chorabase template**: Organizations reverse-engineer format

**Effectiveness Issues** (Measurement & Guidance):
9. **Time estimates vs actuals not tracked**: Cannot measure improvement
10. **Agent-specific quickstarts buried**: Must parse 2000+ line generic guide
11. **No session handoff mechanism**: Session interruption = start over
12. **Success metrics undefined**: Unclear what "successful onboarding" means

#### Domain Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Onboarding Journey                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Discovery          → Learn about chora-base              │
│     └─ PAIN: No decision tree for SAP set selection          │
│                                                               │
│  2. Pre-Flight         → Validate prerequisites              │
│     └─ PAIN: No validation script (40-60% fail mid-install)  │
│                                                               │
│  3. Installation       → Run install-sap.py                  │
│     └─ PAIN: No progress indicators (anxiety)                │
│                                                               │
│  4. Validation         → Verify successful installation      │
│     └─ PAIN: Scattered validation steps                      │
│                                                               │
│  5. First Use          → Apply SAP knowledge                 │
│     └─ PAIN: Agent-specific guides buried in 2000+ lines     │
│                                                               │
│  6. Mastery            → Achieve tier success criteria       │
│     └─ PAIN: Unclear what "success" means per tier           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### Key Entities & Value Objects

**Entities**:
- `Adopter` (AI Agent | Human Developer)
- `SAP Set` (minimal-entry | balanced | comprehensive | full-adoption)
- `Installation Session` (with progress, checkpoints, duration)
- `Validation Report` (pre-flight, post-install, infrastructure)

**Value Objects**:
- `Success Criteria` (per tier: essential/recommended/advanced)
- `Progress Indicator` (current/total, time estimate)
- `Decision Tree` (flowchart: questions → recommended set)
- `FAQ Entry` (issue, solution, frequency)

---

## Requirements Specification

### Functional Requirements

#### Sprint 1 Deliverables (6-8 hours)

**FR-1: Pre-flight Validation Script**
- **File**: `scripts/validate-prerequisites.sh`
- **Inputs**: None (auto-detects environment)
- **Outputs**:
  - Exit code 0 (pass) | 1 (fail)
  - Color-coded report: ✅ PASS / ❌ FAIL / ⚠️ WARNING
- **Validations**:
  - Python 3.8+ installed and in PATH
  - Git 2.x+ installed
  - Required directories exist (`docs/`, `scripts/`, `.chora/`)
  - Sufficient disk space (>100MB)
  - Write permissions to target directories
- **Acceptance Criteria**: Catches 90%+ of prerequisite issues before `install-sap.py` runs
- **Reference**: Integrate learnings from contributed `validate-infrastructure.sh`

**FR-2: Common Onboarding Issues FAQ**
- **File**: `docs/user-docs/troubleshooting/onboarding-faq.md`
- **Structure**:
  ```markdown
  # Common Onboarding Issues

  ## Installation Issues
  ### Issue: Python version mismatch
  ### Issue: Git not found
  ### Issue: Permission denied errors

  ## SAP Set Selection
  ### Issue: Which SAP set should I choose?
  ### Issue: Can I change SAP set later?

  ## Validation Issues
  ### Issue: How do I know installation succeeded?
  ### Issue: SAP awareness check failed

  ## (10+ total entries)
  ```
- **Content**: Top 10 friction points from pilot + solutions
- **Acceptance Criteria**: Addresses common issues with self-service solutions

**FR-3: Visual Decision Tree for SAP Set Selection**
- **File**: `docs/user-docs/reference/sap-set-decision-tree.md`
- **Format**: Mermaid flowchart
- **Questions**:
  1. "Are you a first-time adopter or setting up a new project?" → YES: minimal-entry
  2. "Do you need custom SAP configuration?" → YES: comprehensive
  3. "Do you want all SAPs for reference?" → YES: full-adoption, NO: balanced
- **Acceptance Criteria**: Reduces SAP set selection from 500+ line doc read to <5 minutes
- **Visual**:
  ```mermaid
  graph TD
    A[Start: Choose SAP Set] --> B{First-time adopter?}
    B -->|Yes| C[minimal-entry<br/>4 essential SAPs]
    B -->|No| D{Need custom SAPs?}
    D -->|Yes| E[comprehensive<br/>9 curated SAPs]
    D -->|No| F{Want all SAPs?}
    F -->|Yes| G[full-adoption<br/>18 SAPs]
    F -->|No| H[balanced<br/>6 SAPs]
  ```

#### Sprint 2 Deliverables (8-10 hours)

**FR-4: Enhanced install-sap.py with Progress Indicators**
- **File**: `scripts/install-sap.py` (modification)
- **Enhancement**: Add real-time progress tracking
- **Display Format**:
  ```
  Installing SAP Set: minimal-entry (4 SAPs)
  [========>           ] 2/4 SAPs installed (50%)
  Current: SAP-002 (inbox-coordination)
  Estimated time remaining: ~3 minutes
  ```
- **Implementation**:
  - Track current/total SAP count
  - Estimate time based on average SAP install time (~30 seconds)
  - Update progress bar after each SAP
- **Acceptance Criteria**: Progress indicator visible during installation, time estimates within 20% accuracy

**FR-5: Agent-Specific Quickstart Guides**
- **Files**:
  - `docs/user-docs/how-to/quickstart-claude.md`
  - `docs/user-docs/how-to/quickstart-generic-ai-agent.md`
- **Length**: <500 lines each (vs 2000+ line generic guide)
- **Structure**:
  ```markdown
  # Quickstart: Claude Code Agent

  ## Prerequisites (2 minutes)
  - Python 3.8+
  - Git

  ## Installation (5 minutes)
  1. Clone repository
  2. Run pre-flight validation: `bash scripts/validate-prerequisites.sh`
  3. Install SAPs: `python scripts/install-sap.py minimal-entry`

  ## Validation (2 minutes)
  - Check SAP awareness: `ls docs/skilled-awareness/`
  - Verify 4 SAP directories exist

  ## First Task (5 minutes)
  - Process inbox coordination request (example walkthrough)

  Total time: ~15 minutes
  ```
- **Acceptance Criteria**: Reduces onboarding time by 30%+ vs generic guide for AI agents

**FR-6: Success Criteria Checklists**
- **Files**:
  - `docs/skilled-awareness/adoption-blueprint-minimal-entry.md`
  - `docs/skilled-awareness/adoption-blueprint-balanced.md`
  - `docs/skilled-awareness/adoption-blueprint-comprehensive.md`
  - `docs/skilled-awareness/adoption-blueprint-full-adoption.md`
- **Addition**: Add "Success Criteria" section to each blueprint
- **Format**:
  ```markdown
  ## Success Criteria

  ### Essential Tier
  - [ ] Installation completes without errors
  - [ ] All SAPs visible in docs/skilled-awareness/
  - [ ] Can read SAP-000 protocol specification
  - **Time**: 5 minutes or less

  ### Recommended Tier
  - [ ] Pre-flight validation passes
  - [ ] SAP awareness verification passes (verify-sap-awareness.py)
  - [ ] Can explain SAP dependency relationships
  - **Time**: 15 minutes or less

  ### Advanced Tier
  - [ ] Infrastructure validation passes (all tiers)
  - [ ] Can process inbox coordination request
  - [ ] Can create custom .chorabase configuration
  - **Time**: 30 minutes or less
  ```
- **Acceptance Criteria**: Clear pass/fail criteria for each tier, measurable time targets

**FR-7: Mermaid Dependency Graph Visualization**
- **File**: `docs/skilled-awareness/INDEX.md` (modification)
- **Addition**: Visual SAP dependency graph
- **Format**: Mermaid flowchart showing 18 SAPs with dependency arrows
- **Example**:
  ```mermaid
  graph TD
    SAP000[SAP-000: Protocol Spec] --> SAP001[SAP-001: Inbox]
    SAP000 --> SAP002[SAP-002: Coordination]
    SAP001 --> SAP003[SAP-003: Triage]
    SAP002 --> SAP003
    ...
  ```
- **Acceptance Criteria**: All 18 SAPs represented, dependency arrows accurate, renders in GitHub

### Non-Functional Requirements

**NFR-1: Performance**
- Pre-flight validation completes in <10 seconds
- Progress indicators update at least every 2 seconds
- Decision tree loads instantly in markdown viewers

**NFR-2: Usability**
- FAQ entries have clear problem/solution structure
- Agent quickstarts follow consistent template
- Success checklists use checkbox markdown for printability

**NFR-3: Maintainability**
- All scripts include inline documentation
- Visual diagrams use Mermaid (version controllable, not binary images)
- FAQ organized by category for easy updates

**NFR-4: Compatibility**
- Pre-flight validation works on macOS, Linux, Windows (Git Bash)
- Progress indicators compatible with standard terminals (no fancy Unicode if not supported)
- Mermaid diagrams render in GitHub, VSCode, common markdown viewers

### Deferred Requirements (Backlog)

**DR-1: Onboarding Checkpoint/Resume System** (deferred pending design)
- Rationale: Requires state management design, recovery mechanisms, testing
- Future work: Explore `.chora-onboarding-progress.json` format in separate design doc

**DR-2: Optional Telemetry for Onboarding Metrics** (deferred pending privacy review)
- Rationale: Requires privacy review, opt-in UX design, data governance
- Future work: Coordinate with ecosystem governance on telemetry standards

**DR-3: Custom .chorabase Template** (deferred - lower priority)
- Rationale: Medium priority - most adopters use predefined SAP sets
- Future work: Consider after Sprint 1-2 deliverables validated by early adopters

---

## Design Approach

### Architecture Decisions

**AD-1: Validation Script as Standalone Tool**
- **Decision**: `validate-prerequisites.sh` is separate script, not integrated into `install-sap.py`
- **Rationale**:
  - Can be run independently before installation
  - Easier to test and maintain
  - Can be used in CI/CD pipelines
- **Alternative Considered**: Integrate into `install-sap.py` as pre-flight step
- **Trade-off**: Separate script = extra step, but more flexible

**AD-2: Mermaid for Visual Diagrams**
- **Decision**: Use Mermaid syntax for decision tree and dependency graph
- **Rationale**:
  - Version controllable (text, not binary images)
  - Renders in GitHub, VSCode, common viewers
  - Easy to update and maintain
- **Alternative Considered**: PNG/SVG graphics
- **Trade-off**: Mermaid requires viewer support, but much better for collaboration

**AD-3: Agent-Specific Guides as Separate Files**
- **Decision**: Create `quickstart-claude.md`, `quickstart-generic-ai-agent.md` in `docs/user-docs/how-to/`
- **Rationale**:
  - Easier to navigate than single 2000+ line guide
  - Agent-specific optimizations (commands, validation steps)
  - Can expand to more agent types (Codex, Cursor, etc.) without bloat
- **Alternative Considered**: Sections in single guide
- **Trade-off**: More files to maintain, but better UX

**AD-4: Success Criteria as Checklist Markdown**
- **Decision**: Use `- [ ]` checkbox syntax in markdown
- **Rationale**:
  - Printable and actionable
  - Familiar GitHub/VSCode checkbox rendering
  - Can be copy-pasted into issues/PRs
- **Alternative Considered**: Prose description
- **Trade-off**: Checkboxes are more visual, less narrative

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Improved Onboarding Flow                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Discovery                                                 │
│     └─ Read decision tree (sap-set-decision-tree.md)         │
│     └─ Answer 3 questions → Recommended SAP set              │
│                                                               │
│  2. Pre-Flight                                                │
│     └─ Run: bash scripts/validate-prerequisites.sh           │
│     └─ Output: ✅ PASS / ❌ FAIL report                      │
│     └─ If FAIL: Check FAQ (onboarding-faq.md)                │
│                                                               │
│  3. Installation                                              │
│     └─ Run: python scripts/install-sap.py [set-name]         │
│     └─ Watch: [====>    ] 5/10 SAPs, ~8 min remaining       │
│     └─ Complete: Installation finished                        │
│                                                               │
│  4. Validation                                                │
│     └─ Check: Success criteria checklist (adoption-blueprint)│
│     └─ Verify: SAP awareness, infrastructure validation      │
│                                                               │
│  5. First Use                                                 │
│     └─ Follow: Agent-specific quickstart (quickstart-*.md)   │
│     └─ Complete: First task (e.g., process inbox request)    │
│                                                               │
│  6. Mastery                                                   │
│     └─ Review: Dependency graph (INDEX.md mermaid)           │
│     └─ Achieve: Tier success criteria (essential/rec/adv)    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Success Metrics

**Quantitative Targets**:
- **Onboarding time**: 3-4 hours → 1.5-2 hours (50% reduction)
- **Pre-flight validation**: Catches 90%+ prerequisite issues
- **Decision tree**: SAP set selection 15-30 min → <5 min (83% reduction)
- **Agent quickstarts**: Documentation reading 2000+ lines → <800 lines (60% reduction)
- **Success rate**: ~60% → 90%+ (based on prerequisite failures)

**Qualitative Targets**:
- Reduced "Am I done?" uncertainty (clear success checklists)
- Reduced anxiety during installation (progress indicators)
- Self-service troubleshooting (FAQ resolves 80%+ common issues)
- Better SAP understanding (visual dependency graph)

**Measurement Plan**:
- Post-Sprint 2: Pilot test with fresh AI agent + human adopter
- Compare time, errors, questions vs baseline pilot
- Collect qualitative feedback on clarity, confidence, satisfaction

---

## Implementation Plan

### Sprint 1 (Week 1-2) - 6-8 hours

**Week 1**:
- [ ] Review contributed `validate-infrastructure.sh` (1h)
- [ ] Create `scripts/validate-prerequisites.sh` based on learnings (2-3h)
  - Python version check
  - Git availability check
  - Directory structure check
  - Disk space check
  - Permissions check
- [ ] Test validation script on macOS/Linux (1h)
- [ ] Create `docs/user-docs/troubleshooting/onboarding-faq.md` (2h)
  - 10+ common issues from pilot observations
  - Problem/solution format
  - Links to relevant docs

**Week 2**:
- [ ] Create `docs/user-docs/reference/sap-set-decision-tree.md` (2-3h)
  - Mermaid flowchart
  - 3-question decision path
  - SAP set recommendations with rationale
- [ ] Update main installation guide to reference new tools (30min)
- [ ] Test end-to-end flow: decision tree → validation → installation (30min)

**Sprint 1 Deliverables**:
- ✅ Pre-flight validation script
- ✅ Common Issues FAQ
- ✅ Visual decision tree

### Sprint 2 (Week 3-4) - 8-10 hours

**Week 3**:
- [ ] Enhance `scripts/install-sap.py` with progress indicators (3-4h)
  - Add progress bar library or custom ASCII progress
  - Track current/total SAP count
  - Estimate time remaining (average SAP install time)
  - Test with all 4 SAP sets
- [ ] Create `docs/user-docs/how-to/quickstart-claude.md` (2h)
  - <500 lines
  - Prerequisites → Installation → Validation → First Task
  - Claude-specific commands and tips
- [ ] Create `docs/user-docs/how-to/quickstart-generic-ai-agent.md` (1.5h)
  - Template applicable to any AI agent
  - Generic validation steps

**Week 4**:
- [ ] Add success criteria to adoption blueprints (2h)
  - `adoption-blueprint-minimal-entry.md`
  - `adoption-blueprint-balanced.md`
  - `adoption-blueprint-comprehensive.md`
  - `adoption-blueprint-full-adoption.md`
  - Essential/Recommended/Advanced tier checklists
- [ ] Create Mermaid dependency graph in `INDEX.md` (1-2h)
  - 18 SAPs with dependency arrows
  - Validate accuracy against SAP specifications
- [ ] Integration testing: full onboarding flow with all improvements (1h)

**Sprint 2 Deliverables**:
- ✅ Progress indicators in install-sap.py
- ✅ Agent-specific quickstart guides
- ✅ Success criteria checklists
- ✅ Mermaid dependency graph

### Contributed Artifacts Review (3-4 hours)

**Parallel to Sprint 1**:
- [ ] Review `validate-infrastructure.sh` from chora-workspace (1-2h)
  - Extract reusable validation patterns
  - Identify checks for pre-flight validator
  - Consider integration path (scripts/ directory?)
- [ ] Review `verify-sap-awareness.py` (1h)
  - Evaluate as post-installation validation tool
  - Consider adding to quickstart guides
- [ ] Review `INFRASTRUCTURE_VERIFICATION.md` (1h)
  - Extract key insights for FAQ
  - Reference in troubleshooting docs

---

## Risk Assessment

### Technical Risks

**Risk 1: Progress Indicator Compatibility**
- **Description**: Progress bars may not render correctly on all terminals
- **Likelihood**: Medium
- **Impact**: Low (cosmetic issue)
- **Mitigation**: Use simple ASCII progress (`[====>   ]`), test on Windows/macOS/Linux
- **Fallback**: Percentage-only progress if bar doesn't render

**Risk 2: Time Estimate Accuracy**
- **Description**: Installation time estimates may be inaccurate
- **Likelihood**: Medium
- **Impact**: Low (user expectation management)
- **Mitigation**: Calibrate based on average SAP install time, add margin of error
- **Fallback**: Show progress without time estimate

**Risk 3: Mermaid Rendering Issues**
- **Description**: Some markdown viewers may not support Mermaid
- **Likelihood**: Low (GitHub/VSCode support is widespread)
- **Impact**: Low (falls back to source code)
- **Mitigation**: Test in multiple viewers, provide alt text
- **Fallback**: Add link to Mermaid live editor

### Process Risks

**Risk 4: Scope Creep**
- **Description**: Requests for additional deliverables (checkpoint system, telemetry)
- **Likelihood**: Medium
- **Impact**: Medium (timeline delay)
- **Mitigation**: Clearly communicate deferred items, stick to Sprint 1-2 scope
- **Resolution**: Create separate coordination requests for backlog items

**Risk 5: Contributed Artifact Integration Effort**
- **Description**: Reviewing and integrating contributed tools takes longer than estimated
- **Likelihood**: Medium
- **Impact**: Low (affects Sprint 1 timeline by 1-2 hours)
- **Mitigation**: Allocate dedicated review time, communicate delays early
- **Resolution**: Defer integration to post-Sprint 2 if necessary

### User Experience Risks

**Risk 6: Decision Tree Oversimplification**
- **Description**: 3-question tree may not cover all use cases
- **Likelihood**: Medium
- **Impact**: Medium (users pick wrong SAP set)
- **Mitigation**: Add "Not sure?" fallback option, link to detailed comparison
- **Resolution**: Iterate based on user feedback post-Sprint 1

---

## Dependencies & Prerequisites

### Internal Dependencies

- ✅ Wave 5 SAP Installation Tooling (complete)
- ✅ SAP Sets feature (complete)
- ✅ `install-sap.py` v1.0 (complete)
- ✅ All 18 SAPs documented with 5 artifacts each

### External Dependencies

- 📥 Contributed artifacts from chora-workspace:
  - `validate-infrastructure.sh`
  - `verify-sap-awareness.py`
  - `INFRASTRUCTURE_VERIFICATION.md`
- ⏳ Status: Requested in COORD-003-RESPONSE.json

### Prerequisites

- Python 3.8+ for script modifications
- Bash for validation script
- Mermaid support in target viewers (GitHub, VSCode)
- Access to pilot adoption data for FAQ content

---

## Testing Strategy

### Unit Testing

**Pre-flight Validation Script**:
- Test each validation check independently
- Test on missing prerequisites (Python, Git)
- Test on incorrect directory structure
- Test exit codes (0 = pass, 1 = fail)

**Progress Indicators**:
- Test with different SAP set sizes (4, 6, 9, 18 SAPs)
- Test time estimation accuracy
- Test on different terminal types

### Integration Testing

**End-to-End Onboarding Flow**:
1. Fresh clone → Decision tree → Pre-flight validation → Installation → Validation
2. Test with each SAP set (minimal-entry, balanced, comprehensive, full-adoption)
3. Test with intentional prerequisite failures (catch and report)

### User Acceptance Testing

**Post-Sprint 2 Pilot**:
- Fresh AI agent onboarding using new quickstart guide
- Fresh human developer onboarding
- Measure: time, errors, questions asked
- Compare: baseline pilot (3-4h) vs improved flow (target: 1.5-2h)

---

## Success Criteria (Change Request)

### Acceptance Criteria

- [ ] **Sprint 1 Complete**: Pre-flight validator, FAQ, decision tree delivered
- [ ] **Sprint 2 Complete**: Progress indicators, quickstarts, checklists, dependency graph delivered
- [ ] **Pre-flight validation**: Catches 90%+ prerequisite issues
- [ ] **Decision tree**: Reduces SAP set selection time by 80%+ (30min → <5min)
- [ ] **Agent quickstarts**: Reduces documentation reading by 60%+ (2000 lines → <800 lines)
- [ ] **Progress indicators**: Real-time status during installation
- [ ] **Success checklists**: Clear pass/fail criteria for all tiers
- [ ] **FAQ**: Addresses 10+ common issues with self-service solutions
- [ ] **Dependency graph**: Visual representation of all 18 SAPs
- [ ] **Pilot validation**: Post-Sprint 2 test shows 50% time reduction

### Definition of Done

- [ ] All code changes committed and pushed
- [ ] All documentation created/updated
- [ ] Integration tests pass
- [ ] Pilot validation complete with metrics
- [ ] COORD-003-RESPONSE.json updated with completion status
- [ ] Coordination event emitted (coordination_request_completed)
- [ ] Change request moved to `inbox/completed/`

---

## Communication Plan

### Stakeholder Updates

**chora-workspace (Requesting Repo)**:
- **Sprint 1 Start**: Request contributed artifacts
- **Sprint 1 Complete**: Share FAQ, decision tree, validator for review
- **Sprint 2 Complete**: Request validation of quickstart-claude.md
- **Post-Sprint 2**: Invite to pilot test with fresh agent

**chora-base Team**:
- **Weekly**: Progress updates on deliverables
- **Blockers**: Immediate communication if scope/timeline at risk
- **Completion**: Summary of metrics and learnings

### Documentation Updates

- [ ] Update main README with link to decision tree
- [ ] Update installation guide with pre-flight validation step
- [ ] Update troubleshooting section with FAQ link
- [ ] Add agent quickstarts to "Getting Started" navigation

---

## Appendix

### Reference Materials

- [COORD-003 Original Request](coord-003-onboarding-improvements.json)
- [COORD-003 Supporting Data](coord-003-supporting-data.md)
- [COORD-003 Response](COORD-003-RESPONSE.json)
- [SAP-001: Inbox Coordination Protocol](../../docs/skilled-awareness/inbox/)
- [Wave 5 Release Notes](../../docs/releases/v4.1.0/)

### Glossary

- **SAP**: Standard Adoption Pattern - reusable protocol implementation
- **SAP Set**: Curated collection of SAPs (minimal-entry, balanced, comprehensive, full-adoption)
- **Pre-flight Validation**: Prerequisite checks before installation
- **Adoption Tier**: Success level (essential, recommended, advanced)
- **DDD**: Domain-Driven Design methodology (Phase 3 of development workflow)

---

**Change Request Status**: ✅ Approved - Ready for Implementation
**Next Phase**: Phase 4 (BDD + TDD - Development)
**Assigned To**: chora-base development team
**Target Completion**: Sprint 2 end (2025-11-27)
