# Getting Started with chora-base Template

**chora-base** is a Copier-based project template for creating Python projects with Skilled Awareness Packages (SAPs). Generate production-ready projects with inbox workflows, task management, conflict resolution, and more—in under 5 minutes.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Template Modes](#template-modes)
- [SAP Selection Guide](#sap-selection-guide)
- [Post-Generation](#post-generation)
- [Updating Projects](#updating-projects)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## Prerequisites

**Required:**
- Python 3.8+ (3.11+ recommended)
- [Copier](https://copier.readthedocs.io/) 9.x+: `pip install copier`
- Git

**Optional** (depending on SAP selection):
- [Poetry](https://python-poetry.org/) (Python dependency management): `curl -sSL https://install.python-poetry.org | python3 -`
- [Beads CLI](https://github.com/chora-ecosystem/beads) (task management): `pip install beads-cli`
- [Just](https://github.com/casey/just) (task runner): `brew install just` (macOS) or [see install docs](https://github.com/casey/just#installation)

**Verify installation:**
```bash
copier --version      # Should show 9.x or higher
python --version      # Should show 3.8 or higher
git --version         # Any recent version
```

---

## Quick Start

### 1. Create a New Project

```bash
copier copy gh:liminalcommons/chora-base my-project
```

You'll be prompted for:
- **Project name** (e.g., `my-chora-project`)
- **Description** (brief project summary)
- **Author** (your name)
- **SAP selection mode** (see [Template Modes](#template-modes))
- **Python version** (3.8-3.12, default: 3.11)
- **Git initialization** (recommended: Yes)
- **Poetry usage** (if Python scripts selected)

**Example:**
```bash
$ copier copy gh:liminalcommons/chora-base my-project

🎤 Project name (lowercase, hyphenated): my-chora-project
🎤 Brief project description: A chora-based project for X
🎤 Project author/maintainer: Alice Smith
🎤 SAP selection mode:
  1. Minimal (2 SAPs - Quick start)
  2. Standard (4 SAPs - Recommended)  ← Select this
  3. Comprehensive (8 SAPs - Full suite)
  4. Custom (Choose individual SAPs)
Choice [2]: 2
🎤 Python version:
  1. Python 3.11  ← Default
  2. Python 3.12
Choice [1]: 1
🎤 Initialize git repository? [Y/n]: Y
🎤 Use Poetry for dependency management? [Y/n]: Y

✅ PROJECT GENERATED SUCCESSFULLY
```

### 2. Navigate and Install

```bash
cd my-project
poetry install        # Install dependencies
poetry shell          # Activate virtual environment
just --list           # See available automation recipes
```

### 3. Verify Setup

```bash
# Check git repository
git status

# Check available automation
just --list

# Test SAP features (if included)
just inbox-status           # SAP-001: Check inbox
bd list                     # SAP-015: List beads tasks
just conflict-check         # SAP-053: Check for conflicts
```

---

## Template Modes

### Minimal Mode (2 SAPs)
**Use case:** Quick prototypes, simple projects

**Includes:**
- ✅ SAP-001: Inbox Workflow (coordination requests)
- ✅ SAP-015: Beads Task Management (git-backed tasks)

**Setup time:** ~2 minutes
**Recommended for:** Individual developers, prototypes

### Standard Mode (4 SAPs) ⭐ Recommended
**Use case:** Team projects, production applications

**Includes:**
- ✅ All Minimal SAPs
- ✅ SAP-053: Conflict Resolution (pre-merge conflict detection)
- ✅ SAP-010: Memory System (event logs, knowledge notes)

**Setup time:** ~3 minutes
**Recommended for:** Most projects, team collaboration

### Comprehensive Mode (8 SAPs)
**Use case:** Enterprise projects, research labs

**Includes:**
- ✅ All Standard SAPs
- ✅ SAP-051: Pre-merge Validation (git hooks)
- ✅ SAP-052: Code Ownership (CODEOWNERS, reviewer suggestions)
- ✅ SAP-056: Lifecycle Traceability (feature manifest)
- ✅ SAP-008: Automation Dashboard (metrics tracking)

**Setup time:** ~5 minutes
**Recommended for:** Large teams, complex projects

### Custom Mode
**Use case:** Specific needs, gradual SAP adoption

**Includes:** Choose individual SAPs from questionnaire
**Setup time:** ~3-5 minutes (depends on selection)
**Recommended for:** Experienced users, specific use cases

---

## SAP Selection Guide

### SAP-001: Inbox Workflow (P0 - Always included)
**What it does:** Coordination request management, cross-project communication
**Use when:** Working across multiple repos, managing dependencies
**Files created:** `inbox/`, coordination templates

### SAP-015: Beads Task Management (P0 - Always included)
**What it does:** Git-backed issue tracking, local task management
**Use when:** Tracking implementation tasks without external tools
**Files created:** `.beads/`, beads configuration

### SAP-053: Conflict Resolution (P1 - Standard+)
**What it does:** Pre-merge conflict detection, resolution strategies
**Use when:** 2+ developers, frequent merges
**Files created:** `scripts/conflict-checker.py`, conflict resolution justfile recipes

### SAP-010: Memory System (P1 - Standard+)
**What it does:** Event logging, knowledge notes, agent awareness
**Use when:** Working with AI assistants (Claude, GPT), documenting patterns
**Files created:** `.chora/memory/events/`, `.chora/memory/knowledge/notes/`, `.chora/CLAUDE.md`

### SAP-051: Pre-merge Validation (P2 - Comprehensive)
**What it does:** Git hooks for automated pre-push checks
**Use when:** Enforcing code quality, preventing broken builds
**Files created:** `scripts/pre-push-check.sh`, hook installation recipes

### SAP-052: Code Ownership (P2 - Comprehensive)
**What it does:** CODEOWNERS file, PR reviewer suggestions
**Use when:** Team has domain experts, clear code ownership
**Files created:** `scripts/ownership-coverage.py`, `CODEOWNERS`

### SAP-056: Lifecycle Traceability (P2 - Comprehensive)
**What it does:** Feature manifest, artifact linkage (code→tests→docs)
**Use when:** Complex projects, audit requirements, traceability needs
**Files created:** `scripts/validate-manifest.py`, `feature-manifest.yaml`

### SAP-008: Automation Dashboard (P2 - Comprehensive)
**What it does:** Recipe usage tracking, automation metrics
**Use when:** Measuring automation ROI, optimizing workflows
**Files created:** Metrics-enhanced justfile recipes

---

## Post-Generation

After generation, your project includes:

### Directory Structure
```
my-project/
├── .beads/                     # SAP-015: Beads tasks
├── .chora/                     # SAP-010: Memory system
│   ├── CLAUDE.md               # Agent awareness guide
│   └── memory/
│       ├── events/             # Event logs (A-MEM)
│       └── knowledge/notes/    # Knowledge notes
├── inbox/                      # SAP-001: Coordination
│   ├── incoming/               # New requests
│   ├── active/                 # In-progress work
│   ├── completed/              # Finished work
│   └── templates/              # Request templates
├── scripts/                    # SAP automation scripts
│   ├── conflict-checker.py     # SAP-053 (if included)
│   ├── ownership-coverage.py   # SAP-052 (if included)
│   ├── validate-manifest.py    # SAP-056 (if included)
│   └── pre-push-check.sh       # SAP-051 (if included)
├── docs/                       # Documentation
│   └── GETTING-STARTED.md      # This file
├── README.md                   # Project overview
├── justfile                    # Automation recipes
├── pyproject.toml              # Python config (if applicable)
└── .copier-answers.yml         # Template configuration
```

### Next Steps

1. **Review generated files:**
   ```bash
   cat README.md
   just --list
   ```

2. **Set up development environment:**
   ```bash
   poetry install              # Install dependencies
   poetry shell                # Activate virtual environment
   ```

3. **Initialize workflows** (if using SAP-001):
   ```bash
   just inbox-status           # Check coordination inbox
   ```

4. **Create first task** (if using SAP-015):
   ```bash
   bd create "Set up CI/CD pipeline"
   bd list
   ```

5. **Test automation:**
   ```bash
   just validate               # Run validation checks
   just conflict-check         # Check for conflicts (SAP-053)
   ```

6. **Read domain-specific docs:**
   - `README.md`: Project overview
   - `inbox/README.md`: Coordination workflow (SAP-001)
   - `.chora/CLAUDE.md`: Agent awareness guide (SAP-010)
   - `docs/GETTING-STARTED.md`: This file

---

## Updating Projects

When the chora-base template improves (v1.0.0 → v1.1.0 → v2.0.0), propagate updates to your project:

### Update Command

```bash
cd my-project
copier update
```

### What Gets Updated

- Template files (justfile, scripts, docs)
- SAP artifacts (if you selected them)
- Configuration (pyproject.toml, .copier-answers.yml)

### What's Preserved

- Your custom code
- Project-specific configuration
- Git history
- Local modifications

### Handling Conflicts

If `copier update` produces merge conflicts:

1. **Review conflicts:**
   ```bash
   git status                  # List conflicted files
   git diff                    # Review changes
   ```

2. **Resolve manually:**
   - Open conflicted files in editor
   - Choose between template changes (`<<<<<<< HEAD`) and your changes (`>>>>>>> template`)
   - Keep both if needed

3. **Test after resolution:**
   ```bash
   just validate               # Ensure project still works
   just conflict-check         # Check for remaining conflicts
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "chore: update to chora-base v1.1.0"
   ```

### Update Frequency

**Recommended:**
- **Minor updates** (v1.0.0 → v1.1.0): Every 1-3 months
- **Major updates** (v1.x → v2.0): Review changelog, test in branch first
- **Patch updates** (v1.0.0 → v1.0.1): Optional, bug fixes only

---

## Troubleshooting

### Issue: `copier: command not found`

**Solution:**
```bash
pip install copier
# OR
pipx install copier
```

### Issue: Template generation fails with "Unknown filter"

**Solution:** Update Copier to 9.x+:
```bash
pip install --upgrade copier
copier --version  # Should show 9.x or higher
```

### Issue: Poetry not found

**Solution:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
# OR (macOS)
brew install poetry
```

### Issue: Git repository not initialized

**Solution:**
```bash
cd my-project
git init
git add .
git commit -m "Initial commit from chora-base template"
```

### Issue: Beads CLI not found (if SAP-015 selected)

**Solution:**
```bash
pip install beads-cli
# OR add to pyproject.toml and run poetry install
```

### Issue: `just: command not found`

**Solution:**
```bash
# macOS
brew install just

# Linux
cargo install just
# OR
wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | sudo tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null
echo "deb [signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | sudo tee /etc/apt/sources.list.d/prebuilt-mpr.list
sudo apt update
sudo apt install just

# Windows
scoop install just
# OR
choco install just
```

### Issue: Python version mismatch

**Solution:** Use pyenv to install the correct Python version:
```bash
pyenv install 3.11.5
pyenv local 3.11.5
python --version  # Should show 3.11.5
```

### Issue: Template generates empty files

**Cause:** Likely a conditional logic issue
**Solution:** Check `.copier-answers.yml` for correct SAP selection:
```yaml
sap_selection_mode: standard
include_sap_053: true
include_sap_010: true
```

### Issue: `copier update` fails with conflicts

**Solution:** Use `-f` flag to force update (overwrites local changes):
```bash
copier update -f  # ⚠️ WARNING: Overwrites local changes
```

---

## Examples

### Example 1: Minimal Project (Quick Prototype)

```bash
copier copy gh:liminalcommons/chora-base quick-prototype \
  --data project_name=quick-prototype \
  --data project_description="Quick prototype for X" \
  --data project_author="Alice" \
  --data sap_selection_mode=minimal \
  --data use_git=true
```

**Result:** 2 SAPs (001, 015), ~2 min setup

### Example 2: Standard Project (Recommended)

```bash
copier copy gh:liminalcommons/chora-base my-team-project \
  --data project_name=my-team-project \
  --data project_description="Team project with collaboration features" \
  --data project_author="Team Lead" \
  --data sap_selection_mode=standard \
  --data python_version=3.11 \
  --data use_git=true \
  --data use_poetry=true
```

**Result:** 4 SAPs (001, 015, 053, 010), ~3 min setup

### Example 3: Comprehensive Project (Enterprise)

```bash
copier copy gh:liminalcommons/chora-base enterprise-project \
  --data project_name=enterprise-project \
  --data project_description="Enterprise project with full SAP suite" \
  --data project_author="Enterprise Team" \
  --data sap_selection_mode=comprehensive \
  --data python_version=3.12 \
  --data use_git=true \
  --data use_poetry=true
```

**Result:** 8 SAPs (full suite), ~5 min setup

### Example 4: Custom SAP Selection

```bash
# Generate project with custom SAP selection (interactive)
copier copy gh:liminalcommons/chora-base custom-project

# When prompted:
# sap_selection_mode: custom
# include_sap_001: yes  ← Inbox
# include_sap_015: yes  ← Beads
# include_sap_053: yes  ← Conflict Resolution
# include_sap_010: no   ← Skip Memory System
# include_sap_051: no   ← Skip Pre-merge Validation
# include_sap_052: yes  ← Code Ownership
# include_sap_056: no   ← Skip Traceability
# include_sap_008: no   ← Skip Automation Dashboard
```

**Result:** 4 SAPs (001, 015, 053, 052), ~3 min setup

---

## Additional Resources

- **Template Repository:** https://github.com/liminalcommons/chora-base
- **Copier Documentation:** https://copier.readthedocs.io/
- **SAP Catalog:** `docs/skilled-awareness/INDEX.md` (in template)
- **Issue Tracker:** https://github.com/liminalcommons/chora-base/issues

---

## Version History

- **v1.0.0** (2025-11-20): Initial production release
  - 8 SAPs integrated
  - 3 selection modes (minimal, standard, comprehensive)
  - Copier-based distribution
  - Template update support

---

**Created:** 2025-11-20
**Template Version:** chora-base v1.0.0
**Origin:** OPP-2025-022, CORD-2025-023, SAP-060
