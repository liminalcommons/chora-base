# Context Rationale Content Block

## Description

Explains **why** the requesting party chose this particular approach over alternatives. The rationale section helps recipients understand the decision-making process, constraints considered, and tradeoffs evaluated. This builds confidence that the request is well-considered and prevents re-litigating alternatives.

**When to use**: Coordination requests where approach is non-obvious, multiple alternatives exist, or recipient might question the chosen direction. Especially valuable in exploratory and prescriptive requests.

## Fields / Structure

```json
{
  "context": {
    "rationale": "Explanation of why this approach was chosen over alternatives. May include constraints, prior attempts, or decision criteria. 2-4 paragraphs typical."
  }
}
```

### Field Specifications

- **context.rationale**: String (100-500 words typical)
- Explains decision reasoning (not just restating goals)
- Acknowledges alternatives considered
- Describes constraints or requirements that influenced choice
- May reference prior work or lessons learned
- Complements background (background = situation, rationale = why this response)

## Template / Example

```json
{
  "context": {
    "rationale": "{{why_this_approach}}\n\n{{alternatives_considered}}\n\n{{constraints_or_requirements}}"
  }
}
```

## Variation Points

### Exploratory Requests (Decision Criteria)

Explains why exploration is needed and criteria for success:

```json
{
  "context": {
    "rationale": "We considered three approaches to inbox artifact automation: (1) build custom tooling in chora-base, (2) adopt existing template engines like Jinja2 or Cookiecutter, or (3) integrate with chora-compose. Option 1 would give us full control but requires significant development and maintenance. Option 2 is simpler but lacks the MCP integration and ecosystem alignment we value.\n\nWe're pursuing Option 3 (chora-compose integration) because it offers the best balance of functionality, ecosystem synergy, and shared maintenance. chora-compose's 17 production generators demonstrate maturity, and MCP integration aligns with our vision for agent-assisted workflows. However, we need to validate technical feasibility before committing to this path.\n\nThis exploratory request will help us determine whether chora-compose's architecture can support our SAP-001 schemas, what effort is required, and whether integration makes sense for both teams. If feasibility is high (≥80%), we'll proceed to a 4-week pilot. If lower, we'll fall back to Option 2 (template engine) or Option 1 (custom tooling)."
  }
}
```

**Characteristics**:
- Lists alternatives with pros/cons
- Explains selection criteria (functionality, alignment, maintenance)
- Acknowledges uncertainty ("need to validate")
- Describes decision framework (≥80% threshold)
- 200-300 words typical

### Prescriptive Requests (Constraints and Requirements)

Explains why this specific implementation is needed:

```json
{
  "context": {
    "rationale": "We initially designed SAP-009 v1.0.0 for unidirectional translation (chora-base → external) because our first ecosystem integrations only needed read access to our artifacts. This simplified the initial implementation and avoided bidirectional complexity.\n\nHowever, ecosystem collaboration has evolved: chora-workspace and ecosystem-manifest now need to send coordination requests TO chora-base. Without bidirectional translation, they must manually craft chora-base-format JSON or use separate tooling, creating friction and inconsistency.\n\nExtending SAP-009 to v1.1.0 with bidirectional support is the most maintainable approach. Alternative solutions—like maintaining separate inbound/outbound translators or asking ecosystem repos to adopt chora-base schemas directly—would fragment the ecosystem and increase long-term maintenance burden. By extending SAP-009, we maintain a single translation protocol with clear versioning and backward compatibility."
  }
}
```

**Characteristics**:
- Explains original design decisions
- Describes changed requirements
- Compares alternatives (separate translators, schema adoption)
- Justifies chosen approach (maintainability, consistency)
- 150-250 words typical

### Peer Review Requests (Why External Review)

Explains why peer review is valuable for this work:

```json
{
  "context": {
    "rationale": "We could have published these React SAPs immediately, relying on our team's React expertise and industry best practices. However, as newcomers to the chora ecosystem, we recognize that technical correctness alone isn't sufficient—we need to ensure alignment with chora-base's established SAP patterns, documentation philosophy, and ecosystem conventions.\n\nExternal peer review from chora-base maintainers offers several benefits: (1) validation against proven SAP structures we may not have internalized yet, (2) identification of ecosystem-specific patterns we might have missed, and (3) relationship building through collaborative review. We've budgeted 2 weeks for review feedback and iteration, which fits our timeline while allowing thorough evaluation.\n\nAlternative approaches—like internal review only, or publishing then iterating based on user feedback—would risk introducing patterns that diverge from ecosystem standards, potentially confusing developers and creating technical debt that's harder to fix post-publication."
  }
}
```

**Characteristics**:
- Acknowledges capability but requests validation
- Lists specific benefits (validation, patterns, relationship)
- Describes resource commitment (2 weeks)
- Explains risks of alternatives (divergence, technical debt)
- 150-250 words typical

## Usage Guidance

### When Rationale Adds Value

**Use rationale when**:
- Multiple approaches exist (explain why this one)
- Request might seem obvious but isn't (explain non-obvious reasoning)
- Constraints limit options (explain what rules out alternatives)
- Prior attempts failed (explain lessons learned)
- Significant investment required (explain why it's worth it)

**Skip rationale when**:
- Request is straightforward with no obvious alternatives
- Background section already covers reasoning sufficiently
- Emergency request where speed trumps explanation (P0)

### Structure Options

#### Option 1: Alternatives-First
```
Paragraph 1: List alternatives considered
Paragraph 2: Explain chosen approach and why
Paragraph 3: Describe decision criteria or thresholds
```

#### Option 2: Constraints-First
```
Paragraph 1: Describe constraints or requirements
Paragraph 2: Explain how chosen approach satisfies constraints
Paragraph 3: Note alternatives ruled out by constraints
```

#### Option 3: Evolution-First
```
Paragraph 1: Describe original approach and its limitations
Paragraph 2: Explain what changed (new requirements, learnings)
Paragraph 3: Justify new approach in light of evolution
```

### Tone Guidelines

**For exploratory requests**:
- Acknowledge uncertainty: "We need to validate..."
- Present alternatives fairly: "Option A offers X but lacks Y"
- Describe decision framework: "If feasibility ≥80%, we'll..."

**For prescriptive requests**:
- Assert reasoning confidently: "This is the most maintainable approach"
- Explain constraints clearly: "Without X, we cannot Y"
- Show alternatives were considered: "We evaluated A, B, C and chose C because..."

**For peer reviews**:
- Express humility: "We recognize we may have missed..."
- Highlight collaboration value: "External perspective helps us..."
- Acknowledge alternatives: "We could publish now, but review reduces risk..."

### Common Patterns

#### The "Three Options" Pattern
```
We considered:
1. [Option A]: [Pros/Cons]
2. [Option B]: [Pros/Cons]
3. [Option C]: [Pros/Cons] ← Chosen

We're pursuing Option C because [key benefits] and [constraints met].
```

#### The "Evolution" Pattern
```
Originally, we [past approach] because [past context].
Now, [changed requirements/learnings].
Therefore, [new approach] is needed to [satisfy new requirements].
```

#### The "Validation" Pattern
```
We could [simpler alternative], but we want to ensure [quality dimension].
External [validation/review/expertise] provides [specific benefits].
This investment of [time/resources] reduces risk of [negative outcomes].
```

### Automation Notes

- **AI Generation**: Can draft rationale from context.background + user's decision history
- **Alternative Detection**: AI can prompt user: "Did you consider [obvious alternative]?"
- **Constraint Extraction**: AI can infer constraints from deliverables and acceptance criteria
- **Length Calibration**: Adjust based on request type (exploratory = longer, emergency = shorter)

## Validation Rules

- `context.rationale` field is **optional** (recommended for exploratory/prescriptive)
- Minimum 50 words if present (shorter suggests insufficient reasoning)
- Maximum 800 words (longer suggests need for separate design doc)
- Should mention alternatives or constraints (not just restate goals)
- Avoid pure repetition of background (rationale should add reasoning, not just facts)

## Related Content Blocks

- [context-background.md](context-background.md) - Situation and problem (complements rationale)
- [context-boundaries.md](context-boundaries.md) - What we're NOT requesting (negative rationale)
- [deliverables-structure.md](deliverables-structure.md) - What will be delivered (outcome of rationale)

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)

```json
{
  "context": {
    "rationale": "We considered three approaches to inbox artifact automation: (1) build custom tooling in chora-base, (2) adopt existing template engines like Jinja2 or Cookiecutter, or (3) integrate with chora-compose. Option 1 would give us full control but requires significant development and maintenance. Option 2 is simpler but lacks the MCP integration and ecosystem alignment we value.\n\nWe're pursuing Option 3 (chora-compose integration) because it offers the best balance of functionality, ecosystem synergy, and shared maintenance. chora-compose's 17 production generators demonstrate maturity, and MCP integration aligns with our vision for agent-assisted workflows. However, we need to validate technical feasibility before committing to this path.\n\nThis exploratory request will help us determine whether chora-compose's architecture can support our SAP-001 schemas, what effort is required, and whether integration makes sense for both teams. If feasibility is high (≥80%), we'll proceed to a 4-week pilot. If lower, we'll fall back to Option 2 (template engine) or Option 1 (custom tooling)."
  }
}
```

**Analysis**:
- Clear alternatives (3 options with pros/cons)
- Decision criteria (balance of functionality, synergy, maintenance)
- Acknowledges uncertainty (need to validate)
- Decision framework (≥80% threshold with fallbacks)
- 185 words (ideal exploratory length)

### Example 2: Prescriptive Request (COORD-2025-004)

```json
{
  "context": {
    "rationale": "We initially designed SAP-009 v1.0.0 for unidirectional translation because our first ecosystem integrations only needed read access. This simplified the initial implementation.\n\nHowever, ecosystem collaboration has evolved: chora-workspace and ecosystem-manifest now need to send coordination requests TO chora-base. Without bidirectional translation, they must manually craft chora-base-format JSON, creating friction.\n\nExtending SAP-009 to v1.1.0 is the most maintainable approach. Alternatives like separate translators or asking repos to adopt chora-base schemas would fragment the ecosystem. By extending SAP-009, we maintain a single protocol with clear versioning."
  }
}
```

**Analysis**:
- Evolution narrative (v1.0.0 → v1.1.0)
- Changed requirements (read-only → bidirectional)
- Alternatives dismissed (separate tools, schema adoption)
- Maintainability focus
- 110 words (concise prescriptive length)

### Example 3: Peer Review Request (coord-005)

```json
{
  "context": {
    "rationale": "We could publish these React SAPs immediately based on our team's React expertise. However, as newcomers to the chora ecosystem, we recognize that technical correctness alone isn't sufficient—we need alignment with chora-base's SAP patterns and documentation philosophy.\n\nExternal peer review offers: (1) validation against proven SAP structures, (2) identification of ecosystem-specific patterns we might have missed, and (3) relationship building. We've budgeted 2 weeks for feedback and iteration.\n\nAlternatives like internal review only, or publishing then iterating, would risk introducing patterns that diverge from ecosystem standards, potentially confusing developers and creating technical debt."
  }
}
```

**Analysis**:
- Acknowledges capability but requests validation
- Specific benefits (3 numbered items)
- Resource commitment (2 weeks)
- Risk of alternatives (divergence, confusion, debt)
- 120 words (focused peer review length)

## Common Anti-Patterns

### Anti-Pattern 1: Rationale Just Restates Background
**DON'T**:
```json
{
  "context": {
    "background": "We maintain SAP-001 inbox protocol. It's manual and time-intensive.",
    "rationale": "We maintain SAP-001 inbox protocol. Creating artifacts manually takes too long."
  }
}
```
**Problem**: Rationale adds no new information, just rewords background.

**DO**:
```json
{
  "context": {
    "background": "We maintain SAP-001 inbox protocol. It's manual and time-intensive.",
    "rationale": "We considered custom tooling, template engines, and chora-compose integration. We chose chora-compose because it offers ecosystem synergy and shared maintenance, but need to validate feasibility."
  }
}
```
**Fix**: Rationale explains decision-making process, not just facts.

### Anti-Pattern 2: Rationale Ignores Alternatives
**DON'T**:
```json
{
  "context": {
    "rationale": "We need bidirectional translation so we're implementing SAP-009 v1.1.0."
  }
}
```
**Problem**: No explanation of why this approach vs others.

**DO**:
```json
{
  "context": {
    "rationale": "We considered separate translators vs extending SAP-009. Separate tools would fragment maintenance. Extending SAP-009 keeps a single protocol with clear versioning."
  }
}
```
**Fix**: Acknowledges alternatives and explains choice.

### Anti-Pattern 3: Rationale is Too Detailed
**DON'T**:
```json
{
  "context": {
    "rationale": "[15 paragraphs detailing every technical consideration, benchmarks from 6 template engines, full decision matrix, implementation timeline...]"
  }
}
```
**Problem**: Rationale becomes design document, overwhelming recipient.

**DO**:
```json
{
  "context": {
    "rationale": "We evaluated 6 template engines (detailed analysis in docs/design/template-engine-comparison.md). chora-compose scored highest on ecosystem fit and MCP integration. We need to validate feasibility before committing."
  }
}
```
**Fix**: Summarize reasoning, link to detailed docs if needed.

## Metadata

- **Priority**: MEDIUM (valuable in 60-80% of requests, especially exploratory/prescriptive)
- **Stability**: Stable (rarely changes, reflects thinking at time of request)
- **Reusability**: Universal (pattern applies across artifact types)
- **Generation Source**: AI generation from context.background + user's decision criteria
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
