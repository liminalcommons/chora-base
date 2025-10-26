---
title: Manage MCP Configurations with Claude Desktop
audience: end-users
difficulty: beginner
time: 15 minutes
wave: 1.3-1.5
version: v0.1.5
---

# Manage MCP Configurations with Claude Desktop

Learn how to manage your MCP server configurations directly through conversations with Claude Desktop. No command-line required!

## What You'll Learn

- How to set up signing keys through Claude
- How to add MCP servers to your configuration
- How to check what's in your configuration
- How to fix mistakes and start over
- How to save your configuration

## Prerequisites

- Claude Desktop installed
- MCP Orchestration server configured in Claude Desktop
- 10 minutes

## Before You Start

Make sure you've added the MCP Orchestration server to your Claude Desktop configuration. You should have this in your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "/path/to/python",
      "args": ["-m", "mcp_orchestrator.mcp.server"],
      "env": {"PYTHONPATH": "/path/to/mcp-orchestration/src"}
    }
  }
}
```

##

 Step 1: Initialize Signing Keys (First Time Only)

Before you can save configurations, you need to set up cryptographic keys. Don't worry - Claude can do this for you!

**What to say to Claude:**

> "Initialize the signing keys for MCP orchestration"

**What Claude will do:**

Claude will generate a pair of cryptographic keys and save them securely on your computer. You'll see a response like:

```
✓ Signing keys initialized successfully!

Keys are stored at:
  /Users/you/.mcp-orchestration/keys/

You're now ready to publish configurations.
```

**Important:** You only need to do this once. If you've already initialized keys, Claude will tell you they already exist.

## Step 2: Discover Available Servers

Find out what MCP servers you can add:

**What to say to Claude:**

> "What MCP servers are available?"

**What Claude will show you:**

A list of all available servers with descriptions:

- **Filesystem** - Access local files and directories
- **GitHub** - Integrate with GitHub repositories
- **Memory** - Persistent storage for conversations
- **Brave Search** - Web search capabilities
- **And 10+ more...**

## Step 3: Add Your First Server

Let's start by adding a filesystem server so Claude can access your documents:

**What to say to Claude:**

> "Add a filesystem server that can access my Documents folder"

**What Claude will do:**

1. Call the `add_server_to_config` tool
2. Configure the filesystem server with the path to your Documents folder
3. Show you the current configuration

You'll see a confirmation like:

```
✓ Added filesystem server to your configuration!

Current draft has 1 server:
- filesystem (accessing /Users/you/Documents)
```

## Step 4: Add More Servers

Continue adding servers to build your configuration:

**Example conversations:**

> "Add the memory server too"

> "Add GitHub integration" *(Claude will ask for your GitHub token)*

> "Add Brave Search" *(Claude will ask for your API key)*

Each time you add a server, Claude shows you the updated server count.

## Step 5: Check Your Configuration

At any point, you can see what's in your configuration:

**What to say to Claude:**

> "Show me my current draft configuration"

or simply:

> "What's in my draft?"

**What Claude will show you:**

```
Your current draft configuration has 3 servers:

1. filesystem - accessing /Users/you/Documents
2. memory - persistent storage
3. github - GitHub integration

Here's the complete configuration:
[Full JSON configuration shown]
```

**Why this is useful:**
- Confirms your servers are there
- Shows exact paths and settings
- Helps you spot mistakes before saving

## Step 6: Save Your Configuration

When you're happy with your configuration, save it:

**What to say to Claude:**

> "Publish this configuration with a note that I added filesystem, memory, and GitHub servers"

**What Claude will do:**

1. Sign your configuration with your cryptographic key
2. Save it as a versioned artifact
3. Give you a confirmation with an artifact ID

You'll see:

```
✓ Configuration published successfully!

Artifact ID: 7941a154d02dae62345198ae9b858d4db2aaa8546a62fb50b8302c56ae653afd
Created: 2025-10-24
Servers: 3
Changelog: Added filesystem, memory, and GitHub servers

Your configuration is now saved and signed.
```

## Made a Mistake? Start Over!

If you added the wrong server or want to try a different setup:

**What to say to Claude:**

> "Clear my draft configuration"

or:

> "Start over with the configuration"

**What Claude will do:**

Remove all servers from your draft, giving you a clean slate. You can then build a new configuration from scratch.

**Checking it's cleared:**

> "Show me the draft"

You should see:

```
Your draft is currently empty (0 servers).
```

## Real Example Conversation

Here's a complete example of managing your configuration:

**You:** Initialize the signing keys

**Claude:** ✓ Signing keys initialized successfully!

**You:** What servers are available?

**Claude:** Here are the available MCP servers: [lists all servers]

**You:** Add filesystem server for /Users/me/Documents

**Claude:** ✓ Added filesystem server (1 server in draft)

**You:** Add memory server

**Claude:** ✓ Added memory server (2 servers in draft)

**You:** Show me the draft

**Claude:** Your draft has 2 servers: filesystem, memory [shows full config]

**You:** Publish this with changelog "Initial setup"

**Claude:** ✓ Configuration published! Artifact ID: 7941a154...

**You:** Deploy this configuration to Claude Desktop

**Claude:** ✓ Configuration deployed! Restart Claude Desktop to use the new servers.

*Restart Claude Desktop (⌘Q then reopen)*

**You:** What servers do I have?

**Claude:** [Lists: mcp-orchestration, filesystem, memory, and your other servers]

✅ **Success!** Your servers are now available in Claude Desktop.

## Step 7: Deploy Your Configuration

Once you've published your configuration, deploy it to Claude Desktop to actually use the servers.

**What to say to Claude:**

> "Deploy my latest configuration to Claude Desktop"

or simply:

> "Deploy to Claude"

**What Claude will do:**

1. Retrieve your latest published configuration
2. Verify its cryptographic signature
3. Write it to Claude Desktop's config file
4. Record the deployment

You'll see a response like:

```
✓ Configuration deployed successfully!

Deployed artifact: abc123...
Config location: ~/Library/Application Support/Claude/claude_desktop_config.json
Deployed at: 2025-10-25T14:30:00Z

⚠️  Restart Claude Desktop for changes to take effect:
  killall Claude && open -a 'Claude'
```

**Important:** You must restart Claude Desktop after deployment!

### Restart Claude Desktop

**macOS:**
```bash
killall Claude && open -a 'Claude'
```

**Or manually:**
1. Quit Claude Desktop completely (⌘Q, not just close window)
2. Open Claude Desktop again

**Windows/Linux:**
- Close Claude completely
- Reopen from Start menu / application launcher

### Verify Deployment

After restart, check that your servers are available:

**What to say:**

> "What MCP servers do I have available?"

**What to expect:**

Claude should list all your servers:
- mcp-orchestration
- filesystem
- memory
- (any others you added)

### Test Your Servers

Try using your newly deployed servers:

**Test filesystem:**
> "List files in my Documents folder"

**Test memory:**
> "Remember that my favorite programming language is Python"
> *(later)* "What's my favorite programming language?"

If these work, your deployment succeeded! 🎉

## Update Existing Configuration

Already have a deployed config and want to add more servers? Easy!

**What to say:**

> "Add the github server to my configuration"
> *(Claude will ask for your GitHub token)*

> "Show me what changed"

> "Publish with note: Added GitHub integration"

> "Deploy to Claude Desktop"

Then restart Claude Desktop. Your new server is added!

## Tips for Success

### Tip 1: Check Before Publishing

Always view your draft before publishing to make sure everything is correct:

> "Show me the draft before I publish"

### Tip 2: Use Descriptive Changelogs

When publishing, include a note about what you changed:

✅ Good: "Added filesystem for Documents and GitHub for repo access"
❌ Bad: "Updated config"

### Tip 3: Iterative Building

Build your configuration gradually:
1. Add one server
2. Check the draft
3. Add another server
4. Check again
5. Publish when satisfied

### Tip 4: Don't Worry About Mistakes

You can always:
- Clear the draft and start over (before publishing)
- Remove individual servers
- Publish a new version (after publishing)

## Common Questions

### Q: Do I need to specify "claude-desktop" when adding servers?

**A:** No! The tools automatically default to claude-desktop. Just say "add filesystem server" and Claude handles the rest.

### Q: What happens to my old configuration when I publish a new one?

**A:** The old configuration is preserved. Each published configuration gets a unique version (artifact ID). You can view history later (Wave 1.6 feature).

### Q: Can I see the exact configuration before it's published?

**A:** Yes! Just ask Claude to "show me the draft" and you'll see the complete JSON configuration.

### Q: What if I forget my signing keys?

**A:** The keys are stored on your computer at `~/.mcp-orchestration/keys/`. If you lose them, you can regenerate with:

> "Regenerate my signing keys"

### Q: Can Claude access my files after I add the filesystem server?

**A:** Not until you deploy! After adding the filesystem server, you must:
1. Publish the configuration
2. Deploy it to Claude Desktop
3. Restart Claude Desktop

Then Claude can access the specified folder.

## Troubleshooting

### "Error: Signing key not found"

**Solution:** Initialize keys first:
> "Initialize signing keys"

### "Error: Cannot publish empty configuration"

**Solution:** Add at least one server before publishing:
> "Add memory server"

### Draft seems empty after adding servers

**Solution:** View the draft to verify:
> "Show me the draft"

If it's truly empty, try adding the server again or restart Claude Desktop.

### Can't find a specific server

**Solution:** Ask Claude to list available servers:
> "What servers are available?"
> "Search for database servers"

## What's Next?

After mastering configuration management, you can:

1. **Rollback to previous versions** - Deploy older artifact IDs (see [Complete Workflow](complete-workflow.md#use-case-d-rollback-to-previous-version))
2. **Detect configuration drift** - Compare deployed vs latest (see [Complete Workflow](complete-workflow.md#use-case-e-detect-configuration-drift))
3. **View history** - See all your past configurations (Wave 1.6 - coming soon)
4. **Share configurations** - Export artifact IDs for team members

## Summary

You've learned how to:
- ✅ Initialize signing keys through conversation
- ✅ Discover available MCP servers
- ✅ Add servers to your configuration
- ✅ View your draft at any time
- ✅ Clear and start over if needed
- ✅ Publish signed configurations
- ✅ Deploy configurations to Claude Desktop
- ✅ Update existing configurations

All through natural conversation with Claude - no command-line required!

**Complete workflow:** Initialize → Discover → Add → View → Publish → Deploy → Verify ✅

## Need Help?

If you run into issues:
1. Check the [troubleshooting section](#troubleshooting) above
2. View the [technical guide](../../dev-docs/how-to/manage-draft-workflow.md) for developers
3. Report issues at [github.com/your-repo/mcp-orchestration](https://github.com)

---

*This guide covers Wave 1.3-1.5 features (build, publish, deploy). For complete workflow including CLI alternatives, see [Complete Workflow](complete-workflow.md).*
