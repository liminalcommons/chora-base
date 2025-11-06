# chora-base Response to chora-compose Design RFC

**Coordination Metadata**
```yaml
trace_id: COORD-2025-010-chora-base-rfc-response
type: design_feedback
from: chora-base
to: chora-compose
subject: "Design RFC Feedback: Option B Recommendation + Critical Gaps"
date: 2025-11-05
priority: P1
status: active
in_response_to: DESIGN_RFC_ECOSYSTEM_INVITATION.md
```

---

## Executive Summary

chora-base is a **named adopter** in the SAP-017 ledger with **6 documented use cases** spanning 250+ artifacts: (1) SAP-029 generation (90 artifacts across 18 SAPs), (2) SAP documentation maintenance (60 awareness files), (3) project template generation, (4) CI/CD configuration, (5) documentation suite generation (50+ files), and (6) status report generation. We strongly recommend **Option B (5-tool workflow-oriented design)** as it provides the best fit for AI agent workflows across all 6 use cases with minimal cognitive load, idempotent operations, and 88% reduction in tool calls. We've identified **4 critical gaps** in the RFC (agent decision-making, multi-session persistence, batch performance, error recovery) that must be addressed regardless of which option is chosen. We commit to refactoring SAP-017/018 after redesign and piloting SAP-029 in Q1 2026, but we need updated specs with locked parameter naming and clear error semantics.

---

## 1. Design Option Analysis

### Recommendation: Option B (5-Tool Workflow-Oriented Design)

We evaluated all three options against criteria relevant to chora-base's AI-agent-first workflows:

| Criterion | Option A (12 tools) | Option B (5 tools) | Option C (20 tools) | Winner |
|-----------|--------------------|--------------------|---------------------|---------|
| **AI Agent Cognitive Load** | Medium (12 tools to learn) | Low (5 intuitive verbs) | High (20 tools, must chain) | **B** |
| **Idempotence Guarantee** | Unclear per layer | Explicit (safe retries) | Resource-level (partial) | **B** |
| **SAP-029 Use Case Mapping** | Layer 4 → Layer 1 navigation | `create(id="sap-015")` → done | `collection.create()` + chaining | **B** |
| **Token Efficiency** | Moderate (layer lookups) | Best (1-2 calls per workflow) | Worst (4-5 chained calls) | **B** |
| **Parameter Consistency** | Layer-specific params remain | Universal (`id`, `context`, `force`) | REST-consistent but verbose | **B** |

### Detailed Rationale for Option B

#### 1. Matches AI Agent Mental Models

AI agents (especially Claude Code) think in terms of **goals** ("create documentation"), not **architecture** ("navigate to Layer 4, then Layer 2"). Option B's verbs map directly to agent intentions:

- `create()` → "Generate this content/artifact/collection"
- `refresh()` → "Update stale content only"
- `inspect()` → "Check status before deciding next action"
- `configure()` → "Manage config lifecycle"
- `discover()` → "What resources are available?"

Compare to Option A's layer-oriented thinking:
- "Is this a content, artifact, or collection?" (Layer determination)
- "Do I use `generate()` or `compose()` or `coordinate()`?" (Layer-specific verb selection)
- "What's the right config parameter name for this layer?" (Parameter inconsistency persists)

#### 2. Dramatic Reduction in Tool Calls for SAP-029

**Our use case**: Generate 18 SAPs, each with 5 artifacts (90 total)

**Current state (25 tools)**: ~8-10 tool calls per SAP
```python
# Per-SAP workflow with current interface:
list_collection_members(collection_config_path="sap-015.json")  # 1
batch_generate(content_ids=[...], shared_context={...})         # 2
validate_content(content_id="capability-charter")               # 3
validate_content(content_id="protocol-spec")                    # 4
validate_content(content_id="awareness-guide")                  # 5
validate_content(content_id="adoption-blueprint")               # 6
validate_content(content_id="ledger")                           # 7
assemble_artifact(artifact_config_id="sap-015-full-spec")       # 8
generate_collection(collection_config_path="sap-015.json")      # 9
check_freshness(collection_config_path="sap-015.json")          # 10

# Total for 18 SAPs: 18 × 10 = 180 tool calls
```

**Option B (5 tools)**: 1-2 tool calls per SAP
```python
# Per-SAP workflow with Option B:
create(id="sap-015", context={"version": "1.0.0"})  # 1 (handles all 5 artifacts)
inspect(id="sap-015")                               # 2 (optional: check status)

# Total for 18 SAPs: 18 × 1 = 18 tool calls (or 36 with optional inspect)
```

**Impact**: 88% reduction in tool calls (180 → 18-36), massive token savings in Claude Code sessions

#### 3. Idempotence is Critical for AI Agents

AI agents **will** retry failed operations. They **will** lose context mid-session. They **will** call the same operation multiple times across sessions.

Option B explicitly guarantees idempotence (RFC line 234):
> "Idempotent (safe to retry)"

This is essential for:
- **Multi-session work**: beads tasks span days (SAP-015), agents resume work in fresh sessions
- **Error recovery**: If generation fails partway, agent can safely retry `create()` without cleanup
- **Parallel workflows**: Multiple agents can work on different SAPs without coordination overhead

Option A and C don't explicitly address idempotence, leaving uncertainty about retry safety.

#### 4. Internal Orchestration Reduces Complexity

Option B's philosophy (RFC line 238):
> "Handles complexity internally"

This is the **right abstraction level** for AI agents. Agents shouldn't need to:
- Manually orchestrate "generate content → validate → assemble artifact → coordinate collection"
- Track which content pieces are ready before assembly
- Handle dependency ordering (which artifacts depend on which content)

Option B's `create()` handles all of this internally, exposing a simple interface while managing complexity behind the scenes.

**Trade-off acknowledged**: Option A/C provide more granular control. But for our use case (SAP generation), we don't need that granularity. We need **reliable, repeatable generation** with minimal agent decision-making overhead.

### Why Not Option A or C?

**Option A (12 layer-oriented tools)**:
- ❌ Requires understanding the 4-layer architecture (Layer 1: config, Layer 2: generation, Layer 3: composition, Layer 4: collection)
- ❌ Adds conceptual overhead: agents must determine which layer their task belongs to
- ❌ Still has 12 tools to learn vs 5
- ✅ Good for teams who think architecturally (but chora-base agents think in workflows, not layers)

**Option C (20 resource-oriented tools)**:
- ❌ Highest tool count (20 vs 5)
- ❌ Requires chaining 4-5 tool calls for simple workflows (create content → validate → assemble artifact → check collection)
- ❌ Token inefficient: each tool call adds context overhead
- ✅ Predictable REST patterns (but predictability < simplicity for AI agents)
- ✅ Granular control (but we don't need it for our use cases)

---

## 1.5. Complete Use Case Portfolio

While **SAP-029** (generate 90 artifacts across 18 SAPs) is our primary and most complex use case, chora-base has **5 additional use cases** that inform our design preference:

### Use Case 1: SAP Generation (Primary - SAP-029)

**Already detailed above.** This is our highest-priority use case and the main driver for our Option B recommendation.

**Scale**: 18 collections × 5 artifacts = 90 total artifacts
**Frequency**: One-time generation, then iterative updates
**Complexity**: High (multi-level composition, dependency tracking, freshness policies)

---

### Use Case 2: SAP Documentation Maintenance (30+ SAPs)

**Problem**: chora-base has 30+ existing SAPs. Each has AGENTS.md and CLAUDE.md files that must stay synchronized with protocol-spec.md and implementation. When we update a protocol-spec or add new workflows, we need to regenerate awareness files consistently.

**Workflow with Option B**:
```python
# Update AGENTS.md across all 30 SAPs when template changes
for sap_id in ["sap-001", "sap-002", ..., "sap-030"]:
    refresh(id=f"{sap_id}-agents-doc", reason="protocol-spec updated")

# Or as collection:
refresh(id="all-sap-awareness-files")  # Regenerates only stale docs
```

**Scale**: 30 SAPs × 2 files (AGENTS.md, CLAUDE.md) = 60 files
**Frequency**: Weekly to monthly (as protocols evolve)
**Complexity**: Medium (template-based, context from protocol-spec)

**Why this validates Option B**: `refresh()` with freshness policies means we only regenerate what's stale, not all 60 files. Option C would require 60 individual `content.update()` calls with manual staleness checking.

---

### Use Case 3: Project Template Generation (SAP-003 Bootstrap)

**Problem**: When adopting chora-base patterns in new projects, we need to generate standard directory structures (.chora/, docs/skilled-awareness/, inbox/), configuration files (config.yaml, sap-catalog.json), and initial documentation (README.md, CONTRIBUTING.md).

**Workflow with Option B**:
```python
# Bootstrap new project with chora-base patterns
create(id="chora-base-project-template", context={
    "project_name": "my-new-project",
    "saps_to_adopt": ["SAP-001", "SAP-009", "SAP-015"],
    "language": "python"
})

# Result: Complete .chora/ structure, inbox setup, SAP docs
```

**Scale**: 15-20 files per project bootstrap
**Frequency**: Ad-hoc (whenever new projects adopt chora-base)
**Complexity**: Medium (conditional file generation based on SAP selection)

**Why this validates Option B**: `create()` can orchestrate complex conditional generation internally. Option A would require navigating layers (Layer 1: config SAPs → Layer 2: generate files → Layer 3: compose directory structure), adding unnecessary complexity.

---

### Use Case 4: CI/CD Configuration Generation (SAP-005)

**Problem**: GitHub Actions workflows, Docker Compose files, and deployment manifests need environment-specific variations (dev, staging, prod). These must stay synchronized with application architecture changes.

**Workflow with Option B**:
```python
# Generate environment-specific CI/CD configs
create(id="github-actions-ci", context={"environment": "production"})
create(id="docker-compose-stack", context={"environment": "staging"})

# When infrastructure changes, refresh only affected configs
refresh(id="deployment-configs")  # Collection of all env configs
```

**Scale**: 5-10 config files per environment × 3 environments = 15-30 files
**Frequency**: Weekly (as infrastructure evolves)
**Complexity**: Medium (context-dependent generation, environment inheritance)

**Why this validates Option B**: Freshness policies ensure configs stay synchronized with infrastructure changes. `refresh()` detects stale configs automatically without manual tracking.

---

### Use Case 5: Documentation Suite Generation (User/Dev Docs)

**Problem**: chora-base has extensive documentation (docs/user-docs/, docs/dev-docs/, docs/project-docs/) that references 30+ SAPs, multiple scripts, and evolving patterns. When we add new SAPs or update workflows, documentation must be regenerated to include new references, examples, and cross-links.

**Workflow with Option B**:
```python
# Regenerate user documentation when SAP catalog changes
refresh(id="user-docs-suite", reason="SAP-031 added to catalog")

# Generate API reference from source code annotations
create(id="api-reference-docs", context={"source_dir": "src/"})

# Update getting-started guides when bootstrap process changes
refresh(id="getting-started-collection")
```

**Scale**: 50+ documentation files across 3 domains (user/dev/project docs)
**Frequency**: Weekly to bi-weekly (as SAPs evolve)
**Complexity**: High (cross-references, link validation, index generation)

**Why this validates Option B**: Multi-level composition (content → artifact → collection) with automatic dependency tracking. `refresh()` handles complex dependency chains (if protocol-spec updates, regenerate AGENTS.md, which triggers index regeneration).

---

### Use Case 6: Status Report Generation (Project Management)

**Problem**: Weekly project updates, sprint retrospectives, and coordination summaries aggregate data from multiple sources (beads tasks, A-MEM events, git commits, SAP evaluations). These reports need consistent formatting and automatic data collection.

**Workflow with Option B**:
```python
# Generate weekly status report
create(id="weekly-status-report", context={
    "week": "2025-W45",
    "data_sources": [
        "beads://open-tasks",
        "amem://development.jsonl",
        "git://commits-since-last-week"
    ]
})

# Generate sprint retrospective
create(id="sprint-retro-2025-q4", context={
    "sprint_start": "2025-10-01",
    "sprint_end": "2025-10-31"
})
```

**Scale**: 5-10 reports per month
**Frequency**: Weekly (status reports), monthly (retrospectives)
**Complexity**: Medium (data aggregation, formatting, chart generation)

**Why this validates Option B**: LLM-powered generation (not just templates) for summarizing qualitative data. `create()` orchestrates data collection → LLM summarization → report assembly in one call.

---

### Summary: Use Case Portfolio Impact on Design Choice

| Use Case | Frequency | Scale | Complexity | Option B Benefit |
|----------|-----------|-------|------------|------------------|
| **1. SAP Generation** | One-time + updates | 90 artifacts | High | 88% tool call reduction |
| **2. SAP Docs Maintenance** | Weekly-monthly | 60 files | Medium | Automatic staleness detection |
| **3. Project Templates** | Ad-hoc | 15-20 files | Medium | Conditional orchestration |
| **4. CI/CD Configs** | Weekly | 15-30 files | Medium | Environment-specific freshness |
| **5. Documentation Suite** | Weekly-bi-weekly | 50+ files | High | Dependency chain automation |
| **6. Status Reports** | Weekly-monthly | 5-10 reports | Medium | LLM-powered summarization |

**Total Impact**: 6 use cases, 250+ artifacts under management, weekly to monthly regeneration frequency

**Why Option B Wins for All 6**:
1. **Cognitive Load**: 5 tools vs 25 (or 12/20) scales better as use cases multiply
2. **Freshness Automation**: `refresh()` handles staleness across all 6 use cases without custom logic
3. **Idempotence**: Safe to retry across multi-session workflows (SAP-015 beads tasks span days/weeks)
4. **Token Efficiency**: 74% savings per workflow × 6 use cases = massive cumulative savings
5. **Agent-Friendly**: Workflow-oriented verbs (`create`, `refresh`, `inspect`) match all 6 use case mental models

**Option A/C Comparison**:
- Option A (12 tools) requires determining which layer for each use case (cognitive overhead × 6)
- Option C (20 tools) requires chaining 4-5 calls per workflow × 6 use cases = high token cost at scale

---

## 2. Critical Gaps Identified

Regardless of which design option is chosen, the RFC has **4 critical gaps** that impact chora-base's ability to adopt:

### Gap 1: Agent Decision-Making Criteria

**Problem**: The RFC analyzes tool count and parameter naming (excellent!) but doesn't address **when agents should use each tool**. AI agents need decision trees, not just tool signatures.

**Impact on chora-base**:
- Claude Code sessions waste tokens asking "should I use create() or refresh()?"
- Agents retry with different tools when uncertain
- No clear guidance for multi-step workflows

**Specific Request**: Add "Agent Decision Tree" section to protocol-spec (or awareness-guide):

```markdown
## When Should Agents Use Each Tool?

### create()
- **Use when**: First-time generation OR idempotent regeneration
- **Don't use when**: Content already exists and you only want to update stale pieces (use refresh() instead)
- **Safe to retry**: YES (idempotent)
- **Example**: "Generate SAP-015 documentation suite" → create(id="sap-015")

### refresh()
- **Use when**: Content exists but may be stale, want to update only what's needed
- **Don't use when**: Content doesn't exist yet (use create() instead)
- **Safe to retry**: YES (only touches stale content)
- **Example**: "Update documentation if API changed" → refresh(id="sap-015")

### inspect()
- **Use when**: Need to check status before deciding next action
- **Don't use when**: Just want to generate (skip inspection, use create() directly)
- **Safe to retry**: YES (read-only)
- **Example**: "Is documentation fresh?" → inspect(id="sap-015")

### configure()
- **Use when**: Managing config lifecycle (draft → test → save)
- **Don't use when**: Config already exists and you just want to generate (use create() with existing config)
- **Safe to retry**: DEPENDS (read ops: yes, write ops: no for save/persist)
- **Example**: "Create new SAP config" → configure(operation="create", type="collection", data={...})

### discover()
- **Use when**: Exploring available resources before creating
- **Don't use when**: You already know the config ID (use create() directly)
- **Safe to retry**: YES (read-only)
- **Example**: "What SAPs can I generate?" → discover(filter="collection")
```

**Why this matters**: Option B's strength is workflow-oriented design, but without decision guidance, agents must guess which workflow to use.

### Gap 2: Multi-Session Persistence

**Problem**: The RFC doesn't specify how state (especially freshness) persists across API calls, sessions, or repositories.

**Impact on chora-base**:
- chora-base agents work across sessions (beads tasks span days, weeks)
- Agent A generates SAP-015 on Monday, Agent B checks freshness on Friday
- Need clarity: where is freshness state stored? Does it survive session boundaries?

**Specific Request**: Document state persistence guarantees:

```yaml
## State Persistence Questions

1. Session Boundaries:
   Q: Agent A calls create(id="sap-015") today. Agent B calls inspect(id="sap-015") tomorrow.
   A: Does Agent B see yesterday's freshness state? Or recalculated from scratch?

2. Repository Boundaries:
   Q: chora-base tracks freshness in SAP-017/018 docs. chora-compose stores it in .chora-compose/cache/.
   A: Who owns freshness state? Is it portable across repos?

3. Collection Member Granularity:
   Q: Collection has 5 artifacts. Artifact #3 becomes stale.
   A: Does refresh() regenerate only artifact #3? Or all 5? Or the 3 downstream of #3?

4. Freshness Policy Changes:
   Q: Collection has max_age_days=30. We change it to max_age_days=7.
   A: Does existing content immediately become stale? Or does freshness recalculate on next inspect()?

5. Cache Invalidation:
   Q: User manually edits generated content file.
   A: Does chora-compose detect the edit and mark content as "manual override"? Or overwrite on next create()?
```

**Why this matters**: Multi-session workflows are the norm for chora-base (SAP-015 beads enables this), not the exception.

### Gap 3: Batch Operation Performance

**Problem**: The RFC mentions `batch_generate` (line 576) but provides no performance targets or SLAs.

**Impact on chora-base**:
- SAP-029 will generate 90 artifacts in parallel (18 collections × 5 artifacts)
- Need to know: Is this 30 seconds? 5 minutes? 30 minutes?
- Agents must decide: Generate serially (slow but safe) or parallel (fast but risky)?

**Specific Request**: Define performance SLAs and batch behavior:

```yaml
## Batch Operation Performance Targets

### For create(id="collection") with 5 artifacts:
- Sequential generation: < 30 seconds per artifact (< 2.5 min total)
- Parallel generation (if supported): < 60 seconds total
- Failure rate: < 5% per artifact (95% success)

### For 18 collections × 5 artifacts (SAP-029 use case):
- Sequential (18 create() calls, each 2.5 min): < 45 minutes (acceptable)
- Parallel (5 concurrent create() calls): < 10 minutes (target)
- Partial failure handling: Continue processing remaining collections even if one fails

### For refresh() operations:
- Freshness check overhead: < 1 second per collection
- Regeneration only for stale content: < 20% of full generation time
- Batch refresh (multiple collections): Linear scaling with concurrent limit

### Error Scenarios:
- Template rendering error: Fail fast (< 5 seconds)
- LLM generation timeout: Configurable (default: 60 seconds)
- Dependency missing: Fail fast with clear error message
```

**Why this matters**: Option B's `create()` hides parallelism complexity, but agents need to know if generating 18 SAPs is feasible in a single session or requires chunking.

### Gap 4: Error Recovery Patterns

**Problem**: The RFC doesn't specify what happens when operations partially fail.

**Impact on chora-base**:
- If create(id="sap-015") fails on artifact #3 of 5, what's the state?
- Can agent retry? Must agent clean up first? Are artifacts #1-2 lost?
- No guidance means agents will retry incorrectly, causing cascading failures

**Specific Request**: Document error semantics and recovery patterns:

```yaml
## Error Recovery: Partial Failure Scenarios

### Scenario 1: create(id="collection") fails mid-generation
Setup: Collection has 5 artifacts. Artifact #3 fails (template error).

Option A (Transactional - Rollback):
- Delete artifacts #1-2 (rollback to pre-create state)
- Return error with full context
- Agent must fix template and retry create() from scratch

Option B (Partial Success - Keep Progress):
- Keep artifacts #1-2 (mark as SUCCESS)
- Mark artifact #3 as FAILED (with error details)
- Skip artifacts #4-5 (mark as SKIPPED)
- Return partial success with detailed status
- Agent can fix template and retry create() (will skip #1-2, retry #3, generate #4-5)

Option C (Continue On Error):
- Keep artifacts #1-2 (mark as SUCCESS)
- Mark artifact #3 as FAILED
- Continue generating artifacts #4-5
- Return partial success with 4/5 artifacts generated
- Agent can fix template and call refresh() to regenerate only #3

**Which does Option B implement?** (Our preference: Option C for maximum progress preservation)

### Scenario 2: refresh() finds 3/5 artifacts stale
Setup: Artifacts #1, #3, #5 are stale. #2, #4 are fresh.

Expected Behavior:
- Regenerate only #1, #3, #5 (don't touch #2, #4)
- If #3 regeneration fails, keep old version or delete?
- Does failure of #3 block regeneration of #5?

### Scenario 3: Dependency cycle detected
Setup: Artifact A depends on Artifact B, which depends on Artifact A.

Expected Behavior:
- Fail fast with clear error message (cycle detection)
- Suggest resolution: "Remove circular dependency between A and B"
- Don't attempt generation (avoid infinite loop)

### Scenario 4: Context variable missing
Setup: Template expects {{api_version}}, but context doesn't provide it.

Expected Behavior:
- Fail fast with clear error: "Missing required context variable 'api_version'"
- Suggest resolution: "Provide context={'api_version': '...'}"
- Don't generate partial content with missing placeholders
```

**Why this matters**: Option B's idempotence guarantee is only valuable if error recovery semantics are clear. Agents need to know if retrying will make things worse or fix them.

---

## 3. Requirements for SAP-017/018 Refactor

After chora-compose completes the redesign, chora-base will refactor SAP-017 (chora-compose-integration) and SAP-018 (chora-compose-meta) to match the new architecture. We need the following deliverables:

### Deliverable 1: Updated Protocol Specification

**Contents**:
- New tool signatures (5 tools for Option B, or 12/20 for Option A/C)
- **Locked parameter naming standards** (no more 6 variations of config ID)
- Complete error codes and recovery patterns (addressing Gap 4)
- Performance SLAs for batch operations (addressing Gap 3)
- State persistence guarantees (addressing Gap 2)
- Agent decision-making criteria (addressing Gap 1)

**Format**: Markdown protocol-spec.md following SAP-000 structure

**Timeline**: Delivered within 6 weeks of redesign kickoff (by Dec 17, 2025)

### Deliverable 2: Migration Guide

**Contents**:
- Mapping table: old 25 tools → new tools (5/12/20)
- Breaking changes documented with examples
- Migration timeline and grace period (will v2.0.1 remain supported during transition?)
- Code examples: before/after for common workflows
- MCP server configuration updates (tool name changes)

**Format**: Markdown migration-guide.md with side-by-side comparisons

**Timeline**: Delivered with protocol-spec (by Dec 17, 2025)

### Deliverable 3: Agent Integration Examples

**Contents**:
- Claude Code workflows for all new tools (Option B: 5 examples minimum)
- MCP server configuration (updated .claude/mcp_settings.json)
- Multi-session usage patterns (beads integration examples)
- Error recovery workflows (agent decision trees)
- Performance optimization tips (batch operations, parallel generation)

**Format**: AGENTS.md and CLAUDE.md following SAP-009 nested awareness pattern

**Timeline**: Delivered with protocol-spec (by Dec 17, 2025)

### Deliverable 4: Testing Artifacts

**Contents**:
- Integration test suite chora-base can run (validate redesign before refactoring SAPs)
- Performance benchmarks (90-artifact SAP-029 target: < 10 minutes with parallelism)
- Error injection tests (partial failure scenarios from Gap 4)
- Idempotence validation tests (prove retry safety)

**Format**: Python test suite (pytest) + benchmark scripts

**Timeline**: Delivered with protocol-spec (by Dec 17, 2025)

### Timeline Summary

| Milestone | Target Date | Owner | Deliverables |
|-----------|-------------|-------|--------------|
| **RFC feedback due** | Nov 12, 2025 | chora-base | This document |
| **Design finalized** | Dec 3, 2025 | chora-compose | Option A/B/C chosen, gaps addressed |
| **Redesign complete** | Dec 17, 2025 | chora-compose | Protocol-spec, migration guide, examples, tests |
| **SAP-017/018 refactor** | Dec 31, 2025 | chora-base | Updated integration guides |
| **SAP-029 pilot** | Jan 2026 (Q1) | chora-base | Generate 18 SAPs with new design |

---

## 4. Commitment from chora-base

### What We're Committing To

✅ **Provide detailed design feedback** (this document)
✅ **Validate Option B with SAP-029 pilot** (Q1 2026, after redesign complete)
✅ **Refactor SAP-017 (chora-compose-integration)** (match new 5-tool interface)
✅ **Refactor SAP-018 (chora-compose-meta)** (document new architecture)
✅ **Update AGENTS.md/CLAUDE.md** (new workflows, decision trees)
✅ **Document lessons learned** (SAP-017 ledger, agent usage patterns)
✅ **Serve as reference adopter** (for external RFC once validated internally)
✅ **Log adoption metrics** (SAP-027 dogfooding patterns, SAP-010 A-MEM events)

### What We're NOT Committing To (Yet)

❌ **Pilot before redesign** (current 25-tool interface too cumbersome for SAP-029 use case)
❌ **Production use until validated** (pilot must succeed before relying on chora-compose for critical workflows)
❌ **External promotion** (won't recommend to external partners until we validate internally)
❌ **Specific SAP-029 delivery date** (depends on redesign quality and refactored SAP-017/018)
❌ **Contribution to chora-compose codebase** (feedback only at this stage)

### Conditions for Pilot (Q1 2026)

We'll proceed with SAP-029 pilot if:
1. ✅ Option B (or equivalent workflow-oriented design) is implemented
2. ✅ All 4 critical gaps are addressed (decision trees, persistence, performance, error recovery)
3. ✅ Parameter naming is locked (no breaking changes after pilot starts)
4. ✅ Integration tests pass in chora-base environment
5. ✅ Performance benchmarks meet targets (< 10 min for 90 artifacts with parallelism)

If any condition fails, we'll defer pilot to Q2 2026 and provide additional feedback.

---

## 5. Open Questions for chora-compose

We need clarification on these questions before committing to the pilot timeline:

### Q1: Parameter Naming Lock-In

**Question**: Will the redesign (Option B) freeze parameter naming standards?

**Context**: Current state has 6 variations of "config ID" across 15 tools (RFC line 119-131). Option B proposes universal `id` parameter.

**Why we care**: We can't refactor SAP-017/018 if parameter names change post-refactor. Need guarantee that `create(id=...)` won't become `create(config_id=...)` six months later.

**Request**: Commit to stable parameter naming in v3.0.0 release (or whatever version implements redesign).

### Q2: Backward Compatibility

**Question**: Will v2.0.1 (current 25-tool interface) remain supported during transition?

**Context**: chora-base may have interim work using current interface. If redesign launches Dec 2025, we need grace period to migrate.

**Why we care**: Hard cutover would break any interim scripts or workflows. Need to plan migration timing.

**Request**: Clarify deprecation timeline (e.g., v2.0.1 supported for 3 months after v3.0.0 release, then removed).

### Q3: MCP Tool Names

**Question**: Will MCP tool names change in redesign?

**Context**: Current tools like `choracompose:generate_content` may become `choracompose:create`. This impacts MCP server configuration in SAP-017.

**Why we care**: MCP tool names are part of Claude Desktop configuration. Breaking changes require user action.

**Request**: Provide before/after mapping for all MCP tool names (for migration guide and SAP-017 update).

### Q4: Collection Idempotence

**Question**: Is `create(id="collection")` truly idempotent?

**Context**: Option B promises idempotence (RFC line 234), but details unclear.

**Scenarios**:
- Scenario A: `create("sap-015")` called twice → second call is no-op (returns cached result)
- Scenario B: `create("sap-015")` called twice → second call regenerates everything (overwrites)
- Scenario C: `create("sap-015")` called twice → second call regenerates only stale content (hybrid)

**Why we care**: AI agents WILL call `create()` multiple times (retries, multi-session workflows). Need to know if this is safe or will cause unexpected regeneration.

**Request**: Specify exact idempotence semantics (our preference: Scenario C for balance of safety and freshness).

### Q5: Freshness Policy Inheritance

**Question**: Do collection members inherit parent freshness policies?

**Context**: Collection config has `freshness: {max_age_days: 30}`. Do all 5 member artifacts inherit this? Or must each define their own?

**Why we care**: SAP-029 will have 18 collections with uniform freshness policy. If each of 90 artifacts needs individual config, that's 90× maintenance overhead.

**Request**: Document freshness policy inheritance rules (our preference: inherit from collection, with optional per-artifact override).

---

## 6. Next Steps

### Immediate (Week 1-2)

1. **chora-compose reviews feedback** from chora-base and other ecosystem partners
2. **chora-compose synthesizes input** and chooses final design (Option A/B/C or hybrid)
3. **chora-compose addresses critical gaps** (decision trees, persistence, performance, error recovery)

### Short-term (Week 3-6)

4. **chora-compose implements redesign** with locked parameter naming and clear error semantics
5. **chora-compose delivers artifacts** (protocol-spec, migration guide, examples, tests)
6. **chora-base validates integration tests** in chora-base environment

### Medium-term (Week 7-8)

7. **chora-base refactors SAP-017** (chora-compose-integration) to match new interface
8. **chora-base refactors SAP-018** (chora-compose-meta) to document new architecture
9. **chora-base updates awareness files** (AGENTS.md, CLAUDE.md with new workflows)

### Long-term (Q1 2026)

10. **chora-base pilots SAP-029** using refactored SAP-017/018 (generate 18 SAPs, 90 artifacts)
11. **chora-base documents lessons learned** in SAP-017 ledger (adoption metrics, agent patterns, gotchas)
12. **chora-compose uses experience** for external RFC (chora-base as reference adopter)

---

## 7. Contact & Coordination

**chora-base Coordination Contact**: inbox/coordination/ (follow standard inbox protocol)

**Response Method**:
- **Preferred**: Submit coordination response via inbox system (trace_id: COORD-2025-010-response)
- **Alternative**: GitHub issue in chora-compose repo (reference this document)

**Expected Response Timeline**:
- **Initial acknowledgment**: Within 1 week (by Nov 12, 2025)
- **Design decision**: Within 4 weeks (by Dec 3, 2025)
- **Artifact delivery**: Within 6 weeks (by Dec 17, 2025)

**Escalation**: If timeline slips, coordinate via inbox/coordination/active.jsonl with updated expectations

---

## 8. Appendix: Supporting Evidence

### A. chora-base Adoption Status

**SAP-017 (chora-compose-integration)**: v2.0.0, Active status
**SAP-018 (chora-compose-meta)**: v2.0.0, Active status
**Coordination History**: COORD-001 (Oct 29), COORD-2025-002 (Nov 2), COORD-2025-009 (Nov 2, ACCEPTED)
**Named Adopter**: SAP-017 ledger line 98-99 (planned Level 1 adoption for SAP generation)

### B. Complete Use Case Portfolio

**6 Use Cases Across 250+ Artifacts**:

1. **SAP Generation (SAP-029)**: 18 SAPs × 5 artifacts = 90 files | One-time + updates | Priority: HIGH
2. **SAP Documentation Maintenance**: 30 SAPs × 2 files = 60 awareness files | Weekly-monthly | Priority: HIGH
3. **Project Template Generation**: 15-20 files per bootstrap | Ad-hoc | Priority: MEDIUM
4. **CI/CD Configuration**: 15-30 config files across 3 environments | Weekly | Priority: MEDIUM
5. **Documentation Suite**: 50+ files across user/dev/project docs | Weekly-bi-weekly | Priority: MEDIUM
6. **Status Reports**: 5-10 reports per month | Weekly-monthly | Priority: LOW

**SAP-029 Details (Primary Use Case)**:
- **Scope**: Generate 18 SAPs (SAP-032 through SAP-049)
- **Artifacts per SAP**: 5 (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- **Total Artifacts**: 90
- **Expected ROI**: 5x+ productivity improvement (per SAP-017 ledger)
- **Timeline**: Q1 2026 pilot (after chora-compose redesign)

**Cumulative Impact**:
- **Total artifacts under management**: 250+
- **Regeneration frequency**: Daily to monthly (depending on use case)
- **Estimated token savings**: 74% per workflow × 6 use cases = massive cumulative savings
- **Cognitive load reduction**: 5 tools vs 25 = 80% fewer tools to learn

### C. Integration Surface Area

**Current MCP Integration**: SAP-017 documents 4 modalities (pip, MCP, CLI, Docker)
**Preferred Modality**: MCP server (Claude Desktop + Claude Code)
**Tool Count Impact**: 25 tools → 5 tools = 80% reduction in awareness documentation burden
**Parameter Count Impact**: 6 config ID variations → 1 universal `id` = simpler AGENTS.md examples

### D. Token Efficiency Analysis

**Current Interface (25 tools)**:
- Tool discovery: ~500 tokens (list 25 tool signatures)
- Workflow execution: ~1200 tokens (10 tool calls × 120 tokens each)
- Total per SAP: ~1700 tokens

**Option B (5 tools)**:
- Tool discovery: ~200 tokens (list 5 tool signatures)
- Workflow execution: ~240 tokens (2 tool calls × 120 tokens each)
- Total per SAP: ~440 tokens

**Savings**: 74% token reduction per SAP generation workflow
**Scaled to 18 SAPs**: ~23k tokens saved per full SAP-029 execution

---

**End of Response**

**Summary**: chora-base strongly supports Option B (5-tool workflow design) for its alignment with AI agent workflows, dramatic reduction in cognitive load and tool calls, and explicit idempotence guarantees. We've identified 4 critical gaps that must be addressed regardless of design choice. We commit to refactoring SAP-017/018 and piloting SAP-029 in Q1 2026, contingent on receiving updated specs with locked parameters and clear error semantics by Dec 17, 2025. We're ready to collaborate on making chora-compose the best-in-class content generation system for AI-coordinated workflows.

**Date**: 2025-11-05
**Priority**: P1 (blocks SAP-029 adoption)
**Next Action**: Await chora-compose acknowledgment and design decision
