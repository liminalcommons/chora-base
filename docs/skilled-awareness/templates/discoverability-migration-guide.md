# Discoverability Migration Guide

**Version**: 1.0.0
**Last Updated**: 2025-11-09
**For**: SAP authors migrating existing SAPs to discoverability L1 requirement

---

## Overview

This guide helps SAP authors add discoverability to existing SAPs to meet the new L1 requirement (≥80/100 discoverability score).

**Target audience**: SAP authors with existing SAPs at L1 or higher
**Time estimate**: 3-5 hours per SAP
**Prerequisites**: SAP already implemented and documented (5 artifacts complete)

---

## Why Migrate?

**Problem**: Existing SAPs may have excellent implementation but poor discoverability, creating a "meta-discoverability paradox" where sophisticated patterns become liabilities.

**Solution**: Add discoverability touchpoints to root awareness files (README.md, AGENTS.md, CLAUDE.md, justfile) to reduce discovery time from 15-20 minutes to <5 minutes.

**Expected ROI**:
- Discovery time: 15-20 min → 2-5 min (75% reduction)
- Discovery-to-value ratio: 0.6 → 6.0+ (10x improvement)
- Time-to-adoption: Days → Hours (3-5x faster)

---

## Discoverability Scoring Framework

**Total**: 100 points across 6 touchpoints

| Touchpoint | Points | Target | Purpose |
|------------|--------|--------|---------|
| README.md | 30 | ≥30 lines | First discovery point for all users |
| AGENTS.md | 20 | ≥60 lines | Detailed patterns for generic agents |
| CLAUDE.md | 15 | Domain section | Claude-specific navigation |
| justfile | 15 | ≥3 recipes | CLI automation for common tasks |
| Documentation | 10 | Links to 5 artifacts | Reference completeness |
| Examples | 10 | ≥2 workflows | Practical usage patterns |

**L1 requirement**: ≥80/100
**Advanced patterns (SAP-009)**: ≥85/100 (higher bar for meta-capabilities)

---

## Migration Workflow

### Step 1: Audit Current Discoverability (15 minutes)

Run discoverability audit (once SAP-019 v1.1.0 is implemented):

```bash
# Future: Automated audit via SAP-019
python scripts/sap-evaluator.py --discoverability SAP-XXX

# Current: Manual audit
grep -A 40 "SAP-XXX" README.md | wc -l     # Target: ≥30
grep -A 70 "SAP-XXX" AGENTS.md | wc -l     # Target: ≥60
grep -i "SAP-XXX" CLAUDE.md                # Check if domain section exists
grep -i "SAP-XXX" justfile | grep "^[a-z]" | wc -l  # Target: ≥3
```

**Example output**:
```
README.md: 0 lines (0/30 points) ❌
AGENTS.md: 15 lines (10/20 points) ⚠️
CLAUDE.md: No section (0/15 points) ❌
justfile: 0 recipes (0/15 points) ❌
Documentation: 5 artifacts (10/10 points) ✅
Examples: 2 workflows (10/10 points) ✅

Total: 30/100 (LOW)
```

---

### Step 2: Add README.md Section (60 minutes)

**Goal**: 30/30 points (≥30 lines)

**Template**: See [SAP-010 README.md:321-366](../../README.md#L321-L366) or [SAP-015 README.md:367-424](../../README.md#L367-L424) for examples

**Structure**:
```markdown
### [SAP Name] - SAP-XXX

**Status**: [production|pilot|draft] (vX.Y.Z) | **Adoption Level**: LX

[2-3 sentence description of what the SAP provides and its value proposition]

**When to use SAP-XXX**:
- [Use case 1 with concrete scenario]
- [Use case 2 with concrete scenario]
- [Use case 3 with concrete scenario]
- [Use case 4 with concrete scenario]
- [Use case 5 with concrete scenario]

**Quick start**:
```bash
# [Most common workflow with 3-5 commands]
# Include inline comments explaining each step
# Show both programmatic (--json) and human-readable outputs
```

**Core workflows**:
- **[Workflow 1]**: [Description] → [Outcome]
- **[Workflow 2]**: [Description] → [Outcome]
- **[Workflow 3]**: [Description] → [Outcome]

**Integration with other SAPs**:
- **SAP-XXX ([Name])**: [How they integrate]
- **SAP-YYY ([Name])**: [How they integrate]

**ROI**: [Quantified time savings per session/year]

**Documentation**:
- Protocol specification: [Link to protocol-spec.md]
- Adoption blueprint: [Link to adoption-blueprint.md]
- CLI reference: [Command or link to docs]

**CLI recipes** (see justfile):
```bash
just sap-xxx-command-1    # Description
just sap-xxx-command-2    # Description
just sap-xxx-command-3    # Description
```

---
```

**Validation**:
```bash
# Count lines (should be ≥30)
grep -n "### [SAP Name] - SAP-XXX" README.md -A 60 | wc -l

# Expected: 30-60 lines (30/30 points)
```

---

### Step 3: Add AGENTS.md Section (90 minutes)

**Goal**: 20/20 points (≥60 lines)

**Template**: See [SAP-010 AGENTS.md:822-903](../../AGENTS.md#L822-L903) or [SAP-015 AGENTS.md:906-1053](../../AGENTS.md#L906-L1053) for examples

**Structure**:
```markdown
## [SAP Name] - SAP-XXX

**Status**: [production|pilot|draft] (vX.Y.Z) | **Adoption Level**: LX

[2-3 sentence description of the SAP]

**Quick-start approach**:
```bash
# If SAP has nested AGENTS.md/CLAUDE.md (SAP-009 pattern)
cd [domain]/
cat AGENTS.md  # [X-min read]
cat CLAUDE.md  # [Y-min read]

# Alternative: Read full protocol specification
cat docs/skilled-awareness/[sap-name]/protocol-spec.md  # [Z-min read]
```

**When to use SAP-XXX**:
- **[Scenario 1]**: [Description] ([time savings])
- **[Scenario 2]**: [Description] ([time savings])
- **[Scenario 3]**: [Description] ([time savings])

**Core CLI commands**:
```bash
# [Command category 1]
[command 1] [flags]  # Description
[command 2] [flags]  # Description

# [Command category 2]
[command 3] [flags]  # Description
[command 4] [flags]  # Description
```

**Example workflow ([use case])**:
```bash
# Step 1: [Description]
[command 1]

# Step 2: [Description]
[command 2]

# Step 3: [Description]
[command 3]

# Result: [Outcome]
```

**[Data structure or key concept]**:
```json
{
  "[key]": "[value]",
  "[key]": "[value]"
}
```

**Integration with other SAPs**:
- **SAP-XXX ([Name])**: [Integration pattern]
  ```bash
  # [Example integration workflow]
  ```

- **SAP-YYY ([Name])**: [Integration pattern]
  ```bash
  # [Example integration workflow]
  ```

**Nested awareness guides** (if using SAP-009):
- [[domain]/AGENTS.md]([domain]/AGENTS.md) - [Description] ([X-min read, ~Xk tokens])
- [[domain]/CLAUDE.md]([domain]/CLAUDE.md) - [Description] ([Y-min read, ~Yk tokens])
- **Progressive loading**: Load only what you need (60-70% token savings)

**Documentation**:
- Protocol specification: [Link to protocol-spec.md]
- Adoption blueprint: [Link to adoption-blueprint.md]
- CLI reference: [Command or link]

**ROI**: [Quantified time savings]

**Note**: [Any important notes about adoption, prerequisites, or caveats]

---
```

**Validation**:
```bash
# Count lines (should be ≥60)
grep -n "## [SAP Name] - SAP-XXX" AGENTS.md -A 90 | wc -l

# Expected: 60-150 lines (20/20 points)
```

---

### Step 4: Add CLAUDE.md Domain Section (30 minutes)

**Goal**: 15/15 points (domain navigation section)

**Template**: See [SAP-010 CLAUDE.md:257-280](../../CLAUDE.md#L257-L280) or [SAP-015 CLAUDE.md:283-306](../../CLAUDE.md#L283-L306) for examples

**Structure**:
```markdown
### Domain X: [SAP Name] ([directory]/)

**Path**: [[directory]/AGENTS.md]([directory]/AGENTS.md) + [[directory]/CLAUDE.md]([directory]/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [[directory]/CLAUDE.md]([directory]/CLAUDE.md) - [Description] ([X-min, ~Xk tokens])
- [[directory]/AGENTS.md]([directory]/AGENTS.md) - [Description] ([Y-min, ~Yk tokens])

**Use when**:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**Contents**:
- [Key content 1]
- [Key content 2]
- [Key content 3]

**Note**: [Any important notes about when this domain exists or doesn't exist]

---
```

**Where to add**:
- Add after existing domain sections (Domain 1-6)
- Use sequential numbering (Domain 7, 8, etc.)
- Maintain alphabetical or logical ordering

**Validation**:
```bash
# Check if section exists and has proper structure
grep -A 20 "### Domain X:" CLAUDE.md

# Expected: 20-25 lines with navigation links
```

---

### Step 5: Add justfile Recipes (45 minutes)

**Goal**: 15/15 points (≥3 recipes, target 5-10)

**Template**: See [SAP-010 justfile:99-152](../../justfile#L99-L152) or [SAP-015 justfile:154-208](../../justfile#L154-L208) for examples

**Structure**:
```bash
# ============================================================================
# SAP-XXX: [SAP Name]
# ============================================================================
# [2-3 line description of SAP purpose]
# See: [AGENTS.md section reference]

# [Recipe 1 description]
# Example: just sap-xxx-command-1 [args]
sap-xxx-command-1 ARG="default":
    @[command implementation]

# [Recipe 2 description]
# Example: just sap-xxx-command-2 [args]
sap-xxx-command-2 ARG:
    @[command implementation]

# [Recipe 3 description]
# Example: just sap-xxx-command-3
sap-xxx-command-3:
    @[command implementation]

# [Recipe 4 description] (optional)
# Example: just sap-xxx-command-4 [args]
sap-xxx-command-4:
    @[command implementation]

# [Recipe 5 description] (optional)
# Example: just sap-xxx-command-5
sap-xxx-command-5:
    @[command implementation]
```

**Recipe naming conventions**:
- Use `sap-name-action` pattern (e.g., `beads-ready`, `memory-events`)
- Include `--help` examples in comments
- Provide default values for optional arguments
- Use `@` prefix to suppress command echo (cleaner output)
- Handle missing files/directories gracefully with `|| echo "..."`

**Recipe categories** (aim for 5-10 recipes covering):
1. **Query/List**: Show status, list items
2. **Create**: Create new items
3. **Update**: Modify existing items
4. **Search**: Find items by criteria
5. **Stats**: Show statistics or summaries

**Validation**:
```bash
# Count recipes (should be ≥3)
grep -A 50 "# SAP-XXX:" justfile | grep "^[a-z]" | wc -l

# Expected: 3-10 recipes (15/15 points if ≥3)
```

---

### Step 6: Validate Documentation & Examples (15 minutes)

**Goal**: 20/20 points (10 for docs + 10 for examples)

**Documentation validation** (10/10 points):
```bash
# Check all 5 artifacts exist
ls docs/skilled-awareness/[sap-name]/capability-charter.md
ls docs/skilled-awareness/[sap-name]/protocol-spec.md
ls docs/skilled-awareness/[sap-name]/awareness-guide.md  # or AGENTS.md
ls docs/skilled-awareness/[sap-name]/adoption-blueprint.md
ls docs/skilled-awareness/[sap-name]/ledger.md

# Verify links in README.md and AGENTS.md sections point to these files
grep "docs/skilled-awareness/[sap-name]/" README.md AGENTS.md
```

**Examples validation** (10/10 points):
- Check protocol-spec.md has ≥2 workflow examples
- Check AGENTS.md section has ≥1 detailed example
- Verify examples are concrete and runnable

**If missing**:
- Documentation: Add missing artifacts (follow SAP-000 structure)
- Examples: Add workflow examples to protocol-spec.md Section 4

---

### Step 7: Calculate Final Score & Validate (15 minutes)

**Scorecard**:
```bash
# README.md
LINES_README=$(grep -A 40 "SAP-XXX" README.md | wc -l)
SCORE_README=$((LINES_README >= 30 ? 30 : LINES_README))

# AGENTS.md
LINES_AGENTS=$(grep -A 90 "SAP-XXX" AGENTS.md | wc -l)
SCORE_AGENTS=$((LINES_AGENTS >= 60 ? 20 : LINES_AGENTS / 3))

# CLAUDE.md
HAS_CLAUDE=$(grep -i "SAP-XXX" CLAUDE.md | wc -l)
SCORE_CLAUDE=$((HAS_CLAUDE > 0 ? 15 : 0))

# justfile
RECIPES=$(grep -A 50 "SAP-XXX" justfile | grep "^[a-z]" | wc -l)
SCORE_JUSTFILE=$((RECIPES >= 3 ? 15 : RECIPES * 5))

# Documentation (manual check)
SCORE_DOCS=10  # If all 5 artifacts exist

# Examples (manual check)
SCORE_EXAMPLES=10  # If ≥2 workflow examples

# Total
TOTAL=$((SCORE_README + SCORE_AGENTS + SCORE_CLAUDE + SCORE_JUSTFILE + SCORE_DOCS + SCORE_EXAMPLES))

echo "Discoverability Score: $TOTAL/100"
if [ $TOTAL -ge 80 ]; then
  echo "Status: ✅ Meets L1 requirement (≥80/100)"
else
  echo "Status: ❌ Does not meet L1 requirement (need $((80 - TOTAL)) more points)"
fi
```

**Validation checklist**:
- [ ] README.md section ≥30 lines (30/30 points)
- [ ] AGENTS.md section ≥60 lines (20/20 points)
- [ ] CLAUDE.md domain section exists (15/15 points)
- [ ] justfile has ≥3 recipes (15/15 points)
- [ ] All 5 SAP artifacts exist (10/10 points)
- [ ] ≥2 workflow examples (10/10 points)
- [ ] Total score ≥80/100

---

## Common Pitfalls

### Pitfall 1: Incomplete README.md Section

**Problem**: Section is too brief (<30 lines), missing use cases or workflows

**Fix**: Use template structure, include 5 use cases, quick start, and integration patterns

---

### Pitfall 2: Generic AGENTS.md Section

**Problem**: Section lacks detailed examples, just repeats README.md content

**Fix**: Add detailed workflow examples, data structures, integration patterns, and command references

---

### Pitfall 3: Missing CLAUDE.md Section

**Problem**: No domain navigation section for Claude

**Fix**: Add domain section with navigation tips and progressive loading guidance

---

### Pitfall 4: Too Few justfile Recipes

**Problem**: Only 1-2 recipes, missing common workflows

**Fix**: Aim for 5-10 recipes covering query, create, update, search, and stats operations

---

### Pitfall 5: Broken Links

**Problem**: Links in README.md/AGENTS.md point to non-existent files

**Fix**: Validate all links point to existing documentation files

```bash
# Validate links
bash scripts/validate-awareness-links.sh
```

---

## Batch Migration Strategy

**For multiple SAPs** (e.g., migrating 10+ SAPs):

### Option 1: Incremental Migration (Recommended)

**Week 1**: Migrate core SAPs (SAP-000, SAP-001, SAP-009, SAP-010, SAP-015)
**Week 2**: Migrate CI/CD SAPs (SAP-005, SAP-011, SAP-014)
**Week 3**: Migrate domain SAPs (React, testing, etc.)
**Week 4**: Validate all migrations, update catalog

**Rationale**: Core SAPs have highest usage, deliver ROI fastest

---

### Option 2: Automated Migration (Future)

**Script-based migration** (future enhancement to SAP-029):
```bash
# Generate discoverability sections from SAP metadata
python scripts/generate-sap.py SAP-XXX --add-discoverability

# Preview changes
python scripts/generate-sap.py SAP-XXX --add-discoverability --dry-run

# Batch migrate all SAPs
python scripts/batch-add-discoverability.py --all
```

**Prerequisites**: SAP-029 enhancement to support discoverability generation

---

## Example Migrations

### SAP-010 (Memory System)

**Before**: 40/100 (LOW)
- README.md: 0 lines (0/30)
- AGENTS.md: 15 lines (10/20)
- CLAUDE.md: No section (0/15)
- justfile: 0 recipes (0/15)

**After**: 80/100 (HIGH)
- README.md: 51 lines (30/30) ✅
- AGENTS.md: 86 lines (20/20) ✅
- CLAUDE.md: Domain 5 (15/15) ✅
- justfile: 9 recipes (15/15) ✅

**Time**: 4 hours
**Impact**: Discovery time 15-20 min → 2-5 min (75% reduction)

---

### SAP-015 (Task Tracking)

**Before**: Minimal discoverability
- README.md: 0 lines (0/30)
- AGENTS.md: Brief mention (5/20)
- CLAUDE.md: Brief mention (5/15)
- justfile: 0 recipes (0/15)

**After**: 100/100 (HIGH)
- README.md: 58 lines (30/30) ✅
- AGENTS.md: 148 lines (20/20) ✅
- CLAUDE.md: Domain 6 (15/15) ✅
- justfile: 10 recipes (15/15) ✅

**Time**: 3.5 hours
**Impact**: Discovery time 15-20 min → <5 min (75% reduction)

---

## Success Metrics

Track these metrics before and after migration:

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Discovery time | 15-20 min | 2-5 min | <5 min |
| Discovery-to-value ratio | 0.6 | 6.0+ | ≥2.0 |
| Discoverability score | <50 | ≥80 | ≥80 |
| Time-to-adoption | Days | Hours | <1 day |

---

## Next Steps

After migration:

1. **Commit changes**: Create atomic commit per SAP
   ```bash
   git add README.md AGENTS.md CLAUDE.md justfile
   git commit -m "feat(SAP-XXX): Add discoverability improvements (vX.Y.Z)"
   ```

2. **Update SAP catalog**: Add discoverability metadata (Phase 2.4)
   ```json
   {
     "id": "SAP-XXX",
     "discoverability": {
       "score": 80,
       "level": "HIGH",
       "last_audit": "2025-11-09"
     }
   }
   ```

3. **Update ledger**: Document discoverability improvement in SAP ledger
   ```markdown
   ## Version X.Y.Z (2025-11-09)
   - Add discoverability improvements (score: XX → 80/100)
   - Add README.md, AGENTS.md, CLAUDE.md sections
   - Add justfile recipes for common workflows
   ```

4. **Announce**: Update project documentation and announce availability

---

## Questions?

- **Template issues**: See [discoverability-checklist.md](./discoverability-checklist.md)
- **Scoring questions**: See [protocol-spec.md](../sap-self-evaluation/protocol-spec.md) Section 3.5
- **Best practices**: See [SAP-000 AGENTS.md](../sap-framework/AGENTS.md) Practice 6
- **Examples**: See SAP-010, SAP-015 implementations in README.md, AGENTS.md, justfile

---

**Version History**:
- **1.0.0** (2025-11-09): Initial migration guide
  - Step-by-step workflow (7 steps, ~4 hours)
  - Batch migration strategies
  - Example migrations (SAP-010, SAP-015)
  - Success metrics and validation
