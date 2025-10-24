"""CLI commands for config building (Wave 1.2).

This module provides CLI commands for adding and removing servers from
MCP client configurations.
"""

import json
import sys
from typing import Any

import click

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.servers import get_default_registry


@click.command("add-server")
@click.argument("server_id")
@click.option("--client", "-c", required=True, help="Client family (e.g., claude-desktop)")
@click.option("--profile", "-p", required=True, help="Profile (e.g., default)")
@click.option(
    "--param",
    "-P",
    multiple=True,
    help="Parameter in key=value format (can specify multiple)",
)
@click.option(
    "--env",
    "-e",
    multiple=True,
    help="Environment variable in KEY=VALUE format (can specify multiple)",
)
@click.option(
    "--name", "-n", help="Server name in config (defaults to server_id)"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format",
)
def add_server(
    server_id: str,
    client: str,
    profile: str,
    param: tuple[str, ...],
    env: tuple[str, ...],
    name: str | None,
    format: str,
) -> None:
    """Add a server to the draft configuration.

    Examples:

    \b
    # Add filesystem server with path parameter
    mcp-orchestration-add-server filesystem \\
      --client claude-desktop \\
      --profile default \\
      --param path=/Users/me/Documents

    \b
    # Add github server with environment variable
    mcp-orchestration-add-server github \\
      --client claude-desktop \\
      --profile default \\
      --env GITHUB_TOKEN=ghp_...

    \b
    # Add server with custom name
    mcp-orchestration-add-server filesystem \\
      --client claude-desktop \\
      --profile dev \\
      --param path=/tmp \\
      --name filesystem-tmp
    """
    try:
        # Parse parameters
        params: dict[str, Any] = {}
        for p in param:
            if "=" not in p:
                click.echo(f"Error: Invalid parameter format '{p}'. Use key=value", err=True)
                sys.exit(1)
            key, value = p.split("=", 1)
            params[key] = value

        # Parse environment variables
        env_vars: dict[str, str] = {}
        for e in env:
            if "=" not in e:
                click.echo(f"Error: Invalid env format '{e}'. Use KEY=VALUE", err=True)
                sys.exit(1)
            key, value = e.split("=", 1)
            env_vars[key] = value

        # Get server registry
        registry = get_default_registry()

        # Create builder
        builder = ConfigBuilder(client, profile, registry)

        # Add server
        builder.add_server(
            server_id=server_id,
            params=params if params else None,
            env_vars=env_vars if env_vars else None,
            server_name=name,
        )

        # Output result
        server_name = name or server_id

        if format == "json":
            result = {
                "status": "added",
                "server_name": server_name,
                "client_id": client,
                "profile_id": profile,
                "draft": builder.build(),
                "server_count": builder.count(),
            }
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"✓ Added server '{server_name}' to draft config")
            click.echo(f"  Client: {client}")
            click.echo(f"  Profile: {profile}")
            click.echo(f"  Servers in draft: {builder.count()}")
            click.echo()
            click.echo("Draft configuration:")
            click.echo(json.dumps(builder.build(), indent=2))

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command("remove-server")
@click.argument("server_name")
@click.option("--client", "-c", required=True, help="Client family")
@click.option("--profile", "-p", required=True, help="Profile")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format",
)
def remove_server(
    server_name: str,
    client: str,
    profile: str,
    format: str,
) -> None:
    """Remove a server from the draft configuration.

    Examples:

    \b
    # Remove filesystem server
    mcp-orchestration-remove-server filesystem \\
      --client claude-desktop \\
      --profile default

    \b
    # Remove server with custom name
    mcp-orchestration-remove-server filesystem-tmp \\
      --client claude-desktop \\
      --profile dev
    """
    try:
        # Get server registry
        registry = get_default_registry()

        # Create builder (assumes draft exists - will be empty if not)
        builder = ConfigBuilder(client, profile, registry)

        # This is a limitation: CLI can't persist state between calls
        # In reality, this would need to load an existing draft from somewhere
        # For now, we just demonstrate the API

        click.echo(
            "Note: CLI drafts are not persisted. Use MCP tools for stateful drafts.",
            err=True,
        )
        click.echo(
            "This command demonstrates the API but won't affect saved configs.",
            err=True,
        )
        click.echo()

        # Try to remove (will likely fail since draft is empty)
        builder.remove_server(server_name)

        # Output result
        if format == "json":
            result = {
                "status": "removed",
                "server_name": server_name,
                "client_id": client,
                "profile_id": profile,
                "draft": builder.build(),
                "server_count": builder.count(),
            }
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"✓ Removed server '{server_name}' from draft")
            click.echo(f"  Servers remaining: {builder.count()}")
            click.echo()
            click.echo("Updated draft:")
            click.echo(json.dumps(builder.build(), indent=2))

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
