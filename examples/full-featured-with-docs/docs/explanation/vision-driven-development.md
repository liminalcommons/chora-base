# Explanation: Vision-Driven Development

**Audience:** Human developers seeking conceptual understanding
**Type:** Narrative, philosophical
**Related:** [Maintain Vision Documents](../how-to/06-maintain-vision-documents.md), [Memory System Architecture](memory-system-architecture.md)

---

## The Problem: Premature Optimization in Agentic Development

Traditional software development faces a challenge: **how to balance delivering immediate value with keeping future doors open**. This challenge becomes acute in agentic development, where AI coding agents lack the long-term context that human developers carry implicitly.

### The Gold-Plating Trap

**Scenario:** You're building an MCP server. The current need (Wave 1) is simple: 3 basic tools that return data.

**Without vision guidance:**

```python
# AI agent sees "future" might need tool chaining
# Implements full plugin architecture NOW

class ToolOrchestrator:
    def __init__(self):
        self.plugin_manager = PluginManager()  # NOT NEEDED YET
        self.tool_chain_executor = ChainExecutor()  # NOT NEEDED YET
        self.cache_layer = RedisCacheLayer()  # NOT NEEDED YET

    async def execute_tool(self, name: str, params: dict) -> dict:
        # 200 lines of abstraction for a problem that doesn't exist yet
        ...
```

**Result:** Delivered late, over-complex, hard to maintain, solving future problems that may never materialize.

### The Painted-Into-Corner Trap

**Scenario:** Same MCP server, but the opposite problem.

**Without vision guidance:**

```python
# AI agent optimizes for immediate need only
# Returns plain strings (easy today)

async def get_user(user_id: str) -> str:
    return f"User: {user_id}, Email: user@example.com"
```

**Problem:** When Wave 2 needs tool chaining (6 months later), **string responses break everything**. Must refactor all tools, break existing users, write migration guides.

**Result:** Technical debt, breaking changes, user frustration.

### What's Missing: Strategic Context

AI agents need to know:

1. **Current priority:** What's Wave 1? (Deliver this now)
2. **Future direction:** What's Wave 2? (Don't build it, but don't block it)
3. **Decision framework:** When to refactor vs. defer?

**Vision-driven development provides this context.**

---

## What is Vision-Driven Development?

**Definition:** A development methodology that uses **exploratory vision documents** to guide strategic architectural decisions while maintaining agile delivery of committed features.

### Core Principles

1. **Separate Exploratory from Committed**
   - **Vision docs (dev-docs/vision/):** "We might do this, if criteria met"
   - **Roadmap (ROADMAP.md):** "We will do this, by this date"

2. **Build for Today, Design for Tomorrow**
   - Deliver Wave 1 features now
   - Design extension points that keep Wave 2 possible
   - Don't implement Wave 2 until it's committed

3. **Decision Frameworks Over Guesswork**
   - Explicit go/no-go criteria for each wave
   - Refactoring decision flowchart
   - Cost-benefit analysis templates

4. **Stateful Memory for Agents**
   - Agents record decisions in knowledge notes
   - Future agents learn from past decisions
   - Cross-session consistency

### Vision vs. Roadmap

| Aspect | Vision (Exploratory) | Roadmap (Committed) |
|--------|---------------------|---------------------|
| **Nature** | Aspirational, fluid | Concrete, stable |
| **Certainty** | "Might do if..." | "Will do by..." |
| **Timeline** | Waves (post-milestone) | Versions/dates |
| **Audience** | Internal (team + agents) | Public (users) |
| **Changes** | Updated quarterly | Changes = scope change |
| **Purpose** | Guide design decisions | Track delivery progress |

**Example:**

**Vision doc (dev-docs/vision/):**
```markdown
Wave 2: Integration (Exploratory)

If we get 50+ users requesting GitHub integration AND
GitHub API v4 stabilizes AND we have 3 months capacity,
THEN we'll consider building GitHub tool integration.

Decision review: Q1 2026
```

**Roadmap (ROADMAP.md):**
```markdown
v1.5.0 (Q1 2026) - COMMITTED

Features:
- GitHub integration (3 tools: issues, PRs, repos)
- OAuth flow
- Rate limiting

Delivery: January 31, 2026
```

**Difference:** Vision explores possibilities, roadmap commits to delivery.

---

## Relationship to Agile/Iterative Development

**Question:** Isn't vision-driven development contradictory to agile's "respond to change over following a plan"?

**Answer:** No - vision complements agile by providing **strategic guard rails** while maintaining iterative delivery.

### How Vision Enhances Agile

**Traditional Agile (Without Vision):**

```
Sprint 1: Build feature A
Sprint 2: Build feature B
Sprint 3: Refactor A (didn't account for B)
Sprint 4: Refactor B (didn't account for C)
Sprint 5: Major rewrite (architecture debt too high)
```

**Agile + Vision:**

```
Sprint 1: Build feature A (with extension point for future B)
Sprint 2: Build feature B (uses A's extension point, no refactor)
Sprint 3: Build feature C (uses A+B patterns, consistent)
Sprint 4: Deliver early, architecture scales
Sprint 5: Start Wave 2 (foundations solid)
```

### YAGNI Still Applies

**YAGNI (You Aren't Gonna Need It):** Don't build features you don't need yet.

**Vision-driven development agrees:**

❌ **DON'T:** Build Wave 2 features in Wave 1
✅ **DO:** Design Wave 1 with extension points that don't block Wave 2

**Example:**

```python
# ❌ WRONG: Building Wave 2 feature now (violates YAGNI)
class Tool:
    def execute(self, params: dict, chain_context: ChainContext) -> dict:
        # chain_context not needed in Wave 1!
        ...

# ✅ RIGHT: Extension point (doesn't violate YAGNI)
class Tool:
    def execute(self, params: dict) -> dict:
        # Returns dict (not str) - extensible for Wave 2 chaining
        # Dict is Wave 1 requirement too (structured data)
        return {"result": data, "metadata": {...}}
```

**Key insight:** Extension points that serve both present AND future don't violate YAGNI.

### Wave-Based Planning vs. Sprint Planning

**Sprints (2-4 weeks):** Tactical delivery
**Waves (6-18 months):** Strategic capability themes

```
Wave 1: Foundation
  ├─ Sprint 1: Core tools
  ├─ Sprint 2: Error handling
  ├─ Sprint 3: Testing
  └─ Sprint 4: Documentation
  → Delivers v1.0

Wave 2: Integration (exploratory until Wave 1 done)
  ├─ Validate: User demand?
  ├─ Validate: APIs available?
  └─ Decision: Commit or defer?
  → If committed: Plan sprints for v1.5
```

**Relationship:** Waves provide strategic themes → Sprints deliver tactical increments

---

## Decision Frameworks in Practice

### The Refactoring Decision Framework

**When faced with a refactoring opportunity, apply this framework:**

```
┌─────────────────────────────────────────────────────┐
│ 1. Does this help current work (Wave 1)?           │
│    NO → DEFER (focus on current deliverables)      │
│    YES → Continue ↓                                 │
├─────────────────────────────────────────────────────┤
│ 2. Does this unblock future capabilities?          │
│    YES → LIKELY REFACTOR (strategic investment)    │
│    NO → Continue ↓                                  │
├─────────────────────────────────────────────────────┤
│ 3. Cost vs. benefit?                                │
│    HIGH COST → DEFER (wait for Wave 2 commitment)  │
│    LOW COST → REFACTOR (small prep, big payoff)    │
└─────────────────────────────────────────────────────┘
```

### Real Examples from chora-compose

**Example 1: Content Type Detection (Deferred → Wave 2)**

**Situation:** Wave 1 needed simple markdown processing. Vision included intelligent content type detection for Wave 2.

**Decision:**
- Helps current work? **YES** (markdown is a content type)
- Unblocks future? **YES** (Wave 2 needs multi-type support)
- Cost? **HIGH** (2 weeks to implement ML-based detection)

**Outcome:** **DEFER** - Used simple file extension check in Wave 1. Saved 2 weeks. Wave 2 implemented full detection when it mattered.

**Example 2: Structured Output (Refactored in Wave 1)**

**Situation:** Wave 1 tools returned strings. Vision showed Wave 2 needs tool chaining (requires structured data).

**Decision:**
- Helps current work? **YES** (structured data useful now for error handling)
- Unblocks future? **YES** (Wave 2 tool chaining needs dict responses)
- Cost? **LOW** (2 hours to change `str` → `dict` returns)

**Outcome:** **REFACTOR** - Changed all tool returns to dict. Wave 2 tool chaining worked seamlessly.

**Example 3: Multi-Modal Support (Wave 3 Vision)**

**Situation:** Wave 1 text-only. Wave 3 vision included image/video processing.

**Decision:**
- Helps current work? **NO** (Wave 1 is text-only)
- Unblocks future? **MAYBE** (Wave 3 uncertain, might use different approach)
- Cost? **HIGH** (1 month to add multi-modal pipeline)

**Outcome:** **DEFER** - Stayed text-only in Wave 1. Wave 3 eventually used a different library (initial approach would have been wasted effort).

### Cost-Benefit Analysis Template

| Factor | Low Cost (<2 hours) | Medium Cost (2-8 hours) | High Cost (>1 day) |
|--------|---------------------|-------------------------|-------------------|
| **Serves Wave 1** | ✅ REFACTOR | ✅ REFACTOR (if critical) | ⚠️ Evaluate carefully |
| **Serves Wave 2** | ✅ REFACTOR | ⚠️ Defer unless low risk | ❌ DEFER (wait for commit) |
| **Serves Wave 3+** | ⚠️ Evaluate | ❌ DEFER | ❌ DEFER |

**Rule of thumb:** If it takes longer than the current sprint, defer it.

---

## Benefits for AI Agents

### 1. Stateful Memory (A-MEM Integration)

AI agents are stateless by default. Vision + memory system = stateful learning.

**Pattern:**

```python
# Agent reads vision
vision = read_file("dev-docs/vision/CAPABILITY_EVOLUTION.md")
wave_2 = parse_wave(vision, wave_num=2)

# Agent makes decision
if current_task.helps_wave_1 and current_task.unblocks_wave_2:
    decision = "REFACTOR"
else:
    decision = "DEFER"

# Agent records decision for future sessions
emit_event(
    event_type="architecture.decision",
    data={
        "decision": decision,
        "rationale": "Serves Wave 1 AND prepares Wave 2",
        "wave": "wave-2-preparation"
    }
)

create_knowledge_note(
    title="Tool Response Format Decision",
    content=f"Decided to {decision} because...",
    tags=["architecture", "vision", "wave-2"]
)
```

**Outcome:** Next session, agent queries past decisions:

```bash
your-project-memory knowledge search --tag wave-2 --tag architecture
# Finds: "Tool Response Format Decision"
# Learns: "We use dict responses to prepare for Wave 2 chaining"
# Applies: New tools also use dict (consistent with decision)
```

### 2. Cross-Session Consistency

**Without vision:**

Session 1 (Agent A): Implements tool X returning `dict`
Session 2 (Agent B): Implements tool Y returning `str` (inconsistent)
Session 3 (Agent C): Confused by mixed returns, asks human

**With vision:**

Session 1 (Agent A): Reads vision → Returns `dict` → Records decision
Session 2 (Agent B): Queries past decisions → Sees "use dict" → Returns `dict`
Session 3 (Agent C): Queries knowledge → Sees pattern → Returns `dict`

**Result:** Self-consistent architecture without human intervention.

### 3. Reduced Uncertainty in Design Decisions

**Scenario:** Agent encounters design fork:

```python
# Option A: Simple (str return)
async def get_user(user_id: str) -> str:
    return f"User: {user_id}"

# Option B: Structured (dict return)
async def get_user(user_id: str) -> dict:
    return {"user_id": user_id, "metadata": {...}}
```

**Without vision:** Agent guesses, or asks human (context switch, slow)

**With vision:**
1. Agent reads vision: "Wave 2 includes tool chaining (needs structured data)"
2. Agent applies framework: "Option B serves both Wave 1 and Wave 2"
3. Agent implements Option B, records decision
4. Human reviews PR, sees rationale linked to vision, approves quickly

**Outcome:** Faster development, fewer context switches, strategic alignment.

---

## Benefits for Teams

### 1. Alignment on Long-Term Direction

**Before vision docs:**

Developer A: "Let's add plugin system now!"
Developer B: "No, YAGNI - we don't need it"
Developer A: "But users will want it eventually"
Developer B: "Maybe, maybe not"
→ Stalemate, no decision

**After vision docs:**

Developer A: "Let's add plugin system now!"
Developer B: "Check vision: It's Wave 4, decision criteria not met (only 10 users, need 500+)"
Developer A: "Oh, you're right. Let's focus on Wave 1"
→ Objective decision based on documented criteria

### 2. Reduced Bike-Shedding

**Bike-shedding:** Arguing about minor decisions endlessly.

**Vision provides objective anchor:**

Question: "Should we use Strategy pattern or Plugin pattern?"

Answer: "Check vision - Wave 2 needs plugins. Use Plugin pattern if low cost, otherwise defer to Wave 2."

### 3. Onboarding New Developers/Agents

**New developer joins:**

1. Reads ROADMAP.md → Knows what's committed
2. Reads dev-docs/vision/ → Knows long-term direction
3. Reads AGENTS.md Strategic Design → Knows decision frameworks
4. Starts coding with full context

**Time to productivity:** Days instead of weeks.

### 4. Historical Record of Decisions

**6 months later:**

"Why did we use dict responses instead of str?"

**Without vision:** Search git history, read PRs, ask original developers (who may have left)

**With vision:** Read archived Wave 1 in vision/archive/ → See decision rationale → Understand immediately

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Using Vision to Justify Scope Creep

**Symptom:** "But it's in the vision!" used to add features to current sprint

**Example:**
- Sprint goal: Deliver 3 basic tools (Wave 1)
- Developer: "Let's also add tool chaining (Wave 2) since it's in the vision"
- Result: Sprint late, Wave 1 delayed, users waiting

**Mitigation:**
- Vision is **exploratory**, not **committed**
- Roadmap wins: If not in ROADMAP.md, not in current sprint
- Apply decision criteria: "Are ALL criteria met for Wave 2?" (Usually no)

### Pitfall 2: Vision Becomes 5-Year Roadmap

**Symptom:** Vision has 10 waves with detailed feature lists and specific dates

**Example:**
```markdown
Wave 8 (2030): Add quantum computing support
- Use IBM Quantum API
- Implement Shor's algorithm for X
- Deliver by Q2 2030
```

**Problem:** Too specific, will change, becomes stale immediately

**Mitigation:**
- Keep waves 1-4 (max 6)
- Keep waves thematic, not feature-lists
- No dates in vision (dates go in roadmap when committed)
- Archive distant waves if they're too speculative

### Pitfall 3: Never Reviewing/Updating Vision

**Symptom:** Vision doc last updated 18 months ago, completely out of sync

**Example:**
- Vision says "Wave 2: Add WebSocket support"
- Reality: Market shifted to WebRTC, WebSockets obsolete
- Developers still designing for WebSockets (following stale vision)

**Mitigation:**
- **Schedule quarterly reviews** (calendar recurring event)
- Assign owner for vision maintenance
- Make reviews lightweight (30-60 min, not full-day planning)
- Archive outdated waves, add new ones based on learnings

### Pitfall 4: Building Wave 2 Features in Wave 1

**Symptom:** "Preparing for future" becomes "building future features now"

**Example:**
```python
# Wave 1 needs simple processing
# Vision shows Wave 2 needs advanced analytics

# ❌ WRONG: Building Wave 2 analytics engine in Wave 1
class Processor:
    def __init__(self):
        self.analytics_engine = AdvancedAnalyticsEngine()  # NOT NEEDED
        self.ml_model = load_model("analytics-v2")  # NOT NEEDED
```

**Mitigation:**
- Use decision framework: "Does this help Wave 1?"
  - If NO → DEFER (even if it helps Wave 2)
  - If YES AND helps Wave 2 → Refactor (serves both)
- Code reviews check: "Is this Wave 1 requirement or Wave 2 gold-plating?"
- AGENTS.md examples show difference (extension points vs features)

---

## Summary: Vision-Driven Development in Practice

**Vision-driven development is:**

✅ **A strategic framework** for balancing present and future
✅ **A decision tool** for when to refactor vs. defer
✅ **A communication mechanism** between humans and AI agents
✅ **A memory system** for cross-session learning

**Vision-driven development is NOT:**

❌ **A 5-year roadmap** with committed features
❌ **An excuse for scope creep** ("it's in the vision!")
❌ **A replacement for agile** (complements, doesn't replace)
❌ **A way to avoid YAGNI** (YAGNI still applies)

**In one sentence:**

> **Vision-driven development uses exploratory capability waves to guide strategic architectural decisions, enabling teams and AI agents to deliver current commitments while keeping future doors open, without building features before they're needed.**

---

## Further Reading

- **Research:** Agentic Coding Best Practices Research (Section 2.2: Systems Thinking, Section 4.3: A-MEM)
- **How-To:** [Maintain Vision Documents](../how-to/06-maintain-vision-documents.md)
- **Template:** [dev-docs/vision/README.md](../../template/dev-docs/vision/README.md.jinja)
- **Example:** chora-compose content intelligence evolution (real-world case study)

---

**Last Updated:** 2025-10-19
**Version:** chora-base v1.3.1
**Status:** Complete

🧭 Build for today, design for tomorrow. Vision guides the way.
