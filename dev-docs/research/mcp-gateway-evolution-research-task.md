---
title: "Research Task: MCP Gateway Evolution & n8n MCP Server Loadability"
type: research-task
audience: claude-webapp
priority: high
date: 2025-10-23
estimated_hours: 4-6
related:
  - dev-docs/sprint-7a-pattern-n2-completion.md
  - docs/archive/ecosystem/n8n-solution-neutral-intent.md
  - docs/explanation/integration-patterns.md
---

# Research Task: MCP Gateway Evolution & n8n MCP Server Loadability

## Executive Context

We are evolving the `mcp-n8n` project into `mcp-gateway` - a general-purpose MCP server aggregator. This research will inform:

1. **Immediate**: Pattern P5 enhancement (fix tool aggregation bug)
2. **Short-term**: Decouple n8n backend into standalone `mcp-server-n8n` project
3. **Medium-term**: Pattern N4 implementation (n8n as MCP gateway)
4. **Long-term**: MCP server development workflow with chora-base templates

## Strategic Goals

### 1. Repository Rename & Scope Change
- **Current**: `mcp-n8n` (implies n8n-specific)
- **Future**: `mcp-gateway` (general-purpose MCP aggregator)
- **Pattern**: P5 (Gateway & Aggregator) becomes the core offering

### 2. Decouple n8n Backend
- Extract `src/mcp_n8n/backends/n8n_backend.py` into standalone project
- New project: `mcp-server-n8n` (already prototyped as `mcp_server_n8n.py`)
- Make it **loadable** by `mcp-gateway` using standard MCP mechanisms

### 3. MCP Server Loadability Standard
**CRITICAL RESEARCH QUESTION:**
- Is there a standard MCP server "plugin" or "loadability" mechanism?
- Does n8n have a standard for loading external MCP servers?
- Can we define a loadability format that works for both `mcp-gateway` AND n8n (Pattern N4)?

### 4. chora-base Integration
- Use chora-base to scaffold new MCP servers
- Optimize for lower-capability LLMs (Claude Haiku, GPT-4o-mini)
- Ergonomic developer experience for creating loadable MCP servers

## Research Questions

### Section A: MCP Protocol & Standards

#### A1. MCP Server Discovery & Loading
**Question:** Is there a standard MCP protocol mechanism for server discovery, plugin loading, or dynamic registration?

**Research Areas:**
- MCP specification (https://spec.modelcontextprotocol.io/)
- MCP SDK documentation (TypeScript & Python)
- FastMCP plugin/extension mechanisms
- Community MCP server patterns (search GitHub for "mcp-server-*")

**Deliverable:** Document any standard loadability patterns, or confirm none exist

#### A2. MCP Server Configuration Formats
**Question:** What are the standard formats for configuring MCP servers (especially in aggregation scenarios)?

**Research Areas:**
- Claude Desktop `claude_desktop_config.json` format
- MCP server manifests (if any)
- Server capability declaration formats
- Tool namespacing conventions

**Example from Claude Desktop:**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "mcp-server-package@latest"],
      "env": {"API_KEY": "..."}
    }
  }
}
```

**Deliverable:** Recommend standard config format for `mcp-gateway` to load MCP servers

#### A3. MCP Tool Aggregation Best Practices
**Question:** How do existing MCP aggregators/gateways expose tools from multiple backends?

**Research Areas:**
- Search for existing MCP gateway implementations
- FastMCP multi-server examples
- MCP proxy patterns
- Tool namespacing conflicts (e.g., two servers both have `get_status` tool)

**Current Issue:** Our Pattern P5 gateway doesn't expose backend tools - only gateway's own `@mcp.tool()` decorated tools

**Deliverable:**
- Root cause analysis of tool aggregation bug
- Recommended fix (likely: programmatically register backend tools with FastMCP)
- Code examples from other projects

### Section B: n8n Integration Patterns

#### B1. n8n Custom Node Development
**Question:** What's the standard way to create custom n8n nodes, and can they call external MCP servers?

**Research Areas:**
- n8n custom node creation guide (https://docs.n8n.io/integrations/creating-nodes/)
- n8n node development best practices
- HTTP/WebSocket client usage in n8n nodes
- Authentication patterns for external APIs

**Goal:** Pattern N3 - Custom n8n node that calls MCP tools

**Deliverable:**
- Step-by-step guide for creating "MCP Tool Call" node
- Code template for n8n node that speaks MCP protocol
- Example workflow using the node

#### B2. n8n as MCP Gateway (Pattern N4)
**Question:** Can n8n workflows act as dynamic MCP request routers?

**Research Areas:**
- n8n webhook trigger for MCP requests
- n8n HTTP request node for calling MCP servers
- Dynamic routing based on tool name
- SSE/streaming response handling in n8n

**Architecture:**
```
MCP Client → n8n webhook → n8n workflow (routing logic) → MCP Server 1/2/N
```

**Deliverable:**
- Feasibility assessment for Pattern N4
- Prototype workflow design (JSON)
- Performance considerations (latency, streaming)

#### B3. n8n MCP Server Loading
**Question:** Does n8n have a mechanism for loading/discovering external MCP servers?

**Research Areas:**
- n8n community nodes marketplace
- n8n configuration for external services
- n8n credential management for MCP servers
- Dynamic service discovery in n8n

**CRITICAL:** If n8n has a standard loadability format, we should align `mcp-gateway` to use the same format!

**Deliverable:** Document n8n's approach (if any), recommend alignment strategy

### Section C: FastMCP Architecture

#### C1. FastMCP Tool Registration Mechanisms
**Question:** How does FastMCP register and expose tools? Can we programmatically register tools from backends?

**Research Areas:**
- FastMCP source code analysis (https://github.com/jlowin/fastmcp)
- `@mcp.tool()` decorator internals
- Programmatic tool registration APIs
- Dynamic tool loading examples

**Current Code:**
```python
# This works (gateway's own tools)
@mcp.tool()
async def get_gateway_status():
    ...

# This doesn't work (backend tools not exposed)
n8n_backend.tools = [
    {"name": "list_workflows", ...}
]
```

**Deliverable:**
- How to programmatically register backend tools with FastMCP
- Code patch for Pattern P5 tool aggregation bug
- Performance implications of dynamic tool registration

#### C2. FastMCP HTTP Transport & SSE
**Question:** How does FastMCP handle HTTP/SSE transport, and can we chain multiple FastMCP servers?

**Research Areas:**
- FastMCP HTTP transport implementation
- SSE streaming for long-running operations
- FastMCP-to-FastMCP communication patterns
- Error propagation across server boundaries

**Use Case:** `mcp-gateway` (FastMCP) → `mcp-server-n8n` (FastMCP) → n8n API

**Deliverable:**
- Best practices for FastMCP server chaining
- Latency analysis
- Error handling recommendations

#### C3. FastMCP Configuration & Environment Management
**Question:** What's the best practice for configuring FastMCP servers with multiple backends?

**Research Areas:**
- FastMCP configuration patterns
- Environment variable conventions
- Backend enable/disable mechanisms
- Hot-reload capabilities

**Current Approach:**
```python
backends = [
    Backend(name="chora", enabled=True, ...),
    Backend(name="n8n", enabled=config.n8n_enabled, ...),
]
```

**Deliverable:** Recommend configuration format for `mcp-gateway` backend loading

### Section D: MCP Server Development Workflow

#### D1. Existing MCP Server Scaffolding Tools
**Question:** Are there existing tools for scaffolding MCP servers? What can we learn from them?

**Research Areas:**
- Search NPM for "create-mcp-server" or similar
- Search PyPI for MCP server templates
- FastMCP examples repository
- MCP SDK quickstart templates

**Examples to analyze:**
- `mcp-server-github`
- `mcp-server-filesystem`
- `mcp-server-sqlite`
- Any others found in GitHub search

**Deliverable:**
- Comparison table of existing scaffolding tools
- Feature gaps that chora-base could fill
- Recommended template structure

#### D2. chora-base MCP Server Template Design
**Question:** What should a chora-base MCP server template include for optimal ergonomics?

**Research Areas:**
- Review chora-base current capabilities
- Copier template best practices
- FastMCP boilerplate reduction opportunities
- Testing framework integration

**Template Requirements:**
- ✅ Minimal boilerplate (< 100 lines for simple server)
- ✅ FastMCP + HTTP/SSE transport pre-configured
- ✅ Tool decorator examples
- ✅ Environment variable handling
- ✅ Logging setup
- ✅ Startup script generation
- ✅ justfile integration
- ✅ Testing scaffolding (pytest + BDD)
- ✅ Documentation generation

**Deliverable:**
- Template specification for chora-base
- Example: "Create MCP server for GitHub API in 30 seconds"
- Lower-capability LLM optimization notes (Haiku/GPT-4o-mini)

#### D3. MCP Server Loadability Format
**Question:** What should the "loadable MCP server" format be for `mcp-gateway`?

**Options to Evaluate:**

**Option 1: Python Module Loading**
```python
# mcp-gateway loads backends as Python modules
from mcp_server_n8n import create_server

backend = create_server(config)
mcp_gateway.register_backend(backend)
```

**Option 2: Subprocess with STDIO**
```yaml
# mcp-gateway config
backends:
  - name: n8n
    command: mcp-server-n8n
    args: [--n8n-url, http://localhost:5679]
    transport: stdio
```

**Option 3: HTTP/SSE URL**
```yaml
# mcp-gateway config
backends:
  - name: n8n
    url: http://localhost:8680/mcp
    transport: http
```

**Option 4: n8n Community Node Format** (if n8n has standard)
```json
{
  "name": "mcp-server-n8n",
  "version": "1.0.0",
  "nodes": [...],
  "mcpServer": {
    "endpoint": "http://localhost:8680/mcp"
  }
}
```

**RESEARCH PRIORITY:** Does n8n have a standard? If yes, use it!

**Deliverable:**
- Recommended loadability format
- Alignment with n8n (if applicable)
- Backwards compatibility strategy

### Section E: Repository Restructuring

#### E1. mcp-n8n → mcp-gateway Rename Strategy
**Question:** What's the best practice for renaming/restructuring a published Python package?

**Research Areas:**
- PyPI package renaming conventions
- GitHub repository rename impacts
- Import path migration (`from mcp_n8n import X` → `from mcp_gateway import Y`)
- Deprecation strategy for existing users (if any)

**Deliverable:**
- Step-by-step migration plan
- Breaking changes documentation
- Version bump strategy (major version?)

#### E2. Decoupling mcp-server-n8n
**Question:** What's the cleanest way to extract n8n backend into standalone project?

**Current Structure:**
```
mcp-n8n/
  src/mcp_n8n/
    backends/
      n8n_backend.py  ← Extract this
```

**Future Structure:**
```
mcp-gateway/
  src/mcp_gateway/
    gateway.py
    backend_registry.py
    config.py

mcp-server-n8n/  ← New standalone repo
  src/mcp_server_n8n/
    server.py
    tools.py
```

**Research Areas:**
- Git history preservation (git filter-branch or subtree split)
- Shared code patterns (e.g., both need logging, config)
- Dependency management
- Testing isolation

**Deliverable:**
- Extraction plan with git commands
- Shared library identification (create `mcp-common`?)
- Testing strategy for both repos

#### E3. Multi-Repository Management
**Question:** Should we use a monorepo or separate repos for mcp-gateway, mcp-server-n8n, mcp-server-*, etc.?

**Research Areas:**
- Python monorepo tools (Pants, Bazel, Poetry workspaces)
- MCP ecosystem conventions (check other mcp-server-* repos)
- chora-base multi-project support
- CI/CD complexity tradeoffs

**Options:**
- **Monorepo**: `mcp-ecosystem/` with subprojects
- **Multi-repo**: Separate repos for each MCP server
- **Hybrid**: `mcp-gateway` separate, all `mcp-server-*` in one repo

**Deliverable:** Recommended repository structure with rationale

### Section F: Implementation Roadmap

#### F1. Pattern P5 Fix (Immediate)
**Question:** What's the minimal fix to expose backend tools in mcp-gateway?

**Deliverable:**
- Code patch for tool aggregation
- Test cases
- Performance benchmarks

#### F2. Pattern N4 Feasibility (Short-term)
**Question:** Is Pattern N4 (n8n as MCP gateway) practical with current n8n capabilities?

**Deliverable:**
- Feasibility assessment (yes/no/partial)
- If YES: Prototype design
- If NO: Alternative approaches
- If PARTIAL: Incremental path

#### F3. Dependency Analysis
**Question:** What dependencies are needed for the full vision?

**Research Areas:**
- FastMCP version requirements
- n8n version requirements (for custom nodes)
- Python version requirements
- Docker/deployment considerations

**Deliverable:** Dependency matrix and compatibility table

## Research Deliverables Summary

### Document 1: MCP Gateway Architecture Decision Record (ADR)
**Filename:** `dev-docs/architecture/mcp-gateway-adr.md`

**Contents:**
1. Tool aggregation solution (Section C1)
2. Loadability format decision (Section D3)
3. Repository structure decision (Section E3)
4. Configuration format (Section A2, C3)

### Document 2: MCP Server Loadability Specification
**Filename:** `dev-docs/specifications/mcp-server-loadability-spec.md`

**Contents:**
1. Standard loadability format (Section D3)
2. n8n alignment (if applicable) (Section B3)
3. mcp-gateway loading mechanism (Section D3)
4. Tool namespacing conventions (Section A2)
5. Example implementations

### Document 3: Pattern P5 Fix Implementation Plan
**Filename:** `dev-docs/implementation/pattern-p5-tool-aggregation-fix.md`

**Contents:**
1. Root cause analysis (Section C1)
2. Code changes required
3. Test plan
4. Migration guide for existing users

### Document 4: Pattern N4 Feasibility Report
**Filename:** `dev-docs/research/pattern-n4-feasibility.md`

**Contents:**
1. n8n custom node approach (Section B1)
2. n8n webhook routing approach (Section B2)
3. Performance analysis
4. Recommended path forward

### Document 5: chora-base MCP Server Template Specification
**Filename:** `dev-docs/specifications/chora-mcp-server-template-spec.md`

**Contents:**
1. Template structure (Section D2)
2. Generated project layout
3. Example usage with Haiku/GPT-4o-mini
4. Integration with mcp-gateway

### Document 6: Repository Migration Plan
**Filename:** `dev-docs/migration/mcp-n8n-to-mcp-gateway.md`

**Contents:**
1. Rename strategy (Section E1)
2. mcp-server-n8n extraction (Section E2)
3. Multi-repo management (Section E3)
4. Timeline and phases

### Document 7: Implementation Roadmap
**Filename:** `project/ROADMAP-V2.md`

**Contents:**
1. Phase 1: Pattern P5 fix (immediate)
2. Phase 2: mcp-server-n8n extraction (short-term)
3. Phase 3: chora-base templates (medium-term)
4. Phase 4: Pattern N4 (medium-term)
5. Success metrics
6. Dependencies

## Success Criteria

This research is successful if it produces:

1. ✅ **Clear decision** on MCP server loadability format (with n8n alignment if possible)
2. ✅ **Working code patch** for Pattern P5 tool aggregation bug
3. ✅ **Feasibility verdict** on Pattern N4 (yes/no/partial)
4. ✅ **Detailed specification** for chora-base MCP server template
5. ✅ **Migration plan** for mcp-n8n → mcp-gateway rename
6. ✅ **Roadmap** with realistic timelines and dependencies

## Time Allocation Recommendation

- **Section A (MCP Protocol):** 1-1.5 hours
- **Section B (n8n Patterns):** 1.5-2 hours
- **Section C (FastMCP):** 1-1.5 hours
- **Section D (Development Workflow):** 1 hour
- **Section E (Repository):** 0.5 hour
- **Section F (Roadmap):** 0.5 hour
- **Document Writing:** 1 hour

**Total:** 6-8 hours

## Priority Order

If time-constrained, research in this order:

1. **CRITICAL**: Section C1 (Pattern P5 tool aggregation fix) - needed immediately
2. **CRITICAL**: Section D3 (Loadability format) - architectural decision
3. **HIGH**: Section B3 (n8n loadability standard) - may influence D3
4. **HIGH**: Section B1 (n8n custom nodes) - needed for Pattern N4
5. **MEDIUM**: Section D2 (chora-base template) - developer experience
6. **MEDIUM**: Section E (Repository migration) - process planning
7. **LOW**: Section A (MCP standards) - nice to know
8. **LOW**: Section F (Roadmap) - can be done last

## Notes for Researcher

- **Focus on practical solutions** over theoretical purity
- **Prioritize n8n compatibility** - if n8n has a standard, use it
- **Look for existing patterns** - don't reinvent the wheel
- **Code examples** are more valuable than abstract descriptions
- **Performance matters** - document latency implications
- **Simplicity wins** - prefer simple, working solutions over complex ideal ones

## Questions to Ask Project Owner After Research

1. Do you want to support BOTH Python module loading AND subprocess loading for backends?
2. Should we maintain backwards compatibility with current mcp-n8n users, or is this a breaking change?
3. Priority: Fix Pattern P5 first, OR extract mcp-server-n8n first?
4. chora-base template: Target Haiku only, or support GPT-4o-mini and other low-capability LLMs?
5. Pattern N4: Is this required for MVP, or future enhancement?

---

**Researcher:** Please create the 7 deliverable documents listed above, focusing on practical, actionable recommendations. Include code examples wherever possible. Good luck! 🚀
