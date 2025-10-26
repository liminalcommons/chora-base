"""Deployment workflow for automated config deployment.

This module implements the DeploymentWorkflow service that orchestrates:
1. Fetching published artifacts
2. Verifying cryptographic signatures
3. Writing configs to client locations
4. Recording deployment events

Wave 1.5 - End-to-End Config Management
"""

import json
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from mcp_orchestrator.crypto import verify_signature
from mcp_orchestrator.registry import ClientRegistry
from mcp_orchestrator.storage import ArtifactStore, ConfigArtifact, StorageError

from .log import DeploymentLog


class DeploymentError(Exception):
    """Raised when deployment fails."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        """Initialize deployment error.

        Args:
            message: Error message
            details: Optional error details (code, context, etc.)
        """
        super().__init__(message)
        self.details = details or {}


class DeploymentResult(BaseModel):
    """Result of deployment operation."""

    status: str = Field(..., description="Deployment status: 'deployed' or 'failed'")
    config_path: str = Field(..., description="Path where config was written")
    artifact_id: str = Field(..., description="Deployed artifact ID")
    deployed_at: str = Field(..., description="ISO 8601 timestamp")


class DeploymentWorkflow:
    """Orchestrates configuration deployment.

    This service coordinates:
    - Artifact resolution (latest or specific ID)
    - Signature verification
    - Config path determination
    - Atomic file writes
    - Deployment logging
    """

    def __init__(
        self,
        store: ArtifactStore,
        client_registry: ClientRegistry,
        deployment_log: DeploymentLog,
        config_base_dir: str | None = None,
        public_key_path: str | None = None
    ):
        """Initialize deployment workflow.

        Args:
            store: Artifact storage
            client_registry: Client registry for config paths
            deployment_log: Deployment event logger
            config_base_dir: Optional base dir for configs (for testing)
            public_key_path: Optional public key path (for testing)
        """
        self.store = store
        self.client_registry = client_registry
        self.deployment_log = deployment_log
        self.config_base_dir = Path(config_base_dir) if config_base_dir else None

        # Public key path (for signature verification)
        if public_key_path:
            self.public_key_path = Path(public_key_path)
        else:
            # Default: ~/.mcp-orchestration/keys/signing.pub
            home = Path.home()
            self.public_key_path = home / ".mcp-orchestration" / "keys" / "signing.pub"

    def deploy(
        self,
        client_id: str,
        profile_id: str,
        artifact_id: str | None = None
    ) -> DeploymentResult:
        """Deploy configuration artifact.

        Steps:
        1. Resolve artifact (latest if not specified)
        2. Fetch artifact from store
        3. Verify signature
        4. Get client config location
        5. Write config atomically
        6. Record deployment

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier
            artifact_id: Optional specific artifact ID (defaults to latest)

        Returns:
            DeploymentResult with status and paths

        Raises:
            DeploymentError: On deployment failure
        """
        # Step 1: Validate client exists (early check)
        client = self.client_registry.get_client(client_id)
        if client is None:
            raise DeploymentError(
                f"Client '{client_id}' not found in registry",
                {"code": "CLIENT_NOT_FOUND", "client_id": client_id}
            )

        # Step 2: Resolve artifact
        artifact = self._resolve_artifact(client_id, profile_id, artifact_id)

        # Step 3: Verify signature
        self._verify_signature(artifact)

        # Step 4: Get config path
        config_path = self._get_config_path(client_id)

        # Step 4: Write config atomically
        try:
            self._write_config_atomic(config_path, artifact.payload)
        except Exception as e:
            raise DeploymentError(
                f"Failed to write config to {config_path}: {e}",
                {"code": "WRITE_FAILED", "path": str(config_path)}
            ) from e

        # Step 5: Record deployment
        changelog = artifact.metadata.get("changelog")
        self.deployment_log.record_deployment(
            client_id=client_id,
            profile_id=profile_id,
            artifact_id=artifact.artifact_id,
            config_path=str(config_path),
            changelog=changelog
        )

        # Step 6: Return result
        return DeploymentResult(
            status="deployed",
            config_path=str(config_path),
            artifact_id=artifact.artifact_id,
            deployed_at=datetime.now(UTC).isoformat().replace("+00:00", "Z")
        )

    def _resolve_artifact(
        self,
        client_id: str,
        profile_id: str,
        artifact_id: str | None
    ) -> ConfigArtifact:
        """Resolve artifact to deploy.

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier
            artifact_id: Optional specific artifact ID

        Returns:
            ConfigArtifact to deploy

        Raises:
            DeploymentError: If artifact not found
        """
        try:
            if artifact_id:
                # Deploy specific artifact
                artifact = self.store.get_by_id(artifact_id)
            else:
                # Deploy latest for client/profile
                artifact = self.store.get(client_id, profile_id)

            return artifact

        except StorageError as e:
            if artifact_id:
                raise DeploymentError(
                    f"Artifact '{artifact_id}' not found",
                    {"code": "ARTIFACT_NOT_FOUND", "artifact_id": artifact_id}
                ) from e
            else:
                raise DeploymentError(
                    f"No published artifact found for {client_id}/{profile_id}",
                    {"code": "ARTIFACT_NOT_FOUND", "client_id": client_id, "profile_id": profile_id}
                ) from e

    def _verify_signature(self, artifact: ConfigArtifact) -> None:
        """Verify artifact signature.

        Args:
            artifact: Artifact to verify

        Raises:
            DeploymentError: If signature invalid
        """
        if not self.public_key_path.exists():
            raise DeploymentError(
                f"Public key not found at {self.public_key_path}",
                {"code": "PUBLIC_KEY_NOT_FOUND"}
            )

        try:
            is_valid = verify_signature(
                payload=artifact.payload,
                signature_b64=artifact.signature,
                public_key_path=str(self.public_key_path)
            )

            if not is_valid:
                raise DeploymentError(
                    "Signature verification failed",
                    {"code": "SIGNATURE_INVALID", "artifact_id": artifact.artifact_id}
                )

        except Exception as e:
            if isinstance(e, DeploymentError):
                raise

            raise DeploymentError(
                f"Signature verification failed: {e}",
                {"code": "SIGNATURE_INVALID"}
            ) from e

    def _get_config_path(self, client_id: str) -> Path:
        """Get config file path for client.

        Args:
            client_id: Client family identifier

        Returns:
            Path to client config file

        Raises:
            DeploymentError: If client not found
        """
        # Get client from registry
        try:
            client = self.client_registry.get_client(client_id)
        except Exception as e:
            raise DeploymentError(
                f"Client '{client_id}' not found in registry",
                {"code": "CLIENT_NOT_FOUND", "client_id": client_id}
            ) from e

        # Get config location
        config_location = client.config_location

        # Expand ~ to home directory
        config_path = Path(config_location).expanduser()

        # Override with test directory if provided
        if self.config_base_dir:
            # For testing: use test directory instead of actual home
            # Convert absolute path to relative, then append to test dir
            if config_path.is_absolute():
                # Remove leading / to make relative
                relative_path = Path(*config_path.parts[1:])
                config_path = self.config_base_dir / relative_path

        return config_path

    def _write_config_atomic(self, config_path: Path, payload: dict[str, Any]) -> None:
        """Write config atomically (with rollback on failure).

        Steps:
        1. Create parent directories
        2. Write to temporary file
        3. Rename to final location (atomic)

        Args:
            config_path: Path to write config
            payload: Config payload (mcpServers structure)

        Raises:
            OSError: On write failure
        """
        # Step 1: Create parent directories
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Step 2: Write to temporary file
        temp_fd, temp_path = tempfile.mkstemp(
            dir=config_path.parent,
            prefix=".tmp_",
            suffix=".json"
        )

        try:
            with open(temp_fd, "w") as f:
                json.dump(payload, f, indent=2)

            # Step 3: Rename to final location (atomic operation)
            shutil.move(temp_path, config_path)

        except Exception:
            # Rollback: delete temp file if still exists
            if Path(temp_path).exists():
                Path(temp_path).unlink()
            raise
