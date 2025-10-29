# Skilled Awareness Package Inputs Audit

**Date:** 2025-10-27  
**Stakeholders:** Victor Piper (maintainer), Codex assistant (research + synthesis)

This note captures the current evidence base needed to design the Skilled Awareness Package (SAP) document set. It inventories relevant assets, highlights how the emerging protocol / awareness / blueprint pattern shows up today, and records the open questions we must resolve before drafting templates.

---

## 1. Scope Anchors

- **Inbox prototype:** Everything under `inbox/` (protocol, awareness, schemas, examples).
- **Awareness guidance:** All CLAUDE-specific guides in the repo.
  - `inbox/CLAUDE.md`
  - `static-template/CLAUDE.md`
  - `static-template/tests/CLAUDE.md`
  - `static-template/docker/CLAUDE.md`
  - `static-template/scripts/CLAUDE.md`
- **Blueprint sources:** All files in `blueprints/` ending in `.blueprint`, plus supporting docs (e.g., `blueprints/CLAUDE.md.blueprint`, `blueprints/AGENTS.md.blueprint`).

---

## 2. Asset Inventory

| Path | Role | Audience | Key Patterns Observed | Gaps / Risks |
|------|------|----------|-----------------------|--------------|
| `inbox/INBOX_PROTOCOL.md` | Protocol | Maintainers & coordinators | Full life-cycle spec (three intake types, schemas, routing, cadence). | Lacks explicit linkage to adoption steps; status modes implicit. |
| `inbox/IMPLEMENTATION_SUMMARY.md` | Protocol summary | Stakeholders & reviewers | High-level synopsis of goals, deliverables, dependencies. | Needs mapping to future Capability Charter template. |
| `inbox/INTAKE_TRIAGE_GUIDE.md` | Awareness (process) | Human + AI operators | Step-by-step triage workflow with decision helpers. | Duplicates content from protocol in places; could be merged into SAP awareness guide. |
| `inbox/CLAUDE.md` | Awareness (Claude) | Claude Code | Concrete command sequences, move/emit event patterns, checkpoint prompts. | Assumes manual directory moves; no blueprint automation to back it. |
| `inbox/schemas/*.json` | Reference | Tooling, validation | JSON schema per intake type. | Versioning + governance rules not stated. |
| `inbox/active`, `incoming`, `coordination`, `ecosystem`, `completed` (README + examples) | Awareness support | Operators | Directory-level instructions, examples, event logs. | Need consistent metadata (status, owner, last update). |
| `static-template/CLAUDE.md` | Awareness exemplar | Claude Code (project-level) | Progressive context loading, workflow integration, checkpoints. | Example-only; not flagged as template contract. |
| `static-template/tests/CLAUDE.md` | Awareness exemplar | Claude test work | Structured prompts for test generation, fixture usage patterns. | No companion protocol describing testing requirements. |
| `static-template/docker/CLAUDE.md` | Awareness exemplar | Claude Docker tasks | Multi-stage Docker pattern, request templates. | Relies on implicit Dockerfile standards. |
| `static-template/scripts/CLAUDE.md` | Awareness exemplar | Claude automation tasks | Script request template, best practices. | Underlying scripting protocol (requirements, governance) missing. |
| `blueprints/AGENTS.md.blueprint` | Blueprint | Repo adopters | Generates base AGENTS instructions with Diátaxis mapping. | No explicit tie to protocol/awareness docs that inform it. |
| `blueprints/CLAUDE.md.blueprint` | Blueprint | Repo adopters using Claude | Produces Claude guide aligned with evidence-based lifecycle. | Depends on static-template CLAUDE exemplars but relationship undocumented. |
| `blueprints/*.blueprint` (project scaffold) | Blueprint | Template adopters | Project generation scripts covering code, docs, config. | Blueprint concept implicit—no Capability Charter describing promises/limits. |

---

## 3. Capability Coverage Matrix

| Capability | Protocol Assets | Awareness Assets | Blueprint Assets | Notes |
|------------|----------------|------------------|------------------|-------|
| **Cross-repo Inbox** | `inbox/INBOX_PROTOCOL.md`, `inbox/IMPLEMENTATION_SUMMARY.md`, schemas | `inbox/CLAUDE.md`, `inbox/INTAKE_TRIAGE_GUIDE.md`, directory READMEs | **Missing** (only manual instructions) | High-value SAP candidate; blueprint needs install/upgrade story. |
| **Project Bootstrap (chora-base template)** | Implicit in `CHANGELOG.md`, `docs/` standards | `static-template/CLAUDE.md` + nested variants | `blueprints/*.blueprint` | Protocol needs formalization (what the template guarantees). |
| **Testing Enablement** | None explicit (scattered in docs) | `static-template/tests/CLAUDE.md`, tests/AGENTS (via blueprint) | Partial (tests generated with project) | Define testing protocol (coverage targets, workflows) to complete SAP. |
| **Docker Operations** | None explicit | `static-template/docker/CLAUDE.md` (plus docker/AGENTS from blueprint) | Implicit (Docker files emitted when option enabled) | Should capture protocol for container strategy, align blueprint toggles. |
| **Automation Scripts** | None explicit | `static-template/scripts/CLAUDE.md` | Scripts emitted in template | Need protocol for scripting standards (linting, safety) to complete SAP. |

---

## 4. Immediate Follow-Ups

1. **Decide canonical storage** for SAP documents (likely `docs/reference/skilled-awareness/` with per-capability subdirectories).
2. **Clarify protocol vs awareness boundaries**—e.g., what content belongs in Protocol Spec vs Awareness Guide to prevent duplication.
3. **Determine blueprint deliverables** for inbox package (install script, directory manifest, verification checklist).
4. **Document governance rules** for schemas and versioning (in Protocol Spec template).
5. **Collect adopter feedback** (if any) on current inbox prototype to inform gap analysis.

Captured background questions and observations will feed directly into the document templates and Capability Charter draft.

