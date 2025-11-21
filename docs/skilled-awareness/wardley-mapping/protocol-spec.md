# Wardley Mapping Protocol Specification (Manual Workflow)

**Version**: 1.0.0 (Phase 1 Validated)
**Status**: Proven Manual Process (Phase 2 Documentation)
**Created**: 2025-11-20
**Trace ID**: wardley-phase-1-2025-11
**Source**: Phase 1 Manual Practice (chora-workspace, 2025-11-20)

---

## Overview

This protocol documents the **proven manual workflow** for creating Wardley maps from chora ecosystem features. This workflow was validated in Phase 1 and achieved:

- **100% strategic decision influence** (6 out of 6 decisions influenced)
- **67% decision change rate** (4 decisions reversed based on map insights)
- **15-25x ROI** (2.2 hours invested → 4-9 days saved + 2-3 days high-value work identified)
- **64% strategic planning time reduction** (2.2 hours vs 4-6 hour baseline)

**Purpose**: Systematize the manual process for Phase 2 (SAP-064 adoption) and Phase 3 (external validation) before any Phase 4 automation.

**Scope**: Component extraction → Evolution classification → Value chain positioning → Strategic gameplay identification

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Component Extraction                                │
│ Input: feature-manifest.yaml                                │
│ Output: 10-15 strategic components                          │
│ Time: 45 minutes (manual)                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Evolution Classification                           │
│ Input: Components + chora maturity levels (L0-L5)          │
│ Output: Evolution positioning (0.0-1.0)                    │
│ Time: 15 minutes (manual)                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Value Chain Analysis                               │
│ Input: Components + feature.dependencies                   │
│ Output: Value chain layers (User Need → Foundation)        │
│ Time: 30 minutes (manual)                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Strategic Gameplay Identification                  │
│ Input: Positioned map                                      │
│ Output: Strategic principles applied (8 gameplay patterns) │
│ Time: 20 minutes (during strategic session)                │
└─────────────────────────────────────────────────────────────┘

Total Time: ~90 minutes (component extraction → map creation)
            +39 minutes (strategic session application)
            = 2.2 hours end-to-end
```

---

## Step 1: Component Extraction

### Objective

Extract 10-15 **strategically relevant** components from `feature-manifest.yaml` that represent the complete value chain from User Need to Foundation.

### Input

- `feature-manifest.yaml` (workspace root)
- Strategic context: What decision(s) does this map need to inform?

### Method

**1.1: Identify Strategic Decision Context**

Before extracting components, clarify:
- What strategic question(s) will this map help answer?
- What time horizon? (Sprint planning, quarterly roadmap, annual strategy)
- What scope? (Single SAP, ecosystem-wide, cross-repo dependencies)

**Example from Phase 1**:
- Strategic questions: SAP-056 acceleration? Wardley build vs defer? Memory system investment?
- Time horizon: Quarterly roadmap (Q4 2025)
- Scope: chora-workspace ecosystem (15 components)

**1.2: Extract High-Level Components**

Read `feature-manifest.yaml` and identify components that are:
- ✅ **Strategic capabilities** (SAPs, major features, infrastructure)
- ✅ **Cross-cutting concerns** (affects multiple features)
- ✅ **Differentiation points** (unique to chora vs commodity)
- ❌ **NOT low-level code files** (src/module/file.py)
- ❌ **NOT implementation details** (specific functions, classes)

**Manual Process** (45 minutes):
```bash
# 1. List all features (quick scan)
grep -E "^  - id: FEAT-" feature-manifest.yaml | head -50

# 2. Identify SAPs (strategic capabilities)
grep -A 3 "^  - id: FEAT-SAP-" feature-manifest.yaml

# 3. Check feature names and statuses
grep -A 5 "name:" feature-manifest.yaml | grep -A 2 "status:"

# 4. Extract dependencies (for value chain analysis in Step 3)
grep -A 10 "dependencies:" feature-manifest.yaml
```

**Selection Criteria**:
- **User Need layer** (top): 1 component representing the ultimate user goal
- **Visible layer**: 2-4 components users directly interact with
- **Enabling layer**: 4-7 components that enable visible capabilities
- **Foundation layer**: 3-5 components that underpin everything

**Target**: 10-15 components total (Phase 1 used 15 components)

**Output**: List of component names, feature IDs, statuses, maturity levels

**Example from Phase 1**:
```markdown
| Component | Feature ID | Status | Maturity | Strategic Rationale |
|-----------|-----------|--------|----------|-------------------|
| Strategic Decision-Making | User Need | N/A | N/A | Ultimate user goal |
| Wardley Maps | FEAT-WARDLEY-001 | planned | L0-L1 | Visible capability (Genesis) |
| Memory System (SAP-010) | FEAT-SAP-010-L4 | implemented | L4 | Enabling capability (Product/Commodity) |
| Traceability (SAP-056) | FEAT-SAP-056 | implemented | L3 | Enabling capability (Custom → Product) |
| Git Version Control | (external) | mature | Commodity | Foundation (Commodity) |
```

### Pain Points (Phase 4 Automation Candidates)

- **Manual search**: 45 minutes reading feature-manifest.yaml (tedious grepping)
- **No automated importance ranking**: Had to judge strategic relevance manually (subjective)
- **Dependency extraction tedious**: feature.dependencies exists but not extracted systematically

**Automation Candidate**: `scripts/wardley-component-extractor.py`
- Parse feature-manifest.yaml
- Rank components by strategic importance (dependencies, status, tags)
- Output top N components with metadata
- **Criteria**: 30+ min manual AND 10+ repetitions AND 20%+ error rate
- **Current Assessment**: Moderate pain (45 min), but only 1-2 maps per quarter expected (low repetition) → DEFER unless Phase 2-3 validates higher frequency

---

## Step 2: Evolution Classification

### Objective

Position each component on the **Evolution Axis** (horizontal: Genesis 0.0 → Commodity 1.0) based on chora maturity levels (L0-L5).

### Input

- Components from Step 1
- chora maturity levels (L0-L5) from feature-manifest.yaml

### Method

**2.1: Apply L0-L5 → Wardley Evolution Mapping Table**

Use this validated mapping (from Phase 1 learnings):

| chora Maturity | Wardley Stage | Position (0.0-1.0) | Characteristics | Examples |
|----------------|---------------|-------------------|-----------------|----------|
| **L0 (Aware)** | Genesis | 0.0 - 0.125 | Novel, uncertain, experimental, no implementation | Strategic Reports (0.10) |
| **L1 (Planned)** | Genesis → Custom | 0.125 - 0.25 | Understood, planning stage, design complete | Wardley Maps (0.15) |
| **L2 (Implemented)** | Custom | 0.25 - 0.5 | Bespoke, unique implementation, 1 adoption | (None in Phase 1) |
| **L3 (Validated)** | Custom → Product | 0.5 - 0.625 | Standardized, 2+ adoptions, productizing | Traceability (0.55), Metrics (0.60), Feature Manifest (0.50) |
| **L4 (Distributed)** | Product → Commodity | 0.625 - 0.875 | Widespread, productized, 5+ adoptions | Memory (0.80), Self-Eval (0.70), A-MEM (0.70), Knowledge Notes (0.75), Automation (0.75), Docs (0.85) |
| **L5 (Sustained)** | Commodity | 0.875 - 1.0 | Ubiquitous, invisible infrastructure, utility-like | SAP Frontmatter (0.90), Git (0.95), YAML/JSON (1.0) |

**2.2: Handle Ambiguous Cases with Confidence Scores**

For components in transition (e.g., L3 → L4, L4 → L5), use these heuristics:

**Within L3 (Custom → Product, 0.5 - 0.625)**:
- **0.50**: Just validated (2 adoptions, recent)
- **0.55**: Validated + productizing (3 adoptions, stabilizing API)
- **0.60**: Strong product (4+ adoptions, mature API)

**Within L4 (Product → Commodity, 0.625 - 0.875)**:
- **0.65-0.70**: Early product (5-7 adoptions, still evolving)
- **0.75-0.80**: Mature product (8+ adoptions, stable)
- **0.85**: Commoditizing (10+ adoptions, invisible infrastructure)

**Within L5 (Commodity, 0.875 - 1.0)**:
- **0.90**: Internal commodity (chora-workspace standard)
- **0.95**: Ecosystem commodity (Git, Docker)
- **1.0**: Universal commodity (YAML, JSON, HTTP)

**2.3: Document Positioning Rationale**

For each component, record:
- Maturity level (L0-L5)
- Evolution stage (Genesis/Custom/Product/Commodity)
- Position (0.0-1.0)
- Confidence score (High/Medium/Low)
- Rationale (why this position?)

**Example from Phase 1**:
```markdown
| Component | Maturity | Evolution | Position | Confidence | Rationale |
|-----------|----------|-----------|----------|------------|-----------|
| Wardley Maps | L1 | Genesis → Custom | 0.15 | High | Planned, design complete, no implementation yet |
| Traceability (SAP-056) | L3 | Custom → Product | 0.55 | Medium | 3 adoptions, stabilizing API, productizing |
| Memory System (SAP-010) | L4 | Product → Commodity | 0.80 | High | 8+ adoptions, stable, commoditizing |
| Git Version Control | Commodity | Commodity | 0.95 | High | Ecosystem-wide utility, invisible infrastructure |
```

### Output

- Evolution positioning for all components (0.0-1.0)
- Confidence scores and rationale documented

### Pain Points (Phase 4 Automation Candidates)

- **Ambiguity for L3 components**: Custom → Product transition (0.50 vs 0.55 vs 0.60 is judgment call)
- **No confidence scores**: Manual assessment, no algorithmic support
- **Manual time**: 15 minutes (but clear mapping table reduces pain)

**Automation Candidate**: `scripts/wardley-evolution-classifier.py`
- Read SAP maturity, adoption counts, API stability indicators
- Return evolution position with confidence score
- **Current Assessment**: Low pain (15 min, clear mapping table exists) → DEFER automation

---

## Step 3: Value Chain Analysis

### Objective

Position each component on the **Value Chain Axis** (vertical: User Need → Foundation) based on dependency depth and strategic visibility.

### Input

- Components from Step 1
- Evolution positioning from Step 2
- `feature.dependencies` from feature-manifest.yaml

### Method

**3.1: Extract Dependency Graph**

For each component, identify dependencies:
- **Direct dependencies**: Components this one depends on (from feature.dependencies)
- **Reverse dependencies**: Components that depend on this one (derived)

**Manual Process** (10 minutes):
```bash
# Extract dependencies for each feature
grep -A 20 "^  - id: FEAT-SAP-056" feature-manifest.yaml | grep -A 10 "dependencies:"
grep -A 20 "^  - id: FEAT-WARDLEY-001" feature-manifest.yaml | grep -A 10 "dependencies:"
```

**Example dependency structure**:
```
Wardley Maps → Memory System (extracts activity patterns)
Wardley Maps → Traceability (extracts value chain edges)
Wardley Maps → Metrics Tracking (evolution classification data)
Memory System → A-MEM Event Storage (storage infrastructure)
Traceability → Feature Manifest Schema (schema definition)
```

**3.2: Calculate Dependency Depth (Topological Sort)**

**Value chain layers** are determined by **dependency depth** (how many hops from foundation):

**Layer Assignment Algorithm**:
1. **Foundation (Layer 4)**: Components with **no dependencies** (or only external dependencies)
   - Examples: YAML/JSON (1.0), Git (0.95), SAP Frontmatter (0.90)

2. **Enabling (Layer 3)**: Components that depend **only on Foundation**
   - Examples: Memory System → A-MEM Storage, Traceability → Feature Manifest Schema

3. **Visible (Layer 2)**: Components that depend on **Enabling or Foundation**
   - Examples: Wardley Maps → Memory + Traceability, Knowledge Notes → Memory

4. **User Need (Layer 1)**: The ultimate goal, depends on **Visible components**
   - Example: Strategic Decision-Making → Wardley Maps + Strategic Reports + Knowledge Notes

**Manual Process** (20 minutes):
- Start from components with no dependencies (Foundation)
- Work upward, assigning each component to the layer one above its deepest dependency
- Detect circular dependencies (if A → B and B → A, both are same layer)

**3.3: Validate with Strategic Importance**

**Heuristic**: Components that are **user-facing** should be higher in value chain, even if dependency depth suggests otherwise.

**Visibility heuristic**:
- **User Need (100% visible)**: User interacts directly with this component's outputs
- **Visible (70-90% visible)**: User sees results, but may not interact directly
- **Enabling (40-60% visible)**: User benefits indirectly (infrastructure that enables visible capabilities)
- **Foundation (10-30% visible)**: Invisible infrastructure (user assumes it exists)

**Example adjustments**:
- Wardley Maps: Dependency depth suggests Layer 3 (Enabling), but **user-facing** → move to Layer 2 (Visible)
- Documentation (SAP-007): Dependency depth suggests Layer 3, but **visible to user** → keep Layer 3 (Enabling) because docs are generated infrastructure, not direct user interaction

**3.4: Document Value Chain Positioning**

For each component, record:
- Value chain layer (1-4)
- Dependency depth (number of hops from foundation)
- Visibility percentage (10-100%)
- Direct dependencies (list)

**Example from Phase 1**:
```markdown
### Layer 1: User Need (Visibility: 100%)
- **Strategic Decision-Making** - Ultimate user goal, all other components serve this

### Layer 2: Visible Components (Visibility: 70-90%)
- **Wardley Maps** (0.15) - User-facing visual strategic positioning (depends on: Memory, Traceability, Metrics)
- **Strategic Analysis Reports** (0.10) - User-facing gameplay recommendations (depends on: Wardley Maps)
- **Knowledge Notes** (0.75) - User-facing documented patterns (depends on: Memory System)

### Layer 3: Enabling Capabilities (Visibility: 40-60%)
- **Memory System (SAP-010)** (0.80) - Extract strategic insights (depends on: A-MEM Event Storage)
- **Traceability (SAP-056)** (0.55) - Bidirectional feature linkage (depends on: Feature Manifest Schema)
- **Metrics Tracking (SAP-013)** (0.60) - SAP maturity levels (depends on: SAP Frontmatter)
- **Self-Evaluation (SAP-019)** (0.70) - Strategic SAP positioning (depends on: Metrics)
- **Automation Scripts (SAP-008)** (0.75) - Justfile recipes (depends on: YAML/JSON)
- **Documentation (SAP-007)** (0.85) - MkDocs site generation (depends on: SAP Frontmatter)

### Layer 4: Foundation (Visibility: 10-30%)
- **Feature Manifest Schema** (0.50) - YAML schema (depends on: YAML/JSON)
- **A-MEM Event Storage** (0.70) - JSONL event logs (depends on: YAML/JSON)
- **SAP Frontmatter** (0.90) - YAML metadata standard (depends on: YAML/JSON)
- **Git Version Control** (0.95) - Version control infrastructure (external)
- **YAML/JSON Formats** (1.0) - Data interchange formats (external)
```

### Output

- Value chain layer assignments (1-4) for all components
- Dependency graph documented
- Visibility percentages recorded

### Pain Points (Phase 4 Automation Candidates)

- **Dependency depth calculation manual**: Counted hops in dependency graph by hand (tedious, error-prone)
- **Circular dependencies not detected**: Would cause positioning errors if present
- **No topological sort automation**: Had to trace by hand (30 min manual work)

**Automation Candidate**: `scripts/wardley-value-chain-analyzer.py`
- Topological sort of feature.dependencies
- Detect circular dependencies (error detection)
- Output layer assignments with dependency depth metrics
- **Criteria**: 30+ min AND high error risk (circular deps) AND 10+ repetitions
- **Current Assessment**: Moderate pain (30 min), **high error risk** (complex dependency graphs) → **STRONG candidate** IF Phase 2-3 validates frequency (5+ maps per quarter)

---

## Step 4: Strategic Gameplay Identification

### Objective

Identify which **strategic principles** apply to the positioned map, enabling evidence-based strategic decisions.

### Input

- Completed Wardley map (components positioned on evolution + value chain axes)
- Strategic questions to answer (from strategic session)

### Method

**4.1: Eight Core Strategic Principles**

These 8 principles were validated in Phase 1 (100% decision influence):

#### Principle 1: Co-Evolution

**Pattern**: Components that depend on each other should mature together.

**Detection**:
- Component A (lower evolution) is **critical dependency** for Component B (higher evolution)
- Component B's maturation **blocked** by Component A's immaturity

**Example from Phase 1**:
- **SAP-056 (Traceability)** at 0.55 (Custom → Product)
- **Wardley Maps** at 0.15 (Genesis) **depends on** SAP-056 for value chain extraction
- **Strategic Decision**: Accelerate SAP-056 to L4 (0.60-0.65) BEFORE starting Wardley Phase 2
- **Rationale**: Better traceability → better value chain extraction → better maps (co-evolution)

**Application**: Look for Genesis/Custom components that depend on Custom/Product bottlenecks.

---

#### Principle 2: Build vs Buy

**Pattern**: Genesis → build internally, Product/Commodity → buy/reuse externally.

**Detection**:
- Component at **Genesis (0.0-0.25)**: No external alternatives exist → **BUILD**
- Component at **Product (0.5-0.75)**: External alternatives maturing → **BUY** if suitable
- Component at **Commodity (0.75-1.0)**: Ubiquitous externally → **REUSE** (don't build)

**Example from Phase 1**:
- **Wardley Maps** (0.15, Genesis): No external alternatives fit chora's ontology integration → **BUILD**
- **Memory System** (0.80, Product/Commodity): Internal capability mature → **REUSE** (don't rebuild)
- **Git** (0.95, Commodity): Ecosystem-wide utility → **REUSE** (never build)

**Application**: Check evolution positioning to determine build vs buy vs reuse strategy.

---

#### Principle 3: Inertia Loop Avoidance

**Pattern**: Don't over-invest in Genesis (uncertain) or Commodity (diminishing returns).

**Detection**:
- **Genesis (0.0-0.25) over-investment**: Building automation infrastructure before validating manual practice
- **Commodity (0.75-1.0) over-investment**: Enhancing mature capabilities that are already "good enough"

**Example from Phase 1**:
- **Q2 (Wardley Build vs Defer)**: Don't build automation (Commodity) before validating manual (Genesis)
- **Q3 (Memory System)**: SAP-010 at 0.80 (Commodity) → **STOP investing**, maintain as-is (defer enhancements)
- **Q4 (Documentation)**: SAP-007 at 0.85 (Commodity) → **STOP enhancing**, maintain stability (defer advanced plugins)

**Application**: Look for Genesis components with premature automation plans, or Commodity components with active enhancement roadmaps.

---

#### Principle 4: Constraint Exploitation

**Pattern**: Leverage stable Commodity capabilities as foundation for Genesis innovation.

**Detection**:
- Commodity components (0.75-1.0) with **high stability** and **low change rate**
- Genesis components (0.0-0.25) that **can build on** Commodity foundation

**Example from Phase 1**:
- **Memory System (SAP-010)** at 0.80 (Commodity) provides stable foundation
- **Wardley Maps** (0.15, Genesis) leverages Memory for activity pattern extraction
- **Strategic Decision**: Don't enhance SAP-010 (constraint), leverage as-is for Wardley

**Application**: Identify Commodity components that enable Genesis innovation without needing enhancement.

---

#### Principle 5: Ecosystem Play

**Pattern**: Extract patterns from Commodity capabilities → distribute to ecosystem for network effects.

**Detection**:
- Commodity components (0.75-1.0) with **reusable patterns**
- Opportunity to create **meta-SAP** or **pattern library** from Commodity learnings

**Example from Phase 1**:
- **Documentation (SAP-007)** at 0.85 (Commodity) has mature patterns (MkDocs + Diátaxis)
- **Strategic Decision**: Extract documentation patterns → create **SAP-063: Documentation Patterns** meta-SAP
- **Ecosystem Play**: Distribute SAP-063 to chora-base adopters (network effects, not chora-workspace exclusive)

**Application**: Look for Commodity components with high adoption and proven patterns that could be formalized.

---

#### Principle 6: Practice-First (Meta-Recursive)

**Pattern**: Validate manual workflow before investing in automation (mirrors own Genesis → Commodity evolution).

**Detection**:
- Genesis components (0.0-0.25) with **automation plans** before manual validation
- Opportunity to apply **practice-first** to own capability development

**Example from Phase 1**:
- **Wardley capability itself**: Phase 1 (manual practice) → Phase 2 (document) → Phase 3 (validate) → Phase 4 (automate selectively)
- **Q5 (Schema Extension)**: Wait for manual Wardley validation before extending schema (practice-first, defer extension)
- **Q6 (Automation Timing)**: Wait for 10+ map repetitions before automating component extraction (practice-first)

**Application**: Check if Genesis components have premature automation plans (apply practice-first).

---

#### Principle 7: Selective Automation

**Pattern**: Only automate if 30+ min manual work AND 10+ repetitions expected AND 20%+ error rate.

**Detection**:
- Manual processes taking **30+ minutes**
- Expected frequency **10+ times per quarter** (or 5+ if high error risk)
- Error rate **20%+** (quality/consistency issues)

**Example from Phase 1**:
- **Component Extraction**: 45 min manual, but only 1-2 maps per quarter expected → DEFER
- **Value Chain Analyzer**: 30 min manual, **high error risk** (circular deps), IF 5+ maps per quarter → **STRONG candidate**

**Application**: Document pain points during manual practice, evaluate against 3 criteria before automating.

---

#### Principle 8: Bottleneck Identification

**Pattern**: Lower evolution component blocks higher-level capabilities from maturing.

**Detection**:
- Component A (lower evolution) is **critical path** for Component B (higher evolution)
- Component B's adoption **limited** by Component A's maturity

**Example from Phase 1**:
- **SAP-056 (Traceability)** at 0.55 blocks **Wardley Maps** at 0.15
- **Strategic Decision**: Accelerate SAP-056 to L4 to unblock Wardley adoption (remove bottleneck)

**Application**: Trace dependency paths from Genesis to Commodity, identify lowest evolution on critical path.

---

**4.2: Apply Principles to Strategic Questions**

For each strategic question, check which principles apply:

**Example from Phase 1 (Q1: SAP-056 Acceleration)**:
- **Without map**: "Maintain SAP-056 at L3 (no urgent need)" (Medium confidence)
- **With map**: "Accelerate SAP-056 to L4 (bottleneck removal + co-evolution)" (High confidence)
- **Principles applied**: Co-Evolution (#1), Bottleneck Identification (#8)
- **Map reference**: SAP-056 at 0.55 blocks Wardley at 0.15
- **Decision changed**: ✅ YES (B → A)

**4.3: Document Strategic Insights**

For each principle applied, record:
- Which principle (1-8)
- Which component(s) triggered the principle
- What strategic decision changed as a result
- Confidence improvement (Medium → High)

### Output

- Strategic principles applied (list of 1-8)
- Strategic decisions influenced (which questions changed)
- Confidence scores (before/after map analysis)

### Time Investment

- **Manual process**: 20-39 minutes during strategic session
- **Gameplay identification**: Not automated (requires expert judgment)

### Pain Points (Phase 4 Automation Candidates)

- **Codifying gameplay logic**: 8 principles are heuristics, not algorithms (subjective expert judgment)
- **Automation complexity**: High (pattern matching, dependency analysis, strategic context understanding)

**Automation Candidate**: None for now
- **Current Assessment**: Gameplay identification is **expert judgment** (keep manual)
- **Fallback**: Document heuristics in protocol-spec.md (this file), don't attempt algorithmic implementation

---

## Success Metrics (Phase 1 Validation)

### Strategic Value Metrics

| Metric | Phase 1 Result | Target (Phase 2-3) | Validation Method |
|--------|---------------|-------------------|------------------|
| **Strategic Decisions Influenced** | 6 out of 6 (100%) | 1+ per map | Document decisions referenced in sprint plans, roadmaps |
| **Decision Change Rate** | 4 out of 6 (67%) | 50%+ | Track decisions reversed vs same-but-higher-confidence |
| **Strategic Principles Applied** | 8 principles | 3+ per map | Count principles documented in strategic session notes |
| **ROI** | 15-25x | 10x+ | Time invested vs (time saved + high-value work identified) |
| **Strategic Planning Time Reduction** | 64% (2.2 vs 4-6 hours) | 30%+ | Compare session time to baseline (text-only analysis) |

### Process Quality Metrics

| Metric | Phase 1 Result | Target (Phase 2-3) | Validation Method |
|--------|---------------|-------------------|------------------|
| **Time to Map** | 90 min (extraction → positioning) | 60-90 min | Track time for component extraction + evolution + value chain |
| **Component Count** | 15 components | 10-15 | Validate coverage (all value chain layers represented) |
| **Protocol Clarity** | N/A (Phase 2) | 80%+ | External adopter survey (can you create map following protocol?) |
| **Pain Point Frequency** | 1 map in Phase 1 | 10+ maps per quarter | Track map creation frequency over 3 months |

### Automation Threshold Metrics (Phase 4)

| Process | Manual Time | Frequency (Phase 1) | Error Risk | Automation Priority |
|---------|------------|-------------------|------------|-------------------|
| **Component Extraction** | 45 min | 1 map (low) | Low | DEFER (low frequency) |
| **Evolution Classification** | 15 min | 1 map (low) | Low | DEFER (clear mapping table exists) |
| **Value Chain Analysis** | 30 min | 1 map (low) | **High** (circular deps) | **STRONG CANDIDATE** (if frequency increases to 5+ maps/quarter) |
| **Gameplay Identification** | 20-39 min | 1 map (low) | Medium | DEFER (expert judgment, not algorithmic) |

**Selective Automation Criteria**: 30+ min AND 10+ reps AND 20%+ error rate
- **Component Extraction**: ❌ (45 min, but <10 reps expected)
- **Evolution Classification**: ❌ (15 min, low pain)
- **Value Chain Analysis**: ⚠️ **MAYBE** (30 min, high error risk, IF frequency reaches 5+ maps/quarter)
- **Gameplay Identification**: ❌ (not algorithmic, keep manual)

---

## Phase 2-3 Adoption Path

### Phase 2: SAP-064 Creation (Current)

**Goal**: Document proven manual process as SAP-064 artifacts

**Deliverables**:
1. ✅ **protocol-spec.md** (this file) - Manual workflow documentation
2. ⏳ **capability-charter.md** - Problem, vision, scope
3. ⏳ **adoption-blueprint.md** - L0 → L5 maturity path
4. ⏳ **awareness-guide.md** - Quick reference for manual workflow
5. ⏳ **ledger.md** - Track pilot adoption in chora-workspace

**Timeline**: 4-6 days (Sprint 14-15)

### Phase 3: External Adoption Validation

**Goal**: Validate protocol clarity with 2-3 additional maps

**Method**:
1. Create 2-3 additional maps following protocol-spec.md
2. Track time, pain points, protocol clarity (target: 80%+ "I could follow the protocol")
3. Refine SAP-064 v1.1.0 based on pain points

**Success Criteria**:
- External adopter survey: 80%+ can create map following protocol
- Time to map: 60-90 min (within target range)
- Strategic decisions influenced: 1+ per map

**Timeline**: 2-3 days

### Phase 4: Selective Automation (Optional)

**Goal**: Automate validated pain points ONLY if criteria met

**Candidates**:
1. **Value Chain Analyzer** (STRONG candidate):
   - IF frequency reaches 5+ maps per quarter
   - AND high error risk (circular dependency detection)
   - THEN automate topological sort + layer assignment

2. **Component Extractor** (DEFER):
   - ONLY IF frequency reaches 10+ maps per quarter
   - AND manual extraction error rate > 20%

3. **Evolution Classifier** (DEFER):
   - Low pain (15 min, clear mapping table)
   - Keep manual unless error rate > 20%

**Timeline**: 3-5 days (only if Phase 3 validates frequency)

---

## Validation Checklist (Use Before Calling Map "Complete")

Before presenting a Wardley map for strategic decision-making, validate:

**Component Extraction**:
- [ ] 10-15 components identified (not too few, not too many)
- [ ] All value chain layers represented (User Need → Foundation)
- [ ] High-level strategic components (not low-level code files)
- [ ] Feature IDs and maturity levels documented

**Evolution Classification**:
- [ ] All components positioned on evolution axis (0.0-1.0)
- [ ] L0-L5 → Wardley mapping applied consistently
- [ ] Confidence scores documented for ambiguous cases
- [ ] Rationale provided for each positioning

**Value Chain Analysis**:
- [ ] All components positioned on value chain axis (User Need → Foundation)
- [ ] Dependency graph extracted from feature.dependencies
- [ ] Dependency depth calculated (topological sort)
- [ ] No circular dependencies (or documented if present)
- [ ] Visibility percentages assigned (10-100%)

**Strategic Gameplay**:
- [ ] Strategic questions prepared (what decisions will this map inform?)
- [ ] At least 3 strategic principles identified (out of 8)
- [ ] Map positioning referenced in decision rationale
- [ ] Confidence scores improved vs baseline (Medium → High)

**Documentation**:
- [ ] Map representation created (text, visual, or both)
- [ ] Strategic session notes documented (questions, answers, decisions)
- [ ] Pain points logged (for Phase 4 automation consideration)
- [ ] Time metrics tracked (component extraction, positioning, session time)

---

## References

### Phase 1 Artifacts (Validation Evidence)

- [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md) - First manual map (15 components, 4 layers)
- [strategic-session-notes-2025-11.md](../../../docs/wardley/strategic-session-notes-2025-11.md) - 6 strategic questions, 8 principles applied
- [phase-1-gate-decision.md](../../../docs/wardley/phase-1-gate-decision.md) - Gate PASSED (0.95 confidence)

### Evolution Classification Reference

- [.chora/memory/knowledge/notes/2025-11-21-wardley-ontology-evolution-tracking.md](../../../.chora/memory/knowledge/notes/2025-11-21-wardley-ontology-evolution-tracking.md) - Insight #1 (L0-L5 → Genesis/Commodity mapping)

### Strategic Roadmap

- [project-docs/plans/wardley-capability-roadmap-2025-11.md](../../../project-docs/plans/wardley-capability-roadmap-2025-11.md) - Phase 1-4 detailed roadmap

---

**Version**: 1.0.0
**Status**: Phase 1 Validated, Phase 2 Documentation
**Created**: 2025-11-20
**Author**: tab-1 (Claude Code)
**Trace ID**: wardley-phase-1-2025-11
**Next**: Create SAP-064 capability-charter.md (Task 2.2)
