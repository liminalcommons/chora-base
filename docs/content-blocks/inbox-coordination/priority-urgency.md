# Priority and Urgency Content Block

## Description

Two orthogonal dimensions for scheduling coordination requests: **priority** (importance/impact) and **urgency** (time sensitivity). Priority indicates the strategic significance of the request, while urgency indicates when action is needed. These fields drive triage, scheduling, and resource allocation.

**When to use**: Every coordination request to enable proper scheduling and resource planning.

## Fields / Structure

```json
{
  "priority": "P0 | P1 | P2",
  "urgency": "blocks_sprint | next_sprint | backlog"
}
```

### Field Specifications

#### Priority (Importance/Impact)

- **P0 (Critical)**:
  - Blocks major deliverables or causes ecosystem-wide impact
  - Requires immediate attention regardless of current work
  - Typically involves security issues, breaking changes, or showstopper bugs
  - Rarely used for coordination requests (more common in tasks)

- **P1 (High)**:
  - Significant impact on goals or roadmap
  - Should be addressed in current or next sprint
  - Typical for prescriptive requests with concrete deliverables
  - May block future work if not addressed

- **P2 (Normal)**:
  - Standard priority for most requests
  - Important but not urgent
  - Typical for exploratory requests, peer reviews, and backlog items
  - Can be scheduled based on capacity

#### Urgency (Time Sensitivity)

- **blocks_sprint**:
  - Actively blocking current sprint work
  - Needs resolution within days (not weeks)
  - High coordination overhead acceptable
  - Typically paired with P0 or P1

- **next_sprint**:
  - Needed for upcoming sprint (within 2-4 weeks)
  - Should start planning/discussion soon
  - Typical for prescriptive requests
  - Often paired with P1

- **backlog**:
  - No immediate time pressure
  - Can be scheduled based on capacity and priorities
  - Typical for exploratory requests and peer reviews
  - Usually paired with P2, sometimes P1

## Template / Example

```json
{
  "priority": "{{priority_level}}",
  "urgency": "{{urgency_level}}"
}
```

## Variation Points

### Common Pairings

**P0 + blocks_sprint**: Emergency situation
- Security vulnerability requiring immediate ecosystem coordination
- Breaking change discovered in production
- Rare for coordination requests (usually handled as tasks)

**P1 + next_sprint**: High-value upcoming work
- Prescriptive request for feature needed in upcoming release
- Cross-repo integration required for roadmap milestone
- Most common for internal coordination with concrete deliverables

**P1 + backlog**: Important but flexible timeline
- Strategic exploration with high potential impact
- Peer review of significant work (not blocking release)
- Common for exploratory requests to external repos

**P2 + backlog**: Standard exploratory request
- Information gathering and relationship building
- Peer reviews without time pressure
- Most common for ecosystem coordination

**P2 + next_sprint**: Modest priority, time-sensitive
- Small request needed for specific deadline
- Follow-up coordination on existing work
- Less common combination

## Usage Guidance

### Priority Selection

Ask: "What happens if this request is not addressed?"

- **P0**: System breaks, security compromised, ecosystem blocked → **Use P0**
- **P1**: Key goals delayed, significant rework needed, multiple dependencies impacted → **Use P1**
- **P2**: Minor delays, nice-to-have improvements, single-team impact → **Use P2**

### Urgency Selection

Ask: "When does this need to be done?"

- **blocks_sprint**: Right now (days) → **Use blocks_sprint**
- **next_sprint**: Soon (2-4 weeks) → **Use next_sprint**
- **backlog**: Eventually (months, or capacity-dependent) → **Use backlog**

### Anti-Patterns

**DON'T**:
- Mark everything P0 or P1 (creates priority inflation)
- Use blocks_sprint for requests that don't actually block current work
- Use P2 + blocks_sprint (contradictory: if it blocks, it's not P2)
- Change priority/urgency frequently (indicates poor initial assessment)

**DO**:
- Be honest about impact and timeline
- Consider recipient's capacity (external repos may not accept P0 requests)
- Use P2 + backlog for exploratory work (even if high interest)
- Escalate priority if context changes (with justification)

### Triage Implications

Processing order (rough guideline):
1. P0 + blocks_sprint (immediate)
2. P1 + blocks_sprint (same day)
3. P0 + next_sprint (this week)
4. P1 + next_sprint (within 2 weeks)
5. P2 + blocks_sprint (reassess: should be P1)
6. P1 + backlog (scheduled based on capacity)
7. P2 + next_sprint (fill-in work)
8. P2 + backlog (backlog review cycle)

### Automation Notes

- **Default**: If not specified, assume `"priority": "P2", "urgency": "backlog"`
- **AI Inference**: Can suggest priority/urgency from context, but user should confirm
- **Validation**: Check for contradictory pairings (P2 + blocks_sprint)
- **Escalation**: Scripts can flag P0 requests for immediate notification

## Validation Rules

- Both fields are **required**
- `priority` must be one of: `"P0"`, `"P1"`, `"P2"`
- `urgency` must be one of: `"blocks_sprint"`, `"next_sprint"`, `"backlog"`
- Warn (but don't block) on unusual pairings: `P2 + blocks_sprint`, `P0 + backlog`

## Related Content Blocks

- [core-metadata.md](core-metadata.md) - Request identification
- [timeline-patterns.md](timeline-patterns.md) - Specific deadline language
- [estimated-effort-guide.md](estimated-effort-guide.md) - Effort required to address request

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)
```json
{
  "priority": "P2",
  "urgency": "backlog"
}
```
**Rationale**: Exploration of potential integration. High interest but no blocking dependencies. Can be scheduled based on both teams' capacity.

### Example 2: Prescriptive Request (COORD-2025-004)
```json
{
  "priority": "P1",
  "urgency": "next_sprint"
}
```
**Rationale**: Implementation of bidirectional translation layer needed for SAP-009 release. Significant impact, concrete timeline, internal coordination.

### Example 3: Peer Review Request (coord-005)
```json
{
  "priority": "P1",
  "urgency": "backlog"
}
```
**Rationale**: Important peer review for ecosystem alignment, but not blocking any releases. High value, flexible timeline.

## Decision Matrix

| Priority | Urgency | Typical Use Case | Response Time | Example |
|----------|---------|------------------|---------------|---------|
| P0 | blocks_sprint | Emergency | Hours | Security vulnerability coordination |
| P0 | next_sprint | Critical upcoming | 1-2 days | Breaking change migration needed soon |
| P0 | backlog | (Rare) | 1 week | Critical but blocked by dependencies |
| P1 | blocks_sprint | High-value blocker | 1-2 days | Integration needed for current sprint |
| P1 | next_sprint | Planned important work | 1 week | Feature for upcoming release |
| P1 | backlog | Important, flexible | 2-4 weeks | Strategic exploration, peer review |
| P2 | blocks_sprint | (Reassess) | 1-2 days | Should probably be P1 |
| P2 | next_sprint | Small time-sensitive | 1 week | Minor update for specific deadline |
| P2 | backlog | Standard request | 4+ weeks | Exploratory, nice-to-have |

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Semi-stable (may be escalated if context changes)
- **Reusability**: Universal (identical pattern in tasks and proposals)
- **Generation Source**: AI inference from context, user confirmation recommended
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
