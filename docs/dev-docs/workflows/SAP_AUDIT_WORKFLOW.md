# SAP Audit Workflow

**Workflow Type**: Quality Assurance
**Purpose**: Systematic audit process for ensuring SAP completeness, accuracy, and cross-domain integration
**Created**: 2025-10-28 (Wave 2)
**Version**: 1.0

---

## Overview

This workflow provides a systematic approach to auditing Skilled Awareness Packages (SAPs) to ensure:
- Complete and actionable content in all 5 artifacts
- Valid cross-domain references (dev-docs/, project-docs/, user-docs/, system files)
- No broken links (internal or external)
- Concrete examples rather than hypothetical claims
- Alignment with chora-base 4-domain architecture

**Use Cases**:
- Wave 2: Auditing all 14 existing SAPs
- Post-release: Quality checks before SAP distribution
- External adoption: Validating SAPs before cloning into new projects
- SAP creation: Final validation before marking SAP as "complete"

**Time per SAP**: 3-6 hours (varies by SAP complexity and existing quality)

---

## Prerequisites

**Before starting SAP audit**:
- [ ] Link validation script exists (`scripts/validate-links.sh`) - See SAP-016
- [ ] Inventory script functional (`scripts/inventory-chora-base.py`)
- [ ] 4-domain architecture in place (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- [ ] Gap tracking system ready (spreadsheet or markdown table)

**Per-SAP Prerequisites**:
- [ ] SAP exists with all 5 artifacts (charter, protocol, awareness-guide, blueprint, ledger)
- [ ] SAP is in docs/skilled-awareness/[sap-name]/
- [ ] SAP is listed in docs/skilled-awareness/INDEX.md

---

## Audit Process: 6-Step Pattern

### Step 1: Read & Analyze (1-1.5 hours)

**Objective**: Understand SAP scope, claims, and current state

**Tasks**:

1. **Read all 5 artifacts sequentially**:
   ```bash
   # Open in editor
   cd docs/skilled-awareness/[sap-name]

   # Read order:
   # 1. capability-charter.md - Business value, scope
   # 2. protocol-spec.md - Inputs, outputs, guarantees
   # 3. awareness-guide.md - How to use the SAP
   # 4. adoption-blueprint.md - Installation, prerequisites
   # 5. ledger.md - Adoption history
   ```

2. **Create reading notes**:
   - What is the SAP's primary capability?
   - What business value does it claim to provide?
   - What are the key inputs/outputs?
   - What guarantees does it make?
   - What examples are provided?

3. **Map existing references**:
   - Which dev-docs/ files are referenced?
   - Which project-docs/ files are referenced?
   - Which user-docs/ files are referenced?
   - Which system files (code, scripts, configs) are referenced?

4. **Note claims vs. reality**:
   - Does the SAP claim files exist that don't?
   - Are examples concrete or hypothetical?
   - Are workflows referenced or inline?
   - Are there "TODO" or "to be created" markers?

**Deliverable**: Reading notes document or inline comments

---

### Step 2: Cross-Domain Gap Analysis (1-1.5 hours)

**Objective**: Identify missing or broken cross-domain references

**Tasks**:

1. **Check dev-docs/ references**:
   ```bash
   # List all dev-docs references in SAP
   grep -r "dev-docs/" docs/skilled-awareness/[sap-name]/

   # Verify each reference exists
   for path in $(grep -roh "dev-docs/[^)]*" docs/skilled-awareness/[sap-name]/); do
     [ -f "docs/$path" ] && echo "✅ $path" || echo "❌ MISSING: $path"
   done
   ```

2. **Check project-docs/ references**:
   ```bash
   grep -r "project-docs/" docs/skilled-awareness/[sap-name]/

   # Same validation as above
   ```

3. **Check user-docs/ references**:
   ```bash
   grep -r "user-docs/" docs/skilled-awareness/[sap-name]/
   ```

4. **Check system file references** (code, scripts, configs):
   ```bash
   # Look for absolute paths or repository root paths
   grep -r "scripts/" docs/skilled-awareness/[sap-name]/
   grep -r "src/" docs/skilled-awareness/[sap-name]/
   grep -r "\.github/" docs/skilled-awareness/[sap-name]/

   # Verify each exists
   ```

5. **Document gaps by priority**:
   - **Critical**: SAP claims file exists but it doesn't (broken reference)
   - **High**: SAP would be significantly more useful with this content
   - **Medium**: Nice-to-have, improves completeness
   - **Low**: Optional enhancement, minimal impact

**Deliverable**: Gap analysis report (markdown table)

**Template**:
```markdown
## [SAP-NAME] Gap Analysis

### Critical Gaps (Blocks SAP Usage)
- [ ] awareness-guide.md references `dev-docs/workflows/foo.md` (doesn't exist)
- [ ] protocol-spec.md claims script `scripts/bar.sh` (doesn't exist)

### High-Value Gaps (Significantly Improves SAP)
- [ ] No examples in dev-docs/examples/
- [ ] Missing user-facing how-to guide in user-docs/

### Medium Gaps (Improves Completeness)
- [ ] Awareness-guide could reference project-docs/metrics/
- [ ] Blueprint could link to user-docs/reference/

### Low Priority Gaps (Optional)
- [ ] Could add more examples
- [ ] Could create visualization diagram
```

---

### Step 3: Run Link Validation (30 minutes)

**Objective**: Detect all broken links (internal and external)

**Tasks**:

1. **Run automated link checker on SAP directory**:
   ```bash
   # Using SAP-016 link validation script
   ./scripts/validate-links.sh docs/skilled-awareness/[sap-name]/
   ```

2. **Review link validation report**:
   - Internal broken links (critical - must fix)
   - External broken links (investigate - may be intentional or temporary)
   - Ambiguous paths (may work but should be clarified)

3. **Categorize broken links**:
   - **Must fix**: Internal links to docs that should exist
   - **Should fix**: External links to permanent resources (GitHub, official docs)
   - **Note**: External links to dynamic content (may break legitimately)
   - **Defer**: Low-priority documentation enhancements

4. **Document broken links in gap report**:
   ```markdown
   ### Broken Links (Critical)
   - [ ] awareness-guide.md:42 - Links to `../dev-docs/foo.md` (404)
   - [ ] protocol-spec.md:17 - Links to `../../user-docs/bar.md` (404)

   ### External Link Issues
   - [ ] blueprint.md:56 - Links to example.com/resource (404) - May be outdated
   ```

**Deliverable**: Link validation report (from script) + categorized issues in gap report

---

### Step 4: Content Completeness Check (30 minutes)

**Objective**: Ensure all 5 artifacts have actionable, concrete content

**Tasks**:

1. **Capability Charter Checklist**:
   - [ ] Business value clearly stated?
   - [ ] Problem statement concrete (not generic)?
   - [ ] Scope boundaries defined?
   - [ ] Outcomes measurable?
   - [ ] Examples or metrics included?

2. **Protocol Specification Checklist**:
   - [ ] Inputs clearly defined?
   - [ ] Outputs clearly defined?
   - [ ] Guarantees specific (not vague)?
   - [ ] Constraints documented?
   - [ ] Error cases handled?

3. **Awareness Guide Checklist**:
   - [ ] "How to use" instructions clear?
   - [ ] Examples are concrete (not hypothetical)?
   - [ ] Cross-domain references present (2+ domains)?
   - [ ] Common pitfalls documented?
   - [ ] Related content linked?

4. **Adoption Blueprint Checklist**:
   - [ ] Prerequisites explicit?
   - [ ] Installation steps actionable?
   - [ ] Validation criteria clear?
   - [ ] Tool dependencies listed?
   - [ ] Project-specific adaptation guidance?
   - [ ] **Post-install awareness enablement documented?**
   - [ ] **AGENTS.md/CLAUDE.md update steps included?**
   - [ ] **Validation commands for awareness updates included?**

5. **Ledger Checklist**:
   - [ ] At least 1 adoption recorded (chora-base itself)?
   - [ ] Feedback mechanism exists?
   - [ ] Version history tracked?

**Deliverable**: Completeness checklist (pass/fail per artifact)

---

### Step 4.5: Awareness Hierarchy Integration Check (15 minutes)

**Objective**: Ensure SAP adoption blueprint includes AGENTS.md/CLAUDE.md hierarchy updates for discoverability

**Why This Matters**:
- AGENTS.md/CLAUDE.md serve as **discoverability layer** for installed SAPs
- Without updates, agents cannot find newly installed capabilities
- Inconsistent across SAPs if not systematically validated

**Tasks**:

1. **Check for Post-Install Section**:
   ```bash
   grep -i "post-install\|awareness enablement" docs/skilled-awareness/[sap]/adoption-blueprint.md
   ```
   - [ ] Section exists?
   - [ ] Section is complete (not just placeholder)?

2. **Review AGENTS.md Update Instructions**:

   **Required elements**:
   - [ ] Explicit step to update root `AGENTS.md`?
   - [ ] Content template provided (what to add)?
   - [ ] Clear location guidance (which section to update)?
   - [ ] Validation command included (e.g., `grep "SAP-XXX" AGENTS.md`)?

   **Quality criteria**:
   - [ ] Instructions are **agent-executable** (use Edit tool)?
   - [ ] Template content is **concrete** (not just "add reference")?
   - [ ] Examples show **actual SAP references** (not `<sap-name>`)?

3. **Check for Domain-Specific AGENTS.md** (if applicable):

   Some SAPs need domain-specific AGENTS.md files (e.g., tests/, scripts/, docker/):

   - [ ] Does SAP create/modify files in specific domain (tests/, scripts/, etc.)?
   - [ ] If yes, are instructions to create domain-specific AGENTS.md included?
   - [ ] Are customization guidelines provided?

4. **Check for CLAUDE.md References** (if applicable):

   Not all projects have CLAUDE.md, but if mentioned:

   - [ ] CLAUDE.md update mentioned or conditional ("if exists")?
   - [ ] Context loading guidance provided?

5. **Validation Command Quality Check**:

   Good validation example (from SAP-000):
   ```bash
   grep "SAP-000\|SAP Framework" AGENTS.md && echo "✅ AGENTS.md updated"
   ```

   - [ ] Validation command exists?
   - [ ] Command checks for actual content (not just file existence)?
   - [ ] Success message clear?

**Gap Categorization**:

| Finding | Priority | Action |
|---------|----------|--------|
| No post-install section at all | **Critical** | Create in Step 5 |
| Post-install exists but no AGENTS.md step | **Critical** | Add AGENTS.md instructions |
| AGENTS.md step but no validation | **High** | Add validation command |
| Instructions unclear/hypothetical | **High** | Improve with concrete examples |
| Domain-specific AGENTS.md needed but missing | **Medium** | Add domain-specific instructions |
| CLAUDE.md not mentioned | **Low** | Note for Phase 5 |

**Reference Examples**:

**Good Pattern** (SAP-000):
```markdown
### Step 6: Update Project AGENTS.md

Add SAP Framework section to your project's `AGENTS.md`:

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Skilled Awareness Packages (SAPs)
[concrete content template]
```

**Validation**:
```bash
grep "Skilled Awareness Packages" AGENTS.md && echo "✅ AGENTS.md updated"
```
```

**Good Pattern** (SAP-001):
```markdown
## 6. Post-Install Tasks

- **Awareness Enablement:**
  - Update root `CLAUDE.md` and `AGENTS.md` to reference inbox awareness guide.
```

**Bad Pattern** (Avoid):
```markdown
## Post-Install
- Update AGENTS.md with this SAP
```
(No template, no validation, no clear instructions)

**Deliverable**:
- Awareness integration assessment (pass/partial/fail)
- Gaps documented by priority
- Reference to checklist: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](SAP_AWARENESS_INTEGRATION_CHECKLIST.md) (if exists)

**Anti-Pattern to Avoid**:
❌ **Don't skip this check assuming template was followed**
- Template exists but not all SAP creators follow it
- Critical for discoverability
- Quick check (15 min) prevents major usability gap

---

### Step 5: Create Critical Content (1-2 hours)

**Objective**: Fill gaps that block SAP usage or significantly reduce value

**Tasks**:

1. **Prioritize gap filling**:
   - Focus on **Critical** and **High** gaps only in this step
   - Defer Medium/Low gaps to Phase 5 (Content Creation) of Wave 2
   - Do NOT create content beyond SAP usability threshold

2. **Create missing dev-docs/ content** (if critical):
   ```bash
   # Example: SAP claims workflow exists but it doesn't
   # Create minimal viable workflow document

   # Template:
   # 1. Purpose (2-3 sentences)
   # 2. Prerequisites (bullet list)
   # 3. Steps (numbered list)
   # 4. Validation (how to verify success)
   # 5. Cross-references (link back to SAP)
   ```

3. **Create missing user-docs/ content** (if critical):
   ```bash
   # Example: SAP references how-to guide that doesn't exist
   # Create minimal how-to following Diátaxis pattern

   # Template:
   # 1. Goal (what you'll accomplish)
   # 2. Prerequisites
   # 3. Steps with examples
   # 4. Validation
   # 5. Troubleshooting
   # 6. Next steps
   ```

4. **Create missing system files** (if critical):
   ```bash
   # Example: SAP-008 claims script exists but it doesn't
   # Create minimal viable script with:
   # - Usage documentation (comments)
   # - Basic functionality
   # - Error handling
   # - Link back to SAP in comments
   ```

5. **Update SAP awareness-guide with new references**:
   ```markdown
   ## Related Content

   **Developer Workflows**:
   - [Workflow Name](../../dev-docs/workflows/workflow-name.md) - Purpose

   **User Guides**:
   - [How-to Name](../../user-docs/how-to/how-to-name.md) - Purpose

   **System Files**:
   - `scripts/script-name.sh` - Purpose
   ```

6. **Re-run link checker after adding content**:
   ```bash
   ./scripts/validate-links.sh docs/skilled-awareness/[sap-name]/
   ```

**Deliverable**:
- New content files (dev-docs, user-docs, system files)
- Updated awareness-guide.md with cross-references
- Link validation passing (or only non-critical issues remain)

**Time Management**:
- Limit to 1-2 hours per SAP in this step
- If gaps require >2h, mark as "deferred to Phase 5" in gap report
- Focus on minimum viable content, not perfection

---

### Step 6: Enhance Awareness Guide (1 hour)

**Objective**: Make awareness-guide the definitive entry point with explicit cross-domain integration

**Tasks**:

1. **Add "Related Content" section** (if not present):
   ```markdown
   ## Related Content

   This SAP integrates with content across all 4 domains:

   ### Developer Process (dev-docs/)
   - [Workflow Name](../../dev-docs/workflows/name.md) - When to use this SAP in development
   - [Example Walkthrough](../../dev-docs/examples/name.md) - Step-by-step SAP usage

   ### Project Lifecycle (project-docs/)
   - [Integration Plan Template](../../project-docs/integration/template.md) - Planning SAP adoption
   - [Metrics Template](../../project-docs/metrics/template.md) - Measuring SAP impact

   ### Product Documentation (user-docs/)
   - [How-to Guide](../../user-docs/how-to/name.md) - End-user perspective
   - [Reference Spec](../../user-docs/reference/name.md) - Technical details

   ### System Files
   - `scripts/script-name.sh` - Automation tool for this SAP
   - `src/module/file.py` - Core implementation
   - `.github/workflows/ci.yml` - CI/CD integration
   ```

2. **Add concrete examples** (replace hypotheticals):
   ```markdown
   ## Example: [Concrete Scenario]

   **Context**: [Real situation from chora-base or known project]

   **Steps**:
   1. [Actual command or action]
   2. [Actual command or action]
   3. [Actual result]

   **Files involved**:
   - Input: [Actual file path]
   - Output: [Actual file path]
   - Reference: [Link to actual example]
   ```

3. **Add "Common Pitfalls" section** (if not present):
   ```markdown
   ## Common Pitfalls

   ### Pitfall 1: [Concrete mistake]
   **Symptom**: [What you'll see]
   **Cause**: [Why it happens]
   **Solution**: [How to fix]

   ### Pitfall 2: [Concrete mistake]
   ...
   ```

4. **Ensure 4-domain coverage**:
   - Verify awareness-guide references at least 2-3 domains
   - If SAP is domain-specific (e.g., SAP-007 for docs), acknowledge this
   - Add cross-references even if content is minimal (shows integration points)

5. **Add "When to Use This SAP" section** (if not present):
   ```markdown
   ## When to Use This SAP

   **Use this SAP when**:
   - [Specific scenario 1]
   - [Specific scenario 2]

   **Don't use this SAP when**:
   - [Anti-pattern 1]
   - [Anti-pattern 2]

   **Related SAPs**:
   - [SAP-XXX](../sap-xxx/) - For [related capability]
   ```

**Deliverable**: Enhanced awareness-guide.md with:
- Explicit cross-domain references
- Concrete examples
- Common pitfalls
- Clear usage guidance

---

## Audit Deliverables

For each SAP audited, produce:

1. **Gap Analysis Report** - Markdown table with critical/high/medium/low gaps
2. **Link Validation Report** - Output from link checker + categorized issues
3. **Content Completeness Checklist** - Pass/fail for each of 5 artifacts
4. **New Content Created** - List of files created during Step 5
5. **Enhanced Awareness Guide** - Updated awareness-guide.md with cross-domain references

**Tracking Matrix Update**:
Update the Wave 2 tracking matrix with:
- Audit status: Complete
- Gaps found: Count by priority
- Content created: File count
- Validated: ✅ (link checker passed)

---

## Quality Gates

**SAP audit is considered COMPLETE when**:
- [ ] All 5 artifacts read and analyzed
- [ ] Cross-domain gap analysis performed (4 domains checked)
- [ ] Link validation run (script output reviewed)
- [ ] Content completeness checklist filled (5 artifacts assessed)
- [ ] Critical gaps filled (all blocking issues resolved)
- [ ] Awareness-guide enhanced (cross-domain references added)
- [ ] Link validation passes (or only non-critical issues remain)
- [ ] Tracking matrix updated

**SAP audit is considered PASSING when**:
- [ ] Zero critical gaps remain (no broken internal links, no missing critical files)
- [ ] High-value gaps documented (for Phase 5 content creation)
- [ ] Awareness-guide references 2+ domains explicitly
- [ ] Examples are concrete (not hypothetical)
- [ ] All 5 artifacts have actionable content
- [ ] **Adoption blueprint includes post-install awareness enablement with validation commands**

---

## Batch Processing Strategy

For efficiency when auditing multiple SAPs:

### Infrastructure SAPs (Batch Together)
- SAP-003 (Project Bootstrap)
- SAP-005 (CI/CD Workflows)
- SAP-006 (Quality Gates)
- SAP-011 (Docker Operations)

**Why batch**: Similar context, shared infrastructure patterns

**Approach**:
1. Read all 4 SAP charters to understand scope overlap
2. Identify shared gaps (e.g., all need CI/CD examples)
3. Create shared content once, reference from all 4
4. Batch link validation across all 4

### Advanced Capabilities (Batch Together)
- SAP-009 (Agent Awareness)
- SAP-010 (Memory System)
- SAP-013 (Metrics Tracking)

**Why batch**: Conceptually related, may cross-reference each other

**Approach**:
1. Map dependencies between these SAPs
2. Ensure cross-SAP references are valid
3. Create examples that demonstrate integration

### Development Workflow SAPs (Batch Together)
- SAP-000 (SAP Framework)
- SAP-007 (Documentation Framework)
- SAP-012 (Development Lifecycle)

**Why batch**: All relate to development processes

**Approach**:
1. Ensure consistency in workflow patterns
2. Cross-reference related workflows
3. Validate process integration points

---

## Anti-Patterns to Avoid

### During Audit

❌ **Don't create excessive content in Step 5**
- **Why**: Scope creep, timeline risk
- **Instead**: Mark medium/low gaps for Phase 5 (Content Creation)

❌ **Don't skip link validation**
- **Why**: Manual link checking is error-prone and incomplete
- **Instead**: Always run automated link checker

❌ **Don't audit in isolation**
- **Why**: Miss cross-SAP integration opportunities
- **Instead**: Note related SAPs, check for cross-references

❌ **Don't fix cosmetic issues during audit**
- **Why**: Time sink, not critical for SAP usability
- **Instead**: Note for future polish, focus on functionality

❌ **Don't assume hypothetical examples are sufficient**
- **Why**: Less valuable than concrete, tested examples
- **Instead**: Replace with real examples from chora-base or known projects

❌ **Don't skip awareness hierarchy integration check**
- **Why**: Blocks discoverability of installed SAPs, critical usability issue
- **Instead**: Always validate post-install AGENTS.md/CLAUDE.md update steps (Step 4.5)

### In Gap Reports

❌ **Don't mark everything as "Critical"**
- **Why**: Dilutes priority, creates unrealistic expectations
- **Instead**: Reserve "Critical" for actual blockers (broken links, missing essential files)

❌ **Don't create vague gap descriptions**
- **Example**: ❌ "Needs more examples"
- **Instead**: ✅ "awareness-guide.md should include concrete example of SAP-004 TDD workflow with actual test file paths"

❌ **Don't propose large-scale rewrites**
- **Why**: Out of scope for audit phase
- **Instead**: Note specific improvements, defer comprehensive updates to dedicated SAP enhancement wave

---

## Integration with Wave 2 Phases

This workflow is used in:

**Phase 2: Tier 1 Audit (Days 4-7)**
- Apply to SAP-000, SAP-007, SAP-002, SAP-004
- Spend 4-6h per SAP (higher complexity)
- Establish audit pattern quality baseline

**Phase 3: Tier 2 Audit (Days 8-11)**
- Apply to SAP-001, SAP-012, SAP-008
- Spend 4-5h per SAP
- Refine audit process based on Tier 1 learnings

**Phase 4: Tier 3 Audit (Days 12-15)**
- Apply to remaining 7 SAPs
- Spend 3-4h per SAP (batch similar SAPs)
- Optimize for efficiency

**Phase 5: Content Creation (Days 16-18)**
- Address high/medium gaps from all audits
- Create missing dev-docs/, user-docs/, system files
- Prioritize based on cross-SAP impact

---

## Tools & Scripts

**Required**:
- `scripts/validate-links.sh` - Automated link checker (SAP-016)
- `scripts/inventory-chora-base.py` - Coherence validation

**Helpful**:
- `grep` - Finding cross-domain references
- `find` - Locating files
- Text editor with markdown preview
- Gap tracking spreadsheet or markdown table

**Future** (post-Wave 2):
- `scripts/audit-sap.sh` - Automated audit orchestration
- `scripts/generate-gap-report.sh` - Templated gap report creation

---

## Success Metrics

**For Wave 2**:
- 15 SAPs audited (SAP-016 + 14 existing)
- 100% link validation pass rate (or documented exceptions)
- 90%+ critical gaps filled
- Average 2.5+ domains referenced per SAP
- Zero broken internal links

**Per-SAP Quality Indicators**:
- Awareness-guide references ≥2 domains explicitly
- At least 1 concrete example (not hypothetical)
- All 5 artifacts have actionable content
- Zero critical gaps (broken links, missing essential files)

---

## Example Audit Report Template

```markdown
# SAP-XXX Audit Report

**SAP**: SAP-XXX (Name)
**Audited**: 2025-XX-XX
**Auditor**: Claude / [Name]
**Time Spent**: Xh

---

## Summary

**Overall Status**: ✅ PASS / ⚠️ NEEDS WORK / ❌ CRITICAL GAPS

**Key Findings**:
- [3-5 bullet points summarizing audit]

**Recommendation**:
- [Ready for use / Needs critical fixes / Requires major enhancement]

---

## Gap Analysis

### Critical Gaps (Must Fix)
- [ ] Gap description with file reference
- [ ] Gap description with file reference

### High-Value Gaps (Should Fix in Phase 5)
- [ ] Gap description
- [ ] Gap description

### Medium Gaps (Nice to Have)
- [ ] Gap description

### Low Priority Gaps (Defer)
- [ ] Gap description

---

## Link Validation

**Run**: `./scripts/validate-links.sh docs/skilled-awareness/sap-xxx/`

**Result**: ✅ PASS / ⚠️ MINOR ISSUES / ❌ BROKEN LINKS

**Broken Links Found**:
- awareness-guide.md:42 → ../dev-docs/foo.md (404) - CRITICAL
- protocol-spec.md:17 → https://example.com (404) - External, non-critical

---

## Content Completeness

| Artifact | Complete? | Issues |
|----------|-----------|--------|
| capability-charter.md | ✅ Yes | - |
| protocol-spec.md | ✅ Yes | - |
| awareness-guide.md | ⚠️ Partial | Missing concrete examples |
| adoption-blueprint.md | ✅ Yes | - |
| ledger.md | ✅ Yes | - |

---

## Cross-Domain Coverage

| Domain | Referenced? | Files |
|--------|-------------|-------|
| dev-docs/ | ✅ Yes | workflows/foo.md, examples/bar.md |
| project-docs/ | ❌ No | (Opportunity: link to metrics templates) |
| user-docs/ | ✅ Yes | how-to/baz.md |
| System files | ✅ Yes | scripts/qux.sh, src/module.py |

**Coverage Score**: 3/4 domains (75%)

---

## Awareness Hierarchy Integration

**Post-Install Section**: ✅ Present / ⚠️ Partial / ❌ Missing

**AGENTS.md Update Instructions**:
- Root AGENTS.md update step: ✅ Yes / ❌ No
- Content template provided: ✅ Yes / ❌ No
- Validation command included: ✅ Yes / ❌ No
- Instructions agent-executable: ✅ Yes / ⚠️ Needs improvement / ❌ No

**Domain-Specific AGENTS.md** (if applicable):
- Domain-specific files needed: ✅ Yes / ❌ No
- Instructions included: ✅ Yes / ❌ No / N/A

**CLAUDE.md References** (if applicable):
- Mentioned or conditional: ✅ Yes / ❌ No / N/A

**Quality Assessment**:
- Overall: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL
- Priority gaps: [List any critical/high gaps]

**Example Finding**:
```
✅ PASS - SAP-000 includes complete AGENTS.md update in Step 6 with:
  - Clear agent-executable instructions (use Edit tool)
  - Concrete content template
  - Validation command (grep check)
  - Reference to SAP Framework section
```

---

## Content Created

**New Files**:
- docs/dev-docs/workflows/foo-workflow.md (critical gap fill)
- docs/user-docs/how-to/bar-guide.md (high-value gap fill)

**Enhanced Files**:
- docs/skilled-awareness/sap-xxx/awareness-guide.md (added Related Content section)

---

## Recommendations

**For Phase 5 (Content Creation)**:
1. Create project-docs/metrics example for this SAP
2. Add 2-3 more concrete examples to awareness-guide
3. Expand adoption-blueprint with troubleshooting section

**For Future Enhancement**:
- Consider creating visualization diagram
- Could add advanced usage patterns

---

## Tracking Matrix Update

| SAP ID | Status | Gaps Found | Content Created | Validated |
|--------|--------|------------|-----------------|-----------|
| SAP-XXX | ✅ Complete | 2 critical, 3 high, 4 medium | 2 files | ✅ |
```

---

## Workflow Versioning

**Version 1.0 (2025-10-28)**:
- Initial workflow for Wave 2
- 6-step audit pattern
- Integration with link validation (SAP-016)
- Batch processing strategy

**Future Enhancements**:
- Automated audit script (post-Wave 2)
- Gap report templates (integrated tooling)
- Cross-SAP dependency checking (advanced)
- External adoption validation (multi-project)

---

## Related Documentation

**Workflows**:
- [DOCUMENTATION_MIGRATION_WORKFLOW.md](DOCUMENTATION_MIGRATION_WORKFLOW.md) - File migration process
- [Link Validation Workflow](../../skilled-awareness/link-validation-reference-management/awareness-guide.md) - SAP-016 (to be created)

**Project Lifecycle**:
- [Wave 2 Sprint Plan](../../project-docs/sprints/wave-2-sprint-plan.md) - Where this workflow is used
- [Wave 1 SAP Opportunities](../research/wave-1-sap-opportunities.md) - Why SAP audits are needed

**SAP Framework**:
- [SAP-000 Awareness Guide](../../skilled-awareness/sap-framework/awareness-guide.md) - Understanding SAP structure
- [SAP Document Templates](../../skilled-awareness/document-templates.md) - SAP artifact templates

---

**Workflow Version**: 1.0
**Created**: 2025-10-28 (Wave 2, Phase 1)
**Owner**: chora-base development team
**Status**: Active

This workflow demonstrates chora-base's dev-docs/ domain: developer process documentation for systematic SAP quality assurance.
