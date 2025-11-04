# Protocol Specification: Project Bootstrap

**SAP ID**: SAP-003
**Version**: 1.1.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-11-04

---

## 1. Overview

### Purpose

The project-bootstrap capability provides **zero-dependency Python project generation** using a blueprint-based templating system. It orchestrates copying static-template files, renaming package directories, processing variable substitution, and initializing git repositories.

### Design Principles

1. **Zero Dependencies** - Uses only Python stdlib (no Copier, Cookiecutter, Jinja2)
2. **Blueprint-Based** - Simple {{ var }} substitution (human and machine readable)
3. **Explicit Contracts** - Documents all guarantees about generated projects
4. **Validation-First** - Validates generated projects before declaring success
5. **Agent-Optimized** - Designed for AI agent execution (20-40 second generation)

---

## 2. System Architecture

### 2.1 Component Overview

```
chora-base/
├── setup.py                    # Generation orchestrator (443 lines)
├── blueprints/                 # Variable substitution templates (12 files)
│   ├── pyproject.toml.blueprint
│   ├── README.md.blueprint
│   ├── AGENTS.md.blueprint
│   ├── CHANGELOG.md.blueprint
│   ├── ROADMAP.md.blueprint
│   ├── CLAUDE.md.blueprint
│   ├── .gitignore.blueprint
│   ├── .env.example.blueprint
│   ├── package__init__.py.blueprint
│   ├── server.py.blueprint
│   └── mcp__init__.py.blueprint
└── static-template/            # Complete project scaffold (100+ files)
    ├── src/__package_name__/   # Package directory (to be renamed)
    ├── tests/                  # Test suite
    ├── scripts/                # Development scripts (20 files)
    ├── docker/                 # Docker configs
    ├── .github/workflows/      # GitHub Actions (10 workflows)
    ├── docs/                   # Documentation structure
    └── [100+ other files]
```

### 2.2 Generation Flow

```
User/Agent
    │
    ├─► python setup.py <target-dir>
    │
    v
[setup.py: gather_variables()]
    │
    ├─► Prompt for project_name, author_name, author_email
    ├─► Derive project_slug, package_name, mcp_namespace
    ├─► Validate inputs (email format, slug format, semver)
    │
    v
[setup.py: copy_static_template()]
    │
    ├─► shutil.copytree(static-template/, target-dir/)
    ├─► Copy 100+ files preserving structure
    │
    v
[setup.py: rename_package_directories()]
    │
    ├─► Find all __package_name__ directories
    ├─► Rename to actual package_name
    │   (e.g., src/__package_name__/ → src/my_project/)
    │
    v
[setup.py: process_blueprints()]
    │
    ├─► Read each blueprint file
    ├─► Replace {{ var }} with actual values
    ├─► Handle filters ({{ var | upper }})
    ├─► Write to target path
    ├─► Check for unreplaced placeholders
    │
    v
[setup.py: initialize_git()]
    │
    ├─► git init (if .git doesn't exist)
    ├─► git add .
    ├─► git commit -m "Initial commit from chora-base vX.Y.Z"
    │
    v
[setup.py: validate_setup()]
    │
    ├─► Check critical files exist
    ├─► Check for unreplaced {{ placeholders }}
    ├─► Report validation results
    │
    v
Generated Project (ready for development)
```

---

## 3. Data Models

### 3.1 Blueprint Variables

Complete set of variables available in blueprints:

```python
variables = {
    # User-provided
    "project_name": str,              # Display name (e.g., "MCP GitHub")
    "project_slug": str,              # Kebab-case (e.g., "mcp-github")
    "package_name": str,              # Snake_case (e.g., "mcp_github")
    "mcp_namespace": str,             # No separators (e.g., "mcpgithub")
    "project_description": str,       # One-line description
    "author_name": str,               # Full name
    "author_email": str,              # Valid email (validated)
    "github_username": str,           # GitHub handle
    "python_version": str,            # X.Y format (e.g., "3.11")
    "project_version": str,           # Semver (e.g., "0.1.0")
    "license": str,                   # License type (e.g., "MIT")

    # Auto-derived
    "python_version_nodots": str,     # X.Y → XY (e.g., "311")
    "test_coverage_threshold": str,   # Default "85"
    "template_version": str,          # chora-base version (e.g., "3.3.0")
    "generation_date": str,           # YYYY-MM-DD
    "generation_timestamp": str,      # ISO8601
}
```

**Validation Rules**:
- `project_slug`: Must match `^[a-z][a-z0-9-]+$` (lowercase, hyphens)
- `package_name`: Must match `^[a-z][a-z0-9_]+$` (lowercase, underscores, valid Python identifier)
- `author_email`: Must match RFC 5322 email format
- `project_version`: Must match semver `^\d+\.\d+\.\d+$`
- `python_version`: Recommended "3.11" or later

### 3.2 Blueprint Syntax

**Variable Substitution**:
```
{{ variable_name }}           # Basic substitution
{{variable_name}}             # No spaces (also supported)
{{ variable_name | upper }}   # Filter: uppercase
{{variable_name | upper}}     # No spaces (also supported)
```

**Supported Filters**:
- `| upper` - Convert to uppercase

**Example Blueprint** (pyproject.toml.blueprint):
```toml
[project]
name = "{{ project_slug }}"
version = "{{ project_version }}"
description = "{{ project_description }}"
authors = [
    {name = "{{ author_name }}", email = "{{ author_email }}"}
]
requires-python = ">={{ python_version }}"
```

**Generated Output** (after substitution):
```toml
[project]
name = "mcp-github"
version = "0.1.0"
description = "GitHub operations via MCP"
authors = [
    {name = "Alice Smith", email = "alice@example.com"}
]
requires-python = ">=3.11"
```

### 3.3 Blueprint Mappings

Blueprint → Target path mappings (from setup.py:230-242):

```python
{
    'pyproject.toml.blueprint': 'pyproject.toml',
    'README.md.blueprint': 'README.md',
    'AGENTS.md.blueprint': 'AGENTS.md',
    'CHANGELOG.md.blueprint': 'CHANGELOG.md',
    'ROADMAP.md.blueprint': 'ROADMAP.md',
    '.gitignore.blueprint': '.gitignore',
    '.env.example.blueprint': '.env.example',
    'package__init__.py.blueprint': 'src/{package_name}/__init__.py',
    'server.py.blueprint': 'src/{package_name}/mcp/server.py',
    'mcp__init__.py.blueprint': 'src/{package_name}/mcp/__init__.py',
}
```

**Note**: `{package_name}` is substituted at mapping time, not in blueprint content.

---

## 4. Behavior Specification

### 4.1 Generation Workflow

**Input**:
- Target directory path (command line or prompt)
- Project configuration variables (prompted interactively)

**Process**:
1. **Gather Variables** (setup.py:89-186)
   - Prompt for project_name
   - Auto-derive slug, package_name, namespace
   - Prompt for author info (fallback to git config)
   - Validate all inputs
   - Derive additional variables (timestamp, template version)

2. **Copy Static Template** (setup.py:188-202)
   - Copy all files from static-template/ to target-dir/
   - Preserve directory structure
   - Preserve file permissions
   - No variable substitution yet (raw copy)

3. **Rename Package Directories** (setup.py:204-218)
   - Find all `__package_name__` directories (placeholder)
   - Rename to actual package_name
   - Example: `src/__package_name__/` → `src/my_project/`

4. **Process Blueprints** (setup.py:220-290)
   - For each blueprint file:
     - Read blueprint content
     - Replace {{ var }} with actual values
     - Handle | upper filter
     - Check for unreplaced placeholders (warn if found)
     - Write to target path
   - Total: 12 blueprints processed

5. **Initialize Git** (setup.py:292-316)
   - If .git exists: add files + commit
   - If .git doesn't exist: init + add + commit
   - Commit message includes template version and project name

6. **Validate Setup** (setup.py:318-358)
   - Check critical files exist (pyproject.toml, README.md, etc.)
   - Check for unreplaced {{ placeholders }} in key files
   - Report validation results (✅ or ⚠)
   - Return True if all checks pass

**Output**:
- Complete Python project with:
  - Valid pyproject.toml
  - Configured package structure
  - Tests ready to run
  - Git repository initialized
  - No unreplaced placeholders

**Guarantees** (see Section 5):
- All critical files exist
- No {{ placeholders }} in generated files
- Tests loadable (pytest --collect-only)
- Valid Python package (can be installed)
- Git history initialized

### 4.2 Variable Derivation

**project_slug from project_name**:
```python
slug = project_name.lower()
slug = slug.replace(' ', '-').replace('_', '-')
# Example: "MCP GitHub" → "mcp-github"
```

**package_name from project_slug**:
```python
package_name = project_slug.replace('-', '_')
# Example: "mcp-github" → "mcp_github"
```

**mcp_namespace from package_name**:
```python
mcp_namespace = package_name.replace('_', '')
# Example: "mcp_github" → "mcpgithub"
```

**Auto-derived variables**:
```python
python_version_nodots = python_version.replace('.', '')  # "3.11" → "311"
test_coverage_threshold = "85"  # Default
template_version = TEMPLATE_VERSION  # From setup.py constant
generation_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
generation_timestamp = datetime.now(timezone.utc).isoformat()
```

### 4.3 Validation Rules

**File Existence Checks** (setup.py:322-331):
```python
required_files = [
    'pyproject.toml',
    'README.md',
    'AGENTS.md',
    f'src/{package_name}/__init__.py',
    f'src/{package_name}/mcp/server.py',
    f'src/{package_name}/memory/event_log.py',
    f'src/{package_name}/utils/validation.py',
]
```

**Placeholder Checks** (setup.py:342-350):
```python
key_files = ['pyproject.toml', 'README.md', f'src/{package_name}/mcp/server.py']
for file in key_files:
    content = file.read_text()
    if "{{" in content:
        print(f"⚠ Unreplaced placeholders in {file}")
        all_good = False
```

---

## 5. Interface Contracts

### 5.1 CLI Interface

**Command**:
```bash
python setup.py [target_directory]
```

**Arguments**:
- `target_directory` (optional): Path to create project
  - If not provided, prompts interactively
  - Can be relative or absolute path
  - If exists and not empty, warns user

**Interactive Prompts**:
1. Project name (required)
2. Use derived values? [Y/n]
3. Project description (optional)
4. Author name (default: git config user.name)
5. Author email (default: git config user.email, validated)
6. GitHub username (default: derived from author name)
7. Python version (default: "3.11")
8. Initial version (default: "0.1.0", validated semver)
9. License (default: "MIT")

**Output**:
```
============================================================
Chora-Base v3.3.0 Setup
============================================================

Project Configuration
------------------------------------------------------------
[Interactive prompts...]

Summary:
------------------------------------------------------------
  [Variable summary...]

Proceed with setup? [Y/n]:

============================================================
Setting up project...
============================================================

Copying static template to target-dir...
✓ Copied static template

Renaming src/__package_name__/ → src/my_project/
✓ Renamed package directories

Processing blueprints...
  ✓ pyproject.toml
  ✓ README.md
  [... 10 more ...]
✓ Processed blueprints

Initializing git repository...
✓ Initialized git repository

Validating setup...
  ✓ pyproject.toml
  ✓ README.md
  [... more ...]

✅ Validation passed!

============================================================
✅ Setup complete!
============================================================

Project: My Project
Location: /path/to/target-dir

Next steps:
  1. cd target-dir
  2. Run tests: pytest
  3. Start dev server: ./scripts/dev-server.sh
  4. Implement your MCP server in src/my_project/mcp/server.py
```

**Exit Codes**:
- `0` - Success (validation passed)
- `1` - Failure (error during generation or validation)

### 5.2 Python API

**Direct Import** (for agents):
```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path("/path/to/chora-base")))
from setup import gather_variables, copy_static_template, rename_package_directories, process_blueprints, initialize_git, validate_setup

# Example agent workflow
target_dir = Path("my-new-project")
target_dir.mkdir(parents=True, exist_ok=True)

variables = {
    "project_name": "My Project",
    "project_slug": "my-project",
    "package_name": "my_project",
    # ... all other variables
}

copy_static_template(target_dir)
rename_package_directories(target_dir, variables['package_name'])
process_blueprints(target_dir, variables)
initialize_git(target_dir, variables)
success = validate_setup(target_dir, variables['package_name'])

if success:
    print("✅ Generation successful")
else:
    print("⚠ Validation found issues")
```

---

## 6. Guarantees

### 6.1 Generated Project Guarantees

When setup.py validation passes, the generated project **guarantees**:

1. **File Existence**:
   - ✅ `pyproject.toml` exists with valid TOML
   - ✅ `README.md` exists with project description
   - ✅ `AGENTS.md` exists with agent guidance
   - ✅ `src/{package_name}/__init__.py` exists
   - ✅ `src/{package_name}/mcp/server.py` exists
   - ✅ `src/{package_name}/memory/event_log.py` exists
   - ✅ `src/{package_name}/utils/validation.py` exists
   - ✅ All blueprint-generated files exist

2. **Variable Substitution**:
   - ✅ No unreplaced `{{ placeholders }}` in key files
   - ✅ All variables correctly substituted
   - ✅ Filters (| upper) correctly applied

3. **Python Validity**:
   - ✅ package_name is valid Python identifier
   - ✅ All .py files have valid syntax (can be imported)
   - ✅ pyproject.toml is valid TOML
   - ✅ Project can be installed with `pip install -e .`

4. **Test Validity**:
   - ✅ Tests are loadable (`pytest --collect-only`)
   - ✅ Test structure matches testing-framework SAP
   - ✅ Example tests pass (if any)

5. **Git Repository**:
   - ✅ .git directory initialized
   - ✅ Initial commit created
   - ✅ Commit message includes template version

6. **Directory Structure**:
   - ✅ src-layout (not flat layout)
   - ✅ Package directories renamed correctly
   - ✅ Static template structure preserved

### 6.2 Performance Guarantees

**Generation Time** (with Claude Code):
- Target: 20-40 seconds
- Baseline: 60-90 seconds (human with setup.py)
- Measured: setup.py start → validation complete

**Components**:
- Copy static template: ~5-10 seconds (100+ files)
- Rename directories: ~1-2 seconds
- Process blueprints: ~3-5 seconds (12 files)
- Initialize git: ~2-5 seconds
- Validation: ~2-5 seconds

**Optimization**: Claude can parallelize reading blueprints and git config checks.

### 6.3 Template Capability Propagation

**Added**: 2025-11-04 (v1.1.0)
**Reference Implementation**: GAP-003 Track 2

This section formalizes the pattern for extending chora-base capabilities to generated projects through template updates.

#### 6.3.1 Propagation Pattern

When a capability is implemented in chora-base and should be available to all generated projects, follow this protocol:

**Phase 1: Template Creation**
1. Identify the capability working in chora-base (e.g., release workflow, testing framework)
2. Create template versions with `.template` suffix
3. Add Jinja2 template variables (e.g., `{{ project_slug }}`, `{{ package_name }}`)
4. Update template infrastructure files:
   - `docker-compose.yml` - Version variables
   - `Dockerfile` - Metadata labels
   - `.github/workflows/*.yml` - CI/CD jobs
   - Configuration files - Environment variables

**Phase 2: Testing**
1. Create test data fixture in `test-data/{capability}-test.json`
2. Create integration test script: `scripts/test-{capability}-render.py`
3. Validate template rendering:
   - All variables substituted correctly
   - Syntax validation (Python: `py_compile`, etc.)
   - Output inspection in `.test_target/`
4. Document test results

**Phase 3: Documentation**
1. Update relevant SAP ledgers (version bumps)
2. Add capability section to ledgers documenting templates
3. Create completion summary (if part of GAP/initiative)
4. Update [workflow-continuity-gap-report.md](../../../docs/project-docs/workflow-continuity-gap-report.md) if closing a gap

#### 6.3.2 Template Variable Conventions

**Standard Variables** (always available):
```python
{
    "project_name": "Human-readable project name",
    "project_slug": "url-friendly-name",
    "package_name": "python_package_name",
    "project_version": "0.1.0",
    "project_description": "Project description",
    "author_name": "Author Name",
    "author_email": "author@example.com",
    "github_org": "organization",
    "python_version": "3.11",
    "python_version_nodots": "311",
    "license": "MIT"
}
```

**Capability-Specific Variables** (added as needed):
```python
{
    "docker_registry": "ghcr.io",
    "docker_org": "liminalcommons",
    "test_coverage_threshold": 85,
    "pypi_auth_method": "trusted_publishing",
    "include_memory_system": true
}
```

#### 6.3.3 Testing Protocol

**Template Rendering Test Structure**:
```python
# scripts/test-{capability}-render.py

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def test_template_rendering():
    # 1. Load test data
    data = json.load(open("test-data/{capability}-test.json"))

    # 2. Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('static-template/mcp-templates'))

    # 3. Render each template
    for template_name in templates:
        template = env.get_template(template_name)
        output = template.render(**data)

        # 4. Check for unsubstituted variables
        assert '{{' not in output or is_just_syntax(output)

        # 5. Validate syntax (language-specific)
        if template_name.endswith('.py.template'):
            py_compile.compile(output_file, doraise=True)

        # 6. Write to test_target for inspection
        output_file = Path('.test_target') / template_name.replace('.template', '')
        output_file.write_text(output, encoding='utf-8')
```

**Validation Checklist**:
- ✅ All templates render without Jinja2 errors
- ✅ No unsubstituted `{{ variables }}` (except language syntax)
- ✅ Syntax validation passes (Python, YAML, etc.)
- ✅ Output files match expected structure
- ✅ UTF-8 encoding handled correctly (Windows compatibility)

#### 6.3.4 SAP Update Pattern

When adding template support for a capability, update the owning SAP:

**Version Bump**:
- MINOR version bump (e.g., v1.2.0 → v1.3.0)
- Indicates new template support added

**Ledger Updates**:
1. Update frontmatter version and last_updated
2. Add new section: "X.X Template Support" or "X.X {Capability} Template Propagation"
3. Document template files created (names, lines, purpose)
4. List infrastructure files updated
5. Add integration test information
6. Document business impact and metrics
7. Update changelog and version history

**Example** (from SAP-008 v1.3.0):
```markdown
## 4.6 GAP-003 Track 2: Unified Release Workflow (Generated Projects)

**Date**: 2025-11-04
**Templates**: bump-version.py.template, create-release.py.template, justfile.template

**Template Scripts Created**:
| Template | Lines | Purpose |
|----------|-------|---------|
| bump-version.py.template | 400+ | Version management |
| create-release.py.template | 300+ | GitHub release automation |
| justfile.template | 200+ | Task runner integration |

**Integration Testing**: ✅ All tests passed
**Business Impact**: 50% time savings for all generated projects
```

#### 6.3.5 Capability Coverage Tracking

**Current Template Support** (as of v1.1.0):

| Capability (SAP) | Template Support | Test Coverage | Version Added |
|------------------|------------------|---------------|---------------|
| SAP-004: Testing Framework | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-005: CI/CD Workflows | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-006: Quality Gates | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-008: Automation Scripts | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-008: Release Workflow | ✅ Complete | 100% | v1.1.0 (GAP-003 Track 2) |
| SAP-011: Docker Operations | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-012: Development Lifecycle | ✅ Complete | 100% | v1.0.0 (initial) |
| SAP-030: Cross-Platform | ✅ Complete | 100% | v1.0.0 (initial) |

**Propagation Metrics** (to be tracked):
- Template coverage: % of chora-base capabilities with templates
- Propagation time: Time from chora-base implementation to template availability
- Adoption rate: % of generated projects using latest templates

#### 6.3.6 Guarantees for Propagated Capabilities

When a capability is properly propagated via templates, the generated project guarantees:

1. **Template Rendering**:
   - ✅ All `.template` files rendered correctly
   - ✅ All variables substituted (no `{{ placeholders }}` remaining)
   - ✅ Jinja2 filters applied correctly (e.g., `{{ var | upper }}`)

2. **Syntax Validity**:
   - ✅ Generated code compiles/validates
   - ✅ Configuration files parse correctly (YAML, TOML, JSON)
   - ✅ Scripts have proper shebangs and permissions

3. **Integration**:
   - ✅ Capability works in generated project immediately
   - ✅ No additional setup required (unless documented)
   - ✅ Dependencies declared in pyproject.toml

4. **Documentation**:
   - ✅ Usage guide included (if needed)
   - ✅ Examples provided (if applicable)
   - ✅ Troubleshooting guide (if complex)

#### 6.3.7 Best Practices

**DO**:
- ✅ Test template rendering on Windows and Unix
- ✅ Use Jinja2 default filters: `{{ var | default('fallback') }}`
- ✅ Document all new template variables
- ✅ Create comprehensive test fixtures
- ✅ Update SAP ledgers immediately after propagation
- ✅ Cross-reference completion summaries

**DON'T**:
- ❌ Hardcode values that should be variables
- ❌ Skip integration testing
- ❌ Forget to update version history
- ❌ Leave unsubstituted variables in output
- ❌ Mix capability propagation with other changes

**Example** (GAP-003 Track 2):
```bash
# Good: Dedicated commit for template propagation
git commit -m "feat(gap-003): Add release workflow script templates"

# Bad: Mixed with unrelated changes
git commit -m "feat: Add templates and fix bug and update docs"
```

---

## 7. Error Handling

### 7.1 Common Errors

**Error: static-template/ not found**
```
Error: static-template/ not found at /path/to/chora-base/static-template
```
**Cause**: setup.py not run from chora-base root
**Recovery**: Run from chora-base root directory

**Error: Invalid slug**
```
Error: Invalid slug (must start with lowercase letter, use hyphens)
```
**Cause**: project_slug doesn't match `^[a-z][a-z0-9-]+$`
**Recovery**: Re-enter slug (lowercase, hyphens only)

**Error: Invalid email**
```
Error: Invalid email address
```
**Cause**: Email doesn't match RFC 5322 format
**Recovery**: Re-enter valid email

**Error: Directory not empty**
```
Warning: Directory target-dir is not empty!
Continue anyway? [y/N]:
```
**Cause**: Target directory exists with files
**Recovery**: Choose different directory or confirm overwrite

**Error: Unreplaced placeholders**
```
⚠ Unreplaced placeholders in pyproject.toml
```
**Cause**: Variable not in variables dict
**Recovery**: Check blueprint variables, update setup.py:89-186

### 7.2 Validation Failures

**Missing Files**:
```
Validating setup...
  ✓ pyproject.toml
  ✗ Missing: src/my_project/__init__.py

⚠ Validation found issues (see above)
```
**Recovery**: Check rename_package_directories succeeded, check static-template complete

**Unreplaced Placeholders**:
```
Validating setup...
  ⚠ Unreplaced placeholders in README.md

⚠ Validation found issues (see above)
```
**Recovery**: Check blueprint mappings, check variable names match

---

## 8. Quality Attributes

### 8.1 Maintainability

**Blueprint Addition**:
1. Create `blueprints/newfile.blueprint`
2. Add mapping to `blueprint_mappings` dict (setup.py:231-242)
3. Add validation if critical file (setup.py:322-331)
4. Update SAP-003 Protocol (this document, Section 3.3)

**Variable Addition**:
1. Add to `gather_variables()` function (setup.py:89-186)
2. Update variables dict documentation (this document, Section 3.1)
3. Use in blueprints as `{{ new_variable }}`
4. Test with generation

### 8.2 Testability

**Generation Testing**:
```bash
# Test generation with specific values
python setup.py test-project

# Validate generated project
cd test-project
pytest --collect-only  # Check tests loadable
pytest                 # Run tests
```

**Automated Testing** (future):
```bash
# CI test: Generate project + validate
./scripts/test-generation.sh
```

### 8.3 Performance

**Current** (baseline):
- Human with setup.py: 60-90 seconds (interactive prompts slow)
- Agent (Claude Code): 30-60 seconds (parallel operations)

**Target** (Phase 4):
- Agent (Claude Code): 20-40 seconds (optimized parallel)

**Bottlenecks**:
- Copy static-template (100+ files): ~5-10 seconds
- Git initialization: ~2-5 seconds

**Optimizations**:
- Parallel blueprint reading
- Parallel file validation
- Pre-computed blueprint mappings

---

## 9. Dependencies

### 9.1 Internal Dependencies

**Required Files**:
- `setup.py` (443 lines) - Generation orchestrator
- `blueprints/` (12 files) - Variable substitution templates
- `static-template/` (100+ files) - Complete project scaffold

**Related SAPs**:
- SAP-002 (chora-base-meta) - References SAP-003
- SAP-004 (testing-framework) - Generated tests must match
- SAP-005 (ci-cd-workflows) - Generated workflows must match
- SAP-006 (quality-gates) - Generated quality configs must match

### 9.2 External Dependencies

**Required**:
- Python 3.11+ (setup.py uses modern Python)
- Git 2.0+ (for repository initialization)

**Optional**:
- None (zero-dependency generation)

---

## 10. Versioning

### 10.1 Template Versioning

**Current Version**: 3.3.0 (from setup.py:23)

**Version Tracking**:
- Stored in setup.py: `TEMPLATE_VERSION = "3.3.0"`
- Written to generated projects: `variables['template_version']`
- Included in git commit message

**Version Format**: Semver (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes (incompatible upgrades)
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### 10.2 Upgrade Paths

**Upgrade Strategy**:
1. Check current template version (pyproject.toml, README.md)
2. Find upgrade blueprint: `docs/upgrades/vX.Y-to-vA.B.md`
3. Follow upgrade steps
4. Update template_version in project
5. Test project (pytest, workflows)

**Example**: v3.0 → v3.3 upgrade
1. Read: `docs/upgrades/v3.0-to-v3.3.md`
2. Manual changes (if any)
3. Re-run specific blueprints (if needed)
4. Update version in pyproject.toml

---

## 11. Best Practices

### 11.1 For Template Maintainers

**Adding Blueprints**:
1. Create blueprint file in `blueprints/`
2. Use existing variables or add new ones
3. Add mapping to setup.py
4. Test generation with new blueprint
5. Update SAP-003 Protocol

**Changing Static Template**:
1. Make changes in `static-template/`
2. Test generation (verify files copied correctly)
3. Update validation if critical file
4. Document changes in CHANGELOG
5. Update SAP-003 Protocol if major change

**Version Updates**:
1. Update `TEMPLATE_VERSION` in setup.py
2. Update CHANGELOG.md
3. Create upgrade blueprint if breaking
4. Update SAP-003 Ledger with new version
5. Notify adopters

### 11.2 For Project Adopters

**Initial Generation**:
1. Read SAP-003 Adoption Blueprint
2. Prepare project name, author info
3. Run `python setup.py <target-dir>`
4. Validate with `pytest --collect-only`
5. Start development

**Customization**:
1. Modify generated files (not template)
2. Track customizations in CHANGELOG
3. Be aware of upgrade implications
4. Consider contributing patterns back to template

**Upgrades**:
1. Check current version (README.md)
2. Find upgrade blueprint
3. Back up project
4. Follow upgrade steps
5. Test thoroughly

---

## 12. Related Documents

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [sap-framework/protocol-spec.md](../sap-framework/protocol-spec.md) - SAP structure
- [INDEX.md](../INDEX.md) - SAP registry

**SAP-003 Artifacts**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - How to generate projects
- [ledger.md](ledger.md) - Adopter tracking

**Generation Components**:
- [setup.py](/setup.py) - Generation orchestrator (443 lines)
- [blueprints/](/blueprints/) - Variable templates (12 files)
- [static-template/](/static-template/) - Project scaffold (100+ files)

**Related SAPs**:
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - Meta-SAP Section 3.2.1
- [testing-framework/](../testing-framework/) - SAP-004 (generated test structure)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (generated workflows)
- [quality-gates/](../quality-gates/) - SAP-006 (generated quality configs)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for project-bootstrap
