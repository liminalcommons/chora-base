# Awareness Guide: Git Workflow Patterns

**SAP ID**: SAP-051
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants (Claude, GPT, Codex)
**Last Updated**: 2025-11-16

---

## 📖 Quick Reference

**New to SAP-051?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - Install git hooks in 5 minutes with `just git-setup`
- 📚 **Time Savings** - 50-250% ROI (30-90 min/week saved on conflict resolution + PR reviews)
- 🎯 **Branch Naming** - Standardized prefixes (feature/bugfix/hotfix/chore/docs)
- 🔧 **Conventional Commits** - Automated commit message validation (100% compliance)
- 📊 **Merge Strategies** - Clear decision tree (squash vs merge vs rebase)
- 🔗 **Integration** - Works with SAP-001 (Inbox), SAP-010 (Memory), SAP-015 (Beads), SAP-012 (Lifecycle)

This awareness-guide.md provides: Agent-specific workflows, decision trees, and patterns for AI coding assistants using SAP-051 git workflow automation.

---

## Quick Start for AI Agents

### One-Sentence Summary

**SAP-051 defines standardized git workflows (branch naming, conventional commits, merge strategies, git hooks) enabling 30-50% conflict reduction and automated changelog generation for multi-developer collaboration.**

### When to Use This SAP

Use SAP-051 when:
- ✅ User asks to create a new feature branch (enforce branch naming convention)
- ✅ User commits code (validate commit message format)
- ✅ User asks "how should I name this branch?" (provide naming guidance)
- ✅ User wants to generate a changelog (use conventional commits)
- ✅ User asks "should I squash or merge?" (apply merge strategy decision tree)
- ✅ Multi-developer workflow questions (coordinate with SAP-052, SAP-053, SAP-054)
- ✅ Setting up new repository (install git hooks via `just git-setup`)

Don't use SAP-051 for:
- ❌ Single-file commits without git (not a git workflow)
- ❌ Server-side git operations (SAP-051 is client-side only)
- ❌ Complex git history rewriting (SAP-051 is for forward workflows, not git surgery)
- ❌ Non-git version control systems (Mercurial, SVN, etc.)

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1**: Branch Naming Convention
- **Description**: All branches must follow `<type>/<identifier>-<description>` format
- **When to use**: Whenever user creates a branch or you suggest a branch name
- **Example**: `feature/SAP-051-git-workflow-patterns`, `bugfix/.beads-abc-fix-hook`
- **Agent action**: Always validate branch names, suggest corrections if invalid

**Concept 2**: Conventional Commits v1.0.0
- **Description**: Commit messages must follow `<type>(<scope>): <description>` format
- **When to use**: Whenever user commits or you generate commit messages
- **Example**: `feat(sap-051): add git hooks`, `fix(justfile): correct recipe syntax`
- **Agent action**: Generate commit messages in conventional format, explain violations

**Concept 3**: Merge Strategy Decision Tree
- **Description**: Use squash merge for features, merge commit for long-lived branches, rebase for updates
- **When to use**: When user asks "how should I merge this?"
- **Example**: Feature branch → main = squash merge (clean history)
- **Agent action**: Apply decision tree logic, explain rationale

**Concept 4**: Git Hooks Enforcement
- **Description**: Client-side hooks validate commit messages and branch names automatically
- **When to use**: When user encounters commit/push errors from hooks
- **Example**: commit-msg hook rejects "added feature" → explain conventional commits
- **Agent action**: Interpret hook errors, guide user to fix

### Decision Tree

```
User request about git workflow
   │
   ├─ Creating new branch?
   │   ├─ Feature work? → feature/<identifier>-<description>
   │   ├─ Bug fix? → bugfix/<identifier>-<description>
   │   ├─ Urgent fix? → hotfix/<identifier>-<description>
   │   ├─ Maintenance? → chore/<description>
   │   └─ Docs only? → docs/<description>
   │
   ├─ Committing code?
   │   ├─ New feature? → feat(<scope>): <description>
   │   ├─ Bug fix? → fix(<scope>): <description>
   │   ├─ Documentation? → docs(<scope>): <description>
   │   ├─ Refactoring? → refactor(<scope>): <description>
   │   └─ Tests? → test(<scope>): <description>
   │
   ├─ Merging branches?
   │   ├─ Feature → main? → Squash merge (clean history)
   │   ├─ Release → main? → Merge commit (preserve history)
   │   └─ Updating feature with main? → Rebase (avoid merge commits)
   │
   ├─ Hook validation failed?
   │   ├─ commit-msg error? → Fix commit message format
   │   ├─ pre-push error? → Fix branch name or resolve conflicts
   │   └─ Git hooks not installed? → Run `just git-setup`
   │
   └─ Generate changelog?
       └─ Run `just changelog --since=<ref>`
```

---

## 2. Common Agent Workflows

### Workflow 1: User Starts New Feature

**User Request**: "Help me create a new feature for SAP-051 git hooks"

**Agent Actions**:
1. **Suggest branch name** following convention:
   ```bash
   git checkout -b feature/SAP-051-git-hooks
   ```
2. **Explain naming convention**: "I'm using 'feature/' prefix because this is new functionality, 'SAP-051' identifies the SAP, and 'git-hooks' describes the work."
3. **Remind about commit format**: "When you commit, use Conventional Commits format like: `feat(sap-051): add commit-msg validation hook`"

**Validation**:
```bash
# Check branch name is valid
git branch --show-current
# Expected: feature/SAP-051-git-hooks
```

**Expected Output**:
```
Switched to a new branch 'feature/SAP-051-git-hooks'
```

**Common Variations**:
- **Bug fix**: Use `bugfix/<identifier>-<description>` instead
- **Urgent production fix**: Use `hotfix/<identifier>-<description>`
- **Documentation only**: Use `docs/<description>`

---

### Workflow 2: User Commits Code

**User Request**: "Commit this code that adds git hook validation"

**Agent Actions**:
1. **Stage files** (if not already staged):
   ```bash
   git add <files>
   ```
2. **Generate conventional commit message**:
   ```bash
   git commit -m "feat(sap-051): add commit-msg validation hook

   Validates commit messages against Conventional Commits v1.0.0
   schema. Rejects commits that don't follow format.

   Refs: SAP-051, COORD-2025-013"
   ```
3. **Explain commit message structure**: "Using 'feat' type (new feature), 'sap-051' scope, and descriptive subject. Body explains why, footer references related work."

**Validation**:
```bash
# Check commit was created with correct message
git log -1 --pretty=format:"%s"
# Expected: feat(sap-051): add commit-msg validation hook
```

**Expected Output**:
```
[feature/SAP-051-git-hooks a1b2c3d] feat(sap-051): add commit-msg validation hook
 1 file changed, 45 insertions(+)
```

**Common Variations**:
- **Fix commit**: Use `fix(<scope>): <description>`
- **Breaking change**: Add `!` after type: `feat(sap-051)!: change hook interface`
- **Multiple scopes**: Use most specific scope or omit: `feat: add git workflow patterns`

---

### Workflow 3: User Encounters Commit Hook Error

**User Request**: "Git won't let me commit, says my message is invalid"

**Agent Actions**:
1. **Read error message** from commit-msg hook:
   ```
   ❌ Commit message doesn't follow Conventional Commits format
   Expected: <type>(<scope>): <description>
   ```
2. **Identify the issue**: "Your commit message doesn't start with a valid type (feat, fix, docs, etc.)"
3. **Provide fix**:
   ```bash
   # Amend the commit message with correct format
   git commit --amend -m "feat(sap-051): add git workflow patterns"
   ```
4. **Explain format**: "Conventional Commits require: type (feat/fix/docs/etc.) + optional scope in parens + colon + space + description"

**Validation**:
```bash
# Retry commit (should succeed now)
git commit --amend
# Hook should exit 0 (success)
```

**Expected Output**:
```
✓ commit-msg validation passed
[feature/SAP-051 b2c3d4e] feat(sap-051): add git workflow patterns
```

---

### Workflow 4: User Asks About Merge Strategy

**User Request**: "Should I squash or merge my feature branch into main?"

**Agent Actions**:
1. **Apply decision tree**: "Since you're merging a feature branch into main, you should **squash merge**."
2. **Explain rationale**: "Squash merge collapses all your commits into a single commit on main, creating clean linear history. Each feature = one commit."
3. **Provide command** (if merging locally):
   ```bash
   git checkout main
   git merge --squash feature/SAP-051-git-hooks
   git commit -m "feat(sap-051): add git workflow patterns"
   ```
4. **Alternative (GitHub PR)**: "If using GitHub, select 'Squash and merge' when merging the PR."

**Validation**:
```bash
# Check main history is linear
git log --oneline main
# Should show single commit for entire feature
```

---

### Workflow 5: Install Git Hooks in New Repo

**User Request**: "Set up this repository with git workflow standards"

**Agent Actions**:
1. **Check if SAP-051 is installed**:
   ```bash
   git config --get core.hooksPath
   # If empty, hooks not installed
   ```
2. **Install git hooks**:
   ```bash
   just git-setup
   ```
3. **Validate installation**:
   ```bash
   just git-check
   ```
4. **Explain what was installed**: "Installed commit-msg and pre-push hooks from `.githooks/`. These will validate commit messages and branch names automatically."

**Validation**:
```bash
# Verify hooks are active
git config --get core.hooksPath
# Expected: .githooks
```

**Expected Output**:
```
✓ Git hooks installed successfully
✓ commit-msg hook active
✓ pre-push hook active
```

---

### Workflow 6: Generate Changelog

**User Request**: "Create a changelog from recent commits"

**Agent Actions**:
1. **Run changelog generator**:
   ```bash
   just changelog --since=v1.0.0 --output=CHANGELOG.md
   ```
2. **Preview changelog**:
   ```bash
   cat CHANGELOG.md
   ```
3. **Explain changelog structure**: "Changelog is auto-generated from conventional commits, grouped by type (Features, Bug Fixes, Docs, etc.)"

**Validation**:
```bash
# Check changelog was created
ls -lh CHANGELOG.md
```

**Expected Output**:
```markdown
# Changelog

## [1.1.0] - 2025-11-16

### Features
- **sap-051**: add git workflow patterns (a1b2c3d)

### Bug Fixes
- **git-hooks**: correct validation regex (b2c3d4e)
```

---

## 3. Quick Reference for Agents

### Key Commands

```bash
# Install git hooks (one-time setup)
just git-setup

# Validate all commits in current branch
just validate-commits

# Quick validation (hooks + commits + branch name)
just git-check

# Generate changelog from commits
just changelog --since=<ref>

# Check git hook installation
git config --get core.hooksPath

# Test commit message manually (agent testing)
echo "feat(sap-051): test message" > /tmp/test-commit
.githooks/commit-msg /tmp/test-commit
echo $?  # Should be 0 (success)
```

### Important File Paths

| File | Purpose | Agent Action |
|------|---------|--------------|
| `.githooks/commit-msg` | Validates commit messages | Read to understand validation rules |
| `.githooks/pre-push` | Validates branch names | Read to understand branch naming |
| `.git/config` | Git hook configuration | Check `core.hooksPath` is set |
| `CHANGELOG.md` | Generated changelog | Read to preview changelog output |
| `justfile` | Automation recipes | Reference for available commands |

### Configuration Snippets

**Git Config** (`.git/config`):
```ini
[core]
    hooksPath = .githooks

[hooks]
    commit-msg-enabled = true
    pre-push-enabled = true

[conventional-commits]
    types = feat,fix,docs,style,refactor,test,chore
    max-subject-length = 72
```

### Common Patterns

**Pattern 1**: Create feature branch with conventional commit
```bash
# Create branch
git checkout -b feature/SAP-051-new-feature

# Commit with conventional format
git commit -m "feat(sap-051): add new feature

Detailed explanation of why this feature exists and
what problem it solves.

Refs: SAP-051"
```

**Pattern 2**: Fix invalid commit message
```bash
# If commit-msg hook rejects commit, amend it
git commit --amend -m "feat(scope): correct message format"
```

**Pattern 3**: Update feature branch with main (rebase)
```bash
# Fetch latest main
git fetch origin main

# Rebase feature branch on main
git rebase origin/main
```

---

## 4. Integration with Other SAPs

### Complementary SAPs

**SAP-001 (Inbox Coordination Protocol)**
- **Use together when**: Creating coordination requests or tracking cross-repo work
- **Benefit**: Commit messages reference COORD IDs for traceability
- **Agent workflow**:
  1. When user works on coordination request, suggest commit scope: `feat(coord-2025-013): ...`
  2. Add `Refs: COORD-2025-013` in commit footer
  3. A-MEM events can correlate commits with coordination workflow

**SAP-010 (Memory System)**
- **Use together when**: Logging work to A-MEM or correlating commits with events
- **Benefit**: Commit SHAs logged in A-MEM events for full traceability
- **Agent workflow**:
  1. When emitting A-MEM event, include git commit SHA: `"git_commit": "a1b2c3d4"`
  2. When querying memory, agents can `git show <commit-sha>` for full context
  3. Conventional commits enable better event correlation (commit type → event type)

**SAP-015 (Beads Task Tracking)**
- **Use together when**: Working on beads tasks
- **Benefit**: Branch names and commits reference beads task IDs
- **Agent workflow**:
  1. When user starts beads task, suggest branch: `feature/.beads-<task-id>-<description>`
  2. Commit messages reference beads task: `feat(.beads-9rtq): implement feature`
  3. `git log --grep=".beads-9rtq"` finds all commits for task

**SAP-012 (Development Lifecycle)**
- **Use together when**: Following DDD → BDD → TDD workflow
- **Benefit**: Commit types align with lifecycle phases
- **Agent workflow**:
  1. DDD (Design): `docs(sap-051): add protocol specification`
  2. BDD (Behavior): `feat(sap-051): implement feature`
  3. TDD (Testing): `test(sap-051): add validation tests`
  4. Agents can track lifecycle phase via commit types

**SAP-052 (Ownership Zones)** - Future integration
- **Use together when**: Multi-developer collaboration with code ownership
- **Benefit**: Git hooks can enforce CODEOWNERS rules, auto-assign reviewers based on branch
- **Agent workflow**: When creating PR, git hooks read CODEOWNERS and suggest reviewers

**SAP-053 (Conflict Resolution)** - Future integration
- **Use together when**: Resolving merge conflicts
- **Benefit**: Pre-merge hooks detect conflicts, A-MEM logs conflict patterns
- **Agent workflow**: pre-push hook warns of conflicts before push, agents guide resolution

---

## 5. Error Patterns & Troubleshooting

### Error Pattern 1: "Commit message doesn't follow Conventional Commits format"

**Symptoms**:
- User runs `git commit`, commit is rejected
- Error message: `❌ Commit message doesn't follow Conventional Commits format`

**Cause**: Commit message doesn't start with valid type (`feat`, `fix`, `docs`, etc.)

**Agent Solution**:
1. **Diagnose**: Read error message, identify missing/invalid type
2. **Fix**: Amend commit with correct format:
   ```bash
   git commit --amend -m "feat(scope): correct message"
   ```
3. **Verify**: Retry commit, should succeed
4. **Prevent**: Explain conventional commits format to user, provide examples

**Prevention**: When generating commit messages for user, always use conventional format.

---

### Error Pattern 2: "Branch name doesn't follow convention"

**Symptoms**:
- User runs `git push`, push is rejected
- Error message: `❌ Branch name doesn't follow convention`

**Cause**: Branch name doesn't start with valid type (`feature/`, `bugfix/`, `hotfix/`, `chore/`, `docs/`)

**Agent Solution**:
1. **Diagnose**: Check current branch name: `git branch --show-current`
2. **Fix**: Rename branch:
   ```bash
   git branch -m feature/<identifier>-<description>
   ```
3. **Verify**: Run `just git-check` to validate new name
4. **Prevent**: Always suggest branch names that follow convention

**Prevention**: When user asks to create branch, provide name in correct format.

---

### Error Pattern 3: "Git hooks not installed"

**Symptoms**:
- User commits with invalid message, no hook error appears
- `git config --get core.hooksPath` returns empty

**Cause**: Git hooks not installed via `just git-setup`

**Agent Solution**:
1. **Diagnose**: Check hook installation:
   ```bash
   git config --get core.hooksPath
   # If empty, hooks not installed
   ```
2. **Fix**: Install hooks:
   ```bash
   just git-setup
   ```
3. **Verify**: Run `just git-check`
4. **Explain**: "Git hooks are now active. They'll validate commit messages and branch names automatically."

**Prevention**: When setting up new repo, always run `just git-setup` first.

---

### Error Pattern 4: "Pre-push validation failed: conflicts with main"

**Symptoms**:
- User runs `git push`, push is rejected
- Error message: `❌ Pre-push validation failed: conflicts with main`

**Cause**: Current branch has merge conflicts with main branch

**Agent Solution**:
1. **Diagnose**: Check for conflicts:
   ```bash
   git fetch origin main
   git diff origin/main...HEAD
   ```
2. **Fix**: Rebase on main to resolve conflicts:
   ```bash
   git rebase origin/main
   # Resolve conflicts if any
   git rebase --continue
   ```
3. **Verify**: Run `just git-check`, should pass
4. **Push**: Retry `git push`

**Prevention**: Regularly rebase feature branches on main to avoid conflicts accumulating.

---

## 6. Agent Communication Patterns

### Explaining Git Workflow Patterns to Users

**Simple Explanation** (for beginners):
> "SAP-051 provides git workflow standards - it validates your commit messages and branch names automatically, ensuring consistency across the team. Think of it like spell-check for git."

**Technical Explanation** (for experienced users):
> "SAP-051 implements Conventional Commits v1.0.0 with client-side git hooks, enforcing branch naming conventions (feature/bugfix/hotfix prefixes) and commit message schemas (<type>(<scope>): <description>). Enables automated changelog generation and 30-50% conflict reduction."

### Common User Questions

**Q: Why do I need to use this format for commit messages?**

**Agent Response**:
"Conventional Commits enable automated changelog generation and make git history more readable. The format (<type>(<scope>): <description>) helps other developers (and AI agents like me) understand what changed and why. It's a small upfront cost (10 seconds per commit) for big long-term benefits (automated changelogs, better debugging, faster PR reviews)."

**Q: Can I skip the git hooks if I don't want to use Conventional Commits?**

**Agent Response**:
"You can disable git hooks with `git config hooks.commit-msg-enabled false`, but I recommend keeping them active. The hooks prevent mistakes before they reach the remote, saving time later. If conventional commits feel cumbersome, let me know - I can help generate commit messages for you automatically."

**Q: What if I'm working on a quick fix and don't have an issue ID?**

**Agent Response**:
"For quick fixes without issue IDs, you can use a descriptive slug as the identifier. For example: `hotfix/fix-typo-in-readme`. If you're using beads for task tracking, you can create a quick task (`bd create 'Fix typo'`) and use that ID."

**Q: Should I use squash merge or regular merge?**

**Agent Response**:
"Use **squash merge** for feature branches merging into main - this keeps main's history clean (one commit per feature). Use **merge commit** for long-lived branches like releases where you want to preserve the full history. Use **rebase** when updating your feature branch with latest main (avoids merge commits on feature branches)."

---

## 7. Best Practices for Agents

### Do's ✅

- ✅ **Always generate commit messages in conventional format** - Don't ask user what format, just use it
- ✅ **Validate branch names before suggesting** - Use regex: `^(feature|bugfix|hotfix|chore|docs|refactor|test)\/[a-zA-Z0-9\.\-\_]+$`
- ✅ **Explain hook errors clearly** - Don't just show error, explain why and how to fix
- ✅ **Suggest branch names proactively** - When user starts new work, suggest correct name
- ✅ **Reference related work in commit footers** - Add `Refs: SAP-051, COORD-2025-013` for traceability
- ✅ **Use commit types consistently** - feat = new feature, fix = bug fix, docs = documentation only
- ✅ **Keep commit subjects ≤72 characters** - Prevents truncation in git log output
- ✅ **Write commit bodies in present tense** - "Add feature" not "Added feature" or "Adds feature"

### Don'ts ❌

- ❌ **Don't generate non-conventional commit messages** - Always use conventional format
- ❌ **Don't suggest branch names without type prefix** - "my-feature" → "feature/my-feature"
- ❌ **Don't use git commit -m with multi-line messages** - Use heredoc or separate body/footer
- ❌ **Don't force push to main branch** - Violates server-side protection rules
- ❌ **Don't rebase shared branches** - Only rebase local branches
- ❌ **Don't skip git hooks** - They prevent mistakes, let them run
- ❌ **Don't use non-standard commit types** - Stick to: feat, fix, docs, style, refactor, test, chore, perf, ci, build
- ❌ **Don't include secrets in commit messages** - No passwords, API keys, tokens

### Efficiency Tips

**Tip 1**: Batch commit message generation
- **Why**: Reduces back-and-forth with user
- **How**: When user says "commit this", analyze changes and generate commit message immediately

**Tip 2**: Use `just git-check` before push
- **Why**: Catches errors locally before remote push fails
- **How**: Always run `just git-check` before suggesting `git push`

**Tip 3**: Suggest branch rename immediately
- **Why**: Easier to rename before commits exist
- **How**: If user creates branch with invalid name, suggest rename before first commit

---

## 8. Validation & Quality Checks

### Agent Self-Check Checklist

Before completing a git workflow task with SAP-051, agents should verify:

- [ ] Branch name follows convention (`<type>/<identifier>-<description>`)
- [ ] Commit message follows Conventional Commits format
- [ ] Commit subject ≤72 characters
- [ ] Git hooks are installed (`git config --get core.hooksPath` → `.githooks`)
- [ ] Validation commands executed successfully (`just git-check` passed)
- [ ] User understands why conventional format is used (explained if asked)

### Validation Commands

```bash
# Primary validation (hooks + commits + branch name)
just git-check

# Validate commit messages only
just validate-commits

# Check git hook installation
git config --get core.hooksPath

# Test commit message format manually
echo "feat(sap-051): test message" > /tmp/test-commit
.githooks/commit-msg /tmp/test-commit && echo "✓ Valid" || echo "✗ Invalid"
```

---

## 9. Version Compatibility

**Current Version**: 1.0.0

### Compatibility Notes

- **SAP-051 1.0.0** is compatible with:
  - Git 2.25.0+
  - Bash 4.0+
  - Python 3.11+
  - Just 1.0.0+

### Breaking Changes

**No breaking changes** (initial release)

**Future compatibility**:
- If Conventional Commits releases v2.0.0, SAP-051 will create migration path (major version bump)
- Git hook interface is stable (unlikely to change in minor versions)

---

## 10. Additional Resources

### Within chora-base

- [Protocol Specification](./protocol-spec.md) - Technical contracts, schemas, validation rules
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation instructions
- [Capability Charter](./capability-charter.md) - Problem statement, scope, success criteria

### External Resources

- [Conventional Commits v1.0.0 Specification](https://www.conventionalcommits.org/en/v1.0.0/) - Official spec for commit message format
- [Git Hooks Documentation](https://git-scm.com/docs/githooks) - Git's official hook interface documentation
- [Semantic Versioning 2.0.0](https://semver.org/) - Version numbering scheme (relates to commit types)
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches) - Server-side enforcement

---

**For Agents**: This awareness guide is your quick reference for SAP-051 workflows. For detailed technical specifications, see [protocol-spec.md](./protocol-spec.md). For installation instructions, see [adoption-blueprint.md](./adoption-blueprint.md).

**Version**: 1.0.0 (2025-11-16)
