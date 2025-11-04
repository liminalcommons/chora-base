# AGENTS.md - chora-base Template Repository

**Purpose**: Machine-readable instructions for AI agents working on the chora-base template repository.

**Last Updated**: 2025-11-02 (SAP-001 v1.1.0 inbox coordination integration)

---

## Project Overview

**chora-base** is a blueprint-driven Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates without relying on Copier.

**Repository Type**: Template repository (generates other projects)
**Primary Users**: Human developers and AI agents generating/maintaining Python projects
**Key Technology Stack**: Static scaffolding (`static-template/`), and Skilled Awareness Packages (SAP) for capability governance

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
│   │   ├── 01-setup-new-project.md
│   │   ├── 02-configure-testing.md
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
**Naming Pattern**: `NN-kebab-case-title.md` (e.g., `01-setup-new-project.md`)
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
   - Review adopter feedback from real projects (mcp-n8n, chora-compose, and others across MCP, REST, CLI, library domains)

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
   # Use AI agent to generate projects from static-template/ and SAP templates
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
# Use AI agent to generate projects from static-template/ and SAP templates

# Full-featured configuration
# Use AI agent to generate projects from static-template/ and SAP templates
# Enable all optional features when prompted

# Specific project types (run setup script and choose appropriate options)
# Use AI agent to generate projects from static-template/ and SAP templates
# Use AI agent to generate projects from static-template/ and SAP templates
# Use AI agent to generate projects from static-template/ and SAP templates
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

1. **Minimal Python Project**: Basic structure, no optional features
2. **Full-Featured Python Project**: All optional features enabled
3. **Library Project**: No CLI, yes docs, yes tests
4. **CLI Tool Project**: Yes CLI, yes tests
5. **MCP Server** (with SAP-014): MCP-specific features, optional memory/Docker

---

## Common Tasks for AI Agents

### Task 1: Add New Optional Feature

**Goal**: Add a new opt-in feature to the template

**Steps**:
1. Update relevant templates in technology-specific SAPs (e.g., static-template/mcp-templates/ for MCP) to include optional feature toggles.
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
**Key Files**: `static-template/`, technology-specific SAP templates, `docs/skilled-awareness/`

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

## SAP Evaluation Workflow

### Purpose

SAP-019 (Self-Evaluation) enables you to assess SAP adoption depth, identify gaps, and generate improvement roadmaps.

### When to Evaluate

- **After installing new SAP**: Validate installation (`--quick`)
- **Sprint planning**: Generate roadmap for next sprint (`--strategic`)
- **User asks "How's our SAP adoption?"**: Quick status check
- **User asks "How can we improve SAP-X?"**: Deep dive analysis
- **Quarterly reviews**: Track progress over time

### Evaluation Modes

**Quick Check** (30 seconds):
```bash
# Check all installed SAPs
python scripts/sap-evaluator.py --quick

# Check specific SAP
python scripts/sap-evaluator.py --quick SAP-004
```

**Deep Dive** (5 minutes):
```bash
# Analyze specific SAP, save report
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
```

**Strategic Analysis** (30 minutes):
```bash
# Generate quarterly roadmap
python scripts/sap-evaluator.py --strategic --output docs/adoption-reports/sap-roadmap.yaml
```

### Common Workflow: "How can we improve SAP-X?"

1. **Run deep dive**:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
   ```

2. **Read report** (use Read tool):
   ```
   Read: docs/adoption-reports/SAP-004-assessment.md
   ```

3. **Extract top 3 gaps** from report:
   - Gap 1 (P0): [Title], [Impact], [Effort], [Actions]
   - Gap 2 (P1): [...]
   - Gap 3 (P2): [...]

4. **Present to user**:
   ```markdown
   ## SAP-004 Improvement Opportunities

   **Current Level**: 1 (Basic)
   **Next Milestone**: Level 2

   ### Priority Gaps
   1. **[Gap 1 Title]** (P0, 3 hours)
      - Impact: [description]
      - Actions: [concrete steps]

   2. **[Gap 2 Title]** (P1, 1.5 hours)
      - Impact: [description]
      - Actions: [concrete steps]

   Shall I create tasks and implement Gap 1?
   ```

5. **Offer to execute**: If user agrees, use TodoWrite to create tasks, then implement

### Report Structure

Generated reports include:
- **Current State**: Adoption level, completion %, next milestone
- **Validation Results**: Automated checks (✅/❌)
- **Gap Analysis**: Prioritized gaps (P0/P1/P2) with concrete actions
- **Sprint Plan**: This sprint focus, next sprint goals

Example gap:
```
### Gap 1: Test coverage 0% < 85% target (P0)
**Impact**: High - Blocks SAP-005 CI/CD coverage gates
**Effort**: Medium - 3 hours, 8 tests needed
**Actions**:
1. Generate coverage report (5 min)
2. Write 8 tests for API handlers (2.5 hours)
3. Validate ≥85% coverage (2 min)
```

### Integration with Sprint Planning

**Sprint Planning Workflow**:
1. Run strategic analysis to generate roadmap
2. Review priority gaps (top 5)
3. Select 1-2 gaps for current sprint
4. Add to sprint backlog with time estimates
5. Track progress via re-evaluation at sprint end

**Quarterly Review**:
1. Generate strategic roadmap
2. Compare to previous quarter
3. Calculate adoption velocity
4. Update quarterly goals

### Tips for AI Agents

- **Start with quick check**: Don't deep dive unless user asks
- **Focus on top 3 gaps**: Don't overwhelm with full list
- **Prioritize P0 gaps**: These block other SAPs
- **Be specific**: Reference exact commands, files, line numbers from reports
- **Track progress**: Re-run evaluation after implementing improvements

---

## Bidirectional Translation Layer (Mutual Ergonomics)

### Overview

**Purpose**: Enable natural conversational interaction while executing procedurally within the ecosystem ontology.

**Core Principle**: Meet users where they are. You adapt to their communication style; they don't need to memorize exact commands.

### Tools Available

#### 1. Intent Router (`scripts/intent-router.py`)

Translates natural language to formal actions with confidence scoring.

**Usage**:
```python
from intent_router import IntentRouter

router = IntentRouter("docs/dev-docs/patterns/INTENT_PATTERNS.yaml")
matches = router.route(user_input)

if matches and matches[0].confidence >= 0.7:
    # High confidence: execute
    action = matches[0].action
    execute_action(action, matches[0].parameters)
elif matches and matches[0].confidence >= 0.5:
    # Medium confidence: ask for clarification
    clarify_with_user(matches[0])
else:
    # Low confidence: show alternatives
    show_alternatives(matches[:3])
```

**Common Patterns**:
- "show inbox" → `run_inbox_status`
- "how are saps" → `run_sap_evaluator_quick`
- "i want to suggest a big change" → `create_strategic_proposal`
- "review coordination requests" → `review_coordination_requests`

**Pattern Learning**: When user says something repeatedly that maps successfully, add it to triggers.

#### 2. Glossary Search (`scripts/chora-search.py`)

Enables terminology discovery and reverse lookup.

**Usage**:
```bash
# Forward lookup: term → definition
python scripts/chora-search.py "coordination request"

# Reverse lookup: description → term
python scripts/chora-search.py --reverse "I want to suggest a big change"
# Returns: Strategic Proposal (95% confidence)

# Fuzzy matching: handles typos
python scripts/chora-search.py --fuzzy "coordenation"
```

**When to Use**:
- User asks "What is X?"
- User uses unfamiliar terminology
- User describes concept without using correct term
- User makes typos

#### 3. User Preferences (`.chora/user-preferences.yaml`)

Adapt behavior based on user working style.

**Key Preferences**:
- `verbosity`: concise | standard | verbose
- `formality`: casual | standard | formal
- `output_format`: terminal | markdown | json
- `require_confirmation`: always | destructive | never
- `progressive_disclosure`: true | false

**Loading**:
```python
import yaml
from pathlib import Path

prefs_file = Path(".chora/user-preferences.yaml")
if prefs_file.exists():
    with open(prefs_file) as f:
        prefs = yaml.safe_load(f)

    # Adapt verbosity
    if prefs["communication"]["verbosity"] == "concise":
        return brief_summary()
    elif prefs["communication"]["verbosity"] == "verbose":
        return detailed_report()
```

#### 4. Suggestion Engine (`scripts/suggest-next.py`)

Context-aware next action recommendations.

**Usage**:
```bash
# When user asks "what next?" or "what should I do?"
python scripts/suggest-next.py

# Proactive mode (high-priority suggestions only)
python scripts/suggest-next.py --mode proactive
```

**Context Signals**:
- Recent events (last 24 hours)
- Active work items (inbox/active/)
- Current phase (DDD/BDD/TDD detection)
- Quality metrics (coverage, tests, lint)
- Inbox backlog

### Communication Patterns

#### Pattern 1: Natural Input → Execution → Result

**Don't explain what you'll do, show what you did**:

```
❌ Bad:
User: "Create coordination request for traceability"
Agent: "To create a coordination request, you should:
       1. Create JSON in inbox/incoming/coordination/
       2. Use schema from inbox/schemas/
       3. ..."

✅ Good:
User: "Create coordination request for traceability"
Agent: ✅ Created coord-007-traceability-pilot.json
       ✅ Logged event: coordination_request_created
       Next: Submit for sprint planning (2025-11-15)?
```

#### Pattern 2: Progressive Formalization

Move from casual → formal as needed:

```
"I want to add health monitoring" (casual)
  → Strategic Proposal (semi-formal artifact)
  → RFC (formal discussion)
  → ADR (formal decision)
  → Coordination Request (fully formal)
  → Implementation (procedural)
```

#### Pattern 3: Adaptive Output

Match user preferences:

```python
# Concise user
"✅ 12 SAPs installed. Top gap: coverage 60%"

# Verbose user
"""
SAP Adoption Status
===================
- 12/18 SAPs installed (67%)
- Level 2: SAP-004, SAP-019
- Top gap: Test coverage at 60% (need 85%)
  Action: Add 45 tests, est. 4-6 hours
"""
```

#### Pattern 4: Context Retention

Remember conversation context:

```
User: "Show inbox"
Agent: [Shows 3 coordination requests]

User: "Review the first one"
Agent: [Recognizes "first one" = coord-003]
       [Shows coord-003 details]
```

### Anti-Patterns (Avoid These)

❌ **Forcing Exact Syntax**: "Command not recognized" when user says "show me the inbox"
❌ **Explaining Instead of Executing**: Long explanations of what to do instead of doing it
❌ **Ignoring Preferences**: Always verbose output even when user wants concise
❌ **No Context**: Asking "what do you mean by 'it'?" when referent is clear
❌ **Static Patterns**: Never learning new phrases user repeats successfully

### Learning & Adaptation

**Pattern Learning**:
- User says "what's cooking in the inbox?" 3+ times
- Intent router matches to `inbox_status` successfully
- Automatically add "what's cooking" to triggers
- Future queries: instant recognition

**Preference Evolution**:
- User says "too much detail" → Update `verbosity: concise`
- User repeatedly cancels confirmations → Suggest `require_confirmation: destructive`
- Track which features user uses → Recommend relevant SAPs

**Expertise Tracking**:
- User has used coordination requests 10+ times
- Next time: Brief reminder instead of full explanation
- Adapt detail level as user gains expertise

### Integration Points

**See Also**:
- [Bidirectional Communication Pattern Guide](docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md) - Complete pattern documentation
- [Intent Patterns Database](docs/dev-docs/patterns/INTENT_PATTERNS.yaml) - All recognized patterns
- [Glossary](docs/GLOSSARY.md) - Ecosystem terminology (75+ terms)
- [User Preferences Template](.chora/user-preferences.yaml.template) - Configuration options

---

## Inbox Coordination (SAP-001 v1.1.0)

### Session Startup Routine

**Every new session, check inbox for coordination requests**:

```bash
# Visual status dashboard (recommended for human-readable overview)
python scripts/inbox-status.py

# Quick inbox count summary
python scripts/inbox-query.py --count-by-status

# View unacknowledged items (if any)
python scripts/inbox-query.py --incoming --unacknowledged --format summary
```

**Expected Output**:
```
Inbox Status Counts:
  Incoming Coordination: 12
  Incoming Tasks: 0
  Incoming Proposals: 0
  Active: 3
  Completed: 45
  Unacknowledged: 12
```

### Daily Inbox Workflows

#### Morning Routine (2-3 minutes)

1. **Check for new items**:
   ```bash
   python scripts/inbox-query.py --incoming --unacknowledged
   ```

2. **Review high-priority items** (P0, blocks_sprint urgency):
   ```bash
   # View specific request
   python scripts/inbox-query.py --request COORD-2025-XXX --format json
   ```

3. **Acknowledge within SLA** (1 business day, 4 hours for blocks_sprint):
   ```bash
   python scripts/respond-to-coordination.py \
     --request COORD-2025-XXX \
     --status acknowledged \
     --notes "Reviewing - will respond by [date]"
   ```

#### Processing Coordination Requests

**Accept and Start Work**:
```bash
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status accepted \
  --effort "8-12 hours" \
  --timeline "Complete by 2025-11-15" \
  --notes "Starting implementation in current sprint" \
  --move-to-active
```

**Decline with Reason**:
```bash
python scripts/respond-to-coordination.py \
  --request COORD-2025-XXX \
  --status declined \
  --reason "Outside current scope. Recommend proposing for Q1 2026 roadmap."
```

**Check Active Work**:
```bash
python scripts/inbox-query.py --status in_progress
```

### Creating Coordination Requests

**Interactive Mode** (recommended for new users):
```bash
python scripts/generate-coordination-request.py --interactive
```

**Context File Mode** (for AI agents):
```bash
# Create context file
cat > inbox/draft/my-request-context.json << 'EOF'
{
  "title": "Add Feature X to Repository Y",
  "description": "Brief description of what needs to be done",
  "background": "Why this is needed, current state",
  "rationale": "Benefits and justification",
  "priority": "P1",
  "urgency": "next_sprint",
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/target-repo"
}
EOF

# Generate request with AI-powered deliverables and acceptance criteria
python scripts/generate-coordination-request.py \
  --context inbox/draft/my-request-context.json \
  --ai-model claude-sonnet-4-5-20250929 \
  --output inbox/draft/my-request.json
```

**Quality**: Generator produces 94.9% quality deliverables and SMART acceptance criteria

### Service Level Agreements (SLAs)

**Response Times by Urgency**:

| Urgency | Acknowledgment | Full Response | When to Use |
|---------|---------------|---------------|-------------|
| `blocks_sprint` | 4 hours | Same day | Blocking current sprint work |
| `next_sprint` | 1 business day | 3 business days | Needed for next sprint |
| `backlog` | 1 business day | 1 week | Non-urgent, future planning |

**SLA Compliance**:
- Check inbox at session startup
- Prioritize `blocks_sprint` items immediately
- Acknowledge all items within 1 business day
- Provide full response within urgency-based timeline

### Ecosystem Coordination

**Repository Status**: Active participant in ecosystem coordination

**Capabilities**:
- **Provides**: Template generation, SAP framework, coordination protocol
- **Receives**: Feature requests, bug reports, integration proposals

**Ecosystem Dashboard**: [inbox/ecosystem/ECOSYSTEM_STATUS.yaml](inbox/ecosystem/ECOSYSTEM_STATUS.yaml)

**Ecosystem Invitations**: See [inbox/ecosystem/invitations/](inbox/ecosystem/invitations/) for pending invitations

### Inbox Status Dashboard

**For generic agents and quick visual overview**:

```bash
# Full visual dashboard (recommended)
python scripts/inbox-status.py

# Detailed view with item listings
python scripts/inbox-status.py --detailed

# JSON export for programmatic access
python scripts/inbox-status.py --format json

# Markdown report for documentation
python scripts/inbox-status.py --format markdown > inbox-report.md

# Filter by priority
python scripts/inbox-status.py --priority P0 --detailed

# Recent activity (last 7 days)
python scripts/inbox-status.py --last 7d
```

**Dashboard Output Includes**:
- 📥 Incoming queue counts (coordination, tasks, context)
- 🔄 Active work items with details
- ⏱️ Recent activity timeline (last 20 events)
- ✅ Recent completions (last 30 days)
- 💡 Summary with actionable counts

**Use Cases**:
- Session startup: Get at-a-glance status
- Generic agent queries: "inbox status" → run this tool
- Status reports: Export markdown for weekly updates
- Priority triage: Filter by P0/P1 for urgent items
- Trace investigation: `--trace-id` to follow request chains

### Troubleshooting

**Issue: "Item not found"**
- Use full filename as request ID: `COORD-2025-XXX-description` not just `COORD-2025-XXX`
- Check file exists: `ls inbox/incoming/coordination/COORD-2025-XXX*`

**Issue: "No items found"**
- Verify working directory: Must run commands from project root
- Check inbox path: `ls inbox/incoming/coordination/`

**Issue: Post-processing error**
- Skip post-processing: Remove `--post-process` flag
- Use custom output: `--output inbox/draft/my-request.json`

### Key Resources

- **Protocol Spec**: [docs/skilled-awareness/inbox/protocol-spec.md](docs/skilled-awareness/inbox/protocol-spec.md) (SAP-001 v1.1.0)
- **Onboarding Guide**: [docs/ECOSYSTEM_ONBOARDING.md](docs/ECOSYSTEM_ONBOARDING.md)
- **Phase 1 Summary**: [docs/PHASE_1_COMPLETION_SUMMARY.md](docs/PHASE_1_COMPLETION_SUMMARY.md)
- **Validation Report**: [docs/PHASE_1_VALIDATION_REPORT.md](docs/PHASE_1_VALIDATION_REPORT.md)
- **v1.1.0 Announcement**: [inbox/ecosystem/announcements/SAP-001-v1.1.0-RELEASE.md](inbox/ecosystem/announcements/SAP-001-v1.1.0-RELEASE.md)

---

## SAP Adoption Quarterly Review

### Overview

**When**: End of each quarter (Q1: March 31, Q2: June 30, Q3: September 30, Q4: December 31)

**Purpose**: Systematically evaluate SAP adoption progress, identify gaps, and plan next quarter's adoption roadmap using SAP-019 (self-evaluation) tools.

**Duration**: 30-60 minutes per quarter

**Outputs**:
- Strategic roadmap YAML (`project-docs/sap-roadmap-QX-YYYY.yaml`)
- Quarterly review markdown (`docs/adoption-reports/QX-YYYY-review.md`)
- Updated adoption history (`adoption-history.jsonl`)

### Process

**Step 1: Generate Strategic Roadmap** (5 minutes)

```bash
python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
```

This analyzes all installed SAPs, identifies gaps, and creates a prioritized roadmap.

**Step 2: Create Review Document** (10 minutes)

```bash
python scripts/sap-evaluator.py --strategic --format markdown --output docs/adoption-reports/Q{X}-{YEAR}-review.md
```

Or manually create review document with:
- Progress since last quarter (SAPs installed, levels achieved)
- Velocity metrics (SAPs/month, level progressions/month)
- Successes and blockers
- Top 5 priority gaps from roadmap

**Step 3: Analyze Progress** (15 minutes)

Compare to previous quarter:
- How many SAPs progressed to higher levels?
- What was the adoption velocity?
- Which gaps were resolved?
- Which gaps remain unresolved (blockers)?

Calculate velocity:
- SAPs adopted per month
- Level progressions per month
- Hours invested vs hours saved (ROI)

**Step 4: Update Goals** (10 minutes)

Based on roadmap and analysis:
- Set targets for next quarter (# of SAPs to L2, # to L3)
- Prioritize 3-5 focus SAPs from roadmap
- Estimate ROI potential from priority gaps
- Identify blockers to address

**Step 5: Commit Review** (5 minutes)

```bash
git add project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
git add docs/adoption-reports/Q{X}-{YEAR}-review.md
git add adoption-history.jsonl  # If manually updated
git commit -m "docs(sap-019): Q{X}-{YEAR} adoption review

- Strategic roadmap generated
- Progress analysis completed
- Next quarter goals set

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Example Review Document Structure

```markdown
# Q4-2025 SAP Adoption Review

**Generated**: 2025-12-31
**Review Period**: October 1 - December 31, 2025

## Progress Summary

### SAPs Adopted
- Total SAPs: 8 (was 6 in Q3)
- New adoptions: SAP-004, SAP-019

### Level Progression
- Level 2: 4 SAPs (was 2 in Q3)
- Level 3: 1 SAP (was 0 in Q3)
- Average level: 1.75 (was 1.33 in Q3)

### Velocity
- SAPs adopted: 0.67/month (2 in 3 months)
- Level progressions: 1.0/month (3 in 3 months)
- Hours invested: 12 hours this quarter

## Successes

1. **SAP-019 to L3**: Self-evaluation operational, strategic roadmaps generated
2. **SAP-004 to L2**: Test coverage improved from 0% to 75%
3. **SAP-013 integration**: ROI tracking now includes SAP adoption

## Blockers

1. **SAP-004 test coverage gap**: Still below 85% target, blocked by missing pytest fixtures
2. **SAP-009 documentation**: No domain-specific AGENTS.md files created yet

## Next Quarter Goals (Q1-2026)

### Targets
- Bring SAP-004 to L3 (complete test coverage to 85%+)
- Adopt 2 new SAPs (SAP-014, SAP-016)
- Achieve 2.0 average adoption level

### Focus SAPs
1. SAP-004 (testing-framework) - Priority P0, blocks sprint
2. SAP-009 (agent-awareness) - Priority P1, improves documentation
3. SAP-014 (mcp-server-development) - Priority P2, enables MCP development

### Estimated ROI
- Hours to invest: 8-10 hours
- Hours to save: 15-20 hours/quarter
- Expected ROI: 1.75x

## Roadmap

See [project-docs/sap-roadmap-Q1-2026.yaml](../project-docs/sap-roadmap-Q1-2026.yaml) for detailed sprint breakdown.
```

### Tips

**Automate Data Collection**:
- `adoption-history.jsonl` tracks all SAP events automatically
- `python scripts/sap-evaluator.py --quick` shows current state
- Compare git history: `git log --since="3 months ago" --grep="sap-"`

**Focus on Value**:
- Prioritize gaps with highest ROI (hours_saved / hours_invested)
- Address blockers first (gaps blocking other gaps)
- Celebrate wins (completed levels, new adoptions)

**Keep It Short**:
- 30-60 minutes maximum
- Use tools to generate data
- Focus on decisions, not documentation

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
