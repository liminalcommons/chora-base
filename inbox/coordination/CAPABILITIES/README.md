# Capability Registry

**Purpose:** Per-repo capability declarations
**Format:** YAML files, one per repository
**Usage:** Dynamic task routing, dependency verification, discovery

---

## What is This?

The capability registry is a **distributed directory** where each repository declares:
- **What it provides** to the ecosystem
- **What it consumes** from other repos
- **What intake types** it can handle
- **How to contact** maintainers

This enables **capability-based routing** - tasks are sent to repos that can handle them.

---

## File Format

Each repository has a `CAPABILITIES/{repo-name}.yaml` file:

```yaml
repo: repository-name
version: 1.0.0
updated: YYYY-MM-DD

description: |
  Brief description of repository purpose

provides:
  - id: capability_id
    name: "Human Readable Name"
    description: "What this capability does"
    location: "path/to/implementation"
    version: "semver"
    consumers: [list of repos]

consumes:
  - repo: other-repo
    capability: capability_id
    reason: "Why needed"
    version: ">=1.0.0"

capabilities:
  can_receive:
    - type: strategic | coordination | task
      category: [list of categories]

inbox_protocol_version: "1.0"

maintainers:
  - name: Maintainer Name
    github: username

contact:
  - type: github_issue | slack | email
    url: contact_url
```

---

## Current Capabilities

### chora-base
**File:** [chora-base.yaml](chora-base.yaml)

**Provides:**
- MCP server templates
- Health endpoint template (planned)
- DRSO development workflow
- Vision-driven development framework
- Claude Code optimization patterns
- Diátaxis documentation standard

**Consumes:**
- ecosystem-manifest: server_registry, quality_standards

**Can Handle:**
- Strategic: template enhancement, documentation standards
- Coordination: template updates, standard changes
- Tasks: feature, bug, refactor, docs, test

---

### ecosystem-manifest (Template)
**File:** [ecosystem-manifest.yaml.template](ecosystem-manifest.yaml.template)

**Note:** This is a template! Copy to actual ecosystem-manifest repo when created.

**Provides:**
- Server registry
- Health specifications (planned)
- Quality standards
- Manifest schema

**Consumes:**
- chora-base: mcp_server_template, health_endpoint_template

**Can Handle:**
- Strategic: ecosystem expansion, standard changes
- Coordination: add server, update specs, modify gates
- Tasks: update manifest, add servers, update standards

---

## Creating a Capabilities File

### For a New Repo

1. **Copy template:**
   ```bash
   cp inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml.template \
      inbox/coordination/CAPABILITIES/your-repo.yaml
   ```

2. **Customize:**
   - Update `repo`, `description`
   - Define what you `provide`
   - List what you `consume`
   - Specify intake `capabilities`
   - Add `maintainers` and `contact` info

3. **Commit:**
   ```bash
   git add inbox/coordination/CAPABILITIES/your-repo.yaml
   git commit -m "feat(capabilities): Add your-repo capabilities"
   ```

---

## Using Capabilities for Task Routing

### Check if Repo Can Handle Task

```bash
# Can ecosystem-manifest handle coordination requests?
yq '.capabilities.can_receive[] | select(.type == "coordination")' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

# What categories of tasks can chora-base handle?
yq '.capabilities.can_receive[] | select(.type == "task") | .category[]' \
  inbox/coordination/CAPABILITIES/chora-base.yaml
```

### Verify Dependencies

```bash
# Does ecosystem-manifest depend on chora-base?
yq '.consumes[] | select(.repo == "chora-base")' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml

# Check version requirements
yq '.consumes[] | select(.repo == "chora-base") | .version' \
  inbox/coordination/CAPABILITIES/ecosystem-manifest.yaml
```

### Find Who Provides a Capability

```bash
# Who provides health endpoint templates?
for file in inbox/coordination/CAPABILITIES/*.yaml; do
  yq '.provides[] | select(.id == "health_endpoint_template") |
      {repo: .repo, version: .version}' "$file"
done
```

---

## Capability Discovery (Future)

In the future, repos could expose capabilities via MCP resources (following chora-compose pattern):

```python
# Future: MCP resource for capability discovery
await mcp_client.read_resource("capabilities://ecosystem-manifest")

# Returns:
{
  "repo": "ecosystem-manifest",
  "provides": [...],
  "consumes": [...],
  "can_receive": [...]
}
```

This would enable **dynamic capability discovery** without reading YAML files.

---

## Best Practices

### 1. **Keep Updated**
Update capabilities file when:
- Adding new features
- Changing APIs or contracts
- Adding/removing dependencies
- Changing maintainers

### 2. **Version Everything**
- Capability versions (semantic versioning)
- Dependency version constraints
- Capability file version (for schema evolution)

### 3. **Be Specific**
```yaml
# ❌ Vague
provides:
  - id: templates
    name: "Templates"

# ✅ Specific
provides:
  - id: mcp_server_template
    name: "MCP Server Template"
    description: "Production-ready MCP server with FastMCP, tests, docs"
    location: "static-template/templates/mcp-server/"
    version: "3.3.0"
```

### 4. **Document Consumers**
List who uses each capability - helps understand impact of changes:
```yaml
provides:
  - id: health_endpoint_template
    consumers:
      - ecosystem-manifest  # Uses for standards
      - mcp-orchestration  # Deploys servers using this
      - all MCP servers     # Implement using this template
```

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - How capabilities integrate with intake
- [chora-compose integration patterns](../../../inbox/chora-compose/integration-with-orchestration.md) - Capability discovery inspiration
