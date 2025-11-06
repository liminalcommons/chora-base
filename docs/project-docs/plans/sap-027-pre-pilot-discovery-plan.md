# SAP-027 Pre-Pilot Discovery Enhancement Plan

**Plan ID**: PLAN-2025-11-05-SAP-027-PRE-PILOT-DISCOVERY
**SAP**: SAP-027 (Dogfooding Patterns)
**Version**: 1.1.0 (from 1.0.0)
**Priority**: P4 (Validation)
**Estimated Effort**: 4-6 hours
**Dependencies**: None (can execute in parallel with SAP-010)
**Created**: 2025-11-05
**Status**: Draft

---

## 1. Executive Summary

This plan enhances **SAP-027 (Dogfooding Patterns)** to add a **Week -1 Discovery Phase** before pilot execution, complete protocol-spec TODOs, and establish feedback loops connecting pilot results back to strategic vision (SAP-006) and operational backlog (SAP-015).

**Core Problem**: SAP-027 currently defines a 4-week pilot methodology (Week 0: Setup, Week 1-3: Execution, Week 4: Evaluation) but lacks a pre-pilot discovery phase for selecting which intentions to validate. Additionally, protocol-spec has 3 incomplete sections (Section 3: Integration Patterns, Section 4: Configuration, Section 5: Error Handling), and pilot results don't automatically feed back into vision or backlog.

**Solution**: Add 3 enhancements to SAP-027:
1. **Week -1 Discovery Phase**: Systematic process for selecting high-value pilot candidates from intention inventory (SAP-010), prioritizing by evidence level + user demand + strategic alignment
2. **Pilot → Vision Feedback Loop**: Successful pilots (GO decision) automatically update vision Wave 2 decision criteria, promoting exploratory features to roadmap-committed status
3. **Pilot → Backlog Integration**: GO decisions trigger beads epic creation (SAP-015) with priority promotion (P3 → P2), NO-GO decisions log lessons learned (SAP-010)
4. **Protocol-Spec Completion**: Complete Sections 3, 4, 5 (integration patterns, configuration schema, error handling)

**Why This Matters**: This enhancement closes the loop between strategic discovery (SAP-006) and validation (SAP-027), enabling teams to systematically test exploratory ideas via pilots and cascade successful results into committed roadmap and operational backlog.

**Deliverables**:
1. Protocol Spec Section 2 Enhancement (Week -1 Discovery Phase)
2. Protocol Spec Section 3 Enhancement (Integration Patterns)
3. Protocol Spec Section 4 (Configuration Schema)
4. Protocol Spec Section 5 (Error Handling)
5. Awareness Guide Pre-Pilot Discovery Examples
6. Ledger Update (version 1.1.0)

**Integration**:
- **← SAP-010 (Memory System)**: Reads intention inventory, logs pilot results and lessons learned
- **→ SAP-006 (Development Lifecycle)**: Updates vision Wave 2 decision criteria based on pilot GO/NO-GO
- **→ SAP-015 (Task Tracking)**: Creates beads epic on GO decision, promotes P3 → P2

**Success Criteria**:
- Week -1 discovery selects 3-5 pilot candidates in <2 hours
- Pilot GO decision creates beads epic with traceability metadata in <5 minutes
- Pilot NO-GO decision logs lessons learned to A-MEM in <5 minutes
- Vision Wave 2 decision criteria updated after pilot evaluation (evidence A+B%, user demand)

---

## 2. Current State

### 2.1 Artifact Completeness

All 5 SAP-027 artifacts exist and are complete:

| Artifact | Status | Location | Size |
|----------|--------|----------|------|
| Capability Charter | ✅ Complete | `docs/skilled-awareness/dogfooding-patterns/capability-charter.md` | 28 KB |
| Protocol Spec | ⚠️ Incomplete | `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md` | 42 KB |
| Awareness Guide | ✅ Complete | `docs/skilled-awareness/dogfooding-patterns/awareness-guide.md` | 15 KB |
| Adoption Blueprint | ✅ Complete | `docs/skilled-awareness/dogfooding-patterns/adoption-blueprint.md` | 12 KB |
| Ledger | ✅ Complete | `docs/skilled-awareness/dogfooding-patterns/ledger.md` | 8 KB |

**Current Version**: 1.0.0

**Note**: Protocol spec is marked complete but has 3 TODO sections (Sections 3, 4, 5).

### 2.2 Current Capabilities

SAP-027 currently provides:

1. **4-Week Pilot Methodology**:
   - **Week 0 (Setup)**: Define hypothesis, success criteria, test plan
   - **Week 1-3 (Execution)**: Run pilot, collect evidence, log to A-MEM
   - **Week 4 (Evaluation)**: Analyze results, make GO/NO-GO decision

2. **Pilot Evidence Levels**:
   - **Level A (Standards)**: IETF RFCs, W3C specs, PEPs, peer-reviewed research
   - **Level B (Case Studies)**: Production data, industry case studies
   - **Level C (Expert Opinion)**: Blog posts, expert opinions

3. **GO/NO-GO Decision Criteria**:
   - **GO**: Evidence A+B ≥60%, user demand ≥5, success criteria met
   - **NO-GO**: Evidence A+B <60%, user demand <5, success criteria failed

4. **A-MEM Integration**:
   - Pilot setup logged to `.chora/memory/events/dogfooding.jsonl`
   - Pilot results logged to `.chora/memory/events/dogfooding.jsonl`
   - Pilot evaluation logged to `.chora/memory/knowledge/notes/pilot-{id}-final.md`

### 2.3 Gaps in Pre-Pilot Discovery

**Gap 1: No Week -1 Discovery Phase**
- **Current**: Pilot methodology starts at Week 0 (Setup)
- **Missing**: Systematic process for selecting which intentions to validate via pilot
- **Impact**: Teams don't know how to choose pilot candidates from intention inventory (could pick low-value or low-feasibility ideas)

**Gap 2: No Pilot → Vision Feedback Loop**
- **Current**: Pilot results stay in A-MEM (`.chora/memory/knowledge/notes/pilot-{id}-final.md`)
- **Missing**: Mechanism to update vision Wave 2 decision criteria after pilot GO/NO-GO
- **Impact**: Successful pilots don't automatically promote exploratory features to roadmap-committed status

**Gap 3: No Pilot → Backlog Integration**
- **Current**: Protocol spec mentions "GO decision → roadmap" but no workflow
- **Missing**: Automated workflow for creating beads epic on GO, logging lessons learned on NO-GO
- **Impact**: Pilot results don't cascade into operational backlog (manual coordination required)

**Gap 4: Incomplete Protocol Spec Sections**
- **Current**: Sections 3, 4, 5 marked as TODO
  - Section 3: Integration Patterns (SAP-001, SAP-006, SAP-010, SAP-015)
  - Section 4: Configuration Schema (`.chora/config.yaml`)
  - Section 5: Error Handling (common failure modes, recovery strategies)
- **Missing**: Complete technical specification
- **Impact**: Teams can't adopt SAP-027 without these sections (unclear how to integrate, configure, handle errors)

**Gap 5: No Pre-Pilot Discovery Examples in Awareness Guide**
- **Current**: Awareness guide has pilot execution examples but no discovery examples
- **Missing**: Example workflow for selecting pilot candidates from intention inventory
- **Impact**: Teams struggle with "what should I pilot first?" question

---

## 3. Enhancement Overview

### 3.1 Week -1 Discovery Phase

Add new Week -1 phase before pilot setup:

**Purpose**: Systematically select 3-5 pilot candidates from intention inventory (SAP-010)

**Inputs**:
1. Intention inventory (SAP-010 knowledge note type `intention-inventory`)
2. Vision Wave 2 exploratory candidates (SAP-006 vision document)
3. Strategic theme matrix (SAP-010 knowledge note type `strategic-theme-matrix`)

**Activities**:
1. **Query Intention Inventory**: Find all intentions categorized as "exploratory" (evidence A+B 50-70%, user demand 3-10)
2. **Prioritize by Strategic Alignment**: Score intentions by alignment with strategic themes (0-10)
3. **Assess Pilot Feasibility**: Estimate pilot effort (1-3 weeks), risk (low/medium/high), reversibility (reversible/irreversible)
4. **Select Top 3-5 Candidates**: Rank by score = (evidence% × 0.4) + (strategic_alignment × 0.3) + (user_demand × 0.2) + (feasibility × 0.1)
5. **Document Pilot Candidates**: Log to A-MEM (`.chora/memory/knowledge/notes/pilot-candidates-{date}.md`)

**Output**: 3-5 pilot candidates with:
- Intention ID (from inventory)
- Pilot hypothesis ("If we implement X, then Y will improve by Z")
- Success criteria (measurable outcomes)
- Pilot effort (1-3 weeks)
- Risk level (low/medium/high)
- Strategic alignment score (0-10)

**Example**:
```markdown
---
id: pilot-candidates-2025-11-05
type: pilot-candidates
status: draft
tags: [dogfooding, pilot-discovery, strategic-planning]
created: 2025-11-05T00:00:00Z
---

# Pilot Candidates: 2025-11-05

**From**: intention-inventory-2025-11-04
**Vision Wave 2**: vision-chora-base-6-month

## Top 5 Candidates

### 1. SAP-015 Backlog Organization Patterns (Score: 8.7)
**Intention ID**: intention-089 (from inventory)
**Evidence**: A+B 65% (Level A: 25%, Level B: 40%)
**User Demand**: 7 requests (inbox + GitHub issues)
**Strategic Alignment**: 9/10 (aligns with "Strategic Planning Infrastructure" theme)
**Pilot Effort**: 2 weeks
**Risk**: Low (reversible, no breaking changes)
**Hypothesis**: If we add 5 backlog organization patterns to SAP-015, then teams can manage multi-tier backlogs 50% faster (from vision → backlog in <30 min vs current 60+ min)
**Success Criteria**:
- Vision cascade completes in <30 minutes
- Backlog health queries detect issues in <5 seconds
- Quarterly refinement reduces P3/P4 backlog by ≥20%

### 2. SAP-006 Vision Synthesis Workflow (Score: 8.5)
**Intention ID**: intention-067
**Evidence**: A+B 70% (Level A: 30%, Level B: 40%)
**User Demand**: 8 requests
**Strategic Alignment**: 10/10 (core strategic theme)
**Pilot Effort**: 3 weeks
**Risk**: Medium (changes to existing SAP-006 workflow)
**Hypothesis**: If we add 4-phase vision synthesis (Discovery → Analysis → Drafting → Cascade), then strategic planning cycles reduce from 2 weeks to 3 days
**Success Criteria**:
- Discovery phase completes in <2 days
- Vision draft completes in <4 hours
- Backlog cascade completes in <30 minutes

### 3. SAP-010 Strategic Templates (Score: 8.2)
... [3 more candidates]
```

### 3.2 Pilot → Vision Feedback Loop

Add workflow for updating vision Wave 2 decision criteria after pilot evaluation:

**Trigger**: Pilot evaluation complete, GO/NO-GO decision made

**Workflow (GO Decision)**:
1. Read pilot final summary (`.chora/memory/knowledge/notes/pilot-{id}-final.md`)
2. Extract updated evidence levels (A%, B%, C% from pilot)
3. Extract updated user demand (count from pilot feedback)
4. Read vision document (SAP-006 vision Wave 2)
5. Find matching intention in Wave 2 exploratory section
6. Update decision criteria with pilot evidence
7. Evaluate promotion criteria:
   - If evidence A+B ≥70% AND user demand ≥10 → **Promote to Wave 1** (committed)
   - If evidence A+B ≥60% AND user demand ≥5 → **Keep in Wave 2** (exploratory, validated)
8. Update vision document with new criteria
9. Log update to A-MEM (`.chora/memory/events/vision-updates.jsonl`)

**Workflow (NO-GO Decision)**:
1. Read pilot final summary
2. Extract lessons learned (what failed, why)
3. Read vision document (SAP-006 vision Wave 2)
4. Find matching intention in Wave 2 exploratory section
5. Update decision criteria with pilot evidence (likely low A+B%)
6. Evaluate demotion criteria:
   - If evidence A+B <50% OR user demand <3 → **Demote to Wave 3** (aspirational, not validated)
   - If evidence A+B <30% → **Remove from vision** (not viable)
7. Update vision document with new criteria
8. Log lessons learned to A-MEM (`.chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md`)

**Example (GO Decision)**:
```bash
# Pilot: SAP-015 Backlog Organization Patterns
# Result: GO (evidence A+B 75%, user demand 12)

# Read vision document
vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"

# Update Wave 2 → Wave 1 (promotion)
# Before: Wave 2 exploratory (evidence A+B 65%, user demand 7)
# After: Wave 1 committed (evidence A+B 75%, user demand 12)

# Log update to A-MEM
cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "2025-11-05T00:00:00Z",
  "event": "vision_wave_promotion",
  "pilot_id": "pilot-sap-015-2025-q4",
  "decision": "GO",
  "intention": "SAP-015 Backlog Organization Patterns",
  "from_wave": 2,
  "to_wave": 1,
  "evidence_before": {"A": 25, "B": 40, "C": 35},
  "evidence_after": {"A": 35, "B": 40, "C": 25},
  "user_demand_before": 7,
  "user_demand_after": 12
}
EOF
```

### 3.3 Pilot → Backlog Integration

Add workflow for cascading pilot GO decision into beads backlog (SAP-015):

**Trigger**: Pilot evaluation complete, GO decision made

**Workflow**:
1. Read pilot final summary (`.chora/memory/knowledge/notes/pilot-{id}-final.md`)
2. Extract feature name, target version, effort estimate
3. Create beads epic (P1 - NEXT):
   ```bash
   bd create "Epic: {Feature Name} (v{Version})" \
     --type epic \
     --priority 1 \
     --description "From pilot {pilot-id} GO decision. {Description}" \
     --metadata '{
       "from_dogfooding_pilot": "{pilot-id}",
       "decision": "GO",
       "target_version": "v{Version}",
       "pilot_evidence": {"A": 35, "B": 40, "C": 25}
     }'
   ```
4. If pilot had pre-existing P3 task (SOMEDAY), promote to P2 (LATER):
   ```bash
   bd update {task-id} --priority 2 --metadata '{
     "from_dogfooding_pilot": "{pilot-id}",
     "decision": "GO"
   }'
   ```
5. Link epic to roadmap milestone (SAP-010):
   ```bash
   # Create roadmap milestone note
   cat > .chora/memory/knowledge/notes/roadmap-{project}-v{version}.md <<EOF
   ---
   id: roadmap-{project}-v{version}
   type: roadmap-milestone
   version: v{Version}
   from_pilot: {pilot-id}
   beads_epic: {epic-id}
   ---
   # Roadmap Milestone: {Feature Name} (v{Version})
   From pilot {pilot-id} GO decision.
   EOF
   ```
6. Log epic creation to A-MEM (`.chora/memory/events/backlog-updates.jsonl`)

**Example (GO Decision)**:
```bash
# Pilot: SAP-015 Backlog Organization Patterns
# Result: GO (evidence A+B 75%, user demand 12)

# Create beads epic
epic_id=$(bd create "Epic: SAP-015 Backlog Organization (v1.1.0)" \
  --type epic \
  --priority 1 \
  --description "From pilot-sap-015-2025-q4 GO decision. Add 5 backlog organization patterns." \
  --metadata '{
    "from_dogfooding_pilot": "pilot-sap-015-2025-q4",
    "decision": "GO",
    "target_version": "v1.1.0",
    "pilot_evidence": {"A": 35, "B": 40, "C": 25}
  }')

# Log epic creation
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "2025-11-05T00:00:00Z",
  "event": "epic_created_from_pilot",
  "pilot_id": "pilot-sap-015-2025-q4",
  "decision": "GO",
  "epic_id": "$epic_id",
  "target_version": "v1.1.0"
}
EOF
```

**Workflow (NO-GO Decision)**:
1. Read pilot final summary
2. Extract lessons learned (what failed, why)
3. Log lessons learned to A-MEM:
   ```bash
   cat > .chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md <<EOF
   ---
   id: lessons-learned-{pilot-id}
   type: lessons-learned
   pilot_id: {pilot-id}
   decision: NO-GO
   tags: [dogfooding, lessons-learned]
   created: {ISO-8601}
   ---
   # Lessons Learned: {Pilot Name}

   ## What Failed
   - {Failure 1}
   - {Failure 2}

   ## Why It Failed
   - {Root Cause 1}
   - {Root Cause 2}

   ## What We Learned
   - {Lesson 1}
   - {Lesson 2}

   ## Future Recommendations
   - {Recommendation 1}
   - {Recommendation 2}
   EOF
   ```
4. If pilot had pre-existing P3 task (SOMEDAY), demote to P4 (BACKLOG) or close:
   ```bash
   bd update {task-id} --priority 4 --metadata '{
     "from_dogfooding_pilot": "{pilot-id}",
     "decision": "NO-GO",
     "reason": "{Failure Reason}"
   }'
   # OR close entirely
   bd close {task-id} --reason "Pilot NO-GO: {Failure Reason}"
   ```

### 3.4 Protocol Spec Completion

Complete 3 TODO sections in protocol-spec.md:

**Section 3: Integration Patterns**
- 3.1: SAP-001 Integration (coordination requests → pilot candidates)
- 3.2: SAP-006 Integration (pilot results → vision updates)
- 3.3: SAP-010 Integration (A-MEM logging, intention inventory, lessons learned)
- 3.4: SAP-015 Integration (GO decision → beads epic)

**Section 4: Configuration Schema**
- 4.1: `.chora/config.yaml` schema for dogfooding settings
- 4.2: Default configuration values
- 4.3: Environment-specific overrides

**Section 5: Error Handling**
- 5.1: Common failure modes (pilot execution failures, decision criteria conflicts)
- 5.2: Recovery strategies (rollback, re-pilot, abort)
- 5.3: Error logging to A-MEM

### 3.5 Awareness Guide Pre-Pilot Discovery Examples

Add new section to awareness-guide.md with 3 examples:

**Example 1: Week -1 Discovery Workflow**
- Query intention inventory for exploratory candidates
- Prioritize by strategic alignment + evidence + user demand
- Select top 3-5 pilot candidates
- Document pilot hypotheses and success criteria

**Example 2: Pilot GO Decision → Vision + Backlog Cascade**
- Pilot evaluation completes, GO decision made
- Update vision Wave 2 → Wave 1 (promotion)
- Create beads epic (P1) with traceability metadata
- Log updates to A-MEM

**Example 3: Pilot NO-GO Decision → Lessons Learned**
- Pilot evaluation completes, NO-GO decision made
- Extract lessons learned (what failed, why)
- Log lessons learned to A-MEM
- Demote or close pre-existing P3 task
- Update vision Wave 2 → Wave 3 (demotion) or remove entirely

---

## 4. Detailed Deliverables

### Deliverable 1: Protocol Spec Section 2 Enhancement (Week -1 Discovery)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Section to Add**: Section 2.0 (before existing Week 0: Setup)

**Content** (~6 pages):

```markdown
### 2.0: Week -1 - Discovery Phase (NEW)

**Duration**: 1-2 days
**Goal**: Select 3-5 high-value pilot candidates from intention inventory

#### 2.0.1: Inputs

1. **Intention Inventory** (SAP-010): `.chora/memory/knowledge/notes/intention-inventory-{date}.md`
2. **Vision Wave 2** (SAP-006): Vision document exploratory section
3. **Strategic Theme Matrix** (SAP-010): `.chora/memory/knowledge/notes/strategic-theme-matrix-{date}.md`

#### 2.0.2: Activities

**Step 1: Query Intention Inventory**

```bash
# Find all exploratory intentions (evidence A+B 50-70%, user demand 3-10)
grep -l '"evidence_level".*"exploratory"' .chora/memory/knowledge/notes/intention-inventory-*.md | tail -1
```

**Step 2: Prioritize by Strategic Alignment**

For each intention:
1. Read strategic theme matrix
2. Score alignment with current themes (0-10)
3. Example scoring:
   - **10**: Core strategic theme (Vision Wave 1)
   - **7-9**: Exploratory strategic theme (Vision Wave 2)
   - **4-6**: Adjacent to strategic theme
   - **1-3**: Tangential to strategic theme
   - **0**: Not aligned with any theme

**Step 3: Assess Pilot Feasibility**

For each intention:
1. Estimate pilot effort (1-3 weeks)
2. Assess risk (low/medium/high):
   - **Low**: Reversible, no breaking changes, isolated scope
   - **Medium**: Reversible, minor breaking changes, moderate scope
   - **High**: Irreversible, major breaking changes, wide scope
3. Assess reversibility (reversible/irreversible)

**Step 4: Calculate Pilot Score**

For each intention, calculate score:
```
score = (evidence_A_plus_B% × 0.4) + (strategic_alignment × 0.3) + (user_demand × 0.2) + (feasibility × 0.1)
```

Where:
- `evidence_A_plus_B%`: Evidence Level A + B percentage (0-100)
- `strategic_alignment`: Strategic alignment score (0-10)
- `user_demand`: User demand count (0-100+)
- `feasibility`: Feasibility score (0-10, inversely proportional to effort and risk)

**Example**:
```
Intention: SAP-015 Backlog Organization Patterns
evidence_A_plus_B% = 65
strategic_alignment = 9
user_demand = 7
feasibility = 8 (2 weeks effort, low risk)

score = (65 × 0.4) + (9 × 0.3) + (7 × 0.2) + (8 × 0.1)
      = 26 + 2.7 + 1.4 + 0.8
      = 30.9
      = 8.7 / 10 (normalized)
```

**Step 5: Select Top 3-5 Candidates**

Sort intentions by score (descending), select top 3-5.

**Step 6: Document Pilot Candidates**

Create pilot candidates note:
```bash
cat > .chora/memory/knowledge/notes/pilot-candidates-$(date +%Y-%m-%d).md <<'EOF'
---
id: pilot-candidates-{date}
type: pilot-candidates
status: draft
from_intention_inventory: intention-inventory-{date}
from_vision: vision-{project}-{horizon}
tags: [dogfooding, pilot-discovery, strategic-planning]
created: {ISO-8601}
---

# Pilot Candidates: {Date}

**From**: intention-inventory-{date}
**Vision Wave 2**: vision-{project}-{horizon}

## Top 5 Candidates

### 1. {Intention Name} (Score: {Score})
**Intention ID**: {intention-id}
**Evidence**: A+B {%} (Level A: {%}, Level B: {%})
**User Demand**: {count} requests
**Strategic Alignment**: {score}/10
**Pilot Effort**: {weeks} weeks
**Risk**: {low/medium/high}
**Hypothesis**: {If we implement X, then Y will improve by Z}
**Success Criteria**:
- {Criterion 1}
- {Criterion 2}
- {Criterion 3}

### 2. {Intention Name} (Score: {Score})
...
EOF
```

#### 2.0.3: Outputs

- **Pilot Candidates Note**: `.chora/memory/knowledge/notes/pilot-candidates-{date}.md`
- **Next Step**: Select 1 candidate, proceed to Week 0 (Setup)

#### 2.0.4: Decision: Which Candidate to Pilot?

**Factors**:
1. **Highest Score**: Default to top-ranked candidate
2. **Team Capacity**: Choose candidate matching available effort (1-3 weeks)
3. **Strategic Urgency**: Prioritize candidates aligned with near-term roadmap (v1.x vs v2.x)
4. **Risk Appetite**: If low risk tolerance, choose low-risk candidate (even if lower score)

**Example**:
```
Top 5 Candidates:
1. SAP-015 Backlog Organization (Score: 8.7, Effort: 2 weeks, Risk: Low)
2. SAP-006 Vision Synthesis (Score: 8.5, Effort: 3 weeks, Risk: Medium)
3. SAP-010 Strategic Templates (Score: 8.2, Effort: 1.5 weeks, Risk: Low)
4. SAP-027 Pre-Pilot Discovery (Score: 7.9, Effort: 1 week, Risk: Low)
5. SAP-029 SAP Generation (Score: 7.5, Effort: 2 weeks, Risk: Medium)

Decision: Pilot SAP-015 (highest score, low risk, 2-week effort matches team capacity)
```

#### 2.0.5: Integration with Vision Wave 2 (SAP-006)

All pilot candidates should come from Vision Wave 2 exploratory section. This ensures pilots validate strategic exploratory work, not random ideas.

**Workflow**:
1. Read vision Wave 2 section
2. Extract all exploratory features (evidence A+B 50-70%, user demand 3-10)
3. Match against intention inventory
4. Prioritize using score formula (Section 2.0.2)
5. Select top 3-5 candidates
```

---

### Deliverable 2: Protocol Spec Section 3 Enhancement (Integration Patterns)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Section to Add**: Section 3 (complete TODO)

**Content** (~8 pages):

```markdown
## 3. Integration Patterns

This section documents how SAP-027 integrates with other SAPs in the chora-base ecosystem.

### 3.1: SAP-001 Integration (Inbox)

**Purpose**: Coordination requests can trigger pilot discovery

**Workflow**:
1. User creates coordination request in inbox (SAP-001)
2. Coordination request includes feature request, user demand signal
3. During Week -1 discovery, query active coordination requests:
   ```bash
   cat inbox/coordination/active.jsonl | jq -r '.[] | select(.type == "feature_request")'
   ```
4. Add coordination requests to intention inventory (SAP-010)
5. Include in pilot candidate prioritization

**Example**:
```jsonl
{
  "id": "coord-2025-11-05-001",
  "type": "feature_request",
  "title": "Add backlog organization patterns to SAP-015",
  "requester": "chora-base user",
  "user_demand": 7,
  "created": "2025-11-05T00:00:00Z"
}
```

This coordination request becomes intention in inventory, then pilot candidate.

---

### 3.2: SAP-006 Integration (Development Lifecycle)

**Purpose**: Pilot results update vision Wave 2 decision criteria

**Workflow (GO Decision)**:
1. Pilot evaluation complete, GO decision made
2. Read vision document (SAP-006): `.chora/memory/knowledge/notes/vision-{project}-{horizon}.md`
3. Find matching intention in Vision Wave 2 exploratory section
4. Update decision criteria:
   - **Evidence A+B%**: Update from pilot results (e.g., 65% → 75%)
   - **User Demand**: Update from pilot feedback (e.g., 7 → 12 requests)
5. Evaluate promotion criteria:
   - **Promote to Wave 1** (committed): If evidence A+B ≥70% AND user demand ≥10
   - **Keep in Wave 2** (exploratory): If evidence A+B ≥60% AND user demand ≥5
6. Update vision document with new criteria
7. Log update to A-MEM:
   ```bash
   cat >> .chora/memory/events/vision-updates.jsonl <<EOF
   {
     "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
     "event": "vision_wave_promotion",
     "pilot_id": "{pilot-id}",
     "decision": "GO",
     "intention": "{Intention Name}",
     "from_wave": 2,
     "to_wave": 1,
     "evidence_before": {"A": 25, "B": 40, "C": 35},
     "evidence_after": {"A": 35, "B": 40, "C": 25},
     "user_demand_before": 7,
     "user_demand_after": 12
   }
   EOF
   ```

**Workflow (NO-GO Decision)**:
1. Pilot evaluation complete, NO-GO decision made
2. Read vision document
3. Find matching intention in Vision Wave 2
4. Update decision criteria (evidence likely decreased)
5. Evaluate demotion criteria:
   - **Demote to Wave 3** (aspirational): If evidence A+B <50% OR user demand <3
   - **Remove from vision**: If evidence A+B <30%
6. Update vision document
7. Log lessons learned to A-MEM:
   ```bash
   cat > .chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md <<EOF
   ---
   id: lessons-learned-{pilot-id}
   type: lessons-learned
   pilot_id: {pilot-id}
   decision: NO-GO
   intention: {Intention Name}
   tags: [dogfooding, lessons-learned]
   created: {ISO-8601}
   ---

   # Lessons Learned: {Pilot Name}

   ## What Failed
   - {Failure 1}
   - {Failure 2}

   ## Why It Failed
   - {Root Cause 1}
   - {Root Cause 2}

   ## What We Learned
   - {Lesson 1}
   - {Lesson 2}

   ## Future Recommendations
   - {Recommendation 1}
   - {Recommendation 2}
   EOF
   ```

---

### 3.3: SAP-010 Integration (Memory System)

**Purpose**: SAP-027 uses SAP-010 for intention inventory, pilot logging, lessons learned

**Integration Points**:

**1. Intention Inventory (Week -1 Discovery)**
- **Input**: `.chora/memory/knowledge/notes/intention-inventory-{date}.md` (SAP-010 knowledge note type `intention-inventory`)
- **Usage**: Query exploratory intentions for pilot candidate selection
- **Query**:
  ```bash
  grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | tail -1
  ```

**2. Pilot Candidates Note (Week -1 Discovery)**
- **Output**: `.chora/memory/knowledge/notes/pilot-candidates-{date}.md` (SAP-010 knowledge note type `pilot-candidates`)
- **Usage**: Document top 3-5 pilot candidates with scores, hypotheses, success criteria

**3. Pilot Setup Logging (Week 0 Setup)**
- **Output**: `.chora/memory/events/dogfooding.jsonl` (SAP-010 event log)
- **Usage**: Log pilot setup (hypothesis, success criteria, timeline)

**4. Pilot Results Logging (Week 4 Evaluation)**
- **Output**: `.chora/memory/events/dogfooding.jsonl` (SAP-010 event log)
- **Usage**: Log pilot results (GO/NO-GO, evidence, user demand)

**5. Pilot Final Summary (Week 4 Evaluation)**
- **Output**: `.chora/memory/knowledge/notes/pilot-{id}-final.md` (SAP-010 knowledge note type `pilot-final-summary`)
- **Usage**: Complete pilot report (setup, execution, evaluation, decision, next steps)

**6. Lessons Learned (NO-GO Decision)**
- **Output**: `.chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md` (SAP-010 knowledge note type `lessons-learned`)
- **Usage**: Document what failed, why, lessons learned, recommendations

**7. Strategic Theme Matrix (Week -1 Discovery)**
- **Input**: `.chora/memory/knowledge/notes/strategic-theme-matrix-{date}.md` (SAP-010 knowledge note type `strategic-theme-matrix`)
- **Usage**: Score pilot candidates by strategic alignment

**8. Roadmap Milestone (GO Decision)**
- **Output**: `.chora/memory/knowledge/notes/roadmap-{project}-v{version}.md` (SAP-010 knowledge note type `roadmap-milestone`)
- **Usage**: Document roadmap commitment from pilot GO decision

---

### 3.4: SAP-015 Integration (Task Tracking)

**Purpose**: Pilot GO decisions cascade into beads backlog

**Workflow (GO Decision)**:

**Step 1: Create Beads Epic**
```bash
epic_id=$(bd create "Epic: {Feature Name} (v{Version})" \
  --type epic \
  --priority 1 \
  --description "From pilot {pilot-id} GO decision. {Description}" \
  --metadata '{
    "from_dogfooding_pilot": "{pilot-id}",
    "decision": "GO",
    "target_version": "v{Version}",
    "pilot_evidence": {"A": {%}, "B": {%}, "C": {%}}
  }')
```

**Step 2: Promote Existing P3 Task (if exists)**
```bash
# Find P3 task linked to intention
task_id=$(bd list --status open --priority 3 --json | jq -r '.[] | select(.metadata.intention_id == "{intention-id}") | .id')

# Promote to P2 (LATER)
bd update $task_id --priority 2 --metadata '{
  "from_dogfooding_pilot": "{pilot-id}",
  "decision": "GO"
}'
```

**Step 3: Link Epic to Roadmap Milestone (SAP-010)**
```bash
# Update epic with roadmap milestone link
bd update $epic_id --metadata '{
  "roadmap_milestone_note": "roadmap-{project}-v{version}"
}'
```

**Step 4: Log Epic Creation to A-MEM**
```bash
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "epic_created_from_pilot",
  "pilot_id": "{pilot-id}",
  "decision": "GO",
  "epic_id": "$epic_id",
  "target_version": "v{Version}"
}
EOF
```

**Workflow (NO-GO Decision)**:

**Step 1: Demote or Close Existing P3 Task (if exists)**
```bash
# Find P3 task linked to intention
task_id=$(bd list --status open --priority 3 --json | jq -r '.[] | select(.metadata.intention_id == "{intention-id}") | .id')

# Option 1: Demote to P4 (BACKLOG)
bd update $task_id --priority 4 --metadata '{
  "from_dogfooding_pilot": "{pilot-id}",
  "decision": "NO-GO",
  "reason": "{Failure Reason}"
}'

# Option 2: Close entirely
bd close $task_id --reason "Pilot NO-GO: {Failure Reason}"
```

**Step 2: Log Task Update to A-MEM**
```bash
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "task_closed_from_pilot",
  "pilot_id": "{pilot-id}",
  "decision": "NO-GO",
  "task_id": "$task_id",
  "reason": "{Failure Reason}"
}
EOF
```

---

### 3.5: Integration Summary

| SAP | Integration Point | Direction | Trigger | Output |
|-----|-------------------|-----------|---------|--------|
| SAP-001 | Coordination requests | ← | Feature request in inbox | Intention in inventory |
| SAP-006 | Vision updates | → | Pilot GO/NO-GO | Vision Wave promotion/demotion |
| SAP-010 | Intention inventory | ← | Week -1 discovery | Pilot candidates |
| SAP-010 | Pilot logging | → | Pilot setup, evaluation | A-MEM events, knowledge notes |
| SAP-015 | Beads epic creation | → | Pilot GO | Epic (P1), task promotion (P3 → P2) |
| SAP-015 | Task demotion | → | Pilot NO-GO | Task demotion (P3 → P4) or closure |
```

---

### Deliverable 3: Protocol Spec Section 4 (Configuration Schema)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Section to Add**: Section 4 (complete TODO)

**Content** (~3 pages):

```markdown
## 4. Configuration Schema

This section documents the configuration schema for SAP-027 in `.chora/config.yaml`.

### 4.1: Schema

```yaml
dogfooding:
  # Pilot defaults
  pilot:
    default_duration_weeks: 4  # Week 0 + 1-3 execution + Week 4 evaluation
    default_evidence_threshold:
      go:
        evidence_a_plus_b_min: 60  # Minimum evidence A+B% for GO decision
        user_demand_min: 5         # Minimum user demand count for GO
      no_go:
        evidence_a_plus_b_max: 59  # Maximum evidence A+B% triggers NO-GO
        user_demand_max: 4         # Maximum user demand triggers NO-GO

  # Vision integration (SAP-006)
  vision:
    auto_update_on_go: true        # Automatically update vision on GO decision
    promotion_threshold:
      wave_2_to_1:
        evidence_a_plus_b_min: 70  # Promote Wave 2 → Wave 1 if A+B ≥ 70%
        user_demand_min: 10        # Promote Wave 2 → Wave 1 if demand ≥ 10
      wave_3_to_2:
        evidence_a_plus_b_min: 60  # Promote Wave 3 → Wave 2 if A+B ≥ 60%
        user_demand_min: 5         # Promote Wave 3 → Wave 2 if demand ≥ 5
    demotion_threshold:
      wave_2_to_3:
        evidence_a_plus_b_max: 49  # Demote Wave 2 → Wave 3 if A+B < 50%
        user_demand_max: 2         # Demote Wave 2 → Wave 3 if demand < 3
      remove:
        evidence_a_plus_b_max: 29  # Remove from vision if A+B < 30%

  # Backlog integration (SAP-015)
  backlog:
    auto_create_epic_on_go: true   # Automatically create beads epic on GO
    auto_promote_task_on_go: true  # Automatically promote P3 → P2 on GO
    epic_priority: 1               # Priority for epics created from GO decision (P1 - NEXT)
    task_priority_after_go: 2      # Priority for promoted tasks (P2 - LATER)
    auto_demote_task_on_no_go: true  # Automatically demote P3 → P4 on NO-GO
    task_priority_after_no_go: 4   # Priority for demoted tasks (P4 - BACKLOG)

  # A-MEM integration (SAP-010)
  memory:
    log_pilot_setup: true          # Log pilot setup to A-MEM
    log_pilot_results: true        # Log pilot results to A-MEM
    log_vision_updates: true       # Log vision updates to A-MEM
    log_backlog_updates: true      # Log backlog updates to A-MEM
    log_lessons_learned: true      # Log lessons learned on NO-GO

  # Discovery (Week -1)
  discovery:
    candidate_count: 5             # Number of pilot candidates to select
    score_weights:
      evidence: 0.4                # Weight for evidence A+B% (0-1)
      strategic_alignment: 0.3     # Weight for strategic alignment (0-1)
      user_demand: 0.2             # Weight for user demand (0-1)
      feasibility: 0.1             # Weight for feasibility (0-1)
```

### 4.2: Default Configuration

If `.chora/config.yaml` does not exist or `dogfooding` section is missing, use these defaults:

```yaml
dogfooding:
  pilot:
    default_duration_weeks: 4
    default_evidence_threshold:
      go:
        evidence_a_plus_b_min: 60
        user_demand_min: 5
      no_go:
        evidence_a_plus_b_max: 59
        user_demand_max: 4
  vision:
    auto_update_on_go: true
    promotion_threshold:
      wave_2_to_1:
        evidence_a_plus_b_min: 70
        user_demand_min: 10
      wave_3_to_2:
        evidence_a_plus_b_min: 60
        user_demand_min: 5
    demotion_threshold:
      wave_2_to_3:
        evidence_a_plus_b_max: 49
        user_demand_max: 2
      remove:
        evidence_a_plus_b_max: 29
  backlog:
    auto_create_epic_on_go: true
    auto_promote_task_on_go: true
    epic_priority: 1
    task_priority_after_go: 2
    auto_demote_task_on_no_go: true
    task_priority_after_no_go: 4
  memory:
    log_pilot_setup: true
    log_pilot_results: true
    log_vision_updates: true
    log_backlog_updates: true
    log_lessons_learned: true
  discovery:
    candidate_count: 5
    score_weights:
      evidence: 0.4
      strategic_alignment: 0.3
      user_demand: 0.2
      feasibility: 0.1
```

### 4.3: Environment-Specific Overrides

Teams can override defaults per environment (e.g., `production` vs `pilot`):

```yaml
dogfooding:
  pilot:
    default_duration_weeks: 4
  vision:
    auto_update_on_go: true
  backlog:
    auto_create_epic_on_go: true

  # Environment overrides
  environments:
    production:
      pilot:
        default_evidence_threshold:
          go:
            evidence_a_plus_b_min: 70  # Stricter threshold for production
            user_demand_min: 10

    pilot:
      pilot:
        default_evidence_threshold:
          go:
            evidence_a_plus_b_min: 50  # More lenient for pilot projects
            user_demand_min: 3
```

**Usage**:
```bash
# Use production config
export CHORA_ENV=production
# Pilot GO threshold: A+B ≥ 70%, demand ≥ 10

# Use pilot config
export CHORA_ENV=pilot
# Pilot GO threshold: A+B ≥ 50%, demand ≥ 3
```
```

---

### Deliverable 4: Protocol Spec Section 5 (Error Handling)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Section to Add**: Section 5 (complete TODO)

**Content** (~3 pages):

```markdown
## 5. Error Handling

This section documents common failure modes and recovery strategies.

### 5.1: Common Failure Modes

**Failure 1: Pilot Execution Timeout**
- **Symptom**: Pilot exceeds default duration (4 weeks), no evaluation completed
- **Root Cause**: Underestimated effort, scope creep, blocked dependencies
- **Impact**: Backlog stalled, team capacity wasted

**Failure 2: Decision Criteria Conflict**
- **Symptom**: Evidence A+B ≥60% (GO) but user demand <5 (NO-GO), unclear decision
- **Root Cause**: Conflicting criteria, unclear threshold priorities
- **Impact**: Decision paralysis, delayed roadmap

**Failure 3: Vision Update Failure (SAP-006 Integration)**
- **Symptom**: Pilot GO decision made, but vision document not updated
- **Root Cause**: Vision file missing, malformed YAML frontmatter, write permission error
- **Impact**: Pilot results isolated, no strategic feedback loop

**Failure 4: Backlog Update Failure (SAP-015 Integration)**
- **Symptom**: Pilot GO decision made, but beads epic not created
- **Root Cause**: Beads CLI not installed, `.beads/` directory missing, bd command error
- **Impact**: Pilot results not cascaded to backlog, manual coordination required

**Failure 5: Lessons Learned Not Documented (NO-GO Decision)**
- **Symptom**: Pilot NO-GO decision made, no lessons learned logged to A-MEM
- **Root Cause**: Forgot to document, rushed evaluation, unclear responsibility
- **Impact**: Failed pilots repeated, no organizational learning

### 5.2: Recovery Strategies

**Recovery 1: Pilot Execution Timeout → Abort or Extend**

**Decision Tree**:
```
Is pilot blocked by external dependency?
  YES → Extend pilot by 1 week, reassess
  NO  → Is pilot >50% complete?
    YES → Extend by 1 week, complete evaluation
    NO  → Abort pilot, log NO-GO with reason "timeout"
```

**Abort Workflow**:
```bash
# Log abort to A-MEM
cat >> .chora/memory/events/dogfooding.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "pilot_aborted",
  "pilot_id": "{pilot-id}",
  "reason": "timeout",
  "duration_actual": "{weeks} weeks",
  "duration_planned": "4 weeks"
}
EOF

# Document lessons learned
cat > .chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md <<EOF
---
id: lessons-learned-{pilot-id}
type: lessons-learned
pilot_id: {pilot-id}
decision: ABORT
reason: timeout
---

# Lessons Learned: {Pilot Name} (ABORT)

## Why Timeout Occurred
- {Root Cause 1}
- {Root Cause 2}

## What We Learned
- Effort underestimated by {X}%
- Scope should have been reduced to {Scope}

## Future Recommendations
- Use {X}-week buffer for similar pilots
- Reduce scope to {Scope} before starting
EOF
```

**Extend Workflow**:
```bash
# Log extension to A-MEM
cat >> .chora/memory/events/dogfooding.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "pilot_extended",
  "pilot_id": "{pilot-id}",
  "reason": "blocked dependency",
  "duration_new": "5 weeks"
}
EOF
```

---

**Recovery 2: Decision Criteria Conflict → Manual Decision with Rationale**

**Workflow**:
```bash
# Document conflict in pilot final summary
cat >> .chora/memory/knowledge/notes/pilot-{id}-final.md <<EOF

## Decision Criteria Conflict

**Evidence A+B**: 65% (≥60%, suggests GO)
**User Demand**: 4 requests (<5, suggests NO-GO)

**Manual Decision**: GO (prioritized evidence over user demand)
**Rationale**: Evidence is strong (peer-reviewed research + case studies), user demand likely underestimated (only counted inbox + GitHub, not Discord/email)

**Mitigation**: Track user demand more comprehensively in future pilots (Discord, email, community forum)
EOF

# Log manual decision to A-MEM
cat >> .chora/memory/events/dogfooding.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "pilot_decision_manual",
  "pilot_id": "{pilot-id}",
  "decision": "GO",
  "conflict": "evidence vs user_demand",
  "rationale": "Prioritized strong evidence (65% A+B) over low user demand (4)"
}
EOF
```

---

**Recovery 3: Vision Update Failure → Retry with Error Logging**

**Workflow**:
```bash
# Retry vision update
vision_file=".chora/memory/knowledge/notes/vision-{project}-{horizon}.md"

if [ ! -f "$vision_file" ]; then
  echo "ERROR: Vision file not found: $vision_file"

  # Log error to A-MEM
  cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "vision_update_failed",
  "pilot_id": "{pilot-id}",
  "error": "vision_file_not_found",
  "file": "$vision_file"
}
EOF

  # Manual recovery: Create vision file, then retry
  exit 1
fi

# Retry update
# ... (update vision file)

# Log success
cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "vision_update_success_after_retry",
  "pilot_id": "{pilot-id}"
}
EOF
```

---

**Recovery 4: Backlog Update Failure → Retry with Fallback**

**Workflow**:
```bash
# Check beads CLI installed
if ! command -v bd &> /dev/null; then
  echo "ERROR: Beads CLI not installed"

  # Log error
  cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "backlog_update_failed",
  "pilot_id": "{pilot-id}",
  "error": "bd_not_installed"
}
EOF

  # Fallback: Manual epic creation (document in pilot final summary)
  cat >> .chora/memory/knowledge/notes/pilot-{id}-final.md <<EOF

## Next Steps (Manual - bd not installed)
- [ ] Install beads CLI: npm install -g @beads/bd
- [ ] Create epic: bd create "Epic: {Feature Name} (v{Version})" --type epic --priority 1
- [ ] Link to roadmap milestone: bd update {epic-id} --metadata '{"roadmap_milestone_note": "roadmap-{project}-v{version}"}'
EOF

  exit 1
fi

# Retry epic creation
epic_id=$(bd create "Epic: {Feature Name} (v{Version})" --type epic --priority 1 --metadata '{...}')

# Log success
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "epic_created_from_pilot",
  "pilot_id": "{pilot-id}",
  "epic_id": "$epic_id"
}
EOF
```

---

**Recovery 5: Lessons Learned Not Documented → Post-Mortem Review**

**Workflow**:
```bash
# Check if lessons learned exists
lessons_file=".chora/memory/knowledge/notes/lessons-learned-{pilot-id}.md"

if [ ! -f "$lessons_file" ]; then
  echo "WARNING: Lessons learned not documented for pilot {pilot-id}"

  # Schedule post-mortem review
  # Option 1: Create beads task
  bd create "Post-mortem: Document lessons learned for pilot {pilot-id}" \
    --type task \
    --priority 1 \
    --assignee "{lead}" \
    --description "Pilot NO-GO decision made, but lessons learned not documented. Schedule 30-min post-mortem with team."

  # Option 2: Manual reminder
  echo "ACTION REQUIRED: Schedule post-mortem for pilot {pilot-id} within 1 week"
fi
```

### 5.3: Error Logging to A-MEM

All errors should be logged to `.chora/memory/events/dogfooding-errors.jsonl`:

**Schema**:
```jsonl
{
  "timestamp": "2025-11-05T00:00:00Z",
  "event": "pilot_error",
  "pilot_id": "pilot-{id}",
  "error_type": "timeout | decision_conflict | vision_update_failed | backlog_update_failed | lessons_not_documented",
  "error_details": "{Description}",
  "recovery_strategy": "abort | extend | manual_decision | retry | fallback | post_mortem",
  "resolution_status": "resolved | pending"
}
```

**Example**:
```jsonl
{
  "timestamp": "2025-11-05T00:00:00Z",
  "event": "pilot_error",
  "pilot_id": "pilot-sap-015-2025-q4",
  "error_type": "backlog_update_failed",
  "error_details": "bd command not found, beads CLI not installed",
  "recovery_strategy": "fallback",
  "resolution_status": "pending"
}
```
```

---

### Deliverable 5: Awareness Guide Pre-Pilot Discovery Examples

**File**: `docs/skilled-awareness/dogfooding-patterns/awareness-guide.md`

**Section to Add**: Section 3 (Pre-Pilot Discovery Examples)

**Content** (~6 pages):

```markdown
## 3. Pre-Pilot Discovery Examples

This section provides 3 examples of Week -1 discovery workflows.

### 3.1: Example 1 - Week -1 Discovery Workflow

**Scenario**: Chora-base has 89 unfulfilled intentions scattered across 10 sources. Team wants to select 3-5 pilot candidates for 2025-Q4.

**Step 1: Query Intention Inventory**

```bash
# Find latest intention inventory (SAP-010)
intention_file=$(grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | tail -1)
cat "$intention_file"
```

**Output**: 89 intentions categorized by evidence level (A/B/C), user demand, strategic alignment.

**Step 2: Filter Exploratory Candidates**

```bash
# Filter intentions with evidence A+B 50-70%, user demand 3-10
cat "$intention_file" | jq '.intentions[] | select(.evidence.A + .evidence.B >= 50 and .evidence.A + .evidence.B <= 70 and .user_demand >= 3 and .user_demand <= 10)'
```

**Output**: 23 exploratory intentions (good pilot candidates).

**Step 3: Score by Strategic Alignment**

For each of 23 intentions:
1. Read strategic theme matrix (SAP-010)
2. Score alignment (0-10)
3. Example:
   - **SAP-015 Backlog Organization**: Aligns with "Strategic Planning Infrastructure" theme (Score: 9/10)
   - **SAP-006 Vision Synthesis**: Aligns with "Strategic Planning Infrastructure" theme (Score: 10/10)
   - **SAP-030 Data Fetching**: Aligns with "React Ecosystem" theme (Score: 7/10)

**Step 4: Calculate Pilot Scores**

For each intention:
```
score = (evidence_A_plus_B% × 0.4) + (strategic_alignment × 0.3) + (user_demand × 0.2) + (feasibility × 0.1)
```

Example calculations:
```
SAP-015: (65 × 0.4) + (9 × 0.3) + (7 × 0.2) + (8 × 0.1) = 8.7
SAP-006: (70 × 0.4) + (10 × 0.3) + (8 × 0.2) + (7 × 0.1) = 8.9
SAP-030: (55 × 0.4) + (7 × 0.3) + (5 × 0.2) + (6 × 0.1) = 7.1
```

**Step 5: Select Top 5 Candidates**

Sort by score (descending):
1. SAP-006 Vision Synthesis (Score: 8.9)
2. SAP-015 Backlog Organization (Score: 8.7)
3. SAP-010 Strategic Templates (Score: 8.2)
4. SAP-027 Pre-Pilot Discovery (Score: 7.9)
5. SAP-030 Data Fetching (Score: 7.1)

**Step 6: Document Pilot Candidates**

```bash
cat > .chora/memory/knowledge/notes/pilot-candidates-2025-11-05.md <<'EOF'
---
id: pilot-candidates-2025-11-05
type: pilot-candidates
status: draft
from_intention_inventory: intention-inventory-2025-11-04
from_vision: vision-chora-base-6-month
tags: [dogfooding, pilot-discovery, strategic-planning]
created: 2025-11-05T00:00:00Z
---

# Pilot Candidates: 2025-11-05

**From**: intention-inventory-2025-11-04 (89 intentions)
**Vision Wave 2**: vision-chora-base-6-month

## Top 5 Candidates

### 1. SAP-006 Vision Synthesis (Score: 8.9)
**Intention ID**: intention-067
**Evidence**: A+B 70% (Level A: 30%, Level B: 40%, Level C: 30%)
**User Demand**: 8 requests (inbox + GitHub issues)
**Strategic Alignment**: 10/10 (core strategic theme)
**Pilot Effort**: 3 weeks
**Risk**: Medium (changes to existing SAP-006 workflow)
**Hypothesis**: If we add 4-phase vision synthesis (Discovery → Analysis → Drafting → Cascade), then strategic planning cycles reduce from 2 weeks to 3 days
**Success Criteria**:
- Discovery phase completes in <2 days
- Vision draft completes in <4 hours
- Backlog cascade completes in <30 minutes

### 2. SAP-015 Backlog Organization (Score: 8.7)
**Intention ID**: intention-089
**Evidence**: A+B 65% (Level A: 25%, Level B: 40%, Level C: 35%)
**User Demand**: 7 requests
**Strategic Alignment**: 9/10
**Pilot Effort**: 2 weeks
**Risk**: Low (reversible, no breaking changes)
**Hypothesis**: If we add 5 backlog organization patterns, then teams manage multi-tier backlogs 50% faster
**Success Criteria**:
- Vision cascade completes in <30 minutes
- Backlog health queries detect issues in <5 seconds
- Quarterly refinement reduces P3/P4 backlog by ≥20%

### 3. SAP-010 Strategic Templates (Score: 8.2)
...

### 4. SAP-027 Pre-Pilot Discovery (Score: 7.9)
...

### 5. SAP-030 Data Fetching (Score: 7.1)
...
EOF
```

**Step 7: Select Pilot**

**Decision**: Pilot SAP-015 (Score: 8.7, Effort: 2 weeks, Risk: Low)
**Rationale**: High score, low risk, matches team capacity (2 weeks)

**Next Step**: Proceed to Week 0 (Setup) for SAP-015 pilot.

---

### 3.2: Example 2 - Pilot GO Decision → Vision + Backlog Cascade

**Scenario**: SAP-015 pilot complete, GO decision made. Evidence A+B improved from 65% → 75%, user demand from 7 → 12.

**Step 1: Update Vision Wave 2 → Wave 1 (Promotion)**

```bash
# Read vision document
vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"

# Find SAP-015 in Wave 2
grep -A 10 "SAP-015 Backlog Organization" "$vision_file"

# Update evidence + user demand
# Before: Evidence A+B 65%, user demand 7 (Wave 2 exploratory)
# After: Evidence A+B 75%, user demand 12 (Wave 1 committed)

# Manually edit vision file (or use Edit tool)
# Move SAP-015 from Wave 2 section to Wave 1 section
# Update evidence: A 35%, B 40%, C 25%
# Update user demand: 12 requests
```

**Step 2: Log Vision Update to A-MEM**

```bash
cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "vision_wave_promotion",
  "pilot_id": "pilot-sap-015-2025-q4",
  "decision": "GO",
  "intention": "SAP-015 Backlog Organization Patterns",
  "from_wave": 2,
  "to_wave": 1,
  "evidence_before": {"A": 25, "B": 40, "C": 35},
  "evidence_after": {"A": 35, "B": 40, "C": 25},
  "user_demand_before": 7,
  "user_demand_after": 12
}
EOF
```

**Step 3: Create Beads Epic (P1 - NEXT)**

```bash
epic_id=$(bd create "Epic: SAP-015 Backlog Organization (v1.1.0)" \
  --type epic \
  --priority 1 \
  --description "From pilot-sap-015-2025-q4 GO decision. Add 5 backlog organization patterns: multi-tier priority (P0-P4), vision cascade, backlog refinement, epic decomposition, health queries." \
  --metadata '{
    "from_dogfooding_pilot": "pilot-sap-015-2025-q4",
    "decision": "GO",
    "target_version": "v1.1.0",
    "pilot_evidence": {"A": 35, "B": 40, "C": 25}
  }')

echo "Epic created: $epic_id"
```

**Step 4: Create Roadmap Milestone (SAP-010)**

```bash
cat > .chora/memory/knowledge/notes/roadmap-chora-base-v1.1.0-sap-015.md <<EOF
---
id: roadmap-chora-base-v1.1.0-sap-015
type: roadmap-milestone
version: v1.1.0
sap: SAP-015
from_pilot: pilot-sap-015-2025-q4
beads_epic: $epic_id
target_date: 2025-12-31
tags: [roadmap, milestone, sap-015, backlog-organization]
created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

# Roadmap Milestone: SAP-015 Backlog Organization (v1.1.0)

**From**: pilot-sap-015-2025-q4 GO decision
**Beads Epic**: $epic_id
**Target Date**: 2025-12-31

## Features
1. Multi-tier priority pattern (P0-P4)
2. Vision cascade pattern (Wave 1 → beads)
3. Backlog refinement workflow (quarterly)
4. Epic decomposition template
5. Backlog health queries

## Success Criteria
- Vision cascade completes in <30 minutes
- Backlog health queries detect issues in <5 seconds
- Quarterly refinement reduces P3/P4 backlog by ≥20%
EOF
```

**Step 5: Link Epic to Roadmap Milestone**

```bash
bd update $epic_id --metadata '{
  "roadmap_milestone_note": "roadmap-chora-base-v1.1.0-sap-015"
}'
```

**Step 6: Log Epic Creation to A-MEM**

```bash
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "epic_created_from_pilot",
  "pilot_id": "pilot-sap-015-2025-q4",
  "decision": "GO",
  "epic_id": "$epic_id",
  "target_version": "v1.1.0"
}
EOF
```

**Output**:
- Vision Wave 2 → Wave 1 (SAP-015 promoted)
- Beads epic created (P1 - NEXT)
- Roadmap milestone created
- All updates logged to A-MEM

**Next Step**: Decompose epic into tasks (see SAP-015 Epic Decomposition Template).

---

### 3.3: Example 3 - Pilot NO-GO Decision → Lessons Learned

**Scenario**: SAP-030 Data Fetching pilot complete, NO-GO decision made. Evidence A+B decreased from 55% → 45%, user demand from 5 → 2.

**Step 1: Document Lessons Learned**

```bash
cat > .chora/memory/knowledge/notes/lessons-learned-pilot-sap-030-2025-q4.md <<EOF
---
id: lessons-learned-pilot-sap-030-2025-q4
type: lessons-learned
pilot_id: pilot-sap-030-2025-q4
decision: NO-GO
intention: SAP-030 Data Fetching Patterns
tags: [dogfooding, lessons-learned, sap-030]
created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

# Lessons Learned: SAP-030 Data Fetching Patterns (NO-GO)

## What Failed
- **Low User Demand**: Only 2 teams requested data fetching patterns (expected 5+)
- **High Complexity**: Pilot revealed 3 competing approaches (React Query, SWR, custom hooks), no clear winner
- **Weak Evidence**: Evidence A+B decreased from 55% → 45% after pilot (no strong standards, case studies inconclusive)

## Why It Failed
- **Root Cause 1**: Premature piloting - should have researched standards (React Query RFC, community adoption) before pilot
- **Root Cause 2**: Overestimated user demand - assumed 10+ teams needed this, but only 2 teams in chora ecosystem use data fetching
- **Root Cause 3**: Underestimated complexity - 3 competing approaches require deep research, not 2-week pilot

## What We Learned
- **Lesson 1**: Week -1 discovery should include deeper literature review (check for RFCs, community standards)
- **Lesson 2**: User demand should be validated via surveys, not just assumed (actual demand: 2, assumed: 5)
- **Lesson 3**: Complex pilots (3+ competing approaches) need 4-6 weeks, not 2 weeks

## Future Recommendations
- **Recommendation 1**: Demote SAP-030 to Wave 3 (aspirational), re-pilot in 2026-Q2 after deeper research
- **Recommendation 2**: Add "literature review" step to Week -1 discovery (validate evidence A% before piloting)
- **Recommendation 3**: Add "user demand survey" to Week -1 discovery (validate demand before piloting)
EOF
```

**Step 2: Update Vision Wave 2 → Wave 3 (Demotion)**

```bash
# Read vision document
vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"

# Find SAP-030 in Wave 2
grep -A 10 "SAP-030 Data Fetching" "$vision_file"

# Update evidence + user demand
# Before: Evidence A+B 55%, user demand 5 (Wave 2 exploratory)
# After: Evidence A+B 45%, user demand 2 (Wave 3 aspirational)

# Manually edit vision file (or use Edit tool)
# Move SAP-030 from Wave 2 section to Wave 3 section
# Update evidence: A 15%, B 30%, C 55%
# Update user demand: 2 requests
```

**Step 3: Log Vision Update to A-MEM**

```bash
cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "vision_wave_demotion",
  "pilot_id": "pilot-sap-030-2025-q4",
  "decision": "NO-GO",
  "intention": "SAP-030 Data Fetching Patterns",
  "from_wave": 2,
  "to_wave": 3,
  "evidence_before": {"A": 20, "B": 35, "C": 45},
  "evidence_after": {"A": 15, "B": 30, "C": 55},
  "user_demand_before": 5,
  "user_demand_after": 2
}
EOF
```

**Step 4: Close Existing P3 Task (if exists)**

```bash
# Find P3 task linked to SAP-030
task_id=$(bd list --status open --priority 3 --json | jq -r '.[] | select(.title | contains("SAP-030")) | .id')

# Close task
bd close $task_id --reason "Pilot NO-GO: Low user demand (2), weak evidence (A+B 45%), high complexity (3 competing approaches)"
```

**Step 5: Log Task Closure to A-MEM**

```bash
cat >> .chora/memory/events/backlog-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "task_closed_from_pilot",
  "pilot_id": "pilot-sap-030-2025-q4",
  "decision": "NO-GO",
  "task_id": "$task_id",
  "reason": "Low user demand (2), weak evidence (A+B 45%), high complexity"
}
EOF
```

**Output**:
- Lessons learned documented
- Vision Wave 2 → Wave 3 (SAP-030 demoted)
- P3 task closed
- All updates logged to A-MEM

**Next Step**: Re-pilot SAP-030 in 2026-Q2 after deeper research (literature review, user demand survey).
```

---

### Deliverable 6: Ledger Update (Version 1.1.0)

**File**: `docs/skilled-awareness/dogfooding-patterns/ledger.md`

**Section to Add**: Version 1.1.0 entry at top of version history

**Content**:

```markdown
## Version 1.1.0 (2025-11-05)

**Status**: Active → Pilot
**Focus**: Pre-Pilot Discovery and Feedback Loops

### Enhancements
1. **Week -1 Discovery Phase**: Added systematic process for selecting 3-5 pilot candidates from intention inventory (SAP-010), prioritizing by evidence + strategic alignment + user demand + feasibility
2. **Pilot → Vision Feedback Loop**: GO decisions promote Vision Wave 2 → Wave 1 (committed), NO-GO decisions demote Wave 2 → Wave 3 (aspirational)
3. **Pilot → Backlog Integration**: GO decisions create beads epic (SAP-015, P1), NO-GO decisions log lessons learned (SAP-010)
4. **Protocol Spec Completion**: Completed Sections 3 (Integration Patterns), 4 (Configuration Schema), 5 (Error Handling)
5. **Pre-Pilot Discovery Examples**: Added 3 examples to awareness-guide.md (discovery workflow, GO cascade, NO-GO lessons learned)

### Artifacts Updated
- **Protocol Spec**: Added Section 2.0 (Week -1 Discovery, ~6 pages), completed Sections 3-5 (~14 pages)
- **Awareness Guide**: Added Section 3 (Pre-Pilot Discovery Examples, ~6 pages)
- **Ledger**: Updated to version 1.1.0

### Integration
- **SAP-010 (Memory System)**: Reads intention inventory, strategic theme matrix; logs pilot candidates, pilot results, lessons learned
- **SAP-006 (Development Lifecycle)**: Updates vision Wave 2 decision criteria based on pilot GO/NO-GO
- **SAP-015 (Task Tracking)**: Creates beads epic on GO decision, promotes P3 → P2 or closes task on NO-GO

### Configuration
- **`.chora/config.yaml`**: Added `dogfooding` section with pilot defaults, vision thresholds, backlog integration settings, A-MEM logging, discovery scoring weights

### Dogfooding Plan
- **Project**: chora-base
- **Timeline**: 2025-Q4 (3 months)
- **Activities**:
  1. **Week 1**: Run Week -1 discovery, select 3-5 pilot candidates
  2. **Week 2-5**: Pilot SAP-015 (4 weeks: Setup + Execution + Evaluation)
  3. **Week 5**: Make GO/NO-GO decision, cascade to vision + backlog
  4. **Week 6**: Validate feedback loops (vision updated, epic created, lessons learned logged)
- **Success Criteria**:
  - Week -1 discovery selects 3-5 candidates in <2 hours
  - Pilot GO creates beads epic in <5 minutes
  - Pilot NO-GO logs lessons learned in <5 minutes
  - Vision Wave 2 decision criteria updated after pilot
```

---

## 5. Execution Tasks

### Task 1: Add Section 2.0 to Protocol Spec (Week -1 Discovery)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Steps**:
1. Read existing protocol-spec.md to understand structure
2. Add new Section 2.0 before existing Week 0 (Section 2.1 becomes 2.1, renumber subsequent sections)
3. Write 6 subsections (see Deliverable 1 for full content):
   - 2.0.1: Inputs
   - 2.0.2: Activities (6 steps)
   - 2.0.3: Outputs
   - 2.0.4: Decision (which candidate to pilot)
   - 2.0.5: Integration with Vision Wave 2 (SAP-006)
4. Add code examples, scoring formula, decision tree
5. Save file

**Estimated Effort**: 2 hours

**Dependencies**: None

**Success Criteria**:
- Section 2.0 added with 6 subsections (~6 pages)
- Complete workflow documented (query inventory → prioritize → calculate score → select top 5 → document candidates)
- Integration with SAP-006, SAP-010 documented
- Scoring formula tested

---

### Task 2: Complete Section 3 in Protocol Spec (Integration Patterns)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Steps**:
1. Read existing protocol-spec.md Section 3 (currently TODO)
2. Write 5 subsections (see Deliverable 2 for full content):
   - 3.1: SAP-001 Integration (Inbox)
   - 3.2: SAP-006 Integration (Development Lifecycle)
   - 3.3: SAP-010 Integration (Memory System)
   - 3.4: SAP-015 Integration (Task Tracking)
   - 3.5: Integration Summary (table)
3. Add workflows for GO/NO-GO decisions, vision updates, backlog cascades
4. Save file

**Estimated Effort**: 2 hours

**Dependencies**: None

**Success Criteria**:
- Section 3 completed with 5 subsections (~8 pages)
- Integration patterns documented for 4 SAPs (SAP-001, SAP-006, SAP-010, SAP-015)
- GO/NO-GO workflows complete
- Integration summary table accurate

---

### Task 3: Complete Sections 4-5 in Protocol Spec (Configuration + Error Handling)

**File**: `docs/skilled-awareness/dogfooding-patterns/protocol-spec.md`

**Steps**:
1. Write Section 4 (Configuration Schema) with 3 subsections (see Deliverable 3):
   - 4.1: Schema (YAML)
   - 4.2: Default Configuration
   - 4.3: Environment-Specific Overrides
2. Write Section 5 (Error Handling) with 3 subsections (see Deliverable 4):
   - 5.1: Common Failure Modes (5 failures)
   - 5.2: Recovery Strategies (5 recoveries)
   - 5.3: Error Logging to A-MEM
3. Save file

**Estimated Effort**: 1.5 hours

**Dependencies**: None

**Success Criteria**:
- Section 4 completed with YAML schema, defaults, overrides (~3 pages)
- Section 5 completed with 5 failure modes, 5 recovery strategies, error logging (~3 pages)
- Configuration schema valid YAML
- Error recovery workflows tested

---

### Task 4: Add Section 3 to Awareness Guide (Pre-Pilot Discovery Examples)

**File**: `docs/skilled-awareness/dogfooding-patterns/awareness-guide.md`

**Steps**:
1. Read existing awareness-guide.md to understand structure
2. Add new Section 3: "Pre-Pilot Discovery Examples"
3. Write 3 examples (see Deliverable 5 for full content):
   - 3.1: Week -1 Discovery Workflow
   - 3.2: Pilot GO Decision → Vision + Backlog Cascade
   - 3.3: Pilot NO-GO Decision → Lessons Learned
4. Add bash examples, knowledge note templates, A-MEM logging
5. Save file

**Estimated Effort**: 2 hours

**Dependencies**: None

**Success Criteria**:
- Section 3 added with 3 examples (~6 pages)
- Each example includes scenario, step-by-step workflow, code snippets, outputs
- Integration with SAP-006, SAP-010, SAP-015 demonstrated
- Examples tested (can run in chora-base)

---

### Task 5: Update Ledger with Version 1.1.0

**File**: `docs/skilled-awareness/dogfooding-patterns/ledger.md`

**Steps**:
1. Read existing ledger.md to understand version history format
2. Add new version entry for 1.1.0 at top of version history
3. Write version summary (see Deliverable 6 for full content):
   - Status: Active → Pilot
   - Focus: Pre-Pilot Discovery and Feedback Loops
   - Enhancements (5 items)
   - Artifacts Updated (2 items)
   - Integration (3 SAPs)
   - Configuration (dogfooding section)
   - Dogfooding Plan (chora-base, 2025-Q4, 6 weeks, 4 activities, 4 success criteria)
4. Save file

**Estimated Effort**: 30 minutes

**Dependencies**: Tasks 1-4 (protocol spec, awareness guide) must be complete first

**Success Criteria**:
- Version 1.1.0 entry added to ledger
- Dogfooding plan documented (project, timeline, activities, success criteria)
- Integration with SAP-006, SAP-010, SAP-015 documented

---

## 6. Success Criteria

### Functional Success

1. **Week -1 Discovery Selects Candidates**: Discovery workflow selects 3-5 pilot candidates in <2 hours
   - **Validation**: Execute Week -1 discovery with chora-base intention inventory (89 intentions), measure time to select top 5 candidates
   - **Target**: <2 hours from query inventory to documented candidates

2. **Pilot GO Creates Beads Epic**: GO decision creates beads epic with traceability metadata in <5 minutes
   - **Validation**: Simulate pilot GO decision, measure time to create epic with metadata
   - **Target**: <5 minutes from GO decision to epic created + logged to A-MEM

3. **Pilot NO-GO Logs Lessons Learned**: NO-GO decision logs lessons learned to A-MEM in <5 minutes
   - **Validation**: Simulate pilot NO-GO decision, measure time to create lessons learned note + log to A-MEM
   - **Target**: <5 minutes from NO-GO decision to lessons learned logged

4. **Vision Wave 2 Updated After Pilot**: Vision decision criteria updated based on pilot evidence
   - **Validation**: Simulate pilot GO decision (evidence A+B 65% → 75%), verify vision Wave 2 → Wave 1 promotion
   - **Target**: Vision document updated with new evidence, user demand, logged to A-MEM

### Documentation Success

5. **Protocol Spec Complete**: Sections 2.0, 3, 4, 5 added to protocol-spec.md (~20 pages)
   - **Validation**: Check protocol-spec.md has all 4 sections complete
   - **Target**: Week -1 discovery (Section 2.0), integration patterns (Section 3), configuration (Section 4), error handling (Section 5)

6. **Awareness Guide Examples Complete**: 3 pre-pilot discovery examples added to awareness-guide.md (~6 pages)
   - **Validation**: Check awareness-guide.md has Section 3 with 3 examples
   - **Target**: Discovery workflow, GO cascade, NO-GO lessons learned

### Integration Success

7. **SAP-006 Integration**: Pilot results update vision Wave 2 decision criteria
   - **Validation**: Execute pilot GO decision, check vision document updated (Wave 2 → Wave 1)
   - **Target**: Vision evidence A+B%, user demand updated, logged to `.chora/memory/events/vision-updates.jsonl`

8. **SAP-010 Integration**: Pilot candidates, results, lessons learned logged to A-MEM
   - **Validation**: Execute Week -1 discovery + pilot evaluation, check A-MEM files
   - **Target**: Pilot candidates note created, pilot results logged, lessons learned (if NO-GO) logged

9. **SAP-015 Integration**: Pilot GO creates beads epic, NO-GO closes P3 task
   - **Validation**: Execute pilot GO decision, verify beads epic created with `from_dogfooding_pilot` metadata
   - **Target**: Epic has `from_dogfooding_pilot`, `decision: "GO"`, `target_version`, `pilot_evidence` metadata

---

## 7. Testing & Validation

### Unit Testing (Manual)

**Test 1: Week -1 Discovery Workflow**
```bash
# Query intention inventory
intention_file=$(grep -l '"type": "intention-inventory"' .chora/memory/knowledge/notes/*.md | tail -1)
cat "$intention_file"

# Filter exploratory intentions (evidence A+B 50-70%, user demand 3-10)
# Calculate pilot scores
# Select top 5 candidates
# Document pilot candidates note

# Verify pilot candidates note created
ls .chora/memory/knowledge/notes/pilot-candidates-*.md
```

**Test 2: Pilot GO → Vision + Backlog Cascade**
```bash
# Simulate pilot GO decision
pilot_id="pilot-sap-015-2025-q4-test"

# Update vision Wave 2 → Wave 1
vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"
# ... (update vision file)

# Log vision update
cat >> .chora/memory/events/vision-updates.jsonl <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event": "vision_wave_promotion",
  "pilot_id": "$pilot_id",
  "decision": "GO",
  "from_wave": 2,
  "to_wave": 1
}
EOF

# Create beads epic
epic_id=$(bd create "Epic: Test GO Decision" --type epic --priority 1 --metadata '{
  "from_dogfooding_pilot": "'$pilot_id'",
  "decision": "GO"
}')

# Verify epic created
bd show $epic_id --json | jq '.metadata.from_dogfooding_pilot'
# Should output: "pilot-sap-015-2025-q4-test"
```

**Test 3: Pilot NO-GO → Lessons Learned**
```bash
# Simulate pilot NO-GO decision
pilot_id="pilot-sap-030-2025-q4-test"

# Create lessons learned note
cat > .chora/memory/knowledge/notes/lessons-learned-$pilot_id.md <<EOF
---
id: lessons-learned-$pilot_id
type: lessons-learned
pilot_id: $pilot_id
decision: NO-GO
---

# Lessons Learned: Test NO-GO

## What Failed
- Test failure 1

## Why It Failed
- Test root cause

## What We Learned
- Test lesson
EOF

# Verify lessons learned note created
cat .chora/memory/knowledge/notes/lessons-learned-$pilot_id.md
```

### Integration Testing

**Test 4: SAP-006 Integration (Vision Updates)**
```bash
# Execute Week -1 discovery
# Select pilot candidate from Vision Wave 2
# Run pilot (simulated)
# Make GO decision
# Verify vision updated (Wave 2 → Wave 1)

vision_file=".chora/memory/knowledge/notes/vision-chora-base-6-month.md"
grep -A 5 "Wave 1" "$vision_file" | grep "SAP-015"
# Should show SAP-015 in Wave 1 after GO decision
```

**Test 5: SAP-010 Integration (A-MEM Logging)**
```bash
# Execute Week -1 discovery
# Verify pilot candidates note created
ls .chora/memory/knowledge/notes/pilot-candidates-*.md

# Execute pilot evaluation
# Verify pilot results logged
tail -5 .chora/memory/events/dogfooding.jsonl

# Execute NO-GO decision
# Verify lessons learned note created
ls .chora/memory/knowledge/notes/lessons-learned-*.md
```

**Test 6: SAP-015 Integration (Beads Epic/Task)**
```bash
# Execute pilot GO decision
# Verify beads epic created
bd list --type epic --json | jq '.[] | select(.metadata.from_dogfooding_pilot != null)'

# Execute pilot NO-GO decision
# Verify P3 task closed or demoted
bd list --status closed --json | jq '.[] | select(.metadata.from_dogfooding_pilot != null)'
```

### Dogfooding Validation (6 weeks)

**Project**: chora-base
**Timeline**: 2025-Q4 (Weeks 1-6)
**Activities**:
1. **Week 1**: Run Week -1 discovery, select 3-5 pilot candidates
2. **Week 2-5**: Pilot SAP-015 (4 weeks: Setup + Execution + Evaluation)
3. **Week 5**: Make GO/NO-GO decision, cascade to vision + backlog
4. **Week 6**: Validate feedback loops (vision updated, epic created, lessons learned logged)

**Success Metrics**:
- Week -1 discovery time: <2 hours ✅
- Pilot GO epic creation time: <5 minutes ✅
- Pilot NO-GO lessons learned time: <5 minutes ✅
- Vision Wave 2 decision criteria updated: Yes ✅

---

## 8. Boundaries & Integration Points

### SAP-027 Owns (Boundaries)

1. **Dogfooding Methodology**: SAP-027 defines 4-week pilot process (Week 0-4) + Week -1 discovery
2. **Pilot Evidence Levels**: SAP-027 defines evidence levels (A/B/C) and GO/NO-GO thresholds
3. **Pilot → Vision Feedback Loop**: SAP-027 owns workflow for updating vision after pilot
4. **Pilot → Backlog Integration**: SAP-027 owns workflow for creating beads epic on GO, logging lessons learned on NO-GO
5. **Pilot Candidate Selection**: SAP-027 owns Week -1 discovery scoring formula, prioritization

### SAP-027 Does NOT Own

1. **Intention Inventory**: SAP-010 owns intention inventory (SAP-027 reads it)
2. **Vision Synthesis**: SAP-006 owns vision creation (SAP-027 updates it)
3. **Beads Task Tracking**: SAP-015 owns beads CLI (SAP-027 creates epics via bd commands)
4. **A-MEM Event Logging**: SAP-010 owns event logging (SAP-027 logs to it)

### Integration Points

**← SAP-010 (Memory System)**: Reads intention inventory, strategic theme matrix; logs pilot candidates, results, lessons learned
- **Trigger**: Week -1 discovery (read inventory), pilot evaluation (log results)
- **Input**: Intention inventory, strategic theme matrix
- **Output**: Pilot candidates note, pilot results events, lessons learned note
- **Pattern**: Query inventory → score candidates → log to A-MEM

**→ SAP-006 (Development Lifecycle)**: Updates vision Wave 2 decision criteria after pilot
- **Trigger**: Pilot GO/NO-GO decision
- **Input**: Pilot final summary (evidence A+B%, user demand)
- **Output**: Vision document updated (Wave 2 → Wave 1 promotion or Wave 2 → Wave 3 demotion), logged to `.chora/memory/events/vision-updates.jsonl`
- **Pattern**: Read pilot results → update vision decision criteria → log to A-MEM

**→ SAP-015 (Task Tracking)**: Creates beads epic on GO, closes P3 task on NO-GO
- **Trigger**: Pilot GO/NO-GO decision
- **Input**: Pilot final summary (feature name, target version, effort)
- **Output**: Beads epic (P1) with metadata (`from_dogfooding_pilot`, `decision`, `target_version`) on GO, P3 task closed with reason on NO-GO
- **Pattern**: Read pilot results → create epic or close task → log to A-MEM

**← SAP-001 (Inbox)**: Coordination requests become intentions in inventory
- **Trigger**: Feature request coordination request created
- **Input**: Coordination request (type, title, user demand)
- **Output**: Intention added to inventory (SAP-010), considered in Week -1 discovery
- **Pattern**: Query inbox → add to inventory → score in discovery

### Opt-In Integration

All integration is **opt-in** via configuration (`.chora/config.yaml`):
- Teams can use SAP-027 without SAP-006 (no vision updates, set `dogfooding.vision.auto_update_on_go: false`)
- Teams can use SAP-027 without SAP-015 (no beads epic, set `dogfooding.backlog.auto_create_epic_on_go: false`)
- Teams can use SAP-027 without SAP-010 (no A-MEM logging, set `dogfooding.memory.log_pilot_setup: false`)

**Configuration Fields for Integration**:
```yaml
dogfooding:
  vision:
    auto_update_on_go: true  # SAP-006 integration
  backlog:
    auto_create_epic_on_go: true  # SAP-015 integration
  memory:
    log_pilot_setup: true  # SAP-010 integration
```

---

## 9. Rollout Plan

### Phase 1: Documentation (Week 1)

**Tasks**:
1. Add Section 2.0 to protocol-spec.md (Week -1 Discovery) (2 hours)
2. Complete Section 3 in protocol-spec.md (Integration Patterns) (2 hours)
3. Complete Sections 4-5 in protocol-spec.md (Configuration + Error Handling) (1.5 hours)
4. Add Section 3 to awareness-guide.md (Pre-Pilot Discovery Examples) (2 hours)
5. Update ledger.md to version 1.1.0 (30 min)

**Total Effort**: 8 hours
**Owner**: SAP maintainer
**Deliverables**: 6 artifact updates (protocol-spec: 3 sections, awareness-guide: 1 section, ledger: 1 version entry, config: 1 schema)

### Phase 2: Dogfooding (Weeks 2-7, ~6 weeks)

**Project**: chora-base
**Activities**:
1. **Week 2**: Run Week -1 discovery, select 3-5 pilot candidates
2. **Week 3-6**: Pilot SAP-015 (4 weeks: Setup + Execution + Evaluation)
3. **Week 6**: Make GO/NO-GO decision, cascade to vision + backlog
4. **Week 7**: Validate feedback loops (vision updated, epic created, lessons learned logged)

**Total Effort**: 1-2 hours per week (discovery overhead)
**Owner**: Chora-base maintainers
**Deliverables**: Pilot candidates note, pilot final summary, vision update, beads epic, ledger update with metrics

### Phase 3: Ecosystem Adoption (Weeks 8+)

**Promotion**: After successful dogfooding (success criteria met)
**Status**: Pilot → Production
**Channels**:
- Update sap-catalog.json status to "production"
- Announce in chora ecosystem (docs, Discord, GitHub Discussions)
- Add to SAP-003 (project-bootstrap) default adoption

**Support**:
- Answer questions via GitHub Discussions
- Iterate on patterns based on early adopter feedback

---

## 10. Open Questions

**Q1: Should Week -1 discovery scoring weights be configurable?**
- **Current**: Hardcoded (evidence 0.4, strategic_alignment 0.3, user_demand 0.2, feasibility 0.1)
- **Alternative**: Allow teams to configure weights in `.chora/config.yaml`
- **Decision**: Add configuration support (Deliverable 3, Section 4.1). Default weights remain 0.4/0.3/0.2/0.1.

**Q2: Should vision updates be manual or automatic?**
- **Current**: Automatic (if `dogfooding.vision.auto_update_on_go: true`)
- **Alternative**: Always manual (human review required)
- **Decision**: Keep automatic as default, allow teams to disable via config (`auto_update_on_go: false`).

**Q3: Should beads epic creation be automatic or manual?**
- **Current**: Automatic (if `dogfooding.backlog.auto_create_epic_on_go: true`)
- **Alternative**: Always manual (product owner reviews pilot results first)
- **Decision**: Keep automatic as default, allow teams to disable via config (`auto_create_epic_on_go: false`).

**Q4: Should pilot candidates be limited to Vision Wave 2 only?**
- **Current**: Candidates should come from Vision Wave 2 (exploratory)
- **Alternative**: Allow candidates from anywhere (intention inventory, inbox, GitHub issues)
- **Decision**: Recommend Vision Wave 2 (Protocol Spec Section 2.0.5) but don't enforce. Teams can pilot non-vision ideas if needed.

**Q5: How should pilot timeout extensions be handled?**
- **Current**: Manual decision (abort or extend by 1 week)
- **Alternative**: Automatic extension if pilot >50% complete
- **Decision**: Keep manual (Protocol Spec Section 5.2, Recovery 1). Human judgment required for abort/extend decisions.

---

## 11. References

### Internal (Chora-Base)

- **SAP-027 (Dogfooding Patterns)**: [docs/skilled-awareness/dogfooding-patterns/](../skilled-awareness/dogfooding-patterns/)
  - Capability Charter: Problem statement, solution design
  - Protocol Spec: Pilot methodology (will be enhanced)
  - Awareness Guide: Operating patterns (will be enhanced)
  - Adoption Blueprint: Installation guide
  - Ledger: Adoption tracking (will be updated to v1.1.0)

- **SAP-010 (Memory System)**: [docs/skilled-awareness/memory-system/](../skilled-awareness/memory-system/)
  - Intention inventory template: Input for Week -1 discovery
  - Strategic theme matrix: Strategic alignment scoring
  - A-MEM event logging: Pilot results, vision updates, backlog updates

- **SAP-006 (Development Lifecycle)**: [docs/skilled-awareness/development-lifecycle/](../skilled-awareness/development-lifecycle/)
  - Vision synthesis workflow: Pilot results update Wave 2 decision criteria
  - Vision Wave promotion criteria: Wave 2 → Wave 1 thresholds

- **SAP-015 (Task Tracking)**: [docs/skilled-awareness/task-tracking/](../skilled-awareness/task-tracking/)
  - Beads CLI: Create epic on pilot GO, close task on NO-GO
  - Epic decomposition template: Roadmap milestone → epic → tasks

- **SAP-001 (Inbox)**: [docs/skilled-awareness/inbox/](../skilled-awareness/inbox/)
  - Coordination requests: Feature requests become intentions in inventory

### External

- **Lean Startup (Build-Measure-Learn)**: [http://theleanstartup.com/](http://theleanstartup.com/)
- **Shape Up (Betting Table)**: [https://basecamp.com/shapeup](https://basecamp.com/shapeup)
- **Evidence-Based Management**: [https://www.scrum.org/resources/evidence-based-management](https://www.scrum.org/resources/evidence-based-management)

---

**End of SAP-027 Pre-Pilot Discovery Enhancement Plan**
