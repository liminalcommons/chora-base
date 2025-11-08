# Roadmap - SAP Verification Test Server

This document outlines **committed features and timelines** for SAP Verification Test Server.

**Status:** Living document (updated with each release)
**Current Version:** 0.1.0

---

## How We Execute This Roadmap

### Sprint Planning

**Process:** [project-docs/sprints/README.md](project-docs/sprints/README.md)

- **Cadence:** 1-2 week sprints with capacity planning
- **Commitment:** Never >80% of available capacity
- **Tracking:** Velocity and burndown charts

### Development Process

**Details:** [dev-docs/workflows/DEVELOPMENT_PROCESS.md](dev-docs/workflows/DEVELOPMENT_PROCESS.md)

- **DDD:** Write docs first → saves 8-15 hours of rework
- **BDD:** Define acceptance criteria with Gherkin → prevents 2-5 acceptance issues
- **TDD:** Test-driven implementation → 40-80% fewer defects (Microsoft Research)

### Quality Gates

**Metrics:** [project-docs/metrics/PROCESS_METRICS.md](project-docs/metrics/PROCESS_METRICS.md)

- **Test Coverage:** ≥85%
- **Process Adherence:** ≥90% workflow compliance
- **Defect Rate:** <3 per release

---

## Current Focus

### v0.1.0 (Current)

**Target:** [INSERT TARGET DATE]
**Status:** In Development

**Goal:** Establish core functionality and validate product-market fit

**Features:**

- [ ] **Core MCP Server** - Standard protocol implementation
- [ ] **Essential Tools** - 3-5 high-value tools
  - [ ] Tool 1: [Description]
  - [ ] Tool 2: [Description]
  - [ ] Tool 3: [Description]
- [ ] **Error Handling** - Robust error reporting
- [ ] **Documentation** - README, AGENTS.md, examples
- [ ] **Testing** - Unit tests with ≥85% coverage

**Success Criteria:**
- All features delivered and tested
- Coverage ≥85%
- Documentation complete
- [Add project-specific criteria]

---

## Near-Term Roadmap

### v[Next Version] (Planned)

**Target:** [INSERT TARGET DATE]
**Status:** Planning

**Goal:** [Describe next milestone goal]

**Candidate Features:**
- Feature A: [Description]
- Feature B: [Description]
- Feature C: [Description]

**Note:** Features will be confirmed based on v0.1.0 feedback and user demand.

---

## Future Vision: Capability Evolution

**See:** [dev-docs/vision/](dev-docs/vision/) for long-term capability vision.

**Note:** Vision documents describe **potential evolutionary directions** based on
founding vision and anticipated needs. These are **NOT committed features** - they
represent possible future development after current roadmap stabilizes.

**Current Priority:** v0.1.0 remains the focus. Future capabilities will be
evaluated after v0.1.0 based on user needs and adoption.

### Vision Highlights

The evolution explores potential capability waves beyond v0.1.0:

**Wave 1: Foundation** (Current)
- Status: In development (v0.1.0)
- Focus: Core functionality, essential features
- Delivery: [Target date]

**Wave 2: [Next Capability Theme]** (Post-v0.1.0 Vision)
- Status: Exploratory (not committed)
- Focus: [Brief description of next wave]
- Decision: After v0.1.0 stabilizes, based on:
  - User demand signals (issues, feedback, adoption)
  - Technical validation (architecture supports extensions)
  - Team capacity (resources available for next phase)

**Example Wave 2 Themes (Exploratory):**
- Tool chaining and composition
- External API integrations
- Data persistence and caching
- Advanced configuration

**See [dev-docs/vision/CAPABILITY_EVOLUTION.md](dev-docs/vision/CAPABILITY_EVOLUTION.md) for:**
- Detailed wave descriptions
- Decision criteria (go/no-go frameworks)
- Success metrics
- Technical sketches
- Quarterly review process

**Key Principle:** Build for today, design for tomorrow. Vision guides architectural
decisions *today* without committing to timelines *tomorrow*.

---

## Release History

### v0.1.0 (Initial Release)

**Released:** [INSERT RELEASE DATE]
**Status:** Current

**Features:**
- Initial project setup
- Core functionality
- Basic documentation
- Testing infrastructure

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

---

## Roadmap Philosophy

### Committed vs. Exploratory

| Type | Description | Location | Changes |
|------|-------------|----------|---------|
| **Committed** | Features with timelines | This document (ROADMAP.md) | Stable, changes = scope change |
| **Exploratory** | Potential future directions | [dev-docs/vision/](dev-docs/vision/) | Fluid, updated quarterly |

### Roadmap Updates

**Frequency:** Updated with each release and major milestone
**Process:**
1. Delivered features move to Release History
2. Next version features move to Current Focus
3. Planned features shift to Near-Term Roadmap
4. Exploratory features stay in vision documents until committed

### Feedback & Requests

**Feature Requests:** [GitHub Issues](https://github.com/sapverifier/sap-verification-test-server/issues)
**Discussions:** [GitHub Discussions](https://github.com/sapverifier/sap-verification-test-server/discussions)

**Note:** All requests are considered, but inclusion in roadmap depends on:
- Alignment with project vision
- User demand and adoption
- Team capacity and resources
- Technical feasibility

---

## Contributing to Roadmap

Want to influence the roadmap?

1. **Use the project** - Adoption signals value
2. **File issues** - Describe your needs clearly
3. **Contribute code** - PRs for features you need
4. **Join discussions** - Share your use cases
5. **Review vision docs** - Comment on exploratory waves in [dev-docs/vision/](dev-docs/vision/)

---

**Last Updated:** [INSERT DATE]
**Version:** v0.1.0
**Status:** Living document

🗺️ This roadmap reflects committed work. See [dev-docs/vision/](dev-docs/vision/) for long-term possibilities.