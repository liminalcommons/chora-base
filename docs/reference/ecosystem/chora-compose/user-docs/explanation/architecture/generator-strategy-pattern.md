# Generator Strategy Pattern

> **Purpose:** Understand why Chora Compose uses the Strategy Pattern for content generation and how it enables extensibility.

## The Problem

Content generation has different requirements depending on the use case:

- **Static content assembly:** Combine pre-written sections (documentation, templates)
- **Dynamic templating:** Fill templates with runtime data (personalized messages, reports)
- **AI-powered generation:** Create new content based on prompts (code, documentation)
- **Code generation:** Produce source code from specifications (API clients, tests)
- **Multi-pass processing:** Complex pipelines with validation and transformation

**Challenge:** How do you support all these scenarios without creating a monolithic, inflexible generator?

### Attempted Monolithic Approach

```python
class ContentGenerator:
    def generate(self, config, mode="static", ai_prompt=None, template_vars=None):
        if mode == "static":
            # Handle static generation
            pass
        elif mode == "template":
            # Handle template generation
            pass
        elif mode == "ai":
            # Handle AI generation
            pass
        elif mode == "code":
            # Handle code generation
            pass
        # ...endless if/elif chains
```

**Problems:**
- ❌ Violates Single Responsibility Principle (does too much)
- ❌ Hard to test (many code paths)
- ❌ Difficult to extend (modify existing code for new types)
- ❌ Tight coupling (all logic in one place)
- ❌ Parameter explosion (different modes need different params)

---

## The Solution: Strategy Pattern

**Strategy Pattern** defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategies let the algorithm vary independently from clients that use it.

In Chora Compose:
- **Strategy**: Different generation algorithms (Demonstration, Jinja2, AI, etc.)
- **Context**: Content config specifies which strategy to use
- **Client**: ArtifactComposer or user code that calls generators

### Architecture

```
┌─────────────────────────┐
│  GeneratorStrategy      │  Abstract base class
│  (ABC)                  │
├─────────────────────────┤
│ + generate(config)      │  Interface all strategies implement
└─────────────────────────┘
           △
           │ Inheritance
           │
    ┌──────┴──────┬──────────────┬────────────┐
    │             │              │            │
┌───┴───────┐ ┌──┴────────┐ ┌───┴──────┐ ┌──┴──────────┐
│Demonst... │ │Jinja2Gen  │ │AIGen     │ │CustomGen    │
├───────────┤ ├───────────┤ ├──────────┤ ├─────────────┤
│Static     │ │Template   │ │Prompt    │ │External     │
│examples   │ │rendering  │ │based     │ │tool         │
└───────────┘ └───────────┘ └──────────┘ └─────────────┘
```

**Key Insight:** Each generator implements the same interface but uses completely different logic internally.

---

## How It Works in Chora Compose

### 1. Abstract Base Class

```python
# src/chora_compose/generators/base.py

from abc import ABC, abstractmethod
from chora_compose.core.models import ContentConfig

class GeneratorStrategy(ABC):
    """Abstract base for all generators."""

    @abstractmethod
    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        """Generate content - each strategy implements differently."""
        pass

    def _extract_element_data(self, config: ContentConfig) -> dict[str, str]:
        """Common utility - available to all strategies."""
        return {elem.name: elem.example_output or "" for elem in config.elements}
```

**Benefits:**
- Defines contract: All generators must implement `generate()`
- Provides common utilities: Shared helper methods
- Type safety: Code can depend on `GeneratorStrategy` type

### 2. Concrete Strategies

**Strategy 1: DemonstrationGenerator**

```python
# src/chora_compose/generators/demonstration.py

class DemonstrationGenerator(GeneratorStrategy):
    """Static example-based generation."""

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Find demonstration pattern
        pattern = self._find_demo_pattern(config)

        # Extract examples from elements
        elements = self._extract_element_data(config)

        # Substitute into template
        return self._substitute_template(pattern.template, elements)
```

**Strategy 2: Jinja2Generator** (planned)

```python
# src/chora_compose/generators/jinja2.py

class Jinja2Generator(GeneratorStrategy):
    """Dynamic template-based generation."""

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Load Jinja2 template
        template = self._load_template(config)

        # Render with runtime context
        return template.render(context or {})
```

**Strategy 3: AIGenerator** (future)

```python
# src/chora_compose/generators/ai.py

class AIGenerator(GeneratorStrategy):
    """AI-powered content generation."""

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Build prompt from config
        prompt = self._build_prompt(config, context)

        # Call AI API
        return self._call_ai_api(prompt)
```

**Each strategy is independent** - adding new ones doesn't change existing code.

### 3. Strategy Selection

Configs specify which strategy to use:

```json
{
  "generation": {
    "patterns": [
      {
        "id": "my-pattern",
        "type": "demonstration",  // Selects DemonstrationGenerator
        "template": "...",
        "variables": [...]
      }
    ]
  }
}
```

Or:

```json
{
  "generation": {
    "patterns": [
      {
        "type": "jinja2",  // Selects Jinja2Generator
        "template_file": "template.j2"
      }
    ]
  }
}
```

### 4. Client Usage

Clients (like ArtifactComposer) use strategies without knowing implementation details:

```python
# src/chora_compose/core/composer.py

class ArtifactComposer:
    def __init__(self):
        # Registry of available strategies
        self.generators = {
            GenerationType.DEMONSTRATION: DemonstrationGenerator(),
            GenerationType.JINJA2: Jinja2Generator(),
            # Add more as they're implemented
        }

    def _generate_content(self, config: ContentConfig) -> str:
        # Get pattern type from config
        pattern = config.generation.patterns[0]
        generator_type = pattern.type

        # Select appropriate strategy
        generator = self.generators[generator_type]

        # Use strategy (don't care about implementation)
        return generator.generate(config)
```

**Benefits:**
- Composer doesn't know how each generator works
- Adding new strategies requires minimal changes to Composer
- Strategies can be swapped at runtime

---

## Why This Approach?

### Reason 1: Open/Closed Principle

**Open for extension, closed for modification.**

**Adding a new generator:**

1. Create new class inheriting from `GeneratorStrategy`
2. Implement `generate()` method
3. Register in ArtifactComposer
4. Done - no existing code modified

```python
# New custom generator
class CustomGenerator(GeneratorStrategy):
    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Your custom logic
        return custom_generation_logic(config)

# Register it
composer.generators[GenerationType.CUSTOM] = CustomGenerator()
```

**Without Strategy Pattern:** Would need to modify ContentGenerator class, adding more if/elif branches.

### Reason 2: Single Responsibility

Each generator has one job:

- **DemonstrationGenerator:** Extract examples and substitute
- **Jinja2Generator:** Render Jinja2 templates
- **AIGenerator:** Call AI APIs

**Testing is easier:**
```python
def test_demonstration_generator():
    """Test only demonstration logic."""
    generator = DemonstrationGenerator()
    config = create_test_config()
    output = generator.generate(config)
    assert output == expected

def test_jinja2_generator():
    """Test only Jinja2 logic."""
    generator = Jinja2Generator()
    config = create_test_config_with_jinja2()
    output = generator.generate(config)
    assert "{{" not in output  # Verify substitution happened
```

### Reason 3: Flexibility and Composition

Mix and match strategies within one artifact:

```json
{
  "content": {
    "children": [
      {
        "id": "static-intro",
        "pattern_type": "demonstration"  // Uses DemonstrationGenerator
      },
      {
        "id": "dynamic-api-docs",
        "pattern_type": "jinja2"  // Uses Jinja2Generator
      },
      {
        "id": "ai-generated-examples",
        "pattern_type": "ai"  // Uses AIGenerator
      }
    ]
  }
}
```

Each child can use a different strategy - they compose naturally.

### Reason 4: Testability

Mock strategies easily for testing:

```python
class MockGenerator(GeneratorStrategy):
    """Test double for generation testing."""

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        return "MOCKED OUTPUT"

# Use in tests
def test_artifact_composer():
    composer = ArtifactComposer()
    composer.generators[GenerationType.DEMONSTRATION] = MockGenerator()

    output = composer.assemble("test-artifact")
    assert "MOCKED OUTPUT" in output
```

### Reason 5: Runtime Selection

Choose strategies at runtime based on conditions:

```python
def choose_generator(config: ContentConfig) -> GeneratorStrategy:
    """Select generator based on config properties."""

    if config.metadata.get("use_ai"):
        return AIGenerator()
    elif has_template_file(config):
        return Jinja2Generator()
    else:
        return DemonstrationGenerator()

# Use selected strategy
generator = choose_generator(config)
output = generator.generate(config)
```

---

## Alternatives Considered

### Alternative 1: Inheritance Hierarchy

**Approach:**
```python
class ContentGenerator:
    def generate(self, config):
        return self._do_generate(config)

class StaticGenerator(ContentGenerator):
    def _do_generate(self, config):
        # Static logic

class TemplateGenerator(ContentGenerator):
    def _do_generate(self, config):
        # Template logic
```

**Pros:**
- ✅ Some code reuse via inheritance

**Cons:**
- ❌ Tight coupling between parent and children
- ❌ Hard to compose (can only inherit from one class)
- ❌ Fragile base class problem (changing parent affects all children)

**Why rejected:** Composition over inheritance. Strategy Pattern uses composition.

### Alternative 2: Function-Based

**Approach:**
```python
def generate_static(config):
    # Static logic

def generate_template(config):
    # Template logic

def generate_ai(config):
    # AI logic

# Dispatch
generators = {
    "static": generate_static,
    "template": generate_template,
    "ai": generate_ai,
}

output = generators[config.type](config)
```

**Pros:**
- ✅ Simple and pythonic
- ✅ Easy to understand

**Cons:**
- ❌ No shared state or utilities
- ❌ Harder to test (functions instead of classes)
- ❌ No inheritance/interface enforcement
- ❌ Less IDE support (no class-based autocomplete)

**Why rejected:** Need structure for complex generators with shared utilities and state.

### Alternative 3: Plugin System

**Approach:**
```python
class PluginRegistry:
    def register(self, name, generator_class):
        self.plugins[name] = generator_class

# External plugins
registry.register("custom", MyCustomGenerator)
```

**Pros:**
- ✅ Ultimate flexibility
- ✅ External extensibility

**Cons:**
- ❌ Added complexity
- ❌ Discovery mechanism needed
- ❌ Version compatibility issues
- ❌ Overkill for current needs

**Why rejected:** Strategy Pattern provides enough extensibility without plugin complexity. Could evolve to plugins later if needed.

---

## Trade-offs

### Trade-off 1: Simplicity vs. Extensibility

**What we gave up:**
- Single simple class (monolithic generator)
- Direct function calls

**What we gained:**
- Multiple specialized classes
- Unlimited extensibility
- Clean separation of concerns

**Why it's worth it:**
- Complexity is bounded (each strategy is simple)
- Extensibility is critical for growth
- Pattern is well-understood in industry

### Trade-off 2: Performance vs. Flexibility

**What we gave up:**
- Slight overhead from strategy dispatch
- Registry lookup

**What we gained:**
- Runtime strategy selection
- Mockability for testing
- Composability

**Why it's worth it:**
- Overhead is negligible (< 1ms)
- Generation itself is slow (file I/O, AI calls)
- Flexibility benefits outweigh tiny cost

### Trade-off 3: Boilerplate vs. Type Safety

**What we gave up:**
- Some boilerplate (abstract base class)
- Explicit interface definition

**What we gained:**
- Type safety (mypy can check)
- Clear contracts
- IDE autocomplete

**Why it's worth it:**
- Boilerplate is minimal
- Type safety prevents bugs
- Developer experience improved

---

## Real-World Impact

### Before Strategy Pattern

Hypothetical monolithic approach:

```python
def generate(config, mode="static"):
    if mode == "static":
        # ... 100 lines ...
    elif mode == "template":
        # ... 150 lines ...
    # Hard to test, hard to extend
```

**Pain points:**
- Can't test strategies independently
- Adding new mode requires modifying core function
- Risk breaking existing modes when adding new ones

### After Strategy Pattern

```python
class DemonstrationGenerator(GeneratorStrategy):
    def generate(self, config):
        # ... 40 lines of focused logic ...

class Jinja2Generator(GeneratorStrategy):
    def generate(self, config):
        # ... 60 lines of focused logic ...
```

**Improvements:**
- Each strategy tested independently
- New strategies added without touching existing code
- Clear separation of concerns
- Easy to understand and maintain

---

## Future Extensibility

The Strategy Pattern enables planned features:

### Custom External Generators

```python
class ExternalToolGenerator(GeneratorStrategy):
    """Delegate to external command-line tool."""

    def __init__(self, tool_path: Path):
        self.tool_path = tool_path

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        # Write config to temp file
        # Call external tool
        # Read output
        return output
```

### Multi-Stage Generators

```python
class PipelineGenerator(GeneratorStrategy):
    """Chain multiple generators."""

    def __init__(self, stages: list[GeneratorStrategy]):
        self.stages = stages

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        result = ""
        for stage in self.stages:
            result = stage.generate(config, {"previous_output": result})
        return result
```

### Validation-Enabled Generators

```python
class ValidatingGenerator(GeneratorStrategy):
    """Generator that validates output."""

    def __init__(self, inner: GeneratorStrategy, validator: Validator):
        self.inner = inner
        self.validator = validator

    def generate(self, config: ContentConfig, context: dict | None = None) -> str:
        output = self.inner.generate(config, context)
        self.validator.validate(output)
        return output
```

All possible because of the Strategy Pattern foundation.

---

## Key Takeaways

After reading this, you should understand:

1. **The pattern:** Strategy Pattern encapsulates algorithms and makes them interchangeable
2. **The problem:** Different generation needs require different algorithms
3. **The solution:** Abstract base class + concrete strategy implementations
4. **Why this way:** Extensibility, testability, single responsibility
5. **Trade-offs:** Slight complexity for major flexibility gains

**Remember:**
- Each generator is independent and focused
- Adding generators doesn't modify existing code
- Strategies compose naturally
- Pattern enables future growth

---

## See Also

### Internal Documentation

- [DemonstrationGenerator API Reference](../../reference/api/generators/demonstration.md) - Concrete strategy
- [Tutorial: Generate Your First Content](../../tutorials/getting-started/03-generate-your-first-content.md) - See strategy in action
- [How to: Use Demonstration Generator](../../how-to/generation/use-demonstration-generator.md) - Practical usage
- [Config-Driven Architecture](config-driven-architecture.md) - Related architectural decision

### External Resources

- [Strategy Pattern (Gang of Four)](https://en.wikipedia.org/wiki/Strategy_pattern) - Original pattern definition
- [Strategy Pattern in Python](https://refactoring.guru/design-patterns/strategy/python/example) - Python-specific examples
- [Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle) - SOLID principle

### Design Patterns

- **Template Method Pattern** - Alternative using inheritance
- **Factory Pattern** - Often used with Strategy for object creation
- **Decorator Pattern** - For wrapping strategies (like ValidatingGenerator example)
