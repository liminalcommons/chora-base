# Related Work Template Content Block

## Description

Optional field referencing related coordination requests, SAPs, issues, or other work that provides context or benefits from this request. Unlike dependencies (blocking prerequisites), related work has **informational** value - it influences thinking, shares context, or creates synergies, but doesn't block progress.

**When to use**: Coordination requests that connect to broader initiatives, build on prior work, or enable future efforts. Common in ecosystem coordination (~50-60%), less common in standalone requests.

## Fields / Structure

```json
{
  "related": [
    "Reference to related work item 1",
    "Reference to related work item 2"
  ]
}
```

### Field Specifications

- **related**: Array of strings (optional, ~30-50% of requests)
- Each string references one related item
- Should be specific (request IDs, SAP versions, issue numbers)
- May include brief description of relationship
- Can reference past work (context) or future work (enablement)

## Template / Example

```json
{
  "related": [
    "{{related_item_1}} ({{relationship_description}})",
    "{{related_item_2}} ({{relationship_description}})"
  ]
}
```

## Variation Points

### Prior Work (Context and Foundations)

References work that informed or enabled this request:

```json
{
  "related": [
    "SAP-017 chora-compose documentation standards (informed our understanding of chora-compose)",
    "SAP-018 ecosystem integration patterns (provided integration context)",
    "COORD-2025-001 infrastructure audit (identified automation opportunities)",
    "GitHub Issue #234 inbox automation discussion (community feedback on manual process pain)"
  ]
}
```

**Characteristics**:
- Past work that influenced current request
- Provides historical context
- May explain why this approach was chosen
- Helps recipient understand evolution

### Parallel Work (Shared Context)

References concurrent work in related areas:

```json
{
  "related": [
    "COORD-2025-003 chora-workspace SAP adoption (parallel ecosystem integration effort)",
    "SAP-010 ecosystem coordination framework (being developed concurrently)",
    "chora-compose Issue #47 content config improvements (upstream work we're monitoring)"
  ]
}
```

**Characteristics**:
- Work happening in parallel (not blocking)
- Shares context or goals
- May create collaboration opportunities
- Helps identify potential conflicts or synergies

### Future Work (Enablement)

References work that this request will enable:

```json
{
  "related": [
    "SAP-011 task automation (future - will use same chora-compose infrastructure)",
    "COORD-2025-005 proposal generation (future - benefits from content block library)",
    "Ecosystem-wide artifact automation (vision - shared content blocks across repos)"
  ]
}
```

**Characteristics**:
- Future work enabled by current request
- Demonstrates strategic value
- May inform scope decisions (build for future reuse)
- Helps recipient see broader impact

### Cross-Repository References

References work in other repositories:

```json
{
  "related": [
    "chora-workspace COORD-WS-012 SAP generation (similar use case, different repo)",
    "ecosystem-manifest Issue #89 artifact standardization (ecosystem coordination)",
    "chora-compose PR #156 MCP integration improvements (upstream enhancement)"
  ]
}
```

**Characteristics**:
- References external repositories
- May require different ID formats (COORD-WS-012, PR #156)
- Demonstrates ecosystem awareness
- Facilitates cross-repo collaboration

### No Related Work

Many requests have no significant related work to reference:

```json
{
  "related": null
}
```
*Note: Field omitted entirely*

**When to omit**:
- Standalone request with no significant connections
- First request in new area (no prior work)
- Related work too obvious (everyone knows about it)
- Simple, narrow-scope requests

## Usage Guidance

### Relationship Types

**Informed By** (past work provided context):
```
"SAP-017 (informed our understanding of chora-compose architecture)"
```

**Builds On** (extends prior work):
```
"COORD-2025-002 exploration (builds on feasibility findings)"
```

**Parallel To** (concurrent, related work):
```
"SAP-010 ecosystem coordination (parallel effort, shares goals)"
```

**Enables** (makes future work possible):
```
"SAP-011 task automation (future - will reuse content block infrastructure)"
```

**Complements** (works together synergistically):
```
"SAP-004 quality framework (complements with evaluation criteria)"
```

**References** (cites or draws from):
```
"chora-compose documentation (references MCP integration patterns)"
```

### Specificity

**Good** (specific and actionable):
```json
{
  "related": [
    "SAP-001 v1.0.0 inbox protocol (establishes schemas being automated)",
    "COORD-2025-002 exploration phase (feasibility analysis that led to this pilot)",
    "SAP-004 quality framework (will be used for 80% threshold evaluation)",
    "chora-workspace COORD-WS-012 (similar SAP generation use case)"
  ]
}
```

**Poor** (vague and unhelpful):
```json
{
  "related": [
    "Some other SAPs",
    "Prior work on related topics",
    "Future plans"
  ]
}
```

### Ordering Strategy

**Chronological** (past → present → future):
```json
{
  "related": [
    "SAP-017 documentation standards (2025-Q3 - past context)",
    "COORD-2025-002 exploration (2025-11-01 - recent foundation)",
    "This pilot (2025-11 to 2025-12 - current work)",
    "SAP-011 task automation (2026-Q1 - future enablement)"
  ]
}
```

**By Relationship Type**:
```json
{
  "related": [
    "Builds on: COORD-2025-002 exploration",
    "Parallel to: chora-workspace COORD-WS-012",
    "Enables: SAP-011 task automation",
    "Complements: SAP-004 quality framework"
  ]
}
```

**By Importance**:
```json
{
  "related": [
    "SAP-001 inbox protocol (critical context)",
    "COORD-2025-002 exploration (direct foundation)",
    "SAP-017 chora-compose docs (background reading)",
    "GitHub Issue #234 (community discussion)"
  ]
}
```

### Quantity Guidelines

**Too few** (<2 when connections exist):
```json
{
  "related": [
    "SAP-001 inbox protocol"
  ]
}
```
**Issue**: Missing valuable context (exploration phase, quality framework, etc.)

**Too many** (>10):
```json
{
  "related": [
    "SAP-001", "SAP-002", "SAP-003", "SAP-004", "SAP-005",
    "SAP-006", "SAP-007", "SAP-008", "SAP-009", "SAP-010",
    "COORD-2025-001", "COORD-2025-002", "..."
  ]
}
```
**Issue**: Information overload, unclear which are most relevant.

**Just right** (3-7):
```json
{
  "related": [
    "SAP-001 inbox protocol (schemas being automated)",
    "CORD-2025-002 exploration (feasibility foundation)",
    "SAP-004 quality framework (evaluation criteria)",
    "chora-workspace COORD-WS-012 (parallel SAP generation)",
    "SAP-011 task automation (future - will reuse infrastructure)"
  ]
}
```
**Benefit**: Key connections highlighted, recipient can explore if interested.

### Related vs Dependencies

**Dependencies** (blocking prerequisites):
```json
{
  "dependencies": [
    "SAP-001 v1.0.0 (completed - MUST have schemas before automation)",
    "Exploration COORD-2025-002 (completed - MUST validate feasibility)"
  ]
}
```

**Related** (informational, non-blocking):
```json
{
  "related": [
    "SAP-017 documentation (informed our understanding, not blocking)",
    "SAP-011 future automation (will benefit, not required now)",
    "chora-workspace COORD-WS-012 (parallel work, shares context)"
  ]
}
```

**Key difference**: Dependencies block progress if incomplete; related work adds context but doesn't block.

### Automation Notes

- **AI Detection**: Can extract related work from context.background and deliverables
- **Link Validation**: Check if referenced items exist (SAPs in catalog, requests in inbox)
- **Relationship Inference**: AI can suggest relationship type (builds on, enables, etc.)
- **Quantity Curation**: AI can prioritize most relevant 3-7 items if many connections exist

## Validation Rules

- `related` field is **optional** (omit if no significant related work)
- If present, must be array of strings
- Each item should reference specific artifact (SAP version, request ID, issue number)
- Recommended 2-8 items (avoid empty array or excessive list)
- Should not duplicate dependencies (dependencies have stronger blocking relationship)
- Links should be valid (or marked as future/external if not yet created)

## Related Content Blocks

- [dependencies-pattern.md](dependencies-pattern.md) - Blocking prerequisites (stronger relationship)
- [context-background.md](context-background.md) - May reference related work narratively
- [trace-id-format.md](trace-id-format.md) - Alternative way to group related work

## Examples from Real Requests

### Example 1: Prescriptive Request (COORD-2025-004)

```json
{
  "related": [
    "SAP-009 v1.0.0 (foundation being extended to v1.1.0)",
    "chora-workspace coordination discussions (identified bidirectional need)",
    "ecosystem-manifest integration requirements (external format specifications)",
    "SAP-010 ecosystem coordination framework (will use bidirectional translation)",
    "COORD-2025-002 chora-compose exploration (parallel automation effort)"
  ]
}
```

**Analysis**:
- 5 related items (good quantity)
- Mix of SAPs (v1.0.0, SAP-010), coordination (chora-workspace, ecosystem-manifest), and parallel work (COORD-2025-002)
- Brief relationship descriptions in parentheses
- Shows ecosystem awareness and strategic thinking

### Example 2: Exploratory Request (COORD-2025-002)

```json
{
  "related": [
    "SAP-001 v1.0.0 inbox coordination protocol (schemas being considered for automation)",
    "SAP-017 chora-compose documentation standards (initial understanding of chora-compose)",
    "SAP-018 ecosystem integration patterns (integration best practices)",
    "SAP-004 SAP generation pilot framework (quality evaluation approach if pilot proceeds)",
    "GitHub Issue #234 inbox automation discussion (community feedback on manual process)",
    "chora-workspace COORD-WS-012 SAP generation (similar use case, potential content block sharing)"
  ]
}
```

**Analysis**:
- 6 related items (comprehensive but not overwhelming)
- Multiple SAPs (001, 017, 018, 004) provide strategic context
- GitHub issue shows community input
- Cross-repo reference (chora-workspace) demonstrates ecosystem thinking
- Each item has relationship description

### Example 3: Peer Review Request (coord-005)

```json
{
  "related": [
    "SAP-020 through SAP-025 (React SAPs being reviewed)",
    "chora-base SAP catalog (standards and patterns for comparison)",
    "SAP-001 inbox coordination protocol (example of well-structured SAP)"
  ]
}
```

**Analysis**:
- 3 related items (focused on review context)
- References SAPs being reviewed (SAP-020-025)
- Points to comparison baseline (SAP catalog, SAP-001)
- Minimal but sufficient for peer review context

### Example 4: No Related Work (Hypothetical Emergency)

```json
{
  "related": null
}
```
*Note: Field omitted entirely*

**Context**: Emergency P0 coordination request to fix production issue
**Rationale**: No time for related work references, focus on immediate fix

## Common Patterns by Request Type

| Request Type | Related Items | Focus | Examples |
|--------------|---------------|-------|----------|
| Exploratory | 4-7 | Context, prior art, evaluation frameworks | SAPs, explorations, quality frameworks |
| Prescriptive | 3-6 | Foundations, parallel work, future enablement | Prior versions, ecosystem needs, future work |
| Peer Review | 2-4 | Items being reviewed, comparison standards | SAPs under review, catalog, exemplars |
| Emergency (P0) | 0-2 | Root cause, incident tracking | Incident reports, related outages |

## Related Work and Trace IDs

For multi-phase projects, related work often shares a trace_id:

```json
{
  "request_id": "COORD-2025-004",
  "trace_id": "chora-compose-inbox-integration-2025",
  "related": [
    "COORD-2025-002 exploration (shares trace_id: chora-compose-inbox-integration-2025)",
    "Pilot plan document (shares trace_id, generated from COORD-2025-002)",
    "SAP-001 inbox protocol (related context, different trace_id)"
  ]
}
```

**Benefit**: trace_id enables automated grouping; related field provides explicit narrative.

## Value of Related Work References

**For Recipients**:
- Understand broader context and motivation
- Identify collaboration opportunities
- See strategic vision beyond immediate request
- Discover relevant prior art

**For Requesters**:
- Demonstrate thorough research
- Show ecosystem awareness
- Build case for strategic importance
- Enable future work discovery

**For Ecosystem**:
- Create knowledge graph of connected work
- Facilitate cross-repo collaboration
- Enable impact tracking (what did this request enable?)
- Support discoverability (find all work related to topic X)

## Metadata

- **Priority**: MEDIUM (valuable in 30-50% of requests, especially ecosystem coordination)
- **Stability**: Stable (rarely changes, though new related work may emerge later)
- **Reusability**: Universal (identical pattern in tasks, proposals, and strategic planning)
- **Generation Source**: AI extraction from context + catalog/inbox search, user curation
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
