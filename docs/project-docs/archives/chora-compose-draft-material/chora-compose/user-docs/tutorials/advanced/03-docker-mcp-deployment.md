# Tutorial: Deploy chora-compose MCP Server with Docker for n8n Integration

**Target Audience**: Developers new to Docker MCP deployment
**Time**: 30 minutes
**Difficulty**: Intermediate

---

## What You'll Learn

By the end of this tutorial, you will:
- ✅ Deploy chora-compose MCP server in Docker
- ✅ Connect n8n to the MCP server via HTTP/SSE
- ✅ Call chora-compose tools from n8n workflows
- ✅ Understand the multi-container architecture
- ✅ Debug common deployment issues

## What You'll Build

A working multi-container environment with:
1. **chora-compose MCP server** exposing 17 tools via HTTP/SSE
2. **n8n workflow automation** accessing chora-compose tools
3. **Persistent storage** for configs and outputs
4. **Development workflow** using just commands

---

## Prerequisites

### Required

- **Docker Desktop** installed and running
  - macOS/Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
- **Git** for cloning repository
- **Anthropic API key** for code generation (optional but recommended)
  - Get one at: https://console.anthropic.com/

### Recommended

- **Basic Docker knowledge** (docker build, docker-compose up)
- **Familiarity with n8n** (helpful but not required)
- **Terminal/command line** experience

### Check Prerequisites

```bash
# Verify Docker is running
docker --version
# Should show: Docker version 24.x or higher

# Check Docker is running
docker ps
# Should show: CONTAINER ID   IMAGE   ... (even if empty)

# Verify you have the repository
cd /path/to/chora-compose
ls
# Should show: Dockerfile, docker-compose.yml, src/, configs/
```

---

## Step 1: Configure Environment (5 minutes)

### 1.1 Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 1.2 Add Your API Key

Open `.env` in your editor:

```bash
# macOS
open .env

# Linux
nano .env

# Or use your preferred editor
code .env
```

Find the line:
```bash
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY_HERE
```

Replace `YOUR_ANTHROPIC_API_KEY_HERE` with your actual API key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

**Why?** The `code_generation` generator requires an Anthropic API key to function. Without it, you'll still have 16 other tools available.

### 1.3 Verify Configuration

```bash
# Check that .env exists and has your key
cat .env | grep ANTHROPIC_API_KEY
# Should show: ANTHROPIC_API_KEY=sk-ant-api03-...
```

✅ **Checkpoint**: You now have a configured `.env` file

---

## Step 2: Build Docker Image (5 minutes)

### 2.1 Build the Image

Run the build command:

```bash
just docker-build
```

**What's happening?**
- Poetry installs Python dependencies
- Source code is packaged into a wheel
- Multi-stage build creates optimized image
- Final image is ~500MB

**Expected output**:
```
Building chora-compose MCP server Docker image
Step 1/XX : FROM python:3.12-slim AS builder
...
Successfully tagged chora-compose-mcp:latest
```

**Build time**: ~3 minutes (first time), ~30 seconds (with cache)

### 2.2 Verify Image Exists

```bash
docker images | grep chora-compose-mcp
```

**Expected**:
```
chora-compose-mcp   latest   abc123def456   2 minutes ago   500MB
```

✅ **Checkpoint**: Docker image built successfully

---

## Step 3: Start Containers (2 minutes)

### 3.1 Start the Stack

```bash
just docker-up
```

**What's happening?**
- Creates Docker network (`chora-network`)
- Starts chora-compose-mcp container (port 8000)
- Starts n8n container (port 5678)
- Waits for health checks to pass

**Expected output**:
```
Creating network "chora-network"
Creating chora-compose-mcp ... done
Creating n8n               ... done
```

### 3.2 Verify Containers Running

```bash
just docker-ps
```

**Expected**:
```
NAME                  STATUS          PORTS
chora-compose-mcp     Up (healthy)    0.0.0.0:8000->8000/tcp
n8n                   Up              0.0.0.0:5678->5678/tcp
```

**Health Status**: Wait until `chora-compose-mcp` shows "(healthy)" - this can take up to 10 seconds.

### 3.3 Check Server Logs

```bash
just docker-logs
```

**Look for these lines**:
```
Starting chora-compose MCP server...
Server: chora-compose v1.4.2
Transport: sse
Listening on: http://0.0.0.0:8000/sse
Tools: 17 (13 content + 4 config lifecycle)
✓ ANTHROPIC_API_KEY detected - code_generation available
------------------------------------------------------------
Server ready at http://0.0.0.0:8000/sse
Waiting for connections...
```

✅ **Checkpoint**: MCP server is running and healthy

---

## Step 4: Test HTTP Endpoint (2 minutes)

### 4.1 Test Basic Connectivity

```bash
curl http://localhost:8000/
```

**Expected**: HTTP 200 response (FastMCP home page)

### 4.2 Test SSE Endpoint

```bash
curl -N http://localhost:8000/sse
```

**Expected**: Connection opens (SSE stream). Press Ctrl+C to close.

**What if it fails?**
- **Connection refused**: Container not started yet, wait 10 seconds
- **404 Not Found**: Typo in URL (should be `/sse`)
- **Port in use**: Change `MCP_SERVER_PORT` in `.env` to 9000

✅ **Checkpoint**: HTTP/SSE endpoint is accessible

---

## Step 5: Configure n8n (10 minutes)

### 5.1 Access n8n UI

Open your browser and navigate to:
```
http://localhost:5678
```

**First time?** You'll see n8n setup wizard:
1. Create owner account (email + password)
2. Choose workspace name (e.g., "My Workspace")
3. Skip usage telemetry (optional)

### 5.2 Install MCP Client Node

1. Click **Settings** (gear icon, bottom left)
2. Navigate to **Community Nodes**
3. Search for: `n8n-nodes-mcp`
4. Click **Install**
5. Wait for installation (~30 seconds)
6. **Important**: Refresh browser tab after installation

**Version**: Install latest (currently 1.x.x)

### 5.3 Create Test Workflow

1. Click **Workflows** in sidebar
2. Click **+ Add Workflow**
3. Name it: "Test chora-compose MCP"

### 5.4 Add MCP Client Node

1. Click **+** button to add node
2. Search for: "MCP Client"
3. Select **MCP Client** node
4. Node appears on canvas

### 5.5 Configure MCP Connection

In the MCP Client node settings:

**Connection Type**: Select `HTTP Streamable`

**HTTP Endpoint**: Enter exactly:
```
http://chora-compose-mcp:8000/sse
```

**Important**: Use `chora-compose-mcp` (service name), NOT `localhost`. Docker containers communicate via service names.

**Headers**: Leave empty (no auth required for local dev)

### 5.6 Test Connection

1. Click **Test** button at bottom of node settings
2. Should see: "Connection successful"
3. Tools dropdown should populate with chora-compose tools

**Troubleshooting**:
- **Connection refused**: Check both containers on same network (`docker network inspect chora-network`)
- **Tools not loading**: Check MCP server logs (`just docker-logs`)
- **Wrong endpoint**: Verify exact spelling of `http://chora-compose-mcp:8000/sse`

✅ **Checkpoint**: n8n connected to MCP server

---

## Step 6: Call Your First MCP Tool (5 minutes)

### 6.1 Select Tool

In the MCP Client node:

**Tool**: Select `choracompose:list_generators` from dropdown

**Arguments**: Leave empty (this tool takes no parameters)

### 6.2 Execute Workflow

1. Click **Execute Node** button (play icon)
2. Wait 1-2 seconds
3. Node turns green (success!)

### 6.3 View Results

Click on the node to see output:

**Expected JSON**:
```json
{
  "generators": [
    {
      "id": "jinja2",
      "name": "Jinja2 Generator",
      "description": "Template-based content generation using Jinja2"
    },
    {
      "id": "code_generation",
      "name": "AI Code Generation",
      "description": "Generate code using Claude API"
    },
    {
      "id": "template_fill",
      "name": "Template Fill",
      "description": "Simple variable substitution"
    }
  ]
}
```

**Success!** You've called a chora-compose tool from n8n!

### 6.4 Try Another Tool

Let's call `choracompose:list_content_configs`:

1. Change **Tool** dropdown to: `choracompose:list_content_configs`
2. **Arguments**: Leave empty
3. Click **Execute Node**

**Expected**: List of available content configurations

✅ **Checkpoint**: Successfully calling MCP tools from n8n

---

## Step 7: Generate Content (Advanced, 5 minutes)

### 7.1 Add Second MCP Client Node

1. Click **+** button again
2. Add another **MCP Client** node
3. Connect first node to second (drag from dot)

### 7.2 Configure Content Generation

In the second MCP Client node:

**Tool**: Select `choracompose:generate_content`

**Arguments** (click "+ Add Parameter" for each):
```json
{
  "content_config_id": "hello-world-content",
  "context": {
    "name": "n8n"
  }
}
```

**How to enter this**:
1. Click "Add Parameter"
2. Key: `content_config_id`, Value: `hello-world-content`
3. Click "Add Parameter" again
4. Key: `context`, Value: `{"name": "n8n"}`

### 7.3 Execute Complete Workflow

1. Click **Execute Workflow** (top right, play icon)
2. Both nodes execute in sequence
3. View output of second node

**Expected output**:
```json
{
  "output": "Hello, n8n!",
  "generator_used": "jinja2",
  "duration_ms": 45
}
```

**Congratulations!** You've built a multi-step n8n workflow using chora-compose tools!

✅ **Checkpoint**: Multi-node workflow working

---

## Step 8: Edit Configs Without Rebuild (Bonus, 3 minutes)

### 8.1 View Current Config

```bash
cat configs/content/hello-world/hello-world-content.json
```

### 8.2 Edit Config on Host

Open the file in your editor:

```bash
# Change the template to add more content
code configs/content/hello-world/hello-world-content.json
```

Example edit (change template):
```json
{
  "metadata": {
    "title": "Hello World (Updated!)",
    ...
  },
  "generatorSpecific": {
    "jinja2": {
      "template": "configs/templates/hello-world.j2",
      "inputs": {
        "context": {
          "name": "{{name}}",
          "extra": "This config was updated without Docker rebuild!"
        }
      }
    }
  }
}
```

### 8.3 Test Immediately

In n8n:
1. Re-execute the workflow (no rebuild needed!)
2. Output reflects your changes instantly

**Why does this work?**
- Volume mount maps `./configs` to `/app/configs`
- MCP server loads configs dynamically
- No container restart required!

✅ **Checkpoint**: Hot-reload configs working

---

## Step 9: Clean Up (1 minute)

When you're done experimenting:

### 9.1 Stop Containers (Keep Data)

```bash
just docker-down
```

**Result**: Containers stopped, volumes preserved, data intact

### 9.2 Full Cleanup (Remove Everything)

```bash
just docker-clean
```

**Result**: Containers removed, volumes deleted, image kept

**Warning**: This deletes all generated content in `ephemeral/` directory!

---

## What You've Learned

✅ Deploy chora-compose MCP server in Docker
✅ Configure environment variables for deployment
✅ Connect n8n to MCP server via HTTP/SSE
✅ Call MCP tools from n8n workflows
✅ Create multi-step workflows
✅ Edit configs without rebuilding containers
✅ Debug common issues using logs and health checks

---

## Next Steps

### Explore More Tools

Try these MCP tools in n8n:

1. **`choracompose:list_artifact_configs`** - List available artifact configs
2. **`choracompose:assemble_artifact`** - Assemble multi-part documents
3. **`choracompose:draft_config`** - Create draft configurations
4. **`choracompose:cleanup_ephemeral`** - Clean up temporary storage

### Build Real Workflows

**Daily Report Workflow**:
1. Gather git commits (HTTP Request node)
2. Gather events (another HTTP Request)
3. Generate report (choracompose:generate_content)
4. Save to ephemeral storage
5. Post to Slack

**Documentation Pipeline**:
1. Fetch API schema (HTTP Request)
2. Generate API docs (choracompose:generate_content)
3. Assemble complete doc (choracompose:assemble_artifact)
4. Commit to git (SSH node)

### Production Deployment

See [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md) for:
- Secrets management (Vault, AWS Secrets Manager)
- Reverse proxy with TLS (nginx, Traefik)
- Monitoring and logging (Prometheus, ELK)
- Horizontal scaling (multiple replicas)

---

## Common Issues & Solutions

### Issue: Container won't start

**Symptoms**: `just docker-up` fails, container exits immediately

**Debug**:
```bash
just docker-logs
```

**Common causes**:
- **Port conflict**: Change `MCP_SERVER_PORT` in `.env`
- **Missing .env**: Run `cp .env.example .env`
- **Python import error**: Check logs for traceback

### Issue: n8n can't connect to MCP server

**Symptoms**: "Connection refused" or timeout

**Check**:
```bash
# Verify both containers on same network
docker network inspect chora-network
# Should list both containers

# Test from n8n container
docker exec n8n curl http://chora-compose-mcp:8000/
# Should return 200 OK
```

**Solution**: Ensure `docker-compose.yml` has both services on `chora-network`

### Issue: Tools not loading in n8n

**Symptoms**: Dropdown empty, "No tools found"

**Check MCP server logs**:
```bash
just docker-logs
```

**Look for**: Error messages, "Tools: 17" confirmation

**Solution**: Restart both containers:
```bash
just docker-restart
```

### Issue: "Permission denied" errors

**Symptoms**: Can't write to ephemeral or output directories

**Solution**:
```bash
# Fix permissions on host
chmod -R 755 ephemeral/ output/
chown -R 1000:1000 ephemeral/ output/
```

**Why?** Container runs as user ID 1000, needs write access

---

## Troubleshooting Commands

```bash
# View all container logs
just docker-logs-all

# Check container status
just docker-ps

# Open shell in MCP container
just docker-shell
# Inside: ls, env, python -c "import chora_compose"

# Test HTTP endpoint directly
curl -v http://localhost:8000/

# Rebuild from scratch (no cache)
just docker-clean
docker build --no-cache -t chora-compose-mcp:latest .
just docker-up
```

---

## Resources

**Related Documentation**:
- [How-To: Deploy MCP Server with Docker](../../how-to/deployment/deploy-mcp-server-docker.md) - Practical workflows
- [Explanation: Docker MCP Deployment Rationale](../../explanation/deployment/docker-mcp-rationale.md) - Design decisions
- [Reference: Docker MCP API](../../reference/deployment/docker-mcp-reference.md) - Complete specifications

**External Resources**:
- [FastMCP Docs](https://gofastmcp.com)
- [n8n MCP Client](https://www.npmjs.com/package/n8n-nodes-mcp)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Tutorial Version**: 1.0
**Last Updated**: 2025-10-21
**Feedback**: Open an issue if you encounter problems!
