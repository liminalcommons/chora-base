# Week 4 Verification Plan: SAP-007 & SAP-009

**Date Created**: 2025-11-09
**Target Week**: Week 4
**SAPs**: SAP-007 (documentation-framework), SAP-009 (agent-awareness)
**Verification Method**: Incremental adoption on Week 3 generated project
**Estimated Duration**: 4 hours

---

## Executive Summary

Week 4 continues Tier 1 (Core Infrastructure) verification by testing SAP-007 and SAP-009 via incremental adoption. Both SAPs are categorized as **Incremental SAPs** (not included in fast-setup by design), so we'll adopt them on the Week 3 generated project.

**Key Insight from Week 3**: SAP categorization framework discovered - match verification method to SAP category.

---

## SAP Categorization

### SAP-007: Documentation Framework
- **Category**: Incremental SAP
- **Included by Default**: `false` (confirmed in sap-catalog.json)
- **Current Version**: 1.1.0
- **Verification Method**: Incremental adoption (add Diataxis structure to existing project)

### SAP-009: Agent Awareness
- **Category**: Incremental SAP
- **Included by Default**: `false` (confirmed in sap-catalog.json)
- **Current Version**: 1.1.0
- **Verification Method**: Incremental adoption (add AGENTS.md/CLAUDE.md to existing project)

---

## Week 4 Goals

### Primary Goals
1. ✅ Verify SAP-007 L1 criteria (Diataxis structure adoption)
2. ✅ Verify SAP-009 L1 criteria (AGENTS.md/CLAUDE.md adoption)
3. ✅ Document incremental adoption workflow for both SAPs
4. ✅ Achieve GO or CONDITIONAL GO decisions for both SAPs

### Secondary Goals
1. Cross-validate SAP-007 and SAP-009 (documentation patterns consistency)
2. Test SAP synergy: Does SAP-009 reference SAP-007 documentation?
3. Update comprehensive plan with Week 4 results
4. Reach 29% overall progress (9/31 SAPs)

---

## Verification Approach

### Pre-Flight Checks

Before starting verification:

1. **Confirm SAP Categorization**:
   ```bash
   # Check SAP-007 inclusion
   python -c "import json; cat = json.load(open('sap-catalog.json')); print([s for s in cat['saps'] if s['id'] == 'SAP-007'][0]['included_by_default'])"
   # Expected: False

   # Check SAP-009 inclusion
   python -c "import json; cat = json.load(open('sap-catalog.json')); print([s for s in cat['saps'] if s['id'] == 'SAP-009'][0]['included_by_default'])"
   # Expected: False
   ```

2. **Verify Week 3 Project Exists**:
   ```bash
   ls -la docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project/
   # Should contain: README.md, pyproject.toml, src/, tests/, .github/workflows/, etc.
   ```

3. **Confirm SAP Dependencies**:
   - SAP-007 depends on: SAP-000 (sap-framework) ✅
   - SAP-009 depends on: SAP-000 (sap-framework) ✅
   - Both dependencies verified in Week 1

---

## Day 1: SAP-007 (Documentation Framework)

**Duration**: 2 hours
**Target**: CONDITIONAL GO or GO

### L1 Criteria (from adoption-blueprint.md)

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| Diataxis structure exists | `docs/user-docs/{tutorial,how-to,reference,explanation}/` | Directory listing |
| ≥1 document in each category | ≥4 total docs | File count |
| Frontmatter schema present | YAML frontmatter in all docs | Manual inspection |
| Documentation standard | DOCUMENTATION_STANDARD.md exists | File exists check |

### Step-by-Step Verification

**Step 1: Review SAP-007 Adoption Blueprint** (10 min)
```bash
# Read adoption blueprint to understand requirements
cat docs/skilled-awareness/documentation-framework/adoption-blueprint.md

# Identify L1 criteria and incremental adoption workflow
```

**Step 2: Create Diataxis Structure** (20 min)
```bash
cd docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project/

# Create Diataxis directories
mkdir -p docs/user-docs/{tutorial,how-to,reference,explanation}

# Verify structure
ls -la docs/user-docs/
```

**Step 3: Copy DOCUMENTATION_STANDARD.md** (5 min)
```bash
# Copy from static-template
cp c:/Users/victo/code/chora-base/static-template/DOCUMENTATION_STANDARD.md \
   docs/user-docs/DOCUMENTATION_STANDARD.md

# Verify
cat docs/user-docs/DOCUMENTATION_STANDARD.md | head -20
```

**Step 4: Create Sample Documents** (40 min)

Create at least one document in each Diataxis category:

1. **Tutorial**: `docs/user-docs/tutorial/getting-started.md`
   - Goal: Guide user through first tool call
   - Include: Step-by-step instructions with expected outputs
   - Frontmatter: `type: tutorial`, `last_updated`, `version`

2. **How-To**: `docs/user-docs/how-to/create-task.md`
   - Goal: Show how to create a task using MCP tool
   - Include: Prerequisites, steps, troubleshooting
   - Frontmatter: `type: how-to`, `last_updated`, `test_extraction: true`

3. **Reference**: `docs/user-docs/reference/mcp-tools.md`
   - Goal: List all MCP tools with signatures
   - Include: Tool names, parameters, return types
   - Frontmatter: `type: reference`, `last_updated`

4. **Explanation**: `docs/user-docs/explanation/architecture.md`
   - Goal: Explain high-level architecture
   - Include: System design, components, rationale
   - Frontmatter: `type: explanation`, `last_updated`

**Step 5: Verify L1 Criteria** (15 min)
```bash
# Check directories exist
test -d docs/user-docs/tutorial && echo "✅ tutorial/" || echo "❌ tutorial/"
test -d docs/user-docs/how-to && echo "✅ how-to/" || echo "❌ how-to/"
test -d docs/user-docs/reference && echo "✅ reference/" || echo "❌ reference/"
test -d docs/user-docs/explanation && echo "✅ explanation/" || echo "❌ explanation/"

# Count documents (≥1 per category)
find docs/user-docs/tutorial -name "*.md" | wc -l   # Should be ≥1
find docs/user-docs/how-to -name "*.md" | wc -l     # Should be ≥1
find docs/user-docs/reference -name "*.md" | wc -l  # Should be ≥1
find docs/user-docs/explanation -name "*.md" | wc -l # Should be ≥1

# Verify frontmatter (manual check)
head -10 docs/user-docs/tutorial/getting-started.md
head -10 docs/user-docs/how-to/create-task.md
head -10 docs/user-docs/reference/mcp-tools.md
head -10 docs/user-docs/explanation/architecture.md

# Check DOCUMENTATION_STANDARD.md exists
test -f docs/user-docs/DOCUMENTATION_STANDARD.md && echo "✅ DOCUMENTATION_STANDARD.md" || echo "❌ DOCUMENTATION_STANDARD.md"
```

**Step 6: Document Results** (30 min)
```bash
# Create verification report
# File: docs/project-docs/verification/verification-runs/2025-11-09-week4-sap-007-009/SAP-007-VERIFICATION.md

# Include:
# - L1 criteria verification table
# - Directory structure listing
# - Sample frontmatter from each doc type
# - Decision (GO/CONDITIONAL GO/NO-GO)
# - Time taken
# - Blockers (if any)
```

### Expected Decision

**Best Case**: GO ✅
- All 4 L1 criteria met
- Documents have valid frontmatter
- Diataxis structure adopted successfully

**Acceptable**: CONDITIONAL GO ⚠️
- 3/4 criteria met (one category missing document)
- Frontmatter incomplete but present
- Structure exists, needs content

**Worst Case**: NO-GO ❌
- <3 criteria met
- Major blockers preventing adoption

---

## Day 2: SAP-009 (Agent Awareness)

**Duration**: 2 hours
**Target**: CONDITIONAL GO or GO

### L1 Criteria (from adoption-blueprint.md)

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| Root AGENTS.md exists | File exists with ≥100 lines | File check + line count |
| Root CLAUDE.md exists | File exists with ≥50 lines | File check + line count |
| Progressive loading phases documented | 3 phases in AGENTS.md | Manual inspection |
| Tool awareness section | Tool names + descriptions | Manual inspection |

### Step-by-Step Verification

**Step 1: Review SAP-009 Adoption Blueprint** (10 min)
```bash
# Read adoption blueprint
cat docs/skilled-awareness/agent-awareness/adoption-blueprint.md

# Identify L1 criteria and incremental adoption workflow
```

**Step 2: Copy AGENTS.md Template** (20 min)
```bash
cd docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project/

# Copy from static-template
cp c:/Users/victo/code/chora-base/static-template/AGENTS.md AGENTS.md

# Customize for project (replace placeholders)
# - Project name: "Week 3 CI/CD Quality Verification"
# - Namespace: "week3cicd"
# - Tool names: example_tool, hello_world
# - Resources: capabilities
```

**Step 3: Copy CLAUDE.md Template** (15 min)
```bash
# Copy from static-template
cp c:/Users/victo/code/chora-base/static-template/CLAUDE.md CLAUDE.md

# Customize for project
# - Project-specific context
# - File structure
# - Development guidelines
```

**Step 4: Add Progressive Loading Phases to AGENTS.md** (30 min)

Ensure AGENTS.md contains all 3 phases:

1. **Phase 1: Immediate Context** (<3k tokens)
   - Project overview
   - Key constraints
   - Tool inventory

2. **Phase 2: Development Context** (3k-10k tokens)
   - File structure
   - Architecture
   - Common patterns

3. **Phase 3: Deep Context** (10k+ tokens)
   - Implementation details
   - Edge cases
   - Historical decisions

**Step 5: Add Tool Awareness Section** (20 min)

Document all MCP tools in AGENTS.md:
```markdown
## Tool Awareness

### week3cicd:example_tool
**Purpose**: Example tool demonstrating namespace pattern
**Parameters**: None
**Returns**: Success message

### week3cicd:hello_world
**Purpose**: Simple greeting tool
**Parameters**: None
**Returns**: "Hello, World!"
```

**Step 6: Verify L1 Criteria** (15 min)
```bash
# Check AGENTS.md exists and has ≥100 lines
test -f AGENTS.md && echo "✅ AGENTS.md exists" || echo "❌ AGENTS.md missing"
wc -l AGENTS.md  # Should be ≥100

# Check CLAUDE.md exists and has ≥50 lines
test -f CLAUDE.md && echo "✅ CLAUDE.md exists" || echo "❌ CLAUDE.md missing"
wc -l CLAUDE.md  # Should be ≥50

# Verify progressive loading phases (manual check)
grep -n "Phase 1" AGENTS.md
grep -n "Phase 2" AGENTS.md
grep -n "Phase 3" AGENTS.md

# Verify tool awareness section (manual check)
grep -n "Tool Awareness" AGENTS.md
grep -n "week3cicd:" AGENTS.md
```

**Step 7: Document Results** (30 min)
```bash
# Create verification report
# File: docs/project-docs/verification/verification-runs/2025-11-09-week4-sap-007-009/SAP-009-VERIFICATION.md

# Include:
# - L1 criteria verification table
# - AGENTS.md line count
# - CLAUDE.md line count
# - Progressive loading phases listing
# - Tool awareness section excerpt
# - Decision (GO/CONDITIONAL GO/NO-GO)
# - Time taken
# - Blockers (if any)
```

### Expected Decision

**Best Case**: GO ✅
- All 4 L1 criteria met
- AGENTS.md ≥100 lines with 3 phases
- CLAUDE.md ≥50 lines
- Tool awareness section complete

**Acceptable**: CONDITIONAL GO ⚠️
- 3/4 criteria met
- Files exist but need content refinement
- Phases documented but incomplete

**Worst Case**: NO-GO ❌
- <3 criteria met
- Major blockers preventing adoption

---

## Cross-Validation Opportunities

### SAP-007 ↔ SAP-009 Integration

**Test**: Does AGENTS.md reference Diataxis documentation?

Expected:
- AGENTS.md should mention `docs/user-docs/` structure
- AGENTS.md should point to specific how-to guides
- Progressive loading Phase 2 should reference documentation

**Verification**:
```bash
# Check if AGENTS.md mentions docs/user-docs/
grep "docs/user-docs" AGENTS.md

# Check if AGENTS.md references specific docs
grep -E "(tutorial|how-to|reference|explanation)" AGENTS.md
```

If cross-validation succeeds:
- ✅ Confirms both SAPs integrate correctly
- ✅ Demonstrates real-world SAP synergy
- ✅ Validates SAP-007 + SAP-009 design

---

## Risk Assessment

### Known Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Template customization errors | Medium | Medium | Use static-template/ as reference, test placeholders |
| Frontmatter schema mismatch | Low | Low | Copy from existing chora-base docs |
| Progressive loading phases incomplete | Low | Medium | Use chora-base AGENTS.md as example |
| Time overrun (>4h) | Medium | Low | Prioritize L1 criteria, defer L2/L3 |

### Contingency Plans

**If SAP-007 NO-GO**:
- Investigate template issues
- Check static-template/ for correct files
- Document blockers, defer to Week 5

**If SAP-009 NO-GO**:
- Review AGENTS.md template
- Check namespace pattern correctness
- Document blockers, defer to Week 5

**If Both NO-GO**:
- Re-evaluate Week 3 project as verification base
- Consider re-generating project with fixes
- Escalate timeline concerns

---

## Success Criteria

### Week 4 Success Indicators

1. **Both SAPs Verified**: SAP-007 and SAP-009 decisions made
2. **≥1 GO Decision**: At least one full GO (not just CONDITIONAL)
3. **≤4 Hours Total**: Stay within estimated time
4. **0 Critical Blockers**: No unresolvable issues
5. **Cross-Validation Tested**: SAP-007 ↔ SAP-009 integration checked

### Campaign Progress Targets

- **Progress**: 29% (9/31 SAPs)
- **Tier 1**: 78% (7/9 SAPs)
- **GO Decision Rate**: ≥90% (maintain 100% if possible)
- **Time Efficiency**: Within ±20% of estimate

---

## Deliverables

### Required Deliverables

1. **SAP-007-VERIFICATION.md**
   - L1 criteria verification table
   - Diataxis structure listing
   - Sample frontmatter
   - Decision + rationale

2. **SAP-009-VERIFICATION.md**
   - L1 criteria verification table
   - AGENTS.md/CLAUDE.md line counts
   - Progressive loading phases
   - Decision + rationale

3. **WEEK_4_REPORT.md**
   - Executive summary
   - Both SAPs' results
   - Cross-validation findings
   - Time breakdown
   - Next steps

4. **Updated PROGRESS_SUMMARY.md**
   - Reflect 29% completion (9/31 SAPs)
   - Update Tier 1 progress to 78%
   - Add Week 4 to completed weeks

---

## Timeline

### Week 4 Schedule

**Day 1 (2h)**: SAP-007 Verification
- 0:00-0:10 - Review adoption blueprint
- 0:10-0:30 - Create Diataxis structure
- 0:30-0:35 - Copy DOCUMENTATION_STANDARD.md
- 0:35-1:15 - Create sample documents (4 docs)
- 1:15-1:30 - Verify L1 criteria
- 1:30-2:00 - Document results

**Day 2 (2h)**: SAP-009 Verification
- 0:00-0:10 - Review adoption blueprint
- 0:10-0:30 - Copy & customize AGENTS.md
- 0:30-0:45 - Copy & customize CLAUDE.md
- 0:45-1:15 - Add progressive loading phases
- 1:15-1:35 - Add tool awareness section
- 1:35-1:50 - Verify L1 criteria
- 1:50-2:00 - Document results

**Post-Verification (1h)**: Reporting
- Generate Week 4 comprehensive report
- Update PROGRESS_SUMMARY.md
- Test cross-validation
- Prepare for Week 5

---

## Next Steps After Week 4

### Immediate (Post-Week 4)
1. Generate Week 4 comprehensive report
2. Update PROGRESS_SUMMARY.md to 29%
3. Review Week 5 plan (SAP-008, SAP-012)

### Short-Term (Week 5)
1. Verify SAP-008 (automation-scripts)
2. Verify SAP-012 (development-lifecycle)
3. Complete Tier 1 verification (89%, 8/9 SAPs)

### Medium-Term (Weeks 6-11)
- Continue with Tier 2-5 SAPs
- Maintain ≥90% GO decision rate
- Complete by Week 11

---

## Related Documents

- [COMPREHENSIVE_SAP_VERIFICATION_PLAN.md](../COMPREHENSIVE_SAP_VERIFICATION_PLAN.md)
- [PROGRESS_SUMMARY.md](../PROGRESS_SUMMARY.md)
- [WEEK_3_REPORT.md](verification-runs/2025-11-09-week3-sap-005-006/WEEK_3_REPORT.md)
- [SAP-007 Adoption Blueprint](../../skilled-awareness/documentation-framework/adoption-blueprint.md)
- [SAP-009 Adoption Blueprint](../../skilled-awareness/agent-awareness/adoption-blueprint.md)

---

**Plan Created**: 2025-11-09
**Target Execution**: Week 4
**Status**: ✅ READY FOR EXECUTION
