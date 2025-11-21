# SAP-064: Wardley Mapping Capability Charter

**SAP ID**: SAP-064 (chora.strategic.wardley_mapping)
**Version**: 1.0.0
**Status**: Phase 2 (SAP Creation)
**Created**: 2025-11-20
**Maturity**: L1 (Planned)
**Trace ID**: wardley-phase-2-2025-11

---

## Problem Statement

### The Challenge

**Strategic planning in chora-workspace relies on intuition and text-based analysis, lacking systematic visual positioning and evolution assessment.**

**Symptoms**:
1. **Decision uncertainty**: Strategic decisions made with Medium confidence, lacking evidence-based positioning
2. **Hidden bottlenecks**: Dependencies between capabilities not visually apparent (e.g., SAP-056 at 0.55 blocking Wardley Maps at 0.15)
3. **Over-investment risks**: No systematic framework to identify Inertia Loops (over-investing in Genesis or Commodity)
4. **Missed ecosystem opportunities**: Commodity capabilities not recognized as pattern extraction candidates
5. **Long planning cycles**: Text-based strategic analysis takes 4-6 hours per session (60-80% clarification overhead)
6. **Inconsistent evolution assessment**: L0-L5 maturity levels understood, but evolution positioning (Genesis → Commodity) not systematically mapped

### Evidence (Phase 1 Validation)

**Before Wardley Map** (Baseline Strategic Planning):
- **Decision confidence**: Medium (text-based intuition)
- **Strategic planning time**: 4-6 hours estimated (text-only analysis)
- **Clarification overhead**: 60-80% of time spent on "what do you mean by..." questions
- **Strategic principles applied**: Ad-hoc (no systematic framework)
- **Decision change rate**: 0% (no positioning framework to challenge assumptions)

**After Wardley Map** (Phase 1 Manual Practice):
- **Decision confidence**: High (evidence-based positioning)
- **Strategic planning time**: 2.2 hours actual (64% reduction)
- **Clarification overhead**: ~30% (visual map communicates positioning clearly)
- **Strategic principles applied**: 8 principles systematically (Co-Evolution, Build vs Buy, Inertia Loop, Constraint Exploitation, Ecosystem Play, Practice-First, Selective Automation, Bottleneck Identification)
- **Decision change rate**: 67% (4 out of 6 decisions reversed based on map insights)
- **Decisions influenced**: 100% (6 out of 6 strategic questions benefited from map analysis)

**Value Delivered (Phase 1, 2.2 hours invested)**:
- **Time saved**: 4-9 days of wasteful work deferred (SAP-010 enhancements, SAP-007 enhancements, schema extension)
- **High-value work identified**: SAP-056 acceleration (bottleneck removal), SAP-063 ecosystem play (new meta-SAP discovered)
- **ROI**: 15-25x (2.2 hours → 4-9 days saved + 2-3 days high-value work)

### Root Cause

**chora-workspace has strong ontology for maturity assessment (L0-L5) but no systematic framework for:**
1. **Evolution positioning**: Where is this capability on the Genesis → Commodity spectrum?
2. **Value chain analysis**: What depends on what? Where are the bottlenecks?
3. **Strategic gameplay**: Which principles apply? (Co-Evolution, Inertia Loop, Ecosystem Play, etc.)

**Result**: Strategic decisions lack visual positioning context, making it hard to identify bottlenecks, over-investment risks, and ecosystem opportunities.

---

## Vision

### What We're Building

**SAP-064 enables systematic strategic analysis through Wardley mapping integrated with chora ontology (feature-manifest.yaml, L0-L5 maturity, SAP lifecycle).**

**Core Capabilities**:
1. **Component Extraction**: Parse feature-manifest.yaml to identify 10-15 strategic components across value chain layers
2. **Evolution Classification**: Map chora L0-L5 maturity to Wardley Genesis → Commodity positioning (0.0-1.0)
3. **Value Chain Analysis**: Extract dependency graph, calculate dependency depth, assign value chain layers
4. **Strategic Gameplay Identification**: Apply 8 strategic principles systematically to positioned map
5. **Strategic Session Facilitation**: Use map to inform evidence-based strategic decisions

### Integration with chora Ontology

**SAP-064 is NOT a standalone Wardley tool**—it's deeply integrated with chora's existing ontology:

| chora Ontology Element | Wardley Integration |
|----------------------|-------------------|
| **L0-L5 Maturity Levels** | Maps to Evolution Axis (Genesis 0.0 → Commodity 1.0) |
| **feature-manifest.yaml** | Source of components, dependencies, statuses, maturity levels |
| **SAP Lifecycle** | Informs evolution positioning (L3 → Custom/Product, L4 → Product/Commodity) |
| **feature.dependencies** | Extracted for value chain analysis (dependency depth, topological sort) |
| **A-MEM Events** | (Phase 4, optional) Activity pattern extraction for evolution velocity |
| **SAP-056 Traceability** | Bidirectional feature linkage enables value chain edge extraction |

**Key Insight**: chora ontology and Wardley ontology are **naturally aligned** (90%+ overlap)—minimal translation needed. L0-L5 already represents evolution stages; dependencies already represent value chain.

### Success Looks Like

**After SAP-064 adoption at L3 (Validated)**:

**Quantitative Metrics**:
- **Strategic decisions influenced**: 1+ per map (100% in Phase 1)
- **Decision change rate**: 50%+ (67% in Phase 1)
- **Strategic planning time reduction**: 30%+ (64% in Phase 1)
- **ROI**: 10x+ (15-25x in Phase 1)
- **Time to map**: 60-90 minutes (90 min in Phase 1)
- **Protocol clarity**: 80%+ external adopters can create map following protocol-spec.md

**Qualitative Outcomes**:
- Strategic decisions reference map positioning ("SAP-056 at 0.55 blocks Wardley at 0.15, accelerate to remove bottleneck")
- Bottlenecks identified proactively (co-evolution opportunities, lower evolution blocking higher)
- Over-investment avoided (Inertia Loops identified, Commodity enhancements deferred)
- Ecosystem plays discovered (Commodity pattern extraction, meta-SAP creation like SAP-063)
- Strategic principles applied systematically (8 principles, not ad-hoc intuition)

**At L4 (Distributed)**:
- 2+ external repos adopt SAP-064 (chora-compose, chora-github)
- Protocol-spec.md refined to v1.1.0+ based on external feedback
- Cross-repo strategic analysis enabled (chora-workspace, chora-base, chora-compose value chain)

**At L5 (Sustained, optional)**:
- Quarterly strategic mapping practice institutionalized (Q-reviews reference maps)
- Selective automation implemented IF frequency justifies (10+ maps per quarter, 30+ min manual, 20%+ error rate)
- Value chain analyzer automation (IF validated pain point from Phase 2-3)

---

## Scope

### In-Scope (SAP-064 v1.0.0)

**Phase 1 (Genesis, Manual Practice)**: ✅ COMPLETE
- Manual map creation following protocol-spec.md
- Strategic session validation (self-validation or stakeholder session)
- Gate decision (did map influence 1+ strategic decision?)
- Phase 1 deliverables: map file, strategic session notes, gate decision

**Phase 2 (Custom, SAP Creation)**: 🔄 IN PROGRESS
- Document proven manual workflow as protocol-spec.md ✅ COMPLETE
- Create SAP-064 artifacts (charter, blueprint, awareness-guide, ledger) ⏳ IN PROGRESS
- Validate artifact consistency and completeness

**Phase 3 (Product, External Validation)**: ⏳ PENDING
- Pilot adoption with 2-3 additional maps
- Track protocol clarity, time to map, strategic value
- Refine SAP-064 to v1.1.0 based on pilot learnings
- Achieve L3 maturity (2+ adoptions, protocol validated)

**Phase 4 (Commodity, Selective Automation, Optional)**: ⏳ CONDITIONAL
- ONLY IF selective automation criteria met (30+ min AND 10+ reps AND 20% error)
- Value chain analyzer automation (STRONG candidate IF frequency validates)
- Component extractor automation (DEFER unless frequency reaches 10+ maps/quarter)
- Evolution classifier automation (DEFER, low pain)

### Out-of-Scope (SAP-064 v1.0.0)

**NOT included in v1.0.0**:
1. ❌ **Automated visualization**: Manual text-based maps sufficient (Excalidraw/OnlineWardleyMaps for visual if needed)
2. ❌ **Real-time mapping**: Strategic maps updated quarterly or per-sprint, not continuously
3. ❌ **External Wardley tool integration**: chora-native approach preferred (deep ontology integration)
4. ❌ **DSL parser**: No custom Wardley DSL needed (YAML + markdown sufficient)
5. ❌ **MkDocs plugin**: No automated site generation (Phase 4 only, IF justified)
6. ❌ **CI/CD automation**: No automated map updates on git push (manual practice validated first)
7. ❌ **Gameplay automation**: Strategic principle identification remains expert judgment (not algorithmic)

**Deferred to Phase 4** (only if selective automation criteria met):
- Component extraction automation (IF 10+ maps per quarter)
- Value chain analyzer automation (IF 5+ maps per quarter AND high error risk)
- Evolution classifier automation (IF error rate > 20%)

**Future Versions** (SAP-064 v2.0.0+, TBD):
- A-MEM event log integration (activity pattern extraction for evolution velocity)
- Cross-repo value chain analysis (chora-workspace, chora-base, chora-compose dependencies)
- SAP dependency visualization (recursive SAP mapping, IF pain point validated)
- Wardley doctrine integration (Pioneers/Settlers/Town Planners team composition analysis)

---

## Success Criteria

### Phase 2 Success (SAP-064 Creation)

**Deliverables Complete**:
- ✅ protocol-spec.md (manual workflow documented)
- ⏳ capability-charter.md (this file)
- ⏳ adoption-blueprint.md (L0 → L5 maturity path)
- ⏳ awareness-guide.md (quick reference)
- ⏳ ledger.md (adoption tracking)

**Artifact Quality**:
- All artifacts reference Phase 1 evidence (no speculation)
- Consistent success metrics across all artifacts
- 8 strategic principles documented consistently
- L0-L5 → Genesis/Commodity mapping table validated

**Time Investment**: 3.5-5.5 hours (Task 2.2)

---

### Phase 3 Success (External Validation)

**Adoption Metrics**:
- 2-3 additional maps created following protocol-spec.md
- Protocol clarity: 80%+ (adopter survey: "I could follow the protocol")
- Time to map: 60-90 min (within target range)
- Strategic decisions influenced: 1+ per map

**Pain Point Validation**:
- Component extraction time tracked (target: ≤45 min)
- Value chain analysis time tracked (target: ≤30 min)
- Error rate tracked (target: ≤20% for manual processes)
- Frequency tracked (are we creating 5+ maps per quarter?)

**SAP Maturity**: Achieve L3 (Validated) after 2+ adoptions

**Time Investment**: 3-6 hours (Task 2.3)

---

### Phase 4 Success (Selective Automation, Optional)

**Automation Criteria Met**:
- Value chain analyzer: 30+ min manual AND 5+ maps per quarter AND high error risk (circular deps)
- Component extractor: 45+ min manual AND 10+ maps per quarter AND 20%+ error rate
- Evolution classifier: DEFER (low pain, clear mapping table exists)

**Automation Quality** (IF criteria met):
- Scripts reduce manual time by 50%+
- Error rate reduced to <5%
- Scripts validated on 3+ maps

**Time Investment**: 3-5 days (only if Phase 3 validates frequency)

---

## Strategic Alignment

### Wardley Evolution Principles Applied to SAP-064 Development

**Meta-Recursive Pattern**: SAP-064 development FOLLOWS Wardley evolution principles:

1. **Genesis (Phase 1)**: Manual practice, validate value, gate decision
2. **Custom (Phase 2)**: Document proven process as SAP artifacts
3. **Product (Phase 3)**: External validation, refinement to L3
4. **Commodity (Phase 4, optional)**: Selective automation ONLY if validated pain points

**Why this matters**: Demonstrates chora's strategic sophistication—we **practice what we preach** by applying Wardley principles to building Wardley capability.

**Risk Reduction**: Gate decision after 2-3 days (Phase 1) prevents 95% sunk cost vs infrastructure-first approach (15-25 days before validation).

### Integration with chora Ecosystem

**SAP-064 leverages existing capabilities** (Constraint Exploitation):
- **SAP-056 (Traceability)**: Provides dependency graph for value chain analysis
- **SAP-010 (Memory)**: (Phase 4, optional) Activity pattern extraction for evolution velocity
- **SAP-013 (Metrics)**: L0-L5 maturity levels inform evolution classification
- **SAP-008 (Automation)**: Justfile recipes for automation (Phase 4, IF justified)
- **SAP-007 (Documentation)**: Protocol-spec.md integrated with MkDocs (existing Commodity)

**SAP-064 enables future capabilities** (Ecosystem Play):
- **SAP-063 (Documentation Patterns)**: Discovered via Wardley analysis (Q4 SAP-007 at 0.85 Commodity → extract patterns)
- **SAP-065 (Development Lifecycle Meta-SAPs)**: (Future) Strategic roadmap for meta-SAP evolution
- **Cross-repo strategic analysis**: chora-workspace, chora-base, chora-compose value chain positioning

---

## Risk Management

### Risks Mitigated (Phase 1 Gate Decision)

**Risk 1: Over-investment before validation** (95% sunk cost reduction)
- **Risk**: Investing 15-25 days in Wardley infrastructure before proving maps deliver strategic value
- **Mitigation**: Gate decision after 2-3 days (Phase 1) validates value before Phase 2-4 investment
- **Result**: ✅ Gate PASSED (100% decision influence, 67% decision change rate, 15-25x ROI)

**Risk 2: Premature automation** (Inertia Loop avoided)
- **Risk**: Building Commodity automation before validating Genesis manual practice
- **Mitigation**: Practice-first approach (Phase 1 manual → Phase 2 document → Phase 3 validate → Phase 4 automate selectively)
- **Result**: ✅ Manual workflow validated, automation deferred to Phase 4 (only if criteria met)

**Risk 3: External tool adoption mismatch** (Build vs Buy)
- **Risk**: External Wardley tools don't integrate with chora ontology (feature-manifest.yaml, L0-L5, SAP lifecycle)
- **Mitigation**: chora-native approach from Phase 1 (deep ontology integration, no external dependencies)
- **Result**: ✅ 90%+ ontology overlap validated (minimal translation needed)

### Risks Remaining (Phase 2-4)

**Risk 4: External adoption failure** (Phase 3)
- **Risk**: Protocol-spec.md unclear, external adopters can't create maps following protocol (clarity <80%)
- **Mitigation**: Pilot with 2-3 additional maps in Phase 3, track protocol clarity, refine to v1.1.0 if needed
- **Fallback**: If clarity <80%, iterate on protocol-spec.md before distributing to external repos

**Risk 5: Low frequency invalidates automation** (Phase 4)
- **Risk**: Only 1-2 maps per quarter created (below 10+ threshold for automation)
- **Mitigation**: Track frequency in Phase 3, defer automation unless criteria met (30+ min AND 10+ reps AND 20% error)
- **Fallback**: Keep manual workflow if frequency low (manual acceptable for quarterly strategic practice)

**Risk 6: Strategic gameplay complexity** (Phase 4)
- **Risk**: Codifying 8 strategic principles as algorithms is intractable (requires expert judgment)
- **Mitigation**: Document heuristics in protocol-spec.md, keep gameplay identification manual
- **Fallback**: Don't automate gameplay (expert judgment required, not algorithmic)

---

## Dependencies

### Prerequisites (Existing Capabilities)

**Required** (already at L3+):
- ✅ **SAP-056 (Traceability)**: feature.dependencies extracted for value chain analysis
- ✅ **feature-manifest.yaml**: Component metadata (status, maturity, dependencies)
- ✅ **L0-L5 Maturity Model**: Evolution classification foundation

**Recommended** (enhances value):
- ✅ **SAP-013 (Metrics)**: Maturity level tracking
- ✅ **SAP-010 (Memory)**: (Phase 4, optional) Activity pattern extraction

### Enablers (What SAP-064 Unlocks)

**Direct**:
- SAP-056 acceleration prioritized (bottleneck removal, co-evolution with Wardley)
- SAP-063 creation (Documentation Patterns meta-SAP, ecosystem play)
- Strategic roadmap refinement (evidence-based positioning vs intuition)

**Indirect**:
- Cross-repo integration analysis (chora-workspace, chora-base, chora-compose)
- Meta-SAP evolution planning (SAP-065 Development Lifecycle Meta-SAPs)
- Quarterly strategic reviews (institutionalized Wardley practice at L5)

---

## Resource Allocation

### Phase 2: SAP-064 Creation (Current)

**Time Investment**: 8.5-14.5 hours (1-2 days focused work)
- Task 2.1: protocol-spec.md ✅ COMPLETE (2-3 hours)
- Task 2.2: SAP-064 artifacts ⏳ IN PROGRESS (3.5-5.5 hours)
- Task 2.3: Pilot adoption ⏳ PENDING (3-6 hours)

**Deliverables**: 5 artifacts (protocol-spec.md, charter, blueprint, awareness-guide, ledger)

---

### Phase 3: External Validation

**Time Investment**: 6-12 hours (1-2 days)
- 2-3 additional maps × 60-90 min each = 3-4.5 hours
- Documentation and refinement = 2-3 hours
- Pain point tracking and analysis = 1-2 hours
- Protocol-spec.md v1.1.0 iteration (if needed) = 1-2 hours

**Deliverables**: 2-3 map files, strategic session notes, ledger entries, protocol refinement

---

### Phase 4: Selective Automation (Optional)

**Time Investment**: 3-5 days (ONLY if selective automation criteria met)
- Value chain analyzer script = 1-2 days
- Component extractor script = 1-2 days (DEFER unless frequency validates)
- Testing and validation = 1 day

**Deliverables**: scripts/wardley-value-chain-analyzer.py (IF justified)

---

## Governance

### Maturity Progression

**Current**: L1 (Planned)
- Phase 2 artifacts in progress

**Target (End of Phase 3)**: L3 (Validated)
- 2+ adoptions (Phase 1 chora-workspace + Phase 3 pilot maps)
- Protocol clarity validated (80%+ external adopter survey)
- Strategic value demonstrated (1+ decision influenced per map)

**Long-term (Phase 4+)**: L4-L5 (Distributed, Sustained)
- L4: 5+ adoptions (external repos: chora-compose, chora-github)
- L5: Quarterly strategic mapping practice institutionalized

### Review Cadence

**Phase 2-3** (Current):
- Daily check-ins during artifact creation (Task 2.2)
- Post-map retrospectives during pilot adoption (Task 2.3)

**Post-L3**:
- Quarterly strategic reviews (use Wardley maps for roadmap planning)
- Semi-annual SAP-064 maturity assessment (track adoption, protocol clarity, ROI)

---

## References

### Phase 1 Evidence

- [chora-ecosystem-map-2025-11-manual.md](../../../docs/wardley/chora-ecosystem-map-2025-11-manual.md) - First manual map (15 components, 4 layers)
- [strategic-session-notes-2025-11.md](../../../docs/wardley/strategic-session-notes-2025-11.md) - 6 strategic questions, 100% decision influence
- [phase-1-gate-decision.md](../../../docs/wardley/phase-1-gate-decision.md) - Gate PASSED (0.95 confidence, 15-25x ROI)

### Protocol and Implementation

- [protocol-spec.md](protocol-spec.md) - Manual workflow documentation (Phase 1 validated)

### Strategic Context

- [OPP-2025-038](../../../../inbox/opportunities/OPP-2025-038-wardley-mapping-strategic-positioning.md) - Opportunity document (practice-first implementation plan)
- [wardley-capability-roadmap-2025-11.md](../../../../project-docs/plans/wardley-capability-roadmap-2025-11.md) - Detailed roadmap (Phase 1-4 task breakdowns)

---

**Version**: 1.0.0
**Status**: Phase 2 (SAP Creation)
**Maturity**: L1 (Planned)
**Created**: 2025-11-20
**Author**: tab-1 (Claude Code)
**Trace ID**: wardley-phase-2-2025-11
**Next**: Create adoption-blueprint.md (Task 2.2, Artifact 2)
