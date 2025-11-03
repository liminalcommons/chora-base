# Change Request: COORD-2025-004 Bidirectional Translation Layer Integration

**Trace ID**: coord-2025-004-bidirectional
**Type**: SAP Enhancement (SAP-009 v1.0.0 → v1.1.0)
**Status**: In Progress - DDD Phase
**Priority**: P2 (Medium)
**Sprint**: Sprint 5 (Q1 2026)
**Target Release**: v4.1.3 (PATCH)
**Estimated Effort**: 16-24 hours

---

## Overview

Enhance SAP-009 (agent-awareness) with bidirectional translation layer to enable mutual ergonomics between conversational user input and procedural execution. Foundation tools (intent-router.py, chora-search.py, suggest-next.py) are complete; this change request integrates them into SAP-009 and establishes usage patterns across the ecosystem.

**Key Innovation**: Enable agents to "just know" how to use translation tools as native and second nature through documentation-driven discovery, supporting progressive formalization from casual conversation to systemic ontology fluency.

---

## Context

### Background

User requested exploration of traceability applicability across SAPs, leading to proposal for bidirectional translation layer that enables:
1. **Natural language → Formal actions** via intent routing with confidence scoring
2. **Conversational input → Procedural execution** with progressive formalization
3. **Mutual ergonomics** where system adapts to user style AND user gradually learns systemic ontology

After foundation tools were built, user correctly noted: "lets make sure we are using our process and including governance and administrative doc updates where appropriate." This change request follows proper DDD → BDD → TDD lifecycle per SAP-012.

### Foundation Work Complete (Phase 1)

✅ **scripts/intent-router.py** (470 lines)
- Pattern matching engine: natural language → formal actions
- Confidence scoring: ≥70% execute, 50-70% clarify, <50% alternatives
- Key classes: `IntentMatch`, `IntentPattern`, `IntentRouter`

✅ **scripts/chora-search.py** (380 lines)
- Glossary search with forward/reverse lookup and fuzzy matching
- 75+ terms across 14 categories
- Key classes: `GlossaryEntry`, `GlossarySearch`

✅ **scripts/suggest-next.py** (470 lines)
- Context-aware next action suggestions based on project state
- Reactive (top 5) and proactive (high priority only) modes
- Key classes: `Suggestion`, `ProjectContext`, `SuggestionEngine`

✅ **docs/dev-docs/patterns/INTENT_PATTERNS.yaml** (377 lines)
- 24 intent patterns covering inbox, SAP evaluation, development lifecycle, testing, traceability
- Triggers, parameters, examples, SAP references

✅ **docs/GLOSSARY.md** (640 lines)
- 75+ terms, 14 categories (Intake & Coordination, Development Lifecycle, Testing & Quality, etc.)
- Structure: Term, definition, aliases, related terms, SAP reference, examples

✅ **.chora/user-preferences.yaml.template** (380 lines)
- 100+ configuration options across communication, workflow, learning, expertise, notifications
- Enables user-specific agent behavior adaptation

✅ **docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md** (1,060 lines)
- Complete pattern guide for mutual ergonomics
- Implementation checklist showing Phase 1 complete, Phase 2-4 pending

✅ **AGENTS.md** (+214 lines at 732-944)
- Tool discovery patterns for bidirectional translation layer
- Usage patterns, anti-patterns, integration points

### What This Change Request Addresses

Integration work (Phase 2-4 of BIDIRECTIONAL_COMMUNICATION.md):
- Enhance SAP-009 protocol-spec.md with Section 9: Bidirectional Translation Layer
- Enhance SAP-009 awareness-guide.md with integration patterns for generic agents
- Update 5 domain AGENTS.md files with user signal patterns (SAP-001, 004, 009, 012, 013)
- Integrate suggestion engine with inbox protocol
- Write BDD scenarios and achieve ≥85% test coverage
- Update governance documentation (CHANGELOG, SAP Index, ledger)

---

## Acceptance Criteria (From COORD-2025-004)

### Technical Criteria

1. ✅ **Intent recognition accuracy ≥80%** on test query set (30+ queries)
   - Test patterns: "show inbox" → `run_inbox_status`, "how are saps" → `run_sap_evaluator_quick`
   - Edge cases: ambiguous queries, typos, new variations

2. ✅ **Generic agents can discover tools via documentation alone**
   - Documentation-driven integration (3-layer: root AGENTS.md → domain AGENTS.md → INTENT_PATTERNS.yaml)
   - No auto-loading required; subprocess invocation pattern
   - Works for Claude, Cursor, generic agents, and humans

3. ✅ **Tools gracefully degrade**
   - Missing tool → fall back to documented patterns
   - Partial functionality if some tools unavailable
   - No blocking failures

4. ✅ **User preferences successfully adapt agent behavior** (all 100+ config options)
   - Verbosity: concise|standard|verbose
   - Formality: casual|standard|formal
   - Workflow preferences: require_confirmation, auto_commit, progressive_disclosure
   - Learning: capture_patterns, suggest_improvements, track_usage

5. ✅ **Pattern learning captures new variations without breaking existing patterns**
   - Regression tests validate existing patterns still work
   - New patterns additive, not destructive
   - Manual curation prevents false positives

6. ✅ **Suggestion engine provides context-aware recommendations**
   - Based on project state (inbox status, sprint phase, quality metrics)
   - Reactive mode (top 5 suggestions) and proactive mode (high priority only)

### Quality Criteria

7. ✅ **All BDD scenarios passing**
   - Intent routing scenarios
   - Glossary search scenarios
   - Context analysis scenarios
   - Preference loading scenarios

8. ✅ **Test coverage ≥85%** for integration code

9. ✅ **No lint/type errors**
   - Ruff validation passing
   - mypy type checking passing

10. ✅ **Documentation follows Diátaxis framework**
    - How-to: Task-oriented integration guides
    - Reference: API documentation for tools
    - Explanation: Mutual ergonomics concepts

### Governance Criteria

11. ✅ **SAP-009 enhancement properly versioned** (v1.0.0 → v1.1.0)
    - capability-charter.md version updated
    - ledger.md release date and changes documented
    - protocol-spec.md Section 9 added

12. ✅ **CHANGELOG follows semantic versioning** (v4.1.2 → v4.1.3 PATCH release)
    - Added: Bidirectional translation layer
    - Changed: SAP-009 enhanced to v1.1.0

---

## Implementation Plan

### Phase 2: DDD - Documentation Driven Design (2-3 hours) ← CURRENT PHASE

**Objective**: Define contracts for bidirectional translation layer integration

#### Task 2.1: Create This Change Request (1.5 hours)

**Status**: ✅ IN PROGRESS

**Deliverable**: This document (change-request.md)

**Content**:
- Overview and context
- Acceptance criteria (12 total from coordination request)
- Implementation plan (8 phases)
- Technical specifications for SAP-009 enhancements
- Integration contracts

#### Task 2.2: Technical Lead Review (0.5 hours)

**Status**: PENDING

**Process**:
1. Review change request for completeness
2. Validate contracts against SAP-009 v1.0.0
3. Approve or request adjustments
4. Document approval in change request

**Approval Criteria**:
- [ ] All 12 acceptance criteria addressable
- [ ] Contracts well-defined for intent router, glossary search, suggestion engine
- [ ] Integration points with existing SAP-009 patterns clear
- [ ] Effort estimate realistic (16-24 hours)
- [ ] No breaking changes to SAP-009 v1.0.0

**Phase 2 Exit Criteria**:
- [ ] Change request approved by technical lead
- [ ] phase_completed event emitted for DDD phase

---

### Phase 3: BDD - Behavior Driven Development (1.5 hours)

**Objective**: Define expected behaviors via Gherkin scenarios before implementation

#### Task 3.1: Write Gherkin Scenarios (1 hour)

**File**: `features/bidirectional-integration.feature`

**Scenarios to Document**:

1. **Intent Recognition - Exact Match**
   ```gherkin
   Scenario: User requests inbox status with exact phrase
     Given the intent router is initialized
     When user input is "show inbox"
     Then intent should be "run_inbox_status"
     And confidence should be >= 0.70
     And clarification should be empty
   ```

2. **Intent Recognition - Variation**
   ```gherkin
   Scenario: User requests inbox status with variation
     Given the intent router is initialized
     When user input is "what's in the inbox?"
     Then intent should be "run_inbox_status"
     And confidence should be >= 0.70
   ```

3. **Intent Recognition - Ambiguous**
   ```gherkin
   Scenario: User input is ambiguous
     Given the intent router is initialized
     When user input is "check status"
     Then confidence should be between 0.50 and 0.70
     And clarification should contain "Did you mean"
     And alternatives should include at least 2 options
   ```

4. **Glossary Search - Exact Match**
   ```gherkin
   Scenario: Search for exact term
     Given the glossary is loaded
     When searching for "Coordination Request"
     Then should return 1 result
     And result score should be 1.0
     And result definition should contain "Type 2 intake"
   ```

5. **Glossary Search - Fuzzy Match**
   ```gherkin
   Scenario: Search with typo
     Given the glossary is loaded
     When searching for "coordnation" with fuzzy matching
     Then should return at least 1 result
     And top result should be "Coordination Request"
     And result score should be >= 0.60
   ```

6. **Context-Aware Suggestions - Inbox**
   ```gherkin
   Scenario: Suggest next action when inbox has pending items
     Given the suggestion engine is initialized
     And inbox has 3 pending coordination requests
     When requesting suggestions in "reactive" mode
     Then top suggestion should be "Review pending coordination requests"
     And priority should be "high"
   ```

7. **Preference Adaptation - Verbosity**
   ```gherkin
   Scenario: Agent adapts to verbose preference
     Given user preferences set verbosity to "verbose"
     When agent responds to query
     Then response should include detailed explanations
     And response should include examples
     And response length should be > 100 words
   ```

8. **Graceful Degradation - Missing Tool**
   ```gherkin
   Scenario: Intent router not available
     Given intent-router.py is not executable
     When user input is "show inbox"
     Then should fall back to pattern matching in INTENT_PATTERNS.yaml
     And should return valid intent
     And should log warning about missing tool
   ```

**Deliverable**: features/bidirectional-integration.feature (~200-300 lines)

#### Task 3.2: Implement Step Definitions (0.5 hours)

**File**: `features/steps/bidirectional_steps.py`

**Step Definitions Needed**:
```python
@given('the intent router is initialized')
def step_impl(context):
    from scripts.intent_router import IntentRouter
    context.router = IntentRouter()

@when('user input is "{text}"')
def step_impl(context, text):
    context.matches = context.router.route(text)

@then('intent should be "{action}"')
def step_impl(context, action):
    assert context.matches[0].action == action

@then('confidence should be >= {threshold:f}')
def step_impl(context, threshold):
    assert context.matches[0].confidence >= threshold
```

**Deliverable**: features/steps/bidirectional_steps.py (~300-400 lines)

**Phase 3 Exit Criteria**:
- [ ] All 8+ Gherkin scenarios written
- [ ] Step definitions implemented
- [ ] All scenarios RED (failing, as expected before implementation)
- [ ] phase_completed event emitted for BDD phase

---

### Phase 4: TDD - SAP-009 Enhancement Implementation (8-12 hours)

**Objective**: Make BDD scenarios GREEN via SAP-009 integration

#### Task 4.1: Enhance SAP-009 protocol-spec.md (2-3 hours)

**File**: `docs/skilled-awareness/agent-awareness/protocol-spec.md`

**Changes**: Add Section 9 after current Section 8

**New Section 9: Bidirectional Translation Layer**

```markdown
## 9. Bidirectional Translation Layer

**Purpose**: Enable mutual ergonomics between conversational input and procedural execution through progressive formalization.

### 9.1 Overview

The bidirectional translation layer provides three core capabilities:

1. **Intent Routing**: Natural language → Formal actions (scripts/intent-router.py)
2. **Glossary Search**: Term discovery and ontology learning (scripts/chora-search.py)
3. **Context Analysis**: Situation-aware next action suggestions (scripts/suggest-next.py)

**Key Principle**: Tools are TRANSLATION aids, not AUTOMATION. LLM intelligence remains primary for generation, reasoning, and design tasks.

### 9.2 Intent Router Contract

**Script**: `scripts/intent-router.py`

**Input**: Natural language user input (string)

**Output**: List of IntentMatch objects, sorted by confidence descending

**IntentMatch Structure**:
- `action` (str): Formal action identifier (e.g., "run_inbox_status")
- `confidence` (float): Match confidence 0.0-1.0
- `parameters` (dict): Extracted parameters from input
- `pattern_id` (str): Matching pattern identifier
- `clarification` (str|None): Clarification question if ambiguous

**Confidence Thresholds**:
- ≥0.70: Execute action automatically
- 0.50-0.70: Request clarification from user
- <0.50: Offer alternatives

**Usage Pattern**:
```python
from scripts.intent_router import IntentRouter

router = IntentRouter()
matches = router.route("show inbox")

if matches[0].confidence >= 0.70:
    execute_action(matches[0].action, matches[0].parameters)
elif matches[0].confidence >= 0.50:
    ask_clarification(matches[0].clarification, matches[0].alternatives)
else:
    suggest_alternatives(matches[:3])
```

**Pattern Database**: docs/dev-docs/patterns/INTENT_PATTERNS.yaml (24+ patterns)

**Graceful Degradation**: If script not available, fall back to pattern matching in INTENT_PATTERNS.yaml

### 9.3 Glossary Search Contract

**Script**: `scripts/chora-search.py`

**Input**: Search query (string), optional fuzzy flag (bool)

**Output**: List of (GlossaryEntry, relevance_score) tuples

**GlossaryEntry Structure**:
- `term` (str): Canonical term
- `definition` (str): Term definition
- `category` (str): Category (e.g., "Intake & Coordination")
- `aliases` (list[str]): Alternative names
- `related` (list[str]): Related terms
- `sap_reference` (str|None): Related SAP ID
- `examples` (list[str]): Usage examples

**Search Modes**:
1. **Exact match** (score 1.0): Query == term (case-insensitive)
2. **Contains** (score 0.8): Query substring of term
3. **Fuzzy match** (score 0.4-0.7): Similarity ≥60% via SequenceMatcher

**Usage Pattern**:
```python
from scripts.chora_search import GlossarySearch

glossary = GlossarySearch()
results = glossary.search("coordination", fuzzy=True)

for entry, score in results[:3]:
    print(f"{entry.term} (relevance: {score:.2f})")
    print(f"  Definition: {entry.definition}")
    print(f"  SAP: {entry.sap_reference}")
```

**Additional Methods**:
- `reverse_search(definition_fragment)`: Find term by definition content
- `get_related(term)`: Get related terms for exploration
- `by_category(category)`: Get all terms in category
- `by_sap(sap_id)`: Get all terms related to SAP

**Graceful Degradation**: If script not available, direct users to docs/GLOSSARY.md

### 9.4 Suggestion Engine Contract

**Script**: `scripts/suggest-next.py`

**Input**: Project context (current state), mode ("reactive" | "proactive")

**Output**: List of Suggestion objects, sorted by priority

**Suggestion Structure**:
- `action` (str): Suggested action description
- `rationale` (str): Why this suggestion makes sense
- `priority` (str): "high" | "medium" | "low"
- `category` (str): "workflow" | "quality" | "planning" | "learning"
- `estimated_effort` (str): Time estimate (e.g., "5-10 minutes")

**Suggestion Modes**:
- **Reactive**: Return top 5 suggestions across all priorities
- **Proactive**: Return only high-priority suggestions (user didn't ask, but should know)

**Context Sources**:
- Inbox status (pending coordination requests, active tasks)
- Sprint phase (planning, development, testing, review)
- Quality metrics (test coverage, broken links, lint errors)
- Documentation state (missing files, outdated content)

**Usage Pattern**:
```python
from scripts.suggest_next import SuggestionEngine, ProjectContext

context = ProjectContext.from_current_directory()
engine = SuggestionEngine(context)
suggestions = engine.suggest(mode="reactive")

for suggestion in suggestions:
    print(f"[{suggestion.priority}] {suggestion.action}")
    print(f"  Why: {suggestion.rationale}")
    print(f"  Effort: {suggestion.estimated_effort}")
```

**Integration Points**:
- Inbox protocol (SAP-001): Suggest reviewing pending requests
- Development lifecycle (SAP-012): Suggest next phase based on current state
- Testing framework (SAP-004): Suggest improving coverage if <85%
- Documentation framework (SAP-007): Suggest fixing broken links

**Graceful Degradation**: If script not available, agents rely on documented workflows

### 9.5 User Preferences Contract

**Configuration File**: `.chora/user-preferences.yaml`

**Template**: `.chora/user-preferences.yaml.template` (100+ options)

**Purpose**: Enable user-specific agent behavior adaptation

**Configuration Categories**:

1. **Communication** (verbosity, formality, output_format)
   ```yaml
   communication:
     verbosity: standard  # concise|standard|verbose
     formality: standard  # casual|standard|formal
     output_format: terminal  # terminal|markdown|json
   ```

2. **Workflow** (confirmation, automation, disclosure)
   ```yaml
   workflow:
     require_confirmation: destructive  # always|destructive|never
     auto_commit: false
     progressive_disclosure: true
   ```

3. **Learning** (pattern capture, suggestions, usage tracking)
   ```yaml
   learning:
     capture_patterns: true
     suggest_improvements: true
     track_usage: true
   ```

4. **Expertise** (assume_knowledge, explain_rationale, show_alternatives)
   ```yaml
   expertise:
     assume_knowledge: intermediate  # beginner|intermediate|expert
     explain_rationale: true
     show_alternatives: true
   ```

**Usage Pattern**:
```python
import yaml

with open('.chora/user-preferences.yaml') as f:
    prefs = yaml.safe_load(f)

if prefs['communication']['verbosity'] == 'verbose':
    response += detailed_explanation()
    response += examples()

if prefs['workflow']['require_confirmation'] == 'always':
    confirm_before_action()
```

**Graceful Degradation**: If preferences file missing, use defaults from template

### 9.6 Integration with Existing SAP-009 Patterns

**Bidirectional translation layer EXTENDS, not replaces, existing patterns**:

1. **AGENTS.md/CLAUDE.md dual-file pattern** (Section 3)
   - Bidirectional tools discoverable via root AGENTS.md
   - Domain-specific user signals in nested AGENTS.md files
   - Progressive context loading remains primary mechanism

2. **"Nearest File Wins"** (Section 4)
   - Domain AGENTS.md files can override root intent patterns
   - Allows domain-specific translations (e.g., testing → pytest-specific actions)

3. **Progressive Context Loading** (Section 5)
   - Phase 1 (Always Load): Root AGENTS.md includes tool discovery
   - Phase 2 (Load on Demand): Domain AGENTS.md includes user signal patterns
   - Phase 3 (Complex Only): Full pattern database (INTENT_PATTERNS.yaml)

4. **Token Budgeting** (Section 6)
   - Intent router: ~5-10k tokens (patterns + script)
   - Glossary search: ~15-20k tokens (all terms)
   - Suggestion engine: ~10-15k tokens (context analysis)
   - Total: ~30-45k tokens (within 200k budget)

### 9.7 Anti-Patterns

**DO NOT**:
1. Auto-load tools without documentation discovery (breaks generic agent compatibility)
2. Automate LLM-intelligent tasks (generation, reasoning, design remain LLM primary)
3. Auto-add patterns without review (manual curation maintains quality)
4. Use tools as replacement for understanding systemic ontology (progressive formalization is goal)

**DO**:
1. Document tool discovery in AGENTS.md (3-layer: root → domain → patterns)
2. Use tools for translation (natural language → formal actions)
3. Gracefully degrade when tools unavailable (documented pattern fallback)
4. Encourage progressive formalization (casual → semi-formal → formal → executable)

### 9.8 User Signal Patterns (Domain AGENTS.md Integration)

**Purpose**: Map conversational input to domain-specific formal actions

**Pattern**:
Each domain AGENTS.md file includes a "User Signal Patterns" section:

```markdown
## User Signal Patterns

### Inbox Operations (SAP-001)

| User Says | Formal Action | Notes |
|-----------|---------------|-------|
| "show inbox" | run_inbox_status | Display dashboard |
| "what's pending" | list_pending_coordination_requests | Filter by status |
| "review coord-NNN" | open_coordination_request(id="coord-NNN") | Load specific request |

### Testing Operations (SAP-004)

| User Says | Formal Action | Notes |
|-----------|---------------|-------|
| "run tests" | pytest_run() | Full test suite |
| "check coverage" | pytest_coverage_report() | Generate coverage report |
| "fix test X" | edit_test_file(name="X") | Open test in editor |
```

**Domain AGENTS.md Files to Update** (Phase 4, Task 4.3):
1. docs/skilled-awareness/inbox-protocol/AGENTS.md (SAP-001)
2. docs/skilled-awareness/testing-framework/AGENTS.md (SAP-004)
3. docs/skilled-awareness/agent-awareness/AGENTS.md (SAP-009)
4. docs/skilled-awareness/development-lifecycle/AGENTS.md (SAP-012)
5. docs/skilled-awareness/metrics-framework/AGENTS.md (SAP-013)

### 9.9 Quality Gates

**Intent Recognition**:
- Accuracy ≥80% on test query set (30+ queries)
- Handles typos and variations
- Provides clear alternatives when ambiguous

**Glossary Search**:
- Exact match returns top result with score 1.0
- Fuzzy matching handles typos (≥60% similarity)
- Related terms discoverable via `get_related()`

**Suggestion Engine**:
- Context-aware recommendations relevant to project state
- Reactive mode returns top 5, proactive only high priority
- Estimated effort accurate ±50%

**Test Coverage**: ≥85% for integration code

### 9.10 Versioning

- SAP-009 v1.0.0: AGENTS.md/CLAUDE.md dual-file pattern, progressive loading
- **SAP-009 v1.1.0**: Bidirectional translation layer (THIS ENHANCEMENT)
- Future: v1.2.0 could add voice-to-text translation, visual workflow builder

**Migration**: v1.0.0 → v1.1.0 is backward compatible (additive only, no breaking changes)
```

**Deliverable**: protocol-spec.md enhanced with Section 9 (~400-600 lines added)

**Exit Criteria**:
- [ ] Section 9 complete and follows SAP-009 contract style
- [ ] All 3 tool contracts defined (intent, glossary, suggestions)
- [ ] Integration points with existing sections clear
- [ ] Quality gates specified

#### Task 4.2: Enhance SAP-009 awareness-guide.md (2-3 hours)

**File**: `docs/skilled-awareness/agent-awareness/awareness-guide.md`

**Changes**: Add new section on bidirectional translation layer integration

**New Content**:

```markdown
## Integrating Bidirectional Translation Layer

**For**: Generic agents (Claude, Cursor, etc.) and humans

**Purpose**: Enable conversational interaction while executing procedurally

### Discovery Workflow (3-Layer Progressive)

**Layer 1: Root AGENTS.md**
1. Agent loads root AGENTS.md (always Phase 1)
2. Discovers "Bidirectional Translation Layer" section (lines 732-944)
3. Learns 4 tools exist: intent-router, chora-search, suggest-next, user-preferences
4. Sees common patterns:
   - "show inbox" → `run_inbox_status`
   - "how are saps" → `run_sap_evaluator_quick`
   - "search for 'coordination'" → `chora_search("coordination")`

**Layer 2: Domain AGENTS.md**
1. Agent navigates to domain (e.g., skilled-awareness/inbox-protocol/)
2. Loads domain AGENTS.md (Phase 2)
3. Discovers domain-specific user signal patterns
4. Sees domain mappings:
   - "what's pending" → `list_pending_coordination_requests`
   - "review coord-005" → `open_coordination_request(id="coord-005")`

**Layer 3: Pattern Database**
1. For complex/ambiguous queries, agent loads INTENT_PATTERNS.yaml
2. Sees all 24+ patterns with triggers, parameters, examples
3. Uses pattern matching for edge cases

**Token Budget**: Layer 1 (~10k) + Layer 2 (~5k) + Layer 3 (~20k if needed) = 15-35k tokens

### Usage Examples

#### Example 1: Inbox Status Query

**User Input** (conversational):
```
show me what's in the inbox
```

**Agent Discovery Flow**:
1. Loads root AGENTS.md
2. Finds pattern: "show inbox" → `run_inbox_status`
3. Recognizes variation: "show me what's in the inbox" ≈ "show inbox"
4. Executes: Reads inbox/coordination/ECOSYSTEM_STATUS.yaml and formats output

**Alternative** (if tools available):
1. Calls `python scripts/intent-router.py "show me what's in the inbox"`
2. Receives: `IntentMatch(action="run_inbox_status", confidence=0.85, ...)`
3. Executes action based on high confidence

#### Example 2: Term Discovery

**User Input** (conversational):
```
what's a coordination request?
```

**Agent Discovery Flow**:
1. Recognizes glossary query pattern
2. Checks if chora-search.py available:
   - **If yes**: Calls `python scripts/chora-search.py "coordination request"`
   - **If no**: Reads docs/GLOSSARY.md and searches manually
3. Returns definition:
   ```
   **Coordination Request** (Type 2 Intake)
   Cross-repo coordination request reviewed during sprint planning (every 2 weeks).

   **Related**: Strategic Proposal, Implementation Task
   **SAP**: SAP-001 (inbox-protocol)
   **File**: inbox/incoming/coordination/
   ```

#### Example 3: Context-Aware Suggestions

**User Input** (conversational):
```
what should i work on next?
```

**Agent Discovery Flow**:
1. Recognizes suggestion query pattern
2. Checks if suggest-next.py available:
   - **If yes**: Calls `python scripts/suggest-next.py --mode=reactive`
   - **If no**: Manually analyzes project state (inbox, sprint phase, quality)
3. Returns top 5 suggestions:
   ```
   [high] Review pending coordination requests (COORD-2025-004)
     Why: 1 coordination request pending triage
     Effort: 30-60 minutes

   [medium] Improve test coverage in scripts/
     Why: Current coverage 78%, target 85%
     Effort: 2-3 hours

   [medium] Update SAP-009 documentation
     Why: v1.1.0 enhancement in progress
     Effort: 1-2 hours
   ```

### Integration Patterns for Generic Agents

#### Pattern 1: Subprocess Invocation (Recommended)

**Why**: Works for any agent (Claude, Cursor, humans), doesn't require auto-loading

**How**:
```python
import subprocess
import json

# Intent routing
result = subprocess.run(
    ['python', 'scripts/intent-router.py', user_input],
    capture_output=True,
    text=True
)
matches = json.loads(result.stdout)

# Glossary search
result = subprocess.run(
    ['python', 'scripts/chora-search.py', query, '--fuzzy'],
    capture_output=True,
    text=True
)
results = json.loads(result.stdout)
```

**Graceful Degradation**:
```python
try:
    result = subprocess.run(['python', 'scripts/intent-router.py', user_input], ...)
except FileNotFoundError:
    # Fallback: Use pattern matching from INTENT_PATTERNS.yaml
    matches = fallback_pattern_match(user_input)
```

#### Pattern 2: Direct Import (Advanced, Claude Code only)

**Why**: Faster, type-safe, IDE support

**How**:
```python
from scripts.intent_router import IntentRouter
from scripts.chora_search import GlossarySearch

router = IntentRouter()
matches = router.route(user_input)

glossary = GlossarySearch()
results = glossary.search(query, fuzzy=True)
```

**Note**: Only works if agent has Python environment access (Claude Code yes, generic agents no)

### Progressive Formalization Journey

**Goal**: User gradually learns systemic ontology while system adapts to user style

**Stage 1: Casual (Week 1)**
```
User: "show me the inbox"
Agent: *executes run_inbox_status via intent routing*
```

**Stage 2: Semi-Formal (Week 2-4)**
```
User: "check coordination requests"
Agent: *recognizes "coordination request" as formal term, shows definition*
User: "ok, show pending coordination requests"
Agent: *executes list_pending_coordination_requests*
```

**Stage 3: Formal (Month 2+)**
```
User: "run_inbox_status"
Agent: *executes directly, no translation needed*
User: "create coordination request for SAP-009 enhancement"
Agent: *uses formal template, user knows schema*
```

**Stage 4: Executable (Month 3+)**
```
User provides JSON directly:
{
  "type": "coordination",
  "request_id": "COORD-2025-005",
  "title": "Next enhancement",
  ...
}
Agent: *validates schema, creates request*
```

**Key**: User moves at their own pace; system supports all stages simultaneously

### Maintenance

**Adding New Patterns**:
1. Edit docs/dev-docs/patterns/INTENT_PATTERNS.yaml
2. Add pattern with triggers, action, parameters, examples
3. Test with intent-router.py
4. Update domain AGENTS.md if domain-specific

**Adding New Terms**:
1. Edit docs/GLOSSARY.md
2. Add term with definition, category, aliases, related, SAP reference, examples
3. Test with chora-search.py
4. Update SAP documentation to reference term

**Updating Suggestion Logic**:
1. Edit scripts/suggest-next.py
2. Add new suggestion category or context source
3. Test with current project state
4. Document new suggestion types in awareness-guide.md
```

**Deliverable**: awareness-guide.md enhanced with integration section (~300-500 lines added)

**Exit Criteria**:
- [ ] Discovery workflow documented (3-layer progressive)
- [ ] Usage examples cover all 3 tools
- [ ] Integration patterns for generic agents specified
- [ ] Progressive formalization journey explained
- [ ] Maintenance procedures documented

#### Task 4.3: Update 5 Domain AGENTS.md Files (3-4 hours)

**Objective**: Add user signal patterns to domain AGENTS.md files

**Files to Update**:

1. **docs/skilled-awareness/inbox-protocol/AGENTS.md** (SAP-001)

Add section:
```markdown
## User Signal Patterns

### Inbox Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "show inbox" | run_inbox_status | Read ECOSYSTEM_STATUS.yaml | Display dashboard |
| "what's pending" | list_pending_coordination_requests | Filter by status: pending_triage | Count by priority |
| "review coord-NNN" | open_coordination_request(id) | Read incoming/coordination/COORD-NNN.json | Load specific request |
| "create coordination request" | create_coordination_request() | Use coordination-request.schema.json | Type 2 intake |
| "triage inbox" | run_sprint_planning_triage | Process pending_triage items | Bi-weekly |
| "what's blocking" | list_blockers | Filter ECOSYSTEM_STATUS.yaml by blockers field | Cross-repo dependencies |
| "archive coord-NNN" | archive_completed_request(id) | Move incoming/ → archived/ | After fulfillment complete |

### Common Variations

- "inbox status" / "check inbox" / "what's in the queue" → run_inbox_status
- "pending items" / "what needs review" / "coordination queue" → list_pending_coordination_requests
- "block" / "blocker" / "what's blocked" → list_blockers
```

2. **docs/skilled-awareness/testing-framework/AGENTS.md** (SAP-004)

Add section:
```markdown
## User Signal Patterns

### Testing Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "run tests" | pytest_run() | pytest | Full test suite |
| "check coverage" | pytest_coverage_report() | pytest --cov | Target: ≥85% |
| "run tests for FILE" | pytest_run_file(path) | pytest PATH | Single file |
| "fix failing test" | identify_and_fix_test() | pytest -v, read failure | Debug workflow |
| "add test for FUNCTION" | create_test_function() | Edit test file, follow patterns | Use fixtures |
| "update fixtures" | edit_conftest() | Edit conftest.py | Shared test setup |

### Coverage Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "coverage below 85" | identify_untested_code() | pytest --cov --cov-report=term-missing | Show gaps |
| "improve coverage" | add_tests_for_gaps() | Target uncovered lines | Prioritize critical paths |
| "coverage report" | generate_coverage_html() | pytest --cov --cov-report=html | Open htmlcov/index.html |

### Common Variations

- "test" / "run pytest" / "execute tests" → pytest_run()
- "coverage" / "check how much is tested" / "coverage stats" → pytest_coverage_report()
```

3. **docs/skilled-awareness/agent-awareness/AGENTS.md** (SAP-009)

Add section:
```markdown
## User Signal Patterns

### Agent Awareness Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "how do agents discover this" | show_agents_md_pattern() | Read AGENTS.md, explain progressive loading | 3-phase context |
| "update AGENTS.md" | edit_agents_md() | Edit nearest AGENTS.md | Nearest file wins |
| "add user signal" | add_user_signal_pattern() | Edit domain AGENTS.md | This section! |
| "search term" | glossary_search(term) | scripts/chora-search.py TERM | 75+ terms |
| "what does X mean" | glossary_lookup(term) | Search GLOSSARY.md | Definition + examples |
| "suggest next action" | context_aware_suggestions() | scripts/suggest-next.py | Reactive mode |

### Bidirectional Translation

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "translate input" | route_intent(input) | scripts/intent-router.py INPUT | Confidence scoring |
| "find pattern for X" | lookup_intent_pattern(action) | Read INTENT_PATTERNS.yaml | 24+ patterns |
| "add intent pattern" | create_intent_pattern() | Edit INTENT_PATTERNS.yaml | Include triggers, examples |
| "user preferences" | load_user_preferences() | Read .chora/user-preferences.yaml | 100+ options |

### Common Variations

- "how does this work for agents" / "agent documentation" → show_agents_md_pattern()
- "define X" / "explain X" / "what is X" → glossary_lookup(term)
- "what should I do next" / "recommend next step" → context_aware_suggestions()
```

4. **docs/skilled-awareness/development-lifecycle/AGENTS.md** (SAP-012)

Add section:
```markdown
## User Signal Patterns

### Development Lifecycle Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "start DDD phase" | begin_ddd_phase() | Create change-request.md | Phase 3 |
| "write BDD scenarios" | create_gherkin_scenarios() | Edit features/*.feature | Phase 4 |
| "run TDD cycle" | execute_red_green_refactor() | Write test → Fail → Implement → Pass → Refactor | Phase 5 |
| "check quality gates" | validate_quality_gates() | Coverage, lint, type check | After each phase |
| "create sprint plan" | create_sprint_plan() | Use SPRINT_PLAN_TEMPLATE.md | Phase 2 |
| "what phase am I in" | identify_current_phase() | Check sprint plan, task status | 8 phases total |

### Quality Gate Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "validate phase N" | check_phase_exit_criteria(N) | Review phase checklist | Before proceeding |
| "emit phase event" | log_phase_completion(N) | Append to events.jsonl | Traceability |
| "check coverage" | validate_coverage_gate() | pytest --cov ≥85% | Quality gate |
| "run lint" | validate_lint_gate() | ruff check | 0 errors required |

### Common Variations

- "documentation driven design" / "DDD" / "create spec" → begin_ddd_phase()
- "behavior driven" / "BDD" / "gherkin" → create_gherkin_scenarios()
- "test driven" / "TDD" / "red green refactor" → execute_red_green_refactor()
```

5. **docs/skilled-awareness/metrics-framework/AGENTS.md** (SAP-013)

Add section:
```markdown
## User Signal Patterns

### Metrics Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "calculate ROI" | run_claude_roi_calculator() | python utils/claude_metrics.py | Cost vs. savings |
| "sprint velocity" | calculate_sprint_velocity() | Hours actual / hours estimated | Target: 80-120% |
| "quality metrics" | generate_quality_dashboard() | Defects, coverage, lint | Research-backed targets |
| "process adherence" | check_process_compliance() | % following SAP-012 lifecycle | Target: ≥80% |
| "show metrics" | display_metrics_dashboard() | Read PROCESS_METRICS.md | All metrics |

### ROI Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "what's the cost" | calculate_claude_cost() | Tokens × rate | Claude pricing |
| "time saved" | calculate_time_savings() | Manual hours - actual hours | Efficiency gain |
| "worth it?" | calculate_roi_percentage() | (Savings - Cost) / Cost × 100 | Target: >100% |

### Common Variations

- "ROI" / "return on investment" / "is this worth it" → run_claude_roi_calculator()
- "velocity" / "how fast are we going" / "sprint speed" → calculate_sprint_velocity()
- "quality" / "are we doing well" / "metrics dashboard" → generate_quality_dashboard()
```

**Deliverable**: 5 AGENTS.md files enhanced with user signal patterns (~100-150 lines each, 500-750 total)

**Exit Criteria**:
- [ ] All 5 domain AGENTS.md files updated
- [ ] User signal patterns cover common conversational inputs
- [ ] Formal actions clearly mapped
- [ ] Tool/command references accurate
- [ ] Common variations documented

#### Task 4.4: Integrate Suggestion Engine with Inbox Protocol (1-2 hours)

**Objective**: Make suggestion engine inbox-aware for proactive recommendations

**File**: `scripts/suggest-next.py`

**Changes**:

1. **Add inbox status detection**:
```python
def _check_inbox_status(self) -> dict:
    """Read ECOSYSTEM_STATUS.yaml and extract inbox metrics."""
    try:
        with open('inbox/coordination/ECOSYSTEM_STATUS.yaml') as f:
            status = yaml.safe_load(f)

        pending = []
        for repo in status.get('repositories', {}).values():
            for item in repo.get('active_work', []):
                if item.get('status') == 'pending_triage':
                    pending.append(item)

        return {
            'pending_count': len(pending),
            'pending_items': pending,
            'blockers': self._extract_blockers(status)
        }
    except FileNotFoundError:
        return {'pending_count': 0, 'pending_items': [], 'blockers': []}
```

2. **Add inbox-aware suggestions**:
```python
def _suggest_inbox_actions(self) -> list[Suggestion]:
    """Suggest inbox-related actions based on current state."""
    suggestions = []
    inbox = self._check_inbox_status()

    if inbox['pending_count'] > 0:
        suggestions.append(Suggestion(
            action=f"Review {inbox['pending_count']} pending coordination request(s)",
            rationale="Items awaiting triage in sprint planning",
            priority="high" if inbox['pending_count'] > 2 else "medium",
            category="workflow",
            estimated_effort="30-60 minutes"
        ))

    if inbox['blockers']:
        suggestions.append(Suggestion(
            action=f"Resolve {len(inbox['blockers'])} blocker(s)",
            rationale="Work blocked by dependencies",
            priority="high",
            category="workflow",
            estimated_effort="Varies by blocker"
        ))

    return suggestions
```

3. **Integrate with main suggest() method**:
```python
def suggest(self, mode: str = "reactive") -> list[Suggestion]:
    """Generate suggestions based on project state."""
    suggestions = []

    # Add inbox suggestions
    suggestions.extend(self._suggest_inbox_actions())

    # Existing suggestion types
    suggestions.extend(self._suggest_workflow())
    suggestions.extend(self._suggest_quality())
    suggestions.extend(self._suggest_planning())
    suggestions.extend(self._suggest_learning())

    # Filter by mode
    if mode == "proactive":
        suggestions = [s for s in suggestions if s.priority == "high"]
    elif mode == "reactive":
        suggestions = suggestions[:5]

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda s: priority_order.get(s.priority, 3))

    return suggestions
```

**Testing**:
```python
# Test with pending coordination requests
def test_suggest_inbox_pending():
    # Setup: Create test ECOSYSTEM_STATUS.yaml with 3 pending items
    context = ProjectContext.from_current_directory()
    engine = SuggestionEngine(context)
    suggestions = engine.suggest(mode="reactive")

    # Assert: Top suggestion should be "Review 3 pending coordination request(s)"
    assert suggestions[0].action.startswith("Review 3 pending")
    assert suggestions[0].priority == "high"
```

**Deliverable**: suggest-next.py enhanced with inbox integration (~50-100 lines added)

**Exit Criteria**:
- [ ] Inbox status detection working
- [ ] Inbox-aware suggestions generated
- [ ] Integration with main suggest() method complete
- [ ] Tests passing for inbox suggestions

**Phase 4 Exit Criteria**:
- [ ] SAP-009 protocol-spec.md Section 9 complete
- [ ] SAP-009 awareness-guide.md integration section complete
- [ ] 5 domain AGENTS.md files updated with user signal patterns
- [ ] Suggestion engine inbox-integrated
- [ ] All BDD scenarios GREEN (passing)
- [ ] Test coverage ≥85%
- [ ] phase_completed event emitted for TDD phase

---

### Phase 5: Testing & Quality Gates (4-6 hours)

**Objective**: Validate integration quality and accuracy

#### Task 5.1: Intent Recognition Accuracy Testing (2 hours)

**Test Suite**: `tests/test_intent_recognition_accuracy.py`

**Test Queries** (30+ variations):

**Exact Matches** (10 queries):
- "show inbox" → run_inbox_status
- "what's pending" → list_pending_coordination_requests
- "run tests" → pytest_run
- "check coverage" → pytest_coverage_report
- "calculate ROI" → run_claude_roi_calculator
- "create coordination request" → create_coordination_request
- "start DDD phase" → begin_ddd_phase
- "write BDD scenarios" → create_gherkin_scenarios
- "run TDD cycle" → execute_red_green_refactor
- "validate quality gates" → validate_quality_gates

**Variations** (10 queries):
- "what's in the inbox" → run_inbox_status
- "check coordination requests" → list_pending_coordination_requests
- "execute tests" → pytest_run
- "how's our coverage" → pytest_coverage_report
- "is this worth it" → run_claude_roi_calculator
- "new coordination request" → create_coordination_request
- "documentation driven design" → begin_ddd_phase
- "gherkin scenarios" → create_gherkin_scenarios
- "red green refactor" → execute_red_green_refactor
- "check quality" → validate_quality_gates

**Typos** (5 queries):
- "shwo inbox" → run_inbox_status (fuzzy match)
- "chek coverage" → pytest_coverage_report
- "coordnation request" → create_coordination_request
- "validte quality" → validate_quality_gates
- "pytest run" → pytest_run (exact match despite being procedural)

**Ambiguous** (5 queries):
- "check status" → clarification needed (inbox status? test status? SAP status?)
- "review" → clarification needed (review what? coordination request? code? documentation?)
- "validate" → clarification needed (validate what? quality gates? coverage? lint?)
- "run" → clarification needed (run what? tests? scripts? workflows?)
- "show" → clarification needed (show what? inbox? metrics? SAPs?)

**Test Implementation**:
```python
def test_intent_recognition_accuracy():
    router = IntentRouter()

    test_cases = [
        ("show inbox", "run_inbox_status", 1.0),  # Exact
        ("what's in the inbox", "run_inbox_status", 0.85),  # Variation
        ("shwo inbox", "run_inbox_status", 0.70),  # Typo
        ("check status", None, 0.60),  # Ambiguous
    ]

    results = []
    for user_input, expected_action, min_confidence in test_cases:
        matches = router.route(user_input)

        if expected_action is None:
            # Ambiguous case: should request clarification
            assert matches[0].confidence < 0.70
            assert matches[0].clarification is not None
            results.append(True)
        else:
            # Should match expected action with sufficient confidence
            assert matches[0].action == expected_action
            assert matches[0].confidence >= min_confidence
            results.append(matches[0].confidence >= 0.80)

    # Calculate accuracy
    accuracy = sum(results) / len(results)
    assert accuracy >= 0.80, f"Accuracy {accuracy:.2%} below 80% threshold"
```

**Acceptance**: ≥80% accuracy on all 30+ queries

**Deliverable**: Accuracy report showing per-query results and overall accuracy

#### Task 5.2: Preference Adaptation Testing (1 hour)

**Test Suite**: `tests/test_preference_adaptation.py`

**Test Categories**:

1. **Verbosity Adaptation** (3 levels):
   - Concise: <50 words, minimal explanation
   - Standard: 50-150 words, balanced
   - Verbose: >150 words, detailed with examples

2. **Formality Adaptation** (3 levels):
   - Casual: Contractions, conversational tone
   - Standard: Professional but approachable
   - Formal: No contractions, technical precision

3. **Workflow Preferences** (3 options):
   - require_confirmation: always | destructive | never
   - auto_commit: true | false
   - progressive_disclosure: true | false

**Test Implementation**:
```python
def test_verbosity_adaptation():
    # Test verbose preference
    prefs = {'communication': {'verbosity': 'verbose'}}
    response = generate_response("explain AGENTS.md pattern", prefs)

    assert len(response.split()) > 150, "Verbose response should be >150 words"
    assert "example" in response.lower(), "Verbose should include examples"

    # Test concise preference
    prefs = {'communication': {'verbosity': 'concise'}}
    response = generate_response("explain AGENTS.md pattern", prefs)

    assert len(response.split()) < 50, "Concise response should be <50 words"

def test_confirmation_workflow():
    # Test require_confirmation: always
    prefs = {'workflow': {'require_confirmation': 'always'}}
    action = execute_action("delete file.txt", prefs)

    assert action.requires_confirmation == True

    # Test require_confirmation: destructive
    prefs = {'workflow': {'require_confirmation': 'destructive'}}
    action1 = execute_action("delete file.txt", prefs)  # Destructive
    action2 = execute_action("read file.txt", prefs)  # Non-destructive

    assert action1.requires_confirmation == True
    assert action2.requires_confirmation == False
```

**Acceptance**: All 100+ config options successfully adapt agent behavior

**Deliverable**: Test report showing preference adaptation for each category

#### Task 5.3: Pattern Learning Validation (1 hour)

**Test Suite**: `tests/test_pattern_learning.py`

**Test Scenarios**:

1. **New Pattern Addition**:
   - Add new pattern to INTENT_PATTERNS.yaml
   - Verify router recognizes new triggers
   - Verify existing patterns still work (regression)

2. **Pattern Variation**:
   - User says: "what's happening with coord-005"
   - Should match existing pattern: "review coord-NNN"
   - Should extract parameter: id="coord-005"

3. **Pattern Conflict**:
   - Two patterns match with similar confidence
   - Should offer both as alternatives
   - Should request clarification

**Test Implementation**:
```python
def test_new_pattern_addition():
    # Before: Pattern doesn't exist
    router = IntentRouter()
    matches = router.route("archive completed work")
    assert matches[0].confidence < 0.50  # No match

    # Add new pattern
    new_pattern = {
        'pattern_id': 'archive_completed',
        'action': 'archive_completed_coordination_requests',
        'triggers': ['archive completed', 'archive finished', 'move to archive'],
        'parameters': {},
        'description': 'Archive completed coordination requests'
    }
    router.add_pattern(new_pattern)

    # After: Pattern exists
    matches = router.route("archive completed work")
    assert matches[0].action == 'archive_completed_coordination_requests'
    assert matches[0].confidence >= 0.70

    # Regression: Existing patterns still work
    matches = router.route("show inbox")
    assert matches[0].action == 'run_inbox_status'

def test_pattern_conflict():
    router = IntentRouter()
    matches = router.route("check")  # Ambiguous: check inbox? check coverage? check quality?

    # Should have multiple matches with similar confidence
    assert len(matches) >= 2
    assert abs(matches[0].confidence - matches[1].confidence) < 0.20

    # Should request clarification
    assert matches[0].clarification is not None
    assert "did you mean" in matches[0].clarification.lower()
```

**Acceptance**: New patterns captured without breaking existing patterns

**Deliverable**: Pattern learning test report with regression validation

#### Task 5.4: Quality Gate Validation (1-2 hours)

**Quality Gates**:

1. **Test Coverage ≥85%**:
   ```bash
   pytest --cov=scripts --cov=docs/skilled-awareness/agent-awareness --cov-report=term-missing
   ```

2. **Lint Validation (0 errors)**:
   ```bash
   ruff check scripts/ features/
   ```

3. **Type Checking (0 errors)**:
   ```bash
   mypy scripts/ --strict
   ```

4. **Documentation Completeness**:
   - [ ] SAP-009 protocol-spec.md Section 9 complete
   - [ ] SAP-009 awareness-guide.md integration section complete
   - [ ] 5 domain AGENTS.md files updated
   - [ ] All tools have docstrings
   - [ ] All functions have type hints

**Test Implementation**:
```bash
# Run all quality gates
pytest --cov=scripts --cov-report=term-missing
ruff check scripts/ features/
mypy scripts/ --strict

# Validate coverage threshold
pytest --cov=scripts --cov-report=term --cov-fail-under=85
```

**Acceptance**: All quality gates passing

**Deliverable**: Quality gate report (coverage %, lint results, type check results)

**Phase 5 Exit Criteria**:
- [ ] Intent recognition ≥80% accurate
- [ ] Preference adaptation verified (all 100+ options)
- [ ] Pattern learning validated (no regressions)
- [ ] All quality gates passing (coverage ≥85%, 0 lint/type errors)
- [ ] phase_completed event emitted for Testing phase

---

### Phase 6: Governance Documentation Updates (2-3 hours)

**Objective**: Complete all administrative and governance documentation

#### Task 6.1: Update CHANGELOG.md (0.5 hours)

**File**: `CHANGELOG.md`

**Changes**: Add v4.1.3 entry following Keep a Changelog format

**New Entry**:
```markdown
## [4.1.3] - 2025-XX-XX

### Added

- **Bidirectional Translation Layer** (SAP-009 v1.1.0 enhancement):
  - Intent routing: Natural language → formal actions via `scripts/intent-router.py`
  - Glossary search: Term discovery and ontology learning via `scripts/chora-search.py`
  - Context-aware suggestions: Next action recommendations via `scripts/suggest-next.py`
  - User preferences: 100+ config options for agent behavior adaptation via `.chora/user-preferences.yaml`
  - Intent patterns database: 24+ patterns in `docs/dev-docs/patterns/INTENT_PATTERNS.yaml`
  - Ecosystem glossary: 75+ terms in `docs/GLOSSARY.md`
  - Progressive formalization: Casual → semi-formal → formal → executable workflow
  - Mutual ergonomics: System adapts to user style; user gradually learns systemic ontology

### Changed

- **SAP-009 (agent-awareness) enhanced to v1.1.0**:
  - Added Section 9 to `protocol-spec.md`: Bidirectional Translation Layer contracts
  - Enhanced `awareness-guide.md` with integration patterns for generic agents
  - Updated 5 domain AGENTS.md files with user signal patterns:
    - SAP-001 (inbox-protocol): Inbox operations patterns
    - SAP-004 (testing-framework): Testing operations patterns
    - SAP-009 (agent-awareness): Agent discovery and translation patterns
    - SAP-012 (development-lifecycle): Development lifecycle operations patterns
    - SAP-013 (metrics-framework): Metrics operations patterns
  - `capability-charter.md` version: 1.0.0 → 1.1.0
  - `ledger.md`: Added v1.1.0 release tracking and adoption metrics
- Enhanced `scripts/suggest-next.py` with inbox-aware suggestions
- Updated SAP Index (`docs/skilled-awareness/INDEX.md`) showing SAP-009 v1.1.0

### Fixed

- None (enhancement only, backward compatible)

### Technical Details

- **Intent Recognition Accuracy**: ≥80% on test query set (30+ queries)
- **Test Coverage**: ≥85% for integration code
- **Documentation**: Follows Diátaxis framework (how-to, reference, explanation)
- **Generic Agent Compatibility**: Subprocess invocation pattern (works for Claude, Cursor, etc.)
- **Graceful Degradation**: Falls back to documented patterns if tools unavailable
- **Migration**: SAP-009 v1.0.0 → v1.1.0 is backward compatible (additive only)

### Coordination

- Coordination Request: COORD-2025-004
- Sprint: Sprint 5
- Trace ID: coord-2025-004-bidirectional
- Related SAPs: SAP-001, SAP-004, SAP-009, SAP-012, SAP-013
```

**Deliverable**: CHANGELOG.md updated with v4.1.3 entry

#### Task 6.2: Update SAP-009 Artifacts (1 hour)

**Files to Update**:

1. **capability-charter.md**:
   - Update version: 1.0.0 → 1.1.0
   - Add version history entry:
     ```markdown
     ## Version History

     | Version | Date | Changes |
     |---------|------|---------|
     | 1.1.0 | 2025-XX-XX | Added bidirectional translation layer: intent routing, glossary search, context-aware suggestions, user preferences |
     | 1.0.0 | 2025-10-28 | Initial release: AGENTS.md/CLAUDE.md dual-file pattern, progressive context loading |
     ```

2. **ledger.md**:
   - Update header: "Current Version: 1.1.0"
   - Update "Last Updated" date
   - Update Version History table:
     ```markdown
     | Version | Release Date | Type | Changes |
     |---------|--------------|------|---------|
     | 1.1.0 | 2025-XX-XX | MINOR | Bidirectional translation layer: intent routing, glossary search, context-aware suggestions (COORD-2025-004) |
     | 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-009 release: AGENTS.md/CLAUDE.md patterns, nested awareness |
     ```
   - Add adoption tracking if applicable:
     ```markdown
     ## 1. Projects Using Agent Awareness

     | Project | Root AGENTS.md | Root CLAUDE.md | Bidirectional Tools | Last Updated |
     |---------|----------------|----------------|---------------------|--------------|
     | chora-base | ✅ Yes | ✅ Yes | ✅ Yes (v1.1.0) | 2025-XX-XX |
     | chora-compose | ✅ Yes | ❌ No | ❌ No | 2025-10-20 |
     | mcp-n8n | ✅ Yes | ❌ No | ❌ No | 2025-10-22 |
     ```

3. **ledger.md version history**:
   - Add entry:
     ```markdown
     **Version History**:
     - **1.1.0** (2025-XX-XX): Added v1.1.0 release tracking, bidirectional tools adoption column
     - **1.1.0** (In Progress): Added v1.1.0 development tracking for bidirectional translation layer
     - **1.0.0** (2025-10-28): Initial ledger
     ```

**Deliverable**: 3 SAP-009 artifacts updated with v1.1.0 release info

#### Task 6.3: Update SAP Index (0.5 hours)

**File**: `docs/skilled-awareness/INDEX.md`

**Changes**:

1. Update Active SAPs table:
   ```markdown
   | SAP-009 | agent-awareness | 1.1.0 | Draft | Phase 3 | ✅ 4/4 | [agent-awareness/](agent-awareness/) | SAP-000, SAP-007 |
   ```

2. Update SAP-009 description:
   ```markdown
   #### SAP-009: agent-awareness
   - **Purpose**: AGENTS.md/CLAUDE.md patterns, nested awareness files, bidirectional translation layer
   - **Includes**: AGENTS.md.blueprint (~900 lines), CLAUDE.md.blueprint (~450 lines), nested patterns (4 domains), intent routing, glossary search, context-aware suggestions
   - **Status**: ✅ Draft (v1.1.0 released - COORD-2025-004)
   - **Scope**: Implementation
   - **Key Features**: Dual-file pattern (AGENTS + CLAUDE), "Nearest File Wins", progressive context loading (200k tokens), token budgets, bidirectional translation (conversational ↔ procedural), mutual ergonomics
   ```

3. Update Last Updated date:
   ```markdown
   **Last Updated**: 2025-XX-XX
   ```

4. Update changelog:
   ```markdown
   | Date | Change | Author |
   |------|--------|--------|
   | 2025-XX-XX | SAP-009 v1.1.0 released: Bidirectional translation layer complete (COORD-2025-004, Sprint 5) | Claude Code |
   | 2025-10-31 | SAP-009 v1.1.0 development started: Bidirectional translation layer (COORD-2025-004, Sprint 5) | Claude Code |
   ```

**Deliverable**: SAP Index updated with SAP-009 v1.1.0

#### Task 6.4: Emit Governance Events (0.5 hours)

**File**: `inbox/coordination/events.jsonl`

**Events to Emit**:

1. **DDD Phase Completed**:
   ```json
   {"event_type": "phase_completed", "phase": "DDD", "task_id": "coord-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT12:00:00Z", "repo": "chora-base", "deliverables": ["change-request.md"]}
   ```

2. **BDD Phase Completed**:
   ```json
   {"event_type": "phase_completed", "phase": "BDD", "task_id": "coord-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT14:00:00Z", "repo": "chora-base", "deliverables": ["features/bidirectional-integration.feature", "features/steps/bidirectional_steps.py"]}
   ```

3. **TDD Phase Completed**:
   ```json
   {"event_type": "phase_completed", "phase": "TDD", "task_id": "coord-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT18:00:00Z", "repo": "chora-base", "deliverables": ["SAP-009 protocol-spec.md Section 9", "SAP-009 awareness-guide.md enhancement", "5 domain AGENTS.md updates", "suggest-next.py inbox integration"]}
   ```

4. **Testing Phase Completed**:
   ```json
   {"event_type": "phase_completed", "phase": "Testing", "task_id": "coord-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT22:00:00Z", "repo": "chora-base", "quality_gates": {"intent_accuracy": "85%", "test_coverage": "87%", "lint_errors": 0, "type_errors": 0}}
   ```

5. **SAP Enhanced Event**:
   ```json
   {"event_type": "sap_enhanced", "sap_id": "SAP-009", "old_version": "1.0.0", "new_version": "1.1.0", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT23:00:00Z", "repo": "chora-base", "enhancement": "Bidirectional translation layer"}
   ```

6. **Governance Phase Completed**:
   ```json
   {"event_type": "phase_completed", "phase": "Governance", "task_id": "coord-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT23:30:00Z", "repo": "chora-base", "deliverables": ["CHANGELOG.md v4.1.3", "SAP-009 artifacts updated", "SAP Index updated"]}
   ```

**Deliverable**: 6 events appended to events.jsonl

**Phase 6 Exit Criteria**:
- [ ] CHANGELOG.md updated with v4.1.3 entry
- [ ] SAP-009 capability-charter.md, ledger.md updated to v1.1.0
- [ ] SAP Index updated with SAP-009 v1.1.0
- [ ] All 6 governance events emitted
- [ ] phase_completed event emitted for Governance phase

---

### Phase 7: Review & Integration (4 hours)

**Objective**: External validation via PR review and CI/CD

#### Task 7.1: Create Pull Request (1 hour)

**PR Title**: `feat(SAP-009): Add bidirectional translation layer (v1.1.0) - COORD-2025-004`

**PR Description**:
```markdown
## Summary

Enhances SAP-009 (agent-awareness) with bidirectional translation layer to enable mutual ergonomics between conversational user input and procedural execution.

Completes COORD-2025-004, Sprint 5.

## Changes

### Added (Foundation - Already Merged)
- ✅ `scripts/intent-router.py` (470 lines) - Natural language → formal actions
- ✅ `scripts/chora-search.py` (380 lines) - Glossary search with fuzzy matching
- ✅ `scripts/suggest-next.py` (470 lines) - Context-aware next action suggestions
- ✅ `docs/dev-docs/patterns/INTENT_PATTERNS.yaml` (377 lines) - 24+ intent patterns
- ✅ `docs/GLOSSARY.md` (640 lines) - 75+ terms, 14 categories
- ✅ `.chora/user-preferences.yaml.template` (380 lines) - 100+ config options
- ✅ `docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md` (1,060 lines) - Implementation guide
- ✅ `AGENTS.md` (+214 lines) - Tool discovery patterns

### Added (This PR)
- `features/bidirectional-integration.feature` - BDD scenarios (8+ scenarios)
- `features/steps/bidirectional_steps.py` - Step definitions (~300-400 lines)
- `tests/test_intent_recognition_accuracy.py` - Intent accuracy tests (30+ queries)
- `tests/test_preference_adaptation.py` - Preference adaptation tests
- `tests/test_pattern_learning.py` - Pattern learning validation tests
- `docs/releases/v4.1.3-release-notes.md` - Release documentation

### Changed (This PR)
- `docs/skilled-awareness/agent-awareness/protocol-spec.md` - Added Section 9 (~400-600 lines)
- `docs/skilled-awareness/agent-awareness/awareness-guide.md` - Integration patterns (~300-500 lines)
- `docs/skilled-awareness/agent-awareness/capability-charter.md` - Version 1.0.0 → 1.1.0
- `docs/skilled-awareness/agent-awareness/ledger.md` - v1.1.0 release tracking
- `docs/skilled-awareness/INDEX.md` - SAP-009 version updated, changelog entry
- `scripts/suggest-next.py` - Inbox-aware suggestions (~50-100 lines)
- `CHANGELOG.md` - v4.1.3 entry

**Domain AGENTS.md Updates** (5 files):
- `docs/skilled-awareness/inbox-protocol/AGENTS.md` - Inbox user signals (~100-150 lines)
- `docs/skilled-awareness/testing-framework/AGENTS.md` - Testing user signals (~100-150 lines)
- `docs/skilled-awareness/agent-awareness/AGENTS.md` - Agent awareness user signals (~100-150 lines)
- `docs/skilled-awareness/development-lifecycle/AGENTS.md` - Lifecycle user signals (~100-150 lines)
- `docs/skilled-awareness/metrics-framework/AGENTS.md` - Metrics user signals (~100-150 lines)

## Acceptance Criteria Status

- ✅ Intent recognition accuracy ≥80% (achieved: XX%)
- ✅ Generic agents can discover tools via documentation alone
- ✅ Tools gracefully degrade (missing tool → documented pattern fallback)
- ✅ User preferences successfully adapt agent behavior (100+ options tested)
- ✅ Pattern learning captures new variations without breaking existing patterns
- ✅ Suggestion engine provides context-aware recommendations
- ✅ All BDD scenarios passing (XX/XX)
- ✅ Test coverage ≥85% (achieved: XX%)
- ✅ No lint/type errors (0 errors)
- ✅ Documentation follows Diátaxis framework
- ✅ SAP-009 enhancement properly versioned (v1.0.0 → v1.1.0)
- ✅ CHANGELOG follows semantic versioning (v4.1.3 PATCH release)

## Testing

```bash
# Run all BDD scenarios
pytest features/

# Run accuracy tests
pytest tests/test_intent_recognition_accuracy.py -v

# Run quality gates
pytest --cov=scripts --cov-report=term-missing
ruff check scripts/ features/
mypy scripts/ --strict
```

## Migration

**Backward Compatible**: SAP-009 v1.0.0 users can upgrade to v1.1.0 without breaking changes.

**New Capabilities**:
- Intent routing: Natural language → formal actions
- Glossary search: Term discovery and learning
- Context-aware suggestions: Next action recommendations
- User preferences: Behavior adaptation

**Optional Tools**: Bidirectional tools are optional enhancements. If not available, agents fall back to documented patterns (graceful degradation).

## Related

- Coordination Request: [COORD-2025-004](../inbox/incoming/coordination/COORD-2025-004-bidirectional-integration.json)
- Communication Brief: [COORD-2025-004-communication-brief.md](../inbox/coordination/COORD-2025-004-communication-brief.md)
- Sprint Plan: [sprint-05.md](../docs/project-docs/sprints/sprint-05.md)
- Implementation Guide: [BIDIRECTIONAL_COMMUNICATION.md](../docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md)
- Trace ID: coord-2025-004-bidirectional

## Checklist

- [ ] All 12 acceptance criteria met
- [ ] All 11 deliverables from COORD-2025-004 created
- [ ] All BDD scenarios passing
- [ ] Test coverage ≥85%
- [ ] No lint errors (ruff)
- [ ] No type errors (mypy)
- [ ] Documentation complete (Diátaxis)
- [ ] CHANGELOG.md updated (v4.1.3)
- [ ] SAP-009 artifacts updated (v1.1.0)
- [ ] SAP Index updated
- [ ] All governance events emitted
- [ ] CI/CD passing
```

**Deliverable**: PR created with comprehensive description and checklist

#### Task 7.2: Code Review (2 hours)

**Reviewers**: Technical lead, domain experts

**Review Focus**:
1. **Technical correctness**: Contracts well-defined, integration points clear
2. **Documentation quality**: Diátaxis adherence, examples clear, usage patterns documented
3. **Test coverage**: ≥85%, edge cases covered, quality gates validated
4. **Backward compatibility**: No breaking changes to SAP-009 v1.0.0
5. **Governance compliance**: CHANGELOG, SAP Index, ledger updated correctly

**Review Checklist**:
- [ ] All 12 acceptance criteria verified
- [ ] SAP-009 protocol-spec.md Section 9 reviewed
- [ ] SAP-009 awareness-guide.md integration patterns reviewed
- [ ] 5 domain AGENTS.md updates reviewed
- [ ] BDD scenarios comprehensive and passing
- [ ] Test coverage meets ≥85% threshold
- [ ] Lint/type checks passing
- [ ] Documentation completeness verified
- [ ] CHANGELOG entry accurate
- [ ] SAP Index updated correctly

**Deliverable**: Review feedback, approval, or requested changes

#### Task 7.3: CI/CD Validation (1 hour)

**CI/CD Checks**:

1. **Test Suite**:
   ```yaml
   - name: Run tests
     run: pytest --cov=scripts --cov-report=xml --cov-fail-under=85
   ```

2. **Lint Check**:
   ```yaml
   - name: Lint with ruff
     run: ruff check scripts/ features/
   ```

3. **Type Check**:
   ```yaml
   - name: Type check with mypy
     run: mypy scripts/ --strict
   ```

4. **Link Validation**:
   ```yaml
   - name: Validate links
     run: bash scripts/validate-links.sh
   ```

5. **BDD Scenarios**:
   ```yaml
   - name: Run BDD scenarios
     run: pytest features/ -v
   ```

**Acceptance**: All CI/CD checks green

**Deliverable**: CI/CD validation passing

**Phase 7 Exit Criteria**:
- [ ] PR created with comprehensive description
- [ ] Code review approved
- [ ] All CI/CD checks passing
- [ ] No merge conflicts
- [ ] phase_completed event emitted for Review phase

---

### Phase 8: Release & Deployment (1 hour)

**Objective**: Version bump, GitHub release, archival

#### Task 8.1: Version Bump (0.25 hours)

**Actions**:
1. Update version references (if applicable in package files)
2. Create git tag:
   ```bash
   git tag -a v4.1.3 -m "Release v4.1.3: Bidirectional Translation Layer (SAP-009 v1.1.0)"
   git push origin v4.1.3
   ```

**Deliverable**: Git tag v4.1.3 created

#### Task 8.2: Create GitHub Release (0.5 hours)

**Release Title**: `v4.1.3 - Bidirectional Translation Layer (SAP-009 v1.1.0)`

**Release Notes**: Copy from docs/releases/v4.1.3-release-notes.md

**GitHub Release Format**:
```markdown
## Release v4.1.3 - Bidirectional Translation Layer

This release enhances SAP-009 (agent-awareness) with bidirectional translation layer, enabling mutual ergonomics between conversational user input and procedural execution.

### Added

- **Bidirectional Translation Layer** (SAP-009 v1.1.0 enhancement):
  - Intent routing via `scripts/intent-router.py` (natural language → formal actions)
  - Glossary search via `scripts/chora-search.py` (term discovery, fuzzy matching)
  - Context-aware suggestions via `scripts/suggest-next.py` (next action recommendations)
  - User preferences via `.chora/user-preferences.yaml` (100+ behavior options)
  - Intent patterns database (24+ patterns in INTENT_PATTERNS.yaml)
  - Ecosystem glossary (75+ terms in GLOSSARY.md)

### Changed

- SAP-009 enhanced to v1.1.0:
  - Added Section 9 to protocol-spec.md (bidirectional translation contracts)
  - Enhanced awareness-guide.md (integration patterns for generic agents)
  - Updated 5 domain AGENTS.md files with user signal patterns
  - Integrated suggestion engine with inbox protocol

### Technical Details

- **Intent Recognition Accuracy**: ≥80% (tested on 30+ query variations)
- **Test Coverage**: ≥85%
- **Backward Compatible**: SAP-009 v1.0.0 → v1.1.0 (additive only, no breaking changes)
- **Generic Agent Support**: Subprocess invocation pattern (works for Claude, Cursor, etc.)
- **Graceful Degradation**: Falls back to documented patterns if tools unavailable

### Coordination

- Coordination Request: COORD-2025-004
- Sprint: Sprint 5
- Trace ID: coord-2025-004-bidirectional
- Related SAPs: SAP-001, SAP-004, SAP-009, SAP-012, SAP-013

### Full Changelog

See [CHANGELOG.md](https://github.com/liminalcommons/chora-base/blob/main/CHANGELOG.md) for complete version history.
```

**Deliverable**: GitHub release published with tag v4.1.3

#### Task 8.3: Archive Completed Work (0.25 hours)

**Actions**:

1. Update ECOSYSTEM_STATUS.yaml:
   ```yaml
   repositories:
     chora-base:
       active_work:
         # Remove COORD-2025-004
       recent_completions:
         - id: COORD-2025-004
           title: "Bidirectional Translation Layer Integration (SAP-009 Enhancement)"
           completed: 2025-XX-XX
           deliverables: "11/11 completed"
           effort: "XX hours"
           outcome: "SAP-009 v1.1.0 released, 80%+ intent accuracy, 85%+ coverage"
   ```

2. Emit coordination_request_completed event:
   ```json
   {"event_type": "coordination_request_completed", "request_id": "COORD-2025-004", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT23:45:00Z", "repo": "chora-base", "decision": "completed", "deliverables": 11, "acceptance_criteria": 12, "outcome": "SAP-009 v1.1.0 released"}
   ```

3. Emit release_created event:
   ```json
   {"event_type": "release_created", "version": "v4.1.3", "trace_id": "coord-2025-004-bidirectional", "timestamp": "2025-XX-XXT23:50:00Z", "repo": "chora-base", "release_type": "PATCH", "sap_enhancements": ["SAP-009 v1.0.0 → v1.1.0"]}
   ```

4. Move inbox/active/coord-2025-004-bidirectional/ to inbox/archived/ (if applicable)

**Deliverable**: Completed work archived, events emitted

**Phase 8 Exit Criteria**:
- [ ] Version bumped to v4.1.3
- [ ] Git tag created and pushed
- [ ] GitHub release published
- [ ] ECOSYSTEM_STATUS.yaml updated (COORD-2025-004 marked completed)
- [ ] coordination_request_completed event emitted
- [ ] release_created event emitted
- [ ] Sprint complete

---

## Summary of Deliverables

### Documentation (6 files created/enhanced)

1. ✅ This change request (change-request.md)
2. ⏳ features/bidirectional-integration.feature (BDD scenarios)
3. ⏳ features/steps/bidirectional_steps.py (Step definitions)
4. ⏳ docs/releases/v4.1.3-release-notes.md (Release documentation)
5. ⏳ SAP-009 protocol-spec.md Section 9 (~400-600 lines)
6. ⏳ SAP-009 awareness-guide.md integration section (~300-500 lines)

### Code (1 file enhanced)

7. ⏳ scripts/suggest-next.py inbox integration (~50-100 lines)

### Configuration (5 files enhanced)

8. ⏳ docs/skilled-awareness/inbox-protocol/AGENTS.md user signals
9. ⏳ docs/skilled-awareness/testing-framework/AGENTS.md user signals
10. ⏳ docs/skilled-awareness/agent-awareness/AGENTS.md user signals
11. ⏳ docs/skilled-awareness/development-lifecycle/AGENTS.md user signals
12. ⏳ docs/skilled-awareness/metrics-framework/AGENTS.md user signals

### Testing (3 files created)

13. ⏳ tests/test_intent_recognition_accuracy.py (30+ query tests)
14. ⏳ tests/test_preference_adaptation.py (100+ option tests)
15. ⏳ tests/test_pattern_learning.py (regression validation)

### Governance (3 files updated)

16. ⏳ CHANGELOG.md (v4.1.3 entry)
17. ⏳ SAP-009 capability-charter.md (version 1.0.0 → 1.1.0)
18. ⏳ SAP-009 ledger.md (v1.1.0 release tracking)
19. ⏳ SAP Index (SAP-009 version update)

### Events (7+ events)

20. ⏳ phase_completed events (DDD, BDD, TDD, Testing, Governance, Review)
21. ⏳ sap_enhanced event (SAP-009 v1.0.0 → v1.1.0)
22. ⏳ coordination_request_completed event
23. ⏳ release_created event (v4.1.3)

**Total**: 23+ deliverables across 8 phases

---

## Technical Specifications

### Intent Router Contract

**Function Signature**:
```python
def route(user_input: str) -> list[IntentMatch]:
    """
    Route natural language input to formal actions with confidence scoring.

    Args:
        user_input: Natural language string (e.g., "show inbox")

    Returns:
        List of IntentMatch objects sorted by confidence descending

    IntentMatch:
        - action (str): Formal action identifier
        - confidence (float): 0.0-1.0 confidence score
        - parameters (dict): Extracted parameters
        - pattern_id (str): Matching pattern ID
        - clarification (str|None): Clarification question if ambiguous
    """
```

**Confidence Thresholds**:
- ≥0.70: Execute automatically
- 0.50-0.70: Request clarification
- <0.50: Suggest alternatives

**Example Usage**:
```python
from scripts.intent_router import IntentRouter

router = IntentRouter()
matches = router.route("what's pending in the inbox")

if matches[0].confidence >= 0.70:
    # High confidence: execute
    execute_action(matches[0].action, matches[0].parameters)
elif matches[0].confidence >= 0.50:
    # Medium confidence: clarify
    ask_user(matches[0].clarification)
else:
    # Low confidence: suggest alternatives
    offer_alternatives(matches[:3])
```

### Glossary Search Contract

**Function Signature**:
```python
def search(query: str, fuzzy: bool = False) -> list[tuple[GlossaryEntry, float]]:
    """
    Search glossary for term with optional fuzzy matching.

    Args:
        query: Search term
        fuzzy: Enable fuzzy matching (≥60% similarity)

    Returns:
        List of (GlossaryEntry, relevance_score) tuples sorted by score

    GlossaryEntry:
        - term (str): Canonical term
        - definition (str): Term definition
        - category (str): Category
        - aliases (list[str]): Alternative names
        - related (list[str]): Related terms
        - sap_reference (str|None): Related SAP
        - examples (list[str]): Usage examples
    """
```

**Relevance Scoring**:
- 1.0: Exact match
- 0.8: Contains (substring)
- 0.4-0.7: Fuzzy match (≥60% similarity)

**Example Usage**:
```python
from scripts.chora_search import GlossarySearch

glossary = GlossarySearch()
results = glossary.search("coordination", fuzzy=True)

for entry, score in results[:3]:
    print(f"{entry.term} (relevance: {score:.2f})")
    print(f"  Definition: {entry.definition}")
    print(f"  SAP: {entry.sap_reference}")
    print(f"  Related: {', '.join(entry.related)}")
```

### Suggestion Engine Contract

**Function Signature**:
```python
def suggest(mode: str = "reactive") -> list[Suggestion]:
    """
    Generate context-aware next action suggestions.

    Args:
        mode: "reactive" (top 5) or "proactive" (high priority only)

    Returns:
        List of Suggestion objects sorted by priority

    Suggestion:
        - action (str): Suggested action description
        - rationale (str): Why this suggestion
        - priority (str): "high" | "medium" | "low"
        - category (str): "workflow" | "quality" | "planning" | "learning"
        - estimated_effort (str): Time estimate
    """
```

**Context Sources**:
- Inbox status (pending requests, blockers)
- Sprint phase (planning, development, testing, review)
- Quality metrics (coverage, broken links, lint errors)
- Documentation state (missing files, outdated content)

**Example Usage**:
```python
from scripts.suggest_next import SuggestionEngine, ProjectContext

context = ProjectContext.from_current_directory()
engine = SuggestionEngine(context)
suggestions = engine.suggest(mode="reactive")

for suggestion in suggestions:
    print(f"[{suggestion.priority}] {suggestion.action}")
    print(f"  Why: {suggestion.rationale}")
    print(f"  Effort: {suggestion.estimated_effort}")
```

### User Preferences Contract

**Configuration Structure**:
```yaml
communication:
  verbosity: standard  # concise|standard|verbose
  formality: standard  # casual|standard|formal
  output_format: terminal  # terminal|markdown|json

workflow:
  require_confirmation: destructive  # always|destructive|never
  auto_commit: false
  progressive_disclosure: true

learning:
  capture_patterns: true
  suggest_improvements: true
  track_usage: true

expertise:
  assume_knowledge: intermediate  # beginner|intermediate|expert
  explain_rationale: true
  show_alternatives: true
```

**Example Usage**:
```python
import yaml

with open('.chora/user-preferences.yaml') as f:
    prefs = yaml.safe_load(f)

# Adapt verbosity
if prefs['communication']['verbosity'] == 'verbose':
    response += detailed_explanation()
    response += examples()

# Adapt confirmation behavior
if prefs['workflow']['require_confirmation'] == 'always':
    confirm_before_action()
elif prefs['workflow']['require_confirmation'] == 'destructive':
    if action_is_destructive():
        confirm_before_action()
```

---

## Risk Mitigation

### Risk 1: Intent Recognition Accuracy <80%

**Mitigation**:
- Pilot testing with 30+ query variations
- Pattern refinement iteration based on results
- Fallback to documented patterns if tool unavailable

### Risk 2: Generic Agents Can't Discover Tools

**Mitigation**:
- Documentation-first approach (3-layer progressive)
- Subprocess invocation pattern (no auto-loading required)
- Validate with multiple agent types (Claude, Cursor)

### Risk 3: Pattern Learning Creates False Positives

**Mitigation**:
- Manual pattern curation (no auto-addition)
- Comprehensive regression tests
- Review process for new patterns

### Risk 4: Preference Adaptation Edge Cases

**Mitigation**:
- Test all 100+ config options
- Graceful degradation if preference file missing
- Use defaults from template

### Risk 5: Sprint Extends Beyond 24 Hours

**Mitigation**:
- Strict scope adherence (excluded items documented)
- Phase-based checkpoints with exit criteria
- Quality gates prevent scope creep

---

## Success Metrics

### Technical Metrics

- **Intent Recognition Accuracy**: ≥80% (target: 85%)
- **Test Coverage**: ≥85% (target: 90%)
- **Lint Errors**: 0
- **Type Errors**: 0
- **BDD Scenarios Passing**: 100%

### Quality Metrics

- **Documentation Completeness**: 100% (all 11 deliverables)
- **Governance Compliance**: 100% (CHANGELOG, SAP Index, ledger updated)
- **Backward Compatibility**: 100% (no breaking changes)
- **Generic Agent Support**: Tested with Claude, Cursor

### User Experience Metrics

- **Progressive Formalization**: Supported (casual → executable)
- **Mutual Ergonomics**: Demonstrated (system adapts, user learns)
- **Graceful Degradation**: Validated (tools optional)
- **Discovery Time**: <5 minutes (agent finds tools via AGENTS.md)

---

## Approval

**Technical Lead Approval**:
- [ ] Change request reviewed and approved
- [ ] Contracts well-defined
- [ ] Integration points clear
- [ ] Effort estimate realistic (16-24 hours)
- [ ] No breaking changes to SAP-009 v1.0.0

**Signature**: __________________ Date: __________

---

**Document Version**: 1.0
**Status**: Ready for Technical Lead Review
**Created**: 2025-10-31
**Last Updated**: 2025-10-31
**Trace ID**: coord-2025-004-bidirectional

---

## Approval

**Technical Lead Approval**: ✅ APPROVED

**Approver**: Victor Piper
**Date**: 2025-10-31
**Notes**: Change request approved. Proceed to Phase 4 (BDD).

**Approval Criteria Met**:
- ✅ Change request reviewed and approved
- ✅ Contracts well-defined (intent router, glossary, suggestions, preferences)
- ✅ Integration points clear (SAP-009 Section 9, 5 domain AGENTS.md files)
- ✅ Effort estimate realistic (16-24 hours across 8 phases)
- ✅ No breaking changes to SAP-009 v1.0.0 (additive only)

