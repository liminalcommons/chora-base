# Awareness Guide: Agent Awareness

**SAP ID**: SAP-009
**Version**: 2.1.0
**Target Audience**: AI agents
**Last Updated**: 2025-11-10

---

## 1. Quick Reference

### When to Use This SAP

**Use the Agent Awareness SAP when**:
- Starting work on a new codebase (read nearest AGENTS.md for domain patterns)
- Optimizing context loading for Claude (progressive loading strategy, token budgets)
- Understanding domain-specific patterns (read domain AGENTS.md, not just root)
- Creating awareness files for new directories/domains (follow protocol structure)
- Managing token budgets for different task types (small feature vs refactor)

**Don't use for**:
- Generic Claude usage - this SAP is chora-base-specific awareness file structure
- Non-hierarchical projects - SAP assumes "Nearest File Wins" directory hierarchy
- Static documentation - AGENTS.md is for dynamic agent guidance, not user docs
- One-time instructions - awareness files should be reusable across sessions

**Read awareness files**:
- Working on project root? → Read root AGENTS.md
- Working on tests? → Read tests/AGENTS.md
- Working on scripts? → Read scripts/AGENTS.md
- Using Claude? → Also read corresponding CLAUDE.md

**Principle**: "Nearest File Wins" - Read awareness file closest to code you're editing

---

## 2. Agent Context Loading

**Essential Context (2-3k tokens)**:
- [protocol-spec.md](protocol-spec.md) Sections 2, 3 - File structure, context optimization

**For writing awareness files**:
- [protocol-spec.md](protocol-spec.md) Section 4 - Content guidelines

---

## 3. Common Workflows

### 3.1 Read Appropriate Awareness File

**Steps**:
1. Identify working directory (e.g., tests/)
2. Check for AGENTS.md in that directory
3. If exists, read tests/AGENTS.md
4. If not exists, read parent directory AGENTS.md
5. If using Claude, also read CLAUDE.md (same directory)

**Example**:
- Editing tests/test_server.py → Read tests/AGENTS.md + tests/CLAUDE.md
- Editing src/server.py → Read root AGENTS.md + root CLAUDE.md
- Running scripts/build.sh → Read scripts/AGENTS.md + scripts/CLAUDE.md

### 3.2 Optimize Context Loading (Claude)

**Context**: 2k tokens (Protocol Section 3)

**Progressive Loading**:
1. **Phase 1** (0-10k): Essential - Task + relevant AGENTS.md + active files
2. **Phase 2** (10-50k): Extended - Related modules + tests + docs
3. **Phase 3** (50-200k): Full - Entire codebase (complex refactoring only)

**Token Budget by Task**:
- Small feature: 15-30k
- Large feature: 30-60k
- Bug fix: 5-10k
- Refactor: 20-40k

---

## 4. When to Split Awareness Files

### 4.1 File Size Thresholds

**Warning Threshold**: 1,000 lines (~5.6k tokens)
**Critical Threshold**: 2,000 lines (~11.2k tokens)

**Why this matters**: Large awareness files cause critical workflows to be buried and frequently missed by agents. The "meta-discoverability paradox" - by making everything discoverable in one place, we make nothing discoverable.

**Token estimate calculation**: `lines × 5.6 avg tokens/line`

### 4.2 Splitting Indicators

You should split awareness files when you observe:

✅ **File exceeds 1,000 lines** (warning zone)
✅ **File exceeds 2,000 lines** (critical - must split immediately)
✅ **Token estimate exceeds 10k** (beyond Phase 1 budget)
✅ **Critical workflows buried >50%** into file
✅ **Multiple distinct domains/concerns** in one file
✅ **Agents report missing documented workflows** despite documentation existing
✅ **File growth trajectory** suggests future problems

### 4.3 Splitting Strategy

**Step 1: Measure current state**
```bash
wc -l AGENTS.md CLAUDE.md
# Calculate token estimate: lines × 5.6 avg tokens/line
```

**Step 2: Identify distinct domains**
- What are the major topic areas?
- What content clusters together naturally?
- What workflows/processes are critical?

**Step 3: Create "Critical Workflows" section**
- Surface most important workflows at top of root file
- Provide quick reference + links to full details
- Use "⚠️" emoji for high visibility
- Keep this section in root file (lines 20-100 typically)

**Step 4: Extract domain content**
```bash
mkdir -p domain-name/
# Extract relevant sections to nested files
# Keep each file <500-800 lines
```

**Step 5: Update root file**
- Add Critical Workflows section at top (after overview)
- Replace detailed content with pointers to nested files
- Update frontmatter: `nested_structure: true`
- List `nested_files:` in frontmatter

**Step 6: Update CLAUDE.md**
- Add Critical Workflows section (coordinate with AGENTS.md)
- Update navigation references
- Reduce file to 600-800 lines

**Step 7: Update cross-references**
- README.md
- Other documentation
- Ensure all links work
- Run link validation

### 4.4 Recommended Domain Taxonomy

**Common domains** (use these for consistency):
- `/workflows/` or `/dev-process/` - Development workflows, sprint processes
- `/saps/` - SAP catalog and quick references (if applicable)
- `/features/` - Feature-specific patterns
- `/integrations/` - Integration patterns with other tools/SAPs
- `/getting-started/` - Onboarding and setup guides
- Custom domains as needed for your project

### 4.5 Critical Workflows Pattern

**Location**: Immediately after project overview, before main content

**Purpose**: Surface workflows that agents frequently miss

**Structure**:
```markdown
## ⚠️ Critical Workflows (Read This First!)

### [Workflow 1 Name]
**When**: [Trigger condition]
**Quick reference**: [Bash commands or steps]
**Full details**: [Link to nested file with complete template]

### [Workflow 2 Name]
...
```

**Example** (from chora-workspace implementation):
```markdown
## ⚠️ Critical Workflows (Read This First!)

### Sprint Completion Workflow
**When**: End of sprint (every 2 weeks)
**Quick reference**:
bash
just sprint-complete  # Generate report
git add . && git commit -m "chore: Sprint N completion"

**Full details**: [dev-process/AGENTS.md](dev-process/AGENTS.md#sprint-completion)

### Git Commit Conventions
**Format**: `type(scope): description`
**Types**: feat, fix, docs, chore, refactor
**Full spec**: [dev-process/AGENTS.md](dev-process/AGENTS.md#git-conventions)
```

### 4.6 Pattern Variations by Project Size

**Small Projects (<500 lines)**:
- **Don't split yet!** Keep monolithic structure
- **Rationale**: Overhead of navigation outweighs benefits at small scale

**Medium Projects (500-1,500 lines)**:
- **Light split**: 2-3 nested files for major domains
- **Example**:
  ```
  /AGENTS.md (root, 600 lines)
  /workflows/AGENTS.md (400 lines)
  /features/AGENTS.md (300 lines)
  ```

**Large Projects (1,500+ lines)**:
- **Full split**: 5+ nested files following domain structure
- **Example** (chora-workspace):
  ```
  /AGENTS.md (root, 839 lines)
  /saps/AGENTS.md (600 lines)
  /dev-process/AGENTS.md (450 lines)
  /docs/AGENTS.md (300 lines)
  /scripts/AGENTS.md (250 lines)
  ```

**Meta-Repositories (3,000+ lines before split)**:
- **Extensive split**: Match project structure with awareness structure
- **Principle**: "Nearest file wins" - agents read closest AGENTS.md for domain expertise

### 4.7 Evidence from chora-workspace

**Problem**: Root AGENTS.md was 2,766 lines (~15.4k tokens), sprint completion workflow buried at line 1,878 (66% into file), frequently missed by agents.

**Solution**: Split into 3-tier nested structure with Critical Workflows section at top.

**Results**:
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Root file size | 2,766 lines | 839 lines | **-70%** |
| Token budget | ~15.4k | ~5.5k | **Within Phase 1** ✓ |
| Workflow location | Line 1878 (66% buried) | Lines 32-50 (top 10%) | **Highly discoverable** ✓ |
| Structure | Monolithic | Modular (3 files) | **Research-backed** ✓ |

**Source**: COORD-2025-012 (chora-workspace coordination request)
**Research**: "Agentic Coding Best Practices" (p. 5-6) - "Prefer single-file artifacts for components under 500 lines" and "use modular architecture with nested AGENTS.md files"

### 4.8 Anti-Patterns to Avoid

❌ **Splitting too early**: Don't split <500 lines - creates unnecessary navigation overhead
❌ **Too many files**: Don't create 20+ nested files - defeats discoverability
❌ **No root critical workflows**: Don't remove all content from root - must provide orientation
❌ **Inconsistent structure**: Don't mix flat + nested randomly - follow pattern consistently
❌ **Broken cross-references**: Don't forget to update all links after splitting
❌ **No frontmatter indicators**: Don't skip `nested_structure: true` field - breaks tooling

---

## 5. Best Practices

**DO**:
- ✅ Read nearest awareness file first
- ✅ Use progressive context loading
- ✅ Create checkpoints every 5-10 interactions (Claude)
- ✅ Follow token budgets
- ✅ Split awareness files when they exceed 1,000 lines
- ✅ Surface critical workflows at top of root file
- ✅ Validate links after splitting

**DON'T**:
- ❌ Read entire project AGENTS.md for domain task
- ❌ Load full context (50-200k) for simple tasks
- ❌ Skip domain-specific awareness files
- ❌ Let awareness files grow beyond 2,000 lines
- ❌ Bury critical workflows deep in files

---

## 6. Common Pitfalls

### Pitfall 1: Reading Entire Project AGENTS.md for Domain-Specific Task

**Scenario**: Agent reads root AGENTS.md (general guidance) when working on tests/, missing test-specific patterns in tests/AGENTS.md.

**Example**:
```bash
# Agent task: "Fix failing test in tests/test_server.py"

# WRONG: Agent reads root AGENTS.md
Read /AGENTS.md  # General project guidance (200 lines)

# MISSING: Domain-specific guidance
# tests/AGENTS.md has pytest-specific patterns, fixtures, mocking strategies
```

**Fix**: Follow "Nearest File Wins" - read awareness file closest to working directory:
```bash
# Correct approach:
# 1. Identify working directory: tests/
# 2. Check for tests/AGENTS.md
ls tests/AGENTS.md  # Exists!

# 3. Read domain-specific file:
Read tests/AGENTS.md  # Pytest patterns, test structure guidance

# 4. If using Claude, also read:
Read tests/CLAUDE.md  # Claude-specific test optimizations

# 5. If needed, escalate to parent:
Read /AGENTS.md  # Only if tests/AGENTS.md insufficient
```

**Why it matters**: Domain-specific awareness files contain patterns critical for that domain. Root AGENTS.md is too general. Reading root file wastes tokens (load 200 lines general vs 50 lines specific). Protocol Section 2.2 mandates "Nearest File Wins".

### Pitfall 2: Skipping Domain-Specific Awareness Files

**Scenario**: Agent assumes root AGENTS.md is sufficient, doesn't check for domain files, misses critical patterns.

**Example**:
```bash
# Agent task: "Add automation script in scripts/"

# Agent checks root:
Read /AGENTS.md  # Project overview

# Agent starts coding WITHOUT checking:
ls scripts/AGENTS.md  # EXISTS but not read!

# Result: Agent misses:
# - Script naming conventions (scripts/ has specific format)
# - Error handling patterns
# - Integration with justfile
```

**Fix**: Always check for domain-specific files before starting work:
```bash
# Before working in ANY directory:
# 1. Check for AGENTS.md in working directory:
ls <working-dir>/AGENTS.md

# 2. If exists, read it:
Read <working-dir>/AGENTS.md

# 3. If using Claude, check for CLAUDE.md:
ls <working-dir>/CLAUDE.md
Read <working-dir>/CLAUDE.md  # Claude-specific patterns

# 4. Only then start work
```

**Why it matters**: Skipping domain files leads to pattern violations. scripts/AGENTS.md has 20 script-specific patterns not in root. Violating patterns requires rework (10-30 minutes). Reading domain file takes 1 minute.

### Pitfall 3: Not Using Progressive Context Loading

**Scenario**: Agent loads entire codebase (50-200k tokens) for small bug fix, hits token limit unnecessarily.

**Example**:
```bash
# User: "Fix typo in README.md"

# WRONG: Agent loads everything
Read entire project  # 150k tokens
# - All source files
# - All tests
# - All docs
# - All config files

# Result: 150k tokens used for 1-line change!
# Token limit hit on response, can't complete
```

**Fix**: Use progressive context loading (Protocol Section 3.2):
```bash
# Progressive loading phases:

# Phase 1 (0-10k tokens): Essential only
Read /AGENTS.md  # 2k tokens
Read README.md   # 1k tokens
# Total: 3k tokens for 1-line typo fix

# Phase 2 (10-50k tokens): Extended context (IF NEEDED)
# For larger features:
Read related modules  # 20k tokens
Read relevant tests   # 15k tokens
# Total: 35k tokens

# Phase 3 (50-200k tokens): Full codebase (RARELY)
# Only for complex refactoring:
Read entire codebase  # 150k tokens
# Use ONLY when absolutely necessary
```

**Why it matters**: Token budgets should match task complexity. Protocol Section 3.2 defines budgets: Bug fix (5-10k), Small feature (15-30k), Refactor (20-40k). Loading 150k for typo wastes 140k tokens. Progressive loading saves tokens, prevents limit errors.

### Pitfall 4: Forgetting CLAUDE.md When Using Claude

**Scenario**: Claude agent reads AGENTS.md but not CLAUDE.md, misses Claude-specific optimizations.

**Example**:
```bash
# Claude working on tests/

# Claude reads:
Read tests/AGENTS.md  # Generic agent patterns

# Claude SKIPS:
# tests/CLAUDE.md exists but not read!

# Missing Claude-specific optimizations:
# - Agentic loop checkpointing (every 5-10 interactions)
# - Extended thinking for complex test logic
# - Parallel tool calls for independent test runs
```

**Fix**: Claude must read both AGENTS.md AND CLAUDE.md:
```bash
# Claude workflow:
# 1. Read domain AGENTS.md (generic patterns):
Read <domain>/AGENTS.md

# 2. Read domain CLAUDE.md (Claude-specific):
Read <domain>/CLAUDE.md

# 3. Apply BOTH:
# - AGENTS.md: Generic patterns (all agents)
# - CLAUDE.md: Claude optimizations (checkpointing, extended thinking)
```

**Why it matters**: CLAUDE.md contains Claude-specific optimizations not applicable to other agents. Skipping CLAUDE.md means missing checkpointing guidance (prevents long context issues), extended thinking triggers (better complex reasoning), parallel tool usage (faster execution). Protocol Section 2.3 mandates Claude agents read both files.

### Pitfall 5: Creating Awareness Files Without Following Protocol

**Scenario**: Agent creates new AGENTS.md for custom directory but doesn't follow protocol structure, file is inconsistent.

**Example**:
```markdown
# Agent creates: custom-lib/AGENTS.md (WRONG structure)

# Random sections, no protocol compliance:
## Notes
Some patterns here...

## Tips
- Do this
- Do that

## Links
- Link 1
- Link 2

# Missing required sections from Protocol Section 4:
# - Quick Reference (required)
# - Common Patterns (required)
# - Best Practices (required)
# - Related Resources (required)
```

**Fix**: Follow protocol structure (Protocol Section 4.2):
```markdown
# custom-lib/AGENTS.md (CORRECT structure)

**Domain**: custom-lib/
**Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference
[Domain-specific quick commands]

## 2. Common Patterns
[Patterns specific to custom-lib/]

## 3. Best Practices
**DO**:
- ✅ [Best practices]

**DON'T**:
- ❌ [Anti-patterns]

## 4. Related Resources
- [Links to relevant files]

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide
```

**Why it matters**: Protocol structure ensures consistency across all awareness files. Inconsistent structure makes files hard to use. Other agents expect standard sections. Protocol Section 4.2 mandates structure. Following protocol takes 5 extra minutes, fixing inconsistent files later takes 30-60 minutes.

---

## 7. Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-009 --source /path/to/chora-base
```

This will automatically install:
- SAP-009 (Agent Awareness System)
- SAP-000 (SAP Framework)
- SAP-007 (Documentation Framework)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `minimal-entry` - 5 essential SAPs for quick ecosystem onboarding
- `recommended` - 10 SAPs covering core development workflows
- `mcp-server` - 10 SAPs for building MCP servers
- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Dependencies

This SAP depends on:
- SAP-000 (SAP Framework)
- SAP-007 (Documentation Framework)

All dependencies are automatically installed.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/agent-awareness/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

# Verify agent awareness files exist
ls AGENTS.md
ls CLAUDE.md
ls static-template/AGENTS.md
ls static-template/CLAUDE.md
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## 8. Bidirectional Translation Layer Integration (v1.1.0)

**For**: Generic agents (Claude, Cursor, etc.) and humans

**Purpose**: Enable conversational interaction while executing procedurally through progressive formalization

### 8.1 Discovery Workflow (3-Layer Progressive)

**Layer 1: Root AGENTS.md** - Agent loads root AGENTS.md, discovers 4 bidirectional tools, sees common patterns

**Layer 2: Domain AGENTS.md** - Agent navigates to domain, loads domain-specific user signal patterns

**Layer 3: Pattern Database** - For complex queries, loads full `INTENT_PATTERNS.yaml` (24+ patterns)

**Token Budget**: 15-35k tokens total (Layer 1: ~10k, Layer 2: ~5k, Layer 3: ~20k if needed)

**See**: [protocol-spec.md Section 6](protocol-spec.md) for complete contracts and specifications

### 8.2 Quick Integration for Generic Agents

**Subprocess Invocation** (Recommended):
```python
import subprocess, json

# Intent routing
result = subprocess.run(['python', 'scripts/intent-router.py', user_input], capture_output=True, text=True)
matches = json.loads(result.stdout)

# Glossary search
result = subprocess.run(['python', 'scripts/chora-search.py', query, '--fuzzy'], capture_output=True, text=True)
results = json.loads(result.stdout)

# Context-aware suggestions
result = subprocess.run(['python', 'scripts/suggest-next.py', '--mode=reactive'], capture_output=True, text=True)
suggestions = json.loads(result.stdout)
```

**Graceful Degradation**: If tools unavailable, fall back to documented patterns in AGENTS.md and INTENT_PATTERNS.yaml

### 8.3 Progressive Formalization

**Stage 1 (Week 1)**: User says "show inbox" → Agent translates and executes

**Stage 2 (Week 2-4)**: User says "coordination request" → Agent recognizes formal term, teaches definition

**Stage 3 (Month 2+)**: User says "run_inbox_status" → Agent executes directly, no translation

**Stage 4 (Month 3+)**: User provides JSON → Agent validates and executes

**Goal**: User learns systemic ontology at their own pace while system adapts to their style

### 8.4 User Preferences

**Configuration**: `.chora/user-preferences.yaml` (100+ options)

**Categories**:
- **Communication**: verbosity (concise|standard|verbose), formality (casual|standard|formal)
- **Workflow**: require_confirmation (always|destructive|never), progressive_disclosure
- **Learning**: capture_patterns, suggest_improvements, track_usage
- **Expertise**: assume_knowledge (beginner|intermediate|expert)

**Adaptation**: Agents load preferences and adapt response style, confirmation behavior, explanation depth

### 8.5 Maintenance

**Add Intent Pattern**: Edit `INTENT_PATTERNS.yaml`, test with `intent-router.py`, update domain AGENTS.md

**Add Glossary Term**: Edit `GLOSSARY.md`, test with `chora-search.py`, reference in SAP docs

**Update Suggestions**: Edit `suggest-next.py`, test with current project state, document new types

---

## 9. Related Content

### Within This SAP (skilled-awareness/agent-awareness/)

- [capability-charter.md](capability-charter.md) - Problem statement, scope, outcomes for SAP-011
- [protocol-spec.md](protocol-spec.md) - Complete technical contract (file hierarchy, progressive loading, protocol structure)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide for creating awareness files
- [ledger.md](ledger.md) - Agent awareness adoption tracking, version history
- **This document** (awareness-guide.md) - Agent workflows for using awareness files

### Developer Process (dev-docs/)

**Workflows**:
- [dev-docs/workflows/agent-assisted-development.md](../../dev-docs/workflows/agent-assisted-development.md) - Workflows for working with AI agents
- [dev-docs/workflows/context-management.md](../../dev-docs/workflows/context-management.md) - Managing context in long sessions

**Tools**:
- [dev-docs/tools/claude-code.md](../../dev-docs/tools/claude-code.md) - Claude Code specific patterns
- [dev-docs/tools/cursor.md](../../dev-docs/tools/cursor.md) - Cursor IDE patterns

**Development Guidelines**:
- [dev-docs/development/awareness-file-standards.md](../../dev-docs/development/awareness-file-standards.md) - Standards for writing AGENTS.md and CLAUDE.md

### Project Lifecycle (project-docs/)

**Implementation Components**:
- [blueprints/AGENTS.md.blueprint](/blueprints/AGENTS.md.blueprint) - Template for creating AGENTS.md files
- [blueprints/CLAUDE.md.blueprint](/blueprints/CLAUDE.md.blueprint) - Template for creating CLAUDE.md files
- [static-template/AGENTS.md](/static-template/AGENTS.md) - Root awareness file in generated projects
- [static-template/CLAUDE.md](/static-template/CLAUDE.md) - Root Claude-specific file in generated projects

**Guides**:
- [project-docs/guides/creating-awareness-files.md](../../project-docs/guides/creating-awareness-files.md) - Guide for writing awareness files
- [project-docs/guides/token-optimization.md](../../project-docs/guides/token-optimization.md) - Optimizing token usage with progressive loading

**Audits & Releases**:
- [project-docs/audits/](../../project-docs/audits/) - SAP audits including SAP-011 validation
- [project-docs/releases/](../../project-docs/releases/) - Version release documentation

### User Guides (user-docs/)

**Getting Started**:
- [user-docs/guides/working-with-agents.md](../../user-docs/guides/working-with-agents.md) - Introduction to agent awareness files

**Tutorials**:
- [user-docs/tutorials/creating-custom-agents-file.md](../../user-docs/tutorials/creating-custom-agents-file.md) - Create custom AGENTS.md for your domain
- [user-docs/tutorials/optimizing-claude-sessions.md](../../user-docs/tutorials/optimizing-claude-sessions.md) - Optimize Claude with progressive loading

**Reference**:
- [user-docs/reference/agents-file-structure.md](../../user-docs/reference/agents-file-structure.md) - AGENTS.md structure reference
- [user-docs/reference/claude-file-structure.md](../../user-docs/reference/claude-file-structure.md) - CLAUDE.md structure reference

### Other SAPs (skilled-awareness/)

**Core Framework**:
- [sap-framework/](../sap-framework/) - SAP-000 (defines SAP structure)
- [chora-base/protocol-spec.md](../chora-base/protocol-spec.md) - SAP-002 Meta-SAP Section 3.2.9 (documents SAP-011)

**Dependent Capabilities**:
- [project-bootstrap/](../project-bootstrap/) - SAP-003 (generates AGENTS.md and CLAUDE.md files)
- [memory-system/](../memory-system/) - SAP-009 (.chora/memory/AGENTS.md and CLAUDE.md)

**Supporting Capabilities**:
- [documentation-framework/](../documentation-framework/) - SAP-007 (awareness files follow Diataxis)
- [automation-scripts/](../automation-scripts/) - SAP-008 (scripts/AGENTS.md for script patterns)

**Core Documentation**:
- [README.md](/README.md) - chora-base overview
- [AGENTS.md](/AGENTS.md) - Root agent awareness file
- [CLAUDE.md](/CLAUDE.md) - Root Claude-specific file
- [CHANGELOG.md](/CHANGELOG.md) - Version history including SAP-011 updates
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol

---

**Version History**:
- **2.1.0** (2025-11-10): Added Section 4 (When to Split Awareness Files) - file size thresholds, splitting strategy, Critical Workflows pattern, domain taxonomy, evidence from chora-workspace (COORD-2025-012); renumbered subsequent sections
- **1.1.0** (2025-10-31): Added Section 7 (Bidirectional Translation Layer Integration) - discovery workflow, tool integration patterns, progressive formalization, user preferences, maintenance procedures; fixed SAP ID (SAP-011 → SAP-009)
- **1.0.1** (2025-10-28): Fixed SAP ID (SAP-009 → SAP-011), added "When to Use" section, "Common Pitfalls" with Wave 2 learnings, enhanced "Related Content" with 4-domain coverage
- **1.0.0** (2025-10-28): Initial awareness guide
