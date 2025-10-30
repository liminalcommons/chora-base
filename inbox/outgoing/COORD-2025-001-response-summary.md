# Response to COORD-2025-001: SAP-019 Minimal Ecosystem Entry

**From**: chora-base team
**To**: chora-workspace team
**Date**: 2025-10-29
**Response Time**: 6 hours
**Status**: ✅ Accepted with Modifications

---

## TL;DR

**Your Request**: Add SAP-019 (Minimal Ecosystem Entry) to enable 5-SAP lightweight onboarding

**Our Response**: ✅ We'll implement **SAP Sets** in Wave 5 instead of formal SAP-019

**Why**: SAP sets solve your problem better - same 5-SAP minimal entry, but more flexible, lower maintenance, and enables multiple use cases (testing-focused, MCP, custom org sets)

**What You Get**:
```bash
python scripts/install-sap.py --set minimal-entry
# Installs: SAP-000, SAP-001, SAP-009, SAP-016, SAP-002
# Result: ~29k tokens (71% reduction), 3-5 hours (90%+ time savings)
```

**Timeline**: Wave 5 completion Q1 2026 (v4.1.0)

---

## The Problem (We Agree!)

You're absolutely right that ecosystem onboarding has too much friction:

- **Current**: 18 SAPs, ~100k tokens, 2-4 weeks to full adoption
- **Pain**: Can't do cross-repo coordination without heavy upfront investment
- **Need**: Lightweight entry for ecosystem participation

**We acknowledge this is a real problem** and appreciate you bringing it to our attention via the inbox coordination protocol!

---

## The Solution: SAP Sets (Better Than Formal SAP-019)

Instead of creating a formal SAP-019 with 5 artifacts, we'll enhance Wave 5 (SAP Installation Tooling) with a **SAP Sets** feature.

### What Are SAP Sets?

**SAP sets** are curated bundles of SAPs for specific use cases, defined in `sap-catalog.json` and installable with one command.

**5 Standard Sets We'll Create**:

1. **minimal-entry** (5 SAPs) - Ecosystem onboarding ← **This is for you!**
2. **recommended** (10 SAPs) - Core dev workflow
3. **full** (18 SAPs) - Comprehensive coverage
4. **testing-focused** (6 SAPs) - Testing & quality
5. **mcp-server** (10 SAPs) - MCP development

**Plus**: Projects can define **custom sets** in `.chorabase` for organizational standards

### Why This Is Better Than Formal SAP-019

| Aspect | SAP Sets | Formal SAP-019 |
|--------|----------|----------------|
| **Installation** | One command: `--set minimal-entry` | Read SAP-019, then install 5 SAPs |
| **Flexibility** | Multiple sets (minimal, testing, MCP, custom) | Single "Bronze tier" only |
| **Maintenance** | Catalog entry (JSON) | 5 SAP artifacts to maintain |
| **Extensibility** | Custom sets via `.chorabase` | Central SAP only |
| **Philosophy** | Convenience, not prescription | Prescriptive tiers (Bronze/Silver/Gold) |
| **Use Cases** | Generalizable to many patterns | Only ecosystem entry |

**Key Insight**: You get exactly what you need (5-SAP minimal entry) without the overhead of a formal SAP or prescriptive tier terminology.

---

## The minimal-entry Set (For You!)

### Composition

**5 SAPs** selected specifically for ecosystem coordination:

| SAP ID | Name | Why Included | Tokens |
|--------|------|--------------|--------|
| **SAP-000** | sap-framework | Core SAP protocols and templates | ~7k |
| **SAP-001** | inbox-coordination | Cross-repo coordination protocol | ~5k |
| **SAP-009** | agent-awareness | AGENTS.md pattern for discoverability | ~6k |
| **SAP-016** | link-validation | Documentation quality | ~4k |
| **SAP-002** | chora-base-meta | Understanding chora-base | ~7k |
| **Total** | | | **~29k** |

### Installation

```bash
# From your repo (chora-workspace)
cd chora-workspace

# Install minimal-entry set from chora-base
python scripts/install-sap.py \
  --source ../chora-base \
  --set minimal-entry

# Output:
# Installing "Minimal Ecosystem Entry" set (5 SAPs, ~29k tokens, 3-5 hours)
#
# ✅ SAP-000: sap-framework
# ✅ SAP-001: inbox-coordination (includes inbox/ structure)
# ℹ️  Note: SAP-001 is in pilot status - may undergo changes
# ✅ SAP-009: agent-awareness (includes AGENTS.md)
# ✅ SAP-016: link-validation-reference-management
# ✅ SAP-002: chora-base-meta
#
# ✅ Set installed successfully!
#
# Next steps:
# 1. Review AGENTS.md and customize for your project
# 2. Create inbox/CAPABILITIES/chora-workspace.yaml
# 3. Add domain-specific SAP if needed (e.g., SAP-004 for testing)
```

### Impact

- **Token Reduction**: ~100k → ~29k (**71% reduction**)
- **Time Reduction**: 2-4 weeks → 3-5 hours (**90%+ reduction**)
- **Ecosystem Ready**: Inbox protocol, agent awareness, SAP framework all included
- **One Command**: No manual copying, ledger updates, or INDEX.md edits

---

## Addressing Your Concerns

### Concern 1: SAP-001 Is Pilot Status

**Your Note**: SAP-001 (inbox) has awareness score 2/4 and is in Pilot

**Our Response**:
- ✅ **Still included** in minimal-entry - it's essential for cross-repo coordination
- ⚠️ **Warning added**: install-sap.py will warn users that SAP-001 may change
- 🔄 **Plan**: When SAP-001 reaches Active, we can update set (or create minimal-entry-v2)

**Rationale**: Your use case (ecosystem coordination) **requires** inbox protocol. Pilot status is acceptable with clear warnings.

### Concern 2: Bronze/Silver/Gold Tiers

**Your Proposal**: Introduce tiered adoption (Bronze = minimal, Silver = intermediate, Gold = full)

**Our Feedback**:
- ❌ **Not adopting tier terminology** - conflicts with v4.0 flexible adoption model
- ✅ **Using "sets" instead** - convenience groupings, not prescriptive levels
- ✅ **Multiple pathways** - minimal, recommended, testing, MCP, custom (not hierarchical)

**Rationale**: v4.0 philosophy is "projects choose capabilities" not "projects climb tiers". Sets provide convenience without prescription.

### Concern 3: Maintenance Burden

**Your Proposal**: Create formal SAP-019 with 5 artifacts

**Our Feedback**:
- ❌ **5 artifacts = high maintenance** - capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger
- ✅ **SAP sets = low maintenance** - JSON catalog entry + 3 user guides
- ✅ **Easy evolution** - update set composition without SAP versioning overhead

**Benefit**: You get minimal entry feature without us maintaining a formal SAP forever.

---

## Custom Sets (Bonus Feature!)

You can define **organization-specific sets** in your `.chorabase` file:

```yaml
# chora-workspace/.chorabase
sap_sets:
  chora-workspace-minimal:
    name: "chora-workspace Minimal Entry"
    description: "Our project's standard minimal set"
    saps:
      - SAP-000  # Framework
      - SAP-001  # Inbox
      - SAP-004  # Testing (domain-specific for us)
      - SAP-009  # Agent awareness
      - SAP-016  # Link validation
    estimated_tokens: 34000
    estimated_hours: "4-6"
```

**Then**:
```bash
python scripts/install-sap.py --set chora-workspace-minimal
```

**Use Cases**:
- Standardize onboarding across your organization
- Add domain-specific SAPs to minimal entry
- Create role-specific sets (dev, QA, docs contributor)

---

## Timeline & Next Steps

### Wave 5 Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| **Wave 4 Complete** | Nov 2025 | 🔄 In Progress |
| **Wave 5 Start** | Nov 2025 | 📋 Planned |
| **Wave 5 Complete** | Q1 2026 | 📋 Planned |
| **v4.1.0 Release** | Q1 2026 | 📋 Planned |
| **Pilot Testing** | Q1 2026 | 🤝 Invitation Extended |

### Your Next Steps

**Immediate**:
1. ✅ Review this response
2. 📝 Provide feedback on minimal-entry set composition
3. 🤔 Decide if you want to pilot test Wave 5
4. 📅 Optionally: Schedule design review call to discuss

**When Wave 5 Available** (Q1 2026):
1. 📦 Install minimal-entry set in chora-workspace
2. 🧪 Test ecosystem coordination workflows
3. 💬 Provide feedback on set composition and tooling
4. 🎨 Optionally: Define custom chora-workspace-minimal set

**Workaround** (If You Need Solution Sooner):
- We can provide **manual installation instructions** for the 5 SAPs
- Not one-line, but gets you unblocked while Wave 5 is in development

---

## Open Questions for You

We'd love your feedback on these questions:

### 1. Set Composition

**Does the minimal-entry set composition meet your needs?**

Current: SAP-000, SAP-001, SAP-009, SAP-016, SAP-002

**Alternatives**:
- Add SAP-004 (testing) for test-driven ecosystem work?
- Add SAP-007 (documentation) for doc-heavy coordination?
- Replace SAP-002 (chora-base-meta) with something else?

### 2. Pilot Testing

**Would you like to pilot test Wave 5 when ready?**

**Benefits**:
- Early access to SAP sets feature
- Ability to influence design
- First-mover advantage in ecosystem

**Commitment**:
- Test minimal-entry set in chora-workspace
- Provide feedback (what works, what doesn't)
- ~4-8 hours of testing time

### 3. Additional Sets

**Are there other use-case-specific sets we should create?**

Current standard sets:
- minimal-entry
- recommended
- full
- testing-focused
- mcp-server

**Ideas**:
- workspace-focused?
- django-focused?
- react-focused?
- docs-contributor-focused?

### 4. Design Review

**Should we schedule a design review call?**

**Purpose**:
- Discuss set composition in detail
- Gather requirements from chora-workspace
- Align on approach and timeline

**Format**: Video call, 30-60 minutes

### 5. Timing

**Is Q1 2026 timeline acceptable, or is there urgency for sooner?**

**If urgent**:
- We can provide manual installation workaround
- Or prioritize minimal-entry in Wave 5 implementation

---

## Why We're Excited About This

**SAP sets solve multiple problems at once**:

1. **Your Problem**: Lightweight ecosystem entry (5 SAPs, one command)
2. **Testing Problem**: testing-focused set for QA contributors
3. **MCP Problem**: mcp-server set for MCP developers
4. **Org Problem**: Custom sets for organizational standards
5. **Future Problem**: Generalizable pattern for new use cases

**This is strategic alignment** - we're not just solving your immediate need, we're building infrastructure that benefits the entire ecosystem.

---

## How to Respond

**Via GitHub Issue**:
- Open issue in chora-base: "Feedback on COORD-2025-001 Response"
- Reference this response document

**Via Inbox Protocol**:
- Create response file: `chora-workspace/inbox/outgoing/COORD-2025-001-feedback.json`
- Push to chora-workspace, we'll monitor

**Via Email/Chat**:
- Contact chora-base maintainers directly
- Reference COORD-2025-001

**We're here to collaborate** - this response is the start of a conversation, not the end!

---

## Summary

| Aspect | Details |
|--------|---------|
| **Your Request** | SAP-019 (Minimal Ecosystem Entry) for inclusion |
| **Our Decision** | ✅ Accepted with modifications (SAP sets approach) |
| **What You Get** | One-line installation of 5-SAP minimal-entry set |
| **Benefits** | 71% token reduction, 90%+ time savings, extensible |
| **Timeline** | Q1 2026 (v4.1.0) |
| **Pilot Invitation** | Yes - extended to chora-workspace |
| **Next Step** | Your feedback on set composition |

---

**Thank you for the thoughtful proposal!** The inbox coordination protocol is working exactly as intended - identifying ecosystem needs and enabling strategic collaboration.

We're excited to build SAP sets and see chora-workspace adopt minimal-entry!

— chora-base team

**Response Date**: 2025-10-29
**Response Time**: 6 hours from COORD-2025-001 submission
**Status**: Awaiting chora-workspace feedback
