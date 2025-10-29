# Migration Guide: chora-base v2.x to v3.0.0

**Target Audience:** Existing chora-base v2.x adopters
**Estimated Time:** 2-4 hours (depending on customization level)
**Difficulty:** Moderate (requires manual merge of customizations)

## Overview

chora-base v3.0.0 is a **major architectural change** from v2.x. This guide helps you migrate existing v2.x projects to v3.0.0.

**Key Changes:**
- ❌ No more Copier dependency
- ✅ Static template architecture (70% of files)
- ✅ Simple blueprint system (10 core files)
- ✅ All features enabled by default
- ✅ AI-agent-first design

## Should You Migrate?

### ✅ Migrate Now If:

- You're experiencing Copier issues (template generation failures, update conflicts)
- You work primarily with AI coding agents
- You want zero-dependency setup
- You're starting a new project based on existing v2.x project
- You want latest chora-base features and improvements

### ⏸️ Wait If:

- Your v2.x project is stable and working well
- You have extensive customizations that would be hard to merge
- You don't have time for 2-4 hour migration
- You're waiting for v3.1.0 blueprint simplifications

### 📌 Never Migrate If:

- Your project has diverged significantly from template
- Migration cost outweighs benefits
- You prefer Copier-based workflow

**Note:** v2.x continues to work - migration is optional, not required.

## Migration Strategies

### Strategy 1: Fresh Generation + Manual Merge (Recommended)

**Best For:** Most projects with moderate customization

**Process:**
1. Generate fresh v3.0.0 project
2. Copy your custom code/logic into new structure
3. Merge any template customizations
4. Test thoroughly
5. Commit

**Pros:**
- Clean v3.0.0 structure
- No template conflicts
- Latest best practices

**Cons:**
- Requires manual work
- Takes 2-4 hours

### Strategy 2: Incremental File Replacement

**Best For:** Projects with heavy customization

**Process:**
1. Keep existing v2.x structure
2. Selectively copy v3.0.0 improvements
3. Replace files one-by-one
4. Test after each change
5. Commit incrementally

**Pros:**
- Lower risk (smaller changes)
- Keep existing customizations
- Can pause/resume

**Cons:**
- Longer total time (4-6 hours)
- May miss template improvements
- Partial v3.0.0 adoption

### Strategy 3: Stay on v2.x

**Best For:** Stable projects, heavy customization

**Process:**
1. Continue using v2.x template
2. Manually port specific v3.0.0 features if needed
3. Migrate only when absolutely necessary

**Pros:**
- No work required
- Zero risk
- Existing setup continues working

**Cons:**
- Miss v3.0.0 improvements
- Copier issues persist
- No AI-agent-first features

## Migration Steps (Strategy 1: Fresh Generation)

### Phase 1: Preparation (15 minutes)

#### 1. Backup Your Project

```bash
cd /path/to/your-v2x-project

# Commit all changes
git add -A
git commit -m "chore: Backup before v3.0.0 migration"

# Create backup branch
git checkout -b pre-v3-migration
git checkout main  # or your default branch
```

#### 2. Document Your Customizations

Create a checklist of what you've customized:

```markdown
## My Customizations

### Code Changes
- [ ] Custom utility functions in src/{package}/utils/
- [ ] Modified MCP server logic in src/{package}/mcp/server.py
- [ ] Additional tests in tests/

### Configuration Changes
- [ ] Modified pyproject.toml dependencies
- [ ] Custom GitHub Actions workflows
- [ ] Custom justfile tasks
- [ ] Modified pre-commit hooks

### Documentation Changes
- [ ] Updated README.md
- [ ] Modified AGENTS.md
- [ ] Added custom docs in docs/

### Infrastructure Changes
- [ ] Custom Docker configuration
- [ ] Modified scripts in scripts/
- [ ] Custom environment variables in .env

### Removed Features
- [ ] Deleted memory system
- [ ] Removed Docker files
- [ ] Removed certain tests
```

#### 3. Extract Key Configuration

Note your current configuration from v2.x:

```bash
# Extract from .copier-answers.yml or files
grep "project_name" .copier-answers.yml
grep "author_name" .copier-answers.yml
# etc.
```

Save these values for v3.0.0 generation.

### Phase 2: Generate v3.0.0 Project (10 minutes)

#### 1. Clone/Update chora-base

```bash
cd /tmp  # or wherever you keep templates
git clone https://github.com/liminalcommons/chora-base.git
cd chora-base
git checkout v3.0.0
```

#### 2. Generate Fresh Project

**Option A: With AI Agent (Recommended)**

Ask your AI coding agent:

> "Generate a new chora-base v3.0.0 project with these details:
> - project_name: [your-project-name]
> - author_name: [Your Name]
> - author_email: [your@email.com]
> - github_username: [your-github-username]
>
> Use the AGENT_SETUP_GUIDE.md in /tmp/chora-base/"

**Option B: Manual with setup.py**

```bash
cd /tmp/chora-base
python setup.py your-project-name

# Follow prompts with your existing project details
```

**Result:** Fresh v3.0.0 project in `/tmp/your-project-name/`

### Phase 3: Merge Customizations (60-90 minutes)

#### 1. Copy Custom Code

```bash
# Your original project
SRC=/path/to/your-v2x-project

# Fresh v3.0.0 project
DEST=/tmp/your-project-name

# Copy your custom business logic (NOT template files)
cp -r $SRC/src/your_package/custom_module/ $DEST/src/your_package/
cp $SRC/src/your_package/server.py $DEST/src/your_package/mcp/server.py

# Merge carefully - don't overwrite template improvements!
```

#### 2. Merge Configuration Files

**pyproject.toml:**
```bash
# Compare
diff $SRC/pyproject.toml $DEST/pyproject.toml

# Manually merge:
# - Keep v3.0.0 structure
# - Add your custom dependencies
# - Preserve your version/description/URLs
```

**justfile:**
```bash
# Compare
diff $SRC/justfile $DEST/justfile

# Manually merge:
# - Keep v3.0.0 tasks
# - Add your custom tasks
# - Update task logic if you modified existing tasks
```

**GitHub Actions:**
```bash
# Compare
diff -r $SRC/.github/workflows/ $DEST/.github/workflows/

# Manually merge:
# - Keep v3.0.0 workflow structure
# - Add your custom workflows
# - Merge modifications to existing workflows
```

#### 3. Merge Documentation

**README.md:**
```bash
# Start with v3.0.0 README structure
# Add your project-specific:
# - Features/usage examples
# - API documentation
# - Screenshots/demos
# - Custom installation steps
```

**AGENTS.md:**
```bash
# Start with v3.0.0 AGENTS.md
# Add your project-specific:
# - Custom workflows
# - Project-specific context
# - Domain knowledge
# - Custom commands/tools
```

**Other docs:**
```bash
# Copy your custom docs
cp -r $SRC/docs/custom-guide.md $DEST/docs/
```

#### 4. Merge Tests

```bash
# Copy custom tests
cp $SRC/tests/test_custom_feature.py $DEST/tests/

# Update test structure if needed
# v3.0.0 may have new test patterns/fixtures
```

#### 5. Merge Scripts

```bash
# Compare
diff -r $SRC/scripts/ $DEST/scripts/

# Merge:
# - Keep v3.0.0 standard scripts
# - Add your custom scripts
# - Update modified scripts carefully
```

### Phase 4: Environment & Dependencies (15 minutes)

#### 1. Set Up Environment

```bash
cd /tmp/your-project-name

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"
```

#### 2. Copy Environment Config

```bash
# Copy your .env (if you have one)
cp /path/to/your-v2x-project/.env .env

# Update for any new v3.0.0 variables
```

#### 3. Install Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files  # Fix any issues
```

### Phase 5: Validation & Testing (30-60 minutes)

#### 1. Run Linting

```bash
just lint
# or
ruff check .
black --check .
mypy src/
```

Fix any issues that appear.

#### 2. Run Tests

```bash
just test
# or
pytest

# Check coverage
pytest --cov=src/your_package --cov-report=term-missing
```

Ensure ≥85% coverage (v3.0.0 standard).

#### 3. Test Your Application

**MCP Server:**
```bash
# Run server
python -m your_package.mcp.server

# Test with Claude Desktop or MCP Inspector
```

**CLI Tool:**
```bash
# Run CLI
your-package --help
your-package command --arg value
```

**Library:**
```bash
# Test imports
python -c "import your_package; print(your_package.__version__)"
```

#### 4. Smoke Test Scripts

```bash
# Run smoke tests
./scripts/smoke-test.sh

# Run integration tests
./scripts/integration-test.sh
```

#### 5. Validate Memory System (if using)

```bash
# Test memory CLI
your-package-memory query --type "test_event"
your-package-memory knowledge search --tag "test"
```

### Phase 6: Git Migration (15 minutes)

#### 1. Replace Your Project

**DANGER:** This replaces your entire project with v3.0.0 structure.

```bash
# Back up original (should already have backup branch)
cd /path/to/your-v2x-project
git checkout -b v2x-archive
git checkout main

# Remove old files (except .git/)
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# Copy v3.0.0 project
cp -r /tmp/your-project-name/* .
cp -r /tmp/your-project-name/.* . 2>/dev/null || true

# Review changes
git status
git diff
```

#### 2. Commit Migration

```bash
git add -A
git commit -m "feat: Migrate to chora-base v3.0.0

BREAKING CHANGE: Migrated from Copier-based v2.x to static template v3.0.0

- Removed Copier dependency
- Adopted static-template architecture (91 files)
- Using blueprint system (10 core templates)
- All features enabled by default
- Merged customizations from v2.x

See: docs/releases/v2-to-v3-migration.md
"
```

#### 3. Test Post-Migration

```bash
# Full test suite
just test

# Smoke tests
just smoke

# Try your application
# [test your specific functionality]
```

### Phase 7: Cleanup (10 minutes)

#### 1. Remove v2.x Artifacts

```bash
# Remove Copier files
rm -f .copier-answers.yml

# Remove old template references
grep -r "copier" . --exclude-dir=.git  # Should find nothing
```

#### 2. Update CI/CD

If you have custom CI beyond GitHub Actions:
- Update CI scripts for v3.0.0 structure
- Remove Copier from CI dependencies
- Test CI builds

#### 3. Update Documentation

- Update any README references to setup process
- Update CONTRIBUTING.md if it referenced Copier
- Add migration notes to CHANGELOG.md

### Phase 8: Verification (15 minutes)

#### Final Checklist

- [ ] All tests pass (`just test`)
- [ ] Linting passes (`just lint`)
- [ ] Coverage ≥85% (`pytest --cov`)
- [ ] Application runs correctly
- [ ] Git history is clean
- [ ] No Copier artifacts remain
- [ ] Documentation is updated
- [ ] CI/CD works (push and check)

#### Verify Key Features

**Memory System:**
- [ ] Events log correctly
- [ ] Knowledge notes create/search works
- [ ] Trace context propagates

**CLI Tools:**
- [ ] All commands work
- [ ] Help text is correct

**MCP Server:**
- [ ] Server starts without errors
- [ ] Tools are registered
- [ ] Resources are accessible

**Development Workflow:**
- [ ] `just` commands work
- [ ] Pre-commit hooks run
- [ ] Scripts execute correctly

## Migration Troubleshooting

### Issue: Import Errors After Migration

**Symptom:**
```python
ModuleNotFoundError: No module named 'your_package'
```

**Solution:**
```bash
# Reinstall in development mode
pip install -e ".[dev]"

# Verify installation
pip list | grep your-package
```

### Issue: Tests Failing After Migration

**Symptom:**
```
ImportError: cannot import name 'old_function'
```

**Solution:**
- Review test imports - v3.0.0 may have different module structure
- Update test fixtures - v3.0.0 has new conftest.py patterns
- Check for deprecated utilities

### Issue: GitHub Actions Failing

**Symptom:**
CI builds fail with "setup.py not found" or similar

**Solution:**
```yaml
# Update .github/workflows/ to use v3.0.0 patterns
# No more copier commands
# Use pip install -e . directly
```

### Issue: Memory System Not Working

**Symptom:**
```
FileNotFoundError: .chora/memory/events/
```

**Solution:**
```bash
# Create memory directories
mkdir -p .chora/memory/{events,knowledge,profiles}

# Or regenerate with memory enabled
```

### Issue: Pre-commit Hooks Failing

**Symptom:**
```
ruff...Failed
black...Failed
```

**Solution:**
```bash
# Reinstall hooks
pre-commit clean
pre-commit install

# Run and fix issues
pre-commit run --all-files

# Fix reported issues, then commit
```

### Issue: Lost Customizations

**Symptom:**
Features/code you had in v2.x are missing

**Solution:**
```bash
# Check backup branch
git checkout pre-v3-migration
git diff main...pre-v3-migration > changes.patch

# Review patch
less changes.patch

# Manually re-apply lost customizations
```

## Rollback Procedure

If migration fails or causes issues:

### Quick Rollback

```bash
cd /path/to/your-project

# Revert to backup branch
git checkout pre-v3-migration

# Create new main from backup
git branch -D main
git checkout -b main

# Force push (if you pushed bad migration)
git push -f origin main
```

### Selective Rollback

```bash
# Keep some v3.0.0 files, restore others
git checkout pre-v3-migration -- src/your_package/custom_module.py
git checkout pre-v3-migration -- tests/test_custom.py

git commit -m "fix: Restore custom code from v2.x"
```

## Post-Migration Best Practices

### 1. Document Your Migration

Add to your CHANGELOG.md:

```markdown
## [X.0.0] - 2025-10-25

### Changed
- **BREAKING:** Migrated to chora-base v3.0.0 architecture
- Removed Copier dependency
- Adopted static template + blueprint structure
- All features now enabled by default

### Migration Notes
- See docs/releases/v2-to-v3-migration.md for details
- Backup branch: pre-v3-migration
- Migration date: 2025-10-25
- Migration time: ~3 hours
```

### 2. Update Your README

Add migration notice:

```markdown
## Recent Updates

### vX.0.0 - Migrated to chora-base v3.0.0

This project has been migrated from chora-base v2.x to v3.0.0:
- No more Copier dependency
- Static template architecture
- All features enabled by default

See [CHANGELOG.md](CHANGELOG.md) for details.
```

### 3. Share Learnings

If you encountered issues:
- Open GitHub issue on chora-base
- Share migration tips in Discussions
- Help improve this migration guide

### 4. Plan for v3.1.0+

v3.1.0 will simplify blueprints further:
- Pure `{{ variable }}` replacement
- No Jinja2 conditionals
- Easier future migrations

Consider waiting for v3.1.0 if you:
- Struggled with blueprint complexity
- Have ongoing v2.x features to integrate
- Want easier future updates

## FAQ

### Q: Can I stay on v2.x forever?

**A:** Yes, v2.x continues to work. Migration is optional. However:
- New features will be v3.0.0+ only
- Bug fixes may prioritize v3.0.0
- Community may shift to v3.0.0

### Q: Will my existing v2.x project break?

**A:** No, it continues working. Only new generation/updates use v3.0.0.

### Q: Can I use Copier with v3.0.0?

**A:** No, v3.0.0 removed Copier support. Use setup.py or AI agents instead.

### Q: How often will v3.x change?

**A:** chora-base follows semantic versioning:
- v3.0.x: Patches (bug fixes, minor improvements)
- v3.x.0: Minor (new features, backward compatible)
- v4.0.0: Major (breaking changes)

### Q: What if I have a lot of customizations?

**A:** Consider Strategy 3 (stay on v2.x) or Strategy 2 (incremental). Full migration may not be worth it for heavily customized projects.

### Q: Can AI agents help with migration?

**A:** Yes! Ask your agent:

> "Migrate my chora-base v2.x project to v3.0.0 following docs/releases/v2-to-v3-migration.md"

They can handle much of the manual merge work.

### Q: What if I need features from both v2.x and v3.0.0?

**A:** Generate fresh v3.0.0, then cherry-pick v2.x features you need. v3.0.0 includes all v2.x features plus new ones.

## Resources

**Migration Planning:**
- [Release Notes](v3.0.0-release-notes.md) - What changed in v3.0.0
- [AGENT_SETUP_GUIDE.md](../../AGENT_SETUP_GUIDE.md) - Setup guide for v3.0.0

**v3.0.0 Documentation:**
- [README.md](../../README.md) - Updated for v3.0.0
- [CHANGELOG.md](../../CHANGELOG.md) - Version history

**Setup Tools:**
- [setup.py](../../setup.py) - CLI helper for manual setup
- [static-template/](../../static-template/) - 91 ready-to-use files
- [blueprints/](../../blueprints/) - 10 core templates

**Support:**
- [GitHub Issues](https://github.com/liminalcommons/chora-base/issues) - Report migration issues
- [GitHub Discussions](https://github.com/liminalcommons/chora-base/discussions) - Ask questions

---

**Need Help?**
- Open an issue: [chora-base/issues](https://github.com/liminalcommons/chora-base/issues)
- Ask in discussions: [chora-base/discussions](https://github.com/liminalcommons/chora-base/discussions)
- Check examples: [examples/](../../examples/)
