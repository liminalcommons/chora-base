# Outgoing Coordination Requests

This directory contains coordination requests sent FROM mcp-orchestration TO other repositories in the Liminal Commons ecosystem.

---

## Active Coordination Requests

### COORD-2025-004: Ecosystem Coordination Full Onboarding

**Status:** Submitted
**Priority:** High
**Created:** 2025-10-31
**Target Repo:** chora-workspace (ecosystem coordination hub)
**Response Deadline:** 2025-11-14

**Summary:**
mcp-orchestration accepts Full Onboarding to ecosystem coordination hub with conditional W3 Health Monitoring participation.

**Files:**
- [COORD-2025-004-ecosystem-onboarding.json](coordination/COORD-2025-004-ecosystem-onboarding.json) - Formal coordination request
- [COORD-2025-004-communication-brief.md](coordination/COORD-2025-004-communication-brief.md) - Comprehensive 20k+ word brief

**Key Points:**
- ✅ Accept Full Onboarding (45 min + 10 min/week)
- ⏸️ W3 participation conditional on Wave 2.0 completion + ecosystem-manifest registry
- ❓ Questions for 3 teams (see COORD-2025-005, 006, 007)

**Action Required:**
- Response by Nov 14, 2025
- Onboard to coordination hub
- Begin W3 coordination (if dependencies met)

---

### COORD-2025-005: Questions for ecosystem-manifest

**Status:** Prepared (will submit after onboarding accepted)
**Priority:** High
**Created:** 2025-10-31
**Target Repo:** ecosystem-manifest
**Trace ID:** ecosystem-w3-health-monitoring

**Summary:**
Clarifying questions about server registry timeline and schema for W3 Health Monitoring integration.

**File:** [COORD-2025-005-ecosystem-manifest-questions.json](coordination/COORD-2025-005-ecosystem-manifest-questions.json)

**Critical Questions:**
1. When will repository be created? Is Week 4 delivery realistic?
2. What health check fields in registry? Schema versioning?
3. Sample registry file for early integration testing?

**Impact if Delayed:**
- Blocks auto-discovery feature (P1 blocker)
- Forces hardcoded server list (technical debt)
- May delay W3 Go decision (Nov 15)

---

### COORD-2025-006: Questions for mcp-gateway

**Status:** Prepared (will submit after onboarding accepted)
**Priority:** Medium
**Created:** 2025-10-31
**Target Repo:** mcp-gateway
**Trace ID:** ecosystem-w3-health-monitoring

**Summary:**
Coordinate health status API integration and testing timeline for W3 Health Monitoring.

**File:** [COORD-2025-006-mcp-gateway-questions.json](coordination/COORD-2025-006-mcp-gateway-questions.json)

**Critical Questions:**
1. Response format for health status API? JSON schema?
2. Real-time WebSocket or HTTP polling preference?
3. Ready for integration testing Week 9?
4. Acceptance criteria for integration success?

**Our Deliverables:**
- Health Status API v1.0 (Week 8)
- OpenAPI spec with examples
- Test environment (5 sample servers)
- Integration test script
- On-call support (<2h response)

---

### COORD-2025-007: Questions for chora-base

**Status:** Prepared (will submit after onboarding accepted)
**Priority:** Medium
**Created:** 2025-10-31
**Target Repo:** chora-base
**Trace ID:** ecosystem-w3-health-monitoring

**Summary:**
Questions about W3 health check templates and Docker patterns for Health Monitoring implementation.

**File:** [COORD-2025-007-chora-base-questions.json](coordination/COORD-2025-007-chora-base-questions.json)

**Critical Questions:**
1. Are health check templates W3-ready? Status?
2. Best practices for health monitoring? (polling, thresholds)
3. Auto-recovery patterns? (restart strategies, backoff)
4. ROI validation for 200-300% template claim?

**Decision Criteria:**
- Use templates if: W3-ready, documented, save >2 hours
- Custom implementation if: Not ready by Week 4, don't fit use case
- Impact: 3h savings (5h custom → 2h templates) = 60% reduction

---

## Coordination Protocol Usage

### How to Submit

1. **Create JSON request** following schema ([../schemas/coordination-request.schema.json](../schemas/coordination-request.schema.json))
2. **Write communication brief** (optional but recommended for complex requests)
3. **Log event** to `../coordination/events.jsonl`
4. **Notify target repo** (GitHub issue, email, etc.)

### Event Logging

All coordination requests logged to `../coordination/events.jsonl` with:
- `trace_id`: For cross-repo tracking
- `event_type`: coordination_submitted, coordination_accepted, etc.
- `source`: mcp-orchestration
- `target`: Target repository name
- `metadata`: Additional context

**Example:**
```json
{"timestamp":"2025-10-31T21:05:00Z","trace_id":"ecosystem-coordination-launch-2025-10-31","event_type":"coordination_submitted","source":"mcp-orchestration","target":"chora-workspace","metadata":{"participation_level":"full_onboarding","w3_conditional":true,"coordination_id":"COORD-2025-004"}}
```

### Trace IDs

**Current trace IDs:**
- `ecosystem-coordination-launch-2025-10-31` - Onboarding coordination
- `ecosystem-w3-health-monitoring` - W3 Health Monitoring coordination (ecosystem-manifest, mcp-gateway, chora-base)

**Query events:**
```bash
# All W3-related events
jq 'select(.trace_id=="ecosystem-w3-health-monitoring")' ../coordination/events.jsonl

# All our outgoing coordination
jq 'select(.source=="mcp-orchestration")' ../coordination/events.jsonl
```

---

## Timeline

### Phase 1: Onboarding (Nov 1-14)

| Date | Activity | Status |
|------|----------|--------|
| **Oct 31** | Submit COORD-2025-004 (Full Onboarding) | ✅ Submitted |
| **Nov 7** | Submit capability declaration | 📋 Planned |
| **Nov 7** | Create inbox/ structure in repo | 📋 Planned |
| **Nov 14** | Response deadline | ⏰ Deadline |

### Phase 2: Team Coordination (Nov 9-22)

| Date | Activity | Status |
|------|----------|--------|
| **Nov 9** | Submit COORD-2025-005 (ecosystem-manifest) | 📋 Prepared |
| **Nov 9** | Submit COORD-2025-006 (mcp-gateway) | 📋 Prepared |
| **Nov 9** | Submit COORD-2025-007 (chora-base) | 📋 Prepared |
| **Nov 9-22** | Monitor responses, coordinate follow-ups | 📋 Planned |

### Phase 3: W3 Go/NoGo (Nov 15)

| Date | Activity | Status |
|------|----------|--------|
| **Nov 15** | W3 Go/NoGo decision | ⏰ Decision Point |
| **Week 5-8** | W3 implementation (if Go) | ⏸️ Conditional |

---

## Success Criteria

### For Onboarding (COORD-2025-004)

**Must-Have:**
- ✅ Coordination request submitted by Nov 14
- ✅ Capability declaration submitted by Nov 7
- ✅ Inbox protocol adopted in mcp-orchestration

**Success Indicators:**
- ✅ Dashboard shows our blockers (ecosystem-manifest, chora-base)
- ✅ Can track dependency progress in real-time
- ✅ Event traceability working

### For Team Coordination (COORD-2025-005, 006, 007)

**Must-Have:**
- ✅ All 3 requests submitted by Nov 9
- ✅ Responses received by Nov 22
- ✅ Blockers clarified or resolved

**Success Indicators:**
- ✅ ecosystem-manifest timeline confirmed (Week 4 feasible or not)
- ✅ mcp-gateway API requirements clarified
- ✅ chora-base templates assessed (use or custom)

### For W3 Go Decision (Nov 15)

**Go Criteria:**
- ✅ Wave 2.0 v0.2.0 released
- ✅ ecosystem-manifest Week 4 delivery confirmed or workaround acceptable
- ✅ chora-base templates reviewed

**NoGo Criteria:**
- ❌ Wave 2.0 quality gates failing
- ❌ ecosystem-manifest timeline too uncertain
- ❌ Too many unknowns/blockers

---

## Contact

**Repository:** mcp-orchestration
**Team:** MCP Orchestration Team
**Coordination Lead:** [Your name]
**Response Time:** <2 business days for coordination requests

**For questions:**
- GitHub Issues: https://github.com/[org]/mcp-orchestration/issues
- Coordination Dashboard: (link when available)
- Email: (provide email)

---

**Document Created:** 2025-10-31
**Last Updated:** 2025-10-31
**Active Requests:** 4 (1 submitted, 3 prepared)
**Total Events Logged:** 1
