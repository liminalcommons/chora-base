# Core Metadata Content Block

## Description

Fundamental identifying fields present in every coordination request. These fields establish the artifact's type, unique identifier, human-readable title, and creation timestamp. This block represents the immutable foundation of any coordination request.

**When to use**: Every coordination request artifact requires this block. It is always the first section in the JSON structure.

## Fields / Structure

```json
{
  "type": "coordination",
  "request_id": "coord-NNN",
  "title": "Brief descriptive title (50-80 chars)",
  "created": "YYYY-MM-DD"
}
```

### Field Specifications

- **type**: Literal string `"coordination"` (distinguishes from "task" and "proposal" types)
- **request_id**: Pattern `coord-NNN` or `COORD-YYYY-NNN`
  - Legacy format: `coord-NNN` (e.g., "coord-005")
  - Modern format: `COORD-YYYY-NNN` (e.g., "COORD-2025-002")
  - NNN is zero-padded 3-digit sequential number
- **title**: Concise description capturing essence of request
  - Target length: 50-80 characters
  - Avoid redundant prefixes like "Coordination Request for..."
  - Use title case
- **created**: ISO 8601 date format `YYYY-MM-DD`
  - Represents when request was initially created
  - Does not change during request lifecycle

## Template / Example

```json
{
  "type": "coordination",
  "request_id": "{{request_id}}",
  "title": "{{title}}",
  "created": "{{created_date}}"
}
```

## Variation Points

### Request ID Format
- **Legacy projects**: May use `coord-NNN` format
- **New projects (2025+)**: Should use `COORD-YYYY-NNN` format for better chronological sorting

### Title Patterns by Request Type
- **Exploratory**: "Exploring [topic/system] - [purpose]"
- **Prescriptive**: "[Action] [system/feature] for [goal]"
- **Peer Review**: "Peer Review: [artifact] - [scope]"

### Creation Date
- Use UTC date at time of request composition
- Format strictly as YYYY-MM-DD (no timestamps)

## Usage Guidance

### ID Allocation
- **Manual creation**: Choose next available number in sequence
- **Automated generation**: Post-processing wrapper allocates ID from sequence file
- **Pilot workflow**: IDs allocated after generation during file promotion step

### Title Crafting
1. Start with action or topic (not "Request to...")
2. Include key context (system/feature name)
3. Indicate purpose or goal
4. Keep under 80 characters

**Good titles**:
- "Exploring chora-compose Integration for Inbox Automation"
- "Bidirectional Translation Layer for SAP-009"
- "Peer Review: React SAPs - Ecosystem Alignment"

**Poor titles**:
- "Coordination Request" (too vague)
- "Request to Explore Using chora-compose as Infrastructure Layer for SAP-001 Inbox Coordination Protocol" (too long)
- "chora-compose" (too terse)

### Automation Notes
- **type**: Always literal `"coordination"` (no placeholders needed)
- **request_id**: Leave as placeholder for post-processing
- **title**: May be AI-generated from context.purpose or user input
- **created**: Inject current date via system function

## Validation Rules

- `type` must be exactly `"coordination"`
- `request_id` must match regex: `^(coord-\d{3}|COORD-\d{4}-\d{3})$`
- `title` length must be 10-120 characters
- `created` must match regex: `^\d{4}-\d{2}-\d{2}$`
- All four fields are **required** (no optional fields in this block)

## Related Content Blocks

- [repository-fields.md](repository-fields.md) - From/to repository identification
- [trace-id-format.md](trace-id-format.md) - Optional correlation identifier
- [priority-urgency.md](priority-urgency.md) - Scheduling metadata

## Examples from Real Requests

### Example 1: Exploratory Request (COORD-2025-002)
```json
{
  "type": "coordination",
  "request_id": "COORD-2025-002",
  "title": "Exploring chora-compose Integration for Inbox Automation",
  "created": "2025-11-01"
}
```

### Example 2: Prescriptive Request (COORD-2025-004)
```json
{
  "type": "coordination",
  "request_id": "COORD-2025-004",
  "title": "Bidirectional Translation Layer for SAP-009",
  "created": "2025-10-28"
}
```

### Example 3: Peer Review Request (coord-005)
```json
{
  "type": "coordination",
  "request_id": "coord-005",
  "title": "Peer Review: React Foundation SAPs",
  "created": "2025-10-15"
}
```

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Stable (fields never change after creation)
- **Reusability**: Inbox-specific (similar patterns in task/proposal, but different type values)
- **Generation Source**: Hybrid (type is literal, ID from post-processing, title from AI/user, date from system)
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
