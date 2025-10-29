# Awareness Guide: Project Bootstrap

**SAP ID**: SAP-003
**Version**: 1.0.1
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

### When to Use This SAP

**Use the Project Bootstrap SAP when**:
- Generating a new Python project from chora-base template
- Understanding the project generation workflow (setup.py + blueprints)
- Customizing project generation with optional flags (--no-docker, --no-memory, --no-claude)
- Validating a generated project structure
- Adopting chora-base patterns in existing projects

**Don't use for**:
- Non-Python projects (chora-base is Python-specific)
- Minimal/simple projects (chora-base is comprehensive, production-ready)
- Projects that don't need AI agent support or structured workflows
- Manual project setup without generation (use static-template/ directly instead)

### Common Agent Tasks

**Generate new project**:
```bash
python setup.py <target-directory>
```

**Validate generated project**:
```bash
cd <target-directory>
pytest --collect-only  # Check tests loadable
pytest                 # Run tests
```

**Understand generation system**:
1. Read: [protocol-spec.md](protocol-spec.md) - Complete technical contract
2. Study: [setup.py](/setup.py) - Generation logic (443 lines)
3. Check: [blueprints/](/blueprints/) - Variable templates (12 files)

### Quick Commands

**Test generation**:
```bash
python setup.py test-project
cd test-project && pytest --collect-only
```

**Check blueprint variables**:
```bash
grep -r "{{" blueprints/
```

**Find static template files**:
```bash
find static-template/ -type f | wc -l  # Count files
ls -la static-template/                # List top-level
```

---

## 2. Agent Context Loading

### Essential Context (3-5k tokens)

**For generating projects**:
1. [protocol-spec.md](protocol-spec.md) (6k tokens) - Generation flow, contracts
2. [setup.py](/setup.py) (1.5k tokens) - Implementation (functions only, skip prompts)
3. Blueprint variables (Section 3.1 in Protocol) - Variable list

**For troubleshooting generation**:
1. [protocol-spec.md](protocol-spec.md) Section 7 (1k tokens) - Error handling
2. [adoption-blueprint.md](adoption-blueprint.md) Section 8 (1k tokens) - Troubleshooting
3. Validation logic (setup.py:318-358) - Validation checks

**For extending generation**:
1. [protocol-spec.md](protocol-spec.md) Section 8.1 (1k tokens) - Maintainability
2. [setup.py](/setup.py) full read (1.5k tokens) - Implementation details
3. Example blueprint (blueprints/pyproject.toml.blueprint) - Blueprint syntax

### What to Skip

- ❌ Static template file contents (100+ files) - Only read when needed
- ❌ Generated project files - Focus on template, not output
- ❌ Interactive prompt logic (setup.py:89-186) - Agents use direct variable dict

---

## 3. Common Workflows

### 3.1 Generate New Project

**Context**: 5k tokens (Protocol + setup.py)

**Steps**:
1. **Prepare Variables**:
   ```python
   variables = {
       "project_name": "My MCP Server",
       "project_slug": "my-mcp-server",      # Derived from project_name
       "package_name": "my_mcp_server",      # Derived from project_slug
       "mcp_namespace": "mymcpserver",       # Derived from package_name
       "project_description": "One-line description",
       "author_name": "Your Name",
       "author_email": "email@example.com",
       "github_username": "yourusername",
       "python_version": "3.11",
       "project_version": "0.1.0",
       "license": "MIT",
       # Auto-derived (setup.py will add these)
       "python_version_nodots": "311",
       "test_coverage_threshold": "85",
       "template_version": "3.3.0",
       "generation_date": "2025-10-28",
       "generation_timestamp": "2025-10-28T12:00:00Z",
   }
   ```

2. **Run Generation**:
   ```bash
   python setup.py my-mcp-server
   # Follow prompts with prepared variables
   ```

3. **Validate Generation**:
   ```bash
   cd my-mcp-server
   pytest --collect-only  # Should show tests loadable
   ls -la src/my_mcp_server/  # Package directory exists
   grep -r "{{" .  # No unreplaced placeholders
   ```

4. **Success Criteria**:
   - All critical files exist (pyproject.toml, README.md, src/{package}/)
   - No {{ placeholders }} in key files
   - pytest --collect-only succeeds
   - Git repository initialized

**Time**: 30-60 seconds (with Claude optimizations)

### 3.2 Troubleshoot Generation Failure

**Context**: 3-5k tokens (Protocol Section 7 + validation logic)

**Scenario 1: Unreplaced Placeholders**

**Symptom**:
```
⚠ Unreplaced placeholders in pyproject.toml
```

**Steps**:
1. Check which variable is unreplaced:
   ```bash
   grep "{{" pyproject.toml
   # Output: name = "{{ project_slug }}"
   ```

2. Verify variable was passed to process_blueprints():
   ```python
   # In setup.py, check variables dict includes project_slug
   if "project_slug" not in variables:
       print("Missing project_slug!")
   ```

3. Check blueprint mapping exists:
   ```python
   # setup.py:231-242
   blueprint_mappings = {
       'pyproject.toml.blueprint': 'pyproject.toml',  # Should exist
   }
   ```

4. Re-run generation with correct variables

**Scenario 2: Missing Files**

**Symptom**:
```
✗ Missing: src/my_project/__init__.py
```

**Steps**:
1. Check static-template has file:
   ```bash
   ls static-template/src/__package_name__/__init__.py
   # Should exist
   ```

2. Check rename_package_directories ran:
   ```bash
   ls my-project/src/
   # Should show my_project/, not __package_name__/
   ```

3. Check copy_static_template succeeded:
   ```bash
   find my-project/ -type f | wc -l
   # Should match static-template file count
   ```

4. Re-run generation, watch for errors in each step

**Scenario 3: Generation Times Out**

**Symptom**:
- Generation takes > 90 seconds
- Hangs at "Copying static template"

**Steps**:
1. Check static-template size:
   ```bash
   du -sh static-template/
   # Should be < 10MB
   ```

2. Check target directory is local (not network drive)

3. Parallelize where possible:
   - Read blueprints while copying static-template
   - Check git config while processing blueprints

### 3.3 Extend Generation System

**Context**: 8-12k tokens (Protocol + setup.py full + example blueprint)

**Add New Blueprint**:

1. **Create Blueprint File**:
   ```bash
   # blueprints/newfile.md.blueprint
   # Project: {{ project_name }}

   This is a new file with {{ package_name }}.
   ```

2. **Add Mapping**:
   ```python
   # setup.py:231-242
   blueprint_mappings = {
       # ... existing mappings ...
       'newfile.md.blueprint': 'NEWFILE.md',
   }
   ```

3. **Test Generation**:
   ```bash
   python setup.py test-new-blueprint
   cd test-new-blueprint
   cat NEWFILE.md  # Should have substituted variables
   ```

4. **Update SAP-003 Protocol**:
   - Add to Section 3.3 (Blueprint Mappings)
   - Add to Section 6.1 (Guarantees) if critical file
   - Update Section 12 (Version History)

**Add New Variable**:

1. **Add to gather_variables()**:
   ```python
   # setup.py:89-186
   def gather_variables() -> Dict[str, str]:
       # ... existing prompts ...
       variables['new_variable'] = input("New variable: ").strip()
       return variables
   ```

2. **Document Variable**:
   ```python
   # Protocol Section 3.1
   "new_variable": str,  # Description
   ```

3. **Use in Blueprints**:
   ```
   # Any blueprint file
   New value: {{ new_variable }}
   ```

4. **Test**:
   ```bash
   python setup.py test-new-variable
   grep "new_variable" test-new-variable/*
   # Should show substituted value, not {{ new_variable }}
   ```

---

## 4. Integration Patterns

### 4.1 With Project Generation

**Pattern**: Agent orchestrates setup.py

```
User: "Generate an MCP server for GitHub operations"

Agent:
  1. Load: SAP-003 Protocol (generation workflow)
  2. Prepare variables:
     project_name = "MCP GitHub"
     project_slug = "mcp-github"  # Derived
     package_name = "mcp_github"  # Derived
     description = "GitHub operations via MCP"
     author = git config user.name
     email = git config user.email
  3. Run: python setup.py mcp-github (with variables)
  4. Validate: pytest --collect-only
  5. Report: "✅ Generated mcp-github (85 tests loadable)"
```

### 4.2 With Testing Framework

**Pattern**: Generated tests match SAP-004

```
Generation creates:
  - tests/conftest.py (pytest configuration)
  - tests/test_mcp_server.py (example tests)
  - tests/utils/test_*.py (utility tests)

SAP-004 (testing-framework) defines:
  - Test structure (conftest patterns)
  - Coverage thresholds (85%)
  - Pytest plugins (pytest-asyncio, pytest-cov)

Agent validates:
  - Generated tests match SAP-004 structure
  - Coverage config matches SAP-004 (85%)
  - Pytest plugins match SAP-004
```

### 4.3 With CI/CD Workflows

**Pattern**: Generated workflows match SAP-005

```
Generation creates:
  - .github/workflows/test.yml (pytest + coverage)
  - .github/workflows/quality.yml (ruff, mypy)
  - .github/workflows/build.yml (build + publish)

SAP-005 (ci-cd-workflows) defines:
  - Workflow structure (test matrix, caching)
  - Quality gates (coverage 85%, type checks)
  - Build process (hatchling, PyPI)

Agent validates:
  - Generated workflows match SAP-005 structure
  - Quality gates match SAP-005 thresholds
  - Build process matches SAP-005
```

---

## 5. Common Pitfalls

### Pitfall 1: Not Reading Capability Charter Before Generating

**Scenario**: Agent generates project without understanding what project-bootstrap provides.

**Example**:
```bash
# Agent immediately runs:
python setup.py my-project

# Without reading SAP-003 Charter to understand:
# - What gets generated (100+ files)
# - What capabilities are included (testing, CI/CD, memory, docker)
# - What optional flags exist (--no-docker, --no-memory)
```

**Fix**: Always read Charter first to understand scope:
```bash
# Read: docs/skilled-awareness/project-bootstrap/capability-charter.md
# Then generate with informed choices:
python setup.py my-project --no-docker  # Skip docker if not needed
```

**Why it matters**: Generating unnecessary components (docker, memory) adds complexity. Understanding optional flags saves cleanup time. Charter reading takes 3-5 minutes, cleanup takes 30-60 minutes.

### Pitfall 2: Skipping Validation After Generation

**Scenario**: Agent generates project, reports success, but doesn't validate structure.

**Example**:
```bash
python setup.py my-project
# Output: "✅ Project generation complete!"

# Agent reports success to user WITHOUT running:
cd my-project
pytest --collect-only  # Tests loadable?
grep -r "{{"          # Placeholders replaced?
ls src/my_package/    # Package directory exists?
```

**Fix**: Always run 5-step validation (Protocol Section 6.1):
```bash
# Step 1: Critical files exist
ls pyproject.toml README.md src/my_package/__init__.py

# Step 2: No unreplaced placeholders
grep -r "{{" . --exclude-dir=.git

# Step 3: Tests loadable
pytest --collect-only

# Step 4: Git initialized
git log --oneline

# Step 5: Python files compile
python -m py_compile src/my_package/__init__.py
```

**Why it matters**: Silent failures waste user time. Unreplaced placeholders break imports. Validation takes 10-15 seconds, debugging later takes 10-30 minutes.

### Pitfall 3: Overwriting Project Without --force Flag Understanding

**Scenario**: Agent tries to regenerate project in existing directory.

**Example**:
```bash
# First generation
python setup.py my-project
# Success!

# Later, user asks to "regenerate with new settings"
python setup.py my-project  # ERROR: Directory exists!

# setup.py checks target_dir.exists() and blocks overwrite
# Agent doesn't understand why generation failed
```

**Fix**: Understand --force flag and use cautiously:
```bash
# Check if directory exists first
if [ -d "my-project" ]; then
    # Ask user confirmation before --force
    echo "Project exists. Overwrite? This will DELETE all changes."
    # If confirmed:
    python setup.py my-project --force  # Removes existing directory
fi
```

**Why it matters**: --force DELETES the entire directory, losing user changes. Protocol Section 2.2.1 documents this behavior. Always confirm with user before destructive operations.

### Pitfall 4: Not Checking for Unreplaced Placeholders in Non-Critical Files

**Scenario**: Validation passes for critical files, but placeholders remain in documentation.

**Example**:
```bash
# Agent runs validation
ls pyproject.toml  # ✅ Exists
pytest --collect-only  # ✅ Tests loadable

# But doesn't check docs:
cat docs/development.md
# Shows: "See {{ project_slug }} repository"
# Placeholder not replaced! User sees broken docs.
```

**Fix**: Check ALL files for placeholders, not just critical ones:
```bash
# Comprehensive check (excludes .git)
grep -r "{{" . --exclude-dir=.git

# If found, investigate which blueprint mapping is missing
# setup.py:231-242 should map all blueprints:
blueprint_mappings = {
    'docs/development.md.blueprint': 'docs/development.md',  # Must exist
}
```

**Why it matters**: Documentation with {{ placeholders }} looks broken to users. Protocol Section 3.3 lists all 12 blueprint mappings. Checking all files takes 1-2 seconds, fixing docs later takes 5-10 minutes.

### Pitfall 5: Forgetting setup.py vs static-template/ Distinction

**Scenario**: Agent modifies static-template/ when they should modify blueprints/.

**Example**:
```python
# Agent wants to change pyproject.toml for generated projects
# WRONG: Edits static-template/pyproject.toml
static-template/pyproject.toml:
    name = "my-package"  # Hardcoded!

# Generated projects all get "my-package", not {{ project_slug }}
```

**Fix**: Understand two-tier system (Protocol Section 3):
```bash
# static-template/: Static files (copied as-is)
# blueprints/: Variable templates ({{ }} replaced)

# For variable content, use blueprints:
blueprints/pyproject.toml.blueprint:
    name = "{{ project_slug }}"  # Will be replaced

# For static content, use static-template:
static-template/tests/conftest.py  # No variables, copy as-is
```

**Why it matters**: Modifying static-template/ for variable content breaks all future generations. Understanding the distinction prevents this. Protocol Section 3.2 documents blueprint processing, Section 3.4 documents static template copying.

---

## 6. Best Practices

### DO

- ✅ Read SAP-003 Protocol before generating (understand contracts)
- ✅ Validate after generation (pytest --collect-only)
- ✅ Check for unreplaced placeholders (grep "{{")
- ✅ Use derived variables (project_slug from project_name)
- ✅ Test generation with edge cases (special characters, long names)

### DON'T

- ❌ Generate without understanding contracts (read Protocol first)
- ❌ Skip validation (always run pytest --collect-only)
- ❌ Modify static-template directly (use blueprints for variable content)
- ❌ Assume placeholders replaced (always validate)
- ❌ Forget to initialize git (setup.py does this, but verify)

---

## 6. Claude-Specific Optimizations

### Context Management

**Load Order** (progressive):
1. Protocol Section 2 (3k) → Understand generation flow
2. setup.py functions (1k) → Understand implementation
3. Blueprint list (1k) → Know what gets generated

**Token Budget**:
- Essential: 3-5k (Protocol flow + setup.py functions)
- Extended: 8-10k (+ error handling + validation)
- Full: 12-15k (+ example blueprints + static-template overview)

### Parallel Operations

**During Generation**:
```
Parallel:
  - Read all blueprints (blueprints/*.blueprint)
  - Check git config (user.name, user.email)
  - Prepare target directory (mkdir -p)

Sequential:
  - Copy static-template (depends on target dir exists)
  - Rename directories (depends on copy complete)
  - Process blueprints (depends on copy complete)
  - Initialize git (depends on all files ready)
  - Validate (depends on git complete)
```

**Result**: 30-60 second generation (vs 60-90s sequential)

### Error Recovery

**Validation Failures**:
```
If validation fails:
  1. Report specific failure (missing file, unreplaced placeholder)
  2. Suggest recovery steps (from Protocol Section 7)
  3. Offer to re-run specific step:
     - Re-run process_blueprints() for placeholder issues
     - Re-run rename_package_directories() for missing package dir
     - Re-run copy_static_template() for missing files
```

---

## 7. Troubleshooting Reference

### Quick Diagnostics

**Check Generation Success**:
```bash
# 1. Critical files exist?
ls pyproject.toml README.md src/my_package/__init__.py

# 2. No placeholders?
grep -r "{{" . --exclude-dir=.git

# 3. Tests loadable?
pytest --collect-only

# 4. Git initialized?
git log --oneline

# 5. Python valid?
python -m py_compile src/my_package/__init__.py
```

**Expected Output**:
```
✅ All critical files exist
✅ No unreplaced placeholders
✅ Tests loadable (pytest shows X tests collected)
✅ Git history (1+ commits)
✅ Python files compile
```

### Common Issues

| Symptom | Cause | Recovery |
|---------|-------|----------|
| Missing files | copy_static_template failed | Re-run from chora-base root |
| Unreplaced {{ }} | Variable not in dict | Add variable to gather_variables() |
| Package dir wrong | rename_package_directories failed | Check __package_name__ → package_name |
| Tests not found | pytest config wrong | Check pyproject.toml [tool.pytest.ini_options] |
| Git error | Git not installed | Install git, re-run initialize_git() |

---

## 8. Related Content

### Within This SAP (skilled-awareness/project-bootstrap/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-003
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (generation flow, validation)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for generating projects
- [ledger.md](ledger.md) - Adopter tracking, version history, generation metrics
- **This document** (awareness-guide.md) - Agent workflows and optimizations

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/TDD_WORKFLOW.md](../../dev-docs/workflows/TDD_WORKFLOW.md) - Test-driven development in generated projects
- [dev-docs/workflows/BDD_WORKFLOW.md](../../dev-docs/workflows/BDD_WORKFLOW.md) - Behavior-driven development approach

**Tools**:
- [dev-docs/tools/ruff.md](../../dev-docs/tools/ruff.md) - Linting (generated projects use ruff)
- [dev-docs/tools/mypy.md](../../dev-docs/tools/mypy.md) - Type checking (generated projects use mypy)

**Development Guidelines**:
- [dev-docs/development/code-style.md](../../dev-docs/development/code-style.md) - Coding standards for generated projects

### Project Lifecycle (project-docs/)

**Generation & Setup**:
- [project-docs/guides/project-generation.md](../../project-docs/guides/project-generation.md) - Comprehensive project generation guide
- [project-docs/guides/environment-setup.md](../../project-docs/guides/environment-setup.md) - Setting up development environment

**Implementation Components**:
- [setup.py](/setup.py) - Generation orchestrator (443 lines)
- [blueprints/](/blueprints/) - Variable templates (12 .blueprint files)
- [static-template/](/static-template/) - Project scaffold (100+ files)

**Audits & Releases**:
- [project-docs/audits/](../../project-docs/audits/) - SAP audits including SAP-003 validation
- [project-docs/sprints/](../../project-docs/sprints/) - Sprint planning for SAP updates
- [project-docs/releases/](../../project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/quickstart.md](../../user-docs/guides/quickstart.md) - Quick start with project generation
- [user-docs/guides/installation.md](../../user-docs/guides/installation.md) - Installing chora-base

**Tutorials**:
- [user-docs/tutorials/first-mcp-server.md](../../user-docs/tutorials/first-mcp-server.md) - Build your first MCP server (uses SAP-003 generation)
- [user-docs/tutorials/customizing-template.md](../../user-docs/tutorials/customizing-template.md) - Customize generated projects

**Reference**:
- [user-docs/reference/cli-reference.md](../../user-docs/reference/cli-reference.md) - setup.py CLI reference
- [user-docs/reference/project-structure.md](../../user-docs/reference/project-structure.md) - Generated project structure explained

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.1 (documents SAP-003)

**Generated Capabilities**:
- [testing-framework/](../testing-framework/) - SAP-004 (generated test structure, pytest config)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (generated GitHub Actions workflows)
- [quality-gates/](../quality-gates/) - SAP-006 (generated pre-commit hooks, quality checks)
- [memory-system/](../memory-system/) - SAP-009 (optional memory capability)
- [docker-operations/](../docker-operations/) - SAP-010 (optional Docker support)

**Supporting Capabilities**:
- [automation-scripts/](../automation-scripts/) - SAP-008 (scripts for project tasks)
- [agent-awareness/](../agent-awareness/) - SAP-011 (AI agent guidance in generated projects)
- [metrics-tracking/](../metrics-tracking/) - SAP-013 (usage metrics in generated projects)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Agent guidance for using chora-base
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-003 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **1.0.1** (2025-10-28): Added "Common Pitfalls" section with Wave 2 learnings (5 scenarios: Charter reading, validation, --force flag, placeholder checking, setup.py vs static-template), enhanced "Related Content" with 4-domain coverage (dev-docs/, project-docs/, user-docs/, skilled-awareness/)
- **1.0.0** (2025-10-28): Initial awareness guide for project-bootstrap
