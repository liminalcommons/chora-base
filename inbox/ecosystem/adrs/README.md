# ADRs (Architecture Decision Records)

**Status:** Finalized decisions
**Purpose:** Historical record of "why" decisions were made
**Immutable:** Once written, ADRs are never modified (only superseded)

---

## Purpose

This directory contains **Architecture Decision Records** - lightweight documents capturing important architectural decisions and their rationale.

## When to Create an ADR

Create an ADR when:
- ✅ An RFC has been accepted and finalized
- ✅ A significant architectural decision has been made
- ✅ A cross-repo pattern or standard is established
- ✅ A technology choice impacts multiple repos

**Examples:**
- "We will use JSONL format for event logs across all repos"
- "Health check responses must follow OpenAPI format"
- "Trace context propagates via `CHORA_TRACE_ID` environment variable"

---

## ADR Format

ADRs use a minimal, consistent format:

```markdown
---
adr: [number]
title: ADR Title
date: YYYY-MM-DD
status: accepted | superseded | deprecated
supersedes: [optional - ADR number this replaces]
superseded-by: [optional - ADR number that replaces this]
---

# ADR [Number]: [Title]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive Consequences
- What benefits does this decision provide?

### Negative Consequences
- What downsides or trade-offs do we accept?

## Compliance
How will repos verify compliance with this decision?

## Related
- Links to related RFCs, proposals, or other ADRs
- Links to affected repos or implementation PRs
```

---

## ADR Lifecycle

```
inbox/ecosystem/rfcs/      (RFC under discussion)
          ↓ RFC accepted
          ↓
inbox/ecosystem/adrs/      (ADR created) ← YOU ARE HERE
          ↓ implementation
inbox/incoming/coordination/ (tasks generated)
```

### ADR Status

- **accepted** - Current decision, actively followed
- **superseded** - Replaced by newer ADR (links to successor)
- **deprecated** - No longer recommended but not yet superseded

**Important:** ADRs are **immutable**. If a decision changes, create a new ADR that supersedes the old one. This preserves historical context.

---

## ADR Numbering

ADRs are numbered sequentially and independently from RFCs:
- `0001-event-log-format.md`
- `0002-health-check-standard.md`
- `0003-trace-context-propagation.md`

---

## Example ADRs

### ADR 0001: Use JSONL for Event Logs

```markdown
---
adr: 0001
title: Use JSONL for Event Logs
date: 2025-10-27
status: accepted
---

# ADR 0001: Use JSONL for Event Logs

## Context
We need a standardized format for event logs across all ecosystem repos to enable cross-repo traceability and observability.

## Decision
All repos will emit events as JSONL (JSON Lines) format:
- One JSON object per line
- Append-only (never modify existing lines)
- Each event includes `trace_id`, `event_type`, `timestamp`
- File location: `var/telemetry/events.jsonl`

## Consequences

### Positive Consequences
- Simple to parse (split by newline, parse JSON)
- Streamable (can tail -f and process line-by-line)
- Language-agnostic (JSON supported everywhere)
- Append-only enables safe concurrent writes

### Negative Consequences
- Requires post-processing for analytics (not queryable like database)
- File can grow large (need rotation strategy)
- No schema enforcement at write time

## Compliance
Repos verify compliance by:
1. Emitting events to `var/telemetry/events.jsonl`
2. Including required fields: `trace_id`, `event_type`, `timestamp`
3. Using valid JSON per line
4. Appending only (never modifying existing lines)

## Related
- chora-compose: Already implements this pattern
- RFC 0001: Cross-repo traceability (if existed)
```

---

## How to Create an ADR

1. RFC is accepted and finalized
2. Create new ADR file: `adrs/NNNN-title.md`
3. Use next available number
4. Follow template above
5. Commit to repository
6. Reference in implementation tasks

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - Complete intake process
- [Examples above](#example-adrs) - Sample ADRs
