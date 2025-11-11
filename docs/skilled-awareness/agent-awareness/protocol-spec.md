# Protocol Specification: Agent Awareness

**SAP ID**: SAP-009
**Version**: 2.1.0
**Status**: Active
**Last Updated**: 2025-11-10

---

## 1. Overview

### Purpose

The agent-awareness capability provides **structured guidance files for AI agents** using AGENTS.md (generic) and CLAUDE.md (Claude-specific) patterns with nested domain-specific awareness.

### Design Principles

1. **Dual-File Pattern** - AGENTS.md (all agents) + CLAUDE.md (Claude optimizations)
2. **Nearest File Wins** - Agents read awareness file nearest to code they're working on
3. **Progressive Loading** - Essential → Extended → Full context phases (manage 200k token budget)
4. **Domain-Specific** - Nested files (tests/AGENTS.md, scripts/AGENTS.md) for focused guidance
5. **Context Optimization** - Token budgets, checkpoint patterns, artifact-first development

---

## 2. File Structure

### 2.1 AGENTS.md Structure

**Purpose**: Generic AI agent guidance (all agents)
**Location**: Project root + nested directories
**Size**: ~900 lines (root), ~200-300 lines (nested)

**Sections**:
1. **Project Overview** - Architecture, key components, strategic context
2. **Development Process** - 8-phase lifecycle, DDD→BDD→TDD workflows
3. **Documentation Structure** - Nested awareness files (nearest file wins)
4. **Repository Structure** - Directory layout, key files
5. **Key Concepts** - Domain concepts, patterns, conventions
6. **Common Tasks** - Add feature, fix bug, write tests, create docs
7. **Testing** - Run tests, check coverage, debug failures
8. **Pull Request Workflow** - Create PR, address reviews, merge
9. **Troubleshooting** - Common issues, error recovery

**Example** (root AGENTS.md):
```markdown
# AGENTS.md

## Project Overview
**My Project** is a Model Context Protocol (MCP) server...

## Development Process
This project follows the 8-phase chora-base lifecycle...

## Documentation Structure (Nearest File Wins)
- [AGENTS.md](/AGENTS.md) - Project overview (this file)
- [tests/AGENTS.md](/AGENTS.md) - Testing guide
- [scripts/AGENTS.md](/AGENTS.md) - Script reference

## Key Concepts
**MCP Protocol**: [Explanation]
**Event Log**: [Explanation]
...
```

### 2.2 CLAUDE.md Structure

**Purpose**: Claude-specific optimizations
**Location**: Project root + nested directories
**Size**: ~450 lines (root), ~150-200 lines (nested)

**Sections**:
1. **Quick Start for Claude** - Reading order, Claude-specific capabilities
2. **Claude Capabilities Matrix** - Strengths per task type
3. **Context Window Management** - Progressive loading (200k tokens)
4. **Artifact-First Development** - When to use artifacts vs inline
5. **Checkpoint Patterns** - Session preservation every 5-10 interactions
6. **Token Budgets** - Budget by task (feature: 15-30k, bug: 5-10k, refactor: 20-40k)
7. **ROI Tracking** - ClaudeROICalculator integration

**Example** (root CLAUDE.md):
```markdown
# CLAUDE.md - Claude-Specific Development Guide

## Quick Start for Claude
1. Read [AGENTS.md](/AGENTS.md) first
2. Read CLAUDE.md (this file) for optimizations

## Context Window Management (200k Tokens)

### Progressive Loading
**Phase 1 (0-10k)**: Essential context (task + relevant files)
**Phase 2 (10-50k)**: Extended context (related modules + tests)
**Phase 3 (50-200k)**: Full context (entire codebase)

### Token Budgets by Task
- Add feature: 15-30k tokens
- Fix bug: 5-10k tokens
- Refactor: 20-40k tokens
```

### 2.3 Nested Awareness Pattern

**Principle**: "Nearest File Wins" - Agents read awareness file closest to code they're editing

**Structure**:
```
project-root/
├── AGENTS.md                    # Generic project guidance (~900 lines)
├── CLAUDE.md                    # Claude optimizations (~450 lines)
├── tests/
│   ├── AGENTS.md                # Testing guide (~250 lines)
│   └── CLAUDE.md                # Claude test patterns (~150 lines)
├── scripts/
│   ├── AGENTS.md                # Script reference (~200 lines)
│   └── CLAUDE.md                # Claude automation (~100 lines)
├── docker/
│   ├── AGENTS.md                # Docker operations (~200 lines)
│   └── CLAUDE.md                # Claude Docker patterns (~100 lines)
└── .chora/memory/
    ├── AGENTS.md                # Memory system (A-MEM) (~300 lines)
    └── CLAUDE.md                # Claude memory usage (~150 lines)
```

**Benefits**:
- Focused guidance (don't read entire project guide for testing)
- Faster context loading (200-300 lines vs 900 lines)
- Domain expertise (testing guide written by testing expert)
- Modularity (update domain guide without changing root)

---

## 3. Context Optimization

### 3.1 Progressive Context Loading

**Phase 1: Essential (0-10k tokens)**
Load immediately at session start:
- Current task definition
- Relevant AGENTS.md section
- Active files (1-3 files working on)
- Recent conversation summary

**Phase 2: Extended (10-50k tokens)**
Load as needed for implementation:
- Related module code
- Test suites for affected components
- Recent git history (git log --oneline -20)
- Related documentation

**Phase 3: Full (50-200k tokens)**
Load for complex refactoring:
- Complete codebase structure
- Full test suite
- All documentation
- Historical decisions

### 3.2 Token Budgets by Task

| Task Type | Token Budget | What to Load |
|-----------|--------------|--------------|
| Add small feature | 15-30k | Essential + relevant module + tests |
| Add major feature | 30-60k | Extended + dependencies + docs |
| Fix bug | 5-10k | Essential + error trace + relevant code |
| Refactor | 20-40k | Extended + affected modules + tests |
| Write docs | 10-20k | Essential + code to document + examples |
| Review PR | 15-25k | Essential + PR diff + related code |

### 3.3 Checkpoint Patterns

**Create checkpoint every 5-10 interactions**:

```markdown
## Claude Session Checkpoint

**Date**: 2025-10-28
**Task**: Add custom error handling to MCP server

**Progress**:
- ✅ Wrote CustomError class (src/utils/errors.py)
- ✅ Added tests (tests/utils/test_errors.py)
- 🔄 Integrating with server.py (in progress)

**Next Steps**:
1. Update server.py to use CustomError
2. Add error handling docs
3. Run full test suite

**Context Loaded** (25k tokens):
- src/utils/errors.py
- tests/utils/test_errors.py
- src/mcp/server.py
- AGENTS.md (error handling section)
```

---

## 4. Content Guidelines

### 4.1 AGENTS.md Content

**DO Include**:
- ✅ Project architecture overview
- ✅ Key concepts and domain terms
- ✅ Development workflow (DDD→BDD→TDD)
- ✅ Common tasks with step-by-step instructions
- ✅ Links to nested awareness files

**DON'T Include**:
- ❌ Claude-specific optimizations (use CLAUDE.md)
- ❌ Complete code examples (link to docs or reference)
- ❌ Implementation details (keep high-level)

### 4.2 CLAUDE.md Content

**DO Include**:
- ✅ Context window management strategies
- ✅ Token budgets by task type
- ✅ Checkpoint patterns
- ✅ Artifact-first development patterns
- ✅ ROI tracking integration

**DON'T Include**:
- ❌ Generic agent guidance (use AGENTS.md)
- ❌ Non-Claude-specific patterns
- ❌ Duplicate AGENTS.md content

### 4.3 Nested File Content

**DO Include**:
- ✅ Domain-specific guidance (testing, scripts, Docker, etc.)
- ✅ Quick reference for domain tasks
- ✅ Links back to root awareness files

**DON'T Include**:
- ❌ Project-wide architecture (in root AGENTS.md)
- ❌ Complete duplication of root content

---

## 4.4 Critical Workflows Pattern (v2.1.0)

**Purpose**: Surface frequently-missed workflows at the top of awareness files to solve the "meta-discoverability paradox"

**Problem**: As awareness files grow (>1,000 lines), critical workflows get buried and agents miss them despite documentation existing

**Solution**: Dedicated "⚠️ Critical Workflows (Read This First!)" section immediately after project overview

**Location**: Root AGENTS.md and CLAUDE.md, lines 20-100 (after overview, before main content)

**Structure**:
```markdown
## ⚠️ Critical Workflows (Read This First!)

**Problem solved**: [Brief description of workflows agents frequently miss]

### [Workflow 1 Name]
**When**: [Trigger condition - when to use this workflow]
**Quick reference**:
bash
# Commands or steps
command-1
command-2

**Full details**: [Link to nested file with complete template]

### [Workflow 2 Name]
**When**: [Trigger condition]
**Quick reference**:
- Step 1
- Step 2
- Step 3

**Full details**: [Link to detailed documentation]
```

**Example** (from chora-workspace implementation):
```markdown
## ⚠️ Critical Workflows (Read This First!)

**Problem solved**: Sprint completion workflows were buried at line 1,878 (66% into file) and frequently missed by agents.

### Sprint Completion Workflow
**When**: End of sprint (every 2 weeks)
**Quick reference**:
bash
just sprint-complete  # Generate report
git add . && git commit -m "chore: Sprint N completion"

**Full details**: [dev-process/AGENTS.md](dev-process/AGENTS.md#sprint-completion)

### Git Commit Conventions
**When**: Every commit
**Quick reference**:
bash
git commit -m "type(scope): description"
# Types: feat, fix, docs, chore, refactor, test

**Full details**: [dev-process/AGENTS.md](dev-process/AGENTS.md#git-conventions)
```

**Content Selection Criteria**:
- ✅ Workflows that agents have missed in past sessions
- ✅ Workflows critical to project success (e.g., testing, quality gates)
- ✅ Workflows with complex triggers (not obvious when to use)
- ✅ Workflows referenced frequently (>5 times per sprint)
- ❌ One-time setup tasks (put in getting-started guide)
- ❌ Workflows that are already discoverable via file structure

**Benefits**:
- Workflows discoverable in top 10% of file (vs 50-70% buried)
- Agent token usage reduced (workflows loaded in Phase 1)
- Pattern visibility increased (emoji makes section stand out)
- Navigation improved (quick ref + link to full details)

**Evidence**: chora-workspace implementation achieved:
- 70% file size reduction (2,766 → 839 lines)
- Workflows moved from line 1,878 to lines 32-50
- Sprint completion workflow no longer missed by agents

**Source**: COORD-2025-012 (Nested Awareness Pattern - Meta-Discoverability Solution)

---

## 5. Integration Patterns

### 5.1 With Documentation Framework (SAP-007)

**Awareness files are documentation**:
- Follow Diataxis principles (AGENTS.md = Reference + How-To)
- Include YAML frontmatter with progressive loading hints (recommended)

**Frontmatter Schema for Awareness Files** (Phase 2.4):

All AGENTS.md and CLAUDE.md files SHOULD include YAML frontmatter for better agent discoverability and progressive loading:

```yaml
---
sap_id: SAP-015                         # SAP ID if file is SAP-specific
version: 2.0.0                          # File version (track updates)
status: pilot                           # Status: draft | pilot | active
last_updated: 2025-11-04                # Last modification date
type: reference                         # Document type (usually "reference")
audience: agents                        # Primary audience (agents | developers | both)
complexity: intermediate                # Skill level: beginner | intermediate | advanced
estimated_reading_time: 12              # Minutes to read completely

# Progressive Loading Hints
progressive_loading:
  phase_1: "lines 1-100"                # Quick reference (0-10k tokens)
  phase_2: "lines 101-250"              # Implementation details (10-50k tokens)
  phase_3: "full"                       # Deep dive (50k+ tokens)

# Token Estimates (helps agents decide what to load)
phase_1_token_estimate: 2500            # Estimated tokens for phase 1
phase_2_token_estimate: 5000            # Estimated tokens for phase 2
phase_3_token_estimate: 8500            # Estimated tokens for full file

# Nested Structure Support (v2.1.0)
nested_structure: true                  # Optional: true if this file has nested awareness files
nested_files:                           # Optional: list of nested file paths (if nested_structure: true)
  - "saps/AGENTS.md"
  - "dev-process/AGENTS.md"
  - "docs/AGENTS.md"
---
```

**Progressive Loading Strategy**:

Agents should load awareness files in phases based on current context needs:

**Phase 1 (0-10k token budget)**:
- Load: Quick Reference section only
- Purpose: Orient to capability, check if relevant
- Example: Lines 1-100 (What is X? When to use? Key commands)

**Phase 2 (10-50k token budget)**:
- Load: Phase 1 + Common Workflows + Integration Patterns
- Purpose: Understand implementation details
- Example: Lines 1-250 (Workflows, CLI reference, integrations)

**Phase 3 (50k+ token budget)**:
- Load: Complete file
- Purpose: Deep understanding, troubleshooting, edge cases
- Example: Full file (including troubleshooting, advanced patterns)

**Example AGENTS.md with Frontmatter**:

```markdown
---
sap_id: SAP-015
version: 2.0.0
status: pilot
last_updated: 2025-11-04
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-100"
  phase_2: "lines 101-250"
  phase_3: "full"
phase_1_token_estimate: 2500
phase_2_token_estimate: 5000
phase_3_token_estimate: 8500
---

# Agent Task Tracking (SAP-015) - Agent Awareness

## Quick Reference  <!-- Phase 1 starts here -->

### What is Agent Task Tracking?

...

## Common Workflows  <!-- Phase 1 continues -->

...

## Integration Patterns  <!-- Phase 2 starts here (line 101+) -->

...

## Troubleshooting  <!-- Phase 3 includes this -->

...
```

**Benefits of Progressive Loading**:

1. **Reduced Token Usage**: Agents load only what they need (30-70% savings)
2. **Faster Context Loading**: Agents orient quickly with Phase 1
3. **Better Navigation**: Clear boundaries for partial reads
4. **Measurable Efficiency**: Token estimates help agents plan
- Link to related docs (user-docs/, dev-docs/)

### 5.2 With Development Lifecycle (SAP-012)

**AGENTS.md references DDD→BDD→TDD workflows**:
- Links to dev-docs/workflows/DDD_WORKFLOW.md
- Links to dev-docs/workflows/BDD_WORKFLOW.md
- Links to dev-docs/workflows/TDD_WORKFLOW.md
- Quick decision trees for agent workflow selection

---

## 6. Bidirectional Translation Layer (v1.1.0)

### 6.1 Overview

**Purpose**: Enable mutual ergonomics between conversational user input and procedural execution through progressive formalization.

**Key Principle**: Tools are TRANSLATION aids, not AUTOMATION. LLM intelligence remains primary for generation, reasoning, and design tasks.

### 6.2 Core Capabilities

The bidirectional translation layer provides three core capabilities:

1. **Intent Routing**: Natural language → Formal actions (`scripts/intent-router.py`)
2. **Glossary Search**: Term discovery and ontology learning (`scripts/chora-search.py`)
3. **Context Analysis**: Situation-aware next action suggestions (`scripts/suggest-next.py`)

**Supporting Infrastructure**:
- **Intent Patterns Database**: `docs/dev-docs/patterns/INTENT_PATTERNS.yaml` (24+ patterns)
- **Ecosystem Glossary**: `docs/GLOSSARY.md` (75+ terms, 14 categories)
- **User Preferences**: `.chora/user-preferences.yaml` (100+ configuration options)

### 6.3 Intent Router Contract

**Script**: `scripts/intent-router.py`

**Purpose**: Route natural language input to formal actions with confidence scoring

**Input**: Natural language user input (string)

**Output**: List of `IntentMatch` objects, sorted by confidence descending

**IntentMatch Structure**:
```python
class IntentMatch:
    action: str              # Formal action identifier (e.g., "run_inbox_status")
    confidence: float        # Match confidence 0.0-1.0
    parameters: dict         # Extracted parameters from input
    pattern_id: str          # Matching pattern identifier
    clarification: str|None  # Clarification question if ambiguous
```

**Confidence Thresholds**:
- **≥0.70**: Execute action automatically (high confidence)
- **0.50-0.70**: Request clarification from user (medium confidence)
- **<0.50**: Offer alternatives (low confidence)

**Usage Pattern**:
```python
from scripts.intent_router import IntentRouter

router = IntentRouter()
matches = router.route("show inbox")

if matches[0].confidence >= 0.70:
    # High confidence: execute action
    execute_action(matches[0].action, matches[0].parameters)
elif matches[0].confidence >= 0.50:
    # Medium confidence: ask for clarification
    ask_clarification(matches[0].clarification, matches[0].alternatives)
else:
    # Low confidence: suggest alternatives
    suggest_alternatives(matches[:3])
```

**Pattern Database**: `docs/dev-docs/patterns/INTENT_PATTERNS.yaml`

**Pattern Structure**:
```yaml
- pattern_id: inbox_status
  action: run_inbox_status
  triggers:
    - show inbox
    - what's in the inbox
    - inbox status
    - check inbox
  parameters: {}
  description: Display inbox status dashboard
  examples:
    - "What's in the inbox?"
    - "Show me pending coordination requests"
  sap_reference: SAP-001
```

**Graceful Degradation**: If script not available, fall back to pattern matching in INTENT_PATTERNS.yaml

### 6.4 Glossary Search Contract

**Script**: `scripts/chora-search.py`

**Purpose**: Search glossary for term discovery and ontology learning

**Input**: Search query (string), optional fuzzy flag (bool)

**Output**: List of `(GlossaryEntry, relevance_score)` tuples

**GlossaryEntry Structure**:
```python
class GlossaryEntry:
    term: str                # Canonical term
    definition: str          # Term definition
    category: str            # Category (e.g., "Intake & Coordination")
    aliases: list[str]       # Alternative names
    related: list[str]       # Related terms
    sap_reference: str|None  # Related SAP ID
    examples: list[str]      # Usage examples
```

**Search Modes**:
1. **Exact match** (score 1.0): Query == term (case-insensitive)
2. **Contains** (score 0.8): Query is substring of term
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
    print(f"  Related: {', '.join(entry.related)}")
```

**Additional Methods**:
- `reverse_search(definition_fragment)`: Find term by definition content
- `get_related(term)`: Get related terms for exploration
- `by_category(category)`: Get all terms in category
- `by_sap(sap_id)`: Get all terms related to SAP

**Glossary Structure**: `docs/GLOSSARY.md`

**Entry Format**:
```markdown
### Coordination Request
Type 2 intake for cross-repo dependencies or blocking work reviewed during sprint planning (every 2 weeks).

**Aliases:** Type 2 intake, coord-NNN
**Related:** Strategic Proposal, Implementation Task
**SAP:** SAP-001
**File:** inbox/incoming/coordination/
**Example:** Coordinating testing improvements between chora-base and chora-compose
```

**Graceful Degradation**: If script not available, direct users to `docs/GLOSSARY.md`

### 6.5 Suggestion Engine Contract

**Script**: `scripts/suggest-next.py`

**Purpose**: Generate context-aware next action suggestions based on project state

**Input**: Project context (current state), mode ("reactive" | "proactive")

**Output**: List of `Suggestion` objects, sorted by priority

**Suggestion Structure**:
```python
class Suggestion:
    action: str            # Suggested action description
    rationale: str         # Why this suggestion makes sense
    priority: str          # "high" | "medium" | "low"
    category: str          # "workflow" | "quality" | "planning" | "learning"
    estimated_effort: str  # Time estimate (e.g., "5-10 minutes")
```

**Suggestion Modes**:
- **Reactive**: Return top 5 suggestions across all priorities (user asked "what should I do")
- **Proactive**: Return only high-priority suggestions (user didn't ask, but should know)

**Context Sources**:
- **Inbox status**: Pending coordination requests, active blockers (from `ECOSYSTEM_STATUS.yaml`)
- **Sprint phase**: Planning, development, testing, review (from sprint plan files)
- **Quality metrics**: Test coverage, broken links, lint errors (from pytest/ruff output)
- **Documentation state**: Missing files, outdated content (from file system analysis)

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
- **Inbox protocol (SAP-001)**: Suggest reviewing pending requests when `status: pending_triage`
- **Development lifecycle (SAP-012)**: Suggest next phase based on current sprint plan
- **Testing framework (SAP-004)**: Suggest improving coverage if <85%
- **Documentation framework (SAP-007)**: Suggest fixing broken links if validation fails

**Graceful Degradation**: If script not available, agents rely on documented workflows

### 6.6 User Preferences Contract

**Configuration File**: `.chora/user-preferences.yaml`

**Template**: `.chora/user-preferences.yaml.template` (100+ options)

**Purpose**: Enable user-specific agent behavior adaptation

**Configuration Categories**:

**1. Communication** (verbosity, formality, output_format):
```yaml
communication:
  verbosity: standard  # concise|standard|verbose
  formality: standard  # casual|standard|formal
  output_format: terminal  # terminal|markdown|json
```

**2. Workflow** (confirmation, automation, disclosure):
```yaml
workflow:
  require_confirmation: destructive  # always|destructive|never
  auto_commit: false
  progressive_disclosure: true
```

**3. Learning** (pattern capture, suggestions, usage tracking):
```yaml
learning:
  capture_patterns: true
  suggest_improvements: true
  track_usage: true
```

**4. Expertise** (assume_knowledge, explain_rationale, show_alternatives):
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

# Adapt verbosity
if prefs['communication']['verbosity'] == 'verbose':
    response += detailed_explanation()
    response += examples()
elif prefs['communication']['verbosity'] == 'concise':
    response = summarize(response)

# Adapt confirmation behavior
if prefs['workflow']['require_confirmation'] == 'always':
    confirm_before_action()
elif prefs['workflow']['require_confirmation'] == 'destructive':
    if action_is_destructive():
        confirm_before_action()
```

**Graceful Degradation**: If preferences file missing, use defaults from template

### 6.7 Integration with Existing SAP-009 Patterns

**Bidirectional translation layer EXTENDS, not replaces, existing patterns**:

**1. AGENTS.md/CLAUDE.md dual-file pattern** (Section 2):
- Bidirectional tools discoverable via root AGENTS.md
- Domain-specific user signals in nested AGENTS.md files
- Progressive context loading remains primary mechanism

**2. "Nearest File Wins"** (Section 3):
- Domain AGENTS.md files can override root intent patterns
- Allows domain-specific translations (e.g., testing → pytest-specific actions)

**3. Progressive Context Loading** (Section 4):
- **Phase 1 (Always Load)**: Root AGENTS.md includes tool discovery
- **Phase 2 (Load on Demand)**: Domain AGENTS.md includes user signal patterns
- **Phase 3 (Complex Only)**: Full pattern database (INTENT_PATTERNS.yaml)

**4. Token Budgeting** (Section 4):
- Intent router: ~5-10k tokens (patterns + script)
- Glossary search: ~15-20k tokens (all terms)
- Suggestion engine: ~10-15k tokens (context analysis)
- **Total**: ~30-45k tokens (within 200k budget)

### 6.8 User Signal Patterns (Domain AGENTS.md Integration)

**Purpose**: Map conversational input to domain-specific formal actions

**Pattern**: Each domain AGENTS.md file includes a "User Signal Patterns" section

**Example Structure**:
```markdown
## User Signal Patterns

### Inbox Operations (SAP-001)

| User Says | Formal Action | Notes |
|-----------|---------------|-------|
| "show inbox" | run_inbox_status | Display dashboard |
| "what's pending" | list_pending_coordination_requests | Filter by status |
| "review coord-NNN" | open_coordination_request(id="coord-NNN") | Load specific request |
```

**Domain AGENTS.md Files Enhanced** (v1.1.0):
1. `docs/skilled-awareness/inbox-protocol/AGENTS.md` (SAP-001)
2. `docs/skilled-awareness/testing-framework/AGENTS.md` (SAP-004)
3. `docs/skilled-awareness/agent-awareness/AGENTS.md` (SAP-009)
4. `docs/skilled-awareness/development-lifecycle/AGENTS.md` (SAP-012)
5. `docs/skilled-awareness/metrics-framework/AGENTS.md` (SAP-013)

### 6.9 Progressive Formalization

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
  ...
}
Agent: *validates schema, creates request*
```

**Key**: User moves at their own pace; system supports all stages simultaneously

### 6.10 Anti-Patterns

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

### 6.11 Quality Gates

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

**BDD Scenarios**: 61 scenarios covering all capabilities

### 6.12 Versioning

- **SAP-009 v1.0.0**: AGENTS.md/CLAUDE.md dual-file pattern, progressive loading
- **SAP-009 v1.1.0**: Bidirectional translation layer (THIS ENHANCEMENT)
- **Future**: v1.2.0 could add voice-to-text translation, visual workflow builder

**Migration**: v1.0.0 → v1.1.0 is backward compatible (additive only, no breaking changes)

---

## 6.5. Self-Evaluation Criteria

### Awareness File Requirements (SAP-009 Phase 4)

**Both AGENTS.md and CLAUDE.md Required** (Equivalent Support):
- [ ] Both files exist in `docs/skilled-awareness/agent-awareness/`
- [ ] Both files have YAML frontmatter with progressive loading metadata
- [ ] Workflow coverage equivalent (±30%): AGENTS.md ≈ CLAUDE.md workflows

**Required Sections (Both Files)**:
- [ ] Overview / Quick Start for Claude
- [ ] User Signal Patterns / Common Workflows (AGENTS.md has pattern tables, CLAUDE.md has 4 workflows)
- [ ] Best Practices / Claude-Specific Tips (5 each)
- [ ] Common Pitfalls (5 each)
- [ ] Integration Patterns / Support & Resources

**Source Artifact Coverage (Both Files)**:
- [ ] capability-charter.md design principles → "Overview" section
- [ ] protocol-spec.md file structure/nearest-wins → "Nearest File Wins Pattern" section
- [ ] awareness-guide.md workflows → "Common Workflows" section
- [ ] adoption-blueprint.md installation → "Quick Reference" section
- [ ] ledger.md adoption tracking → referenced in "Best Practices"

**YAML Frontmatter Fields** (Required):
```yaml
sap_id: SAP-009
version: X.Y.Z
status: active | pilot | draft
last_updated: YYYY-MM-DD
type: reference
audience: agents | claude_code
complexity: beginner | intermediate | advanced
estimated_reading_time: N
progressive_loading:
  phase_1: "lines 1-X"
  phase_2: "lines X-Y"
  phase_3: "full"
phase_1_token_estimate: NNNN
phase_2_token_estimate: NNNN
phase_3_token_estimate: NNNN
```

**Validation Commands**:
```bash
# Check both files exist
test -f docs/skilled-awareness/agent-awareness/AGENTS.md && \
test -f docs/skilled-awareness/agent-awareness/CLAUDE.md

# Validate YAML frontmatter
grep -A 10 "^---$" docs/skilled-awareness/agent-awareness/AGENTS.md | grep "sap_id: SAP-009"
grep -A 10 "^---$" docs/skilled-awareness/agent-awareness/CLAUDE.md | grep "progressive_loading:"

# Check workflow count equivalence (should be within ±30%)
# Note: AGENTS.md uses user signal pattern tables, CLAUDE.md uses explicit workflows
agents_sections=$(grep -E "^### " docs/skilled-awareness/agent-awareness/AGENTS.md | wc -l)
claude_workflows=$(grep "^### Workflow" docs/skilled-awareness/agent-awareness/CLAUDE.md | wc -l)
echo "AGENTS sections: $agents_sections, CLAUDE workflows: $claude_workflows"

# Run comprehensive evaluation
python scripts/sap-evaluator.py --deep SAP-009
```

**Expected Workflow Coverage**:
- AGENTS.md: User signal pattern tables (Agent Discovery, Maintenance, Translation, Progressive Formalization)
- CLAUDE.md: 4 Claude Code workflows (Discover with Read, Progressive Loading, Create with Write, Optimize Token Usage)
- Rationale: Different organization acceptable - AGENTS.md uses pattern tables for quick lookup, CLAUDE.md uses detailed workflows showing Read/Write/Bash tool usage

---

## 7. Related Documents

**SAP-009 Artifacts**:
- [capability-charter.md](capability-charter.md)
- [awareness-guide.md](awareness-guide.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [ledger.md](ledger.md)

**Templates**:
- [blueprints/AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) (~900 lines)
- [blueprints/CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) (~450 lines)

**Examples**:
- [static-template/tests/AGENTS.md](/static-template/tests/AGENTS.md)
- [static-template/scripts/AGENTS.md](/static-template/scripts/AGENTS.md)
- [static-template/docker/AGENTS.md](/static-template/docker/AGENTS.md)

**Related SAPs**:
- [sap-framework/](../sap-framework/) - SAP-000
- [documentation-framework/](../documentation-framework/) - SAP-007

---

**Version History**:
- **2.1.0** (2025-11-10): Added nested structure support - frontmatter fields (nested_structure, nested_files), Section 4.4 Critical Workflows Pattern, updated status to Active (COORD-2025-012)
- **1.1.0** (2025-10-31): Added Section 6 (Bidirectional Translation Layer) - intent routing, glossary search, context-aware suggestions, user preferences, progressive formalization
- **1.0.0** (2025-10-28): Initial protocol specification for agent-awareness
