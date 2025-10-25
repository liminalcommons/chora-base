"""Publishing workflow for validated configuration artifacts.

This module implements the publish workflow following the domain model from
project-docs/capabilities/config-publishing.md

Workflow steps:
1. Validate configuration
2. Sign payload
3. Create artifact
4. Store artifact
5. Update profile index
"""

from typing import Any

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.registry import ClientRegistry
from mcp_orchestrator.storage import ArtifactStore


class ValidationError(Exception):
    """Raised when configuration validation fails."""

    def __init__(self, validation_result: dict[str, Any]):
        self.validation_result = validation_result
        errors = validation_result.get("errors", [])
        error_codes = [e["code"] for e in errors]
        super().__init__(f"Validation failed with errors: {', '.join(error_codes)}")


class PublishingWorkflow:
    """Orchestrates validated configuration publishing.

    This workflow ensures:
    - Configuration is validated before signing
    - Artifacts are cryptographically signed
    - Metadata is enriched (generator, changelog, server_count)
    - Storage operations are atomic
    - Profile index is updated

    Domain Service: Coordinates multiple domain entities and repositories.

    Example:
        >>> store = ArtifactStore()
        >>> client_registry = ClientRegistry()
        >>> workflow = PublishingWorkflow(store, client_registry)
        >>>
        >>> result = workflow.publish(
        ...     builder=builder,
        ...     private_key_path="~/.mcp-orchestration/keys/signing.key",
        ...     signing_key_id="default",
        ...     changelog="Added filesystem server"
        ... )
        >>> print(result["artifact_id"])
    """

    def __init__(
        self,
        store: ArtifactStore,
        client_registry: ClientRegistry,
    ):
        """Initialize publishing workflow.

        Args:
            store: Artifact storage repository
            client_registry: Client registry for validation
        """
        self.store = store
        self.client_registry = client_registry

    def publish(
        self,
        builder: ConfigBuilder,
        private_key_path: str,
        signing_key_id: str,
        changelog: str | None = None,
    ) -> dict[str, Any]:
        """Publish a validated configuration as signed artifact.

        Workflow:
        1. Validate configuration
        2. Sign payload (if validation passes)
        3. Create artifact with metadata
        4. Store artifact
        5. Update profile index

        Args:
            builder: ConfigBuilder with draft configuration
            private_key_path: Path to Ed25519 private key
            signing_key_id: Identifier for signing key
            changelog: Optional changelog message

        Returns:
            Dictionary with:
            - status: "published"
            - artifact_id: SHA-256 content address
            - client_id: Client family
            - profile_id: Profile
            - server_count: Number of servers
            - changelog: Changelog if provided
            - created_at: ISO 8601 timestamp

        Raises:
            ValidationError: If configuration validation fails
            IOError: If storage operation fails

        References:
            - Capability: project-docs/capabilities/config-publishing.md
            - BDD: project-docs/capabilities/behaviors/mcp-config-publish.feature
        """
        # Step 1: Validate configuration
        validation_result = self._validate_config(builder)

        if not validation_result["valid"]:
            raise ValidationError(validation_result)

        # Step 2-4: Sign, create artifact, store
        # We reuse the existing builder.to_artifact() which handles signing
        # But we need to enrich metadata with PublishingWorkflow generator
        artifact = builder.to_artifact(
            signing_key_id=signing_key_id,
            private_key_path=private_key_path,
            changelog=changelog,
        )

        # Enrich metadata to indicate PublishingWorkflow (not just ConfigBuilder)
        artifact.metadata["generator"] = "PublishingWorkflow"

        # Step 5: Store artifact (atomic operation)
        self.store.store(artifact)

        # Return result
        return {
            "status": "published",
            "artifact_id": artifact.artifact_id,
            "client_id": builder.client_id,
            "profile_id": builder.profile_id,
            "server_count": builder.count(),
            "changelog": changelog,
            "created_at": artifact.created_at,
        }

    def _validate_config(
        self,
        builder: ConfigBuilder,
    ) -> dict[str, Any]:
        """Validate draft configuration.

        This implements the same validation logic as the validate_config MCP tool,
        but as a private method for use within the workflow.

        Args:
            builder: ConfigBuilder with draft configuration

        Returns:
            Validation result with:
            - valid: bool
            - errors: list of error dicts
            - warnings: list of warning dicts
            - server_count: int
        """
        from datetime import UTC, datetime

        errors = []
        warnings = []

        # Validation 1: Check for empty config
        if builder.count() == 0:
            errors.append({
                "code": "EMPTY_CONFIG",
                "message": "Configuration is empty. Add at least one server before publishing.",
                "severity": "error",
            })

        # Validation 2: Check each server configuration
        payload = builder.build()
        if "mcpServers" in payload:
            servers = payload["mcpServers"]

            for server_name, server_config in servers.items():
                # Check required fields
                if "command" not in server_config:
                    errors.append({
                        "code": "MISSING_COMMAND",
                        "message": f"Server '{server_name}' is missing required 'command' field.",
                        "severity": "error",
                        "server": server_name,
                    })

                if "args" not in server_config:
                    errors.append({
                        "code": "MISSING_ARGS",
                        "message": f"Server '{server_name}' is missing required 'args' field.",
                        "severity": "error",
                        "server": server_name,
                    })

                # Check args is a list
                if "args" in server_config and not isinstance(server_config["args"], list):
                    errors.append({
                        "code": "INVALID_ARGS_TYPE",
                        "message": f"Server '{server_name}' has invalid 'args' type (must be list).",
                        "severity": "error",
                        "server": server_name,
                    })

                # Check env vars if present
                if "env" in server_config:
                    env_vars = server_config["env"]
                    if not isinstance(env_vars, dict):
                        errors.append({
                            "code": "INVALID_ENV_TYPE",
                            "message": f"Server '{server_name}' has invalid 'env' type (must be dict).",
                            "severity": "error",
                            "server": server_name,
                        })
                    else:
                        # Check for empty env var values
                        for env_key, env_value in env_vars.items():
                            if not env_value or not str(env_value).strip():
                                warnings.append({
                                    "code": "EMPTY_ENV_VAR",
                                    "message": f"Server '{server_name}' has empty environment variable '{env_key}'.",
                                    "severity": "warning",
                                    "server": server_name,
                                })

        # Validation 3: Check client-specific limitations
        try:
            client_def = self.client_registry.get_client(builder.client_id)

            # Check max servers
            max_servers = client_def.limitations.max_servers
            if max_servers and builder.count() > max_servers:
                errors.append({
                    "code": "TOO_MANY_SERVERS",
                    "message": f"Configuration has {builder.count()} servers, but {builder.client_id} supports max {max_servers}.",
                    "severity": "error",
                    "limit": max_servers,
                    "actual": builder.count(),
                })

            # Check max env vars per server
            max_env_vars = client_def.limitations.max_env_vars_per_server
            if max_env_vars and "mcpServers" in payload:
                for server_name, server_config in payload["mcpServers"].items():
                    if "env" in server_config:
                        env_count = len(server_config["env"])
                        if env_count > max_env_vars:
                            errors.append({
                                "code": "TOO_MANY_ENV_VARS",
                                "message": f"Server '{server_name}' has {env_count} env vars, but {builder.client_id} supports max {max_env_vars}.",
                                "severity": "error",
                                "server": server_name,
                                "limit": max_env_vars,
                                "actual": env_count,
                            })

        except Exception:
            # Client not found - add warning but don't fail validation
            warnings.append({
                "code": "UNKNOWN_CLIENT",
                "message": f"Client '{builder.client_id}' not found in registry. Cannot validate client-specific limitations.",
                "severity": "warning",
            })

        # Determine if valid
        valid = len(errors) == 0

        return {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
            "server_count": builder.count(),
            "validated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        }
