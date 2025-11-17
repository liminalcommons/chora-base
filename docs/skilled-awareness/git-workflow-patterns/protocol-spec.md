# Protocol Specification: Git Workflow Patterns

**SAP ID**: SAP-051
**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-16

---

## 1. Overview

Git Workflow Patterns (SAP-051) defines standardized git workflows for multi-developer collaboration across the chora ecosystem. This protocol establishes branch naming conventions, commit message standards (Conventional Commits v1.0.0), merge strategies, and automated validation via git hooks.

### Key Capabilities

- Standardized branch naming (feature/bugfix/hotfix/chore/docs prefixes)
- Conventional Commits v1.0.0 schema enforcement
- Merge strategy decision tree (squash vs merge vs rebase)
- Client-side git hooks (pre-commit, commit-msg, pre-push validation)
- Justfile automation (git-setup, validate-commits, changelog generation)
- Automated changelog generation from commit history
- Integration with SAP-001 (Inbox), SAP-010 (Memory), SAP-015 (Beads)

---

## 2. Core Contracts

### Contract 1: Branch Naming Convention

**Description**: Standardized branch naming schema for identifying work type and tracing to issues/tasks.

**Format**:
```
<type>/<identifier>-<description>

Where:
- type: feature | bugfix | hotfix | chore | docs | refactor | test
- identifier: Issue ID or beads task ID (e.g., "SAP-051" or ".beads-9rtq")
- description: Lowercase, hyphen-separated (e.g., "git-workflow-patterns")
```

**Examples**:
```bash
feature/SAP-051-git-workflow-patterns
bugfix/.beads-abc123-fix-commit-msg-hook
hotfix/COORD-2025-013-urgent-security-patch
chore/update-dependencies
docs/sap-051-protocol-spec
refactor/simplify-git-hooks
test/add-commit-msg-validation-tests
```

**Validation Rules**:
- Must match regex: `^(feature|bugfix|hotfix|chore|docs|refactor|test)\/[a-zA-Z0-9\.\-\_]+$`
- Description part must be lowercase with hyphens (no underscores or spaces)
- Identifier part should reference issue tracker (SAP ID, beads ID, COORD ID, or descriptive slug)
- Total length < 100 characters (to avoid git limitations)

**Enforcement**: Pre-push git hook validates branch name before allowing push.

---

### Contract 2: Conventional Commits v1.0.0

**Description**: Commit message schema following Conventional Commits v1.0.0 specification for consistent, parseable commit history.

**Format**:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Type**: One of:
- `feat`: New feature (correlates with MINOR in semantic versioning)
- `fix`: Bug fix (correlates with PATCH in semantic versioning)
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code change that neither fixes bug nor adds feature
- `test`: Adding or updating tests
- `chore`: Changes to build process, tooling, dependencies
- `perf`: Performance improvement
- `ci`: CI/CD configuration changes
- `build`: Build system or external dependency changes
- `revert`: Reverts a previous commit

**Scope** (optional): Noun describing section of codebase (e.g., `sap-051`, `git-hooks`, `justfile`)

**Description**: Concise summary in present tense (lowercase, no period at end)

**Body** (optional): Detailed explanation of "why" behind change (motivation, context, trade-offs)

**Footer** (optional):
- `BREAKING CHANGE: <description>` - Breaking changes (correlates with MAJOR version)
- `Refs: <issue-id>` - Reference to issue tracker
- `Co-authored-by: Name <email>` - Co-author attribution

**Examples**:
```
feat(sap-051): add git workflow patterns protocol

Implements standardized branch naming, conventional commits, and git hooks
to support multi-developer collaboration.

Refs: SAP-051, COORD-2025-013
```

```
fix(git-hooks): correct commit-msg validation regex

Previous regex failed on scopes with hyphens. Updated to allow
alphanumeric and hyphen characters in scope field.

Refs: .beads-abc123
```

```
feat(justfile)!: change git-setup recipe interface

BREAKING CHANGE: `just git-setup` now requires --confirm flag for
destructive operations. Previous behavior was too aggressive.

Migration: Run `just git-setup --confirm` to install hooks.
```

**Validation Rules**:
- Type must be one of the allowed types (see list above)
- Description must be present (non-empty)
- Description must start with lowercase letter
- Description must not end with period
- Subject line (type + scope + description) must be ≤72 characters
- Body lines must be ≤100 characters (wrapped)
- Footer must follow key: value format

**Enforcement**: commit-msg git hook validates commit message before allowing commit.

---

### Contract 3: Merge Strategy Decision Tree

**Description**: Decision tree for choosing merge strategy based on context.

**Strategies**:

**1. Squash Merge** (recommended for feature branches)
- **Use when**: Merging feature/bugfix/hotfix branches into main
- **Effect**: Collapses all commits into single commit on main
- **Benefits**: Clean linear history, one commit per feature
- **Command**: `git merge --squash <branch>`

**2. Merge Commit** (recommended for long-lived branches)
- **Use when**: Merging release branches, integrating long-lived work
- **Effect**: Preserves full commit history with merge commit
- **Benefits**: Full audit trail, preserves context
- **Command**: `git merge --no-ff <branch>`

**3. Rebase** (recommended for local branch updates)
- **Use when**: Updating feature branch with latest main
- **Effect**: Replays commits on top of main (rewrites history)
- **Benefits**: Avoids merge commits on feature branches, clean linear history
- **Command**: `git rebase main`

**Decision Tree**:
```
Is branch being merged into main?
  ├─ YES: Is it a feature/bugfix/hotfix branch?
  │   ├─ YES: Squash merge (clean history)
  │   └─ NO: Merge commit (preserve history)
  └─ NO: Is it updating feature branch with main?
      ├─ YES: Rebase (avoid merge commits)
      └─ NO: Merge commit (default strategy)
```

**Validation Rules**:
- Feature branches should be squashed when merged to main
- Rebase only for local branches (never rebase shared/pushed branches)
- Force push prohibited on main branch (server-side protection)

**Enforcement**: Documented in awareness guide, not enforced by git hooks (developer judgment required).

---

### Contract 4: Git Hook Schema

**Description**: Client-side git hooks for automated validation.

**Hook Types**:

**1. pre-commit** (validates before commit)
- **Trigger**: Before commit is created (after `git commit`)
- **Validation**: Runs linters, formatters, tests (if applicable)
- **Exit**: Non-zero exit code aborts commit

**2. commit-msg** (validates commit message)
- **Trigger**: After commit message entered (before commit finalized)
- **Validation**: Validates Conventional Commits schema
- **Exit**: Non-zero exit code aborts commit with error message

**3. pre-push** (validates before push)
- **Trigger**: Before commits pushed to remote (`git push`)
- **Validation**: Validates branch naming, checks for conflicts with main
- **Exit**: Non-zero exit code aborts push

**Hook Interface** (Bash):
```bash
#!/usr/bin/env bash
# Hook name: commit-msg
# Args: $1 = path to commit message file
# Exit: 0 = success, 1 = failure

set -e  # Exit on first error

COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Validation logic here
# ...

# Exit 0 if valid, exit 1 if invalid
exit 0
```

**Hook Storage**:
- Hooks stored in: `chora-base/.githooks/` (version controlled)
- Installed to: `<repo>/.git/hooks/` (via `git config core.hooksPath`)
- Symlink pattern: `git config core.hooksPath .githooks`

**Validation Criteria**:
- Hooks must be executable (`chmod +x`)
- Hooks must exit 0 (success) or non-zero (failure)
- Hooks should provide clear error messages on failure
- Hooks should run in <500ms (minimal developer friction)

---

### Contract 5: Justfile Automation Interface

**Description**: Justfile recipes for git workflow automation.

**Recipe Signatures**:

**1. git-setup** - Install git hooks
```bash
just git-setup [--confirm]

# Installs git hooks from .githooks/ to .git/hooks/
# --confirm: Skip confirmation prompt (for CI/CD)
```

**2. validate-commits** - Validate commit messages in branch
```bash
just validate-commits [<ref>]

# Validates all commits from <ref> to HEAD
# Default <ref>: origin/main
# Exit 0 if all valid, exit 1 if any invalid
```

**3. changelog** - Generate changelog from commits
```bash
just changelog [--since=<ref>] [--output=<file>]

# Generates changelog from conventional commits
# --since: Start ref (default: last tag)
# --output: Output file (default: CHANGELOG.md)
```

**4. git-check** - Quick validation (hooks + commits + branch)
```bash
just git-check

# Validates:
# - Git hooks installed
# - Current branch name follows convention
# - Recent commits follow conventional commits
# Exit 0 if all valid, exit 1 if any invalid
```

**Recipe Dependencies**:
- Requires `just` v1.0.0+
- Requires `git` v2.25.0+
- Python 3.11+ (for commit message parsing)
- Optional: `conventional-changelog` tool (for advanced changelog generation)

---

## 3. Integration Patterns

### Integration with SAP-001 (Inbox Coordination)

**Integration Point**: Commit messages reference coordination request IDs

**Pattern**:
```bash
# Coordination request work uses COORD ID in commit scope
git commit -m "feat(coord-2025-013): implement sap-051 git hooks

Implements git workflow patterns as defined in COORD-2025-013.

Refs: COORD-2025-013, SAP-051"
```

**Benefits**:
- Traceability from commit to coordination request
- A-MEM events can correlate commits with coordination workflow
- `git log --grep="COORD-2025-013"` finds all related commits

---

### Integration with SAP-010 (Memory System)

**Integration Point**: Commit SHAs logged in A-MEM events

**Pattern**:
```json
{
  "event_type": "sap_artifact_created",
  "timestamp": "2025-11-16T16:00:00Z",
  "sap_id": "SAP-051",
  "artifact": "capability_charter",
  "git_commit": "a1b2c3d4",
  "details": {
    "file": "chora-base/docs/skilled-awareness/git-workflow-patterns/capability-charter.md"
  }
}
```

**Benefits**:
- A-MEM queries can find commits associated with events
- `git show <commit-sha>` provides context for A-MEM events
- Event correlation via commit SHAs (trace work across sessions)

---

### Integration with SAP-015 (Beads Task Tracking)

**Integration Point**: Branch names and commit messages reference beads task IDs

**Pattern**:
```bash
# Create branch for beads task
git checkout -b feature/.beads-9rtq-sap-051-charter

# Commit references beads task
git commit -m "feat(.beads-9rtq): create sap-051 capability charter

Completes beads task for COORD-2025-013 charter deliverable.

Refs: .beads-9rtq, COORD-2025-013, SAP-051"
```

**Benefits**:
- Beads task completion correlates with git commits
- `git log --grep=".beads-9rtq"` finds all commits for task
- Branch name indicates which beads task is being worked on

---

### Integration with SAP-012 (Development Lifecycle)

**Integration Point**: Conventional commit types align with DDD → BDD → TDD phases

**Mapping**:
- **DDD (Design)**: `docs:` commits for design documents, RFCs, ADRs
- **BDD (Behavior)**: `feat:` commits for feature implementation
- **TDD (Testing)**: `test:` commits for test implementation
- **Refactoring**: `refactor:` commits between phases

**Pattern**:
```bash
# DDD: Document design
git commit -m "docs(sap-051): add protocol specification

Defines technical contracts for git workflow patterns."

# BDD: Implement feature
git commit -m "feat(sap-051): add commit-msg validation hook

Validates conventional commits schema before allowing commit."

# TDD: Add tests
git commit -m "test(sap-051): add commit-msg hook validation tests

Tests valid and invalid commit message formats."
```

---

## 4. Configuration

### Configuration Schema

Git hooks configuration uses `.git/config` for per-repo settings:

```ini
[core]
    hooksPath = .githooks  # Use versioned hooks instead of .git/hooks

[hooks]
    # Enable/disable specific hooks
    commit-msg-enabled = true
    pre-push-enabled = true
    pre-commit-enabled = false  # Disabled by default (optional)

[conventional-commits]
    # Conventional commits configuration
    types = feat,fix,docs,style,refactor,test,chore,perf,ci,build,revert
    scopes =   # Optional: Restrict allowed scopes (empty = any scope)
    max-subject-length = 72
    max-body-line-length = 100
    require-scope = false  # Optional: Require scope in all commits

[branch-naming]
    # Branch naming configuration
    types = feature,bugfix,hotfix,chore,docs,refactor,test
    require-identifier = true  # Require issue/task ID in branch name
    max-length = 100
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GIT_HOOKS_ENABLED` | No | `true` | Enable/disable all git hooks |
| `COMMIT_MSG_VALIDATION` | No | `true` | Enable commit message validation |
| `BRANCH_NAME_VALIDATION` | No | `true` | Enable branch name validation |
| `CONVENTIONAL_COMMITS_STRICT` | No | `false` | Strict mode (fail on warnings) |
| `GIT_WORKFLOW_DEBUG` | No | `false` | Enable debug output in hooks |

### Justfile Configuration

Justfile recipes use variables for configuration:

```makefile
# Git workflow configuration
git_hooks_dir := ".githooks"
git_default_branch := "main"
changelog_output := "CHANGELOG.md"
changelog_tool := "git-cliff"  # Or "conventional-changelog"

# Validation strictness
strict_validation := "false"
```

---

## 5. Error Handling

### Error Codes

| Code | Error | Cause | Resolution |
|------|-------|-------|------------|
| `SAP-051-001` | Invalid commit message format | Commit doesn't follow Conventional Commits | Fix commit message to match schema: `<type>: <description>` |
| `SAP-051-002` | Invalid branch name | Branch doesn't follow naming convention | Rename branch: `git branch -m <new-name>` |
| `SAP-051-003` | Git hooks not installed | `.git/config` not configured for hooks | Run `just git-setup` to install hooks |
| `SAP-051-004` | Hook validation failed | Pre-commit/pre-push checks failed | Review hook output, fix issues, retry |
| `SAP-051-005` | Changelog generation failed | Commits don't follow Conventional Commits | Ensure all commits use conventional format |
| `SAP-051-006` | Merge conflict with main | Branch has conflicts with main branch | Rebase branch on main: `git rebase main` |

### Common Errors

**Error: "commit message doesn't follow Conventional Commits format"**
- **Cause**: Commit message missing type prefix (e.g., `feat:`, `fix:`)
- **Solution**: Amend commit message: `git commit --amend -m "feat: <description>"`

**Error: "branch name doesn't follow convention"**
- **Cause**: Branch name doesn't start with allowed type (feature/bugfix/hotfix/chore/docs)
- **Solution**: Rename branch: `git branch -m feature/<identifier>-<description>`

**Error: "git hooks not installed"**
- **Cause**: `core.hooksPath` not set in `.git/config`
- **Solution**: Run `just git-setup` to configure hooks

**Error: "pre-push validation failed: conflicts with main"**
- **Cause**: Current branch has merge conflicts with main branch
- **Solution**: Rebase on main: `git fetch origin main && git rebase origin/main`

---

## 6. Security Considerations

### Hook Execution Security

**Risk**: Git hooks execute arbitrary code - malicious hooks can compromise system.

**Mitigations**:
1. **Version control hooks** - Store hooks in `.githooks/` (reviewable, auditable)
2. **Explicit installation** - Require `just git-setup` to install hooks (opt-in, not automatic)
3. **Code review** - All hook changes require PR review before merge
4. **Minimal dependencies** - Hooks use Bash + Python stdlib only (no external packages)

### Commit Message Sanitization

**Risk**: Commit messages could contain secrets (passwords, API keys, tokens).

**Mitigations**:
1. **Pre-commit secret scanning** - Optionally integrate with `git-secrets` or `trufflehog`
2. **Commit message linting** - Warn on suspicious patterns (e.g., `password=`, `token=`)
3. **Developer training** - Document best practices for commit messages (no secrets)

### Branch Protection

**Risk**: Force push to main branch could corrupt git history.

**Mitigations**:
1. **Server-side protection** - Configure GitHub branch protection rules (block force push on main)
2. **Pre-push validation** - Warn on force push attempts in pre-push hook
3. **Documentation** - Explicitly document that force push is prohibited on shared branches

---

## 7. Performance Requirements

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| commit-msg hook | < 100ms | Time from commit to hook completion |
| pre-push hook | < 500ms | Time from push to hook completion |
| validate-commits recipe | < 2s per 100 commits | `time just validate-commits` |
| changelog generation | < 5s per 1000 commits | `time just changelog` |
| git-setup installation | < 5s | `time just git-setup` |

### Resource Usage

- **Disk**: Hooks total < 50 KB (minimal storage footprint)
- **Memory**: Hook execution < 10 MB RSS (lightweight, no heavy parsing)
- **CPU**: Hooks single-threaded (no parallelization needed for small repos)

### Scalability

- **Small repos** (< 1000 commits): All operations < 1s
- **Medium repos** (1000-10k commits): validate-commits < 10s, changelog < 30s
- **Large repos** (> 10k commits): Consider batching (validate recent commits only)

---

## 8. Examples

### Example 1: Basic Workflow

**Scenario**: Create feature branch, make commits, merge to main

```bash
# Create feature branch
git checkout -b feature/SAP-051-git-workflow

# Make commits (conventional format)
git commit -m "feat(sap-051): add protocol specification"
git commit -m "docs(sap-051): update charter with examples"
git commit -m "test(sap-051): add commit-msg validation tests"

# Validate commits before pushing
just validate-commits

# Push to remote
git push -u origin feature/SAP-051-git-workflow

# Create PR, get review, then merge (squash merge recommended)
# GitHub UI: Merge pull request (squash and merge)
```

**Expected Output**:
```
✓ commit-msg validation passed (3 commits)
✓ branch name valid: feature/SAP-051-git-workflow
✓ no conflicts with main
✓ ready to push
```

### Example 2: Fix Invalid Commit Message

**Scenario**: Commit message doesn't follow Conventional Commits

```bash
# Attempt commit with invalid message
git commit -m "added new feature"

# Error from commit-msg hook:
# ❌ Commit message doesn't follow Conventional Commits format
# Expected: <type>(<scope>): <description>
# Examples:
#   feat(sap-051): add new feature
#   fix(git-hooks): correct validation regex
#
# Commit aborted.

# Fix: Amend commit message
git commit --amend -m "feat(sap-051): add git workflow patterns"

# Success:
# ✓ commit-msg validation passed
# [feature/SAP-051-git-workflow a1b2c3d] feat(sap-051): add git workflow patterns
```

### Example 3: Generate Changelog

**Scenario**: Generate changelog from conventional commits

```bash
# Generate changelog for all commits since v1.0.0 tag
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

### Documentation
- **sap-051**: update charter with examples (c3d4e5f)

### Tests
- **sap-051**: add commit-msg validation tests (d4e5f6g)
```

---

## 9. Validation & Testing

### Validation Commands

```bash
# Validate git hooks are installed
git config --get core.hooksPath
# Expected: .githooks

# Validate commit messages in current branch
just validate-commits
# Expected: ✓ All commits valid

# Validate branch name
just git-check
# Expected: ✓ Branch name valid

# Test commit-msg hook manually
echo "invalid commit message" > /tmp/test-commit-msg
.githooks/commit-msg /tmp/test-commit-msg
# Expected: Exit code 1 (failure)

echo "feat(sap-051): valid commit message" > /tmp/test-commit-msg
.githooks/commit-msg /tmp/test-commit-msg
# Expected: Exit code 0 (success)
```

### Test Cases

**Test Case 1**: Valid conventional commit
- **Given**: Commit message "feat(sap-051): add git workflow patterns"
- **When**: commit-msg hook executes
- **Then**: Hook exits 0 (success), commit allowed

**Test Case 2**: Invalid commit message (missing type)
- **Given**: Commit message "added new feature"
- **When**: commit-msg hook executes
- **Then**: Hook exits 1 (failure), commit aborted, error message shown

**Test Case 3**: Valid branch name
- **Given**: Branch name "feature/SAP-051-git-workflow"
- **When**: pre-push hook executes
- **Then**: Hook exits 0 (success), push allowed

**Test Case 4**: Invalid branch name
- **Given**: Branch name "my-feature-branch"
- **When**: pre-push hook executes
- **Then**: Hook exits 1 (failure), push aborted, error message shown

---

## 10. Versioning & Compatibility

### Version Compatibility

**Current Version**: 1.0.0

**Compatibility Guarantees**:
- Patch versions (1.0.x): Backward compatible bug fixes to hooks, no schema changes
- Minor versions (1.x.0): Backward compatible new features (e.g., new commit types, new hooks)
- Major versions (x.0.0): Breaking changes (e.g., Conventional Commits schema changes, hook interface changes)

**Migration Path**:
- 1.0.x → 1.x.0: Re-run `just git-setup` to update hooks (no config changes)
- 1.x.0 → 2.0.0: Follow migration guide (config schema may change, hook interface may change)

### Dependency Compatibility

| Dependency | Minimum Version | Tested Version | Status |
|------------|----------------|----------------|--------|
| Git | 2.25.0 | 2.43.0 | ✅ Compatible |
| Bash | 4.0 | 5.2 | ✅ Compatible |
| Python | 3.11.0 | 3.12.0 | ✅ Compatible |
| Just | 1.0.0 | 1.16.0 | ✅ Compatible |

### Conventional Commits Version

SAP-051 implements **Conventional Commits v1.0.0** specification.

Specification: https://www.conventionalcommits.org/en/v1.0.0/

**Compatibility**:
- If Conventional Commits releases v2.0.0, SAP-051 will create migration path (major version bump)
- Current implementation is strict v1.0.0 (no extensions, no custom types)

---

## 11. Related Specifications

### Within chora-base

**SAP Artifacts**:
- [Capability Charter](./capability-charter.md) - Problem statement and scope
- [Awareness Guide](./awareness-guide.md) - AI agent quick reference
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Traceability Ledger](./ledger.md) - Version history and adoption tracking

**Related SAPs**:
- [SAP-001: Inbox Coordination Protocol](../inbox/protocol-spec.md) - Coordination requests reference git commits
- [SAP-010: Memory System](../memory-system/protocol-spec.md) - A-MEM events log commit SHAs
- [SAP-015: Task Tracking](../task-tracking/protocol-spec.md) - Beads tasks correlate with git branches
- [SAP-012: Development Lifecycle](../development-lifecycle/protocol-spec.md) - DDD → BDD → TDD aligns with commit types

**Dependent SAPs** (build on SAP-051):
- SAP-052: Ownership Zones - Uses git hooks for PR automation
- SAP-053: Conflict Resolution - Uses pre-merge hooks, commit SHAs
- SAP-054: Work Partitioning - Uses branch analysis, commit clustering
- SAP-055: Multi-Dev Awareness - Documents git workflow patterns

### External Specifications

- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) - Commit message specification
- [Semantic Versioning 2.0.0](https://semver.org/) - Version numbering scheme
- [Git Hooks Documentation](https://git-scm.com/docs/githooks) - Git hook interface specification
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches) - Server-side branch protection

---

**Version History**:
- **1.0.0** (2025-11-16): Initial protocol specification for Git Workflow Patterns
