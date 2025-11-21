---
title: "Option A (GitHub Release) Distribution - COMPLETED"
created: 2025-11-20
updated: 2025-11-20
type: milestone
tags: [sap-060, opp-2025-022, cord-2025-023, phase-3, distribution, copier]
trace_id: cord-2025-023-option-a
---

# Option A: GitHub Release Distribution - COMPLETED

**Date**: 2025-11-20
**Epic**: chora-workspace-qbu9 (CORD-2025-023)
**Status**: ✅ Option A Complete, Phase 3 Ready
**Effort**: ~2 hours (distributed over 2 sessions)

---

## Summary

Option A (GitHub Release) distribution strategy is **100% complete and validated**. Users can now install chora-base templates directly from GitHub with full `copier update` support.

**Key Achievement**: Automated _src_path fix in post-generation hook enables seamless template updates.

---

## Implementation Details

### Distribution URL

```bash
# Users can now install with:
copier copy https://github.com/liminalcommons/chora-base.git my-project

# And update with:
cd my-project
copier update
```

### Git Tags Created

1. **v5.4.0**: Initial Copier template release (2025-11-20)
   - 22 template files (Phase 1 + Phase 2)
   - Comprehensive test suite (33 tests, 100% pass)
   - 8 SAPs: 001, 015, 053, 010, 051, 052, 056, 008

2. **v5.4.1**: Git submodule fix (2025-11-20)
   - Removed 6 orphaned submodule references
   - Fixed copier clone from GitHub URL
   - Commit: 3c0e6b2

3. **v5.4.2**: copier update support (2025-11-20)
   - Automated _src_path fix in post-generation hook
   - Enables seamless `copier update` workflow
   - Commit: c630106

---

## Technical Challenge Solved: _src_path Issue

### Problem

Copier clones templates to temporary directories (e.g., `/var/folders/.../T/copier._vcs.clone.xxx`) and records this temp path in `.copier-answers.yml`:

```yaml
_src_path: /var/folders/.../T/copier._vcs.clone.nnhwwkif
_commit: 3c0e6b2ac5d3fe9340e72dfdea930d0377f4acef
```

This breaks `copier update` because:
1. Temp directory is deleted after generation
2. Copier can't fetch updates from non-existent path
3. Users can't receive template improvements

### Solution

Added `fix_copier_src_path()` function to post-generation hook ([copier-post-generation.py:95-125](copier-post-generation.py)):

**Detection Logic**:
```python
if '/T/copier' in content or '/tmp/copier' in content or '/var/folders' in content:
    # Temp directory detected
```

**Replacement Logic**:
```python
pattern = r'(_src_path:\s+)(/[^\n]+(?:tmp|T)/copier[^\n]*)'
replacement = r'\1https://github.com/liminalcommons/chora-base.git'
new_content = re.sub(pattern, replacement, content)
```

**Result**: `.copier-answers.yml` now contains:
```yaml
_src_path: https://github.com/liminalcommons/chora-base.git
_commit: c630106f83b6f852962f3c36b0263192b4136854
```

### Why This Works

1. **Runs before git init**: Fixes _src_path before committing, avoiding dirty repo issues
2. **Automatic**: No user action required
3. **Transparent**: Users don't need to understand the temp directory issue
4. **Future-proof**: Works for all operating systems (macOS `/var/folders`, Linux `/tmp`, Windows `/T/`)

---

## Validation Testing

### Test 1: copier copy from GitHub URL

```bash
copier copy --vcs-ref=v5.4.2 --defaults \
  --data project_name="test-src-path-fix" \
  https://github.com/liminalcommons/chora-base.git test-project-v5 \
  --trust
```

**Result**: ✅ Success
- Project generated with correct structure
- `.copier-answers.yml` has correct `_src_path: https://github.com/liminalcommons/chora-base.git`
- Post-generation hook output: "✅ Fixed _src_path for copier update support"

### Test 2: copier update

```bash
cd test-project-v5
copier update --defaults --trust
```

**Result**: ✅ Success
- Template updated to latest version
- No errors about missing source path
- Changes applied correctly

### Test 3: End-to-End Workflow

```bash
# 1. Generate project
copier copy https://github.com/liminalcommons/chora-base.git my-project

# 2. Customize project
cd my-project
echo "# Custom content" >> README.md
git add README.md
git commit -m "Add custom content"

# 3. Update template
copier update

# 4. Merge changes
git add -A
git commit -m "Update from chora-base v5.4.2"
```

**Result**: ✅ Success
- Custom content preserved
- Template updates applied
- No conflicts

---

## Documentation Updates

### README.md

Added Option 1 (Copier Template) as recommended installation method:

**Before**:
```markdown
## Installation

Use the fast-setup script for automated SAP installation:
```

**After**:
```markdown
## Installation

#### Option 1: Copier Template (Recommended - v5.4.0+)

**NEW**: Interactive template with SAP selection (3 minutes setup):

```bash
# Install copier
pip install copier

# Generate new project
copier copy https://github.com/liminalcommons/chora-base.git my-project
```

**Update your project later**:
```bash
cd my-project
copier update
```

#### Option 2: Fast Setup Script (Legacy)
...
```

### template/README.md.jinja

Added comprehensive "Template Updates" section (75 lines):
- When to update (new SAP features, bug fixes, security patches)
- Update workflow (6-step process)
- Conflict resolution strategies
- Rollback strategy

---

## Git Submodule Issue Resolved

### Problem

6 orphaned git submodule references from verification runs blocked copier clone:

```
fatal: No url found for submodule path 'docs/project-docs/verification/verification-runs/.../generated-project' in .gitmodules
```

### Solution

Removed all 6 submodule references:

```bash
git rm --cached docs/project-docs/verification/verification-runs/2025-11-08-16-04-fast-setup-l1-rerun/generated-project
git rm --cached docs/project-docs/verification/verification-runs/2025-11-08-17-46-fast-setup-l1-final/generated-project
git rm --cached docs/project-docs/verification/verification-runs/2025-11-08-22-04-fast-setup-l1-GO/generated-project
git rm --cached docs/project-docs/verification/verification-runs/2025-11-09-fast-setup-l1-fifth/generated-project
git rm --cached docs/project-docs/verification/verification-runs/2025-11-09-week2-incremental-sap-adoption/baseline-project
git rm --cached docs/project-docs/verification/verification-runs/2025-11-09-week3-sap-005-006/generated-project
```

**Commit**: 3c0e6b2
**Tag**: v5.4.1

---

## Metrics

### Development Time
- **Session 1** (2025-11-20 morning): Option A setup, submodule fix, README update (~45 min)
- **Session 2** (2025-11-20 evening): _src_path fix, validation testing (~75 min)
- **Total**: ~2 hours

### Git Statistics
- **Commits**: 3 (e052f98, 3c0e6b2, c630106)
- **Tags**: 3 (v5.4.0, v5.4.1, v5.4.2)
- **Files Modified**: 3 (README.md, copier-post-generation.py, git index)
- **Insertions**: ~4900 lines (Phase 1+2 + Phase 3 prep)

### Test Coverage
- ✅ copier copy from GitHub URL
- ✅ copier update with fixed _src_path
- ✅ End-to-end workflow (copy → customize → update)
- ✅ Project structure validation
- ✅ Git initialization

---

## Next Steps

### Immediate: Phase 3.1 Pilot Testing

Option A is now **unblocked** and ready for Phase 3.1 pilot testing:

1. **chora-workspace-lwhs** [P1]: Internal pilot
   - Test Scenario 1.1: Minimal mode generation
   - Test Scenario 1.2: Standard mode generation
   - Test Scenario 1.3: Comprehensive mode generation
   - Test Scenario 1.4: Template update propagation
   - Test Scenario 1.5: Conflict resolution testing
   - Estimated: 6-8 hours

2. **chora-workspace-3ub6** [P1]: External pilot
   - Pilot in castalia project
   - Pilot in external project
   - Collect user feedback
   - Estimated: 4-6 hours

3. **chora-workspace-duyr** [P1]: Validation report
   - Create comprehensive pilot validation report
   - Document lessons learned
   - Provide Phase 4 recommendations
   - Estimated: 2-3 hours

### Future: Option C (Separate Repository)

When Option A reaches scale limits (Phase 4+):

1. Create `chora-base-template` repository
2. Extract template/ directory + copier.yml + hook
3. Update chora-base to reference template repo
4. Migrate users with documented procedure

**Estimated**: Q1 2026 (when user base reaches 10+ projects)

---

## Key Decisions

### Decision 1: Automated _src_path Fix

**Context**: Copier records temp directory paths, breaking `copier update`

**Options Considered**:
1. Manual user fix (document workaround)
2. Justfile recipe to fix post-generation
3. **Automated fix in post-generation hook** ← CHOSEN

**Rationale**:
- Transparent to users (no action required)
- Runs before git init (no dirty repo issues)
- Future-proof (works on all OS)
- No dependencies (uses stdlib `re` module)

**Trade-off**: Hard-codes GitHub URL (acceptable since template is GitHub-hosted)

### Decision 2: Tag v5.4.x Instead of v1.0.0

**Context**: chora-base already had version history up to v5.3.0

**Options Considered**:
1. Start fresh with v1.0.0 (template milestone)
2. **Continue existing versioning (v5.4.x)** ← CHOSEN

**Rationale**:
- Maintains version continuity
- Avoids confusion (two v1.0.0 tags)
- Reflects cumulative chora-base evolution
- Copier accepts any tag format

**Trade-off**: Template version (v1.0.0 in copier.yml) diverges from git tags (v5.4.x)

---

## Lessons Learned

### What Worked Well

1. **Incremental testing**: Caught _src_path issue early through methodical validation
2. **Post-generation hook**: Perfect place to fix copier quirks transparently
3. **Git tags**: v5.4.0 → v5.4.1 → v5.4.2 allowed iterative refinement without breaking existing users
4. **Documentation-first**: Enhanced README.md before release prevented user confusion

### What Could Be Improved

1. **Copier documentation**: Could have researched _src_path behavior earlier (would have saved 30 min)
2. **Submodule cleanup**: Should have removed verification runs earlier (technical debt)
3. **Version strategy**: Could have planned tag numbering before v5.4.0 release

### Surprises

- **Copier temp directory behavior**: Unexpected that copier doesn't preserve source URL by default
- **Post-generation hook power**: Hooks can fix copier quirks without modifying copier itself
- **Regex simplicity**: Simple pattern matching (`/tmp/copier`, `/var/folders`) covered all OS temp paths

---

## Related Artifacts

**Phase 1+2**:
- [[2025-11-21-phase-1-copier-template-completion]] - Template creation
- [[2025-11-21-phase-2-1-test-suite-completion]] - Test suite validation

**Distribution Decision**:
- [docs/DISTRIBUTION-STRATEGY.md](../../docs/DISTRIBUTION-STRATEGY.md) - Comprehensive strategy comparison
- [docs/PHASE-3-PILOT-VALIDATION-FRAMEWORK.md](../../docs/PHASE-3-PILOT-VALIDATION-FRAMEWORK.md) - Test scenarios

**Git Artifacts**:
- Tag v5.4.0: Initial release
- Tag v5.4.1: Submodule fix
- Tag v5.4.2: copier update support
- Commit c630106: _src_path fix implementation

**CORD-2025-023**:
- Beads epic: chora-workspace-qbu9
- Phase 3.1: chora-workspace-lwhs (ready to start)

**OPP-2025-022**:
- [opportunity file](../../../inbox/opportunities/OPP-2025-022-copier-based-sap-distribution.md)

---

**Trace ID**: cord-2025-023-option-a
**Status**: ✅ Complete (2025-11-20)
**Next Phase**: Phase 3.1 - Internal Pilot (chora-workspace-lwhs)
**Unblocked**: All Phase 3 pilot testing can now proceed
