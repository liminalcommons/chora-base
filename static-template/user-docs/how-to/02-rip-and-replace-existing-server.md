# How-To: Rip-and-Replace Existing MCP Server

## Quick Reference

**Time:** 2-3 hours
**Risk:** Medium (requires backup)
**Result:** Existing project regenerated from template with all code preserved

---

## Prerequisites

- Existing MCP server with Git history
- Identified project-specific vs template-derivable files
- Backup branch created

---

## Phase 1: Backup (10 min)

```bash
# Create backup branch
git checkout -b backup-pre-rip-replace
git tag backup-v$(grep version pyproject.toml | cut -d'"' -f2)
git push origin backup-pre-rip-replace
git push origin backup-v*

# Document current state
find . -type f -not -path './.git/*' > pre-rip-replace-files.txt
cat pyproject.toml > pre-rip-replace-pyproject.toml
pytest --collect-only > pre-rip-replace-tests.txt
```

---

## Phase 2: Extract Project Assets (15 min)

```bash
# Create migration directory
mkdir MIGRATION_ASSETS

# Copy project-specific code
cp -r src/your_package MIGRATION_ASSETS/
cp -r tests MIGRATION_ASSETS/
cp -r docs MIGRATION_ASSETS/
cp CHANGELOG.md MIGRATION_ASSETS/
cp README.md MIGRATION_ASSETS/README-old.md

# Copy project-specific assets (if exist)
cp -r schemas MIGRATION_ASSETS/ 2>/dev/null || true
cp -r templates MIGRATION_ASSETS/ 2>/dev/null || true
```

---

## Phase 3: Generate Fresh Template (15 min)

```bash
# Navigate to parent directory
cd ..

# Generate new project using blueprints
python setup.py your-project-NEW

# Provide the same answers as the original project:
# - project_name: your-project
# - package_name: your_package
# - include_memory: true  # NEW feature
# - ... (see How-To 01 for full prompts)

# Script initializes git and commits template snapshot automatically.
cd your-project-NEW
```

---

## Phase 4: Migrate Code (20 min)

```bash
# Remove template placeholders
rm -rf src/your_package/*
rm -rf tests/*

# Copy real code
cp -r ../your-project/MIGRATION_ASSETS/your_package/* src/your_package/
cp -r ../your-project/MIGRATION_ASSETS/tests/* tests/

# Copy docs
cp -r ../your-project/MIGRATION_ASSETS/docs/* docs/

# Copy project assets
cp -r ../your-project/MIGRATION_ASSETS/schemas . 2>/dev/null || true
cp -r ../your-project/MIGRATION_ASSETS/templates . 2>/dev/null || true
cp ../your-project/MIGRATION_ASSETS/CHANGELOG.md .
```

---

## Phase 5: Merge Hybrid Files (30 min)

### pyproject.toml

```bash
# Open in editor, merge:
# 1. Template dependencies (fastmcp, pydantic, pytest, ruff, mypy)
# 2. Project-specific dependencies (from MIGRATION_ASSETS/pre-rip-replace-pyproject.toml)
# 3. Project-specific entry points
# 4. Project-specific tool configs (pytest markers, etc.)
```

**Example merge:**
```toml
[project]
dependencies = [
    "pydantic>=2.7",
    "mcp==1.13.1",
    "fastmcp>=0.3.0",
    # ADD PROJECT-SPECIFIC:
    "your-api-client>=0.6.0",
    "httpx>=0.24.0",
]

[project.scripts]
your-mcp-server = "your_package.server:main"
your-mcp-memory = "your_package.cli.memory:main"  # NEW from template
# ADD PROJECT-SPECIFIC:
your-custom-cli = "your_package.cli.custom:main"
```

### README.md

```bash
# Use project README as base
cp MIGRATION_ASSETS/README-old.md README.md

# Add template badge at top (line 3-4)
# [![Template](https://img.shields.io/badge/template-chora--base-blue)](https://github.com/liminalcommons/chora-base)

# Add "Template Origin" section at bottom
```

**Template Origin section:**
```markdown
## Template Origin

This project was regenerated from [chora-base](https://github.com/liminalcommons/chora-base) v1.0.0 template, gaining:
- 18 automation scripts (setup.sh, testing workflows, diagnostics)
- 7 GitHub Actions workflows (CI/CD automation)
- Agent Memory System (event log, knowledge graph, trace context)
- AGENTS.md (machine-readable instructions for AI coding agents)
- Quality gates (ruff, black, mypy, pre-commit hooks)
- justfile task automation

**Regeneration Date:** 2025-10-17
**Previous Version:** v0.6.0 (backup-v0.6.0 tag)
```

---

## Phase 6: Adapt Template Features (20 min)

### AGENTS.md

```bash
# Open AGENTS.md, customize:
# 1. Project Overview → Add project-specific architecture
# 2. Common Tasks → Replace generic examples with project-specific workflows
# 3. Architecture Constraints → Add project-specific patterns
```

**Example customization:**
```markdown
## Common Tasks

### Adding a New Tool

1. Create tool function in `src/your_package/tools/your_tool.py`
2. Register tool with `@mcp.tool()` decorator
3. Add BDD scenario in `tests/features/test_your_tool.feature` (if using pytest-bdd)
4. Run `pytest tests/features/` to validate
```

### scripts/

```bash
# Adapt scripts to project specifics:

# scripts/smoke-test.sh
# Change from:
# pytest tests/ -m "not slow"
# To:
# pytest tests/unit tests/contracts -v

# scripts/integration-test.sh
# Change from:
# pytest tests/ -m integration
# To:
# pytest tests/features tests/e2e -v
```

### .github/workflows/

```bash
# Update workflows with project secrets:

# .github/workflows/test.yml
# Add environment variables:
# env:
#   YOUR_API_KEY: ${{ secrets.YOUR_API_KEY }}

# .github/workflows/release.yml
# Update PyPI token secret name:
# TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN_YOUR_PROJECT }}
```

---

## Phase 7: Validate (15 min)

```bash
# Install dependencies
./scripts/setup.sh

# Run smoke tests
./scripts/smoke-test.sh

# Compare test count with pre-rip-replace
pytest --collect-only | grep "test session starts" -A 5
# Should match: cat ../your-project/pre-rip-replace-tests.txt

# Run full test suite
./scripts/integration-test.sh

# Run pre-merge validation
./scripts/pre-merge.sh
```

**Validation checklist:**
- [ ] All tests passing (same count as before)
- [ ] Test coverage ≥ 85%
- [ ] Lint checks passing (ruff)
- [ ] Type checks passing (mypy)
- [ ] Format checks passing (black)

---

## Phase 8: Replace Old Repo (10 min)

```bash
# Navigate to old repo
cd ../../your-project

# Remove all files except .git
find . -not -path './.git/*' -not -name '.git' -type f -delete
find . -not -path './.git/*' -not -name '.git' -type d -empty -delete

# Copy new structure
cp -r ../your-project-NEW/* .
cp -r ../your-project-NEW/.* . 2>/dev/null || true

# Commit rip-replace
git add -A
git commit -m "feat: Rip-replace with chora-base v1.0.0 infrastructure

Complete regeneration from chora-base template...
(See commit message template in docs/reference/commit-messages.md)
"

# Tag major version bump
git tag v1.0.0

# Push to GitHub
git push origin main
git push origin v1.0.0
```

---

## Post-Migration

### Update GitHub Repo Settings

1. Add topics: `mcp`, `chora-base`, `model-context-protocol`
2. Update description: "MCP server (chora-base template)"
3. Add secrets (if needed): `YOUR_API_KEY`, `PYPI_TOKEN_YOUR_PROJECT`

### Create GitHub Release

```bash
gh release create v1.0.0 \
  --title "v1.0.0 - Rip-Replace with chora-base Infrastructure" \
  --notes "See CHANGELOG.md for details"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Test count mismatch | Check MIGRATION_ASSETS completeness: `ls -R MIGRATION_ASSETS/tests/` |
| Dependency conflicts | Review pyproject.toml merge for version pins |
| Scripts failing | Check project-specific paths in scripts/integration-test.sh |
| Workflows failing | Verify GitHub secrets are set: `gh secret list` |
| Pre-commit hooks failing | Run `pre-commit run --all-files` to see errors |

---

## Next Steps

- [How-To: Customize AGENTS.md](03-customize-agents-md.md)
- [How-To: Add Memory System to Existing Tools](04-add-memory-to-tools.md)
- [Reference: Rip-and-Replace Decision Matrix](../reference/rip-and-replace-decision-matrix.md)
