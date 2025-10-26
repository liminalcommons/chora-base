# Claude Vision Planning - Strategic Design

**Purpose:** Claude-specific patterns for strategic vision work and future capability planning.

**Parent:** See [../../CLAUDE.md](../../CLAUDE.md) for project-level patterns, [../CLAUDE.md](../CLAUDE.md) for development guide, and [AGENTS.md](AGENTS.md) for generic vision guide.

---

## Critical Distinction: Vision vs. Roadmap

**IMPORTANT:** Claude must understand the difference between vision (exploratory) and roadmap (committed).

### Vision Documents (This Directory)
- **Status:** Exploratory, aspirational, fluid
- **Purpose:** Inform architecture, keep options open
- **NOT for implementation:** Don't build exploratory features now

### Roadmap ([../../ROADMAP.md](../../ROADMAP.md))
- **Status:** Committed, time-bound, stable
- **Purpose:** Define what to build next
- **FOR implementation:** Build committed features

---

## Claude's Strengths for Vision Work

### 1. Strategic Analysis Across 200k Context

Claude can hold entire vision documents + current codebase in context:

```markdown
"Analyze strategic alignment:

Load:
1. All vision documents (dev-docs/vision/)
2. Current codebase architecture (src/mcp_orchestrator/)
3. Current wave plan (project-docs/WAVE_1X_PLAN.md)
4. User feedback (if available)

Analysis:
- Does current architecture support future vision?
- What extension points should we design now?
- What technical debt blocks future capabilities?
- What decisions keep options open?

Provide strategic recommendations."
```

### 2. Multi-Wave Planning

Claude excels at wave-based capability evolution:

```markdown
"Plan Wave 2.0 based on Wave 1.x learnings:

Context:
- Wave 1.x complete: [list features]
- User feedback: [summarize requests]
- Technical learnings: [architecture insights]
- Vision documents: [relevant sections]

Planning:
1. Identify most valuable Wave 2 capabilities
2. Estimate effort and dependencies
3. Design extension points in current code
4. Document risks and unknowns

Output: Wave 2.0 plan draft for review"
```

### 3. Architecture for Future Capabilities

Claude can design extension points without implementing features:

```markdown
"Design artifact metadata for future policy engine:

Current: Artifact has hash, signature, timestamp
Vision: Wave 2 adds policy enforcement (governance)

Task:
1. Review vision/MCP_CONFIG_ORCHESTRATION.md (Wave 2)
2. Identify what metadata future policies need
3. Design extensible metadata schema
4. Don't implement policy engine (not committed)
5. Do add metadata fields (low cost, high value)

Show me metadata schema design."
```

---

## Vision Work Patterns

### Pattern: Strategic Planning Session

```markdown
"Strategic planning for mcp-orchestration:

## Context (200k window advantage)
Load everything:
1. All vision documents (dev-docs/vision/)
2. Current wave completed (project-docs/WAVE_1X_PLAN.md)
3. Entire codebase (src/mcp_orchestrator/)
4. User documentation (user-docs/)
5. Recent telemetry (var/telemetry/events.jsonl)

## Analysis Questions
1. What patterns emerged in Wave 1.x?
2. What user needs aren't met?
3. What technical debt accumulated?
4. What architecture constraints exist?
5. What opportunities appeared?

## Vision Alignment
1. Review MCP_CONFIG_ORCHESTRATION.md
2. Which Wave 2/3/4 capabilities are most valuable?
3. What should we prioritize next?
4. What foundation do we need?

## Output
- Wave planning recommendations
- Architecture improvements needed
- Strategic decisions for leadership

Provide comprehensive strategic analysis."
```

### Pattern: Capability Evaluation

```markdown
"Evaluate proposed capability: [capability_name]

## Evaluation Criteria
1. **User Value**
   - What problem does this solve?
   - How many users need this?
   - What's the impact if we don't build it?

2. **Technical Feasibility**
   - Can we build with current architecture?
   - What extensions are needed?
   - What are the risks?

3. **Strategic Fit**
   - Aligns with product vision?
   - Builds on current capabilities?
   - Opens future opportunities?

4. **Cost/Benefit**
   - Effort estimate (story points)
   - Time to market
   - Maintenance burden
   - ROI projection

## Context
- Vision: dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md
- Current architecture: src/mcp_orchestrator/
- User feedback: [if available]

## Recommendation
Should we:
- Build now (add to roadmap)
- Plan for next wave (design extension points)
- Defer indefinitely (document reasoning)

Provide evaluation with reasoning."
```

### Pattern: Extension Point Design

```markdown
"Design extension points for future capability:

Future Capability: [name] (from vision documents)
Current Wave: [X].[Y]
Future Wave: [Z] (estimated)

## Task
1. Review vision document describing capability
2. Identify what current code needs to support future
3. Design extension points (interfaces, metadata, hooks)
4. Estimate cost of adding extension points now
5. Estimate cost if we don't (future refactoring)

## Constraints
- Don't implement the future capability
- Do design minimal extension points
- Keep current code clean and simple
- Document intent in code comments

## Output
- Extension point design
- Code changes needed (minimal)
- Documentation of future use
- Cost/benefit analysis

Show me extension point design before implementing."
```

---

## Vision Documentation Patterns

### Pattern: Write Vision Document

```markdown
"Write vision document for [capability]:

## Structure (follow CAPABILITY_EVOLUTION.example.md)

### Wave Overview
- Wave number and name
- Strategic objective
- Success criteria
- Time horizon (relative, not dates)

### Capabilities
For each capability:
- Name and purpose
- User value (problem solved)
- Technical approach (high-level)
- Dependencies (what must exist first)
- Effort estimate (T-shirt size)

### Architecture Evolution
- What changes to architecture?
- What extension points needed?
- What technical debt to address?

### Success Metrics
- How do we measure success?
- What's the target outcome?
- What KPIs track progress?

### Risks and Unknowns
- What could go wrong?
- What don't we know yet?
- What assumptions are we making?

## Tone
- Exploratory, not committal
- Use "might", "could", "if"
- Present options, not decisions

Generate vision document draft."
```

### Pattern: Update Vision Based on Learnings

```markdown
"Update vision documents based on Wave [X] learnings:

## Learnings from Wave [X]
1. What we learned about users
2. What we learned about technology
3. What we learned about process
4. What assumptions were wrong

## Vision Impact
1. Review vision documents (dev-docs/vision/)
2. What capabilities are more/less valuable now?
3. What technical approaches changed?
4. What timelines shifted?

## Updates Needed
1. Revise vision documents
2. Adjust wave planning
3. Update capability priorities
4. Document reasoning for changes

Show me vision update recommendations."
```

---

## Ecosystem Vision Work

### Pattern: Research Integration Approach

```markdown
"Research integration with [external_system]:

## Context
- Vision: Ecosystem integration (Wave 4)
- Current: Wave 1.x (standalone)
- External system: [name and purpose]

## Research Questions
1. What value does integration provide?
2. What's the technical approach?
3. What dependencies exist?
4. What risks are involved?
5. What's the effort estimate?

## Deliverables
1. Integration research document (dev-docs/research/)
2. Proof-of-concept (if needed)
3. Architecture proposal
4. Recommendation (build now/later/never)

## Constraints
- Don't build integration now (not committed)
- Do validate feasibility
- Do inform architecture decisions
- Do document learnings

Create research plan."
```

---

## Strategic Decision Framework

### Pattern: Make/Defer/Never Decision

```markdown
"Evaluate capability for build decision:

Capability: [name]
Source: [vision document, user request, technical need]

## Evaluation Framework

### Make (Build Now)
Criteria:
- High user value (solves major pain)
- Technically ready (architecture supports)
- Strategic priority (aligns with vision)
- Resource available (team has capacity)

### Defer (Plan for Future Wave)
Criteria:
- Medium user value (nice to have)
- Technical gaps (need foundation first)
- Strategic fit (aligns with vision)
- Resource constrained (no capacity now)

### Never (Explicitly Not Building)
Criteria:
- Low user value (minimal demand)
- Poor strategic fit (off-mission)
- Technical constraints (can't build)
- Maintenance burden (too costly)

## Recommendation
Decision: [Make/Defer/Never]
Wave: [if Defer, which wave?]
Reasoning: [why this decision?]

Provide decision with clear reasoning."
```

---

## Vision Review Cadence

### Pattern: Quarterly Vision Review

```markdown
"Quarterly vision review (Q[N] 202[Y]):

## Review Process
1. **Load full context** (200k advantage)
   - All vision documents
   - All completed waves
   - Current architecture
   - User feedback
   - Market changes

2. **Evaluate assumptions**
   - What assumptions were made last quarter?
   - Which proved true/false?
   - What new information exists?

3. **Adjust priorities**
   - Capability priority changes?
   - Timeline shifts?
   - New opportunities?
   - Deprecated ideas?

4. **Update vision documents**
   - Revise based on learnings
   - Add new capabilities
   - Remove invalidated ideas
   - Update wave planning

## Output
- Updated vision documents
- Revised wave priorities
- Strategic recommendations
- Next quarter focus

Provide comprehensive quarterly review."
```

---

## Best Practices for Vision Work

### ✅ Do's

1. **Think long-term** - Multi-wave perspective (2-3 years)
2. **Keep options open** - Design for flexibility
3. **Document reasoning** - Why decisions were made
4. **Use vision context** - Inform current architecture
5. **Stay exploratory** - Don't commit prematurely
6. **Validate assumptions** - Test with users/POCs
7. **Revise regularly** - Quarterly vision reviews
8. **Separate vision/roadmap** - Clear boundaries

### ❌ Don'ts

1. **Don't implement vision now** - Not committed features
2. **Don't treat as roadmap** - Vision is exploratory
3. **Don't ignore learnings** - Update based on data
4. **Don't over-specify** - Keep high-level
5. **Don't commit timelines** - Use wave-relative
6. **Don't ignore architecture** - Vision must be feasible
7. **Don't forget users** - Validate assumptions
8. **Don't set and forget** - Review quarterly

---

## Resources

### Vision Documents (This Directory)
- **[MCP_CONFIG_ORCHESTRATION.md](MCP_CONFIG_ORCHESTRATION.md)** - Core product vision
- **[MCP_SERVER_SPEC.md](MCP_SERVER_SPEC.md)** - MCP protocol specification
- **[CAPABILITY_EVOLUTION.example.md](CAPABILITY_EVOLUTION.example.md)** - Wave planning template
- **[ecosystem-intent.md](ecosystem-intent.md)** - Ecosystem vision
- **[README.md](README.md)** - Vision documents overview

### Committed Work
- **[../../ROADMAP.md](../../ROADMAP.md)** - Committed roadmap (not vision)
- **[../../project-docs/WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md)** - Current wave plan

### Parent Guides
- **[../../CLAUDE.md](../../CLAUDE.md)** - Project-level Claude patterns
- **[../CLAUDE.md](../CLAUDE.md)** - Development guide
- **[AGENTS.md](AGENTS.md)** - Generic vision guide

### Related Guides
- **[../research/CLAUDE.md](../research/CLAUDE.md)** - Research patterns

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
