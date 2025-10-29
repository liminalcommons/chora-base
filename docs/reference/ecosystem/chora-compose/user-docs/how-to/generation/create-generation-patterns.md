# How to Create Generation Patterns

> **Goal:** Design effective generation patterns for the DemonstrationGenerator.

## When to Use This

You need to create generation patterns when:
- Designing a new content configuration
- Defining how elements should be assembled
- Creating reusable content templates
- Establishing consistent output structure
- Planning multi-section documents

## Prerequisites

- Understanding of content config structure
- Familiarity with DemonstrationGenerator
- JSON syntax knowledge

---

## Solution

### Quick Version

```json
{
  "generation": {
    "patterns": [
      {
        "id": "unique-pattern-id",
        "type": "demonstration",
        "template": "{{variable1}}\n\n{{variable2}}",
        "variables": [
          {
            "name": "variable1",
            "source": "elements.element1.example_output"
          },
          {
            "name": "variable2",
            "source": "elements.element2.example_output",
            "default": "Default content"
          }
        ]
      }
    ]
  }
}
```

### Detailed Steps

#### 1. Define Your Pattern Structure

Start by sketching the desired output structure:

```
DESIRED OUTPUT:
# Title

Description paragraph

## Section 1
Content for section 1

## Section 2
Content for section 2

---
Footer
```

#### 2. Identify Content Elements

Break down the structure into named elements:

- `title` → "# Title"
- `description` → "Description paragraph"
- `section1-heading` → "## Section 1"
- `section1-content` → "Content for section 1"
- `section2-heading` → "## Section 2"
- `section2-content` → "Content for section 2"
- `footer` → "---\nFooter"

#### 3. Create Element Definitions

```json
{
  "elements": [
    {
      "name": "title",
      "format": "markdown",
      "example_output": "# My Document"
    },
    {
      "name": "description",
      "format": "markdown",
      "example_output": "This document explains..."
    },
    {
      "name": "section1-heading",
      "format": "markdown",
      "example_output": "## Introduction"
    },
    {
      "name": "section1-content",
      "format": "markdown",
      "example_output": "Welcome to this document..."
    },
    {
      "name": "section2-heading",
      "format": "markdown",
      "example_output": "## Details"
    },
    {
      "name": "section2-content",
      "format": "markdown",
      "example_output": "Here are the specifics..."
    },
    {
      "name": "footer",
      "format": "markdown",
      "example_output": "---\n© 2025 My Company"
    }
  ]
}
```

#### 4. Design the Template

Create a template that matches your structure:

```json
{
  "template": "{{title}}\n\n{{description}}\n\n{{section1-heading}}\n{{section1-content}}\n\n{{section2-heading}}\n{{section2-content}}\n\n{{footer}}"
}
```

**Note:** Use `\n` for newlines in JSON. The generator converts them to actual newlines.

#### 5. Map Variables to Elements

```json
{
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "description", "source": "elements.description.example_output"},
    {"name": "section1-heading", "source": "elements.section1-heading.example_output"},
    {"name": "section1-content", "source": "elements.section1-content.example_output"},
    {"name": "section2-heading", "source": "elements.section2-heading.example_output"},
    {"name": "section2-content", "source": "elements.section2-content.example_output"},
    {"name": "footer", "source": "elements.footer.example_output"}
  ]
}
```

#### 6. Combine into Complete Pattern

```json
{
  "generation": {
    "patterns": [
      {
        "id": "standard-doc-pattern",
        "type": "demonstration",
        "template": "{{title}}\n\n{{description}}\n\n{{section1-heading}}\n{{section1-content}}\n\n{{section2-heading}}\n{{section2-content}}\n\n{{footer}}",
        "variables": [
          {"name": "title", "source": "elements.title.example_output"},
          {"name": "description", "source": "elements.description.example_output"},
          {"name": "section1-heading", "source": "elements.section1-heading.example_output"},
          {"name": "section1-content", "source": "elements.section1-content.example_output"},
          {"name": "section2-heading", "source": "elements.section2-heading.example_output"},
          {"name": "section2-content", "source": "elements.section2-content.example_output"},
          {"name": "footer", "source": "elements.footer.example_output"}
        ]
      }
    ]
  }
}
```

---

## Pattern Design Recipes

### Recipe: Markdown Document

**Use case:** Technical documentation, README files

```json
{
  "template": "# {{title}}\n\n> {{tagline}}\n\n## Overview\n\n{{overview}}\n\n## Installation\n\n{{installation}}\n\n## Usage\n\n{{usage}}\n\n## API Reference\n\n{{api}}\n\n## License\n\n{{license}}",
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "tagline", "source": "elements.tagline.example_output"},
    {"name": "overview", "source": "elements.overview.example_output"},
    {"name": "installation", "source": "elements.installation.example_output"},
    {"name": "usage", "source": "elements.usage.example_output"},
    {"name": "api", "source": "elements.api.example_output"},
    {"name": "license", "source": "elements.license.example_output"}
  ]
}
```

### Recipe: Python Module

**Use case:** Generate Python files with docstrings

```json
{
  "template": "\"\"\"{{module_docstring}}\"\"\"\n\n{{imports}}\n\n{{constants}}\n\n{{class_definitions}}\n\n{{functions}}",
  "variables": [
    {"name": "module_docstring", "source": "elements.module-docstring.example_output"},
    {"name": "imports", "source": "elements.imports.example_output"},
    {"name": "constants", "source": "elements.constants.example_output"},
    {"name": "class_definitions", "source": "elements.classes.example_output"},
    {"name": "functions", "source": "elements.functions.example_output"}
  ]
}
```

### Recipe: API Response

**Use case:** Generate JSON or structured data

```json
{
  "template": "{\\n  \"status\": \"success\",\\n  \"data\": {{data}},\\n  \"metadata\": {{metadata}}\\n}",
  "variables": [
    {"name": "data", "source": "elements.data.example_output"},
    {"name": "metadata", "source": "elements.metadata.example_output"}
  ]
}
```

### Recipe: Blog Post

**Use case:** Content generation for blogs

```json
{
  "template": "---\\ntitle: {{title}}\\ndate: {{date}}\\nauthor: {{author}}\\ntags: {{tags}}\\n---\\n\\n{{content}}\\n\\n---\\n\\n## Comments\\n\\n{{comments}}",
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "date", "source": "elements.date.example_output"},
    {"name": "author", "source": "elements.author.example_output"},
    {"name": "tags", "source": "elements.tags.example_output"},
    {"name": "content", "source": "elements.content.example_output"},
    {"name": "comments", "source": "elements.comments.example_output", "default": "Comments are disabled."}
  ]
}
```

### Recipe: Email Template

**Use case:** Generate emails

```json
{
  "template": "To: {{recipient}}\\nFrom: {{sender}}\\nSubject: {{subject}}\\n\\n{{greeting}}\\n\\n{{body}}\\n\\n{{signature}}\\n\\n{{footer}}",
  "variables": [
    {"name": "recipient", "source": "elements.recipient.example_output"},
    {"name": "sender", "source": "elements.sender.example_output"},
    {"name": "subject", "source": "elements.subject.example_output"},
    {"name": "greeting", "source": "elements.greeting.example_output"},
    {"name": "body", "source": "elements.body.example_output"},
    {"name": "signature", "source": "elements.signature.example_output"},
    {"name": "footer", "source": "elements.footer.example_output"}
  ]
}
```

---

## Best Practices

### 1. Use Descriptive Pattern IDs

**Good:**
```json
{"id": "readme-with-badges"}
{"id": "python-module-full"}
{"id": "api-doc-minimal"}
```

**Bad:**
```json
{"id": "pattern1"}
{"id": "p2"}
{"id": "demo"}
```

### 2. Name Variables Clearly

**Good:**
```json
{"name": "installation-instructions", "source": "..."}
{"name": "api-reference", "source": "..."}
```

**Bad:**
```json
{"name": "var1", "source": "..."}
{"name": "content", "source": "..."}  // Too vague
```

### 3. Provide Defaults for Optional Content

```json
{
  "variables": [
    {
      "name": "optional-section",
      "source": "elements.optional.example_output",
      "default": ""
    }
  ]
}
```

This prevents errors if the element is missing or empty.

### 4. Maintain Consistent Formatting

Keep indentation and spacing consistent in templates:

```json
{
  "template": "# {{title}}\n\n## Section 1\n\n{{section1}}\n\n## Section 2\n\n{{section2}}"
}
```

Not:
```json
{
  "template": "#{{title}}\n##Section 1\n{{section1}}\n##Section 2\n{{section2}}"
}
```

### 5. Use Semantic Element Names

Match element names to their purpose:

```json
{
  "elements": [
    {"name": "introduction", ...},
    {"name": "methodology", ...},
    {"name": "results", ...},
    {"name": "conclusion", ...}
  ]
}
```

### 6. Test Templates with Real Data

Before finalizing, generate with actual example_output to verify spacing and structure.

---

## Advanced Patterns

### Pattern: Hierarchical Structure

**Nested sections with subsections:**

```json
{
  "template": "# {{main-title}}\n\n## {{section1-title}}\n\n{{section1-intro}}\n\n### {{subsection1-title}}\n\n{{subsection1-content}}\n\n### {{subsection2-title}}\n\n{{subsection2-content}}\n\n## {{section2-title}}\n\n{{section2-content}}",
  "variables": [
    {"name": "main-title", "source": "elements.main-title.example_output"},
    {"name": "section1-title", "source": "elements.section1-title.example_output"},
    {"name": "section1-intro", "source": "elements.section1-intro.example_output"},
    {"name": "subsection1-title", "source": "elements.subsection1-title.example_output"},
    {"name": "subsection1-content", "source": "elements.subsection1-content.example_output"},
    {"name": "subsection2-title", "source": "elements.subsection2-title.example_output"},
    {"name": "subsection2-content", "source": "elements.subsection2-content.example_output"},
    {"name": "section2-title", "source": "elements.section2-title.example_output"},
    {"name": "section2-content", "source": "elements.section2-content.example_output"}
  ]
}
```

### Pattern: Repeated Element

**Reuse same element in multiple places:**

```json
{
  "template": "# {{title}}\n\n{{description}}\n\n---\n\n## Quick Reference\n\n{{description}}\n\n---\n\n## Full Details\n\n{{full-content}}",
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "description", "source": "elements.description.example_output"},
    {"name": "full-content", "source": "elements.full-content.example_output"}
  ]
}
```

The `description` variable appears twice in the template.

### Pattern: Conditional Sections (with defaults)

**Optional sections that can be omitted:**

```json
{
  "template": "# {{title}}\n\n{{content}}\n\n{{optional-warning}}\n\n{{footer}}",
  "variables": [
    {"name": "title", "source": "elements.title.example_output"},
    {"name": "content", "source": "elements.content.example_output"},
    {
      "name": "optional-warning",
      "source": "elements.warning.example_output",
      "default": ""
    },
    {"name": "footer", "source": "elements.footer.example_output"}
  ]
}
```

If `warning` element is empty, the double newline remains. To truly omit, set default to "".

---

## Troubleshooting

**Problem:** Template produces extra blank lines
**Solution:**
- Check for `\n\n` in template where optional content might be empty
- Use empty string `""` as default for optional variables
- Test with empty elements to see actual output

**Problem:** Variables not substituted
**Solution:**
- Ensure variable name in template exactly matches variable definition
- Check for typos (case-sensitive)
- Verify double curly braces: `{{varname}}`

**Problem:** Newlines not rendering
**Solution:**
- Use `\n` in JSON template strings
- Generator automatically converts `\n` → newline
- Don't use literal newlines in JSON (invalid)

**Problem:** Template too complex to maintain
**Solution:**
- Break into multiple smaller patterns
- Use child content configs for sub-sections
- Consider using Jinja2Generator for complex logic

**Problem:** Can't represent desired structure
**Solution:**
- DemonstrationGenerator is intentionally simple
- For conditionals, loops, or complex logic, use Jinja2Generator
- For multiple variants, create multiple patterns

---

## When to Use Multiple Patterns

A single config can have multiple patterns for different outputs:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "full-version",
        "type": "demonstration",
        "template": "{{all-sections}}",
        "variables": [...]
      },
      {
        "id": "summary-version",
        "type": "demonstration",
        "template": "{{summary-only}}",
        "variables": [...]
      },
      {
        "id": "technical-version",
        "type": "demonstration",
        "template": "{{technical-details}}",
        "variables": [...]
      }
    ]
  }
}
```

**Note:** DemonstrationGenerator uses the first `demonstration` pattern by default. To use others, you'd need to specify which pattern to use (future enhancement).

---

## Pattern Evolution

Start simple, refine iteratively:

**Version 1: Minimal**
```json
{
  "template": "{{intro}}\n{{body}}"
}
```

**Version 2: Add Structure**
```json
{
  "template": "# Document\n\n{{intro}}\n\n## Details\n\n{{body}}"
}
```

**Version 3: Add Metadata**
```json
{
  "template": "---\ntitle: {{title}}\n---\n\n# {{title}}\n\n{{intro}}\n\n## Details\n\n{{body}}"
}
```

**Version 4: Polish**
```json
{
  "template": "---\ntitle: {{title}}\nauthor: {{author}}\ndate: {{date}}\n---\n\n# {{title}}\n\n> {{tagline}}\n\n{{intro}}\n\n## Details\n\n{{body}}\n\n---\n\n{{footer}}"
}
```

---

## See Also

- [How to: Use Demonstration Generator](use-demonstration-generator.md) - Apply these patterns
- [How to: Debug Generation](debug-generation.md) - Troubleshoot issues
- [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - Learn basics
- [DemonstrationGenerator API Reference](../../reference/api/generators/demonstration.md) - Technical details
