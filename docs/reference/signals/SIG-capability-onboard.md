# SIG-capability-onboard

Tracks onboarding of manifests/behaviors to Chora platform standards.

## Tasks
- [x] Validate star.yaml against chora-validator
- [x] Implement behaviors/interfaces
- [x] Emit onboarding signal once complete

## Validation Log
- 2025-10-05 15:05: Manifest validation via `mcp-orchestrator manifest-validate manifests/star.yaml` returned success.
- 2025-10-05 15:05: Behavior specs present with `@behavior` and `@status` tags; `mcp-orchestrator behavior-validate docs/capabilities/behaviors` returned success.
- 2025-10-05 15:05: Value scenarios present; `mcp-orchestrator scenario-validate manifests/star.yaml` returned success for `mcp.registry.manage.create-doc` with guide and test references.
- 2025-10-05 15:05: Pytest run: all tests passed.

## Notes
- Manifest enriched with tags, dependencies (tooling/runtime), and telemetry signal `SIG.capability.mcp.registry.onboard`.
- Behavior definitions added under `docs/capabilities/behaviors/` using Gherkin for `MCP.REGISTRY.MANAGE`.
- Value scenario `mcp.registry.manage.create-doc` added with guide and stub test; will connect to full automation in CI.

## Status
- complete (Release A onboarding tasks complete; telemetry stubs scheduled for next release)
- 2025-10-06T18:29:30Z: CI workflow added () and validators passing.
  - manifest-validate: OK
  - behavior-validate: OK
  - scenario-validate: OK
  - pytest: OK
- 2025-10-06T18:30:02Z: Scenario status set to ready (guide/tests validated).
