# SAP-017: chora-compose Integration - Capability Charter

**SAP ID**: SAP-017
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-10-29
**Category**: Ecosystem Integration SAP

---

## What This Is

**chora-compose Integration** is a capability package that enables developers to integrate [chora-compose](https://github.com/liminalcommons/chora-compose) - a Docker Compose-based orchestration system for AI agent development environments - with their chora-base Python projects.

This SAP provides integration patterns, configuration guidance, and best practices for leveraging chora-compose's containerized development workflows alongside chora-base project structures.

**Key Capabilities**:
- Docker Compose integration patterns for chora-base projects
- Multi-container orchestration for AI agent environments
- Volume management for persistent data and code
- Environment configuration and secrets management
- Service dependency coordination (databases, APIs, MCP servers)
- Development workflow patterns (local, Docker, hybrid)

---

## Why This Exists

### The Problem

Integrating Docker-based development environments with Python projects requires:
- Understanding Docker Compose service orchestration
- Managing volume mounts for local development
- Configuring environment variables and secrets
- Coordinating service dependencies (databases, APIs, tools)
- Balancing local development speed vs. containerized consistency
- Debugging containerized services

**Time Investment**: 4-8 hours for first integration, 1-2 hours per subsequent project
**Error Rate**: High (volume mount issues, environment config, network problems)

### The Solution

SAP-017 provides production-ready integration patterns that:
- ✅ Implement best practices for Docker Compose + chora-base
- ✅ Include working volume mount configurations
- ✅ Provide environment variable patterns and examples
- ✅ Document service dependency patterns
- ✅ Offer debugging strategies for common issues
- ✅ Support hybrid workflows (local + Docker)

**Time Investment**: 30-60 minutes for first integration, 10-15 minutes per subsequent project
**Error Rate**: Low (battle-tested patterns, documented troubleshooting)

**ROI**: Saves 3-7 hours per project integration, reduces containerization debugging time

---

## Who Should Use This

### Primary Audience

**Python Developers with chora-base Projects**:
- Building AI agents or MCP servers with chora-base
- Need containerized development environments
- Want reproducible builds across machines
- Deploying to Docker-based production environments

**Team Leads / Platform Engineers**:
- Standardizing development environments across teams
- Managing multi-developer projects
- Ensuring environment consistency
- Building CI/CD pipelines with Docker

### Secondary Audience

**AI Application Developers**:
- Developing applications with multiple service dependencies
- Prototyping integrations with databases, APIs, tools
- Testing multi-container architectures

**DevOps Engineers**:
- Deploying chora-base projects to production
- Managing containerized AI agent infrastructure
- Building platform-as-a-service offerings

### Anti-Audience (Who Should NOT Use This)

**Don't use SAP-017 if**:
- Not using chora-base Python projects (no integration needed)
- Don't need Docker/containers (local development sufficient)
- Using non-Docker orchestration (Kubernetes, serverless, VMs)
- Building simple scripts (containerization overkill)

---

## Expected Outcomes

After adopting SAP-017, development teams should achieve:

### Immediate Outcomes (Week 1)
1. **Successful Docker Compose integration** - chora-base project running in containers with all dependencies
2. **Environment consistency** - Developers can clone and run the project with `docker compose up`
3. **Basic orchestration** - Multiple services (app, database, etc.) coordinated successfully

### Short-Term Outcomes (Month 1)
1. **Reduced onboarding time** - New developers productive within hours, not days
2. **Fewer environment issues** - "Works on my machine" problems eliminated
3. **Hybrid workflow mastery** - Team comfortable switching between local and containerized development

### Long-Term Outcomes (Quarter 1)
1. **Production parity** - Development environment mirrors production configuration
2. **Team standardization** - All projects use consistent Docker Compose patterns
3. **CI/CD integration** - Automated testing and deployment using same containers

### Measurable Success Criteria
- **Setup time**: ≤30 minutes for first Docker integration (vs 4-8 hours manual)
- **Onboarding speed**: New developers running code in ≤1 hour (vs 4+ hours)
- **Environment parity**: >95% consistency between dev and production
- **Issue reduction**: >80% fewer environment-related bugs

---

## Business Value

### Direct Benefits

**Speed**:
- Reduce integration time from 4-8 hours to 30-60 minutes
- Enable quick project onboarding for new team members
- Faster iteration with pre-configured services

**Quality**:
- Consistent development environments across machines
- Reproducible builds (eliminate "works on my machine")
- Isolated service dependencies (no local install conflicts)

**Maintainability**:
- Centralized configuration management
- Version-controlled environment definitions
- Easy updates via docker-compose.yml changes

### Indirect Benefits

**Collaboration**:
- Simplified environment setup for contributors
- Standardized tooling across teams
- Easier code reviews (consistent test environments)

**Deployment**:
- Development-production parity
- Docker-native deployment pipelines
- Easy scaling with container orchestration

**Learning**:
- Practical Docker Compose examples
- Integration pattern library
- Troubleshooting playbook

---

## Core Capabilities

### 1. Multi-Container Orchestration

**Capability**: Coordinate multiple services (Python app, database, API gateways, MCP servers) using Docker Compose.

**Use Cases**:
- AI agent + PostgreSQL database + Redis cache
- MCP server + n8n workflow automation + monitoring
- Multi-server development (frontend + backend + AI services)

**Patterns**:
```yaml
# docker-compose.yml example
services:
  app:
    build: .
    volumes:
      - .:/workspace
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

**Benefits**:
- Single command startup: `docker compose up`
- Automatic service discovery
- Dependency ordering
- Health check coordination

---

### 2. Volume Management

**Capability**: Mount local code, data, and configuration into containers for live development.

**Use Cases**:
- Live code reloading (edit locally, run in container)
- Persistent database data across container restarts
- Shared configuration files
- Log file access from host

**Patterns**:
```yaml
services:
  app:
    volumes:
      # Source code (read-write for development)
      - .:/workspace:delegated
      # Python dependencies (cache)
      - pip-cache:/root/.cache/pip
      # Configuration (read-only)
      - ./config:/app/config:ro
      # Logs (writable, accessible from host)
      - ./logs:/app/logs
```

**Benefits**:
- Fast development iteration (no rebuild for code changes)
- Persistent data (databases, caches)
- Local file access (logs, outputs)
- Dependency caching (faster rebuilds)

---

### 3. Environment Configuration

**Capability**: Manage environment variables, secrets, and configuration across services.

**Use Cases**:
- API keys and credentials
- Database connection strings
- Feature flags
- Service endpoints

**Patterns**:
```yaml
services:
  app:
    env_file:
      - .env.local      # Local overrides (gitignored)
      - .env.defaults   # Default values (committed)
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    secrets:
      - api_key
      - db_password

secrets:
  api_key:
    file: ./secrets/api_key.txt
  db_password:
    file: ./secrets/db_password.txt
```

**Benefits**:
- Secure secrets management (not in code)
- Environment-specific configuration
- Default values with overrides
- Docker secrets integration

---

### 4. Service Dependencies

**Capability**: Define startup order and health checks for interdependent services.

**Use Cases**:
- Database must start before application
- API gateway depends on backend services
- MCP server needs database connection

**Patterns**:
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 10s
      timeout: 5s
      retries: 3

  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
```

**Benefits**:
- Reliable startup order
- Automatic retry on failures
- Service readiness verification
- Graceful degradation

---

### 5. Network Isolation

**Capability**: Isolate service communication within Docker networks.

**Use Cases**:
- Internal services (database, cache) not exposed to host
- Multiple projects on same machine (no port conflicts)
- Security boundaries (frontend/backend isolation)

**Patterns**:
```yaml
services:
  app:
    networks:
      - frontend
      - backend
    ports:
      - "8000:8000"  # Exposed to host

  db:
    networks:
      - backend      # Only backend network (not exposed)

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

**Benefits**:
- Service isolation
- Port conflict prevention
- Security boundaries
- Multi-project support

---

### 6. Development Workflow Support

**Capability**: Support hybrid workflows (local Python + Docker services) and full containerization.

**Use Cases**:
- Run Python locally, databases in Docker
- Full containerization for production parity
- Mix local tools (IDE, debugger) with Docker services

**Patterns**:
```yaml
# Hybrid: Local Python + Docker services
services:
  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"  # Exposed for local Python
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"  # Exposed for local Python

# Full: Everything in Docker
services:
  app:
    build: .
    volumes:
      - .:/workspace
    depends_on:
      - db
      - redis
  # ... (db, redis without port exposure)
```

**Benefits**:
- Flexibility (choose local vs. Docker per service)
- Fast iteration (local Python debugging)
- Production parity (full containerization)
- IDE support (local Python with Docker services)

---

## Integration Points

### With chora-base

**SAP-003 (Project Bootstrap)**:
- chora-base project structure compatible with Docker Compose
- `pyproject.toml` configurations work in containers
- Test frameworks (pytest) run in Docker

**SAP-014 (MCP Server Development)**:
- MCP servers deployable via Docker Compose
- Client configuration for containerized servers
- Multi-server orchestration patterns

**SAP-004 (Testing Framework)**:
- Run pytest in containers
- Test databases in Docker
- CI/CD integration patterns

### With chora-compose

**Repository**: https://github.com/liminalcommons/chora-compose

**chora-compose provides**:
- Pre-configured compose files for common stacks
- AI agent development environments
- Service templates (databases, monitoring, APIs)
- Workflow automation integration (n8n, MCP gateway)

**Integration Patterns**:
- Import chora-compose services into your project
- Extend chora-compose configurations
- Reference chora-compose templates

---

## Adoption Metrics

### Success Indicators

**Quantitative**:
- Integration time < 1 hour (first time)
- Environment setup time < 5 minutes (docker compose up)
- Zero "works on my machine" incidents
- 100% environment reproducibility

**Qualitative**:
- Developers prefer Docker workflow over local
- Onboarding new team members < 30 minutes
- CI/CD pipeline uses Docker
- Production environments use Docker

### Risk Indicators

**Quantitative**:
- Container startup failures > 10%
- Volume mount issues > 5%
- Network connectivity problems > 5%
- Build time > 5 minutes

**Qualitative**:
- Developers avoid Docker (too complex)
- Frequent "container not starting" complaints
- Volume sync problems (code changes not reflected)
- Performance issues (slower than local)

---

## Related SAPs

### Prerequisites

**SAP-003: Project Bootstrap** - chora-base project structure required for integration

### Recommended

**SAP-014: MCP Server Development** - For deploying MCP servers via Docker Compose
**SAP-004: Testing Framework** - For running tests in Docker containers
**SAP-018: chora-compose Meta** - For comprehensive chora-compose architecture understanding

### Future Integration

**SAP-XXX: CI/CD Pipeline** (future) - Docker-based build and deployment
**SAP-XXX: Production Deployment** (future) - Docker Compose in production

---

## Version History

### v1.0.0 (2025-10-29) - Initial Release

**Features**:
- 6 core capabilities documented
- Integration patterns with chora-base and chora-compose
- Adoption metrics and risk indicators
- Cross-references to related SAPs

**Scope**:
- Docker Compose integration patterns
- Volume management and environment configuration
- Service dependency coordination
- Development workflow support

---

## Related Documentation

**SAP-017 Artifacts**:
- [adoption-blueprint.md](adoption-blueprint.md) - Integration guide
- [awareness-guide.md](awareness-guide.md) - SAPP navigation

**User Documentation**:
- [How to Integrate chora-compose](../../user-docs/how-to/integrate-chora-compose.md) - Quick start guide

**External Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Docker Compose configurations and templates
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Official Docker Compose docs

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
