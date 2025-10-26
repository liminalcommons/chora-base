# User Documentation

Welcome to mcp-orchestration user documentation!

This directory contains **end-user documentation** following the [Diátaxis framework](https://diataxis.fr/):

## Directory Structure

- **[tutorials/](tutorials/)** - Learning-oriented guides for new users
- **[how-to/](how-to/)** - Task-oriented guides for solving specific problems
- **[reference/](reference/)** - Information-oriented API specifications and references
- **[explanation/](explanation/)** - Understanding-oriented conceptual documentation

## 🚀 Quick Start

**New to mcp-orchestration?** Follow this path:

1. **[Complete Workflow: Zero to Deployed](how-to/complete-workflow.md)** - End-to-end guide covering all use cases (20 min) **← START HERE**
2. **[Your First Configuration](tutorials/01-first-configuration.md)** - Hands-on tutorial with step-by-step guidance (20 min)
3. **[Manage Configs with Claude](how-to/manage-configs-with-claude.md)** - Conversational workflow (no CLI) (15 min)

**Already installed?** Jump to specific tasks:
- **[Add Server](how-to/add-server-to-config.md)** - Add servers to your config (5 min)
- **[Publish Config](how-to/publish-config.md)** - Validate and publish (5 min)
- **[Deploy Config](how-to/deploy-config.md)** - Deploy to Claude Desktop (5 min)

## All Documentation

### Tutorials (Learning-Oriented)

Learn by doing with hands-on guides:

- **[Your First MCP Configuration](tutorials/01-first-configuration.md)** - Get started in 15 minutes

### How-To Guides (Task-Oriented)

Solve specific problems:

**Complete Workflows:**
- **[Complete Workflow: Zero to Deployed](how-to/complete-workflow.md)** - End-to-end guide (all use cases) (20 min) **← Recommended**
- **[Manage Configs with Claude Desktop](how-to/manage-configs-with-claude.md)** - Conversational workflow (15 min)
- **[Get Started with mcp-orchestration](how-to/get-started.md)** - Install and configure only (10 min)

**Managing Servers:**
- **[Add an MCP Server to Your Config](how-to/add-server-to-config.md)** - Add servers (filesystem, GitHub, etc.)
- **[Remove a Server from Config](how-to/remove-server-from-config.md)** - Remove unwanted servers
- [Add a New MCP Server to Registry](how-to/add-server-to-registry.md) - Register custom servers (advanced)

**Managing Clients:**
- [Add a New MCP Client](how-to/add-new-client.md) - Register new clients (advanced)
- [Discover Available Clients](how-to/discover-clients.md) - See supported clients

**Publishing and Deployment:**
- **[Publish Config](how-to/publish-config.md)** - Validate and publish configurations
- **[Deploy Config](how-to/deploy-config.md)** - Deploy to client applications
- [Check for Updates](how-to/check-config-updates.md) - Detect configuration drift
- [Verify Signatures](how-to/verify-signatures.md) - Verify authenticity

**Legacy Guides:**
- [Get Your First Config](how-to/get-first-config.md) - Retrieve configurations (pre-Wave 1.5)
- [Use a Configuration](how-to/use-config.md) - Manual config application (pre-Wave 1.5)

### Reference (Information-Oriented)

Look up technical details:

- **[MCP Tools API](reference/mcp-tools.md)** - Complete tool reference (13 tools)

### Explanation (Understanding-Oriented)

Understand key concepts:

- **[Cryptographic Signing](explanation/cryptographic-signing.md)** - Why signatures matter
- **[Draft Workflow](explanation/draft-workflow.md)** - Understanding draft → publish pattern

## For Documentation Contributors

See [DOCUMENTATION_STANDARD.md](../DOCUMENTATION_STANDARD.md) for:
- Frontmatter schema requirements
- Writing standards and templates
- How to choose the right document type
- Cross-referencing guidelines

---

**Note:** This directory is for **users** of mcp-orchestration. For developer documentation, see [dev-docs/](../dev-docs/).
