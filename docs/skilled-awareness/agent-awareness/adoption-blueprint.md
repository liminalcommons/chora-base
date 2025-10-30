# Adoption Blueprint: Agent Awareness

**SAP ID**: SAP-009
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides creating AGENTS.md and CLAUDE.md files for your project.

**Time Estimate**: 15-20 minutes for root files, 5-10 min per nested file

---

## 2. Installing the SAP

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-009 --source /path/to/chora-base
```

**What This Installs**:
- agent-awareness capability documentation (5 artifacts)
- AGENTS.md and CLAUDE.md templates
- Example nested awareness files

### Part of Sets

This SAP is included in:
- minimal-entry
- recommended
- full
- mcp-server

To install a complete set:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/agent-awareness/*.md
ls AGENTS.md CLAUDE.md
```

---

## 3. Quick Start

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
- [AGENTS.md](/AGENTS.md) - This file
- [tests/AGENTS.md](/AGENTS.md) - Testing
- [scripts/AGENTS.md](/AGENTS.md) - Scripts

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
See [root AGENTS.md](/AGENTS.md) for project overview.

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

## 7. Update Project AGENTS.md (Post-Install Awareness Enablement)

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the Agent Awareness capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover AGENTS.md and CLAUDE.md structure
- Quick reference for awareness patterns
- Links to awareness documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Agent Awareness

AGENTS.md and CLAUDE.md files providing AI-optimized project navigation.

**Documentation**: [docs/skilled-awareness/agent-awareness/](docs/skilled-awareness/agent-awareness/)

**Quick Start**:
- Read: [adoption-blueprint.md](docs/skilled-awareness/agent-awareness/adoption-blueprint.md)
- Guide: [awareness-guide.md](docs/skilled-awareness/agent-awareness/awareness-guide.md)

**Key Files**:
- Root AGENTS.md: Project overview and capabilities
- Root CLAUDE.md: Context window management
- Nested AGENTS.md: Domain-specific guidance
```

**Validation**:
```bash
grep "Agent Awareness" AGENTS.md && echo "✅ AGENTS.md updated"
```

---

## 8. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) - Template
- [CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) - Template

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint
