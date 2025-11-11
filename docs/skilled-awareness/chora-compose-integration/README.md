# SAP-017: Chora-Compose Integration

**Version:** 2.0.0 | **Status:** Active | **Maturity:** Production

> Choose from 4 integration modalities (pip/MCP/CLI/Docker) for chora-compose adoption—interactive modality selector guides you to <30 min time-to-first-success with role-based workflows for developers, AI agents, teams, and DevOps.

---

## 🚀 Quick Start (2 minutes)

```bash
# Interactive modality selector (recommended)
python scripts/select-modality.py
# Output: Guided questionnaire → Recommended modality → Quick start instructions

# Or choose modality directly:

# Option 1: pip (Python library integration)
pip install chora-compose
python -c "from chora_compose import ConfigLoader; print('✅ Installed')"

# Option 2: MCP Server (AI agent access)
python scripts/create-mcp-server.py --name "Chora-Compose MCP" --namespace chora --output ~/projects/chora-compose-mcp

# Option 3: CLI (interactive interface)
pip install chora-compose
chora-compose --help

# Option 4: Docker (team deployment)
docker build -t chora-compose:latest -f Dockerfile.chora-compose .
docker run -p 8000:8000 chora-compose:latest
```

**First time?** → Run `python scripts/select-modality.py` for personalized recommendation (2-min read)

---

## 📖 What Is SAP-017?

SAP-017 provides **integration guidance for chora-compose adoption** across 4 modalities: pip (library), MCP server (AI agents), CLI (interactive), and Docker (team deployment). It includes an interactive modality selector ([select-modality.py](select-modality.py)) that guides users to the right integration approach based on their role, use case, and environment.

**Key Innovation**: **Interactive modality selector** - 2-minute questionnaire analyzes your needs (role, team size, infrastructure, use case) and recommends the optimal integration path with <30 min time-to-first-success.

---

## 🎯 When to Use

Use SAP-017 when you need to:

1. **Choose integration approach** - Decide between pip, MCP, CLI, or Docker
2. **Quick adoption** - <30 min time-to-first-success across all modalities
3. **Role-based guidance** - Workflows tailored for developers, AI agents, teams, DevOps
4. **Multi-modal deployment** - Deploy chora-compose across different environments
5. **Decision validation** - Validate modality choice against requirements

**Not needed for**: Direct chora-compose usage (see chora-compose docs), or if modality already chosen

---

## ✨ Key Features

- ✅ **4 Integration Modalities** - pip (library), MCP (AI agents), CLI (interactive), Docker (team)
- ✅ **Interactive Selector** - `select-modality.py` guides to optimal modality (<2 min)
- ✅ **Role-Based Workflows** - Developer, AI agent, team, DevOps paths
- ✅ **<30 Min Time-to-First-Success** - Quick wins for all modalities
- ✅ **Decision Trees** - Clear modality selection criteria
- ✅ **Python 3.12+ Support** - Async generators, structural pattern matching
- ✅ **Troubleshooting Guides** - Common errors and resolutions
- ✅ **n8n Integration Examples** - Docker-based workflow automation

---

## 📚 Quick Reference

### Interactive Modality Selector

#### **select-modality.py** - Guided Recommendation

```bash
python scripts/select-modality.py

# Interactive questionnaire (2 minutes):
# 1. What is your primary role?
#    a) Developer (integrating into Python project)
#    b) AI Agent (Claude, Cursor, etc.)
#    c) Team Lead (team-wide deployment)
#    d) DevOps Engineer (infrastructure deployment)

# 2. What is your use case?
#    a) Generate documentation/configs in Python project
#    b) Enable AI agent to generate content
#    c) Interactive testing and prototyping
#    d) Team-wide content generation service

# 3. What is your team size?
#    a) Solo developer (1 person)
#    b) Small team (2-5 people)
#    c) Medium team (6-20 people)
#    d) Large team (20+ people)

# 4. What is your infrastructure preference?
#    a) Local development (laptop/desktop)
#    b) Cloud deployment (AWS, GCP, Azure)
#    c) On-premises servers
#    d) Container orchestration (Kubernetes, Docker Swarm)

# Output: Recommended modality + quick start instructions + rationale
```

**Example Output**:
```
🎯 Recommended Modality: pip (Python Library)

Rationale:
- Role: Developer → pip integration provides programmatic control
- Use case: Python project integration → Library usage fits naturally
- Team size: Solo → No team deployment needed
- Infrastructure: Local → No deployment complexity

Quick Start:
1. Install: pip install chora-compose
2. Import: from chora_compose import ConfigLoader
3. Docs: https://chora-compose.readthedocs.io/en/latest/

Time to first success: < 10 minutes
```

---

### Modality 1: pip (Python Library)

**Description**: Python library integration for direct code usage.

**When to Use**:
- Integrating chora-compose into Python projects
- Programmatic content generation (build scripts, CI/CD)
- Library usage in larger automation frameworks
- Need fine-grained control over generation

**Quick Start**:
```bash
# 1. Install
pip install chora-compose

# 2. Basic usage
python <<EOF
from chora_compose import ConfigLoader, ContentGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("config.yaml")

# Generate content
generator = ContentGenerator()
result = generator.generate(config)

# Access output
print(result.content)
print(result.output_path)
EOF

# 3. Verify
# Check result.output_path for generated content
```

**Requirements**:
- Python 3.12+ (async generators, structural pattern matching)
- pip or Poetry for dependency management
- Write access to output directory
- Git (optional, for `git_reference` context sources)

**Time to First Success**: < 10 minutes

---

### Modality 2: MCP Server (AI Agents)

**Description**: Model Context Protocol server deployment for AI agent access.

**When to Use**:
- Enabling AI agents (Claude Desktop, Cursor, Cline) to generate content
- Team-wide AI agent access to chora-compose
- Integration with MCP-compatible tools
- Need AI-driven content generation workflows

**Quick Start**:
```bash
# 1. Create MCP server from template
just create-mcp-server "Chora-Compose MCP" chora ~/projects/chora-compose-mcp

# 2. Navigate and install
cd ~/projects/chora-compose-mcp
uv sync

# 3. Install chora-compose in MCP server
uv add chora-compose

# 4. Implement MCP tools (edit src/chora_compose_mcp/server.py)
from mcp import mcp
from chora_compose import ConfigLoader, ContentGenerator

@mcp.tool()
def generate_content(config_path: str) -> dict:
    """Generate content from YAML config."""
    loader = ConfigLoader()
    config = loader.load_content_config(config_path)
    generator = ContentGenerator()
    result = generator.generate(config)
    return {"content": result.content, "path": result.output_path}

# 5. Test MCP server
just mcp-test

# 6. Configure Claude Desktop
just mcp-claude-config chora-compose-mcp ~/projects/chora-compose-mcp chora_compose_mcp
# Copy output to ~/Library/Application Support/Claude/claude_desktop_config.json

# 7. Restart Claude Desktop
# Use tool: "Use chora:generate_content with config_path 'config.yaml'"
```

**Requirements**:
- Python 3.12+ (chora-compose requirement)
- FastMCP library (MCP server SDK)
- Claude Desktop, Cursor, or Cline (MCP client)
- SAP-014 (MCP Server Development) adopted

**Time to First Success**: < 30 minutes

---

### Modality 3: CLI (Interactive Interface)

**Description**: Interactive command-line interface for testing and workflows.

**When to Use**:
- Interactive testing and prototyping
- Ad-hoc content generation
- Debugging config files
- Quick validation before automation

**Quick Start**:
```bash
# 1. Install
pip install chora-compose

# 2. Run CLI
chora-compose --help
# Output: Shows all available commands

# 3. Generate content interactively
chora-compose generate --config config.yaml --output output.md

# 4. Validate config
chora-compose validate --config config.yaml

# 5. List templates
chora-compose list-templates
```

**Requirements**:
- Python 3.12+
- pip for installation
- Write access to output directory
- Terminal access

**Time to First Success**: < 15 minutes

---

### Modality 4: Docker (Team Deployment)

**Description**: Container-based deployment for team access and n8n workflows.

**When to Use**:
- Team-wide content generation service
- n8n workflow integration
- Cloud deployment (AWS, GCP, Azure)
- Container orchestration (Kubernetes)
- Isolate dependencies from host system

**Quick Start**:
```bash
# 1. Build Docker image
docker build -t chora-compose:latest -f Dockerfile.chora-compose .

# 2. Run container
docker run -d -p 8000:8000 \
  -v ./configs:/app/configs:ro \
  -v ./output:/app/output \
  chora-compose:latest

# 3. Test service
curl http://localhost:8000/health
# Output: {"status": "ok"}

# 4. Generate content via HTTP
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"config_path": "/app/configs/config.yaml"}'

# 5. n8n integration (optional)
# See n8n-examples/ for workflow templates
```

**Requirements**:
- Docker (or Docker Desktop)
- Docker Compose (optional, for orchestration)
- Port 8000 available
- Volume mounts for configs and output

**Time to First Success**: < 25 minutes

---

### Decision Trees

#### **Decision Tree 1: Choose Modality by Role**

```
Your Role?
├─ Developer → pip (library integration)
├─ AI Agent (Claude, Cursor) → MCP server
├─ Team Lead → Docker (team deployment)
└─ DevOps Engineer → Docker (infrastructure deployment)
```

---

#### **Decision Tree 2: Choose Modality by Use Case**

```
Your Use Case?
├─ Python project integration → pip
├─ AI agent content generation → MCP
├─ Interactive testing → CLI
├─ Team-wide service → Docker
└─ n8n workflow automation → Docker
```

---

#### **Decision Tree 3: Choose Modality by Team Size**

```
Team Size?
├─ Solo (1 person) → pip or CLI
├─ Small (2-5 people) → MCP or CLI
├─ Medium (6-20 people) → Docker
└─ Large (20+ people) → Docker (with Kubernetes)
```

---

### Role-Based Workflows

#### **Workflow 1: Developer (pip Integration)**

**Goal**: Integrate chora-compose into Python project for programmatic content generation.

```bash
# 1. Install chora-compose
pip install chora-compose

# 2. Create config file (config.yaml)
cat > config.yaml <<'EOF'
name: "API Documentation"
output_path: "docs/api.md"
context_sources:
  - type: file
    path: "src/api.py"
template: |
  # API Documentation

  Generated from: {{ context.files[0].path }}
EOF

# 3. Write Python script (generate_docs.py)
cat > generate_docs.py <<'EOF'
from chora_compose import ConfigLoader, ContentGenerator

loader = ConfigLoader()
config = loader.load_content_config("config.yaml")

generator = ContentGenerator()
result = generator.generate(config)

print(f"✅ Generated: {result.output_path}")
EOF

# 4. Run script
python generate_docs.py
# Output: ✅ Generated: docs/api.md

# 5. Integrate into CI/CD (GitHub Actions)
# Add to .github/workflows/docs.yml:
# - run: pip install chora-compose
# - run: python generate_docs.py
```

**Time**: < 10 minutes

---

#### **Workflow 2: AI Agent (MCP Integration)**

**Goal**: Enable Claude Desktop to generate content via chora-compose MCP server.

```bash
# 1. Create MCP server (see Modality 2 Quick Start above)
just create-mcp-server "Chora-Compose MCP" chora ~/projects/chora-compose-mcp

# 2. Implement tools (edit src/chora_compose_mcp/server.py)
# [See Modality 2 example code]

# 3. Configure Claude Desktop
just mcp-claude-config chora-compose-mcp ~/projects/chora-compose-mcp chora_compose_mcp

# 4. Restart Claude Desktop

# 5. Use in Claude
# User: "Use the chora:generate_content tool to generate API docs from src/api.py"
# Claude: Calls tool → Returns generated content
```

**Time**: < 30 minutes

---

#### **Workflow 3: Team Lead (Docker Deployment)**

**Goal**: Deploy chora-compose as team-wide service for content generation.

```bash
# 1. Build Docker image
docker build -t chora-compose:latest -f Dockerfile.chora-compose .

# 2. Create docker-compose.yml
cat > docker-compose.yml <<'EOF'
version: '3.8'
services:
  chora-compose:
    image: chora-compose:latest
    ports:
      - "8000:8000"
    volumes:
      - ./configs:/app/configs:ro
      - ./output:/app/output
    environment:
      - ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

# 3. Start service
docker-compose up -d

# 4. Test service
curl http://localhost:8000/health

# 5. Share with team
# Team members can access service at http://your-server:8000
```

**Time**: < 25 minutes

---

## 🔗 Integration with Other SAPs

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-014** (MCP Server Development) | MCP Modality | Create chora-compose MCP server using SAP-014 templates |
| **SAP-011** (Docker Operations) | Docker Modality | Deploy chora-compose using SAP-011 Docker best practices |
| **SAP-005** (CI/CD) | pip Modality | Integrate chora-compose in GitHub Actions workflows |
| **SAP-018** (Chora-Compose Meta) | All Modalities | Use chora-compose to generate SAP documentation |

**Cross-SAP Workflow Example**:
```bash
# 1. Choose modality (SAP-017)
python scripts/select-modality.py
# Recommended: MCP (AI agent role)

# 2. Create MCP server (SAP-014)
just create-mcp-server "Chora-Compose MCP" chora ~/projects/chora-compose-mcp

# 3. Deploy with Docker (SAP-011)
just docker-build chora-compose-mcp latest

# 4. CI/CD validation (SAP-005)
# Add to .github/workflows/test.yml:
# - run: just mcp-test
```

---

## 🏆 Success Metrics

- **Modality Selection**: <2 minutes (interactive selector)
- **Time to First Success**: <30 minutes (all modalities)
- **pip Integration**: <10 minutes
- **MCP Integration**: <30 minutes
- **CLI Usage**: <15 minutes
- **Docker Deployment**: <25 minutes

---

## 🔧 Troubleshooting

**Problem**: `select-modality.py` not found

**Solution**: Run from repository root:
```bash
python scripts/select-modality.py
# Or with absolute path:
python /path/to/chora-base/scripts/select-modality.py
```

---

**Problem**: Import error `ModuleNotFoundError: No module named 'chora_compose'`

**Solution**: Install chora-compose:
```bash
pip install chora-compose
# Verify:
python -c "import chora_compose; print('✅ Installed')"
```

---

**Problem**: MCP server not loading in Claude Desktop

**Solution**: See SAP-014 troubleshooting for MCP server issues.

---

## 📄 Learn More

- **[protocol-spec.md](protocol-spec.md)** - Complete integration specifications (43KB, 22-min read)
- **[AGENTS.md](AGENTS.md)** - Agent integration workflows (14KB, 7-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration patterns (13KB, 7-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Integration setup guide (22KB, 11-min read)
- **[select-modality.py](select-modality.py)** - Interactive modality selector script
- **[n8n-examples/](n8n-examples/)** - n8n workflow integration examples

---

**Version History**:
- **2.0.0** (2025-11-04) - Added interactive modality selector, role-based workflows, decision trees
- **1.0.0** (2025-10-01) - Initial integration guide with 4 modalities

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
