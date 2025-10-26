# Framework Templates for Claude

**Purpose:** Reusable request templates that maximize Claude's effectiveness for common development tasks.

**Problem Solved:** Inconsistent requests, missing requirements, poor first-pass success, repeated iterations.

---

## Overview

**Structured requests yield better results.** These templates provide:

- **Consistent quality** - Proven patterns for common tasks
- **Faster results** - Reduce iterations by being comprehensive upfront
- **Better outcomes** - Higher first-pass success rate
- **Time savings** - Don't reinvent request structure each time

**Without templates:** Ad-hoc requests, missing details, multiple iterations
**With templates:** Comprehensive specs, clear expectations, efficient execution

---

## Template Index

| Template | Use When | Estimated Time | First-Pass Success |
|----------|----------|----------------|-------------------|
| [Feature Implementation](#feature-implementation-template) | Building new capability | 2-4 hours | 75-85% |
| [Debugging](#debugging-template) | Investigating errors | 30-60 min | 80-90% |
| [Refactoring](#refactoring-template) | Improving existing code | 1-3 hours | 70-80% |
| [Code Review](#code-review-template) | Reviewing pull requests | 20-40 min | 85-95% |
| [Test Generation](#test-generation-template) | Adding test coverage | 30-90 min | 80-90% |
| [Documentation](#documentation-template) | Writing/updating docs | 30-60 min | 75-85% |

---

## Feature Implementation Template

**When:** Building new functionality from scratch
**Goal:** Complete, production-ready feature in one session

### Template

```markdown
# Feature: [Feature Name]

## Overview
**What:** [1-2 sentence description]
**Why:** [Business justification / problem being solved]
**Success criteria:** [Specific, measurable outcomes]

## Design Reference
**Documentation:** [path to DDD design doc if available]
**Architecture:** [relevant section of AGENTS.md or design]
**Related features:** [similar existing features to reference]

## Implementation Requirements

### 1. Core Functionality
**Specification:**
- Input: [type, format, constraints, example]
- Output: [type, format, example]
- Behavior: [detailed description of what it should do]

**Example usage:**
```python
# Example of how feature should be used
result = my_feature(input_data)
assert result == expected_output
```

### 2. Error Handling
**Required error scenarios:**
- Invalid input: [expected behavior]
- Missing dependencies: [expected behavior]
- Network failures: [expected behavior, if applicable]
- Edge cases: [list specific edge cases]

**Error response format:**
```python
# Example error response
{
    "error": "error_code",
    "message": "Human-readable message",
    "details": {...}
}
```

### 3. Testing Requirements
**Coverage target:** 85%+
**Test categories:**
- ✅ Happy path test (core functionality)
- ✅ Edge cases (minimum 3)
- ✅ Error conditions (all error scenarios above)
- ✅ Boundary value tests
- ✅ Integration test (if interacts with other components)

**Test framework:** pytest
**Fixtures:** [list any needed fixtures or mocks]

### 4. Documentation
**Required:**
- Docstring with examples for main function/class
- Inline comments for complex logic
- README update (if user-facing feature)
- API documentation (if adds endpoint)

### 5. Code Style & Patterns
**Follow patterns in:** [path to similar existing code]
**Specific requirements:**
- Type hints: Required for all functions
- Error handling style: [project convention]
- Naming convention: [snake_case, camelCase, etc.]
- Imports: [organization pattern]

**Style reference:**
```python
# Example of project code style
def example_function(param: str) -> dict[str, Any]:
    """Example showing project patterns.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When param is invalid
    """
    # Implementation following project style
```

## Constraints
- Python version: [e.g., 3.11+]
- Dependencies: [only use these libraries]
- Performance: [any performance requirements]
- Security: [any security considerations]
- Backward compatibility: [maintain compatibility with...]

## Integration Points
**Interfaces with:**
- [Component 1]: [how they interact]
- [Component 2]: [how they interact]

**Database changes:** [if any schema changes needed]
**Configuration:** [any new config variables]

## Acceptance Criteria
- [ ] Core functionality implemented and working
- [ ] All error scenarios handled
- [ ] Tests passing (coverage ≥85%)
- [ ] Documentation complete
- [ ] Code follows project patterns
- [ ] No breaking changes (or documented if necessary)
- [ ] Linter passing (ruff check)
- [ ] Type checker passing (mypy)

## Workflow Integration
**This feature follows:**
1. DDD: Design documented in [path]
2. BDD: Acceptance tests written first
3. TDD: Unit tests drive implementation

**See:** dev-docs/workflows/ for complete workflow

---

Claude, please implement this feature following the DDD→BDD→TDD workflow:
1. Review the design (if provided)
2. Generate acceptance tests first (BDD)
3. Implement core functionality to pass tests (TDD)
4. Add comprehensive error handling
5. Complete documentation
6. Verify all acceptance criteria met

Generate as artifact for easy copying to files.
```

**Estimated time:** 2-4 hours for medium feature
**First-pass success:** 75-85% with complete specification

---

## Debugging Template

**When:** Investigating errors or unexpected behavior
**Goal:** Identify root cause and implement fix

### Template

```markdown
# Debug Request: [Error/Issue Description]

## Error Context

### Error Message
```
[Full error traceback or message]
```

### Reproduction Steps
1. [Step 1 to reproduce]
2. [Step 2 to reproduce]
3. [Error occurs at this point]

**Reproducibility:** Always | Sometimes (X% of time) | Rare

### Environment
- **OS:** [Operating System]
- **Python version:** [3.11.x]
- **Dependencies:** [relevant package versions]
- **Configuration:** [relevant settings]

## Code Context

### Relevant Code
```python
# File: path/to/file.py
# Lines XX-YY (where error occurs)
[Paste code section with error]
```

### Recent Changes
```bash
# Recent commits that might be related
$(git log --oneline -5 path/to/file.py)
```

### Related Files
- [File 1]: [why relevant]
- [File 2]: [why relevant]

## Expected vs Actual Behavior

**Expected:**
[What should happen]

**Actual:**
[What actually happens]

**Difference:**
[Specific discrepancy]

## Investigation So Far

### What I've Tried
1. **Attempt 1:** [What was tried]
   - **Result:** [What happened]
   - **Conclusion:** [Why it didn't work]

2. **Attempt 2:** [What was tried]
   - **Result:** [What happened]
   - **Conclusion:** [Why it didn't work]

### Hypotheses
- **Hypothesis 1:** [Possible cause]
  - **Evidence:** [Why you think this]
- **Hypothesis 2:** [Possible cause]
  - **Evidence:** [Why you think this]

## Debugging Request

Claude, please:
1. **Analyze the error** - Identify root cause
2. **Explain why it occurs** - Help me understand the issue
3. **Provide corrected code** - Fix with explanation
4. **Suggest preventive measures** - How to avoid in future
5. **Add regression test** - Prevent this bug from returning

If you need more context, please ask specific questions.
```

**Estimated time:** 30-60 minutes
**First-pass success:** 80-90% with complete error context

---

## Refactoring Template

**When:** Improving code structure, performance, or maintainability
**Goal:** Better code without changing behavior

### Template

```markdown
# Refactoring Request: [Code Section]

## Refactoring Goal

**Primary objective:** [Improve readability | Performance | Maintainability | etc.]
**Specific improvements:**
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

## Current Code

### Code to Refactor
```python
# File: path/to/file.py
# Lines XX-YY
[Paste code to refactor]
```

### Context
**What this code does:** [Explanation]
**Why it needs refactoring:** [Specific problems]
**Constraints:** [What must stay the same]

## Current Behavior (Must Preserve)

### Test Coverage
```python
# Existing tests that must continue passing
[Paste relevant tests]
```

**Coverage:** [X%]

### Expected Behavior
**Inputs:** [Examples]
**Outputs:** [Expected results]
**Edge cases:** [Scenarios that must work]

## Refactoring Approach

**Preferred patterns:** [Project patterns to follow]
**Reference code:** [Path to similar well-written code]

**Code style example:**
```python
# Example of desired style/pattern
[Example from project]
```

## Requirements

### Must Have
- [ ] Preserve all existing behavior
- [ ] All existing tests pass
- [ ] Code coverage maintained or improved
- [ ] Type hints added/improved
- [ ] Documentation updated

### Should Have
- [ ] Improved readability
- [ ] Reduced complexity (cyclomatic, cognitive)
- [ ] Better error messages
- [ ] More consistent with project patterns

### Nice to Have
- [ ] Performance improvement (if measurable)
- [ ] Reduced code duplication
- [ ] Better separation of concerns

## Metrics

**Current:**
- Lines of code: [X]
- Cyclomatic complexity: [Y]
- Test coverage: [Z%]

**Target:**
- Lines of code: [Target or "reduce by N%"]
- Cyclomatic complexity: [Target]
- Test coverage: [≥ current]

## Safety Checks

**Before refactoring:**
```bash
# Run tests to establish baseline
pytest path/to/tests.py -v
```

**After refactoring:**
```bash
# Must pass
pytest path/to/tests.py -v
ruff check path/to/file.py
mypy path/to/file.py
```

---

Claude, please refactor this code:
1. Analyze current structure
2. Identify specific improvements
3. Apply refactoring in stages (easier to review)
4. Ensure all tests still pass
5. Document significant changes

Show before/after comparison for each stage.
```

**Estimated time:** 1-3 hours
**First-pass success:** 70-80%

---

## Code Review Template

**When:** Reviewing code before merge
**Goal:** Thorough review covering functionality, quality, security

### Template

```markdown
# Code Review Request

## Change Overview
**PR/Branch:** [name]
**Author:** [name]
**Description:** [what changed and why]

## Files Changed
```bash
$(git diff --name-only main...branch)
```

## Code to Review
```python
[Paste changed code or use git diff output]
```

## Review Checklist

### Functionality
- [ ] Correct implementation of requirements
- [ ] Edge case handling comprehensive
- [ ] Error handling complete
- [ ] Behavior matches specification
- [ ] No unintended side effects

### Performance
- [ ] Time complexity acceptable
  - **Current:** [O(n), O(n^2), etc.]
  - **Acceptable:** [threshold]
- [ ] Space complexity acceptable
- [ ] Database queries optimized (if applicable)
- [ ] No obvious performance issues

### Security
- [ ] Input validation present
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS protection (if web-facing)
- [ ] Authentication/authorization checks
- [ ] Sensitive data handling appropriate
- [ ] No hardcoded secrets/credentials

### Maintainability
- [ ] Code is readable and clear
- [ ] Naming is descriptive
- [ ] Comments explain "why" not "what"
- [ ] Documentation complete (docstrings)
- [ ] Complexity reasonable (not over-engineered)
- [ ] Follows SOLID principles

### Testing
- [ ] Test coverage ≥ [threshold, e.g., 85%]
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Integration tests (if needed)

### Code Style
- [ ] Follows project conventions
- [ ] Type hints present
- [ ] Linter passing (ruff check)
- [ ] Type checker passing (mypy)
- [ ] Consistent with existing code

### Project Integration
- [ ] Integrates cleanly with existing code
- [ ] No breaking changes (or documented/versioned)
- [ ] Dependencies appropriate
- [ ] Configuration changes documented
- [ ] Migration path clear (if needed)

## Specific Review Focus
[Any particular areas the author wants reviewed carefully]

---

Claude, please review this code covering all checklist items:
1. Provide overall assessment (approve/request changes/needs work)
2. List specific issues found (with line numbers)
3. Suggest improvements (with code examples)
4. Identify security concerns (if any)
5. Rate code quality (1-10) with justification

Be thorough but constructive.
```

**Estimated time:** 20-40 minutes
**First-pass success:** 85-95%

---

## Test Generation Template

**When:** Adding tests to existing code or improving coverage
**Goal:** Comprehensive test suite with high coverage

### Template

```markdown
# Test Generation Request

## Code to Test
```python
# File: path/to/module.py
[Paste code that needs tests]
```

**Current coverage:** [X%]
**Target coverage:** [Y%, typically 85%+]

## Testing Requirements

### Test Framework
- **Framework:** pytest
- **Fixtures location:** tests/conftest.py
- **Naming pattern:** test_[function]_[scenario]_[expected]

### Test Categories Needed

#### 1. Happy Path Tests
- [ ] Basic functionality with valid inputs
- [ ] Typical use cases
- [ ] Expected workflow

#### 2. Edge Cases (minimum 3)
- [ ] Empty inputs
- [ ] Boundary values (min, max)
- [ ] Large datasets
- [ ] [Domain-specific edge case]

#### 3. Error Conditions
- [ ] Invalid input types
- [ ] Missing required parameters
- [ ] Out-of-range values
- [ ] Resource unavailable (if applicable)
- [ ] All raised exceptions

#### 4. Integration Tests (if applicable)
- [ ] Interaction with [Component A]
- [ ] Interaction with [Component B]
- [ ] End-to-end workflow

### Mocking Strategy
**External dependencies to mock:**
- [Dependency 1]: [Why and how to mock]
- [Dependency 2]: [Why and how to mock]

**Example mock:**
```python
@pytest.fixture
def mock_dependency():
    return Mock(spec=Dependency)
```

## Example Test Pattern
```python
# Example following project style
def test_function_scenario_expected(fixture1, fixture2):
    """Test that function does X when Y.

    This test verifies [specific behavior].
    """
    # Arrange
    input_data = {...}
    expected = {...}

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected
```

## Coverage Analysis

**Uncovered lines (run pytest --cov):**
```
[Paste coverage report showing uncovered lines]
```

**Priority coverage:**
1. Critical paths (error handling, core logic)
2. Edge cases
3. Error conditions

---

Claude, please generate comprehensive tests:
1. Cover all test categories above
2. Use pytest fixtures for common setup
3. Include descriptive docstrings
4. Add @pytest.mark.parametrize for multiple scenarios
5. Organize with clear arrange-act-assert structure
6. Target ≥85% coverage

Generate as artifact for easy copying.
```

**Estimated time:** 30-90 minutes
**First-pass success:** 80-90%

---

## Documentation Template

**When:** Writing or updating documentation
**Goal:** Clear, comprehensive, helpful documentation

### Template

```markdown
# Documentation Request: [Module/Feature]

## Documentation Type
- [ ] README section
- [ ] API documentation
- [ ] How-to guide
- [ ] Architecture documentation
- [ ] User guide

## Content to Document

### Code/Feature
```python
[Paste code that needs documentation]
```

### Current Documentation
```markdown
[Paste existing documentation if updating]
```

## Documentation Requirements

### Audience
**Primary:** [Developers | Users | Both]
**Assumed knowledge:** [What readers already know]
**Learning goal:** [What they should understand after reading]

### Required Sections

#### Overview
- [ ] Purpose (what this does)
- [ ] When to use it
- [ ] Quick example

#### Usage
- [ ] Installation/setup (if applicable)
- [ ] Basic usage example
- [ ] Common patterns
- [ ] Best practices

#### API Reference (if applicable)
- [ ] All public functions/classes
- [ ] Parameters with types
- [ ] Return values
- [ ] Exceptions raised
- [ ] Code examples

#### Examples
- [ ] Simple example (hello world)
- [ ] Real-world example
- [ ] Edge cases handling
- [ ] Error handling

#### Additional
- [ ] Configuration options
- [ ] Troubleshooting common issues
- [ ] Related documentation
- [ ] Changelog/migration notes

### Documentation Style

**Format:** Markdown
**Code examples:** Include type hints
**Tone:** [Professional | Friendly | Technical | etc.]

**Example format:**
```markdown
## Function Name

Brief description of what it does.

### Parameters
- `param1` (type): Description
- `param2` (type, optional): Description. Defaults to X.

### Returns
- `return_type`: Description of return value

### Raises
- `ExceptionType`: When this exception occurs

### Example
```python
# Example usage
result = function_name(param1="value")
```

### Notes
- Important detail 1
- Important detail 2
```

---

Claude, please generate documentation:
1. Follow project documentation style
2. Include practical examples
3. Explain "why" not just "what"
4. Add troubleshooting for common issues
5. Link to related documentation

Make it clear, concise, and helpful.
```

**Estimated time:** 30-60 minutes
**First-pass success:** 75-85%

---

## Multi-Phase Development Pattern

**When:** Large feature spanning multiple sessions
**Goal:** Structured approach to complex development

### Pattern

```markdown
Phase 1: Analysis & Design (30-60 min)
↓
Phase 2: Core Implementation (2-4 hours)
↓
Phase 3: Error Handling & Edge Cases (1-2 hours)
↓
Phase 4: Testing (1-2 hours)
↓
Phase 5: Documentation & Polish (30-60 min)
↓
Phase 6: Review & Refinement (30-60 min)
```

**Use when:**
- Feature estimated >4 hours
- Complex with many edge cases
- Requires careful design

**Pattern request:**
```markdown
"Let's implement [feature] in phases:

Phase 1: Design & Planning
- Review requirements
- Design API interface
- Identify integration points
- Plan error handling strategy

[Create checkpoint after Phase 1]

Phase 2: Core Implementation
- Implement happy path
- Basic functionality working
- No error handling yet

[Create checkpoint after Phase 2]

Phase 3: Robustness
- Add error handling
- Handle edge cases
- Validate inputs

[Continue through phases...]

Use checkpoint pattern to preserve state between phases."
```

---

## Socratic Development Pattern

**When:** Unclear requirements or complex architectural decisions
**Goal:** Explore solution space before coding

### Pattern

```markdown
# Socratic Exploration: [Problem]

Instead of immediate implementation, let's explore:

## Questions to Consider

1. **Requirements Clarity**
   - What are we really trying to achieve?
   - What are the must-haves vs nice-to-haves?
   - What are the success criteria?

2. **Architectural Decisions**
   - What are the key architectural choices?
   - What trade-offs exist?
   - What are the alternatives?

3. **Edge Cases**
   - What could go wrong?
   - What edge cases might we overlook?
   - What failure modes exist?

4. **Existing Patterns**
   - How is this done elsewhere in the codebase?
   - Are there similar features to reference?
   - What lessons can we learn from them?

5. **Future Considerations**
   - How might requirements change?
   - What extension points do we need?
   - How do we avoid painting ourselves into a corner?

---

Claude, before we code, help me think through these questions.
Provide analysis and recommendations, then we'll design the implementation.
```

**Use for:** Complex features, unclear requirements, architectural decisions

---

## Best Practices

### ✅ Template Usage Do's

1. **Customize templates** - Adapt to your specific needs
2. **Be complete** - Fill in all sections thoroughly
3. **Provide examples** - Concrete examples improve results
4. **Reference existing code** - Point to similar implementations
5. **State constraints** - Be explicit about limitations
6. **Include context** - Workflow, patterns, conventions

### ❌ Template Usage Don'ts

1. **Don't skip sections** - Each section serves a purpose
2. **Don't be vague** - "Make it work" vs specific requirements
3. **Don't omit examples** - Examples clarify expectations
4. **Don't ignore style** - Consistent style improves quality
5. **Don't forget tests** - Always include testing requirements

---

## Metrics

**Track template effectiveness:**

| Metric | Definition | Target |
|--------|------------|--------|
| **First-pass success** | % tasks completed without iteration | >75% |
| **Time to completion** | Actual vs estimated time | <estimate |
| **Quality score** | Code quality rating (1-10) | >7 |
| **Rework rate** | % needing significant changes | <20% |

---

**See Also:**
- [METRICS_TRACKING.md](METRICS_TRACKING.md) - Track template effectiveness
- [CHECKPOINT_PATTERNS.md](CHECKPOINT_PATTERNS.md) - Use with multi-phase pattern

---

**Version:** 3.3.0
**Pattern Maturity:** ⭐⭐⭐ Production-ready
**Last Updated:** 2025-10-26
