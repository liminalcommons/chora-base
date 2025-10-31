# How to Generate API Docs from OpenAPI Schemas

> **Goal:** Transform OpenAPI/Swagger schemas into human-readable API documentation using Jinja2 templates.

## When to Use This

You need this approach when:
- Converting OpenAPI 3.x schemas to documentation
- Generating API reference docs from Swagger files
- Creating multiple doc formats from one schema (Markdown, HTML, RST)
- Automating API documentation updates
- Maintaining consistency between API spec and docs

## Prerequisites

- Chora Compose installed with Jinja2Generator
- OpenAPI 3.x or Swagger 2.x schema file
- Basic understanding of Jinja2 templates
- Familiarity with content configurations

---

## Solution

### Quick Version

**1. Create Jinja2 template for API docs:**

```jinja2
# API Reference: {{ api.info.title }}

Version: {{ api.info.version }}

{{ api.info.description }}

## Endpoints

{% for path, methods in api.paths.items() %}
### {{ path }}

{% for method, operation in methods.items() %}
#### {{ method.upper() }}

{{ operation.summary }}

**Description:** {{ operation.description }}

**Parameters:**
{% for param in operation.parameters %}
- `{{ param.name }}` ({{ param.in }}) - {{ param.description }}
  - Type: {{ param.schema.type }}
  - Required: {{ param.required }}
{% endfor %}

**Response:**
```json
{{ operation.responses['200'].content['application/json'].example | tojson(indent=2) }}
```

{% endfor %}
{% endfor %}
```

**2. Create content config:**

```json
{
  "type": "content",
  "id": "api-docs-from-openapi",
  "generation": {
    "patterns": [{
      "id": "openapi-to-markdown",
      "type": "jinja2",
      "template": "templates/api-reference.j2",
      "context": {
        "api": "data/openapi-spec.json"
      }
    }]
  }
}
```

**3. Generate:**

```python
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

loader = ConfigLoader()
generator = Jinja2Generator()

config = loader.load_content_config("api-docs-from-openapi")
output = generator.generate(config)

print(output)
```

---

## Detailed Steps

### Step 1: Prepare Your OpenAPI Schema

**Example OpenAPI schema** (`data/openapi-spec.json`):

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "User Management API",
    "version": "1.0.0",
    "description": "API for managing users and authentication"
  },
  "paths": {
    "/users": {
      "get": {
        "summary": "List all users",
        "description": "Retrieve a paginated list of all users",
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "description": "Page number",
            "required": false,
            "schema": {"type": "integer", "default": 1}
          },
          {
            "name": "limit",
            "in": "query",
            "description": "Items per page",
            "required": false,
            "schema": {"type": "integer", "default": 20}
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
                  "total": 2
                }
              }
            }
          }
        }
      },
      "post": {
        "summary": "Create a new user",
        "description": "Register a new user in the system",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {"type": "string"},
                  "email": {"type": "string"},
                  "password": {"type": "string"}
                },
                "required": ["name", "email", "password"]
              },
              "example": {
                "name": "Charlie",
                "email": "charlie@example.com",
                "password": "secret123"
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "User created",
            "content": {
              "application/json": {
                "example": {
                  "id": 3,
                  "name": "Charlie",
                  "email": "charlie@example.com"
                }
              }
            }
          }
        }
      }
    },
    "/users/{id}": {
      "get": {
        "summary": "Get user by ID",
        "description": "Retrieve a specific user by their ID",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "User ID",
            "required": true,
            "schema": {"type": "integer"}
          }
        ],
        "responses": {
          "200": {
            "description": "User found",
            "content": {
              "application/json": {
                "example": {
                  "id": 1,
                  "name": "Alice",
                  "email": "alice@example.com"
                }
              }
            }
          },
          "404": {
            "description": "User not found"
          }
        }
      }
    }
  }
}
```

### Step 2: Create Jinja2 Template

**Create template** (`templates/api-reference.j2`):

```jinja2
# {{ api.info.title }}

**Version:** {{ api.info.version }}

{{ api.info.description }}

---

## Endpoints

{% for path, methods in api.paths.items() %}
### `{{ path }}`

{% for method, operation in methods.items() %}
#### {{ method.upper() }} {{ path }}

{{ operation.summary }}

**Description:** {{ operation.description }}

{% if operation.parameters %}
**Parameters:**

| Name | Location | Type | Required | Description |
|------|----------|------|----------|-------------|
{% for param in operation.parameters %}
| `{{ param.name }}` | {{ param.in }} | {{ param.schema.type }} | {{ 'Yes' if param.required else 'No' }} | {{ param.description }} |
{% endfor %}
{% endif %}

{% if operation.requestBody %}
**Request Body:**

```json
{{ operation.requestBody.content['application/json'].example | tojson(indent=2) }}
```

**Schema:**
{% for prop, details in operation.requestBody.content['application/json'].schema.properties.items() %}
- `{{ prop }}` ({{ details.type }}){% if prop in operation.requestBody.content['application/json'].schema.required %} - **Required**{% endif %}
{% endfor %}
{% endif %}

**Responses:**

{% for status, response in operation.responses.items() %}
**{{ status }}** - {{ response.description }}

{% if response.content and 'application/json' in response.content %}
```json
{{ response.content['application/json'].example | tojson(indent=2) }}
```
{% endif %}
{% endfor %}

---

{% endfor %}
{% endfor %}

## Error Codes

All endpoints may return these error codes:

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Authentication required
- `403` - Forbidden: Insufficient permissions
- `500` - Internal Server Error: Server-side error

## Authentication

All endpoints require authentication via Bearer token:

```
Authorization: Bearer <your-api-token>
```
```

### Step 3: Create Content Configuration

**Content config** (`configs/content/api-docs/api-docs-content.json`):

```json
{
  "type": "content",
  "id": "api-docs-from-openapi",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "name": "API Documentation from OpenAPI",
    "description": "Generate API reference docs from OpenAPI schema",
    "version": "1.0",
    "tags": ["api", "documentation", "openapi"]
  },
  "generation": {
    "patterns": [
      {
        "id": "openapi-to-markdown",
        "type": "jinja2",
        "template": "templates/api-reference.j2",
        "context": {
          "api": {
            "source": "file",
            "path": "data/openapi-spec.json"
          }
        }
      }
    ]
  }
}
```

### Step 4: Generate Documentation

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

# Initialize
loader = ConfigLoader()
generator = Jinja2Generator()

# Load config
config = loader.load_content_config("api-docs-from-openapi")

# Generate
output = generator.generate(config)

# Save
output_path = Path("docs/API_REFERENCE.md")
output_path.write_text(output, encoding="utf-8")

print(f"✓ Generated API documentation: {output_path}")
print(f"✓ Size: {len(output)} characters")
```

**Output preview:**

```markdown
# User Management API

**Version:** 1.0.0

API for managing users and authentication

---

## Endpoints

### `/users`

#### GET /users

List all users

**Description:** Retrieve a paginated list of all users

**Parameters:**

| Name | Location | Type | Required | Description |
|------|----------|------|----------|-------------|
| `page` | query | integer | No | Page number |
| `limit` | query | integer | No | Items per page |

**Responses:**

**200** - Successful response

```json
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
  ],
  "page": 1,
  "total": 2
}
```

...
```

---

## Common Patterns

### Pattern: Multi-Version API Docs

Generate docs for multiple API versions:

**Directory structure:**
```
data/
  api-v1.json
  api-v2.json
  api-v3.json
templates/
  api-reference.j2  # Same template for all
```

**Script:**

```python
from pathlib import Path
from chora_compose.generators.jinja2 import Jinja2Generator

generator = Jinja2Generator()

versions = ["v1", "v2", "v3"]

for version in versions:
    # Load OpenAPI spec
    spec_path = Path(f"data/api-{version}.json")
    spec = json.loads(spec_path.read_text())

    # Generate with context
    config = loader.load_content_config("api-docs-template")
    config.generation.patterns[0].context = {"api": spec}

    output = generator.generate(config)

    # Save versioned docs
    output_path = Path(f"docs/API_REFERENCE_{version.upper()}.md")
    output_path.write_text(output)

    print(f"✓ Generated {version} docs: {output_path}")
```

**Use case:** Maintaining docs for multiple API versions simultaneously

### Pattern: Multi-Format Output

Generate HTML, Markdown, and RST from same schema:

**Templates:**
- `templates/api-reference.md.j2` - Markdown format
- `templates/api-reference.html.j2` - HTML format
- `templates/api-reference.rst.j2` - ReStructuredText format

**Content config with multiple patterns:**

```json
{
  "generation": {
    "patterns": [
      {
        "id": "markdown-output",
        "type": "jinja2",
        "template": "templates/api-reference.md.j2",
        "context": {"api": "data/openapi-spec.json"}
      },
      {
        "id": "html-output",
        "type": "jinja2",
        "template": "templates/api-reference.html.j2",
        "context": {"api": "data/openapi-spec.json"}
      },
      {
        "id": "rst-output",
        "type": "jinja2",
        "template": "templates/api-reference.rst.j2",
        "context": {"api": "data/openapi-spec.json"}
      }
    ]
  }
}
```

**Generate all formats:**

```python
from pathlib import Path

config = loader.load_content_config("api-docs-multiformat")

for pattern in config.generation.patterns:
    # Generate with specific pattern
    output = generator.generate(config, context={"pattern_id": pattern.id})

    # Determine extension from pattern ID
    ext = pattern.id.split("-")[0]  # e.g., "markdown" from "markdown-output"

    # Save
    output_path = Path(f"docs/API_REFERENCE.{ext}")
    output_path.write_text(output)

    print(f"✓ Generated {ext} format: {output_path}")
```

**Use case:** Publishing to multiple platforms (GitHub, ReadTheDocs, internal wiki)

### Pattern: Filtered Endpoint Documentation

Generate docs for specific endpoint groups:

**Template with filtering:**

```jinja2
# {{ api.info.title }} - {{ filter_tag | title }} Endpoints

{% for path, methods in api.paths.items() %}
{% for method, operation in methods.items() %}
{% if filter_tag in operation.get('tags', []) %}
### {{ method.upper() }} {{ path }}

{{ operation.summary }}

{{ operation.description }}

---

{% endif %}
{% endfor %}
{% endfor %}
```

**Generate filtered docs:**

```python
from chora_compose.generators.jinja2 import Jinja2Generator

generator = Jinja2Generator()

# Load OpenAPI spec
spec = json.loads(Path("data/openapi-spec.json").read_text())

# Generate docs for each tag
tags = ["users", "auth", "admin"]

for tag in tags:
    config = loader.load_content_config("api-docs-filtered")

    # Pass filter context
    context = {
        "api": spec,
        "filter_tag": tag
    }

    output = generator.generate(config, context=context)

    # Save tag-specific docs
    output_path = Path(f"docs/API_{tag.upper()}.md")
    output_path.write_text(output)

    print(f"✓ Generated {tag} docs: {output_path}")
```

**Use case:** Separate documentation for different user roles or microservices

### Pattern: OpenAPI + Examples Enrichment

Combine OpenAPI schema with external example files:

**Directory structure:**
```
data/
  openapi-spec.json
  examples/
    users-list.json
    users-create.json
    users-get.json
```

**Enhanced template:**

```jinja2
{% for path, methods in api.paths.items() %}
{% for method, operation in methods.items() %}
### {{ method.upper() }} {{ path }}

{{ operation.description }}

**Example Request:**

{% set example_id = operation.operationId %}
{% if examples[example_id] %}
```bash
curl -X {{ method.upper() }} "{{ base_url }}{{ path }}" \
  -H "Authorization: Bearer $TOKEN" \
  {% if method == 'post' or method == 'put' %}
  -H "Content-Type: application/json" \
  -d '{{ examples[example_id].request | tojson }}'
  {% endif %}
```

**Example Response:**

```json
{{ examples[example_id].response | tojson(indent=2) }}
```
{% endif %}

{% endfor %}
{% endfor %}
```

**Load examples and generate:**

```python
import json
from pathlib import Path

# Load OpenAPI spec
spec = json.loads(Path("data/openapi-spec.json").read_text())

# Load all examples
examples = {}
for example_file in Path("data/examples").glob("*.json"):
    example_id = example_file.stem  # e.g., "users-list"
    examples[example_id] = json.loads(example_file.read_text())

# Generate with enriched context
context = {
    "api": spec,
    "examples": examples,
    "base_url": "https://api.example.com/v1"
}

config = loader.load_content_config("api-docs-enriched")
output = generator.generate(config, context=context)

Path("docs/API_REFERENCE.md").write_text(output)
```

**Use case:** Living documentation with real tested examples

---

## Advanced Usage

### Custom Jinja2 Filters

Add custom filters for OpenAPI processing:

```python
from chora_compose.generators.jinja2 import Jinja2Generator

# Create generator with custom filters
def format_type(schema):
    """Format OpenAPI schema type as human-readable."""
    if schema.get("type") == "array":
        return f"Array<{format_type(schema.get('items', {}))}>"
    elif schema.get("type") == "object":
        return "Object"
    else:
        return schema.get("type", "any").title()

def http_status_text(code):
    """Convert status code to text."""
    status_map = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error"
    }
    return status_map.get(int(code), "Unknown")

# Register filters
generator = Jinja2Generator()
generator.env.filters['format_type'] = format_type
generator.env.filters['http_status_text'] = http_status_text

# Use in template
"""
Type: {{ param.schema | format_type }}
Status: {{ status_code }} {{ status_code | http_status_text }}
"""
```

### Validation Before Generation

Validate OpenAPI schema before generating docs:

```python
from pathlib import Path
import json
from jsonschema import validate, ValidationError

# OpenAPI 3.0 meta-schema
openapi_schema = json.loads(Path("schemas/openapi-3.0.json").read_text())

# Load user's API spec
spec_path = Path("data/openapi-spec.json")
spec = json.loads(spec_path.read_text())

# Validate
try:
    validate(instance=spec, schema=openapi_schema)
    print("✓ OpenAPI schema is valid")
except ValidationError as e:
    print(f"✗ Invalid OpenAPI schema: {e.message}")
    exit(1)

# Generate docs
config = loader.load_content_config("api-docs-from-openapi")
output = generator.generate(config)
```

### Incremental Updates

Only regenerate docs when OpenAPI spec changes:

```python
import hashlib
from pathlib import Path

def file_hash(path: Path) -> str:
    """Compute SHA256 hash of file."""
    return hashlib.sha256(path.read_text().encode()).hexdigest()

# Paths
spec_path = Path("data/openapi-spec.json")
output_path = Path("docs/API_REFERENCE.md")
hash_path = Path("docs/.api-spec-hash")

# Check if regeneration needed
current_hash = file_hash(spec_path)
previous_hash = hash_path.read_text() if hash_path.exists() else ""

if current_hash == previous_hash:
    print("✓ API spec unchanged, skipping generation")
else:
    print("⚠ API spec changed, regenerating docs...")

    # Generate
    config = loader.load_content_config("api-docs-from-openapi")
    output = generator.generate(config)
    output_path.write_text(output)

    # Save hash
    hash_path.write_text(current_hash)

    print(f"✓ Generated: {output_path}")
```

---

## Troubleshooting

**Problem:** `KeyError: 'paths'` when generating
**Solution:**
- Verify OpenAPI schema has `paths` key
- Check schema version (OpenAPI 3.x vs Swagger 2.x)
- Validate schema against OpenAPI meta-schema
- Ensure JSON is well-formed

**Problem:** Missing response examples in output
**Solution:**
- Check OpenAPI schema has `responses[status].content[type].example`
- Provide default examples in template: `{{ response.content['application/json'].example | default('{}') }}`
- Use external examples pattern shown above

**Problem:** Template renders `None` for optional fields
**Solution:**
- Use Jinja2 default filter: `{{ field | default('N/A') }}`
- Use conditional: `{% if field %}{{ field }}{% else %}N/A{% endif %}`
- Set defaults in context before generation

**Problem:** Table formatting breaks with special characters
**Solution:**
- Escape special markdown characters: `{{ description | replace('|', '\\|') }}`
- Use HTML entities for complex content
- Consider using different format (not tables) for complex data

**Problem:** Large schemas cause memory issues
**Solution:**
- Process endpoints incrementally (one tag at a time)
- Use streaming/chunked generation
- Split into multiple smaller output files
- Filter unnecessary schema fields before passing to template

**Problem:** Generated docs don't match actual API behavior
**Solution:**
- **Critical:** Keep OpenAPI schema in sync with code
- Use schema validation in tests
- Generate schema from code (e.g., FastAPI auto-generation)
- Set up CI/CD to validate schema matches implementation

---

## Best Practices

### 1. Keep OpenAPI Schema as Single Source of Truth

**Good:**
```python
# API implementation generates OpenAPI schema
# Docs generated from that schema
# Both always in sync
```

**Bad:**
```python
# Manually maintain OpenAPI schema separate from code
# Schema gets out of date
# Docs don't match reality
```

### 2. Version Your Templates

```
templates/
  api-reference/
    v1.j2  # For older projects
    v2.j2  # Current standard
    v3.j2  # Experimental new format
```

Link config to specific template version for stability.

### 3. Validate Generated Output

```python
# After generation, validate output
output = generator.generate(config)

# Check expected sections present
assert "## Endpoints" in output
assert "/users" in output
assert "Authentication" in output

# Check no template errors leaked through
assert "{{" not in output
assert "{%" not in output
```

### 4. Include Generation Metadata

Add metadata to generated docs:

```jinja2
---
title: {{ api.info.title }}
version: {{ api.info.version }}
generated: {{ now() }}
source: {{ source_file }}
generator: Chora Compose Jinja2Generator
---
```

This helps users know when docs were last updated.

---

## See Also

- [How to: Use Template Inheritance](use-template-inheritance.md) - Reusable template components
- [How to: Debug Jinja2 Template Errors](debug-jinja2-templates.md) - Fix template issues
- [Tutorial: Dynamic Content with Jinja2](../../tutorials/intermediate/01-dynamic-content-with-jinja2.md) - Learn Jinja2 basics
- [Jinja2Generator API Reference](../../reference/api/generators/jinja2.md) - Technical details
- [Why Jinja2 for Dynamic Generation](../../explanation/architecture/why-jinja2-for-dynamic-generation.md) - Design rationale
