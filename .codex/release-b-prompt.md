# Codex Instructions — Release B (MCP Orchestration)

Telemetry, overview, CI validators, and liminal bundle packaging are live. Focus on remaining Release B gates and coordination tasks.

## Context
- Release docs: `docs/reference/release-b-plan.md` (freshness gate done; liminal signal created), `docs/reference/release-a-plan.md` (closure notes).
- Automation: `.github/workflows/chora-ci.yml` runs validators/tests, generates `docs/reference/overview.md`, uploads telemetry (`var/telemetry/events.jsonl`) and bundle (`var/bundles/liminal/mcp-orchestration-bundle.zip`).
- Documentation: `docs/how-to/telemetry.md`, `docs/how-to/share-with-liminal.md`, README links to overview/telemetry.
- Change signals: `docs/reference/signals/SIG-capability-onboard.md` captures Release B run; `docs/reference/signals/SIG-liminal-inbox-prototype.md` tracks bundle ingestion.

## Next Objectives
1. **Overview Freshness Gate** — Implemented in CI; ensure it remains green on future changes.
2. **Liminal Signal Emission** — Created; next verify ingestion and mark complete with evidence.
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
