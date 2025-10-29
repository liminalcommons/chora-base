# MCP Resource Providers Guide

This guide explains how to use Chora Compose's MCP resource providers to access configuration data, schemas, generated content, and generator information through Claude Desktop.

---

## Table of Contents

1. [Overview](#overview)
2. [config:// - Configuration Access](#config-configuration-access)
3. [schema:// - Schema Definitions](#schema-schema-definitions)
4. [content://generated/ - Generated Content](#contentgenerated-generated-content)
5. [generator:// - Generator Registry](#generator-generator-registry)
6. [Common Workflows](#common-workflows)
7. [Performance Tips](#performance-tips)

---

## Overview

### What Are Resource Providers?

Resource providers give Claude read-only access to your Chora Compose data through URI-based patterns. Think of them as browsable directories that Claude can explore to understand your system.

**Key characteristics:**

- **Read-only** - Resources provide information, tools perform actions
- **URI-based** - Access via standardized patterns like `config://content/my-config`
- **Contextual** - Help Claude understand what's available and how to use it

**Available providers:**

- `config://` - Access content and artifact configurations
- `schema://` - View JSON schemas for configurations
- `content://generated/` - Browse generated content and versions
- `generator://` - Discover available generators and their capabilities

### When to Use Resources vs Tools

**Use resources when:**
- Discovering what's available
- Reading existing data
- Understanding system configuration
- Reviewing generated content

**Use tools when:**
- Generating new content
- Assembling artifacts
- Modifying configurations
- Executing workflows

**Example conversation:**

```
You: "What content types can I generate?"

Claude reads: config://content/
→ Sees: user-guide, api-docs, faq, tutorial...

Claude: "You have 8 content types configured: user-guide, api-docs, faq..."

You: "Generate the user-guide"

Claude calls: generate_content(content_config_id="user-guide")
→ Creates the content
```

---

## config:// - Configuration Access

### Overview

The **config://** provider lets Claude read your content and artifact configurations. This helps Claude understand what can be generated and how things are configured.

**Use cases:**
- Discover available content and artifact configurations
- Understand generator requirements before generation
- Browse your content catalog
- Check configuration details

### URI Patterns

#### List all content configurations

```
config://content/
```

Returns a list of all content configurations with metadata.

**Ask Claude:**
```
Show me all available content configurations
```

**What Claude sees:**
```json
{
  "total": 8,
  "content": [
    {
      "id": "user-guide",
      "title": "User Guide",
      "generator_type": "jinja2",
      "stage": "active"
    },
    {
      "id": "api-docs",
      "title": "API Documentation",
      "generator_type": "jinja2",
      "stage": "active"
    }
  ]
}
```

#### Get specific content configuration

```
config://content/{id}
```

Returns complete configuration for a specific content ID.

**Ask Claude:**
```
Show me the configuration for user-guide
```

**What Claude sees:**
```json
{
  "id": "user-guide",
  "title": "User Guide",
  "generator": {
    "type": "jinja2",
    "template": "templates/user-guide.md.j2"
  },
  "output": {
    "format": "markdown",
    "filename": "user-guide.md"
  },
  "metadata": {
    "type": "documentation",
    "description": "Complete user guide for chora-compose"
  }
}
```

#### List all artifact configurations

```
config://artifact/
```

Returns a list of all artifact configurations with metadata.

**Ask Claude:**
```
What artifacts can I assemble?
```

#### Get specific artifact configuration

```
config://artifact/{id}
```

Returns complete configuration for a specific artifact ID.

**Ask Claude:**
```
Show me what's in the user-docs artifact
```

### Practical Examples

#### Example 1: Discover and generate content

```
You: "What documentation can I generate?"

Claude reads: config://content/
→ Filters by type: "documentation"

Claude: "You have 5 documentation content types:
  - user-guide (User Guide)
  - api-docs (API Documentation)
  - faq (Frequently Asked Questions)
  - tutorial (Getting Started Tutorial)
  - changelog (Change Log)

Which would you like to generate?"

You: "Generate the user-guide"

Claude calls: generate_content(content_config_id="user-guide")
```

#### Example 2: Understand artifact dependencies

```
You: "Assemble the user-docs artifact"

Claude reads: config://artifact/user-docs
→ Sees required content: user-guide, faq

Claude: "The user-docs artifact needs two content pieces:
  - user-guide (required) ✓ generated
  - faq (optional) ✗ not generated yet

I'll generate the faq first, then assemble."

Claude calls:
  1. generate_content(content_config_id="faq")
  2. assemble_artifact(artifact_config_id="user-docs")
```

#### Example 3: Configuration validation

```
You: "Why is my-content failing to generate?"

Claude reads: config://content/my-content
→ Inspects configuration

Claude reads: schema://content
→ Checks required fields

Claude: "The configuration is missing the required 'output.format' field.
According to the schema, output.format must be one of: markdown, json, text, html.

Would you like me to suggest a fix?"
```

---

## schema:// - Schema Definitions

### Overview

The **schema://** provider exposes JSON Schema definitions for configurations. This helps Claude understand what fields are required, what values are valid, and how to create correct configurations.

**Use cases:**
- Understand configuration requirements
- Validate user input
- Generate configuration templates
- Provide field documentation

### URI Patterns

#### Get content schema

```
schema://content
```

Returns the complete JSON Schema for content configurations.

**Ask Claude:**
```
What fields are required in a content configuration?
```

**What Claude sees:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Content Configuration Schema",
  "type": "object",
  "required": ["id", "generator", "output", "metadata"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$"
    },
    "generator": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": {
          "enum": ["jinja2", "template_fill", "demonstration"]
        }
      }
    }
  }
}
```

#### Get artifact schema

```
schema://artifact
```

Returns the complete JSON Schema for artifact configurations.

### Practical Examples

#### Example 1: Create a new configuration

```
You: "Create a new content config for release notes"

Claude reads: schema://content
→ Understands required fields

Claude: "I'll create a release-notes configuration following the schema.
All required fields will be included:
  - id: release-notes
  - generator: jinja2
  - output: markdown format
  - metadata: documentation type

Here's the template: ..."
```

#### Example 2: Validate existing configuration

```
You: "Why is my config invalid?"

Claude reads: config://content/my-config
→ Gets current configuration

Claude reads: schema://content
→ Gets validation rules

Claude: "I found 3 schema validation errors:
  1. Missing required 'output.format' field
  2. Invalid generator.type 'custom' (must be: jinja2, template_fill, or demonstration)
  3. metadata.tags should be an array, not a string

Here's the corrected configuration: ..."
```

#### Example 3: Field documentation

```
You: "What does retrieval_strategy mean in artifact configs?"

Claude reads: schema://artifact
→ Finds field definition

Claude: "retrieval_strategy determines which version of content to use:
  - 'latest' (default): Always use the most recent version
  - 'specific_version': Use a pinned version

Unless you need version pinning, 'latest' is recommended."
```

---

## content://generated/ - Generated Content

### Overview

The **content://generated/** provider exposes generated content from ephemeral storage. This allows Claude to review generated content, compare versions, and understand content history.

**Use cases:**
- Review generated content before assembly
- Compare different versions
- Debug generation issues
- Track content evolution

### URI Patterns

#### Get latest generated content

```
content://generated/{id}
```

Returns the most recently generated version of content.

**Ask Claude:**
```
Show me the latest user-guide content
```

**What Claude sees:**
```markdown
# User Guide

## Getting Started

Welcome to chora-compose...

(metadata: generated 2 hours ago, 4.5 KB, jinja2)
```

#### List content versions

```
content://generated/{id}/versions
```

Returns a list of all available versions with timestamps.

**Ask Claude:**
```
Show me the version history for api-docs
```

**What Claude sees:**
```json
{
  "content_id": "api-docs",
  "total_versions": 5,
  "versions": [
    {
      "version": "20251014_103000",
      "timestamp": "2025-10-14T10:30:00Z",
      "size_bytes": 4567,
      "is_latest": true
    },
    {
      "version": "20251014_093000",
      "timestamp": "2025-10-14T09:30:00Z",
      "size_bytes": 4321,
      "is_latest": false
    }
  ]
}
```

#### Get specific version

```
content://generated/{id}/v/{version}
```

Returns a specific historical version.

**Ask Claude:**
```
Show me the api-docs from yesterday afternoon
```

### Practical Examples

#### Example 1: Review before assembly

```
You: "Show me the user-guide before I assemble it"

Claude reads: content://generated/user-guide
→ Gets latest content

Claude: "Here's the latest user-guide (generated 2 hours ago):

# User Guide

## Getting Started
...

(4.5 KB, jinja2 generator)

Would you like me to assemble the artifact now?"

You: "Yes"

Claude calls: assemble_artifact(artifact_config_id="user-docs")
```

#### Example 2: Compare versions

```
You: "What changed in the latest api-docs?"

Claude reads: content://generated/api-docs/versions
→ Gets version list

Claude reads: content://generated/api-docs (latest)
Claude reads: content://generated/api-docs/v/20251014_083000 (previous)
→ Compares versions

Claude: "Changes in latest api-docs (1.5 hours ago):

Added:
  - New endpoint: POST /api/content/batch
  - New parameter: force on regenerate

Modified:
  - Updated GET /api/generators description

(+142 lines, -28 lines, +2.3 KB)"
```

#### Example 3: Debug empty content

```
You: "My tutorial content is empty. Why?"

Claude reads: content://generated/tutorial
→ Sees 0 bytes

Claude reads: config://content/tutorial
→ Checks configuration

Claude: "The tutorial content exists but is empty (0 bytes).

Issue: The template file 'templates/tutorial.md.j2' doesn't exist.

Solutions:
  1. Create the template file
  2. Or update the config to point to an existing template

Would you like me to help create a template?"
```

#### Example 4: Content evolution analysis

```
You: "How has the user-guide evolved?"

Claude reads: content://generated/user-guide/versions
→ Analyzes history

Claude: "user-guide evolution (8 versions, 3 weeks):

Growth: 3.2 KB → 4.5 KB (+40%)
Frequency: 2-3 updates per week

Major changes:
  - Week 1: Basic structure
  - Week 2: Added Advanced Features
  - Week 3: Added Troubleshooting, expanded examples

The guide has matured significantly!"
```

---

## generator:// - Generator Registry

### Overview

The **generator://** provider exposes the generator registry, helping Claude understand what generators are available and how to use them.

**Use cases:**
- Discover available generators
- Understand generator capabilities
- Match user needs to appropriate generators
- Get configuration examples

### URI Patterns

#### List all generators

```
generator://list
```

Returns all registered generators with metadata.

**Ask Claude:**
```
What generators are available?
```

**What Claude sees:**
```json
{
  "total": 5,
  "generators": [
    {
      "type": "jinja2",
      "category": "builtin",
      "description": "Full Jinja2 templating engine",
      "capabilities": ["templates", "logic", "filters"],
      "supported_formats": ["markdown", "text", "html", "json"]
    },
    {
      "type": "template_fill",
      "category": "builtin",
      "description": "Simple variable substitution",
      "capabilities": ["simple_substitution"],
      "supported_formats": ["markdown", "text"]
    }
  ]
}
```

#### Get specific generator details

```
generator://{type}
```

Returns detailed information about a specific generator.

**Ask Claude:**
```
Tell me about the jinja2 generator
```

**What Claude sees:**
```json
{
  "type": "jinja2",
  "description": "Full Jinja2 template engine with loops, conditionals, filters",
  "capabilities": ["templates", "logic", "filters", "inheritance"],
  "required_config": ["template"],
  "optional_config": ["context_defaults", "extensions"],
  "supported_formats": ["markdown", "text", "html", "json"],
  "usage_examples": [...]
}
```

#### List built-in generators

```
generator://builtin
```

Returns only built-in generators (excludes plugins).

#### List plugin generators

```
generator://plugins
```

Returns only user-installed plugin generators.

### Practical Examples

#### Example 1: Find the right generator

```
You: "I want to create markdown documentation"

Claude reads: generator://list
→ Filters by supported_formats: "markdown"

Claude: "For markdown documentation, you have 3 options:

1. jinja2 (recommended): Full template power
   - Best for: Complex docs with dynamic content
   - Supports: loops, conditionals, filters

2. template_fill: Simple substitution
   - Best for: Simple docs with static structure
   - Fast and straightforward

3. demonstration: Example-based
   - Best for: Quick prototypes

Which fits your needs?"

You: "Complex user guide"

Claude: "Perfect! jinja2 is the right choice."
```

#### Example 2: Check generator capabilities

```
You: "I need a generator that supports template inheritance"

Claude reads: generator://list
→ Filters by capabilities: "inheritance"

Claude: "jinja2 supports template inheritance!

You can create a base template and extend it:

Base template (base.md.j2):
  # {{title}}
  {% block content %}{% endblock %}

Extended template (guide.md.j2):
  {% extends 'base.md.j2' %}
  {% block content %}
  ## Getting Started
  ...
  {% endblock %}

This is great for maintaining consistent structure!"
```

#### Example 3: Configuration help

```
You: "How do I configure the jinja2 generator?"

Claude reads: generator://jinja2
→ Gets configuration schema

Claude: "To configure jinja2:

Required:
  - template: Path to your Jinja2 template file

Optional:
  - context_defaults: Default variables
  - extensions: Jinja2 extensions
  - filters: Custom filters

Minimal example:
{
  'generator': {
    'type': 'jinja2',
    'template': 'templates/my-doc.md.j2'
  }
}

Would you like me to create a config?"
```

---

## Common Workflows

### Workflow 1: Create New Content

```
1. You: "Create markdown documentation for tutorials"

2. Claude reads: generator://list
   → Recommends jinja2 for markdown

3. Claude reads: schema://content
   → Understands required fields

4. Claude creates configuration template
   → Shows you the config

5. You: "Looks good, save it"

6. You manually save the config file

7. Claude calls: generate_content(content_config_id="tutorial")

8. Claude reads: content://generated/tutorial
   → Shows you the result
```

### Workflow 2: Assemble Artifact

```
1. You: "Assemble user-docs"

2. Claude reads: config://artifact/user-docs
   → Checks dependencies

3. Claude reads: content://generated/user-guide
   Claude reads: content://generated/faq
   → Verifies content exists

4. Claude: "All content ready:
   - user-guide ✓
   - faq ✓"

5. Claude calls: assemble_artifact(artifact_config_id="user-docs")
```

### Workflow 3: Debug Configuration

```
1. You: "Generation is failing for my-content"

2. Claude reads: config://content/my-content
   → Inspects configuration

3. Claude reads: schema://content
   → Validates against schema

4. Claude reads: generator://jinja2
   → Checks generator requirements

5. Claude: "Found the issue:
   - Missing required field: output.format
   - Should be one of: markdown, json, text, html

   Here's the fix: ..."
```

### Workflow 4: Version Comparison

```
1. You: "What changed in api-docs?"

2. Claude reads: content://generated/api-docs/versions
   → Gets version history

3. Claude reads latest and previous versions
   → Compares content

4. Claude: "Changes in last update:
   - Added 2 new endpoints
   - Updated 3 descriptions
   - +142 lines, -28 lines"
```

---

## Performance Tips

### Response Times

Typical response times for resource operations:

| Provider | Operation | Time | Notes |
|----------|-----------|------|-------|
| config:// | Single config | 10-30ms | Fast filesystem read |
| config:// | List all | 50-150ms | Directory scan |
| schema:// | Get schema | 5-20ms | Small files, very cacheable |
| content:// | Latest | 10-50ms | Single file read |
| content:// | Versions | 20-100ms | Directory scan |
| generator:// | List | 1-5ms | In-memory, very fast |
| generator:// | Details | <1ms | Dictionary lookup |

### Optimization Tips

**1. Use specific URIs when possible**

✅ Good:
```
generator://jinja2
```

❌ Slower:
```
generator://list (then filter client-side)
```

**2. Use list operations for bulk queries**

✅ Good:
```
config://content/ (gets all at once)
```

❌ Slower:
```
Multiple config://content/{id} calls
```

**3. Understand caching behavior**

- `schema://` - Schemas rarely change, cache aggressively
- `generator://` - Registry is static, cache for session
- `config://` - Configs change occasionally, cache briefly
- `content://generated/{id}` - Content changes frequently, don't cache

**4. Avoid unnecessary operations**

- Only check versions when you need history
- Use `content://generated/{id}` for latest (faster than versions + filter)
- List operations are more expensive than direct reads

---

## Error Handling

### Common Errors

**Resource not found:**
```
Error: Content config 'nonexistent' not found
Hint: Use config://content/ to list available configs
```

**Invalid URI pattern:**
```
Error: Invalid config:// URI pattern
Valid patterns:
  - config://content/{id}
  - config://artifact/{id}
  - config://content/
  - config://artifact/
```

**Content not generated:**
```
Error: Content 'tutorial' has not been generated yet
Suggestion: Use generate_content tool first
```

### Recovery Steps

1. **Use list operations** to discover what's available
2. **Check spelling** of resource IDs
3. **Verify resources exist** before accessing them
4. **Read error hints** - they usually tell you what to do

---

## Summary

Resource providers give Claude the ability to explore your Chora Compose system:

- **config://** - Browse configurations and understand what can be generated
- **schema://** - Validate and create correct configurations
- **content://generated/** - Review generated content and track history
- **generator://** - Discover generators and their capabilities

Combined with tools, resource providers enable Claude to intelligently assist with content generation, artifact assembly, and system configuration.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-15
**Feedback:** [GitHub Issues](https://github.com/liminalcommons/chora-compose/issues)
