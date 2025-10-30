# Adoption Blueprint: Cross-Repository Inbox Skilled Awareness Package

---

## 1. Read Before You Begin
- **Capability Charter:** `docs/reference/skilled-awareness/inbox/capability-charter.md`
- **Protocol Spec:** `docs/reference/skilled-awareness/inbox/protocol-spec.md`
- **Prerequisites:**
  - Repository uses Git and supports committing coordination artefacts.
  - Maintainership agreement to adopt inbox workflow (coordination cadence defined).
  - Shell utilities available (`bash`, `jq`, optional `yq`) or equivalent tooling.
  - AI agent guides (AGENTS.md / CLAUDE.md) ready to reference new awareness guide.

---

## 2. Installation

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-001 --source /path/to/chora-base
```

**What This Installs**:
- Inbox coordination protocol documentation (5 artifacts)
- `inbox/` directory structure at repository root
- Schema files, CAPABILITIES configuration, and event log
- Cross-repo coordination workflows

### Part of Sets

This SAP is included in:
- minimal-entry
- recommended
- full

To install a complete set:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Validation

Verify all artifacts exist:

```bash
# Verify SAP documentation
ls docs/skilled-awareness/inbox/*.md
# Verify inbox directory structure
ls inbox/coordination/events.jsonl inbox/incoming/
```

### Manual Installation (Alternative)

If you cannot use the install script, follow these manual steps:

1. Create `inbox/` directory at repository root
2. Copy prototype structure from `chora-base/inbox/`
3. Add schema files under `inbox/schemas/`
4. Initialize `inbox/coordination/events.jsonl` as an empty append-only log
5. Customize `coordination/CAPABILITIES/<repo>.yaml` with repo-specific routing details
6. Add awareness references to the repo's `CLAUDE.md` / `AGENTS.md`
7. Commit with message noting adoption

---

## 3. Files & Directories

| Path | Purpose | Optional? | Notes |
|------|---------|-----------|-------|
| `inbox/INBOX_PROTOCOL.md` | Local protocol copy (press ready reference). | Yes (may link to canonical doc) | Keep pointer to spec for operator convenience. |
| `inbox/CLAUDE.md` | Awareness guide tailored to repo. | Recommended | Customize with repo name, capabilities. |
| `inbox/coordination/events.jsonl` | Event log for state transitions. | Required | Initialize empty file; ensure append-only. |
| `inbox/coordination/CAPABILITIES/<repo>.yaml` | Defines work the repo can send/receive. | Required | Update with categories, limits, contacts. |
| `inbox/incoming/coordination/` | Queue for coordination requests. | Required | Start empty; ensure README describing usage. |
| `inbox/incoming/tasks/` | Queue for implementation tasks. | Required | Provide README with acceptance criteria. |
| `inbox/ecosystem/proposals/` | Strategic proposals (markdown). | Optional initially | Adopt when planning cadence defined. |
| `docs/reference/skilled-awareness/inbox/` | Canonical SAP docs (charter, spec, etc.). | Required | Copy or symlink from chora-base template. |
| `docs/reference/skilled-awareness/inbox/ledger.md` | Traceability ledger entry for repo. | Required | Seed with repo information during install. |

---

## 4. Configuration Checklist

- [ ] Repo maintainer owns inbox package (listed in ledger).  
- [ ] `CAPABILITIES/<repo>.yaml` defines `provides`, `consumes`, `can_receive`.  
- [ ] Awareness guide cross-linked from root `CLAUDE.md` / `AGENTS.md`.  
- [ ] Event log file created with header comment describing format (optional metadata).  
- [ ] Schema validation command tested (`cat … | jq .` or `python -m json.tool`).  
- [ ] Documentation plan updated to include inbox capability (if applicable).

---

## 5. Verification

- **Smoke Checks:**  
  - Create sample coordination request (JSON) and ensure schema validation passes.  
  - Move sample task through `incoming → active → completed` while logging events.  
  - Run awareness checklist: agent performs triage simulation using guide.

- **Acceptance Tests:**  
  - Ensure README/CLAUDE instructions clear to another maintainer (peer review).  
  - Confirm event log entry format consistent with spec.  
  - Review adoption ledger entry for accuracy and completeness.

- **Rollback Plan:**  
  - Remove `inbox/` directory and revert supporting docs to previous state.  
  - Update ledger with rollback note and reason.  
  - Communicate to ecosystem coordinator via inbox strategic note.

---

## 6. Post-Install Tasks

- **Awareness Enablement:**  
  - Update root `CLAUDE.md` and `AGENTS.md` to reference inbox awareness guide.  
  - Schedule agent dry run to confirm instructions.

- **Status Ledger Update:**  
  - Add entry to `docs/reference/skilled-awareness/inbox/ledger.md` noting adoption date, version, and feedback channel.

- **Feedback Loop:**  
  - After first sprint of usage, document lessons learned in ledger feedback log.  
  - Raise coordination item if additional automation or schema changes needed.
