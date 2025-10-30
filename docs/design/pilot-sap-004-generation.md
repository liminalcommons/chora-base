# Pilot Project: SAP-004 Generation with chora-compose

**Status**: 🧪 Approved (2025-10-29)
**Timeline**: 2 weeks (starting ~2025-11-06)
**Effort**: 4-6 hours (chora-base), 4-6 hours (chora-compose)

---

## Goal

Validate that chora-compose can generate SAP artifacts meeting our quality bar (80%+ of hand-written quality).

---

## Pilot SAP: SAP-004 (Testing Framework)

**Why SAP-004?**
- ✅ Mature SAP with clear structure
- ✅ Technical depth but not overwhelming
- ✅ Reusable patterns (pytest, coverage, CI/CD)
- ✅ Minimal interdependencies with other SAPs
- ✅ Not too simple (SAP-000) or too complex (SAP-018)

**Current State**:
- 5 hand-written artifacts (~15k tokens total)
- Took 8-12 hours to create originally
- Located: `docs/skilled-awareness/testing-framework/`

**Target**:
- Generate from constituent content blocks + context
- Quality ≥ 80% of hand-written version
- Generation time < 5 seconds per artifact

---

## Timeline

| Week | Dates | Phase | Effort |
|------|-------|-------|--------|
| **Week 1** | 2025-11-06 to 2025-11-12 | Decomposition & Configuration | 3-6 hours |
| **Week 2** | 2025-11-13 to 2025-11-19 | Generation & Decision | 1-3 hours |

---

## Phase 1: Decomposition (Week 1, 2-4 hours)

**Owner**: chora-base team with chora-compose guidance

**Tasks**:
1. Read all 5 SAP-004 artifacts
2. Identify constituent content blocks:
   - Reusable across multiple SAPs (e.g., `pytest-setup.md`)
   - SAP-specific (e.g., `sap-004-problem-statement.md`)
3. Categorize content by reusability:
   - **Universal**: Usable across many SAPs
   - **Domain**: Usable within testing domain
   - **SAP-specific**: Unique to SAP-004
4. Document content block structure and rationale
5. Share decomposition with chora-compose

**Deliverable**: Content blocks + decomposition rationale document

---

## Phase 2: Configuration (Week 1-2, 1-2 hours)

**Owner**: chora-compose creates, chora-base reviews

**Tasks (chora-compose)**:
1. Create content configs for 5 artifact types:
   - `sap-004-charter.json`
   - `sap-004-protocol.json`
   - `sap-004-guide.json`
   - `sap-004-blueprint.json`
   - `sap-004-ledger.json`
2. Create artifact assembly config
3. Create templates (Jinja2) if needed
4. Share configs with chora-base

**Tasks (chora-base)**:
1. Review configs and templates
2. Provide feedback on structure
3. Iterate if needed

**Deliverable**: Validated configs ready for generation

---

## Phase 3: Generation & Quality Review (Week 2, 1-2 hours)

**Owner**: Both teams collaborate

**Tasks (chora-compose)**:
1. Generate SAP-004 artifacts using configured generator
2. Provide generation logs and metrics
3. Share generated artifacts

**Tasks (chora-base)**:
1. Compare generated vs hand-written SAP-004
2. Assess against 10 success criteria (see below)
3. Document findings: what works, what needs improvement
4. Score quality (0-100%)

**Deliverable**: Quality comparison report

---

## Phase 4: Go/No-Go Decision (Week 2, 1 hour)

**Owner**: chora-base decides, chora-compose provides input

**Decision**:
- **Go** (quality ≥ 80%): Proceed with Wave 6 Option B (generation-based collections) in v4.2.0
- **No-Go** (quality < 80%): Fall back to Option A (metadata only) or Option C (defer to v4.3.0)
- **Partial** (mixed results): Hybrid approach (generate some SAPs, hand-write others)

**Deliverable**: Decision document with rationale

---

## Success Criteria (10 Criteria)

### From chora-compose Response

1. ✅ **Structure Match**: Generated artifacts match hand-written SAP-004 structure
2. ✅ **Quality Bar**: Meets "could publish this" standard
3. ✅ **Performance**: Generation time < 5 seconds per artifact
4. ✅ **Maintainability**: Updating content block → regenerate → changed artifacts only
5. ✅ **Flexibility**: Same blocks + different context → customized output

### Additional from chora-base

6. ✅ **Technical Accuracy**: Generated content is factually correct
7. ✅ **Coherence**: Reads as unified documentation, not assembled fragments
8. ✅ **Agent-Readability**: Claude can parse and understand generated SAPs effectively
9. ✅ **Ease of Maintenance**: Content blocks easy to update without deep framework knowledge
10. ✅ **Scalability**: Clear path to generating remaining 17 SAPs

---

## Quality Assessment Rubric

| Criterion | Weight | Score (0-10) | Weighted Score |
|-----------|--------|--------------|----------------|
| Structure Match | 10% | TBD | TBD |
| Technical Accuracy | 20% | TBD | TBD |
| Coherence | 15% | TBD | TBD |
| Agent-Readability | 10% | TBD | TBD |
| Quality Bar | 15% | TBD | TBD |
| Performance | 5% | TBD | TBD |
| Maintainability | 10% | TBD | TBD |
| Flexibility | 5% | TBD | TBD |
| Ease of Maintenance | 5% | TBD | TBD |
| Scalability | 5% | TBD | TBD |
| **Total** | **100%** | | **TBD** |

**Go Threshold**: 80%+ overall score

---

## Risks & Mitigations

**Risk 1**: Generated quality doesn't meet 80% threshold
- **Likelihood**: Medium
- **Mitigation**: Iterate on configs and templates during pilot
- **Fallback**: Fall back to Option A or C

**Risk 2**: SAP-004 decomposition too complex
- **Likelihood**: Low
- **Mitigation**: Start with simple decomposition, refine iteratively
- **Escalation**: Consult chora-compose on decomposition strategy

**Risk 3**: Timeline slips due to async coordination
- **Likelihood**: Low-Medium
- **Mitigation**: 24-48 hour response time commitment from both teams
- **Buffer**: 2-week timeline includes buffer for iteration

---

## Collaboration & Communication

**Primary Channel**: Inbox protocol (JSON files in repos)
**Technical Discussion**: GitHub issues or direct communication
**Response Time**: 24-48 hours for most items, faster for quick clarifications

**Tracking**:
- This document: `docs/design/pilot-sap-004-generation.md`
- chora-compose may create their own tracking document

**Progress Updates**:
- End of Week 1: Decomposition complete, configs under review
- Mid Week 2: Generation complete, quality assessment underway
- End of Week 2: Go/No-Go decision made

---

## Deliverables

1. ✅ Pilot project plan (this document)
2. ⏳ Content blocks for SAP-004 (Week 1)
3. ⏳ Content configs (5 artifact types) (Week 1-2)
4. ⏳ Generated SAP-004 artifacts (5 files) (Week 2)
5. ⏳ Quality comparison report (Week 2)
6. ⏳ Go/No-Go decision document (Week 2)

---

## Related Coordination

- **COORD-2025-002**: Exploratory request to chora-compose (sent 2025-10-29)
- **COORD-2025-002-response**: chora-compose response (received 2025-10-29)
- **COORD-2025-002-RESPONSE**: chora-base acceptance (sent 2025-10-29)

---

## Next Steps

**Immediate (This Week)**:
1. ✅ Create this tracking document (done!)
2. 📖 Review chora-compose documentation (README, architecture, configs)
3. 📚 Re-read SAP-004 artifacts to prepare for decomposition
4. 🤝 Confirm start date with chora-compose team

**Week 1 Kickoff** (~2025-11-06):
1. Begin SAP-004 decomposition
2. Collaborate with chora-compose on content block structure
3. Review their configs as they're created

---

**Last Updated**: 2025-10-29
**Status**: Awaiting pilot start (~2025-11-06)
**Owner**: chora-base team (pilot execution), both teams (collaboration)
