# Context Background Content Block

## Description

Provides situational context explaining **why** this coordination request exists. The background section helps recipients understand the requester's current situation, constraints, and motivations without requiring deep knowledge of their project. This is the narrative foundation that makes the request comprehensible and actionable.

**When to use**: Every coordination request, especially cross-repository requests where shared context cannot be assumed. Critical for building trust and facilitating productive collaboration.

## Fields / Structure

```json
{
  "context": {
    "background": "1-3 paragraph narrative explaining current situation, what led to this request, and why it matters. Should be self-contained and accessible to external readers."
  }
}
```

### Field Specifications

- **context.background**: String (150-800 words typical)
- Written as coherent narrative paragraphs (not bullet points)
- Assumes recipient has limited knowledge of requesting project
- Explains current state → problem/opportunity → why requesting coordination
- Avoids jargon or defines terms inline
- Sets the stage for more detailed context fields (rationale, questions, etc.)

## Template / Example

```json
{
  "context": {
    "background": "{{paragraph_1_current_situation}}\n\n{{paragraph_2_problem_or_opportunity}}\n\n{{paragraph_3_why_this_request}}"
  }
}
```

## Variation Points

### Exploratory Requests (Discovery Narrative)

Emphasizes learning, uncertainty, and open-ended exploration:

```json
{
  "context": {
    "background": "chora-base maintains SAP-001 (Inbox Coordination Protocol), which defines a 3-tier intake system for coordination requests, implementation tasks, and strategic proposals. Currently, creating these artifacts is a manual process: developers hand-craft JSON files with 15-20 required fields, ensuring schema compliance, consistent formatting, and proper event emission. While this works, it's time-intensive (30-60 minutes per coordination request) and error-prone.\n\nWe recently learned about chora-compose through ecosystem discussions and were intrigued by its approach to template-driven content generation. Our initial understanding was limited—we saw references in SAP-017/018 that suggested Docker orchestration, which didn't seem relevant. However, deeper research revealed that chora-compose is actually a content generation framework with 17 production generators and MCP integration, which could potentially automate our inbox artifact creation.\n\nBefore investing in integration work, we want to explore whether chora-compose is technically feasible and strategically aligned for inbox artifact automation. This request seeks your expertise in assessing compatibility between our SAP-001 schemas and your content generation architecture, understanding effort required, and determining whether a pilot makes sense for both teams."
  }
}
```

**Characteristics**:
- Explains current manual process and pain points
- Describes discovery journey ("recently learned", "initial understanding", "deeper research")
- Acknowledges uncertainty and need for expert input
- Ends with clear exploration goal
- 200-400 words typical

### Prescriptive Requests (Implementation Context)

Emphasizes specific needs, decisions already made, and clear objectives:

```json
{
  "context": {
    "background": "SAP-009 (Bidirectional Translation Layer) currently supports chora-base → external format translation, enabling our artifacts to be consumed by external tools. This unidirectional approach was appropriate for our initial ecosystem integrations (read-only consumption of our specs).\n\nHowever, we're now collaborating with chora-workspace and ecosystem-manifest, both of which need to send coordination requests TO chora-base (external format → chora-base). Our current SAP-009 v1.0.0 doesn't support inbound translation, creating a blocker for ecosystem coordination. We've committed to unblocking this in the current sprint (P1 priority, next_sprint urgency).\n\nThis request specifies the implementation requirements for SAP-009 v1.1.0, which extends the translation layer to support bidirectional flows. We've already designed the protocol extension and need implementation, testing, and documentation to complete the sprint deliverable."
  }
}
```

**Characteristics**:
- Explains current state and its limitations
- Describes specific blocker or requirement
- Indicates decisions already made ("we've committed", "we've designed")
- Clear implementation focus
- 150-300 words typical

### Peer Review Requests (Evaluation Context)

Emphasizes work completed and desire for external perspective:

```json
{
  "context": {
    "background": "chora-workspace has developed a comprehensive set of React-focused SAPs (SAP-020 through SAP-025) covering foundation patterns, state management, performance optimization, testing, styling, and linting. These SAPs are intended to serve as the definitive React guidance for the chora ecosystem, promoting consistency across projects.\n\nWe've invested significant effort in creating these SAPs, drawing from industry best practices and our team's React experience. However, as a relatively new member of the chora ecosystem, we want to ensure our SAPs align with chora-base's established documentation standards, SAP conventions, and ecosystem philosophy.\n\nWe're requesting a peer review from chora-base maintainers to validate technical accuracy, assess ecosystem alignment, and identify any gaps or anti-patterns we may have missed. Our goal is to produce SAPs that serve the broader ecosystem, not just our immediate project needs."
  }
}
```

**Characteristics**:
- Describes work completed and its scope
- Explains desire for validation ("ensure alignment", "want to validate")
- Acknowledges limitations ("relatively new", "may have missed")
- Emphasizes ecosystem service goal
- 150-300 words typical

## Usage Guidance

### Three-Paragraph Structure

**Paragraph 1: Current Situation**
- What exists today
- What we've been doing
- Current capabilities and constraints

Example opening:
- "chora-base maintains SAP-001 (Inbox Coordination Protocol), which..."
- "SAP-009 (Bidirectional Translation Layer) currently supports..."
- "chora-workspace has developed a comprehensive set of React-focused SAPs..."

**Paragraph 2: Problem or Opportunity**
- What changed or what we discovered
- The gap between current state and desired state
- Why the status quo is insufficient

Example transitions:
- "However, we recently learned that..."
- "This unidirectional approach creates a blocker when..."
- "As a relatively new ecosystem member, we want to ensure..."

**Paragraph 3: Why This Request**
- How this coordination request addresses the gap
- What we're specifically seeking from the recipient
- Expected outcome or next steps

Example closings:
- "This request seeks your expertise in assessing..."
- "We're requesting implementation of SAP-009 v1.1.0 to..."
- "We're asking for peer review to validate..."

### Tone and Voice

**For external repos (from_repo ≠ to_repo)**:
- Humble and collaborative (not demanding)
- Explain assumptions (don't assume shared knowledge)
- Acknowledge recipient's expertise
- Use "we're exploring" not "we need you to"

**For internal coordination (from_repo == to_repo)**:
- More direct and concise (shared context assumed)
- Can reference internal decisions and priorities
- Still explain reasoning (for future readers)
- Use "we're implementing" not "we're exploring"

### Accessibility Guidelines

Write for readers who:
- May not know your project's history
- May not understand your acronyms/jargon
- May have limited time (concise but complete)
- May revisit this request months later (self-contained)

**DO**:
- Define acronyms on first use: "SAP-001 (Inbox Coordination Protocol)"
- Explain context: "a 3-tier intake system for..." not just "SAP-001"
- Use concrete examples: "30-60 minutes per request" not "time-intensive"
- Link concepts: "which could potentially automate our inbox artifact creation"

**DON'T**:
- Use undefined acronyms: "SAP-001" without explanation
- Assume knowledge: "You know our inbox challenges"
- Be vague: "It's slow" vs "30-60 minutes per coordination request"
- Bury the lede: Start with context, not deep technical details

### Length Calibration

**Too short** (<100 words):
```json
{
  "context": {
    "background": "We need to integrate chora-compose with our inbox. Can you help us figure out if this is feasible?"
  }
}
```
**Problem**: No context on what inbox does, why integration matters, or what feasibility means.

**Too long** (>1000 words):
```json
{
  "context": {
    "background": "chora-base was created in Q2 2024 as a... [5 paragraphs of history]... and that's why we're now considering chora-compose integration."
  }
}
```
**Problem**: Recipient loses thread, background becomes documentation.

**Just right** (200-400 words):
```json
{
  "context": {
    "background": "chora-base maintains SAP-001 (Inbox Coordination Protocol)... [3 focused paragraphs]... This request seeks your expertise in assessing compatibility."
  }
}
```
**Benefit**: Complete context, accessible to external reader, focused on relevant history.

### Automation Notes

- **AI Generation**: Strong candidate for AI drafting from context.purpose + user's project knowledge
- **Personalization**: May need user refinement for tone (especially humble/collaborative voice)
- **Template Base**: Can provide structure ("Paragraph 1: Current situation...") for user to fill
- **Link to Other Context**: Background sets stage for rationale, questions, and collaboration modes

## Validation Rules

- `context.background` field is **required**
- Minimum 100 words (shorter suggests insufficient context)
- Maximum 1000 words (longer suggests need for separate design doc)
- Should be narrative paragraphs (not bullet points or lists)
- No markdown formatting required (plain text or simple markdown)

## Related Content Blocks

- [context-rationale.md](context-rationale.md) - Why this approach vs alternatives
- [exploratory-questions.md](exploratory-questions.md) - Specific questions arising from background
- [context-boundaries.md](context-boundaries.md) - What we're NOT requesting (complements background)
- [core-metadata.md](core-metadata.md) - Request identification

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)

```json
{
  "context": {
    "background": "chora-base maintains SAP-001 (Inbox Coordination Protocol), which defines a 3-tier intake system for coordination requests, implementation tasks, and strategic proposals. Currently, creating these artifacts is a manual process: developers hand-craft JSON files with 15-20 required fields, ensuring schema compliance, consistent formatting, and proper event emission. While this works, it's time-intensive (30-60 minutes per coordination request) and error-prone.\n\nWe recently learned about chora-compose through ecosystem discussions and were intrigued by its approach to template-driven content generation. Our initial understanding was limited—we saw references in SAP-017/018 that suggested Docker orchestration, which didn't seem relevant. However, deeper research revealed that chora-compose is actually a content generation framework with 17 production generators and MCP integration, which could potentially automate our inbox artifact creation.\n\nBefore investing in integration work, we want to explore whether chora-compose is technically feasible and strategically aligned for inbox artifact automation. This request seeks your expertise in assessing compatibility between our SAP-001 schemas and your content generation architecture, understanding effort required, and determining whether a pilot makes sense for both teams."
  }
}
```

**Analysis**:
- 3 paragraphs: current manual process → discovery journey → request goal
- Defines SAP-001 for external reader
- Concrete pain points (30-60 minutes, error-prone)
- Acknowledges initial misunderstanding (builds trust)
- Humble close ("seeks your expertise", "makes sense for both teams")
- 180 words (ideal exploratory length)

### Example 2: Prescriptive Request (COORD-2025-004)

```json
{
  "context": {
    "background": "SAP-009 (Bidirectional Translation Layer) currently supports chora-base → external format translation, enabling our artifacts to be consumed by external tools. This unidirectional approach was appropriate for our initial ecosystem integrations (read-only consumption of our specs).\n\nHowever, we're now collaborating with chora-workspace and ecosystem-manifest, both of which need to send coordination requests TO chora-base (external format → chora-base). Our current SAP-009 v1.0.0 doesn't support inbound translation, creating a blocker for ecosystem coordination. We've committed to unblocking this in the current sprint (P1 priority, next_sprint urgency).\n\nThis request specifies the implementation requirements for SAP-009 v1.1.0, which extends the translation layer to support bidirectional flows. We've already designed the protocol extension and need implementation, testing, and documentation to complete the sprint deliverable."
  }
}
```

**Analysis**:
- 3 paragraphs: current limitation → blocker → implementation request
- Explains technical context (unidirectional vs bidirectional)
- Specific blocker (ecosystem collaboration needs)
- Indicates decisions made (committed, designed)
- Direct tone appropriate for internal coordination
- 140 words (concise prescriptive length)

### Example 3: Peer Review Request (coord-005)

```json
{
  "context": {
    "background": "chora-workspace has developed a comprehensive set of React-focused SAPs (SAP-020 through SAP-025) covering foundation patterns, state management, performance optimization, testing, styling, and linting. These SAPs are intended to serve as the definitive React guidance for the chora ecosystem, promoting consistency across projects.\n\nWe've invested significant effort in creating these SAPs, drawing from industry best practices and our team's React experience. However, as a relatively new member of the chora ecosystem, we want to ensure our SAPs align with chora-base's established documentation standards, SAP conventions, and ecosystem philosophy.\n\nWe're requesting a peer review from chora-base maintainers to validate technical accuracy, assess ecosystem alignment, and identify any gaps or anti-patterns we may have missed. Our goal is to produce SAPs that serve the broader ecosystem, not just our immediate project needs."
  }
}
```

**Analysis**:
- 3 paragraphs: work completed → desire for validation → review request
- Describes scope (6 SAPs covering specific topics)
- Acknowledges position ("relatively new member")
- Humble tone ("want to ensure", "may have missed")
- Ecosystem service motivation (not just self-interest)
- 145 words (focused peer review length)

## Common Patterns by Request Type

| Request Type | Length | Tone | Focus | Typical Opening |
|--------------|--------|------|-------|-----------------|
| Exploratory | 200-400 words | Humble, curious | Discovery, learning | "We maintain X which currently..." |
| Prescriptive | 150-300 words | Direct, clear | Implementation, delivery | "X currently supports Y, but we need Z..." |
| Peer Review | 150-300 words | Humble, appreciative | Validation, improvement | "We've created X and want to ensure..." |
| Emergency (P0) | 100-200 words | Urgent, concise | Problem, impact | "X is currently broken, affecting..." |

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Stable (rarely changes after initial creation)
- **Reusability**: Universal (pattern applies across artifact types, content varies)
- **Generation Source**: AI generation from user's project context and request goals
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
