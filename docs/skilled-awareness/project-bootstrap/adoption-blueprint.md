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

**Time Estimate**: 5-10 minutes (agent-assisted), 10-20 minutes (human)

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

## 3. Generation Workflow

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

**Auto-Derived** (setup.py will calculate):
- **Project Slug**: Kebab-case (e.g., "mcp-github" from "MCP GitHub")
- **Package Name**: Snake_case (e.g., "mcp_github" from "mcp-github")
- **MCP Namespace**: No separators (e.g., "mcpgithub" from "mcp_github")

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

### Step 3: Run Generation

**For Humans** (interactive):
```bash
# Historical Note: setup.py removed in Wave 3 Phase 5
# Follow interactive prompts
```

**For Agents** (programmatic):
```python
# Prepare variables dict
variables = {
    "project_name": "MCP GitHub",
    "project_slug": "mcp-github",
    "package_name": "mcp_github",
    "mcp_namespace": "mcpgithub",
    "project_description": "GitHub operations via MCP",
    "author_name": "Alice Smith",
    "author_email": "alice@example.com",
    "github_username": "alice-smith",
    "python_version": "3.11",
    "project_version": "0.1.0",
    "license": "MIT",
}

# Run setup.py with variables (interactive prompts use these defaults)
# Historical Note: setup.py removed in Wave 3 Phase 5
```

**Output** (expected):
```
============================================================
Chora-Base v3.3.0 Setup
============================================================

Project Configuration
------------------------------------------------------------
Project name: MCP GitHub
Derived values:
  Project slug: mcp-github
  Package name: mcp_github
  MCP namespace: mcpgithub

Use these derived values? [Y/n]: y
Project description: GitHub operations via MCP
Author name [Alice Smith]:
Author email [alice@example.com]:
GitHub username [alice-smith]:
Python version [3.11]:
Initial version [0.1.0]:
License [MIT]:

Summary:
------------------------------------------------------------
  [Shows all variables]

Proceed with setup? [Y/n]: y

============================================================
Setting up project...
============================================================

Copying static template to my-new-project...
✓ Copied static template

Renaming src/__package_name__/ → src/mcp_github/
✓ Renamed package directories

Processing blueprints...
  ✓ pyproject.toml
  ✓ README.md
  ✓ AGENTS.md
  ✓ CHANGELOG.md
  ✓ ROADMAP.md
  ✓ .gitignore
  ✓ .env.example
  ✓ src/mcp_github/__init__.py
  ✓ src/mcp_github/mcp/server.py
  ✓ src/mcp_github/mcp/__init__.py
✓ Processed blueprints

Initializing git repository...
✓ Initialized git repository

Validating setup...
  ✓ pyproject.toml
  ✓ README.md
  ✓ AGENTS.md
  ✓ src/mcp_github/__init__.py
  ✓ src/mcp_github/mcp/server.py
  ✓ src/mcp_github/memory/event_log.py
  ✓ src/mcp_github/utils/validation.py

✅ Validation passed!

============================================================
✅ Setup complete!
============================================================

Project: MCP GitHub
Location: /path/to/my-new-project

Next steps:
  1. cd my-new-project
  2. Run tests: pytest
  3. Start dev server: ./scripts/dev-server.sh
  4. Implement your MCP server in src/mcp_github/mcp/server.py
```

**Time**: 30-60 seconds (agent), 2-5 minutes (human with prompts)

### Step 4: Validate Generated Project

**Change to project directory**:
```bash
cd my-new-project
```

**Run validation checks**:

1. **Check critical files exist**:
```bash
ls pyproject.toml README.md AGENTS.md src/mcp_github/__init__.py
# Expected: All files listed (no errors)
```

2. **Check for unreplaced placeholders**:
```bash
grep -r "{{" . --exclude-dir=.git --exclude-dir=__pycache__
# Expected: No output (no unreplaced placeholders)
```

3. **Check tests are loadable**:
```bash
pytest --collect-only
# Expected: X tests collected (no errors)
```

4. **Check git initialized**:
```bash
git log --oneline
# Expected: 1 commit "Initial commit from chora-base v3.3.0"
```

5. **Check Python files valid**:
```bash
python -c "import sys; sys.path.insert(0, 'src'); import mcp_github; print('✅ Package imports')"
# Expected: ✅ Package imports
```

**All checks pass**: ✅ Generation successful, proceed to development

**Any check fails**: See Section 8 (Troubleshooting)

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
