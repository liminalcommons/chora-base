# AGENTS Guidance — mcp-orchestration

Scope: applies to the entire repo.

Coding & Docs
- Keep changes minimal and focused on the requested task.
- Prefer repository-relative paths in docs and manifests.
- Use capability IDs like `mcp.registry.manage` and behavior IDs like `MCP.REGISTRY.MANAGE`.
- Value scenarios belong in the manifest under `value_scenarios` and must reference docs and tests.

Validation & CI
- Local: run `PYTHONPATH=src` for CLI and tests.
- Required commands:
  - `python -m mcp_orchestrator.cli manifest-validate manifests/star.yaml`
  - `python -m mcp_orchestrator.cli behavior-validate docs/capabilities/behaviors`
  - `python -m mcp_orchestrator.cli scenario-validate manifests/star.yaml`
  - `pytest -q`
- CI workflow: `.github/workflows/chora-ci.yml` runs validators and tests without installing the package, using `PYTHONPATH=src`.

Style
- Python: follow existing structure; no one-letter variable names.
- Tests: place value scenario tests under `tests/value-scenarios/`.

Change Signals
- Update `docs/reference/signals/SIG-capability-onboard.md` with validator/test outcomes and status.

