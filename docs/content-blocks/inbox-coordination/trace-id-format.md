# Trace ID Format Content Block

## Description

Optional correlation identifier that links related coordination requests, implementations, events, and artifacts across the ecosystem. Trace IDs enable tracking work from initial exploration through pilot, implementation, and production deployment. They serve as the thread connecting distributed coordination efforts.

**When to use**: Coordination requests that are part of larger initiatives, multi-phase projects, or ecosystem-wide coordination. Not required for standalone requests.

## Fields / Structure

```json
{
  "trace_id": "descriptive-project-name-year"
}
```

### Field Specifications

- **trace_id**: String (optional, present in 67% of analyzed requests)
- Format: `kebab-case-descriptive-name-year`
- Should be human-readable and self-documenting
- Consistent across all related artifacts (requests, tasks, events, logs)
- Typically includes project/initiative name and year for uniqueness
- No strict length limit, but 30-60 characters is typical

## Template / Example

```json
{
  "trace_id": "{{project_name}}-{{year}}"
}
```

## Variation Points

### Multi-Phase Projects

For projects with exploration → pilot → implementation phases:

```json
{
  "trace_id": "chora-compose-inbox-integration-2025"
}
```

**Usage**:
- Exploration phase: COORD-2025-002 uses this trace_id
- Pilot phase: Tasks and artifacts use same trace_id
- Implementation phase: All related work shares trace_id
- Events: All events.jsonl entries use this trace_id

**Benefit**: Can query all related work via `grep "chora-compose-inbox-integration-2025" inbox/coordination/events.jsonl`

### Ecosystem-Wide Initiatives

For coordination affecting multiple repositories:

```json
{
  "trace_id": "ecosystem-sap-standardization-2025"
}
```

**Usage**:
- Multiple coordination requests across repos share trace_id
- Each repo's implementation tasks inherit trace_id
- Ecosystem status tracking uses trace_id for rollup

**Benefit**: Stakeholders can track initiative progress across ecosystem

### Feature Development

For specific features with multiple coordination points:

```json
{
  "trace_id": "bidirectional-translation-v1.1-2025"
}
```

**Usage**:
- Initial coordination request
- Related tasks and subtasks
- Documentation updates
- Release notes and announcements

**Benefit**: Feature history and related work easily discoverable

### Pilot Programs

For SAP-004 style pilots with structured evaluation:

```json
{
  "trace_id": "sap-004-pilot-react-saps-2025"
}
```

**Usage**:
- Pilot planning documents
- Generated artifacts for evaluation
- Quality assessments and metrics
- Decision documentation

**Benefit**: Pilot artifacts and decisions grouped together

## Usage Guidance

### Naming Conventions

**Good trace IDs**:
- `chora-compose-inbox-integration-2025` (project + scope + year)
- `ecosystem-sap-standardization-2025` (initiative + year)
- `bidirectional-translation-v1.1-2025` (feature + version + year)
- `sap-004-pilot-react-saps-2025` (program + scope + year)

**Poor trace IDs**:
- `project-1` (not descriptive)
- `chora-compose-exploration-pilot-implementation-phase-1-2025` (too long)
- `COORD-2025-002` (this is request_id, not trace_id)
- `chora_compose_integration` (use kebab-case, not snake_case)

### Length Guidelines

- **Minimum**: 10 characters (avoid cryptic abbreviations)
- **Typical**: 30-60 characters (descriptive but scannable)
- **Maximum**: 80 characters (longer suggests need for abbreviation)

### Year Suffix

- **Always include year** for uniqueness and temporal context
- Use 4-digit year: `2025` not `25`
- Place at end for chronological sorting
- If project spans years, use start year: `long-project-2025` (even if continuing into 2026)

### Consistency

Once established, trace_id should:
- **Never change** across project lifecycle
- Be used **identically** in all related artifacts (no variations)
- Appear in **all related events** (events.jsonl)
- Be **documented** in README or project docs for discoverability

### When to Omit trace_id

**Skip trace_id when**:
- Standalone, one-off coordination request
- No planned follow-up or related work
- Single-repository, single-sprint task
- Request is self-contained and won't be referenced later

**Use trace_id when**:
- Multi-phase project (exploration → pilot → implementation)
- Ecosystem-wide initiative affecting multiple repos
- Related series of coordination requests
- Want to track work across time and repositories

### Automation Notes

- **AI Generation**: Can suggest trace_id from context.purpose and project scope
- **Uniqueness Check**: Query events.jsonl to avoid collision (rare but possible)
- **Propagation**: Once set, automatically propagate to related tasks/events
- **Environment Variable**: Set `CHORA_TRACE_ID` in shell for scripts to inherit

## Validation Rules

- `trace_id` field is **optional** (omit if not needed)
- If present, must be non-empty string
- Should use kebab-case format (lowercase words separated by hyphens)
- Recommended pattern: `^[a-z0-9-]+-\d{4}$` (ends with 4-digit year)
- Length: 10-80 characters recommended
- Should not match existing request_id patterns (coord-NNN, COORD-YYYY-NNN)

## Related Content Blocks

- [core-metadata.md](core-metadata.md) - Request identification (different from trace_id)
- [context-background.md](context-background.md) - May explain project context for trace_id
- [related-work-template.md](related-work-template.md) - Links to other work with same trace_id

## Examples from Real Requests

### Example 1: Multi-Phase Exploration (COORD-2025-002)

```json
{
  "trace_id": "chora-compose-inbox-integration-2025"
}
```

**Context**: Exploration request that could lead to pilot and implementation
**Related Artifacts**:
- Exploration documents in `docs/exploration/`
- Pilot plan (if approved)
- Generated artifacts during pilot
- Events in `events.jsonl`

**Query**:
```bash
grep "chora-compose-inbox-integration-2025" inbox/coordination/events.jsonl
# Returns: exploration_started, exploration_completed, pilot_planning_started, etc.
```

### Example 2: Prescriptive Implementation (COORD-2025-004)

```json
{
  "trace_id": "bidirectional-translation-sap009-2025"
}
```

**Context**: Implementation request for SAP-009 v1.1.0
**Related Artifacts**:
- Coordination request COORD-2025-004
- Implementation tasks in `inbox/active/`
- SAP-009 document updates
- Test suite additions
- Release notes

**Benefit**: All SAP-009 v1.1.0 work discoverable via trace_id

### Example 3: No Trace ID (coord-005)

```json
{
  "trace_id": null
}
```
*Note: Field omitted entirely in actual request*

**Context**: Standalone peer review request
**Rationale**: One-time review, no planned follow-up phases, no related coordination

## Event Emission Integration

When trace_id is present, all emitted events should include it:

```json
{
  "event_type": "coordination_request_created",
  "timestamp": "2025-11-01T14:30:00-07:00",
  "request_id": "COORD-2025-002",
  "trace_id": "chora-compose-inbox-integration-2025",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-compose"
}
```

This enables trace-based queries:

```bash
# Find all events for this project
python scripts/inbox-status.py --trace-id chora-compose-inbox-integration-2025

# Or via jq
jq 'select(.trace_id == "chora-compose-inbox-integration-2025")' inbox/coordination/events.jsonl
```

## Usage in Scripts

Scripts can read trace_id from environment or artifact:

```bash
# Set in environment for all related work
export CHORA_TRACE_ID="chora-compose-inbox-integration-2025"

# Scripts automatically include in emitted events
python scripts/process-inbox.py  # Emits events with $CHORA_TRACE_ID
```

## Cross-Repository Coordination

For ecosystem initiatives, use same trace_id across all participating repos:

**chora-base** (COORD-2025-010):
```json
{
  "request_id": "COORD-2025-010",
  "trace_id": "ecosystem-sap-standardization-2025",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-workspace"
}
```

**chora-workspace** (COORD-2025-008):
```json
{
  "request_id": "COORD-2025-008",
  "trace_id": "ecosystem-sap-standardization-2025",
  "from_repo": "github.com/liminalcommons/chora-workspace",
  "to_repo": "github.com/liminalcommons/ecosystem-manifest"
}
```

**Benefit**: `grep "ecosystem-sap-standardization-2025" */inbox/coordination/events.jsonl` shows initiative status across ecosystem

## Metadata

- **Priority**: MEDIUM (present in 67% of coordination requests, high value when used)
- **Stability**: Immutable (never changes once set)
- **Reusability**: Universal (identical pattern in tasks, proposals, events)
- **Generation Source**: AI suggestion from project scope, user confirmation
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
