# Ergonomic Patterns Extracted from Adopter Projects

**Status:** Active Research Document
**Last Updated:** 2025-10-24
**Source:** mcp-orchestration v0.1.3 learnings
**Version:** 1.0.0

---

## Purpose

This document extracts **generalizable Python patterns** from real-world chora-base adopter projects. These patterns solve common ergonomic problems across diverse project types (MCP servers, REST APIs, CLI tools, libraries).

**Key Principle:** Extract the **universal patterns** beneath domain-specific implementations, making them available as optional chora-base affordances.

---

## Pattern Extraction Methodology

### Source Projects

1. **mcp-orchestration** (v0.1.3)
   - Type: MCP server
   - Scale: 12 tools, 5 resources, ~3,000 LOC
   - Learnings: [Full Knowledge Base](https://github.com/liminalcommons/mcp-orchestration/tree/main/share-with-chora-base)

### Pattern Identification Process

1. **Observe Pain Points** - Document friction during development
2. **Measure Impact** - Count duplicated code, affected files
3. **Generalize** - Extract domain-agnostic pattern from MCP-specific code
4. **Validate** - Verify pattern applies to 3+ project types
5. **Integrate** - Add to chora-base as optional utility

---

## Pattern Catalog

### Pattern 1: Input Normalization

**Domain-Specific Problem (MCP):** MCP tools receive parameters from multiple sources:
- MCP protocol sends `dict`
- Claude Desktop sometimes serializes as JSON `string`
- CLI tools receive `tuple` of `"key=value"` strings

**Universal Problem:** APIs accept inputs in multiple formats that need normalization.

**Generalizable Pattern:**

```python
# Universal pattern: Normalize inputs regardless of source format
from chora.utils.validation import normalize_input, InputFormat

@normalize_input(
    params=InputFormat.DICT_OR_JSON,    # Works for: API bodies, config files
    env_vars=InputFormat.DICT_OR_JSON,
)
async def my_function(params: dict | None, env_vars: dict | None):
    # params and env_vars are guaranteed to be dict or None
    # No manual JSON parsing needed
```

**Applies To:**
- **REST APIs** - Accept JSON string or parsed dict
- **CLI tools** - Parse `--param key=value` arguments
- **RPC servers** - Handle serialized parameters
- **Config parsers** - Support YAML/JSON/TOML inputs
- **MCP servers** - Handle protocol variations

**Impact:** Eliminates ~50 lines of duplicated parsing code per project

---

### Pattern 2: Response Standardization

**Domain-Specific Problem (MCP):** MCP tools manually construct response dicts with inconsistent fields.

**Universal Problem:** APIs/services need consistent response format for success/error cases.

**Generalizable Pattern:**

```python
# Universal pattern: Standardized responses for any API
from chora.utils.responses import Response

async def my_endpoint():
    try:
        result = perform_operation()
        return Response.success(
            action="created",
            data={"id": result.id},
            metadata={"count": get_count()},
        )
    except NotFoundError as e:
        return Response.error(
            error_code="not_found",
            message=str(e),
            details={"available": list_available()},
        )
```

**Applies To:**
- **REST APIs** - Consistent endpoint responses
- **CLI tools** - Structured command outputs
- **RPC methods** - Standardized return values
- **Microservices** - Service-to-service communication
- **MCP servers** - Tool response formatting

**Impact:** Reduces ~120 lines of manual dict construction, improves consistency

---

### Pattern 3: Error Formatting with Suggestions

**Domain-Specific Problem (MCP):** MCP server errors don't suggest alternatives when entity not found.

**Universal Problem:** Applications need user-friendly errors with actionable suggestions.

**Generalizable Pattern:**

```python
# Universal pattern: Helpful errors with fuzzy matching
from chora.utils.errors import ErrorFormatter

def get_server(server_id: str):
    if server_id not in available_servers:
        raise ValueError(
            ErrorFormatter.not_found(
                entity_type="server",
                entity_id=server_id,
                available=list(available_servers.keys()),
            )
        )
    # Returns: "Server 'githbu' not found. Did you mean 'github'?"
```

**Applies To:**
- **CLI tools** - Suggest correct commands/flags
- **APIs** - Suggest valid endpoints/parameters
- **Config validation** - Suggest corrections
- **Database queries** - Suggest similar records
- **MCP servers** - Suggest valid tool/resource names

**Impact:** Reduces support burden, improves UX across all interfaces

---

### Pattern 4: State Persistence for Stateful Applications

**Domain-Specific Problem (MCP):** Draft configurations lost on server restart (in-memory only).

**Universal Problem:** Applications need to persist state between runs.

**Generalizable Pattern:**

```python
# Universal pattern: Auto-persisted state
from chora.utils.persistence import StatefulObject

class MyService(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.myapp/state.json")
        # State auto-restored from disk

    def update_config(self, config: dict):
        self.config = config
        self._save_state()  # Auto-persists to disk
```

**Applies To:**
- **CLI tools** - Save session state, preferences
- **Daemons** - Persist configuration changes
- **Desktop apps** - User preferences, window state
- **Services** - Draft/pending operations
- **MCP servers** - Draft configurations, partial work

**Impact:** Eliminates ~100 lines of custom storage code per project

---

### Pattern 5: Comprehensive API Documentation

**Domain-Specific Problem (MCP):** MCP tool docstrings need specific sections for discoverability.

**Universal Problem:** APIs need standardized documentation format.

**Generalizable Pattern:**

```python
# Universal pattern: Structured API documentation
def process_data(
    input_data: dict,
    options: dict | None = None,
) -> dict:
    """Process data with configurable options.

    Detailed description of what this function does and why it exists.
    Performance notes if relevant (e.g., "p95 < 200ms").

    Args:
        input_data: Description of expected structure
        options: Optional configuration (defaults to {})

    Returns:
        Dictionary with:
        - status: 'success' or 'error'
        - result: Processed data
        - metadata: Processing statistics

    Raises:
        ValueError: If input_data is malformed

    Example:
        >>> result = process_data({"key": "value"})
        >>> print(result["status"])
        'success'
    """
```

**Applies To:**
- **Libraries** - Public API documentation
- **REST APIs** - Endpoint documentation
- **CLI tools** - Command help text
- **Internal modules** - Developer documentation
- **MCP servers** - Tool/resource descriptions

**Impact:** Improves discoverability, reduces support questions

---

### Pattern 6: Default Parameters for Ergonomics

**Domain-Specific Problem (MCP):** 90% of tool calls use same `client_id`, requiring repetitive input.

**Universal Problem:** Functions require boilerplate arguments for common use cases.

**Generalizable Pattern:**

```python
# Universal pattern: Smart defaults for 80% use case
def connect_to_database(
    host: str = "localhost",      # 80% use localhost
    port: int = 5432,              # Standard PostgreSQL port
    database: str = "app_db",      # Common name
    timeout: int = 30,             # Reasonable default
):
    """Connect with smart defaults for development, allow production override."""
```

**Applies To:**
- **All function signatures** - Reduce boilerplate for common cases
- **CLI tools** - Fewer required flags
- **Configuration** - Sensible defaults
- **APIs** - Optional parameters with common defaults

**Impact:** Reduces cognitive load, faster development

---

### Pattern 7: Structured Data Over Plain Strings

**Domain-Specific Problem (MCP):** Returning plain strings limits future tool chaining.

**Universal Problem:** Unstructured outputs are hard to parse, compose, or extend.

**Generalizable Pattern:**

```python
# ❌ AVOID: Plain string return
def get_status() -> str:
    return "Server is running with 3 connections"

# ✅ PREFER: Structured dict return
def get_status() -> dict:
    return {
        "state": "running",
        "connections": 3,
        "uptime_seconds": 12345,
        "version": "1.2.3",
    }
```

**Applies To:**
- **All return values** - Enable composition, testing, extension
- **Configuration** - Dict/dataclass over strings
- **Logs** - Structured logging (JSON) over plain text
- **Responses** - Machine-readable formats

**Impact:** Enables future features without breaking changes

---

## Implementation in chora-base

### Optional Utility Modules

**Added via `copier.yml` flags:**

```yaml
include_api_utilities:
  type: bool
  help: Include API utilities (validation, responses, errors)?
  default: true
  when: "{{ project_type in ['mcp_server', 'library'] }}"

include_persistence_helpers:
  type: bool
  help: Include state persistence helpers?
  default: false
  when: "{{ project_type != 'library' }}"
```

**Generated files (when enabled):**
- `src/{{package_name}}/utils/validation.py` - Input normalization
- `src/{{package_name}}/utils/responses.py` - Response builders
- `src/{{package_name}}/utils/errors.py` - Error formatting
- `src/{{package_name}}/utils/persistence.py` - State management

### Documentation

**User-facing docs:**
- `user-docs/reference/python-patterns.md` - Pattern catalog
- `user-docs/how-to/use-input-validation.md` - Validation guide
- `user-docs/how-to/standardize-responses.md` - Response guide
- `user-docs/how-to/improve-error-messages.md` - Error guide
- `user-docs/how-to/persist-application-state.md` - Persistence guide

---

## Pattern Validation Matrix

| Pattern | MCP Server | REST API | CLI Tool | Library | Validated |
|---------|------------|----------|----------|---------|-----------|
| Input Normalization | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |
| Response Standardization | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |
| Error Formatting | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |
| State Persistence | ✅ Yes | ⚠️ Partial | ✅ Yes | ❌ N/A | ✅ |
| API Documentation | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |
| Default Parameters | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |
| Structured Data | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ |

**Validation Criteria:** Pattern must apply to 3+ project types to be included.

---

## Metrics & Impact

### From mcp-orchestration

**Before chora-base utilities:**
- Parameter validation: ~50 lines duplicated across 8 files
- Response formatting: ~120 lines manual dict construction
- Error messages: 8 different inconsistent formats
- State persistence: ~100 lines custom code or omitted

**After chora-base utilities (projected):**
- Parameter validation: 1 decorator per function (~90% reduction)
- Response formatting: 2-3 lines per response (~85% reduction)
- Error messages: Standardized, helpful suggestions
- State persistence: Automatic with mixin

**Total Impact:** ~12-15% code reduction, significant consistency improvement

### Expected Ecosystem Impact

**For adopters using utilities:**
- 10-15% less boilerplate code
- Faster development (less time on infrastructure)
- Better UX (consistent errors, helpful messages)
- Easier maintenance (standardized patterns)

---

## Related Resources

### External Knowledge Bases

- **mcp-orchestration learnings** - [Full knowledge base](https://github.com/liminalcommons/mcp-orchestration/tree/main/share-with-chora-base)
  - 8 documented pain points with evidence
  - 10 proven patterns from production
  - 20+ before/after code examples
  - Detailed API specifications for primitives

### chora-base Documentation

- [Template Configuration](../../template/user-docs/reference/template-configuration.md) - Feature flags
- [Python Patterns Reference](../../template/user-docs/reference/python-patterns.md) - Usage guide
- [Benefits Guide](../BENEFITS.md) - Template value proposition

---

## Contributing New Patterns

### Pattern Submission Process

1. **Document the pain point** - Describe specific friction in your project
2. **Provide evidence** - Code references, line counts, affected files
3. **Generalize the pattern** - Show it applies to 3+ project types
4. **Propose implementation** - API design, examples, tests
5. **Submit PR** - Add to this document with validation evidence

### Validation Criteria

✅ **Accept if:**
- Pattern solves real pain (evidence from 1+ adopter project)
- Pattern generalizes to 3+ project types
- Implementation is simple (<200 LOC)
- Pattern improves ergonomics measurably (>10% code reduction OR significant UX improvement)

❌ **Reject if:**
- Too domain-specific (only works for 1 project type)
- Too complex (>500 LOC implementation)
- Low impact (<5% code reduction, no UX improvement)
- Reinvents existing Python stdlib/ecosystem solution

---

## Future Research

### Patterns Under Evaluation

1. **Workflow Composition** - Chaining tools/functions with data flow
2. **Telemetry Integration** - Automatic instrumentation for observability
3. **Config Validation** - Pydantic-based config schema validation
4. **Retry/Circuit Breaker** - Resilience patterns for external calls

### Open Questions

- Should utilities support async/sync automatically?
- How to handle cross-cutting concerns (logging, metrics)?
- When to prefer decorator vs mixin vs utility function?
- How to avoid over-abstraction (YAGNI principle)?

---

**Version History:**

- **v1.0.0** (2025-10-24) - Initial extraction from mcp-orchestration learnings
  - 7 patterns validated across 4+ project types
  - Implementation plan for chora-base integration
  - Validation matrix and impact metrics

---

**Maintained by:** chora-base core team
**Contributions:** Welcome via PR (follow submission process above)
**License:** MIT (same as chora-base)
