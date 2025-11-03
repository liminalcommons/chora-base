# chora-compose MCP Server Testing Results

**Date**: 2025-11-02
**Context**: Week 5 Integration Decision - Testing MCP server to choose Path A/B vs Path C
**Docker Container**: `chora-compose-mcp:latest` running on port 8000 (healthy, 14 hours uptime)

---

## Test Environment

### Docker Status ✅
```bash
$ docker ps | grep chora-compose
f1ef0275630a   chora-compose-mcp:latest   "python -m chora_com…"   14 hours ago   Up 14 hours (healthy)   0.0.0.0:8000->8000/tcp
```

**Status**: Container running and healthy
**Port**: 8000 (NOT 8001 as in config - may need config update)
**Uptime**: 14 hours
**Health**: Healthy

### MCP Configuration

**Expected Configuration** (from claude_desktop_config.json):
- Type: `sse`
- URL: `http://localhost:8001/sse`
- Timeout: 60 seconds
- Auto-approved tools: 24 tools

**Actual Docker Port**: 8000

**Action Required**: Update Claude Desktop config to use port 8000, or update Docker to use port 8001

---

## Test Plan

### Phase 1: Connection Testing (Claude Desktop Required)

Since MCP testing requires the Claude Desktop app (not Claude Code), the following tests need to be performed in Claude Desktop:

#### 1. Connection Verification
- [ ] Open Claude Desktop app
- [ ] Start new conversation
- [ ] Check if `chora-compose` server appears in tools list
- [ ] Verify 24 tools are available

#### 2. Core Tool Testing
**Test these tools to verify basic functionality**:

1. **`choracompose__hello_world`**
   - Purpose: Test MCP connection
   - Expected: Connection confirmation message
   - Result: PENDING

2. **`choracompose__list_generators`**
   - Purpose: List available generators
   - Expected: List of generator types (template, AI, etc.)
   - Result: PENDING

3. **`choracompose__list_artifact_configs`**
   - Purpose: Check existing artifact configs
   - Expected: List of configured artifacts
   - Result: PENDING

4. **`choracompose__list_content_configs`**
   - Purpose: Check existing content configs
   - Expected: List of content configurations
   - Result: PENDING

#### 3. Configuration Tool Testing
**Test interactive config creation workflow**:

5. **`choracompose__draft_config`**
   - Purpose: Draft new configuration interactively
   - Test Case: Create inbox coordination request content config
   - Expected: Interactive prompts for config structure
   - Result: PENDING

6. **`choracompose__test_config`**
   - Purpose: Test configuration before saving
   - Test Case: Validate drafted config structure
   - Expected: Validation results
   - Result: PENDING

7. **`choracompose__save_config`**
   - Purpose: Save configuration to disk
   - Test Case: Save drafted coordination request config
   - Expected: Config file created on disk
   - Result: PENDING

#### 4. Generation Tool Testing
**Test content and artifact generation**:

8. **`choracompose__generate_content`**
   - Purpose: Generate content from config
   - Test Case: Generate "request_id" content block
   - Expected: Generated content matching pattern
   - Result: PENDING

9. **`choracompose__batch_generate`**
   - Purpose: Generate multiple content pieces
   - Test Case: Generate all 15 coordination request content blocks
   - Expected: All 15 content blocks generated
   - Result: PENDING

10. **`choracompose__assemble_artifact`**
    - Purpose: Assemble artifact from content configs (CRITICAL TEST)
    - Test Case: Generate complete coordination request JSON
    - Expected: Assembled JSON artifact with all fields
    - Result: PENDING

#### 5. Validation Tool Testing
**Test quality assurance capabilities**:

11. **`choracompose__validate_content`**
    - Purpose: Validate content against schema
    - Test Case: Validate generated coordination request
    - Expected: Validation pass/fail with details
    - Result: PENDING

12. **`choracompose__check_freshness`**
    - Purpose: Check content freshness (v1.9.0 feature)
    - Test Case: Check if content configs are up-to-date
    - Expected: Freshness status for each config
    - Result: PENDING

#### 6. Dependency & Utility Testing

13. **`choracompose__trace_dependencies`**
    - Purpose: Trace config dependencies
    - Test Case: Trace coordination request artifact dependencies
    - Expected: Dependency graph showing all content configs
    - Result: PENDING

14. **`choracompose__cleanup_ephemeral`**
    - Purpose: Clean up temporary content
    - Test Case: Clean up test-generated content
    - Expected: Ephemeral content removed
    - Result: PENDING

---

## Phase 2: Config Compatibility Assessment

### Test with Week 3 Content Configs

We have 15 content configs created in Week 3:
1. `content-block-request_id.json`
2. `content-block-type.json`
3. `content-block-title.json`
4. `content-block-from_repo.json`
5. `content-block-to_repo.json`
6. `content-block-priority.json`
7. `content-block-urgency.json`
8. `content-block-description.json`
9. `content-block-context_background.json`
10. `content-block-context_rationale.json`
11. `content-block-deliverables.json`
12. `content-block-acceptance_criteria.json`
13. `content-block-timeline_milestones.json`
14. `content-block-estimated_effort.json`
15. `content-block-dependencies.json`

**Compatibility Questions**:
- [ ] Can chora-compose load our existing content configs?
- [ ] Do config schemas match between Week 3 design and chora-compose expectations?
- [ ] Can we use chora-compose artifact assembly with our configs?
- [ ] Do we need to restructure configs to match chora-compose format?

**Format Comparison**:

**Our Week 3 Format**:
```json
{
  "type": "content",
  "id": "content-block-request_id",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "type": "coordination",
    "version": "1.0",
    "title": "Request ID Content Block"
  },
  "elements": [
    {
      "id": "request_id_field",
      "generation_pattern": "template_fill",
      "example_output": "COORD-2025-NNN"
    }
  ]
}
```

**chora-compose Expected Format** (need to verify):
- PENDING: Test with `choracompose__list_content_configs` to see actual format
- PENDING: Check schema compatibility
- PENDING: Determine if restructuring needed

---

## Phase 3: Post-Processing Integration

### Requirement
Our inbox protocol requires 4-step post-processing:
1. Validate schema
2. Allocate request_id
3. Emit event to events.jsonl
4. Promote file from draft/ to incoming/

**Integration Questions**:
- [ ] Does chora-compose support post-generation hooks?
- [ ] Can we call `scripts/process-generated-artifact.py` after `assemble_artifact`?
- [ ] Do we need to build a wrapper script?
- [ ] Can chora-compose emit events to our events.jsonl format?

**Test Case**:
1. Generate coordination request using `assemble_artifact`
2. Run `scripts/process-generated-artifact.py` on output
3. Verify all 4 steps execute successfully
4. Check if request_id allocation works
5. Verify event emission

---

## Phase 4: Inbox Generation Workflow Test

### Complete End-to-End Test

**Goal**: Generate a real coordination request from start to finish

**Steps**:
1. Use `choracompose__draft_config` to create artifact config
2. Use `choracompose__batch_generate` to generate all 15 content blocks
3. Use `choracompose__assemble_artifact` to create final JSON
4. Run post-processing: `python3 scripts/process-generated-artifact.py <output>`
5. Verify final artifact in `inbox/incoming/coordination/`

**Success Criteria**:
- ✅ All 15 content blocks generated correctly
- ✅ Artifact assembly produces valid JSON
- ✅ Post-processing completes all 4 steps
- ✅ Final coordination request passes schema validation
- ✅ Request appears in inbox dashboard (`python3 scripts/inbox-status.py`)

**Test Coordination Request**:
- Title: "Test MCP Generation Workflow"
- Type: coordination
- From: chora-base
- To: chora-workspace
- Priority: P3
- Urgency: exploratory

---

## Decision Criteria

### Path A/B Criteria (Use chora-compose MCP tools)
**Choose this path if ALL criteria met**:
- ✅ Docker container running and accessible
- ✅ 24 MCP tools functional in Claude Desktop
- ✅ `assemble_artifact` can generate coordination requests
- ✅ Config format compatible (or easily adaptable)
- ✅ Post-processing can integrate (via wrapper or hooks)
- ✅ End-to-end test generates valid coordination request

**Estimated Effort**: 8-16 hours
**Risk**: MEDIUM (depends on config compatibility)

### Path C Criteria (Build standalone generator)
**Choose this path if ANY critical capability missing**:
- ❌ MCP tools not accessible from Claude Desktop
- ❌ `assemble_artifact` cannot generate inbox artifacts
- ❌ Config format incompatible (major restructuring needed)
- ❌ Post-processing cannot integrate
- ❌ End-to-end test fails

**Estimated Effort**: 20-30 hours
**Risk**: LOW (full control, proven Week 3 configs)

---

## Test Results Summary

**Status**: PENDING - Requires Claude Desktop testing

**Docker Status**: ✅ Running (port 8000, healthy)
**MCP Connection**: ⚠️ Port mismatch (config says 8001, Docker uses 8000)
**Tool Testing**: PENDING (requires Claude Desktop)
**Config Compatibility**: PENDING
**Post-processing**: PENDING
**End-to-End**: PENDING

---

## Next Steps

### Immediate (Before Proceeding with Implementation)
1. **Update Claude Desktop Config** to use port 8000 instead of 8001
   ```json
   {
     "mcpServers": {
       "chora-compose": {
         "type": "sse",
         "url": "http://localhost:8000/sse",  // Changed from 8001
         "timeout": 60,
         "disabled": false,
         "autoApprove": [/* 24 tools */]
       }
     }
   }
   ```

2. **Open Claude Desktop App** and perform Phase 1-4 tests

3. **Document Results** in this file

4. **Make Decision**: Path A/B or Path C based on test outcomes

### If Path A/B (MCP tools work)
- Create MCP wrapper scripts
- Adapt Week 3 configs to chora-compose format (if needed)
- Build post-processing integration
- Estimated: 8-16 hours over 2 weeks

### If Path C (MCP tools insufficient)
- Implement standalone generator
- Reuse Week 3 content configs as-is
- Build generation engine (literal, template, AI generators)
- Estimated: 20-30 hours over 2-3 weeks

---

**Test Date**: PENDING
**Tester**: PENDING
**Decision**: PENDING

**Related Documents**:
- [chora-compose Integration Decision](chora-compose-integration-decision.md)
- [MCP Integration Notes](mcp-integration-notes.md)
- [Week 4 Results](chora-compose-pilot-week4-results.md)
- CORD-2025-004: Coordination request to chora-compose team
