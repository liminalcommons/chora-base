# How To: Authenticate with HTTP API

**Difficulty:** Beginner
**Time:** 5 minutes
**Prerequisites:** HTTP server running (see [Deploy HTTP Server](deploy-http-server.md))
**Related:** [Deploy HTTP Server](deploy-http-server.md), [Migrate stdio to HTTP](migrate-stdio-to-http.md)

---

## Overview

This guide shows you how to authenticate with the mcp-orchestration HTTP API using bearer tokens or API keys. Authentication is required for all endpoints to ensure secure access to your MCP configurations.

**What you'll learn:**
- Generate bearer tokens
- Use bearer tokens in requests
- Set up API key authentication
- Manage and rotate tokens
- Troubleshoot authentication issues

**Authentication Methods:**
1. **Bearer Token** (recommended) - Dynamic tokens with usage tracking
2. **API Key** (alternative) - Static key from environment variable

---

## Quick Start

```bash
# 1. Generate token
TOKEN=$(mcp-orchestration-generate-token | grep "Generated token:" | awk '{print $3}')

# 2. Use in curl
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/clients

# Or use API key
export MCP_ORCHESTRATION_API_KEY="my-secret-key"
curl -H "X-API-Key: $MCP_ORCHESTRATION_API_KEY" \
  http://localhost:8000/v1/clients
```

---

## Method 1: Bearer Token Authentication (Recommended)

### Step 1: Generate a Bearer Token

```bash
mcp-orchestration-generate-token
```

**Output:**
```
Generated token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v

Use in requests:
  Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v

Or set as environment variable:
  export MCP_ORCHESTRATION_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v
```

**Token characteristics:**
- 43 characters (base64-encoded 32 bytes)
- Cryptographically secure (uses `secrets.token_urlsafe`)
- Unique (collision probability negligible)
- Valid until server restart (in-memory storage in v0.2.0)

### Step 2: Store the Token Securely

**Option A: Environment variable (recommended)**
```bash
# In ~/.bashrc or ~/.zshrc
export MCP_ORCH_TOKEN="a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc

# Use in requests
curl -H "Authorization: Bearer $MCP_ORCH_TOKEN" \
  http://localhost:8000/v1/clients
```

**Option B: .env file**
```bash
# Create .env file
echo "MCP_ORCH_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v" > .env

# Load from .env
export $(cat .env | xargs)

# Use in requests
curl -H "Authorization: Bearer $MCP_ORCH_TOKEN" \
  http://localhost:8000/v1/clients
```

**Option C: Password manager**
- Store in 1Password, LastPass, Bitwarden, etc.
- Retrieve when needed via CLI:
  ```bash
  # Example with 1Password CLI
  TOKEN=$(op read "op://Private/MCP Orch Token/token")
  curl -H "Authorization: Bearer $TOKEN" \
    http://localhost:8000/v1/clients
  ```

### Step 3: Use Bearer Token in Requests

**With curl:**
```bash
curl -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v" \
  http://localhost:8000/v1/clients
```

**With httpie:**
```bash
http GET localhost:8000/v1/clients \
  Authorization:"Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v"
```

**With Python requests:**
```python
import requests

token = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get("http://localhost:8000/v1/clients", headers=headers)
print(response.json())
```

**With JavaScript fetch:**
```javascript
const token = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v";

fetch("http://localhost:8000/v1/clients", {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## Method 2: API Key Authentication

### Step 1: Set API Key Environment Variable

**Before starting the server**, set the API key:

```bash
export MCP_ORCHESTRATION_API_KEY="my-super-secret-api-key-12345"
mcp-orchestration-serve-http
```

**Or in systemd service:**
```ini
[Service]
Environment="MCP_ORCHESTRATION_API_KEY=my-super-secret-api-key-12345"
ExecStart=/usr/local/bin/mcp-orchestration-serve-http
```

### Step 2: Use API Key in Requests

**With curl:**
```bash
curl -H "X-API-Key: my-super-secret-api-key-12345" \
  http://localhost:8000/v1/clients
```

**With Python requests:**
```python
import requests

api_key = "my-super-secret-api-key-12345"
headers = {"X-API-Key": api_key}

response = requests.get("http://localhost:8000/v1/clients", headers=headers)
print(response.json())
```

**With n8n HTTP Request node:**
```
URL: http://localhost:8000/v1/clients
Method: GET
Headers:
  - Name: X-API-Key
  - Value: {{$env.MCP_ORCH_API_KEY}}
```

---

## Token Management

### Generate Multiple Tokens

You can generate multiple tokens for different applications:

```bash
# Token for n8n
TOKEN_N8N=$(mcp-orchestration-generate-token | grep "Generated" | awk '{print $3}')
echo "n8n token: $TOKEN_N8N"

# Token for web app
TOKEN_WEB=$(mcp-orchestration-generate-token | grep "Generated" | awk '{print $3}')
echo "web app token: $TOKEN_WEB"

# Token for CI/CD
TOKEN_CI=$(mcp-orchestration-generate-token | grep "Generated" | awk '{print $3}')
echo "CI/CD token: $TOKEN_CI"
```

**All tokens are valid simultaneously.**

### Token Lifecycle

**Current behavior (v0.2.0):**
- Tokens stored in-memory
- Tokens persist until server restart
- No expiration (infinite lifetime until restart)
- Usage tracked (last_used, usage_count)

**Future enhancements (v0.2.1+):**
- Redis persistence (tokens survive restarts)
- Token expiration (configurable TTL)
- Token revocation
- Rate limiting per token

### Rotate Tokens

**Best practice:** Rotate tokens monthly

```bash
# 1. Generate new token
NEW_TOKEN=$(mcp-orchestration-generate-token | grep "Generated" | awk '{print $3}')

# 2. Update applications to use new token
# (update .env files, environment variables, etc.)

# 3. Test with new token
curl -H "Authorization: Bearer $NEW_TOKEN" \
  http://localhost:8000/v1/clients

# 4. Old tokens will be invalidated on next server restart
```

---

## Authentication in Different Scenarios

### Scenario 1: Local Development

**Use bearer token with environment variable:**

```bash
# ~/.bashrc or ~/.zshrc
export MCP_ORCH_TOKEN="dev-token-$(uuidgen)"

# In your scripts
curl -H "Authorization: Bearer $MCP_ORCH_TOKEN" \
  http://localhost:8000/v1/clients
```

### Scenario 2: Production Server

**Use API key with secrets management:**

```bash
# Store in systemd service
[Service]
Environment="MCP_ORCHESTRATION_API_KEY=prod-key-from-vault"

# Or load from external secrets manager
ExecStartPre=/usr/local/bin/load-secrets.sh
ExecStart=/usr/local/bin/mcp-orchestration-serve-http
```

### Scenario 3: CI/CD Pipeline

**Use bearer token from GitHub Secrets:**

```yaml
# .github/workflows/deploy.yml
- name: Deploy config
  env:
    MCP_TOKEN: ${{ secrets.MCP_ORCHESTRATION_TOKEN }}
  run: |
    curl -H "Authorization: Bearer $MCP_TOKEN" \
      -X POST \
      -H "Content-Type: application/json" \
      -d @config.json \
      http://mcp-server:8000/v1/config/claude-desktop/default/publish
```

### Scenario 4: n8n Workflow

**Use API key from n8n credentials:**

```
HTTP Request Node:
  URL: {{$env.MCP_SERVER_URL}}/v1/clients
  Headers:
    X-API-Key: {{$credentials.MCP_API_Key}}
```

### Scenario 5: Web Application

**Use bearer token from backend:**

```javascript
// Frontend makes request to your backend
fetch("/api/mcp/clients")
  .then(response => response.json())
  .then(data => setClients(data));

// Backend proxies to mcp-orchestration
app.get("/api/mcp/clients", async (req, res) => {
  const token = process.env.MCP_ORCH_TOKEN;
  const response = await fetch("http://mcp-server:8000/v1/clients", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  res.json(await response.json());
});
```

---

## Troubleshooting

### Issue: 401 Unauthorized

**Error response:**
```json
{
  "detail": "Authentication required"
}
```

**Causes:**
1. Missing Authorization header
2. Invalid token
3. Typo in header name

**Solutions:**

```bash
# Check 1: Include Authorization header
curl -H "Authorization: Bearer <token>" http://localhost:8000/v1/clients

# Check 2: Verify token is correct
echo $MCP_ORCH_TOKEN

# Check 3: Check header syntax (case-sensitive)
# ✅ Correct: "Authorization: Bearer <token>"
# ❌ Wrong: "authorization: bearer <token>"
```

### Issue: Invalid Authentication Credentials

**Error response:**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Causes:**
1. Token doesn't exist in server (server restarted)
2. API key doesn't match environment variable
3. Malformed token

**Solutions:**

```bash
# Generate new token after server restart
mcp-orchestration-generate-token

# Verify API key matches
echo $MCP_ORCHESTRATION_API_KEY

# Check for whitespace in token
echo "$TOKEN" | xxd  # Look for extra characters
```

### Issue: Token Works in curl but Not in Browser

**Cause:** CORS or credentials issue

**Solution:**

```javascript
// Include credentials in fetch
fetch("http://localhost:8000/v1/clients", {
  headers: {
    "Authorization": `Bearer ${token}`
  },
  credentials: "include"  // Add this
})
```

### Issue: Token Not Persisting After Server Restart

**Expected behavior:** Tokens are in-memory (v0.2.0)

**Solutions:**

```bash
# Option 1: Use API key (persists via environment variable)
export MCP_ORCHESTRATION_API_KEY="static-key"

# Option 2: Wait for Wave 2.1 (Redis persistence)

# Option 3: Script to regenerate tokens on startup
echo "TOKEN=$(mcp-orchestration-generate-token | grep Generated | awk '{print $3}')" >> .env
```

---

## Security Best Practices

### ✅ DO:

1. **Use HTTPS in production**
   ```bash
   # Tokens visible in HTTP
   # Use reverse proxy with TLS
   ```

2. **Store tokens securely**
   ```bash
   # ✅ Environment variables
   # ✅ .env files (.gitignore'd)
   # ✅ Secrets managers (Vault, 1Password)
   ```

3. **Rotate tokens regularly**
   ```bash
   # Monthly rotation recommended
   ```

4. **Use different tokens per application**
   ```bash
   # n8n, web app, CI/CD each get their own token
   ```

5. **Monitor token usage**
   ```bash
   # Check logs for suspicious activity
   # Future: /v1/tokens endpoint for usage stats
   ```

### ❌ DON'T:

1. **Don't commit tokens to git**
   ```bash
   # Add .env to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Don't share tokens**
   ```bash
   # Each developer gets their own token
   ```

3. **Don't use tokens in URLs**
   ```bash
   # ❌ http://localhost:8000/v1/clients?token=abc123
   # ✅ Authorization: Bearer abc123 (header)
   ```

4. **Don't hardcode tokens in code**
   ```python
   # ❌ token = "hardcoded-token-123"
   # ✅ token = os.getenv("MCP_ORCH_TOKEN")
   ```

5. **Don't use HTTP in production**
   ```bash
   # Tokens are visible in plain text
   # Always use HTTPS
   ```

---

## Testing Authentication

### Test Valid Token

```bash
# Should return 200 OK
curl -v -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/v1/clients \
  2>&1 | grep "HTTP/"

# Expected: HTTP/1.1 200 OK
```

### Test Invalid Token

```bash
# Should return 401 Unauthorized
curl -v -H "Authorization: Bearer invalid_token" \
  http://localhost:8000/v1/clients \
  2>&1 | grep "HTTP/"

# Expected: HTTP/1.1 401 Unauthorized
```

### Test No Authentication

```bash
# Should return 401 Unauthorized
curl -v http://localhost:8000/v1/clients \
  2>&1 | grep "HTTP/"

# Expected: HTTP/1.1 401 Unauthorized
```

### Test API Key

```bash
# Should return 200 OK if API key is set
curl -v -H "X-API-Key: $MCP_ORCHESTRATION_API_KEY" \
  http://localhost:8000/v1/clients \
  2>&1 | grep "HTTP/"

# Expected: HTTP/1.1 200 OK
```

---

## Advanced Usage

### Programmatic Token Generation (Future)

**Via API endpoint (planned for Wave 2.1):**

```bash
# Generate token via API (requires admin token)
curl -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/v1/admin/tokens/generate
```

### Token Revocation (Future)

**Planned for Wave 2.1:**

```bash
# Revoke specific token
curl -X DELETE \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/v1/admin/tokens/$TOKEN_ID
```

### Token Expiration (Future)

**Planned for Wave 2.1:**

```bash
# Generate token with expiration
mcp-orchestration-generate-token --expires-in 30d

# Generate token with specific expiry
mcp-orchestration-generate-token --expires-at "2026-01-01"
```

---

## Next Steps

Now that you understand authentication:

1. **Secure your deployment:** Set up HTTPS reverse proxy
2. **Integrate applications:** n8n, web apps, CI/CD
3. **Monitor usage:** Track token usage in logs
4. **Plan rotation:** Set up monthly token rotation schedule

**Related Guides:**
- [Deploy HTTP Server](deploy-http-server.md) - Server setup
- [Migrate stdio to HTTP](migrate-stdio-to-http.md) - Migration guide
- [Complete Workflow](complete-workflow.md) - Full orchestration workflow

---

## Summary

You've learned how to authenticate with the mcp-orchestration HTTP API!

**What you accomplished:**
- ✅ Generated bearer tokens
- ✅ Used tokens in HTTP requests
- ✅ Set up API key authentication
- ✅ Stored tokens securely
- ✅ Learned security best practices

**Authentication methods:**
- **Bearer Token** - Dynamic, tracked, recommended
- **API Key** - Static, simple, good for server-to-server

**Key takeaways:**
- Always use HTTPS in production
- Store tokens in environment variables
- Rotate tokens regularly
- Use different tokens per application
- Never commit tokens to git

---

**Guide Version:** 1.0
**Last Updated:** 2025-10-26
**mcp-orchestration Version:** 0.2.0+
**Difficulty:** Beginner
**Estimated Time:** 5 minutes
