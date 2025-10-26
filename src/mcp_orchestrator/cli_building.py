"""CLI commands for config building (Wave 1.2), publishing (Wave 1.4), and deployment (Wave 1.5).

This module provides CLI commands for adding and removing servers from
MCP client configurations, publishing validated configurations, and deploying
configurations to client locations.
"""

import json
import sys
from pathlib import Path
from typing import Any

import click

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.deployment import DeploymentWorkflow, DeploymentError
from mcp_orchestrator.deployment.log import DeploymentLog
from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError
from mcp_orchestrator.registry import get_default_registry as get_client_registry
from mcp_orchestrator.servers import get_default_registry
from mcp_orchestrator.storage import ArtifactStore


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


@click.command("publish-config")
@click.option("--client", "-c", required=True, help="Client family (e.g., claude-desktop)")
@click.option("--profile", "-p", required=True, help="Profile (e.g., default)")
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to JSON configuration file",
)
@click.option(
    "--changelog",
    "-m",
    help="Changelog message describing the changes",
)
@click.option(
    "--format",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format",
)
def publish_config(
    client: str,
    profile: str,
    file: Path,
    changelog: str | None,
    format: str,
) -> None:
    """Publish a validated configuration from a JSON file.

    This command:
    1. Loads the configuration from a JSON file
    2. Validates the configuration for errors
    3. Signs it with your Ed25519 private key
    4. Stores it as a content-addressable artifact
    5. Updates the profile index

    Examples:

    \b
    # Publish configuration with changelog
    mcp-orchestration-publish-config \\
      --client claude-desktop \\
      --profile default \\
      --file my-config.json \\
      --changelog "Added filesystem and github servers"

    \b
    # Publish configuration (JSON output)
    mcp-orchestration-publish-config \\
      --client claude-desktop \\
      --profile default \\
      --file my-config.json \\
      --format json
    """
    try:
        # Load configuration from file
        with open(file) as f:
            config_data = json.load(f)

        # Validate file structure
        if "mcpServers" not in config_data:
            click.echo(
                "Error: Configuration file missing 'mcpServers' key",
                err=True,
            )
            sys.exit(1)

        if not config_data["mcpServers"]:
            click.echo(
                "Error: Configuration has no servers. Add at least one server.",
                err=True,
            )
            sys.exit(1)

        # Get registries
        server_registry = get_default_registry()
        client_registry = get_client_registry()

        # Create builder and populate from file
        builder = ConfigBuilder(client, profile, server_registry)

        # Add each server from the config file
        for server_name, server_config in config_data["mcpServers"].items():
            # Extract command, args, env from server_config
            command = server_config.get("command")
            args = server_config.get("args", [])
            env = server_config.get("env", {})

            # Note: We're adding "raw" servers, not from registry
            # This allows publishing arbitrary configs from files
            builder._servers[server_name] = {
                "command": command,
                "args": args,
                "env": env,
            }

        # Get signing key paths
        home = Path.home()
        key_dir = home / ".mcp-orchestration" / "keys"
        private_key_path = key_dir / "signing.key"

        if not private_key_path.exists():
            click.echo(
                f"Error: Signing key not found at {private_key_path}",
                err=True,
            )
            click.echo(
                "Run 'mcp-orchestration-init-keys' to generate keys first.",
                err=True,
            )
            sys.exit(1)

        # Use PublishingWorkflow to validate → sign → store
        store = ArtifactStore()
        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        result = workflow.publish(
            builder=builder,
            private_key_path=str(private_key_path),
            signing_key_id="default",
            changelog=changelog,
        )

        # Output result
        if format == "json":
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo("✓ Configuration validated successfully")
            click.echo("✓ Configuration signed with Ed25519")
            click.echo(f"✓ Artifact stored: {result['artifact_id'][:16]}...")
            click.echo("✓ Published successfully!")
            click.echo()
            click.echo(f"Artifact ID: {result['artifact_id']}")
            click.echo(f"Client: {result['client_id']}")
            click.echo(f"Profile: {result['profile_id']}")
            click.echo(f"Server count: {result['server_count']}")
            if changelog:
                click.echo(f"Changelog: {changelog}")

    except ValidationError as e:
        # Validation errors
        errors = e.validation_result.get("errors", [])
        click.echo("✗ Configuration validation failed", err=True)
        click.echo()
        for error in errors:
            click.echo(f"  [{error['code']}] {error['message']}", err=True)
        sys.exit(1)

    except FileNotFoundError:
        click.echo(f"Error: Configuration file not found: {file}", err=True)
        sys.exit(1)

    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON in configuration file: {e}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command("deploy-config")
@click.option("--client", "-c", required=True, help="Client family (e.g., claude-desktop)")
@click.option("--profile", "-p", required=True, help="Profile (e.g., default)")
@click.option(
    "--artifact-id",
    "-a",
    help="Specific artifact ID to deploy (defaults to latest)",
)
@click.option(
    "--format",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format",
)
def deploy_config(
    client: str,
    profile: str,
    artifact_id: str | None,
    format: str,
) -> None:
    """Deploy a published configuration to the client's config location.

    This command:
    1. Resolves the artifact to deploy (latest or specific version)
    2. Verifies the artifact's Ed25519 signature
    3. Writes the configuration to the client's config file
    4. Records the deployment in the deployment log

    The config is written to the client-specific location:
    - Claude Desktop (macOS): ~/Library/Application Support/Claude/claude_desktop_config.json
    - Cursor: ~/.cursor/mcp_config.json

    Examples:

    \b
    # Deploy latest configuration
    mcp-orchestration-deploy-config \\
      --client claude-desktop \\
      --profile default

    \b
    # Deploy specific version (rollback)
    mcp-orchestration-deploy-config \\
      --client claude-desktop \\
      --profile default \\
      --artifact-id abc123...

    \b
    # Deploy with JSON output
    mcp-orchestration-deploy-config \\
      --client claude-desktop \\
      --profile default \\
      --format json
    """
    try:
        # Get deployment dependencies
        home = Path.home()
        base_dir = home / ".mcp-orchestration"

        store = ArtifactStore()
        client_registry = get_client_registry()
        deployment_log = DeploymentLog(
            deployments_dir=str(base_dir / "deployments")
        )

        # Get public key for signature verification
        public_key_path = base_dir / "keys" / "signing.pub"
        if not public_key_path.exists():
            click.echo(
                f"Error: Public key not found at {public_key_path}",
                err=True,
            )
            click.echo(
                "Run 'mcp-orchestration-init-keys' to generate keys first.",
                err=True,
            )
            sys.exit(1)

        # Create deployment workflow
        workflow = DeploymentWorkflow(
            store=store,
            client_registry=client_registry,
            deployment_log=deployment_log,
            public_key_path=str(public_key_path),
        )

        # Deploy configuration
        result = workflow.deploy(
            client_id=client,
            profile_id=profile,
            artifact_id=artifact_id,
        )

        # Output result
        if format == "json":
            click.echo(json.dumps(result.model_dump(), indent=2))
        else:
            click.echo("✓ Configuration deployed successfully!")
            click.echo()
            click.echo(f"Artifact ID: {result.artifact_id}")
            click.echo(f"Config path: {result.config_path}")
            click.echo(f"Deployed at: {result.deployed_at}")
            click.echo()
            click.echo("⚠️  Restart the client application for changes to take effect:")
            if client == "claude-desktop":
                click.echo("  killall Claude && open -a 'Claude'")
            elif client == "cursor":
                click.echo("  Reload window in Cursor (Cmd+Shift+P → 'Developer: Reload Window')")

    except DeploymentError as e:
        # Deployment-specific errors
        error_code = e.details.get("code", "UNKNOWN")
        click.echo(f"✗ Deployment failed: [{error_code}]", err=True)
        click.echo(f"  {e.message}", err=True)

        # Provide helpful guidance based on error code
        if error_code == "CLIENT_NOT_FOUND":
            click.echo()
            click.echo("Available clients:", err=True)
            try:
                for c in client_registry.list_clients():
                    click.echo(f"  - {c.client_id}", err=True)
            except Exception:
                pass

        elif error_code == "ARTIFACT_NOT_FOUND":
            click.echo()
            click.echo("No published artifact found. Publish a configuration first:", err=True)
            click.echo(f"  mcp-orchestration-publish-config --client {client} --profile {profile} --file config.json", err=True)

        elif error_code == "SIGNATURE_INVALID":
            click.echo()
            click.echo("The artifact's signature is invalid. This may indicate:", err=True)
            click.echo("  - Corrupted storage", err=True)
            click.echo("  - Tampering", err=True)
            click.echo("  - Wrong public key", err=True)
            click.echo()
            click.echo("Try re-publishing the configuration.", err=True)

        elif error_code == "WRITE_FAILED":
            click.echo()
            click.echo("Failed to write config file. Check:", err=True)
            click.echo("  - File permissions", err=True)
            click.echo("  - Parent directory exists", err=True)
            click.echo(f"  - Disk space available", err=True)

        sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
