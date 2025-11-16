# Namespace Format Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-15
**Part of**: Ecosystem Ontology & Composition Vision (SAP-048)

---

## Purpose

This document defines the **3-level hierarchical namespace format** used by the chora ecosystem for capability identification. The namespace format ensures global uniqueness, semantic organization, and cross-repository discovery for both Service-type and Pattern-type capabilities.

---

## Namespace Format

### Standard Format

```
chora.{domain}.{capability}
```

**Components**:
1. **Prefix**: `chora` (ecosystem identifier, fixed)
2. **Domain**: One of 20 standardized domains (see [domain-taxonomy.md](./domain-taxonomy.md))
3. **Capability**: Unique capability name within domain (snake_case)

**Examples**:
- `chora.registry.lookup` (Service-type: registry lookup service)
- `chora.react.form_validation` (Pattern-type: form validation SAP)
- `chora.interface.multi` (Pattern-type: multi-interface design patterns)

---

## Level 1: Ecosystem Prefix

### Definition

**Value**: `chora` (fixed, lowercase)

**Purpose**: Identifies all capabilities as part of the chora ecosystem

**Rationale**:
- Prevents collisions with other ecosystems (e.g., `kubernetes.*`, `aws.*`)
- Enables global capability discovery across repositories
- Provides PyPI namespace reservation (`chora-*` packages)

**Collision Prevention**:
- Ecosystem prefix is **immutable** (cannot be changed)
- All capabilities MUST use `chora` prefix
- Non-chora capabilities use different prefix (e.g., `acme.domain.capability`)

---

## Level 2: Domain

### Definition

**Value**: One of 20 standardized domains (lowercase, snake_case if multi-word)

**Purpose**: Organizes capabilities into semantic categories

**Validation Rules**:
1. Domain MUST exist in [domain-taxonomy.md](./domain-taxonomy.md)
2. Domain MUST be lowercase
3. Multi-word domains use snake_case (e.g., `developer_experience`)
4. Domain is **required** (cannot be empty)

**Current Domains** (10 active, 10 reserved):

**Active**:
- `infrastructure` - Core framework capabilities
- `registry` - Service discovery and health monitoring
- `bootstrap` - System initialization and startup
- `devex` - Developer experience tools
- `interface` - Interface design patterns
- `composition` - Service orchestration
- `templates` - Project templates and generators
- `react` - React application patterns
- `awareness` - Agent awareness and memory
- `workflow` - Development lifecycle patterns
- `integration` - Third-party integrations
- `optimization` - Performance optimization

**Reserved** (future use):
- `database` - Database integration patterns
- `security` - Authentication and authorization
- `monitoring` - Observability and error tracking
- `vue` - Vue.js patterns
- `angular` - Angular patterns
- `mobile` - Mobile app patterns
- `desktop` - Desktop app patterns
- `api` - Backend API patterns

**Domain Selection**: See [domain-taxonomy.md#domain-allocation-guidelines](./domain-taxonomy.md#domain-allocation-guidelines)

---

## Level 3: Capability

### Definition

**Value**: Unique capability name within domain (lowercase, snake_case)

**Purpose**: Identifies specific capability functionality

**Naming Conventions**:

1. **Use snake_case** (lowercase with underscores)
   - ✅ `form_validation`
   - ❌ `formValidation` (camelCase)
   - ❌ `form-validation` (kebab-case)

2. **Be descriptive and specific**
   - ✅ `multi_interface` (clear: multiple interfaces)
   - ❌ `multi` (ambiguous)
   - ✅ `lookup` (when domain provides context: `registry.lookup`)

3. **Avoid redundancy with domain**
   - ✅ `chora.react.form_validation` (not `react_form_validation`)
   - ✅ `chora.registry.lookup` (not `registry_lookup`)

4. **Use action verbs for Service-type capabilities**
   - ✅ `lookup`, `initialize`, `deploy`, `monitor`
   - Service-type capabilities **do** something at runtime

5. **Use noun phrases for Pattern-type capabilities**
   - ✅ `form_validation`, `multi_interface`, `saga_patterns`
   - Pattern-type capabilities **describe** knowledge/patterns

6. **Maximum length**: 50 characters (recommended: 20-30)

7. **Character set**: `[a-z0-9_]` (lowercase letters, numbers, underscores)

---

## Uniqueness Constraints

### Global Uniqueness

**Rule**: Each full namespace (`chora.domain.capability`) MUST be globally unique across the entire ecosystem.

**Validation**:
```bash
# Pre-commit hook checks for duplicates
grep "dc_identifier: chora.domain.capability" capabilities/*.yaml

# Returns error if duplicate found
```

**Collision Detection**:
- Checked at **commit time** (pre-commit hook)
- Checked at **CI/CD time** (GitHub Actions workflow)
- Checked at **registry sync time** (etcd/PostgreSQL insertion)

### Domain-Scoped Uniqueness

**Rule**: Capability names MUST be unique within a domain.

**Example**:
- ✅ `chora.react.form_validation` + `chora.vue.form_validation` (different domains)
- ❌ `chora.react.form_validation` + `chora.react.form_validation` (same domain, same name)

**Rationale**: Allows similar patterns across different technology stacks (React, Vue, Angular) without namespace pollution.

### Cross-Domain Disambiguation

If similar capabilities exist across domains, use descriptive suffixes:

**Example**:
- `chora.react.testing` (React testing patterns)
- `chora.devex.testing_framework` (Generic testing framework)
- `chora.api.testing` (API testing patterns)

---

## Namespace Aliases (Legacy Support)

### Purpose

Support backward compatibility during migration from `sap-catalog.json` to unified ontology.

### Alias Format

```yaml
# New primary namespace
metadata:
  dc_identifier: chora.react.form_validation

# Legacy alias (deprecated)
  dc_identifier_legacy: SAP-041
```

### Alias Resolution

**Registry lookup** supports both namespaces during transition:

```bash
# New namespace (preferred)
chora registry lookup chora.react.form_validation

# Legacy SAP ID (deprecated, resolves to new namespace)
chora registry lookup SAP-041
# Returns: chora.react.form_validation (with deprecation warning)
```

### Alias Deprecation Timeline

- **v5.2.0** (Week 4): Aliases introduced for pilot capabilities
- **v5.3.0** (Week 8): Aliases for all 45 SAPs
- **v5.5.0** (Week 16): Deprecation warnings added
- **v6.0.0** (Q2 2026): Legacy aliases removed

---

## Namespace Versioning

### Version Field

**Separate from namespace**: Versions use SemVer 2.0.0 in `dc_hasVersion` field

```yaml
metadata:
  dc_identifier: chora.react.form_validation  # Namespace (stable)
  dc_hasVersion: "1.2.3"                       # Version (changes)
```

**Rationale**: Namespaces are **identity**, versions are **evolution**.

### Version Constraints in Dependencies

```yaml
dc_relation:
  requires:
    - capability: chora.react.foundation
      version: ^1.0.0              # Caret range (1.x.x)
    - capability: chora.registry.lookup
      version: ">=2.0.0 <3.0.0"    # Range
    - capability: chora.bootstrap.initialize
      version: ~1.2.0              # Tilde range (1.2.x)
```

**SemVer Operators**:
- `^1.0.0` - Compatible with 1.x.x (allows minor/patch updates)
- `~1.2.0` - Compatible with 1.2.x (allows patch updates only)
- `>=1.5.0 <2.0.0` - Explicit range
- `1.0.0` - Exact version (not recommended for dependencies)

---

## Namespace Examples by Domain

### Infrastructure Domain

```
chora.infrastructure.sap_framework      (SAP-000, Pattern)
chora.infrastructure.inbox              (SAP-001, Pattern)
chora.infrastructure.meta_package       (SAP-002, Pattern)
```

### Registry Domain

```
chora.registry.lookup                   (SAP-044, Service, pilot)
chora.registry.health_monitor           (future, Service)
chora.registry.dependency_resolver      (future, Service)
```

### Bootstrap Domain

```
chora.bootstrap.initialize              (SAP-045, Service, pilot)
chora.bootstrap.config_loader           (future, Service)
chora.bootstrap.env_validator           (future, Service)
```

### DevEx Domain

```
chora.devex.project_bootstrap           (SAP-003, Pattern)
chora.devex.testing_framework           (SAP-004, Pattern)
chora.devex.ci_cd                       (SAP-005, Pattern)
chora.devex.quality_gates               (SAP-006, Pattern)
chora.devex.documentation               (SAP-007, Pattern)
chora.devex.automation                  (SAP-008, Pattern)
chora.devex.docker                      (SAP-011, Pattern)
```

### Interface Domain

```
chora.interface.design                  (SAP-042, Pattern, pilot)
chora.interface.multi                   (SAP-043, Pattern, pilot)
chora.interface.cli_patterns            (future, Pattern)
chora.interface.rest_patterns           (future, Pattern)
chora.interface.mcp_patterns            (future, Pattern)
```

### Composition Domain

```
chora.composition.saga                  (SAP-046, Service, pilot)
chora.composition.circuit_breaker       (future, Service)
chora.composition.event_bus             (future, Service)
```

### Templates Domain

```
chora.templates.capability_server       (SAP-047, Pattern, pilot)
chora.templates.react_app               (future, Pattern)
chora.templates.python_lib              (future, Pattern)
```

### React Domain

```
chora.react.foundation                  (SAP-020, Pattern)
chora.react.testing                     (SAP-021, Pattern)
chora.react.linting                     (SAP-022, Pattern)
chora.react.state_management            (SAP-023, Pattern)
chora.react.styling                     (SAP-024, Pattern)
chora.react.performance                 (SAP-025, Pattern)
chora.react.accessibility               (SAP-026, Pattern)
chora.react.authentication              (SAP-033, Pattern, pilot)
chora.react.database_integration        (SAP-034, Pattern, pilot)
chora.react.file_upload                 (SAP-035, Pattern, pilot)
chora.react.error_handling              (SAP-036, Pattern, pilot)
chora.react.realtime                    (SAP-037, Pattern, pilot)
chora.react.i18n                        (SAP-038, Pattern, pilot)
chora.react.e2e_testing                 (SAP-039, Pattern, pilot)
chora.react.monorepo                    (SAP-040, Pattern, pilot)
chora.react.form_validation             (SAP-041, Pattern, pilot)
```

### Awareness Domain

```
chora.awareness.nested_pattern          (SAP-009, Pattern)
chora.awareness.event_memory            (SAP-010, Pattern)
chora.awareness.task_tracking           (SAP-015, Pattern, pilot)
chora.awareness.sap_evaluation          (SAP-019, Pattern)
```

### Workflow Domain

```
chora.workflow.lifecycle                (SAP-012, Pattern)
chora.workflow.metrics                  (SAP-013, Pattern)
chora.workflow.link_validation          (SAP-016, Pattern)
chora.workflow.dogfooding               (SAP-027, Pattern)
chora.workflow.publishing               (SAP-028, Pattern, pilot)
chora.workflow.sap_generation           (SAP-029, Pattern, pilot)
```

### Integration Domain

```
chora.integration.compose               (SAP-017, Service)
chora.integration.compose_meta          (SAP-018, Service)
chora.integration.llm_orchestration     (future, Service)
```

---

## Namespace Validation Rules

### Pre-Commit Hook Validation

The pre-commit hook (`scripts/validate-namespaces.py`) enforces:

1. **Format Validation**:
   - Matches regex: `^chora\.[a-z_]+\.[a-z0-9_]{1,50}$`
   - Three components separated by dots
   - Lowercase only, snake_case

2. **Domain Validation**:
   - Domain exists in `docs/ontology/domain-taxonomy.md`
   - Domain is not deprecated

3. **Uniqueness Validation**:
   - No duplicate namespaces in `capabilities/*.yaml`
   - No conflicts with existing PyPI packages (`chora-*`)

4. **Version Validation**:
   - `dc_hasVersion` field uses valid SemVer (x.y.z)

5. **Dependency Validation**:
   - All dependencies reference valid namespaces
   - Version constraints use valid SemVer operators

### CI/CD Validation

GitHub Actions workflow (`.github/workflows/validate-capabilities.yaml`) runs:

```yaml
- name: Validate Capability Namespaces
  run: |
    python scripts/validate-namespaces.py capabilities/

- name: Check Namespace Collisions
  run: |
    python scripts/check-namespace-collisions.py capabilities/

- name: Validate Cross-Type Dependencies
  run: |
    python scripts/validate-cross-type-deps.py capabilities/
```

### Registry Validation

etcd and PostgreSQL insertion validates:

1. **Namespace uniqueness** (UNIQUE constraint on `dc_identifier`)
2. **Domain existence** (FOREIGN KEY to domains table)
3. **SemVer format** (CHECK constraint on `dc_hasVersion`)

---

## Namespace Migration Process

### From SAP-XXX to chora.domain.capability

**Step 1: Identify Target Domain**

Use [domain-taxonomy.md#domain-allocation-guidelines](./domain-taxonomy.md#domain-allocation-guidelines)

**Step 2: Choose Capability Name**

Follow naming conventions (snake_case, descriptive, no redundancy)

**Step 3: Create YAML Manifest**

```yaml
apiVersion: chora.dev/v1
kind: Capability

metadata:
  dc_identifier: chora.react.form_validation
  dc_identifier_legacy: SAP-041  # Alias during transition
  dc_title: "React Form Validation Patterns"
  dc_description: "React Hook Form + Zod validation patterns for production apps"
  dc_type: "Pattern"
  dc_hasVersion: "1.0.0"
```

**Step 4: Update Dependencies**

```yaml
dc_relation:
  requires:
    - capability: chora.react.foundation  # Use new namespace
      version: ^1.0.0
      relationship: prerequisite
```

**Step 5: Validate and Commit**

```bash
# Validate manifest
python scripts/validate-capability.py capabilities/chora.react.form_validation.yaml

# Commit (pre-commit hook auto-validates)
git add capabilities/chora.react.form_validation.yaml
git commit -m "feat(ontology): migrate SAP-041 to chora.react.form_validation"
```

---

## Namespace Best Practices

### DO

✅ **Use descriptive, self-documenting names**
```
chora.react.form_validation  (clear purpose)
```

✅ **Leverage domain context for brevity**
```
chora.registry.lookup  (domain clarifies "registry lookup")
```

✅ **Use consistent naming across similar capabilities**
```
chora.react.form_validation
chora.vue.form_validation
chora.angular.form_validation
```

✅ **Follow type-specific conventions**
```
# Service-type: action verbs
chora.registry.lookup
chora.bootstrap.initialize

# Pattern-type: noun phrases
chora.react.form_validation
chora.interface.multi
```

### DON'T

❌ **Use abbreviations or acronyms (unless well-known)**
```
chora.react.fv  (unclear)
```

❌ **Repeat domain in capability name**
```
chora.react.react_form_validation  (redundant)
```

❌ **Use overly generic names**
```
chora.react.utils  (too broad)
```

❌ **Mix naming conventions**
```
chora.react.formValidation  (camelCase, should be snake_case)
chora.react.form-validation  (kebab-case, should be snake_case)
```

❌ **Exceed character limits**
```
chora.react.extremely_detailed_form_validation_with_schema_validation  (too long)
```

---

## Namespace Collision Analysis

### Analysis of 45 Current SAPs

**Potential Collisions**: 0

All 45 SAPs have been pre-analyzed for namespace collisions:
- No duplicate capability names within domains
- No conflicts with reserved PyPI packages
- No conflicts with Kubernetes ecosystem (`k8s.*`)
- No conflicts with cloud providers (`aws.*`, `gcp.*`, `azure.*`)

### Future Collision Prevention

**Reserved Namespaces**:
- `chora.*` - Reserved for chora ecosystem only
- `chora.{domain}.*` - Reserved for capabilities in that domain

**Forbidden Namespaces**:
- `chora.test.*` - Reserved for testing (not production capabilities)
- `chora.internal.*` - Reserved for chora-base internals
- `chora.deprecated.*` - Reserved for archived capabilities

---

## Namespace Documentation Requirements

Each capability manifest MUST include:

```yaml
metadata:
  dc_identifier: chora.domain.capability     # REQUIRED: Namespace
  dc_title: "Human-Readable Title"           # REQUIRED: Display name
  dc_description: "One-sentence summary"     # REQUIRED: Purpose
  dc_type: "Service" | "Pattern"             # REQUIRED: Capability type
  dc_hasVersion: "x.y.z"                     # REQUIRED: SemVer version

  dc_identifier_legacy: "SAP-XXX"            # OPTIONAL: Alias (during migration)
  dc_creator: "Chora Core Team"              # OPTIONAL: Author
  dc_date: "2025-11-15"                      # OPTIONAL: Publication date
```

---

## Version History

- **1.0.0** (2025-11-15): Initial namespace specification
  - 3-level hierarchical format defined
  - Naming conventions established
  - Validation rules documented
  - 45 SAPs analyzed for collisions (0 found)
  - Migration process from SAP-XXX format

---

## Related Documentation

- [Domain Taxonomy](./domain-taxonomy.md) (Week 1.1, ONT-001)
- [Migration Guide](./migration-guide.md) (Week 1.3, ONT-003)
- [Capability Type Definitions](./capability-types.md) (Week 1.4, ONT-004)
- [SemVer Specification](https://semver.org/) (external)

---

**Next Steps**:
1. Week 1.3: Create migration mapping (ONT-003)
2. Week 1.4: Define unified capability types (ONT-004)
