# RFCs (Requests for Comments)

**Status:** Accepted proposals under active discussion
**Purpose:** Collaborative design before implementation
**Review:** Continuous (async via GitHub comments/discussions)

---

## Purpose

This directory contains **accepted strategic proposals** that are being refined through collaborative discussion before implementation.

## Lifecycle

```
inbox/ecosystem/proposals/  (proposed)
          ↓ quarterly review
          ↓ ACCEPTED
inbox/ecosystem/rfcs/       (under discussion) ← YOU ARE HERE
          ↓ design finalized
inbox/ecosystem/adrs/       (decision recorded)
          ↓ implementation begins
inbox/incoming/coordination/ (cross-repo tasks created)
```

---

## RFC Format

RFCs follow a structured format adapted from Rust RFC process:

```markdown
---
rfc: [number]
title: RFC Title
status: draft | final-comment-period | accepted | withdrawn
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# RFC [Number]: [Title]

## Summary
One paragraph explanation of the feature.

## Motivation
Why are we doing this? What use cases does it support? What is the expected outcome?

## Guide-level explanation
Explain the proposal as if it was already implemented and you were teaching it to another developer. That generally means:

- Introducing new named concepts.
- Explaining the feature largely in terms of examples.
- Explaining how developers should *think* about the feature, and how it should impact the way they use the ecosystem.

## Reference-level explanation
This is the technical portion of the RFC. Explain the design in sufficient detail that:

- Its interaction with other features is clear.
- It is reasonably clear how the feature would be implemented.
- Corner cases are dissected by example.

## Drawbacks
Why should we *not* do this?

## Rationale and alternatives
- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not choosing them?
- What is the impact of not doing this?

## Prior art
Discuss prior art, both the good and the bad, in relation to this proposal.

## Unresolved questions
- What parts of the design do you expect to resolve through the RFC process before this gets merged?
- What parts of the design do you expect to resolve through the implementation of this feature before stabilization?
- What related issues do you consider out of scope for this RFC that could be addressed in the future independently of the solution that comes out of this RFC?

## Future possibilities
Think about what the natural extension and evolution of your proposal would be and how it would affect the ecosystem holistically.
```

---

## Review Process

### Active Discussion
- RFCs are discussed via GitHub Issues/Discussions
- Anyone can comment and contribute
- Changes incorporated via pull requests
- Aim for consensus, not unanimous agreement

### Final Comment Period
- When design is stable, enter "final comment period" (FCP)
- Announced to team (1 week minimum)
- Last chance for objections
- After FCP, move to acceptance or withdrawal

### Acceptance
- RFC accepted → move to [`inbox/ecosystem/adrs/`](../adrs/)
- Create ADR documenting the decision
- Generate implementation tasks → `inbox/incoming/coordination/`
- Update ROADMAP.md with timeline

---

## Active RFCs

*None yet - this is a new process!*

---

## Completed RFCs

See [`inbox/ecosystem/adrs/`](../adrs/) for finalized decisions.

---

## RFC Numbering

RFCs are numbered sequentially: `0001-title.md`, `0002-title.md`, etc.

To create a new RFC:
1. Copy template above
2. Use next available number
3. Create as `rfcs/NNNN-your-title.md`
4. Open GitHub Issue for discussion
5. Link RFC file in issue description

---

## Questions?

See:
- [INBOX_PROTOCOL.md](../../INBOX_PROTOCOL.md) - Complete intake process
- [INTAKE_TRIAGE_GUIDE.md](../../INTAKE_TRIAGE_GUIDE.md) - Decision criteria
