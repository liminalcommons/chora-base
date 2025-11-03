---
title: Chora-Compose Inbox Integration Exploration
type: exploration
trace_id: chora-compose-inbox-integration-2025
created: 2025-11-02
status: in_progress
---

# Chora-Compose as Inbox Protocol Infrastructure - Exploration Summary

## Context

chora-base's SAP-001 (Inbox Coordination Protocol) currently uses manual JSON artifact creation for coordination requests, implementation tasks, and strategic proposals. This manual process requires 30-60 minutes per coordination request and 15-30 minutes per implementation task, with high cognitive load for maintaining consistent structure and completeness.

**Hypothesis**: chora-compose MCP infrastructure can serve as the generation layer for inbox artifacts, replacing manual JSON creation with template-driven, automated generation.

**Trace Context**: `chora-compose-inbox-integration-2025`

## Research Questions

### Primary Questions

1. **Can chora-compose generate valid inbox artifacts?**
   - Do generated artifacts validate against JSON schemas?
   - Can content configs produce the required structure (18+ required fields)?
   - How does quality compare to hand-written artifacts?

2. **What is the integration architecture?**
   - How do inbox artifact schemas map to chora-compose content configurations?
   - How do inbox workflows map to chora-compose collections?
   - What transformation points exist between manual and automated generation?

3. **What are the efficiency gains?**
   - Time reduction per artifact type?
   - Maintenance overhead reduction?
   - Template reuse benefits across ecosystem?

### Secondary Questions

4. **What gaps exist in chora-compose?**
   - Missing features needed for inbox integration?
   - Compatibility issues with inbox protocol requirements?
   - Migration challenges from manual to automated?

5. **What is the pilot scope?**
   - Which artifact types are best suited for initial pilot?
   - Success criteria and quality thresholds?
   - Decision points and fallback options?

## Exploration Approach

### Methodology

1. **Comprehensive System Analysis** (Nov 2, 2025)
   - Deep exploration of current inbox implementation (schemas, workflows, processing scripts)
   - Deep exploration of chora-compose capabilities (architecture, generators, MCP integration)
   - Parallel research using Task tool with Plan subagent (very thorough)

2. **Integration Mapping**
   - Map inbox artifact types to chora-compose content types
   - Map inbox workflows to chora-compose collections
   - Identify transformation points and integration patterns

3. **Gap Analysis**
   - Identify missing chora-compose features
   - Assess compatibility with inbox protocol requirements
   - Document migration challenges

4. **Feasibility Assessment**
   - Technical feasibility (can it work?)
   - Quality feasibility (will it meet 80%+ threshold?)
   - Maintenance feasibility (is it sustainable?)
   - Ecosystem feasibility (will it benefit other repos?)

## Key Findings

### Critical Discovery: chora-compose Architecture

**MAJOR FINDING**: chora-compose is **NOT** Docker Compose orchestration as documented in outdated SAP-017 and SAP-018.

**Actual Architecture**: chora-compose is a **content generation framework** with:
- **17 production generators** for various content types
- **MCP server integration** (17 MCP tools for conversational generation)
- **Template-driven artifact composition** using Jinja2, demonstration, and template_fill patterns
- **Ephemeral storage** with timestamp-based versioning
- **Modular content assembly** via ContentElements and ChildReferences

This discovery fundamentally changes the integration potential - chora-compose is ideally suited for inbox artifact automation.

### Current Inbox Implementation

**Three Core Artifact Types**:

1. **Coordination Requests** (`inbox/schemas/coordination-request.schema.json`)
   - 18 required fields (type, request_id, title, from_repo, to_repo, priority, urgency, deliverables, etc.)
   - Lifecycle: incoming → sprint planning → active → completed
   - Current effort: 30-60 minutes per request
   - JSON Schema validation required

2. **Implementation Tasks** (`inbox/schemas/implementation-task.schema.json`)
   - 18 required fields (task_id, sprint, priority, category, deliverables, etc.)
   - Workflow phases: DDD → BDD → TDD → Review → Completion
   - Current effort: 15-30 minutes per task
   - Quality metrics tracking (coverage, tests, mypy, ruff)

3. **Strategic Proposals** (`inbox/schemas/strategic-proposal.schema.json`)
   - Quarterly review cycle
   - Scoring framework (0-50 points across 5 dimensions)
   - Lifecycle: proposal → RFC → ADR → coordination requests
   - Current effort: 1-2 hours per proposal

**Processing Infrastructure**:
- `scripts/inbox-status.py` (443 lines) - Parses and filters inbox artifacts
- `inbox/coordination/events.jsonl` - Append-only event log with trace_id correlation
- Directory-based workflow (incoming/, active/, completed/)

**Key Requirements**:
- JSON Schema validation (100% structural compliance)
- Sequential ID generation (coord-NNN, task-NNN)
- Event emission with CHORA_TRACE_ID
- Compatible with existing processing scripts

### chora-compose Capabilities

**Content Generation Architecture**:

```
Collection (workflow orchestration)
   ↓
SAP (atomic capability)
   ↓
Artifacts (multi-part assembly)
   ↓
Content Configs (single-purpose generators)
   ↓
ContentElements (individual sections)
   ↓
Content Blocks (reusable markdown)
```

**Key Components**:

1. **ContentElement** - Atomic content unit
   - `name`, `description`, `prompt_guidance`
   - `format` (markdown | code | json | yaml | section)
   - `example_output` (actual content block)
   - `generation_source` (ai | human | template | mixed)

2. **GenerationPattern** - Assembly logic
   - `type` (jinja2 | demonstration | template_fill)
   - `template` (Jinja2 template string)
   - `variables` (data bindings)

3. **InputSource** - Context injection (6 types)
   - `content_config` - Load another content config
   - `external_file` - Load JSON/YAML/text from filesystem
   - `git_reference` - Load from git ref (commit, branch, tag)
   - `ephemeral_output` - Load previously generated content
   - `inline_data` - Embed JSON data directly
   - `artifact_config` - Load artifact config metadata

4. **ChildReference** - Modular composition
   - `id`, `path` (to content config)
   - `required`, `order` (assembly sequence)
   - `retrievalStrategy` (latest | specific version)

5. **Ephemeral Storage** - Versioned content cache
   - Pattern: `ephemeral/{content_id}/{timestamp}.{format}`
   - Timestamp-based versioning
   - Session-level caching

**MCP Integration**: 17 tools for conversational generation via Claude Desktop

### Integration Mapping

**Inbox Artifact Types → chora-compose Content Types**:

| Inbox Artifact | chora-compose Mapping | Complexity |
|----------------|----------------------|------------|
| Coordination Request | Artifact Config (5-7 content elements) | Medium |
| Implementation Task | Artifact Config (5-7 content elements) | Medium |
| Strategic Proposal | Artifact Config (8-10 content elements) | High |
| Triage Decision | Content Config (template_fill) | Low |
| Change Request (DDD) | Content Config (Jinja2) | Medium-High |
| Completion Summary | Content Config (demonstration) | Low |

**Inbox Workflows → chora-compose Collections**:

```
Collection: Coordination Request Lifecycle
├─ Stage 1: Request Generation (automated via MCP)
│  └─ Content configs: core-metadata, context-fields, deliverables, acceptance-criteria
├─ Stage 2: Triage Decision (semi-automated template)
│  └─ Content config: triage-decision
├─ Stage 3: Change Request (automated from criteria)
│  └─ Content config: change-request-ddd
└─ Stage 4: Fulfillment Tracking (automated from events)
   └─ Content config: completion-summary
```

**Transformation Points** (Manual → Automated):

1. **Request Creation**: Hand-write 200-line JSON → MCP conversational generation (5-10 min)
2. **Context Injection**: Manual research → Auto-populate from `.chorabase.json`, `sap-catalog.json`, `events.jsonl`
3. **Template Reuse**: Copy-paste from previous → Content blocks shared across ecosystem
4. **Validation**: Manual review → JSON Schema validation + automated quality checks

### Gap Analysis

**chora-compose Features Needed (from COORD-2025-002-CLARIFICATION)**:

1. **Force parameter at ArtifactComposer level**
   - Status: Only in MCP tools, not in ArtifactComposer
   - Effort: 2-3 hours
   - Priority: Medium
   - Workaround: Call MCP tool with `force=True`

2. **retrievalStrategy wiring in ArtifactComposer**
   - Status: Defined in ChildReference but not enforced
   - Effort: 2-4 hours
   - Priority: Medium
   - Workaround: Manual orchestration via external_file references

3. **Staleness detection** (TTL, input hash comparison)
   - Status: Not implemented
   - Effort: 6-8 hours
   - Priority: Low (not critical for pilot)
   - Workaround: User-driven regeneration

4. **HTTP URL sources**
   - Status: Not supported
   - Effort: 2-3 hours
   - Priority: Low (git_reference sufficient)

**Total Gap-Closing Effort**: 8-13 hours (within pilot scope, non-blocking)

**Inbox Protocol Requirements vs chora-compose Patterns**:

| Requirement | chora-compose Pattern | Conflict? | Solution |
|-------------|----------------------|-----------|----------|
| JSON Schema validation | Pydantic validation on configs | No | Post-generation validation using jsonschema library |
| Sequential ID generation | User-defined content IDs | No | ID allocation logic in generation context |
| Event emission | No built-in event emission | No | Custom generator wrapper |
| Directory structure | Flexible output paths in artifact metadata | No | Artifact config specifies inbox-compatible paths |

**No fundamental conflicts identified**. All inbox requirements can be met with custom wrappers or configuration.

### Feasibility Assessment

**Technical Feasibility: HIGH (90%)**

Strong alignment factors:
- ✅ Both systems are JSON/YAML config-driven
- ✅ Both use template-based generation (Jinja2 compatible)
- ✅ Both support modular composition (content blocks → artifacts)
- ✅ Both have MCP integration
- ✅ Both support context-aware generation

Minor gaps (8-13 hours total):
- Force parameter wiring (2-3 hours)
- retrievalStrategy enforcement (2-4 hours)
- Post-generation validation and event emission (4-6 hours)

**Quality Feasibility: MEDIUM-HIGH (75%)**

Success factors:
- ✅ SAP-004 pilot provides quality validation framework (80%+ threshold)
- ✅ Inbox artifacts are more structured than prose (easier to template)
- ✅ JSON Schema validation ensures structural correctness
- ✅ Demonstration generator provides deterministic quality baseline

Risk factors:
- ❌ Generated text coherence (mitigated by ContentElement composition)
- ❌ Context completeness (requires good repo metadata)
- ❌ Edge cases and special requests (may need manual override)

Mitigation: Start with template_fill (deterministic), iterate to AI-based generation for flexibility

**Maintenance Feasibility: HIGH (85%)**

Long-term sustainability:
- ✅ Content blocks in chora-base (domain expertise maintained by team)
- ✅ Configs version-controlled (evolution tracking)
- ✅ Generated artifacts are reviewable (git diff)
- ✅ Update content block once → regenerate all affected artifacts

Effort estimates:
- Current manual: 30-60 min per coord request, 15-30 min per task
- With chora-compose: 5-10 min per artifact (70-80% reduction)
- Maintenance: 2-4 hours/month (vs 10-20 hours manual)

**Ecosystem Feasibility: HIGH (90%)**

Ecosystem benefits:
- ✅ chora-workspace can use same patterns
- ✅ ecosystem-manifest can generate coord requests to chora-base
- ✅ Shared content blocks reduce duplication
- ✅ Pilot project already approved (COORD-2025-002)

Collaboration readiness:
- ✅ Communication patterns established (inbox protocol, async iteration)
- ✅ Go/no-go decision point (~Nov 19) provides exit strategy

### Efficiency Gains (Projected)

**Time Reduction**:
- Coordination request: 30-60 min → 5-10 min (70-83% reduction)
- Implementation task: 15-30 min → 3-5 min (80-83% reduction)
- Triage decision: 10-15 min → 2-3 min (80-85% reduction)

**Maintenance Reduction**:
- Template updates: 10-20 hours/month → 2-4 hours/month (80% reduction)
- New artifact type setup: 4-6 hours → 1-2 hours (66% reduction)

**Quality Improvements**:
- Structural consistency: Improved (JSON Schema validation)
- Completeness: Improved (template ensures all required fields)
- Traceability: Improved (automated trace_id propagation)

**Ecosystem Multiplier**:
- Same patterns for SAP generation (18 SAPs × 5 artifacts = 90 documents)
- Same patterns for other repos (chora-workspace, ecosystem-manifest, etc.)
- Shared content block library reduces duplication

## Open Questions

### For chora-compose Team (via COORD-2025-002)

1. **Force parameter**: Can this be wired at ArtifactComposer level?
2. **retrievalStrategy**: When will this be fully implemented?
3. **Content config authoring**: Best practices for complex JSON generation?
4. **Validation hooks**: Where should JSON Schema validation occur?

### For chora-base Team

1. **Pilot scope**: Start with coordination requests only, or include tasks?
2. **Quality threshold**: Is 80% sufficient, or higher bar needed?
3. **Migration strategy**: Parallel operation (manual + automated), or cutover?
4. **Content block ownership**: Who maintains the content block library?

## Recommendations

### Primary Recommendation: PROCEED TO PILOT

**Rationale**:
1. **Exceptional strategic alignment** between systems (90% technical feasibility)
2. **Proven technology** (17 production generators, MCP integration)
3. **Low integration effort** (8-13 hours to close minor gaps)
4. **High ROI** (70-83% time reduction, 80% maintenance reduction)
5. **Ecosystem multiplier** (benefits SAP generation + inbox coordination)

**Recommended Pilot Scope**:
- **Artifact type**: Coordination requests only (medium complexity, high value)
- **Timeline**: 4 weeks (Nov 4-29, 2025)
- **Success criteria**: 80%+ quality, 50%+ time reduction, 100% schema validation
- **Decision point**: Week 4 (Nov 29) - GO/PARTIAL/NO-GO

**Leverage SAP-004 Pilot**: Extend approved SAP-004 pilot to include inbox artifact generation

### Alternative Options (If Pilot Deferred)

**Option A**: Storage-based approach (v4.1.0 SAP sets)
- Use chora-compose for SAP generation only
- Continue manual inbox artifact creation
- Revisit inbox automation in v4.3.0 (Q2 2026)

**Option B**: Wrapper/adapter layer
- Build custom wrapper around chora-compose
- More control, higher effort (30-40 hours)
- Useful if chora-compose lacks critical features

**Option C**: Alternative tool exploration
- Evaluate other template-driven generation tools
- Higher risk, longer timeline (8-12 weeks)

## Next Steps

### Immediate Actions (Week 1: Nov 4-8)

1. **Complete Phase 1 Documentation** (in progress)
   - ✅ Exploration summary (this document)
   - ⏳ Architecture analysis document
   - ⏳ Integration options document

2. **Review with Team**
   - Share findings with chora-base team
   - Discuss pilot scope and timeline
   - Make GO/NO-GO decision on pilot

3. **If GO: Create Pilot Plan** (Phase 2)
   - Detailed pilot plan document
   - Content block design document
   - Timeline with decision points

### Phase 1 Decision Criteria

**GO to Pilot if**:
- ✅ Technical feasibility HIGH (≥80%)
- ✅ Team capacity available (20-30 hours over 4 weeks)
- ✅ SAP-004 pilot shows positive results
- ✅ chora-compose team responsive to COORD-2025-002

**NO-GO if**:
- ❌ Technical feasibility LOW (<60%)
- ❌ Team capacity insufficient
- ❌ SAP-004 pilot quality <70%
- ❌ chora-compose team lacks capacity for collaboration

**DEFER if**:
- ⚠️ Technical feasibility MEDIUM (60-79%)
- ⚠️ Need to address blockers first
- ⚠️ SAP-004 pilot needs more iteration

## References

### Key Documents

- **Inbox Protocol**: `/inbox/INBOX_PROTOCOL.md` (831 lines)
- **Intake Triage Guide**: `/inbox/INTAKE_TRIAGE_GUIDE.md` (836 lines)
- **Development Lifecycle**: `/docs/skilled-awareness/development-lifecycle/protocol-spec.md` (808 lines)
- **SAP Framework**: `/docs/skilled-awareness/sap-framework/protocol-spec.md`
- **SAP Catalog**: `/sap-catalog.json` (26 SAPs)

### Coordination Artifacts

- **COORD-2025-002**: Exploratory request to chora-compose
- **COORD-2025-002-CLARIFICATION**: Follow-up questions about chora-compose architecture
- **SAP-004 Pilot**: chora-compose SAP generation pilot (approved, ~Nov 6 start)

### Example Workflows

- **Health Monitoring W3**: Complete strategic → tactical flow example
  - `/inbox/examples/health-monitoring-w3/`
- **Task Completion**: DDD → BDD → TDD example
  - `/inbox/completed/dry-run-20251027-task-301-broadcast-template/`

## Exploration Metadata

**Status**: In Progress (Phase 1 of 8)

**Timeline**:
- Exploration started: Nov 2, 2025
- Expected completion: Nov 8, 2025 (Week 1)
- Decision point: Nov 8, 2025 (GO/NO-GO to pilot)

**Contributors**:
- Victor (chora-base)
- Claude Code Agent (research and analysis)

**Trace Context**: `chora-compose-inbox-integration-2025`

**Events**:
- 2025-11-02: exploration_started

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Next Review**: 2025-11-08 (Phase 1 decision point)
