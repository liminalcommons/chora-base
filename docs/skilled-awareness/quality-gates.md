# Skilled Awareness Package Quality Gates

**Aim:** Define the validation criteria, approval checkpoints, and ownership responsibilities required before declaring a Skilled Awareness Package ready for ecosystem-wide adoption. These guardrails keep the framework solution-neutral while enforcing bar-raising rigor.

---

## 1. Definition of Done per Artefact

| Artefact | Minimum Content Criteria | Verification Method | Owner |
|----------|-------------------------|---------------------|-------|
| Capability Charter | Problem, scope, outcomes, stakeholders, lifecycle plan completed; open questions documented. | Charter peer review (captured in PR/issue). | Capability Owner |
| Protocol Spec | All sections populated with concrete requirements; interfaces cross-linked to schemas; governance policy stated. | Technical design review sign-off (architecture + QA). | Capability Owner / Architect |
| Awareness Guide | At least two operational patterns, decision support checklist, escalation instructions, learning hooks. | Agent ops dry run & transcript attached. | Agent Ops Lead |
| Adoption Blueprint | Dual-path install options (script/manual or reason for omission), verification checklist, rollback plan. | Pilot repo installation with checklist results. | Implementation Champion |
| Traceability Ledger | Snapshot metadata, adoption table seeded, feedback log template in place. | QA validation that ledger includes initial entries + instructions. | Ecosystem Coordinator |

---

## 2. Cross-Cutting Quality Checks

- **Consistency Audit:** Verify terminology matches across documents (e.g., intake types, capability modes). Run markdown lint or manual checklist.
- **Traceability Links:** Each document references the others (Charter ↔ Spec ↔ Guide ↔ Blueprint ↔ Ledger) with relative paths that resolve in the repo.
- **Version Alignment:** Protocol version number updated everywhere (spec header, ledger snapshot, awareness guide prerequisite note).
- **Accessibility:** Headings follow markdown hierarchy, tables have headers, code blocks include info strings for syntax highlighting.
- **Diátaxis Alignment:** Sections map to Explanation, How-To, Reference, Tutorial; flag deviations for review.

---

## 3. Approval Matrix

| Decision | Required Approvers | Optional Reviewers | Escalation |
|----------|--------------------|--------------------|------------|
| Charter adoption | Capability Owner + Ecosystem Coordinator | Product/Strategy partner | Governance council |
| Protocol activation | Capability Owner + Architect + QA/Compliance | Security lead | CTO / Technical steering |
| Awareness publication | Agent Ops Lead + Capability Owner | Senior agent users | Ecosystem coordinator |
| Blueprint release | Implementation Champion + Capability Owner | DevOps/tooling | Program management |
| Ledger go-live | Ecosystem Coordinator | All repo representatives | Governance council |

Escalation path should be exercised when approvals block for longer than the agreed SLA (default: 5 business days).

---

## 4. Rollout Checklist

Before announcing availability:

- [ ] Capability Charter merged, version stamped.
- [ ] Protocol Spec approved with recorded decision summary.
- [ ] Awareness Guide validated through live session (notes stored).
- [ ] Adoption Blueprint executed in at least one staging repo; feedback incorporated.
- [ ] Traceability Ledger seeded with pilot repo entry and assigned owner.
- [ ] Inbox entry created (strategic or coordination) to inform the wider ecosystem.
- [ ] Release communication drafted (README update, CHANGELOG note, or coordination broadcast).

---

## 5. Maintenance Cadence

- **Quarterly:** Review charter relevance and ledger completeness; retire outdated actions.
- **On Protocol Changes:** Re-run awareness dry runs, update blueprint verification steps, bump version references.
- **On Adoption Feedback:** Within one sprint, respond in ledger and, if necessary, trigger hotfix cycle (minor version release).

---

## 6. Ownership Registry (Initial)

| Role | Primary Owner | Backup |
|------|---------------|--------|
| Capability Owner | Victor Piper | Codex assistant (document prep) |
| Agent Ops Lead | Codex assistant (temporary) | TBD (future agent team member) |
| Implementation Champion | Victor Piper (pilot repos) | TBD per repo |
| Ecosystem Coordinator | Victor Piper | TBD |
| QA/Compliance Liaison | TBD | — |

Update this table as roles expand; the Traceability Ledger should link back to the current registry.

---

## 7. Open Questions

1. What is the SLA for incorporating ledger feedback into protocol/blueprint updates?
2. How do we integrate automated checks (e.g., CI) to ensure templates stay populated over time?
3. Should we define lightweight metrics (adoption velocity, issue count) to feed back into the charter outcomes?

Capture resolutions in the Capability Charter or future governance documents.

