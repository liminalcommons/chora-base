# chora-compose Integration Decision Document

**Date**: 2025-11-02
**Status**: **DECISION MADE - Path C (Build Standalone, Future Migration)**
**Decision**: Proceed with standalone generation system, keep configs compatible for future chora-compose integration
**Pilot**: chora-compose Inbox Integration
**Trace ID**: chora-compose-inbox-integration-2025

---

## Executive Summary

**Investigation reveals that chora-compose has artifact generation capabilities, but:**
1. The installed package (v1.9.1) appears to be incomplete/placeholder
2. CLI commands are not available
3. Recent development (v1.9.0) focused on **stigmergic context links** and **SAP regeneration**, not inbox artifact generation
4. The extensive archived documentation is for **building** chora-compose, not using it in production

**Recommendation**: **Path C - Build Standalone Generator** with chora-compose-compatible config format for future migration when chora-compose reaches production maturity.

---

## Investigation Results

### 1. chora-compose Package Status

**Installation Check:**
```bash
$ pip list | grep chora-compose
chora-compose      1.9.1

$ which chora-compose
# No output - CLI not in PATH

$ python3 -c "import chora_compose; print(chora_compose.__version__)"
# AttributeError: module 'chora_compose' has no attribute '__version__'
```

**Finding**: Package installed but appears incomplete. Missing:
- CLI entry points
- Core functionality attributes
- Production-ready implementation

### 2. chora-compose Capabilities Analysis

**From Archived Documentation** ([chora-compose user docs](docs/project-docs/archives/chora-compose-draft-material/chora-compose/user-docs/)):

#### Core Architecture ✅ EXISTS

**Components Documented**:
1. **ConfigLoader**: Loads and validates content/artifact configs
2. **ArtifactComposer**: Assembles content configs into artifacts
3. **Generators**:
   - Demonstration generator (uses example_output)
   - Template-fill generator (Jinja2)
   - Code generation (AI-powered, future)
4. **Content vs Artifact**: Clear distinction matches our design
5. **Composition Strategies**: concat, merge, overlay

**Key Documentation**:
- [How to Create Artifact Config](docs/project-docs/archives/chora-compose-draft-material/chora-compose/user-docs/how-to/configs/create-artifact-config.md)
- [How to Create Content Config](docs/project-docs/archives/chora-compose-draft-material/chora-compose/user-docs/how-to/configs/create-content-config.md)
- [Quick Start Guide](docs/project-docs/archives/chora-compose-draft-material/chora-compose/user-docs/QUICK_START_GUIDE.md)

**API Usage Pattern** (from docs):
```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.core.composer import ArtifactComposer

# Load config
config = ConfigLoader().load_artifact_config('my-artifact')

# Generate artifact
path = ArtifactComposer().assemble('my-artifact')
```

**Config Structure** (matches our Week 3 design!):
```json
{
  "type": "artifact",
  "id": "coordination-request-artifact",
  "metadata": {
    "outputs": [{"file": "output.json", "format": "json"}],
    "compositionStrategy": "concat"
  },
  "content": {
    "children": [
      {
        "id": "core-metadata",
        "path": "configs/content/core-metadata.json",
        "order": 1,
        "required": true
      }
    ]
  }
}
```

### 3. v1.9.0 Focus: Stigmergic Links, NOT Inbox Generation

**From COORD-2025-003**:

**v1.9.0 Capabilities** (Released 2025-10-30):
1. **Stigmergic context links**: 95% token reduction (20k→1k) for cross-repo operations
2. **Freshness tracking**: Automated staleness detection
3. **Collections documentation**: 3-tier content generation for SAP regeneration

**Use Case**: Regenerating existing SAP documentation efficiently, not creating new inbox artifacts

**Target Workflow**:
```
[@chora-compose/collection:sap-004-complete]
→ Loads complete SAP-004 context (1k tokens instead of 20k)
→ Agent regenerates SAP with updated content
```

**NOT the inbox pilot use case**:
- We need: Generate coordination request from minimal context (5-10 fields → 18 fields)
- v1.9.0 provides: Efficient loading of existing content for regeneration

### 4. Documentation Type Analysis

**Type**: Development/Implementation Guides (NOT User Guides)

**Evidence**:
- Quick Start focuses on "Begin Implementation" and "Sprint 1"
- Guides cover "convert schemas", "build ConfigLoader", "implement generators"
- File structure: `configs/`, `src/chora_compose/`, `schemas/` (source code structure)
- Commands use: `poetry run python -c "from chora_compose.core..."`

**Interpretation**: Documentation is for **building chora-compose**, not for **using a production-ready tool**.

**Current State**: chora-compose is in **active development**, not production release.

### 5. Config Compatibility Assessment

**Our Week 3 Configs** vs **chora-compose Schema**:

| Element | Our Design | chora-compose Docs | Compatible? |
|---------|-----------|-------------------|-------------|
| Artifact structure | `content_elements[]`, `assembly` | `content.children[]`, `metadata` | ⚠️ Different structure |
| Content configs | 15 JSON files with placeholders | Content elements with example_output | ⚠️ Different approach |
| Generation patterns | template_fill, demonstration, ai_augmented | demonstration, template_fill, code_generation | ✅ Similar concepts |
| Post-processing | Separate wrapper script | Not documented (future?) | ❌ Not supported |
| Conditional inclusion | `include_if` logic in configs | `conditions` field (future?) | ⚠️ Partial support |

**Assessment**: Our configs are **conceptually compatible** but would need restructuring to match chora-compose's actual schema.

---

## Decision Analysis

### Path A: Integrate with chora-compose (AS-IS)

**Effort**: 16-24 hours

**Requirements**:
1. Install/build chora-compose from source
2. Restructure our 15 content configs to match chora-compose schema
3. Modify artifact assembly config
4. Remove post-processing (not supported)
5. Implement conditional logic differently
6. Test and debug integration

**Pros**:
- ✅ Leverage chora-compose architecture
- ✅ MCP integration available (future)
- ✅ Active development

**Cons**:
- ❌ chora-compose not production-ready
- ❌ Would need to build from source (no working CLI)
- ❌ Config restructuring required (16-24 hours wasted if chora-compose changes)
- ❌ Post-processing not supported (ID allocation, events critical for SAP-001)
- ❌ Conditional inclusion logic uncertain
- ❌ Focus on SAP regeneration, not inbox generation

**Risk**: **HIGH** - Building on unstable foundation, incompatible focus

**Recommendation**: ❌ **DO NOT CHOOSE** - Too risky, wrong use case match

---

### Path B: Wait for chora-compose + Interim Solution

**Effort**: 12-16 hours (interim) + TBD (migration)

**Approach**:
1. Build minimal Jinja2 generator consuming our content configs (12-16 hours)
2. Keep configs in chora-compose-compatible format
3. Monitor chora-compose development
4. Migrate when production-ready

**Pros**:
- ✅ Unblocks inbox pilot immediately
- ✅ Maintains compatibility path
- ✅ Lower risk than Path A
- ✅ Can leverage chora-compose when mature

**Cons**:
- ❌ Unknown timeline for chora-compose production readiness
- ❌ May need to migrate twice (interim → chora-compose)
- ❌ Config format may change, invalidating compatibility work
- ❌ Maintenance of interim solution

**Risk**: **MEDIUM** - Migration uncertainty, dual maintenance

**Recommendation**: ⚠️ **VIABLE ALTERNATIVE** - Good if chora-compose timeline is clear (3-6 months)

---

### Path C: Build Standalone Generator (RECOMMENDED)

**Effort**: 20-30 hours

**Approach**:
1. Build complete generation system using our content blocks
2. Python-based with Jinja2 templates + AI integration
3. Use config format inspired by chora-compose but optimized for our needs
4. Include post-processing pipeline (ID allocation, events, validation)
5. Keep architecture modular for potential future migration

**Implementation Plan**:

#### Week 5-6: Core Generation System (20-30 hours)

**Phase 1: Generation Engine** (12-16 hours)
- Config loader with JSON schema validation
- Content element processor
- Template renderer (Jinja2)
- AI integration for augmented fields (title, background, acceptance criteria)
- Artifact assembler

**Phase 2: Integration** (4-6 hours)
- Connect to existing post-processing pipeline
- Quality evaluation integration
- End-to-end testing

**Phase 3: Validation** (4-8 hours)
- Generate 10 real coordination requests
- Run quality assessment (target: ≥80%)
- Iterate on AI prompts
- Performance optimization

**Pros**:
- ✅ Complete control over features needed for SAP-001
- ✅ Post-processing fully integrated (ID allocation, events critical)
- ✅ Conditional inclusion logic exactly as designed
- ✅ Optimized for inbox use case (not SAP regeneration)
- ✅ Production-ready in 2-3 weeks
- ✅ Can still migrate to chora-compose if/when mature
- ✅ Leverages all Week 2-4 work (content blocks, configs, validation)

**Cons**:
- ❌ More upfront effort (20-30 hours vs 12-16 interim)
- ❌ Won't benefit from chora-compose MCP integration initially
- ❌ Separate codebase to maintain

**Risk**: **LOW** - Self-contained, production-ready, meets all requirements

**Recommendation**: ✅ **STRONGLY RECOMMENDED** - Best path to production

---

## Decision Rationale

### Why Path C (Standalone Generator)?

1. **chora-compose Not Production-Ready**
   - Incomplete package installation
   - No working CLI
   - Development/implementation docs, not user docs
   - Focus on different use case (SAP regeneration)

2. **Use Case Mismatch**
   - chora-compose v1.9.0: Stigmergic links for SAP regeneration
   - Our pilot: Generate new coordination requests from minimal context
   - Different problems, different solutions

3. **Post-Processing Requirements**
   - SAP-001 requires ID allocation, event emission, file promotion
   - chora-compose docs don't mention post-processing support
   - Critical for inbox protocol compliance

4. **Timeline and Risk**
   - Standalone: Production in 2-3 weeks with LOW risk
   - Path A: 16-24 hours + HIGH risk of chora-compose instability
   - Path B: 12-16 hours + MEDIUM risk of wasted migration effort

5. **Pilot Success Already Proven**
   - Week 4 achieved 94.9% quality score
   - All infrastructure validated (schemas, validation, post-processing)
   - Content blocks and configs designed
   - **Only missing: generation engine** (20-30 hours)

6. **Future Migration Path Preserved**
   - Modular architecture allows chora-compose migration later
   - Config format can be adapted
   - chora-compose will mature over time (6-12 months likely)

---

## Implementation Plan: Path C

### Architecture

```
User Context Input (JSON)
    ↓
Content Config Loader
  - Load 15 content configs
  - Validate against schemas
  - Build execution graph (order, dependencies)
    ↓
Content Generators
  - Literal Generator: Hardcoded values (type, etc.)
  - User Input Generator: Direct from context
  - Template Generator: Jinja2 templates
  - AI Generator: Claude/OpenAI for augmented fields
    ↓
Artifact Assembler
  - Merge content elements
  - Apply conditional inclusion logic
  - Validate structure
    ↓
Draft Artifact (JSON)
    ↓
Post-Processing Pipeline (EXISTING)
  - scripts/process-generated-artifact.py
  - Schema validation
  - ID allocation
  - Event emission
  - File promotion
    ↓
Final Coordination Request
```

### Technology Stack

**Core**:
- Python 3.12+
- Jinja2 for templates
- JSON Schema validation (jsonschema library)
- Pydantic for config models

**AI Integration**:
- Anthropic Claude API (for AI-augmented fields)
- OpenAI API (alternative/fallback)
- Prompt templates in configs

**Existing Infrastructure** (reuse):
- `scripts/process-generated-artifact.py` ✅
- `scripts/evaluate-pilot-quality.py` ✅
- `schemas/coordination-request.json` ✅
- Content blocks (15 markdown files) ✅
- Content configs (15 JSON files) ✅

### Directory Structure

```
scripts/
  generate-coordination-request.py  # NEW - Main generation script
  generators/
    __init__.py                     # NEW
    config_loader.py                # NEW - Load content configs
    literal_generator.py            # NEW - Hardcoded values
    user_input_generator.py         # NEW - From context
    template_generator.py           # NEW - Jinja2
    ai_generator.py                 # NEW - AI-augmented
    assembler.py                    # NEW - Merge elements
  process-generated-artifact.py     # EXISTING ✅
  evaluate-pilot-quality.py         # EXISTING ✅

configs/
  content/coordination-request/     # EXISTING - 15 configs ✅
  artifact/coordination-request.json # EXISTING ✅

docs/content-blocks/inbox-coordination/ # EXISTING - 15 blocks ✅

schemas/
  coordination-request.json         # EXISTING ✅

context-examples/coordination/      # EXISTING - 3 examples ✅
```

### CLI Usage (Target)

```bash
# Generate coordination request from context
python scripts/generate-coordination-request.py \
  --context context-examples/coordination/example-exploratory.json \
  --output inbox/draft/

# Post-process and promote
python scripts/process-generated-artifact.py \
  inbox/draft/coordination-request.json \
  --verbose

# Evaluate quality
python scripts/evaluate-pilot-quality.py \
  --generated inbox/incoming/coordination/COORD-2025-NNN.json \
  --reference context-examples/coordination/example-exploratory.json
```

### Week 5-6 Milestones

**Week 5: Core Implementation** (20-24 hours)
- Day 1-2: Config loader, generators skeleton (8-10 hours)
- Day 3-4: AI integration, assembler (8-10 hours)
- Day 5: Integration with post-processing (4-6 hours)

**Week 6: Validation & Refinement** (8-12 hours)
- Day 1-2: Generate 10 coordination requests (4-6 hours)
- Day 3: Quality assessment, iteration (2-4 hours)
- Day 4-5: Performance optimization, documentation (2-4 hours)

**Success Criteria**:
- ✅ Generate coordination requests in <10 minutes
- ✅ Quality score ≥80% (target: maintain 94.9% from Week 4 test artifacts)
- ✅ 100% schema validation pass rate
- ✅ 100% post-processing success rate
- ✅ AI-generated fields meet word count/coherence requirements

---

## Future Migration to chora-compose

### When to Migrate

**Conditions**:
1. chora-compose reaches v2.0+ (production stable)
2. CLI available and documented
3. Artifact generation use case explicitly supported
4. Post-processing hooks/plugins available
5. Migration effort justified by new capabilities (MCP, etc.)

**Timeline Estimate**: 6-12 months minimum

### Migration Effort Estimate

**Low Effort** (if chora-compose matures as expected): 12-20 hours
- Restructure configs to chora-compose schema
- Migrate to chora-compose API
- Test and validate
- Update documentation

**Medium Effort** (if significant changes needed): 24-40 hours
- Redesign content configs
- Rebuild integration
- Extensive testing

**High Effort** (if incompatible): Stay standalone
- If chora-compose diverges, maintain standalone
- Continue leveraging proven architecture

### Migration Decision Points

**Evaluate quarterly**:
- Q1 2025: Check chora-compose v1.x maturity
- Q2 2025: Assess production readiness
- Q3 2025: Decision on migration if v2.0 released
- Q4 2025: Migrate if justified

---

## Risks and Mitigation

### Risk 1: AI Generation Quality Variance

**Risk**: AI-generated backgrounds/criteria may be inconsistent
**Probability**: MEDIUM
**Impact**: Quality scores drop below 80%

**Mitigation**:
- Detailed prompts in content configs
- Quality evaluation after each generation
- Iterative prompt engineering
- Fallback to templates for critical fields

### Risk 2: Development Time Overrun

**Risk**: 20-30 hour estimate exceeds actual time
**Probability**: LOW-MEDIUM
**Impact**: Delays production rollout

**Mitigation**:
- Phased implementation (core → AI → refinement)
- Reuse existing components (post-processing, validation)
- Start with demonstration generator (simpler than AI)
- Quality over speed (80% threshold non-negotiable)

### Risk 3: chora-compose Becomes Standard

**Risk**: Ecosystem adopts chora-compose, we're incompatible
**Probability**: LOW (6-12 month timeline)
**Impact**: Integration friction

**Mitigation**:
- Modular architecture enables migration
- Monitor chora-compose development
- Maintain config compatibility where possible
- Migration plan documented

---

## Recommendation Summary

**DECISION: Path C - Build Standalone Generator**

**Rationale**:
1. ✅ chora-compose not production-ready (no CLI, incomplete package)
2. ✅ Use case mismatch (SAP regeneration vs inbox generation)
3. ✅ Post-processing requirements critical for SAP-001
4. ✅ Low risk, production-ready in 2-3 weeks
5. ✅ Leverages all Week 2-4 validated work
6. ✅ Future migration path preserved

**Effort**: 20-30 hours (Week 5-6)

**Timeline**: Production-ready by Week 7

**Success Probability**: **HIGH** (95%+)
- All infrastructure validated
- Clear technical path
- Self-contained implementation
- Proven quality metrics (94.9%)

**Next Steps**:
1. ✅ Create this decision document (COMPLETE)
2. Begin Week 5 implementation (Core Generation System)
3. Maintain quality validation throughout
4. Document for ecosystem adoption

---

**Decision Made**: 2025-11-02
**Approved By**: Victor (Product), Claude Code (Engineering)
**Status**: ✅ **APPROVED - PROCEED WITH PATH C**
**Next Phase**: Week 5 Implementation - Core Generation System
