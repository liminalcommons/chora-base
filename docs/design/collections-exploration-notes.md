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

## UPDATE: chora-compose Response (2025-10-29)

### Major Discovery: Perfect Alignment Found

**COORD-2025-002 Response Received**: chora-compose is NOT Docker orchestration - it's a **content generation framework with 17 production generators** designed exactly for our use case!

### What We Learned

**chora-compose Reality**:
- ✅ Content generation framework (not Docker tool)
- ✅ 17 production generators for structured documentation
- ✅ 17 MCP tools for AI-native workflows
- ✅ Artifact composition from constituent content blocks
- ✅ Supports exactly our model: content blocks + context → SAP artifacts
- ✅ Template-based (Jinja2) with configuration-driven workflows
- ✅ MCP integration (generate conversationally via Claude Desktop)

**Our Documentation Gap**:
- ❌ SAP-017 and SAP-018 document **outdated version** (Docker focus from early development)
- ✅ Need to rewrite both SAPs after pilot validates current capabilities

**Their Response**:
> "STRONG ALIGNMENT! chora-compose is NOT just Docker orchestration - it's a content generation framework with 17 production generators, artifact composition, and template-based workflows. Documentation generation is EXACTLY our core capability."

### Answers to Our Open Questions

**Q2: Composition Tool** (ANSWERED)
- ✅ **chora-compose** (content generation framework)
- NOT custom script, NOT LLM API, NOT template engine
- Proven at scale with 17 production generators
- MCP integration enables AI-native workflows

**Q1: Constituent Content Architecture** (CLARIFYING)
- Likely: Template slots with Jinja2 rendering
- Content configs (JSON) define what goes where
- Artifact configs assemble multiple content pieces
- **Pilot will validate**: Decompose SAP-004 to test model

**Q3: Storage Model** (CLARIFYING)
- Content blocks in chora-base (version controlled)
- Configs and templates in chora-compose (generation logic)
- Generated artifacts can be cached or regenerated
- **Pilot will validate**: Test this hybrid approach

**Q4: Freshness Semantics** (SUPPORTED)
- chora-compose supports both "latest" (cached) and "fresh" (regenerate)
- Versioning tracks changes across regenerations
- **Pilot will validate**: Test caching and regeneration

**Q5: Existing SAPs** (HYBRID LIKELY)
- Keep hand-written SAPs as canonical (for now)
- Generate customized variants for target repos
- **Pilot will determine**: Can generated match hand-written quality?

**Q6-10: Quality, Versioning, Maintenance** (PARTIALLY ANSWERED)
- chora-compose has validation rules and quality gates
- Config versioning and schema validation supported
- **Pilot will validate**: Test quality assurance workflow

### Pilot Project Approved

**Decision**: ✅ Accept chora-compose pilot proposal (Option 3: Experiment Together)

**Pilot SAP**: SAP-004 (Testing Framework)
**Timeline**: 1-2 weeks (starting ~2025-11-06)
**Effort**: 4-6 hours (chora-base), 4-6 hours (chora-compose)

**Pilot Phases**:
1. **Decomposition** (Week 1, 2-4 hours) - Decompose SAP-004 into content blocks
2. **Configuration** (Week 1-2, 1-2 hours) - chora-compose creates configs, chora-base reviews
3. **Generation & Quality Review** (Week 2, 1-2 hours) - Generate and assess quality
4. **Go/No-Go Decision** (Week 2, 1 hour) - Proceed with Option B or fall back

**Success Threshold**: Generated SAP-004 meets **80%+** of hand-written quality

**Go/No-Go Outcomes**:
- **Go**: Proceed with Wave 6 Option B (generation-based collections) in v4.2.0
- **No-Go**: Fall back to Option A (metadata only) or Option C (defer to v4.3.0)

### Effort Estimates Updated

**Original Estimate** (v4.2.0 Option B):
- 81-138 hours (wide range due to uncertainty)
- Custom script: 20-30 hours OR external tool integration: 30-50 hours

**New Estimate** (with chora-compose):
- **20-40 hours total** (chora-compose's estimate after initial setup)
- **56-89 hours including SAP-017/018 rewrite** (vs 81-138 original)
- **87% maintenance reduction**: 144-216 hours → 20-40 hours

**Pilot Project**:
- 6-11 hours combined (4-6 hours chora-base, 2-4 hours chora-compose)

### Mutual Benefits Identified

**For chora-compose**:
1. Flagship use case: 18 SAPs × 5 artifacts = 90 generated artifacts
2. Quality validation: Our high bar tests generator robustness
3. Ecosystem integration: Deep collaboration with widely-adopted chora-base
4. Use case clarity: "Generate SAPs" vs abstract "content generation"
5. Documentation at scale: Real-world stress test
6. SAP generation showcase: Demonstrable capability

**For chora-base**:
1. 87% effort reduction (144-216h → 20-40h)
2. Consistency via shared templates
3. Efficiency: Update blocks once, regenerate all
4. Adaptability: Context-aware generation
5. Quality gates via framework
6. MCP integration (generate conversationally)
7. Versioning support
8. Ecosystem benefit: Other repos can generate SAPs

### Risks Acknowledged

**Risk 1: Quality doesn't meet bar**
- Likelihood: Medium
- Mitigation: Pilot first, no obligation to continue
- **Our addition**: Detailed quality rubric, 80% threshold

**Risk 2: SAP interdependencies**
- Likelihood: Low-Medium
- Mitigation: Start simple, iterate
- **Our addition**: SAP-004 has minimal interdependencies

**Risk 3: Setup effort exceeds value**
- Likelihood: Low
- Mitigation: Break-even analysis after pilot
- **Our addition**: Even 10 of 18 SAPs = 50%+ savings

**Risk 4: Framework changes break generation**
- Likelihood: Low
- Mitigation: Config versioning, validation, tests
- **Our addition**: Content blocks in chora-base (version controlled)

### Updated Recommended Path

1. ✅ **Ship v4.1.0 with SAP sets** (in progress - Wave 5)
2. ✅ **Document generation vision** (this doc - complete)
3. ✅ **Explore composition tools** (COORD-2025-002 - **chora-compose confirmed**)
4. 🧪 **Execute pilot project** (SAP-004 generation - approved)
5. 🎯 **Make go/no-go decision** (end of pilot - ~2025-11-19)
6. ⏳ **If Go**: Implement v4.2.0 Option B with chora-compose
7. ⏳ **If No-Go**: Fall back to Option A or C

### Next Steps

**Immediate (This Week)**:
1. ✅ Accept pilot proposal (COORD-2025-002-RESPONSE sent)
2. 📖 Review chora-compose documentation (README, architecture, configs)
3. ⚠️ Add warning to SAP-017/018 (outdated content)
4. 📋 Create pilot project tracking document

**Pilot Week 1** (~2025-11-06 to 2025-11-12):
1. Decompose SAP-004 into content blocks (2-4 hours)
2. Review chora-compose configs (1-2 hours)
3. Iterate on structure

**Pilot Week 2** (~2025-11-13 to 2025-11-19):
1. Generate SAP-004 artifacts (chora-compose)
2. Quality assessment (1-2 hours)
3. Go/no-go decision (1 hour)

**If Pilot Succeeds**:
1. Proceed with Wave 6 Option B in v4.2.0
2. Rewrite SAP-017/018 (16-24 hours)
3. Scale to remaining 17 SAPs
4. Integrate with collections architecture

**If Pilot Fails**:
1. Document learnings
2. Fall back to Option A or C
3. Still update SAP-017/018 (correct documentation)

### Key Insights

**Collection Concept Validated**:
- Storage-based (v4.1.0) solves immediate problem ✅
- Generation-based (v4.2.0) now has clear implementation path ✅
- Tool identified and validated ✅
- Pilot provides low-risk validation ✅

**Strategic Alignment**:
- chora-compose needs validation use case (90 artifacts)
- chora-base needs efficiency (87% reduction)
- Ecosystem benefits from both (consistent SAP patterns)

**Surprise Discovery**:
- We thought we were reaching out to Docker tool
- Discovered perfect-fit content generation framework
- This is rare and exciting alignment!

### Related Files

**Coordination**:
- `inbox/outgoing/coordination/COORD-2025-002-chora-compose-exploration.json` - Our request
- `inbox/incoming/coordination/COORD-2025-002-response.json` - Their response
- `inbox/outgoing/COORD-2025-002-RESPONSE.json` - Our acceptance

**Planning**:
- `docs/project-docs/CHORA-BASE-4.0-VISION.md` - Wave 6 updated to Pilot Phase
- `docs/design/pilot-sap-004-generation.md` - Pilot tracking (to be created)
- `docs/design/sap-017-018-update-plan.md` - SAP update planning (to be created)

**SAPs Needing Update**:
- `docs/skilled-awareness/chora-compose-integration/` (SAP-017) - Outdated
- `docs/skilled-awareness/chora-compose-meta/` (SAP-018) - Outdated

---

## UPDATE: Clarification Response (2025-10-30)

### COORD-2025-002-CLARIFICATION Response Received

**Summary**: All 5 architectural questions answered. Strong foundation confirmed with minor gaps. **No blockers for pilot** - missing features can be added incrementally (2-6 hours each).

### Answers to Critical Questions

#### Q1: Caching & Freshness Semantics (ANSWERED)

**Short Answer**: Partial support - works for pilot, can enhance if needed

**What Exists**:
- ✅ Versioned ephemeral storage with timestamp-based versions
- ✅ Session-level context cache (in-memory)
- ✅ `force: bool` parameter in MCP tools (force=True bypasses cache)
- ✅ RetrievalStrategy enum defined ("latest", "all", "version", "approved_only")

**What Doesn't Exist**:
- ❌ Automatic staleness detection (no TTL or input hash comparison)
- ❌ Dependency-based invalidation (input changes don't auto-trigger regeneration)
- ❌ force parameter at ArtifactComposer level (only in MCP tools)
- ❌ Per-child cache control (can't configure which children to cache vs regenerate)

**Terminology Clarification**:
- They use: `force: bool` (industry standard from git, npm, docker)
- Not: "latest" vs "fresh" (those are retrievalStrategy values)
- **Mapping**:
  - Our "latest" = Their `force=False` (default, use cached)
  - Our "fresh" = Their `force=True` (always regenerate)

**Workaround for Pilot**:
- Use existing `force` parameter pattern from MCP tools
- For cached: call `generate_content(config_id)` - uses session cache
- For fresh: call `generate_content(config_id, force=True)` - bypasses cache
- Limitation: Works for individual content, not automatic at artifact assembly level

**Effort to Add Missing Features**:
- `force` in ArtifactComposer: 2-3 hours
- Per-child cache control (honor retrievalStrategy): 3-4 hours
- Staleness detection: 6-8 hours (complex, likely not needed)

**Recommendation**: Start with existing patterns, defer advanced caching to Phase 2

#### Q2: Content Block Architecture (PERFECT MATCH)

**Short Answer**: Hybrid - Template Slots + Modular Blocks. ContentElement provides structure, GenerationPattern provides assembly logic, ChildReference provides modularity.

**ContentElement Structure** (Atomic Unit):
```json
{
  "name": "problem-statement",
  "description": "Human-readable description",
  "prompt_guidance": "Hints for AI generation",
  "format": "markdown | code | json | yaml | gherkin | section | text",
  "example_output": "Actual content or example (the 'content block' itself)",
  "generation_source": "ai | human | template | mixed | any",
  "review_status": "pending | approved | needs_revision | rejected"
}
```

**GenerationPattern Structure** (Assembly Logic):
```json
{
  "id": "pattern-id",
  "type": "jinja2 | demonstration | template_fill",
  "template": "{{ title }}\n\n{{ features }}\n\n{{ installation }}",
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "features", "source": "elements.features.example_output"}
  ],
  "generation_config": {
    "context": {...}
  }
}
```

**ChildReference Structure** (Modular Composition):
```json
{
  "id": "shared-pytest-setup",
  "path": "configs/content/shared-pytest-setup/shared-pytest-setup-content.json",
  "required": true,
  "order": 10,
  "version": "1.2.3",
  "retrievalStrategy": "latest"
}
```

**Composition Strategy**:
- ✅ Concat (join children with `\n\n`) - implemented
- ❌ Merge, template, custom - not yet implemented

**Granularity Recommendations**:
- **Element level**: Single logical unit (problem-statement, pytest-setup-code)
- **Content config level**: Related elements forming coherent piece (SAP charter with 5-7 elements)
- **Child config level**: When >5-7 elements OR reusability needed
- **Artifact level**: Final assembly of multiple content configs

**Recommended Structure for SAP Decomposition**:
```
Tier 1: Elements (5-7 ContentElements per artifact)
  ↓
Tier 2: Content Configs (one per artifact: sap-004-charter-content.json)
  ↓
Tier 3: Shared Blocks (extract common patterns, reference via children)
  ↓
Tier 4: Artifact (sap-004-testing-framework-artifact.json references 5 content configs)
```

**Example SAP-004 Charter Elements**:
- title (markdown)
- problem-statement (section)
- solution-approach (section)
- key-capabilities (section)
- adoption-prerequisites (section)

**Reusable Shared Blocks**:
- shared-pytest-setup-content.json (referenced by multiple SAPs)
- shared-ci-cd-patterns-content.json
- shared-docker-integration-content.json

**Decision**: Use hybrid model - template slots for structure, modular blocks for reusability

#### Q3: Context Schema (FULLY FLEXIBLE)

**Short Answer**: No predefined schema - users define exactly what they need. 6 source types, JSONPath selectors, nested objects, custom fields.

**InputSource Types** (6 Built-in):
1. **content_config**: Load another content config as context
2. **external_file**: Load JSON/YAML/text from filesystem
3. **git_reference**: Load file from git ref (commit, branch, tag) - format: `{ref}:{path}`
4. **ephemeral_output**: Load previously generated content from storage
5. **inline_data**: Embed JSON data directly in config
6. **artifact_config**: Load artifact config metadata as context

**Data Selectors** (Extract Portions):
- **whole_content**: Return entire content (default)
- **jsonpath**: `$.users[0].name`, `$.paths.*.get.summary`, `$..name`
- **line_range**: `10-20`, `:50`, `100:`
- **markdown_section**: `# Installation`, `## Usage Examples`
- **code_element**: `function:calculate_total`, `class:UserManager`

**Context Structure Flexibility**:
- No predefined schema - define whatever you need
- Nested objects fully supported
- Any field names allowed (repo_role, existing_capabilities, preferences, team_structure)
- Type system: Python `dict[str, Any]` (str, int, bool, list, dict, etc.)

**Example Context for SAP Generation**:
```json
{
  "inputs": {
    "sources": [
      {
        "id": "repo_metadata",
        "source_type": "external_file",
        "source_locator": "target-repo/repo-metadata.json",
        "data_selector": "$",
        "required": true
      },
      {
        "id": "existing_capabilities",
        "source_type": "external_file",
        "source_locator": "target-repo/sap-catalog.json",
        "data_selector": "$.adopted_saps[*].id",
        "required": false
      },
      {
        "id": "user_preferences",
        "source_type": "inline_data",
        "source_locator": "{\"verbosity\": \"concise\", \"include_examples\": true, \"technical_depth\": \"intermediate\"}",
        "required": false
      }
    ]
  }
}
```

**Resolved Context Structure**:
```json
{
  "repo_metadata": {
    "repo_name": "my-mcp-server",
    "repo_role": "mcp_server_developer",
    "team_structure": "solo_developer",
    "coordination_needs": false
  },
  "existing_capabilities": ["SAP-000", "SAP-001", "SAP-003"],
  "user_preferences": {
    "verbosity": "concise",
    "include_examples": true,
    "technical_depth": "intermediate"
  }
}
```

**Recommended Context Fields for SAP Generation**:
- **repo_metadata**: repo_name, repo_role, primary_language, team_structure
- **existing_capabilities**: adopted_saps (array of SAP IDs), capability_tags
- **user_preferences**: verbosity (concise|moderate|detailed), include_examples (bool), technical_depth (beginner|intermediate|advanced)
- **coordination_context**: coordinates_with (array), coordination_mode (optional)

**Decision**: Define custom context via InputSource, store schemas in chora-base, version alongside SAPs

#### Q4: Hybrid Storage + Generation (PARTIAL SUPPORT, WORKS MANUALLY)

**Short Answer**: Yes, can mix storage-based (canonical hand-written) and generation-based. Manual hybrid works today via external_file, automatic orchestration needs ~2-4 hours.

**Current Hybrid Support**:

**Via external_file** (Reference stored content):
```json
{
  "inputs": {
    "sources": [
      {
        "id": "canonical_sap_framework",
        "source_type": "external_file",
        "source_locator": "chora-base/docs/skilled-awareness/sap-framework/capability-charter.md",
        "data_selector": "# SAP Structure",
        "required": true
      }
    ]
  },
  "generation": {
    "patterns": [{
      "template": "This SAP follows the structure defined in SAP-000:\n\n{{ canonical_sap_framework }}\n\n## Specific to Testing Framework\n\n{{ generated_specific_content }}"
    }]
  }
}
```

**Via ephemeral_output** (Reference previously generated):
```json
{
  "artifact_children": [
    {
      "id": "sap-000-stored",
      "path": "configs/content/sap-000-passthrough-content.json",
      "note": "passthrough content config that loads from external_file (stored)"
    },
    {
      "id": "sap-004-generated",
      "path": "configs/content/sap-004-charter-content.json",
      "note": "generated fresh based on target repo context"
    }
  ]
}
```

**Via demonstration generator** (Pass-through mode):
- Generate() returns stored content unchanged
- Use for canonical SAPs that don't need customization

**What's Missing**:
- ❌ retrievalStrategy defined but not enforced in ArtifactComposer
- ❌ Automatic decision (stored vs generated based on staleness)
- ❌ Per-child mode control (explicit 'stored' vs 'generated' flag)

**Effort to Add**:
- Wire retrievalStrategy: 2-3 hours
- Staleness-aware hybrid: 4-6 hours (complex)
- Per-child mode control: 1-2 hours

**Workaround for Pilot**:
- Create passthrough content config that loads via external_file for canonical SAPs
- Use normal generation patterns for customized SAPs
- Artifact assembles mix of passthrough + generated children

**Example Bronze Collection Hybrid**:
- Canonical SAPs (stored): SAP-000 (framework), SAP-001 (inbox)
- Generated SAPs (fresh): SAP-004 (testing customized for repo), SAP-009 (awareness customized)
- Assembly: Artifact references 2 passthrough configs + 2 generated configs

**Decision**: Start with manual hybrid via external_file, consider automatic orchestration if need emerges (2-4 hours)

#### Q5: Content Block Storage Location (CLEAR PATTERNS EXIST)

**Short Answer**: Hybrid (Option C recommended) - Domain content in chora-base, configs in both repos, generated outputs in ephemeral storage.

**Existing Storage Patterns**:

**Content configs**: `configs/content/{config-id}/{config-id}-content.json`
- Example: `configs/content/my-feature/my-feature-content.json`
- Purpose: Define what to generate and how

**Artifact configs**: `configs/artifact/{artifact-id}/{artifact-id}-artifact.json`
- Example: `configs/artifact/documentation-bundle/documentation-bundle-artifact.json`
- Purpose: Define how to assemble multiple content pieces

**Draft configs**: `ephemeral/drafts/{type}/{draft-id}.json`
- Example: `ephemeral/drafts/content/draft-20251030T153045-a1b2c3.json`
- Purpose: Temporary configs before persistence

**Generated content**: `ephemeral/{content_id}/{timestamp}.{format}`
- Example: `ephemeral/api-docs/2025-10-30T15:30:45.123456+00:00.md`
- Fallback: `/tmp/chora-ephemeral/` or `${TMPDIR}/chora-ephemeral/`
- Purpose: Versioned generated content (cached)

**Final artifacts**: User-specified in `ArtifactConfig.metadata.outputs[].file`
- Examples: `docs/MY_FEATURE.md`, `README.md`, `tests/test_feature.py`

**Recommended Hybrid Approach**:

**Domain content in chora-base**:
- What: Actual content blocks (markdown files, reusable text)
- Where: `chora-base/docs/content-blocks/testing-framework/*.md`
- Why: Domain experts (chora-base maintainers) own and update content
- Version control: Git history tracks content evolution
- Examples:
  - `docs/content-blocks/testing-framework/problem-statement.md`
  - `docs/content-blocks/testing-framework/pytest-setup.md`
  - `docs/content-blocks/testing-framework/coverage-requirements.md`
  - `docs/content-blocks/shared/ci-cd-patterns.md`

**Configs in both repos**:
- **chora-base configs**: Content configs defining SAP generation
  - Where: `chora-base/configs/content/sap-004/*.json`
  - Examples: `sap-004-charter/sap-004-charter-content.json`
- **chora-compose templates**: Jinja2 templates for SAP artifact structure
  - Where: `chora-compose/templates/sap/*.j2` (if reusable across projects)
  - Examples: `templates/sap/charter.md.j2`

**Reference pattern**:
```json
{
  "config_location": "chora-base/configs/content/sap-004-charter/sap-004-charter-content.json",
  "references_content": {
    "inputs": {
      "sources": [
        {
          "id": "problem_statement",
          "source_type": "external_file",
          "source_locator": "../../docs/content-blocks/testing-framework/problem-statement.md",
          "note": "Relative path from config to content block"
        }
      ]
    }
  }
}
```

**Remote Content Support**:
- ✅ git_reference: Load from git refs (commits, branches, tags)
  - Format: `{ref}:{path}` - example: `main:README.md`, `v1.0.0:docs/charter.md`
  - Use case: Reference content blocks from specific chora-base versions
- ❌ HTTP URLs not supported (can add in 2-3 hours if needed)
- Workaround: Use git_reference or external_file after git clone

**Version Control Patterns**:
- Content versioning: Git history for content blocks in chora-base
- Config versioning: Evolution metadata in configs + git history
- Generated artifact versioning: Ephemeral storage with timestamp-based versions

**Recommendation for SAP Pilot**:

**Content block storage**:
- Location: `chora-base/docs/content-blocks/`
- Structure:
  - SAP-specific: `docs/content-blocks/testing-framework/*.md`
  - Shared: `docs/content-blocks/shared/*.md` (reused across SAPs)
  - Organized by SAP: `docs/content-blocks/{sap-name}/` directories
- Ownership: chora-base team maintains content
- Version control: Git history in chora-base tracks evolution

**Config storage**:
- Content configs: `chora-base/configs/content/sap-004-*/` (5 configs, one per artifact)
- Artifact config: `chora-base/configs/artifact/sap-004-testing-framework/` (1 config referencing 5 content configs)
- Templates: Start inline (in config), extract to files if reuse emerges

**Cross-repo reference**:
- Approach 1: Git submodule (add chora-base as submodule, reference via relative path) - **Recommended for pilot**
- Approach 2: git_reference source type with chora-base repo URL
- Approach 3: Copy configs from chora-base to target repo (loses upstream updates)

**Decision**: Hybrid storage - content blocks in chora-base, configs in chora-base, templates inline or in chora-compose, generated in ephemeral

### Pilot Execution Plan (Updated)

**Week 1 Decomposition** (~2025-11-06 to 2025-11-12):

**What You Now Know**:
1. Content block architecture: Use ContentElement with hybrid template slots + modular blocks
2. Context structure: Define custom fields via InputSource (repo_metadata, existing_capabilities, user_preferences)
3. Storage locations: Content blocks in chora-base/docs/content-blocks/, configs in chora-base/configs/
4. Hybrid approach: Reference stored content via external_file, generate customized content
5. Caching: Use existing patterns (force parameter), defer advanced caching to Phase 2

**Decomposition Steps**:
1. Select SAP-004 artifacts (charter, protocol, guide, blueprint, ledger)
2. Decompose each artifact into 5-7 ContentElements (problem-statement, solution-approach, etc.)
3. Extract shared/reusable blocks into separate markdown files (pytest-setup.md, coverage-requirements.md)
4. Create 5 content configs (one per artifact) in chora-base/configs/content/sap-004-*/
5. Create 1 artifact config that references 5 content configs
6. Define context schema (repo_metadata.json, user_preferences.json)

**Expected Output**:
- Content blocks: ~10-15 markdown files in docs/content-blocks/testing-framework/
- Content configs: 5 JSON files in configs/content/sap-004-*/
- Artifact config: 1 JSON file in configs/artifact/sap-004-testing-framework/
- Context schemas: Example context files for testing

**During Pilot Flexibility**:
- Discovery mode: Experiment with patterns, adjust based on what works
- Iteration expected: Decomposition may require 2-3 rounds of refinement
- Feature additions: If discover need for force parameter or retrievalStrategy wiring, they can add (2-4 hours)
- No commitment: Pilot is exploration - if patterns don't work, adjust or acknowledge misalignment

### Feature Gaps and Effort Estimates

**Missing Features Summary**:
- ❌ force in ArtifactComposer: 2-3 hours (Low priority for pilot)
- ❌ retrievalStrategy wiring: 2-4 hours (Medium priority if hybrid orchestration needed)
- ❌ Staleness detection: 6-8 hours (Low priority - complex, likely not needed)
- ❌ HTTP URL sources: 2-3 hours (Low priority - git_reference works for most cases)

**What Doesn't Need Building**:
- ✅ Content architecture - exists and works well
- ✅ Context flexibility - fully flexible, no changes needed
- ✅ Storage patterns - clear patterns exist
- ✅ Hybrid via external_file - works today
- ✅ Versioned ephemeral storage - production-ready

### Architectural Alignment Assessment

**Strong Alignment**:
- ✅ Multi-tier composition (elements → content → artifact → collection) matches SAP → Collection → Collection-of-Collections vision
- ✅ Hybrid storage + generation supported via InputSource patterns
- ✅ Context-aware generation is core capability (Jinja2 + context)
- ✅ Caching and versioning infrastructure exists (ephemeral storage)
- ✅ Modular block reusability via child references

**Minor Gaps**:
- Caching terminology and control (use 'force: bool', can enhance 2-3 hours)
- retrievalStrategy not wired (easy addition 2-4 hours)
- No automatic staleness detection (complex 6-8 hours, likely not needed)

**No Architectural Conflicts**: Our vision fits within chora-compose architecture. Gaps are feature additions, not design conflicts.

### Next Steps

**Our Side** (chora-base):
- Begin SAP-004 decomposition using ContentElement pattern
- Store content blocks in chora-base/docs/content-blocks/testing-framework/
- Create content configs referencing blocks via external_file
- Define context schemas (repo_metadata, user_preferences)
- Share initial configs for review/iteration

**Their Side** (chora-compose):
- Available for questions during decomposition
- Review configs and provide feedback
- Add missing features if specific needs emerge (2-4 hours as needed)
- Iterate on patterns based on pilot learnings

**Collaboration Mode**: Async via inbox protocol or GitHub issues, sync call if helpful

### Key Takeaway

**Tone from chora-compose**: "Transparent and technical. We've given you honest assessment of what exists, what doesn't, and effort estimates. No overselling - strong foundation with pilot-friendly gaps."

**Our Response**: Thrilled by the comprehensive 1,124-line technical response with code examples, effort estimates, workarounds, and recommendations. This is exactly what we needed to move forward with confidence.

**Appreciation from them**: "Thank you for the detailed architectural questions! This level of specificity helps ensure we're aligned on approach before decomposition begins. Looking forward to the pilot."

---

**Status**: Clarification Complete (2025-10-30) - Ready for Week 1 Decomposition
**Next Review**: After pilot completes (~2025-11-19) for go/no-go decision
**Owner**: chora-base maintainers
**Stakeholders**: chora-compose (collaboration partner), chora-workspace (collections adopter)
