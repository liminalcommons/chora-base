# Chora-Base 4.0.0 Vision & Roadmap

**Version**: 3.0 (Updated post-Wave 3)
**Created**: 2025-10-28
**Last Updated**: 2025-10-29
**Status**: Wave 3 Complete, Wave 4 Planning
**Target Release**: Q1 2026 (February or January - 4-6 months ahead of schedule)

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

## Current State: v3.8.0 (Wave 3 Complete)

### Major Achievements (v3.6.0 - v3.8.0)
- ✅ **18 SAPs with 100% coverage** (was 16, added SAP-014, SAP-017, SAP-018)
- ✅ **Universal foundation achieved** - Framework-agnostic base with optional technology SAPs
- ✅ **SAP-014 (MCP Server Development)** - First technology-specific SAP, ~10,958 lines
- ✅ **SAP-017/018 (chora-compose Integration)** - First ecosystem integration SAPs, ~6,745 lines
- ✅ **blueprints/ deleted** - 11 templates migrated, setup.py removed (443 lines)
- ✅ **Root docs generalized** - README.md, AGENTS.md no longer MCP-specific
- ✅ **External linking pattern** - Established for ecosystem tool documentation
- ✅ **Clone-based workflow** - Template generation replaced with clone & customize

### Previous Achievements (v3.0.0 - v3.5.0)
- ✅ Documentation framework (Diátaxis-inspired)
- ✅ Complete automation tooling
- ✅ SAP framework with 4-domain architecture
- ✅ Comprehensive testing patterns

### Resolved Pain Points (Wave 3)
- ✅ ~~Template generation locks projects to creation-time version~~ - Now clone-based
- ✅ ~~MCP-specific assumptions in base~~ - MCP now optional via SAP-014
- ✅ ~~Two conflicting patterns: blueprints vs. SAP adoption~~ - blueprints removed
- ✅ ~~Valuable MCP expertise not packaged for reuse~~ - Now packaged as SAP-014

### Remaining Challenges (Wave 4+)
- 🔄 No upgrade path from chora-base improvements (Wave 4: merge model)
- 🔄 Link validation issues discovered (~629 broken links across older SAPs)
- 🔄 No SAP installation tooling (Wave 5)
- 🔄 Missing technology SAPs (Django, FastAPI, React - Wave 6+)

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

## Wave 1: Documentation Architecture Unification (v3.4.0) ✅ **COMPLETE**

**Status**: ✅ Complete (2025-10-29)
**Duration**: ~30 minutes (projected: 1-2 weeks)
**Effort**: ~0.5 hours (projected: 40-60 hours)

**Goal**: Align chora-base root docs/ with universal 4-domain structure

### Actual Achievements

1. ✅ Moved research PDF to `docs/dev-docs/research/`
2. ✅ Moved inventory files to `docs/project-docs/inventory/`
3. ✅ Archived chora-compose draft material (121 files, 2.2MB) to `docs/project-docs/archives/`
4. ✅ Deleted empty legacy directories (`docs/research/`, `docs/inventory/`, `docs/reference/`)
5. ✅ 4-domain structure now pure: `dev-docs/`, `project-docs/`, `user-docs/`, `skilled-awareness/`, `standards/`

**Metrics**:
- Files moved: ~15
- Directories cleaned: 3
- Archives created: 1 (121 files preserved)
- Efficiency: 79x faster than projected (0.5h vs. 40-60h)

**Result**: chora-base has clean, consistent 4-domain architecture

### Original Plan

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

## Wave 2: SAP Content Audit & Enhancement (v3.5.0) ✅ **COMPLETE**

**Status**: ✅ Complete (2025-10-29)
**Duration**: ~4 hours (projected: 2-3 weeks)
**Effort**: ~4 hours (projected: 80-120 hours)

**Goal**: Ensure all 18 SAPs properly reference the 4-domain structure and have complete content

### Actual Achievements

**SAP 4-Domain Integration Audit**:
- Audited all 18 SAPs for 4-domain cross-references
- Result: 17 out of 18 SAPs already had excellent 4-domain integration (6-70 references each)
- Enhanced SAP-018 (chora-compose-meta) from 0 → 13 cross-references

**User Documentation Creation** (12 files, ~4,200 lines):
1. ✅ `docs/user-docs/guides/github-actions.md` (605 lines)
2. ✅ `docs/user-docs/tutorials/debugging-ci-failures.md` (434 lines)
3. ✅ `docs/user-docs/tutorials/customizing-workflows.md` (461 lines)
4. ✅ `docs/user-docs/reference/workflow-reference.md` (515 lines)
5. ✅ `docs/user-docs/guides/installation.md` (234 lines)
6. ✅ `docs/user-docs/guides/quickstart.md` (75 lines)
7. ✅ `docs/user-docs/guides/code-quality.md` (275 lines)
8. ✅ `docs/user-docs/guides/docker-basics.md` (185 lines)
9. ✅ `docs/user-docs/guides/using-justfile.md` (125 lines)
10. ✅ `docs/user-docs/guides/working-with-agents.md` (365 lines)
11. ✅ `docs/user-docs/guides/cross-session-memory.md` (270 lines)
12. ✅ `docs/user-docs/guides/understanding-metrics.md` (280 lines)

**Metrics**:
- SAPs audited: 18 (all current SAPs)
- SAPs with good 4-domain integration: 18/18 (100%)
- User-docs files created: 12
- Total lines of documentation added: ~4,200
- Broken links reduced: ~180 → ~30-40 (78-83% reduction)
- Efficiency: 20-30x faster than projected (4h vs. 80-120h)

**Result**: All SAPs have comprehensive 4-domain cross-references, extensive user documentation created

### Original Plan

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

## Wave 3: Extract MCP Capabilities into SAP-014 (v3.6.0-v3.8.0) ✅ **COMPLETE**

**Status**: ✅ Complete (2025-10-29)
**Versions**: v3.6.0 (Track 1), v3.7.0 (Track 2), v3.8.0 (Track 3)
**Duration**: 1 day (projected: 3-4 weeks)
**Effort**: ~30 hours total (projected: 80-108 hours)

**Goal**: Make chora-base language/framework agnostic while preserving MCP server development capabilities as an optional, installable SAP-014 package

### Actual Achievements

**Track 1: SAP-014 MCP Server Development** (v3.6.0, ~15-20 hours):
- Created SAP-014 with 5 core artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- Created 4-domain supporting documentation (~20 additional files)
- Established Chora MCP Conventions v1.0 (standards)
- Migrated 11 blueprint templates to static-template/mcp-templates/
- Deleted blueprints/ directory and setup.py (443 lines)
- Generalized root documentation (README.md, AGENTS.md)
- **Total**: 25 files created, 15 files deleted, ~10,958 lines added

**Track 2: SAP-017/018 chora-compose Integration** (v3.7.0, ~13 hours):
- Created SAP-017 (chora-compose-integration): Tactical integration guide (4 files, 2,684 lines)
- Created SAP-018 (chora-compose-meta): Strategic meta-documentation (6 files, 4,061 lines)
- Documented 12+ integration patterns (minimal, full stack, hybrid, MCP, multi-project, CI/CD)
- Established external linking pattern for ecosystem tools
- Created two-SAP structure pattern (tactical + strategic)
- **Total**: 10 files created, ~6,745 lines added

**Track 3: Documentation & Closure** (v3.8.0, ~2 hours):
- Updated INDEX.md (16 → 18 SAPs)
- Created comprehensive Wave 3 summary (~950 lines)
- Updated CHANGELOG.md (v3.6.0, v3.7.0, v3.8.0 entries)
- Fixed forward references in SAP-017
- Published 2 GitHub releases

**Metrics**:
- SAPs created: 3 (SAP-014, SAP-017, SAP-018)
- Files created: 35
- Files deleted: 15
- Net files: +20
- Lines added: ~17,703
- Lines deleted: ~4,643
- Net lines: +13,060
- Link validation: 0 broken links (SAP-014, SAP-017, SAP-018)

**Key Patterns Established**:
1. **Technology-Specific SAP Pattern**: SAP-014 as template for Django, FastAPI, React
2. **Ecosystem Integration SAP Pattern**: Two-SAP structure (tactical + strategic)
3. **External Linking Pattern**: Link to external repos, don't duplicate docs
4. **Clone-Based Workflow**: Replaced blueprints + setup.py generation

**Impact**:
- ✅ chora-base is now framework-agnostic
- ✅ MCP capabilities preserved and enhanced as SAP-014
- ✅ First technology-specific SAP created
- ✅ First ecosystem integration SAPs created
- ✅ Template generation workflow retired
- ✅ Universal foundation achieved

### Original Plan (From v2.1 Vision Doc)

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

## Wave 5: SAP Installation Tooling (v4.1.0)

**Goal**: Make SAP adoption seamless for Claude and humans

**Status**: 🔄 In Progress (started 2025-10-29)
- ✅ SAP catalog created (commit e9653b2)
- 🔄 SAP sets feature added (COORD-2025-001 decision)
- 📋 install-sap.py pending

**Strategic Enhancement**: Added **SAP Sets** feature in response to COORD-2025-001 (chora-workspace coordination request for lightweight ecosystem onboarding). SAP sets provide curated bundles of SAPs installable with one command, solving the "18 SAPs are too many for quick entry" problem without creating prescriptive tiers.

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

#### 5.1b: SAP Sets Feature (NEW - from COORD-2025-001)

**Enhancement**: Add `sap_sets` section to catalog for curated SAP bundles

**Problem Solved**: chora-workspace identified that 18 SAPs (~100k tokens, 2-4 weeks) creates adoption friction for ecosystem coordination. Needed lightweight entry point.

**Solution**: SAP sets - curated bundles installable with one command, without formal SAP-019 or prescriptive tier terminology.

**5 Standard Sets**:

1. **minimal-entry** (5 SAPs) - Ecosystem onboarding
   - SAP-000 (sap-framework), SAP-001 (inbox), SAP-009 (agent-awareness), SAP-016 (link-validation), SAP-002 (chora-base-meta)
   - ~29k tokens (71% reduction from 100k)
   - 3-5 hours (90%+ reduction from 2-4 weeks)

2. **recommended** (10 SAPs) - Core dev workflow
   - Includes minimal-entry + SAP-003/004/005/006/007

3. **full** (18 SAPs) - Comprehensive coverage
   - All SAPs for advanced users

4. **testing-focused** (6 SAPs) - Testing & quality
   - SAP-000, 003, 004, 005, 006, 016

5. **mcp-server** (10 SAPs) - MCP development
   - Testing-focused + SAP-007, 009, 012, 014

**Custom Sets**: Projects can define organization-specific sets in `.chorabase`:

```yaml
# .chorabase
sap_sets:
  my-org-minimal:
    name: "Our Organization's Minimal Entry"
    saps: [SAP-000, SAP-004, SAP-007, SAP-009]
    estimated_tokens: 25000
```

**Installation**:
```bash
# Install standard set
python scripts/install-sap.py --set minimal-entry

# Install custom set
python scripts/install-sap.py --set my-org-minimal

# List available sets
python scripts/install-sap.py --list-sets
```

**Strategic Advantages**:
- ✅ Solves lightweight entry without formal SAP-019 (lower maintenance)
- ✅ No prescriptive tiers (Bronze/Silver/Gold) - maintains v4.0 flexible adoption
- ✅ Multiple use cases (minimal, testing, MCP, custom)
- ✅ Extensible for organizations
- ✅ Generalizable pattern for future needs

**Response**: inbox/outgoing/COORD-2025-001-response.json

#### 5.2: Create SAP Installation Script

**File**: `scripts/install-sap.py`

```python
#!/usr/bin/env python3
"""
Install a SAP from chora-base into current project.

Usage:
    # Install individual SAP
    python scripts/install-sap.py SAP-004
    python scripts/install-sap.py SAP-004 --source /path/to/chora-base

    # Install SAP set (NEW)
    python scripts/install-sap.py --set minimal-entry
    python scripts/install-sap.py --set recommended

    # List options
    python scripts/install-sap.py --list
    python scripts/install-sap.py --list-sets
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
**Duration**: 3-4 weeks
**Effort**: ~72-96 hours (increased from 60-80 due to SAP sets feature)
- Base functionality: 48-63 hours
- SAP sets enhancement: 24-33 hours

**Started**: 2025-10-29 (sap-catalog.json created, commit e9653b2)
**Target Completion**: Q1 2026 (v4.1.0)

**Breakdown**:
- Week 1: sap-catalog.json (✅ done), install-sap.py base (16-20 hours)
- Week 2: SAP sets feature (12-16 hours), validation (4-6 hours)
- Week 3: Documentation (10-14 hours), testing (8-12 hours)
- Week 4: Integration, polish, update adoption blueprints (12-16 hours)

**Strategic Note**: SAP sets feature added in response to COORD-2025-001 (chora-workspace coordination request). Adds ~20% complexity but solves ecosystem onboarding friction and aligns with v4.0 flexible adoption philosophy.

---

## Wave 6: Collections Architecture (v4.2.0 - PILOT PHASE APPROVED)

**Goal**: Evolve SAP sets into first-class collections with generation-based artifacts from constituent content

**Status**: 🧪 Pilot Phase Approved (2025-10-29)

**UPDATE (2025-10-29)**: **Major Discovery** - chora-compose IS a content generation framework (not Docker orchestration), with 17 production generators designed exactly for SAP use case. Pilot project approved to validate approach.

**Context**: Wave 5 introduces storage-based SAP sets (simple bundles). Wave 6 will implement generation-based collections using chora-compose as composition engine. Decision based on:
1. ✅ COORD-2025-002 response from chora-compose (strong alignment discovered)
2. ✅ Pilot project approved: Generate SAP-004 from constituent content blocks
3. ✅ chora-compose has 17 production generators + MCP tools for structured documentation
4. ⏳ Pilot must pass quality bar (80%+ of hand-written quality)

**Strategic Decision**: **Pursuing Option B** (generation-based) pending pilot success
- **Pilot Project**: Generate SAP-004 (Testing Framework) - 1-2 weeks, 4-6 hours effort
- **Go/No-Go Decision**: End of pilot based on quality assessment
- **If Go**: Full Wave 6 implementation in v4.2.0 with chora-compose
- **If No-Go**: Fall back to Option A (metadata only) or Option C (defer)

**Composition Tool Identified**: **chora-compose** (github.com/liminalcommons/chora-compose)
- NOT Docker orchestration (our SAP-017/018 document outdated version)
- IS content generation framework with artifact composition
- 17 production generators + 17 MCP tools
- Supports exactly our model: content blocks + context → SAP artifacts

**Dependencies**:
- ✅ Wave 5 (v4.1.0) ships and is adopted by at least one pilot repo (chora-workspace)
- ✅ chora-compose confirmed as composition engine
- 🧪 Pilot project with chora-compose (SAP-004 generation)
- ⏳ Pilot must pass quality bar (80%+ of hand-written quality)
- ⏳ Feedback from chora-workspace on collections needs

---

### Pilot Project: SAP-004 Generation (2025-11-06 to 2025-11-19)

**Status**: 🧪 Approved (2025-10-29)

**Goal**: Validate that chora-compose can generate SAP artifacts meeting quality bar

**Pilot SAP**: SAP-004 (Testing Framework)
- Why: Mature SAP with clear structure, technical depth, reusable patterns
- Current: 5 hand-written artifacts (~15k tokens, 8-12 hours to create)
- Target: Generate from content blocks + context

**Timeline**: 1-2 weeks (starting ~2025-11-06)

**Phases**:

**Phase 1: Decomposition** (Week 1, 2-4 hours)
- Decompose SAP-004 into constituent content blocks
- Identify reusable vs SAP-specific content
- Document content block structure

**Phase 2: Configuration** (Week 1-2, 1-2 hours)
- chora-compose creates content configs (5 artifact types)
- chora-base reviews and provides feedback
- Iterate on templates and structure

**Phase 3: Generation & Quality Review** (Week 2, 1-2 hours)
- Generate SAP-004 artifacts using chora-compose
- Compare generated vs hand-written
- Assess against 10 success criteria

**Phase 4: Go/No-Go Decision** (Week 2, 1 hour)
- If quality ≥ 80%: Proceed with Wave 6 Option B
- If quality < 80%: Fall back to Option A or C
- Document learnings regardless of outcome

**Collaboration**:
- Async coordination (24-48 hour response times)
- Via inbox protocol + GitHub issues
- Tracked in: docs/design/pilot-sap-004-generation.md

**Related Coordination**:
- COORD-2025-002: Exploratory request to chora-compose (sent 2025-10-29)
- COORD-2025-002-response: chora-compose response (received 2025-10-29)
- COORD-2025-002-RESPONSE: Acceptance of pilot (sent 2025-10-29)
- COORD-2025-002-CLARIFICATION: 5 detailed architectural questions (sent 2025-10-30)
- COORD-2025-002-CLARIFICATION-RESPONSE: Comprehensive answers (received 2025-10-30)
- COORD-2025-002-CLARIFICATION-RESPONSE-acknowledgment: Readiness confirmed (sent 2025-10-30)

**UPDATE (2025-10-30)**: **Clarification Complete** - All 5 architectural questions answered comprehensively (1,124-line technical response). **No blockers for pilot** - strong foundation with minor gaps (2-6 hours each if needed).

**Key Findings from Clarification**:

**Terminology Alignment**:
- chora-compose uses: `force: bool` (industry standard from git, npm, docker)
- Not: "latest" vs "fresh" terminology
- **Mapping**: force=False (use cached) = our "latest", force=True (regenerate) = our "fresh"

**Content Architecture** (Q2 - PERFECT MATCH):
- Hybrid: Template Slots + Modular Blocks
- ContentElement = atomic unit (5-7 per artifact)
- GenerationPattern = assembly logic (Jinja2 templates)
- ChildReference = modular composition (reusable blocks)
- **Recommendation**: Decompose each SAP artifact into 5-7 ContentElements, extract shared patterns

**Context Schema** (Q3 - FULLY FLEXIBLE):
- No predefined schema - define exactly what we need
- 6 InputSource types: content_config, external_file, git_reference, ephemeral_output, inline_data, artifact_config
- JSONPath selectors for data extraction
- **Recommendation**: Define repo_metadata, existing_capabilities, user_preferences, coordination_context

**Hybrid Storage + Generation** (Q4 - PARTIAL SUPPORT, WORKS MANUALLY):
- Can mix canonical (stored) and generated artifacts
- Manual hybrid via external_file works today
- Auto-orchestration needs 2-4 hours if desired
- **Recommendation**: Create passthrough configs for canonical SAPs, generation for customized SAPs

**Storage Location** (Q5 - CLEAR PATTERNS):
- Content blocks: `chora-base/docs/content-blocks/` (domain content)
- Configs: `chora-base/configs/content/` and `chora-base/configs/artifact/`
- Generated outputs: `ephemeral/{content_id}/{timestamp}.{format}`
- **Recommendation**: Hybrid approach - content in chora-base, configs in both repos

**Pilot Readiness**:
- Week 1 decomposition steps detailed with examples
- Expected outputs: ~10-15 content blocks, 5 content configs, 1 artifact config
- Feature gaps identified with effort estimates (2-6 hours each if needed)
- Discovery mode encouraged - iterate based on what works

---

### Tasks (If Pilot Succeeds → Option B)

#### 6.1: Enhanced Collection Schema

**If pursuing rich metadata** (Option A - lower complexity):

```json
{
  "collections": [
    {
      "id": "minimal-entry",
      "name": "Minimal Ecosystem Entry",
      "version": "1.0.0",
      "saps": ["SAP-000", "SAP-001", "SAP-009", "SAP-016", "SAP-002"],
      "dependencies_resolved": ["SAP-000", "SAP-016", "SAP-002", "SAP-001", "SAP-009"],
      "installation_order": [...],
      "estimated_tokens": 29000,
      "estimated_hours": "3-5",
      "success_criteria": [
        "AGENTS.md declares capabilities",
        "inbox/ structure exists"
      ],
      "context_requirements": {
        "repo_role": "optional",
        "existing_capabilities": "optional"
      }
    }
  ]
}
```

**Enhancements over v4.1.0 SAP sets**:
- Dependency resolution tracked
- Success criteria explicit
- Context requirements documented
- Versioning support
- Richer metadata for tools

#### 6.2: Constituent Content Architecture

**If pursuing generation-based** (Option B - higher complexity):

**Exploration needed**:
1. Decompose 1-2 example SAPs into constituent content blocks (manual exercise)
2. Assess quality of decomposition
3. Identify reusable patterns across SAPs
4. Determine storage model (content-blocks/ in chora-base? external tool?)

**Potential structure**:
```
docs/
  content-blocks/          # NEW: Reusable content chunks
    sap-framework-problem.md
    sap-framework-solution-core.md
    testing-introduction.md
    testing-pytest-setup.md
    ...
  composition-recipes/     # NEW: How to assemble SAPs
    SAP-000-charter.yaml
    SAP-000-protocol.yaml
    ...
  skilled-awareness/       # EXISTING: May become generated artifacts
    sap-framework/
    testing-framework/
    ...
```

**Key Questions**:
- What tool generates artifacts? (custom script, LLM API, template engine, external tool?)
- Where is authoritative source? (content blocks or generated artifacts?)
- How to ensure generated quality matches hand-written quality?
- "Latest" vs "fresh" semantics for caching?

#### 6.3: Composition Tooling

**If pursuing generation-based**:

**Option A: Custom Python Script**
```python
#!/usr/bin/env python3
"""Compose SAP artifacts from constituent content blocks"""

def compose_sap_artifact(
    sap_id: str,
    artifact_type: str,  # charter, protocol, guide, blueprint, ledger
    context: dict,       # repo_role, existing_capabilities, preferences
    freshness: str = "latest"  # or "fresh"
):
    """Generate artifact from content blocks + context"""
```

**Option B: Integration with External Tool**
- Coordinate with ecosystem tool for composition capabilities
- Co-discover what's possible (not prescribe requirements)
- See exploration notes for coordination approach

**Option C: LLM-Based Generation**
- Use Anthropic/OpenAI API for semantic composition
- Content blocks as context, prompts for structure
- Quality review required

**Decision Needed**: Which approach aligns with chora-base capabilities and philosophy?

#### 6.4: Migration Path (SAP Sets → Collections)

**Breaking Change in v4.2.0**:

v4.1.0 syntax:
```bash
python scripts/install-sap.py --set minimal-entry
```

v4.2.0 syntax:
```bash
python scripts/install-sap.py --collection minimal-entry
# or migrate to chora-compose if external tool integration happens
```

**Migration Guide Required**:
- Document syntax changes
- Provide backward compatibility shim (deprecation warning)
- Update all documentation examples
- Notify ecosystem via inbox protocol

### Coordination Requirements

#### With chora-workspace (Pilot Feedback)

**Questions to ask after v4.1.0 ships**:
1. How well did minimal-entry set meet your needs?
2. What role-based collections would be valuable?
3. Should SAPs adapt to repo context (generation) or stay uniform (storage)?
4. Are custom organizational sets needed?

#### With Composition Tool (If Pursuing Generation)

**See**: [docs/design/collections-exploration-notes.md](../design/collections-exploration-notes.md) for detailed co-discovery approach

**NOT prescribing requirements**. Instead, exploring:
- What capabilities exist today?
- What would be natural extensions?
- Is this aligned with tool's vision?
- Can we experiment together?

**Co-discovery coordination request** (to be created if pursuing):
- Type: `architecture_proposal` (exploratory, not implementation request)
- Questions, not requirements
- Collaboration modes as options
- Explicit non-requirements documented

### Effort Estimate (Updated 2025-10-29)

**Pilot Project (Approved)**:
- SAP-004 decomposition: 2-4 hours (chora-base)
- Config creation: 2-4 hours (chora-compose)
- Generation & quality review: 1-2 hours (both)
- Decision meeting: 1 hour (both)
- **Total Pilot**: 6-11 hours combined, 4-6 hours chora-base effort

**Option A: Rich Metadata Only** (Fallback if pilot fails)
- Collection schema enhancement: 8-12 hours
- Documentation: 6-8 hours
- Migration guide: 4-6 hours
- **Total**: 18-26 hours

**Option B: Generation-Based Collections** (If pilot succeeds)
- **Per chora-compose estimate**: 20-40 hours total (after initial setup)
- **Breakdown**:
  - Content decomposition (18 SAPs): 10-15 hours
  - chora-compose integration: 5-10 hours (configs, templates)
  - SAP-017/018 rewrite: 16-24 hours (document current chora-compose)
  - Testing and quality assurance: 10-15 hours
  - Documentation: 10-15 hours
  - Migration guide: 5-10 hours
- **Total**: 56-89 hours (vs original estimate of 81-138 hours)
- **Maintenance reduction**: 144-216 hours → 20-40 hours (87% reduction)

### Success Criteria (Updated 2025-10-29)

**Pilot Success Criteria** (SAP-004 Generation):
- ✅ Generated artifacts match structure of hand-written SAP-004
- ✅ Quality meets "could publish this" bar (80%+ of hand-written quality)
- ✅ Performance: generation time < 5 seconds per artifact
- ✅ Maintainability: updating content block → regenerate → changed artifacts
- ✅ Flexibility: same blocks + different context → customized output
- ✅ Technical accuracy: generated content is factually correct
- ✅ Coherence: reads as unified documentation, not assembled fragments
- ✅ Agent-readability: Claude can parse and understand generated SAPs
- ✅ Ease of maintenance: content blocks easy to update without deep framework knowledge
- ✅ Scalability: clear path to generating remaining 17 SAPs

**Wave 6 Option B Success** (If pilot passes):
- ✅ All 18 SAPs decomposed into constituent content blocks
- ✅ chora-compose generates artifacts meeting quality bar for all SAPs
- ✅ Generation time < 5 seconds per artifact across all SAPs
- ✅ Content blocks maintained in chora-base (version controlled)
- ✅ SAP-017/018 updated to reflect current chora-compose capabilities
- ✅ Context-aware generation working (same SAP, different contexts → customized)
- ✅ At least 1 ecosystem repo adopts generated collections successfully

**Wave 6 Option A Success** (Fallback if pilot fails):
- ✅ Collections have richer metadata than SAP sets
- ✅ Dependency resolution automatic
- ✅ Success criteria explicit and testable
- ✅ At least 2 ecosystem repos adopt collections successfully

### Decision Points (Updated 2025-10-29)

**Decision Point 1** (RESOLVED - 2025-10-29): Pursue Wave 6 in v4.2.0?
- **Decision**: YES - Pilot project approved
- **Factors**: chora-compose response showed strong alignment
- **Next**: Pilot SAP-004 generation (1-2 weeks)

**Decision Point 2** (End of Pilot - ~2025-11-19): Go/No-Go for Option B?
- **Go Threshold**: Generated SAP-004 meets 80%+ of hand-written quality
- **If Go**: Proceed with Wave 6 Option B (generation-based) in v4.2.0
- **If No-Go**: Fall back to Option A (metadata only) or Option C (defer to v4.3.0)

**Decision Point 3** (RESOLVED - 2025-10-29): Which composition approach?
- **Decision**: chora-compose (content generation framework)
- **Factors**: Perfect alignment, 17 production generators, proven at scale, MCP integration
- **Status**: Pilot project underway to validate

### Cleanup Tracking

If Wave 6 is included, track in `v4-cleanup-manifest.md`:

**Files to Delete**:
- None (additive, though may deprecate --set flag in favor of --collection)

**Files to Create**:
- `docs/design/collections-architecture-rfc.md` (formal RFC if pursuing)
- `docs/content-blocks/` (if pursuing generation)
- `docs/composition-recipes/` (if pursuing generation)
- `scripts/compose-sap.py` (if custom composition script)

**Files to Update**:
- `sap-catalog.json` (collections schema enhancement)
- `scripts/install-sap.py` (--collection flag, deprecate --set)
- All Wave 5 documentation (migration examples)

**References to Update**:
- SAP-000 (SAP Framework) - document collections pattern
- Wave 5 documentation - migration notes

**Git History**:
- Breaking change (v4.1.0 → v4.2.0) requires semver minor bump

---

## Wave 7: Multi-Repo Coordination (v4.3.0+ - DEFERRED)

**Goal**: Enable SAP discovery and sharing across organization repos

**Note**: Previously planned as Wave 6. Deferred to allow Wave 6 focus on collections architecture. May be implemented in v4.3.0 or later based on ecosystem needs.

**See Previous Planning**: Original Wave 6 content (multi-repo coordination) available in git history if needed.

### High-Level Tasks (When Implemented)

- SAP Registry Protocol for cross-repo discovery
- Enhanced Inbox Integration for SAP coordination
- SAP Versioning with semantic versioning
- External SAP installation from other repos

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

| Wave | Version | Status | Duration (Projected → Actual) | Effort (Projected → Actual) | Deliverables |
|------|---------|--------|------------------------------|----------------------------|--------------|
| Wave 1 | v3.4.0 | ✅ **Complete** | ~~1-2 weeks~~ → **30 min** | ~~40-60h~~ → **0.5h** | 4-domain docs structure cleanup |
| Wave 2 | v3.5.0 | ✅ **Complete** | ~~2-3 weeks~~ → **4 hours** | ~~80-120h~~ → **4h** | SAP 4-domain audit + 12 user-docs files |
| Wave 3 | v3.6.0-v3.8.0 | ✅ **Complete** | ~~3-4 weeks~~ → **1 day** | ~~80-108h~~ → **~30h** | MCP extraction (SAP-014) + chora-compose SAPs (SAP-017/018) + Track 3 closure |
| Wave 4 | v3.9.0 | 🔄 Next | 2-3 weeks | 60-80h | Clone & merge model |
| Wave 5 | v3.10.0 | 🔄 Pending | 2-3 weeks | 60-80h | SAP installation tooling |
| Wave 6 | v3.11.0 | 🔄 Optional | 3-4 weeks | 100+h | Multi-repo (OPTIONAL - defer to v4.1?) |
| Wave 7 | v3.12.0 | 🔄 Pending | 2-3 weeks | 60-80h | Testing & validation |
| Wave 8 | v4.0.0-rc1 | 🔄 Pending | 1 week | 20-30h | Cleanup execution & release prep |

**Progress**: Wave 3 complete (2025-10-29), **4-6 months ahead of schedule**

### Updated Timeline (Post-Wave 3)

**Aggressive Timeline (No Wave 6)** - *RECOMMENDED*
**Total Remaining**: 9-13 weeks (~2-3.5 months from now)
- Wave 1-2: Skipped or significantly reduced (4-domain structure largely exists, SAP content already high-quality)
- Wave 4: November-December 2025 (clone & merge model)
- Wave 5: December 2025-January 2026 (SAP installation tooling)
- Wave 7: January-February 2026 (testing & validation)
- Wave 8: February 2026 (cleanup & release prep)
- **Release**: February 2026 (vs. March 2026 original)

**Conservative Timeline (With Wave 6)** - *IF NEEDED*
**Total Remaining**: 13-18 weeks (~3-4.5 months from now)
- Wave 1-2: Skipped or significantly reduced
- Wave 4: November-December 2025
- Wave 5: December 2025-January 2026
- Wave 6: January-February 2026 (multi-repo)
- Wave 7: February-March 2026
- Wave 8: March 2026
- **Release**: March-April 2026

**Most Aggressive** - *IF WAVE 1-2 CAN BE SKIPPED*
**Total Remaining**: 6-10 weeks (~1.5-2.5 months from now)
- Wave 4: November 2025 (2-3 weeks)
- Wave 5: December 2025 (2-3 weeks)
- Wave 7: December 2025-January 2026 (2-3 weeks)
- Wave 8: January 2026 (1 week)
- **Release**: January 2026 (5 months ahead!)

### Updated Recommendations (Post-Wave 3)

1. **✅ Wave 3 Complete** - Exceeded expectations (1 day vs. 3-4 weeks)
2. **Evaluate Wave 1-2 Necessity** - 4-domain structure largely exists, SAP content already comprehensive
3. **Skip directly to Wave 4** if Wave 1-2 not needed (recommendation: assess first)
4. **Defer Wave 6 to v4.1.0** - Multi-repo is nice-to-have, not critical
5. **Target Q1 2026 for v4.0.0 release** - February or January (4-6 months ahead of schedule)
6. **Release v4.1.0 in Q2 2026** with Wave 6 if needed

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

**Document Version**: 3.0 (Updated post-Wave 3)
**Last Updated**: 2025-10-29
**Author**: Claude (with user guidance)
**Status**: Wave 3 Complete, Wave 4 Planning

**Changes from v2.1**:
- **Current State Updated**: v3.3.0 → v3.8.0 (Wave 3 completed)
- **Wave 3 Status**: Moved from "Future Work" to "Completed Work"
- **Wave 3 Metrics**: Documented actual vs. projected (1 day vs. 3-4 weeks, 30 hours vs. 80-108 hours)
- **Timeline Adjusted**: v4.0.0 release accelerated by 4-6 months (ahead of schedule)
- **SAP Count**: 16 → 18 SAPs (SAP-014, SAP-017, SAP-018 added)

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
