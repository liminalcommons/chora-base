---
title: mcp-orchestration Coordination Invitation
description: Personalized invitation for mcp-orchestration to join chora-workspace coordination hub
tags: [mcp-orchestration, invitation, coordination, onboarding]
diataxis_type: reference
author: Victor Piper / Liminal Commons
created: 2025-10-31
updated: 2025-10-31
status: active
---

# Invitation: mcp-orchestration → chora-workspace

**To**: mcp-orchestration Repository Stewards & Contributors
**From**: chora-workspace (Distributed Development Coordination Hub)
**Date**: 2025-10-31
**Subject**: Coordinate Your Dependencies - Unlock W3 Health Monitoring

---

## Why We're Reaching Out

**mcp-orchestration** sits at a **critical integration point** in the ecosystem:

**Your dependencies**:
- **Upstream**: ecosystem-manifest (server registry, health specs)
- **Upstream**: chora-base (templates, Docker patterns)

**Your consumers**:
- **Downstream**: mcp-gateway (queries health status)
- **Downstream**: Claude Desktop users (rely on auto-recovery)

**Your challenge**: How do you coordinate delivery when blocked by ecosystem-manifest (not yet created) and consumed by mcp-gateway (active development)?

**Our solution**: Inbox coordination protocol with dependency tracking, event traceability, and ecosystem dashboard.

---

## What mcp-orchestration Gains

### 1. Dependency Tracking & Blocker Visibility

**Your current challenge**:
- W3 Health Monitoring requires server registry from ecosystem-manifest
- ecosystem-manifest repository doesn't exist yet
- How do you know when it will? How do you communicate that you're blocked?

**What we offer**:
```yaml
# Your capability declaration shows blockers
mcp-orchestration:
  blockers:
    - type: dependency
      description: Awaits ecosystem-manifest server registry
      from_repo: ecosystem-manifest
      required_for: Auto-discovery feature (W3 health monitoring)
      impact: Blocks Sprint 3 (Week 5-8 in W3 timeline)
      priority: P1

# Ecosystem dashboard makes this visible to everyone
# ecosystem-manifest sees they're blocking you
# Leadership sees priority dependency
# You have clear signal when blocker resolves
```

**Value**: No more "when will X be ready?" emails. Dashboard shows real-time status of all dependencies.

### 2. Event Traceability Across Integration Points

**Your current challenge**:
- You integrate with ecosystem-manifest (reads registry), mcp-gateway (provides status), chora-base (uses templates)
- When integration fails, how do you trace root cause across repos?

**What we offer**:
```bash
# All W3 work uses trace_id: "ecosystem-w3-health-monitoring"

# Your events
{"event_type":"registry_read_failed","trace_id":"ecosystem-w3-health-monitoring",
 "details":{"error":"Schema version mismatch","registry_version":"0.9.0","expected":">=1.0.0"}}

# ecosystem-manifest's events
{"event_type":"registry_published","trace_id":"ecosystem-w3-health-monitoring",
 "details":{"version":"0.9.0","breaking_changes":true}}

# Query shows correlation
jq 'select(.trace_id=="ecosystem-w3-health-monitoring") |
    select(.timestamp > "2025-11-01" and .timestamp < "2025-11-02")' \
  */inbox/coordination/events.jsonl

# Result: Clear timeline showing registry published with breaking change
# → your integration failed due to version mismatch → coordination needed
```

**Value**: Cross-repo debugging in minutes (not hours of Slack threads), complete audit trail.

### 3. Coordinated Integration Testing

**Your current challenge**:
- mcp-gateway depends on your health status API
- How do you coordinate "we're ready for integration testing"?
- How do you handle "we found a bug in your API" feedback?

**What we offer** via coordination requests:

```json
{
  "type": "coordination",
  "request_id": "coord-005",
  "from_repo": "mcp-orchestration",
  "to_repo": "mcp-gateway",
  "title": "Health Status API Ready for Integration Testing",
  "deliverables": [
    "Health status API v1.0 deployed to test environment",
    "OpenAPI spec published with example responses",
    "Test data: 5 servers (3 healthy, 1 degraded, 1 down)",
    "Integration test script (validates mcp-gateway can query status)"
  ],
  "acceptance_criteria": [
    "mcp-gateway successfully queries status for all 5 test servers",
    "Response time <100ms for status queries",
    "Error handling works (graceful degradation if orchestration unavailable)"
  ],
  "timeline": "Ready for testing Week 10, feedback by Week 11"
}
```

**mcp-gateway's response**:
```json
{
  "status": "accepted",
  "assignee": "gateway-team",
  "estimated_effort": "4 hours",
  "test_completion_date": "2025-11-15",
  "feedback_event": "integration_test_complete"
}
```

**Value**: Clear handoffs, async coordination, no synchronization overhead (you don't wait idle while gateway tests).

### 4. Template & Pattern Reuse from chora-base

**Your current challenge**:
- chora-base has templates for Docker deployment, health checks, documentation
- How do you know what's available? Which templates are proven?

**What we offer**:

**Capability registry shows**:
```yaml
chora-base:
  provides:
    - capability: docker_deployment_template
      version: v3.3.0
      status: production_ready
      consumers: [mcp-orchestration]
      roi: 200-300% (2-3h saved per use)

    - capability: health_check_template
      version: v3.3.0
      status: production_ready
      consumers: [mcp-orchestration, mcp-gateway]
      roi: 150-250% (1-2h saved per use)
```

**Knowledge notes provide patterns**:
- `template-driven-development-efficiency.md` - How to maximize template ROI
- `zero-defect-prevention-patterns.md` - Prevent defects (not detect)
- `progressive-context-loading-strategy.md` - Reduce onboarding time 75-80%

**Value**: Don't reinvent the wheel - reuse proven templates with 200-300% ROI, learn from documented patterns.

---

## W3 Health Monitoring: Your Central Role

In W3, **mcp-orchestration is the core implementation**:

### Week 5-8: Your Primary Deliverable (coord-003)

**Request**: Implement health monitoring for MCP server lifecycle management

**Dependencies** (must be ready first):
- Week 3-4: chora-base health check template (coord-001)
- Week 3-4: ecosystem-manifest server registry (coord-002)

**Your deliverables**:
1. **Health monitoring service** (reads registry, polls servers, updates status)
2. **Auto-recovery logic** (restarts failed containers)
3. **Status API** (provides health data to mcp-gateway)
4. **Alerting integration** (notifies on persistent failures)

**Enables downstream**:
- Week 9-12: mcp-gateway health-aware routing (coord-004)
- Week 9-12: Integration testing across orchestration + gateway
- Week 13-16: Production rollout

**Coordination timeline**:
```
Week 3: ecosystem-manifest starts registry (you're not blocked)
Week 4: chora-base completes template (you can start using)
Week 5: You start implementation (dependencies met)
Week 6-7: Development with interim status updates
Week 8: Complete, signal to mcp-gateway "ready for integration"
Week 9-10: mcp-gateway integrates (you support their testing)
Week 11-12: Joint integration testing
Week 13-16: Coordinated production rollout
```

**Events you'll log** (trace_id: `ecosystem-w3-health-monitoring`):
- `health_monitoring_implementation_started` (Week 5)
- `registry_integration_complete` (Week 6)
- `auto_recovery_logic_complete` (Week 7)
- `status_api_deployed` (Week 8)
- `integration_test_passed` (Week 11)
- `production_rollout_complete` (Week 16)

**Our coordination support**:
- **Week 3**: Signal when ecosystem-manifest registry is ready
- **Week 4**: Signal when chora-base template is ready
- **Week 8**: Facilitate handoff to mcp-gateway for integration testing
- **Week 11**: Coordinate integration test across both teams
- **Week 13-16**: Coordinate release sequence (who deploys when)

---

## Success Pattern: How to Write Effective Coordination Requests

When you need something from another repo (or offer something to them):

### ✅ DO: Quantify the Dependency Impact

**Example**:
```json
{
  "blocker": "Awaiting ecosystem-manifest server registry",
  "impact": "Blocks auto-discovery feature (eliminates 15-20 min manual configuration per deployment)",
  "timeline": "Need registry by Week 4 to start Week 5 implementation (2-week sprint)",
  "workaround": "Can start health monitoring with hardcoded server list (technical debt to resolve later)"
}
```

### ✅ DO: Offer Integration Support

**Example**:
```json
{
  "deliverable": "Health status API v1.0",
  "support_offered": [
    "OpenAPI spec with example responses (15 min for mcp-gateway to understand API)",
    "Test environment with 5 sample servers (mcp-gateway can test immediately)",
    "Integration test script (validates mcp-gateway implementation)",
    "On-call support during integration week (Slack/GitHub, <2h response time)"
  ],
  "value": "Reduces mcp-gateway integration effort by ~40% (6h → 3.5h estimated)"
}
```

### ✅ DO: Propose Clear Acceptance Criteria

**Example**:
```json
{
  "acceptance_criteria": [
    "mcp-gateway successfully queries health status for ≥10 servers",
    "Response time <100ms at p95 (mcp-gateway has performance budget)",
    "Error handling graceful (if orchestration down, gateway shows cached status)",
    "Integration test passes (validates end-to-end health-aware routing)"
  ],
  "success_metrics": {
    "test_duration": "<4 hours for integration testing",
    "defects_found": "<2 issues (both resolved within 1 business day)",
    "coordination_overhead": "<30 min total (async via coordination requests)"
  }
}
```

**Result from COORD-003**: 70% acceptance, 0.5h response time, 50% acceleration through clear criteria.

---

## Pre-Filled Capability Template

We've created this based on your v0.2.0 scope and W3 planning:

```yaml
# File: inbox/coordination/CAPABILITIES/mcp-orchestration.yaml

repository:
  name: mcp-orchestration
  role: service_layer
  description: MCP server lifecycle management with health monitoring and auto-recovery
  version: v0.2.0 (in development)

provides:
  - capability: docker_lifecycle_management
    description: Deploy, monitor, and auto-recover MCP servers as Docker containers
    version: v0.2.0
    api: HTTP REST
    consumers: [mcp-gateway]
    documentation: docs/lifecycle-api.md

  - capability: health_monitoring
    description: Continuous health checks for all managed MCP servers
    version: v0.2.0 (W3 deliverable)
    api: WebSocket (real-time) + HTTP REST (polling)
    consumers: [mcp-gateway]
    documentation: docs/health-monitoring.md

  - capability: auto_recovery
    description: Automatic restart of failed containers with exponential backoff
    version: v0.2.0
    configuration: YAML
    consumers: [all_mcp_server_deployments]
    documentation: docs/auto-recovery.md

consumes:
  - capability: server_registry
    from_repo: ecosystem-manifest
    version: ">=1.0.0"
    purpose: Auto-discovery of MCP servers to manage
    criticality: P1 (blocks W3 health monitoring)

  - capability: health_check_template
    from_repo: chora-base
    version: ">=3.3.0"
    purpose: Standardized health check implementation
    criticality: P1 (W3 dependency)

  - capability: docker_deployment_template
    from_repo: chora-base
    version: ">=3.3.0"
    purpose: Container lifecycle patterns
    criticality: P2 (optimization, not blocker)

responsibilities:
  - Deploy MCP servers as Docker containers
  - Monitor health of all managed servers
  - Auto-recover failed servers (restart with backoff)
  - Provide real-time health status to mcp-gateway
  - Log lifecycle events for audit and debugging

current_status:
  state: in_development
  current_version: v0.2.0
  next_milestone: W3 Health Monitoring implementation (Week 5-8)
  estimated_completion: Q1 2026 (Week 16 of W3)

blockers:
  - type: dependency
    description: Awaits ecosystem-manifest server registry
    from_repo: ecosystem-manifest
    required_for: Auto-discovery feature (W3 coord-003)
    impact: Blocks Week 5-8 sprint (can't start until Week 4 delivery)
    priority: P1
    workaround: Can implement with hardcoded server list (technical debt)

  - type: dependency
    description: Awaits chora-base health check template
    from_repo: chora-base
    required_for: Standardized health monitoring (W3 coord-003)
    impact: Delays implementation by 1-2 days (can start without, but rework likely)
    priority: P2
    workaround: Implement custom health checks, migrate to template later

coordination_preferences:
  request_format: coordination_requests (JSON schema)
  response_sla: 1_business_day
  integration_testing: Test environment available, async coordination preferred
  event_logging: All major milestones logged with trace_id

contact:
  maintainers: [orchestration-team@liminalcommons.org]
  slack_channel: "#mcp-orchestration"
  github: "github.com/liminal-commons/mcp-orchestration"
```

**Action**: Review, adjust as needed, and we'll add to ecosystem capability registry.

---

## What We're Asking

### Minimal Commitment (1-2 hours)

**Step 1: Register Capabilities** (15 min)
- Review pre-filled template above
- Adjust current status, blockers, contact info
- Submit PR to chora-workspace

**Step 2: Adopt Inbox Protocol** (30 min)
- Create `inbox/` structure in mcp-orchestration
- Copy schemas from chora-workspace
- Document in README

**Step 3: Log Events for W3** (Ongoing, 30 sec per event)
- When W3 proceeds, log major milestones
- Use trace_id: `ecosystem-w3-health-monitoring`
- ~8-12 events over 12-week implementation

**Total**: 45 min upfront + 4-6 min over W3 timeline

### What You Get in Return

**Immediate**:
- Dashboard visibility of blockers (ecosystem-manifest status)
- Pre-filled capability template (5 min review vs 30 min creation)
- W3 coordination support (dependency signaling, integration coordination)

**During W3 (if it proceeds)**:
- Signals when dependencies ready (Week 3-4 completions)
- Integration coordination with mcp-gateway (Week 9-12)
- Event traceability for cross-repo debugging
- Access to chora-base templates (200-300% ROI)

**Ongoing**:
- Knowledge notes with proven patterns
- Ecosystem dashboard for all integration points
- Coordination request protocol (async, structured, 70% acceptance rate)

---

## Next Steps

### Option 1: Full Onboarding (Recommended for W3 Participants)

1. **Review capability template** (5 min)
2. **Register in ecosystem** (10 min PR submission)
3. **Adopt inbox protocol** (30 min setup)
4. **Join weekly broadcasts** (10 min/week, know when dependencies resolve)

**Timeline**: 45 min initial + 10 min/week

**Value**: Full W3 coordination support, dependency tracking, integration coordination

### Option 2: Capability Registry Only

1. **Submit capability declaration** (15 min with pre-filled template)
2. **Receive blocker notifications** when ecosystem-manifest ready
3. **Evaluate inbox adoption** when W3 proceeds

**Timeline**: 15 min one-time

**Value**: Blocker visibility, minimal commitment

### Option 3: Observer Mode

1. **Watch weekly broadcasts** (Sundays, 10 min/week)
2. **Monitor W3 progress** via ecosystem dashboard
3. **Decide later** based on W3 timeline

**Timeline**: 10 min/week, zero setup

**Value**: Stay informed, no commitment

---

## Why This Matters

### For mcp-orchestration

You're at a **critical integration point** with dependencies both upstream (ecosystem-manifest, chora-base) and downstream (mcp-gateway).

**Without coordination**:
- Email/Slack threads asking "when will registry be ready?"
- Integration surprises when mcp-gateway's assumptions don't match your API
- Cross-repo debugging via manual log correlation
- Blocked waiting with no visibility

**With coordination**:
- Dashboard shows dependency status real-time
- Coordination requests structure handoffs (clear acceptance criteria)
- Event traceability enables cross-repo debugging in minutes
- Async coordination (no synchronization overhead)

### For W3 Health Monitoring

You're **the core implementation** (Week 5-8). Coordination makes the difference between:
- ❌ **Without**: Blocked until Week 4, unclear when to start, integration chaos Week 9-12
- ✅ **With**: Clear signals Week 3-4, smooth start Week 5, coordinated integration Week 9-12

**Evidence from W3 example**: 47 events logged, 4 repos coordinated, 16-week timeline with clear dependencies.

### For the Ecosystem

Your participation **validates** that coordination works for complex integrations (multiple dependencies, async development, cross-repo testing).

---

## Questions?

### About Coordination

- Read: [ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md](../ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md)
- Review: W3 example (your role is coord-003) at `chora-base/inbox/examples/health-monitoring-w3/`
- Ask: File coordination request or email

### About W3 Timeline

- **When does W3 start?** Awaiting strategic approval (quarterly review)
- **What if ecosystem-manifest delays?** Capability registry tracks blocker, you can use workaround (hardcoded server list)
- **How firm is Week 5-8 timeline?** Flexible based on upstream delivery, dashboard shows real-time status

---

## Conclusion

**mcp-orchestration**, you're at the **center of W3 Health Monitoring** with critical dependencies and consumers.

**We're offering**:
- Dependency tracking (know when blockers resolve)
- Event traceability (cross-repo debugging in minutes)
- Integration coordination (structured handoffs with mcp-gateway)
- Pre-filled capability template (5 min review vs 30 min creation)

**We're asking**:
- 45 min onboarding (or 15 min capability-only, or 0 min observer mode)
- Event logging during W3 (30 sec per milestone, 8-12 events)
- Coordination request usage for integration needs

**The coordination workspace unblocks your dependencies and streamlines your integrations. Let's make W3 Health Monitoring a coordinated success.**

---

**Document**: mcp-orchestration-invitation.md
**Date**: 2025-10-31
**Author**: Victor Piper / Liminal Commons
**Trace ID**: `ecosystem-coordination-launch-2025-10-31`

**Attachments**:
- Pre-filled capability template (above)
- W3 timeline (your role: coord-003, Week 5-8)
- Coordination request success pattern

**Response requested by**: 2025-11-14 (2 weeks)
**Preferred response format**: Coordination request or email
