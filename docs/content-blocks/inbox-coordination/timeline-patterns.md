# Timeline Patterns Content Block

## Description

Optional field specifying specific dates, milestones, or temporal constraints for a coordination request. Unlike priority/urgency (relative scheduling), timeline provides **absolute dates** or **milestone dependencies**. Useful when work must align with releases, events, or external commitments.

**When to use**: Coordination requests with hard deadlines, release coordination, or milestone dependencies. Less common than priority/urgency (~30-40% of requests) but critical when present.

## Fields / Structure

```json
{
  "timeline": "Description of deadlines, milestones, or temporal constraints"
}
```

### Field Specifications

- **timeline**: String (optional, ~30-40% of requests)
- Specifies absolute dates (YYYY-MM-DD) or milestone names
- Complements priority/urgency (urgency = relative, timeline = absolute)
- May include dependencies ("after X", "before Y release")
- Flexible format (narrative or structured)

## Template / Example

```json
{
  "timeline": "{{deadline_or_milestone_description}}"
}
```

## Variation Points

### Hard Deadline (Date-Specific)

Specific date by which work must be completed:

```json
{
  "timeline": "Needed by 2025-11-22 for Q4 ecosystem integration release"
}
```

**Characteristics**:
- Absolute date (YYYY-MM-DD format)
- Reason for deadline included (release, event, commitment)
- Pairs with urgency: "next_sprint" for 2-4 weeks out, "blocks_sprint" for <1 week

### Milestone Dependency

Work must complete before/after specific milestone:

```json
{
  "timeline": "Must complete before SAP-009 v1.1.0 release (planned for 2025-11-15). Blocks SAP-010 implementation which depends on bidirectional translation."
}
```

**Characteristics**:
- References specific milestone/release
- Includes milestone date when known
- Explains dependency chain
- Helps recipient understand broader context

### Phased Timeline

Multi-phase request with per-phase timelines:

```json
{
  "timeline": "Phase 1 (Exploration): 2025-11-01 to 2025-11-08\nPhase 2 (Pilot): 2025-11-09 to 2025-12-06 (if Phase 1 GO decision)\nPhase 3 (Implementation): 2025-12-07 to 2026-01-03 (if pilot successful)"
}
```

**Characteristics**:
- Breaks timeline into phases
- Each phase has date range
- Later phases conditional on earlier success
- Typical for exploratory → pilot → implementation workflows

### Flexible Timeline (No Hard Deadline)

Preferred timeframe without strict deadline:

```json
{
  "timeline": "Preferred completion by end of Q4 2025 (2025-12-31), but flexible if capacity constraints exist. No hard blocker, but would enable earlier ecosystem adoption."
}
```

**Characteristics**:
- Target date with flexibility noted
- Acknowledges recipient capacity
- Explains benefit of earlier completion
- Pairs with "backlog" urgency

### No Timeline

Many requests omit timeline field:

```json
{
  "timeline": null
}
```
*Note: Field omitted entirely*

**When to omit**:
- priority/urgency sufficient for scheduling
- No external dependencies or deadlines
- Flexible, capacity-driven work
- Most exploratory and peer review requests

## Usage Guidance

### Timeline vs Urgency

**Urgency** (relative scheduling):
- `blocks_sprint`: Needed within days
- `next_sprint`: Needed within 2-4 weeks
- `backlog`: Needed eventually, capacity-driven

**Timeline** (absolute scheduling):
- `"Needed by 2025-11-22"`: Specific date
- `"Before v2.0.0 release"`: Milestone-relative
- `"Q4 2025 preferred"`: Time window

**Use both when helpful**:
```json
{
  "urgency": "next_sprint",
  "timeline": "Needed by 2025-11-22 for Q4 release"
}
```
This gives recipient both relative priority (next 2-4 weeks) and absolute deadline (specific date).

### Date Formatting

**Preferred**: ISO 8601 format `YYYY-MM-DD`
- Unambiguous internationally
- Sortable and parseable
- Examples: `2025-11-22`, `2025-12-31`

**Acceptable**: Month names for readability
- "November 22, 2025" or "22 Nov 2025"
- Use when audience is human-focused (not machine-parsed)

**Avoid**: Ambiguous formats
- `11/22/25` (US) vs `22/11/25` (EU) → confusion
- `11/22/2025` → is it Nov 22 or 22 Nov?

### Timeline Justification

Always explain **why** the timeline matters:

**Good** (context provided):
```json
{
  "timeline": "Needed by 2025-11-22 for Q4 ecosystem integration release, which multiple downstream repos depend on"
}
```

**Poor** (arbitrary deadline):
```json
{
  "timeline": "Needed by 2025-11-22"
}
```

**Benefit**: Recipient can assess whether deadline is negotiable or firm.

### Flexible vs Firm Deadlines

**Firm deadline** (non-negotiable):
```json
{
  "timeline": "MUST complete by 2025-11-15 - conference demo on 2025-11-16, cannot reschedule"
}
```

**Flexible deadline** (preferred but negotiable):
```json
{
  "timeline": "Preferred by 2025-11-30 for Q4 OKRs, but can slip to Q1 2026 if needed"
}
```

**Conditional deadline** (depends on decision):
```json
{
  "timeline": "If GO decision by 2025-11-08, pilot would run 2025-11-09 to 2025-12-06. DEFER decision would push to Q1 2026."
}
```

### Buffer and Contingency

Include buffer for recipient planning:

**Tight** (no buffer):
```json
{
  "timeline": "Needed by 2025-11-15 for release on 2025-11-15"
}
```
**Risk**: No time for unexpected issues.

**Buffered** (recommended):
```json
{
  "timeline": "Needed by 2025-11-10 for release on 2025-11-15 (5-day integration buffer)"
}
```
**Benefit**: Recipient can absorb minor delays without missing release.

### Timeline for Recurring Work

For ongoing or phased work:

```json
{
  "timeline": "Initial review by 2025-11-15, follow-up iteration by 2025-11-30, final approval by 2025-12-15"
}
```

This gives recipient checkpoints and enables incremental progress tracking.

### Automation Notes

- **AI Generation**: Can infer timeline from context (mentions of releases, events)
- **Date Parsing**: Extract dates and validate format (YYYY-MM-DD preferred)
- **Urgency Correlation**: Check timeline vs urgency consistency (e.g., deadline in 3 days but urgency=backlog is inconsistent)
- **Buffer Suggestion**: AI can recommend buffer based on estimated_effort and deadline

## Validation Rules

- `timeline` field is **optional** (omit if no specific deadline/milestone)
- If present, should include at least one date or milestone reference
- Dates should use YYYY-MM-DD format when possible
- Should explain reason for timeline (not just arbitrary date)
- Should indicate flexibility (firm vs preferred vs conditional)

## Related Content Blocks

- [priority-urgency.md](priority-urgency.md) - Relative scheduling (complements timeline)
- [estimated-effort-guide.md](estimated-effort-guide.md) - Effort required (timeline ÷ effort = bandwidth needed)
- [dependencies-pattern.md](dependencies-pattern.md) - Prerequisite work that affects timeline

## Examples from Real Requests

### Example 1: Exploratory Request with Phased Timeline (COORD-2025-002)

```json
{
  "timeline": "Phase 1 (Exploration): 2025-11-01 to 2025-11-08\nGO/NO-GO decision: 2025-11-08\nPhase 2 (Pilot): 2025-11-09 to 2025-12-06 (if GO)\nPilot decision: 2025-12-06\nPhase 3 (Implementation): TBD based on pilot results"
}
```

**Analysis**:
- Multi-phase timeline with decision points
- Specific dates for each phase (ISO 8601)
- Conditional phases (if GO, if pilot successful)
- Phase 3 deliberately TBD (depends on learnings)
- Enables recipient to plan capacity per phase

### Example 2: Prescriptive Request with Release Deadline (COORD-2025-004)

```json
{
  "timeline": "Needed by 2025-11-15 for SAP-009 v1.1.0 release, which unblocks chora-workspace and ecosystem-manifest integration (blocked since 2025-10-20)"
}
```

**Analysis**:
- Firm deadline (2025-11-15)
- Reason provided (release, unblocks integrations)
- Context on blocker duration (blocked since Oct 20)
- Helps recipient assess urgency and prioritize

### Example 3: Peer Review Request without Timeline (coord-005)

```json
{
  "timeline": null
}
```
*Note: Field omitted entirely*

**Analysis**:
- No hard deadline for peer review
- urgency: "backlog" indicates flexible timing
- Appropriate when review can happen as capacity allows
- Recipient can schedule based on availability

### Example 4: Flexible Timeline (Hypothetical)

```json
{
  "timeline": "Preferred completion by 2025-12-31 (end of Q4) for ecosystem integration OKRs, but no hard blocker if it slips to Q1 2026. Earlier completion enables more repos to integrate in Q4."
}
```

**Analysis**:
- Target date with flexibility noted (2025-12-31)
- Explains context (Q4 OKRs)
- Acknowledges alternative (Q1 2026 acceptable)
- Describes benefit of earlier completion (ecosystem adoption)

## Common Patterns by Request Type

| Request Type | Timeline Pattern | Example | Frequency |
|--------------|------------------|---------|-----------|
| Exploratory | Phased with decision points | "Exploration: Nov 1-8, Pilot: Nov 9-Dec 6 (if GO)" | 30-40% |
| Prescriptive | Release-aligned | "Needed by Nov 15 for v1.1.0 release" | 60-70% |
| Peer Review | Often omitted | Field not present | 70-80% (capacity-driven) |
| Emergency (P0) | Immediate | "Needed by [today/tomorrow] to unblock production" | 90%+ |

## Timeline and Priority/Urgency Matrix

Understanding how timeline relates to priority/urgency:

| Timeline | Priority | Urgency | Implication |
|----------|----------|---------|-------------|
| 3 days away | P0-P1 | blocks_sprint | Drop everything, all hands |
| 2 weeks away | P1 | next_sprint | Schedule in current/next sprint |
| 1 month away | P1 | next_sprint | Include in upcoming sprint planning |
| 3 months away | P1-P2 | backlog | Backlog, but watch calendar |
| Flexible/none | P2 | backlog | Capacity-driven scheduling |
| Flexible/none | P1 | backlog | Important but no hard deadline |

## Metadata

- **Priority**: MEDIUM (valuable in 30-40% of requests, critical when present)
- **Stability**: Semi-stable (may adjust during scoping, but deadlines rarely move)
- **Reusability**: Universal (identical pattern in tasks, proposals, and project planning)
- **Generation Source**: AI extraction from context mentions of dates/releases, user confirmation
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
