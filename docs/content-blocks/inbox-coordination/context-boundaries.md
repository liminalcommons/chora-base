# Context Boundaries Content Block

## Description

Optional field explicitly stating what the requester is **NOT** asking for. Clarifies boundaries and scope to prevent misunderstandings, especially in exploratory requests where recipients might assume broader commitment than intended. Demonstrates thoughtfulness and respect for recipient's concerns.

**When to use**: Exploratory cross-repository requests where scope ambiguity could create anxiety or false assumptions. Rare in prescriptive requests (deliverables define positive scope) and internal requests (boundaries more obvious). Present in ~15-25% of exploratory external requests.

## Fields / Structure

```json
{
  "context": {
    "not_requesting": "Explicit statement of what we are NOT asking for. May include scope boundaries, non-commitments, or common misinterpretations to preempt. 1-3 paragraphs typical."
  }
}
```

**Alternative naming**:
```json
{
  "context": {
    "boundaries": "...",
    "scope_exclusions": "...",
    "what_we_are_not_asking": "..."
  }
}
```

### Field Specifications

- **context.not_requesting**: String (50-300 words typical)
- States explicit boundaries or exclusions
- Addresses common concerns or misinterpretations
- May explain what future phases *might* involve (but not committing now)
- Tone: Reassuring and clarifying (not defensive)

## Template / Example

```json
{
  "context": {
    "not_requesting": "{{boundary_1}}\n\n{{boundary_2}}\n\n{{boundary_3}}"
  }
}
```

## Variation Points

### Exploratory Request (Scope Boundaries)

Clarifies that exploration doesn't commit to implementation:

```json
{
  "context": {
    "not_requesting": "We want to be clear about what we are NOT requesting in this exploration:\n\n- We are NOT asking chora-compose to modify its architecture to accommodate chora-base's specific needs. If integration requires changes to chora-compose core, that's a signal to explore alternative approaches.\n\n- We are NOT expecting chora-compose team to implement our inbox automation. This exploration is about feasibility and learning—if we proceed to pilot or implementation, chora-base will own the development work (content configs, integration scripts, etc.).\n\n- We are NOT committing to adopt chora-compose regardless of exploration findings. We have a clear GO/NO-GO decision framework (≥80% technical feasibility, team capacity, quality threshold). If feasibility is low or integration effort is prohibitive, we'll pursue alternatives.\n\n- We are NOT asking for immediate action. This is discovery work with a 1-2 week timeline for the exploration phase. Any future collaboration (pilot, implementation) would be separately scoped with explicit mutual agreement."
  }
}
```

**Characteristics**:
- 4 explicit "NOT requesting" statements
- Addresses potential concerns (architecture changes, implementation burden, forced adoption, immediate commitment)
- Reassures recipient (we own the work, we have alternatives, no pressure)
- Typical for exploratory requests to external repos

### Partnership Request (Commitment Boundaries)

Clarifies that initial engagement doesn't imply long-term partnership:

```json
{
  "context": {
    "not_requesting": "Important boundaries for this initial engagement:\n\n- This is NOT a commitment to long-term strategic partnership. We're starting with a focused 4-week pilot to validate the approach. Both teams will have a decision point at week 4 to determine if deeper collaboration makes sense.\n\n- We are NOT expecting chora-compose to adopt chora-base's processes or conventions. We're exploring whether chora-compose's existing patterns work for our use case, not asking you to change yours.\n\n- We are NOT requesting exclusive relationship or preventing you from collaborating with other ecosystem repos on similar use cases. Broader ecosystem adoption would actually strengthen the value proposition."
  }
}
```

**Characteristics**:
- 3 boundaries around commitment, process adoption, exclusivity
- Reassures recipient (no lock-in, no process changes, no exclusivity demands)
- Appropriate for requests that could evolve into partnership

### Peer Review Request (Scope Limitations)

Clarifies what aspects are in/out of scope for review:

```json
{
  "context": {
    "not_requesting": "To keep this review focused and respectful of your time, we are NOT asking for:\n\n- Line-by-line code review of implementation examples. We're seeking architectural and pattern guidance, not detailed code critique.\n\n- Comparison with every possible React library or framework. Our SAPs focus on core React patterns applicable across ecosystem projects, not comprehensive React ecosystem coverage.\n\n- Rewriting or heavy editing of our documentation. We're looking for feedback and recommendations that we can implement, not asking you to do the writing.\n\n- Immediate turnaround. We understand peer review takes time. 2-3 weeks is our target, but we're flexible if you need more time."
  }
}
```

**Characteristics**:
- 4 scope exclusions (code review, comprehensive comparison, rewriting, rushed timeline)
- Reduces reviewer burden (focus on high-level, not details)
- Sets realistic timeline expectations

### No Boundaries (Prescriptive or Internal)

Most requests omit this field:

```json
{
  "context": {
    "not_requesting": null
  }
}
```
*Note: Field omitted entirely*

**When to omit**:
- Prescriptive requests (positive scope is clear)
- Internal coordination (boundaries understood)
- Simple, unambiguous requests
- Emergency requests (no time for boundary clarification)

## Usage Guidance

### When Boundaries Add Value

**Use boundaries when**:
- Exploratory request to external repo (prevent scope anxiety)
- Request could be misinterpreted as broader commitment
- Prior similar requests led to misunderstandings
- Recipient might reasonably assume larger ask
- First-time coordination with recipient (building trust)

**Skip boundaries when**:
- Scope is unambiguous from deliverables
- Internal request (shared context)
- Recipient knows your norms (established relationship)
- Emergency (focus on what IS needed)

### Boundary Types

#### Scope Boundaries
What's excluded from this request:
```
"We are NOT asking for comprehensive rewrite of all artifact types—just coordination requests for now."
```

#### Commitment Boundaries
What we're not committing to long-term:
```
"This exploration does NOT commit us to adoption—we have clear GO/NO-GO criteria."
```

#### Effort Boundaries
What we're not asking recipient to do:
```
"We are NOT expecting you to implement this—we'll own development if we proceed."
```

#### Timeline Boundaries
What we're not demanding immediately:
```
"We are NOT asking for immediate action—exploration has 2-week timeline, no rush."
```

#### Relationship Boundaries
What we're not assuming about partnership:
```
"This is NOT a request for exclusive relationship—ecosystem-wide collaboration is fine."
```

### Tone Guidelines

**Good tone** (reassuring, clarifying):
```
"We want to be clear about what we are NOT requesting..."
"Important boundaries for this engagement..."
"To keep this focused and respectful of your time..."
```

**Poor tone** (defensive, apologetic):
```
"We promise we're not trying to..."
"Please don't think we're asking for..."
"Sorry if this seems like a big ask but..."
```

**Good boundaries** (specific and reassuring):
```
"We are NOT asking chora-compose to modify its core architecture to accommodate our needs. If integration requires core changes, that's a signal to explore alternatives."
```

**Poor boundaries** (vague and unhelpful):
```
"We're not asking for too much."
"We don't want to burden you."
```

### Framing Patterns

#### The "We Own It" Pattern
Clarifies recipient is not expected to implement:
```
"We are NOT expecting you to implement our inbox automation. chora-base will own development work (content configs, integration scripts, maintenance). We're seeking expertise and guidance, not implementation labor."
```

#### The "No Commitment" Pattern
Clarifies exploration doesn't obligate adoption:
```
"This exploration does NOT commit either team to adoption or partnership. We have clear decision criteria (≥80% feasibility, team capacity) and explicit exit points."
```

#### The "Focused Scope" Pattern
Clarifies boundaries within larger domain:
```
"We are NOT requesting comprehensive solution for all artifact types. This pilot focuses specifically on coordination requests (1 of 3 artifact types). Tasks and proposals are future possibilities, not current scope."
```

#### The "Flexible Timeline" Pattern
Clarifies no pressure for immediate action:
```
"We are NOT asking for immediate action or rushed response. Exploration has 2-week suggested timeline, but we're flexible if your capacity requires longer. Quality guidance beats quick response."
```

### Relationship to Positive Scope

Boundaries complement positive scope (deliverables, questions):

**Deliverables** (what we ARE requesting):
```json
{
  "deliverables": [
    "Feasibility assessment",
    "Integration options comparison",
    "Recommendation on pilot"
  ]
}
```

**Boundaries** (what we are NOT requesting):
```json
{
  "context": {
    "not_requesting": "We are NOT asking you to implement our pilot, modify chora-compose architecture, or commit to long-term partnership. This is discovery work to inform our decision."
  }
}
```

**Together**: Clear positive and negative scope reduces ambiguity.

### Automation Notes

- **AI Generation**: Can infer boundaries from context.background and common concerns
- **Concern Detection**: AI can identify potential misinterpretations (e.g., "Are they asking us to rewrite our system?")
- **Tone Calibration**: AI should use reassuring tone (not defensive or apologetic)
- **Validation**: Check boundaries are meaningful (not obvious "we're not asking you to drop everything")

## Validation Rules

- `context.not_requesting` field is **optional** (valuable in ~15-25% of exploratory requests)
- If present, minimum 30 words (shorter suggests insufficient clarity)
- Maximum 500 words (longer suggests over-explanation)
- Should be phrased positively (reassuring) not defensively (apologetic)
- Should address realistic concerns (not obvious non-requests)

## Related Content Blocks

- [context-background.md](context-background.md) - Positive context (what we're doing)
- [context-rationale.md](context-rationale.md) - Why this approach (complements boundaries)
- [deliverables-structure.md](deliverables-structure.md) - Positive scope (what we ARE requesting)
- [collaboration-modes.md](collaboration-modes.md) - Engagement options (flexible boundaries)

## Examples from Real Requests

### Example 1: Exploratory Request with Comprehensive Boundaries (COORD-2025-002)

```json
{
  "context": {
    "not_requesting": "We want to be very clear about what we are NOT requesting or assuming:\n\n**Not Requesting Architecture Changes**: We are NOT asking chora-compose to modify its core architecture, add chora-base-specific features, or accommodate our idiosyncrasies. If our SAP-001 schemas don't map well to chora-compose's structures, that's valuable information that would lead us to explore alternatives—not a request for you to change.\n\n**Not Expecting Implementation Work**: We are NOT asking the chora-compose team to implement our inbox automation. This exploration is about learning and feasibility assessment. If we proceed to pilot or full implementation, chora-base will own the development work: creating content configs, building integration scripts, maintaining our content block library, and troubleshooting our use case.\n\n**Not Committing to Adoption**: This exploration does NOT represent a commitment from chora-base to adopt chora-compose regardless of findings. We have a structured decision framework with clear GO/NO-GO criteria (≥80% technical feasibility, adequate team capacity, ≥80% quality threshold via SAP-004 rubric). If feasibility is medium or low, we'll pursue alternative approaches (custom tooling or existing template engines).\n\n**Not Demanding Immediate Action**: We are NOT asking for immediate response or rushed collaboration. Our exploration timeline is 1-2 weeks (ending Nov 8), but we understand you have your own priorities and timelines. If capacity constraints delay response, we can adjust our timeline or proceed with self-directed research using existing documentation. Quality guidance is more valuable than quick response.\n\n**Not Assuming Exclusivity**: If you're working with other ecosystem repos on similar artifact generation use cases, that's fantastic—it would actually strengthen the ecosystem value proposition. We're not seeking exclusive relationship or partnership."
  }
}
```

**Analysis**:
- 5 major boundaries (architecture, implementation, commitment, timeline, exclusivity)
- Each boundary addresses a realistic concern recipient might have
- Reassuring tone ("that's valuable information", "we understand")
- Specific details (≥80% threshold, 1-2 week timeline, decision framework)
- Demonstrates thoughtfulness and respect
- Appropriate for first-time cross-repo exploratory request
- ~280 words (comprehensive but not excessive)

### Example 2: Peer Review Request with Scope Boundaries (coord-005)

```json
{
  "context": {
    "not_requesting": "To keep this review focused and manageable, we want to clarify what we are NOT requesting:\n\n**Not Line-by-Line Code Review**: We're seeking architectural and pattern-level feedback, not detailed code critique of every example. High-level assessment of whether examples are representative and clear is sufficient.\n\n**Not Comprehensive React Ecosystem Comparison**: Our SAPs intentionally focus on core React patterns applicable across ecosystem projects. We're not trying to cover every React library, framework, or edge case—just the foundational patterns teams need.\n\n**Not Asking You to Rewrite**: We're looking for feedback and recommendations that we (chora-workspace) can act on. We're not asking chora-base reviewers to rewrite documentation or provide ready-to-merge edits.\n\n**Not Rushing Timeline**: While we'd love feedback within 2-3 weeks, we understand peer review is a time-intensive gift. If you need more time, or can only provide partial review, that's completely acceptable and appreciated."
  }
}
```

**Analysis**:
- 4 boundaries (code review depth, comprehensiveness, implementation, timeline)
- Reduces reviewer burden (focus on high-level patterns)
- Sets realistic expectations (2-3 weeks preferred, flexible)
- Tone: Appreciative and flexible ("gift", "completely acceptable")
- Appropriate for peer review where scope could expand
- ~150 words (concise but clear)

### Example 3: No Boundaries (Prescriptive - COORD-2025-004)

```json
{
  "context": {
    "not_requesting": null
  }
}
```
*Note: Field omitted entirely*

**Analysis**:
- Prescriptive internal request with clear deliverables
- Scope is unambiguous from deliverables and acceptance criteria
- Internal coordination (boundaries understood from shared context)
- No benefit to stating obvious boundaries

## Common Patterns by Request Type

| Request Type | Boundaries Present? | Typical Count | Focus | Purpose |
|--------------|-------------------|---------------|-------|---------|
| Exploratory (External) | 50-60% | 3-5 | Architecture changes, implementation work, commitment | Prevent scope anxiety |
| Exploratory (Internal) | <10% | 1-2 | Scope limitations only | Shared context makes most obvious |
| Prescriptive | <5% | - | - | Deliverables define positive scope |
| Peer Review | 20-30% | 2-4 | Review depth, rewrites, timeline | Manage reviewer burden |
| Emergency (P0) | 0% | - | - | No time for boundary clarification |

## Boundaries and Trust Building

Explicit boundaries build trust in cross-repo coordination:

**Without boundaries** (recipient may worry):
```
Request: "We want to explore using chora-compose for inbox automation..."
Recipient thinks: "Are they expecting us to rewrite our system? Will this become a huge time sink? Are they going to demand we support their use case forever?"
→ Anxiety, hesitation, possibly decline
```

**With boundaries** (recipient reassured):
```
Request: "We want to explore using chora-compose for inbox automation..."
Boundaries: "We're NOT asking you to modify architecture, implement our use case, or commit long-term. Just feasibility guidance."
Recipient thinks: "Oh, low-risk exploration. They own the work. Clear decision criteria. I can do that."
→ Confidence, more likely to engage
```

## Boundaries vs Risk Mitigation

Boundaries are **preemptive** risk mitigation:

**Without boundaries** (reactive):
```
Request sent → Recipient worried → They ask clarifying questions → We clarify → Several days lost
```

**With boundaries** (proactive):
```
Request sent (with boundaries) → Recipient reassured → Accepts with appropriate mode → Collaboration begins
```

**Value**: Saves time, reduces friction, builds trust from first contact.

## Metadata

- **Priority**: LOW (present in ~15-25% of requests, mostly exploratory to external repos)
- **Stability**: Stable (rarely changes, reflects initial scope understanding)
- **Reusability**: Moderate (pattern applies to external requests, content varies by concerns)
- **Generation Source**: AI generation from context + concern detection, user refinement for tone
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
