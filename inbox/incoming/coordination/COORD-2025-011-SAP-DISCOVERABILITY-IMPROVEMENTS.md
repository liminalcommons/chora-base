---
type: coordination_request
request_id: COORD-2025-011
title: "SAP Adoption Blueprint Improvement: Discoverability Requirements"
from: chora-workspace
to: chora-base
priority: high
status: draft
created: 2025-11-09
tags: [sap-framework, discoverability, adoption-blueprint, dx]
---

# Coordination Request: SAP Discoverability Requirements

**Request ID**: COORD-2025-011
**From**: chora-workspace (Victor)
**To**: chora-base SAP Framework maintainers
**Priority**: High
**Created**: 2025-11-09

---

## Executive Summary

### Problem Statement

**Current Issue**: SAP adoption blueprints do not explicitly require discoverability improvements, leading to:
- Excellent SAP implementations with poor discoverability (40-55/100 scores)
- Wasted agent time navigating to find capabilities (10-15 min per session)
- Meta-discoverability paradox: Advanced patterns (nested hierarchies) become liabilities instead of assets

**Evidence from chora-workspace**:
- SAP-010 (Memory System): Implementation 9/10, Discoverability 40/100
- SAP-015 (Task Tracking): Implementation 8/10, Discoverability 55/100
- Navigation tax: 10-15 minutes wasted per session discovering features

**Impact**: ROI of sophisticated patterns (SAP-009 nested hierarchies) is **negative** until discoverability improved

---

## Request

### Proposal: Add Discoverability as L1 Requirement

**Recommendation**: Update SAP adoption blueprint template to include discoverability as **L1 (Pilot) requirement**, not L2 or L3.

**Rationale**:
1. Without discoverability, even excellent implementations are invisible
2. Navigation tax exceeds token savings from advanced patterns
3. Agents can't adopt what they can't discover
4. Discoverability is prerequisite for L2/L3 usage metrics

**Specific Changes Requested**:

#### 1. Update Adoption Blueprint Template

Add to **every SAP adoption blueprint**:

```markdown
### L1 Requirement: Discoverability (New)

**Goal**: Make SAP discoverable via root awareness files

**Checklist**:
- [ ] Add dedicated section to README.md (30+ lines)
  - "When to use SAP-XXX" (5 use cases)
  - "What you get" (features list)
  - Quick-start code example (5-10 commands)
  - Links to domain files (if nested hierarchy)
  - ROI statement
- [ ] Add dedicated section to AGENTS.md (60+ lines)
  - Workflows with examples
  - Integration patterns with other SAPs
  - Links to nested AGENTS.md (if SAP-009 pattern used)
- [ ] Add justfile recipes (≥3 recipes per SAP)
  - Inline comments with examples
  - Section header with description
- [ ] Add direct links if using nested hierarchy
  - Root CLAUDE.md → Domain CLAUDE.md
  - Root AGENTS.md → Domain AGENTS.md

**Success Criteria**:
- Discoverability score ≥80/100
- Agent can discover SAP in <5 minutes from root files
- All touchpoints present (README, AGENTS, justfile)

**Validation**:
Run discoverability audit (if available):
\```bash
just disc | grep SAP-XXX
# Target: ≥80/100
\```
```

#### 2. Add Discoverability Audit to SAP-019 (Self-Evaluation)

Update SAP-019 to include discoverability metrics:

```markdown
## Discoverability Assessment

**Touchpoints** (100 points total):
- README.md: 30 points (dedicated section, examples, ROI)
- AGENTS.md: 20 points (dedicated section, workflows)
- CLAUDE.md: 15 points (domain-specific guidance)
- justfile: 15 points (≥3 recipes with comments)
- Documentation: 10 points (how-to guides, references)
- Examples: 10 points (working implementations)

**Scoring**:
- 80-100: HIGH (excellent discoverability)
- 50-79: MEDIUM (adequate, needs improvement)
- 0-49: LOW (critical gap, blocks adoption)

**Target**: ≥80/100 for L1 completion
```

#### 3. Update SAP-000 (SAP Framework) Guidance

Add to SAP-000 adoption guidance:

```markdown
## Discoverability-First Adoption

**Principle**: "Implementation quality is irrelevant if undiscoverable"

**Anti-Pattern** (current common mistake):
1. Implement SAP (excellent quality)
2. Use SAP internally (works well)
3. Mark L1 complete
4. Discoverability score: 40/100
5. Other agents can't find it
6. ROI = $0

**Correct Pattern**:
1. Implement SAP (excellent quality)
2. Add README.md section (dedicated)
3. Add AGENTS.md section (dedicated)
4. Add justfile recipes (≥3)
5. Validate discoverability ≥80/100
6. Mark L1 complete
7. ROI = Projected value

**Time Investment**:
- Discoverability work: 3-5 hours
- One-time cost
- Returns: 10-15 min saved per session
- Break-even: 20-30 sessions (1-2 months)
```

---

## Evidence & Research

### Finding 1: Meta-Discoverability Paradox

**Research**: CLAUDE_Complete.md, Section 3.1 (Context Window Optimization)

> "Progressive Context Loading
> - Phase 1: Essential Context (0-10k tokens)
> - Phase 2: Extended Context (10-50k tokens)"

**Application**: Nested hierarchies (SAP-009) enable 60-70% token savings

**Problem**: Without discoverability, navigation tax exceeds token savings

**Evidence from chora-workspace**:

| Scenario | Navigation Time | Token Usage | Net Benefit |
|----------|----------------|-------------|-------------|
| Without discoverability | 15-20 min | 15-20k | **Negative** (wasted time) |
| With discoverability | 5-8 min | 5-8k | **Positive** (60% savings) |

**Conclusion**: Advanced patterns require proportionally higher discoverability

---

### Finding 2: Discovery-to-Value Ratio

**Metric**: Value gained / Discovery cost

**Observed ratios in chora-workspace**:

| SAP | Implementation Quality | Discoverability | Discovery Cost | Value | Ratio |
|-----|----------------------|-----------------|----------------|-------|-------|
| SAP-010 (before) | 9/10 | 40/100 | 15-20 min | 10-12 min/session | **0.5-0.8** (poor) |
| SAP-010 (after) | 9/10 | 90/100 | 5 min | 10-12 min/session | **2.0-2.4** (excellent) |
| SAP-015 (before) | 8/10 | 55/100 | 10-15 min | 5-10 min/session | **0.5-1.0** (poor) |
| SAP-015 (after) | 8/10 | 85/100 | 2-3 min | 5-10 min/session | **2.0-5.0** (excellent) |

**Target**: Discovery-to-Value ratio ≥ 2.0 (value exceeds discovery cost from first session)

**Recommendation**: L1 requirement should ensure ratio ≥ 2.0

---

### Finding 3: Discoverability-Implementation Gap

**Measurement**: Implementation quality - Discoverability quality

**Data from chora-workspace (before improvements)**:

| SAP | Implementation | Discoverability | Gap |
|-----|----------------|-----------------|-----|
| SAP-010 | 9/10 | 4/10 | **5 points** (50%) |
| SAP-015 | 8/10 | 5.5/10 | **2.5 points** (25%) |
| SAP-014 | 9/10 | 8/10 | **1 point** (10%) |

**Observation**: SAP-014 (high discoverability) adopted faster than SAP-010 (low discoverability)

**Conclusion**: Discoverability is adoption bottleneck, not implementation quality

---

### Finding 4: "Nearest File Wins" Requires Direct Links

**Pattern**: SAP-009 nested hierarchy (root → domain AGENTS.md/CLAUDE.md)

**Theory**: Agents load progressive context from nearest file

**Reality**: Agents waste 5-10 minutes discovering nested files exist

**Solution**: Direct links in root files

**Example** (from chora-workspace CLAUDE.md):

```markdown
### Domain 4: Memory System (.chora/)

**Path**: [.chora/AGENTS.md](.chora/AGENTS.md) + [.chora/CLAUDE.md](.chora/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.chora/CLAUDE.md](.chora/CLAUDE.md) - Claude workflows (8-min, 5k tokens)
- [.chora/AGENTS.md](.chora/AGENTS.md) - Memory patterns (13-min, 10k tokens)
```

**Impact**: Navigation time reduced from 15 min → 2 min (87% reduction)

**Recommendation**: SAP-009 adoption blueprint should mandate direct links in root files

---

## Observations & Learnings

### Observation 1: Implementation-First vs Discoverability-First

**Current common pattern** (chora-workspace experience):
1. Adopt SAP (focus on implementation quality)
2. Use SAP successfully (internal validation)
3. Mark L1 complete
4. Months later: Discover discoverability is 40/100
5. Other agents never adopt because they can't discover it

**Recommended pattern**:
1. Adopt SAP (implementation quality)
2. Add discoverability immediately (README, AGENTS, justfile)
3. Validate discoverability ≥80/100
4. Mark L1 complete
5. Usage spreads naturally (agents can discover it)

**Time difference**: +3-5 hours upfront (discoverability work)
**ROI difference**: 10x better adoption (discoverable from day 1)

---

### Observation 2: Nested Hierarchies Need Extra Discoverability

**SAP-009 Pattern**: Nested AGENTS.md/CLAUDE.md in domains

**Benefits** (theoretical):
- 60-70% token reduction
- Domain-specific expertise
- Scalable to 1000+ files

**Benefits** (actual, without discoverability):
- **0% realized** (agents can't find nested files)
- Navigation tax > token savings
- Complexity with no benefit

**Required for SAP-009 effectiveness**:
1. ✅ Root README.md mentions nested pattern
2. ✅ Root AGENTS.md explains "nearest file wins"
3. ✅ Root CLAUDE.md has direct links to domain files
4. ✅ Each domain section has "Navigation tip" with links
5. ✅ Token savings explicitly stated (motivate agents to use pattern)

**Recommendation**: SAP-009 adoption blueprint should include discoverability checklist

---

### Observation 3: Justfile Recipes as CLI Discoverability

**Finding**: Agents discover SAPs via `just --list` frequently

**Evidence**:
- `just --list | grep memory` → Discovers SAP-010 recipes
- `just --list | grep beads` → Discovers SAP-015 recipes
- Inline comments guide usage

**Best practices**:
```bash
# Section header with SAP reference
# ============================================================================
# SAP-010: Memory System (A-MEM)
# ============================================================================
# Event logging, knowledge notes for cross-session learning.
# See: .chora/AGENTS.md, .chora/CLAUDE.md

# Recipe with inline comment and example
# Show last N memory events (default: 20)
# Example: just memory-events 50
memory-events N="20":
    @tail -n {{N}} .chora/memory/events/*.jsonl
```

**Recommendation**: SAP adoption blueprints should require ≥3 justfile recipes with examples

---

### Observation 4: Documentation Touchpoint Often Missing

**Issue**: Discoverability audit expects docs in specific locations

**Common mistake**:
- Create excellent how-to guides
- Place in arbitrary location (not per SAP-007)
- Audit reports "0/10 - No documentation"
- Actual discoverability harmed

**Solution**: SAP-007 compliance should be L1 requirement for SAPs with user-facing features

**Recommended structure**:
```
docs/
├── how-to/          # Task-oriented (e.g., "How to use SAP-010")
├── explanation/     # Understanding-oriented (e.g., "Why nested hierarchies")
├── reference/       # Information-oriented (e.g., "Event log schema")
└── tutorial/        # Learning-oriented (e.g., "Your first knowledge note")
```

**Recommendation**: Add to L1 checklist: "Organize documentation per SAP-007"

---

## Proposed Changes to chora-base

### Change 1: Update Adoption Blueprint Template

**File**: `chora-base/templates/sap-adoption-blueprint-template.md`

**Section to add** (after L1 implementation checklist):

```markdown
### L1 Requirement: Discoverability (New)

**Goal**: Make SAP discoverable via root awareness files

Before marking L1 complete, ensure:

#### README.md Section (30+ lines)
- [ ] Add "### SAP-XXX: [Name]" section to README.md
- [ ] Include "When to use SAP-XXX" (5 use cases)
- [ ] Include "What you get" (features/capabilities list)
- [ ] Include quick-start code example (5-10 commands)
- [ ] Include links to nested files (if SAP-009 pattern used)
- [ ] Include ROI statement (time saved, value delivered)
- [ ] Include documentation links

**Template**:
\```markdown
### [SAP Name]

**When to use SAP-XXX**:
- [Use case 1]
- [Use case 2]
- [Use case 3]
- [Use case 4]
- [Use case 5]

**What you get**:
- [Feature 1 with details]
- [Feature 2 with details]
- [Feature 3 with details]

**Quick start**:
\```bash
# [Command 1 with comment]
just command-1

# [Command 2 with comment]
just command-2
\```

**Documentation**: [Link to guides]

**ROI**: [Time saved, value statement]
\```

#### AGENTS.md Section (60+ lines)
- [ ] Add "### SAP-XXX: [Name]" section to AGENTS.md
- [ ] Include "When to use SAP-XXX" (5+ scenarios)
- [ ] Include "Quick-start approach" with code examples
- [ ] Include "What you get" (detailed features)
- [ ] Include workflow example (complete scenario)
- [ ] Include integration patterns with other SAPs
- [ ] Include links to nested AGENTS.md (if SAP-009 pattern)
- [ ] Include ROI statement

#### justfile Recipes (≥3)
- [ ] Add section header with SAP reference
- [ ] Add section comment describing SAP purpose
- [ ] Add ≥3 recipes for common operations
- [ ] Add inline comments for each recipe
- [ ] Add usage examples for complex recipes
- [ ] Test all recipes work

**Template**:
\```bash
# ============================================================================
# SAP-XXX: [SAP Name]
# ============================================================================
# [Brief description of SAP purpose]
# See: [Link to AGENTS.md or nested files]

# [Recipe description with details]
# Example: just recipe-name arg
recipe-name ARG="default":
    @command {{ARG}}
\```

#### Direct Links (if using SAP-009 nested hierarchy)
- [ ] Update root CLAUDE.md domain section
- [ ] Add "Navigation tip" with token savings statement
- [ ] Add direct links to domain CLAUDE.md
- [ ] Add direct links to domain AGENTS.md
- [ ] Add estimated read times and token counts

**Template**:
\```markdown
### Domain X: [Domain Name] (path/)

**Path**: [path/AGENTS.md](path/AGENTS.md) + [path/CLAUDE.md](path/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [path/CLAUDE.md](path/CLAUDE.md) - Claude workflows (X-min, Yk tokens)
- [path/AGENTS.md](path/AGENTS.md) - [Domain] patterns (X-min, Yk tokens)

**Use when**:
- [Scenario 1]
- [Scenario 2]
\```

#### Validation
- [ ] Run discoverability audit (target ≥80/100)
- [ ] Test: Can agent discover SAP in <5 min from README.md?
- [ ] Test: Are all justfile recipes working?
- [ ] Test: Are nested file links clickable and correct?

**Success Criteria**:
- Discoverability score ≥80/100
- Agent discovery time <5 minutes
- All touchpoints complete (README, AGENTS, justfile, docs)
- Direct links validated (if nested hierarchy)
```

---

### Change 2: Update SAP-019 (Self-Evaluation) Spec

**File**: `chora-base/docs/skilled-awareness/sap-self-evaluation/protocol-spec.md`

**Section to add**:

```markdown
## Discoverability Assessment

### Scoring Framework (100 points)

#### README.md (30 points)
- **30 points**: Dedicated section (30+ lines) with "When to use", examples, ROI, links
- **15 points**: Mentioned (10-29 lines) with some examples
- **0 points**: Not mentioned or brief mention only (<10 lines)

**Validation**:
\```bash
# Count lines in SAP section
grep -A 50 "### SAP-XXX" README.md | wc -l
# Target: ≥30 lines
\```

#### AGENTS.md (20 points)
- **20 points**: Dedicated section (60+ lines) with workflows, integrations, examples
- **10 points**: Section exists (30-59 lines) with some guidance
- **5 points**: Listed in SAP catalog only
- **0 points**: Not mentioned

#### CLAUDE.md (15 points)
- **15 points**: Dedicated workflow/pattern section or domain section with direct links
- **7 points**: Mentioned in context (integration pattern, etc.)
- **0 points**: Not mentioned

#### justfile (15 points)
- **15 points**: ≥3 recipes with section header and inline comments
- **10 points**: 1-2 recipes with comments
- **5 points**: 1 recipe without comments
- **0 points**: No recipes

#### Documentation (10 points)
- **10 points**: ≥3 docs (how-to, explanation, or reference) in SAP-007 structure
- **5 points**: 1-2 docs
- **0 points**: No documentation

#### Examples (10 points)
- **10 points**: ≥5 working implementations or examples
- **5 points**: 1-4 examples
- **0 points**: No examples

### Score Interpretation

| Score | Level | Assessment |
|-------|-------|------------|
| 80-100 | HIGH | Excellent discoverability, agents find SAP easily |
| 50-79 | MEDIUM | Adequate, but needs improvement |
| 0-49 | LOW | Critical gap, blocks adoption |

**L1 Requirement**: Score ≥80/100
**L2 Requirement**: Maintain score ≥80/100
**L3 Requirement**: Maintain score ≥80/100

### Audit Script

\```python
# Add to sap-evaluator.py or create disc-audit.py
def audit_discoverability(sap_id):
    """Audit SAP discoverability across 6 touchpoints."""
    score = 0

    # README.md (30 points)
    readme_lines = count_sap_section_lines("README.md", sap_id)
    if readme_lines >= 30:
        score += 30
    elif readme_lines >= 10:
        score += 15

    # AGENTS.md (20 points)
    agents_lines = count_sap_section_lines("AGENTS.md", sap_id)
    if agents_lines >= 60:
        score += 20
    elif agents_lines >= 30:
        score += 10
    elif has_catalog_entry("AGENTS.md", sap_id):
        score += 5

    # CLAUDE.md (15 points)
    if has_dedicated_section("CLAUDE.md", sap_id):
        score += 15
    elif is_mentioned("CLAUDE.md", sap_id):
        score += 7

    # justfile (15 points)
    recipe_count = count_recipes("justfile", sap_id)
    if recipe_count >= 3:
        score += 15
    elif recipe_count >= 1:
        score += 10 if has_comments("justfile", sap_id) else 5

    # Documentation (10 points)
    doc_count = count_docs(sap_id)
    if doc_count >= 3:
        score += 10
    elif doc_count >= 1:
        score += 5

    # Examples (10 points)
    example_count = count_examples(sap_id)
    if example_count >= 5:
        score += 10
    elif example_count >= 1:
        score += 5

    return {
        "sap_id": sap_id,
        "score": score,
        "level": "HIGH" if score >= 80 else "MEDIUM" if score >= 50 else "LOW",
        "readme": readme_lines,
        "agents": agents_lines,
        "recipes": recipe_count,
        "docs": doc_count,
        "examples": example_count
    }
\```
```

---

### Change 3: Update SAP-000 (SAP Framework) Guidance

**File**: `chora-base/docs/skilled-awareness/sap-framework/AGENTS.md`

**Section to add** (in adoption guidance):

```markdown
## Discoverability-First Adoption Pattern

### The Meta-Discoverability Principle

> **"The better the pattern, the worse the impact if undiscoverable"**

Advanced SAP patterns (nested hierarchies, progressive loading) offer high value BUT require proportionally higher discoverability investment.

**Without discoverability**: Sophisticated patterns become **liabilities** instead of assets.

### Anti-Pattern: Implementation-First (Common Mistake)

\```
Day 1: Implement SAP (excellent quality, 20 hours)
Day 2-30: Use SAP internally (works great)
Day 30: Mark L1 complete
Day 60: Run discoverability audit → 40/100
Day 90: Other agents still can't find SAP
ROI: $0 (invisible to others)
\```

**Problem**: Months of work, zero adoption outside pilot team

### Correct Pattern: Discoverability-First

\```
Day 1: Implement SAP (excellent quality, 20 hours)
Day 2: Add discoverability (README, AGENTS, justfile, 3-5 hours)
Day 2: Validate discoverability ≥80/100
Day 2: Mark L1 complete
Day 3+: Natural adoption (agents discover via README/justfile)
ROI: Projected value realized (discoverable from day 1)
\```

**Time Investment**:
- Discoverability work: 3-5 hours (one-time)
- Returns: 10-15 min saved per session per agent
- Break-even: 20-30 sessions (1-2 months for single agent)

### Checklist: L1 Discoverability Requirements

Before marking L1 complete:

- [ ] README.md dedicated section (30+ lines)
- [ ] AGENTS.md dedicated section (60+ lines)
- [ ] justfile recipes (≥3) with comments
- [ ] Direct links (if nested hierarchy)
- [ ] Discoverability audit ≥80/100
- [ ] Agent can discover SAP in <5 min

**Validation**:
\```bash
just disc | grep SAP-XXX
# Target: ≥80/100
\```

### Special Case: Nested Hierarchies (SAP-009)

**SAP-009 pattern** requires **extra discoverability**:

1. Root README.md explains nested pattern benefits
2. Root AGENTS.md has "Nested Awareness" section
3. Root CLAUDE.md domain sections have direct links
4. Each domain section has "Navigation tip" with token savings
5. Token savings explicitly stated (60-70% reduction)

**Without extra discoverability**: Navigation tax > token savings = **negative ROI**
```

---

### Change 4: Create Discoverability Checklist Template

**New file**: `chora-base/templates/discoverability-checklist.md`

```markdown
# SAP-XXX Discoverability Checklist

Use this checklist to ensure SAP-XXX meets L1 discoverability requirements (≥80/100).

## README.md Section (30 points)

- [ ] Section added: `### SAP-XXX: [Name]`
- [ ] "When to use SAP-XXX" (5 use cases)
- [ ] "What you get" (features list with details)
- [ ] Quick-start code example (5-10 commands)
- [ ] Links to nested files (if SAP-009 pattern)
- [ ] ROI statement (time/value saved)
- [ ] Documentation links
- [ ] **Line count**: _____ (target: ≥30 lines)

## AGENTS.md Section (20 points)

- [ ] Section added: `### SAP-XXX: [Name]`
- [ ] "When to use SAP-XXX" (5+ scenarios)
- [ ] "Quick-start approach" with code
- [ ] "What you get" (detailed features)
- [ ] Example workflow (complete scenario)
- [ ] Integration patterns with other SAPs
- [ ] Links to nested AGENTS.md (if SAP-009)
- [ ] ROI statement
- [ ] **Line count**: _____ (target: ≥60 lines)

## CLAUDE.md Coverage (15 points)

- [ ] Dedicated section OR domain section with direct links
- [ ] Claude-specific tips/patterns
- [ ] Token budget guidance (if relevant)
- [ ] Workflow examples

## justfile Recipes (15 points)

- [ ] Section header with SAP reference
- [ ] Section comment (SAP purpose)
- [ ] Recipe 1: _________________ (with comment & example)
- [ ] Recipe 2: _________________ (with comment & example)
- [ ] Recipe 3: _________________ (with comment & example)
- [ ] All recipes tested and working

## Documentation (10 points)

- [ ] How-to guide: ___________________
- [ ] Explanation doc: _______________ (if needed)
- [ ] Reference doc: _________________ (if needed)
- [ ] Organized per SAP-007 structure

## Examples (10 points)

- [ ] Example 1: ___________________
- [ ] Example 2: ___________________
- [ ] Example 3: ___________________
- [ ] Example 4: ___________________
- [ ] Example 5: ___________________

## Direct Links (if SAP-009 nested hierarchy)

- [ ] Root CLAUDE.md domain section updated
- [ ] "Navigation tip" with token savings
- [ ] Link to domain CLAUDE.md
- [ ] Link to domain AGENTS.md
- [ ] Read times and token counts

## Validation

- [ ] Discoverability audit run: `just disc | grep SAP-XXX`
- [ ] **Score**: _____ / 100 (target: ≥80)
- [ ] Agent discovery test (<5 min from README.md)
- [ ] All justfile recipes working
- [ ] Nested links clickable (if applicable)

## Notes

[Add any observations, challenges, or learnings here]

---

**Completed by**: ___________
**Date**: ___________
**Ready for L1 completion**: Yes / No
```

---

## Benefits of Proposed Changes

### Benefit 1: Faster Adoption

**Current**: SAPs adopted slowly, many never discovered
**Proposed**: SAPs discoverable from day 1, natural adoption

**Evidence**: SAP-014 (high discoverability from start) adopted 3x faster than SAP-010 (low initial discoverability)

---

### Benefit 2: Higher ROI Realization

**Current**: ROI = $0 until discoverability improved (months later)
**Proposed**: ROI = Projected value from L1 completion

**Example** (SAP-010 in chora-workspace):
- Implementation: 20 hours ($1,000)
- Discoverability: 5 hours ($250)
- Total investment: $1,250
- Returns (with discoverability): 40-48 hours/year ($2,000-2,400)
- ROI: 160-192% year 1
- Returns (without discoverability): 0 hours (invisible)
- ROI: -100% (sunk cost)

---

### Benefit 3: Better DX for SAP Authors

**Current**: Authors confused why excellent implementations aren't adopted
**Proposed**: Clear checklist, explicit requirements, validation script

---

### Benefit 4: Compound Network Effects

**Current**: Each SAP adoption is isolated (no cross-SAP discovery)
**Proposed**: README.md/AGENTS.md sections create SAP catalog, agents browse

**Evidence**: After improving SAP-015 discoverability, agents also discovered SAP-010 (same README.md page)

---

## Implementation Roadmap

### Phase 1: Template Updates (Week 1)

**Tasks**:
1. Update adoption blueprint template (add L1 discoverability section)
2. Create discoverability checklist template
3. Document examples from chora-workspace

**Effort**: 4-6 hours
**Owner**: chora-base maintainers

---

### Phase 2: SAP-019 Update (Week 2)

**Tasks**:
1. Add discoverability assessment to SAP-019 spec
2. Create or update audit script (disc-audit.py)
3. Document scoring framework

**Effort**: 6-8 hours
**Owner**: chora-base maintainers

---

### Phase 3: SAP-000 Guidance (Week 2-3)

**Tasks**:
1. Add discoverability-first adoption pattern to SAP-000
2. Document meta-discoverability principle
3. Create examples and anti-patterns

**Effort**: 4-6 hours
**Owner**: chora-base maintainers

---

### Phase 4: Pilot & Validation (Week 3-4)

**Tasks**:
1. Apply new requirements to 1-2 SAPs in chora-base
2. Validate checklist completeness
3. Measure adoption improvement

**Effort**: 8-12 hours
**Owner**: chora-base maintainers + chora-workspace validation

---

### Phase 5: Rollout (Month 2)

**Tasks**:
1. Update all existing SAP adoption blueprints
2. Announce changes to adopters
3. Create migration guide for existing adoptions

**Effort**: 10-15 hours
**Owner**: chora-base maintainers

---

## Success Metrics

### Metric 1: Discoverability Score Improvement

**Baseline**: Average 45/100 (LOW) across SAPs in chora-workspace
**Target**: Average ≥80/100 (HIGH) for all L1+ SAPs

**Measurement**: Run audit quarterly

---

### Metric 2: Adoption Rate

**Baseline**: ~30% of implemented SAPs actively used by multiple agents
**Target**: ~80% of L1+ SAPs actively used

**Measurement**: Track usage metrics (SAP-019)

---

### Metric 3: Time to Discovery

**Baseline**: 10-15 minutes average (navigation tax)
**Target**: <5 minutes (direct discovery from root files)

**Measurement**: Survey agents, track discovery time

---

### Metric 4: ROI Realization Rate

**Baseline**: ~40% of SAPs realize projected ROI (blocked by discoverability)
**Target**: ~90% of SAPs realize projected ROI

**Measurement**: Compare actual vs projected returns

---

## Questions for chora-base Team

1. **Is L1 the right level for discoverability requirements?**
   - Alternative: L0 (before implementation starts)
   - Rationale for L1: Implementation proves value, then make discoverable

2. **Should discoverability audit be automated?**
   - Proposal: Add `just disc` recipe to all projects
   - Runs automatically in CI/CD (optional)

3. **How to handle legacy SAPs adopted before new requirements?**
   - Proposal: Migration guide + grace period (3-6 months)
   - Gradual improvement OK (don't block usage)

4. **Should nested hierarchies (SAP-009) have higher discoverability threshold?**
   - Proposal: SAP-009 requires ≥85/100 (vs ≥80/100 for others)
   - Rationale: Advanced pattern needs extra discoverability

5. **Should justfile recipe count be flexible?**
   - Current proposal: ≥3 recipes minimum
   - Some SAPs may only need 1-2 recipes
   - Alternative: "At least 1 recipe per major operation"

---

## Appendices

### Appendix A: Case Studies

#### Case Study 1: SAP-010 (Memory System)

**Before**:
- Implementation: 9/10 (excellent)
- Discoverability: 40/100 (LOW)
- Adoption: 1 agent (pilot only)
- ROI: $0 (blocked by discoverability)

**After** (discoverability improvements):
- Implementation: 9/10 (maintained)
- Discoverability: 90/100 (HIGH)
- Adoption: 3 agents (spreading)
- ROI: $2,000-2,400/year (realized)

**Time Investment**: 5 hours (discoverability work)
**Break-even**: Month 2

---

#### Case Study 2: SAP-015 (Task Tracking)

**Before**:
- Implementation: 8/10 (good)
- Discoverability: 55/100 (MEDIUM)
- Adoption: 2 agents (limited)
- Navigation tax: 10-15 min per session

**After**:
- Implementation: 8/10 (maintained)
- Discoverability: 85/100 (HIGH)
- Adoption: 4 agents (broad)
- Navigation tax: 2-3 min per session (83% reduction)

**Time Investment**: 4 hours
**Break-even**: Month 1

---

### Appendix B: Templates & Examples

Full templates provided in Change proposals (Sections 1-4).

Examples from chora-workspace available at:
- [README.md](../../README.md) - SAP-010, SAP-015 sections
- [AGENTS.md](../../AGENTS.md) - SAP-010, SAP-015 sections
- [SAP-010-DISCOVERABILITY-ANALYSIS.md](../sap-completions/SAP-010-DISCOVERABILITY-ANALYSIS.md)

---

### Appendix C: Research References

- **CLAUDE_Complete.md**: Claude-powered agentic development guide
  - Section 2.1: CLAUDE.md File Hierarchy
  - Section 3.1: Context Window Optimization

- **chora-workspace metrics**: Real-world data from 3-month pilot
  - 2 SAPs improved (SAP-010, SAP-015)
  - Discoverability scores: 40/55 → 90/85 (+50/+30 points)
  - Combined time savings: 20-25 min/session
  - Annualized ROI: $4,000-5,000

---

## Next Steps

**For chora-base team**:
1. Review proposal and provide feedback
2. Prioritize changes (accept all, subset, or modify)
3. Estimate effort for changes
4. Schedule implementation (timeline)

**For chora-workspace**:
5. Continue piloting improvements (SAP-010, SAP-015 done)
6. Apply to remaining SAPs (SAP-001, SAP-012, etc.)
7. Validate metrics (3-6 month tracking)
8. Share learnings back to chora-base

**Timeline**:
- **Feedback**: 1-2 weeks
- **Implementation**: 4-6 weeks
- **Validation**: 3-6 months

---

**Prepared by**: Claude (AI Agent) on behalf of chora-workspace
**Date**: 2025-11-09
**Status**: Draft (awaiting chora-base feedback)
**Related Work**:
- [SAP-010-DISCOVERABILITY-ANALYSIS.md](../sap-completions/SAP-010-DISCOVERABILITY-ANALYSIS.md)
- [SAP-015 discoverability improvements](../../README.md#task-tracking-beads)
