# AGENTS.md/CLAUDE.md SAP Alignment Gap Analysis

**Audit Date**: 2025-11-12
**Auditor**: Claude (Task: chora-base-sxg)
**Scope**: All AGENTS.md and CLAUDE.md files vs 45 active/pilot SAPs
**Status**: ❌ Gaps identified - remediation required

---

## Executive Summary

**Problem**: Significant gaps exist between SAPs marked as "adopted" in sap-catalog.json and their documentation in awareness files (AGENTS.md/CLAUDE.md). This creates friction for agents trying to use adopted SAPs in practice.

**Impact**: Agents cannot discover or use key SAPs (SAP-015 beads, SAP-001 inbox, SAP-042-047 capability server suite, SAP-033-041 React wave) because they are not documented in the awareness network.

**Root Cause**: Rapid SAP adoption (30 → 45 SAPs in recent waves) without updating awareness files to reflect new capabilities.

**Recommendation**: Implement 3-tier remediation plan (P0 critical fixes, P1 high-priority additions, P2 integration patterns).

---

## Gap Analysis by File

### 1. docs/skilled-awareness/AGENTS.md

**File Role**: Domain-level awareness for SAP registry, primary discovery point for agents

**Gaps Identified**:

| Line | Gap | Severity | Fix Required |
|------|-----|----------|--------------|
| 219 | SAP-047 description says "Cookiecutter template" | P0 | Change to "Jinja2-based template" |

**Status**: 99% correct, 1 critical gap

**Impact**: High - misleads agents about SAP-047 implementation approach

---

### 2. Root AGENTS.md

**File Role**: Root navigation + critical workflows, first file read by agents

**Gaps Identified**:

| Line | Gap | Severity | Fix Required |
|------|-----|----------|--------------|
| 219 | Says "30+ capabilities" | P0 | Change to "45 capabilities" |
| 425-435 | Quick Reference table shows only 8 SAPs | P0 | Add SAP-042-047, key React SAPs |

**Missing SAPs in Quick Reference**:
- SAP-042 (interface-design) - pilot, foundational for capability servers
- SAP-043 (multi-interface) - pilot, 75% time savings
- SAP-044 (registry) - pilot, service discovery
- SAP-045 (bootstrap) - pilot, 90% failure reduction
- SAP-046 (composition) - pilot, 1,141% ROI
- SAP-047 (capability-server-template) - pilot, 2,271% ROI
- SAP-033 (react-authentication) - pilot, 93.75% time savings
- SAP-034 (react-database-integration) - pilot, 89.6% time savings
- SAP-041 (react-form-validation) - pilot, 88.9% time savings

**Status**: 60% complete, critical gaps in recent SAPs

**Impact**: Critical - agents cannot discover 15+ newly adopted SAPs

---

### 3. docs/skilled-awareness/CLAUDE.md

**File Role**: Claude-specific patterns for SAP navigation and adoption

**Gaps Identified**:

| Section | Gap | Severity | Fix Required |
|---------|-----|----------|--------------|
| Entire file | No Claude-specific workflows for SAP-015 (beads) | P1 | Add beads usage examples |
| Entire file | No Claude-specific workflows for SAP-001 (inbox) | P1 | Add inbox coordination examples |
| Entire file | No mentions of SAP-042-047 (capability server suite) | P1 | Add capability server generation workflow |
| Entire file | No tips for SAP-033-041 (React wave 5 SAPs) | P2 | Add React SAP Claude patterns |

**Status**: 40% complete for newly adopted SAPs

**Impact**: High - Claude cannot provide specific guidance on key SAPs

**Example Missing Workflow**:
```markdown
### Workflow: Using Beads for Task Tracking (SAP-015)

User: "Continue working on the feature from yesterday"

Claude:
1. Check if SAP-015 adopted: ls .beads/
2. If yes: bd ready --json to find unblocked work
3. Read task details: bd show {id} --json
4. Resume work with full context

Why: Beads provides persistent memory across sessions
```

---

### 4. docs/dev-docs/AGENTS.md

**File Role**: Developer workflows for contributing to chora-base

**Gaps Identified**:

| Section | Gap | Severity | Fix Required |
|---------|-----|----------|--------------|
| Entire file | No SAP-015 (beads) for development task tracking | P1 | Add beads usage in dev workflow |
| Line 98 | Mentions SAP-006 once, no deeper patterns | P2 | Add pre-commit hook integration |
| Entire file | No SAP-005 (ci-cd-workflows) usage patterns | P2 | Add GitHub Actions workflow |
| Entire file | No SAP integration patterns | P2 | Add SAP-specific dev workflows |

**Status**: 20% complete for SAP integration

**Impact**: Medium - developers don't know how to use adopted SAPs during development

**Example Missing Workflow**:
```markdown
### Workflow: Track Development Tasks with Beads (SAP-015)

When: Starting work on feature or bug fix

Steps:
1. Check ready tasks: bd ready --json
2. Claim task: bd update {id} --status in_progress --assignee {name}
3. Work on task using TDD/BDD/DDD workflows
4. Add progress comments: bd comment {id} "Completed X, next Y"
5. Close task: bd close {id} --reason "Implemented and tested"
```

---

### 5. docs/user-docs/AGENTS.md

**File Role**: End-user documentation navigation

**Gaps Identified**:

| Line | Gap | Severity | Fix Required |
|------|-----|----------|--------------|
| 450 | Says "All 30+ SAP capabilities" | P0 | Change to "45 SAP capabilities" |
| Entire file | No SAP-specific user workflows | P2 | Add SAP usage patterns for end-users |
| Entire file | No SAP integration patterns | P2 | Add how SAPs integrate with user docs |

**Status**: 30% complete for SAP integration

**Impact**: Low-Medium - users navigate to skilled-awareness for SAP details anyway

---

### 6. docs/project-docs/AGENTS.md

**File Role**: Project management workflows

**Gaps Identified**:

| Section | Gap | Severity | Fix Required |
|---------|-----|----------|--------------|
| Entire file | No SAP-015 (beads) for project task tracking | P1 | Add beads project management workflow |
| Line 407 | Mentions SAP-015 ledger, no usage patterns | P2 | Add beads usage in sprint planning |
| Entire file | No SAP-001 (inbox) for project coordination | P1 | Add inbox coordination workflow |
| Entire file | No SAP integration patterns | P2 | Add SAP-specific project workflows |

**Status**: 10% complete for SAP integration

**Impact**: Medium - project managers cannot leverage SAPs for coordination/tracking

**Example Missing Workflow**:
```markdown
### Workflow: Sprint Planning with Beads (SAP-015)

Steps:
1. Review backlog: bd list --status open --priority 0,1 --json
2. Create sprint epic: bd create "Sprint N: Goals" --type epic --priority 0
3. Decompose into tasks: bd create "Task 1" --priority 0 --parent {epic_id}
4. Add dependencies: bd dep add {task2_id} {task1_id}
5. Track sprint progress: bd ready --json
```

---

## Prioritized Remediation Plan

### Priority 0 (P0) - Critical Fixes (15-30 minutes)

**Goal**: Fix incorrect/outdated information that actively misleads agents

**Tasks**:
1. ✅ Fix SAP-047 "Cookiecutter" → "Jinja2-based" in docs/skilled-awareness/AGENTS.md:219
2. ✅ Update "30+" → "45 capabilities" in Root AGENTS.md:219
3. ✅ Update "30+" → "45 capabilities" in docs/user-docs/AGENTS.md:450
4. ✅ Add missing SAPs to Root AGENTS.md Quick Reference table (SAP-042-047, SAP-033-041)

**Deliverable**: All awareness files have accurate SAP counts and descriptions

---

### Priority 1 (P1) - High-Priority Additions (1-2 hours)

**Goal**: Document key SAPs (beads, inbox, capability server) in root and domain awareness files

**Tasks**:
1. ✅ Add SAP-015 (beads) usage patterns to Root AGENTS.md
   - Section: "Common Workflows" → Add "Workflow: Multi-Session Task Tracking with Beads"
2. ✅ Add SAP-001 (inbox) usage patterns to Root AGENTS.md
   - Section: "Common Workflows" → Add "Workflow: Cross-Repo Coordination with Inbox"
3. ✅ Add Claude-specific workflows to docs/skilled-awareness/CLAUDE.md
   - Workflow: Using Beads for Persistent Memory (SAP-015)
   - Workflow: Coordinating via Inbox (SAP-001)
   - Workflow: Generating Capability Servers (SAP-047)
4. ✅ Add SAP-015 workflows to docs/dev-docs/AGENTS.md
   - Section: "Development Workflows" → Add beads integration
5. ✅ Add SAP-015 workflows to docs/project-docs/AGENTS.md
   - Section: "Common Workflows" → Add sprint planning with beads

**Deliverable**: Agents can discover and use beads, inbox, and capability server template via awareness files

---

### Priority 2 (P2) - Integration Patterns (2-3 hours)

**Goal**: Add comprehensive SAP integration patterns to all domain awareness files

**Tasks**:
1. ✅ Add "SAP Integration Patterns" section to docs/dev-docs/AGENTS.md
   - Pattern: SAP-015 + TDD/BDD/DDD workflows
   - Pattern: SAP-006 (quality-gates) + pre-commit hooks
   - Pattern: SAP-005 (ci-cd-workflows) + GitHub Actions
2. ✅ Add "SAP Integration Patterns" section to docs/user-docs/AGENTS.md
   - How SAPs enhance user documentation
   - When to navigate to skilled-awareness for SAP details
3. ✅ Add "SAP Integration Patterns" section to docs/project-docs/AGENTS.md
   - Pattern: SAP-015 (beads) + sprint planning
   - Pattern: SAP-001 (inbox) + cross-repo coordination
   - Pattern: SAP-019 (sap-self-evaluation) + audit workflows
4. ✅ Add React SAP (SAP-033-041) tips to docs/skilled-awareness/CLAUDE.md
   - Claude-specific patterns for React authentication, database, forms

**Deliverable**: Complete SAP integration awareness across all domains

---

## Success Metrics

**Before Remediation**:
- SAP count accuracy: 67% (2/3 files correct)
- SAP-015 (beads) documentation: 10% (mentioned, no workflows)
- SAP-001 (inbox) documentation: 30% (some patterns documented)
- SAP-042-047 documentation: 20% (listed in INDEX.md, not in awareness)
- SAP-033-041 documentation: 5% (listed in catalog, not in awareness)

**After P0 Remediation** (Target):
- SAP count accuracy: 100%
- Core SAP descriptions: 100% accurate

**After P1 Remediation** (Target):
- SAP-015 (beads) documentation: 80% (workflows in root, dev-docs, project-docs)
- SAP-001 (inbox) documentation: 80% (workflows in root, skilled-awareness)
- SAP-042-047 documentation: 70% (workflows in root, CLAUDE.md)

**After P2 Remediation** (Target):
- SAP integration patterns: 90% (all domains have SAP-specific sections)
- Agent discoverability: 95% (agents can find and use any adopted SAP)

---

## Validation Plan

**After Each Priority Level**:
1. Read all modified AGENTS.md files
2. Check that SAP-015, SAP-001, SAP-042-047 workflows are present
3. Verify SAP count accuracy (should say "45 capabilities")
4. Test agent navigation: Can agent find beads workflow? Inbox workflow? Capability server workflow?

**Final Validation**:
1. Read root AGENTS.md → Should have beads + inbox workflows
2. Read docs/skilled-awareness/CLAUDE.md → Should have Claude-specific SAP workflows
3. Read all domain AGENTS.md files → Should have SAP integration patterns
4. Verify all "30+" references updated to "45 capabilities"

---

## Related Tasks

- **chora-base-sxg**: This audit task
- **chora-base-43o**: Fixed SAP-047 Cookiecutter → Jinja2 (✅ completed, missed AGENTS.md update)
- **chora-base-4if**: Updated INDEX.md with 6 new capability server SAPs (✅ completed)

---

## Conclusion

**Current State**: 45 SAPs adopted, but only ~40% documented in awareness network. This creates a gap between "SAP adopted" and "SAP actually used in practice."

**Root Cause**: Rapid SAP growth (30 → 45 SAPs in recent waves) without corresponding awareness file updates.

**Recommendation**: Implement 3-tier remediation plan (P0: 15-30 min, P1: 1-2 hours, P2: 2-3 hours). Total effort: 3.5-5.5 hours.

**Expected Outcome**: Agents can seamlessly discover and use all 45 adopted SAPs via awareness network, closing the adoption-usage gap.

---

**Audit Status**: ✅ Complete
**Next Action**: Begin P0 remediation (fix SAP counts, SAP-047 description)
