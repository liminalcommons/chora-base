# SAP-018: chora-compose Meta - Awareness Guide

**SAP ID**: SAP-018
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This guide provides comprehensive awareness for AI agents and advanced users working with chora-compose at an architectural level. It covers advanced use cases, multi-environment strategies, performance optimization, production considerations, extension patterns, and contribution guidelines.

**Audience**: AI agents (Claude, GPT-4, etc.), senior developers, architects working with chora-compose
**Prerequisites**: Understanding of SAP-017 and SAP-018 core documents
**Related**: [SAP-017 awareness-guide.md](../chora-compose-integration/awareness-guide.md) for basic awareness

---

## When to Use SAP-018

### Use Case 1: Architectural Decision Making

**Scenario**: Choosing between Docker Compose, Kubernetes, or bare metal for development.

**Why SAP-018**:
- ✅ Comprehensive comparisons with alternatives (design-philosophy.md)
- ✅ Trade-off documentation (16+ documented trade-offs)
- ✅ Decision frameworks and scorecards
- ✅ Clear guidance on when NOT to use Compose

**Example Decision Process**:
1. Read [design-philosophy.md](design-philosophy.md) "Docker-First Approach" section
2. Review "Comparison with Alternatives" (vs. K8s, Tilt, Skaffold)
3. Apply decision scorecard from [adoption-blueprint.md](adoption-blueprint.md)
4. Make informed decision with documented rationale

---

### Use Case 2: Organization-Wide Adoption

**Scenario**: Rolling out chora-compose to 50+ developers across multiple teams.

**Why SAP-018**:
- ✅ Adoption strategies (greenfield, pilot, incremental)
- ✅ Rollout patterns (top-down, bottom-up, CoE)
- ✅ Success metrics and governance
- ✅ Migration paths from existing setups

**Example Rollout**:
1. Form Center of Excellence (2-4 experts)
2. Run pilots on 3 diverse projects
3. Create template repository
4. Roll out incrementally (high-impact projects first)
5. Measure adoption metrics monthly

---

### Use Case 3: Advanced Integration

**Scenario**: Integrating chora-compose with CI/CD, monitoring, multi-project setups.

**Why SAP-018**:
- ✅ 12+ integration patterns cataloged (integration-patterns.md)
- ✅ CI/CD patterns (GitHub Actions, GitLab CI)
- ✅ Multi-project patterns (isolation, shared services)
- ✅ Production considerations

**Example**: GitHub Actions Integration
- Review Pattern 8 in [integration-patterns.md](integration-patterns.md)
- Implement test service with tmpfs database
- Add coverage collection and upload
- Reference workflow for multiple projects

---

### Use Case 4: Performance Optimization

**Scenario**: Docker Compose development environment is slow (startup, file operations).

**Why SAP-018**:
- ✅ Volume performance optimization (architecture-overview.md)
- ✅ Resource management patterns
- ✅ Build optimization strategies
- ✅ Platform-specific tuning (macOS/Windows/Linux)

**Example Optimizations**:
```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Delegated consistency
      - /workspace/__pycache__  # Exclude caches
      - pip-cache:/root/.cache/pip  # Named volume for deps
    deploy:
      resources:
        limits:
          cpus: '2.0'  # Prevent resource hogging
```

---

### Use Case 5: Contributing to Ecosystem

**Scenario**: Building extensions, templates, or contributing to chora-compose repository.

**Why SAP-018**:
- ✅ Design philosophy alignment
- ✅ Architectural understanding
- ✅ Pattern consistency
- ✅ Extension guidelines

---

## Advanced Use Cases

### Multi-Environment Management

**Strategy 1: Environment-Specific Compose Files**

```bash
# File structure
docker-compose.yml           # Base configuration
docker-compose.dev.yml       # Development overrides
docker-compose.test.yml      # Testing overrides
docker-compose.prod.yml      # Production configuration
```

**Usage**:
```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Testing
docker compose -f docker-compose.yml -f docker-compose.test.yml run test

# Production
docker compose -f docker-compose.prod.yml up -d
```

**Example Overrides**:
```yaml
# docker-compose.dev.yml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Dev only: live reload
    ports:
      - "8000:8000"  # Dev only: direct access
    command: uvicorn app:app --reload

# docker-compose.test.yml
services:
  db:
    tmpfs:
      - /var/lib/postgresql/data  # Test only: in-memory DB
  app:
    environment:
      - TESTING=true
    command: pytest tests/ -v

# docker-compose.prod.yml
services:
  app:
    image: registry.example.com/app:${VERSION}
    restart: always
    secrets:
      - app_secret
    # No volumes, no ports (behind nginx)
```

---

### Performance Tuning

**Build Optimization**: Multi-stage builds

```dockerfile
# Slow: Single stage (rebuilds deps every time)
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Fast: Multi-stage (caches deps)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
```

**Volume Performance**: Platform-specific optimizations

```yaml
# macOS/Windows: Use delegated + exclusions
services:
  app:
    volumes:
      - .:/workspace:delegated
      - /workspace/node_modules
      - /workspace/.venv
      - /workspace/__pycache__
      - pip-cache:/root/.cache/pip

# Linux: Use user namespaces
services:
  app:
    user: "${UID}:${GID}"  # Match host user
    volumes:
      - .:/workspace  # No consistency mode needed
```

**Resource Limits**: Prevent container sprawl

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

---

### Multi-Project Orchestration

**Pattern**: Shared Infrastructure + Project-Specific Services

**Shared Infrastructure** (`~/docker/infra.yml`):
```yaml
services:
  traefik:
    image: traefik:latest
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: dev
    volumes:
      - shared-postgres:/var/lib/postgresql/data
    networks:
      - infra

networks:
  infra:
    name: shared-infra
    external: false

volumes:
  shared-postgres:
```

**Project 1** (`project1/docker-compose.yml`):
```yaml
services:
  app:
    build: .
    labels:
      - "traefik.http.routers.project1.rule=Host(`project1.localhost`)"
    networks:
      - default
      - infra
    environment:
      - DATABASE_URL=postgresql://postgres:dev@postgres:5432/project1_db

networks:
  infra:
    external: true
    name: shared-infra
```

**Project 2** (`project2/docker-compose.yml`):
```yaml
services:
  app:
    build: .
    labels:
      - "traefik.http.routers.project2.rule=Host(`project2.localhost`)"
    networks:
      - default
      - infra
    environment:
      - DATABASE_URL=postgresql://postgres:dev@postgres:5432/project2_db

networks:
  infra:
    external: true
    name: shared-infra
```

**Benefits**:
- Single load balancer (Traefik) routes to all projects
- Shared database (isolated by database name)
- Domain-based routing (project1.localhost, project2.localhost)

---

## Extension Patterns

### Custom Service Templates

**Use Case**: Create reusable service definitions for your organization.

**Structure**:
```
org/compose-templates/
├── services/
│   ├── postgres.yml
│   ├── redis.yml
│   ├── rabbitmq.yml
│   └── monitoring.yml
└── stacks/
    ├── python-web.yml
    ├── python-mcp.yml
    └── nodejs-web.yml
```

**Example: postgres.yml**:
```yaml
# Reusable PostgreSQL service template
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
      POSTGRES_USER: ${POSTGRES_USER:-dev}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER:-dev}"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - backend

volumes:
  postgres-data:

networks:
  backend:
```

**Usage in Projects**:
```yaml
# project/docker-compose.yml
include:
  - ../compose-templates/services/postgres.yml
  - ../compose-templates/services/redis.yml

services:
  app:
    build: .
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
```

---

### Compose Profiles for Optional Services

**Use Case**: Enable/disable services dynamically (monitoring, debugging tools).

**Implementation**:
```yaml
services:
  app:
    build: .
    # Always runs

  db:
    image: postgres:15-alpine
    # Always runs

  prometheus:
    image: prom/prometheus
    profiles: ["monitoring"]
    # Only runs with --profile monitoring

  grafana:
    image: grafana/grafana
    profiles: ["monitoring"]
    # Only runs with --profile monitoring

  pgadmin:
    image: dpage/pgadmin4
    profiles: ["debug"]
    # Only runs with --profile debug
```

**Usage**:
```bash
# Basic: app + db
docker compose up -d

# With monitoring
docker compose --profile monitoring up -d

# With monitoring + debugging
docker compose --profile monitoring --profile debug up -d
```

---

## Production Considerations

### When to Use Compose in Production

**Good Fit**:
- Single-host deployments (VPS, small servers)
- Low-to-medium traffic (<10k req/min)
- Simple scaling needs (vertical scaling)
- Cost-sensitive environments
- Dev/test environments

**Example Scenarios**:
- Internal tools (admin dashboards, monitoring)
- Side projects / MVPs
- Small business websites
- Development/staging servers

**Not a Good Fit**:
- Multi-host orchestration (use Kubernetes)
- High availability requirements (use K8s)
- Auto-scaling needs (use K8s, ECS)
- Complex service mesh (use Istio, Linkerd)

---

### Production Checklist

**Security**:
- [ ] Use Docker secrets (not .env files)
- [ ] Enable TLS/SSL
- [ ] Restrict network access (internal networks)
- [ ] Use read-only volumes where possible
- [ ] Scan images for vulnerabilities
- [ ] Disable exposed ports (only through reverse proxy)

**Reliability**:
- [ ] Set restart policies (`restart: always`)
- [ ] Configure health checks for all services
- [ ] Implement log rotation (limit log size)
- [ ] Set resource limits (prevent OOM)
- [ ] Use named volumes (not bind mounts)
- [ ] Regular backups (volumes, databases)

**Performance**:
- [ ] Use production-optimized images (not -alpine for CPU-intensive)
- [ ] Enable caching where appropriate
- [ ] Tune service resources (CPU, memory)
- [ ] Use separate networks (frontend/backend)
- [ ] Implement monitoring (Prometheus, Grafana)

**Deployment**:
- [ ] Version images (not :latest)
- [ ] Use image registry (not local builds)
- [ ] Implement CI/CD pipeline
- [ ] Document deployment process
- [ ] Test rollback procedure

---

## Contribution Guidelines

### Contributing to chora-compose Repository

**Process**:
1. **Fork** https://github.com/liminalcommons/chora-compose
2. **Create Branch**: `feature/add-mongodb-template`
3. **Make Changes**: Add template, update docs
4. **Test**: Verify template works in isolation
5. **Submit PR**: Include description, examples, tests
6. **Review**: Maintainers review, request changes
7. **Merge**: PR merged, template available to community

**Quality Standards**:
- Templates must be tested
- Documentation required (README in template dir)
- Follow existing naming conventions
- Include health checks
- Provide .env.example

---

## Installation

### Quick Install

Install this SAP with its dependencies:

```bash
python scripts/install-sap.py SAP-018 --source /path/to/chora-base
```

This will automatically install:
- SAP-018 (Chora-Compose Meta Package)
- SAP-017 (Chora-Compose Integration)
- SAP-003 (Project Bootstrap & Scaffolding)
- SAP-000 (SAP Framework)

### Part of Sets

This SAP is included in the following [standard sets](../../user-docs/reference/standard-sap-sets.md):

- `full` - All 18 SAPs (complete capability suite)

To install a complete set:

```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Dependencies

This SAP depends on:
- SAP-017 (Chora-Compose Integration)

All dependencies are automatically installed.

### Validation

After installation, verify the SAP artifacts exist:

```bash
ls docs/skilled-awareness/chora-compose-meta/
# Should show: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md
```

### Custom Installation

For custom installation paths or options, see:
- [Install SAP Set How-To](../../user-docs/how-to/install-sap-set.md)
- [Install SAP Script Reference](../../user-docs/reference/install-sap-script.md)

---

## Related Content

### Cross-Domain Cross-References

**Development Documentation** (`docs/dev-docs/`):
- Not directly applicable (chora-compose is operational tool, not chora-base development)
- See chora-compose repository for contribution workflows

**User Documentation** (`docs/user-docs/`):
- [How to Integrate chora-compose](../../user-docs/how-to/integrate-chora-compose.md) - User-facing integration guide
- [Why Use MCP Servers](../../user-docs/explanation/why-mcp-servers.md) - Context for MCP + Docker Compose patterns
- [MCP Protocol Reference](../../user-docs/reference/mcp-protocol-spec.md) - MCP protocol details
- [FastMCP API Reference](../../user-docs/reference/fastmcp-api-reference.md) - FastMCP-specific patterns

**Project Documentation** (`docs/project-docs/`):
- [Wave 3 Track 2 Summary](../../project-docs/wave-3-track-2-summary.md) - SAP-017/018 creation context
- [Wave 3 Summary](../../project-docs/wave-3-summary.md) - Overall Wave 3 achievements
- [Wave 3 Execution Plan](../../project-docs/wave-3-execution-plan.md) - Planning for SAP-017/018
- [v4.0 Vision](../../project-docs/CHORA-BASE-4.0-VISION.md) - Universal foundation vision (ecosystem integration pattern)

**Standards** (`docs/standards/`):
- [Chora MCP Conventions v1.0](../../standards/CHORA_MCP_CONVENTIONS_v1.0.md) - MCP naming and structure standards

**SAP Documentation** (`docs/skilled-awareness/`):
- [SAP-017: chora-compose Integration](../chora-compose-integration/) - Tactical integration guide
- [SAP-003: Project Bootstrap](../project-bootstrap/) - chora-base project structure
- [SAP-014: MCP Server Development](../mcp-server-development/) - MCP server patterns with Docker
- [SAP-004: Testing Framework](../testing-framework/) - Testing in containerized environments
- [SAP-011: Docker Operations](../docker-operations/) - Docker best practices
- [SAP-007: Documentation Framework](../documentation-framework/) - Documentation standards

### External References

**chora-compose**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Source code and templates

**Docker**:
- [Docker Compose Specification](https://github.com/compose-spec/compose-spec) - Official spec
- [Compose File Reference](https://docs.docker.com/compose/compose-file/) - Full reference
- [Awesome Compose](https://github.com/docker/awesome-compose) - Example projects

**Alternatives**:
- [Tilt](https://tilt.dev/) - Kubernetes development
- [Skaffold](https://skaffold.dev/) - K8s build and deploy
- [DevContainers](https://containers.dev/) - VS Code remote development

---

## Quick Reference

### Essential SAP-018 Documents

**For Architecture**:
- [architecture-overview.md](architecture-overview.md) (~1,000 lines)

**For Philosophy**:
- [design-philosophy.md](design-philosophy.md) (~1,000 lines)

**For Patterns**:
- [integration-patterns.md](integration-patterns.md) (~900 lines)

**For Adoption**:
- [adoption-blueprint.md](adoption-blueprint.md) (~600 lines)

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Features**:
- Advanced use cases (multi-environment, performance, multi-project)
- Extension patterns (custom templates, profiles)
- Production considerations (when to use, checklist)
- Contribution guidelines

---

## Related Documentation

**SAP-018 Artifacts**:
- [capability-charter.md](capability-charter.md) - Business value, capabilities
- [architecture-overview.md](architecture-overview.md) - Technical architecture
- [design-philosophy.md](design-philosophy.md) - Design principles
- [integration-patterns.md](integration-patterns.md) - Pattern catalog
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption strategy

**Related SAPs**:
- [SAP-017: chora-compose Integration](../chora-compose-integration/) - Tactical integration guide

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
