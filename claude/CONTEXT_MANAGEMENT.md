# Context Management for Claude

**Purpose:** Optimize Claude's 200k token context window for efficient, long-duration development sessions.

**Problem Solved:** Context overload, information loss, inefficient token usage, degraded response quality.

---

## Overview

Claude's 200k token context window is powerful but requires strategic management. Poor context management leads to:

- **Information overload** - Too much irrelevant context confuses focus
- **Response degradation** - Quality decreases as context fills
- **Context loss** - Important details pushed out by noise
- **Inefficiency** - Wasted tokens on unused information

**This guide provides:** Progressive loading strategies, context pruning techniques, and memory preservation patterns.

---

## Progressive Context Loading Strategy

Load context in phases based on task complexity and session progress.

### Phase 1: Essential Context (0-10k tokens)

**Target:** Immediate task execution
**When:** Session start, new task, quick fixes
**Contents:**

```markdown
## Essential Context Package (0-10k tokens)

### 1. Current Task Definition (500-1k tokens)
- Task description
- Success criteria
- Constraints and requirements

### 2. Active File Contents (2-5k tokens)
- 1-3 files you're currently modifying
- Related test files
- Configuration files (if relevant)

### 3. Relevant AGENTS.md Section (1-2k tokens)
- Project overview
- Architecture diagram
- Key conventions

### 4. Recent Conversation Summary (0-2k tokens)
- Last 5-10 interactions (if continuing session)
- Key decisions made
- Blockers encountered
```

**Load command pattern:**
```markdown
"Current task: Implement [feature]

Active files:
1. src/module.py (current implementation)
2. tests/test_module.py (existing tests)

Project context: See AGENTS.md - We're building an MCP server using FastMCP.

Success criteria: [specific criteria]"
```

### Phase 2: Extended Context (10-50k tokens)

**Target:** Complex implementation, refactoring
**When:** Multi-file changes, architectural work
**Contents:**

```markdown
## Extended Context Package (10-50k tokens)

### 1. Essential Context (from Phase 1)

### 2. Related Module Code (5-15k tokens)
- Modules that interact with current work
- Shared utilities
- Base classes/interfaces

### 3. Test Suites (3-10k tokens)
- Full test suite for affected components
- Integration tests
- Fixtures and mocks

### 4. Recent Git History (2-5k tokens)
git log --oneline --no-merges -20
git diff HEAD~5..HEAD --stat

### 5. Related Documentation (3-10k tokens)
- API documentation
- Architecture decision records
- Relevant workflow docs (DDD, BDD, TDD)
```

**Load command pattern:**
```markdown
"Continuing [feature] work. Extended context needed:

Core files: [list]
Related modules: [list]
Test suite: tests/[path]

Recent changes: $(git log --oneline -10)

References:
- dev-docs/workflows/DDD_WORKFLOW.md (documentation approach)
- Architecture: [specific section from AGENTS.md]"
```

### Phase 3: Full Context (50-200k tokens)

**Target:** Large-scale refactoring, architecture overhaul
**When:** Rare - only for project-wide changes
**Contents:**

```markdown
## Full Context Package (50-200k tokens)

### 1. Extended Context (from Phase 2)

### 2. Complete Codebase Structure (20-50k tokens)
```bash
tree -L 3 -I '__pycache__|*.pyc|.git'
```

### 3. Full Test Suite (10-30k tokens)
- All test files
- Coverage reports
- Integration test scenarios

### 4. All Documentation (10-40k tokens)
- README.md
- All dev-docs/
- All AGENTS.md files
- Workflow documentation

### 5. Historical Decisions (5-20k tokens)
- Knowledge graph notes
- Past architectural decisions
- Refactoring history
- Bug pattern analysis

### 6. Dependencies & Configuration (5-15k tokens)
- pyproject.toml
- All config files
- Environment setup docs
```

**Load command pattern:**
```markdown
"Major refactoring: [description]

Need full codebase context:

1. Project structure: $(tree -L 3)
2. All source files: src/
3. All tests: tests/
4. All docs: dev-docs/, README.md
5. Configuration: pyproject.toml, all config files

Historical context:
- Knowledge graph: $(project-memory knowledge search --tag refactoring)
- Past decisions: [specific ADRs]

This is a large-scale change affecting multiple modules."
```

---

## Context Pruning Strategies

When context approaches limits (150k+ tokens), prune strategically.

### Automatic Pruning Triggers

**Signs you need to prune:**
- Responses slowing down (>30 seconds)
- Claude asking for clarification on recently discussed topics
- Repeated information in responses
- Loss of conversation focus

### Pruning Priority (Keep → Remove)

**KEEP (High Priority):**
1. Current task definition
2. Active file contents (files being edited)
3. Recent decisions (last 10 interactions)
4. Error messages and stack traces
5. Key architecture constraints

**REDUCE (Medium Priority):**
6. Related module code → Keep only signatures, remove implementations
7. Test suites → Keep failing tests, remove passing
8. Git history → Keep last 5 commits, remove older
9. Documentation → Keep TOC and summaries, remove details

**REMOVE (Low Priority):**
10. Completed tasks and their discussions
11. Exploratory conversations that didn't lead anywhere
12. Duplicate information
13. Historical context no longer relevant
14. Full file contents of unchanged modules

### Pruning Command Pattern

```markdown
"Context is getting full. Let's prune to essentials:

KEEP:
- Current task: [task]
- Active files: [list]
- Last 5 decisions: [list]

REMOVE:
- Completed tasks: [list]
- Exploratory discussion on [topic] (decided against)
- Full contents of unchanged modules

SUMMARIZE:
- Git history: Last 5 commits only
- Test suite: Failing tests only
- Related modules: Signatures only, not implementations

Checkpoint saved at: .chora/memory/claude-checkpoints/YYYY-MM-DD.md"
```

---

## Token Budget Management

Track and allocate tokens strategically.

### Token Estimation Guidelines

| Content Type | Tokens (approx) |
|--------------|-----------------|
| 1 line of Python code | 10-15 tokens |
| 1 markdown paragraph | 50-100 tokens |
| 1 small function (10 lines) | 100-150 tokens |
| 1 medium function (50 lines) | 500-750 tokens |
| 1 test file (~100 lines) | 1,000-1,500 tokens |
| 1 module (~500 lines) | 5,000-7,500 tokens |
| Full git log (50 commits) | 2,000-3,000 tokens |

### Budget Allocation Strategy

**For 200k token window:**

```markdown
## Token Budget Allocation

Phase 1: Essential (0-10k)
- Task definition: 1k
- Active files (2-3): 4-6k
- AGENTS.md excerpt: 2k
- Recent context: 1-2k

Phase 2: Extended (10-50k)
- Essential: 10k (carried over)
- Related modules: 15k
- Test suite: 10k
- Git history: 3k
- Documentation: 10k

Phase 3: Full (50-200k)
- Extended: 50k (carried over)
- Complete codebase: 50k
- All tests: 30k
- All docs: 40k
- Historical: 20k
- Reserve: 10k (breathing room)
```

### Monitoring Token Usage

**Request a token count:**
```markdown
"Can you estimate our current context usage in tokens?"
```

**Claude will estimate based on:**
- Conversation length
- Code files loaded
- Documentation referenced

---

## Memory Preservation Techniques

Preserve important context when pruning or ending sessions.

### Technique 1: Progressive Summarization

After every 10 interactions:

```markdown
## Session Summary (Auto-generated every 10 interactions)

**Tasks Completed:**
1. [Task 1]: [outcome]
2. [Task 2]: [outcome]

**Key Decisions:**
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

**Current State:**
- Working file: [path]
- Next step: [specific action]

**Learnings:**
- [Pattern/insight discovered]
```

### Technique 2: Checkpoint Files

At end of session or before major context changes:

```markdown
# Claude Session Checkpoint
# File: .chora/memory/claude-checkpoints/2025-10-26-feature-auth.md

## Session Metadata
- Date: 2025-10-26
- Duration: 3 hours
- Task: Implement OAuth2 authentication

## Completed Work
✅ Designed OAuth2 flow (see dev-docs/design/oauth2-flow.md)
✅ Implemented authorization endpoint (src/auth/oauth.py)
✅ Added tests for happy path (tests/test_oauth.py)

## In Progress
🔄 Error handling for OAuth failures (50% complete)
- Implemented: Invalid token, expired token
- Remaining: Network errors, provider failures

## Key Decisions
1. **Use oauthlib library**: More secure than custom implementation
   - Rationale: Battle-tested, handles edge cases

2. **Store tokens in memory only**: No persistence initially
   - Rationale: Simplifies first iteration, add persistence in v2

## Code State
```python
# src/auth/oauth.py
# Lines 1-150: Complete
# Lines 151-200: Error handling (in progress)
# TODO: Add network timeout handling (line 175)
```

## Next Steps
1. Complete error handling (1-2 hours)
2. Add integration tests (1 hour)
3. Update documentation (30 min)
4. Code review with team

## Context to Load for Continuation
- Essential: src/auth/oauth.py, tests/test_oauth.py
- Reference: dev-docs/design/oauth2-flow.md
- Dependencies: oauthlib docs (web search if needed)

## Known Issues
- Test flakiness in test_token_refresh (line 234)
- Need to mock time.sleep() for faster tests
```

**Save to:** `.chora/memory/claude-checkpoints/[date]-[feature].md`

### Technique 3: Knowledge Graph Integration

Distill session learnings into permanent knowledge:

```bash
# After solving non-trivial problem
echo "OAuth2 implementation pattern: Use oauthlib for security. \
Store tokens in-memory initially. Add network timeout handling. \
Test with mocks for external provider." | \
  project-memory knowledge create "OAuth2 Implementation Pattern" \
  --tag authentication --tag oauth2 --tag best-practice
```

**Query in future sessions:**
```bash
project-memory knowledge search --tag authentication
```

---

## Context Loading Patterns by Task Type

### Pattern: Quick Bug Fix (Phase 1)

```markdown
"Quick bug fix needed:

Bug: [description]
Error: [stack trace]

Context needed:
- File with bug: [path]
- Relevant test: [path]
- Recent changes: $(git log --oneline -5)

No need for full context - this is isolated."
```

### Pattern: New Feature (Phase 2)

```markdown
"New feature: [name]

Design complete: dev-docs/design/[feature].md

Context needed:
- Related modules: [list]
- Similar existing features: [list]
- Test suite for [module]: tests/[path]
- Workflow: dev-docs/workflows/DDD_WORKFLOW.md

Architecture: See AGENTS.md section on [relevant area]"
```

### Pattern: Large Refactoring (Phase 3)

```markdown
"Major refactoring: [description]

This will affect multiple modules across the codebase.

Load full context:
1. All source: src/
2. All tests: tests/
3. Architecture docs: AGENTS.md, dev-docs/architecture/
4. Past refactorings: $(git log --grep='refactor' --oneline -10)

Checkpoint saved: .chora/memory/claude-checkpoints/[date]-refactor.md

This is a multi-session task - using checkpoint for continuity."
```

---

## Best Practices

### ✅ Do's

1. **Start small** - Begin with Phase 1, expand only if needed
2. **Create checkpoints** - Every 10 interactions or end of session
3. **Prune proactively** - Don't wait for context to fill completely
4. **Summarize frequently** - After completing subtasks
5. **Use knowledge graph** - Distill learnings for future sessions
6. **Monitor quality** - If responses degrade, prune context

### ❌ Don'ts

1. **Front-load everything** - Don't dump entire codebase immediately
2. **Ignore token budget** - Track and manage context size
3. **Skip checkpoints** - Leads to context loss and rework
4. **Keep completed work** - Prune finished tasks from context
5. **Repeat information** - Reference once, don't reload unnecessarily
6. **Lose decisions** - Always record key decisions before pruning

---

## Troubleshooting

### Problem: Responses Getting Slow

**Diagnosis:** Context overload (150k+ tokens)

**Solution:**
1. Prune low-priority content
2. Summarize completed work
3. Remove duplicate information
4. Keep only active files in full

### Problem: Claude Losing Track of Recent Decisions

**Diagnosis:** Important context pruned too aggressively

**Solution:**
1. Create checkpoint with decisions
2. Keep "Key Decisions" summary in context
3. Reference checkpoint in next request

### Problem: Need to Resume After Break

**Diagnosis:** Fresh session, no context

**Solution:**
1. Load checkpoint file
2. Summarize in request: "Continuing from checkpoint: [summary]"
3. Add only essential Phase 1 context
4. Expand to Phase 2 if needed

---

## Metrics

**Track these to optimize:**

- **Context efficiency** = Tokens used / Tokens needed
  - Target: >0.7 (70%+ of context is relevant)

- **Pruning frequency** = Pruning events / Session duration
  - Target: 1 prune per 2-3 hours

- **Checkpoint quality** = Successful resumes / Total resumes
  - Target: >0.9 (90%+ successful continuations)

---

## Integration with Other Patterns

**With Checkpoints:** Create checkpoint before pruning - preserves full context
**With Metrics:** Track context efficiency as ROI metric
**With Templates:** Include context requirements in task templates

---

## SAP-Specific Context Management

### Overview

Skilled Awareness Packages (SAPs) introduce structured capability packaging. Use these optimized loading patterns when working with SAPs.

**Related**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

### Essential Context for SAP Work (10-15k tokens)

**When Creating a SAP**:
```markdown
Phase 1: Load Framework (5k tokens)
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [document-templates.md](../docs/reference/skilled-awareness/document-templates.md)

Phase 2: Load Reference Implementation (10k tokens)
- [inbox SAP](../docs/reference/skilled-awareness/inbox/) (all 5 artifacts)
- Study structure, patterns, tone

Phase 3: Create Artifacts (progressive)
- Start with Charter (understand problem)
- Add Protocol (define contract)
- Add Awareness, Blueprint, Ledger
- Total: ~15-20k tokens of new content
```

**When Installing a SAP**:
```markdown
Essential Load (2-4k tokens)
- Target SAP's adoption-blueprint.md
- Validation commands section

Extended Load (3-5k tokens, if needed)
- Target SAP's protocol-spec.md
- Prerequisites and dependencies
```

### Token Budget by SAP Activity

| Activity | Essential | Extended | Full | Notes |
|----------|-----------|----------|------|-------|
| Create SAP | 5k | 15k | 30k | Essential: protocol + templates |
| Install SAP | 2k | 5k | 10k | Essential: blueprint only |
| Upgrade SAP | 3k | 8k | 15k | Essential: upgrade blueprint + current protocol |
| Understand SAP | 1k | 3k | 8k | Essential: charter only |

### Progressive Loading: Creating a SAP

**Step 1: Understand Framework (5k tokens)**
```
Read: SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
Skip: Examples, optional sections
Focus: SAP structure, 5 artifacts, installation pattern
```

**Step 2: Study Reference (10k tokens)**
```
Read: inbox SAP (all 5 artifacts)
Skip: Infrastructure files, examples
Focus: Artifact structure, writing style, frontmatter
```

**Step 3: Load Templates (4k tokens)**
```
Read: document-templates.md
Skip: Already familiar sections
Focus: Template for current artifact
```

**Step 4: Create Artifact (progressive)**
```
Charter: 3-5k tokens
Protocol: 5-8k tokens
Awareness: 4-6k tokens
Blueprint: 4-6k tokens
Ledger: 2-3k tokens
Total: 18-28k tokens (created content)
```

**Total Context**: ~19-37k tokens (input) + 18-28k tokens (output) = 37-65k tokens

**Optimization**: Drop templates after reading, drop reference after patterns understood

### Progressive Loading: Installing a SAP

**Step 1: Find SAP (minimal)**
```
Read: docs/reference/skilled-awareness/INDEX.md (skim, 1k tokens)
Locate target SAP directory
```

**Step 2: Read Blueprint (2-4k tokens)**
```
Read: <sap>/adoption-blueprint.md
Skip: Background, examples (unless needed)
Focus: Prerequisites, installation steps, validation
```

**Step 3: Execute (minimal additional context)**
```
Load: Only infrastructure files as needed
Execute: Step-by-step from blueprint
Validate: Commands from blueprint
```

**Total Context**: ~3-5k tokens (most of session)

**Optimization**: Blueprint is self-contained, minimal dependencies

### Context Pruning for SAPs

**What to Keep**:
- Current artifact being created/edited
- SAP protocol (if creating SAP)
- Blueprint steps (if installing SAP)
- Validation commands

**What to Drop**:
- Completed artifact sections
- Reference SAP infrastructure
- Examples (unless actively referencing)
- Template sections already applied

**Example Pruning Strategy (Creating SAP)**:
```
Token Budget: 50k used, need to prune

Keep:
- Current artifact (Charter, 4k tokens)
- Protocol (5k tokens, reference)
- Templates (2k tokens, current section)
Total kept: 11k tokens

Drop:
- Previous conversation (15k tokens)
- Reference SAP infrastructure (10k tokens)
- Example projects (14k tokens)
Total dropped: 39k tokens

Result: 11k tokens, 39k freed
```

### SAP Workflow Context Patterns

**Pattern 1: Create SAP (DDD → BDD → TDD)**

```
DDD Phase:
  Load: Protocol (5k), Templates (2k), Charter template (1k)
  Output: Charter (3-5k) + Protocol (5-8k)
  Context: ~18k tokens

BDD Phase:
  Load: Charter (4k), Protocol (6k), BDD examples (3k)
  Output: Feature files (2-3k, optional for SAPs)
  Context: ~15k tokens

TDD Phase:
  Load: Charter (4k), Protocol (6k), Blueprint template (2k)
  Output: Infrastructure + Awareness (4-6k) + Blueprint (4-6k) + Ledger (2-3k)
  Context: ~28k tokens
```

**Pattern 2: Install SAP**

```
Read Blueprint → Execute Steps → Validate → Update Ledger
Context: 3-5k tokens (entire workflow)
```

**Pattern 3: Upgrade SAP**

```
Check Version → Find Upgrade Blueprint → Execute → Validate → Update Ledger
Context: 5-8k tokens (includes upgrade notes + rollback)
```

### Multi-SAP Context Management

**Scenario**: Working with multiple SAPs simultaneously (e.g., dependencies)

**Strategy**:
1. **Primary SAP**: Full context (Charter + Protocol + current artifact)
2. **Dependency SAPs**: Protocol only (reference)
3. **Future SAPs**: INDEX.md summary only

**Example** (creating testing-framework SAP, depends on project-bootstrap):
```
Primary (testing-framework):
  - Charter (draft, 4k)
  - Protocol (draft, 6k)
  - Templates (2k)
  Total: 12k tokens

Dependency (project-bootstrap):
  - Protocol only (5k)
  Total: 5k tokens

Context total: 17k tokens
```

### SAP Index as Context Hub

**Use SAP Index for quick reference**:
- Load once at session start (5k tokens)
- Reference throughout session
- Don't reload unless checking dependencies

**Pattern**:
```
Session start: Load INDEX.md
Throughout: Reference in memory
Session end: Update if SAPs created
```

### Context Checkpoints for SAPs

**Checkpoint after completing each artifact**:
```
After Charter: Checkpoint with "Charter complete"
After Protocol: Checkpoint with "Protocol complete"
After Awareness: Checkpoint with "Awareness complete"
After Blueprint: Checkpoint with "Blueprint complete"
After Ledger: Checkpoint with "SAP complete"
```

**Benefit**: Can resume SAP creation from any artifact

**Recovery Pattern**:
```
Resume: Load checkpoint
Identify: Last completed artifact
Load: Current artifact template only
Continue: Next artifact
```

---

**See Also:**
- [CHECKPOINT_PATTERNS.md](CHECKPOINT_PATTERNS.md) - State preservation strategies
- [FRAMEWORK_TEMPLATES.md](FRAMEWORK_TEMPLATES.md) - Task templates with context specs
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - SAP protocol
- [docs/reference/skilled-awareness/INDEX.md](../docs/reference/skilled-awareness/INDEX.md) - SAP registry
- [docs/reference/skilled-awareness/sap-framework/awareness-guide.md](../docs/reference/skilled-awareness/sap-framework/awareness-guide.md) - SAP agent guidance

---

**Version:** 3.3.0 + SAP Framework v1.0.0
**Pattern Maturity:** ⭐⭐⭐ Production-ready
**Last Updated:** 2025-10-27
