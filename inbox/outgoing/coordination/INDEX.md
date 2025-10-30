# Outgoing Coordination Requests Index

This directory tracks coordination requests sent from chora-base to other repositories in the ecosystem.

## Active Requests

### COORD-2025-002: chora-compose Exploration
- **To**: chora-compose team
- **Date Sent**: 2025-10-29
- **Type**: Architecture proposal (exploratory)
- **Status**: ✅ Clarification Complete & Ready for Pilot (2025-10-30)
- **Question**: Is structured documentation generation within chora-compose's vision?
- **Answer**: YES - Strong alignment! chora-compose IS content generation framework with 17 generators
- **Files**:
  - [COORD-2025-002-chora-compose-exploration.json](./COORD-2025-002-chora-compose-exploration.json) (our request)
  - [COORD-2025-002-exploration-summary.md](./COORD-2025-002-exploration-summary.md) (our request summary)
  - `../../incoming/coordination/COORD-2025-002-response.json` (their response)
  - [../../COORD-2025-002-RESPONSE.json](../../COORD-2025-002-RESPONSE.json) (our acceptance)
  - [../../COORD-2025-002-RESPONSE-summary.md](../../COORD-2025-002-RESPONSE-summary.md) (acceptance summary)
  - [../../COORD-2025-002-CLARIFICATION.json](../../COORD-2025-002-CLARIFICATION.json) (follow-up clarification - 5 questions)
  - [../../COORD-2025-002-CLARIFICATION-summary.md](../../COORD-2025-002-CLARIFICATION-summary.md) (clarification summary)
  - `../../incoming/coordination/COORD-2025-002-CLARIFICATION-response.json` (comprehensive answers - 1,124 lines)
  - [../../COORD-2025-002-CLARIFICATION-RESPONSE-acknowledgment.json](../../COORD-2025-002-CLARIFICATION-RESPONSE-acknowledgment.json) (readiness confirmed)
- **Outcome**: Pilot project approved - Generate SAP-004 (Testing Framework) - 1-2 weeks, 4-6 hours effort
- **Clarification Sent**: 2025-10-30 - 5 questions about caching, content architecture, context schema, hybrid model, storage
- **Clarification Received**: 2025-10-30 - All questions answered comprehensively, **no blockers for pilot**
- **Key Findings**:
  - Q1 (Caching): Partial support - use `force: bool` parameter, works for pilot
  - Q2 (Content Architecture): Perfect match - ContentElement with hybrid template slots + modular blocks
  - Q3 (Context Schema): Fully flexible - 6 InputSource types, custom fields supported
  - Q4 (Hybrid Model): Partial support - manual hybrid via external_file works today
  - Q5 (Storage Location): Clear patterns - content blocks in chora-base, configs in both repos
- **Pilot Readiness**: Week 1 decomposition steps detailed, expected outputs specified, feature gaps identified (2-6 hours each if needed)
- **Next Step**: Begin Week 1 decomposition (~2025-11-06), execute pilot, make go/no-go decision (~2025-11-19)

## Completed Responses

### COORD-2025-001: Minimal SAP Collaboration (Response to chora-workspace)
- **To**: chora-workspace team
- **Date Sent**: 2025-10-29
- **Type**: Response to coordination request
- **Status**: ✅ Sent (awaiting their feedback)
- **Decision**: Accepted with modifications (SAP sets approach)
- **Files**:
  - [../COORD-2025-001-response.json](../COORD-2025-001-response.json) (machine-readable)
  - [../COORD-2025-001-response-summary.md](../COORD-2025-001-response-summary.md) (human-readable)
- **Deliverable**: SAP sets feature in Wave 5 (v4.1.0, Q1 2026)
- **Next Step**: Await chora-workspace pilot feedback

---

## Coordination Protocol

For details on how coordination requests work, see:
- **Protocol**: [../INBOX_PROTOCOL.md](../INBOX_PROTOCOL.md)
- **Schema**: [../schemas/coordination-request.schema.json](../schemas/coordination-request.schema.json)
- **Examples**: [../examples/](../examples/)

## Response Tracking

Responses from other repos are tracked in:
- `inbox/incoming/coordination/` - New coordination requests to chora-base
- `inbox/active/` - Work in progress
- `inbox/completed/` - Archived completed work
