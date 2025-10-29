# chora-base Skilled Awareness Package Roadmap

**Purpose:** Provide an adopter-centric plan for evolving chora-base so every major capability ships as a first-class Skilled Awareness Package (SAP). The roadmap covers two parallel goals:
- Mature the SAP framework itself (governance, tooling, and adoption support).
- Migrate existing chora-base features to achieve 100% coverage within the new framework.

Reference assets:
- SAP templates and workflow: `docs/reference/skilled-awareness/document-templates.md`, `docs/reference/skilled-awareness/workflow-mapping.md`
- Inbox SAP implementation: `docs/reference/skilled-awareness/inbox/`

---

## 1. Current Adopter Experience

| Capability | What adopters receive today | SAP coverage status | Adopter pain points |
|------------|----------------------------|---------------------|---------------------|
| Project bootstrap (Copier template + blueprints) | Rich scaffolding, docs, CI defaults via `blueprints/` and `static-template/` | Protocol missing, awareness partial (claude guides), blueprint implicit | Hard to reason about guarantees, versioning, and upgrade paths; no single source for expectations |
| Testing enablement | Test suites, fixtures, coverage defaults, CLAUDE test patterns | Protocol absent, awareness partial, blueprint implicit | Adopters unclear on required coverage, when to enforce metrics, or how to extend |
| Docker + deployment | Dockerfiles, optional compose, docker CLAUDE guide | Protocol absent, awareness partial, blueprint implicit | No documented lifecycle for enabling/disabling Docker options; inconsistent adoption |
| Automation scripts & justfile | Scripts emitted in template, CLAUDE patterns | Protocol absent, awareness partial | Standards for safety/idempotency assumed rather than contractually defined |
| Cross-repo inbox (prototype) | Inbox directory + docs in `inbox/` | **Full SAP (pilot)** | Ready for adoption pilot; weekly broadcast cadence defined |
| Memory system (A-MEM) | Static templates, docs, optional feature toggle | SAP not yet defined | Needs structured guidance for when/how to enable and maintain |

Key insight: adopters already benefit from strong scaffolding, but guidance is fragmented. SAP formalizes the promise so human and AI operators receive consistent contracts, install instructions, and lifecycle transparency.

---

## 2. SAP Maturity Gaps

### Framework-Level Gaps
- **Governance consolidation:** Templates live in `docs/reference/skilled-awareness/`, but framework roles, versioning policy, and change management still rely on informal coordination. Need a canonical charter + RACI.
- **Automation & validation:** Adoption remains LLM/manual. No automated checks ensure SAP artefacts stay populated or linked. CI support and linting should enforce template completeness.
- **Visibility:** Ledger + weekly broadcast workflow exists for inbox only. Need cross-capability dashboarding and a central SAP index for adopters.
- **Tooling pathways:** No scripts or Copier hooks yet for installing SAP bundles; blueprint integration points remain manual.

### Capability Coverage Gaps
- **Project bootstrap:** Must produce full SAP: protocol clarifying guarantees (e.g., dev lifecycle, optional features), awareness for both Claude & human maintainers, explicit adoption blueprint (Copier usage, upgrade process), ledger tracking adopters.
- **Testing enablement:** Define testing protocol (coverage thresholds, test types), awareness (update `static-template/tests/CLAUDE.md` + AGENTS), blueprint for enabling/disabling advanced testing packages, ledger row.
- **Docker operations:** Document lifecycle (on/off toggles, security expectations), awareness updates, adoption blueprint for enabling Docker features, ledger tracking.
- **Automation scripts:** Formalize scripts protocol (idempotency, safety), awareness, blueprint for customizing script sets.
- **Memory system:** Create SAP to describe A-MEM architecture, agent behaviors, install steps, and adoption tracking.
- **Remaining optional features:** Any other feature toggles (docs packages, release workflows) require SAP treatment to achieve parity.

---

## 3. Roadmap Phases

### Phase 1 – Framework Hardening (2025-10 → 2025-11)
- **Objectives:** Establish governance, automate guardrails, finalize inbox SAP rollout.
- **Key Deliverables:**
  - SAP governance charter + RACI matrix.
  - CI or lint checks ensuring new SAP docs include required sections.
  - Weekly broadcast cadence live; ledger templated for multi-capability tracking.
  - Copier-to-blueprint cleanup across guidance, user docs, and tooling (✓ docs updated; release notes flagged as legacy).
  - Victor sign-off on broadcast template; adoption pilot kickoff for inbox (chora-compose).
- **Success Metrics:** inbox SAP pilot complete; automated checks running; stakeholders subscribe to broadcast cadence.

### Phase 2 – Core Capability Migration (2025-11 → 2026-01)
- **Objectives:** Bring core chora-base offerings (project bootstrap, testing, Docker) into SAP parity.
- **Key Deliverables:**
  - SAP document sets for project bootstrap, testing, Docker operations.
  - Awareness guides updated and referenced in root `AGENTS.md` / `CLAUDE.md`.
  - Adoption blueprints integrated into Copier usage docs; ledger entries for adopters.
  - Optional automation scripts: e.g., `scripts/install-sap-bundle.sh` for applying capability packages.
- **Success Metrics:** Core capabilities flagged as SAP-compliant (ledger entries), adopter pilots confirm reduced onboarding friction, upgrade guidance updated.

### Phase 3 – Extended Capability Coverage (2026-01 → 2026-03)
- **Objectives:** Cover remaining optional features (automation scripts, memory system, docs workflows) and align examples.
- **Key Deliverables:**
  - SAP sets for automation, memory system (A-MEM), doc workflows (e.g., Diátaxis).
  - Examples in `examples/` updated or annotated to reflect SAP adoption status.
  - Cross-capability SAP index published for adopters (linking to each capability directory).
- **Success Metrics:** Ledger shows 100% capability coverage; adopters confirm clarity via feedback survey; documentation references SAP index.

### Phase 4 – Automation & Ecosystem Integration (2026-03 → 2026-05)
- **Objectives:** Reduce manual burden, enable multi-repo installs, and integrate with ecosystem tooling.
- **Key Deliverables:**
  - CLI or Copier extensions to apply SAP bundles (install/uninstall/upgrade).
  - Dashboard or status page reading ledger + events for real-time visibility.
  - Automated reminders for broadcasts, ledger updates, and SAP review cadences.
- **Success Metrics:** Installation time reductions, broadcast automation in place, ecosystem stakeholders rely on dashboard.

---

## 4. Dependencies & Coordination
- **Stakeholders:** Victor (Capability Owner), Codex/Claude agents (Agent Ops), adopter maintainers (e.g., chora-compose), future governance reps.
- **Tools & Repos:** chora-base, adopter repos (examples, chora-compose, ecosystem-manifest), CI pipelines once established.
- **Communication:** Weekly broadcast (using template), inbox coordination requests, ledger updates per capability.
- **Risks:** Manual workload before automation; adoption drift in example repos; cross-repo coordination time.

---

## 5. Tracking & Next Actions
- Maintain ledger entries per capability with progress checkboxes.
- Align with Victor to approve broadcast template and Phase 1 plan.
- Schedule inbox SAP pilot execution window (2025-11-01 → 2025-11-05).
- Open governance charter draft issue referencing this roadmap.

This roadmap will evolve as adoption feedback arrives; update the ledger and broadcast notes whenever phases shift or deliverables are completed.
