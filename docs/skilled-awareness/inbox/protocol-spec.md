# Cross-Repository Inbox Skilled Awareness Package
## Protocol Specification

**Version:** 1.0.0
**Status:** Draft (proposed for adoption)
**Maintainer:** Capability Owner (Victor Piper)

---

## 1. Overview
- **Purpose:** Provide a Git-native coordination protocol that standardizes intake, routing, and lifecycle management for cross-repository work across the Liminal Commons ecosystem.
- **Intended Consumers:**
  - Repository maintainers implementing cross-repo coordination.
  - AI agents (Claude, Codex) executing inbox triage and task processing.
  - Ecosystem governance teams tracking strategic proposals and dependencies.
- **Modes of Operation:**
  - **Planning Mode:** Focused on strategic proposals and coordination requests; quarterly and sprint-level cadences.
  - **Execution Mode:** Handles approved implementation tasks through the DDD → BDD → TDD lifecycle.

---

## 2. Design Principles
1. **Git-First Coordination** — All state lives in the repository; no external services required.
2. **Respect Lifecycle Phases** — Strategic, coordination, and implementation workflows align with evidence-based development phases.
3. **Traceability by Default** — Every action emits structured events and maintains audit trails.
4. **Agent Accessibility** — Protocol must be operable via machine-readable instructions with clearly defined command patterns.
5. **Composable Adoption** — Downstream repos may enable protocol components incrementally while retaining compatibility.

---

## 3. Functional Requirements
- **FR-1:** Support three intake types (strategic, coordination, implementation) with distinct review cadences and schemas.
- **FR-2:** Provide deterministic directory structure enabling queue states: `incoming`, `active`, `completed`, `ecosystem`, `coordination`.
- **FR-3:** Maintain JSON schemas for each intake type; validation must succeed before progression.
- **FR-4:** Emit append-only JSONL events capturing state transitions with `CHORA_TRACE_ID`.
- **FR-5:** Offer triage workflow that aligns with development phases, including escalation paths.
- **FR-6:** Integrate with capability-based routing per repository (e.g., `CAPABILITIES/<repo>.yaml`).
- **FR-7:** Document operational patterns for AI agents (commands, move instructions, event emission).
- **FR-8:** Provide adoption instructions and verification steps for downstream repositories.

---

## 4. Interfaces and Artifacts
- **Inputs:**
  - Markdown documents for strategic proposals (`ecosystem/proposals/`).
  - JSON payloads for coordination requests and implementation tasks (`incoming/coordination/`, `incoming/tasks/`).
  - Capability descriptors (`coordination/CAPABILITIES/<repo>.yaml`).
- **Outputs:**
  - Event log (`coordination/events.jsonl`).
  - Status snapshots (`coordination/ECOSYSTEM_STATUS.yaml`).
  - Completed artifacts stored in `completed/` with archival metadata.
- **CLI Hooks / Commands:**
  - Standard shell commands for listing, moving, and validating files (e.g., `ls`, `cat`, `mkdir`, `mv`).
  - Optional script hooks (future automation) for schema validation or reporting.

---

## 5. Operational Workflow
### Lifecycle Stages
1. **Intake:** Item added to `incoming/` (coordination or tasks) or `ecosystem/proposals/`.
2. **Review:** Item evaluated at appropriate cadence (quarterly, sprint, continuous).
3. **Activation:** Accepted items moved to `active/`; trace ID ensured.
4. **Execution:** DDD → BDD → TDD phases executed; progress checkpoints recorded.
5. **Completion:** Results stored and summarized in `completed/`; events emitted.
6. **Feedback:** Lessons captured, ledger updated (see SAP ledger).

### Decision Branches
- **Planning vs Execution Mode:**
  - Planning mode items require coordination review before activation.
  - Execution mode tasks can be activated once prerequisites met.
- **Escalation Paths:** If capability mismatch or resource constraints observed, escalate via coordination request or strategic proposal update.

---

## 6. Governance & Compliance
- **Versioning Policy:** Semantic versioning; patch updates for documentation tweaks, minor for schema or workflow improvements, major for breaking structural changes.
- **Compatibility Guarantees:** Downstream repos implementing `v1.x` must remain compatible with later `v1.y`; major version bump signals migration guide requirement.
- **Audit Requirements:** Event log and status snapshots must be reviewable; adoption ledger to log version and feedback.
- **Security / Privacy Considerations:** Protocol stores coordination data in repository; ensure sensitive information is sanitized before commit.

---

## 7. Reference Materials
- **Schemas:**
  - `inbox/schemas/strategic-proposal.schema.json`
  - `inbox/schemas/coordination-request.schema.json`
  - `inbox/schemas/implementation-task.schema.json`
- **Examples:**
  - `inbox/examples/` (populate as adoption proceeds).
  - `inbox/completed/` records for retrospectives.
- **Related Protocols:**
  - Evidence-Based Development Workflow (DDD/BDD/TDD).
  - Memory system protocols (for event capture).
  - Future Status Protocol (planning).
