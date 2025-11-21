# Strategic Opportunity Management - Awareness Guide (AGENTS.md)

**Pattern ID**: SAP-060
**Quick Reference**: Systematic opportunity lifecycle from discovery → prioritization → scoping → delivery → learning
**Version**: 1.0.0
**Status**: Pilot

---

## Quick Start (30 seconds)

**When you discover a strategic opportunity**:
1. Copy `inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md` template
2. Fill in 15-minute capture: problem, solution, VERA scores
3. Calculate priority: `(V × 2.0) + (E × 1.5) + (R × 1.0) + (A × 2.5)`
4. If Priority ≥ 25: promote to CORD
5. If High Risk (R ≤ 2) or High Effort (E ≤ 2): define waypoint first

**Priority bands**:
- 30-35 (Critical): Start immediately
- 25-29 (High): Start within 1-2 weeks
- 20-24 (Medium): Next sprint (2-4 weeks)
- 15-19 (Low): Backlog (quarterly review)
- <15 (Defer): Archive

---

## Core Concepts

### VERA Prioritization Framework

**Formula**: `Priority = (Value × 2.0) + (Effort × 1.5) + (Risk × 1.0) + (Alignment × 2.5)`

**Scoring dimensions** (1-5 scale):

| Dimension | Weight | What to Assess | Key Question |
|-----------|--------|----------------|--------------|
| **Value (V)** | 2.0 | Quantified benefits | "How much time/money/adoption will this save/gain?" |
| **Effort (E)** | 1.5 | Total hours required (INVERTED) | "How much work is this?" (1=80+ hrs, 5=<4 hrs) |
| **Risk (R)** | 1.0 | Technical/adoption risks (INVERTED) | "What could go wrong?" (1=very risky, 5=safe) |
| **Alignment (A)** | 2.5 | Strategic fit | "How critical is this to current/quarterly/long-term goals?" |

**INVERTED scores**: Effort and Risk use inverted scales (lower effort/risk = higher score) so the formula aligns with intuition (higher priority = more urgent).

### Waypoint De-Risking Pattern

**When to use**: High Risk (R ≤ 2) OR High Effort (E ≤ 2) OR new domain OR multiple approaches

**Waypoint structure**:
- **Goal**: What question/uncertainty are we resolving?
- **Deliverable**: What artifact answers it? (research doc, prototype, spike, etc.)
- **Success criteria**: What evidence validates the approach? (>70% confidence, ROI quantified, decision made)
- **Estimated time**: 3-4 hours (if >4 hours, break into smaller waypoint)
- **GO/NO-GO decision**: Clear criteria for proceeding vs pivoting

**ROI**: 10-15x return (4 hours validation prevents 40-60 hours waste)

### A-MEM Intention Tracking

**4 lifecycle events** (log to `.chora/memory/events/YYYY-MM.jsonl`):

1. **opportunity_identified**: Opportunity captured, VERA scored, intended impact logged
2. **opportunity_promoted**: Priority ≥ 25, CORD created, active work planned
3. **opportunity_delivered**: Work completed, deliverables shipped, actual effort logged
4. **outcome_validated**: Retrospective complete, intended vs actual impact compared

**Alignment ratings** (outcome_validated):
- **achieved**: Actual ≥ 90% of intended (excellent prediction)
- **partial**: Actual 60-89% of intended (overestimated)
- **missed**: Actual 30-59% of intended (significant gap)
- **opposite**: Actual <30% or negative (fundamental misjudgment)

---

## Workflows

### Workflow 1: Capture Opportunity (<15 min)

```bash
# 1. Copy template
cp inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md \
   inbox/opportunities/OPP-2025-NNN-short-name.md

# 2. Fill in sections (10-15 min):
#    - Problem statement (2 min)
#    - Solution overview (2 min)
#    - VERA scoring (5 min) ← Quantify Value!
#    - Waypoint definition (3 min, if needed)
#    - Intended impact (3 min)

# 3. Calculate priority:
# Priority = (V × 2.0) + (E × 1.5) + (R × 1.0) + (A × 2.5)

# 4. Update status field:
#    - Priority < 25: status = captured
#    - Priority ≥ 25: status = ready_to_promote
```

**Target**: 10-15 minutes from discovery to captured opportunity

### Workflow 2: VERA Scoring (5 min)

**Step 1: Value (2 min)** - Quantify benefits
```
V=5: Transformational (100+ hrs/yr saved, 80%+ adoption, 200%+ ROI)
V=4: High (50-100 hrs/yr, 50-80% adoption, 100-200% ROI)
V=3: Moderate (20-50 hrs/yr, 20-50% adoption, 50-100% ROI)
V=2: Low (5-20 hrs/yr, 5-20% adoption, 20-50% ROI)
V=1: Minimal (<5 hrs/yr, <5% adoption, <20% ROI)

Example: "85-90% time savings (17-115 min/project), +50-65pp adoption, 236% ROI" → V=5
```

**Step 2: Effort (1 min)** - Estimate hours (INVERTED)
```
E=5: Very low (≤4 hrs)
E=4: Low (4-15 hrs)
E=3: Moderate (15-40 hrs)
E=2: High (40-80 hrs)
E=1: Very high (>80 hrs)

Example: "38-60 hours total" → E=2
```

**Step 3: Risk (1 min)** - Assess unknowns (INVERTED)
```
R=5: Very low (proven approach, no dependencies)
R=4: Low (familiar tools, isolated changes)
R=3: Moderate (some unknowns, moderate dependencies)
R=2: High (significant unknowns, complex dependencies)
R=1: Very high (unproven approach, critical dependencies)

Example: "Copier vs Cookiecutter uncertain" → R=3
```

**Step 4: Alignment (1 min)** - Strategic fit
```
A=5: Critical (blocks sprint goals, enables OKRs, core mission)
A=4: High (accelerates current work, supports quarterly goals)
A=3: Moderate (nice to have, fits long-term vision)
A=2: Low (tangential to focus, future priority)
A=1: Misaligned (contradicts strategy, defer)

Example: "Blocks SAP Lifecycle Meta-SAPs, core distribution" → A=5
```

**Step 5: Calculate (10 sec)**
```
Priority = (V × 2.0) + (E × 1.5) + (R × 1.0) + (A × 2.5)
Example: (5 × 2.0) + (2 × 1.5) + (3 × 1.0) + (5 × 2.5) = 28.5

Priority band: 28.5 → High (25-29)
Recommendation: "Plan for current sprint (start within 1-2 weeks)"
```

### Workflow 3: Waypoint Validation (3-4 hours)

**When**: High Risk (R ≤ 2) OR High Effort (E ≤ 2)

**Process**:
```
1. Define waypoint goal (5 min)
   Example: "Validate Copier is correct tool (vs Cookiecutter, cruft, manual)"

2. Define deliverable (5 min)
   Example: "Research findings with tool comparison, ROI analysis"

3. Define success criteria (5 min)
   Example: "Tool selected with >70% confidence"

4. Allocate 3-4 hours for validation work

5. Execute waypoint (3-4 hours)
   - Research tools (Copier, Cookiecutter, cruft)
   - Compare features, fit, complexity
   - Analyze ROI (time savings, adoption, update propagation)
   - Document findings

6. Make GO/NO-GO decision (10 min)
   GO: Proceed to full execution (38-60 hours)
   NO-GO: Pivot to alternative or archive opportunity

7. Update opportunity file:
   waypoint:
     status: complete
     decision: "GO - Copier selected (78% fit vs Cookiecutter 43%)"
```

**Example** (OPP-2025-022):
- Goal: Validate Copier vs Cookiecutter
- Deliverable: [sap-distribution-mechanisms-research.md](../../../.chora/memory/knowledge/notes/2025-11-19-sap-distribution-mechanisms-research.md)
- Success: Copier 78% fit vs Cookiecutter 43% fit → GO
- Time: 3-4 hours
- Prevented: 38-60 hours wasted on Cookiecutter template that can't update

### Workflow 4: Promote to CORD (Priority ≥ 25)

**Trigger**: VERA Priority ≥ 25 (High or Critical band)

**Process**:
```bash
# 1. Create CORD file
cp inbox/templates/coordination-request-template.json \
   inbox/incoming/coordination/CORD-2025-NNN-short-name.json

# 2. Link to opportunity
# In CORD-2025-NNN.json:
{
  "origin_opportunity": "OPP-2025-022",
  "vera_priority": 28.5,
  "estimated_effort": "38-60 hours",
  ...
}

# 3. Update opportunity status
# In OPP-2025-NNN.md:
status: promoted
promoted_to: CORD-2025-023
promotion_date: 2025-11-23

# 4. Log A-MEM event
# Append to .chora/memory/events/YYYY-MM.jsonl:
{
  "timestamp": "2025-11-23T00:00:00Z",
  "event_type": "opportunity_promoted",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "promoted_to": "CORD-2025-023",
  "promotion_reason": "Priority 28.5 (High) + Strategic alignment"
}
```

### Workflow 5: Deliver Opportunity

**Process**:
```bash
# 1. Decompose CORD to Beads tasks
bd create "Phase 1: Template Creation" --metadata "opportunity_id:OPP-2025-022"
bd create "Phase 2: Testing" --metadata "opportunity_id:OPP-2025-022"
bd create "Phase 3: Pilot" --metadata "opportunity_id:OPP-2025-022"
bd create "Phase 4: Distribution" --metadata "opportunity_id:OPP-2025-022"

# 2. Execute work (use Beads workflow)

# 3. Complete all tasks
bd close chora-workspace-abc
bd close chora-workspace-def
# ... (close all tasks)

# 4. Log opportunity_delivered event
# Append to .chora/memory/events/YYYY-MM.jsonl:
{
  "timestamp": "2025-12-20T00:00:00Z",
  "event_type": "opportunity_delivered",
  "trace_id": "sap-distribution-copier-2025-11-19",
  "opportunity_id": "OPP-2025-022",
  "completion_date": "2025-12-20",
  "actual_effort_hours": 52,
  "effort_variance": "+8.7% (52 vs 48 estimated)",
  "deliverables": ["copier.yml", "template/", "docs"]
}

# 5. Update opportunity file
status: delivered
completion_date: 2025-12-20
actual_effort: 52 hours
```

### Workflow 6: Retrospective & Learning (6-8 weeks post-delivery)

**Process**:
```
1. Measure actual impact (6-8 weeks after delivery)
   - Time savings: Measure actual vs intended
   - Adoption: Survey users, check metrics
   - ROI: Calculate actual vs intended

2. Compare intended vs actual
   Intended: 85-90% time savings, +50-65pp adoption, 236% ROI
   Actual: 88% time savings, +58pp adoption, 241% ROI
   Alignment: achieved (within ±10%)

3. Log outcome_validated event
   (See Event 4 schema in protocol-spec.md)

4. Extract patterns to knowledge note
   - What worked well (waypoint, VERA accuracy)
   - What could improve (effort estimation)
   - Lessons learned
   - Anti-patterns to avoid

5. Update VERA scoring rubrics if needed
   - If systematic overestimation: adjust Value rubric
   - If systematic underestimation: adjust Effort rubric
   - Improve scoring accuracy over time
```

---

## Integration Points

### SAP-001 (Inbox)

**Directory structure**:
- `inbox/opportunities/` - Strategic opportunities (OPP-YYYY-NNN)
- `inbox/incoming/coordination/` - Promoted opportunities (CORD-YYYY-NNN)

**Promotion workflow**: Priority ≥ 25 → Create CORD with `origin_opportunity` link

### SAP-015 (Beads)

**Task linking**:
```bash
# Link Beads tasks to opportunity
bd create "Task name" --metadata "opportunity_id:OPP-2025-022"

# Query tasks by opportunity
bd list --filter "metadata.opportunity_id:OPP-2025-022"
```

### SAP-019 (Evaluation)

**VERA scoring input**:
- Value: ROI analysis from SAP-019 deep dive
- Alignment: Strategic roadmap priorities from SAP-019
- Risk: Historical adoption patterns from SAP-019

### SAP-056 (Traceability)

**Bidirectional links**:
- Feature manifest: `origin.opportunity: "OPP-2025-022"`
- Opportunity file: `[[FEAT-003]]` wikilinks
- Knowledge notes: `related: [OPP-2025-022]` in frontmatter

---

## Common Scenarios

### Scenario 1: Quick Opportunity (Priority 20-24, Medium)

```
1. Capture in 10 min with template
2. VERA score: Priority 22 (Medium)
3. No waypoint needed (Low risk, Low effort)
4. Stays in inbox/opportunities/ (not promoted)
5. Schedule for next sprint (2-4 weeks)
6. Log opportunity_identified event
```

### Scenario 2: Strategic Opportunity (Priority 28, High)

```
1. Capture in 15 min with template
2. VERA score: Priority 28.5 (High)
3. Define waypoint (High Risk R=3, High Effort E=2)
4. Execute 4-hour waypoint validation
5. GO decision → Promote to CORD
6. Log opportunity_promoted event
7. Decompose to Beads tasks
8. Execute → Deliver → Retrospective
9. Log opportunity_delivered → outcome_validated events
```

### Scenario 3: Critical Opportunity (Priority 32, Critical)

```
1. Capture in 12 min (urgent)
2. VERA score: Priority 32 (Critical)
3. Start immediately (drop other work)
4. Waypoint if needed (can't afford wrong approach)
5. Promote to CORD immediately
6. Execute with high priority
7. Full retrospective with stakeholder communication
```

### Scenario 4: Low Priority (Priority 16, Low)

```
1. Capture in 10 min
2. VERA score: Priority 16 (Low)
3. Stays in inbox/opportunities/
4. Backlog (revisit quarterly)
5. Don't start until Higher/Critical opportunities completed
6. Re-evaluate VERA scores quarterly (context may change)
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Skipping Waypoint on High-Risk Work
**Symptom**: Starting 40+ hour effort without validation
**Fix**: If R ≤ 2 OR E ≤ 2, define waypoint first

### ❌ Anti-Pattern 2: Over-Detailed Capture (>15 min)
**Symptom**: Spending 30-60 min documenting before starting
**Fix**: Use template, aim for 10-15 min, refine during execution

### ❌ Anti-Pattern 3: VERA Without Quantification
**Symptom**: "Value = 5 because important" (no metrics)
**Fix**: Quantify time savings, adoption increase, ROI

### ❌ Anti-Pattern 4: No Intention Tracking
**Symptom**: Delivering without logging expected impact
**Fix**: Log opportunity_identified event with intended_impact

### ❌ Anti-Pattern 5: Ignoring Priority Bands
**Symptom**: Priority 18 (Low) but starting immediately
**Fix**: Respect bands - defer Low until High/Critical completed

---

## Tools & Automation

### justfile Recipes (Future - L2)

```bash
# Opportunity management
just opportunity-create "Short name"     # Create from template
just opportunity-score OPP-2025-022      # Calculate VERA priority
just opportunity-promote OPP-2025-022    # Promote to CORD

# Portfolio dashboard (L2)
just opportunity-dashboard               # Show all opportunities
just opportunity-list --priority high    # Filter by priority band
just opportunity-metrics                 # VERA accuracy report
```

### Manual Workflows (L1 - Current)

**Create opportunity**:
```bash
cp inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md \
   inbox/opportunities/OPP-2025-NNN-short-name.md
```

**Calculate VERA priority**:
```python
# Manual calculation
v, e, r, a = 5, 2, 3, 5  # VERA scores
priority = (v * 2.0) + (e * 1.5) + (r * 1.0) + (a * 2.5)
print(f"Priority: {priority}")  # 28.5
```

**Log A-MEM event**:
```bash
# Append to .chora/memory/events/2025-11.jsonl
echo '{
  "timestamp": "2025-11-21T00:00:00Z",
  "event_type": "opportunity_identified",
  "opportunity_id": "OPP-2025-022",
  "vera_scores": {"value": 5, "effort": 2, "risk": 3, "alignment": 5, "priority": 28.5}
}' >> .chora/memory/events/2025-11.jsonl
```

---

## Success Metrics

### L1 Validation (Achieved 2025-11-21)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Capture time | <15 min | 10-15 min | ✅ Met |
| VERA accuracy | 80%+ | 100% (2/2) | ✅ Exceeded |
| Waypoint ROI | ≥1 pivot prevented | 10-15x ROI | ✅ Met |
| Integration | Works with SAP-001/015/019/056 | All 4 working | ✅ Met |

### L2 Evolution Triggers

Adopt L2 when **ANY 2** of these occur:
1. >20 opportunities captured (automation value)
2. >30% have dependencies (portfolio scale)
3. <70% VERA accuracy (need historical data)
4. Stakeholders request dashboards (reporting burden)
5. 3+ custom templates (template fragmentation)

---

## Quick Reference Card

**VERA Formula**: `(V × 2.0) + (E × 1.5) + (R × 1.0) + (A × 2.5)`

**Priority Bands**:
- 30-35: Critical (start now)
- 25-29: High (1-2 weeks)
- 20-24: Medium (2-4 weeks)
- 15-19: Low (quarterly)
- <15: Defer

**Waypoint Trigger**: R ≤ 2 OR E ≤ 2
**Waypoint Time**: 3-4 hours
**Waypoint ROI**: 10-15x

**A-MEM Events**:
1. opportunity_identified (capture)
2. opportunity_promoted (CORD)
3. opportunity_delivered (complete)
4. outcome_validated (retrospective)

**Files**:
- Template: `inbox/opportunities/STRATEGIC-OPPORTUNITY-MANAGEMENT-L1.md`
- Opportunities: `inbox/opportunities/OPP-YYYY-NNN-*.md`
- Promoted: `inbox/incoming/coordination/CORD-YYYY-NNN.json`
- Events: `.chora/memory/events/YYYY-MM.jsonl`

---

**Version**: 1.0.0
**Status**: Pilot (L1 validated)
**Next Review**: After 5+ opportunities delivered
**Trace ID**: sap-060-awareness-guide-2025-11-21
