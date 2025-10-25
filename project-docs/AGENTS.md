# Project Planning & Management Guide

**Purpose:** Guide for project planning, roadmap, architecture decisions, wave planning.

**Parent:** See [../AGENTS.md](../AGENTS.md) for project overview and core architecture.

---

## Quick Reference

- **Current wave:** Wave 1.1 (Server catalog) - see [WAVE_1X_PLAN.md](WAVE_1X_PLAN.md)
- **Long-term roadmap:** See [../ROADMAP.md](../ROADMAP.md)
- **Architecture decisions:** ADRs in `decisions/` directory (when created)
- **Release notes:** `releases/` directory (when created)
- **Sprint planning:** `sprints/` directory (when created)

---

## Directory Structure

```
project-docs/
├── AGENTS.md           # This file - project planning guide
├── README.md           # Directory overview
├── WAVE_1X_PLAN.md     # Wave 1.x detailed planning
├── decisions/          # Architecture Decision Records (ADRs) [future]
├── releases/           # Release notes and checklists [future]
└── sprints/            # Sprint planning documents [future]
```

---

## Wave-Based Development

### Overview

**mcp-orchestration uses wave-based development** for incremental capability delivery.

**Benefits:**
- Clear milestones with deliverable scope
- Exploratory vs committed separation
- Gradual complexity scaling
- User feedback integration points

### Current Status

**Wave 1.0 (v0.1.0):** ✅ **DELIVERED**
- Core config orchestration
- Ed25519 cryptographic signing
- Content-addressable storage
- 4 MCP tools (list_clients, list_profiles, get_config, diff_config)
- 2 MCP resources
- Multi-client registry (Claude Desktop, Cursor)

**Wave 1.1:** 🟡 **IN PROGRESS**
- MCP server catalog
- Server discovery and browsing
- Server metadata management
- CLI commands for server operations
- See [WAVE_1X_PLAN.md](WAVE_1X_PLAN.md) for details

**Wave 1.2:** 📋 **PLANNED**
- Automated server installation
- Server dependency resolution
- Config composition (merge profiles)
- Enhanced diff visualization

### Future Waves (Exploratory)

**Wave 2: Governance** (Exploratory - Not Committed)
- Policy engine for config validation
- Approval workflows for changes
- Audit logging and compliance
- Role-based access control

**Wave 3: Intelligence** (Exploratory - Not Committed)
- Smart config validation (AI-powered)
- Anomaly detection in configs
- Usage analytics and insights
- Recommendation engine

**Wave 4: Ecosystem** (Exploratory - Not Committed)
- Multi-tenant SaaS deployment
- Marketplace for MCP servers
- Federation with other registries
- Community server ratings/reviews

---

## Roadmap Management

### Roadmap Document

**Location:** [../ROADMAP.md](../ROADMAP.md)

**Purpose:** Long-term vision and strategic goals.

**Contents:**
- Vision statement
- Wave progression
- Milestones and target dates
- Success metrics per wave

### When to Update Roadmap

**Update when:**
- Completing a wave (mark delivered, update dates)
- Planning next wave (refine scope, dependencies)
- Strategic pivot (market feedback, technical constraints)
- Milestone achievement (document learnings)

**Process:**
1. Review current wave progress
2. Document lessons learned
3. Refine next wave scope based on feedback
4. Update target dates and success metrics
5. Commit changes with explanation

### Roadmap Review Cadence

**Quarterly:** Full roadmap review
- Assess wave progress
- Adjust future wave scope
- Update strategic priorities

**Monthly:** Wave progress check
- Track deliverables
- Identify blockers
- Adjust timeline if needed

**Weekly:** Sprint alignment
- Ensure sprint work aligns with wave goals
- Flag risks to wave completion

---

## Wave Planning Process

### Planning a New Wave

**When to plan:** 2-4 weeks before current wave completes.

**Steps:**

**1. Define Wave Theme**
```markdown
Wave X: [Theme Name]
Goal: [1-2 sentence description of wave focus]
Target Users: [Who benefits from this wave]
Success Metrics: [How we measure success]
```

**2. Identify Capabilities**
- List features/capabilities for the wave
- Group by module/subsystem
- Prioritize must-have vs nice-to-have

**3. Technical Design**
- Architecture changes needed
- New modules or refactoring
- External dependencies
- Performance considerations

**4. Break Down into Deliverables**
- Concrete, testable deliverables
- Dependencies between deliverables
- Estimated effort per deliverable

**5. Define Done Criteria**
- Functional requirements met
- Tests passing (≥85% coverage)
- Documentation updated
- Release notes written

**6. Document in WAVE_XX_PLAN.md**
```markdown
# Wave X.X Plan

## Overview
[Wave theme, goals, timeline]

## Capabilities
[List of features/capabilities]

## Technical Design
[Architecture, modules, dependencies]

## Deliverables
[Concrete deliverables with acceptance criteria]

## Testing Strategy
[How to validate wave completion]

## Risks & Mitigations
[Potential blockers and mitigation plans]

## Success Metrics
[How to measure wave success]
```

### Wave Planning Template

**File:** Create `WAVE_XX_PLAN.md` following this structure:

```markdown
# Wave X.X Plan: [Theme]

**Status:** Planning | In Progress | Delivered
**Target:** [YYYY-MM-DD]
**Owner:** [Lead developer/PM]

---

## Overview

**Goal:** [1-2 sentences describing wave focus]

**Why this wave:** [Strategic rationale - user needs, technical debt, market opportunity]

**Success Metrics:**
- [Metric 1: e.g., 90% of users can discover servers in <30 seconds]
- [Metric 2: e.g., Zero security vulnerabilities in signing implementation]
- [Metric 3: e.g., 85%+ test coverage maintained]

---

## Capabilities

### Capability 1: [Name]
**Description:** [What users can do]
**Value:** [Why it matters]
**Complexity:** Low | Medium | High

### Capability 2: [Name]
...

---

## Technical Design

### Architecture Changes
[Diagram or description of architectural changes]

### New Modules
- `module_name/` - [Description]
- `another_module/` - [Description]

### External Dependencies
- [Dependency 1] - [Why needed]
- [Dependency 2] - [Why needed]

### Performance Considerations
[Expected performance impact, optimization strategies]

---

## Deliverables

| # | Deliverable | Owner | Estimate | Status |
|---|------------|-------|----------|--------|
| 1 | [Deliverable 1] | [Name] | X days | Not Started |
| 2 | [Deliverable 2] | [Name] | X days | In Progress |
| 3 | [Deliverable 3] | [Name] | X days | Complete |

### Deliverable 1: [Name]
**Description:** [Detailed description]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests written and passing
- [ ] Documentation updated

---

## Testing Strategy

### Unit Tests
[Which new modules need unit tests]

### Integration Tests
[Which workflows need integration tests]

### Super-Tests
[End-to-end scenarios for wave validation]

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Mitigation strategy] |
| [Risk 2] | Low/Med/High | Low/Med/High | [Mitigation strategy] |

---

## Timeline

| Milestone | Target Date | Status |
|-----------|------------|--------|
| Planning Complete | YYYY-MM-DD | ✅ |
| Development Start | YYYY-MM-DD | 🟡 |
| Feature Complete | YYYY-MM-DD | ⏳ |
| Testing & Docs | YYYY-MM-DD | ⏳ |
| Release | YYYY-MM-DD | ⏳ |

---

## Dependencies

**Upstream (must complete before this wave):**
- Wave X.Y deliverable Z

**Downstream (blocked on this wave):**
- Wave X.Z feature A

---

## Success Metrics

**Functional:**
- [ ] All capabilities deliverable
- [ ] All acceptance criteria met
- [ ] Zero P0/P1 bugs

**Quality:**
- [ ] Test coverage ≥85%
- [ ] No regressions in existing features
- [ ] Performance benchmarks met

**Documentation:**
- [ ] User docs updated
- [ ] AGENTS.md files updated
- [ ] Release notes written

---

**End of Wave X.X Plan**
```

---

## Architecture Decision Records (ADRs)

### Purpose

**ADRs document significant architectural decisions** with context, reasoning, and consequences.

**When to write an ADR:**
- Choosing between architectural patterns
- Selecting technology/library (e.g., Ed25519 vs RSA)
- Defining module boundaries
- Establishing coding standards

### ADR Template

**File:** `decisions/YYYYMMDD-title-of-decision.md`

```markdown
# ADR-XXX: [Title of Decision]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Context:** Wave X.X
**Deciders:** [Names]

---

## Context

[What is the issue we're facing? What factors are relevant?]

---

## Decision

[What is the change we're proposing/announcing?]

---

## Rationale

[Why did we choose this option? What are the benefits?]

---

## Alternatives Considered

### Alternative 1: [Name]
**Pros:** [Benefits]
**Cons:** [Drawbacks]
**Reason for rejection:** [Why not chosen]

### Alternative 2: [Name]
...

---

## Consequences

**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Drawback 1]
- [Mitigation: how we address drawback]

**Neutral:**
- [Impact 1]

---

## Implementation Notes

[How to implement this decision? Key considerations?]

---

## References

- [Link to related discussions]
- [Link to research documents]
- [Link to specifications]

---

**End of ADR**
```

### Example ADRs for mcp-orchestration

**ADR-001: Content-Addressable Storage for Artifacts**
- **Decision:** Use SHA-256 hashing for artifact IDs (Git/Docker pattern)
- **Rationale:** Immutability, deduplication, integrity verification
- **Alternative:** UUID-based IDs (rejected - no integrity guarantee)

**ADR-002: Ed25519 for Cryptographic Signatures**
- **Decision:** Use Ed25519 exclusively (no RSA, ECDSA)
- **Rationale:** Performance (100K signs/sec), security (128-bit), simplicity
- **Alternative:** RSA-4096 (rejected - 100x slower, larger signatures)

**ADR-003: Wave-Based Development Model**
- **Decision:** Organize roadmap into waves (foundation → governance → intelligence → ecosystem)
- **Rationale:** Clear milestones, incremental complexity, feedback integration
- **Alternative:** Waterfall (rejected - inflexible), pure agile (rejected - unclear long-term vision)

---

## Release Management

### Release Versioning

**mcp-orchestration uses semantic versioning (SemVer):**
- **Major (X.0.0):** Breaking changes (wave major version)
- **Minor (0.X.0):** New features (wave minor version)
- **Patch (0.0.X):** Bug fixes

**Wave to version mapping:**
- Wave 1.0 → v0.1.0 (minor because project <1.0)
- Wave 1.1 → v0.2.0
- Wave 1.2 → v0.3.0
- Wave 2.0 → v1.0.0 (major - first production release)

### Release Checklist

**Create:** `releases/vX.Y.Z-checklist.md`

```markdown
# Release vX.Y.Z Checklist

**Wave:** Wave X.Y
**Target Date:** YYYY-MM-DD
**Release Manager:** [Name]

---

## Pre-Release

### Development
- [ ] All deliverables complete
- [ ] All tests passing (≥85% coverage)
- [ ] No P0/P1 bugs
- [ ] Performance benchmarks met

### Documentation
- [ ] User docs updated ([user-docs/](../user-docs/))
- [ ] AGENTS.md files updated
- [ ] CHANGELOG.md updated
- [ ] Release notes written

### Code Quality
- [ ] Linting passes (`just lint`)
- [ ] Type checking passes (`just typecheck`)
- [ ] Pre-merge checks pass (`just pre-merge`)

---

## Release

### Versioning
- [ ] Version bumped in `pyproject.toml`
- [ ] Version bumped in `__init__.py`
- [ ] Git tag created (`vX.Y.Z`)

### Build
- [ ] Distribution packages built (`just build`)
- [ ] Packages validated (`twine check dist/*`)
- [ ] TestPyPI upload successful (`just publish-test`)

### Publish
- [ ] PyPI upload (`just publish-prod`)
- [ ] GitHub release created
- [ ] Release notes attached

---

## Post-Release

### Communication
- [ ] Announcement on GitHub Discussions
- [ ] Update README.md if needed
- [ ] Update ROADMAP.md (mark wave delivered)

### Monitoring
- [ ] Monitor PyPI downloads
- [ ] Watch for bug reports
- [ ] Track user feedback

### Planning
- [ ] Retrospective completed
- [ ] Next wave planning started

---

**End of Release Checklist**
```

---

## Sprint Planning (Agile)

### Sprint Structure

**If using agile sprints:**
- **Sprint length:** 2 weeks
- **Sprint goal:** Aligned with current wave deliverables
- **Sprint planning:** Define sprint backlog from wave deliverables

### Sprint Planning Template

**File:** `sprints/sprint-XX-YYYY-MM-DD.md`

```markdown
# Sprint XX: [Sprint Goal]

**Dates:** YYYY-MM-DD to YYYY-MM-DD
**Wave:** Wave X.Y
**Sprint Goal:** [1 sentence describing sprint focus]

---

## Sprint Backlog

| Task | Owner | Estimate | Status |
|------|-------|----------|--------|
| [Task 1] | [Name] | X points | Not Started |
| [Task 2] | [Name] | X points | In Progress |
| [Task 3] | [Name] | X points | Complete |

---

## Definition of Done

- [ ] All tasks completed
- [ ] Tests written and passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Demo prepared

---

## Risks

- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

---

**End of Sprint Plan**
```

### Sprint Retrospective

**After each sprint, document:**
- What went well
- What could improve
- Action items for next sprint

**File:** `sprints/sprint-XX-retrospective.md`

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Wave started
emit_event("project.wave_started", status="pending",
           metadata={"wave": "1.1", "theme": "Server Catalog"})

# Wave completed
emit_event("project.wave_completed", status="success",
           metadata={"wave": "1.1", "deliverables_count": 5})

# ADR created
emit_event("project.adr_created", status="success",
           metadata={"adr_id": "ADR-001", "title": "Content-Addressable Storage"})

# Release published
emit_event("project.release_published", status="success",
           metadata={"version": "0.2.0", "wave": "1.1"})

# Sprint completed
emit_event("project.sprint_completed", status="success",
           metadata={"sprint": 5, "velocity": 23, "goal_met": True})
```

**Create knowledge notes for:**
- Wave planning decisions (why we prioritized certain features)
- ADR rationale (deeper context beyond ADR doc)
- Release retrospectives (learnings from releases)
- Strategic pivots (why we changed direction)

**Tag pattern:** `project`, `planning`, `wave-X.Y`, `adr`, `release`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Project overview
- **[../ROADMAP.md](../ROADMAP.md)** - Long-term roadmap
- **[WAVE_1X_PLAN.md](WAVE_1X_PLAN.md)** - Current wave planning
- **[../dev-docs/AGENTS.md](../dev-docs/AGENTS.md)** - Contributing workflows
- **[../dev-docs/vision/AGENTS.md](../dev-docs/vision/AGENTS.md)** - Vision documents

---

## Common Tasks for Agents

### Task 1: Check Current Wave Status

```bash
# Read current wave plan
cat project-docs/WAVE_1X_PLAN.md

# Check roadmap for overall progress
cat ROADMAP.md
```

### Task 2: Plan Next Wave

1. Review current wave completion status
2. Identify next wave theme from roadmap
3. Create `WAVE_XX_PLAN.md` using template above
4. Break down capabilities into deliverables
5. Estimate effort and timeline
6. Document risks and mitigations

### Task 3: Document Architecture Decision

1. Identify decision requiring documentation
2. Create `decisions/YYYYMMDD-title.md` using ADR template
3. Document context, decision, rationale, alternatives
4. List consequences (positive, negative, neutral)
5. Get team review and approval
6. Update ADR status to "Accepted"

### Task 4: Prepare for Release

1. Create release checklist from template
2. Verify all pre-release items complete
3. Update version numbers
4. Build and test packages
5. Write release notes
6. Publish to PyPI
7. Create GitHub release
8. Complete post-release tasks

### Task 5: Sprint Planning

1. Review wave deliverables
2. Select tasks for upcoming sprint
3. Create sprint planning document
4. Define sprint goal aligned with wave
5. Estimate tasks and assign owners
6. Conduct daily standups (track progress)
7. Complete sprint retrospective

---

## Decision Framework for Agents

**When working on mcp-orchestration, agents should:**

1. **Check current wave:** Read [WAVE_1X_PLAN.md](WAVE_1X_PLAN.md) to understand current focus
2. **Align with wave goals:** Ensure work contributes to current wave deliverables
3. **Respect wave boundaries:** Don't implement Wave 2+ features during Wave 1
4. **Document decisions:** Create ADRs for significant architectural choices
5. **Track progress:** Update wave plan with deliverable status
6. **Plan incrementally:** Focus on current wave, refine next wave as you learn

**Example decision:**
- **Question:** Should I implement policy engine for config validation?
- **Check roadmap:** Policy engine is Wave 2 (Governance), we're in Wave 1.1
- **Decision:** No - focus on Wave 1.1 server catalog instead
- **Alternative:** Document idea in Wave 2 planning notes for future consideration

---

**End of Project Planning & Management Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or consult the roadmap at [../ROADMAP.md](../ROADMAP.md).
