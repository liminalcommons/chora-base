# Protocol Specification: Development Lifecycle

**SAP ID**: SAP-012
**Version**: 1.1.0
**Status**: Active
**Last Updated**: 2025-11-06

---

## 1. Overview

This protocol defines the **8-phase development lifecycle** for chora-base projects, integrating **DDD → BDD → TDD** methodologies into a unified workflow.

**Core Guarantee**: Following this lifecycle reduces defects by 40-80% (research-backed) while maintaining development velocity.

**Lifecycle**: Vision (months) → Planning (weeks) → Requirements (days) → Development (days-weeks) → Testing (hours-days) → Review (hours-days) → Release (hours) → Monitoring (continuous)

---

## 2. Architecture

### 2.1 Lifecycle Overview

```
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: VISION & STRATEGY (Months)                             │
│ Strategic roadmap, market analysis, ecosystem alignment          │
│ Documents: ROADMAP.md, vision statements                         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: PLANNING & PRIORITIZATION (Weeks)                      │
│ Sprint planning, backlog grooming, stakeholder alignment         │
│ Documents: sprint-template.md, backlog                           │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 3: REQUIREMENTS & DESIGN (Days)                           │
│ Documentation-Driven Development: Define requirements through   │
│ Diataxis-structured docs before implementation                  │
│ L2: Manual BDD | L3: Executable How-To → Extracted BDD         │
│ Documents: Diataxis docs, API specs, acceptance criteria        │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 4: DEVELOPMENT (BDD + TDD) (Days-Weeks)                   │
│ BDD: Gherkin scenarios (RED)                                    │
│ TDD: Red-Green-Refactor cycles                                  │
│ Documents: .feature files, tests/, src/                         │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 5: TESTING & QUALITY (Hours-Days)                        │
│ Unit → Smoke → Integration → E2E                                │
│ Coverage ≥85%, linting, type checking, security                 │
│ Commands: pytest, ruff, mypy, pre-commit                        │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 6: REVIEW & INTEGRATION (Hours-Days)                     │
│ Code review, docs review, CI/CD pipeline, merge                │
│ Tools: GitHub PR, CI workflows                                  │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 7: RELEASE & DEPLOYMENT (Hours)                          │
│ Version bump, changelog, build, publish PyPI, deploy prod      │
│ Scripts: bump-version.sh, prepare-release.sh, publish-prod.sh  │
└────────────────────┬─────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 8: MONITORING & FEEDBACK (Continuous)                    │
│ Metrics, user feedback, bug reports, iteration planning        │
│ Documents: PROCESS_METRICS.md, issue tracker                    │
└──────────────────────────────────────────────────────────────────┘
                     │
                     └──→ Back to PHASE 1 or PHASE 2 (continuous improvement)
```

### 2.2 Documentation-Driven Development → BDD → TDD Integration

```
Documentation-Driven Development (Phase 3)
  ↓
  L2 Pattern: Write docs manually → Write BDD scenarios manually
  L3 Pattern: Write executable how-to → Extract BDD scenarios (automated)
  ↓
  Produces: API specification + Acceptance criteria
  ↓
BDD (Behavior Driven Development)
  ↓
  Produces: Executable Gherkin scenarios (.feature files)
  Status: RED (all scenarios fail, feature not implemented)
  ↓
TDD (Test Driven Development)
  ↓
  RED-GREEN-REFACTOR cycles:
    1. Write unit test (RED)
    2. Implement minimal code (GREEN)
    3. Refactor (improve design, tests stay GREEN)
    4. Repeat until all BDD scenarios pass
  ↓
  Produces: Fully tested feature (unit tests + BDD scenarios GREEN)
```

**Note on Terminology**:
- **Documentation-Driven Development** (Phase 3): Write Diataxis-structured documentation before implementation
- **Domain-Driven Design** (DDD): Eric Evans' strategic design patterns for complex domain logic (entities, aggregates, bounded contexts) - used when domain complexity requires explicit modeling
- Both can be used together: Documentation-Driven Development for requirements, Domain-Driven Design for complex domain modeling

### 2.3 Light+ Planning Construct Hierarchy

The 8-phase lifecycle operates within a **4-level planning hierarchy** that structures work from strategic vision to daily tasks.

**Key Principle**: Planning constructs define **WHAT** we build, while the 8 phases define **HOW** we build it.

```
1. Strategy (Quarterly)
       ↓
2. Releases (Sprint-based)
       ↓
3. Features (User capabilities)
       ↓
4. Tasks (Work items)
```

---

#### 2.3.1 Construct 1: Strategy

**Purpose**: 3-6 month strategic direction
**Planned in**: Phase 1 (Vision & Strategy)
**Cadence**: Quarterly review
**Owner**: Product/Tech Lead

**Artifacts**:
- `ROADMAP.md` - Strategic vision and capability waves
- `docs/project-docs/vision/` - Vision documents
- `.chora/memory/knowledge/notes/strategic-analysis-*.md` - Strategic priorities

**Activities**:
- Define strategic themes (3-5 per quarter)
- Establish success metrics
- Identify capability waves
- Set design principles

**SAP Maturity Levels**:
- **L0**: No strategic planning
- **L1**: Basic ROADMAP.md exists
- **L2**: Quarterly strategy documented with metrics
- **L3**: Strategy actively guides release planning
- **L4**: Strategy integrated with retrospectives and feedback loops
- **L5**: Strategic planning optimized with predictive modeling

---

#### 2.3.2 Construct 2: Releases

**Purpose**: Group features into deliverable milestones
**Planned in**: Phase 2 (Planning)
**Cadence**: Per sprint (1-2 weeks) or version milestone
**Owner**: Product Manager / Scrum Master

**Artifacts**:
- Sprint planning documents
- Version milestones in ROADMAP.md
- Sprint tracking documents

**Activities**:
- Select features for release based on strategy
- Create sprint goals
- Estimate capacity (never >80%)
- Track velocity and burndown
- Link features to strategic themes

**SAP Maturity Levels**:
- **L0**: Ad-hoc releases, no planning
- **L1**: Basic sprint structure exists
- **L2**: Consistent sprint cadence with planning docs
- **L3**: Release planning integrated with strategy
- **L4**: Automated release metrics and retrospectives
- **L5**: Optimized release cadence with predictive planning

---

#### 2.3.3 Construct 3: Features

**Purpose**: User-facing capabilities to be built
**Planned in**: Phase 2 (Planning) + Phase 3 (Requirements & Design)
**Cadence**: Per feature
**Owner**: Feature Owner / Developer

**Artifacts**:
- DDD worksheets (Phase 3)
- BDD scenarios (Phase 4)
- Feature specification documents
- Architecture Decision Records (ADRs)

**Activities**:
- Define user value and acceptance criteria
- Domain modeling (DDD workflow)
- Technical design
- Break down into tasks
- Link to release milestones

**SAP Maturity Levels**:
- **L0**: No feature planning, code-first approach
- **L1**: Basic feature descriptions exist
- **L2**: Features documented before implementation
- **L3**: DDD/BDD/TDD workflow followed for all features
- **L4**: Feature specs integrated with metrics and retrospectives
- **L5**: Feature planning optimized with reusable patterns

---

#### 2.3.4 Construct 4: Tasks

**Purpose**: Day-to-day work items
**Planned in**: Phase 2 (Planning)
**Cadence**: Daily
**Owner**: Individual Contributors

**Artifacts**:
- `.beads/issues.jsonl` - Task database (SAP-015)
- Beads CLI for task management
- Task dependencies and estimates

**Activities**:
- Break features into tasks (2-8 hour chunks)
- Track status (todo → in_progress → done)
- Manage dependencies
- Log time estimates vs actuals
- Link tasks to features

**SAP Maturity Levels**:
- **L0**: No task tracking
- **L1**: Basic task list (TODO comments, issues)
- **L2**: Structured task tracking (Beads installed)
- **L3**: Tasks linked to features with dependency tracking
- **L4**: Automated task metrics and velocity tracking
- **L5**: Optimized task management with AI-assisted breakdown

---

#### 2.3.5 Integration with 8 Phases

The 4 planning constructs map to the 8 execution phases:

| Phase | Planning Constructs Used | Activities |
|-------|-------------------------|------------|
| **Phase 1: Vision & Strategy** | Strategy (Construct 1) | Define quarterly strategic themes, capability waves |
| **Phase 2: Planning** | Releases, Features, Tasks (Constructs 2-4) | Sprint planning, feature breakdown, task creation |
| **Phase 3: Requirements (DDD)** | Features (Construct 3) | Feature specification, domain modeling |
| **Phase 4: Development (BDD/TDD)** | Features, Tasks (Constructs 3-4) | Build features using tasks |
| **Phase 5-8: Testing → Monitoring** | Tasks (Construct 4) | Execute tasks, track completion |

**Planning Flows**:

**Quarterly (Strategy)**:
1. Review previous quarter metrics
2. Define strategic themes for next quarter
3. Update ROADMAP.md with capability waves
4. Set measurable success criteria

**Per Sprint (Releases)**:
1. Review strategic themes
2. Select features that align with themes
3. Create sprint goal
4. Break features into tasks
5. Estimate and commit (≤80% capacity)

**Per Feature**:
1. Define user value and acceptance criteria
2. Execute DDD workflow (domain modeling)
3. Break into tasks
4. Add to sprint backlog
5. Link to release milestone

**Daily (Tasks)**:
1. Pick task from backlog (`.beads/issues.jsonl`)
2. Execute using BDD/TDD methodology
3. Update task status
4. Log progress and learnings

---

#### 2.3.6 Benefits of Light+ Model

1. **Traceability**: Every task links to a feature → release → strategy
2. **Scalability**: Simple projects skip Strategy, complex projects use full hierarchy
3. **Fork-Friendly**: Template users adopt incrementally (L0 → L5 maturity)
4. **Clear Separation**: Planning constructs (WHAT) separate from execution phases (HOW)
5. **Maturity Tracking**: Use SAP maturity levels to track adoption depth

**Quick Reference**: See [LIGHT_PLUS_REFERENCE.md](LIGHT_PLUS_REFERENCE.md) for practical planning workflows and maturity assessment.

---

## 3. Phase Contracts

### 3.1 Phase 1: Vision & Strategy (ENHANCED)

**Time Scale**: 5-8 days (1-2 days per sub-phase)
**Frequency**: Quarterly
**Participants**: Leadership, product, engineering leads
**Objective**: Synthesize scattered user intentions into structured vision and operational backlog

**Overview**: Phase 1 has been expanded from a monolithic vision/strategy phase into **4 structured sub-phases** that systematically consolidate scattered intentions (inbox, GitHub, dogfooding, research, A-MEM) into a multi-timeframe strategic vision (3/6/12-month horizons) and cascade Wave 1 into operational backlog.

---

#### 3.1.1: Phase 1.1 - Discovery

**Duration**: 1-2 days

**Inputs**:
1. **Inbox Coordination Requests** (SAP-001): `cat inbox/coordination/active.jsonl`
2. **GitHub Issues**: `gh issue list --label feature-request,high-demand`
3. **Dogfooding Pilot Feedback** (SAP-027): `grep '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md`
4. **Research Reports**: `ls docs/research/*-research.md`
5. **A-MEM Knowledge Notes** (SAP-010): `grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md`

**Activities**:
1. Query latest intention inventory (if exists): `grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | sort | tail -1`
2. Scan inbox for new coordination requests since last inventory
3. Review GitHub issues/discussions with `feature-request` or `high-demand` labels
4. Read dogfooding pilot final summaries from SAP-027
5. Query A-MEM knowledge graph for unfulfilled user needs
6. Consolidate all intentions into inventory (SAP-010 template)
7. Categorize intentions by evidence level:
   - **Level A** (Standards): IETF RFCs, W3C specs, PEPs, peer-reviewed research
   - **Level B** (Case Studies): Production data (>100 users), industry case studies, established patterns
   - **Level C** (Expert Opinion): Blog posts, expert opinions, single-user requests, unvalidated ideas

**Output**: Intention inventory (`.chora/memory/knowledge/notes/intention-inventory-{date}.md`)

**Quality Gates**:
- ✅ All 5 sources scanned (inbox, GitHub, dogfooding, research, A-MEM)
- ✅ Each intention has: title, source, evidence citation, user demand count, related SAPs, priority
- ✅ Evidence percentages calculated (A%, B%, C%)

**Example** (chora-base Nov 2025):
- Scanned 89 unfulfilled intentions:
  - Inbox: 4 coordination requests
  - GitHub: 12 feature requests
  - Dogfooding: 3 pilot summaries (SAP-029, SAP-028, SAP-027)
  - Research: 8 research reports
  - A-MEM: 15 knowledge notes with `user-request` tag
- Evidence levels: 16% A, 35% B, 49% C
- Top intention: "Strategic Planning Workflow" (4 inbox requests, HIGH priority)

---

#### 3.1.2: Phase 1.2 - Analysis

**Duration**: 1-2 days

**Input**: Intention inventory (from Phase 1.1)

**Activities**:
1. Cluster intentions into strategic themes (pattern recognition):
   - Group by similar user needs (e.g., "Strategic Planning", "Testing & Quality", "MCP Integration")
   - Count intentions per theme
2. Calculate evidence level breakdown per theme:
   - Theme A%: (Level A intentions / total intentions in theme) × 100
   - Theme B%: (Level B intentions / total intentions in theme) × 100
   - Theme C%: (Level C intentions / total intentions in theme) × 100
   - Theme A+B%: Theme A% + Theme B%
3. Quantify user demand per theme (sum across intentions)
4. Estimate effort per theme (sum across intentions)
5. Estimate ROI potential per theme (time savings multiplier)
6. Apply Wave decision criteria:
   - **Wave 1 (Committed)**: Evidence A+B ≥ 70%, user demand ≥ 10, effort < 50 hours
   - **Wave 2 (Exploratory)**: Evidence A+B ≥ 60%, user demand ≥ 5, validate via dogfooding (SAP-027)
   - **Wave 3 (Aspirational)**: Evidence A+B < 60%, user demand < 5, defer to quarterly review
7. Rank themes by (evidence × demand × roi_potential)
8. Document in strategic theme matrix (SAP-010 template)

**Output**: Strategic theme matrix (`.chora/memory/knowledge/notes/strategic-themes-{date}.md`)

**Quality Gates**:
- ✅ All intentions assigned to themes (no orphans)
- ✅ Each theme has: intention count, evidence breakdown (A%, B%, C%), user demand, effort estimate, ROI estimate, priority, recommended wave
- ✅ Wave decision criteria applied consistently
- ✅ Top 3-5 themes identified for vision drafting

**Example** (chora-base Nov 2025):
- 42 intentions → 5 themes:
  1. **Strategic Planning Infrastructure**: 14 intentions, 79% A+B, 4 user requests → Wave 1 ✅
  2. **Testing & Quality**: 8 intentions, 75% A+B, 8 user requests → Wave 1 ✅
  3. **MCP Integration**: 6 intentions, 83% A+B, 8 user requests → Wave 2 (validate via dogfooding)
  4. **Performance Optimization**: 5 intentions, 60% A+B, 3 user requests → Wave 2 (needs more evidence)
  5. **Documentation Quality**: 4 intentions, 50% A+B, 2 user requests → Wave 3 (defer)

---

#### 3.1.3: Phase 1.3 - Vision Drafting

**Duration**: 2-3 days

**Input**: Strategic theme matrix (from Phase 1.2)

**Activities**:
1. Copy vision document template: `cp .chora/memory/templates/vision-document-template.md .chora/memory/knowledge/notes/vision-{project}-{horizon}.md`
2. Fill frontmatter:
   - `horizon`: 3-month | 6-month | 12-month
   - `waves`: Array (wave 1: committed, wave 2: exploratory, wave 3: aspirational)
   - `status`: draft (until stakeholder review)
3. Write Wave 1 (Committed - 3-month horizon):
   - Features from HIGH-priority themes (evidence A+B ≥ 70%, user demand ≥ 10)
   - Target version (e.g., v1.5.0)
   - Target date (e.g., 2026-02-01)
   - Success criteria (measurable outcomes)
   - Will be decomposed to ROADMAP.md + beads epic/tasks in Phase 1.4
4. Write Wave 2 (Exploratory - 6-month horizon):
   - Candidates from MEDIUM-priority themes (evidence A+B ≥ 60%, user demand ≥ 5)
   - Decision review date (quarterly)
   - Validation plan (dogfooding pilots via SAP-027)
   - Decision criteria (time savings ≥ 5x, satisfaction ≥ 85%, bugs = 0, adoption ≥ 2)
5. Write Wave 3 (Aspirational - 12-month horizon):
   - Long-term vision from LOW-priority themes or future possibilities
   - Quarterly review (promote to Wave 2 or deprecate)
   - May not have specific features, more directional themes
6. Review with stakeholders
7. Update `status: active` after approval

**Output**: Vision document (`.chora/memory/knowledge/notes/vision-{project}-{horizon}.md`)

**Quality Gates**:
- ✅ Wave 1 (Committed): All features have evidence A+B ≥ 70%, target version set, success criteria measurable
- ✅ Wave 2 (Exploratory): Decision review date set, validation plan defined (which dogfooding pilots)
- ✅ Wave 3 (Aspirational): Quarterly review cadence documented
- ✅ Stakeholders approved (status: active)

**Multi-Timeframe Guidance**:

**3-Month Horizon (Wave 1)**:
- **Status**: Committed in ROADMAP.md
- **Decomposed**: Beads epic + tasks (Phase 1.4)
- **Review**: Sprint planning (bi-weekly), sprint retrospective (bi-weekly)
- **Updates**: Feature scope may adjust, but version target is committed

**6-Month Horizon (Wave 2)**:
- **Status**: Exploratory
- **Validation**: Dogfooding pilot (SAP-027) - 6-week pilot per candidate
- **Decision**: Quarterly review (commit to Wave 1 in next vision, defer to Wave 3, or remove)
- **Criteria**: GO decision requires time savings ≥ 5x, satisfaction ≥ 85%, bugs = 0, adoption ≥ 2

**12-Month Horizon (Wave 3)**:
- **Status**: Aspirational
- **Review**: Quarterly (promote to Wave 2 if evidence/demand increases, deprecate if no traction)
- **Updates**: Themes may shift based on ecosystem trends, new research, changed priorities

**Example Vision Document** (chora-base Nov 2025):
```yaml
---
id: vision-chora-base-6-month
type: strategic-vision
horizon: 6-month
status: active
waves:
  - wave: 1
    status: committed
    target_version: v1.5.0
    target_date: 2026-02-01
  - wave: 2
    status: exploratory
    decision_review: 2026-Q1
---

# Vision: chora-base 6-Month (Nov 2025 - Apr 2026)

## Wave 1: Strategic Planning Infrastructure (Committed - 3 months)

**Target**: v1.5.0 (Feb 1, 2026)

**Features**:
- SAP-010: Strategic knowledge templates (vision, intention, roadmap, theme)
- SAP-006: Vision synthesis workflow (discovery → analysis → drafting → cascade)
- SAP-015: Backlog organization patterns (multi-tier, refinement, decomposition)
- SAP-027: Pre-pilot discovery phase (intention prioritization)

**Success Criteria**:
- All 4 SAPs enhanced with strategic planning capabilities
- Workflow pipeline validated through dogfooding in chora-base
- Ecosystem can consolidate intentions → vision → backlog

## Wave 2: Automation & Tooling (Exploratory - 6 months)

**Decision Review**: 2026-Q1 (after Wave 1 delivery)

**Candidates**:
- Intention discovery CLI (scripts/discover-intentions.py)
- Strategic theme clustering CLI (scripts/cluster-strategic-themes.py)
- Vision → backlog cascade CLI (scripts/cascade-vision-to-backlog.py)
- Backlog health dashboard (scripts/backlog-health.py)

**Validation Plan**: Dogfood CLIs during Wave 1 execution, collect time savings data (target ≥ 5x), GO/NO-GO decision Q1 2026

## Wave 3: Ecosystem Adoption (Aspirational - 12 months)

**Target**: 3+ ecosystem projects adopt strategic planning SAPs

**Themes**:
- Public documentation for strategic planning workflow
- Video tutorials for vision synthesis
- Case studies from ecosystem adopters
- Strategic planning SAP set (minimal-strategic-planning)
```

---

#### 3.1.4: Phase 1.4 - Backlog Cascade

**Duration**: 1 day

**Input**: Vision Wave 1 (committed) from Phase 1.3

**Activities**:
1. Update ROADMAP.md with Wave 1 features:
   - Copy features from vision Wave 1
   - Add target version, target date, success criteria
   - Link to vision document
2. Create roadmap milestone knowledge note:
   - Copy template: `cp .chora/memory/templates/roadmap-milestone-template.md .chora/memory/knowledge/notes/milestone-{version}.md`
   - Fill frontmatter: version, target_date, from_vision_wave: 1, linked_to: [vision-{project}-{horizon}]
   - List features, success criteria
3. Create beads epic from Wave 1 (SAP-015 integration):
   ```bash
   bd create "Wave 1: {Theme} (v{version})" \
     --priority 1 \
     --type epic \
     --description "From vision-{project}-{horizon} Wave 1. Features: {list}."
   ```
   - Returns epic ID (e.g., chora-base-epic-xyz)
4. Update roadmap milestone with epic ID:
   - Add to `linked_to` array: `beads-epic-{id}`
5. Decompose epic into tasks (SAP-015 patterns):
   - Research phase (P2): Spikes, API research
   - Implementation phase (P1): Core features
   - Quality phase (P1): Tests, documentation
6. Link tasks to epic:
   ```bash
   bd dep add {epic-id} blocks {task-1-id}
   bd dep add {epic-id} blocks {task-2-id}
   ...
   ```
7. Add metadata for traceability:
   ```bash
   bd update {epic-id} --metadata '{"from_vision_wave": 1, "roadmap_version": "v{version}", "vision_document": "vision-{project}-{horizon}"}'
   ```

**Output**:
- Updated ROADMAP.md (Wave 1 features)
- Roadmap milestone knowledge note (`.chora/memory/knowledge/notes/milestone-{version}.md`)
- Beads epic (chora-base-epic-{id})
- Beads tasks (P0-P2, linked to epic)

**Quality Gates**:
- ✅ ROADMAP.md updated with Wave 1 features, target version, target date, success criteria
- ✅ Roadmap milestone note created with `linked_to: [vision, beads-epic]`
- ✅ Beads epic created with `from_vision_wave: 1` metadata
- ✅ All Wave 1 features decomposed into beads tasks
- ✅ Tasks linked to epic via dependencies (`bd dep add {epic} blocks {task}`)

**Traceability Chain**:
Vision Wave 1 → ROADMAP.md → Roadmap Milestone Note → Beads Epic → Beads Tasks

**Example** (chora-base v1.5.0):
- ROADMAP.md updated with 4 SAP enhancements (SAP-010, SAP-006, SAP-015, SAP-027)
- Roadmap milestone: `milestone-v1.5.0.md` with `linked_to: [vision-chora-base-6-month, beads-epic-chora-base-xyz]`
- Beads epic: `chora-base-xyz` with metadata `{"from_vision_wave": 1, "roadmap_version": "v1.5.0"}`
- Beads tasks: 20 tasks (5 per SAP) linked to epic

---

**Phase 1 Summary**: The 4-phase vision synthesis workflow consolidates scattered intentions (Phase 1.1) → clusters into themes (Phase 1.2) → drafts multi-timeframe vision (Phase 1.3) → cascades Wave 1 into operational backlog (Phase 1.4). This systematic approach ensures evidence-based strategic planning with clear traceability from user needs to executable tasks.

---

### 3.2 Phase 2: Planning & Prioritization

**Time Scale**: Weeks (sprint cycle, typically 2 weeks)
**Frequency**: Every sprint (biweekly)
**Participants**: Product, engineering leads, team

#### Inputs
- ROADMAP.md (from Phase 1)
- Backlog items
- Previous sprint velocity
- Bug reports and user feedback

#### Activities
1. Sprint planning meeting (2 hours max with templates)
2. Backlog grooming and prioritization
3. Capacity planning (velocity-based)
4. Risk identification
5. Dependency mapping

#### Outputs
- **sprints/sprint-{NN}.md** - Sprint plan (from template)
- **Committed items** - Stories, bugs, tech debt
- **Sprint goals** - Clear, measurable objectives

#### Quality Gates
- ✅ Sprint capacity matches team velocity (±20%)
- ✅ Dependencies identified and resolved
- ✅ Sprint goals SMART (Specific, Measurable, Achievable, Relevant, Time-bound)

#### Template: Sprint Planning
**Location**: `project-docs/sprints/sprint-template.md`

**Key Sections**:
- Sprint metadata (number, dates, participants)
- Sprint goals (3-5 clear objectives)
- Committed items (user stories, bugs, tech debt)
- Stretch goals (optional, if capacity allows)
- Risks and dependencies
- Definition of Done

---

### 3.3 Phase 3: Requirements & Design (DDD)

**Time Scale**: Days (2-5 days for medium feature)
**Frequency**: Per feature
**Participants**: Engineers, product, designers

#### Inputs
- Sprint plan (from Phase 2)
- User story or feature request
- API constraints (existing architecture)

#### Activities (DDD Workflow)
1. **Write change request** (Explanation + How-To, Diataxis format)
2. **Design API** (Reference documentation, function signatures)
3. **Extract acceptance criteria** (Given-When-Then format)
4. **Get stakeholder approval** (review meeting)

#### Outputs
- **Explanation doc** - Why this feature? Problem statement, solution approach
- **Reference doc** - API specification (functions, parameters, return types)
- **Acceptance criteria** - Given-When-Then scenarios (input for BDD)

#### Quality Gates
- ✅ API design reviewed by technical lead
- ✅ Acceptance criteria complete (cover happy path + edge cases)
- ✅ Documentation passes frontmatter validation (SAP-007)
- ✅ Stakeholder approval obtained

#### DDD Workflow Example

**Step 1: Write Explanation Document** (Why?)
```markdown
---
title: Add Configuration Validation Feature
type: explanation
status: draft
audience: developers
last_updated: 2025-10-28
---

# Configuration Validation Feature

## Problem
Users frequently provide invalid configuration files, leading to
cryptic runtime errors.

## Solution
Add a `validate_config()` function that checks configuration schemas
before application startup, providing clear error messages.

## Acceptance Criteria
1. Given valid config, when validating, then return success
2. Given invalid config, when validating, then return detailed errors
3. Given missing required field, when validating, then specify field name
```

**Step 2: Write Reference Documentation** (What?)
```markdown
---
title: Configuration Validation API
type: reference
status: draft
audience: developers
last_updated: 2025-10-28
---

# Configuration Validation API

## `validate_config(config_path: str) -> ValidationResult`

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- `ValidationResult`: Object with `is_valid` (bool) and `errors` (list)

**Raises:**
- `FileNotFoundError`: If config_path doesn't exist

**Example:**
```python
result = validate_config("config.yaml")
if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
```
```

---

### 3.4 Phase 4: Development (BDD + TDD)

**Time Scale**: Days-Weeks (1-14 days depending on complexity)
**Frequency**: Per feature
**Participants**: Engineers, AI assistants

#### Part A: BDD (Behavior Driven Development)

**Time**: 1-3 hours
**Input**: Acceptance criteria (from DDD Phase 3)

**Activities**:
1. Write Gherkin scenarios (`.feature` files)
2. Implement step definitions (`steps/`)
3. Run BDD tests → Verify RED (all fail)

**Output**: Executable specifications (failing tests)

**BDD Example**:
```gherkin
# features/config_validation.feature
Feature: Configuration Validation
  As a user
  I want to validate my configuration file
  So that I catch errors before runtime

  Scenario: Valid configuration
    Given a valid configuration file "config.yaml"
    When I validate the configuration
    Then validation succeeds
    And no errors are reported

  Scenario: Missing required field
    Given a configuration file "config.yaml" missing "api_key"
    When I validate the configuration
    Then validation fails
    And error message includes "api_key is required"
```

#### Part B: TDD (Test Driven Development)

**Time**: 4 hours - 2 weeks (depending on complexity)
**Input**: API spec (DDD) + BDD scenarios

**Activities** (RED-GREEN-REFACTOR loop):
1. **RED**: Write unit test (fails)
2. **GREEN**: Implement minimal code (test passes)
3. **REFACTOR**: Improve design (tests stay green)
4. **Repeat** until all BDD scenarios pass

**Output**: Feature implemented with ≥85% coverage

**TDD Example (Cycle 1)**:

**RED** - Write failing test:
```python
# tests/test_config_validation.py
def test_validate_config_with_valid_file():
    """Test validation succeeds with valid config."""
    result = validate_config("tests/fixtures/valid_config.yaml")
    assert result.is_valid is True
    assert result.errors == []
```

**GREEN** - Implement minimal code:
```python
# src/config_validation.py
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]

def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file."""
    # Minimal implementation to pass test
    return ValidationResult(is_valid=True, errors=[])
```

**REFACTOR** - Improve design (add actual validation logic, tests stay green)

#### Quality Gates (Phase 4)
- ✅ All BDD scenarios pass (GREEN)
- ✅ All unit tests pass (GREEN)
- ✅ Coverage ≥85% (pytest --cov)
- ✅ No type errors (mypy)
- ✅ Linting passes (ruff)

---

### 3.5 Phase 5: Testing & Quality

**Time Scale**: Hours-Days (2 hours - 2 days)
**Frequency**: Per PR
**Participants**: Engineers, QA, CI/CD

#### Test Pyramid
```
        E2E (10%)
       /        \
    Integration (20%)
   /                \
  Smoke (10%)
 /                    \
Unit Tests (60%)
```

#### Activities
1. **Unit tests** - Already done in TDD (Phase 4)
2. **Smoke tests** - Quick validation (`./scripts/smoke-test.sh`, ~10 sec)
3. **Integration tests** - System interactions (`pytest tests/integration/`)
4. **E2E tests** - Full user workflows (if applicable)
5. **Coverage check** - `pytest --cov` (≥85% required)
6. **Linting** - `ruff check`
7. **Type checking** - `mypy src/ tests/`
8. **Security scan** - CodeQL (in CI)

#### Outputs
- Test results (pass/fail)
- Coverage report (HTML + terminal)
- Linting report
- Type checking report

#### Quality Gates
- ✅ All tests pass (unit, smoke, integration, E2E)
- ✅ Coverage ≥85%
- ✅ No linting errors
- ✅ No type errors
- ✅ No security vulnerabilities (CodeQL)

#### Commands
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run smoke tests (quick validation)
./scripts/smoke-test.sh

# Run integration tests only
pytest tests/integration/

# Pre-merge validation (runs all checks)
just pre-merge
```

---

### 3.6 Phase 6: Review & Integration

**Time Scale**: Hours-Days (4 hours - 3 days)
**Frequency**: Per PR
**Participants**: Reviewers, maintainers

#### Activities
1. **Code review** - Reviewer examines changes
2. **Documentation review** - Verify docs updated
3. **CI/CD pipeline** - All workflows pass (test.yml, lint.yml, security.yml)
4. **Address feedback** - Iterate on reviews
5. **Merge to main** - Squash and merge

#### Outputs
- Approved PR
- Merged code (main branch)
- Updated documentation

#### Quality Gates
- ✅ At least 1 approval from maintainer
- ✅ All CI workflows pass (test, lint, security)
- ✅ Documentation updated (if API changed)
- ✅ CHANGELOG.md updated (if user-facing change)
- ✅ No merge conflicts

#### Pull Request Checklist
```markdown
## PR Checklist
- [ ] Tests added/updated (coverage ≥85%)
- [ ] Documentation updated (API changes)
- [ ] CHANGELOG.md updated (user-facing changes)
- [ ] All CI workflows pass
- [ ] Code reviewed and approved
- [ ] No merge conflicts
```

---

### 3.7 Phase 7: Release & Deployment

**Time Scale**: Hours (1-4 hours)
**Frequency**: Per version (weekly to monthly)
**Participants**: Release manager, DevOps

#### Activities
1. **Version bump** - `./scripts/bump-version.sh <patch|minor|major>`
2. **Update CHANGELOG.md** - Add release notes
3. **Prepare release** - `./scripts/prepare-release.sh`
4. **Build distribution** - `./scripts/build-dist.sh`
5. **Publish to PyPI** - `./scripts/publish-prod.sh` (or publish-test.sh for testing)
6. **Create GitHub release** - Tag + release notes
7. **Deploy to production** - Infrastructure deployment (if applicable)

#### Outputs
- New version tag (e.g., v1.2.0)
- PyPI package published
- GitHub release created
- Production deployment (if applicable)

#### Quality Gates
- ✅ All tests pass on main branch
- ✅ Version number follows semver (MAJOR.MINOR.PATCH)
- ✅ CHANGELOG.md complete
- ✅ Release notes reviewed
- ✅ PyPI publish succeeds
- ✅ Smoke tests pass on published package

#### Semantic Versioning
- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features (backward compatible)
- **PATCH** (0.0.x): Bug fixes (backward compatible)

#### Commands
```bash
# Bump version (updates pyproject.toml, __init__.py)
./scripts/bump-version.sh patch  # 1.0.0 → 1.0.1
./scripts/bump-version.sh minor  # 1.0.1 → 1.1.0
./scripts/bump-version.sh major  # 1.1.0 → 2.0.0

# Prepare release (run tests, update CHANGELOG)
./scripts/prepare-release.sh patch

# Build distribution packages
./scripts/build-dist.sh

# Publish to test PyPI (verify before prod)
./scripts/publish-test.sh

# Publish to production PyPI
./scripts/publish-prod.sh
```

---

### 3.8 Phase 8: Monitoring & Feedback

**Time Scale**: Continuous
**Frequency**: Always on
**Participants**: All stakeholders

#### Activities
1. **Collect metrics** - Process metrics, quality metrics, velocity
2. **User feedback** - Issues, feature requests, surveys
3. **Bug triage** - Prioritize and schedule fixes
4. **Retrospectives** - Sprint retrospectives, release retrospectives
5. **Iterate** - Feed learnings back to Phase 1 or Phase 2

#### Outputs
- **PROCESS_METRICS.md** - Updated with actuals
- **Issue tracker** - Triaged bugs and feature requests
- **Retrospective notes** - Sprint retrospective, lessons learned

#### Metrics to Track

**Quality Metrics** (from PROCESS_METRICS.md):
- Defects per release: Target <3
- Test coverage: Target ≥85%
- Code review time: Target <24 hours
- CI/CD success rate: Target ≥95%

**Velocity Metrics**:
- Story points completed per sprint
- Sprint velocity trend (last 6 sprints)
- Planned vs delivered ratio: Target ≥70%

**Process Adherence Metrics**:
- DDD adoption: % features with docs-first approach
- BDD adoption: % features with Gherkin scenarios
- TDD adoption: % code written test-first

#### Feedback Loop
```
Phase 8 Monitoring
      ↓
Identify issue or opportunity
      ↓
   ┌─────────────────┐
   │ Minor fix/bug?  │ → Phase 2 (add to sprint backlog)
   │ Major feature?  │ → Phase 1 (update roadmap)
   └─────────────────┘
```

---

## 4. Integration Patterns

**Overview**: SAP-006 Development Lifecycle integrates with SAP-001 (Inbox), SAP-010 (A-MEM), SAP-015 (Beads), SAP-027 (Dogfooding) to enable end-to-end strategic planning from scattered intentions to operational backlog.

---

### 4.1 Integration with SAP-001 (Inbox Coordination Protocol)

**Integration Point**: Phase 1.1 Discovery

**Data Flow**: SAP-001 inbox → SAP-006 intention inventory

**Mechanism**:
1. Phase 1.1 Discovery reads active coordination requests: `cat inbox/coordination/active.jsonl`
2. Each coordination request mapped to intention in inventory:
   - `title`: Coordination request title
   - `source`: "inbox (coordination request {id})"
   - `evidence`: Coordination request description (usually Level B or C)
   - `user_demand`: 1 (requester) + any upvotes/comments
3. High-priority coordination requests (P0, urgent) → HIGH-priority intentions

**Example** (chora-base Nov 2025):
- COORD-2025-001 "Minimal SAP collaboration" → Intention "SAP ecosystem collaboration patterns" (HIGH priority)
- COORD-2025-003 "v1.9.0 capabilities update" → Intention "Update v1.9.0 capability docs" (MEDIUM priority)

**Benefits**:
- Coordination requests systematically evaluated (not ad-hoc)
- User demand signal captured in intention inventory
- Enables evidence-based prioritization (coordination request = Level B evidence if from established contributor)

---

### 4.2 Integration with SAP-010 (Memory System - A-MEM)

**Integration Point**: Phase 1.1-1.4 (all sub-phases)

**Data Flow**: Bidirectional
- SAP-006 → SAP-010: Creates strategic knowledge notes (intention inventory, theme matrix, vision document, roadmap milestone)
- SAP-010 → SAP-006: Provides strategic templates, stores vision artifacts for quarterly review

**Mechanism**:

**Phase 1.1 Discovery**:
- Copy template: `cp .chora/memory/templates/intention-inventory-template.md .chora/memory/knowledge/notes/intention-inventory-{date}.md`
- Query existing intentions: `grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md`
- Query dogfooding feedback: `grep '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md`

**Phase 1.2 Analysis**:
- Copy template: `cp .chora/memory/templates/strategic-theme-matrix-template.md .chora/memory/knowledge/notes/strategic-themes-{date}.md`
- Link to input: `input_inventory: intention-inventory-{date}` in frontmatter

**Phase 1.3 Vision Drafting**:
- Copy template: `cp .chora/memory/templates/vision-document-template.md .chora/memory/knowledge/notes/vision-{project}-{horizon}.md`
- Store with `type: strategic-vision` for queryability

**Phase 1.4 Backlog Cascade**:
- Copy template: `cp .chora/memory/templates/roadmap-milestone-template.md .chora/memory/knowledge/notes/milestone-{version}.md`
- Link to vision: `linked_to: [vision-{project}-{horizon}]` in frontmatter

**Example** (chora-base v1.5.0):
```bash
# Phase 1.1
cp .chora/memory/templates/intention-inventory-template.md \
   .chora/memory/knowledge/notes/intention-inventory-2025-11-05.md

# Phase 1.2
cp .chora/memory/templates/strategic-theme-matrix-template.md \
   .chora/memory/knowledge/notes/strategic-themes-2025-11-05.md

# Phase 1.3
cp .chora/memory/templates/vision-document-template.md \
   .chora/memory/knowledge/notes/vision-chora-base-6-month.md

# Phase 1.4
cp .chora/memory/templates/roadmap-milestone-template.md \
   .chora/memory/knowledge/notes/milestone-v1.5.0.md
```

**Benefits**:
- Standardized structure for strategic artifacts (reusable across ecosystem)
- Knowledge graph traceability (intention → theme → vision → roadmap)
- Quarterly review queries: `grep -l '"type": "strategic-vision"' .chora/memory/knowledge/notes/*.md | xargs grep -l '"status": "active"'`

---

### 4.3 Integration with SAP-015 (Task Tracking with Beads)

**Integration Point**: Phase 1.4 Backlog Cascade

**Data Flow**: SAP-006 → SAP-015 (vision Wave 1 → beads epic/tasks)

**Mechanism**:

**Step 1: Create Beads Epic**
```bash
bd create "Wave 1: Strategic Planning Infrastructure (v1.5.0)" \
  --priority 1 \
  --type epic \
  --description "From vision-chora-base-6-month Wave 1. Features: SAP-010, SAP-006, SAP-015, SAP-027 enhancements."
# Returns: chora-base-epic-xyz
```

**Step 2: Decompose Epic into Tasks**
```bash
# SAP-010 tasks
bd create "SAP-010: Create 4 strategic templates" --priority 2
bd create "SAP-010: Update protocol-spec Section 3.5" --priority 2
bd create "SAP-010: Update awareness-guide strategic section" --priority 2

# SAP-006 tasks
bd create "SAP-006: Expand Phase 1 with 4 sub-phases" --priority 2
bd create "SAP-006: Add multi-timeframe vision guidance" --priority 2
...
```

**Step 3: Link Tasks to Epic**
```bash
bd dep add chora-base-epic-xyz blocks {sap-010-task-1-id}
bd dep add chora-base-epic-xyz blocks {sap-010-task-2-id}
...
```

**Step 4: Add Traceability Metadata**
```bash
bd update chora-base-epic-xyz --metadata '{
  "from_vision_wave": 1,
  "roadmap_version": "v1.5.0",
  "vision_document": "vision-chora-base-6-month",
  "target_date": "2026-02-01"
}'
```

**Step 5: Link Roadmap Milestone to Epic**
Update roadmap milestone note:
```yaml
---
id: milestone-v1.5.0
type: roadmap-milestone
version: v1.5.0
linked_to:
  - vision-chora-base-6-month
  - beads-epic-chora-base-xyz  # Add epic ID here
---
```

**Traceability Chain**:
1. Vision Wave 1 (`vision-chora-base-6-month.md`, Wave 1 section)
2. Roadmap milestone (`milestone-v1.5.0.md`, `linked_to: [vision-..., beads-epic-...]`)
3. Beads epic (`chora-base-epic-xyz`, metadata `from_vision_wave: 1`)
4. Beads tasks (20 tasks, dependencies link to epic)

**Benefits**:
- Automatic decomposition of strategic vision into operational work
- Traceability from vision → roadmap → epic → tasks
- Agents can query: "Show me all tasks for vision Wave 1" → `bd list --json | jq '.[] | select(.metadata.from_vision_wave == 1)'`

---

### 4.4 Integration with SAP-027 (Dogfooding Patterns)

**Integration Point**: Phase 1.1 Discovery + Quarterly Vision Review

**Data Flow**: Bidirectional
- SAP-027 → SAP-006: Pilot feedback informs vision decision criteria
- SAP-006 → SAP-027: Vision Wave 2 candidates become pilot candidates

**Mechanism**:

**Phase 1.1 Discovery**: Read pilot feedback
```bash
# Query dogfooding pilot summaries
grep -l '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md

# Example: SAP-029 pilot final summary
# - Pattern: sap-generation
# - Result: GO (119x time savings, 100% satisfaction, 0 bugs, 2 adoption cases)
# - Recommendation: Formalize SAP-029, add to vision Wave 1 for v1.5.0
```

**Quarterly Vision Review**: Update Wave 2 decision criteria
```markdown
## Wave 2: Automation & Tooling (Exploratory - 6 months)

**Decision Review**: 2026-Q1 (after Wave 1 delivery)

**Candidate 1: SAP Generation Automation**
- **Status**: ✅ Validated (Pilot GO - Nov 2025)
- **Evidence**: Dogfooding pilot (SAP-029) achieved 119x time savings (target: ≥5x)
- **Satisfaction**: 100% (target: ≥85%)
- **Bugs**: 0 (target: 0)
- **Adoption**: 2 SAPs generated (SAP-029, SAP-028) (target: ≥2)
- **Decision**: **COMMIT to Wave 1 in next vision (v1.6.0)**

**Candidate 2: Intention Discovery CLI**
- **Status**: ⏳ Pending pilot (Q1 2026)
- **Validation Plan**: 6-week pilot during v1.5.0 execution
- **Decision Criteria**: Time savings ≥ 5x, satisfaction ≥ 85%, bugs = 0, adoption ≥ 2
- **Decision**: Defer to Q1 2026 review
```

**Vision Wave 2 → SAP-027 Pilot Selection**:
1. Quarterly review identifies top 1-3 Wave 2 candidates
2. Rank by (evidence × demand × roi_potential)
3. Select #1 candidate for dogfooding pilot
4. SAP-027 Week -1 Discovery reads vision Wave 2 list

**Benefits**:
- Wave 2 candidates systematically validated before committing resources
- Quarterly review updates driven by objective pilot data (not opinions)
- Tight feedback loop: pilot GO → vision Wave 1 → roadmap → backlog

---

## 5. Decision Trees

### 5.1 Which Methodology to Use?

```
What are you building?
│
├─ New feature or API?
│  │
│  ├─ Step 1: DDD (Phase 3) - Write docs first
│  │   └─ Design API, extract acceptance criteria
│  │
│  ├─ Step 2: BDD (Phase 4) - Write scenarios
│  │   └─ Convert acceptance criteria to Gherkin
│  │
│  └─ Step 3: TDD (Phase 4) - Implement
│      └─ RED-GREEN-REFACTOR until BDD scenarios pass
│
├─ Bug fix?
│  │
│  ├─ Step 1: Write failing test that reproduces bug
│  │   └─ Use TDD (unit test) or BDD (if user-facing)
│  │
│  ├─ Step 2: Fix bug (make test pass)
│  │
│  └─ Step 3: Verify fix doesn't break anything
│      └─ Run full test suite
│
├─ Refactoring existing code?
│  │
│  ├─ Step 1: Ensure tests exist (write if missing)
│  │
│  ├─ Step 2: Refactor
│  │   └─ Tests must stay GREEN throughout
│  │
│  └─ Step 3: Verify behavior unchanged
│      └─ Run full test suite
│
└─ Experimental prototype?
   └─ Skip all three (prototype first, then wrap with tests)
```

### 5.2 Time Investment by Feature Complexity

| Phase | Simple Feature | Medium Feature | Complex Feature |
|-------|----------------|----------------|-----------------|
| **DDD (Phase 3)** | 2-4 hours | 4-8 hours | 1-2 days |
| **BDD (Phase 4)** | 1-2 hours | 2-3 hours | 4-6 hours |
| **TDD (Phase 4)** | 4-8 hours | 1-2 days | 3-5 days |
| **Testing (Phase 5)** | 1-2 hours | 2-4 hours | 4-8 hours |
| **Review (Phase 6)** | 2-4 hours | 4-8 hours | 1-2 days |
| **Total** | 1 day | 2-3 days | 1-2 weeks |

**ROI**: 40-60% reduction in rework + bugs + maintenance time

---

## 6. Templates

### 6.1 Sprint Template

**Location**: `project-docs/sprints/sprint-template.md`

**Usage**: Copy template at sprint start, fill in details

**Sections**:
1. Sprint metadata (number, dates, participants)
2. Sprint goals (3-5 SMART objectives)
3. Committed items (stories, bugs, tech debt with story points)
4. Stretch goals (optional items if capacity allows)
5. Risks and dependencies
6. Definition of Done
7. Daily standup notes
8. Sprint retrospective (completed at sprint end)

### 6.2 Release Template

**Location**: `project-docs/releases/release-template.md`

**Usage**: Copy template before release, fill in details

**Sections**:
1. Release metadata (version, date, release manager)
2. Release goals (what's included in this release)
3. Features (new functionality)
4. Bug fixes (resolved issues)
5. Breaking changes (if any, MAJOR version only)
6. Upgrade guide (if breaking changes)
7. Known issues (unresolved bugs)
8. Release checklist (pre-release validation)

### 6.3 Process Metrics Template

**Location**: `project-docs/metrics/PROCESS_METRICS.md`

**Usage**: Update monthly, track trends

**Metrics Categories**:
1. **Quality Metrics**: Defects per release, test coverage, code review time
2. **Velocity Metrics**: Story points per sprint, velocity trend, planned vs delivered
3. **Process Adherence**: DDD/BDD/TDD adoption rates
4. **CI/CD Metrics**: Pipeline success rate, build time, deployment frequency

---

## 6. Anti-Patterns

**Location**: `dev-docs/ANTI_PATTERNS.md` (1,309 lines)

**Key Anti-Patterns**:

### 6.1 Skipping DDD
**Anti-Pattern**: Writing code before documenting API
**Impact**: Unclear requirements, frequent rework, poor API design
**Fix**: Always write API reference docs (Phase 3) before coding

### 6.2 Writing Tests After Code
**Anti-Pattern**: Implement feature, then "add tests later"
**Impact**: Low coverage, tests confirm implementation (not requirements)
**Fix**: Follow TDD (RED-GREEN-REFACTOR), tests drive design

### 6.3 Ignoring BDD Scenarios
**Anti-Pattern**: Skip Gherkin scenarios, rely only on unit tests
**Impact**: Disconnect between user requirements and implementation
**Fix**: Write BDD scenarios for user-facing behavior (Phase 4)

### 6.4 Skipping Code Review
**Anti-Pattern**: Merge directly to main without review
**Impact**: Bugs slip through, knowledge not shared, inconsistent code quality
**Fix**: Always require PR + 1 approval (Phase 6)

### 6.5 No Sprint Retrospective
**Anti-Pattern**: Skip retrospectives to "save time"
**Impact**: Same mistakes repeated, no process improvement
**Fix**: 30-min retrospective at sprint end, document learnings

---

## 7. Integration with Other SAPs

### 7.1 SAP-004 (testing-framework)
- **TDD (Phase 4)** uses pytest infrastructure
- **Coverage enforcement** (≥85%) from SAP-004
- **Test patterns** (unit, parametrized, async, mock) from SAP-004

### 7.2 SAP-005 (ci-cd-workflows)
- **Phase 5 (Testing)** executes CI workflows (test.yml, lint.yml)
- **Phase 6 (Review)** requires CI pass (quality gate)
- **Phase 7 (Release)** uses release.yml workflow

### 7.3 SAP-006 (quality-gates)
- **Phase 4 (Development)** enforced by pre-commit hooks
- **Phase 5 (Testing)** includes lint + type check from SAP-006
- **Phase 6 (Review)** verifies all hooks passed

### 7.4 SAP-007 (documentation-framework)
- **DDD (Phase 3)** uses Diataxis structure (Explanation, Reference)
- **Frontmatter validation** ensures docs follow standard
- **Executable How-Tos** generate tests for Phase 4

### 7.5 SAP-008 (automation-scripts)
- **Phase 4 (Development)** uses `just test`, `just lint`
- **Phase 5 (Testing)** uses `./scripts/pre-merge.sh`
- **Phase 7 (Release)** uses `./scripts/bump-version.sh`, `./scripts/publish-prod.sh`

### 7.6 SAP-013 (metrics-tracking)
- **Phase 8 (Monitoring)** uses ClaudeROICalculator
- **Process metrics** tracked in PROCESS_METRICS.md
- **Sprint velocity** tracked per sprint

---

## 8. Research Evidence

### 8.1 DDD → BDD → TDD Effectiveness

**Source**: "Test Driven Development: By Example" (Kent Beck, 2002)
- **40-80% defect reduction** when following TDD
- **Improved design** due to testability-first approach
- **Living documentation** (tests as specs)

**Source**: "The Cucumber Book" (Matt Wynne, Aslak Hellesøy, 2017)
- **BDD scenarios reduce ambiguity** by 60%
- **Stakeholder alignment** improved (Given-When-Then)
- **Executable specifications** prevent regression

**Source**: "Docs as Code" (Anne Gentle, 2017)
- **Documentation Driven Design** reduces API churn by 50%
- **Docs-first** approach catches design issues early
- **Test extraction** from docs ensures synchronization

---

## 9. Quality Gates Summary

| Phase | Quality Gates | Tools |
|-------|---------------|-------|
| **Phase 1: Vision** | Vision reviewed, roadmap aligned, metrics defined | Manual review |
| **Phase 2: Planning** | Capacity matches velocity, dependencies resolved, SMART goals | sprint-template.md |
| **Phase 3: Requirements (DDD)** | API reviewed, acceptance criteria complete, docs validated | Diataxis, frontmatter validation |
| **Phase 4: Development (BDD+TDD)** | BDD scenarios pass, unit tests pass, coverage ≥85%, no type errors | pytest, mypy, ruff |
| **Phase 5: Testing** | All tests pass, coverage ≥85%, no linting/type errors, no vulnerabilities | pytest, ruff, mypy, CodeQL |
| **Phase 6: Review** | 1+ approval, CI pass, docs updated, CHANGELOG updated | GitHub PR, CI workflows |
| **Phase 7: Release** | Tests pass on main, semver followed, CHANGELOG complete, PyPI publish succeeds | bump-version.sh, publish-prod.sh |
| **Phase 8: Monitoring** | Metrics tracked, feedback collected, retrospectives documented | PROCESS_METRICS.md |

---

## 9.5. Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/development-lifecycle/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Quick Start / Quick Start for Claude
- [ ] Common Workflows / Claude Code Workflows
- [ ] Best Practices / Claude-Specific Tips
- [ ] Common Pitfalls / Troubleshooting
- [ ] Related Content / Support & Resources

**Source Artifact Coverage (Both Files)**:
- [ ] capability-charter.md problem statement → "When to Use" section
- [ ] protocol-spec.md 8-phase lifecycle → "Workflows" section
- [ ] awareness-guide.md workflows → "Common Workflows" section
- [ ] adoption-blueprint.md installation → "Quick Start" section
- [ ] ledger.md sprint tracking → referenced in "Evidence of Use"

**YAML Frontmatter Fields** (Required):
```yaml
sap_id: SAP-012
version: X.Y.Z
status: active | pilot | draft
last_updated: YYYY-MM-DD
type: reference
audience: agents | claude_code
complexity: intermediate
estimated_reading_time: N
progressive_loading:
  phase_1: "lines 1-X"
  phase_2: "lines X-Y"
  phase_3: "full"
phase_1_token_estimate: NNNN
phase_2_token_estimate: NNNN
phase_3_token_estimate: NNNN
```

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/development-lifecycle/AGENTS.md && \
test -f docs/skilled-awareness/development-lifecycle/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/development-lifecycle/AGENTS.md | grep "progressive_loading:"
grep -A 10 "^---$" docs/skilled-awareness/development-lifecycle/CLAUDE.md | grep "progressive_loading:"

# Check workflow count equivalence
agents_workflows=$(grep "^### Workflow" docs/skilled-awareness/development-lifecycle/AGENTS.md | wc -l)
claude_workflows=$(grep "^### Workflow" docs/skilled-awareness/development-lifecycle/CLAUDE.md | wc -l)
echo "AGENTS workflows: $agents_workflows, CLAUDE workflows: $claude_workflows"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-012
```

**Expected Workflow Coverage**:
- AGENTS.md: Workflows for 8 phases (Vision, Planning, DDD, BDD, TDD, Quality, Review, Release)
- CLAUDE.md: 3 Claude Code workflows (Sprint start, DDD change request, BDD scenarios)
- Rationale: Different granularity acceptable - AGENTS.md covers all phases, CLAUDE.md focuses on high-leverage tool patterns

---

## 10. Related Documents

**Workflow Documentation**:
- [DEVELOPMENT_PROCESS.md](/static-template/dev-docs/workflows/DEVELOPMENT_PROCESS.md) - 8-phase lifecycle overview
- [DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD→BDD→TDD integration
- [DDD_WORKFLOW.md](/static-template/dev-docs/workflows/DDD_WORKFLOW.md) - Documentation Driven Design
- [BDD_WORKFLOW.md](/static-template/dev-docs/workflows/BDD_WORKFLOW.md) - Behavior Driven Development
- [TDD_WORKFLOW.md](/static-template/dev-docs/workflows/TDD_WORKFLOW.md) - Test Driven Development
- [ANTI_PATTERNS.md](/static-template/dev-docs/ANTI_PATTERNS.md) - Common mistakes

**Templates**:
- [sprint-template.md](/static-template/project-docs/sprints/sprint-template.md) - Sprint planning template
- [release-template.md](/static-template/project-docs/releases/release-template.md) - Release planning template
- [PROCESS_METRICS.md](/static-template/project-docs/metrics/PROCESS_METRICS.md) - Process metrics dashboard

**Related SAPs**:
- [SAP-004: testing-framework](../testing-framework/) - pytest, coverage, fixtures
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/) - GitHub Actions workflows
- [SAP-006: quality-gates](../quality-gates/) - Pre-commit hooks
- [SAP-007: documentation-framework](../documentation-framework/) - Diataxis structure
- [SAP-008: automation-scripts](../automation-scripts/) - Scripts and justfile

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for development-lifecycle SAP
