# AGENTS.md

This file provides machine-readable instructions for AI coding agents working with test-docs-standard.

---

## Project Overview

**test-docs-standard** is a Model Context Protocol (MCP) server that provides [describe your server's capabilities].

**Core Architecture:** [Describe your architecture pattern]
- [Key architecture point 1]
- [Key architecture point 2]
- [Key architecture point 3]

**Key Components:**
- **Main Module** (`[main_module].py`) - [Description]
- **[Component 2]** (`[module].py`) - [Description]
- **[Component 3]** (`[module].py`) - [Description]

### Strategic Context

**Current Priority:** [Describe current sprint/milestone focus]
- See [ROADMAP.md](ROADMAP.md) for committed work
- Focus: [List 2-3 key deliverables]

**Long-Term Vision:** [Describe evolutionary direction]
- See [dev-docs/vision/](dev-docs/vision/) for future capabilities
- Waves: [List 2-4 high-level capability themes]

**Design Principle:** Deliver current commitments while keeping future doors open.
- Don't build future features now
- Do design extension points and document decisions
- Do refactor when it serves both present and future

---

## Dev Environment Tips

### Prerequisites
- **Python 3.11+** required (3.11+ recommended)
- **Git** for version control
- **just** (optional but recommended) - Task runner for common commands
- **[Add project-specific prerequisites]**

### Installation

```bash
# Clone repository
git clone https://github.com/liminalcommons/test-docs-standard.git
cd test-docs-standard

# One-command setup (recommended)
./scripts/setup.sh

# Manual setup alternative
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install
```

### Environment Variables

Create a `.env` file in project root:

```env
# Application configuration
TEST_DOCS_STANDARD_LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR, CRITICAL
TEST_DOCS_STANDARD_DEBUG=0             # Set to 1 for debug mode

# Add your environment variables here
```

### Client Configuration

#### Claude Desktop (macOS)

**Development Mode (Editable Install):**
```json
{
  "mcpServers": {
    "test-docs-standard-dev": {
      "command": "/path/to/test-docs-standard/.venv/bin/python",
      "args": ["-m", "test_docs_standard.server"],
      "cwd": "/path/to/test-docs-standard",
      "env": {
        "TEST_DOCS_STANDARD_DEBUG": "1"
      }
    }
  }
}
```

**Production Mode (Installed Package):**
```json
{
  "mcpServers": {
    "test-docs-standard": {
      "command": "test-docs-standard",
      "args": [],
      "env": {}
    }
  }
}
```

**Config file location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Cursor

See `.config/cursor-mcp.example.json` for complete examples.

**Config file location:** `~/.cursor/mcp.json`

---

## Testing Instructions

### Run All Tests

```bash
# Using just (recommended)
just test

# Direct pytest
pytest

# With coverage report
just test-coverage
# OR
pytest --cov=test_docs_standard --cov-report=term-missing
```

### Smoke Tests (Quick Validation)

```bash
# Fast smoke tests (<30 seconds)
just smoke

# Direct pytest
pytest tests/smoke/ -v
```

### Test Categories

```bash
# Unit tests only
pytest tests/ -k "not integration and not smoke" -v

# Integration tests
pytest tests/integration/ -v

# Specific test file
pytest tests/test_example.py -v

# Specific test function
pytest tests/test_example.py::test_function -v
```

### Pre-Commit Hooks

```bash
# Run all pre-commit checks
just pre-commit
# OR
pre-commit run --all-files

# Install hooks (one-time setup)
pre-commit install

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

### Linting & Type Checking

```bash
# All quality checks (lint + typecheck + format)
just check

# Individual checks
just lint       # Ruff linting
just typecheck  # Mypy type checking
just format     # Ruff formatting

# Manual commands
ruff check src/test_docs_standard tests/
mypy src/test_docs_standard
ruff format src/test_docs_standard tests/

# Auto-fix linting issues
ruff check --fix src/test_docs_standard tests/
```

### Coverage Requirements

- **Overall coverage:** ≥85%
- **Critical paths:** 100% ([list critical paths])
- **[Module name]:** ≥90% ([describe module])

### Pre-Merge Verification

```bash
# Full verification before submitting PR
just pre-merge

# Equivalent to:
# - pre-commit run --all-files
# - pytest (smoke + full test suite)
# - coverage check
```

---

## PR Instructions

### Branch Naming

```
feature/descriptive-name     # New features
fix/issue-description        # Bug fixes
hotfix/critical-fix          # Production hotfixes
docs/documentation-update    # Documentation only
refactor/code-improvement    # Refactoring
```

### Commit Message Format

Follow **Conventional Commits** style:

```
type(scope): brief description

Detailed explanation of changes (if needed)

Closes #issue-number
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

**Scopes:** [List your project-specific scopes]

**Examples:**
```
feat(core): add new feature X

Implement feature X with comprehensive error handling
and unit tests.

Closes #23

---

fix(server): handle edge case gracefully

When [condition], system now [behavior] instead of
crashing.

Fixes #45
```

### PR Checklist

**Before opening PR:**
- [ ] Branch is up to date with `main`
- [ ] All tests pass locally (`just test`)
- [ ] Coverage maintained or improved (≥85%)
- [ ] Linting passes (`just lint`)
- [ ] Type checking passes (`just typecheck`)
- [ ] Pre-commit hooks pass (`just pre-commit`)
- [ ] Code formatted (`just format`)
**Documentation (if applicable):**
- [ ] README.md updated (if user-facing changes)
- [ ] AGENTS.md updated (if agent workflow changes)
- [ ] API reference docs updated (if new tools/capabilities)
- [ ] CHANGELOG.md entry added (for releases)

**Testing:**
- [ ] Unit tests added/updated
- [ ] Integration tests added (if applicable)
- [ ] Smoke tests pass (`just smoke`)
- [ ] Manual testing completed

**Review:**
- [ ] Self-review completed
- [ ] Code follows project style guide
- [ ] No debug code or commented-out code
- [ ] Error messages are clear and actionable
- [ ] Logging statements use appropriate levels

### Quality Gates (must pass)

1. **Lint:** `ruff check` → No errors
2. **Format:** `ruff format --check` → Formatted
3. **Types:** `mypy` → Type safe
4. **Tests:** All tests pass
5. **Coverage:** ≥85%
6. **Pre-commit:** All hooks pass

### PR Review Process

- **Required approvals:** 1+ reviewer
- **Merge strategy:** Squash and merge (clean history)
- **CI/CD:** All quality gates must pass
- **Timeline:** Most PRs reviewed within 24-48 hours

---

## Architecture Overview

[Describe your project's architecture here. Include diagrams, key design patterns, and architectural decisions.]

### Key Design Patterns

- **[Pattern 1]:** [Description]
- **[Pattern 2]:** [Description]
- **[Pattern 3]:** [Description]

### Configuration Management

[Describe how configuration works in your project, including environment variables, config files, etc.]

---

## Key Constraints & Design Decisions

### Target Audience

A Python project built with chora-base template

**CRITICAL:** test-docs-standard is designed for **LLM-intelligent MCP clients** (Claude Desktop, Cursor, Roo Code).

- ✅ **FOR LLM agents** - Claude Desktop, Cursor, custom MCP clients
- ✅ **FOR programmatic use** - Python API, automation workflows
- ❌ **NOT for human CLI users** - No interactive wizards or watch modes

**Implication:** All features prioritize agent ergonomics over human UX.

### [Additional Constraints]

[Document your project-specific constraints and design decisions here.]

---

## Strategic Design

### Balancing Current Priorities with Future Vision

**The Balance:**
- ✅ **Deliver:** Ship current commitments on time
- ✅ **Design for evolution:** Keep future doors open (extension points)
- ✅ **Refactor strategically:** When it serves both present and future
- ❌ **NOT:** Premature optimization, gold plating, scope creep

**Key Insight:** Build for today, design for tomorrow. Don't implement Wave 2 features in Wave 1, but don't paint yourself into corners either.

### Vision-Aware Implementation Pattern

**When implementing features, ask:**

1. **Architecture Check:** "Does this design block future capabilities in [dev-docs/vision/](dev-docs/vision/)?"
   - ✅ YES → Refactor before implementing
   - ✅ NO → Proceed

2. **Refactoring Signal:** "Should I refactor this now?"
   ```
   ┌─────────────────────────────────────────────────────┐
   │ Does it help current work (Wave 1)?                 │
   │   NO → DEFER (focus on current deliverables)       │
   │   YES → Continue ↓                                  │
   ├─────────────────────────────────────────────────────┤
   │ Does it unblock future capabilities?                │
   │   YES → LIKELY REFACTOR (strategic investment)     │
   │   NO → Continue ↓                                   │
   ├─────────────────────────────────────────────────────┤
   │ Cost vs. benefit?                                    │
   │   HIGH COST → DEFER (wait for Wave 2 commitment)   │
   │   LOW COST → REFACTOR (small prep, big payoff)     │
   └─────────────────────────────────────────────────────┘
   ```

3. **Decision Documentation:** Where to record decisions
- **Knowledge notes:** `test_docs_standard-memory knowledge create "Decision: [topic]"`
   - **Tags:** Use `architecture`, `vision`, `wave-N` tags for discoverability
### Practical Examples

**Example: Building Tool Interface**

**Scenario:** Wave 1 needs simple tool responses. Wave 2 vision includes tool chaining.

**❌ DON'T (Premature Optimization):**
```python
# DON'T build tool chaining now
async def get_data(query: str) -> str:
    # Implements full chaining system (Wave 2 feature)
    return chain_tools([tool_a, tool_b])(query)  # Not needed yet!
```

**✅ DO (Extension Point):**
```python
# DO return structured data (enables future chaining)
async def get_data(query: str) -> dict:
    """Returns structured response (extensible for Wave 2)."""
    return {
        "result": process_query(query),
        "metadata": {"timestamp": now(), "version": "1.0"}
    }
    # Wave 2 can add: "next_tool": "tool_b", "chain_id": "..."
```

### Refactoring Decision Framework

**Use this checklist before refactoring:**

- [ ] **Current Work:** Does this help Wave 1 deliverables?
- [ ] **Future Vision:** Check [dev-docs/vision/](dev-docs/vision/) - does this prepare for next wave?
- [ ] **Cost Assessment:** Low cost (<2 hours) or high cost (>1 day)?
- [ ] **Decision:** Apply framework above → Refactor now or defer?
- [ ] **Documentation:** Record decision (knowledge note)

### Capturing Knowledge for Future Agents

**Use A-MEM (Agentic Memory) patterns:**

1. **Emit Events:** Track architectural decisions
   ```python
   from test_docs_standard.memory import emit_event

   emit_event(
       event_type="architecture.decision",
       data={
           "decision": "Use dict returns for tool extensibility",
           "rationale": "Enables Wave 2 tool chaining",
           "wave": "wave-2-preparation"
       },
       status="success"
   )
   ```

2. **Create Knowledge Notes:**
   ```bash
   echo "Decision: Tool Response Format

   Context: Wave 1 tools return simple data, Wave 2 vision includes tool chaining.

   Decision: Return dict (not str) from all tools.

   Rationale:
   - Low cost refactor (1 hour)
   - Unblocks Wave 2 tool chaining
   - Backward compatible (wrap str in dict)

   Tags: architecture, vision, wave-2, tools
   " | test_docs_standard-memory knowledge create "Tool Response Format"
   ```

3. **Link to Vision:**
   - Reference vision waves in knowledge notes
   - Tag notes with `wave-N` for future discoverability
   - Query past decisions: `test_docs_standard-memory knowledge search --tag wave-2`

### Quick Reference: Strategic Design Checklist

**Before implementing any feature:**

1. ✅ **Check ROADMAP.md:** Is this in current committed work?
2. ✅ **Check vision:** Does this align with evolutionary direction?
3. ✅ **Apply framework:** Refactor now or defer? (use flowchart above)
4. ✅ **Document:** Record decision for future agents
5. ✅ **Code:** Implement with extension points, not future features

**Remember:** Deliver today, design for tomorrow. No gold plating!

---

## Common Tasks for Agents

### Task Discovery (START HERE)

**First step when working in this project: Discover available tasks**

```bash
just --list
```

This provides a machine-readable catalog of all development tasks.

**Why `just` for agents:**
- **Self-documenting**: `just --list` reveals all tasks instantly (no prose parsing)
- **Consistent**: Same commands across all chora-base projects
- **Structured**: Machine-parseable task catalog
- **Composable**: `just --show <task>` reveals implementation details
- **Transferable**: Commands learned here work in all chora-base projects

**Pattern**: Always start with `just --list` when working in a new chora-base project. Store commands as ecosystem-wide patterns, not project-specific.

**Example workflow:**
```bash
# Discover tasks
just --list
# Output: test, lint, pre-merge, build, etc.

# Understand a specific task
just --show pre-merge
# Output: shows it runs ./scripts/pre-merge.sh

# Execute
just pre-merge
```

**Memory note**: Store as:
```json
{
  "ecosystem": "chora-base",
  "discovery_command": "just --list",
  "common_tasks": {
    "test": "just test",
    "pre_merge": "just pre-merge",
    "build": "just build"
  },
  "applies_to": "all_chora_base_projects"
}
```

This knowledge transfers to mcp-n8n, chora-compose, and all future chora-base projects.

### Adding a New MCP Tool

1. Create tool function in `src/test_docs_standard/tools/your_tool.py`
2. Register tool with `@mcp.tool()` decorator
3. Add memory integration (emit events)
4. Add unit test in `tests/unit/test_your_tool.py`
5. Add integration test with memory validation
6. Update README.md tool list
7. Run tests: `just test`

**Example:**
```python
from test_docs_standard.memory import emit_event, TraceContext
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-docs-standard")

@mcp.tool()
async def your_tool(param: str) -> dict:
    """Your tool description.

    Args:
        param: Parameter description

    Returns:
        Result dictionary
    """
# Emit start event
    emit_event("tool.your_tool.started", status="pending", metadata={"param": param})

try:
        # Your tool logic here
        result = process(param)
# Emit success event
        emit_event("tool.your_tool.completed", status="success", metadata={"result_count": len(result)})
return {"success": True, "data": result}
    except Exception as e:
# Emit failure event
        emit_event("tool.your_tool.failed", status="failure", metadata={"error": str(e)})
return {"success": False, "error": str(e)}
```

### Running Tests for Specific Module

```bash
# Test specific module
pytest tests/test_test_docs_standard_module.py -v

# Test with coverage for module
pytest tests/test_module.py --cov=test_docs_standard.module --cov-report=term-missing

# Test specific function
pytest tests/test_module.py::test_function_name -vv

# Run with debugger on failure
pytest tests/test_module.py --pdb
```

### Agent Self-Service: Learning from Past Errors

**When encountering a problem you've seen before:**

1. **Query past events** to find similar failures
2. **Search knowledge** for documented solutions
3. **Review related notes** via bidirectional links
4. **Apply the solution** from past learning
5. **Record outcome** to improve knowledge base

**Example workflow:**

```bash
# Problem: Tool failing with "rate limit exceeded"

# Step 1: Query past rate limit failures
test-docs-standard-memory query --type "tool.failed" --since 30d | grep "rate limit"

# Step 2: Search knowledge base
test-docs-standard-memory knowledge search --tag rate-limits --tag troubleshooting

# Step 3: Show specific solution note
test-docs-standard-memory knowledge show rate-limit-handling

# Step 4: Apply exponential backoff solution (from knowledge note)
# ... implement fix ...

# Step 5: Record successful outcome
echo "Applied exponential backoff from rate-limit-handling note.
Rate limit errors reduced from 50/day to 2/day (96% improvement).
Solution: Added retry logic with delays [1s, 2s, 4s, 8s]." | \
  test-docs-standard-memory knowledge create "Rate Limit Fix - Exponential Backoff Success" \
    --tag rate-limits --tag performance --tag solved --confidence high

# Step 6: Link to original problem note
test-docs-standard-memory knowledge link rate-limit-handling rate-limit-fix-success
```

### Agent Self-Service: Creating Knowledge from Debugging

**When you solve a non-obvious problem:**

```bash
# After fixing a tricky bug, create knowledge note

# 1. Create note with problem context
echo "## Problem
Tool X was failing intermittently with 'connection timeout'.

## Investigation
- Analyzed events: test-docs-standard-memory query --type tool.x.failed --since 7d
- Found pattern: Failures only during peak hours (9am-5pm)
- Root cause: Connection pool exhaustion (max 10 connections)

## Solution
Increased connection pool size to 50 in config.
Added connection pool monitoring.

## Validation
- Ran load test: 100 concurrent requests
- Zero timeouts after fix
- Connection pool usage: avg 15/50 (healthy headroom)

## Related
- Connection pool settings: [link to config docs]
- Load testing guide: [link to testing docs]" | \
  test-docs-standard-memory knowledge create "Tool X Connection Timeout Fix" \
    --tag connection-pool --tag timeout --tag performance --confidence high

# 2. Tag for future retrieval
test-docs-standard-memory knowledge tag connection-timeout-fix production-issues

# 3. Link to related notes
test-docs-standard-memory knowledge link connection-timeout-fix connection-pool-config
```

**Benefits of creating knowledge:**
- Future sessions can query this solution
- Avoid repeating the same debugging work
- Build cumulative expertise over time
- Share learnings across agent instances

### Debugging Common Issues

```bash
# Check logs
just logs  # If justfile has log task
# OR
tail -f logs/test_docs_standard.log

# Test single component
python -m test_docs_standard.module_name

# Check environment
env | grep TEST_DOCS_STANDARD

# Validate configuration
python -c "from test_docs_standard import config; print(config)"
```

### Fixing Linting/Type Errors

```bash
# Auto-fix linting issues
ruff check --fix src/test_docs_standard

# Format code
ruff format src/test_docs_standard

# Check types and show errors
mypy src/test_docs_standard --pretty --show-error-codes

# Fix specific type error
# Add type: ignore[error-code] comment to problematic line
```


### Design Decision: Check Against Vision

**When:** Before making architectural decisions or significant refactors

**Steps:**

1. **Check current priority:**
   ```bash
   cat ROADMAP.md | head -50
   # Current: [Your current sprint/milestone]
   ```

2. **Check long-term vision:**
   ```bash
   cat dev-docs/vision/CAPABILITY_EVOLUTION.md | head -100
   # Future waves: [Your capability themes]
   ```

3. **Apply decision framework:**
   - **Does this help current work?** (YES → continue)
   - **Does this align with vision?** (YES → good sign)
   - **Cost vs. benefit?** (LOW COST → likely proceed)

4. **Document decision:**
```bash
   # Create knowledge note
   echo "Decision: [Your decision]

   Context: [Current situation]

   Decision: [What you decided]

   Rationale:
   - Helps Wave 1 deliverables: [How]
   - Aligns with Wave 2 vision: [Which capability]
   - Low cost: [Effort estimate]

   Outcome: [Expected result]

   Tags: architecture, vision, wave-N, decision
   " | test_docs_standard-memory knowledge create "Decision: [Topic]"
   ```
5. **Link to vision:**
   - If prepares for future waves, note it in documentation
- Add tags to knowledge notes for discoverability: `wave-2`, `architecture`, `vision`
- Update vision document if decision affects feasibility

**Example Decision:**

**Scenario:** Should we refactor tool responses from `str` to `dict`?

1. **Current work:** Wave 1 needs simple responses → `str` works
2. **Vision:** Wave 2 includes tool chaining → needs structured data (`dict`)
3. **Cost:** Low (1-2 hours to refactor)
4. **Decision:** ✅ REFACTOR NOW (serves both present and future)

---

## Project Structure

```
test-docs-standard/
├── src/test_docs_standard/       # Main source code
│   ├── __init__.py
│   ├── server.py               # MCP server entry point
│   ├── memory/                 # Agent memory system
│   │   ├── event_log.py
│   │   ├── knowledge_graph.py
│   │   └── trace.py
│   └── [your modules]
├── tests/                      # Test suite
│   ├── smoke/                  # Smoke tests (<30s)
│   ├── integration/            # Integration tests
│   └── test_*.py               # Unit tests
├── scripts/                    # Automation scripts
│   ├── setup.sh                # One-command setup
│   ├── venv-create.sh          # Create virtual environment
│   └── [other scripts]
├── docs/                       # Documentation
│   ├── DEVELOPMENT.md          # Developer deep dive
│   └── TROUBLESHOOTING.md      # Problem-solution guide
├── .github/workflows/          # CI/CD pipelines
│   ├── test.yml                # Test workflow
│   └── lint.yml                # Lint workflow
├── .chora/memory/              # Agent memory (gitignored)
│   ├── README.md               # Memory architecture docs
│   ├── events/                 # Event log (JSONL format)
│   ├── knowledge/              # Knowledge notes (YAML frontmatter)
│   │   ├── notes/*.md          # Individual notes
│   │   ├── links.json          # Bidirectional links
│   │   └── tags.json           # Tag index
│   └── profiles/               # Agent-specific profiles
├── pyproject.toml              # Python packaging & tool config
├── justfile                    # Task runner commands
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
├── README.md                   # Human-readable project overview
├── AGENTS.md                   # This file (machine-readable instructions)
├── CONTRIBUTING.md             # Contribution guidelines
└── LICENSE                     # MIT license
```

### Knowledge Note Metadata Standards

Knowledge notes (`.chora/memory/knowledge/notes/*.md`) use **YAML frontmatter** following Zettelkasten best practices for machine-readable metadata.

**Required Frontmatter Fields:**
- `id`: Unique note identifier (kebab-case)
- `created`: ISO 8601 timestamp
- `updated`: ISO 8601 timestamp
- `tags`: Array of topic tags for search/organization

**Optional Frontmatter Fields:**
- `confidence`: `low` | `medium` | `high` - Solution reliability
- `source`: `agent-learning` | `human-curated` | `external` | `research`
- `linked_to`: Array of related note IDs (bidirectional linking)
- `status`: `draft` | `validated` | `deprecated`
- `author`: Agent or human creator
- `related_traces`: Array of trace IDs that led to this knowledge

**Example Knowledge Note:**

```markdown
---
id: api-timeout-solution
created: 2025-01-17T10:00:00Z
updated: 2025-01-17T12:30:00Z
tags: [troubleshooting, api, performance]
confidence: high
source: agent-learning
linked_to: [connection-pool-tuning, retry-patterns]
status: validated
author: claude-code
related_traces: [abc123, def456]
---

# API Timeout Solution

## Problem
API calls timing out after 30s during high load...

## Solution
Increase timeout to 60s and implement retry with exponential backoff...

## Evidence
- Trace abc123: Successful completion at 45s
- Trace def456: Successful completion at 52s
- Load test: 98% success rate with new settings
```

**Why YAML Frontmatter?**
- ✅ **Semantic Search**: Query by confidence, tags, or date (`grep "confidence: high"`)
- ✅ **Tool Compatibility**: Works with Obsidian, Zettlr, LogSeq, Foam
- ✅ **Knowledge Graph**: Enables bidirectional linking and visualization
- ✅ **Agent Decision-Making**: Filter by confidence level for solution reliability

**Reference:** See [.chora/memory/README.md](.chora/memory/README.md) for complete schema documentation.

---

## Documentation Philosophy

### Diátaxis Framework

test-docs-standard documentation follows the [Diátaxis framework](https://diataxis.fr/), serving **two first-class audiences**:

1. **Human Developers** - Learning, understanding, decision-making
2. **AI Agents** - Task execution, reference lookup, machine-readable instructions

**Four Quadrants:**

| Type | Purpose | Primary Audience | When to Use |
|------|---------|------------------|-------------|
| **Tutorials** | Learning-oriented | Humans (new users) | "I want to learn how test-docs-standard works" |
| **How-To Guides** | Task-oriented | Humans + Agents | "I want to accomplish a specific task" |
| **Reference** | Information-oriented | Humans + Agents | "I need to look up a fact/command/API" |
| **Explanation** | Understanding-oriented | Humans | "I want to understand why/how this works" |

### For AI Agents (Recommended Reading Order)

**When starting work on test-docs-standard:**

1. **Start here:** AGENTS.md (this file) - Machine-readable project instructions
2. **Quick reference:** How-To Guides - Executable task recipes
   - How to add new features
   - How to run tests
   - How to deploy
3. **Lookup facts:** Reference Docs - API specs, configuration options, commands
4. **Skip:** Tutorials (for human learning) and Explanations (conceptual background)

**Example: Agent workflow for "Add new feature X"**

```bash
# 1. Read AGENTS.md section: "Common Tasks for Agents" → "Adding a New MCP Tool"
# 2. Follow steps 1-7 (create file, register tool, add tests, etc.)
# 3. If unclear on testing: Consult "Testing Instructions" section in AGENTS.md
# 4. If need API reference: Read relevant module docstrings or Reference docs
# 5. Run pre-merge: `just pre-merge` (from AGENTS.md "Pre-Merge Verification")
```

### For Human Developers (Recommended Learning Path)

**New to test-docs-standard:**

1. **README.md** - Project overview, quick start (5 minutes)
2. **Tutorial** - Guided learning experience (30-60 minutes)
3. **DEVELOPMENT.md** - Developer deep dive (architecture, debugging)
4. **How-To Guides** - Task-specific recipes (as needed)
5. **Reference Docs** - Lookup API details (as needed)
6. **Explanation Docs** - Understand design decisions (optional)

### Documentation Hierarchy

```
docs/
├── README.md                   # Human entry point (project overview)
├── AGENTS.md                   # Agent entry point (this file)
├── CONTRIBUTING.md             # Human contributor guide
├── DEVELOPMENT.md              # Developer deep dive
├── TROUBLESHOOTING.md          # Problem-solution guide
└── [additional docs]/
```

**Quick Reference:**

- **For agents:** AGENTS.md → How-To Guides → Reference Docs
- **For humans:** README → Tutorials → How-To Guides → Explanations

### DDD/BDD/TDD Workflow

This project follows the Chora ecosystem's integrated DDD/BDD/TDD workflow:

1. **DDD Phase** - Write API reference docs FIRST (documentation-driven design)
2. **BDD Phase** - Write scenarios SECOND (behavior-driven development)
3. **TDD Phase** - Red-Green-Refactor THIRD (test-driven development)
4. **CI Phase** - Automated quality gates
5. **Merge & Release** - Semantic versioning

**Why this order matters:**

- **Docs first** ensures clear API design before implementation
- **Scenarios second** captures expected behavior as executable specs
- **Tests third** drives implementation with fast feedback loop
- **CI validates** all quality gates pass before merge
- **Semantic versioning** communicates changes to users

**For agents:** Follow this workflow when adding new features. Write docs → scenarios → tests → implementation.

---

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python --version  # Must be 3.11+

# Check virtual environment
which python  # Should be .venv/bin/python

# Reinstall dependencies
./scripts/venv-create.sh

# Check environment variables
cat .env

# Test application directly
python -m test_docs_standard.server
```

### Test Failures

```bash
# Run specific test with verbose output
pytest tests/test_example.py::test_function -vvs

# Show full error trace
pytest --tb=long

# Run with debugger
pytest --pdb

# Check test coverage
pytest --cov=test_docs_standard --cov-report=term-missing

# Clean test cache
pytest --cache-clear
rm -rf .pytest_cache __pycache__
```

### Type Checking Errors

```bash
# Run mypy with verbose output
mypy src/test_docs_standard --show-error-codes --pretty

# Check specific file
mypy src/test_docs_standard/[module].py

# Ignore specific error (if intentional)
# Add to line:
# type: ignore[error-code]

# Update mypy configuration
# Edit [tool.mypy] in pyproject.toml
```

### Coverage Drop

```bash
# Show missing coverage lines
pytest --cov=test_docs_standard --cov-report=term-missing

# Generate HTML report
pytest --cov=test_docs_standard --cov-report=html
open htmlcov/index.html

# Check coverage for specific module
pytest --cov=test_docs_standard.[module] --cov-report=term-missing

# Identify untested code
coverage report --show-missing
```

### Pre-Commit Hook Failures

```bash
# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files

# Update hook versions
pre-commit autoupdate

# Bypass hooks (emergency only, NOT recommended)
git commit --no-verify

# Clear pre-commit cache
pre-commit clean
```

### Memory CLI Errors

**Problem: Memory commands not found**

```bash
# Verify CLI installation
which test-docs-standard-memory
# Expected: .venv/bin/test-docs-standard-memory

# If missing, reinstall package with CLI
pip install -e .

# Verify entry point in pyproject.toml
grep -A 5 "\[project.scripts\]" pyproject.toml
# Should contain: test-docs-standard-memory = "test_docs_standard.cli.memory:main"
```

**Problem: Query returns empty results**

```bash
# Check event log directory
ls -la .chora/memory/events/
# Expected: Monthly directories (e.g., 2025-01/)

# Check events file exists and has content
cat .chora/memory/events/$(date +%Y-%m)/events.jsonl | wc -l
# If 0, no events emitted yet

# Emit test event to verify system
python -c "from test_docs_standard.memory import emit_event; emit_event('test.verify', status='success')"

# Query again
test-docs-standard-memory query --type test.verify
# Should show test event
```

**Problem: JSON parsing errors from CLI**

```bash
# Validate JSONL format in event log
python -c "
import json
with open('.chora/memory/events/2025-01/events.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'Line {i} invalid: {e}')
"

# If corrupted, backup and recreate
mv .chora/memory/events/2025-01/events.jsonl .chora/memory/events/2025-01/events.jsonl.backup
touch .chora/memory/events/2025-01/events.jsonl
```

### Event Log Troubleshooting

**Problem: Events not appearing in queries**

```bash
# 1. Verify event emission
python -c "
from test_docs_standard.memory import emit_event
print('Emitting test event...')
emit_event('debug.test', status='success', metadata={'test': 'value'})
print('Event emitted successfully')
"

# 2. Check event log file was written
ls -lh .chora/memory/events/$(date +%Y-%m)/events.jsonl
# Size should increase after emission

# 3. View raw event log
tail -5 .chora/memory/events/$(date +%Y-%m)/events.jsonl

# 4. Query with verbose output
test-docs-standard-memory query --type debug.test --json | python -m json.tool
```

**Problem: Trace correlation not working**

```bash
# Verify CHORA_TRACE_ID environment variable
echo $CHORA_TRACE_ID
# Should be UUID format if set by TraceContext

# Emit event with explicit trace_id
python -c "
from test_docs_standard.memory import emit_event, TraceContext
with TraceContext() as trace_id:
    print(f'Trace ID: {trace_id}')
    emit_event('test.trace', trace_id=trace_id, status='success')
"

# Query by trace_id
test-docs-standard-memory trace <TRACE_ID>
# Should show all events with that trace_id
```

**Problem: Event log too large / performance issues**

```bash
# Check total event count
cat .chora/memory/events/*/events.jsonl | wc -l

# Archive old events (older than 90 days)
mkdir -p .chora/memory/archive
find .chora/memory/events -type d -name "2024-*" -exec mv {} .chora/memory/archive/ \;

# Query stats for retention analysis
test-docs-standard-memory stats --since 90d
# Review event types, identify noise (e.g., excessive debug events)
```

### Knowledge Graph Troubleshooting

**Problem: Knowledge notes not found in search**

```bash
# 1. List all knowledge notes
ls -la .chora/memory/knowledge/notes/
# Check if note file exists

# 2. Verify note format (YAML frontmatter + markdown)
cat .chora/memory/knowledge/notes/my-note.md
# Expected format:
# ---
# id: my-note
# title: My Note
# tags: [tag1, tag2]
# confidence: medium
# created: 2025-01-17T10:00:00Z
# updated: 2025-01-17T10:00:00Z
# ---
# Content here

# 3. Rebuild tag index if corrupted
python -c "
from test_docs_standard.memory.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
kg._rebuild_tag_index()  # Internal method - use with caution
print('Tag index rebuilt')
"

# 4. Search again
test-docs-standard-memory knowledge search --tag my-tag
```

**Problem: Broken bidirectional links**

```bash
# Check links.json structure
cat .chora/memory/knowledge/links.json | python -m json.tool

# Expected format:
# {
#   "note-a": ["note-b", "note-c"],
#   "note-b": ["note-a"],
#   "note-c": ["note-a"]
# }

# Verify linked notes exist
python -c "
import json
with open('.chora/memory/knowledge/links.json') as f:
    links = json.load(f)
    for note, targets in links.items():
        print(f'{note} → {targets}')
        for target in targets:
            path = f'.chora/memory/knowledge/notes/{target}.md'
            if not __import__('os').path.exists(path):
                print(f'  WARNING: {target} does not exist')
"

# Fix broken links
test-docs-standard-memory knowledge link note-a note-b  # Recreate link
```

**Problem: Tag corruption or duplicates**

```bash
# View tag index
cat .chora/memory/knowledge/tags.json | python -m json.tool

# Find duplicate tags (case-sensitive)
cat .chora/memory/knowledge/tags.json | python -c "
import json, sys
tags = json.load(sys.stdin)
seen = {}
for tag in tags.keys():
    lower = tag.lower()
    if lower in seen:
        print(f'Duplicate: {tag} vs {seen[lower]}')
    seen[lower] = tag
"

# Merge tags if needed
test-docs-standard-memory knowledge search --tag old-tag
# Create notes with new standardized tag
# Manually remove old tag from tag index
```

### Trace Context Troubleshooting

**Problem: CHORA_TRACE_ID not propagating to subprocesses**

```bash
# Verify TraceContext sets environment variable
python -c "
from test_docs_standard.memory import TraceContext
import os
with TraceContext() as trace_id:
    print(f'Inside context: {os.environ.get(\"CHORA_TRACE_ID\")}')
    # Should match trace_id
print(f'Outside context: {os.environ.get(\"CHORA_TRACE_ID\")}')
# Should be None or previous value
"

# Test subprocess propagation
python -c "
from test_docs_standard.memory import TraceContext
import subprocess, os
with TraceContext() as trace_id:
    result = subprocess.run(
        ['python', '-c', 'import os; print(os.environ.get(\"CHORA_TRACE_ID\"))'],
        capture_output=True,
        text=True
    )
    print(f'Trace ID: {trace_id}')
    print(f'Subprocess saw: {result.stdout.strip()}')
    # Should match
"
```

**Problem: Multiple overlapping trace contexts**

```bash
# Anti-pattern: Nested TraceContext (avoid this)
# python -c "
# from test_docs_standard.memory import TraceContext
# with TraceContext() as trace_1:  # Outer context
#     with TraceContext() as trace_2:  # Inner context overrides
#         emit_event('test')  # Uses trace_2, loses trace_1
# "

# Correct pattern: Single TraceContext per workflow
python -c "
from test_docs_standard.memory import TraceContext, emit_event
with TraceContext() as trace_id:
    emit_event('workflow.started', trace_id=trace_id)
    # ... all workflow steps ...
    emit_event('workflow.completed', trace_id=trace_id)
# Query workflow by trace_id
"
```

---

## Agent Memory System

### Overview

test-docs-standard includes a stateful memory infrastructure for cross-session learning and knowledge persistence, implementing A-MEM (Agentic Memory) principles.

**Memory capabilities:**
- **Event Log** - Append-only operation history with trace correlation
- **Knowledge Graph** - Structured learnings with Zettelkasten-style linking
- **Trace Context** - Multi-step workflow tracking via `CHORA_TRACE_ID`
- **Cross-Session Learning** - Avoid repeating mistakes across sessions

### Memory Location

All memory data stored in `.chora/memory/`:

```
.chora/memory/
├── README.md                    # Memory architecture documentation
├── events/                      # Event log storage (monthly partitions)
│   ├── 2025-01/
│   │   ├── events.jsonl         # Daily aggregated events
│   │   └── traces/              # Per-trace details
│   └── index.json               # Event index (searchable)
├── knowledge/                   # Knowledge graph
│   ├── notes/                   # Individual knowledge notes
│   ├── links.json               # Note connections
│   └── tags.json                # Tag index
├── profiles/                    # Agent-specific profiles
└── queries/                     # Saved queries
```

**Privacy:** Memory directory is in `.gitignore` by default (contains ephemeral learning data, not source code).

### Event Log Usage

**Emit events during operations:**

```python
from test_docs_standard.memory import emit_event, TraceContext

# Start workflow with trace context
with TraceContext() as trace_id:
    # Emit operation events
    emit_event(
        "app.operation_completed",
        trace_id=trace_id,
        status="success",
        operation_name="example",
        duration_ms=1234
    )
```

**Query recent events:**

```python
from test_docs_standard.memory import query_events

# Find failures in last 24 hours
failures = query_events(
    event_type="app.operation_failed",
    status="failure",
    since_hours=24
)

# Analyze patterns
for failure in failures:
    error = failure["metadata"]["error"]
    print(f"Operation failed: {error}")
```

### Knowledge Graph Usage

**Create learning notes:**

```python
from test_docs_standard.memory import KnowledgeGraph

kg = KnowledgeGraph()

# Create note from learned pattern
note_id = kg.create_note(
    title="[Learning Title]",
    content="[Detailed learning content]",
    tags=["tag1", "tag2"],
    confidence="high"
)
```

**Search knowledge:**

```python
# Find notes by tag
notes = kg.search(tags=["error", "fix"])

# Find notes by content
notes = kg.search(text="timeout")

# Get related notes
related = kg.get_related("note-id", max_distance=2)
```

### CLI Tools for Agents

**Query events via bash:**

```bash
# Find recent failures
test-docs-standard-memory query --type "app.failed" --status failure --since "24h"

# Get all events from last 7 days
test-docs-standard-memory query --since "7d" --limit 100

# Get events as JSON for processing
test-docs-standard-memory query --type "app.started" --json
```

**Get trace timeline:**

```bash
# Show workflow timeline
test-docs-standard-memory trace abc123

# Get trace as JSON
test-docs-standard-memory trace abc123 --json
```

**Search and manage knowledge:**

```bash
# Find notes about errors
test-docs-standard-memory knowledge search --tag error

# Create knowledge note
echo "Fix content" | test-docs-standard-memory knowledge create "Title" --tag tag1 --confidence high

# Show note details
test-docs-standard-memory knowledge show note-id
```

**View statistics:**

```bash
# Stats for last 7 days
test-docs-standard-memory stats

# Stats for last 24 hours with JSON output
test-docs-standard-memory stats --since 24h --json
```

### A-MEM Self-Service Workflow (Agent Learning Loop)

**The agent learning loop implements A-MEM (Agentic Memory) principles:**

```
┌─────────────────────────────────────────────────────────┐
│  1. ENCOUNTER PROBLEM                                   │
│  Agent encounters error, unexpected behavior, or        │
│  performance issue during task execution                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. QUERY PAST EVENTS (Event Log)                       │
│  Search for similar failures in event history           │
│  test-docs-standard-memory query --type problem.type --since 30d  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. SEARCH KNOWLEDGE (Knowledge Graph)                  │
│  Find documented solutions in knowledge base            │
│  test-docs-standard-memory knowledge search --tag problem_domain  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. TRAVERSE LINKS (Bidirectional Navigation)           │
│  Follow related notes for deeper context                │
│  test-docs-standard-memory knowledge show note-id        │
│  (Shows linked notes in "Related" section)              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. APPLY SOLUTION                                       │
│  Implement the learned fix from knowledge base          │
│  (Code changes, config updates, etc.)                   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  6. VALIDATE OUTCOME                                     │
│  Test that solution resolves the problem                │
│  Run tests, check metrics, verify behavior              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  7. RECORD LEARNING (Memory Evolution)                   │
│  Create/update knowledge note with outcome              │
│  test-docs-standard-memory knowledge create "Solution Title"     │
│  Link to original problem note                          │
│  Tag for future retrieval                               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  8. CUMULATIVE IMPROVEMENT                               │
│  Future encounters of same problem → query knowledge    │
│  Faster resolution time (no re-debugging)               │
│  Build expertise over multiple sessions                 │
└─────────────────────────────────────────────────────────┘
```

**Example: Applying A-MEM Loop to Performance Issue**

```bash
# 1. ENCOUNTER PROBLEM
# Agent notices: API responses taking >5 seconds (slow)

# 2. QUERY PAST EVENTS
test-docs-standard-memory query --type "api.slow_response" --since 30d
# Output: Found 15 events of slow responses in past month

# 3. SEARCH KNOWLEDGE
test-docs-standard-memory knowledge search --tag performance --tag api
# Output: Found 3 notes: "API Caching Strategy", "Connection Pool Tuning", "Query Optimization"

# 4. TRAVERSE LINKS
test-docs-standard-memory knowledge show api-caching-strategy
# Output shows:
# ## API Caching Strategy
# Problem: API responses slow due to repeated database queries
# Solution: Implemented Redis caching with 5-minute TTL
# Validation: Response time reduced from 5s to 200ms (96% improvement)
# Related: connection-pool-tuning, query-optimization

# 5. APPLY SOLUTION
# Implement Redis caching based on knowledge note guidance
# ... code changes ...

# 6. VALIDATE OUTCOME
# Run load test, measure response times
# Result: Response time now 180ms (97% improvement vs original 5s)

# 7. RECORD LEARNING
echo "## Context
Applied Redis caching to API endpoints based on 'API Caching Strategy' note.

## Implementation
- Added Redis client with 5-minute TTL
- Cached GET endpoints for /users, /products, /orders
- Cache invalidation on POST/PUT/DELETE

## Outcome
- Response time: 5s → 180ms (97% faster)
- Database load: -80% (queries cached)
- Redis memory usage: ~50MB (within budget)

## Refinement from Original
Original note used 5-minute TTL. Found 10-minute TTL works better for this use case.
Updated cache invalidation logic to be more granular.

## Related
- api-caching-strategy (original guide)
- connection-pool-tuning (complementary optimization)
- redis-configuration (cache config details)" | \
  test-docs-standard-memory knowledge create "API Caching - Production Implementation" \
    --tag performance --tag api --tag caching --tag production --confidence high

# 8. CUMULATIVE IMPROVEMENT
# Link back to original note
test-docs-standard-memory knowledge link api-caching-strategy api-caching-production

# Tag for production issues
test-docs-standard-memory knowledge tag api-caching-production solved production-win

# Future sessions encountering slow API will:
# 1. Query events → find "api.slow_response"
# 2. Search knowledge → find "API Caching - Production Implementation"
# 3. See 97% improvement outcome → high confidence solution
# 4. Apply immediately without re-debugging
```

**A-MEM Principles in Action:**

1. **Dynamic Organization** - Agent creates notes, tags, links (not pre-defined schema)
2. **Note Construction** - Structured format with Problem/Solution/Validation
3. **Bidirectional Linking** - Notes reference each other (knowledge graph)
4. **Memory Evolution** - New notes update/refine existing knowledge
5. **Cross-Session Learning** - Future sessions benefit from past learning
6. **Confidence Tracking** - High confidence solutions applied first

See [.chora/memory/README.md](.chora/memory/README.md) for complete memory architecture documentation.

---

## Related Resources

- **Repository:** https://github.com/liminalcommons/test-docs-standard
- **Chora Base Template:** https://github.com/liminalcommons/chora-base
- **Chora Composer:** https://github.com/liminalcommons/chora-composer
- **Chora Platform:** https://github.com/liminalcommons/chora-platform
- **MCP Specification:** https://modelcontextprotocol.io/
---

**Version:** 0.1.0
**Last Updated:** [Update date]
**Format:** AGENTS.md standard (OpenAI/Google/Sourcegraph)
🤖 Generated with [chora-base](https://github.com/liminalcommons/chora-base) template
