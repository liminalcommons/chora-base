# Adoption Blueprint: CI/CD Workflows

**SAP ID**: SAP-005
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides using chora-base's GitHub Actions workflows for CI/CD automation.

**Time Estimate**: 5-10 minutes to understand, workflows run automatically

---

## 2. Prerequisites

- Generated project from chora-base (SAP-003)
- GitHub repository created
- Workflows pushed to .github/workflows/

---

## 3. Quick Start

### Step 1: View Workflows

Navigate to GitHub repository → **Actions** tab

**You'll see**:
- Test (runs on every push/PR)
- Lint (runs on every push/PR)
- CodeQL (security scanning)
- Docs Quality (when docs change)

### Step 2: Understanding Status

**Green checkmark** (✅): Workflow passed
**Red X** (❌): Workflow failed
**Yellow circle** (🟡): Workflow running

### Step 3: When Workflows Fail

1. Click failed workflow
2. Click failed job
3. Read error message
4. Fix issue locally
5. Push again (workflows re-run automatically)

---

## 4. Required vs Optional Workflows

**Required** (must pass for merge):
- ✅ test.yml - Tests + coverage ≥85%
- ✅ lint.yml - Ruff + mypy
- ✅ smoke.yml - Smoke tests
- ✅ codeql.yml - Security scanning
- ✅ dependency-review.yml - Dependency security (PRs only)

**Optional** (recommended):
- ⚠️ docs-quality.yml - Documentation validation

---

## 5. Customizing Workflows

**Add Python version to matrix**:
```yaml
# .github/workflows/test.yml
matrix:
  python-version: ["3.11", "3.12", "3.13", "3.14"]  # Add 3.14
```

**Change coverage threshold**:
```yaml
# .github/workflows/test.yml
run: pytest --cov=src --cov-fail-under=90  # Change from 85 to 90
```

**Best Practice**: Test changes locally first

---

## 6. Troubleshooting

**Problem**: Test workflow fails with "coverage <85%"
**Solution**: Run `pytest --cov=src --cov-report=term-missing` locally, increase coverage

**Problem**: Lint workflow fails with ruff errors
**Solution**: Run `ruff check . --fix` locally, commit fixes

**Problem**: CodeQL finds vulnerabilities
**Solution**: Review Security tab, fix vulnerability, push fix

---

## 7. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the CI/CD Workflows capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover GitHub Actions workflows
- Quick reference for CI/CD operations
- Links to workflow documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### CI/CD Workflows

Automated GitHub Actions workflows for testing, linting, security scanning, and deployment.

**Documentation**: [docs/skilled-awareness/ci-cd-workflows/](docs/skilled-awareness/ci-cd-workflows/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/ci-cd-workflows/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/ci-cd-workflows/awareness-guide.md)

**Key Workflows**:
- test.yml: Runs tests + coverage check (required)
- lint.yml: Code quality checks (required)
- codeql.yml: Security scanning (required)
- docs-quality.yml: Documentation validation (optional)
```

**Validation**:
```bash
grep "CI/CD Workflows" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 8. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [testing-framework/](../testing-framework/) - SAP-004
- [quality-gates/](../quality-gates/) - SAP-006

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint
