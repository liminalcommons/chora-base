# Chora-Base: Claude Agent Awareness (Root)

**Project**: chora-base
**Version**: 4.10.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-06

---

## ⚠️ CRITICAL: Read This First!

**chora-base is a TEMPLATE SOURCE, not a project to set up.**

### Quick Decision for Claude

**Are you trying to CREATE A NEW PROJECT using chora-base?**

**✅ YES** → Use the fast-setup script (recommended):

```bash
python scripts/create-model-mcp-server.py \
    --name "Your Project Name" \
    --namespace yournamespace \
    --output ~/projects/your-project
```

**What happens**: 1-2 minutes of automated setup creating a fully-configured model citizen MCP server with all chora-base infrastructure (testing, CI/CD, quality gates, beads, inbox, A-MEM, documentation).

**See**: [README.md](README.md#-start-here-ai-agent-quick-decision-tree) or [Quickstart Guide](docs/user-docs/quickstart-mcp-server.md)

---

**Are you DEVELOPING chora-base itself?**

**✅ YES** → Continue reading this file for Claude-specific navigation patterns

---

## Quick Start for Claude

This file provides Claude-specific navigation and context loading strategies for working with the chora-base template repository.

### First-Time Navigation

**New to chora-base?**
1. You're reading the right file (root `CLAUDE.md`)
2. Determine your task domain (see Navigation Tree below)
3. Navigate to the appropriate domain's `AGENTS.md` file
4. Read the domain-specific `CLAUDE.md` for Claude patterns
5. Dive into specific SAP documentation as needed

**Returning to chora-base?**
1. Check your task domain
2. Navigate directly to relevant SAP or documentation
3. Use progressive context loading (see below)

---

## What is Chora-Base?

**Chora-base** is a comprehensive template and framework for AI-assisted software development, built around the **SAP (Skilled Awareness Package) framework**. It provides:

- 📦 **30+ Skilled Awareness Packages (SAPs)**: Modular capabilities for development workflows
- 🤖 **Agent-First Design**: Built for Claude Code, Claude Desktop, and other AI agents
- 📋 **Nested Awareness Pattern**: Progressive context loading via AGENTS.md/CLAUDE.md hierarchy
- 🎯 **Production-Ready Templates**: Bootstrap projects with battle-tested patterns
- 🔄 **Coordination Infrastructure**: Cross-repo inbox, event memory (A-MEM), task tracking (beads)

---

## Architecture Overview

### SAP Framework (SAP-000)

The foundation of chora-base is the **SAP framework**, which packages capabilities into five standardized artifacts:

1. **Capability Charter**: Problem statement, solution design, success criteria
2. **Protocol Spec**: Complete technical specification, commands, workflows
3. **Awareness Guide**: Operating patterns for agents (AGENTS.md or awareness-guide.md)
4. **Adoption Blueprint**: Step-by-step installation guide
5. **Ledger**: Adoption tracking, metrics, feedback, version history

Every SAP follows this pattern, making it easy to learn and adopt new capabilities.

### Nested Awareness Pattern (SAP-009)

Chora-base uses a **5-level nested awareness hierarchy**:

```
/CLAUDE.md                                    ← You are here (Root)
│
├─ docs/skilled-awareness/                    ← Domain: SAP Capabilities
│  ├─ AGENTS.md                               ← Generic agent patterns
│  ├─ CLAUDE.md                               ← Claude-specific patterns
│  │
│  ├─ sap-framework/                          ← SAP-000 (Capability Level)
│  │  ├─ AGENTS.md                            ← SAP-000 patterns
│  │  ├─ capability-charter.md
│  │  ├─ protocol-spec.md
│  │  ├─ awareness-guide.md
│  │  └─ ledger.md
│  │
│  ├─ inbox/                                  ← SAP-001 (Capability Level)
│  │  ├─ AGENTS.md
│  │  ├─ CLAUDE.md
│  │  └─ ... (5 artifacts)
│  │
│  └─ ... (30+ SAPs)
│
├─ docs/dev-docs/                             ← Domain: Developer Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (architecture, contributing, etc.)
│
├─ docs/user-docs/                            ← Domain: User Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (getting started, tutorials, reference)
│
└─ docs/project-docs/                         ← Domain: Project Management
   ├─ AGENTS.md
   ├─ CLAUDE.md
   └─ ... (plans, decisions, retrospectives)
```

**Principle**: "Nearest file wins" - navigate from root → domain → capability → feature → component, progressively loading context as needed.

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand task domain and high-level approach

**Read**:
1. This file (`/CLAUDE.md`) for project overview
2. Target domain's `AGENTS.md` (e.g., `docs/skilled-awareness/AGENTS.md`)
3. Target domain's `CLAUDE.md` for Claude-specific patterns

**Output**: Clear understanding of where to find detailed information

---

### Phase 2: Specification (10-50k tokens)

**Goal**: Load detailed technical specifications for the task

**Read**:
1. Target SAP's `protocol-spec.md` for complete technical details
2. Target SAP's `awareness-guide.md` (or `AGENTS.md`) for operating patterns
3. Related SAPs' `AGENTS.md` files if integration needed

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

## Navigation Tree: Where Should Claude Go?

### Domain 1: User-Facing Documentation

**Path**: [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)

**Use when**:
- User asks "how do I use chora-base?"
- User needs tutorials or getting started guides
- User wants reference documentation
- User is new to chora-base ecosystem

**Contents**:
- Getting started guides
- Tutorials and examples
- Reference documentation
- FAQ and troubleshooting

---

### Domain 2: Developer Documentation

**Path**: [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)

**Use when**:
- Contributing to chora-base
- Understanding chora-base architecture
- Setting up development environment
- Debugging chora-base internals

**Contents**:
- Developer setup
- Architecture documentation
- Contributing guidelines
- Testing and debugging

---

### Domain 3: Project Management Documentation

**Path**: [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

**Use when**:
- User asks about project plans or roadmap
- User wants to understand governance or decisions
- Coordinating work across the project
- Reviewing retrospectives or lessons learned

**Contents**:
- Project plans (like PLAN-2025-11-04-SAP-009-FULL)
- Decision records (ADRs)
- Retrospectives
- Coordination requests

---

### Domain 4: Skilled Awareness (SAP Capabilities)

**Path**: [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)

**Use when**:
- User wants to adopt a specific SAP
- Understanding SAP framework
- Implementing or extending capabilities
- Exploring available SAPs (30+ capabilities)

**Contents**:
- SAP Framework (SAP-000)
- 30+ SAP capabilities
- SAP catalog and index
- Integration patterns

**Key SAPs to Know**:
- **SAP-000** (sap-framework): Foundation for all SAPs
- **SAP-001** (inbox): Cross-repo coordination
- **SAP-009** (agent-awareness): This nested awareness pattern
- **SAP-010** (A-MEM): Agent memory and event tracking
- **SAP-015** (task-tracking): Persistent task management with beads
- **SAP-027** (dogfooding-patterns): How to validate SAPs
- **SAP-029** (sap-generation): Generate new SAPs

---

### Domain 5: Memory System (.chora/)

**Path**: [.chora/AGENTS.md](.chora/AGENTS.md) + [.chora/CLAUDE.md](.chora/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.chora/CLAUDE.md](.chora/CLAUDE.md) - Claude workflows (8-min, ~5k tokens)
- [.chora/AGENTS.md](.chora/AGENTS.md) - Memory patterns (13-min, ~10k tokens)

**Use when**:
- Creating knowledge notes to capture learnings
- Querying event logs for context restoration
- Logging significant events (milestones, decisions, errors)
- Restoring context across sessions (hours, days, or weeks apart)
- Building knowledge graph with wikilink connections

**Contents**:
- Event logging patterns (JSONL format, trace correlation)
- Knowledge note workflows (Zettelkasten-style)
- Agent profile management
- Query template examples
- Context restoration workflows

**Note**: Memory system (`.chora/`) only exists in generated projects, not in chora-base template repository itself.

---

### Domain 6: Task Tracking (.beads/)

**Path**: [.beads/AGENTS.md](.beads/AGENTS.md) + [.beads/CLAUDE.md](.beads/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [.beads/CLAUDE.md](.beads/CLAUDE.md) - Claude beads workflows (7-min, ~5k tokens)
- [.beads/AGENTS.md](.beads/AGENTS.md) - Beads patterns (10-min, ~8k tokens)

**Use when**:
- Restoring context at session startup (finding unblocked work)
- Tracking multi-session work (progress, blockers, dependencies)
- Managing backlog and task prioritization
- Coordinating with other agents or team members
- Creating audit trails for completed work

**Contents**:
- Session startup patterns (`bd ready --json`)
- Task lifecycle workflows (create, update, block, close)
- Query patterns by status/assignee/tags
- Integration with SAP-001 (inbox) and SAP-010 (memory)
- Context restoration workflows

**Note**: Beads (`.beads/`) only exists in generated projects when SAP-015 is adopted, not in chora-base template repository itself.

---

### Domain 7: Inbox Coordination Protocol (inbox/)

**Path**: [docs/skilled-awareness/inbox/AGENTS.md](docs/skilled-awareness/inbox/AGENTS.md) + [docs/skilled-awareness/inbox/CLAUDE.md](docs/skilled-awareness/inbox/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [docs/skilled-awareness/inbox/CLAUDE.md](docs/skilled-awareness/inbox/CLAUDE.md) - Claude inbox workflows (8-min, ~6k tokens)
- [docs/skilled-awareness/inbox/AGENTS.md](docs/skilled-awareness/inbox/AGENTS.md) - Inbox patterns (12-min, ~9k tokens)

**Use when**:
- Creating or responding to coordination requests
- Querying inbox status at session startup
- Generating AI-powered coordination requests
- Managing cross-repo collaboration with formalized SLAs
- Tracking coordination events and ecosystem participation

**Contents**:
- 5 CLI tools (install, query, respond, generate, status)
- Session startup routines and daily workflows
- SLA guidelines (48h default, 4h urgent, 1-week backlog)
- Ecosystem coordination patterns
- Integration with SAP-010 (memory) and SAP-015 (beads)

**Note**: Inbox coordination (SAP-001) is included in chora-base for ecosystem collaboration. Active coordination happens in `inbox/` directory.

---

### Domain 8: Agent Awareness (agent-awareness/)

**Path**: [docs/skilled-awareness/agent-awareness/AGENTS.md](docs/skilled-awareness/agent-awareness/AGENTS.md) + [docs/skilled-awareness/agent-awareness/CLAUDE.md](docs/skilled-awareness/agent-awareness/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [docs/skilled-awareness/agent-awareness/CLAUDE.md](docs/skilled-awareness/agent-awareness/CLAUDE.md) - Claude progressive loading patterns (10-min, ~7k tokens)
- [docs/skilled-awareness/agent-awareness/AGENTS.md](docs/skilled-awareness/agent-awareness/AGENTS.md) - Nested awareness patterns (15-min, ~11k tokens)

**Use when**:
- Understanding the nested AGENTS.md/CLAUDE.md pattern (SAP-009)
- Implementing progressive context loading (200k token management)
- Creating domain-specific awareness files (tests/, scripts/, .chora/)
- Validating awareness structure (7 required sections)
- Optimizing token usage with "nearest file wins" pattern

**Contents**:
- Nested hierarchy pattern (5 levels: root → domain → SAP → feature → component)
- Progressive loading phases (Essential 0-10k, Extended 10-50k, Comprehensive 50-200k)
- Domain-specific awareness examples (tests/, scripts/, .chora/, inbox/)
- Validation workflows (structure, links, token tracking)
- Integration patterns (ALL SAPs use this pattern)

**Progressive Loading Strategy**:
```markdown
Phase 1 (0-10k): Read root AGENTS.md sections 1-2 only
Phase 2 (10-50k): Read root + domain-specific AGENTS.md + CLAUDE.md (60-70% savings)
Phase 3 (50-200k): Read all SAP artifacts (only for complex tasks)
```

**Note**: Agent awareness (SAP-009) is the META-SAP that ALL other SAPs depend on for discoverability. This pattern enables 60-70% token reduction via domain-specific files.

---

### CI/CD Workflows (SAP-005) - Quick Reference

**No domain-specific CLAUDE.md** (workflows are infrastructure, not code)

**Claude patterns for CI/CD**:
```markdown
# Session startup: Check CI status
gh run list --limit 10
just ci-status

# If CI failed: Investigate and fix
gh run view {run_id} --log          # Read logs
just ci-logs {run_id}               # Alternative

# Create bead for tracking (SAP-015)
bd create "Fix test.yml failure" --priority high

# Fix locally BEFORE pushing (SAP-006)
pytest tests/                       # Run tests
ruff check --fix src/ tests/        # Auto-fix linting
mypy src/ tests/                    # Type check

# Push and verify
git push origin branch
gh run list --limit 5               # Verify new run
```

**Progressive loading strategy**:
- **Phase 1**: No loading needed (CI is automated)
- **Phase 2**: Read [.github/workflows/](../.github/workflows/) if debugging CI failures
- **Phase 3**: Read [docs/skilled-awareness/ci-cd-workflows/protocol-spec.md](docs/skilled-awareness/ci-cd-workflows/protocol-spec.md) for workflow specifications

**ROI**: Automated quality gates catch 95%+ preventable issues before merge, <5 min feedback loops

---

## Common Claude Code Workflows

### Workflow 1: Adopting a SAP

```markdown
User: "I want to add task tracking to my project"

Claude:
1. Navigate to docs/skilled-awareness/AGENTS.md
2. Find SAP-015 (task-tracking) in the SAP catalog
3. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
4. Follow step-by-step installation guide
5. Update project AGENTS.md with SAP-015 patterns
```

**Progressive Loading**:
- Phase 1: Read `docs/skilled-awareness/AGENTS.md` + `docs/skilled-awareness/task-tracking/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/task-tracking/protocol-spec.md` + `adoption-blueprint.md`
- Phase 3 (if needed): Read `capability-charter.md` + `ledger.md` for design rationale

---

### Workflow 2: Understanding Chora-Base Architecture

```markdown
User: "How does chora-base work?"

Claude:
1. Read this file (CLAUDE.md) for overview
2. Navigate to docs/dev-docs/CLAUDE.md for developer perspective
3. Read docs/skilled-awareness/sap-framework/protocol-spec.md
4. Review sap-catalog.json for capability inventory
```

**Progressive Loading**:
- Phase 1: Read `/CLAUDE.md` + `docs/dev-docs/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/sap-framework/protocol-spec.md`
- Phase 3 (if deep dive): Read architecture documentation, source code

---

### Workflow 3: Contributing to Chora-Base

```markdown
User: "I want to contribute a new SAP"

Claude:
1. Read docs/dev-docs/AGENTS.md for contributing guidelines
2. Navigate to docs/skilled-awareness/sap-generation/
3. Read SAP-029 adoption-blueprint.md for generation workflow
4. Use SAP templates to scaffold new capability
5. Follow SAP-000 protocol-spec.md for artifact requirements
```

**Progressive Loading**:
- Phase 1: Read `docs/dev-docs/AGENTS.md` + `docs/skilled-awareness/CLAUDE.md`
- Phase 2: Read `docs/skilled-awareness/sap-generation/protocol-spec.md` + `sap-framework/protocol-spec.md`
- Phase 3: Review existing SAPs for examples (e.g., SAP-015)

---

### Workflow 4: Multi-Session Task Tracking

```markdown
User: "Continue working on the feature from yesterday"

Claude:
1. Check if SAP-015 (beads) is adopted: ls .beads/
2. If yes: bd ready --json to find unblocked work
3. Read task details: bd show {id} --json
4. Resume work with full context from task description
```

**Why This Matters**: Beads (SAP-015) provides persistent memory across sessions, eliminating context re-establishment overhead.

---

## Claude-Specific Tips

### Tip 1: Use Domain-Level CLAUDE.md Files

Each domain has a `CLAUDE.md` file with Claude-specific patterns:
- [docs/skilled-awareness/CLAUDE.md](docs/skilled-awareness/CLAUDE.md) - SAP navigation
- [docs/dev-docs/CLAUDE.md](docs/dev-docs/CLAUDE.md) - Development workflows
- [docs/user-docs/CLAUDE.md](docs/user-docs/CLAUDE.md) - User documentation tips
- [docs/project-docs/CLAUDE.md](docs/project-docs/CLAUDE.md) - Project navigation

**Always read the domain CLAUDE.md after navigating to a domain.**

---

### Tip 2: Leverage SAP Integration Patterns

Many SAPs integrate with each other:
- **SAP-001 (inbox) + SAP-015 (beads)**: Decompose coordination requests into tasks
- **SAP-010 (A-MEM) + SAP-015 (beads)**: Correlate tasks with event traces
- **SAP-009 (awareness) + all SAPs**: Every SAP uses nested awareness pattern

Look for "Integration with Other SAPs" sections in AGENTS.md files.

---

### Tip 3: Use JSON Output for Programmatic Workflows

Many SAP CLIs provide `--json` flags for Claude Code:
- `bd ready --json` (beads task tracking)
- `bd show {id} --json` (task details)
- `bd list --status open --json` (backlog)

Parse JSON in Claude Code sessions for structured data.

---

### Tip 4: Respect Progressive Loading

**Don't over-read**:
- If user asks "what is SAP-015?", read `docs/skilled-awareness/task-tracking/AGENTS.md` (5min), NOT all 5 artifacts (30min)
- Only read `protocol-spec.md` when implementing
- Only read `capability-charter.md` when understanding design rationale

**Do progressive loading**:
- Phase 1: Quick reference (AGENTS.md)
- Phase 2: Implementation (protocol-spec.md, adoption-blueprint.md)
- Phase 3: Deep understanding (capability-charter.md, ledger.md)

---

### Tip 5: Check Adoption Status Before Recommending SAPs

Always check SAP status in `sap-catalog.json` before recommending:
- **production**: Battle-tested, recommend freely
- **pilot**: Dogfooding phase, use with caution
- **draft**: Experimental, only recommend if explicitly requested
- **deprecated**: Don't recommend, suggest alternatives

Example:
```json
{
  "id": "SAP-015",
  "name": "task-tracking",
  "status": "pilot",  ← Pilot phase, validate before broad recommendation
  "version": "1.0.0"
}
```

---

## Key Files for Claude

### High-Frequency Files (Read Often)

- `/CLAUDE.md` (this file) - Root navigation
- `sap-catalog.json` - Machine-readable SAP registry
- `AGENTS.md` (project root) - Quick reference for all agents
- `docs/skilled-awareness/INDEX.md` - SAP capability index

### Configuration Files

- `.chora/config.yaml` - Chora configuration
- `.beads/config.yaml` - Beads task tracking (if SAP-015 adopted)
- `package.json` - npm dependencies
- `pyproject.toml` - Python dependencies

### Coordination Files (If SAP-001 Adopted)

- `inbox/coordination/active.jsonl` - Active coordination requests
- `inbox/coordination/archived.jsonl` - Historical requests
- `inbox/coordination/events.jsonl` - Coordination event log

### Memory Files (If SAP-010 Adopted)

- `.chora/memory/events/*.jsonl` - Event-sourced history
- `.chora/memory/events/development.jsonl` - Development events
- `.chora/memory/events/inbox.jsonl` - Coordination events

### Task Files (If SAP-015 Adopted)

- `.beads/issues.jsonl` - Task source of truth (git-committed)
- `.beads/beads.db` - SQLite cache (gitignored, auto-generated)

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

## Common Pitfalls for Claude

### Pitfall 1: Over-Reading Documentation

**Problem**: Reading all 5 SAP artifacts when only AGENTS.md is needed

**Fix**: Use progressive loading:
- Quick question? Read AGENTS.md only
- Implementation? Read protocol-spec.md + adoption-blueprint.md
- Design rationale? Then read capability-charter.md

---

### Pitfall 2: Ignoring SAP Status

**Problem**: Recommending `draft` SAPs as production-ready

**Fix**: Always check `status` in sap-catalog.json:
```bash
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status
```

---

### Pitfall 3: Not Using Task Tracking

**Problem**: Losing context between sessions, forgetting subtasks

**Fix**: If SAP-015 adopted, ALWAYS use beads:
```bash
bd ready --json                                    # Find work
bd update {id} --status in_progress --assignee me  # Claim
bd close {id} --reason "Completed X"              # Finish
```

---

### Pitfall 4: Not Updating AGENTS.md

**Problem**: Implementing features without updating agent awareness

**Fix**: After implementing a feature, update relevant AGENTS.md:
- Root AGENTS.md for project-wide patterns
- Domain AGENTS.md for domain-specific patterns
- SAP AGENTS.md for capability-specific patterns

---

### Pitfall 5: Broken Link Networks

**Problem**: Creating AGENTS.md/CLAUDE.md files with broken links

**Fix**: After creating awareness files, validate links:
```bash
bash scripts/validate-awareness-links.sh
```

---

## Quick Reference: SAP Catalog

### Core Infrastructure (Adopt First)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-000 | sap-framework | production | Foundation for all SAPs |
| SAP-009 | agent-awareness | production | This nested awareness pattern |
| SAP-001 | inbox | production | Cross-repo coordination |
| SAP-010 | memory-system | production | Event-sourced agent memory |

### Development Workflow

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-003 | project-bootstrap | draft | Scaffold new projects |
| SAP-005 | ci-cd-workflows | production | GitHub Actions automation |
| SAP-011 | docker-operations | production | Container management |
| SAP-015 | task-tracking | pilot | Persistent task memory (beads) |

### SAP Ecosystem

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-027 | dogfooding-patterns | production | Validate SAP adoption |
| SAP-029 | sap-generation | production | Generate new SAPs |
| SAP-028 | publishing-automation | draft | Automated SAP distribution |

### Frontend Development (React Ecosystem)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-016 | link-validation | draft | Reference management |
| SAP-017 | state-management | draft | React state patterns |
| SAP-018 | form-validation | draft | Form handling |
| SAP-026 | ui-component-library | draft | Design system |
| SAP-030 | data-fetching | draft | API integration |
| SAP-031 | routing-navigation | draft | Next.js routing |
| SAP-032 | performance-optimization | draft | React performance |

**Full Catalog**: See [sap-catalog.json](sap-catalog.json) or [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

---

## Example Claude Code Session

```markdown
User: "Help me set up task tracking for this project"

Claude (Phase 1: Orientation):
- Read /CLAUDE.md (this file) for project overview
- Navigate to docs/skilled-awareness/AGENTS.md
- Find SAP-015 (task-tracking) in catalog
- Read docs/skilled-awareness/task-tracking/AGENTS.md for quick overview

Claude (Phase 2: Implementation):
- Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
- Follow step-by-step installation:
  1. Install beads CLI: npm install -g @beads/bd
  2. Initialize: bd init
  3. Create first tasks
  4. Update AGENTS.md with beads patterns

Claude (Phase 3: If Needed):
- Read protocol-spec.md for complete CLI reference
- Read capability-charter.md for design rationale
- Review integration patterns with SAP-001 and SAP-010

Result: SAP-015 successfully adopted, task tracking operational
```

---

## Support & Resources

### Documentation

- **SAP Framework**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- **Agent Awareness**: [docs/skilled-awareness/agent-awareness/](docs/skilled-awareness/agent-awareness/)
- **SAP Catalog**: [sap-catalog.json](sap-catalog.json)
- **SAP Index**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

### Key Commands

```bash
# SAP discovery
cat sap-catalog.json | grep -A 10 '"id": "SAP-'

# Task tracking (if SAP-015 adopted)
bd ready --json
bd list --status open --json

# Coordination (if SAP-001 adopted)
cat inbox/coordination/active.jsonl

# Event history (if SAP-010 adopted)
tail -n 20 .chora/memory/events/development.jsonl
```

### Navigation

- **Need SAP documentation?** → [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)
- **Need developer setup?** → [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)
- **Need user guides?** → [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)
- **Need project plans?** → [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

---

## Version History

- **1.0.0** (2025-11-04): Initial root CLAUDE.md for chora-base
  - Complete navigation tree to 4 domains
  - Progressive context loading strategy
  - Claude Code vs Claude Desktop patterns
  - Common workflows and pitfalls
  - SAP catalog quick reference

---

**Next Steps**:
1. Determine your task domain (user docs, dev docs, project docs, SAPs)
2. Navigate to appropriate domain AGENTS.md
3. Read domain CLAUDE.md for Claude-specific patterns
4. Dive into specific SAP or documentation as needed

**Remember**: "Nearest file wins" - progressively load context from root → domain → capability → feature → component.

Happy navigating! 🚀
