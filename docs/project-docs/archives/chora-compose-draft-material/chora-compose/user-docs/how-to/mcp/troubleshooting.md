# MCP Server Troubleshooting Guide

This guide helps you diagnose and resolve common issues when using the Chora Compose MCP server with Claude Desktop.

---

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Connection Issues](#connection-issues)
3. [Tool Execution Errors](#tool-execution-errors)
4. [Configuration Issues](#configuration-issues)
5. [Performance Issues](#performance-issues)
6. [Debug Mode](#debug-mode)
7. [Common Error Codes](#common-error-codes)
8. [Getting Help](#getting-help)

---

## Setup Issues

### Claude Desktop doesn't see the MCP server

**Symptoms:**
- Server not listed in Claude Desktop MCP tools
- No chora-compose tools available in Claude

**Solutions:**

**1. Verify config file location**

Check that your MCP configuration exists:

```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cat ~/.config/Claude/claude_desktop_config.json

# Windows
type %APPDATA%\Claude\claude_desktop_config.json
```

You should see a `chora-compose` entry under `mcpServers`.

**2. Validate JSON syntax**

Ensure your config file is valid JSON:

```bash
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If this command fails, you have a syntax error in your config file.

**3. Verify config content**

Your configuration should look like this:

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

**4. Check the working directory path**

The `cwd` field must be an **absolute path** to your chora-compose installation:

- ✅ Correct: `/Users/yourname/projects/chora-compose`
- ❌ Wrong: `~/projects/chora-compose` (tilde not expanded)
- ❌ Wrong: `../chora-compose` (relative path)

Get the absolute path:

```bash
cd /path/to/chora-compose
pwd
# Copy this path into your config
```

**5. Restart Claude Desktop**

After making changes:
1. Fully quit Claude Desktop (don't just close the window)
2. Relaunch the application
3. Wait 10-15 seconds for MCP initialization
4. Try asking Claude about available MCP tools

---

### ModuleNotFoundError when server starts

**Symptoms:**

```
ModuleNotFoundError: No module named 'chora_compose'
```

**Solutions:**

**1. Install dependencies**

```bash
cd /path/to/chora-compose
poetry install
```

**2. Verify Poetry environment**

```bash
poetry env info
```

You should see an active virtualenv. If not, run `poetry install` again.

**3. Test the import manually**

```bash
poetry run python -c "from chora_compose.mcp import server; print('OK')"
```

If this prints `OK`, the module is installed correctly.

---

### FastMCP not found

**Symptoms:**

```
ModuleNotFoundError: No module named 'fastmcp'
```

**Solution:**

Install the FastMCP dependency:

```bash
cd /path/to/chora-compose
poetry add fastmcp
```

Or if using pip:

```bash
pip install fastmcp
```

---

## Connection Issues

### Server starts but disconnects immediately

**Symptoms:**
- Server appears briefly in Claude Desktop
- Immediately disconnects
- Error messages in Claude Desktop logs

**Solutions:**

**1. Run the server manually to see errors**

```bash
cd /path/to/chora-compose
poetry run python src/chora_compose/mcp/server.py
```

The server should start and wait for input. If it crashes immediately, you'll see the error message.

Press Ctrl+C to stop the server.

**2. Check for import errors**

Test that all modules can be imported:

```bash
poetry run python -c "
import sys
sys.path.insert(0, 'src')
from chora_compose.mcp import server
from chora_compose.mcp import tools
print('All modules loaded successfully')
"
```

**3. Verify dependencies installed**

```bash
poetry install
poetry run python -c "import pydantic, jinja2, fastmcp; print('Dependencies OK')"
```

---

### Connection timeout in Claude Desktop

**Symptoms:**
- Server doesn't respond to tool calls
- Timeout errors after 30 seconds
- Claude reports the server is unresponsive

**Solutions:**

**1. Check server startup time**

The server must start quickly (under 2 seconds):

```bash
time poetry run python src/chora_compose/mcp/server.py &
# Should complete in < 2 seconds
```

If startup is slow, you may have:
- Slow imports
- Network calls during initialization
- Heavy computation at startup

**2. Test tool responsiveness**

Use the `hello_world` tool (if available) to test basic connectivity:

Ask Claude:
```
Call the hello_world MCP tool.
```

This should respond immediately (under 100ms).

**3. Check system resources**

Ensure your system has adequate resources:
- CPU not overloaded
- Sufficient memory available
- No disk I/O bottlenecks

---

## Tool Execution Errors

### config_not_found error

**Symptoms:**

```json
{
  "success": false,
  "error": {
    "code": "config_not_found",
    "message": "Config 'my-config' not found"
  }
}
```

**Solutions:**

**1. Verify config file exists**

Check that your configuration file exists:

```bash
# For content configs
ls configs/content/my-config/my-config.json

# For artifact configs
ls configs/artifacts/my-artifact/my-artifact.json
```

**2. Check working directory**

Config paths are relative to the `cwd` specified in your Claude Desktop MCP configuration.

Verify the `cwd` path points to your chora-compose installation root (where the `configs/` directory exists).

**3. Verify config ID matches filename**

The config ID must match the filename (without extension):
- File: `simple-readme.json`
- Config ID: `simple-readme`

**4. Validate JSON syntax**

```bash
python -m json.tool path/to/config.json
```

If this fails, you have invalid JSON.

---

### generator_not_found error

**Symptoms:**

```json
{
  "error": {
    "code": "generator_not_found",
    "message": "Generator 'custom_gen' not found"
  }
}
```

**Solutions:**

**1. List available generators**

Ask Claude to list generators:
```
Use list_generators to show me all available generators.
```

Check if your generator is in the list.

**2. Verify generator type in config**

Ensure your content config references a valid built-in generator:

```json
{
  "generation": {
    "patterns": [{
      "type": "demonstration"
    }]
  }
}
```

**3. Valid built-in generators**

- `demonstration` - Example-based generation
- `jinja2` - Full Jinja2 templating
- `template_fill` - Simple variable substitution
- `code_generation` - AI-powered code generation (requires API key)
- `bdd_scenario_assembly` - BDD test scenario assembly

---

### generation_failed error

**Symptoms:**

```json
{
  "error": {
    "code": "generation_failed",
    "message": "Template syntax error"
  }
}
```

**Solutions:**

**1. Check template syntax**

Depending on your generator:

**For jinja2:**
- Verify Jinja2 syntax is correct
- Check for unclosed tags: `{% if %}...{% endif %}`
- Validate filter usage: `{{ value|upper }}`

**For template_fill:**
- Use `{{variable}}` format (double curly braces)
- No spaces inside braces: `{{name}}` not `{{ name }}`

**For demonstration:**
- Ensure `example_output` field exists in elements
- Verify elements are properly referenced in patterns

**2. Validate context variables**

Ensure all required variables are provided:

```python
# Missing variables will cause generation to fail
context = {
  "name": "value",
  "required_var": "value"
}
```

Check the error message for which variables are missing.

**3. Test generation manually**

Create a minimal test to isolate the issue:

```python
from chora_compose.generators.registry import GeneratorRegistry

registry = GeneratorRegistry()
gen = registry.get("jinja2")

# Test with simple template
result = gen.generate(
    template="Hello, {{name}}!",
    context={"name": "World"}
)
print(result)
```

---

### invalid_config_id error (Security)

**Symptoms:**

```json
{
  "error": {
    "code": "invalid_config_id",
    "message": "Config ID contains invalid path characters"
  }
}
```

**Cause:**

Path traversal attempt detected. Config IDs cannot contain:
- `..` (parent directory)
- `/` or `\` (path separators)
- Other path manipulation characters

**Solution:**

Use simple config IDs without path components:

- ✅ Correct: `my-config`, `user-profile`, `release-notes`
- ❌ Wrong: `../my-config`, `/etc/config`, `..\\config`

This is a security feature working as intended to prevent path traversal attacks.

---

## Configuration Issues

### Pydantic validation errors

**Symptoms:**

```
ValidationError for ContentConfig
metadata.description
  Field required [type=missing]
```

**Solutions:**

**1. Check required fields**

Ensure all required fields are present:

```json
{
  "type": "content",
  "id": "my-config",
  "schemaRef": {
    "uri": "file://schemas/content/v3.1/schema.json",
    "version": "3.1"
  },
  "metadata": {
    "description": "Required description",
    "version": "1.0.0"
  },
  "elements": [
    {
      "name": "content",
      "description": "Main content",
      "format": "markdown"
    }
  ],
  "generation": {
    "patterns": [...]
  }
}
```

**2. Use the validate_content tool**

Ask Claude to validate your config:

```
Use validate_content to check if my config "my-config" is valid.
```

This will return detailed validation errors.

**3. Check enum values**

Some fields accept only specific values:

```json
{
  "metadata": {
    "compositionStrategy": "concat"
  }
}
```

Valid values: `concat`, `merge`, `template`, `custom`

---

### Elements validation fails

**Symptoms:**

```
elements
  List should have at least 1 item after validation
```

**Solution:**

Add at least one element to your config:

```json
{
  "elements": [
    {
      "name": "content",
      "description": "Main content section",
      "format": "markdown",
      "example_output": "# Example\n\nContent here."
    }
  ]
}
```

Every content config must have at least one element.

---

## Performance Issues

### Slow content generation

**Symptoms:**
- Tool calls take more than 10 seconds
- Timeout warnings
- Sluggish responses

**Solutions:**

**1. Clear ephemeral storage**

Old generated content can slow down operations:

```bash
cd /path/to/chora-compose
rm -rf ephemeral/*
```

**2. Use idempotency**

Set `force=false` (default) to reuse previously generated content:

- First call: Generates fresh content (~2 seconds)
- Subsequent calls: Returns cached content (~100ms)

**3. Optimize configs**

Reduce complexity:
- Fewer elements per config
- Simpler templates
- Smaller context objects
- Remove unnecessary patterns

**4. Check AI-powered generators**

The `code_generation` generator requires API calls, which are slower:
- Ensure `ANTHROPIC_API_KEY` is valid
- Check network connectivity
- Verify API rate limits not exceeded

---

### High memory usage

**Symptoms:**
- Server uses more than 500MB memory
- System slowdown
- Memory warnings

**Solutions:**

**1. Monitor memory usage**

```bash
ps aux | grep python | grep chora_compose
```

**2. Restart the server**

Claude Desktop automatically restarts the MCP server if it crashes. You can also:
1. Quit Claude Desktop
2. Relaunch it
3. Server will restart fresh

**3. Check for large configs**

Very large configuration files can consume memory:
- Keep configs under 100KB
- Split large artifacts into smaller pieces
- Use references instead of embedding content

---

## Debug Mode

### Enable detailed logging

**1. Run server manually**

Start the server outside Claude Desktop to see all output:

```bash
cd /path/to/chora-compose
poetry run python src/chora_compose/mcp/server.py
```

The server logs to stderr, which you'll see in the terminal.

**2. Test specific tools**

Create a test script:

```python
import asyncio
from chora_compose.mcp.tools import generate_content

async def test():
    result = await generate_content(
        content_config_id="simple-readme",
        context={},
        force=False
    )
    print(result)

asyncio.run(test())
```

Run it:

```bash
poetry run python test_tool.py
```

**3. Add debug logging**

Edit the server code to add debug output:

```python
import sys

# Add debug statements
print(f"DEBUG: Processing request", file=sys.stderr)
```

---

### Verify tool registration

Check which tools are registered:

```python
from chora_compose.mcp.server import mcp

# List all registered tools
print("Registered tools:")
for tool in mcp.list_tools():
    print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
```

Expected output:
- `generate_content`
- `assemble_artifact`
- `list_generators`
- `validate_content`
- `hello_world` (optional)
- `code_generation` (optional, if API key set)

---

## Common Error Codes

| Error Code | Meaning | Typical Cause | Solution |
|------------|---------|---------------|----------|
| `config_not_found` | Config file not found | Wrong path or filename | Check file exists and `cwd` is correct |
| `invalid_config_id` | Security violation | Path traversal attempt | Use simple config IDs without path separators |
| `generator_not_found` | Generator not registered | Typo or missing dependency | Use `list_generators` to see available generators |
| `generation_failed` | Generator execution error | Template syntax or context issue | Check template syntax and required variables |
| `assembly_failed` | Artifact assembly error | Missing content or composition issue | Verify all content pieces exist and are valid |
| `validation_failed` | Schema validation error | Invalid config structure | Use `validate_content` tool for details |
| `internal_error` | Unexpected server error | Bug or resource issue | Check logs and report issue |

---

## Getting Help

### Documentation Resources

1. **MCP Setup Guide**: [README.md](README.md) - Installation and configuration
2. **Tool Reference**: [tool-reference.md](tool-reference.md) - Complete API documentation
3. **End-to-End Exercise**: [end-to-end-exercise.md](end-to-end-exercise.md) - Validation workflow
4. **Examples**: [/examples](../../examples/) - Working sample configurations

### Support Channels

**Report bugs:**
- GitHub Issues: https://github.com/liminalcommons/chora-compose/issues
- Include:
  - Error messages (full text)
  - Configuration files (sanitized)
  - Steps to reproduce
  - System info (OS, Python version)

**Get help:**
- Check existing GitHub Issues for similar problems
- Review the troubleshooting guide (this document)
- Test with sample configurations from `/examples`

---

## FAQ

**Q: Can I use relative paths in configs?**

A: Yes, relative paths are resolved relative to the `cwd` specified in your Claude Desktop MCP configuration.

**Q: How do I add custom generators?**

A: Custom generator plugins are planned for a future release. Currently, you can use the 5 built-in generators.

**Q: Can I run multiple MCP servers?**

A: Yes, add multiple entries under `mcpServers` in your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "chora-compose": { ... },
    "another-server": { ... }
  }
}
```

**Q: Is there a way to test without Claude Desktop?**

A: Yes, write Python scripts that import and call the tools directly (see [Debug Mode](#debug-mode) section).

**Q: What Python version is required?**

A: Python 3.12 or higher is required (specified in `pyproject.toml`).

**Q: How do I update to the latest version?**

A: Pull the latest code and reinstall:

```bash
cd /path/to/chora-compose
git pull
poetry install
```

Then restart Claude Desktop.

---

**Document Version:** 1.2.0
**Last Updated:** 2025-10-15
**Feedback:** [GitHub Issues](https://github.com/liminalcommons/chora-compose/issues)
