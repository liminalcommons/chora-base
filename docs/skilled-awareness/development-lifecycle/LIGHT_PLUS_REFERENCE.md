---
sap_id: SAP-012
version: 1.5.0
status: Active
last_updated: 2025-11-06
type: reference
audience: developers, ai-agents
---

# Light+ Planning Model - Quick Reference

**Part of SAP-012: Development Lifecycle**

## Quick Overview

| Construct | Owner | Cadence | Artifact | Phase |
|-----------|-------|---------|----------|-------|
| **Strategy** | Product/Tech Lead | Quarterly | ROADMAP.md | Phase 1 |
| **Releases** | PM/Scrum Master | Per sprint (1-2 weeks) | Sprint docs, trackers | Phase 2 |
| **Features** | Feature Owner/Dev | Per feature | DDD docs, BDD scenarios | Phase 2-3 |
| **Tasks** | Individual Contributors | Daily | .beads/issues.jsonl | Phase 2-8 |

---

## The 4 Constructs

```
Strategy (WHAT to achieve)
    ↓
Releases (WHEN to deliver)
    ↓
Features (WHAT capabilities)
    ↓
Tasks (HOW to build)
```

**Key Principle**: Planning constructs define **WHAT** we build, 8-phase lifecycle defines **HOW** we build it.

---

## Maturity Assessment

### Quick Maturity Check

**Strategy (Construct 1)**:
- [ ] ROADMAP.md exists with strategic vision
- [ ] Quarterly strategic themes documented (3-5 themes)
- [ ] Success metrics defined and measurable
- [ ] Strategy actively guides release planning decisions

**Releases (Construct 2)**:
- [ ] Consistent sprint cadence (1-2 weeks)
- [ ] Sprint planning documents exist
- [ ] Features grouped into release milestones
- [ ] Velocity and burndown tracking active

**Features (Construct 3)**:
- [ ] DDD workflow used for all features
- [ ] Feature specs created before implementation
- [ ] Acceptance criteria defined (BDD scenarios)
- [ ] Features explicitly linked to releases

**Tasks (Construct 4)**:
- [ ] Task tracking system in place (Beads or equivalent)
- [ ] Tasks broken down to 2-8 hour chunks
- [ ] Dependencies tracked between tasks
- [ ] Tasks explicitly linked to features

### SAP Maturity Levels

| Level | Description | Strategy | Releases | Features | Tasks |
|-------|-------------|----------|----------|----------|-------|
| **L0** | None | No planning | Ad-hoc | Code-first | No tracking |
| **L1** | Basic | ROADMAP exists | Sprint structure | Descriptions | Task list |
| **L2** | Configured | Quarterly docs | Consistent cadence | Pre-implementation docs | Structured tracking |
| **L3** | Active | Guides releases | Integrated with strategy | DDD/BDD/TDD workflow | Linked to features |
| **L4** | Deep | Integrated feedback | Automated metrics | Metrics + retrospectives | Velocity tracking |
| **L5** | Mature | Predictive modeling | Optimized cadence | Reusable patterns | AI-assisted |

**Overall SAP-012 Maturity**: Minimum of all 4 constructs + 8-phase execution

---

## Common Planning Patterns

### Pattern 1: Strategy-First Planning

**Use when**: Starting new quarter, major strategic shift, or new product

```
1. Quarterly: Define strategic themes (Phase 1)
   └─ Review metrics from previous quarter
   └─ Identify 3-5 strategic themes
   └─ Set measurable success criteria
   └─ Document in ROADMAP.md

2. Monthly: Alignment check
   └─ Review current releases against strategy
   └─ Adjust priorities if needed

3. Per sprint: Feature selection (Phase 2)
   └─ Select features that align with themes
   └─ Create sprint goal tied to strategy

4. Daily: Task execution (Phase 4-8)
   └─ Execute tasks within features
```

### Pattern 2: Bottom-Up Validation

**Use when**: Ensuring tactical work aligns with strategy

```
1. Collect completed tasks
   └─ Review .beads/issues.jsonl

2. Verify task → feature alignment
   └─ Do tasks contribute to planned features?

3. Verify feature → release alignment
   └─ Do features support release goals?

4. Verify release → strategy alignment
   └─ Do releases advance strategic themes?

5. Course-correct if misalignment found
```

### Pattern 3: Incremental Adoption

**Use when**: New team adopting Light+ model, or forking template

```
1. Start with Tasks only (L1)
   └─ Install Beads, track daily work
   └─ Build habit of task tracking

2. Add Feature planning (L2)
   └─ Create feature specs before coding
   └─ Link tasks to features
   └─ Use DDD workflow

3. Add Release planning (L2-L3)
   └─ Create sprint goals
   └─ Group features into releases
   └─ Track velocity

4. Add Strategy layer (L3-L4)
   └─ Define quarterly themes
   └─ Link releases to strategy
   └─ Integrate retrospectives
```

### Pattern 4: Agile Sprint Integration

**Use when**: Following Scrum or similar agile methodology

```
Sprint Start (Day 1):
├─ Review strategy alignment
├─ Plan sprint (Phase 2)
│  └─ Select features from roadmap
│  └─ Break features into tasks
│  └─ Estimate capacity (≤80%)
└─ Create sprint goal

Mid-Sprint (Day 3-5):
├─ Daily standups (task-level)
├─ Adjust priorities if needed
└─ Address blockers

Sprint End (Day 7-10):
├─ Demo completed features
├─ Retrospective (what worked/didn't)
├─ Update metrics
└─ Plan next sprint
```

---

## Planning Workflows

### Quarterly Planning (Strategy)

**Duration**: 2-4 hours
**Participants**: Product Lead, Tech Lead, key stakeholders

```bash
# 1. Review previous quarter
python scripts/sap-evaluator.py SAP-012  # Check SAP maturity
# Review metrics, velocity, completion rates

# 2. Define strategic themes
# Edit ROADMAP.md
# - Add 3-5 strategic themes for next quarter
# - Set measurable success criteria
# - Identify capability waves

# 3. Communicate strategy
# Share with team
# Update docs/project-docs/ with strategic plans
```

### Sprint Planning (Releases)

**Duration**: 1-2 hours
**Participants**: Scrum Master, Dev Team

```bash
# 1. Review strategic themes
cat ROADMAP.md

# 2. Select features for sprint
# Based on:
# - Strategic alignment
# - Dependencies
# - Team capacity (≤80%)

# 3. Break features into tasks
bd create "Implement feature X - task 1"
bd create "Implement feature X - task 2"
# Link to feature in task description

# 4. Estimate and commit
# Use Fibonacci: 1, 2, 3, 5, 8, 13 hours
# Total ≤ 80% of available capacity
```

### Feature Planning (Features)

**Duration**: 30-60 minutes per feature
**Participants**: Feature Owner, Developers

```bash
# 1. Define user value (Phase 2)
# Create feature spec (or use DDD worksheet)
# - Problem statement
# - User stories
# - Acceptance criteria

# 2. Domain modeling (Phase 3 - DDD)
# Follow docs/dev-docs/workflows/DDD_WORKFLOW.md
# - Identify entities, value objects
# - Map relationships
# - Design APIs

# 3. Break into tasks (Phase 2)
bd create "Feature X - implement entity model"
bd create "Feature X - write BDD scenarios"
bd create "Feature X - implement TDD tests"
# Link tasks to feature spec

# 4. Add to sprint backlog
# Link feature to release/sprint
```

### Daily Task Execution (Tasks)

**Duration**: Throughout day
**Participants**: Individual Contributors

```bash
# Morning: Pick task
bd list --status=todo
bd start <task-id>

# Development: Execute using 8-phase lifecycle
# Phase 4-8: BDD/TDD → Testing → Review → etc.

# Throughout: Update status
bd comment <task-id> "Progress update"

# Evening: Mark complete
bd done <task-id>

# Log learnings
echo '{"event":"task_complete","task":"X","learnings":"Y"}' \
  >> .chora/memory/events/development.jsonl
```

---

## Tools & Integration

### Strategy Layer
- **ROADMAP.md**: Strategic vision and capability waves
- **docs/project-docs/vision/**: Detailed vision documents
- **.chora/memory/knowledge/notes/**: Strategic analysis documents
- **SAP-019**: Self-Evaluation Framework (roadmap generation)

### Release Layer
- **Sprint planning docs**: Per-sprint planning artifacts
- **docs/project-docs/sprints/**: Weekly progress tracking
- **ROADMAP.md**: Version milestones

### Feature Layer
- **DDD worksheets**: Domain modeling (Phase 3)
- **BDD scenarios**: Behavioral specifications (Phase 4)
- **ADRs**: Architecture Decision Records
- **docs/dev-docs/workflows/**: Process documentation

### Task Layer
- **Beads (SAP-015)**: Task tracking system
- **.beads/issues.jsonl**: Task database
- **bd CLI**: `bd create`, `bd list`, `bd start`, `bd done`

---

## Integration Commands

### Check Planning Health
```bash
# Overall SAP maturity
python scripts/sap-evaluator.py

# Specific deep dive
python scripts/sap-evaluator.py --deep SAP-012

# Check task status
bd list

# Review roadmap
cat ROADMAP.md
```

### Create Planning Artifacts
```bash
# Quarterly strategy
vim ROADMAP.md  # Update strategic themes

# Sprint planning
vim docs/project-docs/sprints/week-$(date +%W).md

# Feature planning
# Follow docs/dev-docs/workflows/DDD_WORKFLOW.md

# Task creation
bd create "Task description"
```

### Validate Alignment
```bash
# Tasks → Features: Check task descriptions link to features
bd list | grep -i "feature"

# Features → Releases: Check ROADMAP.md links features to versions
cat ROADMAP.md

# Releases → Strategy: Check sprint goals align with strategic themes
cat docs/project-docs/sprints/week-*.md
```

---

## Metrics & Tracking

### Strategy Metrics (Quarterly)
- Strategic theme completion rate (%)
- Success criteria achievement
- Strategic alignment score (releases supporting themes)

### Release Metrics (Per Sprint)
- Sprint velocity (story points or hours)
- Sprint completion rate (%)
- Feature delivery rate

### Feature Metrics (Per Feature)
- Time from DDD → Done
- Acceptance criteria met (%)
- Defect rate per feature

### Task Metrics (Daily)
- Task completion rate
- Estimate accuracy (estimated vs. actual)
- Blocked task count

---

## Quick Checklist: Am I Using Light+ Correctly?

**Daily**:
- [ ] Tasks linked to features (not just random work)
- [ ] Using BDD/TDD workflow (Phase 4)
- [ ] Updating task status regularly

**Weekly (Per Sprint)**:
- [ ] Sprint goal defined
- [ ] Features selected based on strategy
- [ ] Capacity ≤80% of available time
- [ ] Retrospective held (learnings captured)

**Monthly**:
- [ ] Review strategic alignment
- [ ] Adjust priorities if misalignment detected
- [ ] Update metrics

**Quarterly**:
- [ ] Review previous quarter metrics
- [ ] Update strategic themes in ROADMAP.md
- [ ] Communicate strategy to team
- [ ] Assess SAP maturity levels

---

## Troubleshooting

### Problem: Tasks don't link to features
**Solution**: Add feature reference to task description or metadata
```bash
bd create "Feature: User Auth - implement OAuth2 flow"
```

### Problem: Features not aligned with releases
**Solution**: Review ROADMAP.md, ensure each version lists features
```markdown
### v0.2.0
**Features**:
- OAuth2 Authentication
- Data Export
```

### Problem: Releases not aligned with strategy
**Solution**: Review sprint planning, ensure features advance strategic themes
```
Strategic Theme: "Security & Privacy"
└─ Release v0.2.0
   └─ Feature: OAuth2 Authentication ✓
```

### Problem: Don't know current maturity level
**Solution**: Run SAP evaluation
```bash
python scripts/sap-evaluator.py            # Quick check (30 seconds)
python scripts/sap-evaluator.py --deep SAP-012  # Deep dive (5 minutes)
```

---

## See Also

- **[protocol-spec.md](protocol-spec.md)** - Complete SAP-012 protocol specification
- **[protocol-spec.md - Section 2.3](protocol-spec.md#23-light-planning-construct-hierarchy)** - Light+ technical documentation
- **[awareness-guide.md](awareness-guide.md)** - Agent operating patterns for SAP-012
- **[capability-charter.md](capability-charter.md)** - SAP-012 problem statement and solution design
- **[adoption-blueprint.md](adoption-blueprint.md)** - Step-by-step SAP-012 installation guide
- **SAP-015 Documentation** - [docs/skilled-awareness/task-tracking/](../task-tracking/) - Beads task tracking system
- **SAP-019 Documentation** - [docs/skilled-awareness/sap-self-evaluation/](../sap-self-evaluation/) - Self-Evaluation Framework

---

**Last Updated**: 2025-11-06
**SAP Version**: SAP-012 v1.1 (Light+ Extension)
**Maintained By**: chora-base project
