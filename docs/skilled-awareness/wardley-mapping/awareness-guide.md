# SAP-064: Wardley Mapping Awareness Guide (Quick Reference)

**SAP ID**: SAP-064 (chora.strategic.wardley_mapping)
**Version**: 1.0.0
**Created**: 2025-11-20
**Audience**: Quick start for new adopters

---

## What is Wardley Mapping?

**Wardley mapping** is a visual strategic positioning tool that helps you:
- **See where capabilities are evolving** (Genesis → Commodity)
- **Identify dependencies** (value chain analysis)
- **Make evidence-based strategic decisions** (not just intuition)

**Why use it?**
- **Identify bottlenecks**: Lower evolution components blocking higher-level capabilities
- **Avoid over-investment**: Don't enhance Commodity (mature) or over-build Genesis (uncertain)
- **Discover ecosystem opportunities**: Extract patterns from Commodity capabilities
- **Improve decision confidence**: Medium → High confidence (evidence-based vs intuition)

**When to create a map?**
- Quarterly strategic planning (roadmap decisions, capability priorities)
- Major investment decisions (build vs buy, accelerate vs defer)
- Cross-repo integration planning (chora-workspace, chora-base, chora-compose)
- SAP lifecycle decisions (which SAPs to accelerate? maintain? deprecate?)

---

## Four-Step Workflow (90 minutes total)

```
Step 1: Component Extraction (45 min)
   ↓
Step 2: Evolution Classification (15 min)
   ↓
Step 3: Value Chain Analysis (30 min)
   ↓
Step 4: Strategic Gameplay (20-39 min, during strategic session)
```

---

## Step 1: Component Extraction (45 min)

**Goal**: Identify 10-15 strategic components from `feature-manifest.yaml`

**Quick commands**:
```bash
# List all features
grep -E "^  - id: FEAT-" feature-manifest.yaml | head -50

# Find SAPs (strategic capabilities)
grep -A 3 "^  - id: FEAT-SAP-" feature-manifest.yaml

# Check statuses
grep -A 5 "name:" feature-manifest.yaml | grep -A 2 "status:"
```

**Selection criteria**:
- ✅ High-level SAPs and capabilities (not code files)
- ✅ Cross-cutting concerns (affects multiple features)
- ✅ Unique to your repo vs commodity (Git, YAML)
- ✅ All value chain layers represented (User Need → Foundation)

**Target**: 10-15 components (not too few, not too many)

**Example components**:
- User Need: Strategic Decision-Making
- Visible: Wardley Maps, Knowledge Notes, Strategic Reports
- Enabling: Memory System (SAP-010), Traceability (SAP-056), Metrics (SAP-013)
- Foundation: Git, YAML/JSON, SAP Frontmatter

---

## Step 2: Evolution Classification (15 min)

**Goal**: Position components on Evolution Axis (Genesis 0.0 → Commodity 1.0)

**Mapping table** (chora L0-L5 → Wardley evolution):

| chora Maturity | Wardley Stage | Position (0.0-1.0) | Key Traits |
|----------------|---------------|-------------------|------------|
| **L0** (Aware) | Genesis | 0.0 - 0.125 | Novel, experimental, no implementation |
| **L1** (Planned) | Genesis → Custom | 0.125 - 0.25 | Design complete, planning stage |
| **L2** (Implemented) | Custom | 0.25 - 0.5 | Bespoke, unique, 1 adoption |
| **L3** (Validated) | Custom → Product | 0.5 - 0.625 | Standardized, 2+ adoptions |
| **L4** (Distributed) | Product → Commodity | 0.625 - 0.875 | Widespread, 5+ adoptions |
| **L5** (Sustained) | Commodity | 0.875 - 1.0 | Ubiquitous, invisible utility |

**Quick positioning heuristics**:
- **0.15**: Planned but not implemented (L1)
- **0.55**: Validated with 2-3 adoptions (L3)
- **0.80**: Distributed with 8+ adoptions, mature (L4)
- **0.95**: Ecosystem utility (Git, Docker)
- **1.0**: Universal standard (YAML, JSON, HTTP)

**Document**: Component name, evolution position, confidence (High/Medium/Low), rationale

---

## Step 3: Value Chain Analysis (30 min)

**Goal**: Position components on Value Chain Axis (User Need → Foundation)

**Four layers** (dependency depth + visibility):

1. **User Need (Layer 1)** - Visibility: 100%
   - Ultimate user goal (everything serves this)
   - Example: "Strategic Decision-Making"

2. **Visible (Layer 2)** - Visibility: 70-90%
   - User-facing outputs (direct interaction)
   - Examples: Wardley Maps, Knowledge Notes, Strategic Reports

3. **Enabling (Layer 3)** - Visibility: 40-60%
   - Infrastructure that enables visible capabilities
   - Examples: Memory System, Traceability, Metrics, Documentation

4. **Foundation (Layer 4)** - Visibility: 10-30%
   - Invisible infrastructure (user assumes it exists)
   - Examples: Git, YAML/JSON, Feature Manifest Schema, A-MEM Storage

**Quick assignment algorithm**:
1. Start with components that have **no dependencies** (Foundation)
2. Work upward: component's layer = 1 + deepest dependency's layer
3. Validate with visibility: user-facing components should be higher

**Document**: Component name, value chain layer (1-4), dependency depth, visibility %

---

## Step 4: Strategic Gameplay (20-39 min, during strategic session)

**Goal**: Apply 8 strategic principles to inform decisions

### Eight Strategic Principles (Cheat Sheet)

#### 1. Co-Evolution
**Pattern**: Capabilities that depend on each other should mature together

**When to apply**: Genesis/Custom component depends on Custom/Product bottleneck

**Example**: SAP-056 (Traceability) at 0.55 blocks Wardley Maps at 0.15 → Accelerate SAP-056 to L4 (co-evolution)

**Strategic question**: "Which capabilities are blocked by lower evolution dependencies?"

---

#### 2. Build vs Buy
**Pattern**: Genesis → build internally, Product/Commodity → buy/reuse externally

**When to apply**: Making build vs buy decisions, tool adoption choices

**Example**: Wardley Maps at 0.15 (Genesis) → BUILD (no external alternatives fit chora ontology)
Memory System at 0.80 (Commodity) → REUSE (mature internal capability, don't rebuild)

**Strategic question**: "Where is this component on evolution axis? Are external alternatives mature?"

---

#### 3. Inertia Loop Avoidance
**Pattern**: Don't over-invest in Genesis (uncertain) or Commodity (diminishing returns)

**When to apply**: Enhancement decisions, capability investment prioritization

**Example**: SAP-010 at 0.80 (Commodity) → DEFER enhancements (Inertia Loop, maintain as-is)
Wardley capability at 0.15 (Genesis) → Don't build automation before validating manual practice

**Strategic question**: "Is this Genesis (high risk, don't over-build) or Commodity (mature, don't over-enhance)?"

---

#### 4. Constraint Exploitation
**Pattern**: Leverage stable Commodity as foundation for Genesis innovation

**When to apply**: Identifying what to reuse vs rebuild, dependency planning

**Example**: Memory System (0.80 Commodity) provides stable foundation → Wardley Maps (0.15 Genesis) leverages it

**Strategic question**: "Which Commodity capabilities can we leverage as-is (without enhancement)?"

---

#### 5. Ecosystem Play
**Pattern**: Extract patterns from Commodity → distribute to ecosystem for network effects

**When to apply**: Identifying meta-SAP opportunities, pattern library creation

**Example**: Documentation (SAP-007) at 0.85 (Commodity) → Extract patterns → SAP-063 (Documentation Patterns meta-SAP)

**Strategic question**: "Which Commodity capabilities have proven patterns worth distributing?"

---

#### 6. Practice-First (Meta-Recursive)
**Pattern**: Validate manual workflow before investing in automation

**When to apply**: Automation decisions, tool build vs buy choices

**Example**: Wardley Phase 1 (manual practice) → Phase 2 (document) → Phase 3 (validate) → Phase 4 (automate selectively)

**Strategic question**: "Have we validated manual process before building automation?"

---

#### 7. Selective Automation
**Pattern**: Only automate if 30+ min manual work AND 10+ repetitions AND 20%+ error rate

**When to apply**: Deciding which pain points to automate

**Example**: Component extraction (45 min, but <10 maps/quarter) → DEFER automation
Value chain analysis (30 min, high error risk, IF 5+ maps/quarter) → STRONG automation candidate

**Strategic question**: "Does this meet 3 criteria: 30+ min, 10+ reps, 20% error?"

---

#### 8. Bottleneck Identification
**Pattern**: Lower evolution component blocks higher-level capabilities from maturing

**When to apply**: Identifying what to accelerate, removing blockers

**Example**: SAP-056 at 0.55 is critical path for Wardley at 0.15 → Accelerate SAP-056 (remove bottleneck)

**Strategic question**: "What's the lowest evolution component on the critical path?"

---

## Success Metrics (Use These to Validate Your Map)

| Metric | Target | Phase 1 Result |
|--------|--------|----------------|
| **Strategic Decisions Influenced** | 1+ per map | 6 out of 6 (100%) |
| **Decision Change Rate** | 50%+ | 4 out of 6 (67%) |
| **Strategic Principles Applied** | 3+ | 8 principles |
| **ROI** | 10x+ | 15-25x |
| **Strategic Planning Time Reduction** | 30%+ | 64% (2.2 vs 4-6 hours) |
| **Time to Map** | 60-90 min | 90 min |
| **Protocol Clarity** (L4) | 80%+ | TBD (Phase 3) |

---

## When to Automate (Phase 4, Optional)

**Selective Automation Criteria** (ALL 3 must be met):
1. **Manual time**: 30+ minutes per process
2. **Frequency**: 10+ repetitions per quarter (or 5+ if high error risk)
3. **Error rate**: 20%+ (quality/consistency issues)

**Automation Candidates** (from Phase 1 pain points):

| Process | Manual Time | Frequency | Error Risk | Priority |
|---------|------------|-----------|------------|----------|
| **Component Extraction** | 45 min | 1-2 maps/quarter | Low | DEFER (low frequency) |
| **Evolution Classification** | 15 min | 1-2 maps/quarter | Low | DEFER (clear mapping table) |
| **Value Chain Analysis** | 30 min | 1-2 maps/quarter | **High** (circular deps) | **STRONG CANDIDATE** (IF frequency increases to 5+) |
| **Gameplay Identification** | 20-39 min | 1-2 maps/quarter | Medium | DEFER (expert judgment, not algorithmic) |

**Recommended**: Wait until Phase 3 (External Validation) before automating. Track frequency over 3 months.

---

## Common Pitfalls (Avoid These)

### Pitfall 1: Too Many Components
**Problem**: Mapping 30+ components → overwhelming, unclear value chain

**Solution**: Limit to 10-15 strategic components (high-level SAPs, not code files)

---

### Pitfall 2: Skipping Strategic Session
**Problem**: Creating map but not using it for decisions → no ROI validation

**Solution**: Always prepare 6+ strategic questions, conduct session, document decision influence

---

### Pitfall 3: Premature Automation
**Problem**: Building automation before validating manual process (Inertia Loop)

**Solution**: Apply Practice-First principle (manual → document → validate → automate selectively)

---

### Pitfall 4: Ignoring Dependencies
**Problem**: Positioning components without analyzing feature.dependencies → wrong value chain layers

**Solution**: Extract dependency graph from feature-manifest.yaml, calculate dependency depth

---

### Pitfall 5: No ROI Tracking
**Problem**: Creating map but not documenting time saved, high-value work identified

**Solution**: Calculate ROI (time invested vs time saved + high-value work), document in gate-decision.md

---

## Quick Start Checklist (L0-L3 in 1-2 Sprints)

### Week 1: L0-L1 (Aware + Planned)
- [ ] Read this awareness-guide.md (30 min)
- [ ] Review Phase 1 example map (30 min)
- [ ] Identify 6+ strategic questions (30 min)
- [ ] Extract 10-15 component list (60 min)
- [ ] Create strategic-session-agenda.md (30 min)

**Total**: 3 hours

---

### Week 2: L2-L3 (Implemented + Validated)
- [ ] Component extraction (45 min)
- [ ] Evolution classification (15 min)
- [ ] Value chain analysis (30 min)
- [ ] Create map file (60-90 min)
- [ ] Conduct strategic session (60-90 min)
- [ ] Document session notes and gate decision (45 min)

**Total**: 5-6 hours

---

**Timeline**: 8-9 hours total → Achieve L3 (Validated) in 1-2 sprints

---

## Next Steps

**After reading this guide**:
1. ✅ **L0 (Aware)**: You can now explain Wardley concepts
2. ➡️ **L1 (Planned)**: Create strategic-session-agenda.md (see [adoption-blueprint.md](adoption-blueprint.md#level-1-planned-prepare-strategic-session))
3. ➡️ **L2 (Implemented)**: Create first map following [protocol-spec.md](protocol-spec.md)

**For detailed workflow**: See [protocol-spec.md](protocol-spec.md) (comprehensive manual process)

**For maturity progression**: See [adoption-blueprint.md](adoption-blueprint.md) (L0-L5 path with time estimates)

**For strategic context**: See [capability-charter.md](capability-charter.md) (problem, vision, scope)

---

## References

### Phase 1 Evidence (chora-workspace L3 Adoption)
- [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md) - Example map (15 components, 4 layers)
- [strategic-session-notes-2025-11.md](../../../docs/wardley/strategic-session-notes-2025-11.md) - 6 strategic questions, 100% decision influence
- [phase-1-gate-decision.md](../../../docs/wardley/phase-1-gate-decision.md) - Gate PASSED (0.95 confidence, 15-25x ROI)

### SAP-064 Artifacts
- [protocol-spec.md](protocol-spec.md) - Detailed manual workflow (526 lines, comprehensive)
- [adoption-blueprint.md](adoption-blueprint.md) - L0-L5 maturity path (586 lines, detailed progression)
- [capability-charter.md](capability-charter.md) - Problem, vision, scope (332 lines, strategic context)
- [ledger.md](ledger.md) - Adoption tracking (to be created)

---

**Version**: 1.0.0
**Status**: Phase 2 (SAP Creation)
**Created**: 2025-11-20
**Author**: tab-1 (Claude Code)
**Trace ID**: wardley-phase-2-2025-11
**Next**: Create ledger.md (Task 2.2, Artifact 4 - Final)
