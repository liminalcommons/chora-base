# Git Workflow Quick Start (SAP-051)

**For**: New team members adopting SAP-051 Git Workflow Patterns
**Time**: 5-10 minutes to get started
**Level**: Beginner-friendly

---

## TL;DR - Quick Commands

```bash
# 1. Install git hooks (one-time setup)
just git-setup

# 2. Create a branch
git checkout -b feature/YOUR-TASK-description

# 3. Make changes and commit
git add .
git commit -m "feat(scope): your change description"

# 4. Validate before push
just git-check

# 5. Push
git push
```

Done! Your commits now follow team conventions automatically.

---

## Why This Matters

**Problem**: Without conventions, git history becomes chaotic:
- ❌ "fixed stuff"
- ❌ "updates"
- ❌ "asdf"
- ❌ Branches named "test", "final", "final-final-v2"

**Solution**: SAP-051 enforces conventions automatically:
- ✅ `feat(auth): add user login`
- ✅ `fix(api): correct validation bug`
- ✅ Branches: `feature/SAP-051-user-auth`
- ✅ Auto-generated changelogs
- ✅ Full traceability

**Team Benefits**:
- Changelog generation from commits (no manual CHANGELOG.md)
- Easy `git log` filtering (`git log --grep="feat"`)
- Clearer code reviews
- Better release notes

---

## Installation (5 minutes)

### Step 1: Install Git Hooks

```bash
# In your project directory
just git-setup
```

**What this does**:
- Installs commit message validation hook
- Installs branch name validation hook
- Configures git to use `.githooks/` directory

**Verify**:
```bash
git config --get core.hooksPath
# Expected: .githooks
```

### Step 2: Test It Works

```bash
# Try an INVALID commit (should fail)
git commit --allow-empty -m "test commit"
# ❌ Error: doesn't follow Conventional Commits format

# Try a VALID commit (should succeed)
git commit --allow-empty -m "test: verify git hooks working"
# ✓ commit-msg validation passed
```

If both tests work as expected, you're ready!

---

## Daily Workflow

### 1. Creating Branches

**Format**: `<type>/<identifier>-<description>`

**Examples**:
```bash
# Feature branch
git checkout -b feature/SAP-051-user-authentication

# Bug fix branch
git checkout -b bugfix/.beads-abc-login-error

# Hotfix branch
git checkout -b hotfix/critical-security-patch

# Documentation branch
git checkout -b docs/sap-051-readme-update
```

**Valid Types**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `chore/` - Maintenance tasks
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Adding tests

**Tip**: Include SAP ID, COORD ID, or beads task ID in branch name for automatic traceability.

---

### 2. Writing Commit Messages

**Format**: `<type>(<scope>): <description>`

**Basic Examples**:
```bash
# Feature
git commit -m "feat(auth): add password reset functionality"

# Bug fix
git commit -m "fix(api): correct user validation logic"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Refactoring
git commit -m "refactor(hooks): simplify validation logic"

# Tests
git commit -m "test(auth): add unit tests for login"

# Chores
git commit -m "chore(deps): update dependencies to latest"
```

**Advanced Examples**:
```bash
# With multi-line description
git commit -m "feat(sap-051): implement git workflow patterns

Add commit-msg and pre-push hooks for validation.
Includes justfile recipes for automation.

Refs: SAP-051, COORD-2025-013"

# Breaking changes
git commit -m "feat(api)!: change response format to JSON

BREAKING CHANGE: API now returns JSON instead of XML"
```

**Valid Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Formatting (no code change)
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `chore` - Maintenance
- `perf` - Performance improvement
- `ci` - CI/CD changes
- `build` - Build system changes
- `revert` - Revert previous commit

**Scope** (optional but recommended):
- Component or area of change: `auth`, `api`, `ui`, `hooks`, `tests`
- SAP ID: `sap-051`
- Task ID: `.beads-9rtq`

---

### 3. Before Pushing

```bash
# Validate your commits and branch
just git-check

# Expected output:
# ✓ Git hooks configured correctly
# ✓ Branch name follows convention
# ✓ All commits follow Conventional Commits format
```

If validation fails, the output will tell you exactly what to fix.

---

## Troubleshooting

### "Commit rejected - doesn't follow Conventional Commits format"

**Problem**: Your commit message doesn't match the pattern.

**Solution**:
```bash
# Check the error message for hints
# Common mistakes:
# ❌ "Added new feature" → ✅ "feat: add new feature"
# ❌ "fix:update code" → ✅ "fix: update code" (space after colon!)
# ❌ "FEAT: new thing" → ✅ "feat: new thing" (lowercase type)
```

**Quick fix**:
```bash
# Amend your last commit with correct message
git commit --amend -m "feat(scope): correct message"
```

### "Branch name doesn't follow convention"

**Problem**: Branch name doesn't match `<type>/<identifier>-<description>`

**Solution**:
```bash
# Rename your branch
git branch -m feature/SAP-051-correct-name
```

### "Hook not running"

**Problem**: Hooks aren't being triggered.

**Solution**:
```bash
# Re-run git-setup
just git-setup

# Verify hooks path
git config --get core.hooksPath
# Should output: .githooks
```

### "Permission denied (on macOS/Linux)"

**Problem**: Hook scripts aren't executable.

**Solution**:
```bash
chmod +x .githooks/*
```

---

## Tips & Tricks

### 1. Generate Commit Message Templates

```bash
# Auto-extract SAP/COORD/beads IDs from branch name
just git-commit-template "sap-051" "feat"

# Output:
# feat(sap-051): <description>
#
# Refs: SAP-051
```

### 2. Validate Specific Commits

```bash
# Validate last 5 commits
just validate-commits HEAD~5

# Validate all commits in branch
just validate-commits main
```

### 3. Generate Changelog

```bash
# Generate changelog from last tag
just changelog v1.0.0 CHANGELOG.md
```

### 4. Check Configuration

```bash
# Show current git workflow configuration
just git-config-show
```

### 5. Bypass Hooks (Emergency Only!)

```bash
# Skip validation (use ONLY in emergencies)
git commit --no-verify -m "emergency: critical hotfix"

# You'll need to fix the commit message later:
git commit --amend -m "fix(critical): emergency hotfix for production issue"
```

---

## FAQ

**Q: Do I need to follow this for every commit?**
A: Yes! The hooks enforce it automatically, so invalid commits won't go through.

**Q: Can I use my own commit types?**
A: Yes, configure custom types with `just git-config-custom`. See Level 2 docs.

**Q: What if I forget the format?**
A: The hook will reject invalid commits and show examples. Use `just git-commit-template` for help.

**Q: Does this slow down my workflow?**
A: No! Validation takes <100ms. You'll save time from not having to manually write changelogs.

**Q: Can I disable the hooks?**
A: Yes, but not recommended:
```bash
git config hooks.commit-msg-enabled false
git config hooks.pre-push-enabled false
```

**Q: Where can I learn more?**
A: See full documentation:
- [Adoption Blueprint](skilled-awareness/git-workflow-patterns/adoption-blueprint.md) - Complete setup guide
- [Protocol Spec](skilled-awareness/git-workflow-patterns/protocol-spec.md) - Technical details
- [Awareness Guide](skilled-awareness/git-workflow-patterns/awareness-guide.md) - Deeper understanding

---

## Level 2 & 3 Features (Optional)

Once comfortable with basics, explore advanced features:

**Level 2** (Custom Configuration):
- Custom commit types
- SAP/COORD/beads ID integration
- Configurable validation rules
- One-command configuration

**Level 3** (Production Mastery):
- CI/CD validation
- Automated changelog generation
- A-MEM event correlation
- Team metrics

See [Adoption Blueprint](skilled-awareness/git-workflow-patterns/adoption-blueprint.md) for details.

---

## Getting Help

**In this repo**:
```bash
# Check git workflow status
just git-check

# Show configuration
just git-config-show

# Validate commits
just validate-commits HEAD~10
```

**Team Resources**:
- 📖 [Full Documentation](skilled-awareness/git-workflow-patterns/)
- 🐛 Report issues to team lead or create GitHub issue
- 💬 Ask in team chat for quick help

---

**Version**: 1.0.0 (2025-11-16)
**SAP**: SAP-051 (Git Workflow Patterns)
**Next**: See [Adoption Blueprint](skilled-awareness/git-workflow-patterns/adoption-blueprint.md) for advanced features
