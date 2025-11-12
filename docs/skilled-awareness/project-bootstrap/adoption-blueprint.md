# Adoption Blueprint: Project Bootstrap

**SAP ID**: SAP-003
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides **adopters** (humans and AI agents) through using chora-base's project bootstrap capability to generate new Python projects.

**What You'll Do**:
- Generate a new Python project from chora-base template
- Validate the generated project
- Customize the project for your needs
- Understand upgrade paths

**Time Estimate**: 1-2 minutes (agent with fast-setup), 5-10 minutes (human with fast-setup)

**Historical Time** (pre-v4.9.0): 30-40 minutes (manual SAP-by-SAP adoption)

---

## 2. Prerequisites

### Required Software

- **Python**: 3.11 or later
- **Git**: 2.0 or later
- **chora-base**: Clone of chora-base repository

### Required Knowledge

- Basic Python project structure
- Git basics (commit, push)
- Command line usage

### Required Access

- Write access to directory where project will be created
- Git configured (user.name, user.email)

---

## 3. Installing the SAP

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-003 --source /path/to/chora-base
```

**What This Installs**:
- project-bootstrap capability documentation (5 artifacts)
- static-template/ directory with all project scaffolding files

### Part of Sets

This SAP is included in:
- recommended
- full
- testing-focused
- mcp-server

To install a complete set:
```bash
python scripts/install-sap.py --set recommended --source /path/to/chora-base
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/project-bootstrap/*.md
ls static-template/
```

---

## 4. Generation Workflow

### Step 1: Clone chora-base

Clone the chora-base template repository:

```bash
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base
```

**Validation**:
```bash
ls static-template/ && echo "Note: setup.py and blueprints/ removed in Wave 3 Phase 5" && echo "✅ chora-base ready"
```

### Step 2: Prepare Project Information

Decide on your project details:

**Required Information**:
- **Project Name**: Display name (e.g., "MCP GitHub")
- **Project Description**: One-line description
- **Author Name**: Your full name
- **Author Email**: Your email address
- **GitHub Username**: Your GitHub handle

**Auto-Derived** (create-capability-server.py will calculate):
- **Project Slug**: Kebab-case (e.g., "mcp-github" from "MCP GitHub")
- **Package Name**: Snake_case (e.g., "mcp_github" from "mcp-github")
- **MCP Namespace**: No separators (e.g., "github" from "mcp_github")
- **Author Info**: From git config (user.name, user.email) if not provided
- **GitHub Username**: From git remote origin or derived from author name

**Example**:
```
Project Name: MCP GitHub
Description: GitHub operations via MCP
Author: Alice Smith
Email: alice@example.com
GitHub Username: alice-smith

Derived:
  Project Slug: mcp-github
  Package Name: mcp_github
  MCP Namespace: mcpgithub
```

### Step 3: Run Fast-Setup Script

**New (v4.9.0+): One-Command Setup**

Use the fast-setup script to create a "model citizen" MCP server with all chora-base infrastructure:

```bash
python scripts/create-capability-server.py \
    --name "MCP GitHub" \
    --namespace github \
    --output ~/projects/mcp-github
```

**What This Creates**:
- FastMCP server scaffold
- Beads task tracking (SAP-015)
- Inbox coordination (SAP-001)
- A-MEM memory system (SAP-010)
- CI/CD workflows (SAP-005)
- Quality gates (SAP-006)
- Testing framework (SAP-004)
- Documentation (SAP-007)
- Agent awareness (SAP-009)

**Setup Time**: 1-2 minutes (agent), 5-10 minutes (human)

**For Agents** (programmatic):
```python
import subprocess

# Run fast-setup script
result = subprocess.run([
    "python", "scripts/create-capability-server.py",
    "--name", "MCP GitHub",
    "--namespace", "github",
    "--output", "/path/to/mcp-github",
], check=True, capture_output=True, text=True)

# Validation automatically runs
print(result.stdout)
```

**Historical Note**:
- setup.py removed in Wave 3 Phase 5 (Oct 29, 2025, commit f7e5f26)
- Replaced with create-capability-server.py in v4.9.0 (Nov 6, 2025)
- New approach: Dynamic template rendering with decision profiles

**Output** (expected):
```
================================================================================
Create Model Citizen MCP Server v1.0.0
Chora-Base v4.9.0
================================================================================

📋 Using profile: standard
   FastMCP + beads + inbox, full CI/CD (DEFAULT)

🔧 Deriving project variables...
   Auto-derived namespace: github

📦 Project Configuration
────────────────────────────────────────────────────────────────────────────────
  Project Name:     MCP GitHub
  Project Slug:     mcp-github
  Package Name:     mcp_github
  MCP Namespace:    github
  Description:      MCP GitHub - MCP server for github operations
  Author:           Alice Smith <alice@example.com>
  GitHub:           alice-smith
  Python Version:   3.11
  License:          MIT
  Profile:          standard
────────────────────────────────────────────────────────────────────────────────

📁 Creating project at: /path/to/mcp-github

📂 Creating directory structure...
  ✓ Created src/mcp_github/
  ✓ Created tests/
  ✓ Created docs/user-docs/
  ✓ Created .beads/
  ✓ Created inbox/coordination/
  ✓ Created .chora/memory/events/

📋 Copying static files...
  ✓ Copied .github/workflows/test.yml
  ✓ Copied .gitignore

Rendering templates...
  ✓ Rendered src/mcp_github/server.py
  ✓ Rendered pyproject.toml
  ✓ Rendered AGENTS.md
  ✓ Rendered CLAUDE.md

Initializing beads (SAP-015)...
  ✓ Created .beads/config.yaml
  ✓ Created .beads/issues.jsonl

Initializing inbox (SAP-001)...
  ✓ Created inbox/coordination/active.jsonl

Initializing A-MEM (SAP-010)...
  ✓ Created .chora/memory/events/development.jsonl

Initializing git repository...
  ✓ Initialized git repository
  ✓ Created initial commit

Validating generated project...
  ✅ FastMCP server exists
  ✅ MCP namespace module exists
  ✅ AGENTS.md with YAML frontmatter
  ✅ CLAUDE.md exists
  ✅ Beads initialized
  ✅ Inbox initialized
  ✅ Memory system initialized
  ✅ Testing framework configured
  ✅ CI/CD workflows configured
  ✅ Quality gates configured
  ✅ Documentation structure
  ✅ No unsubstituted variables

================================================================================
✅ Model Citizen MCP Server Created Successfully!
================================================================================

📁 Location: /path/to/mcp-github

📝 Next Steps:
  1. cd /path/to/mcp-github
  2. Create virtual environment: python -m venv venv && source venv/bin/activate
  3. Install dependencies: pip install -e .[dev]
  4. Run tests: pytest

🚀 Happy coding!
```

**Time**: 1-2 minutes (agent), 5-10 minutes (human)

### Step 4: Validate Generated Project

**Automated Validation (v4.9.0+)**:

The create-capability-server.py script automatically runs validation after generation. To manually re-validate:

```bash
cd /path/to/mcp-github
python /path/to/chora-base/scripts/validate-model-citizen.py
```

**Output**:
```
================================================================================
Model Citizen MCP Server Validation v1.0.0
================================================================================

Project: /path/to/mcp-github

✅ FastMCP server exists
✅ MCP namespace module exists
✅ AGENTS.md with YAML frontmatter
✅ CLAUDE.md exists
✅ Beads initialized
✅ Inbox initialized
✅ Memory system initialized
✅ Testing framework configured
✅ CI/CD workflows configured
✅ Quality gates configured
✅ Documentation structure
✅ No unsubstituted variables

================================================================================
Summary
================================================================================
  Passed:    12/12
  Failed:    0 required checks
  Warnings:  0 recommended checks

✅ Project is MODEL CITIZEN COMPLIANT!
```

**Strict Validation** (fail on warnings):
```bash
python /path/to/chora-base/scripts/validate-model-citizen.py --strict
```

**JSON Output** (for programmatic use):
```bash
python /path/to/chora-base/scripts/validate-model-citizen.py --format json
```

**All checks pass**: ✅ Generation successful, proceed to development

**Any check fails**: Re-run create-capability-server.py or fix issues manually

### Step 5: Initial Development Setup

**Install dependencies**:
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

**Run tests**:
```bash
pytest  # Should pass (example tests included)
```

**Start development**:
```bash
# Edit your MCP server implementation
# File: src/mcp_github/mcp/server.py

# Test changes
pytest

# Start dev server
./scripts/dev-server.sh
```

### Step 6: Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Project Bootstrap capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover project scaffolding and initialization tools
- Quick reference for creating new chora-base projects
- Links to bootstrap templates and patterns

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
### Project Bootstrap

Copier-based project scaffolding for creating new chora-base repositories with complete infrastructure, testing, and CI/CD setup.

**Documentation**: [docs/skilled-awareness/project-bootstrap/](docs/skilled-awareness/project-bootstrap/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/project-bootstrap/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/project-bootstrap/awareness-guide.md)

**Features**:
- Complete project structure generation
- Pre-configured testing framework (pytest, coverage)
- CI/CD workflows (GitHub Actions)
- Docker support with compose configurations
- Quality gates (ruff, mypy, coverage ≥85%)
```

**Validation**:
```bash
grep "Project Bootstrap" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 4. Validation Checklist

Run this complete validation after generation:

```bash
#!/bin/bash
# Full validation script

echo "🔍 Validating generated project..."

# 1. Critical files exist
echo "1️⃣ Checking critical files..."
files=(
    "pyproject.toml"
    "README.md"
    "AGENTS.md"
    "CHANGELOG.md"
    "src/mcp_github/__init__.py"
    "src/mcp_github/mcp/server.py"
    "tests/conftest.py"
    ".github/workflows/test.yml"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
        exit 1
    fi
done

# 2. No unreplaced placeholders
echo "2️⃣ Checking for unreplaced placeholders..."
if grep -rq "{{" . --exclude-dir=.git --exclude-dir=__pycache__; then
    echo "  ❌ Found unreplaced placeholders:"
    grep -r "{{" . --exclude-dir=.git --exclude-dir=__pycache__
    exit 1
else
    echo "  ✅ No unreplaced placeholders"
fi

# 3. Tests loadable
echo "3️⃣ Checking tests loadable..."
if pytest --collect-only > /dev/null 2>&1; then
    count=$(pytest --collect-only 2>&1 | grep "test" | wc -l)
    echo "  ✅ Tests loadable ($count tests)"
else
    echo "  ❌ Tests not loadable"
    pytest --collect-only
    exit 1
fi

# 4. Git initialized
echo "4️⃣ Checking git initialized..."
if git log --oneline > /dev/null 2>&1; then
    echo "  ✅ Git initialized ($(git log --oneline | wc -l) commits)"
else
    echo "  ❌ Git not initialized"
    exit 1
fi

# 5. Python package valid
echo "5️⃣ Checking Python package valid..."
if python -c "import sys; sys.path.insert(0, 'src'); import mcp_github" 2>/dev/null; then
    echo "  ✅ Package imports successfully"
else
    echo "  ❌ Package import failed"
    exit 1
fi

echo ""
echo "✅ All validation checks passed!"
echo "🚀 Ready for development"
```

---

## 5. Customization

### 5.1 Customize Generated Files

**After generation**, you can customize any generated files:

**Common Customizations**:
1. **README.md**: Add project-specific features, installation, usage
2. **ROADMAP.md**: Add your project roadmap
3. **src/{package}/mcp/server.py**: Implement your MCP server logic
4. **tests/**: Add your test cases
5. **.github/workflows/**: Customize CI/CD workflows

**Best Practice**: Track customizations in CHANGELOG.md for upgrade clarity

### 5.2 Customize Before Generation

**Option 1: Modify Blueprints** (affects all future generations):
```bash
# Edit blueprint
vim blueprints/README.md.blueprint

# Generate with modified blueprint
python setup.py my-project
```

**Option 2: Modify Static Template** (affects all future generations):
```bash
# Edit static file
vim static-template/scripts/dev-server.sh

# Generate with modified template
python setup.py my-project
```

**Option 3: Fork chora-base** (for major customizations):
```bash
# Fork chora-base on GitHub
git clone https://github.com/yourusername/chora-base-custom.git
cd chora-base-custom

# Make customizations
# ... edit blueprints, static-template ...

# Use your fork for generation
python setup.py my-project
```

### 5.3 Add New Blueprints

See [awareness-guide.md](awareness-guide.md) Section 3.3 for detailed instructions.

**Quick Steps**:
1. Create `blueprints/newfile.blueprint`
2. Add mapping to `setup.py:231-242`
3. Test generation

---

## 6. Upgrade Path

### 6.1 Check Current Template Version

**In generated project**:
```bash
# Check version in README.md
grep "chora-base" README.md

# Check initial commit message
git log --reverse --oneline | head -1
# Shows: "Initial commit from chora-base vX.Y.Z"
```

**In chora-base repository**:
```bash
# Check template version
grep "TEMPLATE_VERSION" setup.py
# Shows: TEMPLATE_VERSION = "3.3.0"
```

### 6.2 Upgrade Project to New Template Version

**Scenario**: Your project uses chora-base v3.0, want to upgrade to v3.3

**Steps**:

1. **Check upgrade blueprint exists**:
```bash
# In chora-base repo
ls docs/upgrades/
# Look for: v3.0-to-v3.3.md
```

2. **Read upgrade blueprint**:
```bash
cat docs/upgrades/v3.0-to-v3.3.md
# Follow instructions
```

3. **Typical upgrade process**:
```bash
# Backup your project
cp -r my-project my-project-backup

# Update specific files from new template
# (blueprint will specify which files)
cp chora-base/static-template/.github/workflows/test.yml my-project/.github/workflows/

# Re-run specific blueprints (if needed)
# (blueprint will provide instructions)

# Test project
cd my-project
pytest

# Update version tracking
# Edit README.md, add note about upgrade to v3.3
```

4. **Commit upgrade**:
```bash
git add .
git commit -m "chore: Upgrade to chora-base v3.3.0"
```

**Upgrade Frequency**: Check for template updates quarterly or when needed

---

## 7. Best Practices

### For Initial Generation

1. **Prepare variables beforehand** - Know your project name, description, author info
2. **Use defaults** - Accept derived values (slug, package name) unless you have specific needs
3. **Validate immediately** - Run validation checks right after generation
4. **Test early** - Run pytest to ensure tests pass
5. **Commit often** - Commit generated project immediately, then commit customizations separately

### For Customization

1. **Track customizations** - Document changes in CHANGELOG.md
2. **Separate commits** - Commit template changes separately from customizations
3. **Consider contributing** - If customization is generally useful, consider contributing back to chora-base
4. **Test thoroughly** - Re-run tests after customizations
5. **Update docs** - Update README.md to reflect customizations

### For Upgrades

1. **Read upgrade blueprint** - Don't guess, follow documented upgrade path
2. **Backup first** - Always backup project before upgrading
3. **Test after upgrade** - Run full test suite after upgrade
4. **Review changes** - Use `git diff` to review what changed
5. **Document upgrade** - Note template version upgrade in CHANGELOG.md

---

## 8. Troubleshooting

### Problem: setup.py not found

**Symptom**:
```
python: can't open file 'setup.py': [Errno 2] No such file or directory
```

**Solution**:
- Ensure you're in chora-base root directory:
```bash
cd /path/to/chora-base
ls setup.py  # Should exist
```

### Problem: static-template/ not found

**Symptom**:
```
Error: static-template/ not found at /path/to/chora-base/static-template
```

**Solution**:
- Ensure chora-base repository is complete:
```bash
ls static-template/  # Should show directories
git pull  # Update to latest
```

### Problem: Unreplaced placeholders

**Symptom**:
```
⚠ Unreplaced placeholders in pyproject.toml
```

**Solution**:
- Check which variable is unreplaced:
```bash
grep "{{" pyproject.toml
```
- Re-run generation with correct variable values
- If variable is missing from setup.py, file issue or add custom variable

### Problem: Tests not loadable

**Symptom**:
```
pytest --collect-only
ERROR: file not found: tests
```

**Solution**:
- Check tests directory exists:
```bash
ls -la tests/
```
- Check pytest configuration:
```bash
cat pyproject.toml | grep -A5 "\[tool.pytest"
```
- Verify static-template was copied correctly:
```bash
find . -name "conftest.py"
```

### Problem: Package import fails

**Symptom**:
```
ImportError: No module named 'mcp_github'
```

**Solution**:
- Check package directory exists:
```bash
ls src/mcp_github/__init__.py
```
- Check __package_name__ was renamed:
```bash
find . -name "__package_name__"  # Should be empty
```
- Install package in development mode:
```bash
pip install -e .
```

### Problem: Git initialization fails

**Symptom**:
```
Error: git not found
```

**Solution**:
- Install git:
```bash
# macOS
brew install git

# Linux
sudo apt-get install git

# Verify
git --version
```

### Problem: Generation times out

**Symptom**:
- Generation hangs for > 90 seconds

**Solution**:
- Check static-template size (should be < 10MB)
- Check target directory is local (not network drive)
- Check disk space:
```bash
df -h .
```
- Try smaller test generation first:
```bash
python setup.py test-quick
```

---

## 9. Next Steps

### After Successful Generation

**Immediate Tasks**:
1. ✅ Validate generation (Section 4)
2. ✅ Install dependencies (`pip install -e ".[dev]"`)
3. ✅ Run tests (`pytest`)
4. ✅ Commit to version control (`git push`)

**Development Tasks**:
1. Implement MCP server logic (src/{package}/mcp/server.py)
2. Write tests (tests/)
3. Update documentation (README.md, docs/)
4. Configure CI/CD (.github/workflows/)

**Learn More**:
1. Read [AGENTS.md](/AGENTS.md) - Agent guidance for development
2. Read [SAP-004 (testing-framework)](../testing-framework/) - Testing patterns
3. Read [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - CI/CD setup
4. Read [SAP-006 (quality-gates)](../quality-gates/) - Quality standards

---

## 10. Related Documents

**SAP-003 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [ledger.md](ledger.md) - Adopter tracking

**Generation Components**:
- [setup.py](/setup.py) - Generation orchestrator (443 lines)
- [blueprints/](/blueprints/) - Variable templates (12 files)
- [static-template/](/static-template/) - Project scaffold (100+ files)

**Related SAPs**:
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP Section 3.2.1
- [testing-framework/](../testing-framework/) - SAP-004 (next in dependency chain)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (depends on testing)
- [quality-gates/](../quality-gates/) - SAP-006 (depends on testing)

**Core Docs**:
- [README.md](/README.md) - Project overview
- [AGENTS.md](/AGENTS.md) - Agent guidance
- [CHANGELOG.md](/CHANGELOG.md) - Version history

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint for project-bootstrap
