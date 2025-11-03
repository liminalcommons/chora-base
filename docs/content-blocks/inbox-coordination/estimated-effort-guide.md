# Estimated Effort Guide Content Block

## Description

Requester's estimate of effort required to address the coordination request. Helps recipients understand scope, plan capacity, and assess feasibility. Effort estimates set expectations and enable informed triage decisions. This is the **requester's perspective** (not binding commitment from recipient).

**When to use**: Coordination requests where effort estimation is valuable for planning. Common in prescriptive requests (specific deliverables) and helpful in exploratory requests (scoping). Less common in peer reviews (effort varies by reviewer).

## Fields / Structure

```json
{
  "estimated_effort": "N-M hours" | "N-M days" | "N-M weeks"
}
```

### Field Specifications

- **estimated_effort**: String (optional, present in ~67% of analyzed requests)
- Format: `"N-M {hours|days|weeks}"` where N < M
- Represents **range** not single point (acknowledges uncertainty)
- From requester's perspective (what they think is needed)
- Typically includes breakdown by deliverable in context if detailed

## Template / Example

```json
{
  "estimated_effort": "{{low_estimate}}-{{high_estimate}} {{time_unit}}"
}
```

## Variation Points

### Prescriptive Requests (Detailed Estimates)

Most specific form with per-deliverable breakdown:

```json
{
  "estimated_effort": "40-60 hours",
  "context": {
    "effort_breakdown": "Estimated effort breakdown:\n- SAP-009 v1.1.0 specification: 8-12 hours\n- Implementation in scripts/: 15-20 hours\n- Test suite (≥80% coverage): 10-15 hours\n- Documentation updates: 4-6 hours\n- Integration testing: 3-5 hours\n\nTotal: 40-58 hours (rounded to 40-60 hours for estimation buffer)"
  }
}
```

**Characteristics**:
- Specific range (40-60 hours)
- Per-deliverable breakdown in context
- Acknowledges uncertainty (ranges per item)
- Includes buffer (40-58 → 40-60)
- Hour-level precision for 1-2 week efforts

### Exploratory Requests (Phase-Based Estimates)

Estimates for multi-phase exploration:

```json
{
  "estimated_effort": "12-18 hours",
  "context": {
    "effort_breakdown": "Exploration phase: 12-18 hours total\n- Research chora-compose architecture: 3-5 hours\n- Map SAP-001 schemas to content configs: 4-6 hours\n- Prototype 1-2 content configs: 3-5 hours\n- Document findings and recommendations: 2-3 hours\n\nIf exploration leads to pilot, additional 28-42 hours estimated (documented in pilot plan)."
  }
}
```

**Characteristics**:
- Current phase estimate (12-18 hours)
- Phase breakdown (research, map, prototype, document)
- Future phase estimate mentioned (28-42 hours pilot)
- Hour-level precision appropriate for exploration

### Peer Review Requests (Reviewer Effort)

Estimates for review time required:

```json
{
  "estimated_effort": "4-8 hours",
  "context": {
    "effort_breakdown": "Estimated review effort:\n- Initial read-through of 6 SAPs: 2-3 hours\n- Comparison with chora-base patterns: 1-2 hours\n- Documentation of recommendations: 1-2 hours\n- Follow-up discussion (if needed): 0-1 hour"
  }
}
```

**Characteristics**:
- Reviewer perspective (not requester implementation effort)
- Hour-level precision (short review)
- Includes contingency (0-1 hour follow-up)
- Conservative estimate (respects reviewer time)

### No Estimate

Some requests omit estimated_effort:

```json
{
  "estimated_effort": null
}
```
*Note: Field omitted entirely in actual request*

**When to omit**:
- Effort highly variable or unknown
- Emergency requests (effort estimation less important than urgency)
- Open-ended exploration (scope unclear)
- Simple requests (effort obvious)

## Usage Guidance

### Unit Selection

**Hours** (1-40 hour range):
- Short tasks or explorations
- Detailed, well-scoped work
- Single-sprint efforts
- Example: `"4-8 hours"`, `"15-25 hours"`

**Days** (2-10 day range):
- Medium-sized projects
- Multi-deliverable requests
- When hour-level precision is false confidence
- Example: `"3-5 days"`, `"5-10 days"`

**Weeks** (1-8 week range):
- Large initiatives
- Multi-phase projects
- When daily precision is inappropriate
- Example: `"2-4 weeks"`, `"4-8 weeks"`

**Conversion guidelines**:
- 1 day ≈ 6-8 hours (focused work)
- 1 week ≈ 20-30 hours (accounting for meetings, interruptions)
- Use hours for <40 hours, days for 40-200 hours, weeks for >200 hours

### Range Width

**Narrow range** (30-50% spread):
```json
{"estimated_effort": "20-30 hours"}  // 50% spread
```
**When**: Well-understood scope, similar prior work, prescriptive request

**Medium range** (50-100% spread):
```json
{"estimated_effort": "10-20 hours"}  // 100% spread
```
**When**: Moderate uncertainty, some unknowns, typical for explorations

**Wide range** (100%+ spread):
```json
{"estimated_effort": "10-30 hours"}  // 200% spread
```
**When**: High uncertainty, many unknowns, novel work
**Warning**: Ranges this wide suggest need for spike/exploration first

### Estimation Techniques

#### Bottom-Up (Prescriptive)
1. List deliverables
2. Estimate each deliverable separately
3. Sum ranges (low-to-low, high-to-high)
4. Add 10-20% buffer for integration/unknowns

Example:
```
Deliverable A: 5-8 hours
Deliverable B: 10-15 hours
Deliverable C: 3-5 hours
─────────────────────────
Sum: 18-28 hours
Buffer (15%): 21-32 hours
Rounded: 20-35 hours
```

#### Top-Down (Exploratory)
1. Compare to similar past requests
2. Adjust for differences in scope/complexity
3. Use analogous effort as baseline

Example:
```
Similar exploration (COORD-2025-001): 15-20 hours
This request is ~50% larger scope
Adjusted: 22-30 hours
```

#### Three-Point (High Uncertainty)
1. Estimate best case (optimistic)
2. Estimate worst case (pessimistic)
3. Estimate most likely (realistic)
4. Range: `(optimistic to pessimistic)`

Example:
```
Optimistic: 12 hours (everything goes smoothly)
Most likely: 18 hours (typical unknowns)
Pessimistic: 30 hours (major unknowns hit)
Range: 12-30 hours
```

### Calibration Over Time

Track actual vs estimated effort to improve:

```
COORD-2025-001: Estimated 10-15 hours, Actual 18 hours (overran by 20%)
COORD-2025-002: Estimated 12-18 hours, Actual 14 hours (within range)
COORD-2025-003: Estimated 20-30 hours, Actual 22 hours (within range)

Learning: Underestimating integration overhead, add 20% buffer
```

### Breakdown in Context

For complex requests, include breakdown in `context.effort_breakdown`:

```json
{
  "estimated_effort": "40-60 hours",
  "context": {
    "effort_breakdown": "Breakdown by deliverable:\n- [Deliverable 1]: N-M hours\n- [Deliverable 2]: N-M hours\n- [Deliverable 3]: N-M hours\n- Integration and testing: N-M hours\nTotal: X-Y hours"
  }
}
```

**Benefits**:
- Shows thought process (not arbitrary number)
- Helps recipient validate estimate
- Identifies where uncertainty lies
- Enables scoping discussions

### Requester vs Recipient Perspective

**Requester estimate** (what this field captures):
- Based on requester's understanding of deliverables
- May not account for recipient's codebase complexity
- Serves as scoping signal, not commitment

**Recipient estimate** (developed during triage):
- Based on recipient's knowledge of their system
- More accurate but requires investigation
- Informs accept/defer/reject decision

**Healthy interaction**:
```
Requester: "estimated_effort": "15-25 hours"
Recipient (after review): "We estimate 30-40 hours due to legacy code complexity"
Outcome: Adjust scope or timeline based on recipient's estimate
```

### Automation Notes

- **AI Generation**: Can estimate from deliverables + historical data
- **Validation**: Warn if effort seems mismatched to scope (1 hour for complex deliverables, 200 hours for simple request)
- **Breakdown**: AI can generate per-deliverable breakdown for review
- **Unit Selection**: AI chooses hours/days/weeks based on total range

## Validation Rules

- `estimated_effort` field is **optional** (recommended for prescriptive requests)
- If present, must match pattern: `^\d+-\d+ (hours|days|weeks)$`
- Low estimate must be < high estimate
- Recommended ranges:
  - Hours: 2-100 (beyond this, use days)
  - Days: 2-20 (beyond this, use weeks)
  - Weeks: 1-12 (beyond this, consider breaking into phases)
- Range spread: Low should be ≥30% of high (avoid false precision like "19-20 hours")

## Related Content Blocks

- [deliverables-structure.md](deliverables-structure.md) - What will be delivered (effort basis)
- [priority-urgency.md](priority-urgency.md) - When it's needed (effort vs urgency tradeoff)
- [timeline-patterns.md](timeline-patterns.md) - Specific deadlines (effort → timeline)

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)

```json
{
  "estimated_effort": "12-18 hours"
}
```

**Analysis**:
- Exploration phase only (pilot not included)
- Hour-level precision appropriate for short exploration
- 50% spread (moderate uncertainty)
- Actual breakdown documented in pilot plan (not in request)

**Context from pilot plan**:
```
Exploration: 12-18 hours
- Research: 3-5 hours
- Mapping: 4-6 hours
- Prototype: 3-5 hours
- Documentation: 2-3 hours
```

### Example 2: Prescriptive Request (COORD-2025-004)

```json
{
  "estimated_effort": "40-59 hours",
  "context": {
    "effort_breakdown": "Estimated effort breakdown:\n- SAP-009 v1.1.0 specification: 8-12 hours\n- Implementation (scripts/translate-bidirectional.py): 15-20 hours\n- Test suite (≥80% coverage): 10-15 hours\n- Documentation (CHANGELOG, INDEX, examples): 4-6 hours\n- Integration testing and validation: 3-5 hours\n- Review and iteration: 2-4 hours\n\nTotal: 42-62 hours (accounting for unknowns)"
  }
}
```

**Analysis**:
- Detailed per-deliverable breakdown
- Hour-level precision (well-scoped work)
- 48% spread (good confidence)
- Includes buffer for unknowns
- Bottom-up estimation (sum of parts + buffer)

### Example 3: Peer Review Request (coord-005)

```json
{
  "estimated_effort": null
}
```
*Note: Field omitted entirely*

**Analysis**:
- Peer review effort varies by reviewer
- Requester can't estimate recipient's review depth
- Appropriate to omit when effort is reviewer-dependent

**Alternative** (if estimate desired):
```json
{
  "estimated_effort": "4-8 hours",
  "context": {
    "effort_note": "This is our estimate for thorough review of 6 SAPs. Actual effort may vary based on your review depth and availability. We appreciate any level of feedback you can provide."
  }
}
```

## Common Patterns by Request Type

| Request Type | Typical Range | Unit | Spread | Breakdown Detail |
|--------------|---------------|------|--------|------------------|
| Exploratory | 8-30 hours | Hours | 50-100% | Phase-based (research, map, document) |
| Prescriptive | 20-100 hours | Hours or Days | 30-50% | Per-deliverable (spec, code, tests, docs) |
| Peer Review | 2-10 hours | Hours | 50-100% | By review activity (read, compare, document) |
| Emergency (P0) | Often omitted | - | - | Effort less important than speed |

## Effort vs Priority/Urgency

Effort and priority/urgency are **independent** dimensions:

| Priority | Urgency | Effort | Implication |
|----------|---------|--------|-------------|
| P1 | blocks_sprint | 8-12 hours | Small, urgent blocker - high ROI |
| P1 | blocks_sprint | 80-120 hours | Large, urgent blocker - all-hands effort |
| P2 | backlog | 8-12 hours | Small, flexible - easy fill-in work |
| P2 | backlog | 80-120 hours | Large, flexible - needs dedicated sprint(s) |

**Anti-pattern**: Assuming low effort → low priority, or high urgency → high effort

## Metadata

- **Priority**: MEDIUM (valuable in ~67% of requests, especially prescriptive)
- **Stability**: Semi-stable (may be revised during scoping discussions)
- **Reusability**: Universal (identical pattern in tasks and proposals)
- **Generation Source**: AI estimation from deliverables + historical data, user refinement
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
