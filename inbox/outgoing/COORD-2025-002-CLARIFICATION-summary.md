# Clarifying Questions Before Pilot (COORD-2025-002-CLARIFICATION)

**From**: chora-base team
**To**: chora-compose team
**Date**: 2025-10-29
**Type**: Follow-up clarification (not new request)
**Timing**: Before Pilot Week 1 (~2025-11-06)

---

## TL;DR

After sending our pilot acceptance, we realized we may have **under-communicated** some architectural details about our full collections vision. This clarification ensures we're aligned before decomposition begins.

**5 Questions** (answers helpful before Week 1, but not blocking):
1. Caching & freshness ("latest" vs "fresh" modes)
2. Content block architecture (template slots vs modular vs semantic)
3. Context schema (what dimensions supported?)
4. Hybrid model (storage + generation mix)
5. Content block storage location

**Not asking for**: Changes to pilot plan, new features, or urgent responses

---

## Context

**Pilot Status**: ✅ Approved (COORD-2025-002-RESPONSE sent 2025-10-29)
**Pilot Start**: ~2025-11-06 (Week 1: Decomposition phase)
**Why Now**: Decomposition requires clarity on content architecture and caching

### What We Communicated Well ✅
- Collections as role-based SAP bundles
- Context-aware generation (same SAP, different contexts → customized artifacts)
- Content blocks + context → artifacts model
- Pilot plan and timeline

### What We Under-Communicated ⚠️
- **"Latest" vs "fresh"** semantics (mentioned in 1 line, not explained)
- **Hybrid model** as intentional choice (not just fallback)
- **Constituent content** architecture options
- **Content block storage** location
- **Full collections vision** (multi-tier composition, role-based holons)

---

## Question 1: Caching & Freshness Semantics ⭐ CRITICAL

**Question**: Does chora-compose support both "use cached artifact" and "always regenerate fresh" modes?

### Our Vision

**"Latest" Mode**: Use cached/stored artifact if available
- **When**: Production deployments, stable versions, performance priority
- **Benefit**: Fast (no regeneration), consistent (tested versions)
- **Trade-off**: May be stale if content blocks updated

**"Fresh" Mode**: Always regenerate from content blocks
- **When**: Development, customization needs, context changes
- **Benefit**: Up-to-date (latest content blocks), context-specific (customized)
- **Trade-off**: Slower (generation overhead)

**User Choice**:
```bash
generate_collection('minimal-entry', freshness='latest')  # Use cached
generate_collection('minimal-entry', freshness='fresh')   # Regenerate
```

**System-Determined** (alternative):
- Auto-detect when regeneration needed:
  - Content block modified since last generation
  - Context changed significantly
  - Cache TTL expired

### Why This Matters

This affects:
- How we structure content blocks
- How repos consume collections
- Performance vs. freshness trade-offs
- Caching infrastructure needs

### Sub-Questions

1. How does caching work in chora-compose?
2. Can users explicitly request fresh generation vs cached?
3. What triggers cache invalidation? (content updates, context changes, TTL?)
4. Where are cached artifacts stored? (filesystem, database, in-memory?)
5. How is cache versioning handled?

---

## Question 2: Content Block Architecture ⭐ CRITICAL

**Question**: Which model does chora-compose use for constituent content blocks?

### Three Models

#### Option A: Template Slots
**Description**: Fixed structure with variable content slots

**Example**:
```jinja2
# Charter template
## Problem Statement
{{ problem_statement }}

## Solution Approach
{{ solution_approach }}
```

**Pros**: Simple, predictable, easy to validate
**Cons**: Less flexible, requires explicit template design

---

#### Option B: Modular Blocks
**Description**: Library of reusable content chunks that get assembled

**Example**:
```
content-blocks/
  testing/
    pytest-setup.md         (reusable across SAPs)
    coverage-requirements.md
    ci-cd-patterns.md
  sap-004/
    problem-statement.md    (SAP-specific)
```

**Pros**: Highly reusable, composable, DRY
**Cons**: More complex assembly logic, potential coherence issues

---

#### Option C: Semantic Composition
**Description**: Framework selects relevant content blocks based on context

**Example**:
```
Given context='MCP server' + 'testing'
→ Framework selects: pytest-setup.md, mcp-testing-patterns.md, docker-test-env.md
```

**Pros**: Most flexible, context-aware selection
**Cons**: Requires AI/semantic understanding, less predictable

---

### Why This Matters

SAP-004 decomposition approach depends on your model:
- **Template slots**: We create structured templates with clear variables
- **Modular blocks**: We create library of reusable chunks
- **Semantic**: We tag content blocks with metadata for selection

We want to decompose SAP-004 in a way that aligns with your framework.

### Sub-Questions

1. Does chora-compose use one of these models, a hybrid, or something else?
2. How do content blocks reference/import each other?
3. Best practices for decomposing a 5-artifact SAP into content blocks?
4. How granular should content blocks be? (paragraph-level, section-level, document-level?)

---

## Question 3: Context Schema ⭐ IMPORTANT

**Question**: Can you share an example context schema from your framework?

### Our Assumptions

```json
{
  "repo_role": "mcp-server",
  "existing_capabilities": ["testing", "docker", "ci-cd"],
  "preferences": {
    "verbosity": "concise",
    "include_examples": true,
    "technical_depth": "intermediate"
  },
  "coordination_needs": true,
  "team_structure": "small-team"
}
```

### Why This Matters

We want to structure SAP-004 generation to accept rich context. Need to understand:
- What context dimensions your framework supports
- How deeply nested context can be
- Type system for context values
- Custom context fields allowed?

### Sub-Questions

1. What context variables does chora-compose support out-of-box?
2. Can we define custom context fields?
3. How deeply nested can context be?
4. Type system for context values? (string, enum, object, array?)
5. Context validation/schema enforcement?

---

## Question 4: Hybrid Model (Storage + Generation) ⭐ IMPORTANT

**Question**: Can some artifacts be storage-based (canonical hand-written) while others are generation-based?

### Our Vision

**Not all SAPs need generation.** Some are hand-crafted, others generated.

**Use Cases**:

| SAP | Approach | Rationale |
|-----|----------|-----------|
| **SAP-000** (sap-framework) | Hand-written canonical | Foundational docs, rarely changes, hand-crafted quality |
| **SAP-004** (testing-framework) | Canonical + generated variants | Base version stored, customized versions generated per repo type |
| **SAP-014** (mcp-server) | Always generated | Highly context-specific, different for each MCP server |
| **Custom org SAP** | Org maintains canonical, generates team versions | Organization standards + team customizations |

### The Question

Is this hybrid approach supported?
- ✅ **OR**: Does chora-compose require all-or-nothing (either all artifacts generated or all stored)?

### Why This Matters

We have **18 existing hand-written SAPs**. Some may benefit from generation (customization), others should remain canonical. Need to understand if hybrid is architecturally supported.

### Sub-Questions

1. Can generation reference stored artifacts? (e.g., include canonical SAP-000, generate customized SAP-004)
2. Can collections contain mix of stored + generated artifacts?
3. How to handle dependencies between stored and generated artifacts?
4. Is there a "pass-through" mode for artifacts that don't need generation?

---

## Question 5: Content Block Storage Location

**Question**: Where should content blocks live: chora-base repo, chora-compose repo, both, or user-defined?

### Four Options

#### Option A: chora-base
**Approach**: Content blocks stored in `chora-base/docs/content-blocks/`

**Pros**:
- ✅ Version controlled with SAPs
- ✅ Owned by domain experts
- ✅ Easy for chora-base team to update

**Cons**:
- ❌ chora-compose needs to access chora-base content
- ❌ Cross-repo dependency

---

#### Option B: chora-compose
**Approach**: Content blocks stored in chora-compose as part of framework

**Pros**:
- ✅ Framework owns content
- ✅ Simpler deployment
- ✅ No cross-repo access needed

**Cons**:
- ❌ chora-base doesn't own content
- ❌ Harder for domain experts to update

---

#### Option C: Hybrid
**Approach**: Domain content in chora-base, templates in chora-compose

**Pros**:
- ✅ Separation of concerns (content vs generation logic)
- ✅ Each repo owns their domain

**Cons**:
- ❌ More complex
- ❌ Requires coordination between repos

---

#### Option D: User-Defined
**Approach**: Each project defines content block locations in config

**Pros**:
- ✅ Maximum flexibility
- ✅ Projects control their content

**Cons**:
- ❌ No standard location
- ❌ Harder to share content blocks

---

### Why This Matters

Affects where we put SAP-004 content blocks during decomposition. Want to use your recommended pattern.

### Sub-Questions

1. Does chora-compose have a standard location for content blocks?
2. Can content blocks be remote (e.g., fetched from chora-base repo URL)?
3. How to version control content blocks separate from generated artifacts?
4. Import/export patterns for content blocks across repos?

---

## Collections Vision (Full Picture)

Since we under-communicated this, here's the complete vision:

### What Are Collections?

**Collections** = Higher-level holons (compositions of SAPs) that enable role-based bundling and context-aware generation.

### Role-Based Bundles

**Examples**:
- **MCP Server Developer**: SAPs 0, 3, 4, 14, 17, 18 (development workflow)
- **Platform Engineer**: SAPs 0, 7, 8, 11, 13 (infrastructure/observability)
- **Bronze Tier Entry**: SAPs 0, 1, 9, 16, 2 (minimal ecosystem onboarding)

**Benefit**: Repos request collection by role, get exactly what they need.

### Context-Aware Generation

**Same collection, different contexts** → Different artifacts

**Example**:
```bash
# MCP server repo
generate_collection('bronze-tier', context={
  role: 'mcp-server',
  capabilities: ['docker'],
  preferences: {verbosity: 'concise'}
})
# → Gets MCP-specific SAP-004 (testing for MCP servers)

# Django web app repo
generate_collection('bronze-tier', context={
  role: 'web-app',
  capabilities: ['django', 'postgresql'],
  preferences: {verbosity: 'detailed'}
})
# → Gets web-app-specific SAP-004 (testing for Django apps)
```

**Benefit**: Customized documentation for each repo's needs, not one-size-fits-all.

### "Latest" vs "Fresh" Artifacts

**Use Cases**:
- **Latest**: Production deployment needs stable, tested versions (use cached)
- **Fresh**: Development needs up-to-date customizations (always regenerate)
- **Hybrid**: Some artifacts cached (stable), others fresh (context-specific)

**User Control**:
```bash
generate_collection('minimal-entry', freshness='latest')  # Fast, cached
generate_collection('minimal-entry', freshness='fresh')   # Slow, current
```

**System-Determined** (alternative):
- Auto-regenerate if content blocks changed since last generation

### Multi-Tier Composition

| Tier | What | Example |
|------|------|---------|
| **Tier 1** | SAP (atomic holon) | SAP-004 with 5 artifacts |
| **Tier 2** | Collection (role bundle) | "MCP Dev Stack" (6 SAPs) |
| **Tier 3** | Collection of collections | "Ecosystem Health" (Bronze + Observability + Coordination) |

**Benefit**: Hierarchical composition enables complex use cases while maintaining simplicity.

---

## Impact on Pilot

### Decomposition Phase (Week 1)

Starting ~2025-11-06, we need to understand:
1. **Q2**: How to structure content blocks (template slots vs modular vs semantic)
2. **Q5**: Where to store content blocks (chora-base vs chora-compose vs hybrid)
3. **Q3**: What context to prepare (context schema)
4. **Q1**: Whether to plan for caching (latest vs fresh)
5. **Q4**: How hybrid model works (storage + generation)

### If We Misunderstand

- May structure content blocks incorrectly
- Requires rework during pilot or after
- Delays pilot progress

### If We Align Now

- Decomposition proceeds smoothly
- Content blocks structured optimally from start
- Pilot validates approach efficiently

---

## Our Flexibility

**We're flexible** on implementation details. If your architecture requires different approach than our vision, we can adapt.

### Non-Negotiables

1. Quality must meet **80%+** of hand-written SAP bar
2. Generated artifacts must be **agent-readable** (Claude can parse)
3. Content must be **factually accurate and coherent**

### Nice-to-Haves (Could Be Phase 2)

1. User-controlled "latest" vs "fresh" (could start with always-fresh)
2. Hybrid storage + generation (could start with all-generation)
3. Multi-tier collections (could start with simple collections)

---

## What We're NOT Asking

❌ Changes to pilot timeline or scope
❌ Implementation of new features for pilot
❌ Commitment to support collections architecture long-term
❌ Answers immediately (helpful before Week 1, but not blocking)

---

## Ideal Outcome

**By Week 1 Start** (~2025-11-06):
- Answers to **Q1** (caching) and **Q2** (content architecture) so we decompose correctly

**During Pilot**:
- Answers to **Q3-Q5** inform how we structure configs and where we store blocks

**After Pilot**:
- If pilot succeeds, we have clear path for scaling to 18 SAPs with aligned architecture

---

## Response Options

We're flexible on how you respond:

1. **Brief Answers**: Quick answers to 5 questions (~30 min effort)
2. **Detailed Discussion**: Schedule 30-60 min call to discuss architecture
3. **Documentation Links**: Point us to relevant docs that answer these questions
4. **Pilot as Discovery**: We learn through experimentation, adjust as we go

**All options work!** Choose what fits your availability and style.

---

## Thank You

Thank you for the enthusiastic response to COORD-2025-002! The alignment is exciting.

These clarifying questions help ensure we're approaching the pilot with **shared understanding** of the architecture. Looking forward to your thoughts!

— chora-base team

**Date**: 2025-10-29
**Reference**: COORD-2025-002 (original request), COORD-2025-002-RESPONSE (our acceptance)
**Next**: Await your response (helpful before Week 1, but not blocking pilot)
