---
title: Your First MCP Configuration
audience: beginners
difficulty: beginner
time: 15 minutes
wave: 1.3
version: v0.1.3
---

# Your First MCP Configuration

Welcome! In this tutorial, you'll create and publish your first MCP server configuration. By the end, you'll have a working configuration that gives Claude access to your files.

## What You'll Accomplish

You'll see with your own eyes:
- Claude Desktop talking to the mcp-orchestration server
- Your signing keys being created
- A filesystem server being added to your configuration
- Your configuration being signed and saved
- A unique artifact ID proving your success

**Time:** 15 minutes

## Before You Begin

You need:
- Claude Desktop installed and running
- Python 3.9 or later
- 15 minutes of uninterrupted time

## Step 1: Install mcp-orchestration

Open your terminal and run:

```bash
pip install mcp-orchestration
```

**What to expect:** You'll see installation messages. Wait until you see "Successfully installed mcp-orchestration".

## Step 2: Add the Server to Claude Desktop

Find your Claude Desktop configuration file. On macOS it's at:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Open it in a text editor and add:

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

**Important:** If you already have other servers, add `"mcp-orchestration"` to the existing `mcpServers` object.

Save the file.

## Step 3: Restart Claude Desktop

Quit Claude Desktop completely (not just close the window), then open it again.

**What to expect:** Claude Desktop reads the config file on startup. No error message means it worked.

## Step 4: Test the Connection

Open a new conversation with Claude and type:

> What MCP servers are available?

**What to expect:** Claude should respond with a list starting with "brave-search", "filesystem", "github", and more.

**If this doesn't work:** See the troubleshooting section at the end.

## Step 5: Create Your Signing Keys

Still in Claude, say:

> Initialize the signing keys

**What to expect:** Claude will respond with something like:

```
✓ Signing keys initialized successfully!

Keys stored at: /Users/yourname/.mcp-orchestration/keys/

You're now ready to publish configurations.
```

**Why this matters:** These keys let you sign your configurations, proving they came from you. You only do this once.

## Step 6: Add a Filesystem Server

Now let's give Claude access to a folder. Choose a safe folder for testing (like `~/Documents`).

Say to Claude:

> Add a filesystem server that can access my Documents folder

**What to expect:** Claude will confirm:

```
✓ Added filesystem server to your configuration!

Current draft has 1 server:
- filesystem (accessing /Users/yourname/Documents)
```

**See what happened?** You now have a draft configuration with one server in it.

## Step 7: Check Your Work

Let's look at what we built. Ask Claude:

> Show me my current draft configuration

**What to expect:** Claude will show you:

```
Your current draft has 1 server:

1. filesystem - accessing /Users/yourname/Documents

Configuration:
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/yourname/Documents"]
    }
  }
}
```

**This is important:** You can see exactly what will be saved before you save it.

## Step 8: Publish Your Configuration

You're happy with it, so let's save it. Say to Claude:

> Publish this configuration with a note: "My first configuration with filesystem access"

**What to expect:** Claude will respond with:

```
✓ Configuration published successfully!

Artifact ID: 8e91a062ff85a4180e571fd3821941aafa1b41d582582275aec426dae657c6de
Created: 2025-10-24
Servers: 1
Changelog: My first configuration with filesystem access

Your configuration is now saved and cryptographically signed.
```

**Success!** That long artifact ID is proof that you did it. It's unique to your configuration.

## What You Just Learned

Through doing, you learned:

1. **How to install** mcp-orchestration
2. **How to configure** Claude Desktop to use it
3. **How to test** the connection works
4. **How to create** cryptographic signing keys
5. **How to add** a server to your configuration
6. **How to view** your draft before saving
7. **How to publish** a signed configuration

## What You Built

You now have:
- ✅ Signing keys at `~/.mcp-orchestration/keys/`
- ✅ A published configuration stored as a cryptographically signed artifact
- ✅ A unique artifact ID you can reference later
- ✅ Knowledge of the basic workflow

## Next Steps

Now that you know the basics, you can:

1. **Add more servers** - Try adding the memory server or GitHub integration (see [How-to Guide: Add Servers](../how-to/manage-configs-with-claude.md))
2. **Understand signing** - Learn why cryptographic signatures matter (see [Explanation: Cryptographic Signing](../explanation/cryptographic-signing.md))
3. **Explore available servers** - Browse all 15+ servers in the registry (see [How-to Guide: Browse Servers](../how-to/browse-servers.md))

## Troubleshooting

### Claude doesn't respond to "What MCP servers are available?"

**Possible causes:**
1. Claude Desktop didn't restart properly
2. Configuration file has a JSON syntax error
3. mcp-orchestration isn't installed properly

**What to do:**
1. Quit Claude Desktop completely (check Activity Monitor on Mac)
2. Validate your JSON at https://jsonlint.com
3. Run `which mcp-orchestration` in terminal to verify installation

### "Error: Signing key not found"

**What happened:** You tried to publish before initializing keys.

**What to do:** Say to Claude: "Initialize the signing keys"

### Claude says "Tool not available"

**What happened:** The mcp-orchestration server isn't running.

**What to do:**
1. Check your `claude_desktop_config.json` has the right path
2. Restart Claude Desktop
3. Check Claude Desktop logs at `~/Library/Logs/Claude/mcp*.log`

### Different folder path shows up

**What happened:** Claude might interpret "Documents" differently.

**What to do:** Be specific: "Add filesystem server for /Users/yourname/Documents" (use your actual username)

## You Did It!

Congratulations! You've published your first cryptographically signed MCP configuration. You learned by doing, which means you can now repeat this workflow confidently.

---

**Need help?** See the [How-to Guides](../how-to/) for specific tasks or [Explanations](../explanation/) to understand concepts more deeply.
