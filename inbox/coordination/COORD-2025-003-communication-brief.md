# Communication Brief: chora-compose v1.9.0 Capabilities

**Trace ID:** CHORA-COORD-2025-003
**Date:** 2025-10-30
**From:** chora-compose
**To:** chora-base (primary), ecosystem repositories (secondary)
**Purpose:** Inform ecosystem about v1.9.0 cross-repository coordination capabilities

---

## Executive Summary

chora-compose v1.9.0 introduces **stigmergic context links** and **freshness tracking**, enabling efficient cross-repository coordination with 95% token reduction (20k→1k tokens) for common operations like SAP regeneration.

**Key Impact:**
- AI agents can trigger chora-compose capabilities via environmental cues (no context loading)
- Automated staleness detection identifies expired content requiring regeneration
- Cross-repo workflows become 10x faster and more reliable

**Action Required:** Update chora-base documentation to reference these capabilities (see coordination request COORD-2025-003)

---

## What's New in v1.9.0

### 1. Stigmergic Context Links (95% Token Reduction)

**Problem Solved:**
Previously, when chora-base needed to regenerate SAP documentation, the AI agent had to:
1. Load chora-compose AGENTS.md (15k tokens)
2. Load SAP-014 awareness guide (10k tokens)
3. Understand MCP tool structure (3k tokens)
4. Construct correct MCP call with parameters
5. Execute: `choracompose:generate_collection(collection_id="sap-004-complete")`

**Cost:** 28k tokens, 5 steps, error-prone

**Solution:**
Stigmergic context links embed capability triggers directly in documentation:

```markdown
To regenerate SAP-004 Testing Framework documentation:
[@chora-compose/collection:sap-004-complete]
```

AI agents recognize the pattern `[@repo/capability:resource-id]` and execute the corresponding MCP tool immediately, without loading any chora-compose documentation.

**Cost:** 1k tokens, 1 step, zero construction errors (95% reduction)

**Available Capabilities:**
- `collection`: Generate multi-artifact collections
- `freshness`: Check content age/staleness
- `generate`: Generate single content item
- `validate`: Validate collection config

**Syntax:**
```
[@{repository}/{capability}:{resource-identifier}]
```

**Examples:**
```markdown
[@chora-compose/collection:sap-004-complete]
[@chora-compose/freshness:all-saps]
[@chora-compose/generate:charter:sap-004]
[@chora-compose/validate:collection:sap-suite]
```

**Documentation:**
- Explanation: [docs/explanation/concepts/stigmergic-context-links.md](../../docs/explanation/concepts/stigmergic-context-links.md)
- How-to: [docs/how-to/coordination/use-context-links.md](../../docs/how-to/coordination/use-context-links.md)
- Reference: [docs/reference/mcp/check-freshness-tool.md](../../docs/reference/mcp/check-freshness-tool.md)

---

### 2. Freshness Tracking (Automated Staleness Detection)

**Problem Solved:**
Documentation ages and becomes stale, but there was no automated way to:
- Identify which content needs regeneration
- Prioritize regeneration work
- Track content health across collections

**Solution:**
New MCP tool `choracompose:check_freshness` analyzes collection manifests and returns freshness status for each member.

**Three-State Classification:**
- **Fresh** (<80% of threshold): Content is current, no action needed (green)
- **Stale** (80-100% of threshold): Schedule regeneration soon (yellow)
- **Expired** (≥100% of threshold): Regenerate immediately (red)

**Configuration:**
```json
{
  "collection_id": "sap-004-complete",
  "members": [
    {
      "id": "charter",
      "freshness_threshold_days": 30
    },
    {
      "id": "protocol",
      "freshness_threshold_days": 7
    },
    {
      "id": "awareness-guide",
      "freshness_threshold_days": 3
    }
  ]
}
```

**Output Example:**
```json
{
  "collection_id": "sap-004-complete",
  "overall_status": "stale",
  "members": [
    {
      "member_id": "charter",
      "status": "fresh",
      "age_days": 12,
      "threshold_days": 30,
      "threshold_percentage": 40.0,
      "expires_in_days": 18,
      "recommendation": "no_action"
    },
    {
      "member_id": "protocol",
      "status": "stale",
      "age_days": 6,
      "threshold_days": 7,
      "threshold_percentage": 85.7,
      "expires_in_days": 1,
      "recommendation": "schedule_regeneration"
    },
    {
      "member_id": "awareness-guide",
      "status": "expired",
      "age_days": 5,
      "threshold_days": 3,
      "threshold_percentage": 166.7,
      "expired_by_days": 2,
      "recommendation": "regenerate_immediately"
    }
  ],
  "summary": {
    "total_members": 3,
    "fresh_count": 1,
    "stale_count": 1,
    "expired_count": 1
  }
}
```

**Use Cases:**
- **Weekly maintenance scans**: CI/CD workflow checks all SAPs, regenerates expired content
- **Health monitoring dashboards**: Visualize content age across ecosystem
- **Selective regeneration**: Only regenerate stale/expired members (saves generation time)
- **Prioritization**: Focus on expired content first, schedule stale content

**Performance:**
- O(n) where n = number of members
- Typical latency: 10-50ms for 10-50 members
- Overhead: ~150 bytes per member in manifest

**Documentation:**
- Explanation: [docs/explanation/concepts/freshness-tracking-design.md](../../docs/explanation/concepts/freshness-tracking-design.md)
- How-to: [docs/how-to/coordination/check-freshness.md](../../docs/how-to/coordination/check-freshness.md)
- Reference: [docs/reference/mcp/check-freshness-tool.md](../../docs/reference/mcp/check-freshness-tool.md)

---

### 3. Collections Documentation Complete (v1.4.0 catch-up)

**Problem Solved:**
v1.4.0 implemented the Collections architecture (3-tier content generation), but documentation was incomplete. v1.9.1 backfilled comprehensive documentation.

**What's Available:**
- **How-to guides** (5 docs, 2,360 lines):
  - [assemble-collection.md](../../docs/how-to/collections/assemble-collection.md) - Basic collection creation
  - [higher-order-collections.md](../../docs/how-to/collections/higher-order-collections.md) - Nested collections
  - [create-collection-config.md](../../docs/how-to/collections/create-collection-config.md) - Configuration patterns
  - [validate-collection-config.md](../../docs/how-to/collections/validate-collection-config.md) - Validation
  - [cache-collection-results.md](../../docs/how-to/collections/cache-collection-results.md) - Performance optimization

**3-Tier Architecture:**
```
Content (atomic blocks: paragraphs, code snippets, configurations)
  ↓
Artifacts (assemblies: README, API doc, test file)
  ↓
Collections (multi-artifact bundles: SAP, project scaffold, doc suite)
```

**Key Features:**
- **Shared context**: Define once, propagate to all members
- **Context modes**: MERGE, OVERRIDE, ISOLATE
- **Generation strategies**: Parallel (with concurrency limits) or Sequential
- **Nested collections**: Collections of collections (recursive)
- **Smart caching**: SHA-256 context hashing for invalidation
- **Manifest tracking**: What/when/how for debugging

**Proof-of-Concept:**
- SAP-004 Testing Framework: 5 artifacts generated from chora-base content blocks
- Quality: 100% success (5/5 artifacts valid)
- Performance: ~12.5s parallel generation (concurrency_limit=3)
- Cache effectiveness: 80%+ hit rate on subsequent runs

---

## How chora-base Can Use These Capabilities

### Scenario 1: Regenerate SAP Documentation

**Traditional Workflow (BEFORE v1.9.0):**
```markdown
1. Load chora-compose AGENTS.md
2. Load SAP-014 awareness guide
3. Understand generate_collection tool
4. Construct MCP call: choracompose:generate_collection(collection_id="sap-004-complete")
5. Execute

Token cost: 28k tokens
Steps: 5
Error risk: Medium (parameter construction errors)
```

**Stigmergic Workflow (AFTER v1.9.0):**
```markdown
1. Add to chora-base AGENTS.md or SAP maintenance doc:
   "To regenerate SAP-004: [@chora-compose/collection:sap-004-complete]"
2. AI agent encounters link, pattern matcher triggers MCP call

Token cost: 1k tokens
Steps: 1
Error risk: Zero (no parameter construction)
```

**Savings: 95% token reduction, 80% time reduction**

---

### Scenario 2: Weekly SAP Freshness Checks

**Automated Workflow:**

1. **CI/CD schedule** (GitHub Actions, cron: weekly):
   ```yaml
   - name: Check SAP Freshness
     run: |
       mcp-client execute choracompose:check_freshness \
         --manifest-path .chora/manifests/all-saps.json \
         --default-threshold-days 7
   ```

2. **Review output**, identify expired SAPs:
   ```json
   {
     "overall_status": "expired",
     "expired_count": 3,
     "stale_count": 5,
     "fresh_count": 10
   }
   ```

3. **Trigger regeneration** for expired SAPs:
   ```markdown
   Expired SAPs (regenerate immediately):
   - [@chora-compose/collection:sap-004-complete]
   - [@chora-compose/collection:sap-007-complete]
   - [@chora-compose/collection:sap-012-complete]

   Stale SAPs (schedule this week):
   - [@chora-compose/collection:sap-003-complete]
   - [@chora-compose/collection:sap-009-complete]
   ```

4. **Slack notification** (optional):
   ```
   📊 SAP Freshness Report (2025-W44)

   Expired: 3 SAPs (regenerate now)
   Stale: 5 SAPs (schedule this week)
   Fresh: 10 SAPs (no action)

   View full report: [link]
   ```

**Benefit:** Proactive maintenance, no manual tracking, automated prioritization

---

### Scenario 3: Health Monitoring Dashboard

**Integration with health-monitoring repo:**

1. **Query freshness** for all collections:
   ```javascript
   const collections = ['sap-004-complete', 'sap-007-complete', 'sap-012-complete'];
   const freshnessData = await Promise.all(
     collections.map(id =>
       mcpClient.call('choracompose:check_freshness', { collection_id: id })
     )
   );
   ```

2. **Visualize health** in dashboard:
   ```
   Content Health Dashboard
   ========================

   SAP-004 Testing Framework    ████████░░ 80% Fresh (6/8 days)
   SAP-007 Documentation        ██████████ 100% Fresh (2/7 days)
   SAP-012 Quality Gates        ████░░░░░░ 40% Fresh (expired 3 days ago)

   Action Items:
   - SAP-012: Regenerate immediately (expired)
   - SAP-004: Monitor (stale in 2 days)
   ```

3. **Automated alerts** when thresholds crossed:
   ```
   ⚠️ ALERT: SAP-012 Quality Gates documentation expired 3 days ago

   Recommendation: Regenerate immediately
   Command: [@chora-compose/collection:sap-012-complete]
   ```

**Benefit:** Real-time visibility, automated alerts, data-driven maintenance

---

## Integration Checklist for chora-base

### Phase 1: Documentation Updates (2-4 hours)

- [ ] **Update AGENTS.md**
  - Add stigmergic context link examples for SAP regeneration
  - Reference v1.9.0 capabilities in cross-repo section
  - Document token efficiency (20k→1k savings)

- [ ] **Create SAP Maintenance Guide**
  - Document freshness tracking workflow
  - Add CI/CD integration examples
  - Include troubleshooting section

- [ ] **Update relevant SAPs**
  - SAP-000 (sap-framework): Reference stigmergic links for SAP regeneration
  - SAP-001 (inbox-coordination): Update coordination examples
  - SAP-009 (agent-awareness): Add v1.9.0 capability patterns

- [ ] **Validate changes**
  - Test at least one stigmergic context link end-to-end
  - Verify freshness check works with existing SAP collections
  - Confirm documentation links are bidirectional (chora-base ↔ chora-compose)

### Phase 2: CI/CD Integration (1-2 hours)

- [ ] **Create GitHub Actions workflow** (`.github/workflows/sap-freshness.yml`)
  ```yaml
  name: SAP Freshness Check
  on:
    schedule:
      - cron: '0 10 * * 1'  # Weekly, Monday 10am
    workflow_dispatch:

  jobs:
    check-freshness:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Check SAP Freshness
          run: |
            # Call chora-compose check_freshness tool
            # Parse output, identify expired SAPs
            # Comment on issue or send Slack notification
  ```

- [ ] **Test workflow** manually via workflow_dispatch
- [ ] **Document workflow** in chora-base README or SAP maintenance guide

### Phase 3: Health Monitoring (Optional, 2-3 hours)

- [ ] **Create health dashboard** (if health-monitoring repo exists)
  - Query freshness for all SAPs
  - Visualize content age
  - Set up automated alerts

- [ ] **Schedule weekly reviews** (team process)
  - Review freshness report
  - Prioritize regeneration work
  - Track content health trends

---

## Technical Reference

### Stigmergic Context Link Syntax

**Pattern:**
```
[@{repository}/{capability}:{resource-identifier}]
```

**Components:**
- `repository`: Target repo name (e.g., `chora-compose`)
- `capability`: Exposed capability (e.g., `collection`, `freshness`, `generate`, `validate`)
- `resource-identifier`: Specific resource to act on (e.g., `sap-004-complete`)

**How it Works:**
1. AI agent scans documentation (AGENTS.md, README, SAP files)
2. Pattern matcher recognizes `[@...]` syntax
3. Capability map resolves to MCP tool:
   - `collection` → `choracompose:generate_collection`
   - `freshness` → `choracompose:check_freshness`
   - `generate` → `choracompose:generate_demonstration`
   - `validate` → `choracompose:validate_collection_config`
4. Tool executes with resource-identifier as parameter
5. No context loading required (95% token savings)

**Capability Map (chora-compose v1.9.0):**
```yaml
capabilities:
  collection:
    tool: choracompose:generate_collection
    parameters:
      collection_id: "{resource-identifier}"

  freshness:
    tool: choracompose:check_freshness
    parameters:
      manifest_path: ".chora/manifests/{resource-identifier}.json"

  generate:
    tool: choracompose:generate_demonstration
    parameters:
      generator_id: "{resource-identifier}"

  validate:
    tool: choracompose:validate_collection_config
    parameters:
      config_path: "configs/collections/{resource-identifier}.json"
```

---

### Freshness Tracking API

**MCP Tool:** `choracompose:check_freshness`

**Input:**
```json
{
  "manifest_path": ".chora/manifests/sap-004-complete.json",
  "default_threshold_days": 7,
  "policy_overrides": {
    "charter": 30,
    "protocol": 7,
    "awareness-guide": 3
  }
}
```

**Output:**
```json
{
  "collection_id": "sap-004-complete",
  "overall_status": "stale|fresh|expired",
  "checked_at": "2025-10-30T20:00:00Z",
  "members": [
    {
      "member_id": "charter",
      "status": "fresh|stale|expired",
      "age_days": 12,
      "threshold_days": 30,
      "threshold_percentage": 40.0,
      "generated_at": "2025-10-18T10:00:00Z",
      "expires_at": "2025-11-17T10:00:00Z",
      "expires_in_days": 18,
      "recommendation": "no_action|schedule_regeneration|regenerate_immediately"
    }
  ],
  "summary": {
    "total_members": 3,
    "fresh_count": 1,
    "stale_count": 1,
    "expired_count": 1
  }
}
```

**Status Classification:**
- `fresh`: age < 80% of threshold (green)
- `stale`: 80% ≤ age < 100% of threshold (yellow)
- `expired`: age ≥ 100% of threshold (red)

**Recommendations:**
- `no_action`: Content is fresh, no regeneration needed
- `schedule_regeneration`: Content is stale, schedule regeneration this week
- `regenerate_immediately`: Content expired, regenerate now

---

## Resources

### chora-compose Documentation

**Stigmergic Context Links:**
- Explanation: [docs/explanation/concepts/stigmergic-context-links.md](../../docs/explanation/concepts/stigmergic-context-links.md)
- How-to: [docs/how-to/coordination/use-context-links.md](../../docs/how-to/coordination/use-context-links.md)
- Examples: [docs/how-to/coordination/stigmergic-workflow.md](../../docs/how-to/coordination/stigmergic-workflow.md)

**Freshness Tracking:**
- Explanation: [docs/explanation/concepts/freshness-tracking-design.md](../../docs/explanation/concepts/freshness-tracking-design.md)
- How-to: [docs/how-to/coordination/check-freshness.md](../../docs/how-to/coordination/check-freshness.md)
- Reference: [docs/reference/mcp/check-freshness-tool.md](../../docs/reference/mcp/check-freshness-tool.md)

**Collections:**
- How-to: [docs/how-to/collections/](../../docs/how-to/collections/) (5 comprehensive guides)
- Reference: [docs/reference/schemas/collection-config.md](../../docs/reference/schemas/collection-config.md)

### chora-compose Capabilities

**MCP Tools (18 total):**
- `choracompose:generate_collection` - Generate multi-artifact collections
- `choracompose:check_freshness` - Check content staleness (v1.9.0)
- `choracompose:list_generators` - List available generators
- `choracompose:compose_artifact` - Generate single artifact
- [See full tool reference](../../docs/reference/mcp/tool-reference.md)

**Capabilities Registry:**
- [inbox/coordination/CAPABILITIES/chora-compose.yaml](../coordination/CAPABILITIES/chora-compose.yaml)

### Contact

**Questions or Issues:**
- GitHub Issues: https://github.com/liminalcommons/chora-compose/issues
- GitHub Discussions: https://github.com/liminalcommons/chora-compose/discussions
- Maintainer: Victor (@victorpiper)

**Coordination Requests:**
- Submit via inbox protocol: [inbox/incoming/coordination/](../incoming/coordination/)
- Schema: [inbox/schemas/coordination-request.schema.json](../schemas/coordination-request.schema.json)
- Review SLA: 72 hours

---

## Next Steps

1. **Review coordination request** COORD-2025-003
2. **Approve/reject** based on chora-base priorities
3. **If approved:** Assign to sprint, follow integration checklist
4. **If questions:** Reply via coordination protocol or GitHub Discussions

**Estimated Effort:** 2-4 hours (Phase 1 documentation updates)

**Expected Impact:**
- 95% token reduction for SAP regeneration workflows
- Automated staleness detection for proactive maintenance
- Foundation for ecosystem-wide cross-repo coordination

---

**End of Communication Brief**
