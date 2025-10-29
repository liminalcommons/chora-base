# Chora Compose MCP Server

Integrate Chora Compose with **Claude Desktop** through the Model Context Protocol (MCP). Generate content, assemble artifacts, and validate configurations through natural conversation with Claude.

---

## What is MCP Integration?

The **Model Context Protocol (MCP)** is an open protocol that allows AI applications like Claude Desktop to connect with tools and data sources. The Chora Compose MCP server exposes content generation capabilities directly to Claude.

### Why Use It?

**Natural Workflow:**
- Ask Claude to generate content instead of running commands
- Explore generators and configurations conversationally
- Get instant validation feedback
- Stay in Claude Desktop for your entire workflow

**Powerful Integration:**
- Claude understands your content generation patterns
- Automatic configuration discovery
- Real-time content generation
- Interactive troubleshooting

### Common Use Cases

- Generate documentation from templates
- Assemble multi-part documentation
- Validate configuration files
- Explore available generators
- Prototype content workflows interactively

---

## Quick Start

### Prerequisites

Before installing the MCP server:

- [ ] **Python 3.12+** installed ([Installation Guide](../tutorials/getting-started/01-installation.md))
- [ ] **Chora Compose** installed (`poetry install` complete)
- [ ] **Claude Desktop** application installed
- [ ] Basic familiarity with Chora Compose

### Step 1: Verify Chora Compose Installation

```bash
cd /path/to/chora-compose
poetry run python -c "from chora_compose.mcp import server; print('MCP server ready!')"
```

**Expected:** `MCP server ready!`

If this fails, ensure Chora Compose is properly installed first.

### Step 2: Configure Claude Desktop

**macOS:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** Edit `%APPDATA%\Claude\claude_desktop_config.json`

**Linux:** Edit `~/.config/Claude/claude_desktop_config.json`

Add this configuration (replace `/path/to/chora-compose` with your actual path):

```json
{
  "mcpServers": {
    "chora-compose": {
      "command": "poetry",
      "args": ["run", "python", "src/chora_compose/mcp/server.py"],
      "cwd": "/absolute/path/to/chora-compose",
      "env": {}
    }
  }
}
```

**Important:** Use absolute paths, not relative paths like `~/` or `./`

### Step 3: Restart Claude Desktop

1. **Fully quit** Claude Desktop (⌘+Q on macOS, not just close window)
2. **Relaunch** Claude Desktop
3. **Wait 10-15 seconds** for MCP server initialization

### Step 4: Test the Connection

Open Claude Desktop and send this message:

```
List all available content generators
```

**Expected Response:**

Claude should call the `list_generators` tool and show you:
- demonstration
- jinja2
- template_fill
- code_generation
- bdd_scenario_assembly

**Success!** Your MCP server is connected.

---

## Available Tools

The MCP server exposes 4 core tools for content generation:

### 1. generate_content

Generate content from a configuration file.

**Example prompts:**
```
Generate content using the config ID 'simple-readme'
Generate content from my-docs-content
Create content from the api-reference config
```

**What it does:**
- Loads the specified content configuration
- Runs the appropriate generator (Jinja2, Demonstration, etc.)
- Saves generated content
- Returns content and metadata

**Parameters:**
- `content_config_id` (required) - ID of your content config
- `context` (optional) - Runtime variables for templates
- `force` (optional) - Regenerate even if content exists

**See:** [Complete Tool Documentation](tool-reference.md#generate_content)

### 2. assemble_artifact

Assemble final artifacts from multiple content pieces.

**Example prompts:**
```
Assemble the user-documentation artifact
Create the final artifact from complete-docs config
Assemble artifact called project-readme
```

**What it does:**
- Loads artifact configuration
- Generates all child content pieces
- Composes them according to assembly strategy
- Writes final output file

**Parameters:**
- `artifact_config_id` (required) - ID of artifact config
- `output_path` (optional) - Override default output location
- `force` (optional) - Force reassembly

**See:** [Complete Tool Documentation](tool-reference.md#assemble_artifact)

### 3. list_generators

Discover available content generators.

**Example prompts:**
```
List all available generators
What generators can I use?
Show me the built-in generators
```

**What it does:**
- Returns list of all registered generators
- Shows generator capabilities and status
- Indicates which generators are ready to use

**Parameters:**
- `generator_type` (optional) - Filter by "builtin" or "plugin"
- `include_plugins` (optional) - Include/exclude plugin generators

**Built-in Generators:**
- **demonstration** - Example-based generation
- **jinja2** - Full template engine
- **template_fill** - Simple substitution
- **code_generation** - AI-powered code
- **bdd_scenario_assembly** - BDD test scenarios

**See:** [Complete Tool Documentation](tool-reference.md#list_generators)

### 4. validate_content

Validate configuration files for correctness.

**Example prompts:**
```
Validate the simple-readme configuration
Is my-config valid?
Check if the api-docs config has errors
```

**What it does:**
- Loads the configuration
- Validates against JSON schema
- Checks Pydantic model constraints
- Returns detailed error messages if invalid

**Parameters:**
- `content_or_config_id` (required) - Config to validate
- `validation_rules` (optional) - Custom validation rules

**See:** [Complete Tool Documentation](tool-reference.md#validate_content)

---

## Usage Examples

### Example 1: Generate Documentation

**You:** Generate content from the api-docs config

**Claude:** I'll generate that content for you using the Chora Compose MCP server.

*[Calls generate_content tool with api-docs config]*

**Result:**
- ✓ Loaded configuration: api-docs-content
- ✓ Used generator: jinja2
- ✓ Generated 5,234 characters
- ✓ Saved to: ephemeral/api-docs.md

Your API documentation has been generated successfully!

### Example 2: Explore Generators

**You:** What content generators are available?

**Claude:** Let me check the available generators.

*[Calls list_generators tool]*

**Result:**

I found 5 built-in generators:

1. **demonstration** - Example-based generation
   - Uses example outputs from configs
   - Fast and predictable

2. **jinja2** - Full template engine
   - Supports variables, loops, conditionals
   - Powerful for dynamic content

3. **template_fill** - Simple substitution
   - Basic {{variable}} replacement
   - Lightweight option

4. **code_generation** - AI-powered
   - Generates code from specifications
   - (Coming soon)

5. **bdd_scenario_assembly** - BDD scenarios
   - Creates Gherkin test scenarios
   - (Coming soon)

### Example 3: Validate Configuration

**You:** Is the readme-content config valid?

**Claude:** I'll validate that configuration.

*[Calls validate_content tool]*

**Result:** ✅ Configuration is valid

- Schema validation: passed
- No errors found
- No warnings
- Ready to use for generation

### Example 4: Assemble Complete Artifact

**You:** Assemble the complete-documentation artifact

**Claude:** I'll assemble that artifact for you.

*[Calls assemble_artifact tool]*

**Result:**
- ✓ Loaded artifact config: complete-documentation
- ✓ Generated 3 content pieces
- ✓ Assembled using concat strategy
- ✓ Output written to: output/DOCUMENTATION.md
- ✓ Total size: 12,450 characters

Your documentation artifact has been assembled!

---

## Troubleshooting

### MCP Server Not Appearing

**Symptom:** Claude doesn't respond to generator commands

**Solutions:**
1. Verify `claude_desktop_config.json` exists in correct location
2. Check JSON syntax is valid (no trailing commas)
3. Ensure absolute paths are used (not `~/` or `./`)
4. Restart Claude Desktop completely (⌘+Q then relaunch)
5. Wait 15 seconds after relaunch for initialization

### Configuration Not Found Errors

**Error:** `Config 'my-config' not found`

**Solutions:**
- Verify `cwd` in config points to project root
- Check config exists at: `configs/content/{id}/{id}.json`
- Use correct config ID (matches filename without extension)
- Ensure you're in the correct Chora Compose project

### Generator Not Found Errors

**Error:** `Generator 'xyz' not found`

**Solutions:**
- Run `list_generators` to see available generators
- Check generator name spelling
- Verify generator is registered (for plugins)
- Some generators may not be implemented yet (check status)

### Connection Timeout

**Symptom:** Claude says MCP server isn't responding

**Solutions:**
- Check Chora Compose dependencies are installed
- Verify Python 3.12+ is being used
- Test server manually: `poetry run python src/chora_compose/mcp/server.py`
- Check for error messages in Claude Desktop logs
- Ensure no firewall blocking local connections

### Permission Errors

**Error:** Permission denied accessing files

**Solutions:**
- Check file/directory permissions in project
- Ensure output directories are writable
- Run with appropriate user permissions
- Verify Poetry virtual environment has correct permissions

---

## Advanced Configuration

### Custom Working Directory

If your configs are in a non-standard location:

```json
{
  "mcpServers": {
    "chora-compose": {
      "command": "poetry",
      "args": ["run", "python", "src/chora_compose/mcp/server.py"],
      "cwd": "/custom/project/path",
      "env": {
        "CHORA_COMPOSE_CONFIG_DIR": "/custom/configs"
      }
    }
  }
}
```

### Multiple Chora Compose Instances

Run multiple projects simultaneously:

```json
{
  "mcpServers": {
    "chora-compose-project-a": {
      "command": "poetry",
      "args": ["run", "python", "src/chora_compose/mcp/server.py"],
      "cwd": "/path/to/project-a"
    },
    "chora-compose-project-b": {
      "command": "poetry",
      "args": ["run", "python", "src/chora_compose/mcp/server.py"],
      "cwd": "/path/to/project-b"
    }
  }
}
```

Claude will have access to generators from both projects.

---

## Next Steps

### Learn More

- **[Tool Reference](tool-reference.md)** - Complete MCP tool documentation
- **[End-to-End Exercise](end-to-end-exercise.md)** - Comprehensive testing guide
- **[Troubleshooting Guide](troubleshooting.md)** - Fix common issues
- **[Resource Providers](resource-providers.md)** - Access configs and content

### Explore Chora Compose

- **[Tutorials](../tutorials/)** - Learn Chora Compose fundamentals
- **[How-To Guides](../how-to/)** - Task-oriented recipes
- **[API Reference](../reference/)** - Complete API documentation

---

## Getting Help

### Documentation
- Check [Troubleshooting Guide](troubleshooting.md)
- Review [Tool Reference](tool-reference.md)
- Read [Chora Compose docs](../)

### Support
- **GitHub Issues:** [Report problems](https://github.com/liminalcommons/chora-compose/issues)
- **Search existing issues** before creating new ones
- Include full error messages and reproduction steps

---

**MCP Server Ready!** Start generating content with Claude Desktop.

**Quick test:** Ask Claude to "list available generators" to verify your setup.
