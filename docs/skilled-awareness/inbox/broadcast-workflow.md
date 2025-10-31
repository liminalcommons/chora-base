# Weekly Ledger Broadcast Workflow

**Goal:** Ensure the cross-repo inbox ledger informs the ecosystem on a predictable cadence via the coordination channel.

---

## Cadence
- **Frequency:** Weekly (default: Mondays)
- **Responsible:** Ecosystem Coordinator (Victor Piper)
- **Artifacts:** `docs/reference/skilled-awareness/inbox/ledger.md`, `inbox/coordination/ECOSYSTEM_STATUS.yaml`, broadcast coordination request/update.

---

## Steps
1. **Ledger Review**
   - Read most recent adoption entries and feedback log.
   - Update adoption table rows with new statuses or notes.
   - Confirm upcoming actions are accurate; adjust dates/owners as needed.

2. **Status Summary Generation**
   - Extract key highlights (new adoptions, blockers, feedback).
   - Append a weekly section to `inbox/coordination/ECOSYSTEM_STATUS.yaml` under `sap_inbox` (create section if absent) using format:
     ```yaml
     sap_inbox:
       - week: 2025-11-03
         summary: >
           One-line headline.
         details:
           - item: "Adoption progress"
             status: "In progress"
             notes: "..."
           - item: "Upcoming actions"
             status: "Planned"
             notes: "..."
     ```

3. **Broadcast via Inbox**
   - Create/update a coordination request (or weekly update) referencing the status summary.
   - Include links to ledger, pilot plan, and open questions.
   - Tag affected repos in the broadcast content.

4. **Follow-Up**
   - Track responses or acknowledgements.
   - Log any new tasks or blockers back into the ledger feedback section.

---

## Schedule Reminders
- Add personal calendar reminder for Monday 10:00 local time.
- If delayed, reschedule within same week to maintain cadence.
- Missed updates should be noted in the next broadcast with explanation.

---

## Future Automation Ideas
- Script to parse ledger and render summary YAML automatically.
- GitHub Action or cron job to remind coordinator if update not committed by end-of-day Monday.
- Dashboard integration pulling from `ECOSYSTEM_STATUS.yaml`.

