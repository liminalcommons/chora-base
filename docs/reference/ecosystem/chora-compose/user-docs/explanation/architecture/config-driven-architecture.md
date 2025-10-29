# Config-Driven Architecture

> **Purpose:** Understand why Chora Compose uses configuration over code and the benefits this architectural approach provides.

## The Problem

Traditional content generation faces several challenges:

**Hard-coded content generation:**
```python
def generate_readme():
    title = "# My Project"
    description = "This is my project."
    installation = "## Installation\n\nnpm install"
    # ... hard-coded strings everywhere

    return f"{title}\n\n{description}\n\n{installation}"
```

**Problems:**
- ❌ Changes require code modifications
- ❌ Non-developers can't update content
- ❌ No reusability across projects
- ❌ Hard to version content separately from code
- ❌ Content and structure tightly coupled
- ❌ Testing requires code changes

**Template-only approaches:**
```jinja2
{# README.j2 #}
# {{ title }}

{{ description }}

## Installation

{{ installation_instructions }}
```

**Problems:**
- ❌ Structure still in templates (code)
- ❌ No validation of template variables
- ❌ Hard to compose from multiple sources
- ❌ Limited metadata and constraints
- ❌ No machine-readable structure definition

---

## The Solution: Configuration-Driven Architecture

**Configuration-driven** means the system's behavior is defined primarily through data (configuration files) rather than code.

In Chora Compose:
- **What to generate** → Defined in configs
- **Structure and relationships** → Defined in configs
- **Validation rules** → Defined in configs
- **Generation strategies** → Selected in configs
- **Dependencies and metadata** → Tracked in configs

**Code's role:** Generic, reusable processors that interpret configs.

### Architecture Diagram

```
Configs (Data)                   Code (Processors)
     ↓                                 ↓
┌──────────────┐              ┌──────────────┐
│ Content      │──────────────→│ ConfigLoader │
│ Config JSON  │              │ (Validates)  │
└──────────────┘              └──────────────┘
                                      ↓
┌──────────────┐              ┌──────────────┐
│ Artifact     │──────────────→│ Generator    │
│ Config JSON  │              │ (Processes)  │
└──────────────┘              └──────────────┘
                                      ↓
┌──────────────┐              ┌──────────────┐
│ JSON Schema  │──────────────→│ Composer     │
│ (Validation) │              │ (Assembles)  │
└──────────────┘              └──────────────┘
                                      ↓
                              ┌──────────────┐
                              │ Output File  │
                              └──────────────┘
```

**Key insight:** Configs are first-class citizens. Code is generic infrastructure.

---

## How It Works in Chora Compose

### Layer 1: Schema (The Contract)

JSON Schemas define what valid configs look like:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://chora-compose.org/schemas/content/v3.1/schema.json",
  "title": "Content Configuration Schema",
  "type": "object",
  "required": ["type", "id", "metadata", "elements"],
  "properties": {
    "type": {"const": "content"},
    "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
    "elements": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/$defs/ContentElement"}
    }
  }
}
```

**Benefits:**
- Machine-readable contract
- Validation before processing
- Tool-independent (any language can validate)
- Versioned (v3.0 → v3.1)

### Layer 2: Configs (The Data)

Configs are instances conforming to schemas:

**Content config:**
```json
{
  "type": "content",
  "id": "readme-content",
  "elements": [
    {
      "name": "introduction",
      "format": "markdown",
      "example_output": "# Welcome"
    }
  ],
  "generation": {
    "patterns": [{
      "type": "demonstration",
      "template": "{{introduction}}",
      "variables": [...]
    }]
  }
}
```

**Artifact config:**
```json
{
  "type": "artifact",
  "id": "readme-artifact",
  "content": {
    "children": [
      {"id": "readme-content", "path": "...", "order": 1}
    ]
  },
  "metadata": {
    "outputs": [{"file": "README.md"}],
    "compositionStrategy": "concat"
  }
}
```

**Benefits:**
- Declarative (what, not how)
- Versionable (git-friendly JSON)
- Composable (artifacts reference content)
- Portable (can move between systems)

### Layer 3: Code (The Processors)

Code is generic and reusable:

```python
# ConfigLoader: Generic config processor
loader = ConfigLoader()
config = loader.load_content_config("any-config-id")  # Works for any valid config

# Generator: Strategy pattern - swappable
generator = DemonstrationGenerator()  # or Jinja2Generator, AIGenerator, etc.
output = generator.generate(config)

# Composer: Generic orchestrator
composer = ArtifactComposer()
result = composer.assemble("any-artifact-id")  # Works for any valid artifact
```

**Code never hard-codes:**
- Content strings
- File paths (reads from configs)
- Structure (defined in configs)
- Dependencies (tracked in configs)

---

## Why This Approach?

### Reason 1: Separation of Concerns

**Clear boundaries:**
- **Configs:** Define WHAT and WHEN
- **Schemas:** Define structure and constraints
- **Code:** Define HOW

**Example:**

**Config says WHAT:**
```json
{
  "id": "api-docs",
  "outputs": [{"file": "docs/API.md"}],
  "children": [
    {"id": "endpoints", "order": 1},
    {"id": "authentication", "order": 2}
  ]
}
```

**Code says HOW:**
```python
def assemble(artifact_id):
    config = load_config(artifact_id)  # Generic
    children = sort_by_order(config.children)  # Generic
    contents = [generate(child) for child in children]  # Generic
    return compose(contents, config.strategy)  # Generic
```

**Benefits:**
- Change WHAT without changing code
- Change HOW without changing configs
- Test code with many configs
- Test configs without changing code

### Reason 2: Non-Developer Accessibility

**Config-driven systems enable non-developers:**

```json
{
  "elements": [
    {
      "name": "welcome-message",
      "example_output": "Welcome to our API!"
    }
  ]
}
```

A technical writer can:
- ✅ Update `example_output` directly
- ✅ Change element order
- ✅ Add new sections
- ✅ Modify metadata

Without touching code or understanding Python.

**Traditional code-driven:**
```python
def generate():
    return "Welcome to our API!"  # Requires code change
```

Non-developer must:
- ❌ Find the right file
- ❌ Understand Python syntax
- ❌ Avoid breaking code
- ❌ Run tests

### Reason 3: Reusability and Composition

**Configs are composable:**

```
content/
  intro/intro-content.json
  features/features-content.json
  usage/usage-content.json

artifacts/
  readme-artifact.json         → uses [intro, features, usage]
  user-guide-artifact.json     → uses [intro, usage]
  marketing-artifact.json      → uses [intro, features]
```

**Same content, multiple artifacts:**
- No code duplication
- DRY (Don't Repeat Yourself)
- Single source of truth per content piece

**Code-driven equivalent:**
```python
def generate_readme():
    return intro() + features() + usage()

def generate_user_guide():
    return intro() + usage()  # Duplicate function calls

def generate_marketing():
    return intro() + features()  # More duplication
```

### Reason 4: Versioning and Evolution

**Configs version independently:**

```
configs/
  v1.0/
    readme-content.json
  v2.0/
    readme-content.json  # Updated content, same code
```

**Schema evolution:**

```
schemas/
  content/
    v3.0/schema.json
    v3.1/schema.json  # Backward-compatible changes
```

**Code handles multiple versions:**
```python
loader = ConfigLoader()
config = loader.load_content_config("readme-content")  # Auto-detects version
```

**Benefits:**
- Content evolves without code changes
- Schemas evolve with migration paths
- Old configs still work (if compatible)
- Clear deprecation path

### Reason 5: Testability

**Config-driven systems are easier to test:**

**Test with many configs:**
```python
@pytest.mark.parametrize("config_id", [
    "readme-content",
    "api-docs-content",
    "user-guide-content",
    # ... dozens more
])
def test_generation(config_id):
    loader = ConfigLoader()
    config = loader.load_content_config(config_id)
    generator = DemonstrationGenerator()

    output = generator.generate(config)

    assert output  # Works for ANY valid config
```

**Test configs independently:**
```python
def test_readme_config_valid():
    """Config is valid without running code."""
    loader = ConfigLoader()
    config = loader.load_content_config("readme-content")

    assert config.id == "readme-content"
    assert len(config.elements) > 0
    # No generation needed to test config
```

**Code-driven equivalent:**
Each config requires custom test code.

### Reason 6: Introspection and Tooling

**Configs are data - easy to analyze:**

```python
# List all artifacts and their outputs
for artifact_file in Path("configs/artifacts").glob("*.json"):
    config = loader.load_artifact_config(artifact_file.stem)
    print(f"{config.id} → {config.metadata.outputs[0].file}")

# Find all content using a specific format
for content_file in Path("configs/content").rglob("*.json"):
    config = loader.load_config(content_file)
    if any(e.format == "python" for e in config.elements):
        print(f"Python content: {config.id}")
```

**Can build tools:**
- Config validators
- Dependency analyzers
- Migration helpers
- Documentation generators (from configs!)
- IDEs and editors

**Code-driven systems:** Hard to introspect, requires parsing code.

---

## Trade-offs

### Trade-off 1: Flexibility vs Simplicity

**What we gave up:**
- Direct code manipulation
- Full programming language power
- Inline logic

**What we gained:**
- Declarative simplicity
- Non-developer accessibility
- Validation guarantees

**Why it's worth it:**
- 90% of use cases don't need code
- Complex cases: extend with custom generators
- Configs easier to understand than code

**When it's not:** Extremely dynamic scenarios better suited to code (but can still use Jinja2 or AI generators).

### Trade-off 2: Verbosity vs Explicitness

**What we gave up:**
- Concise code
- Implicit behavior

**What we gained:**
- Explicit configuration
- Self-documenting structure
- Clear contracts

**Config example (verbose):**
```json
{
  "type": "content",
  "id": "intro-content",
  "schemaRef": {...},
  "metadata": {...},
  "elements": [...]
}
```

**Code equivalent (concise):**
```python
content = Content(id="intro", elements=[...])
```

**Why it's worth it:**
- Explicitness prevents errors
- Machine-readable structure
- Validation catches mistakes
- Clear intent for future readers

### Trade-off 3: Upfront Structure vs Quick Iteration

**What we gave up:**
- Quick prototyping (must create configs)
- Rapid iteration (schema constraints)

**What we gained:**
- Structured from day one
- Validated before execution
- Consistent patterns

**Why it's worth it:**
- Small upfront cost
- Huge long-term maintainability
- Prevents technical debt

**Mitigation:** Provide templates and generators for common config patterns.

---

## Real-World Impact

### Before: Code-Driven

**Example:** Generate README for projects

```python
# readme_generator.py (hard-coded)
def generate_readme(project_name: str, description: str):
    return f"""# {project_name}

{description}

## Installation

npm install {project_name}

## Usage

const {project_name} = require('{project_name}');
"""

# generate_project_readme.py
readme = generate_readme("my-app", "My application")
Path("README.md").write_text(readme)
```

**Pain points:**
- Every project needs custom script
- Structure changes require code modifications
- Non-developers can't update
- Hard to test variations

### After: Config-Driven

**Example:** Same README generation

**Config:** `configs/content/readme/readme-content.json`
```json
{
  "elements": [
    {"name": "title", "example_output": "# My App"},
    {"name": "description", "example_output": "My application"},
    {"name": "installation", "example_output": "## Installation\n\nnpm install my-app"},
    {"name": "usage", "example_output": "## Usage\n\nconst myApp = require('my-app');"}
  ],
  "generation": {
    "patterns": [{
      "template": "{{title}}\n\n{{description}}\n\n{{installation}}\n\n{{usage}}"
    }]
  }
}
```

**Usage:**
```python
# One line for any project
composer = ArtifactComposer()
composer.assemble("readme-artifact")
```

**Improvements:**
- ✅ Non-developers update `example_output`
- ✅ Same code works for all projects
- ✅ Version configs in git
- ✅ Test with multiple configs
- ✅ Validate before generation

---

## Alternatives Considered

### Alternative 1: Pure Code (No Configs)

**Approach:**
```python
class ReadmeGenerator:
    def __init__(self, title, description, installation, usage):
        self.title = title
        self.description = description
        # ...

    def generate(self):
        return f"{self.title}\n\n{self.description}..."
```

**Pros:**
- ✅ Full Python power
- ✅ IDE support
- ✅ Type checking

**Cons:**
- ❌ Code changes for content updates
- ❌ Not accessible to non-developers
- ❌ Hard to compose
- ❌ No declarative validation

**Why rejected:** Couples content to code, loses flexibility.

### Alternative 2: Pure Templates (No Structure)

**Approach:**
```jinja2
{# README.j2 #}
# {{ title }}

{{ description }}

## Installation

{{ installation }}
```

**Pros:**
- ✅ Separate content from code
- ✅ Familiar to many

**Cons:**
- ❌ No structure validation
- ❌ No composition support
- ❌ No metadata
- ❌ Template is still code

**Why rejected:** Insufficient structure and validation.

### Alternative 3: Database-Driven

**Approach:**
```sql
CREATE TABLE content_elements (
    id INT,
    name VARCHAR(255),
    content TEXT
);
```

**Pros:**
- ✅ Centralized storage
- ✅ Query capabilities

**Cons:**
- ❌ Not version-control friendly
- ❌ Requires database setup
- ❌ No file-based workflows
- ❌ Complex for simple cases

**Why rejected:** Overkill for content generation, poor git integration.

### Alternative 4: YAML Configs

**Approach:**
```yaml
type: content
id: readme-content
elements:
  - name: title
    example_output: "# My App"
```

**Pros:**
- ✅ More readable than JSON
- ✅ Comments supported

**Cons:**
- ❌ No standard schema validation (JSON Schema is JSON)
- ❌ Whitespace-sensitive (error-prone)
- ❌ Less tool support

**Why rejected:** JSON Schema standard + better tooling outweighs readability.

---

## When to Use Config-Driven Architecture

### Ideal For:

✅ **Structured content generation**
- Documentation
- Reports
- Code generation from specs

✅ **Repetitive patterns**
- Multiple similar outputs
- Template-based workflows

✅ **Collaborative environments**
- Non-developers contribute content
- Subject matter experts own content

✅ **Versioned content**
- Content evolves independently
- Multiple versions coexist

✅ **Compliance and audit**
- Need traceability
- Validation requirements

### Not Ideal For:

❌ **One-off scripts**
- Quick throwaway code
- No reuse expected

❌ **Highly dynamic logic**
- Complex business rules
- Algorithmic content (use code or AI)

❌ **Simple cases**
- Single static file
- No variation needed

---

## Key Takeaways

After reading this, you should understand:

1. **The approach:** Configs define behavior, code processes configs
2. **The benefits:** Separation, reusability, testability, non-developer access
3. **The trade-offs:** Verbosity, upfront structure, less flexibility
4. **When to use:** Structured, reusable, collaborative content
5. **How it works:** Schemas validate, configs declare, code processes

**Remember:**
- Configs are first-class, not second-class
- Code is infrastructure, not content
- Declarative beats imperative for structure
- Composition over hard-coding

---

## See Also

### Internal Documentation

- [Tutorial: Your First Config](../../tutorials/getting-started/02-your-first-config.md) - See configs in action
- [How to: Create Content Config](../../how-to/configs/create-content-config.md) - Build configs
- [ConfigLoader API Reference](../../reference/api/core/config-loader.md) - How configs are processed
- [ArtifactComposer API Reference](../../reference/api/core/artifact-composer.md) - Orchestration
- [Generator Strategy Pattern](generator-strategy-pattern.md) - How processing is pluggable
- [Why Two-Layer Validation](why-two-layer-validation.md) - Config validation approach

### External Resources

- [The Twelve-Factor App: Config](https://12factor.net/config) - Config principles
- [JSON Schema Specification](https://json-schema.org/) - Schema standard
- [Declarative vs Imperative Programming](https://en.wikipedia.org/wiki/Declarative_programming) - Programming paradigms
- [Domain-Specific Languages](https://en.wikipedia.org/wiki/Domain-specific_language) - Related concepts
