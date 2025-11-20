# chora-base Distribution Strategy Decision

**Date**: 2025-11-21
**Context**: CORD-2025-023 Phase 2.2 Completion
**Decision Required**: How to distribute chora-base template for `copier update` support
**Status**: ⏳ Awaiting Decision

---

## Executive Summary

The chora-base Copier template requires git-tracked remote URL distribution to enable `copier update` functionality. Three viable strategies exist, each with different trade-offs for maintenance, user experience, and ecosystem integration.

**Quick Comparison**:

| Strategy | `copier update` Support | Setup Complexity | Best For |
|----------|------------------------|------------------|----------|
| **A: GitHub Release** | ✅ Works perfectly | Low | Public distribution |
| **B: Git Submodule** | ⚠️ Requires manual submodule update | Medium | Monorepo coordination |
| **C: Separate Repo** | ✅ Works perfectly | Medium | Clean separation |

**Recommendation**: **Option A (GitHub Release)** for immediate public distribution, with Option C (Separate Repo) for long-term scalability.

---

## Problem Statement

### Background

During Phase 2.2 validation (chora-workspace-inr3), we discovered that `copier update` **requires** the template source to be a git-trackable remote URL, not a local file path.

**Technical Limitation**:
```bash
# ❌ Does NOT work:
$ copier copy /local/path/to/template my-project
$ cd my-project && copier update
Error: Updating is only supported in git-tracked templates.

# ✅ DOES work:
$ copier copy https://github.com/user/template.git my-project
$ cd my-project && copier update
# Fetches latest template changes successfully
```

**Root Cause**: Copier's update mechanism expects `_src_path` in `.copier-answers.yml` to be a URL it can fetch updates from (via `git fetch`).

### Impact

Without choosing a distribution strategy:
- ❌ Users cannot run `copier update` to receive template improvements
- ❌ Phase 3 pilot testing blocked (cannot validate update propagation)
- ❌ Template distribution unclear (how do users access chora-base?)

---

## Distribution Strategy Options

### Option A: GitHub Release (Direct Distribution)

**Overview**: Push chora-base to GitHub as-is. Users install directly from GitHub URL.

**User Installation**:
```bash
# Install from GitHub:
copier copy https://github.com/liminalcommons/chora-base.git my-project

# Update later:
cd my-project
copier update  # Fetches latest from GitHub
```

**Architecture**:
```
GitHub Repository: liminalcommons/chora-base
├── copier.yml
├── template/
├── copier-post-generation.py
└── ... (all current structure)

User's .copier-answers.yml:
_src_path: https://github.com/liminalcommons/chora-base.git
_commit: <git-hash-when-generated>
```

**Pros**:
- ✅ **Simplest setup**: No infrastructure changes needed
- ✅ **`copier update` works immediately**: Users can update out-of-the-box
- ✅ **Version tagging**: Use git tags for stable releases (v1.0.0, v1.1.0)
- ✅ **Clear provenance**: GitHub URL in `.copier-answers.yml` shows origin
- ✅ **Low maintenance**: Single repository, no coordination overhead
- ✅ **Fast time-to-pilot**: Can start Phase 3 immediately

**Cons**:
- ⚠️ **Template mixed with source**: chora-base repo contains both template and project structure
- ⚠️ **Git submodule complexity**: chora-base has nested submodules that complicate cloning
- ⚠️ **No separation of concerns**: Template distribution tied to project development
- ⚠️ **User confusion**: Users see entire chora-base structure, not just template

**Best For**:
- Quick pilot testing (Phase 3)
- Internal use within chora ecosystem
- MVP distribution before scaling

**Implementation Effort**: **Low (2-3 hours)**
1. Push chora-base to GitHub (if not already public)
2. Tag first release: `git tag v1.0.0 && git push --tags`
3. Update README.md with installation instructions
4. Test copier copy and update with GitHub URL

---

### Option B: Git Submodule in Monorepo

**Overview**: Keep chora-base as git submodule within chora-workspace. Users clone monorepo, then install template from submodule path.

**User Installation**:
```bash
# Clone monorepo:
git clone https://github.com/liminalcommons/chora-workspace.git
cd chora-workspace
git submodule update --init --recursive

# Install from submodule:
copier copy ./packages/chora-base my-project

# Update later:
cd packages/chora-base && git pull
cd ../../my-project && copier update
```

**Architecture**:
```
chora-workspace/
├── packages/
│   ├── chora-base/          ← Git submodule (template source)
│   ├── chora-compose/       ← Sibling project
│   └── ...
└── README.md

User's .copier-answers.yml:
_src_path: /path/to/chora-workspace/packages/chora-base
_commit: <git-hash-when-generated>
```

**Pros**:
- ✅ **Monorepo coordination**: Single chora-workspace repo for all projects
- ✅ **Template source controlled**: chora-base development tracked in workspace
- ✅ **Version pinning**: Submodule pin specific template versions
- ✅ **Internal distribution**: Good for multi-developer chora teams

**Cons**:
- ⚠️ **Manual submodule update**: Users must `git pull` in submodule before `copier update`
- ⚠️ **Complex workflow**: Two-step update (submodule pull → copier update)
- ⚠️ **User confusion**: Requires understanding of git submodules
- ⚠️ **Not public-friendly**: External users must clone entire monorepo
- ⚠️ **Local path limitation**: `_src_path` still a local path (copier may reject updates)

**Best For**:
- Internal chora team development
- Multi-project coordination (chora-base + chora-compose + castalia)
- When template and projects co-evolve frequently

**Implementation Effort**: **Medium (4-6 hours)**
1. Add chora-base as submodule: `git submodule add <url> packages/chora-base`
2. Update workspace documentation with submodule workflow
3. Test copier copy from submodule path
4. Validate update propagation (may still hit local path limitation)

**⚠️ Risk**: Copier may still reject updates from local submodule path. Requires validation.

---

### Option C: Separate Template Repository

**Overview**: Create dedicated `chora-base-template` repository containing only template files. Separate from chora-base project development.

**User Installation**:
```bash
# Install from dedicated template repo:
copier copy https://github.com/liminalcommons/chora-base-template.git my-project

# Update later:
cd my-project
copier update  # Works seamlessly
```

**Architecture**:
```
Repository 1: liminalcommons/chora-base
├── docs/               ← Project documentation
├── scripts/            ← Development scripts
├── ... (project structure)
└── README.md

Repository 2: liminalcommons/chora-base-template
├── copier.yml
├── template/
├── copier-post-generation.py
└── README.md           ← Template-specific README

User's .copier-answers.yml:
_src_path: https://github.com/liminalcommons/chora-base-template.git
_commit: <git-hash-when-generated>
```

**Pros**:
- ✅ **Clean separation**: Template distribution separate from project development
- ✅ **`copier update` works perfectly**: No manual steps for users
- ✅ **Easiest for external users**: Simple, single-purpose repository
- ✅ **Template-specific versioning**: Git tags for template releases independent of project
- ✅ **No submodule complexity**: Users don't see nested submodules
- ✅ **Scalable**: Best long-term architecture for public distribution

**Cons**:
- ⚠️ **Two repositories to maintain**: chora-base and chora-base-template
- ⚠️ **Sync overhead**: Changes to SAPs must be propagated to template repo
- ⚠️ **Initial setup effort**: Requires creating and configuring second repository
- ⚠️ **CI/CD coordination**: Template updates may require automated sync from chora-base

**Best For**:
- Public distribution to external users
- Long-term scalability
- When template stability is important (fewer breaking changes)

**Implementation Effort**: **Medium (6-8 hours)**
1. Create new repository: `chora-base-template`
2. Copy template files from chora-base:
   - `copier.yml`
   - `template/` directory
   - `copier-post-generation.py`
   - Template-specific README
3. Set up CI/CD to sync template changes from chora-base (optional)
4. Tag first release: `git tag v1.0.0 && git push --tags`
5. Update chora-base README with link to template repo
6. Test copier copy and update with template repo URL

---

## Decision Matrix

### Evaluation Criteria

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **`copier update` Support** | High | ✅ 10/10 | ⚠️ 5/10 | ✅ 10/10 |
| **Setup Complexity** | Medium | ✅ 9/10 | ⚠️ 6/10 | ⚠️ 7/10 |
| **User Experience** | High | ✅ 8/10 | ❌ 4/10 | ✅ 10/10 |
| **Maintenance Overhead** | High | ✅ 9/10 | ⚠️ 7/10 | ⚠️ 6/10 |
| **Scalability** | Medium | ⚠️ 6/10 | ⚠️ 5/10 | ✅ 10/10 |
| **Time to Pilot** | High | ✅ 10/10 | ⚠️ 7/10 | ⚠️ 6/10 |
| **Public Distribution** | High | ✅ 8/10 | ❌ 3/10 | ✅ 10/10 |
| **Monorepo Integration** | Low | ⚠️ 5/10 | ✅ 9/10 | ❌ 3/10 |
| **Total (Weighted)** | - | **82/100** | **54/100** | **80/100** |

**Scoring**:
- ✅ 10/10 = Excellent
- ✅ 8-9/10 = Good
- ⚠️ 5-7/10 = Acceptable
- ❌ 3-4/10 = Poor

---

## Recommendations

### Recommended Strategy: Hybrid Approach

**Phase 3 (Immediate - Pilot Testing)**:
→ **Use Option A (GitHub Release)**

**Rationale**:
- Fastest time-to-pilot (2-3 hours setup)
- Validates `copier update` workflow immediately
- Allows Phase 3 testing to proceed without delay
- Low risk, reversible decision

**Action Items**:
1. Tag chora-base v1.0.0
2. Update README with installation instructions
3. Test in Phase 3.1 (chora-workspace pilot)
4. Validate update propagation in Phase 3.2 (castalia pilot)

---

**Phase 4 (Long-term - Public Distribution)**:
→ **Migrate to Option C (Separate Template Repository)**

**Rationale**:
- Best user experience for external users
- Clean separation of concerns
- Scalable for public adoption
- No submodule complexity

**Action Items**:
1. Create `chora-base-template` repository (post-Phase 3)
2. Migrate template files and documentation
3. Set up CI/CD for template sync (optional)
4. Update chora-base README to point to template repo
5. Communicate migration to Phase 3 pilot users

**Migration Path**:
Existing users on Option A can migrate to Option C:
```bash
# Update .copier-answers.yml:
_src_path: https://github.com/liminalcommons/chora-base-template.git

# Run copier update:
copier update
```

---

### Alternative Recommendation: Option C Only

If setup time for separate repo is acceptable (6-8 hours), **skip Option A and go directly to Option C**.

**When to Choose This**:
- Public distribution is primary goal
- Willing to invest 6-8 hours upfront
- Want to avoid migration overhead later
- Template stability is important

---

## Implementation Plans

### Implementation: Option A (GitHub Release)

**Estimated Time**: 2-3 hours

**Steps**:

1. **Verify GitHub Repository** (15 minutes)
   ```bash
   # Check if chora-base is already on GitHub:
   cd packages/chora-base
   git remote -v

   # If not, add remote:
   git remote add origin https://github.com/liminalcommons/chora-base.git
   git push -u origin main
   ```

2. **Tag First Release** (10 minutes)
   ```bash
   # Tag v1.0.0:
   git tag -a v1.0.0 -m "chora-base template v1.0.0 - Initial public release"
   git push --tags

   # Verify tag:
   git tag -l
   ```

3. **Update README.md** (30 minutes)
   - Add "Installation" section with GitHub URL
   - Document `copier update` workflow
   - Link to template documentation

4. **Test Installation** (60 minutes)
   ```bash
   # Test copier copy from GitHub:
   copier copy https://github.com/liminalcommons/chora-base.git test-install-v1

   # Verify files:
   cd test-install-v1
   ls -la

   # Test copier update:
   # (Make small template change, commit, then update)
   copier update
   ```

5. **Create Release Notes** (30 minutes)
   - Document SAPs included (8 SAPs)
   - List known limitations
   - Link to COPIER-QUESTIONNAIRE-DESIGN.md

**Validation Checklist**:
- [ ] chora-base pushed to GitHub
- [ ] v1.0.0 tag created and pushed
- [ ] README.md updated with installation instructions
- [ ] Test project generated successfully
- [ ] `copier update` tested and validated
- [ ] Release notes created

---

### Implementation: Option C (Separate Template Repository)

**Estimated Time**: 6-8 hours

**Steps**:

1. **Create Template Repository** (30 minutes)
   ```bash
   # Create new repo on GitHub: chora-base-template
   # Clone locally:
   git clone https://github.com/liminalcommons/chora-base-template.git
   cd chora-base-template
   ```

2. **Copy Template Files** (60 minutes)
   ```bash
   # From chora-base, copy template files:
   cp -r ../chora-base/copier.yml .
   cp -r ../chora-base/template .
   cp ../chora-base/copier-post-generation.py .

   # Copy essential documentation:
   mkdir docs
   cp ../chora-base/COPIER-QUESTIONNAIRE-DESIGN.md docs/
   cp ../chora-base/README.md docs/TEMPLATE-ORIGIN.md

   # Create template-specific README:
   # (See template below)
   ```

3. **Create Template README.md** (60 minutes)
   - Document template installation
   - List SAPs included
   - Link to chora-base for SAP definitions
   - Document update workflow
   - Include contribution guide

4. **Version Alignment** (30 minutes)
   ```bash
   # Tag with matching version:
   git add -A
   git commit -m "Initial template repository v1.0.0"
   git tag -a v1.0.0 -m "chora-base-template v1.0.0"
   git push -u origin main --tags
   ```

5. **Update chora-base** (30 minutes)
   - Update chora-base README to link to template repo
   - Document template sync workflow (for maintainers)
   - Create TEMPLATE-SYNC.md guide

6. **Test Installation** (90 minutes)
   ```bash
   # Test from template repo:
   copier copy https://github.com/liminalcommons/chora-base-template.git test-template-v1

   # Verify files:
   cd test-template-v1
   just --list

   # Test update:
   # (Make template change, commit, update)
   cd ../chora-base-template
   # ... make change ...
   git commit -am "Add new justfile recipe"
   cd ../test-template-v1
   copier update
   ```

7. **Optional: CI/CD Setup** (120 minutes)
   - Create GitHub Action to sync template from chora-base
   - Trigger on chora-base commits to template files
   - Automated testing of template generation

**Validation Checklist**:
- [ ] chora-base-template repository created
- [ ] Template files copied correctly
- [ ] Template README.md written
- [ ] v1.0.0 tag created
- [ ] chora-base README updated with template link
- [ ] Test project generated successfully
- [ ] `copier update` tested and validated
- [ ] (Optional) CI/CD workflow configured

---

## Risks and Mitigations

### Risk 1: Git Submodule Complexity (Option A)

**Risk**: chora-base contains nested git submodules that may cause cloning issues for users.

**Likelihood**: Medium
**Impact**: Medium (user confusion, failed installations)

**Mitigation**:
- Document submodule cloning: `git clone --recurse-submodules`
- Provide troubleshooting guide for submodule errors
- Consider flattening submodules in template (separate docs from template)
- **Long-term**: Migrate to Option C to avoid this issue

---

### Risk 2: Template-Project Sync Overhead (Option C)

**Risk**: Changes to SAPs in chora-base must be manually synced to chora-base-template, creating maintenance overhead.

**Likelihood**: High (frequent SAP updates expected)
**Impact**: Medium (template lags behind chora-base)

**Mitigation**:
- Automate sync with CI/CD (GitHub Actions)
- Create TEMPLATE-SYNC.md guide for manual sync
- Schedule weekly sync reviews
- Use git tags to track which chora-base version corresponds to template version

**Automation Example** (GitHub Actions):
```yaml
name: Sync Template from chora-base

on:
  workflow_dispatch:  # Manual trigger
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout chora-base-template
        uses: actions/checkout@v3

      - name: Fetch chora-base changes
        run: |
          git remote add chora-base https://github.com/liminalcommons/chora-base.git
          git fetch chora-base

      - name: Copy template files
        run: |
          cp -r chora-base/main:copier.yml .
          cp -r chora-base/main:template .
          cp chora-base/main:copier-post-generation.py .

      - name: Create PR
        # ... create PR for review
```

---

### Risk 3: User Migration Overhead (A → C)

**Risk**: Users who adopt Option A in Phase 3 will need to migrate to Option C later.

**Likelihood**: High (if hybrid approach used)
**Impact**: Low (migration is straightforward)

**Mitigation**:
- Document migration path upfront
- Provide migration guide with exact steps
- Offer migration support during transition
- Communicate migration timeline early (end of Phase 3)

**Migration Guide**:
```bash
# Update .copier-answers.yml:
sed -i 's|_src_path: https://github.com/liminalcommons/chora-base.git|_src_path: https://github.com/liminalcommons/chora-base-template.git|' .copier-answers.yml

# Run copier update:
copier update

# Verify update:
git diff
just --list
```

---

## Decision Log

### Decision Required

**Question**: Which distribution strategy should chora-base adopt?

**Options**:
1. **Option A**: GitHub Release (immediate)
2. **Option B**: Git Submodule (monorepo)
3. **Option C**: Separate Template Repository (long-term)
4. **Hybrid**: Option A → Option C migration

**Decision Maker**: Project maintainer / chora-workspace lead

**Deadline**: Before Phase 3.1 (chora-workspace pilot) begins

**Recommendation**: Hybrid (Option A for Phase 3, migrate to Option C for Phase 4)

---

### Decision Template

**Date**: [YYYY-MM-DD]
**Decided By**: [Name]
**Decision**: [Option A / B / C / Hybrid]
**Rationale**: [Why this option?]
**Next Steps**: [What to do next?]

---

## References

### Related Documents

- **Phase 2.2 Completion**: [.chora/memory/knowledge/notes/2025-11-21-phase-2-2-copier-update-validation.md](../../.chora/memory/knowledge/notes/2025-11-21-phase-2-2-copier-update-validation.md)
- **Copier Questionnaire Design**: [COPIER-QUESTIONNAIRE-DESIGN.md](../COPIER-QUESTIONNAIRE-DESIGN.md)
- **SAP-060 Capability Charter**: [docs/skilled-awareness/strategic-opportunity-management/capability-charter.md](../docs/skilled-awareness/strategic-opportunity-management/capability-charter.md)

### External Resources

- **Copier Documentation**: https://copier.readthedocs.io
- **Copier Update Workflow**: https://copier.readthedocs.io/en/stable/updating/
- **Git Submodules**: https://git-scm.com/book/en/v2/Git-Tools-Submodules
- **GitHub Releases**: https://docs.github.com/en/repositories/releasing-projects-on-github

---

**Created**: 2025-11-21
**Status**: ⏳ Awaiting Decision
**Trace ID**: cord-2025-023-distribution-strategy
**SAP**: SAP-060 Strategic Opportunity Management
