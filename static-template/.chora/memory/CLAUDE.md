# Claude Memory Integration Patterns

**Purpose:** Claude-specific patterns for A-MEM (Agentic Memory) integration and cross-session learning.

**Parent:** See [../../CLAUDE.md](../../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic memory guide.

---

## Claude + A-MEM Integration

Claude's 200k context window + A-MEM create powerful cross-session learning:

- **Session memory** (Claude's context) → **Persistent memory** (A-MEM)
- **Working knowledge** (current task) → **Permanent knowledge** (knowledge graph)
- **Ephemeral insights** (conversation) → **Distilled learnings** (structured notes)

---

## Memory Tier Strategy for Claude

### Tier 1: Claude's Context Window (Ephemeral)

**What:** Current conversation, working memory, active files

**Use for:**
- Current task execution
- Immediate problem-solving
- Active coding session

**Claude optimization:**
```markdown
"Load essential context:
- Current task: [description]
- Active files: [list]
- Recent decisions: [from checkpoint]

This is Tier 1 - ephemeral session memory."
```

### Tier 2: Event Log (Persistent Conversation)

**What:** Timestamped operation events, trace-correlated workflows

**Query pattern for Claude:**
```markdown
"Query recent failures to avoid repeating mistakes:

{{ project_slug }}-memory query --type app.failed --since 7d

Show me what failed recently so I don't repeat those approaches."
```

**Claude can learn from:**
- Past failures (what didn't work)
- Successful patterns (what did work)
- Performance data (how long things took)
- Debugging history (how issues were resolved)

### Tier 3: Knowledge Graph (Permanent Structural Knowledge)

**What:** Distilled learnings, proven solutions, architectural decisions

**Query pattern for Claude:**
```markdown
"Search knowledge graph before implementing:

{{ project_slug }}-memory knowledge search --tag [relevant-topic]

Have we solved this problem before? What did we learn?"
```

**Claude should create notes after:**
- Solving non-trivial problems
- Discovering important patterns
- Making architectural decisions
- Finding optimal solutions

---

## Progressive Memory Loading with Claude

### Pattern: Start Session with Memory Context

```markdown
# Session Start Pattern

"Starting work on [task]. Load memory context:

## Tier 1: Essential (Claude's Context)
- Task definition
- Active files
- Recent checkpoint: [path]

## Tier 2: Recent Events (Event Log)
# Load relevant recent events
{{ project_slug }}-memory query --type [relevant-type] --since 7d

## Tier 3: Proven Solutions (Knowledge Graph)
# Search for related learnings
{{ project_slug }}-memory knowledge search --tag [topic]

Synthesize these memory tiers to inform current task."
```

### Pattern: Query Before Solving

```markdown
# Before implementing new feature
"Before I implement [feature], search memory:

1. Has similar feature been built?
   {{ project_slug }}-memory knowledge search --tag [feature-type]

2. Were there past challenges?
   {{ project_slug }}-memory query --type feature.* --grep [keyword]

3. What patterns worked well?
   {{ project_slug }}-memory knowledge search --tag pattern

Use learnings to inform current implementation."
```

---

## Event Log Integration

### Creating Events During Development

**Pattern: Log significant operations**

```bash
# After implementing feature
{{ project_slug }}-memory log \
  --type feature.implemented \
  --trace-id $(uuidgen) \
  --message "Implemented [feature]" \
  --metadata '{"lines": 250, "tests": 15, "time_hours": 3}'
```

**Claude can request logging:**
```markdown
"After completing this implementation, log to event system:

{{ project_slug }}-memory log --type feature.implemented \\
  --message \"Implemented [feature] with [approach]\" \\
  --metadata '{\"coverage\": 0.92, \"time_saved\": 120}'
```

### Querying Events for Context

**Pattern: Analyze failure patterns**

```markdown
"Analyze recent test failures to identify patterns:

{{ project_slug }}-memory query --type test.failed --since 30d

Common causes:
- [Pattern 1]
- [Pattern 2]

Avoid these in current test implementation."
```

**Pattern: Learn from successful implementations**

```markdown
"How have we successfully implemented similar features?

{{ project_slug }}-memory query --type feature.implemented \\
  --grep [keyword] --since 90d

Extract successful patterns and apply to current task."
```

---

## Knowledge Graph Integration

### Creating Knowledge Notes

**Pattern: After solving problem**

```markdown
"Problem solved. Create knowledge note:

{{ project_slug }}-memory knowledge create \\
  \"Solution to [problem]\" \\
  --tag problem-type \\
  --tag solution-pattern \\
  --confidence 0.9 \\
  <<EOF
Problem: [Description]

Solution: [Approach that worked]

Why it works: [Explanation]

When to use: [Conditions]

Alternatives considered: [Other approaches and why rejected]

Evidence: [Results, metrics]
EOF

This ensures we don't solve the same problem twice."
```

**Claude prompt pattern:**
```markdown
"We solved [problem] using [approach]. Create knowledge note for future reference:

Title: [descriptive title]
Tags: [relevant tags]
Content:
- What: [what problem was solved]
- How: [solution approach]
- Why: [rationale]
- When: [when to use this pattern]
- Evidence: [that it worked]
```

### Searching Knowledge Graph

**Pattern: Before starting new work**

```markdown
"Query knowledge graph for relevant patterns:

{{ project_slug }}-memory knowledge search --tag [topic]

Review existing knowledge:
- [Note 1]: [summary]
- [Note 2]: [summary]

Apply relevant patterns to current task."
```

**Pattern: Discover related knowledge**

```markdown
"Find knowledge related to [topic]:

{{ project_slug }}-memory knowledge search \\
  --tag [primary-tag] \\
  --text [keyword]

Load top 3 most relevant notes into context.
Identify patterns applicable to current task."
```

---

## Checkpoint + Memory Integration

### Enhanced Checkpoint with Memory References

```markdown
# CLAUDE_CHECKPOINT.md (Memory-Enhanced)

## Session Metadata
[Standard checkpoint fields...]

## Memory Integration

### Knowledge Referenced
- [[knowledge-note-id-1]]: [Note title]
  - Applied pattern: [which pattern]
  - Result: [outcome]

- [[knowledge-note-id-2]]: [Note title]
  - Applied pattern: [which pattern]
  - Result: [outcome]

### Events Logged
- [event-id-1]: feature.implemented
- [event-id-2]: bug.fixed

### Queries Performed
```bash
# Queries that informed this session
{{ project_slug }}-memory query --type bug.* --since 30d
{{ project_slug }}-memory knowledge search --tag error-handling
```

### New Knowledge Created
- [[new-note-id]]: [Title]
  - Tags: [tags]
  - Confidence: [score]

## Next Session Memory Load
To resume this work:
1. Load this checkpoint
2. Query: `{{ project_slug }}-memory query --trace-id [session-trace-id]`
3. Load knowledge: [[knowledge-ids]]
```

---

## Cross-Session Learning Patterns

### Pattern 1: Avoid Repeated Mistakes

```markdown
# Before attempting risky operation
"Check if this has failed before:

{{ project_slug }}-memory query --type operation.failed \\
  --grep [operation-keyword] \\
  --since 90d

If similar failures exist:
1. Review failure reasons
2. Identify what was learned
3. Apply learnings to avoid repeating

If no failures found:
- Proceed with caution
- Log detailed events if it fails
- Create knowledge note if solved
```

### Pattern 2: Reuse Proven Solutions

```markdown
# Before implementing solution
"Search for proven solutions to similar problems:

{{ project_slug }}-memory knowledge search \\
  --tag solution-pattern \\
  --tag [problem-domain]

If proven solution exists:
1. Review approach
2. Adapt to current context
3. Apply with confidence
4. Update knowledge note with new application

If no solution found:
- Experiment carefully
- Document extensively
- Create knowledge note when successful
```

### Pattern 3: Track Decision Evolution

```markdown
# When reconsidering past decision
"Review history of decisions on [topic]:

{{ project_slug }}-memory knowledge search --tag decision \\
  --text [topic]

Trace evolution:
- Initial decision: [when, what, why]
- Revisions: [when, what changed, why]
- Current state: [what we think now]

Document new decision as knowledge note with history context."
```

---

## Memory-Driven Development Workflow

### Workflow Integration

**Phase 1: Planning (Memory Query)**
```markdown
Before planning [feature]:
1. Query past similar features
2. Review architectural decisions
3. Check for known issues/patterns
4. Load relevant knowledge into context
```

**Phase 2: Design (Memory-Informed)**
```markdown
During design of [feature]:
1. Reference proven patterns from knowledge graph
2. Avoid known anti-patterns from event log
3. Consider past architectural decisions
4. Document design decisions as knowledge
```

**Phase 3: Implementation (Memory-Guided)**
```markdown
During implementation:
1. Apply patterns from knowledge graph
2. Avoid approaches that failed before
3. Log significant operations to event log
4. Track progress with trace IDs
```

**Phase 4: Retrospective (Memory Creation)**
```markdown
After completing [feature]:
1. Create knowledge notes for learnings
2. Log success/failure to event log
3. Update related knowledge notes
4. Link knowledge notes (Zettelkasten style)
```

---

## Context Preservation with Memory System

### When Context Gets Full, Preserve to Memory

```markdown
# Before pruning Claude's context
"Context approaching limit. Preserve to memory:

1. Create checkpoint: .chora/memory/claude-checkpoints/[date].md
2. Extract key learnings:
   - [Learning 1]: Create knowledge note
   - [Learning 2]: Create knowledge note
3. Log session metrics to event log
4. Reference knowledge IDs in checkpoint

After pruning, checkpoint + memory queries restore context."
```

---

## Memory Metrics for Claude

### Track Memory System Effectiveness

```markdown
# In checkpoint or session summary

## Memory System Metrics

**Queries:**
- Knowledge queries: 5
- Event queries: 3
- Hits: 6 relevant results

**Knowledge Created:**
- New notes: 2
- Updated notes: 1
- Links created: 3

**Value:**
- Solutions reused: 2 (saved ~4 hours)
- Mistakes avoided: 1 (saved ~2 hours)
- Patterns applied: 3

**Quality:**
- Knowledge confidence: 0.85 avg
- Query relevance: 0.90
```

---

## Common Memory Patterns for {{ project_name }}

### Pattern: MCP Tool Development

```bash
# Before implementing MCP tool
{{ project_slug }}-memory knowledge search --tag mcp-tool

# After implementing successfully
echo "MCP tool pattern: [description of pattern]" | \\
  {{ project_slug }}-memory knowledge create \\
  "MCP Tool: [tool-name] Implementation" \\
  --tag mcp-tool --tag [domain]
```

### Pattern: API Integration

```bash
# Before integrating with external API
{{ project_slug }}-memory knowledge search --tag api-integration --tag [api-name]

# Document integration learnings
{{ project_slug }}-memory knowledge create \\
  "API Integration: [api-name]" \\
  --tag api-integration \\
  --tag [api-name] \\
  --tag rate-limiting  # If relevant
```

### Pattern: Bug Resolution

```bash
# Search for similar past bugs
{{ project_slug }}-memory query --type bug.* --grep [error-keyword]

# After fixing, log resolution
{{ project_slug }}-memory log --type bug.fixed \\
  --message "Fixed [bug]: [solution]"

# Create knowledge note for complex bugs
echo "Bug fix: [description]" | \\
  {{ project_slug }}-memory knowledge create \\
  "Bug Fix: [title]" --tag bug-fix --tag [category]
```

---

## Best Practices: Claude + Memory

### ✅ Do's

1. **Query before solving** - Check memory for existing solutions
2. **Create notes after success** - Preserve learnings
3. **Use trace IDs** - Link related events across sessions
4. **Reference in checkpoints** - Link checkpoints to knowledge
5. **Tag consistently** - Makes knowledge discoverable
6. **Update confidence** - Refine knowledge over time
7. **Link related notes** - Build knowledge graph connections

### ❌ Don'ts

1. **Don't skip queries** - You might repeat solved problems
2. **Don't create duplicate notes** - Search first, update if exists
3. **Don't use vague tags** - Specific tags enable better search
4. **Don't forget trace IDs** - Loses multi-step context
5. **Don't hoard ephemeral** - Not everything needs permanent storage
6. **Don't ignore low confidence** - Low confidence notes need refinement

---

**See Also:**
- [../../CLAUDE.md](../../CLAUDE.md) - Project-level Claude patterns
- [AGENTS.md](AGENTS.md) - Generic memory system guide
- [../../claude/CHECKPOINT_PATTERNS.md](../../claude/CHECKPOINT_PATTERNS.md) - Checkpoint integration
- [../../claude/CONTEXT_MANAGEMENT.md](../../claude/CONTEXT_MANAGEMENT.md) - Context + memory strategies

---

**Version:** 3.3.0
**Last Updated:** 2025-10-26
