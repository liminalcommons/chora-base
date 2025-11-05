# Understanding SAPs (Skilled Awareness Packages)

**Purpose**: Conceptual overview of the SAP framework
**Audience**: Developers and AI agents new to chora-base
**Reading Time**: 10-15 minutes
**Category**: Explanation (Diataxis)

**Last Updated**: 2025-11-05

---

## Table of Contents

1. [What is a SAP?](#what-is-a-sap)
2. [Why SAPs Exist](#why-saps-exist)
3. [SAP Structure: The 5-7 Artifact Pattern](#sap-structure-the-5-7-artifact-pattern)
4. [SAP Lifecycle and Status Levels](#sap-lifecycle-and-status-levels)
5. [SAP Sets: Curated Bundles](#sap-sets-curated-bundles)
6. [SAP IDs vs Directory Names](#sap-ids-vs-directory-names)
7. [How SAPs Relate to chora-base](#how-saps-relate-to-chora-base)
8. [SAP Adoption Process](#sap-adoption-process)
9. [SAPs vs Other Patterns](#saps-vs-other-patterns)
10. [Common Misconceptions](#common-misconceptions)

---

## What is a SAP?

**SAP** stands for **Skilled Awareness Package**.

A SAP is a **self-contained, reusable capability** packaged with standardized documentation. It's both:
1. **A protocol/pattern** to follow (e.g., "how to structure tests")
2. **Complete documentation** for adopting that pattern (adoption guide, technical spec, examples)

Think of a SAP as a "recipe book + ingredients list + cooking techniques + quality checklist" for a specific development capability.

### Example

**SAP-004 (testing-framework)** is a SAP that packages:
- **The Capability**: pytest-based testing patterns with coverage, fixtures, mocking
- **The Documentation**: How to set up pytest, write tests, run tests, integrate with CI/CD
- **The Standards**: File naming conventions, test organization, quality gates

When you "adopt SAP-004", you're learning and implementing those pytest patterns in your project.

### SAP Framework Origins

The SAP framework itself is **SAP-000 (sap-framework)** - it's self-documenting! SAP-000 defines:
- What a SAP is
- The 5-7 artifact structure
- How to create new SAPs
- Governance and versioning

**Meta-fact**: Every SAP (including SAP-000) follows the SAP-000 specification. This self-referential property ensures consistency across all SAPs.

---

## Why SAPs Exist

### Problem: Documentation Fragmentation

Before SAPs, chora-base documentation suffered from:
- **Inconsistent structure**: Some guides had adoption steps, others didn't
- **Missing information**: Technical specs without examples, or examples without specs
- **Poor AI agent support**: No standardized "AGENTS.md" file for agent-specific patterns
- **Hard to discover**: No catalog of capabilities, unclear dependencies

### Solution: Standardized Packaging

SAPs solve this by:
1. **Enforcing structure**: Every SAP has the same 5-7 artifacts (AGENTS.md, protocol-spec.md, etc.)
2. **Completeness guarantee**: Can't be a SAP without adoption guide + technical spec + awareness guide
3. **AI-first design**: AGENTS.md and CLAUDE.md files provide agent-specific guidance
4. **Catalog-driven**: sap-catalog.json provides machine-readable registry of all SAPs

### Benefits

**For Developers**:
- Predictable documentation structure (always know where to find adoption steps)
- Clear dependencies (know what SAPs you need first)
- Adoption tracking (ledger.md shows your progress)

**For AI Agents**:
- Standardized navigation (AGENTS.md at known location)
- Clear protocols (protocol-spec.md has complete technical details)
- Tool-optimized guidance (CLAUDE.md for Claude Code, etc.)

**For Project Maintainers**:
- Consistent quality (all SAPs follow same template)
- Easy to add capabilities (just follow SAP-000 pattern)
- Versionable (each SAP has independent semantic versioning)

---

## SAP Structure: The 5-7 Artifact Pattern

Every SAP contains **5 required artifacts** and **up to 2 optional artifacts**:

### Required Artifacts (5)

#### 1. capability-charter.md
**Purpose**: Problem statement, solution design, success criteria

**Contains**:
- What problem does this SAP solve?
- Why this solution approach?
- What are the goals and non-goals?
- What are success criteria for adoption?

**Read this when**: Understanding the "why" behind a SAP

**Example** (SAP-004 testing-framework):
```markdown
## Problem
Python projects need consistent, maintainable testing practices...

## Solution
SAP-004 provides pytest-based testing framework with...

## Success Criteria
- [ ] 80%+ test coverage
- [ ] All tests pass in CI/CD
- [ ] Test execution < 5 minutes
```

#### 2. protocol-spec.md
**Purpose**: Complete technical specification

**Contains**:
- Technical architecture and design
- Commands, APIs, file structures
- Configuration options
- Integration points with other SAPs
- Complete reference documentation

**Read this when**: Implementing the SAP (need technical details)

**Example** (SAP-004):
```markdown
## Pytest Configuration

File: `pyproject.toml`

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
...
```

#### 3. AGENTS.md or awareness-guide.md
**Purpose**: Operating patterns for AI agents

**Contains**:
- Quick reference for agents
- Common commands and workflows
- Integration with other SAPs
- Agent-specific tips and warnings

**Read this when**: You're an AI agent navigating this SAP

**Example** (SAP-004 AGENTS.md):
```markdown
## Quick Commands

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src/myproject tests/
```

#### 4. adoption-blueprint.md
**Purpose**: Step-by-step implementation guide

**Contains**:
- Prerequisites and dependencies
- Installation steps
- Configuration steps
- Validation steps
- Troubleshooting common issues

**Read this when**: Actually adopting/implementing this SAP

**Example** (SAP-004):
```markdown
## Step 1: Install Dependencies

pip install pytest pytest-cov pytest-mock

## Step 2: Configure pytest

Create `pyproject.toml` with...

## Step 3: Write First Test

Create `tests/test_example.py`:...
```

#### 5. ledger.md
**Purpose**: Adoption tracking and version history

**Contains**:
- Adoption metrics (how many projects using this?)
- Version history (what changed in each version?)
- Adoption feedback (what issues did users face?)
- Status updates (moved from draft → pilot → active)

**Read this when**: Understanding SAP maturity and adoption trends

**Example** (SAP-004 ledger.md):
```markdown
## Adoption Tiers

- **Essential**: Basic pytest setup (5 projects)
- **Recommended**: Coverage + fixtures (3 projects)
- **Advanced**: Property-based testing (1 project)

## Version History

- v1.0.0 (2025-10-01): Initial release
- v1.1.0 (2025-10-15): Added pytest-mock patterns
```

### Optional Artifacts (2)

#### 6. CLAUDE.md (optional but recommended)
**Purpose**: Claude Code-specific patterns and optimizations

**Contains**:
- Claude Code tool usage (Read, Bash, Glob, Grep)
- Progressive context loading strategies
- Claude-specific workflows
- Tips for leveraging Claude's strengths

**Read this when**: You're Claude Code agent

**Example** (SAP-000 CLAUDE.md):
```markdown
## Progressive Context Loading

Phase 1: Read AGENTS.md (5-10k tokens)
Phase 2: Read protocol-spec.md (10-50k tokens)
Phase 3: Read capability-charter.md (50-200k tokens)
```

#### 7. README.md (optional, for human-readable overview)
**Purpose**: Human-friendly introduction

**Contains**:
- Quick overview of SAP
- Key features and highlights
- Links to other artifacts
- Getting started tips

**Read this when**: First exposure to a SAP, want quick summary

---

## SAP Lifecycle and Status Levels

SAPs evolve through three lifecycle stages:

### Status: draft

**Meaning**: Experimental, under active development

**Characteristics**:
- Artifacts may be incomplete
- Breaking changes expected
- Not recommended for production use
- Limited testing and validation

**When to use**: Only if explicitly exploring experimental features

**Example**: SAP-026 (react-accessibility) in early development

### Status: pilot

**Meaning**: Functional but undergoing validation

**Characteristics**:
- All required artifacts complete
- Dogfooding in real projects (validation phase)
- May undergo changes based on feedback
- Stable enough for non-critical projects

**When to use**: If you're willing to provide feedback and adapt to changes

**Example**: SAP-001 (inbox) during ecosystem validation

### Status: active

**Meaning**: Production-ready, battle-tested

**Characteristics**:
- Validated in multiple projects
- Stable API/patterns (semantic versioning for changes)
- Comprehensive documentation
- Recommended for production use

**When to use**: Default choice - use freely

**Example**: SAP-000 (sap-framework), SAP-005 (ci-cd-workflows), SAP-006 (quality-gates)

### Status Transitions

```
draft → pilot → active
  ↓       ↓       ↓
  (experimental) (validation) (production)
```

**How SAPs advance**:
1. **draft → pilot**: All artifacts complete, ready for dogfooding
2. **pilot → active**: Validated in 2+ projects, positive feedback, no major issues

**Rare transitions**:
- **active → pilot**: Major breaking changes required (avoid if possible)
- **pilot → draft**: Fundamental design issues discovered (rare)
- **deprecated**: SAP superseded by newer SAP (archived, not deleted)

---

## SAP Sets: Curated Bundles

**SAP Sets** are pre-defined bundles of SAPs for specific use cases.

### Why SAP Sets Exist

**Problem**: With 29+ SAPs, which should you adopt first?

**Solution**: Curated sets that make sense together:
- **minimal-entry**: Essential 5 SAPs for getting started
- **testing-focused**: 6 SAPs for quality-first development
- **mcp-server**: 10 SAPs for building MCP servers
- **recommended**: 10 SAPs for production-ready projects
- **full**: 18 SAPs for comprehensive reference
- **react-development**: 10 SAPs for React/Next.js apps

### SAP Set Structure

Defined in `sap-catalog.json` under `"sap_sets"`:

```json
{
  "minimal-entry": {
    "name": "Minimal Ecosystem Entry",
    "description": "Essential SAPs for first-time chora ecosystem adoption",
    "saps": ["SAP-000", "SAP-001", "SAP-009", "SAP-016", "SAP-002"],
    "estimated_tokens": 29000,
    "estimated_hours": "3-5",
    "use_cases": [
      "First-time chora ecosystem adoption",
      "Contributing to ecosystem repos via inbox protocol"
    ]
  }
}
```

### Example: minimal-entry Set

**SAPs included**:
1. **SAP-000 (sap-framework)**: Foundation - understand what SAPs are
2. **SAP-001 (inbox)**: Cross-repo coordination protocol
3. **SAP-002 (chora-base)**: Meta-SAP documenting chora-base itself
4. **SAP-009 (agent-awareness)**: AGENTS.md/CLAUDE.md nested pattern
5. **SAP-016 (link-validation)**: Validate markdown links

**Why these together**:
- SAP-000 is foundational (required to understand SAPs)
- SAP-001 + SAP-009 enable ecosystem collaboration
- SAP-016 ensures documentation quality
- SAP-002 provides self-reference documentation

**Adoption order**: Follow numeric order (SAP-000 → SAP-001 → SAP-002 → SAP-009 → SAP-016)

### How to Use SAP Sets

**Option 1: Adopt entire set**
```bash
# View SAP set contents
grep -A 30 '"minimal-entry"' sap-catalog.json

# Explore each SAP in order
cat docs/skilled-awareness/sap-framework/AGENTS.md
cat docs/skilled-awareness/inbox/AGENTS.md
# etc...
```

**Option 2: Pick individual SAPs from set**
```bash
# Maybe you only need SAP-000 and SAP-009
cat docs/skilled-awareness/sap-framework/adoption-blueprint.md
cat docs/skilled-awareness/agent-awareness/adoption-blueprint.md
```

**Note**: SAP sets are **reference bundles**, not installable packages. chora-base already has all SAPs - sets just suggest which to explore first.

---

## SAP IDs vs Directory Names

### The Mapping

**SAP ID format** (used in catalog and references):
- `SAP-000`, `SAP-001`, `SAP-004`, `SAP-015`
- Zero-padded three-digit numbers
- Used in documentation cross-references

**Directory name format** (actual filesystem):
- `sap-framework/`, `inbox/`, `testing-framework/`, `task-tracking/`
- Lowercase with hyphens
- Used in file paths

### Examples

| SAP ID | Directory Name | Location |
|--------|---------------|----------|
| SAP-000 | `sap-framework` | `docs/skilled-awareness/sap-framework/` |
| SAP-001 | `inbox` | `docs/skilled-awareness/inbox/` |
| SAP-004 | `testing-framework` | `docs/skilled-awareness/testing-framework/` |
| SAP-009 | `agent-awareness` | `docs/skilled-awareness/agent-awareness/` |
| SAP-014 | `mcp-server-development` | `docs/skilled-awareness/mcp-server-development/` |
| SAP-015 | `task-tracking` | `docs/skilled-awareness/task-tracking/` |

### How to Find Mapping

**In sap-catalog.json** (machine-readable):
```bash
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep location
# Output: "location": "docs/skilled-awareness/task-tracking"
```

**Why the difference?**
- **SAP IDs**: Stable identifiers, never change even if directory renamed
- **Directory names**: Human-readable, match common naming conventions

### Common Mistake

❌ **Wrong**: `ls docs/skilled-awareness/SAP-000-sap-framework/`
✅ **Correct**: `ls docs/skilled-awareness/sap-framework/`

**Previous quickstart guides (now fixed)** assumed `SAP-XXX-name/` format, causing 90% of commands to fail.

---

## How SAPs Relate to chora-base

### chora-base's Dual Purpose

**chora-base** is both:
1. **A Python project template** - bootstrap new Python projects with best practices
2. **A SAP distribution repository** - includes 29 pre-installed SAPs

### Architecture

```
chora-base/
├── src/                     # Python source code (template)
├── tests/                   # Python tests (template)
├── docs/
│   ├── skilled-awareness/   # ← 29 SAPs live here
│   │   ├── sap-framework/   # SAP-000
│   │   ├── inbox/           # SAP-001
│   │   ├── testing-framework/ # SAP-004
│   │   └── ... (26 more)
│   ├── user-docs/           # User-facing documentation
│   ├── dev-docs/            # Developer documentation
│   └── project-docs/        # Project management docs
├── sap-catalog.json         # SAP registry (29 SAPs)
├── CLAUDE.md                # Root Claude navigation
├── AGENTS.md                # Root agent patterns
└── README.md                # Project overview
```

### Using chora-base

**As a template** (for new projects):
```bash
# 1. Clone chora-base
git clone https://github.com/org/chora-base.git my-new-project
cd my-new-project

# 2. Remove SAPs you don't need
rm -rf docs/skilled-awareness/react-*  # If not React project

# 3. Customize for your project
nano AGENTS.md
nano README.md

# 4. Start developing with adopted SAP patterns
```

**As a SAP reference** (for learning):
```bash
# 1. Clone chora-base
git clone https://github.com/org/chora-base.git
cd chora-base

# 2. Explore SAPs
cat docs/skilled-awareness/sap-framework/AGENTS.md

# 3. Adopt patterns into your existing project
# (Copy patterns, not entire SAP directories)
```

### SAPs Are Pre-Installed

**Key Concept**: You **don't install SAPs** from chora-base - they're already there! You:
1. **Explore** them (read AGENTS.md, protocol-spec.md)
2. **Adopt** their patterns (follow adoption-blueprint.md)
3. **Track** your progress (update ledger.md)

**Previous confusion** (now fixed): Old quickstart guides claimed to "install SAPs via script" - this was incorrect. SAPs are documentation + patterns, not installable packages.

---

## SAP Adoption Process

### Adoption Tiers

Most SAPs define three adoption tiers:

#### Essential Tier (~5 minutes)
**Goal**: Minimal viable adoption

**Example** (SAP-004 testing-framework):
- Install pytest
- Create `tests/` directory
- Write one test
- Run `pytest`

**When to stop here**: Prototyping, learning, time-constrained

#### Recommended Tier (~15 minutes)
**Goal**: Production-ready setup

**Example** (SAP-004):
- Essential tier +
- Configure pytest in `pyproject.toml`
- Add coverage reporting
- Set up fixtures
- Integrate with CI/CD

**When to stop here**: Most projects - balanced effort/value

#### Advanced Tier (~30-60 minutes)
**Goal**: Full capability adoption

**Example** (SAP-004):
- Recommended tier +
- Property-based testing (Hypothesis)
- Mutation testing (mutmut)
- Performance benchmarks (pytest-benchmark)
- Custom plugins

**When to stop here**: Critical projects, advanced needs

### Step-by-Step Process

1. **Read AGENTS.md** (2-3 min) - Quick overview
2. **Read protocol-spec.md** (5-10 min) - Technical details
3. **Read adoption-blueprint.md** (3-5 min) - Implementation steps
4. **Follow blueprint** (5-60 min depending on tier) - Actually adopt
5. **Update ledger.md** (1 min) - Track your adoption tier
6. **Validate** (2-5 min) - Run tests, check success criteria

### Multi-SAP Adoption

**When adopting multiple SAPs**:
1. Follow dependency order (SAP-000 before everything)
2. Adopt in small batches (2-3 SAPs at a time)
3. Validate each before moving to next
4. Track progress (update each ledger.md)

**Example - minimal-entry set**:
```
Session 1 (Day 1): SAP-000 (sap-framework) - understand foundation
Session 2 (Day 1): SAP-009 (agent-awareness) - set up AGENTS.md
Session 3 (Day 2): SAP-001 (inbox) - coordination protocol
Session 4 (Day 2): SAP-016 (link-validation) - documentation quality
Session 5 (Day 3): SAP-002 (chora-base) - self-reference documentation
```

---

## SAPs vs Other Patterns

### SAPs vs Design Patterns (Gang of Four)

| Aspect | SAPs | Design Patterns |
|--------|------|-----------------|
| **Scope** | Complete capabilities | Code structures |
| **Documentation** | 5-7 artifacts | 1-2 pages |
| **Examples** | Complete adoption guides | Code snippets |
| **Tooling** | CLI tools, configs | Code only |
| **AI-Aware** | Yes (AGENTS.md, CLAUDE.md) | No |

**Example**:
- **Design Pattern**: "Singleton" - how to ensure only one instance
- **SAP**: "SAP-004 (testing-framework)" - complete pytest setup with fixtures, coverage, CI/CD integration

### SAPs vs RFCs (Request for Comments)

| Aspect | SAPs | RFCs |
|--------|------|-----|
| **Purpose** | Package capabilities | Propose standards |
| **Status** | Draft → Pilot → Active | Proposed → Accepted |
| **Implementation** | Included in SAP | Separate |
| **Documentation** | 5-7 artifacts | 1 document |
| **Versioning** | Semantic versioning | Sequential numbering |

**Example**:
- **RFC**: "RFC 7540: HTTP/2" - specification of protocol
- **SAP**: "SAP-014 (mcp-server)" - how to build MCP servers (implementation + spec)

### SAPs vs ADRs (Architecture Decision Records)

| Aspect | SAPs | ADRs |
|--------|------|-----|
| **Purpose** | Reusable capabilities | Record decisions |
| **Scope** | Multi-project | Single project |
| **Mutability** | Versioned updates | Immutable (append-only) |
| **Structure** | 5-7 artifacts | 1 document |

**Example**:
- **ADR**: "ADR-012: We chose pytest over unittest" - decision record
- **SAP**: "SAP-004 (testing-framework)" - how to use pytest (reusable pattern)

**SAPs can reference ADRs**: A SAP's capability-charter.md might say "Based on ADR-012, we chose pytest..."

---

## Common Misconceptions

### Misconception 1: "SAPs are installable packages"

**Wrong**: SAPs are installed via `install-sap.py` script

**Right**: SAPs are pre-installed documentation. You **explore** and **adopt** their patterns, not "install" them.

**Why the confusion**: Previous quickstart guides (now fixed) described installation workflow that didn't match repository structure.

### Misconception 2: "SAPs are code libraries"

**Wrong**: SAP-004 is a pytest library

**Right**: SAP-004 is documentation + patterns for using pytest. The pytest library is installed separately (`pip install pytest`).

**SAPs contain**:
- Documentation (how to use a capability)
- Patterns (best practices, file structures)
- Configuration examples (pyproject.toml snippets)

**SAPs do NOT contain**:
- Executable code (no Python packages)
- Binary dependencies
- Installable libraries

### Misconception 3: "One SAP = One technology"

**Wrong**: SAP-004 is pytest, SAP-005 is GitHub Actions (1:1 mapping)

**Right**: SAPs often combine multiple technologies:
- **SAP-004** includes: pytest + pytest-cov + pytest-mock + fixtures + parametrization
- **SAP-005** includes: GitHub Actions + pytest integration + linting + deployment

**SAPs are capabilities**, not individual tools.

### Misconception 4: "Must adopt all SAPs"

**Wrong**: Need all 29 SAPs for chora-base to work

**Right**: Adopt only SAPs relevant to your project needs. Even adopting just SAP-000 is valuable (understanding the framework).

**Analogy**: SAPs are like a cookbook - you don't cook every recipe, just the ones you need.

### Misconception 5: "SAPs are chora-base specific"

**Wrong**: SAPs only work in chora-base projects

**Right**: SAPs are **general-purpose patterns**. You can adopt SAP-004 (testing-framework) in any Python project, not just chora-base.

**Portability**: Read a SAP's adoption-blueprint.md and apply patterns to your project, regardless of whether it started from chora-base template.

---

## Summary

**SAPs are**:
- Self-contained, reusable capability packages
- Standardized documentation (5-7 artifacts)
- AI-aware (AGENTS.md, CLAUDE.md)
- Lifecycle-managed (draft → pilot → active)
- Catalog-driven (sap-catalog.json)

**SAPs are NOT**:
- Installable code packages
- Single-tool wrappers
- chora-base-specific
- Required to use together

**Key Takeaways**:
1. Every SAP follows SAP-000 specification (5-7 artifacts)
2. SAPs exist at `docs/skilled-awareness/{name}/` (not `SAP-XXX-name/`)
3. SAP sets provide curated bundles for specific use cases
4. Adoption has three tiers: Essential → Recommended → Advanced
5. chora-base includes 29 pre-installed SAPs as documentation + patterns

**Next Steps**:
- [Quickstart: Generic AI Agent](../how-to/quickstart-generic-ai-agent.md) - Explore all 29 SAPs (15 min)
- [Quickstart: Claude Code](../how-to/quickstart-claude.md) - Claude-optimized exploration (12 min)
- [SAP Framework Protocol](../../skilled-awareness/sap-framework/protocol-spec.md) - Complete SAP-000 specification
- [SAP Catalog](/sap-catalog.json) - Machine-readable registry of all SAPs

---

**Version**: 1.0.0
**Last Updated**: 2025-11-05
**Category**: Explanation (Diataxis)
**Reading Time**: 10-15 minutes
