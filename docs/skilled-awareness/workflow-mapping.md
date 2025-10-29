# Skilled Awareness Package Workflow Map

**Objective:** Describe how the SAP document set fits into the broader lifecycle— from capability ideation through adoption and monitoring—so stakeholders can coordinate work without presupposing specific tooling.

---

## 1. Lifecycle Overview

| Phase | Primary Outputs | Drivers | Entry Criteria | Exit Criteria |
|-------|-----------------|---------|----------------|---------------|
| **Discovery** | Capability Charter (draft) | Product/Governance | Clear problem statement, sponsors identified | Charter approved for protocol design |
| **Specification** | Protocol Spec (draft), Schema updates | Capability Maintainer | Charter approved, dependencies known | Protocol reviewed, acceptance criteria agreed |
| **Awareness Design** | Awareness Guide (draft), training hooks | Agent Ops team | Protocol near-final, operator personas identified | Guide piloted with agents (dry run) |
| **Adoption Planning** | Adoption Blueprint (draft), install scripts (optional) | Repo Maintainers | Awareness guide validated, installation surface mapped | Blueprint tested in at least one staging repo |
| **Rollout & Monitoring** | Traceability Ledger (active), feedback loop | Ecosystem Coordination | Blueprint approved, early adopters onboard | Ledger populated, feedback collection running |
| **Continuous Improvement** | Versioned updates, retrospectives | Maintainers + adopters | Ledger shows adoption/feedback | Next iteration prioritized or capability sunset planned |

---

## 2. Roles and Responsibilities

- **Capability Owner:** shepherds charter, owns protocol spec, coordinates reviews.
- **Agent Operations Lead:** ensures awareness guide reflects real workflows; schedules agent dry runs.
- **Implementation Champion (per repo):** adapts adoption blueprint to local context; executes verification steps.
- **Ecosystem Coordinator:** maintains traceability ledger, watches cross-repo impacts, escalates blockers.
- **QA / Compliance Partner:** validates that protocol and blueprint meet organizational policy (security, data handling, etc.).

Each role may be held by the same person in smaller teams; responsibilities should still be tracked explicitly.

---

## 3. Review Cadence

| Artefact | Review Type | Facilitator | Timing | Checklist Highlights |
|----------|-------------|-------------|--------|----------------------|
| Capability Charter | Alignment Review | Capability Owner | Once per capability, revisit quarterly | Problem clarity, success metrics, scope boundaries |
| Protocol Spec | Technical Design Review | Architecture / Maintainer | Before first adoption & on major revisions | Interface completeness, failure modes, governance |
| Awareness Guide | Agent Playtest | Agent Ops Lead | Before rollout, after significant workflow change | Decision trees usable, escalation paths clear |
| Adoption Blueprint | Pilot Retrospective | Implementation Champion | After first install & major updates | Installation friction, verification coverage |
| Traceability Ledger | Ecosystem Sync | Coordinator | Bi-weekly or sprintly | Adoption status accuracy, feedback processing |

---

## 4. Workflow Integrations

- **Documentation-Driven Design (DDD):** Capability Charter seeds DDD artefacts; link charter sections to DDD templates so reasoning stays consistent.
- **Evidence-Based Lifecycle (BDD/TDD):** Adoption blueprint should reference relevant workflow guides (e.g., for tests, docker) ensuring protocol requirements tie to executable practices.
- **Inbox Coordination:** When a new capability is proposed, log a strategic or coordination item in the inbox prototype to trigger cross-repo awareness.
- **Memory/Knowledge Systems:** Store final documents in the repo, but also emit summary checkpoints into `.chora/memory/` (or equivalent) so AI agents ingest the latest instructions automatically.

---

## 5. Adoption Flow (Textual Swimlane)

```
Stakeholder        Activity
--------------     ------------------------------------------------------------
Capability Owner   Draft charter → collect stakeholder input → seek approval
Architecture       Review protocol spec → ensure compliance with ecosystem standards
Agent Ops          Run tabletop exercise with awareness guide → capture refinements
Repo Maintainer    Execute blueprint in staging → document friction points
QA/Compliance      Validate protocol & blueprint → sign off or request changes
Coordinator        Update ledger → communicate readiness to ecosystem
Adopters           Install capability → perform verification → report back
```

---

## 6. Tooling Suggestions (Optional)

While tooling remains implementation-specific, consider the following patterns to operationalize the workflow:

- **Checklists as Code:** Use markdown checklists committed alongside the templates to enforce sign-offs.
- **Automation Hooks:** Optional scripts can read the ledger to generate status dashboards without changing the protocol.
- **Template Validation:** Use CI to ensure required sections exist in each document (e.g., via markdown linting rules).
- **Inbox Notifications:** Emit inbox events when protocol versions change or blueprint updates are released.

---

## 7. Outstanding Questions

1. How do we synchronize ledger updates with external project trackers (GitHub Projects, Jira, etc.)?
2. Should blueprints include optional Copier tasks for bulk installation across repos?
3. Do we need an explicit escalation protocol when adoption stalls (e.g., 60 days with no progress)?

Document answers in the Capability Charter or an ecosystem governance note as they emerge.

