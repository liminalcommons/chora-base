# Codex Instructions — Release B (MCP Orchestration)

Value scenario onboarding is complete; finish telemetry adoption and bundle delivery for Release B.

## Context
- Release docs: `docs/reference/release-b-plan.md` (active), `docs/reference/release-a-plan.md` (closure notes).
- Assets: `manifests/star.yaml`, behaviors under `docs/capabilities/behaviors/`, value scenario docs/tests, telemetry sink `var/telemetry/events.jsonl`, bundle directory `var/bundles/liminal/`.
- Documentation: `docs/how-to/create-doc.md`, telemetry/bundle stubs (`docs/how-to/telemetry.md`, `docs/how-to/share-with-liminal.md`).
- Change signal: `docs/reference/signals/SIG-capability-onboard.md` (log weekly progress).

## Priorities
1. **Telemetry Integration** — Vendor/import `TelemetryEmitter` from platform tooling, emit events for validator CLI commands + key flows, and capture examples in `docs/how-to/telemetry.md`. Add regression tests covering JSONL output.
2. **CI & Validator Coverage** — Add/update automation (workflow or script) to run manifest/behavior/scenario validators and pytest on every change. Record evidence in release plan and change signal.
3. **Liminal Bundle Prep** — Populate `var/bundles/liminal/` with manifest, overview, telemetry snapshot, and signal note. Document packaging/consumption steps in `docs/how-to/share-with-liminal.md` and reference bundle hashes in change signals.
4. **Overview Publication** — Generate `docs/reference/overview.md` via `scripts/generate_repo_overview.py`, enforce freshness (pre-commit or CI), and link from README + signals.

## Workflow Expectations
- Review outstanding checkboxes in `docs/reference/release-b-plan.md` before new work.
- After running validators/tests, update release docs and change signals with command outputs and timestamps.
- Keep telemetry artifacts organised under `var/` and share bundle metadata when coordinating with `chora-liminal`.

## Guardrails
- Maintain stdout JSON-RPC purity for CLI scripts; log diagnostics to stderr.
- Coordinate schema updates with platform signals before merging breaking changes.
- Run `pytest -q` (and validator commands) whenever telemetry or manifest logic changes.
