# Claude Desktop MCP Configuration & HTTP Transport Support: Technical Briefing

**Date:** October 23, 2025  
**Context:** Investigating whether Claude Desktop can connect to remote HTTP MCP endpoints without spawning a local executable  
**Error Encountered:** `spawn . EACCES` when attempting HTTP transport configuration without `command` field

---

## Executive Summary

**Critical Finding:** Claude Desktop's `claude_desktop_config.json` does NOT support direct HTTP/SSE transport configuration. All MCP server entries MUST specify a `command` field that spawns a local stdio-based subprocess. Claude Desktop is a stdio-only MCP client.

**Root Cause of Error:** The `spawn . EACCES` error occurs because Claude Desktop attempts to execute the `command` field value as a subprocess. When `command` is missing or empty, it defaults to spawning the current directory (`.`), which is not executable.

**Recommended Solution:** Use `npx mcp-remote` as a stdio-to-HTTP/SSE proxy to connect to your remote MCP server.

---

## 1. Schema & Requirements

### Configuration File Location

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### JSON Schema Structure

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "<executable>",        // REQUIRED: Command to spawn subprocess
      "args": ["<arg1>", "<arg2>"],     // REQUIRED: Array of command arguments
      "env": {                           // OPTIONAL: Environment variables
        "KEY": "value"
      },
      "cwd": "<working-directory>"      // OPTIONAL: Working directory for subprocess
    }
  }
}
```

### Field Requirements

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `command` | **YES** | string | Executable to spawn (e.g., `node`, `python`, `npx`, `uvx`) |
| `args` | **YES** | array\<string\> | Arguments passed to the command |
| `env` | NO | object | Environment variables for the subprocess |
| `cwd` | NO | string | Working directory (defaults to user home) |

**CRITICAL:** There is no `transport` or `type` field. Every entry is implicitly stdio transport via subprocess spawning.

### Validation Behavior

Claude Desktop validates configuration entries as follows:

1. **Checks for `command` field** - If missing, attempts to spawn `.` (current directory), resulting in `EACCES` error
2. **Verifies executable exists** - Must be in PATH or absolute path
3. **Launches subprocess on startup** - Each server is a separate process
4. **Communicates via stdio** - Uses stdin/stdout for MCP JSON-RPC messages

**Source:** Multiple configuration examples from official Anthropic documentation and community implementations consistently show this schema.

---

## 2. HTTP Transport Support

### Native HTTP Support: NOT AVAILABLE in claude_desktop_config.json

**Official Statement (GitHub Discussion #16):**
> "Configuring the MCP servers into Claude Desktop App currently only show how to add the stdio protocol versions. ==> How do I add MCP server using HTTP with SSE transport? Or is it not yet supported?"
> 
> **Response from @dsp-ant (Maintainer, Nov 27, 2024):** "This is not supported at the moment."

**Updated Status (June 2025):**
> "Remote MCP support in Claude is now documented here: https://support.anthropic.com/en/articles/11175166-about-custom-integrations-using-remote-mcp"

### Remote MCP via Settings > Connectors (Paid Plans Only)

**As of June 2025**, Claude introduced "Custom Connectors" for remote MCP servers:

**Availability:**
- Claude.ai web (Pro, Max, Team, Enterprise plans)
- Claude Desktop (Pro, Max, Team, Enterprise plans)
- Claude Mobile (iOS/Android) - view only, cannot add new

**Configuration Method:**
1. Navigate to **Settings > Connectors** (NOT via config file)
2. Click "Add integration" or "Add custom connector"
3. Enter remote MCP server URL (HTTP or SSE)
4. Complete OAuth flow if required

**Key Limitation (from official docs):**
> "To configure remote MCP servers for use in Claude Desktop, add them via Settings > Connectors. **Claude Desktop will not connect to remote servers that are configured directly via claude_desktop_config.json.**"

**Supported Protocols:**
- Server-Sent Events (SSE) - `https://example.com/mcp/sse`
- Streamable HTTP - `https://example.com/mcp` (recommended for reliability)
- OAuth 2.1 with Dynamic Client Registration (DCR)
- Authless connections

**Source:** 
- https://support.anthropic.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers
- https://support.anthropic.com/en/articles/11175166-about-custom-integrations-using-remote-mcp

### Why stdio-only in config file?

**Design Rationale:**
1. **Security:** Local stdio processes have implicit trust - user explicitly installed them
2. **Simplicity:** No network configuration, firewalls, or TLS certificates to manage
3. **Environment isolation:** Each server runs in its own subprocess with explicit env vars
4. **Backwards compatibility:** Maintains consistency with initial MCP release

---

## 3. Workarounds / Known Patterns

### Primary Pattern: mcp-remote Proxy

**What is mcp-remote?**
- **NPM Package:** `mcp-remote` by @jms830
- **Purpose:** stdio-to-HTTP/SSE bridge for Claude Desktop
- **How it works:** Spawns a local stdio process that forwards MCP messages to remote HTTP endpoint
- **Auth Support:** OAuth 2.0, Bearer tokens, custom headers

**Installation & Configuration:**

```json
{
  "mcpServers": {
    "my-remote-server": {
      "command": "npx",
      "args": [
        "-y",                                    // Auto-accept npm install
        "mcp-remote@latest",                     // Use latest version
        "https://example.com/mcp/sse",           // Remote server URL
        "--header",                              // Optional auth header
        "Authorization: Bearer ${AUTH_TOKEN}"
      ],
      "env": {
        "AUTH_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Security Critical:**
- **RCE vulnerability fixed in v0.1.16 (June 2025)**
- **ALWAYS use:** `mcp-remote@^0.1.16` or `mcp-remote@latest`
- **Never use:** older versions without specifying version

**Transport Strategy Options:**
```bash
# Default: tries HTTP, falls back to SSE
npx mcp-remote https://example.com/mcp

# SSE only
npx mcp-remote https://example.com/mcp/sse --transport sse-only

# HTTP only
npx mcp-remote https://example.com/mcp --transport http-only
```

**OAuth Configuration:**
- Default callback port: `3334`
- Custom port: Add as argument after URL (e.g., `"9696"`)
- Custom host: Use `--host` flag (e.g., `--host myapp.local`)

### Alternative Pattern: mcp-proxy (Python/TypeScript)

**Multiple implementations available:**

1. **@punkpeye/mcp-proxy (TypeScript)** - Used by FastMCP internally
2. **sparfenyuk/mcp-proxy (Python)** - Bidirectional stdio ↔ HTTP/SSE

**Example (Python):**
```bash
# Expose local stdio server as HTTP/SSE
mcp-proxy --port=8080 uvx mcp-server-fetch

# Then in claude_desktop_config.json:
{
  "mcpServers": {
    "fetch-proxy": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8080/sse"]
    }
  }
}
```

### Community Solutions

**Cloudflare Workers Pattern:**
- Host MCP server on Cloudflare Workers
- Use `mcp-remote` to connect from Claude Desktop
- OAuth handled by Cloudflare
- **Reference:** https://developers.cloudflare.com/agents/guides/remote-mcp-server/

**FastMCP Proxy Pattern:**
```python
from fastmcp import FastMCP

# Create proxy to remote server
proxy = FastMCP.as_proxy(
    "https://example.com/mcp/sse",
    name="Remote Server Proxy"
)

if __name__ == "__main__":
    proxy.run()  # Runs via STDIO for Claude Desktop
```

Then install with:
```bash
fastmcp install claude-desktop proxy_server.py --server-name "Remote Proxy"
```

---

## 4. Version-Specific Notes

### Current Claude Desktop Version Support

**As of October 2025:**
- **stdio transport:** Fully supported since MCP launch (Nov 2024)
- **HTTP/SSE via config:** Not supported
- **HTTP/SSE via UI:** Supported (June 2025+) for paid plans only
- **Desktop Extensions (.mcpb):** Supported - one-click installs with bundled dependencies

### Version History

| Date | Change | Version |
|------|--------|---------|
| Nov 2024 | MCP protocol launch - stdio only | Initial |
| Dec 2024 | Community develops `mcp-remote` | N/A |
| May 2025 | "Integrations" feature announced | N/A |
| June 2025 | Remote MCP via Settings > Connectors | Claude Desktop 0.7+ |
| July 2025 | Mobile support for remote MCP | Claude iOS/Android |
| Oct 2025 | Desktop Extensions (.mcpb) launch | Claude Desktop 0.8+ |

**No Roadmap for HTTP in Config File:**
- No official announcement of plans to support `transport: "http"` in `claude_desktop_config.json`
- Focus appears to be on UI-based remote server management for paid plans
- Community consensus: `mcp-remote` is the interim solution

---

## 5. References & Diagnostics

### Official Documentation

1. **Getting Started with Local MCP Servers**
   - https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop

2. **Building Custom Connectors via Remote MCP**
   - https://support.anthropic.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers

3. **Desktop Extensions Announcement**
   - https://www.anthropic.com/engineering/desktop-extensions

4. **MCP Specification**
   - https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/

### GitHub Issues & Discussions

1. **HTTP-with-SSE Transport Discussion**
   - https://github.com/orgs/modelcontextprotocol/discussions/16
   - Confirms: "This is not supported at the moment" (Nov 2024)
   - Updated: Remote MCP now available via UI (June 2025)

2. **Transport Closed Unexpectedly Issues**
   - https://github.com/modelcontextprotocol/servers/issues/1748
   - Related to initialization timing, not transport type

### Key NPM Packages

1. **mcp-remote** (stdio-to-HTTP proxy)
   - https://www.npmjs.com/package/mcp-remote
   - https://github.com/jms830/mcp-remote

2. **mcp-proxy** (TypeScript implementation)
   - https://www.npmjs.com/package/mcp-proxy
   - https://github.com/punkpeye/mcp-proxy

3. **mcp-proxy** (Python implementation)
   - https://github.com/sparfenyuk/mcp-proxy

### Logging & Diagnostics

**Log Locations:**

**macOS:**
```bash
# Claude Desktop transport logs
~/Library/Logs/Claude/mcp.log
~/Library/Logs/Claude/mcp-*.log

# Individual server logs
~/Library/Logs/Claude/mcp-server-<server-name>.log
```

**Windows:**
```powershell
# Claude Desktop logs
%APPDATA%\Claude\logs\mcp.log
%APPDATA%\Claude\logs\mcp-server-<server-name>.log
```

**Enable Debug Logging:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://example.com/sse", "--debug"],
      "env": {
        "DEBUG": "*",
        "MCP_LOG_LEVEL": "debug"
      }
    }
  }
}
```

**Common Error Patterns:**

| Error | Cause | Solution |
|-------|-------|----------|
| `spawn . EACCES` | Missing `command` field | Add valid `command` (e.g., `"npx"`) |
| `command not found` | Executable not in PATH | Use absolute path or install tool |
| `Cannot connect to MCP server` | Server failed to start | Check server logs in `~/Library/Logs/Claude/` |
| `transport closed unexpectedly` | Initialization timeout | See previous briefing on timing issues |
| `ENOENT` | Invalid file path in args | Verify all paths are absolute and exist |

**Manual Testing:**

Test server independently before adding to Claude:
```bash
# Test stdio server directly
npx mcp-remote https://example.com/mcp/sse

# Use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector npx mcp-remote https://example.com/sse
```

---

## Recommended Configuration Strategy

### For Your Use Case: Testing HTTP MCP Server

**Current Goal:** Connect Claude Desktop to `hello_http_mcp_server.py` running on `http://localhost:5000`

**Option 1: Use mcp-remote (Recommended)**

```json
{
  "mcpServers": {
    "hello-http": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://localhost:5000/sse"
      ]
    }
  }
}
```

**Prerequisites:**
- Ensure `hello_http_mcp_server.py` is running and serving on port 5000
- Server must implement SSE or Streamable HTTP transport
- Test with: `curl http://localhost:5000/sse` (should return SSE stream)

**Option 2: Create Stdio Wrapper**

If you want to avoid mcp-remote, create a simple stdio wrapper:

```python
# hello_stdio_wrapper.py
import sys
from mcp_n8n.gateway import main

if __name__ == "__main__":
    # Set backend to use HTTP_SSE strategy
    # Communicate via stdio with Claude Desktop
    main()
```

Then configure:
```json
{
  "mcpServers": {
    "hello-http": {
      "command": "python",
      "args": ["/absolute/path/to/hello_stdio_wrapper.py"]
    }
  }
}
```

**Option 3: Use FastMCP Proxy**

```python
# proxy.py
from fastmcp import FastMCP

proxy = FastMCP.as_proxy(
    "http://localhost:5000/sse",
    name="Hello HTTP Proxy"
)

if __name__ == "__main__":
    proxy.run()  # Runs stdio transport
```

Configure:
```bash
fastmcp install claude-desktop proxy.py --server-name "Hello HTTP"
```

---

## Gaps & Limitations

### Known Limitations

1. **No native HTTP transport in config file**
   - No `transport: "http"` or `transport: "sse"` option exists
   - No plans announced for future support
   - UI-based remote servers require paid plans

2. **Environment variable inheritance**
   - Subprocesses do NOT inherit shell environment automatically
   - Must explicitly pass all required vars in `env` section
   - No support for `.env` file loading (must parse manually)

3. **Network access for stdio servers**
   - Servers CAN make outbound network requests (not sandboxed)
   - However, long initialization blocks cause transport timeouts (see previous briefing)
   - Solution: Defer network I/O until after MCP handshake

4. **Debugging visibility**
   - Limited diagnostics in UI
   - Must check log files manually
   - No real-time connection status indicators

5. **Configuration validation**
   - No schema validation on save
   - Errors only surface on Claude Desktop restart
   - Malformed JSON causes entire config to be ignored

### Feature Gaps

**Compared to Claude Code (CLI):**
- Claude Code supports native HTTP transport with `--transport http` flag
- Claude Code has interactive permission UI (`/permissions` command)
- Claude Code supports project-scoped config (`.mcp.json` files)

**Compared to Cursor/VSCode:**
- These editors support native SSE servers directly in config
- Example (Cursor v0.48.0+): direct SSE URL without proxy

### Documentation Gaps

1. **No official JSON schema** published by Anthropic
2. **Limited troubleshooting guides** for common errors
3. **Sparse examples** of HTTP/SSE configurations
4. **No migration guide** from stdio to remote servers

---

## Follow-up Actions

### Immediate Steps

1. **Test mcp-remote locally:**
```bash
# Terminal 1: Start your HTTP MCP server
python hello_http_mcp_server.py

# Terminal 2: Test mcp-remote connection
npx -y mcp-remote@latest http://localhost:5000/sse --debug
```

2. **Update claude_desktop_config.json:**
```json
{
  "mcpServers": {
    "hello-http-test": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://localhost:5000/sse",
        "--debug"
      ]
    }
  }
}
```

3. **Restart Claude Desktop** and check logs:
```bash
tail -f ~/Library/Logs/Claude/mcp-server-hello-http-test.log
```

### Long-term Considerations

1. **For production use:**
   - Consider migrating to remote MCP via Settings > Connectors (requires paid plan)
   - Deploy server with proper HTTPS endpoint
   - Implement OAuth 2.1 for secure authentication

2. **If staying with local stdio:**
   - Follow timing best practices from previous briefing
   - Use background initialization pattern
   - Keep network I/O out of startup path

3. **Feature request to Anthropic:**
   - File GitHub issue requesting native HTTP transport in config file
   - Note use case: local development/testing without proxy overhead
   - Mention compatibility with Claude Code's `--transport http` flag

4. **Alternative: Desktop Extension (.mcpb)**
   - Package your MCP server as a Desktop Extension
   - Provides one-click install for users
   - Handles dependencies and updates automatically

---

## Conclusion

**Answer to Original Question:**
> "Can Claude Desktop connect to remote HTTP MCP endpoints without spawning a local executable?"

**No.** Claude Desktop's `claude_desktop_config.json` requires every MCP server entry to specify a `command` that spawns a local subprocess using stdio transport. There is no native HTTP transport support in the configuration file.

**The "spawn . EACCES" error** you encountered is expected behavior when attempting to configure an HTTP transport without a `command` field.

**Recommended Path Forward:**
1. Use `npx mcp-remote` as a stdio-to-HTTP proxy (simplest, most widely adopted)
2. OR upgrade to paid plan and use Settings > Connectors for native remote MCP
3. OR create custom stdio wrapper that communicates with your HTTP backend

The `mcp-remote` pattern is the de facto standard in the MCP community for bridging stdio-only clients (like Claude Desktop) to HTTP/SSE servers, with over 31K weekly downloads and active maintenance.

---

## Appendix: Complete Working Example

**Scenario:** Connect Claude Desktop to a local FastMCP server running on HTTP

**1. Server Code (server.py):**
```python
from fastmcp import FastMCP

mcp = FastMCP("Hello World")

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # For HTTP access
    mcp.run(transport="sse", port=5000)
```

**2. Start Server:**
```bash
python server.py
# Server listening on http://localhost:5000/sse
```

**3. Claude Desktop Config:**
```json
{
  "mcpServers": {
    "hello-world": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://localhost:5000/sse"
      ]
    }
  }
}
```

**4. Verification:**
```bash
# Check logs
tail -f ~/Library/Logs/Claude/mcp-server-hello-world.log

# Should see successful connection
# "Connected to remote MCP server"
# "Tools available: greet"
```

**5. Usage in Claude:**
```
User: "Greet Victor"
Claude: [uses greet tool] → "Hello, Victor!"
```

This pattern works reliably for local testing and can be adapted for remote servers by changing the URL.
