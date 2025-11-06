#!/usr/bin/env python3
"""Create Model Citizen MCP Server - Fast Setup Script

This script creates a fully-configured "model citizen" MCP server with all
chora-base infrastructure pre-configured:

- FastMCP server scaffold
- Beads task tracking (SAP-015)
- Inbox coordination (SAP-001)
- A-MEM memory system (SAP-010)
- CI/CD workflows (SAP-005)
- Quality gates (SAP-006)
- Testing framework (SAP-004)
- Documentation (SAP-007)
- Agent awareness (SAP-009)

Target setup time: 1-2 minutes (agent), 5-10 minutes (human)

Usage:
    python scripts/create-model-mcp-server.py \\
        --name "Weather MCP Server" \\
        --namespace weather \\
        --author "Alice Smith" \\
        --email "alice@example.com" \\
        --github alice-smith \\
        --output ~/projects/weather-mcp

    # Or use a decision profile (minimal/standard/full)
    python scripts/create-model-mcp-server.py \\
        --profile standard \\
        --name "Weather" \\
        --namespace weather \\
        --output ~/projects/weather-mcp
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

VERSION = "1.0.0"
CHORA_BASE_VERSION = "4.9.0"

# Template variables that can be customized via profiles
DEFAULT_CONFIG = {
    "python_version": "3.11",
    "python_version_nodots": "311",
    "license": "MIT",
    "test_coverage_threshold": 85,
    "project_version": "0.1.0",
    "docker_registry": "ghcr.io",
    "mcp_enable_namespacing": "true",
    "mcp_validate_names": "true",
    "mcp_resource_uri_scheme": "true",
    "include_beads": True,
    "include_inbox": True,
    "include_memory": True,
    "include_ci_cd": True,
}

DECISION_PROFILES = {
    "minimal": {
        "description": "FastMCP only, no beads/inbox, minimal CI",
        "include_beads": False,
        "include_inbox": False,
        "include_memory": False,
        "include_ci_cd": False,
    },
    "standard": {
        "description": "FastMCP + beads + inbox, full CI/CD (DEFAULT)",
        # Uses DEFAULT_CONFIG
    },
    "full": {
        "description": "Standard + A-MEM advanced features, all SAPs",
        "include_memory": True,
        # Additional future features can go here
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
    return f"{project_name} - MCP server for {namespace} operations"


# ============================================================================
# DIRECTORY STRUCTURE FUNCTIONS
# ============================================================================

def create_directory_structure(output_dir: Path, package_name: str, config: Dict[str, Any]) -> None:
    """Create the project directory structure.

    Standard structure:
    project/
    ├── src/
    │   └── {package}/
    │       ├── __init__.py
    │       ├── server.py
    │       └── mcp/
    │           └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── docs/
    │   ├── user-docs/
    │   ├── dev-docs/
    │   └── project-docs/
    ├── scripts/
    ├── .github/workflows/
    ├── .beads/              (if include_beads)
    ├── inbox/               (if include_inbox)
    ├── .chora/memory/       (if include_memory)
    └── logs/
    """
    directories = [
        f"src/{package_name}",
        f"src/{package_name}/mcp",
        "tests",
        "docs/user-docs",
        "docs/dev-docs",
        "docs/project-docs",
        "docs/skilled-awareness",
        "scripts",
        ".github/workflows",
        "logs",
    ]

    # Conditional directories based on config
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

    # Create all directories
    for dir_path in directories:
        (output_dir / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {dir_path}/")


def copy_static_template(chora_base_dir: Path, output_dir: Path, config: Dict[str, Any]) -> None:
    """Copy static template files (non-Jinja2 files)."""
    static_template = chora_base_dir / "static-template"

    # Files to copy directly (not templated)
    static_files = [
        ".gitignore",
        ".dockerignore",
        "Dockerfile",
        "Dockerfile.test",
        "docker-compose.yml",
        ".coveragerc",
        "ruff.toml",
        ".editorconfig",
    ]

    if config.get("include_ci_cd"):
        # Copy GitHub Actions workflows
        workflows_src = static_template / ".github" / "workflows"
        workflows_dst = output_dir / ".github" / "workflows"
        if workflows_src.exists():
            for workflow in workflows_src.glob("*.yml"):
                shutil.copy2(workflow, workflows_dst / workflow.name)
                print(f"  ✓ Copied .github/workflows/{workflow.name}")

    # Copy static files
    for file_name in static_files:
        src = static_template / file_name
        if src.exists():
            shutil.copy2(src, output_dir / file_name)
            print(f"  ✓ Copied {file_name}")


# ============================================================================
# TEMPLATE RENDERING
# ============================================================================

def render_templates(chora_base_dir: Path, output_dir: Path, variables: Dict[str, Any]) -> None:
    """Render all Jinja2 templates with provided variables."""
    template_dir = chora_base_dir / "static-template" / "mcp-templates"

    if not template_dir.exists():
        print(f"❌ Error: Template directory not found: {template_dir}")
        sys.exit(1)

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,  # Fail on undefined variables
    )

    # Template mapping: template_name -> output_path
    template_mappings = {
        "server.py.template": f"src/{variables['package_name']}/server.py",
        "mcp__init__.py.template": f"src/{variables['package_name']}/mcp/__init__.py",
        "package__init__.py.template": f"src/{variables['package_name']}/__init__.py",
        "pyproject.toml.template": "pyproject.toml",
        "README_TEMPLATE.md": "README.md",
        "AGENTS.md.template": "AGENTS.md",
        "CLAUDE.md.template": "CLAUDE.md",
        "CHANGELOG.md.template": "CHANGELOG.md",
        "ROADMAP.md.template": "ROADMAP.md",
        ".env.example.template": ".env.example",
        ".gitignore.template": ".gitignore",
        "justfile.template": "justfile",
        "bump-version.py.template": "scripts/bump-version.py",
        "create-release.py.template": "scripts/create-release.py",
        "how-to-create-release.md.template": "docs/user-docs/how-to-create-release.md",
    }

    print("\nRendering templates...")
    for template_name, output_path in template_mappings.items():
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
                print(f"  ✓ Rendered {output_path}")

        except Exception as e:
            print(f"  ❌ Error rendering {template_name}: {e}")
            sys.exit(1)


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

This directory implements SAP-001 (Inbox Protocol) for coordinating work across
repositories and agents.

## Structure

- `coordination/active.jsonl` - Active coordination requests
- `coordination/archived.jsonl` - Completed/rejected requests
- `coordination/events.jsonl` - Event log
- `examples/` - Example coordination patterns

## Usage

See [SAP-001 documentation](docs/skilled-awareness/inbox/) for details.

**Project**: {variables['project_name']}
**Initialized**: {datetime.utcnow().date().isoformat()}
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
    """Validate the generated project meets model citizen requirements."""
    print("\nValidating generated project...")

    checks = []

    # Check 1: FastMCP server exists
    server_path = output_dir / f"src/{variables['package_name']}/server.py"
    checks.append(("FastMCP server exists", server_path.exists()))

    # Check 2: MCP namespace module exists
    mcp_init = output_dir / f"src/{variables['package_name']}/mcp/__init__.py"
    checks.append(("MCP namespace module exists", mcp_init.exists()))

    # Check 3: AGENTS.md exists with frontmatter
    agents_md = output_dir / "AGENTS.md"
    agents_exists = agents_md.exists()
    has_frontmatter = False
    if agents_exists:
        content = agents_md.read_text()
        has_frontmatter = content.startswith("---")
    checks.append(("AGENTS.md with frontmatter", agents_exists and has_frontmatter))

    # Check 4: CLAUDE.md exists
    checks.append(("CLAUDE.md exists", (output_dir / "CLAUDE.md").exists()))

    # Check 5: pyproject.toml exists
    checks.append(("pyproject.toml exists", (output_dir / "pyproject.toml").exists()))

    # Check 6: Tests directory exists
    checks.append(("tests/ directory exists", (output_dir / "tests").exists()))

    # Check 7: Documentation structure
    checks.append(("Documentation structure", (output_dir / "docs" / "user-docs").exists()))

    # Check 8: Beads initialized (if enabled)
    if variables.get('include_beads'):
        beads_check = (output_dir / ".beads" / "issues.jsonl").exists()
        checks.append(("Beads initialized (.beads/issues.jsonl)", beads_check))

    # Check 9: Inbox initialized (if enabled)
    if variables.get('include_inbox'):
        inbox_check = (output_dir / "inbox" / "coordination" / "active.jsonl").exists()
        checks.append(("Inbox initialized (inbox/coordination/active.jsonl)", inbox_check))

    # Check 10: Memory initialized (if enabled)
    if variables.get('include_memory'):
        memory_check = (output_dir / ".chora" / "memory" / "events" / "development.jsonl").exists()
        checks.append(("Memory initialized (.chora/memory/events/development.jsonl)", memory_check))

    # Check 11: Git repository
    checks.append(("Git repository initialized", (output_dir / ".git").exists()))

    # Check 12: No unsubstituted template variables
    unsubstituted_files = []
    for py_file in output_dir.rglob("*.py"):
        content = py_file.read_text()
        if '{{' in content or '}}' in content:
            unsubstituted_files.append(str(py_file.relative_to(output_dir)))
    checks.append(("No unsubstituted variables", len(unsubstituted_files) == 0))

    # Print results
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
        description="Create a model citizen MCP server with chora-base infrastructure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Required arguments
    parser.add_argument(
        "--name",
        required=True,
        help="Project name (e.g., 'Weather MCP Server')",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output directory for the new project",
    )

    # MCP-specific arguments
    parser.add_argument(
        "--namespace",
        help="MCP namespace (3-20 chars, lowercase, alphanumeric). If not provided, derived from name.",
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
        default="standard",
        help="Decision profile (default: standard)",
    )
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
    print(f"Create Model Citizen MCP Server v{VERSION}")
    print(f"Chora-Base v{CHORA_BASE_VERSION}")
    print("=" * 80)
    print()

    # Validate chora-base directory
    if not args.chora_base_dir.exists():
        print(f"❌ Error: chora-base directory not found: {args.chora_base_dir}")
        sys.exit(1)

    template_dir = args.chora_base_dir / "static-template" / "mcp-templates"
    if not template_dir.exists():
        print(f"❌ Error: Template directory not found: {template_dir}")
        print("   Make sure you're running from chora-base directory")
        sys.exit(1)

    # Load decision profile
    profile_config = DEFAULT_CONFIG.copy()
    if args.profile in DECISION_PROFILES:
        profile_config.update(DECISION_PROFILES[args.profile].get("config", {}))
        print(f"📋 Using profile: {args.profile}")
        print(f"   {DECISION_PROFILES[args.profile]['description']}")
        print()

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
        "project_name": args.name,
        "project_slug": project_slug,
        "package_name": package_name,
        "mcp_namespace": mcp_namespace,
        "project_description": args.description or derive_description(args.name, mcp_namespace),
        "author_name": author_name,
        "author_email": author_email,
        "github_username": github_username,
        "github_org": github_username,  # Default to same as username
        **profile_config,
    }

    # Print summary
    print("\n📦 Project Configuration")
    print("─" * 80)
    print(f"  Project Name:     {variables['project_name']}")
    print(f"  Project Slug:     {variables['project_slug']}")
    print(f"  Package Name:     {variables['package_name']}")
    print(f"  MCP Namespace:    {variables['mcp_namespace']}")
    print(f"  Description:      {variables['project_description']}")
    print(f"  Author:           {variables['author_name']} <{variables['author_email']}>")
    print(f"  GitHub:           {variables['github_username']}")
    print(f"  Python Version:   {variables['python_version']}")
    print(f"  License:          {variables['license']}")
    print(f"  Profile:          {args.profile}")
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
    print("✅ Model Citizen MCP Server Created Successfully!")
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
    print("5. Configure Claude Desktop:")
    print(f'''   Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
   {{
     "mcpServers": {{
       "{project_slug}": {{
         "command": "python",
         "args": ["-m", "{package_name}.server"],
         "cwd": "{args.output.absolute()}"
       }}
     }}
   }}
''')
    print()
    print("📚 Documentation:")
    print(f"   README:     {args.output}/README.md")
    print(f"   AGENTS.md:  {args.output}/AGENTS.md")
    print(f"   CLAUDE.md:  {args.output}/CLAUDE.md")
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
