# Liminal Bundle (Release B)

This directory will contain a bundle consumable by the Chora Liminal inbox prototype.

Suggested contents
- `manifests/star.yaml`
- `docs/reference/overview.md`
- `docs/reference/signals/SIG-capability-onboard.md` (or extracted snippet)
- `var/telemetry/events.jsonl`

Packaging
- A simple `.zip` of the repo subset is sufficient for prototype testing.
- Example:
  ```bash
  zip -r var/bundles/liminal/mcp-orchestration-bundle.zip \
    manifests/star.yaml \
    docs/reference/overview.md \
    docs/reference/signals/SIG-capability-onboard.md \
    var/telemetry/events.jsonl
  ```
