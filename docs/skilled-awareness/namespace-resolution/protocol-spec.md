# Protocol Specification: Namespace Resolution & Ontology Navigation

**Capability ID**: SAP-049
**Modern Namespace**: chora.awareness.namespace_resolution
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This document specifies the complete protocol for resolving legacy SAP-XXX identifiers to modern `chora.domain.capability` namespaces and navigating the ecosystem ontology. It defines the alias mapping format, REST API contracts, resolution algorithms, and deprecation timeline.

**Protocol Goals**:
- **Backward Compatibility**: 100% resolution of legacy SAP-XXX identifiers (45 total)
- **Deprecation Awareness**: Clear warnings with days until sunset (2026-06-01)
- **Performance**: <50ms resolution latency
- **Reliability**: 99.9% availability during 6-month transition period
- **Migration Support**: Automated guidance for updating references

---

## Alias Mapping Format

### File Location

**Path**: `capabilities/alias-mapping.json`

**Format**: JSON

**Encoding**: UTF-8

---

### Schema

```json
{
  "version": "string (semver)",
  "updated": "string (ISO 8601 date)",
  "sunset_date": "string (ISO 8601 date)",
  "description": "string",
  "total_aliases": "integer",
  "aliases": {
    "SAP-XXX": {
      "namespace": "string (chora.domain.capability)",
      "status": "string (deprecated | active)",
      "sunset_date": "string (ISO 8601 date)",
      "notes": "string (optional)"
    }
  }
}
```

---

### Example

```json
{
  "version": "1.0.0",
  "updated": "2025-11-15",
  "sunset_date": "2026-06-01",
  "description": "Machine-readable mapping of legacy SAP-XXX identifiers to modern chora.domain.capability namespaces",
  "total_aliases": 45,
  "aliases": {
    "SAP-000": {
      "namespace": "chora.infrastructure.sap_framework",
      "status": "deprecated",
      "sunset_date": "2026-06-01",
      "notes": "Core SAP framework"
    },
    "SAP-001": {
      "namespace": "chora.infrastructure.inbox",
      "status": "deprecated",
      "sunset_date": "2026-06-01",
      "notes": "Inbox coordination protocol"
    },
    "SAP-015": {
      "namespace": "chora.awareness.task_tracking",
      "status": "deprecated",
      "sunset_date": "2026-06-01",
      "notes": "Task tracking with beads"
    }
  }
}
```

---

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | String | Yes | Semver version of mapping file (e.g., "1.0.0") |
| `updated` | String | Yes | Last update date (ISO 8601: YYYY-MM-DD) |
| `sunset_date` | String | Yes | Date when legacy identifiers stop working |
| `description` | String | Yes | Brief description of mapping purpose |
| `total_aliases` | Integer | Yes | Total number of aliases (must match count) |
| `aliases` | Object | Yes | Map of SAP-XXX → metadata |
| `aliases[SAP-XXX].namespace` | String | Yes | Modern namespace (chora.domain.capability) |
| `aliases[SAP-XXX].status` | String | Yes | "deprecated" or "active" |
| `aliases[SAP-XXX].sunset_date` | String | Yes | Same as root sunset_date (or custom) |
| `aliases[SAP-XXX].notes` | String | No | Optional description or migration notes |

---

## REST API Specification

### Base URL

**Development**: `http://localhost:8001`

**Production**: TBD (future deployment)

---

### Endpoints

#### 1. Resolve Alias (JSON)

**Endpoint**: `GET /api/v1/resolve/{sap_id}`

**Description**: Resolve legacy SAP-XXX identifier to modern namespace with deprecation info

**Path Parameters**:
- `sap_id` (string, required): Legacy identifier (e.g., "SAP-015" or "015")

**Response** (200 OK):
```json
{
  "sap_id": "SAP-015",
  "namespace": "chora.awareness.task_tracking",
  "deprecated": true,
  "sunset_date": "2026-06-01",
  "days_until_sunset": 197,
  "deprecation_warning": "This identifier is deprecated and will stop working on 2026-06-01 (197 days). Please use 'chora.awareness.task_tracking' instead.",
  "docs_url": "https://github.com/chora-base/docs/skilled-awareness/task-tracking",
  "migration_guide": "Update all references from SAP-015 to chora.awareness.task_tracking"
}
```

**Response** (404 Not Found):
```json
{
  "error": "not_found",
  "message": "SAP-XXX not found in alias mapping",
  "sap_id": "SAP-999"
}
```

**Example Request**:
```bash
curl http://localhost:8001/api/v1/resolve/SAP-015
```

**Example Response**:
```json
{
  "sap_id": "SAP-015",
  "namespace": "chora.awareness.task_tracking",
  "deprecated": true,
  "sunset_date": "2026-06-01",
  "days_until_sunset": 197,
  "deprecation_warning": "This identifier is deprecated and will stop working on 2026-06-01 (197 days). Please use 'chora.awareness.task_tracking' instead.",
  "docs_url": "https://github.com/chora-base/docs/skilled-awareness/task-tracking"
}
```

---

#### 2. HTTP Redirect (Browser)

**Endpoint**: `GET /{sap_id}`

**Description**: HTTP 301 redirect to capability documentation with deprecation headers

**Path Parameters**:
- `sap_id` (string, required): Legacy identifier (e.g., "SAP-015" or "015")

**Response** (301 Moved Permanently):
```
HTTP/1.1 301 Moved Permanently
Location: https://github.com/chora-base/docs/skilled-awareness/task-tracking
X-Deprecated: true
X-Sunset-Date: 2026-06-01
X-Modern-Namespace: chora.awareness.task_tracking
X-Days-Until-Sunset: 197
```

**Response** (404 Not Found):
```
HTTP/1.1 404 Not Found
Content-Type: text/html

<html>
  <body>
    <h1>SAP-XXX Not Found</h1>
    <p>The identifier SAP-999 was not found in the alias mapping.</p>
  </body>
</html>
```

**Example Request**:
```bash
curl -I http://localhost:8001/SAP-015
```

**Example Response**:
```
HTTP/1.1 301 Moved Permanently
Location: https://github.com/chora-base/docs/skilled-awareness/task-tracking
X-Deprecated: true
X-Sunset-Date: 2026-06-01
X-Modern-Namespace: chora.awareness.task_tracking
```

---

#### 3. List All Aliases

**Endpoint**: `GET /api/v1/aliases`

**Description**: List all SAP-XXX → modern namespace mappings

**Response** (200 OK):
```json
{
  "version": "1.0.0",
  "total": 45,
  "sunset_date": "2026-06-01",
  "aliases": [
    {
      "sap_id": "SAP-000",
      "namespace": "chora.infrastructure.sap_framework",
      "status": "deprecated"
    },
    {
      "sap_id": "SAP-001",
      "namespace": "chora.infrastructure.inbox",
      "status": "deprecated"
    }
  ]
}
```

**Example Request**:
```bash
curl http://localhost:8001/api/v1/aliases
```

---

#### 4. Health Check

**Endpoint**: `GET /health`

**Description**: Service health check

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "alias-redirect",
  "version": "1.0.0",
  "aliases_loaded": 45,
  "uptime_seconds": 3600
}
```

---

## Resolution Algorithm

### Input Normalization

**Goal**: Accept multiple input formats (SAP-015, sap-015, 015, SAP015)

**Algorithm**:
```python
def normalize_sap_id(input_id: str) -> str:
    """
    Normalize SAP identifier to standard format (SAP-XXX)

    Args:
        input_id: User input (e.g., "SAP-015", "sap-015", "015", "SAP015")

    Returns:
        Normalized SAP ID (e.g., "SAP-015")
    """
    # Remove whitespace
    input_id = input_id.strip()

    # Convert to uppercase
    input_id = input_id.upper()

    # Extract number
    import re
    match = re.search(r'(\d+)', input_id)

    if not match:
        raise ValueError(f"Invalid SAP ID: {input_id}")

    number = match.group(1)

    # Zero-pad to 3 digits
    number = number.zfill(3)

    # Return standard format
    return f"SAP-{number}"

# Examples
assert normalize_sap_id("SAP-015") == "SAP-015"
assert normalize_sap_id("sap-15") == "SAP-015"
assert normalize_sap_id("15") == "SAP-015"
assert normalize_sap_id("SAP015") == "SAP-015"
```

---

### Alias Lookup

**Goal**: Resolve normalized SAP-XXX to modern namespace

**Algorithm**:
```python
import json
from datetime import datetime, date

def resolve_alias(sap_id: str) -> dict:
    """
    Resolve SAP-XXX to modern namespace with deprecation info

    Args:
        sap_id: Normalized SAP ID (e.g., "SAP-015")

    Returns:
        dict with namespace, deprecated, days_until_sunset, etc.

    Raises:
        KeyError: If SAP-XXX not found in mapping
    """
    # Load alias mapping
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    # Lookup alias
    if sap_id not in mapping['aliases']:
        raise KeyError(f"SAP-XXX not found: {sap_id}")

    alias_info = mapping['aliases'][sap_id]

    # Calculate days until sunset
    sunset_date_str = alias_info.get('sunset_date', mapping['sunset_date'])
    sunset_date = datetime.strptime(sunset_date_str, '%Y-%m-%d').date()
    today = date.today()
    days_until_sunset = (sunset_date - today).days

    # Build response
    result = {
        'sap_id': sap_id,
        'namespace': alias_info['namespace'],
        'deprecated': alias_info['status'] == 'deprecated',
        'sunset_date': sunset_date_str,
        'days_until_sunset': max(0, days_until_sunset),
        'deprecation_warning': None,
        'docs_url': None,
    }

    # Generate deprecation warning
    if result['deprecated']:
        if days_until_sunset > 0:
            result['deprecation_warning'] = (
                f"This identifier is deprecated and will stop working on {sunset_date_str} "
                f"({days_until_sunset} days). Please use '{alias_info['namespace']}' instead."
            )
        else:
            result['deprecation_warning'] = (
                f"This identifier was deprecated on {sunset_date_str} and no longer works. "
                f"Please use '{alias_info['namespace']}' instead."
            )

    # Generate docs URL (simple conversion)
    # chora.awareness.task_tracking → docs/skilled-awareness/task-tracking
    namespace_parts = alias_info['namespace'].split('.')
    if len(namespace_parts) >= 3:
        capability_name = namespace_parts[2].replace('_', '-')
        result['docs_url'] = f"https://github.com/chora-base/docs/skilled-awareness/{capability_name}"

    return result
```

---

### Caching Strategy

**Goal**: Reduce API load and improve performance

**Algorithm**:
```python
import time
from functools import lru_cache

class AliasResolver:
    """Alias resolver with caching (60s TTL)"""

    def __init__(self):
        self._cache_time = {}

    @lru_cache(maxsize=128)
    def _resolve_cached(self, sap_id: str, cache_key: int) -> dict:
        """Internal cached resolver"""
        return resolve_alias(sap_id)

    def resolve(self, sap_id: str) -> dict:
        """
        Resolve SAP-XXX with caching (60s TTL)

        Args:
            sap_id: Normalized SAP ID

        Returns:
            Resolution result (cached)
        """
        # Cache key based on current minute (60s buckets)
        cache_key = int(time.time() / 60)

        # Resolve (cached)
        return self._resolve_cached(sap_id, cache_key)
```

---

## Deprecation Timeline

### Transition Period

**Start Date**: 2025-11-15 (ontology migration complete)

**Sunset Date**: 2026-06-01 (6 months)

**Total Duration**: 197 days (as of 2025-11-16)

---

### Warning Escalation

| Period | Days Remaining | Warning Level | Behavior |
|--------|----------------|---------------|----------|
| 6-3 months | 197-90 | Info | Log deprecation notice, continue operation |
| 3-1 month | 90-30 | Warning | Show yellow warning in CLI/UI, continue operation |
| <1 month | <30 | Error | Show red error in CLI/UI, continue operation with loud warning |
| Post-sunset | <0 | Fatal | Return HTTP 410 Gone, refuse to resolve |

---

### Example Warning Messages

**6-3 months (Info)**:
```
ℹ️ SAP-015 is deprecated. Please use 'chora.awareness.task_tracking' instead.
   Sunset: 2026-06-01 (197 days remaining)
```

**3-1 month (Warning)**:
```
⚠️ SAP-015 is deprecated and will stop working on 2026-06-01 (45 days).
   Please update to 'chora.awareness.task_tracking' immediately.
```

**<1 month (Error)**:
```
🚨 SAP-015 is deprecated and will stop working in 15 days (2026-06-01)!
   All references MUST be updated to 'chora.awareness.task_tracking'.
   See migration guide: https://github.com/chora-base/docs/ontology/MIGRATION.md
```

**Post-sunset (Fatal)**:
```
❌ SAP-015 is no longer supported (deprecated 2026-06-01).
   Use 'chora.awareness.task_tracking' instead.
   See migration guide: https://github.com/chora-base/docs/ontology/MIGRATION.md
```

---

## Ontology Navigation Patterns

### Domain Extraction

**Goal**: Extract domain from modern namespace

**Algorithm**:
```python
def extract_domain(namespace: str) -> str:
    """
    Extract domain from modern namespace

    Args:
        namespace: Modern namespace (e.g., "chora.devex.registry")

    Returns:
        Domain name (e.g., "devex")

    Raises:
        ValueError: If namespace format invalid
    """
    parts = namespace.split('.')

    if len(parts) < 3 or parts[0] != 'chora':
        raise ValueError(f"Invalid namespace format: {namespace}")

    return parts[1]

# Examples
assert extract_domain("chora.devex.registry") == "devex"
assert extract_domain("chora.awareness.task_tracking") == "awareness"
assert extract_domain("chora.infrastructure.sap_framework") == "infrastructure"
```

---

### Capability Discovery by Domain

**Goal**: Find all capabilities in a given domain

**Algorithm**:
```python
def find_capabilities_by_domain(domain: str) -> list:
    """
    Find all capabilities in a given domain

    Args:
        domain: Domain name (e.g., "devex", "awareness")

    Returns:
        List of capability dicts with sap_id, namespace, domain
    """
    import json
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    capabilities = []

    for sap_id, info in mapping['aliases'].items():
        namespace = info['namespace']

        try:
            cap_domain = extract_domain(namespace)
        except ValueError:
            continue

        if cap_domain == domain:
            capabilities.append({
                'sap_id': sap_id,
                'namespace': namespace,
                'domain': cap_domain,
                'status': info['status']
            })

    return sorted(capabilities, key=lambda c: c['namespace'])

# Example usage
devex_caps = find_capabilities_by_domain('devex')
print(f"Found {len(devex_caps)} capabilities in 'devex' domain")
for cap in devex_caps:
    print(f"  - {cap['namespace']} (legacy: {cap['sap_id']})")
```

---

### Reverse Lookup (Namespace → SAP-XXX)

**Goal**: Find legacy SAP-XXX identifier for a given modern namespace

**Algorithm**:
```python
def reverse_lookup(namespace: str) -> str:
    """
    Find legacy SAP-XXX identifier for a modern namespace

    Args:
        namespace: Modern namespace (e.g., "chora.awareness.task_tracking")

    Returns:
        Legacy SAP-XXX identifier (e.g., "SAP-015")

    Raises:
        KeyError: If namespace not found
    """
    import json
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    for sap_id, info in mapping['aliases'].items():
        if info['namespace'] == namespace:
            return sap_id

    raise KeyError(f"Namespace not found: {namespace}")

# Examples
assert reverse_lookup("chora.awareness.task_tracking") == "SAP-015"
assert reverse_lookup("chora.infrastructure.inbox") == "SAP-001"
```

---

## Client Libraries

### Python

**Installation**: No external dependencies (uses `requests` for REST API)

**Basic Usage**:
```python
import requests

class AliasResolver:
    """Client for alias resolution API"""

    def __init__(self, base_url='http://localhost:8001'):
        self.base_url = base_url

    def resolve(self, sap_id: str) -> dict:
        """Resolve SAP-XXX to modern namespace"""
        response = requests.get(f"{self.base_url}/api/v1/resolve/{sap_id}")

        if response.status_code == 404:
            return None

        return response.json()

    def list_aliases(self) -> list:
        """List all aliases"""
        response = requests.get(f"{self.base_url}/api/v1/aliases")
        result = response.json()
        return result['aliases']

# Usage
resolver = AliasResolver()
result = resolver.resolve('SAP-015')
print(f"{result['sap_id']} → {result['namespace']}")
print(f"Warning: {result['deprecation_warning']}")
```

---

### Bash

**Using curl**:
```bash
# Resolve alias
curl http://localhost:8001/api/v1/resolve/SAP-015

# List all aliases
curl http://localhost:8001/api/v1/aliases

# Check service health
curl http://localhost:8001/health

# Follow redirect (browser-like)
curl -L http://localhost:8001/SAP-015
```

---

### JavaScript/Node.js

**Installation**: No external dependencies (uses `fetch`)

**Basic Usage**:
```javascript
class AliasResolver {
  constructor(baseUrl = 'http://localhost:8001') {
    this.baseUrl = baseUrl;
  }

  async resolve(sapId) {
    const response = await fetch(`${this.baseUrl}/api/v1/resolve/${sapId}`);

    if (response.status === 404) {
      return null;
    }

    return await response.json();
  }

  async listAliases() {
    const response = await fetch(`${this.baseUrl}/api/v1/aliases`);
    const result = await response.json();
    return result.aliases;
  }
}

// Usage
const resolver = new AliasResolver();
const result = await resolver.resolve('SAP-015');
console.log(`${result.sap_id} → ${result.namespace}`);
console.log(`Warning: ${result.deprecation_warning}`);
```

---

## Error Handling

### SAP-XXX Not Found

**HTTP Status**: 404 Not Found

**Response**:
```json
{
  "error": "not_found",
  "message": "SAP-XXX not found in alias mapping",
  "sap_id": "SAP-999"
}
```

**Client Handling**:
```python
result = resolver.resolve('SAP-999')
if result is None:
    print(f"Error: SAP-999 not found")
```

---

### Invalid SAP-XXX Format

**HTTP Status**: 400 Bad Request

**Response**:
```json
{
  "error": "invalid_format",
  "message": "Invalid SAP-XXX format. Expected: SAP-XXX (e.g., SAP-015)",
  "input": "SAPXXX"
}
```

---

### Service Unavailable

**HTTP Status**: 503 Service Unavailable

**Response**:
```json
{
  "error": "service_unavailable",
  "message": "Alias redirect service is temporarily unavailable. Please try again later."
}
```

**Fallback**:
```python
def resolve_with_fallback(sap_id: str) -> dict:
    """Resolve with fallback to local file if service unavailable"""
    try:
        # Try API first
        return resolver.resolve(sap_id)
    except requests.exceptions.ConnectionError:
        # Fallback to local file
        import json
        with open('capabilities/alias-mapping.json', 'r') as f:
            mapping = json.load(f)

        if sap_id in mapping['aliases']:
            return {
                'sap_id': sap_id,
                'namespace': mapping['aliases'][sap_id]['namespace'],
                'deprecated': True,
                'note': 'Resolved from local fallback (service unavailable)'
            }

        return None
```

---

## Performance Characteristics

### API Response Time

**Target**: <50ms for alias resolution

**Benchmark** (local service):
- **Alias resolution**: ~10ms
- **List all aliases**: ~20ms
- **Health check**: ~5ms

---

### Caching Performance

**Client-Side Cache**: 60s TTL (reduces API calls by ~90%)

**Server-Side Cache**: In-memory alias mapping (no disk I/O)

---

### Throughput

**Target**: 1,000 requests/sec

**Benchmark** (local service):
- **Resolve API**: ~1,500 req/sec
- **List API**: ~800 req/sec

---

## Security Considerations

### No Authentication (Development)

**Current**: Service runs without authentication on localhost:8001

**Production Recommendation**: Add API key or OAuth for public deployment

---

### Rate Limiting

**Current**: None (development)

**Production Recommendation**: 100 requests/minute per IP

---

### CORS

**Current**: CORS enabled for all origins (development)

**Production Recommendation**: Restrict to allowed domains

---

## Versioning and Compatibility

### Protocol Version

**Current**: 1.0.0

**Versioning Scheme**: Semantic Versioning 2.0.0

---

### Backward Compatibility Guarantees

**Guaranteed**:
- Alias mappings will remain stable until sunset (2026-06-01)
- REST API contracts will not change (breaking changes require major version bump)
- Deprecation warnings will escalate predictably based on timeline

**Not Guaranteed**:
- Performance characteristics may improve
- Internal implementation may change
- Sunset date may be extended (but never shortened)

---

## References

- [Alias Mapping File](../../../capabilities/alias-mapping.json) - Machine-readable mappings
- [Alias Redirect Service](../../../services/alias-redirect/app.py) - FastAPI implementation
- [SAP Namespace Reference](../../../docs/ontology/SAP-NAMESPACE-REFERENCE.md) - Human-readable table
- [Ontology Migration Complete](../../../docs/ontology/ONTOLOGY-MIGRATION-COMPLETE.md) - Migration summary

---

**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Status**: Draft
**Next Review**: After initial agent adoption (2 weeks)
