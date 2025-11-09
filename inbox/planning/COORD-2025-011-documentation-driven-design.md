---
title: "Coordination Request: Documentation-Driven Design for SAP-012"
type: coordination-request
request_id: COORD-2025-011
from: chora-workspace
to: chora-base
priority: medium
status: under-review
created: 2025-11-08
reviewed: 2025-11-08
response: inbox/outgoing/COORD-2025-011-RESPONSE.md
decision: conditional-approve
related_saps: [SAP-012, SAP-007, SAP-027]
tags: [documentation-driven-design, diataxis, executable-docs, feature-discovery]
---

# Coordination Request: Documentation-Driven Design for SAP-012

**Request ID**: COORD-2025-011
**From**: chora-workspace (Victor Piper)
**To**: chora-base team
**Date**: 2025-11-08
**Priority**: Medium
**Status**: Draft

---

## Executive Summary

**Request**: Enhance SAP-012 Light+ Planning Model to embrace **true Documentation-Driven Design** where **user-facing Diataxis-structured documentation IS the product** and drives BDD feature discovery.

**Current State**: SAP-012 uses DDD (Domain-Driven Design) for complex features and BDD (Behavior-Driven Development) for acceptance criteria, but documentation is seen as a *description* of the product, not the product itself.

**Desired State**: Documentation becomes **the ground truth** from which BDD features are discovered, where:
1. **Diataxis-structured docs** (Tutorial, How-To, Explanation, Reference) are the primary deliverables
2. **How-To guides** are executable (auto-generate E2E tests)
3. **BDD scenarios** are extracted FROM documentation, not written separately
4. **Documentation quality** = **Product quality**

---

## Problem Statement

### Current Workflow (SAP-012 at L2)

```
1. Define Feature Spec (prospective)
   ↓
2. Write BDD Acceptance Criteria (Given/When/Then)
   ↓
3. Implement Code
   ↓
4. Write Documentation (after the fact)
```

**Issue**: Documentation is an afterthought, often drifts from reality.

### Desired Workflow (Documentation-Driven)

```
1. Write User-Facing Documentation (Diataxis-structured)
   - How-To: Executable guides with validation commands
   - Tutorial: Learning-oriented walkthroughs
   - Explanation: Conceptual understanding
   - Reference: Technical specifications
   ↓
2. Extract BDD Scenarios FROM How-To guides
   - Use existing `extract_e2e_tests_from_howtos.py` pattern
   - Generate feature specs from executable docs
   ↓
3. Implement Code to make documentation true
   ↓
4. Validate: E2E tests prove docs work
```

**Benefit**: Documentation becomes the **source of truth**, not a lagging indicator.

---

## Evidence: Executable Documentation Already Works

chora-workspace already has infrastructure for executable how-to guides:

**File**: [docs/user-docs/how-to/write-executable-documentation.md](../../docs/user-docs/how-to/write-executable-documentation.md)

**Key Features**:
- **Frontmatter**: `test_extraction: true` enables E2E test generation
- **Step Format**: `### Step 1:` with Command, Expected Output, Validation blocks
- **Automation**: `extract_e2e_tests_from_howtos.py` generates pytest tests
- **Validation**: Tests prove docs work before each release

**Example Pipeline** (from the guide):

```markdown
1. Write How-To guide (executable format)
   ↓
2. Extract E2E tests: python3 scripts/extract_e2e_tests_from_howtos.py
   ↓
3. Generate DDD Intent: python3 scripts/generate_ddd_intent_from_howto.py
   ↓
4. Generate BDD Scenarios: python3 scripts/generate_bdd_from_intent.py
   ↓
5. Validate bidirectional links: python3 scripts/validate_docs_coverage.py
```

**This already achieves Documentation-Driven Design!**

---

## Proposed Enhancement to SAP-012

### Add "Construct 0: Documentation" (Foundation Level)

**Hierarchy Becomes**:

```
Construct 0: Documentation (Diataxis-structured, executable)
  ↓ discovers
Construct 1: Strategy (Quarterly themes)
  ↓ informs
Construct 2: Releases (Sprints)
  ↓ delivers
Construct 3: Features (BDD specs extracted FROM docs)
  ↓ breaks down into
Construct 4: Tasks (Daily work)
```

### Maturity Levels for Construct 0 (Documentation)

**L0 (Absent)**: No structured documentation

**L1 (Basic)**: Documentation exists but not structured (random READMEs)

**L2 (Configured)**: Diataxis structure adopted
- How-To, Tutorial, Explanation, Reference directories exist
- Frontmatter standards defined
- Basic executable how-to format

**L3 (Active)**: Executable documentation drives development
- 10+ executable how-to guides
- E2E tests auto-generated from docs
- BDD scenarios extracted from how-tos
- Documentation quality gates in CI/CD

**L4 (Deep)**: Documentation-first workflow
- All features start with how-to guides
- Docs reviewed before code
- Automated doc coverage reports
- User feedback loop on docs

**L5 (Mature)**: Documentation IS the product
- Docs deploy as interactive guides
- Metrics on doc usage (which guides are read/executed)
- A/B testing on documentation approaches
- Documentation drives product roadmap

---

## Proposed Changes to SAP-012 Templates

### 1. Add Documentation Section to Feature Spec Template

**Current** (SAP-012 L2):
```markdown
## Problem Statement
## User Stories
## BDD Acceptance Criteria
## Technical Design (optional)
## Tasks
```

**Proposed**:
```markdown
## Problem Statement

## User-Facing Documentation (REQUIRED)
- [ ] How-To guide: `docs/how-to/<feature-name>.md` (executable)
- [ ] Tutorial (if learning-oriented): `docs/tutorial/<feature-name>.md`
- [ ] Explanation (if conceptual): `docs/explanation/<feature-name>.md`
- [ ] Reference (if technical spec): `docs/reference/<feature-name>.md`

## BDD Acceptance Criteria (Extracted from How-To)
<!-- Auto-generated from executable how-to guide -->

## Technical Design (optional)
## Tasks
```

### 2. Update Feature Planning Workflow

**Add Step 2.5: Write Executable How-To** (before BDD scenarios):

```markdown
### Step 2.5: Write Executable How-To Guide (1-2 hours)

1. **Create how-to guide**: `docs/how-to/<feature-name>.md`
2. **Use executable format**:
   - Frontmatter: `test_extraction: true`
   - Steps: `### Step 1:`, `### Step 2:`, etc.
   - Commands, Expected Output, Validation blocks
3. **Extract E2E tests**: Verify tests generate successfully
4. **Extract BDD scenarios**: Use as acceptance criteria

**Benefit**: Documentation drives feature definition, not the reverse
```

### 3. Add Diataxis Reference to SAP-012 Protocol Spec

**Section**: "Documentation Philosophy"

**Content**:
- Explain Diataxis framework (Tutorial, How-To, Explanation, Reference)
- Link to [Diataxis documentation](https://diataxis.fr/)
- Provide chora-base-specific examples for each type
- Explain when to use each documentation type

---

## Integration with Existing SAP-012

### No Breaking Changes

This enhancement is **additive**, not a replacement:

1. **Construct 1-4 unchanged**: Strategy, Releases, Features, Tasks remain
2. **DDD still optional**: For complex domain logic (Step 5)
3. **BDD still required**: But now *extracted* from docs, not written separately
4. **Construct 0 optional at L1-L2**: Only mandatory at L3+ for "documentation-first" teams

### Migration Path

**For existing features**:
- L2 features (BDD-first) remain valid
- L3+ features adopt Documentation-Driven (How-To-first)

**For new features**:
- Recommend Documentation-Driven from the start
- Template suggests: "Write How-To guide first, extract BDD scenarios"

---

## Success Criteria

### Short-Term (L2 → L3 transition)

- [ ] **Template updated**: Feature spec template includes "User-Facing Documentation" section
- [ ] **Workflow documented**: Step 2.5 added to feature planning workflow
- [ ] **Diataxis reference**: SAP-012 protocol spec explains Diataxis framework
- [ ] **Example feature**: 1 prospective feature created using Documentation-Driven approach

### Long-Term (L3 adoption)

- [ ] **10+ executable how-tos**: Across chora-base features
- [ ] **E2E coverage**: 80%+ of how-to guides have passing E2E tests
- [ ] **BDD extraction**: Automated script extracts BDD from how-tos
- [ ] **Doc quality gates**: CI/CD fails if docs don't generate valid tests

---

## Open Questions

### Q1: Should Construct 0 be numbered differently?

**Options**:
- **A**: Construct 0 (Foundation) - comes before Strategy
- **B**: Construct 5 (Documentation) - comes after Tasks
- **C**: Parallel construct (not in hierarchy, applies to all levels)

**Recommendation**: **Option A (Construct 0)** - Documentation is the foundation

### Q2: How to handle non-executable documentation?

**Examples**: Conceptual explanations, architectural decisions, reference specs

**Answer**: Diataxis covers this:
- **How-To**: Executable (task-oriented)
- **Tutorial**: Semi-executable (learning-oriented)
- **Explanation**: Non-executable (conceptual)
- **Reference**: Non-executable (technical specs)

Only **How-To** guides need to be executable. Others are traditional docs.

### Q3: Compatibility with existing DDD/BDD/TDD workflow?

**Answer**: Fully compatible:
- **How-To** → **BDD scenarios** (auto-extracted)
- **BDD scenarios** → **TDD tests** (existing process)
- **DDD models** remain optional for complex features

Documentation-Driven **enhances** the workflow, doesn't replace it.

---

## Proposed Timeline

### Phase 1: Template Enhancement (1-2 hours)

- Update feature spec template with "User-Facing Documentation" section
- Add Step 2.5 to feature planning workflow
- Document Diataxis framework in SAP-012 protocol spec

### Phase 2: Example Feature (2-3 hours)

- Create 1 prospective feature using Documentation-Driven approach
- Write executable how-to guide first
- Extract BDD scenarios from how-to
- Validate E2E tests pass

### Phase 3: Validation & Distribution (1-2 hours)

- Document patterns in knowledge note
- Add to SAP-012 L3 criteria
- Distribute updated templates to chora-base

**Total Effort**: 4-7 hours

---

## References

### chora-workspace Evidence

- **Executable How-To Guide**: [write-executable-documentation.md](../../docs/user-docs/how-to/write-executable-documentation.md)
- **Extraction Script**: `scripts/extract_e2e_tests_from_howtos.py` (referenced in guide)
- **Validation Pipeline**: E2E test → DDD Intent → BDD Scenarios → Bidirectional links

### Diataxis Framework

- **Official Site**: https://diataxis.fr/
- **Four Types**:
  - **Tutorial**: Learning-oriented (take me by the hand)
  - **How-To**: Task-oriented (show me how to solve this problem)
  - **Explanation**: Understanding-oriented (help me understand)
  - **Reference**: Information-oriented (tell me the facts)

### Related SAPs

- **SAP-012**: Development Lifecycle (Light+ Planning Model)
- **SAP-010**: A-MEM (Memory system, templates)
- **SAP-019**: Self-Evaluation (quality metrics)

---

## Requested Actions

### From chora-base Team

1. **Review**: Assess feasibility of adding Construct 0 (Documentation) to SAP-012
2. **Feedback**: Is Diataxis alignment desirable for chora-base?
3. **Decision**: Should this be SAP-012 enhancement or separate SAP (e.g., SAP-030: Documentation-Driven Design)?
4. **Timeline**: If approved, when could this be integrated?

### From chora-workspace

1. **Prototype**: Create 1 feature using Documentation-Driven approach
2. **Validate**: Prove executable how-to → BDD extraction workflow
3. **Document**: Capture patterns in knowledge note
4. **Share**: Provide example to chora-base for review

---

## Next Steps (If Approved)

1. **chora-workspace**: Prototype Documentation-Driven feature (1 sprint)
2. **chora-base**: Review prototype and provide feedback
3. **Joint**: Refine SAP-012 templates and workflow
4. **chora-base**: Distribute updated SAP-012 to ecosystem
5. **chora-workspace**: Adopt at L3 (10+ executable how-tos)

---

## Appendix: Example Transformation

### Current Approach (BDD-First)

**Feature Spec**: `2025-11-sap-015-l3-adoption.md`

```markdown
## BDD Acceptance Criteria

Scenario: Adopt new Beads tracking scripts
  Given chora-base has sap015-*.py scripts
  When I test sap015-create-task.py
  Then task is created in .beads/issues.jsonl
  And task has correct JSON schema
```

**Problem**: Where's the user documentation?

### Documentation-Driven Approach

**How-To Guide**: `docs/how-to/use-beads-task-tracking.md`

```markdown
---
title: "How to Create Tasks with Beads"
type: how-to
test_extraction: true
execution_mode: local
e2e_test_id: beads-create-task
---

# How to Create Tasks with Beads

## Steps

### Step 1: Create a Task

**Command:**
\`\`\`bash
python scripts/beads-add-task.py "Task title" "Description" 1
\`\`\`

**Expected Output:**
\`\`\`
[OK] Task created: chora-workspace-abc - Task title
\`\`\`

**Validation:**
\`\`\`bash
tail -n 1 .beads/issues.jsonl | python -m json.tool | grep -q "Task title" && echo "Task created"
\`\`\`
```

**Feature Spec**: `2025-11-sap-015-l3-adoption.md`

```markdown
## User-Facing Documentation

- [x] How-To: [use-beads-task-tracking.md](../../docs/how-to/use-beads-task-tracking.md) ✅

## BDD Acceptance Criteria (Extracted from How-To)

Scenario: Create a task with Beads (from Step 1 of how-to)
  Given I have beads-add-task.py script
  When I run `python scripts/beads-add-task.py "Task title" "Description" 1`
  Then output shows "[OK] Task created: chora-workspace-abc - Task title"
  And `.beads/issues.jsonl` contains a new task with title "Task title"
  And task JSON passes schema validation
```

**Benefits**:
1. ✅ **Users get documentation** (how-to guide)
2. ✅ **Developers get BDD scenarios** (extracted from how-to)
3. ✅ **E2E tests validate** (docs prove they work)
4. ✅ **Single source of truth** (how-to drives everything)

---

**Status**: Draft (awaiting chora-base team review)
**Expected Response Time**: 1-2 weeks
**Contact**: Victor Piper (chora-workspace maintainer)

---

**Created**: 2025-11-08
**Framework**: SAP-012 Light+ Planning Model
**Related Request**: None (first of its kind)
**Priority Justification**: Medium - Enhances SAP-012 but not blocking current work
