# Collections Architecture Exploration Notes

**Status**: Exploratory (Pre-RFC)
**Created**: 2025-10-29
**Context**: Response to COORD-2025-001 (chora-workspace minimal SAP collaboration)

---

## Overview

This document captures exploratory thinking about evolving the SAP framework to support **collections as higher-level holons** and **generation-based artifacts**. This is pre-RFC work to clarify architectural questions before coordination with ecosystem repos.

## Current State (v4.0)

### SAP Structure
- **18 SAPs** documented in chora-base
- Each SAP = **5 required artifacts** (charter, protocol, awareness-guide, adoption-blueprint, ledger)
- SAPs are **hand-written markdown files** stored in `docs/skilled-awareness/{sap-name}/`
- **Dependency graph** exists (defined in sap-catalog.json)
- **Installation**: Manual copying of files (to be automated in Wave 5)

### Pain Points
1. **High barrier to entry**: 18 SAPs = ~100k tokens, 2-4 weeks to adopt fully
2. **No role-based bundles**: Can't say "I'm an MCP server, give me exactly what I need"
3. **Manual artifact creation**: Each SAP requires 8-12 hours to write 5 artifacts
4. **Static content**: Artifacts don't adapt to context (repo role, existing capabilities, etc.)
5. **Storage-based**: SAPs are files to copy, not compositions to generate

## Vision: Collections as Higher-Level Holons

### Architectural Concept

**Collection** = Higher-order holon that bundles related SAPs for specific role/purpose

```
Ecosystem
   ↓
Collection (e.g., "MCP Server Dev Stack")
   ↓
SAP (atomic capability holon)
   ↓
Artifacts (5 documents)
   ↓
Sections (structured content)
   ↓
Content Blocks (constituent content)
```

### Properties of Collections

1. **Composition** (not inheritance):
   - Collections bundle atomic SAPs
   - Each SAP remains independently adoptable
   - Collection provides curated subset for specific role

2. **Role-Based**:
   - "MCP Server Developer" → SAPs 0, 3, 4, 14, 17, 18
   - "Platform Engineer" → SAPs 0, 7, 8, 11, 13
   - "Bronze Tier Entry" → SAPs 0, 1, 9, 16, 2

3. **Requestable**:
   - Agent requests collection by name or role
   - System provides artifacts (cached or fresh)
   - Installation/integration happens automatically

4. **Context-Aware**:
   - Same collection can adapt to different repos
   - Artifacts composed based on repo role, existing capabilities, preferences

## Generation-Based vs Storage-Based

### Storage-Based (Current & v4.1.0 SAP Sets)

**Model**: SAPs are static files to copy

```
Collection = Bundle of Static SAP Artifacts
           ↓
Installation = Copy Files from chora-base to target repo
```

**Pros**:
- ✅ Simple implementation
- ✅ Consistent content (what you see is what you get)
- ✅ Fast (no generation overhead)
- ✅ Reviewable (artifacts are committed, versioned)

**Cons**:
- ❌ Not context-aware (same artifacts for all repos)
- ❌ Manual maintenance (18 SAPs × 5 artifacts = 90 files)
- ❌ No adaptation (MCP server gets same docs as Django app)
- ❌ High storage overhead (duplicate files across repos)

### Generation-Based (v4.2.0+ Vision)

**Model**: SAPs are recipes for composing artifacts from constituent content

```
Collection = Recipe for Composing Artifacts
           ↓
Constituent Content Blocks (stored or generated)
           ↓
Context (repo role, capabilities, preferences)
           ↓
Composition Engine (TBD: what tool?)
           ↓
Generated Artifacts (cached or fresh)
```

**Pros**:
- ✅ Context-aware (adapts to repo role, capabilities)
- ✅ Lower storage (content blocks reused across SAPs)
- ✅ Consistent patterns (generated from templates)
- ✅ Faster SAP creation (compose from building blocks)
- ✅ Customizable (same SAP, different contexts → different output)

**Cons**:
- ❌ Complex implementation (need composition engine)
- ❌ Requires tooling (what generates artifacts? where does it run?)
- ❌ Quality concerns (generated content vs hand-crafted)
- ❌ Caching strategy (when to regenerate? how to version?)

## Key Architectural Questions

### Q1: What is "Constituent Content"?

**Option A: Template Slots**
```yaml
# SAP-000 capability-charter template
sections:
  - id: problem-statement
    content: "Fixed content about SAP framework problem..."
  - id: solution-approach
    content: "Generated based on {{capability_name}} and {{target_role}}..."
```

**Option B: Modular Content Blocks**
```yaml
# SAP-000 capability-charter composition
content_blocks:
  - "content-blocks/sap-framework-problem.md" (stored)
  - "content-blocks/sap-framework-solution-core.md" (stored)
  - "generated-stakeholder-section" (generated based on repo role)
```

**Option C: Semantic Composition**
- Agent provides context (repo role, existing capabilities, goals)
- Composition engine selects relevant content blocks from library
- Generates coherent document from selected blocks + context

**Decision Needed**: Which model aligns with chora-base philosophy and capabilities?

### Q2: Where Does Constituent Content Live?

**Option A: In chora-base**
- `docs/content-blocks/` directory with reusable markdown chunks
- SAP definitions reference content blocks
- Content blocks versioned with chora-base

**Option B: In Composition Tool**
- External tool (e.g., hypothetical content generation service) stores templates
- chora-base provides schemas/specifications
- Tool generates artifacts on request

**Option C: Hybrid**
- Core content blocks in chora-base (domain knowledge)
- Templates in composition tool (generation logic)
- Ephemeral context in tool's cache (request-specific data)

**Decision Needed**: Where is authoritative source of content?

### Q3: What is the Composition Engine?

**Current Assumption**: "chora-compose" might be the tool

**Reality Check**:
- **chora-compose** (as documented in SAP-017/018) is Docker Compose orchestration
- **NOT a content generation tool** (despite early research agent confusion)
- **Wrong tool** for SAP artifact generation

**Alternative Tools**:
1. **Custom Python script in chora-base** (e.g., `scripts/compose-sap.py`)
   - Pros: Full control, no external dependency
   - Cons: Need to build all composition logic

2. **LLM-based generation** (via API: Anthropic, OpenAI, etc.)
   - Pros: Semantic understanding, natural language composition
   - Cons: Cost, latency, quality variability, API dependency

3. **Template engine** (Jinja2, Liquid, etc.)
   - Pros: Fast, deterministic, well-understood
   - Cons: Limited adaptability, requires explicit templates

4. **Dedicated MCP server** (future tool, doesn't exist yet)
   - Pros: Could integrate with chora ecosystem, agent-native
   - Cons: Doesn't exist, would need to build or coordinate

**Decision Needed**: What tool generates SAP artifacts?

### Q4: "Latest" vs "Fresh" Semantics

**"Latest"**: Use cached artifact if available
- Faster (no regeneration)
- Consistent (same artifact for all requests until cache expires)
- Trade-off: May be stale if content blocks changed

**"Fresh"**: Recompose artifact on every request
- Up-to-date (always uses latest content blocks + current context)
- Context-specific (same SAP, different repo → different artifact)
- Trade-off: Slower, more compute

**User Choice**:
```bash
# Use cached if available
request_collection minimal-entry --freshness=latest

# Always regenerate
request_collection minimal-entry --freshness=fresh
```

**System-Determined**:
- Check content block modification times
- If content changed since last generation → regenerate
- If context changed significantly → regenerate
- Otherwise → use cached

**Decision Needed**: User choice, system-determined, or both?

### Q5: What Happens to Existing SAPs?

**Option A: Keep as Canonical**
- Existing 18 SAPs remain as hand-written markdown (authoritative source)
- Generation creates variants/adaptations based on canonical SAPs
- Canonical SAPs are reviewed, versioned, committed

**Option B: Decompose and Regenerate**
- Decompose existing SAPs into constituent content blocks
- Delete original markdown files
- Generate SAPs on-demand going forward
- Risk: Loss of hand-crafted quality?

**Option C: Hybrid**
- Keep canonical SAPs in chora-base (for review, versioning)
- Generation creates customized variants for target repos
- Target repos get adapted versions, not canonical ones

**Decision Needed**: What's authoritative - stored SAPs or generated SAPs?

### Q6: Collection Definition Schema

**If generation-based**, collection schema needs to specify:

```yaml
id: minimal-entry
name: "Minimal Ecosystem Entry"
version: "1.0.0"

artifacts:
  - sap_id: SAP-000
    composition_recipe: "recipes/sap-framework-charter.yaml"
    required_context:
      - target_repo_role
      - existing_capabilities
    content_blocks:
      - "content-blocks/sap-framework-problem.md"
      - "content-blocks/sap-framework-solution-core.md"

  - sap_id: SAP-001
    composition_recipe: "recipes/inbox-protocol-charter.yaml"
    required_context:
      - coordination_needs
      - team_structure

generation_strategy:
  default_freshness: latest  # or fresh
  cache_ttl: 7 days
  recompose_triggers:
    - content_block_updated
    - context_changed
    - user_requested_fresh

installation:
  order: [SAP-000, SAP-001, SAP-009, SAP-016, SAP-002]
  estimated_time_hours: 3-5
```

**Decision Needed**: What metadata is required in collection definitions?

## Phased Implementation Strategy

### Phase 1: v4.1.0 (Q1 2026) - Storage-Based SAP Sets

**What**: Simple collections (just SAP ID arrays)
```json
{
  "sap_sets": {
    "minimal-entry": {
      "saps": ["SAP-000", "SAP-001", "SAP-009", "SAP-016", "SAP-002"],
      "estimated_tokens": 29000,
      "estimated_hours": "3-5"
    }
  }
}
```

**Installation**: Copy static files
```bash
python scripts/install-sap.py --set minimal-entry
# Copies 5 SAPs (5 artifacts each = 25 files) to target repo
```

**Why Start Here**:
- ✅ Solves immediate problem (chora-workspace onboarding)
- ✅ Simple implementation (24-33 hours)
- ✅ No external dependencies
- ✅ Validates collection concept with users
- ✅ Buys time to explore generation approach

### Phase 2: v4.2.0 (Q2 2026+) - Generation-Based Collections

**What**: Collections with composition recipes

**Prerequisite Decisions**:
1. ✅ Decide on composition engine (custom script, LLM, template engine, new tool?)
2. ✅ Decide on constituent content model (template slots, modular blocks, semantic?)
3. ✅ Decide on storage location (chora-base, external tool, hybrid?)
4. ✅ Decide on freshness semantics (user choice, system-determined, both?)
5. ✅ Decide on existing SAP handling (canonical, decompose, hybrid?)

**Implementation**:
- Decompose 1-2 SAPs into constituent content blocks (pilot)
- Build/integrate composition engine
- Create composition recipes
- Test generation quality vs hand-written
- Iterate based on feedback

**Timeline**: Depends on tool availability and coordination

## Who Needs to Be Involved?

### Internal (chora-base)

**Decisions we can make unilaterally**:
- Collection schema (metadata, structure)
- Constituent content model (how we organize building blocks)
- Storage location (where content blocks live in chora-base)
- Phasing (v4.1.0 vs v4.2.0 scope)

**Implementation we can do independently**:
- v4.1.0 SAP sets (no external dependencies)
- Content block library (in chora-base)
- Custom composition script (if we build our own)

### External Coordination Needed

**If using existing tool for composition**:
- Need to identify tool (currently: chora-compose is wrong tool)
- Coordinate on capabilities, integration, timeline
- Co-design composition approach

**Ecosystem feedback**:
- **chora-workspace**: Does minimal-entry set meet needs? Pilot test?
- **Other repos**: What role-based collections matter? Custom sets needed?

## Next Steps (Pre-RFC)

### 1. Clarify Vision (1-2 weeks)

**Questions to answer internally**:
- Do we want generation-based collections, or is storage-based sufficient?
- If generation: What tool/approach makes sense?
- What's the value proposition? (Is generation worth the complexity?)

**Approach**:
- Document trade-offs (this doc)
- Prototype 1 SAP decomposition (manual exercise)
- Assess feasibility and value

### 2. External Exploration (2-4 weeks)

**If generation-based looks valuable**:
- Identify potential composition tools
- Reach out for co-discovery (not requirements)
- Ask: "Can we explore X together?" not "Please build X"

**Coordination pattern**:
- Use `architecture_proposal` type (exploratory)
- Include questions, collaboration modes, explicit non-requirements
- Frame as mutual learning, not one-way request

### 3. Decision Point (After Exploration)

**Option A: Pursue Generation**
- Tool/approach identified
- Ecosystem partner interested in collaborating
- Value proposition clear
- → Write formal RFC, plan v4.2.0 implementation

**Option B: Defer Generation**
- No suitable tool found, or too complex
- Storage-based SAP sets meet needs
- Generation value unclear
- → Ship v4.1.0 SAP sets, revisit generation in v4.3.0+

**Option C: Build Custom**
- No external tool fits
- Value is clear enough to warrant building our own
- → Scope custom composition script in v4.2.0

### 4. Proceed with v4.1.0 Regardless

**Wave 5 implementation** (storage-based SAP sets):
- Does NOT depend on generation decisions
- Solves immediate problem
- Provides foundation for v4.2.0 enhancements
- Timeline: Q1 2026

## Open Questions for Future RFC

1. **Constituent content architecture**: Templates? Blocks? Semantic?
2. **Composition tool**: Custom script? LLM API? Template engine? External tool?
3. **Storage model**: Content blocks in chora-base? External? Ephemeral?
4. **Freshness semantics**: User choice? System-determined? Both?
5. **Existing SAPs**: Canonical? Decompose? Hybrid?
6. **Quality assurance**: How to ensure generated content meets SAP quality standards?
7. **Versioning**: How to version collections, content blocks, and generated artifacts?
8. **Customization**: How much can repos customize generated artifacts?
9. **Maintenance**: Who maintains content blocks? Composition recipes? Templates?
10. **Testing**: How to test generated artifacts for correctness, completeness, coherence?

## Conclusion

**Current State**:
- v4.1.0 SAP sets (storage-based) are well-defined and implementable
- Generation-based collections are visionary but under-specified

**Recommended Path**:
1. ✅ **Ship v4.1.0 with SAP sets** (solves immediate need, validates collection concept)
2. ✅ **Document generation vision** (this exploration doc)
3. ✅ **Explore composition tools** (co-discovery, not prescription)
4. ⏳ **Decide on v4.2.0 scope** (based on exploration outcomes)
5. ⏳ **Write formal RFC** (if pursuing generation in v4.2.0)

**Key Insight**:
Collections as higher-level holons are valuable **regardless of generation**. Storage-based collections (v4.1.0) provide immediate benefit. Generation-based collections (v4.2.0+) are enhancement, not requirement.

---

**Status**: Exploratory - NOT an RFC yet
**Next Review**: After Wave 5 (v4.1.0) ships and ecosystem feedback gathered
**Owner**: chora-base maintainers
**Stakeholders**: chora-workspace (pilot), future: composition tool maintainers (TBD)
