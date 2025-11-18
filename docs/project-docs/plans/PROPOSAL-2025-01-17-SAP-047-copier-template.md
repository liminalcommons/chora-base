# SAP-047 Enhancement Proposal: Copier-Based Template Implementation

**Status**: Proposed
**Created**: 2025-01-17
**Author**: Chora Workspace Team
**Related**: SAP-047 (Capability Server Template), SAP-045 (Startup Sequencing)

---

## Executive Summary

This proposal recommends implementing SAP-047 as a **Copier-based template** with integrated config loading patterns validated in chora-workspace. This approach enables both initial project generation and incremental template updates, critical for SAP pattern evolution.

**Key Benefits**:
- ✅ Template updates for existing capability servers
- ✅ Config loading pattern (v5.2.0 etcd integration)
- ✅ Standardized project structure with best practices
- ✅ Reduced time-to-production for new capability servers

---

## Background

### Current State (2025-01-17)

**SAP-047 Documentation**: ✅ Complete
- [protocol-spec.md](protocol-spec.md) - Comprehensive specification with config loading pattern (section 3.3)
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption guidelines
- [capability-charter.md](capability-charter.md) - Template charter

**Template Repository**: ❌ Empty
- `liminalcommons/chora-capability-server-template` exists but has no template files
- No project generation mechanism currently available

**Validated Patterns**: ✅ Tested in chora-workspace
- Config loading utilities (YAML-based, sensible defaults)
- CLI integration with `--config` option
- StartupSequence integration (SAP-045)
- Registry backend integration (v5.2.0 EtcdRegistryBackend)

**Reference Implementations**:
- `chora-workspace/packages/chora-gateway/` - Config loading pattern ✅
- `chora-workspace/packages/chora-orchestration/` - Config loading pattern ✅
- Test suite: `chora-workspace/test-config-loading.py` ✅

---

## Problem Statement

### Challenge 1: SAP Pattern Evolution

Capability servers need to adopt new SAP patterns over time:
- Config loading (v5.2.0 - etcd integration)
- Future infrastructure patterns (messaging, observability, etc.)
- Security enhancements
- Performance optimizations

**Current Limitation**: No mechanism to propagate template updates to existing capability servers.

### Challenge 2: Template Maintenance

Protocol-spec already uses `{{cookiecutter.variable}}` syntax, but:
- No actual template files exist
- No generation tool configured
- Inconsistency between spec and implementation

### Challenge 3: Adoption Friction

New capability servers require:
- Manual project structure setup
- Copy/paste from reference implementations
- 2-4 hours setup time
- Risk of missing patterns or misconfiguration

---

## Proposed Solution: Copier-Based Template

### Why Copier Over Cookiecutter?

| Feature | Cookiecutter | Copier | Decision |
|---------|-------------|--------|----------|
| **Template updates** | ❌ One-time only | ✅ `copier update` | **Critical for SAP evolution** |
| **Change tracking** | ❌ No tracking | ✅ `.copier-answers.yml` | Enables selective adoption |
| **Configuration** | JSON | YAML | More readable |
| **Validation** | Python hooks | Tasks + schema | Better UX |
| **Community** | Mature (20k⭐) | Growing (1.7k⭐) | Both acceptable |
| **Maintenance** | Active | Active | Both acceptable |

**Verdict**: **Copier** - Template updates are critical for SAP pattern propagation.

### Architecture

```
liminalcommons/chora-capability-server-template/
├── copier.yml                           # Template configuration
├── template/
│   ├── {{project_slug}}/
│   │   ├── src/
│   │   │   └── {{namespace}}/
│   │   │       └── {{project_slug}}/
│   │   │           ├── config/          # ← NEW: Config loading pattern
│   │   │           │   ├── __init__.py.jinja
│   │   │           │   └── loader.py.jinja
│   │   │           ├── core/
│   │   │           │   ├── __init__.py.jinja
│   │   │           │   ├── capability.py.jinja
│   │   │           │   ├── models.py.jinja
│   │   │           │   └── exceptions.py.jinja
│   │   │           ├── interfaces/
│   │   │           │   ├── __init__.py.jinja
│   │   │           │   ├── cli.py.jinja  # ← With --config option
│   │   │           │   ├── rest.py.jinja
│   │   │           │   └── mcp.py.jinja
│   │   │           ├── bootstrap/
│   │   │           │   ├── __init__.py.jinja
│   │   │           │   └── startup.py.jinja  # ← SAP-045 integration
│   │   │           └── registry/
│   │   │               ├── __init__.py.jinja
│   │   │               ├── client.py.jinja
│   │   │               └── heartbeat.py.jinja
│   │   ├── config/
│   │   │   └── config.yaml.jinja        # ← With etcd settings
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_config_loader.py.jinja
│   │   │   ├── test_capability.py.jinja
│   │   │   └── test_cli.py.jinja
│   │   ├── docs/
│   │   │   ├── README.md.jinja
│   │   │   └── AGENTS.md.jinja
│   │   ├── .gitignore.jinja
│   │   ├── pyproject.toml.jinja
│   │   ├── poetry.lock.jinja
│   │   └── README.md.jinja
│   └── .copier-answers.yml.jinja
├── tasks/
│   ├── post_gen.py                      # Post-generation tasks
│   └── validate.py                      # Pre-generation validation
├── README.md
└── .copier-answers.yml
```

---

## Implementation Details

### 1. Template Configuration (`copier.yml`)

```yaml
_templates_suffix: .jinja
_skip_if_exists:
  - "*.py"  # Don't overwrite user code
  - "tests/*"
  - "docs/*"

# Project metadata
project_name:
  type: str
  help: "Project name (e.g., 'Analytics Service')"
  validator: "{% if not project_name %}Required{% endif %}"

project_slug:
  type: str
  default: "{{ project_name.lower().replace(' ', '-').replace('_', '-') }}"
  help: "Project slug (for package naming)"
  validator: "{% if not project_slug.match('^[a-z][a-z0-9-]*$') %}Invalid slug format{% endif %}"

namespace:
  type: str
  default: "chora"
  help: "Python namespace"

project_description:
  type: str
  help: "Short project description"
  default: "{{ project_name }} capability server"

author_name:
  type: str
  help: "Author name"
  default: "Chora Team"

author_email:
  type: str
  help: "Author email"
  default: "team@liminalcommons.org"

# Python settings
python_version:
  type: str
  default: "3.11"
  choices:
    - "3.11"
    - "3.12"

# Feature flags
enable_saga:
  type: bool
  default: false
  help: "Enable SAP-046 (Saga orchestration)?"

enable_circuit_breaker:
  type: bool
  default: false
  help: "Enable SAP-046 (Circuit breaker)?"

enable_event_bus:
  type: bool
  default: false
  help: "Enable event bus integration?"

enable_mcp:
  type: bool
  default: true
  help: "Enable MCP server interface?"

# Registry settings (v5.2.0)
registry_enabled:
  type: bool
  default: true
  help: "Enable etcd registry backend?"

# Tasks (post-generation)
_tasks:
  - "git init"
  - "poetry install"
  - "poetry run pre-commit install"
  - "poetry run pytest --collect-only"  # Verify tests discoverable
```

### 2. Config Loader Template (`template/{{project_slug}}/src/{{namespace}}/{{project_slug}}/config/loader.py.jinja`)

```python
"""
Configuration loader for {{project_slug}}.

Loads runtime configuration from YAML file with sensible defaults.
"""

import yaml
from pathlib import Path
from typing import Dict, Optional


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config.yaml file. If None, uses default location
                    (config/config.yaml relative to package root).

    Returns:
        Configuration dictionary with all settings.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        yaml.YAMLError: If config file has invalid YAML syntax.

    Example:
        >>> config = load_config()
        >>> etcd_host = config['registry']['etcd_host']
        >>> print(f"Connecting to etcd at {etcd_host}")
    """
    if config_path is None:
        # Default: config/config.yaml relative to package root
        package_root = Path(__file__).parent.parent.parent.parent
        config_path = package_root / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Expected location: {config_path.absolute()}"
        )

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"Invalid YAML syntax in {config_path}: {e}"
        ) from e

    if config is None:
        config = {}

    return config


{% if registry_enabled %}
def get_registry_config(config: Dict) -> Dict:
    """
    Extract registry-specific configuration.

    Args:
        config: Full configuration dictionary.

    Returns:
        Registry configuration with etcd connection settings.
    """
    registry = config.get('registry', {})

    return {
        'enabled': registry.get('enabled', True),
        'etcd_host': registry.get('etcd_host', 'localhost'),
        'etcd_port': registry.get('etcd_port', 2379),
        'heartbeat_timeout': registry.get('heartbeat_timeout', 30),
        'heartbeat_interval': registry.get('heartbeat_interval', 30),
    }
{% endif %}


def get_http_config(config: Dict) -> Dict:
    """
    Extract HTTP server configuration.

    Args:
        config: Full configuration dictionary.

    Returns:
        HTTP server configuration settings.
    """
    http = config.get('http', {})

    return {
        'host': http.get('host', '0.0.0.0'),
        'port': http.get('port', 8080),
        'cors_enabled': http.get('cors_enabled', True),
    }


def get_capability_config(config: Dict) -> Dict:
    """
    Extract capability-specific configuration.

    Args:
        config: Full configuration dictionary.

    Returns:
        Capability configuration settings.
    """
    capability = config.get('capability', {})

    return {
        # Add capability-specific settings here
        'timeout': capability.get('timeout', 30),
        'max_workers': capability.get('max_workers', 4),
    }
```

### 3. Runtime Config Template (`template/{{project_slug}}/config/config.yaml.jinja`)

```yaml
# Runtime configuration for {{project_slug}}

service:
  name: "{{project_slug}}"
  port: 8080
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR

{% if registry_enabled %}
# Registry (v5.2.0+: Production EtcdRegistryBackend)
registry:
  enabled: true
  manifest_url: "http://manifest:8080"
  heartbeat_interval: 30  # seconds
  heartbeat_timeout: 30  # seconds
  # etcd connection (for chora-manifest EtcdRegistryBackend)
  etcd_host: "localhost"  # Use 'etcd1' inside Docker network
  etcd_port: 2379
  auto_discovery: true
{% endif %}

# HTTP server
http:
  host: "0.0.0.0"
  port: 8080
  cors_enabled: true

# Capability-specific settings
capability:
  timeout: 30
  max_workers: 4
  # Add your settings here

{% if enable_saga %}
# Saga orchestration (SAP-046)
saga:
  enabled: true
  database: "sqlite:///saga_state.db"
  # For production: "postgresql://user:pass@localhost:5432/dbname"
{% endif %}

{% if enable_event_bus %}
# Event bus
event_bus:
  backend: "redis"  # redis, nats, memory
  redis:
    host: "localhost"
    port: 6379
    db: 0
{% endif %}

# Logging
logging:
  level: "INFO"
  format: "json"
  output: "stdout"
```

### 4. CLI Template with Config Loading (`template/{{project_slug}}/src/{{namespace}}/{{project_slug}}/interfaces/cli.py.jinja`)

```python
"""CLI interface for {{project_slug}}."""

import click
import asyncio
from ..config.loader import load_config{% if registry_enabled %}, get_registry_config{% endif %}, get_http_config
{% if registry_enabled %}from ..bootstrap.startup import StartupSequence{% endif %}


@click.group()
@click.version_option()
def main():
    """{{project_description}}"""
    pass


@main.command()
@click.option("--config", default=None, help="Path to config.yaml file")
@click.option("--port", default=None, help="Port (overrides config)")
def serve(config: str, port: int):
    """Start {{project_slug}} server."""
    async def _serve():
        # Load configuration
        cfg = load_config(config)
        http_config = get_http_config(cfg)

        # Override port from CLI if provided
        if port is None:
            port = http_config.get('port', 8080)

        {% if registry_enabled %}
        # Initialize with StartupSequence
        startup = StartupSequence(cfg)
        await startup.initialize()

        # TODO: Start server with startup.capability
        {% else %}
        # TODO: Start server without registry integration
        {% endif %}

        click.echo(f"Starting {{project_slug}} server on port {port}...")

    asyncio.run(_serve())


@main.command()
@click.option("--config", default=None, help="Path to config.yaml file")
def health(config: str):
    """Check health status."""
    async def _health():
        # Load configuration
        cfg = load_config(config)

        # TODO: Implement health check

        click.echo("Status: healthy")

    asyncio.run(_health())


if __name__ == "__main__":
    main()
```

---

## Usage Examples

### Initial Project Generation

```bash
# Install copier
pip install copier

# Generate new capability server
copier copy gh:liminalcommons/chora-capability-server-template my-analytics-service

# Prompts:
# project_name: Analytics Service
# project_slug: analytics-service
# namespace: chora
# enable_saga: no
# enable_mcp: yes
# registry_enabled: yes

# Generated structure:
cd analytics-service
tree -L 3
# analytics-service/
# ├── src/
# │   └── chora/
# │       └── analytics_service/
# │           ├── config/           # ← Config loading pattern
# │           ├── core/
# │           ├── interfaces/
# │           ├── bootstrap/
# │           └── registry/
# ├── config/
# │   └── config.yaml              # ← Runtime config with etcd
# ├── tests/
# └── pyproject.toml

# Run tests
poetry install
poetry run pytest
```

### Template Updates (Critical Feature!)

```bash
# Scenario: Template adds new SAP pattern (e.g., observability)

# Update existing capability server from template
cd chora-gateway
copier update

# Copier shows diff of changes:
# - config/loader.py: Added get_observability_config()
# - config/config.yaml: Added observability section
# - pyproject.toml: Added prometheus dependency

# Accept/reject changes interactively
# Selective adoption of new patterns!
```

---

## Migration Path for Existing Capability Servers

### Phase 1: Generate from Template (New Projects)

**Timeline**: Q1 2025

1. Set up copier template in `chora-capability-server-template`
2. Validate generation with test project
3. Document in SAP-047 adoption-blueprint.md

**Success Criteria**:
- ✅ New capability server generated in <5 minutes
- ✅ All tests pass out-of-the-box
- ✅ Config loading pattern working
- ✅ Registry integration functional

### Phase 2: Retrospective Adoption (Existing Projects)

**Timeline**: Q2 2025

**Approach**: Use copier's update mechanism with existing projects:

```bash
# 1. Initialize copier tracking
cd chora-gateway
copier copy --force --data-file .copier-answers.yml \
  gh:liminalcommons/chora-capability-server-template .

# 2. Review changes, keep local customizations
git diff  # See what changed

# 3. Selectively commit template patterns
git add config/loader.py
git commit -m "adopt: SAP-047 config loading pattern"
```

**Projects to Migrate**:
1. chora-gateway (already has config loading ✅)
2. chora-orchestration (already has config loading ✅)
3. chora-manifest
4. chora-github
5. chora-n8n
6. Future capability servers

---

## Testing Strategy

### 1. Template Validation Tests

```python
# tests/test_template_generation.py
import pytest
from copier import run_copy

def test_minimal_generation():
    """Test template generation with minimal options."""
    run_copy(
        ".",
        "/tmp/test-capability",
        data={
            "project_name": "Test Service",
            "project_slug": "test-service",
            "namespace": "chora",
        },
        vcs_ref="HEAD",
    )

    # Verify structure
    assert Path("/tmp/test-capability/src/chora/test_service/config/loader.py").exists()
    assert Path("/tmp/test-capability/config/config.yaml").exists()

    # Verify generated code is valid Python
    subprocess.run(["python", "-m", "py_compile", "src/**/*.py"], check=True)

def test_all_features_enabled():
    """Test generation with all features enabled."""
    run_copy(
        ".",
        "/tmp/test-full",
        data={
            "project_name": "Full Featured",
            "enable_saga": True,
            "enable_circuit_breaker": True,
            "enable_event_bus": True,
        },
    )

    # Verify saga files generated
    assert Path("/tmp/test-full/src/chora/full_featured/saga/").exists()
```

### 2. Generated Project Tests

```bash
# After generation, verify:
poetry install              # Dependencies install
poetry run pytest           # Tests pass
poetry run mypy src/        # Type checking passes
poetry run ruff check src/  # Linting passes
```

### 3. Update Tests

```python
def test_template_update():
    """Test that template updates don't break existing projects."""
    # Generate v1
    run_copy(".", "/tmp/project", data={"project_name": "Test"})

    # Make local changes
    Path("/tmp/project/src/chora/test/custom.py").write_text("# Custom code")

    # Update to v2
    run_update("/tmp/project", data={})

    # Verify custom code preserved
    assert Path("/tmp/project/src/chora/test/custom.py").exists()
```

---

## Success Metrics

### Adoption Metrics

- **Generation Time**: New capability server in <5 minutes (vs 2-4 hours manual)
- **Test Coverage**: Generated projects have 80%+ test coverage
- **Pattern Consistency**: 100% of capability servers use config loading pattern
- **Update Adoption**: 80%+ of updates adopted within 1 sprint

### Quality Metrics

- **Build Success**: Generated projects build without errors
- **Test Pass Rate**: 100% of generated tests pass
- **Type Safety**: mypy passes with no errors
- **Linting**: ruff passes with no errors

### Developer Experience

- **Developer Satisfaction**: 8/10+ rating for template UX
- **Time to First PR**: <1 day for new capability server
- **Documentation Completeness**: All features documented with examples

---

## Risks and Mitigations

### Risk 1: Copier Learning Curve

**Impact**: Medium
**Likelihood**: Medium

**Mitigation**:
- Comprehensive documentation in adoption-blueprint.md
- Video walkthrough of generation and update process
- Template includes `.copier-answers.yml` examples

### Risk 2: Template Drift from Spec

**Impact**: High
**Likelihood**: Low

**Mitigation**:
- Automated tests compare generated code to protocol-spec
- CI/CD validates template on every commit
- Quarterly review of template vs spec alignment

### Risk 3: Breaking Changes in Updates

**Impact**: High
**Likelihood**: Medium

**Mitigation**:
- Semantic versioning for template
- Update notes for each template version
- Copier shows diff before applying changes
- Ability to skip/defer updates

---

## Implementation Roadmap

### Phase 1: Template Setup (2 weeks)

**Week 1**:
- [ ] Set up copier template structure
- [ ] Port config loading pattern from chora-workspace
- [ ] Create basic generation test
- [ ] Documentation: README.md, usage guide

**Week 2**:
- [ ] Add all template files (cli, rest, mcp, tests)
- [ ] Implement validation hooks
- [ ] Test generation with all feature flags
- [ ] Update SAP-047 adoption-blueprint.md

### Phase 2: Validation (1 week)

- [ ] Generate test capability server
- [ ] Run full test suite on generated project
- [ ] Validate against protocol-spec requirements
- [ ] Community feedback on generated structure

### Phase 3: Migration (2 weeks)

- [ ] Migrate chora-manifest to use config loading
- [ ] Migrate chora-github to use config loading
- [ ] Migrate chora-n8n to use config loading
- [ ] Document migration experience

### Phase 4: Production (Ongoing)

- [ ] Publish template to GitHub
- [ ] Update chora-base documentation
- [ ] Create video walkthrough
- [ ] Support new capability server creation

---

## References

### Prior Art

**Validated in chora-workspace**:
- [chora-gateway config loader](../../../../../../packages/chora-gateway/src/chora_gateway/config/loader.py)
- [chora-orchestration config loader](../../../../../../packages/chora-orchestration/src/chora_orchestration/config/loader.py)
- [Test suite](../../../../../../test-config-loading.py)

**SAP References**:
- [SAP-045: Startup Sequencing](../startup-sequencing/)
- [SAP-047: Protocol Spec](protocol-spec.md) - Section 3.3 (Config Loading Pattern)

**Copier Resources**:
- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier GitHub](https://github.com/copier-org/copier)

---

## Appendices

### Appendix A: Example `.copier-answers.yml`

```yaml
# Answers file for chora-analytics-service
# Generated by copier on 2025-01-17

_commit: abc123def456
_src_path: gh:liminalcommons/chora-capability-server-template

project_name: Analytics Service
project_slug: analytics-service
namespace: chora
project_description: Real-time analytics capability server
author_name: Chora Team
author_email: team@liminalcommons.org
python_version: '3.11'
enable_saga: false
enable_circuit_breaker: false
enable_event_bus: true
enable_mcp: true
registry_enabled: true
```

### Appendix B: Comparison with Cookiecutter

If the decision leans toward cookiecutter despite the update limitation:

**Cookiecutter Advantages**:
- More mature ecosystem (20k stars)
- Wider community familiarity
- More third-party templates to learn from

**Cookiecutter Disadvantages**:
- No template update mechanism (critical for SAP evolution)
- JSON configuration (less readable than YAML)
- No built-in task system (need post-gen hooks)

**Recommendation**: Still prefer Copier for template updates capability.

---

## Decision

**Status**: Awaiting approval

**Recommendation**: Proceed with Copier-based template implementation

**Next Action**: Set up template structure in `chora-capability-server-template` repository

---

**Document Version**: 1.0
**Last Updated**: 2025-01-17
**Related Files**:
- [protocol-spec.md](protocol-spec.md) - SAP-047 specification
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption guidelines
