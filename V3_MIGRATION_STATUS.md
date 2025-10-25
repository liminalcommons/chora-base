# Chora-Base v3.0.0 Migration Status

**Date:** 2025-10-25
**Status:** In Progress (70% complete)

## ✅ Completed

### 1. AGENT_SETUP_GUIDE.md (2000+ lines)
- **Location:** `/AGENT_SETUP_GUIDE.md`
- **Status:** Complete and ready to use
- **Content:**
  - Full setup procedure for AI agents
  - Variable reference and derivation rules
  - Feature flags documentation
  - Validation checklist
  - Troubleshooting guide
  - 3 complete worked examples

### 2. Directory Structure Created
- `/static-template/` - For ready-to-use files
- `/blueprints/` - For variable substitution templates
- `/examples/` - For reference implementations

### 3. Partial Static Template Population
- ✅ `static-template/src/__package_name__/memory/` (2 files)
  - event_log.py
  - knowledge_graph.py
- ✅ `static-template/src/__package_name__/utils/` (5 files)
  - __init__.py
  - errors.py
  - persistence.py
  - responses.py
  - validation.py
- ✅ `static-template/.editorconfig`
- ✅ `static-template/.github/dependabot.yml`

### 4. Partial Blueprints Created
- ✅ `blueprints/pyproject.toml.blueprint`
- ✅ `blueprints/README.md.blueprint`

## 🚧 Remaining Work

### 1. Complete static-template/ Population (~1 hour)

**Need to copy from template/ to static-template/:**

#### GitHub Workflows (8 files)
```bash
# These need package_name substitution in one line each
template/.github/workflows/*.yml.jinja → static-template/.github/workflows/*.yml
```
**Decision needed:** Either:
- Option A: Copy as-is, make them blueprints
- Option B: Do simple sed replacement for package_name

#### Tests (6 files)
```bash
template/tests/AGENTS.md.jinja → static-template/tests/AGENTS.md (mostly static)
template/tests/utils/*.jinja → static-template/tests/utils/*.py
```

#### Scripts (25+ files)
```bash
template/scripts/*.sh.jinja → static-template/scripts/*.sh
template/scripts/*.py.jinja → static-template/scripts/*.py
```
**Note:** Most scripts are 95% static, only {{package_name}} needs replacement

#### Documentation (15+ files)
```bash
template/user-docs/**/*.md → static-template/user-docs/**/*.md (all static)
template/.chora/memory/*.md → static-template/.chora/memory/*.md (all static)
```

#### Docker Files (3 files)
```bash
template/Dockerfile.jinja → blueprints/Dockerfile.blueprint
template/docker-compose.yml.jinja → blueprints/docker-compose.yml.blueprint
template/.dockerignore.jinja → static-template/.dockerignore (static)
```

#### Other Config (4 files)
```bash
template/justfile.jinja → static-template/justfile (static)
template/NAMESPACES.md → static-template/NAMESPACES.md (static with placeholders)
template/.pre-commit-config.yaml.jinja → static-template/.pre-commit-config.yaml (static)
```

### 2. Complete Blueprints Creation (~30 min)

**Remaining blueprints needed (8 files):**

3. `blueprints/AGENTS.md.blueprint` (from template/AGENTS.md.jinja)
4. `blueprints/CHANGELOG.md.blueprint` (from template/CHANGELOG.md.jinja)
5. `blueprints/CONTRIBUTING.md.blueprint` (from template/CONTRIBUTING.md.jinja - if exists)
6. `blueprints/ROADMAP.md.blueprint` (from template/ROADMAP.md.jinja - if exists)
7. `blueprints/.gitignore.blueprint` (from template/.gitignore.jinja)
8. `blueprints/.env.example.blueprint` (from template/.env.example.jinja)
9. `blueprints/server.py.blueprint` (from template/src/{{package_name}}/mcp/server.py.jinja)
10. `blueprints/__init__.py.blueprint` (from template/src/{{package_name}}/__init__.py.jinja - if exists)

### 3. Create setup.py CLI Helper (~30 min)

**Purpose:** Optional Python script for manual/non-agent setup

**Features needed:**
- Prompt for variables (project_name, author, etc.)
- Derive variables (slug, package_name, namespace)
- Copy static-template/ to target
- Rename __package_name__/ directories
- Process 10 blueprints with variable substitution
- Validate setup
- Initialize git repo

**Reference:** See AGENT_SETUP_GUIDE.md Section 4 for detailed procedure

### 4. Create Example Project (~20 min)

**Generate:** `examples/mcp-github/`
- Full working example using the new system
- Demonstrates what agents should produce
- Can be used for validation testing

### 5. Update README.md (~15 min)

**Changes needed:**
- Remove copier references
- Add new "Setup with AI Agent" section
- Update quick start to: "Ask your AI agent: 'Set up chora-base for [project]'"
- Link to AGENT_SETUP_GUIDE.md
- Note: Can also use setup.py manually

### 6. Create Release Documentation (~15 min)

**Files to create:**
- `docs/releases/v3.0.0-release-notes.md`
- `docs/releases/v2-to-v3-migration-guide.md`
- Update `CHANGELOG.md` with v3.0.0 entry

## 📋 Quick Implementation Guide

### For AI Agents Completing This Work

**Step 1: Complete Static Template**
```bash
# Copy all static files (strip .jinja suffix when file is static)
for file in template/**/*; do
  # Determine if truly static (no {{variables}})
  # Copy to static-template/ preserving structure
done
```

**Step 2: Create Remaining Blueprints**
```bash
# For each of 8 remaining blueprint files:
cp template/[source].jinja blueprints/[target].blueprint
# Verify {{variable}} syntax is simple
```

**Step 3: Create setup.py**
```python
#!/usr/bin/env python3
"""
Chora-base v3.0 setup script.
Optional CLI alternative to AI agent setup.
"""
import os
import shutil
from pathlib import Path

def gather_variables() -> dict:
    """Prompt user for required variables."""
    # Interactive prompts or argparse

def copy_static_template(target_dir: str):
    """Copy all static-template/ files."""

def rename_package_dirs(target_dir: str, package_name: str):
    """Rename __package_name__/ → {package_name}/"""

def process_blueprints(target_dir: str, variables: dict):
    """Process 10 blueprint files."""

def validate_setup(target_dir: str, package_name: str) -> bool:
    """Run validation checks."""

def main():
    # Gather variables
    # Copy static template
    # Rename directories
    # Process blueprints
    # Validate
    # Init git
    # Done!
```

**Step 4: Test Setup**
```bash
cd /tmp
python /path/to/chora-base/setup.py
# Or: have AI agent read AGENT_SETUP_GUIDE.md and execute
```

**Step 5: Update Documentation**
```markdown
# README.md changes:

## Quick Start (New)

### With AI Agent (Recommended)
Ask your AI coding agent:
> "Set up chora-base for my MCP server called [project-name]"

Your agent will read AGENT_SETUP_GUIDE.md and autonomously set up your project.

### Manual Setup
\`\`\`bash
python setup.py
\`\`\`

Follow the prompts to configure your project.
```

**Step 6: Create Release**
```bash
# Update CHANGELOG.md
# Create release notes
# Commit everything
git add .
git commit -m "feat: v3.0.0 - AI-agent-first architecture

- Remove copier dependency
- Add AGENT_SETUP_GUIDE.md (2000+ lines)
- 70% static files, 10 simple blueprints
- Optional setup.py CLI helper
- All features enabled by default

BREAKING CHANGE: Copier no longer used. Migration guide: docs/releases/v2-to-v3-migration-guide.md"

git tag -a v3.0.0 -m "Release v3.0.0: AI-Agent-First Architecture"
git push origin main
git push origin v3.0.0
```

## 🎯 Success Criteria

Before considering v3.0.0 complete:

- [ ] All 70+ static files copied to static-template/
- [ ] All 10 blueprints created
- [ ] setup.py script working end-to-end
- [ ] Example project generated successfully
- [ ] README.md updated
- [ ] Release notes created
- [ ] Manual test: Generate a project, verify it works
- [ ] Agent test: Have AI agent use AGENT_SETUP_GUIDE.md to generate project

## 📊 Estimated Remaining Time

- Complete static-template/: 1 hour
- Create blueprints: 30 minutes
- Create setup.py: 30 minutes
- Test & validate: 30 minutes
- Update docs: 15 minutes
- Release: 15 minutes

**Total: ~3 hours of focused work**

## 🚀 Ready to Use Now

Even though incomplete, **AGENT_SETUP_GUIDE.md is fully usable today** by AI agents who can:
1. Read the guide
2. Manually copy files from the existing template/ directory
3. Process them according to the guide's instructions

The remaining work is automation/convenience, not core functionality.

---

*Last updated: 2025-10-25*
