# Custom Generator Tutorial: chora-compose Meta

**SAP ID**: SAP-018 (Supporting Documentation)
**Version**: 1.0.0
**Last Updated**: 2025-11-04

---

## Overview

Complete step-by-step tutorial for creating custom content generators in chora-compose Meta. Build three increasingly sophisticated generators: a static badge generator, a dynamic API documentation generator, and a test case generator.

**What You'll Learn**:
- BaseGenerator interface and lifecycle
- Context resolution and validation
- Template rendering patterns
- Error handling and validation
- Generator registration and discovery
- Testing custom generators

**Prerequisites**:
- Python 3.12+
- chora-compose v1.5.0+ installed
- Basic understanding of Python classes and inheritance
- Familiarity with chora-compose MCP tools (see [protocol-spec.md](./protocol-spec.md))

**Time to Complete**: 2-3 hours (all 3 generators)

---

## Table of Contents

1. [Generator Architecture Overview](#1-generator-architecture-overview)
2. [Tutorial 1: Badge Generator (Beginner)](#2-tutorial-1-badge-generator-beginner)
3. [Tutorial 2: API Documentation Generator (Intermediate)](#3-tutorial-2-api-documentation-generator-intermediate)
4. [Tutorial 3: Test Case Generator (Advanced)](#4-tutorial-3-test-case-generator-advanced)
5. [Generator Registration & Discovery](#5-generator-registration--discovery)
6. [Testing Your Generators](#6-testing-your-generators)
7. [Best Practices](#7-best-practices)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Generator Architecture Overview

### BaseGenerator Interface

All custom generators must inherit from `chora_compose.generators.BaseGenerator` and implement these methods:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseGenerator(ABC):
    """Base class for all content generators."""

    @abstractmethod
    def generate(self, context: Dict[str, Any], config: Dict[str, Any]) -> str:
        """
        Generate content from context and config.

        Args:
            context: Resolved context variables (from config + runtime)
            config: Full content configuration

        Returns:
            Generated content as string

        Raises:
            GenerationError: If generation fails
            ValidationError: If context/config invalid
        """
        pass

    def validate_context(self, context: Dict[str, Any]) -> None:
        """
        Validate context before generation (optional override).

        Args:
            context: Context to validate

        Raises:
            ValidationError: If context invalid
        """
        pass

    def get_required_context_keys(self) -> list[str]:
        """
        Return list of required context keys (optional override).

        Returns:
            List of required context key names
        """
        return []
```

### Generator Lifecycle

```
1. Registration
   ├─ Generator class imported
   ├─ Registered in GeneratorRegistry
   └─ Available via list_generators tool

2. Invocation (generate_content)
   ├─ Load content config
   ├─ Resolve context (inline_data, external_file, etc.)
   ├─ Merge config context + runtime context
   ├─ Select generator by type
   ├─ Call validate_context() [optional]
   └─ Call generate(context, config)

3. Generation
   ├─ Apply template/logic
   ├─ Return generated string
   ├─ Store in ephemeral storage
   └─ Emit content_generated event
```

### File Structure

Recommended project structure:

```
my_project/
├── generators/                    # Custom generators package
│   ├── __init__.py               # Package init (imports generators)
│   ├── badge_generator.py        # Tutorial 1
│   ├── api_doc_generator.py      # Tutorial 2
│   └── test_case_generator.py    # Tutorial 3
├── configs/
│   └── content/
│       ├── badge.json            # Config for badge generator
│       ├── api-endpoint.json     # Config for API doc generator
│       └── test-case.json        # Config for test case generator
├── tests/
│   └── test_generators.py        # Generator tests
└── pyproject.toml                # Dependencies (chora-compose)
```

---

## 2. Tutorial 1: Badge Generator (Beginner)

**Goal**: Create a simple generator that produces Markdown shields.io badges.

**Difficulty**: ⭐ Beginner (30-45 minutes)

**Features**:
- Static template rendering
- Context variable substitution
- Simple validation

### Step 1: Create Generator Class

Create `generators/badge_generator.py`:

```python
"""
Badge Generator: Generate shields.io badges in Markdown.

Usage:
    Config requires context with: label, message, color
    Optional: style (flat, flat-square, plastic, etc.)
"""

from typing import Dict, Any
from chora_compose.generators import BaseGenerator
from chora_compose.exceptions import ValidationError


class BadgeGenerator(BaseGenerator):
    """Generates shields.io badges in Markdown format."""

    def get_required_context_keys(self) -> list[str]:
        """Badge requires label, message, and color."""
        return ["label", "message", "color"]

    def validate_context(self, context: Dict[str, Any]) -> None:
        """
        Validate badge context.

        Checks:
        - Required keys present
        - Color is valid shields.io color
        """
        required = self.get_required_context_keys()
        missing = [key for key in required if key not in context]

        if missing:
            raise ValidationError(
                f"Missing required context keys: {', '.join(missing)}",
                details={"missing_keys": missing}
            )

        # Validate color (shields.io supports hex, named colors, or status codes)
        color = context["color"]
        valid_colors = [
            "brightgreen", "green", "yellowgreen", "yellow",
            "orange", "red", "blue", "lightgrey", "success",
            "important", "critical", "informational", "inactive"
        ]

        if not (color in valid_colors or color.startswith("#")):
            raise ValidationError(
                f"Invalid color '{color}'. Must be named color or hex (#RRGGBB)",
                details={"color": color, "valid_colors": valid_colors}
            )

    def generate(self, context: Dict[str, Any], config: Dict[str, Any]) -> str:
        """
        Generate shields.io badge in Markdown.

        Example output:
            ![Status](https://img.shields.io/badge/status-active-brightgreen)
        """
        label = context["label"]
        message = context["message"]
        color = context["color"]
        style = context.get("style", "flat")  # Default: flat style

        # URL-encode label and message (simple approach)
        label_encoded = label.replace(" ", "%20").replace("-", "--")
        message_encoded = message.replace(" ", "%20").replace("-", "--")

        # Build shields.io URL
        badge_url = (
            f"https://img.shields.io/badge/"
            f"{label_encoded}-{message_encoded}-{color}"
            f"?style={style}"
        )

        # Generate Markdown image
        alt_text = f"{label}: {message}"
        badge_markdown = f"![{alt_text}]({badge_url})"

        return badge_markdown
```

### Step 2: Create Content Config

Create `configs/content/status-badge.json`:

```json
{
  "type": "content",
  "id": "status-badge",
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "Project status badge",
    "version": "1.0.0",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "badge",
      "format": "markdown",
      "example_output": "![Status](https://img.shields.io/badge/status-active-brightgreen)"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "status-badge-pattern",
        "type": "badge",
        "context": {
          "sources": [
            {
              "type": "inline_data",
              "data": {
                "label": "status",
                "message": "active",
                "color": "brightgreen",
                "style": "flat"
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Step 3: Register Generator

Create `generators/__init__.py`:

```python
"""Custom generators package."""

from chora_compose.registry import GeneratorRegistry
from .badge_generator import BadgeGenerator

# Register custom generators
GeneratorRegistry.register("badge", BadgeGenerator)

__all__ = ["BadgeGenerator"]
```

### Step 4: Test Generator

Create `tests/test_badge_generator.py`:

```python
"""Tests for BadgeGenerator."""

import pytest
from generators.badge_generator import BadgeGenerator
from chora_compose.exceptions import ValidationError


def test_badge_generation():
    """Test basic badge generation."""
    generator = BadgeGenerator()

    context = {
        "label": "build",
        "message": "passing",
        "color": "brightgreen"
    }

    config = {}  # Not used in this simple generator

    result = generator.generate(context, config)

    assert "![build: passing]" in result
    assert "https://img.shields.io/badge/build-passing-brightgreen" in result
    assert "style=flat" in result


def test_badge_with_custom_style():
    """Test badge with custom style."""
    generator = BadgeGenerator()

    context = {
        "label": "version",
        "message": "1.0.0",
        "color": "blue",
        "style": "flat-square"
    }

    result = generator.generate(context, {})

    assert "style=flat-square" in result


def test_badge_validation_missing_keys():
    """Test validation catches missing required keys."""
    generator = BadgeGenerator()

    context = {"label": "test"}  # Missing message and color

    with pytest.raises(ValidationError) as exc:
        generator.validate_context(context)

    assert "Missing required context keys" in str(exc.value)
    assert "message" in str(exc.value)
    assert "color" in str(exc.value)


def test_badge_validation_invalid_color():
    """Test validation catches invalid colors."""
    generator = BadgeGenerator()

    context = {
        "label": "test",
        "message": "value",
        "color": "invalid-color"
    }

    with pytest.raises(ValidationError) as exc:
        generator.validate_context(context)

    assert "Invalid color" in str(exc.value)


def test_badge_hex_color():
    """Test badge with hex color."""
    generator = BadgeGenerator()

    context = {
        "label": "custom",
        "message": "badge",
        "color": "#FF6347"  # Tomato red
    }

    generator.validate_context(context)  # Should not raise
    result = generator.generate(context, {})

    assert "#FF6347" in result
```

### Step 5: Run Generator via MCP

**Option 1: Direct Python**:
```python
from chora_compose import ContentGenerator

# Import custom generators (triggers registration)
import generators

# Generate content
generator = ContentGenerator()
result = generator.generate("status-badge", force=False)

print(result["content"])
# Output: ![status: active](https://img.shields.io/badge/status-active-brightgreen?style=flat)
```

**Option 2: MCP Tool (Claude Desktop)**:
```json
{
  "tool": "choracompose:generate_content",
  "arguments": {
    "content_config_id": "status-badge",
    "context": {},
    "force": false
  }
}
```

**Expected Output**:
```markdown
![status: active](https://img.shields.io/badge/status-active-brightgreen?style=flat)
```

### Tutorial 1 Summary

✅ **Learned**:
- BaseGenerator inheritance
- Required context keys pattern
- Context validation
- Simple template rendering
- Generator registration

✅ **Time**: ~30-45 minutes

✅ **Next**: Tutorial 2 builds on this with dynamic data loading

---

## 3. Tutorial 2: API Documentation Generator (Intermediate)

**Goal**: Generate REST API endpoint documentation from OpenAPI spec or manual config.

**Difficulty**: ⭐⭐ Intermediate (60-90 minutes)

**Features**:
- External file loading (OpenAPI spec)
- Dynamic template rendering
- Schema validation
- Multiple output formats

### Step 1: Create Generator Class

Create `generators/api_doc_generator.py`:

```python
"""
API Documentation Generator: Generate REST API endpoint docs.

Supports:
- OpenAPI 3.0 spec loading
- Manual endpoint configuration
- Markdown and ReStructuredText output
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from chora_compose.generators import BaseGenerator
from chora_compose.exceptions import ValidationError, GenerationError


class APIDocGenerator(BaseGenerator):
    """Generates REST API endpoint documentation."""

    SUPPORTED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    SUPPORTED_FORMATS = ["markdown", "rst"]

    def get_required_context_keys(self) -> list[str]:
        """API doc requires endpoint path and method."""
        return ["path", "method"]

    def validate_context(self, context: Dict[str, Any]) -> None:
        """Validate API endpoint context."""
        # Check required keys
        required = self.get_required_context_keys()
        missing = [key for key in required if key not in context]
        if missing:
            raise ValidationError(
                f"Missing required context keys: {', '.join(missing)}",
                details={"missing_keys": missing}
            )

        # Validate HTTP method
        method = context["method"].upper()
        if method not in self.SUPPORTED_METHODS:
            raise ValidationError(
                f"Unsupported HTTP method: {method}",
                details={
                    "method": method,
                    "supported": self.SUPPORTED_METHODS
                }
            )

        # Validate output format
        output_format = context.get("output_format", "markdown")
        if output_format not in self.SUPPORTED_FORMATS:
            raise ValidationError(
                f"Unsupported output format: {output_format}",
                details={
                    "format": output_format,
                    "supported": self.SUPPORTED_FORMATS
                }
            )

    def _load_openapi_spec(self, spec_path: str) -> Optional[Dict[str, Any]]:
        """Load OpenAPI spec from file."""
        try:
            spec_file = Path(spec_path)
            if not spec_file.exists():
                return None

            with open(spec_file) as f:
                if spec_path.endswith(".json"):
                    return json.load(f)
                elif spec_path.endswith((".yaml", ".yml")):
                    import yaml
                    return yaml.safe_load(f)
        except Exception as e:
            raise GenerationError(
                f"Failed to load OpenAPI spec: {e}",
                details={"spec_path": spec_path, "error": str(e)}
            )

        return None

    def _extract_endpoint_from_openapi(
        self,
        spec: Dict[str, Any],
        path: str,
        method: str
    ) -> Optional[Dict[str, Any]]:
        """Extract endpoint details from OpenAPI spec."""
        paths = spec.get("paths", {})
        if path not in paths:
            return None

        method_lower = method.lower()
        endpoint = paths[path].get(method_lower)

        return endpoint

    def _render_markdown(self, endpoint_data: Dict[str, Any]) -> str:
        """Render endpoint documentation in Markdown."""
        lines = []

        # Title
        method = endpoint_data["method"].upper()
        path = endpoint_data["path"]
        lines.append(f"## {method} {path}")
        lines.append("")

        # Summary
        if "summary" in endpoint_data:
            lines.append(endpoint_data["summary"])
            lines.append("")

        # Description
        if "description" in endpoint_data:
            lines.append(endpoint_data["description"])
            lines.append("")

        # Parameters
        parameters = endpoint_data.get("parameters", [])
        if parameters:
            lines.append("### Parameters")
            lines.append("")
            lines.append("| Name | Type | Location | Required | Description |")
            lines.append("|------|------|----------|----------|-------------|")

            for param in parameters:
                name = param.get("name", "")
                param_type = param.get("schema", {}).get("type", "string")
                location = param.get("in", "query")
                required = "Yes" if param.get("required", False) else "No"
                description = param.get("description", "")

                lines.append(f"| {name} | {param_type} | {location} | {required} | {description} |")

            lines.append("")

        # Request Body
        request_body = endpoint_data.get("requestBody")
        if request_body:
            lines.append("### Request Body")
            lines.append("")

            content = request_body.get("content", {})
            for content_type, schema_info in content.items():
                lines.append(f"**Content-Type**: `{content_type}`")
                lines.append("")

                schema = schema_info.get("schema", {})
                if "example" in schema_info:
                    lines.append("**Example**:")
                    lines.append("```json")
                    lines.append(json.dumps(schema_info["example"], indent=2))
                    lines.append("```")
                    lines.append("")

        # Responses
        responses = endpoint_data.get("responses", {})
        if responses:
            lines.append("### Responses")
            lines.append("")

            for status_code, response_info in responses.items():
                description = response_info.get("description", "")
                lines.append(f"**{status_code}**: {description}")
                lines.append("")

                content = response_info.get("content", {})
                for content_type, schema_info in content.items():
                    if "example" in schema_info:
                        lines.append(f"*{content_type}*:")
                        lines.append("```json")
                        lines.append(json.dumps(schema_info["example"], indent=2))
                        lines.append("```")
                        lines.append("")

        # Authentication
        if "security" in endpoint_data:
            lines.append("### Authentication")
            lines.append("")
            security = endpoint_data["security"]
            for scheme in security:
                for scheme_name, scopes in scheme.items():
                    lines.append(f"- **{scheme_name}**: {', '.join(scopes) if scopes else 'No scopes'}")
            lines.append("")

        return "\n".join(lines)

    def _render_rst(self, endpoint_data: Dict[str, Any]) -> str:
        """Render endpoint documentation in ReStructuredText."""
        lines = []

        # Title
        method = endpoint_data["method"].upper()
        path = endpoint_data["path"]
        title = f"{method} {path}"
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")

        # Summary
        if "summary" in endpoint_data:
            lines.append(endpoint_data["summary"])
            lines.append("")

        # Description
        if "description" in endpoint_data:
            lines.append(endpoint_data["description"])
            lines.append("")

        # Parameters
        parameters = endpoint_data.get("parameters", [])
        if parameters:
            lines.append("Parameters")
            lines.append("----------")
            lines.append("")

            for param in parameters:
                name = param.get("name", "")
                param_type = param.get("schema", {}).get("type", "string")
                location = param.get("in", "query")
                required = param.get("required", False)
                description = param.get("description", "")

                lines.append(f"``{name}``")
                lines.append(f"    **Type**: {param_type}")
                lines.append(f"    **Location**: {location}")
                lines.append(f"    **Required**: {'Yes' if required else 'No'}")
                if description:
                    lines.append(f"    {description}")
                lines.append("")

        # Similar rendering for request body and responses...
        # (Abbreviated for brevity - full implementation would mirror Markdown)

        return "\n".join(lines)

    def generate(self, context: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Generate API endpoint documentation."""
        path = context["path"]
        method = context["method"].upper()
        output_format = context.get("output_format", "markdown")

        # Build endpoint data structure
        endpoint_data = {
            "path": path,
            "method": method,
            "summary": context.get("summary", ""),
            "description": context.get("description", ""),
            "parameters": context.get("parameters", []),
            "requestBody": context.get("requestBody"),
            "responses": context.get("responses", {}),
            "security": context.get("security", [])
        }

        # If OpenAPI spec provided, merge data
        openapi_spec_path = context.get("openapi_spec")
        if openapi_spec_path:
            spec = self._load_openapi_spec(openapi_spec_path)
            if spec:
                openapi_endpoint = self._extract_endpoint_from_openapi(
                    spec, path, method
                )
                if openapi_endpoint:
                    # Merge OpenAPI data (OpenAPI takes precedence)
                    endpoint_data.update(openapi_endpoint)
                    endpoint_data["path"] = path
                    endpoint_data["method"] = method

        # Render based on output format
        if output_format == "markdown":
            return self._render_markdown(endpoint_data)
        elif output_format == "rst":
            return self._render_rst(endpoint_data)
        else:
            raise GenerationError(f"Unsupported output format: {output_format}")
```

### Step 2: Create Content Config

Create `configs/content/api-get-users.json`:

```json
{
  "type": "content",
  "id": "api-get-users",
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "GET /api/users endpoint documentation",
    "version": "1.0.0",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "endpoint-doc",
      "format": "markdown",
      "example_output": "## GET /api/users\n\nRetrieve list of users..."
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "api-doc-pattern",
        "type": "api_doc",
        "context": {
          "sources": [
            {
              "type": "inline_data",
              "data": {
                "path": "/api/users",
                "method": "GET",
                "summary": "Retrieve list of users",
                "description": "Returns a paginated list of all users in the system.",
                "parameters": [
                  {
                    "name": "page",
                    "in": "query",
                    "schema": {"type": "integer", "default": 1},
                    "description": "Page number for pagination"
                  },
                  {
                    "name": "limit",
                    "in": "query",
                    "schema": {"type": "integer", "default": 20},
                    "description": "Number of users per page"
                  }
                ],
                "responses": {
                  "200": {
                    "description": "Successful response",
                    "content": {
                      "application/json": {
                        "example": {
                          "users": [
                            {"id": 1, "name": "Alice", "email": "alice@example.com"},
                            {"id": 2, "name": "Bob", "email": "bob@example.com"}
                          ],
                          "page": 1,
                          "total": 42
                        }
                      }
                    }
                  },
                  "401": {
                    "description": "Unauthorized - invalid or missing API key"
                  }
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Step 3: Update Generator Registration

Update `generators/__init__.py`:

```python
"""Custom generators package."""

from chora_compose.registry import GeneratorRegistry
from .badge_generator import BadgeGenerator
from .api_doc_generator import APIDocGenerator

# Register custom generators
GeneratorRegistry.register("badge", BadgeGenerator)
GeneratorRegistry.register("api_doc", APIDocGenerator)

__all__ = ["BadgeGenerator", "APIDocGenerator"]
```

### Step 4: Test Generator

Run via MCP:
```json
{
  "tool": "choracompose:generate_content",
  "arguments": {
    "content_config_id": "api-get-users",
    "context": {},
    "force": false
  }
}
```

**Expected Output**:
```markdown
## GET /api/users

Retrieve list of users

Returns a paginated list of all users in the system.

### Parameters

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| page | integer | query | No | Page number for pagination |
| limit | integer | query | No | Number of users per page |

### Responses

**200**: Successful response

*application/json*:
```json
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
  ],
  "page": 1,
  "total": 42
}
```

**401**: Unauthorized - invalid or missing API key
```

### Tutorial 2 Summary

✅ **Learned**:
- External file loading (OpenAPI specs)
- Dynamic template rendering
- Multiple output formats (Markdown, RST)
- Complex data structure handling
- Error handling patterns

✅ **Time**: ~60-90 minutes

✅ **Next**: Tutorial 3 builds on this with code generation

---

## 4. Tutorial 3: Test Case Generator (Advanced)

**Goal**: Generate test cases from specifications (BDD scenarios, unit tests, integration tests).

**Difficulty**: ⭐⭐⭐ Advanced (90-120 minutes)

**Features**:
- Code generation (Python pytest, JavaScript Jest)
- Template-based rendering (Jinja2)
- Fixture management
- Multi-file output

### Step 1: Create Generator Class

Create `generators/test_case_generator.py`:

```python
"""
Test Case Generator: Generate test cases from specifications.

Supports:
- Pytest (Python)
- Jest (JavaScript/TypeScript)
- BDD scenarios (Gherkin → test code)
"""

from typing import Dict, Any, List
from jinja2 import Template, Environment, BaseLoader
from chora_compose.generators import BaseGenerator
from chora_compose.exceptions import ValidationError, GenerationError


class TestCaseGenerator(BaseGenerator):
    """Generates test cases from specifications."""

    SUPPORTED_FRAMEWORKS = ["pytest", "jest"]
    SUPPORTED_TYPES = ["unit", "integration", "e2e", "bdd"]

    # Pytest template
    PYTEST_TEMPLATE = '''"""
{{ test_description }}

Generated test file for {{ module_name }}.
"""

import pytest
{% for import_stmt in imports %}
{{ import_stmt }}
{% endfor %}


{% for fixture in fixtures %}
@pytest.fixture
def {{ fixture.name }}():
    """{{ fixture.description }}"""
    {{ fixture.setup | indent(4) }}
    yield {{ fixture.yield_value }}
    {{ fixture.teardown | indent(4) }}


{% endfor %}
{% for test_case in test_cases %}
def test_{{ test_case.name }}({% for fixture in test_case.fixtures %}{{ fixture }}{{ ", " if not loop.last else "" }}{% endfor %}):
    """{{ test_case.description }}"""
    # Arrange
    {% for line in test_case.arrange %}
    {{ line }}
    {% endfor %}

    # Act
    {% for line in test_case.act %}
    {{ line }}
    {% endfor %}

    # Assert
    {% for line in test_case.assertions %}
    {{ line }}
    {% endfor %}


{% endfor %}
'''

    # Jest template (simplified)
    JEST_TEMPLATE = '''/**
 * {{ test_description }}
 *
 * Generated test file for {{ module_name }}.
 */

{% for import_stmt in imports %}
{{ import_stmt }}
{% endfor %}

{% for test_case in test_cases %}
describe('{{ test_case.suite }}', () => {
  test('{{ test_case.description }}', () => {
    // Arrange
    {% for line in test_case.arrange %}
    {{ line }}
    {% endfor %}

    // Act
    {% for line in test_case.act %}
    {{ line }}
    {% endfor %}

    // Assert
    {% for line in test_case.assertions %}
    {{ line }}
    {% endfor %}
  });
});

{% endfor %}
'''

    def get_required_context_keys(self) -> list[str]:
        """Test generator requires framework and test cases."""
        return ["framework", "module_name", "test_cases"]

    def validate_context(self, context: Dict[str, Any]) -> None:
        """Validate test generation context."""
        required = self.get_required_context_keys()
        missing = [key for key in required if key not in context]
        if missing:
            raise ValidationError(
                f"Missing required context keys: {', '.join(missing)}",
                details={"missing_keys": missing}
            )

        # Validate framework
        framework = context["framework"]
        if framework not in self.SUPPORTED_FRAMEWORKS:
            raise ValidationError(
                f"Unsupported test framework: {framework}",
                details={
                    "framework": framework,
                    "supported": self.SUPPORTED_FRAMEWORKS
                }
            )

        # Validate test cases structure
        test_cases = context["test_cases"]
        if not isinstance(test_cases, list) or len(test_cases) == 0:
            raise ValidationError(
                "test_cases must be non-empty list",
                details={"test_cases": test_cases}
            )

        # Validate each test case
        for idx, test_case in enumerate(test_cases):
            required_fields = ["name", "description", "assertions"]
            missing_fields = [f for f in required_fields if f not in test_case]
            if missing_fields:
                raise ValidationError(
                    f"Test case {idx} missing required fields: {', '.join(missing_fields)}",
                    details={"test_case_index": idx, "missing": missing_fields}
                )

    def _render_pytest(self, context: Dict[str, Any]) -> str:
        """Render pytest test file."""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.PYTEST_TEMPLATE)

        return template.render(
            test_description=context.get("test_description", "Test suite"),
            module_name=context["module_name"],
            imports=context.get("imports", []),
            fixtures=context.get("fixtures", []),
            test_cases=context["test_cases"]
        )

    def _render_jest(self, context: Dict[str, Any]) -> str:
        """Render Jest test file."""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.JEST_TEMPLATE)

        return template.render(
            test_description=context.get("test_description", "Test suite"),
            module_name=context["module_name"],
            imports=context.get("imports", []),
            test_cases=context["test_cases"]
        )

    def generate(self, context: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Generate test file based on framework."""
        framework = context["framework"]

        if framework == "pytest":
            return self._render_pytest(context)
        elif framework == "jest":
            return self._render_jest(context)
        else:
            raise GenerationError(f"Unsupported framework: {framework}")
```

### Step 2: Create Content Config

Create `configs/content/test-user-service.json`:

```json
{
  "type": "content",
  "id": "test-user-service",
  "schemaRef": {"id": "content-schema", "version": "3.1"},
  "metadata": {
    "description": "Unit tests for UserService",
    "version": "1.0.0",
    "output_format": "python"
  },
  "elements": [
    {
      "name": "test-suite",
      "format": "python",
      "example_output": "def test_create_user():\n    ..."
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "test-pattern",
        "type": "test_case",
        "context": {
          "sources": [
            {
              "type": "inline_data",
              "data": {
                "framework": "pytest",
                "module_name": "UserService",
                "test_description": "Unit tests for UserService class",
                "imports": [
                  "from myapp.services import UserService",
                  "from myapp.models import User"
                ],
                "fixtures": [
                  {
                    "name": "user_service",
                    "description": "UserService instance with test database",
                    "setup": "service = UserService(db='test.db')\nreturn service",
                    "yield_value": "service",
                    "teardown": "service.close()"
                  }
                ],
                "test_cases": [
                  {
                    "name": "create_user_success",
                    "description": "Test creating a new user successfully",
                    "fixtures": ["user_service"],
                    "arrange": [
                      "user_data = {'name': 'Alice', 'email': 'alice@example.com'}"
                    ],
                    "act": [
                      "result = user_service.create_user(user_data)"
                    ],
                    "assertions": [
                      "assert result.success is True",
                      "assert result.user.name == 'Alice'",
                      "assert result.user.email == 'alice@example.com'"
                    ]
                  },
                  {
                    "name": "create_user_duplicate_email",
                    "description": "Test creating user with duplicate email fails",
                    "fixtures": ["user_service"],
                    "arrange": [
                      "existing_user = user_service.create_user({'name': 'Bob', 'email': 'bob@example.com'})",
                      "duplicate_data = {'name': 'Bobby', 'email': 'bob@example.com'}"
                    ],
                    "act": [
                      "with pytest.raises(ValueError) as exc:",
                      "    user_service.create_user(duplicate_data)"
                    ],
                    "assertions": [
                      "assert 'Email already exists' in str(exc.value)"
                    ]
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Step 3: Update Generator Registration

Update `generators/__init__.py`:

```python
"""Custom generators package."""

from chora_compose.registry import GeneratorRegistry
from .badge_generator import BadgeGenerator
from .api_doc_generator import APIDocGenerator
from .test_case_generator import TestCaseGenerator

# Register custom generators
GeneratorRegistry.register("badge", BadgeGenerator)
GeneratorRegistry.register("api_doc", APIDocGenerator)
GeneratorRegistry.register("test_case", TestCaseGenerator)

__all__ = ["BadgeGenerator", "APIDocGenerator", "TestCaseGenerator"]
```

### Step 4: Generate Test File

Run via MCP:
```json
{
  "tool": "choracompose:generate_content",
  "arguments": {
    "content_config_id": "test-user-service",
    "context": {},
    "force": false
  }
}
```

**Expected Output** (`test_user_service.py`):
```python
"""
Unit tests for UserService class

Generated test file for UserService.
"""

import pytest
from myapp.services import UserService
from myapp.models import User


@pytest.fixture
def user_service():
    """UserService instance with test database"""
    service = UserService(db='test.db')
    return service
    yield service
    service.close()


def test_create_user_success(user_service):
    """Test creating a new user successfully"""
    # Arrange
    user_data = {'name': 'Alice', 'email': 'alice@example.com'}

    # Act
    result = user_service.create_user(user_data)

    # Assert
    assert result.success is True
    assert result.user.name == 'Alice'
    assert result.user.email == 'alice@example.com'


def test_create_user_duplicate_email(user_service):
    """Test creating user with duplicate email fails"""
    # Arrange
    existing_user = user_service.create_user({'name': 'Bob', 'email': 'bob@example.com'})
    duplicate_data = {'name': 'Bobby', 'email': 'bob@example.com'}

    # Act
    with pytest.raises(ValueError) as exc:
        user_service.create_user(duplicate_data)

    # Assert
    assert 'Email already exists' in str(exc.value)
```

### Tutorial 3 Summary

✅ **Learned**:
- Code generation with Jinja2 templates
- Complex context structures
- Fixture management
- Multi-test-case generation
- Template inheritance patterns

✅ **Time**: ~90-120 minutes

✅ **Next**: Learn registration and testing patterns

---

## 5. Generator Registration & Discovery

### Manual Registration

Register generators in `__init__.py`:

```python
from chora_compose.registry import GeneratorRegistry
from .my_generator import MyGenerator

GeneratorRegistry.register("my_generator", MyGenerator)
```

### Auto-Discovery via Entry Points (Future: v2.1.0)

Add to `pyproject.toml`:

```toml
[project.entry-points."chora_compose.generators"]
badge = "my_project.generators:BadgeGenerator"
api_doc = "my_project.generators:APIDocGenerator"
test_case = "my_project.generators:TestCaseGenerator"
```

### List Available Generators

Via MCP:
```json
{
  "tool": "choracompose:list_generators",
  "arguments": {}
}
```

Returns:
```json
{
  "generators": [
    {
      "type": "badge",
      "class": "BadgeGenerator",
      "module": "generators.badge_generator",
      "required_context": ["label", "message", "color"]
    },
    {
      "type": "api_doc",
      "class": "APIDocGenerator",
      "module": "generators.api_doc_generator",
      "required_context": ["path", "method"]
    },
    {
      "type": "test_case",
      "class": "TestCaseGenerator",
      "module": "generators.test_case_generator",
      "required_context": ["framework", "module_name", "test_cases"]
    }
  ]
}
```

---

## 6. Testing Your Generators

### Unit Test Structure

```python
"""
Tests for custom generators.

Run with: pytest tests/test_generators.py -v
"""

import pytest
from chora_compose.exceptions import ValidationError, GenerationError
from generators.badge_generator import BadgeGenerator


class TestBadgeGenerator:
    """Test suite for BadgeGenerator."""

    @pytest.fixture
    def generator(self):
        """Create generator instance."""
        return BadgeGenerator()

    def test_basic_generation(self, generator):
        """Test basic badge generation."""
        context = {
            "label": "test",
            "message": "passing",
            "color": "green"
        }
        result = generator.generate(context, {})
        assert "test-passing-green" in result

    def test_validation_error(self, generator):
        """Test validation catches errors."""
        with pytest.raises(ValidationError):
            generator.validate_context({"label": "test"})

    def test_required_keys(self, generator):
        """Test required keys listing."""
        keys = generator.get_required_context_keys()
        assert "label" in keys
        assert "message" in keys
        assert "color" in keys
```

### Integration Test with MCP

```python
"""Integration tests with chora-compose."""

import pytest
from chora_compose import ContentGenerator
import generators  # Triggers registration


def test_badge_via_content_generator():
    """Test badge generation via ContentGenerator."""
    gen = ContentGenerator()

    # Assumes configs/content/status-badge.json exists
    result = gen.generate("status-badge", force=False)

    assert result["success"] is True
    assert "status-active-brightgreen" in result["content"]
```

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=generators --cov-report=html

# Run specific test
pytest tests/test_badge_generator.py::test_basic_generation -v
```

---

## 7. Best Practices

### 1. Context Validation

**Always validate context** before generation:

```python
def validate_context(self, context: Dict[str, Any]) -> None:
    """Validate required keys and types."""
    # Check required keys
    required = self.get_required_context_keys()
    missing = [k for k in required if k not in context]
    if missing:
        raise ValidationError(f"Missing keys: {missing}")

    # Validate types
    if not isinstance(context.get("count"), int):
        raise ValidationError("count must be integer")
```

### 2. Error Handling

**Provide detailed error messages**:

```python
try:
    result = self._process_data(context)
except Exception as e:
    raise GenerationError(
        f"Failed to process data: {e}",
        details={
            "context": context,
            "error_type": type(e).__name__,
            "error": str(e)
        }
    )
```

### 3. Template Organization

**Extract templates to separate files**:

```
generators/
├── templates/
│   ├── pytest.jinja2
│   ├── jest.jinja2
│   └── api_doc.md.jinja2
└── test_case_generator.py
```

Load templates:
```python
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

template_dir = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("pytest.jinja2")
```

### 4. Caching Awareness

**Generators should be deterministic** for caching to work:

✅ **Good** (deterministic):
```python
def generate(self, context, config):
    return f"Version: {context['version']}"
```

❌ **Bad** (non-deterministic):
```python
import datetime

def generate(self, context, config):
    # Timestamp changes every time!
    return f"Generated at: {datetime.now()}"
```

If you need timestamps, pass them via context.

### 5. Documentation

**Document your generators**:

```python
class MyGenerator(BaseGenerator):
    """
    One-line summary.

    Detailed description of what this generator does,
    when to use it, and any special requirements.

    **Required Context**:
        - key1 (str): Description
        - key2 (int): Description

    **Optional Context**:
        - opt_key (bool): Description (default: False)

    **Example**:
        ```python
        context = {"key1": "value", "key2": 42}
        result = generator.generate(context, {})
        ```

    **Output Format**: markdown
    """
```

---

## 8. Troubleshooting

### Error: Generator not found

**Symptom**:
```json
{
  "error": {
    "code": "generator_not_found",
    "message": "Generator type 'my_generator' not found"
  }
}
```

**Solution**:
1. Check registration in `__init__.py`:
   ```python
   GeneratorRegistry.register("my_generator", MyGenerator)
   ```

2. Verify import path:
   ```python
   import generators  # Triggers __init__.py
   ```

3. List available generators:
   ```json
   {"tool": "choracompose:list_generators", "arguments": {}}
   ```

### Error: Missing required context keys

**Symptom**:
```json
{
  "error": {
    "code": "validation_failed",
    "message": "Missing required context keys: label, color"
  }
}
```

**Solution**:
1. Check `get_required_context_keys()` return value
2. Verify config's `context.sources` includes required data
3. Use `choracompose:preview_generation` to test context

### Error: Template rendering failed

**Symptom**:
```python
jinja2.exceptions.TemplateError: Undefined variable 'foo'
```

**Solution**:
1. Check template variable names match context keys
2. Use Jinja2 defaults: `{{ foo | default("fallback") }}`
3. Validate context structure before rendering

### Performance: Slow generation

**Symptom**: Generation takes >5 seconds for simple content

**Solutions**:
1. **Profile generator**:
   ```python
   import time

   def generate(self, context, config):
       start = time.perf_counter()
       result = self._render(context)
       duration = time.perf_counter() - start
       print(f"Generation took {duration:.2f}s")
       return result
   ```

2. **Cache external data**:
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def _load_schema(self, schema_path):
       # Load once, cache result
       return json.load(open(schema_path))
   ```

3. **Avoid I/O in hot path**: Load files in `__init__` or use lazy loading

---

## Summary

**Completed**:
- ✅ Tutorial 1: Badge Generator (static templates)
- ✅ Tutorial 2: API Doc Generator (dynamic data)
- ✅ Tutorial 3: Test Case Generator (code generation)
- ✅ Registration and discovery
- ✅ Testing strategies
- ✅ Best practices and troubleshooting

**Key Takeaways**:
1. **BaseGenerator interface**: `generate()`, `validate_context()`, `get_required_context_keys()`
2. **Validation first**: Always validate context before generation
3. **Error handling**: Provide detailed error messages with context
4. **Deterministic output**: Ensure same context → same output (for caching)
5. **Testing**: Unit tests + integration tests with ContentGenerator

**Next Steps**:
1. Implement your own generator for your use case
2. Add unit tests with pytest
3. Register and test via MCP tools
4. Share with community (submit to chora-compose generator registry)

**Resources**:
- [protocol-spec.md §2](./protocol-spec.md#2-mcp-tools-specification) - MCP tool reference
- [awareness-guide.md](./awareness-guide.md) - AI agent patterns
- [chora-compose GitHub](https://github.com/liminalcommons/chora-compose) - Source code and examples

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
