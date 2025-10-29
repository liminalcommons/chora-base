# AGENTS.md - chora-base Template Repository

**Purpose**: Machine-readable instructions for AI agents working on the chora-base template repository.

**Last Updated**: 2025-10-22 (v1.9.3)

---

## Project Overview

**chora-base** is a blueprint-driven Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates without relying on Copier.

**Repository Type**: Template repository (generates other projects)
**Primary Users**: Human developers and AI agents generating/maintaining Python projects
**Key Technology Stack**: Blueprint bundles (`blueprints/`), static scaffolding (`static-template/`), and Skilled Awareness Packages (SAP) for capability governance

### Key Concepts

- **Template vs Generated Project**: chora-base is the template; generated projects are adopters
- **Blueprint Generation**: `.blueprint` files define how adopters bootstrap projects via scripted or agent-led workflows
- **Static Assets**: `static-template/` contains ready-to-copy files used by blueprints
- **Skilled Awareness Packages (SAPs)**: Each major capability ships with charter, protocol, awareness guide, adoption blueprint, and ledger entry to guide humans and AI agents
- **Upgrade Path**: Adopters follow SAP adoption blueprints and ledger/broadcast updates to stay aligned with the template

---

## Skilled Awareness Packages (SAPs)

### Overview

chora-base packages all major capabilities as **Skilled Awareness Packages (SAPs)** — complete, installable bundles with clear contracts and agent-executable blueprints.

**Why SAPs Matter**:
- Clear contracts (explicit guarantees, no assumptions)
- Predictable upgrades (sequential adoption, migration blueprints)
- Machine-readable (AI agents can parse and execute)
- Governance (versioning, change management, tracking)

### SAP Structure

Every SAP includes:

1. **5 Core Artifacts**:
   - Capability Charter (problem, scope, outcomes)
   - Protocol Specification (technical contract)
   - Awareness Guide (agent execution patterns)
   - Adoption Blueprint (installation steps)
   - Traceability Ledger (adopter tracking)

2. **Infrastructure** (schemas, templates, configs, directories)

3. **Testing Layer** (optional validation)

### Key Documents

**Root Protocol**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- Defines what SAPs are and how they work
- Installation pattern (blueprint-based, not scripts)
- Integration with DDD → BDD → TDD
- Scope levels (Vision & Strategy, Planning, Implementation)

**SAP Index**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
- Registry of all 14 capabilities
- Current coverage: 2/14 (14%)
- Target coverage: 100% by Phase 4 (2026-05)
- Dependencies, priorities, effort estimates

**Framework SAP**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- Meta-SAP defining the SAP pattern itself
- Complete reference implementation
- Templates and guidelines

**Reference Implementation**: [docs/skilled-awareness/inbox/](docs/skilled-awareness/inbox/)
- Pilot SAP for cross-repo coordination
- Complete example with infrastructure and testing

### Creating SAPs

**When to Create SAP**:
- New major capability (e.g., testing-framework, docker-operations)
- Capability needs structured governance
- Multiple adopters will use capability
- Clear upgrade path needed

**Process**:
1. Read: [docs/skilled-awareness/document-templates.md](docs/skilled-awareness/document-templates.md)
2. Create directory: `docs/skilled-awareness/<capability-name>/`
3. Create 5 artifacts using templates
4. Add infrastructure (schemas, templates, etc.)
5. Update SAP Index: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
6. Follow DDD → BDD → TDD:
   - DDD: Create Charter + Protocol
   - BDD: Define acceptance criteria
   - TDD: Implement infrastructure + Awareness + Blueprint

**Time Estimate**: 8-20 hours per SAP (varies by complexity)

### Installing SAPs

**Process**:
1. Find SAP in INDEX.md
2. Navigate to SAP directory (e.g., `docs/skilled-awareness/inbox/`)
3. Read `adoption-blueprint.md`
4. Execute installation steps sequentially
5. Run validation commands
6. Update `ledger.md` (add adopter record)

**Example**:
```bash
# Find SAP
cat docs/skilled-awareness/INDEX.md

# Read blueprint
cat docs/skilled-awareness/inbox/adoption-blueprint.md

# Execute steps (agent-executable markdown instructions)
# ... follow blueprint step-by-step ...

# Validate
ls inbox/coordination/CAPABILITIES && echo "✅ Installed"
```

### SAP Roadmap

**Phase 1** (2025-10 → 2025-11): Framework Hardening
- ✅ SAP-000 (sap-framework)
- ✅ SAP-001 (inbox-coordination, pilot)
- 🔄 SAP-002 (chora-base-meta)

**Phase 2** (2025-11 → 2026-01): Core Capabilities
- SAP-003 (project-bootstrap)
- SAP-004 (testing-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)

**Phase 3** (2026-01 → 2026-03): Extended Capabilities
- SAP-007 (documentation-framework)
- SAP-008 (automation-scripts)
- SAP-009 (agent-awareness)
- SAP-010 (memory-system / A-MEM)
- SAP-011 (docker-operations)
- SAP-012 (development-lifecycle)

**Phase 4** (2026-03 → 2026-05): Optimization
- SAP-013 (metrics-tracking)

**See**: [docs/skilled-awareness/chora-base-sap-roadmap.md](docs/skilled-awareness/chora-base-sap-roadmap.md)

---

## Repository Structure

```
chora-base/
├── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  # Root SAP protocol
├── static-template/             # Static scaffolding copied into generated projects
│   ├── src/                     # Python source baseline
│   ├── tests/                   # Test baseline
│   ├── scripts/                 # Automation scripts
│   ├── .github/workflows/       # CI/CD workflows
│   └── ...                      # Other project files
├── blueprints/                  # Blueprint bundles for bootstrapping adopters
│   ├── README.md.blueprint
│   ├── CLAUDE.md.blueprint
│   ├── AGENTS.md.blueprint
│   └── ...
├── docs/                        # Template documentation
│   ├── reference/
│   │   ├── skilled-awareness/   # SAP Framework & all SAPs
│   │   │   ├── INDEX.md         # SAP registry (all 14 capabilities)
│   │   │   ├── document-templates.md  # Templates for creating SAPs
│   │   │   ├── chora-base-sap-roadmap.md  # Phased adoption plan
│   │   │   ├── sap-framework/   # SAP-000: Framework SAP (meta-capability)
│   │   │   ├── inbox/           # SAP-001: Inbox coordination (pilot)
│   │   │   ├── chora-base/      # SAP-002: chora-base meta-SAP (planned)
│   │   │   └── ...              # Future SAPs (project-bootstrap, testing, etc.)
│   │   ├── template-configuration.md
│   │   └── ...
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
│   ├── explanation/             # Conceptual explanations
│   ├── research/                # Research documents
│   │   └── Agentic Coding Best Practices Research.pdf
│   ├── BENEFITS.md              # ROI analysis
│   └── DOCUMENTATION_PLAN.md    # Documentation strategy
├── inbox/                       # Inbox coordination capability (SAP-001)
│   ├── INBOX_PROTOCOL.md        # Protocol
│   ├── CLAUDE.md                # Awareness
│   ├── schemas/                 # JSON schemas
│   ├── coordination/            # Coordination directory
│   └── examples/                # Complete examples (e.g., health-monitoring-w3)
├── examples/                    # Example generated projects
│   ├── full-featured-with-vision/
│   ├── full-featured-with-docs/
│   └── ...
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
   - Determine whether capability needs its own Skilled Awareness Package (SAP)
   - Update relevant blueprints and static assets to include the feature

3. **Implementation Phase**
   - Update `static-template/` and `blueprints/` assets
   - Add automation or install scripts if feature is optional
   - Run blueprint generation scripts (or agent-assisted flow) to validate outputs
   - Generate/update examples in `examples/` if demonstrating complex feature

4. **Documentation Phase**
   - Update `README.md` if user-facing feature
   - Add to `template/AGENTS.md.jinja` if relevant to AI agents
   - Document in appropriate `docs/` subdirectory
   - Update `docs/BENEFITS.md` if adding measurable value
   - Create/refresh SAP documents (charter, protocol, awareness guide, adoption blueprint, ledger entry)

5. **Validation Phase**
   - Generate fresh project using blueprint workflow (see setup guides)
   - Run generated project's tests: `cd /tmp/test-validation && ./scripts/setup.sh && pytest`
   - Test upgrade path: follow SAP adoption blueprint scenarios (e.g., apply updates to example repos)
   - Verify conditional combinations (Docker on/off, memory on/off, etc.)

### Releasing New Version

**Version Numbering**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR** (X.0.0): Breaking changes requiring adopter action
- **MINOR** (1.X.0): New features, additive changes (current: v1.9.3)
- **PATCH** (1.1.X): Bug fixes only

**Release Process**:

1. **Pre-Release Validation**
   ```bash
   # Generate project from blueprints (interactive; answer prompts as needed)
   python setup.py /tmp/test-release
   cd /tmp/test-release && ./scripts/setup.sh && pytest

   # Test update path (use example project + SAP adoption blueprint)
   cd examples/full-featured-with-vision
   # Follow relevant SAP adoption blueprint to apply latest changes
   ./scripts/setup.sh && pytest
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
# Minimal configuration (accept defaults)
python setup.py /tmp/test-minimal

# Full-featured configuration
python setup.py /tmp/test-full
# Enable all optional features when prompted

# Specific project types (run setup script and choose appropriate options)
python setup.py /tmp/test-mcp
python setup.py /tmp/test-lib
python setup.py /tmp/test-cli
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
# Test template updates merge correctly (use SAP adoption blueprint)
cd examples/full-featured-with-vision
git checkout -b test-update
# Apply latest blueprint changes manually or via automation scripts
# Resolve any conflicts and verify diff is reasonable
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
1. Update relevant blueprint(s) in `blueprints/` to include optional feature toggles.
2. Add conditional logic or installation hooks in `static-template/` and supporting scripts.
3. Refresh SAP documents (especially protocol + adoption blueprint) to describe the new capability.
4. Update `template/AGENTS.md.jinja` if feature affects AI agent workflows.
5. Document in `README.md` under "Features" section.
6. Add to `CHANGELOG.md` under `## [Unreleased]`.
7. Test blueprint generation with feature enabled/disabled via `python setup.py`.

### Task 2: Fix Bug in Template

**Goal**: Correct error in template that affects generated projects

**Steps**:
1. Reproduce in generated project:
   ```bash
   python setup.py /tmp/bug-test
   cd /tmp/bug-test
   # Reproduce issue
   ```

2. Fix in `template/` source files

3. Test fix:
   ```bash
   python setup.py /tmp/bug-fix-test
   cd /tmp/bug-fix-test
   # Verify fix works
   ```

4. Update `CHANGELOG.md` under `## [Unreleased]` in "Fixed" section

5. Commit with `fix(scope): description`

6. Create PATCH release if critical bug

### Task 3: Release New Version

**See**: "Releasing New Version" workflow above

**Checklist**:
- [ ] All tests pass (`python setup.py /tmp/test && cd /tmp/test && pytest`)
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

**Rationale**: Blueprints use Jinja2 placeholders for flexible customization and remain compatible with existing project content
**Trade-off**: Complex conditionals require disciplined structure; mitigate with helper scripts and clear template snippets

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

### Pitfall 2: Forgetting Template Metadata

**Problem**: Creating blueprint files without required metadata or helper comments
**Prevention**: Follow blueprint conventions (header comments, clear placeholder instructions)
**Detection**: Run blueprint lint scripts or manual review before committing

### Pitfall 3: Breaking Conditional Logic

**Problem**: Adding `{% if ... %}` without updating supporting install scripts or awareness docs
**Prevention**: Test with feature on AND off via `python setup.py`; update SAP adoption blueprint accordingly
**Detection**: Generate project with feature disabled, verify files excluded and docs consistent

### Pitfall 4: Stale Examples

**Problem**: Example projects lag behind template changes
**Prevention**: Document in commit message: "Note: examples/ not updated (drift expected)"
**Detection**: Periodically regenerate examples using `python setup.py` and compare to current blueprint outputs

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

### Blueprint Engine

**Tooling**: `setup.py` interactive generator (can be wrapped by automation scripts)
**Key Files**: `blueprints/`, `static-template/`, `docs/skilled-awareness/`

### Generated Projects

**Update Mechanism**: Follow capability-specific SAP adoption blueprints and ledger guidance
**Configuration**: Project metadata stored in generated files (`pyproject.toml`, `AGENTS.md`, etc.); no `.copier-answers.yml`
**Merge Strategy**: Manual or scripted merge guided by SAP protocols (e.g., apply blueprint diffs, run tests, update docs)

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
