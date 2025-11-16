# SAP Namespace Quick Reference

**Status**: Legacy SAP-XXX identifiers are deprecated
**Sunset Date**: 2026-06-01
**Days Until Sunset**: 198

---

## ⚠️ Deprecation Notice

Legacy `SAP-XXX` identifiers are **deprecated** and will be sunset on **June 1, 2026**.

**Please use modern `chora.domain.capability` namespaces instead.**

### Migration Resources

- **Alias Redirect Service**: http://localhost:8000/SAP-XXX
- **Migration Guide**: [migration-guide.md](migration-guide.md)
- **Phase 3 Summary**: [PHASE3-COMPLETE.md](PHASE3-COMPLETE.md)

---

## Quick Reference Table

| Legacy ID | Modern Namespace | Domain | Type |
|-----------|------------------|--------|------|
| SAP-000 | chora.infrastructure.sap_framework | infrastructure | Pattern |
| SAP-001 | chora.infrastructure.inbox | infrastructure | Pattern |
| SAP-002 | chora.infrastructure.chora_base | infrastructure | Pattern |
| SAP-003 | chora.devex.project_bootstrap | devex | Pattern |
| SAP-004 | chora.devex.testing_framework | devex | Pattern |
| SAP-005 | chora.devex.ci_cd_workflows | devex | Pattern |
| SAP-006 | chora.devex.quality_gates | devex | Pattern |
| SAP-007 | chora.devex.documentation_framework | devex | Service |
| SAP-008 | chora.devex.automation_scripts | devex | Pattern |
| SAP-009 | chora.awareness.agent_awareness | awareness | Pattern |
| SAP-010 | chora.awareness.memory_system | awareness | Pattern |
| SAP-011 | chora.devex.docker_operations | devex | Pattern |
| SAP-012 | chora.awareness.development_lifecycle | awareness | Pattern |
| SAP-013 | chora.awareness.metrics_tracking | awareness | Pattern |
| SAP-014 | chora.devex.mcp_server_development | devex | Pattern |
| SAP-015 | chora.awareness.task_tracking | awareness | Service |
| SAP-016 | chora.awareness.link_validation_reference_management | awareness | Pattern |
| SAP-017 | chora.integration.chora_compose_integration | integration | Pattern |
| SAP-018 | chora.integration.chora_compose_meta | integration | Pattern |
| SAP-019 | chora.awareness.sap_self_evaluation | awareness | Service |
| SAP-020 | chora.react.foundation | react | Pattern |
| SAP-021 | chora.react.testing | react | Pattern |
| SAP-022 | chora.react.linting | react | Pattern |
| SAP-023 | chora.react.state_management | react | Pattern |
| SAP-024 | chora.react.styling | react | Pattern |
| SAP-025 | chora.integration.react_performance | integration | Pattern |
| SAP-026 | chora.integration.react_accessibility | integration | Pattern |
| SAP-027 | chora.awareness.dogfooding_patterns | awareness | Pattern |
| SAP-028 | chora.awareness.publishing_automation | awareness | Pattern |
| SAP-029 | chora.awareness.sap_generation | awareness | Pattern |
| SAP-033 | chora.react.authentication | react | Pattern |
| SAP-034 | chora.react.database_integration | react | Pattern |
| SAP-035 | chora.react.file_upload | react | Pattern |
| SAP-036 | chora.react.error_handling | react | Pattern |
| SAP-037 | chora.integration.react_realtime_synchronization | integration | Pattern |
| SAP-038 | chora.integration.react_internationalization | integration | Pattern |
| SAP-039 | chora.integration.react_e2e_testing | integration | Pattern |
| SAP-040 | chora.integration.react_monorepo_architecture | integration | Pattern |
| SAP-041 | chora.react.form_validation | react | Pattern |
| SAP-042 | chora.devex.interface_design | devex | Service |
| SAP-043 | chora.devex.multi_interface | devex | Service |
| SAP-044 | chora.devex.registry | devex | Service |
| SAP-045 | chora.devex.bootstrap | devex | Service |
| SAP-046 | chora.devex.composition | devex | Pattern |
| SAP-047 | chora.devex.capability_server_template | devex | Service |

---

## Domain Index

### infrastructure (3 capabilities)
- chora.infrastructure.sap_framework (SAP-000)
- chora.infrastructure.inbox (SAP-001)
- chora.infrastructure.chora_base (SAP-002)

### devex (13 capabilities)
- chora.devex.project_bootstrap (SAP-003)
- chora.devex.testing_framework (SAP-004)
- chora.devex.ci_cd_workflows (SAP-005)
- chora.devex.quality_gates (SAP-006)
- chora.devex.documentation_framework (SAP-007)
- chora.devex.automation_scripts (SAP-008)
- chora.devex.docker_operations (SAP-011)
- chora.devex.mcp_server_development (SAP-014)
- chora.devex.interface_design (SAP-042)
- chora.devex.multi_interface (SAP-043)
- chora.devex.registry (SAP-044)
- chora.devex.bootstrap (SAP-045)
- chora.devex.composition (SAP-046)
- chora.devex.capability_server_template (SAP-047)

### awareness (9 capabilities)
- chora.awareness.agent_awareness (SAP-009)
- chora.awareness.memory_system (SAP-010)
- chora.awareness.development_lifecycle (SAP-012)
- chora.awareness.metrics_tracking (SAP-013)
- chora.awareness.task_tracking (SAP-015)
- chora.awareness.link_validation_reference_management (SAP-016)
- chora.awareness.sap_self_evaluation (SAP-019)
- chora.awareness.dogfooding_patterns (SAP-027)
- chora.awareness.publishing_automation (SAP-028)
- chora.awareness.sap_generation (SAP-029)

### react (12 capabilities)
- chora.react.foundation (SAP-020)
- chora.react.testing (SAP-021)
- chora.react.linting (SAP-022)
- chora.react.state_management (SAP-023)
- chora.react.styling (SAP-024)
- chora.react.authentication (SAP-033)
- chora.react.database_integration (SAP-034)
- chora.react.file_upload (SAP-035)
- chora.react.error_handling (SAP-036)
- chora.react.form_validation (SAP-041)

### integration (8 capabilities)
- chora.integration.chora_compose_integration (SAP-017)
- chora.integration.chora_compose_meta (SAP-018)
- chora.integration.react_performance (SAP-025)
- chora.integration.react_accessibility (SAP-026)
- chora.integration.react_realtime_synchronization (SAP-037)
- chora.integration.react_internationalization (SAP-038)
- chora.integration.react_e2e_testing (SAP-039)
- chora.integration.react_monorepo_architecture (SAP-040)

---

## Type Index

### Service-type (9 capabilities)
Runtime components with health monitoring:
- chora.devex.documentation_framework (SAP-007)
- chora.awareness.task_tracking (SAP-015)
- chora.awareness.sap_self_evaluation (SAP-019)
- chora.devex.interface_design (SAP-042)
- chora.devex.multi_interface (SAP-043)
- chora.devex.registry (SAP-044)
- chora.devex.bootstrap (SAP-045)
- chora.devex.capability_server_template (SAP-047)

### Pattern-type (36 capabilities)
Documentation-based capabilities:
- All other capabilities not listed as Service-type

---

## Programmatic Access

### REST API

```bash
# Resolve single alias
curl http://localhost:8000/api/v1/resolve/SAP-015

# List all aliases
curl http://localhost:8000/api/v1/aliases
```

### Python

```python
import json
from pathlib import Path

# Load alias mapping
with open("capabilities/alias-mapping.json", "r") as f:
    data = json.load(f)

# Resolve alias
sap_id = "SAP-015"
namespace = data["aliases"][sap_id]["namespace"]
print(f"{sap_id} -> {namespace}")
```

### Bash

```bash
# Using jq
sap_id="SAP-015"
namespace=$(jq -r ".aliases[\"$sap_id\"].namespace" capabilities/alias-mapping.json)
echo "$sap_id -> $namespace"
```

---

## Migration Timeline

| Phase | Date | Status |
|-------|------|--------|
| **Phase 1**: Foundation & Pilot | 2025-11-15 | ✅ Complete |
| **Phase 2**: Full Migration | 2025-11-15 | ✅ Complete |
| **Phase 3**: Source Data Cleanup | 2025-11-15 | ✅ Complete |
| **Deprecation Start** | 2025-11-15 | 🟡 Active |
| **Critical Warning** (90 days) | 2026-03-01 | ⏳ Pending |
| **Final Warning** (30 days) | 2026-05-01 | ⏳ Pending |
| **Sunset Date** | 2026-06-01 | ⏳ Pending |

---

## Related Documentation

- [Migration Guide](migration-guide.md) - Step-by-step migration instructions
- [Namespace Specification](namespace-spec.md) - Modern namespace format rules
- [Domain Taxonomy](domain-taxonomy.md) - Complete domain hierarchy
- [Phase 3 Summary](PHASE3-COMPLETE.md) - Migration completion report
- [Alias Redirect Service](../../services/alias-redirect/README.md) - HTTP redirect service

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Status**: Active
**Sunset Date**: 2026-06-01
