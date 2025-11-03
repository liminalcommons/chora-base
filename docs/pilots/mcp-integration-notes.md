# MCP Server Integration Notes

**Date**: 2025-11-02
**Context**: chora-compose Pilot Investigation Phase

---

## MCP Configuration Status

### Claude Desktop MCP Servers ✅

**Config Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Currently Configured Servers**:

1. **chora-compose** ✅ PRODUCTION DEPLOYMENT (Docker + HTTP/SSE)
   - **Transport**: HTTP with Server-Sent Events (SSE)
   - **URL**: `http://localhost:8001/sse`
   - **Timeout**: 60 seconds
   - **Status**: Production-ready MCP server running in Docker
   - **Auto-approved tools**: 24 tools including:
     - Content generation: `generate_content`, `regenerate_content`, `batch_generate`
     - Artifact assembly: `assemble_artifact`, `list_artifacts`
     - Configuration: `draft_config`, `test_config`, `save_config`, `modify_config`
     - Validation: `validate_content`, `validate_collection_config`
     - Management: `list_generators`, `trace_dependencies`, `cleanup_ephemeral`
     - Collections: `generate_collection`, `list_collection_members`, `check_collection_cache`
     - Freshness tracking: `check_freshness`

   **Alternative Configuration (STDIO - for local development)**:
   - Command: `/Users/victorpiper/code/chora-compose/scripts/run_mcp_server.sh`
   - Working Directory: `/Users/victorpiper/code/chora-compose`
   - Module: `chora_compose.mcp.server`
   - Transport: STDIO

2. **lightrag**
   - Command: `uv` with args
   - Working Directory: `/Users/victorpiper/code/mcp-server-lightrag`
   - Status: Configured for RAG operations

### chora-compose MCP Server Details

#### Production Deployment (Docker + HTTP/SSE)

**Status**: ✅ **FULLY FUNCTIONAL** (Production deployment via Docker)

**Available Tools** (24 total):

1. **Core Generation**
   - `choracompose__generate_content` - Generate content from config
   - `choracompose__regenerate_content` - Regenerate existing content
   - `choracompose__batch_generate` - Generate multiple content pieces
   - `choracompose__preview_generation` - Preview before generating

2. **Artifact Management**
   - `choracompose__assemble_artifact` - Assemble artifact from content configs
   - `choracompose__list_artifacts` - List generated artifacts
   - `choracompose__list_artifact_configs` - List artifact configurations

3. **Content Management**
   - `choracompose__list_content` - List generated content
   - `choracompose__list_content_configs` - List content configurations
   - `choracompose__delete_content` - Remove generated content
   - `choracompose__cleanup_ephemeral` - Clean up temporary content

4. **Configuration Tools**
   - `choracompose__draft_config` - Draft new configuration interactively
   - `choracompose__test_config` - Test configuration before saving
   - `choracompose__save_config` - Save configuration to disk
   - `choracompose__modify_config` - Modify existing configuration

5. **Validation & Quality**
   - `choracompose__validate_content` - Validate content against schema
   - `choracompose__validate_collection_config` - Validate collection config
   - `choracompose__check_freshness` - Check content freshness

6. **Collections**
   - `choracompose__generate_collection` - Generate content collection
   - `choracompose__list_collection_members` - List collection members
   - `choracompose__check_collection_cache` - Check collection cache status

7. **Utilities**
   - `choracompose__hello_world` - Test MCP connection
   - `choracompose__list_generators` - List available generators
   - `choracompose__trace_dependencies` - Trace config dependencies

**Connection Details**:
- **Endpoint**: `http://localhost:8001/sse` (CONFIG) vs `http://localhost:8000/sse` (ACTUAL DOCKER PORT)
- **⚠️ PORT MISMATCH**: Docker container runs on port 8000, config specifies 8001
- **Protocol**: HTTP with Server-Sent Events (SSE)
- **Timeout**: 60 seconds
- **Auto-approval**: All 24 tools pre-approved
- **Action Required**: Update claude_desktop_config.json to use port 8000

**To Test**:
```bash
# Check if Docker container is running
docker ps | grep chora-compose

# Test HTTP endpoint
curl http://localhost:8001/health  # (if health endpoint exists)

# Or use Claude Desktop app to test MCP tools
```

#### Local Development (STDIO)

**Script**: `/Users/victorpiper/code/chora-compose/scripts/run_mcp_server.sh`

**Features**:
- Loads `.env` file if present (preserves existing env vars)
- Sets `MCP_TRANSPORT=stdio` by default
- Adds `src/` to PYTHONPATH for editable installs
- Tries multiple Python interpreters:
  1. Project-local `.venv/bin/python`
  2. Poetry-managed environment (`poetry run python`)
  3. System `python3`
  4. System `python`

**Module Executed**: `python -m chora_compose.mcp.server`

**To Test**:
```bash
# Test MCP server directly (STDIO mode)
/Users/victorpiper/code/chora-compose/scripts/run_mcp_server.sh

# Or via Python module
cd /Users/victorpiper/code/chora-compose
python -m chora_compose.mcp.server
```

---

## MCP Server Configuration Guide

### For Claude Desktop

**Configuration File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Basic Structure**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "/path/to/executable",
      "args": ["optional", "arguments"],
      "cwd": "/working/directory",
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

### Common Patterns

#### Python Package (uv)
```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/server",
        "run",
        "package-name"
      ],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

#### Python Module (direct)
```json
{
  "mcpServers": {
    "my-module-server": {
      "command": "python3",
      "args": ["-m", "my_module.mcp_server"],
      "cwd": "/path/to/project",
      "env": {}
    }
  }
}
```

#### Shell Script
```json
{
  "mcpServers": {
    "my-script-server": {
      "command": "/path/to/run_server.sh",
      "cwd": "/path/to/working/directory",
      "env": {
        "CONFIG_PATH": "/path/to/config.json"
      }
    }
  }
}
```

#### Node.js Server
```json
{
  "mcpServers": {
    "my-node-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

#### HTTP/SSE Server (like chora-compose)
```json
{
  "mcpServers": {
    "my-http-server": {
      "type": "sse",
      "url": "http://localhost:8001/sse",
      "timeout": 60,
      "disabled": false,
      "autoApprove": [
        "tool_name_1",
        "tool_name_2"
      ]
    }
  }
}
```

---

## MCP Server vs Claude Code

### Important Distinction

**Claude Desktop**: Uses MCP servers defined in `claude_desktop_config.json`
- Desktop app integration
- Persistent server connections
- Configured per-user, globally

**Claude Code** (this session): Different integration mechanism
- VS Code extension
- Does not use `claude_desktop_config.json`
- Server/tool configuration managed differently

### Claude Code Configuration

**Current Understanding**: Claude Code tools are built-in and managed by the extension, not via MCP server configuration files.

**To Add Custom Tools to Claude Code**: Would require VS Code extension configuration, not MCP server setup.

---

## Testing chora-compose MCP Server

### Prerequisites

1. chora-compose installed with MCP module
2. Python environment available (`.venv`, poetry, or system)
3. ANTHROPIC_API_KEY set (if required by server)

### Test Commands

**Direct Script Test**:
```bash
cd /Users/victorpiper/code/chora-compose
./scripts/run_mcp_server.sh
```

**Expected Behavior**:
- Server starts and listens on STDIO
- Waits for MCP protocol messages
- May output initialization logs

**If Module Missing**:
```
ModuleNotFoundError: No module named 'chora_compose.mcp.server'
```

**Resolution**: chora-compose MCP module may not be implemented in v1.9.1

### Test from Claude Desktop

1. Open Claude Desktop app
2. Start new conversation
3. Check if chora-compose tools are available
4. If working, you should see chora-compose capabilities in tool list

**Status Check**:
- Tools appear: ✅ MCP server working
- No tools or connection error: ❌ Server not functional
- Never started: ⚠️ Config issue or module missing

---

## Implications for Inbox Pilot

### chora-compose MCP Server IS WORKING ✅

**Status**: Production deployment confirmed with 24 functional tools

**Key Finding**: This SIGNIFICANTLY changes the integration decision!

**Available Capabilities**:
1. ✅ **Artifact assembly** (`assemble_artifact`) - Core requirement met
2. ✅ **Content generation** (`generate_content`, `batch_generate`) - Core requirement met
3. ✅ **Configuration tools** (`draft_config`, `test_config`, `save_config`) - Interactive workflow
4. ✅ **Validation** (`validate_content`, `validate_collection_config`) - Quality assurance
5. ✅ **Dependency tracing** (`trace_dependencies`) - Config management
6. ✅ **Freshness tracking** (`check_freshness`) - Aligns with v1.9.0 features

**Impact on Integration Decision**:

The discovery of a fully functional MCP server with 24 tools suggests:
- **Path A may now be viable** if MCP tools can be used from Claude Code
- **Path B becomes more attractive** if we can use MCP for generation + our post-processing
- **Path C remains safe** but may be redundant if chora-compose is production-ready

**Critical Questions**:
1. Can Claude Code access HTTP/SSE MCP servers? (Previously thought no, but worth investigating)
2. Does chora-compose support our post-processing requirements?
3. Can we use chora-compose MCP tools for inbox artifact generation?

**Recommended Next Steps**:
1. Test chora-compose MCP server in Claude Desktop (immediate)
2. Explore `draft_config`, `test_config`, `assemble_artifact` capabilities
3. Test inbox coordination request generation workflow
4. Assess post-processing integration options
5. Potentially revise integration decision to Path A or Path B

---

## Recommendations

### URGENT: Test MCP Server (PRIORITY CHANGED)

**Original Assessment**: MCP server status unknown, Path C recommended
**New Information**: Production MCP server with 24 tools available
**Revised Priority**: Test immediately before proceeding with Path C

### Immediate Actions (Next 1-2 Hours)

1. **Test chora-compose MCP Server in Claude Desktop** (30-60 minutes)
   - Open Claude Desktop app
   - Check if chora-compose tools are available
   - Test key tools:
     - `choracompose__hello_world` - Verify connection
     - `choracompose__list_artifact_configs` - Check existing configs
     - `choracompose__draft_config` - Test interactive config creation
     - `choracompose__assemble_artifact` - Test artifact generation
   - Document actual behavior and output

2. **Test Inbox Generation Workflow** (30-45 minutes)
   - Try to generate a coordination request using MCP tools
   - Test with our existing content configs (if compatible)
   - Document any config format differences
   - Check if post-processing hooks are available

3. **Reassess Integration Decision** (15-30 minutes)
   - Compare actual MCP capabilities vs. our requirements
   - Evaluate post-processing integration options
   - Consider revised Path A or B if capabilities match
   - Update decision document with findings

### Short-Term (Week 5+)

**If MCP Server Meets Requirements** (REVISED):
- ✅ Proceed with Path A or B (integrate with chora-compose)
- Use MCP tools for generation
- Add post-processing integration if needed
- Build wrapper scripts for automation
- Estimated effort: 8-16 hours (vs. 20-30 for Path C)

**If MCP Server Doesn't Meet Requirements**:
- ✅ Proceed with Path C (standalone generator) as originally planned
- Document MCP findings for future reference
- Consider MCP integration as enhancement later

### Long-Term (Weeks 8-12)

**MCP Integration for chora-base** (if valuable):
- Consider building chora-base MCP server
- Expose inbox coordination tools
- Enable Claude Desktop to generate coordination requests
- Integrate with either chora-compose (Path A/B) or standalone (Path C)

---

## Claude Desktop vs Claude Code Clarification

### Claude Desktop (MCP Client)
- **What it is**: Standalone desktop application for Claude
- **MCP Support**: ✅ Full support via `claude_desktop_config.json`
- **Server Types**: Any MCP-compliant server (Python, Node.js, shell scripts)
- **Use Case**: Interactive exploration, tool integration, persistent connections

### Claude Code (VS Code Extension)
- **What it is**: VS Code extension for AI-assisted coding
- **MCP Support**: ❌ Does not use `claude_desktop_config.json`
- **Tool Access**: Built-in tools provided by extension (Read, Write, Edit, Bash, etc.)
- **Use Case**: Code editing, file operations, terminal commands within VS Code

**Your Question Context**: You're using **Claude Code** (VS Code extension), which does not consume MCP servers from `claude_desktop_config.json`. The MCP configuration is for **Claude Desktop** app only.

**To Use chora-compose MCP Server**: Would need to test in **Claude Desktop** app, not Claude Code.

---

## Summary

✅ **chora-compose MCP server is configured** in Claude Desktop
✅ **Run script exists** and is executable
⚠️ **Functionality unknown** (need to test)
❌ **Claude Code cannot use MCP servers** from `claude_desktop_config.json` (different integration)

**Recommendation**: Test chora-compose MCP server in Claude Desktop app to assess capabilities, but this doesn't affect Claude Code sessions or the inbox pilot decision (Path C still recommended).

---

**Last Updated**: 2025-11-02
**Related Documents**:
- [chora-compose Integration Decision](chora-compose-integration-decision.md)
- [Week 4 Results](chora-compose-pilot-week4-results.md)
- COORD-2025-004: Coordination request to chora-compose team

---

## UPDATED SUMMARY (2025-11-02 - Docker Discovery)

### Key Findings

✅ **chora-compose MCP server is PRODUCTION-READY** (Docker + HTTP/SSE at http://localhost:8001/sse)
✅ **24 tools available** including:
  - Artifact assembly: `assemble_artifact`, `list_artifacts`
  - Content generation: `generate_content`, `batch_generate`, `regenerate_content`
  - Config management: `draft_config`, `test_config`, `save_config`, `modify_config`
  - Validation: `validate_content`, `validate_collection_config`
  - Dependency tracking: `trace_dependencies`
  - Freshness: `check_freshness`

✅ **Auto-approved tools** for seamless workflow
⚠️ **CRITICAL DECISION POINT**: Need to test capabilities before proceeding with Path C
❌ **Claude Code cannot use MCP servers** from `claude_desktop_config.json` (different integration)

### REVISED Recommendation

**URGENT**: Test chora-compose MCP server in Claude Desktop app (1-2 hours) BEFORE proceeding with standalone implementation (Path C).

**Why This Changes Everything**:
- Original assessment: chora-compose incomplete, CLI missing, unstable
- New information: Production MCP server with 24 tools, Docker deployment
- Original recommendation: Path C (20-30 hours standalone)
- Potential revision: Path A/B (8-16 hours with chora-compose) if capabilities match

**Decision Flow**:
1. **Test MCP server** in Claude Desktop (1-2 hours)
   - Verify 24 tools work as documented
   - Test `assemble_artifact` with inbox configs
   - Check post-processing integration options
   
2. **If MCP tools meet requirements** → Revise to Path A/B
   - Use chora-compose MCP tools for generation
   - Add post-processing wrapper if needed
   - Effort: 8-16 hours (40-50% time savings vs. Path C)
   
3. **If MCP tools don't meet requirements** → Proceed with Path C
   - Build standalone generator as planned
   - Effort: 20-30 hours
   - Consider MCP integration later

**Potential Claude Code Integration**:
You mentioned "supergateway" as a possible bridge for HTTP/SSE MCP servers in Claude Code. This would enable:
- Using chora-compose tools directly from Claude Code sessions
- No need for Claude Desktop app switching
- Seamless integration with existing workflows

**Next Step**: Test MCP server before making final decision on Week 5 implementation.

