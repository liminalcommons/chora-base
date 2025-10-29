# PYPI_TOKEN Configuration Guide

**Purpose:** Enable automated PyPI releases via GitHub Actions

**Status:** ⏳ PENDING (requires repository admin access)

---

## What is PYPI_TOKEN?

The `PYPI_TOKEN` is a GitHub repository secret that allows the [release.yml](.github/workflows/release.yml) workflow to automatically publish new versions of chora-compose to PyPI when a new release is created.

## Why Configure It?

**Current State (Manual):**
```bash
# Must manually run on each release:
poetry build
poetry publish
```

**With PYPI_TOKEN (Automated):**
```bash
# Just create a GitHub release, workflow handles the rest:
gh release create v1.4.0
# → Automatically builds and publishes to PyPI
```

---

## Configuration Steps

### Step 1: Create PyPI API Token

1. **Log in to PyPI:** https://pypi.org
2. **Go to Account Settings** → **API tokens**
3. **Click "Add API token"**
4. **Configure token:**
   - Token name: `chora-compose-github-actions`
   - Scope: **Project: chora-compose** (recommended)
     - Alternative: "Entire account" (less secure)
5. **Copy the token** (starts with `pypi-...`)
   - ⚠️ **Save immediately!** Token only shown once

### Step 2: Add Secret to GitHub

1. **Go to GitHub repository:** https://github.com/liminalcommons/chora-compose
2. **Navigate to:** Settings → Secrets and variables → Actions
3. **Click "New repository secret"**
4. **Configure secret:**
   - Name: `PYPI_TOKEN`
   - Value: Paste the PyPI token from Step 1
5. **Click "Add secret"**

### Step 3: Verify Configuration

1. **Check release.yml references correct secret:**
   ```yaml
   # .github/workflows/release.yml
   - name: Publish to PyPI
     env:
       POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
     run: poetry publish
   ```

2. **Test with a pre-release (optional):**
   ```bash
   # Create a test release to verify automation
   gh release create v1.3.1-test --prerelease
   # Check Actions tab to see if workflow runs
   ```

---

## Security Best Practices

✅ **Do:**
- Use project-scoped tokens (limits damage if compromised)
- Rotate tokens periodically (every 6-12 months)
- Use GitHub's environment protection rules for production releases
- Review workflow runs regularly

❌ **Don't:**
- Commit tokens to git (secrets only!)
- Share tokens in Slack/email
- Use account-wide tokens unless necessary
- Grant token access to untrusted contributors

---

## Troubleshooting

### "Authentication failed" error

**Cause:** Token invalid or expired

**Fix:**
1. Generate new PyPI token
2. Update GitHub secret with new token
3. Re-run failed workflow

### "Package already exists" error

**Cause:** Version already published to PyPI

**Fix:**
1. Check PyPI: https://pypi.org/project/chora-compose/
2. Bump version: `./scripts/bump-version.sh patch`
3. Create new release with bumped version

### Workflow doesn't trigger

**Cause:** Release not tagged properly

**Fix:**
1. Ensure release tag matches pattern: `v*.*.*`
2. Check workflow triggers in `.github/workflows/release.yml`
3. Manually trigger workflow if needed (Actions → release.yml → Run workflow)

---

## Alternative: Manual Release Process

If PYPI_TOKEN is not configured, releases can still be done manually:

```bash
# 1. Bump version
./scripts/bump-version.sh minor  # or major, patch

# 2. Update CHANGELOG.md
# (edit [Unreleased] section and create new version section)

# 3. Commit version bump
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): Bump version to v1.4.0"

# 4. Tag release
git tag v1.4.0
git push origin main --tags

# 5. Build distribution
./scripts/build-dist.sh

# 6. Publish to PyPI
poetry publish
# (will prompt for PyPI username/password or token)

# 7. Create GitHub release
gh release create v1.4.0 --notes "See CHANGELOG.md for details"
```

---

## Parity Impact

**Checklist Item:** 4.4 - release.yml has PYPI_TOKEN secret configured

**Current Status:** ❌ Not configured (manual releases only)

**Options:**
1. **Configure now** → Achieves 76/80 (95% - A+ grade)
2. **Defer to first release** → Stays at 75/80 (93.75%)
   - Still production-ready, just manual release process

**Recommendation:** Configure before first automated release (v1.4.0+)

---

## References

- **PyPI API Tokens:** https://pypi.org/help/#apitoken
- **GitHub Secrets:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **release.yml workflow:** [.github/workflows/release.yml](.github/workflows/release.yml)
- **Poetry publish:** https://python-poetry.org/docs/cli/#publish

---

**Last Updated:** 2025-10-18
**Owner:** Repository Admin
**Status:** Pending configuration
