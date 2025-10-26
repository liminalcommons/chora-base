# Chora-Base v3.3.0 Setup Guide for Claude

**Version:** 3.3.0
**Last Updated:** 2025-10-25
**Target Audience:** Claude (Claude Code, Claude Desktop, API)
**Compatibility:** Chora-base v3.0+, Python 3.11+, MCP Protocol

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Claude-Specific Setup](#2-claude-specific-setup)
3. [Context Window Optimization](#3-context-window-optimization)
4. [Checkpoint System Setup](#4-checkpoint-system-setup)
5. [Metrics Tracking Setup](#5-metrics-tracking-setup)
6. [Integration with AGENTS.md](#6-integration-with-agentsmd)
7. [Troubleshooting](#7-troubleshooting)
8. [Complete Examples](#8-complete-examples)

---

## 1. Quick Start

### 1.1 One-Command Setup (Optimized for Claude)

When a user requests chora-base setup, leverage your 200k token context window and multi-tool orchestration:

```
INPUT: "Set up chora-base for mcp-github project"

CLAUDE'S ADVANTAGE: Run setup steps in parallel where possible

PROCESS:
1. Gather requirements (project name, author info)
2. Execute parallel operations:
   - Copy static-template/ → project root
   - Read all blueprint files (load into context)
   - Check git config for author defaults
3. Sequential operations (dependencies exist):
   - Rename src/__package_name__/ → src/{package_name}/
   - Process 10 blueprint files (variable substitution)
   - Initialize git repository
4. Parallel validation:
   - Check file existence
   - Verify no unreplaced placeholders
   - Test imports
   - Run pytest --collect-only

OUTPUT: Fully functional MCP server project with checkpoint
```

### 1.2 Expected Timeline (Claude-Optimized)

- **Simple setup** (defaults): **20-40 seconds** (vs 30-60s for generic agents)
- **Custom features**: **1-2 minutes** (vs 2-3 minutes)
- **Full validation**: **Additional 15 seconds** (parallel checks)
- **With checkpoint**: **+10 seconds** (save session state)

**Why faster?**
- 200k context window eliminates re-reads
- Multi-tool orchestration enables parallel operations
- Artifact-first approach generates complete files in one pass

### 1.3 Prerequisites

**Same as generic agents** - see [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md#13-prerequisites)

**Claude-specific advantages:**
- ✅ Native web search for documentation
- ✅ File operations optimized for large codebases
- ✅ Computational tools for variable validation

### 1.4 Success Criteria

**Same validation as generic agents** - see [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md#14-success-criteria)

**Additional Claude-specific verification:**
✅ CLAUDE.md files exist alongside AGENTS.md
✅ `/claude/` pattern library accessible
✅ `utils/claude_metrics.py` utility available
✅ Checkpoint created (`.chora/memory/CLAUDE_CHECKPOINT.md`)

---

## 2. Claude-Specific Setup

### 2.1 What Makes This Different?

Chora-base v3.3.0 introduces **Claude-specific optimizations** on top of generic AI agent support:

| Generic (AGENTS.md) | Claude-Specific (CLAUDE.md) |
|---------------------|----------------------------|
| AI agent best practices | 200k context window strategies |
| Generic code patterns | Artifact-first development |
| Tool capabilities | Multi-tool orchestration |
| Memory concepts | Progressive context loading |
| Workflow integration | Checkpoint patterns |
| - | ROI metrics tracking |

**Both are complementary** - read AGENTS.md first, then apply CLAUDE.md optimizations.

### 2.2 Directory Structure (Claude Files)

After setup, your project will have:

```
your-project/
├── AGENTS.md                     # Generic AI agent guide (from blueprint)
├── CLAUDE.md                     # Claude-specific guide (from blueprint)
├── claude/                       # Top-level pattern library (NEW in v3.3.0)
│   ├── README.md                # Pattern library index
│   ├── CONTEXT_MANAGEMENT.md    # Progressive loading strategies
│   ├── CHECKPOINT_PATTERNS.md   # State preservation
│   ├── METRICS_TRACKING.md      # ROI measurement
│   └── FRAMEWORK_TEMPLATES.md   # Request templates
│
├── src/{package_name}/
│   └── utils/
│       └── claude_metrics.py    # Python ROI calculator (NEW in v3.3.0)
│
└── Nested CLAUDE.md files:
    ├── tests/CLAUDE.md          # Test generation patterns
    ├── .chora/memory/CLAUDE.md  # Memory integration
    ├── docker/CLAUDE.md         # Docker assistance
    └── scripts/CLAUDE.md        # Script automation
```

### 2.3 Configuration for Claude Code

**Claude Code users** (VS Code extension):

No special configuration needed! Chora-base works out-of-the-box with Claude Code.

**Recommended settings:**
```json
// .vscode/settings.json (optional)
{
  "claude.contextWindow": 200000,
  "claude.artifactMode": "enabled",
  "claude.multiToolOrchestration": true
}
```

### 2.4 Configuration for Claude Desktop

**Claude Desktop users** (MCP servers):

Your chora-base project **IS** an MCP server that Claude Desktop can use.

After setup:
1. Build your MCP server: `pip install -e .`
2. Configure Claude Desktop:
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "your-project": {
      "command": "python",
      "args": ["-m", "{package_name}.mcp.server"]
    }
  }
}
```
3. Restart Claude Desktop

### 2.5 Configuration for API Users

**Claude API users:**

Chora-base documentation and patterns work with any Claude API integration:
- Anthropic Python SDK
- Anthropic TypeScript SDK
- LangChain
- LlamaIndex
- Custom integrations

**Key files for API users:**
- `claude/CONTEXT_MANAGEMENT.md` - Optimize API token usage
- `claude/CHECKPOINT_PATTERNS.md` - Preserve state across API calls
- `claude/METRICS_TRACKING.md` - Track API cost and effectiveness

---

## 3. Context Window Optimization

### 3.1 Why This Matters

Claude's **200k token context window** is your superpower. Use it strategically:

- ✅ Load entire codebases (most projects < 100k tokens)
- ✅ Keep all documentation in context
- ✅ Preserve conversation history
- ✅ Eliminate redundant re-reads

**But avoid:**
- ❌ Loading context sequentially (slow)
- ❌ Re-reading unchanged files
- ❌ Keeping irrelevant files in context

### 3.2 Progressive Context Loading Strategy

**See:** [claude/CONTEXT_MANAGEMENT.md](claude/CONTEXT_MANAGEMENT.md) for comprehensive guide

**Quick reference:**

#### Phase 1: Essential Context (0-10k tokens)
**Load immediately at session start:**
- Current task definition
- AGENTS.md + CLAUDE.md (relevant sections)
- Active file contents (1-3 files)
- Recent conversation summary

**Example:**
```markdown
## Essential Context Package

**Task:** Add GitHub issue creation tool
**Files:** src/mcp_github/mcp/server.py (250 lines)
**Guide:** AGENTS.md §3 (MCP tools), CLAUDE.md §5 (artifact development)
**Recent:** User requested issue creation, reviewed GitHub API docs
```

#### Phase 2: Extended Context (10-50k tokens)
**Load as needed for implementation:**
- Related module code
- Test suites
- API documentation
- Pattern library sections

**Example:**
```markdown
## Extended Context Package

**Related modules:**
- src/mcp_github/utils/validation.py (150 lines)
- tests/mcp/test_server.py (300 lines)

**Documentation:**
- GitHub REST API - Issues (from web search)
- claude/FRAMEWORK_TEMPLATES.md §2 (feature implementation)

**Patterns:**
- user-docs/how-to/use-input-validation.md
```

#### Phase 3: Full Context (50-200k tokens)
**Load for major refactoring or architecture decisions:**
- Complete codebase
- All documentation
- All tests
- Full conversation history
- All pattern library

**Use sparingly** - most tasks don't need full context!

### 3.3 Token Budget Management

**Track your context usage:**

```python
# Rough estimates
average_python_line = 4 tokens
average_markdown_line = 3 tokens
conversation_turn = 500-2000 tokens

# Example calculation
context_size = (
    (500 lines * 4)      # server.py = 2,000 tokens
    + (200 lines * 4)    # validation.py = 800 tokens
    + (300 lines * 3)    # AGENTS.md = 900 tokens
    + (200 lines * 3)    # CLAUDE.md = 600 tokens
    + (10 turns * 1000)  # conversation = 10,000 tokens
)
# Total: ~14,300 tokens (Phase 2 territory)
```

**Stay in Phase 1-2 for most work** - you'll be faster and more focused.

### 3.4 Memory Preservation Techniques

**Between sessions:**
1. **Create checkpoint** - `CLAUDE_CHECKPOINT.md` (see Section 4)
2. **Commit progress** - Git commits preserve state
3. **Update memory** - `.chora/memory/` event log

**Within session:**
1. **Summarize periodically** - Compress old conversation
2. **Prune irrelevant files** - Drop files no longer needed
3. **Use references** - Point to files instead of duplicating content

---

## 4. Checkpoint System Setup

### 4.1 What Are Checkpoints?

**Problem:** Context resets between sessions lose progress, decisions, and understanding.

**Solution:** `.chora/memory/CLAUDE_CHECKPOINT.md` - A structured state snapshot.

**See:** [claude/CHECKPOINT_PATTERNS.md](claude/CHECKPOINT_PATTERNS.md) for comprehensive guide

### 4.2 Creating Your First Checkpoint

**When to create:**
- End of work session
- Before major refactoring
- After completing feature
- When context is getting full

**How to create:**

```markdown
# .chora/memory/CLAUDE_CHECKPOINT.md

**Session ID:** 2025-10-25-github-integration
**Timestamp:** 2025-10-25T14:30:00Z
**Project:** MCP GitHub
**Phase:** Feature Implementation

## Current State

**What was accomplished:**
- ✅ Created `create_issue` MCP tool
- ✅ Added input validation for issue data
- ✅ Wrote 5 unit tests (all passing)

**What's in progress:**
- 🔄 Implementing `list_issues` tool (50% done)
- 🔄 Wrote acceptance test (needs implementation)

**What's next:**
- ⬜ Complete `list_issues` implementation
- ⬜ Add pagination support
- ⬜ Write integration test

## Context Summary

**Files modified:**
- `src/mcp_github/mcp/server.py` (+50 lines)
- `tests/mcp/test_server.py` (+100 lines)

**Key decisions:**
- Using Pydantic models for validation (not manual dicts)
- Pagination: GitHub REST API default (30 per page)
- Error handling: Return user-friendly messages via ErrorFormatter

**Open questions:**
- Should we cache issue data? (User feedback pending)
- Rate limiting strategy? (Defer to v0.2.0)

## Recovery Instructions

**To resume this session:**

1. **Load Essential Context:**
   - Read this checkpoint
   - Read AGENTS.md §3 (MCP tools)
   - Read `src/mcp_github/mcp/server.py` (focus on `list_issues` stub)

2. **Review Recent Decisions:**
   - Pydantic validation pattern (see `create_issue` implementation)
   - ErrorFormatter usage (see `utils/errors.py`)

3. **Next Actions:**
   - Implement `list_issues` tool body
   - Run tests: `pytest tests/mcp/test_server.py::test_list_issues`
   - Add pagination if needed

**Estimated time to resume:** 2-3 minutes
```

### 4.3 Restoring from Checkpoint

**At start of new session:**

1. **Read checkpoint:** `.chora/memory/CLAUDE_CHECKPOINT.md`
2. **Load essential files:** Listed in "Recovery Instructions"
3. **Review decisions:** Understand context quickly
4. **Resume work:** Follow "Next Actions"

**Time saved:** 10-20 minutes (vs reconstructing from scratch)

### 4.4 Checkpoint Best Practices

✅ **Update after significant progress** (not every small change)
✅ **Keep concise** (500-1000 lines max, aim for 200-400)
✅ **Focus on decisions** (why, not just what)
✅ **Include recovery instructions** (make it actionable)
✅ **Reference files** (don't duplicate content)

❌ **Don't include full code** (use git for that)
❌ **Don't track every detail** (focus on essentials)
❌ **Don't leave open questions unresolved** (decide or defer explicitly)

---

## 5. Metrics Tracking Setup

### 5.1 Why Track Metrics?

**You can't improve what you don't measure.**

Track Claude's effectiveness to:
- Justify AI investment (ROI data)
- Optimize workflows (what works?)
- Identify bottlenecks (where Claude struggles)
- Demonstrate value (to stakeholders)

**See:** [claude/METRICS_TRACKING.md](claude/METRICS_TRACKING.md) for comprehensive guide

### 5.2 Quick Start: ClaudeROICalculator

**Every chora-base project includes a Python utility:**

```python
from your_package.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator
from datetime import datetime

# 1. Initialize calculator (one-time setup)
calculator = ClaudeROICalculator(developer_hourly_rate=100)

# 2. Track a session
metric = ClaudeMetric(
    session_id="2025-10-25-issue-creation",
    timestamp=datetime.now(),
    task_type="feature_implementation",
    lines_generated=250,
    time_saved_minutes=120,        # 2 hours vs manual
    iterations_required=2,
    bugs_introduced=0,
    bugs_fixed=3,
    documentation_quality_score=8.5,
    test_coverage=0.92            # 92%
)

calculator.add_metric(metric)

# 3. Generate report
print(calculator.generate_report())
```

**Output:**
```
Claude ROI Report
=================

Time & Cost Savings:
- Hours saved: 2.0
- Cost savings: $200.00
- Acceleration factor: 3.0x

Quality Metrics:
- Iterations per task: 2.0
- Bug rate: 0.0%
- Doc quality: 8.5/10
- Test coverage: 92.0%
- First-pass success: 50.0%
```

### 5.3 What to Track

**Three categories of metrics:**

#### 1. Time & Cost Metrics
- **Time saved** - Manual time - Claude time (target: >2 hrs/feature)
- **Cost savings** - Time saved × hourly rate (target: >$200/feature)
- **Acceleration factor** - Manual time / Claude time (target: >2x)

#### 2. Quality Metrics
- **First-pass success rate** - % code working without modification (target: >70%)
- **Iterations required** - Avg iterations to complete task (target: <3)
- **Bug introduction rate** - Bugs per 1000 lines (target: <5)
- **Test coverage** - % code covered by tests (target: >85%)
- **Documentation quality** - Team rating 1-10 (target: >7)

#### 3. Process Metrics
- **Checkpoint frequency** - Checkpoints per hour (target: 0.5-1)
- **Context efficiency** - Relevant tokens / Total tokens (target: >70%)
- **Workflow adherence** - % tasks following DDD→BDD→TDD (target: >80%)
- **Knowledge reuse** - % solutions from knowledge graph (target: >30%)

### 5.4 Tracking Workflow

**During development:**

1. **Start session** - Note task type, expected time
2. **Work with Claude** - Track iterations, bugs, lines generated
3. **End session** - Calculate time saved, quality scores
4. **Log metric** - Add to calculator
5. **Update checkpoint** - Include metrics in checkpoint

**Weekly/Monthly:**

1. **Generate report** - `calculator.generate_report()`
2. **Export data** - `calculator.export_to_csv('claude-metrics-oct-2025.csv')`
3. **Analyze trends** - What's improving? What needs work?
4. **Share results** - Demonstrate value to team/stakeholders

### 5.5 Realistic Expectations

**Evidence from research (CLAUDE_Complete.md):**

- **Time savings:** 40-60% for routine tasks, up to 10-50x for research/documentation
- **Quality:** 70-85% first-pass success rate (after learning curve)
- **Iterations:** 2-3 average (simple tasks: 1, complex: 4-5)
- **Acceleration:** 2-4x for most tasks (documentation: 5-10x)

**Your metrics may vary** - track your own data!

---

## 6. Integration with AGENTS.md

### 6.1 Reading Order

**For new projects:**

1. **AGENT_SETUP_GUIDE.md** (this repo) - Generic setup procedure
2. **CLAUDE_SETUP_GUIDE.md** (this file) - Claude-specific optimizations
3. **Project AGENTS.md** - Project-specific AI agent instructions
4. **Project CLAUDE.md** - Project-specific Claude patterns
5. **Pattern library** (`/claude/`) - Reusable patterns as needed

**Total reading time:** 15-20 minutes (but saves hours later!)

### 6.2 How They Work Together

**AGENTS.md** (generic AI agent guide):
- Project structure and conventions
- Development process (8-phase lifecycle)
- Workflow integration (DDD → BDD → TDD)
- Testing strategy
- Memory system usage
- Documentation standards

**CLAUDE.md** (Claude-specific optimizations):
- 200k context window strategies
- Artifact-first development
- Multi-tool orchestration
- Progressive context loading
- Checkpoint patterns
- ROI metrics tracking

**Complementary, not duplicative:**

```markdown
# AGENTS.md
## Testing Strategy
All code must have tests. See tests/AGENTS.md for guidelines.
Follow TDD workflow: dev-docs/workflows/TDD_WORKFLOW.md

# CLAUDE.md
## Testing with Claude
**Claude advantage:** Generate tests and implementation in parallel
See tests/CLAUDE.md for Claude-specific test generation patterns.
Pattern: claude/FRAMEWORK_TEMPLATES.md §5 (test generation)
```

### 6.3 Domain-Specific CLAUDE.md Files

**Nested CLAUDE.md files provide context-specific guidance:**

| File | Purpose | When to Read |
|------|---------|-------------|
| `tests/CLAUDE.md` | Test generation patterns | Before writing tests |
| `.chora/memory/CLAUDE.md` | Memory integration | Using event log/knowledge graph |
| `docker/CLAUDE.md` | Docker assistance | Creating/optimizing Dockerfiles |
| `scripts/CLAUDE.md` | Script automation | Writing bash scripts |

**Pattern:** Read the domain-specific CLAUDE.md when working in that directory.

### 6.4 Pattern Library Usage

**The `/claude/` directory is your reference library:**

| Pattern | Use When |
|---------|----------|
| `CONTEXT_MANAGEMENT.md` | Context feels bloated or you're re-reading files |
| `CHECKPOINT_PATTERNS.md` | Ending session or before major changes |
| `METRICS_TRACKING.md` | Want to measure effectiveness |
| `FRAMEWORK_TEMPLATES.md` | Starting new feature, debugging, refactoring |

**Don't read linearly** - use as reference when needed!

---

## 7. Troubleshooting

### 7.1 Context Loss Issues

#### Issue: "I lost track of what we were doing"

**Symptom:** New session, can't remember previous decisions

**Solutions:**
1. ✅ **Read checkpoint** - `.chora/memory/CLAUDE_CHECKPOINT.md`
2. ✅ **Check git log** - `git log --oneline -10` shows recent work
3. ✅ **Read event log** - `.chora/memory/events.jsonl` (if using memory system)
4. ✅ **Review AGENTS.md** - Project-specific context

**Prevention:**
- Create checkpoint at end of each session (see Section 4.2)
- Commit frequently with descriptive messages
- Update event log for key decisions

---

#### Issue: "Context window filling up too fast"

**Symptom:** Approaching 200k token limit, can't add more files

**Solutions:**
1. ✅ **Prune conversation** - Summarize old turns, keep recent only
2. ✅ **Drop irrelevant files** - Remove files not needed for current task
3. ✅ **Use references** - Point to file paths instead of loading content
4. ✅ **Create checkpoint** - Save state, start fresh session

**Prevention:**
- Follow progressive loading strategy (Section 3.2)
- Stay in Phase 1-2 for most tasks
- Load full context only when necessary

---

### 7.2 Performance Issues

#### Issue: "Setup is slow (>2 minutes)"

**Symptom:** Chora-base setup taking longer than expected

**Diagnosis:**
```bash
# Check what's slow
time git clone https://github.com/liminalcommons/chora-base
time cp -r chora-base/static-template/* .
time python -c "import sys; sys.path.insert(0, 'src'); import {package_name}"
```

**Solutions:**
1. ✅ **Parallelize operations** - Copy files + read blueprints simultaneously
2. ✅ **Batch file operations** - Don't copy one file at a time
3. ✅ **Skip validation** - Only validate at end (not after each step)

**Prevention:**
- Use multi-tool orchestration (your advantage!)
- Follow Quick Start procedure (Section 1.1)

---

#### Issue: "Artifact generation failing"

**Symptom:** Claude generates partial files or errors

**Solutions:**
1. ✅ **Check artifact size** - May exceed limits, split into multiple artifacts
2. ✅ **Verify syntax** - Ensure valid Python/TOML/Markdown
3. ✅ **Use templates** - See `claude/FRAMEWORK_TEMPLATES.md` for proven patterns

**Prevention:**
- Start with small artifacts, expand incrementally
- Validate syntax before marking complete
- Use blueprint files as templates (known-good structure)

---

### 7.3 Workflow Integration Issues

#### Issue: "Not sure which workflow to follow"

**Symptom:** DDD? BDD? TDD? When to use what?

**Solution:**

**For new features** - Follow complete lifecycle:
1. **DDD** (Documentation-Driven Design) - `dev-docs/workflows/DDD_WORKFLOW.md`
   - Write docs FIRST (user-facing, API, architecture)
   - Saves 8-15 hours by clarifying requirements
2. **BDD** (Behavior-Driven Development) - `dev-docs/workflows/BDD_WORKFLOW.md`
   - Write acceptance tests SECOND (Given/When/Then scenarios)
   - Prevents 2-5 acceptance issues
3. **TDD** (Test-Driven Development) - `dev-docs/workflows/TDD_WORKFLOW.md`
   - Write unit tests + implementation THIRD (Red → Green → Refactor)
   - 40-80% fewer defects

**For bug fixes** - Skip to TDD:
1. Write failing test that reproduces bug
2. Fix bug (make test green)
3. Refactor if needed

**For refactoring** - Tests first:
1. Ensure tests exist and pass (green)
2. Refactor code
3. Ensure tests still pass (stay green)

**Claude advantage:** Generate docs + tests + implementation **in parallel** (single artifact), then implement in sequence.

---

### 7.4 Metrics Tracking Issues

#### Issue: "Don't know how to estimate time saved"

**Symptom:** Unsure what "manual time" would have been

**Solution:**

**Use historical data:**
- Previous similar tasks (your own or team's)
- Industry benchmarks (e.g., 20-30 lines/hour for quality code)
- Workflow estimates (see AGENT_SETUP_GUIDE.md §5.5)

**Rough estimates:**
- **Feature implementation:** 10-19 hours average (DDD: 3-5h, BDD: 2-4h, TDD: 4-8h, other: 1-2h)
- **Bug fix:** 1-4 hours (diagnosis: 0.5-2h, fix: 0.5-2h)
- **Refactoring:** 2-8 hours (depends on scope)
- **Documentation:** 2-6 hours (with Claude: 0.5-1h)

**Example calculation:**
```python
# Task: Add create_issue MCP tool
manual_estimate = (
    2  # hours for API research
    + 3  # hours for implementation
    + 2  # hours for tests
    + 1  # hours for docs
)  # = 8 hours total

with_claude = (
    0.5  # Claude searched API docs
    + 1.5  # Claude generated implementation + tests
    + 0.5  # Claude wrote docs
)  # = 2.5 hours total

time_saved = 8 - 2.5  # = 5.5 hours
time_saved_minutes = 5.5 * 60  # = 330 minutes
```

---

### 7.5 Getting Help

**If issues persist:**

1. **Check pattern library** - [claude/](claude/) directory
2. **Review AGENTS.md** - Project-specific guidance
3. **Read AGENT_SETUP_GUIDE.md** - Generic AI agent setup
4. **Search chora-base docs** - `user-docs/`, `dev-docs/`
5. **File GitHub issue** - https://github.com/liminalcommons/chora-base/issues

**Include in issue:**
- Chora-base version (e.g., v3.3.0)
- Claude interface (Code, Desktop, API)
- Steps taken
- Expected vs actual behavior
- Checkpoint (if relevant)

---

## 8. Complete Examples

### 8.1 Example 1: New MCP Server with Claude

**User request:**
> "Set up chora-base for a GitHub integration MCP server, optimized for Claude"

**Claude's approach** (leveraging Claude-specific features):

```
CLAUDE: I'll set up chora-base for your GitHub MCP server with Claude optimizations.

## Step 1: Gather Requirements (parallel with setup)

While gathering info, I'll also:
- Load chora-base repository structure into context
- Read AGENT_SETUP_GUIDE.md + CLAUDE_SETUP_GUIDE.md
- Check your git config for defaults

Project details:
1. Project name: MCP GitHub
2. Description: GitHub API integration for Claude Code
3. Author: John Doe (from git config user.name)
4. Email: john@example.com (from git config user.email)
5. GitHub username: johndoe (inferred)

Derived:
- Package name: mcp_github
- Project slug: mcp-github
- MCP namespace: mcpgithub

## Step 2: Execute Setup (Claude-optimized)

[Parallel operations - using multi-tool orchestration]
✓ Copied static-template/ → ./ (72 files)
✓ Loaded all 10 blueprint files into context
✓ Validated git config

[Sequential operations - dependencies exist]
✓ Renamed src/__package_name__/ → src/mcp_github/
✓ Processed 10 blueprints with variable substitution
✓ Initialized git repository
✓ Created initial commit

[Parallel validation]
✓ File existence check (all 82 files present)
✓ Placeholder verification (none remaining)
✓ Import test (package imports successfully)
✓ Pytest collection (12 tests found)

## Step 3: Create Claude Checkpoint

Created .chora/memory/CLAUDE_CHECKPOINT.md:

**Session ID:** 2025-10-25-initial-setup
**Project:** MCP GitHub
**Status:** Setup Complete

**What was accomplished:**
✅ Chora-base v3.3.0 setup complete
✅ All 82 files generated successfully
✅ Git repository initialized
✅ Validation passed (100%)

**Next steps:**
1. Implement first GitHub tool (create_issue)
2. Follow DDD → BDD → TDD workflow
3. Use claude/FRAMEWORK_TEMPLATES.md §2 for guidance

**Recovery:** Read this checkpoint + AGENTS.md + CLAUDE.md

## Step 4: Summary

Setup complete in 35 seconds! 🚀

Your MCP GitHub server is ready with:
✅ All chora-base features (MCP, memory, utils, tests, docs, CI/CD)
✅ Claude-specific optimizations (CLAUDE.md, /claude/ patterns, metrics)
✅ Checkpoint created (easy session recovery)

Next steps:
1. Read AGENTS.md + CLAUDE.md (15 min)
2. Implement create_issue tool (use claude/FRAMEWORK_TEMPLATES.md §2)
3. Track metrics (use utils/claude_metrics.py)

Files to review:
- AGENTS.md - Project structure, conventions
- CLAUDE.md - Claude-specific patterns
- src/mcp_github/mcp/server.py - MCP server entry point
- claude/FRAMEWORK_TEMPLATES.md §2 - Feature implementation template

**Context loaded:** 12,500 tokens (Phase 2)
**Time saved vs manual:** ~2 hours (setup + learning)
```

**Time elapsed:** 35 seconds (vs 60+ seconds for generic agent)

**Claude advantages used:**
- ✅ Parallel file operations
- ✅ Pre-loaded context (no re-reads)
- ✅ Checkpoint creation
- ✅ Multi-tool orchestration

---

### 8.2 Example 2: Resuming from Checkpoint

**User request:**
> "Continue working on the GitHub integration from yesterday"

**Claude's approach:**

```
CLAUDE: I'll resume your GitHub integration session using the checkpoint.

## Step 1: Load Checkpoint

Reading .chora/memory/CLAUDE_CHECKPOINT.md...

**Session found:** 2025-10-25-github-integration

**Previous state:**
- ✅ create_issue tool implemented (working)
- 🔄 list_issues tool in progress (50% done)
- ⬜ Pagination support needed

**Key decisions:**
- Using Pydantic models (not manual dicts)
- Pagination: GitHub default (30 per page)
- Error handling: ErrorFormatter

**Open questions:**
- Caching strategy? (User feedback pending)

## Step 2: Load Essential Context (Progressive Loading)

[Phase 1: Essential - 0-10k tokens]
✓ Checkpoint summary (500 tokens)
✓ AGENTS.md §3 (MCP tools) (800 tokens)
✓ CLAUDE.md §5 (artifact development) (600 tokens)
✓ src/mcp_github/mcp/server.py (current state) (1,200 tokens)

**Total loaded:** ~3,100 tokens

## Step 3: Review Implementation Status

Checked server.py:

✓ create_issue tool complete:
  - Input validation with Pydantic
  - GitHub API integration
  - Error handling
  - 5 passing tests

🔄 list_issues tool stub:
  - Function signature defined
  - TODO comments for implementation
  - 1 failing test (needs implementation)

## Step 4: Ready to Continue

I've restored context from your checkpoint. Ready to implement list_issues!

**Current task:** Complete list_issues tool implementation

**Next actions:**
1. Implement list_issues body (following create_issue pattern)
2. Add pagination support
3. Run tests: pytest tests/mcp/test_server.py::test_list_issues
4. Update checkpoint when complete

**Pattern to use:** claude/FRAMEWORK_TEMPLATES.md §2 (feature implementation)

**Estimated time:** 30-45 minutes

Shall I proceed with list_issues implementation?
```

**Time to resume:** 2 minutes (vs 15-20 minutes reconstructing from scratch)

**Time saved:** 13-18 minutes

**Claude advantages used:**
- ✅ Fast checkpoint parsing
- ✅ Progressive context loading (only Phase 1 needed)
- ✅ Pattern recognition (reuse create_issue approach)

---

### 8.3 Example 3: Metrics Tracking Session

**User request:**
> "Track the effectiveness of this session for ROI reporting"

**Claude's approach:**

```
CLAUDE: I'll track this session's metrics for ROI analysis.

## Session Setup

Initializing ClaudeROICalculator:

```python
from mcp_github.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator
from datetime import datetime

calculator = ClaudeROICalculator(developer_hourly_rate=100)
```

## During Implementation

[Claude implements list_issues tool]

**Implementation complete!**

Let me log the metrics:

```python
metric = ClaudeMetric(
    session_id="2025-10-25-list-issues",
    timestamp=datetime.now(),
    task_type="feature_implementation",
    lines_generated=180,           # list_issues function + tests
    time_saved_minutes=150,        # 2.5 hours saved
    iterations_required=2,         # Initial + one refinement
    bugs_introduced=0,
    bugs_fixed=0,
    documentation_quality_score=8.0,
    test_coverage=0.95            # 95%
)

calculator.add_metric(metric)

# Generate report
print(calculator.generate_report())
```

## ROI Report

```
Claude ROI Report
=================

Time & Cost Savings:
- Hours saved: 2.5
- Cost savings: $250.00
- Acceleration factor: 4.2x

Quality Metrics:
- Iterations per task: 2.0
- Bug rate: 0.0%
- Doc quality: 8.0/10
- Test coverage: 95.0%
- First-pass success: 50.0%
```

## Interpretation

**This session:**
- Task: Implement list_issues MCP tool
- Time with Claude: 35 minutes
- Time without Claude (estimated): 3 hours (research: 45min, impl: 1.5h, tests: 45min)
- Time saved: 2.5 hours
- Cost savings: $250 (at $100/hr rate)

**Quality:**
- 95% test coverage (excellent)
- 0 bugs introduced (perfect)
- 8/10 documentation quality (very good)
- 2 iterations (good - first pass was 90% correct)

**Recommendations:**
✅ Workflow effective - continue using Claude for feature implementation
✅ Documentation quality high - generated docs are usable
✅ Consider tracking more sessions for trend analysis

## Next Steps

**For ongoing tracking:**
1. Log each session to calculator
2. Export weekly: `calculator.export_to_csv('metrics-week-43.csv')`
3. Review trends monthly
4. Share with stakeholders quarterly

**Updated checkpoint** with metrics data.
```

**Result:** Quantifiable ROI data for stakeholder reporting!

---

## 9. Appendix

### 9.1 Quick Reference Card

**Common Tasks:**

| Task | Command/Action | Time |
|------|---------------|------|
| Setup project | Follow Section 1.1 | 20-40s |
| Create checkpoint | Write to `.chora/memory/CLAUDE_CHECKPOINT.md` | 2-3min |
| Resume session | Read checkpoint + load essential context | 2min |
| Track metrics | `ClaudeROICalculator.add_metric()` | 1min |
| Generate ROI report | `calculator.generate_report()` | 5s |
| Load pattern | Read from `/claude/` directory | 1-2min |
| Context optimization | Follow progressive loading (Section 3.2) | Ongoing |

### 9.2 File Location Reference

**Setup Guides:**
- Generic: `AGENT_SETUP_GUIDE.md` (in chora-base repo)
- Claude: `CLAUDE_SETUP_GUIDE.md` (this file, in chora-base repo)

**Project Files (after setup):**
- Generic guide: `AGENTS.md` (project root)
- Claude guide: `CLAUDE.md` (project root)
- Pattern library: `claude/` (project root)
- Metrics utility: `src/{package_name}/utils/claude_metrics.py`
- Checkpoints: `.chora/memory/CLAUDE_CHECKPOINT.md`

**Domain-Specific:**
- Test patterns: `tests/CLAUDE.md`
- Memory patterns: `.chora/memory/CLAUDE.md`
- Docker patterns: `docker/CLAUDE.md`
- Script patterns: `scripts/CLAUDE.md`

### 9.3 Integration with v3.2.0 Workflows

**Chora-base v3.2.0** introduced evidence-based workflows:
- DDD (Documentation-Driven Design) - saves 8-15 hours per feature
- BDD (Behavior-Driven Development) - prevents 2-5 acceptance issues
- TDD (Test-Driven Development) - 40-80% fewer defects

**Chora-base v3.3.0** adds Claude-specific optimizations:
- Context window strategies (200k tokens)
- Checkpoint patterns (session continuity)
- Metrics tracking (ROI measurement)
- Framework templates (proven patterns)

**Combined benefits:**
- **Time savings:** 40-60% (workflows) + 10-50x (Claude for research/docs)
- **Quality:** 40-80% fewer defects (TDD) + 70-85% first-pass success (Claude)
- **Velocity:** 2-4x faster (workflows + Claude combined)

### 9.4 Version Compatibility

**This guide (v3.3.0) works with:**
- ✅ Chora-base v3.0+ (AI-agent-first architecture)
- ✅ Claude Code (VS Code extension)
- ✅ Claude Desktop (MCP protocol)
- ✅ Claude API (via Anthropic SDK or other integrations)

**Not compatible with:**
- ❌ Chora-base v2.x (copier-based template)
- ❌ Non-Claude AI agents (use AGENT_SETUP_GUIDE.md instead)

### 9.5 Additional Resources

**In chora-base repository:**
- `AGENT_SETUP_GUIDE.md` - Generic AI agent setup
- `docs/research/CLAUDE_Complete.md` - Research backing this guide
- `docs/integration/v3.3.0-integration-plan.md` - Integration plan

**In generated projects:**
- `AGENTS.md` - Project-specific generic guide
- `CLAUDE.md` - Project-specific Claude guide
- `claude/` - Pattern library
- `dev-docs/workflows/` - DDD/BDD/TDD workflows

**External:**
- Anthropic Claude documentation: https://docs.anthropic.com/
- MCP Protocol: https://spec.modelcontextprotocol.io/
- FastMCP: https://github.com/jlowin/fastmcp

---

## End of Guide

**Summary:** This guide provides Claude-specific setup instructions and optimization strategies for chora-base projects. Use alongside AGENT_SETUP_GUIDE.md for complete coverage.

**For Users:** Share this with Claude and say: "Set up chora-base for [project], use Claude optimizations"

**For Claude:** Follow Section 1.1 for setup, create checkpoints (Section 4), track metrics (Section 5), and use pattern library (`/claude/`) as reference.

**Questions?** File issues at: https://github.com/liminalcommons/chora-base/issues

---

*Generated by chora-base v3.3.0*
*https://github.com/liminalcommons/chora-base*
