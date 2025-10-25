# Vision Documents Usage Guide

**Purpose:** Guide for using vision documents to inform strategic design decisions.

**Parent:** See [../../AGENTS.md](../../AGENTS.md) for project overview and [../AGENTS.md](../AGENTS.md) for development workflows.

---

## Quick Reference

- **What are vision docs?** Exploratory capability planning (not committed features)
- **Key vision docs:**
  - [MCP_CONFIG_ORCHESTRATION.md](MCP_CONFIG_ORCHESTRATION.md) - Core product vision
  - [MCP_SERVER_SPEC.md](MCP_SERVER_SPEC.md) - MCP protocol specification
  - [CAPABILITY_EVOLUTION.example.md](CAPABILITY_EVOLUTION.example.md) - Wave planning template
- **Decision framework:** See [README.md](README.md) "Decision Framework" section
- **Review cadence:** Quarterly (Q1, Q2, Q3, Q4)

---

## Directory Structure

```
dev-docs/vision/
├── AGENTS.md                           # This file - vision documents usage guide
├── README.md                           # Vision documents overview
├── MCP_CONFIG_ORCHESTRATION.md         # Core product vision
├── MCP_SERVER_SPEC.md                  # MCP protocol specification
├── CAPABILITY_EVOLUTION.example.md     # Wave planning template
├── spec.md                             # Original spec draft
└── archive/                            # Archived/delivered waves [future]
```

---

## Vision vs. Roadmap

**CRITICAL DISTINCTION for AI agents:**

### Vision Documents (This Directory)

**Nature:** Exploratory, aspirational, fluid
**Status:** Possible future directions (not committed)
**Timeline:** Waves (post-milestone, no dates)
**Changes:** Fluid, revised quarterly
**Keywords:** "might", "could", "if", "exploratory", "potential"

**Example from vision:**
```markdown
Wave 3: Intelligence (Exploratory)
We might add AI-powered config validation if:
- User demand reaches 100+ requests
- AI models mature (95%+ accuracy)
- Team has 6+ months capacity
```

### Roadmap (../../ROADMAP.md)

**Nature:** Committed, time-bound, stable
**Status:** Committed deliverables
**Timeline:** Specific versions and dates
**Changes:** Changes = scope change (rare)
**Keywords:** "will", "planned", "committed", "target date"

**Example from roadmap:**
```markdown
Wave 1.1 (v0.2.0) - Target: 2025-11-15
Features:
- MCP server catalog
- Server discovery CLI
- Server metadata management
```

### Decision Rule for Agents

**When implementing features:**
- ✅ **Use roadmap** - Build what's committed in [../../ROADMAP.md](../../ROADMAP.md)
- ✅ **Use vision** - Inform architecture choices (keep future doors open)
- ❌ **Don't use vision** - Implement exploratory features (not committed)

**Example:**
- ❌ **Wrong:** "Vision mentions Wave 3 AI validation, I'll implement it now"
- ✅ **Right:** "Vision mentions Wave 3 AI validation, I'll structure validation layer to support future AI integration"

---

## Using Vision Documents Strategically

### Use Case 1: Architecture Decisions

**Scenario:** Designing a new module, choosing between two approaches.

**Process:**

1. **Read current wave in vision:**
```bash
# Check what future capabilities are planned
cat dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md
```

2. **Identify future requirements:**
```markdown
Wave 2: Governance
- Policy engine for config validation
- Requires: Extensible validation layer
```

3. **Evaluate both options:**

**Option A (Simple):**
```python
def validate_config(config: dict) -> bool:
    # Hard-coded validation rules
    return config.get("version") == "1.0"
```

**Option B (Extensible for Wave 2):**
```python
def validate_config(config: dict, validators: list[Validator] = None) -> bool:
    # Plugin architecture (supports future policy engine)
    validators = validators or [default_validator()]
    return all(v.validate(config) for v in validators)
```

4. **Decision:**
- Choose **Option B** - Enables Wave 2 without breaking changes
- Document choice in ADR or knowledge note

5. **Emit decision event:**
```python
from mcp_orchestrator.memory import create_note

create_note(
    content="Chose extensible validation architecture to support Wave 2 policy engine",
    tags=["architecture", "wave-2", "validation", "future-proofing"],
    references=["dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md"]
)
```

### Use Case 2: Refactoring Decisions

**Scenario:** Existing code is messy, considering refactoring.

**Decision Framework:**

**Step 1: Check current wave**
```bash
# What wave are we in?
cat project-docs/WAVE_1X_PLAN.md
```

**Step 2: Check next wave requirements**
```bash
# Does next wave need this module refactored?
cat dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md
```

**Step 3: Apply refactoring matrix**

|                          | **Next Wave Needs It** | **Next Wave Doesn't Need It** |
|--------------------------|------------------------|-------------------------------|
| **Current Wave Blocked** | ✅ **Refactor Now**     | ✅ **Refactor Now**            |
| **Current Wave OK**      | ✅ **Refactor Now**     | ❌ **Defer** (YAGNI)           |

**Example:**
- **Situation:** Storage module is messy, Wave 1.1 needs it for server catalog
- **Decision:** ✅ Refactor now (next wave needs it + current wave blocked)

**Step 4: Document decision**
```python
emit_event("architecture.refactoring_decision", status="success",
           metadata={
               "module": "storage",
               "decision": "refactor_now",
               "rationale": "Wave 1.1 server catalog requires storage refactoring"
           })
```

### Use Case 3: Feature Requests

**Scenario:** User requests a feature via GitHub issue.

**Process:**

1. **Check if feature is in current wave:**
```bash
cat project-docs/WAVE_1X_PLAN.md | grep -i "feature name"
```

2. **If not, check vision documents:**
```bash
cat dev-docs/vision/*.md | grep -i "feature name"
```

3. **Categorize request:**

**Case A: In current wave**
- ✅ Implement (aligned with roadmap)

**Case B: In future wave (exploratory)**
- Label issue with wave tag (e.g., `wave-2`)
- Add comment: "This feature aligns with Wave 2 (Governance). We'll consider it after Wave 1 completes. See [vision doc](link)."
- Track demand (increment counter in vision doc)

**Case C: Not in any wave**
- Evaluate if it fits strategic direction
- If yes: Add to vision doc as new capability
- If no: Politely decline with explanation

4. **Update vision doc if needed:**
```markdown
## Wave 2: Governance

**User Demand Signals:**
- GitHub issue #42 (policy validation)
- GitHub issue #57 (role-based access)
- Slack request from 3 enterprise users
- Total demand: 15 users

**Decision:** Demand below threshold (need 50+ users). Re-evaluate in Q2.
```

### Use Case 4: PR Review with Vision Context

**Scenario:** Reviewing a PR that adds new functionality.

**Review Checklist:**

1. **Current wave alignment:**
```bash
# Does PR contribute to current wave?
cat project-docs/WAVE_1X_PLAN.md
```
- ✅ If yes: Good alignment
- ❌ If no: Question necessity (scope creep?)

2. **Future-proofing check:**
```bash
# Does PR block future capabilities?
cat dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md
```
- ✅ If extensible: Good design
- ❌ If hard-coded: Request refactoring

3. **Example review comment:**
```markdown
Thanks for this PR! A few observations:

**Wave Alignment:** ✅ This contributes to Wave 1.1 server catalog (good).

**Future-Proofing:** ⚠️ The hard-coded server list might block Wave 2 governance features (policy-driven server allowlists). Consider making this extensible:

```python
# Current (hard-coded)
ALLOWED_SERVERS = ["mcp-filesystem", "mcp-database"]

# Suggested (extensible for Wave 2)
def get_allowed_servers(policy: Policy = None) -> list[str]:
    policy = policy or DefaultPolicy()
    return policy.allowed_servers()
```

See [vision doc](link) for Wave 2 context.
```

---

## Decision Framework for Agents

**When encountering a design decision, follow this framework:**

### Step 1: Identify Current Context

```bash
# What wave are we in?
cat project-docs/WAVE_1X_PLAN.md

# What's the current roadmap?
cat ROADMAP.md
```

### Step 2: Check Vision for Future Requirements

```bash
# What do future waves need?
cat dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md
```

### Step 3: Apply Decision Matrix

|                               | **Supports Future Waves** | **Blocks Future Waves** | **Neutral** |
|-------------------------------|---------------------------|-------------------------|-------------|
| **Adds significant complexity** | ❓ **Defer** (validate need) | ❌ **Don't do**          | ❌ **Don't do** |
| **Minimal complexity increase** | ✅ **Do it**               | ❌ **Don't do**          | ✅ **Do it** (if needed for current wave) |
| **Simplifies architecture**     | ✅ **Do it**               | ⚠️ **Reconsider vision** | ✅ **Do it** |

### Step 4: Document Decision

**If decision is significant, create knowledge note:**

```python
from mcp_orchestrator.memory import create_note

create_note(
    content="""
    Architecture Decision: Chose plugin-based validation layer

    Context: Implementing config validation for Wave 1.1
    Decision: Use plugin architecture instead of hard-coded rules
    Rationale: Wave 2 governance requires extensible validation
    Trade-offs: Slightly more complex now, but enables Wave 2 without refactoring

    References:
    - dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md (Wave 2 requirements)
    - src/mcp_orchestrator/validation.py:45 (implementation)
    """,
    tags=["architecture", "validation", "wave-2-prep", "decision"],
    references=[
        "dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md",
        "src/mcp_orchestrator/validation.py"
    ]
)
```

---

## Quarterly Review Process

**Vision documents are reviewed quarterly to stay aligned with reality.**

### Review Schedule

- **Q1 (January):** After v1.0 release
- **Q2 (April):** After v1.5 release
- **Q3 (July):** After v2.0 release
- **Q4 (October):** After v2.5 release

### Review Tasks for Agents

**If you're running a quarterly review, follow these steps:**

**1. Assess Delivered Waves**

```bash
# Check what was delivered since last review
cat CHANGELOG.md | grep -A 10 "v0.2.0"
```

For each delivered wave:
```python
# Archive delivered wave
mv dev-docs/vision/WAVE_XX.md dev-docs/vision/archive/WAVE_XX.md

# Add delivery metadata
echo "
**Status:** Delivered in v0.2.0 (2025-11-15)
**Outcome:** All features shipped as planned
**Learnings:** [Document key learnings for future waves]
" >> dev-docs/vision/archive/WAVE_XX.md
```

**2. Evaluate Deferred Waves**

For waves previously deferred, check if criteria are now met:

```bash
# Check GitHub issues for demand signals
gh issue list --label "wave-2" --state all

# Count user requests
echo "User demand: $(gh issue list --label "wave-2" | wc -l) users"
```

If criteria met:
```markdown
**Decision:** Wave 2 criteria now met (52 users, threshold 50+).
**Action:** Move Wave 2 to ROADMAP.md for v1.5.0.
```

If criteria not met:
```markdown
**Decision:** Wave 2 criteria not met (15 users, threshold 50+).
**Action:** Defer to Q3 review.
```

**3. Identify New Waves**

```bash
# Check for emerging themes in issues
gh issue list --label "enhancement" --state open
```

If new capability themes emerge, add exploratory wave:
```markdown
## Wave 5: [New Theme]

**Status:** Exploratory (Q4 2025)
**User Signals:** 12 GitHub issues requesting [capability]
**Decision Criteria:** [Define criteria]
```

**4. Update Decision Criteria**

Based on learnings, update criteria for future waves:
```markdown
## Wave 3: Intelligence

**Updated Criteria (Q4 2025):**
- ~~100+ users requesting~~ → **50+ users requesting** (lowered based on adoption rate)
- AI model accuracy ≥95%
- Team capacity: 6+ months
```

**5. Document Review**

Add review entry to vision doc:
```markdown
## Review History

### 2025-10-24 (Q4 Review)

**Delivered:**
- Wave 1.1: Server catalog (v0.2.0)

**Committed:**
- Wave 1.2: Config composition (v0.3.0, target 2025-12-15)

**Deferred:**
- Wave 2: Governance (user demand: 15, threshold: 50)
- Wave 3: Intelligence (dependency: Wave 2 not started)

**New Waves:**
- Wave 5: Mobile support (exploratory, 12 GitHub issues)

**Updated Criteria:**
- Wave 3 user threshold lowered to 50+ (from 100+)
```

---

## Common Patterns for Agents

### Pattern 1: Check Before Implementing

**Before implementing any feature:**

```python
def should_implement_feature(feature_name: str) -> tuple[bool, str]:
    """Check if feature should be implemented now.

    Returns:
        (should_implement, reason)
    """
    # 1. Check current wave
    current_wave = get_current_wave()  # e.g., "1.1"

    # 2. Check if feature is in current wave plan
    wave_plan = read_wave_plan(current_wave)
    if feature_name in wave_plan["deliverables"]:
        return True, f"Feature is in Wave {current_wave} plan"

    # 3. Check if feature is in future wave (exploratory)
    vision = read_vision_doc()
    future_waves = [w for w in vision["waves"] if w["status"] == "exploratory"]

    for wave in future_waves:
        if feature_name in wave["capabilities"]:
            return False, f"Feature is exploratory in Wave {wave['id']}, not committed yet"

    # 4. Feature not in any wave
    return False, "Feature not in roadmap or vision"


# Usage
should_impl, reason = should_implement_feature("policy-engine")
if should_impl:
    implement_feature()
else:
    print(f"Skipping: {reason}")
```

### Pattern 2: Architecture Future-Proofing

**When designing modules:**

```python
def design_module_architecture(module_name: str) -> dict:
    """Design module with future waves in mind."""

    # 1. Read vision for next 2 waves
    vision = read_vision_doc()
    next_waves = vision["waves"][current_wave_index:current_wave_index+2]

    # 2. Identify extension points needed for future waves
    extension_points = []
    for wave in next_waves:
        for capability in wave["capabilities"]:
            if capability_affects_module(capability, module_name):
                extension_points.append({
                    "wave": wave["id"],
                    "capability": capability,
                    "extension_needed": infer_extension_point(capability)
                })

    # 3. Design with extension points
    return {
        "module": module_name,
        "core_features": get_current_wave_features(),
        "extension_points": extension_points,
        "extensibility": "plugin-based" if extension_points else "simple"
    }
```

### Pattern 3: Refactoring Evaluation

**When considering refactoring:**

```python
def evaluate_refactoring(module_name: str, technical_debt: str) -> str:
    """Evaluate if refactoring should happen now or be deferred.

    Returns:
        "refactor_now" | "defer_to_wave_X" | "defer_indefinitely"
    """
    # 1. Check if current wave is blocked
    current_wave_blocked = is_current_wave_blocked_by_debt(technical_debt)

    if current_wave_blocked:
        return "refactor_now"

    # 2. Check if next wave needs this module
    next_wave = get_next_wave()
    next_wave_needs_module = module_name in next_wave["affected_modules"]

    if next_wave_needs_module:
        return "refactor_now"

    # 3. Defer refactoring (YAGNI principle)
    future_wave = find_wave_needing_module(module_name)
    if future_wave:
        return f"defer_to_wave_{future_wave['id']}"
    else:
        return "defer_indefinitely"
```

---

## Memory Integration

**Emit events for vision-related decisions:**

```python
from mcp_orchestrator.memory import emit_event, create_note

# Architecture decision informed by vision
emit_event("vision.architecture_decision", status="success",
           metadata={
               "decision": "plugin-based-validation",
               "current_wave": "1.1",
               "future_wave_enabled": "2.0",
               "rationale": "Enables governance without breaking changes"
           })

# Wave review completed
emit_event("vision.quarterly_review", status="success",
           metadata={
               "quarter": "Q4 2025",
               "waves_delivered": ["1.1"],
               "waves_committed": ["1.2"],
               "waves_deferred": ["2.0", "3.0"]
           })

# Feature request evaluated against vision
emit_event("vision.feature_evaluation", status="success",
           metadata={
               "feature": "policy-engine",
               "wave": "2.0",
               "status": "deferred",
               "reason": "user_demand_below_threshold"
           })
```

**Create knowledge notes for strategic decisions:**

```python
create_note(
    content="""
    Refactoring Decision: Deferred storage layer refactoring to Wave 1.2

    Context: Storage module has technical debt (nested functions, no tests)
    Vision Check: Wave 1.2 needs storage refactoring for config composition
    Decision: Defer refactoring to Wave 1.2 (not blocking current wave)
    Reasoning: YAGNI principle - no immediate need, next wave will require it anyway

    References:
    - dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md (Wave 1.2 requirements)
    - project-docs/WAVE_1X_PLAN.md (current wave deliverables)
    """,
    tags=["refactoring", "defer", "wave-1.2", "storage", "decision"],
    references=[
        "dev-docs/vision/MCP_CONFIG_ORCHESTRATION.md",
        "project-docs/WAVE_1X_PLAN.md"
    ]
)
```

---

## Related Documentation

- **[README.md](README.md)** - Vision documents overview
- **[MCP_CONFIG_ORCHESTRATION.md](MCP_CONFIG_ORCHESTRATION.md)** - Core product vision
- **[../../ROADMAP.md](../../ROADMAP.md)** - Committed roadmap
- **[../../project-docs/AGENTS.md](../../project-docs/AGENTS.md)** - Wave planning
- **[../AGENTS.md](../AGENTS.md)** - Contributing workflows
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview

---

## Vision Document Checklist for Agents

**When reading vision documents, extract:**

- [ ] Current wave status (committed vs exploratory)
- [ ] Next 1-2 waves and their capabilities
- [ ] Decision criteria for next wave
- [ ] Technical requirements for future waves
- [ ] User demand signals
- [ ] Dependencies between waves

**When making architecture decisions, consider:**

- [ ] Does this block future waves?
- [ ] Does this enable future waves?
- [ ] Is the complexity justified by current + future needs?
- [ ] Can I defer this decision to a future wave?
- [ ] Should I document this decision for future reference?

**When reviewing PRs, check:**

- [ ] Aligns with current wave plan
- [ ] Doesn't block future waves
- [ ] Extensibility matches vision requirements
- [ ] Complexity is justified by roadmap

---

**End of Vision Documents Usage Guide**

For questions not covered here, see [README.md](README.md) for vision document philosophy or [../../AGENTS.md](../../AGENTS.md) for project overview.
