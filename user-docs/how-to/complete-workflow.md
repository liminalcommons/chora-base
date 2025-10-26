---
title: Complete Workflow - Zero to Deployed Configuration
audience: end-users
difficulty: beginner
time: 20-25 minutes
wave: 1.0-1.5
version: v0.1.5
---

# Complete Workflow: Zero to Deployed Configuration

**What you'll accomplish:** Install mcp-orchestration, build a configuration, and deploy it to Claude Desktop.

**Time:** 20-25 minutes first time, 5-10 minutes for updates

**Who this is for:** Anyone who wants the complete picture, from installation through deployment and ongoing maintenance.

---

## Table of Contents

- [Part 1: First-Time Setup](#part-1-first-time-setup) (~5 min)
- [Part 2: Build Your Configuration](#part-2-build-your-configuration) (~10 min)
- [Part 3: Validate & Publish](#part-3-validate--publish) (~3 min)
- [Part 4: Deploy to Claude](#part-4-deploy-to-claude) (~5 min)
- [Part 5: Maintenance Workflows](#part-5-maintenance-workflows)
- [Troubleshooting](#troubleshooting)
- [Quick Reference](#quick-reference)

---

## Key Concepts

Before starting, understand these states:

- **Draft** - Working configuration in progress (not saved)
- **Published** - Signed and stored configuration with artifact ID
- **Deployed** - Configuration written to Claude Desktop's config file

**Workflow:** Draft → Validate → Publish → Deploy → Restart Claude

**Interfaces:** Each task can be done via conversational commands (in Claude) or CLI commands (in terminal).

---

## Part 1: First-Time Setup

### Step 1.1: Install

```bash
pip install mcp-orchestration
```

Verify installation:
```bash
mcp-orchestration --version
# Expected: mcp-orchestration v0.1.5
```

---

### Step 1.2: Add to Claude Desktop

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

Add mcp-orchestration to your config:

```json
{
  "mcpServers": {
    "mcp-orchestration": {
      "command": "mcp-orchestration"
    }
  }
}
```

If you have existing servers, add to the `mcpServers` object:
```json
{
  "mcpServers": {
    "existing-server": { "command": "..." },
    "mcp-orchestration": { "command": "mcp-orchestration" }
  }
}
```

**Restart Claude Desktop** completely (⌘Q on macOS, then reopen).

---

### Step 1.3: Initialize Signing Keys

**Conversational:**
```
"Initialize the signing keys for MCP orchestration"
```

**CLI:**
```bash
mcp-orchestration-init
```

**Expected:**
```
✓ Signing keys initialized successfully!

Keys stored at:
  /Users/you/.mcp-orchestration/keys/
  - signing.key (private - keep secure!)
  - signing.pub (public - shareable)
```

---

### Step 1.4: Verify Setup

**Conversational:**
```
"What MCP servers are available?"
```

**Expected:** Claude lists 15+ servers (filesystem, github, memory, brave-search, etc.)

If this works, setup is complete.

---

## Part 2: Build Your Configuration

Choose your scenario:
- **Scenario A:** Starting fresh (no existing config)
- **Scenario B:** Adding to existing config

### Scenario A: Starting Fresh

#### Discover Servers

**Conversational:**
```
"Show me all available MCP servers"
```

**CLI:**
```bash
mcp-orchestration-list-servers
```

**Expected:** List of 15+ servers with descriptions.

---

#### Add Servers

**Example: Add filesystem + memory + github**

| Task | Conversational | CLI |
|------|---------------|-----|
| **Filesystem** | `"Add a filesystem server for my Documents folder"` | `mcp-orchestration-add-server filesystem --client claude-desktop --profile default --param path=/Users/you/Documents` |
| **Memory** | `"Add the memory server"` | `mcp-orchestration-add-server memory --client claude-desktop --profile default` |
| **GitHub** | `"Add GitHub integration with my token"` (Claude prompts for token) | `mcp-orchestration-add-server github --client claude-desktop --profile default --env GITHUB_TOKEN=ghp_...` |

**After adding:**
```
✓ Added filesystem server to your configuration!

Current draft has 3 servers:
- filesystem (accessing /Users/you/Documents)
- memory (persistent storage)
- github (GitHub integration)
```

---

#### View Draft

**Conversational:**
```
"Show me my current draft configuration"
```

**Expected output shows:**
- Server count
- Configuration preview (JSON)
- Note: "This is your draft - not saved yet"

---

#### Fix Mistakes (Optional)

**Conversational:**
```
"Remove the github server from my draft"
"Clear my draft and start over"
```

**CLI:**
```bash
mcp-orchestration-remove-server github --client claude-desktop --profile default
```

Note: CLI drafts aren't persisted between commands. For stateful drafts, use conversational interface.

---

### Scenario B: Adding to Existing Config

#### View Current Config

**Conversational:**
```
"What's my current Claude Desktop configuration?"
```

**CLI:**
```bash
mcp-orchestration get-config claude-desktop default
```

Shows what's currently deployed.

---

#### Add Server

**Conversational:**
```
"Add a filesystem server to my config"
```

**CLI:**
```bash
mcp-orchestration-add-server filesystem \
  --client claude-desktop \
  --profile default \
  --param path=/Users/you/Documents
```

Claude adds to draft without affecting deployed config yet.

---

#### View Diff

**Conversational:**
```
"Show me the difference between my draft and current config"
```

**CLI:**
```bash
mcp-orchestration diff-config claude-desktop default
```

**Expected:**
```
Configuration Comparison:
Draft vs. Current (claude-desktop/default)

Status: DRIFT_DETECTED

Changes:
+ filesystem (added in draft)
  - Servers in draft: 4
  - Servers in current: 3
```

---

## Part 3: Validate & Publish

### Validate Configuration

**Conversational:**
```
"Validate my draft configuration"
```

**Expected (success):**
```
✓ Configuration validated successfully!
- Servers: 3
- Errors: 0
- Warnings: 0
```

**Expected (error):**
```
✗ Validation failed with 1 error:

[MISSING_ENV] Server 'github' requires GITHUB_TOKEN

Fix this before publishing.
```

**Fix errors:**
```
"Update the github server with my token: ghp_..."
```

Then validate again.

---

### Publish Configuration

**Conversational:**
```
"Publish this configuration with note: 'Added filesystem, memory, and github servers'"
```

**CLI:**
```bash
# First export draft to file (easier via Claude - CLI coming in future wave)
# Then publish:
mcp-orchestration-publish-config \
  --client claude-desktop \
  --profile default \
  --file my-config.json \
  --changelog "Added filesystem, memory, and github servers"
```

**Expected:**
```
✓ Configuration validated successfully
✓ Configuration signed with Ed25519
✓ Published successfully!

Artifact ID: abc123def456789...
Server count: 3
```

**Important:** Save the Artifact ID for rollbacks.

---

## Part 4: Deploy to Claude

### Deploy Latest Configuration

**Conversational:**
```
"Deploy my latest configuration to Claude Desktop"
```

**CLI:**
```bash
mcp-orchestration-deploy-config \
  --client claude-desktop \
  --profile default
```

**Expected:**
```
✓ Configuration deployed successfully!

Artifact ID: abc123def456...
Config path: /Users/you/Library/.../claude_desktop_config.json

⚠️  Restart the client application for changes to take effect
```

---

### Restart Claude Desktop

**macOS:** `killall Claude && open -a 'Claude'`
**Windows:** Close completely, reopen from Start menu
**Linux:** `pkill -f claude && claude-desktop &`

---

### Verify Deployment

**Conversational:**
```
"What MCP servers do I have available?"
```

**Expected:** Lists your servers (mcp-orchestration, filesystem, memory, github, plus any existing).

**Test servers:**
```
"List files in my Documents folder"          # Test filesystem
"Remember that my favorite color is blue"    # Test memory
"Show me my recent GitHub repositories"      # Test github
```

Success! Your configuration is deployed and working.

---

## Part 5: Maintenance Workflows

### Update Configuration

**Add new server:**

**Conversational:**
```
"Add the postgres server to my configuration"
"Show me what will change if I publish this"
"Validate this configuration"
"Publish it with note: 'Added postgres for database access'"
"Deploy it to Claude Desktop"
```

**CLI:**
```bash
# Add server
mcp-orchestration-add-server postgres \
  --client claude-desktop --profile default \
  --param connection=postgresql://localhost/db

# Publish (after exporting draft)
mcp-orchestration-publish-config \
  --client claude-desktop --profile default \
  --file updated-config.json \
  --changelog "Added postgres"

# Deploy
mcp-orchestration-deploy-config \
  --client claude-desktop --profile default

# Restart
killall Claude && open -a 'Claude'
```

**Time:** 2-3 minutes for updates.

---

### Rollback to Previous Version

If you saved artifact IDs from previous publishes:

**Conversational:**
```
"Deploy artifact abc123... to Claude Desktop"
```

**CLI:**
```bash
mcp-orchestration-deploy-config \
  --client claude-desktop \
  --profile default \
  --artifact-id abc123...
```

Then restart Claude Desktop.

Note: Wave 1.6 will add `list-deployment-history` tool. For now, track artifact IDs manually.

---

### Detect Configuration Drift

Check if published config differs from deployed:

**Conversational:**
```
"What configuration is currently deployed to Claude Desktop?"
"What's my latest published configuration?"
```

Compare artifact IDs:
- **Same ID:** No drift
- **Different IDs:** Drift detected (deployed is outdated)

**Fix drift:**
```
"Deploy my latest configuration"
```

---

## Troubleshooting

### Installation Issues

**`pip install` fails:**
```bash
pip install --user mcp-orchestration
# Or upgrade pip first:
pip install --upgrade pip && pip install mcp-orchestration
```

**Claude doesn't respond to MCP queries:**
1. Verify config file is valid JSON
2. Check mcp-orchestration in PATH: `which mcp-orchestration`
3. Restart Claude Desktop completely (⌘Q, not just window close)
4. Check Claude Desktop logs for errors

**Keys initialization fails:**
```bash
# Use CLI directly
mcp-orchestration-init

# Check permissions
ls -la ~/.mcp-orchestration/keys/
# signing.key should be -rw------- (600)
```

---

### Building Configuration

**Server not found:**
```
"List all available servers"
"Search for [keyword]"
```

**Draft is empty after adding servers:**
1. Try adding server again
2. Restart Claude Desktop
3. Use CLI as fallback

---

### Publishing & Deployment

**Validation error - Missing environment variable:**
```
"Update github server with token: ghp_..."
```

**Cannot publish empty configuration:**
Add at least one server before publishing.

**Signing key not found:**
```bash
mcp-orchestration-init
```

**Deploy succeeds but servers not available:**
Cause: Didn't restart Claude Desktop.
Fix: `killall Claude && open -a 'Claude'`

**Config file not found:**
Verify client/profile:
```bash
mcp-orchestration list-clients
```

**Signature verification failed:**
Re-publish the configuration.

---

## Quick Reference

### First-Time Setup
```bash
# Install
pip install mcp-orchestration

# Add to Claude Desktop config
# ~/Library/Application Support/Claude/claude_desktop_config.json
# Add: { "mcpServers": { "mcp-orchestration": { "command": "mcp-orchestration" } } }

# Restart Claude
killall Claude && open -a 'Claude'

# Initialize keys (via Claude)
"Initialize the signing keys for MCP orchestration"
```

---

### Common Commands

| Task | Conversational | CLI |
|------|---------------|-----|
| **List servers** | `"What MCP servers are available?"` | `mcp-orchestration-list-servers` |
| **Add server** | `"Add filesystem server for Documents"` | `mcp-orchestration-add-server filesystem --client claude-desktop --profile default --param path=/Users/you/Documents` |
| **View draft** | `"Show me my draft"` | (Use conversational interface) |
| **Validate** | `"Validate this configuration"` | (Runs automatically on publish) |
| **Publish** | `"Publish with note: 'Initial setup'"` | `mcp-orchestration-publish-config --client claude-desktop --profile default --file config.json --changelog "Initial setup"` |
| **Deploy** | `"Deploy to Claude Desktop"` | `mcp-orchestration-deploy-config --client claude-desktop --profile default` |
| **Check drift** | `"What's deployed vs latest?"` | `mcp-orchestration diff-config claude-desktop default` |
| **Rollback** | `"Deploy artifact abc123..."` | `mcp-orchestration-deploy-config --client claude-desktop --profile default --artifact-id abc123...` |

---

### Standard Workflow

**Build → Publish → Deploy:**

1. Add servers (conversational or CLI)
2. View and validate draft
3. Publish with changelog note
4. Deploy to client
5. Restart Claude Desktop
6. Verify servers available

**Update existing:**
Same workflow - new servers add to existing config.

---

## Advanced Topics

### Using Profiles

Manage multiple configurations per client:

```bash
# Dev profile with debugging servers
mcp-orchestration-add-server ... --profile dev

# Production profile with minimal servers
mcp-orchestration-add-server ... --profile prod

# Deploy specific profile
mcp-orchestration-deploy-config --client claude-desktop --profile prod
```

---

### Multiple Clients

Deploy configurations to different MCP clients:

```bash
# Deploy to Claude Desktop
mcp-orchestration-deploy-config --client claude-desktop

# Deploy to Cursor
mcp-orchestration-deploy-config --client cursor
```

Each client gets the appropriate config location automatically.

---

### Scripting Deployments

```bash
#!/bin/bash
# Deploy pre-built config

mcp-orchestration-deploy-config \
  --client claude-desktop \
  --profile default \
  --format json > deployment-result.json

if [ $? -eq 0 ]; then
  echo "✓ Deployment successful"
  cat deployment-result.json | jq '.artifact_id'
else
  echo "✗ Deployment failed"
  exit 1
fi
```

---

## What's Next?

### Wave 1.6: Audit & History (Coming Soon)
- `list_deployment_history` - See all past deployments
- `get_deployment_details` - Query specific deployment
- Deployment comparison tools
- Automated drift alerts

### Wave 2.x: Ecosystem Integration
- Remote deployment API
- Team configuration sharing
- Configuration templates
- Automated server discovery

---

## See Also

**Task-Specific Guides:**
- [Get Started](get-started.md) - Installation only
- [Add Server to Config](add-server-to-config.md) - Server configuration details
- [Manage Configs with Claude](manage-configs-with-claude.md) - Conversational workflow

**Reference:**
- [MCP Tools API](../reference/mcp-tools.md) - Complete API specifications
- [Cryptographic Signing](../explanation/cryptographic-signing.md) - How signatures work
- [Draft Workflow](../explanation/draft-workflow.md) - Understanding drafts

**Tutorials:**
- [Your First Configuration](../tutorials/01-first-configuration.md) - Guided learning

---

## Summary

You've learned the complete mcp-orchestration workflow:

- **Setup:** Install, configure, initialize keys
- **Build:** Discover servers, create configuration
- **Validate:** Check for errors before publishing
- **Publish:** Sign and save configuration
- **Deploy:** Apply to Claude Desktop
- **Maintain:** Update, rollback, detect drift

**Interfaces:** Both conversational (Claude) and CLI workflows covered.

**Questions or issues?** File an issue at [github.com/liminalcommons/mcp-orchestration](https://github.com/liminalcommons/mcp-orchestration)

**Documentation standard:** This guide follows [Diátaxis](https://diataxis.fr/) how-to format.
