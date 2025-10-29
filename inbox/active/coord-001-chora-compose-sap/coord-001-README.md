# Coordination Request: coord-001

**Title**: Create SAP-017 & SAP-018 for chora-compose ecosystem integration
**Created**: 2025-10-28
**Status**: Awaiting Wave 2 Execution Review
**Priority**: P1 (High)

---

## Quick Start (For Wave 2 Execution Agent)

### 1. Read These Files (In Order)

1. **[coord-001-chora-compose-sap.json](coord-001-chora-compose-sap.json)** (6.4K)
   - The contract: Deliverables, acceptance criteria, timeline
   - Start here to understand WHAT is being requested

2. **[coord-001-chora-compose-sap-CONTEXT.md](coord-001-chora-compose-sap-CONTEXT.md)** (17K)
   - Complete background: Research, decisions, implementation guidance
   - Read this to understand HOW to execute

3. **[coord-001-chora-compose-sap-RATIONALE.md](coord-001-chora-compose-sap-RATIONALE.md)** (11K)
   - Explains why inbox protocol was chosen
   - Read this to understand WHY we're doing it this way

**Total reading**: ~35K (approx. 8-10k tokens)

---

## What's Being Requested

Create two SAPs to enable ecosystem repos to adopt chora-compose:

### SAP-017: chora-compose-integration
**Purpose**: How to adopt chora-compose in your repo
**Artifacts**: 5 (charter, protocol, awareness-guide, adoption-blueprint, ledger)
**Estimated Effort**: 8-12 hours

### SAP-018: chora-compose-meta
**Purpose**: Complete protocol specification (mirrors SAP-002 pattern)
**Artifacts**: 5 (charter, protocol, awareness-guide, adoption-blueprint, ledger)
**Estimated Effort**: 12-16 hours

---

## Why This Matters

**Strategic Value**:
- Enables ecosystem repos to "just know" when/how to use chora-compose
- Demonstrates 4 access modalities (pip, SAP, MCP, API)
- First cross-conversation coordination via inbox protocol
- Meta-dogfooding: Using inbox to coordinate SAP about inbox-compatible capability

**Aligns With**:
- ✅ Wave 2 Phase 2 (SAP content audit & enhancement)
- ✅ v4.0 Vision (multi-repo coordination patterns)
- ✅ Inbox protocol (cross-context coordination)

---

## Decision to Accept

### Should Wave 2 Accept This?

**Evaluate**:
- [ ] Does this fit Wave 2 goals? **Yes** - SAP content creation
- [ ] Is timing right? **Yes** - Wave 2 Phase 2 active (target Oct 31)
- [ ] Do we have bandwidth? **Yes** - can parallelize with other SAP audits
- [ ] Are dependencies met? **Yes** - SAP-000, SAP-002, SAP-016 exist
- [ ] Is context complete? **Yes** - 35K of background documentation

**If all checks pass** → Accept and move to `inbox/active/`

---

## How to Accept

```bash
# 1. Create active work directory
mkdir -p inbox/active/coord-001-chora-compose-sap

# 2. Move all coordination files
mv inbox/incoming/coordination/coord-001-* \
   inbox/active/coord-001-chora-compose-sap/

# 3. Emit acceptance event
echo '{"event_type": "coordination_accepted", "request_id": "coord-001", "trace_id": "chora-compose-sap-creation-2025-10-28", "timestamp": "'$(date -Iseconds)'", "accepted_by": "wave-2-execution", "estimated_completion": "2025-10-31"}' >> inbox/coordination/events.jsonl

# 4. Begin execution (see CONTEXT.md for detailed steps)
```

---

## How to Execute

**High-level steps** (see CONTEXT.md for detailed implementation):

1. **Create SAP-017** (8-12 hours):
   ```bash
   mkdir -p docs/skilled-awareness/chora-compose-integration
   # Create 5 artifacts using templates from SAP-000
   # Reference pattern: SAP-004 (testing-framework)
   ```

2. **Create SAP-018** (12-16 hours):
   ```bash
   mkdir -p docs/skilled-awareness/chora-compose-meta
   # Create 5 artifacts following SAP-002 pattern
   # Document complete architecture
   ```

3. **Update INDEX.md** (30 min):
   ```bash
   # Add SAP-017 and SAP-018 entries
   ```

4. **Validate** (30 min):
   ```bash
   # Run link validation (SAP-016)
   ./scripts/validate-links.sh docs/skilled-awareness/chora-compose-*
   ```

5. **Complete** (15 min):
   ```bash
   # Move to completed, emit event
   mv inbox/active/coord-001-chora-compose-sap inbox/completed/
   echo '{"event_type": "coordination_completed", ...}' >> inbox/coordination/events.jsonl
   ```

---

## Acceptance Criteria (Must All Pass)

- [ ] SAP-017 has all 5 artifacts
- [ ] SAP-018 has all 5 artifacts
- [ ] Both SAPs reference actual chora-compose docs (not hypothetical)
- [ ] Both SAPs follow 4-domain architecture pattern
- [ ] SAP-017 provides clear "when to use" decision framework
- [ ] SAP-018 documents all 17 MCP tools + 5 resources
- [ ] Future capabilities clearly marked as roadmap
- [ ] INDEX.md updated with both SAPs
- [ ] Link validation passes (no broken references)
- [ ] Demonstrates cross-conversation coordination (meta-goal)

---

## Questions?

- **What is being requested?** → Read JSON file
- **Why inbox protocol?** → Read RATIONALE.md
- **How do I execute?** → Read CONTEXT.md (implementation guidance section)
- **What's the background?** → Read CONTEXT.md (research & decision matrix)

---

## Timeline

**Proposed**: Start Oct 29, Target Oct 31
**Duration**: 2-3 days
**Effort**: 20-28 hours total

**Flexibility**: Can be parallelized with other Wave 2 SAP audits

---

## Trace ID

All events should use:
```
trace_id: chora-compose-sap-creation-2025-10-28
```

This enables correlation across:
- Strategic planning conversation (where this originated)
- Wave 2 execution conversation (where this will be implemented)
- Event logs (inbox/coordination/events.jsonl)

---

**Ready to Accept?** → Follow "How to Accept" steps above
**Questions?** → Read the three coordination files in order
**Status**: Awaiting your review

---

**Document Version**: 1.0
**Created**: 2025-10-28
**For**: Wave 2 Execution Conversation
**From**: Strategic Planning Conversation
