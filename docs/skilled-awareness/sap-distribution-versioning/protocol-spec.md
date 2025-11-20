# SAP Distribution & Versioning: Protocol Specification

**SAP ID**: SAP-062
**Version**: 1.0.0
**Status**: draft
**Last Updated**: 2025-11-20

---

## 1. Copier Template Patterns

### 1.1 Template Directory Structure

**Required Structure**:
```
chora-base/
├── copier.yml                    # Template configuration + questionnaire
├── template/                     # Template files (will be copied)
│   ├── .github/
│   │   └── workflows/           # CI/CD workflows (conditional)
│   ├── docs/                    # Documentation (conditional SAPs)
│   ├── scripts/                 # Automation scripts (conditional SAPs)
│   ├── justfile                 # Recipe collection (base + conditional)
│   ├── pyproject.toml          # Python project config (conditional)
│   ├── README.md               # Project README (templated)
│   └── .gitignore              # Standard ignores
├── {{ _copier_conf.answers_file }}.jinja  # .copier-answers.yml template
└── includes/                    # Reusable template fragments (optional)
```

**Design Principles**:
1. **Minimal by default**: Base template includes only essential files (README, .gitignore, basic structure)
2. **Conditional SAP inclusion**: SAP-specific files added only if selected in questionnaire
3. **No template artifacts**: Generated project contains no `copier.yml`, `template/`, or `includes/`
4. **Clean directory structure**: Generated project looks hand-crafted (not template-generated)

---

### 1.2 Variable Naming Conventions

**Standard Variables** (all templates must include):
```yaml
# copier.yml
project_name:
  type: str
  help: "Project name (lowercase, hyphens, no spaces)"
  validator: "{% if not project_name | regex_search('^[a-z0-9-]+$') %}Invalid project name{% endif %}"

project_slug:
  type: str
  default: "{{ project_name | lower | replace(' ', '-') | replace('_', '-') }}"

author_name:
  type: str
  help: "Your name (for copyright, README)"

author_email:
  type: str
  help: "Your email (for pyproject.toml, git config)"
  validator: "{% if '@' not in author_email %}Invalid email{% endif %}"

python_version:
  type: str
  default: "3.11"
  choices:
    - "3.9"
    - "3.10"
    - "3.11"
    - "3.12"
```

**SAP Selection Variables** (multi-select checkboxes):
```yaml
sap_selection:
  type: str
  help: "Which SAP bundle do you want?"
  choices:
    Minimal (2-3 SAPs): minimal
    Standard (4-6 SAPs): standard
    Comprehensive (8-12 SAPs): comprehensive
    Custom (pick individual SAPs): custom
  default: standard

# Conditional: If custom selected
sap_coordination:
  type: bool
  help: "Include SAP-001 (Inbox Coordination)?"
  default: yes
  when: "{{ sap_selection == 'custom' }}"

sap_task_tracking:
  type: bool
  help: "Include SAP-015 (Beads Task Tracking)?"
  default: yes
  when: "{{ sap_selection == 'custom' }}"

sap_memory_system:
  type: bool
  help: "Include SAP-010 (A-MEM Memory System)?"
  default: no
  when: "{{ sap_selection == 'custom' }}"

# ... (additional SAP variables)
```

**Computed Variables** (derived from user input):
```yaml
_sap_list:
  type: list
  # Computed based on sap_selection + individual SAP flags
  # Used internally for conditional file inclusion

_requires_python_tooling:
  type: bool
  # True if any SAP requires Python (pyproject.toml, poetry, pytest)

_requires_justfile:
  type: bool
  # True if any SAP includes automation recipes
```

**Naming Rules**:
1. **User-facing variables**: `snake_case` (e.g., `project_name`, `author_email`)
2. **Internal variables**: `_snake_case` with leading underscore (e.g., `_sap_list`, `_requires_python`)
3. **SAP variables**: `sap_<sap_name>` (e.g., `sap_coordination`, `sap_task_tracking`)
4. **Boolean variables**: Use `yes`/`no` (not `true`/`false`) for Copier compatibility
5. **Choice variables**: Use descriptive keys, not cryptic codes (e.g., `"Standard (4-6 SAPs): standard"`)

---

### 1.3 Inline Jinja2 Expressions

**Conditional File Inclusion**:
```jinja
{# Only include if SAP-001 selected #}
{% if sap_coordination %}
docs/coordination/
  inbox-workflow.md
scripts/
  inbox-status.py
{% endif %}

{# Only include if SAP-015 selected #}
{% if sap_task_tracking %}
scripts/
  beads-helper.sh
docs/
  task-tracking-guide.md
{% endif %}
```

**Conditional File Content**:
```jinja
{# justfile: Conditional recipe inclusion #}
# Base recipes (always included)
help:
    just --list

{% if sap_coordination %}
# SAP-001: Inbox Coordination recipes
inbox-status:
    python scripts/inbox-status.py

inbox-list:
    python scripts/inbox-status.py --list
{% endif %}

{% if sap_task_tracking %}
# SAP-015: Beads Task Tracking recipes
task-list:
    bd list

task-create TITLE:
    bd create "{{TITLE}}"
{% endif %}
```

**Variable Substitution**:
```jinja
{# README.md: Project-specific content #}
# {{ project_name }}

**Author**: {{ author_name }} ({{ author_email }})
**Python Version**: {{ python_version }}

## Included SAPs

{% if sap_coordination %}
- **SAP-001**: Inbox Coordination ([docs/coordination/](docs/coordination/))
{% endif %}
{% if sap_task_tracking %}
- **SAP-015**: Beads Task Tracking ([scripts/beads-helper.sh](scripts/beads-helper.sh))
{% endif %}
```

**Expression Syntax Rules**:
1. **Conditionals**: `{% if condition %}...{% endif %}` (block statements)
2. **Variable output**: `{{ variable }}` (inline substitution)
3. **Comments**: `{# comment text #}` (ignored in output)
4. **Filters**: `{{ project_name | lower | replace(' ', '-') }}` (transformation pipeline)
5. **Whitespace control**: `{%- if -%}` (strip whitespace before/after tags)

---

### 1.4 Questionnaire Design Principles

**Progressive Disclosure**:
```yaml
# Step 1: Essential project info
project_name:
  help: "Project name (lowercase, hyphens)"

author_name:
  help: "Your name"

# Step 2: SAP selection (high-level)
sap_selection:
  help: "Which SAP bundle?"
  choices: [minimal, standard, comprehensive, custom]

# Step 3: Custom SAP selection (only if custom chosen)
sap_coordination:
  when: "{{ sap_selection == 'custom' }}"

# Step 4: Advanced options (optional, after main flow)
include_ci_cd:
  help: "Include GitHub Actions CI/CD?"
  default: no
```

**Sensible Defaults**:
- Default to `standard` bundle (4-6 SAPs) - balances utility and simplicity
- Default to `yes` for common SAPs (SAP-001, SAP-015) - most projects need these
- Default to `no` for advanced SAPs (SAP-010, SAP-053) - opt-in for complexity
- Default to current Python version (`3.11`) - avoid outdated defaults

**Clear Help Text**:
```yaml
sap_coordination:
  help: |
    Include SAP-001 (Inbox Coordination)?

    Provides structured intake for coordination requests, strategic proposals,
    and implementation tasks. Recommended for multi-developer projects.

    Files: docs/coordination/, scripts/inbox-status.py, templates/
    Effort: 5-10 min initial setup
```

**Input Validation**:
```yaml
project_name:
  validator: "{% if not project_name | regex_search('^[a-z0-9-]+$') %}Project name must be lowercase, hyphens, no spaces{% endif %}"

author_email:
  validator: "{% if '@' not in author_email %}Invalid email format (must contain @){% endif %}"

python_version:
  choices: ["3.9", "3.10", "3.11", "3.12"]  # Restrict to valid options
```

**Questionnaire Completion Time Target**: <3 minutes for standard bundle, <5 minutes for custom selection

---

## 2. Semantic Versioning Strategy

### 2.1 Version Number Format

**Format**: `MAJOR.MINOR.PATCH` (e.g., `1.0.0`, `1.1.0`, `2.0.0`)

**Examples**:
- `1.0.0` - Initial release (SAP-062 L4 distribution)
- `1.0.1` - Bug fix (typo in README template)
- `1.1.0` - New feature (add SAP-053 to template)
- `2.0.0` - Breaking change (restructure directory layout)

---

### 2.2 Version Bump Rules

**PATCH Bump** (1.0.X → 1.0.Y):
- **Trigger**: Bug fixes, documentation updates, typo corrections
- **Examples**:
  - Fix broken link in README template
  - Correct typo in questionnaire help text
  - Update copyright year in LICENSE template
  - Fix incorrect default value in copier.yml
- **Backward Compatibility**: **Required** (existing projects can update safely)
- **Breaking Changes**: **Forbidden** (any breaking change requires MAJOR bump)

**MINOR Bump** (1.X.0 → 1.Y.0):
- **Trigger**: New features, non-breaking enhancements, new SAP additions
- **Examples**:
  - Add new SAP to template (SAP-053, SAP-061, SAP-062)
  - Add new questionnaire option (e.g., "include CI/CD?")
  - Enhance existing SAP with new script (non-breaking addition)
  - Add optional post-generation hook (doesn't affect existing projects)
- **Backward Compatibility**: **Required** (new features are additive only)
- **Breaking Changes**: **Forbidden** (backward compatibility mandatory)

**MAJOR Bump** (X.0.0 → Y.0.0):
- **Trigger**: Breaking changes, deprecation removals, architecture changes
- **Examples**:
  - Restructure directory layout (e.g., `scripts/` → `automation/`)
  - Remove deprecated SAP (after 2+ version deprecation period)
  - Change variable naming convention (e.g., `project_name` → `name`)
  - Require newer Python version (e.g., drop Python 3.9 support)
- **Backward Compatibility**: **Not Required** (breaking changes allowed)
- **Migration Guide**: **Required** (must document upgrade path)
- **Deprecation Period**: **Required** (2+ MINOR versions warning before removal)

---

### 2.3 Version Tagging Workflow

**Git Tagging**:
```bash
# Tag new version in chora-base repository
git tag -a v1.1.0 -m "feat: Add SAP-053 to template (Conflict Resolution)"
git push origin v1.1.0

# Tag format: v<MAJOR>.<MINOR>.<PATCH>
# Annotation: Conventional Commit message (feat/fix/BREAKING CHANGE)
```

**Tag Naming Convention**:
- Format: `vMAJOR.MINOR.PATCH` (e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`)
- Prefix: Always use `v` prefix (Copier convention)
- No suffixes: No `-alpha`, `-beta`, `-rc` (use branches for pre-release)

**When to Tag**:
1. After completing SAP integration (e.g., SAP-053 added to template)
2. After fixing critical bug (e.g., broken template generation)
3. After completing migration guide for breaking change
4. Never tag work-in-progress (WIP) or incomplete features

**Tag Annotation Guidelines**:
```bash
# Good tag annotations (Conventional Commits format)
git tag -a v1.0.1 -m "fix: Correct typo in README template"
git tag -a v1.1.0 -m "feat: Add SAP-053 (Conflict Resolution) to template"
git tag -a v2.0.0 -m "BREAKING CHANGE: Restructure directory layout (scripts/ → automation/)"

# Bad tag annotations (too vague)
git tag -a v1.1.0 -m "Update"  # ❌ Too vague
git tag -a v1.1.0 -m "Various improvements"  # ❌ Not specific
```

---

### 2.4 `_commit` Field Usage

**Purpose**: Pin template to specific git commit (not just version tag)

**Use Cases**:
1. **Version pinning**: Generate project from specific template version
2. **Development testing**: Test unreleased template changes
3. **Reproducible builds**: Ensure exact template version for audit trail

**Syntax**:
```bash
# Generate from specific version tag
copier copy --vcs-ref v1.1.0 gh:liminalcommons/chora-base my-project

# Generate from specific commit hash
copier copy --vcs-ref abc1234 gh:liminalcommons/chora-base my-project

# Generate from branch (not recommended for production)
copier copy --vcs-ref feature-branch gh:liminalcommons/chora-base my-project
```

**`.copier-answers.yml` Example**:
```yaml
# Project generated from template
_src_path: gh:liminalcommons/chora-base
_commit: v1.1.0  # Pinned to version 1.1.0
project_name: my-awesome-project
author_name: John Doe
sap_selection: standard
```

**Update Behavior**:
```bash
# Update to latest version (respects _commit pin)
copier update

# Output: "Template is already at v1.1.0. Use --vcs-ref to update to different version."

# Force update to newer version
copier update --vcs-ref v1.2.0

# Output: "Updating from v1.1.0 to v1.2.0..."
```

**Best Practices**:
- **Use version tags** (`v1.1.0`) not commit hashes (`abc1234`) - tags are human-readable
- **Pin production projects** to stable versions (not `HEAD` or `main` branch)
- **Test before updating** - run `copier update --vcs-ref v1.2.0` in test branch first
- **Review changelog** before updating (check for breaking changes, migration guides)

---

## 3. Update Propagation (`copier update`)

### 3.1 Update Workflow

**Standard Update Process**:
```bash
# Step 1: Check current template version
cat .copier-answers.yml | grep _commit
# Output: _commit: v1.0.0

# Step 2: Review template changelog
# Visit: https://github.com/liminalcommons/chora-base/blob/main/CHANGELOG.md
# Check: What changed between v1.0.0 and latest?

# Step 3: Create update branch (recommended)
git checkout -b update-template-v1.1.0

# Step 4: Run copier update
copier update

# Step 5: Review changes (git diff)
git diff

# Step 6: Resolve conflicts (if any)
# See Section 3.3 for conflict resolution patterns

# Step 7: Test changes
# Run: just test, pytest, etc.

# Step 8: Commit update
git add .
git commit -m "chore: Update template from v1.0.0 to v1.1.0"

# Step 9: Merge to main
git checkout main
git merge update-template-v1.1.0
```

**Update Frequency Recommendations**:
- **PATCH updates**: Apply within 1 week (low risk, bug fixes only)
- **MINOR updates**: Review within 1 month (new features, low risk)
- **MAJOR updates**: Review carefully, schedule migration (breaking changes)
- **Security patches**: Apply immediately (if template has security fixes)

---

### 3.2 `.copier-answers.yml` Structure

**Purpose**: Stores user's original questionnaire responses + template metadata

**Location**: Project root (e.g., `my-project/.copier-answers.yml`)

**Standard Fields**:
```yaml
# Template metadata (managed by Copier)
_src_path: gh:liminalcommons/chora-base  # Template source URL
_commit: v1.1.0                           # Current template version
_copier_version: 9.1.0                    # Copier tool version

# User responses (from questionnaire)
project_name: my-awesome-project
project_slug: my-awesome-project
author_name: John Doe
author_email: john@example.com
python_version: '3.11'

# SAP selection
sap_selection: standard
sap_coordination: yes
sap_task_tracking: yes
sap_memory_system: no
sap_automation: yes
sap_link_validation: yes
sap_traceability: yes

# Advanced options
include_ci_cd: no
include_docker: no
```

**Field Modification**:
- **Template metadata**: Automatically updated by `copier update` (don't edit manually)
- **User responses**: Safe to edit manually (will be preserved across updates)
- **New questionnaire options**: Will be prompted during `copier update` if template adds new questions

**Version Control**:
- **Commit to git**: **YES** - `.copier-answers.yml` should be version controlled
- **Gitignore**: **NO** - don't add to `.gitignore` (needed for updates)
- **Reason**: Required for `copier update` to know template version and user preferences

---

### 3.3 Conflict Resolution Patterns

**Common Conflict Scenarios**:

#### Conflict 1: justfile Recipe Name Change

**Scenario**: Template renames recipe `sap-check` → `sap-validate`

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
sap-check:
    python scripts/sap-evaluator.py --quick
=======
sap-validate:
    python scripts/sap-evaluator.py --quick
>>>>>>> template-v1.2.0
```

**Resolution Strategy**: **Accept template change + preserve local customizations**
```bash
# 1. Accept template's new recipe name
sap-validate:
    python scripts/sap-evaluator.py --quick

# 2. Add backward-compatible alias (optional)
sap-check: sap-validate  # Deprecated: use sap-validate
```

**Time to Resolve**: <1 min

---

#### Conflict 2: README.md Content Conflict

**Scenario**: Both template and local project updated README.md

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
## Features

- Custom feature A (local addition)
- Custom feature B (local addition)
=======
## Features

- Template feature X (template addition from v1.2.0)
>>>>>>> template-v1.2.0
```

**Resolution Strategy**: **Merge both changes**
```markdown
## Features

- Custom feature A (local addition)
- Custom feature B (local addition)
- Template feature X (template addition from v1.2.0)
```

**Time to Resolve**: <2 min

---

#### Conflict 3: Script Path Restructure (Breaking Change)

**Scenario**: Template v2.0.0 moves `scripts/` → `automation/` (BREAKING CHANGE)

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
scripts/
  inbox-status.py (local customizations)
  beads-helper.sh (local customizations)
=======
automation/
  inbox-status.py (template update)
  beads-helper.sh (template update)
>>>>>>> template-v2.0.0
```

**Resolution Strategy**: **Follow migration guide** (template v2.0.0 must provide guide)
```bash
# 1. Read migration guide (template CHANGELOG.md or MIGRATION-v2.0.md)
# 2. Move local customizations to new structure
mv scripts/inbox-status.py automation/inbox-status.py
mv scripts/beads-helper.sh automation/beads-helper.sh

# 3. Update references (justfile, docs, other scripts)
# Old: python scripts/inbox-status.py
# New: python automation/inbox-status.py

# 4. Remove old directory
rm -rf scripts/
```

**Time to Resolve**: 10-15 min (requires testing)

---

#### Conflict 4: pyproject.toml Dependency Version

**Scenario**: Template updates dependency version, local project has different version

**Conflict**:
```diff
<<<<<<< HEAD (your local version)
[tool.poetry.dependencies]
python = "^3.10"
pytest = "^7.3.0"  # Local version
=======
[tool.poetry.dependencies]
python = "^3.11"
pytest = "^8.0.0"  # Template update
>>>>>>> template-v1.3.0
```

**Resolution Strategy**: **Prefer template version + test**
```bash
# 1. Accept template's newer dependency versions
[tool.poetry.dependencies]
python = "^3.11"
pytest = "^8.0.0"

# 2. Update lock file
poetry update

# 3. Run tests to verify compatibility
pytest

# 4. If tests fail, investigate and fix (or revert to old version temporarily)
```

**Time to Resolve**: 5-10 min (includes testing)

---

### 3.4 Conflict Prevention Best Practices

**For Template Maintainers**:
1. **Avoid renaming files** unless absolutely necessary (creates merge conflicts)
2. **Use additive changes** - add new files instead of modifying existing ones
3. **Document breaking changes** in CHANGELOG.md with migration guide
4. **Test updates** with real projects before releasing new version
5. **Use MINOR bumps** for most changes (reserve MAJOR for true breaking changes)

**For Template Users**:
1. **Don't modify template files** directly - extend or override instead
   - ❌ **Bad**: Edit `justfile` directly (conflicts on update)
   - ✅ **Good**: Create `justfile.local` and include it
2. **Commit frequently** before running `copier update` (easy to revert)
3. **Use update branches** (don't update directly on `main`)
4. **Review changelog** before updating (know what changed)
5. **Test after updating** (run tests, check scripts, validate docs)

---

## 4. Backward Compatibility Management

### 4.1 Deprecation Policy

**Deprecation Timeline**:
```
v1.0.0: Feature introduced (sap-check recipe)
v1.1.0: Feature still supported (no changes)
v1.2.0: Feature deprecated (add deprecation warning, introduce replacement)
v1.3.0: Feature still supported (continue deprecation warning)
v2.0.0: Feature removed (breaking change, migration guide required)
```

**Minimum Deprecation Period**: **2 MINOR versions** before removal

**Example - Recipe Deprecation**:
```bash
# v1.2.0: Add deprecation warning
sap-check:
    @echo "⚠️  DEPRECATED: sap-check is deprecated, use sap-validate instead (will be removed in v2.0.0)"
    python scripts/sap-evaluator.py --quick

sap-validate:
    python scripts/sap-evaluator.py --quick

# v1.3.0: Continue warning
sap-check:
    @echo "⚠️  DEPRECATED: sap-check will be removed in v2.0.0. Use sap-validate instead."
    python scripts/sap-evaluator.py --quick

sap-validate:
    python scripts/sap-evaluator.py --quick

# v2.0.0: Remove deprecated recipe
# sap-check: <-- REMOVED (breaking change)

sap-validate:
    python scripts/sap-evaluator.py --quick
```

**Deprecation Warning Format**:
```
⚠️  DEPRECATED: <old-feature> is deprecated, use <new-feature> instead (will be removed in v<version>)
```

---

### 4.2 Migration Guides

**Required for MAJOR Version Bumps**:

Every MAJOR version bump (1.x.x → 2.0.0) **must include**:
1. **CHANGELOG.md entry** with breaking changes section
2. **MIGRATION-v2.0.md** guide (separate file for complex migrations)
3. **Before/after examples** (show old vs new approach)
4. **Migration script** (if possible, automate the migration)

**Migration Guide Template**:
```markdown
# Migration Guide: v1.x.x → v2.0.0

## Breaking Changes

### 1. Directory Restructure: scripts/ → automation/

**What Changed**:
- All scripts moved from `scripts/` to `automation/`
- Justfile recipes updated to use new paths
- Documentation links updated

**Action Required**:
1. Move your custom scripts:
   ```bash
   mv scripts/my-custom-script.sh automation/my-custom-script.sh
   ```

2. Update justfile recipes:
   ```diff
   - python scripts/my-script.py
   + python automation/my-script.py
   ```

3. Update documentation links:
   ```diff
   - [My Script](scripts/my-script.py)
   + [My Script](automation/my-script.py)
   ```

**Estimated Time**: 10-15 minutes

**Testing**: Run `just --list` to verify all recipes work

---

### 2. Recipe Rename: sap-check → sap-validate

**What Changed**:
- `sap-check` recipe removed (deprecated since v1.2.0)
- Use `sap-validate` instead

**Action Required**:
1. Update scripts/docs that reference `just sap-check`:
   ```diff
   - just sap-check
   + just sap-validate
   ```

**Estimated Time**: <5 minutes

**Testing**: Run `just sap-validate` to verify it works

---

## Rollback Instructions

If migration fails or causes issues:

```bash
# 1. Revert to previous template version
copier update --vcs-ref v1.3.0

# 2. Or: Reset to pre-update state
git checkout <commit-before-update>
git checkout -b revert-update
```
```

---

### 4.3 Version Compatibility Matrix

**Template Version → chora-base Version Requirements**:

| Template Version | chora-base Version | Python Version | Copier Version | Breaking Changes |
|------------------|-------------------|----------------|----------------|------------------|
| **v1.0.0** | chora-base v1.0.0+ | Python 3.9+ | Copier 8.0+ | Initial release |
| **v1.1.0** | chora-base v1.1.0+ | Python 3.9+ | Copier 8.0+ | Added SAP-053, SAP-061 |
| **v1.2.0** | chora-base v1.2.0+ | Python 3.10+ | Copier 8.0+ | Deprecated sap-check recipe |
| **v2.0.0** | chora-base v2.0.0+ | Python 3.11+ | Copier 9.0+ | **BREAKING**: Restructured directories |

**SAP Version Compatibility**:

| SAP | Template v1.0.0 | Template v1.1.0 | Template v2.0.0 | Notes |
|-----|----------------|----------------|----------------|-------|
| SAP-001 | ✅ Supported | ✅ Supported | ✅ Supported | Inbox Coordination |
| SAP-015 | ✅ Supported | ✅ Supported | ✅ Supported | Beads Task Tracking |
| SAP-053 | ❌ Not available | ✅ Added v1.1.0 | ✅ Supported | Conflict Resolution |
| SAP-061 | ❌ Not available | ✅ Added v1.1.0 | ✅ Supported | Ecosystem Integration |
| SAP-062 | ❌ Not available | ❌ Not available | ✅ Added v2.0.0 | Distribution & Versioning |

**Dependency Compatibility**:

```yaml
# pyproject.toml - Minimum versions required by template

# Template v1.0.0 requirements
[tool.poetry.dependencies]
python = "^3.9"
pyyaml = "^6.0"
click = "^8.0"

# Template v1.1.0 requirements (added SAP-053, SAP-061)
[tool.poetry.dependencies]
python = "^3.9"
pyyaml = "^6.0"
click = "^8.0"
gitpython = "^3.1"  # Added for SAP-053 conflict detection

# Template v2.0.0 requirements (breaking change: Python 3.11+)
[tool.poetry.dependencies]
python = "^3.11"  # BREAKING: Dropped Python 3.9/3.10 support
pyyaml = "^6.0"
click = "^8.1"
gitpython = "^3.1"
```

---

### 4.4 Graceful Degradation Patterns

**Principle**: New template features should not break old projects

**Pattern 1: Optional Dependency**
```python
# scripts/new-feature.py (added in v1.2.0)
try:
    import new_library  # New dependency added in v1.2.0
except ImportError:
    print("⚠️  new_library not installed. Install with: pip install new-library")
    print("⚠️  Or update pyproject.toml to template v1.2.0")
    sys.exit(1)
```

**Pattern 2: Feature Detection**
```bash
# justfile (added in v1.2.0)
# New recipe that uses new SAP
sap-new-feature:
    @if [ ! -f "scripts/new-feature.py" ]; then \
        echo "⚠️  SAP-XXX not installed. Update template to v1.2.0 to use this feature."; \
        exit 1; \
    fi
    python scripts/new-feature.py
```

**Pattern 3: Version Check**
```python
# scripts/helper.py (utility used by multiple scripts)
import sys

REQUIRED_TEMPLATE_VERSION = "1.2.0"

def check_template_version():
    """Warn if template is outdated (but don't block)."""
    try:
        with open(".copier-answers.yml", "r") as f:
            import yaml
            data = yaml.safe_load(f)
            current_version = data.get("_commit", "unknown").lstrip("v")

            if current_version < REQUIRED_TEMPLATE_VERSION:
                print(f"⚠️  Warning: Template version {current_version} is outdated.")
                print(f"⚠️  Some features require template v{REQUIRED_TEMPLATE_VERSION}+")
                print(f"⚠️  Run 'copier update' to update.")
                # Don't exit - just warn (graceful degradation)
    except FileNotFoundError:
        pass  # .copier-answers.yml not found (not a template-generated project)
```

---

## 5. Post-Generation Hooks

### 5.1 Hook Execution Order

**Copier Hook Lifecycle**:
```
1. User answers questionnaire
2. Copier processes Jinja2 templates
3. Copier copies files to destination
4. ⚙️  PRE-PROJECT HOOK (optional)
5. Copier creates project directory
6. ⚙️  POST-PROJECT HOOK (optional)
7. Done
```

---

### 5.2 Standard Post-Generation Hooks

**Hook Definition** (in `copier.yml`):
```yaml
_tasks:
  # Hook 1: Initialize git repository
  - command: git init
    when: "{{ include_git_init }}"

  # Hook 2: Install Python dependencies
  - command: poetry install
    when: "{{ _requires_python_tooling }}"

  # Hook 3: Initialize pre-commit hooks
  - command: pre-commit install
    when: "{{ include_precommit }}"

  # Hook 4: Create initial git commit
  - command: |
      git add .
      git commit -m "chore: Initial commit from template v{{ _commit }}"
    when: "{{ include_git_init }}"
```

**Hook Best Practices**:
1. **Make hooks optional** - use `when` conditions (don't force on all users)
2. **Handle failures gracefully** - hooks should warn, not crash
3. **Keep hooks fast** - target <30 sec total execution time
4. **Document hook behavior** - explain what each hook does in README

---

### 5.3 Custom Hook Examples

**Hook: Create .env file from template**
```yaml
_tasks:
  - command: |
      if [ ! -f .env ]; then
        cp .env.example .env
        echo "✅ Created .env file (edit with your settings)"
      fi
```

**Hook: Set up development database**
```yaml
_tasks:
  - command: |
      if command -v docker &> /dev/null; then
        docker-compose up -d postgres
        echo "✅ Started PostgreSQL database"
      else
        echo "⚠️  Docker not found. Skipping database setup."
      fi
    when: "{{ include_docker }}"
```

**Hook: Generate SSH keys**
```yaml
_tasks:
  - command: |
      if [ ! -f .ssh/id_rsa ]; then
        mkdir -p .ssh
        ssh-keygen -t rsa -b 4096 -f .ssh/id_rsa -N ""
        echo "✅ Generated SSH keys"
      fi
    when: "{{ include_ssh_keys }}"
```

---

## 6. Multi-Tier SAP Selection

### 6.1 Tier Definitions

**Minimal Tier** (2-3 SAPs):
- **Target**: Single-developer projects, prototypes, learning
- **Setup time**: <2 min
- **SAPs**:
  - SAP-001 (Inbox Coordination) - Optional
  - SAP-015 (Beads Task Tracking) - Required
- **Files**: ~10 files (~500 lines total)

**Standard Tier** (4-6 SAPs):
- **Target**: Small teams (2-5 developers), production projects
- **Setup time**: 2-3 min
- **SAPs**:
  - SAP-001 (Inbox Coordination)
  - SAP-015 (Beads Task Tracking)
  - SAP-010 (A-MEM Memory System)
  - SAP-008 (Automation Recipes)
  - SAP-016 (Link Validation)
  - SAP-056 (Traceability)
- **Files**: ~30 files (~1,500 lines total)

**Comprehensive Tier** (8-12 SAPs):
- **Target**: Large teams (5+ developers), complex projects
- **Setup time**: 3-5 min
- **SAPs**:
  - All Standard SAPs +
  - SAP-053 (Conflict Resolution)
  - SAP-051 (Work Context Coordination)
  - SAP-052 (Code Ownership)
  - SAP-061 (Ecosystem Integration)
  - SAP-062 (Distribution & Versioning)
  - SAP-009 (Agent Awareness)
- **Files**: ~60 files (~3,000 lines total)

**Custom Tier**:
- **Target**: Power users, specific use cases
- **Setup time**: 5-10 min (questionnaire takes longer)
- **SAPs**: À la carte selection via questionnaire
- **Files**: Variable (depends on selection)

---

### 6.2 Tier Selection Logic

**Questionnaire Flow**:
```yaml
# Step 1: Ask tier preference
sap_selection:
  type: str
  help: "Which SAP bundle do you want?"
  choices:
    Minimal (2-3 SAPs) - Quick start, essential features: minimal
    Standard (4-6 SAPs) - Recommended for most projects: standard
    Comprehensive (8-12 SAPs) - Full ecosystem, advanced features: comprehensive
    Custom - Pick individual SAPs: custom
  default: standard

# Step 2: If custom, show individual SAP checkboxes
# (20+ questions, one per SAP)

# Step 3: Compute _sap_list based on tier or custom selection
```

**Tier Recommendation Logic**:
```
IF team_size == 1 THEN recommend minimal
ELSE IF team_size <= 5 THEN recommend standard
ELSE recommend comprehensive

IF project_type == "prototype" THEN recommend minimal
IF project_type == "production" AND team_size > 1 THEN recommend standard
```

---

### 6.3 SAP Dependency Resolution

**Current Approach** (v1.0.0): **Manual selection** (no automatic dependency resolution)

**Example**:
- User selects: SAP-053 (Conflict Resolution)
- SAP-053 depends on: SAP-051 (Work Context Coordination)
- **Current behavior**: User must manually select SAP-051 (no auto-resolution)

**Future Enhancement** (v2.0.0): **Automatic dependency resolution**

**Proposed Algorithm**:
```yaml
# copier.yml - SAP dependency graph
_sap_dependencies:
  SAP-053:
    - SAP-051  # Conflict Resolution depends on Work Context Coordination
    - SAP-015  # Conflict Resolution depends on Beads Task Tracking
  SAP-061:
    - SAP-016  # Ecosystem Integration depends on Link Validation
  SAP-062:
    - SAP-061  # Distribution & Versioning depends on Ecosystem Integration

# Compute _sap_list with transitive dependencies
_sap_list:
  # If user selected SAP-053, automatically add SAP-051 and SAP-015
```

**Defer to v2.0.0**: Dependency resolution adds complexity (validation, circular deps, version conflicts). Start simple (manual selection) in v1.0.0.

---

## 7. Testing & Validation

### 7.1 Template Generation Tests

**Test Suite** (in `tests/test_template_generation.py`):
```python
import subprocess
import pytest
from pathlib import Path

def test_minimal_tier_generation():
    """Test: Generate project with minimal tier."""
    result = subprocess.run([
        "copier", "copy",
        "--data", "sap_selection=minimal",
        "--data", "project_name=test-minimal",
        ".", "output/test-minimal"
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert Path("output/test-minimal/README.md").exists()
    assert Path("output/test-minimal/justfile").exists()
    assert Path("output/test-minimal/.copier-answers.yml").exists()

def test_standard_tier_generation():
    """Test: Generate project with standard tier."""
    # Similar to minimal, but check for more SAP files

def test_comprehensive_tier_generation():
    """Test: Generate project with comprehensive tier."""
    # Similar, but check for all SAP files

def test_custom_tier_generation():
    """Test: Generate project with custom SAP selection."""
    result = subprocess.run([
        "copier", "copy",
        "--data", "sap_selection=custom",
        "--data", "sap_coordination=yes",
        "--data", "sap_task_tracking=yes",
        "--data", "sap_memory_system=no",
        ".", "output/test-custom"
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert Path("output/test-custom/docs/coordination/").exists()
    assert not Path("output/test-custom/docs/memory/").exists()
```

---

### 7.2 Update Propagation Tests

**Test Suite** (in `tests/test_template_update.py`):
```python
def test_patch_update_no_conflicts():
    """Test: PATCH update (v1.0.0 → v1.0.1) should apply cleanly."""
    # 1. Generate project from v1.0.0
    # 2. Update to v1.0.1
    # 3. Assert no conflicts

def test_minor_update_with_new_sap():
    """Test: MINOR update (v1.0.0 → v1.1.0) adds new SAP files."""
    # 1. Generate project from v1.0.0 (without SAP-053)
    # 2. Update to v1.1.0 (adds SAP-053)
    # 3. Assert SAP-053 files present after update

def test_major_update_with_migration():
    """Test: MAJOR update (v1.0.0 → v2.0.0) requires migration."""
    # 1. Generate project from v1.0.0
    # 2. Update to v2.0.0 (breaking change: scripts/ → automation/)
    # 3. Assert migration guide is shown
    # 4. Assert old structure removed, new structure present
```

---

### 7.3 Validation Checklist

**Pre-Release Validation** (before tagging new version):
- ✅ Template generates successfully (all 3 tiers)
- ✅ All SAP scripts executable in generated project
- ✅ Questionnaire completes in <5 min (tested with real user)
- ✅ Post-generation hooks succeed (git init, poetry install)
- ✅ Generated project passes SAP-061 validation (`python scripts/validate-ecosystem-integration.py`)
- ✅ Update propagation tested (v1.0 → v1.1 → v2.0)
- ✅ CHANGELOG.md updated with version notes
- ✅ Migration guide written (if MAJOR version bump)

---

## Version History

### v1.0.0 (2025-11-20) - Initial Release

**Changes**:
- Initial protocol specification for SAP-062
- Copier template patterns (directory structure, variable naming, Jinja2 expressions, questionnaire design)
- Semantic versioning strategy (PATCH/MINOR/MAJOR bump rules, git tagging workflow, `_commit` usage)
- Update propagation protocol (`copier update` workflow, conflict resolution patterns)
- Backward compatibility management (deprecation policy, migration guides, version compatibility matrix)
- Post-generation hooks (git init, dependency install, pre-commit setup)
- Multi-tier SAP selection (minimal/standard/comprehensive/custom tiers)
- Testing & validation guidelines

**Context**:
- Created as part of CORD-2025-023 (3-SAP Suite Delivery)
- Phase 3 deliverable (parallel with Phase 4 SAP-050 promotion)
- Trace ID: sap-development-lifecycle-meta-saps-2025-11-20

**Author**: Claude (Anthropic) via tab-2 (chora-workspace)

---

**Created**: 2025-11-20
**Last Updated**: 2025-11-20
**Status**: draft
**Next Review**: After adoption-blueprint.md completion
