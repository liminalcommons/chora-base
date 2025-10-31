# Wave 1: SAP Evolution Opportunities

**Wave**: Wave 1 - Documentation Architecture Unification
**Date**: 2025-10-28
**Purpose**: Identify patterns from Wave 1 that could become new or enhanced SAPs

---

## Executive Summary

Wave 1 revealed multiple opportunities for SAP evolution across three levels:
- **Object-Level**: 2 new SAP candidates (Documentation Migration, Link Validation)
- **Process-Level**: 3 SAP enhancements (SAP-007, SAP-008, SAP-000)
- **Meta-Level**: 1 framework enhancement (SAP opportunity identification)

**Priority for v4.0**: Medium-High (especially Link Validation for Wave 2+)

---

## Object-Level Opportunities

### Potential SAP-015: Documentation Migration

**Why Create This SAP?**
- Repeated pattern across multiple waves and projects
- Complex enough to benefit from structured approach
- High value for external adopters migrating to chora-base
- Proven workflow created in Wave 1

**Capability Description**:
Systematic documentation restructuring with validation, enabling projects to migrate from any documentation structure to chora-base's 4-domain architecture.

**Artifacts Needed**:

1. **capability-charter.md**
   - Business value: Reduce migration time by 50-70% vs ad-hoc approach
   - Problem: Documentation restructuring is error-prone, time-consuming
   - Scope: File classification, migration, validation, reference updates
   - Outcomes: 100% coherence maintained, zero broken links

2. **protocol-spec.md**
   - Inputs: Source documentation structure, target 4-domain structure
   - Outputs: Migrated files, updated references, validation report
   - Guarantees: No files lost, all references updated, coherence maintained
   - Constraints: Requires manual decisions on ambiguous classifications

3. **awareness-guide.md**
   - Base: [DOCUMENTATION_MIGRATION_WORKFLOW.md](../workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) (already exists!)
   - References:
     - dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md - Process
     - project-docs/sprints/wave-1-sprint-plan.md - Example sprint
     - project-docs/metrics/wave-1-execution-metrics.md - Measured results
     - scripts/inventory-chora-base.py - Validation tool

4. **adoption-blueprint.md**
   - Prerequisites: Baseline inventory, migration plan
   - Installation: Copy workflow, adapt to project
   - Validation: Run inventory before/after, check links
   - Tools: inventory script, sed for path updates

5. **ledger.md**
   - Track adoptions: Which projects used this SAP
   - Feedback: What worked, what didn't
   - Versions: Track SAP evolution

**Dependencies**: SAP-007 (Documentation Framework)

**Priority**: Medium
- Essential for external adopters
- Useful for Waves 2-7 (documentation reorganization)
- Can be deferred to post-v4.0 if time-constrained

**Effort to Create**: ~20-30 hours
- Charter: 4h (define business value)
- Protocol: 6h (formalize contracts)
- Awareness-guide: 4h (adapt existing workflow)
- Adoption-blueprint: 4h (installation steps)
- Ledger: 2h (template + Wave 1 entry)
- Integration: 4h (update INDEX, cross-references)
- Validation: 6h (test with example migration)

---

### Potential SAP-016: Link Validation & Reference Management

**Why Create This SAP?**
- Critical for maintaining documentation coherence
- Prevents broken links after migrations
- High ROI: Automated validation vs manual checking
- Needed for Wave 2+ quality assurance

**Capability Description**:
Automated link checking, reference mapping, and broken link detection across all documentation and code.

**Artifacts Needed**:

1. **capability-charter.md**
   - Business value: Eliminate broken links, maintain navigation integrity
   - Problem: Manual link checking is slow, error-prone, incomplete
   - Scope: Markdown links, code imports, relative paths, external URLs
   - Outcomes: 100% valid links, reference graph visualization

2. **protocol-spec.md**
   - Inputs: Documentation paths, link patterns to check
   - Outputs: Validation report, broken link list, reference graph
   - Guarantees: Detects all internal broken links, reports external link status
   - Constraints: Cannot fix links automatically (only detection)

3. **awareness-guide.md**
   - How to run link checker
   - How to interpret results
   - How to fix common link issues
   - Integration with CI/CD (fail builds on broken links)
   - References:
     - scripts/validate-links.sh - Tool (to be created)
     - dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md - Use case
     - .github/workflows/link-validation.yml - CI integration

4. **adoption-blueprint.md**
   - Prerequisites: Python 3.x, markdown files
   - Installation: Copy script, configure paths
   - Usage: Run before commits, in CI pipeline
   - Validation: Should detect known broken links

5. **ledger.md**
   - Track which projects use link validation
   - Track bugs found and fixed

**System Files**:
- `scripts/validate-links.sh` - Link checker script (to be created)
- `.github/workflows/link-validation.yml` - CI integration (to be created)

**Dependencies**: SAP-007 (Documentation Framework), SAP-008 (Automation Scripts)

**Priority**: High
- Needed immediately for Wave 2 (SAP content audit)
- Prevents quality issues in future waves
- Low effort, high value

**Effort to Create**: ~12-16 hours
- Charter: 2h
- Protocol: 3h
- Awareness-guide: 2h
- Adoption-blueprint: 2h
- Ledger: 1h
- **Script development**: 6-8h (the main effort)
- Integration: 2h

**Recommendation**: Create in early Wave 2 before SAP content audit begins.

---

## Process-Level Opportunities

### Enhancement to SAP-008: Automation Scripts

**Learning from Wave 1**:
Migration benefits from incremental automation (move-one-validate-one pattern).

**Proposed Enhancement**:
Add documentation migration automation patterns to SAP-008.

**New Scripts to Add**:

1. **scripts/migrate-doc.sh**
   ```bash
   # Move file + update references + validate
   migrate-doc.sh <old-path> <new-path>
   ```
   - Moves file with git mv (if tracked) or mv
   - Updates all references automatically (sed on common locations)
   - Validates no broken references remain
   - Logs migration in manifest

2. **scripts/validate-links.sh**
   ```bash
   # Comprehensive link checker
   validate-links.sh [--domain docs/] [--fix]
   ```
   - Checks all markdown links
   - Reports broken links
   - Optional: Suggests fixes
   - Integrates with CI

3. **scripts/generate-reference-table.sh**
   ```bash
   # Auto-create old→new mapping for migrations
   generate-reference-table.sh <old-dir> <new-dir>
   ```
   - Scans directories
   - Generates migration mapping table
   - Outputs markdown table for planning

**Update Required**:
- SAP-008 awareness-guide.md: Add "Documentation Migration Patterns" section
- SAP-008 protocol-spec.md: Add scripts to guaranteed scripts list
- Create 3 new scripts in scripts/

**Effort**: ~16-20 hours
- Script development: 12-16h
- SAP-008 updates: 4h

**Priority**: Medium (helpful for future migrations, not critical)

---

### Enhancement to SAP-007: Documentation Framework

**Learning from Wave 1**:
4-domain decision tree is critical for content classification.

**Proposed Enhancement**:
Add domain classification decision tree tool/checklist to SAP-007.

**New Artifact**:

1. **docs/user-docs/reference/documentation-classification-guide.md**
   - Interactive decision tree (can be CLI tool or documentation)
   - Examples for each domain
   - Anti-patterns (what NOT to put where)
   - Referenced from SAP-007 awareness-guide

2. **Optional: scripts/classify-doc.sh**
   ```bash
   # Interactive classification helper
   classify-doc.sh <file-path>
   ```
   - Asks questions about the file
   - Suggests domain based on answers
   - Can move file if user confirms

**Update Required**:
- SAP-007 awareness-guide.md: Add "Content Classification" section
- SAP-007 protocol-spec.md: Add classification as a capability
- Create classification guide document

**Effort**: ~8-12 hours
- Classification guide: 6h
- SAP-007 updates: 2h
- Optional script: 4h (if implemented)

**Priority**: Medium-Low (helpful, but ARCHITECTURE.md already provides decision tree)

---

### Enhancement to SAP-000: SAP Framework

**Learning from Wave 1**:
Each wave reveals new SAP opportunities - we need a systematic approach to identify them.

**Proposed Enhancement**:
Add "Identifying SAP Opportunities" section to SAP-000.

**New Content**:

1. **sap-framework/awareness-guide.md** - Add section:
   ```markdown
   ## Identifying SAP Opportunities

   ### During Wave Execution

   Ask these questions:

   **Object-Level** (Directly applicable to task):
   - Could this task be its own SAP?
   - Is this pattern reusable across projects?
   - Does it have clear inputs/outputs?

   **Process-Level** (Broader workflow):
   - Did we discover a repeatable pattern?
   - Is there a tool/script that should be formalized?
   - Would other projects benefit from this workflow?

   **Meta-Level** (Framework improvements):
   - Does this reveal gaps in SAP framework itself?
   - Should SAP-000 be enhanced?
   - Is there a meta-pattern about identifying SAPs?

   ### Documentation Pattern

   Create: `docs/dev-docs/research/wave-N-sap-opportunities.md`

   Document:
   - Potential new SAPs
   - SAP enhancements
   - Priority and effort estimates
   - Dependencies

   ### Timing

   - During execution: Note insights
   - During retrospective: Formalize opportunities
   - Between waves: Prioritize and plan SAP creation
   ```

2. **sap-framework/protocol-spec.md** - Add:
   ```markdown
   ## SAP Lifecycle: Discovery

   SAPs can emerge from:
   1. Wave retrospectives (what patterns did we use?)
   2. External adoption feedback (what do adopters need?)
   3. Cross-repo analysis (what's common across projects?)
   4. Framework evolution (what gaps exist?)
   ```

**Update Required**:
- SAP-000 awareness-guide.md: Add section (~400 lines)
- SAP-000 protocol-spec.md: Add discovery lifecycle (~200 lines)
- Update document-templates.md with opportunity template

**Effort**: ~6-8 hours
- Content writing: 4-5h
- Integration: 2-3h

**Priority**: Medium (useful for future waves, demonstrates meta-awareness)

**Impact**: Makes SAP discovery systematic rather than ad-hoc.

---

## Meta-Level Insights

### Pattern: Waves Reveal SAPs

**Observation**:
Wave 1 (documentation restructuring) revealed at least 2 new SAP candidates and 3 enhancement opportunities.

**Hypothesis**:
Each wave will reveal 1-3 new SAP opportunities as we encounter reusable patterns.

**Implication for v4.0 Planning**:
- Reserve "SAP discovery" as an explicit phase in each wave retrospective
- Budget 10-15% of wave time for SAP opportunity documentation
- Plan "SAP consolidation wave" (could be Wave 2.5 or Wave 4.5) to formalize discoveries

**Recommendation**:
Add to each Wave retrospective checklist:
```markdown
## SAP Discovery Questions

1. What patterns did we use repeatedly?
2. What tools did we create?
3. What decisions required frameworks?
4. What would help external adopters?
5. What revealed gaps in existing SAPs?
```

---

## Prioritization for v4.0

### High Priority (Create in Wave 2)

**SAP-016: Link Validation**
- **Why**: Needed immediately for Wave 2 SAP content audit
- **Effort**: 12-16h
- **Impact**: Prevents quality issues in all future waves
- **Dependencies**: None (can start immediately)

### Medium Priority (Create in Wave 3-4)

**SAP-015: Documentation Migration**
- **Why**: Useful for external adopters, demonstrates patterns
- **Effort**: 20-30h
- **Impact**: High value for adoption, lower urgency
- **Dependencies**: Wave 1 complete (provides basis)

**SAP-008 Enhancement: Migration Scripts**
- **Why**: Useful for Wave 2-7 documentation work
- **Effort**: 16-20h
- **Impact**: Efficiency gains in future waves
- **Dependencies**: SAP-016 (link validation) should exist first

### Medium-Low Priority (Create in Wave 4-5 or post-v4.0)

**SAP-007 Enhancement: Classification Guide**
- **Why**: ARCHITECTURE.md already provides decision tree
- **Effort**: 8-12h
- **Impact**: Helpful but not critical
- **Dependencies**: None

**SAP-000 Enhancement: SAP Discovery**
- **Why**: Improves framework, demonstrates meta-awareness
- **Effort**: 6-8h
- **Impact**: Systematic vs ad-hoc discovery
- **Dependencies**: Wave 2 retrospective (more data points)

---

## Action Items

### Immediate (Wave 2 Start)

- [ ] Create SAP-016 (Link Validation) before SAP content audit begins
- [ ] Add SAP discovery questions to Wave 2 retrospective template
- [ ] Review this document during Wave 2 planning

### Wave 3-4

- [ ] Decide: Create SAP-015 (Documentation Migration) or defer to post-v4.0?
- [ ] Decide: Enhance SAP-008 with migration scripts?
- [ ] Review SAP opportunity backlog, prioritize for v4.1

### Wave 6-7

- [ ] Consolidate all SAP discoveries from Waves 1-5
- [ ] Create any high-value SAPs before v4.0 release
- [ ] Document SAP roadmap for v4.1

### Post-v4.0

- [ ] External adoption feedback: What SAPs do adopters need?
- [ ] Cross-repo analysis: What patterns emerge?
- [ ] Plan v4.1 SAP additions

---

## Cross-Wave Patterns

### Emerging Patterns to Watch

As we complete Waves 1-7, look for:
- **Repeated tools/scripts** → Candidate SAPs
- **Repeated decision points** → Candidate decision trees
- **Repeated validations** → Candidate quality gates
- **Repeated process steps** → Candidate workflows

### Example Pattern Triggers

**Tool trigger**: If we create 3+ similar scripts, consider a SAP
**Decision trigger**: If we ask the same question 5+ times, create decision tree
**Validation trigger**: If we run the same check 10+ times, automate and formalize
**Process trigger**: If we follow the same steps 3+ times, document as workflow

---

## Integration with Existing SAPs

### SAP-007 (Documentation Framework)
- Enhanced with migration patterns (proposed)
- Enhanced with classification guide (proposed)
- Already covers 4-domain architecture (complete)

### SAP-008 (Automation Scripts)
- Enhanced with migration scripts (proposed)
- Could include link validation (if SAP-016 not created separately)

### SAP-000 (SAP Framework)
- Enhanced with SAP discovery framework (proposed)
- Demonstrates meta-awareness (chora-base using chora-base)

### New SAPs
- SAP-015: Documentation Migration (proposed)
- SAP-016: Link Validation & Reference Management (proposed)

---

## Recommendations

### For Wave 2

1. **Create SAP-016 first** (link validation) - highest ROI, needed immediately
2. **Add SAP discovery to retrospective** - systematic opportunity identification
3. **Review migration workflow** - any improvements before formalizing as SAP?

### For Wave 3-4

1. **Decide on SAP-015** - documentation migration as formal SAP or keep as workflow?
2. **Consider SAP-008 enhancements** - migration scripts add value?

### For Post-v4.0

1. **External feedback loop** - what SAPs do adopters request?
2. **SAP marketplace vision** - how do SAPs spread across organizations?
3. **SAP quality scoring** - how do we measure SAP effectiveness?

---

**Document Version**: 1.0
**Created**: 2025-10-28
**Author**: Claude (chora-base development team)
**Status**: Active (informs Wave 2+ planning)
**Next Review**: Wave 2 retrospective
