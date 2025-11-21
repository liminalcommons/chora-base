# SAP-064: Wardley Mapping Adoption Blueprint

**SAP ID**: SAP-064 (chora.strategic.wardley_mapping)
**Version**: 1.0.0
**Status**: Phase 2 (SAP Creation)
**Created**: 2025-11-20
**Trace ID**: wardley-phase-2-2025-11

---

## Overview

This blueprint documents the **L0 → L5 maturity path** for adopting SAP-064 (Wardley Mapping capability) in your repository.

**Purpose**: Provide clear adoption criteria, deliverables, and success metrics for each maturity level.

**Audience**: chora-workspace, chora-base adopters, external repos (chora-compose, chora-github)

---

## Maturity Model Overview

| Level | Name | Focus | Time Investment | Success Criteria | Deliverables |
|-------|------|-------|----------------|-----------------|--------------|
| **L0** | Aware | Read protocol-spec.md, understand 8 principles | 1-2 hours | Can explain Wardley evolution and value chain concepts | None |
| **L1** | Planned | Prepare strategic session (questions, stakeholders, components) | 2-3 hours | Strategic session agenda created, 6+ questions prepared | strategic-session-agenda.md |
| **L2** | Implemented | Create first manual map following protocol | 4-6 hours | Map created (10-15 components positioned), 90 min execution time | {ecosystem}-map-{date}-manual.md |
| **L3** | Validated | Conduct strategic session, achieve 1+ decision influenced | 2-3 hours | 1+ strategic decision influenced, 10x+ ROI documented | strategic-session-notes.md, gate-decision.md |
| **L4** | Distributed | Adopt in 2+ repos, refine protocol based on external feedback | 6-12 hours | 2+ external adoptions, protocol clarity 80%+, v1.1.0 refinement | 2+ map files (external repos), protocol-spec.md v1.1.0+ |
| **L5** | Sustained | Quarterly strategic mapping practice, selective automation (optional) | Ongoing | Quarterly maps created, automation IF criteria met (10+ maps/quarter) | Quarterly strategic reviews, automation scripts (IF justified) |

**Total Time to L3**: 9-14 hours (1-2 sprints)
**Total Time to L4**: 15-26 hours (2-4 sprints)
**Total Time to L5**: Ongoing (quarterly practice)

---

## Level 0: Aware (Understand Concepts)

### Goal

**Understand Wardley mapping concepts and how they integrate with chora ontology.**

### Prerequisites

- None (starting point for all adopters)

### Activities (1-2 hours)

**1. Read awareness-guide.md** (30 min)
- Quick start: What is Wardley mapping? Why use it?
- Four-step workflow overview (component extraction, evolution, value chain, gameplay)
- Eight strategic principles (cheat sheet)

**2. Read protocol-spec.md (optional, for depth)** (45-60 min)
- Detailed manual workflow documentation
- Step-by-step component extraction method
- Evolution classification rules (L0-L5 → Genesis/Commodity)
- Value chain analysis method (dependency depth, topological sort)
- Strategic gameplay identification (8 principles with examples)

**3. Review Phase 1 Example** (30 min)
- Read [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md)
- Review [strategic-session-notes-2025-11.md](../../../docs/wardley/strategic-session-notes-2025-11.md)
- Understand gate decision: [phase-1-gate-decision.md](../../../docs/wardley/phase-1-gate-decision.md)

### Success Criteria

**Knowledge Check** (can you answer these?):
- What is the difference between Genesis and Commodity evolution stages?
- What are the 4 value chain layers? (User Need → Foundation)
- What is Co-Evolution principle? When does it apply?
- What is Inertia Loop avoidance? (Don't over-invest in Genesis or Commodity)
- How does chora L0-L5 maturity map to Wardley evolution stages?

### Deliverables

- None (awareness only)

### Time Investment

- **Minimum**: 1 hour (awareness-guide.md + example map review)
- **Recommended**: 2 hours (protocol-spec.md deep dive)

---

## Level 1: Planned (Prepare Strategic Session)

### Goal

**Prepare strategic session materials: strategic questions, stakeholder identification, component list.**

### Prerequisites

- L0 complete (understand Wardley concepts)
- Access to `feature-manifest.yaml` (component extraction source)

### Activities (2-3 hours)

**1. Identify Strategic Context** (30 min)

What strategic decisions need to be made?
- **Examples from Phase 1**:
  - Q1: SAP-056 Acceleration Priority (Accelerate to L4? Maintain at L3? Defer?)
  - Q2: Wardley Build vs Defer (Invest in SAP-064? Defer? Adopt external tools?)
  - Q3: Memory System Investment (Maintain as-is? Enhance? Consolidate with SAP-056?)
  - Q4: Documentation vs New Capabilities (Invest in SAP-007? Maintain as Commodity? Extract patterns?)
  - Q5: Feature Manifest Schema Evolution (Extend now? Wait for validation? Keep minimal?)
  - Q6: Automation vs Manual Processes (Automate now? Wait for validation? Keep manual?)

**Strategic question format**:
```markdown
### Question N: [Decision Title]

**Context**: [Background information, why this decision matters]

**Decision Options**:
- Option A: [Describe first option]
- Option B: [Describe second option]
- Option C: [Describe third option]

**Wardley Analysis Framework**:
- Evolution positioning: [What question about Genesis → Commodity?]
- Value chain importance: [What question about dependencies?]
- Strategic principle: [Which of 8 principles might apply?]
```

**Recommended**: 6+ strategic questions (Phase 1 used 6, achieved 100% decision influence)

**2. Identify Stakeholders** (15 min)

Who should participate in the strategic session?
- **Technical lead**: Architecture decisions, capability priorities
- **Product manager**: Roadmap decisions, resource allocation
- **Strategic decision-maker**: Investment decisions, ecosystem strategy

**Self-validation mode** (Phase 1 approach):
- If no external stakeholders available, conduct self-validation session
- Develop strategic questions independently
- Answer each question twice (baseline vs Wardley-informed)
- Document decision changes and confidence improvements

**3. Extract Component List (Preview)** (60-90 min)

Following [protocol-spec.md Step 1](protocol-spec.md#step-1-component-extraction), identify 10-15 strategic components:

```bash
# List all features (quick scan)
grep -E "^  - id: FEAT-" feature-manifest.yaml | head -50

# Identify SAPs (strategic capabilities)
grep -A 3 "^  - id: FEAT-SAP-" feature-manifest.yaml

# Check feature names and statuses
grep -A 5 "name:" feature-manifest.yaml | grep -A 2 "status:"
```

**Selection criteria**:
- ✅ High-level SAPs and capabilities (not low-level code files)
- ✅ Cross-cutting concerns (affects multiple features)
- ✅ Differentiation points (unique to your repo vs commodity)
- ✅ Represent all value chain layers (User Need → Foundation)

**Target**: 10-15 components (Phase 1 used 15)

**4. Create Strategic Session Agenda** (30 min)

Document in `strategic-session-agenda-{date}.md`:
- Session purpose, participants, duration
- Strategic questions (6+)
- Answer format (baseline vs Wardley-informed)
- Success criteria (1+ decision influenced)

**Template**: See [strategic-session-agenda-2025-11.md](../../../docs/wardley/strategic-session-agenda-2025-11.md)

### Success Criteria

**Planning Complete** (can you answer these?):
- What strategic decisions will this map inform? (6+ questions)
- Who will participate in the strategic session? (stakeholders identified)
- What components will be mapped? (10-15 components identified)
- What is the success criteria? (1+ decision influenced, 10x+ ROI)

### Deliverables

- `strategic-session-agenda-{date}.md` (strategic questions, answer format, success criteria)

### Time Investment

- **Minimum**: 2 hours (3-4 strategic questions, basic component list)
- **Recommended**: 3 hours (6+ strategic questions, comprehensive component list)

---

## Level 2: Implemented (Create First Manual Map)

### Goal

**Create first manual Wardley map following protocol-spec.md (10-15 components positioned on evolution + value chain axes).**

### Prerequisites

- L1 complete (strategic session agenda created, component list identified)
- Dedicated time block (90-120 min uninterrupted)

### Activities (4-6 hours)

**1. Component Extraction** (45 min)

Following [protocol-spec.md Step 1](protocol-spec.md#step-1-component-extraction):
- Read feature-manifest.yaml to extract 10-15 strategic components
- Document: component name, feature ID, status, maturity level (L0-L5)
- Identify strategic rationale for each component (why include this?)

**Pain points to track**:
- Time spent on manual grepping (automation candidate if 10+ maps/quarter)
- Difficulty ranking strategic importance (subjective judgment)
- Tedious dependency extraction (feature.dependencies manual parsing)

**2. Evolution Classification** (15 min)

Following [protocol-spec.md Step 2](protocol-spec.md#step-2-evolution-classification):
- Apply L0-L5 → Genesis/Commodity mapping table
- Assign evolution position (0.0-1.0) to each component
- Document confidence score (High/Medium/Low) and rationale

**Mapping table reference**:
| chora Maturity | Wardley Stage | Position (0.0-1.0) |
|----------------|---------------|-------------------|
| L0 (Aware) | Genesis | 0.0 - 0.125 |
| L1 (Planned) | Genesis → Custom | 0.125 - 0.25 |
| L2 (Implemented) | Custom | 0.25 - 0.5 |
| L3 (Validated) | Custom → Product | 0.5 - 0.625 |
| L4 (Distributed) | Product → Commodity | 0.625 - 0.875 |
| L5 (Sustained) | Commodity | 0.875 - 1.0 |

**3. Value Chain Analysis** (30 min)

Following [protocol-spec.md Step 3](protocol-spec.md#step-3-value-chain-analysis):
- Extract dependency graph from feature.dependencies
- Calculate dependency depth (topological sort, manual for now)
- Assign value chain layer (User Need → Visible → Enabling → Foundation)
- Validate with strategic importance (user-facing components higher in chain)

**Pain points to track**:
- Dependency depth calculation tedious (manual hop counting)
- Circular dependency detection missing (error risk)
- No topological sort automation (strong automation candidate)

**4. Create Map File** (60-90 min)

Document in `{ecosystem}-map-{date}-manual.md`:
- Component extraction table (15 components with evolution + value chain positioning)
- Text-based map representation (ASCII diagram showing layers)
- Dependencies documented (A → B notation)
- Strategic observations (5+ insights from positioning)
- Pain points logged (for Phase 4 automation consideration)

**Template**: See [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md)

**Optional visual**: Export to Excalidraw or OnlineWardleyMaps for presentation

### Success Criteria

**Map Complete** (validation checklist):
- [ ] 10-15 components identified (not too few, not too many)
- [ ] All value chain layers represented (User Need → Foundation)
- [ ] All components positioned on evolution axis (0.0-1.0)
- [ ] Dependency graph extracted from feature.dependencies
- [ ] No circular dependencies (or documented if present)
- [ ] Text-based map representation created
- [ ] Strategic observations documented (3-5 insights)
- [ ] Pain points logged (time, errors, manual processes)

**Time to map**: 60-90 minutes execution time (Phase 1 achieved 90 min)

### Deliverables

- `{ecosystem}-map-{date}-manual.md` (complete map file with positioning, dependencies, observations)

### Time Investment

- **Minimum**: 4 hours (streamlined map creation, minimal documentation)
- **Recommended**: 6 hours (comprehensive map + strategic observations + pain point logging)

---

## Level 3: Validated (Conduct Strategic Session)

### Goal

**Conduct strategic session using Wardley map to inform strategic decisions. Achieve 1+ decision influenced with documented ROI.**

### Prerequisites

- L2 complete (first manual map created)
- Strategic session scheduled (stakeholders confirmed) OR self-validation mode

### Activities (2-3 hours)

**1. Prepare Strategic Session** (15 min)

- Review strategic-session-agenda.md (6+ questions)
- Annotate map with strategic questions (which components relate to each question?)
- Prepare baseline answers (what would you decide WITHOUT the map?)

**2. Conduct Strategic Session** (60-90 min)

**For each strategic question**:
1. **Baseline answer** (5-10 min): Answer WITHOUT referencing map
   - Decision: Option A/B/C
   - Reasoning: Text-based intuition, heuristics
   - Confidence: Low/Medium/High
   - Time to decision: X minutes

2. **Wardley-informed answer** (5-10 min): Answer WITH map positioning
   - Decision: Option A/B/C (may change from baseline)
   - Wardley positioning: Evolution stage, value chain layer, dependencies
   - Strategic principle applied: Which of 8 principles? (Co-Evolution, Build vs Buy, Inertia Loop, etc.)
   - Map reference: Specific component positioning that influenced decision
   - Confidence: Low/Medium/High (should improve vs baseline)
   - Time to decision: X minutes

3. **Comparison** (2-3 min): Document influence
   - Did map influence decision? YES / NO
   - If YES, how? (What did map reveal that text analysis missed?)
   - Decision changed? (Option A → Option B, or same option but higher confidence)

**Example from Phase 1 (Q1: SAP-056 Acceleration)**:
- **Baseline**: "Maintain SAP-056 at L3 (no urgent need)" (Medium confidence, 3 min)
- **Wardley-informed**: "Accelerate SAP-056 to L4 now (bottleneck removal + co-evolution)" (High confidence, 5 min)
- **Comparison**: ✅ YES influenced, decision REVERSED (B → A), principles: Co-Evolution (#1), Bottleneck Identification (#8)

**3. Document Session Outcomes** (30-45 min)

Create `strategic-session-notes-{date}.md`:
- Record all 6+ questions with baseline + Wardley-informed answers
- Summary table: decision changed? map influenced? principles applied?
- Strategic planning time metrics (session time vs baseline estimate)
- Value delivered: time saved, high-value work identified, ROI calculation

**4. Make Gate Decision** (15 min)

Create `gate-decision.md`:
- **Gate Question**: Did the Wardley map influence 1+ strategic decision?
- **Decision**: ✅ YES (proceed with SAP-064 adoption) OR ❌ NO (pivot/defer)
- **Evidence**: Strategic decisions influenced (% influenced, % changed)
- **Value delivered**: Time saved, ROI calculated
- **Confidence**: Very High / High / Medium / Low
- **Next steps**: Continue to L4 (if YES) or pivot (if NO)

### Success Criteria

**Strategic Value Validated**:
- [ ] Strategic decisions influenced: **1+ per map** (Phase 1: 6 out of 6 = 100%)
- [ ] Decision change rate: **50%+** (Phase 1: 4 out of 6 = 67%)
- [ ] Strategic principles applied: **3+ principles** (Phase 1: 8 principles)
- [ ] ROI: **10x+** (Phase 1: 15-25x)
- [ ] Strategic planning time reduction: **30%+** (Phase 1: 64% = 2.2 hours vs 4-6 baseline)

**Gate Decision**:
- [ ] ✅ **YES**: Map influenced 1+ decision → Proceed to L4 (high confidence SAP-064 delivers value)
- [ ] ❌ **NO**: Map didn't influence decisions → Pivot/Defer (save 12+ days, explore alternatives)

**SAP Maturity**: Achieve L3 (Validated) after gate decision PASSED

### Deliverables

- `strategic-session-notes-{date}.md` (6+ questions answered, decision influence documented)
- `gate-decision.md` (YES/NO with confidence, evidence, next steps)
- Ledger entry (adoption record with ROI, principles applied, pain points)

### Time Investment

- **Minimum**: 2 hours (4 strategic questions, basic session notes)
- **Recommended**: 3 hours (6+ strategic questions, comprehensive session notes, gate decision)

---

## Level 4: Distributed (External Adoption + Protocol Refinement)

### Goal

**Adopt SAP-064 in 2+ repositories (external to chora-workspace). Refine protocol-spec.md to v1.1.0+ based on external feedback.**

### Prerequisites

- L3 complete (chora-workspace adoption validated, gate decision PASSED)
- Access to external repos (chora-compose, chora-github, or other chora-base adopters)

### Activities (6-12 hours)

**1. Pilot SAP-064 in External Repo #1** (3-4 hours)

- Create map following protocol-spec.md (90 min)
- Track protocol clarity: "Could I follow the protocol easily?" (1-10 scale)
- Track pain points: What was unclear? What took longest? What had errors?
- Document adoption in ledger.md

**2. Pilot SAP-064 in External Repo #2** (3-4 hours)

- Create map following protocol-spec.md (90 min)
- Compare to Repo #1: Same pain points? Different strategic context?
- Track frequency: How often are maps being created? (5+ per quarter → automation candidate)

**3. Collect Feedback and Refine Protocol** (2-3 hours)

**Protocol clarity survey** (external adopters):
- "Could you create a map following protocol-spec.md?" (Yes/No)
- "Which step was unclear?" (Component extraction / Evolution / Value chain / Gameplay)
- "What would improve the protocol?" (Free text)

**Target**: 80%+ protocol clarity (external adopters can follow protocol)

**If clarity <80%**: Iterate on protocol-spec.md v1.1.0
- Clarify ambiguous steps (e.g., "How do I calculate dependency depth?")
- Add more examples (e.g., "What does Co-Evolution look like in practice?")
- Simplify complex sections (e.g., "Value chain topological sort")

**4. Update Ledger with External Adoptions** (30 min)

Document each external adoption:
- Repository name, adopter, map file path
- Components mapped, strategic decisions influenced
- Protocol clarity score (1-10)
- Pain points, automation candidates
- Time to map (60-90 min target)

### Success Criteria

**External Validation**:
- [ ] 2+ external repos adopted SAP-064 (chora-compose, chora-github, etc.)
- [ ] Protocol clarity: **80%+** external adopters can follow protocol-spec.md
- [ ] Time to map: **60-90 min** (within target range)
- [ ] Strategic decisions influenced: **1+ per map** (consistent with Phase 1)
- [ ] Pain point patterns identified (what consistently takes longest? high error risk?)

**Protocol Refinement**:
- [ ] protocol-spec.md v1.1.0+ released (if clarity <80%)
- [ ] Pain point thresholds tracked (frequency, manual time, error rate)
- [ ] Automation candidates prioritized (value chain analyzer STRONG candidate IF frequency validates)

**SAP Maturity**: Achieve L4 (Distributed) after 2+ external adoptions

### Deliverables

- 2+ map files (external repos)
- 2+ strategic session notes (external repos)
- 2+ ledger entries (external adoptions)
- protocol-spec.md v1.1.0+ (IF refinement needed)

### Time Investment

- **Minimum**: 6 hours (2 external maps × 90 min each + basic feedback collection)
- **Recommended**: 12 hours (2 external maps + comprehensive feedback + protocol iteration)

---

## Level 5: Sustained (Quarterly Practice + Selective Automation)

### Goal

**Institutionalize quarterly strategic mapping practice. Selectively automate validated pain points (IF criteria met).**

### Prerequisites

- L4 complete (external adoptions validated, protocol clarity 80%+)
- Quarterly strategic planning cadence established

### Activities (Ongoing)

**1. Quarterly Strategic Mapping Practice** (2-3 hours per quarter)

**Integration with roadmap planning**:
- Create Wardley map for quarterly strategic review (90 min)
- Use map to inform roadmap decisions (capability priorities, resource allocation)
- Document strategic decisions influenced (track ROI over time)

**Q-review format**:
- Q1: Annual strategic planning (comprehensive map, 15+ components)
- Q2: Mid-year roadmap adjustment (focused map, 8-10 components)
- Q3: Pre-planning for Q4 (focused map, 8-10 components)
- Q4: Year-end retrospective + next year planning (comprehensive map, 15+ components)

**2. Track Automation Thresholds** (30 min per quarter)

**Selective automation criteria**:
- **Manual time**: 30+ min per process
- **Frequency**: 10+ repetitions per quarter (or 5+ if high error risk)
- **Error rate**: 20%+ (quality/consistency issues)

**Track metrics**:
- Maps created per quarter (frequency threshold: 10+)
- Time per process (component extraction, value chain analysis, evolution classification)
- Error rate (circular dependencies detected, incorrect evolution positioning)

**3. Automate Validated Pain Points (IF criteria met)** (3-5 days one-time)

**Value Chain Analyzer** (STRONG candidate):
- **IF**: 5+ maps per quarter (frequency) AND high error risk (circular dependency detection)
- **THEN**: Build `scripts/wardley-value-chain-analyzer.py`
  - Topological sort of feature.dependencies
  - Detect circular dependencies (error detection)
  - Output layer assignments with dependency depth metrics
  - Reduce manual time from 30 min to <10 min
  - Reduce error rate from 20%+ to <5%

**Component Extractor** (DEFER unless high frequency):
- **IF**: 10+ maps per quarter (frequency) AND 45+ min manual time
- **THEN**: Build `scripts/wardley-component-extractor.py`
  - Parse feature-manifest.yaml
  - Rank components by strategic importance (dependencies, status, tags)
  - Output top N components with metadata
  - Reduce manual time from 45 min to <15 min

**Evolution Classifier** (DEFER, low pain):
- **Assessment**: Low pain (15 min, clear mapping table), keep manual
- **Only automate IF**: Error rate > 20% (confidence score misalignment)

**Gameplay Identification** (NOT algorithmic, keep manual):
- **Assessment**: Strategic principle identification requires expert judgment (not algorithmic)
- **Approach**: Document heuristics in protocol-spec.md, keep manual

### Success Criteria

**Quarterly Practice**:
- [ ] Quarterly maps created (Q1, Q2, Q3, Q4)
- [ ] Strategic decisions influenced: **1+ per quarter** (institutionalized practice)
- [ ] ROI tracked over time (cumulative value delivered)

**Selective Automation** (IF criteria met):
- [ ] Automation criteria validated (10+ maps per quarter, 30+ min manual, 20%+ error)
- [ ] Scripts reduce manual time by **50%+**
- [ ] Error rate reduced to **<5%**
- [ ] Scripts validated on **3+ maps**

**SAP Maturity**: Achieve L5 (Sustained) after 4+ quarterly practices OR selective automation deployed

### Deliverables

- 4+ quarterly map files (Q1-Q4)
- 4+ strategic session notes (quarterly reviews)
- Ledger entries (quarterly practice ROI)
- Automation scripts (IF criteria met): scripts/wardley-value-chain-analyzer.py

### Time Investment

- **Quarterly practice**: 2-3 hours per quarter (ongoing)
- **Automation** (optional): 3-5 days one-time (ONLY if selective automation criteria met)

---

## Adoption Checklist (Use This to Track Progress)

### L0: Aware (1-2 hours)

- [ ] Read awareness-guide.md (30 min)
- [ ] Read protocol-spec.md (optional, 45-60 min)
- [ ] Review Phase 1 example map (30 min)
- [ ] Pass knowledge check (can explain Wardley concepts)

### L1: Planned (2-3 hours)

- [ ] Identify strategic context (6+ questions prepared)
- [ ] Identify stakeholders (or plan self-validation)
- [ ] Extract component list (10-15 components identified)
- [ ] Create strategic-session-agenda.md

### L2: Implemented (4-6 hours)

- [ ] Component extraction (45 min, 10-15 components)
- [ ] Evolution classification (15 min, L0-L5 → 0.0-1.0)
- [ ] Value chain analysis (30 min, dependency depth, layer assignment)
- [ ] Create {ecosystem}-map-{date}-manual.md (complete map file)
- [ ] Log pain points (time, errors, manual processes)

### L3: Validated (2-3 hours)

- [ ] Prepare strategic session (review agenda, annotate map)
- [ ] Conduct strategic session (6+ questions, baseline + Wardley-informed)
- [ ] Document strategic-session-notes.md (decision influence, ROI)
- [ ] Make gate decision (gate-decision.md: YES/NO with confidence)
- [ ] Achieve 1+ decision influenced, 10x+ ROI

### L4: Distributed (6-12 hours)

- [ ] Pilot SAP-064 in external repo #1 (3-4 hours)
- [ ] Pilot SAP-064 in external repo #2 (3-4 hours)
- [ ] Collect feedback, track protocol clarity (80%+ target)
- [ ] Refine protocol-spec.md to v1.1.0+ (IF clarity <80%)
- [ ] Update ledger with external adoptions

### L5: Sustained (Ongoing)

- [ ] Quarterly strategic mapping practice (Q1-Q4)
- [ ] Track automation thresholds (frequency, manual time, error rate)
- [ ] Automate validated pain points IF criteria met (value chain analyzer STRONG candidate)
- [ ] Document quarterly ROI (cumulative value delivered)

---

## Estimated Timeline

| Maturity Level | Time Investment | Cumulative Time | Calendar Time |
|---------------|----------------|----------------|--------------|
| **L0** (Aware) | 1-2 hours | 1-2 hours | 1 day (self-paced) |
| **L1** (Planned) | 2-3 hours | 3-5 hours | 1-2 days |
| **L2** (Implemented) | 4-6 hours | 7-11 hours | 1 sprint (1 week) |
| **L3** (Validated) | 2-3 hours | 9-14 hours | 1-2 sprints |
| **L4** (Distributed) | 6-12 hours | 15-26 hours | 2-4 sprints |
| **L5** (Sustained) | 2-3 hours/quarter (ongoing) | Ongoing | Quarterly |

**Fastest path to L3**: 9 hours (minimum) = 1 focused sprint
**Recommended path to L3**: 14 hours = 1-2 sprints with buffer
**Full adoption to L4**: 15-26 hours = 2-4 sprints

---

## References

### Phase 1 Evidence (chora-workspace L3 Adoption)

- [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md) - First manual map (15 components, 4 layers)
- [strategic-session-notes-2025-11.md](../../../docs/wardley/strategic-session-notes-2025-11.md) - 6 strategic questions, 100% decision influence, 15-25x ROI
- [phase-1-gate-decision.md](../../../docs/wardley/phase-1-gate-decision.md) - Gate PASSED (0.95 confidence)

### Protocol and Quick Reference

- [protocol-spec.md](protocol-spec.md) - Detailed manual workflow (Phase 1 validated)
- [awareness-guide.md](awareness-guide.md) - Quick reference (condensed version)

### Capability Charter

- [capability-charter.md](capability-charter.md) - Problem, vision, scope, success criteria

---

**Version**: 1.0.0
**Status**: Phase 2 (SAP Creation)
**Created**: 2025-11-20
**Author**: tab-1 (Claude Code)
**Trace ID**: wardley-phase-2-2025-11
**Next**: Create awareness-guide.md (Task 2.2, Artifact 3)
