---
title: "SAP-053: Conflict Resolution"
type: guide
sap: SAP-053
created: 2025-11-19
last_updated: 2025-11-19
status: active
tags: [sap-053, conflict-resolution, pre-merge-detection, git-workflow]
related: [SAP-051, SAP-052]
---

# SAP-053: Conflict Resolution

**Version**: 1.0.0 (Detection-Only)
**Status**: Production-Ready (Phase 4 - Distribution)
**Adoption Level**: L3 (Validated)

---

## What is SAP-053?

SAP-053 (Conflict Resolution) provides **pre-merge conflict detection** to catch merge conflicts BEFORE you create a pull request. Instead of discovering conflicts after opening a PR, you can detect them locally and resolve them proactively.

**Key Benefits**:
- ⚡ **Faster PR reviews** - No back-and-forth due to merge conflicts
- 🎯 **Proactive resolution** - Fix conflicts before they block your PR
- 📊 **Conflict classification** - Understand what type of conflict you have
- 🤖 **Automation-ready** - JSON output for CI/CD integration
- 💡 **Smart strategies** - Recommended resolution approach for each conflict type

---

## Quick Start

### 1. Check for Conflicts Before Creating PR

```bash
# From your feature branch, check if it will conflict with main
just conflict-check

# Output:
# ✅ NO CONFLICTS DETECTED
# Safe to merge into main
```

### 2. If Conflicts Are Detected

```bash
# Example output:
# ⚠️  CONFLICTS DETECTED
#
# Files with conflicts (2):
# 1. project-docs/sprints/sprint-13.md
#    - Type: CONTENT
#    - Strategy: MANUAL_REVIEW_WITH_OWNERSHIP
#
# 2. package-lock.json
#    - Type: LOCKFILE
#    - Strategy: REGENERATE_FROM_SOURCE
```

### 3. Resolve Based on Strategy

**For LOCKFILE conflicts** (auto-resolvable):
```bash
# Regenerate lockfile from package.json
npm install  # or yarn install, or poetry lock
git add package-lock.json
git commit -m "fix: regenerate lockfile to resolve conflict"
```

**For CONTENT conflicts** (manual review):
```bash
# Coordinate with file owner or pair to resolve
# See SAP-052 (Ownership Zones) for who owns the file
just ownership-suggest-reviewers project-docs/sprints/sprint-13.md
```

---

## Installation

SAP-053 conflict-checker.py is already included in chora-base. If you're starting a new project:

### Option 1: Using chora-compose (Recommended)

```bash
# Create new project with SAP-053 pre-installed
chora create my-project --template base
cd my-project
just conflict-check  # Ready to use!
```

### Option 2: Manual Installation

```bash
# Copy conflict-checker.py to your project
cp packages/chora-base/scripts/conflict-checker.py scripts/

# Add justfile recipes (append to your justfile)
cat packages/chora-base/justfile | grep -A 15 "SAP-053" >> justfile

# Test installation
just conflict-check
```

---

## Usage

### Basic Usage

```bash
# Check for conflicts with default branch (main)
just conflict-check

# Check for conflicts with a different branch
just conflict-check dev

# Verbose output for debugging
just conflict-check-verbose

# JSON output for automation
just conflict-check-json
```

### Justfile Recipes

| Recipe | Description | Example |
|--------|-------------|---------|
| `just conflict-check [BRANCH]` | Check for conflicts (text output) | `just conflict-check main` |
| `just conflict-check-json [BRANCH]` | Check for conflicts (JSON output) | `just conflict-check-json dev` |
| `just conflict-check-verbose [BRANCH]` | Check with verbose debugging | `just conflict-check-verbose` |
| `just conflict-status [BRANCH]` | Quick status check (with jq) | `just conflict-status` |

### Direct Python Usage

```bash
# From scripts/ directory
python scripts/conflict-checker.py --branch main

# With flags
python scripts/conflict-checker.py --branch main --json
python scripts/conflict-checker.py --branch main --verbose
python scripts/conflict-checker.py --help
```

---

## Understanding Conflict Types

SAP-053 classifies conflicts into 6 types:

### 1. CONTENT (Manual Review)

**What**: Semantic changes to code, documentation, or configuration
**Strategy**: MANUAL_REVIEW or MANUAL_REVIEW_WITH_OWNERSHIP
**Resolution**: Requires human judgment to merge changes

**Example**:
```python
# Your branch:
def calculate_total(items):
    return sum(item.price for item in items)

# Main branch:
def calculate_total(items, tax_rate=0.0):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

**How to resolve**: Understand both changes, combine functionality
```bash
# Coordinate with code owner
just ownership-suggest-reviewers src/utils/calculator.py
```

---

### 2. LOCKFILE (Auto-Resolvable)

**What**: Dependency lockfiles (package-lock.json, poetry.lock, Gemfile.lock)
**Strategy**: REGENERATE_FROM_SOURCE
**Resolution**: Regenerate from source dependency file

**Example**:
```bash
# Conflict in package-lock.json
⚠️  CONFLICTS DETECTED
Files: package-lock.json
Type: LOCKFILE
Strategy: REGENERATE_FROM_SOURCE
```

**How to resolve**:
```bash
# For npm
rm package-lock.json
npm install

# For poetry
rm poetry.lock
poetry lock

# For bundler
rm Gemfile.lock
bundle install
```

---

### 3. METADATA (Auto-Resolvable)

**What**: OS-generated files (.DS_Store, __pycache__, .pyc)
**Strategy**: DELETE_AND_REGENERATE
**Resolution**: Delete file, let system regenerate if needed

**Example**:
```bash
# Conflict in .DS_Store
⚠️  CONFLICTS DETECTED
Files: .DS_Store
Type: METADATA
Strategy: DELETE_AND_REGENERATE
```

**How to resolve**:
```bash
# Delete metadata file
git rm .DS_Store
git commit -m "fix: remove metadata file conflict"

# Add to .gitignore to prevent future conflicts
echo ".DS_Store" >> .gitignore
```

---

### 4. WHITESPACE (Auto-Resolvable)

**What**: Conflicts caused only by whitespace differences (spaces vs tabs, line endings)
**Strategy**: AUTO_RESOLVE_FORMATTING
**Resolution**: Use formatter to normalize

**Example**:
```bash
# Conflict due to mixed tabs/spaces
⚠️  CONFLICTS DETECTED
Files: src/utils.py
Type: WHITESPACE
Strategy: AUTO_RESOLVE_FORMATTING
```

**How to resolve**:
```bash
# For Python
black src/utils.py
git add src/utils.py
git commit -m "fix: normalize whitespace"

# For JavaScript/TypeScript
prettier --write src/utils.ts
```

---

### 5. FORMATTING (Auto-Resolvable)

**What**: Code style differences (quotes, brackets, indentation)
**Strategy**: AUTO_RESOLVE_FORMATTING
**Resolution**: Apply formatter

**Example**: Similar to WHITESPACE, use project formatter (black, prettier, rustfmt)

---

### 6. UNKNOWN

**What**: Conflict type couldn't be determined
**Strategy**: MANUAL_REVIEW
**Resolution**: Inspect file manually

---

## Exit Codes

conflict-checker.py uses exit codes for automation:

| Exit Code | Meaning | Description |
|-----------|---------|-------------|
| **0** | No conflicts | Safe to merge, proceed with PR |
| **1** | Manual review needed | Conflicts require human resolution |
| **2** | Auto-resolvable | Conflicts can be resolved automatically |
| **3** | Error | Tool error (not in git repo, uncommitted changes, etc.) |

**Usage in CI/CD**:
```bash
# Example GitHub Actions workflow
- name: Check for merge conflicts
  run: just conflict-check
  # Fails if exit code != 0

- name: Block PR if manual conflicts exist
  run: |
    just conflict-check-json > conflicts.json
    MANUAL=$(jq '.manual_review_files | length' conflicts.json)
    if [ "$MANUAL" -gt 0 ]; then
      echo "::error::PR has $MANUAL files requiring manual conflict resolution"
      exit 1
    fi
```

---

## JSON Output

For automation and dashboards, use JSON output:

```bash
just conflict-check-json | jq .
```

**Example JSON**:
```json
{
  "has_conflicts": true,
  "safe_to_merge": false,
  "total_files": 2,
  "manual_review_files": ["project-docs/sprints/sprint-13.md"],
  "auto_resolvable_files": ["package-lock.json"],
  "conflicts": [
    {
      "file": "project-docs/sprints/sprint-13.md",
      "type": "CONTENT",
      "strategy": "MANUAL_REVIEW_WITH_OWNERSHIP",
      "description": "Code or documentation requiring manual merge"
    },
    {
      "file": "package-lock.json",
      "type": "LOCKFILE",
      "strategy": "REGENERATE_FROM_SOURCE",
      "description": "Lockfile conflict - regenerate from source"
    }
  ],
  "exit_code": 1
}
```

**Useful jq queries**:
```bash
# Get list of auto-resolvable files
just conflict-check-json | jq -r '.auto_resolvable_files[]'

# Check if safe to merge (boolean)
just conflict-check-json | jq -r '.safe_to_merge'

# Count manual review files
just conflict-check-json | jq '.manual_review_files | length'
```

---

## Integration with Other SAPs

### SAP-051 (Git Workflow)

Add conflict checking to your pre-push workflow:

```bash
# In .git/hooks/pre-push
#!/bin/bash
# Check for conflicts before pushing
just conflict-check || {
  echo "⚠️  Conflicts detected with main branch"
  echo "Run 'just conflict-check' to see details"
  exit 1
}
```

### SAP-052 (Ownership Zones)

Use ownership data to route conflict resolution:

```bash
# Find who owns conflicting files
just conflict-check-json | \
  jq -r '.manual_review_files[]' | \
  xargs just ownership-suggest-reviewers-staged
```

### SAP-010 (A-MEM)

*(Future enhancement)* Log conflict events for pattern analysis:

```json
{
  "type": "conflict_detected",
  "timestamp": "2025-11-19T14:30:00Z",
  "files": ["sprint-13.md"],
  "conflict_types": ["CONTENT"],
  "branch": "feature-123",
  "target_branch": "main"
}
```

---

## Workflows

### Pre-PR Workflow (Recommended)

```bash
# 1. You finish feature work on your branch
git add .
git commit -m "feat: add user authentication"

# 2. Check for conflicts BEFORE creating PR
just conflict-check

# 3a. If no conflicts → Create PR
gh pr create --title "Add user authentication"

# 3b. If conflicts → Resolve first
just conflict-check-json > conflicts.json
# ... resolve based on conflict types ...
# ... then create PR
```

---

### Multi-Developer Coordination (with SAP-052)

```bash
# Developer A: Working on sprint plan
git checkout -b update-sprint-13
# ... edit project-docs/sprints/sprint-13.md ...
git commit -m "Update sprint 13 deliverables"

# Check for conflicts
just conflict-check

# Output shows conflict:
# ⚠️  CONFLICTS DETECTED
# Files: project-docs/sprints/sprint-13.md
# Strategy: MANUAL_REVIEW_WITH_OWNERSHIP

# Find owner
just ownership-suggest-reviewers project-docs/sprints/sprint-13.md
# Output: @victorpiper (Project Management)

# Coordinate with owner before merging
# Message: "Hey Victor, I updated sprint-13.md, can you review?"
```

---

### CI/CD Integration

**GitHub Actions**:
```yaml
name: Check Conflicts

on:
  pull_request:
    branches: [main]

jobs:
  conflict-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Need full history for conflict check

      - name: Check for merge conflicts
        run: |
          just conflict-check
          EXIT_CODE=$?

          if [ $EXIT_CODE -eq 1 ]; then
            echo "::warning::Manual conflict resolution required"
            just conflict-check-json > conflicts.json
            cat conflicts.json
          elif [ $EXIT_CODE -eq 2 ]; then
            echo "::notice::Auto-resolvable conflicts detected"
          fi

          exit $EXIT_CODE
```

---

## Troubleshooting

### Error: "Not in a git repository"

```bash
# Ensure you're in the repository root
cd /path/to/your/repo
just conflict-check
```

### Error: "Working directory has uncommitted changes"

```bash
# Commit or stash changes first
git add .
git commit -m "WIP: feature work"

# Or stash
git stash
just conflict-check
git stash pop
```

### Error: "Already on target branch 'main'"

```bash
# You can't check conflicts while on the target branch
# Switch to your feature branch first
git checkout feature-branch
just conflict-check
```

### Error: "Target branch 'main' does not exist"

```bash
# Fetch from remote
git fetch origin main

# Or check local branches
git branch -a
```

---

## Performance

**Benchmarks** (from Phase 3 validation):
- **Detection time**: ~2 seconds (average)
- **Memory usage**: <50 MB
- **File limit**: Tested up to 100 files (no degradation)

**Expected performance**:
- Small repos (<1000 files): <3 seconds
- Medium repos (1000-10000 files): 3-10 seconds
- Large repos (>10000 files): 10-30 seconds

---

## Limitations

### Current Limitations (v1.0.0 - Detection Only)

1. **Detection only, no auto-resolution** - You must resolve conflicts manually (even for lockfiles)
2. **No A-MEM integration** - Conflict events not logged to memory system
3. **Basic whitespace detection** - May miss complex whitespace-only conflicts
4. **No conflict prediction** - Cannot predict future conflicts before they happen
5. **No pattern analysis** - Doesn't identify recurring conflict patterns

### Future Enhancements (Roadmap)

See [capability-charter.md](capability-charter.md) for full SAP-053 vision (6 tools):
- `conflict-resolver.py` - Interactive conflict resolution with escalation
- `conflict-auto-resolver.py` - Automatic resolution for lockfiles, metadata
- `conflict-predictor.py` - Predict conflicts before committing
- `conflict-pattern-detector.py` - Identify recurring patterns
- `conflict-stats.py` - Generate conflict analytics and dashboards

---

## FAQ

### Q: Should I run this before every PR?

**A**: Yes! Add it to your pre-PR checklist:
1. `just test` - Run tests
2. `just conflict-check` - Check for conflicts
3. `gh pr create` - Create PR

Or automate it in a pre-push hook (see SAP-051 integration).

### Q: What if I have auto-resolvable conflicts?

**A**: conflict-checker.py will tell you, but you still need to resolve them manually in v1.0.0. Future versions will include `conflict-auto-resolver.py` for automatic resolution.

### Q: Can I use this in CI/CD?

**A**: Yes! Use `just conflict-check-json` for structured output and check exit codes (see CI/CD Integration section).

### Q: Does this replace GitHub's conflict detection?

**A**: No, it complements it. This tool detects conflicts **before** you create a PR, saving you time. GitHub still shows conflicts after PR creation.

### Q: What about multi-file conflicts?

**A**: conflict-checker.py detects all conflicting files and classifies each one. You'll see a list of all conflicts in the output.

### Q: Can I customize conflict types?

**A**: Not in v1.0.0. Conflict types are hardcoded based on file patterns and content analysis. Future versions may support custom classification.

---

## Version History

- **v1.0.0** (2025-11-19) - Initial release (Detection-Only)
  - Pre-merge conflict detection
  - 6 conflict type classifications
  - 6 resolution strategies
  - Text and JSON output
  - Exit codes for automation
  - 15 automated tests (100% pass rate)

---

## Contributing

Found a bug or have a feature request?

1. **Report issues**: Create a GitHub issue with `[SAP-053]` prefix
2. **Contribute code**: See [CONTRIBUTING.md](../../../../CONTRIBUTING.md)
3. **Share feedback**: Provide real-world adoption feedback in ledger.md

---

## Resources

### SAP-053 Documentation

- [capability-charter.md](capability-charter.md) - Vision and scope
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [awareness-guide.md](awareness-guide.md) - Agent workflows
- [adoption-blueprint.md](adoption-blueprint.md) - 4-phase adoption plan
- [ledger.md](ledger.md) - Adoption tracking template

### Related SAPs

- **SAP-051** (Git Workflow) - Pre-push hooks, commit conventions
- **SAP-052** (Ownership Zones) - File ownership, CODEOWNERS integration
- **SAP-010** (A-MEM) - Event logging, pattern analysis

### External Resources

- [Git Merge Documentation](https://git-scm.com/docs/git-merge)
- [GitHub Conflict Resolution Guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts)

---

**Created**: 2025-11-19
**Author**: Claude (AI peer) + Victor Piper
**License**: MIT
**Trace ID**: sap-053-phase4-distribution-2025-11-19
