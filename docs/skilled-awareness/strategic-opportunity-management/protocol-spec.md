# Strategic Opportunity Management - Protocol Specification

**Pattern ID**: SAP-060
**Pattern Name**: strategic-opportunity-management
**Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-21

## 1. Overview

This specification defines the complete lifecycle protocol for Strategic Opportunity Management, including VERA prioritization framework, waypoint de-risking pattern, A-MEM intention tracking, and integration workflows.

## 2. Opportunity Lifecycle States

### State Machine

```
┌────────────┐
│ discovered │ (informal idea, not yet captured)
└─────┬──────┘
      │ capture (<15 min with template)
      ▼
┌────────────┐
│  captured  │ (OPP-YYYY-NNN file created, VERA scored)
└─────┬──────┘
      │ VERA Priority calculated
      │
      ├─ Priority < 25 → stays in opportunities/ (Low/Medium)
      │
      └─ Priority ≥ 25 → promote to CORD
         ▼
┌────────────┐
│  promoted  │ (CORD-YYYY-NNN created, active work planned)
└─────┬──────┘
      │ waypoint validation (if High Risk or High Effort)
      ▼
┌────────────┐
│ validated  │ (GO decision, ready for full execution)
└─────┬──────┘
      │ decompose to Beads tasks, execute
      ▼
┌────────────┐
│ delivered  │ (work completed, deliverables shipped)
└─────┬──────┘
      │ retrospective (intended vs actual)
      ▼
┌────────────┐
│  learned   │ (outcome validated, patterns extracted)
└────────────┘
```

### State Definitions

| State | Criteria | Artifacts | A-MEM Event |
|-------|----------|-----------|-------------|
| **discovered** | Idea identified but not documented | None | None |
| **captured** | OPP file created, VERA scored | `OPP-YYYY-NNN.md` | `opportunity_identified` |
| **promoted** | Priority ≥ 25, CORD created | `OPP-YYYY-NNN.md` + `CORD-YYYY-NNN.json` | `opportunity_promoted` |
| **validated** | Waypoint complete (if applicable), GO decision | Waypoint deliverable (research doc, prototype, etc.) | Part of `opportunity_promoted` |
| **delivered** | Work completed, deliverables shipped | Final artifacts (code, docs, etc.) | `opportunity_delivered` |
| **learned** | Retrospective complete, patterns extracted | Knowledge note | `outcome_validated` |

## 3. VERA Prioritization Framework

### Formula

```
Priority = (Value × 2.0) + (Effort × 1.5) + (Risk × 1.0) + (Alignment × 2.5)

Where:
- Value (V): 1-5 scale
- Effort (E): 1-5 scale (INVERTED: 1=High effort, 5=Low effort)
- Risk (R): 1-5 scale (INVERTED: 1=High risk, 5=Low risk)
- Alignment (A): 1-5 scale
```

**Score Range**: 7.0 (worst) to 35.0 (best)

### Dimension Scoring (1-5 Scale)

#### Value (V) - "What business/technical benefits will this deliver?"

| Score | Criteria | Example |
|-------|----------|---------|
| **5** | Transformational (100+ hours saved/year, 80%+ adoption increase, 200%+ ROI) | Automated SAP distribution: 85-90% time savings, +50-65pp adoption |
| **4** | High value (50-100 hours saved/year, 50-80% adoption increase, 100-200% ROI) | Feature manifest traceability: 60-73% discovery time savings |
| **3** | Moderate value (20-50 hours saved/year, 20-50% adoption increase, 50-100% ROI) | Improved documentation search: 30-40% time savings |
| **2** | Low value (5-20 hours saved/year, 5-20% adoption increase, 20-50% ROI) | Minor workflow optimization: 10-15% time savings |
| **1** | Minimal value (<5 hours saved/year, <5% adoption increase, <20% ROI) | Cosmetic improvements, nice-to-haves |

**Quantification Required**: Value must be expressed in time savings, adoption metrics, or ROI calculations.

#### Effort (E) - "How much time will this require?" (INVERTED)

| Score | Criteria | Example |
|-------|----------|---------|
| **5** | Very low effort (≤4 hours) | Quick script, documentation update |
| **4** | Low effort (4-15 hours) | Small feature, simple integration |
| **3** | Moderate effort (15-40 hours) | Multi-file refactor, new SAP adoption |
| **2** | High effort (40-80 hours) | New capability server, major architectural change |
| **1** | Very high effort (>80 hours) | Ecosystem-wide migration, new platform |

**Note**: Effort is INVERTED so lower effort gets higher score (aligns with "easier is better" intuition).

#### Risk (R) - "What could go wrong?" (INVERTED)

| Score | Criteria | Example |
|-------|----------|---------|
| **5** | Very low risk (proven approach, no dependencies, easy rollback) | Copy existing pattern, documentation work |
| **4** | Low risk (familiar tools, isolated changes, clear rollback) | Known library integration, configuration change |
| **3** | Moderate risk (some unknowns, moderate dependencies, rollback possible) | New tool evaluation (Copier vs Cookiecutter) |
| **2** | High risk (significant unknowns, complex dependencies, difficult rollback) | Breaking API change, major refactor |
| **1** | Very high risk (unproven approach, critical dependencies, no rollback) | Custom protocol design, distributed system coordination |

**Note**: Risk is INVERTED so lower risk gets higher score (aligns with "safer is better" intuition).

#### Alignment (A) - "How well does this fit our strategy?"

| Score | Criteria | Example |
|-------|----------|---------|
| **5** | Critical strategic alignment (blocks current sprint goals, enables quarterly OKRs, core mission) | SAP Lifecycle Meta-SAPs, core infrastructure |
| **4** | High alignment (accelerates current work, supports quarterly goals, high priority) | Distribution automation, testing framework |
| **3** | Moderate alignment (nice to have now, fits long-term vision, medium priority) | Developer experience improvements |
| **2** | Low alignment (tangential to current focus, future priority, low urgency) | Experimental features, speculative work |
| **1** | Misaligned (contradicts strategy, no clear fit, should defer) | Out-of-scope work, distractions |

### Weight Rationale

**Alignment (2.5x)**: Strategic fit is most important - work must advance organizational goals
**Value (2.0x)**: Must deliver meaningful benefits - quantified impact matters
**Effort (1.5x)**: Easier is better, but not decisive - don't avoid valuable hard work
**Risk (1.0x)**: Manageable risks shouldn't block high-value aligned work

### Priority Bands

| Priority Range | Band | Recommendation | Example Action |
|----------------|------|----------------|----------------|
| **30-35** | Critical | Start immediately, block other work if needed | Drop everything, start now |
| **25-29** | High | Plan for current sprint, start within 1-2 weeks | Add to sprint, prioritize highly |
| **20-24** | Medium | Plan for next sprint, start within 2-4 weeks | Backlog, schedule next sprint |
| **15-19** | Low | Backlog, revisit quarterly | Defer to quarterly planning |
| **<15** | Defer | Archive unless context changes significantly | Archive, don't prioritize |

### VERA Scoring Example (OPP-2025-022)

```yaml
vera_scores:
  value: 5        # 85-90% time savings, +50-65pp adoption, 236% ROI
  effort: 2       # 38-60 hours total execution (High effort)
  risk: 3         # Moderate - Copier vs Cookiecutter vs cruft vs manual
  alignment: 5    # Critical - Blocks SAP Lifecycle Meta-SAPs, core distribution

# Calculation:
# Priority = (5 × 2.0) + (2 × 1.5) + (3 × 1.0) + (5 × 2.5)
#          = 10.0 + 3.0 + 3.0 + 12.5
#          = 28.5

priority_band: high        # 25-29 range
recommendation: "Plan for current sprint (start within 1-2 weeks)"

# Actual outcome: Started within 1 day (28.5 accurately predicted urgency) ✅
```

## 4. Waypoint De-Risking Pattern

### When to Use Waypoint

**Trigger criteria** (ANY of these):
- High Risk (R ≤ 2): Technical approach uncertain
- High Effort (E ≤ 2): >40 hours work, need to validate first
- New domain: Unfamiliar tools/patterns
- Multiple approaches: Need to compare options before committing
- Stakeholder uncertainty: Need evidence before approval

### Waypoint Structure

```yaml
waypoint:
  goal: "What question/uncertainty are we resolving?"
  deliverable: "What concrete artifact will answer it?"
  success_criteria: "What evidence validates the approach?"
  estimated_time: "3-4 hours"  # If >4 hours, break into smaller waypoint
  go_no_go_decision:
    go_criteria: "Conditions for proceeding to full execution"
    no_go_criteria: "Conditions for pivoting or abandoning"
    pivot_options: ["Alternative approaches if NO-GO"]
```

### Waypoint Deliverables (Examples)

- **Research document**: Tool comparison with scoring rubric (OPP-2025-022 example)
- **Proof of concept**: Minimal prototype demonstrating feasibility
- **Decision record**: Architecture decision with tradeoff analysis
- **Spike report**: Technical investigation results with recommendations
- **Risk assessment**: Threat model with mitigation strategies
- **User research**: Interviews, surveys, usability tests

### Waypoint Workflow

```
1. Define waypoint (3-5 min during opportunity capture)
   ↓
2. Allocate 3-4 hours for validation work
   ↓
3. Execute waypoint (research, prototype, spike, etc.)
   ↓
4. Analyze results against success criteria
   ↓
5. Make GO/NO-GO decision
   ↓
6. If GO: Proceed to full execution (38-60 hours)
   If NO-GO: Pivot to alternative or archive opportunity
```

### Waypoint ROI Calculation

**Investment**: 3-4 hours validation
**Prevented waste**: 38-60 hours if wrong approach
**ROI**: 10-15x return on validation investment

**Example** (OPP-2025-022):
- Waypoint: 3-4 hours research (Copier vs Cookiecutter comparison)
- Decision: GO - Copier selected (78% fit vs Cookiecutter 43%)
- Prevented: 38-60 hours building Cookiecutter template that can't update
- ROI: 10-15x (4 hours prevents 40-60 hours waste)

## 5. A-MEM Intention Tracking

### Event Schema (4 Lifecycle Events)

#### Event 1: opportunity_identified

**When**: Opportunity captured, VERA scored
**Purpose**: Log intended impact for later validation

```json
{
  "timestamp": "2025-11-21T00:00:00Z",
  "event_type": "opportunity_identified",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "title": "Copier-based SAP Distribution System",
  "vera_scores": {
    "value": 5,
    "effort": 2,
    "risk": 3,
    "alignment": 5,
    "priority": 28.5
  },
  "intended_impact": {
    "time_savings": "85-90% reduction (17-115 min saved per project)",
    "adoption_increase": "+50-65pp (30-50% → 80-95%)",
    "update_propagation": "60-80% adopt updates (vs 0-10% manual)",
    "annual_savings": "$7,000/year (50 projects/year)",
    "roi_5year": "+236% ($23,200 net benefit)"
  },
  "waypoint": {
    "status": "complete",
    "decision": "GO - Copier selected (78% fit vs Cookiecutter 43%)"
  }
}
```

#### Event 2: opportunity_promoted

**When**: Priority ≥ 25, CORD created
**Purpose**: Track promotion to active work

```json
{
  "timestamp": "2025-11-23T00:00:00Z",
  "event_type": "opportunity_promoted",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "promoted_to": "CORD-2025-023",
  "promotion_reason": "Priority 28.5 (High band) + Strategic alignment (SAP Lifecycle Meta-SAPs)",
  "estimated_effort": "38-60 hours (4 phases)",
  "target_completion": "2025-12-20"
}
```

#### Event 3: opportunity_delivered

**When**: Work completed, deliverables shipped
**Purpose**: Mark completion, enable retrospective

```json
{
  "timestamp": "2025-12-20T00:00:00Z",
  "event_type": "opportunity_delivered",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "completion_date": "2025-12-20",
  "actual_effort_hours": 52,
  "effort_variance": "+8.7% (52 vs 48 estimated)",
  "deliverables": [
    "copier.yml configuration",
    "template/ directory with 6 SAPs",
    "Documentation and integration tests"
  ]
}
```

#### Event 4: outcome_validated

**When**: 6-8 weeks post-delivery, actual impact measured
**Purpose**: Closed-loop learning, VERA accuracy improvement

```json
{
  "timestamp": "2026-02-15T00:00:00Z",
  "event_type": "outcome_validated",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "intended_impact": {
    "time_savings": "85-90%",
    "adoption_increase": "+50-65pp",
    "roi_5year": "+236%"
  },
  "actual_impact": {
    "time_savings": "88%",
    "adoption_increase": "+58pp",
    "roi_5year": "+241%"
  },
  "alignment": "achieved",  # achieved/partial/missed/opposite
  "variance_analysis": "Within ±5% of estimate - VERA Value score (5) accurate",
  "lessons_learned": [
    "Waypoint validation prevented 40-60 hours waste",
    "VERA Priority 28.5 accurately predicted urgency (started within 1 day)",
    "Copier selection (78% fit) was correct decision"
  ]
}
```

### Alignment Ratings

| Rating | Criteria | Example |
|--------|----------|---------|
| **achieved** | Actual impact ≥ 90% of intended (excellent prediction) | 88% time savings vs 85-90% intended |
| **partial** | Actual impact 60-89% of intended (acceptable but overestimated) | 65% time savings vs 85-90% intended |
| **missed** | Actual impact 30-59% of intended (significant gap, learn why) | 40% time savings vs 85-90% intended |
| **opposite** | Actual impact <30% or negative (fundamental misjudgment) | No time savings or negative impact |

### Variance Analysis (Continuous Improvement)

**After 5+ opportunities with outcome_validated events**:

1. **VERA Accuracy Analysis**:
   - Compare intended vs actual impact across all opportunities
   - Identify systematic overestimation/underestimation patterns
   - Adjust VERA scoring rubrics if needed

2. **Waypoint ROI Validation**:
   - Measure prevented waste (wrong approaches avoided)
   - Calculate actual ROI (validation time vs waste prevented)
   - Refine waypoint trigger criteria

3. **Priority Band Calibration**:
   - Analyze "time to start" vs priority band
   - Validate band recommendations (Critical: immediate, High: 1-2 weeks, etc.)
   - Adjust bands if actual urgency mismatches

## 6. Integration Workflows

### SAP-001 (Inbox) Integration

**Directory Structure**:
```
inbox/
├── opportunities/                      # Strategic opportunities (OPP-YYYY-NNN)
│   ├── OPP-2025-001-*.md
│   ├── OPP-2025-022-*.md
│   └── STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md  # Template
├── incoming/
│   └── coordination/                   # Promoted opportunities (CORD-YYYY-NNN)
│       ├── CORD-2025-023-*.json        # Promoted from OPP-2025-022
│       └── ...
```

**Promotion Workflow** (Priority ≥ 25):
1. Opportunity captured in `inbox/opportunities/OPP-YYYY-NNN.md`
2. VERA scoring calculates Priority ≥ 25
3. Create `inbox/incoming/coordination/CORD-YYYY-NNN.json`
4. Link CORD back to OPP: `"origin_opportunity": "OPP-YYYY-NNN"`
5. Log `opportunity_promoted` A-MEM event
6. Triage CORD during sprint planning

### SAP-015 (Beads) Integration

**Task Linking**:
```bash
# When creating Beads tasks for a promoted opportunity:
bd create "SAP-060: Create charter artifact" --metadata "opportunity_id:OPP-2025-022"
bd create "SAP-060: Create protocol spec" --metadata "opportunity_id:OPP-2025-022"
bd create "SAP-060: Create awareness guide" --metadata "opportunity_id:OPP-2025-022"

# Query tasks by opportunity:
bd list --filter "metadata.opportunity_id:OPP-2025-022"
```

**Traceability**:
- Beads tasks include `opportunity_id` in metadata
- All tasks use opportunity's `trace_id` for correlation
- Completion of all Beads tasks → triggers `opportunity_delivered` event

### SAP-019 (Evaluation) Integration

**VERA Scoring Input**:
- **Value**: ROI analysis from SAP-019 evaluation
- **Alignment**: Strategic roadmap from SAP-019 informs priorities
- **Risk**: Adoption patterns and historical data from SAP-019

**Example**:
```bash
# Use SAP-019 strategic analysis to inform VERA scoring
just sap-roadmap  # Generates strategic roadmap
# Extract Alignment scores from roadmap priorities

just sap-deep SAP-009  # Deep dive on specific SAP
# Extract Value and Risk scores from adoption metrics
```

### SAP-056 (Traceability) Integration

**Bidirectional Links**:

**Feature Manifest** (`feature-manifest.yaml`):
```yaml
features:
  - id: FEAT-002
    name: "Unified Discovery System"
    origin:
      opportunity: "OPP-2025-001"  # ← Links feature to opportunity
      created: "2025-11-15"
    requirements:
      - id: REQ-FEAT-002-001
        origin_opportunity: "OPP-2025-001"
```

**Opportunity File** (OPP-2025-022.md):
```markdown
## Related Features
- [[FEAT-003]]: SAP Distribution Automation (origin of this feature)

## Knowledge Extracted
- [[2025-11-19-sap-distribution-copier-vs-cookiecutter]]
- [[2025-11-21-strategic-opportunity-management-pattern]]
```

**Knowledge Note**:
```markdown
---
related:
  - OPP-2025-022  # Opportunity that created this knowledge
  - FEAT-003      # Feature that emerged from this knowledge
---
```

## 7. Anti-Patterns

### Anti-Pattern 1: Skipping Waypoint on High-Risk Work

**Symptom**: Starting 40+ hour effort without 3-4 hour validation
**Risk**: Wasting 10-15x time if approach is wrong
**Remedy**: If R ≤ 2 OR E ≤ 2, define waypoint first

**Example**:
❌ **Bad**: "Copier looks good, let's build the whole template (60 hours)"
✅ **Good**: "Let's research Copier vs Cookiecutter (4 hours) → then decide"

### Anti-Pattern 2: Over-Detailed Capture (>15 Minutes)

**Symptom**: Spending 30-60 minutes documenting opportunity before starting
**Risk**: Capture becomes barrier to action (analysis paralysis)
**Remedy**: Template provides just enough structure—aim for 10-15 min capture

**Example**:
❌ **Bad**: Spend 45 min writing comprehensive charter before starting
✅ **Good**: Use L1 template, capture in 12 min, refine during execution

### Anti-Pattern 3: VERA Scoring Without Quantification

**Symptom**: Value score = 5 without dollar/hour savings calculation
**Risk**: Inflated priority, poor resource allocation
**Remedy**: Value requires quantified benefits (time savings, adoption increase, ROI)

**Example**:
❌ **Bad**: "Value = 5 because this is really important"
✅ **Good**: "Value = 5: 85-90% time savings, +50-65pp adoption, 236% ROI"

### Anti-Pattern 4: No Intention Tracking

**Symptom**: Delivering work without logging expected impact
**Risk**: Can't validate VERA accuracy, no closed-loop learning
**Remedy**: Log `opportunity_identified` event with intended_impact before execution

**Example**:
❌ **Bad**: Build feature, ship, move on (no intended impact logged)
✅ **Good**: Log intended impact → deliver → measure actual → validate alignment

### Anti-Pattern 5: Ignoring Priority Bands

**Symptom**: Priority 18 (Low) but starting immediately
**Risk**: Resource misallocation, strategic work gets starved
**Remedy**: Respect priority bands - defer Low priority until Medium/High/Critical completed

**Example**:
❌ **Bad**: "Priority 18 but I have time, so I'll start now"
✅ **Good**: "Priority 18 → backlog, revisit quarterly. Focus on Priority 28.5 work"

## 8. L1 → L2 Evolution Triggers

**When to adopt L2 (Portfolio Management)**:

Trigger **ANY 2** of these 5 criteria:

1. **Automation value**: >20 opportunities captured (manual tracking painful)
2. **Portfolio scale**: Managing dependencies becomes complex (>30% have dependencies)
3. **VERA accuracy gap**: <70% accuracy (need historical data to improve)
4. **Reporting burden**: Stakeholders request portfolio dashboards
5. **Template fragmentation**: 3+ custom templates emerge (specialization by type)

**L2 Capabilities** (Future):
- Portfolio dashboard (`just opportunity-dashboard`)
- Automated VERA calculation with historical data
- Dependency graph visualization
- Beads API integration (auto-create tasks from CORD)
- Custom VERA weights per context (technical vs strategic vs research)

## 9. Validation Checklist

### L1 Adoption Validation

- [ ] L1 template exists and is usable (`STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md`)
- [ ] At least 1 opportunity captured in <15 min
- [ ] VERA scoring produces priority band
- [ ] Priority band matches actual resourcing decision (80%+ accuracy target)
- [ ] Waypoint defined for High Risk (R ≤ 2) or High Effort (E ≤ 2) opportunity
- [ ] Waypoint prevents wrong-direction work (at least 1 example)
- [ ] `opportunity_identified` A-MEM event logged
- [ ] Integration with SAP-001 (opportunity routing) works
- [ ] Integration with SAP-015 (Beads linking) works

### L2 Adoption Validation

- [ ] Portfolio dashboard shows all opportunities
- [ ] Automated VERA calculation using historical data
- [ ] Dependency graph visualization
- [ ] Custom VERA weights per opportunity type
- [ ] VERA accuracy >70% with calibration

---

**Created**: 2025-11-21
**Protocol Version**: 1.0.0
**Next Review**: After 5+ opportunities delivered (validate VERA accuracy)
**Trace ID**: sap-060-protocol-spec-2025-11-21
