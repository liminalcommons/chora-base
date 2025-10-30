# Outgoing Coordination Requests Index

This directory tracks coordination requests sent from chora-base to other repositories in the ecosystem.

## Active Requests

### COORD-2025-002: chora-compose Exploration
- **To**: chora-compose team
- **Date Sent**: 2025-10-29
- **Type**: Architecture proposal (exploratory)
- **Status**: ✅ Response Received & Pilot Approved (2025-10-29)
- **Question**: Is structured documentation generation within chora-compose's vision?
- **Answer**: YES - Strong alignment! chora-compose IS content generation framework with 17 generators
- **Files**:
  - [COORD-2025-002-chora-compose-exploration.json](./COORD-2025-002-chora-compose-exploration.json) (our request)
  - [COORD-2025-002-exploration-summary.md](./COORD-2025-002-exploration-summary.md) (our request summary)
  - `../../incoming/coordination/COORD-2025-002-response.json` (their response)
  - [../../COORD-2025-002-RESPONSE.json](../../COORD-2025-002-RESPONSE.json) (our acceptance)
  - [../../COORD-2025-002-RESPONSE-summary.md](../../COORD-2025-002-RESPONSE-summary.md) (acceptance summary)
- **Outcome**: Pilot project approved - Generate SAP-004 (Testing Framework) - 1-2 weeks, 4-6 hours effort
- **Next Step**: Execute pilot (~2025-11-06 to 2025-11-19), make go/no-go decision for Wave 6 Option B

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
