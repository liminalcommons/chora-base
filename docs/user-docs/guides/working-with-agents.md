# Working with AI Agents

**Audience**: Developers working with Claude Code, Cursor, or other AI coding assistants
**Related**: [SAP-009: Agent Awareness](../../skilled-awareness/agent-awareness/)

---

## Overview

Chora-base projects are optimized for AI agent collaboration through:
- **AGENTS.md** - Comprehensive agent context
- **SAPs** - Structured capability documentation
- **Clear conventions** - Predictable patterns
- **Executable documentation** - Step-by-step guides

---

## Quick Start

### 1. Share Context with Agent

**Essential files to share**:
```
AGENTS.md           # Project overview
CLAUDE.md           # Claude-specific guidance
README.md           # Getting started
docs/skilled-awareness/INDEX.md  # SAP catalog
```

**In Claude Code/Cursor**:
```
"Read AGENTS.md to understand this project"
```

### 2. Use SAPs for Guidance

```
"I need to add tests for the validation module.
Read SAP-004 (Testing Framework) for guidance."
```

### 3. Ask for Step-by-Step Plans

```
"Create a plan for implementing user authentication.
Include files to create, tests to write, and SAPs to reference."
```

---

## Best Practices

### 1. Provide Clear Context

**Bad**:
```
"Add a user model"
```

**Good**:
```
"Add a User model to src/myproject/models.py with fields:
- id (UUID)
- email (str, unique)
- created_at (datetime)

Include validation, database schema, and tests.
Follow patterns in SAP-004 (Testing Framework)."
```

### 2. Reference SAPs

```
"Implement email validation following SAP-004 testing patterns"
"Add CI/CD following SAP-005 workflow specifications"
"Create API endpoints using patterns from SAP-002"
```

### 3. Request Explanations

```
"Explain the testing strategy used in tests/test_validation.py"
"Why do we use pytest fixtures instead of setUp/tearDown?"
"What's the purpose of the ledger.md file in SAPs?"
```

### 4. Iterative Development

```
"Let's build the authentication system in 3 phases:
Phase 1: User model + database migrations
Phase 2: API endpoints (register, login, logout)
Phase 3: Tests + documentation

Start with Phase 1."
```

---

## Common Workflows

### Feature Development

```
1. "Create a plan for implementing [feature]"
2. Agent reads relevant SAPs and creates plan
3. "Proceed with Phase 1"
4. Agent implements, you review
5. "Add tests for what we just built"
6. "Update AGENTS.md to document this feature"
```

### Debugging

```
1. "Tests are failing in tests/test_api.py. Debug the issue."
2. Agent reads test file, identifies problem
3. "The issue is [explanation]. Here's the fix:"
4. Review and apply fix
```

### Refactoring

```
1. "The validation logic in api.py is complex. Refactor into smaller functions."
2. Agent proposes refactoring
3. "Show me the before and after"
4. "Apply the refactoring"
5. "Add tests to ensure behavior unchanged"
```

---

## Agent-Friendly Patterns

### Clear File Organization
```
src/myproject/
  models/          # Database models
  api/            # API endpoints
  services/       # Business logic
  utils/          # Utilities
tests/            # Mirror src/ structure
```

### Descriptive Names
```python
# Good
def validate_email_format(email: str) -> bool:
    """Validate email format using regex."""

# Avoids confusion
def check(data):  # What does this check?
```

### Type Hints
```python
# Agent can infer types and catch errors
def process_user(user: User) -> UserResponse:
    return UserResponse(id=user.id, name=user.name)
```

### Comprehensive Tests
```python
# Agent can understand expected behavior
def test_email_validation():
    """Test email validation logic."""
    assert validate_email("user@example.com") == True
    assert validate_email("invalid") == False
    assert validate_email("") == False
```

---

## Troubleshooting

### Agent Doesn't Follow Project Patterns

**Solution**: Be explicit about SAPs
```
"Add authentication following SAP-003 project bootstrap patterns.
Specifically, use the directory structure and naming conventions from that SAP."
```

### Agent Makes Incorrect Assumptions

**Solution**: Provide more context
```
"Before implementing, read:
1. AGENTS.md (project overview)
2. src/myproject/models.py (existing models)
3. SAP-004 (testing patterns)

Then create a plan."
```

### Agent Creates Low-Quality Tests

**Solution**: Reference quality standards
```
"Add tests following SAP-004 standards:
- 95%+ coverage
- Test edge cases and error paths
- Use pytest fixtures
- Include docstrings"
```

---

## Advanced Techniques

### Multi-File Context

```
"I'm refactoring the API layer. Read these files:
- src/myproject/api/routes.py
- src/myproject/api/schemas.py
- tests/test_api.py
- SAP-002 (chora-base patterns)

Propose improvements while maintaining backward compatibility."
```

### Pattern Extraction

```
"I've implemented email validation in 3 places.
Extract a reusable pattern and update all 3 locations."
```

### Documentation Generation

```
"Generate API documentation for all endpoints in src/myproject/api/
Format as Markdown with examples."
```

---

## Related Documentation

- [SAP-009: Agent Awareness](../../skilled-awareness/agent-awareness/)
- [AGENTS.md](../../../../AGENTS.md) - Project-specific agent context
- [CLAUDE.md](../../../../CLAUDE.md) - Claude-specific guidance

---

**Last Updated**: 2025-10-29
