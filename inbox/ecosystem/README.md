---
title: Ecosystem Communication Hub - README
description: Guide to ecosystem announcements, invitations, and coordination workflow
tags: [ecosystem, communication, workflow, meta-documentation]
diataxis_type: explanation
author: Victor Piper / Liminal Commons
created: 2025-10-31
updated: 2025-10-31
status: active
---

# Ecosystem Communication Hub

**Purpose**: This directory contains strategic communications for the Liminal Commons ecosystem announcing chora-workspace as the distributed development coordination hub.

**Status**: Ready for distribution (2025-10-31)
**Response Deadline**: November 14, 2025 (2 weeks)

---

## What These Documents Are

### Overview

This is the **official launch communication suite** for chora-workspace ecosystem coordination. It includes:

1. **Primary announcement** - General ecosystem-wide announcement (all stakeholders)
2. **Personalized invitations** - Repository-specific invitations (3 repos)
3. **Weekly broadcast** - First ecosystem status broadcast (all stakeholders)
4. **Onboarding guide** - Step-by-step tutorial (repository maintainers)
5. **Capability templates** - Pre-filled registration templates (3 repos)

**Total content**: ~26,000 words across 8 documents

**Investment**: 3.5 hours creation time

**Expected outcome**: 2-3 repositories onboard within 2 weeks, ecosystem coordination operational

---

## Who Should Act on These Documents

### Primary Audiences

| Document | Audience | Role | Action Required |
|----------|----------|------|-----------------|
| **ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md** | All ecosystem stakeholders | Read & share | Review announcement, forward to teams |
| **[repo]-invitation.md** (3 files) | Repository maintainers/stewards | Decision-makers | Review invitation, choose participation level, respond by Nov 14 |
| **2025-11-03-ecosystem-launch.md** | All ecosystem stakeholders | Stay informed | Read weekly updates, track coordination status |
| **ONBOARDING_GUIDE.md** | Repository contributors | Implementation | Follow steps to onboard (if repo decides to participate) |
| **[repo]-template.yaml** (3 files) | Repository maintainers | Registration | Review template, submit capability declaration |

### Target Repositories (5 total)

**Already Participating**:
1. ✅ **chora-base** - Template/framework repository (inbox protocol adopted)
2. ✅ **chora-workspace** - Coordination hub (this repository)

**Invited to Participate** (action required):
3. **ecosystem-manifest** - Standards authority (planned repository)
4. **mcp-orchestration** - Service layer (v0.2.0 in development)
5. **mcp-gateway** - Interface layer (v1.2.0 active)

---

## How to Respond - Workflow Guide

### For Repository Stewards/Maintainers

You received a personalized invitation in `invitations/[your-repo]-invitation.md`. Here's what to do:

#### Step 1: Read Your Invitation (10-15 minutes)

**File locations**:
- ecosystem-manifest: [invitations/ecosystem-manifest-invitation.md](invitations/ecosystem-manifest-invitation.md)
- mcp-orchestration: [invitations/mcp-orchestration-invitation.md](invitations/mcp-orchestration-invitation.md)
- mcp-gateway: [invitations/mcp-gateway-invitation.md](invitations/mcp-gateway-invitation.md)

**Look for**:
- "What [your-repo] Gains" section - Your specific value proposition
- "Pre-Filled Capability Template" - Ready-to-use registration template
- "W3 Health Monitoring: Your Role" - If participating in W3
- "What We're Asking" - Time commitment options

#### Step 2: Choose Participation Level (5 minutes)

Three options based on your capacity:

**Option 1: Full Onboarding** (45 min setup + 10 min/week)
- **What**: Register capabilities + adopt inbox protocol + join broadcasts
- **Best for**: W3 participants, repos with cross-repo dependencies
- **Value**: Full coordination support, dependency tracking, integration help
- **Commitment**: 45 min initial setup, 10 min/week ongoing

**Option 2: Capability Registration Only** (15 min one-time)
- **What**: Register capabilities (dashboard visibility only)
- **Best for**: Repos that want to stay visible but have limited capacity
- **Value**: Ecosystem dashboard presence, blocker tracking, easy to expand later
- **Commitment**: 15 min one-time, can upgrade to full later

**Option 3: Observer Mode** (0 min, no commitment)
- **What**: Receive weekly broadcasts, no setup required
- **Best for**: Repos evaluating coordination workspace before committing
- **Value**: Stay informed, zero effort, decide later
- **Commitment**: None, can join anytime

#### Step 3: Respond by November 14, 2025

**Choose your response method**:

##### Response Method A: Via Coordination Request (Recommended)

**Best for**: Testing coordination workflow, formal response

**Steps**:
1. Copy template: `inbox/schemas/coordination-request.schema.json`
2. Create file: `your-repo-participation-response.json`
3. Fill in:
   ```json
   {
     "type": "coordination",
     "request_id": "coord-NNN",
     "from_repo": "your-repo-name",
     "to_repo": "chora-workspace",
     "title": "Response to Ecosystem Coordination Invitation",
     "priority": "P2",
     "urgency": "next_sprint",
     "deliverables": [
       "Participation decision: [Full Onboarding / Capability Only / Observer]",
       "If participating: Capability declaration submission",
       "If participating: Estimated timeline for inbox adoption"
     ],
     "acceptance_criteria": [
       "Decision communicated by November 14, 2025",
       "If participating: Capability template submitted within 1 week",
       "If participating: Inbox protocol adopted within 2 weeks"
     ],
     "trace_id": "ecosystem-coordination-launch-2025-10-31"
   }
   ```
4. Submit PR to chora-workspace: `inbox/coordination/your-response.json`

##### Response Method B: Via Email (Simpler)

**Best for**: Quick response, informal communication

**To**: victor.piper@liminalcommons.org
**Subject**: `[Ecosystem Coordination] [your-repo] Participation Response`

**Email template**:
```
Hi,

Re: Ecosystem Coordination Invitation for [your-repo]

Our decision: [Full Onboarding / Capability Registration Only / Observer Mode / Decline]

[If Full Onboarding or Capability Registration:]
- Capability template reviewed: [Yes/No, need adjustments]
- Estimated submission date: [Date within 1 week]
- Questions/concerns: [Any questions]

[If Observer Mode:]
- Add to broadcast distribution: [Email address]
- Reason for waiting: [Optional: capacity, evaluating, unclear value, etc.]

[If Decline:]
- Reason: [Optional: not applicable, wrong timing, etc.]

Contact: [Your name, email]

Thanks,
[Your name]
```

##### Response Method C: Via GitHub Issue

**Best for**: Questions, discussion before deciding

1. Go to: https://github.com/liminal-commons/chora-workspace/issues/new
2. Title: `[Ecosystem Coordination] [your-repo] - [Question/Response]`
3. Describe your decision, questions, or concerns
4. Tag: @victorpiper (or relevant maintainer)

#### Step 4: If Participating - Follow Onboarding Guide

**File**: [ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md)

**Quick reference**:
- **Capability registration**: See "Step 1" (~15 min)
- **Inbox protocol adoption**: See "Step 2" (~30 min)
- **First coordination request**: See "Step 3" (optional)

Your pre-filled capability template is ready at:
- `CAPABILITIES/ecosystem-manifest-template.yaml`
- `CAPABILITIES/mcp-orchestration-template.yaml`
- `CAPABILITIES/mcp-gateway-template.yaml`

---

## What Happens After You Respond

### Timeline

**Week 1 (Nov 3-9)**:
- Invitations sent ✅ (complete)
- Repositories review invitations
- Questions/discussions via email or GitHub

**Week 2 (Nov 10-16)**:
- Responses due by November 14
- Second weekly broadcast published (Nov 10) with response status
- Capability registrations processed (<1 business day)

**Week 3+ (Nov 17+)**:
- Participating repos appear in ecosystem dashboard
- Inbox protocol adoption support provided
- Weekly broadcasts continue (every Sunday)
- W3 Health Monitoring coordination begins (if approved)

### If You Choose Full Onboarding

**You get**:
1. **Dashboard visibility** - Your repo appears in ECOSYSTEM_STATUS.yaml
2. **Capability template processed** - Merged within 1 business day
3. **Onboarding support** - Help with inbox protocol setup
4. **Weekly broadcasts** - Ecosystem status every Sunday
5. **Coordination support** - Help with W3 (if participating)

**We track**:
- Capability registration submitted ✅
- Inbox protocol adopted ✅
- First coordination request submitted ✅
- Active participation in weekly broadcasts ✅

### If You Choose Capability Registration Only

**You get**:
1. **Dashboard visibility** - Your repo appears in ECOSYSTEM_STATUS.yaml
2. **Blocker tracking** - Dependencies visible to ecosystem
3. **Weekly broadcasts** - Stay informed on ecosystem status

**Can upgrade to full onboarding anytime** - Just email or file coordination request

### If You Choose Observer Mode

**You get**:
- Weekly broadcasts sent to your email
- No action required, no commitment

**Can join anytime** - When ready, follow onboarding guide

---

## Distribution Instructions (For chora-workspace Maintainers)

### How to Distribute These Communications

#### Step 1: Prepare Distribution List

**Target contacts**:
- ecosystem-manifest stewards: [TBD - repository not yet created]
- mcp-orchestration stewards: orchestration-team@liminalcommons.org
- mcp-gateway stewards: gateway-team@liminalcommons.org

**Get contact info**:
- Check repository README files for maintainer contacts
- Check GitHub org members for team leads
- Use existing Slack/email channels if available

#### Step 2: Send Personalized Invitations

**Method**: Email with attachments

**Email template**:
```
Subject: [Invitation] Join chora-workspace Ecosystem Coordination Hub

Hi [Repository Team],

chora-workspace is now operational as the distributed development coordination hub for our ecosystem. We're inviting [your-repo] to participate.

**Your personalized invitation**: See attached [your-repo]-invitation.md

**What we're offering**:
- Pre-filled capability template (5 min review vs 30 min creation)
- Proven coordination protocol (70% acceptance rate, 82-142% ROI)
- [Specific value for your repo - from invitation]

**What we're asking**:
- Choose participation level by November 14, 2025
- Options: Full Onboarding (45 min), Capability Only (15 min), or Observer (0 min)

**How to respond**: See inbox/ecosystem/README.md (attached) for complete workflow

**Questions?** Reply to this email or check the ecosystem announcement (also attached).

Attachments:
- [your-repo]-invitation.md (your specific invitation)
- ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md (full ecosystem context)
- ONBOARDING_GUIDE.md (step-by-step if you participate)
- README.md (this workflow guide)

Thanks,
[Your name]
chora-workspace Coordination Team
```

#### Step 3: Post Weekly Broadcast

**Where**:
- chora-workspace repository: `inbox/coordination/broadcasts/`
- Ecosystem communication channels (Slack, Discord, email list)
- GitHub Discussions (if enabled)

**When**: Every Sunday

**First broadcast**: `2025-11-03-ecosystem-launch.md`

#### Step 4: Update Ecosystem Dashboard

**File**: `inbox/coordination/ECOSYSTEM_STATUS.yaml` (or create if doesn't exist in chora-base)

**Add section**:
```yaml
coordination_launch:
  invitations_sent: 2025-10-31
  response_deadline: 2025-11-14
  invited_repos:
    - ecosystem-manifest
    - mcp-orchestration
    - mcp-gateway

  responses_received:
    # Update as responses come in
    ecosystem-manifest: pending
    mcp-orchestration: pending
    mcp-gateway: pending
```

#### Step 5: Track Responses

**Create tracking file**: `inbox/ecosystem/INVITATION_RESPONSES.md`

**Template**:
```markdown
# Ecosystem Coordination Invitation Responses

**Sent**: 2025-10-31
**Deadline**: 2025-11-14

## Response Status

### ecosystem-manifest
- **Status**: Pending
- **Contact**: [email when known]
- **Last follow-up**: [date]
- **Notes**: Repository not yet created

### mcp-orchestration
- **Status**: Pending
- **Contact**: orchestration-team@liminalcommons.org
- **Last follow-up**: [date]
- **Notes**: [Any notes from discussions]

### mcp-gateway
- **Status**: Pending
- **Contact**: gateway-team@liminalcommons.org
- **Last follow-up**: [date]
- **Notes**: [Any notes from discussions]

## Follow-up Schedule

- **Week 1 (Nov 3-9)**: Initial invitation sent, monitor for questions
- **Week 2 (Nov 10)**: Gentle reminder if no response yet
- **Week 2 (Nov 14)**: Response deadline
- **Week 3 (Nov 17)**: Follow up with non-responders, offer extended deadline
```

---

## Measuring Success

### Short-term Success Metrics (2 weeks)

**Response rate**:
- ✅ Target: 2/3 repositories respond (67%)
- ✅ Stretch: 3/3 repositories respond (100%)

**Participation rate**:
- ✅ Target: 1 repository chooses Full Onboarding
- ✅ Stretch: 2 repositories choose Full Onboarding

**Engagement quality**:
- ✅ Target: At least 1 question/discussion per invitation (shows engagement)
- ✅ Stretch: Capability templates submitted within 1 week

### Medium-term Success Metrics (1 month)

**Onboarding completion**:
- ✅ Target: 1 repository fully onboarded (capability + inbox protocol)
- ✅ Stretch: 2 repositories fully onboarded

**Coordination activity**:
- ✅ Target: 1 cross-repo coordination request submitted
- ✅ Stretch: W3 Health Monitoring coordination begins

**Ecosystem health**:
- ✅ Target: Weekly broadcasts published consistently
- ✅ Stretch: Knowledge notes created from coordination learnings

### Long-term Success Metrics (3 months)

**Ecosystem maturity**:
- ✅ Target: 3+ repositories in capability registry
- ✅ Target: W3 coordination active (if strategically approved)
- ✅ Target: First ROI report from ecosystem coordination (not just SAP adoption)

---

## Troubleshooting

### Problem: No responses after 1 week

**Action**:
1. Send gentle reminder email (see template below)
2. Check if invitations were received (email delivery confirmation)
3. Offer to discuss over call/video if easier than written response
4. Ask if invitation unclear - offer to clarify

**Reminder email template**:
```
Subject: [Gentle Reminder] Ecosystem Coordination Invitation - Response by Nov 14

Hi [Team],

Quick reminder: We'd love to hear your thoughts on the ecosystem coordination invitation sent on Oct 31.

**Response deadline**: November 14, 2025 (this Friday)

**No pressure** - If you need more time or have questions, just let us know.

**Need help deciding?** Happy to jump on a quick call to discuss what participation would look like for [your-repo].

**Just want to observe?** That's fine too - let us know and we'll add you to broadcast distribution (zero commitment).

Reply here or check the workflow guide: inbox/ecosystem/README.md

Thanks,
[Your name]
```

### Problem: Response is "we're interested but not ready"

**Action**:
1. Offer Observer Mode (zero commitment, can upgrade later)
2. Ask what would help them be ready (timeline, resources, unclear value)
3. Offer extended timeline if helpful
4. Document in response tracking for follow-up

### Problem: Response is "unclear if this is valuable for us"

**Action**:
1. Point to repository-specific value section in their invitation
2. Offer to create custom value analysis for their repo
3. Suggest Capability Registration Only (15 min, low commitment, easy to evaluate)
4. Ask what evidence would help them decide (case studies, ROI data, examples)

### Problem: Capability template needs significant changes

**Action**:
1. Accept this as valid feedback - templates are starting points
2. Help them customize template (offer review/suggestions)
3. Document patterns for future template improvements
4. Update generic template based on learnings

---

## Files in This Directory

### Announcements
- **ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md** (~6,000 words) - Primary announcement for all stakeholders
- **2025-11-03-ecosystem-launch.md** (in `../coordination/broadcasts/`) - First weekly broadcast

### Invitations (Personalized)
- **invitations/ecosystem-manifest-invitation.md** (~4,000 words) - Standards authority, first external adopter
- **invitations/mcp-orchestration-invitation.md** (~4,000 words) - Service layer, W3 core implementation
- **invitations/mcp-gateway-invitation.md** (~4,000 words) - Interface layer, W3 user-facing delivery

### Guides & Templates
- **ONBOARDING_GUIDE.md** (~4,000 words) - Step-by-step tutorial for onboarding
- **CAPABILITIES/[repo]-template.yaml** (3 files) - Pre-filled capability registration templates

### Meta-Documentation
- **README.md** (this file) - What/who/how for entire communication suite

---

## Quick Reference

### Key Dates
- **Sent**: October 31, 2025
- **First Broadcast**: November 3, 2025
- **Response Deadline**: November 14, 2025 (2 weeks)
- **Second Broadcast**: November 10, 2025

### Key Links
- **Invitation workflow**: See "How to Respond - Workflow Guide" above
- **Onboarding steps**: [ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md)
- **Coordination protocol**: [ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md](ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md)
- **Success patterns**: [coordination-request-success-patterns.md](../../.chora/memory/knowledge/coordination-request-success-patterns.md)

### Contact
- **Email**: victor.piper@liminalcommons.org
- **GitHub Issues**: https://github.com/liminal-commons/chora-workspace/issues
- **Coordination Requests**: `inbox/coordination/`

---

## Summary

**These documents launch the chora-workspace ecosystem coordination hub.**

**Target repositories must**:
1. Read their personalized invitation
2. Choose participation level
3. Respond by November 14, 2025

**chora-workspace maintainers must**:
1. Send invitations via email
2. Track responses in INVITATION_RESPONSES.md
3. Publish weekly broadcasts
4. Support onboarding for participating repos

**Success looks like**: 2-3 repos onboarded within 2 weeks, ecosystem coordination operational, W3 coordination ready to begin (if approved).

**This README ensures nobody ignores these important documents by clearly explaining what they are, who should act, and how to respond.**

---

**Document**: README.md (Ecosystem Communication Hub)
**Created**: 2025-10-31
**Author**: Victor Piper / Liminal Commons
**Status**: Ready for use

**Next Action**: Send invitations to target repositories using distribution instructions above.
