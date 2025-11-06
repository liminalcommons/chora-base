# SAP-010 Enhancement Plan: Strategic Knowledge Templates

**Status**: Draft
**Created**: 2025-11-05
**Owner**: Claude + User
**Priority**: P1 (Foundation)
**Estimated Duration**: 4-6 hours
**Dependencies**: None (can start immediately)

---

## 1. Executive Summary

This enhancement adds 4 strategic knowledge templates to SAP-010 (A-MEM Memory System) to enable systematic storage of strategic planning artifacts. These templates provide the foundational infrastructure for SAP-006 (vision synthesis), SAP-015 (backlog cascade), and SAP-027 (pilot discovery) workflows. By creating reusable templates for vision documents, intention inventories, roadmap milestones, and strategic theme matrices, the entire chora-base ecosystem gains a standardized way to consolidate scattered user intentions into clarified strategic artifacts.

---

## 2. Current State

### Artifact Completeness
- ✅ capability-charter.md (9,835 bytes)
- ✅ protocol-spec.md (30,153 bytes)
- ✅ awareness-guide.md (29,768 bytes)
- ✅ adoption-blueprint.md (19,030 bytes)
- ✅ ledger.md (20,473 bytes)

### Current Capabilities
- **4 Memory Types**: Ephemeral session, event log (`.chora/memory/events/*.jsonl`), knowledge graph (`.chora/memory/knowledge/notes/*.md`), agent profiles
- **Knowledge Graph**: Zettelkasten-style notes with YAML frontmatter, bidirectional links, tags index
- **Existing Templates**: `daily-logging-template.md` (for tracking daily work, beads usage, context restoration)
- **Event Tag Taxonomy**: 7 domains (development, sap, automation, coordination, memory, infrastructure, errors)

### Gaps
- ❌ **No strategic planning templates**: Only daily logging template exists
- ❌ **No vision/roadmap schemas**: Knowledge notes are generic, no vision-specific frontmatter
- ❌ **No intention tracking templates**: No structure for consolidating unfulfilled user intentions
- ❌ **No strategic knowledge node types**: All notes treated equally, no distinction between operational vs strategic

---

## 3. Enhancement Overview

### What We're Adding
1. **4 Strategic Knowledge Templates**: Vision document, intention inventory, roadmap milestone, strategic theme matrix
2. **Knowledge Node Type System**: New `type` field in frontmatter to distinguish strategic vs operational knowledge
3. **Strategic Artifact Lifecycle**: Creation → quarterly review → archival workflow
4. **Query Patterns**: Search by type (e.g., find all vision docs, find stale inventories)
5. **Documentation**: protocol-spec Section 3.5, awareness-guide strategic planning section

### Why This Matters
- **Foundational Infrastructure**: Enables SAP-006 vision synthesis, SAP-015 backlog cascade, SAP-027 pilot discovery
- **Reusable Across Ecosystem**: Any project can adopt these templates for strategic planning
- **Standardized Storage**: Consistent structure for strategic artifacts makes them queryable and reusable
- **Traceability**: Vision ↔ roadmap ↔ beads epic linkage via `linked_to` field

### Integration with Other SAPs
- **SAP-006 (Lifecycle)**: Vision synthesis workflow uses vision template, intention inventory template, theme matrix template
- **SAP-015 (Beads)**: Backlog cascade links roadmap milestone notes to beads epic IDs via `linked_to` field
- **SAP-027 (Dogfooding)**: Pre-pilot discovery reads intention inventory, pilot feedback stored as knowledge notes

---

## 4. Detailed Deliverables

### Deliverable 1: Vision Document Template
**File**: `.chora/memory/templates/vision-document-template.md`
**Type**: New file
**Effort**: 1 hour

**Description**: Template for creating vision documents with capability waves (3-month, 6-month, 12-month horizons).

**Content Outline**:
- **Frontmatter**:
  - `id`: vision-{project}-{horizon}
  - `type`: strategic-vision
  - `horizon`: 3-month | 6-month | 12-month
  - `status`: draft | active | archived
  - `waves`: Array of wave objects (wave number, status, target version, decision review date)
  - `tags`: [vision, strategic-planning, {project}]
  - `created`, `updated`: ISO 8601 timestamps
- **Body**:
  - Wave 1 (Committed - 3 months): Features for ROADMAP.md
  - Wave 2 (Exploratory - 6 months): Candidates for dogfooding validation
  - Wave 3 (Aspirational - 12 months): Long-term vision

**Example**:
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
  - wave: 2
    status: exploratory
    decision_review: 2026-Q1
tags: [vision, strategic-planning, chora-base]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Vision: chora-base 6-Month (Nov 2025 - Apr 2026)

## Wave 1: Strategic Planning Infrastructure (Committed - 3 months)

**Target**: v1.5.0 (Feb 2026)

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
- Intention discovery CLI (`scripts/discover-intentions.py`)
- Strategic theme clustering CLI (`scripts/cluster-strategic-themes.py`)
- Vision → backlog cascade CLI (`scripts/cascade-vision-to-backlog.py`)
- Backlog health dashboard (`scripts/backlog-health.py`)

**Validation Plan**: Dogfood CLIs in Wave 1 execution, collect time savings data

## Wave 3: Ecosystem Adoption (Aspirational - 12 months)

**Target**: 3+ ecosystem projects adopt strategic planning SAPs

**Candidates**:
- Public documentation for strategic planning workflow
- Video tutorials for vision synthesis
- Case studies from ecosystem adopters
- Strategic planning SAP set (minimal-strategic-planning)
```

---

### Deliverable 2: Intention Inventory Template
**File**: `.chora/memory/templates/intention-inventory-template.md`
**Type**: New file
**Effort**: 45 minutes

**Description**: Template for consolidating scattered unfulfilled intentions from multiple sources (inbox, GitHub, dogfooding feedback, research).

**Content Outline**:
- **Frontmatter**:
  - `id`: intention-inventory-{date}
  - `type`: intention-inventory
  - `sources`: Object with counts (inbox, github, dogfooding, research, a-mem)
  - `tags`: [intention-discovery, strategic-planning, backlog-refinement]
  - `created`, `updated`: ISO 8601 timestamps
- **Body**:
  - High-Evidence Intentions (Level A: Standards, peer-reviewed research)
  - Medium-Evidence Intentions (Level B: Industry case studies, production data)
  - Low-Evidence Intentions (Level C: Expert opinion, blog posts)

**Example**:
```yaml
---
id: intention-inventory-2025-11-05
type: intention-inventory
sources:
  inbox: 4
  github: 12
  dogfooding: 3
  research: 8
  a-mem: 15
tags: [intention-discovery, strategic-planning, backlog-refinement]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Intention Inventory - 2025-11-05

**Total Intentions**: 42
**High-Evidence (A)**: 14 (33%)
**Medium-Evidence (B)**: 18 (43%)
**Low-Evidence (C)**: 10 (24%)

## High-Evidence Intentions (Level A: Standards, Research)

### 1. OIDC Trusted Publishing for PyPI
- **Source**: PyPI documentation, PEP 740
- **Evidence**: OIDC introduced 2023 as recommended default, PEP 740 attestations require trusted publishing
- **User Demand**: Security best practice (standards-based)
- **Related**: SAP-028 (publishing-automation)
- **Priority**: HIGH

### 2. Strategic Planning Workflow
- **Source**: Research (PM methodologies), inbox coordination requests
- **Evidence**: PM best practices (OKRs, roadmapping), user demand from 4 coordination requests
- **User Demand**: 4 explicit requests in inbox
- **Related**: SAP-006, SAP-010, SAP-015, SAP-027
- **Priority**: HIGH

## Medium-Evidence Intentions (Level B: Case Studies)

### 3. MCP Server Testing Patterns
- **Source**: MCP ecosystem (GitHub discussions, FastMCP examples)
- **Evidence**: Production usage in chora-compose, mcp-n8n projects
- **User Demand**: 8 developers requesting
- **Related**: SAP-014 (mcp-server-development)
- **Priority**: MEDIUM

[... continue for all 42 intentions ...]

## Analysis Summary

**Top 5 Themes** (by evidence × demand):
1. Strategic Planning (14 intentions, 33% Level A, 4 user requests) → **Recommend Wave 1**
2. Testing & Quality (8 intentions, 25% Level A, 8 user requests) → **Recommend Wave 1**
3. MCP Integration (6 intentions, 17% Level B, 8 user requests) → **Recommend Wave 2**
4. Performance Optimization (5 intentions, 20% Level A, 3 user requests) → **Recommend Wave 2**
5. Documentation Quality (4 intentions, 25% Level B, 2 user requests) → **Recommend Wave 3**
```

---

### Deliverable 3: Roadmap Milestone Template
**File**: `.chora/memory/templates/roadmap-milestone-template.md`
**Type**: New file
**Effort**: 45 minutes

**Description**: Template for tracking roadmap milestones (from vision Wave 1) with linkage to beads epics.

**Content Outline**:
- **Frontmatter**:
  - `id`: milestone-{version}
  - `type`: roadmap-milestone
  - `version`: Semantic version (e.g., v1.5.0)
  - `target_date`: ISO 8601 date
  - `from_vision_wave`: 1 | 2 | 3 (which wave this came from)
  - `committed`: true | false
  - `linked_to`: Array of IDs (vision document, beads epic)
  - `tags`: [roadmap, milestone, {version}]
  - `created`, `updated`: ISO 8601 timestamps
- **Body**:
  - Features (from Vision Wave)
  - Success Criteria
  - Linked Beads Epic (ID, task count, progress)

**Example**:
```yaml
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
**Status**: In Progress

## Features (from Vision Wave 1)

### SAP-010: Strategic Knowledge Templates
- 4 templates (vision, intention, roadmap, theme)
- Knowledge node type system
- Strategic artifact lifecycle
- **Effort**: 4-6 hours

### SAP-006: Vision Synthesis Workflow
- 4-phase workflow (discovery → analysis → drafting → cascade)
- Multi-timeframe vision guidance (3/6/12-month horizons)
- Integration with SAP-010, SAP-015, SAP-027
- **Effort**: 8-12 hours

### SAP-015: Backlog Organization Patterns
- Multi-tier backlog (P0-P4)
- Vision → backlog cascade
- Backlog refinement workflow (quarterly)
- Epic decomposition patterns
- **Effort**: 6-10 hours

### SAP-027: Pre-Pilot Discovery Phase
- Week -1 discovery phase
- Pilot selection criteria
- Dogfooding → vision feedback loop
- Pilot → backlog integration
- **Effort**: 4-6 hours

## Success Criteria

- ✅ All 4 SAPs enhanced with strategic planning capabilities
- ✅ Workflow pipeline validated through dogfooding in chora-base
- ✅ Ecosystem can consolidate intentions → vision → backlog
- ✅ Templates reusable across ecosystem projects
- ✅ Integration between SAPs tested (vision → backlog, pilot → backlog)

## Linked Beads Epic

- **Epic ID**: chora-base-xyz (to be created after approval)
- **Tasks**: 20 tasks (estimated)
  - SAP-010: 5 tasks (templates + docs)
  - SAP-006: 6 tasks (workflow + templates + docs)
  - SAP-015: 5 tasks (patterns + docs)
  - SAP-027: 4 tasks (discovery + integration + docs)
- **Progress**: 0% (not started)

## Dependencies

- **Blockers**: None (foundational work)
- **Enables**: Ecosystem strategic planning adoption (Wave 2)
```

---

### Deliverable 4: Strategic Theme Matrix Template
**File**: `.chora/memory/templates/strategic-theme-matrix-template.md`
**Type**: New file
**Effort**: 45 minutes

**Description**: Template for clustering intentions into strategic themes with prioritization (used in SAP-006 vision synthesis analysis phase).

**Content Outline**:
- **Frontmatter**:
  - `id`: strategic-themes-{date}
  - `type`: strategic-theme-matrix
  - `input_inventory`: intention-inventory-{date} (which inventory this analyzed)
  - `tags`: [strategic-planning, theme-analysis, vision-synthesis]
  - `created`, `updated`: ISO 8601 timestamps
- **Body**:
  - Theme 1, 2, 3... (name, intention count, evidence breakdown, user demand, priority, recommended wave)

**Example**:
```yaml
---
id: strategic-themes-2025-11-05
type: strategic-theme-matrix
input_inventory: intention-inventory-2025-11-05
tags: [strategic-planning, theme-analysis, vision-synthesis]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Strategic Theme Matrix - 2025-11-05

**Input**: intention-inventory-2025-11-05 (42 intentions)
**Themes Identified**: 5
**Recommended for Wave 1**: 2 themes (Strategic Planning, Testing & Quality)

---

## Theme 1: Strategic Planning Infrastructure

**Intentions**: 14 (from inventory)
**Evidence Level**:
- Level A (Standards): 5 (36%)
- Level B (Case Studies): 6 (43%)
- Level C (Expert Opinion): 3 (21%)
- **Total A+B**: 11 (79%) ✅ Exceeds 70% threshold

**User Demand**: 4 explicit inbox requests, 10 GitHub feature requests
**Related SAPs**: SAP-006, SAP-010, SAP-015, SAP-027
**Effort Estimate**: 22-34 hours (4 SAP enhancements)
**ROI Potential**: 10x (based on reducing vision synthesis time from days to hours)

**Priority**: **HIGH**
**Recommended Wave**: **Wave 1** (Committed for v1.5.0)

**Rationale**: High evidence (79% A+B), explicit user demand (4 requests), foundational capability enabling other workflows, strong ROI potential.

---

## Theme 2: Testing & Quality Improvements

**Intentions**: 8 (from inventory)
**Evidence Level**:
- Level A (Standards): 2 (25%)
- Level B (Case Studies): 4 (50%)
- Level C (Expert Opinion): 2 (25%)
- **Total A+B**: 6 (75%) ✅ Exceeds 70% threshold

**User Demand**: 8 developers requesting (GitHub issues)
**Related SAPs**: SAP-004 (testing-framework), SAP-014 (mcp-server-development)
**Effort Estimate**: 12-20 hours
**ROI Potential**: 5x (based on reducing test writing time)

**Priority**: **HIGH**
**Recommended Wave**: **Wave 1** (Committed for v1.5.0)

**Rationale**: High evidence (75% A+B), strong user demand (8 developers), aligns with SAP-004 L2 maturity goals.

---

## Theme 3: MCP Integration & Tooling

**Intentions**: 6 (from inventory)
**Evidence Level**:
- Level A (Standards): 1 (17%)
- Level B (Case Studies): 4 (67%)
- Level C (Expert Opinion): 1 (17%)
- **Total A+B**: 5 (83%) ✅ Exceeds 70% threshold

**User Demand**: 8 developers requesting (MCP ecosystem)
**Related SAPs**: SAP-014 (mcp-server-development), SAP-017/018 (chora-compose)
**Effort Estimate**: 10-15 hours
**ROI Potential**: 8x (based on reducing MCP development time)

**Priority**: **MEDIUM**
**Recommended Wave**: **Wave 2** (Exploratory, validate via dogfooding)

**Rationale**: Very high evidence (83% A+B) but narrow audience (MCP developers). Recommend dogfooding pilot before ecosystem commitment.

---

## Theme 4: Performance Optimization

**Intentions**: 5 (from inventory)
**Evidence Level**:
- Level A (Standards): 1 (20%)
- Level B (Case Studies): 2 (40%)
- Level C (Expert Opinion): 2 (40%)
- **Total A+B**: 3 (60%) ❌ Below 70% threshold

**User Demand**: 3 users requesting
**Related SAPs**: SAP-025 (react-performance), SAP-032 (performance-optimization)
**Effort Estimate**: 15-25 hours
**ROI Potential**: 3x (based on improving Core Web Vitals)

**Priority**: **MEDIUM**
**Recommended Wave**: **Wave 2** (Exploratory, needs more evidence)

**Rationale**: Evidence below threshold (60% A+B), moderate user demand (3 users). Recommend gathering more production data before committing.

---

## Theme 5: Documentation Quality

**Intentions**: 4 (from inventory)
**Evidence Level**:
- Level A (Standards): 1 (25%)
- Level B (Case Studies): 1 (25%)
- Level C (Expert Opinion): 2 (50%)
- **Total A+B**: 2 (50%) ❌ Below 70% threshold

**User Demand**: 2 users requesting
**Related SAPs**: SAP-007 (documentation-framework), SAP-016 (link-validation)
**Effort Estimate**: 8-12 hours
**ROI Potential**: 2x (based on reducing documentation errors)

**Priority**: **LOW**
**Recommended Wave**: **Wave 3** (Aspirational, defer until more demand)

**Rationale**: Low evidence (50% A+B), low user demand (2 users), incremental improvement rather than capability gap.

---

## Recommendation Summary

**Commit to Wave 1** (v1.5.0, 3 months):
- Theme 1: Strategic Planning Infrastructure (14 intentions, 79% A+B, 4 requests)
- Theme 2: Testing & Quality Improvements (8 intentions, 75% A+B, 8 requests)

**Explore in Wave 2** (6 months, validate via dogfooding):
- Theme 3: MCP Integration & Tooling (6 intentions, 83% A+B, 8 requests)
- Theme 4: Performance Optimization (5 intentions, 60% A+B, 3 requests)

**Defer to Wave 3** (12 months, quarterly review):
- Theme 5: Documentation Quality (4 intentions, 50% A+B, 2 requests)

**Total Intentions Addressed**: 22/42 (52%) in Wave 1
**Remaining Intentions**: 20 (48%) deferred to Wave 2/3 or closed
```

---

### Deliverable 5: Protocol Spec Section 3.5
**File**: `docs/skilled-awareness/memory-system/protocol-spec.md` (update)
**Type**: Update existing (add new section)
**Effort**: 1.5 hours

**Description**: Add Section 3.5 "Strategic Knowledge Templates" to document the 4 new templates, `type` field usage, query patterns, and lifecycle.

**Content Outline**:
- **Section 3.5: Strategic Knowledge Templates**
  - 3.5.1: Overview (strategic vs operational knowledge)
  - 3.5.2: Template Reference (vision, intention, roadmap, theme)
  - 3.5.3: Type Field System (strategic-vision, intention-inventory, roadmap-milestone, strategic-theme-matrix)
  - 3.5.4: Query Patterns (find by type, find stale inventories, trace vision → roadmap → epic)
  - 3.5.5: Strategic Artifact Lifecycle (creation → quarterly review → archival)
  - 3.5.6: Integration Points (SAP-006 vision synthesis, SAP-015 backlog cascade, SAP-027 pilot discovery)

**Location in File**: After Section 3.4 (Agent Profiles), before Section 4 (Event Log Schema)

**Example Content**:
```markdown
### 3.5: Strategic Knowledge Templates

**Purpose**: Standardized templates for strategic planning artifacts (vision, intention inventory, roadmap milestones, theme matrices).

#### 3.5.1: Strategic vs Operational Knowledge

A-MEM knowledge notes serve two purposes:

**Operational Knowledge** (existing):
- Troubleshooting solutions
- Pattern learnings
- Configuration notes
- Personal preferences

**Strategic Knowledge** (NEW):
- Vision documents (multi-horizon plans)
- Intention inventories (consolidated user requests)
- Roadmap milestones (version goals)
- Strategic theme matrices (prioritization analysis)

**Distinction**: Use `type` field in frontmatter to distinguish.

#### 3.5.2: Template Reference

Four templates are provided in `.chora/memory/templates/`:

**1. vision-document-template.md**:
- **Purpose**: Create vision documents with capability waves
- **Horizons**: 3-month (committed), 6-month (exploratory), 12-month (aspirational)
- **Usage**: `cp .chora/memory/templates/vision-document-template.md .chora/memory/knowledge/notes/vision-{project}-{horizon}.md`
- **Frontmatter**: `type: strategic-vision`, `horizon`, `status`, `waves` array

**2. intention-inventory-template.md**:
- **Purpose**: Consolidate unfulfilled intentions from inbox, GitHub, dogfooding, research
- **Usage**: `cp .chora/memory/templates/intention-inventory-template.md .chora/memory/knowledge/notes/intention-inventory-{date}.md`
- **Frontmatter**: `type: intention-inventory`, `sources` object

**3. roadmap-milestone-template.md**:
- **Purpose**: Track roadmap milestones (from vision Wave 1) with linkage to beads epics
- **Usage**: `cp .chora/memory/templates/roadmap-milestone-template.md .chora/memory/knowledge/notes/milestone-{version}.md`
- **Frontmatter**: `type: roadmap-milestone`, `version`, `target_date`, `from_vision_wave`, `linked_to` array

**4. strategic-theme-matrix-template.md**:
- **Purpose**: Cluster intentions into strategic themes with prioritization
- **Usage**: `cp .chora/memory/templates/strategic-theme-matrix-template.md .chora/memory/knowledge/notes/strategic-themes-{date}.md`
- **Frontmatter**: `type: strategic-theme-matrix`, `input_inventory`

#### 3.5.3: Type Field System

**New Frontmatter Field**: `type`

**Valid Values**:
- `troubleshooting`: Operational knowledge (error solutions)
- `pattern-learning`: Operational knowledge (best practices)
- `strategic-vision`: Strategic knowledge (vision document)
- `intention-inventory`: Strategic knowledge (unfulfilled user intentions)
- `roadmap-milestone`: Strategic knowledge (version goals)
- `strategic-theme-matrix`: Strategic knowledge (theme prioritization)

**Example**:
```yaml
---
id: vision-chora-base-6-month
type: strategic-vision
horizon: 6-month
status: active
tags: [vision, strategic-planning, chora-base]
---
```

**Query by Type**:
```bash
# Find all vision documents
grep -l '"type": "strategic-vision"' .chora/memory/knowledge/notes/*.md

# Find latest intention inventory
grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | sort | tail -1

# Find all roadmap milestones
grep -l '"type": "roadmap-milestone"' .chora/memory/knowledge/notes/*.md
```

#### 3.5.4: Query Patterns

**Find Stale Inventories** (>3 months old):
```bash
grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | \
  xargs grep -l '"created": "2025-0[1-7]'
```

**Trace Vision → Roadmap → Epic**:
```bash
# Step 1: Find vision document
vision_id=$(grep -l '"id": "vision-chora-base-6-month"' .chora/memory/knowledge/notes/*.md | head -1)

# Step 2: Find linked roadmap milestones
grep -l "linked_to.*vision-chora-base-6-month" .chora/memory/knowledge/notes/*.md

# Step 3: Find beads epic ID in roadmap milestone
grep "beads-epic-" .chora/memory/knowledge/notes/milestone-v1.5.0.md

# Step 4: Show beads epic
bd show chora-base-xyz
```

**Find Active Visions**:
```bash
grep -l '"type": "strategic-vision"' .chora/memory/knowledge/notes/*.md | \
  xargs grep -l '"status": "active"'
```

#### 3.5.5: Strategic Artifact Lifecycle

**Creation** (monthly for inventories, quarterly for visions):
1. Copy template from `.chora/memory/templates/`
2. Fill frontmatter (id, type, tags, created, updated)
3. Fill body content
4. Save to `.chora/memory/knowledge/notes/{id}.md`
5. Update links.json (if linking to other notes)

**Quarterly Review** (vision documents):
1. Read active vision documents: `grep -l '"status": "active"' .chora/memory/knowledge/notes/vision-*.md`
2. Check Wave decision criteria (have exploratory items been validated?)
3. Update `status` field:
   - Wave 1 committed → delivered: Mark `status: archived`, link to milestone note
   - Wave 2 exploratory → committed: Promote to Wave 1 in new vision document
   - Wave 2 exploratory → deferred: Move to Wave 3 or remove
4. Create new vision document for next quarter

**Archival** (post-delivery):
1. Update `status: archived` in frontmatter
2. Add `delivered_date`, `outcome` fields
3. Link to roadmap milestone note (which version delivered this wave)
4. Keep in `.chora/memory/knowledge/notes/` for traceability (do NOT delete)

#### 3.5.6: Integration Points

**SAP-006 (Development Lifecycle)**: Vision synthesis workflow uses strategic templates
- **Phase 1.1 (Discovery)**: Creates intention inventory using `intention-inventory-template.md`
- **Phase 1.2 (Analysis)**: Creates strategic theme matrix using `strategic-theme-matrix-template.md`
- **Phase 1.3 (Vision Drafting)**: Creates vision document using `vision-document-template.md`
- **Phase 1.4 (Backlog Cascade)**: Creates roadmap milestone using `roadmap-milestone-template.md`

**SAP-015 (Task Tracking with Beads)**: Roadmap milestone links to beads epic
- **Vision Cascade**: Roadmap milestone `linked_to` field contains beads epic ID
- **Epic Metadata**: Beads epic metadata contains `from_vision_wave`, `roadmap_version`
- **Traceability**: Vision → roadmap → epic → tasks chain

**SAP-027 (Dogfooding Patterns)**: Pre-pilot discovery reads intention inventory
- **Week -1 Discovery**: Queries latest intention inventory for pilot candidate prioritization
- **Pilot Feedback**: Stores pilot final summary as knowledge note with tags `[dogfooding-feedback, {pattern}, vision-wave-{N}]`
- **Vision Update**: Quarterly vision review queries dogfooding feedback to update Wave 2 decision criteria
```

---

### Deliverable 6: Awareness Guide Strategic Planning Section
**File**: `docs/skilled-awareness/memory-system/awareness-guide.md` (update)
**Type**: Update existing (add new section)
**Effort**: 45 minutes

**Description**: Add "Strategic Planning Workflows" section to awareness-guide.md showing when/how to use each template with examples from chora-base.

**Content Outline**:
- **Strategic Planning Workflows** (new section after "Knowledge Graph Workflows")
  - When to use strategic templates
  - Intention Discovery Workflow (monthly)
  - Strategic Theme Analysis Workflow (quarterly)
  - Vision Drafting Workflow (quarterly)
  - Roadmap Milestone Creation Workflow (after vision Wave 1 commit)
  - Example: chora-base strategic planning cycle

**Example Content**:
```markdown
## Strategic Planning Workflows

### When to Use Strategic Templates

Use strategic templates when:
- **Monthly**: Consolidating unfulfilled intentions (inbox, GitHub, dogfooding, research)
- **Quarterly**: Synthesizing vision from intentions, reviewing Wave decision criteria
- **Post-Wave-Commit**: Creating roadmap milestones for committed vision waves
- **Post-Pilot**: Storing dogfooding feedback for vision decision updates

### Intention Discovery Workflow (Monthly)

**Trigger**: 1st of each month

**Inputs**:
- Inbox coordination requests: `cat inbox/coordination/active.jsonl`
- GitHub issues: Query `label:feature-request`
- Dogfooding feedback: `grep '"tags".*dogfooding-feedback' .chora/memory/knowledge/notes/*.md`
- Research reports: `ls docs/research/*-research.md`
- A-MEM knowledge notes: `grep '"tags".*user-request' .chora/memory/knowledge/notes/*.md`

**Steps**:
1. Copy template:
   ```bash
   cp .chora/memory/templates/intention-inventory-template.md \
      .chora/memory/knowledge/notes/intention-inventory-$(date +%Y-%m-%d).md
   ```

2. Fill frontmatter:
   - `id`: intention-inventory-{date}
   - `sources`: Update counts (inbox, github, dogfooding, research, a-mem)

3. Categorize intentions by evidence level:
   - **Level A** (Standards): IETF RFCs, W3C specs, peer-reviewed research
   - **Level B** (Case Studies): Production data, industry case studies (>100 users)
   - **Level C** (Expert Opinion): Blog posts, expert opinions, single-user requests

4. Add each intention with:
   - Title
   - Source (inbox, github, dogfooding, research, a-mem)
   - Evidence citation
   - User demand (count)
   - Related SAPs
   - Priority (HIGH/MEDIUM/LOW)

5. Calculate evidence percentages: A%, B%, C%

**Output**: intention-inventory-{date}.md

**Example** (chora-base Nov 2025):
- Scanned 89 unfulfilled intentions from discovery
- 14 High-Evidence (A): 16%
- 31 Medium-Evidence (B): 35%
- 44 Low-Evidence (C): 49%
- Top theme: Strategic Planning (14 intentions, HIGH priority)

### Strategic Theme Analysis Workflow (Quarterly)

**Trigger**: After intention inventory, before vision drafting

**Input**: Latest intention inventory

**Steps**:
1. Copy template:
   ```bash
   cp .chora/memory/templates/strategic-theme-matrix-template.md \
      .chora/memory/knowledge/notes/strategic-themes-$(date +%Y-%m-%d).md
   ```

2. Cluster intentions into themes (pattern recognition)

3. For each theme, calculate:
   - Intention count
   - Evidence level breakdown (A%, B%, C%)
   - User demand (sum across intentions)
   - Effort estimate
   - ROI potential

4. Apply Wave decision criteria:
   - **Wave 1 (Committed)**: Evidence A+B ≥ 70%, user demand ≥ 10, effort < 50 hours
   - **Wave 2 (Exploratory)**: Evidence A+B ≥ 60%, user demand ≥ 5, validate via dogfooding
   - **Wave 3 (Aspirational)**: Evidence A+B < 60%, user demand < 5, defer until more data

5. Rank themes by (evidence × demand × roi_potential)

**Output**: strategic-themes-{date}.md

**Example** (chora-base Nov 2025):
- 42 intentions → 5 themes
- Theme 1 (Strategic Planning): 79% A+B, 4 requests → Wave 1 ✅
- Theme 2 (Testing): 75% A+B, 8 requests → Wave 1 ✅
- Theme 3 (MCP): 83% A+B, 8 requests → Wave 2 (validate)
- Theme 4 (Performance): 60% A+B, 3 requests → Wave 2 (needs evidence)
- Theme 5 (Docs): 50% A+B, 2 requests → Wave 3 (defer)

### Vision Drafting Workflow (Quarterly)

**Trigger**: After strategic theme analysis

**Input**: Strategic theme matrix

**Steps**:
1. Copy template:
   ```bash
   cp .chora/memory/templates/vision-document-template.md \
      .chora/memory/knowledge/notes/vision-{project}-{horizon}.md
   ```

2. Fill frontmatter:
   - `horizon`: 3-month | 6-month | 12-month
   - `waves`: Array (wave 1: committed, wave 2: exploratory, wave 3: aspirational)
   - `status`: draft (until reviewed)

3. Write Wave 1 (Committed):
   - Features from HIGH-priority themes (evidence A+B ≥ 70%, user demand ≥ 10)
   - Target version (e.g., v1.5.0)
   - Success criteria (measurable outcomes)

4. Write Wave 2 (Exploratory):
   - Candidates from MEDIUM-priority themes (evidence A+B ≥ 60%, user demand ≥ 5)
   - Decision review date (quarterly)
   - Validation plan (dogfooding pilots)

5. Write Wave 3 (Aspirational):
   - Long-term vision from LOW-priority themes or future possibilities
   - Quarterly review (promote to Wave 2 or remove)

6. Update `status: active` after stakeholder review

**Output**: vision-{project}-{horizon}.md

**Example** (chora-base Nov 2025):
- Horizon: 6-month (Nov 2025 - Apr 2026)
- Wave 1: Strategic Planning Infrastructure (4 SAP enhancements, v1.5.0, Feb 2026)
- Wave 2: Automation & Tooling (4 CLIs, validate via dogfooding, decision Q1 2026)
- Wave 3: Ecosystem Adoption (3+ projects adopt, case studies, 12-month)

### Roadmap Milestone Creation Workflow (After Vision Wave 1 Commit)

**Trigger**: After vision Wave 1 finalized

**Input**: Vision document (Wave 1 section)

**Steps**:
1. Copy template:
   ```bash
   cp .chora/memory/templates/roadmap-milestone-template.md \
      .chora/memory/knowledge/notes/milestone-{version}.md
   ```

2. Fill frontmatter:
   - `version`: Target version (e.g., v1.5.0)
   - `target_date`: Delivery date
   - `from_vision_wave`: 1
   - `linked_to`: [vision-{project}-{horizon}]
   - `committed`: true

3. List features from Wave 1

4. Define success criteria (measurable)

5. Create beads epic (will be linked after epic created):
   ```bash
   bd create "Wave 1: {Theme} (v{version})" \
     --priority 1 \
     --type epic \
     --description "From vision-{project}-{horizon} Wave 1"
   ```

6. Update `linked_to` array with beads epic ID

**Output**: milestone-{version}.md, beads epic

**Example** (chora-base v1.5.0):
- Features: SAP-010, SAP-006, SAP-015, SAP-027 enhancements
- Success criteria: All 4 SAPs enhanced, workflow validated, ecosystem reusable
- Beads epic: chora-base-xyz (20 tasks estimated)
- Linked: vision-chora-base-6-month → milestone-v1.5.0 → beads-epic-xyz
```

---

### Deliverable 7: Ledger Update
**File**: `docs/skilled-awareness/memory-system/ledger.md` (update)
**Type**: Update existing (add version entry)
**Effort**: 15 minutes

**Description**: Document this enhancement in ledger.md as version 1.1.0.

**Content**: Add new version entry:
```markdown
### Version 1.1.0 (2025-11-05)

**Enhancement**: Strategic Knowledge Templates

**Changes**:
- Added 4 strategic knowledge templates (vision, intention inventory, roadmap milestone, strategic theme matrix)
- Added knowledge node type system (`type` field in frontmatter)
- Added strategic artifact lifecycle (creation → quarterly review → archival)
- Added query patterns for strategic knowledge (find by type, trace vision → roadmap → epic)
- Updated protocol-spec.md Section 3.5 (Strategic Knowledge Templates)
- Updated awareness-guide.md (Strategic Planning Workflows section)

**Integration**:
- SAP-006 (Development Lifecycle): Vision synthesis workflow uses strategic templates
- SAP-015 (Task Tracking): Roadmap milestone links to beads epic via `linked_to` field
- SAP-027 (Dogfooding Patterns): Pre-pilot discovery reads intention inventory

**Effort**: 4-6 hours (template creation, documentation, examples)
```

---

## 5. Execution Tasks

### Task 1: Create Vision Document Template
**Effort**: 1 hour
**Dependencies**: None

**Steps**:
1. Create file `.chora/memory/templates/vision-document-template.md`
2. Write YAML frontmatter (id, type, horizon, status, waves, tags, created, updated)
3. Write body structure (Wave 1/2/3 sections with placeholders)
4. Add example (chora-base 6-month vision)
5. Add usage instructions (copy template, fill frontmatter, fill waves)

**Output**: vision-document-template.md (ready to use)

---

### Task 2: Create Intention Inventory Template
**Effort**: 45 minutes
**Dependencies**: None

**Steps**:
1. Create file `.chora/memory/templates/intention-inventory-template.md`
2. Write YAML frontmatter (id, type, sources, tags, created, updated)
3. Write body structure (High/Medium/Low evidence sections with placeholders)
4. Add example (chora-base Nov 2025 inventory with 42 intentions)
5. Add evidence level definitions (A: Standards, B: Case Studies, C: Expert Opinion)

**Output**: intention-inventory-template.md (ready to use)

---

### Task 3: Create Roadmap Milestone Template
**Effort**: 45 minutes
**Dependencies**: None

**Steps**:
1. Create file `.chora/memory/templates/roadmap-milestone-template.md`
2. Write YAML frontmatter (id, type, version, target_date, from_vision_wave, committed, linked_to, tags, created, updated)
3. Write body structure (Features, Success Criteria, Linked Beads Epic sections)
4. Add example (chora-base v1.5.0 milestone with 4 SAP enhancements)
5. Add instructions for linking to beads epic

**Output**: roadmap-milestone-template.md (ready to use)

---

### Task 4: Create Strategic Theme Matrix Template
**Effort**: 45 minutes
**Dependencies**: None

**Steps**:
1. Create file `.chora/memory/templates/strategic-theme-matrix-template.md`
2. Write YAML frontmatter (id, type, input_inventory, tags, created, updated)
3. Write body structure (Theme 1/2/3... sections with intention count, evidence, user demand, priority, recommended wave)
4. Add example (chora-base 5 themes from 42 intentions)
5. Add Wave decision criteria (Wave 1: A+B ≥70%, Wave 2: A+B ≥60%, Wave 3: A+B <60%)

**Output**: strategic-theme-matrix-template.md (ready to use)

---

### Task 5: Update Protocol Spec Section 3.5
**Effort**: 1.5 hours
**Dependencies**: Tasks 1-4 (templates created)

**Steps**:
1. Read current protocol-spec.md to find insertion point (after Section 3.4 Agent Profiles)
2. Write Section 3.5: Strategic Knowledge Templates
   - 3.5.1: Overview (strategic vs operational knowledge)
   - 3.5.2: Template Reference (4 templates)
   - 3.5.3: Type Field System (strategic-vision, intention-inventory, roadmap-milestone, strategic-theme-matrix)
   - 3.5.4: Query Patterns (find by type, find stale, trace vision → roadmap → epic)
   - 3.5.5: Strategic Artifact Lifecycle (creation, quarterly review, archival)
   - 3.5.6: Integration Points (SAP-006, SAP-015, SAP-027)
3. Add examples and code snippets
4. Update Table of Contents

**Output**: Updated protocol-spec.md with Section 3.5

---

### Task 6: Update Awareness Guide Strategic Planning Section
**Effort**: 45 minutes
**Dependencies**: Tasks 1-4 (templates created)

**Steps**:
1. Read current awareness-guide.md to find insertion point (after "Knowledge Graph Workflows")
2. Write "Strategic Planning Workflows" section
   - When to use strategic templates
   - Intention Discovery Workflow (monthly)
   - Strategic Theme Analysis Workflow (quarterly)
   - Vision Drafting Workflow (quarterly)
   - Roadmap Milestone Creation Workflow (after Wave 1 commit)
   - Example: chora-base strategic planning cycle
3. Add step-by-step instructions with bash commands
4. Add examples from chora-base dogfooding

**Output**: Updated awareness-guide.md with strategic planning section

---

### Task 7: Update Ledger with Version 1.1.0
**Effort**: 15 minutes
**Dependencies**: Tasks 1-6 (all enhancements complete)

**Steps**:
1. Read current ledger.md to find version history section
2. Add version 1.1.0 entry with:
   - Date (2025-11-05)
   - Enhancement title (Strategic Knowledge Templates)
   - Changes (4 templates, type system, lifecycle, query patterns, docs)
   - Integration points (SAP-006, SAP-015, SAP-027)
   - Effort (4-6 hours)
3. Update "Maturity Level" section if L3 criteria met

**Output**: Updated ledger.md with version 1.1.0 entry

---

## 6. Success Criteria

### Functional
- ✅ 4 strategic knowledge templates exist in `.chora/memory/templates/`
- ✅ Templates have complete frontmatter (id, type, tags, created, updated)
- ✅ Templates have example content from chora-base dogfooding
- ✅ Type field system documented (`type`: strategic-vision, intention-inventory, roadmap-milestone, strategic-theme-matrix)
- ✅ Query patterns work (find by type, find stale, trace vision → roadmap → epic)

### Integration
- ✅ SAP-006 can use templates for vision synthesis workflow
- ✅ SAP-015 can link roadmap milestone to beads epic via `linked_to` field
- ✅ SAP-027 can read intention inventory for pilot discovery

### Documentation
- ✅ Protocol-spec.md Section 3.5 complete (Strategic Knowledge Templates)
- ✅ Awareness-guide.md has strategic planning workflows section
- ✅ Ledger.md documents version 1.1.0 enhancement
- ✅ Examples provided from chora-base dogfooding

---

## 7. Testing & Validation

### How to validate this enhancement:

**Test 1: Template Usability**
1. Copy vision-document-template.md to `notes/vision-test-{date}.md`
2. Fill frontmatter with test data
3. Fill Wave 1/2/3 sections
4. Verify file is valid markdown with frontmatter

**Test 2: Query Patterns**
1. Create test vision document with `type: strategic-vision`
2. Run query: `grep -l '"type": "strategic-vision"' .chora/memory/knowledge/notes/*.md`
3. Verify test vision document is found

**Test 3: Vision → Roadmap → Epic Traceability**
1. Create test vision document: `vision-test-6-month`
2. Create test roadmap milestone: `milestone-v1.0.0` with `linked_to: [vision-test-6-month]`
3. Create test beads epic: `bd create "Test epic"`
4. Update roadmap milestone `linked_to` with epic ID
5. Run trace query: `grep "linked_to.*vision-test-6-month" .chora/memory/knowledge/notes/*.md`
6. Verify roadmap milestone is found
7. Verify beads epic ID is in roadmap milestone

### Dogfooding Checklist:
- ✅ Use vision-document-template.md to create chora-base 6-month vision
- ✅ Use intention-inventory-template.md to document 89 unfulfilled intentions
- ✅ Use strategic-theme-matrix-template.md to analyze 5 themes
- ✅ Use roadmap-milestone-template.md to create v1.5.0 milestone
- ✅ Document usage in ledger.md version 1.1.0 entry
- ✅ Collect feedback: Were templates easy to use? Did they save time?

---

## 8. Boundaries & Integration Points

### This SAP Owns
- ✅ Strategic knowledge template storage (`.chora/memory/templates/`)
- ✅ Knowledge node type system (`type` field in frontmatter)
- ✅ Strategic artifact lifecycle (creation → quarterly review → archival)
- ✅ Query patterns for strategic knowledge (grep commands)
- ✅ Template schemas (frontmatter structure, body structure)

### This SAP Does NOT Own
- ❌ Vision synthesis workflow (owned by SAP-006 Development Lifecycle)
- ❌ Backlog cascade operations (owned by SAP-015 Task Tracking)
- ❌ Pilot discovery workflow (owned by SAP-027 Dogfooding Patterns)
- ❌ Beads epic creation (owned by SAP-015 Task Tracking)

### Integration Points

**SAP-010 → SAP-006 (Development Lifecycle)**:
- **Mechanism**: SAP-006 Phase 1 vision synthesis workflow uses SAP-010 strategic templates
- **Data Flow**: SAP-006 creates intention inventory → theme matrix → vision document using SAP-010 templates
- **Example**: SAP-006 Phase 1.1 Discovery copies `intention-inventory-template.md`, fills with data, saves to `.chora/memory/knowledge/notes/`

**SAP-010 ↔ SAP-015 (Task Tracking with Beads)**:
- **Mechanism**: Roadmap milestone note links to beads epic ID via `linked_to` field
- **Data Flow**: SAP-015 creates beads epic → SAP-010 roadmap milestone updated with epic ID → traceability established
- **Example**: Roadmap milestone `linked_to: [vision-chora-base-6-month, beads-epic-chora-base-xyz]`

**SAP-010 ← SAP-027 (Dogfooding Patterns)**:
- **Mechanism**: SAP-027 Week -1 discovery reads latest intention inventory from SAP-010
- **Data Flow**: SAP-010 stores intention inventory → SAP-027 queries `grep '"type": "intention-inventory"' ... | tail -1` → SAP-027 uses for pilot selection
- **Example**: SAP-027 pilot selection criteria filters intentions by evidence level (A+B ≥ 70%) from inventory

---

## 9. Rollout Plan

**Phase**: 1 (Foundation)
**Recommended Order**: Execute first (all other SAPs depend on templates)

**Parallel Execution**:
- ✅ Can execute in parallel with: SAP-027 (Pre-Pilot Discovery Plan) - SAP-027 doesn't strictly need templates until Week -1 discovery
- ❌ Must complete before: SAP-006 (Vision Synthesis Plan) - SAP-006 Phase 1 requires templates
- ❌ Must complete before: SAP-015 (Backlog Organization Plan) - SAP-015 vision cascade requires roadmap milestone template

**Critical Path**: This is on the critical path for strategic planning enhancements. All other SAPs blocked until templates exist.

---

## 10. Open Questions

None - plan is self-contained and ready to execute.

---

## 11. References

- **SAP-010 Current Artifacts**: `docs/skilled-awareness/memory-system/`
- **Research Findings**: Comprehensive SAP research conducted by Plan agent (2025-11-05)
- **Related Plans**:
  - `docs/project-docs/plans/sap-006-vision-synthesis-plan.md` (depends on this plan)
  - `docs/project-docs/plans/sap-015-backlog-organization-plan.md` (soft dependency on this plan)
  - `docs/project-docs/plans/sap-027-pre-pilot-discovery-plan.md` (can execute in parallel)
  - `docs/project-docs/plans/strategic-planning-enhancements-overview.md` (integration overview)
