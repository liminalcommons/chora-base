---
id: strategic-themes-{date}
type: strategic-theme-matrix
input_inventory: intention-inventory-{date}
total_intentions: 0
total_themes: 0
tags: [strategic-planning, theme-analysis, vision-synthesis]
created: YYYY-MM-DDTHH:MM:SSZ
updated: YYYY-MM-DDTHH:MM:SSZ
---

# Strategic Theme Matrix - {Date}

## Overview

**Purpose**: This matrix clusters unfulfilled intentions from the intention inventory into strategic themes, analyzes each theme's evidence quality and user demand, and recommends wave assignments for vision planning.

**Date**: {YYYY-MM-DD}

**Input**: `intention-inventory-{date}.md` ({N} intentions)

**Themes Identified**: {N}

**Recommended for Wave 1**: {N} themes

**Recommended for Wave 2**: {N} themes

**Deferred to Wave 3**: {N} themes

---

## Methodology

### Theme Clustering

**Process**:
1. Group intentions by strategic domain (e.g., strategic planning, testing, performance)
2. Identify common patterns across intentions
3. Name theme based on primary capability gap

**Theme Characteristics**:
- **Cohesive**: Intentions within theme address related problems
- **Distinct**: Themes don't overlap significantly
- **Actionable**: Theme can be addressed with concrete features/SAP enhancements

---

### Evidence Quality Scoring

For each theme, calculate evidence distribution from constituent intentions:

**Level A (Standards & Research)**: {N} intentions ({XX}%)
- IETF RFCs, W3C specs, ISO standards, PEPs
- Peer-reviewed research, production data

**Level B (Case Studies & Industry Practice)**: {N} intentions ({XX}%)
- Industry case studies (>100 users)
- Production usage in ecosystem
- Expert consensus, framework recommendations

**Level C (Expert Opinion & Blogs)**: {N} intentions ({XX}%)
- Blog posts, single expert opinions
- Single-user requests
- Anecdotal evidence

**Total A+B**: {N} intentions ({XX}%)

---

### Wave Assignment Criteria

**Wave 1 (Committed - 3 months)**:
- Evidence: A+B ≥ 70%
- User Demand: ≥ 10 explicit requests
- Effort: < 50 hours (deliverable in 3 months)
- Strategic Value: Foundational capability or high ROI (≥5x)

**Wave 2 (Exploratory - 6 months)**:
- Evidence: A+B ≥ 60% (needs validation via dogfooding)
- User Demand: ≥ 5 explicit requests
- Effort: < 100 hours
- Strategic Value: Moderate ROI (3-5x), validate before committing

**Wave 3 (Aspirational - 12 months)**:
- Evidence: A+B < 60% (insufficient evidence)
- User Demand: < 5 explicit requests
- Effort: Any
- Strategic Value: Future potential, defer until more data

**Defer** (Do not pursue):
- Evidence: A+B < 50% (very low evidence)
- User Demand: ≤ 1 request
- Strategic Value: Low ROI (<2x) or misaligned with vision

---

## Theme Analysis

### Theme 1: {Theme Name}

**Intentions**: {N} (from inventory)

**Evidence Level**:
- Level A (Standards): {N} ({XX}%)
- Level B (Case Studies): {N} ({XX}%)
- Level C (Expert Opinion): {N} ({XX}%)
- **Total A+B**: {N} ({XX}%) {✅ if ≥70%, ⚠️ if 60-70%, ❌ if <60%}

**User Demand**: {N} explicit requests from {sources}

**Related SAPs**: {SAP-XXX, SAP-YYY, SAP-ZZZ}

**Effort Estimate**: {X-Y hours} ({breakdown by SAP or feature})

**ROI Potential**: {X}x (based on {validation source - e.g., production data, case studies})

**Priority**: **HIGH** | **MEDIUM** | **LOW**

**Recommended Wave**: **Wave 1** | **Wave 2** | **Wave 3** | **Defer**

**Rationale**: {Why this wave assignment? Explain evidence quality, user demand strength, strategic value, ROI validation}

**Key Intentions** (top 3-5):
1. {Intention title} (Evidence: Level {A|B|C}, Demand: {N} requests)
2. {Intention title} (Evidence: Level {A|B|C}, Demand: {N} requests)
3. {Intention title} (Evidence: Level {A|B|C}, Demand: {N} requests)

---

### Theme 2: {Theme Name}

**Intentions**: {N}

**Evidence Level**:
- Level A: {N} ({XX}%)
- Level B: {N} ({XX}%)
- Level C: {N} ({XX}%)
- **Total A+B**: {N} ({XX}%) {Status indicator}

**User Demand**: {N} requests

**Related SAPs**: {SAP-XXX}

**Effort Estimate**: {X-Y hours}

**ROI Potential**: {X}x

**Priority**: {HIGH|MEDIUM|LOW}

**Recommended Wave**: {Wave 1|2|3|Defer}

**Rationale**: {Explanation}

**Key Intentions**:
1. {Intention}
2. {Intention}

---

### Theme 3: {Theme Name}

{...repeat structure...}

---

## Recommendation Summary

### Wave 1 Candidates (Commit to 3-month roadmap)

| Theme | Intentions | A+B % | User Demand | Effort | ROI | Rationale |
|-------|------------|-------|-------------|--------|-----|-----------|
| {Theme 1} | {N} | {XX}% ✅ | {N} requests | {X-Y}h | {X}x | {Short rationale} |
| {Theme 2} | {N} | {XX}% ✅ | {N} requests | {X-Y}h | {X}x | {Short rationale} |

**Total Intentions in Wave 1**: {N}/{total} ({XX}%)

**Total Effort**: {X-Y hours}

**Expected ROI**: {Average or combined ROI multiplier}

---

### Wave 2 Candidates (Validate via dogfooding)

| Theme | Intentions | A+B % | User Demand | Validation Plan |
|-------|------------|-------|-------------|-----------------|
| {Theme 3} | {N} | {XX}% ⚠️ | {N} requests | {What to validate - e.g., dogfood CLIs in Wave 1, measure time savings} |
| {Theme 4} | {N} | {XX}% ⚠️ | {N} requests | {Validation approach} |

**Total Intentions in Wave 2**: {N}/{total} ({XX}%)

**Validation Timeline**: {When decisions will be made - e.g., Q1 2026 after Wave 1 data}

---

### Wave 3 / Deferred

| Theme | Intentions | A+B % | User Demand | Defer Reason |
|-------|------------|-------|-------------|--------------|
| {Theme 5} | {N} | {XX}% ❌ | {N} requests | {Why defer - e.g., insufficient evidence, low demand, misaligned priority} |

**Total Intentions Deferred**: {N}/{total} ({XX}%)

**Quarterly Review**: Re-evaluate if evidence improves or demand increases

---

## Coverage Analysis

**Intentions Addressed**: {N}/{total} ({XX}%)

**Breakdown**:
- Wave 1: {N} intentions ({XX}%)
- Wave 2: {N} intentions ({XX}%)
- Wave 3: {N} intentions ({XX}%)
- Deferred: {N} intentions ({XX}%)

**Quality Check**:
- ✅ High-evidence intentions (A+B ≥70%) prioritized in Wave 1
- ✅ Medium-evidence intentions (A+B 60-70%) validated in Wave 2 before committing
- ✅ Low-evidence intentions (A+B <60%) deferred until more data
- ✅ User demand factored into priority (requests × evidence quality)

---

## Next Steps

1. **Review Theme Assignments**: Validate wave recommendations with stakeholders
2. **Create Vision Document**: Use `vision-document-template.md` to draft multi-wave vision from themes
3. **Adjust Priorities**: If needed, promote/demote themes based on strategic priorities
4. **Create Roadmap Milestone**: After Vision Wave 1 finalized, use `roadmap-milestone-template.md`
5. **Create Beads Epics**: Use SAP-015 to create epics for Wave 1 features

---

## Changelog

### {YYYY-MM-DD} - Matrix Created
- Analyzed {N} intentions from `intention-inventory-{date}.md`
- Clustered into {N} themes
- {X} themes recommended for Wave 1 (Committed)
- {Y} themes recommended for Wave 2 (Exploratory)
- {Z} themes deferred to Wave 3 or removed

### {YYYY-MM-DD} - Quarterly Review
- {Record updates to theme priorities, evidence levels, wave assignments}

---

## Example: Chora-Base Strategic Themes (Nov 2025)

**Note**: This example shows how the template is used in practice.

---
id: strategic-themes-2025-11-05
type: strategic-theme-matrix
input_inventory: intention-inventory-2025-11-05
total_intentions: 42
total_themes: 5
tags: [strategic-planning, theme-analysis, vision-synthesis]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Strategic Theme Matrix - 2025-11-05

**Input**: intention-inventory-2025-11-05 (42 intentions)

**Themes**: 5

**Wave 1 Candidates**: 2 (Strategic Planning, Testing & Quality)

---

## Theme 1: Strategic Planning Infrastructure

**Intentions**: 14 (from inventory)

**Evidence Level**:
- Level A (Standards): 5 (36%)
- Level B (Case Studies): 6 (43%)
- Level C (Expert Opinion): 3 (21%)
- **Total A+B**: 11 (79%) ✅ Exceeds 70% threshold

**User Demand**: 4 explicit inbox requests, 10 GitHub feature requests (14 total)

**Related SAPs**: SAP-006, SAP-010, SAP-015, SAP-027

**Effort Estimate**: 22-34 hours (4 SAP enhancements)

**ROI Potential**: 10x (based on reducing vision synthesis time from 40 hours → 4 hours)

**Priority**: **HIGH**

**Recommended Wave**: **Wave 1** (Committed for v1.5.0)

**Rationale**:
- Very high evidence quality (79% A+B) from PM best practices and production validation
- Strong user demand (14 explicit requests across inbox and GitHub)
- Foundational capability enabling strategic planning across ecosystem
- Validated ROI (10x time savings based on manual vision synthesis measurements)
- No blockers, can start immediately

**Key Intentions**:
1. Strategic planning workflow (Evidence: Level A, Demand: 4 inbox + 10 GitHub)
2. Vision synthesis process (Evidence: Level B, Demand: 4 requests)
3. Intention discovery automation (Evidence: Level B, Demand: 3 requests)
4. Multi-wave planning (Evidence: Level A - PM standard, Demand: 4 requests)
5. Backlog cascade patterns (Evidence: Level B, Demand: 8 requests)

---

## Theme 2: Testing & Quality Improvements

**Intentions**: 8

**Evidence Level**:
- Level A: 2 (25%)
- Level B: 4 (50%)
- Level C: 2 (25%)
- **Total A+B**: 6 (75%) ✅ Exceeds 70% threshold

**User Demand**: 8 developers requesting (GitHub issues)

**Related SAPs**: SAP-004 (Testing Framework), SAP-014 (MCP Server Development)

**Effort**: 12-20 hours

**ROI Potential**: 5x (based on reducing test writing time)

**Priority**: **HIGH**

**Recommended Wave**: **Wave 1** (Committed for v1.5.0)

**Rationale**:
- High evidence quality (75% A+B) from testing standards and production usage
- Strong user demand (8 developers across ecosystem)
- Aligns with SAP-004 L2 maturity goals (test coverage target: 85%)
- Direct productivity improvement (5x faster test authoring)

**Key Intentions**:
1. MCP server testing patterns (Evidence: Level B, Demand: 8 devs)
2. Tool invocation mocking (Evidence: Level A - testing standard, Demand: 5 devs)
3. Integration test automation (Evidence: Level B, Demand: 3 devs)

---

## Theme 3: MCP Integration & Tooling

**Intentions**: 6

**Evidence Level**:
- Level A: 1 (17%)
- Level B: 4 (67%)
- Level C: 1 (17%)
- **Total A+B**: 5 (83%) ✅ Exceeds 70% threshold

**User Demand**: 8 developers requesting (MCP ecosystem)

**Related SAPs**: SAP-014, SAP-017, SAP-018

**Effort**: 10-15 hours

**ROI Potential**: 8x (based on reducing MCP development time)

**Priority**: **MEDIUM**

**Recommended Wave**: **Wave 2** (Exploratory, validate via dogfooding)

**Rationale**:
- Very high evidence quality (83% A+B) BUT narrow audience (MCP developers only)
- Strong demand within niche (8 devs in MCP ecosystem)
- Recommend dogfooding pilot before ecosystem commitment
- Validate ROI claim (8x) with real usage data before promoting to Wave 1

**Validation Plan**:
- Dogfood MCP testing patterns in chora-compose during Wave 1
- Measure actual time savings vs 8x claim
- Survey 8 requesting developers after pilot
- Decision review: Q1 2026

**Key Intentions**:
1. MCP server testing patterns (Evidence: Level B, Demand: 8)
2. FastMCP integration (Evidence: Level B, Demand: 6)

---

## Theme 4: Performance Optimization

**Intentions**: 5

**Evidence Level**:
- Level A: 1 (20%)
- Level B: 2 (40%)
- Level C: 2 (40%)
- **Total A+B**: 3 (60%) ⚠️ Below 70% threshold, at Wave 2 minimum

**User Demand**: 3 users requesting

**Related SAPs**: SAP-025, SAP-032

**Effort**: 15-25 hours

**ROI Potential**: 3x (based on improving Core Web Vitals)

**Priority**: **MEDIUM**

**Recommended Wave**: **Wave 2** (Exploratory, needs more evidence)

**Rationale**:
- Evidence just meets Wave 2 threshold (60% A+B), needs validation
- Moderate user demand (3 users)
- ROI unclear (3x based on assumptions, not production data)
- Recommend gathering more production performance data before committing

**Validation Plan**:
- Instrument performance metrics in current applications
- Collect baseline Core Web Vitals data
- Validate 3x ROI claim with real measurements
- Decision review: Q2 2026 after 3 months data collection

---

## Theme 5: Documentation Quality

**Intentions**: 4

**Evidence Level**:
- Level A: 1 (25%)
- Level B: 1 (25%)
- Level C: 2 (50%)
- **Total A+B**: 2 (50%) ❌ Below 60% threshold

**User Demand**: 2 users requesting

**Related SAPs**: SAP-007, SAP-016

**Effort**: 8-12 hours

**ROI Potential**: 2x (based on reducing documentation errors)

**Priority**: **LOW**

**Recommended Wave**: **Wave 3** (Aspirational, defer until more demand)

**Rationale**:
- Low evidence quality (50% A+B, below Wave 2 minimum)
- Low user demand (2 users)
- Low ROI (2x, incremental improvement rather than capability gap)
- Defer until evidence improves or demand increases

**Path to Wave 2**:
- User demand increases to 5+ requests
- Production data shows documentation issues causing significant support burden
- Evidence quality improves to 60%+ A+B

---

## Recommendation Summary

### Wave 1 (Commit to v1.5.0)
- **Theme 1: Strategic Planning** (14 intentions, 79% A+B, 14 requests, 10x ROI)
- **Theme 2: Testing & Quality** (8 intentions, 75% A+B, 8 requests, 5x ROI)

**Total**: 22/42 intentions (52%) addressed in Wave 1

### Wave 2 (Validate via dogfooding)
- **Theme 3: MCP Integration** (6 intentions, 83% A+B, 8 requests) - Validate 8x ROI claim
- **Theme 4: Performance** (5 intentions, 60% A+B, 3 requests) - Gather production data

**Total**: 11/42 intentions (26%) in Wave 2 validation

### Wave 3 / Deferred
- **Theme 5: Documentation** (4 intentions, 50% A+B, 2 requests) - Insufficient evidence and demand

**Total**: 9/42 intentions (21%) deferred

---

## Usage Instructions

### How to Use This Template

1. **Copy Template** (after creating intention inventory):
   ```bash
   cp .chora/memory/templates/strategic-theme-matrix-template.md \
      .chora/memory/knowledge/notes/strategic-themes-$(date +%Y-%m-%d).md
   ```

2. **Fill Frontmatter**:
   - `id`: strategic-themes-{date}
   - `input_inventory`: Reference to intention inventory used
   - `total_intentions`: Total from inventory
   - `total_themes`: Number of themes identified
   - Set timestamps

3. **Cluster Intentions into Themes**:
   - Read intention inventory
   - Group related intentions (strategic domain, capability gap, SAP alignment)
   - Name each theme clearly (describes the capability or domain)

4. **For Each Theme**:
   - Count intentions in theme
   - Calculate evidence distribution (A%, B%, C%)
   - Calculate Total A+B percentage
   - Count user demand (explicit requests)
   - List related SAPs
   - Estimate effort
   - Estimate ROI potential (with validation source)
   - Assign priority (HIGH/MEDIUM/LOW)
   - Recommend wave (1/2/3/Defer) based on criteria
   - Write rationale (explain wave assignment)
   - List top 3-5 key intentions

5. **Create Recommendation Summary**:
   - Table of Wave 1 candidates
   - Table of Wave 2 candidates with validation plans
   - Table of Wave 3/deferred themes with defer reasons

6. **Calculate Coverage**:
   - How many intentions addressed? (Wave 1 + Wave 2 + Wave 3)
   - What percentage in each wave?
   - Quality check: High-evidence → Wave 1, Medium → Wave 2, Low → defer

7. **Next Step**: Create vision document using `vision-document-template.md`

### Integration with Other Templates

**Inputs**:
- `intention-inventory-{date}.md` - Source of intentions to cluster

**Outputs**:
- `vision-{project}-{horizon}.md` - Vision with wave assignments based on themes

### Wave Assignment Decision Tree

```
For each theme:
├─ Is A+B ≥ 70%?
│  ├─ YES → Is user demand ≥ 10?
│  │  ├─ YES → Wave 1 (Committed)
│  │  └─ NO → Wave 2 (Exploratory, moderate demand)
│  └─ NO → Is A+B ≥ 60%?
│     ├─ YES → Is user demand ≥ 5?
│     │  ├─ YES → Wave 2 (Exploratory, needs validation)
│     │  └─ NO → Wave 3 (Aspirational, defer)
│     └─ NO → Defer (insufficient evidence)
```

### When to Update Matrix

**Quarterly Review**: Re-evaluate themes based on new evidence, demand changes, or strategic priority shifts

**After Dogfooding**: Update Wave 2 themes with validation results, promote to Wave 1 or defer to Wave 3

**After Vision Synthesis**: No updates needed (matrix is input to vision, not modified by it)
