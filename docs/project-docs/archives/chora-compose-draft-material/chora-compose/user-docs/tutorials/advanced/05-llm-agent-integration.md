# Tutorial: LLM Agent Integration with Chora Compose

**Difficulty:** Advanced
**Duration:** 45 minutes
**Prerequisites:**
- Completion of [MCP Integration Deep Dive](01-mcp-integration-deep-dive.md)
- Understanding of [Agentic Workflows](02-agentic-workflow.md)
- Familiarity with multi-repo ecosystems

**What You'll Learn:**
- How to integrate chora-compose as an LLM agent
- Step-by-step workflow for automated artifact generation
- Integration patterns for ecosystem repos
- Verification and validation workflows

**What You'll Build:**
- An autonomous agent that generates artifacts from configs
- Integration with platform lifecycle gates
- Automated validation and verification workflow

---

## Table of Contents

1. [Setup and Prerequisites](#step-1-setup-and-prerequisites)
2. [Create Your First Agent Workflow](#step-2-create-your-first-agent-workflow)
3. [Implement Config Validation](#step-3-implement-config-validation)
4. [Generate Artifacts](#step-4-generate-artifacts)
5. [Emit Lifecycle Events](#step-5-emit-lifecycle-events)
6. [Complete Integration](#step-6-complete-integration)

---

## Step 1: Setup and Prerequisites

### Install Chora Compose

```bash
# Clone the repository
git clone https://github.com/liminalcommons/chora-compose.git
cd chora-compose

# Install dependencies
poetry install

# Verify installation
poetry run chora-compose --version
```

### Understand the Integration Contract

As an LLM agent, you'll interact with chora-compose through three key interfaces:

1. **Inputs**: Content and artifact configs
2. **Execution**: CLI or Python API
3. **Outputs**: Generated artifacts + run metadata

**Directory structure you'll work with:**
```
your-consumer-repo/
├── configs/
│   ├── content/
│   │   └── weekly-report-intro.json
│   └── artifact/
│       └── weekly-report.json
├── dist/                          # Generated artifacts land here
│   └── latest_run_manifest.json  # Run metadata
└── schemas/                       # For validation
    ├── content/v3.1/schema.json
    └── artifact/v3.1/schema.json
```

---

## Step 2: Create Your First Agent Workflow

### Scenario: Automated Documentation Generation

You're building an agent that generates weekly reports for a platform. When triggered, your agent should:

1. Validate the config exists and is schema-compliant
2. Generate the artifact using chora-compose
3. Store the artifact in the correct location
4. Emit a lifecycle event for platform gates

### Create the Agent Script

Create `scripts/agent_generate.py`:

```python
#!/usr/bin/env python3
"""
Autonomous agent for generating artifacts via chora-compose.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Agent configuration
AGENT_NAME = "weekly-report-generator"
PLATFORM_GATE = "weekly-report-ready"


def log_agent_action(action: str, details: dict[str, Any]) -> None:
    """Log agent actions for observability."""
    print(f"[{AGENT_NAME}] {action}")
    print(json.dumps(details, indent=2))


def validate_prerequisites() -> bool:
    """
    Step 1: Validate that all prerequisites are met.

    Returns:
        True if all checks pass, False otherwise
    """
    log_agent_action("Validating prerequisites", {})

    # Check 1: Config files exist
    content_config = Path("configs/content/weekly-report-intro.json")
    artifact_config = Path("configs/artifact/weekly-report.json")

    if not content_config.exists():
        log_agent_action("Error", {"message": f"Config not found: {content_config}"})
        return False

    if not artifact_config.exists():
        log_agent_action("Error", {"message": f"Config not found: {artifact_config}"})
        return False

    log_agent_action("Prerequisites validated", {
        "content_config": str(content_config),
        "artifact_config": str(artifact_config)
    })

    return True


def main() -> int:
    """Main agent workflow."""
    print(f"=== {AGENT_NAME} Starting ===\n")

    # Step 1: Prerequisites
    if not validate_prerequisites():
        return 1

    print(f"\n=== {AGENT_NAME} Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Run it:**
```bash
python scripts/agent_generate.py
```

**Expected output:**
```
=== weekly-report-generator Starting ===

[weekly-report-generator] Validating prerequisites
{}
[weekly-report-generator] Prerequisites validated
{
  "content_config": "configs/content/weekly-report-intro.json",
  "artifact_config": "configs/artifact/weekly-report.json"
}

=== weekly-report-generator Complete ===
```

---

## Step 3: Implement Config Validation

### Add Schema Validation

Extend your agent to validate configs against JSON schemas:

```python
import subprocess


def validate_config(config_path: Path) -> tuple[bool, str]:
    """
    Step 2: Validate config against schema.

    Args:
        config_path: Path to config file

    Returns:
        (success, message) tuple
    """
    log_agent_action("Validating config", {"path": str(config_path)})

    try:
        # Use chora-compose CLI for validation
        result = subprocess.run(
            ["poetry", "run", "chora-compose", "validate", str(config_path)],
            capture_output=True,
            text=True,
            check=True
        )

        log_agent_action("Validation passed", {
            "config": str(config_path),
            "output": result.stdout.strip()
        })
        return True, result.stdout

    except subprocess.CalledProcessError as e:
        log_agent_action("Validation failed", {
            "config": str(config_path),
            "error": e.stderr
        })
        return False, e.stderr


def main() -> int:
    """Main agent workflow."""
    print(f"=== {AGENT_NAME} Starting ===\n")

    # Step 1: Prerequisites
    if not validate_prerequisites():
        return 1

    # Step 2: Validate configs
    content_config = Path("configs/content/weekly-report-intro.json")
    artifact_config = Path("configs/artifact/weekly-report.json")

    success, message = validate_config(content_config)
    if not success:
        return 1

    success, message = validate_config(artifact_config)
    if not success:
        return 1

    print(f"\n=== {AGENT_NAME} Complete ===")
    return 0
```

**What this does:**
- Uses chora-compose's built-in validation
- Checks configs against JSON schemas
- Logs validation results for observability
- Fails fast if validation fails

---

## Step 4: Generate Artifacts

### Add Artifact Generation

Now add the core functionality - generating artifacts:

```python
from datetime import datetime


def generate_artifact(artifact_config_path: Path) -> tuple[bool, dict[str, Any]]:
    """
    Step 3: Generate artifact using chora-compose.

    Args:
        artifact_config_path: Path to artifact config

    Returns:
        (success, metadata) tuple
    """
    log_agent_action("Generating artifact", {"config": str(artifact_config_path)})

    start_time = datetime.now()

    try:
        # Execute chora-compose
        result = subprocess.run(
            ["poetry", "run", "chora-compose", "compose", str(artifact_config_path)],
            capture_output=True,
            text=True,
            check=True
        )

        duration = (datetime.now() - start_time).total_seconds()

        metadata = {
            "status": "success",
            "duration_seconds": duration,
            "output": result.stdout.strip(),
            "timestamp": datetime.now().isoformat()
        }

        log_agent_action("Generation complete", metadata)
        return True, metadata

    except subprocess.CalledProcessError as e:
        duration = (datetime.now() - start_time).total_seconds()

        metadata = {
            "status": "failed",
            "duration_seconds": duration,
            "error": e.stderr,
            "timestamp": datetime.now().isoformat()
        }

        log_agent_action("Generation failed", metadata)
        return False, metadata


def main() -> int:
    """Main agent workflow."""
    print(f"=== {AGENT_NAME} Starting ===\n")

    # Step 1: Prerequisites
    if not validate_prerequisites():
        return 1

    # Step 2: Validate configs
    content_config = Path("configs/content/weekly-report-intro.json")
    artifact_config = Path("configs/artifact/weekly-report.json")

    success, message = validate_config(content_config)
    if not success:
        return 1

    success, message = validate_config(artifact_config)
    if not success:
        return 1

    # Step 3: Generate artifact
    success, metadata = generate_artifact(artifact_config)
    if not success:
        return 1

    print(f"\n=== {AGENT_NAME} Complete ===")
    return 0
```

---

## Step 5: Emit Lifecycle Events

### Add Platform Integration

Integrate with platform lifecycle gates:

```python
def emit_lifecycle_event(gate_id: str, metadata: dict[str, Any]) -> bool:
    """
    Step 4: Emit lifecycle event for platform gates.

    Args:
        gate_id: Platform gate identifier
        metadata: Run metadata

    Returns:
        True if event emitted successfully
    """
    log_agent_action("Emitting lifecycle event", {
        "gate_id": gate_id,
        "metadata_keys": list(metadata.keys())
    })

    # Read manifest from chora-compose output
    manifest_path = Path("dist/latest_run_manifest.json")

    if not manifest_path.exists():
        log_agent_action("Warning", {
            "message": "Manifest not found, creating minimal event"
        })
        manifest_data = {}
    else:
        with open(manifest_path) as f:
            manifest_data = json.load(f)

    # Create lifecycle event payload
    event = {
        "gate_id": gate_id,
        "agent": AGENT_NAME,
        "timestamp": datetime.now().isoformat(),
        "status": metadata.get("status", "unknown"),
        "manifest": manifest_data,
        "metadata": metadata
    }

    # Write to platform event stream (example: append to JSONL)
    events_file = Path("var/lifecycle_events.jsonl")
    events_file.parent.mkdir(parents=True, exist_ok=True)

    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    log_agent_action("Lifecycle event emitted", {
        "gate_id": gate_id,
        "events_file": str(events_file)
    })

    return True


def main() -> int:
    """Main agent workflow."""
    print(f"=== {AGENT_NAME} Starting ===\n")

    # Step 1: Prerequisites
    if not validate_prerequisites():
        return 1

    # Step 2: Validate configs
    content_config = Path("configs/content/weekly-report-intro.json")
    artifact_config = Path("configs/artifact/weekly-report.json")

    success, message = validate_config(content_config)
    if not success:
        return 1

    success, message = validate_config(artifact_config)
    if not success:
        return 1

    # Step 3: Generate artifact
    success, metadata = generate_artifact(artifact_config)
    if not success:
        return 1

    # Step 4: Emit lifecycle event
    emit_lifecycle_event(PLATFORM_GATE, metadata)

    print(f"\n=== {AGENT_NAME} Complete ===")
    return 0
```

---

## Step 6: Complete Integration

### Add Error Handling and Retries

Complete the integration with production-grade error handling:

```python
import time
from typing import Optional


def retry_with_backoff(
    func: callable,
    max_retries: int = 3,
    base_delay: float = 1.0
) -> tuple[bool, Any]:
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        base_delay: Base delay in seconds

    Returns:
        (success, result) tuple
    """
    for attempt in range(max_retries):
        try:
            result = func()
            return True, result
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                log_agent_action("Retry scheduled", {
                    "attempt": attempt + 1,
                    "max_retries": max_retries,
                    "delay_seconds": delay,
                    "error": str(e)
                })
                time.sleep(delay)
            else:
                log_agent_action("Max retries exceeded", {
                    "attempts": max_retries,
                    "error": str(e)
                })
                return False, str(e)


def verify_artifact_output(metadata: dict[str, Any]) -> bool:
    """
    Step 5: Verify artifact was generated correctly.

    Args:
        metadata: Generation metadata

    Returns:
        True if verification passes
    """
    log_agent_action("Verifying artifact output", {})

    # Check manifest exists
    manifest_path = Path("dist/latest_run_manifest.json")
    if not manifest_path.exists():
        log_agent_action("Verification failed", {
            "reason": "Manifest not found"
        })
        return False

    # Parse manifest
    with open(manifest_path) as f:
        manifest = json.load(f)

    # Verify artifact files exist
    if "artifacts" in manifest:
        for artifact_path in manifest["artifacts"]:
            if not Path(artifact_path).exists():
                log_agent_action("Verification failed", {
                    "reason": "Artifact file not found",
                    "path": artifact_path
                })
                return False

    log_agent_action("Verification passed", {
        "manifest_path": str(manifest_path),
        "artifacts_count": len(manifest.get("artifacts", []))
    })

    return True


def cleanup_on_failure() -> None:
    """Clean up partial artifacts on failure."""
    log_agent_action("Cleaning up failed run", {})

    # Remove partial artifacts
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.glob("*.partial"):
            file.unlink()
            log_agent_action("Removed partial file", {"path": str(file)})


def main() -> int:
    """Main agent workflow with complete error handling."""
    print(f"=== {AGENT_NAME} Starting ===\n")

    try:
        # Step 1: Prerequisites
        if not validate_prerequisites():
            return 1

        # Step 2: Validate configs
        content_config = Path("configs/content/weekly-report-intro.json")
        artifact_config = Path("configs/artifact/weekly-report.json")

        success, message = validate_config(content_config)
        if not success:
            return 1

        success, message = validate_config(artifact_config)
        if not success:
            return 1

        # Step 3: Generate artifact (with retries)
        success, metadata = retry_with_backoff(
            lambda: generate_artifact(artifact_config),
            max_retries=3
        )

        if not success:
            cleanup_on_failure()
            return 1

        # Step 4: Verify output
        if not verify_artifact_output(metadata):
            cleanup_on_failure()
            return 1

        # Step 5: Emit lifecycle event
        emit_lifecycle_event(PLATFORM_GATE, metadata)

        print(f"\n=== {AGENT_NAME} Complete ===")
        return 0

    except Exception as e:
        log_agent_action("Fatal error", {"error": str(e)})
        cleanup_on_failure()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Testing Your Integration

### Create a Test Config

Create `configs/content/weekly-report-intro.json`:

```json
{
  "content_id": "weekly-report-intro",
  "format": "markdown",
  "generation": {
    "patterns": [
      {
        "type": "jinja2",
        "template_string": "# Weekly Report\n\nGenerated: {{ timestamp }}\n\n## Summary\n{{ summary }}"
      }
    ]
  },
  "metadata": {
    "description": "Weekly report introduction",
    "version": "1.0.0"
  }
}
```

### Run the Agent

```bash
# Make executable
chmod +x scripts/agent_generate.py

# Run
python scripts/agent_generate.py
```

**Expected workflow:**
1. ✅ Validates prerequisites
2. ✅ Validates configs against schemas
3. ✅ Generates artifact using chora-compose
4. ✅ Verifies output exists
5. ✅ Emits lifecycle event

---

## Next Steps

You've successfully built an autonomous LLM agent that integrates with chora-compose! Now you can:

1. **Expand to Multiple Artifacts**: Modify the agent to handle multiple configs
2. **Add Scheduling**: Integrate with cron or orchestration platforms
3. **Enhance Observability**: Add structured logging and metrics
4. **Implement Advanced Patterns**: See [Agent Integration Playbook](../../explanation/ecosystem/agent-integration-playbook.md)

## Related Documentation

- [Agent Integration Playbook](../../explanation/ecosystem/agent-integration-playbook.md) - Concepts and patterns
- [MCP Integration Deep Dive](01-mcp-integration-deep-dive.md) - MCP protocol details
- [Agentic Workflow](02-agentic-workflow.md) - End-to-end workflows
- [How to Generate Content](../../how-to/generation/generate-content.md) - Generation basics
- [Validate Configs](../../how-to/configs/validate-configs.md) - Validation details
