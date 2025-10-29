# SAP Awareness Integration Audit - Triage Report

**Date**: 2025-10-29
**Audit Tool**: `scripts/check-sap-awareness-integration.sh`
**Scope**: All 18 SAPs in `docs/skilled-awareness/`

---

## Executive Summary

**Current PASS Rate**: **11% (2/18 SAPs)**
**Target PASS Rate**: **100% (18/18 SAPs)**
**Gap**: **16 SAPs requiring remediation**

**Primary Issue**: Missing "Post-Install Awareness Enablement" section in adoption blueprints

---

## Detailed Results

###  ✅ PASSING SAPs (2/18)

| SAP ID | Name | Score | Status | Notes |
|--------|------|-------|--------|-------|
| SAP-000 | sap-framework | 4/4 | ✅ PASS | All checks passed |
| SAP-001 | inbox | 2/4 | ⚠️  PASS (warnings) | 2 warnings (missing validation cmd, agent instructions) |

###  ❌ FAILING SAPs (16/18)

#### Pattern A: Missing Post-Install + AGENTS.md (11 SAPs)

| SAP ID | Name | Checks Failed | Missing |
|--------|------|---------------|---------|
| SAP-004 | testing-framework | 2/4 | Post-install section, AGENTS.md mention |
| SAP-005 | ci-cd-workflows | 2/4 | Post-install section, AGENTS.md mention |
| SAP-006 | quality-gates | 2/4 | Post-install section, AGENTS.md mention |
| SAP-007 | documentation-framework | 2/4 | Post-install section, AGENTS.md mention |
| SAP-008 | automation-scripts | 2/4 | Post-install section, AGENTS.md mention |
| SAP-011 | docker-operations | 2/4 | Post-install section, AGENTS.md mention |
| SAP-012 | development-lifecycle | 2/4 | Post-install section, AGENTS.md mention |
| SAP-013 | metrics-tracking | 2/4 | Post-install section, AGENTS.md mention |
| SAP-015 | link-validation-reference-management | 2/4 | Post-install section, AGENTS.md mention |
| SAP-016 | mcp-server-development | 2/4 | Post-install section, AGENTS.md mention |
| SAP-017 | chora-compose-integration | 2/4 | Post-install section, AGENTS.md mention |
| SAP-018 | chora-compose-meta | 2/4 | Post-install section, AGENTS.md mention |

#### Pattern B: Missing Post-Install Only (5 SAPs)

| SAP ID | Name | Checks Failed | Missing | Has AGENTS.md? |
|--------|------|---------------|---------|----------------|
| SAP-002 | chora-base | 1/4 | Post-install section | ✅ Yes |
| SAP-003 | project-bootstrap | 1/4 | Post-install section | ✅ Yes |
| SAP-009 | agent-awareness | 1/4 | Post-install section | ✅ Yes |
| SAP-010 | memory-system | 1/4 | Post-install section | ✅ Yes |

---

## Root Cause Analysis

### Why SAPs Are Failing

**Missing Component**: "Post-Install Awareness Enablement" section in `adoption-blueprint.md`

**What This Section Does**:
1. Instructs agents/users to update root `AGENTS.md` file
2. Provides specific content to add (concrete template, not placeholders)
3. Includes validation command to verify update
4. Explains why this step matters (discoverability)

**Reference Example**: [SAP-000 adoption-blueprint.md:208-251](../../docs/skilled-awareness/sap-framework/adoption-blueprint.md#L208-L251)

### Impact of Missing Section

**Without Awareness Enablement**:
- ❌ Agents cannot discover installed SAPs
- ❌ No visibility into available capabilities
- ❌ SAPs remain "invisible" after installation
- ❌ Fails Wave 2 quality gates

**With Awareness Enablement**:
- ✅ AGENTS.md serves as capability index
- ✅ Agents can find SAPs by reading root file
- ✅ Clear installation verification
- ✅ Meets SAP framework quality standards

---

## Remediation Plan

### Phase 1: Pattern A SAPs (11 SAPs - 11 hours)

**Task**: Add complete post-install awareness section

**For each SAP**:
1. Add "Step X: Update Project AGENTS.md" section
2. Include:
   - Why this matters (discoverability)
   - Agent-executable instructions (Edit tool)
   - Concrete content template (specific to SAP)
   - Validation command
3. Ensure AGENTS.md file path is correct
4. Add validation grep command

**Estimated Effort**: ~1 hour per SAP × 11 = **11 hours**

**SAPs**:
- SAP-004: testing-framework
- SAP-005: ci-cd-workflows
- SAP-006: quality-gates
- SAP-007: documentation-framework
- SAP-008: automation-scripts
- SAP-011: docker-operations
- SAP-012: development-lifecycle
- SAP-013: metrics-tracking
- SAP-015: link-validation-reference-management
- SAP-016: mcp-server-development
- SAP-017: chora-compose-integration
- SAP-018: chora-compose-meta

### Phase 2: Pattern B SAPs (5 SAPs - 4 hours)

**Task**: Add post-install section (AGENTS.md already mentioned)

**For each SAP**:
1. Add "Step X: Update Project AGENTS.md" section
2. Same requirements as Phase 1
3. These SAPs already mention AGENTS.md elsewhere, just missing formal post-install step

**Estimated Effort**: ~45 min per SAP × 5 = **3.75 hours**

**SAPs**:
- SAP-002: chora-base
- SAP-003: project-bootstrap
- SAP-009: agent-awareness
- SAP-010: memory-system

### Phase 3: Validation (1 hour)

**Task**: Re-run audit to verify 100% PASS rate

**Steps**:
1. Run `check-sap-awareness-integration.sh` on all 18 SAPs
2. Verify all SAPs pass basic checks
3. Document before/after metrics
4. Create final audit summary report

**Estimated Effort**: **1 hour**

---

## Total Effort Estimate

| Phase | SAPs | Hours | Notes |
|-------|------|-------|-------|
| Phase 1 | 11 | 11.0 | Complete section addition |
| Phase 2 | 5 | 3.75 | Partial section addition |
| Phase 3 | - | 1.0 | Re-validation |
| **Total** | **16** | **15.75** | **~16 hours** |

**Original Estimate**: 25-35 hours
**Actual Estimate**: ~16 hours (more focused scope after triage)

---

## Quality Standards

### Checklist for Each Remediation

- [ ] Section titled "Step X: Update Project AGENTS.md"
- [ ] Includes "Why This Step Matters" explanation
- [ ] Includes "For agents" executable instructions
- [ ] Provides concrete content template (no `<placeholders>`)
- [ ] Includes validation command (`grep ... AGENTS.md`)
- [ ] References SAP-specific capability name
- [ ] Links to SAP documentation paths
- [ ] Passes `check-sap-awareness-integration.sh`

### Content Template Pattern

```markdown
### Step X: Update Project AGENTS.md

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the <SAP-NAME> capability.

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

\`\`\`markdown
### <Capability Name>

<Description of what this capability provides>

**Documentation**: [docs/skilled-awareness/<sap-directory>/](/docs/skilled-awareness/<sap-directory>/)

**Quick Start**:
- Read: [adoption-blueprint.md](/docs/skilled-awareness/<sap-directory>/adoption-blueprint.md)
- Guide: [awareness-guide.md](/docs/skilled-awareness/<sap-directory>/awareness-guide.md)
\`\`\`

**Validation**:
\`\`\`bash
grep "<Capability Name>" AGENTS.md && echo "✅ AGENTS.md updated"
\`\`\`
```

---

## Success Criteria

### Audit Completion Criteria

- [x] All 18 SAPs audited with helper script
- [x] Triage report created with detailed findings
- [ ] All 16 failing SAPs remediated
- [ ] Re-validation shows 100% PASS rate (18/18)
- [ ] Final audit summary report published
- [ ] INDEX.md updated with awareness scores

### Quality Gates

- **Basic Checks**: All 4 checks pass for all 18 SAPs
- **PASS Rate**: 100% (18/18 SAPs)
- **Documentation**: All SAPs have agent-discoverable awareness sections
- **Validation**: Helper script exits 0 for all SAPs

---

## Next Actions

1. **Begin Phase 1 Remediation** (11 SAPs)
   - Start with Wave 3 SAPs (SAP-016, SAP-017, SAP-018) - freshest in context
   - Then infrastructure SAPs (SAP-005, SAP-006, SAP-011)
   - Then workflow SAPs (SAP-007, SAP-008, SAP-012, SAP-013, SAP-015)
   - Finally testing SAP (SAP-004)

2. **Phase 2 Remediation** (5 SAPs)
   - SAP-002, SAP-003, SAP-009, SAP-010

3. **Re-Validation**
   - Run audit script on all 18
   - Create final summary

4. **Complete Coordination Request**
   - Move coord-002 to completed
   - Publish audit summary to `docs/project-docs/audits/`
   - Update INDEX.md with awareness scores
   - Emit completion event

---

**Document Version**: 1.0
**Created**: 2025-10-29
**Status**: Triage Complete - Ready for Remediation
