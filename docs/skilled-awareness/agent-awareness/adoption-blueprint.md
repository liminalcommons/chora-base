# Adoption Blueprint: Agent Awareness

**SAP ID**: SAP-009
**Version**: 2.1.0
**Last Updated**: 2025-11-10

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

### Step 3: Assess File Size and Plan Structure (v2.1.0)

**Check current or projected size**:
```bash
wc -l AGENTS.md CLAUDE.md
# Calculate token estimate: lines × 5.6 avg tokens/line
```

**Decision Tree**:
- **<500 lines**: Single file (optimal) - Skip to Step 4
- **500-1,000 lines**: Monitor, prepare for potential split - Continue to Step 4
- **1,000-2,000 lines**: Should split (warning zone) - Proceed to Step 3a
- **>2,000 lines**: Must split immediately (critical zone) - Proceed to Step 3a

**Step 3a: If Splitting Needed** (files >1,000 lines)

**1. Identify distinct domains**:
- What are the major topic areas in your project?
- What content clusters together naturally?
- What workflows/processes are critical and frequently missed?

**2. Recommended domain taxonomy**:
- `/workflows/` or `/dev-process/` - Development workflows, sprint processes
- `/saps/` - SAP catalog and quick references (if applicable)
- `/features/` - Feature-specific patterns
- `/integrations/` - Integration patterns
- `/getting-started/` - Onboarding guides
- Custom domains as needed

**3. Create nested directory structure**:
```bash
mkdir -p workflows/
mkdir -p saps/
mkdir -p features/
```

**4. Extract domain-specific content** to nested files:
- Keep each nested file <500-800 lines
- Maintain clear navigation links between files
- Use "Nearest File Wins" principle

**5. Add "Critical Workflows" section** to root file:
- Location: Immediately after project overview (lines 20-100)
- Include 3-5 most frequently-missed workflows
- Provide quick reference + links to full details
- Use "⚠️" emoji for visibility

**6. Update frontmatter** in root files:
```yaml
---
nested_structure: true
nested_files:
  - "workflows/AGENTS.md"
  - "saps/AGENTS.md"
  - "features/AGENTS.md"
---
```

**7. Validate structure**:
```bash
# Check links are not broken
python scripts/validate-awareness-links.sh

# Verify file sizes
wc -l AGENTS.md */AGENTS.md
# Root should be <1,000 lines
# Nested should be <800 lines each
```

**See**: [awareness-guide.md Section 4](awareness-guide.md#4-when-to-split-awareness-files) for complete splitting strategy and evidence from chora-workspace

### Step 4: Create Nested Files (Optional - if not done in Step 3)

**For domains with complex guidance** (and files <1,000 lines):
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
- **2.1.0** (2025-11-10): Added Step 3 (Assess File Size and Plan Structure) - file size thresholds, splitting decision tree, domain taxonomy, Critical Workflows pattern, validation steps (COORD-2025-012)
- **1.0.0** (2025-10-28): Initial adoption blueprint
