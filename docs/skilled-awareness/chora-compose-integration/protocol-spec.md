# Protocol Specification: chora-compose Integration

**SAP ID**: SAP-017
**Version**: 2.0.0
**Status**: active
**Last Updated**: 2025-11-04

---

## 1. Overview

Integration guide for adopting chora-compose: 4 modalities (pip/MCP/CLI/Docker), role-based workflows, decision trees, time-to-first-success <30 minutes.

### Key Capabilities

This SAP provides complete integration specifications for chora-compose adoption:

- **Interactive modality selector**: [select-modality.py](./select-modality.py) - Guided questionnaire to choose the right integration approach
- **pip integration**: Library usage patterns for Python project integration
- **MCP server deployment**: AI agent access via Model Context Protocol
- **CLI usage**: Interactive command-line interface for testing and workflows
- **Docker deployment**: Container-based deployment for n8n workflows and team access
- **Decision trees**: Clear modality selection guidance
- **Role-based workflows**: Tailored paths for developers, AI agents, teams, DevOps
- **Quick wins (< 30 min)**: Fast time-to-first-success across all modalities
- **Troubleshooting**: Common errors and resolution workflows

**Quick Start**: Run `python select-modality.py` for an interactive modality selection experience (< 2 minutes).

---

## 2. Core Contracts

This section defines the four integration modalities for chora-compose adoption.

### Contract 1: pip Integration (Library)

**Description**: Python library integration for direct code usage in Python projects.

**Interface**:

```python
# Installation
pip install chora-compose

# Basic usage
from chora_compose import ConfigLoader, ContentGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("path/to/config.yaml")

# Generate content
generator = ContentGenerator()
result = generator.generate(config)

# Access generated content
print(result.content)
print(result.output_path)
```

**Requirements**:
- Python 3.12+ (async generators, structural pattern matching)
- pip or Poetry for dependency management
- Write access to output directory
- Git (optional, for `git_reference` context sources)

**Use Cases**:
- Python project integration (documentation, configs, test data generation)
- Programmatic content generation in build scripts
- CI/CD integration for automated content updates
- Library usage in larger automation frameworks

**When to Use**: Choose pip modality when you need to integrate chora-compose as a library in Python code, trigger generation programmatically, or integrate in build/CI workflows.

---

### Contract 2: MCP Server Integration (AI Agents)

**Description**: Model Context Protocol server deployment for AI agent access (Claude Desktop, Cursor, etc.).

**Interface**:

```json
// Claude Desktop config: ~/.config/claude/config.json (macOS/Linux)
// or %APPDATA%\Claude\config.json (Windows)
{
  "mcpServers": {
    "chora-compose": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "${workspaceFolder}:/workspace",
        "ghcr.io/liminalcommons/chora-compose-mcp:latest"
      ]
    }
  }
}
```

**Tools Available** (22 MCP tools):

**Config Creation Tools** (6):
- `create_content_config`: Create content configuration
- `create_artifact_config`: Create artifact configuration
- `create_collection_config`: Create collection configuration
- `save_draft_config`: Save draft configuration to ephemeral storage
- `load_draft_config`: Load draft configuration from ephemeral storage
- `delete_draft_config`: Delete draft configuration

**Generation Tools** (3):
- `generate_content`: Generate single content piece from config
- `assemble_artifact`: Assemble artifact from multiple content pieces
- `assemble_collection`: Assemble collection (bulk generation)

**Utility Tools** (remaining 13):
- `list_capabilities`: List available generators
- `get_generator_info`: Get generator details
- `test_generator`: Test generator with sample data
- `validate_config`: Validate configuration syntax
- `store_ephemeral_output`: Store temporary output (30-day retention)
- `retrieve_ephemeral_output`: Retrieve temporary output
- `list_ephemeral_outputs`: List all ephemeral outputs
- `delete_ephemeral_output`: Delete ephemeral output
- `list_collections`: List available collections
- `get_collection_status`: Get collection generation status
- `invalidate_cache`: Force cache invalidation
- `resolve_context`: Resolve context from sources
- `check_freshness`: Check if cached content is fresh

**Requirements**:
- Docker Desktop installed and running
- Claude Desktop or compatible MCP client (Cursor, etc.)
- MCP server configuration (config.json)
- Volume mount permissions (workspace access)

**Use Cases**:
- Conversational content creation with AI agents
- Interactive config development and testing
- Exploratory content generation workflows
- AI-assisted configuration refinement

**When to Use**: Choose MCP server modality when you want AI agent access (Claude Desktop, Cursor), conversational content generation, or interactive development with AI assistance.

---

### Contract 3: CLI Integration (Interactive)

**Description**: Command-line interface for interactive usage, testing, and manual workflows.

**Interface**:

```bash
# Installation
pip install "chora-compose[cli]"

# Create content config (interactive prompts)
chora-compose create content --output my-content-config.yaml

# Generate content from config
chora-compose generate content --config my-content-config.yaml

# Create artifact config
chora-compose create artifact --output my-artifact-config.yaml

# Assemble artifact
chora-compose generate artifact --config my-artifact-config.yaml

# List available generators
chora-compose list capabilities

# Validate config
chora-compose validate --config my-config.yaml

# Check version
chora-compose --version
```

**Requirements**:
- Python 3.12+
- CLI extras installed: `pip install "chora-compose[cli]"`
- Terminal access (bash, zsh, PowerShell)
- Write access to output directory

**Use Cases**:
- Testing config changes before committing
- Manual content generation workflows
- Quick prototyping of new configs
- Learning chora-compose interactively

**When to Use**: Choose CLI modality when you want interactive testing, manual workflows, quick prototyping, or are learning chora-compose functionality.

---

### Contract 4: Docker Integration (Team Deployment)

**Description**: Docker deployment for n8n workflows, team access, and containerized environments.

**Interface**:

```yaml
# docker-compose.yml
version: "3.8"

services:
  chora-compose-mcp:
    image: ghcr.io/liminalcommons/chora-compose-mcp:latest
    volumes:
      - ./workspace:/workspace
      - ./configs:/configs
    environment:
      - CHORA_COMPOSE_LOG_LEVEL=INFO
      - CHORA_COMPOSE_CACHE_DIR=/workspace/.chora-compose
    ports:
      - "8080:8080"  # Optional: HTTP API (v1.6.0+)
    restart: unless-stopped
```

**Deployment**:

```bash
# Start service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f chora-compose-mcp

# Stop service
docker-compose down
```

**Requirements**:
- Docker and Docker Compose installed
- Volume mount permissions for workspace and configs
- Network access (if HTTP API enabled)
- n8n instance (for workflow integration)

**Use Cases**:
- Team-shared chora-compose deployment
- n8n workflow automation integration
- Centralized content generation service
- Multi-user environments with shared configs

**When to Use**: Choose Docker modality when you want team deployment, n8n workflow integration, centralized service, or need to provide chora-compose to multiple users.

---

## 3. Integration Patterns

Common patterns for integrating chora-compose in different scenarios.

### Pattern 1: Developer Workflow (pip)

**Scenario**: Python developer integrating chora-compose in project.

**Steps**:

1. **Install**:
   ```bash
   pip install chora-compose
   ```

2. **Create config directory**:
   ```bash
   mkdir configs/
   ```

3. **Create content config** (`configs/api-docs.yaml`):
   ```yaml
   version: "3.1"
   content_id: api-docs
   generator_type: jinja2
   output_path: docs/api-reference.md

   template: |
     # API Reference

     {% for endpoint in endpoints %}
     ## {{ endpoint.method }} {{ endpoint.path }}

     {{ endpoint.description }}

     {% endfor %}

   context:
     external_file:
       path: specs/openapi.yaml
       format: yaml
   ```

4. **Generate in Python** (`scripts/generate_docs.py`):
   ```python
   from chora_compose import ConfigLoader, ContentGenerator

   loader = ConfigLoader()
   config = loader.load_content_config("configs/api-docs.yaml")

   generator = ContentGenerator()
   result = generator.generate(config)

   print(f"✓ Generated: {result.output_path}")
   ```

**Result**: Generated content in `docs/api-reference.md`.

---

### Pattern 2: AI Agent Workflow (MCP)

**Scenario**: Claude Desktop user generating content conversationally.

**Steps**:

1. **Install Docker Desktop**: Download from https://www.docker.com/products/docker-desktop/

2. **Configure Claude Desktop**:
   - Edit: `~/.config/claude/config.json` (macOS/Linux) or `%APPDATA%\Claude\config.json` (Windows)
   - Add MCP server configuration (see Contract 2 above)

3. **Restart Claude Desktop**

4. **Conversational creation**:
   ```
   User: "Create a content config for API documentation using the OpenAPI generator"

   Claude: [Uses create_content_config tool]

   User: "Generate the content"

   Claude: [Uses generate_content tool]

   User: "Save to docs/api-reference.md"

   Claude: [Writes output to file]
   ```

**Result**: Generated content via conversational workflow.

---

### Pattern 3: Team Workflow (Docker)

**Scenario**: Team sharing chora-compose via Docker deployment.

**Steps**:

1. **DevOps**: Deploy chora-compose MCP server via Docker Compose (see Contract 4)

2. **Developers**: Configure MCP clients (Claude Desktop, Cursor) to point to team deployment

3. **Team**: Create shared configs in Git repository (`configs/`)

4. **Developers**: Generate content via MCP tools

5. **Automated**: n8n workflows trigger generation on events (PR created, issue labeled, etc.)

**Result**: Team collaboration with shared configs and centralized deployment.

---

## 4. Workflows

Two critical workflows for chora-compose adoption.

### Workflow 1: First Success (< 30 minutes)

**Purpose**: Get from zero to first generated content in under 30 minutes.

**Steps**:

**Step 1: Choose Modality** (5 minutes)

**Interactive Selector** (Recommended):
```bash
python select-modality.py  # Interactive questionnaire
python select-modality.py --quick --export md  # Quick mode + export guide
```

The [select-modality.py](./select-modality.py) tool asks 4 questions and recommends the best modality for your use case with setup instructions.

**Manual Decision Tree**:
- Developer integrating in Python? → **pip**
- AI agent user (Claude Desktop)? → **MCP server**
- Testing/exploring? → **CLI**
- Team deployment? → **Docker**

**Step 2: Install** (5-10 minutes)

For **pip**:
```bash
pip install chora-compose
```

For **MCP**:
```bash
# Install Docker Desktop (if not installed)
# Configure Claude Desktop config.json (see Contract 2)
# Restart Claude Desktop
```

For **CLI**:
```bash
pip install "chora-compose[cli]"
```

For **Docker**:
```bash
# Create docker-compose.yml (see Contract 4)
docker-compose up -d
```

**Step 3: Create First Config** (5-10 minutes)

For **pip/CLI**:
```yaml
# configs/hello-world.yaml
version: "3.1"
content_id: hello-world
generator_type: jinja2
output_path: output/hello-world.md

template: |
  # Hello World

  This is my first generated content using chora-compose!

  Generated at: {{ generation_timestamp }}

context:
  inline_data:
    generation_timestamp: "2025-11-04T12:00:00"
```

For **MCP**:
```
User: "Create a content config for a simple hello world markdown file"
Claude: [Uses create_content_config tool]
User: "Save it to configs/hello-world.yaml"
Claude: [Saves config]
```

**Step 4: Generate** (1-2 minutes)

For **pip**:
```python
from chora_compose import ConfigLoader, ContentGenerator

loader = ConfigLoader()
config = loader.load_content_config("configs/hello-world.yaml")

generator = ContentGenerator()
result = generator.generate(config)

with open(result.output_path, "w") as f:
    f.write(result.content)

print(f"✓ Generated: {result.output_path}")
```

For **MCP**:
```
User: "Generate the hello-world content"
Claude: [Uses generate_content tool]
```

For **CLI**:
```bash
chora-compose generate content --config configs/hello-world.yaml
```

**Step 5: Validate** (1-2 minutes)

```bash
# Check output exists
ls output/hello-world.md

# View content
cat output/hello-world.md
```

**Expected Output**:
```markdown
# Hello World

This is my first generated content using chora-compose!

Generated at: 2025-11-04T12:00:00
```

**Success Criteria**:
- Output file exists at expected path
- Content is correctly generated
- No errors in logs/console
- Total time: < 30 minutes

---

### Workflow 2: Production Integration (1-2 days)

**Purpose**: Integrate chora-compose in real project for production content generation.

**Day 1 Morning: Setup** (2-3 hours)

1. **Install chosen modality** (see Workflow 1, Step 2)

2. **Set up config directory structure**:
   ```bash
   mkdir -p configs/{content,artifacts,collections}
   mkdir -p templates
   mkdir -p output
   ```

3. **Create first production config** (e.g., API documentation):
   ```yaml
   # configs/content/api-docs-users.yaml
   version: "3.1"
   content_id: api-docs-users
   generator_type: jinja2
   output_path: docs/api-reference/users.md

   template_path: templates/api-docs.md.j2

   context:
     external_file:
       path: specs/openapi.yaml
       format: yaml
   ```

4. **Test generation workflow**:
   ```bash
   # Test with pip/CLI
   chora-compose generate content --config configs/content/api-docs-users.yaml

   # Verify output
   cat docs/api-reference/users.md
   ```

**Day 1 Afternoon: Integration** (3-4 hours)

1. **Integrate in build process** (if pip):
   ```python
   # scripts/generate_docs.py
   from chora_compose import ConfigLoader, ContentGenerator

   def generate_documentation():
       """Generate all API documentation."""
       loader = ConfigLoader()
       generator = ContentGenerator()

       configs = [
           "configs/content/api-docs-users.yaml",
           "configs/content/api-docs-auth.yaml",
           "configs/content/api-docs-posts.yaml",
       ]

       for config_path in configs:
           config = loader.load_content_config(config_path)
           result = generator.generate(config)
           print(f"✓ Generated: {result.output_path}")

   if __name__ == "__main__":
       generate_documentation()
   ```

2. **Configure team access** (if Docker):
   - Deploy Docker Compose service
   - Share MCP configuration with team
   - Document connection instructions

3. **Create templates/configs for common use cases**:
   - API documentation templates
   - Configuration file templates
   - Test data generation configs

4. **Document workflow for team** (`configs/README.md`):
   ```markdown
   # Content Generation Configs

   ## Quick Start
   1. Install: `pip install chora-compose`
   2. Run: `python scripts/generate_docs.py`
   3. Check: `ls output/`

   ## Configs
   - `content/api-docs-*.yaml`: API documentation
   - `artifacts/api-docs.yaml`: Combined artifact
   ```

**Day 2 Morning: Validation** (2-3 hours)

1. **Generate production content**:
   ```bash
   python scripts/generate_docs.py
   ```

2. **Review quality and accuracy**:
   - Check generated content matches specs
   - Validate formatting and structure
   - Ensure all required sections present

3. **Refine configs based on feedback**:
   - Adjust templates for better output
   - Add missing context sources
   - Fix any generation issues

4. **Measure productivity improvement**:
   - Time to generate manually vs. automated
   - Calculate ROI (target: ≥2x productivity)

**Day 2 Afternoon: Optimization** (2-3 hours)

1. **Add error handling**:
   ```python
   try:
       result = generator.generate(config)
   except GenerationError as e:
       logger.error(f"Generation failed: {e}")
       # Handle error appropriately
   ```

2. **Set up monitoring/logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   ```

3. **Create runbook for common issues** (see Section 13: Troubleshooting)

4. **Train team on usage**:
   - Walk through config creation
   - Demonstrate generation workflows
   - Answer questions and iterate

**Expected Output**: chora-compose generating production content in real workflows, team trained, configs in version control, ROI ≥2x.

---

### Workflow 3: n8n Automation Integration (Docker Modality)

**Purpose**: Integrate chora-compose with n8n workflow automation platform for scheduled generation, event-driven assembly, and batch documentation workflows.

**Prerequisites**:
- Docker Desktop installed and running
- n8n installed (v1.0.0+): `npm install -g n8n` or Docker: `docker run -p 5678:5678 n8nio/n8n`
- chora-compose Docker image: `docker pull ghcr.io/liminalcommons/chora-compose:latest`
- chora-compose configs in version control

**Duration**: 2-4 hours (setup + 3 example workflows)

**Steps**:

**Step 1: n8n Setup** (30 minutes)

1. **Install n8n**:
   ```bash
   # Option 1: npm
   npm install -g n8n
   n8n start

   # Option 2: Docker
   docker run -p 5678:5678 \
     -v /var/run/docker.sock:/var/run/docker.sock \
     n8nio/n8n
   ```

2. **Access n8n UI**: Open http://localhost:5678

3. **Configure credentials** (for integrations):
   - Slack: Create bot token at https://api.slack.com/apps (scope: `chat:write`)
   - GitHub: Create personal access token with `repo` scope
   - Cloud Storage: Configure OAuth for Google Drive, S3, etc.

**Step 2: Import Example Workflows** (15 minutes)

Three production-ready workflow examples are provided in [n8n-examples/](./n8n-examples/):

1. **[Scheduled Content Generation](./n8n-examples/workflow-1-scheduled-generation.json)**:
   - Trigger: Every 6 hours (configurable schedule)
   - Action: Generate content using chora-compose
   - Notifications: Slack on success/failure
   - Use case: Daily metrics, weekly reports, recurring documentation

2. **[Webhook-Triggered Artifact Assembly](./n8n-examples/workflow-2-webhook-assembly.json)**:
   - Trigger: POST webhook (from GitHub PR, CI/CD, manual)
   - Action: Assemble multi-piece artifact with optional PR context
   - Upload: Cloud storage (Google Drive, S3)
   - Response: JSON with artifact URL and status
   - Use case: PR documentation, on-demand artifact generation

3. **[Batch Documentation Generation](./n8n-examples/workflow-3-batch-docs.json)**:
   - Trigger: Manual or webhook
   - Action: Generate collection (18+ items) in parallel
   - Reporting: GitHub summary issue, Slack notification
   - Metrics: Success rate, cache hit rate, execution time
   - Use case: Full documentation regeneration, nightly builds

**Import Instructions**:
1. In n8n UI: Workflows → Import from File
2. Select workflow JSON file (e.g., `workflow-1-scheduled-generation.json`)
3. Configure credentials (Slack, GitHub, etc.)
4. Activate workflow

**Step 3: Configure First Workflow** (30 minutes)

**Example: Scheduled Content Generation**

1. **Import workflow**: `workflow-1-scheduled-generation.json`

2. **Update config path**:
   - Click "Execute chora-compose Generation" node
   - Update `--config` argument to your config file
   - Example: `--config /workspace/configs/content/daily-metrics.yaml`

3. **Configure schedule**:
   - Click "Schedule Trigger" node
   - Set interval: hours (6), days (1), or cron expression
   - Save workflow

4. **Configure Slack notifications** (optional):
   - Add Slack credential: Credentials → Header Auth
   - Header: `Authorization`, Value: `Bearer xoxb-your-token`
   - Assign to "Notify Slack" nodes

5. **Test workflow**:
   - Click "Execute Workflow"
   - Verify output file generated
   - Check Slack notification received

**Step 4: Webhook Integration** (30 minutes)

**Example: Webhook-Triggered Artifact Assembly**

1. **Import workflow**: `workflow-2-webhook-assembly.json`

2. **Note webhook URL**:
   - Click "Webhook Trigger" node
   - Copy URL: `http://n8n.yourcompany.com/webhook/chora-compose/assemble-docs`

3. **Test webhook**:
   ```bash
   curl -X POST http://localhost:5678/webhook/chora-compose/assemble-docs \
     -H "Content-Type: application/json" \
     -d '{
       "artifact_id": "api-docs",
       "config_path": "configs/artifacts/api-docs.yaml",
       "trigger_source": "manual"
     }'
   ```

4. **GitHub PR integration** (optional):
   - Create GitHub webhook: Repository → Settings → Webhooks
   - Payload URL: `http://n8n.yourcompany.com/webhook/chora-compose/assemble-docs`
   - Content type: `application/json`
   - Events: Pull request (opened, synchronize)

**Step 5: Batch Generation** (30 minutes)

**Example: Batch Documentation Generation**

1. **Import workflow**: `workflow-3-batch-docs.json`

2. **Create collection config**: `configs/collections/all-docs.yaml`
   ```yaml
   version: "1.0"
   collection_id: all-docs
   execution_strategy: parallel
   max_workers: 4

   artifacts:
     - config_path: configs/artifacts/api-docs.yaml
     - config_path: configs/artifacts/user-guide.yaml
     - config_path: configs/artifacts/architecture-docs.yaml
   ```

3. **Configure GitHub integration** (optional):
   - Add GitHub credential with `repo` scope
   - Update repository owner/name in "Create GitHub Summary Issue" node

4. **Execute batch generation**:
   ```bash
   curl -X POST http://localhost:5678/webhook/chora-compose/generate-all-docs \
     -H "Content-Type: application/json" \
     -d '{
       "collection_config": "configs/collections/all-docs.yaml",
       "parallel_workers": 4,
       "invalidate_cache": false
     }'
   ```

**Step 6: Production Deployment** (30 minutes)

1. **Deploy n8n to production**:
   ```yaml
   # docker-compose.yml
   version: "3.8"
   services:
     n8n:
       image: n8nio/n8n
       ports:
         - "5678:5678"
       volumes:
         - n8n_data:/home/node/.n8n
         - /var/run/docker.sock:/var/run/docker.sock
       environment:
         - N8N_BASIC_AUTH_ACTIVE=true
         - N8N_BASIC_AUTH_USER=${N8N_USER}
         - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
         - N8N_HOST=${N8N_HOST}
         - N8N_PROTOCOL=https
         - WEBHOOK_URL=https://${N8N_HOST}
       restart: unless-stopped

   volumes:
     n8n_data:
   ```

2. **Configure reverse proxy** (Nginx/Traefik):
   - Enable HTTPS/TLS for webhook endpoints
   - Configure authentication for n8n UI
   - Set up rate limiting for webhook endpoints

3. **Monitor workflows**:
   - Check n8n execution logs regularly
   - Set up alerts for failed executions
   - Monitor Docker resource usage: `docker stats`

**Expected Output**:
- n8n running with 3 production workflows
- Scheduled generation working (daily/weekly/hourly)
- Webhook endpoints integrated with GitHub/CI/CD
- Batch generation creating documentation collections
- Team notifications via Slack/email on success/failure

**Integration Patterns**:

| Pattern | Workflow | Trigger | Output |
|---------|----------|---------|--------|
| **Scheduled Generation** | Workflow 1 | Cron/interval | Single content piece + Slack notification |
| **Event-Driven Assembly** | Workflow 2 | GitHub PR webhook | Multi-piece artifact + cloud upload |
| **Bulk Regeneration** | Workflow 3 | Manual/nightly | Collection (18+ items) + GitHub summary |

**Performance Benchmarks** (M1 Mac, 16GB RAM, Docker Desktop):

| Workflow | Execution Time | Cache Hit Rate | Notes |
|----------|----------------|----------------|-------|
| Workflow 1 (single content) | 2-5 seconds | 95% (cached) | Daily metrics generation |
| Workflow 2 (5-piece artifact) | 8-12 seconds | 90% (cached) | PR documentation assembly |
| Workflow 3 (18 artifacts) | 45-60 seconds | 94% (cached) | Full SAP documentation (parallel) |

**Troubleshooting**:

**Issue**: "Docker not found" error in n8n workflow

**Solution**:
1. Ensure Docker Desktop is running
2. Mount Docker socket in n8n container: `-v /var/run/docker.sock:/var/run/docker.sock`
3. Verify n8n can execute Docker commands

**Issue**: Webhook not triggering workflow

**Solution**:
1. Ensure workflow is activated in n8n UI
2. Check webhook URL matches exactly (case-sensitive)
3. Verify webhook authentication configured correctly

**Issue**: Batch generation timeout

**Solution**:
1. Increase timeout in "Execute Collection Generation" node (default: 600000ms = 10 minutes)
2. Reduce `parallel_workers` to lower resource usage
3. Split large collections into smaller batches

**Additional Resources**:
- [n8n Examples README](./n8n-examples/README.md) - Detailed setup guide, customization examples
- [n8n Documentation](https://docs.n8n.io/) - Official n8n docs
- [Workflow JSON Files](./n8n-examples/) - 3 production-ready workflow examples

---

## 5. File Structure

Expected directory structure for chora-compose projects.

**Directory Layout**:
```
project-root/
├── configs/
│   ├── content/              # Content configs
│   │   ├── api-docs-users.yaml
│   │   ├── api-docs-auth.yaml
│   │   └── test-data.yaml
│   ├── artifacts/            # Artifact configs
│   │   └── api-docs.yaml
│   ├── collections/          # Collection configs
│   │   └── all-docs.yaml
│   └── README.md             # Config documentation
├── templates/                # Jinja2 templates
│   └── api-docs.md.j2
├── output/                   # Generated content (excluded from git)
│   └── docs/
├── .chora-compose/           # Ephemeral storage (excluded from git)
│   └── cache/
├── scripts/
│   └── generate_docs.py      # Generation scripts
└── .gitignore                # Exclude output/, .chora-compose/
```

**File Descriptions**:

**configs/content/*.yaml**:
- **Purpose**: Content configuration files
- **Format**: YAML (version 3.1)
- **Required**: At least one content config
- **Example**: See Workflow 1, Step 3

**configs/artifacts/*.yaml**:
- **Purpose**: Artifact assembly configuration
- **Format**: YAML (version 3.1)
- **Required**: No (only if using artifacts)

**configs/collections/*.yaml**:
- **Purpose**: Collection bulk generation configuration
- **Format**: YAML (version 1.0)
- **Required**: No (only if using collections)

**templates/*.j2**:
- **Purpose**: Reusable Jinja2 templates
- **Format**: Jinja2 template syntax
- **Required**: No (can use inline templates in configs)

**output/**:
- **Purpose**: Generated content output directory
- **Format**: Various (markdown, JSON, YAML, etc.)
- **Required**: Created automatically
- **Git**: Excluded (add to .gitignore)

**.chora-compose/**:
- **Purpose**: Ephemeral storage, cache (30-day retention)
- **Format**: Internal chora-compose format
- **Required**: Created automatically
- **Git**: Excluded (add to .gitignore)

---

## 6. Validation & Testing

### Validation Rules

**Rule 1: Installation Check**
- **Check**: chora-compose is installed and accessible
- **Requirement**: `chora-compose --version` succeeds (CLI) or `import chora_compose` works (pip)
- **Error Message**: "chora-compose not found. Install with: pip install chora-compose"

**Rule 2: Config Syntax**
- **Check**: YAML config is valid and matches schema
- **Requirement**: Parses without errors, has required fields
- **Error Message**: "Invalid config: [specific syntax error]"

**Rule 3: Generator Available**
- **Check**: Specified generator_type exists
- **Requirement**: Generator registered in registry
- **Error Message**: "Unknown generator: {generator_type}. Use `list capabilities` to see available generators"

**Rule 4: Output Path Writable**
- **Check**: Output directory is writable
- **Requirement**: Write permissions, parent directory exists
- **Error Message**: "Cannot write to output path: {path}. Check permissions"

### Testing Protocol

**Unit Tests** (for pip integration):
```bash
# Run unit tests
pytest tests/

# With coverage
pytest --cov=chora_compose tests/
```

**Integration Tests**:
```bash
# Test pip integration
python scripts/generate_docs.py

# Test CLI
chora-compose generate content --config configs/test-config.yaml

# Test MCP (via Claude Desktop)
# Manually test MCP tools in Claude Desktop
```

**Manual Verification**:
1. Install chora-compose via chosen modality
2. Create test config (hello-world example)
3. Generate content and verify output exists
4. Check output content matches expected format
5. Expected result: Output file exists with correct content

---

## 7. Error Handling

### Error 1: ModuleNotFoundError (pip)

**Condition**: chora-compose not installed or not in Python path

**Error Message**:
```
ModuleNotFoundError: No module named 'chora_compose'
```

**Resolution**:
1. Install chora-compose: `pip install chora-compose`
2. Verify installation: `python -c "import chora_compose; print(chora_compose.__version__)"`
3. If using virtual environment, ensure it's activated

**Prevention**:
- Use `requirements.txt` to track dependencies
- Document installation in project README

---

### Error 2: Docker Not Running (MCP)

**Condition**: Docker Desktop not running when using MCP server modality

**Error Message**:
```
Cannot connect to the Docker daemon. Is the docker daemon running?
```

**Resolution**:
1. Start Docker Desktop application
2. Wait for Docker to fully start (whale icon in system tray)
3. Verify: `docker ps` succeeds
4. Restart Claude Desktop

**Prevention**:
- Set Docker Desktop to start automatically on login
- Add Docker status check to troubleshooting docs

---

### Error 3: Invalid Config Syntax

**Condition**: YAML syntax error or missing required fields

**Error Message**:
```
ConfigValidationError: Invalid config at configs/my-config.yaml
- Missing required field: 'content_id'
- Line 12: invalid YAML syntax
```

**Resolution**:
1. Validate YAML syntax: use online YAML validator or `yamllint`
2. Check required fields: `version`, `content_id`, `generator_type`, `output_path`
3. Use `chora-compose validate --config configs/my-config.yaml` (CLI)

**Prevention**:
- Use templates or `create_content_config` tool to generate valid configs
- Run validation before committing configs to version control

---

### Error 4: Permission Denied (Output Path)

**Condition**: No write permission to output directory

**Error Message**:
```
PermissionError: [Errno 13] Permission denied: 'output/docs/api-reference.md'
```

**Resolution**:
1. Check output directory permissions: `ls -la output/`
2. Fix permissions: `chmod -R u+w output/`
3. Ensure parent directory exists: `mkdir -p output/docs/`

**Prevention**:
- Create output directory with correct permissions before generation
- Document required permissions in project README

---

## 8. Performance Considerations

### Performance Benchmarks

Comprehensive performance metrics for all 4 modalities are documented in [ledger.md §6.1 Performance Metrics](./ledger.md#performance-metrics).

**Quick Reference** (M1 Mac, 16GB RAM, chora-compose v1.5.0):

| Modality | Operation | Median (p50) | p95 | Use Case |
|----------|-----------|--------------|-----|----------|
| **pip** | Generate small content (1KB) | 150ms | 280ms | Fast Python integration |
| **pip** | Assemble 5-piece artifact | 650ms | 1.2s | Programmatic builds |
| **MCP** | Tool invocation latency | 45ms | 95ms | AI agent interactions |
| **MCP** | Generate via MCP | 380ms | 720ms | Interactive generation |
| **CLI** | CLI startup | 420ms | 680ms | Command-line testing |
| **Docker** | Generate via Docker | 1.2s | 2.1s | Team consistency |

**Collection Performance** (18-artifact SAP generation):
- **Sequential**: 18.5s (0.97 artifacts/s)
- **Parallel (4 workers)**: 6.2s (2.9 artifacts/s) - **Recommended**
- **Parallel (8 workers)**: 5.8s (3.1 artifacts/s) - Diminishing returns
- **Cache hit rate**: 94%+ (5-10x speedup on cache hits)

**Run Your Own Benchmarks**:

```bash
# Quick benchmark (10 iterations)
python benchmark-chora-compose.py

# Full benchmark (100 iterations)
python benchmark-chora-compose.py --iterations 100

# Single modality
python benchmark-chora-compose.py --modality pip --iterations 100

# Export results
python benchmark-chora-compose.py --export md --output my-benchmarks.md
```

See [benchmark-chora-compose.py](./benchmark-chora-compose.py) for the benchmarking script.

---

### Performance Targets

| Operation | Target Time | Actual (Median) | Status | Notes |
|-----------|-------------|-----------------|--------|-------|
| Install (pip) | < 2 minutes | ~1 minute | ✅ Met | Depends on network speed |
| Install (MCP) | < 10 minutes | ~5 minutes | ✅ Met | Includes Docker pull |
| First config creation | < 5 minutes | ~3 minutes | ✅ Met | Interactive or copy template |
| Generate single content | < 5 seconds | 150-580ms | ✅ Met | Simple template, small context |
| Generate artifact (5 pieces) | < 20 seconds | 650ms-1.2s | ✅ Met | 5 content pieces + assembly |
| Generate collection (18 SAPs) | < 5 minutes | 6.2s (parallel) | ✅ Met | Parallel generation, 94% cache hit |

---

### Optimization Strategies

1. **Strategy 1: Use Caching**
   - **When to use**: Generating content multiple times with unchanged context
   - **Impact**: 94%+ cache hit rate = 5-10x speedup (from seconds to milliseconds)
   - **Implementation**: Caching automatic (SHA-256 context hashing)
   - **Measured**: 94% hit rate in production (SAP generation workload)

2. **Strategy 2: Parallel Collection Generation**
   - **When to use**: Generating multiple independent artifacts
   - **Impact**: 3x faster than sequential (18.5s → 6.2s with 4 workers)
   - **Implementation**: Set `execution_strategy: parallel, max_workers: 4` in collection config
   - **Measured**: Near-linear scaling up to 4 workers, diminishing returns beyond

3. **Strategy 3: Reuse Templates**
   - **When to use**: Multiple content pieces with similar structure
   - **Impact**: Reduced config size, easier maintenance, faster config parsing
   - **Implementation**: Store templates in `templates/` directory, reference via `template_path`

4. **Strategy 4: Choose Right Modality for Use Case**
   - **pip**: Fastest (150ms), best for Python integration and CI/CD
   - **MCP**: Low latency (45ms overhead), best for AI agents
   - **Docker**: Slower (1.2s), best for team consistency and reproducibility
   - **See**: [select-modality.py](./select-modality.py) for guided selection

---

### Performance Monitoring

**Baseline Your Environment**:

```bash
# Run benchmark to establish baseline
python benchmark-chora-compose.py --iterations 100 --export md

# Compare periodically to detect regressions
# Expected: Within 20% of baseline (±20ms for fast operations)
```

**Key Metrics to Track**:
1. **Cache hit rate**: Should stay >90% in production (check logs)
2. **Generation latency**: p95 should be within 2x of median
3. **Parallel efficiency**: 4 workers should be 3-4x faster than sequential

---

## 9. Security Considerations

### Security Requirements

1. **Requirement 1: No Secrets in Configs**
   - **Risk**: API keys, passwords exposed in version-controlled configs
   - **Mitigation**: Use environment variables or external files (excluded from git) for sensitive data

2. **Requirement 2: Output Path Validation**
   - **Risk**: Path traversal attacks writing to unintended locations
   - **Mitigation**: chora-compose validates output paths are within project root

3. **Requirement 3: Docker Volume Mounts**
   - **Risk**: MCP server with excessive permissions accessing sensitive files
   - **Mitigation**: Mount only workspace directory, not entire home directory

### Sensitive Data

**Data Types**:
- API keys, tokens: Use environment variables, never hardcode in configs
- Credentials: Store in external files (`.env`), exclude from git
- PII: Avoid including in context sources or templates

**Storage**:
- Ephemeral storage (`.chora-compose/`) contains temporary outputs (30-day retention)
- Ensure `.chora-compose/` is excluded from version control
- Generated output may contain sensitive data - review before committing

---

## 10. Versioning & Compatibility

### Version History

| Version | Date | Changes | Breaking |
|---------|------|---------|----------|
| 2.0.0 | 2025-11-04 | Complete rewrite: chora-compose integration (was Docker Compose) | Yes |
| 1.0.0 | 2025-10-29 | Initial version (Docker Compose content, wrong tool) | N/A |

### Compatibility Matrix

| SAP-017 Version | chora-compose Version | Required SAP Versions | Notes |
|---------|------------------------------|-------|-------|
| 2.0.0 | v1.4.0+ (Collections Complete) | SAP-000 v2.0+ | Collections architecture support |
| 1.0.0 | N/A (Docker Compose) | SAP-000 v1.0+ | Archived (wrong tool) |

### Migration Guides

**Migrating from v1.0.0 to v2.0.0**:

This is a **complete rewrite**, not a migration:
- v1.0.0 documented Docker Compose (container orchestration)
- v2.0.0 documents chora-compose (content generation framework)
- No migration path exists (different tools entirely)
- v1.0.0 content archived to `archives/sap-017-v1.0.0-docker-compose/`

**If you need Docker Compose documentation**:
- See archived v1.0.0 content
- Consider enhancing SAP-011 (docker-operations) with Docker Compose patterns
- Create new SAP-030/031 specifically for Docker Compose if needed

---

## 11. Examples

### Example 1: Basic pip Usage

**Scenario**: Generate API documentation from OpenAPI spec using pip integration.

**Setup**:
```bash
# Install
pip install chora-compose

# Create config
mkdir -p configs/content
cat > configs/content/api-docs.yaml <<EOF
version: "3.1"
content_id: api-docs
generator_type: jinja2
output_path: docs/api-reference.md

template: |
  # API Reference

  {% for path, methods in paths.items() %}
  ## {{ path }}

  {% for method, details in methods.items() %}
  ### {{ method|upper }}
  {{ details.summary }}
  {% endfor %}
  {% endfor %}

context:
  external_file:
    path: specs/openapi.yaml
    format: yaml
EOF
```

**Execution**:
```python
from chora_compose import ConfigLoader, ContentGenerator

loader = ConfigLoader()
config = loader.load_content_config("configs/content/api-docs.yaml")

generator = ContentGenerator()
result = generator.generate(config)

print(f"✓ Generated: {result.output_path}")
```

**Expected Result**:
```
✓ Generated: docs/api-reference.md
```

File `docs/api-reference.md` contains formatted API documentation.

---

### Example 2: MCP Conversational Usage

**Scenario**: AI agent (Claude Desktop) creates and generates content conversationally.

**Setup**: MCP server configured in Claude Desktop (see Contract 2)

**Conversation**:
```
User: "I need to generate API documentation. Can you help?"

Claude: "I can help you generate API documentation using chora-compose.
        Do you have an OpenAPI spec file?"

User: "Yes, it's at specs/openapi.yaml"

Claude: "Great! I'll create a content config for you."
        [Uses create_content_config tool with Jinja2 generator]
        "I've created the config. Would you like me to generate the documentation now?"

User: "Yes, please generate it to docs/api-reference.md"

Claude: [Uses generate_content tool]
        "✓ Documentation generated at docs/api-reference.md"
```

**Result**: API documentation generated conversationally with no manual config creation.

---

## 12. Troubleshooting

### Issue 1: MCP Server Not Showing in Claude Desktop

**Symptoms**:
- Claude Desktop doesn't show chora-compose in MCP servers list
- Tools not available in Claude conversation

**Diagnosis**:
```bash
# Check Docker is running
docker ps

# Check config.json syntax
cat ~/.config/claude/config.json | jq .

# Check Docker image exists
docker images | grep chora-compose-mcp
```

**Solution**:
1. Verify config.json has correct syntax (valid JSON)
2. Ensure Docker Desktop is running
3. Restart Claude Desktop (completely quit and reopen)
4. Check Claude Desktop logs for MCP server errors
5. Manually pull image: `docker pull ghcr.io/liminalcommons/chora-compose-mcp:latest`

---

### Issue 2: Generation Fails with "Generator Not Found"

**Symptoms**:
- Error: "Unknown generator: {generator_type}"
- Generation fails immediately

**Diagnosis**:
```bash
# List available generators
chora-compose list capabilities

# Check config syntax
cat configs/my-config.yaml
```

**Solution**:
1. Verify `generator_type` in config matches available generator (case-sensitive)
2. Available generators: `jinja2`, `demonstration`, `template_fill` (v1.5+)
3. Update config with correct generator name
4. For custom generators, ensure they're registered in generator registry

---

### Issue 3: Slow First Generation

**Symptoms**:
- First generation takes 30+ seconds
- Subsequent generations much faster

**Diagnosis**: This is expected behavior (cold start, no cache)

**Solution**:
1. First generation builds cache (context resolution, template compilation)
2. Subsequent generations use cache (5-10x faster)
3. No action needed - this is normal behavior
4. To force rebuild: use `invalidate_cache` tool or delete `.chora-compose/cache/`

---

## 13. References

### Internal Documentation

- [capability-charter.md](./capability-charter.md) - Problem statement, solution, scope
- [awareness-guide.md](./awareness-guide.md) - AI agent quick reference and decision trees
- [adoption-blueprint.md](./adoption-blueprint.md) - Step-by-step Level 1/2/3 adoption guide
- [ledger.md](./ledger.md) - Version history and adoption tracking

### External Resources

- [chora-compose README](https://github.com/liminalcommons/chora-compose) - Project overview and quick start
- [chora-compose AGENTS.md](https://github.com/liminalcommons/chora-compose/blob/main/AGENTS.md) - Complete MCP tools documentation (22 tools)
- [chora-compose Documentation](https://github.com/liminalcommons/chora-compose/tree/main/docs) - Comprehensive docs (Diátaxis framework)
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - Required for MCP and Docker modalities

---

**Document Version**: 2.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
