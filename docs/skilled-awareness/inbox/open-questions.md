# Inbox SAP: Open Questions & Blockers

| # | Question / Blocker | Context | Proposed Resolution | Owner | Status |
|---|--------------------|---------|---------------------|-------|--------|
| 1 | How should ledger updates integrate with ecosystem dashboards or inbox broadcasts? | Charter §5 notes ambiguity; decision affects rollout communication. | Generate a weekly summary from the ledger and append it to `inbox/coordination/ECOSYSTEM_STATUS.yaml`, then broadcast the headline via a coordination request so other repos receive the update. Future automation can read the ledger for dashboards. | Victor Piper | Planned |
| 2 | Do we prioritize building an automated installer (`install-inbox.sh`) before piloting in other repos? | Adoption blueprint Option B placeholder; need feasibility decision. | Rely on LLM-guided manual adoption plus checklist for the first two repos; defer scripted installer until after collecting adoption feedback, then schedule automation as a follow-up. | Victor Piper | Planned |
| 3 | What is the SLA for processing coordination items once inbox adopted (e.g., within 2 business days)? | Protocol lacks explicit timing; impacts governance. | Agents check inbox by default each session; commit to acknowledging new coordination items within one business day and escalate blockers immediately when dependencies arise in other repos. | Ecosystem coordination (Victor Piper for now) | Active |
| 4 | How do we handle sensitive information in coordination requests? | Governance compliance requirement not fully documented. | Operate under trusted-ecosystem assumption but require sanitised summaries in Git; place sensitive details in secure channels and reference them. When collaborators extend beyond trusted circle, draft a formal data-handling addendum. | Capability Owner + QA/Compliance (TBD) | Active |
| 5 | Who serves as Agent Ops Lead long term to maintain awareness guide and conduct dry runs? | Quality gates assign temporary owner; need permanent designation. | Victor Piper remains primary Agent Ops Lead, with a quarterly review to confirm coverage and nominate a backup from future agent team members. | Victor Piper | Active |

Update this table as questions resolve; link to meeting notes or decisions where appropriate.


How should ledger updates integrate with ecosystem? Dashboards are inbox broadcasts.
I don't know please make a suggestion.

Do we prioritize building automated installer?
I'm not sure it depends on what needs to be set up in the adopter repos, I can imagine that adoption is agent driven and so instead of programmatic logic driving installation, we could have LLM intelligent installation and appropriate, documentation, checklist, etc.

What is the SLA for processing coordination items once inbox is adopted?
Because it is Victor interacting with the Kodex or Claude code agents in each visual studio window the implication is inbox should be checked by default and as soon as progress is impeded or blocked behind dependencies upon another repo at that time, the agent should inform Victor of the blockage so that Victor would go Work with the agents in the other visual studio window in order to unblock progress in the blocked repo.

 How do we handle sensitive information and coordination requests?
 In our current, our current assumptions are that we will be doing development within a trusted ecosystem as soon as that changes, we will introduce other policies or remediation.

 Who serves as agent ops lead long-term to maintain awareness, guide, and conduct dry runs?
 For now it's Victor occasionally going back into the repose that are responsible for defining awareness guides, which is this one that is chora base.
