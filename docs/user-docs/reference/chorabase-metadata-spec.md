# .chorabase Metadata Specification

**Version**: 1.0
**Status**: Active
**Last Updated**: 2025-10-29

---

## Overview

The `.chorabase` file is a YAML configuration that defines the boundary between structure and content in chora-base projects. It enables automated merging of upstream updates while preserving project-specific customizations.

### Purpose

- Define which files are mergeable from upstream (structure)
- Protect project-specific files from accidental overwrites (content)
- Configure intelligent merge strategies for hybrid files
- Track project customizations and migrations

### Location

- **Root projects**: `/.chorabase` (chora-base itself)
- **Generated projects**: `/.chorabase` (projects created from chora-base)
- **Template**: `/static-template/.chorabase` (template for new projects)

---

## File Format

### Schema Version 1.0

```yaml
version: "4.1.0"                    # Chorabase version
structural_version: "4.1.0"         # Structural compatibility version
created: "2025-10-29"               # Creation date (YYYY-MM-DD)
project_type: "chora-base-project"  # Project type identifier

structure_only: []                  # List of structure-only files/patterns
content_only: []                    # List of content-only files/patterns
hybrid: {}                          # Map of hybrid files with strategies

customizations: []                  # Tracking of project customizations
merge: {}                           # Merge configuration
migration: {}                       # Migration tracking
```

---

## Core Fields

### `version`

**Type**: String (semver)
**Required**: Yes
**Description**: The chora-base version this file was created with

**Example**:
```yaml
version: "4.1.0"
```

**Usage**: Helps determine compatibility when merging from upstream

---

### `structural_version`

**Type**: String (semver)
**Required**: Yes
**Description**: The structural compatibility version

**Example**:
```yaml
structural_version: "4.1.0"
```

**Usage**:
- Used to determine if upstream changes are compatible
- Major version bump = breaking structural changes
- Minor version bump = new features, backward compatible
- Patch version bump = bug fixes

---

### `created`

**Type**: String (ISO 8601 date)
**Required**: Yes
**Description**: When this project was created/initialized

**Example**:
```yaml
created: "2025-10-29"
```

**Usage**: Tracking project age, helpful for understanding customization drift

---

### `project_type`

**Type**: String
**Required**: Yes
**Description**: Identifies the type of project

**Valid Values**:
- `"chora-base-root"` - The chora-base repository itself
- `"chora-base-project"` - A project created from chora-base
- `"chora-base-fork"` - A fork of chora-base (future use)

**Example**:
```yaml
project_type: "chora-base-project"
```

**Usage**: Determines merge behavior and validation rules

---

## Structure Classification

### `structure_only`

**Type**: Array of strings (file paths or glob patterns)
**Required**: Yes
**Description**: Files that should always be merged from upstream

**Syntax**:
- Exact paths: `scripts/install-sap.py`
- Glob patterns: `docs/skilled-awareness/sap-framework/**`
- Wildcards: `*.md`, `**/*.py`

**Example**:
```yaml
structure_only:
  # Core protocols and standards
  - SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
  - DOCUMENTATION_STANDARD.md

  # SAP Framework (always from upstream)
  - docs/skilled-awareness/sap-framework/**

  # Automation tooling
  - scripts/merge-upstream-structure.py
  - scripts/install-sap.py

  # Configuration templates
  - .github/workflows/test.yml
  - .github/workflows/lint.yml

  # Static template structure
  - static-template/.github/**
  - static-template/justfile
```

**Rules**:
1. Files must not contain project-specific content
2. Safe to overwrite with upstream version
3. Changes are improvements, not customizations
4. Glob patterns match recursively

**What to Include**:
- ✅ Protocol specifications
- ✅ Standard documents
- ✅ Automation scripts
- ✅ CI/CD templates
- ✅ Framework files
- ✅ Configuration templates

**What NOT to Include**:
- ❌ Source code (`src/`, `tests/`)
- ❌ Project-specific documentation
- ❌ Secrets or credentials
- ❌ Custom configurations

---

### `content_only`

**Type**: Array of strings (file paths or glob patterns)
**Required**: Yes
**Description**: Files that should never be merged from upstream

**Syntax**: Same as `structure_only`

**Example**:
```yaml
content_only:
  # Source code (always project-specific)
  - src/**
  - tests/**

  # Project-specific SAPs
  - docs/skilled-awareness/my-project/**
  - docs/skilled-awareness/testing-framework/**

  # Version control
  - .git/**
  - .gitignore

  # Environment and secrets
  - .env
  - .env.*
  - "*.local"

  # Build artifacts
  - dist/**
  - build/**
  - "*.egg-info"
  - __pycache__/**

  # IDE and editor
  - .vscode/**
  - .idea/**
  - .DS_Store
```

**Rules**:
1. Never merged from upstream
2. Complete project control
3. Contains unique implementations
4. Protected from accidental overwrites

**What to Include**:
- ✅ Source code
- ✅ Tests
- ✅ Project-specific documentation
- ✅ Custom configurations
- ✅ Secrets and environment files
- ✅ Build artifacts
- ✅ IDE settings

---

### `hybrid`

**Type**: Object mapping file paths to merge configurations
**Required**: No (but recommended for common hybrid files)
**Description**: Files requiring intelligent merge strategies

**Structure**:
```yaml
hybrid:
  <file_path>:
    description: "Human-readable description"
    merge_strategy: "<strategy_name>"
    # Strategy-specific configuration
```

**Supported Merge Strategies**:

#### 1. `section-by-section`

Merges files by section headers, preserving some sections and merging others.

**Use Case**: AGENTS.md, CLAUDE.md

**Configuration**:
```yaml
AGENTS.md:
  description: "Root agent awareness file"
  merge_strategy: "section-by-section"
  structure_markers:
    - "^## [A-Z]"        # Level 2 headers
    - "^### [A-Z]"       # Level 3 headers
  content_markers:
    - "^(?!##|###)"      # Non-header content
  preserve_sections:
    - "Project Overview"
    - "Common Tasks"
    - "Custom Capabilities"
  merge_sections:
    - "Project Structure"
    - "Development Process"
    - "SAP Framework"
```

**Algorithm**:
1. Parse both current and upstream into sections
2. Keep `preserve_sections` from current
3. Take `merge_sections` from upstream
4. Maintain section order from current

#### 2. `template-variables`

Preserves project-specific variables while updating template structure.

**Use Case**: README.md

**Configuration**:
```yaml
README.md:
  description: "Project README"
  merge_strategy: "template-variables"
  structure_markers:
    - "^## [A-Z]"
    - "badges_section: .*shields\\.io"
  content_markers:
    - "project_name"
    - "project_description"
  template_variables:
    project_name: "{{ PROJECT_NAME }}"
    project_description: "{{ PROJECT_DESCRIPTION }}"
    repository_url: "{{ REPOSITORY_URL }}"
  preserve_sections:
    - "Overview"
    - "Features"
```

**Algorithm**:
1. Extract variable values from current
2. Get upstream template
3. Replace `{{ VARIABLE }}` with current values
4. Preserve specified sections

#### 3. `table-rows`

Merges markdown tables by rows, preserving project-specific rows.

**Use Case**: docs/skilled-awareness/INDEX.md

**Configuration**:
```yaml
docs/skilled-awareness/INDEX.md:
  description: "SAP index"
  merge_strategy: "table-rows"
  structure_markers:
    - "^| SAP ID"
    - "^\\|---"
  content_markers:
    - "^| SAP-[0-9]"
  preserve_rows:
    - "SAP-000"  # Framework SAP (merge from upstream)
  merge_rows:
    - "SAP-000"
  project_specific_rows:
    - "SAP-001"
    - "SAP-002"
    # ... all project SAPs
```

**Algorithm**:
1. Parse tables into rows by SAP ID
2. Update `preserve_rows` from upstream
3. Keep `project_specific_rows` from current
4. Maintain table formatting

#### 4. `append-only`

Never overwrites content, only appends new content.

**Use Case**: CHANGELOG.md

**Configuration**:
```yaml
CHANGELOG.md:
  description: "Changelog"
  merge_strategy: "append-only"
  structure_markers:
    - "^## \\[.*\\]"     # Version headers
    - "^### Added"
  content_markers:
    - "^- "              # Changelog entries
  preserve_all_content: true
```

**Algorithm**:
1. Keep all current content
2. Append new upstream entries
3. Never remove or modify existing entries

#### 5. `manual`

Requires manual merge, no automation.

**Use Case**: ROADMAP.md (too project-specific)

**Configuration**:
```yaml
ROADMAP.md:
  description: "Project roadmap"
  merge_strategy: "manual"
  require_manual_merge: true
```

**Algorithm**:
1. Skip automated merge
2. Report to user for manual resolution
3. Provide conflict markers if needed

---

## Metadata Fields

### `customizations`

**Type**: Array of objects
**Required**: No
**Description**: Tracks what the project has customized

**Structure**:
```yaml
customizations:
  - file: "<file_path>"
    sections: []           # List of customized sections (for hybrid files)
    variables: {}          # Map of customized variables
    last_modified: "YYYY-MM-DD"
    notes: "Optional description"
```

**Example**:
```yaml
customizations:
  - file: "AGENTS.md"
    sections:
      - "Project Overview"
      - "Common Tasks"
    last_modified: "2025-10-29"

  - file: "README.md"
    variables:
      project_name: "my-awesome-project"
      project_description: "A revolutionary AI tool"
    last_modified: "2025-10-29"
```

**Usage**:
- Helps track what's been changed
- Useful for merge conflict resolution
- Documentation of customization history

---

### `merge`

**Type**: Object
**Required**: Yes
**Description**: Configuration for upstream merge behavior

**Structure**:
```yaml
merge:
  upstream_remote: "chora-base"
  upstream_url: "https://github.com/liminalcommons/chora-base.git"
  upstream_branch: "main"

  backup_before_merge: true
  backup_location: ".chora-backup-{timestamp}"

  conflict_strategy: "manual"  # manual | auto | abort
  conflict_markers: true

  validate_after_merge: true
  validation_commands:
    - "ruff check ."
    - "mypy src"
    - "pytest tests/ -x"
```

**Fields**:

#### `upstream_remote`
Remote name for upstream repository (default: `"chora-base"`)

#### `upstream_url`
Git URL for upstream repository

#### `upstream_branch`
Branch to merge from (default: `"main"`)

#### `backup_before_merge`
Whether to create backup before merge (recommended: `true`)

#### `backup_location`
Backup directory template (`{timestamp}` replaced with current time)

#### `conflict_strategy`
How to handle conflicts:
- `"manual"` - Stop and require user resolution
- `"auto"` - Attempt automatic resolution
- `"abort"` - Abort on any conflict

#### `conflict_markers`
Whether to add Git conflict markers (recommended: `true`)

#### `validate_after_merge`
Whether to run validation after merge (recommended: `true`)

#### `validation_commands`
List of commands to run for validation

---

### `migration`

**Type**: Object
**Required**: No
**Description**: Tracks migration history between versions

**Structure**:
```yaml
migration:
  from_version: "4.0.0"
  to_version: "4.1.0"
  migration_date: "2025-10-29"
  notes:
    - "Added .chorabase metadata"
    - "Implemented hybrid file merging"
```

**Usage**:
- Track version upgrades
- Document breaking changes
- Historical record of migrations

---

## Complete Example

### Example 1: chora-base Root Project

```yaml
# .chorabase for chora-base itself
version: "4.1.0"
structural_version: "4.1.0"
created: "2025-10-29"
project_type: "chora-base-root"

structure_only:
  - SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
  - DOCUMENTATION_STANDARD.md
  - docs/skilled-awareness/sap-framework/**
  - scripts/*.py
  - scripts/*.sh
  - static-template/**

content_only:
  - src/**
  - tests/**
  - docs/skilled-awareness/inbox/**
  - docs/skilled-awareness/chora-base/**
  - .git/**
  - .env*

hybrid:
  AGENTS.md:
    merge_strategy: "section-by-section"
    preserve_sections:
      - "Project Overview"
    merge_sections:
      - "Project Structure"

merge:
  upstream_remote: "origin"
  upstream_url: "https://github.com/liminalcommons/chora-base.git"
  upstream_branch: "main"
  validate_after_merge: true
  validation_commands:
    - "ruff check ."
    - "pytest tests/"
```

### Example 2: Generated Project

```yaml
# .chorabase for a project created from chora-base
version: "4.1.0"
structural_version: "4.1.0"
created: "2025-11-01"
project_type: "chora-base-project"
project_name: "my-mcp-server"

structure_only:
  - SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
  - docs/skilled-awareness/sap-framework/**
  - scripts/install-sap.py
  - .github/workflows/**

content_only:
  - src/**
  - tests/**
  - docs/skilled-awareness/my-mcp-server/**
  - .env*

hybrid:
  AGENTS.md:
    merge_strategy: "section-by-section"
    preserve_sections:
      - "Project Overview"
      - "MCP Server Details"
  README.md:
    merge_strategy: "template-variables"
    template_variables:
      project_name: "my-mcp-server"
      project_description: "An MCP server for data analysis"

customizations:
  - file: "README.md"
    variables:
      project_name: "my-mcp-server"
    last_modified: "2025-11-01"

merge:
  upstream_remote: "chora-base"
  upstream_url: "https://github.com/liminalcommons/chora-base.git"
  upstream_branch: "main"
  validate_after_merge: true
  validation_commands:
    - "ruff check src/"
    - "pytest tests/"
```

---

## Validation Rules

### Required Fields

Must be present:
- `version`
- `structural_version`
- `created`
- `project_type`
- `structure_only` (can be empty list)
- `content_only` (can be empty list)
- `merge.upstream_remote`
- `merge.upstream_url`

### Semantic Rules

1. **No Overlap**: A file cannot be in both `structure_only` and `content_only`
2. **Hybrid Explicit**: Hybrid files must be defined in `hybrid`, not in structure/content
3. **Valid Patterns**: Glob patterns must be valid
4. **Semver Versions**: `version` and `structural_version` must be valid semver
5. **Date Format**: `created` must be ISO 8601 (YYYY-MM-DD)

### Validation Command

```bash
# Future: Automated validation
python scripts/validate-chorabase.py .chorabase
```

---

## Migration Guide

### From No `.chorabase` (v3.x → v4.0)

1. Create `.chorabase` in repository root
2. Classify existing files into categories
3. Define hybrid merge strategies
4. Test merge in dry-run mode

### From v1.0 → v2.0 (Future)

Breaking changes will be documented with migration scripts.

---

## Best Practices

### 1. Default to Content

When unsure, add to `content_only`. It's safer to preserve than overwrite.

### 2. Document Customizations

Track all customizations in the `customizations` field.

### 3. Test Merge First

Always run `--dry-run` before actual merge.

### 4. Version Carefully

Bump `structural_version` major when boundaries change significantly.

### 5. Regular Updates

Merge from upstream regularly to avoid large divergence.

---

## Troubleshooting

### Problem: File in wrong category

**Symptom**: File gets overwritten or not merged when expected

**Solution**: Check `.chorabase`, move file to correct category

### Problem: Hybrid merge not working

**Symptom**: Manual merge required for file that should be automated

**Solution**: Check `hybrid` configuration, ensure merge strategy is correct

### Problem: Validation fails

**Symptom**: `.chorabase` not recognized by merge script

**Solution**: Run validation, check YAML syntax, ensure required fields present

---

## Related Documentation

- [How to: Upgrade Structure from Upstream](../how-to/upgrade-structure-from-upstream.md)
- [Explanation: Structure vs Content Model](../explanation/structure-vs-content-model.md)
- [Merge Scripts](../../../scripts/) - Implementation of merge logic

---

**Specification Version**: 1.0
**Last Updated**: 2025-10-29
**Maintained By**: chora-base core team
