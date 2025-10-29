# Quick Start Guide - Begin Implementation

**Goal:** Get you started with the first sprint in the next 30 minutes

---

## Immediate Next Steps (Today)

### 1. Review Planning Documents ✅

You now have:
- **[ROADMAP.md](../ROADMAP.md)** - Complete productization strategy (20 weeks, 6 phases)
- **[SPRINT_PLAN.md](SPRINT_PLAN.md)** - Detailed sprint breakdown with story points
- This guide - How to start right now

### 2. Set Up Your Development Branch

```bash
# Create development branch for Sprint 1
git checkout -b sprint-1/schema-foundation

# Create feature branch for first story
git checkout -b feature/convert-content-schema
```

### 3. Choose Your Starting Point

You have **three options** for where to begin:

#### Option A: Schema Conversion (Recommended First)
**Time:** 2-4 hours
**Impact:** Foundation for everything else

Start here: Convert [schemas/content-schema.json](../schemas/content-schema.json) to proper JSON Schema

```bash
# 1. Read the current schema
cat schemas/content-schema.json

# 2. Create new schema directory structure
mkdir -p schemas/content/v3.0
mkdir -p schemas/artifact/v3.0
mkdir -p schemas/common

# 3. Start converting (I can help with this!)
```

#### Option B: Core Engine Skeleton (Parallel Track)
**Time:** 3-5 hours
**Impact:** Foundation for implementation

Set up the core package structure:

```bash
# 1. Create package structure
mkdir -p src/chora_compose/{core,generators,validators,storage,collaboration,cli}

# 2. Create __init__.py files
touch src/chora_compose/__init__.py
touch src/chora_compose/core/__init__.py
touch src/chora_compose/generators/__init__.py
# ... (for all subdirectories)

# 3. Start with config_loader.py (I can help!)
```

#### Option C: MCP Proof of Concept (Explore First)
**Time:** 2-3 hours
**Impact:** See the end goal

Build a minimal MCP server to understand the target:

```bash
# 1. Install MCP SDK
poetry add mcp

# 2. Create minimal server
touch src/chora_compose/mcp/minimal_server.py

# 3. Test with Claude Desktop (I can provide the code!)
```

---

## Recommended First Week Plan

### Day 1 (Today)
- [x] Review roadmap and sprint plan
- [ ] Choose starting point (recommend Option A)
- [ ] Set up development branch
- [ ] Begin schema conversion

### Day 2
- [ ] Complete content schema conversion
- [ ] Start artifact schema conversion
- [ ] Write schema validation tests

### Day 3
- [ ] Complete artifact schema conversion
- [ ] Validate all existing configs against new schemas
- [ ] Create schema documentation

### Day 4
- [ ] Set up core package structure
- [ ] Implement ConfigLoader skeleton
- [ ] Create Pydantic models for configs

### Day 5
- [ ] Complete ConfigLoader implementation
- [ ] Write comprehensive tests
- [ ] Sprint review preparation

---

## What I Can Help You With Right Now

### 1. Schema Conversion
**Say:** "Let's convert the content schema to JSON Schema"
- I'll create the proper JSON Schema v2020-12 format
- Add all validation rules and constraints
- Include examples and documentation

### 2. Core Implementation
**Say:** "Let's build the ConfigLoader class"
- I'll implement the config loading logic
- Add JSON Schema validation
- Create Pydantic models

### 3. MCP Prototype
**Say:** "Let's build a minimal MCP server"
- I'll create a basic MCP server
- Add one or two tools as proof of concept
- Help you test it with Claude Desktop

### 4. Test Setup
**Say:** "Let's set up the test framework"
- I'll configure pytest with coverage
- Create test fixtures
- Write example tests

---

## Decision Points for Today

### Decision 1: Schema Version Format
**Question:** How should we version the schemas?

**Option A: Semantic Versioning (Recommended)**
```
schemas/content/v3.0/schema.json
schemas/content/v3.1/schema.json  # Minor update
schemas/content/v4.0/schema.json  # Breaking change
```

**Option B: Date-Based Versioning**
```
schemas/content/2025-10-10/schema.json
schemas/content/2025-11-15/schema.json
```

**Recommendation:** Option A for better compatibility tracking

### Decision 2: Project Name
**Question:** Should we keep "chora-compose" or rename?

Current: `chora_compose` (Chora Compose framework)

Alternatives:
- `workflow_kernel`
- `ai_workflow`
- `artifact_engine`
- Keep as-is

**Recommendation:** Keep `chora_compose` - it's descriptive and unique

### Decision 3: First Milestone Target
**Question:** What's the concrete goal for Sprint 1?

**Recommended Milestone:** "Generate README.md from configs using new schemas"

Success criteria:
- [ ] Schemas converted to JSON Schema standard
- [ ] ConfigLoader can load and validate configs
- [ ] Basic demonstration generator works
- [ ] Can run: `chora-compose generate readme-artifact`
- [ ] Output matches expected README.md

---

## Quick Command Reference

### Project Setup
```bash
# Install dependencies
poetry install --all-extras

# Activate virtual environment
poetry shell

# Run tests
poetry run pytest

# Run linter
poetry run ruff check .

# Format code
poetry run ruff format .

# Type check
poetry run mypy .
```

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/story-name

# Make changes, then:
git add .
git commit -m "feat: implement X"

# Run pre-commit checks
poetry run pre-commit run --all-files

# Push to remote
git push origin feature/story-name
```

### Testing Commands
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/chora_compose --cov-report=html

# Run specific test file
poetry run pytest tests/unit/test_config_loader.py

# Run with verbose output
poetry run pytest -v

# Run only failed tests
poetry run pytest --lf
```

---

## File Templates

### Template: JSON Schema (Content)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://yourorg.com/schemas/content-schema/v3.0.json",
  "title": "Chora Compose Content Configuration Schema",
  "description": "Defines content configs for ephemeral generation",
  "type": "object",
  "required": ["type", "id", "schemaRef", "metadata", "elements"],
  "additionalProperties": false,
  "properties": {
    "type": {
      "type": "string",
      "const": "content",
      "description": "Discriminator field identifying this as a content config"
    },
    "id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*$",
      "description": "Unique identifier using kebab-case",
      "examples": ["readme-content", "api-docs-content"]
    }
  }
}
```

### Template: Pydantic Model
```python
from pydantic import BaseModel, Field
from typing import Literal

class ContentConfig(BaseModel):
    """Content configuration model"""

    type: Literal["content"] = Field(
        description="Discriminator field"
    )
    id: str = Field(
        pattern=r"^[a-z][a-z0-9-]*$",
        description="Unique identifier using kebab-case"
    )
    # ... rest of fields
```

### Template: Test File
```python
import pytest
from chora_compose.core.config_loader import ConfigLoader

class TestConfigLoader:
    """Tests for ConfigLoader class"""

    @pytest.fixture
    def loader(self):
        return ConfigLoader(schema_dir="schemas")

    def test_load_valid_content_config(self, loader):
        """Should load valid content config successfully"""
        config = loader.load_content_config("readme-content")
        assert config.id == "readme-content"
        assert config.type == "content"

    def test_load_invalid_config_raises_error(self, loader):
        """Should raise ConfigValidationError for invalid config"""
        with pytest.raises(ConfigValidationError):
            loader.load_content_config("invalid-config")
```

---

## Troubleshooting

### Issue: Poetry not found
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: Python version mismatch
```bash
# Check Python version
python --version  # Should be 3.12+

# Use pyenv if needed
pyenv install 3.12
pyenv local 3.12
```

### Issue: Pre-commit hooks failing
```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run manually
poetry run pre-commit run --all-files

# Skip hooks for emergency commit (not recommended)
git commit --no-verify -m "message"
```

---

## Sprint 1 Success Checklist

By the end of Sprint 1 (2 weeks), you should have:

### Week 1
- [ ] Content schema converted to JSON Schema
- [ ] Artifact schema converted to JSON Schema
- [ ] Schema validation tests passing
- [ ] All existing configs validate successfully

### Week 2
- [ ] Core package structure created
- [ ] ConfigLoader implemented and tested
- [ ] Pydantic models for configs
- [ ] Basic demonstration generator
- [ ] Can generate README end-to-end
- [ ] Test coverage >80%

### Sprint 1 Demo
- [ ] Run: `chora-compose generate readme-artifact`
- [ ] Show: Generated README.md matches expected output
- [ ] Show: Validation catches invalid configs
- [ ] Show: Test coverage report

---

## Resources

### Documentation
- [JSON Schema Specification](https://json-schema.org/specification.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)

### Code Examples
- See `examples/` directory for workflow examples
- See `tests/fixtures/` for test data examples

### Getting Help
- GitHub Issues: For bugs and feature requests
- Discussions: For questions and ideas
- This chat: For immediate implementation help!

---

## What to Do Right Now

**Choose one:**

1. **"Let's convert the content schema"** → I'll help you create a proper JSON Schema
2. **"Let's build the config loader"** → I'll implement the core loading logic
3. **"Let's create a minimal MCP server"** → I'll build a proof of concept
4. **"Let's set up the test framework"** → I'll configure pytest and write example tests
5. **"Show me the architecture"** → I'll create architecture diagrams

**Just tell me what you'd like to tackle first!**

---

**Last Updated:** 2025-10-10
**Sprint:** 1 (Schema Foundation)
**Status:** Ready to Begin 🚀
