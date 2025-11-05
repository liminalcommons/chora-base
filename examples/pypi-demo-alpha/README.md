# pypi-demo-alpha

**SAP-028 OIDC Publishing Demonstration Package (Alpha)**

This is a minimal demonstration package showcasing [SAP-028 (Publishing Automation)](../../docs/skilled-awareness/publishing-automation/) with OIDC trusted publishing to PyPI.

## Purpose

Validates SAP-028 adoption for **L3 maturity** (Organization-wide OIDC adoption, 5+ projects).

This demo project demonstrates:
- ✅ OIDC trusted publishing (zero secrets)
- ✅ PEP 740 attestations (build provenance)
- ✅ GitHub Actions release workflow
- ✅ 5-minute setup time

## SAP-028 Configuration

### OIDC Trusted Publishing

This project uses **OIDC trusted publishing** as configured in [.github/workflows/release.yml](./.github/workflows/release.yml):

```yaml
permissions:
  id-token: write  # Required for OIDC

steps:
  - name: Publish to PyPI (OIDC Trusted Publishing)
    uses: pypa/gh-action-pypi-publish@release/v1
    with:
      attestations: true  # PEP 740 build provenance
```

**No secrets required!** The trust relationship is configured on PyPI:
1. Go to PyPI → Account → Publishing
2. Add publisher: `liminalcommons/chora-base` → `pypi-demo-alpha`
3. GitHub Actions can now publish without API tokens

### Security Benefits

- **Zero secrets**: No `PYPI_API_TOKEN` in GitHub Secrets
- **Fine-grained trust**: Only this repository can publish `pypi-demo-alpha`
- **Build provenance**: PEP 740 attestations verify build integrity
- **No token rotation**: Ephemeral tokens automatically generated per release

## Installation

```bash
pip install pypi-demo-alpha
```

## Usage

```python
from pypi_demo_alpha import hello_sap028

print(hello_sap028())
# Output: "Hello from pypi-demo-alpha! Published to PyPI using SAP-028..."
```

## Publishing a Release

```bash
# Tag a new version
git tag v0.1.0
git push origin v0.1.0

# GitHub Actions automatically:
# 1. Builds the package
# 2. Generates PEP 740 attestations
# 3. Publishes to PyPI using OIDC (no secrets!)
```

## SAP-028 Adoption

| Metric | Value |
|--------|-------|
| **Adoption Level** | L1 (Basic) |
| **Publishing Method** | OIDC Trusted Publishing |
| **Setup Time** | 5 minutes |
| **Secrets Required** | 0 |
| **PEP 740 Attestations** | ✅ Enabled |

## Related

- [SAP-028 Documentation](../../docs/skilled-awareness/publishing-automation/)
- [OIDC Publishing Setup Guide](../../docs/skilled-awareness/publishing-automation/adoption-blueprint.md)
- [chora-base Template](../../static-template/)

## License

MIT
