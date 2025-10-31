# Skilled Awareness Package Ledger: Cross-Repository Inbox

## 1. Snapshot
- **Protocol Version:** 1.0.0 (draft)
- **Maintainer:** Victor Piper (Capability Owner)
- **Last Review:** 2025-10-27

---

## 2. Adoption Table

| Repository | Protocol Version | Awareness Installed | Blueprint Status | Notes | Last Updated |
|-----------|------------------|----------------------|------------------|-------|--------------|
| chora-base | 1.0.0 (draft) | Yes (prototype) | In Progress | SAP documents in preparation; awaiting automation feedback. | 2025-10-27 |
| chora-compose | — | No | Not Started | Candidate for second pilot; access confirmed, gathering readiness details. | 2025-10-27 |

_Add new rows as repositories adopt the package._

---

## 3. Feedback Log

- **Date:** 2025-10-27
  **Source:** chora-base (prototype)
  **Summary:** Manual installation exposes need for automation script and explicit schema validation instructions.
  **Action Taken:** Captured in adoption blueprint as future enhancement.
- **Date:** 2025-10-27
  **Source:** Inbox SAP dry run
  **Summary:** Executed end-to-end dry run (triage → activation → completion). Noted requirement to initialize `events.jsonl` and confirmed awareness guide covers escalation.
  **Action Taken:** Updated dry-run checklist and adoption blueprint follow-up notes; broadcast template skeleton added.

_Record feedback chronologically with concrete follow-up actions._

---

## 4. Upcoming Actions

- [ ] Prepare automation concept (`install-inbox.sh`) for Option B in adoption blueprint. (Owner: TBD, Due: —)
- [x] Schedule agent dry run using awareness guide post-document finalization. (Owner: Codex assistant, Due: 2025-10-30) — **Completed 2025-10-27 (documented in dry-run checklist)**
- [ ] Identify next pilot repository (e.g., chora-composer or ecosystem manifest). (Owner: Victor Piper, Due: 2025-11-05)
- [ ] Collect readiness details for chora-compose (maintainers, capabilities, timeline). (Owner: Victor Piper, Due: 2025-11-01) — **In progress**
- [ ] Publish first weekly status summary to `inbox/coordination/ECOSYSTEM_STATUS.yaml`. (Owner: Victor Piper, Due: 2025-11-03) — **Drafted placeholder (2025-10-27)**
- [ ] Review and approve broadcast template with Victor. (Owner: Victor Piper, Due: 2025-10-31) — **Template refined 2025-10-27; pending approval**
- [ ] Review new SAP roadmap and align Phase 1 tasks. (Owner: Victor Piper, Due: 2025-10-31) — **Roadmap updated 2025-10-28; awaiting approval**

_Update checkboxes as actions complete; add new items as needed._

---

## 5. Change History

- **2025-10-27:** Initial ledger created as part of SAP documentation set (version 1.0.0 draft).
- **2025-10-27:** Dry run executed; events logged and broadcast template drafted.
