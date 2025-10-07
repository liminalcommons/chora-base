---
title: Release B Plan — Telemetry & Liminal Integration
status: draft
version: 0.1.0
last_updated: 2025-10-07
---

# Release B Plan — MCP Orchestration

Release B focuses on adopting the platform telemetry/overview tooling and integrating with the liminal inbox prototype.

## Objectives
- Emit telemetry for key CLI flows using the shared emitter.
- Publish repository overviews alongside manifests and value scenarios.
- Provide liminal-ready bundles (manifest + telemetry + signals) for inbox ingestion.
- Track progress via change signals and update documentation accordingly.

## Workstreams & Status

### 1. Telemetry Adoption
- [x] Import telemetry emitter (shim) and write CLI events to `var/telemetry/events.jsonl`.
- [x] Document telemetry usage in `docs/how-to/telemetry.md` (commands + schema).
- [x] Update CI to archive telemetry samples for liminal testing.

### 2. Repository Overview Publication
- [x] Run `scripts/generate_repo_overview.py manifests/star.yaml -o docs/reference/overview.md` and commit output.
- [ ] Include overview link in README + change signal updates.
- [ ] Add automation step (Makefile or script) to refresh overview and fail CI if stale.

### 3. Liminal Bundle Prep
- [x] Package manifest, overview, telemetry, and change signal notes under `var/bundles/liminal/` (README + structure).
- [ ] Provide usage notes for liminal repo (`docs/how-to/share-with-liminal.md`).
- [ ] Emit signal update `SIG-liminal-inbox-prototype` referencing bundle location.

### 4. Governance & Comms
- [ ] Update `docs/reference/release-b-plan.md` checkboxes as work completes.
- [ ] Add weekly progress note to `docs/reference/signals/SIG-capability-onboard.md` during Release B.
- [ ] Confirm adoption by referencing platform change signal `SIG-telemetry-adoption`.

## Acceptance Criteria
1. Telemetry events generated for manifest and scenario validation commands; emitter outputs validated in tests.
2. Repository overview kept in sync with manifest and value scenario metadata (CI enforcement).
3. Liminal bundle available with documentation, consumed successfully by inbox prototype (evidence via change signal).
4. Release documentation updated with links to telemetry files, overview artifacts, and liminal bundle instructions.

## Evidence Checklist
- `var/telemetry/events.jsonl`
- `docs/reference/overview.md`
- `var/bundles/liminal/README.md` (or equivalent packaging notes)
- Change signal updates referencing telemetry + bundle locations

Keep this plan current; mark tasks complete with timestamps and link supporting PRs or commits.
