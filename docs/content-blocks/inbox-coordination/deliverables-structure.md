# Deliverables Structure Content Block

## Description

Concrete, actionable outputs expected from a coordination request. Deliverables specify **what** the requesting party needs, using precise language to minimize ambiguity. Each deliverable should be independently verifiable and contribute to the overall request goal.

**When to use**: Every coordination request to clearly define expected outcomes. Especially critical for prescriptive requests with concrete needs.

## Fields / Structure

```json
{
  "deliverables": [
    "Specific, actionable outcome 1",
    "Specific, actionable outcome 2",
    "Specific, actionable outcome 3"
  ]
}
```

### Field Specifications

- **deliverables**: Array of strings (1-15 items typical)
- Each string describes a **single, discrete output**
- Should be phrased as nouns or noun phrases (not full sentences)
- Order indicates priority or logical sequence (not strict)
- Use consistent terminology across related requests

## Template / Example

```json
{
  "deliverables": [
    "{{deliverable_1}}",
    "{{deliverable_2}}",
    "{{deliverable_3}}"
  ]
}
```

## Variation Points

### Prescriptive Requests (Specific Artifacts)

Most specific form - names exact files, versions, or features:

```json
{
  "deliverables": [
    "SAP-009 v1.1.0 with bidirectional translation protocol specification",
    "Implementation in scripts/translate-bidirectional.py with ≥80% test coverage",
    "CHANGELOG.md entry documenting breaking changes and migration path",
    "Updated docs/skilled-awareness/INDEX.md referencing SAP-009 v1.1.0"
  ]
}
```

**Characteristics**:
- File paths and version numbers specified
- Quantitative criteria embedded (≥80%)
- Clear, verifiable outcomes
- 5-15 deliverables typical

### Exploratory Requests (Knowledge Artifacts)

Focus on information, decisions, or understanding:

```json
{
  "deliverables": [
    "Architectural analysis document comparing inbox schemas to chora-compose structures",
    "Feasibility assessment (technical, quality, maintenance dimensions)",
    "Integration options comparison with effort estimates",
    "Recommendation on whether to proceed with pilot"
  ]
}
```

**Characteristics**:
- Emphasize analysis, comparison, recommendations
- Documents over code
- Open-ended exploration over implementation
- 3-6 deliverables typical

### Peer Review Requests (Feedback Artifacts)

Focus on specific feedback and recommendations:

```json
{
  "deliverables": [
    "Technical review of React SAP architecture patterns",
    "Alignment assessment with ecosystem standards",
    "Recommendations for improving developer experience",
    "Identification of potential edge cases or anti-patterns"
  ]
}
```

**Characteristics**:
- Request feedback, not implementation
- Assessment and recommendation language
- Quality and compatibility focus
- 4-8 deliverables typical

## Usage Guidance

### Quality Characteristics

**Good deliverables**:
- Specific: "SAP-009 v1.1.0" not "updated documentation"
- Measurable: "≥80% test coverage" not "good test coverage"
- Actionable: "Implementation in scripts/translate.py" not "make it work"
- Relevant: Each deliverable clearly serves the request goal
- Independent: Each can be verified separately

**Poor deliverables**:
- Vague: "Improve the system"
- Unmeasurable: "Make it better"
- Process-focused: "Have a meeting to discuss"
- Duplicate: Repeating same deliverable in different words

### Granularity Guidance

**Too granular** (micro-tasks):
```json
{
  "deliverables": [
    "Create file docs/sap-009.md",
    "Add title to docs/sap-009.md",
    "Add description to docs/sap-009.md",
    "Add examples to docs/sap-009.md"
  ]
}
```
**Problem**: Treating deliverables like tasks. Use acceptance criteria for details.

**Too coarse** (vague outcomes):
```json
{
  "deliverables": [
    "Complete the integration"
  ]
}
```
**Problem**: No clarity on what "complete" means.

**Just right** (discrete artifacts):
```json
{
  "deliverables": [
    "SAP-009 v1.1.0 protocol specification document",
    "Python implementation with ≥80% test coverage",
    "Documentation updates in INDEX.md and CHANGELOG.md"
  ]
}
```
**Benefit**: Clear artifacts, measurable criteria, logical grouping.

### Phrasing Patterns

#### Document Deliverables
- "[Document Name] with [key sections]"
- "Analysis of [topic] covering [dimensions]"
- "Comparison of [options] with [evaluation criteria]"

Examples:
- "Architecture analysis document comparing inbox schemas to chora-compose structures"
- "Feasibility assessment (technical, quality, maintenance dimensions)"

#### Implementation Deliverables
- "Implementation of [feature] in [location] with [quality criteria]"
- "[File path] with [version] including [key capabilities]"
- "[Component] supporting [use cases] with [performance criteria]"

Examples:
- "Implementation in scripts/translate-bidirectional.py with ≥80% test coverage"
- "SAP-009 v1.1.0 with bidirectional translation protocol specification"

#### Review/Feedback Deliverables
- "Review of [artifact] assessing [dimensions]"
- "Recommendations for [improvement area]"
- "Identification of [risks/gaps/opportunities]"

Examples:
- "Technical review of React SAP architecture patterns"
- "Recommendations for improving developer experience"

### Ordering Strategy

**Logical dependency order**:
```json
{
  "deliverables": [
    "Architectural analysis (first: understand)",
    "Design document (second: plan)",
    "Implementation (third: build)",
    "Documentation (fourth: explain)"
  ]
}
```

**Priority order**:
```json
{
  "deliverables": [
    "Critical feature X (highest value)",
    "Important feature Y (medium value)",
    "Nice-to-have feature Z (lowest value)"
  ]
}
```

**Artifact grouping**:
```json
{
  "deliverables": [
    "SAP-009 document",
    "SAP-010 document",
    "Implementation in scripts/",
    "Tests in tests/",
    "Documentation in docs/"
  ]
}
```

### Automation Notes

- **AI Generation**: Can draft deliverables from context.purpose and context.questions
- **Validation**: Check for vague language ("improve", "better", "fix")
- **Cross-reference**: Deliverables should align with acceptance_criteria
- **Count**: Warn if <2 deliverables (too vague) or >20 deliverables (too granular)

## Validation Rules

- `deliverables` field is **required**
- Must be an array of strings
- Minimum 1 deliverable (typically 3+ for meaningful requests)
- Maximum 20 deliverables (suggests over-specification)
- Each string should be 10-150 characters (not single words or full paragraphs)
- No duplicate deliverables (case-insensitive check)

## Related Content Blocks

- [acceptance-criteria-patterns.md](acceptance-criteria-patterns.md) - How to verify deliverables
- [context-background.md](context-background.md) - Why these deliverables matter
- [estimated-effort-guide.md](estimated-effort-guide.md) - Effort to produce deliverables

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)

```json
{
  "deliverables": [
    "Architectural analysis document comparing inbox schemas to chora-compose structures",
    "Feasibility assessment (technical, quality, maintenance dimensions)",
    "Integration options comparison with effort estimates",
    "Recommendation on whether to proceed with pilot or alternative approaches"
  ]
}
```

**Analysis**:
- 4 deliverables (appropriate for exploration)
- Focuses on knowledge artifacts (analysis, assessment, comparison, recommendation)
- Logical flow: understand → evaluate → compare → recommend
- Each deliverable is independently valuable

### Example 2: Prescriptive Request (COORD-2025-004)

```json
{
  "deliverables": [
    "SAP-009 v1.1.0 with bidirectional translation protocol specification",
    "Implementation in scripts/translate-bidirectional.py with ≥80% test coverage",
    "Integration tests demonstrating chora-base ↔ external format translation",
    "CHANGELOG.md entry documenting v1.1.0 changes and migration path",
    "Updated docs/skilled-awareness/INDEX.md referencing SAP-009 v1.1.0",
    "Example configurations in examples/translation/ for common scenarios",
    "Performance benchmarks showing <100ms translation time for typical payloads",
    "Error handling documentation for edge cases and malformed input",
    "Versioning strategy document for future protocol evolution",
    "Announcement in inbox/coordination/events.jsonl with trace_id"
  ]
}
```

**Analysis**:
- 10 deliverables (comprehensive prescriptive request)
- Mix of code, tests, documentation, examples, and metadata
- Specific versions (v1.1.0) and criteria (≥80%, <100ms)
- Covers implementation, validation, documentation, and communication

### Example 3: Peer Review Request (coord-005)

```json
{
  "deliverables": [
    "Technical review of React SAP architecture and patterns",
    "Assessment of alignment with chora-base documentation standards",
    "Recommendations for improving clarity and developer onboarding",
    "Identification of potential gaps or edge cases in coverage",
    "Suggestions for ecosystem-wide patterns that could be extracted"
  ]
}
```

**Analysis**:
- 5 deliverables (focused peer review)
- All focus on feedback and recommendations
- Progressive depth: review → assess → recommend → identify → suggest
- Balances specific feedback with strategic thinking

## Common Patterns by Request Type

| Request Type | Deliverable Count | Focus | Examples |
|--------------|-------------------|-------|----------|
| Exploratory | 3-6 | Analysis, assessment, recommendations | "Feasibility assessment", "Comparison of options" |
| Prescriptive | 5-15 | Code, tests, documentation, examples | "Implementation in X with Y% coverage", "Updated docs/Z" |
| Peer Review | 4-8 | Feedback, recommendations, improvements | "Technical review of X", "Recommendations for Y" |
| Emergency (P0) | 1-3 | Immediate fixes, minimal documentation | "Patch for vulnerability X", "Hotfix deployment" |

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Semi-stable (may evolve during discussion, frozen at acceptance)
- **Reusability**: Universal (identical pattern in tasks, slightly different in proposals)
- **Generation Source**: AI generation from context, user refinement recommended
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
