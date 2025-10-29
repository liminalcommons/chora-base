# Tutorial: Generate Dynamic Content with Jinja2

**Learning Goal:** Master dynamic content generation using Jinja2 templates with runtime variables, conditionals, loops, and filters.

---

## What You'll Learn

By the end of this tutorial, you will:
- Create content configurations using Jinja2 templates
- Pass runtime context variables to templates
- Use conditionals and loops for dynamic structure
- Apply filters to transform data
- Generate multiple variations from a single template

---

## Prerequisites

Before starting, ensure you have:

- [ ] Chora Compose installed (`poetry install`)
- [ ] Python 3.12 or higher
- [ ] Completed [Generate Your First Content](../getting-started/03-generate-your-first-content.md)
- [ ] Basic text editor or IDE

**No Jinja2 experience required** - this tutorial teaches you everything you need.

---

## Time Required

Approximately 25 minutes

---

## Understanding the Difference

### Static Generation (Demonstration Generator)

Fixed content from example_output:

```json
{
  "elements": [{
    "name": "greeting",
    "example_output": "Hello, World!"
  }]
}
```

Output is always: `"Hello, World!"`

### Dynamic Generation (Jinja2 Generator)

Dynamic content from templates + runtime variables:

```jinja2
Hello, {{ name }}!
```

Output depends on context:
- `{"name": "Alice"}` → `"Hello, Alice!"`
- `{"name": "Bob"}` → `"Hello, Bob!"`

**Key differences:**

| Feature | Demonstration | Jinja2 |
|---------|--------------|--------|
| Content source | Fixed examples | Dynamic templates |
| Runtime data | Not supported | Fully supported |
| Conditionals | No | Yes |
| Loops | No | Yes |
| Filters | No | Yes |
| Use case | Simple prototypes | Production content |

---

## Step 1: Create Your First Jinja2 Template

Create a new file `templates/greeting.j2`:

```jinja2
# Greeting for {{ name }}

Hello, {{ name }}!

{% if show_info %}
This message was generated at {{ timestamp }}.
{% endif %}

Your role: {{ role | default("User") }}
```

**Template syntax explained:**

- `{{ name }}` - Variable substitution
- `{% if show_info %}...{% endif %}` - Conditional block (only shows if show_info is true)
- `{{ role | default("User") }}` - Variable with fallback default

**Create the templates directory:**

```bash
mkdir -p templates
```

Save the template file in this directory.

---

## Step 2: Create a Jinja2 Content Configuration

Create `configs/content/dynamic-greeting/dynamic-greeting-content.json`:

```json
{
  "type": "content",
  "id": "dynamic-greeting-content",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Dynamic greeting with Jinja2",
    "version": "1.0",
    "generation_frequency": "on-demand",
    "output_format": "markdown"
  },
  "elements": [
    {
      "name": "greeting-template",
      "description": "Jinja2 template for personalized greeting",
      "format": "jinja2",
      "template_file": "templates/greeting.j2"
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "jinja2-greeting",
        "type": "jinja2",
        "template_source": "file",
        "template_file": "templates/greeting.j2",
        "required_context": ["name"],
        "optional_context": ["show_info", "timestamp", "role"]
      }
    ]
  }
}
```

**Configuration explained:**

- `"type": "jinja2"` - Use the Jinja2 generator
- `"template_source": "file"` - Template comes from an external file
- `"template_file"` - Path to the .j2 template file
- `required_context` - Variables that must be provided at generation time
- `optional_context` - Variables that can be omitted

**Create the configuration directory:**

```bash
mkdir -p configs/content/dynamic-greeting
```

---

## Step 3: Generate Content with Runtime Context

Create a Python script `generate_dynamic.py`:

```python
from pathlib import Path
from datetime import datetime
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

# Load the configuration
loader = ConfigLoader()
config = loader.load_content_config("dynamic-greeting-content")

# Create Jinja2 generator
generator = Jinja2Generator(template_dir=Path("templates"))

# Provide runtime context
context = {
    "name": "Alice",
    "show_info": True,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "role": "Developer"
}

# Generate content
output = generator.generate(config, context=context)

print("=== Generated Content ===")
print(output)
```

**Run the generator:**

```bash
poetry run python generate_dynamic.py
```

**Expected output:**

```markdown
=== Generated Content ===
# Greeting for Alice

Hello, Alice!

This message was generated at 2025-10-15 14:30:45.

Your role: Developer
```

**Success!** You've generated dynamic content with runtime variables.

---

## Step 4: Generate Multiple Variations

Modify your script to generate content for multiple users:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

loader = ConfigLoader()
config = loader.load_content_config("dynamic-greeting-content")
generator = Jinja2Generator(template_dir=Path("templates"))

# Generate for multiple users
users = [
    {"name": "Alice", "role": "Developer", "show_info": True},
    {"name": "Bob", "role": "Designer", "show_info": False},
    {"name": "Charlie", "show_info": False},  # No role - will use default
]

for user_context in users:
    output = generator.generate(config, context=user_context)
    print(f"\n{'='*50}")
    print(output)
```

**Run it:**

```bash
poetry run python generate_dynamic.py
```

**Output:**

```markdown
==================================================
# Greeting for Alice

Hello, Alice!

This message was generated at 2025-10-15 14:30:45.

Your role: Developer

==================================================
# Greeting for Bob

Hello, Bob!

Your role: Designer

==================================================
# Greeting for Charlie

Hello, Charlie!

Your role: User
```

**What's happening:**

- Same configuration and template
- Different context for each generation
- Missing optional variables use defaults or are omitted
- Conditional blocks only appear when their condition is true

---

## Step 5: Add Loops to Your Template

Update `templates/greeting.j2` to include a task list:

```jinja2
# Greeting for {{ name }}

Hello, {{ name }}!

{% if show_info %}
This message was generated at {{ timestamp }}.
{% endif %}

Your role: {{ role | default("User") }}

{% if tasks %}
## Your Tasks

{% for task in tasks %}
- {{ loop.index }}. {{ task }}
{% endfor %}
{% endif %}
```

**New features:**

- `{% for task in tasks %}` - Loop over a list
- `{{ loop.index }}` - Built-in loop counter (starts at 1)
- `{% endfor %}` - End of loop block

Update your generation script:

```python
from pathlib import Path
from datetime import datetime
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

loader = ConfigLoader()
config = loader.load_content_config("dynamic-greeting-content")
generator = Jinja2Generator(template_dir=Path("templates"))

context = {
    "name": "Alice",
    "role": "Developer",
    "show_info": True,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "tasks": [
        "Review pull requests",
        "Update documentation",
        "Fix bug #123"
    ]
}

output = generator.generate(config, context=context)
print(output)
```

**Output:**

```markdown
# Greeting for Alice

Hello, Alice!

This message was generated at 2025-10-15 14:30:45.

Your role: Developer

## Your Tasks

- 1. Review pull requests
- 2. Update documentation
- 3. Fix bug #123
```

**Template power:**

- Dynamic list length (any number of tasks)
- Automatic numbering
- Structure adapts to data

---

## Step 6: Use Jinja2 Filters

Filters transform data in templates. Update `templates/greeting.j2`:

```jinja2
# Greeting for {{ name | title }}

Hello, {{ name | title }}!

Your role: {{ role | default("User") | upper }}

{% if email %}
Contact: {{ email | lower }}
{% endif %}

Member since: {{ join_date | default("Unknown") }}
```

**Common filters:**

- `title` - Capitalize each word
- `upper` - Convert to uppercase
- `lower` - Convert to lowercase
- `default("value")` - Provide fallback value

Generate with:

```python
context = {
    "name": "alice smith",
    "role": "developer",
    "email": "ALICE@EXAMPLE.COM",
    "join_date": "2024-01-15"
}

output = generator.generate(config, context=context)
print(output)
```

**Output:**

```markdown
# Greeting for Alice Smith

Hello, Alice Smith!

Your role: DEVELOPER

Contact: alice@example.com

Member since: 2024-01-15
```

**Filters in action:**

- `alice smith` → `Alice Smith` (title filter)
- `developer` → `DEVELOPER` (upper filter)
- `ALICE@EXAMPLE.COM` → `alice@example.com` (lower filter)

---

## Step 7: Use Inline Templates (Alternative)

Instead of external files, you can use inline templates for simple cases:

```json
{
  "generation": {
    "patterns": [{
      "id": "inline-greeting",
      "type": "jinja2",
      "template_source": "inline",
      "template": "Hello, {{ name }}! Today is {{ day }}.",
      "required_context": ["name", "day"]
    }]
  }
}
```

**When to use inline templates:**

- ✅ Short, simple templates (1-3 lines)
- ✅ No complex logic
- ✅ Embedded in configuration

**When to use file templates:**

- ✅ Long templates (4+ lines)
- ✅ Complex logic (loops, conditionals)
- ✅ Reusable across configs
- ✅ Easier to edit and maintain

---

## Step 8: Generate and Save Multiple Files

Generate personalized files for each user:

```python
from pathlib import Path
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.jinja2 import Jinja2Generator

loader = ConfigLoader()
config = loader.load_content_config("dynamic-greeting-content")
generator = Jinja2Generator(template_dir=Path("templates"))

users = [
    {"name": "Alice", "role": "Developer"},
    {"name": "Bob", "role": "Designer"},
    {"name": "Charlie", "role": "Manager"},
]

# Create output directory
output_dir = Path("output/greetings")
output_dir.mkdir(parents=True, exist_ok=True)

for user_context in users:
    # Generate content
    output = generator.generate(config, context=user_context)

    # Save to individual file
    filename = f"{user_context['name'].lower()}-greeting.md"
    output_file = output_dir / filename
    output_file.write_text(output, encoding="utf-8")

    print(f"✓ Generated {filename}")

print(f"\n✓ All greetings saved to {output_dir}")
```

**Run it:**

```bash
poetry run python generate_dynamic.py
```

**Output:**

```
✓ Generated alice-greeting.md
✓ Generated bob-greeting.md
✓ Generated charlie-greeting.md

✓ All greetings saved to output/greetings
```

**Check the generated files:**

```bash
ls output/greetings/
# alice-greeting.md  bob-greeting.md  charlie-greeting.md

cat output/greetings/alice-greeting.md
# See the personalized content for Alice
```

---

## What You Learned

Congratulations! You've mastered Jinja2 dynamic generation:

- ✅ Created Jinja2 templates with variables and conditionals
- ✅ Configured content to use the Jinja2 generator
- ✅ Passed runtime context to generate dynamic content
- ✅ Used loops to generate lists
- ✅ Applied filters to transform data
- ✅ Generated multiple variations from one template
- ✅ Saved personalized output files

---

## Key Concepts

### Dynamic Generation Workflow

```
Template (structure) + Context (data) → Generator → Output
```

**Template defines:**
- Overall structure
- Variable placeholders
- Conditional sections
- Loop patterns

**Context provides:**
- Actual data values
- Boolean flags
- Lists and objects
- Runtime information

**Generator combines:**
- Evaluates conditionals
- Executes loops
- Applies filters
- Produces final output

### Jinja2 Syntax Reference

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ var }}` | Variable substitution | `{{ name }}` |
| `{% if condition %}` | Conditional block | `{% if active %}...{% endif %}` |
| `{% for item in list %}` | Loop block | `{% for task in tasks %}...{% endfor %}` |
| `{{ var \| filter }}` | Apply filter | `{{ name \| title }}` |
| `{{ var \| default("x") }}` | Default value | `{{ role \| default("User") }}` |

### Advantages Over Static Generation

**One template, many outputs:**
- Generate personalized content for thousands of users
- Maintain one template instead of many files

**Runtime data integration:**
- Pull data from databases, APIs, files
- Generate reports with current data

**Conditional sections:**
- Show/hide content based on context
- Adapt structure to data

**Complex transformations:**
- Format data (dates, numbers, text)
- Filter and sort lists
- Calculate derived values

---

## Troubleshooting

### Error: `TemplateNotFoundError: greeting.j2`

**Cause:** Template file not found

**Solutions:**
1. Check that `templates/` directory exists in project root
2. Verify file is named exactly `greeting.j2` (case-sensitive)
3. Ensure `template_dir` parameter points to correct directory:
   ```python
   generator = Jinja2Generator(template_dir=Path("templates"))
   ```

### Error: `UndefinedError: 'name' is undefined`

**Cause:** Required variable missing from context

**Solutions:**
1. Provide all `required_context` variables in context dict:
   ```python
   context = {"name": "Alice"}  # Include all required variables
   ```
2. Check spelling of variable names (case-sensitive)
3. For optional variables, use defaults in template:
   ```jinja2
   {{ role | default("User") }}
   ```

### Error: Template syntax error

**Cause:** Invalid Jinja2 syntax

**Solutions:**
1. Check that tags are balanced:
   - Every `{% if %}` needs `{% endif %}`
   - Every `{% for %}` needs `{% endfor %}`
2. Use correct delimiters:
   - `{% %}` for statements (if, for, endif, endfor)
   - `{{ }}` for expressions (variables, filters)
3. Check for typos in filter names
4. Validate syntax at [jinja.palletsprojects.com](https://jinja.palletsprojects.com/)

### Output is empty or missing sections

**Cause:** Conditional evaluating to false or missing context

**Solutions:**
1. Check that conditional variables are true:
   ```python
   context = {"show_info": True}  # Not False or missing
   ```
2. Verify loop variables are non-empty lists:
   ```python
   context = {"tasks": ["task1", "task2"]}  # Not empty list []
   ```
3. Add debug output to see context:
   ```python
   print(f"Context: {context}")
   ```

---

## Next Steps

**Continue learning:**

- [How-To: Use Template Inheritance](../../how-to/generation/use-template-inheritance.md) - Create reusable base templates
- [How-To: Debug Jinja2 Templates](../../how-to/generation/debug-jinja2-templates.md) - Advanced debugging techniques
- [Reference: Jinja2 Generator API](../../reference/api-generated/generators/jinja2.md) - Complete API documentation

**Explore advanced topics:**

- [Explanation: Why Jinja2 for Dynamic Generation?](../../explanation/architecture/why-jinja2-for-dynamic-generation.md) - Design rationale
- [Reference: Built-in Jinja2 Filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters) - Official Jinja2 docs

**Build something real:**

- Generate API documentation from OpenAPI specs
- Create personalized email templates
- Build multi-language documentation
- Generate test data files

---

**Tutorial complete!** You now have the skills to create powerful dynamic content generation workflows with Chora Compose and Jinja2.

**Document Version:** 1.0.0
**Last Updated:** 2025-10-15
**Feedback:** [GitHub Issues](https://github.com/liminalcommons/chora-compose/issues)
