# Auto-Generated API Reference

**Type**: Auto-generated from Python docstrings
**Audience**: Developers needing quick reference
**Purpose**: Technical specifications and function signatures

---

## ⚙️ About This Documentation

This directory contains **auto-generated API documentation** created directly from Python docstrings in the codebase. These docs are:

- ✅ Always up-to-date with code
- ✅ Technically precise
- ✅ Generated automatically
- ⚠️ Minimal examples
- ⚠️ Less context than hand-written docs

**Generation Process**: These docs are generated using automated tools that parse Python docstrings and type hints.

---

## 🔀 api/ vs api-generated/

| Aspect | **api/** (Hand-written) | **api-generated/** (Auto-generated) |
|--------|-------------------------|-------------------------------------|
| **Source** | Written by humans | Generated from docstrings |
| **Content** | Comprehensive, contextual | Technical, precise |
| **Examples** | Real-world use cases | Minimal |
| **Audience** | All developers | Reference lookup |
| **Updates** | Manual, curated | Automated from code |
| **Best For** | Learning, integration | Quick reference |

**Recommendation**:
- 📚 **Start with [api/](../api/README.md)** for learning and understanding
- 🔍 **Use api-generated/** for quick signature lookups

---

## 📂 Available Documentation

### Core Modules

- **[core-config_loader.md](core-config_loader.md)** - Configuration loading
- **[core-composer.md](core-composer.md)** - Artifact composition
- **[core-models.md](core-models.md)** - Core data models

### Generators

- **[generators-base.md](generators-base.md)** - Base generator interface
- **[generators-jinja2.md](generators-jinja2.md)** - Jinja2 generator
- **[generators-demonstration.md](generators-demonstration.md)** - Demonstration generator

---

## 🔄 Keeping Docs in Sync

### Auto-generation Process

```bash
# Generate API docs from code (example - actual command may vary)
python scripts/generate_api_docs.py

# Output: docs/reference/api-generated/*.md
```

**When docs are regenerated**:
- Before major releases
- After significant API changes
- On-demand when docstrings updated

**Note**: These docs may lag slightly behind latest code. For the absolute truth, consult the source code.

---

## 📝 Documentation Format

Auto-generated docs follow this structure:

```markdown
# module_name.submodule

> **File:** `src/path/to/file.py`

Module description from docstring.

## Classes

### ClassName

Class description.

**Methods:**

#### `method_name`

```python
def method_name(self, param: Type) -> ReturnType
```

Method description.

**Parameters:**
- `param` (Type) - Parameter description

**Returns:**
- ReturnType - Return value description
```

---

## ⚠️ Limitations

These auto-generated docs have limitations:

1. **Minimal Examples**: Code examples may be absent or minimal
2. **Less Context**: Missing "why" and "when to use" guidance
3. **No Cross-References**: Limited links to related documentation
4. **Technical Focus**: Assumes familiarity with codebase

**For comprehensive documentation**, see [hand-written API docs](../api/README.md).

---

## 🎯 When to Use Auto-Generated Docs

**Use api-generated/ when**:
- ✅ Quick signature lookup ("What parameters does this function take?")
- ✅ Type checking ("What does this function return?")
- ✅ Confirming docstring accuracy
- ✅ Cross-referencing with IDE

**Use [api/](../api/README.md) when**:
- ✅ Learning how to use an API
- ✅ Understanding design decisions
- ✅ Finding practical examples
- ✅ Integrating with chora-compose

---

## 🔗 Related Documentation

### Hand-Written API Docs
- **[api/ README](../api/README.md)** - Comprehensive API documentation

### Source Code
- **[src/chora_compose/](../../../src/chora_compose/)** - Python source code
- **Docstrings**: The source of truth for this auto-generated documentation

### For Users
- [How-To Guides](../../how-to/) - Task-oriented guides
- [Tutorials](../../tutorials/) - Learning-oriented lessons
- [Explanation](../../explanation/) - Understanding-oriented articles

---

## 🤝 Improving Auto-Generated Docs

Want better auto-generated docs? **Improve the docstrings!**

### Good Docstring Example

```python
def load_content_config(self, config_id: str) -> ContentConfig:
    """Load a content configuration by ID.

    Args:
        config_id: Unique identifier for the configuration

    Returns:
        Validated ContentConfig instance

    Raises:
        ConfigNotFoundError: If config file doesn't exist
        ValidationError: If config fails validation

    Example:
        >>> loader = ConfigLoader()
        >>> config = loader.load_content_config("my-config")
    """
```

### Contributing Improvements

1. **Add/improve docstrings** in source code
2. **Submit PR** with enhanced docstrings
3. **Regenerate docs** (maintainers will do this)
4. **Documentation automatically improves**

See: [CONTRIBUTING.md](../../../CONTRIBUTING.md)

---

## 📊 Coverage

| Module | Classes | Functions | Documented |
|--------|---------|-----------|------------|
| core.config_loader | 1 | 5+ | ✅ |
| core.composer | 1 | 3+ | ✅ |
| core.models | 5+ | - | ✅ |
| generators.base | 1 | - | ✅ |
| generators.jinja2 | 1 | 3+ | ✅ |
| generators.demonstration | 1 | 2+ | ✅ |

**Total**: 6 modules documented

**Note**: Not all modules have auto-generated docs. For complete coverage, see [api/README.md](../api/README.md).

---

## 🔍 Finding What You Need

### Quick Lookup Table

| I want to... | File |
|--------------|------|
| Load a config | [core-config_loader.md](core-config_loader.md) |
| Compose an artifact | [core-composer.md](core-composer.md) |
| Use Jinja2 generator | [generators-jinja2.md](generators-jinja2.md) |
| Understand data models | [core-models.md](core-models.md) |
| Create custom generator | [generators-base.md](generators-base.md) |

### Search Tips

**In this directory**:
```bash
# Find all mentions of a function
grep -r "function_name" docs/reference/api-generated/

# Find all classes
grep -r "^### " docs/reference/api-generated/
```

**Better approach**: Use hand-written docs in [api/](../api/README.md) with comprehensive indexes.

---

## ⚖️ Source of Truth

**Order of precedence** (most authoritative first):

1. **Source Code** (`src/chora_compose/`) - Absolute truth
2. **Auto-generated Docs** (this directory) - Derived from docstrings
3. **Hand-written Docs** ([api/](../api/README.md)) - May lag slightly but provide context

**For critical integrations**: Always verify against source code.

---

**Last Updated**: Auto-generated on each release
**Generation Tool**: Python docstring parser (specific tool TBD)
**Maintained By**: Automated process + docstring contributors
**Diataxis Category**: Reference (Information-Oriented)
