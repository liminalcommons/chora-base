# Adoption Blueprint: Git Workflow Patterns

**SAP ID**: SAP-051
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-051 Git Workflow Patterns across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Install git hooks, basic validation | 5-10 min | Minimal (quarterly hook updates) | New repositories, pilot projects, development environments |
| **Level 2: Advanced** | Custom configuration, integrate with SAP-001/015 | 15-30 min | Low (monthly reviews) | Active projects, multi-developer teams |
| **Level 3: Mastery** | Full integration, automated changelog, CI/CD validation | 30-60 min | Medium (sprint reviews) | **Recommended for production** |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption over 2-4 weeks)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
- Getting started with Git Workflow Patterns
- Installing git hooks for commit message and branch name validation
- Development and testing environments
- Quick proof-of-concept before team-wide rollout
- Individual developer adoption (no team coordination required)

### Time Estimate

- **Setup**: 5-10 minutes
- **Learning Curve**: Minimal (conventional commits take 1-2 commits to internalize)

### Prerequisites

**Required**:
- Git 2.25.0+ installed (`git --version`)
- Just 1.0.0+ installed (`just --version`)
- Repository cloned locally with `.githooks/` directory
- Write access to repository

**Recommended**:
- Python 3.11+ (for advanced commit message parsing, optional for basic hooks)
- Familiarity with git basics (commit, push, branch)

### Step-by-Step Instructions

#### Step 1.1: Verify Prerequisites

**Action**:
```bash
# Check git version
git --version

# Check just is installed
just --version

# Check .githooks/ directory exists (if not, see troubleshooting)
ls .githooks/
```

**Expected Output**:
```
git version 2.43.0
just 1.16.0
commit-msg  pre-push  pre-commit  (git hook scripts)
```

**Verification**:
```bash
# Verify hooks are executable
ls -lh .githooks/
# All hooks should have 'x' permission
```

---

#### Step 1.2: Install Git Hooks

**Action**:
```bash
# Install git hooks via justfile recipe
just git-setup
```

**Expected Output**:
```
Installing git hooks from .githooks/...
✓ Configured git to use .githooks/ for hooks
✓ commit-msg hook active
✓ pre-push hook active
✓ pre-commit hook active (optional)
Git hooks installed successfully!
```

**What this does**:
- Sets `core.hooksPath = .githooks` in `.git/config`
- Git will now run hooks from `.githooks/` instead of `.git/hooks/`
- Hooks are version-controlled (in repo) not local (in .git/)

**Verification**:
```bash
# Check git config
git config --get core.hooksPath
# Expected: .githooks
```

---

#### Step 1.3: Test Commit Message Validation

**Action**:
```bash
# Create a test file
echo "test" > test-file.txt
git add test-file.txt

# Try committing with INVALID message (should fail)
git commit -m "added test file"
```

**Expected Output** (hook should reject commit):
```
❌ Commit message doesn't follow Conventional Commits format
Expected: <type>(<scope>): <description>

Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert

Examples:
  feat(sap-051): add git workflow patterns
  fix(git-hooks): correct validation regex
  docs(readme): update installation instructions

Commit aborted.
```

**Now try with VALID message**:
```bash
# Commit with conventional format (should succeed)
git commit -m "chore: add test file for git hook validation"
```

**Expected Output**:
```
✓ commit-msg validation passed
[feature/SAP-051-git-hooks a1b2c3d] chore: add test file for git hook validation
 1 file changed, 1 insertion(+)
 create mode 100644 test-file.txt
```

**Verification**:
```bash
# Check commit was created
git log -1 --oneline
# Expected: a1b2c3d chore: add test file for git hook validation
```

---

#### Step 1.4: Test Branch Name Validation

**Action**:
```bash
# Check current branch name
git branch --show-current

# If branch name is invalid (e.g., "main", "my-branch"), create valid test branch
git checkout -b feature/SAP-051-test-branch
```

**Expected Output**:
```
Switched to a new branch 'feature/SAP-051-test-branch'
```

**Test pre-push hook**:
```bash
# Run git-check to validate branch name
just git-check
```

**Expected Output**:
```
✓ Git hooks installed
✓ Branch name valid: feature/SAP-051-test-branch
✓ Recent commits follow Conventional Commits
All checks passed!
```

**Verification**:
```bash
# Try invalid branch name (create locally, don't push)
git checkout -b my-invalid-branch

# Run git-check (should warn)
just git-check
# Expected: ❌ Branch name doesn't follow convention
```

---

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] `git config --get core.hooksPath` returns `.githooks`
- [ ] commit-msg hook rejects invalid commit messages (tested above)
- [ ] commit-msg hook accepts valid conventional commits (tested above)
- [ ] `just git-check` validates branch name
- [ ] Pre-push hook is active (will validate before push)

#### Validation Commands

```bash
# Comprehensive validation
just git-check

# Expected output:
# ✓ Git hooks installed
# ✓ Branch name valid
# ✓ Recent commits follow Conventional Commits
# All checks passed!
```

### Common Issues (Level 1)

**Issue 1**: `just: command not found`
- **Cause**: Just (command runner) not installed
- **Solution**: Install just: https://github.com/casey/just#installation
  - macOS: `brew install just`
  - Linux: `cargo install just` or package manager
  - Windows: `scoop install just` or `choco install just`

**Issue 2**: `.githooks/` directory doesn't exist
- **Cause**: Repository doesn't have SAP-051 infrastructure yet
- **Solution**: This is expected - SAP-051 infrastructure is created during Phase 2 (Infrastructure Development). For now, wait for chora-base to publish SAP-051 with `.githooks/` directory.

**Issue 3**: Hooks not running (commits succeed with invalid messages)
- **Cause**: `core.hooksPath` not set correctly
- **Solution**: Re-run `just git-setup` or manually set:
  ```bash
  git config core.hooksPath .githooks
  ```

**Issue 4**: Permission denied when running hooks
- **Cause**: Hooks not executable
- **Solution**: Make hooks executable:
  ```bash
  chmod +x .githooks/*
  ```

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds:
- Custom git workflow configuration (commit types, branch types, validation strictness)
- Integration with SAP-001 (Inbox) for coordination request tracing
- Integration with SAP-015 (Beads) for task tracking
- Validation automation in editor/IDE (optional)
- Team-wide adoption patterns

### Time Estimate

- **Setup**: 15-30 minutes (incremental from Level 1)
- **Total from Start**: 20-40 minutes

### Prerequisites

**Required**:
- ✅ Level 1 adoption complete (git hooks installed and tested)
- Python 3.11+ installed (for advanced parsing)
- Repository uses SAP-001 inbox (optional, for coordination tracing)
- Repository uses SAP-015 beads (optional, for task tracking)

### Step-by-Step Instructions

#### Step 2.1: Configure Custom Commit Types

**Action**:
```bash
# Edit .git/config to customize conventional commits
git config conventional-commits.types "feat,fix,docs,style,refactor,test,chore,coord,sap"

# Add custom scopes (optional)
git config conventional-commits.scopes "sap-051,git-hooks,justfile,docs,tests"

# Set max subject length (default: 72)
git config conventional-commits.max-subject-length 72
```

**Expected Output**:
```
# No output, but config is updated
```

**Verification**:
```bash
# Check config was set
git config --get conventional-commits.types
# Expected: feat,fix,docs,style,refactor,test,chore,coord,sap
```

**What this enables**:
- Custom commit types (e.g., `coord:` for coordination requests, `sap:` for SAP work)
- Scoped validation (optional: restrict allowed scopes)
- Configurable subject length limits

---

#### Step 2.2: Integrate with SAP-001 (Inbox Coordination)

**Action**:
When working on coordination requests, reference COORD ID in commits:

```bash
# Commit format for coordination request work
git commit -m "feat(coord-2025-013): implement sap-051 git hooks

Implements git workflow patterns as defined in COORD-2025-013.

Refs: COORD-2025-013, SAP-051"
```

**Expected Output**:
```
✓ commit-msg validation passed
[feature/SAP-051-git-hooks b2c3d4e] feat(coord-2025-013): implement sap-051 git hooks
```

**Benefits**:
- Commits trace to coordination requests
- `git log --grep="COORD-2025-013"` finds all related work
- A-MEM events can correlate commits with coordination workflow

---

#### Step 2.3: Integrate with SAP-015 (Beads Task Tracking)

**Action**:
When working on beads tasks, include task ID in branch name and commits:

```bash
# Create branch with beads task ID
bd show .beads-9rtq  # Get task description
git checkout -b feature/.beads-9rtq-sap-051-charter

# Commit with beads task ID
git commit -m "feat(.beads-9rtq): create sap-051 capability charter

Completes beads task for COORD-2025-013 charter deliverable.

Refs: .beads-9rtq, COORD-2025-013, SAP-051"
```

**Expected Output**:
```
✓ commit-msg validation passed
[feature/.beads-9rtq-sap-051-charter c3d4e5f] feat(.beads-9rtq): create sap-051 capability charter
```

**Benefits**:
- `git log --grep=".beads-9rtq"` finds all commits for task
- Beads task completion correlates with git commits
- Full traceability: beads task → commits → coordination request

---

#### Step 2.4: Configure Validation Strictness

**Action**:
```bash
# Enable strict mode (fail on warnings, not just errors)
git config conventional-commits.strict true

# Require scope in all commits (optional, more restrictive)
git config conventional-commits.require-scope false  # Keep false for flexibility

# Enable debug output (for troubleshooting hooks)
export GIT_WORKFLOW_DEBUG=true
```

**Expected Output**:
```
# No output, config updated
```

**Verification**:
```bash
# Check strict mode is enabled
git config --get conventional-commits.strict
# Expected: true
```

---

#### Step 2.5: Use Convenience Recipes (Level 2 Helpers)

**Action**:
Use justfile recipes for easier Level 2 configuration:

```bash
# Configure custom settings with one command
just git-config-custom "feat,fix,docs,custom" "80" "true"

# Show current configuration
just git-config-show

# Reset to defaults if needed
just git-config-reset

# Generate commit message template with SAP integration
just git-commit-template "sap-051" "feat"
# Auto-extracts SAP-051, COORD-XXX, .beads-xxx from branch name
# Outputs: feat(sap-051): <description>
#
#          Refs: SAP-051
```

**Expected Output (git-config-show)**:
```
Current Git Workflow Configuration:
====================================

Hooks:
  core.hooksPath = .githooks
  commit-msg enabled = true
  pre-push enabled = true
  pre-commit enabled = false

Commit Message Rules:
  types = feat,fix,docs,custom
  max subject length = 80
  strict mode = true

Branch Naming Rules:
  types = feature,bugfix,hotfix,chore,docs,refactor,test
  max length = 100
  check conflicts = false
```

**Benefits**:
- One-command configuration (no manual git config editing)
- Visual confirmation of current settings
- Easy reset to defaults
- Auto-generate commit messages with SAP/COORD/beads IDs from branch names

**Recipe Details**:
- `git-config-custom TYPES MAX_LENGTH STRICT`: Configure commit types, max length, strict mode
- `git-config-show`: Display current configuration in readable format
- `git-config-reset`: Reset all git workflow config to defaults
- `git-commit-template SCOPE TYPE`: Generate commit template extracting IDs from branch

---

### Configuration

#### Level 2 Git Configuration

**.git/config** (example):
```ini
[core]
    hooksPath = .githooks

[hooks]
    commit-msg-enabled = true
    pre-push-enabled = true
    pre-commit-enabled = false  # Optional: Enable for pre-commit linting

[conventional-commits]
    types = feat,fix,docs,style,refactor,test,chore,perf,ci,build,revert,coord,sap
    scopes = sap-051,git-hooks,justfile,docs,tests,coord-2025-013,.beads-9rtq
    max-subject-length = 72
    max-body-line-length = 100
    require-scope = false
    strict = true

[branch-naming]
    types = feature,bugfix,hotfix,chore,docs,refactor,test
    require-identifier = true
    max-length = 100
```

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] Custom commit types configured (if using)
- [ ] SAP-001 coordination request workflow tested (COORD ID in commits)
- [ ] SAP-015 beads task workflow tested (beads ID in branch name and commits)
- [ ] `just validate-commits` passes for all commits in branch
- [ ] Strict mode validated (if enabled)

#### Validation Commands

```bash
# Validate all commits in current branch
just validate-commits

# Expected output:
# Validating commits from origin/main..HEAD
# ✓ commit a1b2c3d valid: feat(sap-051): add git hooks
# ✓ commit b2c3d4e valid: docs(sap-051): update readme
# All commits valid (2/2)
```

---

## Level 3: Mastery (Production-Ready)

### Purpose

Level 3 adoption adds:
- Automated changelog generation from conventional commits
- CI/CD integration (GitHub Actions validation)
- Team onboarding documentation
- Full SAP-010 (A-MEM) integration for event correlation
- Quarterly hook maintenance and updates

### Time Estimate

- **Setup**: 30-60 minutes (incremental from Level 2)
- **Total from Start**: 50-90 minutes

### Prerequisites

**Required**:
- ✅ Level 2 adoption complete (custom configuration, SAP integration)
- GitHub Actions enabled (for CI/CD validation)
- SAP-010 (Memory System) adopted (for A-MEM integration)
- Team trained on Conventional Commits (documentation or workshop)

### Step-by-Step Instructions

#### Step 3.1: Set Up Automated Changelog Generation

**Action**:
```bash
# Generate changelog from all commits since v1.0.0 tag
just changelog --since=v1.0.0 --output=CHANGELOG.md

# Preview changelog
cat CHANGELOG.md
```

**Expected Output** (CHANGELOG.md):
```markdown
# Changelog

## [1.1.0] - 2025-11-16

### Features
- **sap-051**: add git workflow patterns protocol (a1b2c3d)
- **sap-051**: implement commit-msg validation hook (b2c3d4e)
- **coord-2025-013**: complete SAP-051 infrastructure (c3d4e5f)

### Documentation
- **sap-051**: update charter with examples (d4e5f6g)
- **readme**: add installation instructions (e5f6g7h)

### Tests
- **sap-051**: add commit-msg validation tests (f6g7h8i)

### Chores
- **deps**: update git dependency to 2.43.0 (g7h8i9j)
```

**Automation**:
Add changelog generation to release workflow:
```bash
# In release script
just changelog --since=$(git describe --tags --abbrev=0) --output=CHANGELOG-new.md
cat CHANGELOG-new.md >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: update changelog for $(git describe --tags --abbrev=0)"
```

---

#### Step 3.2: Add CI/CD Validation (GitHub Actions)

**Action**:
Create `.github/workflows/git-validation.yml`:

```yaml
name: Git Workflow Validation

on:
  pull_request:
    branches: [main]
  push:
    branches: [main, feature/*, bugfix/*, hotfix/*]

jobs:
  validate-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history for validation

      - name: Install Just
        run: curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

      - name: Validate Commit Messages
        run: just validate-commits

      - name: Validate Branch Name
        if: github.event_name == 'pull_request'
        run: just git-check

      - name: Generate Changelog Preview
        if: github.event_name == 'pull_request'
        run: |
          just changelog --since=origin/main --output=CHANGELOG-preview.md
          cat CHANGELOG-preview.md >> $GITHUB_STEP_SUMMARY
```

**Expected Output**:
- GitHub Actions run on every PR and push
- Validates all commits follow Conventional Commits
- Validates branch name follows convention
- Generates changelog preview in PR summary

---

#### Step 3.3: Integrate with SAP-010 (A-MEM Event Logging)

**Action**:
Log git commits in A-MEM events:

```bash
# When creating significant commit, log A-MEM event
cat >> .chora/memory/events/2025-11.jsonl << EOF
{
  "event_type": "sap_artifact_created",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "sap_id": "SAP-051",
  "artifact": "capability_charter",
  "git_commit": "$(git rev-parse HEAD)",
  "trace_id": "multi-dev-sap-051-2025-11-16",
  "details": {
    "file": "chora-base/docs/skilled-awareness/git-workflow-patterns/capability-charter.md",
    "commit_message": "$(git log -1 --pretty=format:%s)"
  }
}
EOF
```

**Benefits**:
- A-MEM events include commit SHA for full traceability
- `git show <commit-sha>` provides context for A-MEM events
- Event correlation via commit SHAs across sessions

---

#### Step 3.4: Create Team Onboarding Documentation

**Action**:
Create `docs/git-workflow-guide.md`:

```markdown
# Git Workflow Guide (SAP-051)

## Quick Start

1. Install git hooks: `just git-setup`
2. Create branch: `git checkout -b feature/YOUR-TASK-description`
3. Commit: `git commit -m "feat(scope): description"`
4. Push: `git push`

## Commit Message Format

**Template**: `<type>(<scope>): <description>`

**Examples**:
- `feat(sap-051): add new feature`
- `fix(git-hooks): correct bug in validation`
- `docs(readme): update installation guide`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Add/update tests
- `chore`: Maintenance tasks

## Branch Naming

**Template**: `<type>/<identifier>-<description>`

**Examples**:
- `feature/SAP-051-git-workflow`
- `bugfix/.beads-abc-fix-validation`
- `hotfix/urgent-security-patch`

## FAQ

**Q: Why do I need to follow this format?**
A: Enables automated changelog generation and keeps git history clean.

**Q: What if the hook rejects my commit?**
A: Fix the commit message format with `git commit --amend -m "..."`.
```

---

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] Changelog generation works (`just changelog` produces valid output)
- [ ] CI/CD validation passes on PRs
- [ ] A-MEM events include commit SHAs
- [ ] Team documentation created and accessible
- [ ] All team members trained on Conventional Commits
- [ ] Quarterly hook maintenance scheduled

#### Validation Commands

```bash
# Test changelog generation
just changelog --since=v1.0.0 --output=/tmp/test-changelog.md
cat /tmp/test-changelog.md

# Validate CI/CD workflow syntax
actionlint .github/workflows/git-validation.yml  # If actionlint installed

# Check A-MEM events include git commits
grep "git_commit" .chora/memory/events/2025-11.jsonl | head -3
```

---

## Upgrade Paths

### Upgrading from No SAP-051 → Level 1

1. Run `just git-setup`
2. Test commit message validation
3. Fix any existing commits if needed: `git rebase -i origin/main` + amend messages

### Upgrading from Level 1 → Level 2

1. Configure custom commit types (Step 2.1)
2. Update documentation with SAP-001/015 integration patterns (Step 2.2-2.3)
3. Set validation strictness (Step 2.4)

### Upgrading from Level 2 → Level 3

1. Set up changelog automation (Step 3.1)
2. Add CI/CD validation (Step 3.2)
3. Integrate with SAP-010 A-MEM (Step 3.3)
4. Create team onboarding docs (Step 3.4)

---

## Rollback Procedures

### Disable Git Hooks Temporarily

```bash
# Disable all hooks
git config --unset core.hooksPath

# Or disable specific hooks
git config hooks.commit-msg-enabled false
git config hooks.pre-push-enabled false
```

### Permanently Remove SAP-051

```bash
# Unset git config
git config --unset core.hooksPath
git config --remove-section hooks
git config --remove-section conventional-commits

# Remove .githooks/ directory (if desired)
rm -rf .githooks/
```

---

## Maintenance

### Quarterly Hook Updates

```bash
# Update hooks from chora-base (if using as submodule)
cd chora-base
git pull origin main
cd ..

# Re-run git-setup to update hooks
just git-setup
```

### Monitoring Adoption

```bash
# Check team compliance
just validate-commits

# Generate adoption report
git log --since="1 month ago" --pretty=format:"%s" | grep -E "^(feat|fix|docs|refactor|test|chore):" | wc -l
# Shows number of conventional commits in last month
```

---

**Version**: 1.0.0 (2025-11-16)
**Next**: See [Traceability Ledger](./ledger.md) for adoption tracking across ecosystem
