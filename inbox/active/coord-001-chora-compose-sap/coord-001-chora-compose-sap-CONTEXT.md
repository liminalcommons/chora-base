# Coordination Request Context: chora-compose SAPs

**Request ID**: coord-001
**Created**: 2025-10-28
**For**: Wave 2 Execution Conversation
**From**: Strategic Planning Conversation

---

## Executive Summary

Create two SAPs (SAP-017 and SAP-018) to enable ecosystem repos to discover, adopt, and skillfully use chora-compose as a content generation capability. This demonstrates inbox protocol for cross-conversation coordination and establishes chora-compose as a first-class ecosystem capability with multiple access modalities.

---

## Background: How We Got Here

### The Strategic Conversation

**Topic**: "How can we use chora-compose as a 'second brain' capability broker to enable agents across the ecosystem to access capabilities via pip, SAP, MCP, or API?"

**Key Insights Discovered**:

1. **Chora-compose is architecturally perfect for this role** because:
   - Config-driven (capabilities can be defined as configs)
   - MCP discovery built-in (`capabilities://` resources)
   - Observable (events track all operations)
   - Composable (atomic capabilities assemble into workflows)
   - Self-documenting (uses itself to generate docs)

2. **Chora-base should contain SAPs** that teach agents how to acquire skilled awareness of chora-compose, enabling ecosystem repos to "just know when and how to use chora-compose skillfully in the context of their own role"

3. **Four access modalities** enable different use cases:
   - **pip**: Python library for programmatic access
   - **SAP**: Documentation/process-based adoption
   - **MCP**: AI agent tools (17 tools)
   - **API**: REST/HTTP gateway

---

## Research Conducted

### Chora-Compose Documentation Analysis

**Scope**: 113 markdown files in `docs/reference/ecosystem/chora-compose/user-docs`

**Key Findings**:

#### 1. Core Architecture (Config-Driven)
- **Layer 1**: JSON schemas define structure/validation
- **Layer 2**: Configs are data (content.json, artifact.json)
- **Layer 3**: Code is generic processors (ConfigLoader, Generator, Composer)
- **Benefit**: Configs are first-class, code is infrastructure

#### 2. MCP Integration (17 Tools + 5 Resources)

**MCP Tools**:
- `generate_content` - Generate from config
- `assemble_artifact` - Compose final output
- `batch_generate` - Parallel generation
- `draft_config` - Conversational config creation
- `test_config` - Preview config output
- `validate_content` - Validate configs
- `list_generators` - Discover available generators
- [10 more tools...]

**MCP Resources**:
- `capabilities://server` - Server metadata, features, limits
- `capabilities://tools` - Tool inventory with schemas
- `capabilities://generators` - Generator registry
- `capabilities://resources` - Resource URI catalog
- `capabilities://ecosystem` (future) - Cross-repo capability registry

#### 3. Observable Architecture
- JSONL event telemetry (`var/telemetry/events.jsonl`)
- Trace context propagation (`CHORA_TRACE_ID`)
- Duration metrics for all operations
- Event-driven observability

#### 4. Position in AI Tooling Ecosystem
- **Layer 1+ Primitive**: Specialized service (not orchestrator)
- **Orchestration Layer**: n8n, Zapier (above chora-compose)
- **MCP-Native**: First-class Model Context Protocol support
- **Composable**: Content → Artifacts assembly pattern

---

## Decision Matrix

User provided answers to 7 key questions:

### 1. SAP ID Assignment
**Answer**: Not specified, but SAP-003, SAP-004, SAP-008 already assigned
**Decision**: Use **SAP-017** and **SAP-018** (next available)

### 2. Scope
**Answer**: **C** - Two separate SAPs:
- **SAP-017**: `chora-compose-integration` (how to use it in your repo)
- **SAP-018**: `chora-compose-meta` (complete protocol, mirrors chora-base-meta pattern)

**Rationale**: Separates "how to use" from "what it is", follows SAP-002 pattern

### 3. Location Strategy
**Answer**: **C** - Both places:
- chora-base has integration SAP (how ecosystem repos adopt it)
- chora-compose repo has meta SAP (source of truth, self-documentation)

### 4. Adoption Prerequisites
**Answer**: **A** - Agent already has chora-base adopted (builds on SAP-000, SAP-001)

### 5. Real vs Aspirational
**Answer**: **C** - Current state + clear roadmap section for future capabilities

**Future capabilities to mark as roadmap**:
- Ecosystem capability registry
- `find_capability()` MCP tool
- `install_capability()` MCP tool
- `capabilities://ecosystem` resource
- Multi-repo capability broker features

### 6. File Creation Approach
**Answer**: **A** - Create files directly in chora-base, ready to commit

### 7. Capability Broker Features
**Answer**: **B** - "Future Capabilities" section (clearly marked as roadmap)

---

## SAP Content Structure

### SAP-017: chora-compose-integration

**Purpose**: Enable repos to adopt chora-compose for their content generation needs

**Target Audience**:
- MCP server developers (need tool documentation)
- Application developers (need API docs, README generation)
- Platform engineers (need audit reports, dashboards)

**Key Content**:

#### capability-charter.md
```markdown
# What This Capability Provides
- Configuration-driven content generation
- MCP tools for AI agent integration
- Composable artifact assembly
- Observable generation workflows

# When To Adopt This Capability
Your repo SHOULD adopt chora-compose if:
- ✅ You generate documentation (README, API docs, release notes)
- ✅ You want AI agents to help with content generation
- ✅ You need version-controlled content configs
- ✅ You want observable content generation (event telemetry)

# Role-Based Adoption
## For MCP Server Repos
Use chora-compose to: Generate tool documentation, schema files, example configs

## For Application Repos
Use chora-compose to: Generate API documentation, user guides, release notes

## For Platform Repos
Use chora-compose to: Generate reports, dashboards, audit logs
```

#### protocol-spec.md
```markdown
# Core Concepts
1. Content Configs - JSON defining individual content pieces
2. Artifact Configs - JSON assembling content into outputs
3. MCP Tools - 17 tools for AI agents
4. Capability Discovery - Resources for introspection

# Access Methods
## Method 1: Python Library (pip)
pip install chora-compose
from chora_compose import ArtifactComposer

## Method 2: MCP Tools (for AI agents)
await mcp_client.call_tool("generate_content", {
    "content_config_id": "api-docs"
})

## Method 3: CLI
poetry run chora-compose compose artifact-id

## Method 4: HTTP Gateway
POST http://localhost:8000/mcp/tools/generate_content

# Observability
All operations emit events to var/telemetry/events.jsonl with trace_id
```

#### awareness-guide.md
```markdown
# For AI Agents Working in Ecosystem Repos

## Quick Reference
- Generate documentation: mcp_client.call_tool("generate_content", ...)
- Discover capabilities: mcp_client.read_resource("capabilities://server")
- Create config conversationally: mcp_client.call_tool("draft_config", ...)

## Role-Based Usage Patterns
[Detailed patterns for MCP server dev, app dev, platform engineer]

## Decision: When to Use chora-compose
Use chora-compose when:
- ✅ Content is structured (follows template)
- ✅ Content changes frequently
- ✅ Multiple similar outputs needed
- ✅ AI agent should generate
- ✅ Need observability

Don't use when:
- ❌ One-off manual content
- ❌ Highly creative content
- ❌ Content already written

## Integration Workflow
1. Install: pip install chora-compose
2. Create configs: Use draft_config tool conversationally
3. Generate: call generate_content tool
4. Add to CI/CD (optional)

## Context Loading Strategy
Essential (load first): ~5k tokens
- This awareness guide
- chora-compose README
- MCP tool reference

Extended (if needed): ~15k tokens
- Config schema docs
- Generator selection guide
```

#### adoption-blueprint.md
```markdown
# Phase 1: Installation (30 min)
1. pip install chora-compose
2. Create directory structure (configs/, templates/, var/telemetry/)
3. Verification

# Phase 2: First Config (1 hour)
1. Create content config (via MCP draft_config tool)
2. Create artifact config
3. Generate content

# Phase 3: MCP Integration (30 min)
1. Configure MCP server in Claude Desktop config
2. Test MCP connection
3. Test content generation via MCP

# Phase 4: CI/CD Integration (1 hour)
1. Create GitHub Action
2. Test workflow

# Phase 5: Update Ecosystem Coordination (30 min)
1. Declare capability in CAPABILITIES.yaml
2. Update AGENTS.md with chora-compose section

# Verification Checklist
- [ ] chora-compose installed
- [ ] Directory structure created
- [ ] At least one config exists
- [ ] Can generate content
- [ ] MCP server configured (if using)
- [ ] CI/CD workflow added (optional)
- [ ] CAPABILITIES.yaml updated
- [ ] AGENTS.md updated
```

### SAP-018: chora-compose-meta

**Purpose**: Complete protocol specification for chora-compose (mirrors SAP-002 pattern)

**Target Audience**:
- Chora-compose maintainers
- Advanced users extending chora-compose
- Ecosystem architects
- Anyone needing deep understanding

**Key Content**:

#### capability-charter.md
```markdown
# Chora-Compose: Config-Driven Content Generation Framework

## Strategic Value
- Universal content generation language for ecosystem
- MCP-native AI agent integration
- Observable content pipelines
- Composable capability building blocks

## Scope
- Config-driven architecture (schemas, configs, code)
- 17 MCP tools + 5 resource families
- Generator strategy pattern (Jinja2, BDD, CodeGen, AI)
- Event telemetry and trace correlation

## Position in Ecosystem
Layer 1+ Primitive (not orchestration layer)
Invoked by: n8n, Zapier, GitHub Actions, Claude Desktop, Cursor
Integrates with: chora-base, mcp-orchestration, health-service

## Future Vision
- Capability broker for ecosystem
- Multi-modal access (pip/SAP/MCP/API)
- Cross-repo capability registry
- Dynamic capability discovery
```

#### protocol-spec.md
```markdown
# Complete Architecture Specification

## Layer 1: Schemas (The Contract)
JSON Schemas define structure:
- content/v3.1/schema.json
- artifact/v3.1/schema.json
- [Complete schema documentation]

## Layer 2: Configs (The Data)
Configs are instances conforming to schemas:
- Content configs (elements, generation patterns)
- Artifact configs (composition, outputs)

## Layer 3: Code (The Processors)
Generic, reusable processors:
- ConfigLoader (validates, loads configs)
- Generator (executes generation strategies)
- Composer (assembles artifacts)

## MCP Tools (17 tools)
[Complete tool reference with schemas]

## MCP Resources (5 families)
[Complete resource documentation]

## Observability Architecture
- JSONL event log (var/telemetry/events.jsonl)
- Trace context (CHORA_TRACE_ID env var)
- Event schema v1.0
- Cross-system trace correlation

## Generator Strategy Pattern
- Demonstration (example_output-based)
- Jinja2 (template-based)
- BDD (Gherkin scenario-based)
- CodeGen (code generation)
- AI (LLM-based, future)

## Access Modalities
1. pip: Python library (ArtifactComposer API)
2. MCP: 17 tools for AI agents
3. CLI: chora-compose command
4. API: HTTP gateway (wraps MCP)
```

#### awareness-guide.md
```markdown
# For Maintainers and Advanced Users

## Architecture Mental Model
Think of chora-compose as:
- Language: Configs are DSL for content generation
- Compiler: Code transforms configs → content
- Runtime: MCP server provides execution environment
- Observable: Events provide introspection

## Extension Points
1. Custom Generators (implement GeneratorStrategy)
2. Custom Resources (add MCP resources)
3. Custom Tools (add MCP tools)
4. Custom Schemas (extend config schemas)

## Integration Patterns
[Detailed patterns for ecosystem integration]

## Future Capabilities (Roadmap)
### Capability Broker Features (Target: v4.1)
- Ecosystem capability registry
- find_capability() MCP tool
- install_capability() MCP tool
- capabilities://ecosystem resource
- Cross-repo capability discovery

[Mark clearly as NOT current state]
```

---

## Implementation Guidance

### For Wave 2 Execution Agent

**When you see this coordination request in inbox**:

1. **Read these files**:
   - `coord-001-chora-compose-sap.json` (this is the contract)
   - `coord-001-chora-compose-sap-CONTEXT.md` (this is the background)
   - `coord-001-chora-compose-sap-RATIONALE.md` (this is the why)

2. **Validate alignment**:
   - Does this fit Wave 2 goals? **Yes** - SAP content audit & enhancement
   - Is this the right time? **Yes** - Wave 2 Phase 2 is active
   - Do we have bandwidth? **Yes** - can parallelize with other SAP audits

3. **Accept the work**:
   ```bash
   mkdir inbox/active/coord-001-chora-compose-sap
   mv inbox/incoming/coordination/coord-001-* inbox/active/coord-001-chora-compose-sap/
   ```

4. **Execute deliverables**:

   **For SAP-017 (chora-compose-integration)**:
   ```bash
   mkdir -p docs/skilled-awareness/chora-compose-integration

   # Create 5 artifacts using templates from SAP-000
   # Reference: docs/skilled-awareness/document-templates.md
   # Pattern: docs/skilled-awareness/chora-base (SAP-002 integration pattern)

   # 1. capability-charter.md (use CONTEXT.md structure above)
   # 2. protocol-spec.md (document 4 access methods)
   # 3. awareness-guide.md (for AI agents, role-based patterns)
   # 4. adoption-blueprint.md (5-phase installation)
   # 5. ledger.md (track adoptions)
   ```

   **For SAP-018 (chora-compose-meta)**:
   ```bash
   mkdir -p docs/skilled-awareness/chora-compose-meta

   # Create 5 artifacts using SAP-002 as pattern
   # Reference: docs/skilled-awareness/chora-base (complete meta pattern)

   # 1. capability-charter.md (strategic value, scope, vision)
   # 2. protocol-spec.md (complete architecture, 17 tools, 5 resources)
   # 3. awareness-guide.md (for maintainers, extension points)
   # 4. adoption-blueprint.md (for chora-compose repo itself)
   # 5. ledger.md (track meta-adoption)
   ```

   **Update INDEX.md**:
   ```markdown
   | SAP-017 | chora-compose-integration | 1.0.0 | Draft | Extension | docs/skilled-awareness/chora-compose-integration/ | SAP-000 |
   | SAP-018 | chora-compose-meta | 1.0.0 | Draft | Extension | docs/skilled-awareness/chora-compose-meta/ | SAP-000, SAP-017 |
   ```

5. **Validate**:
   ```bash
   # Run link validation
   ./scripts/validate-links.sh docs/skilled-awareness/chora-compose-integration/
   ./scripts/validate-links.sh docs/skilled-awareness/chora-compose-meta/

   # Verify all 5 artifacts exist for each SAP
   ls docs/skilled-awareness/chora-compose-integration/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md
   ls docs/skilled-awareness/chora-compose-meta/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md
   ```

6. **Complete**:
   ```bash
   # Move to completed
   mv inbox/active/coord-001-chora-compose-sap inbox/completed/

   # Emit completion event
   echo '{"event_type": "coordination_completed", "request_id": "coord-001", "trace_id": "chora-compose-sap-creation-2025-10-28", "timestamp": "'$(date -Iseconds)'", "deliverables": ["SAP-017", "SAP-018"], "status": "success"}' >> inbox/coordination/events.jsonl
   ```

---

## Reference Material

### Source Documentation
- **Primary**: `docs/reference/ecosystem/chora-compose/user-docs/` (113 files)
- **Architecture**: `docs/reference/ecosystem/chora-compose/user-docs/explanation/architecture/config-driven-architecture.md`
- **MCP Tools**: `docs/reference/ecosystem/chora-compose/user-docs/reference/mcp/tool-reference.md`
- **Capabilities**: `docs/reference/ecosystem/chora-compose/user-docs/reference/api/resources/capabilities.md`
- **Integration**: `docs/reference/ecosystem/chora-compose/user-docs/explanation/ecosystem/agent-integration-playbook.md`

### Pattern References
- **SAP-002**: `docs/skilled-awareness/chora-base/` (meta pattern to follow for SAP-018)
- **SAP-000**: `docs/skilled-awareness/sap-framework/` (SAP structure, templates)
- **SAP-004**: `docs/skilled-awareness/testing-framework/` (good example of integration SAP)

### Tools
- **Link Validation**: `scripts/validate-links.sh` (SAP-016)
- **Templates**: `docs/skilled-awareness/document-templates.md` (SAP artifact templates)
- **INDEX**: `docs/skilled-awareness/INDEX.md` (add entries here)

---

## Success Indicators

You'll know you succeeded when:

1. ✅ Both SAPs have all 5 artifacts
2. ✅ Link validation passes (no broken references)
3. ✅ Both SAPs reference actual chora-compose docs (not hypothetical files)
4. ✅ SAP-017 provides clear decision framework ("when to use chora-compose")
5. ✅ SAP-018 documents complete architecture (17 tools, 5 resources, 4 access modes)
6. ✅ Future capabilities clearly marked as roadmap
7. ✅ INDEX.md shows SAP-017 and SAP-018 as "Draft"
8. ✅ Can demonstrate cross-conversation coordination (meta-goal achieved)
9. ✅ Any ecosystem repo could now install SAP-017 and skillfully use chora-compose

---

## Questions?

If you need clarification:
1. Check `coord-001-chora-compose-sap-RATIONALE.md` for the "why"
2. Reference SAP-002 (chora-base-meta) for meta SAP pattern
3. Reference SAP-004 (testing-framework) for integration SAP pattern
4. Use source material in `docs/reference/ecosystem/chora-compose/user-docs/`

---

**Document Version**: 1.0
**Created**: 2025-10-28
**Author**: Claude Code (Strategic Planning)
**For**: Claude Code (Wave 2 Execution)
**Status**: Ready for execution
