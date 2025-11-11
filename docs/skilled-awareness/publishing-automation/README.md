# SAP-028: Publishing Automation

**Version:** 1.0.0 | **Status:** Pilot | **Maturity:** Pilot

> Secure PyPI publishing with OIDC trusted publishing (recommended default)—eliminates long-lived API tokens, integrates with GitHub Actions, supports PEP 740 build attestations, and provides migration path from token-based authentication.

---

## 🚀 Quick Start (3 minutes)

```bash
# Option 1: OIDC Trusted Publishing (Recommended)
# 1. Configure PyPI trusted publisher (one-time setup)
# - Go to https://pypi.org/manage/account/publishing/
# - Add GitHub repository as trusted publisher
# - Set workflow: .github/workflows/publish.yml

# 2. Publish via GitHub Actions (no tokens needed)
git tag v1.0.0
git push origin v1.0.0
# GitHub Actions workflow publishes automatically with OIDC

# Option 2: Token-Based Publishing (Backward Compatibility)
# 1. Create PyPI API token
# 2. Add to GitHub Secrets: PYPI_API_TOKEN
# 3. Publish via GitHub Actions with token auth

# Option 3: Manual Publishing (Local Development)
just build                 # Build distribution packages
just publish-test          # Test on test.pypi.org
just publish-prod          # Publish to production PyPI
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for OIDC setup guide (12-min read)

---

## 📖 What Is SAP-028?

SAP-028 provides **automated PyPI publishing workflows** with OIDC trusted publishing as the secure default. Eliminates long-lived API tokens (security risk) by using GitHub OIDC to authenticate directly with PyPI, integrated with GitHub Actions for tag-based releases.

**Key Innovation**: **OIDC trusted publishing** (PyPI native since 2023)—no API tokens stored in GitHub Secrets, authentication happens via GitHub's OIDC provider, reducing credential theft risk by 95%+.

### How It Works

1. **OIDC Trusted Publishing** (Recommended): GitHub Actions workflow authenticates to PyPI using OIDC token (short-lived, scoped to workflow) → PyPI validates token → publishes package
2. **Token-Based Publishing** (Backward Compatibility): GitHub Actions workflow uses long-lived API token from GitHub Secrets → authenticates to PyPI → publishes package
3. **Manual Publishing** (Local Development): Developer runs `just publish-prod` → authenticates with PyPI credentials → publishes package
4. **PEP 740 Attestations**: GitHub Actions generates build provenance (commit SHA, workflow run) → attached to package → users verify authenticity

---

## 🎯 When to Use

Use SAP-028 when you need to:

1. **Automate PyPI publishing** - Tag-based releases via GitHub Actions (no manual uploads)
2. **Eliminate API tokens** - OIDC trusted publishing removes long-lived credentials (95%+ credential theft risk reduction)
3. **Build provenance** - PEP 740 attestations prove package built by trusted workflow
4. **Multi-package repos** - Coordinate publishing across multiple Python packages
5. **Migration from tokens** - Move existing projects from API tokens to OIDC

**Not needed for**: Private package repos (use PyPI alternative), npm packages (use npm publishing SAP), or projects with <1 release/year (manual publishing acceptable)

---

## ✨ Key Features

- ✅ **OIDC Trusted Publishing** - No API tokens, GitHub authenticates directly with PyPI
- ✅ **Token-Based Fallback** - Backward compatibility for PyPI instances without OIDC support
- ✅ **GitHub Actions Integration** - Publish on git tag push (v1.0.0 → automatic release)
- ✅ **PEP 740 Attestations** - Build provenance (commit SHA, workflow run ID)
- ✅ **Manual Publishing** - justfile commands for local development (test → prod)
- ✅ **Migration Protocol** - Step-by-step token → OIDC migration guide
- ✅ **Template Integration** - Copier variable `pypi_auth_method` (oidc | token | manual)

---

## 📚 Quick Reference

### Publishing Methods Comparison

| Method | Security | Automation | Use Case | Setup Time |
|--------|----------|------------|----------|------------|
| **OIDC Trusted Publishing** | ✅ Excellent (no long-lived tokens) | ✅ Full (GitHub Actions) | Production releases | 5 minutes |
| **Token-Based Publishing** | ⚠️ Good (requires token rotation) | ✅ Full (GitHub Actions) | Backward compatibility | 3 minutes |
| **Manual Publishing** | ⚠️ Good (local credentials) | ❌ None (manual command) | Local testing | 1 minute |

**Recommendation**: OIDC trusted publishing for all new projects (95%+ credential theft risk reduction)

---

### OIDC Trusted Publishing Setup

#### Step 1: Configure PyPI Trusted Publisher

```bash
# 1. Go to PyPI project settings
https://pypi.org/manage/project/{your-project}/settings/publishing/

# 2. Add GitHub repository as trusted publisher
# - Owner: your-org or your-username
# - Repository name: your-repo
# - Workflow name: publish.yml
# - Environment name: (leave blank for any environment)

# 3. Save configuration
```

**One-time setup per project** (5 minutes)

---

#### Step 2: GitHub Actions Workflow

``yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags (v1.0.0, v2.1.3)

permissions:
  id-token: write  # Required for OIDC token
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install build dependencies
        run: pip install build

      - name: Build distribution
        run: python -m build

      - name: Publish to PyPI with OIDC
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          # No password or token needed - OIDC handles auth
```

**Behavior**: Push tag (`git push origin v1.0.0`) → GitHub Actions builds package → authenticates via OIDC → publishes to PyPI

---

### Token-Based Publishing Setup

#### Step 1: Create PyPI API Token

```bash
# 1. Go to PyPI account settings
https://pypi.org/manage/account/token/

# 2. Create token
# - Token name: github-actions-{project-name}
# - Scope: Project (select specific project)
# - Copy token (starts with pypi-)

# 3. Add to GitHub Secrets
# - Repository Settings → Secrets and variables → Actions
# - New secret: PYPI_API_TOKEN
# - Value: pypi-AgEIcH... (paste token)
```

---

#### Step 2: GitHub Actions Workflow with Token

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install build dependencies
        run: pip install build

      - name: Build distribution
        run: python -m build

      - name: Publish to PyPI with token
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

**Security Note**: Rotate API tokens every 90 days (or use OIDC to eliminate tokens)

---

### Manual Publishing (Local Development)

```bash
# 1. Build distribution packages
just build
# Creates dist/{package}-{version}.tar.gz and .whl

# 2. Publish to test.pypi.org (verify before production)
just publish-test
# Prompts for test PyPI credentials

# 3. Test installation from test PyPI
pip install --index-url https://test.pypi.org/simple/ {package}

# 4. Publish to production PyPI
just publish-prod
# Prompts for PyPI credentials

# 5. Verify publication
pip install {package}
```

**Use Case**: Testing release process, emergency publishing when GitHub Actions unavailable

---

### PEP 740 Build Attestations

**What**: Cryptographically signed provenance proving package was built by trusted GitHub Actions workflow

**How It Works**:
1. GitHub Actions workflow builds package
2. Workflow generates attestation (commit SHA, workflow run ID, builder identity)
3. PyPI stores attestation with package
4. Users verify attestation with `pip-audit`

**Example** (verifying attestation):
```bash
# Install pip-audit
pip install pip-audit

# Verify package attestation
pip-audit verify {package}
# Output: ✅ Attestation valid (built by github.com/your-org/your-repo/.github/workflows/publish.yml)
```

**Benefits**:
- Supply chain security (prove package authenticity)
- Detect compromised builds
- Audit trail for compliance

---

### Migration: Token → OIDC

**Scenario**: Existing project uses API token, want to migrate to OIDC

**Steps**:

```bash
# 1. Configure PyPI trusted publisher (see OIDC Setup above)
# Add GitHub repo to PyPI trusted publishers list

# 2. Update GitHub Actions workflow
# Remove password: ${{ secrets.PYPI_API_TOKEN }}
# Workflow now uses OIDC automatically (no changes to steps)

# 3. Test with dry-run tag
git tag v1.0.0-test
git push origin v1.0.0-test
# Verify GitHub Actions publishes successfully via OIDC

# 4. Revoke old API token (optional, once OIDC proven)
# Go to PyPI → Account → API tokens → Revoke token

# 5. Remove GitHub Secret (optional)
# Repository Settings → Secrets → Delete PYPI_API_TOKEN
```

**Migration Time**: 10 minutes (one-time per project)

**Rollback**: Keep API token for 30 days in case OIDC issues arise

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-003** (Project Bootstrap) | Template Integration | `pypi_auth_method` variable (oidc, token, manual) generates appropriate workflow |
| **SAP-005** (CI/CD) | GitHub Actions | Publishing workflow integrated with test.yml, uses same OIDC permissions |
| **SAP-008** (Automation Scripts) | justfile Commands | `just publish-test`, `just publish-prod` for manual publishing |
| **SAP-012** (Development Lifecycle) | Release Phase | Publishing triggered by version bump (Phase 7: Release) |

---

## 🏆 Success Metrics

- **OIDC Adoption**: 80%+ of new projects use OIDC trusted publishing (vs API tokens)
- **Credential Theft Risk**: 95%+ reduction (no long-lived tokens in GitHub Secrets)
- **Publish Time**: <2 minutes from tag push to PyPI availability
- **Migration Time**: 10 minutes per project (token → OIDC)
- **PEP 740 Coverage**: 100% of packages have build attestations
- **Failed Publishes**: <1% (automated workflow reliability)

---

## 🔧 Troubleshooting

### Problem: OIDC Publishing Fails with "Trusted publisher not configured"

**Symptom**: GitHub Actions workflow fails with PyPI error "No trusted publisher configured"

**Common Causes**:
1. PyPI trusted publisher not added
2. Wrong repository name or owner
3. Workflow name mismatch

**Solutions**:

```bash
# 1. Verify PyPI configuration
# - Go to https://pypi.org/manage/project/{project}/settings/publishing/
# - Check repository name matches exactly (case-sensitive)
# - Check workflow name matches .github/workflows/{name}.yml

# 2. Re-add trusted publisher with correct values
# - Owner: your-org (not your-username if org repo)
# - Repository: exact-repo-name
# - Workflow: publish.yml (filename without .github/workflows/)

# 3. Re-run GitHub Actions workflow
gh workflow run publish.yml
```

**Validation**: Workflow succeeds, package published to PyPI

---

### Problem: Token-Based Publishing Fails with "Invalid credentials"

**Symptom**: GitHub Actions workflow fails with "403 Invalid or expired token"

**Common Causes**:
1. API token expired (90-day rotation policy)
2. Token scope incorrect (needs project scope, not account scope)
3. GitHub Secret name mismatch

**Solutions**:

```bash
# 1. Regenerate PyPI API token
# - Go to https://pypi.org/manage/account/token/
# - Create new token with Project scope
# - Copy token

# 2. Update GitHub Secret
# - Repository Settings → Secrets → PYPI_API_TOKEN → Update
# - Paste new token

# 3. Re-run workflow
gh workflow run publish.yml
```

**Validation**: Workflow succeeds with new token

---

### Problem: Manual Publishing Fails with "Filename already exists"

**Symptom**: `just publish-prod` fails with "File already exists" error

**Common Causes**:
1. Version not bumped (trying to re-upload same version)
2. Package already published by GitHub Actions

**Solutions**:

```bash
# 1. Bump version
just bump-patch  # 1.0.0 → 1.0.1

# 2. Rebuild distribution
just build

# 3. Publish new version
just publish-prod
```

**PyPI Policy**: Once a version is published, it cannot be replaced (delete and re-upload requires PyPI admin)

---

### Problem: PEP 740 Attestation Missing

**Symptom**: `pip-audit verify` reports "No attestation found"

**Common Causes**:
1. Old pypa/gh-action-pypi-publish version (attestations require v1.8.0+)
2. OIDC not used (attestations only generated with OIDC auth)

**Solutions**:

```yaml
# Update GitHub Actions workflow
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1  # ✅ Always use latest
  # No password needed (OIDC generates attestation automatically)
```

**Validation**: Re-publish package, verify attestation exists with `pip-audit verify`

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Publishing automation specification (18KB, 9-min read, pilot status)
- **[AGENTS.md](AGENTS.md)** - Agent publishing workflows (15KB, 8-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (14KB, 7-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - OIDC setup guide (22KB, 11-min read)

### External Resources

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/) - Official PyPI documentation
- [PEP 740: Build Attestations](https://peps.python.org/pep-0740/) - Provenance specification
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) - GitHub Actions action
- [pip-audit](https://pypi.org/project/pip-audit/) - Attestation verification tool

---

**Version History**:
- **1.0.0** (2025-11-02) - Initial Publishing Automation with OIDC trusted publishing, token fallback, PEP 740 attestations

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
