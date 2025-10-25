# Wave 1.3: Claude Desktop Ergonomics

**Goal**: Improve user experience when interacting with mcp-orchestration through Claude Desktop by addressing confusion points and reducing friction.

## Problems Identified from User Testing

### 1. Parameter Format Confusion
**Issue**: Claude tried passing params as bare string first, got error, then figured out JSON string format.
```
First attempt: "params": "/Users/victorpiper/Documents"  ❌ Failed
Second attempt: "params": "{\"path\":\"/Users/victorpiper/Documents\"}"  ✅ Worked
```

**Why confusing**: The tool description shows `{"path": "/Users/me/Documents"}` but Claude needs to pass it as a JSON string.

**Solution**: Clearer documentation in tool description explaining the dual format.

### 2. Draft State Visibility
**Issue**: Claude wasn't sure if previously added servers persisted in draft after adding new ones.
- Added memory → server_count: 1
- Added filesystem → server_count: 1 (Claude wondered if memory was cleared)
- Added memory again → server_count: 2 (confirmed both persist)

**Why confusing**: No direct way to view draft without modifying it.

**Solution**: Add `view_draft_config` tool for read-only draft inspection.

### 3. No Way to Start Over
**Issue**: If Claude makes mistakes, no way to clear the draft and start fresh.

**Solution**: Add `clear_draft_config` tool.

### 4. Repetitive Parameters
**Issue**: Every tool call requires `client_id="claude-desktop"` and `profile_id="default"`.

**Solution**: Default these parameters to common values.

### 5. Key Initialization Not Automated
**Issue**: `publish_config` failed with "Run 'mcp-orchestration-init' to generate keys" but Claude can't help the user run this command.

**Solution**: Add `initialize_keys` tool so Claude can set up crypto for the user.

## Wave 1.3 Scope

### New Tools (3)

1. **`view_draft_config`** - View current draft without modifying
2. **`clear_draft_config`** - Clear all servers from draft
3. **`initialize_keys`** - Generate Ed25519 signing keys

### Breaking Changes (None)

- Default parameters are backward compatible
- New tools are additions, not modifications

### Documentation Improvements

1. **Add note to `add_server_to_config` description**:
   ```
   Note: When calling from Claude Desktop, params and env_vars are automatically
   parsed from JSON strings. You can pass {"path": "/tmp"} and it will be handled
   correctly.
   ```

2. **Add workflow guidance to tool descriptions**:
   - Reference related tools ("use view_draft_config to see current state")
   - Suggest common workflows ("typically: add → view → publish")

## Implementation Plan

### Phase 1: Core Tools
1. Add `view_draft_config` tool
2. Add `clear_draft_config` tool
3. Add `initialize_keys` tool

### Phase 2: Default Parameters
1. Update all Wave 1.2 tools to default `client_id="claude-desktop"`, `profile_id="default"`
2. Ensure backward compatibility with explicit values

### Phase 3: Documentation
1. Improve tool descriptions with clearer examples
2. Add cross-references between related tools
3. Document common workflows in tool help

### Phase 4: Testing
1. Unit tests for new tools
2. E2E test for full workflow with defaults
3. Manual testing in Claude Desktop

## Success Metrics

- Claude successfully completes workflow without parameter errors
- Claude knows when draft persists vs. when to check state
- Claude can recover from mistakes by clearing draft
- Claude can initialize keys autonomously

## Release Notes

Version 0.1.3 will include:
- 3 new MCP tools for better workflow management
- Default parameters reduce boilerplate
- Clearer documentation reduces confusion
- Autonomous key initialization
