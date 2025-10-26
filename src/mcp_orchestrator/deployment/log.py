"""Deployment logging and history tracking.

This module tracks deployment events and maintains a record of which artifacts
are currently deployed for each client/profile combination.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DeploymentRecord(BaseModel):
    """Record of a single deployment event."""

    artifact_id: str = Field(..., description="Deployed artifact ID")
    config_path: str = Field(..., description="Path where config was written")
    deployed_at: str = Field(..., description="ISO 8601 timestamp")
    changelog: str | None = Field(None, description="Changelog from artifact metadata")


class DeploymentLog:
    """Tracks deployment history for client/profile combinations."""

    def __init__(self, deployments_dir: str):
        """Initialize deployment log.

        Args:
            deployments_dir: Directory to store deployment logs
        """
        self.deployments_dir = Path(deployments_dir)
        self.deployments_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_path(self, client_id: str, profile_id: str) -> Path:
        """Get path to deployment log file for client/profile.

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier

        Returns:
            Path to deployment log JSON file
        """
        client_dir = self.deployments_dir / client_id
        client_dir.mkdir(parents=True, exist_ok=True)
        return client_dir / f"{profile_id}.json"

    def record_deployment(
        self,
        client_id: str,
        profile_id: str,
        artifact_id: str,
        config_path: str,
        changelog: str | None = None
    ) -> None:
        """Record a deployment event.

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier
            artifact_id: Deployed artifact ID
            config_path: Path where config was written
            changelog: Optional changelog from artifact metadata
        """
        log_path = self._get_log_path(client_id, profile_id)

        # Create deployment record
        record = DeploymentRecord(
            artifact_id=artifact_id,
            config_path=config_path,
            deployed_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            changelog=changelog
        )

        # Load existing log or create new
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
        else:
            log_data = {
                "client_id": client_id,
                "profile_id": profile_id,
                "current_deployment": None,
                "history": []
            }

        # Move current deployment to history (if exists)
        if log_data["current_deployment"]:
            log_data["history"].insert(0, log_data["current_deployment"])

        # Keep only last 10 history entries
        log_data["history"] = log_data["history"][:10]

        # Update current deployment
        log_data["current_deployment"] = record.model_dump()

        # Write log
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

    def get_deployed_artifact(self, client_id: str, profile_id: str) -> str | None:
        """Get currently deployed artifact ID for client/profile.

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier

        Returns:
            Deployed artifact ID, or None if no deployment recorded
        """
        log_path = self._get_log_path(client_id, profile_id)

        if not log_path.exists():
            return None

        with open(log_path) as f:
            log_data = json.load(f)

        current = log_data.get("current_deployment")
        if current:
            return current["artifact_id"]

        return None

    def get_deployment_history(
        self,
        client_id: str,
        profile_id: str,
        limit: int = 10
    ) -> list[DeploymentRecord]:
        """Get deployment history for client/profile.

        Args:
            client_id: Client family identifier
            profile_id: Profile identifier
            limit: Maximum number of history entries to return

        Returns:
            List of deployment records (most recent first)
        """
        log_path = self._get_log_path(client_id, profile_id)

        if not log_path.exists():
            return []

        with open(log_path) as f:
            log_data = json.load(f)

        history = []

        # Add current deployment
        if log_data.get("current_deployment"):
            history.append(DeploymentRecord(**log_data["current_deployment"]))

        # Add historical deployments
        for record_data in log_data.get("history", []):
            history.append(DeploymentRecord(**record_data))

        return history[:limit]
