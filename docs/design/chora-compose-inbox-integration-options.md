---
title: Chora-Compose Inbox Integration - Options Analysis
type: options-analysis
trace_id: chora-compose-inbox-integration-2025
created: 2025-11-02
status: in_progress
---

# Integration Options: Chora-Compose as Inbox Protocol Infrastructure

## Executive Summary

This document evaluates three integration approaches for using chora-compose as the infrastructure layer for SAP-001 (Inbox Coordination Protocol). Each option is analyzed for effort, benefits, risks, and suitability.

**Recommended Option**: **Option A (Direct Integration)** - Highest ROI, lowest risk, leverages proven technology with pilot validation.

## Option A: Direct Integration via Content Configs (RECOMMENDED)

### Overview

Use chora-compose content generation framework directly to generate inbox artifacts through template-driven content configs and MCP integration.

### Architecture

```
User Request (MCP or CLI)
         ↓
chora-compose MCP Tool: generate_content()
         ↓
Content Configs (chora-base/configs/content/)
├─ coordination-request/core-metadata.json
├─ coordination-request/context-fields.json
├─ coordination-request/deliverables.json
└─ coordination-request/acceptance-criteria.json
         ↓
Artifact Composer (chora-compose)
├─ Resolve InputSources (repo metadata, git refs, etc.)
├─ Execute GenerationPatterns (Jinja2, demonstration, template_fill)
└─ Assemble ContentElements
         ↓
Ephemeral Storage: drafts/coordination/draft-XYZ.json
         ↓
Post-Processing Wrapper (chora-base)
├─ JSON Schema validation
├─ Sequential ID allocation
├─ Event emission (events.jsonl)
└─ Promotion to inbox/incoming/coordination/
         ↓
Final Artifact: inbox/incoming/coordination/coord-NNN.json
```

### Implementation Details

**Phase 1: Pilot (4 weeks)**
- Artifact type: Coordination requests only
- Scope: 3-5 test generations
- Success criteria: 80%+ quality, 50%+ time reduction, 100% schema validation

**Phase 2: Expansion (4-6 weeks, if pilot successful)**
- Add implementation tasks
- Add triage decisions
- Add change requests (DDD)

**Phase 3: Full Integration (8-12 weeks)**
- Add strategic proposals
- Add completion summaries
- Ecosystem adoption (share content block library)

### Effort Estimate

**Setup (One-Time)**:
- Content block decomposition: 4-6 hours
- Content config authoring: 6-8 hours
- Post-processing wrapper (validation, events): 4-6 hours
- Testing and documentation: 4-6 hours
- **Total**: 18-26 hours

**Per-Artifact Type**:
- Content block design: 2-3 hours
- Content config creation: 2-4 hours
- Testing and validation: 1-2 hours
- **Total**: 5-9 hours per artifact type

**Pilot (4 weeks)**:
- Coordination request setup: 18-26 hours
- 3-5 test generations: 6-10 hours
- Quality assessment: 4-6 hours
- **Total**: 28-42 hours

**Full Implementation (3 artifact types)**:
- Coordination requests: 18-26 hours (pilot)
- Implementation tasks: 10-15 hours
- Strategic proposals: 12-18 hours
- **Total**: 40-59 hours

### Benefits

**Time Reduction**:
- ✅ Coordination request: 30-60 min → 5-10 min (70-83% reduction)
- ✅ Implementation task: 15-30 min → 3-5 min (80-83% reduction)
- ✅ Triage decision: 10-15 min → 2-3 min (80-85% reduction)

**Quality Improvements**:
- ✅ Structural consistency (JSON Schema validation)
- ✅ Completeness (template ensures all required fields)
- ✅ Traceability (automated trace_id propagation)

**Maintenance Benefits**:
- ✅ Update content block once → regenerate all affected artifacts
- ✅ Template reuse across ecosystem (chora-workspace, ecosystem-manifest)
- ✅ Maintenance: 2-4 hours/month (vs 10-20 hours manual)

**Ecosystem Multiplier**:
- ✅ Same patterns for SAP generation (18 SAPs × 5 artifacts = 90 documents)
- ✅ Shared content block library reduces duplication
- ✅ MCP integration enables conversational generation

### Risks

**Risk 1: Generated Quality Below 80% Threshold**
- **Likelihood**: Medium
- **Impact**: High (blocks full adoption)
- **Mitigation**: Start with template_fill (deterministic), iterate to AI-based
- **Fallback**: Use automated for simple fields, manual for complex

**Risk 2: Context Incompleteness**
- **Likelihood**: Medium-High
- **Impact**: Medium (lower quality but still usable)
- **Mitigation**: Define minimal required context (repo_metadata.json)
- **Fallback**: Provide defaults, allow user override

**Risk 3: Integration Breaks Existing Workflows**
- **Likelihood**: Low
- **Impact**: High (disrupts operations)
- **Mitigation**: Extensive testing, parallel operation during pilot
- **Fallback**: Roll back, continue manual process

### Dependencies

**chora-compose Features** (from COORD-2025-002-CLARIFICATION):
- ✅ Content configs with InputSources (EXISTS)
- ✅ Artifact composition (EXISTS)
- ✅ MCP integration (EXISTS)
- ⚠️ Force parameter at ArtifactComposer level (MISSING, 2-3 hours)
- ⚠️ retrievalStrategy wiring (MISSING, 2-4 hours)
- ❌ Staleness detection (NOT CRITICAL for pilot)

**chora-base Infrastructure**:
- ✅ JSON schemas (exist)
- ✅ inbox-status.py (exists)
- ✅ Event logging (exists)
- ❌ Post-processing wrapper (NEED TO BUILD, 4-6 hours)
- ❌ Content block library (NEED TO BUILD, 4-6 hours)

**Total Gap-Closing Effort**: 8-13 hours (within pilot scope)

### Success Criteria

**Pilot Success** (Week 4 decision):
- ✅ Generated artifacts validate against JSON Schema (100%)
- ✅ Content quality ≥80% vs hand-written examples
- ✅ inbox-status.py can parse artifacts (100%)
- ✅ Event tracing works correctly (100%)
- ✅ Time reduction ≥50% (30-60 min → ≤15 min)

**Full Integration Success** (v4.2.0):
- ✅ All 3 artifact types supported
- ✅ Quality maintained ≥80% across all types
- ✅ Team adoption ≥80% (prefer automated over manual)
- ✅ Ecosystem adoption (≥1 other repo using patterns)

### Recommendation

**PROCEED TO PILOT** with Option A

**Rationale**:
1. **Exceptional alignment** (90% technical feasibility)
2. **Proven technology** (17 production generators, MCP integration)
3. **Low integration effort** (8-13 hours to close gaps)
4. **High ROI** (70-83% time reduction, 80% maintenance reduction)
5. **Ecosystem multiplier** (benefits SAP generation + inbox coordination)
6. **Clear exit strategy** (pilot go/no-go decision at Week 4)

---

## Option B: Wrapper/Adapter Layer

### Overview

Build a custom wrapper around chora-compose that provides inbox-specific abstractions and additional control.

### Architecture

```
User Request (CLI or API)
         ↓
Inbox Artifact Generator Wrapper (chora-base)
├─ Parse user request
├─ Validate context
├─ Allocate sequential ID
└─ Map to chora-compose concepts
         ↓
chora-compose Adapter Layer
├─ Translate inbox concepts → content configs
├─ Inject inbox-specific context
└─ Call chora-compose generation
         ↓
chora-compose (as library)
         ↓
Generated Content (in-memory)
         ↓
Inbox Artifact Generator Wrapper
├─ JSON Schema validation
├─ Quality checks (custom rules)
├─ Event emission
├─ File placement
└─ Git commit (optional)
         ↓
Final Artifact: inbox/incoming/coordination/coord-NNN.json
```

### Implementation Details

**Wrapper Components**:

1. **Inbox Artifact Generator CLI**
```bash
chora-base inbox generate coordination \
  --from-repo ecosystem-manifest \
  --to-repo chora-base \
  --priority P0 \
  --title "Health endpoint template" \
  --deliverables "Template,Documentation,Example" \
  --trace-id ecosystem-w3-health
```

2. **Adapter Layer** (`chora_base/inbox/generators/adapter.py`)
```python
class ChoraComposeAdapter:
    """
    Translate inbox concepts to chora-compose content configs
    """

    def generate_coordination_request(self, context: dict) -> dict:
        """
        Generate coordination request using chora-compose
        """
        # Map inbox context → content config context
        config_context = self._map_context(context)

        # Call chora-compose
        result = chora_compose.generate_content(
            config_id="coordination-request",
            context=config_context
        )

        # Post-process
        validated = self._validate(result["output"])
        self._emit_event(validated, context["trace_id"])

        return validated
```

3. **Custom Quality Checks**
```python
def check_deliverables_quality(deliverables: list) -> dict:
    """
    Custom quality checks beyond JSON Schema
    """
    issues = []

    for d in deliverables:
        # Too vague?
        if len(d.split()) < 3:
            issues.append(f"Deliverable too vague: '{d}'")

        # Missing specificity?
        if "TODO" in d or "TBD" in d:
            issues.append(f"Deliverable incomplete: '{d}'")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
```

### Effort Estimate

**Setup (One-Time)**:
- Wrapper CLI design: 4-6 hours
- Adapter layer implementation: 8-12 hours
- Custom quality checks: 4-6 hours
- Testing and documentation: 6-8 hours
- **Total**: 22-32 hours

**Per-Artifact Type**:
- Adapter logic: 3-5 hours
- Quality checks: 2-3 hours
- Testing: 2-3 hours
- **Total**: 7-11 hours per artifact type

**Pilot (4 weeks)**:
- Wrapper + adapter: 22-32 hours
- Coordination request logic: 7-11 hours
- 3-5 test generations: 6-10 hours
- Quality assessment: 4-6 hours
- **Total**: 39-59 hours

**Full Implementation (3 artifact types)**:
- Wrapper + adapter: 22-32 hours (one-time)
- Coordination requests: 7-11 hours
- Implementation tasks: 7-11 hours
- Strategic proposals: 10-15 hours (more complex)
- **Total**: 46-69 hours

### Benefits

**More Control**:
- ✅ Custom quality checks beyond JSON Schema
- ✅ Inbox-specific CLI (simpler interface)
- ✅ Fine-grained error handling
- ✅ Custom retry logic

**Better Debugging**:
- ✅ Clearer error messages (inbox-focused)
- ✅ Step-by-step logging
- ✅ Intermediate state inspection

**Flexibility**:
- ✅ Can swap chora-compose for alternative generator
- ✅ Gradual adoption (wrapper can use manual fallback)
- ✅ Custom generation strategies

### Risks

**Risk 1: Higher Effort**
- **Likelihood**: High
- **Impact**: Medium (delays pilot)
- **Mitigation**: Start with minimal wrapper, iterate
- **Fallback**: Simplify to thin wrapper (closer to Option A)

**Risk 2: Maintenance Burden**
- **Likelihood**: Medium
- **Impact**: Medium (more code to maintain)
- **Mitigation**: Keep wrapper thin, delegate to chora-compose
- **Fallback**: Deprecate wrapper, use chora-compose directly

**Risk 3: Complexity**
- **Likelihood**: Medium
- **Impact**: Low (team learning curve)
- **Mitigation**: Good documentation, examples
- **Fallback**: Simplify interface

### Dependencies

**Same as Option A**, plus:
- ❌ Wrapper implementation (22-32 hours)
- ❌ CLI design and UX (4-6 hours)
- ❌ Custom quality checks (4-6 hours)

**Total Gap-Closing Effort**: 38-57 hours (vs 8-13 hours for Option A)

### Success Criteria

**Same as Option A**, plus:
- ✅ Wrapper CLI is intuitive (user testing)
- ✅ Custom quality checks catch issues (≥90% precision)
- ✅ Debugging experience is good (clear error messages)

### Recommendation

**DEFER** - Consider only if Option A fails pilot

**Rationale**:
1. **Higher effort** (38-57 hours vs 8-13 hours)
2. **More complexity** (additional layer to maintain)
3. **Unclear benefits** (Option A may be sufficient)
4. **Premature optimization** (build wrapper only if direct integration has issues)

**When to Reconsider**:
- If Option A pilot shows chora-compose lacks critical features
- If custom quality checks prove essential (not just nice-to-have)
- If CLI abstraction significantly improves UX (validated by user testing)

---

## Option C: Continue Manual Approach (Baseline)

### Overview

Keep current manual JSON creation process, no integration with chora-compose.

### Architecture

```
User (human)
         ↓
Text Editor (vim, VS Code)
├─ Hand-write JSON (30-60 min)
├─ Reference previous examples
└─ Copy-paste and modify
         ↓
Manual Validation
├─ Run jsonschema validate
├─ Visual inspection
└─ Review with team
         ↓
Manual Event Emission
├─ Hand-write event JSON
└─ Append to events.jsonl
         ↓
Git Commit
         ↓
Final Artifact: inbox/incoming/coordination/coord-NNN.json
```

### Implementation Details

**No changes** - current process continues

**Current Workflow**:
1. User identifies need for coordination request
2. Copy previous example (`coord-001.json`)
3. Edit in text editor (30-60 minutes)
4. Validate: `jsonschema validate coord-042.json --schema coordination-request.schema.json`
5. Manually emit event to `events.jsonl`
6. Git commit

### Effort Estimate

**Setup (One-Time)**: 0 hours (status quo)

**Per-Artifact**:
- Coordination request: 30-60 min
- Implementation task: 15-30 min
- Strategic proposal: 1-2 hours

**Maintenance**:
- Template updates: 10-20 hours/month (scattered across team)
- New artifact type: 4-6 hours (create example, document)

### Benefits

**No Integration Effort**:
- ✅ Zero setup time
- ✅ No dependency on chora-compose
- ✅ No learning curve

**Maximum Flexibility**:
- ✅ Can handle any edge case
- ✅ No constraints from templates
- ✅ Full control over content

**Simplicity**:
- ✅ No new tools to learn
- ✅ No additional moving parts
- ✅ Clear what's happening (direct editing)

### Risks

**Risk 1: No Efficiency Gains**
- **Likelihood**: High (certain)
- **Impact**: High (missed opportunity)
- **Cost**: 30-60 min per coordination request (ongoing)

**Risk 2: Inconsistency**
- **Likelihood**: Medium
- **Impact**: Medium (quality variance)
- **Example**: Some coords have detailed deliverables, others are vague

**Risk 3: High Cognitive Load**
- **Likelihood**: High (certain)
- **Impact**: Medium (team fatigue)
- **Example**: Remembering all 18 required fields, ensuring completeness

**Risk 4: No Template Reuse**
- **Likelihood**: High (certain)
- **Impact**: Medium (duplication across repos)
- **Example**: Each repo creates their own coordination request patterns

### Dependencies

**None** - status quo

### Success Criteria

**Not applicable** - this is the baseline

### Recommendation

**REJECT** - Use only as fallback if Option A pilot fails

**Rationale**:
1. **No efficiency gains** (30-60 min per artifact, ongoing)
2. **Missed opportunity** (chora-compose alignment proven)
3. **High maintenance burden** (10-20 hours/month)
4. **No ecosystem benefits** (each repo duplicates effort)
5. **Pilot de-risks Option A** (low-cost validation)

**When to Use**:
- As fallback for edge cases (custom one-off requests)
- During Option A pilot (parallel operation)
- If Option A pilot fails quality threshold (<70%)

---

## Option Comparison Matrix

| Criterion | Option A: Direct Integration | Option B: Wrapper/Adapter | Option C: Manual (Baseline) |
|-----------|----------------------------|---------------------------|---------------------------|
| **Setup Effort** | 18-26 hours | 39-59 hours | 0 hours |
| **Per-Artifact Effort** | 5-10 min | 10-15 min | 30-60 min |
| **Time Reduction** | 70-83% | 60-75% | 0% (baseline) |
| **Maintenance** | 2-4 hours/month | 4-8 hours/month | 10-20 hours/month |
| **Quality Consistency** | High (template-driven) | Very High (custom checks) | Medium (human variance) |
| **Flexibility** | High (content configs) | Very High (custom logic) | Maximum (direct editing) |
| **Ecosystem Reuse** | High (shared content blocks) | Medium (wrapper is chora-base-specific) | Low (manual duplication) |
| **Complexity** | Low (leverage chora-compose) | Medium (additional layer) | Low (direct editing) |
| **Dependencies** | chora-compose (8-13 hours gaps) | chora-compose + wrapper (38-57 hours) | None |
| **Risk** | Low-Medium (pilot validates) | Medium (more moving parts) | Low (status quo) |
| **ROI** | Very High (83% reduction, ecosystem multiplier) | Medium-High (75% reduction, more control) | Zero (no change) |

---

## Decision Framework

### Decision Criteria

**Effort vs Benefit**:
- Option A: 18-26 hours setup → 70-83% ongoing reduction → **Best ROI**
- Option B: 39-59 hours setup → 60-75% ongoing reduction → **Medium ROI**
- Option C: 0 hours setup → 0% ongoing reduction → **No ROI**

**Technical Feasibility**:
- Option A: High (90%) - chora-compose proven, minor gaps
- Option B: High (85%) - more control, more complexity
- Option C: High (100%) - status quo

**Quality Confidence**:
- Option A: Medium-High (75%) - pilot will validate 80%+ threshold
- Option B: High (85%) - custom quality checks increase confidence
- Option C: Medium (60%) - human variance, no validation

**Ecosystem Value**:
- Option A: Very High - shared content blocks, MCP integration, SAP generation synergy
- Option B: Medium - wrapper is chora-base-specific, less reusable
- Option C: Low - manual duplication across repos

**Risk Profile**:
- Option A: Low-Medium - pilot provides exit strategy, gaps are closable
- Option B: Medium - more code to maintain, longer timeline
- Option C: Low - status quo, no change risk

### Recommended Decision Path

**Phase 1: Exploration (Week 1)** ✅ Current Phase
- Complete exploration documentation
- Review with team
- Make GO/NO-GO decision on pilot

**If GO: Phase 2: Pilot (Weeks 2-4)**
- Execute Option A pilot
- 3-5 test coordination request generations
- Measure quality (≥80% threshold)
- Validate integration (inbox-status.py, events)

**Decision Point (Week 4):**
- **If pilot successful (quality ≥80%)**: Proceed with Option A full implementation
- **If pilot marginal (quality 70-79%)**: Consider Option B (wrapper for more control)
- **If pilot fails (quality <70%)**: Fall back to Option C (manual), revisit in Q2 2026

**If SUCCESSFUL: Phase 3: Full Implementation (Weeks 5-12)**
- Expand to implementation tasks
- Expand to strategic proposals
- Ecosystem adoption (share content block library)

---

## Detailed Recommendation: Option A (Direct Integration)

### Why Option A?

**1. Exceptional Strategic Alignment**
- chora-compose architecture (content generation, modular composition, MCP integration) perfectly matches inbox protocol needs (structured artifacts, workflow orchestration, automation)
- Both systems are JSON/YAML config-driven
- Both support template-based generation (Jinja2)
- Both have MCP integration

**2. Proven Technology**
- 17 production generators in chora-compose
- MCP integration working and tested
- Demonstrated quality in other use cases (SAP-004 pilot)

**3. Low Integration Effort**
- 8-13 hours to close minor gaps (force parameter, retrievalStrategy, validation wrapper)
- 18-26 hours total pilot setup
- Clear path to full implementation

**4. High ROI**
- 70-83% time reduction per artifact
- 80% maintenance reduction
- Ecosystem multiplier (SAP generation + inbox coordination)

**5. Clear Exit Strategy**
- Pilot provides go/no-go decision at Week 4
- Can fall back to Option C if quality threshold not met
- Parallel operation during pilot (manual + automated coexist)

### Implementation Roadmap

**Week 1: Exploration** ✅
- ✅ Exploration summary document
- ✅ Architecture analysis document
- ✅ Integration options document (this doc)
- ⏳ Team review and GO/NO-GO decision

**Week 2: Pilot Planning**
- Create pilot plan document
- Design content blocks for coordination requests
- Define success metrics and data collection

**Week 3: Pilot Execution (DDD)**
- Create change request (Diátaxis format)
- Design content configs
- Implement content blocks

**Week 4: Pilot Execution (BDD + TDD) + Validation**
- Create BDD scenarios
- Implement content configs and wrapper
- Generate 3-5 test coordination requests
- Measure quality and make go/no-go decision

**Weeks 5-8: Full Implementation (If Successful)**
- Expand to implementation tasks
- Expand to strategic proposals
- Ecosystem adoption

### Success Metrics (Pilot)

**Quantitative**:
- ✅ Schema validation: 100% (must pass)
- ✅ Quality score: ≥80% vs hand-written
- ✅ Time reduction: ≥50% (30-60 min → ≤15 min)
- ✅ inbox-status.py integration: 100% (must parse)
- ✅ Event tracing: 100% (must emit correct events)

**Qualitative**:
- ✅ Deliverables are coherent and actionable
- ✅ Acceptance criteria are testable (BDD-ready)
- ✅ Context fields are relevant and accurate
- ✅ Overall readability and usefulness

**Process**:
- ✅ Generation workflow is smooth (no major friction)
- ✅ Error messages are clear and helpful
- ✅ Documentation is sufficient for team adoption

### Risk Mitigation Strategy

**Risk 1: Quality Below 80%**
- Start with template_fill (deterministic)
- Iterate to AI-based generation for flexibility
- Partial adoption: Use for simple fields, manual for complex

**Risk 2: Context Incompleteness**
- Define minimal required context (repo_metadata.json)
- Provide defaults for optional fields
- User can override/supplement context manually

**Risk 3: Integration Breaks Workflows**
- Extensive testing against existing examples
- Parallel operation (manual + automated coexist)
- Validation: inbox-status.py must work without modification

**Risk 4: Team Adoption Low**
- Good documentation and examples
- Hands-on training session
- Feedback loops during pilot

---

## Conclusion

### Summary

**Option A (Direct Integration)** is the clear winner:
- ✅ Highest ROI (83% time reduction, 80% maintenance reduction)
- ✅ Lowest risk (pilot validates, clear exit strategy)
- ✅ Best ecosystem value (shared content blocks, MCP integration)
- ✅ Proven technology (17 production generators, demonstrated quality)
- ✅ Reasonable effort (18-26 hours pilot, 40-59 hours full implementation)

**Option B (Wrapper/Adapter)** is premature optimization:
- ⚠️ Higher effort (39-59 hours vs 18-26 hours)
- ⚠️ More complexity (additional layer to maintain)
- ⚠️ Unclear benefits (Option A may be sufficient)
- ✅ Consider only if Option A pilot shows gaps

**Option C (Manual)** is status quo fallback:
- ❌ No efficiency gains (missed opportunity)
- ❌ High cognitive load (30-60 min per artifact, ongoing)
- ❌ No ecosystem benefits (manual duplication)
- ✅ Use only for edge cases or if Option A fails

### Recommended Decision

**PROCEED TO PILOT (Option A)**

**Next Steps**:
1. **Team review** (Week 1): Review exploration documents, make GO/NO-GO
2. **If GO: Pilot planning** (Week 2): Create pilot plan, design content blocks
3. **Pilot execution** (Weeks 3-4): Generate, validate, measure
4. **Decision point** (Week 4): GO/PARTIAL/NO-GO on full implementation

**Success Probability**: High (90%)
- Technical feasibility: 90% (proven alignment)
- Quality feasibility: 75% (pilot will validate 80%+ threshold)
- Team capacity: High (pilot approved, SAP-004 synergy)
- chora-compose collaboration: High (COORD-2025-002 positive signals)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-02
**Status**: Complete (Phase 1 deliverable)
**Next Review**: 2025-11-08 (with team for GO/NO-GO decision)
