# Acceptance Criteria Patterns Content Block

## Description

Measurable conditions that define when a coordination request is successfully completed. Acceptance criteria translate deliverables into verifiable tests, specifying **how to know** when each deliverable meets quality standards. They serve as the contract between requester and recipient.

**When to use**: Every coordination request to establish clear success conditions. Critical for avoiding scope creep and ensuring alignment.

## Fields / Structure

```json
{
  "acceptance_criteria": [
    "Measurable condition 1 with quantitative threshold",
    "Measurable condition 2 with verification method",
    "Measurable condition 3 with clear pass/fail"
  ]
}
```

### Field Specifications

- **acceptance_criteria**: Array of strings (2-20 items typical)
- Each criterion must be **objectively verifiable** (not subjective opinion)
- Should include quantitative thresholds where applicable (≥80%, <100ms, etc.)
- Phrased as positive conditions ("X passes Y" not "X doesn't fail Y")
- Maps to deliverables (but not necessarily 1:1)

## Template / Example

```json
{
  "acceptance_criteria": [
    "{{criterion_1}}",
    "{{criterion_2}}",
    "{{criterion_3}}"
  ]
}
```

## Variation Points

### Prescriptive Requests (Quantitative Verification)

Most specific form with measurable thresholds:

```json
{
  "acceptance_criteria": [
    "SAP-009 protocol specification includes bidirectional translation examples",
    "scripts/translate-bidirectional.py achieves ≥80% test coverage",
    "Integration tests pass for both chora-base → external and external → chora-base",
    "Translation performance benchmarks show <100ms for payloads ≤10KB",
    "CHANGELOG.md documents breaking changes with migration examples",
    "docs/skilled-awareness/INDEX.md links to SAP-009 v1.1.0",
    "inbox-status.py validates generated artifacts without errors",
    "JSON schema validation passes for all example configurations",
    "Error handling tests cover ≥5 edge cases (malformed input, version mismatch, etc.)",
    "Documentation review confirms ≥85% clarity score"
  ]
}
```

**Characteristics**:
- Quantitative thresholds (≥80%, <100ms, ≥85%)
- Tool-based verification (test coverage, benchmarks, validation scripts)
- Specific file references
- Clear pass/fail conditions
- 8-15 criteria typical

### Exploratory Requests (Qualitative Assessment)

Focus on completeness and utility of analysis:

```json
{
  "acceptance_criteria": [
    "Architecture analysis covers all 5 inbox artifact types (coordination, task, proposal, event, ecosystem)",
    "Feasibility assessment addresses technical, quality, and maintenance dimensions",
    "Integration options comparison includes effort estimates for each approach",
    "Recommendation includes clear GO/NO-GO/DEFER criteria",
    "Document structure follows Diátaxis framework (Explanation, How-To, Reference)",
    "Analysis references ≥3 real coordination request examples",
    "Pilot plan includes 4-week timeline with week-by-week deliverables"
  ]
}
```

**Characteristics**:
- Completeness checks (covers X, addresses Y, includes Z)
- Coverage thresholds (≥3 examples, all 5 types)
- Structure requirements (follows framework, includes sections)
- Decision-focused (clear criteria, recommendations)
- 4-10 criteria typical

### Peer Review Requests (Feedback Quality)

Focus on review depth and actionability:

```json
{
  "acceptance_criteria": [
    "Technical review covers architecture, patterns, and integration points",
    "Alignment assessment compares against ≥3 chora-base SAPs for consistency",
    "Recommendations include ≥5 specific, actionable improvement suggestions",
    "Edge case analysis identifies ≥3 potential issues with mitigation strategies",
    "Ecosystem pattern suggestions reference similar work in ≥2 other repos",
    "Review is constructive and includes specific examples (not just abstract feedback)",
    "Delivery timeline is ≤2 weeks from request acceptance"
  ]
}
```

**Characteristics**:
- Coverage requirements (covers X, compares Y)
- Quantity thresholds (≥5 suggestions, ≥3 issues)
- Quality constraints (specific, actionable, constructive)
- Reference requirements (≥2 repos, ≥3 SAPs)
- 5-10 criteria typical

## Usage Guidance

### SMART Criteria Framework

Apply SMART principles to each acceptance criterion:

- **Specific**: "Test coverage ≥80%" not "Good test coverage"
- **Measurable**: "≥5 edge cases" not "Several edge cases"
- **Achievable**: "≥80% coverage" not "100% coverage" (for complex systems)
- **Relevant**: Directly verifies a deliverable
- **Time-bound**: Use urgency/timeline fields, not acceptance criteria

### Quantitative Thresholds

**Common patterns**:
- Test coverage: `≥70%` (basic), `≥80%` (standard), `≥90%` (critical)
- Performance: `<100ms`, `<1s`, `<5s` (with payload size context)
- Documentation: `≥85%` clarity/completeness (from review rubric)
- Examples: `≥3` (exploration), `≥5` (comprehensive)
- Edge cases: `≥3` (basic), `≥5` (thorough)

**When to use**:
- Use quantitative when objectively measurable (tests, benchmarks, counts)
- Use qualitative when threshold doesn't add value ("passes validation" not "passes ≥95% of validation")

### Verification Methods

**Automated verification** (preferred when possible):
- "pytest passes with ≥80% coverage"
- "inbox-status.py validates without errors"
- "JSON schema validation passes"
- "Benchmark suite shows <100ms average"

**Manual verification** (when automation not feasible):
- "Documentation review confirms ≥85% clarity" (requires human judgment)
- "Peer review identifies ≥5 improvement suggestions" (subjective)
- "Examples demonstrate ≥3 real-world scenarios" (requires interpretation)

**Hybrid verification**:
- "Integration tests pass (automated) and manual testing confirms expected behavior (manual)"

### Mapping to Deliverables

**One deliverable → Multiple criteria**:
```json
{
  "deliverables": [
    "Implementation in scripts/translate-bidirectional.py with ≥80% test coverage"
  ],
  "acceptance_criteria": [
    "scripts/translate-bidirectional.py implements bidirectional translation protocol",
    "pytest passes with ≥80% line coverage",
    "Integration tests demonstrate both translation directions",
    "Performance benchmarks show <100ms for typical payloads"
  ]
}
```

**Multiple deliverables → One criterion**:
```json
{
  "deliverables": [
    "CHANGELOG.md entry",
    "Updated docs/skilled-awareness/INDEX.md",
    "README.md updates"
  ],
  "acceptance_criteria": [
    "All documentation files reference SAP-009 v1.1.0 consistently"
  ]
}
```

### Anti-Patterns

**DON'T**:
- Use subjective language: "Code is clean" → Use: "Linter passes without warnings"
- Specify process: "Have 3 review meetings" → Use: "Review identifies ≥5 improvements"
- Duplicate deliverables: "Create SAP-009" (deliverable) + "SAP-009 exists" (criterion)
- Use vague quantifiers: "Several examples" → Use: "≥3 examples"

**DO**:
- Use tool-based verification when possible
- Include both functional (does it work?) and quality (how well?) criteria
- Reference specific files, scripts, or validation methods
- Keep criteria independent (each verifiable separately)

### Phrasing Patterns

#### Test/Validation Criteria
- "[Tool/test] passes with [threshold]"
- "[Validation script] succeeds without errors"
- "[Metric] achieves [quantitative threshold]"

Examples:
- "pytest passes with ≥80% line coverage"
- "inbox-status.py validates generated artifacts without errors"
- "Performance benchmarks show <100ms average translation time"

#### Coverage Criteria
- "[Deliverable] covers [scope/dimensions]"
- "[Analysis] addresses [N] [topics/cases/scenarios]"
- "[Documentation] includes [sections/examples]"

Examples:
- "Architecture analysis covers all 5 inbox artifact types"
- "Error handling tests cover ≥5 edge cases"
- "Documentation includes ≥3 real-world examples"

#### Compliance Criteria
- "[Artifact] follows [standard/framework/pattern]"
- "[Implementation] adheres to [guideline] with [threshold]"
- "[Output] conforms to [schema/format]"

Examples:
- "Document structure follows Diátaxis framework"
- "JSON output conforms to inbox coordination schema"
- "Code adheres to PEP 8 with ≥95% linter compliance"

#### Reference Criteria
- "[Artifact] references [specific version/document]"
- "[Analysis] compares against [N] [examples/standards]"
- "[Review] cites [sources/precedents]"

Examples:
- "docs/INDEX.md links to SAP-009 v1.1.0"
- "Alignment assessment compares against ≥3 chora-base SAPs"
- "Recommendations reference similar patterns from ≥2 ecosystem repos"

### Automation Notes

- **AI Generation**: Draft criteria from deliverables, user should refine thresholds
- **Validation**: Check for measurability (flag subjective language)
- **Cross-reference**: Verify all deliverables have corresponding criteria
- **Threshold Realism**: Warn on extreme thresholds (100% coverage, 0ms latency)

## Validation Rules

- `acceptance_criteria` field is **required**
- Must be an array of strings
- Minimum 2 criteria (single criterion suggests incomplete specification)
- Maximum 25 criteria (over-specification)
- Each string should be 15-200 characters
- Should include quantitative thresholds where applicable
- Must be verifiable (either automated or via defined manual process)

## Related Content Blocks

- [deliverables-structure.md](deliverables-structure.md) - What needs to be created
- [context-background.md](context-background.md) - Why these criteria matter
- [priority-urgency.md](priority-urgency.md) - When verification happens

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)

```json
{
  "acceptance_criteria": [
    "Architecture analysis document covers inbox schemas, workflows, and processing infrastructure",
    "Analysis maps SAP-001 artifact types to chora-compose structures (content configs, collections, etc.)",
    "Feasibility assessment addresses technical alignment, quality potential, and maintenance burden",
    "Integration options comparison includes ≥2 approaches with effort estimates",
    "Recommendation includes clear GO/NO-GO/DEFER criteria based on technical feasibility and team capacity",
    "Documents follow Diátaxis framework with Explanation, How-To, and Reference sections",
    "Analysis references ≥3 real coordination request examples from chora-base inbox"
  ]
}
```

**Analysis**:
- 7 criteria covering completeness, structure, and quality
- Quantitative thresholds where applicable (≥2 approaches, ≥3 examples)
- Mix of coverage (covers X), mapping (maps Y to Z), and framework compliance
- Each criterion independently verifiable
- Maps to 4 deliverables (analysis, assessment, comparison, recommendation)

### Example 2: Prescriptive Request (COORD-2025-004)

```json
{
  "acceptance_criteria": [
    "SAP-009 v1.1.0 includes bidirectional translation protocol specification with examples",
    "scripts/translate-bidirectional.py achieves ≥80% test coverage (pytest)",
    "Integration tests pass for chora-base → external format translation",
    "Integration tests pass for external format → chora-base translation",
    "Performance benchmarks demonstrate <100ms translation time for payloads ≤10KB",
    "CHANGELOG.md documents v1.1.0 changes including breaking changes and migration path",
    "docs/skilled-awareness/INDEX.md links to SAP-009 v1.1.0",
    "inbox-status.py successfully validates all generated artifacts",
    "JSON schema validation passes for all example configurations",
    "Error handling tests cover ≥5 edge cases (malformed input, version mismatch, missing fields, invalid types, boundary conditions)",
    "Documentation clarity review achieves ≥85% score",
    "events.jsonl includes implementation_completed event with correct trace_id"
  ]
}
```

**Analysis**:
- 12 criteria (comprehensive prescriptive request)
- Heavy use of quantitative thresholds (≥80%, <100ms, ≥5, ≥85%)
- Tool-based verification preferred (pytest, inbox-status.py, schema validation)
- Specific version references (v1.1.0)
- Covers functionality, performance, documentation, and process compliance
- Maps to 10 deliverables

### Example 3: Peer Review Request (coord-005)

```json
{
  "acceptance_criteria": [
    "Technical review covers React SAP architecture, component patterns, and state management approaches",
    "Alignment assessment compares against ≥3 existing chora-base SAPs for consistency",
    "Recommendations include ≥5 specific, actionable improvement suggestions with examples",
    "Edge case analysis identifies ≥3 potential issues with proposed mitigation strategies",
    "Ecosystem pattern suggestions reference similar work in ≥2 other chora ecosystem repos",
    "Review feedback is constructive and includes specific code/documentation examples",
    "Review delivered within 2 weeks of request acceptance"
  ]
}
```

**Analysis**:
- 7 criteria focused on review quality and actionability
- Quantitative thresholds for thoroughness (≥3 SAPs, ≥5 suggestions, ≥3 issues, ≥2 repos)
- Quality constraints (specific, actionable, constructive, with examples)
- Timeline criterion (2 weeks) for accountability
- Maps to 5 deliverables (review, assessment, recommendations, identification, suggestions)

## Common Patterns by Request Type

| Request Type | Criteria Count | Quantitative Ratio | Verification Method | Examples |
|--------------|----------------|-------------------|---------------------|----------|
| Exploratory | 4-10 | 30-50% | Manual review, coverage checks | "≥3 examples", "covers all N types" |
| Prescriptive | 8-15 | 60-80% | Automated tests, benchmarks, validation scripts | "≥80% coverage", "<100ms", "passes validation" |
| Peer Review | 5-10 | 40-60% | Hybrid (manual review with quantitative targets) | "≥5 suggestions", "≥3 comparisons", "constructive" |
| Emergency (P0) | 2-5 | 70-90% | Automated validation, quick verification | "Vulnerability patched", "Hotfix deployed", "Tests pass" |

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Semi-stable (may evolve during clarification, frozen at acceptance)
- **Reusability**: Universal (pattern applies to tasks and proposals, with domain-specific criteria)
- **Generation Source**: AI generation from deliverables, user refinement of thresholds critical
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
