# How-To: Generate GitHub Release Notes Using Chora Compose

**Skill Level:** Intermediate
**Time:** 5 minutes
**Prerequisites:**
- Chora Compose installed
- Understanding of Jinja2 templates
- [CHANGELOG generation setup](generate-changelog.md) completed
- GitHub CLI (`gh`) installed

## What This Solves

GitHub release notes are typically copy-pasted from CHANGELOG.md or manually written. This approach has problems:

1. **Duplication**: Same information written twice
2. **Inconsistency**: Different formatting between CHANGELOG and release notes
3. **Manual effort**: Time-consuming copy-paste and formatting
4. **Missing context**: Release notes lack installation instructions, links

By using Chora Compose's Jinja2Generator with a different template but the **same data source**, we can:

- Generate both CHANGELOG.md and GitHub release notes from one JSON file
- Ensure consistency between both outputs
- Add GitHub-specific features (emojis, installation steps, links)
- Automate the entire release notes workflow

This demonstrates the **power of data reuse** - one source, multiple outputs.

## Key Insight: Data Reuse

The magic of this approach is using the **same structured data** but **different templates**:

```
vX.X.X-release-data.json
    ↓
    ├── changelog.j2 → CHANGELOG.md (Keep a Changelog format)
    └── release-notes.j2 → release-notes.md (GitHub-optimized format)
```

**Same data, different presentations!**

**Note:** Replace `X.X.X` with your actual version number (e.g., `0.4.0`) throughout this guide.

## Files Overview

```
configs/
├── content/changelog/
│   ├── vX.X.X-release-data.json       # ✅ Already created (shared data)
│   ├── changelog-content.json          # ✅ CHANGELOG config
│   └── release-notes-content.json      # 🆕 Release notes config
└── templates/changelog/
    ├── changelog.j2                    # ✅ CHANGELOG template
    └── release-notes.j2                # 🆕 Release notes template

scripts/
├── generate_changelog.py               # ✅ CHANGELOG generator
└── generate_release_notes.py           # 🆕 Release notes generator

CHANGELOG-generated.md                  # ✅ Generated CHANGELOG
release-notes-vX.X.X.md                 # 🆕 Generated release notes
```

## Step 1: Create GitHub-Optimized Template

Create a template optimized for GitHub releases with emojis, highlights, and installation instructions:

**File:** `configs/templates/changelog/release-notes.j2`

```jinja2
## Summary

This release includes {{ release.sections.added.core_features | length }} new core features, {{ release.sections.changed | length }} improvements, and {{ release.sections.fixed | length }} bug fixes.

## 🎉 Highlights

- **{{ release.sections.added.core_features[0].name }}**: {{ release.sections.added.core_features[0].description }}
- **{{ release.sections.added.documentation.total_documents }} Complete Documentation**: Full {{ release.sections.added.documentation.framework }} framework implementation
- **{{ release.sections.added.development_process.name }}**: {{ release.sections.added.development_process.status }}

---

## ✨ What's New

### Core Features
{% for feature in release.sections.added.core_features %}
**{{ feature.name }}**
{{ feature.description }}

{% for detail in feature.details %}
- {{ detail }}
{% endfor %}

{% endfor %}

### Documentation
{{ release.sections.added.documentation.total_documents }} complete documents following the {{ release.sections.added.documentation.framework }} framework:

- **{{ release.sections.added.documentation.tutorials | length }} Tutorials**: {% for tutorial in release.sections.added.documentation.tutorials %}{{ tutorial }}{% if not loop.last %}, {% endif %}{% endfor %}
- **{{ release.sections.added.documentation.how_to_guides | length }} How-To Guides**: Practical guides for common tasks
- **{{ release.sections.added.documentation.reference | length }} Reference Docs**: Complete API documentation
- **{{ release.sections.added.documentation.explanation | length }} Explanation Docs**: Deep dives into design decisions

---

## 🔄 Changes
{% for change in release.sections.changed %}
- **{{ change.item }}**: {{ change.description }}
{% endfor %}

---

## 🐛 Bug Fixes
{% for fix in release.sections.fixed %}
- **{{ fix.item }}**: {{ fix.description }}
{% endfor %}

---

## 📦 Installation

### From Source
\```bash
git clone https://github.com/liminalcommons/chora-compose.git
cd chora-compose
git checkout v{{ release.version }}
poetry install
\```

### Verify Installation
\```bash
poetry run python -c "from chora_compose import __version__; print(f'Chora Compose v{__version__}')"
\```

---

## 📚 Documentation

- 📖 [Complete Documentation](https://github.com/liminalcommons/chora-compose/tree/v{{ release.version }}/docs)
- 🚀 [Getting Started Tutorial](https://github.com/liminalcommons/chora-compose/blob/v{{ release.version }}/docs/tutorials/getting-started/01-installation.md)
- 💡 [Examples](https://github.com/liminalcommons/chora-compose/tree/v{{ release.version }}/examples)
- 📝 [Full Changelog](https://github.com/liminalcommons/chora-compose/blob/v{{ release.version }}/CHANGELOG.md)

---

## 🔒 Security

{% for security_item in release.notes.security %}
- {{ security_item }}
{% endfor %}

---

## 🙏 Thank You

Thank you to everyone who contributed to this release!

**Full Changelog**: [{{ release.version }}]({{ release.release_url }})
```

**Template Features:**
- Emoji section markers for visual appeal
- Summary with automated counts
- Highlights section (top 3 features)
- Installation instructions with version
- Documentation links (versioned)
- Security notes
- Thank you message

## Step 2: Create Release Notes Content Config

Create a content config that uses the **same data** but different template:

**File:** `configs/content/changelog/release-notes-content.json`

```json
{
  "type": "content",
  "id": "release-notes-vX-X-X",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "Generated GitHub release notes for Chora Compose vX.X.X",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "markdown"
  },
  "instructions": {
    "global": "Generate GitHub release notes from structured release data using Jinja2 template.",
    "system_prompt": "Transform release data JSON into GitHub-optimized release notes format.",
    "user_prompt": "Include highlights, installation instructions, documentation links, and security notes."
  },
  "inputs": {
    "sources": [
      {
        "id": "release-data",
        "source_type": "external_file",
        "source_locator": "configs/content/changelog/vX.X.X-release-data.json",
        "notes": "Structured release data for vX.X.X (same data as CHANGELOG)"
      }
    ]
  },
  "elements": [
    {
      "name": "release-notes",
      "description": "Complete GitHub release notes content",
      "prompt_guidance": "Generate comprehensive release notes optimized for GitHub releases.",
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
        "id": "release-notes-generation",
        "type": "jinja2",
        "template": "release-notes.j2",
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
        "description": "Initial release notes generation config for dogfooding Chora Compose.",
        "rationale": "Demonstrate reusing same data for multiple outputs (CHANGELOG + release notes)."
      }
    ]
  }
}
```

**Key Point:** Notice the `source_locator` points to the **same JSON file** as the CHANGELOG config!

## Step 3: Create Generation Script

Create a script to generate release notes:

**File:** `scripts/generate_release_notes.py`

```python
#!/usr/bin/env python3
"""Generate GitHub release notes from structured release data using Jinja2Generator."""

from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.core.models import ContentConfig
from chora_compose.generators.jinja2 import Jinja2Generator


def main() -> None:
    """Generate GitHub release notes from structured data."""
    # Load the content config
    config_path = Path("configs/content/changelog/release-notes-content.json")
    loader = ConfigLoader()
    config = loader.load_config(config_path)

    if not isinstance(config, ContentConfig):
        raise ValueError(f"Expected ContentConfig, got {type(config)}")

    # Generate release notes using Jinja2Generator
    template_dir = Path("configs/templates/changelog")
    generator = Jinja2Generator(template_dir=template_dir)
    release_notes_content = generator.generate(config)

    # Write to output file
    output_path = Path("release-notes-vX.X.X.md")
    output_path.write_text(release_notes_content, encoding="utf-8")

    print(f"✅ Release notes generated successfully!")
    print(f"📄 Output written to: {output_path}")
    print(f"\nUse with gh CLI:")
    print(f"  gh release edit vX.X.X --notes-file {output_path}")


if __name__ == "__main__":
    main()
```

## Step 4: Generate Release Notes

Run the generation script:

```bash
poetry run python scripts/generate_release_notes.py
```

**Expected Output:**
```
Loading config from: configs/content/changelog/release-notes-content.json
Generating release notes using Jinja2Generator...

✅ Release notes generated successfully!
📄 Output written to: release-notes-vX.X.X.md
📊 Generated 4166 characters
📝 Generated 186 lines

Use with gh CLI:
  gh release edit vX.X.X --notes-file release-notes-vX.X.X.md

Or for new releases:
  gh release create vX.X.X --notes-file release-notes-vX.X.X.md dist/*.whl dist/*.tar.gz
```

## Step 5: Review Generated Release Notes

Preview the generated release notes:

```bash
cat release-notes-vX.X.X.md | head -50
```

**Sample Output:**
```markdown
## Summary

This release includes 4 new core features, 3 improvements, and 3 bug fixes.

## 🎉 Highlights

- **Jinja2Generator**: Template-based content generation with full Jinja2 support
- **24 Complete Documentation**: Full Diátaxis framework implementation
- **Documentation-Driven Development (DDD) Pilot**: Complete success

---

## ✨ What's New

### Core Features

**Jinja2Generator**
Template-based content generation with full Jinja2 support

- Template inheritance and includes
- Custom filters via `register_filter()`
...
```

## Step 6: Use with GitHub CLI

### For Existing Releases (Update)

Update an existing release with new notes:

```bash
gh release edit vX.X.X --notes-file release-notes-vX.X.X.md
```

### For New Releases (Create)

Create a new release with generated notes:

```bash
gh release create v0.3.0 \
  --title "Release v0.3.0" \
  --notes-file release-notes-v0.3.0.md \
  dist/*.whl dist/*.tar.gz
```

## Benefits

### 1. Single Source of Truth
- Release data stored once: `v0.2.0-release-data.json`
- Used by both CHANGELOG and release notes
- No duplication, no inconsistency

### 2. Multiple Output Formats
From one JSON file, generate:
- `CHANGELOG.md` (Keep a Changelog format)
- `release-notes.md` (GitHub release format)
- Future: Blog posts, email newsletters, tweets

### 3. GitHub-Specific Enhancements
The release notes template adds:
- Emojis for visual appeal (🎉, ✨, 🐛, 📦, 🔒)
- Highlights section (top features)
- Installation instructions
- Documentation links (version-specific)
- Thank you message

### 4. Automated Workflow
```bash
# 1. Update release data
vim configs/content/changelog/v0.3.0-release-data.json

# 2. Generate both outputs
poetry run python scripts/generate_changelog.py
poetry run python scripts/generate_release_notes.py

# 3. Commit and tag
git add CHANGELOG.md
git commit -m "chore: prepare v0.3.0 release"
git tag -a v0.3.0 -F release-notes-v0.3.0.md

# 4. Create GitHub release
gh release create v0.3.0 \
  --notes-file release-notes-v0.3.0.md \
  dist/*.whl dist/*.tar.gz
```

### 5. Consistency Guaranteed
- Both outputs generated from same data
- Template changes apply to all releases
- Version-specific links automatically correct

## Comparison: CHANGELOG vs Release Notes

**CHANGELOG.md** (Keep a Changelog format):
- Standard format for version control
- Complete history (all versions)
- Links to releases at bottom
- No emojis or GitHub-specific features
- Used by developers reading the repo

**release-notes.md** (GitHub-optimized):
- Single release focus
- Summary and highlights at top
- Emojis for visual appeal
- Installation instructions included
- Documentation links (version-specific)
- Thank you message
- Used by users viewing releases

**Both use the same data!** This is the power of template-based generation.

## Real-World Workflow

### For v0.3.0 Release:

1. **Create release data**: `configs/content/changelog/v0.3.0-release-data.json`
2. **Update config IDs**: Change `v0-2-0` to `v0-3-0` in configs
3. **Update paths**: Point to new data file in both configs
4. **Generate both**:
   ```bash
   poetry run python scripts/generate_changelog.py
   poetry run python scripts/generate_release_notes.py
   ```
5. **Review and commit**:
   ```bash
   diff CHANGELOG.md CHANGELOG-generated.md
   mv CHANGELOG-generated.md CHANGELOG.md
   git add CHANGELOG.md
   git commit -m "chore: prepare v0.3.0 release"
   ```
6. **Create release**:
   ```bash
   gh release create v0.3.0 --notes-file release-notes-v0.3.0.md dist/*
   ```

## Troubleshooting

**Template rendering errors:**
- Check template syntax with `poetry run python -m jinja2 configs/templates/changelog/release-notes.j2`
- Verify all referenced fields exist in JSON data
- Test with minimal data first

**Missing emojis in output:**
- Emojis should work in markdown
- GitHub renders them correctly
- If not visible, check terminal encoding

**Links not working:**
- Verify `release.version` in JSON matches tag
- Check `release.release_url` is correct
- Ensure branch exists for versioned docs links

**gh CLI errors:**
- Ensure authenticated: `gh auth login`
- Verify repository access: `gh repo view`
- Check file exists: `ls -l release-notes-vX.X.X.md`

## Next Steps

1. **Automate for future releases**: Create script that takes version as argument
2. **Add more output formats**: Email newsletter template, blog post template
3. **CI/CD integration**: Auto-generate on version bump
4. **Custom highlights**: Add `highlights` field to JSON data for manual curation
5. **Social media**: Generate Twitter/LinkedIn posts from same data

## Related Documentation

- [How-To: Generate CHANGELOG](generate-changelog.md) - Setup the shared data source
- [Jinja2Generator API Reference](../../reference/generators/jinja2-generator.md)
- [Tutorial: Dynamic Content with Jinja2](../../tutorials/getting-started/04-dynamic-content-jinja2.md)
- [Release Process](../../meta/RELEASE_PROCESS.md) - Full release workflow

## Success Criteria

You've successfully set up release notes generation when:

- ✅ Release notes template created with GitHub optimizations
- ✅ Content config points to same data as CHANGELOG
- ✅ Generated release notes include summary, highlights, installation
- ✅ Emojis render correctly
- ✅ Version-specific documentation links work
- ✅ `gh release create` accepts the notes file
- ✅ Both CHANGELOG and release notes stay in sync

## Metadata

**Category:** Dogfooding
**Tags:** github, release-notes, jinja2, automation, data-reuse
**Last Updated:** 2025-10-11
**Chora Compose Version:** 0.2.0+
