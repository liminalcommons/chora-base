# Consuming Chora Compose: LLM Agent Playbook

**Date:** 2025-10-13
**Maintainer:** Chora Compose Core
**Primary Persona:** Autonomous LLM developer agent integrating Chora ecosystem repos

---

## TL;DR (Agent Facing)

| Agent Question | Key Answer | Next Action |
| --- | --- | --- |
| Why should I call Chora Compose? | It turns declarative configs into fully generated artifacts so sibling repos stay configuration-driven. | Confirm a content or artifact config exists (or create one) and call the `compose` CLI/API. |
| What do I provide? | Validated content + artifact configs, source materials, and storage target hints. | Fetch or generate configs, ensure schemas at `schemas/*` validate, prepare source payloads. |
| What do I get back? | A composed artifact bundle (files, stdout summaries, run metadata) plus contract-compliant status events. | Write artifacts to the contract location, emit Ack gate signal, continue workflow. |

---

## Scenario: Brief for an LLM Engineer-Agent

You receive an instruction from `chora-platform` to publish refreshed onboarding docs. The platform exposes the target artifact manifest and links to content configs. Your mandate:

1. Pull the latest `chora-compose` release (Poetry project `chora-compose`, module `chora_compose`).
2. Evaluate configs under `configs/` to confirm they reference the correct source materials.
3. Run the compose pipeline to generate artifacts into the repo-local `dist/` and publish manifest metadata.

---

## Value Proposition for Ecosystem Repos

- **Declarative-first:** Converts JSON/Pydantic configs into consistent documentation, specs, or auxiliary artifacts; no ad hoc scripting required downstream.
- **Composable pipeline:** Separates content fragments (`configs/content`) from final artifacts (`configs/artifact`), enabling other repos to mix and reuse outputs.
- **Validated contracts:** Ships schemas at `schemas/content/v3.1` and `schemas/artifact/v3.1` so consuming agents can verify configurations before execution.
- **Generator hub:** Provides Jinja2 and Demonstration generators today, with roadmap slots for template fill, code generation, and BDD scenarios.
- **Workflow ready:** Emits structured run summaries suitable for DRSO gates (status, coverage, release acknowledgements).

---

## Integration Contract (What You Must Honor)

1. **Inputs**
   - Content configs referencing templates, source data selectors, and generation patterns.
   - Artifact configs linking child content configs and defining output destinations.
   - Source materials (files, APIs) accessible relative to repo root or supplied providers.
2. **Execution**
   - Invoke via CLI (`poetry run chora-compose compose <artifact-config>`) or Python API (`from chora_compose.core.composer import ArtifactComposer`).
   - Provide storage backend hints (default `EphemeralStorageManager`; swap when integrating persistent targets).
3. **Outputs**
   - Artifact files written to configured output directories.
   - Run metadata (status, duration, component list) available for telemetry collection.
   - Optional manifest JSON for downstream discovery (see `dist/latest_run_manifest.json`).

---

## Ecosystem Fit: Where Chora Compose Sits

```
chora-workspace (coordination)
   └─ chora-platform (standards, discovery)
        └─ mcp-orchestration (manifest + lifecycle)
             └─ mcp-n8n (workflow automation)
                  └─ chora-compose (content + artifact generation)
```

- **Produces:** Typed artifacts, run manifests, capability descriptors.
- **Consumes:** Configurations registered in chora-platform, orchestration prompts from mcp-n8n, storage providers from sibling repos (future).
- **Signals:** Lifecycle events for DRSO gates, publishing `Ack` readiness once artifacts land.

---

## Agent Playbooks

### 1. Bootstrap a New Consumer Repo
1. Clone both the target repo and `chora-compose`.
2. Copy or scaffold required configs using templates in `dev-docs/templates`.
3. Validate configs with `poetry run chora-compose validate <path>`.
4. Register a manifest snippet (see Machine-Readable Summary) with `chora-platform`.
5. Execute `compose` and store artifacts under the consumer repo’s agreed directory (`docs/`, `dist/`, etc.).

### 2. Refresh Existing Artifacts on Schedule
1. Pull latest tags for `chora-compose` (check `CHANGELOG.md` for breaking updates).
2. Re-run validation; watch for schema version bumps.
3. Execute artifact generation; capture run metadata.
4. Emit change signal via `mcp-orchestration` API including run manifest hash.

### 3. Extend Generator Capabilities
1. Inspect current generators in `src/chora_compose/generators/`.
2. Implement new generator following `BaseGenerator` contract.
3. Add schema extension if new generator requires patterns.
4. Provide tutorial/update docs under `docs/how-to/generation/`.
5. Publish release notes via `release-notes-*` flow and alert ecosystem.

---

## Guardrails Before You Execute

- ✅ Schema validation passes (`schemas/content|artifact/v3.1`).
- ✅ Source resolution checks succeed (use `ConfigLoader.preview_sources()`).
- ✅ Storage manager target writable (default ephemeral OK for local use).
- ✅ Tests updated if generator behavior changes (`tests/`).
- ✅ Telemetry hooks configured to notify `mcp-orchestration` on success/failure.

If any condition fails, abort and raise an alert in the platform change channel.

---

## Prompt Scaffolding for LLM Agents

```text
System Prompt Snippet:
- You are the integration agent responsible for running Chora Compose against validated configs.
- Always verify schema compliance before generation.
- Emit lifecycle events after each compose run using the manifest template.

User Prompt Template:
<goal>Generate [artifact-id] using configs at [path], targeting release gate [gate-id].</goal>
<constraints>
  - Use generator: [jinja2|demonstration|custom].
  - Source materials located at [relative-paths].
  - Output must land in [repo/subdir].
</constraints>
<verification>
  - Validate configs.
  - Show run summary (artifact path, generator used, hash).
  - Emit Ack gate payload.
</verification>
```

---

## Machine-Readable Summary (YAML)

```yaml
chora_compose_consumption:
  version: 0.8.0
  persona: llm_developer_agent
  inputs:
    content_config_schema: schemas/content/v3.1/schema.json
    artifact_config_schema: schemas/artifact/v3.1/schema.json
    storage_manager: chora_compose.storage.ephemeral.EphemeralStorageManager
  entrypoints:
    cli: poetry run chora-compose compose <artifact-config>
    python: chora_compose.core.composer.ArtifactComposer
  outputs:
    artifacts_dir: dist/
    manifest: dist/latest_run_manifest.json
    events: drso.lifecycle.compose_run
  dependencies:
    coordinating_repos:
      - chora-platform
      - mcp-orchestration
      - mcp-n8n
  verification_steps:
    - validate_schemas
    - dry_run_preview
    - compose_execute
    - emit_ack_signal
```

---

## Related References

- `README.md` – project overview, quick start.
- `docs/ECOSYSTEM_ANALYSIS.md` – positioning within broader Chora ecosystem.
- `docs/how-to/generation/*` – generator-specific instructions.
- `CHANGELOG.md` – release cadence and backward compatibility notes.
- `schemas/*/` – authoritative contract definitions for configs.
