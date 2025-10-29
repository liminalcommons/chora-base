# Coordination Request Rationale: Why Inbox Protocol?

**Request ID**: coord-001
**Created**: 2025-10-28
**Question**: Why use inbox protocol for cross-conversation coordination?

---

## The Situation

We had a strategic conversation about chora-compose as a "capability broker" and arrived at a conclusion: **chora-base should contain SAPs that teach agents how to use chora-compose**.

Now we need to communicate this to another Claude Code conversation (the one actively working on Wave 2 execution) so they can create the SAPs.

**Three options for communication**:

1. **Human copy-paste**: User copies our discussion to the other conversation
2. **Shared file**: Create a file both conversations read
3. **Inbox protocol**: Use chora-base's coordination system

We chose **Option 3: Inbox Protocol**. Here's why.

---

## Why Inbox Protocol?

### 1. **It's Idiomatic to Chora-Base**

Chora-base has a built-in cross-repository coordination system: **the inbox protocol** ([SAP-001](../../docs/skilled-awareness/inbox/)).

**Inbox supports three intake types**:
- **Type 1 (Strategic)**: `inbox/ecosystem/proposals/` - Quarterly review
- **Type 2 (Coordination)**: `inbox/incoming/coordination/` - Sprint planning review
- **Type 3 (Tasks)**: `inbox/incoming/tasks/` - Continuous intake

Our work is **Type 2 (Coordination)**:
- ✅ Spans multiple "repos" (in this case, multiple Claude conversations)
- ✅ Requires sprint planning review (Wave 2 is in progress)
- ✅ Has dependencies (SAP-000, SAP-002, SAP-016)
- ✅ Part of coordinated work (Wave 2 SAP content audit)

**Using inbox is the right tool for the job.**

---

### 2. **It Demonstrates the Pattern We're Documenting**

We're creating SAPs for **chora-compose**, which will enable **inbox-based coordination** across ecosystem repos. Using inbox protocol to coordinate this work is **meta-dogfooding**.

**The beautiful recursion**:
```
Using inbox protocol
  → to coordinate SAP creation
    → for capability (chora-compose)
      → that enables inbox-compatible coordination
        → across ecosystem repos
```

This demonstrates:
- Inbox works for cross-context coordination (not just cross-repo)
- SAPs are executable communication (not just documentation)
- Chora-base patterns apply to chora-base development itself

**Dogfooding = credibility.**

---

### 3. **It's Explicit and Auditable**

**Option 1 (copy-paste)** problems:
- No record of what was communicated
- No trace of decision-making
- Can't replay or audit the coordination

**Option 2 (shared file)** problems:
- No workflow structure
- Unclear who owns what
- No acceptance criteria
- No completion tracking

**Option 3 (inbox protocol)** benefits:
- ✅ Structured JSON contract (`coord-001-chora-compose-sap.json`)
- ✅ Complete context document (`coord-001-chora-compose-sap-CONTEXT.md`)
- ✅ Clear deliverables and acceptance criteria
- ✅ Timeline and dependencies explicit
- ✅ Event log tracks completion (`inbox/coordination/events.jsonl`)
- ✅ Trace ID enables correlation (`chora-compose-sap-creation-2025-10-28`)

**Everything is trackable.**

---

### 4. **It Respects Development Process**

From [INBOX_PROTOCOL.md](../../inbox/INBOX_PROTOCOL.md):

> **Design Philosophy:** "Ecosystem communications influence team direction" - Strategic proposals and coordination requests flow through proper planning phases (Vision & Strategy → Planning & Prioritization) before becoming implementation tasks.

Our request:
- ✅ Aligns with Vision & Strategy (v4.0 multi-repo coordination)
- ✅ Enters at Planning phase (Wave 2 sprint planning can integrate immediately)
- ✅ Respects existing workflow (doesn't bypass process)

**We're following the process we're building.**

---

### 5. **It Enables Asynchronous Coordination**

The other conversation (Wave 2 execution) can:
1. **Discover** the request when they check inbox
2. **Review** the context and decide if it fits their sprint
3. **Accept** by moving to `inbox/active/`
4. **Execute** when they have bandwidth
5. **Complete** and emit event when done

**No real-time coordination needed.** The inbox is the queue.

This mirrors how cross-repo coordination works:
- Repo A creates coordination request
- Repo B discovers it (via pull, API, notification)
- Repo B accepts and executes
- Both repos emit events with shared trace_id

**Same pattern, different context.**

---

### 6. **It Creates a Historical Record**

When this work is complete, we'll have:

```
inbox/completed/coord-001-chora-compose-sap/
├── coord-001-chora-compose-sap.json          # Original request
├── coord-001-chora-compose-sap-CONTEXT.md    # Full background
├── coord-001-chora-compose-sap-RATIONALE.md  # This document
├── events.jsonl                               # Work timeline
└── metadata.json                              # Completion data
```

Future maintainers can:
- See why SAP-017 and SAP-018 were created
- Understand the decision-making process
- Trace the cross-conversation coordination
- Learn from the pattern

**Knowledge compounds.**

---

## What Makes This Special?

### **First Cross-Conversation Coordination Example**

To our knowledge, this is the **first documented case** of:
- Using inbox protocol to coordinate between two Claude Code sessions
- Treating separate conversations as "repos" in the coordination model
- Demonstrating SAPs as "capability transmission protocol" across contexts

**This establishes a pattern** for:
- Handing off work between sessions
- Coordinating complex multi-session workflows
- Using chora-base patterns for chora-base development

---

## Alternative Approaches (And Why We Didn't Use Them)

### Approach 1: User Manual Handoff

**How it would work**:
1. User reads this conversation
2. User switches to Wave 2 conversation
3. User types: "Create SAP-017 and SAP-018 for chora-compose"
4. User pastes our discussion as context

**Problems**:
- ❌ User becomes the "communication protocol" (error-prone)
- ❌ No structured deliverables or acceptance criteria
- ❌ Context gets compressed/lost in translation
- ❌ No auditability (what was actually communicated?)
- ❌ Doesn't demonstrate chora-base patterns

**Why inbox is better**: Explicit contract, complete context, auditable.

---

### Approach 2: Direct File Creation

**How it would work**:
1. This conversation creates SAP-017 and SAP-018 files directly
2. Wave 2 conversation discovers them when running inventory
3. Wave 2 conversation validates/enhances them

**Problems**:
- ❌ Bypasses Wave 2's planning process
- ❌ No coordination workflow (surprise files appear)
- ❌ Unclear ownership (who maintains these SAPs?)
- ❌ Violates "respect development process" principle
- ❌ Doesn't establish coordination pattern

**Why inbox is better**: Respects process, clear ownership, explicit acceptance.

---

### Approach 3: Shared TODO List

**How it would work**:
1. Add "Create chora-compose SAPs" to shared todo list
2. Wave 2 conversation picks it up when reviewing todos
3. Execute

**Problems**:
- ❌ No context beyond todo item title
- ❌ No structured deliverables
- ❌ No dependencies or acceptance criteria
- ❌ Can't audit what was requested vs. delivered
- ❌ TODO != coordination protocol

**Why inbox is better**: Structured contract, dependencies explicit, auditable.

---

## Inbox Protocol Advantages Summary

| Aspect | Manual Handoff | Direct Files | Shared TODO | Inbox Protocol |
|--------|----------------|--------------|-------------|----------------|
| **Structured** | ❌ | ❌ | ❌ | ✅ JSON schema |
| **Complete Context** | ⚠️ Lossy | ❌ None | ❌ None | ✅ CONTEXT.md |
| **Auditable** | ❌ | ❌ | ❌ | ✅ events.jsonl |
| **Respects Process** | ⚠️ Maybe | ❌ Bypass | ⚠️ Maybe | ✅ Yes |
| **Async** | ❌ Real-time | ⚠️ Polling | ⚠️ Polling | ✅ Queue-based |
| **Ownership** | ⚠️ Unclear | ⚠️ Unclear | ⚠️ Unclear | ✅ Clear |
| **Dependencies** | ❌ Implicit | ❌ None | ❌ None | ✅ Explicit |
| **Acceptance Criteria** | ❌ Vague | ❌ None | ❌ None | ✅ Explicit |
| **Historical Record** | ❌ None | ❌ None | ❌ None | ✅ Complete |
| **Demonstrates Pattern** | ❌ No | ❌ No | ❌ No | ✅ Meta-dogfooding |

**Winner**: Inbox Protocol

---

## Meta-Insight: Inbox as "Capability Transmission Medium"

In our strategic conversation, we discussed **chora as a capability transmission protocol**:

> "Chora isn't just a template or framework—it's a **protocol for transmitting architectural intelligence between LLM-augmented systems**."

**This coordination request IS that protocol in action**:

1. **Discovery**: SAPs define what capabilities exist (SAP-017, SAP-018)
2. **Transmission**: Inbox carries capability knowledge across contexts
3. **Adoption**: Wave 2 conversation receives and integrates
4. **Execution**: SAPs get created following blueprints
5. **Coordination**: Events track the flow

**The medium (inbox) and the message (SAPs) are unified.**

This is the vision we're documenting in the chora-compose SAPs, demonstrated by the very act of creating them.

---

## Expected Outcomes

### For Wave 2 Execution Conversation

**When they check inbox**, they'll find:
- ✅ Clear request with structured deliverables
- ✅ Complete context (113 docs researched, decisions documented)
- ✅ Ready-to-execute templates
- ✅ Validation criteria (SAP-016 link checking)
- ✅ Integration path (fits Wave 2 goals)

**They can**:
1. Accept immediately (aligns with Wave 2)
2. Execute with confidence (everything is explicit)
3. Validate success (acceptance criteria clear)
4. Complete and move on (emit event, archive)

### For Chora-Base Ecosystem

**After completion**, we'll have:
- ✅ Two new SAPs (SAP-017, SAP-018)
- ✅ Ecosystem repos can adopt chora-compose
- ✅ Agents "just know" when/how to use chora-compose
- ✅ First cross-conversation coordination example
- ✅ Proof that inbox protocol works beyond repos

### For Future Work

**This establishes**:
- ✅ Pattern for cross-conversation coordination
- ✅ Pattern for complex handoffs
- ✅ Pattern for meta-dogfooding
- ✅ Confidence that chora-base patterns scale

---

## Conclusion

We chose inbox protocol because it's:
1. **Idiomatic** - The right tool for coordination
2. **Meta** - Demonstrates the pattern we're documenting
3. **Explicit** - Everything is auditable
4. **Respectful** - Follows development process
5. **Async** - No real-time coordination needed
6. **Historical** - Creates permanent record

**It's not just communication—it's capability transmission.**

By using inbox to coordinate SAP creation for chora-compose, we demonstrate:
- Inbox works across contexts (not just repos)
- SAPs are executable (not just documentation)
- Chora patterns apply to chora development (meta-dogfooding)

**This is the way.**

---

**Document Version**: 1.0
**Created**: 2025-10-28
**Author**: Claude Code (Strategic Planning)
**For**: Anyone wondering "why inbox?"
**Status**: Final rationale
