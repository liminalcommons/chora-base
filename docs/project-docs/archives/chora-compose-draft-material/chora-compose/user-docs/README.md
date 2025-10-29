# Chora Compose Documentation

Welcome to the Chora Compose documentation! This documentation follows the [Diátaxis framework](https://diataxis.fr) to help you learn, accomplish tasks, find references, and understand concepts.

**Chora Compose** is a configuration-driven framework for generating content and artifacts through Human-AI collaboration, with MCP (Model Context Protocol) server capabilities.

---

## 🧭 Where to Start

### New to Chora Compose?
Start with our **tutorials** to learn the fundamentals:
→ [Installation Tutorial](tutorials/getting-started/01-installation.md)

### Ready to accomplish a specific task?
Check our **how-to guides** for practical solutions:
→ [How-To Guides](how-to/)

### Looking for detailed API information?
Browse our **reference documentation**:
→ [API Reference](reference/)

### Want to understand the concepts?
Read our **explanations** for deeper understanding:
→ [Explanations](explanation/)

---

## 📚 Documentation Structure (Diátaxis)

This documentation is organized into four types:

### 🎓 Tutorials (Learning-Oriented)

**For:** Users learning Chora Compose for the first time
**Goal:** Build foundational knowledge through hands-on lessons

**Getting Started:**
- [01: Installing Chora Compose](tutorials/getting-started/01-installation.md)
- [02: Your First Content Generation](tutorials/getting-started/02-first-generation.md)
- [03: Understanding Content Configs](tutorials/getting-started/03-content-configs.md)
- [04: Understanding Artifact Configs](tutorials/getting-started/04-artifact-configs.md)

**Intermediate:**
- [01: Creating Custom Generators](tutorials/intermediate/01-custom-generators.md)
- [02: Conversational Config Creation](tutorials/intermediate/02-conversational-config-creation.md)

**Advanced:**
- [01: MCP Integration Deep Dive](tutorials/advanced/01-mcp-integration-deep-dive.md)
- [02: Agentic Workflow - End-to-End with Claude Code](tutorials/advanced/02-agentic-workflow.md)
- [03: Docker MCP Deployment with n8n](tutorials/advanced/03-docker-mcp-deployment.md)
- [04: Create a Custom Generator](tutorials/advanced/04-custom-generator-creation.md)
- [05: LLM Agent Integration](tutorials/advanced/05-llm-agent-integration.md)

---

### 🛠️ How-To Guides (Task-Oriented)

**For:** Users who need to solve a specific problem
**Goal:** Get practical steps to accomplish your task

**Configs:**
- [Discover and Browse Configs](how-to/configs/discover-and-browse-configs.md)
- [Create Content Configs](how-to/configs/create-content-configs.md)
- [Create Artifact Configs](how-to/configs/create-artifact-configs.md)
- [Work with Examples in Configs](how-to/configs/work-with-examples.md)
- [Validate Configs](how-to/configs/validate-configs.md)

**Content Generation:**
- [Generate Content from Configs](how-to/generation/generate-content.md)
- [Generate Multiple Artifacts](how-to/generation/generate-multiple-artifacts.md)
- [Delete Generated Content](how-to/generation/delete-content.md)
- [Generate Using Demo Pattern](how-to/generation/generate-demo-pattern.md)
- [Generate Using Template Pattern](how-to/generation/generate-template-pattern.md)

**Generators:**
- [Use Template Fill Generator](how-to/generators/use-template-fill-generator.md)
- [Use BDD Scenario Generator](how-to/generators/use-bdd-scenario-generator.md)
- [Use Code Generation Generator](how-to/generators/use-code-generation-generator.md)

**MCP (Model Context Protocol):**
- [Use MCP Tools](how-to/mcp/use-mcp-tools.md)
- [Access MCP Resources](how-to/mcp/access-mcp-resources.md)
- [Create Configs Conversationally](how-to/mcp/create-configs-conversationally.md)
- [Test Configs Before Saving](how-to/mcp/test-configs-before-saving.md)
- [Modify Draft Configs](how-to/mcp/modify-draft-configs.md)
- [Troubleshoot MCP Issues](how-to/mcp/troubleshooting.md)

**Storage:**
- [Manage Ephemeral Storage](how-to/storage/manage-ephemeral-storage.md)
- [Understand Versioning](how-to/storage/understand-versioning.md)
- [List and Retrieve Content](how-to/storage/list-retrieve-content.md)
- [Clean Up Storage](how-to/storage/cleanup-storage.md)

**Testing:**
- [Test Configs Before Deployment](how-to/testing/test-configs-before-deployment.md)
- [Validate Generated Content](how-to/testing/validate-generated-content.md)

**CI/CD:**
- [Integrate with GitHub Actions](how-to/ci-cd/integrate-with-github-actions.md)

**Deployment:**
- [Deploy Without Docker](how-to/deployment/deploy-without-docker.md)

---

### 📖 Reference (Information-Oriented)

**For:** Users looking up technical details
**Goal:** Provide accurate, comprehensive information

**API Documentation:**
- [API Reference (Hand-written)](reference/api/README.md) - Comprehensive guides
- [API Reference (Auto-generated)](reference/api-generated/README.md) - Technical reference
- [Core Engine API](reference/api/core-engine.md)
- [Generator API](reference/api/generators.md)
- [Validator API](reference/api/validators.md)
- [Storage API](reference/api/storage.md)

**MCP Reference:**
- [MCP Overview](reference/mcp/README.md)
- [Tool Reference (17 tools)](reference/mcp/tool-reference.md)
- [Resource Providers (5 resources)](reference/mcp/resource-providers.md)
- [Capabilities Discovery](reference/api/resources/capabilities.md)

**Generator Reference:**
- [Generator Comparison](reference/generators/generator-comparison.md) - Choose the right generator
- [BDD Scenario Generator API](reference/generators/bdd-scenario-api.md)
- [Built-in Generators](reference/generators/builtin-generators.md)
- [Generator Registry](reference/generators/generator-registry.md)
- [Generator Plugins](reference/generators/generator-plugins.md)

---

### 💡 Explanation (Understanding-Oriented)

**For:** Users seeking deeper conceptual understanding
**Goal:** Clarify and illuminate topics

**Architecture:**
- [Config-Driven Architecture](explanation/architecture/config-driven-architecture.md)
- [Generator Strategy Pattern](explanation/architecture/generator-strategy-pattern.md)
- [Why Jinja2 for Dynamic Generation](explanation/architecture/why-jinja2-for-dynamic-generation.md)
- [Why Two-Layer Validation](explanation/architecture/why-two-layer-validation.md)
- [Conversational Workflow Authoring](explanation/architecture/conversational-workflow-authoring.md)

**Concepts:**
- [Ephemeral Storage vs Artifacts](explanation/concepts/ephemeral-vs-artifacts.md)
- [Human-AI Collaboration Workflows](explanation/concepts/human-ai-collaboration.md)
- [Ephemeral Storage Design](explanation/concepts/ephemeral-storage-design.md)
- [Human-AI Collaboration Philosophy](explanation/concepts/human-ai-collaboration-philosophy.md)
- [Configuration-Driven Development](explanation/concepts/configuration-driven-development.md)
- [Content vs Artifacts](explanation/concepts/content-vs-artifacts.md)

**Design Decisions:**
- [JSON Schema Validation](explanation/design-decisions/json-schema-validation.md)
- [Separate Config Types](explanation/design-decisions/separate-config-types.md)
- [Event-Driven Telemetry](explanation/design-decisions/event-driven-telemetry.md)

**Workflows:**
- [Generator Selection Guide](explanation/workflows/generator-selection-guide.md)
- [Testing and Validation Approaches](explanation/workflows/testing-validation-approaches.md)
- [Batch Processing Patterns](explanation/workflows/batch-processing-patterns.md)

**Generators:**
- [When to Use Which Generator](explanation/generators/when-to-use-which.md)

**Integration:**
- [MCP Workflow Model](explanation/integration/mcp-workflow-model.md)

**Testing:**
- [Testing Philosophy](explanation/testing/testing-philosophy.md)

**Ecosystem:**
- [Position in AI Tooling Landscape](explanation/ecosystem/position-in-ai-tooling.md)
- [Integration with Orchestration](explanation/ecosystem/integration-with-orchestration.md)
- [Agent Integration Playbook](explanation/ecosystem/agent-integration-playbook.md)

**Deployment:**
- [Docker MCP Deployment Rationale](explanation/deployment/docker-mcp-rationale.md)

---

## 🚀 Quick Start

**Get up and running in 30 minutes:**

[Quick Start Guide](QUICK_START_GUIDE.md) - Installation, first generation, and basic commands

---

## 🎯 Common Tasks

### I want to...

**Install Chora Compose**
→ [Installation Tutorial](tutorials/getting-started/01-installation.md)

**Create my first config conversationally**
→ [Conversational Config Creation Tutorial](tutorials/intermediate/02-conversational-config-creation.md)

**Generate content from a config**
→ [Generate Content How-To](how-to/generation/generate-content.md)

**Use MCP tools with Claude Code**
→ [Use MCP Tools How-To](how-to/mcp/use-mcp-tools.md)

**Understand all 17 MCP tools**
→ [MCP Tool Catalog](reference/mcp/tool-reference.md)

**Discover MCP server capabilities**
→ [Capabilities Reference](reference/api/resources/capabilities.md)

**Browse example configs**
→ [Discover Configs How-To](how-to/configs/discover-and-browse-configs.md)

**Understand the architecture**
→ [Config-Driven Architecture Explanation](explanation/architecture/config-driven-architecture.md)

**Build a custom generator**
→ [Custom Generators Tutorial](tutorials/intermediate/01-custom-generators.md)

---

## 📦 What's New in v1.1.0

**MCP Capability Discovery Pattern:**
- 4 new `capabilities://` resources for agent introspection
- Dynamic feature discovery without hardcoded knowledge
- Plugin-aware generator registry reflection

**Config Lifecycle Management:**
- 4 new MCP tools for conversational workflow authoring
- `draft_config`, `test_config`, `save_config`, `modify_config`
- Zero-friction config creation through conversation

**Total MCP Features:**
- 17 MCP tools (13 → 17)
- 5 resource URI families (1 → 5)

See [CHANGELOG.md](../CHANGELOG.md) for complete details.

---

## 🔗 Additional Resources

### Core Project Files
- [README.md](../README.md) - Project overview and setup
- [CHANGELOG.md](../CHANGELOG.md) - Version history and changes
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute

### Developer Documentation
**For AI agents and developers:**
→ [AGENTS.md](../AGENTS.md) - Machine-readable agent instructions

**For team-facing documentation** (planning, retrospectives, architecture decisions):
→ [dev-docs/](../dev-docs/)

### Specifications
- [Event Schema](../specs/event-schema.md)
- [Content Config Schema](../schemas/content-schema.json)
- [Artifact Config Schema](../schemas/artifact-schema.json)

### Example Configs
- [configs/](../configs/) - Example content and artifact configurations

---

## 📊 Documentation Statistics (v1.1.0)

**Diátaxis Framework Documentation:**
- **Tutorials:** 9 documents (getting-started + intermediate + advanced)
- **How-To Guides:** 35 documents (configs, generation, generators, MCP, storage, testing, CI/CD, deployment)
- **Reference:** 16 documents (API, MCP, storage, generators, resources, deployment)
- **Explanation:** 16 documents (architecture, concepts, workflows, testing, ecosystem, integration, deployment)

**Total User Documentation:** 76+ documents (~55,000 lines)

**Documentation Coverage:**
- ✅ 100% of MCP tools documented
- ✅ All v1.1.0 features covered
- ✅ Consistent cross-referencing
- ✅ Complete tutorial pathways

---

## 🤝 Contributing to Documentation

Found an issue or want to improve the docs?

**For documentation issues:**
- Open an issue with label `documentation`
- Submit a pull request with fixes
- See [CONTRIBUTING.md](../CONTRIBUTING.md)

**Documentation standards:**
- Use Markdown for all documentation
- Follow Diátaxis framework principles
- Include code examples where appropriate
- Keep line length ≤120 characters
- Use relative links between docs

---

## 💬 Getting Help

**Unclear documentation?**
→ Open an issue with label `documentation`

**Need a new how-to guide?**
→ Request enhancement with label `docs-enhancement`

**Found an error?**
→ Submit a PR with fix

**Have questions?**
→ See [Quick Start Guide](QUICK_START_GUIDE.md) or ask in discussions

---

**Version:** Chora Compose v1.1.0
**Last Updated:** 2025-10-17
**Documentation Framework:** [Diátaxis](https://diataxis.fr)
