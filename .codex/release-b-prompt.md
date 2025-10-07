# Codex Instructions — Release B (MCP Orchestration)

Telemetry, overview, CI validators, and liminal bundle packaging are live. Focus on the final Release B gates and coordination tasks.

## Context
- Release docs: `docs/reference/release-b-plan.md` (telemetry/overview tasks complete; freshness gate + liminal signal pending), `docs/reference/release-a-plan.md` (closure notes).
- Automation: `.github/workflows/chora-ci.yml` runs validators/tests, generates `docs/reference/overview.md`, uploads telemetry (`var/telemetry/events.jsonl`) and bundle (`var/bundles/liminal/mcp-orchestration-bundle.zip`).
- Documentation: `docs/how-to/telemetry.md`, `docs/how-to/share-with-liminal.md`, README links to overview/telemetry.
- Change signal: `docs/reference/signals/SIG-capability-onboard.md` captures Release B run; liminal inbox signal still outstanding.

## Next Objectives
1. **Overview Freshness Gate** — Implement CI enforcement (e.g., script step) that fails when `docs/reference/overview.md` is stale compared with `manifests/star.yaml`. Update release plan and signals once active.
2. **Liminal Signal Emission** — After verifying liminal bundle ingestion, create/update a liminal-specific signal entry with artifact paths and telemetry evidence.
3. **Telemetry Migration Prep** — Plan the transition from local shim to platform `TelemetryEmitter`. Document required changes and dependencies in the release plan.
4. **Evidence Hygiene** — Continue logging validator/test commands, bundle metadata, and coordination notes in `docs/reference/release-b-plan.md` and signals (timestamps + artifact links).

## Workflow Expectations
- Review outstanding checklist items before editing.
- Run validators/tests (manifest, behavior, scenario, pytest) whenever telemetry, manifest, or overview code changes.
- After CI or local packaging, update docs/signals with bundle paths and telemetry summaries.

## Guardrails
- Preserve stdout JSON-RPC purity for CLI tools; log diagnostics to stderr.
- Keep telemetry/bundle outputs under `var/`; documentation updates under `docs/`.
- Coordinate schema changes with platform signals prior to merging.
