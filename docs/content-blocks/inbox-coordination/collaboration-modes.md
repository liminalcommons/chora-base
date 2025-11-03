# Collaboration Modes Content Block

## Description

Optional field offering different engagement levels or collaboration styles to the recipient. Most common in **exploratory requests** to external repositories, where the requester wants to be flexible and respectful of the recipient's capacity and preferences. Demonstrates humility and partnership orientation.

**When to use**: Exploratory cross-repository requests where multiple engagement levels are acceptable. Rare in prescriptive requests (specific deliverables defined) and internal requests (collaboration mode implicit). Present in ~20-30% of exploratory external requests.

## Fields / Structure

```json
{
  "collaboration_modes": [
    "Mode 1: Description of high-engagement option",
    "Mode 2: Description of medium-engagement option",
    "Mode 3: Description of low-engagement option"
  ]
}
```

**Alternative structure** (with metadata):
```json
{
  "collaboration_modes": {
    "High Engagement": {
      "description": "Detailed collaboration with...",
      "effort": "15-20 hours",
      "outcome": "Comprehensive assessment"
    },
    "Medium Engagement": {
      "description": "Focused review of...",
      "effort": "8-12 hours",
      "outcome": "Targeted recommendations"
    },
    "Low Engagement": {
      "description": "Quick feedback on...",
      "effort": "2-4 hours",
      "outcome": "High-level guidance"
    }
  }
}
```

### Field Specifications

- **collaboration_modes**: Array of strings OR object with mode details
- Typically 2-5 modes offered (ordered high → low engagement)
- Each mode describes what recipient would contribute
- May include estimated effort per mode
- Demonstrates flexibility and respect for recipient capacity

## Template / Example

**Simple array**:
```json
{
  "collaboration_modes": [
    "{{mode_1_high_engagement}}",
    "{{mode_2_medium_engagement}}",
    "{{mode_3_low_engagement}}"
  ]
}
```

**Structured with metadata**:
```json
{
  "collaboration_modes": {
    "{{Mode_Name_1}}": {
      "description": "{{what_recipient_contributes}}",
      "effort": "{{estimated_hours}}",
      "outcome": "{{expected_deliverable}}"
    }
  }
}
```

## Variation Points

### Exploratory Request (Flexible Engagement)

Offers multiple levels from deep collaboration to light feedback:

```json
{
  "collaboration_modes": [
    "Deep Collaboration: Joint exploration where we work together to map SAP-001 schemas to chora-compose structures, prototype 2-3 content configs, and co-develop integration design. Your expertise in chora-compose architecture would be invaluable. Estimated effort: 15-20 hours over 2-3 weeks.",

    "Expert Consultation: You provide architectural guidance through async discussion (GitHub issues, documentation review, 1-2 video calls). We do the prototyping and come back with specific questions. Estimated effort: 8-12 hours over 2-3 weeks.",

    "Documentation-Driven: We study existing chora-compose docs and examples, you review our draft integration design and provide written feedback on feasibility and approach. Estimated effort: 4-6 hours (documentation review + written feedback).",

    "High-Level Guidance: Quick assessment (30-60 min call or written response) on whether our use case aligns with chora-compose's design intent, with pointers to relevant examples or documentation. Estimated effort: 1-2 hours.",

    "Async Resource Sharing: You point us to relevant documentation, examples, or issues that address similar use cases. We proceed independently and report back findings. Estimated effort: <1 hour (resource curation)."
  ]
}
```

**Characteristics**:
- 5 modes from high (15-20 hours) to low (<1 hour)
- Each mode specifies what recipient contributes
- Estimated effort helps recipient choose
- Demonstrates respect for recipient's time
- Typical for exploratory requests to external repos with unknown capacity

### Peer Review Request (Review Depth Options)

Offers different review depths:

```json
{
  "collaboration_modes": [
    "Comprehensive Review: Detailed technical review of all 6 React SAPs (SAP-020 through SAP-025) with written feedback on architecture, patterns, examples, and ecosystem alignment. Estimated effort: 8-10 hours.",

    "Focused Review: Select 2-3 SAPs to review in depth, providing detailed feedback on those while offering high-level feedback on the remainder. Estimated effort: 4-6 hours.",

    "High-Level Assessment: Read through all SAPs and provide general feedback on overall quality, major gaps, and ecosystem alignment (without detailed line-by-line review). Estimated effort: 2-3 hours.",

    "Spot Check: Review one representative SAP (you choose) and extrapolate feedback to the set. Estimated effort: 1-2 hours."
  ]
}
```

**Characteristics**:
- 4 modes with decreasing depth
- All modes valuable (even spot check provides signal)
- Effort ranges from 1-2 hours to 8-10 hours
- Appropriate for peer review where any level of feedback is helpful

### Partnership Request (Engagement Styles)

Offers different collaboration styles for strategic partnership:

```json
{
  "collaboration_modes": [
    "Strategic Partnership: Ongoing collaboration where chora-base and chora-compose jointly develop inbox automation as a reference implementation for ecosystem artifact generation. Includes regular sync meetings, shared roadmap planning, and co-marketing. Long-term commitment.",

    "Pilot Collaboration: Work together on 4-week pilot to validate integration approach, with decision point at end to determine if partnership continues. Structured engagement with clear success criteria.",

    "Technical Advisory: chora-compose team provides technical guidance and reviews our integration work, but we own implementation and maintenance. Async collaboration via GitHub issues and occasional calls.",

    "Independent Integration: We proceed independently using public chora-compose APIs and documentation, filing issues as needed. chora-compose team treats us as standard external users."
  ]
}
```

**Characteristics**:
- 4 modes from deep partnership to independent use
- Each mode defines relationship structure
- No effort estimates (strategic decision, not effort-driven)
- Appropriate for requests that could evolve into partnership

### No Collaboration Modes (Prescriptive or Internal)

Most requests omit this field:

```json
{
  "collaboration_modes": null
}
```
*Note: Field omitted entirely*

**When to omit**:
- Prescriptive requests (deliverables already specified)
- Internal coordination (collaboration mode implicit)
- Emergency requests (no time for mode selection)
- Requests with single clear engagement model

## Usage Guidance

### Mode Design Principles

**Progressive Reduction** (high → low engagement):
- Start with most comprehensive option
- Each subsequent mode reduces scope or depth
- All modes valuable (not "ideal vs fallback")
- Recipient chooses based on capacity and interest

**Clear Differentiation**:
- Each mode should be distinctly different (not minor variations)
- Effort differences should be meaningful (2x or more)
- Outcomes should map to different effort levels

**Respect and Flexibility**:
- Frame all modes as valuable (not "best vs bare minimum")
- Avoid guilt-tripping language ("if you have time...")
- Emphasize recipient's choice and agency

### Effort Specification

**Include effort estimates when**:
- Modes differ significantly in time commitment
- Recipient needs to plan capacity
- Request is to external team (less context on scope)

**Format options**:
```
"Estimated effort: 15-20 hours over 2-3 weeks"
"Estimated effort: 4-6 hours (async, over 1-2 weeks)"
"Estimated effort: 1-2 hours (30-60 min call + brief follow-up)"
"Estimated effort: <1 hour (quick resource sharing)"
```

### Outcome Clarity

Each mode should specify what deliverable or outcome results:

```
"Deep Collaboration: ... → Outcome: Co-developed integration design with prototypes"
"Expert Consultation: ... → Outcome: Architectural guidance document"
"High-Level Guidance: ... → Outcome: Quick assessment with pointers"
```

This helps recipient assess value vs effort.

### Typical Mode Patterns

**3-Mode Pattern** (Simple):
```
1. High engagement (comprehensive, 10-15 hours)
2. Medium engagement (focused, 4-6 hours)
3. Low engagement (guidance, 1-2 hours)
```

**5-Mode Pattern** (Flexible):
```
1. Deep collaboration (joint work, 15-20 hours)
2. Active consultation (guidance + review, 8-12 hours)
3. Documentation-driven (async review, 4-6 hours)
4. High-level guidance (quick assessment, 1-2 hours)
5. Resource sharing (pointers, <1 hour)
```

**2-Mode Pattern** (Binary):
```
1. Collaborative (work together, 10-15 hours)
2. Independent (we do it, you review, 2-4 hours)
```

### Tone and Framing

**Good** (respectful, empowering):
```
"We'd value collaboration at any level that fits your capacity and interest. Here are some options we've thought through:"
```

**Poor** (guilt-tripping, hierarchical):
```
"We really need your help but understand if you're too busy. The bare minimum would be..."
```

**Good mode descriptions**:
```
"Expert Consultation: You provide architectural guidance through async discussion. Your chora-compose expertise would help us avoid pitfalls. Estimated effort: 8-12 hours."
```

**Poor mode descriptions**:
```
"Option 2: If you don't have time for full collaboration, maybe you could at least answer some questions."
```

### When NOT to Offer Modes

**Don't offer modes when**:
- Prescriptive request with specific deliverables
- Internal request (collaboration style established)
- Emergency (no time for mode selection)
- Only one engagement model makes sense

**Example anti-pattern**:
```json
{
  "deliverables": [
    "SAP-009 v1.1.0 specification",
    "Implementation with tests",
    "Documentation updates"
  ],
  "collaboration_modes": [
    "Full implementation (40-60 hours)",
    "Partial implementation (20-30 hours)",
    "Just the spec (5-10 hours)"
  ]
}
```
**Issue**: This is scope negotiation, not collaboration modes. Should be in deliverables or clarified during triage.

### Automation Notes

- **AI Generation**: Can draft modes from context.background and deliverables
- **Effort Estimation**: Can suggest effort ranges based on mode scope
- **Outcome Mapping**: Can draft expected outcomes per mode
- **Validation**: Check that modes are meaningfully different (not minor variations)

## Validation Rules

- `collaboration_modes` field is **optional** (useful in ~20-30% of exploratory requests)
- If present, must be array of strings OR object with mode details
- Recommended 2-5 modes (fewer suggests false choice, more suggests over-complexity)
- Modes should be ordered (typically high → low engagement)
- Each mode should be distinct (meaningful effort/scope differences)
- Tone should be respectful and empowering (not guilt-tripping)

## Related Content Blocks

- [deliverables-structure.md](deliverables-structure.md) - What's delivered (may vary by mode)
- [exploratory-questions.md](exploratory-questions.md) - Questions may vary by engagement mode
- [estimated-effort-guide.md](estimated-effort-guide.md) - Overall effort (sum of both parties)

## Examples from Real Requests

### Example 1: Exploratory Request with 5 Modes (COORD-2025-002)

```json
{
  "collaboration_modes": [
    "Deep Collaboration: Joint exploration where we work together to map SAP-001 schemas to chora-compose structures, prototype 2-3 content configs, and co-develop integration design. Your chora-compose architecture expertise would be invaluable for ensuring alignment. Estimated effort: 15-20 hours over 2-3 weeks (sync meetings + async work).",

    "Expert Consultation: You provide architectural guidance and answer specific questions through async discussion (GitHub issues, PR reviews) or 1-2 video calls. We handle prototyping and implementation, coming to you for validation and course correction. Estimated effort: 8-12 hours over 2-3 weeks (mostly async).",

    "Documentation-Driven: We study existing chora-compose documentation, examples, and generator code. You review our draft integration design document and provide written feedback on feasibility, architecture fit, and potential issues. Estimated effort: 4-6 hours (documentation review + written feedback).",

    "High-Level Guidance: Quick assessment (30-60 min video call or detailed written response) on whether our inbox automation use case aligns with chora-compose's design intent, with pointers to relevant examples, documentation sections, or similar generators to study. Estimated effort: 1-2 hours.",

    "Async Resource Sharing: You point us to relevant documentation, example generators, GitHub issues, or design documents that address similar structured artifact generation use cases. We proceed independently with self-directed research and report back our findings. Estimated effort: <1 hour (resource curation and brief guidance)."
  ]
}
```

**Analysis**:
- 5 modes covering 15-20 hours to <1 hour
- Each mode clearly describes recipient's contribution
- Effort estimates include timeframe (weeks) and format (sync/async)
- Respectful tone ("would be invaluable", "we'd value")
- All modes framed as valuable (not "ideal vs fallback")
- Demonstrates humility appropriate for external exploratory request

### Example 2: Peer Review Request (coord-005)

```json
{
  "collaboration_modes": [
    "Comprehensive Review: Detailed review of all 6 React SAPs (SAP-020 through SAP-025) with written feedback on technical accuracy, ecosystem alignment, documentation quality, and specific improvement suggestions. Estimated effort: 8-10 hours.",

    "Focused Review: Select 2-3 SAPs that you feel are most critical or representative, provide detailed feedback on those, and high-level impressions on the remainder. Estimated effort: 4-6 hours.",

    "High-Level Assessment: Read through all SAPs and provide general feedback on overall quality, major patterns or concerns, and ecosystem fit (without line-by-line review). Estimated effort: 2-3 hours.",

    "Spot Check: Review one SAP of your choice (we suggest SAP-021 React State Management as it's central) and provide feedback that we can extrapolate to the others. Estimated effort: 1-2 hours."
  ]
}
```

**Analysis**:
- 4 modes from 8-10 hours to 1-2 hours
- Each mode reduces review depth or breadth
- Suggestion in "Spot Check" mode (SAP-021) helps recipient choose
- All modes valuable (even spot check provides signal)
- Demonstrates respect for reviewer's time

### Example 3: No Collaboration Modes (Prescriptive - COORD-2025-004)

```json
{
  "collaboration_modes": null
}
```
*Note: Field omitted entirely*

**Analysis**:
- Prescriptive internal request with specific deliverables
- Collaboration style is implicit (internal team)
- No need for mode selection (scope already defined)

## Common Patterns by Request Type

| Request Type | Modes Offered? | Typical Count | Engagement Range | Purpose |
|--------------|----------------|---------------|------------------|---------|
| Exploratory (External) | 60-70% | 3-5 | <1 hour to 15-20 hours | Respect capacity, flexible partnership |
| Exploratory (Internal) | <10% | - | - | Collaboration implicit |
| Prescriptive | <5% | - | - | Deliverables define scope |
| Peer Review | 30-40% | 3-4 | 1-2 hours to 8-10 hours | Review depth flexibility |
| Emergency (P0) | 0% | - | - | No time for mode selection |

## Collaboration Modes and Decision-Making

Offering modes empowers recipient to choose engagement level:

**Without modes** (recipient must negotiate):
```
Requester: "Can you help us explore chora-compose integration?"
Recipient: "What level of involvement do you need?"
Requester: "Um... how much time do you have?"
→ Awkward negotiation, unclear expectations
```

**With modes** (recipient selects):
```
Requester: "We're exploring chora-compose integration. We've outlined 5 engagement levels from deep collaboration (15-20 hours) to resource sharing (<1 hour). Which fits your capacity and interest?"
Recipient: "Expert Consultation (8-12 hours) works for us - we'll provide guidance and review your designs."
→ Clear expectations, recipient empowered
```

## Value of Collaboration Modes

**For Recipients**:
- Clear expectations for each engagement level
- Agency to choose based on capacity and interest
- No guilt for choosing lighter engagement
- Effort estimates enable planning

**For Requesters**:
- Demonstrates respect and humility
- Increases acceptance likelihood (flexible ask)
- Builds goodwill for future collaboration
- Gets some value even if recipient chooses light mode

**For Relationship**:
- Establishes partnership mindset (not transactional)
- Builds trust through flexibility
- Enables scaled engagement (start light, deepen later)
- Models ecosystem collaboration norms

## Metadata

- **Priority**: LOW (present in ~20-30% of requests, mostly exploratory to external repos)
- **Stability**: Stable (rarely changes, though chosen mode may be documented)
- **Reusability**: Moderate (pattern applies to external requests, content varies by domain)
- **Generation Source**: AI generation from context + deliverables, user refinement for tone
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
