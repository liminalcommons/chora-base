#!/usr/bin/env python3
"""Create Capability Server - Fast Setup Script (SAP-047)

This script creates a fully-configured production-ready capability server with
multi-interface support (CLI, REST API, optional MCP) and all chora-base
infrastructure pre-configured.

CAPABILITY SERVER ARCHITECTURE (SAP-042-047):
- Multi-interface support: CLI (Click), REST API (FastAPI), optional MCP (SAP-043)
- Core/interface separation: Business logic independent of interfaces (SAP-042)
- Optional service registry for discovery (SAP-044)
- Optional bootstrap orchestration for startup (SAP-045)
- Optional composition patterns: Saga, circuit breaker, event bus (SAP-046)

GENERATED STRUCTURE:
- Core layer: Models, services, exceptions (interface-agnostic)
- Interface layer: CLI, REST, MCP (conditional)
- Infrastructure layer: Registry, bootstrap, composition (optional)
- Tests: 85%+ coverage target (210+ test cases)
- Documentation: AGENTS.md, CLI.md, API.md, ARCHITECTURE.md
- Configuration: pyproject.toml, Dockerfile, docker-compose.yml
- CI/CD: GitHub Actions workflows (test, lint, release)

Target setup time: 5 minutes (generates 40-60 hours of manual work)
Projected ROI: 2,271% (see SAP-047 capability-charter.md)

Usage:
    # Minimal: CLI + REST only
    python scripts/create-capability-server.py \\
        --name "Task Manager" \\
        --namespace taskmanager \\
        --output ~/projects/task-manager

    # Full: All interfaces + infrastructure
    python scripts/create-capability-server.py \\
        --name "Task Manager" \\
        --namespace taskmanager \\
        --enable-mcp \\
        --enable-registry \\
        --enable-bootstrap \\
        --enable-composition \\
        --output ~/projects/task-manager

    # With author info
    python scripts/create-capability-server.py \\
        --name "Task Manager" \\
        --namespace taskmanager \\
        --author "Alice Smith" \\
        --email "alice@example.com" \\
        --github alice-smith \\
        --output ~/projects/task-manager

NOTE: This replaces the legacy SAP-014 (mcp-server-development) approach.
      For capability servers, always use SAP-047 patterns (this script).
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Try to import Jinja2, provide helpful error if missing
try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    print("❌ Error: Jinja2 not installed")
    print("   Install with: pip install jinja2")
    sys.exit(1)


# ============================================================================
# CONSTANTS
# ============================================================================

VERSION = "2.0.0"  # SAP-047 capability server templates (Phases 1-5 complete, Phase 6 verification)
CHORA_BASE_VERSION = "5.0.0"  # Released: includes capability server architecture suite (SAP-042-047)

# Template variables that can be customized via profiles
DEFAULT_CONFIG = {
    "python_version": "3.11",
    "python_version_nodots": "311",
    "license": "MIT",
    "test_coverage_threshold": 85,
    "project_version": "0.1.0",
    "docker_registry": "ghcr.io",
    "pypi_auth_method": "trusted_publishing",

    # Multi-interface support (SAP-043)
    "enable_mcp": False,  # MCP interface is optional

    # Infrastructure patterns (SAP-044-046)
    "enable_registry": False,  # Service discovery (SAP-044)
    "enable_bootstrap": False,  # Startup orchestration (SAP-045)
    "enable_composition": False,  # Saga, circuit breaker, events (SAP-046)

    # Chora-base SAPs (optional)
    "include_beads": False,  # Task tracking (SAP-015)
    "include_inbox": False,  # Coordination (SAP-001)
    "include_memory": False,  # A-MEM (SAP-010)
    "include_ci_cd": True,  # GitHub Actions (SAP-005)
    "include_docker": True,  # Docker deployment
}

DECISION_PROFILES = {
    "minimal": {
        "description": "CLI + REST only, no optional features",
        # Uses DEFAULT_CONFIG (all optional features disabled)
    },
    "standard": {
        "description": "CLI + REST + MCP, full CI/CD (RECOMMENDED)",
        "enable_mcp": True,
        "include_ci_cd": True,
    },
    "full": {
        "description": "All interfaces + all infrastructure (registry, bootstrap, composition)",
        "enable_mcp": True,
        "enable_registry": True,
        "enable_bootstrap": True,
        "enable_composition": True,
        "include_ci_cd": True,
        "include_beads": True,
        "include_inbox": True,
    },
}


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_namespace(namespace: str) -> bool:
    """Validate MCP namespace format.

    Chora MCP Conventions v1.0:
    - 3-20 characters
    - Lowercase alphanumeric only
    - Must start with letter
    """
    pattern = r'^[a-z][a-z0-9]{2,19}$'
    return bool(re.match(pattern, namespace))


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_slug(slug: str) -> bool:
    """Validate project slug format (kebab-case)."""
    pattern = r'^[a-z][a-z0-9-]+$'
    return bool(re.match(pattern, slug))


def validate_package_name(name: str) -> bool:
    """Validate Python package name (snake_case)."""
    pattern = r'^[a-z][a-z0-9_]+$'
    return bool(re.match(pattern, name))


def validate_github_username(username: str) -> bool:
    """Validate GitHub username format."""
    # GitHub usernames: alphanumeric + hyphen, not start/end with hyphen
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    return bool(re.match(pattern, username))


# ============================================================================
# DERIVATION FUNCTIONS
# ============================================================================

def derive_slug(project_name: str) -> str:
    """Derive kebab-case slug from project name.

    Example: "Weather MCP Server" -> "weather-mcp-server"
    """
    slug = project_name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def derive_package_name(slug: str) -> str:
    """Derive snake_case package name from slug.

    Example: "weather-mcp-server" -> "weather_mcp_server"
    """
    return slug.replace('-', '_')


def derive_namespace(package_name: str) -> str:
    """Derive MCP namespace from package name.

    Example: "weather_mcp_server" -> "weather"

    Takes first component before underscore or _mcp suffix.
    """
    # Remove common suffixes
    namespace = package_name.replace('_mcp', '').replace('_server', '')
    # Take first component
    namespace = namespace.split('_')[0]
    return namespace


def derive_description(project_name: str, namespace: str) -> str:
    """Generate default project description."""
    return f"{project_name} - Multi-interface capability server"


def derive_capability_name_pascal(capability_name: str) -> str:
    """Derive PascalCase class name from capability name.

    Example: "Task Manager" -> "TaskManager"
    """
    # Remove non-alphanumeric characters and split into words
    words = re.findall(r'[A-Za-z0-9]+', capability_name)
    # Capitalize first letter of each word
    return ''.join(word.capitalize() for word in words)


def derive_capability_name_lower(capability_name: str) -> str:
    """Derive lowercase name for messages.

    Example: "Task Manager" -> "task manager"
    """
    return capability_name.lower()


def derive_capability_name_snake(capability_name: str) -> str:
    """Derive snake_case name for Python identifiers.

    Example: "Task Manager" -> "task_manager"
    Example: "Chora Capability Server Template" -> "chora_capability_server_template"
    """
    # Normalize whitespace and replace with underscores
    words = capability_name.split()
    return '_'.join(word.lower() for word in words)


# ============================================================================
# DIRECTORY STRUCTURE FUNCTIONS
# ============================================================================

def create_directory_structure(output_dir: Path, package_name: str, config: Dict[str, Any]) -> None:
    """Create the capability server directory structure.

    Capability server architecture (SAP-042-047):
    project/
    ├── {package_name}/          # Source code (no src/ directory)
    │   ├── core/                # Business logic (interface-agnostic)
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── services.py
    │   │   └── exceptions.py
    │   ├── interfaces/          # Interface adapters
    │   │   ├── cli/             # Click CLI
    │   │   ├── rest/            # FastAPI REST
    │   │   └── mcp/             # FastMCP (optional)
    │   ├── infrastructure/      # Infrastructure patterns (optional)
    │   │   ├── registry/        # Service discovery (if enable_registry)
    │   │   ├── bootstrap/       # Startup orchestration (if enable_bootstrap)
    │   │   └── composition/     # Saga, circuit breaker, events (if enable_composition)
    │   └── config/              # Configuration (future)
    ├── tests/                   # Test suite
    │   ├── core/
    │   ├── interfaces/
    │   └── infrastructure/      (if any infrastructure enabled)
    ├── docs/                    # Documentation (optional, future)
    ├── scripts/                 # Utility scripts (optional, future)
    ├── .github/workflows/       # CI/CD (if include_ci_cd)
    ├── .beads/                  # Task tracking (if include_beads)
    ├── inbox/                   # Coordination (if include_inbox)
    └── .chora/memory/           # A-MEM (if include_memory)
    """
    # Core directories (always created)
    directories = [
        f"{package_name}/core",
        f"{package_name}/interfaces/cli",
        f"{package_name}/interfaces/rest",
        "tests/core",
        "tests/interfaces",
    ]

    # MCP interface (optional)
    if config.get("enable_mcp"):
        directories.append(f"{package_name}/interfaces/mcp")

    # Infrastructure directories (optional)
    if config.get("enable_registry"):
        directories.append(f"{package_name}/infrastructure/registry")
        directories.append("tests/infrastructure")

    if config.get("enable_bootstrap"):
        directories.append(f"{package_name}/infrastructure/bootstrap")
        directories.append("tests/infrastructure")

    if config.get("enable_composition"):
        directories.append(f"{package_name}/infrastructure/composition")
        directories.append("tests/infrastructure")

    # CI/CD (optional)
    if config.get("include_ci_cd"):
        directories.append(".github/workflows")

    # Chora-base SAPs (optional)
    if config.get("include_beads"):
        directories.append(".beads")

    if config.get("include_inbox"):
        directories.extend([
            "inbox/coordination",
            "inbox/examples",
        ])

    if config.get("include_memory"):
        directories.extend([
            ".chora/memory/events",
            ".chora/memory/knowledge",
            ".chora/memory/profiles",
            ".chora/memory/traces",
        ])

    # Create all directories (deduplicate)
    directories = sorted(set(directories))
    for dir_path in directories:
        (output_dir / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {dir_path}/")


def copy_static_template(chora_base_dir: Path, output_dir: Path, config: Dict[str, Any]) -> None:
    """Copy static template files (non-Jinja2 files).

    Note: For capability servers (SAP-047), all files are Jinja2 templates.
    This function is kept for future extensibility but currently does nothing.
    """
    # All capability server files are Jinja2 templates (.template files)
    # No static files to copy
    pass


# ============================================================================
# TEMPLATE RENDERING
# ============================================================================

def render_templates(chora_base_dir: Path, output_dir: Path, variables: Dict[str, Any]) -> None:
    """Render all Jinja2 templates with provided variables."""
    template_dir = chora_base_dir / "static-template" / "capability-server-templates"

    if not template_dir.exists():
        print(f"❌ Error: Template directory not found: {template_dir}")
        sys.exit(1)

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,  # Fail on undefined variables
    )

    package_name = variables['package_name']

    # Template mapping: template_name -> output_path
    # Organized by phase for clarity
    template_mappings = {}

    # ========================================================================
    # PHASE 1: Core Templates
    # ========================================================================
    template_mappings.update({
        "core/__init__.py.template": f"{package_name}/core/__init__.py",
        "core/models.py.template": f"{package_name}/core/models.py",
        "core/services.py.template": f"{package_name}/core/services.py",
        "core/exceptions.py.template": f"{package_name}/core/exceptions.py",
        "tests/core/test_models.py.template": "tests/core/test_models.py",
        "tests/core/test_services.py.template": "tests/core/test_services.py",
        "tests/core/test_exceptions.py.template": "tests/core/test_exceptions.py",
    })

    # ========================================================================
    # PHASE 2: Interface Templates
    # ========================================================================
    # CLI interface (always included)
    template_mappings.update({
        "interfaces/cli/__init__.py.template": f"{package_name}/interfaces/cli/__init__.py",
        "interfaces/cli/commands.py.template": f"{package_name}/interfaces/cli/commands.py",
        "interfaces/cli/formatters.py.template": f"{package_name}/interfaces/cli/formatters.py",
    })

    # REST interface (always included)
    template_mappings.update({
        "interfaces/rest/__init__.py.template": f"{package_name}/interfaces/rest/__init__.py",
        "interfaces/rest/routes.py.template": f"{package_name}/interfaces/rest/routes.py",
        "interfaces/rest/models.py.template": f"{package_name}/interfaces/rest/models.py",
        "interfaces/rest/middleware.py.template": f"{package_name}/interfaces/rest/middleware.py",
    })

    # MCP interface (optional)
    if variables.get('enable_mcp'):
        template_mappings.update({
            "interfaces/mcp/__init__.py.template": f"{package_name}/interfaces/mcp/__init__.py",
            "interfaces/mcp/tools.py.template": f"{package_name}/interfaces/mcp/tools.py",
            "interfaces/mcp/resources.py.template": f"{package_name}/interfaces/mcp/resources.py",
        })

    # Interface tests
    template_mappings.update({
        "tests/interfaces/test_cli.py.template": "tests/interfaces/test_cli.py",
        "tests/interfaces/test_rest.py.template": "tests/interfaces/test_rest.py",
    })
    if variables.get('enable_mcp'):
        template_mappings["tests/interfaces/test_mcp.py.template"] = "tests/interfaces/test_mcp.py"

    # ========================================================================
    # PHASE 3: Infrastructure Templates
    # ========================================================================
    # Registry (optional)
    if variables.get('enable_registry'):
        template_mappings.update({
            "infrastructure/registry/__init__.py.template": f"{package_name}/infrastructure/registry/__init__.py",
            "infrastructure/registry/registry.py.template": f"{package_name}/infrastructure/registry/registry.py",
            "tests/infrastructure/test_registry.py.template": "tests/infrastructure/test_registry.py",
        })

    # Bootstrap (optional)
    if variables.get('enable_bootstrap'):
        template_mappings.update({
            "infrastructure/bootstrap/__init__.py.template": f"{package_name}/infrastructure/bootstrap/__init__.py",
            "infrastructure/bootstrap/bootstrap.py.template": f"{package_name}/infrastructure/bootstrap/bootstrap.py",
            "tests/infrastructure/test_bootstrap.py.template": "tests/infrastructure/test_bootstrap.py",
        })

    # Composition (optional)
    if variables.get('enable_composition'):
        template_mappings.update({
            "infrastructure/composition/__init__.py.template": f"{package_name}/infrastructure/composition/__init__.py",
            "infrastructure/composition/circuit_breaker.py.template": f"{package_name}/infrastructure/composition/circuit_breaker.py",
            "infrastructure/composition/event_bus.py.template": f"{package_name}/infrastructure/composition/event_bus.py",
            "infrastructure/composition/saga.py.template": f"{package_name}/infrastructure/composition/saga.py",
            "tests/infrastructure/test_circuit_breaker.py.template": "tests/infrastructure/test_circuit_breaker.py",
            "tests/infrastructure/test_event_bus.py.template": "tests/infrastructure/test_event_bus.py",
            "tests/infrastructure/test_saga.py.template": "tests/infrastructure/test_saga.py",
        })

    # Infrastructure package __init__.py (if any infrastructure enabled)
    if any([variables.get('enable_registry'), variables.get('enable_bootstrap'), variables.get('enable_composition')]):
        template_mappings["infrastructure/__init__.py.template"] = f"{package_name}/infrastructure/__init__.py"

    # ========================================================================
    # PHASE 4: Documentation & Configuration Templates
    # ========================================================================
    # Documentation
    template_mappings.update({
        "AGENTS.md.template": "AGENTS.md",
        "CLAUDE.md.template": "CLAUDE.md",
        "VERIFICATION.md.template": "VERIFICATION.md",
        "CLI.md.template": "CLI.md",
        "API.md.template": "API.md",
        "ARCHITECTURE.md.template": "ARCHITECTURE.md",
    })

    # Configuration
    template_mappings.update({
        "pyproject.toml.template": "pyproject.toml",
        "setup.py.template": "setup.py",
        "README.md.template": "README.md",
    })

    # Deployment
    if variables.get('include_docker'):
        template_mappings.update({
            "Dockerfile.template": "Dockerfile",
            "docker-compose.yml.template": "docker-compose.yml",
        })

    # CI/CD
    if variables.get('include_ci_cd'):
        template_mappings.update({
            ".github/workflows/ci.yml.template": ".github/workflows/ci.yml",
            ".github/workflows/cd.yml.template": ".github/workflows/cd.yml",
            ".github/dependabot.yml.template": ".github/dependabot.yml",
        })

    # ========================================================================
    # Package __init__.py files (simple content, no templates needed)
    # ========================================================================
    # Create package __init__.py files directly
    init_files = {
        f"{package_name}/__init__.py": f'"""{ variables["capability_name"]} - Multi-interface capability server."""\n\n__version__ = "{variables["project_version"]}"\n',
        f"{package_name}/interfaces/__init__.py": '"""Interface adapters for CLI, REST, and MCP."""\n',
        "tests/__init__.py": '"""Test suite for {capability_name}."""\n'.format(**variables),
        "tests/core/__init__.py": '"""Core logic tests."""\n',
        "tests/interfaces/__init__.py": '"""Interface tests."""\n',
    }
    if any([variables.get('enable_registry'), variables.get('enable_bootstrap'), variables.get('enable_composition')]):
        init_files["tests/infrastructure/__init__.py"] = '"""Infrastructure tests."""\n'

    # ========================================================================
    # Render all templates
    # ========================================================================
    print(f"\nRendering templates ({len(template_mappings)} files)...")
    rendered_count = 0
    for template_name, output_path in sorted(template_mappings.items()):
        try:
            template = env.get_template(template_name)
            output = template.render(**variables)

            # Write rendered content
            output_file = output_dir / output_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output, encoding='utf-8')

            # Check for unsubstituted variables
            if '{{' in output or '}}' in output:
                print(f"  ⚠️  {output_path} - Warning: Unsubstituted variables found")
            else:
                rendered_count += 1
                print(f"  ✓ Rendered {output_path}")

        except Exception as e:
            print(f"  ❌ Error rendering {template_name}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # Write __init__.py files
    print(f"\nCreating __init__.py files ({len(init_files)} files)...")
    for file_path, content in sorted(init_files.items()):
        output_file = output_dir / file_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
        print(f"  ✓ Created {file_path}")

    print(f"\n✅ Successfully rendered {rendered_count}/{len(template_mappings)} templates + {len(init_files)} __init__.py files")


# ============================================================================
# SAP INITIALIZATION
# ============================================================================

def initialize_beads(output_dir: Path, variables: Dict[str, Any]) -> None:
    """Initialize beads task tracking (SAP-015)."""
    print("\nInitializing beads (SAP-015)...")

    beads_dir = output_dir / ".beads"
    beads_dir.mkdir(exist_ok=True)

    # Create config.yaml
    config_yaml = f"""# Beads Configuration (SAP-015)
project_id: {variables['project_slug']}
project_name: {variables['project_name']}
version: 1.0.0

# Task ID generation
hash_length: 3

# Git integration
auto_commit: true
commit_message_template: "task({{id}}): {{summary}}"

# Defaults
default_assignee: {variables['author_name']}
default_priority: medium
"""
    (beads_dir / "config.yaml").write_text(config_yaml, encoding='utf-8')
    print("  ✓ Created .beads/config.yaml")

    # Create metadata.json
    metadata = {
        "project_id": variables['project_slug'],
        "project_name": variables['project_name'],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "created_by": variables['author_name'],
        "chora_base_version": CHORA_BASE_VERSION,
        "beads_version": "0.21.6",
    }
    (beads_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print("  ✓ Created .beads/metadata.json")

    # Create empty issues.jsonl
    (beads_dir / "issues.jsonl").touch()
    print("  ✓ Created .beads/issues.jsonl")

    # Create .gitignore for .beads/
    gitignore = """# Beads - Git-backed task tracking
# Commit issues.jsonl, ignore everything else

# SQLite database (auto-generated from issues.jsonl)
beads.db
beads.db-shm
beads.db-wal

# Daemon and logs
daemon.log
*.log

# Backups
*.backup
*.bak

# Keep issues.jsonl (source of truth)
!issues.jsonl
!config.yaml
!metadata.json
"""
    (beads_dir / ".gitignore").write_text(gitignore, encoding='utf-8')
    print("  ✓ Created .beads/.gitignore")


def initialize_inbox(output_dir: Path, variables: Dict[str, Any]) -> None:
    """Initialize inbox coordination (SAP-001)."""
    print("\nInitializing inbox (SAP-001)...")

    inbox_dir = output_dir / "inbox"
    coord_dir = inbox_dir / "coordination"

    # Create active.jsonl and archived.jsonl
    (coord_dir / "active.jsonl").touch()
    (coord_dir / "archived.jsonl").touch()
    print("  ✓ Created inbox/coordination/active.jsonl")
    print("  ✓ Created inbox/coordination/archived.jsonl")

    # Create events.jsonl with initialization event
    init_event = {
        "event_type": "inbox_initialized",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": variables['project_name'],
        "created_by": variables['author_name'],
        "chora_base_version": CHORA_BASE_VERSION,
    }
    (coord_dir / "events.jsonl").write_text(json.dumps(init_event) + "\n", encoding='utf-8')
    print("  ✓ Created inbox/coordination/events.jsonl")

    # Create README.md
    readme = f"""# Inbox - Cross-Repository Coordination

This directory implements SAP-001 v1.2.0 (Inbox Protocol) for coordinating work across
repositories and agents.

## Structure

- `coordination/active.jsonl` - Active coordination requests
- `coordination/archived.jsonl` - Completed/rejected requests
- `coordination/events.jsonl` - Event log
- `examples/` - Example coordination patterns

## Usage

See [SAP-001 documentation](docs/skilled-awareness/inbox/) for details.

## Optional Features (v1.2.0)

This project includes basic inbox setup (Level 1). To enable advanced features:

- **Level 2 (CLI Tools)**: Install Python CLI tools for inbox management
  ```bash
  pip install click pyyaml jsonlines
  ```

- **Level 3 (AI Generation)**: Enable AI-powered COORD generation (60x ROI)
  ```bash
  pip install anthropic openai jinja2
  export ANTHROPIC_API_KEY="sk-ant-..."
  ```

- **Light+ Integration**: Connect inbox to strategic planning (SAP-012)
  - Add `light_plus_metadata` to COORD schema
  - Use Phase 1.1 Discovery workflow for quarterly planning
  - See adoption-blueprint.md for setup instructions

**Project**: {variables['project_name']}
**Initialized**: {datetime.utcnow().date().isoformat()}
**SAP-001 Version**: 1.2.0
"""
    (inbox_dir / "README.md").write_text(readme, encoding='utf-8')
    print("  ✓ Created inbox/README.md")


def initialize_memory(output_dir: Path, variables: Dict[str, Any]) -> None:
    """Initialize A-MEM memory system (SAP-010)."""
    print("\nInitializing A-MEM (SAP-010)...")

    memory_dir = output_dir / ".chora" / "memory"
    events_dir = memory_dir / "events"

    # Create initial event
    init_event = {
        "event_type": "project_created",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": variables['project_name'],
        "package": variables['package_name'],
        "namespace": variables.get('mcp_namespace', ''),
        "created_by": variables['author_name'],
        "chora_base_version": CHORA_BASE_VERSION,
        "template_version": VERSION,
        "metadata": {
            "python_version": variables.get('python_version', '3.11'),
            "license": variables.get('license', 'MIT'),
            "includes": {
                "beads": variables.get('include_beads', False),
                "inbox": variables.get('include_inbox', False),
                "memory": True,
                "ci_cd": variables.get('include_ci_cd', False),
            }
        }
    }
    (events_dir / "development.jsonl").write_text(json.dumps(init_event) + "\n", encoding='utf-8')
    print("  ✓ Created .chora/memory/events/development.jsonl")

    # Create memory README
    readme = f"""# A-MEM - Agent Memory System

This directory implements SAP-010 (Memory System) for event-sourced agent memory,
cross-session learning, and knowledge graph management.

## Structure

- `events/` - Event-sourced history (development, testing, deployment)
- `knowledge/` - Zettelkasten knowledge graph
- `profiles/` - Agent profiles and preferences
- `traces/` - Execution traces and debugging

## Event Schema

See [SAP-010 protocol-spec](docs/skilled-awareness/memory-system/protocol-spec.md) for event schema v1.0.

**Project**: {variables['project_name']}
**Initialized**: {datetime.utcnow().date().isoformat()}
"""
    (memory_dir / "README.md").write_text(readme, encoding='utf-8')
    print("  ✓ Created .chora/memory/README.md")


# ============================================================================
# GIT INITIALIZATION
# ============================================================================

def initialize_git(output_dir: Path, variables: Dict[str, Any]) -> None:
    """Initialize git repository with initial commit."""
    print("\nInitializing git repository...")

    try:
        # Initialize git
        subprocess.run(
            ["git", "init"],
            cwd=output_dir,
            check=True,
            capture_output=True,
        )
        print("  ✓ Initialized git repository")

        # Add all files
        subprocess.run(
            ["git", "add", "."],
            cwd=output_dir,
            check=True,
            capture_output=True,
        )
        print("  ✓ Staged all files")

        # Create initial commit
        commit_message = f"""Initial commit from chora-base model-citizen template v{VERSION}

Project: {variables['project_name']}
Package: {variables['package_name']}
Namespace: {variables.get('mcp_namespace', 'N/A')}

Generated with chora-base v{CHORA_BASE_VERSION}
Template: model-citizen-mcp v{VERSION}

Includes:
- FastMCP server scaffold
- Beads task tracking (SAP-015): {variables.get('include_beads', False)}
- Inbox coordination (SAP-001): {variables.get('include_inbox', False)}
- A-MEM memory system (SAP-010): {variables.get('include_memory', False)}
- CI/CD workflows (SAP-005): {variables.get('include_ci_cd', False)}
- Quality gates (SAP-006): ✓
- Testing framework (SAP-004): ✓
- Documentation (SAP-007): ✓
- Agent awareness (SAP-009): ✓

Created by: {variables['author_name']} <{variables['author_email']}>
Date: {datetime.utcnow().date().isoformat()}
"""

        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=output_dir,
            check=True,
            capture_output=True,
        )
        print("  ✓ Created initial commit")

    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  Git initialization failed: {e}")
        print("     (You can initialize git manually later)")


# ============================================================================
# VALIDATION
# ============================================================================

def validate_generated_project(output_dir: Path, variables: Dict[str, Any]) -> bool:
    """Validate the generated project meets capability server requirements (SAP-047)."""
    print("\nValidating generated project...")

    checks = []
    package_name = variables['package_name']

    # ========================================================================
    # Core Layer Checks
    # ========================================================================
    checks.append(("Core models exist", (output_dir / package_name / "core" / "models.py").exists()))
    checks.append(("Core services exist", (output_dir / package_name / "core" / "services.py").exists()))
    checks.append(("Core exceptions exist", (output_dir / package_name / "core" / "exceptions.py").exists()))

    # ========================================================================
    # Interface Layer Checks
    # ========================================================================
    checks.append(("CLI interface exists", (output_dir / package_name / "interfaces" / "cli" / "__init__.py").exists()))
    checks.append(("REST interface exists", (output_dir / package_name / "interfaces" / "rest" / "__init__.py").exists()))

    if variables.get('enable_mcp'):
        mcp_check = (output_dir / package_name / "interfaces" / "mcp" / "__init__.py").exists()
        checks.append(("MCP interface exists (optional)", mcp_check))

    # ========================================================================
    # Infrastructure Layer Checks (Optional)
    # ========================================================================
    if variables.get('enable_registry'):
        registry_check = (output_dir / package_name / "infrastructure" / "registry" / "registry.py").exists()
        checks.append(("Registry exists (SAP-044)", registry_check))

    if variables.get('enable_bootstrap'):
        bootstrap_check = (output_dir / package_name / "infrastructure" / "bootstrap" / "bootstrap.py").exists()
        checks.append(("Bootstrap exists (SAP-045)", bootstrap_check))

    if variables.get('enable_composition'):
        circuit_breaker_check = (output_dir / package_name / "infrastructure" / "composition" / "circuit_breaker.py").exists()
        event_bus_check = (output_dir / package_name / "infrastructure" / "composition" / "event_bus.py").exists()
        saga_check = (output_dir / package_name / "infrastructure" / "composition" / "saga.py").exists()
        checks.append(("Composition patterns exist (SAP-046)", circuit_breaker_check and event_bus_check and saga_check))

    # ========================================================================
    # Test Suite Checks
    # ========================================================================
    checks.append(("Core tests exist", (output_dir / "tests" / "core" / "test_models.py").exists()))
    checks.append(("Interface tests exist", (output_dir / "tests" / "interfaces" / "test_cli.py").exists()))

    if any([variables.get('enable_registry'), variables.get('enable_bootstrap'), variables.get('enable_composition')]):
        infra_tests_exist = (output_dir / "tests" / "infrastructure").exists()
        checks.append(("Infrastructure tests exist", infra_tests_exist))

    # ========================================================================
    # Documentation Checks
    # ========================================================================
    checks.append(("AGENTS.md exists", (output_dir / "AGENTS.md").exists()))
    checks.append(("CLI.md exists", (output_dir / "CLI.md").exists()))
    checks.append(("API.md exists", (output_dir / "API.md").exists()))
    checks.append(("ARCHITECTURE.md exists", (output_dir / "ARCHITECTURE.md").exists()))
    checks.append(("README.md exists", (output_dir / "README.md").exists()))

    # ========================================================================
    # Configuration Checks
    # ========================================================================
    checks.append(("pyproject.toml exists", (output_dir / "pyproject.toml").exists()))
    checks.append(("setup.py exists", (output_dir / "setup.py").exists()))

    if variables.get('include_docker'):
        checks.append(("Dockerfile exists", (output_dir / "Dockerfile").exists()))
        checks.append(("docker-compose.yml exists", (output_dir / "docker-compose.yml").exists()))

    if variables.get('include_ci_cd'):
        ci_check = (output_dir / ".github" / "workflows" / "ci.yml").exists()
        cd_check = (output_dir / ".github" / "workflows" / "cd.yml").exists()
        checks.append(("CI/CD workflows exist", ci_check and cd_check))

    # ========================================================================
    # Chora-base SAP Checks (Optional)
    # ========================================================================
    if variables.get('include_beads'):
        beads_check = (output_dir / ".beads" / "issues.jsonl").exists()
        checks.append(("Beads initialized (SAP-015)", beads_check))

    if variables.get('include_inbox'):
        inbox_check = (output_dir / "inbox" / "coordination" / "active.jsonl").exists()
        checks.append(("Inbox initialized (SAP-001)", inbox_check))

    if variables.get('include_memory'):
        memory_check = (output_dir / ".chora" / "memory" / "events" / "development.jsonl").exists()
        checks.append(("A-MEM initialized (SAP-010)", memory_check))

    # ========================================================================
    # Git Repository Check
    # ========================================================================
    checks.append(("Git repository initialized", (output_dir / ".git").exists()))

    # ========================================================================
    # Template Variable Substitution Check
    # ========================================================================
    unsubstituted_files = []
    for py_file in output_dir.rglob("*.py"):
        content = py_file.read_text(encoding='utf-8')
        # Check for {{ }} but exclude Jinja2 raw blocks and comments
        if ('{{' in content or '}}' in content) and 'Jinja2' not in content:
            unsubstituted_files.append(str(py_file.relative_to(output_dir)))
    checks.append(("No unsubstituted variables", len(unsubstituted_files) == 0))

    # ========================================================================
    # Print Results
    # ========================================================================
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False

    if unsubstituted_files:
        print("\n  ⚠️  Files with unsubstituted variables:")
        for file_path in unsubstituted_files:
            print(f"     - {file_path}")

    return all_passed


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Create a capability server with multi-interface support (SAP-047)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Required arguments
    parser.add_argument(
        "--name",
        required=True,
        help="Capability name (e.g., 'Task Manager', 'Weather Service')",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output directory for the new project",
    )

    # Namespace (used for MCP if enabled, also for CLI/API naming)
    parser.add_argument(
        "--namespace",
        help="Namespace for interfaces (3-20 chars, lowercase, alphanumeric). If not provided, derived from name.",
    )

    # Author information
    parser.add_argument(
        "--author",
        help="Author name (default: from git config)",
    )
    parser.add_argument(
        "--email",
        help="Author email (default: from git config)",
    )
    parser.add_argument(
        "--github",
        help="GitHub username/org (default: from git remote or author name)",
    )

    # Optional customization
    parser.add_argument(
        "--description",
        help="Project description (default: auto-generated)",
    )
    parser.add_argument(
        "--profile",
        choices=["minimal", "standard", "full"],
        default="minimal",
        help="Decision profile: minimal (CLI+REST), standard (CLI+REST+MCP+CI/CD), full (all features). Default: minimal",
    )

    # Interface flags (SAP-043)
    parser.add_argument(
        "--enable-mcp",
        action="store_true",
        help="Enable MCP interface (FastMCP)",
    )

    # Infrastructure flags (SAP-044-046)
    parser.add_argument(
        "--enable-registry",
        action="store_true",
        help="Enable service registry (SAP-044)",
    )
    parser.add_argument(
        "--enable-bootstrap",
        action="store_true",
        help="Enable bootstrap orchestration (SAP-045)",
    )
    parser.add_argument(
        "--enable-composition",
        action="store_true",
        help="Enable composition patterns: saga, circuit breaker, event bus (SAP-046)",
    )

    # Chora-base SAPs (optional)
    parser.add_argument(
        "--enable-beads",
        action="store_true",
        help="Enable beads task tracking (SAP-015)",
    )
    parser.add_argument(
        "--enable-inbox",
        action="store_true",
        help="Enable inbox coordination (SAP-001)",
    )
    parser.add_argument(
        "--enable-memory",
        action="store_true",
        help="Enable A-MEM memory system (SAP-010)",
    )

    # System flags
    parser.add_argument(
        "--chora-base-dir",
        type=Path,
        default=Path(__file__).parent.parent,  # Assume running from chora-base/scripts/
        help="Path to chora-base directory (default: auto-detected)",
    )

    # Validation flags
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip post-generation validation",
    )
    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Skip git initialization",
    )

    args = parser.parse_args()

    # Print header
    print("=" * 80)
    print(f"Create Capability Server v{VERSION} (SAP-047)")
    print(f"Chora-Base v{CHORA_BASE_VERSION}")
    print("=" * 80)
    print()

    # Validate chora-base directory
    if not args.chora_base_dir.exists():
        print(f"❌ Error: chora-base directory not found: {args.chora_base_dir}")
        sys.exit(1)

    template_dir = args.chora_base_dir / "static-template" / "capability-server-templates"
    if not template_dir.exists():
        print(f"❌ Error: Template directory not found: {template_dir}")
        print("   Make sure you're running from chora-base directory")
        print("   Expected: static-template/capability-server-templates/")
        sys.exit(1)

    # Load decision profile
    profile_config = DEFAULT_CONFIG.copy()
    if args.profile in DECISION_PROFILES:
        profile_config.update(DECISION_PROFILES[args.profile])
        print(f"📋 Using profile: {args.profile}")
        print(f"   {DECISION_PROFILES[args.profile]['description']}")
        print()

    # Override profile with explicit flags
    if args.enable_mcp:
        profile_config['enable_mcp'] = True
    if args.enable_registry:
        profile_config['enable_registry'] = True
    if args.enable_bootstrap:
        profile_config['enable_bootstrap'] = True
    if args.enable_composition:
        profile_config['enable_composition'] = True
    if args.enable_beads:
        profile_config['include_beads'] = True
    if args.enable_inbox:
        profile_config['include_inbox'] = True
    if args.enable_memory:
        profile_config['include_memory'] = True

    # Derive variables
    print("🔧 Deriving project variables...")
    project_slug = derive_slug(args.name)
    package_name = derive_package_name(project_slug)

    # Use provided namespace or derive from package name
    if args.namespace:
        if not validate_namespace(args.namespace):
            print(f"❌ Error: Invalid namespace format: {args.namespace}")
            print("   Must be 3-20 chars, lowercase alphanumeric, start with letter")
            sys.exit(1)
        mcp_namespace = args.namespace
    else:
        mcp_namespace = derive_namespace(package_name)
        print(f"   Auto-derived namespace: {mcp_namespace}")

    # Get author info from git config if not provided
    author_name = args.author
    author_email = args.email

    if not author_name:
        try:
            result = subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True,
                text=True,
                check=True,
            )
            author_name = result.stdout.strip()
            print(f"   Auto-detected author: {author_name} (from git config)")
        except subprocess.CalledProcessError:
            print("❌ Error: --author required (git config user.name not set)")
            sys.exit(1)

    if not author_email:
        try:
            result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True,
                text=True,
                check=True,
            )
            author_email = result.stdout.strip()
            print(f"   Auto-detected email: {author_email} (from git config)")
        except subprocess.CalledProcessError:
            print("❌ Error: --email required (git config user.email not set)")
            sys.exit(1)

    # Validate email
    if not validate_email(author_email):
        print(f"❌ Error: Invalid email format: {author_email}")
        sys.exit(1)

    # Get GitHub username
    github_username = args.github
    if not github_username:
        # Try to derive from git remote
        try:
            result = subprocess.run(
                ["git", "config", "remote.origin.url"],
                capture_output=True,
                text=True,
                check=True,
            )
            remote_url = result.stdout.strip()
            # Extract username from git@github.com:username/repo.git or https://github.com/username/repo.git
            match = re.search(r'github\.com[:/]([^/]+)', remote_url)
            if match:
                github_username = match.group(1)
                print(f"   Auto-detected GitHub: {github_username} (from git remote)")
        except subprocess.CalledProcessError:
            pass

    if not github_username:
        # Fallback to author name (make it GitHub-safe)
        github_username = author_name.lower().replace(' ', '-')
        print(f"   Using GitHub username: {github_username} (derived from author)")

    if not validate_github_username(github_username):
        print(f"❌ Error: Invalid GitHub username format: {github_username}")
        sys.exit(1)

    # Build variables dict
    variables = {
        # Core identifiers
        "capability_name": args.name,  # Human-readable name (e.g., "Task Manager")
        "capability_name_pascal": derive_capability_name_pascal(args.name),  # PascalCase (e.g., "TaskManager")
        "capability_name_lower": derive_capability_name_lower(args.name),  # lowercase (e.g., "task manager")
        "capability_name_snake": derive_capability_name_snake(args.name),  # snake_case (e.g., "task_manager")
        "project_name": args.name,  # Legacy compatibility
        "project_slug": project_slug,  # Filesystem-safe slug
        "package_name": package_name,  # Python package name
        "namespace": mcp_namespace,  # Used for CLI/REST/MCP interfaces
        "mcp_namespace": mcp_namespace,  # Legacy compatibility

        # Metadata
        "project_description": args.description or derive_description(args.name, mcp_namespace),
        "author_name": author_name,
        "author_email": author_email,
        "github_username": github_username,
        "github_org": github_username,  # Default to same as username
        "docker_org": github_username,  # Default Docker org to GitHub username

        # Configuration (includes enable_* flags)
        **profile_config,

        # Timestamps
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    # Print summary
    print("\n📦 Project Configuration")
    print("─" * 80)
    print(f"  Capability Name:  {variables['capability_name']}")
    print(f"  Package Name:     {variables['package_name']}")
    print(f"  Namespace:        {variables['namespace']}")
    print(f"  Description:      {variables['project_description']}")
    print(f"  Author:           {variables['author_name']} <{variables['author_email']}>")
    print(f"  GitHub:           {variables['github_username']}")
    print(f"  Python Version:   {variables['python_version']}")
    print(f"  License:          {variables['license']}")
    print(f"  Profile:          {args.profile}")
    print()
    print("  Interfaces:")
    print("    ✅ CLI (Click)")
    print("    ✅ REST API (FastAPI)")
    if variables.get('enable_mcp'):
        print("    ✅ MCP (FastMCP)")
    print()
    print("  Infrastructure:")
    if variables.get('enable_registry'):
        print("    ✅ Service Registry (SAP-044)")
    if variables.get('enable_bootstrap'):
        print("    ✅ Bootstrap Orchestration (SAP-045)")
    if variables.get('enable_composition'):
        print("    ✅ Composition Patterns (SAP-046)")
    if not any([variables.get('enable_registry'), variables.get('enable_bootstrap'), variables.get('enable_composition')]):
        print("    (none - minimal profile)")
    print("─" * 80)
    print()

    # Check if output directory exists
    if args.output.exists():
        print(f"❌ Error: Output directory already exists: {args.output}")
        print("   Choose a different location or remove the existing directory")
        sys.exit(1)

    # Create output directory
    print(f"📁 Creating project at: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    print("\n📂 Creating directory structure...")
    create_directory_structure(args.output, package_name, variables)

    # Copy static template files
    print("\n📋 Copying static files...")
    copy_static_template(args.chora_base_dir, args.output, variables)

    # Render Jinja2 templates
    render_templates(args.chora_base_dir, args.output, variables)

    # Initialize SAPs
    if variables.get('include_beads'):
        initialize_beads(args.output, variables)

    if variables.get('include_inbox'):
        initialize_inbox(args.output, variables)

    if variables.get('include_memory'):
        initialize_memory(args.output, variables)

    # Initialize git
    if not args.skip_git:
        initialize_git(args.output, variables)

    # Validate generated project
    if not args.skip_validation:
        validation_passed = validate_generated_project(args.output, variables)
        if not validation_passed:
            print("\n⚠️  Some validation checks failed (see above)")
            print("   Project generated but may need manual fixes")

    # Print success message
    print("\n" + "=" * 80)
    print("✅ Capability Server Created Successfully!")
    print("=" * 80)
    print()
    print(f"📁 Location: {args.output.absolute()}")
    print()
    print("📝 Next Steps:")
    print()
    print("1. Navigate to project:")
    print(f"   cd {args.output}")
    print()
    print("2. Create virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # On macOS/Linux")
    print("   # venv\\Scripts\\activate  # On Windows")
    print()
    print("3. Install dependencies:")
    print("   pip install -e .[dev]")
    print()
    print("4. Run tests:")
    print("   pytest")
    print()
    print("5. Start the server (choose one):")
    print()
    print("   a) CLI Interface:")
    print(f"      {package_name} --help")
    print(f"      {package_name} create \"My Item\"")
    print()
    print("   b) REST API:")
    print("      uvicorn {}.interfaces.rest:app --reload".format(package_name))
    print("      # Then visit: http://localhost:8000/docs")
    print()

    if variables.get('enable_mcp'):
        print("   c) MCP Interface:")
        print(f"      Add to ~/Library/Application Support/Claude/claude_desktop_config.json:")
        print(f'''      {{
        "mcpServers": {{
          "{variables['namespace']}": {{
            "command": "python",
            "args": ["-m", "{package_name}.interfaces.mcp"],
            "cwd": "{args.output.absolute()}"
          }}
        }}
      }}
''')
        print()

    print("6. Run with Docker (optional):")
    if variables.get('include_docker'):
        print("   docker-compose up -d")
        print("   # API: http://localhost:8000")
        if variables.get('enable_registry'):
            print("   # Registry: http://localhost:8001")
        print()

    print("📚 Documentation:")
    print(f"   README:        {args.output}/README.md")
    print(f"   AGENTS.md:     {args.output}/AGENTS.md")
    print(f"   CLI.md:        {args.output}/CLI.md")
    print(f"   API.md:        {args.output}/API.md")
    print(f"   ARCHITECTURE:  {args.output}/ARCHITECTURE.md")
    print()

    if variables.get('include_beads'):
        print("🔧 Beads Task Tracking:")
        print("   bd create \"First task\" --assignee me")
        print("   bd list")
        print()

    print("🚀 Happy coding!")
    print()


if __name__ == "__main__":
    main()
