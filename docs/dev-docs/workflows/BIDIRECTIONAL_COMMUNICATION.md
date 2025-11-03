# Bidirectional Communication: Mutual Ergonomics Pattern

**Purpose**: Define how to translate between natural conversational user input and procedural ecosystem execution, enabling mutual adaptation between user and agent.

**Core Principle**: The system should meet users where they are, not force them to learn its language first. Both parties learn and adapt over time.

---

## 1. Overview

### The Translation Challenge

```
USER SIDE                    TRANSLATION LAYER                SYSTEM SIDE
(Natural Language)          (Bidirectional)                   (Procedural)

"Show me what's             →  Intent Router    →            run_inbox_status()
 in the inbox"

"How are SAPs?"             →  Pattern Match    →            sap_evaluator --quick

"I want to suggest          →  Semantic         →            create_strategic_proposal
 a big change"                 Analysis                      (Type 1 intake)

                            ←  Display          ←             ✅ prop-005 created
Result visualization           Formatter                      Score: 42/50
```

### Key Components

1. **Intent Router** - Natural language → Formal actions
2. **Glossary Search** - Terminology discovery and reverse lookup
3. **User Preferences** - Adaptive behavior based on working style
4. **Suggestion Engine** - Context-aware next action recommendations
5. **Output Formatter** - Results → Digestible insights

---

## 2. Communication Patterns

### Pattern 1: Natural Input → Recognition → Clarification → Execution

**Flow**:
```
User: "show me what's pending"
  ↓
Intent Router: Matches "inbox_status" pattern (confidence: 95%)
  ↓
Agent: ✅ High confidence → Execute directly
  ↓
Output: Inbox status dashboard (formatted per user preferences)
```

**When Ambiguous (confidence 50-70%)**:
```
User: "check coordination stuff"
  ↓
Intent Router: Possible matches:
  - review_coordination_requests (65%)
  - inbox_status (55%)
  ↓
Agent: ⚠️ Medium confidence → Ask for clarification
  "Did you mean: Review coordination requests? (65% confidence)"
  ↓
User: "yes"
  ↓
Execute: review_coordination_requests
```

**When Low Confidence (<50%)**:
```
User: "coordenation stuf"  # Typo
  ↓
Intent Router: No good matches (best: 35%)
  ↓
Agent: 🤔 Low confidence → Show alternatives
  "Did you mean one of these?"
  1. Review coordination requests (35%)
  2. Inbox status (30%)
  3. Search glossary for 'coordination' (suggested)
  ↓
User: Selects option or rephrases
```

### Pattern 2: Progressive Formalization

**Lifecycle**:
```
CASUAL → SEMI-FORMAL → FORMAL → EXECUTABLE

"I want to add health monitoring"
  ↓ (Intent recognition + clarification)
Strategic Proposal (Type 1 intake)
  ↓ (Template-based structure)
prop-005-health-monitoring.md
  ↓ (Triage scoring)
Score: 42/50 → Accept
  ↓ (RFC discussion)
RFC-0005-health-monitoring.md
  ↓ (Final decision)
ADR-0005-adopt-health-checks.md
  ↓ (Implementation breakdown)
coord-XXX, coord-YYY, coord-ZZZ
  ↓ (DDD → BDD → TDD)
Executable code + tests
```

**Key Insight**: Each step adds formality while preserving intent.

### Pattern 3: Adaptive Output Formatting

**Based on User Preferences**:

```python
# User preferences: verbosity=concise, formality=casual
Output: "✅ 12 SAPs installed. 2 at Level 2. Top gap: SAP-004 coverage at 60%."

# User preferences: verbosity=verbose, formality=formal
Output:
"""
SAP Adoption Status Report
==========================
Current State: 12/18 capabilities installed (67% coverage)

Level Distribution:
- Level 0 (Not Installed): 6 SAPs
- Level 1 (Basic): 10 SAPs
- Level 2 (Integrated): 2 SAPs (SAP-004, SAP-019)
- Level 3 (Optimized): 0 SAPs

Priority Gap: SAP-004 (testing-framework)
- Current coverage: 60% (target: ≥85%)
- Recommended action: Add 45 tests to critical paths
- Estimated effort: 4-6 hours
"""
```

**Progressive Disclosure**:
```
# Initial response (summary)
"✅ 12/18 SAPs installed. 2 at Level 2."

# User: "show more"
"Top gaps:
 1. SAP-004 coverage: 60% (need 85%)
 2. SAP-012 BDD adoption: 40% (need 80%)
 3. SAP-001 event logging incomplete"

# User: "details on SAP-004"
[Full gap analysis with specific files and recommendations]
```

### Pattern 4: Conversational Context Retention

**Session-Based Memory**:
```
User: "Show inbox status"
Agent: [Displays inbox with 3 coordination requests]

User: "Review the first one"
Agent: [Recognizes "first one" = first coordination request from previous output]
      [Loads coord-003.json and displays details]

User: "Accept it"
Agent: [Recognizes "it" = coord-003]
      [Moves to active/, emits event, creates change-request.md]
```

**Cross-Turn Reference Resolution**:
- "it", "that", "the previous one" → Track referents
- Session context maintained for N turns (configurable)
- Reset on explicit "new topic" or timeout

---

## 3. Tools & Scripts

### 3.1 Intent Router

**Script**: `scripts/intent-router.py`

**Usage**:
```bash
# Single query
python scripts/intent-router.py "show me what's in the inbox"
# Output: ✅ Matched: run_inbox_status (confidence: 95%)

# Interactive mode
python scripts/intent-router.py --interactive
> show me what's pending
> check sap status
> quit

# Learn new pattern
python scripts/intent-router.py --learn "what's cooking" --action inbox_status
# Now "what's cooking" → inbox_status
```

**Integration in Agents**:
```python
# AGENTS.md or CLAUDE.md
from intent_router import IntentRouter

router = IntentRouter("docs/dev-docs/patterns/INTENT_PATTERNS.yaml")
matches = router.route(user_input)

if matches and matches[0].confidence >= 0.7:
    action = matches[0].action
    # Execute action
else:
    # Ask for clarification
```

### 3.2 Glossary Search

**Script**: `scripts/chora-search.py`

**Usage**:
```bash
# Forward lookup (term → definition)
python scripts/chora-search.py "coordination request"

# Reverse lookup (description → term)
python scripts/chora-search.py --reverse "I want to suggest a big change"
# Output: Strategic Proposal (95% match)

# Fuzzy matching (handles typos)
python scripts/chora-search.py --fuzzy "coordenation"
# Output: Coordination Request (82% similarity)

# Related terms
python scripts/chora-search.py --related "strategic proposal"
# Output: RFC, ADR, Coordination Request
```

**Integration in Conversations**:
```
User: "What's a coordination request?"
  ↓
Agent: [Detects "what's" + terminology]
       [Calls chora-search.py "coordination request"]
       [Returns definition from GLOSSARY.md]
  ↓
Output:
  "📖 Coordination Request
   Type 2 intake for cross-repo dependencies reviewed during sprint planning.

   Related: Strategic Proposal, Implementation Task
   Example: Coordinating testing improvements between chora-base and chora-compose"
```

### 3.3 User Preferences

**File**: `.chora/user-preferences.yaml`

**Loading Order**:
1. System defaults (hardcoded)
2. `.chora/user-preferences.yaml` (user-specific)
3. Environment variables (temporary overrides)

**Example Adaptation**:
```python
# Load preferences
with open(".chora/user-preferences.yaml") as f:
    prefs = yaml.safe_load(f)

# Adapt verbosity
if prefs["communication"]["verbosity"] == "concise":
    return summary_only()
elif prefs["communication"]["verbosity"] == "verbose":
    return full_details()

# Adapt formality
if prefs["communication"]["formality"] == "casual":
    return "Let's check the inbox! 📥"
elif prefs["communication"]["formality"] == "formal":
    return "Initiating inbox status query."
```

### 3.4 Suggestion Engine

**Script**: `scripts/suggest-next.py`

**Usage**:
```bash
# Reactive mode (user asked "what next?")
python scripts/suggest-next.py

# Proactive mode (background check, high-priority only)
python scripts/suggest-next.py --mode proactive

# Comprehensive mode (all possibilities)
python scripts/suggest-next.py --mode comprehensive
```

**Context Signals Used**:
- Recent events (event log)
- Active work items (inbox/active/)
- Current phase (DDD/BDD/TDD detection)
- Quality metrics (coverage, lint, tests)
- Inbox backlog

**Example Output**:
```
💡 Suggested Next Actions
=========================

1. 🔴 ⚙️ Start BDD scenarios
   Change request complete for task-005. Ready to write Gherkin scenarios.
   ⏱️  Estimated time: 1-2 hours
   📝 Command: python scripts/start-bdd.py task-005

2. 🟡 ✅ Improve test coverage (currently 72%)
   Coverage below 85% target. Add tests for uncovered code.
   ⏱️  Estimated time: 1-3 hours
   📝 Command: pytest --cov=src --cov-report=html

3. 🟢 📋 Review coordination requests
   3 pending coordination request(s) in inbox.
   ⏱️  Estimated time: 15-30 minutes
   📝 Command: python scripts/inbox-status.py
```

---

## 4. Interaction Modes

### Mode 1: Conversational (Phase 1 - Vision & Strategy)

**Characteristics**:
- Open-ended exploration
- Brainstorming and ideation
- No rigid structure
- Meta-systemic thinking encouraged

**Agent Behavior**:
- Ask clarifying questions
- Explore alternatives
- Surface related concepts
- Capture ideas for later formalization

**Example**:
```
User: "I'm thinking about traceability enhancements"

Agent: "Interesting! A few clarifying questions:
 1. Is this about link validation (SAP-016)?
 2. Or broader requirements traceability (REQ → TEST mapping)?
 3. Or something else?

 Also, what pain point triggered this? That helps scope the solution."

User: "We had 220 broken links in Wave 2. Want to prevent that."

Agent: "Got it - link rot prevention. That aligns with SAP-016 enhancements.

 Quick options:
 A. Extend existing link validator (scripts/validate-links.sh)
 B. Add bidirectional link tracking (reverse lookups)
 C. Both

 Also relevant: Cross-SAP dependency visualization would help impact analysis.

 Want to explore these or something else?"
```

### Mode 2: Hybrid (Phase 2 - Planning)

**Characteristics**:
- Structured but flexible
- Discussion → Artifact creation
- Prioritization and trade-offs
- Decision capture

**Agent Behavior**:
- Guide toward sprint plan template
- Suggest using triage framework
- Offer to create artifacts
- Balance conversation with procedure

**Example**:
```
User: "Let's plan the traceability work"

Agent: "I'll help you plan. Using the triage framework (SAP-001):

 Q1: Is this a strategic proposal (Type 1) or coordination request (Type 2)?
     → Seems like coordination request (fits in 1-2 sprints)

 Q2: Priority? (P0/P1/P2)
     → P1 (high value, but not blocking current sprint)

 Q3: Estimated effort?
     → Based on 80-20 analysis: 15-21 hours pilot

 Should I create coord-XXX.json for sprint planning review?
 Or want to discuss scope first?"
```

### Mode 3: Procedural (Phase 3-8 - Execution)

**Characteristics**:
- Artifact-first communication
- Tools and status updates
- Minimal explanation
- Efficiency-focused

**Agent Behavior**:
- Execute → Display result
- Don't explain what will happen, show what happened
- Use todos for tracking
- Emit events for traceability

**Example**:
```
User: "Create the coordination request for traceability"

Agent: ✅ Created inbox/incoming/coordination/coord-007-traceability-pilot.json
       ✅ Logged event: coordination_request_created
       ✅ Updated inbox status

       Next: Submit for sprint planning (2025-11-15)
       Track: python scripts/inbox-status.py --filter coordination

       Want me to draft the change request (DDD Phase 3)?
```

---

## 5. Learning & Adaptation

### Pattern Learning

**How It Works**:
```
User: "what's cooking in the inbox?"
  ↓
Agent: [Runs intent router, matches "inbox_status" with 75% confidence]
       [Executes action successfully]
       [Logs usage: "what's cooking" → inbox_status]
  ↓
After 3+ successful uses:
  Intent router adds "what's cooking" to inbox_status triggers
  Future confidence: 95%
```

**Pattern Evolution**:
```yaml
# Before learning
triggers:
  - show inbox
  - inbox status
  - what's in the inbox

# After learning (user says "what's cooking" 3 times)
triggers:
  - show inbox
  - inbox status
  - what's in the inbox
  - what's cooking  # Learned from usage
```

### Preference Adaptation

**Progressive Discovery**:
```
Session 1:
User: "Show inbox status"
Agent: [Shows verbose output]
User: "Too much detail"
Agent: "Got it. Updating preference: verbosity=concise"
       [Updates .chora/user-preferences.yaml]

Session 2:
User: "Show inbox status"
Agent: [Shows concise output automatically]
```

### Expertise Tracking

**Skill Progression**:
```
# Initial state (beginner)
User: "What's a coordination request?"
Agent: [Full explanation + examples]

# After 10 successful coordination request operations
User: "What's a coordination request?"
Agent: [Detects: user has used this 10+ times]
       "You've worked with 10+ coordination requests.
        Want the detailed explanation or just a reminder?"
```

---

## 6. Anti-Patterns (Don't Do This)

### ❌ Anti-Pattern 1: Force Exact Syntax

```
# Bad
User: "show me the inbox"
Agent: "Command not recognized. Did you mean: python scripts/inbox-status.py?"

# Good
User: "show me the inbox"
Agent: [Recognizes intent, executes inbox_status]
       [Shows result]
```

### ❌ Anti-Pattern 2: Explain Instead of Execute

```
# Bad
User: "Create a coordination request for traceability"
Agent: "To create a coordination request, you should:
       1. Create a JSON file in inbox/incoming/coordination/
       2. Use the schema from inbox/schemas/coordination-request.schema.json
       3. Fill in the required fields: title, priority, estimated_effort
       4. Run python scripts/validate-coordination.py to check
       5. Then submit for sprint planning"

# Good
User: "Create a coordination request for traceability"
Agent: ✅ Created coord-007-traceability-pilot.json
       Next: Review and submit for sprint planning?
```

### ❌ Anti-Pattern 3: One-Size-Fits-All Output

```
# Bad (ignores user preferences)
User: "Quick SAP status"
Agent: [Always shows 50-line verbose report]

# Good (adapts to preferences)
User: "Quick SAP status"
Agent: [Checks user_preferences.yaml: verbosity=concise]
       "✅ 12 SAPs installed. 2 at Level 2. Top gap: SAP-004 coverage."
```

### ❌ Anti-Pattern 4: No Context Retention

```
# Bad
User: "Show inbox"
Agent: [Shows 3 coordination requests]
User: "Review the first one"
Agent: "What do you mean by 'the first one'?"

# Good
User: "Show inbox"
Agent: [Shows 3 coordination requests, stores context]
User: "Review the first one"
Agent: [Recognizes referent: coord-003]
       [Displays coord-003 details]
```

### ❌ Anti-Pattern 5: Static Patterns (No Learning)

```
# Bad
# User says "what's pending" 20 times
# Intent router still doesn't recognize it (not in hardcoded list)

# Good
# After 3 successful matches to "inbox_status"
# Pattern added automatically to triggers
# Future recognition: instant
```

---

## 7. Implementation Checklist

### Phase 1: Foundation (Week 1)
- [x] Create intent router (scripts/intent-router.py)
- [x] Create pattern database (INTENT_PATTERNS.yaml)
- [x] Create glossary search (scripts/chora-search.py)
- [x] Create glossary (docs/GLOSSARY.md)
- [x] Create user preferences template
- [x] Create suggestion engine (scripts/suggest-next.py)

### Phase 2: Integration (Week 2)
- [ ] Update AGENTS.md with intent router usage
- [ ] Update CLAUDE.md with preference loading
- [ ] Add user signal patterns to 5 high-traffic SAPs
- [ ] Integrate suggestion engine with inbox protocol
- [ ] Test end-to-end workflow

### Phase 3: Validation (Week 3)
- [ ] Test with 30+ natural language queries
- [ ] Validate preference system across tools
- [ ] Measure intent router accuracy (target: ≥80%)
- [ ] Gather user feedback
- [ ] Iterate based on findings

### Phase 4: Documentation (Week 4)
- [ ] Document bidirectional communication pattern (this guide)
- [ ] Add examples to awareness guides
- [ ] Create video walkthrough
- [ ] Update user-docs with terminology discovery
- [ ] Publish as part of v4.2.0 release

---

## 8. Success Metrics

### Quantitative

- **Intent Recognition Accuracy**: ≥80% on test queries
- **Clarification Rate**: ≤20% (most queries understood first try)
- **Pattern Learning Rate**: +5 learned patterns per week (during active use)
- **User Satisfaction**: ≥85% on ease-of-use survey
- **Time to Competency**: ≤2 hours for new users to perform basic operations

### Qualitative

- Users report feeling "understood" by the system
- Natural language preferred over memorizing commands
- Onboarding friction reduced ("I just asked for what I wanted")
- Meta-systemic thinking supported (exploration → formalization)
- Mutual adaptation evident (system learns user vocabulary)

---

## 9. Future Enhancements

### Short-Term (v4.3.0)
- Multi-turn dialogue with clarification loops
- Voice-to-text integration for hands-free operation
- Visual decision trees (interactive flowcharts)
- Team vocabulary sharing (shared pattern library)

### Medium-Term (v5.0.0)
- ML-based intent classification (beyond pattern matching)
- Personalized onboarding (adaptive learning paths)
- Cross-session context retention (long-term memory)
- Natural language → code generation (advanced)

### Long-Term (v6.0.0)
- Multi-agent coordination (agents collaborate on user behalf)
- Predictive suggestions (anticipate needs before asking)
- Analogical reasoning (explain new concepts via familiar analogies)
- Conversational workflow composition (build workflows through dialogue)

---

## 10. Related Documents

**Core Infrastructure**:
- [Intent Router](../../scripts/intent-router.py) - Natural language → actions
- [Glossary Search](../../scripts/chora-search.py) - Terminology discovery
- [Suggestion Engine](../../scripts/suggest-next.py) - Context-aware recommendations
- [User Preferences](../../.chora/user-preferences.yaml.template) - Adaptive behavior

**Related SAPs**:
- [SAP-001: inbox-coordination](../../skilled-awareness/inbox-coordination/) - Intake system
- [SAP-009: agent-awareness](../../skilled-awareness/agent-awareness/) - AGENTS.md patterns
- [SAP-012: development-lifecycle](../../skilled-awareness/development-lifecycle/) - DDD → BDD → TDD

**Workflows**:
- [DDD Workflow](DDD_WORKFLOW.md) - Documentation Driven Design
- [BDD Workflow](BDD_WORKFLOW.md) - Behavior Driven Development
- [TDD Workflow](TDD_WORKFLOW.md) - Test Driven Development

---

**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-10-31
**Owner**: chora-base core team

**Meta-Note**: This guide itself demonstrates the principle - written conversationally to be accessible, with formal structure emerging progressively through sections.
