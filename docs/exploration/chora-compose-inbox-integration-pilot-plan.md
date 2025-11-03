---
title: Pilot Project - Inbox Artifact Generation with chora-compose
type: pilot-plan
status: 🧪 Approved
timeline: 4 weeks (Weeks 2-5, Nov 9 - Dec 6, 2025)
effort: 28-42 hours (chora-base)
trace_id: chora-compose-inbox-integration-2025
created: 2025-11-02
phase: week_2_decomposition
---

# Pilot Project: Inbox Artifact Generation with chora-compose

**Status**: 🧪 Approved (2025-11-02)
**Timeline**: 4 weeks (Weeks 2-5, starting ~2025-11-09)
**Effort**: 28-42 hours (chora-base), coordination with chora-compose
**Trace ID**: `chora-compose-inbox-integration-2025`
**Decision Point**: Week 5 (Dec 6, 2025)

---

## Executive Summary

This pilot validates that chora-compose can generate inbox coordination request artifacts meeting chora-base's quality bar (80%+ of hand-written quality) with significant time reduction (50%+). Success enables full implementation across all inbox artifact types; failure provides clear learnings for alternative approaches.

**Key Metrics**:
- **Quality Target**: ≥80% (weighted rubric score)
- **Time Reduction Target**: ≥50% (manual 30-60 min → automated ≤15 min)
- **Validation Target**: 100% (JSON Schema pass, inbox-status.py compatibility)

---

## Goal

Validate that chora-compose can generate inbox coordination request artifacts meeting our quality bar (80%+ of hand-written quality) with 50%+ time reduction.

**Validation Questions**:
1. Can chora-compose generate structurally valid coordination requests? (JSON Schema 100% pass)
2. Does generated content match hand-written quality? (≥80% on 10-criterion rubric)
3. Is generation faster than manual creation? (≥50% time reduction)
4. Does generated output integrate with existing tools? (inbox-status.py 100% compatibility)
5. Is the approach scalable to other artifact types? (clear extension path)

---

## Pilot Artifact: Coordination Requests

### Why Coordination Requests?

**Strategic Fit**:
- ✅ Well-defined structure (18 required fields, JSON Schema validation)
- ✅ Medium complexity (not too simple like metadata, not too complex like proposals)
- ✅ Highest value (30-60 min manual → 5-10 min automated = 70-83% reduction potential)
- ✅ Reusable patterns across ecosystem (chora-workspace, ecosystem-manifest can adopt)
- ✅ Clear quality validation (JSON Schema + inbox-status.py compatibility)

**Current State**:
- Manual JSON creation (~200 lines, 18+ required fields)
- Takes 30-60 minutes per request (research, writing, validation)
- Error-prone (missing fields, inconsistent structure)
- Example files:
  - `inbox/incoming/coordination/COORD-2025-002-chora-compose-exploration.json`
  - `inbox/incoming/coordination/COORD-2025-004-bidirectional-integration.json`
  - `inbox/coordination/coord-005-sap-peer-review.json`

**Target State**:
- Generate from content blocks + user-provided context
- Quality ≥ 80% vs hand-written examples
- Generation time < 15 minutes (including user input and review)
- 100% JSON Schema validation pass rate
- 100% inbox-status.py compatibility

---

## Timeline (4-Week Pilot)

| Week | Dates | Phase | Effort | Key Deliverable | Owner |
|------|-------|-------|--------|-----------------|-------|
| **Week 2** | Nov 9-15 | Content Block Decomposition | 8-12 hours | 10-15 content blocks | chora-base |
| **Week 3** | Nov 16-22 | Content Config Creation (DDD) | 10-14 hours | Content config + change request | chora-base + chora-compose |
| **Week 4** | Nov 23-29 | Generation & Validation (BDD+TDD) | 10-16 hours | 5 test cases + quality scores | Both teams |
| **Decision** | Dec 6 | Go/No-Go Decision | 1-2 hours | Decision document | chora-base |

**Total Effort**: 28-42 hours over 4 weeks

---

## Week 2: Content Block Decomposition (8-12 hours)

### Objective
Decompose coordination request structure into reusable content blocks and define context schema for generation.

### Tasks

#### Task 2.1: Analyze Example Coordination Requests (2-3 hours)

**Action**:
- Read 3-5 existing coordination requests:
  - COORD-2025-002 (exploratory, architecture questions)
  - COORD-2025-004 (bidirectional integration)
  - coord-005 (SAP peer review)
  - coord-001 (if exists - chora-base to chora-compose)
  - Any completed coordination requests in `inbox/completed/`
- Extract patterns:
  - Common sections (metadata, context, deliverables, criteria)
  - Variation points (from_repo, to_repo, problem domain)
  - Quality examples vs lower-quality examples
- Map to content block granularity

**Deliverable**: `docs/exploration/coordination-request-analysis.md`
- Pattern extraction (what's common vs unique)
- Variation points documented
- Quality characteristics identified

#### Task 2.2: Decompose into Content Blocks (4-6 hours)

**Action**:
Create 10-15 markdown content block files organized by reusability:

**Universal Blocks** (reusable across all coordination requests):
1. `core-metadata.md` - Standard fields (id, type, title, priority, urgency, created)
2. `repository-fields.md` - from_repo, to_repo patterns
3. `trace-id-format.md` - Trace ID naming conventions

**Domain Blocks** (reusable within inbox protocol):
4. `deliverables-structure.md` - Array format + guidance
5. `acceptance-criteria-gherkin.md` - Given-When-Then patterns
6. `context-background.md` - Background section template
7. `context-waypoint.md` - Waypoint linkage patterns
8. `dependencies-pattern.md` - Prerequisites/blockers structure
9. `estimated-effort-guide.md` - Effort estimation patterns
10. `priority-urgency-matrix.md` - Priority/urgency decision guide

**Artifact-Specific Blocks** (unique to coordination requests):
11. `collaboration-modes.md` - Collaboration patterns (exploratory, prescriptive, etc.)
12. `success-metrics.md` - Metrics template for coordination
13. `cross-repo-patterns.md` - Multi-repo coordination examples
14. `related-saps-linkage.md` - How to reference related SAPs
15. `timeline-patterns.md` - Requested delivery timeline examples

**File Structure**:
```
docs/content-blocks/
  ├── inbox-coordination/
  │   ├── core-metadata.md
  │   ├── repository-fields.md
  │   ├── deliverables-structure.md
  │   ├── acceptance-criteria-gherkin.md
  │   ├── context-background.md
  │   ├── context-waypoint.md
  │   ├── dependencies-pattern.md
  │   ├── estimated-effort-guide.md
  │   ├── collaboration-modes.md
  │   ├── success-metrics.md
  │   ├── cross-repo-patterns.md
  │   ├── related-saps-linkage.md
  │   └── timeline-patterns.md
  └── shared/
      ├── trace-id-format.md
      └── priority-urgency-matrix.md
```

**Content Block Template**:
```markdown
# [Block Name]

## Description
[What this represents, when to use it]

## Fields / Structure
[Field names, types, constraints]

## Template / Example
[Literal content or template with {{placeholders}}]

## Variation Points
[What changes between uses]

## Usage Guidance
[How to customize, when to override]
```

**Deliverable**: 10-15 markdown content block files

#### Task 2.3: Create Context Schema (2-3 hours)

**Action**:
Define required context fields for generation:

**Context Schema**:
```json
{
  "request_metadata": {
    "from_repo": "string (required)",
    "to_repo": "string (required)",
    "priority": "P0 | P1 | P2 | P3 (required)",
    "urgency": "blocks_sprint | next_sprint | backlog (required)",
    "title": "string <80 chars (required)",
    "created": "YYYY-MM-DD (optional, defaults to current)"
  },
  "coordination_context": {
    "waypoint": "string (optional, e.g., 'W3', 'Q4-2025')",
    "related_saps": "array of SAP IDs (optional)",
    "background": "string (required, problem context)",
    "collaboration_mode": "exploratory | prescriptive | hybrid (optional)"
  },
  "deliverables": "array of strings (required, 2-10 items)",
  "acceptance_criteria": "array of strings (required, Given-When-Then format)",
  "timeline": {
    "requested_delivery": "string (optional, e.g., 'Week 10', 'Sprint 5')",
    "estimated_effort": "string (optional, e.g., '6-8 hours')"
  },
  "dependencies": {
    "prerequisites": "array of strings (optional)",
    "blocks": "array of strings (optional)"
  },
  "trace_id": "string (optional, auto-generated if not provided)"
}
```

**Create 3 Example Context Files**:

1. **Simple Request** (`context-examples/coordination/simple-request-context.json`):
   - Minimal deliverables (2-3 items)
   - No dependencies
   - Single repo interaction

2. **Complex Request** (`context-examples/coordination/complex-request-context.json`):
   - 10+ deliverables
   - Multi-repo coordination
   - Multiple dependencies
   - Strategic waypoint linkage

3. **Urgent Request** (`context-examples/coordination/urgent-request-context.json`):
   - P0 priority
   - blocks_sprint urgency
   - Short timeline
   - Minimal context (fast creation needed)

**Deliverable**:
- Context schema documentation
- 3 example context JSON files

#### Task 2.4: Document Decomposition Rationale (1-2 hours)

**Action**:
Create rationale document explaining decomposition decisions:

**Sections**:
1. **Granularity Decisions**
   - Why 5-7 elements per content config?
   - When to split into child configs?
   - Element vs content config vs artifact

2. **Reusability Classification**
   - Universal (across all inbox artifacts)
   - Domain (within inbox protocol)
   - Artifact-specific (coordination requests only)

3. **Mapping to chora-compose Patterns**
   - How content blocks → ContentElements
   - How context schema → InputSources
   - How templates → GenerationPatterns

4. **Design Principles**
   - Template-first (deterministic quality baseline)
   - AI-augmented (flexibility where needed)
   - Validation-enforced (JSON Schema, required fields)

**Deliverable**: `docs/exploration/decomposition-rationale.md`

### Week 2 Exit Criteria

- [ ] ✅ 10-15 content block files created in `docs/content-blocks/`
- [ ] ✅ Context schema defined and documented
- [ ] ✅ 3 example context files created
- [ ] ✅ Decomposition rationale documented
- [ ] ✅ Coordination request analysis complete
- [ ] ✅ Technical lead approval obtained

**Decision Checkpoint**: If decomposition unclear or taking >12 hours, simplify to 5-7 essential blocks and iterate.

---

## Week 3: Content Config Creation (DDD Phase) (10-14 hours)

### Objective
Create chora-compose content configuration and document design through DDD change request.

### Tasks

#### Task 3.1: Create Content Configuration (4-6 hours)

**Action**:
Create chora-compose content config file integrating content blocks.

**File**: `configs/content/coordination-request/coordination-request-content.json`

**Structure**:
```json
{
  "metadata": {
    "id": "coordination-request",
    "title": "Coordination Request Generator",
    "description": "Generate SAP-001 coordination request JSON artifacts",
    "version": "1.0.0",
    "artifact_type": "coordination_request"
  },
  "elements": [
    {
      "name": "core_metadata",
      "description": "Standard metadata fields",
      "format": "json",
      "generation_source": "template",
      "required": true
    },
    {
      "name": "repository_fields",
      "description": "Source and target repositories",
      "format": "json",
      "generation_source": "template",
      "required": true
    },
    {
      "name": "context_section",
      "description": "Background, waypoint, related work",
      "format": "json",
      "generation_source": "mixed",
      "required": true
    },
    {
      "name": "deliverables",
      "description": "Array of deliverable items",
      "format": "json",
      "generation_source": "ai",
      "required": true
    },
    {
      "name": "acceptance_criteria",
      "description": "Given-When-Then criteria array",
      "format": "json",
      "generation_source": "ai",
      "required": true
    },
    {
      "name": "dependencies",
      "description": "Prerequisites and blockers",
      "format": "json",
      "generation_source": "template",
      "required": false
    },
    {
      "name": "timeline",
      "description": "Delivery timeline and effort estimate",
      "format": "json",
      "generation_source": "template",
      "required": false
    }
  ],
  "inputs": {
    "sources": [
      {
        "id": "core_metadata_template",
        "source_type": "external_file",
        "source_locator": "../../docs/content-blocks/inbox-coordination/core-metadata.md",
        "required": true
      },
      {
        "id": "deliverables_patterns",
        "source_type": "external_file",
        "source_locator": "../../docs/content-blocks/inbox-coordination/deliverables-structure.md",
        "required": true
      },
      {
        "id": "acceptance_criteria_guide",
        "source_type": "external_file",
        "source_locator": "../../docs/content-blocks/inbox-coordination/acceptance-criteria-gherkin.md",
        "required": true
      },
      {
        "id": "user_context",
        "source_type": "inline_data",
        "data": "{{context}}",
        "required": true
      }
    ]
  },
  "generation": {
    "patterns": [{
      "id": "coordination-request-json",
      "type": "jinja2",
      "template": "{\n  \"type\": \"coordination\",\n  \"request_id\": \"{{request_id}}\",\n  \"title\": \"{{context.request_metadata.title}}\",\n  \"from_repo\": \"{{context.request_metadata.from_repo}}\",\n  \"to_repo\": \"{{context.request_metadata.to_repo}}\",\n  \"priority\": \"{{context.request_metadata.priority}}\",\n  \"urgency\": \"{{context.request_metadata.urgency}}\",\n  \"deliverables\": {{deliverables | tojson}},\n  \"acceptance_criteria\": {{acceptance_criteria | tojson}},\n  \"trace_id\": \"{{trace_id}}\"\n}",
      "variables": [
        {"name": "request_id", "source": "auto_allocated"},
        {"name": "deliverables", "source": "elements.deliverables.example_output"},
        {"name": "acceptance_criteria", "source": "elements.acceptance_criteria.example_output"},
        {"name": "trace_id", "source": "context.trace_id"}
      ]
    }]
  },
  "validation": {
    "schema": "inbox/schemas/coordination-request.schema.json",
    "required_fields": ["type", "request_id", "title", "from_repo", "to_repo", "priority", "urgency", "deliverables", "acceptance_criteria"]
  }
}
```

**Deliverable**: Validated content config JSON file

#### Task 3.2: Create DDD Change Request (3-4 hours)

**Action**:
Write comprehensive change request following chora-base's Diátaxis pattern.

**File**: `inbox/active/chora-compose-inbox-pilot/change-request.md`

**Sections** (Diátaxis Framework):

1. **Frontmatter**:
```yaml
---
title: Inbox Artifact Generation via chora-compose
type: change-request
status: draft
phase: 3-ddd
created: 2025-11-09
request_id: chora-compose-inbox-pilot
trace_id: chora-compose-inbox-integration-2025
---
```

2. **Executive Summary** (1-2 paragraphs)

3. **Explanation** (Why this feature?)
   - Context: Current manual process (30-60 min, error-prone)
   - Problem Statement: High cognitive load, inconsistent quality
   - Business Value: 70-83% time reduction, template reuse, ecosystem benefits
   - Stakeholders: chora-base team, ecosystem repos

4. **How-To Guide** (User workflow)
   - Step 1: User identifies coordination need
   - Step 2: Prepare context (from_repo, deliverables, criteria)
   - Step 3: Generate via MCP tool or CLI
   - Step 4: Review generated JSON
   - Step 5: Validate and commit to inbox/incoming/
   - Expected journey: 5-10 minutes total

5. **Reference** (API design)
   - Content config structure
   - Context schema
   - Post-processing wrapper contract
   - Generation patterns (Jinja2, template_fill, demonstration)
   - Validation requirements (JSON Schema, inbox-status.py)

6. **Functional Requirements**
   - FR-1: Generate valid coordination request JSON
   - FR-2: Validate against JSON Schema
   - FR-3: Allocate sequential request ID
   - FR-4: Emit event to events.jsonl
   - FR-5: Place in inbox/incoming/coordination/
   - FR-6: Support context variations
   - FR-7: Maintain inbox-status.py compatibility
   - FR-8: Generate in <15 minutes
   - FR-9: Achieve ≥80% quality vs hand-written
   - FR-10: Support customization and overrides

7. **Non-Functional Requirements**
   - NFR-1: Performance (generation <15 min)
   - NFR-2: Quality (≥80% rubric score)
   - NFR-3: Maintainability (content blocks easy to update)
   - NFR-4: Scalability (extensible to tasks, proposals)
   - NFR-5: Reliability (100% schema validation)

8. **Acceptance Criteria** (Given-When-Then format)
   - AC-1: Given user context, When generate, Then valid JSON produced
   - AC-2: Given generated JSON, When validate, Then passes JSON Schema
   - AC-3: Given generated artifact, When parse with inbox-status.py, Then displays correctly
   - AC-4: Given 5 test generations, When score quality, Then ≥80% average
   - AC-5: Given manual baseline 45 min, When generate automated, Then <15 min
   - [5 more criteria...]

9. **Architecture Decisions**
   - AD-1: Use chora-compose content configs (not custom generator)
   - AD-2: Template-first with AI augmentation (not pure AI)
   - AD-3: Post-processing wrapper for chora-base specifics
   - AD-4: JSON Schema validation before promotion
   - AD-5: Ephemeral storage for drafts, inbox/ for finals

10. **Risk Assessment**
    - High: Generated quality <80% → Mitigation: Iterate configs, fallback to hybrid
    - Medium: Context incompleteness → Mitigation: Define minimal schema, provide defaults
    - Low: Integration breaks workflows → Mitigation: Parallel operation, extensive testing

11. **Testing Strategy**
    - BDD scenarios (Week 4)
    - 5 test generations (simple, complex, urgent, strategic, edge)
    - Quality rubric scoring (10 criteria)
    - Regression: inbox-status.py, JSON Schema, event emission

12. **Success Criteria**
    - Quality ≥80% (weighted rubric)
    - Time reduction ≥50%
    - Schema validation 100%
    - Parser compatibility 100%

**Deliverable**: DDD change request (600-800 lines, Diátaxis format)

**Approval Required**: Technical lead sign-off before Week 4

#### Task 3.3: Design Post-Processing Wrapper (2-3 hours)

**Action**:
Design validation and promotion wrapper.

**File**: `docs/exploration/wrapper-design-spec.md`

**Wrapper Contract**:

**Input**:
- Generated JSON from chora-compose (ephemeral storage)
- User context (for trace_id, metadata)

**Processing Steps**:
1. **Load Generated Content**
   - Read from ephemeral storage path
   - Parse JSON

2. **JSON Schema Validation**
   - Validate against `inbox/schemas/coordination-request.schema.json`
   - Return errors if validation fails (don't proceed)

3. **Sequential ID Allocation**
   - Scan `inbox/incoming/coordination/` for existing `coord-*.json` files
   - Extract numeric IDs, find max
   - Allocate next ID: `coord-{max+1:03d}` (e.g., coord-042)

4. **Event Emission**
   - Append to `inbox/coordination/events.jsonl`:
   ```json
   {
     "event_type": "coordination_request_created",
     "trace_id": "<from context>",
     "timestamp": "<ISO 8601>",
     "request_id": "coord-042",
     "generation_method": "chora-compose",
     "config_id": "coordination-request",
     "from_repo": "<from JSON>",
     "to_repo": "<from JSON>"
   }
   ```

5. **File Promotion**
   - Copy to `inbox/incoming/coordination/coord-042.json`
   - Set file permissions (644)

6. **Validation Checks**
   - Run `inbox-status.py --trace-id <trace_id>` to verify parsing
   - Return success/failure status

**Output**:
```json
{
  "success": true,
  "artifact_id": "coord-042",
  "artifact_path": "inbox/incoming/coordination/coord-042.json",
  "trace_id": "chora-compose-inbox-integration-2025",
  "validation": {
    "schema": "pass",
    "inbox_status": "pass"
  },
  "generation_time_seconds": 420
}
```

**Error Handling**:
- Schema validation fails → Return errors, don't promote
- ID allocation fails → Use fallback (timestamp-based), log warning
- Event emission fails → Log error, still promote (events are audit, not critical)
- inbox-status.py fails → Log error, still promote (but flag for review)

**Deliverable**: Wrapper design specification (implementation in Week 4)

#### Task 3.4: Review and Iterate (1-2 hours)

**Action**:
- Share content config with chora-compose team
- Request feedback on InputSource usage, GenerationPattern structure
- Incorporate chora-compose best practices
- Refine based on feedback

**Deliverable**: Updated content config + review notes

### Week 3 Exit Criteria

- [ ] ✅ Content config created and chora-compose-compatible
- [ ] ✅ DDD change request complete (600-800 lines, Diátaxis format)
- [ ] ✅ Technical lead approval obtained on change request
- [ ] ✅ Post-processing wrapper designed with clear contract
- [ ] ✅ chora-compose team review complete, feedback incorporated

**Decision Checkpoint**: If content config doesn't work with chora-compose patterns, iterate 1-2 rounds (2-4 hours). If fundamental incompatibility, escalate for decision.

---

## Week 4: Generation & Validation (BDD + TDD Phase) (10-16 hours)

### Objective
Generate test coordination requests, validate quality against rubric, make go/no-go decision.

### Tasks

#### Task 4.1: Create BDD Scenarios (2-3 hours)

**Action**:
Write Gherkin scenarios and step definitions.

**File**: `features/inbox-integration.feature`

**Scenarios** (5-7):

```gherkin
Feature: Inbox Artifact Generation with chora-compose

  Scenario: Generate valid coordination request from context
    Given a coordination request context with from_repo "ecosystem-manifest"
    And to_repo "chora-base"
    And priority "P0"
    And 3 deliverables
    When I generate coordination request using chora-compose
    Then a JSON file is created
    And the JSON validates against coordination-request.schema.json
    And all 18 required fields are present

  Scenario: Generated artifact parses with inbox-status.py
    Given a generated coordination request "coord-test-001.json"
    When I run inbox-status.py with trace_id filter
    Then the request appears in the output
    And priority is displayed correctly
    And from_repo and to_repo are shown

  Scenario: Sequential ID allocation
    Given existing coordination requests coord-040, coord-041
    When I generate a new coordination request
    Then the request_id is "coord-042"
    And the file is placed at inbox/incoming/coordination/coord-042.json

  Scenario: Event emission with trace_id
    Given a coordination request context with trace_id "test-trace-123"
    When I generate coordination request
    Then an event is appended to events.jsonl
    And the event has event_type "coordination_request_created"
    And the event has trace_id "test-trace-123"

  Scenario: Deliverables completeness
    Given a coordination request context with 5 deliverables
    When I generate coordination request
    Then the generated JSON has exactly 5 deliverables
    And each deliverable is a non-empty string

  Scenario: Acceptance criteria in Given-When-Then format
    Given a coordination request context with 3 acceptance criteria
    When I generate coordination request
    Then the generated JSON has exactly 3 acceptance criteria
    And each criterion contains "Given", "When", or "Then"

  Scenario: Quality score meets threshold
    Given 5 generated coordination request samples
    When I score each against the 10-criterion rubric
    Then the average score is >= 80%
    And no sample scores below 70%
```

**File**: `features/steps/inbox_integration_steps.py`

```python
from behave import given, when, then
import json
from pathlib import Path
import subprocess

@given('a coordination request context with from_repo "{from_repo}"')
def step_impl(context, from_repo):
    if not hasattr(context, 'request_context'):
        context.request_context = {}
    context.request_context['from_repo'] = from_repo

@when('I generate coordination request using chora-compose')
def step_impl(context):
    # Call wrapper script
    result = subprocess.run([
        'python', 'scripts/generate-coordination-request.py',
        '--context', json.dumps(context.request_context),
        '--trace-id', 'test-trace-123'
    ], capture_output=True, text=True)
    context.generation_result = json.loads(result.stdout)

@then('a JSON file is created')
def step_impl(context):
    path = Path(context.generation_result['artifact_path'])
    assert path.exists(), f"Artifact not found at {path}"

# [More step definitions...]
```

**Action**: Verify RED state (all scenarios fail before implementation)

**Deliverable**: BDD scenarios + step definitions (RED state confirmed)

#### Task 4.2: Generate 5 Test Coordination Requests (3-5 hours)

**Action**:
Generate test cases using chora-compose + wrapper.

**Test Cases**:

1. **Simple Coordination Request** (`coord-test-001.json`)
   - Context: `context-examples/coordination/simple-request-context.json`
   - Minimal deliverables (2-3 items)
   - No dependencies
   - Standard priority (P1)

2. **Complex Coordination Request** (`coord-test-002.json`)
   - Context: `context-examples/coordination/complex-request-context.json`
   - 10+ deliverables
   - Multi-repo coordination (from_repo: ecosystem-manifest)
   - Multiple dependencies
   - Strategic waypoint (W3, Q4-2025)

3. **Urgent P0 Request** (`coord-test-003.json`)
   - Context: `context-examples/coordination/urgent-request-context.json`
   - Priority: P0, Urgency: blocks_sprint
   - Short timeline (this sprint)
   - Minimal context (fast creation scenario)

4. **Strategic Collaboration** (`coord-test-004.json`)
   - Long-term collaboration request
   - Exploratory collaboration mode
   - Architecture questions (like COORD-2025-002)
   - Multiple related SAPs

5. **Edge Case** (`coord-test-005.json`)
   - Optional fields populated
   - Custom context fields
   - Unusual structure (testing flexibility)

**Capture for Each**:
- Generation start/end timestamps
- Iteration count (how many refinements needed)
- User interventions (manual edits)
- chora-compose logs (warnings, errors)

**Deliverable**:
- 5 generated JSON files in `inbox/active/chora-compose-inbox-pilot/generated-samples/`
- Generation log in `docs/exploration/pilot-generation-log.md`

#### Task 4.3: Implement Post-Processing Wrapper (2-3 hours)

**Action**:
Implement wrapper script from Week 3 design.

**File**: `scripts/generate-coordination-request.py`

```python
#!/usr/bin/env python3
"""
Wrapper for chora-compose coordination request generation

Handles:
- chora-compose content generation
- JSON Schema validation
- Sequential ID allocation
- Event emission
- File promotion to inbox/incoming/
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import validate, ValidationError
import re
import shutil

def allocate_next_id(inbox_dir: Path = Path("inbox")) -> str:
    """Allocate sequential coordination request ID"""
    incoming = inbox_dir / "incoming" / "coordination"
    if not incoming.exists():
        return "coord-001"

    existing = list(incoming.glob("coord-*.json"))
    if not existing:
        return "coord-001"

    max_id = max(
        int(re.search(r'coord-(\d+)', f.stem).group(1))
        for f in existing
    )

    return f"coord-{max_id + 1:03d}"

def validate_schema(artifact: dict, schema_path: Path) -> dict:
    """Validate against JSON Schema"""
    with open(schema_path) as f:
        schema = json.load(f)

    try:
        validate(instance=artifact, schema=schema)
        return {"valid": True, "errors": []}
    except ValidationError as e:
        return {"valid": False, "errors": [str(e)]}

def emit_event(event_type: str, trace_id: str, event_data: dict,
               events_file: Path = Path("inbox/coordination/events.jsonl")):
    """Append event to JSONL log"""
    event = {
        "event_type": event_type,
        "trace_id": trace_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event_data
    }

    with open(events_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

def generate_coordination_request(context: dict, trace_id: str, force: bool = False):
    """
    Main wrapper function

    Steps:
    1. Call chora-compose (TODO: integrate with chora-compose MCP)
    2. Validate JSON Schema
    3. Allocate sequential ID
    4. Emit event
    5. Promote to inbox/incoming/
    """
    start_time = datetime.now(timezone.utc)

    # Step 1: Generate (for now, simulate with template)
    # TODO: Replace with actual chora-compose call
    generated = simulate_generation(context)

    # Step 2: Validate
    schema_path = Path("inbox/schemas/coordination-request.schema.json")
    validation = validate_schema(generated, schema_path)

    if not validation["valid"]:
        print(json.dumps({
            "success": False,
            "error": "validation_failed",
            "details": validation["errors"]
        }))
        sys.exit(1)

    # Step 3: Allocate ID
    request_id = allocate_next_id()
    generated["request_id"] = request_id

    # Step 4: Emit event
    emit_event(
        event_type="coordination_request_created",
        trace_id=trace_id,
        event_data={
            "request_id": request_id,
            "generation_method": "chora-compose",
            "from_repo": generated["from_repo"],
            "to_repo": generated["to_repo"]
        }
    )

    # Step 5: Promote
    dest_path = Path(f"inbox/incoming/coordination/{request_id}.json")
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, 'w') as f:
        json.dump(generated, f, indent=2)

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    # Output result
    result = {
        "success": True,
        "artifact_id": request_id,
        "artifact_path": str(dest_path),
        "trace_id": trace_id,
        "validation": {
            "schema": "pass",
            "inbox_status": "pass"  # TODO: Test with inbox-status.py
        },
        "generation_time_seconds": duration
    }

    print(json.dumps(result, indent=2))

def simulate_generation(context: dict) -> dict:
    """Temporary simulation (replace with chora-compose integration)"""
    return {
        "type": "coordination",
        "request_id": "PLACEHOLDER",  # Will be allocated
        "title": context["request_metadata"]["title"],
        "from_repo": context["request_metadata"]["from_repo"],
        "to_repo": context["request_metadata"]["to_repo"],
        "priority": context["request_metadata"]["priority"],
        "urgency": context["request_metadata"]["urgency"],
        "created": datetime.now(timezone.utc).date().isoformat(),
        "deliverables": context["deliverables"],
        "acceptance_criteria": context["acceptance_criteria"],
        "context": context.get("coordination_context", {}),
        "trace_id": context.get("trace_id", "")
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", type=json.loads, required=True)
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args()
    generate_coordination_request(args.context, args.trace_id, args.force)
```

**Test**:
- Run with all 5 context files
- Verify BDD scenarios turn GREEN
- Verify files created in inbox/incoming/coordination/

**Deliverable**: Working wrapper script (250-400 lines) + GREEN BDD scenarios

#### Task 4.4: Quality Assessment (3-5 hours)

**Action**:
Score each generated request against 10-criterion rubric.

**File**: `docs/exploration/pilot-quality-assessment.md`

**Rubric** (10 Criteria):

| Criterion | Weight | Scoring Guide (0-10) |
|-----------|--------|---------------------|
| **Structure Match** | 10% | 10 = Perfect structure match, 0 = Major deviations |
| **Technical Accuracy** | 20% | 10 = 100% accurate, 5 = Minor errors, 0 = Hallucinations |
| **Coherence** | 15% | 10 = Seamless prose, 5 = Awkward transitions, 0 = Disjointed |
| **Completeness** | 15% | 10 = All fields complete, 5 = Some generic, 0 = Missing |
| **JSON Schema** | 10% | 10 = 100% pass, 0 = Any error |
| **inbox-status** | 10% | 10 = Perfect parsing, 0 = Parse error |
| **Time Reduction** | 5% | 10 = ≥70%, 5 = 50%, 0 = No reduction |
| **Maintainability** | 5% | 10 = Trivial to update blocks, 5 = Moderate, 0 = Complex |
| **Flexibility** | 5% | 10 = Fully customizable, 5 = Partial, 0 = Rigid |
| **Scalability** | 5% | 10 = Obvious extension, 5 = Requires thought, 0 = Unclear |

**For Each Test Case**:
1. Score each criterion (0-10)
2. Multiply by weight
3. Sum weighted scores = overall % (0-100%)

**Comparison**:
- Compare generated vs hand-written (COORD-2025-002, COORD-2025-004)
- Document specific examples of strengths and weaknesses
- Identify patterns in what works vs what doesn't

**Aggregate Metrics**:
- Average quality score across 5 tests
- Min/max scores
- JSON Schema pass rate (should be 100%)
- inbox-status.py pass rate (should be 100%)
- Average time reduction

**Deliverable**: Quality assessment report (800-1200 lines)

#### Task 4.5: Collect Metrics (1-2 hours)

**Action**:
Compile structured metrics data.

**File**: `docs/exploration/pilot-metrics-summary.json`

```json
{
  "pilot_id": "chora-compose-inbox-integration-2025",
  "artifact_type": "coordination_request",
  "test_cases": 5,
  "quality_scores": {
    "average": 86.0,
    "min": 78.0,
    "max": 92.0,
    "by_test_case": [86, 78, 92, 85, 89],
    "by_criterion": {
      "structure_match": 9.2,
      "technical_accuracy": 8.4,
      "coherence": 7.8,
      "completeness": 8.8,
      "json_schema": 10.0,
      "inbox_status": 10.0,
      "time_reduction": 9.0,
      "maintainability": 8.2,
      "flexibility": 8.0,
      "scalability": 8.8
    }
  },
  "time_metrics": {
    "manual_baseline_minutes": 45,
    "automated_average_minutes": 12,
    "reduction_percent": 73.3,
    "by_test_case": [8, 15, 7, 14, 12]
  },
  "validation": {
    "json_schema_pass_rate": 1.0,
    "inbox_status_pass_rate": 1.0
  },
  "iterations": {
    "average_per_request": 2.4,
    "range": [1, 4]
  },
  "decision": "GO",
  "rationale": "Quality score 86% exceeds 80% threshold. Time reduction 73% exceeds 50% target. All validation checks passing."
}
```

**Deliverable**: Structured metrics JSON

#### Task 4.6: Make Go/No-Go Decision (1-2 hours)

**Action**:
Create decision document with data-driven recommendation.

**File**: `docs/exploration/pilot-decision.md`

**Decision Framework**:

**GO** (Quality ≥80%, Time Reduction ≥50%):
- Proceed to full implementation (Weeks 5-12)
- Expand to implementation tasks (2-3 weeks)
- Expand to strategic proposals (2-3 weeks)
- Ecosystem adoption (2-4 weeks)

**PARTIAL** (Quality 70-79%):
- Hybrid approach:
  - Use automation for simple fields (metadata, structure)
  - Manual for complex fields (context, deliverables)
- Re-evaluate in 1-2 sprints

**NO-GO** (Quality <70%):
- Fall back to Option C (manual process)
- Document learnings for future
- Revisit in Q2 2026

**Deliverable**: Decision document (400-600 lines) with:
- Quality scores summary
- Time metrics summary
- Strengths and weaknesses
- Recommendation (GO/PARTIAL/NO-GO)
- Rationale with data references
- Next steps

### Week 4 Exit Criteria

- [ ] ✅ 5 test coordination requests generated
- [ ] ✅ All BDD scenarios GREEN (100% pass rate)
- [ ] ✅ Quality score ≥80% (average across 5 tests)
- [ ] ✅ JSON Schema validation: 100% pass rate
- [ ] ✅ inbox-status.py compatibility: 100% parse success
- [ ] ✅ Time reduction ≥50% (manual 30-60 min → automated ≤15 min)
- [ ] ✅ Decision document complete with recommendation
- [ ] ✅ Metrics data collected and structured

**Decision Point**: Based on metrics, make GO/PARTIAL/NO-GO decision for full implementation.

---

## Success Criteria (Detailed)

### Quantitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Quality Score** | ≥80% | 10-criterion weighted rubric |
| **Time Reduction** | ≥50% | Manual baseline (45 min) vs automated actual |
| **Schema Validation** | 100% | JSON Schema validator (pass/fail) |
| **Parser Compatibility** | 100% | inbox-status.py parse success rate |
| **Iteration Count** | ≤3 | Average refinements per request |

### Qualitative Observations

**What Works Well**:
- Coherence and readability
- Specific sections or fields that shine
- Patterns that transfer well from content blocks

**What Needs Improvement**:
- Awkward transitions or generic content
- Missing nuance or context
- Edge cases not handled well

**Edge Cases**:
- Custom fields or unusual structures
- How does system handle them?
- Gaps identified for future improvement

### Comparison Baseline

**Hand-Written Examples**:
- COORD-2025-002 (exploratory, high quality)
- COORD-2025-004 (prescriptive, complex)
- coord-005 (SAP peer review)

**Generated Must Match**:
- Structure and format
- Level of detail
- Clarity and coherence
- Actionability (deliverables, criteria)

---

## Data Collection Strategy

### During Generation (Week 4, Task 4.2)

**Capture**:
- Timestamp: Start and end of each generation
- Logs: chora-compose output, warnings, errors
- Interventions: Manual edits, context adjustments
- Iterations: Number of refinements needed
- Artifacts: Save intermediate drafts (before/after edits)

**File**: `docs/exploration/pilot-generation-log.md`

**Format**:
```markdown
## Test Case 1: Simple Coordination Request

**Context**: simple-request-context.json
**Start Time**: 2025-11-23T10:30:00Z
**End Time**: 2025-11-23T10:38:15Z
**Duration**: 8.25 minutes

**Iterations**:
1. Initial generation (10:30-10:32): Draft had generic deliverables
2. Refined context (10:33-10:36): Added deliverable patterns
3. Final generation (10:36-10:38): Quality acceptable

**Interventions**:
- Manually refined deliverable #2 (too vague)
- No other manual edits

**chora-compose Logs**:
- No warnings
- Generated using Jinja2 template + AI deliverables

**Result**: coord-test-001.json (200 lines)
```

### During Validation (Week 4, Task 4.4)

**Capture**:
- Rubric scores (10 criteria × 5 test cases = 50 scores)
- Side-by-side comparisons (generated vs hand-written)
- Specific examples of strengths and weaknesses
- Validation results (schema, parser)

**File**: `docs/exploration/pilot-quality-assessment.md`

### Post-Pilot (Week 4, Task 4.5)

**Aggregate**:
- Average quality score, min/max, distribution
- Average time reduction, variance
- Patterns in what works vs what doesn't
- Extrapolation to full implementation

**File**: `docs/exploration/pilot-metrics-summary.json`

---

## Risk Assessment and Mitigation

### High Risks

**Risk 1: Generated Quality <80%**
- **Likelihood**: Medium
- **Impact**: High (blocks full adoption)
- **Mitigation**:
  - Start with template_fill (deterministic baseline)
  - Iterate content configs based on feedback
  - Hybrid approach (automated + manual refinement)
- **Fallback**: PARTIAL decision (use for simple fields only)

### Medium Risks

**Risk 2: Context Incompleteness**
- **Likelihood**: Medium-High
- **Impact**: Medium (lower quality but usable)
- **Mitigation**:
  - Define minimal required context
  - Provide defaults for optional fields
  - User can override/supplement manually
- **Fallback**: Request more context from user, iterate

**Risk 3: Integration Breaks Existing Workflows**
- **Likelihood**: Low
- **Impact**: High (disrupts operations)
- **Mitigation**:
  - Extensive testing with inbox-status.py
  - Parallel operation (manual + automated)
  - Validation against existing examples
- **Fallback**: Roll back, continue manual process

**Risk 4: Timeline Slips (Async Coordination)**
- **Likelihood**: Medium
- **Impact**: Medium (delays decision)
- **Mitigation**:
  - 4-week timeline includes buffer
  - Clear milestones and checkpoints
  - Proactive communication with chora-compose
- **Fallback**: Extend to 5 weeks if needed

### Low Risks

**Risk 5: chora-compose Lacks Features**
- **Likelihood**: Low (COORD-2025-002 confirmed features)
- **Impact**: Medium (delays, workarounds needed)
- **Mitigation**:
  - Gaps already identified (8-13 hours)
  - chora-compose team responsive
  - Wrapper can handle chora-base specifics
- **Fallback**: Implement workarounds in wrapper

---

## Collaboration and Communication

### With chora-compose Team

**Touchpoints**:
- Week 2: Share decomposition approach, get feedback (async)
- Week 3: Share content config, review patterns (async, 24-48h turnaround)
- Week 4: Share generation results, discuss learnings (async)

**Communication**:
- Via COORD-2025-002 (exploratory coordination request)
- Async iteration (24-48 hour response time expected)
- Document decisions and rationale

**Expectations**:
- chora-compose provides guidance on best practices
- chora-base iterates based on feedback
- Collaborative refinement of content configs

### Within chora-base Team

**Touchpoints**:
- Week 2 end: Review content blocks, get technical lead approval
- Week 3 end: Review DDD change request, get approval
- Week 4 end: Review pilot results, make go/no-go decision

**Communication**:
- Regular updates in team channels
- Documentation-first approach (write, then discuss)
- Data-driven decision making

---

## Deliverables Summary

### Week 2 Deliverables (8 files)

| File Path | Type | Purpose |
|-----------|------|---------|
| `docs/exploration/coordination-request-analysis.md` | Analysis | Pattern extraction from examples |
| `docs/exploration/decomposition-rationale.md` | Documentation | Design decisions rationale |
| `docs/content-blocks/inbox-coordination/*.md` | Content Blocks | 10-15 reusable markdown files |
| `docs/content-blocks/shared/*.md` | Content Blocks | 2-3 universal blocks |
| `context-examples/coordination/simple-request-context.json` | Test Data | Simple test case |
| `context-examples/coordination/complex-request-context.json` | Test Data | Complex test case |
| `context-examples/coordination/urgent-request-context.json` | Test Data | Urgent test case |

### Week 3 Deliverables (3 files)

| File Path | Type | Purpose |
|-----------|------|---------|
| `configs/content/coordination-request/coordination-request-content.json` | Config | chora-compose content config |
| `inbox/active/chora-compose-inbox-pilot/change-request.md` | DDD Doc | Requirements specification |
| `docs/exploration/wrapper-design-spec.md` | Design | Post-processing wrapper spec |

### Week 4 Deliverables (13 files)

| File Path | Type | Purpose |
|-----------|------|---------|
| `features/inbox-integration.feature` | BDD | Gherkin scenarios |
| `features/steps/inbox_integration_steps.py` | BDD | Step definitions |
| `scripts/generate-coordination-request.py` | Implementation | Validation wrapper |
| `inbox/active/chora-compose-inbox-pilot/generated-samples/coord-test-*.json` | Samples | 5 generated test cases |
| `docs/exploration/pilot-generation-log.md` | Log | Generation session log |
| `docs/exploration/pilot-quality-assessment.md` | Report | Rubric scores + analysis |
| `docs/exploration/pilot-metrics-summary.json` | Data | Structured metrics |
| `docs/exploration/pilot-decision.md` | Decision | Go/no-go recommendation |

**Total**: ~24 core files + 10-15 content blocks = 34-39 files

---

## Related Coordination

**Dependencies**:
- COORD-2025-002: Exploratory request to chora-compose (active)
- SAP-004 Pilot: chora-compose SAP generation (approved, ~Nov 6 start)

**Enables**:
- Full inbox artifact automation (if GO)
- Ecosystem adoption (chora-workspace, ecosystem-manifest)
- Template library expansion (tasks, proposals)

**Trace ID**: `chora-compose-inbox-integration-2025`

**Events**:
- exploration_started (2025-11-02)
- exploration_phase_completed (2025-11-02)
- pilot_planning_started (2025-11-02)
- [Future] pilot_week_2_started
- [Future] pilot_week_3_started
- [Future] pilot_week_4_started
- [Future] pilot_decision_made

---

## Appendix A: Example Content Block

**File**: `docs/content-blocks/inbox-coordination/core-metadata.md`

```markdown
# Core Metadata - Coordination Request

## Description
Standard metadata fields required for all coordination requests per SAP-001.

## Fields
- `type`: Always "coordination" (string, required)
- `request_id`: Format "COORD-YYYY-NNN" or "coord-NNN" (string, required, auto-allocated)
- `title`: One-sentence description of coordination need (string <80 chars, required)
- `created`: Creation date (YYYY-MM-DD format, required, defaults to current)
- `from_repo`: Source repository name (string, required)
- `to_repo`: Target repository name (string, required)
- `priority`: Priority level (enum: P0 | P1 | P2 | P3, required)
- `urgency`: Urgency level (enum: blocks_sprint | next_sprint | backlog, required)

## Template
```json
{
  "type": "coordination",
  "request_id": "{{request_id}}",
  "title": "{{title}}",
  "created": "{{created_date}}",
  "from_repo": "{{from_repo}}",
  "to_repo": "{{to_repo}}",
  "priority": "{{priority}}",
  "urgency": "{{urgency}}"
}
```

## Variation Points
- `title`: Customized per request (user provides)
- `from_repo`, `to_repo`: From user context
- `priority`: P0-P3 based on impact/urgency assessment
- `urgency`: Based on timeline constraints
- `request_id`: Auto-generated by wrapper (sequential allocation)
- `created`: Defaults to current date (can override)

## Usage Guidance
- Always use this template for core metadata section
- `request_id` is auto-allocated by wrapper (scan existing, increment max)
- `title` should be concise but descriptive (<80 chars)
- `priority` and `urgency` should align (P0 usually blocks_sprint)
- `from_repo` and `to_repo` must match actual repository names

## Validation
- All fields required except where noted
- JSON Schema: `inbox/schemas/coordination-request.schema.json`
- Field constraints:
  - `priority`: Must be one of P0, P1, P2, P3
  - `urgency`: Must be one of blocks_sprint, next_sprint, backlog
  - `title`: Must be <80 characters
  - `created`: Must be valid YYYY-MM-DD date
```

---

## Appendix B: Example Context File

**File**: `context-examples/coordination/simple-request-context.json`

```json
{
  "request_metadata": {
    "from_repo": "ecosystem-manifest",
    "to_repo": "chora-base",
    "priority": "P1",
    "urgency": "next_sprint",
    "title": "Health endpoint template for MCP servers",
    "created": "2025-11-09"
  },
  "coordination_context": {
    "waypoint": "W3",
    "related_saps": ["SAP-014", "SAP-017"],
    "background": "Ecosystem-wide health monitoring initiative requires standardized health endpoint template for all MCP servers.",
    "collaboration_mode": "prescriptive"
  },
  "deliverables": [
    "FastMCP health endpoint template with /health route",
    "Documentation in SAP-014 (Explanation + How-To + Reference)",
    "Example implementation in chora-base/examples/"
  ],
  "acceptance_criteria": [
    "Given the template, When integrated into MCP server, Then /health endpoint returns valid JSON response",
    "Given the documentation, When engineer reads SAP-014, Then can implement health endpoint in <30 minutes",
    "Given the example, When tests run, Then all health checks pass with ≥90% coverage"
  ],
  "timeline": {
    "requested_delivery": "Week 10",
    "estimated_effort": "6-8 hours"
  },
  "dependencies": {
    "prerequisites": ["ADR-001 (health check format)"],
    "blocks": ["coord-002 (ecosystem-manifest health spec)"]
  },
  "trace_id": "ecosystem-w3-health-monitoring"
}
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Status**: Approved - Ready for Week 2 Execution
**Next Review**: 2025-11-15 (Week 2 completion)
