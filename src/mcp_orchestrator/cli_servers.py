"""CLI commands for MCP server registry browsing.

This module provides CLI commands to browse and discover available MCP servers.

Wave 1.1 (v0.1.1):
- list-servers: List all available MCP servers
- describe-server: Get detailed information about a specific server
"""

import json
from typing import Any

import click

from mcp_orchestrator.servers import get_default_registry
from mcp_orchestrator.servers.models import TransportType


@click.command("list-servers")
@click.option(
    "--transport",
    "-t",
    type=click.Choice(["stdio", "http", "sse"], case_sensitive=False),
    help="Filter by transport type",
)
@click.option(
    "--search",
    "-s",
    help="Search query (searches name, description, tags)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format (default: table)",
)
def list_servers(transport: str | None, search: str | None, format: str) -> None:
    """List available MCP servers in the registry.

    Browse the catalog of known MCP servers that can be added to client
    configurations. Servers can be filtered by transport type or searched by keywords.

    Examples:

        # List all servers
        mcp-orchestration-list-servers

        # List only stdio servers
        mcp-orchestration-list-servers --transport stdio

        # Search for database servers
        mcp-orchestration-list-servers --search database

        # Output as JSON
        mcp-orchestration-list-servers --format json
    """
    registry = get_default_registry()

    # Get servers based on filters
    if search:
        servers = registry.search(search)
    elif transport:
        transport_type = TransportType(transport.lower())
        servers = registry.list_by_transport(transport_type)
    else:
        servers = registry.list_all()

    if format == "json":
        # JSON output
        output = {
            "servers": [
                {
                    "server_id": s.server_id,
                    "display_name": s.display_name,
                    "description": s.description,
                    "transport": s.transport,
                    "npm_package": s.npm_package,
                    "tags": s.tags,
                    "requires_env": s.required_env,
                }
                for s in servers
            ],
            "count": len(servers),
            "transport_counts": registry.get_transport_counts(),
        }
        click.echo(json.dumps(output, indent=2))
    else:
        # Table output
        if not servers:
            click.echo("No servers found.")
            return

        click.echo(f"\nFound {len(servers)} server(s):\n")

        for server in servers:
            # Header
            click.echo(click.style(f"● {server.display_name}", fg="cyan", bold=True))
            click.echo(f"  ID: {server.server_id}")
            click.echo(f"  Transport: {_format_transport(server.transport)}")
            click.echo(f"  Description: {server.description}")

            # Tags
            if server.tags:
                tags_str = ", ".join(server.tags)
                click.echo(f"  Tags: {click.style(tags_str, fg='blue')}")

            # NPM package
            if server.npm_package:
                click.echo(f"  NPM: {server.npm_package}")

            # Environment variables
            if server.required_env:
                env_str = ", ".join(server.required_env)
                click.echo(f"  Requires: {click.style(env_str, fg='yellow')}")

            click.echo()  # Blank line between servers

        # Summary
        transport_counts = registry.get_transport_counts()
        click.echo(click.style("Summary:", bold=True))
        click.echo(f"  stdio: {transport_counts['stdio']}")
        click.echo(f"  http:  {transport_counts['http']}")
        click.echo(f"  sse:   {transport_counts['sse']}")
        click.echo()


@click.command("describe-server")
@click.argument("server_id")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    help="Output format (default: text)",
)
def describe_server(server_id: str, format: str) -> None:
    """Get detailed information about a specific MCP server.

    Shows complete server definition including transport configuration,
    parameters, environment variables, and usage examples.

    Examples:

        # Describe the filesystem server
        mcp-orchestration-describe-server filesystem

        # Get JSON output
        mcp-orchestration-describe-server n8n --format json
    """
    registry = get_default_registry()

    try:
        server = registry.get(server_id)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        raise click.exceptions.Exit(1)

    if format == "json":
        # JSON output
        click.echo(json.dumps(server.model_dump(), indent=2))
    else:
        # Human-readable text output
        click.echo()
        click.echo(click.style(f"● {server.display_name}", fg="cyan", bold=True))
        click.echo()

        # Basic info
        click.echo(click.style("Server ID:", bold=True))
        click.echo(f"  {server.server_id}")
        click.echo()

        click.echo(click.style("Description:", bold=True))
        click.echo(f"  {server.description}")
        click.echo()

        # Transport
        click.echo(click.style("Transport:", bold=True))
        click.echo(f"  Type: {_format_transport(server.transport)}")

        if server.transport == "stdio":
            click.echo(f"  Command: {server.stdio_command}")
            if server.stdio_args:
                click.echo(f"  Args: {' '.join(server.stdio_args)}")
        else:  # http or sse
            click.echo(f"  URL: {server.http_url}")
            click.echo(f"  Auth: {server.http_auth_type or 'none'}")
            click.echo(
                click.style(
                    "  Note: Will be automatically wrapped with mcp-remote for stdio compatibility",
                    fg="yellow",
                )
            )
        click.echo()

        # Parameters
        if server.parameters:
            click.echo(click.style("Parameters:", bold=True))
            for param in server.parameters:
                required_str = "required" if param.required else "optional"
                click.echo(f"  • {param.name} ({param.type}, {required_str})")
                click.echo(f"    {param.description}")
                if param.default is not None:
                    click.echo(f"    Default: {param.default}")
                if param.example:
                    click.echo(f"    Example: {param.example}")
            click.echo()

        # Environment variables
        if server.required_env or server.optional_env:
            click.echo(click.style("Environment Variables:", bold=True))
            if server.required_env:
                for env_var in server.required_env:
                    click.echo(f"  • {env_var} " + click.style("(required)", fg="red"))
            if server.optional_env:
                for env_var in server.optional_env:
                    click.echo(f"  • {env_var} (optional)")
            click.echo()

        # Installation
        if server.npm_package:
            click.echo(click.style("Installation:", bold=True))
            click.echo(f"  NPM Package: {server.npm_package}")
            click.echo(f"  Install: npm install -g {server.npm_package}")
            click.echo("  Or use via: npx (no installation needed)")
            click.echo()

        # Documentation
        if server.documentation_url:
            click.echo(click.style("Documentation:", bold=True))
            click.echo(f"  {server.documentation_url}")
            click.echo()

        # Tags
        if server.tags:
            click.echo(click.style("Tags:", bold=True))
            click.echo(f"  {', '.join(server.tags)}")
            click.echo()

        # Usage example
        click.echo(click.style("Usage Example:", bold=True))
        click.echo(_generate_usage_example(server))
        click.echo()


def _format_transport(transport: str) -> str:
    """Format transport type with color.

    Args:
        transport: Transport type string

    Returns:
        Colored transport string
    """
    if transport == "stdio":
        return click.style("stdio", fg="green")
    elif transport == "http":
        return click.style("http", fg="blue")
    elif transport == "sse":
        return click.style("sse", fg="magenta")
    else:
        return transport


def _generate_usage_example(server: Any) -> str:
    """Generate example configuration snippet for a server.

    Args:
        server: ServerDefinition

    Returns:
        Formatted JSON configuration example
    """
    # Build example args with parameter placeholders
    if server.transport == "stdio":
        args = []
        for arg in server.stdio_args:
            # Replace parameter placeholders with example values
            example_arg = arg
            for param in server.parameters:
                placeholder = f"{{{param.name}}}"
                if placeholder in arg:
                    example_value = param.example or param.default or f"<{param.name}>"
                    example_arg = arg.replace(placeholder, str(example_value))
            args.append(example_arg)

        example = {
            server.server_id: {
                "command": server.stdio_command,
                "args": args,
            }
        }

        if server.required_env or server.optional_env:
            env_vars = {}
            for env_var in server.required_env:
                env_vars[env_var] = f"${{{env_var}}}"
            example[server.server_id]["env"] = env_vars

    else:  # http or sse
        # Show URL with parameter examples
        url = server.http_url
        for param in server.parameters:
            placeholder = f"{{{param.name}}}"
            example_value = param.example or param.default or f"<{param.name}>"
            url = url.replace(placeholder, str(example_value))

        example = {
            server.server_id: {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/mcp-remote", "stdio", url],
            }
        }

        if server.required_env:
            env_vars = {}
            for env_var in server.required_env:
                env_vars[env_var] = f"${{{env_var}}}"
            example[server.server_id]["env"] = env_vars

    return json.dumps({"mcpServers": example}, indent=2)


# CLI group for multiple commands
@click.group()
def servers_cli() -> None:
    """MCP server registry commands."""
    pass


servers_cli.add_command(list_servers)
servers_cli.add_command(describe_server)
