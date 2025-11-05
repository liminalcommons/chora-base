# Adoption Blueprint: chora-compose Integration

**SAP ID**: SAP-017
**Version**: 2.0.0
**Last Updated**: 2025-11-04

---

## Overview

This blueprint provides step-by-step instructions for adopting chora-compose across three progressive levels: Basic adoption (< 30 min), Production integration (1-2 days), and Advanced patterns (1-2 weeks).

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Install + first success | < 30 minutes | None | Quick start, proof-of-concept, learning |
| **Level 2: Production** | Real project integration | 1-2 days | Minimal (config updates) | Production use, team workflows |
| **Level 3: Advanced** | Multi-modality + custom patterns | 1-2 weeks | Low (advanced patterns) | **Recommended for production excellence** |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption)

**Quick Path for Experienced Users**: Can skip Level 1, go directly to Level 2 if familiar with content generation frameworks.

---

## Level 1: Basic Adoption (< 30 minutes)

### Purpose

Level 1 adoption is suitable for:
- **Getting started** with chora-compose (first-time users)
- **Understanding core concepts** (modalities, configs, generation)
- **Proof-of-concept** (validate chora-compose fits your needs)
- **Development and testing** environments
- **Quick wins** (< 30 min from zero to first generated content)

### Time Estimate

- **Setup**: 15-25 minutes (choose modality, install, generate first content)
- **Learning Curve**: Easy - Minimal concepts required for basic usage

### Prerequisites

**Required**:
- **Python 3.12+** (for pip, CLI modalities) - check: `python --version`
- **Docker Desktop** (for MCP, Docker modalities) - check: `docker --version`
- **Basic command-line skills** (cd, ls, running commands)
- **Text editor** for editing YAML files
- **SAP-000 (sap-framework)** - Understanding of SAP structure (optional but helpful)

**Recommended**:
- **Git** for version control of configs
- **Claude Desktop or Cursor** (if using MCP modality)

### Step-by-Step Instructions

#### Step 1.1: Choose Your Integration Modality

**Purpose**: Determine which of the 4 integration paths matches your role/use case.

**Decision Tree**:
- **Python developer** integrating in code? → Choose **pip modality**
- **AI agent user** (Claude Desktop, Cursor)? → Choose **MCP server modality**
- **Testing/exploring** chora-compose? → Choose **CLI modality**
- **Team deployment** or n8n workflows? → Choose **Docker modality**

**Action**: Select ONE modality for Level 1. You can adopt additional modalities in Level 3.

**Verification**: You have chosen: [ ] pip, [ ] MCP, [ ] CLI, or [ ] Docker

---

#### Step 1.2: Install chora-compose

**Purpose**: Install chosen modality.

**For pip modality**:
```bash
pip install chora-compose
```

**For MCP modality**:
1. Install Docker Desktop (if not installed): https://www.docker.com/products/docker-desktop/
2. Edit `~/.config/claude/config.json` (macOS/Linux) or `%APPDATA%\Claude\config.json` (Windows)
3. Add MCP server configuration:
```json
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
4. Restart Claude Desktop

**For CLI modality**:
```bash
pip install "chora-compose[cli]"
```

**For Docker modality**:
1. Create `docker-compose.yml`:
```yaml
version: "3.8"
services:
  chora-compose-mcp:
    image: ghcr.io/liminalcommons/chora-compose-mcp:latest
    volumes:
      - ./workspace:/workspace
    restart: unless-stopped
```
2. Start service:
```bash
docker-compose up -d
```

**Verification**:
```bash
# pip/CLI: Check installation
python -c "import chora_compose; print(chora_compose.__version__)"
chora-compose --version

# MCP: Check Docker image
docker images | grep chora-compose-mcp

# Docker: Check service
docker-compose ps
```

**Expected Output**: Installation succeeds, version displayed (e.g., "1.4.0" or later).

---

#### Step 1.3: Create First Config (Hello World)

**Purpose**: Create a minimal content config for testing.

**For pip/CLI modalities**:

Create directory:
```bash
mkdir -p configs/
```

Create `configs/hello-world.yaml`:
```yaml
version: "3.1"
content_id: hello-world
generator_type: jinja2
output_path: output/hello-world.md

template: |
  # Hello World from chora-compose!

  This is my first generated content.

  **Generated at**: {{ timestamp }}
  **Using modality**: {{ modality }}

context:
  inline_data:
    timestamp: "2025-11-04T12:00:00"
    modality: "pip"  # Change to "CLI" if using CLI modality
```

**For MCP modality**:

In Claude Desktop, say:
```
User: "Create a hello-world content config for chora-compose"

Claude: [Uses create_content_config tool]
        "I've created a hello-world config. Would you like me to save it?"

User: "Yes, save to configs/hello-world.yaml"

Claude: [Saves config to file]
```

**Verification**:
```bash
# Check config exists
ls configs/hello-world.yaml

# Check syntax (CLI)
chora-compose validate --config configs/hello-world.yaml
```

**Expected Output**: Config file exists, validation passes.

---

#### Step 1.4: Generate First Content

**Purpose**: Run generation workflow, produce output file.

**For pip modality**:

Create `generate.py`:
```python
from chora_compose import ConfigLoader, ContentGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("configs/hello-world.yaml")

# Generate content
generator = ContentGenerator()
result = generator.generate(config)

# Write output
with open(result.output_path, "w") as f:
    f.write(result.content)

print(f"✓ Generated: {result.output_path}")
```

Run:
```bash
python generate.py
```

**For CLI modality**:
```bash
chora-compose generate content --config configs/hello-world.yaml
```

**For MCP modality**:

In Claude Desktop:
```
User: "Generate content from configs/hello-world.yaml"

Claude: [Uses generate_content tool]
        "✓ Generated: output/hello-world.md"
```

**Verification**:
```bash
# Check output exists
ls output/hello-world.md

# View content
cat output/hello-world.md
```

**Expected Output**:
```markdown
# Hello World from chora-compose!

This is my first generated content.

**Generated at**: 2025-11-04T12:00:00
**Using modality**: pip
```

---

### Level 1 Validation Checklist

- [ ] Chosen integration modality (pip/MCP/CLI/Docker)
- [ ] Installed chora-compose successfully
- [ ] Created first config (`hello-world.yaml`)
- [ ] Generated first content (`output/hello-world.md`)
- [ ] Output file exists and contains expected content
- [ ] **Total time**: < 30 minutes

**Success Criteria**: All checklist items complete, first content generated successfully.

**If you encounter issues**: See [protocol-spec.md](./protocol-spec.md) Section 12 (Troubleshooting) or [awareness-guide.md](./awareness-guide.md) Section 4 (Common Issues).

---

## Level 2: Production Integration (1-2 days)

### Purpose

Level 2 adoption is suitable for:
- **Production environments** (real projects, not toy examples)
- **Team collaboration** (shared configs, version control)
- **Real content generation** (documentation, configs, test data, etc.)
- **Measured ROI** (2-5x productivity improvement vs manual)
- **Repeatable workflows** (build scripts, CI/CD integration)

### Time Estimate

- **Setup**: 1-2 days (setup project structure, create production configs, integrate in workflows, train team)
- **Learning Curve**: Moderate - Requires understanding of templates, context sources, and generation workflows

### Prerequisites

**Required**:
- **Level 1 completed** - Basic modality working
- **Real use case** - Specific content generation need (docs, configs, etc.)
- **Project structure** - Directory for configs, templates, output
- **Version control** - Git repository for tracking configs

**Recommended**:
- **SAP-027 (dogfooding-patterns)** - For 5-week pilot methodology
- **Team buy-in** - Stakeholders agree to chora-compose adoption
- **ROI tracking** - Method to measure productivity improvement

### Step-by-Step Instructions

#### Step 2.1: Set Up Project Structure

**Purpose**: Create organized directory structure for configs, templates, output.

**Action**:
```bash
# Create directories
mkdir -p configs/{content,artifacts,collections}
mkdir -p templates
mkdir -p output

# Add .gitignore
cat >> .gitignore <<EOF
# chora-compose output and cache
output/
.chora-compose/
EOF
```

**Verification**:
```bash
# Check structure
tree -L 2 .
```

**Expected Output**:
```
.
├── configs/
│   ├── content/
│   ├── artifacts/
│   └── collections/
├── templates/
├── output/ (excluded from git)
└── .gitignore
```

---

#### Step 2.2: Identify Real Content Generation Use Cases

**Purpose**: Determine what content you'll generate in production.

**Common Use Cases**:
- **API Documentation**: Generate from OpenAPI/Swagger specs
- **Configuration Files**: Generate environment-specific configs
- **Test Data**: Generate test fixtures, mock data
- **Project Scaffolding**: Generate boilerplate code, templates
- **Documentation**: Generate user guides, technical docs from structured data

**Action**:
1. List 2-3 specific content pieces your project needs
2. Identify source data for each (files, APIs, databases, manual input)
3. Define desired output format (markdown, JSON, YAML, etc.)

**Example**:
- **Use Case 1**: API docs from `specs/openapi.yaml` → `docs/api-reference.md`
- **Use Case 2**: Test fixtures from `specs/schemas.json` → `tests/fixtures/*.json`
- **Use Case 3**: Deployment configs from `environments/*.yaml` → `deploy/configs/*.yaml`

**Verification**: You have documented 2-3 real use cases with source data and output paths.

---

#### Step 2.3: Create Production Configs

**Purpose**: Build real content configs for identified use cases.

**Example**: API Documentation

Create `configs/content/api-docs.yaml`:
```yaml
version: "3.1"
content_id: api-docs
generator_type: jinja2
output_path: docs/api-reference.md

template_path: templates/api-docs.md.j2

context:
  external_file:
    path: specs/openapi.yaml
    format: yaml
```

Create `templates/api-docs.md.j2`:
```jinja2
# API Reference

{{ title }}

## Endpoints

{% for path, methods in paths.items() %}
### {{ path }}

{% for method, spec in methods.items() %}
#### {{ method | upper }}

{{ spec.summary }}

**Parameters**:
{% for param in spec.parameters %}
- `{{ param.name }}` ({{ param.in }}): {{ param.description }}
{% endfor %}

**Response**:
```json
{{ spec.responses['200'].example | tojson(indent=2) }}
```

{% endfor %}
{% endfor %}
```

**Repeat for other use cases** (test data, configs, etc.)

**Verification**:
```bash
# Check configs exist
ls configs/content/

# Validate syntax
chora-compose validate --config configs/content/api-docs.yaml
```

**Expected Output**: Configs validated successfully.

---

#### Step 2.4: Integrate in Build/Workflow

**Purpose**: Automate generation in existing workflows (build scripts, CI/CD, pre-commit hooks).

**For Python projects (pip modality)**:

Create `scripts/generate_content.py`:
```python
#!/usr/bin/env python3
"""Generate all project content using chora-compose."""

from chora_compose import ConfigLoader, ContentGenerator
from pathlib import Path

def generate_all():
    """Generate content from all configs."""
    loader = ConfigLoader()
    generator = ContentGenerator()

    config_dir = Path("configs/content")
    for config_path in config_dir.glob("*.yaml"):
        print(f"Generating from {config_path.name}...")
        config = loader.load_content_config(str(config_path))
        result = generator.generate(config)
        print(f"  ✓ {result.output_path}")

if __name__ == "__main__":
    generate_all()
```

**Add to build process**:
```bash
# In Makefile, package.json scripts, or CI/CD
make docs:
  python scripts/generate_content.py
```

**For AI agent workflows (MCP modality)**:

Document in `configs/README.md`:
```markdown
# Content Generation

## Quick Start
1. Open Claude Desktop
2. Say "generate all chora-compose content"
3. Claude uses MCP tools to generate

## Configs
- `content/api-docs.yaml`: API documentation
- `content/test-data.yaml`: Test fixtures
```

**Verification**:
```bash
# Run generation
python scripts/generate_content.py

# Check outputs
ls docs/*.md tests/fixtures/*.json
```

**Expected Output**: All content generated successfully, outputs exist.

---

#### Step 2.5: Measure Productivity & ROI

**Purpose**: Quantify time savings and productivity improvement.

**Metrics to Track**:
- **Time to generate manually**: X hours/minutes
- **Time to generate with chora-compose**: Y hours/minutes
- **Productivity multiplier**: X / Y (target: ≥2x)
- **Frequency**: How often content is generated (weekly, per release, etc.)
- **ROI**: (Time saved × frequency × hourly rate) - setup cost

**Example Calculation**:
- Manual API docs generation: 2 hours
- chora-compose generation: 10 minutes
- Productivity: 2 hours / 10 min = **12x improvement**
- Frequency: 2x per week
- Weekly time saved: (2 hours - 10 min) × 2 = **3.7 hours/week**

**Action**:
1. Time manual content generation (baseline)
2. Time chora-compose generation
3. Calculate productivity multiplier
4. Document in project README or metrics dashboard

**Verification**: You have documented ROI showing ≥2x productivity improvement.

---

### Level 2 Validation Checklist

- [ ] Project structure set up (configs/, templates/, output/)
- [ ] 2-3 real production use cases identified
- [ ] Production configs created and validated
- [ ] Content generation integrated in build/workflow
- [ ] ROI measured showing ≥2x productivity
- [ ] Team trained on usage (if applicable)
- [ ] Configs in version control
- [ ] **Total time**: 1-2 days

**Success Criteria**: Real content generating in production workflows, ROI ≥2x vs manual.

---

## Level 3: Advanced Patterns (1-2 weeks)

### Purpose

Level 3 adoption is suitable for:
- **Multi-modality usage** (combine pip + MCP + CLI for different workflows)
- **Advanced patterns** (Artifacts, Collections, recursive generation)
- **Custom templates** (domain-specific, organization-specific)
- **Optimization** (caching, parallel generation, performance tuning)
- **Community contribution** (share configs, templates, patterns)
- **Production excellence** (5-10x productivity, zero manual content generation)

### Time Estimate

- **Setup**: 1-2 weeks (explore advanced features, customize templates, optimize workflows, pilot with team)
- **Learning Curve**: Advanced - Requires deep understanding of chora-compose architecture, Collections, custom generators

### Prerequisites

**Required**:
- **Level 2 completed** - Production integration working
- **SAP-018 (chora-compose Architecture)** - Deep architecture understanding
- **Comfort with Jinja2** - Advanced template syntax, filters, macros
- **Performance goals** - Target productivity (5-10x) and generation speed

**Recommended**:
- **SAP-029 (sap-generation)** - Automated SAP artifact generation patterns
- **SAP-031 (Collections Patterns)** - Best practices for Collections
- **Custom generator development** skills (Python)

### Advanced Patterns

#### Pattern 3.1: Multi-Modality Workflows

**Use Case**: Combine modalities for different stages of content creation.

**Example Workflow**:
1. **MCP (Claude Desktop)**: Interactively create and refine config
2. **CLI**: Test config changes locally before committing
3. **pip**: Integrate in CI/CD for automated generation

**Benefits**:
- Flexibility: Use right modality for right task
- Productivity: AI-assisted config creation + automated generation
- Validation: Test locally before production

**Implementation**:
```bash
# 1. Create config with Claude Desktop (MCP)
# User: "Create config for API docs"
# Claude: [Uses create_content_config]

# 2. Test locally (CLI)
chora-compose generate content --config configs/api-docs.yaml

# 3. Commit config, CI/CD runs generation (pip)
git add configs/api-docs.yaml
git commit -m "Add API docs config"
# CI runs: python scripts/generate_content.py
```

---

#### Pattern 3.2: Artifact Assembly

**Use Case**: Combine multiple content pieces into single artifact.

**Example**: Multi-section documentation from separate sources.

Create `configs/artifacts/full-api-docs.yaml`:
```yaml
version: "3.1"
artifact_id: full-api-docs
output_path: docs/api-complete.md

pieces:
  - content_config_path: configs/content/api-intro.yaml
  - content_config_path: configs/content/api-endpoints.yaml
  - content_config_path: configs/content/api-examples.yaml
  - content_config_path: configs/content/api-errors.yaml

assembly_strategy: concatenate
separator: "\n\n---\n\n"
```

**Generate**:
```bash
chora-compose generate artifact --config configs/artifacts/full-api-docs.yaml
```

**Result**: Single `docs/api-complete.md` with all sections assembled.

---

#### Pattern 3.3: Collection (Bulk Generation)

**Use Case**: Generate many similar artifacts in parallel.

**Example**: Generate 18 SAP artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger) × 18 SAPs.

Create `configs/collections/all-saps.yaml`:
```yaml
version: "1.0"
collection_id: all-saps
description: "Generate all 18 SAP artifacts"

execution_strategy: parallel
workers: 4

artifacts:
  - artifact_config_path: configs/artifacts/sap-001.yaml
  - artifact_config_path: configs/artifacts/sap-002.yaml
  # ... (18 total)
  - artifact_config_path: configs/artifacts/sap-018.yaml
```

**Generate**:
```bash
chora-compose generate collection --config configs/collections/all-saps.yaml
```

**Performance**: Parallel generation (4 workers) = 3-4x faster than sequential.

---

#### Pattern 3.4: Custom Templates with Macros

**Use Case**: Reusable template components across multiple configs.

Create `templates/_macros.j2`:
```jinja2
{% macro render_section(title, content) %}
## {{ title }}

{{ content }}

---
{% endmacro %}

{% macro render_code_block(language, code) %}
```{{ language }}
{{ code }}
```
{% endmacro %}
```

Use in `templates/api-docs.md.j2`:
```jinja2
{% import '_macros.j2' as macros %}

# API Documentation

{{ macros.render_section("Overview", overview) }}

{% for endpoint in endpoints %}
{{ macros.render_section(endpoint.name, endpoint.description) }}
{{ macros.render_code_block("bash", endpoint.curl_example) }}
{% endfor %}
```

**Benefits**: DRY (Don't Repeat Yourself), consistent formatting, easier maintenance.

---

### Level 3 Validation Checklist

- [ ] Using 2+ modalities for different workflows
- [ ] Created at least one Artifact (multi-piece assembly)
- [ ] Created at least one Collection (bulk generation)
- [ ] Custom templates with macros/reusable components
- [ ] Measured productivity ≥5x vs manual (Level 2 was ≥2x)
- [ ] Configs shared with team or community
- [ ] Zero manual content generation (all automated)
- [ ] **Total time**: 1-2 weeks

**Success Criteria**: Advanced patterns in production, 5-10x productivity, zero manual generation.

---

## Troubleshooting & Support

### Common Adoption Issues

**Issue 1: "Level 1 took longer than 30 minutes"**
- **Cause**: Unfamiliarity with concepts, installation issues, Docker setup delays
- **Fix**: Follow troubleshooting in [protocol-spec.md](./protocol-spec.md) Section 12
- **Prevention**: Review [awareness-guide.md](./awareness-guide.md) before starting

**Issue 2: "ROI not meeting Level 2 target (≥2x)"**
- **Cause**: Configs too simple (not automating enough), content structure doesn't match templates
- **Fix**: Review use cases, ensure you're automating repetitive content, refine templates
- **Goal**: Target 50-80% time savings

**Issue 3: "Team not adopting chora-compose"**
- **Cause**: Lack of training, unclear value proposition, complexity perceived too high
- **Fix**: Use SAP-027 (dogfooding-patterns) 5-week pilot, measure and communicate ROI
- **Goal**: ≥80% team adoption for relevant content tasks

### Where to Get Help

**Internal Resources**:
- [protocol-spec.md](./protocol-spec.md) - Technical contracts, troubleshooting
- [awareness-guide.md](./awareness-guide.md) - Decision trees, agent workflows
- [capability-charter.md](./capability-charter.md) - Problem statement, scope

**External Resources**:
- [chora-compose README](https://github.com/liminalcommons/chora-compose) - Official docs
- [chora-compose Discussions](https://github.com/liminalcommons/chora-compose/discussions) - Community Q&A

**Related SAPs**:
- SAP-027: Dogfooding Patterns (5-week pilot methodology)
- SAP-029: SAP Generation (automated SAP artifact generation)
- SAP-018: chora-compose Architecture (deep architecture)

---

## Success Metrics Summary

| Level | Time Investment | Productivity Multiplier | Success Criteria |
|-------|-----------------|-------------------------|------------------|
| **Level 1** | < 30 minutes | N/A | First content generated |
| **Level 2** | 1-2 days | 2-5x | Real content in production, ROI positive |
| **Level 3** | 1-2 weeks | 5-10x | Zero manual generation, advanced patterns |

**Recommended Path**:
1. Start with Level 1 (validate chora-compose fits your needs)
2. Move to Level 2 (integrate in real workflows, measure ROI)
3. Adopt Level 3 (optimize, scale, achieve excellence)

---

**Document Version**: 2.0.0
**Last Updated**: 2025-11-04
**Maintainer**: Victor
