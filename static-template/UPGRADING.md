# Upgrading {{ project_name }}

**Project**: {{ project_name }}  
**Template Version**: chora-base {{ template_version }}  
**Generated**: {{ generation_date }}

This guide helps you keep {{ project_name }} aligned with the latest chora-base blueprints and Skilled Awareness Packages (SAPs).

---

## Quick Reference

1. **Review announcements**
   - Read the weekly inbox broadcast (`inbox/coordination/broadcasts/`) for upcoming changes.
   - Check the adoption ledger (`docs/reference/skilled-awareness/**/ledger.md`) for capability updates.
2. **Plan upgrades**
   - Identify impacted SAPs (e.g., inbox, testing, Docker).
   - Open each capability’s adoption blueprint for migration steps.
3. **Execute upgrades**
   - Pull blueprint updates from the chora-base repository (or cherry-pick relevant changes).
   - Apply changes manually or with helper scripts, following SAP instructions.
   - Update documentation and awareness guides as required.
4. **Validate**
   - Run automated tests (`./scripts/setup.sh && pytest`, `just test`).
   - Emit event logs or checkpoint summaries if needed.
5. **Report status**
   - Append notes to the adoption ledger.
   - Share highlights in the next weekly broadcast.

---

## Pre-Upgrade Checklist

Before making changes:

- [ ] Commit or stash all local work (`git status` should be clean).
- [ ] Create a safety branch (`git checkout -b upgrade-YYYYMMDD`).
- [ ] Capture current state in `docs/reference/skilled-awareness/**/ledger.md`.
- [ ] Review recent broadcasts for blockers or dependency changes.
- [ ] Ensure virtual environment and tooling are up to date (`./scripts/setup.sh`).

Optional backup:

```bash
git tag backup-before-upgrade-$(date +%Y%m%d)
```

---

## Upgrade Workflow

1. **Sync Blueprint Changes**
   - Pull latest chora-base main branch.
   - Inspect `blueprints/` and `static-template/` for updates related to your project type.
   - For complex updates, diff against prior release notes in `CHANGELOG.md`.

2. **Apply Capability SAP Updates**
   - For each capability you use (e.g., inbox, testing, Docker, memory):
     - Open the capability’s adoption blueprint (`docs/reference/skilled-awareness/<capability>/adoption-blueprint.md`).
     - Follow migration steps (file updates, new scripts, awareness guide edits).
     - Record actions and outcomes in the capability ledger.

3. **Regenerate Affected Files**
   - When a blueprint changed, re-render the target file by copying from chora-base or re-running helper scripts.
   - Verify placeholders (e.g., `{{ project_name }}`) are replaced; no `{{ ... }}` tokens should remain.

4. **Update Awareness Guides**
   - Refresh `AGENTS.md`, `CLAUDE.md`, and any nested guides to reflect new workflows.
   - For inbox or coordination updates, emit events (`inbox/coordination/events.jsonl`) as appropriate.

5. **Run Validation Suite**
   ```bash
   ./scripts/setup.sh
   pytest
   pre-commit run --all-files
   just test    # if available
   ```

6. **Document Results**
   - Summarize changes in the adoption ledger.
   - Prepare a note for the weekly broadcast (blockers, wins, next steps).

---

## Post-Upgrade Checklist

- [ ] Tests and linting pass.
- [ ] Documentation updated (README, changelog, SAP artefacts).
- [ ] Awareness guides confirm new behaviors.
- [ ] Ledger entry added/updated with outcome and version.
- [ ] Weekly broadcast draft prepared (`inbox/coordination/broadcasts/`).
- [ ] Tag or release prepared if appropriate.

Optional celebratory command:

```bash
just celebrate-upgrade
```

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Conflicts when applying blueprint changes | Manually merge and note decisions in ledger; consider using git mergetool. |
| Tests failing after upgrade | Re-run setup, review change logs, consult SAP protocol for capability-specific fixes. |
| Awareness guide out of sync | Update guides immediately and notify operators via broadcast. |
| Unsure which SAP changed | Check weekly broadcast summary or compare adoption ledger versions. |

---

## Additional Resources

- `docs/reference/skilled-awareness/` – Capability charters, protocols, and adoption blueprints.
- `CHANGELOG.md` – High-level release notes across chora-base versions.
- Inbox broadcasts (`inbox/coordination/broadcasts/`) – Weekly status updates.
- Template roadmap (`docs/reference/skilled-awareness/chora-base-sap-roadmap.md`) – Upcoming SAP work.

Keep the ledger up to date and leverage the weekly broadcast to maintain ecosystem alignment. Upgrades become routine when every capability ships as a well-maintained Skilled Awareness Package.
