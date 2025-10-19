# Upgrading from vX.Y to vX.Z

<!-- This is the template for version-specific upgrade guides -->
<!-- AI-optimized format: decision trees, structured criteria, machine-parseable -->

**Release Date**: YYYY-MM-DD
**Template Version**: vX.Y → vX.Z
**Upgrade Effort**: X-Y hours
**For**: Human developers, AI coding agents

---

## Quick Assessment

| Aspect | Value |
|--------|-------|
| **Effort** | X-Y hours |
| **Breaking Changes** | Yes/No/Conditional |
| **Required For** | [Correctness/New Features/DX Improvement] |
| **Can Skip If** | [Specific conditions when safe to skip] |
| **Displacement Risk** | HIGH/MEDIUM/LOW |
| **Agent Autonomy** | [% of decisions agents can make without human] |

---

## TL;DR

**What's New**:
- Feature 1 (X lines added)
- Feature 2 (Y files changed)
- Fix 3 (CRITICAL - required)

**Impact on Existing Adopters**:
- IF [condition]: [impact description]
- IF [condition]: [impact description]

**Recommended Action**:
- [For new projects]: Adopt immediately
- [For v1.X.0 adopters]: Upgrade now/defer/evaluate
- [For heavily customized projects]: Review [specific files]

---

## Decision Tree for AI Agents

```
START

├─ Does project have CRITICAL issues from v1.X?
│  ├─ YES → Upgrade REQUIRED (correctness fixes)
│  └─ NO → Continue evaluation
│
├─ Does project use [affected feature/system]?
│  ├─ NO → Skip upgrade (not relevant)
│  └─ YES → Continue evaluation
│
├─ Are customizations in [affected files]?
│  ├─ NO → Safe to adopt (copier update)
│  └─ YES → Review merge strategy below
│
├─ Does new approach conflict with existing workflow?
│  ├─ NO → Adopt (benefits > costs)
│  └─ YES → Evaluate displacement criteria
│
END: [ADOPT/DEFER/SKIP] with rationale
```

**Criteria by Project Type**:

| Project Type | Adopt If | Defer If | Skip If |
|--------------|----------|----------|---------|
| **New Project** (generated from v1.X) | Always | N/A | N/A |
| **Stable Project** (few customizations) | [condition] | [condition] | [condition] |
| **Customized Project** (extensive local changes) | [condition] | [condition] | [condition] |
| **Multi-Project Agent** (ecosystem consistency matters) | [condition] | [condition] | [condition] |

---

## What Changed

### Files Added

**New Template Files**:
1. `template/path/to/new/file.jinja` (~X lines)
   - **Purpose**: [description]
   - **When included**: [copier variable condition]
   - **Conflicts with**: [existing file/pattern, if any]
   - **Agent impact**: [how this affects agent workflow]

### Files Modified

**Changed Template Files**:
1. `template/path/to/changed/file.jinja`
   - **Lines changed**: +X -Y
   - **Change type**: [Fix/Enhancement/Refactor]
   - **Displacement risk**: [HIGH/MEDIUM/LOW]
   - **Customization impact**: [likely/unlikely to conflict]
   - **Diff summary**:
     ```diff
     - old approach
     + new approach
     ```

### Files Renamed/Removed

**Deprecations** (if any):
1. `old/file/path` → `new/file/path`
   - **Migration**: [automatic/manual]
   - **Breaking**: [yes/no]

---

## Displacement Analysis

### Type 1: Required (Correctness Fixes)

**None** / **List fixes here**

Example:
```
File: template/src/{{package_name}}/memory/__init__.py
Issue: ImportError when using memory system
Fix: Converted to .jinja, use template variable for imports
Impact: MUST upgrade if using memory system
Strategy: Merge template fix, preserve customizations (see below)
```

### Type 2: Optional (Workflow Improvements)

**None** / **List improvements here**

Example:
```
Feature: `just --list` as primary task discovery
Change: README/CONTRIBUTING/AGENTS.md restructured around just
Benefit: Machine-readable task catalog, ecosystem consistency
Cost: Must install just, update task knowledge patterns
Decision: Adopt if working across chora-base ecosystem, evaluate otherwise
Strategy: See "Workflow Replacement Decision" below
```

### Type 3: Additive (Safe Enhancements)

**None** / **List additions here**

Example:
```
Files: dev-docs/vision/*.md, ROADMAP.md
Purpose: Strategic design framework
Conflict: May overlap with existing planning docs
Strategy: Skip if not needed, integrate if using vision-driven development
```

---

## Upgrade Steps

### Prerequisites

```bash
# 1. Ensure clean git state
git status
# Should show "nothing to commit, working tree clean"

# 2. Create backup
git branch backup-pre-upgrade-vX.Z
git tag backup-vX.Y

# 3. Review current customizations
git diff $(git log --diff-filter=A --format="%H" -n 1 .copier-answers.yml) HEAD
# Shows all changes since initial template generation

# 4. Document customizations (for merge reference)
# List customized files in project's UPGRADING.md
```

### Automated Upgrade

```bash
# Update to new version
copier update --vcs-ref vX.Z --trust

# Review changes
git diff

# Test immediately
./scripts/check-env.sh
pytest
```

### Manual Conflict Resolution

**If copier update shows conflicts:**

#### Conflict 1: [File Path]

**Template Change**:
```diff
[show template diff]
```

**Your Customization** (likely):
```python
[show common customization pattern]
```

**Merge Strategy**:
1. Accept template improvement: [specific lines]
2. Preserve your customization: [specific lines]
3. Combined result:
   ```python
   [show merged version]
   ```

**Validation**:
```bash
[command to verify merge worked]
```

#### Conflict 2: [File Path]

[Repeat for each common conflict]

---

## Workflow Replacement Decision

<!-- Only include if this upgrade advocates replacing existing workflow -->

**New Approach**: [description]

**Current Approach**: [description]

### Benefits Analysis

**New Approach Advantages**:
- [ ] Benefit 1 (quantify if possible)
- [ ] Benefit 2
- [ ] Benefit 3

**New Approach Disadvantages**:
- [ ] Cost 1
- [ ] Cost 2

**Current Approach Advantages**:
- [ ] Benefit 1
- [ ] Benefit 2

**Current Approach Disadvantages**:
- [ ] Cost 1
- [ ] Cost 2

### Decision Criteria

**Adopt New Approach IF**:
- [ ] Working across multiple chora-base projects
- [ ] Benefits significantly outweigh costs
- [ ] No strong attachment to current workflow
- [ ] [Specific criterion for this upgrade]

**Keep Current Approach IF**:
- [ ] Extensive existing patterns/knowledge built on current approach
- [ ] Single-project context (no ecosystem benefit)
- [ ] Current approach meets all needs
- [ ] [Specific criterion for this upgrade]

**Hybrid Strategy** (if applicable):
- [ ] Use new approach for [specific tasks]
- [ ] Keep current approach for [specific tasks]
- [ ] Migration plan: [description]

### Migration Guide

**If adopting new approach:**

```bash
# Step 1: [action]
# Step 2: [action]
# Step 3: [action]
```

**Knowledge Migration** (for AI agents):

**OLD pattern** (project-specific):
```json
{
  "task": "run tests",
  "command": "./scripts/test.sh",
  "project": "my-project"
}
```

**NEW pattern** (ecosystem-wide):
```json
{
  "task": "run tests",
  "command": "just test",
  "ecosystem": "chora-base",
  "applies_to": "all chora-base v1.X+ projects"
}
```

---

## Validation Checklist

### Core Functionality

- [ ] Project imports work: `python -c "from {{ package_name }} import *"`
- [ ] Tests pass: `pytest`
- [ ] Scripts execute: `./scripts/check-env.sh`
- [ ] [Project-specific validation]

### Template Integration

- [ ] New files generated correctly (if applicable)
- [ ] Modified files merged without conflicts
- [ ] Customizations preserved (git diff shows only template changes)
- [ ] `.copier-answers.yml` updated to vX.Z

### Quality Gates

- [ ] Pre-commit hooks pass: `pre-commit run --all-files`
- [ ] Linting passes: `ruff check .`
- [ ] Type checking passes: `mypy src/`
- [ ] Coverage maintained: `pytest --cov`

### Documentation

- [ ] README accurate (if template changed README)
- [ ] AGENTS.md updated (if template changed AGENTS)
- [ ] UPGRADING.md documents this upgrade
- [ ] CHANGELOG.md updated (if relevant)

---

## Example Upgrade Session

<!-- Show step-by-step transcript like chora-compose adoption -->

```bash
# Starting state
$ git status
On branch main
nothing to commit, working tree clean

$ cat .copier-answers.yml | grep _commit
_commit: vX.Y

# Create backup
$ git branch backup-pre-upgrade-vX.Z
$ git tag backup-vX.Y

# Run upgrade
$ copier update --vcs-ref vX.Z --trust
[copier output]

# Review changes
$ git diff --stat
 template/file1.jinja | 10 +++++-----
 template/file2.jinja | 5 +++++
 2 files changed, 10 insertions(+), 5 deletions(-)

$ git diff template/file1.jinja
[shows diff]

# Test
$ ./scripts/check-env.sh
✓ All checks passed

$ pytest
===== 42 passed in 3.14s =====

# Commit
$ git add .
$ git commit -m "chore: Upgrade to chora-base vX.Z

- Updated from vX.Y to vX.Z
- Applied [specific improvement]
- Preserved customizations in [files]
- All tests passing

See docs/upgrades/vX.Y-to-vX.Z.md for details"
```

---

## Rollback Procedure

**If upgrade fails or causes issues:**

```bash
# Option 1: Rollback commit
git reset --hard HEAD~1

# Option 2: Restore from backup branch
git checkout main
git reset --hard backup-pre-upgrade-vX.Z

# Option 3: Restore from tag
git checkout main
git reset --hard backup-vX.Y

# Verify rollback
cat .copier-answers.yml | grep _commit
# Should show vX.Y

./scripts/check-env.sh
pytest
```

**Report issues**:
- GitHub issue: https://github.com/liminalcommons/chora-base/issues
- Include: version numbers, error messages, customizations involved

---

## Common Issues

### Issue 1: [Description]

**Symptom**:
```
[error message or behavior]
```

**Cause**: [explanation]

**Solution**:
```bash
[fix commands]
```

### Issue 2: [Description]

[Repeat for each known issue]

---

## For AI Agents: Decision Documentation

**After completing upgrade, store decision**:

```json
{
  "id": "chora-base-vX.Y-to-vX.Z-upgrade",
  "created": "YYYY-MM-DD",
  "tags": ["chora-base", "upgrade", "vX.Z"],
  "decision": "adopted/deferred/skipped",
  "reasoning": "[why]",
  "customizations_preserved": [
    "file1: [what was preserved]",
    "file2: [what was preserved]"
  ],
  "workflow_changes": [
    "from: [old pattern]",
    "to: [new pattern]",
    "benefit: [why changed]"
  ],
  "validation": {
    "tests": "passing",
    "coverage": "maintained",
    "scripts": "working"
  }
}
```

---

## Related Documentation

- [Upgrade Philosophy](PHILOSOPHY.md) - Principles and decision frameworks
- [vX.Z CHANGELOG](../../CHANGELOG.md#XZ) - Full release notes
- [Next upgrade: vX.Z to vX.Z+1](vX.Z-to-vX.Z+1.md) - Continue upgrading

---

**Template Version**: 1.0 (this template itself may evolve!)
**Feedback**: Improvements to this template welcome via GitHub issues
