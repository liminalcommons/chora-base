# COORD-2025-004: Bidirectional Translation Layer Integration

**Status:** Pending Triage
**Created:** 2025-10-31
**Priority:** P2 (Medium)
**Urgency:** Next Sprint (Sprint 5 or 6)
**Trace ID:** coord-2025-004-bidirectional

## Executive Summary

Formal coordination request to complete the bidirectional translation layer integration (Phase 2-4 of [BIDIRECTIONAL_COMMUNICATION.md](../../docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md)). Foundation tools are complete (Phase 1), but integration work remains to enable agents to "just know" how to use these tools as native and second nature.

## Context

This request emerged from exploration of traceability applicability across SAPs, following proper chora-base governance process (intake → DDD → BDD → TDD).

**Foundation Work Complete (Phase 1):**
- [scripts/intent-router.py](../../scripts/intent-router.py) - Natural language → formal actions
- [scripts/chora-search.py](../../scripts/chora-search.py) - Glossary search with fuzzy matching
- [scripts/suggest-next.py](../../scripts/suggest-next.py) - Context-aware next action suggestions
- [docs/dev-docs/patterns/INTENT_PATTERNS.yaml](../../docs/dev-docs/patterns/INTENT_PATTERNS.yaml) - 24 intent patterns
- [docs/GLOSSARY.md](../../docs/GLOSSARY.md) - 75+ terms, 14 categories
- [.chora/user-preferences.yaml.template](../../.chora/user-preferences.yaml.template) - 100+ config options
- [docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md](../../docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md) - Implementation guide
- [AGENTS.md](../../AGENTS.md) (+214 lines) - Tool discovery patterns

**Integration Work Needed (Phase 2-4):**
- Enhanced SAP-009 (agent-awareness) v1.0.0 → v1.1.0
- Domain AGENTS.md files for 5 SAPs (001, 004, 009, 012, 013)
- Suggestion engine integration with inbox protocol
- BDD scenarios and test coverage ≥85%
- Governance documentation (CHANGELOG, SAP Index, ledger)

## Classification

- **Type:** Type 3 Implementation Tasks + Type 2 Coordination
- **SAP:** Enhancement to SAP-009 (agent-awareness) v1.0.0 → v1.1.0
- **Release:** PATCH (v4.1.2 → v4.1.3)
- **Effort:** 16-24 hours over 1-2 sprints

## Deliverables (11 total)

1. Enhanced SAP-009 protocol-spec.md (Section 9: Bidirectional Translation Layer)
2. Enhanced SAP-009 awareness-guide.md (Integration patterns for generic agents)
3. Enhanced SAP-009 ledger.md (v1.1.0 adoption tracking)
4. Enhanced root AGENTS.md (tool discovery patterns) - **COMPLETE**
5. Enhanced domain AGENTS.md files (5 SAPs with user signal patterns)
6. Suggestion engine integration with inbox protocol
7. BDD scenarios (intent recognition, preferences, pattern learning)
8. Test coverage ≥85% for integration code
9. CHANGELOG.md entry for v4.1.3 release
10. SAP Index update (SAP-009 v1.0.0 → v1.1.0)
11. Event log entries with trace_id

## Acceptance Criteria (12 total)

1. Intent recognition accuracy ≥80% on test query set (30+ queries)
2. Generic agents can discover and use tools via documentation alone
3. Tools gracefully degrade (missing tool → fall back to documented patterns)
4. User preferences successfully adapt agent behavior (100+ config options)
5. Pattern learning captures new variations without breaking existing patterns
6. Suggestion engine provides context-aware recommendations
7. All BDD scenarios pass
8. Test coverage ≥85%
9. No lint/type errors
10. Documentation follows Diátaxis framework
11. SAP-009 enhancement properly versioned (v1.0.0 → v1.1.0)
12. CHANGELOG follows semantic versioning (v4.1.2 → v4.1.3 PATCH)

## Development Workflow

Following SAP-012 Development Lifecycle:

### Phase 1: Intake & Coordination (CURRENT)
- ✅ Coordination request created
- ✅ Event logged (coordination_request_created)
- ✅ ECOSYSTEM_STATUS.yaml updated
- ⏳ Awaiting sprint planning triage

### Phase 2: DDD (Documentation Driven Design)
- Create change-request.md (Diátaxis format)
- Technical lead approval
- Phase completion event

### Phase 3: BDD (Behavior Driven Development)
- Write Gherkin scenarios (features/bidirectional-integration.feature)
- Implement step definitions
- Verify RED (all fail initially)

### Phase 4: TDD (Test Driven Development)
- RED-GREEN-REFACTOR cycles
- Update SAP-009 artifacts
- Add user signal patterns to 5 domain AGENTS.md files
- Achieve ≥85% coverage

### Phase 5: Testing & Quality Gates
- Test intent recognition accuracy (≥80% target)
- Test preference adaptation
- Test pattern learning
- Validate coverage, lint, type checks

### Phase 6: Governance Documentation
- Update SAP-009 (protocol, guide, ledger)
- Update CHANGELOG.md (v4.1.3 entry)
- Update SAP Index

### Phase 7: Review & Integration
- Create PR with checklist
- Code review and approval
- CI/CD validation

### Phase 8: Release & Deployment
- Version bump (4.1.2 → 4.1.3)
- Create GitHub release
- Archive completed work

## Timeline

- **Total Effort:** 16-24 hours
- **Duration:** 1-2 sprints (Sprint 5 or 6, Q1 2026)
- **Triage:** Next sprint planning session

## Dependencies

All dependencies satisfied:
- ✅ Foundation tools complete (Phase 1)
- ✅ Root AGENTS.md updated (+214 lines)
- ✅ .gitignore updated for user configs

## Traceability

- **Trace ID:** coord-2025-004-bidirectional
- **Event Log:** [inbox/coordination/events.jsonl](events.jsonl)
- **Related SAPs:** SAP-001, SAP-004, SAP-009, SAP-012, SAP-013
- **Target Release:** v4.1.3 (PATCH)

## Rationale

User correctly noted we must "use our process and including governance and administrative doc updates where appropriate" after foundation tools were built. This coordination request establishes proper governance for completing the integration work, following the full DDD → BDD → TDD lifecycle with quality gates and traceability.

The bidirectional translation layer enables mutual ergonomics: conversational user input → procedural execution with progressive formalization over time. This supports both new users (start casual, learn gradually) and experienced users (systemic ontology fluency).

## Next Steps

1. **Sprint Planning Triage:** Review and accept for Sprint 5 or 6
2. **DDD Phase:** Create change-request.md following Diátaxis
3. **BDD Phase:** Write Gherkin scenarios
4. **TDD Phase:** RED-GREEN-REFACTOR implementation
5. **Quality Gates:** Coverage ≥85%, all tests passing
6. **Governance Updates:** CHANGELOG, SAP-009 artifacts, SAP Index
7. **Release:** v4.1.3 (PATCH)

## Questions or Concerns?

Review the detailed implementation plan in [BIDIRECTIONAL_COMMUNICATION.md](../../docs/dev-docs/workflows/BIDIRECTIONAL_COMMUNICATION.md) or refer to the coordination request JSON: [COORD-2025-004-bidirectional-integration.json](../incoming/coordination/COORD-2025-004-bidirectional-integration.json)

---

**Created by:** Victor Piper + Claude Code
**Date:** 2025-10-31
**Status:** Pending Triage
