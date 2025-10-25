---
title: Get Started with mcp-orchestration
audience: end-users
difficulty: beginner
time: 10 minutes
wave: 1.0-1.3
version: v0.1.3
---

# Get Started with mcp-orchestration

**Goal:** Install mcp-orchestration, configure it in Claude Desktop, and initialize signing keys.

**Time:** 10 minutes

---

## Step 1: Install mcp-orchestration

Install via pip:

```bash
pip install mcp-orchestration
```

**Verify installation:**

```bash
mcp-orchestration --version
```

Expected output: `mcp-orchestration v0.1.3`

---

## Step 2: Configure Claude Desktop

### macOS

1. Open Claude Desktop configuration file:

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add mcp-orchestration server:

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

**If you already have other servers**, add `"mcp-orchestration"` to the existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "..."
    },
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

3. **Save the file**

### Windows

1. Open configuration file at:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the same configuration as macOS above

3. **Save the file**

### Linux

1. Open configuration file at:
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. Add the same configuration as macOS above

3. **Save the file**

---

## Step 3: Restart Claude Desktop

**Important:** Completely quit Claude Desktop (not just close the window), then reopen it.

**macOS:** `Cmd+Q` to quit, then reopen from Applications
**Windows:** Right-click taskbar icon → Quit, then reopen
**Linux:** Kill the process, then restart

---

## Step 4: Test the Connection

Open Claude Desktop and start a new conversation. Ask:

> What MCP servers are available?

**Expected response:** Claude should list available servers including:
- brave-search
- filesystem
- github
- memory
- (and 10+ more)

**If this works**, mcp-orchestration is connected! ✅

**If this doesn't work**, see [Troubleshooting](#troubleshooting) below.

---

## Step 5: Initialize Signing Keys

Still in Claude Desktop, say:

> Initialize the signing keys

**Expected response:**

```
✓ Signing keys initialized successfully!

Keys stored at: /Users/yourname/.mcp-orchestration/keys/

You're now ready to publish configurations.
```

**What happened:**
- Ed25519 key pair generated
- Private key saved at `~/.mcp-orchestration/keys/signing.key` (mode 0600)
- Public key saved at `~/.mcp-orchestration/keys/signing.pub`

---

## You're Ready!

You now have:
- ✅ mcp-orchestration installed
- ✅ Server configured in Claude Desktop
- ✅ Signing keys initialized
- ✅ Access to 13 MCP tools through Claude

---

## What's Next?

**Build your first configuration:**
- [Tutorial: Your First MCP Configuration](../tutorials/01-first-configuration.md) - Hands-on walkthrough

**Manage servers:**
- [Add an MCP Server to Your Config](add-server-to-config.md) - Add servers like filesystem, GitHub, etc.
- [Remove a Server from Config](remove-server-from-config.md) - Remove unwanted servers

**Explore available servers:**
- [Browse Available MCP Servers](browse-servers.md) - See all 15+ servers

**Manage clients:**
- [Add a New MCP Client](add-new-client.md) - Register new clients (e.g., Cursor)

---

## Troubleshooting

### Claude doesn't list servers

**Symptom:** When you ask "What MCP servers are available?", Claude says it doesn't understand or can't access the tool.

**Solutions:**

1. **Check config file syntax**

   Validate JSON at https://jsonlint.com/

   Common mistakes:
   - Missing comma between servers
   - Trailing comma after last server
   - Quotes not matching

2. **Check Claude Desktop logs**

   macOS:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

   Look for errors mentioning "mcp-orchestration"

3. **Verify mcp-orchestration is in PATH**

   ```bash
   which mcp-orchestration
   ```

   Should return a path like `/usr/local/bin/mcp-orchestration`

   If not found, pip install may have failed

4. **Restart Claude Desktop properly**

   Ensure you fully quit (not just close window)

   Check Activity Monitor (macOS) or Task Manager (Windows) to confirm no Claude processes running

### Keys already exist

**Symptom:** `initialize_keys` says "Signing keys already exist"

**Solution:** This is normal! You only need to initialize once. Your keys are ready to use.

To regenerate (if keys are corrupted):

> Initialize the signing keys with regenerate set to true

### Permission denied

**Symptom:** Error about file permissions when initializing keys

**Solution:**

```bash
# Check .mcp-orchestration directory permissions
ls -la ~/.mcp-orchestration

# Fix permissions if needed
chmod 700 ~/.mcp-orchestration
chmod 700 ~/.mcp-orchestration/keys
```

### Import errors

**Symptom:** Python import errors in logs

**Solution:**

```bash
# Reinstall with dependencies
pip uninstall mcp-orchestration
pip install mcp-orchestration

# Or upgrade
pip install --upgrade mcp-orchestration
```

---

## Alternative: CLI Initialization

If you prefer command-line initialization instead of Claude Desktop:

```bash
# Initialize keys via CLI
mcp-orchestration-init

# This creates:
# - ~/.mcp-orchestration/keys/signing.key (private)
# - ~/.mcp-orchestration/keys/signing.pub (public)
# - Sample configurations (optional)
```

**Note:** CLI init creates sample configs that may not be needed. Using Claude Desktop's `initialize_keys` tool is recommended for most users.

---

## Understanding What You Installed

**mcp-orchestration is an MCP server** that provides configuration management tools:

- **13 MCP tools** accessible through Claude Desktop
- **5 MCP resources** for browsing capabilities
- **6 CLI commands** for terminal use
- **Local storage** at `~/.mcp-orchestration/`

**It does NOT:**
- Replace Claude Desktop (it works with Claude)
- Require internet connection (local-first)
- Share data with external services
- Modify your existing configs (until you publish)

---

## Success Criteria

You're ready to move on when:
- [ ] `pip show mcp-orchestration` shows v0.1.3
- [ ] Claude Desktop config includes "mcp-orchestration"
- [ ] Claude responds to "What MCP servers are available?"
- [ ] Signing keys exist at `~/.mcp-orchestration/keys/`
- [ ] No errors in Claude Desktop logs

---

**Need help?** See [Troubleshooting](#troubleshooting) or file an issue at [github.com/liminalcommons/mcp-orchestration](https://github.com/liminalcommons/mcp-orchestration).
