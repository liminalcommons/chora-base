# How-To: Maintain Vision Documents

**Audience:** Project maintainers, AI agents
**Type:** Task-oriented guide (scannable, actionable)
**Related:** [Vision-Driven Development](../explanation/vision-driven-development.md), [Template Configuration](../reference/template-configuration.md)

---

## Quick Reference

| Task | Command / Action | Frequency |
|------|------------------|-----------|
| **Create vision doc** | Copy `CAPABILITY_EVOLUTION.example.md` → customize waves | Once (project start) |
| **Quarterly review** | Update decision criteria, move delivered waves | Quarterly (Q1/Q2/Q3/Q4) |
| **Archive wave** | Move to `dev-docs/vision/archive/WAVE-NAME.md` | When delivered/deferred |
| **Update ROADMAP.md** | Sync vision highlights with current waves | After each release |
| **Update AGENTS.md** | Sync Strategic Context with current priority | When priorities shift |
| **Check links** | Verify ROADMAP ↔ vision ↔ AGENTS links work | Before each release |

---

## Creating a Vision Document

### Step 1: Copy the Template

```bash
cd your-project/

# Copy example vision document
cp dev-docs/vision/CAPABILITY_EVOLUTION.example.md \
   dev-docs/vision/CAPABILITY_EVOLUTION.md

# Or create project-specific vision doc
cp dev-docs/vision/CAPABILITY_EVOLUTION.example.md \
   dev-docs/vision/MY_CAPABILITY_VISION.md
```

**Note:** Most projects have one vision document (`CAPABILITY_EVOLUTION.md`). Only create multiple if tracking distinct capability themes (e.g., `PLATFORM_EVOLUTION.md` + `API_EVOLUTION.md`).

### Step 2: Customize Waves

**Open** `dev-docs/vision/CAPABILITY_EVOLUTION.md` **and replace example content:**

#### Wave 1 (Foundation) - Current Work

Replace:
```markdown
**Wave 1: Foundation (Current)**
- Core functionality
- Basic tools
- Local operation
```

With your actual Wave 1 capabilities:
```markdown
**Wave 1: Foundation (Current)**
- MCP server with 3 core tools: list, search, get
- Error handling and validation
- Basic configuration (.env support)
- Testing infrastructure (≥85% coverage)
```

#### Wave 2+ (Future Waves) - Exploratory

For each future wave:

1. **Replace capability theme:**
   ```markdown
   **Wave 2: Integration** (Post-v1.0, Exploratory)
   ```
   → Your actual next capability area

2. **Update motivation:**
   - Why this wave matters (user need, market signal)
   - Link to GitHub issues or user feedback

3. **Adjust decision criteria:**
   ```markdown
   | Criterion | Target | Current | Status |
   |-----------|--------|---------|--------|
   | Wave 1 Stable | v1.0 shipped, <5 bugs | TBD | ⏳ Pending |
   | User Demand | 50+ users requesting | TBD | ⏳ Track |
   ```
   → Realistic targets for your project size

4. **Update technical sketch:**
   - Keep high-level (not detailed specs)
   - Show extension points, not full implementations

### Step 3: Remove Unused Waves

If you only need 2-3 waves:

```bash
# Edit dev-docs/vision/CAPABILITY_EVOLUTION.md
# Delete Wave 3, Wave 4 sections if not needed
```

**Minimal vision (2 waves):**
- Wave 1: Foundation (current)
- Wave 2: Integration (next)

**Comprehensive vision (4-6 waves):**
- Wave 1-4: As needed
- Don't exceed 6 waves (too complex)

### Step 4: Test Rendering

```bash
# Generate a test project to verify vision renders correctly
cd /tmp/
copier copy path/to/your-project/template/ test-vision-check \
  --data include_vision_docs=true \
  --defaults

# Check rendered vision
cat test-vision-check/dev-docs/vision/CAPABILITY_EVOLUTION.md | head -100

# Verify no unrendered Jinja variables
grep "{{" test-vision-check/dev-docs/vision/*.md
# Should return empty
```

---

## Structuring Capability Waves

### Wave Naming Conventions

**Good names (theme-based):**
- Wave 1: Foundation
- Wave 2: Integration
- Wave 3: Intelligence
- Wave 4: Ecosystem

**Avoid (feature-list names):**
- Wave 1: Add 3 tools
- Wave 2: Plugin system + caching + webhooks
  (Too specific - use theme instead)

### Writing Capability Themes

Each wave should answer:

1. **What capability does this enable?** (one sentence)
   - Wave 2 enables: "Integration with external systems"

2. **Why does this matter?** (motivation)
   - User need: "Users request GitHub/Notion integrations"

3. **What's the high-level approach?** (technical sketch)
   - "Adapter pattern for external APIs, OAuth support"

**Example: MCP Server Waves**

```markdown
## Wave 1: Foundation (Current)
**Capability:** Core MCP tools for basic operations

## Wave 2: Integration (Post-v1.0)
**Capability:** Connect to external data sources (APIs, databases)

## Wave 3: Intelligence (Post-v2.0)
**Capability:** Smart tool routing and caching based on usage patterns

## Wave 4: Ecosystem (Post-v3.0)
**Capability:** Community-built tools and marketplace
```

**Example: Library Waves**

```markdown
## Wave 1: Core API (Current)
**Capability:** Essential processing functions with type safety

## Wave 2: Extensibility (Post-v1.0)
**Capability:** Plugin system for custom processors

## Wave 3: Multi-Format (Post-v2.0)
**Capability:** Support for JSON, YAML, XML, CSV input/output

## Wave 4: Framework Integration (Post-v3.0)
**Capability:** Adapters for Django, Flask, FastAPI
```

### Setting Realistic Decision Criteria

**Template:**

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| **Wave N-1 Delivered** | vX.0 shipped, stable | Release notes |
| **User Demand** | [N] users requesting | GitHub issues, feedback |
| **Technical Validation** | Spike completed, feasible | Prototype results |
| **Team Capacity** | [N] months available | Budget/planning |

**Adjust targets based on project size:**

| Project Size | User Demand Target | Team Capacity |
|--------------|-------------------|---------------|
| **Small** (1-2 devs) | 10-20 users | 1-2 months |
| **Medium** (3-5 devs) | 50-100 users | 3-6 months |
| **Large** (6+ devs) | 100+ users | 6-12 months |

**Example criteria for small project:**

```markdown
| Criterion | Target | Current | Status |
|-----------|--------|---------|--------|
| Wave 1 Stable | v1.0 shipped, <10 bugs | v0.8 | ⏳ In progress |
| User Demand | 20+ users requesting | 5 | ❌ Below threshold |
| Technical Spike | Completed successfully | Not started | ❌ Need validation |
| Team Capacity | 2 months available | Q3 busy | ❌ Deferred to Q4 |
```

**Decision:** 1/4 criteria met → **DEFER** (revisit after v1.0 stabilizes)

---

## Quarterly Review Process

### Schedule Reviews

**Recommended cadence:**

- **Q1 (January):** After holiday releases stabilize
- **Q2 (April):** Mid-year planning
- **Q3 (July):** Pre-autumn release cycle
- **Q4 (October):** Year-end review

**Trigger reviews when:**
- Major milestone completes (v1.0, v2.0)
- User demand shifts significantly
- Technical landscape changes (new APIs available)

### Review Checklist

**Step 1: Gather Signals (30 minutes)**

```bash
# Check user demand
# Count GitHub issues tagged with wave themes
gh issue list --label "integration" --state open
gh issue list --label "plugins" --state open

# Review discussions
gh search prs --repo owner/repo --label feature-request

# Check adoption metrics (if available)
# - Download counts
# - Active users
# - Tool usage frequency
```

**Step 2: Update Decision Criteria (15 minutes)**

For each wave:

```markdown
| Criterion | Target | Current (2025-10-19) | Status |
|-----------|--------|---------------------|--------|
| Wave 1 Stable | v1.0 shipped | ✅ v1.0.2 stable | ✅ Met |
| User Demand | 50+ users | 📊 65 users | ✅ Met |
| Technical Validation | Spike done | ✅ Prototype works | ✅ Met |
| Team Capacity | 3 months | ❌ 1 month Q4 | ❌ Not met |
```

**Decision:** 3/4 criteria met → **VALIDATE** (run full spike in Q4, commit in Q1)

**Step 3: Archive Delivered Waves (10 minutes)**

If Wave N delivered:

```bash
# Move to archive
mkdir -p dev-docs/vision/archive/
mv dev-docs/vision/WAVE-N-NAME.md dev-docs/vision/archive/

# Or add archive section to single vision doc
# See "Archiving Waves" section below
```

**Step 4: Update Vision Document (30 minutes)**

```markdown
## Review History

### 2025-10-19 (Q4 Review)

**Decisions:**
- Wave 1 (Foundation): ✅ DELIVERED in v1.0.0 (archived)
- Wave 2 (Integration): ✅ COMMITTED to v1.5.0 roadmap (65 users requesting)
- Wave 3 (Intelligence): ⏳ DEFERRED until Wave 2 ships (dependency)
- Wave 4 (Ecosystem): 📝 UPDATED decision criteria (API partners now available)

**User Signals:**
- 65 users active (up from 20 in Q3)
- 12 GitHub issues requesting GitHub integration (Wave 2)
- 3 issues requesting smart caching (Wave 3)

**Technical Changes:**
- GitHub API v4 now stable (enables Wave 2)
- OpenAI embeddings API available (enables Wave 3 tool routing)

**New Waves:**
- None added this quarter

**Archived Waves:**
- Wave 1 (Foundation): Delivered in v1.0.0 on 2025-09-15

**Next Review:** 2026-01-15 (Q1 Review, after v1.5.0 ships)
```

**Step 5: Commit Waves to ROADMAP (if applicable)**

If wave meets ALL criteria → move to ROADMAP.md:

```markdown
# In ROADMAP.md

## Near-Term Roadmap

### v1.5.0 (Q1 2026)

**Goal:** Enable integration with external systems

**Features:**
- GitHub integration (issues, PRs, repos)
- Notion integration (pages, databases)
- API adapter framework
- OAuth authentication

**Decision:** Committed from Wave 2 vision (see dev-docs/vision/)

**Success Criteria:**
- 3+ external systems integrated
- OAuth flow tested with 5+ users
- <5% integration errors
```

Then update vision doc:

```markdown
## Wave 2: Integration (COMMITTED to v1.5.0)

**Status:** ✅ Committed to roadmap (2025-10-19)
**Target:** v1.5.0 (Q1 2026)

See [ROADMAP.md](../../ROADMAP.md) for timeline and committed features.

**Archive Note:** This wave will be archived after v1.5.0 delivers.
```

---

## Archiving Waves

### When to Archive

Archive waves when:

1. **Delivered:** Wave shipped in a release
2. **Deferred Permanently:** Explicit decision not to pursue
3. **Superseded:** New approach replaces old wave

### Archive Options

**Option 1: Separate Archive Files** (recommended for multiple visions)

```bash
mkdir -p dev-docs/vision/archive/

# Archive delivered wave
cat > dev-docs/vision/archive/WAVE-01-FOUNDATION.md <<'EOF'
# Wave 1: Foundation

**Status:** Delivered in v1.0.0 (2025-09-15)
**Archive Date:** 2025-10-19
**Reason:** Delivered

## Original Vision

[Copy original wave content from CAPABILITY_EVOLUTION.md]

## Outcome

**Delivered Features:**
- MCP server with 3 core tools (list, search, get)
- Error handling and validation
- Testing infrastructure (achieved 87% coverage)

**Variance from Vision:**
- Originally planned 5 tools, delivered 3 (search split into two tools)
- Added OAuth support (not in original vision, user request)

**Success Metrics:**
- Target: 10+ users → Actual: 65 users (650% of target)
- Target: <5% error rate → Actual: 2.3% error rate
- Target: 85% coverage → Actual: 87% coverage

**Learnings:**
- Users prioritize quality over quantity (3 excellent tools > 5 mediocre)
- OAuth was critical for adoption (should have been in Wave 1)
- Testing infrastructure paid off (caught 15 bugs pre-release)

## Related Waves

- Wave 2 (Integration): Built on OAuth foundation from Wave 1
- Wave 3 (Intelligence): Tool analytics enabled by Wave 1 telemetry
EOF
```

**Option 2: Archive Section in Vision Doc** (recommended for single vision)

```markdown
# In dev-docs/vision/CAPABILITY_EVOLUTION.md

---

## Archive

### Wave 1: Foundation

**Status:** Delivered in v1.0.0 (2025-09-15)
**Archive Date:** 2025-10-19

[Same content as Option 1]

---

### Wave 2: Integration

**Status:** Deferred Permanently (2025-10-19)
**Archive Date:** 2025-10-19
**Reason:** Market shifted to serverless, integration wave no longer relevant

[Deferred wave details]
```

### Archive Format Template

```markdown
# Wave N: [Name]

**Status:** [Delivered / Deferred / Superseded]
**Archive Date:** YYYY-MM-DD
**Reason:** [Brief reason]

## Original Vision

[Copy original capability theme, motivation, technical sketch]

## Outcome (if Delivered)

**Delivered Features:**
- [List actual features shipped]

**Variance from Vision:**
- [What changed and why]

**Success Metrics:**
- [Target vs. Actual for each metric]

**Learnings:**
- [Key learnings for future waves]

## Rationale (if Deferred/Superseded)

**Why deferred:**
- [Reason 1: e.g., User demand below threshold]
- [Reason 2: e.g., Technical validation failed]

**Alternative approach (if Superseded):**
- [What replaced this wave]

## Related Waves

- [Link to waves that built on this]
- [Link to waves that superseded this]
```

---

## Integration with ROADMAP.md and AGENTS.md

### Keeping ROADMAP.md in Sync

**When to update ROADMAP.md:**

1. **Wave committed:** Add to Near-Term Roadmap
2. **Wave delivered:** Move to Release History
3. **Quarterly review:** Update Vision Highlights section

**Example workflow:**

```bash
# Step 1: Wave 2 meets criteria (quarterly review)
# Update vision doc:
echo "Wave 2: COMMITTED to v1.5.0" >> dev-docs/vision/CAPABILITY_EVOLUTION.md

# Step 2: Add to ROADMAP.md
cat >> ROADMAP.md <<'EOF'
### v1.5.0 (Q1 2026)

**Goal:** Enable integration with external systems (from Wave 2 vision)

**Features:**
- GitHub integration
- Notion integration
- API adapter framework

See [dev-docs/vision/CAPABILITY_EVOLUTION.md](dev-docs/vision/CAPABILITY_EVOLUTION.md) Wave 2 for decision criteria and success metrics.
EOF

# Step 3: When v1.5.0 ships, update both docs
# ROADMAP.md: Move v1.5.0 to Release History
# Vision doc: Archive Wave 2
```

### Keeping AGENTS.md in Sync

**Update Strategic Context when:**

1. **Current priority changes:** New sprint/milestone
2. **Wave commits to roadmap:** Update long-term vision
3. **Quarterly review:** Refresh capability themes list

**Example:**

```markdown
# In AGENTS.md

### Strategic Context

**Current Priority:** Deliver Wave 2 integration features (v1.5.0)
- See [ROADMAP.md](ROADMAP.md) for committed work
- Focus:
  - GitHub API integration
  - Notion API integration
  - OAuth flow completion

**Long-Term Vision:** Enable intelligent, community-driven ecosystem
- See [dev-docs/vision/](dev-docs/vision/) for future capabilities
- Waves:
  - Wave 1: Foundation ✅ (delivered v1.0.0)
  - Wave 2: Integration 🔄 (in progress, v1.5.0)
  - Wave 3: Intelligence 📋 (exploratory, post-v2.0)
  - Wave 4: Ecosystem 📋 (exploratory, post-v3.0)

**Design Principle:** Deliver current commitments while keeping future doors open.
```

### Link Validation Workflow

**Before each release:**

```bash
# Check all vision → roadmap links
grep -r "ROADMAP.md" dev-docs/vision/*.md

# Check all roadmap → vision links
grep -r "dev-docs/vision" ROADMAP.md

# Check all agents → vision links
grep -r "dev-docs/vision" AGENTS.md

# Verify files exist
test -f ROADMAP.md && echo "✅ ROADMAP.md exists"
test -d dev-docs/vision && echo "✅ Vision directory exists"
test -f dev-docs/vision/CAPABILITY_EVOLUTION.md && echo "✅ Vision doc exists"
```

**Fix broken links:**

```bash
# If vision doc renamed
sed -i 's|CAPABILITY_EVOLUTION.md|MY_NEW_VISION.md|g' ROADMAP.md AGENTS.md

# If directory moved
sed -i 's|dev-docs/vision|docs/vision|g' ROADMAP.md AGENTS.md
```

---

## Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| **Vision docs out of sync with roadmap** | ROADMAP.md shows Wave 2, but vision doc still says "exploratory" | Update vision doc status: `Wave 2: COMMITTED to v1.5.0 (see ROADMAP.md)` |
| **Too many waves (complexity)** | 8+ waves, hard to track | Consolidate: Merge related waves, archive distant futures (Wave 6+) |
| **Decision criteria unclear** | Criteria like "good adoption" (vague) | Make quantitative: "50+ active users" (specific, measurable) |
| **No user demand signals** | Can't measure if users want features | Add telemetry (opt-in), track GitHub issues, run user surveys |
| **Waves never committed** | All waves stay "exploratory" forever | Review criteria: Are targets too high? Adjust to realistic thresholds |
| **Vision contradicts roadmap** | Vision says "defer", roadmap says "v1.5" | **Roadmap wins** (committed > exploratory). Update vision to match |
| **Links broken** | `dev-docs/vision/` links 404 | Check file exists, verify relative paths correct, run link validation script |
| **Quarterly reviews skipped** | Last review 18 months ago | Schedule recurring calendar reminder, assign owner, make lightweight (30-60 min) |

---

## Best Practices

### Do

- ✅ **Keep waves high-level** - Themes, not feature lists
- ✅ **Update quarterly** - Schedule recurring reviews
- ✅ **Archive delivered waves** - Historical record valuable
- ✅ **Link to user feedback** - GitHub issues, discussions
- ✅ **Make criteria measurable** - Numbers, not adjectives
- ✅ **Sync with ROADMAP.md** - Single source of truth (roadmap wins)

### Don't

- ❌ **Don't build Wave N in Wave N-1** - No premature implementation
- ❌ **Don't make vision a 5-year plan** - Too specific, will change
- ❌ **Don't skip reviews** - Vision goes stale quickly
- ❌ **Don't commit without criteria met** - Discipline prevents scope creep
- ❌ **Don't have 10+ waves** - Too complex, consolidate

---

## Related Documentation

- **Explanation:** [Vision-Driven Development](../explanation/vision-driven-development.md) - Philosophy and concepts
- **Reference:** [Template Configuration](../reference/template-configuration.md) - `include_vision_docs` variable
- **Vision Guide:** [dev-docs/vision/README.md](../../dev-docs/vision/README.md) - Vision maintenance guide
- **Vision Example:** [CAPABILITY_EVOLUTION.example.md](../../dev-docs/vision/CAPABILITY_EVOLUTION.example.md) - Vision document template

---

**Last Updated:** 2025-10-19
**Version:** chora-base v1.3.1
**Status:** Complete

🗺️ Maintain vision documents to guide strategic decisions across quarters and years.
