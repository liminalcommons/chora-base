# How-To: Generate CHANGELOG Using Chora Compose

**Skill Level:** Intermediate
**Time:** 5 minutes
**Prerequisites:**
- Chora Compose installed
- Understanding of Jinja2 templates
- Familiarity with Keep a Changelog format

## What This Solves

Manually maintaining a CHANGELOG.md is error-prone and time-consuming. By using Chora Compose's Jinja2Generator, we can:

1. Store release data in structured JSON format (single source of truth)
2. Generate CHANGELOG.md automatically from the data
3. Ensure consistent formatting across releases
4. Enable reuse of data for GitHub release notes
5. Validate data structure before generation

This is a "dogfooding" example - using Chora Compose to manage Chora Compose itself.

## Files Overview

The CHANGELOG generation system consists of:

```
configs/
├── content/changelog/
│   ├── changelog-content.json          # Content config
│   └── vX.X.X-release-data.json       # Structured release data (replace X.X.X with version)
└── templates/changelog/
    └── changelog.j2                    # Jinja2 template

scripts/
└── generate_changelog.py               # Generation script

CHANGELOG-generated.md                  # Generated output
```

**Note:** Replace `X.X.X` with your actual version number (e.g., `0.4.0`) throughout this guide.

## Step 1: Prepare Release Data

Create a structured JSON file with your release data:

**File:** `configs/content/changelog/vX.X.X-release-data.json`

```json
{
  "version": "X.X.X",
  "date": "YYYY-MM-DD",
  "release_url": "https://github.com/your-org/your-repo/releases/tag/vX.X.X",
  "sections": {
    "added": {
      "core_features": [
        {
          "name": "Jinja2Generator",
          "description": "Template-based content generation with full Jinja2 support",
          "details": [
            "Template inheritance and includes",
            "Custom filters via `register_filter()`",
            "Global variables via `register_global()`"
          ]
        }
      ],
      "documentation": {
        "total_documents": 24,
        "framework": "Diátaxis",
        "tutorials": ["Your First Config", "Generate Your First Content"]
      }
    },
    "changed": [
      {
        "item": "Generator Strategy Pattern",
        "description": "Refactored to support multiple generator types"
      }
    ],
    "fixed": [
      {
        "item": "Type Hints",
        "description": "Added proper type: ignore comments for library returns"
      }
    ]
  },
  "notes": {
    "breaking_changes": "None in this release (initial feature release)",
    "security": [
      "All dependencies up to date",
      "Input validation on all user-provided data"
    ]
  }
}
```

**Key Benefits:**
- Structured data is easier to validate
- Can be reused for release notes, announcements, etc.
- Version-controlled alongside code
- Can be generated from git history or issue tracking

## Step 2: Create Jinja2 Template

Create a template that transforms the JSON data into Keep a Changelog format:

**File:** `configs/templates/changelog/changelog.j2`

```jinja2
# Changelog

All notable changes to the Chora Compose will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{{ release.version }}] - {{ release.date }}

### Added

#### Core Features
{% for feature in release.sections.added.core_features %}
- **{{ feature.name }}** - {{ feature.description }}
{%- for detail in feature.details %}
  - {{ detail }}
{%- endfor %}
{% endfor %}

#### Documentation ({{ release.sections.added.documentation.total_documents }} Complete Documents)
- Complete {{ release.sections.added.documentation.framework }} documentation framework implementation
- **Tutorials ({{ release.sections.added.documentation.tutorials | length }} documents)**:
{%- for tutorial in release.sections.added.documentation.tutorials %}
  - {{ tutorial }}
{%- endfor %}

### Changed
{% for change in release.sections.changed %}
- **{{ change.item }}** - {{ change.description }}
{% endfor %}

### Fixed
{% for fix in release.sections.fixed %}
- **{{ fix.item }}** - {{ fix.description }}
{% endfor %}

## Notes

### Breaking Changes
- {{ release.notes.breaking_changes }}

### Security
{% for security_item in release.notes.security %}
- {{ security_item }}
{% endfor %}

[{{ release.version }}]: {{ release.release_url }}
```

**Template Features:**
- Dynamic version and date insertion
- Loops for lists (features, changes, fixes)
- Conditional sections
- Automatic counting (e.g., number of tutorials)
- Consistent formatting

## Step 3: Create Content Config

Create a content config that connects the data and template:

**File:** `configs/content/changelog/changelog-content.json`

```json
{
  "type": "content",
  "id": "changelog-vX-X-X",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Generated changelog for Chora Compose vX.X.X release",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "markdown"
  },
  "instructions": {
    "global": "Generate CHANGELOG.md from structured release data using Jinja2 template.",
    "system_prompt": "Transform release data JSON into Keep a Changelog format.",
    "user_prompt": "Include all sections: Added, Changed, Fixed, and Notes."
  },
  "inputs": {
    "sources": [
      {
        "id": "release-data",
        "source_type": "external_file",
        "source_locator": "configs/content/changelog/vX.X.X-release-data.json",
        "notes": "Structured release data for vX.X.X"
      }
    ]
  },
  "elements": [
    {
      "name": "changelog",
      "description": "Complete CHANGELOG.md content",
      "prompt_guidance": "Generate complete changelog following Keep a Changelog format.",
      "format": "markdown",
      "output_format": "markdown",
      "example_output": "",
      "generation_source": "ai",
      "review_status": "approved"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "changelog-generation",
        "type": "jinja2",
        "template": "changelog.j2",
        "generation_config": {
          "context": {
            "release": {
              "source": "file",
              "path": "configs/content/changelog/vX.X.X-release-data.json"
            }
          }
        }
      }
    ]
  },
  "validation": {
    "rules": [
      {
        "id": "markdown-format-check",
        "check_type": "format",
        "target": "output",
        "threshold": 1.0,
        "severity": "error"
      }
    ]
  },
  "state": {
    "tracking": {
      "history": true,
      "versioning": true
    }
  },
  "evolution": {
    "stage": "approved",
    "history": [
      {
        "date": "2025-10-11",
        "type": "creation",
        "description": "Initial changelog generation config for dogfooding Chora Compose.",
        "rationale": "Demonstrate using Chora Compose to manage Chora Compose itself."
      }
    ]
  }
}
```

**Config Highlights:**
- Uses `jinja2` generation type
- Specifies template file (`changelog.j2`)
- Loads context from external JSON file
- Includes validation rules
- Tracks evolution history

## Step 4: Create Generation Script

Create a script to generate the CHANGELOG:

**File:** `scripts/generate_changelog.py`

```python
#!/usr/bin/env python3
"""Generate CHANGELOG.md from structured release data using Jinja2Generator."""

from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.core.models import ContentConfig
from chora_compose.generators.jinja2 import Jinja2Generator


def main() -> None:
    """Generate CHANGELOG from structured data."""
    # Load the content config
    config_path = Path("configs/content/changelog/changelog-content.json")
    loader = ConfigLoader()
    config = loader.load_config(config_path)

    if not isinstance(config, ContentConfig):
        raise ValueError(f"Expected ContentConfig, got {type(config)}")

    # Generate changelog using Jinja2Generator
    template_dir = Path("configs/templates/changelog")
    generator = Jinja2Generator(template_dir=template_dir)
    changelog_content = generator.generate(config)

    # Write to output file
    output_path = Path("CHANGELOG-generated.md")
    output_path.write_text(changelog_content, encoding="utf-8")

    print(f"✅ CHANGELOG generated successfully!")
    print(f"📄 Output written to: {output_path}")


if __name__ == "__main__":
    main()
```

## Step 5: Generate CHANGELOG

Run the generation script:

```bash
poetry run python scripts/generate_changelog.py
```

**Expected Output:**
```
Loading config from: configs/content/changelog/changelog-content.json
Generating CHANGELOG using Jinja2Generator...

✅ CHANGELOG generated successfully!
📄 Output written to: CHANGELOG-generated.md
📊 Generated 5855 characters
📝 Generated 200 lines

Compare with manual version:
  diff CHANGELOG.md CHANGELOG-generated.md

Or use to replace manual version:
  mv CHANGELOG-generated.md CHANGELOG.md
```

## Step 6: Review and Compare

Compare the generated CHANGELOG with your manual version:

```bash
diff CHANGELOG.md CHANGELOG-generated.md
```

If satisfied, replace the manual version:

```bash
mv CHANGELOG-generated.md CHANGELOG.md
```

## Benefits

**Single Source of Truth:**
- Release data stored once in structured format
- No duplication between CHANGELOG and release notes

**Consistency:**
- Every release follows the same format
- No formatting errors or inconsistencies

**Reusability:**
- Same data can generate multiple outputs:
  - CHANGELOG.md
  - GitHub release notes
  - Blog post announcements
  - Email newsletters

**Validation:**
- JSON schema validation ensures data completeness
- Template errors caught before generation

**Version Control:**
- Data files are version-controlled
- Easy to see what changed between releases

**Time Savings:**
- No manual formatting
- No copy-paste errors
- Automated generation in CI/CD

## Next Steps

1. **Automate for All Releases:** Create a script that generates changelogs for all versions
2. **Generate Release Notes:** Use the same data to generate GitHub release notes
3. **CI/CD Integration:** Auto-generate CHANGELOG on version bump
4. **Data Validation:** Add JSON schema for release data validation
5. **Multi-format Output:** Generate HTML, PDF, or other formats from same data

## Troubleshooting

**Config validation errors:**
- Ensure `type: "content"` is present
- Check `id` uses kebab-case (no dots)
- Verify `schemaRef` matches schema version

**Template not found:**
- Verify template path in `generation.patterns[].template`
- Ensure `template_dir` is set correctly in script
- Check template file exists

**Context loading errors:**
- Verify file paths in `generation_config.context`
- Ensure JSON files are valid
- Check file permissions

**Missing data in output:**
- Review template logic (loops, conditionals)
- Check JSON data structure matches template expectations
- Add debug output to see context data

## Related Documentation

- [Jinja2Generator API Reference](../../reference/generators/jinja2-generator.md)
- [How-To: Use Template Inheritance](../generators/use-template-inheritance.md)
- [Tutorial: Dynamic Content with Jinja2](../../tutorials/getting-started/04-dynamic-content-jinja2.md)
- [Explanation: Why Jinja2 for Dynamic Generation](../../explanation/why-jinja2.md)

## Success Criteria

You've successfully set up CHANGELOG generation when:

- ✅ Release data is in structured JSON format
- ✅ Jinja2 template produces correct Keep a Changelog format
- ✅ Content config validates successfully
- ✅ Generated CHANGELOG matches manual version (minus formatting)
- ✅ GitHub release URLs are correct
- ✅ All sections (Added, Changed, Fixed, Notes) are present

## Metadata

**Category:** Dogfooding
**Tags:** changelog, jinja2, automation, release-management
**Last Updated:** 2025-10-11
**Chora Compose Version:** 0.2.0+
