# How To: Deploy HTTP Server

**Difficulty:** Intermediate
**Time:** 10 minutes
**Prerequisites:** mcp-orchestration v0.2.0+, Python 3.12+
**Related:** [Authenticate HTTP API](authenticate-http-api.md), [Migrate stdio to HTTP](migrate-stdio-to-http.md)

---

## Overview

This guide shows you how to deploy the mcp-orchestration HTTP server, making all 10 MCP tools accessible via REST API. This enables remote access, n8n automation, mcp-gateway integration, and web application integration.

**What you'll learn:**
- Start the HTTP server
- Configure host and port
- Access the OpenAPI documentation
- Test endpoints with curl
- Stop the server gracefully

**What you'll achieve:**
- HTTP server running on your chosen port
- All 10 MCP tools accessible via HTTP
- API documentation available at /docs
- Ready for remote integration

---

## Quick Start

```bash
# 1. Start HTTP server
mcp-orchestration-serve-http

# 2. Generate API token (in another terminal)
mcp-orchestration-generate-token

# 3. Test endpoint with curl
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8000/v1/clients

# 4. View API docs
open http://localhost:8000/docs
```

---

## Step-by-Step Guide

### Step 1: Install mcp-orchestration v0.2.0+

Ensure you have the HTTP transport version installed:

```bash
# Check version
python -c "import mcp_orchestrator; print(mcp_orchestrator.__version__)"
# Should output: 0.2.0 or higher

# If not, upgrade
pip install --upgrade mcp-orchestration
```

**Expected output:**
```
0.2.0
```

### Step 2: Start the HTTP Server

Start the server with default settings (0.0.0.0:8000):

```bash
mcp-orchestration-serve-http
```

**Expected output:**
```
Starting HTTP server on http://0.0.0.0:8000
API docs: http://0.0.0.0:8000/docs
OpenAPI schema: http://0.0.0.0:8000/openapi.json
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**What's happening:**
- Server binds to all interfaces (0.0.0.0) on port 8000
- API documentation is auto-generated at /docs
- OpenAPI schema available at /openapi.json
- Server is ready to accept requests in < 5 seconds

### Step 3: Generate an API Token

**In a new terminal window**, generate a bearer token:

```bash
mcp-orchestration-generate-token
```

**Expected output:**
```
Generated token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v

Use in requests:
  Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v

Or set as environment variable:
  export MCP_ORCHESTRATION_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v
```

**Save this token!** You'll need it for all API requests.

### Step 4: Test the API

Test the /v1/clients endpoint:

```bash
curl -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v" \
  http://localhost:8000/v1/clients
```

**Expected output:**
```json
{
  "clients": [
    {
      "client_id": "claude-desktop",
      "display_name": "Claude Desktop",
      "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
      "platform": "macos"
    },
    {
      "client_id": "cursor",
      "display_name": "Cursor",
      "config_path": "~/.cursor/mcp_config.json",
      "platform": "all"
    }
  ]
}
```

✅ **Success!** Your HTTP server is working correctly.

### Step 5: Explore the API Documentation

Open Swagger UI in your browser:

```bash
# macOS
open http://localhost:8000/docs

# Linux
xdg-open http://localhost:8000/docs

# Windows
start http://localhost:8000/docs
```

**What you'll see:**
- Interactive API documentation
- All 14 endpoints listed
- "Try it out" buttons to test endpoints
- Request/response schemas
- Authentication configuration

**Try an endpoint:**
1. Click on "GET /v1/servers"
2. Click "Try it out"
3. Click "Authorize" and enter your bearer token
4. Click "Execute"
5. View the response

### Step 6: Test Additional Endpoints

**List available MCP servers:**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/v1/servers
```

**Get a specific server:**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/v1/servers/filesystem
```

**Get configuration for a client:**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/v1/config/claude-desktop/default
```

**Add server to draft configuration:**
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"server_id": "filesystem", "params": {"path": "/Users/you/Documents"}}' \
  http://localhost:8000/v1/config/claude-desktop/default/draft/add
```

### Step 7: Stop the Server Gracefully

**In the terminal running the server**, press **Ctrl+C**:

**Expected output:**
```
^C
INFO:     Shutting down gracefully...
INFO:     Waiting for connections to close. (CTRL+C to force quit)
INFO:     Application shutdown complete.
INFO:     Finished server process [12345]
INFO:     Server shut down gracefully
```

**What's happening:**
- Server receives SIGINT signal
- In-flight requests are allowed to complete
- Server shuts down within 5 seconds
- No data is lost

---

## Advanced Configuration

### Custom Host and Port

**Bind to specific interface:**
```bash
# Localhost only (more secure)
mcp-orchestration-serve-http --host 127.0.0.1 --port 8000

# All interfaces (accessible remotely)
mcp-orchestration-serve-http --host 0.0.0.0 --port 8000

# Custom port
mcp-orchestration-serve-http --port 9000
```

### Configure Logging

**Set log level:**
```bash
# Debug mode (verbose logging)
mcp-orchestration-serve-http --log-level debug

# Production mode (minimal logging)
mcp-orchestration-serve-http --log-level warning

# Available levels: debug, info, warning, error, critical
```

### Environment Variables

**Set API key via environment variable:**
```bash
export MCP_ORCHESTRATION_API_KEY="your-static-api-key-here"
mcp-orchestration-serve-http
```

Now clients can use `X-API-Key` header instead of bearer tokens:
```bash
curl -H "X-API-Key: your-static-api-key-here" \
  http://localhost:8000/v1/clients
```

### Run as Background Service

**Using nohup (Linux/macOS):**
```bash
nohup mcp-orchestration-serve-http > server.log 2>&1 &
```

**Using systemd (Linux):**
```bash
# Create service file: /etc/systemd/system/mcp-orchestration.service
[Unit]
Description=MCP Orchestration HTTP Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser
Environment="MCP_ORCHESTRATION_API_KEY=your-key-here"
ExecStart=/usr/local/bin/mcp-orchestration-serve-http --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable mcp-orchestration
sudo systemctl start mcp-orchestration
sudo systemctl status mcp-orchestration
```

### Reverse Proxy Setup (HTTPS)

**Using nginx:**
```nginx
# /etc/nginx/sites-available/mcp-orchestration
server {
    listen 443 ssl http2;
    server_name mcp.example.com;

    ssl_certificate /etc/letsencrypt/live/mcp.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mcp.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Using Caddy (simpler):**
```
# Caddyfile
mcp.example.com {
    reverse_proxy localhost:8000
}
```

Then run: `caddy run`

---

## Complete API Endpoint Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /v1/clients | List all supported MCP clients |
| GET | /v1/clients/{client_id}/profiles | List profiles for a client |
| GET | /v1/config/{client_id}/{profile} | Get configuration artifact |
| POST | /v1/config/diff | Compare two configurations |
| POST | /v1/config/{client_id}/{profile}/draft/add | Add server to draft |
| POST | /v1/config/{client_id}/{profile}/draft/remove | Remove server from draft |
| GET | /v1/config/{client_id}/{profile}/draft | View draft configuration |
| DELETE | /v1/config/{client_id}/{profile}/draft | Clear draft configuration |
| POST | /v1/config/{client_id}/{profile}/validate | Validate configuration |
| POST | /v1/config/{client_id}/{profile}/publish | Publish signed configuration |
| POST | /v1/config/{client_id}/{profile}/deploy | Deploy configuration to client |
| GET | /v1/servers | List available MCP servers |
| GET | /v1/servers/{server_id} | Get server details |
| POST | /v1/keys/initialize | Initialize signing keys |

**Auto-generated documentation:** http://localhost:8000/docs

---

## Troubleshooting

### Issue: Port Already in Use

**Error:**
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

**Solution:**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
mcp-orchestration-serve-http --port 9000
```

### Issue: Cannot Connect Remotely

**Problem:** Server only accessible from localhost

**Solution:**
```bash
# Make sure you're binding to 0.0.0.0, not 127.0.0.1
mcp-orchestration-serve-http --host 0.0.0.0

# Check firewall rules
sudo ufw allow 8000/tcp  # Linux
```

### Issue: 401 Unauthorized on All Requests

**Problem:** Missing or invalid authentication

**Solution:**
```bash
# Generate a new token
mcp-orchestration-generate-token

# Use the token in requests
curl -H "Authorization: Bearer <new-token>" \
  http://localhost:8000/v1/clients

# Or use API key
export MCP_ORCHESTRATION_API_KEY="my-key"
curl -H "X-API-Key: my-key" \
  http://localhost:8000/v1/clients
```

### Issue: CORS Errors in Browser

**Problem:** Browser blocks requests due to CORS

**Solution:**
CORS is enabled by default for all origins. If you still have issues:

1. Check browser console for specific error
2. Ensure you're including credentials:
   ```javascript
   fetch('http://localhost:8000/v1/clients', {
     headers: {
       'Authorization': 'Bearer your-token'
     },
     credentials: 'include'
   })
   ```

3. For stricter CORS, configure origins via environment variable (future feature)

### Issue: Slow Response Times

**Problem:** API responses are slow

**Diagnostics:**
```bash
# Test with time
time curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/v1/clients

# Check server logs for slow operations
# Look for warnings or errors
```

**Solutions:**
- Check disk I/O (artifact storage)
- Monitor server resources (CPU, memory)
- Consider caching (Wave 2.2 feature)
- Ensure you're not running in debug mode

---

## Security Best Practices

### ✅ DO:
- **Use HTTPS in production** (reverse proxy with Let's Encrypt)
- **Use strong, random tokens** (generated by `generate-token`)
- **Rotate tokens regularly** (regenerate monthly)
- **Bind to 127.0.0.1** if only local access needed
- **Use environment variables** for API keys (not command-line args)
- **Set up firewall rules** (only allow necessary ports)
- **Monitor access logs** (look for suspicious activity)

### ❌ DON'T:
- **Don't use HTTP in production** (tokens visible in transit)
- **Don't commit tokens to git** (use .env files with .gitignore)
- **Don't expose port 8000 directly to internet** (use reverse proxy)
- **Don't use weak/predictable tokens** (use `generate-token`)
- **Don't disable authentication** (no public API endpoints)
- **Don't run as root** (use unprivileged user)

---

## Performance Tuning

### Expected Performance
- **Server startup:** < 5 seconds
- **p95 latency:** < 300ms for GET requests
- **Throughput:** 100+ concurrent requests
- **Memory usage:** ~50-100 MB

### Optimization Tips

**1. Use production ASGI server:**
```bash
# Uvicorn with multiple workers (production)
uvicorn mcp_orchestrator.http.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

**2. Monitor performance:**
```bash
# Install monitoring tools
pip install prometheus-fastapi-instrumentator

# Metrics will be available at /metrics (future feature)
```

**3. Enable HTTP/2:**
```nginx
# In nginx config
listen 443 ssl http2;
```

---

## Next Steps

Now that your HTTP server is running:

1. **Secure it:** Set up HTTPS with reverse proxy
2. **Authenticate:** Learn about [token management](authenticate-http-api.md)
3. **Integrate:** Connect n8n, mcp-gateway, or web apps
4. **Monitor:** Track API usage and performance
5. **Automate:** Create systemd service for production

**Related Guides:**
- [Authenticate HTTP API](authenticate-http-api.md) - Token management
- [Migrate stdio to HTTP](migrate-stdio-to-http.md) - Migration guide
- [Complete Workflow](complete-workflow.md) - Full orchestration workflow

---

## Summary

You've successfully deployed the mcp-orchestration HTTP server!

**What you accomplished:**
- ✅ Started HTTP server on port 8000
- ✅ Generated API token for authentication
- ✅ Tested endpoints with curl
- ✅ Explored API documentation at /docs
- ✅ Learned advanced configuration options

**Your server provides:**
- 14 HTTP endpoints (all 10 MCP tools)
- Bearer token + API key authentication
- Auto-generated OpenAPI documentation
- CORS support for web clients
- Graceful shutdown on Ctrl+C

**Next:** Integrate with your automation workflows, web apps, or remote clients!

---

**Guide Version:** 1.0
**Last Updated:** 2025-10-26
**mcp-orchestration Version:** 0.2.0+
**Difficulty:** Intermediate
**Estimated Time:** 10 minutes
