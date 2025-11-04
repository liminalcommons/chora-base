---
title: How to Create a Release
type: how-to
status: current
audience: maintainer
last_updated: 2025-11-03
trace_id: sap-synergy-2025-001
---

# How to Create a Release

**Quick Start**: Use `just bump <version>` and `just release`, or run the Python scripts directly.

---

## Overview

This guide explains how to create a new release for chora-base using the unified release workflow (GAP-003). The workflow automates version bumping, CHANGELOG updates, git tagging, and GitHub release creation.

**Tools Used**:
- `scripts/bump-version.py` - Version bumping and git tagging
- `scripts/create-release.py` - GitHub release creation
- `just` task runner (optional convenience layer)

---

## Prerequisites

Before you begin, ensure you have:
- [ ] Python 3.11+ installed
- [ ] git installed and configured
- [ ] Write access to the chora-base repository
- [ ] GitHub CLI (`gh`) installed and authenticated (for release creation)
- [ ] `just` task runner installed (optional, for convenience)

### Install GitHub CLI

```bash
# Mac
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh
```

### Authenticate GitHub CLI

```bash
gh auth login
```

---

## Step-by-Step Release Process

### Step 1: Decide on Version Number

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

**Example**: If current version is 4.3.0:
- Breaking change → 5.0.0
- New feature → 4.4.0
- Bug fix → 4.3.1

### Step 2: Preview Version Bump (Dry Run)

```bash
# Using just (recommended)
just bump-dry 4.4.0

# Or directly with Python
python scripts/bump-version.py 4.4.0 --dry-run
```

**What this does**:
- Shows what would be inserted into CHANGELOG.md
- Shows git commands that would be run
- Does NOT modify any files

**Expected output**:
```
Bumping chora-base version to 4.4.0...
[DRY RUN MODE] No files will be modified

[DRY RUN] Would insert the following into CHANGELOG.md at line X:
---
## [4.4.0] - 2025-11-03

### Added
- TODO: List new features
...
```

### Step 3: Bump Version

```bash
# Using just (recommended)
just bump 4.4.0

# Or directly with Python
python scripts/bump-version.py 4.4.0
```

**What this does**:
1. Updates CHANGELOG.md with new version header (includes TODOs)
2. Creates git commit: `chore(release): Bump version to v4.4.0`
3. Creates annotated git tag: `v4.4.0`

**Expected output**:
```
Bumping chora-base version to 4.4.0...
[OK] Updated CHANGELOG.md with version 4.4.0
[OK] Created git commit: chore(release): Bump version to v4.4.0
[OK] Created git tag: v4.4.0

======================================================================
Next Steps:
======================================================================
1. Edit CHANGELOG.md and replace TODOs with actual changes for v4.4.0
2. Amend the commit with your changes:
     git commit --amend
3. Push the commit and tag to remote:
     git push && git push --tags
4. Create GitHub release:
     just release
     # or: python scripts/create-release.py
======================================================================
```

### Step 4: Edit CHANGELOG

Open `CHANGELOG.md` and replace the TODO placeholders with actual changes:

**Before**:
```markdown
## [4.4.0] - 2025-11-03

### Added
- TODO: List new features

### Changed
- TODO: List changes

### Fixed
- TODO: List bug fixes
```

**After**:
```markdown
## [4.4.0] - 2025-11-03

### Added
- GAP-001: End-to-end CHORA_TRACE_ID propagation
- GAP-002: Auto-generate documentation from coordination
- New scripts: propagate-trace-id.sh, generate-doc-from-coordination.sh

### Changed
- Enhanced SAP-001, SAP-007, SAP-013 with trace_id support
- Migrated all bash scripts to Python for cross-platform support

### Fixed
- Unicode encoding issues in Windows console output
```

**Tips**:
- Be specific and concise
- Group related changes together
- Reference GAP IDs, SAP IDs, or issue numbers
- Follow [Keep a Changelog](https://keepachangelog.com/) format

### Step 5: Amend Commit with Updated CHANGELOG

```bash
git add CHANGELOG.md
git commit --amend
```

**Note**: The commit message stays the same, only the CHANGELOG content changes.

### Step 6: Push to Remote

```bash
# Push both commit and tag
git push && git push --tags
```

**Verification**:
- Check GitHub that commit and tag are visible
- Tag should appear in the "Tags" section

### Step 7: Preview GitHub Release (Dry Run)

```bash
# Using just (recommended)
just release-dry

# Or directly with Python
python scripts/create-release.py --dry-run
```

**What this does**:
- Extracts release notes from CHANGELOG.md for the version
- Shows what GitHub release would be created
- Does NOT create actual release

**Expected output**:
```
[DRY RUN MODE] No release will be created

Extracting release notes from CHANGELOG.md for version 4.4.0...
[OK] Found 523 characters of release notes
[DRY RUN] Would create GitHub release:
  Tag: v4.4.0
  Title: Release v4.4.0
  Notes:
------------------------------------------------------------
### Added
- GAP-001: End-to-end CHORA_TRACE_ID propagation
...
------------------------------------------------------------
```

### Step 8: Create GitHub Release

```bash
# Using just (recommended)
just release

# Or directly with Python
python scripts/create-release.py
```

**What this does**:
1. Detects version from current git tag (v4.4.0)
2. Extracts release notes from CHANGELOG.md
3. Creates GitHub release with notes
4. Publishes release (NOT a draft)

**Expected output**:
```
Detecting version from current git tag...
[OK] Detected version: 4.4.0
Extracting release notes from CHANGELOG.md for version 4.4.0...
[OK] Found 523 characters of release notes
[OK] Created GitHub release: v4.4.0

======================================================================
GitHub release created successfully!
======================================================================
View at: https://github.com/liminalcommons/chora-base/releases/tag/v4.4.0
======================================================================
```

---

## Verification Checklist

After completing the release, verify:

- [ ] Git tag `v4.4.0` exists locally: `git tag | grep 4.4.0`
- [ ] Git tag exists on remote: Check GitHub Tags page
- [ ] CHANGELOG.md has entry for v4.4.0 with real changes (not TODOs)
- [ ] GitHub release exists: https://github.com/liminalcommons/chora-base/releases
- [ ] Release notes match CHANGELOG content
- [ ] Release is marked as "Latest" (if applicable)

---

## Troubleshooting

### Problem: `gh: command not found`

**Solution**: Install GitHub CLI

```bash
# Mac
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh
```

### Problem: `gh` not authenticated

**Error**: `[FAIL] gh CLI not authenticated`

**Solution**:
```bash
gh auth login
```

Follow prompts to authenticate with GitHub.

### Problem: No git tag found

**Error**: `[FAIL] No git tag found for current commit`

**Solution**: Run `just bump <version>` first to create the tag.

### Problem: Unicode characters not displaying

**Symptoms**: Question marks or boxes instead of checkmarks/emojis

**This is normal on Windows**: The release will still be created correctly. Unicode characters are preserved in the GitHub release notes (they just don't display well in Windows console).

**Workaround**: Use `--dry-run` to preview, or check the GitHub release page after creation.

### Problem: Version already exists

**Error**: Git tag already exists

**Solution**:
1. If you need to recreate: `git tag -d v4.4.0` to delete local tag
2. If you pushed it: `git push origin :v4.4.0` to delete remote tag
3. Then run `just bump 4.4.0` again

**Warning**: Avoid deleting tags that are already released.

### Problem: CHANGELOG entry not found

**Warning**: `[WARN] No CHANGELOG entry found for version X.X.X`

**Cause**: You skipped editing CHANGELOG.md, or the version format doesn't match.

**Solution**:
1. Edit CHANGELOG.md
2. Ensure version header matches: `## [4.4.0] - 2025-11-03`
3. Run `git commit --amend` to update
4. Run `just release` again

---

## Advanced Usage

### Create Release for Specific Version

If you're not on the tagged commit:

```bash
# Using just
just release-version 4.3.0

# Or directly
python scripts/create-release.py --version 4.3.0
```

### Script Flags

Both scripts support `--help`:

```bash
python scripts/bump-version.py --help
python scripts/create-release.py --help
```

### Manual Release (Without Scripts)

If you prefer manual control:

```bash
# 1. Update CHANGELOG.md manually
# 2. Create commit
git add CHANGELOG.md
git commit -m "chore(release): Bump version to v4.4.0"

# 3. Create tag
git tag -a v4.4.0 -m "Release v4.4.0"

# 4. Push
git push && git push --tags

# 5. Create release using gh CLI directly
gh release create v4.4.0 --title "Release v4.4.0" --notes "See CHANGELOG.md"
```

---

## Related Documentation

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GAP-003 Implementation Plan](../../project-docs/gap-003-unified-release-implementation-plan.md)
- [Workflow Continuity Gap Report](../../project-docs/workflow-continuity-gap-report.md)
- justfile tasks: `just --list`

---

## Feedback

If you encounter issues or have suggestions for improving this workflow:
1. Open an issue in chora-base repository
2. Tag with `gap-003` and `release-workflow`
3. Include steps to reproduce and expected vs actual behavior

---

**Last Updated**: 2025-11-03
**Part of**: GAP-003 (Unified Release Workflow)
**Trace ID**: sap-synergy-2025-001
