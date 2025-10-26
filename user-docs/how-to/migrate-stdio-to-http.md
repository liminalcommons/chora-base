# How To: Migrate from stdio to HTTP Transport

**Difficulty:** Intermediate
**Time:** 15 minutes
**Prerequisites:** mcp-orchestration v0.2.0+, existing stdio setup
**Related:** [Deploy HTTP Server](deploy-http-server.md), [Authenticate HTTP API](authenticate-http-api.md)

---

## Overview

This guide shows you how to migrate from stdio transport (direct MCP tool access) to HTTP transport (REST API access). You'll learn when to use each transport, how to migrate safely with backward compatibility, and how to verify both transports work simultaneously.

**What you'll learn:**
- Understand stdio vs HTTP transport trade-offs
- Deploy HTTP server alongside stdio
- Verify backward compatibility
- Migrate integrations to HTTP
- Roll back if needed

**What you'll achieve:**
- HTTP server running alongside stdio tools
- Both transports working simultaneously
- Smooth migration with zero downtime
- Ability to roll back to stdio if needed

---

## Quick Start

```bash
# 1. Keep stdio working (no changes to existing setup)
mcp-orchestration-init  # Still works

# 2. Add HTTP server (runs in parallel)
mcp-orchestration-serve-http &

# 3. Generate token for HTTP
TOKEN=$(mcp-orchestration-generate-token | grep "Generated token:" | awk '{print $3}')

# 4. Verify stdio still works
mcp-orchestration-discover

# 5. Verify HTTP works too
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/clients

# Both transports now available!
```

---

## Understanding stdio vs HTTP Transport

### stdio Transport (Original)

**What it is:**
- Direct execution of MCP tools via CLI commands
- Tools run in same process as caller
- Input/output via stdin/stdout/stderr

**Advantages:**
- ✅ Simple setup (no server required)
- ✅ Fast (no network overhead)
- ✅ Secure (no network exposure)
- ✅ Works offline

**Disadvantages:**
- ❌ Local only (cannot access remotely)
- ❌ No automation from external tools (n8n, web apps)
- ❌ Cannot be used by mcp-gateway
- ❌ Requires Python environment on client

**Use cases:**
- Local development
- Personal use
- Offline environments
- Situations requiring maximum security

### HTTP Transport (New in v0.2.0)

**What it is:**
- FastAPI server exposing all MCP tools via REST API
- Tools run in server process
- Input/output via HTTP requests/responses

**Advantages:**
- ✅ Remote access (network accessible)
- ✅ Automation friendly (n8n, web apps, CI/CD)
- ✅ mcp-gateway compatible
- ✅ Language agnostic (any HTTP client)
- ✅ Multiple clients (concurrent access)

**Disadvantages:**
- ❌ Requires server deployment
- ❌ Slower (network overhead)
- ❌ Requires authentication setup
- ❌ Needs HTTPS for production security

**Use cases:**
- Remote access
- n8n automation workflows
- Web application integration
- mcp-gateway deployment
- Multi-user environments
- CI/CD pipelines

### Decision Framework

**Use stdio when:**
- Working locally on single machine
- Security is paramount (no network exposure)
- Maximum performance needed (no network latency)
- Offline environment

**Use HTTP when:**
- Need remote access
- Automating with n8n or web apps
- Integrating with mcp-gateway
- Multiple users/clients
- CI/CD pipelines

**Use both when:**
- Migrating from stdio to HTTP
- Want flexibility for different use cases
- Need backward compatibility

---

## Migration Strategy: Parallel Running

The safest migration strategy is **parallel running** - run both transports simultaneously:

1. **Keep stdio working** (no changes to existing setup)
2. **Add HTTP server** (deploy alongside stdio)
3. **Verify both work** (test both transports)
4. **Migrate integrations gradually** (one at a time)
5. **Monitor both** (ensure no issues)
6. **Eventually deprecate stdio** (if HTTP meets all needs)

**Key principle:** Never break existing stdio workflows while adding HTTP.

---

## Step-by-Step Migration

### Step 1: Verify Current stdio Setup

Before migrating, ensure your stdio setup is working:

```bash
# Check version (should be 0.2.0+)
python -c "import mcp_orchestrator; print(mcp_orchestrator.__version__)"

# Test basic stdio commands
mcp-orchestration-discover
mcp-orchestration-get-config claude-desktop default
```

**Expected output:**
```
0.2.0

Discovering MCP clients...
Found 2 clients:
  - claude-desktop
  - cursor

Getting configuration for claude-desktop/default...
{
  "mcpServers": {...}
}
```

✅ **stdio is working** - safe to proceed with HTTP migration.

### Step 2: Deploy HTTP Server

**Option A: Foreground (for testing)**
```bash
# Start server in current terminal
mcp-orchestration-serve-http
```

**Option B: Background (for production)**
```bash
# Start server in background
nohup mcp-orchestration-serve-http > /tmp/mcp-http.log 2>&1 &

# Save PID for later
echo $! > /tmp/mcp-http.pid

# Check it's running
ps aux | grep mcp-orchestration-serve-http
```

**Option C: systemd (for production servers)**
```bash
# Create service file
sudo tee /etc/systemd/system/mcp-orchestration.service > /dev/null <<EOF
[Unit]
Description=MCP Orchestration HTTP Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
Environment="MCP_ORCHESTRATION_API_KEY=your-static-key-here"
ExecStart=$(which mcp-orchestration-serve-http) --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable mcp-orchestration
sudo systemctl start mcp-orchestration
sudo systemctl status mcp-orchestration
```

**Expected output:**
```
Starting HTTP server on http://0.0.0.0:8000
API docs: http://0.0.0.0:8000/docs
OpenAPI schema: http://0.0.0.0:8000/openapi.json
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **HTTP server is running**.

### Step 3: Generate Authentication Token

**In a new terminal**, generate a bearer token:

```bash
TOKEN=$(mcp-orchestration-generate-token | grep "Generated token:" | awk '{print $3}')
echo "Token: $TOKEN"

# Save for later use
echo "export MCP_HTTP_TOKEN='$TOKEN'" >> ~/.bashrc
source ~/.bashrc
```

**Expected output:**
```
Token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v
```

✅ **Token generated and saved**.

### Step 4: Verify Backward Compatibility

**Test that stdio still works** (it should - HTTP doesn't affect stdio):

```bash
# stdio commands should work unchanged
mcp-orchestration-discover
mcp-orchestration-list-servers
mcp-orchestration-get-server filesystem
```

**Expected result:** All stdio commands work normally.

✅ **stdio backward compatibility confirmed**.

### Step 5: Test HTTP Transport

**Test equivalent HTTP endpoints:**

```bash
# List clients (equivalent to mcp-orchestration-discover)
curl -H "Authorization: Bearer $MCP_HTTP_TOKEN" \
  http://localhost:8000/v1/clients

# List servers (equivalent to mcp-orchestration-list-servers)
curl -H "Authorization: Bearer $MCP_HTTP_TOKEN" \
  http://localhost:8000/v1/servers

# Get server details (equivalent to mcp-orchestration-get-server filesystem)
curl -H "Authorization: Bearer $MCP_HTTP_TOKEN" \
  http://localhost:8000/v1/servers/filesystem
```

**Expected result:** HTTP endpoints return same data as stdio commands.

✅ **HTTP transport working correctly**.

### Step 6: Side-by-Side Comparison

**Verify that stdio and HTTP return identical results:**

```bash
# stdio version
STDIO_OUTPUT=$(mcp-orchestration-list-servers)

# HTTP version
HTTP_OUTPUT=$(curl -s -H "Authorization: Bearer $MCP_HTTP_TOKEN" \
  http://localhost:8000/v1/servers | jq -r '.servers[].server_id' | sort)

# Compare
echo "stdio servers:"
echo "$STDIO_OUTPUT" | jq -r '.[] | .server_id' | sort

echo -e "\nHTTP servers:"
echo "$HTTP_OUTPUT"
```

**Expected result:** Both lists should be identical.

✅ **stdio and HTTP are functionally equivalent**.

### Step 7: Migrate Integrations Gradually

Now migrate your integrations one at a time. Start with the least critical:

#### Example 1: Migrate n8n Workflow

**Before (stdio - not possible):**
n8n cannot call stdio commands directly.

**After (HTTP):**
```
HTTP Request Node:
  URL: http://mcp-server:8000/v1/clients
  Method: GET
  Authentication: Header Auth
    Header: Authorization
    Value: Bearer {{$env.MCP_HTTP_TOKEN}}
```

**Test in n8n:**
1. Create HTTP Request node
2. Configure URL and authentication
3. Execute
4. Verify response

✅ **n8n now has access to MCP tools**.

#### Example 2: Migrate Web Application

**Before (stdio - not possible):**
Web app cannot execute CLI commands.

**After (HTTP):**
```javascript
// Frontend
async function listClients() {
  const response = await fetch('/api/mcp/clients');
  return await response.json();
}

// Backend (Node.js/Express)
app.get('/api/mcp/clients', async (req, res) => {
  const token = process.env.MCP_HTTP_TOKEN;
  const response = await fetch('http://localhost:8000/v1/clients', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  res.json(await response.json());
});
```

✅ **Web app now has access to MCP tools**.

#### Example 3: Keep Local Development on stdio

**No changes needed:**
```bash
# Local development continues using stdio
mcp-orchestration-discover
mcp-orchestration-draft-add filesystem --path ~/Documents
mcp-orchestration-publish
mcp-orchestration-deploy
```

✅ **Local workflow unchanged**.

### Step 8: Monitor Both Transports

**Monitor stdio usage:**
```bash
# Check telemetry for stdio usage
cat var/telemetry/events.jsonl | grep "tool.execute" | jq -r .metadata.tool_name
```

**Monitor HTTP usage:**
```bash
# Check HTTP server logs
tail -f /tmp/mcp-http.log

# Or if using systemd
sudo journalctl -u mcp-orchestration -f
```

**Expected result:** See which transport is being used for what.

### Step 9: Gradual Deprecation (Optional)

Once all integrations migrated to HTTP, you can deprecate stdio:

**Option A: Keep both (recommended)**
- stdio for local development
- HTTP for remote/automation

**Option B: HTTP only**
- Update documentation to use HTTP
- Keep stdio available but unused
- Eventually remove stdio in future major version

---

## Complete Migration Examples

### Example 1: Migrate Developer Workflow

**Scenario:** Developer using stdio locally wants HTTP for remote access.

**Before:**
```bash
# All local stdio
mcp-orchestration-discover
mcp-orchestration-draft-add filesystem --path ~/code
mcp-orchestration-publish
mcp-orchestration-deploy
```

**After (hybrid):**
```bash
# Local: Keep using stdio (faster, simpler)
mcp-orchestration-draft-add filesystem --path ~/code
mcp-orchestration-publish
mcp-orchestration-deploy

# Remote: Use HTTP via curl or web UI
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"server_id": "filesystem", "params": {"path": "/home/user/code"}}' \
  http://mcp-server:8000/v1/config/claude-desktop/default/draft/add
```

**Result:** Flexibility - use stdio locally, HTTP remotely.

### Example 2: Migrate n8n Automation

**Scenario:** Want to automate MCP configuration via n8n.

**Before:**
Not possible - n8n cannot execute stdio commands.

**After:**

**n8n Workflow:**
```
1. HTTP Request: List available servers
   GET http://mcp-server:8000/v1/servers

2. Function: Select server based on criteria

3. HTTP Request: Add server to draft
   POST http://mcp-server:8000/v1/config/claude-desktop/default/draft/add

4. HTTP Request: Validate configuration
   POST http://mcp-server:8000/v1/config/claude-desktop/default/validate

5. HTTP Request: Publish configuration
   POST http://mcp-server:8000/v1/config/claude-desktop/default/publish

6. HTTP Request: Deploy configuration
   POST http://mcp-server:8000/v1/config/claude-desktop/default/deploy
```

**Result:** Fully automated configuration management.

### Example 3: Migrate CI/CD Pipeline

**Scenario:** Deploy configurations via GitHub Actions.

**Before:**
```yaml
# .github/workflows/deploy-mcp.yml
- name: Deploy MCP config
  run: |
    mcp-orchestration-draft-add filesystem --path /data
    mcp-orchestration-publish
    mcp-orchestration-deploy
```

**After:**
```yaml
# .github/workflows/deploy-mcp.yml
- name: Deploy MCP config
  env:
    MCP_TOKEN: ${{ secrets.MCP_HTTP_TOKEN }}
  run: |
    curl -X POST \
      -H "Authorization: Bearer $MCP_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"server_id": "filesystem", "params": {"path": "/data"}}' \
      http://mcp-server:8000/v1/config/claude-desktop/default/draft/add

    curl -X POST \
      -H "Authorization: Bearer $MCP_TOKEN" \
      http://mcp-server:8000/v1/config/claude-desktop/default/publish

    curl -X POST \
      -H "Authorization: Bearer $MCP_TOKEN" \
      http://mcp-server:8000/v1/config/claude-desktop/default/deploy
```

**Result:** CI/CD can deploy to remote MCP server.

---

## stdio to HTTP Mapping

Complete reference for migrating commands:

| stdio Command | HTTP Endpoint | Method |
|---------------|---------------|--------|
| `mcp-orchestration-discover` | `/v1/clients` | GET |
| `mcp-orchestration-list-profiles <client>` | `/v1/clients/{client_id}/profiles` | GET |
| `mcp-orchestration-get-config <client> <profile>` | `/v1/config/{client_id}/{profile}` | GET |
| `mcp-orchestration-list-servers` | `/v1/servers` | GET |
| `mcp-orchestration-get-server <server>` | `/v1/servers/{server_id}` | GET |
| `mcp-orchestration-draft-add <server> --params...` | `/v1/config/{client}/{profile}/draft/add` | POST |
| `mcp-orchestration-draft-remove <server>` | `/v1/config/{client}/{profile}/draft/remove` | POST |
| `mcp-orchestration-draft-view` | `/v1/config/{client}/{profile}/draft` | GET |
| `mcp-orchestration-draft-clear` | `/v1/config/{client}/{profile}/draft` | DELETE |
| `mcp-orchestration-validate` | `/v1/config/{client}/{profile}/validate` | POST |
| `mcp-orchestration-publish` | `/v1/config/{client}/{profile}/publish` | POST |
| `mcp-orchestration-deploy` | `/v1/config/{client}/{profile}/deploy` | POST |
| `mcp-orchestration-diff <config1> <config2>` | `/v1/config/diff` | POST |
| `mcp-orchestration-init` | `/v1/keys/initialize` | POST |

**See complete endpoint documentation:** http://localhost:8000/docs

---

## Rollback Procedures

If you need to roll back to stdio-only:

### Option 1: Stop HTTP Server (Keep Both Available)

```bash
# If running in background
kill $(cat /tmp/mcp-http.pid)

# If using systemd
sudo systemctl stop mcp-orchestration
sudo systemctl disable mcp-orchestration

# stdio continues working unchanged
mcp-orchestration-discover  # Still works
```

**Result:** HTTP disabled, stdio still working.

### Option 2: Revert Integration Changes

If an integration isn't working with HTTP:

**n8n:**
1. Disable HTTP Request nodes
2. Use alternative approach (webhook, manual)

**Web app:**
```javascript
// Temporarily disable HTTP calls
// return await mcpHttpClient.listClients();
return []; // Or fallback data
```

**CI/CD:**
```yaml
# Comment out HTTP deployment
# - name: Deploy via HTTP
#   run: curl ...

# Re-enable stdio deployment (if worker has Python)
- name: Deploy via stdio
  run: mcp-orchestration-deploy
```

### Option 3: Emergency Rollback

If HTTP server is causing issues:

```bash
# 1. Stop HTTP server immediately
sudo systemctl stop mcp-orchestration
# or
pkill -f mcp-orchestration-serve-http

# 2. Verify stdio still works
mcp-orchestration-discover

# 3. Investigate HTTP issues
tail -f /tmp/mcp-http.log
sudo journalctl -u mcp-orchestration

# 4. Fix issues before restarting HTTP
```

**Result:** Immediate return to stdio-only operation.

---

## Troubleshooting Migration

### Issue: Both stdio and HTTP Return Different Results

**Diagnosis:**
```bash
# Get stdio result
STDIO_RESULT=$(mcp-orchestration-list-servers)

# Get HTTP result
HTTP_RESULT=$(curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/servers)

# Compare
diff <(echo "$STDIO_RESULT" | jq -S .) <(echo "$HTTP_RESULT" | jq -S .servers)
```

**Possible causes:**
1. Different versions (stdio using v0.1.5, HTTP using v0.2.0)
2. Different configuration paths
3. Caching issues

**Solutions:**
```bash
# Verify versions match
python -c "import mcp_orchestrator; print(mcp_orchestrator.__version__)"

# Restart HTTP server to clear cache
sudo systemctl restart mcp-orchestration
```

### Issue: HTTP Server Won't Start

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or use different port
mcp-orchestration-serve-http --port 9000
```

### Issue: Authentication Failing After Migration

**Error:**
```
401 Unauthorized
```

**Diagnosis:**
```bash
# Test token validity
curl -v -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/clients \
  2>&1 | grep "HTTP/"
```

**Solutions:**
```bash
# 1. Regenerate token
NEW_TOKEN=$(mcp-orchestration-generate-token | grep "Generated" | awk '{print $3}')

# 2. Update environment variable
export MCP_HTTP_TOKEN="$NEW_TOKEN"

# 3. Update applications to use new token

# 4. Test again
curl -H "Authorization: Bearer $MCP_HTTP_TOKEN" \
  http://localhost:8000/v1/clients
```

### Issue: stdio Stopped Working After HTTP Deployment

**This should never happen** - HTTP and stdio are independent.

**Diagnosis:**
```bash
# Check if stdio commands exist
which mcp-orchestration-discover

# Check if Python package is intact
python -c "import mcp_orchestrator; print('OK')"

# Check if PATH is correct
echo $PATH
```

**Solution:**
```bash
# Reinstall if package is corrupted
pip install --force-reinstall mcp-orchestration

# Verify stdio works
mcp-orchestration-discover
```

---

## Performance Comparison

### Latency Benchmarks

**stdio (local execution):**
```bash
time mcp-orchestration-list-servers
# Real: 0.15s
# User: 0.10s
# Sys:  0.03s
```

**HTTP (network roundtrip):**
```bash
time curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/servers
# Real: 0.25s
# User: 0.01s
# Sys:  0.01s
```

**Result:** stdio is ~40% faster for local operations.

### Throughput Comparison

**stdio (sequential):**
- 1 command = 150ms
- 10 commands = 1.5s
- 100 commands = 15s

**HTTP (parallel):**
- 1 request = 250ms
- 10 parallel requests = 300ms
- 100 parallel requests = 500ms

**Result:** HTTP is faster for parallel operations.

### Resource Usage

**stdio:**
- Memory: 50MB per command (Python process)
- CPU: 10% during execution
- Network: None

**HTTP:**
- Memory: 100MB (server process, persistent)
- CPU: 5% average, 20% during requests
- Network: Minimal (local: ~1KB/request)

**Result:** HTTP uses more memory but less CPU over time.

---

## Security Considerations

### stdio Security Model

**Threat model:**
- ✅ No network exposure
- ✅ File system permissions enforce access control
- ✅ No authentication required (local only)
- ⚠️ Anyone with shell access can execute

**Best for:** Single-user local development.

### HTTP Security Model

**Threat model:**
- ⚠️ Network exposure (requires authentication)
- ✅ Bearer token authentication
- ✅ API key authentication
- ⚠️ Requires HTTPS in production
- ⚠️ Token management required

**Best for:** Multi-user, remote access, automation.

### Migration Security Checklist

During migration, ensure:

- [ ] HTTP server binds to 127.0.0.1 for localhost-only (or 0.0.0.0 with firewall)
- [ ] Strong bearer tokens generated (43 chars, cryptographically secure)
- [ ] Tokens stored securely (environment variables, not in code)
- [ ] HTTPS enabled for production (reverse proxy with Let's Encrypt)
- [ ] Firewall rules configured (only allow port 8000 from trusted IPs)
- [ ] Token rotation scheduled (monthly recommended)
- [ ] stdio access still controlled by file system permissions

---

## Migration Checklist

Use this checklist to track your migration:

### Pre-Migration
- [ ] Verify stdio is working (v0.2.0+)
- [ ] Document current stdio workflows
- [ ] Identify integrations that need HTTP
- [ ] Plan migration order (least critical first)

### Deployment
- [ ] Deploy HTTP server (foreground/background/systemd)
- [ ] Verify HTTP server is running
- [ ] Generate authentication token
- [ ] Store token securely

### Verification
- [ ] Test stdio still works (backward compatibility)
- [ ] Test HTTP endpoints return expected data
- [ ] Compare stdio and HTTP results (should be identical)
- [ ] Test HTTP from remote client (if remote access needed)

### Integration Migration
- [ ] Migrate first integration (e.g., n8n)
- [ ] Test migrated integration
- [ ] Monitor for issues
- [ ] Migrate second integration
- [ ] Repeat for all integrations

### Post-Migration
- [ ] Monitor both transports for 1 week
- [ ] Document which use cases use stdio vs HTTP
- [ ] Update internal documentation
- [ ] Train team on HTTP endpoints
- [ ] Schedule token rotation

### Optional Deprecation
- [ ] Decide if stdio should be deprecated
- [ ] Update documentation to recommend HTTP
- [ ] Plan eventual stdio removal (future major version)

---

## Next Steps

Now that you understand stdio to HTTP migration:

1. **Deploy HTTP server:** Follow [Deploy HTTP Server](deploy-http-server.md)
2. **Set up authentication:** Follow [Authenticate HTTP API](authenticate-http-api.md)
3. **Migrate first integration:** Start with least critical use case
4. **Monitor both transports:** Ensure no issues for 1 week
5. **Gradually migrate remaining integrations:** One at a time

**Related Guides:**
- [Deploy HTTP Server](deploy-http-server.md) - Server deployment
- [Authenticate HTTP API](authenticate-http-api.md) - Token management
- [Complete Workflow](complete-workflow.md) - Full orchestration workflow

---

## Summary

You've learned how to migrate from stdio to HTTP transport!

**What you accomplished:**
- ✅ Understood stdio vs HTTP trade-offs
- ✅ Deployed HTTP server alongside stdio
- ✅ Verified backward compatibility
- ✅ Migrated integrations to HTTP
- ✅ Learned rollback procedures

**Key takeaways:**
- **Parallel running is safest** - run both transports simultaneously
- **Migrate gradually** - one integration at a time
- **Keep stdio for local dev** - it's faster and simpler
- **Use HTTP for automation** - n8n, web apps, remote access
- **Monitor both transports** - ensure no issues
- **HTTPS is required for production** - use reverse proxy

**Migration strategy:**
1. Deploy HTTP alongside stdio (both work)
2. Verify backward compatibility (stdio unchanged)
3. Migrate integrations one by one (gradual)
4. Monitor for issues (1 week minimum)
5. Keep both or deprecate stdio (your choice)

---

**Guide Version:** 1.0
**Last Updated:** 2025-10-26
**mcp-orchestration Version:** 0.2.0+
**Difficulty:** Intermediate
**Estimated Time:** 15 minutes
