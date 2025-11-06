---
id: milestone-{version}
type: roadmap-milestone
version: v1.X.0
target_date: YYYY-MM-DD
from_vision_wave: 1
committed: true
linked_to:
  - vision-{project}-{horizon}
  - beads-epic-{id}
tags: [roadmap, milestone, {version}, {theme}]
created: YYYY-MM-DDTHH:MM:SSZ
updated: YYYY-MM-DDTHH:MM:SSZ
---

# Roadmap Milestone: {version} - {Theme Name}

## Overview

**Version**: {version} (e.g., v1.5.0)

**Target Date**: {YYYY-MM-DD}

**From Vision**: Wave {1|2|3} (Committed | Exploratory | Aspirational)

**Status**: {Planned | In Progress | Completed | Delayed}

**Theme**: {Strategic theme this milestone addresses}

---

## Features (from Vision Wave {N})

### Feature 1: {Feature Name}

**Related SAP**: {SAP-XXX}

**Description**: {2-3 sentence description from vision document}

**Success Criteria**:
- ✅ {Measurable criterion 1}
- ✅ {Measurable criterion 2}
- ✅ {Measurable criterion 3}

**Effort Estimate**: {X-Y hours}

**Completion Status**: {Not Started | In Progress | Completed}

---

### Feature 2: {Feature Name}

**Related SAP**: {SAP-YYY}

**Description**: {Description}

**Success Criteria**:
- ✅ {Criterion 1}
- ✅ {Criterion 2}

**Effort Estimate**: {X-Y hours}

**Completion Status**: {Status}

---

## Success Criteria (Overall Milestone)

**Milestone succeeds if**:
- ✅ {Overall success criterion 1}
- ✅ {Overall success criterion 2}
- ✅ {Overall success criterion 3}
- ✅ {Overall success criterion 4}

**Metrics**:
- **Metric 1**: {What to measure} - Target: {value}
- **Metric 2**: {What to measure} - Target: {value}
- **Metric 3**: {What to measure} - Target: {value}

---

## Linked Beads Epic

**Epic ID**: {beads-epic-id}

**Epic Title**: "{Theme Name} (v{version})"

**Tasks**: {N} tasks (estimated)

**Task Breakdown**:
- **Feature 1**: {M} tasks
  - Task 1: {Task title}
  - Task 2: {Task title}
  - ...
- **Feature 2**: {M} tasks
  - Task 1: {Task title}
  - Task 2: {Task title}
  - ...

**Progress**: {XX}% complete ({completed}/{total} tasks)

**Beads CLI Commands**:
```bash
# View epic details
bd show {beads-epic-id}

# List epic tasks
bd list --parent {beads-epic-id}

# Find unblocked work
bd ready --parent {beads-epic-id} --json
```

---

## Dependencies

### Blockers
- ❌ {Blocker 1 - what blocks this milestone}
- ❌ {Blocker 2}

**Resolution Plan**:
- {How to unblock blocker 1}
- {How to unblock blocker 2}

### Enables
- ✅ {What this milestone enables for future work}
- ✅ {Future capability unlocked by this milestone}

---

## Integration with Other SAPs

**SAP-XXX ({SAP Name})**:
- Integration point: {How this milestone integrates}
- Data flow: {What data/artifacts flow between SAPs}

**SAP-YYY ({SAP Name})**:
- Integration point: {Integration description}
- Data flow: {Data exchange}

---

## Traceability

**Upstream** (where this milestone came from):
- **Vision Document**: `vision-{project}-{horizon}.md` (Wave {N})
- **Strategic Theme Matrix**: `strategic-themes-{date}.md` (Theme {N})
- **Intention Inventory**: `intention-inventory-{date}.md` ({N} intentions)

**Downstream** (what this milestone creates):
- **Beads Epic**: {beads-epic-id} ({N} tasks)
- **Beads Tasks**: Individual tasks decomposed from epic
- **Git Commits**: Code changes for milestone features
- **Release Notes**: {version} release documentation

**Query Traceability**:
```bash
# Find vision document linked to this milestone
grep "linked_to.*milestone-{version}" .chora/memory/knowledge/notes/vision-*.md

# Find beads epic linked to this milestone
grep "beads-epic-" .chora/memory/knowledge/notes/milestone-{version}.md

# Show beads epic
bd show $(grep -o 'beads-epic-[a-z0-9-]*' .chora/memory/knowledge/notes/milestone-{version}.md)
```

---

## Timeline

| Phase | Date | Status |
|-------|------|--------|
| **Milestone Created** | {YYYY-MM-DD} | ✅ Complete |
| **Beads Epic Created** | {YYYY-MM-DD} | ✅ Complete |
| **Development Start** | {YYYY-MM-DD} | {Status} |
| **Feature 1 Complete** | {YYYY-MM-DD} | {Status} |
| **Feature 2 Complete** | {YYYY-MM-DD} | {Status} |
| **Testing & Validation** | {YYYY-MM-DD} | {Status} |
| **Release** | {YYYY-MM-DD} (target) | {Status} |

---

## Risk Assessment

### High-Risk Areas
- **Risk 1**: {Risk description}
  - **Probability**: {Low | Medium | High}
  - **Impact**: {Low | Medium | High}
  - **Mitigation**: {How to mitigate this risk}

- **Risk 2**: {Risk description}
  - **Probability**: {Low | Medium | High}
  - **Impact**: {Low | Medium | High}
  - **Mitigation**: {Mitigation strategy}

### Contingency Plans
- If {risk occurs}, then {contingency action}
- If timeline slips by >2 weeks, then {descope strategy}

---

## Changelog

### {YYYY-MM-DD} - Milestone Created
- Created from vision Wave {N} features
- Beads epic {epic-id} created with {N} estimated tasks
- Target date: {YYYY-MM-DD}

### {YYYY-MM-DD} - Development Started
- Feature {N} implementation began
- {Progress update}

### {YYYY-MM-DD} - Feature {N} Completed
- {Feature name} completed
- Success criteria validated: {list criteria met}
- {N}/{total} features complete

### {YYYY-MM-DD} - Milestone Delivered
- All features completed and tested
- Success criteria met: {X}/{X}
- Released as {version} on {date}

---

## Example: Chora-Base v1.5.0 Milestone (Strategic Planning Infrastructure)

**Note**: This example shows how the template is used in practice.

---
id: milestone-v1.5.0
type: roadmap-milestone
version: v1.5.0
target_date: 2026-02-01
from_vision_wave: 1
committed: true
linked_to:
  - vision-chora-base-6-month
  - beads-epic-chora-base-xyz
tags: [roadmap, milestone, v1.5.0, strategic-planning]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Roadmap Milestone: v1.5.0 - Strategic Planning Infrastructure

**Target Date**: 2026-02-01 (Feb 1, 2026)

**From Vision**: Wave 1 (Committed)

**Status**: Planned

## Features (from Vision Wave 1)

### SAP-010: Strategic Knowledge Templates

**Description**: Add 4 templates (vision, intention inventory, roadmap milestone, strategic theme matrix) to enable systematic storage of strategic planning artifacts.

**Success Criteria**:
- ✅ 4 templates exist in `.chora/memory/templates/`
- ✅ Templates have complete YAML frontmatter with `type` field
- ✅ Templates reusable across ecosystem projects
- ✅ Integration with SAP-006, SAP-015, SAP-027 validated

**Effort**: 4-6 hours

---

### SAP-006: Vision Synthesis Workflow

**Description**: 4-phase workflow (discovery → analysis → drafting → cascade) for evidence-based vision creation with multi-timeframe horizons (3/6/12-month waves).

**Success Criteria**:
- ✅ Workflow reduces vision synthesis time from days to hours
- ✅ Evidence-based decision criteria validated (70% A+B threshold)
- ✅ Multi-wave planning enables exploratory validation
- ✅ Integration with SAP-010 templates and SAP-015 backlog cascade

**Effort**: 8-12 hours

---

### SAP-015: Backlog Organization Patterns

**Description**: Multi-tier backlog (P0-P4) with vision → backlog cascade, epic decomposition patterns, and backlog refinement workflows.

**Success Criteria**:
- ✅ Vision cascade creates roadmap milestones linked to beads epics
- ✅ Epic decomposition patterns documented and validated
- ✅ Backlog health metrics tracked (age, blocked ratio, priority distribution)
- ✅ Quarterly refinement workflow established

**Effort**: 6-10 hours

---

### SAP-027: Pre-Pilot Discovery Phase

**Description**: Week -1 discovery phase for pilot selection using intention inventory and evidence-based prioritization.

**Success Criteria**:
- ✅ Pilot selection criteria validated (evidence ≥70% A+B, user demand ≥10)
- ✅ Intention prioritization workflow integrated with SAP-010
- ✅ Pilot → vision feedback loop established
- ✅ Dogfooding results feed back to quarterly vision review

**Effort**: 4-6 hours

---

## Success Criteria (v1.5.0)

- ✅ All 4 SAPs enhanced with strategic planning capabilities
- ✅ Workflow pipeline validated through dogfooding in chora-base
- ✅ Ecosystem can consolidate intentions → vision → backlog
- ✅ Templates reusable across ecosystem projects (validated in 2+ projects)
- ✅ Integration between SAPs tested (vision → backlog, pilot → backlog)

**Metrics**:
- **Vision synthesis time**: Reduced from 40 hours → 4 hours (10x improvement)
- **Template reusability**: Used in 3+ ecosystem projects
- **Evidence quality**: ≥70% Level A+B for Wave 1 features

---

## Linked Beads Epic

**Epic ID**: chora-base-xyz (to be created after approval)

**Tasks**: 20 tasks (estimated)
- SAP-010: 5 tasks (4 templates + 3 doc updates)
- SAP-006: 6 tasks (4-phase workflow + docs)
- SAP-015: 5 tasks (multi-tier backlog + cascade + docs)
- SAP-027: 4 tasks (discovery phase + integration + docs)

**Progress**: 0% (not started)

---

## Dependencies

**Blockers**: None (foundational work, no external dependencies)

**Enables**:
- Ecosystem strategic planning adoption (Wave 2)
- Automated tooling for vision synthesis (Wave 2)
- Multi-project roadmap coordination (Wave 3)

---

## Integration with Other SAPs

**SAP-010 ↔ SAP-006**: Vision synthesis uses strategic templates
**SAP-010 ↔ SAP-015**: Roadmap milestones link to beads epics
**SAP-010 ↔ SAP-027**: Pre-pilot discovery reads intention inventory
**SAP-006 → SAP-015**: Vision cascade creates roadmap milestones and epics
**SAP-027 → SAP-006**: Dogfooding feedback updates vision Wave 2 decisions

---

## Timeline

| Phase | Date | Status |
|-------|------|--------|
| Milestone Created | 2025-11-05 | ✅ Complete |
| Beads Epic Created | 2025-11-05 | Pending |
| SAP-010 Development | 2025-11-06 | Planned |
| SAP-006 Development | 2025-11-10 | Planned |
| SAP-015 Development | 2025-11-15 | Planned |
| SAP-027 Development | 2025-11-20 | Planned |
| Testing & Validation | 2026-01-15 | Planned |
| Release v1.5.0 | 2026-02-01 | Planned (target) |

---

## Usage Instructions

### How to Use This Template

1. **Copy Template** (after vision Wave 1 finalized):
   ```bash
   cp .chora/memory/templates/roadmap-milestone-template.md \
      .chora/memory/knowledge/notes/milestone-{version}.md
   ```

2. **Fill Frontmatter**:
   - `id`: milestone-{version}
   - `version`: Target semantic version (e.g., v1.5.0)
   - `target_date`: Release date (YYYY-MM-DD)
   - `from_vision_wave`: Which wave (1 = committed, 2 = exploratory)
   - `committed`: true if Wave 1, false if Wave 2/3
   - `linked_to`: Start with vision document ID only
   - `tags`: [roadmap, milestone, {version}, {theme}]

3. **List Features** (from vision Wave):
   - Copy features from vision document Wave section
   - Include description, success criteria, effort estimate
   - Add completion status (not started initially)

4. **Define Overall Success Criteria**:
   - What makes this milestone successful as a whole?
   - Define measurable metrics (time savings, adoption, quality)

5. **Create Beads Epic**:
   ```bash
   bd create "Wave 1: {Theme} (v{version})" \
     --priority 1 \
     --type epic \
     --description "From vision-{project}-{horizon} Wave 1"
   ```

6. **Link Epic to Milestone**:
   - Get epic ID from beads: `bd list --type epic | grep "{version}"`
   - Update `linked_to` array: Add `beads-epic-{id}`
   - Fill "Linked Beads Epic" section with task breakdown

7. **Track Progress**:
   - Update completion status as features finish
   - Update timeline as milestones hit
   - Add changelog entries for major updates

8. **After Delivery**:
   - Update status to "Completed"
   - Add final changelog entry with delivery date
   - Link to release notes

### Integration with Other Templates

**Inputs** (used to create this milestone):
- `vision-{project}-{horizon}.md` - Vision Wave 1 features
- `strategic-themes-{date}.md` - Theme that this milestone addresses
- `intention-inventory-{date}.md` - Original user intentions

**Outputs** (created from this milestone):
- Beads epic (SAP-015) with {N} tasks
- Beads tasks (decomposed from epic)
- Git commits and PRs
- Release notes for {version}

### When to Update Milestone

**Weekly**: Update feature completion status, timeline progress

**After Feature Complete**: Mark feature done, update overall progress percentage

**After Epic Task Update**: Sync beads task completion with milestone tracking

**After Delivery**: Mark milestone complete, add final changelog entry

### Traceability Queries

```bash
# Find the vision document that created this milestone
grep "linked_to.*milestone-v1.5.0" .chora/memory/knowledge/notes/vision-*.md

# Find the beads epic linked to this milestone
grep "beads-epic-" .chora/memory/knowledge/notes/milestone-v1.5.0.md

# Show epic details
epic_id=$(grep -o 'beads-epic-[a-z0-9-]*' .chora/memory/knowledge/notes/milestone-v1.5.0.md)
bd show $epic_id

# List epic tasks
bd list --parent $epic_id

# Find unblocked work in epic
bd ready --parent $epic_id --json
```
