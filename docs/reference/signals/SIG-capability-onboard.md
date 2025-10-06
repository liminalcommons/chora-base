# SIG-capability-onboard

Tracks onboarding of manifests/behaviors to Chora platform standards.

## Tasks
- [x] Validate star.yaml against chora-validator
- [x] Implement behaviors/interfaces
- [x] Emit onboarding signal once complete

## Validation Log
- 2025-10-06: Manifest: `PYTHONPATH=src python -m mcp_orchestrator.cli manifest-validate manifests/star.yaml` → success.
- 2025-10-06: Behaviors: `PYTHONPATH=src python -m mcp_orchestrator.cli behavior-validate docs/capabilities/behaviors` → success.
- 2025-10-06: Scenarios: `PYTHONPATH=src python -m mcp_orchestrator.cli scenario-validate manifests/star.yaml` → success for `mcp.registry.manage.create-doc`.
- 2025-10-06: Pytest: `PYTHONPATH=src pytest -q` → all tests passed.

## Notes
- Manifest enriched with tags, dependencies (tooling/runtime), and telemetry signal `SIG.capability.mcp.registry.onboard`.
- Behavior definitions added under `docs/capabilities/behaviors/` using Gherkin for `MCP.REGISTRY.MANAGE`.
- Value scenario `mcp.registry.manage.create-doc` added with guide and stub test; will connect to full automation in CI.

## Status
- closed (Release A onboarding tasks complete; telemetry stubs scheduled for next release)
- CI: `.github/workflows/chora-ci.yml` added; validator and test steps pass locally and will run in PR.
