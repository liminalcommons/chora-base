# SAP Synergy Discovery & Pursuit Plan

**Date**: 2025-11-03
**Type**: Strategic Framework
**Status**: Active
**Impact**: High - Enables systematic discovery of emergent value opportunities

---

## Executive Summary

This plan provides a structured approach for discovering and pursuing **emergent value that arises when capabilities combine in ways that create outcomes greater than the sum of their parts** across the SAP ecosystem.

**Key Shift**: From documenting existing synergies → to systematically discovering workflow gaps where integration creates emergent value.

**Core Philosophy**:
- Synergies are not metadata to catalog
- Synergies are opportunities to create workflow coherence, context continuity, and transformative adoption patterns
- Design for synergies means exposing integration points, creating intentional overlaps, and building feedback loops

---

## What Are Synergies?

**Synergies are emergent value** created when SAP capabilities combine to produce outcomes greater than their individual contributions.

### Characteristics of Transformative Synergies

1. **Context Continuity**: Information flows automatically without manual bridging
   - Example: CHORA_TRACE_ID from inbox → lifecycle → metrics → memory

2. **Workflow Coherence**: SAPs orchestrate as unified workflow, not adjacent tools
   - Example: SAP-012 DDD phase automatically invokes SAP-007 Diataxis templates

3. **Adaptive Learning**: Output from one SAP improves another's future performance
   - Example: SAP-013 defect patterns update SAP-003 project templates

4. **Network Effects**: Value increases exponentially with adoption
   - Example: SAP-001 inbox creates ecosystem coordination at 3+ repos

5. **Emergent Capabilities**: The combination enables something neither SAP could do alone
   - Example: SAP-009 + SAP-010 = "Agents that learn from project history"

---

## Discovery Methodology: The Workflow Continuity Canvas

Discover synergy opportunities across three dimensions by mapping workflow gaps.

### Dimension 1: Context Continuity Gaps

**Definition**: Places where context is lost, recreated, or manually bridged between SAPs

#### Discovery Questions

1. **Traceability Breaks**: Where does CHORA_TRACE_ID or coordination context disappear?
   - Example: SAP-001 (inbox) → SAP-012 (lifecycle) has trace continuity
   - Gap opportunity: SAP-013 (metrics) doesn't feed back to SAP-001 proposals

2. **Semantic Translation Barriers**: Where do concepts get renamed/reinterpreted?
   - Example: "acceptance criteria" (SAP-012 DDD) vs "test scenarios" (SAP-004) vs "validation rules" (SAP-006)
   - Opportunity: Unified glossary that SAP-009 (agent-awareness) could expose

3. **State Handoff Friction**: Where does one SAP's output require manual transformation for another's input?
   - Example: SAP-007 (docs) → SAP-012 (DDD) works via Diataxis structure
   - Gap opportunity: SAP-010 (memory) doesn't auto-populate SAP-007 glossary

#### Example Gap Documentation

```yaml
gap_id: GAP-001
name: "Metrics Don't Inform Templates"
description: |
  SAP-013 tracks high-defect patterns (e.g., "missing async fixtures causes 40% of test bugs")
  but SAP-003 project templates don't incorporate these learnings.
current_workflow: |
  Developers manually check PROCESS_METRICS.md and remember to add patterns
synergy_opportunity: |
  SAP-013 could generate "anti-pattern snippets" that SAP-003 templates auto-include
  based on defect frequency thresholds
estimated_frequency: "Every new project (2-4/month)"
time_saved: "30-60min debugging/fixing + prevents 2-3 bugs"
evs_score: 82/100
  workflow_impact: 2 (eliminates manual lookup)
  adoption_multiplier: 3 (makes both SAPs more valuable)
  discovery_potential: 2 (pattern: metrics → templates)
  gap_size: 3 (prevents recurring bugs)
  ecosystem_leverage: 3 (benefits all new projects)
```

### Dimension 2: Workflow Coherence Gaps

**Definition**: Places where SAPs work adjacently but not as a unified workflow

#### Discovery Questions

1. **Circular Value Loops**: Where could output from SAP B enhance SAP A's effectiveness?
   - Gap: SAP-013 metrics don't inform SAP-003 blueprint generation templates
   - Opportunity: "High-defect pattern detection" could update SAP-003 anti-pattern templates

2. **Validation Cascades**: Where could one SAP's validation strengthen another's quality gates?
   - Gap: SAP-016 (link validation) only checks docs, not SAP protocol-specs
   - Opportunity: Validate SAP dependency declarations match actual system_files

3. **Progressive Enhancement**: Where could SAP A's presence make SAP B dramatically better?
   - Example: SAP-021 + SAP-026 (React testing + accessibility)
   - Gap opportunity: SAP-009 (agent-awareness) could auto-generate context based on SAP-010 (memory) learnings

### Dimension 3: Adoption Pattern Gaps

**Definition**: Missing intermediate steps or prerequisites that block transformative adoption

#### Discovery Questions

1. **Cliff vs Slope**: Where do SAPs have high adoption friction despite high value?
   - Gap: SAP-012 (full lifecycle) is comprehensive but overwhelming for small teams
   - Opportunity: "SAP-012-lite" subset for simple features (skip Phases 1-2)

2. **Activation Energy**: What's missing that would make SAP combinations "click"?
   - Example: SAP-020→SAP-026 (React stack) has 2.8x→5.0x multiplier jump
   - Gap opportunity: What integration scripts/templates bridge this gap?

3. **Network Effects**: Where do SAPs become exponentially valuable with critical mass?
   - Example: SAP-001 (inbox) only creates network effects with 3+ repos
   - Opportunity: "Ecosystem activation threshold" metrics

---

## Prioritization Framework: Emergent Value Score (EVS)

Score synergy opportunities on five factors to prioritize pursuit.

### Factor 1: Workflow Impact (Weight: 35%)

**Question**: Does this synergy eliminate manual handoffs or create new workflow capabilities?

**Scoring**:
- **3 points**: Creates entirely new workflow (e.g., SAP-001 + SAP-012 + SAP-013 feedback loop)
- **2 points**: Eliminates manual step (e.g., SAP-007 test extraction)
- **1 point**: Reduces friction (e.g., shared configuration)
- **0 points**: Convenience only

**High-Value Pattern**: Context continuity synergies (CHORA_TRACE_ID flows end-to-end)

### Factor 2: Adoption Multiplier (Weight: 25%)

**Question**: Does this synergy make multiple SAPs easier to adopt together than separately?

**Scoring**:
- **3 points**: Reduces combined adoption time by >50% (e.g., React foundation stack)
- **2 points**: Reduces by 25-50% (e.g., Testing + CI/CD)
- **1 point**: Reduces by 10-25%
- **0 points**: No adoption benefit

**High-Value Pattern**: "Cliff removal" synergies that provide intermediate steps

### Factor 3: Discovery Potential (Weight: 20%)

**Question**: Does this synergy enable discovering additional synergies?

**Scoring**:
- **3 points**: Meta-synergy (helps find other synergies) - e.g., SAP-009 + SAP-010 learning loop
- **2 points**: Cross-domain bridge (connects isolated SAP clusters)
- **1 point**: Within-domain enhancement
- **0 points**: Terminal synergy

**High-Value Pattern**: Synergies involving SAP-009 (awareness), SAP-010 (memory), SAP-013 (metrics)

### Factor 4: Gap Size (Weight: 15%)

**Question**: How large is the current workflow break this would fix?

**Scoring**:
- **3 points**: Major gap (hours of manual work or data loss)
- **2 points**: Moderate gap (30-60 min manual bridging)
- **1 point**: Minor gap (convenience)
- **0 points**: No current gap

**High-Value Pattern**: Gaps between domains (SDL ↔ Agent Cognition)

### Factor 5: Ecosystem Leverage (Weight: 5%)

**Question**: Does this benefit scale across multiple adopters?

**Scoring**:
- **3 points**: Benefits all ecosystem adopters automatically
- **2 points**: Benefits with minimal per-repo customization
- **1 point**: Requires per-repo implementation
- **0 points**: chora-base only

### EVS Calculation

```
EVS = (Workflow Impact × 0.35) + (Adoption Multiplier × 0.25) +
      (Discovery Potential × 0.20) + (Gap Size × 0.15) +
      (Ecosystem Leverage × 0.05)

Score range: 0-3 per factor
Total EVS range: 0.0 - 3.0
```

**Prioritization Thresholds**:
- **EVS ≥ 2.5**: Critical - pursue immediately
- **EVS 2.0-2.49**: High - pursue in next sprint
- **EVS 1.5-1.99**: Medium - backlog for future consideration
- **EVS < 1.5**: Low - document but defer

---

## Concrete First Steps

### Phase 1: Discovery (Week 1-2)

#### Action 1: Gap Audit Sprint (2 days)

**Objective**: Systematically identify the top 10 workflow continuity gaps

**Method**:
1. Map the 5 documented "end-to-end-workflow" synergies from sap-catalog.json
2. For each workflow, trace where context/state gets manually bridged
3. Interview pattern: "When you go from SAP X to SAP Y, what do you have to remember/lookup/recreate?"

**Deliverable**: "Workflow Continuity Gap Report" with:
- Gap description
- Current workaround (if any)
- Estimated frequency (daily/weekly/monthly)
- Impact if eliminated (time + quality)
- EVS score breakdown

**Starting Points**:
- SDL workflows: SAP-001 → SAP-012 → SAP-013
- React workflows: SAP-020 → SAP-021 → SAP-022 → SAP-026
- Agent workflows: SAP-009 → SAP-010
- Meta-governance: SAP-027 → SAP-028 → SAP-029

#### Action 2: Traceability Audit (1 day)

**Objective**: Map where CHORA_TRACE_ID and coordination context flows vs breaks

**Method**:
1. Start with SAP-001 (inbox) coordination request
2. Follow CHORA_TRACE_ID through documented workflow (SAP-012 phases)
3. Identify where trace ID is lost, not captured, or requires manual propagation
4. Check which SAPs could consume but don't: SAP-010 (memory), SAP-013 (metrics), SAP-016 (validation)

**Deliverable**: "Context Flow Diagram" showing:
- **Green arrows**: Automatic context propagation
- **Yellow arrows**: Manual but documented handoff
- **Red X**: Context lost / manual recreation

**High-Value Discoveries to Look For**:
- SAP-010 (memory) could auto-tag events with CHORA_TRACE_ID from SAP-001
- SAP-013 (metrics) could aggregate by trace ID to measure "idea → production" lead time
- SAP-016 (link validation) could verify trace IDs in protocol-specs match inbox/

#### Action 3: Cross-Domain Synergy Workshop (3 sessions × 2 hours)

**Objective**: Discover synergies that cross domain boundaries (highest discovery potential)

**Method**:
1. Select 2 SAPs from different domains
2. Ask: "If these SAPs could share state/context, what becomes possible?"
3. Prototype the integration on paper (API sketch, workflow diagram)
4. Score with EVS framework

**Focus Combinations**:
- **SAP-009 (agent-awareness) + SAP-013 (metrics)**: Could agents learn from metrics?
- **SAP-010 (memory) + SAP-007 (docs)**: Could memory auto-populate glossary?
- **SAP-001 (inbox) + SAP-028 (publishing)**: Could coordination trigger releases?

**Deliverable**: 3 "Synergy Opportunity Briefs" (1-page each) with:
- Synergy name and type
- Integration points (APIs, shared files, workflow hooks)
- Prototype workflow diagram
- Estimated EVS score
- Next validation step

### Phase 2: Prioritization & Selection (End of Week 2)

#### Action 4: Calculate EVS Scores

**Method**:
1. Score all discovered gaps and workshop opportunities using EVS framework
2. Create priority-ordered backlog
3. Select highest-scoring opportunity (EVS ≥ 2.5) for validation

**Deliverable**: "Synergy Opportunity Backlog" with:
- Ranked list of all discovered opportunities
- EVS scores and factor breakdowns
- Selected opportunity for Phase 3 implementation

### Phase 3: First Synergy Implementation (Month 1)

#### Action 5: Implement & Validate Highest-Priority Synergy

**Likely Candidates** (based on research):
1. **Metrics → Templates Learning Loop** (GAP-001)
   - SAP-013 exports defect patterns → SAP-003 templates auto-include
   - EVS estimate: 2.6-2.8

2. **End-to-End Trace Continuity**
   - SAP-001 → SAP-012 → SAP-013 → SAP-010 all share CHORA_TRACE_ID
   - EVS estimate: 2.7-2.9

3. **Agent-Aware Memory-Driven Glossary**
   - SAP-009 + SAP-010 → auto-populate SAP-007 glossary
   - EVS estimate: 2.4-2.6

**Method**:
1. Design integration (APIs, file formats, hooks)
2. Implement minimum viable synergy (MVS)
3. Measure impact:
   - Before: time to complete workflow, manual steps required
   - After: time to complete workflow, automation level
   - Delta: time saved, quality improvement, friction reduction

**Deliverable**: "Synergy Implementation Case Study" with:
- Synergy description and EVS score
- Implementation details (code, configs, workflow changes)
- Before/after metrics
- Lessons learned
- Replication guide for similar synergies

---

## Design Principles for "Designing for Synergies"

### Principle 1: Exposed Affordances

**Instead of**: SAPs as isolated capabilities
**Design for**: SAPs that explicitly expose integration points

**Pattern**: Add "Integration Affordances" section to protocol-spec.md

```yaml
## Integration Affordances

### State Exports
- `PROCESS_METRICS.md`: Machine-readable defect patterns (SAP-013)
  - Format: YAML frontmatter + markdown tables
  - Consumers: SAP-003 (templates), SAP-010 (memory)
  - Update frequency: Weekly

### Event Hooks
- `post_install`: Triggered after SAP adoption
  - Payload: {sap_id, timestamp, repo, trace_id}
  - Consumers: SAP-001 (inbox ledger update), SAP-010 (memory event)
  - Location: .sap/hooks/post_install.sh

### Workflow Hooks
- `pre_phase_3`: Called before DDD phase (SAP-012)
  - Input: feature_description
  - Output: suggested_diataxis_type (from SAP-007)
  - Consumer: SAP-009 (agent workflow automation)
  - Protocol: REST endpoint or CLI command
```

**Implementation Checklist**:
- [ ] Every SAP protocol-spec includes "Integration Affordances" section
- [ ] State exports use machine-readable formats (YAML, JSON, not just prose)
- [ ] Event hooks follow consistent naming (pre_/post_ + action)
- [ ] Workflow hooks include input/output schemas

### Principle 2: Intentional Overlaps

**Instead of**: Strict scope boundaries between SAPs
**Design for**: Deliberate overlaps that create synergy opportunities

**Pattern**: Shared contracts that multiple SAPs contribute to/consume from

**Example: Shared Glossary**
```yaml
# .sap/shared/glossary.yaml (shared contract)

terms:
  - term: "acceptance criteria"
    aliases: ["test scenarios", "validation rules"]
    definition: "Conditions that must be met for feature to be considered complete"
    sources:
      - sap: "SAP-012"
        context: "DDD Phase 3 output"
      - sap: "SAP-004"
        context: "Test scenarios for pytest"
      - sap: "SAP-006"
        context: "Quality gate validation rules"
    consumers:
      - "SAP-007" # Documentation framework uses for glossary generation
      - "SAP-009" # Agent awareness uses for bidirectional translation
      - "SAP-010" # Memory stores learned terms
    last_updated: "2025-11-03"
    usage_count: 42
```

**Benefits**:
- SAP-007 defines schema
- SAP-009 consumes for bidirectional translation
- SAP-010 contributes learned terms
- SAP-013 tracks glossary coverage metrics

**Implementation Checklist**:
- [ ] Identify high-overlap concepts (glossary, trace IDs, metrics, quality gates)
- [ ] Create shared contract files in `.sap/shared/`
- [ ] Document which SAPs contribute vs consume
- [ ] Add validation that all contributors follow schema

### Principle 3: Progressive Disclosure of Complexity

**Instead of**: All-or-nothing SAP adoption
**Design for**: Lightweight → Standard → Advanced tiers

**Pattern**: Multi-tier adoption paths in adoption-blueprint.md

**Example: SAP-012 (Development Lifecycle) Tiers**
```yaml
adoption_tiers:
  tier_1_lightweight:
    name: "Essential Flow"
    phases: [3, 4, 5]  # DDD → Dev → Test (skip Vision, Planning, Release, Monitor)
    use_case: "Simple bug fixes, small features"
    setup_time: "15 minutes"
    integrations: []
    time_multiplier: 1.0 (baseline)

  tier_2_standard:
    name: "Full Lifecycle"
    phases: [1, 2, 3, 4, 5, 6, 7, 8]
    use_case: "Major features, new projects"
    setup_time: "2-4 hours"
    integrations:
      - SAP-005 (CI/CD for Phase 6-7)
      - SAP-006 (Quality gates for Phase 5)
    time_multiplier: 1.8x (vs manual full lifecycle)

  tier_3_advanced:
    name: "Ecosystem Integration"
    phases: [1, 2, 3, 4, 5, 6, 7, 8]
    use_case: "Cross-repo coordination, strategic features"
    setup_time: "1-2 days"
    integrations:
      - SAP-001 (inbox coordination for Phase 1-2)
      - SAP-005 (CI/CD for Phase 6-7)
      - SAP-006 (Quality gates for Phase 5)
      - SAP-013 (metrics for Phase 8)
      - SAP-010 (memory for learnings)
    time_multiplier: 2.5x (vs manual + tier benefits from integrations)
```

**Benefits**:
- Removes adoption cliff for complex SAPs
- Creates clear upgrade path (tier 1 → tier 2 → tier 3)
- Makes synergy value explicit (multipliers increase with integration)

**Implementation Checklist**:
- [ ] Identify SAPs with high adoption friction (>2 hour setup)
- [ ] Design 3-tier structure (lightweight, standard, advanced)
- [ ] Document which integrations unlock which tier
- [ ] Add migration guides between tiers

### Principle 4: Synergy-First Architecture Review

**Instead of**: Reviewing SAPs in isolation
**Design for**: Every new SAP/update requires "Synergy Impact Assessment"

**Pattern**: Add checklist to SAP approval process (SAP-000 framework)

```markdown
## Synergy Impact Assessment (required for protocol-spec approval)

Rate each dimension 0-3:

1. **State Exports** (0-3): What machine-readable outputs could other SAPs consume?
   - [ ] 0: No exports
   - [ ] 1: Prose-only outputs (markdown without frontmatter)
   - [ ] 2: Structured exports (YAML/JSON) but no documented consumers
   - [ ] 3: Structured exports with explicit consumer contracts

2. **Event Hooks** (0-3): What lifecycle events could trigger cross-SAP workflows?
   - [ ] 0: No hooks
   - [ ] 1: Manual triggers only
   - [ ] 2: Scriptable hooks but no standard protocol
   - [ ] 3: Standard hook protocol with documented consumers

3. **Shared Contracts** (0-3): What schemas/formats align with existing SAPs?
   - [ ] 0: Unique formats incompatible with other SAPs
   - [ ] 1: Compatible but requires manual translation
   - [ ] 2: Uses shared contracts for some outputs
   - [ ] 3: Fully aligned with shared contract ecosystem

4. **Gap Analysis** (0-3): What workflow gaps does this SAP create or solve?
   - [ ] 0: Creates new gaps without solving existing ones
   - [ ] 1: Neutral (no new gaps, solves none)
   - [ ] 2: Solves 1-2 existing gaps
   - [ ] 3: Solves 3+ existing gaps or major workflow break

5. **Discovery Potential** (0-3): Does this SAP enable finding new synergies?
   - [ ] 0: Terminal capability (dead end)
   - [ ] 1: Single-domain enhancement only
   - [ ] 2: Cross-domain bridge potential
   - [ ] 3: Meta-capability (enables discovering synergies)

**Synergy Score**: __/15 (sum of all ratings)

**Approval Threshold**: 9+ required for approval (average 1.8 per dimension)

**If score < 9**: Identify 2-3 enhancements to reach threshold before approval
```

**Implementation Checklist**:
- [ ] Add Synergy Impact Assessment to SAP-000 framework
- [ ] Require assessment for all new SAPs (SAP-031+)
- [ ] Retroactively assess existing SAPs to identify improvement opportunities
- [ ] Track synergy scores over time (target: increasing average)

---

## Strategic Actions (Month 2-3)

### Action 6: Create "Synergy SAPs"

**Concept**: Some synergies are so valuable they deserve their own SAP (meta-SAPs that orchestrate other SAPs)

**Candidates**:

#### SAP-033: Trace-Driven Development
- **Combines**: SAP-001 (inbox) + SAP-012 (lifecycle) + SAP-013 (metrics) + SAP-010 (memory)
- **Benefit**: End-to-end traceability from strategic proposal → metrics → learnings
- **Type**: Meta-SAP (orchestrates other SAPs)
- **EVS Estimate**: 2.8-3.0
- **Implementation**: Protocol for trace ID propagation, aggregation, and feedback loops

#### SAP-034: Adaptive Templates
- **Combines**: SAP-003 (bootstrap) + SAP-013 (metrics) + SAP-010 (memory)
- **Benefit**: Templates that learn from defect patterns and automatically incorporate fixes
- **Type**: Enhancement SAP
- **EVS Estimate**: 2.6-2.8
- **Implementation**: Defect pattern extraction from SAP-013 → template injection in SAP-003

#### SAP-035: Workflow Automation Bridges
- **Combines**: SAP-008 (scripts) + SAP-012 (lifecycle) + SAP-005 (CI/CD)
- **Benefit**: Automated transitions between lifecycle phases with validation
- **Type**: Integration SAP
- **EVS Estimate**: 2.4-2.6
- **Implementation**: Hook-based phase transitions with quality gates

**Deliverable**: Formalize top 1-2 synergies as new SAPs using SAP generation (SAP-028 + SAP-029)

### Action 7: Synergy Discovery Automation

**Objective**: Build tools to continuously discover new synergy opportunities

**Tools to Build**:

1. **Gap Detector** (extends SAP-013 metrics-tracking)
   - Analyzes commit messages for friction phrases:
     - "manually copied"
     - "had to remember"
     - "looked up in"
     - "TODO: automate"
   - Generates "Potential Gap Report" weekly
   - Output: Ranked list of workflow friction points

2. **Workflow Tracer** (extends SAP-001 inbox + SAP-010 memory)
   - Follows CHORA_TRACE_ID through all SAP-touched files
   - Visualizes context flow (green/yellow/red)
   - Identifies trace breaks as potential gaps
   - Output: Interactive flow diagram

3. **Co-Adoption Analyzer** (extends SAP-013 metrics-tracking)
   - Mines ledger.md files across ecosystem
   - Finds unexpected SAP combinations with high success
   - Detects anti-patterns (co-adoption with low success)
   - Output: "Unexpected Synergy Candidates" report

**Implementation**: Integrate into SAP-013 (metrics-tracking) as new metric types

**Deliverable**: 3 automated discovery tools generating weekly synergy opportunity reports

### Action 8: Ecosystem Synergy Dashboard

**Objective**: Visualize synergy adoption and impact across all repos

**Dashboard Views**:

1. **Synergy Heatmap**
   - Rows: SAPs (30+)
   - Columns: SAPs (30+)
   - Cell color: Co-adoption frequency (white = never, red = always)
   - Annotations: EVS scores for documented synergies

2. **Gap Backlog**
   - Prioritized list of workflow continuity gaps
   - Columns: Gap name, EVS score, affected SAPs, status (discovered/validated/implemented)
   - Filters: By domain, by EVS threshold, by implementation status

3. **Impact Timeline**
   - X-axis: Time (weeks)
   - Y-axis: Cumulative value (time saved, defects prevented)
   - Lines: Each implemented synergy shows impact over time
   - Annotations: Synergy implementation milestones

**Technology**: Static HTML generated by SAP-013 (metrics-tracking), hosted via GitHub Pages

**Deliverable**: Live dashboard at `https://chora-base.github.io/synergy-dashboard/`

---

## Success Criteria

### Phase 1 (Week 1-2)
- [ ] At least 10 workflow continuity gaps documented with EVS scores
- [ ] Context flow mapped for 2+ end-to-end workflows (CHORA_TRACE_ID tracing)
- [ ] 3 cross-domain synergy opportunities prototyped with briefs
- [ ] Synergy Opportunity Backlog created and prioritized

### Phase 2 (Month 1)
- [ ] Highest-priority synergy (EVS ≥ 2.5) implemented
- [ ] Before/after metrics demonstrate measurable impact (time or quality)
- [ ] Case study documented with replication guide
- [ ] At least 1 additional synergy moved to "validated" status

### Phase 3 (Month 2-3)
- [ ] 1-2 synergies formalized as new SAPs (SAP-033, SAP-034, or SAP-035)
- [ ] Synergy discovery automation tools integrated into SAP-013
- [ ] Synergy Impact Assessment added to SAP-000 framework
- [ ] Ecosystem Synergy Dashboard deployed and tracking 5+ repos

### Ongoing
- [ ] Average Synergy Impact Assessment score for new SAPs > 9/15
- [ ] At least 2 new synergies discovered per quarter (via automated tools)
- [ ] Ecosystem dashboard shows increasing co-adoption rates for high-EVS synergies

---

## Key Insights

### What Makes a Synergy Transformative (Not Just Additive)

| Characteristic | Additive (1.1-1.5x) | Transformative (2.0x+) |
|----------------|---------------------|------------------------|
| **Context Flow** | Manual bridging required | Automatic propagation (CHORA_TRACE_ID) |
| **Workflow** | Adjacent tools used separately | Unified orchestrated workflow |
| **Learning** | Static capabilities | Adaptive (output improves input) |
| **Network Effects** | Linear value (1+1=2) | Exponential value (1+1=5) |
| **Capabilities** | Sum of parts | Emergent (neither could do alone) |

### The Difference: Current vs Proposed Approach

| Current (Documenting Synergies) | Proposed (Discovering Synergies) |
|--------------------------------|----------------------------------|
| **Reactive**: document after adoption | **Proactive**: find opportunities before building |
| **Focus**: time multipliers | **Focus**: workflow continuity gaps |
| **Metric**: co-adoption rate | **Metric**: Emergent Value Score (EVS) |
| **Scope**: pairwise SAP combinations | **Scope**: workflow journeys across domains |
| **Outcome**: catalog of what works | **Outcome**: prioritized pipeline of opportunities |
| **Deliverable**: sap-catalog.json updates | **Deliverable**: SAP enhancements + new meta-SAPs |

---

## Next Steps

1. **Immediate** (this week): Begin Gap Audit Sprint (Action 1)
2. **Week 2**: Complete Traceability Audit (Action 2) and Cross-Domain Workshop (Action 3)
3. **Month 1**: Implement and validate first high-EVS synergy (Action 5)
4. **Month 2-3**: Build automation tools and formalize top synergies as SAPs (Actions 6-8)

---

**Plan Created**: 2025-11-03
**Status**: Ready for execution
**Owner**: SAP ecosystem steward
**Review Cadence**: Weekly during Phase 1, bi-weekly during Phase 2-3
