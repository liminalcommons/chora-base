# Exploratory Questions Content Block

## Description

Optional field containing specific questions the requester wants answered through coordination. Most common in **exploratory requests** where the goal is learning and discovery rather than prescriptive implementation. Questions help focus the exploration and provide clear success criteria.

**When to use**: Exploratory coordination requests seeking expertise, assessment, or recommendations. Rare in prescriptive requests (which specify deliverables instead). Present in ~33% of coordination requests overall, but ~80%+ of exploratory requests.

## Fields / Structure

```json
{
  "questions": [
    "Specific question 1?",
    "Specific question 2?",
    "Specific question 3?"
  ]
}
```

**Alternative structure** (grouped by topic):
```json
{
  "questions": {
    "Technical Feasibility": [
      "Question about technical compatibility?",
      "Question about integration approach?"
    ],
    "Effort and Timeline": [
      "Question about estimated effort?",
      "Question about timeline constraints?"
    ]
  }
}
```

### Field Specifications

- **questions**: Array of strings OR object with topic-grouped arrays
- Each question should be specific and answerable
- Phrased as questions (ending with `?`)
- 3-20 questions typical for exploratory requests
- May be grouped by topic/category for clarity

## Template / Example

**Simple array**:
```json
{
  "questions": [
    "{{question_1}}?",
    "{{question_2}}?",
    "{{question_3}}?"
  ]
}
```

**Grouped by topic**:
```json
{
  "questions": {
    "{{Topic_1}}": [
      "{{question_1_1}}?",
      "{{question_1_2}}?"
    ],
    "{{Topic_2}}": [
      "{{question_2_1}}?",
      "{{question_2_2}}?"
    ]
  }
}
```

## Variation Points

### Exploratory Request (Technical Assessment)

Questions focused on feasibility, architecture, and integration:

```json
{
  "questions": {
    "Architecture and Compatibility": [
      "Can chora-compose's content config structure support SAP-001's 18 required fields?",
      "How do content elements map to our inbox artifact types (coordination, task, proposal)?",
      "Does chora-compose support conditional content (e.g., optional fields that vary by request type)?"
    ],
    "Generation Quality": [
      "What quality level can we expect from template-based generation vs AI-augmented generation?",
      "How do existing chora-compose generators handle structured JSON output?",
      "Can we achieve ≥80% quality threshold for inbox artifacts?"
    ],
    "Effort and Integration": [
      "What effort is required to create content configs for coordination requests?",
      "How would chora-compose integration affect our existing inbox processing scripts?",
      "What maintenance burden would we inherit?"
    ],
    "MCP and Tooling": [
      "How does MCP integration work in practice for content generation?",
      "What developer experience improvements does chora-compose provide?",
      "Are there examples of similar structured artifact generation we can learn from?"
    ]
  }
}
```

**Characteristics**:
- 14 questions grouped into 4 topics
- Mix of yes/no and open-ended questions
- Specific technical details (18 fields, ≥80% threshold)
- Covers feasibility, quality, effort, and tooling
- Typical for comprehensive exploration

### Peer Review Request (Feedback Questions)

Questions focused on assessment and improvement:

```json
{
  "questions": {
    "Technical Accuracy": [
      "Are the React patterns we've documented current and best-practice?",
      "Have we missed any critical edge cases or anti-patterns?",
      "Do our component architecture recommendations align with chora-base patterns?"
    ],
    "Documentation Quality": [
      "Is the documentation structure clear and followable?",
      "Are our examples sufficient and realistic?",
      "What areas would benefit from more depth or clarity?"
    ],
    "Ecosystem Alignment": [
      "Do these SAPs fit well with other chora-base SAPs?",
      "Are there conflicting recommendations with existing ecosystem patterns?",
      "What patterns could be extracted for ecosystem-wide reuse?"
    ]
  }
}
```

**Characteristics**:
- 9 questions grouped into 3 topics
- All seek reviewer's expert judgment
- Balance specific (patterns, examples) and general (clarity, alignment)
- Typical for peer review requests

### Focused Exploration (Narrow Scope)

Small number of specific questions for targeted learning:

```json
{
  "questions": [
    "Does chora-compose support ephemeral storage for draft artifacts?",
    "What's the typical development cycle time for creating a new content config?",
    "How would we handle post-generation validation and event emission?"
  ]
}
```

**Characteristics**:
- 3 focused questions (not grouped)
- Very specific technical points
- Appropriate for narrow-scope exploration
- Quick to answer (1-2 hours investigation)

### No Questions (Prescriptive Request)

Prescriptive requests typically omit questions field:

```json
{
  "questions": null
}
```
*Note: Field omitted entirely*

**Rationale**: Prescriptive requests use deliverables and acceptance criteria instead of questions.

## Usage Guidance

### Question Quality

**Good questions** (specific, answerable, actionable):
```
✓ "Can chora-compose support conditional content based on request type (coordination vs task)?"
✓ "What effort is required to create 10-15 content configs for coordination requests?"
✓ "How do existing generators achieve structured JSON output with schema validation?"
```

**Poor questions** (vague, unanswerable, too broad):
```
✗ "Is chora-compose good?"
✗ "How does everything work?"
✗ "What should we do?"
```

### Question Types

**Yes/No questions** (binary feasibility):
```
"Can chora-compose support SAP-001's 18 required fields?"
"Does MCP integration work with structured JSON generation?"
```
- Quick to answer
- Good for go/no-go decisions
- May need follow-up for details

**How questions** (process and approach):
```
"How do content elements map to inbox artifact types?"
"How would integration affect existing processing scripts?"
```
- Require explanation
- Uncover process details
- Often most valuable for learning

**What questions** (information gathering):
```
"What quality level can we expect from template-based generation?"
"What maintenance burden would we inherit?"
```
- Broad information gathering
- May need scoping
- Good for understanding landscape

**Why questions** (rationale and reasoning):
```
"Why do some generators use template_fill vs demonstration patterns?"
"Why does chora-compose use ephemeral storage for drafts?"
```
- Uncover design decisions
- Build deeper understanding
- May reveal non-obvious constraints

### Grouping Strategy

**When to group** (≥6 questions):
- Helps recipient organize response
- Makes patterns clear (e.g., "all architecture questions together")
- Enables parallel investigation (different people handle different topics)

**When NOT to group** (≤5 questions):
- Grouping overhead outweighs benefit
- Questions flow naturally in sequence
- Single coherent topic

**Grouping dimensions**:
- By topic: Architecture, Quality, Effort, Tooling
- By stakeholder: Technical team, Users, Maintainers
- By time: Immediate questions, Follow-up questions, Future questions
- By type: Feasibility, Comparison, Process

### Question Quantity

**Too few** (<3 for exploratory request):
```json
{
  "questions": [
    "Can we use chora-compose for inbox?"
  ]
}
```
**Issue**: Too vague, doesn't focus exploration.

**Too many** (>25):
```json
{
  "questions": [
    "Question 1?", "Question 2?", ..., "Question 30?"
  ]
}
```
**Issue**: Overwhelming, suggests request is too broad.

**Just right** (5-15 for comprehensive exploration):
```json
{
  "questions": {
    "Topic 1": ["Q1?", "Q2?", "Q3?"],
    "Topic 2": ["Q4?", "Q5?", "Q6?"],
    "Topic 3": ["Q7?", "Q8?"]
  }
}
```
**Benefit**: Comprehensive but manageable, organized by topic.

### Questions vs Deliverables

**Questions** (exploratory requests):
```json
{
  "questions": [
    "Can chora-compose support SAP-001 schemas?",
    "What effort is required for integration?",
    "What quality level can we achieve?"
  ],
  "deliverables": [
    "Feasibility assessment answering the above questions",
    "Integration options comparison",
    "Recommendation on whether to proceed"
  ]
}
```
Questions drive exploration; deliverables specify output format.

**Deliverables only** (prescriptive requests):
```json
{
  "deliverables": [
    "SAP-009 v1.1.0 specification",
    "Implementation with ≥80% test coverage",
    "Documentation updates"
  ]
}
```
No questions needed; deliverables are concrete.

### Automation Notes

- **AI Generation**: Can generate questions from context.background and deliverables
- **Grouping**: AI can suggest groupings based on question topics
- **Quality Check**: Flag vague questions ("Is it good?") for user refinement
- **Answer Mapping**: AI can draft answers based on research, for user validation

## Validation Rules

- `questions` field is **optional** (common in exploratory, rare in prescriptive)
- If present, must be array of strings OR object with string array values
- Each question should end with `?` (question mark)
- Recommended 3-20 questions for exploratory requests
- Questions should be specific and answerable
- Avoid duplicate questions

## Related Content Blocks

- [deliverables-structure.md](deliverables-structure.md) - Output format for answering questions
- [context-background.md](context-background.md) - Context that generates questions
- [acceptance-criteria-patterns.md](acceptance-criteria-patterns.md) - How to verify questions were answered

## Examples from Real Requests

### Example 1: Comprehensive Exploratory Request (COORD-2025-002)

```json
{
  "questions": {
    "Architecture and Compatibility": [
      "Can chora-compose's content config structure support SAP-001's 18 required fields for coordination requests?",
      "How do ContentElements and GenerationPatterns map to our inbox artifact types (coordination, task, proposal)?",
      "Does chora-compose support conditional content (e.g., optional fields that vary by request subtype)?",
      "How would we handle complex nested structures like context.questions or deliverables arrays?"
    ],
    "Generation Quality and Patterns": [
      "What quality level can we expect from template-based generation vs AI-augmented generation?",
      "How do existing chora-compose generators handle structured JSON output with schema validation?",
      "Can we achieve ≥80% quality threshold (SAP-004 rubric) for inbox artifacts?",
      "What's the balance between deterministic templates and flexible AI generation?"
    ],
    "Effort and Integration": [
      "What effort is required to create content configs for coordination requests (estimated 10-15 content blocks)?",
      "How would chora-compose integration affect our existing inbox processing scripts (inbox-status.py, validation, events)?",
      "What maintenance burden would we inherit (content block updates, version compatibility)?",
      "Can we do a phased rollout (coordination requests first, then tasks and proposals)?"
    ],
    "MCP and Developer Experience": [
      "How does MCP integration work in practice for structured content generation?",
      "What developer experience improvements does chora-compose provide over manual JSON creation?",
      "Are there examples of similar structured artifact generation (JSON with schemas) we can learn from?",
      "How do we balance automation benefits vs learning curve for new contributors?"
    ]
  }
}
```

**Analysis**:
- 14 questions grouped into 4 topics
- Highly specific (mentions SAP-001, 18 fields, ≥80% threshold, SAP-004 rubric)
- Mix of technical feasibility, quality assessment, and practical concerns
- Each topic has 3-4 questions (balanced)
- Questions inform deliverables (feasibility assessment, options comparison, recommendation)

### Example 2: Peer Review Request (coord-005)

```json
{
  "questions": {
    "Technical Review": [
      "Are the React patterns we've documented (SAP-020 through SAP-025) current and aligned with industry best practices?",
      "Have we missed any critical edge cases, anti-patterns, or performance pitfalls?",
      "Do our component architecture recommendations align with chora-base's architectural philosophy?"
    ],
    "Documentation Quality": [
      "Is the SAP structure (Explanation, How-To, Reference) clear and easy to follow?",
      "Are our code examples sufficient, realistic, and properly explained?",
      "What sections or topics would benefit from more depth, clarity, or examples?"
    ],
    "Ecosystem Alignment": [
      "Do these React SAPs integrate well with existing chora-base SAPs (conventions, terminology, style)?",
      "Are there any conflicting recommendations between our SAPs and established ecosystem patterns?",
      "What patterns or content could be extracted for ecosystem-wide reuse (shared across repos)?",
      "How can we better align our work with the broader chora ecosystem vision?"
    ],
    "Onboarding and Accessibility": [
      "How accessible are these SAPs to developers new to React or the chora ecosystem?",
      "What prerequisites or background knowledge should we document more clearly?",
      "Are there gaps in our progressive disclosure (basic → intermediate → advanced patterns)?"
    ]
  }
}
```

**Analysis**:
- 13 questions grouped into 4 topics
- Focuses on review criteria (technical accuracy, quality, alignment, accessibility)
- Mix of specific (SAP-020-025, code examples) and general (ecosystem vision)
- Each topic has 3-4 questions
- Questions guide peer review scope and depth

### Example 3: Focused Exploration (Hypothetical)

```json
{
  "questions": [
    "Does chora-compose support ephemeral storage for draft artifacts (versioned by timestamp)?",
    "What's the typical development cycle time for creating and testing a new content config?",
    "How would we handle post-generation validation (JSON schema) and event emission (events.jsonl)?"
  ]
}
```

**Analysis**:
- 3 focused questions (no grouping needed)
- Very specific technical points
- Appropriate for narrow-scope, quick exploration (4-6 hours)
- Each question addresses specific integration concern

### Example 4: No Questions (Prescriptive Request - COORD-2025-004)

```json
{
  "questions": null
}
```
*Note: Field omitted entirely*

**Analysis**:
- Prescriptive request specifies exact deliverables instead
- No need for questions (requirements are clear)
- Uses deliverables + acceptance_criteria to define scope

## Common Patterns by Request Type

| Request Type | Questions Present? | Typical Count | Grouping | Focus |
|--------------|-------------------|---------------|----------|-------|
| Exploratory | 80%+ | 8-15 | Usually grouped (3-5 topics) | Feasibility, quality, effort, approach |
| Prescriptive | <10% | 0-3 | Rarely grouped | Clarification only (deliverables specify most) |
| Peer Review | 60-70% | 5-12 | Sometimes grouped (2-4 topics) | Quality, alignment, gaps, improvements |
| Emergency (P0) | <5% | 0-2 | Never grouped | Root cause, impact only |

## Questions and Acceptance Criteria

Questions often map to acceptance criteria:

**Questions**:
```json
{
  "questions": [
    "Can chora-compose support SAP-001's 18 required fields?",
    "What effort is required for integration?",
    "Can we achieve ≥80% quality threshold?"
  ]
}
```

**Corresponding Acceptance Criteria**:
```json
{
  "acceptance_criteria": [
    "Feasibility assessment addresses all 18 SAP-001 fields with specific mapping to chora-compose structures",
    "Effort estimate includes breakdown by deliverable with range (N-M hours)",
    "Quality analysis references SAP-004 rubric and provides threshold prediction with evidence"
  ]
}
```

**Pattern**: Each question → corresponding acceptance criterion that defines how to answer it.

## Metadata

- **Priority**: LOW (present in ~33% overall, but HIGH in exploratory requests ~80%)
- **Stability**: Stable (rarely changes, though may be refined during clarification)
- **Reusability**: Moderate (pattern applies to tasks/proposals, but content highly request-specific)
- **Generation Source**: AI generation from context.background + exploration goals, user refinement
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
