---
title: Understanding the Draft Workflow
audience: end-users
difficulty: beginner
wave: 1.2-1.3
version: v0.1.3
---

# Understanding the Draft Workflow

mcp-orchestration uses a **draft → publish** workflow for building configurations. This document explains why and how this pattern works.

## The Problem with Direct Editing

### Traditional Approach

Most configuration systems work like this:

1. Edit a JSON file directly
2. Save the file
3. Restart the application
4. Hope it works

**Problems:**
- **Mistakes are immediate** - A typo breaks your working config
- **No undo** - Once you save, the old version is gone
- **No preview** - Can't see the full config before committing
- **Error-prone** - JSON syntax errors are easy to make
- **Atomic changes only** - Hard to build complex configs incrementally

### The Draft Alternative

mcp-orchestration uses a different pattern:

1. Build configuration incrementally in a "draft"
2. Preview the draft anytime without committing
3. Make changes until satisfied
4. Publish as an immutable, signed artifact

**Benefits:**
- **Mistakes are recoverable** - Draft can be cleared and restarted
- **Full preview** - See exactly what will be published
- **Guided construction** - Tools validate as you build
- **Incremental** - Add servers one at a time, checking progress
- **Reversible** - Published configs are versioned, drafts are ephemeral

## How Drafts Work

### Draft State

A draft is **in-memory, ephemeral state** stored in the MCP server process:

```
Client: claude-desktop
Profile: default
Draft:
  └─ Servers:
      ├─ filesystem: {path: "/Users/me/Documents"}
      ├─ github: {env: GITHUB_TOKEN}
      └─ memory: {}
```

This draft exists only while the MCP server is running. It's not saved to disk until you explicitly publish.

### Draft Lifecycle

```
1. [Empty] ────────────────┐
                           │
2. add_server ──→ [Draft]  │  (add servers)
                     │      │
3. view_draft ───────┘      │  (inspect)
                     │      │
4. add_server ──→ [Draft]  │  (add more)
                     │      │
5. publish_config ──→ [Published Artifact]  (immutable)
                     or
6. clear_draft ──→ [Empty]  (start over)
```

**Key insight:** You can cycle through steps 2-4 as many times as needed before committing to step 5.

## The Workflow Steps

### Step 1: Initialize Keys (Once)

```typescript
await initialize_keys()
```

Creates cryptographic keys for signing. Only needed once per machine.

**Why separate?** Key generation is a one-time setup. Keeping it separate makes the rest of the workflow cleaner.

### Step 2: Build Draft (Iterative)

```typescript
// Add first server
await add_server_to_config(
  server_id="filesystem",
  params={"path": "/Users/me/Documents"}
)

// Check progress
await view_draft_config()

// Add another
await add_server_to_config(
  server_id="memory"
)

// Check again
await view_draft_config()
```

**Key behavior:** Draft persists across operations. You can add server → view → add server → view in a loop.

**Why this matters:** Building complex configs (5+ servers) requires seeing progress. The draft is your working space.

### Step 3: Publish (Atomic)

```typescript
await publish_config(
  changelog="Added filesystem and memory servers"
)
```

**What happens:**
1. Draft is validated (not empty, all required params present)
2. Draft is transformed into client-specific JSON format
3. JSON is hashed (SHA-256) to create artifact ID
4. JSON is signed with your private key
5. Signed artifact is saved to disk
6. Draft remains in memory (not cleared)

**Why atomic?** Publishing either succeeds completely or fails completely. You never get partial/corrupt artifacts.

### Step 4: Clear Draft (Optional)

```typescript
await clear_draft_config()
```

Removes all servers from draft, returning to empty state.

**When to use:**
- Made mistakes and want to start over
- Switching to a completely different configuration
- Finished and want a clean slate

**When NOT to use:**
- After publishing (if you plan to iterate on the published config)
- Just to remove one server (use `remove_server_from_config` instead)

## Design Rationale

### Why Not Auto-Save?

Auto-saving (like Google Docs) wasn't chosen because:

**Configurations are executable code:**
- Bad config = broken AI assistant
- Need explicit "I'm ready" moment
- Want ability to preview before committing

**Signatures require intent:**
- Signing is a statement of approval
- Can't auto-sign in background
- User must consciously publish

**Versioning needs boundaries:**
- Each publish creates a distinct version
- Versions need changelog/metadata
- Can't have 50 micro-versions from auto-save

### Why Not Direct Publish?

A "publish without draft" approach (construct + publish in one call) wasn't chosen because:

**Complexity:**
- Adding 5 servers requires 5 separate publish operations
- Each publish requires signing, storage, validation
- Can't preview full config before publishing

**Error recovery:**
- If server 4 fails, servers 1-3 are already published
- Reversing requires manual rollback
- Wastes artifact IDs on partial configs

**User experience:**
- No way to see full picture before committing
- Can't build incrementally with feedback
- Increases anxiety about making mistakes

### Why Not Direct File Editing?

Users could directly edit `claude_desktop_config.json` and skip mcp-orchestration entirely. Why add this layer?

**Validation:**
- Catches errors before they break Claude Desktop
- Verifies server IDs exist in registry
- Ensures required parameters are present

**Transport abstraction:**
- HTTP/SSE servers need mcp-remote wrapping
- Users don't need to know this detail
- Config builder handles it automatically

**Versioning:**
- Direct edits have no history
- Can't easily revert to "last working config"
- No audit trail of changes

**Signing:**
- Manual signing is error-prone
- Can't verify authenticity of direct edits
- No proof of who changed what

## State Management

### Where is Draft Stored?

**In-memory** in the MCP server process:

```python
_builders: dict[str, ConfigBuilder] = {}
# Key: "claude-desktop/default"
# Value: ConfigBuilder instance with servers
```

**Not persisted to disk** - Draft exists only while MCP server runs.

**Per client/profile** - Each combination has its own draft:
- `claude-desktop/default` - separate draft
- `claude-desktop/dev` - separate draft
- `cursor/default` - separate draft

### What Happens on Restart?

When MCP server restarts (Claude Desktop restarts):

**Draft is lost:**
- All unpublished changes disappear
- Start fresh with empty draft

**Published artifacts remain:**
- All published configs are on disk
- Can retrieve via `get_config`
- Signatures still valid

**Recommendation:** Publish frequently if building large configs, or complete in one session.

### Multi-Session Scenario

**Session 1:**
```typescript
await add_server_to_config(server_id="filesystem")
await add_server_to_config(server_id="memory")
// [Claude Desktop restarts]
```

**Session 2:**
```typescript
await view_draft_config()
// Returns: { draft: {mcpServers: {}}, server_count: 0 }
// ❌ Draft was lost
```

**Solution:** Publish before closing:
```typescript
await add_server_to_config(server_id="filesystem")
await add_server_to_config(server_id="memory")
await publish_config(changelog="Added filesystem and memory")
// ✅ Now persisted, can continue later
```

## Comparison with Other Patterns

### Git Workflow

**Similarities:**
- Working directory (draft) vs committed history (published)
- Stage changes incrementally
- Explicit commit with message (publish with changelog)

**Differences:**
- Git tracks files, mcp-orchestration tracks configuration
- Git has branches, mcp-orchestration is linear
- Git has distributed remotes, mcp-orchestration is local-first

### Database Transactions

**Similarities:**
- Begin transaction (start draft)
- Make changes (add/remove servers)
- Commit or rollback (publish or clear)

**Differences:**
- Databases have ACID guarantees, drafts are ephemeral
- Databases persist across restarts, drafts don't
- Databases have isolation levels, drafts are single-user

### E-Commerce Shopping Cart

**Similarities:**
- Add items to cart (add servers to draft)
- View cart anytime (view draft)
- Checkout when ready (publish)
- Clear cart to start over (clear draft)

**Differences:**
- Cart persists (cookies/session), draft is in-memory
- Cart has quantity, draft has configuration
- Cart checkout involves payment, draft publish involves signing

## Best Practices

### Practice 1: Preview Before Publishing

Always view the draft before publishing:

```typescript
await view_draft_config()  // Check servers are correct
await publish_config()      // Then commit
```

**Why:** Catches mistakes before they're signed and versioned.

### Practice 2: Publish Milestones

For complex configs, publish incrementally:

```typescript
// Add core servers
await add_server_to_config(server_id="filesystem")
await add_server_to_config(server_id="memory")
await publish_config(changelog="Added core servers")

// Add integrations
await add_server_to_config(server_id="github")
await add_server_to_config(server_id="slack")
await publish_config(changelog="Added integrations")
```

**Why:** Each publish is a save point you can revert to.

### Practice 3: Use Changelogs

Include meaningful changelogs:

```typescript
✅ Good: "Added filesystem for Documents, GitHub for repos"
❌ Bad: "Updated config"
```

**Why:** Future-you will thank you when reviewing history.

### Practice 4: Clear After Publishing (Sometimes)

If starting a completely new config:

```typescript
await publish_config(changelog="Production config v1")
await clear_draft_config()  // Start fresh for v2
```

**Why:** Prevents accidentally including v1 servers in v2.

## Trade-offs

### Advantages

✅ **Safe experimentation** - Draft can be discarded
✅ **Incremental building** - Add servers one at a time
✅ **Full preview** - See complete config before committing
✅ **Explicit versioning** - Each publish is a distinct version
✅ **Error recovery** - Clear draft to start over

### Disadvantages

❌ **State loss on restart** - Draft disappears if MCP server restarts
❌ **Extra step** - Must explicitly publish (can't just "save")
❌ **Learning curve** - More concepts than direct file editing
❌ **Memory overhead** - Draft stored in RAM (negligible for configs)

## Future Directions

The draft workflow enables future features:

**Draft persistence:**
- Auto-save drafts to disk
- Resume after restart
- Named drafts for different use cases

**Collaborative editing:**
- Multiple users editing same draft
- Merge conflict resolution
- Real-time preview

**Advanced validation:**
- Test draft against schema before publishing
- Simulate config without publishing
- Dependency analysis

**Version control integration:**
- Export draft as Git commit
- Import from version control
- Diff against Git history

## Summary

The draft workflow provides:
- **Safety** through preview and reversibility
- **Flexibility** through incremental building
- **Quality** through explicit publishing
- **Traceability** through signed versions

**Mental model:** Draft is your scratch pad, publish is your permanent record.

---

**See Also:**
- [Tutorial: Your First Configuration](../tutorials/01-first-configuration.md) - Experience the workflow
- [How-To: Manage Configs with Claude](../how-to/manage-configs-with-claude.md) - Practical usage
- [Reference: Configuration Building Tools](../reference/mcp-tools.md#configuration-building) - API details
