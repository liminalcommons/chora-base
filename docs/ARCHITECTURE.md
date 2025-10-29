# Chora-Base Documentation Architecture

**Version**: 4.0
**Last Updated**: 2025-10-28
**Status**: Active (Wave 1 implementation)

---

## Executive Summary

Chora-base uses a **universal 4-domain documentation architecture** that separates concerns by audience and lifecycle:

1. **dev-docs/** - For developers working ON the product (process documentation)
2. **project-docs/** - Project lifecycle artifacts (living documents from PM process)
3. **user-docs/** - For users of the delivered product (end-user documentation)
4. **skilled-awareness/** - SAP Framework meta-layer (cross-cutting capabilities)

This structure is **consistent** across all repositories using chora-base, enabling:
- LLMs to navigate any project with the same mental model
- Predictable documentation locations
- Clear separation of concerns
- Upgradeable structure via git merge

---

## The 4-Domain Model

### Visual Structure

```
repo/
├── docs/
│   ├── dev-docs/              ← Domain 1: Developer Process
│   │   ├── workflows/         ← How we build (DDD, BDD, TDD)
│   │   ├── examples/          ← Code walkthroughs
│   │   ├── vision/            ← Long-term roadmap
│   │   ├── research/          ← Technical investigations
│   │   ├── explanation/       ← Design philosophy
│   │   └── README.md
│   │
│   ├── project-docs/          ← Domain 2: Project Lifecycle
│   │   ├── sprints/           ← Sprint plans & retrospectives
│   │   ├── releases/          ← Release notes & plans
│   │   ├── metrics/           ← Process & quality metrics
│   │   ├── integration/       ← Integration plans
│   │   ├── inventory/         ← Repository audits
│   │   └── README.md
│   │
│   ├── user-docs/             ← Domain 3: End-User Documentation
│   │   ├── how-to/            ← Task-oriented guides
│   │   ├── explanation/       ← Conceptual deep-dives
│   │   ├── reference/         ← API docs, config specs
│   │   ├── tutorials/         ← Learning-oriented lessons
│   │   └── README.md
│   │
│   └── skilled-awareness/     ← Domain 4: SAP Meta-Layer
│       ├── sap-framework/     ← SAP-000 (always included)
│       ├── INDEX.md           ← Central SAP registry
│       ├── document-templates.md
│       └── [capability-saps]/ ← Adopted SAPs
│
├── src/                       ← System: Source code
├── tests/                     ← System: Test suite
├── scripts/                   ← System: Automation & tooling
├── .github/                   ← System: CI/CD workflows
├── docker/                    ← System: Container configs
│
├── AGENTS.md                  ← Root: Agent guidance
├── CLAUDE.md                  ← Root: Claude-specific optimizations
├── README.md                  ← Root: Project overview
├── CHANGELOG.md               ← Root: Version history
├── ROADMAP.md                 ← Root: Product roadmap
└── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  ← Root: SAP protocol spec
```

---

## Domain 1: dev-docs/

**Purpose**: Documentation for developers working ON the product

**Audience**:
- Engineers building features
- Contributors to the codebase
- AI agents implementing functionality

**Diátaxis Application**:
- **how-to/** - Process guides ("how to implement TDD", "how to write BDD scenarios")
- **explanation/** - Conceptual understanding ("why test-first", "design philosophy")
- **reference/** - Process specifications ("workflow definitions", "conventions")

**Subdirectories**:
- `workflows/` - Complete development lifecycle processes (DDD, BDD, TDD, etc.)
- `examples/` - Code walkthroughs and demonstrations
- `vision/` - Long-term capability roadmap
- `research/` - Technical investigations and learnings

**Examples**:
- `dev-docs/workflows/TDD_WORKFLOW.md` - Test-Driven Development process
- `dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md` - How DDD → BDD → TDD connect
- `dev-docs/examples/FEATURE_WALKTHROUGH.md` - OAuth2 implementation walkthrough
- `dev-docs/research/adopter-learnings-mcp-orchestration.md` - MCP learnings

**Not Here**:
- End-user guides (→ user-docs/)
- Sprint plans (→ project-docs/sprints/)
- API documentation (→ user-docs/reference/)
- SAP documentation (→ skilled-awareness/)

---

## Domain 2: project-docs/

**Purpose**: Living documents generated/updated during project lifecycle

**Audience**:
- Project managers
- Stakeholders
- Future maintainers
- Leadership

**Characteristics**:
- **Living**: Updated throughout project lifecycle
- **Historical**: Permanent record of decisions and progress
- **Stakeholder-facing**: Often shared with PMs, leadership
- **Generated**: Created as part of PM process, not written upfront

**Subdirectories**:
- `sprints/` - Sprint plans, retrospectives, velocity tracking
- `releases/` - Release notes, plans, post-mortems
- `metrics/` - Quality metrics, process metrics, ROI calculations
- `integration/` - Integration plans, coordination documents
- `inventory/` - Repository audits, coherence reports

**Examples**:
- `project-docs/sprints/wave-1-sprint-plan.md` - Wave 1 sprint planning
- `project-docs/metrics/wave-1-execution-metrics.md` - Measured results
- `project-docs/releases/v3.4.0-wave-1-release-notes.md` - What shipped
- `project-docs/inventory/COHERENCE_REPORT.md` - 100% coherence achievement
- `project-docs/integration/v3.3.0-integration-plan.md` - Integration coordination

**Not Here**:
- Development processes (→ dev-docs/workflows/)
- User guides (→ user-docs/)
- Code examples (→ dev-docs/examples/)

---

## Domain 3: user-docs/

**Purpose**: Documentation for users of the delivered product

**Audience**:
- End-users consuming the product
- Developers integrating with APIs
- Operators deploying the system
- New adopters learning the product

**Diátaxis Application** (Full Framework):
- **how-to/** - Task-oriented guides ("how to install", "how to configure")
- **explanation/** - Conceptual understanding ("architecture", "design decisions")
- **reference/** - Technical specifications ("API docs", "config reference")
- **tutorials/** - Learning-oriented lessons ("getting started", "first project")

**Examples**:
- `user-docs/how-to/write-executable-documentation.md` - Guide for writing executable docs
- `user-docs/explanation/benefits-of-chora-base.md` - Why use chora-base
- `user-docs/explanation/architecture-clarification.md` - Architectural concepts
- `user-docs/reference/mcp-naming-best-practices.md` - Naming conventions spec
- `user-docs/tutorials/getting-started.md` - First steps with the product

**Not Here**:
- Development processes (→ dev-docs/)
- Sprint plans (→ project-docs/)
- SAP installation (→ skilled-awareness/)

---

## Domain 4: skilled-awareness/

**Purpose**: SAP Framework meta-layer (cross-cutting capabilities)

**Audience**:
- All roles (developers, PMs, users)
- AI agents
- External adopters
- Future wave implementations

**Structure**: Always includes SAP-000 (SAP Framework itself)

**SAP Anatomy** (5 artifacts per SAP):
1. `capability-charter.md` - High-level overview, business value
2. `protocol-spec.md` - Technical contracts, inputs/outputs
3. `awareness-guide.md` - How to use, references to all 4 domains
4. `adoption-blueprint.md` - Installation steps
5. `ledger.md` - Adoption tracking

**Cross-Domain References**:
SAPs are meta-layer - they reference content in all 3 other domains:

Example: SAP-004 (Testing Framework) references:
- `dev-docs/workflows/TDD_WORKFLOW.md` - Process
- `project-docs/metrics/test-coverage.md` - Quality tracking
- `user-docs/reference/testing-conventions.md` - Conventions spec
- `tests/` - Actual test suite (system)

**Examples**:
- `skilled-awareness/sap-framework/` - SAP-000 artifacts
- `skilled-awareness/testing-framework/` - SAP-004 artifacts
- `skilled-awareness/INDEX.md` - Central SAP registry
- `skilled-awareness/document-templates.md` - SAP templates

**Not Here**:
- Implementation details (→ src/, tests/)
- User guides (→ user-docs/)
- Process workflows (→ dev-docs/)

---

## Decision Trees

### Where does new documentation go?

```
Start here → Is this documentation...

┌─────────────────────────────────────────────────────┐
│ FOR DEVELOPERS WORKING ON THE PRODUCT?              │
│ (Building features, contributing code)              │
└─────────────────────────────────────────────────────┘
          │
          ├─ YES → dev-docs/
          │        │
          │        ├─ About development PROCESS? → workflows/
          │        ├─ About design PHILOSOPHY? → explanation/
          │        ├─ WALKTHROUGH or EXAMPLE? → examples/
          │        ├─ RESEARCH or LEARNINGS? → research/
          │        └─ LONG-TERM VISION? → vision/
          │
          └─ NO → Continue...

┌─────────────────────────────────────────────────────┐
│ GENERATED DURING PROJECT LIFECYCLE?                 │
│ (Sprint artifacts, metrics, release notes)          │
└─────────────────────────────────────────────────────┘
          │
          ├─ YES → project-docs/
          │        │
          │        ├─ Generated during SPRINTS? → sprints/
          │        ├─ About RELEASES? → releases/
          │        ├─ METRICS or MEASUREMENTS? → metrics/
          │        ├─ INTEGRATION PLANS? → integration/
          │        └─ INVENTORY or AUDITS? → inventory/
          │
          └─ NO → Continue...

┌─────────────────────────────────────────────────────┐
│ FOR END-USERS OF THE PRODUCT?                       │
│ (Using, integrating, deploying the product)         │
└─────────────────────────────────────────────────────┘
          │
          ├─ YES → user-docs/
          │        │
          │        ├─ HOW-TO task guide? → how-to/
          │        ├─ CONCEPTUAL explanation? → explanation/
          │        ├─ REFERENCE spec? → reference/
          │        └─ TUTORIAL for learning? → tutorials/
          │
          └─ NO → Continue...

┌─────────────────────────────────────────────────────┐
│ CROSS-CUTTING CAPABILITY (SAP)?                     │
│ (Reusable capability package, meta-documentation)   │
└─────────────────────────────────────────────────────┘
          │
          └─ YES → skilled-awareness/
                   │
                   ├─ SAP FRAMEWORK itself? → sap-framework/
                   ├─ Capability package? → {capability-name}/
                   ├─ SAP INDEX? → INDEX.md
                   └─ SAP templates? → document-templates.md
```

### Diátaxis Classification (for dev-docs/ and user-docs/)

```
Is the reader...

LEARNING? (studying, acquiring knowledge)
    └─ tutorials/ (learning-oriented)
       - Goal: teach basics through lessons
       - Structure: step-by-step, beginner-friendly
       - Example: "Your First MCP Server"

ACHIEVING A GOAL? (working, problem-solving)
    └─ how-to/ (task-oriented)
       - Goal: solve specific problem
       - Structure: steps to accomplish task
       - Example: "How to Deploy with Docker"

SEEKING INFORMATION? (checking, looking up)
    └─ reference/ (information-oriented)
       - Goal: find specific fact
       - Structure: dry, accurate, complete
       - Example: "API Reference", "Config Spec"

UNDERSTANDING? (studying, thinking)
    └─ explanation/ (understanding-oriented)
       - Goal: understand WHY and HOW
       - Structure: conceptual, contextual
       - Example: "Architecture Explanation"
```

---

## Relationship to Diátaxis

**Diátaxis** is a documentation framework with 4 categories:
1. **Tutorials** (learning-oriented)
2. **How-to Guides** (task-oriented)
3. **Reference** (information-oriented)
4. **Explanation** (understanding-oriented)

**Chora-base applies Diátaxis to TWO domains**:

### dev-docs/ → Diátaxis for Development
- **how-to/**: "How to implement TDD", "How to write BDD scenarios"
- **explanation/**: "Why test-first", "Design philosophy"
- **reference/**: "Workflow definitions", "Process conventions"
- **tutorials/**: "Your first feature using DDD→BDD→TDD"

### user-docs/ → Diátaxis for Product Usage
- **how-to/**: "How to install", "How to configure", "How to deploy"
- **explanation/**: "Architecture overview", "Design decisions"
- **reference/**: "API documentation", "Configuration reference"
- **tutorials/**: "Getting started", "Build your first integration"

### project-docs/ → Does NOT use Diátaxis
- Living documents from PM process
- Not structured by learning/task/info/understanding
- Structured by lifecycle phase (sprints, releases, metrics)

### skilled-awareness/ → Does NOT use Diátaxis
- Meta-layer referencing all other domains
- Structured by SAP protocol (5 artifacts per SAP)
- Cross-cutting capabilities, not documentation categories

---

## Benefits of 4-Domain Architecture

### 1. Clear Separation of Concerns
- Developers know where to find process docs (dev-docs/)
- PMs know where to find sprint/release docs (project-docs/)
- Users know where to find product docs (user-docs/)
- Everyone knows where to find capabilities (skilled-awareness/)

### 2. LLM-Navigable
- Consistent structure across all repos
- Predictable file locations
- Same mental model everywhere
- Reduces "where does this go?" questions

### 3. Upgradeable Structure
- Structure is universal (mergeable from upstream)
- Content is project-specific (customizable)
- Can pull structural improvements via `git merge chora-base/main`
- Clear boundaries via `.chorabase` metadata

### 4. Evidence-Based Workflow
- dev-docs/ documents HOW we work
- project-docs/ tracks WHAT we delivered
- user-docs/ explains WHAT users get
- skilled-awareness/ captures reusable CAPABILITIES

### 5. Meta-Demonstration
- Chora-base uses its own framework
- Wave 1 sprint plan in project-docs/sprints/
- Migration workflow in dev-docs/workflows/
- Wave 1 metrics in project-docs/metrics/
- ARCHITECTURE.md in root (high visibility)

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Mixing Audiences
**Problem**: User guides in dev-docs/, sprint plans in user-docs/

**Impact**:
- Confusing for readers
- Hard to maintain
- Breaks LLM navigation

**Solution**: ✅ Use decision tree to classify correctly

---

### ❌ Anti-Pattern 2: Flat docs/ Structure
**Problem**: All docs at root level (`docs/file1.md`, `docs/file2.md`, ...)

**Impact**:
- Overwhelming number of files
- No clear organization
- Impossible to navigate
- No separation of concerns

**Solution**: ✅ Use 4-domain structure with subdirectories

---

### ❌ Anti-Pattern 3: Domain Subdirectory Confusion
**Problem**: Creating `user-docs/dev-docs/` or similar nested domains

**Impact**:
- Breaks the model
- Confusing hierarchy
- Defeats purpose of separation

**Solution**: ✅ Domains are peers at `docs/` level, not nested

---

### ❌ Anti-Pattern 4: Duplicate Documentation
**Problem**: Same content in multiple domains

**Impact**:
- Maintenance burden
- Inconsistencies
- Unclear single source of truth

**Solution**: ✅ Each document has ONE home, cross-reference from others

---

### ❌ Anti-Pattern 5: Ignoring SAP Meta-Layer
**Problem**: Creating SAPs in user-docs/ or dev-docs/

**Impact**:
- SAPs are cross-cutting, shouldn't be domain-specific
- Breaks SAP protocol
- Hard to discover capabilities

**Solution**: ✅ All SAPs in skilled-awareness/, reference other domains from there

---

## Migration from Old Structure

If migrating from previous structure:

1. **Baseline Inventory**: Run inventory, record file count
2. **Classify Files**: Use decision tree to determine domain
3. **Create Directories**: Create missing subdirectories
4. **Move Files**: Migrate one domain at a time
5. **Update References**: Update cross-references immediately
6. **Validate**: Run inventory + link checker after each domain
7. **Track Cleanup**: Update v4-cleanup-manifest.md as you go
8. **Metrics**: Measure time, validate 100% coherence

See: [docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md](dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md)

---

## Examples from Chora-Base

### Root docs/ Structure (Before Wave 1)
```
docs/
├── BENEFITS.md              ← Mixed
├── DOCUMENTATION_PLAN.md    ← Mixed
├── integration/             ← Mixed
├── inventory/               ← Mixed
├── reference/               ← Mixed
│   ├── skilled-awareness/   ← Buried
│   └── ecosystem/           ← Mixed
├── releases/                ← Mixed
└── research/                ← Mixed
```

### Root docs/ Structure (After Wave 1)
```
docs/
├── dev-docs/
│   ├── workflows/
│   ├── examples/
│   ├── vision/
│   ├── research/            ← Moved here
│   └── README.md
├── project-docs/
│   ├── sprints/             ← NEW
│   ├── releases/            ← Moved here
│   ├── metrics/
│   ├── integration/         ← Moved here
│   ├── inventory/           ← Moved here
│   └── README.md
├── user-docs/
│   ├── how-to/
│   ├── explanation/         ← BENEFITS moved here
│   ├── reference/
│   └── README.md
└── skilled-awareness/       ← Moved from reference/
    ├── sap-framework/
    ├── INDEX.md
    └── [14 SAPs]/
```

---

## Tools & Validation

### Validation Scripts
- `scripts/inventory-chora-base.py` - Verify 100% coherence
- Link checker - Ensure no broken references
- SAP validator - Verify all SAP artifacts complete

### Expected Metrics
- **Total files**: Should match baseline (no files lost)
- **SAP coverage**: 100%
- **Uncovered files**: 0
- **Broken links**: 0

---

## Future Evolution

### Wave 2: SAP Content Audit
- Ensure all SAPs reference actual implementation files
- Add missing dev-docs/ workflows
- Add missing user-docs/ documentation
- Make cross-domain references explicit

### Wave 3-7: Further Refinement
- Continue evolving 4-domain structure
- Add new content types as discovered
- Enhance subdirectory organization
- Improve cross-references

### v4.0 Release
- 4-domain structure fully adopted
- All SAPs reference all 4 domains
- Documentation comprehensive
- Structure upgradeable via git merge

---

## Questions & Answers

**Q: Where do I put code examples?**
A:
- If demonstrating HOW to develop (process), → dev-docs/examples/
- If demonstrating HOW to use product (end-user), → user-docs/how-to/ or tutorials/
- If actual runnable code, → examples/ directory (outside docs/)

**Q: Where do I put API documentation?**
A: user-docs/reference/ (end-users need to reference API specs)

**Q: Where do I put retrospectives?**
A: project-docs/sprints/ (lifecycle artifact from sprint process)

**Q: Where do I put architectural diagrams?**
A: user-docs/explanation/ (conceptual understanding for users)

**Q: Where do I put a new SAP?**
A: skilled-awareness/{sap-name}/ (all SAPs go here)

**Q: Can a SAP reference dev-docs/?**
A: YES! SAPs are meta-layer and reference all 4 domains

**Q: Where does ARCHITECTURE.md go?**
A: Root-level docs/ for high visibility (or user-docs/explanation/)

**Q: What if content fits multiple domains?**
A: Choose ONE primary home, cross-reference from others

---

## Related Documentation

**Workflows**:
- [Documentation Migration Workflow](dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md)
- [Development Lifecycle](dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) (from static-template)

**Vision**:
- [Chora-Base 4.0 Vision](project-docs/CHORA-BASE-4.0-VISION.md)
- [Wave 1 Sprint Plan](project-docs/sprints/wave-1-sprint-plan.md)

**SAP Framework**:
- [SAP Framework](skilled-awareness/sap-framework/)
- [SAP INDEX](skilled-awareness/INDEX.md)

**User Guides**:
- [Benefits of Chora-Base](user-docs/explanation/benefits-of-chora-base.md)

---

**Architecture Version**: 1.0
**Implemented In**: Wave 1 (v3.4.0)
**Status**: Active
**Next Review**: Wave 2 (SAP Content Audit)

This architecture document is itself an example of user-docs/explanation/ content (though placed at root for visibility during Wave 1 migration).
