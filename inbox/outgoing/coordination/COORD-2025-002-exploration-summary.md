# Exploratory Request to chora-compose: Documentation Generation Collaboration?

**From**: chora-base team
**To**: chora-compose team
**Date**: 2025-10-29
**Type**: Exploratory (not implementation request)
**Priority**: Medium / Backlog

---

## TL;DR

**Our Question**: Is structured documentation generation within chora-compose's vision, or is it purely Docker orchestration?

**Why We're Asking**: Exploring generation-based SAP artifacts for v4.2.0+. Your project name suggests "composition" - wondering if that extends beyond containers to content.

**What We Need**: Clarity on your scope and vision. If docs generation is out of scope, that's totally fine - we'll explore other approaches!

**No Pressure**: This doesn't affect our v4.1.0 work. Just exploring options for v4.2.0+ (Q2 2026).

---

## Our Situation

### What We're Doing

chora-base maintains **18 SAPs** (Skilled Awareness Packages) - structured documentation packages for AI agent capabilities.

**Each SAP = 5 Artifacts**:
1. `capability-charter.md` - WHAT/WHY (2-3k tokens)
2. `protocol-spec.md` - HOW (3-4k tokens)
3. `awareness-guide.md` - WHEN/WHERE (4-5k tokens)
4. `adoption-blueprint.md` - INSTALL (3-4k tokens)
5. `ledger.md` - WHO adopted (1-2k tokens)

**Current Pain**: Hand-writing these takes 8-12 hours per SAP × 18 SAPs = 144-216 hours total.

### What We're Exploring

**Hypothesis**: Could we generate SAP artifacts from **constituent content blocks** + **context**?

```
Constituent Content Blocks (stored)
         +
Context (repo role, capabilities)
         ↓
   Composition Engine (?)
         ↓
Generated SAP Artifacts (cached or fresh)
```

**Question**: What tool would be the composition engine?

**Options We're Considering**:
1. Custom Python script (full control, high effort)
2. LLM API directly (quality variability, cost)
3. Template engine like Jinja2 (limited adaptability)
4. External tool - **maybe chora-compose?** (if aligned)

---

## Why We're Reaching Out to You

### What We Know About chora-compose

From SAP-017 and SAP-018 in chora-base:

- **Primary focus**: Docker Compose orchestration for AI agent development environments
- **Capabilities**: Multi-container orchestration, volume management, service dependencies
- **Repository**: https://github.com/liminalcommons/chora-compose (we think - see question below)

### What We're Wondering

**The name "chora-compose" suggests composition**. We're curious:

1. Is "compose" just about Docker containers, or is there a broader composition vision?
2. Have you considered or experimented with documentation/artifact generation?
3. Would this collaboration align with your goals, or is it orthogonal?

### What We're NOT Assuming

❌ We are NOT assuming you're a content generation tool
❌ We are NOT requesting you build features for us
❌ We are NOT trying to redirect your roadmap

✅ We ARE genuinely curious about your vision
✅ We ARE open to hearing "not in scope"
✅ We ARE exploring multiple options

---

## The Use Case (If You're Curious)

### SAP Structure Example

**SAP-004: Testing Framework**

```
docs/skilled-awareness/testing-framework/
  ├── capability-charter.md      (~2.5k tokens)
  ├── protocol-spec.md            (~3.5k tokens)
  ├── awareness-guide.md          (~4.5k tokens)
  ├── adoption-blueprint.md       (~3.5k tokens)
  └── ledger.md                   (~1.5k tokens)
Total: ~15.5k tokens, 8-12 hours to write
```

### Generation Concept

**Constituent Content Blocks**:
```
content-blocks/
  ├── testing-framework-problem.md     (reusable)
  ├── testing-framework-solution.md    (reusable)
  ├── pytest-setup-instructions.md     (reusable)
  ├── coverage-requirements.md         (reusable)
  └── ...
```

**Context** (provided at generation time):
```json
{
  "target_repo": "/path/to/my-project",
  "repo_role": "mcp-server-developer",
  "existing_capabilities": ["docker-packaging", "ci-cd"],
  "preferences": {
    "verbosity": "concise",
    "include_examples": true
  }
}
```

**Generation**:
```
Composition Engine selects relevant content blocks
  + applies context (repo role, existing capabilities)
  + generates coherent SAP artifacts
  → Output: 5 customized markdown files
```

**Caching**:
- "Latest": Use cached artifacts if available (fast)
- "Fresh": Regenerate from content blocks (current)

### Why This Matters

**Benefits**:
- ✅ **Consistency**: All SAPs follow same patterns
- ✅ **Efficiency**: 8-12 hours → 1-2 hours per SAP
- ✅ **Adaptability**: Same SAP, different contexts → customized output
- ✅ **Maintenance**: Update content blocks once, regenerate all
- ✅ **Scalability**: Enable 50+ SAPs without overwhelming burden

**Challenges**:
- ❌ Quality must match hand-written SAPs (high bar)
- ❌ Need tooling/infrastructure for composition
- ❌ Caching and versioning complexity
- ❌ Risk of losing hand-crafted nuance

---

## Our Questions for You

### Vision & Scope

1. **Is chora-compose solely Docker orchestration, or is there a broader 'composition' vision?**

2. **Have you considered structured documentation generation as a use case?**

3. **What does "compose" mean in your project's context?**
   (containers? content? capabilities? other?)

4. **Is there a roadmap or vision document we should review?**

### Current Capabilities

5. **What's the most complex multi-artifact generation you've done with chora-compose?**

6. **Do you have templating or content composition capabilities today?**

7. **Can chora-compose orchestrate multi-step workflows beyond Docker containers?**

8. **Are there examples of using chora-compose for documentation or artifact generation?**

### Potential Collaboration

9. **If documentation generation WAS in scope, what would be a natural extension vs. completely new capability?**

10. **Would a collaboration around structured docs benefit chora-compose's goals, or is it orthogonal?**

11. **Are there other projects in the ecosystem doing content generation we should know about?**

12. **What would make this exploration valuable for chora-compose, not just chora-base?**

### Clarification

13. **SAP-017 and SAP-018 reference two different GitHub URLs:**
    - `github.com/liminalcommons/chora-compose`
    - `github.com/chrisdburr/chora-compose`
    **Which is canonical?**

14. **Is there documentation beyond SAP-017/018 we should review?**

15. **Who are the right people to discuss this with?**

---

## How We Could Collaborate (If Aligned)

### Option 1: Quick Feedback (30 min)

**What**: Brief response clarifying scope and vision

**Outcome**: We understand if documentation generation is in/out of scope

**Your Effort**: 30 minutes to review and respond

### Option 2: Discovery Call (1 hour)

**What**: Video call where:
- chora-base shares SAP structure and needs
- chora-compose shares capabilities and vision
- We explore alignment

**Outcome**: Mutual understanding of potential fit

**Your Effort**: 1 hour call + 30 min prep

### Option 3: Experiment Together (4-8 hours each)

**What**: Collaborate on small prototype
- Pick 1 simple SAP (e.g., SAP-004)
- Decompose into content blocks
- Test generation approach
- Assess quality and feasibility

**Outcome**: Working example OR clear understanding of why it won't work

**Your Effort**: 4-8 hours over 1-2 weeks

### Option 4: Redirect (30 min)

**What**: You suggest alternative tools/approaches better suited for our use case

**Outcome**: We explore other directions, no wasted effort

**Your Effort**: 30 minutes to review and suggest alternatives

### Option 5: Defer (5 min)

**What**: Interesting but not right timing - revisit in 6-12 months

**Outcome**: We pursue other approaches, keep door open for future

**Your Effort**: 5 minutes to acknowledge and defer

---

## What We're NOT Requesting

❌ Implementation of SAP generation features
❌ Commitment to build new capabilities
❌ Changes to chora-compose roadmap
❌ Integration work on your side
❌ Urgent response or decision

---

## What Would Be Helpful

✅ Understanding chora-compose's vision and scope
✅ Clarification on whether documentation generation fits or is orthogonal
✅ Pointers to alternative tools if this is out of scope
✅ Honest assessment of alignment (even if answer is "not aligned")

---

## Our Timeline

### v4.1.0 (Q1 2026) - Proceeding Regardless

**Wave 5: SAP Sets** (storage-based, no generation)
- Simple SAP bundles (e.g., "minimal-entry" = 5 SAPs)
- `python scripts/install-sap.py --set minimal-entry`
- **Doesn't depend on chora-compose or any external tool**

### v4.2.0 (Q2 2026+) - Depends on Exploration

**Wave 6: Collections Architecture** (potentially generation-based)
- Scope depends on:
  1. v4.1.0 pilot feedback from chora-workspace
  2. Tool exploration outcomes (this request)
  3. Value vs. complexity assessment

**Three Options**:
- **Option A**: Rich metadata only (no generation) - 18-26 hours
- **Option B**: Generation-based collections - 81-138 hours (depends on tooling)
- **Option C**: Defer to v4.3.0+ if not ready

**Your response helps inform**: Which option we pursue

---

## References

### In chora-base

**SAP Framework**:
- `docs/skilled-awareness/sap-framework/` (SAP-000 - defines 5-artifact pattern)
- `sap-catalog.json` (machine-readable registry of all 18 SAPs)

**Example SAP**:
- `docs/skilled-awareness/testing-framework/` (SAP-004 - shows structure)

**Your Documentation**:
- `docs/skilled-awareness/chora-compose-integration/` (SAP-017)
- `docs/skilled-awareness/chora-compose-meta/` (SAP-018)

**Exploration Docs**:
- `docs/design/collections-exploration-notes.md` (detailed architectural questions)
- `docs/project-docs/CHORA-BASE-4.0-VISION.md` (Wave 6 planning)

### Related Coordination

**COORD-2025-001**: chora-workspace requested lightweight SAP onboarding
- **Our response**: SAP sets in v4.1.0 (accepted)
- **This led to**: Collections exploration (Wave 6)

---

## How to Respond

### Via Inbox Protocol (Preferred if you use it)

Create response file in your repo:
```
chora-compose/inbox/outgoing/COORD-2025-002-response.json
```

We'll monitor your repo for the response.

### Via GitHub

**Option 1**: Comment on this coordination request (if we open as GitHub issue)

**Option 2**: Open issue in chora-base referencing COORD-2025-002

### Via Email/Direct

Contact chora-base maintainers directly and reference COORD-2025-002

---

## Our Tone

**We're genuinely curious**, not prescriptive.

Honest feedback is valuable:
- ✅ "This aligns with our vision, let's explore!"
- ✅ "Interesting but not our focus - try [alternative tool]"
- ✅ "Not aligned with chora-compose's direction"
- ✅ "Maybe in the future, but not now"

**All of these are helpful responses!** We'd rather know early than pursue misaligned paths.

---

## Thank You!

We recognize you may have clear priorities and this may not fit. We appreciate you taking time to review this exploration request.

**No obligation to respond urgently** - we're proceeding with v4.1.0 regardless and have time before v4.2.0 decisions are needed.

If there's alignment, great! If not, that's completely fine and we'll explore other approaches.

— chora-base team

**Date**: 2025-10-29
**Status**: Awaiting chora-compose feedback (no deadline)
**Related**: COORD-2025-001 (chora-workspace collaboration)
