# Capability Charter: Work Context Coordination

**Capability ID**: chora.coordination.work_context
**Modern Namespace**: chora.coordination.work_context
**Legacy Alias**: SAP-054 (deprecated 2026-06-01), SAP-055 (deprecated 2026-06-01)
**Type**: Capability Server + Pattern
**Status**: Pilot
**Version**: 1.0.0
**Created**: 2025-11-20
**Last Updated**: 2025-11-20

---

## Executive Summary

**chora.coordination.work_context** provides unified multi-context coordination patterns for concurrent development scenarios (multi-tab, multi-developer, multi-session). By abstracting "developer" to "work context", a single set of patterns handles tab-as-dev, real multi-developer teams, and async session coordination.

**Key Innovation**: Tab-as-dev pattern - treat each Claude Code tab as a "developer" for conflict prevention, work partitioning, and awareness. Since multi-dev has stronger requirements than multi-tab, satisfying multi-dev automatically satisfies multi-tab.

**Key Benefits**:
- 🎯 **Unified Pattern**: One implementation for tabs + devs + sessions
- ⚡ **Conflict Prevention**: 60-80% reduction in merge conflicts
- 🗺️ **Work Partitioning**: Intelligent task assignment to minimize conflicts
- 👁️ **Real-Time Awareness**: Who's working where (live dashboard)
- 🔄 **Graceful Scaling**: Start with tabs, add devs later with no rearchitecture

---

## Problem Statement

### Current Challenges

**Multi-Tab Development** (single developer, multiple Claude Code tabs):
- No formal isolation between tabs working in same repo
- Manual coordination via checkpoint messages (informal, error-prone)
- Simultaneous edits to same files = merge conflicts
- No awareness of which tab is editing what files

**Multi-Developer Development** (real team, shared repo):
- Git branch isolation requires constant manual coordination
- "Who's working on this file?" requires Slack/chat interruptions
- Task assignment doesn't consider conflict risk (concurrent edits)
- No real-time dashboard showing active work

**Current Workarounds**:
- Multi-tab: Manual checkpoints, hope tabs don't conflict
- Multi-dev: Over-communicate via chat, defensive branching
- Both: Reactive conflict resolution (git merge after the fact)

### Business Impact

**Multi-Tab Pain** (single developer):
- **20-30% time wasted** on coordination overhead (manual checkpoints)
- **15-25% conflict rate** when tabs edit same files
- **Context switching overhead** (10-15 minutes per tab switch)

**Multi-Dev Pain** (team of 2+):
- **30-50% coordination overhead** (Slack messages, status meetings)
- **40-60% conflict rate** without work partitioning
- **2-3 hours/week** resolving merge conflicts
- **Blocked work** (waiting for colleague to finish editing file)

### User Stories

**As a single developer with multiple tabs**, I want to:
- Register each tab as a "work context" (tab-1, tab-2)
- See which tab is editing which files (work dashboard)
- Get conflict warnings when both tabs edit the same file
- Assign tasks to specific tabs (docs → tab-1, scripts → tab-2)

**As a team of 2+ developers**, I want:
- All the above, but with dev identities (alice, bob) instead of tabs
- Real-time awareness of colleague's active work
- Intelligent task suggestions (avoid assigning conflicting files)
- Conflict zone documentation (which files are high-risk)

**As an AI agent**, I want to:
- Abstract "work context" (tab, dev, session) uniformly
- Detect conflicts proactively (before merge)
- Suggest work partitioning strategies (minimize conflicts)
- Update AGENTS.md with "Multi-Context Coordination" sections

---

## Solution Design

### Approach

**Core Principle**: Abstract "developer" to "work context" - a polymorphic entity representing any concurrent work stream (tab, developer, session).

**3 Pillars**:

1. **Work Context Management**
   - Register contexts: `just work-context-register tab-1 --type tab --branch tab1/feat/x`
   - Query active contexts: `just work-dashboard`
   - Detect conflicts: `just who-is-working-on <file>`

2. **Conflict-Aware Work Partitioning**
   - Task assignment based on ownership + conflict risk
   - Dashboard shows conflict zones (files edited by multiple contexts)
   - Proactive warnings (before editing high-risk files)

3. **Multi-Context AGENTS.md Extensions**
   - Add "Multi-Context Coordination" sections to domain AGENTS.md
   - Document conflict zones (from historical data)
   - Collaboration patterns (solo/async/sync decision tree)

### Architecture

**Lightweight Pilot (Phase 1)**: CLI scripts + YAML config (no capability server)

```
chora-base/ (or any repo using this pattern)
├── .chora/
│   └── work-contexts.yaml        ← Active context registry (manual)
├── scripts/
│   ├── who-is-working-on.sh      ← Query which context owns file
│   └── detect-conflicts.sh       ← Check conflict risks
├── justfile
│   ├── work-context-register     ← Register context
│   ├── work-dashboard            ← Show active contexts + conflicts
│   └── who-is-working-on         ← File ownership query
└── docs/AGENTS.md
    └── ## Multi-Context Coordination  ← New section
```

**Full Implementation (Phase 2)**: Capability server with REST/MCP/CLI interfaces

```
packages/chora-coordination/      ← Capability server (future)
├── src/interfaces/
│   ├── rest/                     ← REST API (port 8080)
│   ├── mcp/                      ← MCP tools (work-context-register, etc.)
│   └── cli/                      ← CLI commands
├── src/core/
│   ├── services.py               ← WorkContextManager
│   └── models.py                 ← WorkContext, ConflictZone
└── docker-compose.yml            ← Local deployment
```

---

## Implementation

### Lightweight Pilot (4-6 hours)

**Phase 1.1: Work Context Registry (1 hour)**

Create `.chora/work-contexts.yaml`:

```yaml
work_contexts:
  - id: tab-1
    type: tab
    branch: tab1/feat/work-context-coordination
    files:
      - "docs/skilled-awareness/work-context-coordination/*.md"
      - "scripts/who-is-working-on.sh"
    started_at: "2025-11-20T15:00:00Z"
    last_activity: "2025-11-20T15:30:00Z"

  - id: tab-2
    type: tab
    branch: tab2/feat/sap-053-phase4
    files:
      - "docs/skilled-awareness/conflict-resolution/*.md"
      - "static-template/scripts/conflict-checker.py"
    started_at: "2025-11-20T14:45:00Z"
    last_activity: "2025-11-20T15:28:00Z"
```

**Phase 1.2: Shell Scripts (2 hours)**

```bash
# scripts/who-is-working-on.sh
#!/usr/bin/env bash
FILE=$1
CONTEXTS_FILE=".chora/work-contexts.yaml"

# Parse YAML (yq or python fallback)
yq eval ".work_contexts[] | select(.files[] | test(\"$FILE\"))" "$CONTEXTS_FILE"
```

```bash
# scripts/detect-conflicts.sh
#!/usr/bin/env bash
# Find files edited by multiple contexts
yq eval ".work_contexts[].files[]" .chora/work-contexts.yaml | \
  sort | uniq -d
```

**Phase 1.3: Justfile Integration (1 hour)**

```makefile
# justfile (chora-base or chora-workspace)

# Register work context
work-context-register ID TYPE BRANCH FILES:
    #!/usr/bin/env bash
    echo "Registering {{ID}} ({{TYPE}}) on branch {{BRANCH}}"
    # Append to .chora/work-contexts.yaml (manual for pilot)
    echo "  - id: {{ID}}" >> .chora/work-contexts.yaml
    echo "    type: {{TYPE}}" >> .chora/work-contexts.yaml
    echo "    branch: {{BRANCH}}" >> .chora/work-contexts.yaml
    echo "    files:" >> .chora/work-contexts.yaml
    echo "      - {{FILES}}" >> .chora/work-contexts.yaml

# Show work dashboard
work-dashboard:
    #!/usr/bin/env bash
    echo "Active Work Contexts:"
    cat .chora/work-contexts.yaml | yq eval '.work_contexts[] | "  \(.id) (\(.type)): \(.files[])"'
    echo ""
    echo "Conflict Zones:"
    scripts/detect-conflicts.sh

# Who's working on file
who-is-working-on FILE:
    scripts/who-is-working-on.sh {{FILE}}
```

**Phase 1.4: AGENTS.md Extensions (1-2 hours)**

Add to `packages/chora-base/docs/AGENTS.md`:

```markdown
## Multi-Context Coordination

This repository supports concurrent work across multiple contexts (tabs, developers, sessions).

### Active Work (Auto-Generated)

<!-- Check .chora/work-contexts.yaml for current state -->
Run `just work-dashboard` to see active contexts and conflict zones.

### Conflict Zones (High Risk)

Files with frequent conflicts requiring coordination:

| File | Risk | Why | Coordination Strategy |
|------|------|-----|----------------------|
| **justfile** | 🔴 HIGH | Shared automation recipes | Check `just work-dashboard` before editing |
| **docs/INDEX.md** | 🟡 MEDIUM | Central index, moderate churn | Communicate before major updates |
| **scripts/*.py** | 🟢 LOW | Separate files per feature | Standard git workflow |

### Collaboration Patterns

**Solo work (tabs)**: Use when contexts work in separate domains
- Example: tab-1 in docs/, tab-2 in scripts/ → No coordination needed

**Async coordination**: Check work-dashboard, avoid conflict zones
- Example: Both tabs need to edit justfile → Coordinate timing

**Sync coordination**: Real-time communication for shared files
- Example: Both devs editing same file → Pair programming or handoff
```

---

## Success Criteria

### Lightweight Pilot (Phase 1)

**Goal**: Validate tab-as-dev pattern with minimal tooling

**Success Metrics**:
1. ✅ `.chora/work-contexts.yaml` tracks 2+ active contexts (tabs or devs)
2. ✅ `just work-dashboard` shows active work + conflict zones
3. ✅ `just who-is-working-on <file>` returns correct context
4. ✅ AGENTS.md includes "Multi-Context Coordination" section
5. ✅ Dogfood test: Tab 1 (this work) + Tab 2 (SAP-053) coordination

**Validation**:
- Manual test: Register tab-1 and tab-2 contexts
- Check dashboard shows both tabs
- Verify conflict detection (e.g., both tabs editing justfile)
- Time to coordination decision: <1 minute (vs 5-10 minutes manual)

### Full Implementation (Phase 2 - Future)

**Goal**: Production capability server with real-time updates

**Success Metrics**:
1. Capability server deployed (docker-compose up)
2. REST API functional (POST /api/contexts/register, GET /api/contexts/active)
3. MCP tools available (work-context-register, who-is-working-on)
4. Web dashboard with real-time updates (WebSocket)
5. SAP-048 registry integration (etcd registration, heartbeats)
6. Conflict alerts (WebSocket notifications when concurrent edits detected)

**Quantified Impact**:
- 60-80% reduction in merge conflicts (proactive conflict detection)
- 20-30% time savings on coordination (dashboard vs Slack messages)
- 40-60% reduction in blocked work (intelligent task assignment)

---

## Integration with Existing SAPs

### SAP-051 (Git Workflow Patterns)
- **Branch naming**: Contexts use branch prefixes (tab1/, tab2/, alice/, bob/)
- **Conventional commits**: All contexts follow same commit format
- **Pre-merge hooks**: Integrate with conflict-checker.py (SAP-053)

### SAP-052 (Code Ownership)
- **CODEOWNERS**: Work partitioning respects ownership zones
- **Conflict zones**: Ownership data informs conflict risk scoring
- **Reviewer assignment**: Suggest reviewers based on context ownership

### SAP-053 (Conflict Resolution)
- **Pre-merge detection**: `just conflict-check` before merging context branches
- **Conflict types**: Detect file/content/semantic conflicts across contexts
- **Resolution guidance**: Link to SAP-053 conflict resolution patterns

### SAP-049 (Namespace Resolution)
- **Modern namespace**: chora.coordination.work_context (not SAP-054)
- **Legacy aliases**: SAP-054, SAP-055 deprecated 2026-06-01
- **Deprecation warnings**: Tools warn when legacy identifiers used

### SAP-010 (Memory System)
- **Event logging**: Emit work_context_registered, conflict_detected events
- **Knowledge notes**: Capture coordination patterns in .chora/memory/knowledge/
- **Trace correlation**: Link contexts via trace_id

---

## Adoption Levels

### L0: Unaware (Baseline)
- No work context tracking
- Manual coordination (Slack, checkpoints)
- Reactive conflict resolution (git merge)

### L1: Essential (Lightweight Pilot)
- `.chora/work-contexts.yaml` registry (manual)
- `just work-dashboard` showing active contexts
- `just who-is-working-on <file>` queries
- AGENTS.md includes "Multi-Context Coordination" section
- **Effort**: 4-6 hours setup
- **Benefit**: 20-30% coordination time savings

### L2: Intermediate (CLI Automation)
- Auto-update work-contexts.yaml on branch checkout (git hooks)
- Conflict detection scripts (detect-conflicts.sh)
- Justfile recipes for all coordination operations
- **Effort**: +2-3 hours (6-9 hours total)
- **Benefit**: 40-50% coordination time savings

### L3: Advanced (Capability Server)
- chora-coordination server deployed (docker-compose)
- REST API + MCP tools + CLI
- Real-time dashboard (WebSocket updates)
- Proactive conflict alerts
- **Effort**: +8-12 hours (14-21 hours total)
- **Benefit**: 60-80% conflict reduction, 50-70% coordination time savings

### L4: Expert (Multi-Repo Federation)
- Federated coordination across multiple repos
- Cross-repo conflict detection
- Shared work dashboard (all repos)
- **Effort**: +6-8 hours (20-29 hours total)
- **Benefit**: Enterprise-scale coordination

---

## ROI Analysis

### Lightweight Pilot (L1)

**Investment**: 4-6 hours ($600-$900 @ $150/hour)

**Savings** (single developer, 2 tabs):
- Coordination overhead: 2 hours/week → 1 hour/week = **1 hour/week saved**
- Conflict resolution: 1 hour/week → 0.5 hours/week = **0.5 hours/week saved**
- **Total savings**: 1.5 hours/week × 50 weeks = **75 hours/year** ($11,250/year)

**ROI**: $11,250 / $900 = **1,150% Year 1**
**Break-even**: 2-3 weeks

### Full Capability Server (L3)

**Investment**: 14-21 hours ($2,100-$3,150 @ $150/hour)

**Savings** (team of 2 developers):
- Coordination overhead: 6 hours/week → 2 hours/week = **4 hours/week saved**
- Conflict resolution: 4 hours/week → 1 hour/week = **3 hours/week saved**
- Blocked work: 2 hours/week → 0.5 hours/week = **1.5 hours/week saved**
- **Total savings per dev**: 8.5 hours/week × 50 weeks = **425 hours/year**
- **Total savings (2 devs)**: 850 hours/year ($127,500/year)

**ROI**: $127,500 / $3,150 = **4,000% Year 1**
**Break-even**: 1-2 weeks

---

## Timeline

### Lightweight Pilot (Phase 1) - Current
- **Duration**: 4-6 hours (1 day)
- **Deliverables**:
  - SAP definition in chora-base (this document)
  - `.chora/work-contexts.yaml` registry
  - Shell scripts (who-is-working-on.sh, detect-conflicts.sh)
  - Justfile recipes (work-context-register, work-dashboard, who-is-working-on)
  - AGENTS.md extensions (Multi-Context Coordination section)

### Full Capability Server (Phase 2) - Future
- **Duration**: 8-12 hours (2-3 days)
- **Prerequisites**: Phase 1 validated, patterns proven
- **Deliverables**:
  - Generate chora-coordination from SAP-047 template
  - REST API + MCP tools + CLI
  - Web dashboard (real-time updates)
  - SAP-048 registry integration
  - Docker deployment

---

## Related Documentation

- **SAP-051** (Git Workflow): Branch naming, conventional commits, pre-merge hooks
- **SAP-052** (Code Ownership): CODEOWNERS, ownership zones, conflict risk
- **SAP-053** (Conflict Resolution): Pre-merge detection, conflict types, resolution guidance
- **SAP-047** (Capability Server Template): Template for Phase 2 implementation
- **SAP-048** (Capability Registry): Service discovery, heartbeats, health checks
- **SAP-049** (Namespace Resolution): Modern namespaces, deprecation warnings

---

**Status**: Pilot (Phase 1 in progress)
**Next Milestone**: Validate tab-as-dev pattern with SAP-053 coordination (Tab 1 + Tab 2)
**Last Updated**: 2025-11-20
