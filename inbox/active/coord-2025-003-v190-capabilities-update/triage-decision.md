# Triage Decision: COORD-2025-003

**Request**: Update chora-base documentation to reference chora-compose v1.9.0 capabilities
**From**: chora-compose
**Date Received**: 2025-10-30
**Date Triaged**: 2025-10-30
**Trace ID**: CHORA-COORD-2025-003

---

## Decision: ✅ ACCEPT

**Priority**: Medium (as requested)
**Urgency**: 2025-W44 sprint
**Estimated Effort**: 2-4 hours (aligns with request estimate)
**Assigned To**: Next available sprint

---

## Rationale

### Strategic Alignment
- **Supports CORD-2025-002 pilot**: Documentation updates enable efficient use of chora-compose for SAP generation
- **Enables Wave 6 Collections architecture**: v4.2.0 planning depends on understanding chora-compose capabilities
- **Cross-repo collaboration success**: Directly follows successful pilot negotiation (CORD-2025-002 accepted)

### Technical Merit
- **95% token reduction**: Stigmergic context links reduce 20k→1k tokens for common operations
- **Automated maintenance**: Freshness tracking enables proactive SAP maintenance
- **Foundation for ecosystem coordination**: Pattern applicable to other cross-repo operations

### Risk Assessment
- **Low implementation risk**: Documentation-only changes, no code modifications
- **Low scope creep**: Clear deliverables with measurable acceptance criteria
- **All dependencies met**: chora-compose v1.9.0 released, documentation complete

### Quality of Request
- **Excellent documentation**: 566-line communication brief with comprehensive technical details
- **Clear acceptance criteria**: 5 specific, measurable criteria provided
- **Realistic effort estimate**: 2-4 hours matches complexity of documentation updates
- **Pre-provided resources**: Communication brief, templates, examples all included

---

## Deliverables (Per Acceptance Criteria)

### 1. Update AGENTS.md with Stigmergic Context Links
**Acceptance Criterion**: "chora-base AGENTS.md includes stigmergic context link examples (e.g., [@chora-compose/collection:sap-004-complete])"

**Changes Required**:
- Add new section: "Cross-Repository Coordination via Stigmergic Context Links"
- Document the `[@repo/capability:resource-id]` pattern
- Provide examples for SAP regeneration:
  - `[@chora-compose/collection:sap-004-complete]` - Generate full SAP
  - `[@chora-compose/freshness:all-saps]` - Check all SAPs freshness
  - `[@chora-compose/generate:charter:sap-004]` - Generate single artifact
- Highlight token efficiency (95% reduction: 20k→1k tokens)
- Reference v1.9.0 capabilities in appropriate sections

**Location**: [AGENTS.md](../../../AGENTS.md) (line ~100-150, after "Installing SAPs" section)

**Effort**: 30-45 minutes

---

### 2. Document Freshness Tracking Workflow
**Acceptance Criterion**: "SAP maintenance workflow documented with freshness tracking integration"

**Changes Required**:
- Create new document: `docs/guides/sap-maintenance-workflow.md`
- Document three-state classification (fresh/stale/expired)
- Explain freshness threshold configuration
- Provide workflow examples:
  - Weekly freshness checks
  - Prioritized regeneration (expired first, then stale)
  - Health monitoring dashboard integration
- Link from SAP Index and relevant SAPs

**Effort**: 60-90 minutes

---

### 3. Add CI/CD Integration Example
**Acceptance Criterion**: "At least one CI/CD example showing automated freshness checks"

**Changes Required**:
- Create `.github/workflows/sap-freshness.yml` (example/template)
- Document workflow in sap-maintenance-workflow.md
- Weekly schedule: Monday 10am
- Output handling: Comment on issue or Slack notification
- Manual trigger via workflow_dispatch for testing

**Effort**: 30-45 minutes

---

### 4. Bidirectional Cross-References
**Acceptance Criterion**: "Cross-references between chora-base and chora-compose documentation are bidirectional"

**Changes Required**:
- Update relevant SAPs to reference chora-compose capabilities:
  - SAP-000 (sap-framework): Add stigmergic links for SAP regeneration
  - SAP-001 (inbox-coordination): Update cross-repo coordination examples
  - SAP-009 (agent-awareness): Add v1.9.0 capability patterns
- Ensure links point to chora-compose docs (communication brief provides paths)
- Verify chora-compose docs already link back to chora-base (per request background)

**Effort**: 30-45 minutes

---

### 5. Validation via Generation Test
**Acceptance Criterion**: "Changes validated by generating at least one SAP using stigmergic context links"

**Changes Required**:
- Test stigmergic context link end-to-end:
  - Place `[@chora-compose/collection:sap-004-complete]` in test document
  - Verify AI agent recognizes pattern
  - Confirm MCP tool executes correctly
  - Validate SAP-004 generates successfully
- Test freshness check:
  - Run `choracompose:check_freshness` on existing SAP collection
  - Verify output format matches communication brief
- Document test results in acceptance response

**Effort**: 15-30 minutes

---

## Total Effort Breakdown

| Task | Estimated Time |
|------|----------------|
| Update AGENTS.md | 30-45 min |
| Create SAP maintenance workflow guide | 60-90 min |
| Create CI/CD workflow example | 30-45 min |
| Update SAP cross-references | 30-45 min |
| Validation testing | 15-30 min |
| **Total** | **165-255 min (2.75-4.25 hours)** |

**Aligns with request estimate**: 2-4 hours ✅

---

## Dependencies

### External (All Met)
- ✅ chora-compose v1.9.0 released (2025-10-30)
- ✅ Stigmergic context links documentation complete
- ✅ Freshness tracking documentation complete
- ✅ Communication brief provided (566 lines of technical details)

### Internal (None Blocking)
- CORD-2025-002 pilot approved but not started (no blocker - this enables the pilot)
- SAP Index current (18 SAPs documented)
- AGENTS.md maintained and up-to-date

---

## Risk Mitigation

### Identified Risks
1. **Risk**: Stigmergic context links not yet battle-tested in chora-base
   - **Mitigation**: Validation testing (acceptance criterion #5) will reveal issues
   - **Fallback**: Document pattern but mark as "experimental" if testing reveals problems

2. **Risk**: CI/CD workflow may need adjustment for chora-base environment
   - **Mitigation**: Create example/template, not production-ready workflow
   - **Note**: Can refine in follow-up based on actual usage

3. **Risk**: Freshness tracking may not align with chora-base SAP maintenance cadence
   - **Mitigation**: Document as option, not requirement
   - **Flexibility**: Team can adjust thresholds and schedules per their workflow

### Low-Risk Assessment
- Documentation-only changes (no breaking changes possible)
- Clear rollback path (revert documentation commits)
- No impact on existing SAP functionality
- Additive features (existing workflows continue unchanged)

---

## Success Metrics

### Immediate (End of Sprint)
- ✅ All 5 acceptance criteria met
- ✅ Validation testing successful
- ✅ Documentation reviewed and merged
- ✅ Response sent to chora-compose (acknowledgment + deliverables)

### Near-term (1-2 weeks)
- Usage data: How many times stigmergic context links used in chora-base operations
- Token savings: Measured reduction in context loading for SAP regeneration
- Freshness adoption: Whether team uses freshness tracking for SAP maintenance

### Long-term (1-3 months)
- CORD-2025-002 pilot success: Documentation enables efficient pilot execution
- Cross-repo coordination patterns: Other repos adopt stigmergic links
- SAP maintenance efficiency: Reduced manual tracking via automated freshness checks

---

## Next Steps

### 1. Move to Active (Immediate)
- [x] Create `inbox/active/coord-2025-003-v190-capabilities-update/`
- [ ] Move coordination request JSON to active directory
- [ ] Move communication brief to active directory
- [ ] Log `coordination_request_accepted` event

### 2. Create Change Request (Phase 3: DDD)
- [ ] Draft `change-request.md` with detailed implementation plan
- [ ] Break down into atomic commits
- [ ] Define done criteria per deliverable
- [ ] Create branch: `feature/coord-2025-003-chora-compose-v190-docs`

### 3. Schedule Implementation (2025-W44)
- [ ] Assign to next available sprint slot
- [ ] Block out 2-4 hours for focused work
- [ ] Schedule validation testing
- [ ] Plan response communication to chora-compose

### 4. Send Acceptance Response (Within 72 hours)
- [ ] Draft COORD-2025-003-RESPONSE.json
- [ ] Acknowledge acceptance
- [ ] Confirm timeline: 2025-W44 (this week or next)
- [ ] Reference triage decision and change request
- [ ] Log `coordination_response_sent` event

---

## Approval

**Triaged By**: Claude (AI Agent)
**Reviewed By**: [Pending human review]
**Approved By**: [Pending]
**Date**: 2025-10-30

**Decision**: ✅ ACCEPT - Straightforward documentation update supporting successful cross-repo collaboration

**Confidence**: High
- Clear deliverables
- Realistic effort estimate
- All dependencies met
- Strategic alignment confirmed
- Low risk, high value

---

**Next Action**: Create change-request.md and move files to active directory
