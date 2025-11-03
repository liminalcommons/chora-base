# Dependencies Pattern Content Block

## Description

Optional field documenting prerequisite work that must complete before this coordination request can begin or finish. Dependencies help recipients understand sequencing constraints, identify blockers, and plan scheduling. They make coordination dependencies explicit rather than implicit.

**When to use**: Coordination requests with prerequisites (other requests, SAPs, infrastructure) or that are part of dependency chains. Common in prescriptive requests (~40-50%), less common in exploratory requests (~20-30%).

## Fields / Structure

```json
{
  "dependencies": [
    "Description of prerequisite 1",
    "Description of prerequisite 2"
  ]
}
```

### Field Specifications

- **dependencies**: Array of strings (optional, ~30-40% of requests)
- Each string describes one prerequisite
- Should be specific (not vague like "other work")
- May include status: "completed", "in progress", "blocked"
- Can reference request IDs, SAP versions, or external work

## Template / Example

```json
{
  "dependencies": [
    "{{prerequisite_1}} ({{status}})",
    "{{prerequisite_2}} ({{status}})"
  ]
}
```

## Variation Points

### Completed Dependencies (Unblocked)

Prerequisites already satisfied:

```json
{
  "dependencies": [
    "SAP-001 v1.0.0 (completed - inbox protocol established)",
    "Exploration phase COORD-2025-002 (completed - feasibility confirmed)",
    "chora-compose v0.5.0 installed (completed - available in environment)"
  ]
}
```

**Characteristics**:
- All dependencies marked as "completed"
- Optional context in parentheses (what was accomplished)
- Signals work can proceed immediately
- Common in prescriptive requests following exploration

### In-Progress Dependencies (Partial Block)

Some prerequisites completed, others in progress:

```json
{
  "dependencies": [
    "SAP-009 v1.0.0 (completed - unidirectional translation working)",
    "chora-workspace SAP adoption (in progress - 60% complete, unblocks bidirectional use case)",
    "ecosystem-manifest coordination protocol (planned - blocks multi-repo coordination)"
  ]
}
```

**Characteristics**:
- Mixed statuses (completed, in progress, planned)
- Percentage or milestone for in-progress items
- Indicates partial unblocking (some work can start)
- Helps recipient plan phased approach

### Blocked Dependencies (Cannot Proceed)

Critical prerequisites not yet satisfied:

```json
{
  "dependencies": [
    "COORD-2025-001 infrastructure setup (blocked - awaiting infrastructure team approval)",
    "Python 3.11+ environment (blocked - current environment is Python 3.9)",
    "chora-compose feature request #47 (blocked - awaiting upstream implementation)"
  ]
}
```

**Characteristics**:
- All or most dependencies "blocked"
- Indicates request cannot proceed yet
- May include what's blocking each dependency
- Should trigger "defer" triage decision until unblocked

### Conditional Dependencies (Depends on Decision)

Prerequisites vary based on earlier decisions:

```json
{
  "dependencies": [
    "Exploration phase GO decision (if GO: proceed to pilot, if NO-GO: fall back to manual process)",
    "If pilot proceeds: chora-compose content config design (pilot week 1-2)",
    "If pilot succeeds: SAP-004 quality framework ≥80% threshold (pilot week 3-4)"
  ]
}
```

**Characteristics**:
- Dependencies conditional on earlier decisions
- Often used in multi-phase projects
- Helps recipient understand decision tree
- Typical for exploratory → pilot → implementation workflows

### External Dependencies (Outside Requesting Repo)

Prerequisites from other repos or systems:

```json
{
  "dependencies": [
    "chora-compose v0.6.0 release (external - chora-compose team, ETA: 2025-11-10)",
    "GitHub API rate limit increase (external - GitHub support ticket #12345)",
    "Ecosystem coordination approval (external - ecosystem-manifest maintainers)"
  ]
}
```

**Characteristics**:
- Marked as "external" to indicate outside requester's control
- May include owning team or system
- Often includes ETA if known
- Signals coordination risk and timeline uncertainty

### No Dependencies

Many requests have no prerequisites:

```json
{
  "dependencies": null
}
```
*Note: Field omitted entirely*

**When to omit**:
- Standalone request with no prerequisites
- All dependencies already satisfied (implicit)
- Dependencies too obvious to state
- Most exploratory and peer review requests

## Usage Guidance

### Status Indicators

**Completed**:
```
"SAP-001 v1.0.0 (completed)"
```
- Work is done, dependency satisfied
- May include brief description of what was accomplished

**In Progress**:
```
"chora-workspace integration (in progress - 60% complete, ETA: Nov 15)"
```
- Work is underway but not finished
- Include percentage, milestone, or ETA when possible
- Helps recipient assess timeline

**Blocked**:
```
"Infrastructure approval (blocked - awaiting security review)"
```
- Work cannot proceed
- Include reason for block if known
- Signals need to defer request until unblocked

**Planned**:
```
"Feature X implementation (planned - Q1 2026)"
```
- Work is scheduled but not started
- Include timeline if known
- Indicates future dependency

### Specificity

**Good** (specific and verifiable):
```json
{
  "dependencies": [
    "SAP-009 v1.0.0 (completed - bidirectional translation protocol)",
    "COORD-2025-002 exploration (completed - 90% technical feasibility)",
    "chora-compose v0.5.0+ (completed - installed and tested)"
  ]
}
```

**Poor** (vague and unverifiable):
```json
{
  "dependencies": [
    "Other work (done)",
    "Some setup (in progress)",
    "Tools (maybe ready)"
  ]
}
```

### Dependency Types

**Technical dependencies** (infrastructure, tools, versions):
```
"Python 3.11+ environment (completed)"
"chora-compose v0.5.0+ (required - not yet installed)"
```

**Process dependencies** (approvals, decisions, reviews):
```
"Security review approval (completed - 2025-10-28)"
"Architecture decision on translation strategy (completed - bidirectional)"
```

**Artifact dependencies** (SAPs, documents, code):
```
"SAP-001 v1.0.0 inbox protocol (completed)"
"COORD-2025-002 exploration phase (completed)"
```

**External dependencies** (other repos, teams, services):
```
"chora-compose feature #47 (external - in progress at chora-compose)"
"GitHub API access (external - rate limit approved)"
```

### Sequencing Information

Dependencies imply sequencing - use to plan workflow:

```json
{
  "dependencies": [
    "Step 1: SAP-009 v1.0.0 (completed)",
    "Step 2: Exploration COORD-2025-002 (completed)",
    "Step 3: Pilot plan (in progress - 80% complete)",
    "Step 4: GO decision (pending - Nov 8)"
  ]
}
```

This explicit sequencing helps recipient understand workflow and current position in dependency chain.

### Automation Notes

- **AI Detection**: Can extract dependencies from context.background and deliverables
- **Status Inference**: Can infer status from events.jsonl or related artifacts
- **Validation**: Check if referenced dependencies exist (SAPs, requests, external refs)
- **Blocking Analysis**: Warn if all dependencies are "blocked" (suggests defer)

## Validation Rules

- `dependencies` field is **optional** (omit if no prerequisites)
- If present, must be array of strings (even if single dependency)
- Each dependency should be specific and verifiable
- Recommended to include status (completed, in progress, blocked, planned)
- Can reference request IDs, SAP versions, external systems
- Empty array `[]` is valid but discouraged (omit field instead)

## Related Content Blocks

- [timeline-patterns.md](timeline-patterns.md) - When work needs to be done (affected by dependencies)
- [related-work-template.md](related-work-template.md) - Related but not prerequisite work
- [context-background.md](context-background.md) - May explain dependency context

## Examples from Real Requests

### Example 1: Prescriptive Request with Completed Dependencies (COORD-2025-004)

```json
{
  "dependencies": [
    "SAP-009 v1.0.0 (completed - unidirectional translation established)",
    "chora-workspace coordination discussions (completed - bidirectional need confirmed)",
    "ecosystem-manifest feedback (completed - external format requirements documented)"
  ]
}
```

**Analysis**:
- All 3 dependencies marked "completed"
- Brief context for each (what was accomplished)
- Signals work can proceed immediately
- Dependencies were sequential (v1.0.0 → discussions → feedback)

### Example 2: Exploratory Request with Mixed Dependencies (COORD-2025-002)

```json
{
  "dependencies": [
    "SAP-001 v1.0.0 inbox protocol (completed - schemas and workflows established)",
    "Initial chora-compose research (in progress - 70% complete, deep-dive underway)",
    "SAP-004 pilot framework (planned - will be used for quality evaluation if pilot proceeds)"
  ]
}
```

**Analysis**:
- Mixed statuses (completed, in progress, planned)
- "In progress" includes percentage (70%)
- "Planned" is conditional (if pilot proceeds)
- Shows phased dependency resolution

### Example 3: No Dependencies (coord-005)

```json
{
  "dependencies": null
}
```
*Note: Field omitted entirely*

**Analysis**:
- Peer review request with no prerequisites
- Can proceed immediately based on capacity
- Standalone request, no blocking dependencies

### Example 4: Blocked Dependencies (Hypothetical)

```json
{
  "dependencies": [
    "chora-compose v0.6.0 release (blocked - external team, ETA unknown)",
    "Infrastructure team approval (blocked - security review pending since Oct 15)",
    "Budget allocation for pilot (blocked - awaiting Q4 budget finalization)"
  ]
}
```

**Analysis**:
- All 3 dependencies "blocked"
- External dependency (v0.6.0) with uncertain timeline
- Process dependencies (approval, budget)
- Should trigger "defer" triage decision

## Dependency and Triage Decision

Dependencies affect triage outcomes:

| Dependencies | Triage Decision | Rationale |
|--------------|-----------------|-----------|
| All completed | Accept or Defer (based on capacity) | No blocking dependencies |
| Most completed, 1-2 in progress | Accept with phased plan | Can start partial work |
| 50% blocked | Defer until unblocked | Too much uncertainty |
| All blocked | Defer or Reject | Cannot proceed |
| External dependencies blocked | Defer with timeline | Wait for external team |

## Dependencies vs Related Work

**Dependencies** (this block):
- **Must** complete before this work can proceed
- **Blocking** relationship
- Affects feasibility and scheduling

**Related Work** (different block):
- **May** influence or benefit from this work
- **Informational** relationship
- Does not block, but provides context

**Example**:
```json
{
  "dependencies": [
    "SAP-009 v1.0.0 (completed - required for bidirectional translation)"
  ],
  "related": [
    "SAP-010 ecosystem coordination (will benefit from this work, not blocking)",
    "chora-workspace SAP adoption (parallel effort, shares context)"
  ]
}
```

## Metadata

- **Priority**: MEDIUM (valuable in 30-40% of requests, critical for sequencing)
- **Stability**: Semi-stable (status changes as dependencies resolve)
- **Reusability**: Universal (identical pattern in tasks, proposals, project planning)
- **Generation Source**: AI extraction from context, user refinement for status
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
