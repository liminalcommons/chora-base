# How-To: Generate Config Examples Using Chora Compose

**Skill Level:** Advanced
**Time:** 30 minutes
**Prerequisites:**
- Chora Compose installed
- Understanding of Jinja2 templates
- Understanding of JSON structure
- Completed Feature 1 (README Generation)

## What This Solves

**The Problem:**
- Writing example configs from scratch is time-consuming and error-prone
- Examples become outdated as features evolve
- Hard to maintain consistency across multiple examples
- Documentation needs working, tested examples
- Users struggle to learn without good examples

**The Solution:**
chora-compose generates its own config examples with documentation and scripts from structured specifications. This demonstrates Chora Compose's ability to create Chora Compose configs - true dogfooding!

**Benefits:**
1. **Always Current** - Examples stay synchronized with features
2. **Consistent** - All examples follow the same structure
3. **Complete** - Each example includes config, README, and generation script
4. **Tested** - Generated examples are immediately usable
5. **Data Reuse** - Specs can generate multiple outputs (web docs, tutorials, etc.)
6. **Learning Aid** - Users can study working examples
7. **Self-Documenting** - Chora Compose demonstrates its own capabilities

## Files Overview

```
configs/
├── content/examples/
│   ├── example-specs.json           # Specifications for 5 examples
│   └── examples-content.json        # Links specs + templates
└── templates/examples/
    ├── content-config.j2            # Template for content configs
    ├── README.j2                    # Template for README files
    └── generation-script.j2         # Template for Python scripts

scripts/
└── generate_examples.py             # Automation script

examples/                            # Generated output directory
├── 01-simple-readme/
│   ├── configs/content/simple-readme.json
│   ├── README.md
│   └── generate.py
├── 02-api-documentation/
│   └── ...
└── (more examples)
```

## Step 1: Understanding Example Specifications

The `example-specs.json` file contains structured specifications for each example:

```json
{
  "metadata": {
    "title": "Chora Compose Example Specifications",
    "purpose": "Phase 2 Dogfooding - Chora Compose generating its own config examples"
  },
  "examples": [
    {
      "id": "01-simple-readme",
      "name": "Simple README Generator",
      "skill_level": "Beginner",
      "time_estimate": "10 minutes",
      "category": "documentation",
      "description": "Demonstrates the basics...",
      "learning_objectives": [
        "Understand content config structure",
        "Learn how elements work"
      ],
      "use_case": "Generate a project README from predefined sections",
      "config": {
        "id": "simple-readme",
        "generator_type": "demonstration",
        "elements": [
          {
            "name": "title",
            "description": "Project title and tagline",
            "example_output": "# My Awesome Project..."
          }
        ],
        "template": "{{elements.title.example_output}}..."
      },
      "expected_output": {
        "description": "A complete README.md...",
        "approx_lines": 20,
        "format": "markdown"
      },
      "next_steps": [
        "Try modifying the feature list",
        "Add a new section"
      ]
    }
  ]
}
```

**Key Sections:**

- **id**: Unique identifier (e.g., `01-simple-readme`)
- **name**: Human-readable name
- **skill_level**: Beginner/Intermediate/Advanced
- **learning_objectives**: What users will learn
- **config**: The actual content config structure
  - **generator_type**: `demonstration` or `jinja2`
  - **elements**: For demonstration generator
  - **data**: For Jinja2 generator
- **expected_output**: What gets generated
- **next_steps**: Extension ideas

## Step 2: Generate All Examples

### Basic Generation

```bash
# Generate all examples
poetry run python scripts/generate_examples.py

# Generate specific examples
poetry run python scripts/generate_examples.py --examples 01-simple-readme 02-api-documentation

# Dry run (preview without creating files)
poetry run python scripts/generate_examples.py --dry-run

# Verbose output
poetry run python scripts/generate_examples.py --verbose
```

### Output

```
📂 Loading example specifications...
✅ Loaded 5 example(s)

🔧 Initializing Jinja2Generator...

🚀 Generating examples to: examples

[1/5] Simple README Generator (01-simple-readme)
  → Generating content config...
  → Generating README.md...
  → Generating generate.py...
     ✅ Complete

...

✅ GENERATION COMPLETE
Generated 5 example(s)
```

## Step 3: Review Generated Examples

Each generated example contains:

1. **Content Config** (`configs/content/<id>.json`)
   - Valid JSON content configuration
   - Ready to use with Chora Compose
   - Follows schema v3.1

2. **README.md**
   - Learning objectives
   - Step-by-step walkthrough
   - Customization tips
   - Troubleshooting
   - Next steps

3. **generate.py**
   - Executable Python script
   - Loads config and generates output
   - Clear success messages

## Step 4: Test a Generated Example

```bash
cd examples/01-simple-readme
python generate.py
```

Expected output:
```
📂 Loading config: configs/content/simple-readme.json
✅ Config loaded: Simple README Generator
   Elements: 4

🔧 Generating content with DemonstrationGenerator...

✅ Generation successful!
📄 Output: output.md
📊 Size: 423 characters
📝 Lines: 18
```

## How It Works

### 1. The Automation Script

`generate_examples.py` performs these steps:

1. **Load Specifications** - Read `example-specs.json`
2. **Initialize Generator** - Create Jinja2Generator with templates
3. **For Each Example**:
   - Load example specification
   - Generate content config JSON
   - Generate README.md
   - Generate generate.py script
   - Make script executable
4. **Create Directory Structure** - Organize files

### 2. The Templates

**content-config.j2** - Generates Valid Configs
```jinja2
{
  "type": "content",
  "id": "{{ example.config.id }}",
  "metadata": {
    "description": "{{ example.description }}",
    "version": "1.0.0"
  },
  {% if example.config.generator_type == "demonstration" %}
  "elements": [
    {% for element in example.config.elements %}
    {
      "name": "{{ element.name }}",
      "description": "{{ element.description }}",
      "format": "text",
      "example_output": {{ element.example_output | tojson }}
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ]
  {% endif %}
}
```

**README.j2** - Generates Documentation
- Uses conditional logic for demonstration vs Jinja2 examples
- Loops over learning objectives and next steps
- Includes troubleshooting sections

**generation-script.j2** - Generates Python Scripts
- Proper shebang and imports
- Loads config using ConfigLoader
- Initializes appropriate generator
- Writes output with success messages

## Adding New Examples

### 1. Add Specification to example-specs.json

```json
{
  "id": "06-your-example",
  "name": "Your Example Name",
  "skill_level": "Intermediate",
  "time_estimate": "15 minutes",
  "category": "your-category",
  "description": "What this example demonstrates",
  "learning_objectives": [
    "Objective 1",
    "Objective 2"
  ],
  "use_case": "Your use case description",
  "config": {
    "id": "your-example",
    "generator_type": "demonstration",  // or "jinja2"
    "elements": [
      // For demonstration generator
    ],
    // OR
    "data": {
      // For Jinja2 generator
    },
    "template_file": "your-template.j2"  // For Jinja2
  },
  "expected_output": {
    "description": "What gets generated",
    "approx_lines": 50,
    "format": "markdown"  // or "json", "gherkin", etc.
  },
  "next_steps": [
    "Extension idea 1",
    "Extension idea 2"
  ]
}
```

### 2. Regenerate Examples

```bash
poetry run python scripts/generate_examples.py
```

Your new example will be generated in `examples/06-your-example/`!

## Customizing Templates

### Modify content-config.j2

Add new fields or change formatting:

```jinja2
"metadata": {
  "description": "{{ example.description }}",
  "version": "1.0.0",
  "output_format": "{{ example.expected_output.format }}"
}
```

### Modify README.j2

Add new sections:

```jinja2
## Performance Considerations

{% if example.performance_notes %}
{{ example.performance_notes }}
{% else %}
Standard performance expectations apply.
{% endif %}
```

### Modify generation-script.j2

Add validation or additional output:

```jinja2
# Validate generated output
if len(output) < 100:
    print("⚠️  Warning: Output seems short")

# Write additional formats
json_output = json.dumps({"content": output})
Path("output.json").write_text(json_output)
```

## Troubleshooting

### Issue: "Config validation failed"

**Cause:** Generated config doesn't match schema v3.1

**Solution:**
1. Check template matches schema requirements
2. Validate example spec has all required fields
3. Test with: `python -m json.tool examples/.../config.json`

### Issue: "Template not found"

**Cause:** Jinja2 can't find template file

**Solution:**
1. Verify template exists in `configs/templates/examples/`
2. Check template name in examples-content.json
3. Ensure template_dir path is correct

### Issue: "Undefined variable in template"

**Cause:** Template references field not in example spec

**Solution:**
1. Check example spec has all required fields
2. Use conditional checks: `{% if example.field %}`
3. Provide defaults: `{{ example.field | default('N/A') }}`

### Issue: "Generated script won't execute"

**Cause:** Script not made executable or has syntax errors

**Solution:**
```bash
chmod +x examples/*/generate.py
python -m py_compile examples/*/generate.py
```

## Advanced: Template-Based Examples

For Jinja2-based examples, include template files:

1. Add template to `configs/templates/examples/`
2. Reference in example spec:
   ```json
   "config": {
     "generator_type": "jinja2",
     "template_file": "api-docs.j2",
     "data": { ...data structure... }
   }
   ```
3. Template will be used by generated script

## Best Practices

1. **Start Simple** - Begin with demonstration examples
2. **Test Generated Examples** - Always run generated scripts
3. **Keep Specs Complete** - Include all fields for best documentation
4. **Use Descriptive IDs** - Pattern: `<number>-<descriptive-name>`
5. **Provide Next Steps** - Help users extend examples
6. **Include Learning Objectives** - Make educational value clear
7. **Test Edge Cases** - Verify templates handle all generator types

## Next Steps

After generating config examples:

1. **Use as Learning Materials** - Share with new users
2. **Generate More Examples** - Add advanced examples
3. **Create Web Documentation** - Generate HTML/website from specs
4. **Build Tutorial System** - Use specs for interactive tutorials
5. **Automate Testing** - Run all example scripts in CI/CD
6. **Create Example Gallery** - Build searchable example catalog

## Related Documentation

- [Feature 1: README Generation](generate-readme.md)
- [Jinja2 Generator Guide](../../how-to/generation/use-jinja2-generator.md)
- [Content Configuration Reference](../../reference/api/core/config-loader.md)

---

**Questions?** Open an issue or see the [Chora Compose Documentation](../../README.md).

**Generated by Phase 2 Dogfooding** | Feature 2: Config Examples Generation
