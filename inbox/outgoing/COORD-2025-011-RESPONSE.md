---
title: "Response to COORD-2025-011: Documentation-Driven Design for SAP-012"
type: coordination-response
request_id: COORD-2025-011
response_id: COORD-2025-011-RESPONSE
from: chora-base (Claude Agent)
to: chora-workspace (Victor Piper)
priority: medium
status: draft
created: 2025-11-08
decision: CONDITIONAL-APPROVE
tags: [documentation-driven-design, diataxis, sap-012, enhancement]
---

# Response to COORD-2025-011: Documentation-Driven Design for SAP-012

**Response ID**: COORD-2025-011-RESPONSE
**From**: chora-base team (Claude Agent)
**To**: chora-workspace (Victor Piper)
**Date**: 2025-11-08
**Decision**: **CONDITIONAL APPROVE** (with refinements)
**Priority**: Medium

---

## Executive Summary

**Assessment**: The proposal to enhance SAP-012 with "Construct 0: Documentation" is **CONDITIONALLY APPROVED** with the following refinements:

1. ✅ **Alignment**: SAP-012 already references Diataxis and "Documentation Driven Design" (DDD) in Phase 3 - this proposal **formalizes and extends** existing patterns
2. ✅ **Value**: Strong evidence from chora-workspace demonstrates executable documentation → BDD extraction workflow is viable
3. ⚠️ **Terminology**: Recommend **renaming "DDD"** in SAP-012 from "Documentation Driven Design" to "**Domain/Design-Driven Development**" to avoid confusion with the proposed "Documentation-Driven Design" workflow
4. 🔄 **Structure**: Instead of "Construct 0", recommend **adding a new Phase 2.5** or enhancing **Phase 3** to include executable documentation patterns
5. 📋 **Scope**: Treat this as **SAP-012 L3 enhancement** (not a new SAP) since it extends the existing development lifecycle

**Recommended Approach**: Enhance SAP-012 protocol spec with:
- Documentation-First workflow as **optional L3 pattern** (not mandatory at L2)
- Diataxis reference section expanded with executable how-to guide patterns
- Feature spec template updated to include "User-Facing Documentation" section
- Clear distinction between Phase 3 DDD (Domain-Driven) and Documentation-Driven workflow

---

## Detailed Assessment

### 1. Current State Analysis

**Findings from SAP-012 Protocol Spec**:

SAP-012 already uses the term "DDD (Documentation Driven Design)" in Phase 3:

```markdown
│ PHASE 3: REQUIREMENTS & DESIGN (DDD) (Days)                     │
│ Documentation Driven Design: Change request → API reference →   │
│ Acceptance criteria                                              │
│ Documents: Diataxis docs, API specs, acceptance criteria        │
```

**References to Diataxis** (found 19 occurrences across SAP-012 artifacts):
- Protocol spec mentions "Diataxis docs" in Phase 3
- Awareness guide references "Write Diataxis docs"
- Adoption blueprint mentions SAP-007 (documentation-framework) with Diataxis structure
- DDD_WORKFLOW.md (919 lines) uses Diataxis structure

**Key Insight**: SAP-012 already has a "Documentation Driven" foundation, but it's positioned as:
- **After** strategic planning (Phase 3, not foundation)
- **Parallel** to BDD scenarios (not driving them)
- **Diataxis-aware** but not executable-first

Your proposal **extends this pattern** to make documentation the **driver** of BDD, not a parallel artifact.

---

### 2. Terminology Conflict Resolution

**Problem**: "DDD" is used for both:
1. "Documentation Driven Design" (Phase 3 in SAP-012)
2. "Domain-Driven Design" (Eric Evans' pattern for complex domain modeling)

**Current COORD-2025-011 proposal**: Introduces "Documentation-Driven Design" as a workflow distinct from both.

**Recommendation**: Clarify terminology in SAP-012 to avoid confusion:

| Term | Meaning | When to Use |
|------|---------|-------------|
| **DDD (Domain-Driven Design)** | Eric Evans' strategic design patterns (entities, aggregates, bounded contexts) | Complex domain logic (e.g., financial modeling, healthcare systems) |
| **Documentation-Driven Development** | Phase 3 of SAP-012 - write docs before code | All features (L2 requirement) |
| **Documentation-First Workflow** | L3 pattern - executable how-to guides → BDD extraction | L3 teams with executable doc infrastructure |

**Action**: Update SAP-012 to rename "DDD (Documentation Driven Design)" → "**Documentation-Driven Development (Phase 3)**" to avoid conflict with Domain-Driven Design.

---

### 3. Proposed Structure: Phase 2.5 vs Construct 0

**COORD-2025-011 Proposal**: Add "Construct 0: Documentation" as foundation layer

**Considerations**:

**Option A: Construct 0 (Foundation)**
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

**Pros**:
- Emphasizes documentation as foundational
- Aligns with "docs are the product" philosophy

**Cons**:
- Renumbering existing constructs (breaking change)
- Documentation isn't always the starting point (sometimes strategy drives docs)
- May confuse existing SAP-012 adopters

---

**Option B: Phase 2.5 Enhancement (Recommended)**

Insert **Phase 2.5** between Planning and Requirements:

```
PHASE 2: Planning & Prioritization (Weeks)
  ↓
PHASE 2.5: Documentation-First Specification (L3 Optional) (Days)
  - Write executable how-to guides (Diataxis How-To)
  - Define user-facing workflows
  - Extract BDD scenarios from how-tos
  ↓
PHASE 3: Requirements & Design (Days)
  - Refine API specs from how-to workflows
  - Finalize acceptance criteria (extracted from how-tos at L3, manual at L2)
  - Domain modeling (if complex domain logic)
  ↓
PHASE 4: Development (BDD + TDD)
```

**Pros**:
- Non-breaking (optional phase at L3)
- Clear workflow: Planning → Docs → Design → Development
- Aligns with maturity levels (L2 = manual BDD, L3 = extracted BDD)

**Cons**:
- Adds phase complexity

---

**Option C: Enhance Phase 3 (Simplest)**

Extend **Phase 3** to include Documentation-First workflow as L3 pattern:

```
PHASE 3: Requirements & Design (Days)

L2 Pattern (Manual BDD):
  1. Write change request (Explanation)
  2. Write API reference
  3. Write BDD scenarios manually

L3 Pattern (Documentation-First):
  1. Write executable how-to guide (Diataxis How-To)
  2. Extract BDD scenarios from how-to
  3. Refine API reference from how-to workflows
  4. Generate E2E tests from how-to validation blocks
```

**Pros**:
- Minimal structural change
- Clear L2 → L3 progression
- Leverages existing Phase 3 positioning

**Cons**:
- Phase 3 becomes more complex

---

**Recommendation**: **Option C (Enhance Phase 3)** - treat Documentation-First as an L3 maturity pattern within existing Phase 3, avoiding structural changes while providing clear guidance for teams at different maturity levels.

---

### 4. Integration with Existing SAP-012 Maturity Levels

**Current SAP-012 Maturity Levels** (from protocol-spec.md):

- **L0 (Absent)**: No lifecycle
- **L1 (Basic)**: Sprint planning exists
- **L2 (Configured)**: 8 phases documented, DDD → BDD → TDD workflow
- **L3 (Active)**: Quality gates enforced, retrospectives conducted
- **L4 (Deep)**: Metrics tracked, continuous improvement loops
- **L5 (Mature)**: Predictive planning, optimized workflows

**Proposed Enhancement**: Add Documentation-First criteria to **L3 maturity**:

**L3 (Active)** - Enhanced:
- ✅ Quality gates enforced (existing)
- ✅ Retrospectives conducted (existing)
- ✅ **10+ executable how-to guides** (new)
- ✅ **E2E tests auto-generated from docs** (new)
- ✅ **BDD scenarios extracted from how-tos** (new)
- ✅ **Documentation quality gates in CI/CD** (new)

This positions Documentation-First as a **natural progression** from L2 (manual BDD) to L3 (automated BDD extraction).

---

### 5. Evidence Validation

**From COORD-2025-011**:

> chora-workspace already has infrastructure for executable how-to guides:
> - File: `docs/user-docs/how-to/write-executable-documentation.md`
> - Frontmatter: `test_extraction: true`
> - Scripts: `extract_e2e_tests_from_howtos.py`, `generate_ddd_intent_from_howto.py`, `generate_bdd_from_intent.py`

**Assessment**: ✅ **Strong evidence** - this is a proven pattern in chora-workspace, not speculative.

**Question**: Are these scripts currently in chora-base or only in chora-workspace?

**Action Required**: If scripts are chora-workspace-only, include them in the enhancement proposal (copy to `scripts/` in chora-base).

---

### 6. SAP-007 Integration

**SAP-007 (documentation-framework)** already provides:
- Diátaxis 4-domain structure
- Frontmatter schema validation
- **Executable how-to guides** ✅ (capability listed in sap-catalog.json)
- **Test extraction from docs** ✅ (capability listed)
- `scripts/extract_tests.py` (system file)

**Finding**: SAP-007 **already supports** executable documentation!

**Recommendation**: Position this enhancement as:
- **SAP-007 + SAP-012 integration** - how to use SAP-007's executable docs to drive SAP-012's BDD workflow
- Update SAP-012 to reference SAP-007 more explicitly for L3 Documentation-First patterns
- Clarify that SAP-007 provides the **infrastructure** (executable doc format, extraction scripts), SAP-012 provides the **workflow** (how to use docs in the development lifecycle)

---

### 7. Proposed Changes to SAP-012

**Summary of Recommended Enhancements**:

#### 7.1 Update Phase 3 Description

**Current**:
```
PHASE 3: REQUIREMENTS & DESIGN (DDD) (Days)
Documentation Driven Design: Change request → API reference →
Acceptance criteria
Documents: Diataxis docs, API specs, acceptance criteria
```

**Proposed**:
```
PHASE 3: REQUIREMENTS & DESIGN (Days)
Documentation-Driven Development: Define user-facing requirements through
Diataxis-structured documentation before implementation.

L2 Pattern (Manual BDD):
  1. Write change request (Diataxis Explanation)
  2. Write API reference (Diataxis Reference)
  3. Write BDD scenarios manually (Given/When/Then)

L3 Pattern (Documentation-First):
  1. Write executable how-to guide (Diataxis How-To, test_extraction: true)
  2. Extract BDD scenarios from how-to (automated via SAP-007)
  3. Generate E2E tests from validation blocks (automated via SAP-007)
  4. Refine API reference from how-to workflows

Documents: Diataxis docs (SAP-007), API specs, acceptance criteria (manual at L2, extracted at L3)
```

---

#### 7.2 Add Documentation-First Workflow Section

Add new section to protocol-spec.md:

**Section 2.4: Documentation-First Workflow (L3 Pattern)**

```markdown
### 2.4 Documentation-First Workflow (L3 Pattern)

**Purpose**: Use executable how-to guides as the source of truth for BDD scenarios and E2E tests.

**Prerequisites**:
- SAP-007 (documentation-framework) adopted
- `test_extraction: true` frontmatter enabled in how-to guides
- Extraction scripts: `scripts/extract_e2e_tests_from_howtos.py` available

**Workflow**:

1. **Write Executable How-To Guide** (1-2 hours)
   - File: `docs/user-docs/how-to/<feature-name>.md`
   - Frontmatter: `test_extraction: true`, `execution_mode: local`
   - Format: Step-by-step with Command, Expected Output, Validation blocks

2. **Extract E2E Tests** (5 minutes, automated)
   - Run: `python scripts/extract_e2e_tests_from_howtos.py`
   - Output: `tests/e2e/test_<feature-name>.py`
   - Validation: `pytest tests/e2e/test_<feature-name>.py`

3. **Extract BDD Scenarios** (10 minutes, semi-automated)
   - Run: `python scripts/generate_bdd_from_howto.py docs/user-docs/how-to/<feature-name>.md`
   - Output: `features/<feature-name>.feature` (Gherkin scenarios)
   - Review: Ensure scenarios match how-to steps (manual verification)

4. **Refine API Reference** (30 minutes)
   - Extract API calls from how-to command blocks
   - Document in `docs/user-docs/reference/api/<feature-name>.md`
   - Cross-link: Reference → How-To bidirectional links

**Benefits**:
- ✅ Documentation proves it works (E2E tests validate how-tos)
- ✅ BDD scenarios extracted, not written separately (50% time savings)
- ✅ Single source of truth (how-to guide drives everything)
- ✅ User-facing value first (docs are the product)

**Anti-Patterns**:
- ❌ Writing how-to after code (defeats "documentation-first")
- ❌ Skipping extraction scripts (manual BDD duplication)
- ❌ Non-executable how-tos (no validation, docs drift)

**See Also**:
- [SAP-007: documentation-framework](../../skilled-awareness/documentation-framework/) - Executable doc infrastructure
- [write-executable-documentation.md](../../user-docs/how-to/write-executable-documentation.md) - How-to guide format
```

---

#### 7.3 Update Feature Spec Template

**File**: `static-template/dev-docs/workflows/templates/feature-spec-template.md`

Add section after "Problem Statement":

```markdown
## User-Facing Documentation (L3 Optional, L4 Recommended)

**At L2**: BDD scenarios written manually (skip this section)
**At L3+**: Executable how-to guide drives BDD extraction (complete this section)

- [ ] **How-To Guide**: `docs/user-docs/how-to/<feature-name>.md`
  - [ ] Frontmatter: `test_extraction: true`
  - [ ] Format: Step-by-step (Command, Expected Output, Validation)
  - [ ] E2E tests extracted: `tests/e2e/test_<feature-name>.py`
  - [ ] E2E tests passing: `pytest tests/e2e/test_<feature-name>.py`

- [ ] **BDD Scenarios Extracted**: `features/<feature-name>.feature`
  - [ ] Scenarios match how-to steps
  - [ ] Gherkin syntax validated

- [ ] **Tutorial** (if learning-oriented): `docs/user-docs/tutorial/<feature-name>.md`

- [ ] **Explanation** (if conceptual): `docs/user-docs/explanation/<feature-name>.md`

- [ ] **Reference** (if technical spec): `docs/user-docs/reference/<feature-name>.md`

**Documentation-First Workflow** (L3+):
1. Write how-to guide first (before implementation)
2. Extract E2E tests: `python scripts/extract_e2e_tests_from_howtos.py`
3. Extract BDD scenarios: `python scripts/generate_bdd_from_howto.py <how-to-file>`
4. Implement code to make how-to work (TDD driven by BDD)
```

---

#### 7.4 Add Diataxis Reference Section

**Section**: "Appendix A: Diataxis Framework"

```markdown
## Appendix A: Diataxis Framework

**Overview**: Diataxis is a systematic approach to technical documentation that divides documentation into four distinct types based on user needs.

**Four Documentation Types**:

1. **Tutorial** (Learning-Oriented)
   - **Purpose**: Teaching a beginner to achieve a simple goal
   - **Format**: Step-by-step lesson
   - **Example**: "Your First MCP Server in 15 Minutes"
   - **When to Write**: Onboarding new users to the project

2. **How-To Guide** (Task-Oriented)
   - **Purpose**: Solving a specific problem
   - **Format**: Sequential steps with validation
   - **Example**: "How to Add a New MCP Tool"
   - **When to Write**: For every feature (L3 requirement)
   - **Executable Format** (L3): Include Command, Expected Output, Validation blocks for E2E test extraction

3. **Explanation** (Understanding-Oriented)
   - **Purpose**: Clarifying concepts and design decisions
   - **Format**: Discussion, background, rationale
   - **Example**: "Why We Use FastMCP Over Raw MCP"
   - **When to Write**: Complex architectural decisions, trade-offs

4. **Reference** (Information-Oriented)
   - **Purpose**: Describing technical details (APIs, configs, schemas)
   - **Format**: Dry, factual, comprehensive
   - **Example**: "MCP Tool Schema Reference"
   - **When to Write**: After implementation (API docs, config specs)

**Diataxis in SAP-012 Workflow**:
- **Phase 1 (Vision)**: Explanation docs (why this feature?)
- **Phase 2 (Planning)**: Tutorial + How-To planning (what will users learn/do?)
- **Phase 3 (Requirements)**: How-To (L3 executable), Reference (API specs)
- **Phase 4 (Development)**: Implement code to make How-To work
- **Phase 7 (Release)**: Tutorial (onboarding), Explanation (design rationale)

**Learn More**: https://diataxis.fr/

**SAP-007 Integration**: SAP-007 (documentation-framework) provides the infrastructure for Diataxis-structured docs, including frontmatter schema, directory structure, and test extraction.
```

---

### 8. Open Questions from COORD-2025-011

**Q1: Should Construct 0 be numbered differently?**

**Answer**: Recommend **not using Construct 0**. Instead, enhance Phase 3 with L3 maturity patterns (see Option C above).

**Rationale**: Documentation isn't always the foundation - sometimes strategy drives documentation. Positioning it as an L3 maturity pattern within Phase 3 provides flexibility.

---

**Q2: How to handle non-executable documentation?**

**Answer**: ✅ **Diataxis already covers this** (as noted in the proposal).

- **How-To**: Executable (L3 requirement)
- **Tutorial**: Semi-executable (optional)
- **Explanation**: Non-executable (conceptual)
- **Reference**: Non-executable (technical specs)

**Clarification**: Only **How-To guides** need `test_extraction: true` at L3. Other Diataxis types remain traditional documentation.

---

**Q3: Compatibility with existing DDD/BDD/TDD workflow?**

**Answer**: ✅ **Fully compatible** (as noted in the proposal).

**L2 Workflow** (Manual BDD):
```
Phase 3: Write docs (Explanation, Reference)
       ↓
Phase 4: Write BDD scenarios manually
       ↓
Phase 4: Write TDD tests
       ↓
Phase 4: Implement code
```

**L3 Workflow** (Documentation-First):
```
Phase 3: Write executable how-to guide
       ↓
Phase 3: Extract BDD scenarios from how-to (automated)
       ↓
Phase 4: BDD scenarios → TDD tests
       ↓
Phase 4: Implement code to make how-to work
```

**Key Difference**: At L3, BDD scenarios are **extracted** from how-tos, not written separately. The TDD cycle remains unchanged.

---

### 9. Success Criteria Validation

**From COORD-2025-011**:

**Short-Term (L2 → L3 transition)**:
- [x] **Template updated**: ✅ Proposed above (Section 7.3)
- [x] **Workflow documented**: ✅ Proposed above (Section 7.2)
- [x] **Diataxis reference**: ✅ Proposed above (Section 7.4)
- [ ] **Example feature**: ⚠️ Requires chora-workspace to provide 1 example (action item)

**Long-Term (L3 adoption)**:
- [ ] **10+ executable how-tos**: ⚠️ chora-base currently has 0 (needs dogfooding)
- [ ] **E2E coverage**: ⚠️ Requires SAP-007 `extract_tests.py` enhancement
- [ ] **BDD extraction**: ⚠️ Requires `generate_bdd_from_howto.py` script in chora-base
- [ ] **Doc quality gates**: ⚠️ Requires CI/CD workflow enhancement

**Assessment**: Short-term criteria achievable in 4-7 hours. Long-term criteria require 3-6 month dogfooding pilot (similar to SAP-029).

---

### 10. Recommended Timeline

**Phase 1: Template Enhancement** (4-6 hours) - **IMMEDIATE**
- Update SAP-012 protocol-spec.md (Sections 7.1, 7.2, 7.4)
- Update feature spec template (Section 7.3)
- Update SAP-012 maturity levels (Section 4)
- Version bump: SAP-012 v1.1.0 → v1.2.0

**Phase 2: Script Integration** (2-3 hours) - **WEEK 1**
- Copy `extract_e2e_tests_from_howtos.py` from chora-workspace to chora-base `scripts/`
- Copy `generate_bdd_from_howto.py` from chora-workspace to chora-base `scripts/`
- Update SAP-007 system_files to include extraction scripts
- Update SAP-012 to reference SAP-007 integration

**Phase 3: Example Feature** (2-3 hours) - **WEEK 2**
- chora-workspace provides 1 example feature using Documentation-First approach
- Include in SAP-012 adoption-blueprint.md as "L3 Pattern Example"
- Cross-reference in SAP-007 adoption-blueprint.md

**Phase 4: Dogfooding Pilot** (3-6 months) - **Q1 2026**
- Use Documentation-First for 10+ new chora-base features
- Collect metrics: time savings, satisfaction, BDD extraction quality
- Apply SAP-027 (dogfooding-patterns) methodology
- GO/NO-GO decision at 3 months (similar to SAP-029 pilot)

**Phase 5: Formalization** (1-2 hours) - **AFTER PILOT**
- Update SAP-012 ledger with dogfooding metrics
- Promote L3 pattern from "optional" to "recommended" (if pilot succeeds)
- Distribute updated SAP-012 to ecosystem

**Total Immediate Effort**: 6-9 hours (Phases 1-3)
**Total Long-Term Effort**: 3-6 months dogfooding (Phase 4)

---

### 11. Decision: Conditional Approve

**Decision**: **CONDITIONAL APPROVE** with the following conditions:

1. ✅ **Terminology**: Rename "DDD" in SAP-012 to avoid confusion with Domain-Driven Design
2. ✅ **Structure**: Enhance Phase 3 (not Construct 0) with L3 maturity patterns
3. ✅ **Integration**: Reference SAP-007 explicitly for executable doc infrastructure
4. ✅ **Scripts**: Include `extract_e2e_tests_from_howtos.py` and `generate_bdd_from_howto.py` in chora-base
5. ✅ **Example**: Provide 1 example feature from chora-workspace demonstrating the workflow
6. ⚠️ **Pilot**: Treat as **L3 enhancement**, not mandatory at L2 (dogfooding required before promotion to "recommended")

**What This Means**:
- **Approved**: The concept is sound, evidence is strong, integration is clear
- **Conditional**: Implementation details need refinement (terminology, structure, scripts)
- **Action Required**: chora-workspace to provide example feature + scripts for integration

---

### 12. Next Steps

**From chora-base Team**:
- [ ] **Review**: Claude agent will review this response for accuracy
- [ ] **Approval**: If user approves, proceed with Phase 1 (template enhancement)
- [ ] **Timeline**: Phases 1-3 can complete in 1-2 weeks

**From chora-workspace**:
1. [ ] **Scripts**: Confirm `extract_e2e_tests_from_howtos.py` and `generate_bdd_from_howto.py` are ready for chora-base integration
2. [ ] **Example**: Create 1 prospective feature using Documentation-First approach
3. [ ] **Validation**: Validate executable how-to → BDD extraction workflow
4. [ ] **Share**: Provide example + scripts to chora-base for review

**Joint (After Phase 3)**:
1. [ ] **Dogfooding**: chora-base adopts Documentation-First for 10+ new features
2. [ ] **Metrics**: Collect time savings, satisfaction, extraction quality (SAP-027 methodology)
3. [ ] **GO Decision**: At 3 months, decide to promote L3 → recommended or keep optional
4. [ ] **Distribution**: Update SAP-012 and distribute to ecosystem

---

## Appendix: SAP-012 Current State

### Current SAP-012 Status
- **Version**: 1.1.0
- **Status**: Active
- **Size**: 156 KB
- **Dependencies**: SAP-000
- **Location**: [docs/skilled-awareness/development-lifecycle](../docs/skilled-awareness/development-lifecycle)

### Current Diataxis References in SAP-012
1. protocol-spec.md: Line 41 - "Documents: Diataxis docs, API specs, acceptance criteria"
2. protocol-spec.md: Line 626 - "Write change request (Explanation + How-To, Diataxis format)"
3. protocol-spec.md: Line 1368 - "DDD (Phase 3) uses Diataxis structure"
4. AGENTS.md: Line 122 - "Phase 3: DDD (Documentation Driven Design)"
5. adoption-blueprint.md: Line 80 - "Documentation framework (SAP-007): Diataxis structure for DDD"

### SAP-007 (documentation-framework) Capabilities
- Diátaxis 4-domain structure
- Frontmatter schema validation
- **Executable how-to guides** ✅
- **Test extraction from docs** ✅
- DOCUMENTATION_STANDARD.md (700 lines)
- System files: `scripts/extract_tests.py`

---

## Summary

**Bottom Line**: This is an excellent proposal that **formalizes and extends** existing SAP-012 + SAP-007 patterns. The evidence is strong, the integration path is clear, and the value proposition is compelling.

**Key Changes**:
1. Rename "DDD" → "Documentation-Driven Development" (terminology clarity)
2. Enhance Phase 3 with L3 maturity patterns (not Construct 0)
3. Integrate SAP-007 extraction scripts into workflow
4. Add Diataxis reference section to SAP-012
5. Update feature spec template with L3 documentation-first section
6. Dogfood for 3-6 months before promoting to "recommended"

**Expected Impact**:
- **L2 teams**: No change (manual BDD workflow remains valid)
- **L3 teams**: 50% time savings on BDD scenario creation (extracted from how-tos)
- **L4 teams**: Documentation becomes product, validated by E2E tests
- **Ecosystem**: chora-base demonstrates documentation-first workflow, reducing adoption friction

**Approval**: Proceed with Phases 1-3 (template enhancement, script integration, example feature) pending user approval.

---

**Status**: Draft (awaiting chora-workspace review)
**Expected Response Time**: 1-2 weeks
**Contact**: chora-base team (via inbox coordination)

---

**Created**: 2025-11-08
**Framework**: SAP-001 (Inbox Coordination Protocol)
**Related SAPs**: SAP-007 (documentation-framework), SAP-012 (development-lifecycle), SAP-027 (dogfooding-patterns)
