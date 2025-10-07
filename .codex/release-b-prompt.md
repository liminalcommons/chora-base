# Codex Instructions — Release B (MCP Orchestration)

Own Release B adoption for the MCP orchestration capability and stay aligned with platform guidance.

## Context
- Release docs: `docs/reference/release-a-plan.md` (closed) and `docs/reference/release-b-plan.md` (active tracker).
- Operational assets: `manifests/star.yaml`, `docs/capabilities/behaviors/`, value scenario docs/tests, `scripts/`, and telemetry sink `var/telemetry/events.jsonl`.
- Coordination: platform digests (`chora-platform/docs/reference/release-b-digest/`), liminal bundle expectations, change signal `docs/reference/signals/SIG-capability-onboard.md`.

## Objectives
1. **Telemetry Integration** — Import `TelemetryEmitter` from `chora_platform_tools` (vendored or vendored copy) into CLI pathways (manifest/behavior/scenario validators, automation scripts). Emit structured events to `var/telemetry/events.jsonl`, add regression tests, and document usage under `docs/how-to/telemetry.md`.
2. **Repository Overview Publication** — Generate `docs/reference/overview.md` (Markdown + optional JSON) using `scripts/generate_repo_overview.py`. Add a refresh command/CI check to prevent drift and link the overview from README + change signals.
3. **Liminal Bundle Delivery** — Package manifest, overview, telemetry snapshot, and the latest signal note into `var/bundles/liminal/`. Provide instructions for consumers (`docs/how-to/share-with-liminal.md`) and reference bundle commit hashes in `SIG-liminal-inbox-prototype`.
4. **Governance Updates** — Keep `docs/reference/release-b-plan.md` and `docs/reference/signals/SIG-capability-onboard.md` current (timestamps, evidence links, dependencies on platform artifacts).

## Workflow Expectations
- Sync with the latest platform release digest before starting work; pull any schema or bundle updates.
- Run required validators/tests (`python -m mcp_orchestrator.cli ...`, `pytest -q`) whenever manifests, behaviors, or telemetry code changes.
- After each milestone, update release docs and change signals, and drop breadcrumbs (paths/commands) other agents can reuse.

## Guardrails
- Maintain stdout JSON-RPC purity for CLI scripts; emit diagnostics to stderr.
- Keep telemetry artifacts under `var/` and document any vendored platform modules.
- Coordinate schema changes with platform signals before committing breaking updates.
