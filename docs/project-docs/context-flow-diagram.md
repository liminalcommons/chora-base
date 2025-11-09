# CHORA_TRACE_ID Context Flow Diagram

**Date**: 2025-11-03
**Type**: Traceability Audit
**Status**: Active
**Impact**: High - Maps end-to-end context propagation across SAP ecosystem

---

## Executive Summary

This diagram maps **CHORA_TRACE_ID** flow across the SAP ecosystem, showing where context propagates automatically (GREEN), manually (YELLOW), or gets lost (RED).

**Key Findings**:
- **Source**: SAP-001 (inbox) generates trace IDs in 3 formats (kebab-case, UUID4, task IDs)
- **Automatic propagation**: SAP-001 → SAP-010 (memory system) via events.jsonl
- **Manual propagation**: SAP-001 → SAP-012 (lifecycle) via agent extraction
- **Context lost**: SAP-013 (metrics), SAP-007 (docs), SAP-005 (CI/CD) don't receive trace IDs

**Recommendation**: Implement GAP-001 (CHORA_TRACE_ID propagation) to enable end-to-end traceability.

---

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CHORA_TRACE_ID Flow Across SAPs                        │
└─────────────────────────────────────────────────────────────────────────────┘

Legend:
  ═══> GREEN automatic propagation
  ──-> YELLOW manual propagation
  ╌╌╌> RED context lost (not implemented)
  [!]  Critical gap

┌─────────────────┐
│   SAP-001       │  SOURCE: Generates trace IDs
│   Inbox         │  - Format: kebab-case, UUID4, task-NNN
│   Coordination  │  - Storage: events.jsonl, task JSON
└────────┬────────┘
         │
         ║ GREEN: Automatic emission on state transitions
         ║ Event schema v1.0 includes trace_id field
         ║
         ▼
┌─────────────────┐
│   SAP-010       │  RECEIVER: Stores & correlates events
│   Memory System │  - Storage: .chora/memory/events/*/traces/{trace_id}.jsonl
│   (A-MEM)       │  - Knowledge notes: related_traces field
└────────┬────────┘
         │
         ║ GREEN: Auto-query by trace_id
         ║ Indirect correlation available
         ║
         ▼
┌─────────────────┐
│   [Potential]   │  Could query metrics by trace (indirect)
│   SAP-013       │  [!] ClaudeMetric schema has NO trace_id field
│   Metrics       │  Status: RED - context lost
└─────────────────┘


         ┌─────────────────┐
         │   SAP-001       │  SOURCE
         │   Inbox         │
         └────────┬────────┘
                  │
                  ─ YELLOW: Manual extraction by agent
                  ─ Agent reads task JSON, sets CHORA_TRACE_ID env var
                  ─
                  ▼
         ┌─────────────────┐
         │   SAP-012       │  PHASE TRACKER: Inherits from parent task
         │   Development   │  - Phases reference trace via task metadata
         │   Lifecycle     │  - No explicit phase-to-phase propagation
         └────────┬────────┘
                  │
                  ├──> YELLOW: Manual emit to SAP-010
                  │    Agent emits phase transition events
                  │
                  ╌╌╌> RED: No propagation to SAP-005 CI/CD
                  │    [!] CI workflows don't receive trace_id
                  │
                  ╌╌╌> RED: No propagation to SAP-007 docs
                  │    [!] Frontmatter has no trace_id field
                  │
                  ╌╌╌> RED: No propagation to SAP-013 metrics
                       [!] Phase 8 metrics manually entered


┌─────────────────┐
│   SAP-007       │  [!] Docs created during DDD phase
│   Documentation │  Frontmatter: NO trace_id field
│   Framework     │  Status: RED - context lost
└─────────────────┘


┌─────────────────┐
│   SAP-005       │  [!] Release workflows triggered by tags
│   CI/CD         │  Workflows: NO trace_id env var
│   Workflows     │  Status: RED - context lost
└─────────────────┘


┌─────────────────┐
│   SAP-016       │  Link validation (stateless)
│   Link          │  Status: NEUTRAL - not applicable
│   Validation    │
└─────────────────┘


┌─────────────────┐
│   SAP-009       │  Provides awareness/guidance
│   Agent         │  Documents trace patterns in AGENTS.md
│   Awareness     │  Status: YELLOW - enables manual propagation
└─────────────────┘
```

---

## Detailed Flow Analysis

### Flow 1: Automatic Propagation (SAP-001 → SAP-010)

**Path**: SAP-001 (Inbox) ═══> SAP-010 (Memory)

**Mechanism**:
1. SAP-001 emits events to `inbox/coordination/events.jsonl` on every state transition:
   - Intake: `{"event_type": "coordination.intake", "trace_id": "ecosystem-w3-health-monitoring", ...}`
   - Review: `{"event_type": "coordination.review", "trace_id": "ecosystem-w3-health-monitoring", ...}`
   - Activation: `{"event_type": "coordination.activation", "trace_id": "ecosystem-w3-health-monitoring", ...}`
   - Completion: `{"event_type": "coordination.completion", "trace_id": "ecosystem-w3-health-monitoring", ...}`

2. SAP-010 memory system automatically:
   - Reads events from `inbox/coordination/events.jsonl`
   - Partitions by month: `.chora/memory/events/YYYY-MM/events.jsonl`
   - Creates per-trace files: `.chora/memory/events/YYYY-MM/traces/{trace_id}.jsonl`
   - Indexes events for cross-session querying

3. Knowledge notes reference traces:
   - Frontmatter field: `related_traces: [trace_id_1, trace_id_2, ...]`
   - Enables correlation between learnings and coordination items

**Status**: ✅ GREEN - Fully automatic, no manual steps

**Evidence**:
- SAP-001 protocol-spec FR-4: "Emit append-only JSONL events capturing state transitions with `CHORA_TRACE_ID`"
- SAP-010 protocol-spec: Event schema v1.0 includes `trace_id` as required field
- Implementation: `emit_event("event.type", trace_id=trace_id)`

---

### Flow 2: Manual Propagation (SAP-001 → SAP-012 → SAP-010)

**Path**: SAP-001 (Inbox) ───> SAP-012 (Lifecycle) ───> SAP-010 (Memory)

**Mechanism**:
1. SAP-001 creates coordination request: `inbox/incoming/coordination/COORD-2024-042.json`
   ```json
   {
     "trace_id": "ecosystem-w3-health-monitoring",
     "title": "W3 Health Monitoring",
     "description": "...",
     ...
   }
   ```

2. Agent reads coordination JSON, extracts `trace_id`:
   ```python
   with open('inbox/incoming/coordination/COORD-2024-042.json') as f:
       coord = json.load(f)
       trace_id = coord['trace_id']
   ```

3. Agent sets environment variable:
   ```bash
   export CHORA_TRACE_ID="ecosystem-w3-health-monitoring"
   ```

4. SAP-012 lifecycle phases reference trace via:
   - Task metadata (inherited from coordination request)
   - Environment variable `CHORA_TRACE_ID`
   - Manual agent discipline (not enforced)

5. Agent emits events to SAP-010 during phase transitions:
   ```python
   emit_event(
       "lifecycle.phase.complete",
       trace_id=os.environ.get('CHORA_TRACE_ID'),
       phase="DDD",
       ...
   )
   ```

**Status**: ⚠️ YELLOW - Manual, requires agent discipline

**Gaps**:
- No schema validation that phases include trace_id
- Agents can forget to set `CHORA_TRACE_ID` env var
- No enforcement mechanism (quality gate)

**Evidence**:
- SAP-012 protocol-spec: Phases reference "task context" but no explicit trace_id requirement
- SAP-009 CLAUDE.md: Documents pattern for extracting trace_id from coordination JSON
- SAP-001 task JSON schema: Includes `trace_id` field

---

### Flow 3: Context Lost (SAP-012 → SAP-013 Metrics)

**Path**: SAP-012 (Lifecycle) ╌╌╌> SAP-013 (Metrics) **BROKEN**

**Problem**:
1. SAP-012 Phase 8 (Monitoring) prescribes tracking metrics in `PROCESS_METRICS.md`
2. SAP-013 provides `ClaudeROICalculator` utility for metrics tracking
3. But `ClaudeMetric` schema does NOT include `trace_id` field:
   ```python
   @dataclass
   class ClaudeMetric:
       session_id: str
       timestamp: str
       task_type: str
       # NO trace_id field
   ```

4. Metrics tracked per-session, not per-coordination-item
5. No way to correlate:
   - "Which coordination trace generated which metrics?"
   - "What's the total ROI for trace ID `ecosystem-w3-health-monitoring`?"
   - "Lead time from SAP-001 intake → SAP-012 production deployment"

**Current Workaround**:
- Manual correlation: Developer notes trace_id in metric description field (unreliable)
- Retrospectives manually review `events.jsonl` and `PROCESS_METRICS.md` side-by-side

**Impact**:
- **Time wasted**: 30-60 min per retrospective (manual correlation)
- **Lost insights**: Can't measure end-to-end lead time, can't aggregate ROI by trace
- **No feedback loop**: Metrics don't inform SAP-001 strategic proposals automatically

**Status**: ❌ RED - Critical gap (see GAP-001, GAP-004)

**Recommendation**: Add optional `trace_id: str | None` field to `ClaudeMetric` dataclass

---

### Flow 4: Context Lost (SAP-012 → SAP-007 Documentation)

**Path**: SAP-012 (Lifecycle DDD Phase) ╌╌╌> SAP-007 (Documentation) **BROKEN**

**Problem**:
1. SAP-012 Phase 3 (Requirements/DDD) prescribes writing SAP-007 Diataxis docs
2. Developer creates markdown file: `user-docs/how-tos/w3-health-monitoring.md`
3. SAP-007 frontmatter schema:
   ```yaml
   ---
   title: "W3 Health Monitoring Setup"
   type: "how-to"
   status: "active"
   audience: "developers"
   test_extraction: false
   related: []
   # NO trace_id field
   ---
   ```

4. No linkage between:
   - Coordination request `COORD-2024-042.json` (trace_id: `ecosystem-w3-health-monitoring`)
   - Documentation file `w3-health-monitoring.md`

5. Can't answer:
   - "Which docs were created for coordination trace X?"
   - "Is documentation complete for strategic proposal Y?"

**Current Workaround**:
- Naming convention (file name matches trace ID) - unreliable
- Manual tracking in spreadsheets

**Impact**:
- **Time wasted**: 15-20 min per coordination item (manual lookup)
- **Lost traceability**: Can't audit "did we document this feature per coordination request?"
- **No automation**: Can't auto-generate doc templates from coordination items

**Status**: ❌ RED - Critical gap (see GAP-002)

**Recommendation**:
- Add `related_traces: [trace_id, ...]` to SAP-007 frontmatter schema
- Auto-populate from SAP-001 coordination JSON when generating doc templates

---

### Flow 5: Context Lost (SAP-012 → SAP-005 CI/CD)

**Path**: SAP-012 (Lifecycle Release Phase) ╌╌╌> SAP-005 (CI/CD) **BROKEN**

**Problem**:
1. SAP-012 Phase 7 (Release) uses SAP-005 `release.yml` workflow
2. Workflow triggered by git tag: `git tag v1.2.0 && git push origin v1.2.0`
3. GitHub Actions workflow runs but **no trace_id context**:
   ```yaml
   # .github/workflows/release.yml
   on:
     push:
       tags:
         - 'v*'
   jobs:
     release:
       runs-on: ubuntu-latest
       steps:
         # NO CHORA_TRACE_ID env var set
         - run: python scripts/publish-prod.sh
   ```

4. Release artifacts (PyPI package, GitHub release notes) don't include trace_id
5. Can't correlate:
   - "Which coordination trace triggered this release?"
   - "What features/bugs are included in this release (by trace ID)?"

**Current Workaround**:
- Manual release notes: Developer lists features/trace IDs in CHANGELOG.md
- No automated linkage

**Impact**:
- **Time wasted**: 20-30 min per release (manual release note generation)
- **Lost audit trail**: Can't trace production deployments back to coordination items
- **No metrics**: Can't measure "time from coordination → production"

**Status**: ❌ RED - Critical gap (see GAP-001)

**Recommendation**:
- Add `CHORA_TRACE_ID` to workflow dispatch inputs or extract from commit message
- Emit event to SAP-010: `{"event_type": "release.published", "trace_id": "...", "version": "v1.2.0"}`

---

## Summary Table: Trace ID Status by SAP

| SAP | Component | Generates | Receives | Stores | Propagates | Status | Gap ID |
|-----|-----------|-----------|----------|--------|------------|--------|--------|
| **SAP-001** | Inbox Coordination | ✅ YES | N/A | events.jsonl, JSON | SAP-010, SAP-012 | ✅ GREEN | - |
| **SAP-010** | Memory System | ❌ No | ✅ AUTO | events/traces/ | Queries only | ✅ GREEN | - |
| **SAP-012** | Dev Lifecycle | ❌ No | ⚠️ MANUAL | Task metadata | SAP-010 manual | ⚠️ YELLOW | - |
| **SAP-013** | Metrics | ❌ No | ❌ NO | NOT stored | None | ❌ RED | GAP-001, GAP-004 |
| **SAP-007** | Documentation | ❌ No | ❌ NO | NOT stored | None | ❌ RED | GAP-001, GAP-002 |
| **SAP-005** | CI/CD | ❌ No | ❌ NO | NOT stored | None | ❌ RED | GAP-001 |
| **SAP-016** | Link Validation | ❌ No | ❌ N/A | NOT stored | None | ⚪ NEUTRAL | - |
| **SAP-009** | Agent Awareness | ❌ No | 📖 DOCS | Guidance only | Enables SAP-010 | ⚠️ YELLOW | - |

**Key**:
- ✅ GREEN: Automatic propagation, fully implemented
- ⚠️ YELLOW: Manual propagation, requires discipline
- ❌ RED: Context lost, not implemented
- ⚪ NEUTRAL: Not applicable (stateless validation)
- 📖 DOCS: Documentation/guidance only

---

## Trace ID Format Analysis

### Format 1: Kebab-Case Descriptive (Recommended)

**Pattern**: `<scope>-<name>-<optional-year>`

**Examples**:
- `ecosystem-w3-health-monitoring` (ecosystem coordination)
- `coord-2024-042` (coordination request #42 in 2024)
- `proposal-enhance-testing-framework` (strategic proposal)

**Pros**:
- Human-readable
- Self-documenting (describes coordination scope)
- Sortable by scope/year

**Cons**:
- Manual generation (prone to typos/inconsistency)
- No guaranteed uniqueness

**Usage**: Strategic proposals, ecosystem coordination

---

### Format 2: UUID4 (Programmatic)

**Pattern**: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx` (full) or `xxxxxxxx` (8-char truncated)

**Examples**:
- `a3f7c891-4b2e-4d91-9a1c-3e5f6d7a8b9c` (full UUID4)
- `a3f7c891` (truncated, for brevity)

**Pros**:
- Guaranteed uniqueness
- Programmatic generation (`str(uuid.uuid4())`)
- No human coordination required

**Cons**:
- Not human-readable
- No semantic meaning

**Usage**: Automated task generation, API-driven coordination

---

### Format 3: Task IDs (Numeric)

**Pattern**: `task-NNN`, `coord-NNN`

**Examples**:
- `task-123` (task ID from inbox)
- `coord-456` (coordination request ID)

**Pros**:
- Short, memorable
- Sequential (easy to track)
- Maps to file names (`inbox/active/task-123/task.json`)

**Cons**:
- Not globally unique (requires namespace like `chora-base:task-123`)
- Manual increment (can conflict)

**Usage**: Local task tracking, inbox coordination

---

**Recommendation**: Use **kebab-case** for strategic/ecosystem coordination (human-readable), **UUID4** for automated/programmatic tasks (guaranteed uniqueness).

---

## Implementation Roadmap

### Phase 1: Schema Updates (Week 1)

**Goal**: Add trace_id fields to all relevant schemas

1. **SAP-013 (Metrics)**:
   ```python
   @dataclass
   class ClaudeMetric:
       session_id: str
       timestamp: str
       task_type: str
       trace_id: str | None = None  # NEW: optional trace correlation
   ```

2. **SAP-007 (Documentation)**:
   ```yaml
   # Frontmatter schema
   ---
   title: "..."
   type: "how-to"
   status: "active"
   related_traces: []  # NEW: array of trace IDs
   ---
   ```

3. **SAP-012 (Lifecycle)**:
   - Document explicit trace_id propagation requirement in phase contracts
   - Add validation: tasks must include `trace_id` field in metadata

---

### Phase 2: Propagation Utilities (Week 2)

**Goal**: Create scripts to propagate trace IDs automatically

1. **`scripts/set-trace-context.sh`**:
   ```bash
   # Extract trace_id from coordination JSON, set env var
   export CHORA_TRACE_ID=$(jq -r '.trace_id' inbox/incoming/coordination/$1)
   ```

2. **`scripts/generate-doc-from-coordination.sh`**:
   ```bash
   # Auto-generate SAP-007 doc with trace_id in frontmatter
   trace_id=$(jq -r '.trace_id' $1)
   cat > user-docs/how-tos/$2.md <<EOF
   ---
   title: "..."
   related_traces: ["$trace_id"]
   ---
   EOF
   ```

3. **SAP-005 Workflow Enhancement**:
   ```yaml
   # .github/workflows/release.yml
   env:
     CHORA_TRACE_ID: ${{ github.event.inputs.trace_id || 'unknown' }}
   ```

---

### Phase 3: Validation & Enforcement (Month 1)

**Goal**: Ensure trace IDs are always propagated

1. **Pre-commit hook** (SAP-006):
   ```bash
   # Warn if committing docs without related_traces field
   if grep -q "^type: how-to" *.md; then
       if ! grep -q "^related_traces:" *.md; then
           echo "WARNING: How-To docs should include related_traces field"
       fi
   fi
   ```

2. **CI validation** (SAP-005):
   ```yaml
   # Fail CI if metrics logged without trace_id
   - run: python scripts/validate-trace-propagation.py
   ```

3. **Documentation** (SAP-009):
   - Update AGENTS.md with explicit trace propagation patterns
   - Add "Trace ID Propagation Protocol" to awareness guides

---

## Success Criteria

- [x] CHORA_TRACE_ID flow mapped across 8 SAPs
- [x] GREEN/YELLOW/RED status assigned to each flow
- [x] 3 critical gaps identified (SAP-013, SAP-007, SAP-005)
- [x] Trace ID format analysis complete (3 formats documented)
- [ ] Phase 1 (Schema updates) implemented
- [ ] Phase 2 (Propagation utilities) created
- [ ] Phase 3 (Validation) enforced

---

**Audit Completed**: 2025-11-03
**Status**: Active - ready for GAP-001 implementation
**Next Steps**: Implement Phase 1 schema updates (SAP-013, SAP-007, SAP-012)
