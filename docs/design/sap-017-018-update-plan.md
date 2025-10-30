# SAP-017 and SAP-018 Update Plan

**Status**: 📋 Planned (defer until after pilot)
**Created**: 2025-10-29
**Priority**: High (outdated documentation)

---

## Problem

**SAP-017 (chora-compose-integration)** and **SAP-018 (chora-compose-meta)** document an **outdated version** of chora-compose.

**Current Documentation** (Incorrect):
- Describes chora-compose as "Docker Compose-based orchestration system for AI agent development environments"
- Focus on container orchestration, volume management, service dependencies
- References Docker-specific patterns and configurations

**Reality** (From COORD-2025-002-response):
- chora-compose IS a **content generation framework** with 17 production generators
- Supports artifact composition from constituent content blocks
- 17 MCP tools for AI-native workflows
- Template-based (Jinja2) with configuration-driven generation
- Used for structured documentation, not container orchestration

---

## Impact

**On Ecosystem**:
- ❌ Other repos learn incorrect information about chora-compose
- ❌ Misleading for new adopters
- ❌ Doesn't document actual capabilities (17 generators, MCP tools)

**On chora-compose**:
- ❌ Misrepresents their project to ecosystem
- ❌ Documentation debt in widely-adopted chora-base

**On Wave 6**:
- ❌ Can't reference SAP-017/018 for chora-compose integration
- ❌ Need accurate documentation before scaling to 18 SAPs

---

## Interim Solution (This Week)

**Add Warning to Both SAPs**:

Create file: `docs/skilled-awareness/chora-compose-integration/OUTDATED-WARNING.md`
Create file: `docs/skilled-awareness/chora-compose-meta/OUTDATED-WARNING.md`

**Warning Text**:
```markdown
# ⚠️ OUTDATED DOCUMENTATION WARNING

**Status**: This SAP documents an early version of chora-compose (Docker orchestration focus).

**Current Reality**: chora-compose is a **content generation framework** with 17 production generators,
not a Docker orchestration tool.

**Update in Progress**: This SAP is being rewritten to reflect current chora-compose capabilities.
Expected completion: After pilot project validates our understanding (~2025-11-19).

**For Current Information**:
- chora-compose repository: https://github.com/liminalcommons/chora-compose
- See: README.md, docs/explanation/architecture/, docs/how-to/configs/

**Related Work**:
- Pilot project: docs/design/pilot-sap-004-generation.md
- Collections exploration: docs/design/collections-exploration-notes.md

**Last Updated**: 2025-10-29
```

Also update first line of each SAP's `capability-charter.md`:
```markdown
# SAP-017: chora-compose Integration - Capability Charter

> ⚠️ **OUTDATED**: This SAP documents an early Docker-focused version. Update in progress. See [OUTDATED-WARNING.md](./OUTDATED-WARNING.md)
```

---

## Full Rewrite Plan (After Pilot)

### Timing

**When**: After pilot project completes (~2025-11-19)
**Why**: Pilot validates our understanding of current chora-compose capabilities
**Effort**: 8-12 hours per SAP (16-24 hours total)

### Approach

**Step 1: Research** (2-3 hours per SAP)
- Read chora-compose documentation:
  - README.md (project overview)
  - docs/explanation/architecture/ (design philosophy)
  - docs/how-to/configs/ (practical examples)
  - MCP tool catalog (17 tools)
- Interview chora-compose team (optional)
- Review pilot project learnings

**Step 2: Rewrite SAP-017** (chora-compose-integration) (6-9 hours)

**New Focus**: How to use chora-compose for content generation in chora-base projects

**5 Artifacts**:
1. **capability-charter.md** (~2 hours)
   - WHAT: chora-compose as content generation framework
   - WHY: Reduce documentation effort, ensure consistency
   - WHO: Developers integrating structured documentation generation

2. **protocol-spec.md** (~2-3 hours)
   - Technical contract: 17 MCP tools, content configs, artifact assembly
   - Data models: Content config schema, artifact config schema
   - Integration patterns: How to use with chora-base projects

3. **awareness-guide.md** (~1-2 hours)
   - WHEN: Use chora-compose for multi-artifact documentation
   - WHERE: Documentation generation, SAP artifacts, structured content
   - Decision framework: When to use vs hand-write

4. **adoption-blueprint.md** (~1-2 hours)
   - Step-by-step: Install chora-compose, create configs, generate content
   - Examples: Simple content generation, SAP artifacts
   - Troubleshooting

5. **ledger.md** (~0.5-1 hour)
   - Adoption records: chora-base (SAP generation pilot)
   - Lessons learned from pilot project

**Step 3: Rewrite SAP-018** (chora-compose-meta) (6-9 hours)

**New Focus**: Comprehensive understanding of chora-compose architecture and design

**5 Artifacts**:
1. **capability-charter.md** (~2 hours)
   - Deep dive: Content generation framework architecture
   - WHY: Design philosophy, composition over configuration
   - WHO: Architects, contributors, platform engineers

2. **protocol-spec.md** (~2-3 hours)
   - Complete technical specification
   - 17 generators documented
   - 17 MCP tools documented
   - Template system (Jinja2)
   - Configuration-driven workflows

3. **awareness-guide.md** (~1-2 hours)
   - Advanced usage patterns
   - Customization and extension
   - Integration with other tools
   - Performance and scaling considerations

4. **adoption-blueprint.md** (~1-2 hours)
   - Advanced adoption: Custom generators, template development
   - Ecosystem integration patterns
   - Contribution guidelines

5. **ledger.md** (~0.5-1 hour)
   - Adoption records across ecosystem
   - Evolution of chora-compose (Docker → content generation)

**Step 4: Review & Publish** (2 hours)
- Internal review
- Share with chora-compose team for accuracy check
- Update INDEX.md and sap-catalog.json
- Commit and publish

---

## Success Criteria

✅ **Accurate**: Documents current chora-compose (content generation, not Docker)
✅ **Complete**: Covers 17 generators, 17 MCP tools, configuration patterns
✅ **Useful**: Enables ecosystem repos to integrate chora-compose
✅ **Validated**: chora-compose team confirms accuracy
✅ **Updated References**: All cross-references in other SAPs updated

---

## Dependencies

- ⏳ **Pilot project must complete** (~2025-11-19)
  - Validates our understanding of chora-compose
  - Provides real-world integration example (SAP generation)
  - Lessons learned inform adoption blueprints

- ⏳ **chora-compose documentation review**
  - Read their docs to understand current capabilities
  - Possibly interview team for clarifications

---

## Risk Mitigation

**Risk 1**: Pilot reveals chora-compose doesn't work for SAP generation
- **Impact**: Still need to rewrite SAP-017/018 (correct documentation)
- **Mitigation**: Rewrite based on their actual capabilities, even if not suitable for our use case

**Risk 2**: chora-compose evolves during rewrite process
- **Impact**: Documentation becomes outdated again
- **Mitigation**: Version lock SAPs to specific chora-compose version, note in charter

**Risk 3**: Effort exceeds 16-24 hours
- **Impact**: Delays Wave 6 work
- **Mitigation**: Prioritize SAP-017 (integration) over SAP-018 (meta) if needed

---

## Timeline

| Phase | Timing | Effort |
|-------|--------|--------|
| **Interim Warning** | This week (2025-10-29) | 0.5 hours |
| **Research** | After pilot (~2025-11-19) | 4-6 hours |
| **Rewrite SAP-017** | Post-pilot | 6-9 hours |
| **Rewrite SAP-018** | Post-pilot | 6-9 hours |
| **Review & Publish** | Post-pilot | 2 hours |
| **Total** | | **18.5-26.5 hours** |

---

## Deliverables

### Immediate

1. ✅ This plan document
2. ⏳ `OUTDATED-WARNING.md` in both SAP directories
3. ⏳ Warning added to first line of capability-charters

### After Pilot

1. ⏳ Completely rewritten SAP-017 (5 artifacts)
2. ⏳ Completely rewritten SAP-018 (5 artifacts)
3. ⏳ Updated cross-references in other SAPs
4. ⏳ Updated INDEX.md and sap-catalog.json

---

## Related Work

**Pilot Project**:
- docs/design/pilot-sap-004-generation.md (validates chora-compose understanding)

**Collections Architecture**:
- docs/design/collections-exploration-notes.md (updated with chora-compose response)
- docs/project-docs/CHORA-BASE-4.0-VISION.md (Wave 6 updated)

**Coordination**:
- COORD-2025-002: Exploratory request to chora-compose
- COORD-2025-002-response: Their response (revealed documentation gap)
- COORD-2025-002-RESPONSE: Our acceptance of pilot

---

## Notes

**Why Defer Until After Pilot**:
1. Pilot validates our understanding of current chora-compose capabilities
2. Pilot provides real-world integration example (SAP generation)
3. Avoid rewriting based on partial understanding
4. Lessons learned from pilot inform adoption blueprints

**Why Not Wait Longer**:
1. Outdated documentation misleads ecosystem NOW
2. Interim warning addresses immediate problem
3. Full rewrite blocks Wave 6 scaling (need accurate integration docs)

---

**Last Updated**: 2025-10-29
**Status**: Interim warning this week, full rewrite after pilot
**Owner**: chora-base team
**Stakeholder**: chora-compose team (accuracy review)
