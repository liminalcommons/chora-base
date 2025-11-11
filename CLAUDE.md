---
nested_structure: true
nested_files:
  - "saps/AGENTS.md"
  - "workflows/AGENTS.md"
  - "getting-started/AGENTS.md"
version: 2.0.0
last_updated: 2025-11-10
claude_compatibility: Sonnet 4.5+
notes: "Claude uses nested AGENTS.md files for domain-specific patterns (AGENTS.md provides guidance applicable to all agents including Claude)"
---

# Chora-Base: Claude Agent Awareness (Root)

**Project**: chora-base
**Version**: 4.11.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-10 (Nested awareness pattern v2.1.0)

---

## ⚠️ Critical Workflows (Read This First!)

**These workflows are frequently missed by Claude. Read carefully before proceeding.**

### 1. Template Source Confusion ⚠️ MOST IMPORTANT

**When**: User says "help me with chora-base" or "set up chora-base"

**Common Mistake**: Claude tries to set up chora-base as a project (pip install, run tests, etc.)

**Correct Action**: chora-base is a TEMPLATE SOURCE, not a project to set up.

**Quick Decision Tree**:
```
User wants to CREATE NEW PROJECT?
  ✅ YES → Use fast-setup script:
    python scripts/create-model-mcp-server.py \
        --name "Project Name" \
        --namespace namespace \
        --output ~/projects/output

  ❌ NO → User is DEVELOPING chora-base template itself
    → Continue reading this file for navigation patterns
```

**Full Details**: [getting-started/CLAUDE.md](getting-started/CLAUDE.md#critical-template-source-decision)

---

### 2. Progressive Context Loading ⚠️ TOKEN OPTIMIZATION

**When**: Starting any task in chora-base

**Common Mistake**: Claude loads entire root CLAUDE.md (2,400+ lines, ~13k tokens) when only need domain-specific guidance.

**Correct Action**: Use 3-phase progressive loading + nested files.

**Quick Reference**:
```
Phase 1 (0-10k tokens): Read root CLAUDE.md (this file) + navigate to domain
Phase 2 (10-50k tokens): Read domain-specific CLAUDE.md (60-70% token savings)
Phase 3 (50-200k tokens): Read full SAP artifacts only if complex task

Example:
Task: "Install SAP-015"
Phase 1: Read root CLAUDE.md (navigate to saps/)
Phase 2: Read saps/CLAUDE.md (SAP-015 quick reference)
Phase 3: Read docs/skilled-awareness/task-tracking/protocol-spec.md (if complex)
```

**Full Details**: [getting-started/CLAUDE.md](getting-started/CLAUDE.md#progressive-context-loading-strategy)

---

### 3. Nested File Navigation ⚠️ "NEAREST FILE WINS"

**When**: Working on domain-specific task

**Common Mistake**: Claude reads only root CLAUDE.md and misses domain-specific patterns in nested CLAUDE.md files.

**Correct Action**: Navigate to nearest CLAUDE.md file for domain expertise.

**Quick Reference**:
```
Navigation Tree:
/CLAUDE.md (you are here)          - Root navigation + critical workflows
├─ saps/CLAUDE.md                  - SAP-specific Claude patterns
├─ workflows/CLAUDE.md             - Development workflow patterns
├─ getting-started/CLAUDE.md       - Onboarding + architecture
├─ scripts/CLAUDE.md               - Script patterns (if exists)
└─ tests/CLAUDE.md                 - Testing patterns (if exists)

Principle: "Nearest file wins" - Read CLAUDE.md closest to code you're working on
```

**Full Details**: [getting-started/CLAUDE.md](getting-started/CLAUDE.md#nested-awareness-pattern)

---

### 4. SAP Status Checking ⚠️ BEFORE RECOMMENDING

**When**: User asks about SAP or Claude recommends SAP

**Common Mistake**: Claude recommends `draft` or `pilot` SAPs as production-ready.

**Correct Action**: Always check SAP status in sap-catalog.json before recommending.

**Quick Reference**:
```bash
# Check SAP status
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status
# Output: "status": "pilot"

# Status meanings:
# - production: Battle-tested, recommend freely
# - pilot: Dogfooding phase, use with caution
# - draft: Experimental, only recommend if explicitly requested
# - deprecated: Don't recommend, suggest alternatives
```

**Full Details**: [saps/CLAUDE.md](saps/CLAUDE.md#sap-status-checking)

---

### 5. Task Tracking Integration ⚠️ MULTI-SESSION WORK

**When**: User asks to continue previous work or track multi-session tasks

**Common Mistake**: Claude doesn't check for beads (SAP-015) to restore context.

**Correct Action**: If SAP-015 adopted, ALWAYS use beads for persistent memory.

**Quick Reference**:
```bash
# Session startup: Find unblocked work
bd ready --json

# Read task details for context
bd show {id} --json

# Update task progress
bd update {id} --status in_progress --assignee claude

# Close when complete
bd close {id} --reason "Completed X"
```

**Full Details**: [workflows/CLAUDE.md](workflows/CLAUDE.md#multi-session-task-tracking)

---

## Quick Start for Claude

This file provides Claude-specific navigation and context loading strategies for the chora-base template repository.

### First-Time Navigation

**New to chora-base?**
1. You're reading the right file (root `CLAUDE.md`)
2. Determine your task domain (see Navigation Tree below)
3. Navigate to appropriate nested `CLAUDE.md` file
4. Use progressive loading (Phase 1 → Phase 2 → Phase 3 only if needed)

**Returning to chora-base?**
1. Check task domain
2. Navigate directly to relevant nested CLAUDE.md
3. Use progressive loading to minimize tokens

---

## What is Chora-Base?

**Chora-base** is a comprehensive template and framework for AI-assisted software development, built around the **SAP (Skilled Awareness Package) framework**.

**Key Features**:
- 📦 **30+ Skilled Awareness Packages (SAPs)**: Modular capabilities
- 🤖 **Agent-First Design**: Built for Claude Code, Claude Desktop
- 📋 **Nested Awareness Pattern**: Progressive context loading
- 🎯 **Production-Ready Templates**: Bootstrap projects in 1-2 minutes
- 🔄 **Coordination Infrastructure**: Inbox, A-MEM, beads

**See**: [getting-started/CLAUDE.md](getting-started/CLAUDE.md) for complete overview

---

## Navigation Tree: Where Should Claude Go?

### Quick Decision Matrix

**Question**: What is the user trying to do?

| User Intent | Navigate To | Purpose |
|-------------|-------------|---------|
| Create new project from template | [getting-started/CLAUDE.md](getting-started/CLAUDE.md) | Fast-setup script guidance |
| Install/adopt SAP | [saps/CLAUDE.md](saps/CLAUDE.md) | SAP-specific Claude patterns |
| Develop chora-base template | [workflows/CLAUDE.md](workflows/CLAUDE.md) | Development workflows |
| Understand architecture | [getting-started/CLAUDE.md](getting-started/CLAUDE.md) | Architecture overview |
| Write/run tests | tests/CLAUDE.md (if exists) | Testing patterns |
| Write scripts | scripts/CLAUDE.md (if exists) | Script patterns |

### Nested File Descriptions

**[getting-started/CLAUDE.md](getting-started/CLAUDE.md)** (Onboarding):
- What is chora-base?
- Architecture overview (SAP framework, nested awareness)
- Quick start guide
- First-time navigation patterns
- Template source decision tree

**[saps/CLAUDE.md](saps/CLAUDE.md)** (SAP Operations):
- SAP-specific Claude patterns
- SAP Quick References (30+ SAPs)
- SAP status checking workflow
- Integration patterns
- JSON output parsing

**[workflows/CLAUDE.md](workflows/CLAUDE.md)** (Development):
- Common Claude Code workflows
- Claude-specific tips and tricks
- Common pitfalls for Claude
- Example Claude sessions
- Multi-session task tracking

---

## Progressive Context Loading Strategy

**Claude should load context in phases to optimize token usage.**

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand task domain and high-level approach

**Read**:
1. This file (`/CLAUDE.md`) - Root navigation
2. Target nested `CLAUDE.md` (e.g., `saps/CLAUDE.md`)

**Output**: Clear understanding of where to find detailed information

**Token Savings**: 60-70% vs reading full root CLAUDE.md

---

### Phase 2: Specification (10-50k tokens)

**Goal**: Load detailed technical specifications for the task

**Read**:
1. Target SAP's `protocol-spec.md` for complete technical details
2. Target SAP's `awareness-guide.md` (or `AGENTS.md`) for operating patterns
3. Related SAPs' `AGENTS.md` if integration needed

**Output**: Complete technical understanding of commands, workflows, APIs

---

### Phase 3: Deep Dive (50-200k tokens)

**Goal**: Understand design rationale and adoption history

**Read**:
1. Target SAP's `capability-charter.md` for problem/solution design
2. Target SAP's `ledger.md` for adoption metrics and feedback
3. Target SAP's `adoption-blueprint.md` if implementing from scratch
4. Source code files as needed

**Output**: Comprehensive understanding for complex implementations

---

## SAP Framework Quick Reference

### What Are SAPs?

**SAPs (Skilled Awareness Packages)** are modular capabilities packaged with 5 standardized artifacts:

1. **Capability Charter** - Problem statement, solution design
2. **Protocol Spec** - Complete technical specification
3. **Awareness Guide** - Operating patterns for agents
4. **Adoption Blueprint** - Step-by-step installation
5. **Ledger** - Adoption tracking, metrics, feedback

**Every SAP follows this pattern**, making capabilities easy to learn and adopt.

### SAP Catalog

**For complete SAP catalog with Claude-specific patterns**, see **[saps/CLAUDE.md](saps/CLAUDE.md)**.

**Most Common SAPs** (quick reference):

| SAP | Name | Status | Claude Pattern |
|-----|------|--------|----------------|
| SAP-000 | sap-framework | production | Read protocol-spec for schema |
| SAP-001 | inbox | production | Use `--json` flags for parsing |
| SAP-003 | project-bootstrap | draft | Fast-setup script workflow |
| SAP-009 | agent-awareness | production | You're using it now! |
| SAP-015 | task-tracking | pilot | `bd ready --json` for context |

**See**: [saps/CLAUDE.md](saps/CLAUDE.md) for all 30+ SAPs

---

## Common Claude Code Workflows

**For complete workflow documentation**, see **[workflows/CLAUDE.md](workflows/CLAUDE.md)**.

**Quick Workflows**:

### Workflow 1: Adopting a SAP

```bash
# 1. Navigate to SAP documentation
ls docs/skilled-awareness/<sap-name>/

# 2. Read adoption blueprint
cat docs/skilled-awareness/<sap-name>/adoption-blueprint.md

# 3. Follow installation steps
# ... (blueprint provides agent-executable commands)

# 4. Validate installation
# ... (blueprint provides validation commands)

# 5. Update project AGENTS.md
vim AGENTS.md  # Add SAP patterns
```

**See**: [workflows/CLAUDE.md](workflows/CLAUDE.md#workflow-1-adopting-a-sap)

### Workflow 2: Multi-Session Task Tracking

```bash
# Session startup: Check for unblocked work
bd ready --json

# Read task details
bd show {id} --json

# Work on task...

# Update progress
bd update {id} --status in_progress

# Close when done
bd close {id} --reason "Completed X"
```

**See**: [workflows/CLAUDE.md](workflows/CLAUDE.md#workflow-4-multi-session-task-tracking)

---

## Claude-Specific Tips

**For complete tips and pitfalls**, see **[workflows/CLAUDE.md](workflows/CLAUDE.md)**.

**Top 5 Tips**:

1. **Use Domain-Level CLAUDE.md Files**: Each domain has Claude-specific patterns (60-70% token savings)

2. **Leverage SAP Integration Patterns**: Many SAPs integrate (SAP-001 + SAP-015, SAP-010 + SAP-015)

3. **Use JSON Output for Programmatic Workflows**: Many CLIs provide `--json` flags for parsing

4. **Respect Progressive Loading**: Don't over-read (Phase 1 → Phase 2 → Phase 3 only if needed)

5. **Check Adoption Status Before Recommending**: Always check `sap-catalog.json` status field

**See**: [workflows/CLAUDE.md](workflows/CLAUDE.md#claude-specific-tips)

---

## Common Pitfalls for Claude

**For complete pitfalls**, see **[workflows/CLAUDE.md](workflows/CLAUDE.md#common-pitfalls-for-claude)**.

**Top 5 Pitfalls**:

1. **Over-Reading Documentation**: Reading all 5 SAP artifacts when only AGENTS.md needed

2. **Ignoring SAP Status**: Recommending `draft` SAPs as production-ready

3. **Not Using Task Tracking**: Losing context between sessions when SAP-015 available

4. **Not Updating AGENTS.md**: Implementing features without updating agent awareness

5. **Broken Link Networks**: Creating awareness files with broken cross-references

**See**: [workflows/CLAUDE.md](workflows/CLAUDE.md#common-pitfalls-for-claude)

---

## Integration with Claude Code vs Claude Desktop

### Claude Code (VSCode Extension)

**Strengths**:
- Direct file system access (Read, Write, Edit tools)
- Shell command execution (Bash tool)
- Git integration
- Multi-file editing workflows

**Recommended SAPs**:
- SAP-015 (task-tracking): Persistent memory across sessions
- SAP-005 (ci-cd-workflows): GitHub Actions integration
- SAP-011 (docker-operations): Container management
- SAP-003 (project-bootstrap): Scaffold new projects

**Patterns**:
- Use beads CLI directly via Bash tool
- Edit AGENTS.md files as you work
- Commit task progress regularly

---

### Claude Desktop (Chat Interface)

**Strengths**:
- Interactive guidance
- Exploratory conversations
- Documentation generation
- Planning and architecture

**Recommended SAPs**:
- SAP-009 (agent-awareness): Navigate documentation
- SAP-027 (dogfooding-patterns): Validate adoption
- SAP-029 (sap-generation): Generate new capabilities
- SAP-001 (inbox): Coordinate across contexts

**Patterns**:
- Use progressive context loading heavily
- Generate plans and documentation
- Provide architectural guidance
- Coordinate multi-session work via inbox

---

## Key Files for Claude

### High-Frequency Files (Read Often)

- `/CLAUDE.md` (this file) - Root navigation + critical workflows
- `sap-catalog.json` - Machine-readable SAP registry
- `AGENTS.md` - Generic agent patterns (complement to CLAUDE.md)
- `docs/skilled-awareness/INDEX.md` - SAP capability index

### Nested CLAUDE.md Files

- [getting-started/CLAUDE.md](getting-started/CLAUDE.md) - Onboarding
- [saps/CLAUDE.md](saps/CLAUDE.md) - SAP operations
- [workflows/CLAUDE.md](workflows/CLAUDE.md) - Development patterns

### Configuration Files

- `.chora/config.yaml` - Chora configuration (if SAP-010 adopted)
- `.beads/config.yaml` - Beads task tracking (if SAP-015 adopted)
- `pyproject.toml` - Python dependencies

### Coordination Files (If SAP-001 Adopted)

- `inbox/coordination/active.jsonl` - Active coordination requests
- `inbox/coordination/archived.jsonl` - Historical requests

---

## Quick Reference Cards

### SAP Status Quick Check

```bash
# Check specific SAP status
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status

# List all SAPs by status
cat sap-catalog.json | jq '.saps[] | select(.status=="production") | .id'
```

### Task Tracking Quick Start

```bash
# If SAP-015 adopted
bd ready --json                    # Find work
bd show {id} --json                # Read details
bd update {id} --status in_progress
bd close {id} --reason "Done"
```

### Validation Quick Commands

```bash
# Quality gates
just pre-merge                     # All gates

# SAP structure
just validate-all-saps             # All SAPs

# Links
bash scripts/validate-awareness-links.sh
```

---

## Related Resources

### Nested CLAUDE.md Files

- [getting-started/CLAUDE.md](getting-started/CLAUDE.md) - Onboarding + architecture
- [saps/CLAUDE.md](saps/CLAUDE.md) - SAP-specific patterns
- [workflows/CLAUDE.md](workflows/CLAUDE.md) - Development workflows

### Key Documents

- [AGENTS.md](AGENTS.md) - Generic agent patterns
- [README.md](README.md) - Project overview
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - SAP protocol

### Documentation Domains

- [docs/user-docs/](docs/user-docs/) - User guides, tutorials
- [docs/dev-docs/](docs/dev-docs/) - Architecture, contributing
- [docs/project-docs/](docs/project-docs/) - Plans, decisions
- [docs/skilled-awareness/](docs/skilled-awareness/) - SAP capabilities

### Tools

- [justfile](justfile) - Unified automation interface
- [scripts/](scripts/) - Automation scripts (25 scripts)
- [.pre-commit-config.yaml](.pre-commit-config.yaml) - Quality gates

---

## Support & Resources

**For Users** (creating projects):
- Start: [README.md](README.md#-start-here-ai-agent-quick-decision-tree)
- Quick Start: [docs/user-docs/quickstart-mcp-server.md](docs/user-docs/quickstart-mcp-server.md)

**For Contributors** (developing template):
- Onboarding: [getting-started/CLAUDE.md](getting-started/CLAUDE.md)
- Workflows: [workflows/CLAUDE.md](workflows/CLAUDE.md)
- Architecture: [docs/dev-docs/ARCHITECTURE.md](docs/dev-docs/ARCHITECTURE.md)

**For SAP Adopters** (installing capabilities):
- SAP Patterns: [saps/CLAUDE.md](saps/CLAUDE.md)
- SAP Index: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
- Specific SAP: `docs/skilled-awareness/<sap-name>/adoption-blueprint.md`

---

## Version History

- **2.0.0** (2025-11-10): Nested awareness pattern v2.1.0
  - Reduced from 2,428 → ~800 lines (67% reduction)
  - Added Critical Workflows section (5 frequently-missed workflows)
  - Created nested structure: saps/, workflows/, getting-started/
  - Frontmatter declares `nested_structure: true`
  - Progressive loading enhanced with 60-70% token savings

- **1.1.0** (2025-11-09): React SAP Excellence Initiative completion
  - Added comprehensive React Development with SAPs section
  - 16 React SAPs categorized and documented
  - Progressive loading strategy for React development
  - Decision trees for provider selection
  - Stack combinations and integration patterns

- **1.0.0** (2025-11-04): Initial root CLAUDE.md for chora-base
  - Complete navigation tree to 4 domains
  - Progressive context loading strategy
  - Claude Code vs Claude Desktop patterns
  - Common workflows and pitfalls
  - SAP catalog quick reference

---

**Next Steps**:
1. Determine your task domain (getting-started, saps, workflows)
2. Navigate to appropriate nested CLAUDE.md file
3. Use progressive loading to minimize tokens (Phase 1 → Phase 2 → Phase 3 only if needed)
4. Follow Critical Workflows at top of this file

Happy navigating! 🚀

---

**Version**: 2.0.0 (nested awareness pattern v2.1.0)
**Last Updated**: 2025-11-10
**Status**: Active
**Line Count**: ~800 lines (reduced from 2,428 lines, 67% reduction)
