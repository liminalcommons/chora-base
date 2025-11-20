# SAP Distribution & Versioning: Awareness Guide

**SAP ID**: SAP-062
**Version**: 1.0.0
**Status**: draft
**Last Updated**: 2025-11-20

---

## Quick Reference for AI Agents

### When to Use SAP-062

**Use SAP-062 when**:
- ✅ Creating new project from chora-base template
- ✅ Updating existing project with template improvements
- ✅ Adding new SAP to template (template maintainer)
- ✅ Versioning SAP release (template maintainer)
- ✅ Resolving template update conflicts

**Don't use SAP-062 when**:
- ❌ Validating SAP structure (use SAP-061 Ecosystem Integration)
- ❌ Tracking SAP adoption metrics (use SAP-050 Development Lifecycle)
- ❌ Generating new SAP artifacts (use SAP-029 SAP Generation)
- ❌ Creating coordination requests (use SAP-001 Inbox)

### Key Commands

```bash
# Generate new project from template
copier copy gh:liminalcommons/chora-base my-project

# Update existing project with template improvements
copier update

# Update to specific template version
copier update --vcs-ref v1.2.0

# Check current template version
cat .copier-answers.yml | grep _commit
```

### Success Criteria Checklist

Before completing SAP-062 work:
- ✅ Template generates project in <3 min
- ✅ All SAP scripts executable in generated project
- ✅ `copier update` applies cleanly (no unresolved conflicts)
- ✅ CHANGELOG.md updated with version notes
- ✅ Migration guide written (if MAJOR version bump)

---

## Agent Workflows

### Workflow 1: Creating New Project from Template

**Scenario**: User wants to create new project with chora-base template

**Steps**:

1. **Install Copier** (if not already installed)
   ```bash
   # Check if Copier is installed
   copier --version

   # If not installed:
   pipx install copier
   # or: pip install copier
   ```

2. **Generate Project**
   ```bash
   # Standard tier (recommended)
   copier copy gh:liminalcommons/chora-base my-project

   # Specific version (pin to v1.1.0)
   copier copy --vcs-ref v1.1.0 gh:liminalcommons/chora-base my-project

   # Quick mode (non-interactive, use defaults)
   copier copy --defaults gh:liminalcommons/chora-base my-project
   ```

3. **Answer Questionnaire**
   ```
   🎯 Project name (lowercase, hyphens): my-awesome-project
   👤 Your name: John Doe
   📧 Your email: john@example.com
   🐍 Python version: 3.11
   📦 SAP bundle: standard (4-6 SAPs)
   ```

4. **Verify Generation**
   ```bash
   cd my-project
   ls -la
   # Should see: README.md, justfile, pyproject.toml, docs/, scripts/, .copier-answers.yml

   cat .copier-answers.yml
   # Should see: _src_path, _commit, project_name, author_name, etc.
   ```

5. **Test Generated Project**
   ```bash
   # Install dependencies (if post-generation hook didn't run)
   poetry install

   # List available recipes
   just --list

   # Run quick validation
   python scripts/validate-ecosystem-integration.py --quick
   ```

**Time**: 3-5 minutes (including questionnaire)

**Error Recovery**:
- If generation fails: Check Copier version (`copier --version`, need 8.0+)
- If dependencies missing: Run `poetry install` or `pip install -r requirements.txt`
- If git not initialized: Run `git init && git add . && git commit -m "Initial commit"`

---

### Workflow 2: Updating Existing Project (PATCH/MINOR)

**Scenario**: Template v1.0.0 → v1.1.0 (new SAP added, backward compatible)

**Steps**:

1. **Check Current Version**
   ```bash
   cat .copier-answers.yml | grep _commit
   # Output: _commit: v1.0.0
   ```

2. **Review Changelog**
   ```bash
   # Visit: https://github.com/liminalcommons/chora-base/blob/main/CHANGELOG.md
   # Check: What changed between v1.0.0 and v1.1.0?
   # Example: "v1.1.0: Added SAP-053 (Conflict Resolution)"
   ```

3. **Create Update Branch** (recommended)
   ```bash
   git checkout -b update-template-v1.1.0
   ```

4. **Run Copier Update**
   ```bash
   copier update

   # Copier output:
   # "Updating from v1.0.0 to v1.1.0..."
   # "🎉 Update complete! Review changes with `git diff`"
   ```

5. **Review Changes**
   ```bash
   git status
   # Output: Modified files, new files (if new SAP added)

   git diff
   # Output: Diff showing template updates
   ```

6. **Resolve Conflicts** (if any)
   ```bash
   # Check for merge conflicts
   git status | grep "both modified"

   # If conflicts exist, see "Workflow 5: Conflict Resolution"
   ```

7. **Test Changes**
   ```bash
   # Run tests
   pytest

   # Validate SAP ecosystem integration
   python scripts/validate-ecosystem-integration.py

   # Test automation recipes
   just --list
   ```

8. **Commit Update**
   ```bash
   git add .
   git commit -m "chore: Update template from v1.0.0 to v1.1.0

   Added SAP-053 (Conflict Resolution) from template update.

   Template diff: https://github.com/liminalcommons/chora-base/compare/v1.0.0...v1.1.0"
   ```

9. **Merge to Main**
   ```bash
   git checkout main
   git merge update-template-v1.1.0
   git push
   ```

**Time**: 10-15 minutes (PATCH), 15-20 minutes (MINOR)

**Skip Conditions**:
- If `.copier-answers.yml` shows `_commit: v1.1.0` → already up-to-date
- If project heavily customized → defer update, test in clean branch first

---

### Workflow 3: Updating with Breaking Changes (MAJOR)

**Scenario**: Template v1.3.0 → v2.0.0 (breaking change: `scripts/` → `automation/`)

**Steps**:

1. **Review Migration Guide** (REQUIRED)
   ```bash
   # Visit: https://github.com/liminalcommons/chora-base/blob/v2.0.0/MIGRATION-v2.0.md
   # Read: All breaking changes and migration steps
   ```

2. **Backup Current State**
   ```bash
   git checkout -b backup-before-v2.0
   git push origin backup-before-v2.0
   ```

3. **Create Update Branch**
   ```bash
   git checkout main
   git checkout -b update-template-v2.0.0
   ```

4. **Run Copier Update**
   ```bash
   copier update --vcs-ref v2.0.0

   # Copier output:
   # "⚠️  WARNING: This is a MAJOR version update (v1.3.0 → v2.0.0)"
   # "⚠️  Read migration guide: MIGRATION-v2.0.md"
   # "Updating..."
   ```

5. **Apply Migration Steps** (from MIGRATION-v2.0.md)
   ```bash
   # Example migration: scripts/ → automation/

   # 1. Move custom scripts
   mv scripts/my-custom-script.sh automation/my-custom-script.sh

   # 2. Update justfile recipes
   sed -i 's|python scripts/|python automation/|g' justfile

   # 3. Update documentation links
   find docs/ -name "*.md" -exec sed -i 's|(scripts/|(automation/|g' {} \;

   # 4. Remove old directory
   rm -rf scripts/
   ```

6. **Resolve Conflicts** (likely many)
   ```bash
   # Check for conflicts
   git status

   # Resolve each conflict following migration guide
   # See "Workflow 5: Conflict Resolution"
   ```

7. **Test Extensively**
   ```bash
   # Full test suite
   pytest

   # Validate all automation recipes
   just --list
   for recipe in $(just --list --unsorted | tail -n +2); do
     echo "Testing: $recipe"
     just $recipe --help || echo "❌ Failed: $recipe"
   done

   # Validate ecosystem integration
   python automation/validate-ecosystem-integration.py
   ```

8. **Commit Migration**
   ```bash
   git add .
   git commit -m "feat!: Migrate to template v2.0.0 (BREAKING CHANGE)

   BREAKING CHANGES:
   - Restructured directory: scripts/ → automation/
   - Updated all justfile recipes to use new paths
   - Updated documentation links

   Migration guide: https://github.com/liminalcommons/chora-base/blob/v2.0.0/MIGRATION-v2.0.md
   Template diff: https://github.com/liminalcommons/chora-base/compare/v1.3.0...v2.0.0"
   ```

9. **Merge to Main** (after thorough testing)
   ```bash
   git checkout main
   git merge update-template-v2.0.0
   git push
   ```

**Time**: 30-60 minutes (depends on migration complexity)

**Rollback Plan**:
```bash
# If migration fails or causes issues
git checkout backup-before-v2.0
git checkout -b rollback-v2.0
git push origin rollback-v2.0

# OR: Revert to previous template version
copier update --vcs-ref v1.3.0
```

---

### Workflow 4: Adding New SAP to Template (Template Maintainer)

**Scenario**: Adding SAP-063 to chora-base template (template maintainer)

**Steps**:

1. **Read SAP-063 Artifacts**
   ```bash
   # Understand what files SAP-063 includes
   ls -la docs/skilled-awareness/sap-063/
   # capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md
   ```

2. **Update `copier.yml` Questionnaire**
   ```yaml
   # Add SAP-063 checkbox
   sap_new_feature:
     type: bool
     help: |
       Include SAP-063 (New Feature)?

       Provides [brief description of SAP-063 capability].

       Files: docs/new-feature/, scripts/new-feature.py
       Effort: [X] min initial setup
     default: no  # opt-in for new SAPs
     when: "{{ sap_selection == 'custom' or sap_selection == 'comprehensive' }}"
   ```

3. **Add SAP Files to `template/`**
   ```bash
   # Create conditional directory inclusion
   mkdir -p template/docs/new-feature.jinja
   cp docs/skilled-awareness/sap-063/* template/docs/new-feature.jinja/

   # Add Jinja2 conditional
   # template/docs/new-feature.jinja/.copier-rename.yaml
   "_default": "{% if sap_new_feature %}docs/new-feature{% endif %}"
   ```

4. **Add Justfile Recipes** (conditional)
   ```jinja
   # template/justfile

   {% if sap_new_feature %}
   # SAP-063: New Feature recipes
   new-feature-status:
       python automation/new-feature-status.py

   new-feature-validate:
       python automation/new-feature-validator.py
   {% endif %}
   ```

5. **Update CHANGELOG.md**
   ```markdown
   ## v1.2.0 (2025-11-XX) - Add SAP-063

   ### Added
   - SAP-063 (New Feature) - [brief description]
   - New questionnaire option: `sap_new_feature`
   - Conditional files: `docs/new-feature/`, `automation/new-feature-status.py`
   - Justfile recipes: `new-feature-status`, `new-feature-validate`

   ### Changed
   - Comprehensive tier now includes SAP-063 (8 → 9 SAPs)

   **Backward Compatibility**: Yes (additive change, MINOR version bump)
   ```

6. **Test Template Generation**
   ```bash
   # Test with SAP-063 enabled
   copier copy \
     --data "sap_selection=custom" \
     --data "sap_new_feature=yes" \
     . output/test-sap-063-enabled

   # Verify SAP-063 files present
   ls output/test-sap-063-enabled/docs/new-feature/

   # Test with SAP-063 disabled
   copier copy \
     --data "sap_selection=standard" \
     . output/test-sap-063-disabled

   # Verify SAP-063 files absent
   ls output/test-sap-063-disabled/docs/ | grep -q new-feature && echo "❌ FAIL" || echo "✅ PASS"
   ```

7. **Test Update Propagation**
   ```bash
   # Generate project from v1.1.0 (without SAP-063)
   copier copy --vcs-ref v1.1.0 . output/test-update

   # Update to v1.2.0 (with SAP-063)
   cd output/test-update
   copier update --vcs-ref v1.2.0

   # Answer questionnaire (should prompt for sap_new_feature)
   # 🎯 Include SAP-063 (New Feature)? (y/N): y

   # Verify SAP-063 files added
   ls docs/new-feature/
   ```

8. **Tag Release**
   ```bash
   git add .
   git commit -m "feat: Add SAP-063 (New Feature) to template

   Added SAP-063 with conditional inclusion via questionnaire.

   - New files: docs/new-feature/, automation/new-feature-status.py
   - New recipes: new-feature-status, new-feature-validate
   - Updated CHANGELOG.md with v1.2.0 release notes

   BREAKING CHANGES: None (backward compatible)

   Closes: #123"

   git tag -a v1.2.0 -m "feat: Add SAP-063 (New Feature)"
   git push origin v1.2.0
   ```

9. **Announce Release**
   ```bash
   # Create GitHub release with changelog excerpt
   gh release create v1.2.0 \
     --title "v1.2.0 - Add SAP-063 (New Feature)" \
     --notes "$(sed -n '/## v1.2.0/,/## v1.1.0/p' CHANGELOG.md)"
   ```

**Time**: 2-3 hours (includes testing and documentation)

**Validation Checklist**:
- ✅ Template generates with SAP-063 enabled
- ✅ Template generates without SAP-063 (standard tier)
- ✅ Update from v1.1.0 → v1.2.0 prompts for SAP-063
- ✅ CHANGELOG.md updated
- ✅ Version tagged (v1.2.0)
- ✅ GitHub release created

---

### Workflow 5: Conflict Resolution (Common Scenarios)

**Scenario 1: justfile Recipe Conflict**

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
sap-check:
    python scripts/sap-evaluator.py --quick --custom-flag
=======
sap-validate:
    python scripts/sap-evaluator.py --quick
>>>>>>> template-v1.2.0
```

**Resolution**:
```bash
# 1. Accept template's new recipe name
# 2. Preserve local customization (--custom-flag)
# 3. Add backward-compatible alias

# Resolved:
sap-validate:
    python scripts/sap-evaluator.py --quick --custom-flag

sap-check: sap-validate  # Deprecated alias (remove in v2.0.0)
```

---

**Scenario 2: README.md Content Conflict**

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
## Features

- Custom feature A
- Custom feature B
=======
## Features

- Template feature X (added in v1.2.0)
>>>>>>> template-v1.2.0
```

**Resolution**:
```markdown
# Merge both changes (order: custom first, template second)

## Features

- Custom feature A
- Custom feature B
- Template feature X (added in v1.2.0)
```

---

**Scenario 3: pyproject.toml Dependency Conflict**

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
[tool.poetry.dependencies]
python = "^3.10"
pytest = "^7.3.0"
custom-lib = "^2.1.0"  # Local addition
=======
[tool.poetry.dependencies]
python = "^3.11"
pytest = "^8.0.0"
>>>>>>> template-v1.3.0
```

**Resolution**:
```toml
# Accept template's newer versions + keep local additions
[tool.poetry.dependencies]
python = "^3.11"  # Template update (BREAKING: dropped 3.10)
pytest = "^8.0.0"  # Template update
custom-lib = "^2.1.0"  # Local addition (preserved)
```

**Post-Resolution Steps**:
```bash
# Update lock file
poetry update

# Run tests
pytest

# If tests fail, investigate and fix
# If pytest 8.0 breaks tests, temporarily pin to 7.x:
# pytest = "^7.4.0"  # Temporary: v8.0 breaks tests (TODO: fix)
```

---

**Scenario 4: File Deletion Conflict**

**Conflict**:
```
Template deleted: scripts/deprecated-tool.py
Your local version has modifications
```

**Resolution**:
```bash
# Option 1: Accept deletion (template is correct)
git rm scripts/deprecated-tool.py
git commit -m "chore: Remove deprecated tool (per template v1.2.0)"

# Option 2: Keep local version (you need it)
git add scripts/deprecated-tool.py
git commit -m "chore: Keep deprecated-tool.py (local requirement)"
# Note: This file will cause conflicts on future updates

# Option 3: Rename to indicate local override
mv scripts/deprecated-tool.py scripts/local-deprecated-tool.py
git add scripts/local-deprecated-tool.py
git commit -m "chore: Rename to local-deprecated-tool.py (not in template)"
```

---

### Workflow 6: Versioning SAP Release (Template Maintainer)

**Scenario**: Releasing SAP-063 v1.1.0 (minor update, backward compatible)

**Steps**:

1. **Determine Version Bump**
   ```bash
   # Current: SAP-063 v1.0.0
   # Changes: Added new protocol section (backward compatible)
   # Bump: MINOR (v1.0.0 → v1.1.0)

   # Decision matrix:
   # - Bug fix only? → PATCH (1.0.0 → 1.0.1)
   # - New feature, backward compatible? → MINOR (1.0.0 → 1.1.0)
   # - Breaking change? → MAJOR (1.0.0 → 2.0.0)
   ```

2. **Update SAP Artifacts**
   ```bash
   # Update version in all 5 artifacts
   sed -i 's/Version: 1.0.0/Version: 1.1.0/' \
     docs/skilled-awareness/sap-063/capability-charter.md \
     docs/skilled-awareness/sap-063/protocol-spec.md \
     docs/skilled-awareness/sap-063/awareness-guide.md \
     docs/skilled-awareness/sap-063/adoption-blueprint.md \
     docs/skilled-awareness/sap-063/ledger.md
   ```

3. **Update Ledger Version History**
   ```markdown
   # docs/skilled-awareness/sap-063/ledger.md

   ## Version History

   ### v1.1.0 (2025-11-XX) - Enhanced Protocol

   **Changes**:
   - Added Section 4.3: Advanced conflict resolution patterns
   - Enhanced awareness-guide.md with 3 new workflows
   - Updated adoption-blueprint.md with L4-L5 levels

   **Backward Compatibility**: Yes (MINOR version bump)

   **Migration Required**: No

   **Adopters**: [List projects using SAP-063]
   ```

4. **Update INDEX.md**
   ```markdown
   # docs/skilled-awareness/INDEX.md

   #### SAP-063: New Feature

   - **Status**: active | **Version**: 1.1.0 | **Domain**: [Domain Name]
   - **Description**: [Updated description if needed]
   - **Dependencies**: SAP-001, SAP-015
   - **Location**: [sap-063/](sap-063/)
   - **Key Features**: [Updated features]
   ```

5. **Update sap-catalog.json**
   ```json
   {
     "id": "SAP-063",
     "title": "New Feature",
     "version": "1.1.0",
     "status": "active",
     "last_updated": "2025-11-XX",
     "capabilities": ["new-capability"],
     "dependencies": ["SAP-001", "SAP-015"]
   }
   ```

6. **Test SAP with New Version**
   ```bash
   # Validate SAP structure
   python scripts/validate-ecosystem-integration.py SAP-063

   # Expected output:
   # ✅ SAP-063: All integration points valid
   # ✅ Version: 1.1.0
   # ✅ Status: active
   ```

7. **Commit Version Bump**
   ```bash
   git add docs/skilled-awareness/sap-063/
   git add docs/skilled-awareness/INDEX.md
   git add sap-catalog.json

   git commit -m "feat(SAP-063): Bump version to v1.1.0

   Added Section 4.3 to protocol-spec.md (advanced conflict resolution).
   Enhanced awareness-guide.md with 3 new workflows.
   Updated adoption-blueprint.md with L4-L5 adoption levels.

   BREAKING CHANGES: None (backward compatible)

   Closes: #456"
   ```

8. **Tag SAP Release** (optional, for major SAPs)
   ```bash
   git tag -a sap-063-v1.1.0 -m "SAP-063 v1.1.0 - Enhanced Protocol"
   git push origin sap-063-v1.1.0
   ```

**Time**: 15-20 minutes

**Skip Conditions**:
- If only fixing typos → Don't bump version (documentation fix, not functional change)
- If SAP is still draft status → Don't version until pilot status

---

## Developer Patterns

### Pattern 1: Pin Template Version for Reproducibility

**Use Case**: Ensure exact template version for audit trail, compliance, or reproducible builds

**Implementation**:
```bash
# Generate project with pinned version
copier copy --vcs-ref v1.1.0 gh:liminalcommons/chora-base my-project

# .copier-answers.yml will contain:
# _commit: v1.1.0

# Future updates require explicit version specification
copier update --vcs-ref v1.2.0  # Won't auto-update to latest
```

**Benefits**:
- **Reproducibility**: Generate exact same project 6 months later
- **Audit trail**: Know exactly which template version was used
- **Controlled updates**: No surprise changes from `copier update`

**Drawbacks**:
- **Manual updates**: Must explicitly specify new version
- **Miss bug fixes**: Won't get PATCH updates automatically

---

### Pattern 2: Test Template Updates in Branch First

**Use Case**: Avoid breaking main branch with template update conflicts

**Implementation**:
```bash
# Always update in branch, never directly on main
git checkout -b update-template-v1.2.0

copier update --vcs-ref v1.2.0

# Review, test, resolve conflicts
git diff
pytest
just --list

# Only merge after validation
git checkout main
git merge update-template-v1.2.0
```

**Benefits**:
- **Safe experimentation**: Can discard branch if update causes issues
- **Review changes**: See full diff before merging
- **Rollback easy**: Just delete branch if update fails

---

### Pattern 3: Gradual Template Update Strategy

**Use Case**: Large codebase with heavy customizations, risky to update all at once

**Implementation**:
```bash
# Don't update entire template in one commit
# Instead: Update incrementally (file by file or SAP by SAP)

# Step 1: Update only SAP-001 files
copier update --vcs-ref v1.2.0 --skip "*" --force "docs/coordination/**"

# Step 2: Test SAP-001 changes
pytest tests/test_coordination.py

# Step 3: Commit SAP-001 update
git commit -m "chore: Update SAP-001 files from template v1.2.0"

# Step 4: Repeat for other SAPs
copier update --vcs-ref v1.2.0 --skip "*" --force "automation/**"
# ... test, commit, repeat
```

**Benefits**:
- **Reduced risk**: Small, isolated changes easier to test and rollback
- **Easier debugging**: If something breaks, know which SAP caused it
- **Incremental validation**: Test each SAP update independently

**Drawbacks**:
- **Time-consuming**: 10+ commits for full template update
- **Conflicts between SAPs**: May need to resolve same file multiple times

---

### Pattern 4: Override Template Files Without Conflicts

**Use Case**: Need to customize template file but avoid future update conflicts

**Implementation**:
```bash
# Option 1: Create local override file (preferred)
# Instead of editing: justfile
# Create: justfile.local

# justfile (template-managed):
!include justfile.local  # Include local overrides

# justfile.local (your customizations):
custom-recipe:
    python my-custom-script.py

# Option 2: Use .copier-skip (ignore file on updates)
# .copier-skip:
# README.md  # Don't update README (heavily customized)

# Option 3: Use git attributes (manual merge only)
# .gitattributes:
# justfile merge=manual  # Force manual merge, never auto-merge
```

**Benefits**:
- **No conflicts**: Local overrides never conflict with template updates
- **Clean separation**: Template files vs local customizations clearly separated
- **Easy updates**: `copier update` skips local override files

---

### Pattern 5: Validate Template Before Committing

**Use Case**: Ensure template update didn't break project (catch issues before commit)

**Implementation**:
```bash
# After copier update, run full validation suite
copier update

# Step 1: Validate SAP ecosystem integration
python automation/validate-ecosystem-integration.py

# Step 2: Test all justfile recipes
just --list
for recipe in $(just --list --unsorted | tail -n +2); do
  just $recipe --help || echo "❌ Failed: $recipe"
done

# Step 3: Run test suite
pytest

# Step 4: Validate links
python automation/validate-links.sh docs/

# Only commit if all checks pass
if [ $? -eq 0 ]; then
  git add .
  git commit -m "chore: Update template to v1.2.0 (validated)"
else
  echo "❌ Validation failed. Fix issues before committing."
fi
```

**Benefits**:
- **Catch breaks early**: Find issues before they reach main branch
- **Automated validation**: Consistent check across all updates
- **Confidence**: Know template update is safe before committing

---

## Multi-Tab Coordination Patterns

### Pattern 1: Parallel Template Development (Template Maintainer)

**Use Case**: Two developers adding different SAPs to template simultaneously

**Coordination**:
```bash
# Developer A (tab-1): Adding SAP-063
git checkout -b feat/add-sap-063
# ... add SAP-063 to template/
git push origin feat/add-sap-063

# Developer B (tab-2): Adding SAP-064
git checkout -b feat/add-sap-064
# ... add SAP-064 to template/
git push origin feat/add-sap-064

# Merge order:
# 1. Developer A merges SAP-063 first
# 2. Developer B rebases SAP-064 on latest main (after SAP-063 merged)
# 3. Developer B resolves conflicts (copier.yml questionnaire, CHANGELOG.md)
# 4. Developer B merges SAP-064
```

**Conflict Files** (expected):
- `copier.yml` (questionnaire order)
- `CHANGELOG.md` (version history)
- `template/justfile` (recipe order)

**Resolution Time**: 5-10 minutes per SAP

---

### Pattern 2: Coordinated Template Update (Multi-Repo)

**Use Case**: Update chora-base template in multiple downstream projects (chora-workspace, castalia, etc.)

**Coordination**:
```bash
# Coordinator (tab-1): Update chora-workspace first
cd chora-workspace
copier update --vcs-ref v1.2.0
# ... resolve conflicts, test, commit

# Developer A (tab-2): Update castalia (waits for chora-workspace completion)
cd castalia
copier update --vcs-ref v1.2.0
# ... reference chora-workspace commit for conflict resolution patterns

# Developer B (tab-3): Update external-project
cd external-project
copier update --vcs-ref v1.2.0
# ... reference chora-workspace + castalia for patterns
```

**Benefit**: Learn from first project's conflict resolution, apply to others

---

## Error Recovery Patterns

### Error 1: Copier Update Fails with Conflicts

**Error**:
```
$ copier update
...
ERROR: Conflicts detected. Resolve manually and run `copier update --skip-answered`.
```

**Recovery**:
```bash
# Step 1: Check which files have conflicts
git status | grep "both modified"

# Step 2: Resolve conflicts manually (see Workflow 5)

# Step 3: Continue update
copier update --skip-answered  # Skip already-answered questions

# Step 4: Validate and commit
pytest
git add .
git commit -m "chore: Update template to v1.2.0 (resolved conflicts)"
```

---

### Error 2: Template Generation Fails (Missing Dependencies)

**Error**:
```
$ copier copy gh:liminalcommons/chora-base my-project
ERROR: Could not find Copier version 8.0+. Install with: pipx install copier
```

**Recovery**:
```bash
# Install Copier
pipx install copier

# Or: Use pip
pip install copier

# Or: Use brew (macOS)
brew install copier

# Retry generation
copier copy gh:liminalcommons/chora-base my-project
```

---

### Error 3: Post-Generation Hook Fails (Git Not Initialized)

**Error**:
```
$ copier copy gh:liminalcommons/chora-base my-project
...
ERROR: git init failed (not found in PATH)
```

**Recovery**:
```bash
# Install git (if missing)
brew install git  # macOS
apt-get install git  # Ubuntu/Debian

# Or: Skip git hook and initialize manually
cd my-project
git init
git add .
git commit -m "chore: Initial commit from template v1.1.0"
```

---

## Troubleshooting Guide

**Q: `copier update` shows "No changes detected" but I know template updated**

**A**: Check if your `.copier-answers.yml` has `_commit` pinned to old version:
```bash
cat .copier-answers.yml | grep _commit
# If _commit: v1.0.0, but latest is v1.2.0:
copier update --vcs-ref v1.2.0  # Force update to specific version
```

---

**Q: Template update breaks my custom scripts**

**A**: Use local override pattern to separate customizations:
```bash
# Create justfile.local (not managed by template)
# justfile (template):
!include justfile.local

# justfile.local (your customizations):
custom-recipe:
    python my-custom-script.py
```

---

**Q: How do I rollback a template update?**

**A**: Revert to previous template version:
```bash
# Option 1: Git revert
git log --oneline | grep "template"  # Find commit hash
git revert <commit-hash>

# Option 2: Copier downgrade
copier update --vcs-ref v1.0.0  # Downgrade to v1.0.0
```

---

**Q: Can I use template without Copier (manual copy)?**

**A**: Yes, but lose update propagation:
```bash
# Manual approach (not recommended):
git clone https://github.com/liminalcommons/chora-base
cp -r chora-base/template/* my-project/

# Drawback: No `copier update` support
# Must manually copy files on each template update
```

---

## Version History

### v1.0.0 (2025-11-20) - Initial Release

**Changes**:
- Initial awareness guide for SAP-062
- 6 agent workflows (create project, update PATCH/MINOR, update MAJOR, add SAP, conflict resolution, version SAP)
- 5 developer patterns (pin version, test in branch, gradual updates, override files, validate before commit)
- 2 multi-tab coordination patterns (parallel development, coordinated updates)
- 3 error recovery patterns + troubleshooting guide

**Context**:
- Created as part of CORD-2025-023 (3-SAP Suite Delivery)
- Phase 3 deliverable (parallel with Phase 4 SAP-050 promotion)
- Trace ID: sap-development-lifecycle-meta-saps-2025-11-20

**Author**: Claude (Anthropic) via tab-2 (chora-workspace)

---

**Created**: 2025-11-20
**Last Updated**: 2025-11-20
**Status**: draft
**Next Review**: After adoption-blueprint.md completion
