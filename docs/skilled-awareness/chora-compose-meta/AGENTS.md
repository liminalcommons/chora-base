---
sap_id: SAP-018
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: advanced
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-220"   # Quick Reference + Core Understanding
  phase_2: "lines 221-420" # Architecture Deep Dive
  phase_3: "full"          # Complete including ecosystem
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 11500
---

# chora-compose Meta (SAP-018) - Agent Awareness

**SAP ID**: SAP-018
**Last Updated**: 2025-11-05
**Audience**: Generic AI Coding Agents

---

## Quick Reference

### When to Use

**Use chora-compose meta (SAP-018) when**:
- Understanding chora-compose architecture deeply
- Making technology decisions (Docker Compose vs alternatives)
- Designing multi-service development environments
- Contributing to chora-compose internals
- Building ecosystem tooling around chora-compose
- Evaluating chora-compose for organization adoption

**Don't use when**:
- Just integrating chora-compose (use SAP-017 instead)
- Simple Docker Compose usage (use SAP-011)
- Production Kubernetes deployments (different system)
- Need step-by-step integration guide (use SAP-017)

### Key Concepts

- **MCP-Native**: Built on Model Context Protocol for LLM integration
- **Configuration-Driven**: All behavior controlled via YAML config
- **Observable**: Comprehensive logging, tracing, metrics
- **Modular**: 17 MCP tools, 5 resource families
- **Access Modalities**: pip, SAP, MCP server, API

### Architecture Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **MCP Server** | Tool interface for LLMs | FastMCP framework |
| **Template Engine** | Content generation | Jinja2 templates |
| **Provider Layer** | LLM abstraction | Anthropic, OpenAI APIs |
| **Config Manager** | YAML validation | Pydantic schemas |
| **Observer** | Logging/metrics | Structured JSON logs |

---

## User Signal Patterns

### Meta-Documentation Operations

| User Says | Formal Action | Resource | Notes |
|-----------|---------------|----------|-------|
| "explain chora-compose architecture" | show_architecture() | protocol-spec.md | System design |
| "why chora-compose" | show_design_philosophy() | capability-charter.md | Design rationale |
| "compare to Kubernetes" | show_ecosystem_positioning() | capability-charter.md | Alternatives |
| "how to extend" | show_contribution_guide() | awareness-guide.md | Extension patterns |
| "MCP tools available" | list_mcp_tools() | protocol-spec.md | 17 tools catalog |
| "chora-compose vs Tilt" | compare_alternatives() | capability-charter.md | Ecosystem position |

### Common Variations

**Architecture Understanding**:
- "explain architecture" / "how does it work" / "system design" → show_architecture()
- "design philosophy" / "why this approach" / "guiding principles" → show_design_philosophy()

**Ecosystem Positioning**:
- "compare to X" / "vs Kubernetes" / "alternatives" → show_ecosystem_positioning()
- "when to use" / "use cases" / "appropriate for" → show_use_cases()

---

## Common Workflows

### Workflow 1: Understanding Architecture (10-15 minutes)

**User signal**: "Explain chora-compose architecture", "How does it work", "System design"

**Purpose**: Understand complete system architecture and components

**Steps**:
1. Read architecture overview:
   ```bash
   # Section 2: Architectural Principles
   cat docs/skilled-awareness/chora-compose-meta/protocol-spec.md | grep -A 50 "Architectural Principles"
   ```

2. Key architectural principles:
   - **Configuration-Driven**: All behavior via YAML config
   - **MCP-Native**: Built on Model Context Protocol
   - **Observable**: Comprehensive logging and tracing
   - **Modular**: 17 MCP tools, pluggable components

3. Component breakdown:
   ```
   chora-compose/
   ├── MCP Server Layer (FastMCP framework)
   │   ├── 17 MCP tools (generate, validate, list, etc.)
   │   └── 5 resource URI families
   ├── Template Engine (Jinja2)
   │   ├── Template discovery
   │   ├── Variable injection
   │   └── Output formatting
   ├── Provider Layer
   │   ├── Anthropic Claude API
   │   ├── OpenAI API
   │   └── Provider abstraction
   ├── Config Manager
   │   ├── YAML schema validation
   │   ├── Environment variable resolution
   │   └── Config merging (global + local)
   └── Observer
       ├── Structured logging (JSON)
       ├── Request/response tracing
       └── Token usage metrics
   ```

4. Integration points:
   - **pip**: Direct Python package installation
   - **MCP Server**: Claude Desktop integration
   - **SAP**: chora-base project integration
   - **API**: Programmatic access (future)

**Expected outcome**: Complete understanding of chora-compose architecture

---

### Workflow 2: Design Philosophy and Trade-offs (5-10 minutes)

**User signal**: "Why chora-compose", "Design philosophy", "Guiding principles"

**Purpose**: Understand design rationale and trade-off decisions

**Steps**:
1. Read design philosophy:
   ```bash
   cat docs/skilled-awareness/chora-compose-meta/capability-charter.md | grep -A 30 "Design Philosophy"
   ```

2. Core principles:
   - **Composition over Configuration**: Compose files declarative
   - **DX-First**: Developer experience prioritized
   - **Explicit Trade-offs**: Performance vs simplicity documented
   - **Standards-Based**: Docker Compose standard, not custom format

3. Trade-off examples:

   **Trade-off 1: Docker Compose vs Kubernetes**
   - **Chosen**: Docker Compose
   - **Rationale**: Simpler for development, local-first
   - **Trade-off**: Less production-ready than K8s
   - **When to reconsider**: Large-scale production deployment

   **Trade-off 2: YAML Config vs Code**
   - **Chosen**: YAML configuration
   - **Rationale**: Declarative, version-controllable, testable
   - **Trade-off**: Less flexible than Python code
   - **When to reconsider**: Complex custom logic needed

   **Trade-off 3: MCP-Native vs REST API**
   - **Chosen**: MCP-first architecture
   - **Rationale**: Standard LLM tool interface, discoverable
   - **Trade-off**: Tied to MCP ecosystem
   - **When to reconsider**: Non-LLM integrations primary use case

4. Design influences:
   - Docker Compose patterns (2015-2025 evolution)
   - MCP Protocol (2024 standard)
   - Tilt, Skaffold (comparison, learning)
   - DevContainers (inspiration for development focus)

**Expected outcome**: Understand why design decisions made, trade-offs accepted

---

### Workflow 3: MCP Tools Catalog (5 minutes)

**User signal**: "MCP tools available", "What tools exist", "List capabilities"

**Purpose**: Understand all 17 MCP tools and their purposes

**Steps**:
1. Read MCP tools catalog:
   ```bash
   cat docs/skilled-awareness/chora-compose-meta/protocol-spec.md | grep -A 100 "MCP Tool Catalog"
   ```

2. Tool categories:

   **Content Generation (6 tools)**:
   - `generate_content`: Generate from template
   - `generate_batch`: Batch generation
   - `generate_with_context`: Context-aware generation
   - `stream_generation`: Real-time streaming
   - `validate_output`: Output validation
   - `format_content`: Format markdown/JSON

   **Template Management (4 tools)**:
   - `list_templates`: Discover available templates
   - `get_template`: Retrieve template content
   - `validate_template`: Template syntax validation
   - `create_template`: New template creation

   **Configuration (3 tools)**:
   - `get_config`: Retrieve current config
   - `validate_config`: Config schema validation
   - `update_config`: Modify configuration

   **Observability (4 tools)**:
   - `get_metrics`: Token usage, generation stats
   - `trace_request`: Request/response tracing
   - `list_logs`: Query structured logs
   - `health_check`: System health status

3. Resource URI families:
   - `template://` - Template access
   - `config://` - Configuration access
   - `log://` - Log access
   - `metric://` - Metrics access
   - `output://` - Generated content access

**Expected outcome**: Know all available tools and when to use each

---

### Workflow 4: Ecosystem Positioning (10 minutes)

**User signal**: "Compare to Kubernetes", "chora-compose vs Tilt", "Alternatives"

**Purpose**: Understand when to use chora-compose vs alternatives

**Steps**:
1. Read ecosystem comparison:
   ```bash
   cat docs/skilled-awareness/chora-compose-meta/capability-charter.md | grep -A 50 "Ecosystem Positioning"
   ```

2. Comparison matrix:

   | Tool | Use Case | Complexity | Best For |
   |------|----------|------------|----------|
   | **chora-compose** | Development env | Low | Local dev, AI agents |
   | **Kubernetes** | Production orchestration | High | Production, scale |
   | **Tilt** | Dev env + K8s preview | Medium | K8s-bound dev |
   | **Skaffold** | CI/CD + K8s deploy | Medium | CI/CD pipelines |
   | **DevContainers** | VS Code integration | Low | VS Code users |

3. Decision criteria:

   **Use chora-compose when**:
   - ✅ Local development environment (primary use case)
   - ✅ AI agent orchestration with MCP
   - ✅ Multi-service Python projects
   - ✅ Docker Compose experience in team
   - ✅ Simple deployment needs

   **Use Kubernetes when**:
   - ⚠️ Production orchestration at scale
   - ⚠️ Complex networking/security requirements
   - ⚠️ Multi-region deployments
   - ⚠️ Advanced rolling updates/canary

   **Use Tilt when**:
   - ⚠️ Kubernetes-bound development
   - ⚠️ Need hot reloading for K8s manifests
   - ⚠️ Local-to-production parity critical

4. Migration paths:
   - **From chora-compose → Kubernetes**: Production readiness
   - **From Docker Compose → chora-compose**: Add MCP integration
   - **From Tilt → chora-compose**: Simplify dev env

**Expected outcome**: Clear understanding of when to use chora-compose vs alternatives

---

### Workflow 5: Contributing to chora-compose (15-20 minutes)

**User signal**: "How to extend", "Contribution guide", "Add new feature"

**Purpose**: Understand contribution patterns and extension points

**Steps**:
1. Read contribution guidelines:
   ```bash
   cat docs/skilled-awareness/chora-compose-meta/awareness-guide.md | grep -A 50 "Contribution Patterns"
   ```

2. Extension points:

   **Extension Point 1: New MCP Tool**
   - Location: `chora_compose/tools/`
   - Pattern: Inherit from `BaseTool`
   - Registration: Add to `MCP_TOOLS` registry
   - Testing: Unit tests + integration tests

   **Extension Point 2: New Provider**
   - Location: `chora_compose/providers/`
   - Pattern: Implement `Provider` interface
   - Configuration: Add to YAML schema
   - Testing: Mock provider tests

   **Extension Point 3: New Template Type**
   - Location: `templates/<type>/`
   - Pattern: Jinja2 templates with frontmatter
   - Validation: JSON schema for variables
   - Documentation: README.md in template dir

3. Contribution workflow:
   ```bash
   # 1. Fork chora-compose repository
   # 2. Create feature branch
   git checkout -b feature/new-mcp-tool

   # 3. Implement feature (e.g., new MCP tool)
   # 4. Write tests
   pytest tests/tools/test_new_tool.py

   # 5. Update documentation
   # 6. Submit pull request
   ```

4. Testing requirements:
   - Unit tests (pytest)
   - Integration tests (MCP server)
   - Type checking (mypy)
   - Linting (ruff)
   - Documentation (docstrings)

**Expected outcome**: Ready to contribute to chora-compose or build extensions

---

## Best Practices

### Practice 1: Read Meta-Documentation Before Integration

**Pattern**:
```markdown
# BEFORE integrating chora-compose:
1. Read SAP-018 (this SAP) - Architecture, philosophy, trade-offs
2. Decide if chora-compose appropriate for use case
3. THEN read SAP-017 - Integration guide
```

**Why**: Understand system before committing to integration

---

### Practice 2: Use MCP Inspector for Tool Discovery

**Pattern**:
```bash
# Launch MCP inspector
npx @modelcontextprotocol/inspector uvx chora-compose

# Discover tools interactively
# Test tool calls before coding
```

**Why**: Visual tool discovery, interactive testing

---

### Practice 3: Understand Trade-offs Before Customization

**Pattern**:
```markdown
# Before customizing chora-compose:
1. Read design trade-offs (SAP-018 protocol-spec)
2. Understand why current approach chosen
3. Consider if customization breaks design principles
```

**Why**: Avoid breaking architectural assumptions

---

### Practice 4: Follow MCP Standards for Extensions

**Pattern**:
```python
# When adding new MCP tool:
from chora_compose.tools import BaseTool
from pydantic import BaseModel

class MyToolInput(BaseModel):
    # Follow MCP parameter schema patterns
    param: str

class MyTool(BaseTool):
    name = "my_tool"
    description = "Clear, concise description for LLM"

    async def run(self, input: MyToolInput) -> str:
        # Implement tool logic
        pass
```

**Why**: Consistent with MCP protocol, discoverable by LLMs

---

### Practice 5: Document Architectural Decisions

**Pattern**:
```markdown
# When making architectural changes:
# Document in ADR (Architecture Decision Record)
# Include: Context, Decision, Rationale, Trade-offs, Alternatives
```

**Why**: Future maintainers understand design evolution

---

## Common Pitfalls

### Pitfall 1: Using chora-compose for Production Orchestration

**Problem**: Try to use chora-compose for production K8s-level orchestration

**Fix**: Use Kubernetes for production

```markdown
# ❌ BAD: chora-compose for production scale
# chora-compose designed for development, not production orchestration

# ✅ GOOD: chora-compose for dev, Kubernetes for production
# Development: chora-compose (simple, fast)
# Production: Kubernetes (robust, scalable)
```

**Why**: chora-compose optimized for dev DX, not production reliability

---

### Pitfall 2: Not Reading Design Philosophy Before Customization

**Problem**: Customize chora-compose without understanding trade-offs

**Fix**: Read design philosophy first

```markdown
# Before customizing:
1. Read SAP-018 protocol-spec (design principles)
2. Understand trade-offs
3. Check if customization aligns with philosophy
```

**Why**: Customizations may break architectural assumptions

---

### Pitfall 3: Treating MCP Tools as REST API

**Problem**: Try to use MCP tools like REST endpoints

**Fix**: Understand MCP protocol semantics

```markdown
# ❌ BAD: Treat MCP tools as HTTP endpoints
# MCP has specific request/response format, not REST

# ✅ GOOD: Use MCP SDK or follow MCP spec
# Use FastMCP client, follow MCP protocol
```

**Why**: MCP has different semantics than REST (SSE, streaming, etc.)

---

### Pitfall 4: Ignoring Observability Infrastructure

**Problem**: Don't use logging/tracing when debugging

**Fix**: Use built-in observability

```bash
# Check structured logs
cat logs/chora-compose.jsonl | jq '.level=="ERROR"'

# Trace specific request
# Look for trace_id in logs
cat logs/chora-compose.jsonl | jq 'select(.trace_id=="abc123")'
```

**Why**: Observability infrastructure designed for debugging

---

### Pitfall 5: Not Understanding Provider Abstraction

**Problem**: Tightly couple to Anthropic API, miss provider abstraction

**Fix**: Use provider abstraction layer

```python
# ✅ GOOD: Use provider abstraction
from chora_compose.providers import get_provider

provider = get_provider("anthropic")  # or "openai"
response = await provider.generate(prompt)
```

**Why**: Provider abstraction enables switching between APIs

---

## Integration with Other SAPs

### SAP-017 (chora-compose-integration)
- SAP-018 provides architecture, SAP-017 provides integration guide
- Read SAP-018 first (understand), then SAP-017 (integrate)

### SAP-011 (docker-operations)
- chora-compose built on Docker Compose
- SAP-011 covers Docker basics, SAP-018 covers chora-compose architecture

### SAP-016 (mcp-server-development)
- MCP server development patterns
- Integration: chora-compose is MCP server, follows MCP patterns

---

## Support & Resources

**SAP-018 Documentation**:
- [Capability Charter](capability-charter.md) - Philosophy, ecosystem positioning
- [Protocol Spec](protocol-spec.md) - Complete architecture specification
- [Awareness Guide](awareness-guide.md) - Contribution patterns, extension points
- [Adoption Blueprint](adoption-blueprint.md) - Learning path
- [Ledger](ledger.md) - Adoption tracking

**chora-compose Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose)
- [MCP Protocol Spec](https://spec.modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

**Related SAPs**:
- [SAP-017 (chora-compose-integration)](../chora-compose-integration/) - Integration guide
- [SAP-011 (docker-operations)](../docker-operations/) - Docker basics
- [SAP-016 (mcp-server-development)](../mcp-server-development/) - MCP patterns

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-018
  - 5 workflows: Architecture, Design Philosophy, MCP Tools, Ecosystem Positioning, Contributing
  - 1 user signal pattern table (Meta-Documentation Operations)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-017, SAP-011, SAP-016

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for complete architecture
3. Check [capability-charter.md](capability-charter.md) for design philosophy
4. For integration: See [SAP-017](../chora-compose-integration/)
