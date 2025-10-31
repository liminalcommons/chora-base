# How to Upgrade Structure from Upstream

**Purpose**: Receive structural updates from chora-base upstream while preserving your project-specific content

**When to Use**: After chora-base releases new features, standards, or templates that you want to adopt

**Time**: 15-30 minutes

---

## Overview

The Clone & Merge Model allows you to safely merge structural updates from the upstream chora-base repository into your project without overwriting your custom code, documentation, or configurations.

**What Gets Merged**:
- ✅ SAP Framework updates (standards, protocols, templates)
- ✅ Automation scripts (install-sap.py, validation tools)
- ✅ Configuration templates (.github/, docker configs)
- ✅ Documentation structure and standards

**What Stays Yours**:
- ✅ Source code (src/, tests/)
- ✅ Project-specific SAPs and documentation
- ✅ Custom configurations and secrets
- ✅ Git history and project identity

**Hybrid Files** (require manual merge):
- ⚙️ AGENTS.md (project overview + structural sections)
- ⚙️ README.md (project identity + template structure)
- ⚙️ INDEX.md (project SAPs + framework SAPs)

---

## Prerequisites

### 1. Check Your Project Type

This guide applies to:
- Projects created from chora-base using Copier
- Repositories that have a `.chorabase` metadata file

Verify your project:
```bash
# Check if .chorabase exists
ls -la .chorabase

# Check project type
grep "project_type" .chorabase
```

Expected output: `project_type: "chora-base-project"` or `"chora-base-root"`

### 2. Install Dependencies

```bash
# Python 3.11+ required
python --version

# Install PyYAML for .chorabase parsing
pip install PyYAML
```

### 3. Clean Working Directory

Commit or stash all local changes:
```bash
git status

# If you have uncommitted changes:
git stash  # or git commit -am "WIP: work in progress"
```

---

## Step 1: Review What Would Be Merged (Dry Run)

**Always run a dry-run first** to preview changes:

```bash
python scripts/merge-upstream-structure.py --dry-run
```

**Example Output**:
```
=======================================
Merge Upstream Structure
=======================================

✓ Loaded .chorabase metadata
✓ Upstream remote found: https://github.com/liminalcommons/chora-base.git
ℹ [DRY RUN] Would fetch from chora-base/main
ℹ [DRY RUN] Would create backup: .chora-backup-20251029-171128

=======================================
Merging Structure-Only Files
=======================================

✓ Found 31 structure-only file patterns

ℹ [DRY RUN] Would merge: scripts/install-sap.py
ℹ [DRY RUN] Would merge: scripts/check-sap-awareness-integration.sh
ℹ [DRY RUN] Would merge: docs/skilled-awareness/sap-framework/protocol-spec.md
...

=======================================
Detecting Hybrid Files
=======================================

⚠ The following files require manual merge:

  ℹ AGENTS.md (strategy: section-by-section)
  ℹ README.md (strategy: template-variables)
  ℹ docs/skilled-awareness/INDEX.md (strategy: table-rows)

=======================================
Merge Summary
=======================================

Structure files merged: 42
Hybrid files requiring manual merge: 3
Errors: 0
```

**Review the output**:
- Which files will be updated?
- Are there any errors or warnings?
- Do the hybrid files need manual attention?

---

## Step 2: Run the Merge

If the dry-run looks good, run the actual merge:

```bash
python scripts/merge-upstream-structure.py
```

**What Happens**:
1. ✅ Creates automatic backup (`.chora-backup-{timestamp}/`)
2. ✅ Fetches latest from upstream
3. ✅ Merges all structure-only files
4. ✅ Reports hybrid files for manual merge
5. ✅ Runs validation (if configured in `.chorabase`)

**Example Output**:
```
✓ Backup created: .chora-backup-20251029-171128
  - Current commit: abc123f
  - Current branch: main

✓ Fetched latest from chora-base/main
✓ Merged: scripts/install-sap.py
✓ Merged: scripts/check-sap-awareness-integration.sh
...

⚠ Hybrid files require manual merge (see below)

✓ Merge workflow completed successfully
```

---

## Step 3: Review Merged Changes

Inspect what was changed:

```bash
# See all changed files
git status

# Review specific file changes
git diff scripts/install-sap.py
git diff docs/skilled-awareness/sap-framework/protocol-spec.md

# See all changes
git diff
```

**Look for**:
- ✅ Updated scripts and automation tools
- ✅ New SAP framework files or updates
- ✅ Configuration template improvements
- ⚠️ Any unexpected changes to content files (shouldn't happen)

---

## Step 4: Merge Hybrid Files

Hybrid files need intelligent merging to preserve your project content while updating structure.

### 4a. Merge AGENTS.md (Section-by-Section)

**Strategy**: Keep project-specific sections, update structural sections

```bash
python scripts/merge-agents-md.py --dry-run
```

**Review the output**, then apply:
```bash
python scripts/merge-agents-md.py
```

**What It Does**:
- ✅ Preserves: "Project Overview", "Common Tasks", "Custom Capabilities"
- ✅ Updates: "Project Structure", "Development Process", "SAP Framework"
- ✅ Maintains: Your project description and custom workflows

### 4b. Merge README.md (Template Variables)

**Strategy**: Preserve project identity, update template structure

```bash
python scripts/merge-readme-md.py --dry-run
```

**Review the output**, then apply:
```bash
python scripts/merge-readme-md.py
```

**What It Does**:
- ✅ Preserves: Project name, description, features, badges
- ✅ Updates: Section structure, installation instructions, standard badges
- ✅ Maintains: Your repository URL and custom sections

### 4c. Merge INDEX.md (Table Rows)

**Strategy**: Update framework SAPs (SAP-000), keep project SAPs (SAP-001+)

```bash
python scripts/merge-index-md.py --dry-run
```

**Review the output**, then apply:
```bash
python scripts/merge-index-md.py
```

**What It Does**:
- ✅ Updates: SAP-000 (framework) from upstream
- ✅ Preserves: SAP-001 through SAP-018 (your installed SAPs)
- ✅ Maintains: Table formatting and metadata columns

---

## Step 5: Validate and Test

Run project validation to ensure everything still works:

```bash
# Linting
ruff check .

# Type checking
mypy src

# Tests
pytest tests/ -x

# Or use justfile
just test
just lint
```

**If validation fails**:
- Review the errors
- Check if upstream changes broke compatibility
- Fix issues or rollback (see Step 7)

---

## Step 6: Commit the Merge

Once everything validates, commit the changes:

```bash
# Add all merged files
git add .

# Commit with descriptive message
git commit -m "chore: Merge structural updates from chora-base v4.1.0

- Updated SAP framework protocols
- Merged automation scripts (install-sap.py, merge tools)
- Updated configuration templates
- Merged AGENTS.md, README.md, INDEX.md hybrid files

Structural version: 4.1.0"

# Push to your repository
git push
```

---

## Step 7: Rollback (If Needed)

If something goes wrong, you can easily rollback:

```bash
# Find your backup directory
ls -la | grep chora-backup

# Get commit hash from backup
cat .chora-backup-20251029-171128/commit.txt

# Reset to that commit
git reset --hard $(cat .chora-backup-20251029-171128/commit.txt)

# Verify rollback
git log -1
```

**Note**: This removes all merged changes. You can try the merge again after investigating the issue.

---

## Troubleshooting

### Problem: "Upstream remote not found"

**Solution**: The script will automatically add the upstream remote:
```bash
git remote add chora-base https://github.com/liminalcommons/chora-base.git
git fetch chora-base main
```

### Problem: "Merge conflicts in hybrid files"

**Solution**: The hybrid merge scripts handle this automatically. If manual intervention is needed:

1. Review the file
2. Manually edit to combine sections
3. Commit the resolved version

### Problem: "Validation fails after merge"

**Possible Causes**:
- Upstream introduced breaking changes
- Your customizations conflict with new structure
- Dependencies need updating

**Solution**:
1. Read upstream CHANGELOG/release notes
2. Check for migration guides
3. Update your code to match new patterns
4. Or rollback and wait for compatibility fix

### Problem: "Some files weren't merged"

**Check**:
- Is the file in `structure_only` in `.chorabase`?
- Does the file exist in upstream?
- Are there glob pattern issues?

**Debug**:
```bash
# Check if file exists in upstream
git ls-tree -r --name-only chora-base/main | grep "your-file.py"

# Check .chorabase configuration
grep "your-file" .chorabase
```

---

## Advanced Usage

### Merge Specific File Patterns Only

Edit `.chorabase` temporarily to merge only specific patterns:

```yaml
# Comment out patterns you don't want to merge
structure_only:
  - scripts/install-sap.py  # Only merge this
  # - scripts/**  # Skip everything else
```

Then run the merge.

### Merge Without Backup

**Not recommended**, but possible:
```bash
python scripts/merge-upstream-structure.py --no-backup
```

### Customize Merge Strategies

Edit `.chorabase` to change how hybrid files are merged:

```yaml
hybrid:
  AGENTS.md:
    preserve_sections:
      - "Project Overview"
      - "My Custom Section"  # Add your section
    merge_sections:
      - "Project Structure"  # Add more sections to merge
```

---

## What's Next?

After successfully merging upstream structure:

1. **Review Release Notes**: Check what features were added
2. **Install New SAPs**: Use `python scripts/install-sap.py <sap-id>` for new capabilities
3. **Update Documentation**: Reflect any new standards in your project docs
4. **Share Experience**: Report issues or improvements to chora-base maintainers

---

## Related Documentation

- [chorabase Metadata Specification](../reference/chorabase-metadata-spec.md) - `.chorabase` file format
- [Structure vs Content Model](../explanation/structure-vs-content-model.md) - Understanding the boundaries
- [SAP Installation Guide](install-sap.md) - Installing new Skilled Awareness Packages
- [Project Bootstrap](project-bootstrap.md) - Creating new projects from chora-base

---

**Last Updated**: 2025-10-29
**Applies to**: chora-base v4.1.0+
**Maintenance**: Update when merge process changes
