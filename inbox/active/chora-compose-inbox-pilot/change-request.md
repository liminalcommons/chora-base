# Change Request: chora-compose Integration for Inbox Artifact Generation

**Type**: Feature Addition (Pilot)
**Request ID**: PILOT-2025-001
**Trace ID**: `chora-compose-inbox-integration-2025`
**Status**: Week 3 - Design (DDD)
**Created**: 2025-11-02
**Target**: SAP-001 Inbox Coordination Protocol v1.1.0

---

## Executive Summary

This change request proposes integrating chora-compose as the content generation infrastructure for SAP-001 (Inbox Coordination Protocol) to automate creation of coordination request artifacts. Currently, creating coordination requests is a manual process taking 30-60 minutes per artifact. This pilot will validate whether chora-compose can reduce this to 5-10 minutes (83% time reduction) while maintaining ≥80% quality threshold.

**Scope**: Coordination requests only (1 of 3 inbox artifact types)
**Approach**: Direct integration (Option A from exploration)
**Timeline**: 4-week pilot (Nov 9 - Dec 6, 2025)
**Decision Point**: Week 4 - GO/PARTIAL/NO-GO on full implementation

---

## Table of Contents

1. [Explanation](#explanation) - What and why
2. [How-To Guide](#how-to-guide) - Step-by-step implementation
3. [Reference](#reference) - Technical specifications
4. [Appendices](#appendices) - Supporting materials

---

## Explanation

### What Is This Change?

This pilot introduces **template-driven artifact generation** for SAP-001 coordination requests using chora-compose's content generation framework. Instead of manually hand-crafting JSON files with 15-20 required fields, developers will provide high-level context that is transformed into valid coordination request artifacts through content configs and content blocks.

#### Current State (Manual)

```bash
# Developer manually creates JSON file
vim inbox/incoming/coordination/COORD-2025-NNN.json

# Developer hand-crafts 18 required fields
{
  "type": "coordination",
  "request_id": "COORD-2025-NNN",  # Manual ID allocation
  "title": "...",                   # Manual writing
  "from_repo": "...",
  "to_repo": "...",
  "priority": "P1",                 # Manual assessment
  "urgency": "next_sprint",
  "deliverables": [...],            # Manual brainstorming
  "acceptance_criteria": [...],     # Manual derivation
  "created": "2025-11-02",
  "context": {
    "background": "...",            # Manual narrative writing
    "rationale": "..."
  },
  # ... 8 more fields
}

# Developer validates manually
python scripts/inbox-status.py --validate COORD-2025-NNN.json

# Developer emits event manually
# ... append to events.jsonl

# Time: 30-60 minutes
# Error rate: Medium (schema violations, inconsistent formatting)
```

#### Future State (Automated with chora-compose)

```bash
# Developer provides high-level context
cat > context.json <<EOF
{
  "request_type": "exploratory",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-compose",
  "purpose": "Explore chora-compose integration for inbox automation",
  "deliverables": [
    "Feasibility assessment",
    "Integration options comparison",
    "Recommendation on pilot"
  ],
  "priority": "P2",
  "urgency": "backlog"
}
EOF

# chora-compose generates coordination request
chora-compose generate coordination-request --context context.json --output draft/

# Post-processing wrapper validates, allocates ID, emits events
python scripts/process-generated-artifact.py draft/coordination-request.json

# Time: 5-10 minutes
# Error rate: Low (template-driven, automated validation)
```

### Why This Change?

#### Problem Statement

**Manual artifact creation is time-intensive and error-prone**:

- **Time Cost**: 30-60 minutes per coordination request (current average)
  - 10-15 min: Brainstorming deliverables and acceptance criteria
  - 10-15 min: Writing context narrative (background, rationale)
  - 5-10 min: Formatting JSON correctly
  - 5-10 min: Validation and event emission
  - 2-5 min: ID allocation and file organization

- **Quality Issues**:
  - Schema violations (typos in enum values, missing required fields)
  - Inconsistent formatting (different tone, structure across requests)
  - Incomplete acceptance criteria (vague, non-measurable)
  - Missing event emission (forget to update events.jsonl)

- **Maintenance Burden**:
  - No reusable patterns (each request written from scratch)
  - Difficult to update conventions (must edit all existing requests)
  - New contributors face steep learning curve (18 required fields, subtle patterns)

#### Opportunity

**chora-compose is exceptionally well-aligned** for inbox automation:

- **Content Generation Framework**: 17 production generators demonstrate maturity with structured content
- **MCP Integration**: Enables agent-assisted workflows (our strategic direction)
- **Template + AI Hybrid**: Deterministic baseline with AI augmentation for flexibility
- **Ecosystem Synergy**: Content blocks shareable across chora ecosystem repos

**Exploration findings** (COORD-2025-002):
- Technical feasibility: **90%** (exceptional alignment)
- Quality potential: **75-85%** (template-based + AI augmentation)
- Maintenance reduction: **80%** (content blocks vs manual)

#### Strategic Value

**Beyond immediate time savings**:

1. **Ecosystem Multiplier**: Content block library usable by chora-workspace, ecosystem-manifest
2. **Extensibility**: Same infrastructure extends to tasks (12-15 blocks) and proposals (10-12 blocks)
3. **Quality Consistency**: Template-driven ensures schema compliance and pattern adherence
4. **Contributor Onboarding**: Simpler context input vs manual JSON crafting

### How Does It Work?

#### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Context Input                        │
│  (JSON: request_type, purpose, deliverables, priority, etc.)   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      chora-compose Engine                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Content Configs (15-20 JSON files)                       │  │
│  │  - core-metadata.json                                    │  │
│  │  - repository-fields.json                                │  │
│  │  - deliverables-structure.json                           │  │
│  │  - acceptance-criteria-patterns.json                     │  │
│  │  - context-background.json                               │  │
│  │  - ... (10 more)                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                        │                                         │
│                        ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Content Blocks (15 markdown files)                       │  │
│  │  Template patterns + variation points + examples         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                        │                                         │
│                        ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Artifact Assembly Config                                 │  │
│  │  Combines content elements into coordination request     │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              Draft Coordination Request (JSON)                   │
│  Valid structure, AI-augmented content, pending validation      │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│               Post-Processing Wrapper (Python)                   │
│  1. JSON schema validation                                      │
│  2. ID allocation (next sequence number)                        │
│  3. Event emission (events.jsonl)                               │
│  4. File promotion (draft → incoming)                           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│      Final Coordination Request in inbox/incoming/              │
│      Valid SAP-001 artifact ready for triage                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Key Components

1. **Content Blocks** (15 markdown files in `docs/content-blocks/inbox-coordination/`)
   - Atomic, reusable patterns for each field or field group
   - Template patterns with variation points
   - Real examples from analyzed requests
   - Generation guidance (template vs AI)

2. **Content Configs** (15-20 JSON files in `configs/content/coordination-request/`)
   - Map content blocks to chora-compose ContentElements
   - Define generation sources (user input, system function, AI)
   - Specify input sources and placeholders

3. **Artifact Assembly Config** (`configs/artifact/coordination-request.json`)
   - Combines ContentElements into full coordination request
   - Defines ordering and dependencies
   - Specifies output format (JSON)

4. **Post-Processing Wrapper** (`scripts/process-generated-artifact.py`)
   - Validates against SAP-001 schema
   - Allocates request_id from sequence
   - Emits events to events.jsonl
   - Promotes draft to inbox/incoming/

#### Generation Flow

**Step 1**: User provides context
```json
{
  "request_type": "exploratory",
  "purpose": "Explore chora-compose integration",
  "deliverables": ["Feasibility assessment", "Options comparison"],
  "priority": "P2"
}
```

**Step 2**: chora-compose processes via content configs
- `core-metadata.json` → generates type, title, created
- `deliverables-structure.json` → formats deliverables array
- `acceptance-criteria-patterns.json` → derives criteria from deliverables
- `context-background.json` → expands purpose into narrative
- ... (12 more configs)

**Step 3**: Draft artifact assembled
```json
{
  "type": "coordination",
  "request_id": "PENDING",  # Post-processing will allocate
  "title": "Exploring chora-compose Integration for Inbox Automation",
  "deliverables": ["Feasibility assessment", "Options comparison"],
  "acceptance_criteria": [
    "Feasibility assessment addresses technical compatibility...",
    "Options comparison includes ≥2 approaches..."
  ],
  "context": {
    "background": "chora-base maintains SAP-001... [AI-generated narrative]"
  }
  # ... 15 more fields
}
```

**Step 4**: Post-processing validates and finalizes
```bash
python scripts/process-generated-artifact.py draft/coordination-request.json
# → Validates schema
# → Allocates ID: COORD-2025-007
# → Emits event to events.jsonl
# → Moves to inbox/incoming/coordination/COORD-2025-007.json
```

---

## How-To Guide

### Prerequisites

Before implementing this pilot:

1. **chora-compose installed** (v0.5.0+)
   ```bash
   # Installation instructions depend on chora-compose setup
   # Assuming pip/npm package or git clone
   ```

2. **Content blocks created** (Week 2 complete)
   - 15 markdown files in `docs/content-blocks/inbox-coordination/`

3. **Context schema defined**
   - `context-examples/coordination/context-schema.json`

4. **Example contexts available**
   - 3 test cases for validation

### Step 1: Create Content Configs (15-20 files)

For each content block, create corresponding chora-compose content config.

**Example: core-metadata.json**

```json
{
  "$schema": "https://chora-compose.dev/schemas/content-config.json",
  "name": "core-metadata",
  "version": "1.0.0",
  "description": "Fundamental identifying fields for coordination requests (type, request_id, title, created)",

  "content_element": {
    "name": "core-metadata",
    "format": "json",
    "example_output": {
      "type": "coordination",
      "request_id": "COORD-2025-NNN",
      "title": "Example Coordination Request Title",
      "created": "2025-11-02"
    }
  },

  "generation": {
    "pattern": "template_fill",
    "template_source": {
      "type": "file",
      "path": "docs/content-blocks/inbox-coordination/core-metadata.md",
      "section": "Template / Example"
    },
    "placeholders": {
      "type": {
        "source": "literal",
        "value": "coordination"
      },
      "request_id": {
        "source": "post_processing",
        "note": "Allocated during post-processing from sequence file"
      },
      "title": {
        "source": "ai_generation",
        "input": "context.purpose",
        "guidance": "Generate 50-80 character title from purpose. Use title case. Avoid 'Request to' prefix."
      },
      "created": {
        "source": "system_function",
        "function": "current_date",
        "format": "YYYY-MM-DD"
      }
    }
  },

  "validation": {
    "required_fields": ["type", "request_id", "title", "created"],
    "field_constraints": {
      "type": {"enum": ["coordination"]},
      "request_id": {"pattern": "^(coord-\\d{3}|COORD-\\d{4}-\\d{3})$"},
      "title": {"minLength": 10, "maxLength": 120},
      "created": {"pattern": "^\\d{4}-\\d{2}-\\d{2}$"}
    }
  }
}
```

**Repeat for all 15 content blocks**:
- `repository-fields.json`
- `priority-urgency.json`
- `deliverables-structure.json`
- `acceptance-criteria-patterns.json`
- `context-background.json`
- `trace-id-format.json`
- `context-rationale.json`
- `estimated-effort-guide.json`
- `timeline-patterns.json`
- `dependencies-pattern.json`
- `related-work-template.json`
- `exploratory-questions.json`
- `collaboration-modes.json`
- `context-boundaries.json`

### Step 2: Create Artifact Assembly Config

**File**: `configs/artifact/coordination-request.json`

```json
{
  "$schema": "https://chora-compose.dev/schemas/artifact-config.json",
  "artifact_type": "coordination-request",
  "version": "1.0.0",
  "description": "SAP-001 coordination request artifact assembly",

  "content_elements": [
    {
      "config": "configs/content/coordination-request/core-metadata.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/repository-fields.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/priority-urgency.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/deliverables-structure.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/acceptance-criteria-patterns.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/context-background.json",
      "required": true,
      "priority": "HIGH"
    },
    {
      "config": "configs/content/coordination-request/trace-id-format.json",
      "required": false,
      "priority": "MEDIUM",
      "condition": "context.trace_id is defined"
    },
    {
      "config": "configs/content/coordination-request/context-rationale.json",
      "required": false,
      "priority": "MEDIUM",
      "condition": "request_type in ['exploratory', 'prescriptive']"
    },
    {
      "config": "configs/content/coordination-request/exploratory-questions.json",
      "required": false,
      "priority": "LOW",
      "condition": "request_type == 'exploratory' AND context.questions is defined"
    },
    {
      "config": "configs/content/coordination-request/collaboration-modes.json",
      "required": false,
      "priority": "LOW",
      "condition": "request_type == 'exploratory' AND from_repo != to_repo"
    }
  ],

  "assembly": {
    "output_format": "json",
    "merge_strategy": "deep_merge",
    "ordering": "by_priority_then_definition"
  },

  "post_processing": {
    "enabled": true,
    "script": "scripts/process-generated-artifact.py",
    "steps": ["validate", "allocate_id", "emit_event", "promote_file"]
  }
}
```

### Step 3: Implement Post-Processing Wrapper

**File**: `scripts/process-generated-artifact.py`

```python
#!/usr/bin/env python3
"""
Post-processing wrapper for chora-compose generated inbox artifacts.

Responsibilities:
1. Validate against SAP-001 JSON schema
2. Allocate request_id from sequence
3. Emit event to events.jsonl
4. Promote draft file to inbox/incoming/
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import jsonschema

def validate_schema(artifact: dict, schema_path: Path) -> bool:
    """Validate artifact against JSON schema."""
    with open(schema_path) as f:
        schema = json.load(f)

    try:
        jsonschema.validate(artifact, schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"Schema validation failed: {e.message}", file=sys.stderr)
        return False

def allocate_request_id(artifact_type: str) -> str:
    """Allocate next request ID from sequence file."""
    sequence_file = Path(f"inbox/.sequence-{artifact_type}")

    if sequence_file.exists():
        current = int(sequence_file.read_text().strip())
    else:
        current = 0

    next_id = current + 1
    sequence_file.write_text(str(next_id))

    year = datetime.now().year
    return f"COORD-{year}-{next_id:03d}"

def emit_event(artifact: dict, event_type: str):
    """Emit event to events.jsonl."""
    event = {
        "event_type": event_type,
        "timestamp": datetime.now().isoformat(),
        "request_id": artifact.get("request_id"),
        "trace_id": artifact.get("trace_id"),
        "from_repo": artifact.get("from_repo"),
        "to_repo": artifact.get("to_repo"),
        "priority": artifact.get("priority"),
        "urgency": artifact.get("urgency")
    }

    events_file = Path("inbox/coordination/events.jsonl")
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

def promote_file(draft_path: Path, artifact: dict):
    """Move draft file to inbox/incoming/ with allocated ID."""
    request_id = artifact["request_id"]
    target_dir = Path("inbox/incoming/coordination")
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / f"{request_id}.json"
    with open(target_path, "w") as f:
        json.dump(artifact, f, indent=2)

    # Clean up draft
    draft_path.unlink()
    print(f"✓ Promoted to {target_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: process-generated-artifact.py <draft-file.json>", file=sys.stderr)
        sys.exit(1)

    draft_path = Path(sys.argv[1])

    # Load draft
    with open(draft_path) as f:
        artifact = json.load(f)

    # Step 1: Validate
    schema_path = Path("schemas/coordination-request.json")
    if not validate_schema(artifact, schema_path):
        sys.exit(1)
    print("✓ Schema validation passed")

    # Step 2: Allocate ID
    request_id = allocate_request_id("coordination")
    artifact["request_id"] = request_id
    print(f"✓ Allocated ID: {request_id}")

    # Step 3: Emit event
    emit_event(artifact, "coordination_request_created")
    print("✓ Event emitted to events.jsonl")

    # Step 4: Promote file
    promote_file(draft_path, artifact)
    print(f"✓ Coordination request {request_id} ready for triage")

if __name__ == "__main__":
    main()
```

### Step 4: Test with Example Contexts

```bash
# Test 1: Exploratory request
chora-compose generate coordination-request \
  --context context-examples/coordination/example-exploratory.json \
  --output inbox/draft/

python scripts/process-generated-artifact.py inbox/draft/coordination-request.json

# Test 2: Prescriptive request
chora-compose generate coordination-request \
  --context context-examples/coordination/example-prescriptive.json \
  --output inbox/draft/

python scripts/process-generated-artifact.py inbox/draft/coordination-request.json

# Test 3: Peer review request
chora-compose generate coordination-request \
  --context context-examples/coordination/example-peer-review.json \
  --output inbox/draft/

python scripts/process-generated-artifact.py inbox/draft/coordination-request.json
```

### Step 5: Evaluate Quality

For each generated artifact, assess against 10-criterion rubric:

```bash
# Run quality assessment
python scripts/evaluate-pilot-quality.py \
  --generated inbox/incoming/coordination/COORD-2025-NNN.json \
  --reference context-examples/coordination/example-exploratory.json \
  --rubric docs/pilots/quality-rubric.json \
  --output results/quality-assessment-NNN.json
```

---

## Reference

### File Structure

```
chora-base/
├── configs/
│   ├── content/
│   │   └── coordination-request/
│   │       ├── core-metadata.json
│   │       ├── repository-fields.json
│   │       ├── priority-urgency.json
│   │       ├── deliverables-structure.json
│   │       ├── acceptance-criteria-patterns.json
│   │       ├── context-background.json
│   │       ├── trace-id-format.json
│   │       ├── context-rationale.json
│   │       ├── estimated-effort-guide.json
│   │       ├── timeline-patterns.json
│   │       ├── dependencies-pattern.json
│   │       ├── related-work-template.json
│   │       ├── exploratory-questions.json
│   │       ├── collaboration-modes.json
│   │       └── context-boundaries.json
│   └── artifact/
│       └── coordination-request.json
├── docs/
│   └── content-blocks/
│       └── inbox-coordination/
│           ├── README.md
│           ├── core-metadata.md
│           ├── repository-fields.md
│           └── ... (13 more)
├── context-examples/
│   └── coordination/
│       ├── context-schema.json
│       ├── example-exploratory.json
│       ├── example-prescriptive.json
│       └── example-peer-review.json
├── scripts/
│   ├── process-generated-artifact.py
│   └── evaluate-pilot-quality.py
├── inbox/
│   ├── draft/  (ephemeral - generated artifacts before processing)
│   ├── incoming/
│   │   └── coordination/  (final artifacts after processing)
│   ├── coordination/
│   │   └── events.jsonl
│   └── .sequence-coordination  (ID allocation)
└── schemas/
    └── coordination-request.json  (SAP-001 schema)
```

### Content Config Schema

Each content config must follow this structure:

```json
{
  "$schema": "https://chora-compose.dev/schemas/content-config.json",
  "name": "string (kebab-case)",
  "version": "semver",
  "description": "string",

  "content_element": {
    "name": "string",
    "format": "json | markdown | yaml",
    "example_output": {}
  },

  "generation": {
    "pattern": "template_fill | demonstration | ai_augmented",
    "template_source": {
      "type": "file | inline",
      "path": "string (if file)",
      "content": "string (if inline)"
    },
    "placeholders": {
      "[placeholder_name]": {
        "source": "literal | user_input | ai_generation | system_function | post_processing",
        "value": "any (if literal)",
        "input": "string (if ai_generation - what to use)",
        "function": "string (if system_function - which function)",
        "guidance": "string (for AI)"
      }
    }
  },

  "validation": {
    "required_fields": ["array of strings"],
    "field_constraints": {
      "[field_name]": {
        "enum": ["array (if enum)"],
        "pattern": "regex string (if pattern)",
        "minLength": "number (if string)",
        "maxLength": "number (if string)"
      }
    }
  }
}
```

### Generation Patterns

**1. template_fill**
- Use when: Content is mostly deterministic with few placeholders
- Example: `core-metadata` (type=literal, ID=post-processing, date=system)

**2. demonstration**
- Use when: Content follows examples but needs adaptation
- Example: `deliverables-structure` (follow patterns from examples)

**3. ai_augmented**
- Use when: Content requires creativity or complex transformation
- Example: `context-background` (expand purpose into narrative)

### Input Sources

**1. literal**
```json
{"source": "literal", "value": "coordination"}
```
Always use this exact value (e.g., type field).

**2. user_input**
```json
{"source": "user_input", "path": "context.priority"}
```
Copy directly from user context (e.g., priority, urgency).

**3. ai_generation**
```json
{
  "source": "ai_generation",
  "input": "context.purpose",
  "guidance": "Expand into 2-3 paragraph narrative explaining background, problem, and why this request"
}
```
AI transforms user input (e.g., purpose → background narrative).

**4. system_function**
```json
{"source": "system_function", "function": "current_date", "format": "YYYY-MM-DD"}
```
System-provided value (e.g., created date, git repo URL).

**5. post_processing**
```json
{"source": "post_processing", "note": "Allocated during post-processing"}
```
Filled by wrapper script after generation (e.g., request_id).

### Quality Rubric (10 Criteria)

| Criterion | Weight | Pass Threshold | Measurement Method |
|-----------|--------|----------------|-------------------|
| Structure Match | 10% | 100% | All required fields present |
| Technical Accuracy | 20% | ≥80% | Expert review of field content |
| Coherence | 15% | ≥75% | Logical flow, consistent tone |
| Completeness | 15% | ≥80% | Deliverables and criteria sufficient |
| JSON Schema | 10% | 100% | jsonschema.validate() passes |
| inbox-status.py | 10% | 100% | inbox-status.py --validate passes |
| Time Reduction | 5% | ≥70% | Actual time vs baseline (30-60 min) |
| Maintainability | 5% | ≥70% | Code review of configs |
| Flexibility | 5% | ≥70% | Handles 3 request types |
| Scalability | 5% | ≥70% | Content blocks reusable for tasks/proposals |

**Overall Pass**: ≥80% weighted score

---

## Appendices

### Appendix A: Decision Rationale

**Why Direct Integration (Option A)?**

From exploration (CORD-2025-002), we evaluated 3 integration approaches:

| Option | Setup Effort | Maintenance | Ecosystem Value | Decision |
|--------|-------------|-------------|-----------------|----------|
| **A: Direct Integration** | 18-26 hours | Low (chora-compose handles updates) | High (shared content blocks) | **CHOSEN** |
| B: Wrapper/Adapter | 39-59 hours | Medium (maintain wrapper + configs) | Medium | Deferred |
| C: Continue Manual | 0 hours | High (manual every time) | None | Rejected |

**Rationale for Option A**:
- Lowest setup effort (fits 4-week pilot)
- Leverages chora-compose's proven architecture
- Maximizes ecosystem synergy (content blocks shareable)
- Clear exit strategy (if pilot fails, minimal sunk cost)

### Appendix B: Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Quality <80% threshold | Low-Medium | High | SAP-004 rubric, 3 test cases, expert review |
| chora-compose integration issues | Low | Medium | Direct collaboration via COORD-2025-002 |
| Time overrun (>42 hours) | Medium | Low | Week-by-week checkpoints, scope flexibility |
| Post-processing bugs | Medium | Medium | Comprehensive testing, manual fallback |

### Appendix C: Success Metrics

**Primary Metric**: Quality ≥80% (weighted rubric)

**Secondary Metrics**:
- Time per artifact: 5-10 minutes (vs 30-60 baseline)
- Error rate: <10% schema violations (vs ~20% manual)
- Developer satisfaction: Positive feedback from 2+ developers

**Data Collection**:
- Generate 3-5 coordination requests
- Measure quality via rubric
- Time each generation (user context → final artifact)
- Survey developers on experience

### Appendix D: Rollback Plan

If pilot fails (quality <70%):

1. **Immediate**: Continue manual process (no disruption)
2. **Week 5**: Document lessons learned
3. **Week 6**: Evaluate Option B (wrapper) or Option C (manual improvements)
4. **Q1 2026**: Revisit with chora-compose v0.6.0 (if features improve fit)

**Sunk Cost**: 28-42 hours (exploration + pilot)
**Benefit Even if Fail**: Content block library (reusable for manual process improvement)

---

**Document Status**: Week 3 - Design (DDD)
**Next Steps**: Create 15-20 content config JSON files
**Target Completion**: 2025-11-15 (Week 3 end)
