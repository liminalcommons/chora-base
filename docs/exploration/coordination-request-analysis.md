---
title: Coordination Request Pattern Analysis
type: analysis
trace_id: chora-compose-inbox-integration-2025
created: 2025-11-02
phase: week_2_decomposition
---

# Coordination Request Pattern Analysis

## Executive Summary

Analysis of 3 representative coordination requests (COORD-2025-002, COORD-2025-004, coord-005) to extract patterns for content block decomposition. Goal: Identify common structure vs variation points to inform template-driven generation.

**Key Findings**:
- **Universal fields** (100% present): type, request_id, title, from_repo, to_repo, priority, urgency, deliverables, acceptance_criteria
- **Common fields** (67-100%): context, trace_id, estimated_effort, timeline
- **Variable structure**: Exploratory vs prescriptive modes, question-based vs task-based
- **Quality markers**: Detailed context, specific deliverables, testable criteria, humble tone

---

## Sample Set

| Request ID | From → To | Type | Priority | Complexity | Lines |
|------------|-----------|------|----------|------------|-------|
| **COORD-2025-002** | chora-base → chora-compose | Exploratory (architecture_proposal) | Medium/Backlog | High | 213 |
| **COORD-2025-004** | chora-base → chora-base | Prescriptive (coordination) | P2/Next Sprint | Medium | 78 |
| **coord-005** | chora-workspace → chora-base | Peer Review (coordination) | P2/Next Sprint | Medium | 96 |

**Diversity**:
- Cross-repo (2025-002, coord-005) vs same-repo (2025-004)
- Exploratory vs prescriptive modes
- Architecture questions vs implementation tasks vs peer review
- 78-213 lines (2.7× variation)

---

## Common Structure (Universal Patterns)

### Core Metadata (100% present)

**Fields**:
```json
{
  "type": "coordination" | "architecture_proposal",
  "request_id": "COORD-YYYY-NNN" | "coord-NNN",
  "title": "string <100 chars",
  "from_repo": "string",
  "to_repo": "string" | "to_repos": ["array"],
  "priority": "P0" | "P1" | "P2" | "medium" | "high",
  "urgency": "blocks_sprint" | "next_sprint" | "backlog",
  "created": "YYYY-MM-DD" | "created_at": "ISO 8601"
}
```

**Observations**:
- `type`: Two variants ("coordination" standard, "architecture_proposal" for exploratory)
- `request_id`: Two formats (COORD-YYYY-NNN uppercase, coord-NNN lowercase)
- `priority`: Mixed enum (P0-P3 standard, "medium"/"high" legacy)
- `urgency`: Consistent enum (blocks_sprint, next_sprint, backlog)
- `created`: Two formats (YYYY-MM-DD date, ISO 8601 timestamp)
- `to_repo`: Single string OR array (multi-repo coordination)

**Template Priority**: HIGH - This is foundation of every request

### Deliverables (100% present)

**Pattern**:
```json
"deliverables": [
  "Specific deliverable 1 (with details)",
  "Specific deliverable 2 (with acceptance hints)",
  "Specific deliverable 3 (with format/location)",
  ...
]
```

**Characteristics**:
- Array of 5-11 items (average: 7)
- Each deliverable is specific, actionable string
- Often includes hints about format, location, or acceptance
- Good examples: "Enhanced SAP-009 protocol-spec.md (Section 9: Bidirectional Translation Layer)"
- Clarity varies: Some vague ("Guidance on SAP structure"), most specific

**Quality Markers**:
- Specific artifact names (SAP-009, protocol-spec.md)
- Parenthetical details (Section 9, Integration patterns)
- Quantification where possible (5 SAPs, ≥85% coverage)

**Template Priority**: HIGH - Critical for clarity and acceptance

### Acceptance Criteria (100% present)

**Pattern**:
```json
"acceptance_criteria": [
  "Criteria with measurable outcome",
  "Another criteria with specific threshold",
  "Behavior-based criteria (Given-When-Then)",
  ...
]
```

**Characteristics**:
- Array of 6-12 items (average: 9)
- Mix of quantitative (≥80%, ≥85% coverage) and qualitative
- Some use BDD format ("Generic agents can discover...")
- Some use simple assertions ("Documentation follows Diátaxis")

**Quality Markers**:
- Measurable thresholds (≥80%, ≥85%)
- Testable behaviors (can discover, gracefully degrade)
- Specific standards (Diátaxis framework, semantic versioning)
- No vague "should be good" criteria

**Template Priority**: HIGH - Essential for definition of done

---

## Common Fields (67-100% present)

### Context (100% present, variable structure)

**COORD-2025-002 Style** (Exploratory):
```json
"context": {
  "our_situation": "Background paragraph",
  "why_reaching_out": "Rationale paragraph",
  "not_assuming": "Clarifications paragraph",
  "our_vision": "Vision paragraph",
  "timeline": "No urgency statement"
}
```

**COORD-2025-004 Style** (Prescriptive):
```json
"context": {
  "background": "Background paragraph",
  "related_sap": "SAP-009",
  "traceability_context": "Emergence story"
}
```

**coord-005 Style** (Peer Review):
```json
"context": {
  "problem": "Problem statement",
  "what_emerged": "Solution summary",
  "why_now": "Timing rationale",
  "why_chora_base": "Why this repo",
  "not_asking": "Clarifications",
  "actually_asking": "Real question"
}
```

**Observations**:
- All 3 have "context" object, but keys differ
- Exploratory: Emphasizes "not assuming", "our vision", humble positioning
- Prescriptive: Straightforward "background", "related_sap"
- Peer Review: Emphasizes "problem", "why now", "what emerged"

**Common Elements**:
- Background/situation (100%)
- Rationale/why (100%)
- Clarifications/boundaries (67% - exploratory + peer review)
- Related work references (67%)

**Template Priority**: HIGH - But needs flexible structure

### Trace ID (67% present)

**Pattern**:
```json
"trace_id": "kebab-case-identifier"
```

**Examples**:
- "coord-2025-004-bidirectional" (structured)
- "ecosystem-coordination-saps-2025-10-31" (descriptive)
- Not present in COORD-2025-002 (33% without)

**Template Priority**: MEDIUM - Should auto-generate if not provided

### Estimated Effort (67% present)

**Pattern**:
```json
"estimated_effort": "16-24 hours over 1-2 sprints"
```

OR nested:
```json
"estimated_effort": {
  "chora_compose_side": { "quick_feedback": "30 minutes", ... },
  "chora_base_side": { "awaiting_response": "0 hours", ... }
}
```

**Observations**:
- Simple string (COORD-2025-004)
- Nested object for collaborative effort (COORD-2025-002)
- Missing in coord-005

**Template Priority**: MEDIUM - Nice to have, not critical

---

## Variable Fields (Domain-Specific)

### Questions (Exploratory Mode)

**CORD-2025-002 Only**:
```json
"questions_for_chora_compose": [
  {
    "category": "Vision & Scope",
    "questions": ["Q1", "Q2", ...]
  },
  {
    "category": "Current Capabilities",
    "questions": ["Q3", "Q4", ...]
  }
]
```

**Characteristics**:
- Grouped by category (4 categories, 14 total questions)
- Open-ended, exploratory
- Shows humble posture ("Have you considered...")

**Template Priority**: LOW - Only for exploratory mode

### Collaboration Modes (Exploratory Mode)

**COORD-2025-002 Only**:
```json
"collaboration_modes": [
  {
    "mode": "Quick Feedback",
    "description": "...",
    "outcome": "..."
  },
  ...
]
```

**Characteristics**:
- 5 modes (Quick Feedback, Discovery Call, Experiment, Redirect, Defer)
- Shows flexibility and respect for recipient's time
- Models humble collaboration

**Template Priority**: LOW - Only for exploratory mode

### What We Are NOT Requesting (Exploratory/Peer Review)

**Pattern** (67% - COORD-2025-002, coord-005):
```json
"what_we_are_NOT_requesting": [
  "Negative item 1",
  "Negative item 2",
  ...
]
```

**Characteristics**:
- Clarifies boundaries
- Prevents misunderstanding
- Models humble collaboration ("not asking you to accept as-is")

**Template Priority**: MEDIUM - Valuable for clarity, not always needed

### Specific Questions (Peer Review Mode)

**coord-005 Only**:
```json
"specific_questions": {
  "philosophy": ["Q1", "Q2", ...],
  "sap_structure": ["Q3", "Q4", ...],
  "template_integration": ["Q5", "Q6", ...],
  ...
}
```

**Characteristics**:
- Grouped by topic (5 groups, 21 total questions)
- Actionable and specific
- Guides reviewer's focus

**Template Priority**: LOW - Only for peer review mode

### Dependencies (Prescriptive Mode)

**COORD-2025-004 Only**:
```json
"dependencies": [
  "Foundation tools complete (DONE: Phase 1)",
  "Root AGENTS.md updated (DONE: +214 lines)",
  ...
]
```

**Characteristics**:
- Prerequisites and completion status
- Shows what's blocking or already done
- Technical and specific

**Template Priority**: MEDIUM - Important for sequencing

### Related (Prescriptive Mode)

**COORD-2025-004 Only**:
```json
"related": {
  "proposals": [],
  "rfcs": [],
  "issues": [],
  "documentation": ["doc1", "doc2"],
  "saps": ["SAP-001", "SAP-004", ...]
}
```

**Characteristics**:
- Links to related work
- Provides context for implementation
- Shows ecosystem awareness

**Template Priority**: MEDIUM - Valuable for context

---

## Quality Markers (High-Quality Examples)

### Detailed Context

**High Quality** (CORD-2025-002):
- Background: Explains "our_situation" (18 SAPs × 5 artifacts = maintenance burden)
- Rationale: "why_reaching_out" (name suggests composition, want to understand vision)
- Boundaries: "not_assuming" (acknowledges may not be in scope)
- Vision: "our_vision" (collections as higher-level holons)
- Timeline: "No urgency, v4.1.0 ships regardless"

**Characteristics**:
- Provides enough context for informed decision
- Acknowledges recipient's perspective
- Sets realistic expectations
- Shows humility ("if not in scope, that's fine")

### Specific Deliverables

**High Quality** (COORD-2025-004):
- "Enhanced SAP-009 protocol-spec.md (Section 9: Bidirectional Translation Layer)"
- "Enhanced SAP-009 ledger.md (v1.1.0 adoption tracking)"
- "BDD scenarios validating intent recognition, preference adaptation, pattern learning"

**Characteristics**:
- Names specific files/sections
- Includes version numbers or identifiers
- Describes what enhancement means (Section 9, v1.1.0)
- Provides context in parentheticals

### Measurable Acceptance Criteria

**High Quality** (COORD-2025-004):
- "Intent recognition accuracy ≥80% on test query set (30+ queries)"
- "Test coverage ≥85%"
- "All BDD scenarios pass (intent routing, glossary search, ...)"
- "No lint/type errors"

**Characteristics**:
- Quantitative thresholds (≥80%, ≥85%)
- Test set sizes specified (30+ queries)
- Specific test categories listed
- Binary checks (no errors)

### Humble Tone

**High Quality** (coord-005):
- "humble_acknowledgments" section
- "not_prescriptive": "you define SAPs"
- "learning_posture": "offering what emerged, seeking your discernment"
- "peer_not_subordinate": "Your 'no' is as valuable as 'yes'"

**Characteristics**:
- Acknowledges bounded rationality
- Explicit about not prescribing
- Positions as peer, not subordinate
- Values honest feedback over agreement

---

## Anti-Patterns (Lower-Quality Examples)

### Vague Deliverables

**Lower Quality** (coord-005):
- "Provide guidance on SAP structure" (what kind of guidance?)
- "Review tone shift" (review for what outcome?)

**Better**:
- "Guidance on SAP structure with specific recommendation: new SAPs (014/015) vs modify existing (001/009/010) vs hybrid, with rationale"
- "Review tone shift identifying specific instances of 'recruitment' language with suggested rewrites"

### Non-Testable Criteria

**Lower Quality** (coord-005):
- "Philosophy docs reviewed for accuracy, resonance, and completeness" (how to measure resonance?)
- "Tone audit identifies any remaining language" (how many instances is acceptable?)

**Better**:
- "Philosophy docs reviewed with feedback document (≥500 words) covering accuracy, alignment with commons values, and 3+ specific gaps identified"
- "Tone audit identifies ≤3 instances of 'recruitment' language in final docs"

### Generic Context

**Lower Quality** (Hypothetical):
```json
"context": {
  "background": "We need this feature for the project"
}
```

**Better**:
```json
"context": {
  "background": "18 SAPs × 5 artifacts × 8-12 hours = 720-1080 hours total maintenance burden. Exploring generation from content blocks to reduce effort while maintaining quality.",
  "related_sap": "SAP-000 defines 5-artifact pattern",
  "why_now": "v4.1.0 ships with SAP sets (storage-based), v4.2.0 explores generation-based approach"
}
```

---

## Variation Points (Template Placeholders)

### Always Variable (User-Provided)

1. **Title**: Unique per request
2. **From/To Repos**: Context-specific
3. **Priority/Urgency**: Based on impact assessment
4. **Deliverables**: Specific to request (5-11 items)
5. **Acceptance Criteria**: Testable outcomes (6-12 items)
6. **Context Background**: Problem/situation statement
7. **Trace ID**: Unique identifier

### Sometimes Variable (Context-Dependent)

8. **Collaboration Mode**: Exploratory vs Prescriptive vs Peer Review
9. **Questions**: If exploratory, 10-20 questions grouped by category
10. **Dependencies**: If prescriptive, what's blocking or done
11. **Related Work**: If prescriptive, links to docs/SAPs/issues
12. **What We're NOT Requesting**: If exploratory/peer review, boundaries
13. **Estimated Effort**: Simple string vs nested object
14. **Timeline**: Flexible vs specific delivery date

### Rarely Variable (Special Cases)

15. **Multi-Repo**: `to_repos` array vs `to_repo` string
16. **Metadata**: Additional fields like `requested_by`, `created_by`
17. **Success Metrics**: Explicit metrics array (COORD-2025-002 only)
18. **Review Format Options**: How to respond (coord-005 only)

---

## Decomposition Strategy

### Universal Blocks (All Coordination Requests)

1. **core-metadata.md**
   - type, request_id, title, created
   - Template with {{placeholders}}

2. **repository-fields.md**
   - from_repo, to_repo (or to_repos)
   - Handle single vs array

3. **priority-urgency.md**
   - priority (P0-P3), urgency (blocks_sprint, next_sprint, backlog)
   - Decision matrix/guidance

4. **deliverables-structure.md**
   - Array format
   - Quality examples (specific, with context)
   - Anti-patterns (vague, no details)

5. **acceptance-criteria-patterns.md**
   - Measurable criteria
   - BDD-style (Given-When-Then)
   - Quantitative thresholds
   - Binary checks

6. **trace-id-format.md**
   - Naming conventions (kebab-case)
   - Auto-generation rules
   - Examples

### Domain Blocks (Inbox Protocol)

7. **context-background.md**
   - Background/situation paragraph template
   - Problem statement patterns

8. **context-rationale.md**
   - Why this request, why now
   - Timing justification

9. **context-boundaries.md**
   - What we're NOT requesting
   - Clarifications

10. **estimated-effort-guide.md**
    - Simple string format
    - Nested object for collaborative effort
    - Estimation guidance

11. **timeline-patterns.md**
    - Flexible timeline language
    - Specific delivery dates
    - Sprint assignment

### Mode-Specific Blocks (Exploratory/Prescriptive/Peer Review)

12. **exploratory-questions.md**
    - Question grouping by category
    - Open-ended question patterns
    - Humble phrasing

13. **collaboration-modes.md**
    - Mode templates (Quick Feedback, Discovery Call, etc.)
    - Outcome expectations

14. **dependencies-pattern.md**
    - Prerequisites format
    - Completion status markers

15. **related-work-template.md**
    - Links to proposals, RFCs, issues, docs, SAPs
    - Cross-reference format

---

## Content Block Priorities

### HIGH Priority (Essential for All Requests)

- core-metadata.md ✅
- repository-fields.md ✅
- priority-urgency.md ✅
- deliverables-structure.md ✅
- acceptance-criteria-patterns.md ✅
- context-background.md ✅

### MEDIUM Priority (Common but Not Universal)

- trace-id-format.md
- context-rationale.md
- estimated-effort-guide.md
- timeline-patterns.md
- dependencies-pattern.md
- related-work-template.md

### LOW Priority (Mode-Specific)

- exploratory-questions.md
- collaboration-modes.md
- context-boundaries.md
- peer-review-format.md

---

## Template Generation Approach

### Step 1: Identify Mode

**User provides**: `collaboration_mode` = "exploratory" | "prescriptive" | "peer_review"

**Determines**:
- Which optional blocks to include
- Tone and phrasing
- Structure variations

### Step 2: Core Fields (Template Fill)

**Always Generated**:
```json
{
  "type": "coordination",
  "request_id": "{{auto_allocated}}",
  "title": "{{user.title}}",
  "created": "{{current_date}}",
  "from_repo": "{{user.from_repo}}",
  "to_repo": "{{user.to_repo}}",
  "priority": "{{user.priority}}",
  "urgency": "{{user.urgency}}"
}
```

### Step 3: Deliverables (AI-Augmented)

**Prompt**:
> Based on the following context, generate 5-7 specific, actionable deliverables following these patterns:
> - Name specific files/sections (e.g., "Enhanced SAP-009 protocol-spec.md (Section 9)")
> - Include version numbers where applicable
> - Add parenthetical details for clarity
> - Avoid vague language ("provide guidance" → "guidance with specific recommendations")
>
> Context: {{user.context.background}}
> Mode: {{collaboration_mode}}

**Output**: Array of 5-7 deliverable strings

### Step 4: Acceptance Criteria (AI-Augmented)

**Prompt**:
> Based on the following deliverables, generate 6-10 testable acceptance criteria following these patterns:
> - Use quantitative thresholds where possible (≥80%, ≥85%)
> - Specify test set sizes (30+ queries)
> - Use BDD format for behavioral criteria
> - Include binary checks (no lint/type errors)
> - Avoid vague criteria ("should be good" → "meets standard X")
>
> Deliverables: {{generated_deliverables}}

**Output**: Array of 6-10 criteria strings

### Step 5: Context (Template + AI)

**Template** (prescriptive mode):
```json
"context": {
  "background": "{{user.background}}",
  "related_sap": "{{user.related_sap}}",
  "traceability_context": "{{user.traceability}}"
}
```

**Template** (exploratory mode):
```json
"context": {
  "our_situation": "{{user.situation}}",
  "why_reaching_out": "{{user.rationale}}",
  "not_assuming": "{{generated_boundaries}}",
  "our_vision": "{{user.vision}}",
  "timeline": "{{user.timeline}}"
}
```

### Step 6: Optional Fields

**Include if user provides**:
- dependencies
- estimated_effort
- related work
- questions (exploratory)
- collaboration_modes (exploratory)

**Auto-generate**:
- trace_id (if not provided): `{{from_repo}}-{{to_repo}}-{{topic}}-{{date}}`
- created (if not provided): Current date

---

## Quality Checklist (Post-Generation Validation)

### Structural Completeness (100% Required)

- [ ] All required fields present (type, request_id, title, from_repo, to_repo, priority, urgency, deliverables, acceptance_criteria)
- [ ] JSON validates against schema
- [ ] Deliverables array has 5-11 items
- [ ] Acceptance criteria array has 6-12 items

### Content Quality (≥80% Target)

- [ ] Deliverables are specific (not vague)
- [ ] Deliverables include context (parentheticals, versions)
- [ ] Acceptance criteria are measurable
- [ ] Acceptance criteria have thresholds (≥80%, ≥85%)
- [ ] Context background is detailed (≥100 words)
- [ ] Tone is humble (if exploratory/peer review)

### Integration Compatibility (100% Required)

- [ ] inbox-status.py can parse (test with script)
- [ ] request_id follows format (coord-NNN or COORD-YYYY-NNN)
- [ ] priority/urgency use valid enums
- [ ] trace_id follows kebab-case convention

---

## Next Steps (Week 2)

1. **Create Content Blocks** (Task 2.2)
   - Use this analysis to decompose into 12-15 markdown files
   - Start with HIGH priority blocks (6 files)
   - Add MEDIUM priority blocks (6 files)
   - Add LOW priority blocks as needed (2-3 files)

2. **Create Context Schema** (Task 2.3)
   - Define required fields based on common patterns
   - Create 3 example contexts (simple, complex, urgent)
   - Map modes (exploratory, prescriptive, peer review)

3. **Document Rationale** (Task 2.4)
   - Explain granularity decisions (why 12-15 blocks?)
   - Justify reusability classification
   - Map to chora-compose patterns

---

## Appendix: Field Presence Matrix

| Field | COORD-2025-002 | COORD-2025-004 | coord-005 | Presence % |
|-------|----------------|----------------|-----------|------------|
| type | ✅ | ✅ | ✅ | 100% |
| request_id | ✅ | ✅ | ✅ | 100% |
| title | ✅ | ✅ | ✅ | 100% |
| from_repo | ✅ | ✅ | ✅ | 100% |
| to_repo(s) | ✅ | ✅ | ✅ | 100% |
| priority | ✅ | ✅ | ✅ | 100% |
| urgency | ✅ | ✅ | ✅ | 100% |
| created | ✅ | ✅ | ✅ | 100% |
| deliverables | ✅ | ✅ | ✅ | 100% |
| acceptance_criteria | ✅ | ✅ | ✅ | 100% |
| context | ✅ | ✅ | ✅ | 100% |
| trace_id | ❌ | ✅ | ✅ | 67% |
| estimated_effort | ✅ | ✅ | ❌ | 67% |
| dependencies | ❌ | ✅ | ❌ | 33% |
| related | ❌ | ✅ | ❌ | 33% |
| questions | ✅ | ❌ | ✅ | 67% |
| collaboration_modes | ✅ | ❌ | ❌ | 33% |
| what_we_are_NOT_requesting | ✅ | ❌ | ❌ | 33% |
| specific_questions | ❌ | ❌ | ✅ | 33% |
| requested_by | ❌ | ✅ | ❌ | 33% |
| success_metrics | ✅ | ❌ | ❌ | 33% |

**Observations**:
- 10 fields at 100% presence (universal)
- 3 fields at 67% presence (common)
- 9 fields at 33% presence (mode-specific or optional)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Status**: Complete (Week 2, Task 2.1)
**Next**: Content block decomposition (Task 2.2)
