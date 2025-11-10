# SAP-002: Chora-Base Meta Package

**Version:** 1.0.0 | **Status:** Active | **Maturity:** Production

> Meta-capability describing chora-base itself using the SAP framework—a comprehensive template and framework for AI-assisted software development with 32+ modular capabilities.

---

## 🚀 Quick Start (2 minutes)

```bash
# 1. Show chora-base meta information
just chora-info

# 2. Verify structure integrity
just verify-structure

# 3. Explore documentation structure
just explore-docs

# 4. List all available SAPs
just list-saps
```

**First time?** → Read [Root README.md](../../../README.md) for complete project overview (10-min read)

---

## 📖 What Is SAP-002?

SAP-002 is the **self-documenting meta-capability** that describes chora-base using the SAP framework—demonstrating the framework's power through dogfooding. Chora-base is a comprehensive template and framework for AI-agent-first Python development, built around 32+ Skilled Awareness Packages (SAPs) providing modular capabilities for production-ready projects.

**Key Innovation**: By using SAP-002 to document chora-base itself, we demonstrate that the SAP framework is sufficiently expressive to capture complex, multi-capability systems—not just individual tools.

---

## 🎯 When to Use

Use SAP-002 when you need to:

1. **Understand chora-base architecture** - Learn how the template repository is structured and how SAPs fit together
2. **Navigate 32+ SAPs** - Discover which capabilities are available and how to adopt them
3. **Bootstrap new projects** - Use chora-base as a template for production-ready Python projects
4. **Contribute to chora-base** - Understand the meta-architecture before adding new capabilities
5. **Demonstrate SAP framework** - Show how SAPs can document entire systems, not just tools

**Not needed for**: Using individual SAPs (each SAP has its own documentation), or quick project generation (use fast-setup script directly)

---

## ✨ Key Features

- ✅ **32+ Skilled Awareness Packages** - Modular capabilities for development workflows (testing, CI/CD, documentation, etc.)
- ✅ **Agent-First Design** - Built for Claude Code, Claude Desktop, and other AI agents with progressive context loading
- ✅ **Nested Awareness Pattern** - 5-level hierarchy (root → domain → SAP → feature → component) with 60-70% token savings
- ✅ **Production-Ready Templates** - Fast-setup script generates projects in 1-2 minutes with all quality gates
- ✅ **Coordination Infrastructure** - Cross-repo inbox (SAP-001), event memory (SAP-010), task tracking (SAP-015)
- ✅ **Self-Documenting** - SAP-002 uses SAP framework to document chora-base itself (dogfooding)
- ✅ **Zero Configuration** - Generated projects pass all quality gates out-of-the-box (85%+ coverage, linting, types)

---

## 📚 Quick Reference

### 2 CLI Commands

#### 1. **chora-info** - Show Meta Information
```bash
just chora-info
# Shows: SAP-002 overview, purpose, documentation links, benefits
# Use: Quick orientation for new contributors or users
```

#### 2. **verify-structure** - Verify Integrity
```bash
just verify-structure
# Shows: Directory structure validation, missing artifacts, consistency checks
# Use: After pulling updates or before contributing
```

### Key Directories

```
chora-base/
├── docs/
│   ├── skilled-awareness/        # 32+ SAP capabilities
│   │   ├── sap-framework/        # SAP-000: Foundation
│   │   ├── inbox/                # SAP-001: Coordination
│   │   ├── chora-base/           # SAP-002: Meta (you are here)
│   │   ├── project-bootstrap/    # SAP-003: Fast-setup
│   │   └── ...                   # 28+ more SAPs
│   ├── user-docs/                # User-facing documentation
│   ├── dev-docs/                 # Developer documentation
│   └── project-docs/             # Project management
├── scripts/                      # Automation scripts
├── justfile                      # Command automation (30+ recipes)
├── CLAUDE.md                     # Root AI agent awareness
├── AGENTS.md                     # Root agent patterns
└── README.md                     # Project overview
```

---

## 🔗 Integration with Other SAPs

SAP-002 is the **meta-SAP** that coordinates all other SAPs:

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-000** (SAP Framework) | Foundation | SAP-002 uses SAP-000 to document itself (5 artifacts) |
| **SAP-009** (Agent Awareness) | Discoverability | SAP-002 uses nested awareness pattern for 32+ SAPs |
| **SAP-003** (Bootstrap) | Project Generation | Fast-setup script creates new projects from chora-base template |
| **SAP-029** (SAP Generation) | New Capabilities | Generate new SAPs using sap-catalog.json + templates |
| **All 32+ SAPs** | Ecosystem | SAP-002 provides the container for all capabilities |

**Meta-Architecture Workflow**:
```bash
# 1. Understand chora-base (SAP-002)
just chora-info
cat docs/skilled-awareness/chora-base/protocol-spec.md

# 2. Explore available SAPs
just list-saps
cat docs/skilled-awareness/INDEX.md

# 3. Adopt specific SAP
cd my-project/
# Follow SAP's adoption-blueprint.md

# 4. Generate new SAP
just generate-sap SAP-042
# Uses SAP-029 to create SAP artifacts
```

---

## 📂 SAP-002 Artifacts

This directory contains the 5 standard SAP artifacts documenting chora-base:

1. **[capability-charter.md](capability-charter.md)** - Problem statement, solution design, stakeholders, lifecycle
2. **[protocol-spec.md](protocol-spec.md)** - Technical architecture, 32+ SAP specifications, quality gates
3. **[AGENTS.md](AGENTS.md)** - AI agent patterns for navigating chora-base ecosystem (28KB, 15-min read)
4. **[adoption-blueprint.md](adoption-blueprint.md)** - How to use chora-base as a template (fast-setup workflow)
5. **[ledger.md](ledger.md)** - Production adoption metrics, feedback, version history

---

## 🏗️ Chora-Base Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Template Repository (chora-base)      │
│  - 32+ SAP capabilities                         │
│  - Documentation framework (Diátaxis)           │
│  - Quality gates (pytest, ruff, mypy)          │
└─────────────────┬───────────────────────────────┘
                  │
                  │ fast-setup (1-2 min)
                  ↓
┌─────────────────────────────────────────────────┐
│  Layer 2: Generated Projects                    │
│  - Adopt SAPs incrementally                     │
│  - Inherit quality gates                        │
│  - Production-ready from day 1                  │
└─────────────────┬───────────────────────────────┘
                  │
                  │ coordination (SAP-001)
                  ↓
┌─────────────────────────────────────────────────┐
│  Layer 3: Ecosystem Collaboration               │
│  - Cross-repo coordination (inbox)              │
│  - Event memory (A-MEM)                         │
│  - Task tracking (beads)                        │
└─────────────────────────────────────────────────┘
```

### SAP Categories (32+ Total)

**Foundation (5 SAPs)**: Core infrastructure
- SAP-000 (SAP Framework), SAP-001 (Inbox), SAP-002 (Chora-Base), SAP-009 (Agent Awareness), SAP-010 (A-MEM)

**Development Workflow (6 SAPs)**: Quality and automation
- SAP-003 (Bootstrap), SAP-004 (Testing), SAP-005 (CI/CD), SAP-006 (Quality Gates), SAP-008 (Automation), SAP-011 (Docker)

**Documentation & Process (4 SAPs)**: Knowledge management
- SAP-007 (Documentation), SAP-012 (Lifecycle), SAP-015 (Task Tracking), SAP-016 (Link Validation)

**React Ecosystem (16 SAPs)**: Next.js 15 + React 19 capabilities
- SAP-020 through SAP-040 (Foundation, Testing, State, Styling, Performance, Authentication, Database, File Upload, Real-Time, i18n, E2E, Monorepo, etc.)

**Meta SAPs (3 SAPs)**: Framework evolution
- SAP-027 (Dogfooding), SAP-028 (Publishing), SAP-029 (SAP Generation)

See [sap-catalog.json](../../../sap-catalog.json) or [INDEX.md](../INDEX.md) for complete list.

---

## 🎓 Progressive Context Loading

Chora-base uses **5-level nested awareness** to optimize AI agent token usage:

### Phase 1: Orientation (0-10k tokens)
Read root awareness files for project overview:
- [/CLAUDE.md](../../../CLAUDE.md) - Root Claude patterns
- [/AGENTS.md](../../../AGENTS.md) - Root agent patterns
- [sap-catalog.json](../../../sap-catalog.json) - SAP inventory

**Output**: Clear understanding of where to find detailed information

### Phase 2: Specification (10-50k tokens)
Read domain-specific awareness files:
- [docs/skilled-awareness/AGENTS.md](../AGENTS.md) - SAP domain patterns
- [docs/skilled-awareness/CLAUDE.md](../CLAUDE.md) - Claude SAP workflows
- Target SAP's protocol-spec.md for technical details

**Output**: Complete technical understanding of specific capability

### Phase 3: Deep Dive (50-200k tokens)
Read complete SAP artifacts only when needed:
- capability-charter.md for problem/solution design
- ledger.md for adoption metrics and feedback
- adoption-blueprint.md for installation from scratch
- Source code files as needed

**Output**: Comprehensive understanding for complex implementations

**Token Savings**: 60-70% reduction vs reading all docs upfront

---

## 🏆 Success Metrics

- **Project Generation**: 1-2 minutes (from template to production-ready project)
- **Quality Gates**: 100% compliance out-of-the-box (85%+ coverage, linting, types)
- **SAP Adoption**: 32+ capabilities available, average 80-90% time savings per SAP
- **Agent Support**: 5-level nested awareness with 60-70% token reduction
- **Ecosystem Collaboration**: 90% coordination effort reduction via SAP-001 inbox protocol

---

## 📄 Learn More

### SAP-002 Artifacts (This Directory)
- **[protocol-spec.md](protocol-spec.md)** - Complete technical architecture, 32+ SAP specifications (34KB)
- **[AGENTS.md](AGENTS.md)** - AI agent navigation patterns for chora-base ecosystem (28KB, 15-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific progressive loading strategies (18KB, 9-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Fast-setup workflow for generating projects (10KB)
- **[capability-charter.md](capability-charter.md)** - Problem statement and solution design (14KB)
- **[ledger.md](ledger.md)** - Production adoption metrics and version history (17KB)

### Root Documentation
- **[README.md](../../../README.md)** - Chora-base project overview (10-min read)
- **[CLAUDE.md](../../../CLAUDE.md)** - Root Claude awareness (comprehensive navigation guide)
- **[AGENTS.md](../../../AGENTS.md)** - Root agent patterns (quick decision tree)

### Domain Documentation
- **[User Docs](../../user-docs/)** - Tutorials, how-to guides, reference
- **[Dev Docs](../../dev-docs/)** - Architecture, contributing, development setup
- **[Project Docs](../../project-docs/)** - Plans, decisions, retrospectives

### SAP Catalog
- **[sap-catalog.json](../../../sap-catalog.json)** - Machine-readable SAP registry (32+ SAPs)
- **[INDEX.md](../INDEX.md)** - Human-readable SAP catalog with descriptions

---

## 🔧 Troubleshooting

**Problem**: `verify-structure` reports missing artifacts

**Solution**: Check for required files per SAP-000 protocol:
```bash
# Each SAP must have 5 artifacts
ls docs/skilled-awareness/my-sap/
# Expected: capability-charter.md, protocol-spec.md,
#           awareness-guide.md (or AGENTS.md),
#           adoption-blueprint.md, ledger.md
```

---

**Problem**: Can't find specific SAP in documentation

**Solution**: Use SAP catalog search:
```bash
# List all SAPs
just list-saps

# Search by keyword
grep -i "keyword" sap-catalog.json

# Browse index
cat docs/skilled-awareness/INDEX.md
```

---

**Problem**: Generated project missing SAP capabilities

**Solution**: SAPs are adopted incrementally, not all included by default:
```bash
# Check which SAPs are included by default
grep '"included_by_default": true' sap-catalog.json

# Adopt additional SAPs as needed
# Follow SAP's adoption-blueprint.md
```

---

## 📞 Support

- **Documentation**: Read [protocol-spec.md](protocol-spec.md) for complete architecture
- **Contributing**: See [dev-docs/CONTRIBUTING.md](../../dev-docs/CONTRIBUTING.md)
- **Issues**: Report bugs via GitHub issues with `[SAP-002]` prefix
- **Coordination**: Use SAP-001 inbox to propose new SAPs or features

---

## 🔍 Dogfooding Demonstration

SAP-002 demonstrates the **SAP framework's expressiveness** by using it to document a complex system (chora-base itself) with 32+ capabilities. This proves that SAPs are not limited to documenting individual tools—they can capture entire ecosystems.

**What This Shows**:
1. **Scalability**: SAP framework handles meta-documentation (SAP documenting SAPs)
2. **Composability**: SAP-002 coordinates 32+ other SAPs without conflicts
3. **Self-Documenting**: chora-base practices what it preaches (SAP-000 protocol compliance)
4. **Progressive Loading**: Even meta-SAPs benefit from nested awareness pattern (60-70% token savings)

**Evidence**: SAP-002 follows the same 5-artifact structure as all other SAPs, proving the framework is universal.

---

**Version History**:
- **1.0.0** (2025-10-28) - Initial meta-capability documentation with 32+ SAP ecosystem

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
