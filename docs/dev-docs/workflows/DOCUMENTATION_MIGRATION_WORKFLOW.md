# Documentation Migration Workflow

**Purpose**: Systematic process for migrating documentation to chora-base 4-domain architecture

**Applies To**: Moving documentation between domains (dev-docs/, project-docs/, user-docs/, skilled-awareness/)

**Evidence**: Tested in Wave 1 (docs/ restructuring to 4-domain model)

---

## Overview

This workflow ensures documentation migrations:
- Preserve all content (no files lost)
- Maintain 100% coherence (all files accounted for)
- Update all cross-references (no broken links)
- Track cleanup items (obsolete files, duplicates)
- Follow systematic validation

**Time Investment**: ~2-4 hours per 10 files migrated (including validation)
**ROI**: Prevents broken links, lost content, structural

 debt

---

## Prerequisites

Before starting migration:

1. **Baseline Inventory**
   ```bash
   python scripts/inventory-chora-base.py
   # Save output: docs/project-docs/inventory/pre-migration-inventory.md
   ```
   - Record total file count
   - Record SAP coverage %
   - Create snapshot of current structure

2. **Create Migration Plan**
   - Sprint plan with file-by-file mapping
   - Time estimates per domain
   - Success criteria defined
   - Risks identified

3. **Create Reference Table**
   ```markdown
   | Old Path | New Path | Domain | References to Update |
   |----------|----------|--------|---------------------|
   | docs/BENEFITS.md | docs/user-docs/explanation/benefits-of-chora-base.md | user-docs | README.md, SAP-002 |
   ```

---

## Phase 1: Planning (DDD - Documentation First)

### 1.1 Understand 4-Domain Model

**Decision Tree for Content Placement**:

```
Is this documentation...

FOR DEVELOPERS WORKING ON THE PRODUCT?
├─ Yes → dev-docs/
│  ├─ About development PROCESS?
│  │  └─ dev-docs/workflows/
│  ├─ About design PHILOSOPHY?
│  │  └─ dev-docs/explanation/
│  ├─ WALKTHROUGH or EXAMPLE?
│  │  └─ dev-docs/examples/
│  ├─ RESEARCH or LEARNINGS?
│  │  └─ dev-docs/research/
│  └─ LONG-TERM VISION?
│     └─ dev-docs/vision/
│
FOR PROJECT MANAGEMENT / LIFECYCLE?
├─ Yes → project-docs/
│  ├─ Generated during SPRINTS?
│  │  └─ project-docs/sprints/
│  ├─ About RELEASES?
│  │  └─ project-docs/releases/
│  ├─ METRICS or MEASUREMENTS?
│  │  └─ project-docs/metrics/
│  ├─ INTEGRATION PLANS?
│  │  └─ project-docs/integration/
│  └─ INVENTORY or AUDITS?
│     └─ project-docs/inventory/
│
FOR END-USERS OF THE PRODUCT?
├─ Yes → user-docs/
│  ├─ HOW-TO task guide?
│  │  └─ user-docs/how-to/
│  ├─ CONCEPTUAL explanation?
│  │  └─ user-docs/explanation/
│  ├─ REFERENCE spec?
│  │  └─ user-docs/reference/
│  └─ TUTORIAL for learning?
│     └─ user-docs/tutorials/
│
CROSS-CUTTING CAPABILITY (SAP)?
└─ Yes → skilled-awareness/
   ├─ SAP FRAMEWORK itself?
   │  └─ skilled-awareness/sap-framework/
   ├─ Capability package?
   │  └─ skilled-awareness/{capability-name}/
   └─ SAP meta-documentation?
      ├─ skilled-awareness/INDEX.md
      └─ skilled-awareness/document-templates.md
```

### 1.2 Create Migration Checklist

**Per File**:
- [ ] Determine correct domain and subdirectory
- [ ] Identify all files that reference this file
- [ ] Plan new filename (kebab-case, descriptive)
- [ ] Estimate time to move + update references

**Per Domain**:
- [ ] Create directory structure if missing
- [ ] Create README.md for domain (if doesn't exist)
- [ ] Identify domain-specific conventions

### 1.3 Document Expected Outcomes

**Success Criteria**:
- All files moved: X files
- All references updated: Y locations
- Validation: 100% pass
- Coherence: 100% maintained
- Time: Within estimate ±20%

---

## Phase 2: Execution (Incremental & Validated)

### 2.1 Create Directory Structure

```bash
# Example: Creating dev-docs structure
mkdir -p docs/dev-docs/{workflows,examples,vision,research,explanation}
mkdir -p docs/project-docs/{sprints,releases,metrics,integration,inventory}
mkdir -p docs/user-docs/{how-to,explanation,reference,tutorials}
mkdir -p docs/skilled-awareness
```

**Validation**:
```bash
# Verify directories created
ls -la docs/dev-docs/
ls -la docs/project-docs/
ls -la docs/user-docs/
ls -la docs/skilled-awareness/
```

### 2.2 Migrate Files (One Domain at a Time)

**Pattern**:
```bash
# 1. Move file
git mv docs/OLD_PATH.md docs/DOMAIN/subdirectory/new-name.md

# 2. Immediately verify moved
ls -la docs/DOMAIN/subdirectory/new-name.md

# 3. Update references (before moving next file)
# ... see section 2.3 ...

# 4. Validate (before moving next file)
# ... see section 2.4 ...
```

**Order of Migration**:
1. **skilled-awareness/** first (most referenced, foundational)
2. **project-docs/** second (historical, lower reference count)
3. **dev-docs/** third (process docs, moderate references)
4. **user-docs/** last (end-user facing, highest visibility)

**Anti-Pattern**: ❌ Don't move all files then update references
**Best Practice**: ✅ Move → Update → Validate → Next file

### 2.3 Update Cross-References

**For each moved file, update references in**:

1. **SAP awareness-guides**
   ```bash
   # Find all SAP awareness-guides
   find docs/skilled-awareness -name "awareness-guide.md" -exec grep -l "OLD_PATH" {} \;

   # Update each reference
   sed -i '' 's|docs/OLD_PATH.md|docs/NEW_PATH.md|g' docs/skilled-awareness/*/awareness-guide.md
   ```

2. **Root documentation**
   ```bash
   # Update README.md, AGENTS.md, CLAUDE.md
   grep -n "OLD_PATH" README.md AGENTS.md CLAUDE.md
   # Update manually or with sed
   ```

3. **INDEX.md files**
   ```bash
   # Update SAP INDEX
   sed -i '' 's|docs/OLD_PATH.md|docs/NEW_PATH.md|g' docs/skilled-awareness/INDEX.md
   ```

4. **Within moved file itself**
   ```bash
   # Update internal cross-references
   sed -i '' 's|(../OLD_RELATIVE_PATH)|(../NEW_RELATIVE_PATH)|g' docs/NEW_PATH.md
   ```

**Reference Update Checklist** (per file):
- [ ] SAP awareness-guides updated
- [ ] Root docs (README, AGENTS, CLAUDE) updated
- [ ] INDEX.md files updated
- [ ] Internal cross-references updated
- [ ] Relative paths adjusted for new location

### 2.4 Continuous Validation

**After each file move**:

```bash
# 1. Verify file exists at new location
test -f docs/NEW_PATH.md && echo "✅ File exists" || echo "❌ File missing"

# 2. Verify file removed from old location
test ! -f docs/OLD_PATH.md && echo "✅ Old location clean" || echo "❌ Old file still exists"

# 3. Check for broken links to this file
grep -r "docs/OLD_PATH" docs/ && echo "❌ Old references remain" || echo "✅ All references updated"

# 4. Verify new references work
# (Manual: Click links in preview, or use link checker)
```

**After each domain migration**:

```bash
# Run full inventory
python scripts/inventory-chora-base.py

# Compare to baseline
# - Total files: Should match (no files lost)
# - SAP coverage: Should be 100%
# - Uncovered: Should be 0
```

### 2.5 Track Cleanup Items

**As you migrate, update v4-cleanup-manifest.md**:

```markdown
## Files to Delete

| File | Wave | Reason | Size | Verified Safe? | Status |
|------|------|--------|------|----------------|--------|
| docs/reference/ecosystem/ | 1 | Now empty directory | - | YES | PENDING |
| docs/reference/chora-base/latest-conversation.md | 1 | Temporary conversation log | 488 KB | YES | PENDING |

## Files to Move

| From | To | Wave | Reason | Status |
|------|-----|------|--------|--------|
| docs/BENEFITS.md | docs/user-docs/explanation/benefits-of-chora-base.md | 1 | Belongs in user-docs explanation | DONE |
```

---

## Phase 3: Validation (Comprehensive)

### 3.1 Inventory Validation

```bash
# Run inventory
python scripts/inventory-chora-base.py

# Generate reports
# - inventory-summary.md
# - directory-structure.md
# - sap-coverage-matrix.md
```

**Check**:
- [ ] Total files: Matches baseline (no files lost)
- [ ] SAP coverage: 100%
- [ ] Uncovered files: 0
- [ ] All migrations accounted for

### 3.2 Link Validation

```bash
# Find all markdown files
find docs -name "*.md" > all-docs.txt

# Check for broken links (example pattern)
while read file; do
    # Extract links
    grep -o '\[.*\](.*\.md)' "$file" | while read link; do
        # Extract path
        path=$(echo "$link" | sed -E 's/.*\((.*)\).*/\1/')

        # Resolve relative path
        dir=$(dirname "$file")
        full_path="$dir/$path"

        # Check if exists
        if [ ! -f "$full_path" ]; then
            echo "❌ Broken link in $file: $path"
        fi
    done
done < all-docs.txt
```

Or use dedicated link checker:
```bash
# Example with markdown-link-check (if available)
npm install -g markdown-link-check
find docs -name "*.md" -exec markdown-link-check {} \;
```

**Check**:
- [ ] All internal links valid
- [ ] All relative paths correct
- [ ] No 404 errors

### 3.3 SAP Validation

```bash
# Verify all SAPs have 5 artifacts
for sap in docs/skilled-awareness/*/; do
    echo "Checking $(basename $sap)..."

    required=("capability-charter.md" "protocol-spec.md" "awareness-guide.md" "adoption-blueprint.md" "ledger.md")

    for file in "${required[@]}"; do
        if [ ! -f "$sap/$file" ]; then
            echo "  ❌ Missing: $file"
        else
            echo "  ✅ $file"
        fi
    done
done
```

**Check**:
- [ ] All 14 SAPs complete
- [ ] All awareness-guides reference actual files
- [ ] No orphan references

### 3.4 Git Status Check

```bash
git status
```

**Verify**:
- [ ] All moves tracked by git
- [ ] No unintended deletions
- [ ] No unexpected new files
- [ ] Working directory clean (or only expected changes)

---

## Phase 4: Documentation & Metrics

### 4.1 Update Cleanup Manifest

Final review of v4-cleanup-manifest.md:
- Mark all "Files to Move" as DONE
- Add any "Files to Delete" discovered
- Add any "Files to Archive" discovered
- List all "References to Update" (mark as DONE)

### 4.2 Create Execution Metrics

**File**: `docs/project-docs/metrics/migration-execution-metrics.md`

```markdown
# Migration Execution Metrics

**Migration**: [Name]
**Wave**: [Number]
**Date**: [YYYY-MM-DD]

## Time Tracking

| Task | Estimated | Actual | Variance |
|------|-----------|--------|----------|
| Planning | 2h | 2.5h | +25% |
| Directory creation | 0.5h | 0.3h | -40% |
| File migrations | 4h | 5h | +25% |
| Reference updates | 8h | 10h | +25% |
| Validation | 2h | 1.5h | -25% |
| **Total** | **16.5h** | **19.3h** | **+17%** |

## File Counts

- Files migrated: X
- References updated: Y
- Domains affected: 4
- SAPs updated: 14

## Quality Metrics

- Inventory validation: PASS ✅
- Link validation: PASS ✅
- SAP validation: PASS ✅
- Coherence: 100% ✅

## Learnings

**What worked well**:
- [List successes]

**What could improve**:
- [List improvements]

**Process adherence**: 95%
```

### 4.3 Create Release Notes

**File**: `docs/project-docs/releases/vX.X.X-migration-release-notes.md`

Document:
- What changed
- Why it changed
- Migration impact
- Benefits delivered
- Breaking changes (if any)

### 4.4 Identify Skilled-Awareness Evolution Opportunities

**Purpose**: Recognize learnings that could become new or enhanced SAPs

**Questions to ask during and after migration**:

1. **Object-Level SAPs** (Directly applicable to migration task):
   - Could "Documentation Migration" be its own SAP?
   - Should there be a SAP for "Link Validation"?
   - Is there a SAP for "Content Classification" (deciding which domain)?
   - Would a "Cross-Reference Management" SAP be valuable?

2. **Process-Level SAPs** (Broader workflow insights):
   - Did we discover a repeatable pattern that isn't documented?
   - Is there a tool/script that should be formalized as a capability?
   - Would other projects benefit from this same workflow?

3. **Meta-Level SAPs** (Framework improvements):
   - Does this migration reveal gaps in SAP framework itself?
   - Should SAP-000 (SAP Framework) be enhanced?
   - Is there a meta-pattern about identifying SAP opportunities?

**Documentation Pattern**:

Create `docs/dev-docs/research/wave-N-sap-opportunities.md`:

```markdown
# Wave N: Skilled-Awareness Evolution Opportunities

## Discovered During Migration

### Direct Object-Level Opportunities

**Potential SAP: Documentation Migration**
- **Why**: Repeated pattern across multiple waves/projects
- **Capability**: Systematic doc restructuring with validation
- **Artifacts Needed**:
  - capability-charter.md (business value of doc migrations)
  - protocol-spec.md (migration contract: inputs, outputs, guarantees)
  - awareness-guide.md (this workflow doc becomes the basis)
  - adoption-blueprint.md (how to install migration tools)
  - ledger.md (track migration adoptions)
- **Dependencies**: SAP-007 (Documentation Framework)
- **Priority**: Medium (useful for v4.0 waves, essential for external adopters)

**Potential SAP: Link Validation**
- **Why**: Critical for maintaining documentation coherence
- **Capability**: Automated link checking, reference mapping
- **Tools**: Link checker script, reference graph generator
- **Priority**: High (prevents broken docs)

### Process-Level Opportunities

**Enhancement to SAP-008: Automation Scripts**
- **Learning**: Migration benefits from incremental scripts (move-one, validate-one pattern)
- **Enhancement**: Add migration automation patterns to SAP-008
- **Script Examples**:
  - `migrate-doc.sh <old-path> <new-path>` (move + update + validate)
  - `validate-links.sh` (comprehensive link checker)
  - `generate-reference-table.sh` (auto-create old→new mapping)

**Enhancement to SAP-007: Documentation Framework**
- **Learning**: 4-domain decision tree is critical for classification
- **Enhancement**: Add decision tree tool or checklist to SAP-007
- **Artifact**: Interactive decision tree (CLI or doc)

### Meta-Level Insights

**SAP-000 Enhancement: SAP Opportunity Identification**
- **Learning**: Each wave reveals new SAP opportunities
- **Enhancement**: Add "Identifying SAP Opportunities" section to SAP-000
- **Pattern**: Questions framework (object/process/meta levels)
- **Timing**: Include in all sprint retrospectives

## Action Items

- [ ] Create SAP-015: Documentation Migration (Wave 3 or post-v4.0)
- [ ] Create SAP-016: Link Validation & Reference Management (Wave 2)
- [ ] Enhance SAP-008 with migration automation patterns (Wave 1 or 2)
- [ ] Enhance SAP-007 with domain classification decision tree (Wave 1)
- [ ] Enhance SAP-000 with SAP opportunity identification framework (Wave 2)

## Cross-Wave Patterns

**Emerging**: As we complete Waves 1-7, look for:
- Repeated tools/scripts → Candidate SAPs
- Repeated decision points → Candidate decision trees
- Repeated validations → Candidate quality gates
- Repeated process steps → Candidate workflows
```

**When to Document**:
- During execution: Note insights in sprint log
- During retrospective: Formalize into SAP opportunities
- Between waves: Prioritize and plan SAP creation

**Integration with Existing SAPs**:
- SAP-007 (Documentation Framework): Enhanced with migration patterns
- SAP-008 (Automation Scripts): Enhanced with migration scripts
- SAP-000 (SAP Framework): Enhanced with opportunity identification
- New SAPs: Created when patterns proven across multiple waves

---

## Common Pitfalls & Anti-Patterns

### ❌ Anti-Pattern 1: Batch Move Without Validation

**Problem**: Move all files, then try to fix all references

**Impact**:
- Overwhelming number of broken links
- Hard to track what's updated
- Easy to miss references
- Difficult to rollback

**Solution**: ✅ Move → Update → Validate → Next file

---

### ❌ Anti-Pattern 2: Inconsistent Naming

**Problem**: Mixing naming conventions (camelCase, snake_case, kebab-case)

**Impact**:
- Inconsistent file discovery
- Harder to grep/search
- Looks unprofessional

**Solution**: ✅ Use kebab-case for all docs: `benefits-of-chora-base.md`

---

### ❌ Anti-Pattern 3: Skipping Inventory Baseline

**Problem**: Start migration without recording baseline

**Impact**:
- Can't verify no files lost
- Can't measure progress
- No rollback point

**Solution**: ✅ Always run inventory before and after

---

### ❌ Anti-Pattern 4: Manual Search for References

**Problem**: Manually searching for cross-references

**Impact**:
- Easy to miss references
- Time-consuming
- Error-prone

**Solution**: ✅ Use grep, sed, and automated link checkers

---

### ❌ Anti-Pattern 5: Ignoring Cleanup Manifest

**Problem**: Not tracking obsolete files during migration

**Impact**:
- Leaves debris in repository
- Cleanup becomes separate project
- Unclear what's intentional

**Solution**: ✅ Update v4-cleanup-manifest.md as you discover items

---

## Rollback Procedure

If migration fails or needs rollback:

### Option 1: Git Reset (if uncommitted)
```bash
git status
git checkout -- .
# Restores all files to last commit
```

### Option 2: Git Revert (if committed)
```bash
git log --oneline
git revert <commit-hash>
# Creates new commit that undoes migration
```

### Option 3: Restore from Baseline
```bash
# If you created a branch for migration
git checkout main
git branch -D migration-attempt
```

---

## Checklist Summary

### Before Migration
- [ ] Baseline inventory complete
- [ ] Migration plan created
- [ ] Reference table created
- [ ] Success criteria defined
- [ ] Directory structure understood

### During Migration
- [ ] Files moved one-by-one (or domain-by-domain)
- [ ] References updated immediately
- [ ] Continuous validation after each move
- [ ] Cleanup manifest updated as you go
- [ ] Git commits incremental (optional: per domain)

### After Migration
- [ ] Inventory validation: PASS
- [ ] Link validation: PASS
- [ ] SAP validation: PASS
- [ ] Cleanup manifest: UPDATED
- [ ] Execution metrics: CREATED
- [ ] Release notes: CREATED
- [ ] Git commit: COMPLETE

---

## Time Estimates

**Per 10 Files**:
- Planning: 0.5-1 hour
- Migration: 0.5-1 hour
- Reference updates: 1-2 hours
- Validation: 0.5 hour
- **Total**: 2.5-4.5 hours

**Factors Affecting Time**:
- Number of cross-references (more = longer)
- Complexity of relative paths (nested = longer)
- Tooling availability (automated > manual)
- Familiarity with structure (first time = longer)

---

## Tools & Scripts

**Required**:
- `scripts/inventory-chora-base.py` - Baseline and validation
- `git mv` - Track file moves
- `grep` / `sed` - Find and update references

**Recommended**:
- Link checker (markdown-link-check or similar)
- Text editor with global search/replace
- Git GUI (for reviewing changes visually)

**Optional**:
- Custom validation scripts
- Automated reference updater
- Visual diff tools

---

## Related Documentation

**Process**:
- [Development Lifecycle](DEVELOPMENT_LIFECYCLE.md) - Overall dev process
- [Documentation Plan](../../project-docs/DOCUMENTATION_PLAN.md) - Documentation strategy

**Architecture**:
- [Architecture](../ARCHITECTURE.md) - 4-domain model explained
- [SAP Framework](../../skilled-awareness/sap-framework/) - SAP structure

**Examples**:
- Wave 1 execution: Real-world application of this workflow

---

**Workflow Version**: 1.0
**Created**: 2025-10-28
**Tested In**: Wave 1 (docs/ restructuring)
**Status**: Active

This workflow is itself an example of dev-docs/ content (process documentation).
