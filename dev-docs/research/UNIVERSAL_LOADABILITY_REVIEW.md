---
title: Universal Loadability Format Review
status: pending-spec
version: 0.1.0
created: 2025-10-24
last_updated: 2025-10-24
spec_source: mcp-gateway v1.2.0
review_target: Week 6 (Early Q1 2026)
---

# Universal Loadability Format Review

**Purpose:** Evaluate mcp-gateway's Universal Loadability Format specification for adoption in mcp-orchestration Wave 2.x.

**Status:** ⏳ Awaiting mcp-gateway v1.2.0 specification (Week 6)

**Coordination:** [MCP_GATEWAY_COORDINATION.md](../../project-docs/ecosystem/MCP_GATEWAY_COORDINATION.md)

---

## Review Framework

### Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Compatibility** | 30% | Alignment with existing capability manifest |
| **Ecosystem Benefit** | 25% | Cross-gateway compatibility value |
| **Implementation Effort** | 20% | Development + testing time required |
| **Maintenance Burden** | 15% | Ongoing support complexity |
| **Extensibility** | 10% | Ability to add mcp-orch specific metadata |

**Passing Score:** ≥70% weighted total

---

## Specification Overview

**Source:** mcp-gateway v1.2.0 (Expected: Weeks 5-6, Early Q1 2026)

**Format:** `mcp-server.json` manifest file

**Purpose:** Standardized discovery format for MCP servers across gateways, clients, and IDEs

### Example Structure (from integration briefing)

```json
{
  "name": "mcp-orchestration",
  "version": "2.0.0",
  "description": "MCP client configuration and server management",
  "author": "orchestration-team",
  "license": "MIT",
  "mcp": {
    "protocol_version": "2024-11-05",
    "transport": {
      "stdio": {
        "command": "uvx",
        "args": ["mcp-orchestration"]
      },
      "http": {
        "url": "http://localhost:8080",
        "auth": "bearer",
        "sse_endpoint": "/mcp/sse"
      }
    },
    "capabilities": {
      "tools": true,
      "resources": false,
      "prompts": false
    },
    "tools": [
      {
        "name": "list_available_servers",
        "description": "List all MCP servers in registry",
        "input_schema": {
          "type": "object",
          "properties": {
            "filter": {
              "type": "string",
              "description": "Optional filter pattern"
            }
          }
        }
      }
    ]
  }
}
```

---

## Comparison with Current Approach

### mcp-orchestration Capability Manifest (Current)

**Format:** YAML-based capability manifest
**Location:** Embedded in [ECOSYSTEM_INTEGRATION.md](./ECOSYSTEM_INTEGRATION.md#capability-manifest)

```yaml
id: mcp.orchestration
version: 0.1.3
owner: liminalcommons/mcp-orchestration
lifecycle_stage: operate
stability: stable

inputs:
  - name: client_id
    type: string
  - name: server_id
    type: string

outputs:
  - name: config_artifact
    type: object

dependencies:
  - name: fastmcp
    version: ">=0.5.0"

security_tier: moderate
adr_links:
  - dev-docs/vision/CAPABILITY_EVOLUTION.example.md

capabilities:
  - id: mcp.orchestration.client.list
    description: List supported MCP clients
    status: stable
    wave: 1.0

telemetry:
  signals:
    - name: mcp.orchestration.tool_usage
      type: counter
```

### Key Differences

| Aspect | Universal Loadability | Current Manifest | Assessment |
|--------|----------------------|------------------|------------|
| **Format** | JSON | YAML | ⚠️ Need conversion |
| **Focus** | MCP protocol discovery | Ecosystem capability tracking | ⚠️ Different purposes |
| **Tool Metadata** | Full input_schema | Capability IDs only | ✅ Loadability more detailed |
| **Transport Info** | Explicit stdio/http config | Not included | ✅ Loadability covers this |
| **Lifecycle** | N/A | lifecycle_stage, stability | ❌ Manifest richer |
| **Telemetry** | N/A | Telemetry signals | ❌ Manifest richer |
| **Security** | auth in transport | security_tier + controls | ⚠️ Different models |

---

## Evaluation (To Be Completed After Spec Review)

### Criterion 1: Compatibility (30%)

**Score:** _TBD after spec review_

**Questions:**
- [ ] Can we generate Universal Loadability from existing code?
- [ ] Do we lose information by converting manifest → loadability?
- [ ] Can we maintain both formats simultaneously?
- [ ] Are there conflicts in structure or semantics?

**Compatibility Options:**
1. **Full Replacement:** Drop YAML manifest, use only Universal Loadability
2. **Dual Format:** Maintain both, generate loadability from manifest
3. **Extension:** Add mcp-orch specific fields to Universal Loadability
4. **Parallel:** Keep separate for different purposes

**Preliminary Assessment:** _To be filled after spec review_

---

### Criterion 2: Ecosystem Benefit (25%)

**Score:** _TBD after spec review_

**Questions:**
- [ ] How many tools/clients will support Universal Loadability?
- [ ] Does this enable auto-discovery we couldn't do before?
- [ ] Will mcp-gateway actually use this for discovery?
- [ ] Are other MCP servers adopting this format?

**Expected Benefits:**
- ✅ Auto-discovery by mcp-gateway
- ✅ IDE integration (VS Code, etc.)
- ✅ Marketplace compatibility
- ✅ Reduced manual configuration

**Risks:**
- ❌ Low adoption if other servers don't implement
- ❌ Spec changes over time require updates

**Preliminary Assessment:** _To be filled after spec review_

---

### Criterion 3: Implementation Effort (20%)

**Score:** _TBD after spec review_

**Estimated Effort:**

**Option 1: Generation Tool**
```python
# src/mcp_orchestrator/loadability/generator.py

def generate_loadability_manifest() -> dict:
    """Generate Universal Loadability Format from MCP server introspection."""
    tools = mcp.list_tools()

    manifest = {
        "name": "mcp-orchestration",
        "version": __version__,
        # ... rest of structure
    }

    return manifest

# CLI command
@cli.command()
def generate_loadability():
    manifest = generate_loadability_manifest()
    with open("mcp-server.json", "w") as f:
        json.dump(manifest, f, indent=2)
```

**Estimated Time:** 1-2 days

**Option 2: Dual Maintenance**
- Generate loadability from capability manifest
- Automated tests to ensure sync
- CI validation

**Estimated Time:** 2-3 days

**Testing Requirements:**
- [ ] Loadability file validates against schema
- [ ] mcp-gateway can auto-discover from loadability file
- [ ] All tools listed correctly
- [ ] Transport info accurate

**Preliminary Assessment:** _To be filled after spec review_

---

### Criterion 4: Maintenance Burden (15%)

**Score:** _TBD after spec review_

**Ongoing Costs:**
- Update loadability file on every tool addition/change
- Keep in sync with MCP protocol version updates
- Monitor spec changes from mcp-gateway
- Validate against schema regularly

**Automation Opportunities:**
- [ ] Auto-generate in CI
- [ ] Validate in pre-commit hook
- [ ] Sync with capability manifest

**Maintenance Strategy:**
1. **Auto-Generation (Preferred):** Generate `mcp-server.json` from code on release
2. **Manual:** Update JSON file manually (error-prone)
3. **CI Validation:** Fail build if out of sync

**Preliminary Assessment:** _To be filled after spec review_

---

### Criterion 5: Extensibility (10%)

**Score:** _TBD after spec review_

**mcp-orchestration Specific Metadata:**
- Capability IDs (e.g., `mcp.orchestration.client.list`)
- Lifecycle stage (`operate`, `validate`, etc.)
- Security tier (`moderate`, `high`)
- Telemetry signals
- Change signal references
- ADR links

**Extension Options:**
1. **Top-level field:** Add `mcp_orchestration` object
   ```json
   {
     "name": "mcp-orchestration",
     "mcp": { /* Universal Loadability */ },
     "mcp_orchestration": {
       "capability_ids": [...],
       "security_tier": "moderate",
       "telemetry": {...}
     }
   }
   ```

2. **Tool-level metadata:** Add custom fields to each tool
   ```json
   {
     "tools": [
       {
         "name": "list_clients",
         "description": "...",
         "x-capability-id": "mcp.orchestration.client.list",
         "x-security": "moderate"
       }
     ]
   }
   ```

3. **Separate file:** Keep capability manifest separate, reference loadability file

**Preliminary Assessment:** _To be filled after spec review_

---

## Decision Framework

### Decision Matrix

| Criteria | Weight | Score (1-5) | Weighted | Notes |
|----------|--------|-------------|----------|-------|
| Compatibility | 30% | _TBD_ | _TBD_ | After spec review |
| Ecosystem Benefit | 25% | _TBD_ | _TBD_ | After spec review |
| Implementation Effort | 20% | _TBD_ | _TBD_ | After spec review |
| Maintenance Burden | 15% | _TBD_ | _TBD_ | After spec review |
| Extensibility | 10% | _TBD_ | _TBD_ | After spec review |
| **TOTAL** | **100%** | - | **_TBD_** | **Passing: ≥70%** |

### Decision Options

**Option A: Full Adoption**
- ✅ Adopt Universal Loadability as primary format
- ✅ Generate from code introspection
- ✅ Publish `mcp-server.json` with releases
- ✅ Maintain capability manifest separately for ecosystem tracking

**Option B: Dual Format (Recommended)**
- ✅ Keep YAML capability manifest as source of truth
- ✅ Generate Universal Loadability from manifest
- ✅ Automate generation in CI
- ✅ Best of both worlds

**Option C: Extension**
- ✅ Adopt Universal Loadability with mcp-orch extensions
- ✅ Propose extensions to mcp-gateway team
- ⚠️ Risk of non-standard format

**Option D: Reject**
- ❌ Do not adopt Universal Loadability
- ❌ Maintain only capability manifest
- ❌ Manual integration with mcp-gateway

**Preliminary Recommendation:** _To be determined after spec review_

---

## Review Process

### Timeline

| Week | Activity | Owner | Status |
|------|----------|-------|--------|
| **Week 1 (Oct 24)** | Create review template | mcp-orch | ✅ Complete |
| **Week 6 (Early Q1 2026)** | Receive v1.2.0 spec | mcp-gateway | ⏳ Pending |
| **Week 7** | Review specification | mcp-orch | 🔴 Not Started |
| **Week 7** | Complete evaluation matrix | mcp-orch | 🔴 Not Started |
| **Week 8** | Make adoption decision | mcp-orch | 🔴 Not Started |
| **Week 8** | Provide feedback to mcp-gateway | mcp-orch | 🔴 Not Started |
| **Wave 2.1** | Implement if adopted | mcp-orch | 🔴 Not Started |

### Review Checklist

**Upon receiving specification (Week 6):**
- [ ] Read complete specification document
- [ ] Review JSON schema (if provided)
- [ ] Examine example files
- [ ] Compare with capability manifest
- [ ] Complete evaluation matrix
- [ ] Score each criterion (1-5)
- [ ] Calculate weighted total
- [ ] Draft preliminary decision
- [ ] Identify questions for mcp-gateway team

**Decision Meeting (Week 8):**
- [ ] Review evaluation results
- [ ] Discuss trade-offs
- [ ] Make go/no-go decision
- [ ] Document rationale
- [ ] Update WAVE_2X_COORDINATION_PLAN.md
- [ ] Communicate decision to mcp-gateway team

---

## Questions for mcp-gateway Team

**To be asked during spec review:**

1. **Versioning:** How do you handle spec version changes?
2. **Extensions:** Are custom fields allowed? Naming convention?
3. **Validation:** Do you provide a JSON schema validator?
4. **Discovery:** How will mcp-gateway use this file in practice?
5. **Updates:** How often should we regenerate the file?
6. **Tooling:** Any code generators or validators available?
7. **Adoption:** Which other MCP servers are adopting this?
8. **Future:** Roadmap for Universal Loadability Format?

---

## Implementation Plan (If Adopted)

### Phase 1: Generator Implementation (Wave 2.1)

**Deliverables:**
- [ ] `src/mcp_orchestrator/loadability/generator.py`
- [ ] CLI command: `mcp-orchestration generate-loadability`
- [ ] Auto-generate in CI on release
- [ ] Publish `mcp-server.json` with PyPI package

**Testing:**
- [ ] Unit tests for generator
- [ ] Validation against JSON schema
- [ ] Integration test with mcp-gateway

### Phase 2: Documentation (Wave 2.1)

**Updates:**
- [ ] Add to user-docs/reference/
- [ ] Explain purpose and usage
- [ ] Document generation process
- [ ] Link from ECOSYSTEM_INTEGRATION.md

### Phase 3: Maintenance (Ongoing)

**Process:**
- [ ] Regenerate on every release
- [ ] CI validation (fail if out of sync)
- [ ] Monitor spec changes from mcp-gateway

---

## Success Criteria

**If adopted, success means:**
- ✅ mcp-gateway can auto-discover mcp-orchestration
- ✅ `mcp-server.json` validates against schema
- ✅ Generation automated in CI
- ✅ Zero manual maintenance required
- ✅ mcp-orchestration capabilities correctly advertised

---

## References

- **Integration Briefing:** [inbox/mcp-n8n(to be mcp-gateway)/integration-briefing-for-mcp-orchestration.md](../../inbox/mcp-n8n(to%20be%20mcp-gateway)/integration-briefing-for-mcp-orchestration.md)
- **Wave 2.x Plan:** [WAVE_2X_COORDINATION_PLAN.md](../../project-docs/WAVE_2X_COORDINATION_PLAN.md#wave-21-api-enhancements)
- **Coordination Tracker:** [MCP_GATEWAY_COORDINATION.md](../../project-docs/ecosystem/MCP_GATEWAY_COORDINATION.md#m3-universal-loadability-review)
- **Current Manifest:** [ECOSYSTEM_INTEGRATION.md#capability-manifest](./ECOSYSTEM_INTEGRATION.md#capability-manifest)

---

**Status:** ⏳ Awaiting mcp-gateway v1.2.0 specification
**Next Action:** Review spec when available (Week 6, Early Q1 2026)
**Owner:** mcp-orchestration team
**Reviewer:** mcp-gateway team (feedback loop)
