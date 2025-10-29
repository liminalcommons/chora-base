# How-To: Generate API Documentation Using Chora Compose

**Skill Level:** Advanced
**Time:** 20 minutes
**Prerequisites:** Chora Compose installed, Understanding of Python AST

## What This Solves

**The Problem:**
- API documentation becomes outdated as code evolves
- Manually maintaining API docs is time-consuming
- Docstrings and type hints are duplicated in documentation
- Hard to keep API reference synchronized with code
- Users need comprehensive, current API documentation

**The Solution:**
Chora Compose extracts API information from its own Python source code using AST parsing and generates comprehensive markdown documentation. This ensures docs stay perfectly synchronized with code.

**Benefits:**
1. **Always Current** - Regenerate from actual source code anytime
2. **Single Source of Truth** - Docstrings are the documentation
3. **Type-Safe** - Type hints automatically included
4. **Comprehensive** - All classes, methods, functions documented
5. **Self-Documenting** - Chora Compose documents its own API (dogfooding!)

## Files Overview

```
scripts/
├─ extract_api_data.py       # Extract API info using AST parsing
└─ generate_api_docs.py      # Generate markdown docs from data

configs/
├─ content/api-docs/
│   └─ api-data.json         # Extracted API data (auto-generated)
└─ templates/api-docs/
    └─ module-reference.j2   # Template for module documentation

docs/reference/api-generated/
└─ *.md                      # Generated API reference docs
```

## Quick Start

### Generate API Documentation

```bash
# One command generates everything
poetry run python scripts/generate_api_docs.py
```

This will:
1. Extract API data from `src/chora_compose/`
2. Generate markdown docs for each module
3. Output to `docs/reference/api-generated/`

### Review Generated Docs

```bash
# List generated files
ls docs/reference/api-generated/

# View a generated doc
cat docs/reference/api-generated/core-config_loader.md
```

## How It Works

### Step 1: API Extraction (`extract_api_data.py`)

Uses Python's `ast` module to parse source files:

1. **Parse Python files** → AST (Abstract Syntax Tree)
2. **Walk AST** → Find classes, functions, methods
3. **Extract metadata**:
   - Names, docstrings
   - Parameters with types and defaults
   - Return types
   - Base classes, decorators
4. **Output JSON** → `api-data.json` with all API info

**Example extracted data:**
```json
{
  "classes": [{
    "name": "ConfigLoader",
    "docstring": "Loads and validates Chora Compose configuration files.",
    "methods": [{
      "name": "__init__",
      "parameters": [
        {"name": "schema_dir", "type": "Optional[Path]", "default": "None"}
      ],
      "return_type": "None"
    }]
  }]
}
```

### Step 2: Documentation Generation (`generate_api_docs.py`)

Uses Jinja2 template to render documentation:

1. **Load extracted data** → `api-data.json`
2. **For each module** → Render template
3. **Generate markdown** → Class docs, method signatures, docstrings
4. **Write files** → `docs/reference/api-generated/`

**Template renders:**
- Module overview
- Class documentation with methods
- Function documentation
- Exception documentation
- Type annotations and parameters

## Customizing the Template

Edit `configs/templates/api-docs/module-reference.j2`:

```jinja2
### {{ class.name }}

{{ class.docstring }}

{% for method in class.methods %}
#### `{{ method.name }}`

```python
def {{ method.name }}({{ parameters }}){% if method.return_type %} -> {{ method.return_type }}{% endif %}
```

{{ method.docstring }}
{% endfor %}
```

## Updating Documentation

When code changes:

```bash
# Regenerate docs
poetry run python scripts/generate_api_docs.py

# Review changes
git diff docs/reference/api-generated/

# Copy updated docs to main API docs (if desired)
cp docs/reference/api-generated/core-*.md docs/reference/api/core/
```

## Troubleshooting

### Issue: "Module has no docstring"
**Solution:** Add module-level docstring to Python file:
```python
"""Module description here."""
```

### Issue: "Method parameters missing types"
**Solution:** Add type hints to function signatures:
```python
def method(self, param: str, count: int = 0) -> bool:
    ...
```

### Issue: "Generated docs look incomplete"
**Solution:** Check that docstrings follow standard format (Google/NumPy style)

## Best Practices

1. **Write Good Docstrings** - Documentation quality depends on docstring quality
2. **Use Type Hints** - Add types to all parameters and return values
3. **Include Examples** - Add example usage in docstrings
4. **Keep Docs Updated** - Regenerate after significant code changes
5. **Review Generated Docs** - Always review before committing

## Next Steps

After generating API docs:

1. **Copy to Main Docs** - Move generated docs to `docs/reference/api/`
2. **Add Cross-Links** - Link related classes and modules
3. **Add Examples** - Enhance with usage examples
4. **Generate Index** - Create API index page linking all modules
5. **Automate in CI** - Run generation in CI to catch doc drift

## Related Documentation

- [Feature 1: README Generation](generate-readme.md)
- [Feature 2: Config Examples](generate-config-examples.md)
- [Content Configuration Reference](../../reference/api/core/config-loader.md)

---

**Questions?** See the [Chora Compose Documentation](../../README.md).

**Generated by Phase 2 Dogfooding** | Feature 3: API Documentation Generation
