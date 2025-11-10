# SAP-018: Chora-Compose Meta

**Version:** 2.0.0 | **Status:** Active | **Maturity:** Production

> Complete architecture for chora-compose content generation framework—24 MCP tools across 7 categories, 5 generators, 3-tier collections (Content → Artifact → Collection), SHA-256 caching, and stigmergic context links.

---

## 🚀 Quick Start (2 minutes)

```bash
# Install chora-compose
pip install chora-compose

# Generate content from config
chora-compose generate --config content-config.yaml

# List available generators
chora-compose list-generators

# Validate content freshness
chora-compose check-freshness content-123

# Generate collection
chora-compose generate-collection --config collection-config.yaml
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete setup (15-min read)

---

## 📖 What Is SAP-018?

SAP-018 provides the **complete technical specification for chora-compose**, a content generation framework with 24 MCP tools, 5 built-in generators (demonstration, jinja2, template_fill, bdd_scenario, code_generation), and 3-tier collections architecture (Content → Artifact → Collection) with context propagation and SHA-256 caching.

**Key Innovation**: **3-tier collections architecture** with stigmergic context links—compose atomic content units into artifacts, then artifacts into collections, with automatic dependency tracking and freshness validation.

---

## 🎯 When to Use

Use SAP-018 when you need to:

1. **Understand chora-compose architecture** - Complete technical specification
2. **Build custom generators** - Extend BaseGenerator interface
3. **Implement collections** - Multi-tier content composition
4. **Debug chora-compose** - Trace dependencies, validate configs
5. **Integrate via MCP** - 24 tools for AI agent access

**Not needed for**: Basic chora-compose usage (see SAP-017), or if already familiar with architecture

---

## ✨ Key Features

- ✅ **24 MCP Tools** - 7 categories (generation, config, storage, discovery, validation, collections, utility)
- ✅ **5 Built-in Generators** - demonstration, jinja2, template_fill, bdd_scenario, code_generation
- ✅ **3-Tier Collections** - Content → Artifact → Collection with context propagation
- ✅ **SHA-256 Caching** - Avoid redundant generation (collection members)
- ✅ **Stigmergic Context Links** - Freshness tracking for dependent content
- ✅ **6 Context Sources** - inline_data, external_file, git_reference, content_config, artifact_config, ephemeral_output
- ✅ **3 Execution Strategies** - Parallel, sequential, mixed
- ✅ **OpenTelemetry Events** - content_generated, artifact_assembled, validation_completed

---

## 📚 Quick Reference

### 24 MCP Tools (7 Categories)

#### **Category 1: Core Generation (5 tools)**

- `choracompose:generate_content` - Generate from content config
- `choracompose:assemble_artifact` - Assemble from artifact config
- `choracompose:regenerate_content` - Force regeneration (bypass cache)
- `choracompose:preview_generation` - Dry-run (no file write)
- `choracompose:batch_generate` - Generate multiple configs

---

#### **Category 2: Config Lifecycle (4 tools)**

- `choracompose:draft_config` - Create config from scratch
- `choracompose:test_config` - Validate config without generation
- `choracompose:modify_config` - Update existing config
- `choracompose:save_config` - Persist config to file

---

#### **Category 3: Storage Management (2 tools)**

- `choracompose:cleanup_ephemeral` - Delete ephemeral outputs (session cleanup)
- `choracompose:delete_content` - Delete generated content by ID

---

#### **Category 4: Discovery (6 tools)**

- `choracompose:list_generators` - Show all available generators
- `choracompose:list_content` - List generated content
- `choracompose:list_artifacts` - List assembled artifacts
- `choracompose:trace_dependencies` - Show dependency graph
- `choracompose:list_content_configs` - List all content configs
- `choracompose:list_artifact_configs` - List all artifact configs

---

#### **Category 5: Validation (2 tools)**

- `choracompose:validate_content` - Check content integrity
- `choracompose:check_freshness` - Verify content is up-to-date (stigmergic links)

---

#### **Category 6: Collection Operations (4 tools)**

- `choracompose:generate_collection` - Generate collection from config
- `choracompose:validate_collection_config` - Validate collection config
- `choracompose:list_collection_members` - Show collection contents
- `choracompose:check_collection_cache` - Verify SHA-256 cache status

---

#### **Category 7: Utility (1 tool)**

- `choracompose:hello_world` - Health check / connectivity test

---

### 5 Built-in Generators

#### **1. demonstration** - Example Generator

Simple passthrough generator for testing.

```yaml
generator: demonstration
inputs:
  message: "Hello, World!"
```

---

#### **2. jinja2** - Jinja2 Template Rendering

Render Jinja2 templates with context data.

```yaml
generator: jinja2
inputs:
  template: "Hello, {{ name }}!"
context:
  name: "Alice"
```

---

#### **3. template_fill** - Simple Variable Substitution

Replace `{{ var }}` placeholders (no logic).

```yaml
generator: template_fill
inputs:
  template: "User: {{ username }}, Email: {{ email }}"
context:
  username: "alice"
  email: "alice@example.com"
```

---

#### **4. bdd_scenario** - BDD Scenario Generation

Generate BDD scenarios from structured input.

```yaml
generator: bdd_scenario
inputs:
  feature: "User Login"
  scenarios:
    - name: "Successful login"
      steps:
        - given: "user on /login"
        - when: "user enters valid credentials"
        - then: "user redirected to dashboard"
```

---

#### **5. code_generation** - Code Scaffolding

Generate code from templates (functions, classes, modules).

```yaml
generator: code_generation
inputs:
  language: "python"
  template: "function"
  name: "calculate_total"
  params: ["items", "tax_rate"]
```

---

### 3-Tier Collections Architecture

#### **Tier 1: Content** (Atomic)

Single generated output from one generator.

```yaml
# content-config.yaml
name: "API Documentation"
generator: jinja2
inputs:
  template: "# API Docs\n\n{{ content }}"
context:
  content: "..."
output_path: "docs/api.md"
```

---

#### **Tier 2: Artifact** (Composed)

Multiple content units assembled together.

```yaml
# artifact-config.yaml
name: "Complete Documentation"
members:
  - content_config: "intro.yaml"
  - content_config: "api.yaml"
  - content_config: "examples.yaml"
output_path: "docs/complete.md"
assembly_strategy: "concatenate"
```

---

#### **Tier 3: Collection** (Orchestrated)

Multiple artifacts with dependencies and caching.

```yaml
# collection-config.yaml
name: "Full Documentation Set"
members:
  - artifact_config: "user-docs.yaml"
  - artifact_config: "dev-docs.yaml"
  - artifact_config: "api-docs.yaml"
execution_strategy: "parallel"
cache_strategy: "sha256"
context_propagation: "MERGE"
```

---

### Context Propagation Modes

#### **MERGE** (Default)

Child configs inherit parent context, child overrides win on conflicts.

```yaml
# Parent context: {user: "admin", role: "superuser"}
# Child context: {user: "alice"}
# Result: {user: "alice", role: "superuser"}
```

---

#### **OVERRIDE**

Child context completely replaces parent context.

```yaml
# Parent context: {user: "admin", role: "superuser"}
# Child context: {user: "alice"}
# Result: {user: "alice"}
```

---

#### **ISOLATE**

Child context is independent (no inheritance).

```yaml
# Parent context: {user: "admin", role: "superuser"}
# Child context: {user: "alice"}
# Result: {user: "alice"}
```

---

### Execution Strategies

#### **Parallel** (Default)

Generate all members concurrently (faster, no guaranteed order).

```yaml
execution_strategy: "parallel"
```

**Use Case**: Independent members with no dependencies

---

#### **Sequential**

Generate members one-by-one in declared order (slower, guaranteed order).

```yaml
execution_strategy: "sequential"
```

**Use Case**: Dependent members (later members reference earlier outputs)

---

#### **Mixed**

Parallel within groups, sequential between groups.

```yaml
execution_strategy: "mixed"
groups:
  - members: ["intro.yaml", "overview.yaml"]  # Parallel group 1
  - members: ["api.yaml", "examples.yaml"]    # Parallel group 2 (after group 1)
```

**Use Case**: Complex dependency graphs with parallelization opportunities

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-017** (Chora-Compose Integration) | Deployment | 4 modalities (pip, MCP, CLI, Docker) for chora-compose access |
| **SAP-007** (Documentation Framework) | Content Generation | Generate Diátaxis docs with chora-compose |
| **SAP-014** (MCP Server Development) | MCP Tools | 24 chora-compose tools accessible via MCP |
| **SAP-029** (SAP Generation) | SAP Scaffolding | Generate SAP artifacts with chora-compose |

---

## 🏆 Success Metrics

- **24 MCP Tools**: 100% protocol compliance (MCP 2024-11-05)
- **5 Generators**: Extensible via BaseGenerator interface
- **3-Tier Collections**: Content → Artifact → Collection composition
- **SHA-256 Caching**: Avoid redundant generation (collection members)
- **Stigmergic Links**: Freshness tracking for dependent content

---

## 🔧 Troubleshooting

**Problem**: Generator not found

**Solution**: List available generators:
```bash
chora-compose list-generators
# Output: demonstration, jinja2, template_fill, bdd_scenario, code_generation
```

---

**Problem**: Collection generation fails with cache errors

**Solution**: Clear cache and regenerate:
```bash
chora-compose cleanup-ephemeral
chora-compose generate-collection --config collection.yaml --force
```

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete technical specification (122KB, 60-min read)
- **[AGENTS.md](AGENTS.md)** - Agent chora-compose workflows (18KB, 9-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (16KB, 8-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Setup guide (58KB, 29-min read)
- **[custom-generator-tutorial.md](custom-generator-tutorial.md)** - Build custom generators (46KB, 23-min read)
- **[architecture-overview.md](architecture-overview.md)** - System architecture (26KB, 13-min read)

---

**Version History**:
- **2.0.0** (2025-11-04) - Added collections architecture, stigmergic context links, 24 MCP tools
- **1.0.0** (2025-09-01) - Initial chora-compose Meta specification

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
