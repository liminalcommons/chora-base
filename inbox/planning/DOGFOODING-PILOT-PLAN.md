# Dogfooding Pilot Plan: SAP Generation Automation

**Plan ID**: PILOT-2025-SAP-027
**Created**: 2025-11-02
**Status**: Planning (Week 1 detailed, ready to start)
**Timeline**: Q1 2026 (8 weeks)
**Owner**: chora-base team

---

## Executive Summary

**Objective**: Automate SAP artifact generation to achieve ≥5x time savings (10 hours → 2 hours per SAP)

**Pattern**: Minimal Viable Dogfooding (MVD) from chora-compose
- Data file (sap-catalog.json extended)
- Templates (5 Jinja2 templates for SAP artifacts)
- Generator (scripts/generate-sap.py)

**Success Criteria**:
- ≥5x time savings
- ≥85% developer satisfaction
- Zero critical bugs
- 2+ real SAPs generated

**If Successful**: Formalize as SAP-027 (dogfooding-patterns) in Q1 2026

---

## Context: Publishing Automation Maturity

**SAP-028 Status**: Level 2 (75% complete, production-ready)

| Component | Status | Gap to 100% |
|-----------|--------|-------------|
| Documentation | ✅ 5/5 artifacts (3,120 lines) | None |
| Testing | ✅ All 3 methods validated | None |
| Ecosystem Adoption | ✅ 1/1 repos (chora-compose) | None |
| Template Integration | ⏳ Variable not configured | 2-3 hours (Q1 2026) |

**Note**: chora-base is a template repository (not a PyPI package), so it doesn't publish to PyPI itself.

**Gap to Level 3**: Add `pypi_auth_method` variable to copier configuration (~2-3 hours)

---

## Current SAP Creation Workflow (Manual)

**Process**:
1. Create directory: `docs/skilled-awareness/{sap-name}/`
2. Write 5 artifacts manually:
   - `capability-charter.md` (~300-400 lines)
   - `protocol-spec.md` (~600-800 lines)
   - `awareness-guide.md` (~500-700 lines)
   - `adoption-blueprint.md` (~700-900 lines)
   - `ledger.md` (~350-450 lines)
3. Update `sap-catalog.json` with metadata entry
4. Update `docs/skilled-awareness/INDEX.md` with new SAP
5. Cross-reference with other SAPs (manual linking)
6. Validate with `scripts/validate-links.sh`

**Time Estimate**: 8-12 hours per SAP (average: 10 hours)

**Pain Points**:
- Frontmatter duplication (SAP ID, version, status, dates repeated 5 times)
- Section structure duplication (each artifact has 5-12 standard sections)
- Cross-reference management (charter → protocol → awareness → adoption → ledger)
- Catalog/index updates (manual JSON editing)
- Consistency errors (typos in SAP ID, version mismatches)

**Scale**: 28 SAPs × 5 artifacts = 140 files with overlapping structure

---

## Pilot Scope: Minimal Viable Dogfooding (MVD)

### Component 1: Data Layer
**Goal**: Extend sap-catalog.json with generation-specific fields

**Deliverables**:
- Enhanced catalog schema with template data fields
- Common content blocks (problem templates, success criteria patterns)
- Reusable section structures extracted from existing SAPs

**Effort**: 2 hours

### Component 2: Template Layer
**Goal**: Create 5 Jinja2 templates for SAP artifacts

**Deliverables**:
- `templates/sap/capability-charter.j2`
- `templates/sap/protocol-spec.j2`
- `templates/sap/awareness-guide.j2`
- `templates/sap/adoption-blueprint.j2`
- `templates/sap/ledger.j2`

**Effort**: 3-4 hours

### Component 3: Generator Script
**Goal**: Build Python script to render templates from catalog data

**Deliverables**:
- `scripts/generate-sap.py`
- Integration with sap-catalog.json
- Automatic INDEX.md updates
- Validation integration (sap-evaluator.py)

**Effort**: 2-3 hours

### Component 4: Integration
**Goal**: Make generation accessible via justfile

**Deliverables**:
- `just generate-sap SAP-029` command
- `just validate-sap SAP-029` command

**Effort**: 30 minutes

**Total Implementation**: 7.5-9.5 hours (one-time investment)

---

## 8-Week Pilot Timeline

### Week 1: Research & Design (2 hours)
**Goal**: Extract common patterns and design data schema

**Deliverables**:
- Pattern extraction report from 3-5 SAPs
- Data schema design for generation fields
- Template structure requirements document

**Status**: DETAILED PLAN BELOW

### Week 2: Template Creation (3-4 hours)
**Goal**: Create 5 Jinja2 templates

**Tasks**:
- Day 1-2: Create capability-charter.j2 and protocol-spec.j2
- Day 3-4: Create awareness-guide.j2 and adoption-blueprint.j2
- Day 5: Create ledger.j2
- Day 6: Test rendering with SAP-028 metadata (dry run)

**Deliverables**: 5 working Jinja2 templates

### Week 3: Generator Implementation (2.5-3.5 hours)
**Goal**: Build generation script and integration

**Tasks**:
- Day 1-2: Build generate-sap.py core logic
- Day 3: Add catalog/index update logic
- Day 4: Add validation integration
- Day 5: Create justfile commands
- Day 6-7: Test with mock SAP data

**Deliverables**: Working `just generate-sap` command

### Week 4: Pilot Testing (2-4 hours)
**Goal**: Generate 1-2 real SAPs and validate

**Tasks**:
- Day 1-2: Generate first real SAP (e.g., SAP-029 or Wave 5 SAP)
- Day 3: Validate with sap-evaluator.py
- Day 4-5: Generate second SAP
- Day 6-7: Fix any template bugs, refinement

**Deliverables**: 2 production-quality generated SAPs

### Weeks 5-8: Validation Period (ongoing)
**Goal**: Measure success criteria in production

**Activities**:
- Use generator for all new SAP creations (Wave 5-6 SAPs)
- Track time savings per SAP (spreadsheet)
- Survey developer satisfaction after each SAP
- Monitor validation pass rates
- Document edge cases and improvements

**Metrics Tracking**:
| SAP | Manual Est. | Actual Time | Time Saved | Validation | Satisfaction |
|-----|-------------|-------------|------------|------------|--------------|
| SAP-029 | 10h | TBD | TBD | TBD | TBD |
| SAP-030 | 10h | TBD | TBD | TBD | TBD |

**Success Threshold**: ≥5x savings, ≥85% satisfaction, zero critical bugs

### End of Week 8: Go/No-Go Decision

**IF SUCCESS** (all criteria met):
- Formalize as SAP-027 (dogfooding-patterns)
- Effort: 9-13 hours for full SAP (5 artifacts)
- Timeline: End of Q1 2026
- Phase: Wave 7 (Ecosystem Coordination)
- Share with ecosystem via SAP-001 inbox

**IF FAILURE** (criteria not met):
- Document lessons learned
- Analyze why chora-base differs from chora-compose (their 9x success)
- Archive templates/scripts for future reference
- Re-evaluate when SAP count > 30 or pain point increases

---

## Week 1 Detailed Plan: Research & Design (2 hours)

### Overview

**Duration**: 2 hours
**Objective**: Extract common patterns from existing SAPs and design generation data schema
**Output**: 3 documents ready for Week 2 template creation

### Task 1.1: Select Reference SAPs (15 minutes)

**Goal**: Choose 3-5 SAPs representing diverse patterns

**Selection Criteria**:
- Mix of phases (Phase 1-4, Wave 2-4)
- Mix of statuses (Draft, Pilot, Active)
- Mix of complexity (simple vs. complex)
- Mix of sizes (small vs. large artifacts)

**Recommended SAPs**:
1. **SAP-028 (publishing-automation)** - Just completed, fresh in mind, Active status
2. **SAP-000 (sap-framework)** - Foundational, defines SAP structure itself
3. **SAP-020 (react-foundation)** - Wave 4, Active, technology-specific
4. **SAP-001 (inbox-coordination)** - Pilot status, coordination-focused
5. **SAP-019 (sap-self-evaluation)** - Meta-SAP (evaluates other SAPs)

**Action Items**:
- [ ] Read all 5 SAPs (capability-charter.md only, quick skim)
- [ ] Identify which represents "typical" structure best
- [ ] Note any outliers or unique patterns

**Output**: List of 3-5 reference SAPs with rationale

---

### Task 1.2: Extract Common Artifact Structures (45 minutes)

**Goal**: Document section-by-section structure for each of the 5 artifacts

#### Subtask 1.2.1: Capability Charter Pattern (10 minutes)

**Action**: Read capability-charter.md from 3 SAPs, extract common structure

**Analysis**:
```markdown
# Common Structure (capability-charter.md)

## Frontmatter (100% common)
- Title: "Capability Charter: {full_name}"
- SAP ID: {id}
- Version: {version}
- Status: {status}
- Owner: {owner}
- Created: {created_date}
- Last Updated: {updated_date}

## Section 1: Problem Statement (100% common)
- Current Challenge (2-3 paragraphs)
- Evidence (bullet list or table)
- Business Impact (1-2 paragraphs)

## Section 2: Proposed Solution (100% common)
- Solution overview (2-3 paragraphs)
- Key Principles (bullet list)

## Section 3: Scope (100% common)
- In Scope (bullet list)
- Out of Scope (bullet list)

## Section 4: Success Criteria (100% common)
- Adoption Success (Level 1/2/3 targets)
- Performance Metrics (if applicable)
- Value Delivered (measurable outcomes)

## Section 5: Dependencies (100% common)
- List of SAP dependencies with rationale

## Section 6: Risks & Mitigations (90% common)
- Table or list of risks with mitigation strategies

## Section 7: Timeline & Milestones (80% common)
- Phase-based or quarter-based timeline
- Key milestones
```

**Output**: capability-charter-structure.md with annotated structure

#### Subtask 1.2.2: Protocol Spec Pattern (10 minutes)

**Action**: Read protocol-spec.md from 3 SAPs, extract common structure

**Analysis**:
```markdown
# Common Structure (protocol-spec.md)

## Frontmatter (100% common)
- Title: "Protocol Specification: {full_name}"
- SAP ID: {id}
- Version: {version}
- Status: {status}
- Last Updated: {updated_date}

## Section 1: Overview (100% common)
- High-level description (2-3 paragraphs)
- Key capabilities (bullet list)

## Section 2: Core Contracts (90% common)
- Main protocol contracts
- Interfaces, APIs, data structures

## Section 3: {Domain-Specific} (varies)
- Publishing: Methods (Trusted/Token/Manual)
- Testing: Framework configuration
- React: Component patterns
[VARIABLE SECTION]

## Section 4: Integration Patterns (80% common)
- How to integrate with other SAPs
- Common use cases

## Section 5: Error Handling (70% common)
- Error codes, messages, recovery

## Section 6: Security Considerations (60% common)
- Security model (if applicable)

## Section 7: Performance Requirements (50% common)
- Benchmarks, thresholds (if applicable)

## Section 8: Examples (90% common)
- Code examples, configuration samples
- Walkthroughs

## Section 9: Related SAPs (100% common)
- Links to dependencies and related SAPs
```

**Output**: protocol-spec-structure.md with annotated structure

#### Subtask 1.2.3: Awareness Guide Pattern (8 minutes)

**Action**: Read awareness-guide.md from 3 SAPs

**Analysis**:
```markdown
# Common Structure (awareness-guide.md)

## Frontmatter (100% common)
- Title: "Awareness Guide: {full_name}"
- SAP ID: {id}
- Version: {version}
- For: AI Agents, LLM-Based Assistants
- Last Updated: {updated_date}

## Section 1: Quick Start for AI Agents (100% common)
- One-sentence summary
- When to use this SAP (checklist)
- When NOT to use this SAP (checklist)

## Section 2: Core Concepts for Agents (90% common)
- Decision trees or flowcharts
- Key terminology
- Quick reference tables

## Section 3: Common Agent Workflows (90% common)
- Workflow 1: {most common task}
- Workflow 2: {second most common}
- Workflow 3: {third most common}
- Each workflow: Context → Action → Validation

## Section 4: Quick Reference (100% common)
- Commands, file paths, validation steps
- Error patterns and solutions

## Section 5: Integration Points (80% common)
- How this SAP relates to other SAPs
- When to use together vs. separately

## Section 6: Edge Cases & Gotchas (70% common)
- Common mistakes
- Anti-patterns
- Troubleshooting tips
```

**Output**: awareness-guide-structure.md with annotated structure

#### Subtask 1.2.4: Adoption Blueprint Pattern (10 minutes)

**Action**: Read adoption-blueprint.md from 3 SAPs

**Analysis**:
```markdown
# Common Structure (adoption-blueprint.md)

## Frontmatter (100% common)
- Title: "Adoption Blueprint: {full_name}"
- SAP ID: {id}
- Version: {version}
- Last Updated: {updated_date}

## Overview (100% common)
- Adoption levels table (Level 1/2/3 comparison)

## Level 1: Basic Adoption (100% common structure)
### Prerequisites
- Software requirements (bullet list)
- Knowledge requirements (bullet list)

### Step-by-Step Instructions
- Numbered steps with code blocks
- Screenshots or diagrams (optional)

### Validation
- How to verify successful adoption
- Test commands
- Expected output

### Time Estimate
- Setup time, maintenance burden

## Level 2: Advanced Adoption (100% common structure)
[Same subsections as Level 1]

## Level 3: Mastery (100% common structure)
[Same subsections as Level 1]

## Troubleshooting Guide (90% common)
- Common errors table
- Solutions and workarounds

## Migration Paths (70% common)
- From Level 1 → Level 2
- From Level 2 → Level 3
- From other tools → This SAP

## Additional Resources (100% common)
- Links to related docs
- External references
```

**Output**: adoption-blueprint-structure.md with annotated structure

#### Subtask 1.2.5: Ledger Pattern (7 minutes)

**Action**: Read ledger.md from 3 SAPs

**Analysis**:
```markdown
# Common Structure (ledger.md)

## Frontmatter (100% common)
- Title: "Traceability Ledger: {full_name}"
- SAP ID: {id}
- Current Version: {version}
- Status: {status}
- Last Updated: {updated_date}

## Section 1: Version History (100% common)
- v{version} ({date}) - {release_type}
  - Status: {status}
  - Summary: {summary}
  - Key Features: {bullet_list}
  - Rationale: {explanation}
  - Dependencies: {list}

## Section 2: Adoption Tracking (80% common)
- Table of projects/teams adopting
- Adoption level per project

## Section 3: Integration Points (90% common)
- SAP integrations table
- External system integrations table

## Section 4: Performance Metrics (60% common)
- Benchmarks (if applicable)
- Time savings, efficiency gains

## Section 5: Security Events (50% common)
- Incident log (if applicable)
- Token rotation tracking (security-focused SAPs)

## Section 6: Changes Since Last Version (100% common)
- New features
- Modified features
- Deprecated features
- Removed features
- Migration required (yes/no)

## Section 7: Testing & Validation (80% common)
- Manual testing results table
- Workflow validation table

## Section 8: Known Issues & Limitations (90% common)
- Current limitations (numbered list)
- Workarounds
- Planned fixes

## Section 9: Documentation Links (100% common)
- Links to other 4 artifacts
- Links to related SAPs
- External resources

## Section 10: Future Enhancements (80% common)
- Planned features by version
- Effort estimates
- Priority rankings

## Section 11: Stakeholder Feedback (70% common)
- Feedback log with entries
- Actions taken

## Section 12: Revision History (100% common)
- Table: Version | Date | Author | Changes

## Section 13: Appendix (60% common)
- SAP metadata (JSON snippet)
- Artifact completeness table
```

**Output**: ledger-structure.md with annotated structure

---

### Task 1.3: Identify Variability Points (30 minutes)

**Goal**: Determine which content is fixed vs. variable vs. optional

#### Subtask 1.3.1: Categorize Content Types (15 minutes)

**Action**: Review structures from Task 1.2, categorize each section

**Categories**:
1. **Fixed** (100% identical across all SAPs): Templates, section headers
2. **Variable** (filled from catalog data): SAP ID, version, status, dates
3. **Semi-structured** (pattern exists, content varies): Problem statements, solutions
4. **Free-form** (minimal structure): Domain-specific content
5. **Optional** (present in some SAPs, absent in others): Security events, performance metrics

**Analysis Matrix**:

| Artifact | Section | Category | Source | Notes |
|----------|---------|----------|--------|-------|
| Charter | Frontmatter | Variable | sap-catalog.json | id, version, status, dates |
| Charter | Problem Statement | Semi-structured | User input + templates | Common problem patterns extractable |
| Charter | Proposed Solution | Semi-structured | User input + templates | Key principles often similar |
| Charter | Scope | Semi-structured | User input | In/Out scope structure fixed |
| Charter | Success Criteria | Semi-structured | User input + templates | Level 1/2/3 structure fixed |
| Charter | Dependencies | Variable | sap-catalog.json | dependencies array |
| Charter | Risks | Free-form | User input | Can provide template table |
| Charter | Timeline | Semi-structured | User input + phase | Phase/Wave structure extractable |
| Protocol | Frontmatter | Variable | sap-catalog.json | id, version, status, dates |
| Protocol | Overview | Semi-structured | User input + description | Description from catalog |
| Protocol | Core Contracts | Free-form | User input | Domain-specific |
| Protocol | Examples | Free-form | User input | Code blocks, configs |
| Protocol | Related SAPs | Variable | sap-catalog.json | dependencies array |
| Awareness | Frontmatter | Variable | sap-catalog.json | id, version, dates |
| Awareness | Quick Start | Semi-structured | User input + description | One-sentence summary from catalog |
| Awareness | Workflows | Free-form | User input | 3-5 common workflows |
| Awareness | Quick Reference | Semi-structured | User input | Commands, paths (predictable structure) |
| Adoption | Frontmatter | Variable | sap-catalog.json | id, version, dates |
| Adoption | Level 1/2/3 | Semi-structured | User input + templates | Structure 100% fixed, steps vary |
| Adoption | Troubleshooting | Free-form | User input | Error table template |
| Ledger | Frontmatter | Variable | sap-catalog.json | id, version, status, dates |
| Ledger | Version History | Variable | User input + catalog | Initial release metadata |
| Ledger | All 12 sections | Semi-structured | Mix | Tables/lists structure fixed |

**Output**: variability-analysis.md with categorization

#### Subtask 1.3.2: Design Template Strategy (15 minutes)

**Goal**: Decide how to handle each category in templates

**Strategy**:

**Fixed Content** → Hard-code in templates
```jinja2
## 1. Problem Statement

### Current Challenge

{{ problem_statement }}
```

**Variable Content** → Direct substitution from catalog
```jinja2
**SAP ID**: {{ id }}
**Version**: {{ version }}
**Status**: {{ status }}
```

**Semi-structured Content** → Template + user input
```jinja2
## 3. Scope

### In Scope

{% for item in in_scope %}
- {{ item }}
{% endfor %}

### Out of Scope

{% for item in out_of_scope %}
- {{ item }}
{% endfor %}
```

**Free-form Content** → Placeholder + comment
```jinja2
## 2. Core Contracts

<!-- Domain-specific content - describe main contracts here -->

{{ core_contracts | default("TODO: Define core contracts for this SAP") }}
```

**Optional Content** → Conditional blocks
```jinja2
{% if has_security_considerations %}
## 6. Security Considerations

{{ security_considerations }}
{% endif %}
```

**Output**: template-strategy.md with approach for each category

---

### Task 1.4: Design Data Schema (30 minutes)

**Goal**: Extend sap-catalog.json schema with generation fields

#### Subtask 1.4.1: Review Current Catalog Schema (5 minutes)

**Action**: Read sap-catalog.json, document current schema

**Current Schema** (per SAP entry):
```json
{
  "id": "SAP-028",
  "name": "publishing-automation",
  "full_name": "Publishing Automation",
  "version": "1.0.0",
  "status": "active",
  "size_kb": 125,
  "description": "Secure PyPI publishing with OIDC...",
  "capabilities": [...],
  "dependencies": ["SAP-003", "SAP-005"],
  "tags": ["security", "publishing", "ci-cd"],
  "author": "chora-base",
  "location": "docs/skilled-awareness/publishing-automation",
  "artifacts": {
    "capability_charter": true,
    "protocol_spec": true,
    "awareness_guide": true,
    "adoption_blueprint": true,
    "ledger": true
  },
  "phase": "Immediate",
  "priority": "P0"
}
```

**Output**: current-schema.md

#### Subtask 1.4.2: Design Generation Fields (20 minutes)

**Goal**: Add fields needed for artifact generation

**Proposed Extended Schema**:
```json
{
  // --- Existing fields (unchanged) ---
  "id": "SAP-029",
  "name": "example-sap",
  "full_name": "Example SAP",
  "version": "1.0.0",
  "status": "draft",
  "description": "...",
  "capabilities": [...],
  "dependencies": [...],
  "tags": [...],
  "author": "...",
  "location": "...",
  "artifacts": {...},
  "phase": "...",
  "priority": "...",

  // --- NEW: Generation fields ---
  "generation": {
    // Charter fields
    "problem_statement": "Current challenge description...",
    "evidence": ["Evidence point 1", "Evidence point 2"],
    "business_impact": "Impact description...",
    "solution_overview": "Proposed solution overview...",
    "key_principles": ["Principle 1", "Principle 2"],
    "in_scope": ["Item 1", "Item 2"],
    "out_of_scope": ["Item 1", "Item 2"],
    "success_criteria_level_1": "Basic adoption success metric",
    "success_criteria_level_2": "Advanced adoption success metric",
    "success_criteria_level_3": "Mastery success metric",
    "risks": [
      {"risk": "Risk description", "mitigation": "Mitigation strategy"}
    ],

    // Protocol fields
    "core_contracts": "Main protocol contracts description...",
    "integration_patterns": "How to integrate...",
    "examples": [
      {"title": "Example 1", "code": "...", "language": "python"}
    ],

    // Awareness fields
    "one_sentence_summary": "SAP-029 defines...",
    "when_to_use": ["Use case 1", "Use case 2"],
    "when_not_to_use": ["Non-use case 1"],
    "agent_workflows": [
      {
        "name": "Workflow 1",
        "context": "When to use this workflow",
        "action": "Steps to take",
        "validation": "How to verify"
      }
    ],

    // Adoption fields
    "prerequisites_level_1": ["Prereq 1", "Prereq 2"],
    "steps_level_1": ["Step 1", "Step 2"],
    "validation_level_1": "How to validate Level 1",
    "time_estimate_level_1": "1-2 hours",
    // (repeat for level_2, level_3)

    // Ledger fields
    "initial_release_summary": "First formalization of...",
    "initial_release_rationale": "Why this SAP was created...",
    "adoption_targets": ["Target 1", "Target 2"]
  }
}
```

**Simplification Strategy**: Start with MINIMAL schema for MVP
- Only frontmatter fields (variable substitution)
- Only high-level descriptions (problem, solution, summary)
- All detailed content = placeholders (user fills manually)

**MVP Schema** (Pilot Version):
```json
{
  // Existing fields (unchanged)
  "id": "SAP-029",
  "name": "example-sap",
  "full_name": "Example SAP",
  "version": "1.0.0",
  "status": "draft",
  "description": "...",
  "capabilities": [...],
  "dependencies": [...],
  "tags": [...],
  "author": "chora-base",
  "location": "docs/skilled-awareness/example-sap",
  "phase": "Wave 5",
  "priority": "P1",

  // NEW: Minimal generation fields for MVP
  "generation": {
    "owner": "Victor",
    "created_date": "2025-11-10",
    "one_sentence_summary": "SAP-029 defines...",
    "problem_statement": "Current challenge...",
    "solution_overview": "Proposed solution..."
  }
}
```

**Rationale**: 80/20 rule
- 80% of time savings comes from frontmatter + structure
- 20% comes from content pre-fill
- Start with structure automation, add content automation later

**Output**: extended-schema.md with MVP and full schemas

#### Subtask 1.4.3: Document Generation Workflow (5 minutes)

**Goal**: Define how generator will use catalog data

**Workflow**:
```
1. User updates sap-catalog.json with new SAP entry
   - Fills `id`, `name`, `full_name`, `description`
   - Fills minimal `generation` fields

2. User runs: just generate-sap SAP-029

3. Generator reads sap-catalog.json, finds SAP-029 entry

4. Generator renders 5 templates with catalog data
   - capability-charter.j2 → capability-charter.md
   - protocol-spec.j2 → protocol-spec.md
   - awareness-guide.j2 → awareness-guide.md
   - adoption-blueprint.j2 → adoption-blueprint.md
   - ledger.j2 → ledger.md

5. Generator writes files to docs/skilled-awareness/example-sap/

6. Generator updates INDEX.md with new SAP entry

7. User manually fills TODO placeholders in 5 artifacts

8. User runs: just validate-sap SAP-029

9. User iterates until validation passes
```

**Output**: generation-workflow.md

---

### Task 1.5: Document Findings & Prepare for Week 2 (10 minutes)

**Goal**: Consolidate all Week 1 outputs into actionable plan for Week 2

#### Deliverable 1: Pattern Extraction Report

**File**: `docs/project-docs/dogfooding-pilot/week-1-pattern-extraction.md`

**Contents**:
- Reference SAPs selected (3-5 SAPs)
- 5 artifact structure documents (charter, protocol, awareness, adoption, ledger)
- Variability analysis (fixed/variable/semi-structured/free-form/optional)
- Template strategy (how to handle each category)

#### Deliverable 2: Data Schema Design

**File**: `docs/project-docs/dogfooding-pilot/week-1-schema-design.md`

**Contents**:
- Current sap-catalog.json schema
- MVP extended schema (minimal fields)
- Full extended schema (future enhancement)
- Generation workflow diagram

#### Deliverable 3: Week 2 Template Creation Plan

**File**: `docs/project-docs/dogfooding-pilot/week-2-plan.md`

**Contents**:
- Template creation priority order (which template first)
- Estimated effort per template
- Testing strategy (how to validate templates)
- Day-by-day breakdown

**Output**: 3 planning documents ready for Week 2 execution

---

## Week 1 Output Summary

**Time Spent**: 2 hours (120 minutes)

**Deliverables**:
1. ✅ Reference SAPs selected (3-5 SAPs)
2. ✅ 5 artifact structure documents
3. ✅ Variability analysis
4. ✅ Template strategy
5. ✅ Extended schema design (MVP + full)
6. ✅ Generation workflow
7. ✅ Week 2 plan prepared

**Readiness for Week 2**: ✅ READY
- Templates can be created from structure documents
- Schema is defined for catalog extensions
- Strategy is clear (fixed/variable/placeholder approach)

---

## Success Metrics for Pilot

### Primary Metrics (from COORD-2025-009)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Time Savings** | ≥5x (10h → ≤2h) | Track actual SAP creation time per SAP |
| **Developer Satisfaction** | ≥85% | Post-SAP survey (1-5 scale) |
| **Quality** | Zero critical bugs | sap-evaluator.py validation pass rate |
| **Adoption** | 2+ real SAPs | Count of production SAPs generated |

### Secondary Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| **Setup ROI** | Break-even by 2nd SAP | Validate one-time investment worth it |
| **Template Coverage** | 80% structure automated | Measure automation completeness |
| **Manual Effort Remaining** | ≤20% per SAP | Measure remaining manual work |
| **Validation Pass Rate** | 100% on first try | Measure template quality |

### Tracking Spreadsheet

**File**: `docs/project-docs/dogfooding-pilot/metrics-tracking.csv`

```csv
SAP_ID,Manual_Estimate_Hours,Actual_Hours,Time_Saved_Hours,Validation_Passes,Satisfaction_Score,Notes
SAP-029,10,TBD,TBD,TBD,TBD,First pilot SAP
SAP-030,10,TBD,TBD,TBD,TBD,Second pilot SAP
```

---

## ROI Analysis

### Break-Even Analysis

**One-Time Investment**: 7.5-9.5 hours (setup)

**Per-SAP Savings**: 8 hours (10h manual → 2h generated)

**Break-Even Point**:
- Savings needed: 9.5 hours
- SAPs needed: 9.5h ÷ 8h = 1.2 SAPs
- **Break-even after 2nd SAP**

### Long-Term ROI

**After 5 SAPs** (typical Wave):
- Manual effort: 5 × 10h = 50 hours
- Generated effort: 9.5h (setup) + 5 × 2h = 19.5 hours
- **Net savings: 30.5 hours (61% reduction)**

**After 10 SAPs** (multiple Waves):
- Manual effort: 10 × 10h = 100 hours
- Generated effort: 9.5h (setup) + 10 × 2h = 29.5 hours
- **Net savings: 70.5 hours (70% reduction)**

**After 20 SAPs** (long-term):
- Manual effort: 20 × 10h = 200 hours
- Generated effort: 9.5h (setup) + 20 × 2h = 49.5 hours
- **Net savings: 150.5 hours (75% reduction)**

### Comparison to chora-compose

**chora-compose results**:
- Use case: 6 React templates
- Efficiency gain: 9x
- Production stability: 6 months
- Status: "Can't imagine going back to manual"

**chora-base projection**:
- Use case: 28+ SAPs (growing)
- Expected efficiency gain: 5-10x (target: 5x minimum)
- If successful: Formalize as SAP-027, share with ecosystem

---

## Risks & Mitigations

### Risk 1: Templates too rigid, don't capture SAP diversity

**Probability**: Medium
**Impact**: High (defeats purpose of automation)

**Mitigation**:
- Start with 80/20 approach (structure only)
- Leave content placeholders for manual fill
- Iterate templates based on 2-3 SAPs before committing

**Fallback**: Use templates for structure only, manual content

---

### Risk 2: Setup time exceeds benefits for small SAP count

**Probability**: Low
**Impact**: Medium (wasted 10 hours)

**Mitigation**:
- Break-even analysis shows ROI after 2nd SAP
- chora-base has 28 SAPs (proven scale)
- Wave 5-7 will add 10+ more SAPs

**Fallback**: Archive for future use when SAP count grows

---

### Risk 3: Maintenance burden if SAP structure changes

**Probability**: Low
**Impact**: Medium (need to update 5 templates)

**Mitigation**:
- SAP structure stable since v4.0.0 (SAP-000)
- Templates co-located with SAP-000 (versioned together)
- Changes to SAP structure = update templates + bump version

**Fallback**: Manual updates, same as current workflow

---

### Risk 4: Generated artifacts lack quality/polish

**Probability**: Medium
**Impact**: High (hurts SAP credibility)

**Mitigation**:
- Validate with sap-evaluator.py (automated quality check)
- Manual review before publishing (same as current)
- Pilot testing with 2 SAPs before wide adoption

**Fallback**: Use for drafts only, manual polish before release

---

## Go/No-Go Criteria (End of Week 8)

### GO Criteria (All must be met)

1. ✅ **Time Savings**: ≥5x efficiency gain (≥2 SAPs measured)
2. ✅ **Satisfaction**: ≥85% developer satisfaction (survey)
3. ✅ **Quality**: Zero critical bugs (validation passes)
4. ✅ **Adoption**: 2+ real SAPs generated successfully

**Action if GO**: Formalize as SAP-027 (9-13 hours), end of Q1 2026

### NO-GO Criteria (Any one triggers)

1. ❌ **Time Savings**: <3x efficiency gain
2. ❌ **Satisfaction**: <70% developer satisfaction
3. ❌ **Quality**: >1 critical bug per SAP
4. ❌ **Adoption**: Unable to generate 2 SAPs

**Action if NO-GO**:
- Document lessons learned
- Archive templates for future reference
- Analyze differences from chora-compose (why they succeeded 9x)
- Re-evaluate when SAP count >30 or pain point increases

---

## Next Steps After Plan Approval

### Immediate Actions (Start Week 1)

1. [ ] Create directory structure:
   ```
   docs/project-docs/dogfooding-pilot/
   ├── week-1-pattern-extraction.md
   ├── week-1-schema-design.md
   ├── week-2-plan.md
   └── metrics-tracking.csv
   ```

2. [ ] Read reference SAPs (Task 1.1)
   - SAP-028 (publishing-automation)
   - SAP-000 (sap-framework)
   - SAP-020 (react-foundation)
   - SAP-001 (inbox-coordination)
   - SAP-019 (sap-self-evaluation)

3. [ ] Extract artifact structures (Task 1.2)
   - capability-charter-structure.md
   - protocol-spec-structure.md
   - awareness-guide-structure.md
   - adoption-blueprint-structure.md
   - ledger-structure.md

4. [ ] Complete Week 1 plan (Tasks 1.3-1.5)

### Week 2 Preparation

- [ ] Review Week 1 deliverables
- [ ] Set up templates/ directory
- [ ] Install Jinja2 (if not already installed)
- [ ] Prepare test data for template rendering

---

## Coordination with chora-compose

**Opportunity**: chora-compose pioneered this pattern (9x efficiency gain)

**Questions for chora-compose** (from COORD-2025-009-RESPONSE):
1. **Q1**: Are there specific gotchas from your 6-month production experience?
2. **Q2**: Is chora-compose preparing v2.0.0 documentation we should be aware of?

**Timeline**: Need input before Q1 2026 pilot launch

**Action**: Send questions via SAP-001 inbox protocol (optional, but valuable)

---

## Future Enhancements (Post-Pilot)

### If SAP-027 Formalized (Q1 2026)

**v1.0.0 (Initial SAP)**:
- Document MVD pattern (data + templates + generator)
- Create awareness guide for AI agents
- Adoption blueprint (how to adopt dogfooding in any project)

**v1.1.0 (Content Automation)**:
- Extend schema with richer content fields
- Add content pre-fill (problem patterns, solution templates)
- Reduce manual effort from 20% → 10%

**v1.2.0 (Cross-SAP Intelligence)**:
- Analyze existing SAPs to suggest related SAPs
- Auto-generate dependency recommendations
- Suggest tags based on content analysis

### Integration with Other SAPs

- **SAP-003 (project-bootstrap)**: Add dogfooding to generated projects
- **SAP-019 (sap-self-evaluation)**: Auto-run evaluation on generated SAPs
- **SAP-001 (inbox-coordination)**: Share pattern with ecosystem

---

## Appendix A: Reference Documents

### Created During Planning

1. `DOGFOODING-PILOT-PLAN.md` (this document)
2. `docs/project-docs/dogfooding-pilot/` (Week 1-8 artifacts)

### Referenced Documents

1. `inbox/incoming/coordination/COORD-2025-009-SAP-PATTERN-RECOMMENDATIONS.md` - chora-compose pattern sharing
2. `inbox/outgoing/COORD-2025-009-RESPONSE-summary.md` - Our acceptance and pilot plan
3. `sap-catalog.json` - Current SAP metadata (v4.8.0, 28 SAPs)
4. `docs/skilled-awareness/publishing-automation/` - SAP-028 (just completed)
5. `docs/skilled-awareness/sap-framework/protocol-spec.md` - SAP-000 structure definition

---

## Appendix B: Time Budget

| Week | Phase | Planned Hours | Cumulative |
|------|-------|--------------|------------|
| 1 | Research & Design | 2h | 2h |
| 2 | Template Creation | 3-4h | 5-6h |
| 3 | Generator Implementation | 2.5-3.5h | 7.5-9.5h |
| 4 | Pilot Testing | 2-4h | 9.5-13.5h |
| 5-8 | Validation Period | Ongoing | N/A |

**Total One-Time Investment**: 9.5-13.5 hours (includes pilot testing)

**Expected Per-SAP Time** (after pilot):
- Manual: 10 hours
- Generated: 2 hours
- **Savings: 8 hours per SAP**

---

## Appendix C: Contact & Collaboration

**chora-base Owner**: Victor
**Pilot Timeline**: Q1 2026 (8 weeks)
**Coordination**: SAP-001 Inbox Protocol

**Questions or Feedback**: inbox/incoming/ or direct message

---

**Plan Version**: 1.0.0
**Created**: 2025-11-02
**Status**: Ready for Week 1 execution
**Next Review**: End of Week 1 (after pattern extraction complete)
