---
id: vision-{project}-{horizon}
type: strategic-vision
horizon: 6-month
status: draft
waves:
  - wave: 1
    status: committed
    target_version: v1.X.0
    decision_review: null
  - wave: 2
    status: exploratory
    target_version: v1.Y.0
    decision_review: YYYY-QX
  - wave: 3
    status: aspirational
    target_version: v2.0.0
    decision_review: YYYY-QX
tags: [vision, strategic-planning, {project}]
created: YYYY-MM-DDTHH:MM:SSZ
updated: YYYY-MM-DDTHH:MM:SSZ
---

# Vision: {Project Name} {Horizon} ({Start Date} - {End Date})

## Overview

**Purpose**: This vision document outlines the strategic direction for {project name} over the next {horizon period}. It organizes planned work into three waves representing different commitment levels and validation stages.

**Horizon**: {horizon period} (e.g., 3-month, 6-month, 12-month)

**Strategic Themes**: {List 2-4 strategic themes this vision addresses}

---

## Wave 1: {Theme Name} (Committed - 3 months)

**Target**: {target version} ({target date})

**Status**: Committed (ready for ROADMAP.md)

### Features

**Feature 1: {Feature Name}**
- **Description**: {1-2 sentence description}
- **Success Criteria**:
  - {Measurable criterion 1}
  - {Measurable criterion 2}
  - {Measurable criterion 3}
- **Effort Estimate**: {X-Y hours}
- **Related SAPs**: {SAP-XXX, SAP-YYY}

**Feature 2: {Feature Name}**
- **Description**: {1-2 sentence description}
- **Success Criteria**:
  - {Measurable criterion 1}
  - {Measurable criterion 2}
- **Effort Estimate**: {X-Y hours}
- **Related SAPs**: {SAP-XXX}

### Success Criteria (Wave 1)

- ✅ {Overall wave success criterion 1}
- ✅ {Overall wave success criterion 2}
- ✅ {Overall wave success criterion 3}

### Rationale

**Why Wave 1 (Committed)?**
- **Evidence Level**: {XX}% Level A+B (exceeds 70% threshold)
- **User Demand**: {N} explicit requests from {sources}
- **Strategic Value**: {Why this is foundational/high-priority}
- **ROI Potential**: {Estimated ROI multiplier based on validation data}

---

## Wave 2: {Theme Name} (Exploratory - 6 months)

**Target**: {target version} ({target date})

**Status**: Exploratory (validate via dogfooding before committing)

**Decision Review**: {Quarter} (e.g., 2026-Q1)

### Candidates

**Candidate 1: {Feature Name}**
- **Description**: {1-2 sentence description}
- **Validation Plan**: {How will this be validated? e.g., dogfooding pilot, user interviews}
- **Success Criteria** (for promotion to Wave 1):
  - {Validation criterion 1}
  - {Validation criterion 2}
- **Effort Estimate**: {X-Y hours}
- **Related SAPs**: {SAP-XXX}

**Candidate 2: {Feature Name}**
- **Description**: {1-2 sentence description}
- **Validation Plan**: {Dogfooding approach}
- **Success Criteria** (for promotion):
  - {Validation criterion 1}
  - {Validation criterion 2}
- **Effort Estimate**: {X-Y hours}

### Decision Criteria (Wave 2 → Wave 1 Promotion)

At quarterly review ({decision_review date}), promote to Wave 1 if:
- ✅ Dogfooding validation shows {specific measurable outcome}
- ✅ User demand increases to {N+} requests
- ✅ Evidence level reaches {XX}% Level A+B
- ✅ ROI potential validated at {X}x multiplier

### Rationale

**Why Wave 2 (Exploratory)?**
- **Evidence Level**: {XX}% Level A+B (60-70% range, needs validation)
- **User Demand**: {N} requests (moderate demand, needs growth)
- **Strategic Value**: {Why this has potential but needs validation}
- **Validation Needed**: {What specific data/feedback is needed before committing}

---

## Wave 3: {Theme Name} (Aspirational - 12 months)

**Target**: {target version} ({target date})

**Status**: Aspirational (long-term vision, defer until more data)

**Decision Review**: Quarterly (promote to Wave 2 or remove)

### Long-Term Vision

**Vision Item 1: {Feature Name}**
- **Description**: {1-2 sentence description of future possibility}
- **What's Missing**: {Why this isn't ready yet - evidence, demand, resources}
- **Path to Wave 2**: {What would need to happen for this to move to exploratory}
- **Related SAPs**: {SAP-XXX}

**Vision Item 2: {Feature Name}**
- **Description**: {Future possibility}
- **What's Missing**: {Gaps preventing earlier commitment}
- **Path to Wave 2**: {Required conditions for promotion}

### Quarterly Review Criteria (Wave 3 → Wave 2 Promotion)

Promote to Wave 2 if:
- ✅ New evidence emerges (e.g., industry standards, research, production data)
- ✅ User demand increases significantly ({N}+ explicit requests)
- ✅ Strategic priority shifts (e.g., ecosystem adoption, new use cases)
- ✅ Resource availability improves (e.g., automation, team growth)

### Rationale

**Why Wave 3 (Aspirational)?**
- **Evidence Level**: {XX}% Level A+B (below 60%, insufficient evidence)
- **User Demand**: {N} requests (low demand, not critical)
- **Strategic Value**: {Future potential but not immediate priority}
- **Defer Until**: {What conditions would justify moving this earlier}

---

## Dependencies & Integration

### Dependencies
- **Blockers**: {List any blockers preventing Wave 1 delivery}
- **Enablers**: {List what Wave 1 enables for future waves}

### Integration with Other SAPs
- **SAP-XXX**: {How this vision integrates with other SAPs}
- **SAP-YYY**: {Cross-SAP dependencies}

### Traceability
- **From Intention Inventory**: `intention-inventory-{date}.md`
- **From Strategic Theme Matrix**: `strategic-themes-{date}.md`
- **To Roadmap Milestone**: `milestone-{version}.md` (created after Wave 1 commit)
- **To Beads Epic**: {epic-id} (created via SAP-015 after Wave 1 commit)

---

## Metrics & Success Tracking

### Wave 1 Success Metrics
- **Metric 1**: {Measurable outcome} - Target: {value}
- **Metric 2**: {Measurable outcome} - Target: {value}
- **Metric 3**: {Measurable outcome} - Target: {value}

### Wave 2 Validation Metrics
- **Pilot Metric 1**: {What to measure during dogfooding} - Target: {value}
- **Pilot Metric 2**: {Validation criterion} - Target: {value}

### Timeline
- **Vision Created**: {creation date}
- **Wave 1 Target**: {target date}
- **Wave 2 Decision Review**: {review date}
- **Wave 3 Quarterly Review**: Every quarter

---

## Changelog

### {YYYY-MM-DD} - Vision Created
- Initial vision document created from intention inventory and strategic theme analysis
- Wave 1: {X} features committed
- Wave 2: {Y} candidates for validation
- Wave 3: {Z} long-term vision items

### {YYYY-MM-DD} - Quarterly Review
- {Record changes to wave status, promotions, deferrals}

---

## Example: Chora-Base 6-Month Vision (Nov 2025 - Apr 2026)

**Note**: This example shows how the template is used in practice.

---
id: vision-chora-base-6-month
type: strategic-vision
horizon: 6-month
status: active
waves:
  - wave: 1
    status: committed
    target_version: v1.5.0
    decision_review: null
  - wave: 2
    status: exploratory
    target_version: v1.6.0
    decision_review: 2026-Q1
  - wave: 3
    status: aspirational
    target_version: v2.0.0
    decision_review: quarterly
tags: [vision, strategic-planning, chora-base]
created: 2025-11-05T00:00:00Z
updated: 2025-11-05T00:00:00Z
---

# Vision: chora-base 6-Month (Nov 2025 - Apr 2026)

## Wave 1: Strategic Planning Infrastructure (Committed - 3 months)

**Target**: v1.5.0 (Feb 2026)

### Features

**SAP-010: Strategic Knowledge Templates**
- Add 4 templates (vision, intention inventory, roadmap milestone, strategic theme matrix)
- Success Criteria:
  - Templates reusable across ecosystem projects
  - Integration with SAP-006, SAP-015, SAP-027 validated
- Effort: 4-6 hours

**SAP-006: Vision Synthesis Workflow**
- 4-phase workflow (discovery → analysis → drafting → cascade)
- Success Criteria:
  - Vision synthesis time reduced from days to hours
  - Evidence-based decision criteria (70% A+B threshold)
- Effort: 8-12 hours

**SAP-015: Backlog Organization Patterns**
- Multi-tier backlog (P0-P4), vision → backlog cascade
- Success Criteria:
  - Backlog health metrics tracked
  - Epic decomposition patterns documented
- Effort: 6-10 hours

**SAP-027: Pre-Pilot Discovery Phase**
- Week -1 discovery phase for pilot selection
- Success Criteria:
  - Pilot → vision feedback loop established
  - Intention prioritization validated
- Effort: 4-6 hours

### Rationale
- Evidence: 79% Level A+B (11/14 intentions)
- Demand: 4 explicit inbox requests, 10 GitHub feature requests
- ROI: 10x potential (reduce vision synthesis from 40 hours → 4 hours)

## Wave 2: Automation & Tooling (Exploratory - 6 months)

**Decision Review**: 2026-Q1

### Candidates

**Intention Discovery CLI** (`scripts/discover-intentions.py`)
- Validation Plan: Use in Wave 1 execution, measure time savings
- Success Criteria: Saves 50%+ time on intention scanning

**Strategic Theme Clustering CLI** (`scripts/cluster-strategic-themes.py`)
- Validation Plan: Dogfood during quarterly vision review
- Success Criteria: Accurate theme detection (90%+ match with manual clustering)

### Decision Criteria
Promote if Wave 1 usage shows 5x+ time savings over manual workflows.

## Wave 3: Ecosystem Adoption (Aspirational - 12 months)

**Target**: 3+ ecosystem projects adopt strategic planning SAPs

**What's Missing**: Wave 1 validation, public documentation, video tutorials

**Path to Wave 2**: After Wave 1 delivery + 1 external adopter feedback

---

## Usage Instructions

### How to Use This Template

1. **Copy Template**:
   ```bash
   cp .chora/memory/templates/vision-document-template.md \
      .chora/memory/knowledge/notes/vision-{project}-{horizon}.md
   ```

2. **Fill Frontmatter**:
   - Replace `{project}` with your project name
   - Replace `{horizon}` with timeframe (3-month, 6-month, 12-month)
   - Set `status: draft` initially
   - Fill `waves` array with target versions and dates

3. **Fill Wave 1 (Committed)**:
   - List features from HIGH-priority strategic themes (evidence A+B ≥ 70%)
   - Define measurable success criteria
   - Estimate effort for each feature

4. **Fill Wave 2 (Exploratory)**:
   - List candidates from MEDIUM-priority themes (evidence A+B 60-70%)
   - Define validation plan (how to dogfood/validate)
   - Set decision review date (quarterly)

5. **Fill Wave 3 (Aspirational)**:
   - List long-term vision items from LOW-priority themes or future possibilities
   - Define what's missing (evidence, demand, resources)
   - Define path to Wave 2 (what conditions would promote this)

6. **Review & Activate**:
   - Update `status: active` after stakeholder review
   - Create roadmap milestone for Wave 1 (use `roadmap-milestone-template.md`)

### Integration with Other Templates

**Inputs** (used to create this vision):
- `intention-inventory-{date}.md` - Source of intentions
- `strategic-themes-{date}.md` - Theme clustering and prioritization

**Outputs** (created from this vision):
- `milestone-{version}.md` - Roadmap milestone for Wave 1 features
- Beads epic via SAP-015 - Tasks for Wave 1 delivery

### When to Update Vision

**Quarterly Review**:
- Check Wave 2 decision criteria (promote, defer, or remove)
- Check Wave 3 promotion criteria (new evidence, demand, priority shifts)
- Update `updated` timestamp in frontmatter
- Add changelog entry

**After Wave Delivery**:
- Mark Wave 1 as delivered, update status to archived
- Promote Wave 2 → Wave 1 if validation successful
- Create new vision document for next period
