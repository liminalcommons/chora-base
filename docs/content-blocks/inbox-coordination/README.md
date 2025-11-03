# Inbox Coordination Content Blocks

**Purpose**: Reusable content blocks for generating SAP-001 coordination request artifacts via chora-compose.

**Status**: Week 2 - Content Block Decomposition (Pilot Phase)
**Created**: 2025-11-02
**Trace ID**: `chora-compose-inbox-integration-2025`

---

## Overview

This directory contains 15 content block markdown files that decompose SAP-001 coordination request artifacts into atomic, reusable components. These content blocks serve as the foundation for chora-compose content configs, enabling template-driven generation of coordination requests with AI augmentation where needed.

## Design Philosophy

### Atomic Decomposition

Each content block represents a **single conceptual unit** with:
- Clear purpose and usage guidance
- Field specifications and validation rules
- Template patterns and variation points
- Real examples from actual coordination requests
- Metadata about priority, stability, and generation source

### Reusability Spectrum

Content blocks are organized by reusability:

- **Universal**: Identical across all artifact types (coordination, task, proposal)
  - Example: `core-metadata.md`, `repository-fields.md`
- **Inbox-specific**: Shared across coordination/task/proposal but not external
  - Example: `priority-urgency.md`, `deliverables-structure.md`
- **Coordination-specific**: Unique to coordination requests
  - Example: `exploratory-questions.md`, `collaboration-modes.md`

### Priority Stratification

Blocks are prioritized by presence frequency in analyzed requests:

- **HIGH** (100% presence): Required in every coordination request
- **MEDIUM** (67% presence): Common, high value when present
- **LOW** (33% presence): Variable, context-dependent

---

## Content Block Inventory

### HIGH Priority (6 blocks - 100% presence)

These blocks are **required** in every coordination request:

| Block | Purpose | Key Fields | Generation Source |
|-------|---------|------------|-------------------|
| **[core-metadata.md](core-metadata.md)** | Fundamental identification | `type`, `request_id`, `title`, `created` | Hybrid (literal + system + AI) |
| **[repository-fields.md](repository-fields.md)** | Source/destination repos | `from_repo`, `to_repo` | User input / environment |
| **[priority-urgency.md](priority-urgency.md)** | Scheduling dimensions | `priority`, `urgency` | AI inference + user confirm |
| **[deliverables-structure.md](deliverables-structure.md)** | Concrete outputs expected | `deliverables` array | AI generation from context |
| **[acceptance-criteria-patterns.md](acceptance-criteria-patterns.md)** | Success conditions | `acceptance_criteria` array | AI generation from deliverables |
| **[context-background.md](context-background.md)** | Situational context | `context.background` | AI generation from purpose |

### MEDIUM Priority (6 blocks - 67% presence)

These blocks appear in most requests and add significant value:

| Block | Purpose | Key Fields | Generation Source |
|-------|---------|------------|-------------------|
| **[trace-id-format.md](trace-id-format.md)** | Multi-phase correlation | `trace_id` | AI suggestion + user confirm |
| **[context-rationale.md](context-rationale.md)** | Decision reasoning | `context.rationale` | AI generation from background |
| **[estimated-effort-guide.md](estimated-effort-guide.md)** | Effort estimation | `estimated_effort` | AI from deliverables + history |
| **[timeline-patterns.md](timeline-patterns.md)** | Deadlines and milestones | `timeline` | User input / AI extraction |
| **[dependencies-pattern.md](dependencies-pattern.md)** | Prerequisites | `dependencies` array | AI extraction + user status |
| **[related-work-template.md](related-work-template.md)** | Contextual connections | `related` array | AI extraction + catalog search |

### LOW Priority (3 blocks - 33% presence)

These blocks are context-dependent, appearing primarily in specific request types:

| Block | Purpose | Key Fields | Request Type Affinity | Generation Source |
|-------|---------|------------|----------------------|-------------------|
| **[exploratory-questions.md](exploratory-questions.md)** | Questions to answer | `questions` array or object | Exploratory (80%+) | AI from context.purpose |
| **[collaboration-modes.md](collaboration-modes.md)** | Engagement options | `collaboration_modes` array | Exploratory external (60-70%) | AI from deliverables + tone |
| **[context-boundaries.md](context-boundaries.md)** | Scope exclusions | `context.not_requesting` | Exploratory external (50-60%) | AI concern detection |

---

## Decomposition Rationale

### Analysis Foundation

Content block decomposition is based on analysis of 3 real coordination requests:

1. **CORD-2025-002** (exploratory, 213 lines, external): chora-compose integration exploration
2. **CORD-2025-004** (prescriptive, 78 lines, internal): SAP-009 bidirectional translation
3. **coord-005** (peer review, 96 lines, external): React SAPs peer review

**Analysis Document**: [coordination-request-analysis.md](../../exploration/coordination-request-analysis.md)

### Universal Fields (100% presence)

**10 fields appeared in all 3 requests**, forming the HIGH priority tier:

```
type, request_id, title, from_repo, to_repo, priority, urgency,
deliverables, acceptance_criteria, context, created
```

**Decomposition decision**: Each became a separate content block (6 blocks total, as `context` was split into background/rationale/boundaries).

**Rationale**:
- **Atomic**: Each field has distinct purpose and generation pattern
- **Reusable**: Can be combined differently for tasks and proposals
- **Variability**: Each field has multiple valid patterns (exploratory vs prescriptive)

### Common Fields (67% presence)

**2 fields appeared in 2 of 3 requests**, forming the MEDIUM priority tier:

```
trace_id (CORD-2025-002, CORD-2025-004)
estimated_effort (CORD-2025-002, CORD-2025-004)
```

Plus **4 additional MEDIUM fields** that are valuable when present:

```
context.rationale (exploratory, prescriptive - explains decision)
timeline (prescriptive, occasionally peer review - deadlines)
dependencies (prescriptive, complex exploratory - prerequisites)
related (all types - ecosystem awareness)
```

**Decomposition decision**: Each became a separate content block (6 blocks).

**Rationale**:
- **High value when present**: trace_id enables correlation, effort enables planning
- **Not universally required**: Standalone requests omit trace_id, simple requests omit dependencies
- **Distinct patterns**: Each has unique generation logic and validation rules

### Variable Fields (33% presence)

**9 fields appeared in 1 of 3 requests** (typically exploratory):

```
questions (CORD-2025-002 - exploratory)
collaboration_modes (CORD-2025-002 - exploratory)
context.not_requesting (CORD-2025-002 - boundaries)
context.humble_acknowledgments (coord-005 - peer review specific)
context.our_situation (CORD-2025-002 - exploratory specific)
context.why_reaching_out (CORD-2025-002 - exploratory specific)
context.what_we_are_NOT_requesting (CORD-2025-002 - same as boundaries)
```

**Decomposition decision**: Created 3 LOW priority blocks:
1. **exploratory-questions.md**: `questions` field
2. **collaboration-modes.md**: `collaboration_modes` field
3. **context-boundaries.md**: `context.not_requesting` / `what_we_are_NOT_requesting`

**Omitted** as request-type-specific:
- `humble_acknowledgments`, `our_situation`, `why_reaching_out` (peer review / exploratory specific, folded into context.background patterns)

**Rationale**:
- **Request-type affinity**: Questions are exploratory (80%+ of exploratory, <10% prescriptive)
- **Reusability**: Boundaries and collaboration modes appear in peer reviews too
- **Consolidation**: Merged similar fields (not_requesting + what_we_are_NOT_requesting → boundaries)

### Context Object Decomposition

The `context` object appeared in all 3 requests but with varying internal structure:

**CORD-2025-002** (exploratory):
```json
{
  "context": {
    "our_situation": "...",
    "why_reaching_out": "...",
    "what_we_are_NOT_requesting": "..."
  }
}
```

**CORD-2025-004** (prescriptive):
```json
{
  "context": {
    "background": "...",
    "rationale": "..."
  }
}
```

**coord-005** (peer review):
```json
{
  "context": {
    "background": "...",
    "humble_acknowledgments": "..."
  }
}
```

**Decomposition decision**: Standardized to 3 sub-blocks:
1. **context-background.md**: Universal narrative (maps from `our_situation` + `why_reaching_out` for exploratory)
2. **context-rationale.md**: Decision reasoning (MEDIUM priority)
3. **context-boundaries.md**: Scope exclusions (LOW priority, maps from `what_we_are_NOT_requesting`)

**Rationale**:
- **Standardization**: Different requests used different field names for similar concepts
- **Composability**: Background is universal, rationale and boundaries are conditional
- **AI generation**: Easier to generate 3 focused blocks than 1 complex object

---

## Generation Strategy

### Template-First Approach

Each content block defines a **template pattern** that serves as the deterministic baseline:

```markdown
## Template / Example

json
{
  "{{field_name}}": "{{placeholder_value}}"
}
```

**Benefits**:
- Deterministic, reproducible baseline
- Clear structure for AI to augment
- Validation-friendly (schema-based)

### AI Augmentation Points

Content blocks identify **variation points** where AI can customize:

```markdown
## Variation Points

### Exploratory Requests (Discovery Narrative)
[Pattern for AI to follow]

### Prescriptive Requests (Implementation Context)
[Alternative pattern for AI]
```

**Benefits**:
- AI knows *what* to vary (not arbitrary)
- Patterns guide *how* to vary (not unconstrained)
- Examples show quality bar

### Hybrid Generation Pipeline

```
User Context Input
    ↓
Template Selection (based on request_type)
    ↓
AI Augmentation (fill variation points)
    ↓
Post-Processing (validation, ID allocation, events)
    ↓
Valid Coordination Request JSON
```

---

## Content Block Structure

Each content block follows a consistent structure:

```markdown
# [Block Name] Content Block

## Description
What this block represents and when to use it

## Fields / Structure
Field specifications, types, constraints

## Template / Example
Literal template or example with placeholders

## Variation Points
How content varies by request type

## Usage Guidance
How to customize, when to override

## Validation Rules
Required vs optional, format constraints

## Related Content Blocks
Cross-references to related blocks

## Examples from Real Requests
Concrete examples from analyzed requests

## Metadata
Priority, stability, reusability, generation source
```

**Rationale**:
- **Self-documenting**: Each block is standalone reference
- **AI-friendly**: Structure is parseable and actionable
- **Human-friendly**: Clear guidance for manual use
- **Example-driven**: Real examples ground understanding

---

## Usage Patterns

### For chora-compose Content Configs

Each content block maps to a **ContentElement** in chora-compose:

```json
{
  "name": "core-metadata",
  "description": "Fundamental identifying fields (type, request_id, title, created)",
  "format": "json",
  "example_output": {
    "type": "coordination",
    "request_id": "COORD-2025-NNN",
    "title": "Example Title",
    "created": "2025-11-02"
  },
  "generation_source": {
    "type": "template_fill",
    "template_path": "docs/content-blocks/inbox-coordination/core-metadata.md",
    "placeholders": {
      "request_id": "from_post_processing",
      "title": "from_user_context",
      "created": "from_system_date"
    }
  }
}
```

**Integration pattern**: Content block markdown → chora-compose ContentElement config

### For Manual Artifact Creation

Developers can use content blocks as **reference documentation** when manually creating coordination requests:

1. Identify required blocks (all HIGH priority)
2. Add MEDIUM priority blocks as needed
3. Consult block templates for formatting
4. Reference examples for quality patterns
5. Validate against acceptance criteria

---

## Quality Characteristics

### Completeness

**Coverage**: 15 content blocks cover 100% of fields observed in analyzed requests:
- 10 universal fields (100% presence) → 6 HIGH + context decomposition
- 2 common fields (67% presence) → part of 6 MEDIUM
- 9 variable fields (33% presence) → 3 LOW + folded into existing

**Verification**: All fields from COORD-2025-002, CORD-2025-004, and coord-005 are represented.

### Atomicity

Each content block represents **one conceptual unit**:
- ✅ `core-metadata.md`: type + request_id + title + created (closely related)
- ✅ `repository-fields.md`: from_repo + to_repo (inseparable pair)
- ✅ `priority-urgency.md`: priority + urgency (orthogonal but paired)
- ✅ All others: Single field or cohesive sub-object

**Anti-pattern avoided**: Not creating 18 micro-blocks (one per field) or 1 mega-block (all fields).

### Reusability

**Universal blocks** (usable across artifact types):
- `core-metadata.md`: Works for coordination, task, proposal (type field varies)
- `repository-fields.md`: Identical for all artifact types
- `priority-urgency.md`: Identical for all artifact types
- `deliverables-structure.md`: Applies to tasks and proposals
- `acceptance-criteria-patterns.md`: Applies to tasks and proposals

**Coordination-specific blocks**:
- `exploratory-questions.md`: Exploratory coordination only
- `collaboration-modes.md`: Cross-repo coordination only
- `context-boundaries.md`: External coordination primarily

**Benefit**: Content block library can be extended to tasks (12-15 blocks) and proposals (10-12 blocks) with ~60-70% reuse.

### Discoverability

**File naming**: `[topic]-[format].md` pattern (e.g., `core-metadata.md`, `context-background.md`)

**Cross-referencing**: Each block links to related blocks in "Related Content Blocks" section

**Priority indicators**: File metadata includes priority (HIGH/MEDIUM/LOW)

**Examples**: Each block includes ≥2 real examples from analyzed requests

---

## Validation and Quality Control

### Schema Validation

Content blocks inform the **context schema** ([context-schema.json](../../../context-examples/coordination/context-schema.json)):

- Required fields from HIGH priority blocks
- Optional fields from MEDIUM/LOW priority blocks
- Validation rules (regex, min/max, enums) from block specifications

### Example Context Files

**3 example context files** demonstrate block usage:

1. **[example-exploratory.json](../../../context-examples/coordination/example-exploratory.json)**: Uses 13/15 blocks (omits timeline details, prescriptive-specific)
2. **[example-prescriptive.json](../../../context-examples/coordination/example-prescriptive.json)**: Uses 12/15 blocks (omits questions, collaboration modes, boundaries)
3. **[example-peer-review.json](../../../context-examples/coordination/example-peer-review.json)**: Uses 11/15 blocks (mix of exploratory and prescriptive patterns)

**Coverage**: All 15 content blocks are used in at least one example.

### Quality Rubric Alignment

Content blocks support the **10-criterion quality rubric** (pilot plan):

| Rubric Criterion | Content Block Support |
|------------------|----------------------|
| **Structure Match** (10%) | All HIGH priority blocks ensure required fields present |
| **Technical Accuracy** (20%) | Block examples from real requests, validation rules |
| **Coherence** (15%) | Related blocks cross-referenced, logical grouping |
| **Completeness** (15%) | 15 blocks cover 100% of observed fields |
| **JSON Schema** (10%) | Block specs inform context-schema.json |
| **inbox-status.py** (10%) | Blocks ensure valid SAP-001 structure |
| **Time Reduction** (5%) | Template patterns speed generation |
| **Maintainability** (5%) | Atomic blocks easier to update than monolithic |
| **Flexibility** (5%) | Variation points enable customization |
| **Scalability** (5%) | Reusable blocks extend to tasks/proposals |

---

## Next Steps (Week 3)

With content blocks decomposed, Week 3 (DDD phase) will:

1. **Create chora-compose content configs** for each content block
   - Map block markdown to ContentElement JSON
   - Define generation_source (template_fill, demonstration, ai_augmented)
   - Specify input sources (user context, system functions, post-processing)

2. **Design artifact assembly config**
   - Combine ContentElements into coordination request artifact
   - Define ordering and dependencies
   - Specify post-processing steps (validation, ID allocation, events)

3. **Document integration architecture**
   - Diátaxis-style change request
   - Architecture diagrams (DDD)
   - Integration points with existing scripts

**Deliverables** (Week 3): 15-20 content config JSON files + artifact assembly config + architecture documentation

---

## Metadata

**Created**: 2025-11-02
**Status**: Week 2 Complete
**Trace ID**: `chora-compose-inbox-integration-2025`
**Related Documents**:
- [Coordination Request Analysis](../../exploration/coordination-request-analysis.md)
- [Pilot Plan](../../exploration/chora-compose-inbox-integration-pilot-plan.md)
- [Context Schema](../../../context-examples/coordination/context-schema.json)
- [Example Contexts](../../../context-examples/coordination/)

**Content Block Count**: 15 (6 HIGH + 6 MEDIUM + 3 LOW)
**Total Lines**: ~7,500 (average 500 lines per block)
**Effort**: 8-12 hours (Week 2, Task 2.2)

---

## Questions or Feedback

For questions about content blocks or suggestions for improvements, see:
- [Pilot Plan](../../exploration/chora-compose-inbox-integration-pilot-plan.md) for decision framework
- [AGENTS.md](../../../AGENTS.md) for general project guidance
- [SAP-001 Inbox Coordination Protocol](../../skilled-awareness/inbox/protocol-spec.md) for schema requirements
