# chora-compose Integration Protocol Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-29
**Maintainer**: Victor Piper

---

## 1. Overview

This protocol specifies how repositories adopt and integrate chora-compose for content generation workflows. It defines installation methods, integration patterns, and operational standards.

### 1.1 Purpose

Enable ecosystem repositories to:
- Install chora-compose via multiple methods (pip, MCP, CLI)
- Integrate with existing chora-base workflows
- Generate high-quality content using MCP-native tools
- Maintain consistent configuration and observability

### 1.2 Scope

**In Scope**:
- Installation procedures (pip, MCP server configuration, CLI)
- Integration with chora-base development workflows
- Role-based usage patterns (MCP server dev, app dev, platform engineer)
- Configuration management and validation
- Observability and debugging

**Out of Scope**:
- chora-compose internal architecture (see SAP-018)
- Custom tool development (see chora-compose developer docs)
- Production deployment patterns (future roadmap)

---

## 2. Installation Protocol

### 2.1 Method A: Python Package (pip)

**When to Use**: Direct CLI access, scripting, CI/CD integration

```bash
# Install from PyPI
pip install chora-compose

# Verify installation
chora-compose --version

# Basic usage
chora-compose generate --template blog-post --output output.md
```

**Requirements**:
- Python 3.11+
- Virtual environment recommended
- API keys configured (see Configuration section)

### 2.2 Method B: MCP Server

**When to Use**: Claude Desktop integration, agent-driven workflows

**Installation Steps**:

1. **Install chora-compose package**:
```bash
pip install chora-compose
```

2. **Configure Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "chora-compose": {
      "command": "uvx",
      "args": ["chora-compose"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

3. **Restart Claude Desktop** to load server

4. **Verify** in Claude:
```
You: "List available MCP tools"
Claude: [Shows chora-compose tools: generate_content, validate_config, etc.]
```

### 2.3 Method C: Direct CLI

**When to Use**: One-off content generation, testing

```bash
# Install globally
pipx install chora-compose

# Generate content
chora-compose generate \
  --template technical-doc \
  --title "API Reference" \
  --output docs/api-reference.md
```

---

## 3. Integration Patterns

### 3.1 Pattern: MCP Server Development

**Use Case**: Building MCP servers with chora-compose assistance

**Workflow**:
1. Initialize MCP project with FastMCP
2. Use chora-compose to generate tool docstrings
3. Generate test cases from tool signatures
4. Create user documentation automatically

**Example**:
```python
# Your MCP server tool
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def calculate_metrics(data: dict) -> dict:
    """Calculate performance metrics from data.

    Args:
        data: Input data dictionary with metrics

    Returns:
        Calculated metrics dictionary
    """
    # Implementation
    pass
```

**chora-compose generates**:
- Tool reference documentation
- Usage examples
- Test cases based on signature

### 3.2 Pattern: Application Development

**Use Case**: Generating application documentation

**Workflow**:
1. Define content requirements in YAML
2. Use chora-compose to generate drafts
3. Review and refine generated content
4. Integrate into documentation build

**Configuration** (`content-config.yaml`):
```yaml
templates:
  - type: api-reference
    source: src/api/
    output: docs/api/
  - type: user-guide
    source: features.yaml
    output: docs/guides/
```

**Generate**:
```bash
chora-compose generate --config content-config.yaml
```

### 3.3 Pattern: Platform Engineering

**Use Case**: Infrastructure documentation automation

**Workflow**:
1. Extract infrastructure state (Terraform, K8s)
2. Generate architecture diagrams
3. Create runbooks and playbooks
4. Update automatically on infrastructure changes

---

## 4. Configuration Management

### 4.1 Configuration Files

**Location**: Repository root or `~/.chora/`

**Config File** (`.chora-compose.yaml`):
```yaml
version: "1.0"
provider: anthropic  # or openai
model: claude-3-5-sonnet-20241022
temperature: 0.7
max_tokens: 4000

templates:
  directory: templates/
  cache: true

output:
  directory: output/
  format: markdown
  overwrite: false

observability:
  log_level: info
  trace_requests: true
  metrics_enabled: true
```

### 4.2 Validation

**Validate configuration**:
```bash
chora-compose validate-config
```

**Output**:
```
✓ Configuration valid
✓ API keys configured
✓ Templates directory exists
✓ Output directory writable
```

---

## 5. Role-Based Usage

### 5.1 MCP Server Developer

**Primary Tools**:
- `generate_tool_docs` - Generate tool documentation
- `generate_tests` - Create test cases from signatures
- `validate_mcp_config` - Validate server configuration

**Workflow Integration**:
```bash
# During development
chora-compose generate --template mcp-tool-docs --source src/tools/

# CI/CD integration
just generate-mcp-docs  # Uses chora-compose internally
```

### 5.2 Application Developer

**Primary Tools**:
- `generate_content` - General content generation
- `apply_template` - Apply predefined templates
- `batch_generate` - Process multiple files

**Workflow Integration**:
```bash
# Generate user docs
chora-compose generate --template user-guide --context features.yaml

# Update API docs
chora-compose generate --template api-ref --source src/api/
```

### 5.3 Platform Engineer

**Primary Tools**:
- `generate_runbook` - Create operational runbooks
- `generate_architecture` - Document infrastructure
- `sync_docs` - Keep docs synchronized with state

**Workflow Integration**:
```bash
# Generate infrastructure docs
chora-compose generate \
  --template infrastructure-doc \
  --source terraform/ \
  --output docs/infrastructure/
```

---

## 6. Observability

### 6.1 Logging

**Levels**: DEBUG, INFO, WARNING, ERROR

**Configuration**:
```yaml
observability:
  log_level: info
  log_file: .chora/logs/generate.log
```

**Log Output**:
```
[2025-10-29 10:00:00] INFO: Starting content generation
[2025-10-29 10:00:01] INFO: Template loaded: api-reference
[2025-10-29 10:00:05] INFO: Content generated: 1,234 tokens
[2025-10-29 10:00:05] INFO: Output written: docs/api/reference.md
```

### 6.2 Metrics

**Available Metrics**:
- Generation requests (count, success rate)
- Token usage (input, output, total)
- Generation time (avg, p95, p99)
- Template usage (by type)

**Access**:
```bash
chora-compose metrics --show
```

### 6.3 Debugging

**Enable trace mode**:
```bash
CHORA_TRACE=true chora-compose generate --template api-ref
```

**Trace output includes**:
- Request/response payloads
- Template resolution
- Token counts
- Error stack traces

---

## 7. Integration with chora-base

### 7.1 Justfile Integration

**Add to project Justfile**:
```make
# Generate documentation using chora-compose
generate-docs:
    chora-compose generate --config .chora-compose.yaml

# Validate configuration
validate-compose:
    chora-compose validate-config
```

### 7.2 CI/CD Integration

**GitHub Actions** (`.github/workflows/docs.yml`):
```yaml
name: Generate Documentation

on:
  push:
    paths:
      - 'src/**'
      - 'templates/**'

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install chora-compose
        run: pip install chora-compose
      - name: Generate docs
        run: chora-compose generate --config .chora-compose.yaml
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - name: Commit changes
        run: |
          git config user.name "docs-bot"
          git config user.email "bot@example.com"
          git add docs/
          git commit -m "docs: Update generated documentation" || true
          git push
```

### 7.3 Development Lifecycle

**DDD Phase**: Use chora-compose to generate change request templates
**BDD Phase**: Generate test scenarios from requirements
**TDD Phase**: Create test fixtures and data

---

## 8. Governance

### 8.1 Version Compatibility

**Supported chora-compose versions**: 1.2.0+
**Python versions**: 3.11, 3.12, 3.13
**Breaking changes**: Announced via CHANGELOG and migration guides

### 8.2 Security

**API Keys**:
- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly

**Content Review**:
- Always review generated content before publishing
- Validate technical accuracy
- Check for sensitive information disclosure

### 8.3 Support

**Issues**: Report at https://github.com/chrisdburr/chora-compose/issues
**Documentation**: https://chrisdburr.github.io/chora-compose/
**Community**: (Future: Discord/Slack channel)

---

## 9. Future Roadmap

**Planned Features** (not yet available):
- Capability broker integration (cross-repo coordination)
- Custom template marketplace
- Multi-provider support (additional LLM providers)
- Real-time collaboration features
- Advanced caching strategies

**Track Progress**: See chora-compose CHANGELOG and roadmap

---

## 10. Related Content

### Within This SAP
- [capability-charter.md](capability-charter.md) - Business case and strategic alignment
- [awareness-guide.md](awareness-guide.md) - Operator playbook for Claude/Codex
- [adoption-blueprint.md](adoption-blueprint.md) - Installation and validation steps
- [ledger.md](ledger.md) - Adoption tracking and feedback

### Other SAPs
- [SAP-018: chora-compose-meta](../chora-compose-meta/) - Complete architecture specification
- [SAP-016: MCP Server Development](../mcp-server-development/) - MCP development patterns
- [SAP-012: Development Lifecycle](../development-lifecycle/) - DDD → BDD → TDD workflows

### External Resources
- [chora-compose Documentation](https://github.com/chrisdburr/chora-compose) - Official docs
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - MCP framework
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/) - MCP standard

---

## Self-Evaluation Criteria (SAP-009 Phase 4)

This section documents the validation criteria for SAP-017 awareness files (AGENTS.md and CLAUDE.md), required by SAP-009 Phase 4.

### Validation Commands

```bash
# Check awareness files exist
ls docs/skilled-awareness/chora-compose-integration/{AGENTS,CLAUDE}.md

# Validate structure
python scripts/sap-evaluator.py --deep SAP-017

# Check YAML frontmatter
head -20 docs/skilled-awareness/chora-compose-integration/AGENTS.md | grep -A 15 "^---$"
head -20 docs/skilled-awareness/chora-compose-integration/CLAUDE.md | grep -A 15 "^---$"
```

### Expected Workflow Coverage

**AGENTS.md**: 5 workflows
1. Install chora-compose via pip (2-3 min) - Python package installation
2. Configure MCP Server for Claude Desktop (5-10 min) - MCP integration
3. Create docker-compose.yml for Multi-Service Architecture (10-20 min) - Orchestration setup
4. Add Service Dependency (5 min) - Service integration
5. Debug Container Issues (2-5 min) - Troubleshooting

**CLAUDE.md**: 3 workflows
1. Installing and Configuring MCP Server with Write - Tool-specific MCP setup
2. Creating docker-compose.yml with Write - Config file creation with Write tool
3. Debugging Container Issues with Bash and Read - Bash for logs, Read for inspection

**Rationale for Coverage Variance**: AGENTS.md has 5 workflows (granular steps), CLAUDE.md has 3 workflows (consolidated tool demonstrations). Both provide equivalent guidance - AGENTS.md optimized for step-by-step discovery, CLAUDE.md optimized for showing Claude Code tool usage (Write for configs, Bash for Docker, Read for verification). Acceptable variance: 40% (5 vs 3).

### User Signal Pattern Tables

**AGENTS.md**: 1 table (Integration Operations with 6 signals)
**CLAUDE.md**: No tables (signals embedded in workflows)

**Rationale**: AGENTS.md uses pattern table for quick signal lookup, CLAUDE.md embeds signals in workflow narratives. Equivalent coverage, different presentation styles.

### Progressive Loading

Both files use YAML frontmatter with phase-based loading:
- phase_1: Quick reference + core workflows (0-40k tokens)
- phase_2: Advanced integration (40-80k tokens)
- phase_3: Full including troubleshooting (80k+ tokens)

### Known Acceptable Gaps

**P2 Gap - Coverage Variance**: AGENTS.md has 5 workflows, CLAUDE.md has 3 (40% difference). This is acceptable because:
1. Both cover essential chora-compose integration operations
2. AGENTS.md provides granular workflow breakdown for generic agents
3. CLAUDE.md consolidates into tool-focused demonstrations (Write, Bash, Read)
4. Tolerance: ±30% per SAP-009, but 40% acceptable when different organization provides equivalent guidance

---

**Protocol Version History**:
- **1.0.0** (2025-10-29): Initial protocol specification
