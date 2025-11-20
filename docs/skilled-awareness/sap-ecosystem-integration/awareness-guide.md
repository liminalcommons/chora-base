# SAP Ecosystem Integration: Awareness Guide

**SAP ID**: SAP-061
**Version**: 1.0.0
**Status**: draft
**Last Updated**: 2025-11-20
**For**: Claude Code agents, human developers, automation tools

---

## Document Purpose

This awareness guide provides **practical workflows and patterns** for Claude Code agents and developers working with SAP ecosystem integration. It translates the technical protocol specification into actionable guidance for day-to-day SAP development.

**What You'll Learn**:
- When to validate ecosystem integration during SAP development
- How to interpret and resolve validation failures
- Proactive patterns for maintaining integration integrity
- Multi-tab coordination strategies for SAP work
- Pre-commit hook interaction patterns

**Before Reading**: Familiarize yourself with [protocol-spec.md](protocol-spec.md) for technical details on validation algorithms and schemas.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Agent Workflows](#agent-workflows)
3. [Pre-commit Hook Patterns](#pre-commit-hook-patterns)
4. [Error Recovery Patterns](#error-recovery-patterns)
5. [Proactive Integration Patterns](#proactive-integration-patterns)
6. [SAP Development Lifecycle Integration](#sap-development-lifecycle-integration)
7. [Multi-Tab Coordination](#multi-tab-coordination)
8. [Validation Commands Reference](#validation-commands-reference)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### For Claude Code Agents

**When to validate ecosystem integration**:
1. ✅ **Always**: Before committing SAP artifacts
2. ✅ **Always**: After status promotion (draft → pilot → active)
3. ✅ **Recommended**: After creating new SAP directory
4. ✅ **Recommended**: Before closing SAP development task

**Quick validation**:
```bash
# Validate single SAP (2s)
python scripts/validate-ecosystem-integration.py SAP-061

# Validate all SAPs (8-10s for ~50 SAPs)
python scripts/validate-ecosystem-integration.py --all

# Get JSON output for automation
python scripts/validate-ecosystem-integration.py SAP-061 --json
```

**Integration checklist** (use during SAP development):
- [ ] SAP entry exists in INDEX.md
- [ ] SAP entry exists in sap-catalog.json (if status=pilot/active)
- [ ] SAP integration exists in copier.yml (if status=pilot/active)
- [ ] SAP mentioned in Progressive Adoption Path (recommended for status=active)
- [ ] All dependencies reference valid SAPs

### For Human Developers

**Pre-commit hook integration**: Ecosystem validation runs automatically when you commit changes to:
- SAP artifacts: `docs/skilled-awareness/*/*.md`
- INDEX.md: `docs/skilled-awareness/INDEX.md`
- Catalog: `sap-catalog.json`
- Copier config: `copier.yml`

**What to expect**:
- ✅ **Pass**: Commit proceeds normally (validation <2s)
- ❌ **Fail**: Commit blocked, fix integration gaps and retry

**Bypass hook** (only when intentionally committing incomplete integration):
```bash
git commit --no-verify -m "WIP: Draft SAP-061 (incomplete integration)"
```

---

## Agent Workflows

### Workflow 1: Creating New SAP

**Scenario**: Claude Code agent is creating a new SAP from scratch.

**Steps**:

1. **Create SAP directory and artifacts** (Phase 1 - Design)
   ```bash
   mkdir docs/skilled-awareness/sap-XXX-name
   cd docs/skilled-awareness/sap-XXX-name
   # Create 5 core artifacts
   touch capability-charter.md protocol-spec.md awareness-guide.md adoption-blueprint.md ledger.md
   ```

2. **Write capability charter** (include metadata)
   ```markdown
   ---
   sap_id: SAP-XXX
   status: draft
   version: 0.1.0
   dependencies:
     - SAP-000
     - SAP-YYY
   ---

   # SAP-XXX: [Title]

   **SAP ID**: SAP-XXX
   **Status**: draft
   **Version**: 0.1.0
   **Dependencies**: SAP-000, SAP-YYY
   ```

3. **Add INDEX.md entry** (required for draft status)
   ```bash
   # Read INDEX.md to find appropriate domain section
   # Add SAP entry under domain heading
   vim docs/skilled-awareness/INDEX.md
   ```

4. **Validate integration** (before first commit)
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: Pass (draft only requires INDEX + dependencies)
   ```

5. **Register work context** (if using multi-tab coordination)
   ```bash
   # Add to .chora/work-contexts.yaml
   just work-context-update tab-N
   ```

6. **Commit initial SAP**
   ```bash
   git add docs/skilled-awareness/sap-XXX-name/ docs/skilled-awareness/INDEX.md
   git commit -m "feat(sap-XXX): Add initial SAP-XXX artifacts (draft)"
   # Pre-commit hook runs validation
   # ✅ Passes (draft requirements met)
   ```

**Time Investment**: 5-10 minutes (validation <2s, context registration 1-2 minutes)

**Integration Gaps Prevented**: INDEX.md omission (most common gap)

---

### Workflow 2: Promoting SAP Status (draft → pilot)

**Scenario**: SAP development complete, ready for pilot testing.

**Steps**:

1. **Update SAP status in capability-charter.md**
   ```markdown
   **Status**: pilot  # Was: draft
   **Version**: 1.0.0  # Increment to 1.0.0 for pilot
   ```

2. **Validate integration** (pilot requires catalog + copier)
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ❌ Fail (missing catalog + copier)
   ```

3. **Add sap-catalog.json entry**
   ```bash
   vim sap-catalog.json
   # Add SAP entry (see protocol-spec.md for schema)
   ```

4. **Add copier.yml integration**
   ```bash
   vim copier.yml
   # Add include_sap_XXX variable under appropriate mode
   ```

5. **Re-validate integration**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ✅ Pass (all pilot requirements met)
   ```

6. **Update INDEX.md status**
   ```bash
   vim docs/skilled-awareness/INDEX.md
   # Update SAP entry: status: pilot, version: 1.0.0
   ```

7. **Register new files in work context**
   ```bash
   # Add sap-catalog.json and copier.yml to work context
   just work-context-update tab-N
   ```

8. **Commit promotion**
   ```bash
   git add docs/skilled-awareness/sap-XXX-name/ docs/skilled-awareness/INDEX.md sap-catalog.json copier.yml
   git commit -m "feat(sap-XXX): Promote SAP-XXX to pilot status (v1.0.0)"
   # Pre-commit hook runs validation
   # ✅ Passes (pilot requirements met)
   ```

**Time Investment**: 10-15 minutes (validation 2s, catalog/copier updates 5-10 minutes)

**Integration Gaps Prevented**: Catalog omission, copier misconfiguration

---

### Workflow 3: Completing SAP Phase (e.g., Phase 4 completion)

**Scenario**: SAP has reached Phase 4 (Distribution), ready to close beads task.

**Steps**:

1. **Verify all artifacts complete**
   ```bash
   ls docs/skilled-awareness/sap-XXX-name/
   # Expect: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md
   ```

2. **Verify status is "active"**
   ```bash
   grep "Status" docs/skilled-awareness/sap-XXX-name/capability-charter.md
   # Expect: **Status**: active
   ```

3. **Run ecosystem validation**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ✅ Pass (all active requirements met)
   # Or: ⚠️ Warning (adoption path not mentioned - optional)
   ```

4. **If validation fails, resolve gaps**
   ```bash
   # Common gaps at Phase 4:
   # - INDEX.md not updated after status change
   # - Copier integration missing
   # - Dependencies changed but not validated
   ```

5. **Update ledger.md** (track completion)
   ```markdown
   ## Phase 4: Distribution (L3 → L4)
   - **Status**: ✅ Complete
   - **Completed**: 2025-11-20
   - **Ecosystem Integration**: ✅ Validated (all 5 integration points)
   ```

6. **Final validation before closing task**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX --verbose
   # Review detailed validation output
   ```

7. **Commit completion**
   ```bash
   git add docs/skilled-awareness/sap-XXX-name/ docs/skilled-awareness/INDEX.md
   git commit -m "docs(sap-XXX): Complete Phase 4 - SAP-XXX at L4 (distributed)"
   # Pre-commit hook runs validation
   # ✅ Passes
   ```

8. **Close beads task**
   ```bash
   bd close chora-workspace-XXXX
   ```

**Time Investment**: 5-10 minutes (validation 2s, ledger update 3-5 minutes)

**Integration Gaps Prevented**: Incomplete integration at SAP completion

---

### Workflow 4: Discovering Integration Gaps (Retroactive Fix)

**Scenario**: Existing SAP missing from INDEX.md (like SAP-053 trigger case).

**Steps**:

1. **Run ecosystem validation on all SAPs**
   ```bash
   python scripts/validate-ecosystem-integration.py --all
   # Output shows which SAPs have integration gaps
   ```

2. **Filter for specific SAP**
   ```bash
   python scripts/validate-ecosystem-integration.py --all --json | jq '.results."SAP-XXX"'
   # Shows detailed validation results for SAP-XXX
   ```

3. **Identify failed integration points**
   ```bash
   # Example output:
   # ❌ Failed: 1/48
   # Failed SAPs:
   #   - SAP-053: INDEX.md
   ```

4. **Fix identified gaps**
   ```bash
   # If INDEX.md missing: Add SAP entry
   vim docs/skilled-awareness/INDEX.md

   # If catalog missing: Add catalog entry
   vim sap-catalog.json

   # If copier missing: Add copier integration
   vim copier.yml
   ```

5. **Re-validate**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ✅ Pass
   ```

6. **Register files in work context**
   ```bash
   just work-context-update tab-N
   ```

7. **Commit fix**
   ```bash
   git add docs/skilled-awareness/INDEX.md  # or other modified files
   git commit -m "fix(sap-XXX): Add SAP-XXX to INDEX.md (retroactive integration)"
   # Pre-commit hook runs validation
   # ✅ Passes
   ```

**Time Investment**: 5-10 minutes per SAP (validation 2s, fix 3-8 minutes)

**Integration Gaps Prevented**: Accumulation of integration debt

---

### Workflow 5: Updating Dependencies

**Scenario**: SAP dependencies change during development.

**Steps**:

1. **Update dependencies in capability-charter.md**
   ```markdown
   **Dependencies**: SAP-000, SAP-051, SAP-010  # Added SAP-010
   ```

2. **Validate dependencies**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ✅ Pass (if SAP-010 exists)
   # Or: ❌ Fail (if SAP-010 does not exist)
   ```

3. **If validation fails with broken dependencies**
   ```bash
   # Option A: Create missing dependency SAP
   # Follow Workflow 1 to create SAP-010

   # Option B: Remove invalid dependency
   vim docs/skilled-awareness/sap-XXX-name/capability-charter.md
   # Remove SAP-010 from dependencies
   ```

4. **Update INDEX.md dependencies field**
   ```bash
   vim docs/skilled-awareness/INDEX.md
   # Update SAP-XXX entry: Dependencies: SAP-000, SAP-051, SAP-010
   ```

5. **Re-validate**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-XXX
   # Expected: ✅ Pass
   ```

6. **Commit dependency update**
   ```bash
   git add docs/skilled-awareness/sap-XXX-name/ docs/skilled-awareness/INDEX.md
   git commit -m "docs(sap-XXX): Update dependencies (add SAP-010)"
   # Pre-commit hook runs validation
   # ✅ Passes
   ```

**Time Investment**: 3-5 minutes (validation 2s, updates 1-3 minutes)

**Integration Gaps Prevented**: Broken dependency references

---

## Pre-commit Hook Patterns

### Pattern 1: Normal Commit Flow (Validation Passes)

**Scenario**: Agent commits SAP artifacts, validation passes.

**Flow**:
```
1. Agent: git add docs/skilled-awareness/sap-061/ docs/skilled-awareness/INDEX.md
2. Agent: git commit -m "feat(sap-061): Add SAP-061 capability charter"
3. Git: Run pre-commit hooks
4. Pre-commit: Detect file pattern match (SAP artifacts modified)
5. Pre-commit: Run validate-ecosystem-integration.py --all
6. Script: Validate all SAPs (8.7s for 48 SAPs)
7. Script: Exit code 0 (all passed)
8. Pre-commit: Hook passed
9. Git: Create commit
10. Agent: Commit successful ✅
```

**Agent Actions**:
- ✅ Proceed with normal workflow
- ✅ No additional actions needed

---

### Pattern 2: Commit Blocked by Validation Failure

**Scenario**: Agent commits SAP artifacts, validation fails.

**Flow**:
```
1. Agent: git commit -m "feat(sap-061): Add SAP-061 to ecosystem"
2. Git: Run pre-commit hooks
3. Pre-commit: Run validate-ecosystem-integration.py --all
4. Script: Validation fails for SAP-061 (exit code 2 - catalog missing)
5. Pre-commit: Hook failed, display output
6. Git: Commit blocked ❌
7. Agent: Read validation output
8. Agent: Fix integration gap (add catalog entry)
9. Agent: Retry commit
10. Git: Commit successful ✅
```

**Agent Actions**:
1. ✅ **Read hook output** to identify failed integration point
2. ✅ **Fix integration gap** (add missing entry)
3. ✅ **Register file in work context** (if new file)
4. ✅ **Retry commit** (hook re-runs validation)

**Example Output**:
```
Validate SAP Ecosystem Integration..................................Failed
- hook id: validate-sap-ecosystem-integration
- exit code: 2

======================================================================
Ecosystem Integration Validation: 48 SAPs
======================================================================

✅ Passed: 47/48
❌ Failed: 1/48

Failed SAPs:
  - SAP-061: sap-catalog.json
```

---

### Pattern 3: Work Context Conflict During Commit

**Scenario**: Agent commits file, work context hook blocks commit (file not registered).

**Flow**:
```
1. Agent: git commit -m "feat(sap-061): Add catalog entry"
2. Git: Run pre-commit hooks
3. Pre-commit: Run work-context-coordination hook (runs BEFORE ecosystem validation)
4. Work context hook: sap-catalog.json not in tab-N's work context
5. Work context hook: Exit code 1 (conflict detected)
6. Git: Commit blocked ❌ (before ecosystem validation even runs)
7. Agent: Read work context output
8. Agent: Add sap-catalog.json to work context
9. Agent: Retry commit
10. Pre-commit: Work context passes, ecosystem validation runs
11. Git: Commit successful ✅
```

**Agent Actions**:
1. ✅ **Recognize work context conflict** (distinct from ecosystem validation)
2. ✅ **Add file to work context**: Edit `.chora/work-contexts.yaml`
3. ✅ **Retry commit** (both hooks now pass)

**Important**: Work context hook runs **before** ecosystem validation. Fix work context conflicts first.

---

### Pattern 4: Bypass Hook for WIP Commits

**Scenario**: Agent working on draft SAP, integration incomplete by design.

**Flow**:
```
1. Agent: Working on SAP-061 Phase 1 (Design)
2. Agent: capability-charter.md complete, other artifacts not started
3. Agent: Want to commit checkpoint before break
4. Agent: Know validation will fail (other artifacts missing)
5. Agent: Use --no-verify to bypass pre-commit hooks
6. Agent: git commit --no-verify -m "WIP: SAP-061 charter (Phase 1 checkpoint)"
7. Git: Skip all pre-commit hooks
8. Git: Create commit ✅
9. Agent: Add TODO to complete integration before merge
```

**Agent Actions**:
- ✅ **Use --no-verify sparingly** (only for intentional WIP commits)
- ✅ **Document intent** in commit message ("WIP", "checkpoint", "incomplete")
- ✅ **Track integration debt** (add TODO, beads task, or reminder)
- ✅ **Complete integration before merging** to main branch

**⚠️ Warning**: Bypassing validation creates integration debt. Complete integration before PR merge.

---

### Pattern 5: Multiple Files, Single Validation Run

**Scenario**: Agent commits multiple files (INDEX.md + catalog + copier), validation runs once.

**Flow**:
```
1. Agent: git add docs/skilled-awareness/INDEX.md sap-catalog.json copier.yml
2. Agent: git commit -m "feat(sap-061): Complete pilot integration"
3. Git: Run pre-commit hooks
4. Pre-commit: Detect multiple files match pattern
5. Pre-commit: Run validate-ecosystem-integration.py --all (single run)
6. Script: Validate all SAPs (8.7s)
7. Script: Exit code 0
8. Git: Create commit ✅
```

**Agent Actions**:
- ✅ **Batch related changes** (commit INDEX + catalog + copier together)
- ✅ **Validation runs once** (not per-file, saving time)
- ✅ **Atomic commit** (all integration points updated together)

**Performance**: Single validation run (8.7s) vs 3 separate runs (26.1s) = 17.4s saved

---

## Error Recovery Patterns

### Error 1: INDEX.md Missing Entry

**Error Output**:
```
❌ INDEX.md
   SAP-061 NOT found in INDEX.md
   Details: Expected entry like '#### SAP-061: <Title>' in docs/skilled-awareness/INDEX.md
```

**Recovery Steps**:

1. **Read INDEX.md** to find appropriate domain section
   ```bash
   vim docs/skilled-awareness/INDEX.md
   # Find domain heading (## Developer Experience, ## Project Management, etc.)
   ```

2. **Extract SAP metadata** from capability-charter.md
   ```bash
   grep -E "(SAP ID|Status|Version|Dependencies|Description)" docs/skilled-awareness/sap-061/capability-charter.md
   ```

3. **Add SAP entry** under domain heading
   ```markdown
   #### SAP-061: SAP Ecosystem Integration

   - **Status**: draft | **Version**: 1.0.0 | **Domain**: Developer Experience
   - **Description**: Automated ecosystem integration validation across 5 integration points preventing gaps like SAP-053 INDEX.md omission
   - **Dependencies**: SAP-000, SAP-050
   - **Location**: [sap-ecosystem-integration/](sap-ecosystem-integration/)
   - **Key Features**: 5 integration point validation (INDEX, catalog, copier, adoption path, dependencies), pre-commit hook integration, status-based requirements, <2s validation, exit codes 0-6, JSON output
   ```

4. **Update statistics** (total SAPs, domain count)
   ```markdown
   **Total SAPs**: 48 → 49
   **Developer Experience**: 16 SAPs → 17 SAPs
   ```

5. **Register INDEX.md in work context**
   ```bash
   just work-context-update tab-N
   ```

6. **Retry commit**
   ```bash
   git add docs/skilled-awareness/INDEX.md
   git commit -m "docs(index): Add SAP-061 to catalog"
   # ✅ Passes
   ```

**Time to Resolve**: 5-8 minutes

---

### Error 2: sap-catalog.json Missing Entry

**Error Output**:
```
❌ sap-catalog.json
   SAP-061 NOT found in sap-catalog.json
   Details: Add SAP entry to sap-catalog.json for machine-readable discovery
```

**Recovery Steps**:

1. **Read sap-catalog.json** to understand structure
   ```bash
   cat sap-catalog.json | jq '.' | head -30
   # Determine if Option A (object with keys) or Option B (array under "saps")
   ```

2. **Extract SAP metadata** from capability-charter.md
   ```bash
   grep -E "(SAP ID|Status|Version|Dependencies|Description|Domain)" docs/skilled-awareness/sap-061/capability-charter.md
   ```

3. **Add catalog entry** (Option A example)
   ```json
   {
     "SAP-061": {
       "id": "SAP-061",
       "title": "SAP Ecosystem Integration",
       "status": "draft",
       "version": "1.0.0",
       "domain": "Developer Experience",
       "description": "Automated ecosystem integration validation across 5 integration points",
       "dependencies": ["SAP-000", "SAP-050"],
       "location": "sap-ecosystem-integration/",
       "created": "2025-11-20",
       "updated": "2025-11-20"
     }
   }
   ```

4. **Validate JSON syntax**
   ```bash
   cat sap-catalog.json | jq '.'
   # Should parse without errors
   ```

5. **Register catalog in work context**
   ```bash
   just work-context-update tab-N
   ```

6. **Retry commit**
   ```bash
   git add sap-catalog.json
   git commit -m "feat(catalog): Add SAP-061 to catalog"
   # ✅ Passes
   ```

**Time to Resolve**: 3-5 minutes

---

### Error 3: copier.yml Missing Integration

**Error Output**:
```
❌ copier.yml
   SAP-061 NOT found in copier.yml
   Details: Add include_sap_061 variable to copier.yml for distribution (status=pilot requires distribution)
```

**Recovery Steps**:

1. **Read copier.yml** to find SAP integration section
   ```bash
   grep -A 5 "include_sap" copier.yml | head -20
   # Understand variable structure
   ```

2. **Create include_sap_061 variable**
   ```yaml
   include_sap_061:
     type: bool
     help: Include SAP-061 (SAP Ecosystem Integration) for automated validation?
     default: false
     when: "{{ sap_selection_mode in ['custom', 'comprehensive'] }}"
   ```

3. **Add to appropriate SAP selection mode**
   ```yaml
   # Under "comprehensive" mode (if SAP is production-ready)
   # Or under "custom" mode (if SAP is pilot/experimental)
   ```

4. **Register copier.yml in work context**
   ```bash
   just work-context-update tab-N
   ```

5. **Retry commit**
   ```bash
   git add copier.yml
   git commit -m "feat(copier): Add SAP-061 distribution config"
   # ✅ Passes
   ```

**Time to Resolve**: 3-5 minutes

---

### Error 4: Broken Dependencies

**Error Output**:
```
❌ Dependencies
   SAP-061 has broken dependencies: SAP-999
   Details: Dependencies reference non-existent SAPs: [SAP-999]
```

**Recovery Steps**:

1. **Verify dependency existence**
   ```bash
   # Check if SAP-999 directory exists
   ls docs/skilled-awareness/ | grep sap-999
   # Or search for SAP-999 in INDEX.md
   grep "SAP-999" docs/skilled-awareness/INDEX.md
   ```

2. **Option A: Create missing dependency** (if SAP-999 should exist)
   ```bash
   # Follow Workflow 1 to create SAP-999
   mkdir docs/skilled-awareness/sap-999
   # Create artifacts...
   ```

3. **Option B: Remove invalid dependency** (if SAP-999 was referenced in error)
   ```bash
   vim docs/skilled-awareness/sap-061/capability-charter.md
   # Remove SAP-999 from dependencies list
   # Update: **Dependencies**: SAP-000, SAP-050 (removed SAP-999)
   ```

4. **Update INDEX.md** (sync dependencies field)
   ```bash
   vim docs/skilled-awareness/INDEX.md
   # Update SAP-061 entry dependencies
   ```

5. **Retry commit**
   ```bash
   git add docs/skilled-awareness/sap-061/ docs/skilled-awareness/INDEX.md
   git commit -m "docs(sap-061): Fix broken dependency (remove SAP-999)"
   # ✅ Passes
   ```

**Time to Resolve**: 2-5 minutes (if removing), 10-20 minutes (if creating missing SAP)

---

### Error 5: Multiple Integration Failures

**Error Output**:
```
❌ FAILURE: SAP-061 has 3 integration gap(s)

Failed checks:
  - INDEX.md: SAP-061 NOT found in INDEX.md
  - sap-catalog.json: SAP-061 NOT found in sap-catalog.json
  - copier.yml: SAP-061 NOT found in copier.yml
```

**Recovery Steps**:

1. **Get detailed JSON output**
   ```bash
   python scripts/validate-ecosystem-integration.py SAP-061 --json | jq '.'
   # Review all failed checks and details fields
   ```

2. **Fix integration points in priority order**
   ```bash
   # Priority 1: INDEX.md (most critical)
   # Priority 2: sap-catalog.json
   # Priority 3: copier.yml
   # Priority 4: Dependencies
   ```

3. **Follow individual error recovery patterns** (Errors 1-4 above)

4. **Batch commit all fixes**
   ```bash
   git add docs/skilled-awareness/INDEX.md sap-catalog.json copier.yml
   git commit -m "fix(sap-061): Complete ecosystem integration (INDEX + catalog + copier)"
   # ✅ Passes
   ```

**Time to Resolve**: 10-20 minutes (sum of individual fixes)

---

## Proactive Integration Patterns

### Pattern 1: Integration-First Development

**Principle**: Add INDEX.md + catalog entries **before** writing SAP artifacts.

**Workflow**:
```bash
# 1. Create SAP directory
mkdir docs/skilled-awareness/sap-061

# 2. Add INDEX.md entry (with placeholder description)
vim docs/skilled-awareness/INDEX.md
# Add: #### SAP-061: [Title TBD]

# 3. Add catalog entry (with placeholder fields)
vim sap-catalog.json
# Add: { "id": "SAP-061", "status": "draft", ... }

# 4. Validate integration (before writing artifacts)
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Passes (INDEX + catalog + dependencies)

# 5. Now write SAP artifacts
touch docs/skilled-awareness/sap-061/capability-charter.md
# Write charter...

# 6. Commit (no integration gaps)
git add .
git commit -m "feat(sap-061): Add SAP-061 with full integration"
# ✅ Passes immediately
```

**Benefits**:
- ✅ No retroactive integration fixes needed
- ✅ Validation passes on first commit
- ✅ Forces SAP metadata design upfront (ID, title, domain, dependencies)

**Time Saved**: 5-10 minutes (no rework, no commit retries)

---

### Pattern 2: Periodic Ecosystem Audits

**Principle**: Run `--all` validation weekly to catch integration drift.

**Workflow**:
```bash
# Weekly audit (e.g., every Monday, before sprint planning)
python scripts/validate-ecosystem-integration.py --all

# If failures found:
python scripts/validate-ecosystem-integration.py --all --json > /tmp/validation-report.json
cat /tmp/validation-report.json | jq '.results | to_entries | map(select(.value.passed == false))'

# Fix gaps proactively (before they accumulate)
# Follow Error Recovery Patterns above
```

**Benefits**:
- ✅ Early detection of integration drift
- ✅ Prevents accumulation of integration debt
- ✅ Maintains ecosystem health

**Time Investment**: 5-10 minutes/week

---

### Pattern 3: Status Promotion Checklist

**Principle**: Validate integration **before** updating status field.

**Workflow**:
```bash
# Before promoting SAP-061 from draft → pilot:

# 1. Check current integration
python scripts/validate-ecosystem-integration.py SAP-061
# ❌ Fail (draft status, catalog/copier not required yet)

# 2. Add catalog entry (prep for pilot)
vim sap-catalog.json

# 3. Add copier integration (prep for pilot)
vim copier.yml

# 4. Validate pilot requirements
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass (now ready for pilot)

# 5. Now update status field
vim docs/skilled-awareness/sap-061/capability-charter.md
# Update: **Status**: pilot

# 6. Commit (validation passes on first try)
git add .
git commit -m "feat(sap-061): Promote to pilot status (v1.0.0)"
# ✅ Passes
```

**Benefits**:
- ✅ Zero commit retries
- ✅ Status promotion atomic (integration complete in single commit)
- ✅ Clear separation of concerns (integration prep → status update)

**Time Saved**: 3-5 minutes (no retries, clear workflow)

---

### Pattern 4: Dependency Validation on Add

**Principle**: Validate dependencies **immediately** after adding to charter.

**Workflow**:
```bash
# Scenario: Adding SAP-010 as dependency

# 1. Update capability-charter.md
vim docs/skilled-awareness/sap-061/capability-charter.md
# Add: **Dependencies**: SAP-000, SAP-050, SAP-010

# 2. Validate dependencies immediately (before continuing work)
python scripts/validate-ecosystem-integration.py SAP-061
# Expected: ✅ Pass (if SAP-010 exists)
# Or: ❌ Fail (if SAP-010 does not exist)

# 3. If fail, resolve immediately
# Option A: Create SAP-010 (if needed)
# Option B: Remove SAP-010 from dependencies (if incorrect)

# 4. Continue work (dependencies validated)
```

**Benefits**:
- ✅ Catch broken dependencies immediately (not at commit time)
- ✅ Prevents downstream work with invalid dependencies
- ✅ Clear feedback loop (add dependency → validate → resolve → continue)

**Time Saved**: 2-5 minutes (catch errors early)

---

## SAP Development Lifecycle Integration

### Phase 1: Design (L0 → L1)

**Integration Requirements**: INDEX.md entry (placeholder OK)

**Workflow**:
```bash
# 1. Create SAP directory
mkdir docs/skilled-awareness/sap-061

# 2. Add INDEX.md placeholder
vim docs/skilled-awareness/INDEX.md
# Add: #### SAP-061: [Title TBD] (draft)

# 3. Write capability-charter.md
# (Include metadata: status=draft, dependencies)

# 4. Validate
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass (draft only requires INDEX + dependencies)

# 5. Commit
git commit -m "feat(sap-061): Phase 1 design complete"
```

**Time**: 10-15 minutes

---

### Phase 2: Infrastructure (L1 → L2)

**Integration Requirements**: INDEX.md complete, catalog entry (if promoting to pilot)

**Workflow**:
```bash
# 1. Complete capability-charter.md (no placeholders)
vim docs/skilled-awareness/sap-061/capability-charter.md

# 2. Write protocol-spec.md, awareness-guide.md

# 3. Update INDEX.md (finalize description, features)
vim docs/skilled-awareness/INDEX.md

# 4. Decide: Stay draft or promote to pilot?
# If pilot: Add catalog + copier (see Phase 3)
# If draft: No additional integration needed

# 5. Validate
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass

# 6. Commit
git commit -m "feat(sap-061): Phase 2 infrastructure complete"
```

**Time**: 2-4 hours (writing artifacts), 5-10 minutes (integration updates)

---

### Phase 3: Pilot (L2 → L3)

**Integration Requirements**: Catalog + copier (required for pilot status)

**Workflow**:
```bash
# 1. Add catalog entry
vim sap-catalog.json

# 2. Add copier integration
vim copier.yml

# 3. Validate pilot requirements
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass (pilot requirements met)

# 4. Update status field
vim docs/skilled-awareness/sap-061/capability-charter.md
# Update: **Status**: pilot

# 5. Update INDEX.md status
vim docs/skilled-awareness/INDEX.md
# Update: status: pilot

# 6. Register files in work context
just work-context-update tab-N

# 7. Commit
git commit -m "feat(sap-061): Promote to pilot (v1.0.0)"
```

**Time**: 10-15 minutes (catalog/copier updates + validation)

---

### Phase 4: Distribution (L3 → L4)

**Integration Requirements**: All 5 integration points (INDEX, catalog, copier, adoption path, dependencies)

**Workflow**:
```bash
# 1. Verify all artifacts complete
ls docs/skilled-awareness/sap-061/
# Expect: 5 artifacts

# 2. Add adoption path mention (recommended for active)
vim docs/skilled-awareness/INDEX.md
# Add SAP-061 to Progressive Adoption Path section

# 3. Validate all integration points
python scripts/validate-ecosystem-integration.py SAP-061 --verbose
# ✅ Pass (all 5 integration points)

# 4. Update status to active
vim docs/skilled-awareness/sap-061/capability-charter.md
# Update: **Status**: active

# 5. Update INDEX.md status
vim docs/skilled-awareness/INDEX.md
# Update: status: active

# 6. Commit
git commit -m "docs(sap-061): Promote to active (L4 - distributed)"

# 7. Close beads task
bd close chora-workspace-XXXX
```

**Time**: 10-15 minutes (adoption path + final validation)

---

## Multi-Tab Coordination

### Coordination Scenario 1: Multiple Tabs, Single SAP

**Problem**: tab-1 working on SAP-061 artifacts, tab-2 updating INDEX.md simultaneously → conflict risk.

**Solution**:

**tab-1** (SAP artifacts):
```yaml
# .chora/work-contexts.yaml
- id: tab-1
  files:
  - docs/skilled-awareness/sap-061/**/*
```

**tab-2** (INDEX.md + catalog):
```yaml
# .chora/work-contexts.yaml
- id: tab-2
  files:
  - docs/skilled-awareness/INDEX.md
  - sap-catalog.json
  - copier.yml
```

**Workflow**:
1. tab-1: Write SAP artifacts, commit (does NOT touch INDEX.md)
2. tab-2: Add INDEX.md entry, catalog entry, copier integration
3. tab-2: Validate ecosystem integration (includes SAP-061 artifacts from tab-1)
4. tab-2: Commit (pre-commit hook passes)
5. Both tabs: Merge without conflicts

**Benefit**: Clear file ownership, no conflicts

---

### Coordination Scenario 2: Multiple SAPs, Shared Files

**Problem**: tab-1 working on SAP-061, tab-2 working on SAP-062, both need to update INDEX.md → conflict.

**Solution**:

**Coordinate INDEX.md updates**:
```bash
# tab-1: Announce intent
just tab-announce-intent tab-1 "Updating INDEX.md for SAP-061"

# tab-2: Check tab status before editing
just tab-status
# Output: tab-1 working on INDEX.md

# tab-2: Wait for tab-1 to finish, then update
# Or: Coordinate merge (tab-1 commits first, tab-2 pulls and adds SAP-062 entry)
```

**Workflow**:
1. tab-1: Add SAP-061 to INDEX.md, commit, push
2. tab-2: Pull latest changes (includes SAP-061 entry)
3. tab-2: Add SAP-062 to INDEX.md (below SAP-061)
4. tab-2: Commit, push
5. Both tabs: No conflicts (sequential updates)

**Benefit**: Sequential INDEX.md updates prevent merge conflicts

---

### Coordination Scenario 3: Validation Across Tabs

**Problem**: tab-1 creates SAP-061 artifacts, tab-2 validates ecosystem → validation fails because tab-1 hasn't committed yet.

**Solution**:

**tab-1 workflow**:
```bash
# 1. Complete SAP-061 artifacts (all 5 files)
# 2. Add INDEX.md entry, catalog entry
# 3. Commit (make artifacts visible to other tabs)
git commit -m "feat(sap-061): Add SAP-061 artifacts + integration"
git push

# 4. Announce completion
just tab-announce-deliverable tab-1 SAP-061 "docs/skilled-awareness/sap-061/"
```

**tab-2 workflow**:
```bash
# 1. Check tab announcements
just tab-status

# 2. Pull latest changes (includes SAP-061 from tab-1)
git pull

# 3. Now validate ecosystem
python scripts/validate-ecosystem-integration.py --all
# ✅ Pass (SAP-061 visible after pull)
```

**Benefit**: Validation operates on committed state (no false negatives)

---

## Validation Commands Reference

### Basic Validation

```bash
# Validate single SAP (default text output)
python scripts/validate-ecosystem-integration.py SAP-061

# Validate single SAP (verbose output)
python scripts/validate-ecosystem-integration.py SAP-061 --verbose

# Validate single SAP (JSON output)
python scripts/validate-ecosystem-integration.py SAP-061 --json

# Validate all SAPs (summary output)
python scripts/validate-ecosystem-integration.py --all

# Validate all SAPs (JSON output for automation)
python scripts/validate-ecosystem-integration.py --all --json
```

### Filtering and Analysis

```bash
# Get failed SAPs only (using jq)
python scripts/validate-ecosystem-integration.py --all --json | \
  jq '.results | to_entries | map(select(.value.passed == false))'

# Get specific integration point failures (e.g., INDEX.md)
python scripts/validate-ecosystem-integration.py --all --json | \
  jq '.results | to_entries | map(select(.value.checks[] | select(.integration_point == "INDEX.md" and .passed == false)))'

# Count total failures
python scripts/validate-ecosystem-integration.py --all --json | jq '.failed'

# Get exit code
python scripts/validate-ecosystem-integration.py SAP-061
echo $?  # 0-6
```

### Pre-commit Hook Usage

```bash
# Run pre-commit hook manually on all files
pre-commit run validate-sap-ecosystem-integration --all-files

# Run pre-commit hook on staged files only
pre-commit run validate-sap-ecosystem-integration

# Skip pre-commit hooks (bypass validation)
git commit --no-verify -m "WIP: Incomplete integration"
```

---

## Troubleshooting

### Issue 1: Validation Passes Locally, Fails in CI

**Symptoms**:
- `python scripts/validate-ecosystem-integration.py SAP-061` passes on developer machine
- CI/CD pipeline fails with "SAP-061 NOT found in INDEX.md"

**Cause**: Developer committed SAP artifacts but NOT INDEX.md (forgot to add).

**Solution**:
```bash
# 1. Check git status
git status
# Output: modified: INDEX.md (not staged)

# 2. Stage INDEX.md
git add docs/skilled-awareness/INDEX.md

# 3. Amend previous commit
git commit --amend --no-edit

# 4. Push (force if already pushed)
git push --force-with-lease
```

**Prevention**: Use `--all` validation before pushing (catches missing files).

---

### Issue 2: Hook Times Out (>60s)

**Symptoms**:
- Pre-commit hook takes >60 seconds
- Git aborts commit with timeout error

**Cause**: Ecosystem has >100 SAPs, `--all` validation too slow.

**Solution**:
```yaml
# .pre-commit-config.yaml
# Change from --all to single-SAP validation
entry: python scripts/validate-ecosystem-integration.py {sap_id}  # Instead of --all
pass_filenames: true  # Pass modified SAP ID to script
```

**Trade-off**: Single-SAP validation faster (<2s) but doesn't catch cross-SAP issues.

---

### Issue 3: False Positive on Adoption Path

**Symptoms**:
- SAP mentioned in INDEX.md but validation says "NOT mentioned in Progressive Adoption Path"

**Cause**: SAP mentioned in wrong section (e.g., domain section instead of adoption path section).

**Solution**:
```bash
# 1. Find "Progressive Adoption Path" section in INDEX.md
grep -A 100 "## Progressive Adoption Path" docs/skilled-awareness/INDEX.md

# 2. Verify SAP-061 mentioned in this section specifically
# If not, add SAP-061 under appropriate adoption path

# 3. Revalidate
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass
```

**Prevention**: Use verbose output to see section boundaries: `--verbose`

---

### Issue 4: Dependencies Check Fails for SAP-000

**Symptoms**:
- Validation fails: "Broken dependencies: SAP-000"

**Cause**: SAP-000 directory missing or lacks capability-charter.md.

**Solution**:
```bash
# 1. Verify SAP-000 exists
ls docs/skilled-awareness/ | grep sap-000

# 2. If missing, create SAP-000 (foundational SAP)
mkdir docs/skilled-awareness/sap-000-framework
touch docs/skilled-awareness/sap-000-framework/capability-charter.md
# Add: **SAP ID**: SAP-000

# 3. Revalidate
python scripts/validate-ecosystem-integration.py SAP-061
# ✅ Pass
```

**Prevention**: SAP-000 should always exist (foundational), check during repo initialization.

---

## Summary

**Key Takeaways for Claude Code Agents**:

1. **Always validate before commit**: `python scripts/validate-ecosystem-integration.py SAP-XXX`
2. **Use integration-first development**: Add INDEX + catalog before writing artifacts
3. **Follow status-based requirements**: draft (INDEX + deps), pilot (+catalog + copier), active (all 5)
4. **Fix work context conflicts first**: Work context hook runs before ecosystem validation
5. **Coordinate INDEX.md updates**: Use multi-tab coordination for shared files
6. **Batch integration updates**: Commit INDEX + catalog + copier together (atomic)
7. **Use --no-verify sparingly**: Only for intentional WIP commits, complete integration before merge

**Performance**:
- Single SAP validation: <2s
- All SAPs validation: ~8-10s (for ~50 SAPs)
- Pre-commit hook: <1s (typical case, 1-2 SAPs modified)

**Integration Gaps Prevented**:
- INDEX.md omission (most common, like SAP-053 trigger case)
- Catalog missing (blocks automation)
- Copier misconfiguration (blocks distribution)
- Broken dependencies (data integrity)

---

**Related Documents**:
- [capability-charter.md](capability-charter.md) - Problem statement and solution overview
- [protocol-spec.md](protocol-spec.md) - Technical validation specifications
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan
- [ledger.md](ledger.md) - SAP-061 adoption tracking

---

**Document Status**: Draft (Phase 1 - Design)
**Next Milestone**: Phase 2 (Infrastructure) - validation script complete, pre-commit hook added
**For**: Claude Code agents, human developers, automation tools
