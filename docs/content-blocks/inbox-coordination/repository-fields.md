# Repository Fields Content Block

## Description

Identifies the source and destination repositories for a coordination request. These fields establish the directional relationship between the requester (from_repo) and the requested party (to_repo). Critical for routing, permissions, and ecosystem coordination.

**When to use**: Every coordination request, especially cross-repository requests. Even internal coordination (same repo) includes these fields for consistency.

## Fields / Structure

```json
{
  "from_repo": "github.com/org/repo-name",
  "to_repo": "github.com/org/repo-name"
}
```

### Field Specifications

- **from_repo**: Repository URL of the requesting party
  - Format: `github.com/{org}/{repo-name}` (no protocol prefix)
  - Represents who is making the request
  - May be same as to_repo for internal coordination

- **to_repo**: Repository URL of the requested party
  - Format: `github.com/{org}/{repo-name}` (no protocol prefix)
  - Represents who needs to act on the request
  - Determines where the request is routed

## Template / Example

```json
{
  "from_repo": "{{requester_repo}}",
  "to_repo": "{{recipient_repo}}"
}
```

## Variation Points

### Cross-Repository Coordination
Most common pattern for ecosystem collaboration:
```json
{
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-compose"
}
```

### Internal Coordination
Same repository for both fields when coordinating between teams/modules within a project:
```json
{
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-base"
}
```

### Multi-Party Coordination
For requests involving multiple repositories, primary recipient goes in to_repo, others in context or related fields:
```json
{
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-compose",
  "context": {
    "stakeholders": [
      "github.com/liminalcommons/chora-workspace",
      "github.com/liminalcommons/ecosystem-manifest"
    ]
  }
}
```

## Usage Guidance

### URL Format Standards
- **DO**: Use `github.com/org/repo` format
- **DON'T**: Include protocols (`https://`), `.git` suffixes, or trailing slashes
- **DON'T**: Use shorthand like `org/repo` without domain

**Good examples**:
- `github.com/liminalcommons/chora-base`
- `github.com/liminalcommons/chora-compose`

**Bad examples**:
- `https://github.com/liminalcommons/chora-base` (protocol)
- `liminalcommons/chora-base` (missing domain)
- `github.com/liminalcommons/chora-base.git` (.git suffix)
- `github.com/liminalcommons/chora-base/` (trailing slash)

### Repository Identification
- Use canonical repository URL (not forks or personal repos)
- For monorepos, use repository root (not subproject paths)
- Organization name is case-sensitive (use official capitalization)

### Internal vs External
- **Internal** (from_repo == to_repo): Typically P1-P2, shorter timelines, assumes shared context
- **External** (from_repo != to_repo): Typically P2, longer timelines, requires more context explanation

### Automation Notes
- **Source**: Usually derived from user context or environment
  - `from_repo`: Git remote URL of current repository
  - `to_repo`: User input or inferred from coordination target
- **Validation**: Verify both repositories exist (HTTP HEAD request to repo URL)
- **Permissions**: Check that from_repo has appropriate permissions to coordinate with to_repo

## Validation Rules

- Both fields are **required**
- Must match regex: `^github\.com/[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$`
- Repository should exist (optional validation via GitHub API)
- from_repo and to_repo may be identical (internal coordination)

## Related Content Blocks

- [core-metadata.md](core-metadata.md) - Request type and ID
- [context-background.md](context-background.md) - Relationship context between repos
- [collaboration-modes.md](collaboration-modes.md) - How repos will work together

## Examples from Real Requests

### Example 1: Cross-Repository Exploration (COORD-2025-002)
```json
{
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-compose"
}
```
**Context**: chora-base exploring integration with external tool (chora-compose)

### Example 2: Internal Coordination (COORD-2025-004)
```json
{
  "from_repo": "github.com/liminalcommons/chora-base",
  "to_repo": "github.com/liminalcommons/chora-base"
}
```
**Context**: Internal request to implement bidirectional translation layer

### Example 3: Peer Review (coord-005)
```json
{
  "from_repo": "github.com/liminalcommons/chora-workspace",
  "to_repo": "github.com/liminalcommons/chora-base"
}
```
**Context**: chora-workspace requesting peer review from chora-base maintainers

## Routing Implications

### Inbox Structure
Requests are routed based on to_repo:
- `inbox/incoming/` receives requests where `to_repo == <current-repo>`
- `inbox/outgoing/` contains requests where `from_repo == <current-repo>`

### Permissions
- from_repo should be verified as authorized to make requests
- to_repo determines who can process/close the request
- Cross-repo coordination may require explicit partnership agreements

### Notifications
- to_repo maintainers receive notifications
- from_repo is CC'd on status updates
- Stakeholders listed in context may receive FYI notifications

## Metadata

- **Priority**: HIGH (required in 100% of coordination requests)
- **Stability**: Stable (never changes after creation)
- **Reusability**: Universal (same pattern in tasks, proposals, ecosystem coordination)
- **Generation Source**: User input or environment detection
- **Version**: 1.0.0
- **Last Updated**: 2025-11-02
