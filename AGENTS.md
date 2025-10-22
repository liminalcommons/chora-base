# AGENTS.md - chora-base Template Repository

**Purpose**: Machine-readable instructions for AI agents working on the chora-base template repository.

**Last Updated**: 2025-10-22 (v1.9.3)

---

## Project Overview

**chora-base** is a Copier-based Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates.

**Repository Type**: Template repository (generates other projects)
**Primary Users**: Human developers and AI agents generating/maintaining Python projects
**Key Technology**: [Copier](https://copier.readthedocs.io/) (Jinja2-based project generator)

### Key Concepts

- **Template vs Generated Project**: chora-base is the template; generated projects are adopters
- **Jinja2 Templating**: Files ending in `.jinja` become templated files in generated projects
- **Conditional Features**: Features controlled via `copier.yml` questions (e.g., `include_docker`, `include_memory_system`)
- **Upgrade Path**: Generated projects update via `copier update` (smart merge, not overwrite)

---

## Repository Structure

```
chora-base/
├── template/                    # Template files (copied to generated projects)
│   ├── src/                     # Python source templates
│   ├── tests/                   # Test templates
│   ├── scripts/                 # Automation script templates
│   ├── .github/workflows/       # CI/CD workflow templates
│   ├── AGENTS.md.jinja          # Main template for generated AGENTS.md (2,540 lines)
│   ├── README.md.jinja          # README template
│   ├── pyproject.toml.jinja     # Python project config template
│   └── ...                      # Other project files
├── docs/                        # Template documentation
│   ├── upgrades/                # Version upgrade guides
│   │   ├── README.md            # Upgrade guide index
│   │   ├── PHILOSOPHY.md        # Upgrade philosophy
│   │   ├── UPGRADE_GUIDE_TEMPLATE.md  # Template for writing upgrade guides
│   │   ├── v1.9.2-to-v1.9.3.md  # Version-specific guides (naming: vX.Y-to-vX.Z.md)
│   │   └── ...
│   ├── how-to/                  # Task-oriented guides
│   │   ├── 01-generate-new-mcp-server.md
│   │   ├── 02-rip-and-replace-existing-server.md
│   │   └── ...
│   ├── reference/               # Reference documentation
│   │   ├── template-configuration.md
│   │   └── ...
│   ├── explanation/             # Conceptual explanations
│   ├── research/                # Research documents
│   │   └── Agentic Coding Best Practices Research.pdf
│   ├── BENEFITS.md              # ROI analysis
│   └── DOCUMENTATION_PLAN.md    # Documentation strategy
├── examples/                    # Example generated projects
│   ├── full-featured-with-vision/
│   ├── full-featured-with-docs/
│   └── ...
├── copier.yml                   # Template configuration (questions, conditionals)
├── CHANGELOG.md                 # Version history
├── README.md                    # Project overview
└── AGENTS.md                    # This file

**IMPORTANT**: This is the FIRST TIME chora-base has its own AGENTS.md. Previously, lack of guidance caused agents to misplace files (e.g., upgrade docs in repo root instead of docs/upgrades/).
```

---

## File Organization Conventions

### Upgrade Documentation

**Location**: `docs/upgrades/`
**Naming Pattern**: `vX.Y-to-vX.Z.md` (e.g., `v1.9.2-to-v1.9.3.md`)
**Not**: UPPERCASE naming, repo root placement

**Why This Matters**: Previous upgrade docs (v1.9.0-to-v1.9.1, v1.9.1-to-v1.9.2) were misplaced in repo root because chora-base lacked this AGENTS.md to guide agents.

**Template**: Use `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md` for structure

### Research Documents

**Location**: `docs/research/`
**Format**: PDF, markdown, or other documentation formats
**Purpose**: Background research informing template features

### How-To Guides

**Location**: `docs/how-to/`
**Naming Pattern**: `NN-kebab-case-title.md` (e.g., `01-generate-new-mcp-server.md`)
**Audience**: Humans + AI agents (task-oriented)

### Reference Documentation

**Location**: `docs/reference/`
**Naming Pattern**: `kebab-case-title.md` (e.g., `template-configuration.md`)
**Audience**: Humans + AI agents (information-oriented)

### Example Projects

**Location**: `examples/`
**Structure**: Full generated project directories
**Purpose**: Test template features, demonstrate usage patterns
**Status**: Examples may lag behind template (document drift in commit messages)

---

## Development Workflows

### Adding New Features to Template

1. **Research Phase**
   - Document research findings in `docs/research/`
   - Identify industry best practices
   - Review adopter feedback from real projects (mcp-n8n, chora-compose)

2. **Design Phase**
   - Update `CHANGELOG.md` under `## [Unreleased]`
   - Consider opt-in vs opt-out (new features usually opt-in)
   - Add question to `copier.yml` if user-facing
   - Update `docs/reference/template-configuration.md` if adding configuration

3. **Implementation Phase**
   - Create `.jinja` files in `template/`
   - Add conditional logic in `copier.yml` `_exclude` section if optional
   - Test with `copier copy . /tmp/test-project` (local testing)
   - Generate example in `examples/` if demonstrating complex feature

4. **Documentation Phase**
   - Update `README.md` if user-facing feature
   - Add to `template/AGENTS.md.jinja` if relevant to AI agents
   - Document in appropriate `docs/` subdirectory
   - Update `docs/BENEFITS.md` if adding measurable value

5. **Validation Phase**
   - Generate fresh project: `copier copy . /tmp/test-validation`
   - Run generated project's tests: `cd /tmp/test-validation && ./scripts/setup.sh && pytest`
   - Test upgrade path: Use existing example, run `copier update`
   - Verify conditional combinations (Docker on/off, memory on/off, etc.)

### Releasing New Version

**Version Numbering**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR** (X.0.0): Breaking changes requiring adopter action
- **MINOR** (1.X.0): New features, additive changes (current: v1.9.3)
- **PATCH** (1.1.X): Bug fixes only

**Release Process**:

1. **Pre-Release Validation**
   ```bash
   # Test template generation
   copier copy . /tmp/test-release
   cd /tmp/test-release && ./scripts/setup.sh && pytest

   # Test update path (use example project)
   cd examples/full-featured-with-vision
   copier update
   ```

2. **Create Upgrade Guide**
   - Location: `docs/upgrades/vX.Y-to-vX.Z.md`
   - Use template: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`
   - Include decision tree for AI agents
   - Document displacement risk (ZERO/LOW/MEDIUM/HIGH)
   - Add migration steps, validation checklist

3. **Update Core Files**
   ```bash
   # Update CHANGELOG.md
   # Change: ## [Unreleased]
   # To:     ## [X.Y.Z] - 2025-MM-DD

   # Update README.md Recent Updates section
   # Add new version entry with key features

   # Update docs/upgrades/README.md
   # Add version to version-specific guides table
   ```

4. **Commit and Tag**
   ```bash
   git add -A
   git commit -m "feat(scope): Brief description (vX.Y.Z)

   Detailed changes:
   - Feature 1
   - Feature 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"

   git tag vX.Y.Z
   git push origin main --tags
   ```

5. **Create GitHub Release**
   ```bash
   gh release create vX.Y.Z \
     --title "vX.Y.Z - Brief Title" \
     --notes "Release notes here (benefits, changes, upgrade guide link)"
   ```

6. **Update docs/upgrades/README.md**
   - Update version table with new entry
   - Update "Status" line if completing a phase

### Creating Upgrade Documentation

**Template**: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`

**Required Sections**:
1. Quick Assessment (TL;DR, effort estimate)
2. Decision Tree for AI Agents (structured IF/THEN)
3. What Changed (file-by-file with line counts)
4. Migration Steps (bash commands)
5. Testing After Upgrade (validation checklist)
6. Rollback Instructions
7. FAQ

**AI-Optimized Format**:
- Machine-parseable decision criteria
- Clear displacement risk assessment (ZERO/LOW/MEDIUM/HIGH)
- Structured upgrade effort estimate (<10min, 10-20min, 1-2hrs, etc.)
- Benefits vs costs analysis for optional changes

---

## Testing Strategy

### Template Generation Tests

```bash
# Test minimal configuration
copier copy --defaults . /tmp/test-minimal

# Test full-featured configuration
copier copy . /tmp/test-full
# Answer all prompts with "yes" for optional features

# Test specific project types
copier copy . /tmp/test-mcp --data project_type=mcp_server
copier copy . /tmp/test-lib --data project_type=library
copier copy . /tmp/test-cli --data project_type=cli_tool
```

### Generated Project Validation

```bash
# Validate generated project can setup and test
cd /tmp/test-project
./scripts/setup.sh
pytest
pre-commit run --all-files
just test  # if justfile included
```

### Update Path Testing

```bash
# Test template updates merge correctly
cd examples/full-featured-with-vision
git checkout -b test-update
copier update --vcs-ref main
# Resolve any conflicts
git diff  # Verify changes are reasonable
```

### Conditional Feature Testing

Test feature combinations that users commonly choose:

1. **Minimal MCP Server**: No memory, no docs, no Docker
2. **Full-Featured MCP Server**: All features enabled
3. **Library**: No CLI, yes docs, yes tests
4. **CLI Tool**: Yes CLI, yes tests, no memory

---

## Common Tasks for AI Agents

### Task 1: Add New Optional Feature

**Goal**: Add a new opt-in feature to the template

**Steps**:
1. Add question to `copier.yml`:
   ```yaml
   include_new_feature:
     type: bool
     help: Include new feature description?
     default: false
   ```

2. Add conditional exclusion:
   ```yaml
   _exclude:
     - "{% if not include_new_feature %}path/to/feature/files{% endif %}"
   ```

3. Create feature files in `template/` (use `.jinja` extension if templating needed)

4. Update `template/AGENTS.md.jinja` if feature affects AI agent workflows

5. Document in `README.md` under "Features" section

6. Add to `CHANGELOG.md` under `## [Unreleased]`

7. Test generation with feature on/off

### Task 2: Fix Bug in Template

**Goal**: Correct error in template that affects generated projects

**Steps**:
1. Reproduce in generated project:
   ```bash
   copier copy . /tmp/bug-test
   cd /tmp/bug-test
   # Reproduce issue
   ```

2. Fix in `template/` source files

3. Test fix:
   ```bash
   copier copy . /tmp/bug-fix-test
   cd /tmp/bug-fix-test
   # Verify fix works
   ```

4. Update `CHANGELOG.md` under `## [Unreleased]` in "Fixed" section

5. Commit with `fix(scope): description`

6. Create PATCH release if critical bug

### Task 3: Release New Version

**See**: "Releasing New Version" workflow above

**Checklist**:
- [ ] All tests pass (`copier copy . /tmp/test && cd /tmp/test && pytest`)
- [ ] CHANGELOG.md updated (Unreleased → [X.Y.Z])
- [ ] README.md updated (Recent Updates section)
- [ ] Upgrade guide created (`docs/upgrades/vX.Y-to-vX.Z.md`)
- [ ] Upgrade guide added to `docs/upgrades/README.md` table
- [ ] Commit with version in message
- [ ] Git tag created (`git tag vX.Y.Z`)
- [ ] Pushed to origin with tags (`git push origin main --tags`)
- [ ] GitHub release created (`gh release create vX.Y.Z`)

### Task 4: Update Research Documentation

**Goal**: Incorporate new research findings into template

**Steps**:
1. Save research document to `docs/research/`

2. Analyze research for actionable enhancements

3. Create plan with specific changes (e.g., Phase 1, 2, 3)

4. Implement changes (see Task 1: Add New Optional Feature)

5. Reference research in commit messages and upgrade guides

6. Update `README.md` or relevant docs with research-backed rationale

**Example**: v1.9.3 added super-tests, memory architecture, and query patterns based on "Agentic Coding Best Practices Research.pdf"

---

## Architecture Decisions

### Why Jinja2 Templating?

**Rationale**: Copier's native template engine, widely understood, supports conditionals
**Trade-off**: Can become verbose for complex logic (mitigated by `copier.yml` `_exclude`)

### Why Opt-In for Advanced Features?

**Rationale**: Prevent overwhelming new adopters, let users choose complexity
**Examples**: `documentation_advanced_features=false`, `include_docker=false`, `include_memory_system=true`

### Why Separate AGENTS.md.jinja (2,540 lines)?

**Known Issue**: AGENTS.md.jinja has grown 176% from v1.0.0 (782 lines) to v1.9.3 (2,540 lines) with zero refactoring
**Upcoming Change**: v2.0.0 will refactor to nested AGENTS.md structure per research recommendations
**Pattern**: Nearest file wins (tests/AGENTS.md, .chora/memory/AGENTS.md, etc.)
**Timeline**: v1.9.3 is final release before v2.0.0 refactoring

### Why docs/upgrades/ for Upgrade Guides?

**Rationale**: Centralized upgrade documentation, easy discovery, consistent structure
**Previous Mistake**: v1.9.0-to-v1.9.1 and v1.9.1-to-v1.9.2 were placed in repo root (lacked this AGENTS.md)
**Fix**: Moved to `docs/upgrades/` in v1.9.3 release

---

## Common Pitfalls & Prevention

### Pitfall 1: Misplaced Files

**Problem**: Placing files in wrong location (e.g., upgrade docs in repo root)
**Prevention**: Follow "File Organization Conventions" section above
**Detection**: Review `git status` before commit, check against conventions

### Pitfall 2: Forgetting .jinja Extension

**Problem**: Creating template files without `.jinja` extension
**Prevention**: All files in `template/` that use Jinja2 syntax MUST end in `.jinja`
**Detection**: Copier will warn if `{{` or `{%` found in non-.jinja files

### Pitfall 3: Breaking Conditional Logic

**Problem**: Adding `{% if ... %}` without updating `_exclude` in `copier.yml`
**Prevention**: Test with feature on AND off
**Detection**: Generate project with `include_feature=false`, verify files excluded

### Pitfall 4: Stale Examples

**Problem**: Example projects lag behind template changes
**Prevention**: Document in commit message: "Note: examples/ not updated (drift expected)"
**Detection**: Run `copier update` in examples/ periodically

### Pitfall 5: Incomplete Upgrade Guides

**Problem**: Missing sections in upgrade guide (no rollback, no testing)
**Prevention**: Use `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md` as checklist
**Detection**: Review against template before committing

### Pitfall 6: Version Number Errors

**Problem**: Tagging wrong version or skipping version in CHANGELOG
**Prevention**: Update CHANGELOG first, then tag with matching version
**Detection**: `git log --oneline` and `git tag -l` should align

---

## Integration Points

### Copier

**Version**: 9.0.0+ required (`_min_copier_version` in `copier.yml`)
**Key Files**: `copier.yml`, `template/`, `.copier-answers.yml` (in generated projects)

### Generated Projects

**Update Mechanism**: `copier update` (run from generated project directory)
**Configuration**: `.copier-answers.yml` (tracks answers, template version)
**Merge Strategy**: Smart merge (not overwrite) - Copier asks about conflicts

### GitHub Actions

**Workflows**: Template includes 7+ CI/CD workflows in `template/.github/workflows/`
**Secrets Required**: `PYPI_TOKEN` (if PyPI publishing enabled)
**Dependabot**: Auto-merge workflow for dependency updates

### Docker

**Optional Feature**: `include_docker=true`
**Strategies**: `production` (multi-stage + compose) or `ci-only` (Dockerfile.test only)
**Integration**: justfile commands (`docker-build`, `docker-test`, etc.)

---

## Memory System (A-MEM)

**Note**: chora-base template includes A-MEM as optional feature (`include_memory_system`)

**Purpose**: Cross-session learning for AI agents working on generated projects

**Components**:
- Event log (`.chora/memory/events/`) - Timestamped operation events
- Knowledge graph (`.chora/memory/knowledge/`) - Distilled learnings
- Profiles (`.chora/memory/profiles/`) - Per-agent learned patterns

**Not Applicable**: chora-base repository itself does not use memory system (no `.chora/` directory)

---

## Questions & Support

### Where to Find Information

**Template configuration**: `docs/reference/template-configuration.md`
**Upgrade philosophy**: `docs/upgrades/PHILOSOPHY.md`
**Version history**: `CHANGELOG.md`
**ROI analysis**: `docs/BENEFITS.md`
**Research**: `docs/research/`

### Where to Report Issues

**GitHub Issues**: https://github.com/liminalcommons/chora-base/issues
**Discussions**: https://github.com/liminalcommons/chora-base/discussions

### Version Information

**Current Version**: v1.9.3 (2025-10-22)
**Next Version**: v2.0.0 (MAJOR - nested AGENTS.md refactoring)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-22 | Initial AGENTS.md for chora-base repository (Phase 2 of v1.9.3 release) |

---

**End of AGENTS.md**

This document is the **source of truth** for AI agents and human developers working on chora-base. When in doubt, refer here first.
