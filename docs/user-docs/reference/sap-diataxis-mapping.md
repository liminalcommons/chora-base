# SAP Artifact to Diataxis Mapping

**Document Type**: Reference
**Purpose**: Definitive guide for mapping SAP artifacts to Diataxis documentation categories
**Audience**: SAP authors, documentation reviewers, quality auditors
**Last Updated**: 2025-11-04

---

## Overview

The Skilled Awareness Package (SAP) framework is explicitly designed around the [Diataxis documentation framework](https://diataxis.fr/), which defines four distinct documentation types based on user intent. Each of the 5 required SAP artifacts maps to a specific Diataxis category.

This reference provides the authoritative mapping, content guidelines, and decision matrix for SAP documentation.

---

## Quick Reference: Artifact-to-Diataxis Mapping

| SAP Artifact | Diataxis Category | User Intent | Primary Purpose |
|--------------|-------------------|-------------|-----------------|
| **capability-charter.md** | **Explanation** | Understanding-oriented | WHY this capability exists, context, rationale, design decisions |
| **protocol-spec.md** | **Reference** | Information-oriented | Technical specifications, APIs, data models, contracts |
| **awareness-guide.md** | **How-To Guide** | Task-oriented | Solve specific problems, workflows, common patterns |
| **adoption-blueprint.md** | **Tutorial** | Learning-oriented | Step-by-step installation, getting started, learning journey |
| **ledger.md** | **Reference** | Information-oriented | Factual records, version history, adoption tracking |

---

## The Four Diataxis Quadrants

### Quadrant 1: Tutorials (Learning-Oriented)

**Diataxis Definition**: Tutorials are learning-oriented lessons that take the reader through a series of steps to complete a project.

**SAP Artifact**: `adoption-blueprint.md`

**Key Characteristics**:
- **Learning journey**: Teaches while doing
- **Safe environment**: Clear validation points, reversible actions
- **Beginner-friendly**: No assumed knowledge beyond stated prerequisites
- **Sequential steps**: Progressive skill building (simple → complex)
- **Concrete**: Uses real examples and actual outcomes

**Content Should Include**:
- Prerequisites (what you need before starting)
- Step-by-step instructions with expected outcomes
- Validation commands at each checkpoint
- Success criteria ("you should now have X")
- Post-installation tasks (awareness enablement)

**Content Should Avoid**:
- Problem-solving focus (belongs in how-to)
- Detailed API specifications (belongs in reference)
- Design rationale (belongs in explanation)
- Troubleshooting (belongs in how-to)

**Example Good Tutorial Content**:
```markdown
### Step 1: Create Inbox Directory

Let's create the inbox coordination structure in your project.

**What you'll learn**: How to set up the basic coordination infrastructure

**Steps**:
1. Create the directory:
   ```bash
   mkdir -p inbox/coordination
   ```

2. Verify it exists:
   ```bash
   ls -la inbox/
   # Expected output: coordination/
   ```

**Checkpoint**: You should now have `inbox/coordination/` in your project root.

**Next**: We'll add your first coordination event.
```

---

### Quadrant 2: How-To Guides (Task-Oriented)

**Diataxis Definition**: How-to guides are task-oriented directions that take the reader through the steps required to solve a real-world problem.

**SAP Artifact**: `awareness-guide.md`

**Key Characteristics**:
- **Problem → Solution**: Addresses specific tasks or challenges
- **Assumes knowledge**: Readers already understand basics (from tutorial)
- **Practical**: Shows how to achieve a specific goal
- **Flexible**: Multiple paths to solution may exist
- **Concrete examples**: Real scenarios, not hypotheticals

**Content Should Include**:
- Common workflows and use cases
- Problem-solution pairs
- Tool usage patterns (Read, Write, Edit, Bash)
- Cross-domain references (dev-docs/, project-docs/, user-docs/)
- Common pitfalls and how to avoid them
- Troubleshooting guidance

**Content Should Avoid**:
- Teaching fundamentals step-by-step (belongs in tutorial)
- Pure technical specifications without context (belongs in reference)
- Design rationale without actionable tasks (belongs in explanation)
- Hypothetical examples (use concrete ones)

**Example Good How-To Content**:
```markdown
### Finding Highest-Priority Pending Task

**Problem**: Agent needs to identify which task to work on next based on priority.

**Solution**:
1. Parse the coordination events file
2. Filter by pending status
3. Sort by priority field
4. Return the top result

**Implementation**:
```bash
jq -r 'select(.status=="pending") | [.priority, .title] | @tsv' \
  inbox/coordination/events.jsonl | sort | head -1
```

**Common Pitfall**: Forgetting to filter by status first can return completed tasks.

**See Also**: [Event Schema Reference](../../skilled-awareness/inbox/protocol-spec.md#event-schema)
```

---

### Quadrant 3: Reference (Information-Oriented)

**Diataxis Definition**: Reference guides are technical descriptions of the machinery and how to operate it.

**SAP Artifacts**: `protocol-spec.md` (primary), `ledger.md` (adoption records)

**Key Characteristics**:
- **Factual**: Comprehensive, accurate, structured information
- **Dry**: No teaching narrative or problem-solving
- **Comprehensive**: Covers all aspects of the interface
- **Consistent**: Predictable structure and format
- **Authoritative**: The single source of truth

**Content Should Include** (protocol-spec.md):
- Input/output specifications
- API interfaces and schemas
- Data models and types
- Guarantees and constraints
- Error cases and handling
- Dependencies (internal, external)
- Versioning contracts

**Content Should Include** (ledger.md):
- Adoption records (who, when, version)
- Version history with dates
- Feedback mechanism
- Status tracking
- Purely factual data

**Content Should Avoid**:
- Learning journeys or progressive teaching (belongs in tutorial)
- Task-solving patterns (belongs in how-to)
- Design rationale or explanations of why (belongs in explanation)
- Subjective descriptions

**Example Good Reference Content** (protocol-spec.md):
```markdown
### Event Schema

**Data Model**:
```yaml
coordination_request:
  trace_id: string (UUID v4)
  priority: enum ["critical", "high", "medium", "low"]
  dependencies: array<string> (trace_ids)
  status: enum ["pending", "in_progress", "completed"]
  title: string (1-200 chars)
  created_at: string (ISO 8601 datetime)
```

**Guarantees**:
- Events are immutable (append-only)
- Trace IDs are globally unique
- Status transitions follow: pending → in_progress → completed
- Dependencies reference valid trace_ids

**Constraints**:
- trace_id MUST be UUID v4 format
- priority MUST be one of the four enum values
- dependencies array MAY be empty
```

**Example Good Reference Content** (ledger.md):
```markdown
| Project | Version | Installed | Status | Feedback |
|---------|---------|-----------|--------|----------|
| chora-base | 1.0.0 | 2025-01-15 | Active | N/A (self-hosted) |
| project-alpha | 1.0.0 | 2025-02-01 | Pilot | Positive - improved coordination |
```

---

### Quadrant 4: Explanation (Understanding-Oriented)

**Diataxis Definition**: Explanations are discussions that clarify and illuminate a particular topic.

**SAP Artifact**: `capability-charter.md`

**Key Characteristics**:
- **Understanding-focused**: Explains WHY, not HOW
- **Context-rich**: Provides background and motivation
- **Discusses alternatives**: Trade-offs and design decisions
- **Conceptual**: Ideas and principles, not procedures
- **Broader perspective**: Connects to larger picture

**Content Should Include**:
- Problem statement (current challenge, evidence, impact)
- Why this solution (rationale, principles)
- Scope and boundaries
- Design trade-offs and alternatives considered
- Success criteria and outcomes
- Stakeholder analysis
- Dependencies and constraints
- Risks and mitigation

**Content Should Avoid**:
- Step-by-step instructions (belongs in tutorial)
- API specifications or schemas (belongs in reference)
- Task-solving workflows (belongs in how-to)
- Generic problem statements without specific context

**Example Good Explanation Content**:
```markdown
### Why This Capability Exists

The inbox coordination protocol emerged from a critical gap in existing project management systems: they optimize for human decision-making but lack machine-readable coordination primitives. This creates friction when AI agents need to understand project priorities, dependencies, and status.

**Design Trade-offs**:

**JSONL format over database**:
- *Rationale*: Git-friendly, human-readable, append-only by nature
- *Trade-off*: Less query performance than SQL
- *Decision*: Version control and auditability outweigh query speed needs

**Event-driven over state-based**:
- *Rationale*: Enables complete audit trail, immutable history
- *Trade-off*: Requires event replay for current state
- *Decision*: Traceability is critical for agent coordination

**Schema-first over ad-hoc**:
- *Rationale*: Ensures machine parsability and validation
- *Trade-off*: Less flexibility for experimentation
- *Decision*: Reliability over flexibility for coordination primitives
```

---

## Decision Matrix: Which Artifact for Which Content?

Use this decision matrix when unsure where content belongs:

| Content Type | Goes In | Not In |
|--------------|---------|--------|
| **Why this capability exists** | capability-charter | protocol-spec, awareness-guide |
| **Problem context and background** | capability-charter | adoption-blueprint |
| **Design trade-offs** | capability-charter | protocol-spec, awareness-guide |
| **Technical specifications** | protocol-spec | capability-charter, adoption-blueprint |
| **API schemas and data models** | protocol-spec | awareness-guide, adoption-blueprint |
| **Guarantees and constraints** | protocol-spec | capability-charter |
| **How to solve specific problem** | awareness-guide | adoption-blueprint, protocol-spec |
| **Common workflows** | awareness-guide | adoption-blueprint |
| **Tool usage patterns** | awareness-guide | protocol-spec |
| **Troubleshooting** | awareness-guide | adoption-blueprint |
| **Step-by-step installation** | adoption-blueprint | capability-charter, awareness-guide |
| **Learning journey (getting started)** | adoption-blueprint | protocol-spec, awareness-guide |
| **Prerequisites** | adoption-blueprint | protocol-spec |
| **Validation commands** | adoption-blueprint | capability-charter |
| **Post-install awareness setup** | adoption-blueprint | awareness-guide |
| **Version history** | ledger | capability-charter, protocol-spec |
| **Adoption records** | ledger | awareness-guide |

---

## Common Anti-Patterns and How to Fix Them

### Anti-Pattern 1: Tutorial Content in Reference Docs

**Symptom**: Protocol-spec has "Let's create a schema" or "You'll learn how to..."

**Problem**: Reference docs should be factual, not teach

**Fix**: Move learning-oriented content to adoption-blueprint, leave only spec in protocol-spec

**Before (❌ Bad)**:
```markdown
# protocol-spec.md
## Creating Your First Event

Let's create your first coordination event! Follow these steps:
1. Open inbox/coordination/events.jsonl
2. Add the following JSON...
```

**After (✅ Good)**:
```markdown
# protocol-spec.md
## Event Schema

**Structure**:
```yaml
event:
  trace_id: string (UUID v4)
  ...
```

**Guarantees**: Events are immutable...
```
*(Tutorial content moved to adoption-blueprint.md)*

---

### Anti-Pattern 2: Reference Content in Tutorials

**Symptom**: Adoption-blueprint includes detailed API schemas or comprehensive spec tables

**Problem**: Tutorials should teach, not document every detail

**Fix**: Link to protocol-spec for details, keep tutorial focused on learning journey

**Before (❌ Bad)**:
```markdown
# adoption-blueprint.md
## Step 2: Understand Event Schema

The event schema has the following complete specification:

| Field | Type | Required | Constraints | Default | ...
|-------|------|----------|-------------|---------|...
[50 rows of complete API reference]
```

**After (✅ Good)**:
```markdown
# adoption-blueprint.md
## Step 2: Create Your First Event

You'll create a simple coordination event with the required fields.

**Basic event structure**:
```json
{
  "trace_id": "123e4567-e89b-12d3-a456-426614174000",
  "priority": "high",
  "title": "My first task"
}
```

For complete event schema, see [Protocol Spec](protocol-spec.md#event-schema).
```

---

### Anti-Pattern 3: How-To Content in Tutorials

**Symptom**: Adoption-blueprint includes troubleshooting or problem-solving sections

**Problem**: Tutorials should be safe learning journeys, not problem-solving guides

**Fix**: Move troubleshooting to awareness-guide, keep blueprint focused on happy path

**Before (❌ Bad)**:
```markdown
# adoption-blueprint.md
## Troubleshooting Installation

**Problem**: Events file is corrupted
**Solution**: Run validation script...

**Problem**: Schema validation fails
**Solution**: Check JSON format...
```

**After (✅ Good)**:
```markdown
# adoption-blueprint.md
## Validation

Run this command to verify your installation:
```bash
python scripts/validate-inbox.py
```

**Expected output**: `✅ All checks passed`

If you encounter issues, see [Troubleshooting Guide](awareness-guide.md#troubleshooting).
```
*(Troubleshooting section moved to awareness-guide.md)*

---

### Anti-Pattern 4: Explanation Content in How-To Guides

**Symptom**: Awareness-guide spends paragraphs explaining why something was designed a certain way

**Problem**: How-to guides should solve tasks, not explain rationale

**Fix**: Move design rationale to capability-charter, keep awareness-guide task-focused

**Before (❌ Bad)**:
```markdown
# awareness-guide.md
## Why We Use JSONL Format

The decision to use JSONL over traditional databases was carefully considered.
We evaluated SQL databases, NoSQL solutions, and file-based formats.
The rationale for JSONL includes...
[3 paragraphs of explanation]
```

**After (✅ Good)**:
```markdown
# awareness-guide.md
## Parsing Events from JSONL

**Problem**: Agent needs to read coordination events

**Solution**: Use `jq` to parse JSONL file:
```bash
jq -r '.title' inbox/coordination/events.jsonl
```

*For rationale behind JSONL format choice, see [Capability Charter](capability-charter.md#design-decisions).*
```

---

### Anti-Pattern 5: Task-Oriented Content in Explanation

**Symptom**: Capability-charter includes "How to install" or specific workflows

**Problem**: Charters explain why, not how

**Fix**: Move procedural content to appropriate artifact

**Before (❌ Bad)**:
```markdown
# capability-charter.md
## Installation Process

To install the inbox protocol:
1. Run `mkdir inbox/coordination`
2. Copy events.jsonl template
3. Update AGENTS.md
```

**After (✅ Good)**:
```markdown
# capability-charter.md
## Adoption Strategy

Successful adoption requires three capabilities:
1. **File structure setup**: Establishes coordination infrastructure
2. **Schema validation**: Ensures event integrity
3. **Awareness integration**: Enables agent discoverability

*See [Adoption Blueprint](adoption-blueprint.md) for installation steps.*
```

---

## Diataxis Compliance Checklist

Use this checklist when creating or reviewing SAP documentation:

### Capability-Charter (Explanation)
- [ ] Explains WHY capability exists (problem context, motivation)
- [ ] Discusses design trade-offs and alternatives
- [ ] Provides rationale for key decisions
- [ ] Avoids step-by-step instructions (no "Step 1, Step 2")
- [ ] Avoids API specifications (no schemas, interfaces)
- [ ] Focuses on understanding, not doing

### Protocol-Spec (Reference)
- [ ] Factual, comprehensive technical specifications
- [ ] Includes data models, schemas, APIs
- [ ] Documents guarantees, constraints, error cases
- [ ] Avoids tutorial language ("Let's", "You'll learn")
- [ ] Avoids problem-solving patterns ("If you need to")
- [ ] Avoids design rationale ("We chose this because")

### Awareness-Guide (How-To)
- [ ] Solves specific problems (task-oriented)
- [ ] Provides concrete examples (not hypotheticals)
- [ ] Assumes knowledge (not teaching fundamentals)
- [ ] Includes cross-domain references (2+ domains)
- [ ] Has troubleshooting or common pitfalls section
- [ ] Avoids learning journey structure
- [ ] Avoids detailed specifications

### Adoption-Blueprint (Tutorial)
- [ ] Learning-oriented (teaches while doing)
- [ ] Sequential steps with expected outcomes
- [ ] Validation checkpoints at each stage
- [ ] Beginner-friendly (minimal assumed knowledge)
- [ ] Safe to experiment (clear rollback/validation)
- [ ] Avoids problem-solving focus
- [ ] Avoids detailed API reference
- [ ] Includes post-install awareness enablement

### Ledger (Reference)
- [ ] Factual adoption records (who, when, version)
- [ ] Version history with dates
- [ ] No tutorial or explanatory content
- [ ] Structured format (tables recommended)

---

## Validation Process

### Automated Validation

Run SAP quality analyzer with Diataxis scoring:
```bash
python scripts/analyze_sap_quality.py
```

This will check each artifact for Diataxis compliance and report:
- Per-artifact Diataxis score (0-100)
- Overall Diataxis compliance (pass/partial/fail)
- Specific category misalignments

### Manual Validation

Follow [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) Step 4.6: Diataxis Compliance Check

This includes:
- Artifact-by-artifact category validation
- Diataxis compliance scorecard
- Content reorganization recommendations

---

## Resources

**Diataxis Framework**:
- [Official Diataxis Documentation](https://diataxis.fr/)
- [Diataxis Interactive Map](https://diataxis.fr/compass/)

**SAP Framework**:
- [SAP-000: SAP Framework Protocol Spec](../../skilled-awareness/sap-framework/protocol-spec.md#diataxis-framework-compliance)
- [SAP-007: Documentation Framework](../../skilled-awareness/documentation-framework/)
- [SAP Audit Workflow](../../dev-docs/workflows/SAP_AUDIT_WORKFLOW.md)

**Quality Tools**:
- `scripts/analyze_sap_quality.py` - Automated Diataxis compliance scoring
- [SAP Quality Gates](../../skilled-awareness/sap-framework/protocol-spec.md#quality-gates)

---

## Frequently Asked Questions

### Q: Can an artifact mix Diataxis categories?

**A**: Some mixing is natural and acceptable, but each artifact should have a **clear primary category**. For example:

- ✅ **Acceptable**: Awareness-guide (How-To) links to protocol-spec (Reference) for details
- ✅ **Acceptable**: Adoption-blueprint (Tutorial) includes brief explanation of why a step is needed
- ❌ **Avoid**: Capability-charter (Explanation) with detailed step-by-step instructions
- ❌ **Avoid**: Protocol-spec (Reference) teaching concepts instead of documenting specs

### Q: What if my capability doesn't need all quadrants?

**A**: All SAPs must have all 5 artifacts, but the depth can vary:

- Simple capabilities may have brief charters (1-2 pages)
- Infrastructure SAPs may have extensive protocol-specs
- All SAPs need adoption-blueprint (installation is always a tutorial)
- All SAPs need awareness-guide (agents need to know how to use it)

Even if brief, each artifact must adhere to its Diataxis category.

### Q: How do I know if my Diataxis compliance is good enough?

**A**: Quality gates for SAP status:

- **Pilot status**: 4/5 artifacts pass Diataxis compliance (≥75 score)
- **Active status**: 5/5 artifacts pass Diataxis compliance

Run `python scripts/analyze_sap_quality.py` to see your scores.

### Q: What if I find mixed content in existing SAPs?

**A**: File a gap in the SAP audit report and prioritize based on severity:

- **Critical**: Tutorials in reference docs (confuses readers)
- **High**: Missing core Diataxis elements (e.g., charter with no "why")
- **Medium**: Minor mixing (e.g., brief explanation in how-to)

---

**Document Version**: 1.0
**Status**: Active
**Last Updated**: 2025-11-04

This reference demonstrates the **Reference** quadrant of Diataxis: factual, comprehensive information about SAP-to-Diataxis mapping, presented without teaching or problem-solving.
