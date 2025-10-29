# How-To: Generate README Using Chora Compose

**Skill Level:** Intermediate
**Time:** 5 minutes
**Prerequisites:**
- Chora Compose installed
- Understanding of Jinja2 templates
- Understanding of JSON structure
- Familiarity with markdown

## What This Solves

Manually maintaining a README.md file is challenging:

1. **Keeping content in sync** - Features change but README lags behind
2. **Version inconsistencies** - Forgetting to update version numbers
3. **Broken links** - Documentation moves but links don't update
4. **Inconsistent formatting** - Manual editing leads to style drift
5. **Duplication** - Same information repeated in multiple places
6. **Time-consuming updates** - Every small change requires manual editing

By using Chora Compose's Jinja2Generator to generate README from structured data, we can:

1. **Single source of truth**: All content in one structured JSON file
2. **Easy updates**: Change the data file and regenerate
3. **Consistent formatting**: Template ensures uniformity across the entire README
4. **Data reuse**: Same data can generate website content, marketing materials, slide decks
5. **Version control**: Track content changes separately from presentation structure
6. **Automated accuracy**: Links, counts, and references stay in sync
7. **Template flexibility**: Change presentation without touching content

This is a "dogfooding" example - using Chora Compose to manage Chora Compose's own documentation, demonstrating the framework's capabilities in a real-world scenario.

## Files Overview

The README generation system consists of:

```
configs/
├── content/readme/
│   ├── readme-content.json        # Content config (links data + template)
│   └── readme-data.json           # Structured README data (409 lines)
└── templates/readme/
    └── readme.j2                   # Jinja2 template (301 lines)

scripts/
└── generate_readme.py             # Generation script (55 lines)

README-generated.md                # Generated output (for comparison)
```

**File purposes:**

- **`readme-data.json`**: All README content in structured JSON format
  - Project metadata (name, version, tagline)
  - Feature list with descriptions
  - Installation instructions
  - Documentation structure
  - Development tools
  - Examples and roadmap

- **`readme.j2`**: Jinja2 template defining presentation
  - Section ordering and headers
  - Formatting rules (badges, tables, code blocks)
  - Conditional logic for different content types

- **`readme-content.json`**: Chora Compose configuration
  - References the data file
  - Specifies the Jinja2 template
  - Defines generation pattern

- **`generate_readme.py`**: Automation script
  - Loads config
  - Runs Jinja2Generator
  - Writes output file

## Step 1: Understanding the Data Structure

The `readme-data.json` file contains all README content in a structured format:

```json
{
  "project": {
    "name": "Chora Compose",
    "short_name": "Chora Compose",
    "version": "0.5.0",           // Update version here
    "tagline": "Configuration-driven framework...",
    "repository": "https://github.com/...",
    "badges": [                    // Shields.io badges
      {
        "label": "Python 3.12+",
        "message": "3.12+",
        "color": "blue",
        "url": "https://www.python.org/downloads/"
      }
    ],
    "links": {                     // Main navigation links
      "documentation": "docs/",
      "changelog": "CHANGELOG.md",
      "examples": "examples/"
    }
  },
  "features": [                    // Key feature highlights
    {
      "name": "Configuration-Driven",
      "description": "Define workflows using JSON Schema-validated configs"
    },
    {
      "name": "Multiple Generators",
      "description": "Template-based (Jinja2), demonstration-based, and more"
    }
  ],
  "quick_start": {                 // Installation section
    "prerequisites": [
      "Python 3.12 or higher",
      "[Poetry](https://python-poetry.org/) for dependency management"
    ],
    "installation_steps": [
      {
        "title": "Clone the repository",
        "command": "git clone https://github.com/..."
      },
      {
        "title": "Install dependencies",
        "command": "poetry install"
      }
    ],
    "first_example": {
      "title": "Your First Generation",
      "description": "Try the included OpenAPI → API Docs example",
      "command": "cd examples/jinja2-api-docs\npoetry run python generate.py"
    }
  },
  "generators": [                  // Available generator types
    {
      "name": "Jinja2",
      "description": "Template-based generation...",
      "status": "✅ v0.4.0"
    }
  ],
  "documentation": {               // Documentation structure
    "framework": "Diátaxis",
    "total_count": 33,
    "categories": {
      "tutorials": {
        "title": "📘 Tutorials",
        "items": [
          {"title": "Your First Config", "path": "docs/..."}
        ]
      }
    }
  },
  "development": {                 // Development tools
    "tools": [
      {
        "name": "ruff",
        "purpose": "Linting and formatting",
        "commands": [
          {"action": "Check code", "command": "poetry run ruff check ."}
        ]
      }
    ]
  },
  "roadmap": {                     // Version roadmap
    "versions": [
      {
        "version": "0.5.0",
        "status": "🚧 In Progress",
        "features": ["Phase 2 Dogfooding", "..."]
      }
    ]
  },
  "related_projects": [...],       // Links to related work
  "footer": {...}                  // Acknowledgments and metadata
}
```

**Key benefits of this structure:**

- **Modular**: Update one section without touching others
- **Validated**: JSON structure ensures consistency
- **Reusable**: Same data for website, slides, marketing materials
- **Version-controlled**: Track content changes separately from structure
- **Searchable**: Easy to find and update specific content
- **Type-safe**: Can be validated against a JSON schema

## Step 2: Understanding the Template

The `readme.j2` template defines how the data is presented:

```jinja2
# {{ readme.project.name }}

**Version {{ readme.project.version }}** | \
[Documentation]({{ readme.project.links.documentation }}) | \
[Changelog]({{ readme.project.links.changelog }})

{{ readme.project.tagline }}.

{% for badge in readme.project.badges -%}
[![{{ badge.label }}](https://img.shields.io/badge/{{ badge.message }}-{{ badge.color }}.svg)]({{ badge.url }})
{% endfor %}

---

## What is {{ readme.project.short_name }}?

{{ readme.project.description }}

**Key Features:**

{% for feature in readme.features -%}
- **{{ feature.name }}** - {{ feature.description }}
{% endfor %}

---

## Quick Start

### Installation

**Prerequisites:**
{% for prereq in readme.quick_start.prerequisites -%}
- {{ prereq }}
{% endfor %}

**Install {{ readme.project.short_name }}:**

```bash
{% for step in readme.quick_start.installation_steps -%}
# {{ step.title }}
{{ step.command }}

{% endfor %}
```
```

**Template features:**

1. **Variables**: `{{ readme.project.name }}` - Insert data values
2. **Loops**: `{% for feature in readme.features %}` - Iterate over lists
3. **Conditionals**: `{% if cat.get('items') %}` - Conditional sections
4. **Filters**: `{{ guides | join(', ') }}` - Transform data

**Customization points:**

- **Add new sections**: Create new data in JSON, add template section
- **Change ordering**: Rearrange template sections
- **Conditional content**: Use `{% if %}` for version-specific content
- **Custom formatting**: Modify headers, lists, code blocks
- **Add emojis**: Include in template for visual emphasis

## Step 3: Running the Generator

Generate the README using the provided script:

```bash
poetry run python scripts/generate_readme.py
```

**Expected output:**

```
Loading config from: configs/content/readme/readme-content.json
Generating README using Jinja2Generator...

✅ README generated successfully!
📄 Output written to: README-generated.md
📊 Generated 10,133 characters
📝 Generated 415 lines

Compare with current version:
  diff README.md README-generated.md

Or use to replace current version:
  mv README-generated.md README.md
```

**The script performs these steps:**

1. Loads `readme-content.json` using ConfigLoader
2. Validates the configuration against the schema
3. Initializes Jinja2Generator with template directory
4. Resolves context (loads `readme-data.json`)
5. Renders `readme.j2` template with the data
6. Writes output to `README-generated.md`
7. Reports statistics (character count, line count)

**Best practices:**

- **Always review diff first**: Check changes before replacing
  ```bash
  diff README.md README-generated.md | less
  ```

- **Commit data separately**: Keep data and template changes in separate commits
  ```bash
  git add configs/content/readme/readme-data.json
  git commit -m "docs: update feature list in README data"
  ```

- **Regenerate after version bumps**: Update `project.version` and regenerate

- **Test links**: Verify all links work after generation
  ```bash
  # Use markdown-link-check or similar tool
  npx markdown-link-check README-generated.md
  ```

- **Keep generated file in .gitignore**: Or commit it if you want version history of generated output

## Step 4: Updating README Content

To update the README, edit the data file and regenerate.

### Adding a New Feature

Edit `configs/content/readme/readme-data.json`:

```json
{
  "features": [
    {
      "name": "Configuration-Driven",
      "description": "Define workflows using JSON Schema-validated configs"
    },
    {
      "name": "NEW FEATURE",
      "description": "Description of the new feature"
    }
  ]
}
```

Regenerate:

```bash
poetry run python scripts/generate_readme.py
```

### Updating Version Number

Edit the version field:

```json
{
  "project": {
    "version": "0.6.0"
  }
}
```

Regenerate to update version everywhere it appears (header, footer, etc.).

### Adding Documentation

Edit the documentation structure:

```json
{
  "documentation": {
    "categories": {
      "tutorials": {
        "items": [
          {"title": "Existing Tutorial", "path": "docs/..."},
          {"title": "New Tutorial", "path": "docs/tutorials/new-tutorial.md"}
        ]
      }
    }
  }
}
```

### Updating the Roadmap

Edit the roadmap versions:

```json
{
  "roadmap": {
    "versions": [
      {
        "version": "0.6.0",
        "status": "🚧 In Progress",
        "features": [
          "Code generation generator",
          "BDD scenario generator"
        ]
      }
    ]
  }
}
```

### Common Update Scenarios

| What to Update | Where in JSON | Example |
|----------------|---------------|---------|
| Version number | `project.version` | `"0.6.0"` |
| Feature list | `features[]` | Add new object |
| Badge | `project.badges[]` | Add new badge object |
| Installation step | `quick_start.installation_steps[]` | Add new step |
| Documentation link | `documentation.categories.*.items[]` | Add new item |
| Dev tool | `development.tools[]` | Add new tool |
| Example | `examples[]` | Add new example object |
| Roadmap version | `roadmap.versions[]` | Add or modify version |

### Validation Checklist

After updating data:

- ✅ **Check JSON syntax**: `jq . configs/content/readme/readme-data.json`
- ✅ **Preview README**: `cat README-generated.md | less`
- ✅ **Check formatting**: Look for broken tables, lists, code blocks
- ✅ **Verify links**: All internal and external links resolve
- ✅ **Check badges**: Shields.io URLs are correct
- ✅ **Test commands**: All shell commands work as documented
- ✅ **Review diff**: Compare with previous version

## Step 5: Customizing the Template

You can modify the template to change presentation without touching the data.

### Adding a New Section

1. **Add data** in `readme-data.json`:

```json
{
  "use_cases": [
    {
      "title": "API Documentation",
      "description": "Generate comprehensive API docs from OpenAPI specs",
      "example": "examples/jinja2-api-docs/"
    },
    {
      "title": "Test Generation",
      "description": "Create BDD scenarios from requirements",
      "example": "examples/bdd-generation/"
    }
  ]
}
```

2. **Add template section** in `readme.j2`:

```jinja2
## Use Cases

Chora Compose excels at these common scenarios:

{% for use_case in readme.use_cases %}
### {{ use_case.title }}

{{ use_case.description }}

**Example:** `{{ use_case.example }}`

{% endfor %}
```

3. **Regenerate** to see the new section.

### Conditional Sections

Show content only for certain conditions:

```jinja2
{% if readme.project.version.startswith('0.') %}
**⚠️ Note:** This is a pre-1.0 release. The API may change.
{% endif %}

{% if readme.roadmap.versions | length > 3 %}
**📋 Detailed Roadmap:** See [ROADMAP.md](ROADMAP.md) for full plans.
{% endif %}
```

### Custom Formatting

Change how content is presented:

```jinja2
{# Table format instead of list #}
| Feature | Description |
|---------|-------------|
{% for feature in readme.features -%}
| **{{ feature.name }}** | {{ feature.description }} |
{% endfor %}

{# Numbered list instead of bullets #}
{% for step in readme.quick_start.installation_steps %}
{{ loop.index }}. **{{ step.title }}**
   ```bash
   {{ step.command }}
   ```
{% endfor %}
```

## Troubleshooting

### Template Rendering Fails

**Error:** `jinja2.exceptions.TemplateAssertionError` or `TypeError`

**Solutions:**

1. **Check JSON syntax**:
   ```bash
   jq . configs/content/readme/readme-data.json
   ```
   If this fails, you have invalid JSON.

2. **Verify field references**:
   - Ensure all fields referenced in template exist in data
   - Check for typos in field names
   - Use `.get()` for optional fields: `{% if cat.get('items') %}`

3. **Check Jinja2 syntax**:
   - Matching `{% %}` and `{{ }}` pairs
   - Proper `{% endfor %}` and `{% endif %}` closing tags
   - Valid filter names (e.g., `join`, not custom Python filters)

### Missing Sections in Output

**Problem:** Expected section doesn't appear in generated README

**Solutions:**

1. **Check conditional logic**:
   ```jinja2
   {% if readme.documentation.categories.get('tutorials') %}
   {# This section only appears if tutorials exist #}
   {% endif %}
   ```

2. **Verify data structure**:
   - Ensure nested objects exist
   - Check array is not empty
   - Validate field names match exactly

3. **Debug with print statements**:
   - Add to template temporarily:
   ```jinja2
   {# DEBUG: {{ readme.documentation | tojson }} #}
   ```

### Formatting Issues

**Problem:** Markdown doesn't render correctly

**Solutions:**

1. **Check for proper escaping**:
   - Special characters in strings may need escaping
   - Use `|safe` filter if HTML is intentional

2. **Verify code block syntax**:
   - Three backticks for code blocks
   - Proper language specifiers

3. **Test with markdown linter**:
   ```bash
   npx markdownlint README-generated.md
   ```

### Performance Issues

**Problem:** Generation is slow

**Solutions:**

1. **Check data file size**:
   - Large JSON files take longer to load
   - Consider splitting into multiple files

2. **Simplify template**:
   - Reduce nested loops
   - Minimize complex conditionals

3. **Profile the script**:
   ```bash
   poetry run python -m cProfile scripts/generate_readme.py
   ```

## Next Steps

After mastering README generation, you can:

### Generate Other Project Documentation

Use the same pattern for:
- **CONTRIBUTING.md**: Contributor guidelines from structured data
- **CODE_OF_CONDUCT.md**: Community standards
- **SECURITY.md**: Security policy
- **SUPPORT.md**: Support resources

### Create Project Website

Reuse the same `readme-data.json` to generate:
- Landing page HTML
- Feature showcase pages
- Documentation portal index

### Auto-Generate Marketing Materials

Transform your data into:
- Slide decks (reveal.js, Marp)
- Social media posts
- Blog announcements
- Email newsletters

### Build Documentation Portal

Generate entire documentation site:
```bash
# Use data to create multiple pages
scripts/generate_website.py
```

### Integrate with CI/CD

Automate README updates:

```yaml
# .github/workflows/update-readme.yml
name: Update README
on:
  push:
    paths:
      - 'configs/content/readme/**'
jobs:
  regenerate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: poetry run python scripts/generate_readme.py
      - run: mv README-generated.md README.md
      - uses: stefanzweifel/git-auto-commit-action@v4
```

## Related Documentation

**Dogfooding guides:**
- [Generate CHANGELOG](generate-changelog.md) - Automated changelog from structured data
- [Generate Release Notes](generate-release-notes.md) - GitHub release notes (data reuse example)
- [Generate Documentation Status](generate-docs-status-report.md) - Real-time docs tracking

**Jinja2 guides:**
- [Use Template Inheritance](../generation/use-template-inheritance.md) - Reusable template patterns
- [Debug Jinja2 Templates](../generation/debug-jinja2-templates.md) - Troubleshooting templates

**Architecture:**
- [Why Jinja2 for Dynamic Generation](../../explanation/architecture/why-jinja2-for-dynamic-generation.md) - Design rationale

---

**Questions?** Open an issue or see the [Jinja2Generator API Reference](../../reference/api/generators/jinja2.md).
