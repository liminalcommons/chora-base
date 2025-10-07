# Codex Instructions — Release B (MCP Orchestration)

Release B telemetry, overview, and bundling are in place; drive the remaining gates to completion.

## Context
- Release docs: `docs/reference/release-b-plan.md` (telemetry + overview tasks checked off, remaining items highlighted), `docs/reference/release-a-plan.md` (closure notes).
- Automation: `.github/workflows/chora-ci.yml` runs validators, pytest, generates `docs/reference/overview.md`, uploads telemetry and liminal bundle artifacts.
- Telemetry: CLI shim emits JSONL to `var/telemetry/events.jsonl`; documented in `docs/how-to/telemetry.md`.
- Bundles: `var/bundles/liminal/mcp-orchestration-bundle.zip` generated locally/CI with manifest, overview, telemetry, signal snippet; packaging steps in `docs/how-to/share-with-liminal.md`.
- Change signals: `docs/reference/signals/SIG-capability-onboard.md` closed for Release A with Release B notes; liminal signal still pending.

## Remaining Objectives
1. **Overview Freshness Gate** — Implement CI enforcement that fails when `docs/reference/overview.md` is stale relative to `manifests/star.yaml`. Update release plan and signal once active.
2. **Liminal Signal Emission** — After the next liminal ingestion run, emit `SIG-liminal-inbox-prototype` entry referencing the bundle zip and telemetry evidence. Document steps in the release plan.
3. **Telemetry Migration** — Plan swap from local shim to platform `TelemetryEmitter`; capture actions/risks when the shared package is available.
4. **Continuous Evidence** — Keep `docs/reference/release-b-plan.md` and signal notes updated with timestamps, command outputs, and artifact paths; link CI artifacts where applicable.

## Workflow Expectations
- Start by reviewing unchecked tasks in `docs/reference/release-b-plan.md`.
- Run validators + pytest locally (PYTHONPATH=src) after changes touching manifests or telemetry.
- When CI artifacts update, mirror the evidence (bundle paths, overview hash) into docs/signals.

## Guardrails
- Maintain stdout JSON-RPC purity for CLI tools; send diagnostics to stderr.
- Store telemetry/bundle outputs under `var/` and documentation under `docs/` as already structured.
- Coordinate schema changes with platform signals before shipping breaking updates.
