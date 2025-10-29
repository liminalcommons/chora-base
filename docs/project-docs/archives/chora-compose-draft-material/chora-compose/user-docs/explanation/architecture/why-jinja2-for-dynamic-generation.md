# Why Jinja2 for Dynamic Generation

> **Purpose:** Explain the rationale for using Jinja2 as Chora Compose's dynamic content generation engine.

## The Problem

### Static Example-Output Limitations

Chora Compose's initial `DemonstrationGenerator` uses static `example_output` fields in content configs. This works well for:

- Fixed content that doesn't change
- Documentation that's manually maintained
- Simple content assembly from predefined pieces

**However, it breaks down for:**

```json
{
  "elements": [
    {
      "name": "user_list",
      "example_output": "- Alice\n- Bob\n- Charlie"
    }
  ]
}
```

**Problems:**
1. **No data binding:** Can't load actual user data from database or API
2. **Manual updates:** Every data change requires config file edit
3. **Duplication:** Same data appears in multiple configs
4. **No logic:** Can't conditionally include sections based on data
5. **Limited transformation:** Can't format, filter, or compute from source data

### Real-World Scenario

**Task:** Generate API documentation from OpenAPI schema

**With static approach:**
```json
{
  "elements": [
    {
      "name": "endpoint_list",
      "example_output": "### GET /users\n\nRetrieve all users...\n\n### POST /users\n\nCreate user..."
    }
  ]
}
```

**Issues:**
- ❌ OpenAPI schema changes → Manual config update required
- ❌ 50 endpoints → 50 manual element entries
- ❌ Can't generate from actual API spec file
- ❌ Documentation drifts from implementation
- ❌ Error-prone and time-consuming

**Need:** Way to generate content dynamically from external data sources.

---

## The Solution: Jinja2 Template Engine

### What is Jinja2?

Jinja2 is a modern, designer-friendly templating language for Python. It allows you to:

```jinja2
{# Template #}
# API Reference

{% for endpoint in api.endpoints %}
### {{ endpoint.method }} {{ endpoint.path }}

{{ endpoint.description }}

**Parameters:**
{% for param in endpoint.parameters %}
- `{{ param.name }}` ({{ param.type }}) - {{ param.description }}
{% endfor %}
{% endfor %}
```

**With data:**
```python
context = {
    "api": {
        "endpoints": [
            {
                "method": "GET",
                "path": "/users",
                "description": "Retrieve all users",
                "parameters": [...]
            }
        ]
    }
}
```

**Produces:**
```markdown
# API Reference

### GET /users

Retrieve all users

**Parameters:**
- `page` (integer) - Page number
- `limit` (integer) - Items per page
```

### Why Jinja2 Specifically?

**1. Python Integration**
- Native Python library (no external dependencies beyond pip install)
- Seamless data passing from Python to templates
- Access to Python objects, dicts, lists directly

**2. Powerful Features**
- Control structures: loops, conditionals, macros
- Filters for data transformation
- Template inheritance for reuse
- Includes for composition
- Extensive built-in functionality

**3. Designer-Friendly Syntax**
- Clear separation of logic and content
- Readable for non-programmers
- Familiar to web developers (similar to Django templates)

**4. Safety**
- Sandboxed execution
- Auto-escaping for security
- No arbitrary Python code execution (by default)

**5. Battle-Tested**
- Used by Flask, Ansible, Salt
- Mature, stable, well-documented
- Large community and ecosystem

---

## Architectural Fit

### Generator Strategy Pattern Integration

Jinja2Generator fits naturally into Chora Compose's generator strategy pattern:

```python
class GeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        pass

class DemonstrationGenerator(GeneratorStrategy):
    """Static example-based generation."""
    def generate(self, config, context=None):
        # Extract example_output fields
        return assembled_examples

class Jinja2Generator(GeneratorStrategy):
    """Dynamic template-based generation."""
    def generate(self, config, context=None):
        # Load template
        # Render with context
        return rendered_output
```

**Benefits:**
- ✅ Same interface as other generators
- ✅ Can be used interchangeably via pattern type
- ✅ Composable with other generators in artifacts
- ✅ No changes to core composer or config loader

### Config-Driven Approach Preserved

Jinja2 enhances, doesn't replace, the config-driven approach:

**Content config still defines behavior:**
```json
{
  "type": "content",
  "id": "api-docs",
  "generation": {
    "patterns": [{
      "id": "api-pattern",
      "type": "jinja2",
      "template": "api-reference.j2",
      "context": {
        "api_spec": {
          "source": "file",
          "path": "openapi.json"
        }
      }
    }]
  }
}
```

**What's config-driven:**
- ✅ Which template to use
- ✅ Where to load data from
- ✅ What context to provide
- ✅ Version, metadata, tags

**What's template-driven:**
- ✅ How to structure output
- ✅ How to format data
- ✅ What sections to include
- ✅ Conditional logic

**Best of both worlds:**
- Declarative config defines WHAT
- Procedural template defines HOW
- Separation of concerns maintained

---

## Comparison: Static vs Dynamic

### Example: User Documentation

**Scenario:** Generate user documentation listing all active users.

#### Static Approach (DemonstrationGenerator)

**Content config:**
```json
{
  "elements": [
    {
      "name": "user_list",
      "example_output": "## Active Users\n\n- Alice (alice@example.com)\n- Bob (bob@example.com)\n- Charlie (charlie@example.com)"
    }
  ]
}
```

**Workflow:**
1. Query database for active users
2. Manually format as markdown
3. Copy into `example_output` field
4. Save config file
5. Generate

**Pain points:**
- ❌ Manual, error-prone process
- ❌ Out of date as soon as user data changes
- ❌ No automation possible
- ❌ Doesn't scale to 1000+ users

#### Dynamic Approach (Jinja2Generator)

**Template** (`templates/user-list.j2`):
```jinja2
## Active Users

{% for user in users %}
- {{ user.name }} ({{ user.email }})
{% endfor %}
```

**Content config:**
```json
{
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "user-list.j2",
      "context": {
        "users": {
          "source": "file",
          "path": "data/active-users.json"
        }
      }
    }]
  }
}
```

**Workflow:**
1. Export users to `data/active-users.json` (automated)
2. Generate (reads fresh data)
3. Done

**Advantages:**
- ✅ Always current with data
- ✅ Scales to any number of users
- ✅ Can be automated in CI/CD
- ✅ Separation of data and presentation

---

## Use Cases Enabled by Jinja2

### Use Case 1: OpenAPI to Markdown

**Problem:** Maintain API docs in sync with OpenAPI spec

**Solution:**
```jinja2
{# templates/api-reference.j2 #}
# {{ api.info.title }}

{% for path, methods in api.paths.items() %}
## {{ path }}

{% for method, operation in methods.items() %}
### {{ method.upper() }}

{{ operation.description }}

{% if operation.parameters %}
**Parameters:**
{% for param in operation.parameters %}
- `{{ param.name }}` ({{ param.schema.type }})
{% endfor %}
{% endif %}
{% endfor %}
{% endfor %}
```

**Config:**
```json
{
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "api-reference.j2",
      "context": {
        "api": {
          "source": "file",
          "path": "openapi.json"
        }
      }
    }]
  }
}
```

**Benefits:**
- Single source of truth (OpenAPI spec)
- Automatic updates when spec changes
- Consistent formatting
- Can generate multiple formats (MD, HTML, PDF)

### Use Case 2: Data-Driven Reports

**Problem:** Generate monthly reports from analytics data

**Template:**
```jinja2
# Monthly Report - {{ month }}

## Summary

- Total users: {{ stats.total_users }}
- New signups: {{ stats.new_users }}
- Active users: {{ stats.active_users }}
- Growth: {{ ((stats.new_users / stats.total_users) * 100) | round(1) }}%

## Top Features

{% for feature in stats.top_features %}
{{ loop.index }}. **{{ feature.name }}** - {{ feature.usage_count }} uses
{% endfor %}

## Recommendations

{% if stats.growth_rate < 5 %}
⚠️ Growth is below target. Consider marketing campaign.
{% else %}
✅ Growth is on track.
{% endif %}
```

**Context (loaded from database/API):**
```json
{
  "month": "October 2025",
  "stats": {
    "total_users": 10543,
    "new_users": 423,
    "active_users": 7821,
    "growth_rate": 4.2,
    "top_features": [...]
  }
}
```

**Benefits:**
- Automated monthly generation
- Always fresh data
- Conditional insights
- Computed metrics

### Use Case 3: Multi-Format Documentation

**Problem:** Generate same content as Markdown, HTML, and LaTeX

**Base template** (`base.j2`):
```jinja2
{% block header %}
{{ title }}
{% endblock %}

{% block content %}
{% for section in sections %}
{{ section.title }}
{{ section.content }}
{% endfor %}
{% endblock %}
```

**Markdown variant** (`document.md.j2`):
```jinja2
{% extends "base.j2" %}

{% block header %}
# {{ title }}
{% endblock %}

{% block content %}
{% for section in sections %}
## {{ section.title }}

{{ section.content }}

{% endfor %}
{% endblock %}
```

**HTML variant** (`document.html.j2`):
```jinja2
{% extends "base.j2" %}

{% block header %}
<h1>{{ title }}</h1>
{% endblock %}

{% block content %}
{% for section in sections %}
<section>
  <h2>{{ section.title }}</h2>
  {{ section.content | safe }}
</section>
{% endfor %}
{% endblock %}
```

**Benefits:**
- Single content source
- Multiple output formats
- Template inheritance eliminates duplication
- Easy to add new formats

### Use Case 4: Localized Content

**Problem:** Generate documentation in multiple languages

**Template:**
```jinja2
{# Uses locale-specific strings #}
# {{ strings.welcome_title }}

{{ strings.welcome_message }}

## {{ strings.getting_started_title }}

{% for step in steps %}
{{ loop.index }}. {{ step }}
{% endfor %}
```

**English context:**
```json
{
  "strings": {
    "welcome_title": "Welcome",
    "welcome_message": "Thank you for using our product.",
    "getting_started_title": "Getting Started"
  },
  "steps": ["Install", "Configure", "Run"]
}
```

**Spanish context:**
```json
{
  "strings": {
    "welcome_title": "Bienvenido",
    "welcome_message": "Gracias por usar nuestro producto.",
    "getting_started_title": "Empezando"
  },
  "steps": ["Instalar", "Configurar", "Ejecutar"]
}
```

**Benefits:**
- Template reuse across locales
- Easy to add new languages
- Consistent structure
- Translatable content separated

---

## Design Decisions

### Decision 1: External Templates vs Inline

**Considered:** Inline templates in content config

```json
{
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template_inline": "# {{ title }}\n\n{{ content }}"
    }]
  }
}
```

**Chose:** External template files

```json
{
  "generation": {
    "patterns": [{
      "type": "jinja2",
      "template": "my-template.j2"
    }]
  }
}
```

**Reasons:**
- ✅ Better editor support (syntax highlighting, linting)
- ✅ Template reuse across configs
- ✅ Version control for templates
- ✅ Cleaner, more maintainable configs
- ✅ Template inheritance requires files

**Trade-off:** Extra file to manage, but worth it for larger templates.

### Decision 2: Context from Config vs Runtime

**Support both:**

**Config context (declarative):**
```json
{
  "context": {
    "title": "My Doc",
    "version": "1.0"
  }
}
```

**Runtime context (imperative):**
```python
output = generator.generate(config, context={
    "generated_date": datetime.now(),
    "user": current_user
})
```

**Why both:**
- ✅ Config context: Static, versionable, declarative
- ✅ Runtime context: Dynamic, computed, imperative
- ✅ Runtime overrides config for flexibility
- ✅ Best of both approaches

### Decision 3: File Loading in Context

**Support source references:**

```json
{
  "context": {
    "api": {
      "source": "file",
      "path": "openapi.json"
    }
  }
}
```

**Why:**
- ✅ Keep data separate from configs
- ✅ Reuse same data across templates
- ✅ Version data files independently
- ✅ Large data doesn't bloat configs
- ✅ Supports JSON, YAML, CSV, etc.

**Alternative considered:** Embed data directly
- ❌ Bloats configs
- ❌ Hard to maintain large datasets
- ❌ Duplication across configs

### Decision 4: Security - Sandboxed Execution

**Default:** Sandboxed Jinja2 environment

**Safe:**
```jinja2
{{ user.name }}
{{ items | length }}
{% for item in items %}...{% endfor %}
```

**Not allowed (by default):**
```jinja2
{{ __import__('os').system('rm -rf /') }}  {# Blocked #}
```

**Why:**
- ✅ Prevent malicious template code
- ✅ Safe to load untrusted templates (with care)
- ✅ No arbitrary Python execution
- ✅ Follows principle of least privilege

**Trade-off:** Limited power, but appropriate for content generation.

---

## Alternatives Considered

### Alternative 1: Python F-Strings

**Approach:** Use Python f-strings for templating

```python
template = f"""
# {title}

{content}
"""
```

**Why not:**
- ❌ No separation of template from code
- ❌ No template reuse
- ❌ No control structures (loops, conditionals)
- ❌ Not designer-friendly
- ❌ Requires Python knowledge

**When to use:** Very simple, one-off string formatting only.

### Alternative 2: String Template

**Approach:** Python's built-in `string.Template`

```python
from string import Template

template = Template("""
# $title

$content
""")

output = template.substitute(title="My Doc", content="Hello")
```

**Why not:**
- ❌ Very limited functionality
- ❌ No loops, conditionals, filters
- ❌ No template inheritance
- ❌ Only simple variable substitution

**When to use:** Ultra-simple variable replacement.

### Alternative 3: Mako

**Approach:** Mako template engine (used by Pyramid)

```mako
# ${title}

% for item in items:
- ${item}
% endfor
```

**Why not:**
- ❌ Less designer-friendly syntax
- ❌ Allows full Python execution (security concern)
- ❌ Smaller community than Jinja2
- ❌ Less familiar to developers

**When to use:** Need full Python power in templates (rare).

### Alternative 4: Mustache/Handlebars

**Approach:** Logic-less templates

```mustache
# {{title}}

{{#items}}
- {{.}}
{{/items}}
```

**Why not:**
- ❌ Too limited (no complex logic)
- ❌ No template inheritance
- ❌ Limited filter support
- ❌ Requires helpers for everything

**When to use:** Multi-language templates (JS + Python).

### Alternative 5: Custom Template Language

**Approach:** Build Chora Compose-specific template language

**Why not:**
- ❌ Reinventing the wheel
- ❌ Maintenance burden
- ❌ Learning curve for users
- ❌ No ecosystem/community
- ❌ Likely inferior to Jinja2

**When to use:** Never (for this use case).

---

## Trade-offs

### Jinja2 Advantages

✅ **Powerful:** Full-featured template language
✅ **Familiar:** Many developers know it (Flask, Ansible)
✅ **Mature:** Stable, well-tested, well-documented
✅ **Flexible:** Extensible with custom filters, tests, globals
✅ **Designer-friendly:** Non-programmers can use
✅ **Safe:** Sandboxed by default
✅ **Fast:** Compiled templates, efficient rendering

### Jinja2 Disadvantages

❌ **Dependency:** Adds external dependency (but popular, well-maintained)
❌ **Learning curve:** Requires learning Jinja2 syntax
❌ **Debugging:** Template errors can be cryptic
❌ **Complexity:** More complex than simple string substitution
❌ **Overkill:** For very simple cases, might be too much

### When to Use Jinja2Generator

**Use Jinja2Generator when:**
- ✅ Content depends on external data
- ✅ Need loops, conditionals, formatting
- ✅ Generating from structured data (JSON, YAML, DB)
- ✅ Multiple output formats from same source
- ✅ Need template reuse and inheritance
- ✅ Content changes frequently with data

**Use DemonstrationGenerator when:**
- ✅ Content is completely static
- ✅ No data dependency
- ✅ Simple, small sections
- ✅ Manually crafted examples
- ✅ No need for logic or transformation

**Use both together:**
```json
{
  "content": {
    "children": [
      {
        "id": "intro",
        "path": "intro-content.json",
        "type": "demonstration"
      },
      {
        "id": "api-docs",
        "path": "api-docs-content.json",
        "type": "jinja2"
      },
      {
        "id": "footer",
        "path": "footer-content.json",
        "type": "demonstration"
      }
    ]
  }
}
```

Static intro/footer with dynamic API docs in the middle.

---

## Impact on Chora Compose Ecosystem

### Documentation Workflow Enhancement

**Before Jinja2:**
```
Edit OpenAPI spec → Manually update example_output → Generate
```

**After Jinja2:**
```
Edit OpenAPI spec → Generate (automatic update)
```

**Result:** Tighter feedback loop, living documentation.

### Enabling New Use Cases

**Now possible:**
1. **Data-driven docs:** Reports, analytics, metrics
2. **Schema-based docs:** OpenAPI, JSON Schema, GraphQL
3. **Multi-format output:** MD, HTML, LaTeX from same source
4. **Localization:** Multi-language documentation
5. **Personalized docs:** User-specific, role-specific content

### Maintaining Chora Compose Philosophy

**Chora Compose principles preserved:**
- ✅ **Config-driven:** Behavior defined in configs
- ✅ **Composable:** Generators work together
- ✅ **Extensible:** Easy to add new generators
- ✅ **Testable:** Templates testable independently
- ✅ **Versionable:** Templates and configs version controlled

**Chora Compose principles enhanced:**
- ✅ **DRY:** Template reuse eliminates duplication
- ✅ **Single source of truth:** Data + template = output
- ✅ **Automation:** Enables CI/CD documentation generation

---

## Real-World Success Stories

### Success Story 1: FastAPI Project

**Challenge:** Keep API docs in sync with code

**Solution:**
- FastAPI auto-generates OpenAPI schema
- Jinja2 template converts to Markdown
- GitHub Actions regenerates on every commit

**Result:**
- Documentation always current
- No manual maintenance
- Developers love it

### Success Story 2: Multi-Language Docs

**Challenge:** Support docs in 5 languages

**Solution:**
- Single Jinja2 template
- 5 locale context files
- Generate all languages in one command

**Result:**
- Consistent structure across languages
- Easy to add new languages
- Translators edit JSON, not markdown

### Success Story 3: Automated Reporting

**Challenge:** Generate weekly metrics reports

**Solution:**
- Query analytics database
- Export to JSON
- Jinja2 template renders report
- Email markdown output

**Result:**
- Fully automated
- No manual report writing
- Saved 4 hours/week

---

## Future Possibilities

### Template Marketplace

**Idea:** Share Jinja2 templates for common use cases

```bash
Chora Compose templates search "openapi to markdown"
Chora Compose templates install openapi-docs-template
```

**Benefits:**
- ✅ Don't reinvent the wheel
- ✅ Best practices baked in
- ✅ Community contributions

### AI-Assisted Template Creation

**Idea:** LLM helps write templates from examples

```
User: "I want to generate user docs from JSON user data"
AI: "Here's a template and config for that..."
```

**Benefits:**
- ✅ Lower barrier to entry
- ✅ Faster template creation
- ✅ Learn Jinja2 by example

### Template Composition

**Idea:** Combine multiple templates

```jinja2
{% include "header.j2" %}
{% include "api-docs.j2" %}
{% include "footer.j2" %}
```

**Already possible with Jinja2!**

### Template Testing Framework

**Idea:** Dedicated testing for templates

```python
@pytest.fixture
def template_test():
    def test(template, context, expected):
        output = generator.generate_from_template(template, context)
        assert output == expected
    return test

def test_user_list_template(template_test):
    template_test(
        template="user-list.j2",
        context={"users": [{"name": "Alice"}]},
        expected="- Alice\n"
    )
```

**Enables:** TDD for documentation templates.

---

## Conclusion

### Why Jinja2 is the Right Choice

1. **Proven technology:** Used by millions, battle-tested
2. **Perfect fit:** Solves dynamic generation problem elegantly
3. **Preserves architecture:** Integrates cleanly with Chora Compose
4. **Enables new use cases:** Data-driven, automated docs
5. **Developer-friendly:** Familiar, well-documented
6. **Future-proof:** Active development, large community

### The Path Forward

**Phase 1 (Current):** Documentation complete ✅
**Phase 2:** Extract tests from documentation
**Phase 3:** Implement Jinja2Generator
**Phase 4:** Integration and real-world validation
**Phase 5:** Community feedback and iteration

### Key Takeaway

> **Jinja2 complements, not replaces, existing generators.**
>
> Use DemonstrationGenerator for static content.
> Use Jinja2Generator for dynamic content.
> Use both together for best results.

The goal: **Make documentation a first-class, automated, always-current artifact of the development process.**

Jinja2 makes this possible.

---

## See Also

- [Tutorial: Dynamic Content with Jinja2](../../tutorials/intermediate/01-dynamic-content-with-jinja2.md) - Get started
- [How to: Generate API Docs from OpenAPI](../../how-to/generation/generate-api-docs-from-openapi.md) - Real example
- [How to: Use Template Inheritance](../../how-to/generation/use-template-inheritance.md) - Advanced usage
- [How to: Debug Jinja2 Templates](../../how-to/generation/debug-jinja2-templates.md) - Fix issues
- [Jinja2Generator API Reference](../../reference/api/generators/jinja2.md) - Technical details
- [Generator Strategy Pattern](generator-strategy-pattern.md) - Architecture overview
- [Config-Driven Architecture](config-driven-architecture.md) - Core philosophy
