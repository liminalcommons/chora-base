---
title: Remove an MCP Server from Configuration
audience: end-users
difficulty: intermediate
time: 2-5 minutes
wave: 1.2-1.3
version: v0.1.5
---

# Remove an MCP Server from Configuration

> **💡 First time?** See [Complete Workflow Guide](complete-workflow.md) Part 2A.5 for basic removal workflow. This guide is a **deep dive on removal operations and draft state management**.

**Goal:** Understand how to remove servers from draft configuration, clear entire drafts, and manage draft state during removal operations.

**Prerequisites:**
- [Get Started](get-started.md) - mcp-orchestration installed
- At least one server in your draft

---

## Understanding Server Removal

**Key concepts:**

**Draft-only operation:** Removal affects only the in-memory draft, not published configurations.

**Server name vs Server ID:** Remove by the name used in your config (which may differ from the registry server_id if you used a custom name).

**Reversible:** Add servers back before publishing if you remove incorrectly.

---

## Removal Methods

### Via Claude (Recommended)

**Single server removal:**
```
> Remove filesystem from config
> Remove github from config
> Remove my-custom-server from config
```

**Clear entire draft:**
```
> Clear the draft configuration
```

### Via CLI

```bash
# View current draft first
mcp-orchestration view-draft

# For programmatic removal, see Reference: MCP Tools API
```

---

## Server Name Resolution

**Server Name** = What it's called in your config (what you remove)
**Server ID** = The registry identifier (what you add)

**Standard case (names match):**
```
Server ID: "filesystem"
Server Name: "filesystem"

> Remove filesystem from config  ✅
```

**Custom name case:**
```
Server ID: "filesystem"
Server Name: "my-docs" (custom name you specified)

> Remove my-docs from config      ✅
> Remove filesystem from config   ❌ (won't find it)
```

**How to check:** `> Show me the current draft`

Use the exact name from the draft server list.

---

## Common Removal Patterns

### Pattern 1: Fix Incorrect Parameters

**Use case:** Server added with wrong configuration

```bash
# Wrong path was used
> Remove filesystem from config

# Add with correct path
> Add filesystem server for /Users/me/Documents

# Verify
> Show me the draft
```

---

### Pattern 2: Clear and Rebuild

**Use case:** Start completely fresh

```bash
# Nuclear option - removes ALL servers
> Clear the draft configuration

# Verify empty draft
> Show me the draft
# Expected: "Your draft is currently empty (0 servers)"

# Rebuild from scratch
> Add memory server
> Add filesystem server for /Users/me/Projects
```

---

### Pattern 3: Selective Removal

**Use case:** Keep some servers, remove others

```bash
# Current: filesystem, github, memory, slack
# Goal: Keep filesystem and memory only

> Remove github from config
> Remove slack from config

# Verify final state
> Show me the draft
# Expected: filesystem, memory
```

---

### Pattern 4: Replace Server

**Use case:** Switch server types

```bash
# Switch from PostgreSQL to SQLite
> Remove postgres from config
> Add sqlite server with path /path/to/db.sqlite
```

---

## Draft State After Removal

**What happens:**

1. **Validation:** Check if server name exists in draft
2. **Removal:** Server removed from in-memory draft
3. **Response:** Updated draft returned with new server count

**State tracking:**

```
Before removal:
- server_count: 3
- servers: [filesystem, github, memory]

After "Remove github from config":
- server_count: 2
- servers: [filesystem, memory]
```

**Important:** The change is NOT permanent until you publish.

---

## Removing from Published Configurations

**Key insight:** Published configs are immutable artifacts. You cannot "edit" them.

**To remove a server from published config:**

1. **Remove from draft:**
   ```
   > Remove [server-name] from config
   ```

2. **Publish new version:**
   ```
   > Publish config with changelog "Removed [server-name]"
   ```

3. **Result:**
   - New version created without the server
   - Old version still exists (versioned, can roll back)

---

## Troubleshooting

### Error: "Server not found in draft"

**Cause:** Server name doesn't exist in current draft

**Solution 1 - Check exact name:**
```
> Show me the draft
```
Use the exact name from the server list.

**Solution 2 - Check for custom names:**

If you added with custom name, use that name:
```
# You added as:
> Add filesystem server with name "work-files" and path /work

# Remove using custom name:
> Remove work-files from config
```

**Solution 3 - Verify draft not empty:**
```
> Show me the draft
```
If `server_count: 0`, nothing to remove.

---

### Removed Wrong Server

**Cause:** Accidentally removed incorrect server

**Solution 1 - Add back immediately:**
```
> Add [server-name] server with [original parameters]
```
Draft isn't published, so changes are reversible.

**Solution 2 - Check server details if parameters forgotten:**
```
> Describe the [server-id] server
```
Review required parameters, then re-add.

---

### Cannot Remove After Publishing

**Symptom:** Want to remove server from published config

**Solution:** Publishing creates immutable artifacts. See [Removing from Published Configurations](#removing-from-published-configurations) above.

---

## Batch Operations

**Current limitation:** One server at a time via Claude:

```bash
> Remove filesystem from config
> Remove github from config
> Remove memory from config
```

**Faster alternative - Clear entire draft:**

```bash
> Clear the draft configuration
```

Then rebuild with only the servers you want. This is more efficient for removing 3+ servers.

---

## Technical Details

### How remove_server_from_config Works

1. **Validate:** Check server_name exists in draft.servers
2. **Remove:** Delete server entry from draft
3. **Update count:** Decrement draft.server_count
4. **Return:** Updated draft state

### Draft State Management

**In-memory:** Draft cleared on MCP server restart

**No persistence:** Add and publish immediately to avoid losing work

**Idempotent:** Removing non-existent server returns error (doesn't silently succeed)

---

## Common Server Removal Scenarios

**Development cleanup:**
- Remove test servers before production publish
- Clear draft after experimentation

**Configuration refinement:**
- Remove servers with wrong parameters
- Replace servers with alternatives

**Security:**
- Remove servers with exposed credentials
- Clear draft containing sensitive data

**Profile management:**
- Remove servers specific to one environment
- Build clean profile-specific configs

---

## Next Steps

1. **Verify draft state:** `> Show me the current draft`
2. **Add replacement servers (if needed):** See [Add Server to Config](add-server-to-config.md)
3. **Publish updated configuration:** See [Publish a Configuration](publish-config.md)
4. **Deploy changes:** See [Complete Workflow Guide](complete-workflow.md) Part 3

---

## See Also

- [Complete Workflow Guide](complete-workflow.md) - End-to-end workflow
- [Add Server to Config](add-server-to-config.md) - Add servers (pair to this guide)
- [View Draft Configuration](view-draft-config.md) - Inspect current draft
- [Clear Draft Configuration](clear-draft-config.md) - Remove all servers at once
- [Publish a Configuration](publish-config.md) - Make changes permanent
- [Reference: MCP Tools API](../reference/mcp-tools.md#remove_server_from_config) - Programmatic usage

---

**Key insight:** The draft is your workspace. Removal operations are reversible until you publish. Use this freedom to experiment and refine your configuration.
