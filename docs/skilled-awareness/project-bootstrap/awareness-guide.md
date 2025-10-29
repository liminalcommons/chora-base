# Awareness Guide: Project Bootstrap

**SAP ID**: SAP-003
**Version**: 1.0.0
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

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
2. Study: [setup.py](../../../../setup.py) - Generation logic (443 lines)
3. Check: [blueprints/](../../../../blueprints/) - Variable templates (12 files)

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
2. [setup.py](../../../../setup.py) (1.5k tokens) - Implementation (functions only, skip prompts)
3. Blueprint variables (Section 3.1 in Protocol) - Variable list

**For troubleshooting generation**:
1. [protocol-spec.md](protocol-spec.md) Section 7 (1k tokens) - Error handling
2. [adoption-blueprint.md](adoption-blueprint.md) Section 8 (1k tokens) - Troubleshooting
3. Validation logic (setup.py:318-358) - Validation checks

**For extending generation**:
1. [protocol-spec.md](protocol-spec.md) Section 8.1 (1k tokens) - Maintainability
2. [setup.py](../../../../setup.py) full read (1.5k tokens) - Implementation details
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

## 5. Best Practices

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

## 8. Related Resources

**SAP-003 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - Technical contract
- [adoption-blueprint.md](adoption-blueprint.md) - How to generate projects
- [ledger.md](ledger.md) - Adopter tracking

**Generation Components**:
- [setup.py](../../../../setup.py) - Generation orchestrator (443 lines)
- [blueprints/](../../../../blueprints/) - Variable templates (12 files)
- [static-template/](../../../../static-template/) - Project scaffold (100+ files)

**Related SAPs**:
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP Section 3.2.1
- [testing-framework/](../testing-framework/) - SAP-004 (generated test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (generated workflows)
- [quality-gates/](../quality-gates/) - SAP-006 (generated quality configs)

**Core Docs**:
- [README.md](../../../../README.md) - Project overview
- [AGENTS.md](../../../../AGENTS.md) - Agent guidance
- [CHANGELOG.md](../../../../CHANGELOG.md) - Version history

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide for project-bootstrap
