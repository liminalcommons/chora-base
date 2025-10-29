# Protocol Specification: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Overview

### Purpose

The agent-awareness capability provides **structured guidance files for AI agents** using AGENTS.md (generic) and CLAUDE.md (Claude-specific) patterns with nested domain-specific awareness.

### Design Principles

1. **Dual-File Pattern** - AGENTS.md (all agents) + CLAUDE.md (Claude optimizations)
2. **Nearest File Wins** - Agents read awareness file nearest to code they're working on
3. **Progressive Loading** - Essential → Extended → Full context phases (manage 200k token budget)
4. **Domain-Specific** - Nested files (tests/AGENTS.md, scripts/AGENTS.md) for focused guidance
5. **Context Optimization** - Token budgets, checkpoint patterns, artifact-first development

---

## 2. File Structure

### 2.1 AGENTS.md Structure

**Purpose**: Generic AI agent guidance (all agents)
**Location**: Project root + nested directories
**Size**: ~900 lines (root), ~200-300 lines (nested)

**Sections**:
1. **Project Overview** - Architecture, key components, strategic context
2. **Development Process** - 8-phase lifecycle, DDD→BDD→TDD workflows
3. **Documentation Structure** - Nested awareness files (nearest file wins)
4. **Repository Structure** - Directory layout, key files
5. **Key Concepts** - Domain concepts, patterns, conventions
6. **Common Tasks** - Add feature, fix bug, write tests, create docs
7. **Testing** - Run tests, check coverage, debug failures
8. **Pull Request Workflow** - Create PR, address reviews, merge
9. **Troubleshooting** - Common issues, error recovery

**Example** (root AGENTS.md):
```markdown
# AGENTS.md

## Project Overview
**My Project** is a Model Context Protocol (MCP) server...

## Development Process
This project follows the 8-phase chora-base lifecycle...

## Documentation Structure (Nearest File Wins)
- [AGENTS.md](/AGENTS.md) - Project overview (this file)
- [tests/AGENTS.md](/AGENTS.md) - Testing guide
- [scripts/AGENTS.md](/AGENTS.md) - Script reference

## Key Concepts
**MCP Protocol**: [Explanation]
**Event Log**: [Explanation]
...
```

### 2.2 CLAUDE.md Structure

**Purpose**: Claude-specific optimizations
**Location**: Project root + nested directories
**Size**: ~450 lines (root), ~150-200 lines (nested)

**Sections**:
1. **Quick Start for Claude** - Reading order, Claude-specific capabilities
2. **Claude Capabilities Matrix** - Strengths per task type
3. **Context Window Management** - Progressive loading (200k tokens)
4. **Artifact-First Development** - When to use artifacts vs inline
5. **Checkpoint Patterns** - Session preservation every 5-10 interactions
6. **Token Budgets** - Budget by task (feature: 15-30k, bug: 5-10k, refactor: 20-40k)
7. **ROI Tracking** - ClaudeROICalculator integration

**Example** (root CLAUDE.md):
```markdown
# CLAUDE.md - Claude-Specific Development Guide

## Quick Start for Claude
1. Read [AGENTS.md](/AGENTS.md) first
2. Read CLAUDE.md (this file) for optimizations

## Context Window Management (200k Tokens)

### Progressive Loading
**Phase 1 (0-10k)**: Essential context (task + relevant files)
**Phase 2 (10-50k)**: Extended context (related modules + tests)
**Phase 3 (50-200k)**: Full context (entire codebase)

### Token Budgets by Task
- Add feature: 15-30k tokens
- Fix bug: 5-10k tokens
- Refactor: 20-40k tokens
```

### 2.3 Nested Awareness Pattern

**Principle**: "Nearest File Wins" - Agents read awareness file closest to code they're editing

**Structure**:
```
project-root/
├── AGENTS.md                    # Generic project guidance (~900 lines)
├── CLAUDE.md                    # Claude optimizations (~450 lines)
├── tests/
│   ├── AGENTS.md                # Testing guide (~250 lines)
│   └── CLAUDE.md                # Claude test patterns (~150 lines)
├── scripts/
│   ├── AGENTS.md                # Script reference (~200 lines)
│   └── CLAUDE.md                # Claude automation (~100 lines)
├── docker/
│   ├── AGENTS.md                # Docker operations (~200 lines)
│   └── CLAUDE.md                # Claude Docker patterns (~100 lines)
└── .chora/memory/
    ├── AGENTS.md                # Memory system (A-MEM) (~300 lines)
    └── CLAUDE.md                # Claude memory usage (~150 lines)
```

**Benefits**:
- Focused guidance (don't read entire project guide for testing)
- Faster context loading (200-300 lines vs 900 lines)
- Domain expertise (testing guide written by testing expert)
- Modularity (update domain guide without changing root)

---

## 3. Context Optimization

### 3.1 Progressive Context Loading

**Phase 1: Essential (0-10k tokens)**
Load immediately at session start:
- Current task definition
- Relevant AGENTS.md section
- Active files (1-3 files working on)
- Recent conversation summary

**Phase 2: Extended (10-50k tokens)**
Load as needed for implementation:
- Related module code
- Test suites for affected components
- Recent git history (git log --oneline -20)
- Related documentation

**Phase 3: Full (50-200k tokens)**
Load for complex refactoring:
- Complete codebase structure
- Full test suite
- All documentation
- Historical decisions

### 3.2 Token Budgets by Task

| Task Type | Token Budget | What to Load |
|-----------|--------------|--------------|
| Add small feature | 15-30k | Essential + relevant module + tests |
| Add major feature | 30-60k | Extended + dependencies + docs |
| Fix bug | 5-10k | Essential + error trace + relevant code |
| Refactor | 20-40k | Extended + affected modules + tests |
| Write docs | 10-20k | Essential + code to document + examples |
| Review PR | 15-25k | Essential + PR diff + related code |

### 3.3 Checkpoint Patterns

**Create checkpoint every 5-10 interactions**:

```markdown
## Claude Session Checkpoint

**Date**: 2025-10-28
**Task**: Add custom error handling to MCP server

**Progress**:
- ✅ Wrote CustomError class (src/utils/errors.py)
- ✅ Added tests (tests/utils/test_errors.py)
- 🔄 Integrating with server.py (in progress)

**Next Steps**:
1. Update server.py to use CustomError
2. Add error handling docs
3. Run full test suite

**Context Loaded** (25k tokens):
- src/utils/errors.py
- tests/utils/test_errors.py
- src/mcp/server.py
- AGENTS.md (error handling section)
```

---

## 4. Content Guidelines

### 4.1 AGENTS.md Content

**DO Include**:
- ✅ Project architecture overview
- ✅ Key concepts and domain terms
- ✅ Development workflow (DDD→BDD→TDD)
- ✅ Common tasks with step-by-step instructions
- ✅ Links to nested awareness files

**DON'T Include**:
- ❌ Claude-specific optimizations (use CLAUDE.md)
- ❌ Complete code examples (link to docs or reference)
- ❌ Implementation details (keep high-level)

### 4.2 CLAUDE.md Content

**DO Include**:
- ✅ Context window management strategies
- ✅ Token budgets by task type
- ✅ Checkpoint patterns
- ✅ Artifact-first development patterns
- ✅ ROI tracking integration

**DON'T Include**:
- ❌ Generic agent guidance (use AGENTS.md)
- ❌ Non-Claude-specific patterns
- ❌ Duplicate AGENTS.md content

### 4.3 Nested File Content

**DO Include**:
- ✅ Domain-specific guidance (testing, scripts, Docker, etc.)
- ✅ Quick reference for domain tasks
- ✅ Links back to root awareness files

**DON'T Include**:
- ❌ Project-wide architecture (in root AGENTS.md)
- ❌ Complete duplication of root content

---

## 5. Integration Patterns

### 5.1 With Documentation Framework (SAP-007)

**Awareness files are documentation**:
- Follow Diataxis principles (AGENTS.md = Reference + How-To)
- Include frontmatter (optional but recommended)
- Link to related docs (user-docs/, dev-docs/)

### 5.2 With Development Lifecycle (SAP-012)

**AGENTS.md references DDD→BDD→TDD workflows**:
- Links to dev-docs/workflows/DDD_WORKFLOW.md
- Links to dev-docs/workflows/BDD_WORKFLOW.md
- Links to dev-docs/workflows/TDD_WORKFLOW.md
- Quick decision trees for agent workflow selection

---

## 6. Related Documents

**SAP-009 Artifacts**:
- [capability-charter.md](capability-charter.md)
- [awareness-guide.md](awareness-guide.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [ledger.md](ledger.md)

**Templates**:
- [blueprints/AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) (~900 lines)
- [blueprints/CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) (~450 lines)

**Examples**:
- [static-template/tests/AGENTS.md](/static-template/tests/AGENTS.md)
- [static-template/scripts/AGENTS.md](/static-template/scripts/AGENTS.md)
- [static-template/docker/AGENTS.md](/static-template/docker/AGENTS.md)

**Related SAPs**:
- [sap-framework/](../sap-framework/) - SAP-000
- [documentation-framework/](../documentation-framework/) - SAP-007

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for agent-awareness
