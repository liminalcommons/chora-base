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
