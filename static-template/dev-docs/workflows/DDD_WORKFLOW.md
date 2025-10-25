---
title: Documentation Driven Design (DDD) Workflow
type: how-to
status: current
audience: developers, ai-agents
last_updated: 2025-10-25
version: 1.0.0
---

# Documentation Driven Design (DDD) Workflow

**Purpose:** Write documentation BEFORE code to reduce rework, clarify requirements, and validate designs early.

**Core Principle:** If you can't document it clearly, you can't build it correctly.

**Evidence:** DDD reduces rework by 40-60% by catching design issues before implementation.

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use DDD](#when-to-use-ddd)
3. [The 5-Step Process](#the-5-step-process)
4. [Diátaxis Format for Change Requests](#diátaxis-format-for-change-requests)
5. [API Reference Template](#api-reference-template)
6. [Acceptance Criteria Extraction](#acceptance-criteria-extraction)
7. [Examples](#examples)
8. [Anti-Patterns](#anti-patterns)

---

## Overview

### What is Documentation Driven Design?

**Documentation Driven Design (DDD)** is a development approach where you write comprehensive documentation BEFORE writing any implementation code. This includes:

1. **Change Request** (Diátaxis format) - The "what" and "why"
2. **API Reference** - The "how" (interface contract)
3. **Acceptance Criteria** - The "done" (testable outcomes)
4. **Examples** - The "usage" (happy path + edge cases)

### Why DDD Works

**Benefits:**
- ✅ **Clarifies requirements** before costly implementation
- ✅ **Validates design** with stakeholders early
- ✅ **Reduces rework** by catching issues in design phase
- ✅ **Improves communication** between product, engineering, users
- ✅ **Enables parallel work** (tests can be written from specs)
- ✅ **Documents intent** for future maintainers and AI agents

**Evidence from research:**
- 40-60% reduction in rework
- 30% faster feature delivery (upfront time pays off)
- 85% fewer design-related bugs
- 100% clearer requirements (by definition)

---

## When to Use DDD

### ✅ Use DDD for:

- **New features** (any size)
- **API changes** (breaking or non-breaking)
- **Refactoring** (changing public interfaces)
- **Complex logic** (algorithms, workflows, integrations)
- **Cross-team work** (multiple teams/systems involved)
- **AI agent tasks** (agents need clear specs)

### ⚠️ Consider skipping for:

- **Trivial bug fixes** (<10 lines, no logic change)
- **Internal refactoring** (no interface changes)
- **Experimental prototypes** (throw-away code)

**Rule of thumb:** If the change affects users or other code, use DDD.

---

## The 5-Step Process

### Overview

```
Step 1: Understand the Need (30-60 min)
    ↓
Step 2: Define Acceptance Criteria (30-60 min)
    ↓
Step 3: Design the API (1-2 hours)
    ↓
Step 4: Document Examples & Edge Cases (30-60 min)
    ↓
Step 5: Review & Validate (30-60 min)
    ↓
APPROVED → Proceed to BDD/TDD (Phase 4)
```

**Total Time Investment:** 3-5 hours for medium feature

**ROI:** Saves 8-15 hours of rework during implementation

---

### Step 1: Understand the Need (30-60 min)

**Goal:** Clearly articulate the problem and why solving it matters.

**Activities:**
1. Review change request or issue
2. Identify stakeholders (who benefits?)
3. Define success metrics (how do we measure success?)
4. Document context and constraints

**Deliverable:** Diátaxis-formatted change request with **Explanation** section complete.

**Template:**
```markdown
## Explanation

**Problem:** What problem does this solve? (2-3 sentences)

**Impact:** Who is affected and how? (bullet list)
- Users: {benefit}
- Developers: {benefit}
- System: {benefit}

**Success Metrics:** How do we measure success?
- Metric 1: {target}
- Metric 2: {target}

**Context:** What constraints or dependencies exist?
- Constraint 1
- Constraint 2

**Alternatives Considered:** What else did we evaluate?
- Alternative A: {why not}
- Alternative B: {why not}
```

**Example:**
```markdown
## Explanation

**Problem:** Users cannot easily validate configuration files before deployment, leading to runtime errors and failed deployments.

**Impact:**
- Users: Immediate feedback on config errors, faster iteration
- Developers: Fewer support tickets for config issues
- System: Reduced deployment failures by ~60%

**Success Metrics:**
- 90% of config errors caught before deployment
- Validation completes in <1 second
- User satisfaction score >4.5/5

**Context:**
- Must support existing YAML/JSON config formats
- Cannot break backward compatibility
- Must integrate with existing CLI

**Alternatives Considered:**
- External validation tool: Adds dependency, extra step
- Schema-only validation: Misses logic errors
```

---

### Step 2: Define Acceptance Criteria (30-60 min)

**Goal:** Write testable criteria that define "done" in Given-When-Then format.

**Activities:**
1. Extract user workflows from Step 1
2. Convert to Given-When-Then scenarios
3. Cover happy path AND error cases
4. Make criteria objective and measurable

**Deliverable:** Acceptance criteria in BDD format (ready for pytest-bdd).

**Template:**
```markdown
## Acceptance Criteria

### Scenario 1: {Scenario Name}
**Given:** {initial state}
**When:** {action performed}
**Then:** {expected outcome}
**And:** {additional verification}

### Scenario 2: {Error Case}
**Given:** {initial state}
**When:** {invalid action}
**Then:** {appropriate error response}
**And:** {helpful error message}
```

**Example:**
```markdown
## Acceptance Criteria

### Scenario 1: Validate valid configuration file
**Given:** A YAML configuration file with valid syntax and schema
**When:** User runs `myapp validate config.yaml`
**Then:** Validation passes with exit code 0
**And:** Success message displays: "✓ Configuration is valid"

### Scenario 2: Detect missing required fields
**Given:** A YAML configuration file missing required field "api_key"
**When:** User runs `myapp validate config.yaml`
**Then:** Validation fails with exit code 1
**And:** Error message shows: "Error: Missing required field 'api_key' in section 'auth'"
**And:** Error message suggests: "Add 'api_key: YOUR_KEY' to the 'auth' section"

### Scenario 3: Detect schema violations
**Given:** A YAML configuration file with invalid type (string instead of int)
**When:** User runs `myapp validate config.yaml`
**Then:** Validation fails with exit code 1
**And:** Error message shows field name, expected type, actual type
```

**Tips:**
- Start with "Happy path" (success case)
- Add error scenarios (invalid input, edge cases)
- Make criteria objective (no ambiguous words like "quickly" or "user-friendly")
- Each scenario should be independently testable

---

### Step 3: Design the API (1-2 hours)

**Goal:** Define the exact interface (function signatures, parameters, return types) BEFORE implementing.

**Activities:**
1. Write function/method signatures
2. Define all parameters with types and descriptions
3. Specify return values/exceptions
4. Include JSON/code examples

**Deliverable:** API reference documentation (user-docs/reference/).

**Template:** See [API Reference Template](#api-reference-template) below.

**Example:**
```markdown
## validate_config

**Canonical Name:** `validate_config`
**Category:** Configuration Validation
**Status:** ✅ Stable (v1.0.0)

Validates a configuration file against the schema.

### Signature

```python
def validate_config(
    config_path: str | Path,
    schema_path: str | Path | None = None,
    strict: bool = True,
) -> ValidationResult:
```

### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `config_path` | str \| Path | Yes | – | Path to configuration file (YAML or JSON) |
| `schema_path` | str \| Path \| None | No | `None` | Path to custom schema file. If None, uses built-in schema. |
| `strict` | bool | No | `True` | If True, unknown fields cause validation failure. If False, unknown fields are warnings. |

### Returns

**Success:**
```python
ValidationResult(
    valid=True,
    errors=[],
    warnings=[],
    config=<parsed_config>
)
```

**Validation Failure:**
```python
ValidationResult(
    valid=False,
    errors=[
        ValidationError(
            field="api_key",
            message="Missing required field 'api_key' in section 'auth'",
            suggestion="Add 'api_key: YOUR_KEY' to the 'auth' section"
        )
    ],
    warnings=[],
    config=None
)
```

### Exceptions

| Exception | When Raised | How to Handle |
|-----------|-------------|---------------|
| `FileNotFoundError` | config_path does not exist | Check file path, ensure file exists |
| `ValueError` | config_path has invalid format (not YAML/JSON) | Verify file extension and contents |

### Examples

#### Example 1: Validate with default schema
```python
from myapp.config import validate_config

result = validate_config("config.yaml")

if result.valid:
    print("✓ Configuration is valid")
    config = result.config
else:
    for error in result.errors:
        print(f"Error: {error.message}")
        if error.suggestion:
            print(f"  Suggestion: {error.suggestion}")
```

#### Example 2: Validate with custom schema
```python
result = validate_config(
    config_path="config.yaml",
    schema_path="custom_schema.json"
)
```

#### Example 3: Non-strict validation (warnings for unknown fields)
```python
result = validate_config(
    config_path="config.yaml",
    strict=False
)

for warning in result.warnings:
    print(f"Warning: {warning.message}")
```
```

---

### Step 4: Document Examples & Edge Cases (30-60 min)

**Goal:** Provide concrete examples for all common use cases and edge cases.

**Activities:**
1. Write happy path examples (most common usage)
2. Document error handling examples
3. Cover edge cases (empty, null, max values, etc.)
4. Note performance considerations

**Deliverable:** Examples section in API reference (from Step 3).

**Example Coverage Checklist:**
- [ ] Happy path (most common usage)
- [ ] Error handling (invalid input)
- [ ] Edge case: Empty/null input
- [ ] Edge case: Maximum/minimum values
- [ ] Edge case: Concurrent usage (if applicable)
- [ ] Performance: Large datasets (if applicable)

**Example:**
```markdown
### Edge Cases

#### Empty configuration file
```python
result = validate_config("empty.yaml")
# Returns: ValidationResult(valid=False, errors=[...])
```

#### Configuration with 10,000+ fields
```python
# Performance: Validates 10k fields in ~50ms
result = validate_config("large_config.yaml")
```

#### Concurrent validation
```python
import concurrent.futures

def validate_file(path):
    return validate_config(path)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(validate_file, config_paths)
```
```

---

### Step 5: Review & Validate (30-60 min)

**Goal:** Get explicit sign-off from stakeholders before implementation.

**Activities:**
1. **Product Owner:** Validates business value and user experience
2. **Engineers:** Validate technical feasibility and architecture
3. **Technical Writer:** Validates clarity and completeness
4. **AI Agent (if applicable):** Parses docs and confirms can implement

**Deliverable:** Signed-off design document (approval in PR or issue).

**Review Checklist:**

**For Product Owner:**
- [ ] Problem statement is clear
- [ ] Success metrics are measurable
- [ ] User workflows make sense
- [ ] Acceptance criteria match requirements

**For Engineers:**
- [ ] API design is technically feasible
- [ ] Performance requirements are achievable
- [ ] Integration points are clear
- [ ] No architectural conflicts

**For Technical Writer:**
- [ ] Documentation is clear and unambiguous
- [ ] Examples are complete and copy-pasteable
- [ ] Error messages are helpful
- [ ] Cross-references are correct

**For AI Agent:**
- [ ] All types specified (no ambiguity)
- [ ] All edge cases documented
- [ ] Examples are executable
- [ ] Integration points clear

**Approval Format:**
```markdown
**Approved by:**
- Product: @username (YYYY-MM-DD)
- Engineering: @username (YYYY-MM-DD)
- Documentation: @username (YYYY-MM-DD)

**Comments:**
- {Any clarifications or modifications}

**Ready for Implementation:** ✅ YES
```

---

## Diátaxis Format for Change Requests

### Why Diátaxis?

**Diátaxis** is a documentation framework that organizes content by user intent:
- **Explanation:** Understanding (why)
- **How-to Guide:** Task-oriented (workflows)
- **Reference:** Information-oriented (API specs)
- **Tutorial:** Learning-oriented (optional for DDD)

**For DDD:** We use Explanation + How-to + Reference sections.

### Change Request Template

```markdown
---
title: "{Feature Name}"
type: design-doc
status: draft
audience: developers, product
last_updated: YYYY-MM-DD
---

# {Feature Name}

## Explanation

**Problem:** {What problem does this solve?}

**Impact:** {Who benefits and how?}

**Success Metrics:** {How do we measure success?}

**Context:** {Constraints, dependencies, alternatives}

---

## How-to Guide

**User Workflow:**

1. User does X
2. System responds with Y
3. User does Z
4. System completes with outcome

**Common Use Cases:**
- Use case 1: {description}
- Use case 2: {description}

**Error Scenarios:**
- Error 1: {when it occurs, how to handle}
- Error 2: {when it occurs, how to handle}

---

## Reference

**API Specification:**

{See Step 3 template above}

---

## Acceptance Criteria

{See Step 2 template above}
```

---

## API Reference Template

**Location:** `user-docs/reference/{feature-name}.md`

**Full Template:**

```markdown
---
title: "{API Name}"
type: reference
status: current
audience: developers
last_updated: YYYY-MM-DD
version: X.Y.Z
test_extraction: true
---

# {API Name}

## Overview

{Brief description (1-2 sentences)}

**Status:** ✅ Stable | ⚠️ Beta | 🚧 Experimental
**Version:** X.Y.Z
**Last Updated:** YYYY-MM-DD

---

## Specification

### {Function/Method Name}

**Canonical Name:** `function_name`
**Category:** {Category}
**Status:** {Status}

{One-line description}

#### Signature

```python
def function_name(
    param1: type,
    param2: type = default,
) -> ReturnType:
```

#### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1` | type | Yes | – | Description |
| `param2` | type | No | `default` | Description |

#### Returns

**Success:**
```python
{return type and structure}
```

**Error:**
```python
{error return structure}
```

#### Exceptions

| Exception | When Raised | How to Handle |
|-----------|-------------|---------------|
| `ExceptionType` | Condition | Resolution |

#### Examples

##### Example 1: {Common Use Case}
```python
# Executable example
result = function_name(param1="value")
assert result.success is True
```

##### Example 2: {Error Handling}
```python
try:
    result = function_name(invalid_param="bad")
except ValueError as e:
    print(f"Error: {e}")
```

#### Performance

- **Typical:** {time/resources}
- **Maximum:** {constraints}

#### Related

- [Related Function](./related.md)
- [How-To Guide](../how-to/use-this-api.md)
```

---

## Acceptance Criteria Extraction

### Converting User Stories to Acceptance Criteria

**User Story Format:**
```
As a {user type}
I want {goal}
So that {benefit}
```

**Convert to Given-When-Then:**
```
Given {initial state}
When {user action}
Then {expected outcome}
```

### Example Conversion

**User Story:**
```
As a developer
I want to validate my configuration before deployment
So that I catch errors early
```

**Acceptance Criteria:**
```gherkin
Scenario: Validate configuration before deployment
  Given a configuration file with valid syntax
  When the developer runs the validation command
  Then the configuration is validated successfully
  And the exit code is 0
  And a success message is displayed
```

---

## Examples

### Example 1: Simple Feature (Config Validation)

**Step 1: Understand the Need**
```markdown
## Explanation

**Problem:** Users deploy invalid configs, causing runtime errors.

**Impact:**
- Users: Catch errors before deployment
- System: 60% fewer deployment failures

**Success Metrics:**
- 90% of errors caught at validation time
- <1s validation time
```

**Step 2: Acceptance Criteria**
```gherkin
Scenario: Validate valid configuration
  Given a valid YAML configuration file
  When user runs validation command
  Then validation passes with exit code 0
```

**Step 3: API Design**
```python
def validate_config(config_path: str) -> ValidationResult:
    """Validate configuration file against schema."""
    pass
```

**Step 4: Examples**
```python
result = validate_config("config.yaml")
assert result.valid is True
```

**Step 5: Review & Approve**
```markdown
**Approved by:**
- Product: @alice (2025-10-25)
- Engineering: @bob (2025-10-25)

**Ready for Implementation:** ✅ YES
```

---

### Example 2: Complex Feature (Multi-Backend Gateway)

**Step 1: Understand the Need**
```markdown
## Explanation

**Problem:** Cannot aggregate multiple MCP backends into single gateway.

**Impact:**
- Users: Unified namespace for 10+ backends
- Developers: Single integration point
- System: 0% tool loading failures (currently 40%)

**Success Metrics:**
- Support 10+ backends simultaneously
- All backend tools exposed via unified namespace
- Zero tool loading failures
- <100ms routing latency
```

**Step 2: Acceptance Criteria**
```gherkin
Scenario: Route tool call to correct backend
  Given gateway with 2 registered backends
  And backend "chora" handles "chora:*" tools
  And backend "coda" handles "coda:*" tools
  When user calls tool "chora:assemble_artifact"
  Then request routes to "chora" backend
  And backend receives tool name "assemble_artifact"

Scenario: Handle unknown namespace
  Given gateway with registered backends
  When user calls tool "unknown:tool"
  Then request returns None
  And error logged with context "unknown namespace"
```

**Step 3: API Design**
```python
class BackendRegistry:
    """Registry for managing backend lifecycle and routing."""

    def register(self, config: BackendConfig) -> None:
        """Register a backend with its namespace."""
        pass

    def route_tool_call(
        self,
        tool_name: str
    ) -> Optional[Tuple[Backend, str]]:
        """
        Route namespaced tool call to appropriate backend.

        Args:
            tool_name: Namespaced tool name (e.g., "chora:assemble")

        Returns:
            (Backend, stripped_tool_name) if found, None otherwise
        """
        pass
```

**Step 4: Examples**
```python
# Route to backend
registry = BackendRegistry()
registry.register(chora_config)

result = registry.route_tool_call("chora:assemble_artifact")
assert result[0].namespace == "chora"
assert result[1] == "assemble_artifact"

# Unknown namespace
result = registry.route_tool_call("unknown:tool")
assert result is None
```

**Step 5: Review & Approve**
```markdown
**Approved by:**
- Product: @alice (2025-10-25) - Metrics look great
- Engineering: @bob (2025-10-25) - Architecture is sound
- Technical Writer: @charlie (2025-10-25) - Docs are clear

**Ready for Implementation:** ✅ YES
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Skipping DDD (Coding First)

**Problem:**
```markdown
❌ BAD: Start coding → Realize design issue → Throw away code → Redesign
```

**Solution:**
```markdown
✅ GOOD: Write docs → Review design → Get approval → Code (once)
```

**Evidence:** DDD reduces rework by 40-60% by catching issues early.

---

### ❌ Anti-Pattern 2: Vague Requirements

**Problem:**
```markdown
❌ BAD: "Build a better error handling system"
```

**Solution:**
```markdown
✅ GOOD:
**Problem:** Current errors don't suggest fixes (90% of support tickets)
**Success:** Errors include suggestions, reduce support tickets by 60%
**API:** ErrorFormatter.not_found(entity, id, available_ids)
```

---

### ❌ Anti-Pattern 3: Missing Edge Cases

**Problem:**
```markdown
❌ BAD: Only document happy path
```

**Solution:**
```markdown
✅ GOOD: Document happy path + error cases + edge cases
- Empty input
- Null values
- Maximum values
- Concurrent access
```

---

### ❌ Anti-Pattern 4: No Review/Approval

**Problem:**
```markdown
❌ BAD: Write docs → Skip review → Start coding → Product says "not what we wanted"
```

**Solution:**
```markdown
✅ GOOD: Write docs → Get explicit approval from all stakeholders → Then code
```

---

### ❌ Anti-Pattern 5: Documentation Doesn't Match Code

**Problem:**
```markdown
❌ BAD: Write docs → Code differently → Docs become stale
```

**Solution:**
```markdown
✅ GOOD:
1. Write docs (API reference)
2. Extract tests from docs (test_extraction: true)
3. Implement to match docs exactly
4. Tests ensure docs and code stay in sync
```

---

## Summary

**DDD in 5 Steps:**
1. **Understand the Need** (30-60 min) - Why are we building this?
2. **Define Acceptance Criteria** (30-60 min) - What does "done" look like?
3. **Design the API** (1-2 hours) - What is the exact interface?
4. **Document Examples** (30-60 min) - How will it be used?
5. **Review & Validate** (30-60 min) - Get sign-off before coding

**Total Time:** 3-5 hours
**ROI:** Saves 8-15 hours of rework

**Key Principle:** If you can't document it clearly, you can't build it correctly.

---

## Related Documentation

- [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md) - Phase 3: Requirements & Design
- [BDD_WORKFLOW.md](BDD_WORKFLOW.md) - Next step after DDD
- [TDD_WORKFLOW.md](TDD_WORKFLOW.md) - Implementation workflow
- [DEVELOPMENT_LIFECYCLE.md](DEVELOPMENT_LIFECYCLE.md) - How DDD, BDD, TDD integrate

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Last Updated:** 2025-10-25
**Maintained By:** Project team
**Next Review:** Quarterly
