# PyPI Publishing Setup Guide

This guide explains how to set up PyPI publishing for {{ project_slug }}.

## Quick Start

{% if pypi_auth_method == 'token' -%}
This project is configured to use **token-based authentication** for PyPI publishing.

### Step 1: Create PyPI API Token

1. Go to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
2. Click "Add API token"
3. **Name**: `GitHub Actions - {{ project_slug }}`
4. **Scope**: Choose one:
   - **"Entire account"** (easier, works immediately)
   - **Specific project** (more secure, requires project to exist first)

5. Click "Add token"
6. **Copy the token** (starts with `pypi-...`) - you won't see it again!

### Step 2: Add Token to GitHub Secrets

1. Go to your repository settings: `https://github.com/{{ github_username }}/{{ project_slug }}/settings/secrets/actions`
2. Click "New repository secret"
3. **Name**: `PYPI_TOKEN`
4. **Secret**: Paste your PyPI token (the one starting with `pypi-...`)
5. Click "Add secret"

### Step 3 (Optional): Test with TestPyPI

For testing releases before publishing to production PyPI:

1. Create TestPyPI token at [https://test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)
2. Add as GitHub secret: `TEST_PYPI_TOKEN`
3. Test your release:
   ```bash
   ./scripts/prepare-release.sh patch
   ./scripts/build-dist.sh
   ./scripts/publish-test.sh  # Publishes to TestPyPI
   ```

### Step 4: Publish to Production PyPI

Once everything is tested:

```bash
# Tag and push (triggers GitHub Actions)
git tag v{{ project_version }}
git push --tags

# Or publish manually:
./scripts/publish-prod.sh
```

**GitHub Actions workflow** (`.github/workflows/release.yml`) will:
1. Build distribution packages
2. Run test suite
3. Publish to PyPI using `PYPI_TOKEN`
4. Create GitHub release

---

## Optional: Migrate to Trusted Publishing

For enhanced security, you can migrate to PyPI trusted publishing (no long-lived tokens needed).

### Benefits of Trusted Publishing

✅ **More secure** - No long-lived API tokens
✅ **No token rotation** - Uses short-lived OIDC tokens
✅ **Audit trail** - PyPI shows GitHub Actions identity in publish history

❌ **GitHub Actions only** - Cannot use with local scripts (`publish-prod.sh`)
❌ **Requires PyPI setup** - Must configure publisher on PyPI.org

### Migration Steps

1. **Configure PyPI Publisher:**
   - Go to [https://pypi.org/manage/project/{{ project_slug }}/settings/publishing/](https://pypi.org/manage/project/{{ project_slug }}/settings/publishing/)
   - Click "Add a new publisher"
   - Fill in:
     - **PyPI Project Name**: `{{ project_slug }}`
     - **Owner**: `{{ github_username }}`
     - **Repository name**: `{{ project_slug }}`
     - **Workflow filename**: `release.yml`
     - **Environment name**: `pypi` (optional)
   - Click "Add"

2. **Update Workflow File** (`.github/workflows/release.yml`):
   ```yaml
   permissions:
     contents: write
     id-token: write  # Enable OIDC trusted publishing

   jobs:
     publish-pypi:
       environment:
         name: pypi
         url: https://pypi.org/p/{{ project_slug }}
       steps:
         - name: Publish to PyPI using trusted publishing
           uses: pypa/gh-action-pypi-publish@release/v1
           # No password/token needed - uses OIDC
   ```

3. **Remove GitHub Secret:**
   - Delete `PYPI_TOKEN` from repository secrets (no longer needed)

4. **Test the Setup:**
   ```bash
   git tag v{{ project_version }}
   git push --tags
   # GitHub Actions will publish using trusted publishing
   ```

{% else -%}
This project is configured to use **trusted publishing (OIDC)** for PyPI publishing.

### Step 1: Publish Your First Release

Before PyPI trusted publishing can work, your project must exist on PyPI. Use a token for the first release:

1. Create a **temporary** PyPI token at [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
   - Scope: "Entire account"
2. Publish first release manually:
   ```bash
   ./scripts/prepare-release.sh patch
   ./scripts/build-dist.sh

   # Upload using token
   twine upload dist/* -u __token__ -p pypi-YOUR_TOKEN_HERE
   ```

### Step 2: Configure Trusted Publisher on PyPI

Once your project exists on PyPI:

1. Go to [https://pypi.org/manage/project/{{ project_slug }}/settings/publishing/](https://pypi.org/manage/project/{{ project_slug }}/settings/publishing/)
2. Click "Add a new publisher"
3. Fill in:
   - **PyPI Project Name**: `{{ project_slug }}`
   - **Owner**: `{{ github_username }}`
   - **Repository name**: `{{ project_slug }}`
   - **Workflow filename**: `release.yml`
   - **Environment name**: `pypi`
4. Click "Add"

### Step 3: Verify Workflow Configuration

Your `.github/workflows/release.yml` should already have:

```yaml
permissions:
  contents: write
  id-token: write  # OIDC trusted publishing

jobs:
  publish-pypi:
    environment:
      name: pypi
      url: https://pypi.org/p/{{ project_slug }}
    steps:
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No password needed - uses OIDC
```

### Step 4: Publish via GitHub Actions

```bash
# Tag and push (triggers GitHub Actions)
git tag v0.2.0
git push --tags

# GitHub Actions will:
# 1. Build distribution
# 2. Run tests
# 3. Publish to PyPI using trusted publishing
# 4. Create GitHub release
```

**No API tokens needed!** GitHub Actions uses OIDC to authenticate.

---

## Optional: Use Token-Based Publishing

If you prefer simpler token-based publishing (works with local scripts):

### Downgrade to Token-Based

1. **Create PyPI token** at [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
2. **Add to GitHub secrets**: `PYPI_TOKEN`
3. **Update workflow** (`.github/workflows/release.yml`):
   ```yaml
   permissions:
     contents: write
     # Remove: id-token: write

   jobs:
     publish-pypi:
       # Remove environment block
       steps:
         - name: Publish to PyPI using token
           uses: pypa/gh-action-pypi-publish@release/v1
           with:
             password: ${{ "{{" }} secrets.PYPI_TOKEN }}
   ```

### Benefits of Token-Based

✅ **Simpler setup** - Just add a secret
✅ **Works locally** - Can use `publish-prod.sh` script
✅ **No PyPI configuration** - Works immediately

❌ **Less secure** - Long-lived token
❌ **Token rotation** - Must rotate periodically

{% endif -%}

---

## Local Publishing (Manual)

### Using Scripts

```bash
# Prepare release
./scripts/prepare-release.sh patch  # or minor, major

# Build distribution
./scripts/build-dist.sh

# Test on TestPyPI (requires TEST_PYPI_TOKEN in .env)
./scripts/publish-test.sh

# Verify installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ {{ project_slug }}

# Publish to production PyPI{% if pypi_auth_method == 'token' %} (requires PYPI_TOKEN in .env){% else %} (requires manual token){% endif %}
./scripts/publish-prod.sh
```

### Using `twine` directly

```bash
# Build
python -m build

# Check distribution
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to production PyPI
twine upload dist/*
```

---

## Troubleshooting

### Error: "Invalid or non-existent authentication information"

{% if pypi_auth_method == 'token' -%}
- **Cause**: `PYPI_TOKEN` secret is missing or incorrect
- **Fix**: Verify token in GitHub repository secrets
- **Check**: Token should start with `pypi-`
{% else -%}
- **Cause**: Trusted publisher not configured on PyPI.org
- **Fix**: Follow [Step 2: Configure Trusted Publisher](#step-2-configure-trusted-publisher-on-pypi)
- **Check**: Verify repository, workflow filename, and environment name match exactly
{% endif -%}

### Error: "Project name already exists"

- **Cause**: Project name `{{ project_slug }}` is already taken on PyPI
- **Fix**: Choose a different name in `pyproject.toml`:
  ```toml
  [project]
  name = "{{ project_slug }}-yourname"  # Make it unique
  ```

### Error: "File already exists"

- **Cause**: Version `{{ project_version }}` already published
- **Fix**: Bump version number:
  ```bash
  ./scripts/prepare-release.sh patch  # Increments version
  ```

### Local publish fails: "No such file or directory: '.env'"

- **Cause**: `.env` file missing (needed for local scripts)
- **Fix**: Create `.env` file:
  ```bash
  cp .env.example .env
  # Add your tokens:
  echo "PYPI_TOKEN=pypi-YOUR_TOKEN_HERE" }} .env
  echo "TEST_PYPI_TOKEN=pypi-YOUR_TEST_TOKEN_HERE" }} .env
  ```

---

## Best Practices

1. **Always test on TestPyPI first**
   ```bash
   ./scripts/publish-test.sh
   pip install --index-url https://test.pypi.org/simple/ {{ project_slug }}
   ```

2. **Use semantic versioning**
   - MAJOR: Breaking changes (1.0.0 → 2.0.0)
   - MINOR: New features, backward compatible (1.0.0 → 1.1.0)
   - PATCH: Bug fixes (1.0.0 → 1.0.1)

3. **Update CHANGELOG.md before releasing**
   ```bash
   ./scripts/prepare-release.sh patch  # Auto-updates CHANGELOG
   ```

4. **Verify build before publishing**
   ```bash
   ./scripts/build-dist.sh
   twine check dist/*
   ```

5. **Tag releases in git**
   ```bash
   git tag v{{ project_version }}
   git push --tags
   ```

---

## Related Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [README.md](README.md) - Project overview
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) - Official docs
- [twine documentation](https://twine.readthedocs.io/) - Package upload tool

---

**Need help?** Open an issue at [the project repository](https://github.com/{{ github_username }}/{{ project_slug }}/issues)
