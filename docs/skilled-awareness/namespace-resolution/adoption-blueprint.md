# Adoption Blueprint: Namespace Resolution & Ontology Navigation

**Capability ID**: SAP-049
**Modern Namespace**: chora.awareness.namespace_resolution
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Overview

This blueprint provides step-by-step guidance for adopting **SAP-049: Namespace Resolution & Ontology Navigation** patterns in your project.

**Adoption Time**: 15-30 minutes

**Prerequisites**:
- [alias-mapping.json](../../../capabilities/alias-mapping.json) available in project
- Python 3.9+ (for Python agents)
- Optional: Alias redirect service running on port 8001

---

## Adoption Checklist

- [ ] **Phase 1**: Setup (5-10 minutes)
  - [ ] Verify alias-mapping.json exists
  - [ ] (Optional) Start alias redirect service
  - [ ] Test alias resolution
- [ ] **Phase 2**: Agent Integration (5-10 minutes)
  - [ ] Install Python dependencies
  - [ ] Create resolution helper module
  - [ ] Test detection and resolution
- [ ] **Phase 3**: Validation (5-10 minutes)
  - [ ] Test all 45 alias resolutions
  - [ ] Verify deprecation warnings
  - [ ] Run integration tests

---

## Phase 1: Setup

### Step 1.1: Verify Alias Mapping File

**Commands**:
```bash
# Check file exists
ls capabilities/alias-mapping.json

# Validate JSON
python -c "import json; json.load(open('capabilities/alias-mapping.json')); print('Valid JSON')"

# Count aliases
python -c "import json; m=json.load(open('capabilities/alias-mapping.json')); print(f'Total aliases: {m[\"total_aliases\"]}')"
```

**Expected Output**:
```
Valid JSON
Total aliases: 45
```

---

### Step 1.2: (Optional) Start Alias Redirect Service

**Commands**:
```bash
# Navigate to service directory
cd services/alias-redirect

# Install dependencies
pip install fastapi uvicorn

# Start service
uvicorn app:app --port 8001

# In another terminal, test
curl http://localhost:8001/health
```

**Expected Output**:
```json
{
  "status": "healthy",
  "service": "alias-redirect",
  "version": "1.0.0",
  "aliases_loaded": 45
}
```

---

### Step 1.3: Test Alias Resolution

**Python Test**:
```python
# Test 1: API resolution (if service running)
import requests

try:
    response = requests.get("http://localhost:8001/api/v1/resolve/SAP-015", timeout=2)
    result = response.json()
    print(f"✓ API resolution works: {result['sap_id']} → {result['namespace']}")
except:
    print("✗ API not available (use local fallback)")

# Test 2: Local file resolution
import json
with open('capabilities/alias-mapping.json') as f:
    mapping = json.load(f)

if 'SAP-015' in mapping['aliases']:
    print(f"✓ Local resolution works: SAP-015 → {mapping['aliases']['SAP-015']['namespace']}")
```

---

## Phase 2: Agent Integration

### Step 2.1: Create Resolution Helper Module

**Create** `alias_resolver.py`:
```python
"""Alias resolution helper for legacy SAP-XXX identifiers"""

import json
import requests
from datetime import datetime, date
from typing import Optional

class AliasResolver:
    """Resolve legacy SAP-XXX identifiers to modern namespaces"""

    def __init__(self, api_url='http://localhost:8001', local_file='capabilities/alias-mapping.json'):
        self.api_url = api_url
        self.local_file = local_file
        self._cache = {}

    def resolve(self, sap_id: str) -> Optional[dict]:
        """
        Resolve SAP-XXX to modern namespace

        Args:
            sap_id: Legacy identifier (e.g., "SAP-015" or "015")

        Returns:
            dict with namespace, deprecated, days_until_sunset, warning
        """
        # Normalize
        sap_id = self._normalize(sap_id)

        # Try API first
        try:
            response = requests.get(f"{self.api_url}/api/v1/resolve/{sap_id}", timeout=2)
            if response.status_code == 200:
                return response.json()
        except:
            pass

        # Fallback to local file
        return self._resolve_local(sap_id)

    def _normalize(self, input_id: str) -> str:
        """Normalize to SAP-XXX format"""
        import re
        match = re.search(r'(\d+)', input_id.upper())
        if not match:
            raise ValueError(f"Invalid SAP ID: {input_id}")
        return f"SAP-{match.group(1).zfill(3)}"

    def _resolve_local(self, sap_id: str) -> Optional[dict]:
        """Resolve using local file"""
        with open(self.local_file) as f:
            mapping = json.load(f)

        if sap_id not in mapping['aliases']:
            return None

        alias_info = mapping['aliases'][sap_id]
        sunset_date = datetime.strptime(mapping['sunset_date'], '%Y-%m-%d').date()
        days_until_sunset = (sunset_date - date.today()).days

        warning = None
        if alias_info['status'] == 'deprecated' and days_until_sunset > 0:
            warning = (
                f"This identifier is deprecated and will stop working on {mapping['sunset_date']} "
                f"({days_until_sunset} days). Please use '{alias_info['namespace']}' instead."
            )

        return {
            'sap_id': sap_id,
            'namespace': alias_info['namespace'],
            'deprecated': alias_info['status'] == 'deprecated',
            'days_until_sunset': max(0, days_until_sunset),
            'deprecation_warning': warning,
            'source': 'local_fallback'
        }

# Example usage
resolver = AliasResolver()
result = resolver.resolve('SAP-015')
if result:
    print(f"{result['sap_id']} → {result['namespace']}")
    if result['deprecated']:
        print(f"⚠️ {result['deprecation_warning']}")
```

---

### Step 2.2: Test Detection and Resolution

**Create** `test_resolution.py`:
```python
#!/usr/bin/env python3
"""Test alias resolution"""

from alias_resolver import AliasResolver
import re

def test_resolution():
    """Test basic resolution"""
    print("Test 1: Basic resolution")
    resolver = AliasResolver()

    result = resolver.resolve('SAP-015')
    assert result is not None, "Failed to resolve SAP-015"
    assert result['namespace'] == 'chora.awareness.task_tracking'
    print("  ✓ Passed")

def test_normalization():
    """Test input normalization"""
    print("Test 2: Input normalization")
    resolver = AliasResolver()

    tests = ['SAP-015', 'sap-015', '015', 'SAP015']
    for test_input in tests:
        result = resolver.resolve(test_input)
        assert result['sap_id'] == 'SAP-015'

    print("  ✓ Passed")

def test_detection():
    """Test detection in user input"""
    print("Test 3: Detection in user input")

    user_input = "I want to install SAP-015 and SAP-001"
    pattern = r'SAP-(\d{3})'
    matches = re.findall(pattern, user_input)

    assert len(matches) == 2
    assert matches[0] == '015'
    assert matches[1] == '001'

    print("  ✓ Passed")

if __name__ == '__main__':
    test_resolution()
    test_normalization()
    test_detection()
    print("\nAll tests passed!")
```

**Run Tests**:
```bash
python test_resolution.py
```

---

## Phase 3: Validation

### Step 3.1: Test All 45 Aliases

**Create** `validate_all_aliases.py`:
```python
#!/usr/bin/env python3
"""Validate all 45 alias resolutions"""

import json
from alias_resolver import AliasResolver

def validate_all():
    """Test all aliases resolve correctly"""
    resolver = AliasResolver()

    with open('capabilities/alias-mapping.json') as f:
        mapping = json.load(f)

    total = len(mapping['aliases'])
    passed = 0

    for sap_id in mapping['aliases']:
        result = resolver.resolve(sap_id)

        if result and result['namespace'] == mapping['aliases'][sap_id]['namespace']:
            passed += 1
        else:
            print(f"✗ Failed: {sap_id}")

    print(f"\n{passed}/{total} aliases resolved correctly")
    return passed == total

if __name__ == '__main__':
    success = validate_all()
    exit(0 if success else 1)
```

**Run**:
```bash
python validate_all_aliases.py

# Expected:
# 45/45 aliases resolved correctly
```

---

### Step 3.2: Verify Deprecation Warnings

**Test**:
```python
from alias_resolver import AliasResolver

resolver = AliasResolver()

# Check all deprecated aliases have warnings
result = resolver.resolve('SAP-015')
assert result['deprecated'] == True
assert result['deprecation_warning'] is not None
assert 'days' in result['deprecation_warning']

print("✓ Deprecation warnings working")
```

---

### Step 3.3: Update Project AGENTS.md

**Add to AGENTS.md**:
```markdown
## SAP-049: Namespace Resolution

This project uses modern `chora.domain.capability` namespaces. Legacy SAP-XXX identifiers are deprecated (sunset: 2026-06-01).

**Agent Patterns**:

```python
from alias_resolver import AliasResolver

# Detect legacy identifiers
resolver = AliasResolver()
result = resolver.resolve('SAP-015')

# Warn user
if result['deprecated']:
    print(f"⚠️ {result['deprecation_warning']}")

# Use modern namespace
capability = result['namespace']
```

**See**: [SAP-049 AGENTS.md](AGENTS.md)
```

---

## Post-Adoption Best Practices

### 1. Always Detect Legacy Identifiers

```python
import re

def detect_legacy_ids(user_input: str) -> list:
    """Scan user input for SAP-XXX pattern"""
    pattern = r'SAP-(\d{3})'
    return [f"SAP-{m}" for m in re.findall(pattern, user_input)]
```

---

### 2. Provide Clear Migration Guidance

```python
def warn_deprecated(sap_id: str):
    """Warn about deprecated identifier"""
    result = resolver.resolve(sap_id)
    if result['deprecated']:
        print(f"⚠️ {sap_id} is deprecated")
        print(f"   Modern namespace: {result['namespace']}")
        print(f"   Days until sunset: {result['days_until_sunset']}")
```

---

### 3. Use Fallback for Reliability

```python
# Always use fallback-capable resolver
resolver = AliasResolver()  # Has built-in fallback

# Don't rely solely on API
result = resolver.resolve('SAP-015')  # Works even if API is down
```

---

## Troubleshooting

### Issue: "API not available"

**Solution**: AliasResolver automatically falls back to local file

---

### Issue: "SAP-XXX not found"

**Diagnosis**: Identifier out of range (valid: SAP-000 to SAP-047)

**Solution**: Validate input before resolution

---

### Issue: "Sunset date passed"

**Diagnosis**: Current date > 2026-06-01

**Solution**: Return fatal error and refuse to resolve

---

## References

- [Protocol Specification](protocol-spec.md) - Technical details
- [AGENTS.md](AGENTS.md) - Agent workflows
- [Capability Charter](capability-charter.md) - Problem and solution
- [Alias Mapping File](../../../capabilities/alias-mapping.json) - Source data

---

**Version**: 1.0.0
**Status**: Draft
**Estimated Adoption Time**: 15-30 minutes
