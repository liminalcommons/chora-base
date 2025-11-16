# Capability Charter: Namespace Resolution & Ontology Navigation

**Capability ID**: SAP-049
**Modern Namespace**: chora.awareness.namespace_resolution
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Created**: 2025-11-16
**Last Updated**: 2025-11-16

---

## Executive Summary

**SAP-049: Namespace Resolution & Ontology Navigation** formalizes agent awareness patterns for resolving legacy SAP-XXX identifiers to modern `chora.domain.capability` namespaces and navigating the ecosystem ontology. It provides standardized patterns for backward compatibility, alias resolution, and ontology exploration during the 6-month transition period (sunset: 2026-06-01).

**Key Benefits**:
- 🔄 **Backward Compatibility**: Seamlessly resolve legacy SAP-XXX identifiers to modern namespaces
- 🗺️ **Ontology Navigation**: Understand relationships between capabilities across domains
- ⚠️ **Deprecation Awareness**: Detect and warn about deprecated identifiers
- 🔍 **Discovery**: Find capabilities by domain, type, or legacy identifier
- 📊 **Migration Support**: Track transition progress and guide users to modern namespaces

---

## Problem Statement

### Current Challenges

The ecosystem ontology migration (completed 2025-11-15) introduced modern `chora.domain.capability` namespaces to replace legacy `SAP-XXX` identifiers. However, without standardized resolution patterns, agents face:

1. **Identifier Confusion**: Users still reference capabilities by legacy SAP-XXX identifiers (e.g., "SAP-015" instead of "chora.awareness.task_tracking")
2. **No Automatic Resolution**: Agents must manually map SAP-XXX → modern namespace, leading to errors
3. **Missing Deprecation Warnings**: Users unaware that legacy identifiers are deprecated (sunset: 2026-06-01)
4. **Ontology Navigation Gaps**: No standardized way to explore capability relationships across domains
5. **Migration Friction**: Users struggle to find equivalent modern namespaces for legacy references

### Business Impact

- **Reduced Agent Effectiveness**: Agents fail when users provide legacy identifiers
- **Poor User Experience**: Users must manually convert SAP-XXX to modern namespaces
- **Missed Migration Deadlines**: Users unaware of 6-month transition timeline
- **Documentation Confusion**: Mixed use of legacy and modern identifiers in conversations
- **Integration Complexity**: Tools and scripts hardcoded with SAP-XXX identifiers break

### User Stories

**As an AI agent**, I want to:
- Automatically resolve "SAP-015" to "chora.awareness.task_tracking" when user mentions it
- Warn users that SAP-XXX identifiers are deprecated and provide modern equivalent
- Navigate the ontology to find related capabilities in other domains
- Suggest modern namespace when user asks about a legacy SAP

**As a developer**, I want:
- Agents to understand both legacy and modern identifiers during transition period
- Clear deprecation warnings with days until sunset (2026-06-01)
- Migration guides showing SAP-XXX → modern namespace mappings
- Tools to validate that all references have been updated

---

## Solution Design

### Approach

SAP-049 formalizes 4 core agent awareness patterns for namespace resolution:

1. **Alias Resolution Pattern**: Resolve SAP-XXX → modern namespace using alias mapping
2. **Deprecation Warning Pattern**: Detect legacy identifiers and warn users with sunset timeline
3. **Ontology Navigation Pattern**: Explore capability relationships across domains
4. **Migration Guide Pattern**: Provide conversion guidance and track progress

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent (Claude Code)                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ SAP-049 Patterns
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Alias Redirect Service (Port 8001)              │
│                                                              │
│  REST API:                                                   │
│    GET /api/v1/resolve/{sap_id}                              │
│      → {namespace, deprecated, days_until_sunset, ...}       │
│                                                              │
│    GET /{sap_id}                                             │
│      → HTTP 301 redirect to docs with deprecation headers   │
│                                                              │
│  Data Source: capabilities/alias-mapping.json                │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ Reads
                             ▼
┌─────────────────────────────────────────────────────────────┐
│          Alias Mapping (alias-mapping.json)                  │
│                                                              │
│  {                                                           │
│    "SAP-000": {                                              │
│      "namespace": "chora.infrastructure.sap_framework",      │
│      "status": "deprecated",                                 │
│      "sunset_date": "2026-06-01"                             │
│    },                                                        │
│    ...                                                       │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

### Core Patterns

**1. Alias Resolution Pattern**

Resolve legacy SAP-XXX identifier to modern namespace:

```python
import requests

def resolve_sap_id(sap_id: str) -> dict:
    """
    Resolve legacy SAP-XXX identifier to modern namespace

    Args:
        sap_id: Legacy identifier (e.g., "SAP-015" or "015")

    Returns:
        dict with namespace, deprecated status, days until sunset
    """
    # Normalize SAP ID
    if not sap_id.startswith("SAP-"):
        sap_id = f"SAP-{sap_id}"

    # Call alias redirect service
    response = requests.get(f"http://localhost:8001/api/v1/resolve/{sap_id}")

    if response.status_code == 404:
        return None

    result = response.json()

    return {
        'sap_id': result['sap_id'],
        'namespace': result['namespace'],
        'deprecated': result['deprecated'],
        'days_until_sunset': result['days_until_sunset'],
        'deprecation_warning': result['deprecation_warning'],
        'docs_url': result['docs_url'],
    }

# Example usage
result = resolve_sap_id("SAP-015")
print(f"SAP-015 → {result['namespace']}")
print(f"Deprecated: {result['deprecated']}")
print(f"Days until sunset: {result['days_until_sunset']}")
print(f"Warning: {result['deprecation_warning']}")

# Output:
# SAP-015 → chora.awareness.task_tracking
# Deprecated: True
# Days until sunset: 197
# Warning: This identifier is deprecated and will stop working on 2026-06-01 (197 days). Please use 'chora.awareness.task_tracking' instead.
```

**2. Deprecation Warning Pattern**

Detect legacy identifiers in user input and provide warnings:

```python
import re

def detect_and_warn_legacy_identifiers(user_input: str) -> list:
    """
    Detect SAP-XXX identifiers in user input and provide warnings

    Args:
        user_input: User's message or request

    Returns:
        List of warnings for each detected legacy identifier
    """
    # Regex to detect SAP-XXX pattern
    sap_pattern = r'SAP-(\d{3})'
    matches = re.findall(sap_pattern, user_input)

    warnings = []

    for match in matches:
        sap_id = f"SAP-{match}"
        result = resolve_sap_id(sap_id)

        if result and result['deprecated']:
            warnings.append({
                'sap_id': sap_id,
                'modern_namespace': result['namespace'],
                'days_until_sunset': result['days_until_sunset'],
                'warning': result['deprecation_warning']
            })

    return warnings

# Example usage
user_input = "I want to install SAP-015 and SAP-001 for task tracking"
warnings = detect_and_warn_legacy_identifiers(user_input)

for warning in warnings:
    print(f"⚠️ {warning['warning']}")

# Output:
# ⚠️ SAP-015 is deprecated and will stop working on 2026-06-01 (197 days). Please use 'chora.awareness.task_tracking' instead.
# ⚠️ SAP-001 is deprecated and will stop working on 2026-06-01 (197 days). Please use 'chora.infrastructure.inbox' instead.
```

**3. Ontology Navigation Pattern**

Explore capability relationships across domains:

```python
def get_capability_domain(namespace: str) -> str:
    """Extract domain from namespace"""
    parts = namespace.split('.')
    if len(parts) >= 2:
        return parts[1]  # e.g., "chora.devex.registry" → "devex"
    return None

def find_capabilities_by_domain(domain: str) -> list:
    """Find all capabilities in a given domain"""
    # Read alias mapping to get all namespaces
    import json
    with open('capabilities/alias-mapping.json', 'r') as f:
        alias_mapping = json.load(f)

    capabilities = []

    for sap_id, info in alias_mapping['aliases'].items():
        namespace = info['namespace']
        cap_domain = get_capability_domain(namespace)

        if cap_domain == domain:
            capabilities.append({
                'sap_id': sap_id,
                'namespace': namespace,
                'domain': cap_domain
            })

    return capabilities

# Example usage
devex_capabilities = find_capabilities_by_domain('devex')
print(f"Found {len(devex_capabilities)} capabilities in 'devex' domain:")
for cap in devex_capabilities:
    print(f"  - {cap['namespace']} (legacy: {cap['sap_id']})")

# Output:
# Found 14 capabilities in 'devex' domain:
#   - chora.devex.registry (legacy: SAP-047)
#   - chora.devex.documentation_framework (legacy: SAP-007)
#   ...
```

**4. Migration Guide Pattern**

Provide conversion guidance and track migration progress:

```python
def generate_migration_report() -> dict:
    """
    Generate migration report showing all SAP-XXX → modern namespace mappings

    Returns:
        dict with total, by_domain, and detailed mappings
    """
    import json
    with open('capabilities/alias-mapping.json', 'r') as f:
        alias_mapping = json.load(f)

    report = {
        'total_aliases': len(alias_mapping['aliases']),
        'sunset_date': alias_mapping.get('sunset_date', '2026-06-01'),
        'by_domain': {},
        'mappings': []
    }

    for sap_id, info in alias_mapping['aliases'].items():
        namespace = info['namespace']
        domain = get_capability_domain(namespace)

        # Count by domain
        if domain not in report['by_domain']:
            report['by_domain'][domain] = 0
        report['by_domain'][domain] += 1

        # Add to detailed mappings
        report['mappings'].append({
            'sap_id': sap_id,
            'namespace': namespace,
            'domain': domain,
            'status': info['status']
        })

    return report

# Example usage
report = generate_migration_report()
print(f"Migration Report:")
print(f"  Total aliases: {report['total_aliases']}")
print(f"  Sunset date: {report['sunset_date']}")
print(f"  By domain:")
for domain, count in sorted(report['by_domain'].items()):
    print(f"    - {domain}: {count} capabilities")
```

---

## Success Metrics

**Adoption Metrics**:
- Number of agents using SAP-049 patterns
- Number of alias resolutions per day
- Number of deprecation warnings shown per day
- Number of users migrating to modern namespaces

**Quality Metrics**:
- Alias resolution accuracy (100% target)
- Deprecation warning coverage (100% of legacy identifiers)
- Migration progress (% of references updated)
- User awareness of sunset date (% who see warning)

**Business Metrics**:
- Reduced agent failures due to legacy identifiers (from 20% to <5%)
- Increased modern namespace usage (from 50% to >90% by sunset)
- Faster migration adoption (users update references within 1 week of warning)
- Improved user satisfaction (clear guidance reduces frustration)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Alias mapping out of sync | High | Automated sync from capability manifests |
| Sunset date missed | Medium | Automated deprecation warnings in all tools |
| Users ignore warnings | Medium | Escalating warning severity (info → warning → error) |
| Alias redirect service down | High | Fallback to local alias-mapping.json file |
| Performance degradation | Low | Cache alias mappings client-side (60s TTL) |

---

## Integration Points

**Prerequisites**:
- **Alias mapping file**: [capabilities/alias-mapping.json](../../../capabilities/alias-mapping.json)
- **Alias redirect service**: FastAPI service on port 8001
- **SAP catalog**: [sap-catalog.json](../../../sap-catalog.json) for complete metadata

**Dependents**:
- **Claude Code agents**: Detect and resolve legacy identifiers automatically
- **Claude Desktop agents**: Provide migration guidance in conversations
- **CLI tools**: Support both legacy and modern identifiers during transition
- **Documentation tools**: Generate migration tables and reference guides

**Complements**:
- **SAP-048 (Registry Discovery)**: Query registry using resolved modern namespaces
- **SAP-000 (SAP Framework)**: Defines namespace format and ontology structure
- **SAP-009 (Agent Awareness)**: Updates AGENTS.md with resolution patterns

---

## Open Questions

1. **Escalation Strategy**: Should warnings escalate from info → warning → error as sunset approaches?
   - **Decision**: Yes - info (6-3 months), warning (3-1 month), error (<1 month)

2. **Fallback Behavior**: What happens after sunset (2026-06-01) when alias service stops?
   - **Decision**: Return HTTP 410 Gone with error message directing to modern namespace

3. **Caching Strategy**: Should agents cache alias mappings or always query service?
   - **Decision**: Cache for 60s (mappings rarely change, reduces API load)

4. **Legacy Identifier Support in APIs**: Should all APIs support both legacy and modern?
   - **Decision**: Yes during transition, modern-only after sunset

5. **Migration Progress Tracking**: Should we track which users have migrated?
   - **Decision**: Optional - log API requests to analyze usage patterns (privacy-respecting)

---

## References

- [Alias Mapping File](../../../capabilities/alias-mapping.json) - Machine-readable SAP-XXX → namespace mappings
- [Alias Redirect Service](../../../services/alias-redirect/app.py) - FastAPI REST API implementation
- [SAP Namespace Reference](../../../docs/ontology/SAP-NAMESPACE-REFERENCE.md) - Human-readable reference table
- [Ontology Migration Complete](../../../docs/ontology/ONTOLOGY-MIGRATION-COMPLETE.md) - Migration project summary
- [SAP-048: Registry Discovery](../capability-registry-discovery/protocol-spec.md) - Registry query patterns

---

**Version**: 1.0.0
**Status**: Draft
**Next Review**: After initial agent adoption (2 weeks)
