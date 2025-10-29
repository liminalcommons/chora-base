# API Reference Documentation

**Type**: Hand-written, user-friendly API documentation
**Audience**: Developers integrating with chora-compose
**Purpose**: Comprehensive guides with examples, best practices, and context

---

## 📖 About This Documentation

This directory contains **hand-written API reference documentation** designed for developers who want to understand and use chora-compose APIs effectively. Each document includes:

- ✅ Comprehensive overviews
- ✅ Practical examples
- ✅ Best practices and patterns
- ✅ Common use cases
- ✅ Links to related documentation
- ✅ Troubleshooting guidance

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

**When to use**:
- 📚 **Use api/** when: Learning, integrating, understanding concepts
- 🔍 **Use api-generated/** when: Quick lookup, checking signatures

---

## 📂 Directory Structure

```
reference/api/
├── core/                    # Core engine APIs
│   ├── config-loader.md     # Configuration loading
│   └── artifact-composer.md # Artifact composition
│
├── generators/              # Generator APIs
│   ├── jinja2.md           # Jinja2 generator
│   └── demonstration.md    # Demonstration generator
│
├── storage/                 # Storage APIs
│   └── ephemeral-config-manager.md
│
├── telemetry/               # Telemetry APIs
│   ├── event-emitter.md
│   └── event-schemas.md
│
├── mcp/                     # MCP integration
│   └── tool-catalog.md
│
├── models/                  # Data models
│   └── upstream-dependencies.md
│
└── resources/               # MCP resources
    └── capabilities.md
```

---

## 🎯 API Categories

### Core Engine

Essential APIs for loading configs and composing artifacts:

- **[ConfigLoader](core/config-loader.md)** - Load and validate configurations
- **[ArtifactComposer](core/artifact-composer.md)** - Compose multi-part artifacts

### Generators

APIs for content generation strategies:

- **[Jinja2Generator](generators/jinja2.md)** - Template-based generation with logic
- **[DemonstrationGenerator](generators/demonstration.md)** - Example-driven generation

### Storage

APIs for managing ephemeral and persistent storage:

- **[EphemeralConfigManager](storage/ephemeral-config-manager.md)** - Manage draft configs

### Telemetry

APIs for event tracking and observability:

- **[EventEmitter](telemetry/event-emitter.md)** - Emit structured events
- **[Event Schemas](telemetry/event-schemas.md)** - Event data structures

### MCP Integration

APIs for Model Context Protocol features:

- **[Tool Catalog](mcp/tool-catalog.md)** - MCP tool definitions
- **[Capabilities Resource](resources/capabilities.md)** - System capabilities

### Models

Data models and schemas:

- **[Upstream Dependencies](models/upstream-dependencies.md)** - Dependency tracking

---

## 🚀 Quick Start

### Loading a Configuration

```python
from chora_compose.core.config_loader import ConfigLoader

loader = ConfigLoader()
config = loader.load_content_config("my-config-id")

# Or load from path
config = loader.load_content_config_from_path("configs/content/my-config.json")
```

See: [ConfigLoader API](core/config-loader.md)

### Generating Content

```python
from chora_compose.generators.jinja2 import Jinja2Generator

generator = Jinja2Generator()
output = generator.generate(config, context={"name": "Alice"})
```

See: [Jinja2Generator API](generators/jinja2.md)

### Composing Artifacts

```python
from chora_compose.core.artifact_composer import ArtifactComposer

composer = ArtifactComposer()
artifact = composer.compose("artifact-config-id")
```

See: [ArtifactComposer API](core/artifact-composer.md)

---

## 📚 Related Documentation

### For Beginners
- [Quick Start Guide](../../QUICK_START_GUIDE.md) - Get started quickly
- [Tutorials](../../tutorials/) - Step-by-step learning paths

### For Integrators
- [How-To Guides](../../how-to/) - Practical task-oriented guides
- [Auto-generated API Reference](../api-generated/README.md) - Technical reference

### For Architecture Understanding
- [Explanation](../../explanation/) - Conceptual deep dives
- [Config-Driven Architecture](../../explanation/architecture/config-driven-architecture.md)

---

## 🔧 API Stability

| Status | Meaning | APIs |
|--------|---------|------|
| ✅ **Stable** | Production-ready, breaking changes only with major version | ConfigLoader, ArtifactComposer, Jinja2Generator |
| ⚠️ **Beta** | Functional but may change in minor versions | EphemeralConfigManager |
| 🚧 **Experimental** | Subject to change without notice | (None currently) |

**Versioning**: chora-compose follows [Semantic Versioning 2.0.0](https://semver.org/).

---

## 📝 Documentation Standards

All API docs in this directory follow these standards:

1. **Structure**: Overview → Classes/Functions → Examples → Best Practices
2. **Code Examples**: Real, runnable code snippets
3. **Cross-References**: Links to related docs (tutorials, how-tos, explanations)
4. **Type Hints**: Full type signatures for all APIs
5. **Error Handling**: Common errors and solutions

---

## 🤝 Contributing

Found an issue or want to improve these docs?

- **Errors/Typos**: Submit PR with fix
- **Missing Examples**: Open issue with use case
- **New APIs**: Add hand-written doc following existing structure
- **Auto-generated Docs**: See [api-generated/README.md](../api-generated/README.md)

See: [CONTRIBUTING.md](../../../CONTRIBUTING.md)

---

## 📊 Coverage

| Category | Hand-written Docs | Auto-generated Docs | Coverage |
|----------|------------------|---------------------|----------|
| Core | 2 docs | 3 docs | 67% |
| Generators | 2 docs | 3 docs | 67% |
| Storage | 1 doc | 0 docs | 100% |
| Telemetry | 2 docs | 0 docs | 100% |
| MCP | 1 doc | 0 docs | 100% |
| **Total** | **10 docs** | **6 docs** | **80%** |

**Goal**: Achieve 100% coverage for all stable APIs by v2.0.0

---

**Last Updated**: 2025-10-21
**Maintained By**: chora-compose documentation team
**Diataxis Category**: Reference (Information-Oriented)
