# MCP Orchestration

Capability provider implementing MCP server lifecycle tooling.

- Aligns with Chora platform standards and validators.
- Publishes manifests/behaviors for discovery and compatibility checks.
- Emits change signals for release and operational events.

## Getting Started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
python scripts/apply_manifest_policy.py manifests/star.yaml
```

See `docs/` for capability descriptions and signals.

## Release Coordination

- Release plans: `docs/reference/release-a-plan.md`, `docs/reference/release-b-plan.md`, `docs/reference/release-plan-b.md`, `docs/reference/release-c-plan.md`
- Repository overview: `docs/reference/overview.md`
- Telemetry how-to: `docs/how-to/telemetry.md`
- Codex agent instructions: `.codex/release-b-prompt.md`
