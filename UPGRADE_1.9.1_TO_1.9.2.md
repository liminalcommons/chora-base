# Upgrade Guide: chora-base v1.9.1 → v1.9.2

**Release Date:** 2025-10-22
**Focus:** AGENTS.md Ergonomic Feature Discovery

## Overview

Version 1.9.2 enhances AGENTS.md to surface optional features (Docker, documentation, CI/CD) for better agent discoverability. This is a **documentation-only enhancement** with **no breaking changes**.

## Who Should Upgrade?

### Immediate Upgrade Recommended:
- ✅ All projects (low risk, documentation only)
- ✅ Projects using Docker, documentation, or CI features
- ✅ Projects with AI agents that consult AGENTS.md

### Impact:
- ⏸️ **Zero code changes required**
- ⏸️ **Zero configuration changes required**
- ✅ **Enhanced agent discoverability** of existing features

## What Changed?

### AGENTS.md Template Updates (~150 lines added):

**New Sections Added:**

1. **Docker Operations** (conditional on `include_docker`)
   - Lists all 17 docker-* commands
   - Common workflows (build, verify, compose)
   - Links to DOCKER_BEST_PRACTICES.md
   - Clarifies adopter wiring responsibilities

2. **Documentation System** (conditional on `include_documentation_standard`)
   - Documents docs_metrics.py, query_docs.py, extract_tests.py
   - Explains health scoring system (0-100)
   - Emphasizes JSON API for agents

3. **CI/CD Expectations** (conditional on `include_github_actions`)
   - Lists 7 GitHub Actions workflows
   - Explains what CI checks before merge
   - Shows local verification steps

**Pattern Documentation:**
- Added Jinja comment documenting standard pattern for future features
- Establishes "capability catalog" philosophy for AGENTS.md

### No Other Changes:
- ❌ No template files changed (Docker, justfile, etc.)
- ❌ No copier.yml changes
- ❌ No new features added
- ❌ No behavior changes

## Upgrade Steps

### Step 1: Update Template

```bash
# From your project root
copier update

# Review changes
git diff
```

**Expected changes:** Only `AGENTS.md` will be updated with new feature sections.

### Step 2: Review New Sections

```bash
# View updated AGENTS.md
cat AGENTS.md | grep "###"
```

**New sections you'll see (if features enabled):**
- `### Docker Operations`
- `### Documentation System`
- `### CI/CD Expectations`

### Step 3: No Testing Required

Since this is documentation-only, no testing is required. The changes only affect how agents discover features, not how features work.

### Step 4: Commit Changes

```bash
git add AGENTS.md
git commit -m "docs(agents): Update AGENTS.md from chora-base v1.9.2

- Add Docker Operations section
- Add Documentation System section
- Add CI/CD Expectations section"
```

## Breaking Changes

**None.** This is a documentation-only release.

## New Capabilities for Agents

Agents working in your project can now:

1. **Discover Docker commands** via AGENTS.md (previously required reading DOCKER_BEST_PRACTICES.md directly)
2. **Understand documentation tooling** (docs_metrics.py, query_docs.py)
3. **Know what CI will check** before creating PRs
4. **See adopter wiring responsibilities** clearly separated from template features

## If You Customized AGENTS.md

If you manually edited AGENTS.md:

1. **Backup your customizations:**
   ```bash
   cp AGENTS.md AGENTS.md.custom
   ```

2. **Update template:**
   ```bash
   copier update
   ```

3. **Merge customizations:**
   - Review `git diff AGENTS.md`
   - Merge your custom content with new feature sections
   - Keep new sections (Docker, Documentation, CI/CD) intact

## Benefits After Upgrade

### For AI Agents:
- ✅ Discover all capabilities via single document (AGENTS.md)
- ✅ Clear separation of template vs. adopter responsibilities
- ✅ Links to detailed guides (no duplication)
- ✅ Expected metrics for each feature

### For Human Developers:
- ✅ Better understanding of what agents can discover
- ✅ Clear documentation of wiring responsibilities
- ✅ Standard pattern for future feature additions

## Troubleshooting

### Issue: AGENTS.md conflicts during update

**Cause:** You customized AGENTS.md sections that were updated

**Solution:**
```bash
# Accept template version first
copier update --force

# Then re-apply your customizations
# Keep new feature sections, merge your custom content
```

### Issue: New sections show "Feature Not Enabled"

**Cause:** Features are conditionally rendered based on copier.yml answers

**Solution:** This is expected. Sections only appear if you enabled the feature:
- `include_docker: true` → Shows Docker Operations
- `include_documentation_standard: true` → Shows Documentation System
- `include_github_actions: true` → Shows CI/CD Expectations

If you want to enable a feature:
```bash
copier recopy --vcs-ref=v1.9.2
# Answer YES when prompted for the feature
```

## Rollback Instructions

If needed, rollback to v1.9.1:

```bash
# Revert AGENTS.md changes
git checkout HEAD~1 -- AGENTS.md

# Or fully rollback template
copier update --vcs-ref=v1.9.1
```

## Testing Checklist

Since this is documentation-only:

- [ ] Review updated AGENTS.md
- [ ] Verify new sections match your enabled features
- [ ] No functional testing required
- [ ] Commit and push

## Timeline Estimate

- **Upgrade time:** 2-5 minutes
- **Review time:** 5-10 minutes
- **Risk level:** Very Low (documentation only)

## Additional Resources

- **CHANGELOG.md** - Detailed technical changes
- **README.md** - v1.9.2 highlights
- **Commit:** [334c1f0](https://github.com/liminalcommons/chora-base/commit/334c1f0)

## Questions or Issues?

1. **Review AGENTS.md sections** - Ensure they match your enabled features
2. **Check copier.yml** - Verify feature flags are set correctly
3. **Open an issue** - If you encounter problems

---

**Version:** v1.9.2
**Release Date:** 2025-10-22
**Upgrade Difficulty:** Very Easy (2-5 minutes)
**Breaking Changes:** None
**Category:** Documentation Enhancement
