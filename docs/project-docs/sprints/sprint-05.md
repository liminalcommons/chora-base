# Sprint 5: Bidirectional Translation Layer Integration

**Sprint ID**: Sprint-05
**Version**: v4.1.3
**Sprint Goal**: Complete bidirectional translation layer integration (SAP-009 v1.1.0) to enable mutual ergonomics between conversational input and procedural execution
**Duration**: 1-2 sprints (16-24 hours)
**Estimated Effort**: 16-24 hours
**Start Date**: TBD (Q1 2026)
**Target Completion**: TBD (Q1 2026)

---

## Sprint Goal

Complete the bidirectional translation layer integration (Phase 2-4 of BIDIRECTIONAL_COMMUNICATION.md) to enable agents to "just know" how to use translation tools as native and second nature. Foundation tools (intent-router.py, chora-search.py, suggest-next.py) are already complete; this sprint integrates them into SAP-009 and establishes usage patterns across the ecosystem.

### Context

Foundation work completed in previous session:
- ✅ scripts/intent-router.py (470 lines) - Pattern matching engine
- ✅ scripts/chora-search.py (380 lines) - Glossary search
- ✅ scripts/suggest-next.py (470 lines) - Context-aware suggestions
- ✅ docs/dev-docs/patterns/INTENT_PATTERNS.yaml (24 patterns)
- ✅ docs/GLOSSARY.md (75+ terms, 14 categories)
- ✅ .chora/user-preferences.yaml.template (100+ config options)
- ✅ docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md (implementation guide)
- ✅ AGENTS.md (+214 lines with tool discovery patterns)
- ✅ COORD-2025-004 coordination request created

This sprint addresses user feedback: "lets make sure we are using our process and including governance and administrative doc updates where appropriate" by following full DDD → BDD → TDD lifecycle.

### Scope

**Included**:
- DDD Phase: Create change request following Diátaxis framework
- BDD Phase: Write Gherkin scenarios for intent recognition, preferences, pattern learning
- TDD Phase: Enhance SAP-009 protocol-spec.md, awareness-guide.md, ledger.md
- Integration: Update 5 domain AGENTS.md files with user signal patterns (SAP-001, 004, 009, 012, 013)
- Testing: Achieve ≥85% coverage, validate intent recognition ≥80% accuracy
- Governance: Update CHANGELOG.md, SAP Index, emit events with trace_id

**Excluded**:
- Auto-loading of tools (use subprocess invocation for generic agent compatibility)
- Pattern auto-addition without review (manual curation maintains quality)
- Automation of LLM-intelligent tasks (tools are translation only, not generation)

---

## Success Criteria

### Quantitative
- [ ] Intent recognition accuracy ≥80% on test query set (30+ queries)
- [ ] Test coverage ≥85% for integration code
- [ ] All BDD scenarios passing (intent routing, glossary, suggestions, preferences)
- [ ] 0 lint errors, 0 type errors
- [ ] 5 domain AGENTS.md files updated with user signal patterns

### Qualitative
- [ ] Generic agents (Claude, Cursor, etc.) can discover tools via documentation alone
- [ ] Tools gracefully degrade (missing tool → documented pattern fallback)
- [ ] User preferences successfully adapt agent behavior (all 100+ config options)
- [ ] Pattern learning captures new variations without breaking existing patterns
- [ ] Documentation follows Diátaxis framework (how-to, reference, explanation)

### Meta-Goals
- [ ] SAP-009 enhanced to v1.1.0
- [ ] CHANGELOG.md updated with v4.1.3 entry
- [ ] SAP Index updated (SAP-009: 1.0.0 → 1.1.0)
- [ ] All events logged with trace_id: coord-2025-004-bidirectional
- [ ] COORD-2025-004 marked as completed in ECOSYSTEM_STATUS.yaml

---

## Committed Work Items

### Phase 1: Governance Updates (COMPLETE)
✅ Created COORD-2025-004 coordination request
✅ Updated ECOSYSTEM_STATUS.yaml
✅ Emitted coordination_request_created event
✅ Updated SAP-009 ledger.md with v1.1.0 "In Progress"
✅ Created Sprint 5 plan (this document)

### Phase 2: DDD - Documentation Driven Design (2-3 hours)

**Objective**: Create comprehensive change request defining the enhancement contract

**Tasks**:
1. **Task 2.1: Create Change Request**
   - **Estimate**: 1.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - inbox/active/task-NNN/change-request.md (Diátaxis format)
     - Documents what, why, how of bidirectional translation layer
     - Defines contracts for intent router, glossary search, suggestion engine
   - **Dependencies**: Sprint plan approval

2. **Task 2.2: Technical Lead Review**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Approval or feedback on change request
     - Adjustments if needed
   - **Dependencies**: Task 2.1 complete

**Phase 2 Exit Criteria**:
- [ ] Change request created following Diátaxis framework
- [ ] Technical lead approval obtained
- [ ] phase_completed event emitted for DDD

### Phase 3: BDD - Behavior Driven Development (1.5 hours)

**Objective**: Define expected behaviors via Gherkin scenarios before implementation

**Tasks**:
1. **Task 3.1: Write Gherkin Scenarios**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - features/bidirectional-integration.feature
     - Scenarios for intent recognition, glossary search, context analysis, preference loading
     - Example: "Given user input 'show inbox', When intent router processes, Then returns 'run_inbox_status' with ≥70% confidence"
   - **Dependencies**: Phase 2 complete

2. **Task 3.2: Implement Step Definitions**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - features/steps/bidirectional_steps.py
     - Executable step definitions calling tools
   - **Dependencies**: Task 3.1 complete

**Phase 3 Exit Criteria**:
- [ ] All Gherkin scenarios written
- [ ] Step definitions implemented
- [ ] All scenarios RED (failing, as expected before implementation)
- [ ] phase_completed event emitted for BDD

### Phase 4: TDD - SAP-009 Enhancement (8-12 hours)

**Objective**: Implement bidirectional translation layer integration via RED-GREEN-REFACTOR

**Tasks**:
1. **Task 4.1: Enhance SAP-009 protocol-spec.md**
   - **Estimate**: 2-3 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Section 9: Bidirectional Translation Layer (added to protocol-spec.md)
     - Contracts for intent router, glossary search, suggestion engine
     - Integration points with existing SAP-009 patterns
   - **Dependencies**: Phase 3 complete

2. **Task 4.2: Enhance SAP-009 awareness-guide.md**
   - **Estimate**: 2-3 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Integration patterns for generic agents
     - Tool discovery workflows (3-layer: root → domain → intent patterns)
     - Usage examples (conversational → procedural translation)
   - **Dependencies**: Task 4.1 complete

3. **Task 4.3: Update 5 Domain AGENTS.md Files**
   - **Estimate**: 3-4 hours
   - **Status**: Not Started
   - **Deliverables**:
     - docs/skilled-awareness/inbox-protocol/AGENTS.md (SAP-001 user signals)
     - docs/skilled-awareness/testing-framework/AGENTS.md (SAP-004 user signals)
     - docs/skilled-awareness/agent-awareness/AGENTS.md (SAP-009 user signals)
     - docs/skilled-awareness/development-lifecycle/AGENTS.md (SAP-012 user signals)
     - docs/skilled-awareness/metrics-framework/AGENTS.md (SAP-013 user signals)
     - Each file: Add user signal patterns mapping conversational input → formal actions
   - **Dependencies**: Task 4.2 complete

4. **Task 4.4: Integrate Suggestion Engine with Inbox Protocol**
   - **Estimate**: 1-2 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Enhancement to suggest-next.py for inbox-aware suggestions
     - Integration hooks in inbox protocol for proactive recommendations
   - **Dependencies**: Task 4.3 complete

**Phase 4 Exit Criteria**:
- [ ] All BDD scenarios GREEN (passing)
- [ ] Test coverage ≥85%
- [ ] RED-GREEN-REFACTOR cycles complete
- [ ] phase_completed event emitted for TDD

### Phase 5: Testing & Quality Gates (4-6 hours)

**Objective**: Validate integration quality and accuracy

**Tasks**:
1. **Task 5.1: Intent Recognition Accuracy Testing**
   - **Estimate**: 2 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Test suite with 30+ query variations
     - Accuracy report (target: ≥80%)
     - Pattern refinements if needed
   - **Dependencies**: Phase 4 complete

2. **Task 5.2: Preference Adaptation Testing**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - Test suite validating all 100+ config options
     - Behavior adaptation verification
   - **Dependencies**: Task 5.1 complete

3. **Task 5.3: Pattern Learning Validation**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - Test suite for new pattern variations
     - Regression tests (existing patterns still work)
   - **Dependencies**: Task 5.2 complete

4. **Task 5.4: Quality Gate Validation**
   - **Estimate**: 1-2 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Coverage report ≥85%
     - Lint validation (0 errors)
     - Type checking (0 errors)
     - Documentation completeness check
   - **Dependencies**: Task 5.3 complete

**Phase 5 Exit Criteria**:
- [ ] Intent recognition ≥80% accurate
- [ ] Preference adaptation verified
- [ ] Pattern learning validated
- [ ] All quality gates passing
- [ ] phase_completed event emitted for Testing

### Phase 6: Governance Documentation Updates (2-3 hours)

**Objective**: Complete all governance and administrative documentation

**Tasks**:
1. **Task 6.1: Update CHANGELOG.md**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - v4.1.3 entry following Keep a Changelog format
     - Sections: Added (bidirectional translation layer), Changed (SAP-009 enhancement)
   - **Dependencies**: Phase 5 complete

2. **Task 6.2: Update SAP-009 Artifacts**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - capability-charter.md (version 1.0.0 → 1.1.0)
     - ledger.md (v1.1.0 release date and changes, "In Progress" → release date)
     - Version history updated in all SAP-009 files
   - **Dependencies**: Task 6.1 complete

3. **Task 6.3: Update SAP Index**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - docs/skilled-awareness/INDEX.md (SAP-009: 1.0.0 → 1.1.0)
     - Last Updated date refreshed
   - **Dependencies**: Task 6.2 complete

4. **Task 6.4: Emit Governance Events**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - phase_completed events for all phases
     - sap_enhanced event for SAP-009 v1.1.0
     - All events include trace_id: coord-2025-004-bidirectional
   - **Dependencies**: Task 6.3 complete

**Phase 6 Exit Criteria**:
- [ ] CHANGELOG.md updated with v4.1.3
- [ ] SAP-009 artifacts updated to v1.1.0
- [ ] SAP Index updated
- [ ] All governance events emitted
- [ ] phase_completed event emitted for Governance

### Phase 7: Review & Integration (4 hours)

**Objective**: Code review, PR approval, CI/CD validation

**Tasks**:
1. **Task 7.1: Create Pull Request**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - PR with comprehensive checklist
     - Summary of changes (11 deliverables from COORD-2025-004)
     - Link to coordination request
   - **Dependencies**: Phase 6 complete

2. **Task 7.2: Code Review**
   - **Estimate**: 2 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Review feedback
     - Adjustments if needed
     - Approval
   - **Dependencies**: Task 7.1 complete

3. **Task 7.3: CI/CD Validation**
   - **Estimate**: 1 hour
   - **Status**: Not Started
   - **Deliverables**:
     - All CI checks passing
     - Integration tests passing
     - Link validation passing
   - **Dependencies**: Task 7.2 complete

**Phase 7 Exit Criteria**:
- [ ] PR created and approved
- [ ] All CI/CD checks passing
- [ ] No merge conflicts
- [ ] phase_completed event emitted for Review

### Phase 8: Release & Deployment (1 hour)

**Objective**: Version bump, GitHub release, archival

**Tasks**:
1. **Task 8.1: Version Bump**
   - **Estimate**: 0.25 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Version updated (4.1.2 → 4.1.3)
     - Git tag created (v4.1.3)
   - **Dependencies**: Phase 7 complete

2. **Task 8.2: Create GitHub Release**
   - **Estimate**: 0.5 hours
   - **Status**: Not Started
   - **Deliverables**:
     - Release notes from CHANGELOG.md
     - Tag published to GitHub
     - Release artifacts if applicable
   - **Dependencies**: Task 8.1 complete

3. **Task 8.3: Archive Completed Work**
   - **Estimate**: 0.25 hours
   - **Status**: Not Started
   - **Deliverables**:
     - COORD-2025-004 marked completed in ECOSYSTEM_STATUS.yaml
     - coordination_request_completed event emitted
     - inbox/active/ work archived if applicable
   - **Dependencies**: Task 8.2 complete

**Phase 8 Exit Criteria**:
- [ ] Version bumped to v4.1.3
- [ ] GitHub release created
- [ ] COORD-2025-004 marked completed
- [ ] release_created event emitted
- [ ] Sprint complete

---

## Effort Breakdown

| Phase | Tasks | Est. Hours | % of Total |
|-------|-------|------------|------------|
| Phase 1: Governance Updates | 3 | COMPLETE | - |
| Phase 2: DDD | 2 | 2-3 | 11% |
| Phase 3: BDD | 2 | 1.5 | 7% |
| Phase 4: TDD | 4 | 8-12 | 50% |
| Phase 5: Testing & Quality | 4 | 4-6 | 23% |
| Phase 6: Governance Docs | 4 | 2-3 | 11% |
| Phase 7: Review | 3 | 4 | 18% |
| Phase 8: Release | 3 | 1 | 4% |
| **Total** | **25** | **16-24** | **100%** |

---

## Risk Assessment

### High Risk
- **Risk**: Intent recognition accuracy <80% after implementation
  - **Impact**: Tools don't meet user expectations, adoption low
  - **Mitigation**: Pilot testing with 30+ queries before integration, pattern refinement iteration

- **Risk**: Generic agents can't discover tools via documentation alone
  - **Impact**: Integration fails core objective (native and second nature)
  - **Mitigation**: Validate with multiple agent types (Claude, Cursor), documentation-first approach

### Medium Risk
- **Risk**: Pattern learning creates false positives or breaks existing patterns
  - **Impact**: User frustration, reduced confidence in tools
  - **Mitigation**: Comprehensive regression tests, manual pattern curation vs. auto-addition

- **Risk**: Preference adaptation doesn't work for edge case configurations
  - **Impact**: Some users can't use tools effectively
  - **Mitigation**: Test all 100+ config options, graceful degradation

### Low Risk
- **Risk**: Sprint extends beyond 24 hours due to scope creep
  - **Impact**: Delays v4.1.3 release, blocks dependent work
  - **Mitigation**: Strict scope adherence (excluded items documented), phase-based checkpoints

---

## Dependencies

### External Dependencies
- None (all work internal to chora-base)

### Internal Dependencies
- ✅ Foundation tools complete (scripts/intent-router.py, chora-search.py, suggest-next.py)
- ✅ Root AGENTS.md updated (+214 lines with tool discovery patterns)
- ✅ .gitignore updated for user configs
- ✅ COORD-2025-004 coordination request created
- ✅ SAP-009 ledger.md updated with v1.1.0 "In Progress"
- ✅ Sprint 5 plan created

---

## Validation Plan

### Pre-Sprint Validation
- [x] Foundation tools executable and tested individually
- [x] Coordination request created and logged
- [x] SAP-009 ledger updated
- [x] Sprint plan created
- [ ] Sprint plan approved by technical lead
- [ ] Start date scheduled

### In-Sprint Validation
- [ ] Phase 2 validation: Change request approved
- [ ] Phase 3 validation: All scenarios RED (pre-implementation)
- [ ] Phase 4 validation: All scenarios GREEN (post-implementation)
- [ ] Phase 5 validation: All quality gates passing

### Post-Sprint Validation
- [ ] All 12 acceptance criteria met (from COORD-2025-004)
- [ ] All 11 deliverables created
- [ ] Documentation complete and following Diátaxis
- [ ] v4.1.3 release published

---

## Rollout Strategy

### Phase Sequencing
1. **Phase 2 (DDD)**: Documentation-first approach establishes contracts before code
2. **Phase 3 (BDD)**: Scenarios define expected behaviors, fail initially (RED)
3. **Phase 4 (TDD)**: Implementation makes scenarios pass (GREEN), then refactor
4. **Phase 5 (Testing)**: Validate quality, accuracy, and edge cases
5. **Phase 6 (Governance)**: Complete administrative documentation
6. **Phase 7 (Review)**: External validation via PR review
7. **Phase 8 (Release)**: Public release with proper versioning

### Commit Strategy
- Commit after each major task completion
- Comprehensive commit messages with COORD-2025-004 reference
- Tag v4.1.3 at final release
- All commits include Co-Authored-By: Claude for traceability

### Review Points
- After Phase 2: Technical lead approval of change request
- After Phase 4: Internal review of SAP-009 enhancements
- After Phase 6: Governance documentation completeness check
- After Phase 7: Final PR approval before release

---

## Metrics & Tracking

### Progress Tracking
- **Phases Complete**: 1/8 (12.5%)
- **Tasks Complete**: 3/25 (12%)
- **Estimated Hours Remaining**: 16-24 hours
- **Target Release**: v4.1.3 (PATCH)

### Quality Metrics
- **Intent Recognition Accuracy**: Target ≥80%
- **Test Coverage**: Target ≥85%
- **Lint/Type Errors**: Target 0
- **BDD Scenarios Passing**: Target 100%
- **Documentation Coverage**: All 11 deliverables from COORD-2025-004

### Event Traceability
- **Trace ID**: coord-2025-004-bidirectional
- **Events Logged**: 1 (coordination_request_created)
- **Target Events**: 8+ (phase completions, SAP enhancement, release)

---

## Documentation Plan

### Documents to Create
1. inbox/active/task-NNN/change-request.md - DDD specification (~800-1200 lines)
2. features/bidirectional-integration.feature - BDD scenarios (~200-300 lines)
3. features/steps/bidirectional_steps.py - Step definitions (~300-400 lines)
4. docs/releases/v4.1.3-release-notes.md - Release documentation (~200-300 lines)

### Documents to Update
1. docs/skilled-awareness/agent-awareness/protocol-spec.md - Add Section 9 (~400-600 lines)
2. docs/skilled-awareness/agent-awareness/awareness-guide.md - Add integration patterns (~300-500 lines)
3. docs/skilled-awareness/agent-awareness/ledger.md - Update v1.1.0 release info (~20 lines)
4. docs/skilled-awareness/agent-awareness/capability-charter.md - Version 1.0.0 → 1.1.0 (~10 lines)
5. docs/skilled-awareness/INDEX.md - SAP-009 version update (~5 lines)
6. CHANGELOG.md - Add v4.1.3 entry (~30-50 lines)
7. 5 domain AGENTS.md files - Add user signal patterns (~100-150 lines each, 500-750 total)

### Summary Documentation
- Sprint summary: docs/project-docs/sprints/sprint-05-summary.md (create post-completion)
- Metrics report: Included in sprint summary
- Lessons learned: Included in sprint summary

---

## Communication Plan

### Stakeholder Updates
- **Frequency**: After each phase completion
- **Format**: Event log entries (events.jsonl) with trace_id
- **Audience**: Ecosystem repos using inbox protocol, future chora-base contributors

### Decision Points
- **Phase 2 Completion**: Proceed with BDD or adjust scope based on change request feedback
- **Phase 4 Completion**: Proceed with testing or iterate on implementation
- **Phase 5 Completion**: Proceed with governance docs or address quality issues
- **Sprint Completion**: Release v4.1.3 or defer if critical issues discovered

---

## Next Steps After Sprint

### Immediate Follow-up
- [ ] Create GitHub release for v4.1.3
- [ ] Update ECOSYSTEM_STATUS.yaml (mark COORD-2025-004 completed)
- [ ] Archive sprint artifacts
- [ ] Create sprint-05-summary.md

### Future Sprints
- Sprint 6 (TBD): Potential enhancements based on bidirectional translation layer usage patterns
- Sprint 7 (TBD): Integration with other SAPs not covered in Sprint 5
- Pattern learning improvements based on real-world usage data

---

## Appendix

### Related Documents
- [COORD-2025-004 Coordination Request](../../inbox/incoming/coordination/COORD-2025-004-bidirectional-integration.json)
- [COORD-2025-004 Communication Brief](../../inbox/coordination/COORD-2025-004-communication-brief.md)
- [BIDIRECTIONAL_COMMUNICATION.md Implementation Guide](../dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md)
- [SAP-009 Agent Awareness](../skilled-awareness/agent-awareness/)
- [SAP-012 Development Lifecycle](../skilled-awareness/development-lifecycle/)

### Reference Materials
- [Intent Patterns Database](../dev-docs/patterns/INTENT_PATTERNS.yaml)
- [Ecosystem Glossary](../../GLOSSARY.md)
- [User Preferences Template](../../.chora/user-preferences.yaml.template)
- [Root AGENTS.md](../../AGENTS.md) - Lines 732-944 (tool discovery patterns)

### Foundation Tools (Already Complete)
- scripts/intent-router.py (470 lines)
- scripts/chora-search.py (380 lines)
- scripts/suggest-next.py (470 lines)
- docs/dev-docs/patterns/INTENT_PATTERNS.yaml (377 lines, 24 patterns)
- docs/GLOSSARY.md (640 lines, 75+ terms)
- .chora/user-preferences.yaml.template (380 lines, 100+ options)
- docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md (1,060 lines)

---

**Sprint Plan Version**: 1.0
**Last Updated**: 2025-10-31
**Status**: Pending Approval
**Coordination Request**: COORD-2025-004
**Trace ID**: coord-2025-004-bidirectional
