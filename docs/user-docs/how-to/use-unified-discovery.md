# How to Use Unified Discovery System (FEAT-002)

**For**: AI agents and developers working with chora-base projects
**Time**: ~10 minutes to learn, 60-80% faster context loading thereafter
**Goal**: Use intelligent query routing to find code, patterns, history, and automation 60-80% faster than traditional grep/glob

**Last Updated**: 2025-11-20 (FEAT-002 promotion to chora-base)

---

## Overview

The Unified Discovery System (FEAT-002) intelligently routes your queries to the optimal information source, saving 65-82% tokens and 60-80% time compared to traditional grep/glob discovery.

**What you'll learn**:
1. How discovery routing works (2 minutes)
2. 4 query types and when to use each (3 minutes)
3. Hands-on examples (5 minutes)
4. Advanced features and troubleshooting (2 minutes)

**Token Savings**: 15,000 tokens average per query (20-40k → 5-8k)
**Speed**: 0.087s average (344x faster than manual exploration)
**Accuracy**: 96.8% routing accuracy (validated on 31 diverse queries)

---

## How Discovery Routing Works (2 minutes)

### The Problem

Traditional discovery approaches are inefficient:
- **grep/glob all files**: 20-40k tokens, 3-5 minutes, loads irrelevant context
- **Manual exploration**: 5-10 minutes guessing which files to read
- **Loading everything**: 150k+ tokens for comprehensive context

### The Solution

Unified Discovery classifies your query into 1 of 4 types and routes to the optimal source:

| Query Type | Routes To | Token Est | Example Query |
|------------|-----------|-----------|---------------|
| **CODE_FEATURE** | Feature Manifest → Grep | 5-8k (80% savings) | "show me authentication code" |
| **PATTERN_CONCEPT** | Knowledge Graph → Manifest | 10-15k (75% savings) | "how do we handle async testing?" |
| **HISTORICAL_EVENT** | Event Logs → Knowledge | 8-12k (70% savings) | "when did we complete SAP-015 L4?" |
| **AUTOMATION_RECIPE** | Justfile → Scripts | 1-5k (93% savings) | "how do I run SAP metrics?" |

**Key Insight**: Different query types need different sources. Discovery routes intelligently so you load exactly what you need.

---

## Prerequisites (1 minute)

### Required Files (Recommended)

Unified Discovery works best with these project structures:

1. **Feature Manifest** (for CODE_FEATURE queries):
   ```bash
   feature-manifest.yaml  # SAP-056 lifecycle traceability
   ```
   *Fallback: glob search of src/, lib/, packages/ (60-70% accuracy)*

2. **Knowledge Graph** (for PATTERN_CONCEPT queries):
   ```bash
   .chora/memory/knowledge/notes/  # Markdown notes with patterns
   ```
   *Fallback: docs/ markdown files (50-60% accuracy)*

3. **Event Logs** (for HISTORICAL_EVENT queries):
   ```bash
   .chora/memory/events/*.jsonl  # JSONL event logs (SAP-010)
   ```
   *Fallback: git log of last 50 commits (40-50% accuracy)*

4. **Justfile** (for AUTOMATION_RECIPE queries):
   ```bash
   justfile  # Automation recipes
   ```
   *Fallback: scripts/ directory search (70-80% accuracy)*

**Quick Check**:
```bash
# Verify discovery system is installed
ls scripts/unified-discovery.py scripts/run-discovery-benchmark.py

# Verify required sources exist (optional - fallback mode works without)
ls feature-manifest.yaml justfile .chora/memory/knowledge/notes/
```

**Note**: Discovery works without these files (fallback mode), but accuracy and token savings are lower. See [Fallback Discovery Mode](#fallback-discovery-mode) for details.

---

## Query Type 1: CODE_FEATURE (3 minutes)

### When to Use

Use CODE_FEATURE queries when you need to:
- Find implementation of a specific feature
- Locate code for authentication, database, API endpoints
- Find documentation or metrics dashboards
- Get code file paths from feature IDs

### Query Patterns

**Strong CODE signals** (routes to CODE with high confidence):
- "**show me** [feature] code"
- "**where is** [feature] implementation"
- "**find** [feature] documentation"
- "[feature] **code**" (ends with "code")

**Examples**:
```bash
# Find authentication implementation
just discover "show me authentication code"

# Find metrics dashboard
just discover "SAP metrics dashboard"

# Find documentation
just discover "show me git workflow patterns documentation"

# Find database code
just discover "database code"
```

### What You Get

Discovery returns:
- **Feature ID** (e.g., FEAT-001, FEAT-002)
- **Feature name** and status (active, deprecated, etc.)
- **Code file paths** with line ranges
- **Test file paths**
- **Documentation paths**
- **Knowledge notes** related to feature

**Token Estimate**: 5-8k (vs 20-40k for grep all files)

### Example Output

```
[QUERY] show me authentication code
[TYPE] code_feature
[METHOD] feature_manifest
[TOKEN EST] ~7,000 tokens

[RESULTS] Found 1 match(es):
1. [FEAT-003] Authentication & Authorization (active)
   Code: 3 file(s)
   Knowledge: [.chora/memory/knowledge/notes/authentication-patterns.md]

[SUGGESTIONS]
   - Load code: src/auth/authenticate.py
   - Read knowledge: .chora/memory/knowledge/notes/authentication-patterns.md
```

**Next Step**: Load suggested files (saves 75% tokens vs grep)

---

## Query Type 2: PATTERN_CONCEPT (2 minutes)

### When to Use

Use PATTERN_CONCEPT queries when you need to:
- Understand "how we do X" (architectural patterns)
- Learn best practices or design decisions
- Find reusable patterns for a specific problem
- Understand workflows or methodologies

### Query Patterns

**Strong PATTERN signals** (routes to PATTERN with high confidence):
- "**how do we** [action]"
- "**what patterns** for [problem]"
- "**best practice** for [scenario]"
- "**explain** our [approach]"

**Examples**:
```bash
# Find testing patterns
just discover "how do we handle async testing"

# Find architectural patterns
just discover "what patterns for error handling"

# Find workflow documentation
just discover "best practice for code review"

# Find design decisions
just discover "explain our database migration strategy"
```

### What You Get

Discovery returns:
- **Knowledge note paths** with relevant patterns
- **Title** and relevance score
- **Path** to markdown file

**Token Estimate**: 10-15k (vs 30-50k for reading all notes)

### Example Output

```
[QUERY] how do we handle async testing
[TYPE] pattern_concept
[METHOD] knowledge_graph
[TOKEN EST] ~12,000 tokens

[RESULTS] Found 3 match(es):
1. Testing Strategy and Best Practices
   Path: .chora/memory/knowledge/notes/testing-strategy.md

2. Async Operations Pattern
   Path: .chora/memory/knowledge/notes/async-patterns.md

[SUGGESTIONS]
   - Read: .chora/memory/knowledge/notes/testing-strategy.md
   - Also relevant: .chora/memory/knowledge/notes/async-patterns.md
```

**Next Step**: Read top 1-2 suggested knowledge notes

---

## Query Type 3: HISTORICAL_EVENT (2 minutes)

### When to Use

Use HISTORICAL_EVENT queries when you need to:
- Find out "when did X happen"
- Review past work on a feature or SAP
- Understand timeline or sequence of events
- Check completion status of milestones

### Query Patterns

**Strong HISTORICAL signals** (routes to HISTORICAL with high confidence):
- "**when did** [event]"
- "**when was** [milestone]"
- "**history** of [feature]"
- Past tense verbs: "**completed**", "**delivered**", "**fixed**"

**Examples**:
```bash
# Find when SAP was completed
just discover "when did we complete SAP-015 L4"

# Find feature delivery date
just discover "when was FEAT-002 delivered"

# Find bug fix history
just discover "when did we fix the parser bug"

# Find previous work
just discover "history of authentication feature"
```

### What You Get

Discovery returns:
- **Timestamp** (ISO 8601 format)
- **Event type** (e.g., sap_adoption_completed, feature_delivered)
- **Trace ID** (links related events)
- **Message** (first 100 chars of event details)

**Token Estimate**: 8-12k (vs 20-30k for reading all sprint plans)

### Example Output

```
[QUERY] when did we complete SAP-015 L4
[TYPE] historical_event
[METHOD] event_logs
[TOKEN EST] ~10,000 tokens

[RESULTS] Found 2 match(es):
1. 2025-11-15T14:30:00-08:00 - sap_adoption_completed
   SAP-015 (Beads Task Tracking) reached Level 4 (Strategic Integration) after 3 sprints

2. 2025-11-15T14:25:00-08:00 - sap_l4_milestone_achieved
   Strategic integration complete: Beads integrated with SAP-010 memory system

[SUGGESTIONS]
   - Found 2 events
   - Latest: 2025-11-15T14:30:00-08:00 - sap_adoption_completed
```

**Next Step**: Review event details for context

---

## Query Type 4: AUTOMATION_RECIPE (2 minutes)

### When to Use

Use AUTOMATION_RECIPE queries when you need to:
- Find "how do I run X" (justfile recipes)
- Learn command-line automation
- Find scripts for validation, testing, building
- Get exact commands to execute

### Query Patterns

**Strong AUTOMATION signals** (routes to AUTOMATION with high confidence):
- "**how do I run** [task]"
- "**how do I execute** [command]"
- "**command** to [action]"
- "**recipe** for [task]"

**Examples**:
```bash
# Find how to run metrics
just discover "how do I run SAP metrics"

# Find validation command
just discover "command to validate links"

# Find test execution
just discover "how do I run tests"

# Find build recipe
just discover "recipe for building project"
```

### What You Get

Discovery returns:
- **Recipe name** (e.g., sap-metrics, validate-links)
- **Description** (from justfile comment)
- **Relevance score**

**Token Estimate**: 1-5k (vs 10-15k for reading justfile + scripts)

### Example Output

```
[QUERY] how do I run SAP metrics
[TYPE] automation_recipe
[METHOD] justfile
[TOKEN EST] ~3,000 tokens

[RESULTS] Found 2 match(es):
1. just sap-metrics
   Generate SAP adoption metrics report (JSON format)

2. just sap-stats
   Show SAP adoption statistics dashboard

[SUGGESTIONS]
   - Run: just sap-metrics
   - Also: just sap-stats
```

**Next Step**: Execute suggested recipe

---

## Hands-On Practice (5 minutes)

### Exercise 1: Find Authentication Code

**Goal**: Find authentication implementation files

```bash
# Step 1: Run discovery query
just discover "show me authentication code"

# Expected: CODE_FEATURE → feature manifest
# Result: Feature ID, code paths, test paths

# Step 2: Load suggested code file
# (Use Read tool with path from suggestions)
```

**Token Saved**: ~15k (20k grep → 5k targeted)

---

### Exercise 2: Learn Testing Patterns

**Goal**: Understand how the project handles testing

```bash
# Step 1: Run discovery query
just discover "how do we handle testing"

# Expected: PATTERN_CONCEPT → knowledge graph
# Result: Knowledge note paths

# Step 2: Read top knowledge note
# (Use Read tool with path from suggestions)
```

**Token Saved**: ~20k (30k all notes → 10k targeted)

---

### Exercise 3: Check Sprint History

**Goal**: Find when SAP-010 was completed

```bash
# Step 1: Run discovery query
just discover "when did we complete SAP-010"

# Expected: HISTORICAL_EVENT → event logs
# Result: Timestamped events

# Step 2: Review event details
# (Events show completion date, trace ID for related work)
```

**Token Saved**: ~10k (20k sprint plans → 10k events)

---

### Exercise 4: Find Validation Command

**Goal**: Get exact command to validate links

```bash
# Step 1: Run discovery query
just discover "how do I validate links"

# Expected: AUTOMATION_RECIPE → justfile
# Result: Recipe name + description

# Step 2: Run suggested recipe
just validate-links
```

**Token Saved**: ~12k (15k justfile exploration → 3k direct)

---

## Advanced Features (2 minutes)

### JSON Output Mode

Use JSON output for piping to other tools:

```bash
# Get JSON output
just discover-json "show me authentication code"

# Pipe to jq for parsing
just discover-json "show me auth code" | jq .query_type

# Use in scripts
QUERY_TYPE=$(just discover-json "my query" | jq -r .query_type)
```

### Benchmark Validation

Validate routing accuracy on test queries:

```bash
# Run benchmark on validation set (31 queries)
just discover-benchmark

# Expected: 96%+ routing accuracy
# Results saved to: scripts/fixtures/feat-002-validation/benchmark-results.csv
```

### Discovery Statistics

View system statistics and metrics:

```bash
# Show discovery stats
just discover-stats

# Output:
# - Token savings: 65-82% vs grep/glob
# - Routing accuracy: 96.8% (30/31 queries)
# - Discovery speed: 0.087s average
# - Query type breakdown
```

---

## Troubleshooting (2 minutes)

### Query Classified as UNKNOWN

**Problem**: Discovery returns query type UNKNOWN with no results

**Causes**:
1. **Low confidence** (score < 0.3): Query is ambiguous
2. **Negative patterns**: Query matches destructive/gibberish patterns
3. **Missing keywords**: Query lacks specific intent signals

**Solutions**:
```bash
# Bad: Ambiguous query
just discover "fix bug in parser"

# Good: Add specificity
just discover "show me parser code"  # CODE
just discover "when did we fix parser"  # HISTORICAL

# Bad: Too generic
just discover "help me"

# Good: Specific intent
just discover "how do I run tests"  # AUTOMATION
```

---

### Wrong Query Type Routed

**Problem**: Discovery routes to wrong type (e.g., CODE instead of PATTERN)

**Causes**:
1. **Conflicting signals**: Query has keywords from multiple types
2. **Synonym expansion**: Keywords expand to unintended types

**Solutions**:
```bash
# Conflicting: "show me" (CODE) + "workflow" (PATTERN)
just discover "show me git workflow"

# Fix: Add explicit intent
just discover "show me git workflow patterns documentation"  # CODE (documentation)
just discover "how do we use git workflow"  # PATTERN (how do we)

# Conflicting: "code" + "run"
just discover "run authentication code"

# Fix: Clarify intent
just discover "show me authentication code"  # CODE (show me)
just discover "how do I run authentication"  # AUTOMATION (how do I run)
```

---

### No Results Found

**Problem**: Discovery routes correctly but finds no results

**Causes**:
1. **Missing source**: Feature manifest, knowledge notes, or event logs not present
2. **No matching content**: Keywords don't match any artifacts
3. **Typos**: Misspelled keywords (fuzzy matching helps but not perfect)

**Solutions**:
```bash
# Check if required sources exist
ls feature-manifest.yaml  # For CODE queries
ls .chora/memory/knowledge/notes/  # For PATTERN queries
ls .chora/memory/events/*.jsonl  # For HISTORICAL queries
ls justfile  # For AUTOMATION queries

# Try broader keywords
just discover "authentication"  # Instead of "auth-handler-v2"

# Check spelling
just discover "authentication"  # Instead of "authentiction"
```

---

### Fallback Discovery Mode

**Problem**: Discovery uses fallback methods with warning messages

**What is Fallback Mode**:

When required SAP structures are missing, discovery gracefully degrades to alternative sources:

| Primary Source | Fallback Source | Method Used | Accuracy |
|----------------|-----------------|-------------|----------|
| feature-manifest.yaml | glob search (src/, lib/, packages/) | `fallback_glob` | ~60-70% |
| .chora/memory/knowledge/ | docs/ markdown files | `fallback_docs` | ~50-60% |
| .chora/memory/events/ | git log (last 50 commits) | `fallback_git_log` | ~40-50% |
| justfile | scripts/ directory (.py, .sh) | `fallback_scripts` | ~70-80% |

**Example**:
```bash
$ just discover "show me authentication code"

⚠️  Using fallback glob search (less accurate than feature manifest)
💡 Adopt SAP-056 (Lifecycle Traceability) for 50-70% token savings
📖 See: docs/user-docs/how-to/use-unified-discovery.md

Found 3 potential files:
  - src/auth/authentication.py
  - src/auth/authorization.py
  - lib/auth/middleware.py
```

**When Fallback Triggers**:

1. **New projects**: Before SAP adoption (no feature manifest yet)
2. **Minimal projects**: Small repos without full chora structure
3. **Legacy projects**: Pre-existing codebases being migrated

**Interpreting Fallback Results**:

✅ **Fallback works**:
- Still finds relevant files (60-80% accuracy vs 96%+ with primary)
- Provides guidance to adopt SAPs for better results
- Lower token savings (1500-2000 tokens vs 5000-8000 with primary)

⚠️ **Fallback limitations**:
- Less accurate routing (more false positives)
- No artifact metadata (just file paths, no requirements/tests links)
- Slower performance (glob searches entire codebase)
- No wikilink connectivity (knowledge graph features unavailable)

**Solutions**:

```bash
# Option 1: Adopt full SAP system (recommended)
# - SAP-056 (Lifecycle Traceability): Create feature-manifest.yaml
# - SAP-010 (Memory System): Set up .chora/memory/ structure
# - SAP-008 (Automation Dashboard): Create justfile

# Option 2: Use fallback mode (acceptable for quick exploration)
# - Fallback discovery still works (60-80% accuracy)
# - Good enough for initial codebase exploration
# - Upgrade to full SAP system when ready for production use

# Check what's missing
ls feature-manifest.yaml  # If missing → fallback_glob
ls .chora/memory/knowledge/notes/  # If missing → fallback_docs
ls .chora/memory/events/  # If missing → fallback_git_log
ls justfile  # If missing → fallback_scripts
```

**Fallback Mode Value**:

- **Without SAPs**: Discovery still works (better than manual grep)
- **With SAPs**: Discovery excellent (96%+ accuracy, 65-82% token savings)
- **Migration path**: Start with fallback, adopt SAPs incrementally

---

## Integration with Progressive Loading

Unified Discovery is most powerful when integrated with progressive context loading:

### Phase 1: Orientation (0-10k tokens)

**Traditional**:
```
1. Read root AGENTS.md (5k tokens)
2. Read domain AGENTS.md (5k tokens)
3. Guess which files to load → often wrong
Total: 10k tokens, 3-5 minutes
```

**With Discovery**:
```
1. Read root AGENTS.md (5k tokens)
2. Run discovery query (0.087s)
3. Load exactly the files suggested by discovery
Total: 5-8k tokens, 1-2 minutes
```

**Token Savings**: 2-5k (20-40% reduction)
**Time Savings**: 2-3 minutes (60% faster)

### Phase 2: Specification (10-50k tokens)

**Traditional**:
```
1. Grep for keywords (load 20+ files)
2. Read files (many irrelevant)
3. Refine search, reload
Total: 40-60k tokens, 10-15 minutes
```

**With Discovery**:
```
1. Run discovery queries for each topic
2. Load targeted artifacts from suggestions
3. No reloading needed (accurate on first try)
Total: 15-25k tokens, 5-7 minutes
```

**Token Savings**: 25-35k (60-70% reduction)
**Time Savings**: 5-8 minutes (50-60% faster)

---

## Best Practices

### DO

✅ **Use specific keywords**: "authentication", "database", "testing"
✅ **Use explicit intent phrases**: "show me", "how do we", "when did", "how do I run"
✅ **Start queries with strong signals**: "show me X" routes to CODE reliably
✅ **Run discovery BEFORE loading files**: Saves 60-80% tokens
✅ **Trust suggestions**: 96.8% routing accuracy, suggestions are targeted

### DON'T

❌ **Use ambiguous queries**: "fix bug" (missing context)
❌ **Mix multiple intents**: "show me workflow and run metrics" (confusing)
❌ **Use overly generic keywords**: "help", "info", "stuff"
❌ **Skip discovery for exploration**: Loading all files wastes 20-40k tokens
❌ **Ignore suggestions**: Suggested files are scored by relevance

---

## Summary

### Key Takeaways

1. **4 Query Types**: CODE, PATTERN, HISTORICAL, AUTOMATION (learn the patterns)
2. **60-80% Token Savings**: 5-15k vs 20-40k (use discovery BEFORE grep)
3. **96.8% Accuracy**: Trust the routing, load suggested files
4. **0.087s Speed**: 344x faster than manual exploration (3-5 minutes → sub-second)
5. **Progressive Loading**: Integrate with Phase 1 for optimal efficiency

### Quick Reference

| If You Need | Use Query Type | Start With |
|-------------|----------------|------------|
| Code files | CODE_FEATURE | "show me [feature] code" |
| Patterns | PATTERN_CONCEPT | "how do we [action]" |
| History | HISTORICAL_EVENT | "when did [event]" |
| Commands | AUTOMATION_RECIPE | "how do I run [task]" |

### Next Steps

1. **Run 4 exercises** in "Hands-On Practice" section (5 min)
2. **Integrate with workflow**: Use discovery before loading files (saves 60-80% tokens)
3. **Validate locally**: Run `just discover-benchmark` to verify 96%+ accuracy (1 min)
4. **Read advanced docs**: scripts/AGENTS.md (Workflow 7) and scripts/CLAUDE.md (Workflow 8)

---

**Questions?** Check [scripts/AGENTS.md](../../scripts/AGENTS.md) for agent-specific patterns or [scripts/CLAUDE.md](../../scripts/CLAUDE.md) for Claude-optimized workflows.

**Feedback?** File issues at https://github.com/anthropics/chora-base/issues with `[FEAT-002]` tag.
