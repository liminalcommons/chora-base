# v4.0 Cleanup Manifest

**Purpose**: Track files, references, and actions that need cleanup as we transform to v4.0.

**Last Updated**: 2025-10-28
**Status**: Empty template - will be populated during Waves 1-7

---

## How to Use This Manifest

### During Waves 1-7
As you work on each wave, **immediately add items to this manifest** when you:
- Discover obsolete files that should be deleted
- Find files that should be archived (not deleted, but not actively used)
- Identify files that need to be moved/renamed
- Notice references that need updating
- Consider git history implications

### During Wave 8
- Review this entire manifest
- Verify each item is still valid
- Execute all actions in priority order:
  1. Delete files
  2. Archive files
  3. Move/rename files
  4. Update references
  5. Clean git history

---

## Files to Delete

**Status codes**: PENDING | IN_PROGRESS | DONE

| File | Wave | Reason | Size | Verified Safe? | Status |
|------|------|--------|------|----------------|--------|
| *(No items yet)* | - | - | - | - | - |

**Instructions**:
- Add files that should be permanently deleted
- "Verified Safe?" = No active references, truly obsolete
- Before marking DONE, verify with: `git grep <filename>`

---

## Files to Archive

**Status codes**: PENDING | IN_PROGRESS | DONE

| File | Wave | Archive Location | Reason | Status |
|------|------|------------------|--------|--------|
| *(No items yet)* | - | - | - | - |

**Instructions**:
- Add files that have historical value but aren't actively used
- Archive location: `.archive/v3-final/` (created in Wave 8)
- Examples: Old conversation logs, deprecated templates

---

## Files to Move/Rename

**Status codes**: PENDING | IN_PROGRESS | DONE

| From | To | Wave | Reason | Status |
|------|-----|------|--------|--------|
| *(No items yet)* | - | - | - | - |

**Instructions**:
- Add files that need new locations
- Verify destination doesn't exist before moving
- Update all references after moving (add to "References to Update" section)

---

## References to Update

**Status codes**: PENDING | IN_PROGRESS | DONE

| File | Line/Section | Update Needed | Wave | Status |
|------|--------------|---------------|------|--------|
| *(No items yet)* | - | - | - | - |

**Instructions**:
- Add any links, imports, or references that need updating
- Be specific about location (line number or section heading)
- Verify update with link checker after completing

---

## Git History Considerations

**Status codes**: PENDING | IN_PROGRESS | DONE

| Issue | Impact | Action | Wave | Status |
|-------|--------|--------|------|--------|
| *(No items yet)* | - | - | - | - |

**Instructions**:
- Track git history decisions (e.g., should we tag before major deletions?)
- Examples: Tag v3.x-final-with-blueprints before deleting blueprints/
- Consider: Should we squash commits? Preserve history?

---

## Expected Items (Anticipated)

### From Wave 1 (Documentation Architecture)
**Files to Delete**:
- Possible: Duplicate docs after reorganization
- Possible: `docs/reference/chora-base/latest-conversation.md` (488 KB temp file)

**Files to Move**:
- All docs/ subdirectories to 4-domain structure
- (Will add specific files as we discover them)

**References to Update**:
- All links pointing to old docs/ locations
- SAP awareness-guides referencing moved files

---

### From Wave 3 (Eliminate MCP-Specific)
**Files to Delete** (HIGH CONFIDENCE):
- `blueprints/` directory (11 files)
- `setup.py` (443 lines)
- `AGENT_SETUP_GUIDE.md`

**Files to Archive** (MAYBE):
- Blueprints (archive for reference before deleting?)
- setup.py (archive for reference?)

**Files to Move**:
- MCP-specific content → SAP-014 location
- MCP templates → `static-template/mcp-templates/`

**References to Update**:
- Root docs (README, AGENTS, CLAUDE) - remove MCP assumptions
- SAP-003 references to blueprints/ and setup.py

**Git History**:
- Tag: `v3.x-final-with-blueprints` before deleting blueprints/

---

### From Waves 4-7 (Minimal Expected)
Waves 4-7 are mostly additive. Will add items as discovered.

---

## Wave 8 Execution Checklist

**Pre-Execution**:
- [ ] Review entire manifest
- [ ] Remove any items that were already handled in earlier waves
- [ ] Add any late discoveries
- [ ] Verify all "Verified Safe?" columns are YES for deletions

**Execution Order**:
1. [ ] Execute all deletions (highest risk, do first so can rollback)
2. [ ] Execute all archives (preserve history)
3. [ ] Execute all moves/renames
4. [ ] Update all references
5. [ ] Address git history items

**Post-Execution**:
- [ ] Run inventory: `python scripts/inventory-chora-base.py`
- [ ] Run link checker: `python scripts/validate-links.py`
- [ ] Run SAP validator: `python scripts/validate-saps.py`
- [ ] Verify 100% coherence maintained
- [ ] Commit cleanup
- [ ] Tag v4.0.0-rc1

---

## Rollback Plan

If Wave 8 execution encounters issues:

1. **Immediate rollback**:
   ```bash
   git reset --hard HEAD~1
   ```

2. **Partial rollback** (restore specific files):
   ```bash
   git checkout HEAD~1 -- path/to/file
   ```

3. **Full project rollback**:
   ```bash
   # Restore from Wave 7 completion tag
   git reset --hard v3.10.0
   ```

---

## Notes

- **Add items as you go** - Don't wait until Wave 8 to discover cleanup needs
- **Be specific** - Exact file paths, line numbers, reasons
- **Verify safety** - Always check for references before marking deletions safe
- **Update status** - Mark items DONE as you complete them in earlier waves
- **Ask if unsure** - If uncertain whether to delete/archive, ask before Wave 8

---

**Template Version**: 1.0
**Created**: 2025-10-28
**Ready for**: Wave 1 population
