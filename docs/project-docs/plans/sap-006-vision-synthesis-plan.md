# SAP-006 Enhancement Plan: Vision Synthesis Workflow

**Status**: Draft
**Created**: 2025-11-05
**Owner**: Claude + User
**Priority**: P2 (Orchestration)
**Estimated Duration**: 8-12 hours
**Dependencies**: SAP-010 Strategic Templates (must complete first)

---

## 1. Executive Summary

This enhancement expands SAP-006 Phase 1 (Vision & Strategy) with a concrete 4-phase workflow for synthesizing scattered user intentions into structured vision documents and operational backlog. Currently, Phase 1 defines vision outputs (ROADMAP.md, vision statements) but lacks a workflow for creating them from scattered sources. This enhancement fills that gap with: (1) Discovery phase - consolidate intentions from inbox/GitHub/dogfooding/research, (2) Analysis phase - cluster intentions into strategic themes, (3) Vision Drafting phase - create multi-timeframe vision with capability waves, (4) Backlog Cascade phase - decompose vision Wave 1 into roadmap milestones and beads tasks. This workflow integrates SAP-010 templates, SAP-015 backlog operations, and SAP-027 pilot feedback, providing end-to-end orchestration for strategic planning.

---

## 2. Current State

### Artifact Completeness
- ✅ capability-charter.md (10,176 bytes)
- ✅ protocol-spec.md (31,281 bytes)
- ✅ awareness-guide.md (19,527 bytes)
- ✅ adoption-blueprint.md (20,269 bytes)
- ✅ ledger.md (16,200 bytes)

### Current Capabilities
- **8-Phase Lifecycle**: Vision & Strategy, Planning & Design, Implementation, Testing & Validation, Documentation, Deployment, Monitoring, Retrospective
- **Phase 1 (Vision & Strategy)**: Defines outputs (ROADMAP.md, vision statements, release plans), quality gates (vision reviewed by stakeholders, roadmap aligned with ecosystem)
- **Templates**: Sprint planning template, release template, process metrics template
- **DDD → BDD → TDD**: Integration of Domain-Driven Design, Behavior-Driven Development, Test-Driven Development
- **Anti-Patterns Guide**: 1,309 lines documenting common development pitfalls

### Gaps
- ❌ **No vision synthesis workflow**: Phase 1 defines outputs but not how to create them from scattered intentions
- ❌ **No intention discovery guidance**: How to find unfulfilled user needs across inbox, GitHub, dogfooding, research
- ❌ **No multi-timeframe vision structure**: No guidance on 3-month (committed) vs 6-month (exploratory) vs 12-month (aspirational) horizons
- ❌ **No vision → backlog cascade workflow**: How to decompose Wave 1 vision into ROADMAP.md → beads epic → tasks
- ❌ **No integration with SAP-001 (inbox)**: Coordination requests not used as intention sources
- ❌ **No integration with SAP-010 (A-MEM)**: Knowledge graph not used for intention memory
- ❌ **No integration with SAP-027 (dogfooding)**: Pilot feedback not used for vision decision criteria

---

## 3. Enhancement Overview

### What We're Adding
1. **Phase 1.1: Discovery** - Consolidate intentions from 5 sources (inbox, GitHub, dogfooding, research, A-MEM)
2. **Phase 1.2: Analysis** - Cluster intentions into strategic themes with evidence levels and user demand
3. **Phase 1.3: Vision Drafting** - Create multi-timeframe vision with capability waves (3/6/12-month horizons)
4. **Phase 1.4: Backlog Cascade** - Decompose Wave 1 into ROADMAP.md, beads epic, tasks
5. **Multi-Timeframe Vision Guidance** - 3-month (committed), 6-month (exploratory), 12-month (aspirational) with decision criteria
6. **Integration Patterns** - SAP-001 (inbox sources), SAP-010 (strategic templates), SAP-015 (backlog cascade), SAP-027 (pilot feedback)
7. **3 Vision Workflow Templates** - Intention inventory, strategic theme matrix, vision document (copy from SAP-010)

### Why This Matters
- **End-to-End Orchestration**: Connects scattered intentions → structured vision → operational backlog
- **Repeatable Process**: Provides concrete steps, not just abstract goals
- **Multi-Horizon Planning**: 3-month committed work + 6-month exploratory + 12-month aspirational
- **Evidence-Based**: Filters intentions by evidence level (A: Standards, B: Case Studies, C: Expert Opinion)
- **Ecosystem Reusable**: Any project can adopt this workflow for strategic planning

### Integration with Other SAPs
- **SAP-010 (A-MEM)**: Uses strategic templates (intention inventory, theme matrix, vision document, roadmap milestone), queries knowledge graph for intentions
- **SAP-015 (Beads)**: Cascade Wave 1 → beads epic/tasks, link roadmap milestone to epic via metadata
- **SAP-027 (Dogfooding)**: Read pilot feedback for Wave 2 decision criteria, update vision quarterly based on GO/NO-GO results
- **SAP-001 (Inbox)**: Read coordination requests as intention sources during discovery phase

---

## 4. Detailed Deliverables

### Deliverable 1: Protocol Spec Section 3.1 Expansion (Phase 1 Workflow)
**File**: `docs/skilled-awareness/development-lifecycle/protocol-spec.md` (update)
**Type**: Update existing (expand Section 3.1)
**Effort**: 3 hours

**Description**: Expand Section 3.1 (Phase 1: Vision & Strategy) from high-level outputs to detailed 4-phase workflow with inputs, activities, outputs, and duration for each sub-phase.

**Content Outline**:
- **Section 3.1.1: Phase 1.1 - Discovery** (NEW)
  - Duration: 1-2 days
  - Inputs: Inbox (SAP-001), GitHub issues, dogfooding feedback (SAP-027), research reports, A-MEM knowledge notes (SAP-010)
  - Activities: Query A-MEM for intentions, scan inbox for coordination requests, review GitHub labels, read dogfooding summaries
  - Output: Intention inventory (SAP-010 template)
  - Example commands: `grep '"type": "intention-inventory"' ...`, `cat inbox/coordination/active.jsonl`, `gh issue list --label feature-request`

- **Section 3.1.2: Phase 1.2 - Analysis** (NEW)
  - Duration: 1-2 days
  - Input: Intention inventory
  - Activities: Cluster intentions by theme (pattern recognition), calculate evidence levels (A ≥30%, B ≥40%, C ≤30%), quantify user demand, prioritize themes by (evidence × demand)
  - Output: Strategic theme matrix (SAP-010 template)
  - Wave Decision Criteria:
    - Wave 1 (Committed): Evidence A+B ≥ 70%, user demand ≥ 10, effort < 50 hours
    - Wave 2 (Exploratory): Evidence A+B ≥ 60%, user demand ≥ 5, validate via dogfooding (SAP-027)
    - Wave 3 (Aspirational): Evidence A+B < 60%, user demand < 5, defer to quarterly review

- **Section 3.1.3: Phase 1.3 - Vision Drafting** (ENHANCED from current)
  - Duration: 2-3 days
  - Input: Strategic theme matrix
  - Activities: Create vision document (SAP-010 template) with capability waves, define Wave 1 features (committed to ROADMAP.md), identify Wave 2 candidates (exploratory, dogfooding validation), outline Wave 3 aspirations (12-month), set decision review dates for Wave 2
  - Output: Vision document (`.chora/memory/knowledge/notes/vision-{project}-{horizon}.md`)
  - Multi-Timeframe Guidance:
    - 3-Month Horizon (Wave 1): Committed in ROADMAP.md, decomposed to beads epic/tasks
    - 6-Month Horizon (Wave 2): Exploratory, dogfooding pilot (SAP-027), decision review quarterly
    - 12-Month Horizon (Wave 3): Aspirational, quarterly review (promote to Wave 2 or deprecate)

- **Section 3.1.4: Phase 1.4 - Backlog Cascade** (NEW)
  - Duration: 1 day
  - Input: Vision Wave 1 (committed)
  - Activities: Update ROADMAP.md with Wave 1 features, create beads epic from Wave 1 (SAP-015 integration), decompose epic into tasks, link tasks to roadmap milestones, add metadata for traceability (`from_vision_wave`, `roadmap_version`)
  - Output: Updated ROADMAP.md, beads epic (chora-base-epic-{id}), beads tasks (P0-P2), roadmap milestone knowledge note (SAP-010 template)
  - Example commands:
    ```bash
    bd create "Wave 1: {Theme} (v{version})" --priority 1 --type epic
    bd create "{Feature 1}" --priority 2
    bd dep add {epic-id} blocks {task-1-id}
    bd update {epic-id} --metadata '{"from_vision_wave": 1, "roadmap_version": "v1.5.0"}'
    ```

**Example Content**:
```markdown
### 3.1: Phase 1 - Vision & Strategy (ENHANCED)

**Duration**: 5-8 days (1-2 days per sub-phase)
**Objective**: Synthesize scattered user intentions into structured vision and operational backlog

---

#### 3.1.1: Phase 1.1 - Discovery (NEW)

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

#### 3.1.2: Phase 1.2 - Analysis (NEW)

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

#### 3.1.3: Phase 1.3 - Vision Drafting (ENHANCED)

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

**Example** (chora-base Nov 2025):
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

#### 3.1.4: Phase 1.4 - Backlog Cascade (NEW)

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
```

---

### Deliverable 2: Protocol Spec Section 4 (Integration Patterns)
**File**: `docs/skilled-awareness/development-lifecycle/protocol-spec.md` (update)
**Type**: Update existing (enhance Section 4)
**Effort**: 2 hours

**Description**: Enhance Section 4 (Integration Patterns) to document SAP-006 integration with SAP-001, SAP-010, SAP-015, SAP-027.

**Content Outline**:
- **Section 4.1: Integration with SAP-001 (Inbox Coordination)** (NEW)
  - **Phase 1.1 Discovery**: Read `inbox/coordination/active.jsonl` as intention source
  - **Coordination → Intention**: Map coordination requests to intention inventory
  - **Example**: 4 coordination requests → 4 HIGH-priority intentions in inventory

- **Section 4.2: Integration with SAP-010 (Memory System - A-MEM)** (NEW)
  - **Template Usage**: Phase 1.1-1.4 use SAP-010 strategic templates (intention inventory, theme matrix, vision document, roadmap milestone)
  - **Knowledge Graph Queries**: Phase 1.1 queries A-MEM for unfulfilled intentions (`grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md`)
  - **Strategic Artifact Storage**: Vision documents, roadmap milestones stored in `.chora/memory/knowledge/notes/`
  - **Example**: Phase 1.1 creates `intention-inventory-2025-11-05.md` using SAP-010 template

- **Section 4.3: Integration with SAP-015 (Task Tracking with Beads)** (NEW)
  - **Phase 1.4 Backlog Cascade**: Create beads epic from vision Wave 1 using `bd create`
  - **Task Decomposition**: Decompose epic into beads tasks with `bd create` + `bd dep add`
  - **Traceability Metadata**: Link epic to vision via metadata `{"from_vision_wave": 1, "roadmap_version": "v1.5.0"}`
  - **Roadmap Milestone Linkage**: Roadmap milestone note `linked_to` field contains beads epic ID
  - **Example**: Vision Wave 1 → beads epic chora-base-xyz → 20 tasks (P0-P2)

- **Section 4.4: Integration with SAP-027 (Dogfooding Patterns)** (NEW)
  - **Phase 1.1 Discovery**: Read dogfooding pilot feedback from SAP-027 final summaries (`grep '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md`)
  - **Wave 2 Validation**: Dogfooding pilots (SAP-027) validate Wave 2 exploratory candidates before committing to Wave 1
  - **Quarterly Vision Review**: Update vision Wave 2 decision criteria based on pilot GO/NO-GO results
  - **Example**: SAP-029 pilot GO (119x time savings) → Update vision Wave 2 "SAP generation validated" criterion → ✅ Met

**Example Content**:
```markdown
### 4: Integration Patterns (ENHANCED)

**Overview**: SAP-006 Development Lifecycle integrates with SAP-001 (Inbox), SAP-010 (A-MEM), SAP-015 (Beads), SAP-027 (Dogfooding) to enable end-to-end strategic planning from scattered intentions to operational backlog.

---

#### 4.1: Integration with SAP-001 (Inbox Coordination Protocol) (NEW)

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

#### 4.2: Integration with SAP-010 (Memory System - A-MEM) (NEW)

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

#### 4.3: Integration with SAP-015 (Task Tracking with Beads) (NEW)

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
  - beads-epic-chora-base-xyz  ← Add epic ID here
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

#### 4.4: Integration with SAP-027 (Dogfooding Patterns) (NEW)

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
5. Execute 6-week pilot (research, build, validate, decide, formalize)
6. GO decision → Update vision Wave 2 "Validated" status → Promote to Wave 1 in next vision
7. NO-GO decision → Update vision Wave 2 "Pilot failed" status → Defer to Wave 3 or remove

**Example** (chora-base):
- Vision Wave 2 candidate: "SAP Generation Automation"
- SAP-027 pilot: SAP-029 (sap-generation) → GO (119x time savings)
- Vision update: Wave 2 "SAP generation validated" ✅ → Commit to Wave 1 in v1.6.0

**Benefits**:
- Systematic validation of exploratory ideas before ecosystem commitment
- Data-driven decision criteria (not guesswork)
- Pilot feedback loop closes gap between vision and execution
```

---

### Deliverable 3: Awareness Guide Vision Synthesis Examples
**File**: `docs/skilled-awareness/development-lifecycle/awareness-guide.md` (update)
**Type**: Update existing (add new section)
**Effort**: 2 hours

**Description**: Add "Vision Synthesis Workflows" section to awareness-guide.md with step-by-step examples from chora-base dogfooding.

**Content Outline**:
- **Vision Synthesis Workflows** (new section after "Sprint Planning Workflows")
  - When to run vision synthesis (monthly discovery, quarterly vision review)
  - Example 1: Intention Discovery (chora-base Nov 2025 - 89 intentions from 5 sources)
  - Example 2: Strategic Theme Analysis (5 themes from 42 intentions)
  - Example 3: Vision Drafting (6-month vision with 3 waves)
  - Example 4: Backlog Cascade (Wave 1 → ROADMAP.md → beads epic → 20 tasks)
  - Example 5: Quarterly Vision Review (update Wave 2 based on pilot feedback)

(Content follows similar structure to SAP-010 awareness-guide examples, adapted for SAP-006 workflows)

---

### Deliverable 4-6: Vision Workflow Templates
**Files**: 3 new files in `docs/project-docs/templates/`
**Type**: New files
**Effort**: 2 hours total (40 min each)

**Description**: Copy SAP-010 strategic templates to `docs/project-docs/templates/` for easy human access (`.chora/memory/templates/` is for agents).

**Files**:
1. `VISION_DOCUMENT_TEMPLATE.md` (copy from SAP-010 vision-document-template.md)
2. `INTENTION_INVENTORY_TEMPLATE.md` (copy from SAP-010 intention-inventory-template.md)
3. `STRATEGIC_THEME_MATRIX.md` (copy from SAP-010 strategic-theme-matrix-template.md)

**Note**: These are human-readable copies. Agent workflows use SAP-010 templates in `.chora/memory/templates/`.

---

### Deliverable 7: Ledger Update
**File**: `docs/skilled-awareness/development-lifecycle/ledger.md` (update)
**Type**: Update existing (add version entry)
**Effort**: 15 minutes

**Description**: Document this enhancement in ledger.md as version 1.1.0.

**Content**: Add new version entry documenting Phase 1 expansion, integration patterns, vision workflow templates.

---

## 5. Execution Tasks

(Similar structure to SAP-010, with 7 tasks matching the 7 deliverables above)

### Task 1: Expand Protocol Spec Section 3.1 (Phase 1 Workflow)
**Effort**: 3 hours
**Dependencies**: SAP-010 templates (must exist first)

**Steps**:
1. Read current protocol-spec.md Section 3.1 (Phase 1: Vision & Strategy)
2. Add Section 3.1.1 (Phase 1.1 - Discovery) with inputs, activities, outputs, duration, example
3. Add Section 3.1.2 (Phase 1.2 - Analysis) with wave decision criteria, theme clustering workflow
4. Enhance Section 3.1.3 (Phase 1.3 - Vision Drafting) with multi-timeframe guidance (3/6/12-month)
5. Add Section 3.1.4 (Phase 1.4 - Backlog Cascade) with beads integration, traceability chain
6. Add quality gates for each sub-phase
7. Add chora-base examples throughout

**Output**: Updated protocol-spec.md Section 3.1 (expanded from 1 page to 5-6 pages)

---

### Task 2: Enhance Protocol Spec Section 4 (Integration Patterns)
**Effort**: 2 hours
**Dependencies**: Task 1 (Section 3.1 references integration points)

**Steps**:
1. Read current protocol-spec.md Section 4
2. Add Section 4.1 (Integration with SAP-001) - inbox coordination requests as intention sources
3. Add Section 4.2 (Integration with SAP-010) - strategic templates, knowledge graph queries
4. Add Section 4.3 (Integration with SAP-015) - backlog cascade, traceability metadata
5. Add Section 4.4 (Integration with SAP-027) - pilot feedback, Wave 2 validation
6. Add examples and code snippets for each integration

**Output**: Updated protocol-spec.md Section 4 (expanded with 4 new integration patterns)

---

### Task 3: Add Awareness Guide Vision Synthesis Section
**Effort**: 2 hours
**Dependencies**: Task 1-2 (protocol-spec complete for reference)

**Steps**:
1. Read current awareness-guide.md to find insertion point (after "Sprint Planning Workflows")
2. Write "Vision Synthesis Workflows" section with 5 examples:
   - When to run vision synthesis
   - Example 1: Intention Discovery (chora-base Nov 2025)
   - Example 2: Strategic Theme Analysis
   - Example 3: Vision Drafting
   - Example 4: Backlog Cascade
   - Example 5: Quarterly Vision Review
3. Add step-by-step bash commands
4. Add chora-base dogfooding examples

**Output**: Updated awareness-guide.md with vision synthesis workflows section

---

### Task 4-6: Create Vision Workflow Templates
**Effort**: 2 hours (40 min each × 3 templates)
**Dependencies**: SAP-010 templates (must exist to copy from)

**Steps** (per template):
1. Copy SAP-010 template from `.chora/memory/templates/{name}.md`
2. Save to `docs/project-docs/templates/{NAME}.md` (human-readable location)
3. Add brief usage instructions at top (for developers/PMs)
4. Verify template has chora-base example

**Output**: 3 new template files in `docs/project-docs/templates/`

---

### Task 7: Update Ledger with Version 1.1.0
**Effort**: 15 minutes
**Dependencies**: Tasks 1-6 (all enhancements complete)

**Steps**:
1. Read current ledger.md version history
2. Add version 1.1.0 entry with:
   - Date (2025-11-05)
   - Enhancement title (Vision Synthesis Workflow)
   - Changes (Phase 1 expanded to 4 sub-phases, integration patterns, templates)
   - Integration points (SAP-001, SAP-010, SAP-015, SAP-027)
   - Effort (8-12 hours)

**Output**: Updated ledger.md with version 1.1.0 entry

---

## 6. Success Criteria

### Functional
- ✅ Protocol-spec Section 3.1 expanded with 4 sub-phases (Discovery, Analysis, Vision Drafting, Backlog Cascade)
- ✅ Multi-timeframe vision guidance documented (3-month committed, 6-month exploratory, 12-month aspirational)
- ✅ Phase 1.1-1.4 each have: duration, inputs, activities, outputs, quality gates, examples
- ✅ Wave decision criteria defined (Wave 1: A+B ≥70%, Wave 2: A+B ≥60%, Wave 3: A+B <60%)

### Integration
- ✅ SAP-001 integration: Inbox coordination requests used as intention sources
- ✅ SAP-010 integration: Strategic templates used in Phase 1.1-1.4, knowledge graph queried for intentions
- ✅ SAP-015 integration: Vision Wave 1 cascades to beads epic/tasks with traceability metadata
- ✅ SAP-027 integration: Pilot feedback updates vision Wave 2 decision criteria quarterly

### Documentation
- ✅ Protocol-spec.md Section 3.1 and 4 complete (5-6 pages + 4 integration patterns)
- ✅ Awareness-guide.md has vision synthesis workflows section with 5 examples
- ✅ 3 vision workflow templates in `docs/project-docs/templates/`
- ✅ Ledger.md documents version 1.1.0 enhancement

---

## 7. Testing & Validation

### Test 1: End-to-End Vision Synthesis
1. Run Phase 1.1 Discovery: Consolidate 10+ test intentions from inbox/GitHub/A-MEM
2. Run Phase 1.2 Analysis: Cluster into 3 themes, apply wave decision criteria
3. Run Phase 1.3 Vision Drafting: Create test vision document with 3 waves
4. Run Phase 1.4 Backlog Cascade: Create ROADMAP.md entry, beads epic, 5 tasks
5. Verify traceability: Vision → roadmap → epic → tasks

### Test 2: Wave 2 Validation via Dogfooding
1. Create test vision with Wave 2 candidate
2. Run SAP-027 pilot for candidate (simulated 6-week pilot)
3. Record pilot result (GO/NO-GO)
4. Run quarterly vision review
5. Update vision Wave 2 decision criteria based on pilot result
6. Verify vision updated correctly (GO → "Validated" ✅, NO-GO → "Pilot failed" ❌)

### Test 3: Integration with SAP-010/SAP-015
1. Verify Phase 1.1-1.4 use SAP-010 templates (check file paths)
2. Verify roadmap milestone note has `linked_to: [vision, beads-epic]`
3. Verify beads epic has metadata `from_vision_wave: 1`
4. Query by vision wave: `bd list --json | jq '.[] | select(.metadata.from_vision_wave == 1)'`
5. Verify results match Wave 1 tasks

### Dogfooding Checklist:
- ✅ Run Phase 1.1-1.4 for chora-base v1.5.0
- ✅ Create intention inventory (89 intentions)
- ✅ Create strategic theme matrix (5 themes)
- ✅ Create vision document (6-month, 3 waves)
- ✅ Cascade Wave 1 to ROADMAP.md + beads epic + 20 tasks
- ✅ Document in ledger.md version 1.1.0 entry
- ✅ Collect feedback: Did workflow save time? Were phases clear?

---

## 8. Boundaries & Integration Points

### This SAP Owns
- ✅ Vision synthesis workflow (Phase 1.1-1.4 orchestration)
- ✅ Multi-timeframe vision guidance (3/6/12-month horizons, wave structure)
- ✅ Wave decision criteria (A+B ≥70% for Wave 1, etc.)
- ✅ ROADMAP.md structure and maintenance
- ✅ Sprint planning workflows (Phase 2)
- ✅ Quarterly vision review process

### This SAP Does NOT Own
- ❌ Strategic template storage (owned by SAP-010 A-MEM)
- ❌ Beads epic/task creation (owned by SAP-015, SAP-006 calls SAP-015 APIs)
- ❌ Dogfooding pilot execution (owned by SAP-027, SAP-006 reads pilot results)
- ❌ Inbox coordination request management (owned by SAP-001, SAP-006 reads inbox)

### Integration Points

**SAP-006 ← SAP-001 (Inbox Coordination Protocol)**:
- **Mechanism**: Phase 1.1 Discovery reads `inbox/coordination/active.jsonl` as intention source
- **Data Flow**: SAP-001 coordination requests → SAP-006 intention inventory
- **Example**: 4 coordination requests → 4 HIGH-priority intentions

**SAP-006 ↔ SAP-010 (Memory System - A-MEM)**:
- **Mechanism**: SAP-006 uses SAP-010 strategic templates in Phase 1.1-1.4
- **Data Flow**: SAP-010 provides templates → SAP-006 creates strategic knowledge notes → SAP-010 stores for quarterly review
- **Example**: Phase 1.1 creates `intention-inventory-2025-11-05.md` using SAP-010 template

**SAP-006 → SAP-015 (Task Tracking with Beads)**:
- **Mechanism**: Phase 1.4 Backlog Cascade creates beads epic/tasks from vision Wave 1
- **Data Flow**: SAP-006 vision Wave 1 → SAP-015 beads epic → SAP-015 beads tasks
- **Example**: Vision Wave 1 (4 SAP enhancements) → beads epic chora-base-xyz → 20 tasks (P0-P2)

**SAP-006 ← SAP-027 (Dogfooding Patterns)**:
- **Mechanism**: Quarterly vision review updates Wave 2 decision criteria based on SAP-027 pilot feedback
- **Data Flow**: SAP-027 pilot GO/NO-GO → SAP-006 updates vision Wave 2 "Validated" status
- **Example**: SAP-029 pilot GO → Vision Wave 2 "SAP generation validated" ✅ → Commit to Wave 1 in next vision

---

## 9. Rollout Plan

**Phase**: 2 (Orchestration)
**Recommended Order**: Execute after SAP-010 (depends on strategic templates)

**Parallel Execution**:
- ❌ Cannot execute before: SAP-010 (Strategic Templates Plan) - hard dependency on templates
- ✅ Can execute in parallel with: SAP-027 (Pre-Pilot Discovery Plan) - no direct dependency
- ⚠️ Soft dependency for: SAP-015 (Backlog Organization Plan) - SAP-015 vision cascade pattern needs SAP-006 Phase 1.4, but SAP-015 can start on other patterns

**Critical Path**: Blocking SAP-015 vision cascade pattern. Recommend executing SAP-010 → SAP-006 → SAP-015 sequentially for cleanest integration.

---

## 10. Open Questions

None - plan is self-contained and ready to execute after SAP-010 complete.

---

## 11. References

- **SAP-006 Current Artifacts**: `docs/skilled-awareness/development-lifecycle/`
- **Research Findings**: Comprehensive SAP research conducted by Plan agent (2025-11-05)
- **Related Plans**:
  - `docs/project-docs/plans/sap-010-strategic-templates-plan.md` (must complete first)
  - `docs/project-docs/plans/sap-015-backlog-organization-plan.md` (soft dependency on this plan)
  - `docs/project-docs/plans/sap-027-pre-pilot-discovery-plan.md` (parallel execution possible)
  - `docs/project-docs/plans/strategic-planning-enhancements-overview.md` (integration overview)
