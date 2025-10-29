# Adoption Blueprint: chora-base Template Repository

**SAP ID**: SAP-002
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Last Updated**: 2025-10-27

---

## 1. Overview

This blueprint guides **adopters** through using chora-base to generate production-ready Python projects.

**What You'll Get**:
- New Python project with full chora-base scaffolding
- All 14 capabilities (current + planned features)
- Production-ready: tests, docs, CI/CD, quality gates

**Time Estimate**: 20-40 seconds (generation), 15-30 minutes (customization)

---

## 2. Prerequisites

### Required

- **Python**: 3.11 or later
- **Git**: 2.0+ (for version control)
- **chora-base**: Clone of chora-base repository

### Optional

- **Docker**: For containerized development (if --no-docker not used)
- **GitHub Account**: For CI/CD workflows

---

## 3. Installation

### Step 1: Clone chora-base

```bash
git clone https://github.com/your-org/chora-base.git
cd chora-base
```

### Step 2: Generate Project

**Basic generation**:
```bash
python setup.py my-project
```

**With author info**:
```bash
python setup.py my-project \
  --author "Your Name" \
  --email "your.email@example.com"
```

**With optional features disabled**:
```bash
python setup.py my-project \
  --no-docker      # Skip Docker files
  --no-memory      # Skip A-MEM system
  --no-claude      # Skip Claude-specific files
```

**Overwrite existing** (careful!):
```bash
python setup.py my-project --force
```

### Step 3: Navigate to Project

```bash
cd my-project
```

### Step 4: Validate Generation

```bash
# Check tests loadable
pytest --collect-only

# Run tests
pytest

# Check coverage
pytest --cov

# Expected: All tests pass, coverage ≥85%
```

### Step 5: Customize Project

**Review generated files**:
- `README.md` - Update description
- `pyproject.toml` - Verify metadata
- `AGENTS.md` - Review agent guidance
- `src/<package>/` - Start implementing features

**Initialize git** (if not already done):
```bash
git add .
git commit -m "Initial commit from chora-base v3.3.0"
```

### Step 6: Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Step 7: Validate Setup

```bash
# Run all checks
just pre-merge

# Expected: All checks pass
```

---

## 4. Configuration

### Required Configuration

**PyPI Publishing** (if releasing to PyPI):
1. Create PyPI account
2. Generate API token
3. Add to GitHub secrets: `PYPI_TOKEN`

**GitHub Actions**:
1. Enable Actions in repository settings
2. Add secrets as needed (PYPI_TOKEN, etc.)

### Optional Configuration

**Docker** (if Docker enabled):
- Review `Dockerfile` and `docker-compose.yml`
- Customize base images, environment variables

**A-MEM** (if memory enabled):
- Review `.chora/memory/README.md`
- Configure event logging, knowledge graph

**Claude** (if Claude files enabled):
- Review `CLAUDE.md`
- Customize context management patterns

---

## 5. Upgrade Path

### Upgrading Generated Project

**When chora-base releases new version**:

1. **Check changelog**:
   ```bash
   # In chora-base repo
   cat CHANGELOG.md
   ```

2. **Read upgrade guide**:
   ```bash
   cat docs/upgrades/v<old>-to-<new>.md
   ```

3. **Apply changes manually**:
   - Copy new files from `static-template/`
   - Update blueprints if customized
   - Run tests to verify

4. **Update project metadata**:
   - Update README with new chora-base version
   - Commit: `chore: Upgrade to chora-base v<version>`

**Note**: Automated upgrade tooling planned for Phase 4.

---

## 6. Validation

### Post-Generation Checklist

```bash
# ✅ Tests loadable
pytest --collect-only

# ✅ Tests pass
pytest

# ✅ Coverage adequate
pytest --cov
# Expected: ≥85%

# ✅ No placeholders
grep -r "{{" src/
# Expected: No results

# ✅ Imports work
python -c "import <package_name>"
# Expected: No errors

# ✅ Git initialized
git log
# Expected: Initial commit

# ✅ Pre-commit works
pre-commit run --all-files
# Expected: All hooks pass
```

---

## 7. Troubleshooting

### Problem: Generation fails

**Symptom**: Error during `python setup.py`

**Solutions**:
- Check Python version: `python --version` (need 3.11+)
- Check directory doesn't exist (or use `--force`)
- Check permissions (write access to parent directory)

### Problem: Tests fail after generation

**Symptom**: `pytest` shows failures

**Solutions**:
- Check all dependencies installed: `pip install -e ".[dev]"`
- Check Python version matches `pyproject.toml`
- Review test output for specific errors
- Verify no placeholders: `grep -r "{{" src/`

### Problem: Pre-commit fails

**Symptom**: `git commit` blocked by hooks

**Solutions**:
- Run hooks manually: `pre-commit run --all-files`
- Fix reported issues (whitespace, YAML, formatting)
- Re-run commit

### Problem: Can't find capability

**Symptom**: Feature mentioned in docs doesn't exist in generated project

**Solutions**:
- Check capability status in [INDEX.md](../INDEX.md)
- May be Planned (not yet implemented)
- Check chora-base version (some features in newer versions only)

---

## 8. Next Steps

### After Generation

1. **Implement Features**:
   - Start in `src/<package>/`
   - Follow DDD → BDD → TDD workflow
   - Reference `dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md`

2. **Write Documentation**:
   - Add tutorials: `user-docs/tutorials/`
   - Add how-tos: `user-docs/how-to/`
   - Follow Diataxis structure

3. **Set Up CI/CD**:
   - Push to GitHub
   - Enable Actions
   - Add secrets (PyPI token, etc.)

4. **Adopt SAPs**:
   - Review available SAPs in [INDEX.md](../INDEX.md)
   - Install SAPs as needed (e.g., inbox-coordination)
   - Follow SAP adoption blueprints

---

## 9. Support

### Getting Help

**Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance
- [protocol-spec.md](protocol-spec.md) - All capabilities
- [INDEX.md](../INDEX.md) - SAP status

**Issues**:
- Open issue in chora-base repository
- Include: chora-base version, command run, error message

**Community**:
- Check existing issues for similar problems
- Review examples/ for reference implementations

---

## 10. Related Documents

**chora-base-meta SAP**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - All 14 capabilities
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [ledger.md](ledger.md) - Adopter tracking

**chora-base Core**:
- [README.md](/README.md) - Overview
- [AGENTS.md](/AGENTS.md) - Agent guidance
- [CHANGELOG.md](/CHANGELOG.md) - Version history
- [CLAUDE_SETUP_GUIDE.md](/CLAUDE_SETUP_GUIDE.md) - Claude setup

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [INDEX.md](../INDEX.md) - All SAPs

---

**Version History**:
- **1.0.0** (2025-10-27): Initial adoption blueprint for chora-base meta-SAP
