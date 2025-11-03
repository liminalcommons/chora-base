#!/usr/bin/env python3
"""
Post-processing wrapper for chora-compose generated artifacts.

This script implements the 4-step pipeline:
1. Validate against JSON schema
2. Allocate request_id from sequence file
3. Emit event to events.jsonl
4. Promote file from draft/ to inbox/incoming/

Usage:
    python scripts/process-generated-artifact.py <draft_file_path>
    python scripts/process-generated-artifact.py inbox/draft/coordination-request.json

Exit codes:
    0: Success
    1: Validation error
    2: File system error
    3: Configuration error
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema package required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(3)


class ArtifactProcessor:
    """Processes draft artifacts through validation and promotion pipeline."""

    def __init__(self, draft_path: Path, verbose: bool = False):
        self.draft_path = draft_path
        self.verbose = verbose
        self.errors = []

        # Repository root
        self.repo_root = Path(__file__).parent.parent

        # Configuration paths
        self.schema_dir = self.repo_root / "schemas"
        self.sequence_dir = self.repo_root / "inbox"
        self.events_file = self.repo_root / "inbox" / "coordination" / "events.jsonl"
        self.error_log = draft_path.parent / "errors.log"

    def log(self, message: str) -> None:
        """Log message if verbose mode enabled."""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def log_error(self, error: str) -> None:
        """Log error to both stderr and error log file."""
        timestamp = datetime.now().isoformat()
        error_entry = f"[{timestamp}] {error}\n"

        print(f"ERROR: {error}", file=sys.stderr)
        self.errors.append(error)

        # Append to error log
        try:
            with open(self.error_log, 'a') as f:
                f.write(error_entry)
        except Exception as e:
            print(f"Warning: Could not write to error log: {e}", file=sys.stderr)

    def validate_schema(self, artifact: Dict[str, Any], schema_path: Path) -> bool:
        """
        Validate artifact against JSON schema.

        Args:
            artifact: Artifact data to validate
            schema_path: Path to JSON schema file

        Returns:
            True if validation passes, False otherwise
        """
        self.log(f"Validating against schema: {schema_path}")

        if not schema_path.exists():
            self.log_error(f"Schema file not found: {schema_path}")
            return False

        try:
            with open(schema_path) as f:
                schema = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in schema file: {e}")
            return False

        try:
            validator = Draft7Validator(schema)
            errors = list(validator.iter_errors(artifact))

            if errors:
                self.log_error("Schema validation failed:")
                for error in errors:
                    path = ".".join(str(p) for p in error.path) if error.path else "root"
                    self.log_error(f"  - {path}: {error.message}")
                return False

            self.log("✓ Schema validation passed")
            return True

        except jsonschema.exceptions.SchemaError as e:
            self.log_error(f"Invalid schema: {e}")
            return False

    def allocate_request_id(self, artifact_type: str) -> Optional[str]:
        """
        Allocate next request_id from sequence file.

        Args:
            artifact_type: Type of artifact ('coordination', 'task', 'proposal')

        Returns:
            Allocated request_id (e.g., 'COORD-2025-003') or None if error
        """
        sequence_file = self.sequence_dir / f".sequence-{artifact_type}"
        self.log(f"Allocating ID from sequence: {sequence_file}")

        # Ensure sequence file exists
        if not sequence_file.exists():
            self.log(f"Creating new sequence file: {sequence_file}")
            sequence_file.write_text("0\n")

        try:
            # Read current sequence
            current_seq = int(sequence_file.read_text().strip())
            next_seq = current_seq + 1

            # Write updated sequence
            sequence_file.write_text(f"{next_seq}\n")

            # Generate request_id
            year = datetime.now().year
            prefix_map = {
                'coordination': 'COORD',
                'task': 'TASK',
                'proposal': 'PROP'
            }
            prefix = prefix_map.get(artifact_type, 'REQ')
            request_id = f"{prefix}-{year}-{next_seq:03d}"

            self.log(f"✓ Allocated request_id: {request_id}")
            return request_id

        except (ValueError, IOError) as e:
            self.log_error(f"Failed to allocate request_id: {e}")
            return None

    def emit_event(self, artifact: Dict[str, Any], event_type: str) -> bool:
        """
        Emit event to events.jsonl.

        Args:
            artifact: Artifact data
            event_type: Type of event (e.g., 'coordination_request_created')

        Returns:
            True if event emitted successfully, False otherwise
        """
        self.log(f"Emitting event: {event_type}")

        # Ensure events directory exists
        self.events_file.parent.mkdir(parents=True, exist_ok=True)

        # Build event
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "request_id": artifact.get("request_id"),
            "trace_id": artifact.get("trace_id"),
            "from_repo": artifact.get("from_repo"),
            "to_repo": artifact.get("to_repo"),
            "priority": artifact.get("priority"),
            "urgency": artifact.get("urgency")
        }

        try:
            # Append to events.jsonl
            with open(self.events_file, 'a') as f:
                f.write(json.dumps(event) + '\n')

            self.log(f"✓ Event emitted to {self.events_file}")
            return True

        except IOError as e:
            self.log_error(f"Failed to emit event: {e}")
            return False

    def promote_file(self, artifact: Dict[str, Any], target_dir: Path, cleanup_draft: bool = True) -> bool:
        """
        Promote file from draft/ to target directory.

        Args:
            artifact: Artifact data
            target_dir: Target directory (e.g., inbox/incoming/coordination/)
            cleanup_draft: Whether to delete draft file after promotion

        Returns:
            True if promotion successful, False otherwise
        """
        request_id = artifact.get("request_id")
        if not request_id:
            self.log_error("Cannot promote file: request_id missing")
            return False

        target_path = target_dir / f"{request_id}.json"
        self.log(f"Promoting to: {target_path}")

        # Ensure target directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Write artifact to target location
            with open(target_path, 'w') as f:
                json.dump(artifact, f, indent=2, ensure_ascii=False)
                f.write('\n')

            self.log(f"✓ File promoted to {target_path}")

            # Clean up draft if requested
            if cleanup_draft:
                self.draft_path.unlink()
                self.log(f"✓ Draft file cleaned up: {self.draft_path}")

            return True

        except IOError as e:
            self.log_error(f"Failed to promote file: {e}")
            return False

    def process(self) -> int:
        """
        Run full processing pipeline.

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        self.log(f"Processing artifact: {self.draft_path}")

        # Step 0: Load draft artifact
        if not self.draft_path.exists():
            self.log_error(f"Draft file not found: {self.draft_path}")
            return 2

        try:
            with open(self.draft_path) as f:
                artifact = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in draft file: {e}")
            return 2

        artifact_type = artifact.get("type")
        if not artifact_type:
            self.log_error("Artifact missing required 'type' field")
            return 1

        # Step 1: Allocate request_id FIRST (before schema validation)
        # This is needed because schema requires valid request_id pattern
        current_id = artifact.get("request_id")
        if current_id == "PENDING" or not current_id:
            request_id = self.allocate_request_id(artifact_type)
            if not request_id:
                return 2
            artifact["request_id"] = request_id
            self.log(f"Allocated request_id: {request_id}")
        else:
            # ID already set, validate it
            self.log(f"Using existing request_id: {current_id}")

        # Step 2: Validate schema (now with valid request_id)
        schema_path = self.schema_dir / f"{artifact_type}-request.json"
        if not self.validate_schema(artifact, schema_path):
            return 1

        # Step 3: Emit event
        event_type = f"{artifact_type}_request_created"
        if not self.emit_event(artifact, event_type):
            return 2

        # Step 4: Promote file
        target_dir = self.repo_root / "inbox" / "incoming" / artifact_type
        if not self.promote_file(artifact, target_dir, cleanup_draft=True):
            return 2

        final_id = artifact["request_id"]
        self.log(f"\n✓ Processing complete! Artifact: {target_dir / f'{final_id}.json'}")
        return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Post-process chora-compose generated artifacts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/process-generated-artifact.py inbox/draft/coordination-request.json
  python scripts/process-generated-artifact.py inbox/draft/coordination-request.json --verbose
        """
    )
    parser.add_argument(
        "draft_file",
        type=Path,
        help="Path to draft artifact JSON file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    processor = ArtifactProcessor(args.draft_file, verbose=args.verbose)
    return processor.process()


if __name__ == "__main__":
    sys.exit(main())
