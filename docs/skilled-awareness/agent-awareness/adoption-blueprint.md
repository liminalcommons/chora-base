# Adoption Blueprint: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides creating AGENTS.md and CLAUDE.md files for your project.

**Time Estimate**: 15-20 minutes for root files, 5-10 min per nested file

---

## 2. Quick Start

### Step 1: Create Root AGENTS.md

**Use template**:
```bash
cp chora-base/blueprints/AGENTS.md.blueprint AGENTS.md
# Replace {{ project_name }} and other variables
```

**Key sections to customize**:
1. **Project Overview** - Your architecture, components
2. **Key Concepts** - Domain-specific terms
3. **Common Tasks** - Add feature, fix bug, write tests

### Step 2: Create Root CLAUDE.md

**Use template**:
```bash
cp chora-base/blueprints/CLAUDE.md.blueprint CLAUDE.md
# Replace {{ project_name }}
```

**Key sections to customize**:
1. **Token Budgets** - Adjust for your project size
2. **Checkpoint Patterns** - Project-specific checkpoints

### Step 3: Create Nested Files (Optional)

**For domains with complex guidance**:
- tests/AGENTS.md - Testing guide (~250 lines)
- scripts/AGENTS.md - Script reference (~200 lines)
- docker/AGENTS.md - Docker operations (~200 lines)

**Content**: Domain-specific quick reference + links to root

---

## 3. AGENTS.md Structure

**Template**:
```markdown
# AGENTS.md

## Project Overview
**My Project** is...

## Development Process
Follows chora-base 8-phase lifecycle...

## Documentation Structure
- [AGENTS.md](AGENTS.md) - This file
- [tests/AGENTS.md](tests/AGENTS.md) - Testing
- [scripts/AGENTS.md](scripts/AGENTS.md) - Scripts

## Key Concepts
**Concept 1**: Explanation
**Concept 2**: Explanation

## Common Tasks
### Add Feature
1. Write docs (DDD)
2. Write tests (BDD/TDD)
3. Implement code

### Fix Bug
1. Reproduce in test
2. Fix code
3. Verify test passes
```

---

## 4. CLAUDE.md Structure

**Template**:
```markdown
# CLAUDE.md

## Context Window Management

### Token Budgets
- Add feature: 20-35k
- Fix bug: 5-12k
- Refactor: 25-45k

### Progressive Loading
**Phase 1 (0-10k)**: Task + files
**Phase 2 (10-50k)**: Related modules
**Phase 3 (50-200k)**: Full codebase

## Checkpoint Pattern
Every 5-10 interactions:
- Task progress
- Next steps
- Context loaded
```

---

## 5. Nested Awareness Files

**When to create**:
- Domain has >5 common tasks
- Domain guide would be >300 lines in root file
- Domain needs specific agent guidance

**Example** (tests/AGENTS.md):
```markdown
# Testing Guide

**For agents working on tests.**
See [root AGENTS.md](../AGENTS.md) for project overview.

## Run Tests
```bash
pytest
pytest --cov=src
```

## Common Testing Tasks
### Add Test
1. Create test_module.py
2. Write test functions
3. Run pytest

### Debug Failing Test
1. Run with -vv flag
2. Check assertion
3. Fix code or test
```

---

## 6. Best Practices

**DO**:
- ✅ Keep root AGENTS.md under 1000 lines
- ✅ Create nested files for complex domains
- ✅ Update awareness files when architecture changes
- ✅ Include links between awareness files

**DON'T**:
- ❌ Duplicate content in root and nested files
- ❌ Include complete code in awareness files (link to docs)
- ❌ Make nested files too long (>400 lines)

---

## 7. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [AGENTS.md.blueprint](../../../../blueprints/AGENTS.md.blueprint) - Template
- [CLAUDE.md.blueprint](../../../../blueprints/CLAUDE.md.blueprint) - Template

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint
