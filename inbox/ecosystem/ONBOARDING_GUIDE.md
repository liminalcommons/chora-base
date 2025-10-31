---
title: Ecosystem Onboarding Quick Start Guide
description: Step-by-step guide for repositories joining the chora-workspace coordination hub
tags: [onboarding, quickstart, inbox-protocol, coordination]
diataxis_type: tutorial
author: Victor Piper / Liminal Commons
created: 2025-10-31
updated: 2025-10-31
status: active
---

# Ecosystem Onboarding Quick Start Guide

**Audience**: Repository maintainers, stewards, and contributors joining the chora-workspace coordination hub

**Time to complete**: 45 minutes (full onboarding) or 15 minutes (capability registration only)

**Prerequisites**: Git repository for your project, GitHub access, basic YAML/JSON knowledge

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start (3 Steps)](#quick-start-3-steps)
3. [Step 1: Register Capabilities](#step-1-register-capabilities-15-minutes)
4. [Step 2: Adopt Inbox Protocol](#step-2-adopt-inbox-protocol-30-minutes)
5. [Step 3: Submit First Coordination Request](#step-3-submit-first-coordination-request-optional)
6. [Verification & Testing](#verification--testing)
7. [Next Steps](#next-steps)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Onboarding?

Onboarding to the chora-workspace coordination hub means:

1. **Registering your capabilities** - Declaring what your repo provides/consumes
2. **Adopting inbox protocol** - Creating `inbox/` directory structure in your repo
3. **Starting coordination** - Using coordination requests for cross-repo work

### Benefits

- ✅ **Ecosystem visibility**: Your repo visible in real-time dashboard
- ✅ **Dependency tracking**: See blockers, signal readiness
- ✅ **Event traceability**: Debug across repos with trace IDs
- ✅ **Proven patterns**: Access 8 patterns with 82-142% ROI
- ✅ **Coordination support**: Structured protocol with 70% acceptance rate

### Participation Levels

| Level | Time | Value | Commitment |
|-------|------|-------|------------|
| **Full Onboarding** | 45 min | Complete coordination support | Recommended for W3 participants |
| **Capability Registry** | 15 min | Dashboard visibility, blocker tracking | Lightweight, easy to expand later |
| **Observer Mode** | 0 min | Weekly broadcasts, stay informed | No setup, decide later |

Choose based on your immediate needs and capacity.

---

## Quick Start (3 Steps)

### For the Impatient

```bash
# Step 1: Get your pre-filled capability template (5 min)
# Download from your invitation email or chora-workspace repo:
# inbox/coordination/CAPABILITIES/[your-repo]-template.yaml

# Step 2: Review and submit capability declaration (10 min)
# Edit the template, then:
git clone https://github.com/liminal-commons/chora-workspace.git
cd chora-workspace
cp /path/to/your-edited-template.yaml inbox/coordination/CAPABILITIES/[your-repo].yaml
git checkout -b capability/[your-repo]
git add inbox/coordination/CAPABILITIES/[your-repo].yaml
git commit -m "Add [your-repo] capability declaration"
git push origin capability/[your-repo]
# Create PR on GitHub

# Step 3 (Optional): Adopt inbox protocol in your repo (30 min)
cd /path/to/your-repo
mkdir -p inbox/{ecosystem/proposals,coordination,incoming/tasks,schemas}
cp /path/to/chora-workspace/inbox/schemas/*.json inbox/schemas/
# Document in README (see examples below)
git add inbox/
git commit -m "Adopt inbox coordination protocol"
git push
```

**That's it!** You're now registered in the ecosystem. Continue reading for detailed instructions.

---

## Step 1: Register Capabilities (15 minutes)

### 1.1 Get Your Pre-Filled Template

**Check your invitation email** or download from chora-workspace:

```bash
# For ecosystem-manifest
https://github.com/liminal-commons/chora-workspace/blob/main/inbox/coordination/CAPABILITIES/ecosystem-manifest-template.yaml

# For mcp-orchestration
https://github.com/liminal-commons/chora-workspace/blob/main/inbox/coordination/CAPABILITIES/mcp-orchestration-template.yaml

# For mcp-gateway
https://github.com/liminal-commons/chora-workspace/blob/main/inbox/coordination/CAPABILITIES/mcp-gateway-template.yaml
```

**Don't have a template?** Use the generic template below.

### 1.2 Review and Edit Template

**Key sections to update**:

```yaml
repository:
  name: your-repo-name  # REQUIRED
  version: v1.0.0       # REQUIRED: Your current version

provides:
  - capability: what_you_offer  # REQUIRED
    version: v1.0.0
    status: active  # Options: planned, in_development, active, maintenance

consumes:
  - capability: what_you_need  # Optional, list dependencies
    from_repo: source-repo
    version: ">=1.0.0"

current_status:
  state: active  # REQUIRED: planned, in_development, active, maintenance
  next_milestone: "Your next goal"

blockers:
  - type: dependency  # Optional, list current blockers
    description: "What's blocking you"
    priority: P1  # P0-P3

contact:
  maintainers:
    - your.email@example.com  # REQUIRED
```

**Time**: 5 minutes to review, adjust values

### 1.3 Submit Capability Declaration

**Option A: Via PR (Recommended)**

```bash
# Clone chora-workspace
git clone https://github.com/liminal-commons/chora-workspace.git
cd chora-workspace

# Create branch
git checkout -b capability/your-repo-name

# Copy your edited template
cp /path/to/your-edited.yaml inbox/coordination/CAPABILITIES/your-repo-name.yaml

# Commit and push
git add inbox/coordination/CAPABILITIES/your-repo-name.yaml
git commit -m "Add capability declaration for your-repo-name

- Provides: [list key capabilities]
- Consumes: [list key dependencies]
- Status: [current state]

Part of ecosystem coordination onboarding."

git push origin capability/your-repo-name
```

Then create PR on GitHub: `https://github.com/liminal-commons/chora-workspace/compare`

**Option B: Via Email**

Send your edited YAML file to: `victor.piper@liminalcommons.org`

Subject: `[Capability Registration] your-repo-name`

**Time**: 10 minutes (PR) or 5 minutes (email)

### 1.4 Verification

**You'll know it worked when**:
- ✅ PR merged or email confirmation received
- ✅ Your repo appears in next weekly broadcast
- ✅ Ecosystem dashboard shows your repo (ECOSYSTEM_STATUS.yaml updated)

**Typical response time**: <1 business day

---

## Step 2: Adopt Inbox Protocol (30 minutes)

### 2.1 Create Directory Structure

**In your repository root**:

```bash
cd /path/to/your-repo

# Create inbox directories
mkdir -p inbox/ecosystem/proposals
mkdir -p inbox/coordination
mkdir -p inbox/incoming/tasks
mkdir -p inbox/schemas

# Verify structure
tree inbox/
# Expected output:
# inbox/
# ├── ecosystem/
# │   └── proposals/
# ├── coordination/
# ├── incoming/
# │   └── tasks/
# └── schemas/
```

**Time**: 2 minutes

### 2.2 Copy Schemas

**Download schema files from chora-workspace**:

```bash
# If you have chora-workspace cloned
cp /path/to/chora-workspace/inbox/schemas/*.json inbox/schemas/

# Or download directly
curl -o inbox/schemas/coordination-request.schema.json \
  https://raw.githubusercontent.com/liminal-commons/chora-workspace/main/inbox/schemas/coordination-request.schema.json

curl -o inbox/schemas/implementation-task.schema.json \
  https://raw.githubusercontent.com/liminal-commons/chora-workspace/main/inbox/schemas/implementation-task.schema.json
```

**Verify**:
```bash
ls inbox/schemas/
# Expected: coordination-request.schema.json, implementation-task.schema.json
```

**Time**: 3 minutes

### 2.3 Document in README

**Add section to your repository's README.md**:

```markdown
## Inbox Coordination Protocol

This repository participates in the [chora-workspace ecosystem coordination hub](https://github.com/liminal-commons/chora-workspace).

### Directory Structure

- `inbox/ecosystem/proposals/` - Strategic proposals (quarterly review)
- `inbox/coordination/` - Coordination requests (bi-weekly review)
- `inbox/incoming/tasks/` - Implementation tasks (continuous)
- `inbox/schemas/` - JSON schemas for validation

### How to Coordinate

**Submit a coordination request**:
1. Review schema: `inbox/schemas/coordination-request.schema.json`
2. Create request: `inbox/coordination/[request-id].json`
3. Follow success pattern: [COORD-003 case study](https://github.com/liminal-commons/chora-workspace/blob/main/.chora/memory/knowledge/coordination-request-success-patterns.md)

**Success rate**: 70% for well-formed requests (quantitative data, clear criteria, strategic alignment)

### Our Capabilities

See our capability declaration: [CAPABILITIES/your-repo-name.yaml](https://github.com/liminal-commons/chora-workspace/blob/main/inbox/coordination/CAPABILITIES/your-repo-name.yaml)

**Provides**: [List key capabilities]
**Consumes**: [List key dependencies]

### Contact

**Coordination requests**: File in `inbox/coordination/`
**Questions**: your-team@example.com
**Response SLA**: 1-2 business days
```

**Time**: 10 minutes

### 2.4 Create Initial README for Inbox

**Optional but recommended**: Document inbox protocol in your repo

**File**: `inbox/README.md`

```markdown
# Inbox Coordination Protocol

This directory implements the [chora-workspace inbox protocol](https://github.com/liminal-commons/chora-workspace) for ecosystem coordination.

## Directory Guide

### `ecosystem/proposals/`
**Purpose**: Strategic proposals requiring quarterly review
**Format**: Markdown documents
**Timeline**: Weeks to months

**When to use**: Multi-quarter initiatives, ecosystem architecture changes, major features

### `coordination/`
**Purpose**: Cross-repo coordination requests requiring bi-weekly review
**Format**: JSON following `schemas/coordination-request.schema.json`
**Timeline**: Days to weeks

**When to use**: Cross-repo features, dependency coordination, integration work

### `incoming/tasks/`
**Purpose**: Approved implementation tasks for continuous execution
**Format**: JSON following `schemas/implementation-task.schema.json`
**Timeline**: Hours to days

**When to use**: Approved tasks, bug fixes, documentation updates

## How to Submit a Request

1. **Choose request type** based on timeline and scope
2. **Follow schema** (`schemas/coordination-request.schema.json`)
3. **Apply success pattern**:
   - ✅ Quantitative data (not qualitative opinions)
   - ✅ Specific friction points (not general complaints)
   - ✅ Offer contributions (prototypes, drafts)
   - ✅ Strategic alignment (connect to priorities)
   - ✅ Clear acceptance criteria (SMART)

**Success rate**: 70% for well-formed requests

## Examples

See complete W3 Health Monitoring example:
- Strategic: [prop-001](https://github.com/liminal-commons/chora-base/inbox/examples/health-monitoring-w3/strategic/)
- Coordination: [coord-001 through coord-004](https://github.com/liminal-commons/chora-base/inbox/examples/health-monitoring-w3/coordination/)
- Timeline: [47 events, 16 weeks](https://github.com/liminal-commons/chora-base/inbox/examples/health-monitoring-w3/events/)

## Contact

**Questions**: See main README for contact information
**Coordination support**: victor.piper@liminalcommons.org
```

**Time**: 10 minutes

### 2.5 Commit and Push

```bash
git add inbox/
git commit -m "Adopt inbox coordination protocol

- Create inbox directory structure
- Add JSON schemas for validation
- Document protocol in README

Part of chora-workspace ecosystem onboarding.

Trace ID: ecosystem-coordination-launch-2025-10-31"

git push origin main
```

**Time**: 5 minutes

---

## Step 3: Submit First Coordination Request (Optional)

### When to Submit

**Wait if**:
- You don't have an immediate cross-repo need
- You want to observe first
- You're still evaluating inbox protocol

**Submit when**:
- You have a dependency on another repo
- You're ready to participate in W3 (or similar initiative)
- You want to test the coordination workflow

### 3.1 Identify Coordination Need

**Good coordination request topics**:
- ✅ Dependency on another repo's feature/API
- ✅ Integration work requiring both repos
- ✅ Breaking change affecting consumers
- ✅ Cross-repo testing or deployment coordination

**Not good for coordination request**:
- ❌ Internal feature (no cross-repo dependency)
- ❌ Bug fix in your own repo
- ❌ General questions (use email instead)

### 3.2 Draft Request Using Schema

**Template**:

```json
{
  "type": "coordination",
  "request_id": "coord-NNN",
  "from_repo": "your-repo",
  "to_repo": "target-repo",
  "title": "Concise description (50-80 chars)",
  "priority": "P1",
  "urgency": "next_sprint",
  "deliverables": [
    "Specific deliverable 1 with measurable outcome",
    "Specific deliverable 2 with measurable outcome"
  ],
  "acceptance_criteria": [
    "SMART criterion 1 (Specific, Measurable, Achievable, Relevant, Time-bound)",
    "SMART criterion 2 with quantitative metric"
  ],
  "strategic_alignment": "How this supports upstream priorities",
  "proposed_timeline": "2 weeks (sprints 3-4)",
  "trace_id": "ecosystem-waypoint-activity",
  "context": {
    "problem": "Quantitative data showing friction (e.g., 3-4h wasted per occurrence)",
    "proposed_solution": "Your proposed approach",
    "alternatives_considered": ["Why alternative 1 rejected", "Why alternative 2 rejected"]
  },
  "contribution_offered": "Working prototype or draft you're providing to accelerate"
}
```

**Validate against schema**:
```bash
# Install jq if not already available
brew install jq  # macOS
apt-get install jq  # Linux

# Validate
jq empty < your-request.json
# No output = valid JSON
```

### 3.3 Apply Success Pattern

**From COORD-003 case study** (70% acceptance):

✅ **DO**: Quantitative data
```json
"context": {
  "problem": "Onboarding takes 3-4 hours (measured across 5 new developers). 71% of time spent on context loading (verification: 18 SAPs exist, all work)."
}
```

❌ **DON'T**: Qualitative opinions
```json
"context": {
  "problem": "Onboarding is slow and confusing."
}
```

✅ **DO**: Offer contributions
```json
"contribution_offered": "Working validate-infrastructure.sh script (300 lines, executable). Could accelerate pre-flight validator by ~50%."
```

❌ **DON'T**: Just ask
```json
"contribution_offered": "None, requesting implementation from target repo."
```

✅ **DO**: Strategic alignment
```json
"strategic_alignment": "Supports v4.x objective: Improve ecosystem growth and adoption. Addresses friction in new developer experience (OKR: Reduce onboarding <2h)."
```

❌ **DON'T**: Assume alignment is obvious
```json
"strategic_alignment": "This seems important."
```

### 3.4 Submit Request

**File location**: `chora-workspace/inbox/coordination/your-request.json`

**Via PR**:
```bash
cd /path/to/chora-workspace
git checkout -b coordination/your-request-id

cp /path/to/your-request.json inbox/coordination/coord-NNN-your-repo.json

git add inbox/coordination/coord-NNN-your-repo.json
git commit -m "Coordination request: [Title]

From: your-repo
To: target-repo
Priority: P1

Deliverables:
- Deliverable 1
- Deliverable 2

Trace ID: [trace-id]"

git push origin coordination/your-request-id
```

**Expected response time**: 0.5-2 hours for triage (based on COORD-003 pattern)

---

## Verification & Testing

### After Step 1 (Capability Registration)

**Verify**:
```bash
# Check ecosystem dashboard
curl https://raw.githubusercontent.com/liminal-commons/chora-workspace/main/inbox/coordination/ECOSYSTEM_STATUS.yaml | grep your-repo-name

# Expected: Your repo appears with status, blockers
```

**You should see**:
- Your repo in weekly broadcast (next Sunday)
- Capability file merged in chora-workspace
- Contact from coordination team confirming

### After Step 2 (Inbox Adoption)

**Verify**:
```bash
# In your repo
ls -la inbox/
# Should show: ecosystem/, coordination/, incoming/, schemas/

# Check schemas
jq empty < inbox/schemas/coordination-request.schema.json
# No errors = valid
```

**Test**: Create a dummy coordination request and validate against schema

### After Step 3 (First Request)

**Verify**:
```bash
# Check your PR was created
git ls-remote origin | grep coordination/your-request-id

# Check JSON is valid
jq empty < inbox/coordination/coord-NNN-your-repo.json
```

**Expected**:
- PR reviewed within 1 business day
- Triage response within 0.5-2 hours (for well-formed requests)
- Acceptance/rejection with clear reasoning

---

## Next Steps

### After Onboarding

1. **Join weekly broadcasts** (Sundays)
   - Watch chora-workspace repo for new broadcasts
   - Stay informed on ecosystem status, coordination progress

2. **Log events for major milestones**
   - Use trace IDs to correlate across repos
   - Format: JSONL (one JSON object per line)
   - Example: `{"event_type":"feature_complete","trace_id":"ecosystem-w3-health-monitoring","timestamp":"2025-11-01T12:00:00Z"}`

3. **Create knowledge notes from learnings**
   - When you discover a pattern
   - When coordination works well (or doesn't)
   - Format: Markdown with YAML frontmatter, [[wikilinks]]

4. **Contribute to coordination protocol**
   - Suggest schema improvements
   - Share successful coordination patterns
   - Help other repos onboard

### For W3 Participants

If your repo is part of W3 Health Monitoring:

1. **Review your W3 coordination request**
   - Example: `chora-base/inbox/examples/health-monitoring-w3/coordination/coord-00X-your-repo.json`
   - Understand deliverables, timeline, dependencies

2. **Set up event logging**
   - Use trace_id: `ecosystem-w3-health-monitoring`
   - Log at major milestones (implementation start, tests pass, deployment)

3. **Coordinate dependencies**
   - Signal when you're blocked (update capability declaration)
   - Signal when you're ready (emit event, file coordination request)

4. **Track via dashboard**
   - Check ECOSYSTEM_STATUS.yaml weekly
   - Know when dependencies resolve, when consumers are ready

---

## Troubleshooting

### Problem: "I don't have a pre-filled template"

**Solution**: Use generic template

```yaml
repository:
  name: your-repo-name
  role: your_role  # e.g., service, library, tool, framework
  description: Brief description
  version: v1.0.0

provides:
  - capability: what_you_provide
    description: Detailed description
    version: v1.0.0
    consumers: [list_of_consumers]
    status: active

consumes:
  - capability: what_you_need
    from_repo: source-repo
    version: ">=1.0.0"
    required: true

responsibilities:
  - What your repo is responsible for

current_status:
  state: active
  next_milestone: Your next goal

contact:
  maintainers:
    - your.email@example.com
```

### Problem: "My capability declaration was rejected"

**Common reasons**:
- Missing required fields (repository.name, version, contact)
- Invalid YAML syntax
- Unclear capability descriptions

**Solution**: Check schema, review examples, ask for help via email

### Problem: "I can't validate JSON against schema"

**Solution**: Use online validator

1. Go to https://www.jsonschemavalidator.net/
2. Paste schema from `inbox/schemas/coordination-request.schema.json` (left panel)
3. Paste your request JSON (right panel)
4. Check for validation errors

### Problem: "My coordination request has no response"

**Expected timeline**:
- Triage: 0.5-2 hours (business days)
- Review: 1-2 business days
- Decision: Communicated via PR comments or coordination request response

**If >3 business days**:
- Check PR for comments
- Email victor.piper@liminalcommons.org with request ID
- Verify request follows success pattern (quantitative data, clear criteria, strategic alignment)

### Problem: "I want to change my capability declaration"

**Solution**: Submit update PR

```bash
# Edit your capability file
vim inbox/coordination/CAPABILITIES/your-repo.yaml

# Submit update
git checkout -b capability/your-repo-update
git add inbox/coordination/CAPABILITIES/your-repo.yaml
git commit -m "Update capability declaration: [what changed]"
git push origin capability/your-repo-update
```

**Frequency**: Update when major changes (new capabilities, version changes, blocker resolution)

---

## Additional Resources

### Documentation

- **Inbox Protocol Spec**: [chora-base/inbox/INBOX_PROTOCOL.md](https://github.com/liminal-commons/chora-base/blob/main/inbox/INBOX_PROTOCOL.md)
- **Agent Patterns**: [chora-base/inbox/CLAUDE.md](https://github.com/liminal-commons/chora-base/blob/main/inbox/CLAUDE.md)
- **System Architecture**: [docs/SYSTEM-ARCHITECTURE.md](../../docs/SYSTEM-ARCHITECTURE.md)
- **Ecosystem Announcement**: [ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md](ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md)

### Examples

- **W3 Complete Example**: [chora-base/inbox/examples/health-monitoring-w3/](https://github.com/liminal-commons/chora-base/tree/main/inbox/examples/health-monitoring-w3)
- **COORD-003 Case Study**: [coordination-request-success-patterns.md](../../.chora/memory/knowledge/coordination-request-success-patterns.md)
- **Capability Declarations**: [inbox/coordination/CAPABILITIES/](../coordination/CAPABILITIES/)

### Templates

- **Coordination Request**: `inbox/schemas/coordination-request.schema.json`
- **Implementation Task**: `inbox/schemas/implementation-task.schema.json`
- **Capability Declaration**: `inbox/coordination/CAPABILITIES/*-template.yaml`

### Support

- **Email**: victor.piper@liminalcommons.org
- **GitHub Issues**: [chora-workspace/issues](https://github.com/liminal-commons/chora-workspace/issues)
- **Weekly Broadcasts**: Every Sunday in `inbox/coordination/broadcasts/`

---

## Summary Checklist

**Step 1: Register Capabilities** (15 min)
- [ ] Get pre-filled template (or use generic)
- [ ] Review and edit template
- [ ] Submit via PR or email
- [ ] Verify in next weekly broadcast

**Step 2: Adopt Inbox Protocol** (30 min)
- [ ] Create `inbox/` directory structure
- [ ] Copy JSON schemas
- [ ] Document in main README
- [ ] Create inbox README (optional)
- [ ] Commit and push

**Step 3: Submit First Request** (optional)
- [ ] Identify coordination need
- [ ] Draft request using schema
- [ ] Apply success pattern (quantitative, contributions, alignment, clear criteria)
- [ ] Submit via PR
- [ ] Track response

**Ongoing**
- [ ] Join weekly broadcasts
- [ ] Log events with trace IDs
- [ ] Create knowledge notes from learnings
- [ ] Update capability declaration as needed

---

**Congratulations!** You're now part of the chora-workspace coordination ecosystem.

**Questions?** Email victor.piper@liminalcommons.org or file a coordination request.

**Next**: Watch for weekly broadcasts (Sundays) and join ecosystem initiatives like W3 Health Monitoring.

---

**Document**: ONBOARDING_GUIDE.md
**Date**: 2025-10-31
**Author**: Victor Piper / Liminal Commons
**Trace ID**: `ecosystem-coordination-launch-2025-10-31`
**Version**: 1.0

**Feedback welcome**: How can we make onboarding easier? Let us know!
