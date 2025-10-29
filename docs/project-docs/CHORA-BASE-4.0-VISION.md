# Chora-Base 4.0.0 Vision & Roadmap

**Version**: 1.0 (Draft)
**Created**: 2025-10-28
**Status**: Planning
**Target Release**: Q1 2026

---

## Executive Summary

Chora-Base v4.0 represents a fundamental transformation from "MCP server template generator" to "Universal project foundation with SAP-based capability adoption." This evolution enables consistent project structure across all repositories, LLM-navigable processes, and upgradeable foundations through git merge workflows.

**Key Changes**:
- Clone-based project creation (not template generation)
- Universal 4-domain documentation architecture
- SAP-based capability installation
- Upstream structural updates via git merge
- Language/framework agnostic foundation

---

## Current State: v3.3.0

### Achievements
- ✅ 14 SAPs with 100% coverage (70 artifacts)
- ✅ Template-based project generation (blueprints/ + setup.py)
- ✅ Comprehensive MCP server scaffold
- ✅ Documentation framework (Diátaxis-inspired)
- ✅ Complete automation tooling

### Pain Points
- ❌ Template generation locks projects to creation-time version
- ❌ No upgrade path from chora-base improvements
- ❌ Mixed documentation structure (inconsistent root vs. static-template)
- ❌ MCP-specific assumptions in base (should be optional capability)
- ❌ Two conflicting patterns: blueprints vs. SAP adoption
- ❌ Valuable MCP expertise not packaged for reuse

### Technical Debt
- blueprints/ and setup.py automation (to be removed, content → SAP-014)
- Inconsistent docs/ structure
- MCP-specific assumptions in root documentation (to be extracted → SAP-014)
- Missing: chora-base user documentation
- Missing: Technology-specific SAPs (MCP, Django, FastAPI, etc.)
- 2020 uncovered files journey created cleanup opportunities

---

## Vision: v4.0.0 - Universal Project Foundation

### Core Transformation

**FROM**: Template that generates isolated projects
**TO**: Living foundation that projects extend

**FROM**: MCP server specific
**TO**: Language/framework agnostic with optional technology SAPs (SAP-014: MCP, future: Django, FastAPI, etc.)

**FROM**: Generate once, diverge forever
**TO**: Clone, customize content, merge structural updates

### Key Principles

1. **Clone, Don't Generate**
   - Chora-base is a git repository to clone, not a template to process
   - Maintains connection to upstream for updates
   - Clear separation: structure (merge) vs. content (customize)

2. **Structure is Universal**
   - All projects share 4-domain documentation architecture
   - Consistent file locations, naming conventions
   - Predictable navigation for LLMs and humans

3. **Content is Customizable**
   - What goes IN the structure varies per project
   - Projects add domain-specific SAPs
   - Implementation details differ, structure doesn't

4. **SAPs are Portable**
   - Copy capability packages from chora-base or other repos
   - Create project-specific SAPs
   - Share SAPs across organization

5. **Upgrades are Mergeable**
   - Structural improvements pull from upstream via git merge
   - Content remains untouched
   - Clear conflict resolution for hybrid files

6. **LLM-First Ergonomics**
   - Claude can navigate all processes from documentation alone
   - Single entry point, clear workflows
   - Step-by-step adoption blueprints

### The 4-Domain Architecture

```
repo/
├── docs/
│   ├── dev-docs/              ← Developer process (Diátaxis for development)
│   │   ├── workflows/         ← DDD, BDD, TDD, processes
│   │   ├── examples/          ← Code walkthroughs
│   │   ├── vision/            ← Long-term capability roadmap
│   │   └── research/          ← Technical investigations
│   │
│   ├── project-docs/          ← Project lifecycle artifacts
│   │   ├── sprints/           ← Sprint planning & retrospectives
│   │   ├── releases/          ← Release notes & plans
│   │   ├── metrics/           ← Process & quality metrics
│   │   ├── integration/       ← Integration plans & coordination
│   │   └── inventory/         ← Repository audits & coherence reports
│   │
│   ├── user-docs/             ← End-user documentation (Diátaxis for product)
│   │   ├── how-to/            ← Task-oriented guides
│   │   ├── explanation/       ← Conceptual deep-dives
│   │   ├── reference/         ← API docs, config specs
│   │   └── tutorials/         ← Learning-oriented lessons
│   │
│   └── skilled-awareness/     ← SAP Framework (meta-layer)
│       ├── INDEX.md           ← Central SAP registry
│       ├── document-templates.md
│       ├── sap-framework/     ← SAP-000 (always included)
│       └── [capability-saps]/ ← Adopted or created SAPs
│
├── src/                       ← System: Source code
├── tests/                     ← System: Test suite
├── scripts/                   ← System: Automation & tooling
├── .github/                   ← System: CI/CD workflows
├── docker/                    ← System: Container configs (optional)
│
├── AGENTS.md                  ← Root: Agent guidance (structured sections)
├── CLAUDE.md                  ← Root: Claude-specific optimizations
├── README.md                  ← Root: Project overview
├── CHANGELOG.md               ← Root: Version history
├── ROADMAP.md                 ← Root: Product roadmap
└── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  ← Root: SAP protocol spec
```

#### Domain Purposes

**dev-docs/** - For developers working ON the product
- **Audience**: Engineers building features
- **Diátaxis**: How-to process guides, conceptual explanations
- **Examples**: DDD_WORKFLOW.md, testing-philosophy.md

**project-docs/** - Artifacts from project lifecycle
- **Audience**: PMs, stakeholders, future maintainers
- **Content**: Living documents generated/updated during work
- **Examples**: Sprint plans, release notes, metrics reports

**user-docs/** - For users of the delivered product
- **Audience**: End-users, API consumers
- **Diátaxis**: How-to use, explanations, tutorials
- **Examples**: API reference, integration guides

**skilled-awareness/** - SAP meta-layer
- **Audience**: All roles (cross-cutting capabilities)
- **Content**: Capability packages that reference all other domains
- **Examples**: SAP-004 references dev-docs/workflows/ and tests/

---

## Wave 1: Documentation Architecture Unification (v3.4.0)

**Goal**: Align chora-base root docs/ with universal 4-domain structure

### Current State Analysis

**Root docs/ structure**:
```
docs/
├── BENEFITS.md              ← About chora-base (where does this go?)
├── DOCUMENTATION_PLAN.md    ← Meta-doc (should be in project-docs/)
├── integration/             ← Integration plans (→ project-docs/)
├── inventory/               ← Inventory reports (→ project-docs/)
├── reference/               ← Mixed content (needs reorganization)
│   ├── skilled-awareness/   ← KEEP (correct location)
│   ├── ecosystem/           ← Architecture docs (→ ?)
│   └── chora-compose/       ← DELETED (obsolete)
├── releases/                ← Release notes (→ project-docs/)
└── research/                ← Research docs (→ dev-docs/ or project-docs/)
```

**static-template/ structure** (already correct):
```
static-template/
├── dev-docs/        ✅ Correct
├── project-docs/    ✅ Correct
├── user-docs/       ✅ Correct
└── [no skilled-awareness/]  ← Need to add SAP-000
```

### Tasks

#### 1.1: Create Missing Directories

```bash
mkdir -p docs/dev-docs/research
mkdir -p docs/project-docs/{integration,inventory,releases}
mkdir -p docs/user-docs/{how-to,explanation,reference,tutorials}
```

#### 1.2: Move Files to Correct Domains

**To dev-docs/**:
- `docs/research/` → `docs/dev-docs/research/`
  - adopter-learnings-mcp-orchestration.md
  - adopter-learnings-executable-docs.md
  - CLAUDE_Complete.md

**To project-docs/**:
- `docs/DOCUMENTATION_PLAN.md` → `docs/project-docs/DOCUMENTATION_PLAN.md`
- `docs/integration/` → `docs/project-docs/integration/`
  - v3.3.0-integration-plan.md
  - v3.2.0-integration-plan.md
- `docs/inventory/` → `docs/project-docs/inventory/`
  - All inventory reports
- `docs/releases/` → `docs/project-docs/releases/`
  - All v2.x and v3.x release notes

**To user-docs/**:
- `docs/BENEFITS.md` → `docs/user-docs/explanation/benefits-of-chora-base.md`
- `docs/reference/writing-executable-howtos.md` → `docs/user-docs/how-to/write-executable-documentation.md`
- `docs/reference/ecosystem/` content needs evaluation:
  - `multi-repo-capability-evolution-to-w3.md` → user-docs/explanation/ or dev-docs/?
  - `ARCHITECTURE_CLARIFICATION.md` → user-docs/explanation/
  - `how-to-setup-mcp-ecosystem.md` → user-docs/how-to/

**Keep in reference/**:
- `docs/reference/skilled-awareness/` ← KEEP (correct location)

#### 1.3: Update All Cross-References

- Search for old paths, update to new paths
- Update INDEX.md references
- Update SAP awareness-guides that link to moved files
- Update README.md references

#### 1.4: Add SAP-000 to static-template

```bash
cp -r docs/reference/skilled-awareness/sap-framework \
      static-template/docs/skilled-awareness/sap-framework

cp SKILLED_AWARENESS_PACKAGE_PROTOCOL.md \
   static-template/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md

cp docs/reference/skilled-awareness/document-templates.md \
   static-template/docs/skilled-awareness/document-templates.md
```

#### 1.5: Create Domain README.md Files

**docs/dev-docs/README.md**:
```markdown
# Developer Documentation

Documentation for developers working ON this project.

## Purpose

This directory contains process documentation using Diátaxis for development:
- **how-to/** - Process guides (TDD, BDD, DDD workflows)
- **explanation/** - Conceptual deep-dives (design philosophy)
- **reference/** - Process specs (workflow definitions)
- **workflows/** - Complete development lifecycle processes
- **examples/** - Code walkthroughs and demonstrations
- **vision/** - Long-term capability roadmap
- **research/** - Technical investigations and learnings

## See Also

- [User Documentation](../user-docs/) - For product users
- [Project Documentation](../project-docs/) - Project lifecycle artifacts
- [SAP Framework](../skilled-awareness/) - Capability packages
```

**docs/project-docs/README.md**:
```markdown
# Project Documentation

Living documents generated/updated during project lifecycle.

## Purpose

This directory contains project management artifacts:
- **sprints/** - Sprint plans, retrospectives, velocity tracking
- **releases/** - Release notes, plans, post-mortems
- **metrics/** - Quality metrics, process metrics, ROI calculations
- **integration/** - Integration plans, coordination documents
- **inventory/** - Repository audits, coherence reports

## Characteristics

- **Living**: Updated throughout project lifecycle
- **Historical**: Permanent record of decisions and progress
- **Stakeholder-facing**: Often shared with PMs, leadership
```

**docs/user-docs/README.md**:
```markdown
# User Documentation

Documentation for users of the delivered product.

## Purpose

This directory contains end-user documentation using Diátaxis:
- **how-to/** - Task-oriented guides (how to integrate, configure, deploy)
- **explanation/** - Conceptual understanding (architecture, design decisions)
- **reference/** - Technical specifications (API docs, config reference)
- **tutorials/** - Learning-oriented lessons (getting started, first project)

## Audience

- End-users consuming the product
- Developers integrating with APIs
- Operators deploying the system
```

#### 1.6: Create Architecture Documentation

**docs/ARCHITECTURE.md**:
```markdown
# Chora-Base Documentation Architecture

## The 4-Domain Model

Chora-base uses a universal 4-domain documentation architecture:

1. **dev-docs/** - Developer process documentation
2. **project-docs/** - Project lifecycle artifacts
3. **user-docs/** - End-user product documentation
4. **skilled-awareness/** - SAP Framework (meta-layer)

[Full explanation of domains, Diátaxis mapping, examples]
```

### Validation

**Checklist**:
- [ ] All files moved to correct domains
- [ ] No broken links
- [ ] All domain README.md files created
- [ ] SAP-000 added to static-template/
- [ ] ARCHITECTURE.md created
- [ ] Git commit: "refactor(docs): Migrate to 4-domain architecture"

### Success Criteria

✅ Chora-base root follows universal 4-domain structure
✅ static-template/ matches chora-base structure
✅ All existing docs migrated (no content lost)
✅ Documentation explains the architecture
✅ All cross-references updated and valid

### Cleanup Tracking

As files are moved and reorganized in Wave 1, track items in `v4-cleanup-manifest.md`:

**Files to Delete**:
- Duplicate or obsolete documentation after reorganization
- Temporary files from inventory process (e.g., `docs/reference/chora-base/latest-conversation.md` 488 KB)

**Files to Archive**:
- Historical documentation that shouldn't be deleted but isn't actively needed

**References to Update**:
- All links pointing to old locations need to be updated
- SAP awareness-guides referencing moved files

### Timeline
**Duration**: 1-2 weeks
**Effort**: ~40-60 hours

---

## Wave 2: SAP Content Audit & Enhancement (v3.5.0)

**Goal**: Ensure all 14 SAPs properly reference the 4-domain structure and have complete content

### Current State

**SAP Coverage** (from inventory):
- SAP-000: SAP Framework - 22 files
- SAP-001: Inbox Protocol - 35 files
- SAP-002: Chora-Base - 55 files
- SAP-003: Project Bootstrap - 18 files
- SAP-004: Testing Framework - 12 files
- SAP-005: CI/CD Workflows - 14 files
- SAP-006: Quality Gates - 6 files
- SAP-007: Documentation Framework - 50 files
- SAP-008: Automation Scripts - 39 files
- SAP-009: Agent Awareness - 15 files
- SAP-010: Memory System - 14 files
- SAP-011: Docker Operations - 12 files
- SAP-012: Development Lifecycle - 11 files
- SAP-013: Metrics Tracking - 7 files

**Issues to address**:
- Not all SAPs reference actual implementation files
- Some SAPs missing dev-docs/ workflows
- Some SAPs missing user-docs/ documentation
- Cross-domain references need to be explicit

### Tasks

#### 2.1: Audit Each SAP for 4-Domain Content

For each SAP, create audit matrix:

| SAP | dev-docs/ | project-docs/ | user-docs/ | System (code/tests/scripts) |
|-----|-----------|---------------|------------|------------------------------|
| SAP-004 | ? | ? | ? | ? |
| ... | | | | |

**For each SAP, identify**:
- What dev-docs/ content exists or is needed?
- What project-docs/ artifacts are generated?
- What user-docs/ guides are needed?
- What system files (code, tests, scripts) does it cover?

#### 2.2: Create Missing Content

**Example: SAP-004 (Testing Framework)**

**Currently covered**:
- `static-template/tests/` (12 files) - System domain
- SAP-004 awareness-guide references testing

**Missing**:
- `dev-docs/workflows/TDD_WORKFLOW.md` - How to practice TDD
- `dev-docs/explanation/testing-philosophy.md` - Why test-first
- `user-docs/reference/testing-conventions.md` - Test structure spec

**Action**: Create these files and update SAP-004 awareness-guide to reference them.

Repeat for all 14 SAPs.

#### 2.3: Update SAP Awareness Guides

**Pattern for awareness-guide.md**:

```markdown
## Related Content

### Developer Documentation
- [TDD Workflow](../../../dev-docs/workflows/TDD_WORKFLOW.md) - Test-driven development process
- [Testing Philosophy](../../../dev-docs/explanation/testing-philosophy.md) - Why test-first

### User Documentation
- [Testing Reference](../../../user-docs/reference/testing-conventions.md) - Test structure spec
- [How to Write Tests](../../../user-docs/how-to/write-effective-tests.md) - Practical guide

### System Implementation
- `tests/` - Test suite structure
- `static-template/.github/workflows/test.yml` - CI test automation
- `scripts/test-runner.sh` - Test execution script

### Project Documentation
- No project-docs artifacts for this SAP (tests results stored elsewhere)
```

#### 2.4: Update document-templates.md

Add section:

```markdown
## SAP Content Across 4 Domains

When creating a new SAP, consider what belongs in each domain:

### dev-docs/ Content
- Workflow guides (how to USE this capability in development)
- Design philosophy (WHY we chose this approach)
- Examples (demonstrations of the capability)

### project-docs/ Content
- Adoption metrics (tracking who uses this SAP)
- Quality baselines (what "good" looks like)
- Integration plans (rolling out the SAP)

### user-docs/ Content
- How-to guides (user tasks enabled by this capability)
- Conceptual explanations (architecture, design decisions)
- Reference specs (APIs, configurations)

### System Content
- Implementation code (src/)
- Test suites (tests/)
- Automation scripts (scripts/)
- CI/CD configs (.github/)

### SAP Documentation (skilled-awareness/)
- capability-charter.md - High-level overview
- protocol-spec.md - Technical contracts
- awareness-guide.md - **REFERENCES content from all 4 domains**
- adoption-blueprint.md - Installation steps
- ledger.md - Adoption tracking
```

#### 2.5: Create Example SAP

Create a new example SAP (SAP-999) that demonstrates perfect 4-domain integration:

```
docs/skilled-awareness/example-capability/
├── capability-charter.md     ← Shows clear business value
├── protocol-spec.md          ← References code in src/
├── awareness-guide.md        ← References all 4 domains explicitly
├── adoption-blueprint.md     ← Clear installation steps
└── ledger.md                 ← Example adoption entries

With content in:
- dev-docs/workflows/example-workflow.md
- project-docs/metrics/example-adoption-metrics.md
- user-docs/how-to/use-example-capability.md
- src/example/ (if applicable)
```

### Validation

**For each SAP**:
- [ ] Audit matrix completed
- [ ] Missing content identified
- [ ] Content created or issue filed
- [ ] Awareness-guide updated with cross-domain references
- [ ] Links verified

### Success Criteria

✅ All 14 SAPs audited for 4-domain content
✅ No "orphan" references (all linked files exist)
✅ Awareness-guides explicitly reference implementation files
✅ Templates updated for future SAP creation
✅ Example SAP demonstrates best practices

### Cleanup Tracking

As SAPs are audited and enhanced, track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- SAP documentation that is redundant or obsolete
- Orphan references in awareness-guides to non-existent files

**Files to Archive**:
- Deprecated SAP versions or draft content that didn't make the cut

**References to Update**:
- SAP awareness-guides now referencing actual implementation files
- Cross-domain links in protocol-specs

### Timeline
**Duration**: 2-3 weeks
**Effort**: ~80-120 hours (varies by missing content)

---

## Wave 3: Extract MCP Capabilities into SAP-014 (v3.6.0)

**Goal**: Make chora-base language/framework agnostic while preserving MCP server development capabilities as an optional, installable SAP-014 package

### Current MCP-Specific Content to Package

Rather than **removing** MCP capabilities, Wave 3 **packages** them as SAP-014, making MCP server development an optional capability that projects can adopt via `python scripts/install-sap.py SAP-014`.

**Root files with MCP assumptions** (to generalize):
- `AGENTS.md` - References MCP server, FastMCP
- `CLAUDE.md` - MCP client configuration examples
- `README.md` - "MCP server template"

**blueprints/ (ALL MCP-specific)** (to move into SAP-014):
- `README.md.blueprint` - MCP server description
- `pyproject.toml.blueprint` - FastMCP dependency
- `server.py.blueprint` - MCP server implementation
- `mcp__init__.py.blueprint` - MCP-specific init

**static-template/ MCP content** (to move into SAP-014 templates):
- `src/__package_name__/mcp/` - MCP server code
- Various MCP references throughout

**Key Insight**: This content represents valuable MCP knowledge. By packaging as SAP-014, we **preserve** this expertise while making the base language-agnostic.

### Tasks

#### 3.1: Analyze MCP vs. Universal Content

Create audit document: `docs/project-docs/mcp-specificity-audit.md`

**Categories**:
1. **Pure MCP** - Only relevant for MCP servers (→ SAP-014)
2. **Python patterns** - Reusable for any Python project (→ Keep, generalize)
3. **Universal patterns** - Applicable to any language (→ Keep)

**Example audit**:
```markdown
| Content | Category | Action |
|---------|----------|--------|
| FastMCP import | Pure MCP | → SAP-014 |
| pytest patterns | Python | Keep, ensure language-neutral SAP-004 |
| Git workflows | Universal | Keep |
| MCP tool/resource patterns | Pure MCP | → SAP-014 |
```

#### 3.2: Create SAP-014: MCP Server Development (Central Task)

**Philosophical Shift**: SAP-014 is not just a "cleanup" - it's the **first technology-specific SAP** and a template for future framework SAPs (Django, FastAPI, React, etc.).

**New SAP structure**:
```
docs/skilled-awareness/mcp-server-development/
├── capability-charter.md      ← Business value: Why MCP servers?
├── protocol-spec.md           ← Technical contracts: FastMCP, tools, resources
├── awareness-guide.md         ← AI agent guidance: How to build MCP servers
├── adoption-blueprint.md      ← Installation: How to add MCP to any project
└── ledger.md                  ← Adoption tracking
```

**Content to **preserve** in SAP-014**:
- **Protocol Knowledge**: MCP specification, FastMCP vs. alternatives
- **Patterns**: Tool/resource/prompt implementation patterns
- **Configuration**: Claude Desktop, Cursor, other MCP clients
- **Testing**: MCP-specific test patterns (mocking tools/resources)
- **Deployment**: MCP server deployment strategies
- **Examples**: Complete MCP server implementations from blueprints/

**SAP-014 4-Domain Integration**:
- **dev-docs/workflows/**: `mcp-development-workflow.md` (how to build MCP servers)
- **user-docs/how-to/**: `implement-mcp-server.md`, `configure-mcp-client.md`
- **user-docs/reference/**: `mcp-protocol-spec.md`, `fastmcp-api-reference.md`
- **user-docs/explanation/**: `why-mcp-servers.md` (architecture, use cases)
- **System files**: `static-template/mcp-templates/` (templates for installation)

**What Makes SAP-014 Special**:
1. **First technology-specific SAP** - demonstrates capability portability
2. **Preserves expertise** - all MCP knowledge retained and enhanced
3. **Template for future SAPs** - shows how to package framework capabilities
4. **Validates v4.0 model** - proves "universal base + optional SAPs" works

#### 3.3: Generalize Root Documentation

**AGENTS.md** - Make language-agnostic:

**Before**:
```markdown
## Project Overview

**Project Name** is a Model Context Protocol (MCP) server that provides [capabilities].
```

**After**:
```markdown
## Project Overview

**Project Name** is a [project type] that provides [capabilities].

**Technology Stack**: [List languages, frameworks]
**Architecture**: [Describe architecture]

For MCP-specific projects, see [SAP-014: MCP Server Development](docs/skilled-awareness/mcp-server-development/)
```

**README.md** - Remove MCP assumptions:

**Before**:
```markdown
# Chora-Base v3.3.0

Production-ready MCP server template with...
```

**After**:
```markdown
# Chora-Base v4.0.0

Universal project foundation with SAP-based capability adoption.

Suitable for:
- Python applications (with appropriate SAPs)
- MCP servers (install SAP-014)
- Web services (install SAP-015)
- CLI tools (install SAP-016)
- Any project benefiting from structured capabilities
```

#### 3.4: Reorganize static-template/

**Current**:
```
static-template/
├── src/__package_name__/
│   ├── mcp/              ← MCP-specific
│   ├── memory/           ← Reusable Python pattern
│   └── utils/            ← Reusable Python pattern
```

**After**:
```
static-template/
├── src/__package_name__/  ← Minimal Python package structure
│   └── __init__.py
├── mcp-templates/         ← MCP-specific content (for SAP-014)
│   ├── server.py
│   ├── __init__.py
│   └── README.md
├── python-templates/      ← Python-specific patterns (for SAP-017)
│   ├── memory/
│   └── utils/
```

Or simpler: Keep everything, document that it's Python/MCP-focused and can be deleted if not needed.

#### 3.5: Delete blueprints/ and setup.py

**Files to delete**:
- `blueprints/` (entire directory - 11 files)
- `setup.py` (443 lines)
- `AGENT_SETUP_GUIDE.md` (describes setup.py)

**Replacement documentation**:
- `docs/user-docs/how-to/start-new-project-from-chora-base.md`
- `docs/user-docs/how-to/customize-project-content.md`
- `docs/user-docs/how-to/upgrade-from-upstream.md`

**New workflow** (documented in how-to guides):
```bash
# 1. Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git my-project
cd my-project

# 2. Remove chora-base-specific content
rm -rf .git
git init

# 3. Customize content
# - Update AGENTS.md, README.md with project specifics
# - Remove SAPs you don't need
# - Add project-specific SAPs

# 4. Install desired SAPs
python scripts/install-sap.py SAP-004  # Testing
python scripts/install-sap.py SAP-014  # MCP (if building MCP server)

# 5. Commit
git add .
git commit -m "Initial commit from chora-base v4.0.0"
```

### Validation

**Checklist**:
- [ ] MCP specificity audit complete
- [ ] SAP-014 created with all MCP content **preserved**
- [ ] SAP-014 installable via `install-sap.py SAP-014`
- [ ] Root docs generalized
- [ ] static-template/ reorganized (or documented)
- [ ] blueprints/ and setup.py deleted
- [ ] New how-to guides created
- [ ] Can create projects with/without MCP (via SAP installation choice)

### Success Criteria

✅ Root AGENTS.md/README.md are language-agnostic
✅ MCP capabilities **fully preserved and enhanced** in SAP-014
✅ SAP-014 installable into any chora-base project
✅ blueprints/ and setup.py removed (content moved to SAP-014)
✅ Clear "clone & customize" workflow documented
✅ Can create MCP servers by installing SAP-014
✅ Can create non-MCP projects by not installing SAP-014
✅ SAP-014 serves as template for future technology-specific SAPs

### Cleanup Tracking

Wave 3 creates significant cleanup items - track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- `blueprints/` directory (11 files) - No longer needed in clone model
- `setup.py` (443 lines) - Obsolete generation script
- `AGENT_SETUP_GUIDE.md` - Describes obsolete workflow
- MCP-specific references in root AGENTS.md, README.md, CLAUDE.md

**Files to Archive**:
- Original blueprint templates (for historical reference before deleting)
- setup.py (for reference if needed)

**Files to Move** (packaging, not deleting):
- MCP-specific content → `docs/skilled-awareness/mcp-server-development/` (SAP-014)
- MCP templates from blueprints/ → SAP-014 templates directory
- MCP implementation code → SAP-014 system files for installation

**References to Update**:
- Root docs (README, AGENTS, CLAUDE) - remove MCP assumptions
- SAP-003 references to blueprints/ and setup.py
- Update to new clone & customize workflow

**Git History**:
- Consider: Should we preserve blueprint history before deletion?
- Decision: Tag current state as v3.x-final-with-blueprints

### Parallel Track: chora-compose Ecosystem Integration (SAP-017, SAP-018)

**Added**: 2025-10-28 (via inbox coordination protocol)

While executing Wave 3 MCP extraction, we can also create chora-compose SAPs in parallel:

**SAP-017: chora-compose-integration**
- How to adopt chora-compose in your repo
- Installation methods (pip, MCP, CLI)
- Role-based usage patterns
- Decision guide: when to use chora-compose
- **Effort**: ~8-12 hours

**SAP-018: chora-compose-meta**
- Complete protocol specification (mirrors SAP-002 pattern)
- All 17 MCP tools + 5 resource families
- 4 access modalities (pip, SAP, MCP, API)
- Position in AI tooling ecosystem
- **Effort**: ~12-16 hours

**Strategic Value**:
- Demonstrates ecosystem SAPs (how one chora tool documents another)
- First cross-repo capability coordination via inbox protocol (coord-001)
- Shows 4 access modalities pattern
- Enables ecosystem repos to discover and adopt chora-compose

**SAP ID Allocation**:
- SAP-014: MCP Server Development (this Wave)
- SAP-015: Django Development (future, v4.2.0)
- SAP-016: Link Validation (exists, Wave 2)
- **SAP-017**: chora-compose-integration (this Wave)
- **SAP-018**: chora-compose-meta (this Wave)
- SAP-019+: React, Rust, etc. (future)

### Timeline
**Duration**: 3-4 weeks (extended from 2-3 weeks)
**Effort**: ~80-108 hours total
- MCP extraction (SAP-014): ~60-80 hours
- chora-compose SAPs (SAP-017, 018): ~20-28 hours

**Parallelization**: Both tracks can be executed simultaneously

---

## Wave 4: Clone & Merge Model (v3.7.0)

**Goal**: Enable upstream structural updates via git merge

### Concept

**Challenge**: How to merge structural improvements from chora-base without overwriting project-specific content?

**Solution**: Clear boundaries between structure (mergeable) and content (project-specific).

### Tasks

#### 4.1: Define Structure vs. Content Boundaries

Create `.chorabase` metadata file:

```yaml
# .chorabase - Chora-Base metadata
version: "4.0.0"
structural_version: "4.0.0"

# Files that are pure structure (always merge from upstream)
structure_only:
  - SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
  - docs/skilled-awareness/sap-framework/**
  - docs/skilled-awareness/document-templates.md
  - .chorabase

# Files that are pure content (never merge from upstream)
content_only:
  - src/**
  - tests/**
  - docs/skilled-awareness/[project-specific-saps]/**
  - .git/**

# Files that are hybrid (manual merge required)
hybrid:
  - AGENTS.md:
      structure:
        - "## Project Overview" section header
        - "## Development Process" section header
      content:
        - Text within sections
  - README.md:
      structure:
        - Section headers
        - Standard badges
      content:
        - Project name, description
        - Feature list
  - docs/skilled-awareness/INDEX.md:
      structure:
        - Table format, column headers
      content:
        - SAP list entries
```

#### 4.2: Create Merge Tooling

**Script**: `scripts/merge-upstream-structure.sh`

```bash
#!/bin/bash
# Merge structural updates from chora-base upstream

# 1. Check if upstream exists
if ! git remote get-url chora-base 2>/dev/null; then
    echo "Adding chora-base upstream..."
    git remote add chora-base https://github.com/liminalcommons/chora-base.git
fi

# 2. Fetch latest
git fetch chora-base

# 3. Read .chorabase for structure-only files
structure_files=$(yq '.structure_only[]' .chorabase)

# 4. Merge structure-only files
for file in $structure_files; do
    git checkout chora-base/main -- "$file"
done

# 5. Report hybrid files that need manual review
echo "Hybrid files requiring manual merge:"
yq '.hybrid | keys[]' .chorabase

# 6. Instructions for user
echo ""
echo "Next steps:"
echo "1. Review hybrid files for conflicts"
echo "2. git add <resolved-files>"
echo "3. git commit -m 'chore: Merge structural updates from chora-base v4.x.x'"
```

#### 4.3: Document Merge Workflows

**File**: `docs/user-docs/how-to/upgrade-structure-from-upstream.md`

```markdown
# How to Upgrade Structure from Upstream

## When to Upgrade

- Chora-base releases new structural improvements
- New SAP framework features
- Bug fixes in structural files
- Documentation architecture updates

## Upgrade Process

### 1. Check Your Version

```bash
cat .chorabase | grep version
# version: "4.0.0"
```

### 2. Check Upstream Version

```bash
git ls-remote https://github.com/liminalcommons/chora-base.git HEAD
# Compare with your structural_version
```

### 3. Run Merge Script

```bash
./scripts/merge-upstream-structure.sh
```

### 4. Review Changes

```bash
git status
# Shows which files were updated
```

### 5. Handle Hybrid Files

For AGENTS.md, README.md, etc.:
- Review diffs carefully
- Keep your content, merge structural changes
- Use `git checkout --patch` for fine-grained control

### 6. Test

- Verify all cross-references still work
- Run any validation scripts
- Check documentation builds

### 7. Commit

```bash
git commit -m "chore: Merge structural updates from chora-base v4.1.0"
```

## Rollback

If merge causes issues:

```bash
git reset --hard HEAD~1
# Or restore specific files
git checkout HEAD~1 -- path/to/file
```
```

#### 4.4: Test with Example Project

**Create test project**:
1. Clone chora-base v4.0.0
2. Customize content (create project-specific SAP, modify AGENTS.md, etc.)
3. Commit as "my-project"
4. Make a structural change in chora-base (e.g., add new section to AGENTS.md template)
5. In "my-project", run merge script
6. Verify: Structural change merged, custom content preserved

### Validation

**Test cases**:
- [ ] Structure-only files merge cleanly
- [ ] Content-only files never touched by merge
- [ ] Hybrid files show clear conflicts
- [ ] Merge script handles errors gracefully
- [ ] Documentation clear and complete

### Success Criteria

✅ `.chorabase` metadata defines boundaries
✅ Merge script successfully merges structure-only files
✅ Hybrid files have clear merge strategy
✅ Documentation explains the model with examples
✅ Example project demonstrates successful upgrade

### Cleanup Tracking

Wave 4 primarily adds new capabilities, minimal cleanup - track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- None expected

**Files to Archive**:
- None expected

**Files to Move**:
- None expected

**References to Update**:
- Update how-to guides to reference .chorabase metadata
- Update documentation to explain merge workflow

**Git History**:
- None (Wave 4 is additive)

### Timeline
**Duration**: 2-3 weeks
**Effort**: ~60-80 hours

---

## Wave 5: SAP Installation Tooling (v3.8.0)

**Goal**: Make SAP adoption seamless for Claude and humans

### Tasks

#### 5.1: Create SAP Catalog

**File**: `sap-catalog.json`

```json
{
  "version": "4.0.0",
  "updated": "2025-10-28",
  "saps": [
    {
      "id": "SAP-000",
      "name": "SAP Framework",
      "status": "active",
      "version": "1.0.0",
      "included_by_default": true,
      "size_kb": 125,
      "description": "Core SAP framework and protocols",
      "dependencies": [],
      "tags": ["meta", "required"],
      "author": "chora-base",
      "location": "docs/skilled-awareness/sap-framework"
    },
    {
      "id": "SAP-004",
      "name": "Testing Framework",
      "status": "active",
      "version": "1.0.0",
      "included_by_default": false,
      "size_kb": 89,
      "description": "pytest-based testing with 95%+ coverage patterns",
      "dependencies": ["SAP-000"],
      "tags": ["testing", "quality", "python"],
      "author": "chora-base",
      "location": "docs/skilled-awareness/testing-framework",
      "system_files": [
        "static-template/tests/",
        "static-template/.github/workflows/test.yml"
      ]
    },
    // ... all 14+ SAPs
  ]
}
```

**Script**: `scripts/sap-catalog.py` (query tool)

```python
#!/usr/bin/env python3
"""SAP Catalog Query Tool"""

def list_saps():
    """List all available SAPs"""

def search_saps(query: str):
    """Search SAPs by keyword"""

def get_sap_info(sap_id: str):
    """Get detailed info about a SAP"""

def check_dependencies(sap_id: str):
    """Show dependency tree"""
```

#### 5.2: Create SAP Installation Script

**File**: `scripts/install-sap.py`

```python
#!/usr/bin/env python3
"""
Install a SAP from chora-base into current project.

Usage:
    python scripts/install-sap.py SAP-004
    python scripts/install-sap.py SAP-004 --source /path/to/chora-base
    python scripts/install-sap.py --list
"""

import argparse
import json
import shutil
from pathlib import Path

def install_sap(sap_id: str, source_dir: Path, target_dir: Path):
    """
    Install a SAP into the current project.

    Steps:
    1. Validate SAP exists in source
    2. Check dependencies (install if missing)
    3. Copy SAP directory
    4. Copy system files (if any)
    5. Update INDEX.md
    6. Update ledger.md
    7. Run validation
    8. Commit (optional)
    """

    # 1. Load catalog
    catalog = json.load(open(source_dir / "sap-catalog.json"))
    sap = next((s for s in catalog["saps"] if s["id"] == sap_id), None)

    if not sap:
        print(f"❌ SAP {sap_id} not found in catalog")
        return False

    print(f"Installing {sap['name']} ({sap_id})...")

    # 2. Check dependencies
    for dep_id in sap.get("dependencies", []):
        if not check_sap_installed(dep_id, target_dir):
            print(f"  📦 Installing dependency: {dep_id}")
            install_sap(dep_id, source_dir, target_dir)

    # 3. Copy SAP directory
    sap_src = source_dir / sap["location"]
    sap_dest = target_dir / sap["location"]

    if sap_dest.exists():
        print(f"⚠️  {sap_id} already installed. Skipping.")
        return True

    shutil.copytree(sap_src, sap_dest)
    print(f"  ✅ Copied SAP directory")

    # 4. Copy system files (if any)
    for sys_file in sap.get("system_files", []):
        src = source_dir / sys_file
        dest = target_dir / sys_file
        if src.exists():
            shutil.copytree(src, dest)
            print(f"  ✅ Copied {sys_file}")

    # 5. Update INDEX.md
    update_index(sap, target_dir)
    print(f"  ✅ Updated INDEX.md")

    # 6. Update ledger
    update_ledger(sap, target_dir)
    print(f"  ✅ Updated ledger")

    # 7. Validate
    if validate_installation(sap_id, target_dir):
        print(f"✅ {sap['name']} installed successfully!")
        return True
    else:
        print(f"❌ Installation validation failed")
        return False

def validate_installation(sap_id: str, target_dir: Path):
    """Validate that all required files exist."""
    sap_dir = target_dir / f"docs/skilled-awareness/{sap_id}"

    required_files = [
        "capability-charter.md",
        "protocol-spec.md",
        "awareness-guide.md",
        "adoption-blueprint.md",
        "ledger.md"
    ]

    for file in required_files:
        if not (sap_dir / file).exists():
            print(f"  ❌ Missing: {file}")
            return False

    return True

# ... implementation ...
```

#### 5.3: Update SAP Awareness Guides

Add installation instructions to every SAP's awareness-guide.md:

```markdown
## Installation

### Quick Install

```bash
python scripts/install-sap.py SAP-004
```

### Manual Install

If you don't have install-sap.py:

1. Copy SAP directory:
   ```bash
   cp -r /path/to/chora-base/docs/skilled-awareness/testing-framework \
         docs/skilled-awareness/
   ```

2. Copy system files:
   ```bash
   cp -r /path/to/chora-base/static-template/tests tests/
   ```

3. Update INDEX.md (add SAP-004 entry)

4. Update ledger.md (record your adoption)

### Validation

```bash
# Verify all 5 artifacts exist
ls docs/skilled-awareness/testing-framework/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md

# Verify system files
ls tests/
```
```

#### 5.4: Dependency Resolution

**Catalog dependencies** (examples):
- SAP-012 (Development Lifecycle) depends on:
  - SAP-004 (Testing Framework) - TDD workflow needs tests
  - SAP-006 (Quality Gates) - BDD needs pre-commit hooks

- SAP-011 (Docker Operations) depends on:
  - SAP-008 (Automation Scripts) - Uses build scripts

**Installation script auto-installs dependencies**:
```bash
$ python scripts/install-sap.py SAP-012

Installing Development Lifecycle (SAP-012)...
  📦 Installing dependency: SAP-004
  ✅ Testing Framework installed
  📦 Installing dependency: SAP-006
  ✅ Quality Gates installed
  ✅ Copied SAP directory
  ✅ Updated INDEX.md
  ✅ Updated ledger
✅ Development Lifecycle installed successfully!
```

### Validation

**Test scenarios**:
- [ ] Install SAP with no dependencies
- [ ] Install SAP with dependencies (auto-installs)
- [ ] Install already-installed SAP (skips gracefully)
- [ ] Install with missing source path (clear error)
- [ ] Validation catches missing files
- [ ] INDEX.md updated correctly
- [ ] Ledger.md updated correctly

### Success Criteria

✅ `sap-catalog.json` complete for all SAPs
✅ `install-sap.py` works for any SAP
✅ Dependencies automatically resolved
✅ Claude can install SAPs with single command
✅ Clear error messages and validation
✅ Rollback on failure (nice-to-have)

### Cleanup Tracking

Wave 5 is primarily additive, minimal cleanup - track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- None expected (all new tooling)

**Files to Archive**:
- None expected

**Files to Move**:
- None expected

**References to Update**:
- SAP awareness-guides now reference install-sap.py
- SAP adoption-blueprints updated with installation instructions

**Git History**:
- None (Wave 5 is additive)

### Timeline
**Duration**: 2-3 weeks
**Effort**: ~60-80 hours

---

## Wave 6: Multi-Repo Coordination (v3.9.0 - OPTIONAL)

**Goal**: Enable SAP discovery and sharing across organization repos

**Note**: This wave is optional for v4.0.0 and can be deferred to v4.1.0

### Tasks (High-Level)

#### 6.1: SAP Registry Protocol
- Define JSON schema for SAP metadata
- Create discovery API (search SAPs across repos)
- Document how to publish SAPs to org registry

#### 6.2: Enhanced Inbox Integration
- SAP adoption requests via inbox protocol
- SAP upgrade notifications
- Cross-repo capability coordination

#### 6.3: SAP Versioning
- Semantic versioning for each SAP
- Upgrade blueprints (v1.0 → v2.0)
- Backward compatibility tracking
- Migration guides

#### 6.4: External SAP Installation
```bash
# Install SAP from another org repo
python scripts/install-sap.py SAP-XYZ \
  --source https://github.com/org/other-project
```

### Cleanup Tracking

If Wave 6 is included, track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- None expected (additive wave)

**Files to Archive**:
- None expected

**Files to Move**:
- None expected

**References to Update**:
- SAP-001 (Inbox) enhancements for SAP coordination
- Documentation on multi-repo SAP discovery

**Git History**:
- None (Wave 6 is additive)

### Timeline
**Duration**: 3-4 weeks (if included)
**Effort**: ~100+ hours

**Recommendation**: Defer to v4.1.0 unless multi-repo coordination is immediate need.

---

## Wave 7: Testing, Validation & Migration (v3.10.0)

**Goal**: Ensure v4.0 quality and smooth migration from v3.x

### Tasks

#### 7.1: Comprehensive Test Suite

**Test areas**:
1. **SAP Installation** (`test_install_sap.py`)
   - Install each SAP
   - Verify all files copied
   - Check INDEX.md updated
   - Validate ledger updated

2. **Merge Tooling** (`test_merge_upstream.py`)
   - Test structure-only merges
   - Test content preservation
   - Test hybrid file handling
   - Test conflict resolution

3. **Documentation** (`test_documentation.py`)
   - Validate all cross-references
   - Check broken links
   - Verify all SAP awareness-guides reference actual files
   - Confirm 4-domain consistency

4. **Integration** (`test_integration.py`)
   - Clone chora-base
   - Customize content
   - Install SAPs
   - Merge upstream update
   - End-to-end workflow

**Target**: 95%+ test coverage of scripts and workflows

#### 7.2: Documentation Audit

**Checklist**:
- [ ] All cross-references valid
- [ ] All code examples tested
- [ ] All paths correct after Wave 1 restructuring
- [ ] All SAP adoption blueprints complete
- [ ] All how-to guides tested with Claude
- [ ] ARCHITECTURE.md comprehensive
- [ ] 4-domain model clearly explained

**Tools**:
- Link checker script
- SAP completeness validator
- Cross-reference mapper

#### 7.3: User Testing

**Test with actual Claude sessions**:
1. **New project creation**: "Create new project using chora-base"
   - Can Claude follow docs to clone & customize?
   - Any confusion points?
   - Time to working project?

2. **SAP installation**: "Install testing framework SAP"
   - Can Claude find and execute install-sap.py?
   - Clear success/failure feedback?
   - Dependencies work correctly?

3. **Upgrade workflow**: "Merge upstream structural updates"
   - Can Claude understand merge-upstream-structure.sh?
   - Hybrid files handled correctly?
   - Clear documentation?

**Collect feedback, iterate on docs/tooling**

#### 7.4: Migration Guide

**File**: `docs/user-docs/how-to/migrate-from-v3-to-v4.md`

```markdown
# Migrating from Chora-Base v3.x to v4.0

## Overview

v4.0 introduces breaking changes to enable the clone & merge model.

**Major changes**:
- Documentation restructured to 4-domain architecture
- blueprints/ and setup.py removed
- MCP-specific content moved to SAP-014
- New SAP installation tooling
- Upstream merge capability

## Migration Options

### Option A: Fresh Start (Recommended for new projects)
1. Create new repo by cloning chora-base v4.0
2. Copy your `src/` code into new structure
3. Copy your tests into new structure
4. Install needed SAPs
5. Commit

### Option B: In-Place Migration (For existing projects)
1. Run migration script: `./scripts/migrate-v3-to-v4.sh`
2. Review changes
3. Test
4. Commit

### Option C: Gradual Migration
1. Keep v3.x project as-is
2. Manually adopt v4.0 patterns incrementally
3. Restructure docs/ over time

## Automated Migration Script

```bash
./scripts/migrate-v3-to-v4.sh
```

**What it does**:
1. Backs up current project
2. Restructures docs/ to 4-domain architecture
3. Adds .chorabase metadata file
4. Updates SAP references
5. Adds install-sap.py script
6. Creates migration report

## Manual Steps

After running migration script:

1. Review moved files
2. Update any custom scripts that reference old paths
3. Test build/test/deploy processes
4. Update CI/CD if paths changed
5. Commit: `git commit -m "chore: Migrate to chora-base v4.0"`

## Breaking Changes

- `blueprints/` no longer exists (if you customized these, port to SAPs)
- `setup.py` no longer exists (use clone workflow)
- `docs/` structure changed (links may break)
- Some SAP files moved (check INDEX.md)

## Rollback

If migration fails:

```bash
./scripts/migrate-v3-to-v4.sh --rollback
```

Or restore from backup:
```bash
mv .chora-backup-YYYYMMDD-HHMMSS project/
```
```

**Migration script**: `scripts/migrate-v3-to-v4.sh`

```bash
#!/bin/bash
# Migrate v3.x project to v4.0 structure

set -e

echo "Chora-Base v3 → v4 Migration"
echo "=============================="
echo ""

# 1. Backup
backup_dir=".chora-backup-$(date +%Y%m%d-%H%M%S)"
echo "Creating backup in $backup_dir..."
cp -r . "$backup_dir"
echo "✅ Backup created"
echo ""

# 2. Check if this is a chora-base project
if [ ! -f "AGENTS.md" ] || [ ! -f "SKILLED_AWARENESS_PACKAGE_PROTOCOL.md" ]; then
    echo "❌ This doesn't look like a chora-base v3.x project"
    echo "Migration aborted."
    exit 1
fi

echo "Detected chora-base v3.x project"
echo ""

# 3. Restructure docs/
echo "Restructuring documentation..."

mkdir -p docs/dev-docs
mkdir -p docs/project-docs/{integration,inventory,releases}
mkdir -p docs/user-docs/{how-to,explanation,reference,tutorials}

# Move files (if they exist)
[ -d "docs/research" ] && mv docs/research docs/dev-docs/ || true
[ -f "docs/DOCUMENTATION_PLAN.md" ] && mv docs/DOCUMENTATION_PLAN.md docs/project-docs/ || true
[ -d "docs/integration" ] && mv docs/integration docs/project-docs/ || true
[ -d "docs/inventory" ] && mv docs/inventory docs/project-docs/ || true
[ -d "docs/releases" ] && mv docs/releases docs/project-docs/ || true
[ -f "docs/BENEFITS.md" ] && mv docs/BENEFITS.md docs/user-docs/explanation/benefits-of-chora-base.md || true

echo "✅ Documentation restructured"
echo ""

# 4. Add .chorabase metadata
echo "Creating .chorabase metadata..."
cat > .chorabase <<'EOF'
# .chorabase - Chora-Base metadata
version: "4.0.0"
structural_version: "4.0.0"
migrated_from: "3.3.0"
migration_date: "$(date -I)"

# [Rest of .chorabase content]
EOF
echo "✅ Metadata created"
echo ""

# 5. Download v4.0 scripts
echo "Adding v4.0 scripts..."
curl -sL https://raw.githubusercontent.com/liminalcommons/chora-base/v4.0.0/scripts/install-sap.py -o scripts/install-sap.py
curl -sL https://raw.githubusercontent.com/liminalcommons/chora-base/v4.0.0/scripts/merge-upstream-structure.sh -o scripts/merge-upstream-structure.sh
chmod +x scripts/*.sh
echo "✅ Scripts added"
echo ""

# 6. Update INDEX.md references (if needed)
# ... implementation ...

# 7. Generate migration report
cat > migration-report.md <<'EOF'
# Migration Report: v3.x → v4.0

**Date**: $(date -I)
**Backup**: $backup_dir

## Changes Made

- Restructured docs/ to 4-domain architecture
- Added .chorabase metadata
- Added v4.0 installation scripts
- [List other changes]

## Next Steps

1. Review moved files in docs/
2. Update any scripts referencing old paths
3. Run tests: `pytest tests/`
4. Commit changes
5. Optional: Set up upstream remote for future merges

## Rollback

If needed, restore from backup:
```bash
rm -rf *
cp -r $backup_dir/* .
```
EOF

echo "✅ Migration complete!"
echo ""
echo "Migration report: migration-report.md"
echo "Backup location: $backup_dir"
echo ""
echo "Next steps:"
echo "1. Review migration-report.md"
echo "2. Test your project"
echo "3. Commit: git commit -m 'chore: Migrate to chora-base v4.0'"
```

### Validation

**Testing matrix**:
- [ ] All scripts tested (install-sap, merge-upstream, etc.)
- [ ] All how-to guides tested with Claude
- [ ] All SAP adoption blueprints tested
- [ ] Migration script tested on v3.x projects
- [ ] Documentation audit complete (no broken links)
- [ ] User testing with 3+ real Claude sessions

### Success Criteria

✅ 95%+ automated test coverage
✅ All documentation validated (links, cross-refs, examples)
✅ User testing successful (Claude can complete workflows)
✅ Migration script works for v3.x projects
✅ Migration guide complete and tested
✅ v4.0.0 ready for release!

### Cleanup Tracking

Wave 7 validates and prepares for cleanup - track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- Test artifacts and temporary validation files after Wave 7 complete

**Files to Archive**:
- Migration logs and reports (archive for reference)

**Files to Move**:
- Migration script to appropriate location (scripts/ or docs/)

**References to Update**:
- Final validation of all cross-references before release
- Ensure no broken links remain

**Git History**:
- Prepare final v4.0.0 tag
- Clean commit history for release

### Timeline
**Duration**: 2-3 weeks
**Effort**: ~60-80 hours

---

## Wave 8: Reconciliation & Cleanup (v4.0.0-rc1)

**Goal**: Execute cleanup manifest, finalize v4.0 release

### Concept

Wave 8 is NOT discovery - it's execution. By this point, the `v4-cleanup-manifest.md` has been populated throughout Waves 1-7. Now we simply execute the manifest.

### Tasks

#### 8.1: Review Cleanup Manifest

Read `v4-cleanup-manifest.md` in its entirety:
- Verify all entries are still valid
- Remove any items that were already handled
- Add any late discoveries
- Prioritize: Delete > Archive > Move

#### 8.2: Execute Deletions

For each file in "Files to Delete" table:
```bash
# 1. Verify file is truly obsolete
# 2. Check no active references exist
# 3. Delete
rm -f <file>

# 4. Update manifest: Mark as DONE
```

**Expected deletions** (from Wave 3):
- `blueprints/` directory (11 files)
- `setup.py`
- `AGENT_SETUP_GUIDE.md`
- Temporary files from Wave 1 reorganization

#### 8.3: Execute Archives

For each file in "Files to Archive" table:
```bash
# 1. Create archive location if needed
mkdir -p .archive/v3-final/

# 2. Move file to archive
mv <file> .archive/v3-final/

# 3. Update manifest: Mark as DONE
```

#### 8.4: Execute Moves/Renames

For each file in "Files to Move" table:
```bash
# 1. Verify destination doesn't exist
# 2. Move file
mv <from> <to>

# 3. Update manifest: Mark as DONE
```

#### 8.5: Update All References

For each item in "References to Update" table:
```bash
# 1. Update the reference
# 2. Verify link works
# 3. Update manifest: Mark as DONE
```

#### 8.6: Final Validation

Run comprehensive validation:
```bash
# 1. Run inventory to verify 100% coherence maintained
python scripts/inventory-chora-base.py

# 2. Run link checker
python scripts/validate-links.py

# 3. Verify all SAP artifacts complete
python scripts/validate-saps.py

# 4. Run full test suite
pytest tests/

# 5. Build documentation
# (if applicable)
```

#### 8.7: Final Git Cleanup

```bash
# 1. Review git status
git status

# 2. Commit cleanup
git add .
git commit -m "chore(v4.0): Execute cleanup manifest - finalize v4.0 structure

- Deleted obsolete files (blueprints/, setup.py, etc.)
- Archived v3.x reference files
- Moved files to final locations
- Updated all cross-references
- Validated 100% coherence

Closes v4-cleanup-manifest.md"

# 3. Tag release candidate
git tag -a v4.0.0-rc1 -m "Release Candidate 1 for v4.0.0"
```

#### 8.8: Generate Release Report

Create `docs/project-docs/releases/v4.0.0-release-report.md`:
```markdown
# v4.0.0 Release Report

## Cleanup Summary

**Files deleted**: X
**Files archived**: Y
**Files moved**: Z
**References updated**: N

## Before/After Structure

### v3.3.0 (Before)
- [Structure snapshot]

### v4.0.0 (After)
- [New structure]

## What Changed

[Summary from cleanup manifest]

## Validation Results

- ✅ 100% SAP coverage maintained
- ✅ All links validated
- ✅ All tests passing
- ✅ Documentation complete

## Release Artifacts

- Tag: v4.0.0-rc1
- Changelog: CHANGELOG.md
- Migration guide: docs/user-docs/how-to/migrate-from-v3-to-v4.md
```

### Validation

**Checklist**:
- [ ] All manifest items executed
- [ ] Inventory shows 100% coherence
- [ ] Link validation passes
- [ ] Tests pass
- [ ] Documentation builds
- [ ] No broken references
- [ ] Git history clean
- [ ] Release report complete

### Success Criteria

✅ Cleanup manifest fully executed
✅ All obsolete files removed
✅ Archive created with v3.x reference files
✅ 100% coherence maintained
✅ All validation passes
✅ v4.0.0-rc1 tagged and ready for release

### Timeline
**Duration**: 1 week
**Effort**: ~20-30 hours

**Note**: This wave should be fast because all discovery happened in Waves 1-7. Wave 8 is pure execution.

---

## v4.0.0 Release: The Universal Project Foundation

### Release Date
**Target**: Q1 2026 (March 2026)

### What v4.0.0 Delivers

**For Claude (LLM Agents)**:
- ✅ Single, clear mental model: "Clone, customize content, adopt SAPs"
- ✅ One-command SAP installation
- ✅ Clear workflows documented in every SAP
- ✅ Upstream structural updates via git merge
- ✅ No ambiguity: Everything documented, nothing automated/hidden

**For Human Developers**:
- ✅ Universal 4-domain documentation architecture
- ✅ Consistent structure across all projects in organization
- ✅ Portable capability packages (SAPs)
- ✅ Upgradeable foundation (merge from upstream)
- ✅ Language/framework agnostic base

**For Organizations**:
- ✅ Shared SAP framework across all repos
- ✅ Cross-repo capability discovery (with Wave 6)
- ✅ Consistent project patterns
- ✅ Knowledge compounding (SAPs as organizational memory)
- ✅ Reduced onboarding time (familiar structure everywhere)

**For Technology Ecosystems**:
- ✅ **SAP-014: MCP Server Development** - First technology-specific SAP
- ✅ MCP expertise preserved and packaged for reuse
- ✅ Template for future framework SAPs (Django, FastAPI, React)
- ✅ Proves SAP portability model works for specialized technologies

### Breaking Changes from v3.x

#### Removed
1. **blueprints/** directory (11 template files)
   - **Reason**: Incompatible with clone & merge model
   - **Migration**: MCP content **preserved** in SAP-014, install via `install-sap.py SAP-014`

2. **setup.py** automated generation script
   - **Reason**: Projects now created by cloning, not generating
   - **Migration**: Use new clone & customize workflow

3. **AGENT_SETUP_GUIDE.md**
   - **Reason**: Describes obsolete setup.py workflow
   - **Migration**: Replaced by how-to guides in user-docs/

4. **MCP-specific root documentation**
   - **Reason**: Base should be framework-agnostic
   - **Migration**: MCP content **packaged and enhanced** in SAP-014, available as optional capability

#### Moved
1. **docs/** restructured
   - `docs/integration/` → `docs/project-docs/integration/`
   - `docs/inventory/` → `docs/project-docs/inventory/`
   - `docs/releases/` → `docs/project-docs/releases/`
   - `docs/research/` → `docs/dev-docs/research/`
   - **Migration**: Automated by migration script

2. **SAP files updated**
   - All 14 SAPs enhanced with 4-domain references
   - Awareness-guides now reference actual implementation files
   - **Migration**: No action needed (documentation improvements)

#### Added
1. **.chorabase** metadata file
   - Defines structure vs. content boundaries
   - Enables upstream merge capability

2. **SAP installation tooling**
   - `scripts/install-sap.py` - Install SAPs
   - `scripts/merge-upstream-structure.sh` - Merge updates
   - `sap-catalog.json` - SAP registry

3. **Comprehensive documentation**
   - `docs/ARCHITECTURE.md` - 4-domain model explained
   - 3 domain README files
   - Multiple how-to guides for v4.0 workflows

### Migration Path

**Three options**:

1. **Fresh Start** (recommended for new projects)
   - Clone chora-base v4.0
   - Copy your code into new structure
   - Install needed SAPs

2. **Automated Migration** (for existing v3.x projects)
   - Run `./scripts/migrate-v3-to-v4.sh`
   - Review changes
   - Test and commit

3. **Gradual Migration** (for complex projects)
   - Keep v3.x, adopt v4.0 patterns incrementally
   - Migrate docs/ structure first
   - Add SAP tooling
   - Eventually restructure fully

### Backward Compatibility

**v4.0 is NOT backward compatible with v3.x**

However:
- Migration script automates most changes
- All v3.x content preserved (just reorganized)
- SAP framework remains compatible
- Can run v3.x and v4.0 projects side-by-side

### Release Artifacts

1. **Git tag**: `v4.0.0`
2. **Release notes**: Detailed changelog
3. **Migration guide**: `docs/user-docs/how-to/migrate-from-v3-to-v4.md`
4. **Migration script**: `scripts/migrate-v3-to-v4.sh`
5. **Documentation**: Complete v4.0 docs in repo

### Success Metrics

**v4.0.0 is successful if**:

1. **Claude Ergonomics**: ⏱️ <5 minutes
   - Claude can start new project from chora-base with zero errors

2. **SAP Adoption**: ⏱️ <2 minutes
   - Installing a SAP always works, includes dependencies

3. **Upgrades Work**: ✅ No manual intervention
   - Can merge upstream structural changes without conflicts

4. **Documentation Quality**: 🔗 100% valid links
   - All cross-references work, 4-domain architecture clear

5. **Adoption**: 📈 5+ projects
   - 5+ external projects successfully using chora-base v4.0

6. **Community**: 👥 Positive feedback
   - Users report improved ergonomics vs. v3.x

---

## Overall Timeline

### Detailed Wave Timeline

| Wave | Version | Duration | Effort | Deliverables |
|------|---------|----------|--------|--------------|
| Wave 1 | v3.4.0 | 1-2 weeks | 40-60h | 4-domain docs structure |
| Wave 2 | v3.5.0 | 2-3 weeks | 80-120h | SAP content audit & enhancement |
| Wave 3 | v3.6.0 | 3-4 weeks | 80-108h | MCP extraction (SAP-014) + chora-compose SAPs (SAP-017/018) |
| Wave 4 | v3.7.0 | 2-3 weeks | 60-80h | Clone & merge model |
| Wave 5 | v3.8.0 | 2-3 weeks | 60-80h | SAP installation tooling |
| Wave 6 | v3.9.0 | 3-4 weeks | 100+h | Multi-repo (OPTIONAL - defer to v4.1?) |
| Wave 7 | v3.10.0 | 2-3 weeks | 60-80h | Testing & validation |
| Wave 8 | v4.0.0-rc1 | 1 week | 20-30h | Cleanup execution & release prep |

### Aggressive Timeline (No Wave 6)
**Total**: 14-19 weeks (~3.5-5 months)
- Waves 1-2: November-December 2025
- Waves 3-4: January 2026
- Waves 5,7: February-March 2026
- Wave 8: March 2026
- **Release**: March 2026

### Conservative Timeline (With Wave 6)
**Total**: 18-25 weeks (~4.5-6.5 months)
- Waves 1-2: November-December 2025
- Waves 3-4: January 2026
- Waves 5-6: February-March 2026
- Wave 7: April 2026
- Wave 8: April 2026
- **Release**: April 2026

### Recommendations

1. **Start Immediately with Wave 1** (documentation architecture foundation)
2. **Wave 1 by end of November** (foundation for everything else)
3. **Defer Wave 6 to v4.1.0** (multi-repo is nice-to-have, not critical for v4.0)
4. **Track cleanup in manifest throughout Waves 1-7** (don't discover at the end)
5. **Target March 2026 for v4.0.0 release** (without Wave 6)
6. **Release v4.1.0 in June 2026** with Wave 6 (multi-repo)

---

## Risk Management

### High Risks

1. **Migration Complexity**
   - **Risk**: Existing v3.x projects hard to migrate
   - **Mitigation**: Comprehensive migration script, testing with real projects
   - **Contingency**: Maintain v3.x LTS branch for 6 months

2. **Documentation Debt**
   - **Risk**: Massive restructuring creates broken links
   - **Mitigation**: Automated link checker, systematic validation
   - **Contingency**: Phased rollout, fix broken links in patches

3. **Community Confusion**
   - **Risk**: Breaking changes frustrate existing users
   - **Mitigation**: Clear communication, migration guide, examples
   - **Contingency**: Extended v3.x support, office hours for migration help

### Medium Risks

4. **Scope Creep**
   - **Risk**: Waves expand beyond estimates
   - **Mitigation**: Strict scope definition, defer non-critical features
   - **Contingency**: Drop Wave 6 from v4.0 scope if needed

5. **SAP Tooling Bugs**
   - **Risk**: install-sap.py has edge cases
   - **Mitigation**: Comprehensive test suite, user testing
   - **Contingency**: Manual installation fallback always available

6. **Merge Conflicts**
   - **Risk**: Upstream merges cause unexpected conflicts
   - **Mitigation**: Clear .chorabase boundaries, hybrid file handling
   - **Contingency**: Documentation for manual resolution

### Low Risks

7. **Performance Issues**
   - **Risk**: Scripts slow with large repos
   - **Mitigation**: Test with large repos, optimize as needed
   - **Contingency**: Async processing, progress indicators

---

## Post-v4.0 Roadmap

### v4.1.0 (June 2026)
- **Wave 6**: Multi-repo coordination
- SAP registry service
- External SAP discovery
- Enhanced inbox integration
- SAP versioning & upgrades

### v4.2.0 (Q3 2026)
- **Framework-specific SAPs** (following SAP-014 template):
  - SAP-015: Django Development (inspired by SAP-014 structure)
  - SAP-019: FastAPI Development
  - SAP-020: React/Next.js Development
  - SAP-021: Rust Web Services
- Language-specific SAP packs (Python, JavaScript, Rust, etc.)
- IDE integrations (VSCode extension for SAP navigation)
- AI agent optimizations (prompt engineering for Claude, GPT-4)

### v4.3.0 (Q4 2026)
- SAP marketplace (discover community SAPs)
- SAP quality scoring (adoption metrics, ratings)
- Automated SAP testing framework
- Cross-organization SAP sharing

### v5.0.0 (2027)
- TBD based on v4.x learnings
- Potential: Full SAP governance platform
- Potential: AI-generated SAPs
- Potential: Real-time SAP synchronization across repos

---

## Conclusion

Chora-Base v4.0 represents a fundamental rethinking of project foundations. By moving from template generation to a cloneable base with portable capability packages, we enable:

1. **Consistency** - All projects share structure
2. **Upgradability** - Structural improvements merge cleanly
3. **Portability** - SAPs work across projects (proven by SAP-014)
4. **Clarity** - LLMs understand the model
5. **Extensibility** - Easy to add new capabilities
6. **Preservation** - Expertise packaged, not discarded (SAP-014 preserves all MCP knowledge)

**SAP-014's Strategic Importance**:
- **First technology-specific SAP** - validates the optional capability model
- **Preserves MCP expertise** - rather than removing it, we enhance and package it
- **Templates future SAPs** - shows how to package Django, FastAPI, React, etc.
- **Proves v4.0's value** - demonstrates "universal base + optional capabilities" works

The 8-wave roadmap is ambitious but achievable. With Wave 6 deferred to v4.1, a March 2026 release is realistic. By tracking cleanup throughout Waves 1-7, Wave 8 becomes a simple execution step rather than a discovery phase.

**Next step**: Begin Wave 1 (Documentation Architecture Unification) immediately.

---

**Document Version**: 2.1 (Draft)
**Last Updated**: 2025-10-28
**Author**: Claude (with user guidance)
**Status**: Ready to begin Wave 1
**Changes from v2.0**:
- **Wave 3 Reframed**: "Eliminate MCP" → "Extract MCP into SAP-014"
- **SAP-014 Positioned**: First technology-specific SAP, preserves MCP expertise
- **Strategic Shift**: From removal to packaging (preservation over deletion)
- **Future Vision**: SAP-014 as template for Django, FastAPI, React SAPs
- **Success Criteria Updated**: Emphasizes capability preservation and portability

**Changes from v1.0**:
- Removed Wave 0 (upfront cleanup)
- Added cleanup tracking to each Wave 1-7
- Added Wave 8 (cleanup execution & release prep)
- Updated timeline to reflect 8-wave structure
