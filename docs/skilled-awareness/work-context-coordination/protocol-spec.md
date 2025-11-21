# Protocol Specification: Work Context Coordination

**Capability ID**: chora.coordination.work_context
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-20

---

## Overview

This document specifies the lightweight pilot protocol for work context coordination. Full API specification (REST/MCP) will be added in Phase 2 (capability server implementation).

---

## Work Context Registry Format

### File: `.chora/work-contexts.yaml`

**Location**: Repository root (e.g., `packages/chora-base/.chora/work-contexts.yaml`)

**Schema**:

```yaml
work_contexts:
  - id: string              # Unique context identifier (tab-1, alice, session-morning)
    type: enum              # "tab" | "dev" | "session"
    branch: string          # Current git branch
    files: list[string]     # File patterns (glob syntax)
    started_at: datetime    # ISO 8601 timestamp
    last_activity: datetime # ISO 8601 timestamp (optional, for future real-time tracking)
```

**Example**:

```yaml
work_contexts:
  - id: tab-1
    type: tab
    branch: tab1/feat/work-context-coordination
    files:
      - "docs/skilled-awareness/work-context-coordination/*.md"
      - "scripts/who-is-working-on.sh"
      - "justfile"
    started_at: "2025-11-20T15:00:00Z"
    last_activity: "2025-11-20T15:30:00Z"

  - id: tab-2
    type: tab
    branch: tab2/feat/sap-053-phase4
    files:
      - "docs/skilled-awareness/conflict-resolution/*.md"
      - "static-template/scripts/conflict-checker.py"
      - "justfile"
    started_at: "2025-11-20T14:45:00Z"
    last_activity: "2025-11-20T15:28:00Z"

  - id: alice
    type: dev
    branch: alice/feat/authentication
    files:
      - "src/auth/*.ts"
      - "tests/auth/*.test.ts"
    started_at: "2025-11-20T10:00:00Z"
```

---

## CLI Interface (Justfile Recipes)

### `just work-context-register ID TYPE BRANCH FILES`

**Purpose**: Register new work context

**Arguments**:
- `ID`: Unique identifier (tab-1, alice, etc.)
- `TYPE`: Context type (tab, dev, session)
- `BRANCH`: Git branch name
- `FILES`: Comma-separated file patterns (glob syntax)

**Example**:
```bash
just work-context-register tab-1 tab tab1/feat/x "docs/*.md,scripts/*.py"
```

**Behavior**: Appends context to `.chora/work-contexts.yaml`

---

### `just work-dashboard`

**Purpose**: Show active work contexts and conflict zones

**Output Format**:
```
Active Work Contexts:
  tab-1 (tab): docs/skilled-awareness/work-context-coordination/*.md, scripts/who-is-working-on.sh, justfile
  tab-2 (tab): docs/skilled-awareness/conflict-resolution/*.md, static-template/scripts/conflict-checker.py, justfile

Conflict Zones:
  ⚠️  justfile (tab-1 + tab-2) - Coordinate before editing
```

**Exit Code**:
- 0: No conflicts detected
- 1: Conflicts detected (for CI/CD integration)

---

### `just who-is-working-on FILE`

**Purpose**: Query which context is editing specific file

**Arguments**:
- `FILE`: File path (supports glob patterns)

**Example**:
```bash
just who-is-working-on justfile
# Output: tab-1 (tab), tab-2 (tab)

just who-is-working-on "docs/INDEX.md"
# Output: No context editing docs/INDEX.md
```

**Exit Code**:
- 0: File owned by 1 context
- 1: File owned by multiple contexts (conflict)
- 2: File not owned by any context

---

## Shell Scripts

### `scripts/who-is-working-on.sh`

**Purpose**: Query file ownership from work-contexts.yaml

**Input**: File path (argv[1])
**Output**: List of contexts editing file (JSON or plain text)

**Algorithm**:
```bash
1. Read .chora/work-contexts.yaml
2. For each context:
   a. For each file pattern in context.files:
      - Check if input file matches pattern (glob matching)
      - If match, add context to results
3. Output results
```

---

### `scripts/detect-conflicts.sh`

**Purpose**: Find files edited by multiple contexts

**Input**: None (reads work-contexts.yaml)
**Output**: List of conflicting files

**Algorithm**:
```bash
1. Extract all file patterns from work-contexts.yaml
2. For each file pattern:
   a. Count how many contexts reference it
   b. If count > 1, add to conflict list
3. Output conflict list
```

---

## AGENTS.md Integration

### Multi-Context Coordination Section

**Location**: Any domain AGENTS.md (docs/, scripts/, etc.)

**Template**:

```markdown
## Multi-Context Coordination

This domain supports concurrent work across multiple contexts (tabs, developers, sessions).

### Active Work

<!-- Check .chora/work-contexts.yaml for current state -->
Run `just work-dashboard` to see active contexts and conflict zones.

### Conflict Zones (High Risk)

Files with frequent conflicts requiring coordination:

| File | Risk | Why | Coordination Strategy |
|------|------|-----|----------------------|
| **justfile** | 🔴 HIGH | Shared automation recipes | Check `just work-dashboard` before editing |
| **INDEX.md** | 🟡 MEDIUM | Central index, moderate churn | Communicate before major updates |
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

## Future Capability Server API (Phase 2)

When chora-coordination capability server is implemented:

### REST API Endpoints

```
POST   /api/v1/contexts/register       # Register work context
GET    /api/v1/contexts/active         # List active contexts
GET    /api/v1/contexts/{id}           # Get context details
DELETE /api/v1/contexts/{id}           # Unregister context
GET    /api/v1/conflicts                # Get conflict zones
GET    /api/v1/file-owner?file={path}  # Query file ownership
```

### MCP Tools

```
work-context-register(id, type, branch, files)     # Register context
work-context-list()                                # List contexts
who-is-working-on(file)                            # Query file owner
detect-conflicts()                                 # Get conflict zones
```

### CLI Commands

```bash
chora-coordination register --id tab-1 --type tab --branch main --files "*.md"
chora-coordination list
chora-coordination conflicts
chora-coordination who-is-working-on justfile
```

---

## Validation

### Test Scenarios

**Scenario 1: Single Tab (No Conflicts)**
```bash
just work-context-register tab-1 tab tab1/feat/x "docs/*.md"
just work-dashboard
# Expected: 1 context, 0 conflicts
```

**Scenario 2: Two Tabs (No Overlap)**
```bash
just work-context-register tab-1 tab tab1/feat/x "docs/*.md"
just work-context-register tab-2 tab tab2/feat/y "scripts/*.py"
just work-dashboard
# Expected: 2 contexts, 0 conflicts
```

**Scenario 3: Two Tabs (Conflict on justfile)**
```bash
just work-context-register tab-1 tab tab1/feat/x "docs/*.md,justfile"
just work-context-register tab-2 tab tab2/feat/y "scripts/*.py,justfile"
just work-dashboard
# Expected: 2 contexts, 1 conflict (justfile)
```

**Scenario 4: Query File Ownership**
```bash
just who-is-working-on justfile
# Expected: tab-1, tab-2 (conflict detected)

just who-is-working-on "docs/INDEX.md"
# Expected: tab-1
```

---

**Status**: Pilot specification (lightweight implementation)
**Next Version**: v2.0.0 will include REST/MCP/CLI capability server specification
**Last Updated**: 2025-11-20
