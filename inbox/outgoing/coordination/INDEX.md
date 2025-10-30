# Outgoing Coordination Requests Index

This directory tracks coordination requests sent from chora-base to other repositories in the ecosystem.

## Active Requests

### COORD-2025-002: chora-compose Exploration
- **To**: chora-compose team
- **Date Sent**: 2025-10-29
- **Type**: Architecture proposal (exploratory)
- **Status**: ⏳ Awaiting Response
- **Question**: Is structured documentation generation within chora-compose's vision?
- **Files**:
  - [COORD-2025-002-chora-compose-exploration.json](./COORD-2025-002-chora-compose-exploration.json) (machine-readable)
  - [COORD-2025-002-exploration-summary.md](./COORD-2025-002-exploration-summary.md) (human-readable)
- **Context**: Wave 6 (Collections Architecture v4.2.0) exploration - understanding if chora-compose could be composition engine for SAP artifact generation
- **No Deadline**: Response whenever convenient, doesn't block v4.1.0 work
- **Next Step**: Monitor for response, adjust Wave 6 plans based on feedback

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
