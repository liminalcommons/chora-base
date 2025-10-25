# Capability Evolution - mcp-orchestration

This document describes the potential evolutionary path for mcp-orchestration across multiple capability waves. These are **exploratory directions**, not committed features.

**Purpose:** Guide strategic design decisions today while keeping future doors open.

---

## Overview: Capability Waves

```
Wave 1: Foundation          Wave 2: Integration       Wave 3: Intelligence      Wave 4: Ecosystem
   (v0.1.0-v0.1.6)         (Post-Wave 1.6, Exploratory)  (Post-Wave 2, Exploratory)  (Post-Wave 3, Exploratory)
   ├─ 1.0 ✅ Foundation     ├─ External systems      ├─ AI/ML features        ├─ Platform features
   ├─ 1.1 ✅ Registry       ├─ API integrations      ├─ Smart automation      ├─ Plugin system
   ├─ 1.2 📋 Transport      ├─ Data sync             ├─ Learning systems      ├─ Third-party tools
   ├─ 1.3 📋 Validation     ├─ Workflow support      ├─ Insights & analytics  └─ Community extensions
   ├─ 1.4 📋 Publishing
   ├─ 1.5 📋 E2E Workflow
   └─ 1.6 📋 Audit/History
```

**Current Status:** Wave 1 in progress - Wave 1.0 ✅ RELEASED, Wave 1.1 ✅ COMPLETED (unreleased), Waves 1.2-1.6 📋 PLANNED

**Decision Cadence:** Review after each Wave 1 sub-wave; major review after Wave 1.6 completion

---

## Wave 1: Foundation (v0.1.0 - v0.1.6)

### Status

**Current:** Wave 1.0 ✅ COMPLETED (v0.1.0), Wave 1.1 ✅ COMPLETED (v0.1.1 unreleased), Waves 1.2-1.6 PLANNED
**Target:** Complete Wave 1 series through v0.1.6
**Timeline:** Wave 1.0 released 2025-10-17, Wave 1.1 completed 2025-10-24

### Capability Theme

Wave 1 delivers core MCP configuration orchestration through **6 incremental sub-waves**, each adding standalone value:

**Wave 1.0 (v0.1.0)** ✅ COMPLETED - Foundation
- MCP Server Infrastructure - stdio-based MCP server
- 4 Core Tools - `list_clients`, `list_profiles`, `get_config`, `diff_config`
- 2 Resources - `capabilities://server`, `capabilities://clients`
- Content-addressable artifact storage with Ed25519 signing
- Client registry (Claude Desktop, Cursor)

**Wave 1.1 (v0.1.1)** ✅ COMPLETED - Server Registry
- Server catalog with 15 known MCP servers
- 2 Tools - `list_available_servers`, `describe_server`
- 2 Resources - `server://registry`, `server://{id}`
- CLI commands for browsing servers

**Waves 1.2-1.6** 📋 PLANNED (see [project-docs/WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md))
- Wave 1.2: Transport abstraction + config generation
- Wave 1.3: Schema validation
- Wave 1.4: Publishing workflow
- Wave 1.5: E2E config management
- Wave 1.6: Audit & history
### Motivation

Why Wave 1 matters:

1. **User Need:** Solve the core problem that mcp-orchestration addresses
2. **Market Signal:** Validate product-market fit before expanding
3. **Technical Foundation:** Establish architecture patterns for future waves
4. **Learning Opportunity:** Gather user feedback to inform Wave 2+

### Technical Sketch

**Architecture Principles:**
- Keep it simple (YAGNI - don't build Wave 2 features yet)
- Extensible design (prepare for Wave 2 without implementing it)
- Clear abstractions (easy to add capabilities later)

**Example: Tool Interface Design**
```python
# Wave 1: Simple function-based tools
async def tool_get_info(query: str) -> dict:
    """Get basic information."""
    return {"result": process_query(query)}

# Extension point for Wave 2 (tool chaining)
# Design: Return structured dict (not plain str) to enable future composition
```
### Success Metrics

How we'll know Wave 1 succeeded:

| Metric | Target | Measurement | Status |
|--------|--------|-------------|--------|
| **Adoption** | 10+ users install and use | GitHub stars, download count | 🔄 In progress |
| **Core Tools Usage** | 80%+ tools used weekly | Event log queries | 🔄 Collecting data |
| **Error Rate** | <5% tool call failures | Error tracking | ✅ Achieved (70%+ test coverage) |
| **Setup Time** | <5 minutes first use | User feedback | ✅ Achieved (init-configs command) |

### Decision: Committed & Partially Delivered

**Status:** ✅ Wave 1.0 & 1.1 delivered, Waves 1.2-1.6 committed
**Rationale:** Core functionality required for product to exist; incremental delivery reduces risk
**Timeline:**
- Wave 1.0 (v0.1.0): ✅ Released 2025-10-17
- Wave 1.1 (v0.1.1): ✅ Completed 2025-10-24 (pending tag/release)
- Waves 1.2-1.6: 📋 Estimated 17-25 days total (see [WAVE_1X_PLAN.md](../../project-docs/WAVE_1X_PLAN.md))

---

## Wave 2: Integration (Post-Wave 1.6, Exploratory)

### Status

**Current:** Exploratory (Not Committed)
**Target:** TBD (likely v0.2.0 or v1.0.0, after Wave 1.6 completes and stabilizes)
**Review Date:** Quarterly review after v0.1.6 ships and user feedback collected

### Capability Theme

Integrate with external systems and workflows:

- **Tool Chaining** - Compose multiple tools in sequences
- **External APIs** - Connect to third-party services (e.g., databases, APIs)
- **Data Persistence** - Cache results, maintain session state
- **Advanced Configuration** - Per-tool config, environment profiles
- **Workflow Integration** - Hooks for automation platforms
### Motivation

Why Wave 2 might matter:

1. **User Signal:** Users request integrations with their existing tools
2. **Market Trend:** Ecosystem integrations drive adoption (network effects)
3. **Competitive:** Standalone tools have less moat than integrated platforms
4. **Technical:** Wave 1 architecture can support integrations with refactoring

### Technical Sketch

**Tool Chaining Example:**
```python
# Wave 2: Tool composition
class ToolChain:
    def __init__(self, tools: List[Tool]):
        self.tools = tools

    async def execute(self, input: dict) -> dict:
        """Execute tools in sequence, passing outputs as inputs."""
        result = input
        for tool in self.tools:
            result = await tool.execute(result)
        return result

# Enables: tool_A → tool_B → tool_C workflows
```

**Data Persistence:**
```python
# Wave 2: Cache layer
class CachedTool(Tool):
    def __init__(self, tool: Tool, cache: Cache):
        self.tool = tool
        self.cache = cache

    async def execute(self, params: dict) -> dict:
        cache_key = hash_params(params)
        if cached := self.cache.get(cache_key):
            return cached

        result = await self.tool.execute(params)
        self.cache.set(cache_key, result, ttl=3600)
        return result
```
### Decision Criteria

Explicit go/no-go criteria for Wave 2:

| Criterion | Target | Current | Status |
|-----------|--------|---------|--------|
| **Wave 1 Complete** | v0.1.6 shipped, <5 critical bugs | v0.1.1 completed | 🔄 In progress (4 waves remaining) |
| **User Demand** | 50+ users requesting integrations | TBD | ⏳ Track after Wave 1.6 |
| **API Availability** | Partner APIs documented, accessible | TBD | ⏳ Survey ecosystem |
| **Team Capacity** | 3+ months eng time available | TBD | ⏳ Budget planning |

**Decision Framework:**
```
IF all criteria met:
  → COMMIT to roadmap (move to ROADMAP.md)
ELSE IF 2-3 criteria met:
  → VALIDATE (run spike/prototype)
ELSE:
  → DEFER (keep exploratory, review quarterly)
```

### Success Metrics (If Committed)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Integrations Used** | 3+ external APIs connected | Usage telemetry |
| **Tool Chains Created** | 20+ users chain tools | Event log analysis |
| **Cache Hit Rate** | >60% for repeated queries | Cache metrics |
### Dependencies

What must be true before Wave 2:

1. **Wave 1.6 Delivered:** All Wave 1 sub-waves (1.0-1.6) completed, stable, and adopted
2. **Architecture Review:** Confirm Wave 1 architecture supports extensions
3. **User Research:** Validate which integrations matter most (collect feedback during Wave 1.x)
4. **Partner APIs:** External APIs available and documented (if applicable)

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Complexity Explosion** | High | Limit to 3-5 integrations in Wave 2.0, expand in 2.1/2.2 |
| **Maintenance Burden** | Medium | Partner APIs change → Use adapter pattern, version pins |
| **User Adoption** | Low | If Wave 1 successful, users will want integrations |

---

## Wave 3: Intelligence (Post-Wave 2, Exploratory)

### Status

**Current:** Exploratory (Not Committed)
**Target:** TBD (after Wave 2 evaluates and delivers)
**Review Date:** Quarterly review after Wave 2 ships

### Capability Theme

Add AI/ML-powered features for smart automation:

- **Smart Tool Selection** - Recommend tools based on user intent
- **Predictive Caching** - Pre-fetch likely next queries
- **Insight Generation** - Analyze usage patterns, suggest optimizations
- **Natural Language Queries** - Translate plain English to tool calls
- **Learning from Feedback** - Improve recommendations over time
### Motivation

Why Wave 3 might matter:

1. **User Need:** As adoption grows, users want automation (reduce manual work)
2. **Market Trend:** AI/ML features become table stakes in 2025+
3. **Competitive:** Smart features differentiate from basic tools
4. **Technical:** Wave 2 data (usage patterns) enables ML training

### Technical Sketch

**Smart Tool Selection Example:**
```python
# Wave 3: ML-powered tool routing
class SmartRouter:
    def __init__(self, model: ToolSelectionModel):
        self.model = model

    async def route(self, user_query: str) -> List[Tool]:
        """Use ML to predict best tool(s) for user intent."""
        # Embed query → Compare to tool embeddings → Rank by relevance
        embeddings = self.model.embed(user_query)
        tool_scores = self.model.score_tools(embeddings)
        return self.model.top_k_tools(tool_scores, k=3)

# Requires: Training data from Wave 1-2 usage logs
```
### Decision Criteria

| Criterion | Target | Current | Status |
|-----------|--------|---------|--------|
| **Wave 2 Delivered** | Wave 2 shipped, integrations adopted | TBD | ⏳ Pending Wave 2 commitment |
| **Training Data** | 10,000+ usage events collected | 🔄 Starting collection in Wave 1 | ⏳ Need Wave 1-2 data |
| **User Demand** | 100+ users requesting AI features | TBD | ⏳ Track feedback |
| **ML Expertise** | Team has ML eng or partner available | TBD | ⏳ Hiring/partnering |
| **Compute Budget** | GPU resources for training/inference | TBD | ⏳ Cost modeling |

### Dependencies

1. **Wave 2 Data:** Need usage patterns from integrations to train models
2. **ML Infrastructure:** Training pipeline, model serving, monitoring
3. **Privacy Review:** Ensure data collection complies with privacy policies
4. **User Trust:** Users must opt-in to data collection for training

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Model Accuracy** | High | Start with rule-based heuristics, add ML incrementally |
| **Compute Costs** | Medium | Use small models, edge inference, cache aggressively |
| **Privacy Concerns** | High | Strict opt-in, local models where possible, privacy audit |
| **Feature Complexity** | Medium | Ship MVPs (e.g., simple recommendations before full NLP) |

---

## Wave 4: Ecosystem (Post-Wave 3, Exploratory)

### Status

**Current:** Exploratory (Not Committed)
**Target:** TBD (after Wave 3 evaluates and delivers)
**Review Date:** Quarterly review after Wave 3 ships

### Capability Theme

Enable third-party developers to extend mcp-orchestration:

- **Tool Marketplace** - Registry of community-built tools
- **Tool SDK** - Simplified API for building custom tools
- **Sandboxed Execution** - Safe execution of third-party tool code
- **Monetization** - Revenue sharing for premium tools (optional)
- **Community Hub** - Forums, docs, tool showcases
### Motivation

Why Wave 4 might matter:

1. **Network Effects:** Community extensions accelerate feature growth
2. **Market Expansion:** Partners reach use cases core team can't address
3. **Competitive Moat:** Ecosystem lock-in (users invested in extensions)
4. **Sustainability:** Community contributions reduce core team burden

### Technical Sketch

**Tool Marketplace Architecture:**
```
┌─────────────────────────────────────┐
│      Tool Marketplace Registry      │
│  (GitHub repo or package registry)  │
└─────────────┬───────────────────────┘
              │
              ├─ Community Tool 1 (pypi package)
              ├─ Community Tool 2 (pypi package)
              └─ Community Tool 3 (pypi package)
                      ↓
┌─────────────────────────────────────┐
│    mcp-orchestration Server         │
│  - Tool discovery (search registry)  │
│  - Tool installation (pip install)   │
│  - Sandboxed execution (containers)  │
└─────────────────────────────────────┘
```

**Tool SDK Example:**
```python
# Wave 4: Simplified tool creation
from mcp_orchestration.sdk import Tool, register

@register
class MyCustomTool(Tool):
    name = "my_custom_tool"
    description = "Does something useful"

    async def execute(self, params: dict) -> dict:
        # Community developer writes this
        return {"result": "custom logic here"}

# Published as PyPI package: mcp-orchestration-tool-mycustom
# Installed: pip install mcp-orchestration-tool-mycustom
# Discovered: Automatically loaded by mcp-orchestration
```
### Decision Criteria

| Criterion | Target | Current | Status |
|-----------|--------|---------|--------|
| **Wave 3 Delivered** | Wave 3 shipped, AI features adopted | TBD | ⏳ Pending Wave 3 commitment |
| **Community Size** | 500+ active users | <10 (early adopters) | ⏳ Growing user base |
| **Extension Demand** | 50+ requests for custom tools/plugins | TBD | ⏳ Track GitHub issues |
| **Platform Maturity** | Stable APIs, <1 breaking change/year | TBD | ⏳ API stability focus (Wave 1 in progress) |
| **Resources** | 6+ months eng time, community manager | TBD | ⏳ Budget planning |

### Dependencies

1. **Stable APIs:** No breaking changes for 12 months (ecosystem needs stability)
2. **Security Infrastructure:** Code review, scanning, sandboxing for third-party code
3. **Legal Review:** Terms for marketplace, liability, content moderation
4. **Community Management:** Dedicated community manager or team

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Security Vulnerabilities** | Critical | Mandatory security scans, sandboxed execution, code review |
| **Low-Quality Extensions** | Medium | Rating system, featured/verified badges, moderation |
| **API Breakage** | High | API versioning, deprecation policy (12-month notice) |
| **Support Burden** | Medium | Clear boundaries (core vs community support) |

---

## Cross-Wave Principles

### Design for Future Waves

**When building Wave N, consider Wave N+1:**

1. **Extensibility:** Use interfaces/protocols, not concrete implementations
2. **Data Collection:** Emit events for future ML training (with privacy controls)
3. **API Stability:** Minimize breaking changes (easier to add than change)
4. **Documentation:** Explain architecture decisions for future maintainers

### Refactoring Decision Framework

**Should I refactor now, or defer?**

```
┌─────────────────────────────────────────────────────┐
│ 1. Does this help current wave (Wave 1)?           │
│    NO → DEFER (focus on current work)              │
│    YES → Continue ↓                                 │
├─────────────────────────────────────────────────────┤
│ 2. Does this block future waves (Wave 2-4)?        │
│    YES → REFACTOR (strategic investment)           │
│    NO → Continue ↓                                  │
├─────────────────────────────────────────────────────┤
│ 3. Cost vs. benefit?                                │
│    HIGH COST → DEFER (wait until Wave 2 committed) │
│    LOW COST → REFACTOR (small prep pays off)       │
└─────────────────────────────────────────────────────┘
```

**Example Decisions:**

| Scenario | Decision | Rationale |
|----------|----------|-----------|
| Return `dict` instead of `str` in tool responses | ✅ REFACTOR | Low cost, unblocks Wave 2 (tool chaining) |
| Build full plugin system in Wave 1 | ❌ DEFER | High cost, Wave 2 not committed yet |
| Add structured logging with trace IDs | ✅ REFACTOR | Low cost, enables Wave 3 (ML training data) |
| Implement ML model serving infra | ❌ DEFER | High cost, Wave 3 not validated yet |

---

## Review History

### 2025-10-24 (Wave 1 Progress Update)

**Status Update:**
- Wave 1.0 (v0.1.0): ✅ DELIVERED (2025-10-17)
- Wave 1.1 (v0.1.1): ✅ COMPLETED (pending tag/release)
- Waves 1.2-1.6: 📋 PLANNED (17-25 days estimated)

**Key Changes:**
- Updated document to reflect Wave 1 sub-wave structure (6 incremental releases)
- Adjusted Wave 2-4 dependencies to reference Wave 1.6 completion
- Added current status for metrics and criteria
- Clarified version numbering (v0.1.x for Wave 1 series)

**Next Review:** After Wave 1.6 ships (target: TBD, ~3-4 weeks from 2025-10-24)

### 2025-10-19 (Initial Vision)

**Decisions:**
- Wave 1 (Foundation): COMMITTED to roadmap
- Wave 2 (Integration): EXPLORATORY (review after Wave 1 complete)
- Wave 3 (Intelligence): EXPLORATORY (depends on Wave 2 data)
- Wave 4 (Ecosystem): EXPLORATORY (long-term vision, 2+ years out)

**Initial Targets:**
- Wave 1.0 (v0.1.0): Foundation release
- Subsequent waves: To be evaluated after Wave 1 stabilizes

---

## How to Use This Document

### For Maintainers

**During implementation:**
1. Check current wave (Wave 1) for context
2. Apply refactoring decision framework before architectural changes
3. Document decisions in ADRs or knowledge notes

**During quarterly reviews:**
1. Update decision criteria status
2. Move delivered waves to archive/
3. Add new waves based on learnings
4. Adjust timelines based on actual velocity

### For AI Coding Agents

**When implementing features:**
1. Read [AGENTS.md](../../AGENTS.md) Section 3: Strategic Design
2. Check this vision doc: "Does design block future waves?"
3. Apply refactoring framework
4. Document decision:
   ```bash
# Record decision in knowledge graph
   echo "Decision: Return dict instead of str in tool responses
   Rationale: Enables Wave 2 tool chaining without breaking changes
   Tags: architecture, vision, wave-2
   " | mcp_orchestration-memory knowledge create "Tool Response Format Decision"
```

### For Contributors

**When proposing features:**
1. Check if feature aligns with current wave
2. If Wave 2+ feature, add to exploratory wave (don't build yet)
3. If Wave 1 feature, ensure it doesn't block future waves

---

## Related Documentation

- [README.md](README.md) - Vision directory guide
- [ROADMAP.md](../../ROADMAP.md) - Committed features and timelines
- [AGENTS.md](../../AGENTS.md) - Machine-readable agent instructions
- [CHANGELOG.md](../../CHANGELOG.md) - Delivered features
- [.chora/memory/](../../.chora/memory/) - Agent memory for decision tracking
---

**Last Updated:** 2025-10-24 (updated after Wave 1.1 completion)
**Template Version:** chora-base v1.3.0
**Status:** Living document (review after each wave milestone)
**Current Wave:** Wave 1 (sub-waves 1.0-1.6, currently at 1.1 ✅)

🧭 This vision guides strategic decisions across multiple years of evolution.
