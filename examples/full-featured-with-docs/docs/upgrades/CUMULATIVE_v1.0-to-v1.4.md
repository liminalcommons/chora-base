# Upgrading from v1.0.0 to v1.4.0 (Cumulative)

**Release Date**: Multi-version jump (v1.0.0 → v1.4.0)
**Template Versions**: v1.0.0 → v1.1.0 → v1.2.0 → v1.3.0 → v1.4.0
**Upgrade Effort**: 4-6 hours (vs 6-9.5 hours incremental)
**For**: Original adopters, multi-version jumps

---

## Quick Assessment

| Aspect | Value |
|--------|-------|
| **Effort** | 4-6 hours (cumulative), 6-9.5 hours (incremental) |
| **Savings** | 30-40% time saved vs incremental |
| **Breaking Changes** | No (all MINOR releases) |
| **Required For** | Critical fixes (v1.2.0 ImportError), ecosystem consistency |
| **Can Skip If** | Never (v1.2.0 fixes required for correctness) |
| **Displacement Risk** | HIGH (multiple workflow changes combined) |
| **Agent Autonomy** | 50% (complex multi-version decisions) |

---

## TL;DR

**What's New Across v1.0→v1.4**:
- **v1.1.0**: AGENTS.md enhancements (+645 lines), A-MEM workflows, Diátaxis docs
- **v1.2.0**: **CRITICAL** ImportError fixes, generalization fixes (hardcoded paths)
- **v1.3.0**: Vision framework (dev-docs/vision/, ROADMAP.md)
- **v1.4.0**: `just` as PRIMARY interface, PyPI auth choice

**Impact on Original Adopters**:
- **MUST upgrade to v1.2.0+**: Critical ImportError fixes (required for correctness)
- **SHOULD adopt v1.4.0**: Ecosystem consistency (`just --list` workflow)
- **Combined displacement**: Multiple workflow changes (task discovery, project planning, PyPI setup)

**Recommended Action**:
- **For all v1.0.0 projects**: Upgrade to v1.4.0 (critical fixes + ecosystem benefits)
- **Strategy**: Cumulative upgrade (30-40% faster than incremental)
- **Critical**: Apply v1.2.0 fixes first, then integrate v1.3/v1.4 features

---

## Decision Tree for AI Agents

```
START: Should I upgrade v1.0.0 → v1.4.0?

├─ Does project have ImportError issues with memory module?
│  ├─ YES → MUST upgrade to v1.2.0+ (critical fix)
│  └─ NO → Continue evaluation (but upgrade still recommended)
│
├─ Will project be maintained long-term?
│  ├─ NO → Defer upgrade (but note: v1.2.0 fixes still valuable)
│  └─ YES → Upgrade RECOMMENDED
│
├─ Working across multiple chora-base projects?
│  ├─ YES → STRONG recommend v1.4.0 (ecosystem consistency)
│  │         - just --list transfers knowledge to all projects
│  │         - Vision framework standardizes strategic planning
│  └─ NO → Evaluate features individually
│
├─ Choose upgrade strategy:
│  ├─ Cumulative (v1.0.0 → v1.4.0 direct):
│  │  - Best if: Need v1.4.0 quickly, can handle combined conflicts
│  │  - Effort: 4-6 hours
│  │  - Risk: HIGH (multiple conflicts at once)
│  │
│  ├─ Incremental (v1.0→v1.1→v1.2→v1.3→v1.4):
│  │  - Best if: Want to validate each step, heavy customizations
│  │  - Effort: 6-9.5 hours
│  │  - Risk: MEDIUM (conflicts spread out)
│  │
│  └─ Hybrid (v1.0→v1.2→v1.4):
│     - Best if: Need critical fixes fast, can skip v1.3
│     - Effort: 2-4 hours
│     - Risk: MEDIUM (two jumps with critical path)

END: RECOMMENDED for all projects (v1.2.0 fixes required)
```

**Decision Matrix**:

| Project Type | v1.0→v1.4 Cumulative | v1.0→v1.1→v1.2→v1.3→v1.4 Incremental | v1.0→v1.2→v1.4 Hybrid |
|--------------|----------------------|--------------------------------------|------------------------|
| **With ImportErrors** | Required, cumulative fastest | Required, safest path | Required, balanced |
| **Multi-project agent** | Recommended (ecosystem) | Thorough but slow | Fast path to v1.4 |
| **Heavy customizations** | High conflict risk | Safer (conflicts isolated) | Moderate risk |
| **Time-constrained** | 4-6 hrs (fastest) | 6-9.5 hrs (slowest) | 2-4 hrs (balanced) |
| **Risk-averse** | Rollback loses all | Rollback one step | Rollback to v1.2 |

---

## What Changed (Cumulative Summary)

### Release-by-Release Overview

#### v1.0.0 → v1.1.0 (Documentation Enhancements)
**Effort**: 30 min | **Risk**: LOW | **Type**: Additive

**Files Modified**:
- `template/AGENTS.md.jinja`: +665 -20
  - A-MEM Integration (8-step learning loop)
  - Memory Troubleshooting (260 lines)
  - Agent Self-Service Workflows
  - Diátaxis Framework documentation

**Impact**: Pure documentation addition, zero conflicts expected

#### v1.1.0 → v1.2.0 (Critical Fixes) ⚠️
**Effort**: 1-2 hrs | **Risk**: HIGH | **Type**: Required

**Files Modified**:
- `template/src/{{ package_name }}/memory/__init__.py`: ImportError fixes
- `template/src/{{ package_name }}/memory/event_log.py`: Hardcoded paths
- `template/src/{{ package_name }}/memory/knowledge_graph.py`: Hardcoded names
- `template/src/{{ package_name }}/memory/trace.py`: Source field generalization
- `template/scripts/*.sh`: Path fixes

**Critical Changes**:
```python
# BEFORE (v1.1.0 - BROKEN)
from mcp_n8n.memory.event_log import EventLog
source: str = "mcp-n8n"

# AFTER (v1.2.0 - FIXED)
from {{ package_name }}.memory.event_log import EventLog
source: str = "{{ project_slug }}"
```

**Impact**: MUST upgrade (correctness issue), extensive conflicts if memory module customized

#### v1.2.0 → v1.3.0 (Vision Framework)
**Effort**: 2-3 hrs | **Risk**: MEDIUM | **Type**: Additive

**Files Added**:
- `template/dev-docs/vision/PRODUCT.md`
- `template/dev-docs/vision/TECHNICAL.md`
- `template/dev-docs/vision/TEAM.md`
- `template/ROADMAP.md.jinja`

**Files Modified**:
- `template/AGENTS.md.jinja`: +450 lines (Strategic Design section)
- `template/README.md.jinja`: Vision framework references

**Impact**: May conflict with existing roadmap/planning docs

#### v1.3.0 → v1.4.0 (just Workflow + PyPI Setup)
**Effort**: 2-3 hrs | **Risk**: MEDIUM | **Type**: Optional workflow

**Files Modified**:
- `template/justfile.jinja`: `just --list` as PRIMARY interface
- `template/AGENTS.md.jinja`: Task Discovery section updated
- `template/README.md.jinja`: `just` workflow prominence
- `template/.github/workflows/release.yml.jinja`: PyPI auth choice
- `template/PYPI_SETUP.md.jinja`: NEW (~420 lines)

**New Copier Prompts**:
- `pypi_auth_method`: token (default) vs trusted_publishing

**Impact**: Workflow displacement (task discovery method changes)

---

### Cumulative Changes (v1.0.0 → v1.4.0)

**Total Files Modified**: 20+ files
**Total Lines Added**: ~3,500 lines (net: ~2,800 after deletions)

**Critical Path Dependencies**:
1. **v1.2.0 fixes FIRST** (ImportError correction required)
2. **v1.3.0 vision** (depends on stable v1.2 foundation)
3. **v1.4.0 just** (depends on v1.3 AGENTS.md structure)

**Cannot skip v1.2.0** - critical fixes must be applied
**Can skip v1.3.0** - vision framework is additive (but recommended)
**Can skip v1.4.0** - workflow change is optional (but ecosystem consistency valuable)

---

## Displacement Analysis (Cumulative)

### Type 1: Required (Correctness Fixes)

#### v1.2.0: ImportError and Generalization Fixes

**What Fixed**:
- Memory module imports broken in v1.0-v1.1 (hardcoded package names)
- Script paths hardcoded to exemplar project structure
- Source fields using wrong project identifiers

**Benefits**:
- Project actually works correctly (critical)
- Memory system functional
- Scripts portable across projects

**Costs**:
- None (critical fix)

**Decision**: MUST adopt (required for correctness)

---

### Type 2: Optional (Workflow Improvements)

#### v1.4.0: just --list as Primary Interface

**What Changed**:
- Task discovery: `ls scripts/` → `just --list`
- Command catalog: README → machine-readable justfile
- Auto-installation of `just` in setup.sh

**Benefits**:
- Machine-readable task catalog
- Ecosystem consistency (works across all chora-base v1.4.0+ projects)
- Self-documenting commands with descriptions

**Costs**:
- New dependency (just)
- Learning curve (new syntax)
- Migration effort (update agent knowledge)

**Knowledge Migration**:
```json
// OLD (project-specific)
{
  "task": "run tests",
  "command": "./scripts/smoke-test.sh",
  "project": "my-project-v1.0"
}

// NEW (ecosystem-wide)
{
  "ecosystem": "chora-base",
  "task": "run tests",
  "command": "just test",
  "applies_to": "all chora-base v1.4.0+ projects"
}
```

**Decision Criteria**:
- Multi-project agents: ADOPT (knowledge transfers)
- Single-project: EVALUATE (benefits vs learning curve)
- Hybrid: Use both (`just test` OR `./scripts/smoke-test.sh`)

---

### Type 3: Additive (Safe Enhancements)

#### v1.1.0: AGENTS.md Memory Troubleshooting

**What Added**:
- A-MEM Integration (8-step learning loop)
- Memory Troubleshooting (260 lines self-service debugging)
- Agent Self-Service Workflows
- Diátaxis Framework navigation

**Benefits**:
- Agents can debug memory issues autonomously
- Structured learning loop documentation
- Better documentation navigation

**Costs**: None (pure addition)

**Decision**: Adopt if using memory system

#### v1.3.0: Vision & Strategic Design Framework

**What Added**:
- `dev-docs/vision/` (PRODUCT, TECHNICAL, TEAM)
- `ROADMAP.md` (strategic planning)
- AGENTS.md Strategic Design section

**Benefits**:
- Long-term vision documentation
- Structured strategic planning
- Agent-aware design decisions

**Costs**:
- May conflict with existing roadmap/planning docs
- Integration effort if you have existing vision docs

**Decision**: Adopt if using vision-driven development, integrate if conflicts

---

## Cumulative Upgrade Steps

### Prerequisites (20 minutes)

```bash
# 1. Ensure clean git state
git status
# Should show "nothing to commit, working tree clean"

# 2. Create comprehensive backup
git branch backup-pre-upgrade-v1.4.0-$(date +%Y%m%d)
git tag backup-v1.0.0

# 3. Review current template version
cat .copier-answers.yml | grep _commit
# Should show v1.0.0

# 4. Document customizations
# Review and update UPGRADING.md with all customized files
# This is CRITICAL for cumulative upgrade (many files will change)

# 5. Read upgrade guide for each version
# - v1.0-to-v1.1.md (understand AGENTS.md changes)
# - v1.1-to-v1.2.md (understand critical fixes)
# - v1.2-to-v1.3.md (understand vision framework)
# - v1.3-to-v1.4.md (understand just workflow)
```

### Strategy Decision (5 minutes)

**Choose your upgrade path**:

#### Option A: Cumulative (v1.0.0 → v1.4.0 direct) - RECOMMENDED
```bash
# Advantages:
# - Fastest: 4-6 hours total
# - One conflict resolution session
# - Immediate access to v1.4.0 features

# Disadvantages:
# - All conflicts at once (can be overwhelming)
# - Harder to isolate issues if something breaks
# - Rollback loses everything

# Best for:
# - Time-constrained projects
# - Minimal customizations
# - Confident with conflict resolution
```

#### Option B: Incremental (v1.0→v1.1→v1.2→v1.3→v1.4)
```bash
# Advantages:
# - Safest: Validate each step
# - Conflicts isolated per version
# - Easier rollback (one version at a time)

# Disadvantages:
# - Slowest: 6-9.5 hours total
# - Four separate conflict resolution sessions
# - Repetitive validation

# Best for:
# - Heavy customizations
# - Risk-averse projects
# - Learning upgrade process
```

#### Option C: Hybrid (v1.0→v1.2→v1.4)
```bash
# Advantages:
# - Balanced: 2-4 hours
# - Critical fixes first (v1.2.0)
# - Skip v1.3 vision if not needed

# Disadvantages:
# - Two jumps (still multiple conflicts)
# - May miss v1.1 AGENTS.md enhancements

# Best for:
# - Need critical fixes quickly
# - Don't use vision-driven development
# - Want ecosystem consistency (v1.4)
```

---

### Cumulative Upgrade Execution (4-6 hours)

#### Step 1: Prepare for Combined Changes (30 min)

```bash
# Review what will change across all versions
# Files that will be modified in v1.0→v1.4:
# - AGENTS.md (v1.1, v1.3, v1.4)
# - memory/* (v1.2 - CRITICAL)
# - dev-docs/vision/* (v1.3 - NEW)
# - ROADMAP.md (v1.3 - NEW)
# - justfile (v1.4)
# - README.md (v1.3, v1.4)
# - PYPI_SETUP.md (v1.4 - NEW)

# Check if you have customized these files
git diff v1.0.0 -- AGENTS.md README.md src/*/memory/ justfile
# Note any customizations found
```

#### Step 2: Execute Cumulative Upgrade (1-2 hours)

```bash
# Run copier update to v1.4.0
copier update --vcs-ref v1.4.0 --trust

# Copier will prompt for new variables introduced across versions:
# - pypi_auth_method (v1.4.0): Choose "token" (default) or "trusted_publishing"

# Answer prompts:
# [?] PyPI authentication method: token

# Copier will apply ALL changes from v1.0.0 → v1.4.0
# This includes:
# - v1.1.0: AGENTS.md enhancements
# - v1.2.0: Memory module fixes
# - v1.3.0: Vision framework
# - v1.4.0: just workflow + PyPI setup

# Review changes (WILL BE EXTENSIVE)
git status
git diff
```

#### Step 3: Resolve Combined Conflicts (2-3 hours)

**Conflicts are EXPECTED in cumulative upgrade**. Apply these strategies:

##### Conflict 1: AGENTS.md (Combined v1.1 + v1.3 + v1.4)

**Template changes across versions**:
- v1.1: Added A-MEM Integration, Memory Troubleshooting
- v1.3: Added Strategic Design section
- v1.4: Updated Task Discovery (just --list)

**Your customization** (likely):
```markdown
## Project-Specific Workflows
[your custom content]
```

**Merge Strategy**: Accept ALL template changes + preserve custom
```bash
# 1. Accept template version first
git checkout --theirs AGENTS.md

# 2. Re-add your custom sections at end
cat >> AGENTS.md <<'EOF'

## Project-Specific Workflows
[paste your custom content here]
EOF

# 3. Verify structure
# Should have: A-MEM Integration, Memory Troubleshooting, Strategic Design, Task Discovery, AND your custom sections
```

##### Conflict 2: Memory Module (v1.2.0 Critical Fixes)

**Template fixed**:
```python
# Old (v1.0-v1.1 - BROKEN)
from mcp_n8n.memory.event_log import EventLog
source: str = "mcp-n8n"

# New (v1.2+ - FIXED)
from {{ package_name }}.memory.event_log import EventLog
source: str = "{{ project_slug }}"
```

**Your customization** (if any):
```python
# Custom event emission logic
def custom_emit_event():
    # your custom code
```

**Merge Strategy**: ALWAYS accept template fix + re-apply custom logic
```bash
# 1. Accept template's critical fix
git checkout --theirs src/{{ package_name }}/memory/__init__.py
git checkout --theirs src/{{ package_name }}/memory/event_log.py
git checkout --theirs src/{{ package_name }}/memory/trace.py

# 2. Re-add your custom logic (if any)
# Edit files to re-insert custom event emission, custom queries, etc.

# 3. Test immediately (critical path)
pytest tests/memory/  # Ensure memory module works
```

##### Conflict 3: README.md (Combined v1.3 + v1.4)

**Template changes**:
- v1.3: Added Vision framework references
- v1.4: Promoted `just` workflow, updated Getting Started

**Your customization** (likely):
- Project description
- Usage examples
- API documentation

**Merge Strategy**: Merge both (template structure + your content)
```bash
# 1. Review template changes
git diff --theirs README.md

# 2. Review your changes
git diff --ours README.md

# 3. Manually merge:
# - Accept template's Development section (just workflow)
# - Accept template's Vision references
# - Keep your project description
# - Keep your usage examples
# - Update Getting Started to match v1.4 (just commands)
```

##### Conflict 4: Vision Framework (v1.3.0 - May Conflict with Existing Roadmap)

**Template added**:
- `dev-docs/vision/PRODUCT.md`
- `dev-docs/vision/TECHNICAL.md`
- `dev-docs/vision/TEAM.md`
- `ROADMAP.md`

**Your project** (if existing roadmap):
- `ROADMAP.md` (existing)
- `VISION.md` (existing)
- Planning docs

**Merge Strategy**: Integrate template structure with existing content
```bash
# Option 1: You have no existing roadmap → Accept template
git add dev-docs/vision/ ROADMAP.md

# Option 2: You have existing ROADMAP.md → Merge
# 1. Rename your existing roadmap
mv ROADMAP.md ROADMAP_OLD.md

# 2. Accept template's ROADMAP.md
git checkout --theirs ROADMAP.md

# 3. Migrate content from old to new structure
# Copy strategic goals from ROADMAP_OLD.md to template's ROADMAP.md

# 4. Fill in vision docs with project-specific content
# Edit dev-docs/vision/PRODUCT.md (your product vision)
# Edit dev-docs/vision/TECHNICAL.md (your tech strategy)
# Edit dev-docs/vision/TEAM.md (your team philosophy)

# 5. Remove old roadmap after migration
rm ROADMAP_OLD.md
```

##### Conflict 5: justfile (v1.4.0 - Custom Tasks)

**Template changed**:
- `just --list` as primary interface
- Updated task descriptions
- New tasks: `just pypi-setup`, `just docs`

**Your customization** (if any):
```bash
# Custom tasks you added
custom-deploy:
    @echo "Deploying to production..."
    ./scripts/deploy.sh
```

**Merge Strategy**: Combine (template tasks + custom tasks)
```bash
# 1. Accept template version
git checkout --theirs justfile

# 2. Re-add your custom tasks at bottom
cat >> justfile <<'EOF'

# === Project-Specific Tasks ===

custom-deploy:
    @echo "Deploying to production..."
    ./scripts/deploy.sh

[other custom tasks]
EOF

# 3. Verify
just --list
# Should show BOTH template tasks AND your custom tasks
```

#### Step 4: Validation (1 hour)

```bash
# 1. Environment check
./scripts/check-env.sh
# Should pass (just may auto-install)

# 2. Memory module critical test
pytest tests/memory/
# MUST pass (v1.2.0 fixes)

# 3. Full test suite
pytest
# All tests should pass

# 4. Verify just workflow
just --list
# Should show all tasks with descriptions

just test
# Should run tests successfully

# 5. Verify customizations preserved
# Check each file in UPGRADING.md "Customized Files" section
# Ensure your custom logic is still present

# 6. Smoke test
./scripts/smoke-test.sh
# Or: just test-smoke

# 7. Pre-merge validation
./scripts/pre-merge.sh
# Or: just pre-merge

# All quality gates should pass
```

#### Step 5: Documentation (30 minutes)

```bash
# 1. Update UPGRADING.md
# Add entry to "Template Version History" table:
# | 2025-10-XX | v1.0.0 | v1.4.0 | Cumulative upgrade: A-MEM, critical fixes, vision, just workflow |

# 2. Document major customization changes (if any)
# Add entries to "Major Customization Changes" table

# 3. Commit upgrade
git add .
git commit -m "chore: Upgrade to chora-base v1.4.0 (cumulative from v1.0.0)

- Updated from v1.0.0 to v1.4.0 (cumulative upgrade)
- Applied v1.1.0: AGENTS.md enhancements (A-MEM, memory troubleshooting)
- Applied v1.2.0: Critical ImportError fixes in memory module
- Applied v1.3.0: Vision framework (dev-docs/vision/, ROADMAP.md)
- Applied v1.4.0: just workflow + PyPI authentication setup
- Preserved customizations: [list your customizations]
- All tests passing, quality gates passed

Effort: ~X hours (cumulative approach)
See docs/upgrades/CUMULATIVE_v1.0-to-v1.4.md for details"

# 4. Tag (optional)
git tag upgraded-to-v1.4.0
```

---

## Incremental Upgrade Path (Alternative)

**If cumulative approach too risky, use incremental**:

### Phase 1: v1.0.0 → v1.1.0 (30 min)
```bash
copier update --vcs-ref v1.1.0 --trust
# Accept AGENTS.md enhancements
# No conflicts expected (pure addition)
pytest  # Validate
git commit -m "chore: Upgrade to v1.1.0 (AGENTS.md enhancements)"
```

See [v1.0-to-v1.1.md](v1.0-to-v1.1.md) for details.

### Phase 2: v1.1.0 → v1.2.0 (1-2 hrs) ⚠️ CRITICAL
```bash
copier update --vcs-ref v1.2.0 --trust
# MUST accept memory module fixes (critical)
# Resolve conflicts in customized memory code
pytest tests/memory/  # MUST pass
pytest  # Full validation
git commit -m "chore: Upgrade to v1.2.0 (critical ImportError fixes)"
```

See [v1.1-to-v1.2.md](v1.1-to-v1.2.md) for details.

### Phase 3: v1.2.0 → v1.3.0 (2-3 hrs)
```bash
copier update --vcs-ref v1.3.0 --trust
# Add vision framework
# Integrate with existing roadmap if conflicts
# Update AGENTS.md with Strategic Design
pytest  # Validate
git commit -m "chore: Upgrade to v1.3.0 (vision framework)"
```

See [v1.2-to-v1.3.md](v1.2-to-v1.3.md) for details.

### Phase 4: v1.3.0 → v1.4.0 (2-3 hrs)
```bash
copier update --vcs-ref v1.4.0 --trust
# Answer: pypi_auth_method = token (or trusted_publishing)
# Accept just workflow
# Update justfile with custom tasks
just --list  # Verify
pytest  # Validate
git commit -m "chore: Upgrade to v1.4.0 (just workflow + PyPI setup)"
```

See [v1.3-to-v1.4.md](v1.3-to-v1.4.md) for details.

**Total incremental effort**: 6-9.5 hours (30m + 1.5hrs + 2.5hrs + 2.5hrs)

---

## Hybrid Upgrade Path (v1.0→v1.2→v1.4)

**Fast path focusing on critical fixes + ecosystem consistency**:

### Phase 1: v1.0.0 → v1.2.0 (2 hours)
```bash
# Jump directly to v1.2.0 (critical fixes)
copier update --vcs-ref v1.2.0 --trust

# This includes:
# - v1.1.0: AGENTS.md enhancements
# - v1.2.0: Memory module fixes

# Resolve conflicts (AGENTS.md likely, memory module if customized)
pytest tests/memory/  # MUST pass
pytest  # Full validation
git commit -m "chore: Upgrade to v1.2.0 (includes v1.1 + critical fixes)"
```

**Benefit**: Get critical fixes quickly with minimal steps
**Cost**: Skip v1.3.0 vision framework (can add later if needed)

### Phase 2: v1.2.0 → v1.4.0 (2 hours)
```bash
# Jump to v1.4.0 (just workflow + PyPI)
copier update --vcs-ref v1.4.0 --trust

# This includes:
# - v1.3.0: Vision framework (can skip if not using)
# - v1.4.0: just workflow + PyPI setup

# Answer prompts:
# [?] pypi_auth_method: token

# Resolve conflicts (AGENTS.md, justfile, README.md)
just --list  # Verify
pytest  # Validate
git commit -m "chore: Upgrade to v1.4.0 (includes v1.3 vision + just workflow)"
```

**Total hybrid effort**: 2-4 hours (50% faster than incremental)

---

## Validation Checklist

### Core Functionality

- [ ] Project imports work: `python -c "from {{ package_name }} import *"`
- [ ] Memory module imports fixed: `python -c "from {{ package_name }}.memory import EventLog"`
- [ ] Tests pass: `pytest`
- [ ] Coverage maintained: `pytest --cov`
- [ ] Scripts execute: `./scripts/check-env.sh`

### Critical Fixes (v1.2.0)

- [ ] No ImportError in memory module
- [ ] Event log uses correct package name (not "mcp-n8n")
- [ ] Knowledge graph uses correct project slug
- [ ] Trace context uses correct source identifier
- [ ] Scripts use generalized paths (not hardcoded)

### Template Integration

#### v1.1.0 Features
- [ ] AGENTS.md has A-MEM Integration section
- [ ] AGENTS.md has Memory Troubleshooting (260 lines)
- [ ] AGENTS.md has Agent Self-Service Workflows
- [ ] AGENTS.md has Diátaxis Framework section

#### v1.3.0 Features
- [ ] `dev-docs/vision/PRODUCT.md` exists
- [ ] `dev-docs/vision/TECHNICAL.md` exists
- [ ] `dev-docs/vision/TEAM.md` exists
- [ ] `ROADMAP.md` exists (or integrated with existing)
- [ ] AGENTS.md has Strategic Design section

#### v1.4.0 Features
- [ ] `justfile` updated with v1.4.0 tasks
- [ ] `just --list` shows task catalog
- [ ] `PYPI_SETUP.md` exists
- [ ] `.github/workflows/release.yml` has chosen PyPI auth method
- [ ] AGENTS.md has updated Task Discovery section

### Version Tracking

- [ ] `.copier-answers.yml` shows `_commit: v1.4.0`
- [ ] `UPGRADING.md` updated with v1.0→v1.4 history entry

### Customizations Preserved

- [ ] All custom sections in AGENTS.md still present
- [ ] All custom tasks in justfile still present
- [ ] Custom memory module logic preserved (if any)
- [ ] Custom README sections preserved
- [ ] Custom scripts logic preserved
- [ ] (Review "Customized Files" section in UPGRADING.md)

### Quality Gates

- [ ] Pre-commit hooks pass: `pre-commit run --all-files`
- [ ] Linting passes: `ruff check .`
- [ ] Type checking passes: `mypy src/`
- [ ] Smoke test passes: `./scripts/smoke-test.sh` OR `just test-smoke`
- [ ] Integration test passes: `./scripts/integration-test.sh` OR `just test-integration`

### Workflow Validation

- [ ] `just --list` works (v1.4.0)
- [ ] `just test` runs tests
- [ ] `just check` runs environment checks
- [ ] `just pre-merge` passes all quality gates
- [ ] Scripts still work directly: `./scripts/check-env.sh`

---

## Example Cumulative Upgrade Session

```bash
# Starting state (v1.0.0 project)
$ cat .copier-answers.yml | grep _commit
_commit: v1.0.0

$ git status
On branch main
nothing to commit, working tree clean

# Create backup
$ git branch backup-pre-upgrade-v1.4.0-$(date +%Y%m%d)
$ git tag backup-v1.0.0

# Document current customizations
$ cat UPGRADING.md
# [Review "Customized Files" section]
# Found customizations:
# - AGENTS.md: Custom workflow section
# - justfile: Custom deploy task
# - src/*/memory/event_log.py: Custom event emission logic

# Run cumulative upgrade
$ copier update --vcs-ref v1.4.0 --trust

[copier prompts for new variables]
? PyPI authentication method (token): token

[copier applies all changes v1.0.0 → v1.4.0]

# Review extensive changes
$ git status
On branch main
Changes not staged for commit:
  modified:   .copier-answers.yml
  modified:   AGENTS.md
  modified:   README.md
  modified:   justfile
  modified:   src/my_project/memory/__init__.py
  modified:   src/my_project/memory/event_log.py
  modified:   src/my_project/memory/trace.py
  new file:   dev-docs/vision/PRODUCT.md
  new file:   dev-docs/vision/TECHNICAL.md
  new file:   dev-docs/vision/TEAM.md
  new file:   ROADMAP.md
  new file:   PYPI_SETUP.md

$ git diff --stat
 .copier-answers.yml                        |    2 +-
 AGENTS.md                                  | +1115 -20
 README.md                                  |   +88 -15
 ROADMAP.md                                 |  +145 new
 PYPI_SETUP.md                              |  +420 new
 dev-docs/vision/PRODUCT.md                 |  +180 new
 dev-docs/vision/TECHNICAL.md               |  +195 new
 dev-docs/vision/TEAM.md                    |  +125 new
 justfile                                   |   +45 -10
 src/my_project/memory/__init__.py          |    +8 -2
 src/my_project/memory/event_log.py         |   +12 -8
 src/my_project/memory/knowledge_graph.py   |    +6 -4
 src/my_project/memory/trace.py             |    +4 -2
 13 files changed, 2345 insertions(+), 61 deletions(-)

# Resolve conflicts

# 1. AGENTS.md - Accept template + re-add custom section
$ git checkout --theirs AGENTS.md
$ cat >> AGENTS.md <<'EOF'

## Project-Specific Workflows
[my custom workflow content]
EOF

# 2. Memory module - Accept critical fixes + re-apply custom logic
$ git checkout --theirs src/my_project/memory/__init__.py
$ git checkout --theirs src/my_project/memory/event_log.py
$ git checkout --theirs src/my_project/memory/trace.py

# Edit event_log.py to re-add custom event emission
$ vim src/my_project/memory/event_log.py
# [Re-added custom emit_custom_event() function]

# 3. justfile - Accept template + re-add custom task
$ git checkout --theirs justfile
$ cat >> justfile <<'EOF'

# === Project-Specific Tasks ===

custom-deploy:
    @echo "Deploying to production..."
    ./scripts/deploy.sh
EOF

# 4. README.md - Manual merge
$ vim README.md
# [Kept project description, accepted template's just workflow section]

# 5. Vision framework - No conflicts (new files)
$ git add dev-docs/vision/ ROADMAP.md PYPI_SETUP.md

# Validate critical fixes (v1.2.0)
$ pytest tests/memory/
===== 15 passed in 2.14s =====

# Full test suite
$ pytest
===== 42 passed in 5.31s =====

# Verify just workflow (v1.4.0)
$ just --list
Available recipes:
    build           # Build distribution packages
    check           # Run environment checks
    clean           # Clean build artifacts
    pre-merge       # Run all pre-merge checks
    pypi-setup      # Interactive PyPI authentication setup
    test            # Run test suite
    custom-deploy   # [My custom task] Deploy to production

$ just test
===== 42 passed in 5.28s =====

# Verify customizations preserved
$ grep "Project-Specific Workflows" AGENTS.md
## Project-Specific Workflows

$ grep "custom-deploy" justfile
custom-deploy:

$ grep "emit_custom_event" src/my_project/memory/event_log.py
def emit_custom_event():

# All customizations preserved ✓

# Run full validation
$ just pre-merge
✓ Environment checks passed
✓ Tests passed (42 passed)
✓ Coverage maintained (87%)
✓ Linting passed
✓ Type checking passed
✓ Pre-commit hooks passed

# Update UPGRADING.md
$ vim UPGRADING.md
# Added: | 2025-10-19 | v1.0.0 | v1.4.0 | Cumulative upgrade: A-MEM, critical fixes, vision, just workflow |

# Commit upgrade
$ git add .
$ git commit -m "chore: Upgrade to chora-base v1.4.0 (cumulative from v1.0.0)

- Updated from v1.0.0 to v1.4.0 (cumulative upgrade)
- Applied v1.1.0: AGENTS.md enhancements (A-MEM, memory troubleshooting)
- Applied v1.2.0: Critical ImportError fixes in memory module
- Applied v1.3.0: Vision framework (dev-docs/vision/, ROADMAP.md)
- Applied v1.4.0: just workflow + PyPI authentication setup (token method)
- Preserved customizations:
  - AGENTS.md: Project-Specific Workflows section
  - justfile: custom-deploy task
  - memory/event_log.py: emit_custom_event() function
- All tests passing (42 passed)
- Quality gates passed (pre-merge validation)

Effort: ~5 hours (cumulative approach)
See docs/upgrades/CUMULATIVE_v1.0-to-v1.4.md for details"

$ git log --oneline -1
a1b2c3d chore: Upgrade to chora-base v1.4.0 (cumulative from v1.0.0)

# Success! v1.0.0 → v1.4.0 complete in ~5 hours
```

---

## Rollback Procedure

**If cumulative upgrade fails or causes issues**:

### Quick Rollback (Uncommitted Changes)

```bash
# If you haven't committed the upgrade yet
git reset --hard HEAD

# Verify
cat .copier-answers.yml | grep _commit
# Should show v1.0.0

./scripts/check-env.sh
pytest
```

### Committed Rollback

```bash
# Option 1: Undo last commit
git reset --hard HEAD~1

# Option 2: Restore from backup branch
git checkout main
git reset --hard backup-pre-upgrade-v1.4.0-$(date +%Y%m%d)

# Option 3: Restore from tag
git checkout main
git tag  # Find your backup tag
git reset --hard backup-v1.0.0

# Verify rollback
cat .copier-answers.yml | grep _commit
# Should show v1.0.0

./scripts/check-env.sh
pytest
```

### Partial Rollback (Cumulative Failed, Try Incremental)

```bash
# If cumulative upgrade too complex, rollback and use incremental
git reset --hard backup-v1.0.0

# Then follow incremental path:
# 1. v1.0.0 → v1.1.0 (30 min)
copier update --vcs-ref v1.1.0 --trust
git commit -m "chore: Upgrade to v1.1.0"

# 2. v1.1.0 → v1.2.0 (1-2 hrs)
copier update --vcs-ref v1.2.0 --trust
git commit -m "chore: Upgrade to v1.2.0 (critical fixes)"

# 3. v1.2.0 → v1.3.0 (2-3 hrs)
copier update --vcs-ref v1.3.0 --trust
git commit -m "chore: Upgrade to v1.3.0 (vision)"

# 4. v1.3.0 → v1.4.0 (2-3 hrs)
copier update --vcs-ref v1.4.0 --trust
git commit -m "chore: Upgrade to v1.4.0 (just workflow)"
```

### Report Issues

If cumulative upgrade consistently fails, report it:

**GitHub Issue**: https://github.com/liminalcommons/chora-base/issues/new

**Include**:
- Upgrade path attempted (cumulative/incremental/hybrid)
- Version: v1.0.0 → v1.4.0
- Conflict points (which files, what errors)
- Customizations involved (from UPGRADING.md)
- Steps to reproduce
- Whether incremental path worked as alternative

---

## Common Issues

### Issue 1: Too Many Conflicts at Once (Cumulative)

**Symptom**:
Cumulative upgrade produces overwhelming conflicts in multiple files

**Cause**: Heavy customizations across files that changed in v1.0→v1.4

**Solution**:
```bash
# Rollback and use incremental approach instead
git reset --hard backup-v1.0.0

# Follow incremental path (see "Incremental Upgrade Path" section)
# Validate each step to isolate conflicts
```

### Issue 2: Memory Module Tests Fail After v1.2.0 Fixes

**Symptom**:
`pytest tests/memory/` fails with ImportError or wrong project names

**Cause**: Custom memory module logic not updated for v1.2.0 generalization

**Solution**:
```bash
# Review v1.2.0 changes
git diff v1.1.0..v1.2.0 -- template/src/{{ package_name }}/memory/

# Update your custom code to use generalized names:
# - Replace hardcoded "mcp_n8n" with {{ package_name }}
# - Replace hardcoded "mcp-n8n" with {{ project_slug }}
# - Update import statements

# Example fix in custom code:
# OLD: from mcp_n8n.memory.event_log import EventLog
# NEW: from my_project.memory.event_log import EventLog

# Re-test
pytest tests/memory/
```

### Issue 3: Vision Framework Conflicts with Existing Roadmap

**Symptom**:
Template's `ROADMAP.md` conflicts with your existing roadmap

**Cause**: Both you and v1.3.0 added ROADMAP.md

**Solution**:
```bash
# Option 1: Migrate to template structure
mv ROADMAP.md ROADMAP_OLD.md
git checkout --theirs ROADMAP.md
# Copy strategic goals from ROADMAP_OLD.md to template's ROADMAP.md
rm ROADMAP_OLD.md

# Option 2: Keep your roadmap, skip template's
git checkout --ours ROADMAP.md
# Note: You'll miss v1.3.0's vision framework structure

# Option 3: Hybrid (rename template's)
git checkout --theirs ROADMAP.md
mv ROADMAP.md ROADMAP_TEMPLATE.md
git checkout --ours ROADMAP.md
# Now you have both: ROADMAP.md (yours) and ROADMAP_TEMPLATE.md (reference)
```

### Issue 4: just Not Found After v1.4.0 Upgrade

**Symptom**:
`just --list` fails with "command not found"

**Cause**: `just` not installed (v1.4.0 auto-installs but may fail)

**Solution**:
```bash
# Re-run setup script (will auto-install just)
./scripts/setup.sh

# Or install manually:
# macOS:
brew install just

# Linux:
cargo install just
# Or: sudo snap install just --classic

# Verify
just --version
just --list
```

### Issue 5: AGENTS.md Custom Sections Lost

**Symptom**:
Your custom AGENTS.md sections missing after cumulative upgrade

**Cause**: Copier overwrote instead of merging (v1.1 + v1.3 + v1.4 all changed AGENTS.md)

**Solution**:
```bash
# Restore from backup
git diff backup-v1.0.0 AGENTS.md > custom_agents_sections.patch

# Review patch to extract your custom sections
cat custom_agents_sections.patch

# Accept template version
git checkout --theirs AGENTS.md

# Manually re-add your custom sections at end of file
vim AGENTS.md
# [Paste your custom sections after template sections]

# Verify structure
# Should have: A-MEM, Memory Troubleshooting, Strategic Design, Task Discovery, AND your custom sections
```

---

## For AI Agents: Decision Documentation

**After completing cumulative upgrade, store decision**:

```json
{
  "id": "chora-base-v1.0-to-v1.4-cumulative-upgrade",
  "created": "2025-10-XX",
  "tags": ["chora-base", "upgrade", "v1.4.0", "cumulative"],

  "upgrade": {
    "from": "v1.0.0",
    "to": "v1.4.0",
    "strategy": "cumulative",
    "decision": "adopted",
    "reasoning": "Multi-version jump for efficiency, needed v1.2.0 critical fixes + v1.4.0 ecosystem consistency"
  },

  "versions_applied": [
    {
      "version": "v1.1.0",
      "type": "additive",
      "features": ["AGENTS.md: A-MEM Integration", "AGENTS.md: Memory Troubleshooting"]
    },
    {
      "version": "v1.2.0",
      "type": "required",
      "features": ["Memory module ImportError fixes", "Path generalization"]
    },
    {
      "version": "v1.3.0",
      "type": "additive",
      "features": ["Vision framework (dev-docs/vision/)", "ROADMAP.md", "Strategic Design"]
    },
    {
      "version": "v1.4.0",
      "type": "optional",
      "features": ["just workflow (primary interface)", "PyPI auth setup (token method)"]
    }
  ],

  "customizations_preserved": [
    "AGENTS.md: Project-Specific Workflows section (re-added after template)",
    "justfile: custom-deploy task (appended after template tasks)",
    "memory/event_log.py: emit_custom_event() function (merged with v1.2 fixes)",
    "README.md: Project description (manual merge with template structure)"
  ],

  "conflicts_resolved": [
    {
      "file": "AGENTS.md",
      "strategy": "accept template + re-add custom sections",
      "template_changes": ["v1.1: A-MEM", "v1.3: Strategic Design", "v1.4: Task Discovery"],
      "custom_preserved": "Project-Specific Workflows section"
    },
    {
      "file": "src/*/memory/*.py",
      "strategy": "accept template fixes (critical) + re-apply custom logic",
      "template_changes": ["v1.2: ImportError fixes", "v1.2: Generalization"],
      "custom_preserved": "emit_custom_event() function"
    },
    {
      "file": "justfile",
      "strategy": "accept template + append custom tasks",
      "template_changes": ["v1.4: just --list primary", "v1.4: New tasks"],
      "custom_preserved": "custom-deploy task"
    },
    {
      "file": "README.md",
      "strategy": "manual merge (template structure + custom content)",
      "template_changes": ["v1.3: Vision references", "v1.4: just workflow prominence"],
      "custom_preserved": "Project description, usage examples"
    }
  ],

  "workflow_changes_adopted": [
    {
      "from": "ls scripts/ (project-specific)",
      "to": "just --list (ecosystem-wide)",
      "benefit": "Knowledge transfers to all chora-base v1.4.0+ projects",
      "migration": "Updated agent knowledge: just commands preferred, scripts still work as fallback"
    },
    {
      "from": "No structured vision docs",
      "to": "dev-docs/vision/ + ROADMAP.md",
      "benefit": "Long-term strategic planning documented",
      "migration": "Populated vision docs with project-specific content"
    }
  ],

  "validation": {
    "tests": "passing (pytest: 42 passed)",
    "coverage": "maintained (87%)",
    "memory_module": "passing (v1.2.0 critical fixes validated)",
    "just_workflow": "working (just --list shows all tasks)",
    "scripts": "working (./scripts/check-env.sh: all checks passed)",
    "pre_merge": "passed (all quality gates)"
  },

  "benefits_realized": [
    "v1.2.0 critical fixes applied (memory module works correctly)",
    "A-MEM workflow documented (v1.1.0)",
    "Vision framework integrated (v1.3.0)",
    "just --list ecosystem consistency (v1.4.0)",
    "30-40% time saved vs incremental (4-6 hrs vs 6-9.5 hrs)"
  ],

  "time_invested": "5 hours (cumulative upgrade + validation)",
  "displacement": {
    "required": ["v1.2.0 memory fixes (MUST adopt)"],
    "optional": ["v1.4.0 just workflow (adopted for ecosystem consistency)"],
    "additive": ["v1.1.0 AGENTS.md", "v1.3.0 vision framework"]
  },

  "lessons_learned": [
    "Cumulative approach efficient for time-constrained projects",
    "Memory module conflicts required careful merge (critical fixes + custom logic)",
    "Vision framework integration smooth (no existing roadmap conflict)",
    "just workflow adoption valuable (ecosystem knowledge transfer)"
  ]
}
```

---

## Comparison: Cumulative vs Incremental vs Hybrid

| Aspect | Cumulative (v1.0→v1.4) | Incremental (v1.0→v1.1→v1.2→v1.3→v1.4) | Hybrid (v1.0→v1.2→v1.4) |
|--------|------------------------|------------------------------------------|--------------------------|
| **Total Effort** | 4-6 hours | 6-9.5 hours | 2-4 hours |
| **Time Savings** | 30-40% vs incremental | Baseline (0% savings) | 50% vs incremental |
| **Conflict Complexity** | HIGH (all at once) | LOW (isolated per version) | MEDIUM (two jumps) |
| **Validation Points** | 1 (end) | 4 (after each version) | 2 (v1.2, v1.4) |
| **Rollback Granularity** | All-or-nothing | Per-version | Two checkpoints |
| **Best For** | Time-constrained, minimal customizations | Heavy customizations, risk-averse | Fast critical fixes + ecosystem |
| **Risk Level** | HIGH | LOW | MEDIUM |
| **Learning Curve** | Steep (all changes together) | Gentle (gradual learning) | Moderate |
| **Recommended When** | Need v1.4.0 features quickly | First-time upgrader, many customizations | Need v1.2 fixes + v1.4 ecosystem |

### When to Use Each Strategy

#### Use Cumulative (v1.0→v1.4) When:
- ✅ Time-constrained (need v1.4.0 in 4-6 hours)
- ✅ Minimal customizations (conflicts manageable)
- ✅ Confident with complex conflict resolution
- ✅ Want immediate access to all v1.4.0 features
- ❌ Heavy customizations (too many conflicts)
- ❌ Risk-averse (no intermediate validation)

#### Use Incremental (v1.0→v1.1→v1.2→v1.3→v1.4) When:
- ✅ First-time upgrader (learning upgrade process)
- ✅ Heavy customizations (isolate conflicts per version)
- ✅ Risk-averse (validate each step)
- ✅ Want to understand each version's changes
- ❌ Time-constrained (6-9.5 hours total)
- ❌ Need v1.4.0 features immediately

#### Use Hybrid (v1.0→v1.2→v1.4) When:
- ✅ Need v1.2.0 critical fixes quickly (2-4 hours)
- ✅ Want v1.4.0 ecosystem consistency
- ✅ Don't need v1.3.0 vision framework
- ✅ Balanced risk tolerance (two validation points)
- ❌ Want v1.3.0 vision framework (must include or add separately)

---

## Related Documentation

- [Upgrade Philosophy](PHILOSOPHY.md) - Principles and decision frameworks
- [v1.0-to-v1.1.md](v1.0-to-v1.1.md) - Documentation enhancements (v1.1.0)
- [v1.1-to-v1.2.md](v1.1-to-v1.2.md) - Critical fixes (v1.2.0)
- [v1.2-to-v1.3.md](v1.2-to-v1.3.md) - Vision framework (v1.3.0)
- [v1.3-to-v1.4.md](v1.3-to-v1.4.md) - just workflow + PyPI setup (v1.4.0)
- [CHANGELOG](../../CHANGELOG.md) - Full release history
- [template/UPGRADING.md](../../template/UPGRADING.md.jinja) - Project-level upgrade guide

---

## Feedback & Continuous Improvement

**This guide is a living document** based on real adoption experiences.

**Help us improve**:
- GitHub Issues: https://github.com/liminalcommons/chora-base/issues/new
- Share your upgrade experience (cumulative/incremental/hybrid)
- Report conflicts not covered in this guide
- Suggest merge strategies that worked better
- Contribute example upgrade sessions

**Especially valuable**:
- Cumulative upgrade transcripts from real projects
- Conflict resolution strategies for custom codebases
- Time estimates from your actual upgrades
- AI agent autonomous decision success rates

---

**Note**: This cumulative guide is designed for **original adopters** (chora-compose, mcp-n8n teams) who started with v1.0.0 and want to reach v1.4.0 efficiently. It represents the complete evolution of chora-base from its first public release to its mature ecosystem-consistent state.

**Target audience**: Multi-project AI agents who will benefit from ecosystem-wide pattern learning (just --list, vision framework) and need critical v1.2.0 fixes.

**Success metric**: <4 hours upgrade time for original adopters (vs estimated 8-12 hours without this guide).
