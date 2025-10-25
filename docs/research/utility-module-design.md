# Utility Module Design - chora-base Affordances

**Status:** Design Document
**Last Updated:** 2025-10-24
**Version:** 1.0.0

---

## Overview

This document defines the design for optional utility modules in chora-base, extracted from real-world adopter patterns (mcp-orchestration v0.1.3).

**Design Principles:**
1. **Optional, not mandatory** - Via copier.yml flags
2. **Generic, not domain-specific** - Works for MCP, REST, CLI, libraries
3. **Simple, not over-engineered** - <200 LOC per module
4. **Tested, not theoretical** - 90%+ test coverage

---

## Module Structure

```
template/src/{{package_name}}/utils/
├── __init__.py.jinja              # Conditional exports
├── validation.py.jinja            # Input normalization (if include_api_utilities)
├── responses.py.jinja             # Response builders (if include_api_utilities)
├── errors.py.jinja                # Error formatting (if include_api_utilities)
└── persistence.py.jinja           # State management (if include_persistence_helpers)
```

---

## Module 1: validation.py - Input Normalization

### Purpose
Normalize parameters from multiple input sources (JSON strings, dicts, key=value pairs).

### API Design

```python
from enum import Enum
from functools import wraps
from typing import Any, Callable
import json

class InputFormat(Enum):
    """Supported input formats."""
    DICT_ONLY = "dict_only"
    DICT_OR_JSON = "dict_or_json"
    KV_PAIRS = "kv_pairs"
    DICT_OR_KV = "dict_or_kv"

def normalize_input(**param_specs) -> Callable:
    """Decorator to auto-convert parameter formats.

    Args:
        **param_specs: Mapping of parameter names to InputFormat values

    Example:
        @normalize_input(
            params=InputFormat.DICT_OR_JSON,
            env_vars=InputFormat.DICT_OR_JSON,
        )
        async def my_func(params: dict | None, env_vars: dict | None):
            # params/env_vars guaranteed to be dict or None
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            for param_name, format_type in param_specs.items():
                if param_name in kwargs:
                    kwargs[param_name] = _convert_param(
                        kwargs[param_name], format_type, param_name
                    )
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            for param_name, format_type in param_specs.items():
                if param_name in kwargs:
                    kwargs[param_name] = _convert_param(
                        kwargs[param_name], format_type, param_name
                    )
            return func(*args, **kwargs)

        # Return appropriate wrapper based on function type
        import inspect
        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator

def _convert_param(value: Any, format_type: InputFormat, param_name: str) -> Any:
    """Convert parameter based on format type."""
    if value is None:
        return None

    if format_type == InputFormat.DICT_ONLY:
        if not isinstance(value, dict):
            raise TypeError(f"Parameter '{param_name}' must be dict")
        return value

    elif format_type == InputFormat.DICT_OR_JSON:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                raise ValueError(f"Parameter '{param_name}' invalid JSON: {e}")
        elif isinstance(value, dict):
            return value
        else:
            raise TypeError(f"Parameter '{param_name}' must be dict or JSON string")

    elif format_type == InputFormat.KV_PAIRS:
        if isinstance(value, (list, tuple)):
            result = {}
            for item in value:
                if isinstance(item, str) and "=" in item:
                    key, val = item.split("=", 1)
                    result[key.strip()] = val.strip()
                else:
                    raise ValueError(f"Item '{item}' not in 'key=value' format")
            return result
        elif isinstance(value, dict):
            return value
        else:
            raise TypeError(f"Parameter '{param_name}' must be list or dict")

    return value
```

### Use Cases
- **MCP servers** - Handle dict/JSON from protocol/client
- **REST APIs** - Accept JSON body or query params
- **CLI tools** - Parse `--param key=value` arguments
- **Config parsers** - Support YAML/JSON/TOML

### LOC: ~150 lines (implementation + docstrings)

---

## Module 2: responses.py - Response Builders

### Purpose
Standardize response format for success/error/partial cases with auto-logging.

### API Design

```python
from dataclasses import dataclass, field
from typing import Any
import time
import logging

logger = logging.getLogger(__name__)

@dataclass
class Response:
    """Standardized response format."""

    @classmethod
    def success(
        cls,
        action: str,
        data: Any = None,
        **metadata: Any,
    ) -> dict[str, Any]:
        """Create success response.

        Args:
            action: What action was performed (e.g., 'created', 'updated')
            data: Result data
            **metadata: Additional metadata (counts, timestamps, etc.)

        Returns:
            Standardized response dict with status='success'

        Example:
            >>> Response.success(
            ...     action="created",
            ...     data={"id": 123},
            ...     count=1,
            ... )
            {
                "status": "success",
                "action": "created",
                "data": {"id": 123},
                "metadata": {"count": 1},
                "timestamp": 1698765432.123,
            }
        """
        response = {
            "status": "success",
            "action": action,
            "data": data,
            "metadata": metadata,
            "timestamp": time.time(),
        }
        logger.info(f"Success: {action}", extra={"response": response})
        return response

    @classmethod
    def error(
        cls,
        error_code: str,
        message: str,
        recoverable: bool = True,
        **details: Any,
    ) -> dict[str, Any]:
        """Create error response.

        Args:
            error_code: Machine-readable error code
            message: Human-readable error message
            recoverable: Whether error is recoverable
            **details: Additional error context

        Returns:
            Standardized error dict with status='error'
        """
        response = {
            "status": "error",
            "error_code": error_code,
            "message": message,
            "recoverable": recoverable,
            "details": details,
            "timestamp": time.time(),
        }
        logger.error(f"Error: {error_code} - {message}", extra={"response": response})
        return response

    @classmethod
    def partial(
        cls,
        action: str,
        succeeded: list[Any],
        failed: list[dict[str, Any]],
        **metadata: Any,
    ) -> dict[str, Any]:
        """Create partial success response (for batch operations).

        Args:
            action: What action was attempted
            succeeded: List of successful items
            failed: List of failed items with reasons
            **metadata: Additional metadata

        Returns:
            Standardized partial success dict with status='partial'
        """
        response = {
            "status": "partial",
            "action": action,
            "succeeded": succeeded,
            "failed": failed,
            "metadata": {
                **metadata,
                "succeeded_count": len(succeeded),
                "failed_count": len(failed),
            },
            "timestamp": time.time(),
        }
        logger.warning(
            f"Partial: {action} - {len(succeeded)}/{len(succeeded) + len(failed)} succeeded",
            extra={"response": response}
        )
        return response
```

### Use Cases
- **REST APIs** - Consistent endpoint responses
- **CLI tools** - Structured command outputs
- **RPC methods** - Standardized return values
- **MCP servers** - Tool response formatting

### LOC: ~120 lines

---

## Module 3: errors.py - Error Formatting

### Purpose
Generate user-friendly error messages with suggestions.

### API Design

```python
from difflib import get_close_matches
from typing import Any

class ErrorFormatter:
    """User-friendly error message formatting."""

    @staticmethod
    def not_found(
        entity_type: str,
        entity_id: str,
        available: list[str],
        max_suggestions: int = 3,
    ) -> str:
        """Format 'not found' error with suggestions.

        Args:
            entity_type: Type of entity (e.g., 'server', 'command')
            entity_id: ID that wasn't found
            available: List of valid IDs for suggestions
            max_suggestions: Maximum suggestions to show

        Returns:
            Formatted error message with suggestions

        Example:
            >>> ErrorFormatter.not_found(
            ...     entity_type="command",
            ...     entity_id="buld",
            ...     available=["build", "test", "lint"],
            ... )
            "Command 'buld' not found. Did you mean 'build'?"
        """
        message = f"{entity_type.capitalize()} '{entity_id}' not found."

        # Fuzzy match for suggestions
        suggestions = get_close_matches(
            entity_id, available, n=max_suggestions, cutoff=0.6
        )

        if suggestions:
            if len(suggestions) == 1:
                message += f" Did you mean '{suggestions[0]}'?"
            else:
                suggestion_list = "', '".join(suggestions)
                message += f" Did you mean one of: '{suggestion_list}'?"
        elif available:
            message += f" Available {entity_type}s: {', '.join(available[:5])}"
            if len(available) > 5:
                message += f" (and {len(available) - 5} more)"

        return message

    @staticmethod
    def already_exists(entity_type: str, entity_id: str) -> str:
        """Format 'already exists' error."""
        return f"{entity_type.capitalize()} '{entity_id}' already exists."

    @staticmethod
    def invalid_parameter(
        param_name: str,
        value: Any,
        expected: str,
    ) -> str:
        """Format 'invalid parameter' error."""
        return (
            f"Invalid parameter '{param_name}': got {type(value).__name__}, "
            f"expected {expected}"
        )
```

### Use Cases
- **CLI tools** - Suggest correct commands
- **APIs** - Suggest valid parameters
- **Config validation** - Suggest fixes
- **MCP servers** - Suggest valid tools/resources

### LOC: ~80 lines

---

## Module 4: persistence.py - State Management

### Purpose
Auto-persist object state to disk.

### API Design

```python
from pathlib import Path
from typing import Any
import json
from abc import ABC

class StatefulObject(ABC):
    """Mixin for auto-persisted state.

    Example:
        class MyService(StatefulObject):
            def __init__(self):
                super().__init__(state_file="~/.myapp/state.json")
                self.config = {}

            def update_config(self, config: dict):
                self.config = config
                self._save_state()  # Auto-persists
    """

    def __init__(self, state_file: Path | str, **kwargs):
        """Initialize stateful object.

        Args:
            state_file: Path to state persistence file
        """
        super().__init__(**kwargs)
        self._state_file = Path(state_file).expanduser()
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_state()

    def _save_state(self):
        """Save current state to disk."""
        state = self._get_state()
        with open(self._state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def _load_state(self):
        """Load state from disk if exists."""
        if self._state_file.exists():
            with open(self._state_file) as f:
                state = json.load(f)
                self._set_state(state)

    def _get_state(self) -> dict[str, Any]:
        """Override to define what state to persist.

        Returns:
            Dictionary of state to save
        """
        # Default: save all non-private attributes
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }

    def _set_state(self, state: dict[str, Any]):
        """Override to restore state.

        Args:
            state: Dictionary of state to restore
        """
        # Default: restore all attributes
        for k, v in state.items():
            setattr(self, k, v)
```

### Use Cases
- **CLI tools** - Save session state
- **Daemons** - Persist configuration
- **Services** - Draft/pending operations
- **MCP servers** - Draft configurations

### LOC: ~100 lines

---

## Conditional Generation

### copier.yml Flags

```yaml
# === Python Ergonomics (Optional) ===

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

### File Generation Logic

**When `include_api_utilities: true`:**
- Generate `utils/validation.py`
- Generate `utils/responses.py`
- Generate `utils/errors.py`
- Update `utils/__init__.py` with exports

**When `include_persistence_helpers: true`:**
- Generate `utils/persistence.py`
- Update `utils/__init__.py` with exports

**When both false:**
- Don't create `utils/` directory at all

---

## Testing Strategy

### Test Coverage Requirements
- **All modules:** 90%+ test coverage
- **Edge cases:** JSON parsing errors, invalid formats, fuzzy matching
- **Both sync/async:** Test decorator with both function types

### Test Structure

```
tests/utils/
├── test_validation.py      # 20+ test cases
├── test_responses.py        # 15+ test cases
├── test_errors.py           # 10+ test cases
└── test_persistence.py      # 15+ test cases
```

---

## Documentation

### User-Facing Docs

1. **Reference:** `template/user-docs/reference/python-patterns.md`
   - Pattern catalog with examples
   - When to use each utility
   - Best practices

2. **How-To Guides:**
   - `template/user-docs/how-to/use-input-validation.md`
   - `template/user-docs/how-to/standardize-responses.md`
   - `template/user-docs/how-to/improve-error-messages.md`
   - `template/user-docs/how-to/persist-application-state.md`

3. **AGENTS.md Section:**
   ```markdown
   ## Optional Utilities

   {% if include_api_utilities %}
   This project includes utilities:
   - `utils.validation` - Normalize inputs
   - `utils.responses` - Format responses
   - `utils.errors` - Helpful errors
   {% endif %}
   ```

---

## Success Criteria

✅ **Generalization:** Utilities work for 3+ project types (MCP, REST, CLI)
✅ **Simplicity:** Each module <200 LOC
✅ **Quality:** 90%+ test coverage
✅ **Documentation:** Clear examples for all use cases
✅ **Impact:** 10%+ code reduction in adopter projects

---

## Implementation Timeline

- **Week 2:** Implement validation.py + tests
- **Week 3:** Implement responses.py + errors.py + tests
- **Week 4:** Implement persistence.py + tests
- **Week 5:** Create documentation

---

**Maintained by:** chora-base core team
**Version:** 1.0.0 (2025-10-24)
