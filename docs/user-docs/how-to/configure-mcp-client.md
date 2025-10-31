# How to Configure MCP Clients

**Last Updated**: 2025-10-29
**Time Estimate**: 5-10 minutes
**Difficulty**: Beginner

---

## Claude Desktop (Recommended)

### macOS Configuration

1. **Locate config file**:
   ```bash
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add MCP server**:
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["-m", "my_mcp_server.server"],
         "cwd": "/Users/yourname/projects/my-mcp-server"
       }
     }
   }
   ```

3. **Restart Claude Desktop** (Cmd+Q, then reopen)

### Windows Configuration

1. **Locate config file**:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Add server** (same JSON as macOS)

3. **Restart Claude Desktop**

### Multiple Servers

```json
{
  "mcpServers": {
    "tasks": {
      "command": "python",
      "args": ["-m", "taskmanager.server"],
      "cwd": "/path/to/taskmanager"
    },
    "docs": {
      "command": "python",
      "args": ["-m", "docgen.server"],
      "cwd": "/path/to/docgen"
    }
  }
}
```

---

## Cursor IDE

1. Open Settings → Extensions → MCP
2. Add server configuration:
   ```json
   {
     "command": "python",
     "args": ["-m", "my_mcp_server.server"],
     "cwd": "/path/to/my-mcp-server"
   }
   ```

---

## Cline (VS Code Extension)

1. Install Cline extension
2. Open Command Palette (Cmd+Shift+P)
3. Search: "Cline: Configure MCP Servers"
4. Add server JSON

---

## Environment Variables

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server.server"],
      "cwd": "/path/to/my-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/my-mcp-server",
        "DEBUG": "true",
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

---

## Using uv (Fast Python Installer)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/my-mcp-server",
        "run",
        "my_mcp_server.server"
      ]
    }
  }
}
```

---

## Troubleshooting

### Server Not Appearing

1. Check config file syntax (valid JSON)
2. Verify paths are absolute (not relative)
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### Import Errors

Add PYTHONPATH:
```json
{
  "env": {
    "PYTHONPATH": "/path/to/my-mcp-server"
  }
}
```

---

## Related Documentation

- [Implement MCP Server](implement-mcp-server.md) - Build your server
- [Test MCP Tools](test-mcp-tools.md) - Test your setup
- [SAP-014 Adoption Blueprint](../../skilled-awareness/mcp-server-development/adoption-blueprint.md)

---

**Last Updated**: 2025-10-29
