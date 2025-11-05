# pypi-demo-beta

**SAP-028 Migration Example (Beta)**

This demonstration package showcases migrating from token-based PyPI publishing to OIDC trusted publishing using [SAP-028 (Publishing Automation)](../../docs/skilled-awareness/publishing-automation/).

## Purpose

Demonstrates **SAP-028 Level 2 adoption**: Token-based projects migrated to OIDC trusted publishing.

Migration metrics:
- ✅ Migration time: 15 minutes
- ✅ Secrets removed: 1 (`PYPI_API_TOKEN`)
- ✅ PEP 740 attestations enabled
- ✅ Zero security incidents post-migration

## Migration Story

### Before (Token-Based Publishing)

```yaml
# .github/workflows/release.yml (OLD)
- name: Publish to PyPI
  run: |
    pip install twine
    twine upload dist/* -u __token__ -p ${{ secrets.PYPI_API_TOKEN }}
```

**Issues**:
- Long-lived `PYPI_API_TOKEN` in GitHub Secrets
- Manual rotation every 90 days
- Token leakage risk
- No build provenance (PEP 740)

### After (OIDC Trusted Publishing)

```yaml
# .github/workflows/release.yml (NEW)
permissions:
  id-token: write  # Required for OIDC

- name: Publish to PyPI (OIDC Trusted Publishing)
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    attestations: true  # PEP 740 build provenance
```

**Benefits**:
- ✅ Zero secrets (ephemeral tokens)
- ✅ No token rotation needed
- ✅ Fine-grained trust (only this repo)
- ✅ PEP 740 build attestations

## Migration Steps (15 minutes)

### 1. Configure PyPI Publisher (5 min)

1. Go to [PyPI Account → Publishing](https://pypi.org/manage/account/publishing/)
2. Add publisher:
   - PyPI Project: `pypi-demo-beta`
   - Owner: `liminalcommons`
   - Repository: `chora-base`
   - Workflow: `release.yml`
   - Environment: `pypi`

### 2. Update GitHub Workflow (5 min)

Replace `twine upload` with `pypa/gh-action-pypi-publish`:

```diff
- - name: Publish with twine
-   run: twine upload dist/* -u __token__ -p ${{ secrets.PYPI_API_TOKEN }}
+ permissions:
+   id-token: write
+
+ - name: Publish to PyPI (OIDC)
+   uses: pypa/gh-action-pypi-publish@release/v1
+   with:
+     attestations: true
```

### 3. Remove Secret & Test (5 min)

1. Delete `PYPI_API_TOKEN` from GitHub Secrets
2. Create a test tag: `git tag v0.1.0 && git push origin v0.1.0`
3. Verify workflow succeeds with OIDC
4. Confirm PEP 740 attestations on PyPI

## Installation

```bash
pip install pypi-demo-beta
```

## Usage

```python
from pypi_demo_beta import verify_migration

result = verify_migration()
print(result)
# Output: {'package': 'pypi-demo-beta', 'publishing_method': 'OIDC trusted publishing', ...}
```

## SAP-028 Adoption

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Secrets Required** | 1 (PYPI_API_TOKEN) | 0 | ✅ 100% reduction |
| **Token Rotation** | Every 90 days | Never | ✅ Zero maintenance |
| **Setup Time** | 30 minutes | 15 minutes (migration) | ✅ 50% faster |
| **Build Provenance** | ❌ None | ✅ PEP 740 | ✅ Supply chain security |
| **Trust Granularity** | Broad (account-level) | Fine (repo-level) | ✅ Principle of least privilege |

## Related

- [SAP-028 Migration Guide](../../docs/skilled-awareness/publishing-automation/adoption-blueprint.md)
- [pypi-demo-alpha](../pypi-demo-alpha/) - New project example
- [chora-compose Migration](https://github.com/liminalcommons/chora-compose) - Production migration

## License

MIT
