# Ledger: Capability Registry & Service Discovery

**Capability ID**: SAP-048
**Modern Namespace**: chora.awareness.capability_registry_discovery
**Type**: Pattern
**Current Status**: Draft
**Current Version**: 1.0.0
**Created**: 2025-11-16
**Last Updated**: 2025-11-16

---

## Version History

### Version 1.0.0 (2025-11-16) - Initial Release

**Status**: Draft → Production (pending dogfooding)

**Changes**:
- Initial SAP creation
- Defined 5 core agent awareness patterns
- Created complete protocol specification for etcd schema
- Documented agent workflows and integration patterns
- Provided adoption blueprint with validation steps

**Artifacts Created**:
- [capability-charter.md](capability-charter.md) - Problem statement and solution design
- [protocol-spec.md](protocol-spec.md) - Complete technical specification
- [AGENTS.md](AGENTS.md) - Agent awareness guide with workflows
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step adoption guide
- [ledger.md](ledger.md) - This file

**Infrastructure Dependencies**:
- etcd cluster (3-node Raft consensus) - Running
- GitOps sync service - Running
- Heartbeat service - Running
- Artifact indexing script - Implemented

**Metrics** (Initial):
- Capabilities indexed: 45
- Services monitored: 9
- Artifacts indexed: 225 (45 × 5)
- Query latency: ~5ms (metadata reads)
- Heartbeat interval: 10s
- TTL lease duration: 30s

**Contributors**:
- Claude (AI Agent) - SAP design and implementation
- Victor (Project Lead) - Requirements and review

---

## Adoption Tracking

### Adoption Status: Not Yet Adopted

**Target Adoption Date**: 2025-11-23 (1 week dogfooding period)

**Adoption Progress**:
- [x] Infrastructure deployed (etcd, GitOps, heartbeat)
- [x] Artifacts indexed
- [ ] Agent integration (pending)
- [ ] Validation tests (pending)
- [ ] Documentation review (pending)
- [ ] Dogfooding period (pending)
- [ ] Production readiness assessment (pending)

**Blockers**: None

**Dependencies**:
- etcd cluster must remain operational
- GitOps sync must run continuously (60s interval)
- Heartbeat service must run for Service-type capabilities

---

## Adoption Metrics

### Target Metrics (Week 1)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Registry queries per day | >100 | TBD | Pending |
| Health checks per day | >50 | TBD | Pending |
| Artifact searches per day | >10 | TBD | Pending |
| Query response time | <10ms | ~5ms | ✓ Met |
| Service uptime | >99% | TBD | Pending |
| Agent integrations | ≥1 | 0 | Pending |

### Long-Term Metrics (Week 4)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Registry queries per day | >500 | TBD | Pending |
| Health checks per day | >200 | TBD | Pending |
| Artifact searches per day | >50 | TBD | Pending |
| Agent integrations | ≥3 | 0 | Pending |
| User satisfaction | ≥4/5 | TBD | Pending |

---

## Feedback Log

### 2025-11-16: Initial Creation

**Source**: Claude (AI Agent)
**Type**: Design Decision
**Feedback**:
- Created SAP-048 to formalize registry discovery patterns
- Infrastructure exists (etcd, GitOps, heartbeat) but lacks agent awareness
- Identified 5 core patterns: discovery, health, dependencies, search, watch
- Chose etcd keyword search over Elasticsearch for simplicity (can upgrade later)

**Action Taken**: Created complete SAP with 5 required artifacts

**Next Steps**:
1. Run dogfooding period with Claude Code agents
2. Gather metrics on query performance and usage
3. Collect agent feedback on pattern usability
4. Refine documentation based on real-world usage
5. Promote to production status if metrics met

---

## Issues and Resolutions

### Issue 1: Search Scalability (2025-11-16)

**Status**: Identified, Not Yet Resolved

**Description**: Simple keyword search may not scale to >10,000 artifacts

**Impact**: Medium (search performance may degrade with many capabilities)

**Proposed Solution**:
- Monitor search performance during dogfooding
- If search latency >100ms, evaluate Elasticsearch integration
- Design external FTS integration without breaking existing patterns

**Timeline**: Evaluate during Week 2 of dogfooding

---

### Issue 2: Watch Mode Filtering (2025-11-16)

**Status**: Identified, Design Decision Made

**Description**: Watch mode returns all events, requiring client-side filtering

**Impact**: Low (agents can filter events easily)

**Resolution**: Use client-side filtering initially. If too many events, add server-side filtering via etcd watch predicates

---

### Issue 3: Metadata Caching Strategy (2025-11-16)

**Status**: Identified, Design Decision Made

**Description**: Should agents cache metadata or always query fresh?

**Impact**: Medium (affects query load and freshness)

**Resolution**:
- Health checks: Always query fresh (critical for accuracy)
- Metadata: Cache for 60s (metadata changes infrequently)
- Artifact content: Cache indefinitely (versioned, immutable)

---

## Change Requests

_No change requests yet. This section will track requested changes during dogfooding._

---

## Usage Examples from Real Projects

_This section will be populated during dogfooding period with real-world usage patterns._

---

## Community Contributions

_This section will track community contributions, improvements, and extensions._

---

## Deprecations and Migrations

_No deprecations yet. This section will track any deprecated patterns or migration guides._

---

## References

- [Capability Charter](capability-charter.md) - Problem statement and solution
- [Protocol Specification](protocol-spec.md) - Technical specification
- [Awareness Guide](AGENTS.md) - Agent patterns
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - SAP schema definition
- [etcd Documentation](https://etcd.io/docs/) - etcd reference

---

## Appendix: Metrics Collection

### How to Collect Metrics

**Registry Query Count**:
```bash
# Count etcd read operations (approximate)
docker-compose exec etcd1 etcdctl endpoint status --write-out=json | jq '.[] | .raft_applied_index'
# Compare over time to estimate query rate
```

**Health Check Count**:
```bash
# Count health key reads (requires etcd metrics)
curl http://localhost:2379/metrics | grep grpc_server_handled_total | grep GetRange
```

**Artifact Search Count**:
```bash
# Instrument registry_client.py to log searches
# Add logging to search_artifacts() method
import logging
logging.info(f"Artifact search: query={query}, results={len(results)}")
```

**Query Response Time**:
```python
import time

start = time.time()
metadata = etcd.get('/chora/capabilities/chora.devex.registry/metadata')
elapsed = (time.time() - start) * 1000  # Convert to ms
print(f"Query time: {elapsed:.2f}ms")
```

---

**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-16
**Next Review**: 2025-11-23 (after 1 week dogfooding)
