# Claude Development Guide - Developer Documentation

**Purpose:** Claude-specific patterns for contributing to mcp-orchestration development.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude patterns and [AGENTS.md](AGENTS.md) for generic developer guide.

---

## Quick Navigation

This directory contains developer documentation for mcp-orchestration contributors:

- **[CLAUDE.md](CLAUDE.md)** (this file) - Claude-specific contribution patterns
- **[AGENTS.md](AGENTS.md)** - Generic developer guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[vision/CLAUDE.md](vision/CLAUDE.md)** - Claude patterns for strategic vision work
- **[research/CLAUDE.md](research/CLAUDE.md)** - Claude patterns for research tasks

---

## Claude's Strengths for mcp-orchestration Development

### 1. Documentation-Driven Development (DDD)

Claude excels at writing clear, comprehensive documentation before code:

```markdown
"Document new MCP tool before implementing:

Tool: [name]
Purpose: [what it does]
Input schema: [Pydantic model]
Output schema: [return type]
Error cases: [exceptions]
Cryptographic requirements: [signing/verification]

Follow pattern in user-docs/reference/mcp-tools.md
Generate complete documentation first."
```

### 2. Wave-Based Development

Claude understands mcp-orchestration's wave-based evolution:

```markdown
"Starting Wave [X].[Y] development:

1. Load wave plan: project-docs/WAVE_1X_PLAN.md
2. Review previous wave retrospective
3. Check telemetry for recent issues
4. Load relevant AGENTS.md files

Context: We're building [feature] in Wave [X].[Y]
Previous waves: [list completed waves]
Next wave: [planned future work]"
```

### 3. Multi-Layer Architecture

Claude can work across mcp-orchestration's layered architecture:

```markdown
"Implement feature across layers:

1. Storage Layer (src/mcp_orchestrator/storage/):
   - Content-addressable storage changes
   - SHA-256 hash operations

2. Crypto Layer (src/mcp_orchestrator/crypto/):
   - Ed25519 signature operations
   - Verification logic

3. MCP Server (src/mcp_orchestrator/mcp/server.py):
   - Tool implementation
   - Input/output schemas

4. Tests (tests/):
   - Unit tests for each layer
   - Integration tests for full flow

Work through layers sequentially, test after each."
```

---

## DDD → BDD → TDD Workflow with Claude

### Pattern: Documentation-First Feature Development

```markdown
# Complete Feature Development Request

## Step 1: Documentation (DDD)
"Document new feature: [feature_name]

Create documentation in:
- user-docs/how-to/[feature].md (user guide)
- user-docs/reference/mcp-tools.md (tool reference)
- CHANGELOG.md (feature announcement)

Include:
- Purpose and use cases
- Input/output schemas
- Error conditions
- Examples with real data
- MCP Inspector screenshots (if applicable)

Don't implement yet - documentation first."

## Step 2: Behavior Definition (BDD)
"Based on documentation, define behavioral tests:

Create: tests/test_[feature].py

Test scenarios:
1. Happy path (valid input, expected output)
2. Edge cases (empty, None, boundary values)
3. Error conditions (invalid input, missing dependencies)
4. Integration (MCP tool → storage → crypto flow)

Use pytest fixtures from conftest.py
Don't implement feature yet - tests first."

## Step 3: Test-Driven Implementation (TDD)
"Now implement [feature] to make tests pass:

1. Write minimal implementation in src/mcp_orchestrator/
2. Run tests: pytest tests/test_[feature].py
3. Iterate until all tests pass
4. Refactor for quality
5. Verify coverage ≥85%

Follow patterns from existing code."

## Step 4: Verification
"Verify feature complete:

Checklist:
- [ ] Documentation written and reviewed
- [ ] All tests passing (pytest)
- [ ] Coverage ≥85% (pytest --cov)
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] Manual testing with MCP Inspector
- [ ] CHANGELOG.md updated
- [ ] Ready for PR"
```

---

## Contributing Patterns for Claude

### Pattern: Add New MCP Tool

```markdown
"Add new MCP tool to mcp-orchestration:

Tool: [tool_name]
Wave: [X].[Y]
Purpose: [description]

## Step 1: Documentation (DDD)
1. Document tool in user-docs/reference/mcp-tools.md
2. Create how-to guide: user-docs/how-to/[use-tool].md
3. Add to CHANGELOG.md (Unreleased section)

## Step 2: Tests (BDD/TDD)
1. Create tests/test_[tool_name].py
2. Test scenarios: happy path, edge cases, errors
3. Test MCP protocol compliance
4. Test storage/crypto integration

## Step 3: Implementation
1. Add tool to src/mcp_orchestrator/mcp/server.py
2. Implement with proper error handling
3. Add telemetry emission
4. Follow existing tool patterns

## Step 4: Integration
1. Test with MCP Inspector
2. Update tool count in server capabilities
3. Run full test suite
4. Update documentation if needed

Show me the implementation plan before starting."
```

### Pattern: Fix Bug with Root Cause Analysis

```markdown
"Debug and fix [issue]:

## Step 1: Reproduce
1. Create minimal reproduction case
2. Add failing test to tests/
3. Confirm test fails consistently

## Step 2: Root Cause Analysis
1. Check telemetry: var/telemetry/events.jsonl
2. Review recent commits: git log --oneline -20
3. Check related code paths
4. Identify root cause (not just symptom)

## Step 3: Fix
1. Implement fix in minimal scope
2. Verify test now passes
3. Ensure no regressions (full test suite)
4. Add additional tests for edge cases

## Step 4: Document
1. Add test documenting the bug
2. Update CHANGELOG.md if user-facing
3. Consider if documentation needs update

Document root cause and fix approach before implementing."
```

### Pattern: Refactor with Safety

```markdown
"Refactor [component] for [goal]:

## Step 1: Safety Net
1. Run full test suite - all must pass
2. Check coverage baseline
3. Create refactoring branch
4. Document current behavior

## Step 2: Incremental Refactoring
1. Make smallest possible change
2. Run tests after EACH change
3. Commit after each successful change
4. Never refactor multiple things at once

## Step 3: Verification
1. All tests still pass
2. Coverage unchanged or improved
3. Type checking passes (mypy)
4. Manual testing if behavior changed

## Step 4: Documentation
1. Update docstrings if interfaces changed
2. Update AGENTS.md if architecture changed
3. Add refactoring note to CHANGELOG.md

Show me refactoring steps before starting.
Proceed incrementally, testing after each change."
```

---

## Code Quality Standards

### Pattern: Request Code Review from Claude

```markdown
"Review my implementation before PR:

Code: [paste implementation]

Review criteria:
1. **Correctness**
   - Logic is correct
   - Edge cases handled
   - Error handling comprehensive

2. **Security**
   - No secrets in code
   - Cryptographic operations correct
   - Input validation proper

3. **Code Quality**
   - Follows project patterns
   - Clear variable names
   - Appropriate abstractions
   - No premature optimization

4. **Testing**
   - Coverage ≥85%
   - Tests are meaningful
   - Edge cases tested
   - Error paths tested

5. **Documentation**
   - Docstrings complete
   - Type hints present
   - User docs updated
   - CHANGELOG.md updated

Provide specific feedback with line numbers."
```

---

## Wave Development with Claude

### Pattern: Start New Wave

```markdown
"Starting Wave [X].[Y] development:

## Context Loading
1. Load wave plan: project-docs/WAVE_1X_PLAN.md
2. Review previous wave retrospective
3. Check current branch: git status
4. Load memory checkpoint: .chora/memory/sessions/

## Planning
1. Break wave into tasks
2. Estimate effort for each
3. Identify dependencies
4. Create task order

## Implementation Approach
1. DDD: Document all features first
2. BDD: Write all tests
3. TDD: Implement incrementally
4. Verify: Test after each feature

## Tracking
1. Create checkpoint daily
2. Emit telemetry for major steps
3. Update CHANGELOG.md as we go
4. Document decisions in wave retrospective

Ready to start Wave [X].[Y]?"
```

### Pattern: Complete Wave

```markdown
"Completing Wave [X].[Y]:

## Pre-Release Checklist
1. All features implemented and tested
2. Documentation complete (user-docs/)
3. CHANGELOG.md updated with all changes
4. All tests passing (≥85% coverage)
5. Type checking passes (mypy)
6. Linting passes (ruff)
7. Manual testing complete

## Wave Retrospective
Create: .chora/memory/retrospectives/wave-[X]-[Y].md

Content:
- What went well
- What challenges we faced
- What we'd do differently
- Patterns to reuse
- Technical debt created
- Lessons for next wave

## Release Preparation
1. Update version in pyproject.toml
2. Finalize CHANGELOG.md
3. Create release commit
4. Tag release: v[X].[Y].[Z]

Show me wave retrospective and release plan."
```

---

## Nested Claude Guides

### Vision Work
See [vision/CLAUDE.md](vision/CLAUDE.md) for:
- Strategic planning patterns
- Ecosystem vision work
- Long-term architecture
- Future wave planning

### Research Tasks
See [research/CLAUDE.md](research/CLAUDE.md) for:
- Research documentation patterns
- Technical investigation
- Integration research
- Proof-of-concept development

---

## Best Practices for Claude Development

### ✅ Do's

1. **Follow DDD → BDD → TDD** - Documentation first, always
2. **Work in small increments** - Test after each change
3. **Use wave context** - Understand current wave scope
4. **Emit telemetry** - Track operations for debugging
5. **Create checkpoints** - Daily session state snapshots
6. **Write comprehensive tests** - ≥85% coverage required
7. **Document decisions** - Why, not just what
8. **Request code review** - Before creating PR

### ❌ Don'ts

1. **Don't skip documentation** - Code without docs is incomplete
2. **Don't implement without tests** - TDD is required
3. **Don't break layers** - Respect architecture boundaries
4. **Don't ignore telemetry** - Past failures predict future issues
5. **Don't work across waves** - Stay focused on current wave
6. **Don't commit untested code** - All tests must pass
7. **Don't skip type hints** - mypy strict mode required
8. **Don't merge without PR** - Code review is mandatory

---

## Resources

### Project Documentation
- **Parent Guide:** [../CLAUDE.md](../CLAUDE.md) - Project-level Claude patterns
- **Developer Guide:** [AGENTS.md](AGENTS.md) - Generic developer guide
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution process
- **Pattern Library:** [../claude/](../claude/) - Claude pattern library

### Domain-Specific Guides
- **Vision:** [vision/CLAUDE.md](vision/CLAUDE.md) - Strategic planning
- **Research:** [research/CLAUDE.md](research/CLAUDE.md) - Research tasks
- **Tests:** [../tests/CLAUDE.md](../tests/CLAUDE.md) - Test generation
- **Docker:** [../docker/CLAUDE.md](../docker/CLAUDE.md) - Container development
- **Scripts:** [../scripts/CLAUDE.md](../scripts/CLAUDE.md) - Automation

### Wave Plans
- **Current Wave:** [../project-docs/WAVE_1X_PLAN.md](../project-docs/WAVE_1X_PLAN.md)
- **Roadmap:** [../ROADMAP.md](../ROADMAP.md)

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
