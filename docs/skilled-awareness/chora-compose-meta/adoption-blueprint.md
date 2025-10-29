# SAP-018: chora-compose Meta - Adoption Blueprint

**SAP ID**: SAP-018
**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active

---

## Overview

This blueprint provides meta-level adoption guidance for chora-compose at organizational, team, and project levels. It covers decision frameworks, rollout strategies, migration paths, success metrics, and governance patterns.

**Audience**: Engineering leaders, architects, platform engineers planning chora-compose adoption
**Prerequisites**: Understanding of [design-philosophy.md](design-philosophy.md) and [architecture-overview.md](architecture-overview.md)
**Related**: [SAP-017](../chora-compose-integration/adoption-blueprint.md) for project-level integration steps

---

## Decision Framework

### Should We Adopt chora-compose?

**Decision Tree**:

```
Do you have multiple developers?
├─ No: Docker Compose still useful (environment reproducibility)
└─ Yes: Continue

Do developers work on multiple projects?
├─ No: Consider, but lower priority
└─ Yes: Continue

Do you use external services (databases, APIs, caches)?
├─ No: Limited value (containerizing simple scripts)
└─ Yes: Continue

Are developers struggling with environment setup?
├─ No: Current process works, chora-compose optional
└─ Yes: **Strong candidate for adoption**

Is "works on my machine" a common problem?
├─ No: Current consistency acceptable
└─ Yes: **Strong candidate for adoption**

Do you need production parity in development?
├─ No: Simple local development sufficient
└─ Yes: **Strong candidate for adoption**
```

**Adoption Scorecard**:

| Criterion | Weight | Score (0-5) | Weighted |
|-----------|--------|-------------|----------|
| Team size (1=solo, 5=10+) | 20% | ___ | ___ |
| Multi-project work | 15% | ___ | ___ |
| Service dependencies | 25% | ___ | ___ |
| Environment consistency issues | 25% | ___ | ___ |
| Onboarding time (1=days, 5=hours) | 15% | ___ | ___ |
| **Total** | **100%** | | ___ |

**Interpretation**:
- **4.0-5.0**: Strong fit - proceed with adoption
- **3.0-3.9**: Good fit - pilot first, then adopt
- **2.0-2.9**: Marginal fit - pilot carefully, consider alternatives
- **< 2.0**: Poor fit - don't adopt (use alternatives)

---

## Adoption Strategies

### Strategy 1: Greenfield Projects (Fastest)

**Approach**: New projects start with chora-compose from day 1.

**Timeline**: 1-2 weeks

**Steps**:
1. **Week 1**: Create template repository with chora-compose
2. **Week 1**: Document standard patterns (db, cache, services)
3. **Week 1**: Train team (1-2 hour workshop)
4. **Week 2**: First project uses template
5. **Week 2**: Iterate on template based on feedback

**Benefits**:
- ✅ No migration complexity
- ✅ Fast adoption (immediate value)
- ✅ Clean patterns from start

**Trade-offs**:
- ❌ Existing projects still inconsistent
- ❌ Team split between old/new patterns

**When to Use**: Startups, new teams, new product lines

---

### Strategy 2: Pilot Projects (Safest)

**Approach**: Adopt on 2-3 pilot projects, refine, then expand.

**Timeline**: 4-8 weeks

**Steps**:
1. **Week 1-2**: Select pilot projects (diverse complexity)
2. **Week 2-4**: Integrate chora-compose, document learnings
3. **Week 4-6**: Refine patterns, create templates
4. **Week 6-8**: Expand to more projects

**Pilot Project Selection Criteria**:
- **Project 1**: Simple (1-2 services) - quick win
- **Project 2**: Medium (3-5 services) - representative
- **Project 3**: Complex (6+ services) - stress test

**Benefits**:
- ✅ Risk mitigation (fail fast on pilot)
- ✅ Pattern validation before scale
- ✅ Team confidence building

**Trade-offs**:
- ❌ Slower adoption (4-8 weeks)
- ❌ Temporary inconsistency

**When to Use**: Established teams, risk-averse organizations

---

### Strategy 3: Incremental Migration (Pragmatic)

**Approach**: Migrate existing projects gradually, prioritize by impact.

**Timeline**: 3-6 months

**Steps**:
1. **Month 1**: Assess all projects (complexity, value)
2. **Month 1-2**: Migrate high-impact projects (frequently worked on)
3. **Month 2-4**: Migrate medium-impact projects
4. **Month 4-6**: Migrate low-impact projects (or archive)

**Prioritization Matrix**:

| Project | Frequency | Complexity | Priority |
|---------|-----------|------------|----------|
| Active daily | Any | **P0** (migrate first) |
| Active weekly | Low-Medium | **P1** |
| Active weekly | High | **P1-P2** (may need refactoring) |
| Active monthly | Any | **P2** |
| Archived/Rarely | Any | **P3** (migrate on-demand or never) |

**Benefits**:
- ✅ Value-driven prioritization
- ✅ Gradual team adaptation
- ✅ Budget-friendly (spread over time)

**Trade-offs**:
- ❌ Long tail (some projects never migrated)
- ❌ Temporary inconsistency across portfolio

**When to Use**: Large organizations, many existing projects

---

## Migration Paths

### From Bare Metal / Local Installation

**Current State**: Developers install services locally (brew, apt, etc.)

**Migration Steps**:

1. **Inventory Services**:
   ```bash
   # Document what's installed locally
   - PostgreSQL 13 (brew)
   - Redis 6 (brew)
   - Python 3.9 (system)
   ```

2. **Create docker-compose.yml**:
   ```yaml
   services:
     db:
       image: postgres:13-alpine  # Match current version
       ports:
         - "5432:5432"  # Expose for hybrid dev
       environment:
         - POSTGRES_PASSWORD=dev
       volumes:
         - postgres-data:/var/lib/postgresql/data

     redis:
       image: redis:6-alpine  # Match current version
       ports:
         - "6379:6379"
   ```

3. **Hybrid Phase** (2-4 weeks):
   - Docker services running
   - Python still local (minimize disruption)
   - Update connection strings (localhost → localhost, no change)

4. **Full Containerization** (optional):
   - Add `app` service to docker-compose.yml
   - Move Python to container
   - Volume mount source code

**Timeline**: 2-4 weeks (hybrid), +2 weeks (full containerization)

---

### From Kubernetes Development

**Current State**: Developers use Minikube/Kind for local K8s.

**Migration Steps**:

1. **Export K8s Manifests**:
   ```bash
   kubectl get deployment,service,configmap -o yaml > k8s-resources.yaml
   ```

2. **Convert to Compose** (use Kompose):
   ```bash
   kompose convert -f k8s-resources.yaml -o docker-compose.yml
   ```

3. **Simplify** (remove K8s-specific features):
   - Remove namespaces
   - Simplify health checks
   - Convert secrets to environment variables (.env.local)
   - Remove ingress (use direct ports)

4. **Test Parity**:
   - Compare functionality (K8s vs. Compose)
   - Document differences
   - Update documentation

**Timeline**: 2-4 weeks

**When to Keep K8s Dev**:
- Production uses K8s-specific features (operators, CRDs)
- Need exact K8s parity
- Team prefers K8s tooling

---

### From Docker (Ad-hoc Commands)

**Current State**: Developers run manual `docker run` commands.

**Migration Steps**:

1. **Document Current Commands**:
   ```bash
   docker run -d --name postgres -e POSTGRES_PASSWORD=dev postgres:15
   docker run -d --name redis redis:7
   docker run -it --link postgres --link redis my-app
   ```

2. **Convert to docker-compose.yml**:
   ```yaml
   services:
     postgres:
       image: postgres:15
       environment:
         - POSTGRES_PASSWORD=dev
       volumes:
         - postgres-data:/var/lib/postgresql/data

     redis:
       image: redis:7
       volumes:
         - redis-data:/data

     app:
       build: .
       depends_on:
         - postgres
         - redis
   ```

3. **Replace Manual Commands**:
   ```bash
   # Old: 5+ commands
   docker run -d --name postgres ...
   docker run -d --name redis ...
   ...

   # New: 1 command
   docker compose up -d
   ```

**Timeline**: 1 week

---

## Rollout Patterns

### Pattern 1: Top-Down (Leadership-Driven)

**Approach**: Leadership mandates chora-compose adoption.

**Steps**:
1. **Leadership Decision**: "All new projects use chora-compose"
2. **Platform Team**: Create templates, documentation
3. **Training**: Company-wide workshops
4. **Enforcement**: Code review requirements, CI checks

**Benefits**:
- ✅ Fast adoption (months, not years)
- ✅ Consistent patterns
- ✅ Platform team support

**Trade-offs**:
- ❌ Potential resistance (mandate, not choice)
- ❌ Initial productivity dip (learning curve)

**When to Use**: Strong platform team, clear leadership, urgent consistency needs

---

### Pattern 2: Bottom-Up (Team-Driven)

**Approach**: Individual teams adopt, success spreads organically.

**Steps**:
1. **Early Adopter Team**: Tries chora-compose
2. **Success Story**: Shares benefits (faster onboarding, fewer issues)
3. **Other Teams**: Adopt voluntarily
4. **Platform Team**: Codifies patterns later

**Benefits**:
- ✅ Organic adoption (no resistance)
- ✅ Real-world validation
- ✅ Team buy-in

**Trade-offs**:
- ❌ Slow adoption (6-12 months)
- ❌ Inconsistent patterns (each team diverges)

**When to Use**: Decentralized organizations, experimental culture

---

### Pattern 3: Center of Excellence

**Approach**: Dedicated team drives adoption, provides support.

**Steps**:
1. **Form CoE**: 2-4 experts, part-time or full-time
2. **Create Assets**: Templates, documentation, training materials
3. **Provide Support**: Office hours, Slack channel, pairing sessions
4. **Measure Success**: Adoption metrics, satisfaction surveys

**Benefits**:
- ✅ Expert support available
- ✅ Consistent guidance
- ✅ Knowledge centralization

**Trade-offs**:
- ❌ Resource investment (CoE staffing)
- ❌ Potential bottleneck (CoE capacity)

**When to Use**: Large organizations (100+ developers), complex migrations

---

## Success Metrics

### Adoption Metrics

**Quantitative**:
- **Adoption Rate**: % of projects using chora-compose
  - Target: 80% of active projects within 6 months
- **Onboarding Time**: Time to first successful local run
  - Target: < 5 minutes (from clone to running)
- **Environment Consistency**: % of developers with identical environments
  - Target: 100%
- **"Works on My Machine" Incidents**: Count per month
  - Target: < 1 per team per month

**Qualitative**:
- Developer satisfaction surveys (1-5 scale)
  - Target: 4.0+ average
- Perceived complexity (1-5, 1=simple)
  - Target: < 2.5 average
- Would recommend to others (yes/no)
  - Target: > 80% yes

---

### Operational Metrics

**Performance**:
- **Startup Time**: `docker compose up` → services ready
  - Target: < 30 seconds
- **Rebuild Time**: Code change → rebuild complete
  - Target: < 2 minutes
- **Resource Usage**: Docker Desktop RAM/CPU
  - Target: < 4GB RAM, < 50% CPU

**Reliability**:
- **Container Failures**: Services crash rate
  - Target: < 1% daily
- **Network Issues**: Connection refused errors
  - Target: < 5% occurrence
- **Volume Issues**: Mount failures, sync problems
  - Target: < 2% occurrence

---

## Governance

### Template Management

**Centralized Template Repository**:
```
org/docker-compose-templates/
├── python-web/          # Flask/FastAPI template
├── python-mcp/          # MCP server template
├── python-cli/          # CLI tool template
└── shared/              # Shared configs
    ├── databases.yml
    ├── caching.yml
    └── monitoring.yml
```

**Update Process**:
1. **Proposal**: Team member proposes template change
2. **Review**: CoE/platform team reviews
3. **Pilot**: Test on 1-2 projects
4. **Rollout**: Update template, announce to teams
5. **Documentation**: Update SAP-017/018

**Versioning**:
```yaml
# docker-compose.yml
# Template Version: 2.1.0
# Last Updated: 2025-10-29
# Changelog: Added Redis Sentinel support
```

---

### Standards and Conventions

**Naming Conventions**:
- Service names: Lowercase, descriptive (app, db, redis)
- Container names: {project}-{service} (myproject-app)
- Volume names: {service}-data (postgres-data)
- Network names: {project}-network

**Port Allocation**:
- Reserve port ranges per team/project
- Document in shared registry
- Avoid conflicts

**Environment Variables**:
- Always use `.env.local` (gitignored)
- Provide `.env.example` (committed)
- Document required variables in README

---

## Common Pitfalls

### Pitfall 1: Over-Engineering Templates

**Symptom**: Templates have 20+ services, 500+ line docker-compose.yml

**Problem**: Cognitive overload, slow startup, hard to understand

**Solution**:
- Start minimal (app + database)
- Add services incrementally
- Use compose profiles for optional services

```yaml
services:
  monitoring:
    image: prometheus
    profiles: ["monitoring"]  # Optional, enable with --profile
```

---

### Pitfall 2: Ignoring Performance

**Symptom**: 5+ minute startup times, slow file operations

**Problem**: Poor DX, developers revert to local installation

**Solution**:
- Use Alpine images (smaller, faster)
- Implement `:delegated` volumes (macOS/Windows)
- Cache dependencies (pip-cache, node_modules)
- Use tmpfs for ephemeral data

---

### Pitfall 3: No Migration Plan

**Symptom**: "Everyone switch to Docker" announcement, chaos ensues

**Problem**: Disrupts productivity, no support, teams frustrated

**Solution**:
- Pilot first (2-3 projects)
- Provide migration guide
- Offer support (office hours, pairing)
- Allow hybrid phase (gradual transition)

---

## Related Documentation

**SAP-018 Artifacts**:
- [capability-charter.md](capability-charter.md) - Core capabilities and business value
- [architecture-overview.md](architecture-overview.md) - Technical architecture
- [design-philosophy.md](design-philosophy.md) - Design principles
- [integration-patterns.md](integration-patterns.md) - Implementation patterns

**Related SAPs**:
- [SAP-017: chora-compose Integration](../chora-compose-integration/) - Project-level integration
- [SAP-003: Project Bootstrap](../project-bootstrap/) - chora-base structure

**External Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Templates and examples

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Active
