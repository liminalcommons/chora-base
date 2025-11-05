# chora-compose Meta Protocol Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-29
**Maintainer**: Victor Piper

---

## 1. Overview

This protocol specification defines the complete architecture, capabilities, and operational model of chora-compose as an MCP-native content generation platform. It serves as the authoritative reference for understanding chora-compose's design philosophy, technical implementation, and ecosystem positioning.

### 1.1 Purpose

Document the complete chora-compose system including:
- Architectural principles and design patterns
- MCP tool catalog (17 tools + 5 resource families)
- Access modalities (pip, SAP, MCP, API)
- Configuration-driven operational model
- Observability and debugging infrastructure
- Future roadmap and capability broker vision

### 1.2 Scope

**In Scope**:
- Complete system architecture
- All MCP tools and resources (current state: v1.2.0)
- Access patterns and integration points
- Configuration schema and validation
- Observability mechanisms
- Future capabilities (clearly marked as roadmap)

**Out of Scope**:
- Step-by-step integration guide (see SAP-017)
- Role-specific workflows (see SAP-017 awareness-guide)
- Troubleshooting procedures (see SAP-017)

---

## 2. Architectural Principles

### 2.1 Configuration-Driven

**Principle**: All behavior controlled via declarative YAML configuration

**Rationale**:
- Predictable, reproducible content generation
- Version-controllable configuration
- Clear separation of concerns (config vs code)
- Easy to test and validate

**Implementation**:
```yaml
# .chora-compose.yaml
version: "1.0"
provider: anthropic
model: claude-3-5-sonnet-20241022

templates:
  directory: templates/
  cache: true

output:
  directory: output/
  format: markdown
```

### 2.2 MCP-Native

**Principle**: Built on Model Context Protocol as first-class integration layer

**Rationale**:
- Standard interface for LLM tool use
- Compatible with Claude Desktop, MCP ecosystem
- Discoverable tools via MCP server protocol
- Observable via MCP inspector

**Implementation**:
- FastMCP framework for server implementation
- 17 MCP tools exposed via standard protocol
- 5 resource URI families for content access
- SSE transport for real-time streaming

### 2.3 Observable

**Principle**: Comprehensive logging, tracing, and metrics

**Rationale**:
- Debug generation issues quickly
- Track token usage and costs
- Understand generation patterns
- Optimize template performance

**Implementation**:
- Structured logging (JSON)
- Request/response tracing
- Token usage metrics
- Template performance analytics

---

## 3. System Architecture

### 3.1 Component Model

```
┌─────────────────────────────────────────────────────┐
│                  Access Layer                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐ │
│  │   pip   │  │   SAP   │  │   MCP   │  │  API   │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └───┬────┘ │
│       │            │            │            │       │
└───────┼────────────┼────────────┼────────────┼───────┘
        │            │            │            │
┌───────┴────────────┴────────────┴────────────┴───────┐
│              Core Generation Engine                   │
│  ┌──────────────────────────────────────────────┐   │
│  │  Template System  │  Content Pipeline       │   │
│  │  - YAML templates │  - Input validation     │   │
│  │  - Jinja2 render  │  - LLM generation       │   │
│  │  - Cache mgmt     │  - Output formatting    │   │
│  └──────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
        │            │            │            │
┌───────┴────────────┴────────────┴────────────┴───────┐
│              Infrastructure Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │ Config Mgmt │  │ Observability│  │ LLM Providers│ │
│  │ - Validation│  │ - Logging    │  │ - Anthropic  │ │
│  │ - Defaults  │  │ - Metrics    │  │ - OpenAI     │ │
│  │ - Overrides │  │ - Tracing    │  │ - (Future)   │ │
│  └─────────────┘  └─────────────┘  └──────────────┘ │
└───────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

```
User Request
    ↓
[Access Layer] (CLI/MCP/SAP/API)
    ↓
[Config Resolution] (merge defaults + user config)
    ↓
[Template Selection] (match request to template)
    ↓
[Input Validation] (schema check, type validation)
    ↓
[Content Generation] (LLM API call with template)
    ↓
[Output Formatting] (markdown/JSON/HTML)
    ↓
[Observability] (log metrics, trace request)
    ↓
Result
```

---

## 4. MCP Tool Catalog

### 4.1 Core Generation Tools

#### 4.1.1 `generate_content`
**Purpose**: General-purpose content generation
**Inputs**:
- `template` (string): Template name or path
- `context` (object): Variables for template
- `output` (string, optional): Output file path

**Outputs**:
- `content` (string): Generated markdown/text
- `metadata` (object): Token count, generation time

**Example**:
```json
{
  "template": "api-reference",
  "context": {
    "api_name": "UserService",
    "endpoints": [...]
  },
  "output": "docs/api/user-service.md"
}
```

#### 4.1.2 `apply_template`
**Purpose**: Apply predefined template to structured data
**Inputs**:
- `template_id` (string): Registered template ID
- `data` (object): Structured input data

**Outputs**:
- `rendered` (string): Template output

#### 4.1.3 `batch_generate`
**Purpose**: Process multiple generation requests
**Inputs**:
- `requests` (array): List of generation requests
- `parallel` (boolean): Run in parallel

**Outputs**:
- `results` (array): Array of generated content
- `summary` (object): Batch statistics

### 4.2 Configuration Tools

#### 4.2.1 `validate_config`
**Purpose**: Validate configuration file
**Inputs**:
- `config_path` (string): Path to config file

**Outputs**:
- `valid` (boolean): Validation result
- `errors` (array): Validation errors if any

#### 4.2.2 `get_config`
**Purpose**: Retrieve current configuration
**Outputs**:
- `config` (object): Complete config object

#### 4.2.3 `set_config`
**Purpose**: Update configuration values
**Inputs**:
- `updates` (object): Config key-value pairs

**Outputs**:
- `config` (object): Updated config

### 4.3 Template Management Tools

#### 4.3.1 `list_templates`
**Purpose**: List available templates
**Outputs**:
- `templates` (array): Template metadata

#### 4.3.2 `get_template`
**Purpose**: Retrieve template content
**Inputs**:
- `template_id` (string): Template identifier

**Outputs**:
- `template` (object): Template definition

#### 4.3.3 `validate_template`
**Purpose**: Validate template syntax
**Inputs**:
- `template` (string): Template content

**Outputs**:
- `valid` (boolean): Validation result
- `errors` (array): Syntax errors

### 4.4 Observability Tools

#### 4.4.1 `get_metrics`
**Purpose**: Retrieve generation metrics
**Inputs**:
- `timeframe` (string, optional): Time range

**Outputs**:
- `metrics` (object): Usage statistics

#### 4.4.2 `get_trace`
**Purpose**: Get request trace
**Inputs**:
- `request_id` (string): Request identifier

**Outputs**:
- `trace` (object): Full request trace

#### 4.4.3 `clear_cache`
**Purpose**: Clear template cache
**Outputs**:
- `cleared` (integer): Items cleared

### 4.5 Development Tools

#### 4.5.1 `generate_tool_docs`
**Purpose**: Generate MCP tool documentation
**Inputs**:
- `source` (string): Tool source directory

**Outputs**:
- `docs` (string): Generated documentation

#### 4.5.2 `generate_tests`
**Purpose**: Generate test cases from signatures
**Inputs**:
- `function` (string): Function signature

**Outputs**:
- `tests` (string): Generated test code

#### 4.5.3 `sync_docs`
**Purpose**: Sync docs with source
**Inputs**:
- `source_dir` (string): Source directory
- `docs_dir` (string): Docs directory

**Outputs**:
- `synced` (array): Updated files

### 4.6 Infrastructure Tools

#### 4.6.1 `validate_mcp_config`
**Purpose**: Validate MCP server configuration
**Inputs**:
- `config_path` (string): MCP config file

**Outputs**:
- `valid` (boolean): Validation result
- `errors` (array): Config errors

#### 4.6.2 `health_check`
**Purpose**: Check system health
**Outputs**:
- `healthy` (boolean): Health status
- `details` (object): Component status

---

## 5. Resource URI Families

### 5.1 Template Resources

**URI Pattern**: `chora-compose://templates/{template_id}`
**Purpose**: Access template definitions
**Example**: `chora-compose://templates/api-reference`

### 5.2 Generated Content Resources

**URI Pattern**: `chora-compose://content/{content_id}`
**Purpose**: Access previously generated content
**Example**: `chora-compose://content/api-user-service-20251029`

### 5.3 Configuration Resources

**URI Pattern**: `chora-compose://config/{key}`
**Purpose**: Access configuration values
**Example**: `chora-compose://config/provider`

### 5.4 Metrics Resources

**URI Pattern**: `chora-compose://metrics/{metric_type}`
**Purpose**: Access metrics data
**Example**: `chora-compose://metrics/token-usage`

### 5.5 Trace Resources

**URI Pattern**: `chora-compose://traces/{trace_id}`
**Purpose**: Access request traces
**Example**: `chora-compose://traces/req-abc123`

---

## 6. Access Modalities

### 6.1 Modality 1: pip (Python Package)

**When to Use**: CLI access, scripting, CI/CD

**Installation**:
```bash
pip install chora-compose
```

**Usage**:
```bash
chora-compose generate --template api-ref --output docs/api.md
```

**Characteristics**:
- Direct Python API access
- CLI commands
- Scriptable workflows
- CI/CD integration

### 6.2 Modality 2: SAP (Skilled Awareness Package)

**When to Use**: Agent-driven discovery and adoption

**Access**: SAP-017 (chora-compose-integration)

**Characteristics**:
- Agent discovers capability
- Guided installation
- Context-aware usage
- Integration patterns

### 6.3 Modality 3: MCP (Model Context Protocol)

**When to Use**: Claude Desktop integration, MCP clients

**Configuration**:
```json
{
  "mcpServers": {
    "chora-compose": {
      "command": "uvx",
      "args": ["chora-compose"]
    }
  }
}
```

**Characteristics**:
- Tool use via MCP protocol
- Resource access
- Real-time generation
- Observable requests

### 6.4 Modality 4: API (HTTP/REST)

**When to Use**: Service integration, web apps

**Status**: Roadmap (not yet implemented)

**Future Design**:
```http
POST /api/v1/generate
Content-Type: application/json

{
  "template": "api-reference",
  "context": {...}
}
```

**Characteristics**:
- RESTful HTTP API
- Authentication/authorization
- Rate limiting
- Webhook callbacks

---

## 7. Configuration Schema

### 7.1 Root Configuration

```yaml
version: "1.0"           # Schema version (required)
provider: "anthropic"    # LLM provider (required)
model: "claude-3-5-sonnet-20241022"  # Model ID (required)
temperature: 0.7         # Generation temperature (0.0-1.0)
max_tokens: 4000         # Max output tokens

templates:               # Template configuration
  directory: "templates/"
  cache: true
  cache_ttl: 3600

output:                  # Output configuration
  directory: "output/"
  format: "markdown"     # markdown|json|html
  overwrite: false

observability:           # Observability configuration
  log_level: "info"      # debug|info|warning|error
  log_file: ".chora/logs/generate.log"
  trace_requests: true
  metrics_enabled: true

providers:               # Provider-specific config
  anthropic:
    api_key_env: "ANTHROPIC_API_KEY"
    base_url: "https://api.anthropic.com"
  openai:
    api_key_env: "OPENAI_API_KEY"
    base_url: "https://api.openai.com"
```

### 7.2 Template Schema

```yaml
id: "api-reference"      # Template identifier
name: "API Reference Generator"
description: "Generate API documentation from OpenAPI spec"
version: "1.0.0"

inputs:                  # Input schema
  - name: "api_name"
    type: "string"
    required: true
  - name: "endpoints"
    type: "array"
    required: true

prompt:                  # Generation prompt
  system: "You are an API documentation expert..."
  user_template: "Generate docs for {{api_name}} with {{endpoints|length}} endpoints..."

output:                  # Output configuration
  format: "markdown"
  sections:
    - "overview"
    - "authentication"
    - "endpoints"
    - "examples"
```

---

## 8. Observability Model

### 8.1 Logging

**Format**: JSON structured logging

**Fields**:
```json
{
  "timestamp": "2025-10-29T10:00:00Z",
  "level": "INFO",
  "component": "generator",
  "event": "content_generated",
  "request_id": "req-abc123",
  "template": "api-reference",
  "tokens": {
    "input": 1234,
    "output": 567,
    "total": 1801
  },
  "duration_ms": 2345
}
```

### 8.2 Metrics

**Collected Metrics**:
- `generation_requests_total` (counter)
- `generation_duration_seconds` (histogram)
- `token_usage_total` (counter, by input/output)
- `template_usage_total` (counter, by template)
- `error_rate` (gauge)

**Access**:
```bash
chora-compose metrics --show
```

### 8.3 Tracing

**Trace Components**:
- Request initiation
- Config resolution
- Template loading
- LLM API call
- Response processing
- Output writing

**Enable**:
```bash
CHORA_TRACE=true chora-compose generate ...
```

---

## 9. Future Roadmap

### 9.1 Capability Broker (Planned)

**Vision**: Cross-repo capability coordination

**Features**:
- Publish templates to ecosystem
- Discover capabilities across repos
- Version compatibility checking
- Dependency resolution

**Status**: Design phase, not yet implemented

### 9.2 Multi-Provider Support (Planned)

**Providers**:
- Anthropic (current)
- OpenAI (current)
- Groq (planned)
- Local models (planned)

### 9.3 Advanced Caching (Planned)

**Features**:
- Semantic caching
- Multi-level cache hierarchy
- Cache warming strategies
- Invalidation policies

### 9.4 Collaboration Features (Planned)

**Features**:
- Real-time co-generation
- Review workflows
- Version control integration
- Team templates

---

## 10. Governance

### 10.1 Version Management

**Current Version**: v1.2.0
**Versioning Scheme**: Semantic versioning (MAJOR.MINOR.PATCH)

**Breaking Changes**:
- Announced in CHANGELOG
- Migration guides provided
- Deprecation warnings (1 version ahead)

### 10.2 Security

**API Key Management**:
- Environment variables only
- Never log API keys
- Rotate keys regularly

**Content Security**:
- Sanitize generated content
- Validate inputs
- Rate limiting (future)

### 10.3 Support

**Documentation**: https://chrisdburr.github.io/chora-compose/
**Issues**: https://github.com/chrisdburr/chora-compose/issues
**Discussions**: GitHub Discussions

---

## 11. Related Content

### Within This SAP
- [capability-charter.md](capability-charter.md) - Strategic positioning
- [awareness-guide.md](awareness-guide.md) - Operator playbook
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [architecture-overview.md](architecture-overview.md) - Architecture deep-dive
- [design-philosophy.md](design-philosophy.md) - Design principles
- [integration-patterns.md](integration-patterns.md) - Usage patterns
- [ledger.md](ledger.md) - Adoption tracking

### Other SAPs
- [SAP-017: chora-compose-integration](../chora-compose-integration/) - Integration guide
- [SAP-016: MCP Server Development](../mcp-server-development/) - MCP patterns
- [SAP-002: chora-base-meta](../chora-base/) - Parallel meta-SAP pattern

### External Resources
- [chora-compose Repository](https://github.com/chrisdburr/chora-compose)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)

---

## 12. Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents self-evaluation criteria for SAP-018 awareness file completeness, enabling automated validation of equivalent support for generic agents and Claude Code.

### 12.1 Awareness File Requirements

**Required Files**:
- `AGENTS.md` - Generic AI agent workflows
- `CLAUDE.md` - Claude Code-specific tool patterns

**Validation Command**:
```bash
python scripts/sap-evaluator.py --deep chora-compose-meta
```

### 12.2 Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Understanding Architecture (10-15 min) - Read architecture overview, component breakdown, integration points
2. Design Philosophy and Trade-offs (5-10 min) - Read design rationale, trade-off examples, design influences
3. MCP Tools Catalog (5 min) - List all 17 MCP tools across 4 categories, resource URI families
4. Ecosystem Positioning (10 min) - Compare to Kubernetes/Tilt/Skaffold, decision criteria, migration paths
5. Contributing to chora-compose (15-20 min) - Extension points, contribution workflow, testing requirements

**CLAUDE.md**: 4 workflows
1. Understanding Architecture with Read - Read protocol-spec.md, extract components, explain to user
2. Understanding Design Trade-offs with Read - Read capability-charter.md, find trade-off documentation, explain rationale
3. Exploring MCP Tools Catalog with Read and Bash - Read MCP tools catalog, launch MCP inspector, list tools interactively
4. Comparing to Alternatives with Read and Grep - Read ecosystem comparison, search comparison matrix, present decision criteria

**Variance**: 4 workflows (CLAUDE.md) vs 5 workflows (AGENTS.md) = 20% difference
**Acceptable**: Yes (within ±30% tolerance)

**Rationale for Variance**: CLAUDE.md consolidates workflows around Read tool for documentation exploration, while AGENTS.md provides granular step-by-step guidance for each meta-documentation operation. Both provide equivalent coverage of chora-compose architecture understanding, design philosophy, MCP tools, and ecosystem positioning through different organizational approaches.

### 12.3 User Signal Pattern Coverage

**AGENTS.md**: 1 table with 6 signals
- Meta-Documentation Operations table
  - "explain chora-compose architecture" → show_architecture()
  - "why chora-compose" → show_design_philosophy()
  - "compare to Kubernetes" → show_ecosystem_positioning()
  - "how to extend" → show_contribution_guide()
  - "MCP tools available" → list_mcp_tools()
  - "chora-compose vs Tilt" → compare_alternatives()

**CLAUDE.md**: Tool-specific patterns documented in 5 tips
- Tip 1: Read protocol-spec.md before technology decisions
- Tip 2: Use Bash to launch MCP inspector
- Tip 3: Use Grep to find design decisions
- Tip 4: Read capability-charter.md for philosophy
- Tip 5: Use Read for progressive loading

**Coverage**: AGENTS.md provides user signal translation, CLAUDE.md provides tool patterns for implementing those signals with Claude Code tools (Read, Bash, Grep).

### 12.4 Validation Checkpoints

**Structural Validation**:
```bash
# Check both awareness files exist
ls docs/skilled-awareness/chora-compose-meta/AGENTS.md
ls docs/skilled-awareness/chora-compose-meta/CLAUDE.md

# Check YAML frontmatter present
head -20 docs/skilled-awareness/chora-compose-meta/AGENTS.md | grep "sap_id: SAP-018"
head -20 docs/skilled-awareness/chora-compose-meta/CLAUDE.md | grep "sap_id: SAP-018"
```

**Coverage Validation**:
```bash
# Count workflows in AGENTS.md (expect: 5)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/chora-compose-meta/AGENTS.md

# Count workflows in CLAUDE.md (expect: 4)
grep -c "^### Workflow [0-9]:" docs/skilled-awareness/chora-compose-meta/CLAUDE.md

# Check user signal table exists in AGENTS.md
grep -c "## User Signal Patterns" docs/skilled-awareness/chora-compose-meta/AGENTS.md
```

**Expected Results**:
- Both awareness files exist ✅
- YAML frontmatter with progressive_loading ✅
- AGENTS.md: 5 workflows, 1 user signal table ✅
- CLAUDE.md: 4 workflows, 5 tool-specific tips ✅
- Workflow variance: 20% (acceptable) ✅

### 12.5 Integration with SAP-009

**Phase 4 Criteria Met**:
- ✅ AGENTS.md provides generic workflow guidance
- ✅ CLAUDE.md provides Claude Code tool patterns
- ✅ Workflow coverage within acceptable variance (20% < 30%)
- ✅ Rationale documented for organizational differences
- ✅ Self-evaluation criteria documented in protocol-spec.md

**SAP-018 Awareness Status**: Phase 4 compliant (equivalent support for generic agents and Claude Code)

---

**Protocol Version History**:
- **1.0.0** (2025-10-29): Initial complete protocol specification for chora-compose v1.2.0
- **1.0.1** (2025-11-05): Added Section 12: Self-Evaluation Criteria (SAP-009 Phase 4 compliance)
