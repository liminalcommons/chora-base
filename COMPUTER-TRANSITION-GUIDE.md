# Computer Transition Quick Reference

**Date**: 2025-11-15
**Purpose**: Seamless continuity for Ecosystem Ontology Phase 1 work

---

## On Your New Computer

### 1. Sync the Repository (2 minutes)

```bash
cd ~/code/chora-base
git pull origin main
```

**What this gets you**:
- ✅ All Week 1-2 documentation (9 files, 192KB)
- ✅ Beads task database (`.beads/issues.jsonl`)
- ✅ Coordination requests (`inbox/coordination/`)
- ✅ **CONTINUITY-2025-11-15.md** - Complete session context

---

### 2. Verify Everything Synced (1 minute)

```bash
# Quick verification
ls -1 docs/ontology/*.md | wc -l        # Should output: 6
ls -1 capabilities/template-*.yaml | wc -l  # Should output: 2
ls -1 schemas/*.{json,md} 2>/dev/null | wc -l  # Should output: 4
test -f CONTINUITY-2025-11-15.md && echo "✅ Continuity file present"
```

All checks should pass ✅

---

### 3. Load Claude Code with Continuity Context (30 seconds)

**Open Claude Code and paste this prompt**:

```
I'm continuing the Ecosystem Ontology Phase 1 work from another computer.

Context handoff:
- Completed Week 1 (Foundation & Taxonomy) and Week 2 (Metadata Schema & Validation)
- Created 192KB of documentation across 9 files
- 8/16 Phase 1 tasks complete (50% done)

Please read CONTINUITY-2025-11-15.md for complete context and verify all deliverables are present. Then confirm you're ready to start Week 3.1 (Pre-commit hook implementation).
```

---

## What Got Committed

### Documentation (9 files)

**Ontology Specifications**:
- `docs/ontology/domain-taxonomy.md` - 20 domains across 4 tiers
- `docs/ontology/namespace-spec.md` - chora.domain.capability format
- `docs/ontology/migration-guide.md` - Migration from sap-catalog.json
- `docs/ontology/capability-types.md` - Service vs Pattern types
- `docs/ontology/dublin-core-schema.md` - 15 Dublin Core elements
- `docs/ontology/chora-extensions-spec.md` - 3 extension namespaces

**Templates**:
- `capabilities/template-service.yaml` - Service-type template
- `capabilities/template-pattern.yaml` - Pattern-type template

**Validation**:
- `schemas/capability-common.schema.json` - Shared definitions
- `schemas/capability-service.schema.json` - Service validator
- `schemas/capability-pattern.schema.json` - Pattern validator
- `schemas/README.md` - Validation documentation

### Continuity Files

- **CONTINUITY-2025-11-15.md** - Complete session handoff (this is the key file!)
- **inbox/coordination/COORD-2025-017-SESSION-HANDOFF-WEEK-2-COMPLETE.json** - Structured handoff data

### Task Tracking

- `.beads/issues.jsonl` - All 16 Phase 1 tasks (8 closed, 8 open)
- Beads database is git-committed and will sync automatically

---

## Expected State After Sync

### ✅ Completed Work

**Week 1**: 4/4 tasks ✅
- Domain taxonomy
- Namespace specification
- Migration guide
- Capability types

**Week 2**: 4/4 tasks ✅
- Dublin Core schema
- YAML templates
- JSON Schema validators
- Chora extensions

### ⏳ Next Up

**Week 3**: 0/4 tasks
- Task 3.1: Pre-commit hook (namespace validation)
- Task 3.2: CI/CD workflow (duplicate detection)
- Task 3.3: Migration script (sap-catalog.json → YAML)
- Task 3.4: Artifact extractor (SAP directory scan)

---

## Key Files for Claude Code

When Claude Code starts on the new computer, these are the critical files to read:

1. **CONTINUITY-2025-11-15.md** - Complete session context (read this first!)
2. **docs/project-docs/plans/PHASE-1-2-EXECUTION-PLAN.md** - Detailed task breakdown
3. **inbox/coordination/COORD-2025-015-ECOSYSTEM-ONTOLOGY-PHASE-1.json** - Phase 1 coordination
4. **inbox/coordination/COORD-2025-017-SESSION-HANDOFF-WEEK-2-COMPLETE.json** - Handoff metadata

---

## Troubleshooting

### Problem: "File not found"

**Solution**: Make sure you did `git pull origin main` first

### Problem: "Beads tasks show different IDs"

**Expected**: Task IDs are unique and will be different from the continuity document. Use task labels:
```bash
bd list --label "week-3" --json | jq -r '.[] | "\(.id): \(.title)"'
```

### Problem: "Claude Code can't find CONTINUITY file"

**Check**:
```bash
ls -lh CONTINUITY-2025-11-15.md
# Should show file with ~50KB size
```

If missing, you may need to commit and push from this computer first (see below).

---

## If This Computer Still Has Unsaved Work

### Push to Remote (1 minute)

```bash
git status  # Verify commit is there
git push origin main
```

Then on new computer:
```bash
git pull origin main  # Gets the commit with all files
```

---

## Session Resumption Commands

Once on new computer with Claude Code loaded:

```bash
# 1. Check beads status
bd list --label "phase-1" --json | jq -r '.[] | "\(.status | ascii_upcase): \(.title)"'

# 2. View Week 3 tasks
bd list --label "week-3" --json | jq -r '.[] | "\(.id): \(.title)"'

# 3. Start Week 3.1
bd update <TASK-ID-FROM-ABOVE> --status in_progress --assignee "claude"
```

Claude Code will handle the rest based on CONTINUITY-2025-11-15.md context!

---

## Timeline

- **This Computer**: Weeks 1-2 complete (8 tasks, 53 hours)
- **New Computer**: Weeks 3-4 ahead (8 tasks, 52 hours)
- **Phase 1 Total**: 16 tasks, ~105 hours

---

**Status**: Ready for seamless transition ✅
**Commit**: e888b37 (feat(ontology): Complete Phase 1 Week 1-2)
**Files Committed**: 15 files, 7885 insertions

---

## Next Steps Summary

1. ✅ Git pull on new computer
2. ✅ Verify files with quick checks above
3. ✅ Open Claude Code with continuity prompt
4. ✅ Claude Code reads CONTINUITY-2025-11-15.md
5. ✅ Start Week 3.1 (Pre-commit hook)

**Estimated Transition Time**: 5 minutes

Good luck! 🚀
