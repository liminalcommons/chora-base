#!/usr/bin/env python3
"""
Ecosystem Onboarding Installer - One-command inbox protocol setup

Installs SAP-001 Inbox Coordination Protocol into any repository with:
- Directory structure (incoming/, active/, completed/, etc.)
- Generator scripts and content configs
- Capability registry template
- Agent automation playbook
- Event log initialization
- Ecosystem registration

Usage:
    # Full installation (recommended)
    python scripts/install-inbox-protocol.py \\
        --repo github.com/liminalcommons/mcp-orchestration \\
        --mode full

    # Minimal installation (protocol only, no tooling)
    python scripts/install-inbox-protocol.py \\
        --repo github.com/liminalcommons/target-repo \\
        --mode minimal

    # Interactive mode (prompts for configuration)
    python scripts/install-inbox-protocol.py --interactive
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import date, datetime
from typing import Dict, List, Optional, Any

# Version tracking
INSTALLER_VERSION = "1.0.0"
PROTOCOL_VERSION = "1.1.0"


class InboxInstaller:
    """Installs SAP-001 inbox protocol into a target repository."""

    def __init__(
        self,
        target_repo: str,
        target_path: Path,
        mode: str = "full",
        capabilities: Optional[List[str]] = None,
        contact_email: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize installer.

        Args:
            target_repo: Repository identifier (e.g., github.com/org/repo)
            target_path: Local path to target repository
            mode: Installation mode (full, minimal, generator-only)
            capabilities: List of capabilities repo provides
            contact_email: Contact email for ecosystem registry
            verbose: Verbose logging
        """
        self.target_repo = target_repo
        self.target_path = target_path
        self.mode = mode
        self.capabilities = capabilities or []
        self.contact_email = contact_email
        self.verbose = verbose

        # Detect source (chora-base) location
        self.source_path = Path(__file__).parent.parent

    def log(self, message: str, level: str = "info"):
        """Log message if verbose or if level is warning/error."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "info": "✓",
            "warn": "⚠️",
            "error": "✗",
            "step": "→"
        }.get(level, "•")

        if self.verbose or level in ["warn", "error"]:
            print(f"[{timestamp}] {prefix} {message}")

    def install(self) -> bool:
        """
        Execute installation.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.log(f"Installing SAP-001 Inbox Protocol v{PROTOCOL_VERSION}", "step")
            self.log(f"Target: {self.target_repo}")
            self.log(f"Mode: {self.mode}")
            self.log(f"Path: {self.target_path}")
            print()

            # Phase 1: Validate target
            self.log("Phase 1: Validating target repository...", "step")
            if not self._validate_target():
                return False

            # Phase 2: Create directory structure
            self.log("Phase 2: Creating inbox directory structure...", "step")
            if not self._create_directories():
                return False

            # Phase 3: Install generator tools (full mode only)
            if self.mode in ["full", "generator-only"]:
                self.log("Phase 3: Installing generator tools...", "step")
                if not self._install_generator():
                    return False
            else:
                self.log("Phase 3: Skipping generator installation (minimal mode)", "step")

            # Phase 4: Create capability registry
            self.log("Phase 4: Creating capability registry...", "step")
            if not self._create_capability_registry():
                return False

            # Phase 5: Setup agent automation
            if self.mode == "full":
                self.log("Phase 5: Setting up agent automation...", "step")
                if not self._setup_agent_automation():
                    return False
            else:
                self.log("Phase 5: Skipping agent automation (not full mode)", "step")

            # Phase 6: Initialize event log
            self.log("Phase 6: Initializing event log...", "step")
            if not self._initialize_event_log():
                return False

            # Phase 7: Register in ecosystem
            self.log("Phase 7: Registering in ecosystem...", "step")
            if not self._register_ecosystem():
                return False

            # Phase 8: Generate completion report
            self.log("Phase 8: Generating installation report...", "step")
            self._generate_report()

            print()
            self.log(f"✓ Installation complete! SAP-001 v{PROTOCOL_VERSION} ready.", "info")
            print()
            self._print_next_steps()

            return True

        except Exception as e:
            self.log(f"Installation failed: {e}", "error")
            if self.verbose:
                import traceback

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

                traceback.print_exc()
            return False

    def _validate_target(self) -> bool:
        """Validate target repository exists and is accessible."""
        # Check target path exists
        if not self.target_path.exists():
            self.log(f"Target path does not exist: {self.target_path}", "error")
            return False

        # Check it's a git repository
        if not (self.target_path / ".git").exists():
            self.log(f"Target is not a git repository: {self.target_path}", "warn")
            response = input("Continue anyway? [y/N]: ")
            if response.lower() != 'y':
                return False

        # Check inbox doesn't already exist
        inbox_path = self.target_path / "inbox"
        if inbox_path.exists():
            self.log("Inbox directory already exists", "warn")
            response = input("Overwrite existing installation? [y/N]: ")
            if response.lower() != 'y':
                return False
            self.log("Removing existing inbox directory...")
            shutil.rmtree(inbox_path)

        self.log(f"Target validated: {self.target_path}")
        return True

    def _create_directories(self) -> bool:
        """Create inbox directory structure."""
        inbox_root = self.target_path / "inbox"

        # Core directories
        directories = [
            "incoming/coordination",
            "incoming/tasks",
            "incoming/proposals",
            "active",
            "completed",
            "draft",
            "ecosystem",
            "coordination",
            "content-blocks",
        ]

        for dir_path in directories:
            full_path = inbox_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.log(f"Created: inbox/{dir_path}")

        # Create .gitkeep files for empty directories
        for dir_path in ["draft", "active", "completed"]:
            gitkeep = inbox_root / dir_path / ".gitkeep"
            gitkeep.touch()

        # Create sequence files
        (inbox_root / ".sequence-coordination").write_text("000\n")
        (inbox_root / ".sequence-task").write_text("000\n")
        (inbox_root / ".sequence-proposal").write_text("000\n")

        self.log(f"✓ Created {len(directories)} directories")
        return True

    def _install_generator(self) -> bool:
        """Install coordination request generator and content configs."""
        # Copy generator package
        source_generator = self.source_path / "scripts" / "inbox_generator"
        target_generator = self.target_path / "scripts" / "inbox_generator"

        if source_generator.exists():
            shutil.copytree(source_generator, target_generator, dirs_exist_ok=True)
            self.log(f"Copied generator package: scripts/inbox_generator/")
        else:
            self.log("Generator package not found in source", "warn")
            return False

        # Copy CLI script
        source_cli = self.source_path / "scripts" / "generate-coordination-request.py"
        target_cli = self.target_path / "scripts" / "generate-coordination-request.py"

        if source_cli.exists():
            shutil.copy2(source_cli, target_cli)
            target_cli.chmod(0o755)
            self.log("Copied CLI tool: scripts/generate-coordination-request.py")
        else:
            self.log("CLI script not found in source", "warn")
            return False

        # Copy content blocks
        source_blocks = self.source_path / "inbox" / "content-blocks"
        target_blocks = self.target_path / "inbox" / "content-blocks"

        if source_blocks.exists():
            # Copy all content block configs
            for config_file in source_blocks.glob("content-block-*.json"):
                shutil.copy2(config_file, target_blocks / config_file.name)
                self.log(f"Copied: inbox/content-blocks/{config_file.name}")

            # Copy artifact config
            artifact_config = source_blocks / "coordination-request-artifact.json"
            if artifact_config.exists():
                shutil.copy2(artifact_config, target_blocks / artifact_config.name)
                self.log("Copied: inbox/content-blocks/coordination-request-artifact.json")

            self.log(f"✓ Installed generator with {len(list((target_blocks).glob('*.json')))} configs")
        else:
            self.log("Content blocks not found in source", "warn")
            return False

        return True

    def _create_capability_registry(self) -> bool:
        """Create capability registry template for this repository."""
        # Extract repo name from URL
        repo_parts = self.target_repo.split("/")
        repo_name = repo_parts[-1] if repo_parts else "unknown"

        capability_file = self.target_path / "inbox" / "coordination" / f"CAPABILITIES_{repo_name}.yaml"

        # Default capabilities based on mode
        if not self.capabilities:
            self.capabilities = ["coordination_requests"]  # All repos can receive coordination

        capability_content = f"""# Capability Registry for {self.target_repo}
# Auto-generated by install-inbox-protocol.py v{INSTALLER_VERSION}
# Last updated: {date.today().isoformat()}

repository:
  name: {repo_name}
  github_url: {self.target_repo}
  inbox_protocol_version: "{PROTOCOL_VERSION}"
  installed: "{date.today().isoformat()}"

capabilities:
  can_provide:
{chr(10).join(f'    - {cap}' for cap in self.capabilities) if self.capabilities else '    # Add capabilities this repo provides'}

  can_receive:
    - coordination_requests  # All repos with inbox can receive coordination
    - tasks                  # Implementation tasks
    # - proposals            # Strategic proposals (uncomment if applicable)

contacts:
  primary: {self.contact_email or "# Add primary contact email"}
  team:
    # Add team member emails or GitHub handles

response_sla:
  acknowledgment: "1 business day"
  full_response: "Depends on urgency and complexity"
  escalation_channel: "# GitHub issues, Slack, email"

status:
  active: true
  availability: "business_hours"  # business_hours, 24x7, maintenance
  health: "healthy"               # healthy, degraded, unavailable

metadata:
  installation_mode: "{self.mode}"
  installer_version: "{INSTALLER_VERSION}"
  auto_generated: true
"""

        capability_file.write_text(capability_content)
        self.log(f"Created capability registry: {capability_file.relative_to(self.target_path)}")
        return True

    def _setup_agent_automation(self) -> bool:
        """Setup agent automation playbook and AGENTS.md."""
        # Create AGENTS.md if it doesn't exist
        agents_file = self.target_path / "inbox" / "AGENTS.md"

        agents_content = f"""# Agent Automation Playbook - Inbox Protocol

**Version**: {PROTOCOL_VERSION}
**Repository**: {self.target_repo}
**Installed**: {date.today().isoformat()}

## Overview

This repository uses SAP-001 Inbox Coordination Protocol for cross-repository communication.
AI agents are configured to automatically monitor and process coordination items.

## Agent Responsibilities

### 1. Inbox Monitoring (Every Session Start)

**Command**: Check for new items
```bash
python scripts/inbox-query.py --incoming --unacknowledged
```

**Actions**:
- Read new coordination requests, tasks, proposals
- Acknowledge receipt within 1 business day
- Escalate urgent/blocking items immediately

### 2. Coordination Request Processing

**Command**: View specific request
```bash
python scripts/inbox-query.py --request COORD-YYYY-NNN
```

**Workflow**:
1. Read deliverables and acceptance criteria
2. Assess feasibility and effort
3. Respond using: `python scripts/respond-to-coordination.py`
4. Move to `active/` if accepted, `completed/` if declined

### 3. Status Updates

**Command**: Update coordination status
```bash
python scripts/update-coordination-status.py \\
    --request COORD-YYYY-NNN \\
    --status in_progress \\
    --notes "Started implementation, ETA 3 days"
```

### 4. Event Logging

All actions are logged to `inbox/coordination/events.jsonl`:
- Request received
- Acknowledgment sent
- Status changes
- Completion events

## SLA Commitments

- **Acknowledgment**: Within 1 business day
- **Full Response**: Depends on urgency (blocks_sprint: same day, next_sprint: 3 days, backlog: 1 week)
- **Escalation**: Immediate for blocking items

## Automation Tools

This installation includes:
- `scripts/inbox-query.py` - Query inbox items
- `scripts/respond-to-coordination.py` - Generate responses
- `scripts/generate-coordination-request.py` - Create new requests
- `scripts/update-coordination-status.py` - Update status (if available)

## Ecosystem Integration

This repository is registered in the chora-base ecosystem:
- **Capability Registry**: `inbox/coordination/CAPABILITIES_{repo_name}.yaml`
- **Ecosystem Dashboard**: Visible in chora-base ECOSYSTEM_STATUS.yaml
- **Weekly Broadcasts**: Receive updates every Sunday

## Questions?

See: `docs/skilled-awareness/inbox/` for detailed protocol documentation
"""

        agents_file.write_text(agents_content)
        self.log(f"Created agent playbook: {agents_file.relative_to(self.target_path)}")
        return True

    def _initialize_event_log(self) -> bool:
        """Initialize event log with installation event."""
        event_log = self.target_path / "inbox" / "coordination" / "events.jsonl"

        # Create installation event
        installation_event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "protocol_installed",
            "repo": self.target_repo,
            "protocol_version": PROTOCOL_VERSION,
            "installer_version": INSTALLER_VERSION,
            "mode": self.mode,
            "capabilities": self.capabilities,
            "trace_id": f"inbox-protocol-install-{date.today().year}"
        }

        with open(event_log, 'w', encoding='utf-8') as f:
            f.write(json.dumps(installation_event) + "\n")

        self.log(f"Initialized event log with installation event")
        return True

    def _register_ecosystem(self) -> bool:
        """Register this repository in chora-base ecosystem registry."""
        # This will be implemented when we build the central registry
        # For now, just create a placeholder registration request

        ecosystem_registration = self.target_path / "inbox" / "ecosystem" / "REGISTRATION.json"

        registration_data = {
            "repository": self.target_repo,
            "registered": date.today().isoformat(),
            "protocol_version": PROTOCOL_VERSION,
            "capabilities": self.capabilities,
            "contact": self.contact_email,
            "status": "pending_approval",
            "notes": "Auto-registered during inbox protocol installation"
        }

        with open(ecosystem_registration, 'w', encoding='utf-8') as f:
            json.dump(registration_data, f, indent=2)

        self.log("Created ecosystem registration request")
        self.log("NOTE: Registration will be processed by chora-base ecosystem coordinator", "warn")
        return True

    def _generate_report(self):
        """Generate installation report."""
        report_file = self.target_path / "inbox" / "INSTALLATION_REPORT.md"

        report_content = f"""# SAP-001 Inbox Protocol Installation Report

**Repository**: {self.target_repo}
**Installation Date**: {date.today().isoformat()}
**Protocol Version**: {PROTOCOL_VERSION}
**Installer Version**: {INSTALLER_VERSION}
**Mode**: {self.mode}

## Installation Summary

✅ **Directory Structure**: Created 9 inbox directories
✅ **Generator Tools**: {'Installed' if self.mode in ['full', 'generator-only'] else 'Skipped (minimal mode)'}
✅ **Capability Registry**: Created with {len(self.capabilities)} capabilities
✅ **Agent Automation**: {'Configured' if self.mode == 'full' else 'Skipped'}
✅ **Event Log**: Initialized
✅ **Ecosystem Registration**: Submitted

## Capabilities Registered

{chr(10).join(f'- {cap}' for cap in self.capabilities) if self.capabilities else 'None specified'}

## Next Steps

1. **Review Configuration**:
   - Edit `inbox/coordination/CAPABILITIES_*.yaml` to add/update capabilities
   - Add contact information and team members

2. **Test Generator** (if installed):
   ```bash
   python scripts/generate-coordination-request.py --interactive
   ```

3. **Configure Agent Automation**:
   - Review `inbox/AGENTS.md` for agent responsibilities
   - Set up notification webhooks (optional)

4. **Submit Ecosystem Registration**:
   - Create PR to chora-base adding your capability registry
   - Wait for ecosystem coordinator approval

5. **Start Coordinating**:
   - Monitor `inbox/incoming/coordination/` for new requests
   - Create coordination requests with generator
   - Participate in weekly ecosystem broadcasts

## Resources

- **Protocol Spec**: https://github.com/liminalcommons/chora-base/docs/skilled-awareness/inbox/protocol-spec.md
- **Agent Guide**: https://github.com/liminalcommons/chora-base/docs/skilled-awareness/inbox/awareness-guide.md
- **Generator Usage**: {self.target_path}/docs/inbox-generator-usage.md (if copied)

## Installation Files

```
{self.target_repo}/
├── inbox/
│   ├── incoming/coordination/     # New coordination requests arrive here
│   ├── incoming/tasks/            # Implementation tasks
│   ├── incoming/proposals/        # Strategic proposals
│   ├── active/                    # Work in progress
│   ├── completed/                 # Archived items
│   ├── draft/                     # Draft coordination items
│   ├── ecosystem/                 # Ecosystem coordination
│   ├── coordination/              # Event logs and capabilities
│   ├── content-blocks/            # Generator configs (if installed)
│   ├── AGENTS.md                  # Agent playbook
│   └── INSTALLATION_REPORT.md     # This file
├── scripts/
│   ├── inbox_generator/           # Generator package (if installed)
│   ├── generate-coordination-request.py  # CLI tool (if installed)
│   └── install-inbox-protocol.py  # This installer (copy)
└── schemas/                       # JSON schemas (if copied)
```

---

**Installed by**: install-inbox-protocol.py v{INSTALLER_VERSION}
**Support**: https://github.com/liminalcommons/chora-base/issues
"""

        report_file.write_text(report_content)
        self.log(f"Generated installation report: {report_file.relative_to(self.target_path)}")

    def _print_next_steps(self):
        """Print next steps for user."""
        print("📋 Next Steps:")
        print()
        print("1. Review capability registry:")
        print(f"   vim {self.target_path}/inbox/coordination/CAPABILITIES_*.yaml")
        print()
        if self.mode in ["full", "generator-only"]:
            print("2. Test the generator:")
            print(f"   cd {self.target_path}")
            print("   python scripts/generate-coordination-request.py --interactive")
            print()
        print(f"{'3' if self.mode in ['full', 'generator-only'] else '2'}. Review installation report:")
        print(f"   cat {self.target_path}/inbox/INSTALLATION_REPORT.md")
        print()
        print(f"{'4' if self.mode in ['full', 'generator-only'] else '3'}. Submit ecosystem registration (create PR to chora-base)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Install SAP-001 Inbox Coordination Protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Input modes
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--repo',
        help='Target repository (e.g., github.com/liminalcommons/mcp-orchestration)'
    )
    input_group.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode (prompts for configuration)'
    )

    # Configuration
    parser.add_argument(
        '--path',
        type=Path,
        help='Local path to target repository (defaults to ../REPO_NAME)'
    )
    parser.add_argument(
        '--mode',
        choices=['full', 'minimal', 'generator-only'],
        default='full',
        help='Installation mode (default: full)'
    )
    parser.add_argument(
        '--capabilities',
        nargs='+',
        help='Capabilities this repo provides (space-separated)'
    )
    parser.add_argument(
        '--contact',
        help='Contact email for ecosystem registry'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose logging'
    )

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        print("=== Interactive Inbox Protocol Installation ===\n")
        args.repo = input("Repository (e.g., github.com/liminalcommons/mcp-orchestration): ")
        args.mode = input("Mode [full/minimal/generator-only] (default: full): ") or "full"

        repo_name = args.repo.split("/")[-1]
        default_path = Path.cwd().parent / repo_name
        path_input = input(f"Local path (default: {default_path}): ")
        args.path = Path(path_input) if path_input else default_path

        caps_input = input("Capabilities (comma-separated, optional): ")
        args.capabilities = [c.strip() for c in caps_input.split(",")] if caps_input else []

        args.contact = input("Contact email (optional): ")
        args.verbose = True

    # Determine target path
    if not args.path:
        repo_name = args.repo.split("/")[-1]
        args.path = Path.cwd().parent / repo_name

    # Validate repo format
    if not args.repo.startswith("github.com/"):
        print(f"ERROR: Repository must start with 'github.com/' (got: {args.repo})")
        sys.exit(1)

    # Create installer and run
    installer = InboxInstaller(
        target_repo=args.repo,
        target_path=args.path,
        mode=args.mode,
        capabilities=args.capabilities,
        contact_email=args.contact,
        verbose=args.verbose
    )

    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
