---
title: Remove an MCP Server from Configuration
audience: end-users
difficulty: beginner
time: 2 minutes
wave: 1.2-1.3
version: v0.1.3
---

# Remove an MCP Server from Configuration

**Goal:** Remove an MCP server from your draft configuration.

**Time:** 2 minutes

**Prerequisites:**
- [Get Started](get-started.md) - mcp-orchestration configured
- At least one server in your draft

---

## Quick Reference

Ask Claude:

> Remove [server-name] from config

**Examples:**
- "Remove filesystem from config"
- "Remove github from config"
- "Remove my-custom-server from config"

---

## Step-by-Step

### Step 1: Check What's in Your Draft

> Show me the current draft configuration

Look for the server names. Example response:

```
Your draft has 3 servers:
1. filesystem
2. github
3. memory
```

### Step 2: Remove the Server

Use the exact server name from step 1:

> Remove filesystem from config

**Response:**

```
✓ Removed filesystem from configuration

Current draft now has 2 servers:
- github
- memory
```

### Step 3: Verify Removal

> Show me the draft

The server should no longer appear in the list.

---

## Common Scenarios

### Scenario 1: Wrong Parameters

You added a server with incorrect parameters:

```
# You added:
filesystem with path /wrong/path

# Fix it:
> Remove filesystem from config
> Add filesystem server with path /correct/path
```

### Scenario 2: No Longer Needed

You don't need a server anymore:

```
> Remove brave-search from config
```

### Scenario 3: Replace with Different Server

Switching from PostgreSQL to SQLite:

```
> Remove postgres from config
> Add sqlite server with path /path/to/db.sqlite
```

### Scenario 4: Start Completely Over

Remove everything and start fresh:

```
> Clear the draft configuration
```

This removes ALL servers at once. See [Pattern 2](#pattern-2-clear-everything) below.

---

## Important Notes

### Server Names vs Server IDs

**Server Name** = What it's called in your config (what you remove)
**Server ID** = The registry identifier (what you add)

**Usually they're the same:**
```
Server ID: "filesystem"
Server Name: "filesystem"

> Remove filesystem from config  ✅
```

**But they can differ if you used a custom name:**
```
Server ID: "filesystem"
Server Name: "my-docs" (custom name you specified)

> Remove my-docs from config  ✅
> Remove filesystem from config  ❌ (won't find it)
```

### Removal Only Affects Draft

**Before publishing:**
- `remove_server_from_config` removes from draft
- Draft changes are reversible (add it back)

**After publishing:**
- Published configs are immutable
- To "remove" from published config: remove from draft, then publish again
- Old version still exists (versioned)

---

## Common Patterns

### Pattern 1: Remove and Re-Add

**Use case:** Fix parameters

```bash
# Wrong path
> Remove filesystem from config

# Correct path
> Add filesystem server with path /Users/me/Documents

# Verify
> Show me the draft
```

### Pattern 2: Clear Everything

**Use case:** Start completely fresh

```bash
# Nuclear option - removes ALL servers
> Clear the draft configuration

# Verify
> Show me the draft
# Should show: "Your draft is currently empty (0 servers)"

# Start building new config
> Add memory server
> Add filesystem server with path /Users/me/Projects
```

### Pattern 3: Selective Removal

**Use case:** Keep some servers, remove others

```bash
# Current draft has: filesystem, github, memory, slack

# Only keep filesystem and memory
> Remove github from config
> Remove slack from config

# Verify
> Show me the draft
# Should show: filesystem, memory
```

---

## Troubleshooting

### "Server not found in draft"

**Symptom:** Error saying server doesn't exist in configuration

**Solutions:**

1. **Check the exact server name**

   > Show me the draft

   Use the exact name from the list

2. **Check if using custom name**

   If you added with custom name, use that name:

   ```
   # You added as:
   > Add filesystem server with name "work-files"

   # Remove using custom name:
   > Remove work-files from config
   ```

3. **Draft might be empty**

   > Show me the draft

   If empty (server_count: 0), nothing to remove

### Removed wrong server

**Symptom:** Accidentally removed the wrong one

**Solutions:**

1. **Add it back immediately**

   > Add [server-name] server with [original parameters]

   The draft isn't published yet, so you can undo

2. **If you forgot the parameters**

   > Describe the [server-id] server

   Check the parameters required, then re-add

### Can't remove after publishing

**Symptom:** Want to remove server from published config

**Solution:**

Publishing creates immutable artifacts. To "remove" a server:

1. **Remove from draft**

   > Remove [server-name] from config

2. **Publish new version**

   > Publish config with changelog "Removed [server-name]"

3. **Old version still exists**

   Previous versions with the server are preserved (can roll back if needed)

---

## What Happens When You Remove?

1. **Validation** - Check if server name exists in draft
2. **Removal** - Server removed from in-memory draft
3. **Response** - Updated draft returned with new server count

**The change is NOT permanent until you publish.**

---

## Batch Operations

Currently, you can only remove one server at a time via Claude:

```bash
> Remove filesystem from config
> Remove github from config
> Remove memory from config
```

**Faster alternative** - Clear entire draft:

```bash
> Clear the draft configuration
```

Then rebuild with only the servers you want.

---

## Next Steps

After removing servers:

1. **Verify the draft**

   > Show me the current draft

2. **Add replacement servers** (if needed)

   See [Add an MCP Server](add-server-to-config.md)

3. **Publish the updated configuration**

   See [Publish a Configuration](publish-config.md)

---

## See Also

- [Add an MCP Server to Config](add-server-to-config.md) - Add servers
- [View Draft Configuration](view-draft-config.md) - Inspect current draft
- [Clear Draft Configuration](clear-draft-config.md) - Remove all servers at once
- [Publish a Configuration](publish-config.md) - Save your changes
- [Reference: remove_server_from_config](../reference/mcp-tools.md#remove_server_from_config) - API details

---

**Remember:** Removal only affects the draft. You can always add servers back before publishing!
